"""Study Engine routes — the single canonical daily-learning API.

Per the canonical architecture:

    Curriculum decides WHAT is learned.
    Study Engine decides WHAT HAPPENS NEXT  ← this file
    Mastery decides WHETHER it was learned.
    Gamification REWARDS the outcome.
    Readiness reports career preparedness.

The home screen calls ``GET /api/v1/study/today`` and renders whatever
shape the Study Engine returns — the frontend does not need to know
which subsystem (curriculum, SRS, adaptive learning, gamification)
supplied each activity.

Legacy endpoints:

    * ``GET /api/v1/adaptive/daily-plan`` — kept as a thin alias so
      existing frontends keep working; new code should prefer
      ``/study/today``.
"""

import asyncio
import random
import time
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, HTTPException

from app.middleware.auth import get_current_user
from app.services.study_engine import get_today, record_activity
from app.database import practice_sessions_collection

router = APIRouter(prefix="/api/v1/study", tags=["study-engine"])


@router.get("/today")
async def today(force: bool = Query(False, description="Force refresh the daily plan"), user=Depends(get_current_user)):
    """Return the canonical daily learning plan for the authenticated user."""
    plan = await get_today(user["id"], force_refresh=force)

    # Beta funnel: track first activation (first time getting a plan)
    try:
        from app.services.analytics_service import track_event
        asyncio.create_task(track_event(
            event="beta_activation",
            path="/api/v1/study/today",
            user_id=user["id"],
            meta={"has_next": bool(plan.get("next"))},
        ))
    except Exception:
        pass

    return plan


@router.get("/prerequisites/{target_skill_id}")
async def prerequisite_learning_step(
    target_skill_id: str,
    user=Depends(get_current_user),
):
    """Return the next prerequisite lesson/diagnostic step for a target skill.

    Progress is derived from persisted, distinct server-graded question-bank
    events. Client-provided scores and lesson-completion flags are not accepted.
    """
    from app.services.prerequisite_graph import get_user_prerequisite_learning_step

    result = await get_user_prerequisite_learning_step(
        user["id"],
        target_skill_id,
    )
    return {"success": True, **result}


@router.post("/activity")
async def log_activity(activity: dict, user=Depends(get_current_user)):
    """Record a completed learning activity and fan-out to mastery / SRS / Diamonds."""
    result = await record_activity(user["id"], activity, role=user.get("role") or user.get("target_role") or "sde")

    # Beta funnel: track first mission completion
    try:
        if activity.get("type") == "learn" and activity.get("passed"):
            from app.services.analytics_service import track_event
            asyncio.create_task(track_event(
                event="beta_first_mission_complete",
                path="/api/v1/study/activity",
                user_id=user["id"],
                meta={
                    "skill_id": activity.get("skill_id"),
                    "score": activity.get("score"),
                    "time_spent": activity.get("time_spent"),
                },
            ))
    except Exception:
        pass

    return {"success": True, "data": result}


@router.post("/prerequisites/{target_skill_id}/assessment")
async def build_prerequisite_assessment(target_skill_id: str, user=Depends(get_current_user)):
    """Create a server-graded, unseen-question assessment for one exact prerequisite."""
    from app.services.prerequisite_graph import SKILL_PREREQUISITES, get_user_prerequisite_learning_step
    from app.services.quiz_service import get_all_questions
    from app.services.skill_taxonomy import canonical_skill_id

    if target_skill_id not in SKILL_PREREQUISITES:
        raise HTTPException(status_code=404, detail="Unknown prerequisite skill.")
    step = await get_user_prerequisite_learning_step(user["id"], target_skill_id)
    next_step = step.get("next_step") or {}
    if next_step.get("kind") not in {"diagnostic_assessment", "teach_and_reassess"}:
        raise HTTPException(status_code=409, detail="This skill has no unresolved prerequisite assessment.")
    skill_id = next_step.get("skill_id")
    if not skill_id:
        raise HTTPException(status_code=409, detail="No prerequisite is available to assess.")

    prior = await practice_sessions_collection.find({
        "user_id": user["id"], "session_type": "prerequisite_assessment",
        "prerequisite_skill_id": skill_id,
    }).to_list(500)
    seen = {
        str(qid) for session in prior
        for qid in (session.get("question_ids") or [])
    }
    candidates = []
    for question in get_all_questions():
        qid = str(question.get("id") or "")
        if not qid or qid in seen:
            continue
        if not (str(question.get("correct_answer") or "").strip()
                or (question.get("options") and question.get("correct_index") is not None)):
            continue
        mapped = None
        for field in ("sub_topic", "topic", "pattern", "domain", "canonical_skill", "skill_id"):
            raw = question.get(field)
            if raw:
                mapped = canonical_skill_id(str(raw))
                if mapped == skill_id:
                    break
        if mapped == skill_id:
            candidates.append(question)
    if not candidates:
        raise HTTPException(status_code=404, detail="No unseen, server-gradable questions are currently authored for this exact prerequisite.")
    selected = random.sample(candidates, min(5, len(candidates)))
    quiz_id = f"prereq_{int(time.time())}_{random.randint(1000, 9999)}"
    now = datetime.now(timezone.utc)
    await practice_sessions_collection.insert_one({
        "user_id": user["id"], "session_type": "prerequisite_assessment",
        "quiz_id": quiz_id, "prerequisite_skill_id": skill_id,
        "target_skill_id": target_skill_id,
        "question_ids": [str(q["id"]) for q in selected],
        "answers": [], "status": "in_progress",
        "created_at": now, "updated_at": now,
    })
    return {
        "success": True, "quiz_id": quiz_id, "skill_id": skill_id,
        "target_skill_id": target_skill_id,
        "questions": [{
            "id": str(q["id"]), "question": q.get("question") or q.get("title") or "",
            "title": q.get("title") or "Practice question",
            "options": q.get("options") or [],
            "difficulty": q.get("difficulty") or "medium",
            "type": q.get("type") or ("mcq" if q.get("options") else "short_answer"),
        } for q in selected],
    }


@router.post("/prerequisites/assessment/answer")
async def answer_prerequisite_assessment(payload: dict, user=Depends(get_current_user)):
    """Grade an answer against the bank key and persist canonical prerequisite evidence."""
    from app.services.quiz_service import submit_quiz_answer
    from app.services.study_engine import emit_learning_event

    quiz_id = str(payload.get("quiz_id") or "")
    question_id = str(payload.get("question_id") or "")
    user_answer = str(payload.get("user_answer") or "")
    if not quiz_id or not question_id or not user_answer:
        raise HTTPException(status_code=422, detail="quiz_id, question_id and user_answer are required.")
    session = await practice_sessions_collection.find_one({
        "user_id": user["id"], "quiz_id": quiz_id,
        "session_type": "prerequisite_assessment",
    })
    if not session or session.get("status") != "in_progress":
        raise HTTPException(status_code=404, detail="Active prerequisite assessment not found.")
    if question_id not in (session.get("question_ids") or []):
        raise HTTPException(status_code=403, detail="Question was not issued in this assessment.")
    if any(a.get("question_id") == question_id for a in (session.get("answers") or [])):
        raise HTTPException(status_code=409, detail="This question has already been answered.")
    result = submit_quiz_answer(
        quiz_id=quiz_id, question_id=question_id, user_answer=user_answer,
        time_taken_seconds=max(0, min(float(payload.get("time_taken_seconds") or 0), 86400)),
        hints_used=0,
    )
    if result.get("error") or result.get("requires_code_execution"):
        raise HTTPException(status_code=422, detail=result.get("error") or "This question requires code execution.")
    passed = bool(result.get("is_correct"))
    now = datetime.now(timezone.utc)
    claimed = await practice_sessions_collection.update_one({
        "user_id": user["id"], "quiz_id": quiz_id,
        "session_type": "prerequisite_assessment", "status": "in_progress",
        "question_ids": question_id, "answers.question_id": {"$ne": question_id},
    }, {"$push": {"answers": {
        "question_id": question_id, "is_correct": passed,
        "answered_at": now, "time_taken_seconds": max(0, min(float(payload.get("time_taken_seconds") or 0), 86400)),
    }}, "$set": {"updated_at": now}})
    if not claimed.modified_count:
        raise HTTPException(status_code=409, detail="Answer already submitted or assessment closed.")
    await emit_learning_event(user["id"], {
        "activity_type": "practice", "source": "question_bank",
        "skill_id": session["prerequisite_skill_id"],
        "question_id": question_id, "assessment_id": quiz_id,
        "passed": passed, "score": 100 if passed else 0,
        "time_spent_seconds": int(max(0, min(float(payload.get("time_taken_seconds") or 0), 86400))),
        "hints_used": 0, "attempt_number": 1,
    })
    updated = await practice_sessions_collection.find_one({
        "user_id": user["id"], "quiz_id": quiz_id,
        "session_type": "prerequisite_assessment",
    })
    if len(updated.get("answers") or []) >= len(updated.get("question_ids") or []):
        await practice_sessions_collection.update_one(
            {"user_id": user["id"], "quiz_id": quiz_id},
            {"$set": {"status": "completed", "completed_at": now}},
        )
    return {
        "success": True, "is_correct": passed,
        "explanation": result.get("explanation") or "",
        "assessment_complete": len(updated.get("answers") or []) >= len(updated.get("question_ids") or []),
    }
