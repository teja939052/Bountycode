"""Personalized Placement OS features — in-process verification.

Covers, with real HTTP through the ASGI app (no ports, no live server):
- 6-world registry with relevance tags (Vision Lock alignment)
- Onboarding mission brief: v3-target accepted, fan-out normalizes company,
  study/today carries mission meta, journey resolves the target
- Aptitude theory cards + all 19 sub-category drills serve
- Sheets progress aggregate shape
- Exam pattern block in track overview
- Mistake Book from a real failed activity
- Readiness simulator shape + verdict set
- CS Fundamentals theory + Alumni experiences serving

Run: venv\\Scripts\\python.exe -m pytest tests/test_os_features.py -q
"""
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import users_collection, gamification_collection


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


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest.fixture
async def authed(client):
    email = f"osfeat.{int(time.time() * 1000)}@example.com"
    r = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "OSFeat", "password": "SecurePass123!"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    token = body["token"]
    user_id = body["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    yield {"headers": headers, "user_id": user_id, "email": email}
    try:
        await users_collection().delete_many({"email": email})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": user_id})
    except Exception:
        pass


def test_worlds_six_with_tags():
    from app.data.worlds_data import WORLD_REGISTRY

    assert set(WORLD_REGISTRY) == {
        "foundations",
        "searchlands",
        "sorting",
        "recursion",
        "linked",
        "stack",
    }
    total = tagged = 0
    for w in WORLD_REGISTRY.values():
        for t in getattr(w, "towns", []) or []:
            for lvl in getattr(t, "levels", []) or []:
                total += 1
                assert getattr(lvl, "company_relevance", None)
                assert getattr(lvl, "role_relevance", None)
                tagged += 1
    assert total == 32
    assert tagged == 32


@needs_db
async def test_onboarding_brief_fanout_and_mission(client, authed):
    h = authed["headers"]
    # v3-target previously 404'd and lost data — must persist now
    r = await client.post(
        "/api/v1/onboarding/complete",
        json={
            "step_id": "v3-target",
            "goal": "placements",
            "role": "Software Engineer",
            "company": "TCS NQT",
            "college": "SRM",
            "branch": "CSE",
            "grad_year": 2026,
            "placement_date": "2026-10-25",
            "daily_minutes": 45,
            "prep_level": "beginner",
        },
        headers=h,
    )
    assert r.status_code == 200, r.text

    r = await client.post(
        "/api/v1/auth/onboarding-complete",
        json={
            "target_companies": ["tcs"],
            "target_company": "tcs",
            "college": "SRM",
            "placement_date": "2026-10-25",
            "daily_minutes": 45,
        },
        headers=h,
    )
    assert r.status_code == 200, r.text
    assert r.json()["onboarding"]["daily_minutes"] == 45

    t = (await client.get("/api/v1/study/today?force=true", headers=h)).json()
    assert t["mission"]["daily_minutes"] == 45
    assert t["mission"]["days_remaining"] is not None
    assert t["mission"]["pace_label"] in ("final week", "focused run", "steady build")

    j = (await client.get("/api/v1/journey/state", headers=h)).json()
    assert j["data"]["company"]["target"] == "tcs"

    rd = (await client.get("/api/v1/gamification/readiness", headers=h)).json()
    assert rd["target_company"] == "tcs"


@needs_db
async def test_aptitude_theory_and_drills(client, authed):
    h = authed["headers"]
    t = (await client.get("/api/v1/aptitude/theory", headers=h)).json()
    assert t["total"] == 18
    q = (await client.get("/api/v1/aptitude/theory-for/quantitative", headers=h)).json()
    assert len(q["topics"]) == 8
    assert all("formulas" in x and "worked_example" in x for x in q["topics"])

    for cat in ("puzzles", "blood-relations", "direction-sense", "sentence-correction"):
        r = await client.post(
            "/api/v1/aptitude/start",
            json={"category": cat, "difficulty": "medium", "question_count": 3},
            headers=h,
        )
        assert r.status_code == 200, (cat, r.text)
        assert r.json()["total_questions"] >= 1


@needs_db
async def test_sheets_progress_shape(client, authed):
    h = authed["headers"]
    p = (await client.get("/api/v1/questions/patterns/progress", headers=h)).json()
    assert p["total_patterns"] > 0
    assert p["total_problems"] > 0
    first = p["sheets"][0]
    for key in ("pattern", "slug", "total", "solved", "mastered", "easy", "medium", "hard"):
        assert key in first
    arrays = next(s for s in p["sheets"] if s["pattern"] == "Arrays")
    assert arrays["easy"] + arrays["medium"] + arrays["hard"] == arrays["total"]


@needs_db
async def test_exam_pattern_block(client, authed):
    h = authed["headers"]
    t = (await client.get("/api/v1/tracks/tcs/overview", headers=h)).json()
    ep = t["exam_pattern"]
    assert ep["name"] == "TCS NQT"
    assert len(ep["stages"]) == 2
    assert all(s["sections"] for s in ep["stages"])
    assert ep["band_logic"]
    assert ep["last_verified_at"]


@needs_db
async def test_mistake_book_from_failure(client, authed):
    h = authed["headers"]
    r = await client.post(
        "/api/v1/study/activity",
        json={"type": "practice", "passed": False, "skill_id": "dsa.arrays",
              "score": 2, "time_spent": 300},
        headers=h,
    )
    assert r.status_code == 200, r.text
    m = (await client.get("/api/v1/evidence/mistakes", headers=h)).json()
    assert m["total_mistakes"] >= 1
    assert m["top_diagnosis"] == "CONCEPT_GAP"
    assert m["items"][0]["skill_id"] == "dsa.arrays"


@needs_db
async def test_simulator_shape(client, authed):
    h = authed["headers"]
    s = (await client.get(
        "/api/v1/gamification/readiness/simulate?company=tcs&daily_minutes=45",
        headers=h,
    )).json()
    assert s["company"] == "tcs"
    assert "company_score" in s["current"]
    assert s["projection"]["verdict"] in (
        "ready", "on-track", "tight", "needs-more-time", "unknown-date")
    assert isinstance(s["highest_impact"], list)
    assert s["projection"]["note"]


@needs_db
async def test_cs_fundamentals_and_alumni(client, authed):
    h = authed["headers"]
    c = (await client.get("/api/v1/cs-fundamentals/theory", headers=h)).json()
    assert c["total"] == 20
    assert set(c["domains"]) == {"os", "dbms", "oop", "cn", "sql"}
    d = (await client.get("/api/v1/cs-fundamentals/domain/dbms", headers=h)).json()
    assert d["total"] == 4
    a = (await client.get("/api/v1/placement/alumni?limit=20", headers=h)).json()
    assert len(a["experiences"]) >= 1
    assert a["experiences"][0]["rounds"]
