"""Repair routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/repair", tags=["repair"])


@router.get("/missions")
async def list_repair_missions(user=Depends(get_current_user)):
    """List repair missions for user."""
    return {"missions": []}


@router.post("/missions/{mission_id}/complete")
async def complete_repair_mission(
    mission_id: str,
    user=Depends(get_current_user),
):
    """Complete a repair mission."""
    return {"mission_id": mission_id, "status": "completed"}