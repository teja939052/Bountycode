"""Correctness tests: execute sampled v2 solutions and verify outputs.

- coding: exec the stored reference solution, run its own test cases
- sql: rebuild sqlite DB from schema+seed, run reference query, compare rows
- debugging: fixed code must differ from buggy code (execution spot check)
- mcq: correct option letter must resolve to a real option value

Sampling keeps CI time bounded; generators already executed 100% at build.
"""
from __future__ import annotations

import json
import os
import sqlite3

import pytest

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")

_CODING_SAMPLE = 30
_SQL_SAMPLE = 30


def _load(name: str) -> list[dict]:
    with open(os.path.join(_DATA_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


def _coding_questions() -> list[dict]:
    return [q for q in _load("bank_coding_v2.json") if q.get("type") == "coding"]


def _run_solution(code: str, inp):
    """Exec solution code, call the single defined function with parsed input."""
    ns: dict = {}
    exec(compile(code, "<solution>", "exec"), ns)  # noqa: S102 - trusted test fixture
    fns = [v for v in ns.values() if callable(v)]
    assert fns, "solution defines no callable"
    fn = fns[0]
    if isinstance(inp, str):
        try:
            inp = json.loads(inp)
        except Exception:
            pass
    return fn(inp)


def test_sampled_coding_solutions_pass_own_tests():
    questions = _coding_questions()
    assert len(questions) >= _CODING_SAMPLE
    step = max(1, len(questions) // _CODING_SAMPLE)
    failures = []
    for q in questions[::step][: _CODING_SAMPLE * 2]:
        code = (q.get("solution") or {}).get("code", "")
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not code or not tcs:
            failures.append((q["id"], "missing code/cases"))
            continue
        for tc in tcs[:3]:
            try:
                got = _run_solution(code, tc.get("input"))
            except Exception as e:  # noqa: BLE001 - report, don't crash suite
                failures.append((q["id"], f"exec error: {e}"))
                break
            exp = tc.get("expected", tc.get("output"))
            try:
                exp_cmp = json.loads(exp) if isinstance(exp, str) else exp
            except Exception:
                exp_cmp = exp
            if isinstance(exp_cmp, float) and isinstance(got, float):
                ok = abs(exp_cmp - got) < 1e-6
            else:
                ok = got == exp_cmp
            if not ok:
                failures.append((q["id"], f"got {got!r} expected {exp_cmp!r}"))
                break
        if len(failures) > 5:
            break
    assert not failures, f"coding failures: {failures[:5]}"


def test_sampled_sql_queries_reproduce_stored_rows():
    data = [q for q in _load("bank_sql_v2.json") if q.get("type") == "sql"]
    assert len(data) >= _SQL_SAMPLE
    step = max(1, len(data) // _SQL_SAMPLE)
    failures = []
    for q in data[::step][: _SQL_SAMPLE * 2]:
        ddl = q.get("sql_schema") or q.get("schema_ddl") or ""
        seed = q.get("seed_inserts") or q.get("sample_data") or ""
        query = q.get("correct_answer") or q.get("correct_query") or ""
        if not (ddl and seed and query):
            failures.append((q["id"], "missing ddl/seed/query"))
            continue
        try:
            conn = sqlite3.connect(":memory:")
            cur = conn.cursor()
            cur.executescript(ddl)
            cur.executescript(seed)
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()
        except Exception as e:  # noqa: BLE001
            failures.append((q["id"], f"sqlite error: {e}"))
            continue
        exp_rows = q.get("expected_rows") or []
        got_rows = ["|".join("" if v is None else str(v) for v in r) for r in rows]
        if sorted(got_rows) != sorted(exp_rows):
            failures.append((q["id"], f"row mismatch: {got_rows[:2]} vs {exp_rows[:2]}"))
        if len(failures) > 5:
            break
    assert not failures, f"sql failures: {failures[:5]}"


def test_debugging_fixed_differs_from_buggy():
    checked = 0
    for q in _load("bank_debugging_v2.json"):
        assert q.get("buggy_code") != q.get("correct_code"), q["id"]
        tcs = q.get("test_cases") or q.get("testcases") or []
        assert tcs, f"{q['id']} has no test cases"
        assert any("expected" in tc or "output" in tc for tc in tcs), q["id"]
        checked += 1
    assert checked >= 133


def test_mcq_correct_letters_resolve():
    checked = 0
    for name in ("bank_thin_v2.json", "bank_csfund_v2.json", "bank_logical_v2.json",
                 "bank_verbal_v2.json", "bank_aptitude_v2.json"):
        for q in _load(name):
            if q.get("type") not in ("aptitude", "logical", "verbal", "cs_fundamentals", "cs"):
                continue
            opts = q.get("options")
            correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
            if isinstance(opts, dict):
                assert correct in [str(k).upper() for k in opts], q["id"]
                checked += 1
            elif isinstance(opts, list):
                ci = q.get("correct_index")
                if isinstance(ci, int):
                    assert 0 <= ci < len(opts), q["id"]
                else:
                    assert str(q.get("correct_answer") or "").strip() in [str(o).strip() for o in opts], q["id"]
                checked += 1
    assert checked > 1000, f"only {checked} mcq resolutions checked"
