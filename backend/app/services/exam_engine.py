"""Unified Exam Engine — reusable timed MCQ assessment infrastructure."""
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import get_collection
from app.services.assessment_blueprint import select_questions
from app.services.scoring import score_question

logger = logging.getLogger(__name__)

COLLECTION = get_collection("exam_attempts")


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def start_exam(
    user_id: str,
    topic: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    count: int = 10,
    duration_minutes: int = 20,
    difficulty_mix: Optional[Dict[str, int]] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    if difficulty_mix:
        questions = select_questions(topic=topic, category=category,
                                     difficulty_mix=difficulty_mix, total=count, seed=seed)
    elif difficulty:
        questions = select_questions(topic=topic, category=category,
                                     difficulty_mix={difficulty: count}, total=count, seed=seed)
    else:
        questions = select_questions(topic=topic, category=category, total=count, seed=seed)
    safe_qs = []
    for q in questions:
        safe_qs.append({
            "id": q.get("id") or q.get("_id"),
            "question": q.get("question") or q.get("text"),
            "options": q.get("options"),
            "difficulty": q.get("difficulty"),
            "topic": q.get("topic"),
            "category": q.get("category"),
        })
    attempt_id = str(uuid.uuid4())
    doc = {
        "attempt_id": attempt_id,
        "user_id": user_id,
        "topic": topic,
        "category": category,
        "difficulty": difficulty,
        "duration_minutes": duration_minutes,
        "question_ids": [q.get("id") for q in questions],
        "questions": questions,
        "answers": {},
        "started_at": _now(),
        "completed_at": None,
        "score": None,
        "total": len(questions),
    }
    await COLLECTION.insert_one(doc)
    return {
        "attempt_id": attempt_id,
        "duration_minutes": duration_minutes,
        "total": len(safe_qs),
        "questions": safe_qs,
    }


async def submit_answer(attempt_id: str, user_id: str, question_id: str, answer: Any) -> Dict[str, Any]:
    attempt = await COLLECTION.find_one({"attempt_id": attempt_id, "user_id": user_id})
    if not attempt:
        raise ValueError("attempt not found")
    if attempt.get("completed_at"):
        raise ValueError("attempt already completed")
    answers = attempt.get("answers") or {}
    answers[question_id] = answer
    await COLLECTION.update_one(
        {"attempt_id": attempt_id},
        {"$set": {"answers": answers}},
    )
    return {"saved": True}


async def complete_exam(attempt_id: str, user_id: str) -> Dict[str, Any]:
    attempt = await COLLECTION.find_one({"attempt_id": attempt_id, "user_id": user_id})
    if not attempt:
        raise ValueError("attempt not found")
    if attempt.get("completed_at"):
        return _report(attempt)
    questions = attempt.get("questions") or []
    answers = attempt.get("answers") or {}
    correct = 0
    review = []
    for q in questions:
        qid = q.get("id")
        ua = answers.get(qid)
        sr = score_question(q, ua, time_spent=None)
        if sr["is_correct"]:
            correct += 1
        review.append({
            "id": qid,
            "question": q.get("question") or q.get("text"),
            "your_answer": ua,
            "correct_answer": sr["correct_answer"],
            "correct": sr["is_correct"],
            "explanation": q.get("explanation"),
        })
    score_pct = round((correct / len(questions)) * 100, 2) if questions else 0.0
    await COLLECTION.update_one(
        {"attempt_id": attempt_id},
        {"$set": {"completed_at": _now(), "score": score_pct, "correct": correct}},
    )
    return {
        "attempt_id": attempt_id,
        "score": score_pct,
        "correct": correct,
        "total": len(questions),
        "review": review,
    }


def _report(attempt: Dict[str, Any]) -> Dict[str, Any]:
    questions = attempt.get("questions") or []
    answers = attempt.get("answers") or {}
    correct = 0
    review = []
    for q in questions:
        qid = q.get("id")
        ua = answers.get(qid)
        sr = score_question(q, ua)
        if sr["is_correct"]:
            correct += 1
        review.append({"id": qid, "question": q.get("question") or q.get("text"),
                      "your_answer": ua, "correct_answer": sr["correct_answer"], "correct": sr["is_correct"],
                      "explanation": q.get("explanation")})
    return {"attempt_id": attempt["attempt_id"], "score": attempt.get("score"),
            "correct": correct, "total": len(questions), "review": review}


async def get_report(attempt_id: str, user_id: str) -> Dict[str, Any]:
    attempt = await COLLECTION.find_one({"attempt_id": attempt_id, "user_id": user_id})
    if not attempt:
        raise ValueError("attempt not found")
    if not attempt.get("completed_at"):
        raise ValueError("attempt not completed")
    return _report(attempt)


async def list_attempts(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    cursor = COLLECTION.find({"user_id": user_id}).sort("started_at", -1).limit(limit)
    out = []
    async for d in cursor:
        out.append({
            "attempt_id": d.get("attempt_id"),
            "topic": d.get("topic"),
            "category": d.get("category"),
            "difficulty": d.get("difficulty"),
            "score": d.get("score"),
            "total": d.get("total"),
            "started_at": d.get("started_at"),
            "completed_at": d.get("completed_at"),
        })
    return out
