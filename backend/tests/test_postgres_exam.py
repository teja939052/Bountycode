"""Integration tests for PostgreSQL-backed practice exam state."""
import os
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.identity import User
from app.repositories.exam import PracticeExamAttemptRepository

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


@pytest.mark.asyncio
async def test_practice_exam_state_persists_without_answer_keys(session):
    user = User(
        email=f"exam_{uuid4().hex[:10]}@test.dev",
        password_hash="test-hash",
        name="Exam Test User",
    )
    session.add(user)
    await session.flush()

    repo = PracticeExamAttemptRepository(session)
    attempt = await repo.create({
        "user_id": user.id,
        "topic": "percentages",
        "duration_minutes": 20,
        "question_ids": ["trusted-q-1", "trusted-q-2"],
        "answers": {},
    })
    await session.commit()

    assert attempt.status == "in_progress"
    assert not hasattr(attempt, "questions")
    assert not hasattr(attempt, "correct_answer")

    async with session.begin():
        updated = await repo.set_answers(attempt.id, user.id, {"trusted-q-1": "B"})
        assert updated is not None
    completed = await repo.complete(attempt.id, user.id, 50.0, 1)
    assert completed is not None
    await session.commit()

    persisted = await repo.get_by_id_and_user(attempt.id, user.id)
    assert persisted is not None
    assert persisted.answers == {"trusted-q-1": "B"}
    assert persisted.status == "completed"
    assert persisted.score == 50
    assert persisted.correct == 1
    assert len(await repo.list_by_user(user.id)) == 1
