"""PostgreSQL repository for deterministic practice exams."""

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RepositoryBase
from app.models.exam import PracticeExamAttempt


class PracticeExamAttemptRepository(RepositoryBase):
    async def get_by_id_and_user(self, attempt_id: UUID, user_id: UUID) -> Optional[PracticeExamAttempt]:
        result = await self.session.execute(
            select(PracticeExamAttempt).where(
                PracticeExamAttempt.id == attempt_id,
                PracticeExamAttempt.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: UUID, limit: int = 20) -> list[PracticeExamAttempt]:
        result = await self.session.execute(
            select(PracticeExamAttempt)
            .where(PracticeExamAttempt.user_id == user_id)
            .order_by(desc(PracticeExamAttempt.started_at))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, data: dict[str, Any]) -> PracticeExamAttempt:
        attempt = PracticeExamAttempt(**data)
        self.session.add(attempt)
        await self.flush()
        return attempt

    async def set_answers(self, attempt_id: UUID, user_id: UUID, answers: dict) -> Optional[PracticeExamAttempt]:
        result = await self.session.execute(
            update(PracticeExamAttempt)
            .where(
                PracticeExamAttempt.id == attempt_id,
                PracticeExamAttempt.user_id == user_id,
                PracticeExamAttempt.status == "in_progress",
            )
            .values(answers=answers)
            .returning(PracticeExamAttempt)
        )
        return result.scalar_one_or_none()

    async def complete(
        self,
        attempt_id: UUID,
        user_id: UUID,
        score: float,
        correct: int,
    ) -> Optional[PracticeExamAttempt]:
        result = await self.session.execute(
            update(PracticeExamAttempt)
            .where(
                PracticeExamAttempt.id == attempt_id,
                PracticeExamAttempt.user_id == user_id,
                PracticeExamAttempt.status == "in_progress",
            )
            .values(
                status="completed",
                score=score,
                correct=correct,
                completed_at=datetime.now(timezone.utc),
            )
            .returning(PracticeExamAttempt)
        )
        return result.scalar_one_or_none()
