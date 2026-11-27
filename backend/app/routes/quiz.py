"""Quiz routes — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/quiz", tags=["quiz"])


def _quiz_time_expired(quiz: dict, now: datetime = None) -> bool:
    """Check if a quiz has expired based on time limit and creation time."""
    if now is None:
        now = datetime.now(timezone.utc)
    time_limit = quiz.get("time_limit_seconds", 0)
    if not time_limit:
        return False
    created_at = quiz.get("created_at")
    if not created_at:
        return False
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    elapsed = (now - created_at).total_seconds()
    return elapsed > time_limit


@router.get("/quizzes")
async def list_quizzes(user=Depends(get_current_user)):
    """List available quizzes."""
    return {"quizzes": []}


@router.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str, user=Depends(get_current_user)):
    """Get quiz details."""
    return {"quiz_id": quiz_id, "title": quiz_id, "questions": []}