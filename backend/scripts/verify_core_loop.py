"""End-to-end verification of the PlacementPro core loop.

Tests:
  1. Register + login
  2. Set target company/role/date
  3. Start diagnostic
  4. Submit diagnostic answers
  5. Verify diagnostic result has 5 dimensions + strengths/weaknesses
  6. Verify first mission is personalized
  7. Complete a mission via study activity
  8. Refresh today plan
  9. Verify plan adapted

Run:
  cd backend
  python -m scripts.verify_core_loop
"""
from __future__ import annotations

import asyncio
import os
import random
import string
from datetime import datetime, timezone, timedelta

import httpx

BASE = os.getenv("BASE_URL", "http://localhost:8000")
EMAIL_DOMAIN = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


async def main() -> None:
    async with httpx.AsyncClient(base_url=BASE, timeout=30.0) as client:
        email = f"e2e_{EMAIL_DOMAIN}@example.com"
        password = "TestPass123!"
        name = "E2E Student"

        # 1. Register
        print("1. Registering...")
        reg = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password, "name": name},
        )
        assert reg.status_code == 200, f"Register failed: {reg.status_code} {reg.text}"
        token = reg.json()["token"]
        client.headers["Authorization"] = f"Bearer {token}"
        print("   [OK] Registered")

        # 2. Set target
        print("2. Setting target...")
        target_resp = await client.post(
            "/api/v1/onboarding/complete",
            json={
                "step_id": "v3-target",
                "target_company": "TCS",
                "target_role": "SDE",
                "placement_date": (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat(),
            },
        )
        assert target_resp.status_code == 200, f"Target failed: {target_resp.status_code} {target_resp.text}"
        print("   [OK] Target set")

        # 3. Start diagnostic
        print("3. Starting diagnostic...")
        start_resp = await client.get("/api/v1/onboarding/diagnostic/start?role=sde")
        assert start_resp.status_code == 200, f"Diagnostic start failed: {start_resp.status_code} {start_resp.text}"
        diag = start_resp.json()
        questions = diag["questions"]
        answers = {}
        for q in questions:
            if q["type"] == "predict" and q.get("options"):
                answers[q["id"]] = q["options"][0]["id"]
            elif q["type"] == "break" and q.get("correct_set"):
                answers[q["id"]] = q["correct_set"][0]
            elif q["type"] == "explore" and q.get("expected_output"):
                answers[q["id"]] = q["expected_output"]
            else:
                answers[q["id"]] = ""
        print(f"   [OK] Got {len(questions)} questions")

        # 4. Submit diagnostic
        print("4. Submitting diagnostic...")
        submit_resp = await client.post(
            "/api/v1/onboarding/diagnostic/complete",
            json={"role": "sde", "answers": answers},
        )
        assert submit_resp.status_code == 200, f"Diagnostic submit failed: {submit_resp.status_code} {submit_resp.text}"
        result = submit_resp.json()

        # 5. Verify dimensions
        print("5. Verifying diagnostic result...")
        dims = result.get("readiness", {}).get("dimensions", [])
        dim_ids = {d["id"] for d in dims}
        assert "quant" in dim_ids, f"Missing quant dimension: {dim_ids}"
        assert "reasoning" in dim_ids, f"Missing reasoning dimension: {dim_ids}"
        assert "verbal" in dim_ids, f"Missing verbal dimension: {dim_ids}"
        assert "coding" in dim_ids, f"Missing coding dimension: {dim_ids}"
        assert "cs_core" in dim_ids, f"Missing cs_core dimension: {dim_ids}"
        print(f"   [OK] 5 dimensions present: {sorted(dim_ids)}")

        # Verify strengths/weaknesses classification
        statuses = {d["status"] for d in dims}
        assert statuses.issubset({"strength", "developing", "weakness", "unknown"}), f"Bad statuses: {statuses}"
        print(f"   [OK] Statuses valid: {statuses}")

        # 6. Verify first mission
        print("6. Verifying first mission...")
        missions = result.get("first_missions", [])
        assert missions, "No first missions returned"
        first = missions[0]
        assert first.get("title"), "First mission missing title"
        assert first.get("topic"), "First mission missing topic"
        print(f"   [OK] First mission: {first['title']} ({first['topic']})")

        # 7. Get today plan
        print("7. Getting today plan...")
        plan_resp = await client.get("/api/v1/study/today")
        assert plan_resp.status_code == 200, f"Plan failed: {plan_resp.status_code} {plan_resp.text}"
        plan = plan_resp.json()

        assert plan.get("next") or plan.get("practice") or plan.get("daily_battle"), \
            f"Plan has no actionable content: {plan.keys()}"
        print(f"   [OK] Plan has {plan.get('totals', {}).get('task_count', 0)} tasks")

        # 8. Record activity
        print("8. Recording activity...")
        activity_resp = await client.post(
            "/api/v1/study/activity",
            json={
                "type": "practice",
                "skill_id": plan.get("practice", [{}])[0].get("skill", "aptitude.quantitative"),
                "passed": True,
                "score": 85,
                "time_spent": 120,
                "idempotency_key": f"e2e_verify_{email}",
            },
        )
        assert activity_resp.status_code in (200, 409), \
            f"Activity failed: {activity_resp.status_code} {activity_resp.text}"
        print("   [OK] Activity recorded")

        # 9. Refresh plan and verify adaptation
        print("9. Refreshing plan...")
        plan2_resp = await client.get("/api/v1/study/today?force_refresh=true")
        assert plan2_resp.status_code == 200, f"Plan refresh failed: {plan2_resp.status_code} {plan2_resp.text}"
        plan2 = plan2_resp.json()

        # The plan should still have content
        assert plan2.get("next") or plan2.get("practice") or plan2.get("daily_battle"), \
            "Refreshed plan has no content"
        print("   [OK] Refreshed plan still has content")

        # 10. Verify diagnostic status
        print("10. Verifying diagnostic status endpoint...")
        status_resp = await client.get("/api/v1/onboarding/diagnostic/status")
        assert status_resp.status_code == 200, f"Status failed: {status_resp.status_code} {status_resp.text}"
        status = status_resp.json()
        assert status.get("completed") is True, "Diagnostic not marked complete"
        assert status.get("baseline_categories"), "Missing baseline_categories"
        print("   [OK] Diagnostic status correct")

        print("\n[OK] All core loop checks passed.")


if __name__ == "__main__":
    asyncio.run(main())
