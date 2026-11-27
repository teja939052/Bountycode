"""PostgreSQL-based Assessment service — migrates assessment persistence from MongoDB Motor.

Provides the canonical assessment persistence flow:
  1. Idempotency check (by idempotency_key)
  2. Create assessment attempt / OA session / interview session
  3. Record sections and responses
  4. Store coding submissions and execution results
  5. Complete assessment with scoring
  6. Emit learning evidence (via PostgresLearningService)
  7. Award XP (via PostgresGamificationService.record_practice, gated by
     xp_event_ledger idempotency)

All assessment writes use the injected AsyncSession within a single
PostgreSQL transaction owned by the caller. No Motor fallback for
assessment-owned operations.

XP is awarded through PostgresGamificationService.record_practice() which
writes to PostgreSQL gamification_profiles and xp_event_ledger. No MongoDB
fallback.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_session as AsyncSessionType
from app.repositories.assessments import (
    AssessmentAttemptRepository,
    AssessmentSectionRepository,
    ResponseRepository,
    CodingSubmissionRepository,
    ExecutionResultRepository,
    OASessionRepository,
    InterviewSessionRepository,
    CompanyAssessmentMetadataRepository,
    AssessmentDefinitionRepository,
    AssessmentVariantRepository,
)
from app.repositories.gamification import XPEventLedgerRepository, GamificationProfileRepository
from app.repositories.identity import UserRepository
from app.models.assessments import (
    AssessmentAttempt,
    AssessmentSection,
    CodingSubmission,
    OASession,
    InterviewSession,
    Response,
    ExecutionResult,
    CompanyAssessmentMetadata,
)
from app.models.identity import User
from app.services.postgres_learning import PostgresLearningService
from app.services.postgres_gamification import record_practice as pg_record_practice

logger = logging.getLogger(__name__)


class PostgresAssessmentService:
    """PostgreSQL-backed assessment service.

    All repository methods share the injected AsyncSession. The caller
    owns the transaction boundary (commit/rollback).
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.attempt_repo = AssessmentAttemptRepository(session)
        self.section_repo = AssessmentSectionRepository(session)
        self.response_repo = ResponseRepository(session)
        self.submission_repo = CodingSubmissionRepository(session)
        self.execution_repo = ExecutionResultRepository(session)
        self.oa_session_repo = OASessionRepository(session)
        self.interview_repo = InterviewSessionRepository(session)
        self.company_meta_repo = CompanyAssessmentMetadataRepository(session)
        self.definition_repo = AssessmentDefinitionRepository(session)
        self.variant_repo = AssessmentVariantRepository(session)
        self.xp_ledger_repo = XPEventLedgerRepository(session)
        self.gamification_repo = GamificationProfileRepository(session)
        self.user_repo = UserRepository(session)

    # ════════════════════════════════════════════════════════════════════════════
    # ASSESSMENT ATTEMPTS
    # ════════════════════════════════════════════════════════════════════════════

    async def create_assessment_attempt(
        self,
        user_id: UUID,
        assessment_id: UUID,
        variant_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> tuple[AssessmentAttempt, bool]:
        """Create a new assessment attempt.

        Returns (attempt, deduplicated). If deduplicated, the existing
        attempt is returned and no new record is created.
        """
        if idempotency_key:
            existing = await self.attempt_repo.get_by_user_and_assessment(user_id, assessment_id)
            for attempt in existing:
                if attempt.idempotency_key == idempotency_key:
                    logger.info("Assessment attempt idempotent replay: %s", user_id)
                    return attempt, True

        attempt = await self.attempt_repo.create({
            "user_id": user_id,
            "assessment_id": assessment_id,
            "variant_id": variant_id,
            "score": None,
            "status": "in_progress",
            "idempotency_key": idempotency_key,
        })
        return attempt, False

    async def get_assessment_attempt(
        self,
        attempt_id: UUID,
    ) -> Optional[AssessmentAttempt]:
        return await self.attempt_repo.get_by_id(attempt_id)

    async def get_user_attempts(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[AssessmentAttempt]:
        return await self.attempt_repo.get_by_user(user_id, limit=limit, offset=offset)

    async def complete_assessment(
        self,
        attempt_id: UUID,
        score: Optional[float],
        completed_at: Optional[datetime] = None,
    ) -> Optional[AssessmentAttempt]:
        """Mark an assessment attempt as completed. Cannot be completed twice."""
        attempt = await self.attempt_repo.get_by_id(attempt_id)
        if not attempt:
            return None
        if attempt.status == "completed":
            # Already completed — idempotent, return existing
            return attempt
        return await self.attempt_repo.complete(attempt_id, score, completed_at)

    # ════════════════════════════════════════════════════════════════════════════
    # SECTIONS AND RESPONSES
    # ════════════════════════════════════════════════════════════════════════════

    async def create_section(
        self,
        attempt_id: UUID,
        section_type: str,
    ) -> AssessmentSection:
        return await self.section_repo.create({
            "attempt_id": attempt_id,
            "section_type": section_type,
            "score": None,
        })

    async def list_sections(
        self,
        attempt_id: UUID,
    ) -> List[AssessmentSection]:
        return await self.section_repo.list_by_attempt(attempt_id)

    async def create_response(
        self,
        section_id: UUID,
        question_id: str,
        answer: Optional[str],
        is_correct: Optional[bool],
        score: Optional[float],
        time_taken_seconds: Optional[int] = None,
        idempotency_key: Optional[str] = None,
    ) -> tuple[Response, bool]:
        """Create a response. Returns (response, deduplicated).

        Idempotency: (section_id, question_id, idempotency_key) is
        database-enforced unique.
        """
        if idempotency_key:
            existing = await self.response_repo.list_by_section(section_id)
            for resp in existing:
                if resp.question_id == question_id and resp.idempotency_key == idempotency_key:
                    logger.info("Response idempotent replay: section=%s question=%s", section_id, question_id)
                    return resp, True

        response = await self.response_repo.create({
            "section_id": section_id,
            "question_id": question_id,
            "answer": answer,
            "is_correct": is_correct,
            "score": score,
            "time_taken_seconds": time_taken_seconds,
            "idempotency_key": idempotency_key,
        })
        return response, False

    async def list_responses_by_attempt(
        self,
        attempt_id: UUID,
    ) -> List[Response]:
        return await self.response_repo.list_by_attempt(attempt_id)

    # ════════════════════════════════════════════════════════════════════════════
    # CODING SUBMISSIONS
    # ════════════════════════════════════════════════════════════════════════════

    async def create_coding_submission(
        self,
        user_id: UUID,
        question_id: str,
        code: str,
        language: str,
        idempotency_key: Optional[str] = None,
    ) -> tuple[CodingSubmission, bool]:
        """Create a coding submission.

        Returns (submission, deduplicated). Execution is handled separately
        by the code execution engine; this only persists the submission.

        Security: execution_result is not populated here — only the code,
        language, and status. Protected test cases are never stored.
        """
        if idempotency_key:
            existing = await self.submission_repo.get_by_idempotency_key(user_id, idempotency_key)
            if existing:
                logger.info("Coding submission idempotent replay: %s / %s", user_id, question_id)
                return existing, True

        # Also check for duplicate (user_id, question_id) without idempotency key
        # as a best-effort guard against retries.
        recent = await self.submission_repo.list_by_user_and_question(user_id, question_id)
        if not idempotency_key and recent:
            # Allow retries without idempotency key, but log for visibility
            logger.warning(
                "Coding submission without idempotency key for %s / %s (prior submissions exist)",
                user_id, question_id,
            )

        submission = await self.submission_repo.create({
            "user_id": user_id,
            "question_id": question_id,
            "code": code,
            "language": language,
            "status": "pending",
            "execution_result": {},
            "idempotency_key": idempotency_key,
        })
        return submission, False

    async def get_coding_submission(
        self,
        submission_id: UUID,
    ) -> Optional[CodingSubmission]:
        return await self.submission_repo.get_by_id(submission_id)

    async def list_user_submissions(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[CodingSubmission]:
        return await self.submission_repo.list_by_user(user_id, limit=limit, offset=offset)

    async def update_submission_result(
        self,
        submission_id: UUID,
        status: str,
        execution_result: dict,
        score: Optional[float] = None,
    ) -> Optional[CodingSubmission]:
        """Update a coding submission with execution results.

        Security: execution_result must not contain protected test cases,
        expected answers, or hidden grading data. Only execution outcomes
        (passed, time, memory, status) are stored.
        """
        return await self.submission_repo.update_result(
            submission_id, status, execution_result, score
        )

    # ════════════════════════════════════════════════════════════════════════════
    # EXECUTION RESULTS
    # ════════════════════════════════════════════════════════════════════════════

    async def store_execution_results(
        self,
        submission_id: UUID,
        results: List[dict],
    ) -> List[ExecutionResult]:
        """Store individual test case execution results.

        Security: `expected` values for hidden test cases must not be
        passed here. Only visible-test-case expected values may be stored.
        """
        enriched = []
        for data in results:
            enriched.append({**data, "submission_id": submission_id})
        return await self.execution_repo.create_many(enriched)

    async def get_execution_results(
        self,
        submission_id: UUID,
    ) -> List[ExecutionResult]:
        return await self.execution_repo.list_by_submission(submission_id)

    # ════════════════════════════════════════════════════════════════════════════
    # ONLINE ASSESSMENT SESSIONS
    # ════════════════════════════════════════════════════════════════════════════

    async def create_oa_session(
        self,
        user_id: UUID,
        company: str,
        role: str,
        blueprint: dict,
        mode: str = "calm",
        integrity_enabled: bool = False,
        questions: Optional[List[dict]] = None,
        idempotency_key: Optional[str] = None,
    ) -> tuple[OASession, bool]:
        """Create an OA session.

        Questions JSONB stores question references (IDs, metadata) — NOT
        protected answer keys or hidden test cases.
        """
        if idempotency_key:
            existing = await self.oa_session_repo.list_by_user_and_company(user_id, company)
            for sess in existing:
                if sess.idempotency_key == idempotency_key:
                    logger.info("OA session idempotent replay: %s / %s", user_id, company)
                    return sess, True

        session = await self.oa_session_repo.create({
            "user_id": user_id,
            "company": company,
            "role": role,
            "blueprint": blueprint,
            "mode": mode,
            "integrity_enabled": integrity_enabled,
            "status": "in_progress",
            "questions": questions or [],
        })
        return session, False

    async def get_oa_session(
        self,
        session_id: UUID,
    ) -> Optional[OASession]:
        return await self.oa_session_repo.get_by_id(session_id)

    async def list_user_oa_sessions(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[OASession]:
        return await self.oa_session_repo.list_by_user(user_id, limit=limit, offset=offset)

    async def update_oa_session(
        self,
        session_id: UUID,
        updates: dict,
    ) -> Optional[OASession]:
        return await self.oa_session_repo.update(session_id, updates)

    async def complete_oa_session(
        self,
        session_id: UUID,
        completed_at: Optional[datetime] = None,
    ) -> Optional[OASession]:
        return await self.oa_session_repo.complete(session_id, completed_at)

    def oa_session_to_public_dict(
        self,
        session: OASession,
    ) -> dict:
        """Client-safe representation — excludes private integrity data."""
        return self.oa_session_repo.to_public_dict(session)

    def oa_session_to_private_dict(
        self,
        session: OASession,
    ) -> dict:
        """Full representation including integrity data — internal/admin only."""
        return self.oa_session_repo.to_private_dict(session)

    # ════════════════════════════════════════════════════════════════════════════
    # INTERVIEW SESSIONS
    # ════════════════════════════════════════════════════════════════════════════

    async def create_interview_session(
        self,
        user_id: UUID,
        interview_type: str,
        role: Optional[str] = None,
        company: Optional[str] = None,
        difficulty: str = "medium",
        idempotency_key: Optional[str] = None,
    ) -> tuple[InterviewSession, bool]:
        """Create an interview session.

        Access control: all queries filter by user_id. A user can never
        access another user's interview session.
        """
        if idempotency_key:
            existing = await self.interview_repo.get_in_progress_by_user(user_id)
            for sess in existing:
                if sess.idempotency_key == idempotency_key:
                    logger.info("Interview session idempotent replay: %s", user_id)
                    return sess, True

        session = await self.interview_repo.create({
            "user_id": user_id,
            "interview_type": interview_type,
            "company": company,
            "difficulty": difficulty,
            "status": "in_progress",
            "score": None,
            "idempotency_key": idempotency_key,
        })
        return session, False

    async def get_interview_session(
        self,
        session_id: UUID,
        user_id: UUID,
    ) -> Optional[InterviewSession]:
        """Get an interview session with ownership enforcement."""
        return await self.interview_repo.get_by_id_and_user(session_id, user_id)

    async def list_user_interviews(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[InterviewSession]:
        return await self.interview_repo.list_by_user(user_id, limit=limit, offset=offset)

    async def update_interview_session(
        self,
        session_id: UUID,
        user_id: UUID,
        updates: dict,
    ) -> Optional[InterviewSession]:
        """Update an interview session with ownership enforcement."""
        session = await self.interview_repo.get_by_id_and_user(session_id, user_id)
        if not session:
            return None
        return await self.interview_repo.update(session_id, updates)

    async def complete_interview_session(
        self,
        session_id: UUID,
        user_id: UUID,
        score: Optional[float],
        completed_at: Optional[datetime] = None,
    ) -> Optional[InterviewSession]:
        """Complete an interview session with ownership enforcement."""
        session = await self.interview_repo.get_by_id_and_user(session_id, user_id)
        if not session:
            return None
        if session.status == "completed":
            return session
        return await self.interview_repo.complete(session_id, score, completed_at)

    # ════════════════════════════════════════════════════════════════════════════
    # COMPANY ASSESSMENT METADATA
    # ════════════════════════════════════════════════════════════════════════════

    async def get_company_metadata(
        self,
        company: str,
        role: str,
        assessment_type: str,
    ) -> Optional[CompanyAssessmentMetadata]:
        return await self.company_meta_repo.get_by_company_role_type(company, role, assessment_type)

    async def create_company_metadata(
        self,
        company: str,
        role: str,
        assessment_type: str,
        assessment_metadata: dict,
    ) -> tuple[CompanyAssessmentMetadata, bool]:
        meta = await self.company_meta_repo.create({
            "company": company,
            "role": role,
            "assessment_type": assessment_type,
            "assessment_metadata": assessment_metadata,
        })
        return meta, False

    # ════════════════════════════════════════════════════════════════════════════
    # XP AWARD — database-enforced idempotency gate
    # ════════════════════════════════════════════════════════════════════════════

    async def award_xp(
        self,
        user_id: UUID,
        activity_type: str,
        score: float,
        idempotency_key: str,
        metadata: Optional[dict] = None,
        role: str = "sde",
    ) -> dict:
        """Award XP for an assessment completion with database-enforced idempotency.

        Design:
        1. Check xp_event_ledger (PostgreSQL) for the idempotency key.
           If present → deduplicated, skip XP award.
        2. Call record_practice() (MongoDB) — the single authoritative XP writer.
           This crosses the PostgreSQL↔MongoDB boundary and is NOT part of
           the PostgreSQL transaction.
        3. Insert into xp_event_ledger (PostgreSQL) with the idempotency key.
           If unique violation (concurrent request), treat as deduplicated.

        Returns:
            dict with 'deduplicated', 'xp_awarded', 'result'
        """
        # Step 1: Database-enforced idempotency gate (PostgreSQL)
        existing = await self.xp_ledger_repo.get_by_idempotency_key(user_id, idempotency_key)
        if existing:
            logger.info("XP idempotent replay: %s / %s", user_id, idempotency_key)
            return {
                "deduplicated": True,
                "xp_awarded": 0,
                "result": None,
            }

        # Step 2: Award XP via PostgreSQL gamification service (single writer,
        # database-enforced idempotency via xp_event_ledger)
        xp_result = None
        try:
            xp_result = await pg_record_practice(
                self.session,
                str(user_id),
                activity_type=activity_type,
                score=score,
                metadata=metadata or {},
                role=role,
                idempotency_key=idempotency_key,
            )
        except Exception as exc:
            logger.error("XP award via pg_record_practice failed for %s: %s", user_id, exc)
            return {
                "deduplicated": False,
                "xp_awarded": 0,
                "result": None,
                "error": str(exc),
            }

        # Step 3: pg_record_practice already recorded idempotency in the
        # xp_event_ledger. Return the result directly.
        xp_awarded = int((xp_result or {}).get("xp_gained", 0) or 0)
        return {
            "deduplicated": xp_result.get("deduplicated", False),
            "xp_awarded": xp_awarded,
            "result": xp_result,
        }

    # ════════════════════════════════════════════════════════════════════════════
    # LEARNING INTEGRATION — emit evidence without full fan-out
    # ════════════════════════════════════════════════════════════════════════════

    async def emit_assessment_evidence(
        self,
        user_id: UUID,
        activity_type: str,
        score: float,
        passed: bool,
        activity_data: dict,
    ) -> Optional[UUID]:
        """Emit learning evidence for an assessment result.

        Uses PostgresLearningService.emit_learning_event (lightweight, no
        mastery/SRS/gamification fan-out). The full mastery update is only
        triggered when verified performance justifies it — not automatically
        on assessment completion.
        """
        service = PostgresLearningService(self.session)
        return await service.emit_learning_event(
            user_id=user_id,
            activity_type=activity_type,
            score=score,
            passed=passed,
            activity_data=activity_data,
        )


async def postgres_assessment_service_stub(user_id: str) -> dict:
    """Stub for PostgresAssessmentService."""
    return {"user_id": user_id}
