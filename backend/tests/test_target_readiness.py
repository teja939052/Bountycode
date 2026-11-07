"""Deterministic target-readiness tests — zero AI, zero network, exact numbers.

Covers the 16 spec cases: empty evidence, hand-computed scores, role/company
differentiation, trust exclusion, critical gates, repair lift, duplicate
safety, retention/transfer/consistency movement, coverage honesty,
determinism, AI-independence, and the no-AI-imports guard.
"""
import ast
import asyncio
import os

import pytest
from mongomock_motor import AsyncMongoMockClient

import app.services.readiness_engine as re


def _ev(mastery=0, assessment=0, transfer=0, retention=0, consistency=50,
        n=0, hs=False, at="2026-09-01T00:00:00+00:00"):
    return {"mastery": mastery, "assessment": assessment, "transfer": transfer,
            "retention": retention, "consistency": consistency,
            "eligible_events": n, "high_stakes": hs, "last_evidence_at": at,
            "counts": {"practice": n, "assessments": 0, "transfer": 0,
                       "srs_reviews": 0, "interviews": 0}}


def _profile(skills):
    return {"role": "test", "company": None,
            "skills": [{"skill_id": sid, "domain": sid, "label": sid,
                        "weight": w, "critical": c, "threshold": 60.0 if c else 0.0,
                        "category": sid, "sources": [sid]}
                       for sid, w, c in skills]}


# 1. Empty user → insufficient evidence -------------------------------------
def test_01_empty_evidence():
    r = re.calculate_target_readiness(_profile([("dsa", 0.5, True), ("coding", 0.5, False)]), {})
    assert r["score"] == 0.0 and r["coverage"] == 0.0
    assert r["status"] == "INSUFFICIENT_EVIDENCE"
    assert "probability" not in str(r).lower()


# 2. Hand-computed skill score ----------------------------------------------
def test_02_skill_formula_exact():
    s = re.score_target_skill(_ev(mastery=80, assessment=70, transfer=60,
                                  retention=50, consistency=90, n=5))
    # 80*.3 + 70*.25 + 60*.2 + 50*.15 + 90*.1 = 24+17.5+12+7.5+9
    assert s["score"] == 70.0, s


# 3. Different roles, same evidence → different scores -----------------------
def test_03_role_differentiation():
    p_sde = re.build_target_profile("sde")
    p_fe = re.build_target_profile("frontend")
    assert {s["skill_id"] for s in p_sde["skills"]} != {s["skill_id"] for s in p_fe["skills"]}
    ev = {"dsa": _ev(mastery=100, assessment=100, transfer=100, retention=100,
                      consistency=100, n=10, hs=True),
          "coding": _ev(mastery=100, assessment=100, transfer=100, retention=100,
                         consistency=100, n=10, hs=True)}
    a = re.calculate_target_readiness(p_sde, ev)
    b = re.calculate_target_readiness(p_fe, ev)
    assert a["score"] != b["score"], (a["score"], b["score"])


# 4. Different companies → different weighting/result ------------------------
def test_04_company_overlay():
    p_tcs = re.build_target_profile("sde", "tcs")
    p_goog = re.build_target_profile("sde", "google")
    w_tcs = {s["skill_id"]: s["weight"] for s in p_tcs["skills"]}
    w_goog = {s["skill_id"]: s["weight"] for s in p_goog["skills"]}
    assert w_tcs != w_goog
    ev = {"dsa": _ev(mastery=90, assessment=90, transfer=90, retention=90,
                      consistency=90, n=10, hs=True),
          "coding": _ev(mastery=40, assessment=40, transfer=40, retention=40,
                         consistency=50, n=10, hs=True)}
    a = re.calculate_target_readiness(p_tcs, ev)
    b = re.calculate_target_readiness(p_goog, ev)
    assert a["score"] != b["score"]


# 5. Trust gate: tiers -------------------------------------------------------
def test_05_trust_weights():
    assert re._trust_weight("verified") == 1.0
    assert re._trust_weight("reviewed") == 0.85
    assert re._trust_weight("automated_checked") == 0.5
    assert re._trust_weight("quarantined") == 0.0
    assert re._trust_weight("unverified") == 0.0
    assert re._trust_weight("needs_review") == 0.0


# 6. Critical skill below threshold → blocker ---------------------------------
def test_06_critical_blocker():
    p = _profile([("dsa", 0.6, True), ("coding", 0.4, False)])
    ev = {"dsa": _ev(mastery=30, assessment=30, transfer=30, retention=30,
                      consistency=50, n=10, hs=True),
          "coding": _ev(mastery=95, assessment=95, transfer=95, retention=95,
                         consistency=95, n=10, hs=True)}
    r = re.calculate_target_readiness(p, ev)
    assert any(b["skill_id"] == "dsa" and b["reason"] == "below_critical_threshold"
               for b in r["blockers"])
    assert r["status"] != "READY"


# 7. High average + critical weakness → never READY ---------------------------
def test_07_high_avg_critical_weakness():
    p = _profile([("dsa", 0.2, True), ("coding", 0.8, False)])
    ev = {"dsa": _ev(mastery=20, assessment=20, transfer=20, retention=20,
                      consistency=50, n=10, hs=True),
          "coding": _ev(mastery=100, assessment=100, transfer=100, retention=100,
                         consistency=100, n=10, hs=True)}
    r = re.calculate_target_readiness(p, ev)
    assert r["score"] > 75, r["score"]
    assert r["status"] != "READY", r


# 8. Successful repair/retest → readiness increases from new evidence ---------
def test_08_repair_lift():
    p = re.build_target_profile("sde")
    base = {"cs_fundamentals": _ev(mastery=40, assessment=35, transfer=0, retention=0,
                                   consistency=50, n=5, hs=True)}
    after = {"cs_fundamentals": _ev(mastery=60, assessment=70, transfer=100, retention=40,
                                    consistency=80, n=12, hs=True,
                                    at="2026-09-18T00:00:00+00:00")}
    a = re.calculate_target_readiness(p, base)
    b = re.calculate_target_readiness(p, after)
    assert b["score"] > a["score"], (a["score"], b["score"])


# 9. Duplicate completion must not inflate (collector dedupe) -----------------
def test_09_duplicate_solves_deduped():
    async def _run():
        import app.database as dbmod
        client = AsyncMongoMockClient()
        db = client["readiness_dup"]
        saved = (getattr(dbmod, "_client", None), getattr(dbmod, "_db", None))
        dbmod._client, dbmod._db = client, db
        try:
            col = dbmod.solved_problems_collection()
            docs = [{"user_id": "u1", "question_id": "q1", "topic": "Arrays"},
                    {"user_id": "u1", "question_id": "q1", "topic": "Arrays"}]
            await col.insert_many(docs)
            orig = re._resolve_question_trust
            re._resolve_question_trust = lambda qid: "verified"  # noqa: E731
            try:
                ev = await re.collect_target_evidence("u1", re.build_target_profile("sde"))
            finally:
                re._resolve_question_trust = orig
            return ev
        finally:
            dbmod._client, dbmod._db = saved
    ev = asyncio.run(_run())
    assert ev["dsa"]["eligible_events"] == 2, ev["dsa"]  # 1 solve + 1 practice count, not 4
    assert ev["dsa"]["counts"]["practice"] == 1


# 10. SRS retention improves → retention component changes ---------------------
def test_10_retention_moves():
    assert re.retention_from_srs(0, 0, 0) == 0.0
    low = re.retention_from_srs(1, 3, 4)
    high = re.retention_from_srs(9, 1, 10)
    assert high > low
    assert high == 90.0 and low == 25.0


# 11. Transfer failure → transfer component decreases --------------------------
def test_11_transfer_moves():
    p = _profile([("dsa", 1.0, False)])
    good = {"dsa": _ev(mastery=70, assessment=70, transfer=100, retention=70,
                        consistency=70, n=10, hs=True)}
    bad = {"dsa": _ev(mastery=70, assessment=70, transfer=0, retention=70,
                       consistency=70, n=10, hs=True)}
    assert (re.calculate_target_readiness(p, good)["score"] -
            re.calculate_target_readiness(p, bad)["score"]) == 20.0


# 12. Consistent performance → consistency improves -----------------------------
def test_12_consistency_rewards_stability():
    shaky = re.consistency_from_series([90, 42, 91, 88])
    steady = re.consistency_from_series([82, 84, 87, 89])
    assert steady > shaky
    assert re.consistency_from_series([80]) == 50.0  # single sample: neutral


# 13. Thin evidence → coverage stays low ---------------------------------------
def test_13_coverage_honest():
    p = re.build_target_profile("sde")
    ev = {"dsa": _ev(mastery=100, assessment=100, transfer=100, retention=100,
                      consistency=100, n=50, hs=True)}
    r = re.calculate_target_readiness(p, ev)
    assert r["coverage"] < 100.0
    assert r["coverage"] == round(sum(s["weight"] for s in p["skills"]
                                     if s["domain"] == "dsa") * 100, 1)


# 14. Same input twice → exactly same result ------------------------------------
def test_14_deterministic():
    p = re.build_target_profile("backend", "amazon")
    ev = {"coding": _ev(mastery=70, assessment=65, transfer=40, retention=60,
                         consistency=75, n=8, hs=True),
          "dsa": _ev(mastery=80, assessment=82, transfer=60, retention=55,
                      consistency=88, n=9, hs=True)}
    assert re.calculate_target_readiness(p, ev) == re.calculate_target_readiness(p, ev)


# 17. Service-tier company targets: valid profiles, weights sum to 1 --------
def test_17_service_company_profiles():
    service = ["tcs", "accenture", "infosys", "wipro", "cognizant",
               "capgemini", "hcl", "tech_mahindra", "techm",
               "lti_mindtree", "lti", "mphasis"]
    for company in service:
        p = re.build_target_profile("sde", company)
        assert p["company"] == company, company
        assert p["skills"], company
        assert abs(sum(s["weight"] for s in p["skills"]) - 1.0) < 1e-3, company
    for key, prof in re.COMPANY_PROFILES.items():
        mw = prof.get("match_weights", {})
        assert abs(sum(mw.values()) - 1.0) < 1e-6, (key, mw)
        for skill in (prof.get("min_skills") or {}):
            assert re._map_skill_to_category(skill) is not None, (key, skill)


# 18. Same evidence, three service targets → three different scores ----------
def test_18_service_targets_differentiate():
    ev = {"dsa": _ev(mastery=95, assessment=95, transfer=95, retention=95,
                      consistency=95, n=10, hs=True),
          "coding": _ev(mastery=15, assessment=15, transfer=15, retention=15,
                         consistency=50, n=10, hs=True),
          "cs_fundamentals": _ev(mastery=50, assessment=50, transfer=50,
                                  retention=50, consistency=50, n=10, hs=True)}
    scores = {}
    for company in ("tcs", "accenture", "infosys"):
        r = re.calculate_target_readiness(
            re.build_target_profile("sde", company), ev)
        assert "probability" not in str(r).lower()
        scores[company] = r["score"]
    assert len(set(scores.values())) == 3, scores
def test_15_no_ai_imports():
    path = os.path.join(os.path.dirname(__file__), "..", "app", "services", "readiness_engine.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    banned = ("openai", "anthropic", "openrouter", "groq", "gemini", "llm",
              "socket", "requests", "httpx", "urllib", "aiohttp")
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            found.append(node.module or "")
    hits = [f for f in found if any(b in f.lower() for b in banned)]
    assert not hits, hits
    # Pure scorer performs no I/O: no await, no open, no socket in its source.
    import inspect
    src = inspect.getsource(re.calculate_target_readiness) + inspect.getsource(re.score_target_skill)
    assert "await " not in src and "open(" not in src and "socket" not in src
