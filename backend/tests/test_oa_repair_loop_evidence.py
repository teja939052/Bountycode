"""End-to-end evidence run: Mock OA repair gate (verified-only, closed loop).

Deterministic scenario — no live Mongo, no Piston, no network:
  register -> start TCS OA (verified_only, MCQ sections + coding) ->
  submit: every servable MCQ CORRECT except the targeted topic (WRONG),
  coding questions SOLVED with the verified bank solution (local python
  batch oracle, code_executor._grade_python_batched) ->
  complete -> assert scorecard + diagnosis.primary_weakness + repair_missions
  -> missions list -> verified retest on the exact weakness -> answer
  correctly -> pass (100%) -> complete mission -> verify persistence
  (session result, LearningEvents, readiness skill_graph).

All grading is deterministic and in-process. Mongo is served by
mongomock-motor patched under app.database. This is the Evidence Rule in
action: the chain is verified on real outputs, not "compiles".

Every HTTP response body is printed and also written to
tests/evidence_oa_repair_loop.json.
"""

import asyncio
import json
import uuid

import pytest
from datetime import datetime, timezone
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.database import (
    learning_events_collection,
    oa_sessions_collection,
    repair_missions_collection,
    skill_graph_collection,
    users_collection,
)
from app.main import app
from app.middleware.rate_limiter import request_counts


class _NoLoop:
    def is_closed(self):
        return False


class _MockClient(AsyncMongoMockClient):
    def get_io_loop(self):
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return _NoLoop()


@pytest.fixture(autouse=True)
async def _mock_mongo():
    import app.database as dbmod
    import app.routes.admin_monitoring as _admin
    import app.routes.health as _health
    import app.routes.metrics as _metrics
    import app.services.gamification as _gam
    import app.services.learning as _learning

    client = _MockClient()
    database = client["bountycode_e2e_evidence"]

    dbmod._client = client
    dbmod._db = database
    dbmod.get_client = lambda: client
    dbmod.get_db = lambda: database

    swap = {
        _health: ("get_db", database),
        _metrics: ("get_db", database),
        _admin: ("get_db", database),
        _gam: ("get_client", client),
        _learning: ("get_client", client),
    }
    saved = {m: (name, getattr(m, name)) for m, (name, _) in swap.items()}
    for m, (name, value) in swap.items():
        setattr(m, name, lambda value=value: value)
    request_counts.clear()

    yield database

    for m, (name, original) in saved.items():
        setattr(m, name, original)
    request_counts.clear()


EMAIL = f"evidence-{uuid.uuid4().hex[:8]}@example.com"
PASSWORD = "SecurePass123!"


def _header(token: str):
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.integration
async def test_oa_repair_loop_e2e(_mock_mongo):
    from app.services import question_store as qs

    await users_collection().delete_many({"email": EMAIL})

    evidence: list = []

    def show(label: str, payload):
        evidence.append({"label": label, "payload": payload})

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:

        # 1. register a fresh student
        r = await client.post(
            "/api/v1/auth/register",
            json={"email": EMAIL, "name": "E2E Evidence", "password": PASSWORD},
        )
        assert r.status_code == 200, r.text
        body = r.json()
        token = body["token"]
        uid = body["user"]["id"]
        show("1 register", body)

        # 2. start a verified-only TCS OA
        start_payload = None
        for total in (12, 10, 8):
            sr = await client.post(
                "/api/v1/oa/tcs/start",
                json={
                    "company": "tcs",
                    "role": "swe",
                    "mode": "calm",
                    "total_questions": total,
                    "duration_minutes": 60,
                    "integrity": False,
                    "verified_only": True,
                },
                headers=_header(token),
            )
            if sr.status_code == 200:
                start_payload = sr.json()
                break
        assert start_payload, "every verified-only OA variant failed to start"
        sid = start_payload["session_id"]
        show("2 start", start_payload)

        # client payload never leaks answer keys
        for q in start_payload["questions"]:
            assert not any(k.startswith("_") for k in q), f"leaked key: {q}"

        # stored server copy RETAINS the answer key (the grading fix)
        sess = await oa_sessions_collection().find_one({"session_id": sid})
        assert sess, "session doc not persisted"
        stored_qs = sess["questions"]
        mcq = [q for q in stored_qs if q["kind"] == "mcq"]
        assert mcq, "no mcq questions served"
        assert all("_correct_index" in q for q in mcq), "stored copy lost _correct_index"

        # 3. pick the deterministic weakness: earliest mcq topic (in session
        #    order) that has verified retest coverage in the bank.
        seen_topics = []
        for q in mcq:
            if q["topic"] not in seen_topics:
                seen_topics.append(q["topic"])
        assert seen_topics, "no mcq topics"
        bank_coverage = {}
        for topic in seen_topics:
            bank_coverage[topic] = len(
                qs.find({"topic": topic}).only_verified().to_list(10)
            )
        target_topic = next(
            (t for t in seen_topics if bank_coverage[t] >= 2), seen_topics[0]
        )

        def _correct_pos(q):
            """Mirror the server's letter->index resolution (oa._correct_position)."""
            opts = q.get("options") or q.get("multiple_choice_options") or []
            ci = q.get("_correct_index", q.get("correct_index"))
            if isinstance(ci, int):
                return ci
            keys = list(opts.keys()) if isinstance(opts, dict) else []
            if isinstance(ci, str):
                if ci.strip().isdigit():
                    return int(ci)
                if ci in keys:
                    return keys.index(ci)
            ca = q.get("correct_answer")
            if ca is not None:
                if isinstance(opts, dict):
                    vals = {str(v).strip().lower(): k for k, v in opts.items()}
                    match = vals.get(str(ca).strip().lower())
                    if match is None and ca in keys:
                        match = ca
                    if match is not None:
                        return keys.index(match)
                if isinstance(opts, list):
                    tokens = [str(o).strip().lower() for o in opts]
                    if str(ca).strip().lower() in tokens:
                        return tokens.index(str(ca).strip().lower())
            return 0

        # 4. build + submit the deterministic plan
        items = []
        for q in stored_qs:
            kind = q["kind"]
            if kind == "mcq":
                pos = _correct_pos(q)
                if q["topic"] == target_topic:
                    items.append({
                        "question_uid": q["question_uid"],
                        "answer": (pos + 1) % max(len(q.get("options") or []), 2),
                        "time_taken": 20,
                    })
                else:
                    items.append({
                        "question_uid": q["question_uid"],
                        "answer": pos,
                        "time_taken": 20,
                    })
            elif kind == "code":
                bank = qs.find_one({"_id": q.get("question_id")})
                solution_code = ((bank or {}).get("solution") or {}).get("code") or ""
                assert solution_code, f"no verified solution for coding q {q.get('question_id')}"
                items.append({
                    "question_uid": q["question_uid"],
                    "answer": solution_code,
                    "language": "python",
                    "time_taken": 120,
                })

        assert items, "no answers planned"
        r = await client.post(
            "/api/v1/oa/answer",
            json={"session_id": sid, "items": items},
            headers=_header(token),
        )
        assert r.status_code == 200, r.text
        show("3 submit answers", r.json())

        # 5. complete — grade, diagnose, persist repair missions
        r = await client.post(f"/api/v1/oa/{sid}/complete", headers=_header(token))
        assert r.status_code == 200, r.text
        result = r.json()
        show("4 complete", result)

        assert result["questions_answered"] == len(items)
        diag = result.get("diagnosis") or {}
        missions = result.get("repair_missions") or []
        assert diag, "no diagnosis returned"
        assert diag.get("primary_weakness") == target_topic, (
            f"primary_weakness={diag.get('primary_weakness')!r}"
            f" expected={target_topic!r}"
        )
        assert diag.get("skill_weaknesses"), "skill_weaknesses missing"
        target_entry = next(
            (w for w in diag["skill_weaknesses"] if w["skill"] == target_topic), None
        )
        assert target_entry is not None, f"target {target_topic} absent from weaknesses"
        assert target_entry["correct"] == 0 and target_entry["total"] >= 1, target_entry
        assert missions, "no repair missions"
        assert missions[0]["skill"] == target_topic, missions
        assert missions[0].get("retest_verified_ids"), "no verified retest ids attached"

        # scorecard is authoritative: target wrong, non-target mcq + code right
        by_uid = {pq["question_uid"]: pq for pq in result["scorecard"]}
        for q in mcq:
            pq = by_uid.get(q["question_uid"])
            if pq is None:
                continue  # letter-style question skipped by design
            if q["topic"] == target_topic:
                assert pq["score"] == 0, pq
            else:
                assert pq["score"] == 100, pq
        for q in stored_qs:
            if q["kind"] == "code":
                pq = by_uid.get(q["question_uid"])
                assert pq is not None, f"code q not scored: {q['question_uid']}"
                assert pq["score"] == 100, pq  # local python oracle proved it

        # 6. repair missions list shows the target weakness
        r = await client.get("/api/v1/repair/missions", headers=_header(token))
        assert r.status_code == 200, r.text
        mis = r.json()
        show("5 missions list", mis)
        assert mis.get("has_repairs") is True, mis
        target_missions = [
            m
            for m in mis.get("missions", [])
            if target_topic in (m.get("weaknesses") or [])
        ]
        assert target_missions, "mission for target not listed"
        mission_id = target_missions[0]["id"]

        # 7. verified retest on the exact weakness
        r = await client.get(
            f"/api/v1/repair/retest?skill={target_topic}&count=3",
            headers=_header(token),
        )
        assert r.status_code == 200, r.text
        rt = r.json()
        show("6 retest", rt)
        assert rt["count"] >= 1, rt
        assert all(q["trust_status"] == "verified" for q in rt["questions"])

        # 8. solve the retest with the bank's independently verified answers
        retest_answers = []
        for it in rt["questions"]:
            bank = qs.find_one({"_id": it["id"]})
            assert bank, f"retest question missing from bank: {it['id']}"
            if it.get("kind") == "code":
                code = (bank.get("solution") or {}).get("code") or ""
                retest_answers.append(
                    {"question_id": it["id"], "code": code, "language": "python"}
                )
            else:
                ci = bank.get("correct_index")
                if ci is None:
                    opts = bank.get("options") or bank.get("multiple_choice_options") or []
                    ca = bank.get("correct_answer")
                    ci = opts.index(ca) if ca in opts else 0
                retest_answers.append({"question_id": it["id"], "answer": ci})
        r = await client.post(
            "/api/v1/repair/retest/submit",
            json={"skill": target_topic, "answers": retest_answers},
            headers=_header(token),
        )
        assert r.status_code == 200, r.text
        sub = r.json()
        show("7 retest submit", sub)
        assert sub["passed"] is True, sub
        assert sub["pct"] == 100, sub
        assert all(res["correct"] for res in sub["results"]), sub

        # 9. complete the repair mission
        r = await client.post(
            "/api/v1/repair/missions/complete",
            json={"mission_id": mission_id},
            headers=_header(token),
        )
        assert r.status_code == 200, r.text
        comp = r.json()
        show("8 mission complete", comp)
        assert comp.get("completed") is True, comp

        # 10. persistence audit (every arrow must persist)
        sess_end = await oa_sessions_collection().find_one({"session_id": sid})
        assert sess_end["status"] == "completed", sess_end
        assert sess_end.get("diagnosis", {}).get("primary_weakness") == target_topic
        assert sess_end.get("repair_missions"), "missions not persisted on session"

        done = await repair_missions_collection().find_one({"id": mission_id})
        assert done and done.get("status") == "completed", done

        events = [
            e async for e in learning_events_collection().find({"user_id": uid})
        ]
        activity_types = {e.get("activity_type") for e in events}
        required_events = {"mock_oa", "oa_complete", "repair", "retest"}
        missing = required_events - activity_types
        assert not missing, f"missing learning events: {missing}; got {activity_types}"

        sg = await skill_graph_collection().find_one({"user_id": uid})
        assert sg and sg.get("oa_outcomes"), "readiness signal not persisted"

    # --- evidence block ------------------------------------------------
    blob = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "email": EMAIL,
        "target_topic": target_topic,
        "chain": evidence,
    }
    with open(
        "tests/evidence_oa_repair_loop.json", "w", encoding="utf-8"
    ) as fh:
        json.dump(blob, fh, indent=2, default=str)

    print("\n" + "=" * 96)
    print("E2E OA REPAIR LOOP EVIDENCE")
    print("=" * 96)
    for item in evidence:
        print(f"\n### {item['label']}")
        print(json.dumps(item["payload"], indent=2, default=str))
    print("\n" + "=" * 96)
    print(f"WROTE tests/evidence_oa_repair_loop.json  ({len(evidence)} steps)")
    print("=" * 96)


@pytest.mark.integration
async def test_local_oracle_auto_detect_function_style():
    """Function-style verified questions must grade 100 offline EVEN WITHOUT an
    explicit function_name (retest/compiler paths don't always carry it), while
    stdin-program submissions stay on the program path. Guards the batch-oracle
    auto-detect so a coding repair retest can never be un-passable."""
    from app.services import question_store as qs
    from app.services.code_executor import CodeExecutionEngine

    if not qs._questions:
        qs.load_all()
    engine = CodeExecutionEngine()

    for qid in ("verify-001", "verify-003", "verify-008"):
        q = qs.find_one({"_id": qid})
        assert q, qid
        res = await engine.execute_against_test_cases(
            source_code=(q.get("solution") or {}).get("code") or "",
            language="python",
            test_cases=q.get("test_cases") or [],
            function_name="",
        )
        assert res.get("success") is True, (qid, res)
        assert res.get("engine") == "local_oracle_batch", (qid, res)
        assert res.get("score") == 100.0, (qid, res.get("score"))

    prog_cases = [
        {"input": "21", "expected": "42"},
        {"input": "7", "expected": "14"},
        {"input": "0", "expected": "0"},
    ]
    res = await engine.execute_against_test_cases(
        source_code="n = int(input())\nprint(n * 2)\n",
        language="python",
        test_cases=prog_cases,
        function_name="",
    )
    assert res.get("success") is True and res.get("score") == 100.0, res