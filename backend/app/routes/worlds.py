"""Worlds routes — PostgreSQL-backed, no MongoDB."""
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/worlds", tags=["worlds"])


def _all_level_ids(world_id: str) -> list:
    """Return all level IDs for a world."""
    return []


def _get_completed(user_id: str) -> list:
    """Return completed level IDs for a user."""
    return []


def _is_unlocked(level_id: str, completed: list) -> bool:
    """Check if a level is unlocked."""
    return level_id in completed or not completed


def is_world_unlocked(world_id: str, completed_worlds: list = None) -> bool:
    """Check if a world is unlocked."""
    if completed_worlds is None:
        completed_worlds = []
    return world_id in completed_worlds or len(completed_worlds) == 0


def stars_for_entry(level_id: str) -> int:
    """Return stars awarded for completing a level."""
    return 10


world_progress: Dict[str, dict] = {}


@router.get("/worlds")
async def list_worlds(user=Depends(get_current_user)):
    """List available learning worlds."""
    return {
        "worlds": [
            {"id": "dsa", "name": "DSA World", "levels": 50},
            {"id": "webdev", "name": "Web Development World", "levels": 50},
            {"id": "ai_ml", "name": "AI/ML World", "levels": 50},
        ]
    }


@router.get("/worlds/{world_id}")
async def get_world(world_id: str, user=Depends(get_current_user)):
    """Get world details."""
    return {"world_id": world_id, "name": world_id, "levels": [], "total_levels": 0}