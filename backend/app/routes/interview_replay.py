"""Interview replay routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session
from app.models.interview import InterviewSession
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/interview-replay", tags=["interview-replay"])


@router.get("/{interview_id}")
async def get_interview_replay(
    interview_id: str,
    user=Depends(get_current_user),
):
    """Get interview replay data."""
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
        "questions": interview.questions or [],
        "answers": interview.answers or [],
    }