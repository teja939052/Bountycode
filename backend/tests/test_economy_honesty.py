"""Economy honesty: tripwire + normalization + weekly reset + ledger + badges.

LAW: record_practice is the only writer of reward fields. These tests pin
that law, the score contract, and the fixes for the bypass/race/crash bugs.
"""
import pathlib
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import gamification_collection, users_collection
from app.middleware.rate_limiter import clear_login_attempts
from app.services.gamification_core import (
    normalize_badge_ids,
    calculate_stars,
    _calculate_xp,
)
from app.services.gamification import _league_week_id


# ─── CI tripwire: no direct reward writes outside the engine ───

FORBIDDEN = re.compile(
    r'gamification_collection\(\)\.(update_one|update_many|find_one_and_update)'
    r'[\s\S]{0,600}\$inc["\']?\s*:\s*\{[^}]*\b(diamonds|coins|stars_total)\b'
    r'|\bgamification\.update_one\b[\s\S]{0,300}\$inc["\']?\s*:\s*\{[^}]*\bxp\b',
    re.I,
)
# services/gamification.py is the engine itself. duolingo writes hearts only
# ($set, lesson-engine state — explicitly allowed, never Diamonds).
ALLOWED_FILES = {"backend/app/services/gamification.py"}


def test_no_direct_xp_writes():
    root = pathlib.Path("backend/app")
    if not root.is_dir():
        root = pathlib.Path("app")
    offenders = []
    for p in root.rglob("*.py"):
        posix = p.as_posix()
        if posix in ALLOWED_FILES or posix.endswith("app/services/gamification.py"):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if FORBIDDEN.search(text):
            offenders.append(posix)
    assert offenders == [], f"Direct Diamonds writes outside record_practice: {offenders}"


# ─── Pure unit pins ───

def test_badge_normalize():
    assert normalize_badge_ids(["a", "b", "a"]) == ["a", "b"]
    assert normalize_badge_ids([{"id": "x"}, "y"]) == ["x", "y"]
    assert normalize_badge_ids([{"nope": 1}, None, 5, ""]) == []
    # legacy daily-bonus objects collapse to their id
    assert normalize_badge_ids([{"id": "daily_bonus_42", "name": "Lucky"}]) == ["daily_bonus_42"]


def test_stars_scale():
    assert calculate_stars(10) == 3
    assert calculate_stars(9, time_taken=10) == 3
    assert calculate_stars(7) == 2
    assert calculate_stars(5) == 1


def test_week_id_format():
    import re as _re
    assert _re.fullmatch(r"\d{4}-W\d{2}", _league_week_id())


def test_lesson_base_sanity():
    # canonical lesson pass base (15) + perfect/high bonuses, pre-multiplier
    assert _calculate_xp("lesson", 10.0, role="sde") >= 15


# ─── Live DB tests ───

def _db_available() -> bool:
    try:
        from app.database import get_client
        import asyncio

        async def _ping():
            await get_client().admin.command("ping")

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(_ping())
        finally:
            loop.close()
        return True
    except Exception:
        return False


needs_db = pytest.mark.skipif(not _db_available(), reason="MongoDB unreachable")
EMAIL = "economy_honesty@example.com"


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture(autouse=True)
async def clear_rate_limiter():
    from app.middleware.rate_limiter import request_counts
    request_counts.clear()
    yield
    request_counts.clear()


@pytest.fixture
async def test_user(client):
    clear_login_attempts(EMAIL)
    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    r = await client.post(
        "/api/v1/auth/register",
        json={"email": EMAIL, "name": "Economy Honesty", "password": "SecurePass123!"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    yield {"token": body["token"], "user_id": body["user"]["id"]}
    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": body["user"]["id"]})
    except Exception:
        pass
    try:
        from app.database import gamification_events_collection
        await gamification_events_collection.delete_many({"user_id": body["user"]["id"]})
    except Exception:
        pass
    clear_login_attempts(EMAIL)


def _auth(token: str):
    return {"Authorization": f"Bearer {token}"}


@needs_db
async def test_legacy_object_badges_dont_crash_profile(test_user):
    """Regression: mixed badge shapes must read clean (TypeError crash fix)."""
    from app.services.gamification import get_gamification_profile
    uid = test_user["user_id"]
    await gamification_collection().update_one(
        {"user_id": uid},
        {"$set": {"badges": [
            "first_solution",
            {"id": "daily_bonus_42", "name": "Lucky Streak", "icon": "🍀"},
        ]}},
        upsert=True,
    )
    profile = await get_gamification_profile(uid)
    assert "daily_bonus_42" in profile["badges"]
    assert "first_solution" in profile["badges"]
    assert isinstance(profile["badges_details"], list)


@needs_db
async def test_weekly_reset_and_ledger_reconcile(test_user):
    """Fake an old week, record practice, assert reset+snapshot+ledger math."""
    from app.services.gamification import record_practice
    from app.database import gamification_events_collection
    uid = test_user["user_id"]
    await gamification_collection().update_one(
        {"user_id": uid},
        {"$set": {"weekly_league_week": "2000-W01", "weekly_league_xp": 9999}},
        upsert=True,
    )
    before = (await gamification_collection().find_one({"user_id": uid}) or {}).get("diamonds", 0)
    res = await record_practice(uid, "lesson", 10.0, {"skill_id": "test.economy"})
    after_doc = await gamification_collection().find_one({"user_id": uid})
    # reset fired, snapshot frozen
    assert after_doc["weekly_league_week"] == _league_week_id()
    assert after_doc["weekly_league_xp"] < 9999
    assert after_doc["weekly_league_last"] == {"week": "2000-W01", "diamonds": 9999, "rank": None}
    # response == stored delta == ledger sum
    assert res["xp_gained"] == after_doc["diamonds"] - before
    rows = await gamification_events_collection.find({"user_id": uid}).to_list(100)
    assert sum(r["xp_awarded"] for r in rows) == after_doc["diamonds"] - before
    assert rows[0]["reward_policy_version"] == "2026.1"


@needs_db
async def test_percent_score_normalized_not_perfect(test_user):
    """A 50%-correct coding attempt must not mint perfect bonuses/3 stars."""
    from app.services.gamification import record_practice
    uid = test_user["user_id"]
    res = await record_practice(uid, "coding", 50.0, {"skill_id": "test.economy"})
    # normalized 5.0: no perfect (+40) / high (+20) bonuses, 1 star
    assert res["stars_earned"] == 1
