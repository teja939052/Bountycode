"""Operations repositories — PostgreSQL-backed."""
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session, RepositoryBase
from app.models.operations import BillingRecord


class BillingRecordRepository(RepositoryBase):
    """Repository for billing records."""

    async def create(self, session: AsyncSession, user_id: str, amount: float, currency: str, payment_type: str, provider: str, metadata: dict = None):
        from app.models.operations import BillingRecord
        record = BillingRecord(
            user_id=user_id,
            amount=amount,
            currency=currency,
            payment_type=payment_type,
            provider=provider,
            event_metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
        session.add(record)
        await session.flush()
        return record

    async def record_revenue_event(self, session: AsyncSession, user_id: str, event_type: str, amount: float, currency: str, metadata: dict = None):
        from app.models.operations import RevenueEvent
        event = RevenueEvent(
            user_id=user_id,
            event_type=event_type,
            amount=amount,
            currency=currency,
            event_metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
        session.add(event)
        await session.flush()
        return event


class RevenueEventRepository(RepositoryBase):
    """Repository for revenue events."""

    async def create(self, session: AsyncSession, user_id: str, event_type: str, amount: float, currency: str, metadata: dict = None):
        from app.models.operations import RevenueEvent
        event = RevenueEvent(
            user_id=user_id,
            event_type=event_type,
            amount=amount,
            currency=currency,
            event_metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
        session.add(event)
        await session.flush()
        return event