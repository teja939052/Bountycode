"""Journey engine — orchestrates the learner's path."""
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from app.database import get_session


async def build_journey_state(user_id: str, role: str = "sde") -> Dict[str, Any]:
    """Build a learner's journey state from PostgreSQL data."""
    async with get_session() as session:
        from app.models.identity import User
        from sqlalchemy import select
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return {"user_id": user_id, "role": role, "skills": {}}
        return {
            "user_id": str(user.id),
            "role": role,
            "skills": {},
            "plan": user.plan,
        }


async def get_learning_path(user_id: str, skill_id: str) -> List[dict]:
    """Get the learning path for a user and skill."""
    async with get_session() as session:
        from app.repositories.learning import UserLearningProgressRepository
        repo = UserLearningProgressRepository(session)
        # Return simplified path
        return [{"skill_id": skill_id, "status": "not_started"}]