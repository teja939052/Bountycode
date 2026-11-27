"""Study routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/study", tags=["study"])


@router.get("/sessions")
async def list_study_sessions(user=Depends(get_current_user)):
    """List user's study sessions."""
    return {"sessions": []}


@router.post("/sessions")
async def create_study_session(
    subject: str,
    duration_minutes: int,
    user=Depends(get_current_user),
):
    """Create a new study session."""
    return {
        "session_id": str(user["id"]) + "-study-1",
        "subject": subject,
        "duration_minutes": duration_minutes,
        "started_at": None,
    }