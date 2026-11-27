"""Unified deterministic practice exam engine backed by PostgreSQL."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import get_session_factory
from app.repositories.exam import PracticeExamAttemptRepository
from app.services.assessment_blueprint import select_questions
from app.services.question_store import get_question_for_serving
from app.services.scoring import score_question


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _uuid(value: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError("invalid exam or user id") from exc


def _safe_question(question: dict) -> dict:
    return {
        "id": question.get("id") or question.get("_id"),
        "question": question.get("question") or question.get("text"),
        "options": question.get("options"),
        "difficulty": question.get("difficulty"),
        "topic": question.get("topic"),
        "category": question.get("category"),
    }


def _trusted_questions(ids: list[str]) -> list[dict]:
    questions = []
    for question_id in ids:
        question = get_question_for_serving(str(question_id))
        if question is not None:
            questions.append(question)
    return questions


def _report(attempt, questions: list[dict]) -> Dict[str, Any]:
    answers = attempt.answers or {}
    correct = 0
    review = []
    for question in questions:
        question_id = str(question.get("id") or question.get("_id"))
        user_answer = answers.get(question_id)
        scored = score_question(question, user_answer)
        if scored["is_correct"]:
            correct += 1
        review.append({
            "id": question_id,
            "question": question.get("question") or question.get("text"),
            "your_answer": user_answer,
            "correct_answer": scored["correct_answer"],
            "correct": scored["is_correct"],
            "explanation": question.get("explanation"),
        })
    return {
        "attempt_id": str(attempt.id),
        "score": attempt.score,
        "correct": correct,
        "total": len(questions),
        "review": review,
    }


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
        questions = select_questions(topic=topic, category=category, difficulty_mix=difficulty_mix, total=count, seed=seed)
    elif difficulty:
        questions = select_questions(topic=topic, category=category, difficulty_mix={difficulty: count}, total=count, seed=seed)
    else:
        questions = select_questions(topic=topic, category=category, total=count, seed=seed)
    question_ids = [str(q.get("id") or q.get("_id")) for q in questions]
    data = {
        "user_id": _uuid(user_id),
        "topic": topic,
        "category": category,
        "difficulty": difficulty,
        "duration_minutes": duration_minutes,
        "question_ids": question_ids,
        "answers": {},
        "started_at": _now(),
    }
    async with get_session_factory()() as session:
        attempt = await PracticeExamAttemptRepository(session).create(data)
        await session.commit()
        return {
            "attempt_id": str(attempt.id),
            "duration_minutes": duration_minutes,
            "total": len(question_ids),
            "questions": [_safe_question(q) for q in questions],
        }


async def submit_answer(attempt_id: str, user_id: str, question_id: str, answer: Any) -> Dict[str, Any]:
    async with get_session_factory()() as session:
        repo = PracticeExamAttemptRepository(session)
        attempt = await repo.get_by_id_and_user(_uuid(attempt_id), _uuid(user_id))
        if not attempt:
            raise ValueError("attempt not found")
        if attempt.status != "in_progress":
            raise ValueError("attempt already completed")
        if str(question_id) not in {str(q) for q in (attempt.question_ids or [])}:
            raise ValueError("question is not part of this attempt")
        answers = dict(attempt.answers or {})
        answers[str(question_id)] = answer
        if not await repo.set_answers(attempt.id, attempt.user_id, answers):
            raise ValueError("attempt already completed")
        await session.commit()
    return {"saved": True}


async def complete_exam(attempt_id: str, user_id: str) -> Dict[str, Any]:
    async with get_session_factory()() as session:
        repo = PracticeExamAttemptRepository(session)
        attempt = await repo.get_by_id_and_user(_uuid(attempt_id), _uuid(user_id))
        if not attempt:
            raise ValueError("attempt not found")
        questions = _trusted_questions(attempt.question_ids or [])
        if attempt.status == "completed":
            return _report(attempt, questions)
        answers = attempt.answers or {}
        correct = sum(
            1 for question in questions
            if score_question(question, answers.get(str(question.get("id") or question.get("_id"))))["is_correct"]
        )
        score_pct = round((correct / len(questions)) * 100, 2) if questions else 0.0
        completed = await repo.complete(attempt.id, attempt.user_id, score_pct, correct)
        if not completed:
            raise ValueError("attempt already completed")
        await session.commit()
        return _report(completed, questions)


async def get_report(attempt_id: str, user_id: str) -> Dict[str, Any]:
    async with get_session_factory()() as session:
        attempt = await PracticeExamAttemptRepository(session).get_by_id_and_user(_uuid(attempt_id), _uuid(user_id))
        if not attempt:
            raise ValueError("attempt not found")
        if attempt.status != "completed":
            raise ValueError("attempt not completed")
        return _report(attempt, _trusted_questions(attempt.question_ids or []))


async def list_attempts(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    async with get_session_factory()() as session:
        attempts = await PracticeExamAttemptRepository(session).list_by_user(_uuid(user_id), limit)
        return [{
            "attempt_id": str(a.id),
            "topic": a.topic,
            "category": a.category,
            "difficulty": a.difficulty,
            "score": a.score,
            "total": len(a.question_ids or []),
            "started_at": a.started_at,
            "completed_at": a.completed_at,
        } for a in attempts]
