"""Gamification service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.database import get_session


def _calculate_level(xp: int) -> int:
    """Calculate level from XP."""
    return 1 + (xp // 1000)


def _calculate_xp(score: float, base: int = 10) -> int:
    """Calculate XP from a 0-100 score."""
    return int(score * base)


def calculate_streak_multiplier(streak: int) -> float:
    """Calculate streak multiplier."""
    return 1.0 + (streak * 0.1)


BOSS_BATTLES: List[dict] = [
    {"level": 10, "name": "First Boss", "xp_required": 10000},
    {"level": 20, "name": "Second Boss", "xp_required": 20000},
    {"level": 30, "name": "Third Boss", "xp_required": 30000},
    {"level": 40, "name": "Fourth Boss", "xp_required": 40000},
    {"level": 50, "name": "Final Boss", "xp_required": 50000},
]

TOWER_TITLES: List[str] = [
    "Hatchling", "Coder", "Builder", "Engineer", "Architect",
    "Master", "Grandmaster", "Legend", "Mythic", "God of Code",
]

POWER_UPS: List[dict] = [
    {"id": "extra_time", "name": "Extra Time", "cost": 50},
    {"id": "hint_reveal", "name": "Hint Reveal", "cost": 30},
    {"id": "retry", "name": "Retry", "cost": 20},
    {"id": "double_xp", "name": "Double XP", "cost": 100},
    {"id": "skip_boss", "name": "Skip Boss", "cost": 200},
    {"id": "show_answer", "name": "Show Answer", "cost": 75},
]

STREAK_MULTIPLIERS: Dict[int, float] = {
    1: 1.0,
    2: 1.1,
    3: 1.2,
    4: 1.3,
    5: 1.5,
    7: 1.7,
    10: 2.0,
}

FOREST_ZONES: List[dict] = [
    {"id": "zone_1", "name": "Starting Forest", "level": 1},
    {"id": "zone_2", "name": "Deep Woods", "level": 10},
    {"id": "zone_3", "name": "Ancient Grove", "level": 20},
    {"id": "zone_4", "name": "Mystic Canopy", "level": 30},
    {"id": "zone_5", "name": "Elder Woods", "level": 40},
]


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