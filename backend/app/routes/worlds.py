"""Worlds routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/worlds", tags=["worlds"])


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