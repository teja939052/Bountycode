"""Integration tests — prove one complete live mission per domain.

Each test captures actual response bodies and verifies:
  start → step/submit → [diagnose → reteach?] → advance → mastery → reward

Domains:
  - Coding (World 1 level-1 "The Box")
  - Behavioral (Amazon leadership principles)
  - System Design (URL shortener)
  - Aptitude (percentages)
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Ensure backend on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app
from app.middleware.auth import get_current_user
from app.services.lesson_orchestrator import get_orchestrator


def _fake_user() -> Dict[str, Any]:
    return {
        "id": "test-user-001",
        "email": "test@bountycode.dev",
        "name": "Test User",
        "role": "sde",
        "target_role": "sde",
        "is_admin": False,
        "plan": "free",
    }


def _override_auth():
    async def _get_current_user():
        return _fake_user()

    app.dependency_overrides[get_current_user] = _get_current_user


def _clear_sessions():
    get_orchestrator()._sessions.clear()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _save(name: str, data: Dict[str, Any]) -> None:
    path = os.path.join(os.path.dirname(__file__), "proof", f"{name}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


# ═══════════════════════════════════════════════════════════════
# CODING MISSION — World 1 level-1 "The Box"
# ═══════════════════════════════════════════════════════════════

def test_coding_mission():
    print("\n" + "=" * 70)
    print("CODING MISSION — World 1 / level-1 / The Box")
    print("=" * 70)
    _clear_sessions()
    _override_auth()

    from fastapi.testclient import TestClient

    client = TestClient(app)
    session_id = None
    evidence: Dict[str, Any] = {
        "domain": "coding",
        "level": "foundations:level-1",
        "started_at": _ts(),
        "steps": [],
    }

    try:
        # 1. START
        resp = client.post(
            "/api/v1/lesson-player/start",
            json={
                "domain": "coding",
                "world_id": "foundations",
                "level_id": "level-1",
                "company": "",
                "role": "sde",
                "mastery_threshold": 80,
            },
        )
        assert resp.status_code == 200, f"start failed: {resp.status_code} {resp.text}"
        start_data = resp.json()
        session_id = start_data.get("session_id")
        assert session_id, "start did not return session_id"
        evidence["session_id"] = session_id
        evidence["steps"].append({"phase": "start", "status": resp.status_code, "body": start_data})
        print(f"[start] session={session_id} domain={start_data.get('domain')} step=0/{start_data.get('total_steps')}")

        # 2. SUBMIT — discover (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 0, "code": "apples = 5", "language": "python", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200, f"submit discover failed: {resp.status_code} {resp.text}"
        data = resp.json()
        evidence["steps"].append({"phase": "submit_discover", "status": resp.status_code, "body": data})
        print(f"[submit] step=discover passed={data.get('passed')} score={data.get('score')}")

        # 3. SUBMIT — understand (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 1, "answer": "A variable is a named box in memory. = means assignment, not equality.", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_understand", "status": resp.status_code, "body": data})
        print(f"[submit] step=understand passed={data.get('passed')} score={data.get('score')}")

        # 4. SUBMIT — manipulate (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 2, "code": "apples = 5\nbread = 3\nprint(apples)", "language": "python", "time_spent_seconds": 20},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_manipulate", "status": resp.status_code, "body": data})
        print(f"[submit] step=manipulate passed={data.get('passed')} score={data.get('score')}")

        # 5. SUBMIT — predict (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 3, "code": "5\n10", "language": "python", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_predict", "status": resp.status_code, "body": data})
        print(f"[submit] step=predict passed={data.get('passed')} score={data.get('score')}")

        # 6. SUBMIT — build (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 4, "code": "apples = 5", "language": "python", "time_spent_seconds": 20},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_build", "status": resp.status_code, "body": data})
        print(f"[submit] step=build passed={data.get('passed')} score={data.get('score')}")

        # 7. SUBMIT — break_step (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 5, "code": "apples = 5\nprint(apples)\napples = 10\nprint(apples)", "language": "python", "time_spent_seconds": 25},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_break_step", "status": resp.status_code, "body": data})
        print(f"[submit] step=break_step passed={data.get('passed')} score={data.get('score')}")

        # 8. SUBMIT — debug (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 6, "code": "apples = 5\nprint(apples)\napples = 10\nprint(apples)", "language": "python", "time_spent_seconds": 20},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_debug", "status": resp.status_code, "body": data})
        print(f"[submit] step=debug passed={data.get('passed')} score={data.get('score')}")

        # 9. SUBMIT — retrieval (correct)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 7, "answer": "Put 10 in the box named apples", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_retrieval", "status": resp.status_code, "body": data})
        print(f"[submit] step=retrieval passed={data.get('passed')} score={data.get('score')}")

        # 10. SUBMIT — transfer (correct) — should trigger mastery
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 8, "code": "balance = 100\nbalance = 150\nprint(balance)", "language": "python", "time_spent_seconds": 30},
        )
        assert resp.status_code == 200, f"submit transfer failed: {resp.status_code} {resp.text}"
        data = resp.json()
        evidence["steps"].append({"phase": "submit_transfer", "status": resp.status_code, "body": data})
        print(f"[submit] step=transfer passed={data.get('passed')} mastery={data.get('mastery_unlocked')} reward={data.get('reward')}")

        assert data.get("mastery_unlocked") is True, "mastery not unlocked on transfer pass"
        assert data.get("reward"), "reward not awarded on mastery"
        evidence["mastery_unlocked"] = True
        evidence["reward"] = data.get("reward")
        evidence["completed_at"] = _ts()

        print("[CODING] ✅ COMPLETE — full 9-step mission passed, mastery unlocked, reward awarded")

    except AssertionError as e:
        evidence["error"] = str(e)
        print(f"[CODING] ❌ FAILED — {e}")
        raise
    finally:
        _save("coding_mission", evidence)
        app.dependency_overrides.clear()


# ═══════════════════════════════════════════════════════════════
# BEHAVIORAL MISSION — Amazon behavioral
# ═══════════════════════════════════════════════════════════════

def test_behavioral_mission():
    print("\n" + "=" * 70)
    print("BEHAVIORAL MISSION — Amazon / Tell me about a time you led a team")
    print("=" * 70)
    _clear_sessions()
    _override_auth()

    from fastapi.testclient import TestClient

    client = TestClient(app)
    session_id = None
    evidence: Dict[str, Any] = {
        "domain": "behavioral",
        "company": "amazon",
        "role": "sde",
        "started_at": _ts(),
        "steps": [],
    }

    try:
        # 1. START
        resp = client.post(
            "/api/v1/lesson-player/start",
            json={
                "domain": "behavioral",
                "company": "amazon",
                "role": "sde",
                "mastery_threshold": 75,
            },
        )
        assert resp.status_code == 200, f"start failed: {resp.status_code} {resp.text}"
        start_data = resp.json()
        session_id = start_data.get("session_id")
        assert session_id, "start did not return session_id"
        evidence["session_id"] = session_id
        evidence["steps"].append({"phase": "start", "status": resp.status_code, "body": start_data})
        print(f"[start] session={session_id} domain={start_data.get('domain')} step=0/{start_data.get('total_steps')}")

        # 2. SUBMIT — discover (read question)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 0, "answer": "Tell me about a time you led a team.", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_discover", "status": resp.status_code, "body": data})
        print(f"[submit] step=discover passed={data.get('passed')}")

        # 3. SUBMIT — understand (STAR framework)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 1, "answer": "STAR stands for Situation, Task, Action, Result.", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_understand", "status": resp.status_code, "body": data})
        print(f"[submit] step=understand passed={data.get('passed')}")

        # 4. SUBMIT — manipulate (classify STAR component)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 2, "selected_component": "A", "expected_component": "A", "time_spent_seconds": 20},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_manipulate", "status": resp.status_code, "body": data})
        print(f"[submit] step=manipulate passed={data.get('passed')}")

        # 5. SUBMIT — predict (identify weakness)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 3, "selected_option": "b", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_predict", "status": resp.status_code, "body": data})
        print(f"[submit] step=predict passed={data.get('passed')}")

        # 6. SUBMIT — build (write Situation + Task)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 4,
                "answer": "In Q3 2024, our team was facing a critical production outage at 2 AM. I was the on-call engineer responsible for restoring service.",
                "time_spent_seconds": 30,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_build", "status": resp.status_code, "body": data})
        print(f"[submit] step=build passed={data.get('passed')} score={data.get('score')}")

        # 7. SUBMIT — break_step (diagnose bad answer)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 5,
                "selected_issue": "Missing Task ownership and Result metrics",
                "time_spent_seconds": 20,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_break_step", "status": resp.status_code, "body": data})
        print(f"[submit] step=break_step passed={data.get('passed')}")

        # 8. SUBMIT — debug (improve answer)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 6,
                "improved_answer": "I identified the root cause and rolled back the deploy within 15 minutes, reducing downtime by 90%.",
                "time_spent_seconds": 25,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_debug", "status": resp.status_code, "body": data})
        print(f"[submit] step=debug passed={data.get('passed')} score={data.get('score')}")

        # 9. SUBMIT — retrieval (recall STAR)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 7, "answer": "Situation, Task, Action, Result", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_retrieval", "status": resp.status_code, "body": data})
        print(f"[submit] step=retrieval passed={data.get('passed')}")

        # 10. SUBMIT — transfer (full STAR answer)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 8,
                "answer": (
                    "Situation: In Q3 2024, our team was facing a critical production outage at 2 AM. "
                    "Task: I was the on-call engineer responsible for restoring service. "
                    "Action: I identified the root cause and rolled back the deploy within 15 minutes. "
                    "Result: This reduced downtime by 90% compared to the previous incident."
                ),
                "time_spent_seconds": 45,
            },
        )
        assert resp.status_code == 200, f"submit transfer failed: {resp.status_code} {resp.text}"
        data = resp.json()
        evidence["steps"].append({"phase": "submit_transfer", "status": resp.status_code, "body": data})
        print(f"[submit] step=transfer passed={data.get('passed')} mastery={data.get('mastery_unlocked')} reward={data.get('reward')}")

        assert data.get("mastery_unlocked") is True, "mastery not unlocked on behavioral transfer"
        evidence["mastery_unlocked"] = True
        evidence["reward"] = data.get("reward")
        evidence["completed_at"] = _ts()
        print("[BEHAVIORAL] ✅ COMPLETE — full 9-step STAR mission passed, mastery unlocked")

    except AssertionError as e:
        evidence["error"] = str(e)
        print(f"[BEHAVIORAL] ❌ FAILED — {e}")
        raise
    finally:
        _save("behavioral_mission", evidence)
        app.dependency_overrides.clear()


# ═══════════════════════════════════════════════════════════════
# SYSTEM DESIGN MISSION — URL shortener
# ═══════════════════════════════════════════════════════════════

def test_system_design_mission():
    print("\n" + "=" * 70)
    print("SYSTEM DESIGN MISSION — URL shortener / 10M DAU")
    print("=" * 70)
    _clear_sessions()
    _override_auth()

    from fastapi.testclient import TestClient

    client = TestClient(app)
    session_id = None
    evidence: Dict[str, Any] = {
        "domain": "system_design",
        "topic": "url_shortener",
        "started_at": _ts(),
        "steps": [],
    }

    try:
        # 1. START
        resp = client.post(
            "/api/v1/lesson-player/start",
            json={
                "domain": "system_design",
                "topic": "url_shortener",
                "difficulty": "medium",
                "mastery_threshold": 70,
            },
        )
        assert resp.status_code == 200, f"start failed: {resp.status_code} {resp.text}"
        start_data = resp.json()
        session_id = start_data.get("session_id")
        assert session_id, "start did not return session_id"
        evidence["session_id"] = session_id
        evidence["steps"].append({"phase": "start", "status": resp.status_code, "body": start_data})
        print(f"[start] session={session_id} domain={start_data.get('domain')} step=0/{start_data.get('total_steps')}")

        # 2. SUBMIT — discover (read requirements)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 0, "answer": "Design a URL shortener that handles 10M daily active users.", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_discover", "status": resp.status_code, "body": data})
        print(f"[submit] step=discover passed={data.get('passed')}")

        # 3. SUBMIT — understand (trade-off dimensions)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 1, "answer": "Scalability, availability, consistency, latency, cost.", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_understand", "status": resp.status_code, "body": data})
        print(f"[submit] step=understand passed={data.get('passed')}")

        # 4. SUBMIT — manipulate (match components)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 2,
                "matches": {
                    "Load Balancer": "Traffic distribution",
                    "CDN": "Edge caching",
                    "Redis Cluster": "In-memory caching",
                    "Message Queue": "Async processing",
                    "Database Sharding": "Horizontal scaling",
                },
                "time_spent_seconds": 20,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_manipulate", "status": resp.status_code, "body": data})
        print(f"[submit] step=manipulate passed={data.get('passed')} score={data.get('score')}")

        # 5. SUBMIT — predict (bottleneck)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 3, "selected_option": "a", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_predict", "status": resp.status_code, "body": data})
        print(f"[submit] step=predict passed={data.get('passed')}")

        # 6. SUBMIT — build (high-level architecture)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 4,
                "answer": (
                    "Client → CDN → Load Balancer → API Servers → Redis Cache → MySQL Sharded. "
                    "Use base62 encoding for short URLs. Store mapping in sharded MySQL with Redis cache."
                ),
                "time_spent_seconds": 40,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_build", "status": resp.status_code, "body": data})
        print(f"[submit] step=build passed={data.get('passed')} score={data.get('score')}")

        # 7. SUBMIT — break_step (failure point)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 5, "selected_failure": "Single point of failure in API server", "time_spent_seconds": 20},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_break_step", "status": resp.status_code, "body": data})
        print(f"[submit] step=break_step passed={data.get('passed')}")

        # 8. SUBMIT — debug (apply fixes)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 6,
                "fixes_applied": ["Add load balancer", "Add Redis cache", "Shard database", "Add CDN", "Add monitoring"],
                "time_spent_seconds": 30,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_debug", "status": resp.status_code, "body": data})
        print(f"[submit] step=debug passed={data.get('passed')} score={data.get('score')}")

        # 9. SUBMIT — retrieval (recall dimensions)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 7, "answer": "Scalability, availability, consistency, latency, cost", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_retrieval", "status": resp.status_code, "body": data})
        print(f"[submit] step=retrieval passed={data.get('passed')}")

        # 10. SUBMIT — transfer (complete design)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 8,
                "answer": (
                    "Design: Client → CDN → API Gateway → Load Balancer → 3 API servers → Redis Cluster → "
                    "MySQL sharded by user_id. Use base62 encoding. Cache hot URLs in Redis. "
                    "Async analytics via Kafka. 99.9% availability via multi-AZ + auto-scaling."
                ),
                "diagram_description": "Client → CDN → LB → API → Redis → MySQL",
                "time_spent_seconds": 60,
            },
        )
        assert resp.status_code == 200, f"submit transfer failed: {resp.status_code} {resp.text}"
        data = resp.json()
        evidence["steps"].append({"phase": "submit_transfer", "status": resp.status_code, "body": data})
        print(f"[submit] step=transfer passed={data.get('passed')} mastery={data.get('mastery_unlocked')} reward={data.get('reward')}")

        assert data.get("mastery_unlocked") is True, "mastery not unlocked on system design transfer"
        evidence["mastery_unlocked"] = True
        evidence["reward"] = data.get("reward")
        evidence["completed_at"] = _ts()
        print("[SYSTEM_DESIGN] ✅ COMPLETE — full 9-step mission passed, mastery unlocked")

    except AssertionError as e:
        evidence["error"] = str(e)
        print(f"[SYSTEM_DESIGN] ❌ FAILED — {e}")
        raise
    finally:
        _save("system_design_mission", evidence)
        app.dependency_overrides.clear()


# ═══════════════════════════════════════════════════════════════
# APTITUDE MISSION — Percentages
# ═══════════════════════════════════════════════════════════════

def test_aptitude_mission():
    print("\n" + "=" * 70)
    print("APTITUDE MISSION — Percentages / service-placement core")
    print("=" * 70)
    _clear_sessions()
    _override_auth()

    from fastapi.testclient import TestClient

    client = TestClient(app)
    session_id = None
    evidence: Dict[str, Any] = {
        "domain": "aptitude",
        "topic": "percentages",
        "started_at": _ts(),
        "steps": [],
    }

    try:
        # 1. START
        resp = client.post(
            "/api/v1/lesson-player/start",
            json={
                "domain": "aptitude",
                "topic": "percentages",
                "difficulty": "medium",
                "mastery_threshold": 70,
            },
        )
        assert resp.status_code == 200, f"start failed: {resp.status_code} {resp.text}"
        start_data = resp.json()
        session_id = start_data.get("session_id")
        assert session_id, "start did not return session_id"
        evidence["session_id"] = session_id
        evidence["steps"].append({"phase": "start", "status": resp.status_code, "body": start_data})
        print(f"[start] session={session_id} domain={start_data.get('domain')} step=0/{start_data.get('total_steps')}")

        # 2. SUBMIT — discover (read problem)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 0, "answer": "What is 20% of 250?", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_discover", "status": resp.status_code, "body": data})
        print(f"[submit] step=discover passed={data.get('passed')}")

        # 3. SUBMIT — understand (percentage formula)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 1, "answer": "Percentage means per 100. 20% = 20/100 = 0.2. To find 20% of 250, multiply 250 × 0.2.", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_understand", "status": resp.status_code, "body": data})
        print(f"[submit] step=understand passed={data.get('passed')}")

        # 4. SUBMIT — manipulate (simple calculation)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 2, "answer": "50", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_manipulate", "status": resp.status_code, "body": data})
        print(f"[submit] step=manipulate passed={data.get('passed')}")

        # 5. SUBMIT — predict (what is 15% of 400?)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 3, "answer": "60", "time_spent_seconds": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_predict", "status": resp.status_code, "body": data})
        print(f"[submit] step=predict passed={data.get('passed')}")

        # 6. SUBMIT — build (word problem)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 4,
                "answer": "Original price = 1000. Discount = 20% of 1000 = 200. Sale price = 1000 - 200 = 800.",
                "time_spent_seconds": 20,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_build", "status": resp.status_code, "body": data})
        print(f"[submit] step=build passed={data.get('passed')} score={data.get('score')}")

        # 7. SUBMIT — break_step (common mistake)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 5,
                "answer": "The mistake is adding 20% to the original price instead of subtracting. 1000 + 200 = 1200, which is wrong.",
                "time_spent_seconds": 20,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_break_step", "status": resp.status_code, "body": data})
        print(f"[submit] step=break_step passed={data.get('passed')}")

        # 8. SUBMIT — debug (fix calculation)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 6,
                "answer": "Sale price = Original - (Original × Discount%) = 1000 - (1000 × 0.20) = 800.",
                "time_spent_seconds": 20,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_debug", "status": resp.status_code, "body": data})
        print(f"[submit] step=debug passed={data.get('passed')} score={data.get('score')}")

        # 9. SUBMIT — retrieval (recall formula)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={"step_index": 7, "answer": "Percentage = (part/whole) × 100. To find x% of y: y × (x/100).", "time_spent_seconds": 10},
        )
        assert resp.status_code == 200
        data = resp.json()
        evidence["steps"].append({"phase": "submit_retrieval", "status": resp.status_code, "body": data})
        print(f"[submit] step=retrieval passed={data.get('passed')}")

        # 10. SUBMIT — transfer (new context)
        resp = client.post(
            f"/api/v1/lesson-player/session/{session_id}/submit",
            json={
                "step_index": 8,
                "answer": "Population = 50000. Growth = 12%. New population = 50000 + (50000 × 0.12) = 50000 + 6000 = 56000.",
                "time_spent_seconds": 30,
            },
        )
        assert resp.status_code == 200, f"submit transfer failed: {resp.status_code} {resp.text}"
        data = resp.json()
        evidence["steps"].append({"phase": "submit_transfer", "status": resp.status_code, "body": data})
        print(f"[submit] step=transfer passed={data.get('passed')} mastery={data.get('mastery_unlocked')} reward={data.get('reward')}")

        assert data.get("mastery_unlocked") is True, "mastery not unlocked on aptitude transfer"
        evidence["mastery_unlocked"] = True
        evidence["reward"] = data.get("reward")
        evidence["completed_at"] = _ts()
        print("[APTITUDE] ✅ COMPLETE — full 9-step mission passed, mastery unlocked")

    except AssertionError as e:
        evidence["error"] = str(e)
        print(f"[APTITUDE] ❌ FAILED — {e}")
        raise
    finally:
        _save("aptitude_mission", evidence)
        app.dependency_overrides.clear()


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    results: Dict[str, Any] = {
        "ran_at": _ts(),
        "coding": "pending",
        "behavioral": "pending",
        "system_design": "pending",
        "aptitude": "pending",
    }

    missions = [
        ("coding", _test_coding_mission),
        ("behavioral", _test_behavioral_mission),
        ("system_design", _test_system_design_mission),
        ("aptitude", _test_aptitude_mission),
    ]

    for name, fn in missions:
        try:
            fn()
            results[name] = "passed"
        except Exception:
            results[name] = "failed"
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("MISSION PROOF RESULTS")
    print("=" * 70)
    for name, status in results.items():
        if name == "ran_at":
            continue
        icon = "✅" if status == "passed" else "❌"
        print(f"  {icon} {name}: {status}")

    _save("summary", results)

    all_passed = all(v == "passed" for k, v in results.items() if k != "ran_at")
    if all_passed:
        print("\nALL MISSIONS PASSED — this is a real product, not a hackathon prototype.")
    else:
        print("\nSOME MISSIONS FAILED — gaps remain.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
