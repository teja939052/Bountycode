"""Coupon repository — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session, RepositoryBase
from app.models.coupon import Coupon, CouponUsage


class CouponRepository(RepositoryBase):
    """Repository for coupons — replaces coupons_collection."""

    async def create(self, session: AsyncSession, coupon: Coupon) -> Coupon:
        session.add(coupon)
        await session.flush()
        return coupon

    async def get_by_code(self, session: AsyncSession, code: str) -> Optional[Coupon]:
        result = await session.execute(
            select(Coupon).where(Coupon.code == code)
        )
        return result.scalar_one_or_none()

    async def list_all(self, session: AsyncSession) -> List[Coupon]:
        result = await session.execute(select(Coupon).order_by(Coupon.created_at.desc()))
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, coupon_id: UUID) -> Optional[Coupon]:
        result = await session.execute(
            select(Coupon).where(Coupon.id == coupon_id)
        )
        return result.scalar_one_or_none()

    async def increment_uses(self, session: AsyncSession, coupon_id: UUID) -> None:
        await session.execute(
            CouponUsage.__table__.insert().values(
                coupon_id=coupon_id,
                user_id=None,  # Will be set by the caller
                used_at=datetime.now(timezone.utc),
            )
        )
        # Increment used_count on the coupon
        await session.execute(
            Coupon.__table__.update()
            .where(Coupon.id == coupon_id)
            .values(used_count=Coupon.used_count + 1)
        )

    async def record_usage(self, session: AsyncSession, coupon_id: UUID, user_id: str) -> None:
        await session.execute(
            CouponUsage.__table__.insert().values(
                coupon_id=coupon_id,
                user_id=UUID(user_id) if user_id else None,
                used_at=datetime.now(timezone.utc),
            )
        )
        # Increment used_count on the coupon
        await session.execute(
            Coupon.__table__.update()
            .where(Coupon.id == coupon_id)
            .values(used_count=Coupon.used_count + 1)
        )