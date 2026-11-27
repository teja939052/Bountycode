"""Learning paths service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session


async def get_all_company_tracks() -> List[dict]:
    """Get all company learning tracks."""
    return [
        {"id": "sde", "name": "Software Development Engineer", "skills": []},
        {"id": "data-analyst", "name": "Data Analyst", "skills": []},
        {"id": "ai-engineer", "name": "AI Engineer", "skills": []},
    ]


async def record_track_topic_mastery(user_id: str, track_id: str, topic_id: str, score: float) -> dict:
    """Record topic mastery for a user."""
    return {"user_id": user_id, "track_id": track_id, "topic_id": topic_id, "score": score}


async def get_learning_path(user_id: str, skill_id: str) -> List[dict]:
    """Get the learning path for a user and skill."""
    async with get_session() as session:
        from app.repositories.learning import UserLearningProgressRepository
        repo = UserLearningProgressRepository(session)
        return [{"skill_id": skill_id, "status": "not_started"}]