"""Precompute expected outputs for every problem with a reference solution.

Runs each reference solution LOCALLY (one sandboxed batch process per
problem, zero external API calls) against the problem's test inputs and
writes verified expected outputs to app/data/expected_outputs.json.

This is the "we already know the answers" offline pipeline: expected values
are generated once, at build/seed time, from canonical solutions — so the
runtime grader never depends on AI generation or remote execution to know
what a correct answer looks like. It only has to compare user output against
these baked values.

Usage:
    python scripts/precompute_expected_outputs.py            # verify + write
    python scripts/precompute_expected_outputs.py --check    # CI mode: fail on mismatch
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.reference_solutions import REFERENCE_SOLUTIONS  # noqa: E402
from app.routes.battles import BATTLE_PROBLEMS  # noqa: E402
from app.services.local_sandbox import execute_local_python_batch  # noqa: E402


def _canon(v) -> str:
    """Mirror of the oracle's canonical serializer (local_sandbox._BATCH_RUNNER)."""
    if isinstance(v, str):
        return v
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (list, tuple)):
        return json.dumps(
            [x.tolist() if hasattr(x, "tolist") else x for x in v],
            separators=(",", ":"),
        )
    return json.dumps(v, separators=(",", ":"))


async def grade_problem(slug: str, problem: dict, ref: dict) -> dict:
    cases = problem.get("test_cases", [])
    stdins = [tc.get("input", "") for tc in cases]

    # Direct oracle call: one sandboxed process grades every case.
    result = await execute_local_python_batch(
        ref["python"],
        stdins,
        timeout=15,
        function_name=ref["function_name"],
    )
    if not result.get("success") or result.get("compile_error"):
        return {
            "slug": slug,
            "status": "harness_error",
            "error": result.get("error") or result.get("compile_error"),
            "expected_outputs": [],
        }

    outputs = []
    for (ok, value), case in zip(result["results"], cases):
        authored = case.get("expected", "")
        status = ("match" if value == authored else "mismatch") if ok else "error"
        outputs.append({
            "input": case.get("input", ""),
            "authored_expected": authored,
            "computed_expected": value,
            "status": status,
        })

    return {
        "slug": slug,
        "title": problem.get("title"),
        "function_name": ref["function_name"],
        "status": (
            "ok"
            if all(o["status"] == "match" for o in outputs)
            else "verified_with_corrections" if all(o["status"] in ("match", "mismatch") for o in outputs)
            else "has_errors"
        ),
        "expected_outputs": [
            {"input": o["input"], "expected": o["computed_expected"]} for o in outputs
        ],
        "diffs": [
            {"input": o["input"], "authored": o["authored_expected"], "canonical": o["computed_expected"]}
            for o in outputs
            if o["status"] == "mismatch"
        ],
    }


async def main() -> int:
    check_only = "--check" in sys.argv

    matched = 0
    report = {}
    for problem in BATTLE_PROBLEMS:
        slug = problem.get("title", "").strip().lower().replace(" ", "-")
        ref = REFERENCE_SOLUTIONS.get(slug)
        if not ref:
            print(f"[skip] {slug}: no reference solution")
            continue
        res = await grade_problem(slug, problem, ref)
        report[slug] = res
        n_diffs = len(res.get("diffs", []))
        if res["status"] == "ok":
            matched += 1
            print(f"[ok]   {slug}: {len(res['expected_outputs'])} cases match")
        elif res["status"] == "verified_with_corrections":
            matched += 1
            for d in res["diffs"]:
                print(f"[fix]  {slug}: input={d['input']!r} authored={d['authored']!r} -> canonical={d['canonical']!r}")
        else:
            print(f"[FAIL] {slug}: {res.get('error', 'case errors')}")

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "app", "data", "expected_outputs.json",
    )
    if check_only:
        total = len(report)
        ok = sum(1 for r in report.values() if r["status"] == "ok")
        print(f"\n{ok}/{total} problems fully consistent with authored answers")
        if ok < total:
            print("Run without --check to regenerate expected_outputs.json")
            return 1
        return 0

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nWrote {out_path} ({matched} problems graded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
