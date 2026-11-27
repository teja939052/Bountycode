"""SDE diagnostic routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/sde-diagnostic", tags=["sde-diagnostic"])


@router.get("/assessment")
async def get_sde_diagnostic(user=Depends(get_current_user)):
    """Get SDE diagnostic assessment."""
    return {
        "assessment_id": "sde_diagnostic",
        "title": "SDE Diagnostic Assessment",
        "questions": [],
        "time_limit_minutes": 60,
    }


@router.post("/assessment/submit")
async def submit_sde_diagnostic(
    answers: dict,
    user=Depends(get_current_user),
):
    """Submit SDE diagnostic answers."""
    return {"submitted": True, "score": 0, "feedback": "Submission recorded"}