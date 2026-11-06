from datetime import datetime, timedelta, timezone

from app.routes.quiz import _quiz_time_expired


def test_untimed_quiz_never_expires():
    now = datetime.now(timezone.utc)
    assert not _quiz_time_expired({"time_limit_seconds": 0, "created_at": now}, now)


def test_timed_quiz_expires_after_deadline():
    started = datetime(2026, 11, 6, 10, 0, tzinfo=timezone.utc)
    assert not _quiz_time_expired(
        {"time_limit_seconds": 60, "created_at": started},
        started + timedelta(seconds=60),
    )
    assert _quiz_time_expired(
        {"time_limit_seconds": 60, "created_at": started},
        started + timedelta(seconds=61),
    )


def test_naive_database_datetime_is_treated_as_utc():
    started = datetime(2026, 11, 6, 10, 0)
    assert _quiz_time_expired(
        {"time_limit_seconds": 30, "created_at": started},
        datetime(2026, 11, 6, 10, 1, tzinfo=timezone.utc),
    )


def test_missing_timestamp_does_not_crash_legacy_sessions():
    assert not _quiz_time_expired({"time_limit_seconds": 30})
