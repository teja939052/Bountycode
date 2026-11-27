"""PostgreSQL Assessment domain integration tests — Phase 5D.

Tests cover all 21 required areas:
 1. Assessment creation
 2. Assessment attempt creation
 3. Section retrieval
 4. Response recording
 5. Submission and completion
 6. Duplicate submission prevention (idempotency)
 7. Score calculation
 8. Historical attempt retention
 9. Coding submission storage
 10. Execution result storage
 11. OA session creation and update
 12. Interview session creation and update
 13. Company assessment metadata
 14. Content-version preservation
 15. User ownership isolation
 16. Concurrent submission handling
 17. Transaction commit
 18. Transaction rollback
 19. Learning evidence integration
 20. XP idempotency
 21. Existing API compatibility

Uses local Supabase PostgreSQL (postgresql+asyncpg://postgres:postgres@127.0.0.1:54322/postgres).

All tests write to real PostgreSQL tables — no mocked repositories.
"""

import asyncio
import os
import pytest
from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select

from app.models import Base
from app.models.identity import User
from app.models.content import AssessmentDefinition, AssessmentVariant
from app.models.assessments import (
    AssessmentAttempt, AssessmentSection, Response,
    CodingSubmission, ExecutionResult, OASession,
    InterviewSession, CompanyAssessmentMetadata,
)
from app.models.gamification import GamificationProfile, XPEventLedger
from app.models.learning import Skill, LearningAttempt, LearningEvidence
from app.repositories.assessments import (
    AssessmentAttemptRepository, AssessmentSectionRepository, ResponseRepository,
    CodingSubmissionRepository, ExecutionResultRepository, OASessionRepository,
    InterviewSessionRepository, CompanyAssessmentMetadataRepository,
    AssessmentDefinitionRepository, AssessmentVariantRepository,
)
from app.repositories.gamification import XPEventLedgerRepository
from app.services.postgres_assessments import PostgresAssessmentService
from app.services.postgres_learning import PostgresLearningService

DATABASE_URL = os.environ.get(
    'SUPABASE_DB_URL',
    'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres',
)


@pytest.fixture
async def session():
    """Create an async SQLAlchemy session for testing."""
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def test_user(session):
    """Create a test user."""
    user = User(
        email=f'test_assess_{uuid4().hex[:8]}@test.dev',
        password_hash='$2b$12$testhashplaceholder',
        name='Test User',
        plan='free',
    )
    session.add(user)
    await session.flush()
    return user


@pytest.fixture
async def test_skill(session):
    """Create a test skill."""
    skill = Skill(
        name=f'test_assess_skill_{uuid4().hex[:8]}',
        topic='arrays',
        sub_topic=None,
        difficulty='medium',
        prerequisites=[],
        content_version='v1.0',
        is_active=True,
    )
    session.add(skill)
    await session.flush()
    return skill


@pytest.fixture
async def test_definition(session):
    """Create a test assessment definition."""
    definition = AssessmentDefinition(
        name=f'test_def_{uuid4().hex[:8]}',
        assessment_type='coding',
        company_tags=['google'],
        topic_tags=['arrays'],
        difficulty='medium',
        time_limit_minutes=45,
        question_count=2,
        is_active=True,
    )
    session.add(definition)
    await session.flush()
    return definition


@pytest.fixture
async def test_variant(session, test_definition):
    """Create a test assessment variant."""
    variant = AssessmentVariant(
        definition_id=test_definition.id,
        variant_id=f'var_{uuid4().hex[:8]}',
        question_ids=['q1', 'q2', 'q3'],
        content_snapshot={'version': 'v1.0', 'hash': 'abc123'},
    )
    session.add(variant)
    await session.flush()
    return variant


@pytest.fixture
async def assessment_service(session):
    """Create a PostgresAssessmentService instance."""
    return PostgresAssessmentService(session)


@pytest.fixture
async def learning_service(session):
    """Create a PostgresLearningService instance."""
    return PostgresLearningService(session)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1: Assessment creation (definitions and variants)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_assessment_definition_creation(session, assessment_service):
    """Test assessment definition creation and retrieval."""
    def_repo = AssessmentDefinitionRepository(session)
    definition = await def_repo.create({
        "name": "TCS Ninja Aptitude",
        "assessment_type": "aptitude",
        "company_tags": ["TCS"],
        "topic_tags": ["quant", "reasoning"],
        "difficulty": "medium",
        "time_limit_minutes": 60,
        "question_count": 20,
        "is_active": True,
    })
    assert definition.id is not None
    assert definition.name == "TCS Ninja Aptitude"
    assert definition.assessment_type == "aptitude"

    retrieved = await def_repo.get_by_id(definition.id)
    assert retrieved is not None
    assert retrieved.id == definition.id


@pytest.mark.asyncio
async def test_assessment_variant_creation(session, test_definition):
    """Test assessment variant creation."""
    var_repo = AssessmentVariantRepository(session)
    variant = await var_repo.create({
        "definition_id": test_definition.id,
        "variant_id": f'var_{uuid4().hex[:8]}',
        "question_ids": ["q1", "q2"],
        "content_snapshot": {"version": "v1.0"},
    })
    assert variant.id is not None
    assert variant.variant_id is not None

    retrieved = await var_repo.get_by_variant_id(variant.variant_id)
    assert retrieved is not None
    assert retrieved.id == variant.id


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Assessment attempt creation
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_assessment_attempt_creation(session, test_user, test_definition, assessment_service):
    """Test assessment attempt creation."""
    attempt, deduped = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        variant_id="var_001",
        idempotency_key=f'attempt_{uuid4().hex[:8]}',
    )
    assert attempt.id is not None
    assert attempt.user_id == test_user.id
    assert attempt.assessment_id == test_definition.id
    assert attempt.status == "in_progress"
    assert deduped is False


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: Section retrieval
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_section_creation_and_retrieval(session, test_user, test_definition, assessment_service):
    """Test section creation within an attempt and retrieval."""
    attempt, _ = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=f'sect_{uuid4().hex[:8]}',
    )

    section = await assessment_service.create_section(attempt.id, "coding")
    assert section.id is not None
    assert section.attempt_id == attempt.id
    assert section.section_type == "coding"

    sections = await assessment_service.list_sections(attempt.id)
    assert len(sections) >= 1
    assert sections[0].id == section.id


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4: Response recording
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_response_recording(session, test_user, test_definition, assessment_service):
    """Test response recording within a section."""
    attempt, _ = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=f'resp_{uuid4().hex[:8]}',
    )
    section = await assessment_service.create_section(attempt.id, "aptitude")

    response, deduped = await assessment_service.create_response(
        section_id=section.id,
        question_id="q_001",
        answer="42",
        is_correct=True,
        score=10.0,
        time_taken_seconds=30,
        idempotency_key=f'resp_key_{uuid4().hex[:8]}',
    )
    assert response.id is not None
    assert response.section_id == section.id
    assert response.question_id == "q_001"
    assert response.is_correct is True
    assert response.score == 10
    assert deduped is False

    responses = await assessment_service.list_responses_by_attempt(attempt.id)
    assert len(responses) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5: Submission and completion
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_assessment_submission_and_completion(session, test_user, test_definition, assessment_service):
    """Test assessment attempt submission and completion (cannot complete twice)."""
    attempt, _ = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=f'complete_{uuid4().hex[:8]}',
    )

    # Complete the assessment
    completed = await assessment_service.complete_assessment(
        attempt.id, score=85.0,
    )
    assert completed is not None
    assert completed.status == "completed"
    assert completed.score == 85

    # Completing again should be idempotent — returns existing, no change
    completed_again = await assessment_service.complete_assessment(
        attempt.id, score=99.0,
    )
    assert completed_again is not None
    assert completed_again.score == 85  # Score should not change


# ══════════════════════════════════════════════════════════════════════════════
# TEST 6: Duplicate submission prevention (idempotency)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_duplicate_attempt_prevention(session, test_user, test_definition, assessment_service):
    """Test idempotency prevents duplicate assessment attempts."""
    idem_key = f'idem_attempt_{uuid4().hex[:8]}'

    attempt1, deduped1 = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=idem_key,
    )
    assert deduped1 is False

    attempt2, deduped2 = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=idem_key,
    )
    assert deduped2 is True
    assert attempt2.id == attempt1.id  # Same attempt returned


@pytest.mark.asyncio
async def test_duplicate_response_prevention(session, test_user, test_definition, assessment_service):
    """Test idempotency prevents duplicate responses."""
    attempt, _ = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=f'dup_resp_{uuid4().hex[:8]}',
    )
    section = await assessment_service.create_section(attempt.id, "coding")
    idem_key = f'idem_resp_{uuid4().hex[:8]}'

    resp1, _ = await assessment_service.create_response(
        section_id=section.id,
        question_id="q_dup",
        answer="answer1",
        is_correct=True,
        score=10.0,
        idempotency_key=idem_key,
    )
    resp2, deduped = await assessment_service.create_response(
        section_id=section.id,
        question_id="q_dup",
        answer="answer2",
        is_correct=False,
        score=0.0,
        idempotency_key=idem_key,
    )
    assert deduped is True
    assert resp2.id == resp1.id


@pytest.mark.asyncio
async def test_duplicate_coding_submission_prevention(session, test_user, assessment_service):
    """Test idempotency prevents duplicate coding submissions."""
    idem_key = f'idem_code_{uuid4().hex[:8]}'

    sub1, _ = await assessment_service.create_coding_submission(
        user_id=test_user.id,
        question_id="q_code_1",
        code="print('hello')",
        language="python",
        idempotency_key=idem_key,
    )
    assert sub1.id is not None

    sub2, deduped = await assessment_service.create_coding_submission(
        user_id=test_user.id,
        question_id="q_code_1",
        code="print('different')",
        language="python",
        idempotency_key=idem_key,
    )
    assert deduped is True
    assert sub2.id == sub1.id


# ══════════════════════════════════════════════════════════════════════════════
# TEST 7: Score calculation
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_score_calculation(session, test_user, test_definition, assessment_service):
    """Test score calculation from responses."""
    attempt, _ = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=f'score_{uuid4().hex[:8]}',
    )
    section = await assessment_service.create_section(attempt.id, "aptitude")

    # Record multiple responses with scores
    await assessment_service.create_response(
        section_id=section.id, question_id="q1", answer="a", is_correct=True,
        score=10.0, idempotency_key=f's1_{uuid4().hex[:8]}',
    )
    await assessment_service.create_response(
        section_id=section.id, question_id="q2", answer="b", is_correct=True,
        score=10.0, idempotency_key=f's2_{uuid4().hex[:8]}',
    )
    await assessment_service.create_response(
        section_id=section.id, question_id="q3", answer="c", is_correct=False,
        score=0.0, idempotency_key=f's3_{uuid4().hex[:8]}',
    )

    responses = await assessment_service.list_responses_by_attempt(attempt.id)
    total_score = sum(r.score or 0 for r in responses)
    assert total_score == 20
    assert len(responses) == 3


# ══════════════════════════════════════════════════════════════════════════════
# TEST 8: Historical attempt retention
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_historical_attempt_retention(session, test_user, test_definition, assessment_service):
    """Test that historical attempts are preserved (not overwritten)."""
    attempts = []
    for i in range(3):
        attempt, _ = await assessment_service.create_assessment_attempt(
            user_id=test_user.id,
            assessment_id=test_definition.id,
            idempotency_key=f'hist_{i}_{uuid4().hex[:8]}',
        )
        await assessment_service.complete_assessment(attempt.id, score=float(i * 30))
        attempts.append(attempt)

    # Retrieve all attempts for this user+assessment
    all_attempts = await assessment_service.get_user_attempts(test_user.id, limit=50)
    matching = [a for a in all_attempts if a.assessment_id == test_definition.id]
    assert len(matching) >= 3

    # All completed attempts should have their scores preserved
    completed = [a for a in matching if a.status == "completed"]
    assert len(completed) >= 3


# ══════════════════════════════════════════════════════════════════════════════
# TEST 9: Coding submission storage
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_coding_submission_storage(session, test_user, assessment_service):
    """Test coding submission storage with user ownership."""
    submission, _ = await assessment_service.create_coding_submission(
        user_id=test_user.id,
        question_id="q_code_storage",
        code="def solve():\n    return 42",
        language="python",
        idempotency_key=f'code_store_{uuid4().hex[:8]}',
    )
    assert submission.id is not None
    assert submission.user_id == test_user.id
    assert submission.question_id == "q_code_storage"
    assert submission.language == "python"
    assert submission.status == "pending"
    assert submission.code == "def solve():\n    return 42"
    assert submission.execution_result == {}  # Not yet executed


# ══════════════════════════════════════════════════════════════════════════════
# TEST 10: Execution result storage
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_execution_result_storage(session, test_user, assessment_service):
    """Test execution result storage for coding submissions."""
    submission, _ = await assessment_service.create_coding_submission(
        user_id=test_user.id,
        question_id="q_exec",
        code="print(1)",
        language="python",
        idempotency_key=f'exec_{uuid4().hex[:8]}',
    )

    # Store execution results (visible test cases only — no hidden expected values)
    results = await assessment_service.store_execution_results(submission.id, [
        {
            "test_case_id": "tc_visible_1",
            "passed": True,
            "expected": "1\n",
            "actual": "1\n",
            "execution_time_ms": 50,
        },
        {
            "test_case_id": "tc_visible_2",
            "passed": False,
            "expected": "2\n",
            "actual": "1\n",
            "execution_time_ms": 60,
        },
    ])
    assert len(results) == 2
    assert results[0].passed is True
    assert results[1].passed is False

    # Verify retrieval
    stored = await assessment_service.get_execution_results(submission.id)
    assert len(stored) == 2

    passed_count = await assessment_service.execution_repo.passed_count_by_submission(submission.id)
    total_count = await assessment_service.execution_repo.total_count_by_submission(submission.id)
    assert passed_count == 1
    assert total_count == 2

    # Update submission with execution outcome
    updated = await assessment_service.update_submission_result(
        submission.id, "wrong_answer", {"passed": 1, "total": 2}, score=50.0
    )
    assert updated is not None
    assert updated.status == "wrong_answer"
    assert updated.score == 50


# ══════════════════════════════════════════════════════════════════════════════
# TEST 11: OA session creation and update
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_oa_session_creation_and_update(session, test_user, assessment_service):
    """Test OA session creation and update."""
    session_obj, _ = await assessment_service.create_oa_session(
        user_id=test_user.id,
        company="Google",
        role="SDE",
        blueprint={"sections": ["coding", "aptitude"], "weights": {"coding": 0.7}},
        mode="timed",
        integrity_enabled=True,
        questions=[{"id": "q1", "type": "coding"}],
        idempotency_key=f'oa_{uuid4().hex[:8]}',
    )
    assert session_obj.id is not None
    assert session_obj.user_id == test_user.id
    assert session_obj.company == "Google"
    assert session_obj.status == "in_progress"

    # Public dict excludes private integrity data
    public = assessment_service.oa_session_to_public_dict(session_obj)
    assert public["company"] == "Google"
    assert "integrity_enabled" not in public  # Private field excluded

    # Private dict includes integrity data
    private = assessment_service.oa_session_to_private_dict(session_obj)
    assert private["integrity_enabled"] is True

    # Update the session
    updated = await assessment_service.update_oa_session(
        session_obj.id, {"status": "completed"}
    )
    assert updated is not None
    assert updated.status == "completed"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 12: Interview session creation and update
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_interview_session_creation_and_update(session, test_user, assessment_service):
    """Test interview session creation, update, and ownership enforcement."""
    interview, _ = await assessment_service.create_interview_session(
        user_id=test_user.id,
        interview_type="behavioral",
        company="Amazon",
        role="SDE",
        difficulty="medium",
        idempotency_key=f'interview_{uuid4().hex[:8]}',
    )
    assert interview.id is not None
    assert interview.user_id == test_user.id
    assert interview.interview_type == "behavioral"
    assert interview.status == "in_progress"

    # Get with ownership enforcement
    retrieved = await assessment_service.get_interview_session(interview.id, test_user.id)
    assert retrieved is not None
    assert retrieved.id == interview.id

    # Another user cannot access this interview
    other_user = User(
        email=f'other_{uuid4().hex[:8]}@test.dev',
        password_hash='$2b$12$hash',
        name='Other User',
    )
    session.add(other_user)
    await session.flush()
    unretrieved = await assessment_service.get_interview_session(interview.id, other_user.id)
    assert unretrieved is None

    # Complete the interview
    completed = await assessment_service.complete_interview_session(
        interview.id, test_user.id, score=8.5,
    )
    assert completed is not None
    assert completed.status == "completed"
    assert completed.score == 8.5


# ══════════════════════════════════════════════════════════════════════════════
# TEST 13: Company assessment metadata
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_company_assessment_metadata(session, assessment_service):
    """Test company assessment metadata creation and retrieval."""
    meta, _ = await assessment_service.create_company_metadata(
        company="TCS",
        role="SDE",
        assessment_type="aptitude",
        assessment_metadata={
            "source": "pattern-relevant",
            "verification_date": "2026-11-01",
            "confidence": 0.8,
        },
    )
    assert meta.id is not None
    assert meta.company == "TCS"
    assert meta.role == "SDE"

    retrieved = await assessment_service.get_company_metadata("TCS", "SDE", "aptitude")
    assert retrieved is not None
    assert retrieved.id == meta.id

    # Different company/type should not match
    not_found = await assessment_service.get_company_metadata("TCS", "SDE", "coding")
    assert not_found is None


# ══════════════════════════════════════════════════════════════════════════════
# TEST 14: Content-version preservation
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_content_version_preservation(session, test_user, test_definition, test_variant, assessment_service):
    """Test that assessment content version is preserved with the attempt."""
    attempt, _ = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        variant_id=test_variant.variant_id,
        idempotency_key=f'ver_{uuid4().hex[:8]}',
    )
    assert attempt.variant_id == test_variant.variant_id

    # Retrieve the variant to verify content snapshot is preserved
    variant = await assessment_service.variant_repo.get_by_id(test_variant.id)
    assert variant is not None
    assert variant.content_snapshot.get("version") == "v1.0"
    assert variant.question_ids == ["q1", "q2", "q3"]


# ══════════════════════════════════════════════════════════════════════════════
# TEST 15: User ownership isolation
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_user_ownership_isolation(session, test_definition, assessment_service):
    """Test that user A cannot access user B's assessment data."""
    user1 = User(
        email=f'iso1_{uuid4().hex[:8]}@test.dev',
        password_hash='$2b$12$hash',
        name='User 1',
    )
    user2 = User(
        email=f'iso2_{uuid4().hex[:8]}@test.dev',
        password_hash='$2b$12$hash',
        name='User 2',
    )
    session.add_all([user1, user2])
    await session.flush()

    # User1 creates an attempt
    attempt1, _ = await assessment_service.create_assessment_attempt(
        user_id=user1.id,
        assessment_id=test_definition.id,
        idempotency_key=f'iso_{uuid4().hex[:8]}',
    )

    # User2 creates an attempt
    attempt2, _ = await assessment_service.create_assessment_attempt(
        user_id=user2.id,
        assessment_id=test_definition.id,
        idempotency_key=f'iso_{uuid4().hex[:8]}',
    )

    # User1 should only see their own attempts
    user1_attempts = await assessment_service.get_user_attempts(user1.id, limit=10)
    user1_ids = [a.id for a in user1_attempts]
    assert attempt1.id in user1_ids
    assert attempt2.id not in user1_ids

    # User2 should only see their own attempts
    user2_attempts = await assessment_service.get_user_attempts(user2.id, limit=10)
    user2_ids = [a.id for a in user2_attempts]
    assert attempt2.id in user2_ids
    assert attempt1.id not in user2_ids


# ══════════════════════════════════════════════════════════════════════════════
# TEST 16: Concurrent submission handling (idempotency under retry)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_concurrent_submission_handling(session, test_user, assessment_service):
    """Test that concurrent submissions with same idempotency key result in one record."""
    idem_key = f'concurrent_{uuid4().hex[:8]}'

    # Simulate concurrent submissions (sequential in test, same key)
    sub1, _ = await assessment_service.create_coding_submission(
        user_id=test_user.id,
        question_id="q_concurrent",
        code="print(1)",
        language="python",
        idempotency_key=idem_key,
    )
    sub2, deduped = await assessment_service.create_coding_submission(
        user_id=test_user.id,
        question_id="q_concurrent",
        code="print(2)",
        language="python",
        idempotency_key=idem_key,
    )
    assert deduped is True
    assert sub2.id == sub1.id

    # Verify only one submission exists
    submissions = await assessment_service.submission_repo.list_by_user_and_question(
        test_user.id, "q_concurrent"
    )
    # There may be other submissions without idempotency key, but only one with this key
    keyed = [s for s in submissions if s.idempotency_key == idem_key]
    assert len(keyed) == 1


# ══════════════════════════════════════════════════════════════════════════════
# TEST 17: Transaction commit
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_transaction_commit():
    """Test that committed transaction persists all assessment writes."""
    from app.database import get_engine
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as tx_session:
        from app.models.identity import User
        from app.models.content import AssessmentDefinition

        user = User(
            email=f'tx_commit_{uuid4().hex[:8]}@test.dev',
            password_hash='$2b$12$hash',
            name='Tx Commit User',
        )
        tx_session.add(user)
        await tx_session.flush()

        definition = AssessmentDefinition(
            name=f'tx_def_{uuid4().hex[:8]}',
            assessment_type='coding',
            company_tags=[],
            topic_tags=[],
            difficulty='medium',
            time_limit_minutes=45,
            question_count=2,
            is_active=True,
        )
        tx_session.add(definition)
        await tx_session.flush()

        async with tx_session.begin_nested():
            service = PostgresAssessmentService(tx_session)
            attempt, _ = await service.create_assessment_attempt(
                user_id=user.id,
                assessment_id=definition.id,
                idempotency_key=f'tx_commit_{uuid4().hex[:8]}',
            )
            section = await service.create_section(attempt.id, "coding")
            await service.create_response(
                section_id=section.id,
                question_id="q_tx",
                answer="answer",
                is_correct=True,
                score=10.0,
                idempotency_key=f'tx_resp_{uuid4().hex[:8]}',
            )
        # Nested transaction committed
        await tx_session.commit()

    # Verify data persists using a new session
    engine2 = create_async_engine(DATABASE_URL)
    async_session2 = sessionmaker(engine2, class_=AsyncSession, expire_on_commit=False)
    async with async_session2() as verify_session:
        result = await verify_session.execute(
            select(AssessmentAttempt).where(AssessmentAttempt.user_id == user.id)
        )
        retrieved = result.scalar_one_or_none()
        assert retrieved is not None
        assert retrieved.status == "in_progress"
    await engine2.dispose()
    await engine.dispose()


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 18: Transaction rollback
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_transaction_rollback():
    """Test that rolled-back transaction discards all assessment writes."""
    from app.database import get_engine
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    attempt_id = None
    async with async_session() as tx_session:
        from app.models.identity import User
        from app.models.content import AssessmentDefinition

        user = User(
            email=f'tx_rollback_{uuid4().hex[:8]}@test.dev',
            password_hash='$2b$12$hash',
            name='Tx Rollback User',
        )
        tx_session.add(user)
        await tx_session.flush()

        definition = AssessmentDefinition(
            name=f'tx_def_2_{uuid4().hex[:8]}',
            assessment_type='coding',
            company_tags=[],
            topic_tags=[],
            difficulty='medium',
            time_limit_minutes=45,
            question_count=2,
            is_active=True,
        )
        tx_session.add(definition)
        await tx_session.flush()

        service = PostgresAssessmentService(tx_session)
        try:
            async with tx_session.begin_nested():
                attempt, _ = await service.create_assessment_attempt(
                    user_id=user.id,
                    assessment_id=definition.id,
                    idempotency_key=f'tx_rollback_{uuid4().hex[:8]}',
                )
                attempt_id = attempt.id
                await service.create_section(attempt.id, "coding")
                # Force an error → nested transaction rolled back
                raise RuntimeError("Forced rollback")
        except RuntimeError:
            pass
    # Session closed → outer transaction rolled back

    # Verify data does NOT persist
    engine2 = create_async_engine(DATABASE_URL)
    async_session2 = sessionmaker(engine2, class_=AsyncSession, expire_on_commit=False)
    async with async_session2() as verify_session:
        if attempt_id is not None:
            result = await verify_session.execute(
                select(AssessmentAttempt).where(AssessmentAttempt.id == attempt_id)
            )
            retrieved = result.scalar_one_or_none()
            assert retrieved is None
    await engine2.dispose()
    await engine.dispose()


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 18: Transaction rollback
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_transaction_rollback():
    """Test that rolled-back transaction discards all assessment writes."""
    from app.database import get_engine
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    attempt_id = None
    async with async_session() as tx_session:
        from app.models.identity import User
        from app.models.content import AssessmentDefinition

        user = User(
            email=f'tx_rollback_{uuid4().hex[:8]}@test.dev',
            password_hash='$2b$12$hash',
            name='Tx Rollback User',
        )
        tx_session.add(user)
        await tx_session.flush()

        definition = AssessmentDefinition(
            name=f'tx_def_2_{uuid4().hex[:8]}',
            assessment_type='coding',
            company_tags=[],
            topic_tags=[],
            difficulty='medium',
            time_limit_minutes=45,
            question_count=2,
            is_active=True,
        )
        tx_session.add(definition)
        await tx_session.flush()

        service = PostgresAssessmentService(tx_session)
        try:
            attempt, _ = await service.create_assessment_attempt(
                user_id=user.id,
                assessment_id=definition.id,
                idempotency_key=f'tx_rollback_{uuid4().hex[:8]}',
            )
            attempt_id = attempt.id
            await service.create_section(attempt.id, "coding")
            # Force an error
            raise RuntimeError("Forced rollback")
        except RuntimeError:
            pass
    # Session closed → transaction rolled back

    # Verify data does NOT persist
    engine2 = create_async_engine(DATABASE_URL)
    async_session2 = sessionmaker(engine2, class_=AsyncSession, expire_on_commit=False)
    async with async_session2() as verify_session:
        if attempt_id is not None:
            result = await verify_session.execute(
                select(AssessmentAttempt).where(AssessmentAttempt.id == attempt_id)
            )
            retrieved = result.scalar_one_or_none()
            assert retrieved is None
    await engine2.dispose()
    await engine.dispose()


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 19: Learning evidence integration
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_learning_evidence_integration(
    session, test_user, test_skill, assessment_service, learning_service
):
    """Test that assessment results emit learning evidence."""
    # Emit assessment evidence via the assessment service
    event_id = await assessment_service.emit_assessment_evidence(
        user_id=test_user.id,
        activity_type="assessment_complete",
        score=7.5,
        passed=True,
        activity_data={
            "skill_id": str(test_skill.id),
            "question_id": "q_assessment_1",
            "assessment_id": str(uuid4()),
            "time_spent_seconds": 120,
            "hints_used": 0,
            "attempt_number": 1,
            "metadata": {"source": "assessment"},
        },
    )
    assert event_id is not None

    # Verify learning attempt was recorded
    attempt = await learning_service.attempt_repo.get_by_id(event_id)
    assert attempt is not None
    assert attempt.activity_type == "assessment_complete"
    assert attempt.passed is True
    assert attempt.evidence_type == "independent"  # No hints used

    # Verify evidence was recorded
    evidence_list = await learning_service.evidence_repo.get_by_user(test_user.id)
    assert len(evidence_list) >= 1
    assert evidence_list[0].evidence_type == "independent"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 20: XP idempotency
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_xp_idempotency(session, test_user, assessment_service):
    """Test that XP is not double-awarded for the same assessment completion.

    Pre-inserts an xp_event_ledger entry with the idempotency key to test the
    database-enforced idempotency gate independently of record_practice (which
    requires MongoDB and may be unavailable in the test environment).
    """
    idem_key = f'xp_assess_{uuid4().hex[:8]}'

    # Create a gamification profile first (FK requirement for xp_event_ledger)
    from app.models.gamification import GamificationProfile, XPEventLedger
    profile = GamificationProfile(
        user_id=test_user.id,
        xp=0,
        level=1,
    )
    session.add(profile)
    await session.flush()

    # Pre-insert a ledger entry with the idempotency key to simulate a prior
    # successful XP award. This tests the DB idempotency gate directly.
    ledger_entry = XPEventLedger(
        user_id=test_user.id,
        activity_type="assessment",
        score=8,
        xp_awarded=50,
        event_metadata={"idempotency_key": idem_key},
        reward_policy_version="v1",
    )
    session.add(ledger_entry)
    await session.flush()

    # Calling award_xp with the same idempotency key should be deduplicated
    result = await assessment_service.award_xp(
        user_id=test_user.id,
        activity_type="assessment",
        score=8.0,
        idempotency_key=idem_key,
        metadata={"assessment_id": "test"},
        role="sde",
    )
    assert result["deduplicated"] is True
    assert result["xp_awarded"] == 0


# ══════════════════════════════════════════════════════════════════════════════
# TEST 21: Existing API compatibility (service method signatures)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_api_compatibility_service_methods(session, test_user, test_definition, assessment_service):
    """Test that service methods return expected shapes for API compatibility."""
    # Create attempt
    attempt, _ = await assessment_service.create_assessment_attempt(
        user_id=test_user.id,
        assessment_id=test_definition.id,
        idempotency_key=f'api_{uuid4().hex[:8]}',
    )
    assert hasattr(attempt, 'id')
    assert hasattr(attempt, 'user_id')
    assert hasattr(attempt, 'assessment_id')
    assert hasattr(attempt, 'status')
    assert hasattr(attempt, 'score')
    assert hasattr(attempt, 'started_at')

    # Create section
    section = await assessment_service.create_section(attempt.id, "coding")
    assert hasattr(section, 'id')
    assert hasattr(section, 'attempt_id')
    assert hasattr(section, 'section_type')

    # Create response
    response, _ = await assessment_service.create_response(
        section_id=section.id,
        question_id="q_api",
        answer="answer",
        is_correct=True,
        score=10.0,
        time_taken_seconds=30,
        idempotency_key=f'api_resp_{uuid4().hex[:8]}',
    )
    assert hasattr(response, 'id')
    assert hasattr(response, 'question_id')

    # Create coding submission
    submission, _ = await assessment_service.create_coding_submission(
        user_id=test_user.id,
        question_id="q_api_code",
        code="print(1)",
        language="python",
        idempotency_key=f'api_code_{uuid4().hex[:8]}',
    )
    assert hasattr(submission, 'id')
    assert hasattr(submission, 'code')
    assert hasattr(submission, 'language')
    assert hasattr(submission, 'status')

    # Create OA session
    oa_session, _ = await assessment_service.create_oa_session(
        user_id=test_user.id,
        company="TestCo",
        role="SDE",
        blueprint={"sections": ["coding"]},
        idempotency_key=f'api_oa_{uuid4().hex[:8]}',
    )
    assert hasattr(oa_session, 'id')
    assert hasattr(oa_session, 'company')
    assert hasattr(oa_session, 'status')

    # Public dict should not expose integrity data
    public = assessment_service.oa_session_to_public_dict(oa_session)
    assert "integrity_enabled" not in public

    # Create interview session
    interview, _ = await assessment_service.create_interview_session(
        user_id=test_user.id,
        interview_type="technical",
        company="TestCo",
        idempotency_key=f'api_int_{uuid4().hex[:8]}',
    )
    assert hasattr(interview, 'id')
    assert hasattr(interview, 'interview_type')
    assert hasattr(interview, 'status')

    # Company metadata
    meta, _ = await assessment_service.create_company_metadata(
        company="TestCo", role="SDE", assessment_type="coding",
        assessment_metadata={"source": "pattern-relevant"},
    )
    assert hasattr(meta, 'id')
    assert hasattr(meta, 'company')
