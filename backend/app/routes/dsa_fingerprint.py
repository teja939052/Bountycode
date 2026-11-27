"""DSA Fingerprint routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session
from sqlalchemy import select
from app.models.learning import LearnerSkillState

router = APIRouter(prefix="/api/v1/dsa-fingerprint", tags=["dsa-fingerprint"])


@router.get("/{user_id}")
async def get_skill_graph(user_id: str, user=Depends(get_current_user)):
    """Get user's DSA fingerprint skill data."""
    async with get_session() as session:
        result = await session.execute(
            select(LearnerSkillState).where(LearnerSkillState.user_id == user_id)
        )
        skill_states = result.scalars().all()

    return {
        "user_id": user_id,
        "skills": [
            {
                "skill_id": s.skill_id,
                "score": s.score,
                "level": s.mastery_level,
                "total_attempts": s.total_attempts,
                "last_practiced": s.last_practiced.isoformat() if s.last_practiced else None,
            }
            for s in skill_states
        ]
    }