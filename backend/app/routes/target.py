"""Target selection + skill baseline — P0: personal starting path.

Reuses existing infrastructure:
- exam engine for diagnostic attempt persistence/scoring
- assessment_blueprint.select_questions for role-specific question selection
- skill_assessment for baseline mastery (skill_graph)
- role_engine.profiles for role/company definitions
- adaptive_learning.generate_learning_path for the preparation path
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
from app.middleware.auth import get_current_user
from app.database import users_collection, skill_graph_collection, get_collection
from bson import ObjectId
from app.services.exam_engine import score_question
from app.services.assessment_blueprint import select_questions
from app.services.skill_assessment import (
    initialize_skill_graph,
    update_skill_score,
    get_skill_graph,
    SKILL_CATEGORIES,
)
from app.services.role_engine.profiles import get_profile, list_profiles
from app.services.adaptive_learning import generate_learning_path

router = APIRouter(prefix="/api/v1/target", tags=["target"])

COLLECTION = get_collection("target_attempts")


class TargetSelectReq(BaseModel):
    company: Optional[str] = None
    role: str = "sde"
    language: str = "python"
    experience_level: str = "fresher"
    study_hours_per_week: int = 10
    target_date: Optional[str] = None


class DiagnosticAnswer(BaseModel):
    attempt_id: str
    question_id: str
    answer: Any


# ────────────────────────────────────────────────────────────
# Role / company metadata
# ────────────────────────────────────────────────────────────
@router.get("/roles")
async def list_roles():
    return {"roles": list_profiles()}


@router.get("/companies")
async def list_companies(role: Optional[str] = Query(None)):
    profile = get_profile(role or "sde")
    companies = [c.name for c in (profile.target_companies if profile else [])]
    return {"companies": companies}


# ────────────────────────────────────────────────────────────
# Target selection
# ────────────────────────────────────────────────────────────
@router.post("/select")
async def select_target(req: TargetSelectReq, user=Depends(get_current_user)):
    profile = {
        "company": req.company,
        "role": req.role,
        "language": req.language,
        "experience_level": req.experience_level,
        "study_hours_per_week": req.study_hours_per_week,
        "target_date": req.target_date,
        "selected_at": datetime.now(timezone.utc).isoformat(),
        "baseline_computed": False,
    }
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"target": profile}},
        upsert=True,
    )
    return {"target": profile, "message": "Target selected. Run diagnostic to set your baseline."}


# ────────────────────────────────────────────────────────────
# Diagnostic: start / answer / complete
# ────────────────────────────────────────────────────────────
def _candidate_topics(role: str) -> List[str]:
    profile = get_profile(role)
    if not profile:
        return []
    topics: List[str] = []
    for skill in profile.required_skills:
        for tag in skill.tags:
            topics.append(tag.lower().replace(" ", "_"))
    # dedupe preserve order
    seen = set()
    out = []
    for t in topics:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


@router.post("/diagnostic/start")
async def start_diagnostic(user=Depends(get_current_user)):
    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    target = db_user.get("target") if db_user else None
    role = (target or {}).get("role", "sde")
    topics = _candidate_topics(role)

    questions: List[dict] = []
    for topic in topics[:4]:
        qs = select_questions(topic=topic, total=2, seed=42)
        questions.extend(qs)
    if len(questions) < 6:
        qs = select_questions(total=6, seed=42)
        existing_ids = {q.get("id") for q in questions}
        for q in qs:
            if q.get("id") not in existing_ids:
                questions.append(q)
    questions = questions[:10]

    safe_qs = []
    for q in questions:
        safe_qs.append({
            "id": q.get("id") or q.get("_id"),
            "question": q.get("question") or q.get("text"),
            "options": q.get("options"),
            "difficulty": q.get("difficulty"),
            "topic": q.get("topic"),
            "sub_topic": q.get("sub_topic"),
        })

    attempt_id = str(uuid.uuid4())
    doc = {
        "attempt_id": attempt_id,
        "user_id": user["id"],
        "role": role,
        "questions": questions,  # full with answers, server-side only
        "answers": {},
        "started_at": datetime.now(timezone.utc),
        "completed_at": None,
        "score": None,
        "total": len(questions),
        "kind": "target_diagnostic",
    }
    await COLLECTION.insert_one(doc)
    return {
        "attempt_id": attempt_id,
        "role": role,
        "total": len(safe_qs),
        "questions": safe_qs,
    }


@router.post("/diagnostic/answer")
async def diagnostic_answer(req: DiagnosticAnswer, user=Depends(get_current_user)):
    attempt = await COLLECTION.find_one({"attempt_id": req.attempt_id, "user_id": user["id"]})
    if not attempt:
        raise HTTPException(status_code=404, detail="attempt not found")
    if attempt.get("completed_at"):
        raise HTTPException(status_code=400, detail="attempt already completed")
    answers = attempt.get("answers") or {}
    answers[req.question_id] = req.answer
    await COLLECTION.update_one(
        {"attempt_id": req.attempt_id},
        {"$set": {"answers": answers}},
    )
    return {"saved": True}


@router.post("/diagnostic/complete")
async def diagnostic_complete(user=Depends(get_current_user)):
    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    target = db_user.get("target") if db_user else None
    role = (target or {}).get("role", "sde")

    # Find the most recent incomplete-or-complete diagnostic for this user
    attempt = await COLLECTION.find_one(
        {"user_id": user["id"], "kind": "target_diagnostic"},
        sort=[("started_at", -1)],
    )
    if not attempt:
        raise HTTPException(status_code=404, detail="no diagnostic attempt found")
    if attempt.get("completed_at"):
        # already completed; return existing baseline
        return await _get_profile(user["id"])

    questions = attempt.get("questions") or []
    answers = attempt.get("answers") or {}

    correct = 0
    review = []
    topic_stats: Dict[str, Dict[str, Any]] = {}
    for q in questions:
        qid = q.get("id")
        ua = answers.get(qid)
        sr = score_question(q, ua)
        if sr["is_correct"]:
            correct += 1
        topic = sr["pattern"] or q.get("topic") or "general"
        stats = topic_stats.setdefault(topic, {"correct": 0, "total": 0})
        stats["total"] += 1
        if sr["is_correct"]:
            stats["correct"] += 1
        review.append({
            "id": qid,
            "question": q.get("question") or q.get("text"),
            "your_answer": ua,
            "correct_answer": sr["correct_answer"],
            "correct": sr["is_correct"],
            "explanation": q.get("explanation"),
            "topic": topic,
        })

    score_pct = round((correct / len(questions)) * 100, 2) if questions else 0.0
    await COLLECTION.update_one(
        {"attempt_id": attempt["attempt_id"]},
        {"$set": {"completed_at": datetime.now(timezone.utc), "score": score_pct, "correct": correct}},
    )

    # Persist baseline mastery per topic into skill_graph
    skill_graph = await skill_graph_collection.find_one({"user_id": user["id"]})
    if not skill_graph:
        skill_graph = await initialize_skill_graph(user["id"])

    category_map = {
        "arrays": "dsa", "strings": "dsa", "linked_lists": "dsa", "stacks_queues": "dsa",
        "trees": "dsa", "graphs": "dsa", "hashing": "dsa", "sorting": "dsa", "searching": "dsa",
        "dynamic_programming": "dsa", "recursion": "dsa", "greedy": "dsa", "binary_search": "dsa",
        "loops": "dsa", "basic_complexity": "dsa",
    }
    for topic, stats in topic_stats.items():
        accuracy = (stats["correct"] / stats["total"]) * 100 if stats["total"] else 0
        category = category_map.get(topic.lower(), "dsa")
        await update_skill_score(
            user_id=user["id"],
            category=category,
            skill=topic,
            score=round(accuracy, 2),
            is_correct=accuracy >= 70,
        )

    # Mark baseline computed on target profile
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"target.baseline_computed": True, "target.baseline_score": score_pct}},
    )

    # Generate the preparation path from the new baseline
    path = await generate_learning_path(user["id"], target_company=target.get("company") if target else None)

    return {
        "attempt_id": attempt["attempt_id"],
        "role": role,
        "score": score_pct,
        "correct": correct,
        "total": len(questions),
        "baseline": {topic: {"correct": s["correct"], "total": s["total"], "accuracy": round((s["correct"]/s["total"])*100, 1) if s["total"] else 0} for topic, s in topic_stats.items()},
        "review": review,
        "path": path,
    }


# ────────────────────────────────────────────────────────────
# Profile
# ────────────────────────────────────────────────────────────
async def _get_profile(user_id: str) -> dict:
    db_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    target = db_user.get("target") if db_user else None
    skill_graph = await get_skill_graph(user_id)
    # flatten skill graph into per-topic baseline
    baseline = {}
    for cat_id, cat_data in (skill_graph.get("categories") or {}).items():
        for skill_name, skill_data in (cat_data.get("skills") or {}).items():
            baseline[skill_name] = {
                "category": cat_id,
                "score": skill_data.get("score", 0),
                "attempts": skill_data.get("attempts", 0),
                "label": "mastered" if skill_data.get("score", 0) >= 85 else ("learning" if skill_data.get("score", 0) >= 40 else ("practicing" if skill_data.get("attempts", 0) > 0 else "untouched")),
            }
    path = await generate_learning_path(user_id, target_company=target.get("company") if target else None)
    return {
        "target": target,
        "baseline": baseline,
        "path": path,
    }


@router.get("/profile")
async def target_profile(user=Depends(get_current_user)):
    return await _get_profile(user["id"])
