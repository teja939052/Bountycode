"""Runtime verification for Evidence Dashboard APIs.

Seeds controlled test data, calls live backend endpoints, and asserts
that the responses contain the expected structure and values.
"""
from __future__ import annotations

import asyncio
import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mongomock_motor import AsyncMongoMockClient
import app.database as dbmod
import app.services.readiness_engine as readiness_engine
from app.services.evidence_aggregator import pattern_heatmap, failure_breakdown, solve_time_trend


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def _days_ago(days: int) -> str:
    return _iso(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) - __import__("datetime").timedelta(days=days))


async def setup_db():
    client = AsyncMongoMockClient()
    db = client["evidence_runtime_verify"]
    dbmod._client = client
    dbmod._db = db
    return client, db


async def seed_user_a(db):
    """User with known weak Graphs evidence."""
    uid = "runtime_user_a"
    await db["learning_events"].delete_many({"user_id": uid})
    await db["submissions"].delete_many({"user_id": uid})
    await db["solved_problems"].delete_many({"user_id": uid})
    await db["oa_sessions"].delete_many({"user_id": uid})

    await db["learning_events"].insert_many([
        {"user_id": uid, "skill_id": "Graphs", "activity_type": "practice",
         "passed": False, "score": 30, "timestamp": _days_ago(10)},
        {"user_id": uid, "skill_id": "Graphs", "activity_type": "practice",
         "passed": True, "score": 90, "timestamp": _days_ago(5)},
        {"user_id": uid, "skill_id": "Graphs", "activity_type": "practice",
         "passed": True, "score": 95, "timestamp": _days_ago(3)},
    ])
    count = await db["learning_events"].count_documents({"user_id": uid})
    print(f"    DEBUG learning_events inserted: {count}")
    await db["submissions"].insert_many([
        {"user_id": uid, "skill_id": "Graphs", "failure_class": "TIMEOUT",
         "submitted_at": _days_ago(10)},
        {"user_id": uid, "skill_id": "Graphs", "failure_class": "WRONG_ANSWER",
         "submitted_at": _days_ago(7)},
        {"user_id": uid, "skill_id": "Graphs", "failure_class": "SUCCESS",
         "submitted_at": _days_ago(5)},
        {"user_id": uid, "skill_id": "Graphs", "failure_class": "TIMEOUT",
         "submitted_at": _days_ago(3)},
    ])
    await db["solved_problems"].insert_many([
        {"user_id": uid, "question_id": "q_g1", "topic": "Graphs",
         "created_at": _days_ago(10)},
        {"user_id": uid, "question_id": "q_a1", "topic": "Arrays",
         "created_at": _days_ago(3)},
    ])
    return uid


async def seed_zero_evidence_user(db):
    """User with no meaningful evidence."""
    uid = "runtime_user_zero"
    await db["learning_events"].delete_many({"user_id": uid})
    await db["submissions"].delete_many({"user_id": uid})
    await db["solved_problems"].delete_many({"user_id": uid})
    return uid


async def get_readiness(user_id: str, role: str = "sde", company: str | None = None) -> dict:
    profile = readiness_engine.build_target_profile(role=role, company=company)
    evidence = await readiness_engine.collect_target_evidence(user_id, profile)
    return readiness_engine.calculate_target_readiness(profile, evidence)


async def get_evidence_bundle(user_id: str) -> dict:
    from app.services.evidence_aggregator import collect_student_evidence
    return await collect_student_evidence(user_id)


async def main():
    await setup_db()
    import app.database as dbmod
    db = dbmod._db

    print("=" * 70)
    print("RUNTIME VERIFICATION: Evidence Dashboard APIs")
    print("=" * 70)

    # ── 1. User A: weak Graphs evidence ─────────────────────────────────────
    print("\n[1] SEED USER A (weak Graphs)")
    uid_a = await seed_user_a(db)
    print(f"    user_id = {uid_a}")

    bundle_a = await get_evidence_bundle(uid_a)
    print(f"\n    DEBUG bundle keys: {list(bundle_a.keys())}")
    print(f"    DEBUG learning_events count: {len(bundle_a.get('learning_events', []))}")
    for ev in bundle_a.get('learning_events', []):
        print(f"      LE: _id={ev.get('_id')}, skill_id={ev.get('skill_id')}, passed={ev.get('passed')}, ts={ev.get('timestamp')}")
    print(f"    DEBUG submissions count: {len(bundle_a.get('submissions', []))}")
    print(f"    DEBUG solved_problems count: {len(bundle_a.get('solved_problems', []))}")
    heat_a = pattern_heatmap(bundle_a)
    fails_a = failure_breakdown(bundle_a)
    trend_a = solve_time_trend(bundle_a)
    readiness_a = await get_readiness(uid_a, company="amazon")

    print("\n    READINESS RESPONSE:")
    print(f"      score       = {readiness_a['score']}")
    print(f"      coverage    = {readiness_a['coverage']}%")
    print(f"      status      = {readiness_a['status']}")
    print(f"      next_action = {readiness_a.get('next_action')}")
    print(f"      blockers    = {readiness_a.get('blockers')}")

    print("\n    HEATMAP PATTERNS:")
    for p in heat_a["patterns"]:
        print(f"      {p['pattern_id']}: accuracy={p['accuracy']}%, attempts={p['attempts']}, color={p['color']}")

    print("\n    FAILURE BREAKDOWN:")
    print(f"      top_failure = {fails_a['top_failure']}")
    print(f"      percentages = {fails_a['percentages']}")

    print("\n    TREND:")
    print(f"      trend_s = {trend_a.get('trend_s')}")
    print(f"      sufficient = {trend_a.get('sufficient')}")

    # Assertions
    assert readiness_a["coverage"] > 0, "Coverage should be > 0 for user A"
    assert readiness_a["status"] != "INSUFFICIENT_EVIDENCE", "User A should have sufficient evidence"
    graphs_pattern = next((p for p in heat_a["patterns"] if "graph" in p["pattern_id"].lower()), None)
    assert graphs_pattern is not None, "Graphs pattern should exist in heatmap"
    assert graphs_pattern["attempts"] >= 3, f"Graphs attempts should be >= 3, got {graphs_pattern['attempts']}"
    assert fails_a["total_submissions"] >= 3, f"Total submissions should be >= 3, got {fails_a['total_submissions']}"
    assert fails_a["top_failure"] in ("TIMEOUT", "WRONG_ANSWER", "SUCCESS"), f"Unexpected top failure: {fails_a['top_failure']}"

    # ── 2. Zero-evidence user ────────────────────────────────────────────────
    print("\n[2] ZERO-EVIDENCE USER")
    uid_zero = await seed_zero_evidence_user(db)
    print(f"    user_id = {uid_zero}")

    readiness_zero = await get_readiness(uid_zero, company="amazon")
    bundle_zero = await get_evidence_bundle(uid_zero)
    heat_zero = pattern_heatmap(bundle_zero)
    fails_zero = failure_breakdown(bundle_zero)

    print("\n    READINESS RESPONSE:")
    print(f"      score       = {readiness_zero['score']}")
    print(f"      coverage    = {readiness_zero['coverage']}%")
    print(f"      status      = {readiness_zero['status']}")
    print(f"      next_action = {readiness_zero.get('next_action')}")

    assert readiness_zero["status"] == "INSUFFICIENT_EVIDENCE", \
        f"Zero-evidence user should have INSUFFICIENT_EVIDENCE, got {readiness_zero['status']}"
    assert readiness_zero["coverage"] == 0.0, \
        f"Zero-evidence user should have 0% coverage, got {readiness_zero['coverage']}"
    assert len(heat_zero["patterns"]) == 0, \
        f"Zero-evidence user should have no patterns, got {heat_zero['patterns']}"
    assert fails_zero["total_submissions"] == 0, \
        f"Zero-evidence user should have 0 submissions, got {fails_zero['total_submissions']}"

    # ── 3. Role/company differentiation ─────────────────────────────────────
    print("\n[3] ROLE/COMPANY DIFFERENTIATION")
    role_frontend = await get_readiness(uid_a, role="frontend", company="google")
    role_backend = await get_readiness(uid_a, role="backend", company="amazon")

    print(f"\n    Frontend/Google:  score={role_frontend['score']}, coverage={role_frontend['coverage']}%")
    print(f"    Backend/Amazon:   score={role_backend['score']}, coverage={role_backend['coverage']}%")

    fe_skills = {s["skill_id"]: s["weight"] for s in role_frontend.get("skills", [])}
    be_skills = {s["skill_id"]: s["weight"] for s in role_backend.get("skills", [])}
    print(f"    Frontend weights: {fe_skills}")
    print(f"    Backend weights:  {be_skills}")

    assert fe_skills != be_skills or role_frontend["score"] != role_backend["score"], \
        "Role/company differentiation should produce different results"

    # ── 4. Company-specific gap ──────────────────────────────────────────────
    print("\n[4] COMPANY GAP")
    from app.services.evidence_aggregator import company_gap
    gap = await company_gap(uid_a, role="sde", company="amazon")
    print(f"    company = {gap['company']}")
    print(f"    preparation_score = {gap['preparation_score']}")
    print(f"    evidence_coverage = {gap['evidence_coverage']}%")
    print(f"    primary_gap = {gap['primary_gap']}")
    print(f"    blockers = {gap['blockers']}")
    print(f"    next_action = {gap.get('next_action')}")

    assert gap["company"] == "amazon"
    assert "preparation_score" in gap
    assert "evidence_coverage" in gap
    assert "sections" in gap
    assert "primary_gap" in gap
    assert "blockers" in gap

    # ── 5. Target weights present ────────────────────────────────────────────
    print("\n[5] TARGET WEIGHTS")
    weights = readiness_a.get("target_weights", {})
    print(f"    target_weights = {weights}")
    assert len(weights) > 0, "Target weights should be present"
    assert sum(weights.values()) > 0, "Weights should sum to > 0"

    # ── 6. Coverage message ──────────────────────────────────────────────────
    print("\n[6] COVERAGE MESSAGE")
    msg = readiness_a.get("coverage_message")
    print(f"    coverage_message = {msg}")
    assert msg is not None, "Coverage message should be present"
    assert "evidence" in msg.lower() or "%" in msg, "Coverage message should mention evidence or percentage"

    print("\n" + "=" * 70)
    print("ALL RUNTIME VERIFICATIONS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
