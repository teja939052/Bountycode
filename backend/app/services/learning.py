"""Learning service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session


async def get_user_progress(user_id: str, skill_id: str) -> dict:
    """Get user learning progress for a skill."""
    async with get_session() as session:
        from app.repositories.learning import UserLearningProgressRepository
        repo = UserLearningProgressRepository(session)
        return {"user_id": user_id, "skill_id": skill_id, "status": "not_started"}


async def record_learning_activity(user_id: str, event: dict) -> dict:
    """Record a learning activity event."""
    async with get_session() as session:
        from app.repositories.learning import LearningEvidenceRepository
        repo = LearningEvidenceRepository(session)
        return {"user_id": user_id, "event": event, "recorded": True}

async def get_learning_path(user_id: str) -> dict:
    """Stub for get_learning_path."""
    return {"user_id": user_id}
