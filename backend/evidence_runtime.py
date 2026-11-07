"""Runtime evidence: submit real code through judge + boss for worlds 9 and 12."""
import asyncio
import sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import gamification_collection, users_collection


EMAIL = "world_gate_evidence2@example.com"

FOUNDATIONS_CODES = {
    "level-1": "apples = 5",
    "level-2": "apples = 5\nbread = 3\nprint(apples)",
    "level-3": "apples = 5\napples = 10\nprint(apples)",
    "level-4": "apples = 5\nbread = 3\ncoins = 20",
    "level-5": "apples = 5\nbread = 3\ntotal = apples + bread\nprint(total)",
    "boss-1": "apples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)",
}


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
    from app.middleware.rate_limiter import clear_login_attempts
    clear_login_attempts(EMAIL)
    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": EMAIL})
    except Exception:
        pass

    r = await client.post(
        "/api/v1/auth/register",
        json={"email": EMAIL, "name": "World Gate Evidence", "password": "SecurePass123!"},
    )
    assert r.status_code == 200, f"Register failed: {r.text}"
    body = r.json()
    token = body["token"]
    user_id = body["user"]["id"]

    yield {"token": token, "user_id": user_id}

    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": user_id})
    except Exception:
        pass
    clear_login_attempts(EMAIL)


async def _auth(token):
    return {"Authorization": f"Bearer {token}"}


async def _complete_all_foundations(client, token):
    """Clear all 6 foundations levels + boss via real endpoints."""
    foundations_world = "foundations"
    for lid, code in FOUNDATIONS_CODES.items():
        r = await client.post(
            f"/api/v1/worlds/{foundations_world}/levels/{lid}/complete",
            headers=await _auth(token),
            json={"code": code, "language": "python", "time_spent_seconds": 20},
        )
        assert r.status_code == 200, f"{lid}: {r.text}"


async def main():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Step 1: Register
        r = await client.post(
            "/api/v1/auth/register",
            json={"email": EMAIL, "name": "World Gate Evidence", "password": "SecurePass123!"},
        )
        assert r.status_code == 200, f"Register failed: {r.text}"
        token = r.json()["token"]
        user_id = r.json()["user"]["id"]
        print(f"Registered user {EMAIL}, uid={user_id}")

        # Step 2: Clear foundations (prereq for all other worlds)
        print("\n=== Clearing foundations ===")
        await _complete_all_foundations(client, token)
        print("  All foundations complete.")

        # Step 3: Attempt world 9 (dynamic) level d-1
        print("\n=== World 9 (dynamic) d-1 attempt ===")
        r = await client.post(
            "/api/v1/worlds/dynamic/levels/d-1/attempt",
            headers=await _auth(token),
            json={"code": "cache = {}\nif 'key' in cache:\n    print(cache['key'])\nelse:\n    cache['key'] = 'found'", "language": "python", "time_spent_seconds": 10},
        )
        print(f"  status={r.status_code}")
        if r.status_code == 200:
            j = r.json()
            print(f"  judge_pass={j.get('judge_pass')}")
            print(f"  xp_awarded={j.get('xp_awarded')}")
            print(f"  xp_total={j.get('xp_total')}")
            if j.get('boss_triggered'):
                print("  *** BOSS TRIGGERED ***")
        else:
            print(f"  {r.text}")

        # Step 4: Attempt world 12 (alpine) level a-1
        print("\n=== World 12 (alpine) a-1 attempt ===")
        r = await client.post(
            "/api/v1/worlds/alpine/levels/a-1/attempt",
            headers=await _auth(token),
            json={"code": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.count = 0", "language": "python", "time_spent_seconds": 10},
        )
        print(f"  status={r.status_code}")
        if r.status_code == 200:
            j = r.json()
            print(f"  judge_pass={j.get('judge_pass')}")
            print(f"  xp_awarded={j.get('xp_awarded')}")
            print(f"  xp_total={j.get('xp_total')}")
            if j.get('boss_triggered'):
                print("  *** BOSS TRIGGERED ***")
        else:
            print(f"  {r.text}")

        # Step 5: Check map state
        print("\n=== Map state ===")
        r = await client.get("/api/v1/map/state", headers=await _auth(token))
        print(f"  status={r.status_code}")
        if r.status_code == 200:
            m = r.json()
            for w in m.get("all_worlds", []):
                print(f"  {w['id']}: status={w['status']}, done={w['done']}/{w['total']}")


asyncio.run(main())