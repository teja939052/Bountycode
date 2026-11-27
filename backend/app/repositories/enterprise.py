"""Enterprise domain repositories — PostgreSQL replacements for MongoDB collection operations."""

from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RepositoryBase
from app.models.enterprise import Cohort, SkillGraph, Gamification
from app.models.identity import User


class CohortRepository(RepositoryBase):
    """Repository for cohorts — replaces cohorts collection."""

    async def get_by_id(self, session: AsyncSession, cohort_id: str) -> Optional[Cohort]:
        result = await session.execute(
            select(Cohort).where(Cohort.id == cohort_id)
        )
        return result.scalar_one_or_none()

    async def get_by_admin(self, session: AsyncSession, admin_id: str) -> List[Cohort]:
        result = await session.execute(
            select(Cohort).where(Cohort.admin_id == admin_id).order_by(Cohort.created_at.desc())
        )
        return result.scalars().all()

    async def create(self, session: AsyncSession, name: str, institution: str, admin_id: str, student_ids: List[str] = None) -> Cohort:
        cohort = Cohort(
            name=name,
            institution=institution,
            admin_id=admin_id,
            student_ids=student_ids or [],
            created_at=datetime.now(timezone.utc),
        )
        session.add(cohort)
        await session.flush()
        return cohort


class SkillGraphRepository(RepositoryBase):
    """Repository for skill graphs — replaces skill_graphs collection."""

    async def get_by_user(self, session: AsyncSession, user_id: str) -> Optional[SkillGraph]:
        result = await session.execute(
            select(SkillGraph).where(SkillGraph.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, user_id: str) -> SkillGraph:
        sg = SkillGraph(user_id=user_id, overall_score=0, diamonds=0, level=1, streak=0)
        session.add(sg)
        await session.flush()
        return sg


class GamificationRepository(RepositoryBase):
    """Repository for gamification data — replaces gamification collection."""

    async def get_by_user(self, session: AsyncSession, user_id: str) -> Optional[Gamification]:
        result = await session.execute(
            select(Gamification).where(Gamification.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, user_id: str) -> Gamification:
        gam = Gamification(user_id=user_id, xp=0, level=1, diamonds=0, streak=0)
        session.add(gam)
        await session.flush()
        return gam