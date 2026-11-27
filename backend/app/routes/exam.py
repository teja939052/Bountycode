from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Optional

from app.database import get_session
from sqlalchemy import select

from app.middleware.auth import get_current_user
from app.services.exam_engine import (
    start_exam, submit_answer, complete_exam, get_report, list_attempts,
)
from app.services.diagnostic import diagnose_exam

router = APIRouter(prefix="/api/v1/exam", tags=["exam"])


class StartReq(BaseModel):
    topic: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    count: int = 10
    duration_minutes: int = 20
    difficulty_mix: Optional[dict] = None
    seed: Optional[int] = None


class AnswerReq(BaseModel):
    attempt_id: str
    question_id: str
    answer: Any


@router.post("/start")
async def start(req: StartReq, user=Depends(get_current_user)):
    return await start_exam(
        user_id=user["id"], topic=req.topic, category=req.category,
        difficulty=req.difficulty, count=req.count, duration_minutes=req.duration_minutes,
        difficulty_mix=req.difficulty_mix, seed=req.seed,
    )


@router.post("/answer")
async def answer(req: AnswerReq, user=Depends(get_current_user)):
    try:
        return await submit_answer(req.attempt_id, user["id"], req.question_id, req.answer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete")
async def complete(attempt_id: str, user=Depends(get_current_user)):
    try:
        return await complete_exam(attempt_id, user["id"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/report/{attempt_id}")
async def report(attempt_id: str, user=Depends(get_current_user)):
    try:
        return await get_report(attempt_id, user["id"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
async def history(user=Depends(get_current_user)):
    return await list_attempts(user["id"])


@router.post("/repair/{topic}")
async def repair(topic: str, count: int = 5, user=Depends(get_current_user)):
    from app.services.assessment_blueprint import select_questions
    questions = select_questions(topic=topic, total=count)
    safe_qs = [{
        "id": q.get("id") or q.get("_id"),
        "question": q.get("question") or q.get("text"),
        "options": q.get("options"),
        "difficulty": q.get("difficulty"),
        "topic": q.get("topic"),
    } for q in questions]
    return {"topic": topic, "questions": safe_qs, "count": len(safe_qs)}


@router.post("/reassess/{topic}")
async def reassess(topic: str, count: int = 5, user=Depends(get_current_user)):
    from app.services.assessment_blueprint import select_questions
    questions = select_questions(topic=topic, total=count)
    safe_qs = [{
        "id": q.get("id") or q.get("_id"),
        "question": q.get("question") or q.get("text"),
        "options": q.get("options"),
        "difficulty": q.get("difficulty"),
        "topic": q.get("topic"),
    } for q in questions]
    return {"topic": topic, "questions": safe_qs, "count": len(safe_qs)}


@router.post("/diagnose/{attempt_id}")
async def diagnose(attempt_id: str, user=Depends(get_current_user)):
    async with get_session() as session:
        from sqlalchemy import select
        from app.models.assessments import InterviewSession
        result = await session.execute(
            select(InterviewSession).where(
                InterviewSession.id == attempt_id,
                InterviewSession.user_id == user["id"],
            )
        )
        attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="attempt not found")
    if not attempt.completed_at:
        raise HTTPException(status_code=400, detail="attempt not completed")
    prev = {}
    results = diagnose_exam(attempt.questions, attempt.get("answers") or {},
                            prev, attempt_id, activity_id=None)
    return {"attempt_id": attempt_id, "diagnostics": results}
