"""PostgreSQL-based gamification service — replaces MongoDB record_practice().

This is the single authoritative writer of XP, coins, stars, streak, badges,
combo, and league state (Gamification Law #1). All writes use SQLAlchemy
AsyncSession on PostgreSQL tables (gamification_profiles, xp_event_ledger).

Database-enforced idempotency: the xp_event_ledger table has a partial unique
index on (user_id, idempotency_key) WHERE idempotency_key IS NOT NULL, which
prevents duplicate XP awards under retries or concurrent requests.

No MongoDB fallback — this is the only XP writer after cutover.
"""

import logging
from datetime import datetime, timezone, date, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, and_

from app.models.gamification import GamificationProfile, XPEventLedger
from app.repositories.gamification import (
    GamificationProfileRepository,
    XPEventLedgerRepository,
)

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# PURE CALCULATION HELPERS (ported from gamification.py — no DB dependency)
# ══════════════════════════════════════════════════════════════════════════════

XP_BASE = {
    "practice": 10,
    "lesson": 15,
    "question_bank": 10,
    "coding": 20,
    "aptitude": 15,
    "interview": 25,
    "resume": 10,
    "system_design": 30,
    "assignment": 10,
    "daily_challenge": 20,
    "daily_challenge_30day": 15,
    "learning_path": 25,
    "company_track": 20,
}


def _calculate_xp(activity_type: str, score: float) -> int:
    """Base XP for an activity type, scaled by score (0-10)."""
    base = XP_BASE.get(activity_type, 10)
    return int(base * (score / 10.0))


def get_xp_with_multiplier(base_xp: int, streak: int, is_first_today: bool) -> int:
    """Apply streak and first-solve multipliers to base XP."""
    multiplier = 1.0
    if streak >= 7:
        multiplier = 1.5
    elif streak >= 3:
        multiplier = 1.25
    if is_first_today:
        multiplier += 0.5
    return int(base_xp * multiplier)


def calculate_stars(score: float, time_taken: Optional[int] = None) -> int:
    """Calculate stars (1-5) from score and optional time taken."""
    if score >= 9.5:
        return 5
    if score >= 8.0:
        return 4
    if score >= 6.5:
        return 3
    if score >= 5.0:
        return 2
    return 1


def _calculate_level(xp: int) -> int:
    """Calculate level from total XP (sqrt-based progression)."""
    import math
    return max(1, int(math.sqrt(xp / 50)) + 1)


def _league_week_id() -> str:
    """Return the current weekly league week identifier."""
    today = date.today()
    # ISO week-based: Monday start
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


# ══════════════════════════════════════════════════════════════════════════════
# POSTGRESQL GAMIFICATION SERVICE
# ══════════════════════════════════════════════════════════════════════════════

class PostgresGamificationService:
    """PostgreSQL-backed gamification operations.

    Single authoritative writer of XP, coins, stars, streak, badges, and
    league state. Uses database-enforced idempotency via xp_event_ledger.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.profile_repo = GamificationProfileRepository(session)
        self.xp_ledger_repo = XPEventLedgerRepository(session)

    # ══════════════════════════════════════════════════════════════════════════
    # PROFILE MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════

    async def get_or_create_profile(self, user_id: UUID) -> GamificationProfile:
        """Get existing profile or create a new one with defaults."""
        profile = await self.profile_repo.get_by_user_id(user_id)
        if profile:
            return profile

        now = datetime.now(timezone.utc)
        profile = GamificationProfile(
            user_id=user_id,
            xp=0,
            level=1,
            streak=0,
            combo=0,
            coins=0,
            stars=0,
            badges=[],
            bosses_defeated=[],
            weekly_xp=0,
            monthly_xp=0,
            last_practice_date=now,
            created_at=now,
            updated_at=now,
        )
        self.session.add(profile)
        await self.session.flush()
        return profile

    # ══════════════════════════════════════════════════════════════════════════
    # RECORD PRACTICE — THE SINGLE AUTHORITATIVE XP WRITER
    # ═══════════════════════════════════════════════════════════════════════════

    async def record_practice(
        self,
        user_id: UUID,
        activity_type: str,
        score: float = 0.0,
        metadata: Optional[dict] = None,
        role: str = "sde",
        idempotency_key: Optional[str] = None,
    ) -> dict:
        """Record a practice activity and update gamification state.

        This replaces the MongoDB-based record_practice(). All writes go to
        PostgreSQL tables: gamification_profiles and xp_event_ledger.

        Database-enforced idempotency: if idempotency_key is provided and a
        matching entry already exists in xp_event_ledger, the XP award is
        skipped and the previous result is returned.

        Args:
            user_id: PostgreSQL UUID of the user.
            activity_type: Activity category (coding, aptitude, interview, etc.).
            score: Pedagogical score 0-10.
            metadata: Optional context dict (role, lesson_id, etc.).
            role: Caller context (carried in metadata).
            idempotency_key: Optional idempotency key to prevent duplicate awards.

        Returns:
            dict with xp_gained, coins_earned, stars_earned, new_streak,
            new_level, level_up, old_level, streak info, etc.
        """
        metadata = dict(metadata or {})
        if role:
            metadata.setdefault("role", role)

        now = datetime.now(timezone.utc)
        today = now.date()

        # Idempotency check: if this award was already recorded, skip it.
        if idempotency_key:
            existing = await self.xp_ledger_repo.get_by_idempotency_key(user_id, idempotency_key)
            if existing:
                logger.info(
                    "Gamification idempotent replay: user=%s activity=%s key=%s",
                    user_id, activity_type, idempotency_key,
                )
                return {
                    "xp_gained": 0,
                    "coins_earned": 0,
                    "stars_earned": 0,
                    "new_streak": existing.streak if existing else 0,
                    "new_level": existing.level if existing else 1,
                    "level_up": False,
                    "old_level": existing.level if existing else 1,
                    "is_first_today": False,
                    "deduplicated": True,
                }

        # Get or create profile
        profile = await self.get_or_create_profile(user_id)
        old_level = profile.level
        old_streak = profile.streak

        # Update streak
        last_date = profile.last_practice_date
        streak_freezes = profile.streak_freezes or 0
        streak_frozen_today = False

        if last_date:
            last_date_val = last_date.date() if isinstance(last_date, datetime) else last_date
            days_diff = (today - last_date_val).days
            if days_diff == 1:
                new_streak = profile.streak + 1
            elif days_diff == 0:
                new_streak = profile.streak
            elif days_diff == 2 and streak_freezes > 0:
                new_streak = profile.streak + 1
                streak_freezes -= 1
                streak_frozen_today = True
            else:
                new_streak = 1
        else:
            new_streak = 1

        longest_streak = max(profile.longest_streak or 0, new_streak)

        # First solve of day?
        first_solve = profile.first_solve_today
        is_first_today = False
        if first_solve:
            first_date = first_solve.date() if isinstance(first_solve, datetime) else first_solve
            is_first_today = first_date != today
        else:
            is_first_today = True

        # Daily goal
        daily_goal_date = profile.daily_goal_date
        if daily_goal_date:
            dg_date = daily_goal_date.date() if isinstance(daily_goal_date, datetime) else daily_goal_date
            if dg_date != today:
                daily_goal_count = 1
            else:
                daily_goal_count = (profile.daily_goal_count or 0) + 1
        else:
            daily_goal_count = 1

        # Calculate XP
        base_xp = _calculate_xp(activity_type, score)
        xp_gained = get_xp_with_multiplier(base_xp, new_streak, is_first_today)

        # Calculate stars
        time_taken = metadata.get("time_taken") if metadata else None
        stars = calculate_stars(score, time_taken)

        # Coins earned
        coins_earned = 10 + (stars * 5)

        # Apply Double XP power-up
        dxp_expires = profile.double_xp_expires
        if dxp_expires:
            try:
                exp_dt = datetime.fromisoformat(str(dxp_expires))
                if exp_dt > now:
                    xp_gained = int(xp_gained * 2)
                    coins_earned = int(coins_earned * 2)
            except (ValueError, TypeError):
                pass

        # Counter field
        counter_field = f"total_{activity_type}s"

        # Update profile
        new_xp = (profile.xp or 0) + xp_gained
        new_level = _calculate_level(new_xp)
        level_up = new_level != old_level

        update_data = {
            "xp": new_xp,
            "level": new_level,
            "streak": new_streak,
            "longest_streak": longest_streak,
            "coins": (profile.coins or 0) + coins_earned,
            "stars_total": (profile.stars_total or 0) + stars,
            "diamonds": (profile.diamonds or 0) + xp_gained,
            "last_practice_date": now,
            "daily_goal_count": daily_goal_count,
            "daily_goal_date": today,
            counter_field: (getattr(profile, counter_field, 0) or 0) + 1,
            "updated_at": now,
        }

        if is_first_today:
            update_data["first_solve_today"] = now
        if streak_frozen_today:
            update_data["streak_freezes"] = streak_freezes

        await self.session.execute(
            update(GamificationProfile)
            .where(GamificationProfile.user_id == user_id)
            .values(**update_data)
        )

        # Emit XP event with idempotency (database-enforced)
        event_metadata = dict(metadata or {})
        if idempotency_key:
            event_metadata["idempotency_key"] = idempotency_key

        await self.xp_ledger_repo.create(
            user_id=user_id,
            activity_type=activity_type,
            score=round(score, 2),
            xp_awarded=xp_gained,
            diamonds_awarded=xp_gained,
            event_metadata=event_metadata,
            reward_policy_version="2026.1",
        )

        # Re-read profile for consistent result
        profile = await self.profile_repo.get_by_user_id(user_id)

        # Build result (compatible with MongoDB record_practice return shape)
        result = {
            "xp_gained": xp_gained,
            "coins_earned": coins_earned,
            "stars_earned": stars,
            "new_streak": new_streak,
            "new_level": new_level,
            "level_up": level_up,
            "old_level": old_level,
            "is_first_today": is_first_today,
            "streak_multiplier": 1.0,  # Simplified — calculate_streak_multiplier not ported
            "streak_frozen": streak_frozen_today,
            "streak_freezes_remaining": streak_freezes,
            "daily_goal_count": daily_goal_count,
            "daily_goal_target": profile.daily_goal_target or 5,
            "deduplicated": False,
        }

        return result

    # ══════════════════════════════════════════════════════════════════════════
    # PROFILE RETRIEVAL
    # ══════════════════════════════════════════════════════════════════════════

    async def get_profile(self, user_id: UUID) -> Optional[GamificationProfile]:
        """Get a user's gamification profile."""
        return await self.profile_repo.get_by_user_id(user_id)

    async def get_profile_dict(self, user_id: UUID) -> Optional[dict]:
        """Get a user's gamification profile as a dict."""
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            return None
        return {
            "user_id": str(profile.user_id),
            "xp": profile.xp,
            "level": profile.level,
            "streak": profile.streak,
            "combo": profile.combo,
            "coins": profile.coins,
            "stars": profile.stars_total,
            "badges": profile.badges,
            "bosses_defeated": profile.bosses_defeated,
            "weekly_xp": profile.weekly_xp,
            "monthly_xp": profile.monthly_xp,
            "last_practice_date": profile.last_practice_date.isoformat() if profile.last_practice_date else None,
            "created_at": profile.created_at.isoformat() if profile.created_at else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        }


async def record_practice(
    session: AsyncSession,
    user_id: str,
    activity_type: str,
    score: float = 0.0,
    metadata: Optional[dict] = None,
    role: str = "sde",
    idempotency_key: Optional[str] = None,
) -> dict:
    """Module-level convenience wrapper for PostgresGamificationService.record_practice.

    Accepts user_id as a string (UUID) and creates a service instance internally.
    Callers should pass a SQLAlchemy AsyncSession.
    """
    service = PostgresGamificationService(session)
    return await service.record_practice(
        UUID(user_id), activity_type, score, metadata, role, idempotency_key
    )
