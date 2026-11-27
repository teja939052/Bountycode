"""Company directory repositories — PostgreSQL-backed."""
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RepositoryBase
from app.models.content import CompanyDirectory


class CompanyDirectoryRepository(RepositoryBase):
    """Repository for company directory entries."""

    async def list_all(self, session: AsyncSession) -> List[CompanyDirectory]:
        result = await session.execute(
            select(CompanyDirectory).order_by(CompanyDirectory.name)
        )
        return result.scalars().all()

    async def search(self, session: AsyncSession, query: str) -> List[CompanyDirectory]:
        result = await session.execute(
            select(CompanyDirectory).where(
                CompanyDirectory.name.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, company_id: str) -> Optional[CompanyDirectory]:
        result = await session.execute(
            select(CompanyDirectory).where(CompanyDirectory.id == company_id)
        )
        return result.scalar_one_or_none()