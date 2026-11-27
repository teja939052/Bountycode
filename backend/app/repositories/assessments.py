"""Assessments domain repositories — PostgreSQL replacements for Motor collection operations.

Collections migrated:
- coding_challenges_collection / submissions_collection -> coding_submissions + execution_results
- oa_sessions_collection -> oa_sessions
- interviews_collection -> interview_sessions
- company_mock_tests_collection -> assessment_attempts (company mock sessions)
- aptitude_tests_collection -> assessment_attempts (aptitude test sessions)
- solved_problems_collection -> responses

Repositories use injected AsyncSession. Transaction boundaries are owned by
the service layer, not the repository. Repositories flush but never commit.

Dual-database safety: never silently falls back to Motor for PostgreSQL-owned
operations.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Set
from uuid import UUID

from sqlalchemy import select, update, delete, func, desc, asc, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import RepositoryBase
from app.models.assessments import (
    AssessmentAttempt,
    AssessmentSection,
    CodingSubmission,
    CompanyAssessmentMetadata,
    ExecutionResult,
    InterviewBooking,
    InterviewSession,
    OASession,
    QuestionAnswer,
    Response,
    SolvedProblem,
)
from app.models.career import ResumeMetadata
from app.models.content import AssessmentDefinition, AssessmentVariant
from app.models.identity import User


# ══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT DEFINITION REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class AssessmentDefinitionRepository(RepositoryBase):
    """Repository for assessment definitions — company/topic test blueprints."""

    async def get_by_id(self, definition_id: UUID) -> Optional[AssessmentDefinition]:
        result = await self.session.execute(
            select(AssessmentDefinition).where(AssessmentDefinition.id == definition_id)
        )
        return result.scalar_one_or_none()

    async def list_active(
        self,
        assessment_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[AssessmentDefinition]:
        query = select(AssessmentDefinition).where(AssessmentDefinition.is_active == True)  # noqa: E712
        if assessment_type:
            query = query.where(AssessmentDefinition.assessment_type == assessment_type)
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, definition_data: dict) -> AssessmentDefinition:
        definition = AssessmentDefinition(**definition_data)
        self.session.add(definition)
        await self.flush()
        return definition


class AssessmentVariantRepository(RepositoryBase):
    """Repository for assessment variants — question selection snapshots."""

    async def get_by_id(self, variant_id: UUID) -> Optional[AssessmentVariant]:
        result = await self.session.execute(
            select(AssessmentVariant).where(AssessmentVariant.id == variant_id)
        )
        return result.scalar_one_or_none()

    async def get_by_variant_id(self, variant_id: str) -> Optional[AssessmentVariant]:
        result = await self.session.execute(
            select(AssessmentVariant).where(AssessmentVariant.variant_id == variant_id)
        )
        return result.scalar_one_or_none()

    async def list_by_definition(
        self,
        definition_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[AssessmentVariant]:
        result = await self.session.execute(
            select(AssessmentVariant)
            .where(AssessmentVariant.definition_id == definition_id)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, variant_data: dict) -> AssessmentVariant:
        variant = AssessmentVariant(**variant_data)
        self.session.add(variant)
        await self.flush()
        return variant


# ══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT ATTEMPT REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class AssessmentAttemptRepository(RepositoryBase):
    """Repository for assessment attempts — one per user per assessment session."""

    async def get_by_id(self, attempt_id: UUID) -> Optional[AssessmentAttempt]:
        result = await self.session.execute(
            select(AssessmentAttempt).where(AssessmentAttempt.id == attempt_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[AssessmentAttempt]:
        result = await self.session.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.user_id == user_id)
            .order_by(desc(AssessmentAttempt.started_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_user_and_assessment(
        self,
        user_id: UUID,
        assessment_id: UUID,
        limit: int = 10,
    ) -> List[AssessmentAttempt]:
        result = await self.session.execute(
            select(AssessmentAttempt)
            .where(
                AssessmentAttempt.user_id == user_id,
                AssessmentAttempt.assessment_id == assessment_id,
            )
            .order_by(desc(AssessmentAttempt.started_at))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_in_progress_by_user(
        self,
        user_id: UUID,
    ) -> List[AssessmentAttempt]:
        result = await self.session.execute(
            select(AssessmentAttempt)
            .where(
                AssessmentAttempt.user_id == user_id,
                AssessmentAttempt.status == "in_progress",
            )
        )
        return list(result.scalars().all())

    async def create(self, attempt_data: dict) -> AssessmentAttempt:
        attempt = AssessmentAttempt(**attempt_data)
        self.session.add(attempt)
        await self.flush()
        return attempt

    async def complete(
        self,
        attempt_id: UUID,
        score: Optional[float],
        completed_at: Optional[datetime] = None,
    ) -> Optional[AssessmentAttempt]:
        updates: Dict[str, Any] = {
            "status": "completed",
            "score": score,
        }
        if completed_at is not None:
            updates["completed_at"] = completed_at
        result = await self.session.execute(
            update(AssessmentAttempt)
            .where(AssessmentAttempt.id == attempt_id)
            .values(**updates)
            .returning(AssessmentAttempt)
        )
        return result.scalar_one_or_none()

    async def abandon(self, attempt_id: UUID) -> Optional[AssessmentAttempt]:
        result = await self.session.execute(
            update(AssessmentAttempt)
            .where(AssessmentAttempt.id == attempt_id)
            .values(status="abandoned")
            .returning(AssessmentAttempt)
        )
        return result.scalar_one_or_none()


# ══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT SECTION REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class AssessmentSectionRepository(RepositoryBase):
    """Repository for sections within an assessment attempt."""

    async def get_by_id(self, section_id: UUID) -> Optional[AssessmentSection]:
        result = await self.session.execute(
            select(AssessmentSection).where(AssessmentSection.id == section_id)
        )
        return result.scalar_one_or_none()

    async def list_by_attempt(
        self,
        attempt_id: UUID,
    ) -> List[AssessmentSection]:
        result = await self.session.execute(
            select(AssessmentSection)
            .where(AssessmentSection.attempt_id == attempt_id)
            .order_by(asc(AssessmentSection.started_at))
        )
        return list(result.scalars().all())

    async def create(self, section_data: dict) -> AssessmentSection:
        section = AssessmentSection(**section_data)
        self.session.add(section)
        await self.flush()
        return section

    async def complete(
        self,
        section_id: UUID,
        score: Optional[float],
        completed_at: Optional[datetime] = None,
    ) -> Optional[AssessmentSection]:
        updates: Dict[str, Any] = {"score": score}
        if completed_at is not None:
            updates["completed_at"] = completed_at
        result = await self.session.execute(
            update(AssessmentSection)
            .where(AssessmentSection.id == section_id)
            .values(**updates)
            .returning(AssessmentSection)
        )
        return result.scalar_one_or_none()


# ══════════════════════════════════════════════════════════════════════════════
# RESPONSE REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class ResponseRepository(RepositoryBase):
    """Repository for individual question responses within an assessment section.

    Idempotency: a (section_id, question_id, idempotency_key) combination is
    database-enforced unique (partial index). Duplicate responses under retry
    or concurrent requests are rejected at the DB level.
    """

    async def get_by_id(self, response_id: UUID) -> Optional[Response]:
        result = await self.session.execute(
            select(Response).where(Response.id == response_id)
        )
        return result.scalar_one_or_none()

    async def list_by_section(
        self,
        section_id: UUID,
    ) -> List[Response]:
        result = await self.session.execute(
            select(Response)
            .where(Response.section_id == section_id)
            .order_by(asc(Response.created_at))
        )
        return list(result.scalars().all())

    async def list_by_attempt(
        self,
        attempt_id: UUID,
    ) -> List[Response]:
        result = await self.session.execute(
            select(Response)
            .join(AssessmentSection, Response.section_id == AssessmentSection.id)
            .where(AssessmentSection.attempt_id == attempt_id)
            .order_by(asc(Response.created_at))
        )
        return list(result.scalars().all())

    async def create(self, response_data: dict) -> Response:
        response = Response(**response_data)
        self.session.add(response)
        await self.flush()
        return response

    async def update(
        self,
        response_id: UUID,
        updates: dict,
    ) -> Optional[Response]:
        result = await self.session.execute(
            update(Response)
            .where(Response.id == response_id)
            .values(**updates)
            .returning(Response)
        )
        return result.scalar_one_or_none()


# ══════════════════════════════════════════════════════════════════════════════
# CODING SUBMISSION REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class CodingSubmissionRepository(RepositoryBase):
    """Repository for coding challenge submissions — migrated from MongoDB submissions.

    Idempotency: a (user_id, question_id, idempotency_key) combination is
    database-enforced unique (partial index). Duplicate submissions under retry
    or concurrent requests are rejected at the DB level.

    Security: execution_result JSONB must never contain protected test cases,
    expected answers, or hidden grading data. Only execution outcomes (passed,
    time, memory, status) are stored.
    """

    async def get_by_id(self, submission_id: UUID) -> Optional[CodingSubmission]:
        result = await self.session.execute(
            select(CodingSubmission).where(CodingSubmission.id == submission_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[CodingSubmission]:
        result = await self.session.execute(
            select(CodingSubmission)
            .where(CodingSubmission.user_id == user_id)
            .order_by(desc(CodingSubmission.submitted_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def list_by_user_and_question(
        self,
        user_id: UUID,
        question_id: str,
    ) -> List[CodingSubmission]:
        result = await self.session.execute(
            select(CodingSubmission)
            .where(
                CodingSubmission.user_id == user_id,
                CodingSubmission.question_id == question_id,
            )
            .order_by(desc(CodingSubmission.submitted_at))
        )
        return list(result.scalars().all())

    async def list_by_question(
        self,
        question_id: str,
        status: Optional[str] = None,
        language: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[CodingSubmission]:
        query = select(CodingSubmission).where(
            CodingSubmission.question_id == question_id
        )
        if status:
            query = query.where(CodingSubmission.status == status)
        if language:
            query = query.where(CodingSubmission.language == language)
        query = query.order_by(desc(CodingSubmission.submitted_at))
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_idempotency_key(
        self,
        user_id: UUID,
        idempotency_key: str,
    ) -> Optional[CodingSubmission]:
        result = await self.session.execute(
            select(CodingSubmission)
            .where(
                CodingSubmission.user_id == user_id,
                CodingSubmission.idempotency_key == idempotency_key,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, submission_data: dict) -> CodingSubmission:
        submission = CodingSubmission(**submission_data)
        self.session.add(submission)
        await self.flush()
        return submission

    async def update_result(
        self,
        submission_id: UUID,
        status: str,
        execution_result: dict,
        score: Optional[float] = None,
    ) -> Optional[CodingSubmission]:
        updates: Dict[str, Any] = {
            "status": status,
            "execution_result": execution_result,
        }
        if score is not None:
            updates["score"] = score
        result = await self.session.execute(
            update(CodingSubmission)
            .where(CodingSubmission.id == submission_id)
            .values(**updates)
            .returning(CodingSubmission)
        )
        return result.scalar_one_or_none()


# ══════════════════════════════════════════════════════════════════════════════
# EXECUTION RESULT REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class ExecutionResultRepository(RepositoryBase):
    """Repository for individual test case execution results.

    Security: `expected` and `actual` fields may contain expected outputs for
    visible test cases only. Hidden test case expected values must never be
    stored here or exposed through frontend responses.
    """

    async def get_by_id(self, result_id: UUID) -> Optional[ExecutionResult]:
        result = await self.session.execute(
            select(ExecutionResult).where(ExecutionResult.id == result_id)
        )
        return result.scalar_one_or_none()

    async def list_by_submission(
        self,
        submission_id: UUID,
    ) -> List[ExecutionResult]:
        result = await self.session.execute(
            select(ExecutionResult)
            .where(ExecutionResult.submission_id == submission_id)
            .order_by(asc(ExecutionResult.created_at))
        )
        return list(result.scalars().all())

    async def create(self, result_data: dict) -> ExecutionResult:
        result = ExecutionResult(**result_data)
        self.session.add(result)
        await self.flush()
        return result

    async def create_many(
        self,
        results: List[dict],
    ) -> List[ExecutionResult]:
        entities = [ExecutionResult(**data) for data in results]
        self.session.add_all(entities)
        await self.flush()
        return entities

    async def passed_count_by_submission(
        self,
        submission_id: UUID,
    ) -> int:
        result = await self.session.execute(
            select(func.count(ExecutionResult.id))
            .where(
                ExecutionResult.submission_id == submission_id,
                ExecutionResult.passed == True,  # noqa: E712
            )
        )
        return result.scalar_one()

    async def total_count_by_submission(
        self,
        submission_id: UUID,
    ) -> int:
        result = await self.session.execute(
            select(func.count(ExecutionResult.id))
            .where(ExecutionResult.submission_id == submission_id)
        )
        return result.scalar_one()


# ══════════════════════════════════════════════════════════════════════════════
# ONLINE ASSESSMENT SESSION REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class OASessionRepository(RepositoryBase):
    """Repository for online assessment sessions — migrated from MongoDB oa_sessions.

    Private candidate information (integrity signals, tab switches, fullscreen
    exits) is stored in the session record but must not be exposed in public
    API responses.
    """

    async def get_by_id(self, session_id: UUID) -> Optional[OASession]:
        result = await self.session.execute(
            select(OASession).where(OASession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[OASession]:
        result = await self.session.execute(
            select(OASession)
            .where(OASession.user_id == user_id)
            .order_by(desc(OASession.started_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def list_by_user_and_company(
        self,
        user_id: UUID,
        company: str,
    ) -> List[OASession]:
        result = await self.session.execute(
            select(OASession)
            .where(OASession.user_id == user_id, OASession.company == company)
            .order_by(desc(OASession.started_at))
        )
        return list(result.scalars().all())

    async def get_in_progress_by_user(
        self,
        user_id: UUID,
    ) -> List[OASession]:
        result = await self.session.execute(
            select(OASession)
            .where(
                OASession.user_id == user_id,
                OASession.status == "in_progress",
            )
        )
        return list(result.scalars().all())

    async def create(self, session_data: dict) -> OASession:
        session = OASession(**session_data)
        self.session.add(session)
        await self.flush()
        return session

    async def update(
        self,
        session_id: UUID,
        updates: dict,
    ) -> Optional[OASession]:
        result = await self.session.execute(
            update(OASession)
            .where(OASession.id == session_id)
            .values(**updates)
            .returning(OASession)
        )
        return result.scalar_one_or_none()

    async def complete(
        self,
        session_id: UUID,
        completed_at: Optional[datetime] = None,
    ) -> Optional[OASession]:
        updates: Dict[str, Any] = {"status": "completed"}
        if completed_at is not None:
            updates["completed_at"] = completed_at
        result = await self.session.execute(
            update(OASession)
            .where(OASession.id == session_id)
            .values(**updates)
            .returning(OASession)
        )
        return result.scalar_one_or_none()

    def to_public_dict(self, session: OASession) -> dict:
        """Return a client-safe representation — excludes private integrity data."""
        return {
            "id": str(session.id),
            "user_id": str(session.user_id),
            "company": session.company,
            "role": session.role,
            "blueprint": session.blueprint,
            "mode": session.mode,
            "status": session.status,
            "started_at": session.started_at.isoformat() if session.started_at else None,
            "completed_at": session.completed_at.isoformat() if session.completed_at else None,
            # `questions` are served as safe questions (without answer keys) by the
            # service layer, not as raw JSONB from this repository.
        }

    def to_private_dict(self, session: OASession) -> dict:
        """Full representation including integrity signals — internal/admin use only."""
        return {
            "id": str(session.id),
            "user_id": str(session.user_id),
            "company": session.company,
            "role": session.role,
            "blueprint": session.blueprint,
            "mode": session.mode,
            "integrity_enabled": session.integrity_enabled,
            "status": session.status,
            "questions": session.questions,
            "started_at": session.started_at.isoformat() if session.started_at else None,
            "completed_at": session.completed_at.isoformat() if session.completed_at else None,
        }


# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEW SESSION REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class InterviewSessionRepository(RepositoryBase):
    """Repository for mock interview sessions — migrated from MongoDB interviews.

    Access control: a user must never access another user's interview session.
    All queries filter by user_id.
    """

    async def get_by_id(self, session_id: UUID) -> Optional[InterviewSession]:
        result = await self.session.execute(
            select(InterviewSession).where(InterviewSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_and_user(
        self,
        session_id: UUID,
        user_id: UUID,
    ) -> Optional[InterviewSession]:
        result = await self.session.execute(
            select(InterviewSession).where(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[InterviewSession]:
        result = await self.session.execute(
            select(InterviewSession)
            .where(InterviewSession.user_id == user_id)
            .order_by(desc(InterviewSession.started_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_in_progress_by_user(
        self,
        user_id: UUID,
    ) -> List[InterviewSession]:
        result = await self.session.execute(
            select(InterviewSession)
            .where(
                InterviewSession.user_id == user_id,
                InterviewSession.status == "in_progress",
            )
        )
        return list(result.scalars().all())

    async def create(self, session_data: dict) -> InterviewSession:
        session = InterviewSession(**session_data)
        self.session.add(session)
        await self.flush()
        return session

    async def update(
        self,
        session_id: UUID,
        updates: dict,
    ) -> Optional[InterviewSession]:
        result = await self.session.execute(
            update(InterviewSession)
            .where(InterviewSession.id == session_id)
            .values(**updates)
            .returning(InterviewSession)
        )
        return result.scalar_one_or_none()

    async def complete(
        self,
        session_id: UUID,
        score: Optional[float],
        completed_at: Optional[datetime] = None,
    ) -> Optional[InterviewSession]:
        updates: Dict[str, Any] = {"status": "completed", "score": score}
        if completed_at is not None:
            updates["completed_at"] = completed_at
        result = await self.session.execute(
            update(InterviewSession)
            .where(InterviewSession.id == session_id)
            .values(**updates)
            .returning(InterviewSession)
        )
        return result.scalar_one_or_none()


# ══════════════════════════════════════════════════════════════════════════════
# COMPANY ASSESSMENT METADATA REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class CompanyAssessmentMetadataRepository(RepositoryBase):
    """Repository for company-specific assessment metadata.

    Company assessment formats retain source, verification date, and confidence
    where those properties exist. Never claims leaked or private company
    questions are official.
    """

    async def get_by_id(self, metadata_id: UUID) -> Optional[CompanyAssessmentMetadata]:
        result = await self.session.execute(
            select(CompanyAssessmentMetadata).where(CompanyAssessmentMetadata.id == metadata_id)
        )
        return result.scalar_one_or_none()

    async def get_by_company_role_type(
        self,
        company: str,
        role: str,
        assessment_type: str,
    ) -> Optional[CompanyAssessmentMetadata]:
        result = await self.session.execute(
            select(CompanyAssessmentMetadata).where(
                CompanyAssessmentMetadata.company == company,
                CompanyAssessmentMetadata.role == role,
                CompanyAssessmentMetadata.assessment_type == assessment_type,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_company(
        self,
        company: str,
    ) -> List[CompanyAssessmentMetadata]:
        result = await self.session.execute(
            select(CompanyAssessmentMetadata)
            .where(CompanyAssessmentMetadata.company == company)
            .order_by(asc(CompanyAssessmentMetadata.created_at))
        )
        return list(result.scalars().all())

    async def create(self, metadata_data: dict) -> CompanyAssessmentMetadata:
        metadata = CompanyAssessmentMetadata(**metadata_data)
        self.session.add(metadata)
        await self.flush()
        return metadata

    async def update(
        self,
        metadata_id: UUID,
        updates: dict,
    ) -> Optional[CompanyAssessmentMetadata]:
        result = await self.session.execute(
            update(CompanyAssessmentMetadata)
            .where(CompanyAssessmentMetadata.id == metadata_id)
            .values(**updates, updated_at=datetime.now(timezone.utc))
            .returning(CompanyAssessmentMetadata)
        )
        return result.scalar_one_or_none()


# ════════════════════════════════════════════════════════════════════════════════
# RESUME METADATA REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════

class ResumeMetadataRepository(RepositoryBase):
    """Repository for resume metadata — migrated from MongoDB `resumes` collection.

    Actual resume file bytes live in Supabase Storage; this table holds metadata
    and extracted text/analysis results.
    """

    async def get_by_id(self, resume_id: UUID) -> Optional[ResumeMetadata]:
        result = await self.session.execute(
            select(ResumeMetadata).where(ResumeMetadata.id == resume_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ResumeMetadata]:
        result = await self.session.execute(
            select(ResumeMetadata)
            .where(ResumeMetadata.user_id == user_id)
            .order_by(desc(ResumeMetadata.created_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, resume_data: dict) -> ResumeMetadata:
        resume = ResumeMetadata(**resume_data)
        self.session.add(resume)
        await self.flush()
        return resume

    async def update(
        self,
        resume_id: UUID,
        updates: dict,
    ) -> Optional[ResumeMetadata]:
        result = await self.session.execute(
            update(ResumeMetadata)
            .where(ResumeMetadata.id == resume_id)
            .values(**updates)
            .returning(ResumeMetadata)
        )
        return result.scalar_one_or_none()


# ═══════════════════════════════════════════════════════════════════════════════
# INTERVIEW BOOKING REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════

class InterviewBookingRepository(RepositoryBase):
    """Repository for scheduled interview bookings.

    Migrated from MongoDB `interview_bookings` collection.
    """

    async def get_by_id(self, booking_id: UUID) -> Optional[InterviewBooking]:
        result = await self.session.execute(
            select(InterviewBooking).where(InterviewBooking.id == booking_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[InterviewBooking]:
        result = await self.session.execute(
            select(InterviewBooking)
            .where(InterviewBooking.user_id == user_id)
            .order_by(desc(InterviewBooking.scheduled_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def list_by_user_and_status(
        self,
        user_id: UUID,
        status: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[InterviewBooking]:
        result = await self.session.execute(
            select(InterviewBooking)
            .where(InterviewBooking.user_id == user_id)
            .where(InterviewBooking.status == status)
            .order_by(desc(InterviewBooking.scheduled_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, booking_data: dict) -> InterviewBooking:
        booking = InterviewBooking(**booking_data)
        self.session.add(booking)
        await self.flush()
        return booking

    async def update(
        self,
        booking_id: UUID,
        updates: dict,
    ) -> Optional[InterviewBooking]:
        result = await self.session.execute(
            update(InterviewBooking)
            .where(InterviewBooking.id == booking_id)
            .values(**updates)
            .returning(InterviewBooking)
        )
        return result.scalar_one_or_none()

    async def count_by_user_and_status(
        self,
        user_id: UUID,
        status: str,
    ) -> int:
        result = await self.session.execute(
            select(func.count(InterviewBooking.id))
            .where(InterviewBooking.user_id == user_id)
            .where(InterviewBooking.status == status)
        )
        return result.scalar_one()


# ═══════════════════════════════════════════════════════════════════════════════
# SOLVED PROBLEM REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class SolvedProblemRepository(RepositoryBase):
    """Repository for daily challenge / problem solve history.

    Migrated from MongoDB `solved_problems` collection.
    """

    async def get_by_id(self, problem_id: UUID) -> Optional[SolvedProblem]:
        result = await self.session.execute(
            select(SolvedProblem).where(SolvedProblem.id == problem_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[SolvedProblem]:
        result = await self.session.execute(
            select(SolvedProblem)
            .where(SolvedProblem.user_id == user_id)
            .order_by(desc(SolvedProblem.created_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, problem_data: dict) -> SolvedProblem:
        problem = SolvedProblem(**problem_data)
        self.session.add(problem)
        await self.flush()
        return problem

    async def get_solved_problem_ids(
        self,
        user_id: UUID,
        problem_ids: List[str],
    ) -> Set[str]:
        result = await self.session.execute(
            select(SolvedProblem.problem_id)
            .where(SolvedProblem.user_id == user_id)
            .where(SolvedProblem.problem_id.in_(problem_ids))
        )
        return {str(row[0]) for row in result.all()}


# ══════════════════════════════════════════════════════════════════════════════
# QUESTION ANSWER REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class QuestionAnswerRepository(RepositoryBase):
    """Repository for question answer records.

    Migrated from MongoDB `question_answers` collection.
    """

    async def get_by_id(self, answer_id: UUID) -> Optional[QuestionAnswer]:
        result = await self.session.execute(
            select(QuestionAnswer).where(QuestionAnswer.id == answer_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[QuestionAnswer]:
        result = await self.session.execute(
            select(QuestionAnswer)
            .where(QuestionAnswer.user_id == user_id)
            .order_by(desc(QuestionAnswer.created_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, answer_data: dict) -> QuestionAnswer:
        answer = QuestionAnswer(**answer_data)
        self.session.add(answer)
        await self.flush()
        return answer

    async def get_best_scores_by_user_and_questions(
        self,
        user_id: UUID,
        question_ids: List[str],
    ) -> Dict[str, float]:
        result = await self.session.execute(
            select(QuestionAnswer.question_id, func.max(QuestionAnswer.score))
            .where(QuestionAnswer.user_id == user_id)
            .where(QuestionAnswer.question_id.in_(question_ids))
            .group_by(QuestionAnswer.question_id)
        )
        return {str(row[0]): float(row[1] or 0) for row in result.all()}
