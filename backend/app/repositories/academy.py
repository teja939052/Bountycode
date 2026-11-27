"""Repositories for the PostgreSQL-backed Academy learner journey."""
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academy import AcademyDiagnosticSession, AcademyLearnerProfile, AcademyLearningPlan


def as_uuid(value: UUID | str) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


def model_dict(model: Any) -> dict:
    if model is None:
        return {}
    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        if isinstance(value, UUID):
            value = str(value)
        elif isinstance(value, datetime):
            value = value.isoformat()
        result[column.name] = value
    return result


class AcademyLearnerProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user(self, user_id: UUID | str) -> AcademyLearnerProfile | None:
        result = await self.session.scalar(
            select(AcademyLearnerProfile).where(AcademyLearnerProfile.user_id == as_uuid(user_id))
        )
        return result

    async def upsert(self, user_id: UUID | str, values: dict[str, Any]) -> AcademyLearnerProfile:
        model = await self.get_by_user(user_id)
        if model is None:
            model = AcademyLearnerProfile(user_id=as_uuid(user_id))
            self.session.add(model)
        for key, value in values.items():
            if key not in {"id", "user_id", "created_at"} and hasattr(model, key):
                setattr(model, key, value)
        await self.session.flush()
        return model


class AcademyDiagnosticSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID | str, diagnostic_id: str, question_ids: list[str]) -> AcademyDiagnosticSession:
        model = AcademyDiagnosticSession(
            user_id=as_uuid(user_id),
            diagnostic_id=diagnostic_id,
            question_ids=question_ids,
            answers=[],
            status="in_progress",
        )
        self.session.add(model)
        await self.session.flush()
        return model

    async def get(self, user_id: UUID | str, diagnostic_id: str, for_update: bool = False) -> AcademyDiagnosticSession | None:
        query = select(AcademyDiagnosticSession).where(
            AcademyDiagnosticSession.user_id == as_uuid(user_id),
            AcademyDiagnosticSession.diagnostic_id == diagnostic_id,
        )
        if for_update:
            query = query.with_for_update()
        return await self.session.scalar(query)

    async def latest_completed(self, user_id: UUID | str) -> AcademyDiagnosticSession | None:
        return await self.session.scalar(
            select(AcademyDiagnosticSession)
            .where(
                AcademyDiagnosticSession.user_id == as_uuid(user_id),
                AcademyDiagnosticSession.status == "completed",
            )
            .order_by(AcademyDiagnosticSession.completed_at.desc())
            .limit(1)
        )

    async def append_answer(self, model: AcademyDiagnosticSession, answer: dict[str, Any]) -> bool:
        answers = list(model.answers or [])
        if any(item.get("question_id") == answer.get("question_id") for item in answers):
            return False
        answers.append(answer)
        model.answers = answers
        model.updated_at = datetime.now(timezone.utc)
        await self.session.flush()
        return True

    async def complete(self, model: AcademyDiagnosticSession, result: dict[str, Any]) -> None:
        model.status = "completed"
        model.result = result
        model.completed_at = datetime.now(timezone.utc)
        model.updated_at = model.completed_at
        await self.session.flush()


class AcademyLearningPlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(self, user_id: UUID | str, plan: dict[str, Any]) -> AcademyLearningPlan:
        model = await self.session.scalar(
            select(AcademyLearningPlan).where(AcademyLearningPlan.user_id == as_uuid(user_id))
        )
        if model is None:
            model = AcademyLearningPlan(user_id=as_uuid(user_id), plan=plan)
            self.session.add(model)
        else:
            model.plan = plan
            model.updated_at = datetime.now(timezone.utc)
        await self.session.flush()
        return model
