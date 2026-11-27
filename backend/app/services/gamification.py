"""Gamification service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def record_practice(
    user_id: str,
    activity_type: str,
    score: float,
    metadata: dict = None,
    role: str = "student",
) -> dict:
    """Record practice activity and award XP."""
    async with get_session() as session:
        from app.models.gamification import GamificationProfile
        from sqlalchemy import select
        result = await session.execute(
            select(GamificationProfile).where(GamificationProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = GamificationProfile(
                user_id=user_id,
                xp=0,
                level=1,
                coins=0,
                stars=0,
                streak=0,
            )
            session.add(profile)
        # Calculate XP gain
        xp_gained = int(score * 10)
        profile.xp += xp_gained
        profile.coins += xp_gained // 10
        # Update level based on XP
        new_level = 1 + (profile.xp // 1000)
        if profile.level != new_level:
            profile.level = new_level
        await session.commit()
    return {
        "xp_gained": xp_gained,
        "coins_earned": xp_gained // 10,
        "new_badges": [],
        "new_streak": profile.streak,
        "level_up": profile.level > 1,
    }


async def get_gamification_profile(user_id: str) -> dict:
    """Get user's gamification profile."""
    async with get_session() as session:
        from app.models.gamification import GamificationProfile
        from sqlalchemy import select
        result = await session.execute(
            select(GamificationProfile).where(GamificationProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
    if not profile:
        return {
            "user_id": user_id,
            "xp": 0,
            "level": 1,
            "coins": 0,
            "stars": 0,
            "streak": 0,
            "badges": [],
        }
    return {
        "user_id": user_id,
        "xp": profile.xp,
        "level": profile.level,
        "coins": profile.coins,
        "stars": profile.stars,
        "streak": profile.streak,
        "badges": profile.badges or [],
    }