"""Gamification domain repositories — PostgreSQL replacements for Motor collection operations.

Per Gamification Law: record_practice() is the only writer of XP/coins/stars/streak/badges.
XP ledger is append-only: profile.xp == sum(xp_event_ledger.xp_awarded) must reconcile.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import select, update, delete, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RepositoryBase
from app.models.gamification import (
    GamificationProfile,
    XPEventLedger,
    Badge,
    UserBadge,
    StreakRecord,
)
from app.models.identity import User


class GamificationProfileRepository(RepositoryBase):
    """Repository for gamification profiles — replaces gamification_collection."""

    async def get_by_user_id(self, user_id: UUID) -> Optional[GamificationProfile]:
        result = await self.session.execute(
            select(GamificationProfile).where(GamificationProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, profile_data: dict) -> GamificationProfile:
        profile = GamificationProfile(user_id=user_id, **profile_data)
        self.session.add(profile)
        await self.flush()
        return profile

    async def get_or_create(self, user_id: UUID) -> GamificationProfile:
        profile = await self.get_by_user_id(user_id)
        if profile:
            return profile
        return await self.create(user_id, {})

    async def update(self, user_id: UUID, updates: dict) -> Optional[GamificationProfile]:
        result = await self.session.execute(
            update(GamificationProfile)
            .where(GamificationProfile.user_id == user_id)
            .values(**updates, updated_at=datetime.now(timezone.utc))
            .returning(GamificationProfile)
        )
        return result.scalar_one_or_none()

    async def get_leaderboard(
        self,
        field: str = "xp",
        limit: int = 50,
        offset: int = 0,
    ) -> List[GamificationProfile]:
        order_col = getattr(GamificationProfile, field, GamificationProfile.xp)
        result = await self.session.execute(
            select(GamificationProfile)
            .order_by(desc(order_col))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def count_above(self, field: str, value: Any) -> int:
        order_col = getattr(GamificationProfile, field, GamificationProfile.xp)
        result = await self.session.execute(
            select(func.count(GamificationProfile.user_id)).where(order_col > value)
        )
        return result.scalar_one()

    async def get_users_above(
        self,
        field: str,
        value: Any,
        limit: int = 10,
    ) -> List[GamificationProfile]:
        order_col = getattr(GamificationProfile, field, GamificationProfile.xp)
        result = await self.session.execute(
            select(GamificationProfile)
            .where(order_col > value)
            .order_by(asc(order_col))
            .limit(limit)
        )
        return list(result.scalars().all())


class XPEventLedgerRepository(RepositoryBase):
    """Repository for XP event ledger — append-only, immutable."""

    async def create(
        self,
        user_id: UUID,
        activity_type: str,
        score: float,
        xp_awarded: int,
        diamonds_awarded: int = 0,
        metadata: dict = None,
        reward_policy_version: str = "v1",
    ) -> XPEventLedger:
        event = XPEventLedger(
            user_id=user_id,
            activity_type=activity_type,
            score=int(score),  # 0-10 scale
            xp_awarded=xp_awarded,
            diamonds_awarded=diamonds_awarded,
            metadata=metadata or {},
            reward_policy_version=reward_policy_version,
        )
        self.session.add(event)
        await self.flush()
        return event

    async def get_total_xp(self, user_id: UUID) -> int:
        """Get total XP — must reconcile with profile.xp."""
        result = await self.session.execute(
            select(func.coalesce(func.sum(XPEventLedger.xp_awarded), 0)).where(
                XPEventLedger.user_id == user_id
            )
        )
        return result.scalar_one()

    async def get_events(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[XPEventLedger]:
        result = await self.session.execute(
            select(XPEventLedger)
            .where(XPEventLedger.user_id == user_id)
            .order_by(desc(XPEventLedger.created_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_idempotency_key(
        self,
        user_id: UUID,
        idempotency_key: str,
    ) -> Optional[XPEventLedger]:
        """Look up an XP event by user and idempotency key (stored in metadata)."""
        result = await self.session.execute(
            select(XPEventLedger)
            .where(XPEventLedger.user_id == user_id)
        )
        for event in result.scalars().all():
            event_meta = event.event_metadata or {}
            if event_meta.get("idempotency_key") == idempotency_key:
                return event
        return None


class BadgeRepository(RepositoryBase):
    """Repository for badges."""

    async def get_by_badge_id(self, badge_id: str) -> Optional[Badge]:
        result = await self.session.execute(select(Badge).where(Badge.badge_id == badge_id))
        return result.scalar_one_or_none()

    async def get_active(self) -> List[Badge]:
        result = await self.session.execute(select(Badge).where(Badge.is_active == True))  # noqa: E712
        return list(result.scalars().all())


class UserBadgeRepository(RepositoryBase):
    """Repository for user-badge associations."""

    async def get_user_badges(self, user_id: UUID) -> List[UserBadge]:
        result = await self.session.execute(
            select(UserBadge).where(UserBadge.user_id == user_id)
        )
        return list(result.scalars().all())

    async def award(self, user_id: UUID, badge_id: str) -> Optional[UserBadge]:
        # Check if already awarded
        existing = await self.session.execute(
            select(UserBadge).where(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge_id,
            )
        )
        if existing.scalar_one_or_none():
            return None
        badge = UserBadge(user_id=user_id, badge_id=badge_id)
        self.session.add(badge)
        await self.flush()
        return badge

    async def has_badge(self, user_id: UUID, badge_id: str) -> bool:
        result = await self.session.execute(
            select(UserBadge).where(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge_id,
            )
        )
        return result.scalar_one_or_none() is not None


class StreakRecordRepository(RepositoryBase):
    """Repository for streak records."""

    async def get_by_user_id(self, user_id: UUID) -> Optional[StreakRecord]:
        result = await self.session.execute(
            select(StreakRecord).where(StreakRecord.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        user_id: UUID,
        current_streak: int,
        longest_streak: int,
        last_practice_date: Optional[str],
    ) -> StreakRecord:
        existing = await self.get_by_user_id(user_id)
        if existing:
            existing.current_streak = current_streak
            existing.longest_streak = longest_streak
            existing.last_practice_date = last_practice_date
            await self.flush()
            return existing
        record = StreakRecord(
            user_id=user_id,
            current_streak=current_streak,
            longest_streak=longest_streak,
            last_practice_date=last_practice_date,
        )
        self.session.add(record)
        await self.flush()
        return record
