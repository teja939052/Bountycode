"""Regression tests for durable spaced-repetition scheduling."""
from datetime import datetime, timedelta, timezone

import pytest

from app.services import spaced_repetition as srs


def test_first_successful_reviews_follow_all_learning_steps(monkeypatch):
    clock = [datetime(2026, 11, 6, 9, 0, tzinfo=timezone.utc)]
    monkeypatch.setattr(srs, "utcnow", lambda: clock[0])

    engine = srs.SpacedRepetitionEngine()
    state = engine.create_new_card("quantitative.percentages", "user-1")

    state = engine.review(state, srs.ReviewGrade.GOOD)
    assert state.learning_step == 1
    assert state.interval == 0
    assert state.next_review == clock[0] + timedelta(minutes=10)

    clock[0] = state.next_review
    state = engine.review(state, srs.ReviewGrade.GOOD)
    assert state.learning_step == 2
    assert state.interval == 0
    assert state.next_review == clock[0] + timedelta(days=1)

    clock[0] = state.next_review
    state = engine.review(state, srs.ReviewGrade.GOOD)
    assert state.learning_step == 3
    assert state.interval == 3
    assert state.repetitions == 1
    assert state.next_review == clock[0] + timedelta(days=3)


def test_deserialize_preserves_legacy_problem_card_due_date():
    raw = {
        "_id": "mongo-id",
        "problem_id": "arrays:two-pointers",
        "user_id": "user-2",
        "interval_days": 7,
        "review_count": 4,
        "ease_factor": 2.35,
        "learning_step": 3,
        "total_reviews": 6,
        "lapses": 1,
        "last_reviewed": "2026-11-01T08:00:00+05:30",
        "next_review": "2026-11-08T08:00:00+05:30",
        "created_at": "2026-10-20T08:00:00+05:30",
        "updated_at": "2026-11-01T08:00:00+05:30",
        "difficulty": "medium",
    }

    state = srs.deserialize_state(raw)

    assert state.concept_id == "arrays:two-pointers"
    assert state.user_id == "user-2"
    assert state.interval == 7
    assert state.repetitions == 4
    assert state.ease_factor == 2.35
    assert state.next_review == datetime(2026, 11, 8, 2, 30, tzinfo=timezone.utc)
    assert state.last_reviewed == datetime(2026, 11, 1, 2, 30, tzinfo=timezone.utc)


def test_due_card_selection_does_not_reset_future_dates(monkeypatch):
    now = datetime(2026, 11, 6, 9, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(srs, "utcnow", lambda: now)
    due = srs.deserialize_state({
        "concept_id": "verbal.reading",
        "user_id": "user-3",
        "next_review": now - timedelta(minutes=1),
    })
    future = srs.deserialize_state({
        "concept_id": "quantitative.ratio",
        "user_id": "user-3",
        "next_review": now + timedelta(days=2),
    })

    selected = srs.get_due_cards([future, due], limit=10)

    assert [card.concept_id for card in selected] == ["verbal.reading"]


@pytest.mark.asyncio
async def test_journey_includes_due_mongo_cards_via_shared_deserializer(monkeypatch):
    """Journey must accept Mongo metadata and legacy problem-card fields."""
    from app.services import journey_engine

    now = datetime(2026, 11, 6, 9, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(srs, "utcnow", lambda: now)

    documents = [
        {
            "_id": "mongo-due",
            "problem_id": "arrays:two-pointers",
            "user_id": "user-4",
            "interval_days": 3,
            "review_count": 2,
            "next_review": now - timedelta(minutes=5),
            "difficulty": "medium",
        },
        {
            "_id": "mongo-future",
            "problem_id": "quantitative.ratio",
            "user_id": "user-4",
            "interval": 4,
            "repetitions": 2,
            "next_review": now + timedelta(days=4),
        },
    ]

    class Cursor:
        def __init__(self, rows):
            self.rows = rows

        def limit(self, _count):
            return self

        def __aiter__(self):
            async def iterate():
                for row in self.rows:
                    yield row
            return iterate()

    class Collection:
        def find(self, query):
            assert query == {"user_id": "user-4"}
            return Cursor(documents)

    from app import database
    monkeypatch.setattr(database, "srs_cards_collection", lambda: Collection())

    due = await journey_engine._get_srs_due("user-4")

    assert [card.concept_id for card in due] == ["arrays:two-pointers"]
    assert due[0].user_id == "user-4"


@pytest.mark.asyncio
async def test_study_engine_can_record_mastery_and_srs_without_double_awarding_xp(monkeypatch):
    from app import database
    from app.services import skill_assessment, study_engine

    mastery_calls = []
    srs_writes = []
    event_writes = []

    async def fake_update_skill_score(user_id, category, subskill, score, passed):
        mastery_calls.append((user_id, category, subskill, score, passed))

    async def fake_fetch_skill_score(_user_id, _category):
        return 42.0

    async def forbidden_reward(*_args, **_kwargs):
        raise AssertionError("award_reward=False must not call record_practice")

    async def no_op_invalidate(_user_id):
        return None

    class FakeSrsCollection:
        async def find_one(self, query):
            assert query == {"user_id": "user-1", "problem_id": "coding.variables"}
            return None

        async def update_one(self, query, update, upsert=False):
            srs_writes.append((query, update, upsert))

    class FakeEventsCollection:
        async def insert_one(self, document):
            event_writes.append(document)

    monkeypatch.setattr(skill_assessment, "update_skill_score", fake_update_skill_score)
    monkeypatch.setattr(study_engine, "_fetch_skill_score", fake_fetch_skill_score)
    monkeypatch.setattr(study_engine, "record_practice", forbidden_reward)
    monkeypatch.setattr(study_engine, "invalidate_daily_plan", no_op_invalidate)
    monkeypatch.setattr(database, "srs_cards_collection", lambda: FakeSrsCollection())
    monkeypatch.setattr(database, "learning_events_collection", lambda: FakeEventsCollection())

    result = await study_engine.record_activity(
        "user-1",
        {
            "type": "learn",
            "source": "company_lesson_assessment",
            "skill_id": "coding.variables",
            "passed": True,
            "score": 85,
            "time_spent": 90,
        },
        award_reward=False,
    )

    assert result["recorded"] is True
    assert result["xp_awarded"] == 0
    assert result["xp_applied"] is False
    assert mastery_calls == [("user-1", "coding", "variables", 85.0, True)]
    assert len(srs_writes) == 1
    assert srs_writes[0][0] == {"user_id": "user-1", "problem_id": "coding.variables"}
    assert len(event_writes) == 1
    assert event_writes[0]["skill_id"] == "coding.variables"
    assert event_writes[0]["source"] == "company_lesson_assessment"
