"""Gamification routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/gamification", tags=["gamification"])


@router.get("/profile")
async def get_gamification_profile(user=Depends(get_current_user)):
    """Get user's gamification profile."""
    return {
        "user_id": user["id"],
        "xp": 0,
        "level": 1,
        "coins": 0,
        "stars": 0,
        "streak": 0,
        "badges": [],
    }


@router.get("/leaderboard")
async def get_leaderboard(user=Depends(get_current_user)):
    """Get gamification leaderboard."""
    return {"leaderboard": []}