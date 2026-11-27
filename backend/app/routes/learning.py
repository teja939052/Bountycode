"""Learning routes — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_session
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


@router.post("/path")
async def get_learning_path(user_id: str, skill_id: str):
    """Get user's learning path for a skill."""
    from app.services.learning import get_learning_path
    return await get_learning_path(user_id, skill_id)


@router.post("/activity")
async def record_activity(event: dict):
    """Record a learning activity event."""
    from app.services.learning import record_learning_activity
    return await record_learning_activity(user_id="current", event=event)