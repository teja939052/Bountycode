"""Rank ladder + badge endpoint tests.

Pure-function pins for voyage_rank_for_level boundaries, plus live-HTTP
tests for the public SVG badge (seeded profile, no auth, no doc creation).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import gamification_collection, users_collection
from app.middleware.rate_limiter import clear_login_attempts
from app.services.gamification_core import VOYAGE_RANKS, voyage_rank_for_level


def test_rank_boundaries():
    assert voyage_rank_for_level(1) == ("Deckhand", "⚓", 0)
    assert voyage_rank_for_level(9) == ("Deckhand", "⚓", 0)
    assert voyage_rank_for_level(10) == ("Lookout", "🔭", 1)
    assert voyage_rank_for_level(24) == ("Lookout", "🔭", 1)
    assert voyage_rank_for_level(25) == ("Navigator", "🧭", 2)
    assert voyage_rank_for_level(44) == ("Navigator", "🧭", 2)
    assert voyage_rank_for_level(45) == ("First Mate", "🗺️", 3)
    assert voyage_rank_for_level(64) == ("First Mate", "🗺️", 3)
    assert voyage_rank_for_level(65) == ("Captain", "🏴‍☠️", 4)
    assert voyage_rank_for_level(84) == ("Captain", "🏴‍☠️", 4)
    assert voyage_rank_for_level(85) == ("Fleet Admiral", "👑", 5)
    assert voyage_rank_for_level(100) == ("Fleet Admiral", "👑", 5)
    # clamps, never throws
    assert voyage_rank_for_level(0)[2] == 0
    assert voyage_rank_for_level(1000)[2] == 5


def test_six_tiers_escalating():
    assert len(VOYAGE_RANKS) == 6
    mins = [r["min_level"] for r in VOYAGE_RANKS]
    assert mins == sorted(mins) and mins[0] == 1
    assert len({r["rank"] for r in VOYAGE_RANKS}) == 6


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
EMAIL = "rank_badge_test@example.com"


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
async def seeded_user(client):
    clear_login_attempts(EMAIL)
    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    r = await client.post(
        "/api/v1/auth/register",
        json={"email": EMAIL, "name": "Rank Badge", "password": "SecurePass123!"},
    )
    assert r.status_code == 200, r.text
    user_id = r.json()["user"]["id"]
    # Seed: enough Diamonds for Lookout (level 10 needs 4050 Diamonds) + foundations cleared
    from app.data.worlds_data import WORLD_REGISTRY
    w = WORLD_REGISTRY["foundations"]
    completed = {f"foundations:{l.id}": {"completed": True} for t in w.towns for l in t.levels}
    try:
        await gamification_collection().update_one(
            {"user_id": user_id},
            {"$set": {"diamonds": 5000, "streak": 7, "completed_competencies": completed}},
            upsert=True,
        )
    except Exception as e:
        pytest.skip(f"seed failed: {e}")
    yield {"user_id": user_id}
    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": user_id})
    except Exception:
        pass
    clear_login_attempts(EMAIL)


@needs_db
async def test_badge_svg_no_auth(client, seeded_user):
    uid = seeded_user["user_id"]
    # No Authorization header on purpose: embeds can't send auth.
    r = await client.get(f"/api/v1/gamification/badge/{uid}.svg")
    assert r.status_code == 200, r.text
    assert r.headers["content-type"].startswith("image/svg+xml")
    body = r.text
    assert body.lstrip().startswith("<svg")
    assert "Lookout" in body
    assert "1/12 worlds cleared" in body
    assert "7-day streak" in body
    assert EMAIL not in body and uid not in body  # no PII in the image


@needs_db
async def test_badge_404_creates_nothing(client):
    ghost = "ghost-user-id-that-cannot-exist-000"
    try:
        await gamification_collection().delete_many({"user_id": ghost})
    except Exception:
        pass
    r = await client.get(f"/api/v1/gamification/badge/{ghost}.svg")
    assert r.status_code == 404
    doc = await gamification_collection().find_one({"user_id": ghost})
    assert doc is None  # public URL must never mint profiles


@needs_db
async def test_profile_and_leaderboard_carry_rank(client, seeded_user):
    from app.middleware.auth import get_current_user  # noqa: F401 (keeps import graph honest)
    token_r = await client.post("/api/v1/auth/login", json={"email": EMAIL, "password": "SecurePass123!"})
    token = token_r.json()["token"]
    H = {"Authorization": f"Bearer {token}"}
    p = await client.get("/api/v1/gamification/profile", headers=H)
    assert p.status_code == 200, p.text
    body = p.json()
    assert body["rank_title"] == "Lookout"
    assert body["rank_tier"] == 1
    assert "title" in body  # legacy tower title untouched
    lb = await client.get("/api/v1/gamification/leaderboard?limit=50")
    assert lb.status_code == 200
    me = [e for e in lb.json() if e.get("user_id") == seeded_user["user_id"]]
    assert me and me[0]["rank_title"] == "Lookout"
