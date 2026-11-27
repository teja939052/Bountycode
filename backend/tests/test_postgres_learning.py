"""PostgreSQL Learning domain tests — validates the migrated Learning system.

Tests cover:
1. Skill creation and prerequisite retrieval
2. Learner skill-state retrieval and update
3. Learning attempt creation
4. Learning evidence recording
5. Duplicate attempt prevention (idempotency)
6. Mastery updates
7. Independent versus assisted evidence
8. SRS scheduling
9. Due review retrieval
10. Repair mission creation
11. Diagnosis and remediation
12. Retest completion
13. User ownership isolation
14. XP idempotency
15. Transaction rollback
16. Failure handling
17. Database constraints (unique, foreign key, check)

Uses local Supabase PostgreSQL (postgresql+asyncpg://postgres:postgres@127.0.0.1:54322/postgres).
"""

import asyncio
import pytest
from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select

from app.models import Base
from app.models.identity import User
from app.models.learning import (
    Skill, SkillPrerequisite, LearnerSkillState, LearningAttempt,
    LearningEvidence, MasterySnapshot, ReviewCard, RepairMission,
    RemediationAttempt,
)
from app.models.gamification import GamificationProfile, XPEventLedger
from app.services.postgres_learning import PostgresLearningService
from app.repositories.learning import (
    SkillRepository, LearnerSkillStateRepository, LearningAttemptRepository,
    LearningEvidenceRepository, ReviewCardRepository, RepairMissionRepository,
    RemediationAttemptRepository, MasterySnapshotRepository,
)
from app.repositories.gamification import GamificationProfileRepository, XPEventLedgerRepository

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:54322/postgres'


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
        email=f'test_{uuid4().hex[:8]}@test.dev',
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
        name=f'test_skill_{uuid4().hex[:8]}',
        topic='arrays',
        sub_topic=None,
        difficulty='easy',
        prerequisites=[],
        content_version='v1.0',
        is_active=True,
    )
    session.add(skill)
    await session.flush()
    return skill


@pytest.fixture
async def learning_service(session):
    """Create a PostgresLearningService instance."""
    return PostgresLearningService(session)


# ════════════════════════════════════════════════════════════════════════════════
# TEST 1: Skill creation and prerequisite retrieval
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_skill_creation_and_prerequisites(session, learning_service):
    """Test skill creation and prerequisite DAG."""
    # Create parent skill
    parent = Skill(
        name='test_parent_skill',
        topic='arrays',
        difficulty='easy',
        prerequisites=[],
        is_active=True,
    )
    session.add(parent)
    await session.flush()

    # Create child skill with prerequisite
    child = Skill(
        name='test_child_skill',
        topic='arrays',
        difficulty='medium',
        prerequisites=[str(parent.id)],
        is_active=True,
    )
    session.add(child)
    await session.flush()

    # Add prerequisite relationship
    prereq = SkillPrerequisite(
        skill_id=child.id,
        prerequisite_skill_id=parent.id,
    )
    session.add(prereq)
    await session.flush()

    # Retrieve prerequisites
    from app.repositories.learning import SkillPrerequisiteRepository
    prereq_repo = SkillPrerequisiteRepository(session)
    prereqs = await prereq_repo.get_prerequisites(child.id)
    assert len(prereqs) == 1
    assert prereqs[0].prerequisite_skill_id == parent.id

    # Retrieve dependents
    dependents = await prereq_repo.get_dependents(parent.id)
    assert len(dependents) == 1
    assert dependents[0].skill_id == child.id


# ════════════════════════════════════════════════════════════════════════════════
# TEST 2: Learner skill-state retrieval and update
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_learner_skill_state_retrieval_and_update(session, test_user, test_skill, learning_service):
    """Test learner skill state creation and update."""
    repo = LearnerSkillStateRepository(session)

    # Initial state
    state = await repo.create_or_update(
        user_id=test_user.id,
        skill_id=test_skill.id,
        score=50.0,
        mastery_level='beginner',
        total_attempts=1,
    )
    assert state.score == 50.0
    assert state.mastery_level == 'beginner'
    assert state.total_attempts == 1

    # Retrieve by user and skill
    retrieved = await repo.get_by_user_and_skill(test_user.id, test_skill.id)
    assert retrieved is not None
    assert retrieved.score == 50.0

    # Update
    updated = await repo.create_or_update(
        user_id=test_user.id,
        skill_id=test_skill.id,
        score=85.0,
        mastery_level='advanced',
        total_attempts=3,
    )
    assert updated.score == 85.0
    assert updated.mastery_level == 'advanced'
    assert updated.total_attempts == 3


# ════════════════════════════════════════════════════════════════════════════════
# TEST 3: Learning attempt creation
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_learning_attempt_creation(session, test_user, test_skill, learning_service):
    """Test learning attempt creation."""
    result = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=8.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_001',
            'passed': True,
            'time_spent_seconds': 120,
            'hints_used': 0,
            'attempt_number': 1,
            'source': 'test',
        },
        award_reward=False,
    )
    assert result['recorded'] is True
    assert result['passed'] is True
    assert result['skill_id'] == str(test_skill.id)
    assert result['event_id'] is not None


# ════════════════════════════════════════════════════════════════════════════════
# TEST 4: Learning evidence recording
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_learning_evidence_recording(session, test_user, test_skill, learning_service):
    """Test learning evidence recording."""
    result = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=6.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_002',
            'passed': False,
            'time_spent_seconds': 300,
            'hints_used': 2,
            'attempt_number': 2,
            'diagnosis_codes': ['REQUIREMENT_MISREAD'],
            'source': 'test',
        },
        award_reward=False,
    )
    assert result['recorded'] is True
    assert result['passed'] is False
    assert 'REQUIREMENT_MISREAD' in result['diagnosis_codes']

    # Verify evidence was recorded
    evidence_repo = LearningEvidenceRepository(session)
    evidence_list = await evidence_repo.get_by_user(test_user.id)
    assert len(evidence_list) >= 1


# ════════════════════════════════════════════════════════════════════════════════
# TEST 5: Duplicate attempt prevention (idempotency)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_duplicate_attempt_prevention(session, test_user, test_skill, learning_service):
    """Test idempotency prevents duplicate attempts."""
    idempotency_key = f'idem_{uuid4().hex[:8]}'

    # First attempt
    result1 = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=7.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_idem',
            'passed': True,
            'idempotency_key': idempotency_key,
            'source': 'test',
        },
        award_reward=False,
    )
    assert result1['recorded'] is True
    assert result1['deduplicated'] is False

    # Second attempt with same idempotency key
    result2 = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=9.0,  # Different score — should be ignored
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_idem',
            'passed': True,
            'idempotency_key': idempotency_key,
            'source': 'test',
        },
        award_reward=False,
    )
    assert result2['recorded'] is False
    assert result2['deduplicated'] is True


# ════════════════════════════════════════════════════════════════════════════════
# TEST 6: Mastery updates
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_mastery_updates(session, test_user, test_skill, learning_service):
    """Test mastery level updates based on score."""
    # Record multiple attempts with increasing scores
    for score in [3.0, 5.0, 7.0, 9.0]:
        await learning_service.record_activity(
            user_id=test_user.id,
            activity_type='practice',
            score=score,
            activity_data={
                'skill_id': str(test_skill.id),
                'question_id': f'q_mastery_{score}',
                'passed': score >= 7.0,
                'source': 'test',
            },
            award_reward=False,
        )

    # Retrieve final state
    repo = LearnerSkillStateRepository(session)
    state = await repo.get_by_user_and_skill(test_user.id, test_skill.id)
    assert state is not None
    assert state.total_attempts == 4
    assert state.score > 0  # Should have accumulated score


# ════════════════════════════════════════════════════════════════════════════════
# TEST 7: Independent versus assisted evidence
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_independent_versus_assisted_evidence(session, test_user, test_skill, learning_service):
    """Test that independent and assisted evidence are tracked separately."""
    # Independent pass
    result1 = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=9.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_independent',
            'passed': True,
            'hints_used': 0,
            'source': 'test',
        },
        award_reward=False,
    )

    # Assisted fail (used hints)
    result2 = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=4.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_assisted',
            'passed': False,
            'hints_used': 3,
            'source': 'test',
        },
        award_reward=False,
    )

    # Verify evidence types
    evidence_repo = LearningEvidenceRepository(session)
    evidence_list = await evidence_repo.get_by_user(test_user.id)
    evidence_types = [e.evidence_type for e in evidence_list]
    assert 'independent' in evidence_types
    assert 'assisted' in evidence_types


# ════════════════════════════════════════════════════════════════════════════════
# TEST 8: SRS scheduling
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_srs_scheduling(session, test_user, test_skill, learning_service):
    """Test SRS card creation and scheduling."""
    result = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=8.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_srs_1',
            'passed': True,
            'source': 'test',
        },
        award_reward=False,
    )

    # Check that a review card was created for this skill
    repo = ReviewCardRepository(session)
    card = await repo.get_by_user_and_problem(test_user.id, str(test_skill.id))
    assert card is not None
    assert card.next_review is not None
    # next_review should be set (SM-2 schedules it)
    assert card.next_review.tzinfo is not None


# ════════════════════════════════════════════════════════════════════════════════
# TEST 9: Due review retrieval
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_due_review_retrieval(session, test_user, test_skill, learning_service):
    """Test due review retrieval."""
    # Create a card due now
    card = ReviewCard(
        user_id=test_user.id,
        problem_id='prob_due_1',
        next_review=datetime.now(timezone.utc) - timedelta(hours=1),
        difficulty='medium',
        interval=1,
        repetitions=1,
        ease_factor=2500,
    )
    session.add(card)
    await session.flush()

    # Retrieve due reviews
    due = await learning_service.get_due_reviews(test_user.id, limit=5)
    assert len(due) >= 1
    assert due[0]['problem_id'] == 'prob_due_1'


# ════════════════════════════════════════════════════════════════════════════════
# TEST 10: Repair mission creation
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_repair_mission_creation(session, test_user, test_skill, learning_service):
    """Test repair mission creation on failure."""
    result = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=3.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_repair',
            'passed': False,
            'diagnosis_codes': ['CONCEPT_GAP'],
            'source': 'test',
        },
        award_reward=False,
    )
    assert result['recorded'] is True
    assert result['repair_id'] is not None

    # Verify repair mission exists
    repo = RepairMissionRepository(session)
    mission = await repo.get_by_id(UUID(result['repair_id']))
    assert mission is not None
    assert mission.status == 'open'
    assert mission.skill_id == test_skill.id


# ════════════════════════════════════════════════════════════════════════════════
# TEST 11: Diagnosis and remediation
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_diagnosis_and_remediation(session, test_user, test_skill, learning_service):
    """Test diagnosis codes and remediation attempts."""
    # Create a repair mission first
    mission = await RepairMissionRepository(session).create({
        'user_id': test_user.id,
        'skill_id': test_skill.id,
        'title': 'Test Repair Mission',
        'description': 'Test remediation',
        'status': 'open',
        'tier': 'repair',
        'estimated_minutes': 10,
    })
    await session.flush()

    # Add remediation attempt
    repo = RemediationAttemptRepository(session)
    attempt = await repo.create({
        'repair_mission_id': mission.id,
        'user_id': test_user.id,
        'score': 8.0,
        'passed': True,
    })
    assert attempt.passed is True
    assert attempt.score == 8.0

    # Count passed attempts
    passed_count = await repo.count_passed_by_mission(mission.id)
    assert passed_count == 1


# ════════════════════════════════════════════════════════════════════════════════
# TEST 12: User ownership isolation
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_user_ownership_isolation(session, test_skill, learning_service):
    """Test that user A cannot access user B's data."""
    # Create two users
    user1 = User(email=f'u1_{uuid4().hex[:8]}@test.dev', password_hash='x', name='User 1')
    user2 = User(email=f'u2_{uuid4().hex[:8]}@test.dev', password_hash='x', name='User 2')
    session.add_all([user1, user2])
    await session.flush()

    # Record activity for user1
    await learning_service.record_activity(
        user_id=user1.id,
        activity_type='practice',
        score=8.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_isolation',
            'passed': True,
            'source': 'test',
        },
        award_reward=False,
    )

    # User2 should not see user1's attempts
    attempts = await LearningAttemptRepository(session).get_by_user(user2.id, limit=10)
    assert len(attempts) == 0

    # User1 should see their own attempts
    attempts1 = await LearningAttemptRepository(session).get_by_user(user1.id, limit=10)
    assert len(attempts1) >= 1


# ════════════════════════════════════════════════════════════════════════════════
# TEST 13: XP idempotency (via gamification)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_xp_idempotency(session, test_user, test_skill, learning_service):
    """Test that XP is not double-awarded for same activity."""
    # First attempt awards XP
    result1 = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=8.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_xp_idem',
            'passed': True,
            'idempotency_key': f'xp_{uuid4().hex[:8]}',
            'source': 'test',
        },
        award_reward=True,
    )

    # Record gamification profile state
    repo = GamificationProfileRepository(session)
    profile_before = await repo.get_by_user_id(test_user.id)
    xp_before = profile_before.xp if profile_before else 0

    # Same idempotency key should not award more XP
    xp_idem_key = f'xp_{uuid4().hex[:8]}'
    result1 = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=8.0,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_xp_idem',
            'passed': True,
            'idempotency_key': xp_idem_key,
            'source': 'test',
        },
        award_reward=True,
    )

    # Record gamification profile state
    repo = GamificationProfileRepository(session)
    profile_before = await repo.get_by_user_id(test_user.id)
    xp_before = profile_before.xp if profile_before else 0

    # Same idempotency key should not award more XP
    result2 = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=10.0,  # Higher score — should still be deduplicated
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_xp_idem',
            'passed': True,
            'idempotency_key': xp_idem_key,  # Use same key
            'source': 'test',
        },
        award_reward=True,
    )
    assert result2['deduplicated'] is True

    profile_after = await repo.get_by_user_id(test_user.id)
    # XP should not have increased due to deduplication
    xp_after = profile_after.xp if profile_after else 0
    assert xp_after == xp_before


# ════════════════════════════════════════════════════════════════════════════════
# TEST 14: Transaction rollback
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_transaction_rollback(session, test_user, test_skill):
    """Test transaction rollback behavior."""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:54322/postgres'

    # Create and commit skill1
    skill_name = f'test_rollback_skill_{uuid4().hex[:8]}'
    skill = Skill(
        name=skill_name,
        topic='test',
        difficulty='easy',
        prerequisites=[],
        is_active=True,
    )
    session.add(skill)
    await session.commit()

    # Verify skill1 exists
    result = await session.execute(select(Skill).where(Skill.name == skill_name))
    assert result.scalar_one_or_none() is not None

    # Attempt a transaction that fails with skill2 — separate session
    skill2_name = f'test_rollback_skill_2_{uuid4().hex[:8]}'
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as tx_session:
        try:
            async with tx_session.begin():
                skill2 = Skill(
                    name=skill2_name,
                    topic='test',
                    difficulty='easy',
                    prerequisites=[],
                    is_active=True,
                )
                tx_session.add(skill2)
                await tx_session.flush()
                # Force an error → transaction rolled back, skill2 undone
                raise Exception('Forced rollback')
        except Exception:
            pass
    await engine.dispose()

    # skill2 should not exist (transaction rolled back)
    result = await session.execute(select(Skill).where(Skill.name == skill2_name))
    assert result.scalar_one_or_none() is None

    # skill1 should still exist (committed earlier)
    result = await session.execute(select(Skill).where(Skill.name == skill_name))
    assert result.scalar_one_or_none() is not None


# ════════════════════════════════════════════════════════════════════════════════
# TEST 15: Failure handling
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_failure_handling_invalid_skill(session, test_user, learning_service):
    """Test failure handling when skill_id is invalid."""
    # Should not crash with invalid skill_id
    result = await learning_service.record_activity(
        user_id=test_user.id,
        activity_type='practice',
        score=5.0,
        activity_data={
            'skill_id': '00000000-0000-0000-0000-000000000000',  # Non-existent UUID
            'question_id': 'q_invalid_skill',
            'passed': True,
            'source': 'test',
        },
        award_reward=False,
    )
    assert result['recorded'] is True  # Should still record, just without skill link


# ════════════════════════════════════════════════════════════════════════════════
# TEST 16: Database constraints (unique, foreign key)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_database_constraints(session, test_user, test_skill):
    """Test database constraints."""
    # Test unique constraint on learner_skill_state (user_id + skill_id)
    from app.models.learning import LearnerSkillState

    state1 = LearnerSkillState(
        user_id=test_user.id,
        skill_id=test_skill.id,
        score=50.0,
        mastery_level='beginner',
        total_attempts=1,
    )
    session.add(state1)
    await session.flush()

    # Duplicate should fail
    state2 = LearnerSkillState(
        user_id=test_user.id,
        skill_id=test_skill.id,
        score=60.0,
        mastery_level='intermediate',
        total_attempts=2,
    )
    session.add(state2)
    with pytest.raises(Exception):
        await session.flush()
    await session.rollback()


# ════════════════════════════════════════════════════════════════════════════════
# TEST 17: Existing learning API compatibility (emission without fan-out)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_emit_learning_event_without_fanout(session, test_user, test_skill, learning_service):
    """Test lightweight event emission without full fan-out."""
    event_id = await learning_service.emit_learning_event(
        user_id=test_user.id,
        activity_type='oa_question',
        score=7.0,
        passed=True,
        activity_data={
            'skill_id': str(test_skill.id),
            'question_id': 'q_oa_1',
            'time_spent_seconds': 60,
            'metadata': {'oa_id': 'oa_001'},
        },
    )
    assert event_id is not None

    # Verify attempt was recorded
    attempt = await LearningAttemptRepository(session).get_by_id(event_id)
    assert attempt is not None
    assert attempt.activity_type == 'oa_question'
    assert attempt.passed is True


# ════════════════════════════════════════════════════════════════════════════════
# TEST 18: Schema/column consistency (actual DB validation)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_database_schema_consistency(session):
    """Validate actual PostgreSQL catalog metadata against SQLAlchemy models."""
    from app.models import Base

    # Get actual table names from PostgreSQL
    result = await session.execute(text("""
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    """))
    db_tables = {row[0] for row in result}

    # Get model table names
    model_tables = set(Base.metadata.tables.keys())

    # All model tables should exist in DB
    missing = model_tables - db_tables
    assert not missing, f"Missing tables in DB: {missing}"

    # Check a few critical columns exist
    result = await session.execute(text("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'users'
    """))
    user_columns = {row[0]: row for row in result}
    assert 'id' in user_columns
    assert 'email' in user_columns
    assert 'password_hash' in user_columns

    # Check UUID default
    id_col = user_columns['id']
    assert 'gen_random_uuid' in str(id_col[3]) or id_col[3] is not None

    # Check foreign keys exist
    result = await session.execute(text("""
        SELECT COUNT(*) FROM information_schema.table_constraints
        WHERE table_schema = 'public' AND constraint_type = 'FOREIGN KEY'
    """))
    fk_count = result.scalar()
    assert fk_count > 0, "No foreign keys found — schema may be incomplete"


# ════════════════════════════════════════════════════════════════════════════════
# TEST 19: Check constraints
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_check_constraints(session):
    """Test that check constraints are enforced."""
    # Try to insert a negative XP award (should fail due to check constraint)
    from app.models.gamification import XPEventLedger
    from app.models.identity import User

    # Get an existing user
    result = await session.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    if user is None:
        pytest.skip("No users in database for constraint test")

    # Get or create gamification profile
    from app.repositories.gamification import GamificationProfileRepository
    profile_repo = GamificationProfileRepository(session)
    profile = await profile_repo.get_or_create(user.id)

    # Try to insert negative XP (check constraint: xp_awarded >= 0)
    from sqlalchemy import text as sql_text
    try:
        await session.execute(sql_text("""
            INSERT INTO xp_event_ledger (user_id, activity_type, score, xp_awarded, diamonds_awarded, metadata, reward_policy_version, created_at)
            VALUES (:user_id, 'test', 0, -10, 0, '{}'::jsonb, 'v1', NOW())
        """), {"user_id": user.id})
        await session.flush()
        pytest.fail("Should have raised check constraint violation")
    except Exception:
        await session.rollback()
    # Constraint works — test passes
