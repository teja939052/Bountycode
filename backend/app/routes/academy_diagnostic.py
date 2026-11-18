"""Baseline placement diagnostic using trusted, server-graded question-bank items."""
from datetime import datetime, timezone
import random
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.database import get_collection
from app.middleware.auth import get_current_user
from app.services.quiz_service import get_all_questions, get_question_by_id
from app.services.adaptive_learning import record_learning_activity

router = APIRouter(prefix="/api/v1/academy/diagnostic", tags=["academy-diagnostic"])
_sessions = lambda: get_collection("academy_diagnostic_sessions")

DOMAIN_ALIASES = {
    "programming fundamentals": "programming_fundamentals",
    "programming logic": "programming_fundamentals",
    "quantitative aptitude": "quantitative_aptitude",
    "aptitude": "quantitative_aptitude",
    "logical reasoning": "logical_reasoning",
    "reasoning": "logical_reasoning",
    "verbal ability": "verbal_ability",
    "computer science fundamentals": "computer_science",
    "computer science": "computer_science",
    "sql": "sql",
    "database": "sql",
    "dsa": "arrays_hashing",
    "arrays": "arrays_hashing",
}

DOMAIN_LABELS = {
    "programming_fundamentals": "Programming fundamentals",
    "arrays_hashing": "DSA and problem solving",
    "quantitative_aptitude": "Quantitative aptitude",
    "logical_reasoning": "Logical reasoning",
    "verbal_ability": "Verbal ability",
    "computer_science": "Computer science fundamentals",
    "sql": "SQL and databases",
}


def canonical_domain(question: Dict[str, Any]) -> Optional[str]:
    for field in ("domain", "sub_topic", "topic", "pattern"):
        raw = str(question.get(field) or "").strip().lower()
        if not raw:
            continue
        normalized = raw.replace("-", "_").replace(" ", "_")
        if raw in DOMAIN_ALIASES:
            return DOMAIN_ALIASES[raw]
        if normalized in DOMAIN_LABELS:
            return normalized
        if normalized in {"array", "arrays_hashing", "hashing"}:
            return "arrays_hashing"
        if normalized in {"programming_fundamentals", "programming_logic"}:
            return "programming_fundamentals"
        if normalized in {"quantitative_aptitude", "logical_reasoning", "verbal_ability", "computer_science", "sql"}:
            return normalized
    # Unknown metadata is not evidence of a programming skill. Keep it
    # unclassified instead of silently contaminating that domain score.
    return None


def has_deterministic_key(question: Dict[str, Any]) -> bool:
    return (
        question.get("correct_index") is not None and bool(question.get("options"))
    ) or bool(str(question.get("correct_answer") or "").strip())


def grade_diagnostic_answer(question: Dict[str, Any], answer: str) -> bool:
    if question.get("correct_index") is not None and question.get("options"):
        try:
            selected = int(answer)
            return selected == int(question["correct_index"])
        except (TypeError, ValueError):
            return False
    expected = str(question.get("correct_answer") or "").strip().casefold()
    return bool(expected) and str(answer).strip().casefold() == expected


def skill_level(score: float, attempts: int) -> str:
    if attempts == 0:
        return "not_assessed"
    if score < 35:
        return "foundation_needed"
    if score < 60:
        return "beginner"
    if score < 80:
        return "developing"
    return "strong"


def _public_question(question: Dict[str, Any], index: int) -> Dict[str, Any]:
    return {
        "id": question["id"],
        "index": index,
        "title": question.get("title") or question.get("topic") or "Question",
        "question": question.get("question") or question.get("prompt") or "",
        "topic": question.get("sub_topic") or question.get("topic") or "General",
        "domain": canonical_domain(question),
        "difficulty": question.get("difficulty", "medium"),
        "type": "mcq" if question.get("options") else "short_answer",
        "options": question.get("options") or [],
    }


class DiagnosticStart(BaseModel):
    questions_per_domain: int = Field(default=4, ge=2, le=8)


class DiagnosticAnswer(BaseModel):
    question_id: str = Field(min_length=1, max_length=160)
    answer: str = Field(max_length=2000)
    time_taken_seconds: int = Field(default=0, ge=0, le=3600)
    confidence: int | None = Field(default=None, ge=1, le=5)


@router.post("/start")
async def start_diagnostic(payload: DiagnosticStart, user=Depends(get_current_user)):
    bank = [
        q for q in get_all_questions()
        if q.get("id") and has_deterministic_key(q)
    ]
    buckets: Dict[str, List[dict]] = {}
    for question in bank:
        domain = canonical_domain(question)
        if domain in DOMAIN_LABELS:
            buckets.setdefault(domain, []).append(question)

    selected = []
    for domain in DOMAIN_LABELS:
        candidates = buckets.get(domain, [])
        if candidates:
            random.shuffle(candidates)
            selected.extend(candidates[:payload.questions_per_domain])
    if len(selected) < 8:
        raise HTTPException(
            status_code=503,
            detail="The diagnostic question bank needs more graded questions. Please try again later.",
        )

    random.shuffle(selected)
    diagnostic_id = f"diag_{uuid.uuid4().hex}"
    now = datetime.now(timezone.utc)
    await _sessions().insert_one({
        "user_id": user["id"],
        "diagnostic_id": diagnostic_id,
        "question_ids": [q["id"] for q in selected],
        "answers": [],
        "status": "in_progress",
        "created_at": now,
        "updated_at": now,
    })
    return {
        "success": True,
        "diagnostic": {
            "diagnostic_id": diagnostic_id,
            "total_questions": len(selected),
            "questions": [_public_question(q, i) for i, q in enumerate(selected)],
        },
    }


@router.post("/{diagnostic_id}/answer")
async def answer_diagnostic(
    diagnostic_id: str,
    payload: DiagnosticAnswer,
    user=Depends(get_current_user),
):
    session = await _sessions().find_one({
        "user_id": user["id"], "diagnostic_id": diagnostic_id,
    })
    if not session:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")
    if session.get("status") != "in_progress":
        raise HTTPException(status_code=409, detail="Diagnostic is already completed.")
    if payload.question_id not in session.get("question_ids", []):
        raise HTTPException(status_code=404, detail="Question is not part of this diagnostic.")

    existing = next(
        (a for a in session.get("answers", []) if a.get("question_id") == payload.question_id),
        None,
    )
    if existing:
        raise HTTPException(status_code=409, detail="This question has already been answered.")
    question = get_question_by_id(payload.question_id)
    if not question:
        raise HTTPException(status_code=410, detail="Question bank item is no longer available.")
    correct = grade_diagnostic_answer(question, payload.answer)
    answer_doc = {
        "question_id": payload.question_id,
        "answer": payload.answer,
        "is_correct": correct,
        "domain_id": canonical_domain(question),
        "time_taken_seconds": payload.time_taken_seconds,
        "confidence": payload.confidence,
        "answered_at": datetime.now(timezone.utc).isoformat(),
    }
    # Claim the answer atomically. The earlier read is useful for a friendly
    # error, but cannot prevent two concurrent requests from both passing it.
    write_result = await _sessions().update_one(
        {
            "user_id": user["id"],
            "diagnostic_id": diagnostic_id,
            "status": "in_progress",
            "answers.question_id": {"$ne": payload.question_id},
        },
        {"$push": {"answers": answer_doc}, "$set": {"updated_at": datetime.now(timezone.utc)}},
    )
    if not getattr(write_result, "matched_count", 0):
        raise HTTPException(status_code=409, detail="This question was already answered or the diagnostic has closed.")
    return {"success": True, "data": {"accepted": True, "answered_count": len(session.get("answers", [])) + 1}}


@router.post("/{diagnostic_id}/complete")
async def complete_diagnostic(diagnostic_id: str, user=Depends(get_current_user)):
    session = await _sessions().find_one({
        "user_id": user["id"], "diagnostic_id": diagnostic_id,
    })
    if not session:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")
    if session.get("status") == "completed":
        return {"success": True, "result": session.get("result")}
    questions = {q["id"]: q for q in get_all_questions() if q.get("id")}
    answers = session.get("answers", [])
    if len(answers) != len(session.get("question_ids", [])):
        raise HTTPException(status_code=409, detail="Answer every diagnostic question before completing.")

    grouped: Dict[str, Dict[str, int]] = {}
    for answer in answers:
        domain = answer.get("domain_id") or canonical_domain(questions.get(answer["question_id"], {}))
        if domain not in DOMAIN_LABELS:
            continue
        grouped.setdefault(domain, {"correct": 0, "total": 0})
        grouped[domain]["total"] += 1
        grouped[domain]["correct"] += int(bool(answer.get("is_correct")))

    breakdown = []
    for domain, counts in grouped.items():
        score = round(counts["correct"] / counts["total"] * 100)
        domain_answers = [answer for answer in answers if (answer.get("domain_id") or canonical_domain(questions.get(answer["question_id"], {}))) == domain]
        timed = [int(answer.get("time_taken_seconds") or 0) for answer in domain_answers if int(answer.get("time_taken_seconds") or 0) > 0]
        confidence_values = [int(answer["confidence"]) for answer in domain_answers if answer.get("confidence") is not None]
        confidence_score = round(sum((value - 1) / 4 * 100 for value in confidence_values) / len(confidence_values)) if confidence_values else None
        breakdown.append({
            "domain": domain,
            "label": DOMAIN_LABELS.get(domain, domain.replace("_", " ").title()),
            "correct": counts["correct"],
            "total": counts["total"],
            "score": score,
            "level": skill_level(score, counts["total"]),
            "average_time_seconds": round(sum(timed) / len(timed)) if timed else None,
            "confidence_score": confidence_score,
            "calibration_gap": confidence_score - score if confidence_score is not None else None,
        })
        await record_learning_activity(user["id"], {
            "domain_id": domain,
            "type": "diagnostic",
            "success": score >= 60,
            "score_impact": 0,
            "score_percent": score,
            "correct_count": counts["correct"],
            "question_count": counts["total"],
            "assessment_id": diagnostic_id,
        })

    overall = round(sum(a["is_correct"] for a in answers) / len(answers) * 100) if answers else 0
    timed_answers = [int(answer.get("time_taken_seconds") or 0) for answer in answers if int(answer.get("time_taken_seconds") or 0) > 0]
    confidence_values = [int(answer["confidence"]) for answer in answers if answer.get("confidence") is not None]
    confidence_score = round(sum((value - 1) / 4 * 100 for value in confidence_values) / len(confidence_values)) if confidence_values else None
    weakest = min(breakdown, key=lambda item: (item["score"], -(item.get("calibration_gap") or 0))) if breakdown else None
    result = {
        "diagnostic_id": diagnostic_id,
        "overall_score": overall,
        "total_questions": len(answers),
        "correct_answers": sum(int(a["is_correct"]) for a in answers),
        "skills": sorted(breakdown, key=lambda item: item["score"]),
        "evidence": {
            "average_time_seconds": round(sum(timed_answers) / len(timed_answers)) if timed_answers else None,
            "confidence_score": confidence_score,
            "calibration_gap": confidence_score - overall if confidence_score is not None else None,
            "weakest_skill": weakest["domain"] if weakest else None,
            "recommended_action": f"Start with {weakest['label']} and repeat varied practice." if weakest else "Complete another diagnostic after your first study cycle.",
        },
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "This is a baseline estimate from a short diagnostic, not a hiring prediction.",
    }
    await _sessions().update_one(
        {"user_id": user["id"], "diagnostic_id": diagnostic_id, "status": "in_progress"},
        {"$set": {"status": "completed", "result": result, "completed_at": datetime.now(timezone.utc)}},
    )
    return {"success": True, "result": result}


@router.get("/latest")
async def latest_diagnostic(user=Depends(get_current_user)):
    session = await _sessions().find_one(
        {"user_id": user["id"], "status": "completed"},
        sort=[("completed_at", -1)],
    )
    if not session:
        return {"success": True, "result": None}
    return {"success": True, "result": session.get("result")}
