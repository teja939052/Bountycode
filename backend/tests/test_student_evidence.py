"""Student evidence layer tests — deterministic, no AI, no network.

Every metric is asserted on fabricated-but-realistically-shaped stored
documents through the real aggregator code (pure + mongomock collector +
HTTP endpoints). Same input → same output, twice.
"""
import ast
import asyncio
import os
from datetime import datetime, timezone

import pytest
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.services import evidence_aggregator as agg


def _iso(days_ago: int) -> str:
    from datetime import timedelta
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def _bundle():
    evs = []
    # dsa.arrays: 4 passes, 1 fail; first attempt pass; times + hints
    for i, (passed, t, h) in enumerate([(True, 600, 0), (True, 540, 0),
                                        (False, 700, 1), (True, 420, 0), (True, 380, 0)]):
        evs.append({"user_id": "u", "activity_type": "question_solve",
                    "skill_id": "dsa.arrays", "question_id": "q-arr",
                    "passed": passed, "score": 100 if passed else 20,
                    "time_spent_seconds": t, "hints_used": h,
                    "attempt_number": i + 1, "timestamp": _iso(10 - i)})
    # dsa.dp: 1 pass, 3 fails (transfer fail once)
    for i, passed in enumerate([False, False, True, False]):
        evs.append({"user_id": "u", "activity_type": "question_solve",
                    "skill_id": "dsa.dp", "question_id": "q-dp",
                    "passed": passed, "score": 90 if passed else 10,
                    "time_spent_seconds": 1400, "hints_used": 2,
                    "attempt_number": i + 1, "timestamp": _iso(9 - i)})
    evs.append({"user_id": "u", "activity_type": "retest", "skill_id": "dsa.dp",
                "question_id": "q-dp-r", "passed": False, "score": 0,
                "time_spent_seconds": 900, "hints_used": 0,
                "attempt_number": 1, "timestamp": _iso(1)})
    subs = [
        {"user_id": "u", "question_id": "q-arr", "skill_id": "dsa.arrays",
         "failure_class": "SUCCESS", "attempt_index": 1,
         "results": [{"input": "[1]", "execution_time": 0.01},
                     {"input": "[1,2,3,4,5,6,7,8]", "execution_time": 0.02},
                     {"input": "[1]*50", "execution_time": 0.05}],
         "submitted_at": _iso(9)},
        {"user_id": "u", "question_id": "q-dp", "skill_id": "dsa.dp",
         "failure_class": "TIMEOUT", "attempt_index": 1,
         "results": [], "submitted_at": _iso(8)},
        {"user_id": "u", "question_id": "q-dp", "skill_id": "dsa.dp",
         "failure_class": "WRONG_ANSWER", "attempt_index": 2,
         "results": [], "submitted_at": _iso(7)},
        {"user_id": "u", "question_id": "q-x", "skill_id": "dsa.dp",
         "failure_class": "SYNTAX_ERROR", "attempt_index": 1,
         "results": [], "submitted_at": _iso(6)},
    ]
    return {"submissions": subs, "learning_events": evs, "oa_sessions": [],
            "aptitude_tests": [], "question_answers": [], "interviews": [],
            "srs_cards": [{"user_id": "u", "concept_id": "dsa.arrays",
                           "repetitions": 5, "lapses": 1, "total_reviews": 6,
                           "next_review": _iso(3), "interval": 7}],
            "srs_states": [], "solved_problems": [],
            "excluded_untrusted_solves": 0}


def test_heatmap_values():
    h = agg.pattern_heatmap(_bundle())
    arr = next(p for p in h["patterns"] if p["pattern_id"] == "dsa.arrays")
    assert arr["attempts"] == 5 and arr["passes"] == 4
    assert arr["accuracy"] == 80.0 and arr["color"] == "green"
    assert arr["first_attempt_rate"] == 100.0
    assert arr["median_solve_time_s"] == 540.0
    assert arr["hints_used"] == 1
    dp = next(p for p in h["patterns"] if p["pattern_id"] == "dsa.dp")
    assert dp["accuracy"] == round(1 / 5 * 100, 1)
    assert dp["color"] == "red"
    assert dp["transfer_rate"] == 0.0
    assert h["weakest_pattern"] == "dsa.dp"
    assert h["next_action"] == {"type": "repair", "skill_id": "dsa.dp",
                                "reason": "lowest accuracy with sufficient evidence"}


def test_failure_breakdown():
    f = agg.failure_breakdown(_bundle())
    assert f["counts"] == {"SUCCESS": 1, "WRONG_ANSWER": 1, "TIMEOUT": 1,
                           "RUNTIME_ERROR": 0, "SYNTAX_ERROR": 1}
    assert f["percentages"]["TIMEOUT"] == 25.0
    assert f["top_failure"] in ("TIMEOUT", "WRONG_ANSWER", "SYNTAX_ERROR")
    assert f["sufficient"] is False  # only 4 submissions
    dp = agg.failure_breakdown(_bundle(), "dsa.dp")
    assert dp["total_submissions"] == 3


def test_time_trend_windows():
    t = agg.solve_time_trend(_bundle())
    assert t["windows"]["all"]["samples"] >= 9
    assert t["windows"]["all"]["median_s"] == agg._median(
        [s for _, s in agg._solve_time_samples(_bundle())])
    assert t["sufficient"] is True


def test_records_and_streak():
    r = agg.personal_records(_bundle())
    assert r["fastest_correct_solve_s"] == 380.0
    assert r["longest_streak_days"] >= 1
    assert r["best_first_attempt"]["pattern_id"] == "dsa.arrays"


def test_retention_honest():
    now = datetime.now(timezone.utc)
    v = agg.retention_view(_bundle(), now)
    assert v["tracked_count"] == 1 and v["due_count"] == 1
    c = v["concepts"][0]
    assert c["successful_retrievals"] == 5
    assert "forget" not in str(v).lower() and "memory" not in str(v).lower()


def test_reattempts_hint_hidden():
    b = _bundle()
    b["learning_events"].append(
        {"user_id": "u", "activity_type": "question_solve", "skill_id": "dsa.arrays",
         "question_id": "dsa.arrays", "passed": True, "score": 100,
         "time_spent_seconds": 500, "hints_used": 3, "attempt_number": 6,
         "timestamp": _iso(0)})
    r = agg.reattempts_due(b)
    assert r["due_count"] == 1
    assert r["due"][0]["hints_hidden"] is True
    assert "independent reattempt" in r["due"][0]["reason"]


def test_pacing_math():
    b = _bundle()
    target = (datetime.now(timezone.utc)).isoformat()
    from datetime import timedelta
    future = (datetime.now(timezone.utc) + timedelta(days=20)).isoformat()
    p = agg.pacing(b, future, 40)
    assert p["days_remaining"] == 19 or p["days_remaining"] == 20
    assert p["required_pace_per_day"] == round(40 / p["days_remaining"], 2)
    assert p["pace_gap_per_day"] == round(p["required_pace_per_day"] - p["current_pace_per_day"], 2)
    bad = agg.pacing(b, "not-a-date", 5)
    assert "error" in bad


def test_complexity_observed_wording():
    c = agg.complexity_signal(_bundle())
    assert c["sufficient"] is False  # not enough varied sizes in fixture
    assert "probability" not in str(c).lower()
    assert "proves" not in str(c).lower()


def test_determinism_twice():
    import copy
    b = _bundle()
    b2 = copy.deepcopy(b)
    assert agg.pattern_heatmap(b) == agg.pattern_heatmap(b2)
    assert agg.failure_breakdown(b) == agg.failure_breakdown(b2)
    assert agg.personal_records(b) == agg.personal_records(b2)


def test_no_ai_imports():
    path = os.path.join(os.path.dirname(__file__), "..", "app", "services", "evidence_aggregator.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    banned = ("openai", "anthropic", "openrouter", "groq", "gemini", "llm",
              "socket", "requests", "httpx", "urllib", "aiohttp")
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            found.append(node.module or "")
    assert not [f for f in found if any(x in f.lower() for x in banned)]


def test_endpoints_and_company_gap_and_report():
    async def _run():
        import app.database as dbmod
        from app.main import app
        client = AsyncMongoMockClient()
        db = client["evidence_http"]
        saved = (getattr(dbmod, "_client", None), getattr(dbmod, "_db", None))
        dbmod._client, dbmod._db = client, db
        try:
            uid = "student-1"
            await dbmod.learning_events_collection().insert_many(
                [{**e, "user_id": uid} for e in _bundle()["learning_events"]])
            await dbmod.submissions_collection().insert_many(
                [{**s, "user_id": uid} for s in _bundle()["submissions"]])
            await dbmod.users_collection().insert_one(
                {"_id": uid, "email": "ev@example.com", "plan": "free"})
            from app.middleware.auth import get_current_user

            async def _user():
                return {"id": uid, "email": "ev@example.com", "plan": "free"}
            app.dependency_overrides[get_current_user] = _user
            try:
                async with AsyncClient(transport=ASGITransport(app=app),
                                       base_url="http://test") as ac:
                    out = {}
                    for path in ["/api/v1/evidence/heatmap",
                                 "/api/v1/evidence/failures",
                                 "/api/v1/evidence/time-trend",
                                 "/api/v1/evidence/records",
                                 "/api/v1/evidence/retention",
                                 "/api/v1/evidence/reattempts",
                                 "/api/v1/evidence/company-gap?role=sde&company=tcs",
                                 "/api/v1/evidence/pacing?target_date=2026-10-20T00:00:00%2B00:00&remaining_missions=40",
                                 "/api/v1/evidence/complexity",
                                 "/api/v1/evidence/report?role=sde&company=tcs",
                                 "/api/v1/evidence/my-performance?role=sde&company=tcs"]:
                        r = await ac.get(path)
                        out[path] = (r.status_code, r.json())
                    return out
            finally:
                app.dependency_overrides.pop(get_current_user, None)
        finally:
            dbmod._client, dbmod._db = saved
    out = asyncio.run(_run())
    for path, (code, body) in out.items():
        assert code == 200, (path, code, str(body)[:200])
    heat = out["/api/v1/evidence/heatmap"][1]
    assert heat["weakest_pattern"] == "dsa.dp"
    gap = out["/api/v1/evidence/company-gap?role=sde&company=tcs"][1]
    assert gap["preparation_score"] >= 0 and "probability" not in str(gap).lower()
    assert gap["disclaimer"].startswith("Preparation score")
    assert gap["next_action"]["type"] == "repair"
    rep = out["/api/v1/evidence/report?role=sde&company=tcs"][1]
    assert rep["report"] == "PlacementPro Performance Report"
    assert "not an employer certification" in rep["disclaimer"]
    assert rep["evidence"]["coding_attempts"] == 4
    perf = out["/api/v1/evidence/my-performance?role=sde&company=tcs"][1]
    assert perf["biggest_weakness"]["pattern_id"] == "dsa.dp"
    assert perf["next"]["type"] == "repair"
