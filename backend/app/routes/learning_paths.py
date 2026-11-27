"""Learning paths routes — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_session
from app.middleware.auth import get_current_user


router = APIRouter(prefix="/api/v1/learning-paths", tags=["learning-paths"])


@router.get("/tracks")
async def get_company_tracks():
    """Get all company learning tracks."""
    from app.services.learning_paths import get_all_company_tracks
    return await get_all_company_tracks()


@router.get("/path")
async def get_learning_path(user_id: str, skill_id: str):
    """Get user's learning path for a skill."""
    from app.services.learning_paths import get_learning_path
    return await get_learning_path(user_id, skill_id)