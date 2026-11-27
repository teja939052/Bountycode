"""Readiness Engine — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def calculate_readiness(user_id: str) -> dict:
    """Calculate readiness score for a user."""
    return {"user_id": user_id, "readiness_score": 0, "ready": False}


async def compute_readiness(user_id: str) -> dict:
    """Compute readiness for user - alias for calculate_readiness."""
    return await calculate_readiness(user_id)

async def get_readiness_details(user_id: str) -> dict:
    """Get detailed readiness information for user."""
    return {"user_id": user_id, "detailed_readiness": {}}

async def calculate_target_readiness(user_id: str) -> dict:
    """Stub for calculate_target_readiness."""
    return {"user_id": user_id}


async def collect_target_evidence(user_id: str) -> dict:
    """Stub for collect_target_evidence."""
    return {"user_id": user_id}
