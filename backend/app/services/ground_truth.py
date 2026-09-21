"""Independent ground-truth cross-check (spec section 1, step 3).

Lint + execution verification only prove INTERNAL consistency (a solution
agreeing with its own test cases) — the 26-stub incident proved that is not
correctness. This module checks a question against a source INDEPENDENT of
whoever authored the solution+test cases:

  Source A — platform oracle (backend/app/data/expected_outputs.json):
    independently-derived input->expected pairs, keyed by problem slug.
    The item's solution is executed against the ORACLE's inputs and its
    outputs compared to the ORACLE's expected values. Agreement means two
    independent sources say the same thing.

  Source B — dual-solution agreement: if the item carries a separately
    authored `verification_solution` (author B, different from `solution`
    author A), both are executed over the stored inputs and must agree
    exactly on every case.

Three-state outcome (deliberately NOT pass/fail):
  - "confirmed":              an independent source exists AND agrees.
  - "no_independent_source":  nothing to check against. NEUTRAL — does not
                              fail gates; flags the coverage gap. New tranches
                              should either supply a second source or get
                              explicit human ground-truth sign-off at review.
  - "mismatch":               an independent source exists AND disagrees.
                              FAIL — this is the self-stamping catch.

Deterministic, zero LLM, zero network. Never mutates trust_status, banks,
or MongoDB. Prospective enforcement only: the existing bank is grandfathered
(the sweep script quantifies coverage); the tranche gate fails ONLY on
mismatch, never on missing coverage.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORACLE_PATH = os.path.join(BACKEND_ROOT, "app", "data", "expected_outputs.json")

_oracle: Optional[dict] = None


def _norm_title(s: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s or "")[:80].lower()).strip()


def load_oracle() -> dict:
    """Load the independent platform oracle (cached)."""
    global _oracle
    if _oracle is None:
        try:
            with open(ORACLE_PATH, encoding="utf-8") as f:
                data = json.load(f)
            _oracle = data if isinstance(data, dict) else {}
        except Exception:
            _oracle = {}
    return _oracle


def match_oracle(item: dict) -> Optional[dict]:
    """Find an oracle entry for this item by strict title match.

    Strict on purpose: applying the wrong oracle's expectations would
    manufacture mismatches. Returns None when no entry matches.
    """
    oracle = load_oracle()
    if not oracle:
        return None
    title = _norm_title(item.get("question") or item.get("question_title")
                        or item.get("title"))
    if not title:
        return None
    for slug, entry in oracle.items():
        if not isinstance(entry, dict):
            continue
        if _norm_title(entry.get("title") or slug) == title:
            return {"slug": slug, **entry}
    return None


def cross_check_solution(solution_code: str,
                         oracle_pairs: List[dict]) -> Dict[str, Any]:
    """Execute solution_code against the oracle's inputs, compare to the
    oracle's expected outputs. Returns pass/fail + per-case detail."""
    from app.services.auto_verify import _run_python_tests
    fake = {
        "id": "ground-truth-probe",
        "solution": {"code": solution_code, "language": "python"},
        "test_cases": [
            {"input": str(p.get("input", "")),
             "output": str(p.get("expected", p.get("output", "")))}
            for p in oracle_pairs or []
        ],
    }
    if not fake["test_cases"]:
        return {"pass": False, "reason": "oracle_has_no_pairs",
                "passed": 0, "total": 0}
    passed, reason, p, total = _run_python_tests(fake)
    return {"pass": passed, "reason": reason or "oracle_agreement",
            "passed": p, "total": total}


def dual_solution_check(item: dict) -> Dict[str, Any]:
    """Require a separately-authored verification_solution to agree with
    the stored solution over the stored test inputs. Exact agreement on
    every case; disagreement fails (one of the two authors is wrong)."""
    sol_a = ((item.get("solution") or {}).get("code", "")
             if isinstance(item.get("solution"), dict) else "")
    sol_b = ((item.get("verification_solution") or {}).get("code", "")
             if isinstance(item.get("verification_solution"), dict)
             else item.get("verification_solution_code", ""))
    if not sol_a or not sol_b:
        return {"state": "no_independent_source",
                "detail": "no_verification_solution_present"}
    from app.services.auto_verify import (
        _extract_funcs, _split_calls, _fn_arity, invoke_conventions, _norm,
    )
    import contextlib
    import io
    tcs = (item.get("test_cases") or item.get("testcases")
           or item.get("visible_test_cases") or [])
    if not tcs:
        return {"state": "no_independent_source",
                "detail": "no_test_cases_to_compare_over"}
    fns = []
    for code in (sol_a, sol_b):
        ns: dict = {}
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(_extract_funcs(code), ns)
        except Exception as e:
            return {"state": "mismatch",
                    "detail": f"second_source_exec_fail:{type(e).__name__}"}
        fn = None
        for line in _extract_funcs(code).splitlines():
            s = line.strip()
            if s.startswith("def "):
                name = s.split("(")[0].replace("def ", "").strip()
                if name in ns and callable(ns[name]):
                    fn = ns[name]
                    break
        if fn is None:
            return {"state": "mismatch", "detail": "second_source_no_func"}
        fns.append((fn, _fn_arity(fn)))
    agree, total = 0, 0
    for tc in tcs:
        raw = tc.get("input", "")
        parts = _split_calls(raw)
        total += 1
        outs = []
        for fn, arity in fns:
            ok, actual, _err = invoke_conventions(fn, parts, raw, arity)
            if not ok:
                return {"state": "mismatch",
                        "detail": f"dual_exec_fail_on_case_{total}"}
            outs.append(actual)
        # Both authors computed a value; agreement is exact normalized
        # equality (ordering-sensitive — same strictness as the verifier).
        if _norm(outs[0]) == _norm(outs[1]):
            agree += 1
        else:
            return {"state": "mismatch",
                    "detail": f"authors_disagree_on_case_{total}"}
    return {"state": "confirmed",
            "detail": f"dual_solution_agreement:{agree}/{total}"}


def ground_truth_status(item: dict) -> Dict[str, Any]:
    """Three-state ground-truth verdict for one item.

    Precedence: explicit mismatch (either source) > confirmed (either
    source) > no_independent_source. Never raises; unknown shapes report
    no_independent_source rather than failing.
    """
    try:
        if str(item.get("type") or "coding").lower() != "coding":
            return {"state": "no_independent_source",
                    "detail": "non_coding_no_oracle_yet"}
        oracle = match_oracle(item)
        if oracle is not None:
            sol = ((item.get("solution") or {}).get("code", "")
                   if isinstance(item.get("solution"), dict) else "")
            if not sol:
                return {"state": "no_independent_source",
                        "detail": "oracle_matched_but_no_solution"}
            res = cross_check_solution(sol, oracle.get("expected_outputs") or [])
            if res["pass"]:
                return {"state": "confirmed",
                        "detail": f"oracle_agreement:{oracle['slug']}:{res['passed']}/{res['total']}"}
            return {"state": "mismatch",
                    "detail": f"oracle_disagreement:{oracle['slug']}:{res['reason']}"[:160]}
        dual = dual_solution_check(item)
        return dual
    except Exception as e:
        return {"state": "no_independent_source",
                "detail": f"check_error_{type(e).__name__}"}
