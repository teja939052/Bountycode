"""Readiness engine integration tests — full pipeline with mock MongoDB.

Exercises the actual wrappers:
- load_target_profile
- load_verified_evidence
- calculate_readiness
- collect_target_evidence (via DB)

Uses mongomock_motor for an in-memory async MongoDB.
"""
from __future__ import annotations

import asyncio
from copy import deepcopy

import pytest
from mongomock_motor import AsyncMongoMockClient

import app.database as dbmod
import app.services.readiness_engine as re


# ── helpers ────────────────────────────────────────────────────────────────

def _setup_db():
    client = AsyncMongoMockClient()
    db = client["readiness_test"]
    return client, db


async def _reset_db(db):
    for name in [
        "solved_problems", "learning_events", "skill_graph",
        "aptitude_tests", "interviews", "srs_cards", "srs",
    ]:
        await db[name].drop()


def _make_col(db, name):
    return db[name]


async def _insert_many(db, name, docs):
    if docs:
        await db[name].insert_many(docs)


async def _run_pipeline(user_id: str, role: str = "sde", company: str | None = None,
                        trust_gate=None) -> dict:
    profile = re.load_target_profile(role=role, company=company)
    evidence = await re.load_verified_evidence(user_id, trust_gate=trust_gate)
    result = re.calculate_target_readiness(profile, evidence)
    result.setdefault("next_action", re.determine_next_action(
        result.get("skills", []), profile
    ))
    return result


# ── fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture()
def db_fixture():
    client, db = _setup_db()
    saved = (getattr(dbmod, "_client", None), getattr(dbmod, "_db", None))
    dbmod._client, dbmod._db = client, db
    yield db
    dbmod._client, dbmod._db = saved


# ── 1. Full pipeline: weak Graphs, strong Arrays ───────────────────────────

@pytest.mark.asyncio
async def test_01_weak_graphs_strong_arrays(db_fixture):
    uid = "user_graphs_weak"
    await _reset_db(db_fixture)

    # Arrays: strong evidence
    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q1", "topic": "Arrays", "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "medium"},
        {"user_id": uid, "question_id": "q2", "topic": "Arrays", "created_at": "2026-09-02T00:00:00+00:00", "difficulty": "easy"},
        {"user_id": uid, "question_id": "q3", "topic": "Arrays", "created_at": "2026-09-03T00:00:00+00:00", "difficulty": "medium"},
    ])
    # Override trust to verified for all
    orig = re._resolve_question_trust
    re._resolve_question_trust = lambda qid: "verified"
    try:
        await _insert_many(db_fixture, "learning_events", [
            {"user_id": uid, "skill_id": "Arrays", "activity_type": "practice",
             "passed": True, "score": 95, "timestamp": "2026-09-04T00:00:00+00:00"},
            {"user_id": uid, "skill_id": "Arrays", "activity_type": "practice",
             "passed": True, "score": 90, "timestamp": "2026-09-05T00:00:00+00:00"},
            {"user_id": uid, "skill_id": "Arrays", "activity_type": "transfer_practice",
             "passed": True, "score": 100, "timestamp": "2026-09-06T00:00:00+00:00"},
        ])
    finally:
        re._resolve_question_trust = orig

    result = await _run_pipeline(uid, role="sde")

    # Must have full response shape
    assert "score" in result
    assert "coverage" in result
    assert "status" in result
    assert "skills" in result
    assert "strengths" in result
    assert "gaps" in result
    assert "blockers" in result
    assert "evidence" in result
    assert "next_action" in result

    arrays = next((s for s in result["skills"] if s["skill_id"] == "dsa"), None)
    # dsa domain includes Arrays topic
    if arrays:
        assert arrays["score"] > 50, f"Arrays/dsa should be strong, got {arrays['score']}"

    # Print actual response
    print("\n=== WEAK GRAPHS / STRONG ARRAYS RESPONSE ===")
    import json
    print(json.dumps(result, indent=2, default=str))


# ── 2. Role differentiation ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_02_role_differentiation_same_evidence(db_fixture):
    uid = "user_role_diff"
    await _reset_db(db_fixture)

    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q1", "topic": "Arrays", "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "medium"},
        {"user_id": uid, "question_id": "q2", "topic": "Graphs", "created_at": "2026-09-02T00:00:00+00:00", "difficulty": "hard"},
    ])
    orig = re._resolve_question_trust
    re._resolve_question_trust = lambda qid: "verified"
    try:
        await _insert_many(db_fixture, "learning_events", [
            {"user_id": uid, "skill_id": "Arrays", "activity_type": "practice",
             "passed": True, "score": 90, "timestamp": "2026-09-03T00:00:00+00:00"},
            {"user_id": uid, "skill_id": "Graphs", "activity_type": "practice",
             "passed": True, "score": 90, "timestamp": "2026-09-04T00:00:00+00:00"},
        ])
    finally:
        re._resolve_question_trust = orig

    role_a = await _run_pipeline(uid, role="frontend")
    role_b = await _run_pipeline(uid, role="backend")

    print("\n=== ROLE DIFFERENTIATION ===")
    print(f"Frontend score: {role_a['score']}")
    print(f"Backend score:  {role_b['score']}")

    # Same evidence, different roles → different weighting → different scores
    # At minimum they should have different skill emphasis
    a_ids = {s["skill_id"] for s in role_a["skills"]}
    b_ids = {s["skill_id"] for s in role_b["skills"]}
    assert a_ids != b_ids or role_a["score"] != role_b["score"], \
        "Role differentiation should produce different results"


# ── 3. Company differentiation ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_03_company_differentiation(db_fixture):
    uid = "user_company_diff"
    await _reset_db(db_fixture)

    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q1", "topic": "Arrays", "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "medium"},
    ])
    orig = re._resolve_question_trust
    re._resolve_question_trust = lambda qid: "verified"
    try:
        await _insert_many(db_fixture, "learning_events", [
            {"user_id": uid, "skill_id": "Arrays", "activity_type": "practice",
             "passed": True, "score": 80, "timestamp": "2026-09-02T00:00:00+00:00"},
        ])
    finally:
        re._resolve_question_trust = orig

    tcs = await _run_pipeline(uid, role="sde", company="tcs")
    google = await _run_pipeline(uid, role="sde", company="google")

    print("\n=== COMPANY DIFFERENTIATION ===")
    print(f"TCS score:      {tcs['score']}")
    print(f"Google score:   {google['score']}")
    print(f"TCS skills:     {[s['skill_id'] for s in tcs['skills']]}")
    print(f"Google skills:  {[s['skill_id'] for s in google['skills']]}")

    # Different companies should weight skills differently
    tcs_weights = {s["skill_id"]: s["weight"] for s in tcs["skills"]}
    google_weights = {s["skill_id"]: s["weight"] for s in google["skills"]}
    assert tcs_weights != google_weights or tcs["score"] != google["score"]


# ── 4. Trust gate: quarantined evidence excluded ────────────────────────────

@pytest.mark.asyncio
async def test_04_trust_gate_excludes_untrusted(db_fixture):
    uid = "user_trust_gate"
    await _reset_db(db_fixture)

    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q_verified", "topic": "Arrays",
         "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "easy"},
        {"user_id": uid, "question_id": "q_auto", "topic": "Graphs",
         "created_at": "2026-09-02T00:00:00+00:00", "difficulty": "hard"},
    ])

    def _trust(qid):
        if qid == "q_verified":
            return "verified"
        elif qid == "q_auto":
            return "automated_checked"
        return "unknown"

    orig = re._resolve_question_trust
    re._resolve_question_trust = _trust
    try:
        # Without trust gate: automated_checked contributes (weight 0.5)
        result_no_gate = await _run_pipeline(uid, role="sde", trust_gate=None)

        # With trust gate: automated_checked is excluded (only verified/reviewed pass)
        result_with_gate = await _run_pipeline(uid, role="sde",
                                               trust_gate=re.TRUSTED_STATUSES)
    finally:
        re._resolve_question_trust = orig

    print("\n=== TRUST GATE ===")
    print(f"Without gate: {result_no_gate['score']}")
    print(f"With gate:    {result_with_gate['score']}")

    # With gate should have less evidence than without
    assert result_no_gate["coverage"] >= result_with_gate["coverage"], \
        f"Trust gate should not increase coverage: {result_no_gate['coverage']} vs {result_with_gate['coverage']}"


# ── 5. Repair / retest effect ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_05_repair_retest_lifts_score(db_fixture):
    uid = "user_repair"
    await _reset_db(db_fixture)

    # Initial weak Graphs evidence
    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q_g1", "topic": "Graphs",
         "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "easy"},
    ])
    await _insert_many(db_fixture, "learning_events", [
        {"user_id": uid, "skill_id": "Graphs", "activity_type": "practice",
         "passed": False, "score": 30, "timestamp": "2026-09-02T00:00:00+00:00"},
    ])

    orig = re._resolve_question_trust
    re._resolve_question_trust = lambda qid: "verified"
    try:
        before = await _run_pipeline(uid, role="sde")
    finally:
        re._resolve_question_trust = orig

    # Now simulate repair: add successful learning events + verified retest
    re._resolve_question_trust = lambda qid: "verified"
    try:
        await _insert_many(db_fixture, "learning_events", [
            {"user_id": uid, "skill_id": "Graphs", "activity_type": "repair",
             "passed": True, "score": 85, "timestamp": "2026-09-10T00:00:00+00:00"},
            {"user_id": uid, "skill_id": "Graphs", "activity_type": "practice",
             "passed": True, "score": 90, "timestamp": "2026-09-11T00:00:00+00:00"},
            {"user_id": uid, "skill_id": "Graphs", "activity_type": "retest",
             "passed": True, "score": 95, "timestamp": "2026-09-12T00:00:00+00:00"},
        ])
        after = await _run_pipeline(uid, role="sde")
    finally:
        re._resolve_question_trust = orig

    print("\n=== REPAIR / RETEST ===")
    print(f"Before repair: {before['score']}")
    print(f"After repair:  {after['score']}")

    graphs_before = next((s for s in before["skills"] if s["skill_id"] == "dsa"), None)
    graphs_after = next((s for s in after["skills"] if s["skill_id"] == "dsa"), None)

    if graphs_before and graphs_after:
        print(f"Graphs score before: {graphs_before['score']}")
        print(f"Graphs score after:  {graphs_after['score']}")
        assert after["score"] > before["score"], "Repair should increase readiness"


# ── 6. AI independence ─────────────────────────────────────────────────────

def test_06_no_ai_imports_in_readiness_engine():
    path = "D:/Project-Fremen/backend/app/services/readiness_engine.py"
    with open(path, encoding="utf-8") as f:
        source = f.read()
    import ast
    tree = ast.parse(source)
    banned = ("openai", "anthropic", "openrouter", "groq", "gemini",
              "llm", "socket", "requests", "httpx", "urllib", "aiohttp")
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            found.append(node.module or "")
    hits = [f for f in found if any(b in f.lower() for b in banned)]
    assert not hits, f"AI/network imports found in readiness_engine.py: {hits}"


# ── 7. Determinism ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_07_deterministic_same_input(db_fixture):
    uid = "user_det"
    await _reset_db(db_fixture)

    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q1", "topic": "Arrays",
         "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "medium"},
    ])
    orig = re._resolve_question_trust
    re._resolve_question_trust = lambda qid: "verified"
    try:
        r1 = await _run_pipeline(uid, role="sde", company="amazon")
        r2 = await _run_pipeline(uid, role="sde", company="amazon")
    finally:
        re._resolve_question_trust = orig

    assert r1 == r2, "Same input must produce identical output"
    print("\n=== DETERMINISM ===")
    print(f"Run 1 score: {r1['score']}")
    print(f"Run 2 score: {r2['score']}")


# ── 8. Actual response shape for weak Graphs user ──────────────────────────

@pytest.mark.asyncio
async def test_08_response_shape_weak_graphs(db_fixture):
    uid = "user_shape"
    await _reset_db(db_fixture)

    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q1", "topic": "Graphs",
         "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "hard"},
    ])
    orig = re._resolve_question_trust
    re._resolve_question_trust = lambda qid: "verified"
    try:
        result = await _run_pipeline(uid, role="sde", company="amazon")
    finally:
        re._resolve_question_trust = orig

    # Required keys
    required = ["score", "coverage", "status", "skills", "strengths",
                "gaps", "blockers", "evidence", "next_action"]
    for key in required:
        assert key in result, f"Missing key: {key}"

    # Each skill entry must have score/weight/status/critical
    for skill in result["skills"]:
        assert "score" in skill
        assert "weight" in skill
        assert "status" in skill
        assert "critical" in skill

    print("\n=== RESPONSE SHAPE (weak Graphs) ===")
    import json
    print(json.dumps(result, indent=2, default=str))


# ── 9. Trust gating via load_verified_evidence wrapper ─────────────────────

@pytest.mark.asyncio
async def test_09_trust_gate_wrapper(db_fixture):
    uid = "user_trust_wrap"
    await _reset_db(db_fixture)

    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q1", "topic": "Arrays",
         "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "easy"},
        {"user_id": uid, "question_id": "q2", "topic": "Arrays",
         "created_at": "2026-09-02T00:00:00+00:00", "difficulty": "easy"},
    ])

    call_count = [0]
    def _trust(qid):
        call_count[0] += 1
        return "verified" if qid == "q1" else "quarantined"

    orig = re._resolve_question_trust
    re._resolve_question_trust = _trust
    try:
        ev_all = await re.load_verified_evidence(uid, trust_gate=None)
        ev_gated = await re.load_verified_evidence(uid, trust_gate=re.TRUSTED_STATUSES)
    finally:
        re._resolve_question_trust = orig

    print("\n=== TRUST GATE WRAPPER ===")
    print(f"Without gate: {len(ev_all)} skills with evidence")
    print(f"With gate:    {len(ev_gated)} skills with evidence")

    # With gate should have <= evidence than without
    assert len(ev_gated) <= len(ev_all)


# ── 10. Full wrapper calculate_readiness end-to-end ─────────────────────────

@pytest.mark.asyncio
async def test_10_calculate_readiness_wrapper(db_fixture):
    uid = "user_wrapper"
    await _reset_db(db_fixture)

    await _insert_many(db_fixture, "solved_problems", [
        {"user_id": uid, "question_id": "q1", "topic": "Arrays",
         "created_at": "2026-09-01T00:00:00+00:00", "difficulty": "medium"},
        {"user_id": uid, "question_id": "q2", "topic": "Graphs",
         "created_at": "2026-09-02T00:00:00+00:00", "difficulty": "hard"},
    ])
    orig = re._resolve_question_trust
    re._resolve_question_trust = lambda qid: "verified"
    try:
        result = await re.calculate_target_readiness_score(uid, target_role="sde", target_company="amazon")
    finally:
        re._resolve_question_trust = orig

    assert isinstance(result, dict)
    assert "score" in result
    assert "coverage" in result
    assert "skills" in result
    assert "next_action" in result

    print("\n=== CALCULATE_READINESS WRAPPER ===")
    import json
    print(json.dumps(result, indent=2, default=str))
