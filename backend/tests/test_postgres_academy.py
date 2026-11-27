"""Integration tests for the PostgreSQL-backed Academy learner journey."""
import os
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.identity import User
from app.repositories.academy import (
    AcademyDiagnosticSessionRepository,
    AcademyLearnerProfileRepository,
    AcademyLearningPlanRepository,
    model_dict,
)

DATABASE_URL = os.environ.get(
    "SUPABASE_DB_URL",
    "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/bountycode",
)


@pytest.fixture
async def session():
    engine = create_async_engine(DATABASE_URL)
    factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as db:
        yield db
        await db.rollback()
    await engine.dispose()


@pytest.fixture
async def user(session):
    account = User(
        email=f"academy_{uuid4().hex[:10]}@test.dev",
        password_hash="test-hash",
        name="Academy Test User",
    )
    session.add(account)
    await session.flush()
    return account


@pytest.mark.asyncio
async def test_academy_profile_diagnostic_and_plan_persist(session, user):
    profile_repo = AcademyLearnerProfileRepository(session)
    profile = await profile_repo.upsert(
        user.id,
        {
            "target_role": "software_engineer",
            "target_companies": ["tcs", "wipro"],
            "onboarding_complete": True,
            "daily_minutes": 90,
        },
    )
    assert model_dict(profile)["onboarding_complete"] is True

    diagnostic_repo = AcademyDiagnosticSessionRepository(session)
    diagnostic = await diagnostic_repo.create(user.id, "diag_test", ["q1", "q2"])
    assert await diagnostic_repo.append_answer(
        diagnostic,
        {"question_id": "q1", "is_correct": True, "domain_id": "sql"},
    )
    assert not await diagnostic_repo.append_answer(
        diagnostic,
        {"question_id": "q1", "is_correct": False, "domain_id": "sql"},
    )
    result = {"diagnostic_id": "diag_test", "overall_score": 50, "skills": []}
    await diagnostic_repo.complete(diagnostic, result)

    latest = await diagnostic_repo.latest_completed(user.id)
    assert latest is not None
    assert latest.result["overall_score"] == 50

    plan = await AcademyLearningPlanRepository(session).upsert(
        user.id, {"current_level": 1, "next_action": {"domain": "sql"}}
    )
    assert plan.plan["current_level"] == 1
    await session.commit()

    persisted = await profile_repo.get_by_user(user.id)
    assert persisted is not None
    assert persisted.target_companies == ["tcs", "wipro"]
