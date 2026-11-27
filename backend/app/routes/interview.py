"""Interview routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.database import get_session
from app.models.interview import InterviewSession

router = APIRouter(prefix="/api/v1/interview", tags=["interview"])


@router.post("/start")
async def start_interview(user=Depends(get_current_user)):
    """Start a new interview session."""
    async with get_session() as session:
        interview = InterviewSession(
            user_id=user["id"],
            role="software_engineer",
            difficulty="medium",
            status="in_progress",
        )
        session.add(interview)
        await session.commit()
        await session.refresh(interview)
    return {
        "interview_id": str(interview.id),
        "status": interview.status,
    }


@router.get("/{interview_id}/result")
async def get_interview_result(interview_id: str, user=Depends(get_current_user)):
    """Get interview results."""
    async with get_session() as session:
        result = await session.execute(
            select(InterviewSession).where(
                InterviewSession.id == interview_id,
                InterviewSession.user_id == user["id"],
            )
        )
        interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return {
        "interview_id": str(interview.id),
        "status": interview.status,
        "score": interview.score,
        "feedback": interview.feedback,
    }


@router.post("/{interview_id}/answer")
async def submit_answer(
    interview_id: str,
    question: str,
    answer: str,
    time_taken: int,
    is_follow_up: bool = False,
    user=Depends(get_current_user),
):
    """Submit an answer to an interview question."""
    async with get_session() as session:
        result = await session.execute(
            select(InterviewSession).where(
                InterviewSession.id == interview_id,
                InterviewSession.user_id == user["id"],
            )
        )
        interview = result.scalar_one_or_none()
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")

        return {
            "interview_id": interview_id,
            "question": question,
            "answer": answer,
            "status": "recorded",
        }