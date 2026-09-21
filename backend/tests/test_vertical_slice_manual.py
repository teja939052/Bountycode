"""Manual submission test for new vertical-slice content."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import users_collection, gamification_collection

client = TestClient(app)

FOUNDATIONS_CODES = {
    "level-1": "apples = 5",
    "level-2": "apples = 5\nbread = 3\nprint(apples)",
    "level-3": "apples = 5\napples = 10\nprint(apples)",
    "level-4": "apples = 5\nbread = 3\ncoins = 20",
    "level-5": "apples = 5\nbread = 3\ntotal = apples + bread\nprint(total)",
    "boss-1": "apples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)",
}

SEARCHLANDS_CODES = {
    "s-1": "for c in cards:\n    x = range(5)\n    if cards:\n        print(c)",
    "s-2": "count = 0\nfor item in items:\n    if item == target:\n        count += 1",
    "s-3": "n items = len(items)\nall n = all(checks)\nn checks = sum(checks)",
    "s-boss": "for i in range(10):\n    if i == 5:\n        break",
}


@pytest.fixture
async def test_user():
    email = "manual-b1@example.com"
    user_id = "manual-b1-user"
    try:
        await users_collection().delete_many({"email": email})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": user_id})
    except Exception:
        pass

    r = client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "Manual B1 Test", "password": "SecurePass123!"},
    )
    assert r.status_code == 200, f"Register failed: {r.text}"
    body = r.json()
    token = body["token"]
    user_id = body["user"]["id"]

    yield {"token": token, "user_id": user_id}

    try:
        await users_collection().delete_many({"email": email})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": user_id})
    except Exception:
        pass


def test_b1_code_step_submission(test_user):
    # Complete foundations first to unlock searchlands
    for lvl_id, code in FOUNDATIONS_CODES.items():
        r = client.post(
            f"/api/v1/worlds/foundations/levels/{lvl_id}/complete",
            headers={"Authorization": f"Bearer {test_user['token']}"},
            json={"code": code, "language": "python", "time_spent_seconds": 0},
        )
        assert r.status_code == 200, f"Complete foundations/{lvl_id} failed: {r.text}"

    # Complete searchlands linear town to unlock binary town
    for lvl_id, code in SEARCHLANDS_CODES.items():
        r = client.post(
            f"/api/v1/worlds/searchlands/levels/{lvl_id}/complete",
            headers={"Authorization": f"Bearer {test_user['token']}"},
            json={"code": code, "language": "python", "time_spent_seconds": 0},
        )
        assert r.status_code == 200, f"Complete searchlands/{lvl_id} failed: {r.text}"

    code = """books = ['Ant','Bear','Cat','Dragon','Eagle','Fox','Goat','Hawk']
target = 'Dragon'
lo, hi = 0, len(books)-1
while lo <= hi:
    mid = (lo+hi)//2
    if books[mid] == target: print(mid); break
    elif books[mid] < target: lo = mid+1
    else: hi = mid-1
"""
    r = client.post(
        "/api/v1/worlds/searchlands/levels/b-1/attempt",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"code": code, "language": "python", "time_spent_seconds": 0, "step_type": "code"},
    )
    print("B1 code status:", r.status_code)
    print("B1 code body:", r.json())
    assert r.status_code == 200
    body = r.json()
    assert "passed" in body


def test_b1_debug_step_submission(test_user):
    for lvl_id, code in FOUNDATIONS_CODES.items():
        r = client.post(
            f"/api/v1/worlds/foundations/levels/{lvl_id}/complete",
            headers={"Authorization": f"Bearer {test_user['token']}"},
            json={"code": code, "language": "python", "time_spent_seconds": 0},
        )
        assert r.status_code == 200, f"Complete foundations/{lvl_id} failed: {r.text}"

    for lvl_id, code in SEARCHLANDS_CODES.items():
        r = client.post(
            f"/api/v1/worlds/searchlands/levels/{lvl_id}/complete",
            headers={"Authorization": f"Bearer {test_user['token']}"},
            json={"code": code, "language": "python", "time_spent_seconds": 0},
        )
        assert r.status_code == 200, f"Complete searchlands/{lvl_id} failed: {r.text}"

    answer = """lo, hi = 0, len(books)-1
while lo <= hi:
    mid = (lo+hi)//2
    if books[mid] == target: return mid
    elif books[mid] < target: lo = mid+1
    else: hi = mid
return -1
"""
    r = client.post(
        "/api/v1/worlds/searchlands/levels/b-1/attempt",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"code": answer, "language": "python", "time_spent_seconds": 0, "step_type": "debug"},
    )
    print("B1 debug status:", r.status_code)
    print("B1 debug body:", r.json())
    assert r.status_code == 200
    body = r.json()
    assert "passed" in body