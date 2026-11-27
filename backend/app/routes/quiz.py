"""Quiz routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/quiz", tags=["quiz"])


@router.get("/quizzes")
async def list_quizzes(user=Depends(get_current_user)):
    """List available quizzes."""
    return {"quizzes": []}


@router.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str, user=Depends(get_current_user)):
    """Get quiz details."""
    return {"quiz_id": quiz_id, "title": quiz_id, "questions": []}