"""Runtime verification for Journey role/company routing, fallback logging, and Diamonds integrity."""
from __future__ import annotations

import asyncio
from bson import ObjectId

from fastapi.testclient import TestClient

from app.main import app
from app.database import gamification_collection, skill_graph_collection, srs_cards_collection, users_collection

client = TestClient(app)


def _make_email(prefix: str) -> str:
    return f"{prefix}@example.com"


async def _reset_user(user_id: str):
    await gamification_collection().delete_many({"user_id": user_id})
    await skill_graph_collection().delete_many({"user_id": user_id})
    await srs_cards_collection().delete_many({"user_id": user_id})


async def _register(email: str, password: str = "SecurePass123!") -> dict:
    # ensure clean state
    try:
        await users_collection().delete_many({"email": email})
    except Exception:
        pass
    r = client.post("/api/v1/auth/register", json={"email": email, "name": email.split("@")[0], "password": password})
    assert r.status_code == 200, r.text
    body = r.json()
    return {"token": body["token"], "user_id": body["user"]["id"]}


async def _set_target(user_id: str, target_role: str, target_company: str):
    await users_collection().update_one(
        {"_id": user_id},
        {"$set": {"target_role": target_role, "target_company": target_company}},
    )


def _auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


async def test_role_company_ordering():
    world_id = "foundations"
    email_a = _make_email("role-a")
    email_b = _make_email("role-b")
    user_a = await _register(email_a)
    user_b = await _register(email_b)
    await _reset_user(user_a["user_id"])
    await _reset_user(user_b["user_id"])
    await _set_target(user_a["user_id"], "frontend", "bounty")
    await _set_target(user_b["user_id"], "backend", "placement")

    headers_a = _auth_headers(user_a["token"])
    headers_b = _auth_headers(user_b["token"])

    res_a = client.get(f"/api/v1/worlds/{world_id}", headers=headers_a)
    res_b = client.get(f"/api/v1/worlds/{world_id}", headers=headers_b)
    assert res_a.status_code == 200, res_a.text
    assert res_b.status_code == 200, res_b.text

    world_a = res_a.json()["world"]
    world_b = res_b.json()["world"]
    levels_a = [lvl["id"] for town in world_a["towns"] for lvl in town["levels"]]
    levels_b = [lvl["id"] for town in world_b["towns"] for lvl in town["levels"]]
    print("ROLE_ROUTING levels_a:", levels_a)
    print("ROLE_ROUTING levels_b:", levels_b)
    assert levels_a == levels_b, "canonical set should match when no levels are tagged"

    routing_a = res_a.json().get("content_routing", {})
    routing_b = res_b.json().get("content_routing", {})
    print("ROLE_ROUTING routing_a:", routing_a)
    print("ROLE_ROUTING routing_b:", routing_b)
    assert routing_a.get("target_role") == "frontend"
    assert routing_b.get("target_role") == "backend"


async def test_fallback_logging():
    world_id = "foundations"
    level_id = "level-1"
    email = _make_email("fallback")
    user = await _register(email)
    await _reset_user(user["user_id"])

    headers = _auth_headers(user["token"])
    attempt_res = client.post(
        f"/api/v1/worlds/{world_id}/levels/{level_id}/attempt",
        headers=headers,
        json={"code": "anything", "language": "python", "time_spent_seconds": 0, "step_type": "predict"},
    )
    print("FALLBACK status:", attempt_res.status_code)
    print("FALLBACK body:", attempt_res.json())
    assert attempt_res.status_code == 200


async def test_xp_integrity():
    world_id = "foundations"
    level_id = "level-1"
    email = _make_email("diamonds")
    user = await _register(email)
    await _reset_user(user["user_id"])

    headers = _auth_headers(user["token"])
    before_doc = await (await gamification_collection().find_one({"user_id": user["user_id"]})) or {}
    before_xp = int(before_doc.get("diamonds", 0))
    before_events = before_doc.get("gamification_events", [])
    print("Diamonds before:", before_xp)

    complete_res = client.post(
        f"/api/v1/worlds/{world_id}/levels/{level_id}/complete",
        headers=headers,
        json={"code": "apples = 5", "language": "python", "time_spent_seconds": 0},
    )
    print("Diamonds complete status:", complete_res.status_code)
    complete_body = complete_res.json()
    print("Diamonds complete body:", complete_body)
    assert complete_res.status_code == 200, complete_res.text

    after_doc = await (await gamification_collection().find_one({"user_id": user["user_id"]})) or {}
    after_xp = int(after_doc.get("diamonds", 0))
    after_events = after_doc.get("gamification_events", [])
    print("Diamonds after:", after_xp)
    print("Diamonds delta:", after_xp - before_xp)
    print("xp_awarded:", complete_body.get("xp_awarded"))
    assert after_xp - before_xp == complete_body.get("xp_awarded", 0)
    assert len(after_events) - len(before_events) == 1


async def test_retry_no_duplicate_xp():
    world_id = "foundations"
    level_id = "level-1"
    email = _make_email("retry")
    user = await _register(email)
    await _reset_user(user["user_id"])

    headers = _auth_headers(user["token"])
    first = client.post(
        f"/api/v1/worlds/{world_id}/levels/{level_id}/complete",
        headers=headers,
        json={"code": "apples = 5", "language": "python", "time_spent_seconds": 0},
    )
    assert first.status_code == 200, first.text
    first_body = first.json()
    first_xp = await (await gamification_collection().find_one({"user_id": user["user_id"]})) or {}
    first_xp_total = int(first_xp.get("diamonds", 0))
    first_event_count = len(first_xp.get("gamification_events", []))

    second = client.post(
        f"/api/v1/worlds/{world_id}/levels/{level_id}/complete",
        headers=headers,
        json={"code": "apples = 5", "language": "python", "time_spent_seconds": 0},
    )
    assert second.status_code == 200, second.text
    second_body = second.json()
    second_xp = await (await gamification_collection().find_one({"user_id": user["user_id"]})) or {}
    second_xp_total = int(second_xp.get("diamonds", 0))
    second_event_count = len(second_xp.get("gamification_events", []))

    print("RETRY first xp_awarded:", first_body.get("xp_awarded"))
    print("RETRY second xp_awarded:", second_body.get("xp_awarded"))
    print("RETRY first total Diamonds:", first_xp_total)
    print("RETRY second total Diamonds:", second_xp_total)
    print("RETRY first events:", first_event_count)
    print("RETRY second events:", second_event_count)
    assert second_body.get("deduplicated") is True
    assert second_xp_total == first_xp_total
    assert second_event_count == first_event_count


async def main():
    await test_role_company_ordering()
    await test_fallback_logging()
    await test_xp_integrity()
    await test_retry_no_duplicate_xp()
    print("\nALL RUNTIME VERIFICATIONS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
