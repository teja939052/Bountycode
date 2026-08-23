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
        return json.dumps([_canon(x) for x in v], separators=(",", ":"))
    if v is None:
        return "None"
    return str(v)


async def grade_problem(slug: str, problem: dict, ref: dict) -> dict:
    cases = problem.get("test_cases", [])
    code = ref["python"]
    stdins = [tc.get("input", "") for tc in cases]

    harness = (
        "import ast, json, sys\n"
        "_CODE = " + repr(code) + "\n"
        "_CASES = json.loads(" + repr(json.dumps(stdins)) + ")\n"
        "exec(compile(_CODE, '<ref>', 'exec'), _NS := {'__name__': '__main__'})\n"
        "_FN = _NS[" + repr(ref["function_name"]) + "]\n"
        "_OUT = []\n"
        "for _raw in _CASES:\n"
        "    try:\n"
        "        _args = ast.literal_eval('(' + _raw + ')') if _raw.strip() else ()\n"
        "        if not isinstance(_args, tuple):\n"
        "            _args = (_args,)\n"
        "        _OUT.append([True, repr(_FN(*_args))])\n"
        "    except BaseException as _e:\n"
        "        _OUT.append([False, '%s: %s' % (type(_e).__name__, _e)])\n"
        "sys.stdout.write('<<ORACLE>>' + json.dumps(_OUT))\n"
    )

    # Reuse the sandbox subprocess machinery by embedding our harness AS the code
    result = await execute_local_python_batch(harness, [""], timeout=15)
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
        computed = ""
        status = "error"
        if ok:
            import ast as _ast
            try:
                computed = _canon(_ast.literal_eval(value))
                status = "match" if computed == authored else "mismatch"
            except (ValueError, SyntaxError):
                computed = value
                status = "unparseable_return"
        outputs.append({
            "input": case.get("input", ""),
            "authored_expected": authored,
            "computed_expected": computed,
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
                print(f"[fix]  {slug}: input={d['input']!r} authored={d['authored']!r} → canonical={d['canonical']!r}")
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
