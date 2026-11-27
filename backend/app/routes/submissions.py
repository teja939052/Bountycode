"""Submissions routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/submissions", tags=["submissions"])


@router.get("/submissions")
async def list_submissions(user=Depends(get_current_user)):
    """List user's submissions."""
    return {"submissions": []}


@router.post("/submissions")
async def create_submission(
    problem_id: str,
    code: str,
    language: str = "python",
    user=Depends(get_current_user),
):
    """Create a submission."""
    return {
        "submission_id": str(user["id"]) + "-sub-1",
        "problem_id": problem_id,
        "status": "submitted",
        "score": None,
    }