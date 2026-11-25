"""PostgreSQL writers — SQLAlchemy AsyncSession-based domain writers.

Writes transformed data to PostgreSQL tables. Writers flush but never
commit — the caller owns the transaction boundary. Supports idempotent
upserts via UserIdentityMap for user-scoped records.
"""

import logging
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RepositoryBase
from app.models.identity import User, UserIdentityMap
from app.repositories.identity import (
    UserIdentityMapRepository,
    UserProfileRepository,
    UserRepository,
)

logger = logging.getLogger(__name__)


class PostgresWriter:
    """Base writer for a single domain.

    Provides idempotent write-through for user-scoped records via
    UserIdentityMap. Each domain writer implements `write_record`.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.identity_repo = UserIdentityMapRepository(session)
        self.user_repo = UserRepository(session)
        self.profile_repo = UserProfileRepository(session)

    async def resolve_postgres_user_id(self, legacy_mongo_id: str) -> Optional[UUID]:
        return await self.identity_repo.get_postgres_id(legacy_mongo_id)

    async def create_identity_map(self, legacy_mongo_id: str, postgres_user_id: UUID) -> None:
        await self.identity_repo.create_mapping(legacy_mongo_id, postgres_user_id)

    async def write_record(self, table: str, data: dict) -> Any:
        raise NotImplementedError

    async def write_batch(
        self,
        table: str,
        records: list[dict],
    ) -> tuple[int, int, list[str]]:
        imported = 0
        failed = 0
        errors: list[str] = []
        for record in records:
            try:
                await self.write_record(table, record)
                imported += 1
            except Exception as exc:  # noqa: BLE001
                failed += 1
                errors.append(str(exc))
                await self.session.rollback()
        return imported, failed, errors


class UserWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> User:
        user = User(**data)
        self.session.add(user)
        await self.session.flush()
        return user


class GamificationProfileWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> Any:
        from app.models.gamification import GamificationProfile, XPEventLedger

        if table == "gamification_profiles":
            profile = GamificationProfile(**data)
            self.session.add(profile)
            await self.session.flush()
            return profile
        if table == "xp_event_ledger":
            event = XPEventLedger(**data)
            self.session.add(event)
            await self.session.flush()
            return event
        raise ValueError(f"Unknown table: {table}")


class CodingSubmissionWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> Any:
        from app.models.assessments import CodingSubmission, ExecutionResult

        if table == "coding_submissions":
            submission = CodingSubmission(**data)
            self.session.add(submission)
            await self.session.flush()
            return submission
        if table == "execution_results":
            result = ExecutionResult(**data)
            self.session.add(result)
            await self.session.flush()
            return result
        raise ValueError(f"Unknown table: {table}")


class AssessmentAttemptWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> Any:
        from app.models.assessments import AssessmentAttempt
        attempt = AssessmentAttempt(**data)
        self.session.add(attempt)
        await self.session.flush()
        return attempt


class OASessionWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> Any:
        from app.models.assessments import OASession
        session = OASession(**data)
        self.session.add(session)
        await self.session.flush()
        return session


class InterviewSessionWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> Any:
        from app.models.assessments import InterviewSession
        session = InterviewSession(**data)
        self.session.add(session)
        await self.session.flush()
        return session


class CareerProfileWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> Any:
        if table == "career_profiles":
            from app.models.career import CareerProfile
            profile = CareerProfile(**data)
            self.session.add(profile)
            await self.session.flush()
            return profile
        if table == "user_profiles":
            from app.models.identity import UserProfile
            profile = UserProfile(**data)
            self.session.add(profile)
            await self.session.flush()
            return profile
        raise ValueError(f"Unknown table: {table}")


class ResumeWriter(PostgresWriter):
    async def write_record(self, table: str, data: dict) -> Any:
        from app.models.career import ResumeMetadata
        resume = ResumeMetadata(**data)
        self.session.add(resume)
        await self.session.flush()
        return resume


WRITERS = {
    "users": UserWriter,
    "gamification_profiles": GamificationProfileWriter,
    "xp_event_ledger": GamificationProfileWriter,
    "skills": PostgresWriter,
    "learning_attempts": PostgresWriter,
    "learning_evidence": PostgresWriter,
    "coding_submissions": CodingSubmissionWriter,
    "execution_results": CodingSubmissionWriter,
    "assessment_attempts": AssessmentAttemptWriter,
    "oa_sessions": OASessionWriter,
    "interview_sessions": InterviewSessionWriter,
    "career_profiles": CareerProfileWriter,
    "user_profiles": CareerProfileWriter,
    "resumes": ResumeWriter,
    "payments": PostgresWriter,
    "repair_missions": PostgresWriter,
    "srs_cards": PostgresWriter,
    "analytics_events": PostgresWriter,
    "audit_logs": PostgresWriter,
    "coupons": PostgresWriter,
}
