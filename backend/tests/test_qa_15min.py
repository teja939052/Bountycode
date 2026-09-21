"""15-minute trust QA: the cheapest insurance in the thread.

Each test replays a real failure mode found during the audits:
1. Engine outage mid-complete -> entry saved + rewards_pending (no loss).
2. Rapid double activity -> combo counts each event once (no double-count).
3. Legacy object badges -> profile reads 200 (no 500).
4. Read-after-write: profile reflects the latest award immediately
   (the API-level half of tab-B staleness; the browser half is covered by
   refetchOnWindowFocus + reward-event invalidation).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import gamification_collection, users_collection
from app.middleware.rate_limiter import clear_login_attempts


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
EMAIL = "qa_15min@example.com"


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
        json={"email": EMAIL, "name": "QA Script", "password": "SecurePass123!"},
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
async def test_engine_outage_loses_nothing(client, test_user, monkeypatch):
    """Forced engine failure on worlds complete: entry saved + flagged."""
    import app.routes.worlds as worlds

    async def _boom(*a, **k):
        raise RuntimeError("simulated engine outage")

    monkeypatch.setattr(worlds, "_award_xp", _boom)
    token, uid = test_user["token"], test_user["user_id"]
    r = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": "apples = 5", "language": "python", "time_spent_seconds": 5},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["completed"] is True
    assert body["rewards_pending"] is True
    assert body["xp_awarded"] == 0
    doc = await gamification_collection().find_one({"user_id": uid})
    entry = doc["completed_competencies"]["foundations:level-1"]
    assert entry["completed"] is True
    assert entry["rewards_pending"] is True


@needs_db
async def test_rapid_double_activity_counts_combo_once_each(test_user):
    """Two back-to-back awards: combo 1 then 2 (window 90s), never 3+."""
    from app.services.gamification import record_practice
    uid = test_user["user_id"]
    r1 = await record_practice(uid, "lesson", 10.0, {"skill_id": "qa.combo"})
    r2 = await record_practice(uid, "lesson", 10.0, {"skill_id": "qa.combo"})
    assert r1["combo"]["current"] == 1
    assert r2["combo"]["current"] == 2
    assert r2["combo"]["current"] <= 2


@needs_db
async def test_badge_claim_survives_legacy_shapes(test_user):
    """Object badges in DB must not 500 profile reads or badge checks."""
    from app.services.gamification import get_gamification_profile
    uid = test_user["user_id"]
    await gamification_collection().update_one(
        {"user_id": uid},
        {"$set": {"badges": [{"id": "daily_bonus_7", "name": "Old"}]}},
        upsert=True,
    )
    profile = await get_gamification_profile(uid)
    assert profile["badges"] == ["daily_bonus_7"]
    assert profile["badges_details"] == []


@needs_db
async def test_profile_reflects_latest_award_immediately(client, test_user):
    """Read-after-write: GET profile shows the just-recorded award."""
    from app.services.gamification import record_practice
    uid, token = test_user["user_id"], test_user["token"]
    before = (await gamification_collection().find_one({"user_id": uid}) or {}).get("diamonds", 0)
    res = await record_practice(uid, "lesson", 10.0, {"skill_id": "qa.stale"})
    r = await client.get("/api/v1/gamification/profile", headers=_auth(token))
    assert r.status_code == 200
    assert r.json()["diamonds"] == before + res["xp_gained"]
