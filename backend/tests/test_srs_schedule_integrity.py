"""Regression tests for durable spaced-repetition scheduling."""
from datetime import datetime, timedelta, timezone

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
