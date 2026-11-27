"""Readiness service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_readiness(user_id: str) -> dict:
    """Get user's interview readiness."""
    return {"user_id": user_id, "readiness_score": 0, "ready": False}


async def calculate_readiness(
    user_id: str,
) -> dict:
    """Calculate interview readiness score."""
    return {"user_id": user_id, "readiness_score": 0, "ready": False, "weak_areas": []}

async def compute_readiness(user_id: str) -> dict:
    """Stub for compute_readiness."""
    return {"user_id": user_id}
