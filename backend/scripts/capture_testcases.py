"""Deterministic test-case capture — zero LLM, zero network.

For coding questions that have a reference solution + examples but NO stored
test cases, execute the already-authored reference solution against each
example's input and record what it actually produces.

- Match (captured output == example expected): validated capture candidate.
  Written to captured_testcases_candidates.json for human review via the
  tranche-approve flow. NEVER auto-promoted, NEVER sets trust_status.
- Mismatch: flagged for human review in the report. NOT promoted.
- No solution / no examples / non-coding: skipped, listed honestly.

Reads from the in-memory canonical store (file-seeded). Writes only:
  backend/app/data/captured_testcases_report.json
  backend/app/data/captured_testcases_candidates.json
Never mutates source banks. Never touches MongoDB. Never sets trust_status.
"""
import ast
import contextlib
import io
import json
import os
import sys

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.services import question_store  # noqa: E402
from app.services.auto_verify import (  # noqa: E402
    _extract_funcs,
    _values_equal,
)

DATA_DIR = os.path.join(BACKEND_ROOT, "app", "data")
REPORT_PATH = os.path.join(DATA_DIR, "captured_testcases_report.json")
CANDIDATES_PATH = os.path.join(DATA_DIR, "captured_testcases_candidates.json")


def _call_with_inputs(fn, inp):
    """Invoke fn with an already-parsed example input."""
    if isinstance(inp, dict):
        try:
            return fn(**inp)
        except TypeError:
            return fn(*inp.values())
    if isinstance(inp, list):
        try:
            return fn(*inp)
        except TypeError:
            return fn(inp)
    return fn(inp)


def main():
    question_store.load_all()
    scanned = 0
    skipped_no_solution = 0
    skipped_no_examples = 0
    skipped_has_testcases = 0
    skipped_non_coding = 0
    exec_fail = 0
    matched = 0
    mismatched = 0
    candidates = []
    mismatches = []

    for q in question_store._questions:
        if str(q.get("type") or "coding").lower() != "coding":
            skipped_non_coding += 1
            continue
        tcs = q.get("test_cases") or q.get("testcases") or []
        if tcs:
            skipped_has_testcases += 1
            continue
        sol = q.get("solution") or {}
        code = str(sol.get("code") or "") if isinstance(sol, dict) else ""
        if not code or "implement optimal" in code.lower():
            skipped_no_solution += 1
            continue
        examples = q.get("examples") or []
        if not examples:
            skipped_no_examples += 1
            continue

        scanned += 1
        src = _extract_funcs(code)
        ns = {}
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(src, ns)
        except Exception as e:
            exec_fail += 1
            mismatches.append({"id": q.get("id"), "reason": "EXEC_FAIL:%s" % type(e).__name__})
            continue
        fn = None
        for line in src.splitlines():
            s = line.strip()
            if s.startswith("def "):
                name = s.split("(")[0].replace("def ", "").strip()
                if name in ns and callable(ns[name]) and name != "main":
                    fn = ns[name]
                    break
        if fn is None:
            exec_fail += 1
            mismatches.append({"id": q.get("id"), "reason": "NO_FUNC"})
            continue

        captured = []
        ok = True
        for ex in examples:
            if not isinstance(ex, dict):
                continue
            inp = ex.get("input")
            expected = ex.get("expected", ex.get("output", ""))
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    actual = _call_with_inputs(fn, inp)
            except Exception as e:
                ok = False
                mismatches.append({"id": q.get("id"), "reason": "CALL_FAIL:%s" % type(e).__name__})
                break
            if _values_equal(actual, expected):
                captured.append({
                    "input": json.dumps(inp) if not isinstance(inp, str) else inp,
                    "output": json.dumps(actual) if not isinstance(actual, str) else actual,
                    "hidden": False,
                    "source": "execution_captured_from_reference_solution",
                })
            else:
                ok = False
                mismatches.append({
                    "id": q.get("id"),
                    "reason": "MISMATCH expected=%r got=%r" % (expected, actual)[:160],
                })
                break
        if ok and captured:
            matched += 1
            candidates.append({
                "id": q.get("id"),
                "question": str(q.get("question") or "")[:120],
                "captured_test_cases": captured,
                "provenance": "execution_captured_from_reference_solution",
                "note": "candidate only — requires human review via tranche-approve; trust_status untouched",
            })
        elif not ok:
            mismatched += 1

    report = {
        "scanned_candidates": scanned,
        "matched_execution_captures": matched,
        "mismatched_flagged_for_review": mismatched,
        "exec_failures": exec_fail,
        "skipped_non_coding": skipped_non_coding,
        "skipped_has_testcases": skipped_has_testcases,
        "skipped_no_solution": skipped_no_solution,
        "skipped_no_examples": skipped_no_examples,
        "mismatches_sample": mismatches[:50],
        "rule": "zero LLM, zero network, no trust_status mutation, no source-bank mutation",
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1)
    with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
