"""Intake lint — deterministic filler detection at the door.

Pure function, zero LLM, zero network. Applied to:
  1. POST /api/questions/submit (user submissions) — stubs rejected with 422,
     everything else enters as UNVERIFIED candidates as before.
  2. scripts/lint_intake.py batch spot-checks over file banks.

Three-state verdict (deliberately NOT a trust stamp):
  - "pass":         structurally complete intake.
  - "needs_work":   accepted as UNVERIFIED candidate with lint_flags
                     (e.g. missing test cases — curatable, not filler).
  - "rejected":     filler — stub bodies, formatter-as-solution,
                     template placeholders. Never enters any pool.

This lint screens INTAKE only. It never sets trust_status, never promotes,
never quarantines. Promotion still requires the trust pipeline
(automated execution -> human review -> tranche-approve).
"""
from __future__ import annotations

import ast
from typing import Any, Dict, List, Tuple

TEMPLATE_MARKERS = (
    "implement optimal solution here",
    "implement your solution here",
    "todo: implement",
    "your code here",
    "write your solution here",
)

# A sole function definition with one of these names is a serializer /
# pretty-printer, not a problem solution (evidence: nc-two-sum's `fmt`
# that formats values instead of solving two-sum).
FORMATTER_NAMES = {"fmt", "format", "format_output", "pretty", "pretty_print",
                   "display", "show", "dump", "stringify"}


def _text(v: Any) -> str:
    return str(v or "").strip()


def _func_defs(tree: ast.Module) -> list:
    return [n for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _is_literal_return_only(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True when the body does no computation: docstring/pass followed by
    a single `return <literal>` (evidence: `def largest(nums): return 0`)."""
    body = [n for n in fn.body if not isinstance(n, ast.Expr)]
    if len(body) != 1:
        return False
    node = body[0]
    if not isinstance(node, ast.Return) or node.value is None:
        return False
    return isinstance(node.value, (ast.Constant, ast.List, ast.Tuple,
                                   ast.Dict, ast.Set))


def _is_pass_only(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    body = [n for n in fn.body if not isinstance(n, ast.Expr)]
    return len(body) == 1 and isinstance(body[0], ast.Pass)


def _lint_coding_solution(code: str) -> List[str]:
    """Return rejection reasons (empty = solution acceptable)."""
    reasons: List[str] = []
    if not code:
        return ["missing_solution"]
    lowered = code.lower()
    for marker in TEMPLATE_MARKERS:
        if marker in lowered:
            return ["template_placeholder"]
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return ["solution_syntax_error"]
    fns = _func_defs(tree)
    if not fns:
        # Class-only / stdin-script style (pp-* wrappers define _pp_main,
        # which IS a FunctionDef, so reaching here means truly no defs).
        stmts = [n for n in tree.body
                 if not isinstance(n, (ast.Import, ast.ImportFrom, ast.Expr))]
        if not stmts:
            return ["no_executable_statements"]
        return []
    if all(_is_pass_only(f) for f in fns):
        return ["stub_pass_only_body"]
    if all(_is_literal_return_only(f) for f in fns):
        return ["stub_literal_return_only"]
    real = [f for f in fns if not _is_pass_only(f)
            and not _is_literal_return_only(f)]
    if not real:
        return ["stub_literal_return_only"]
    if (len(fns) == 1 and fns[0].name.lower() in FORMATTER_NAMES
            and not any(a.arg in ("self", "cls") for a in fns[0].args.args)):
        return ["formatter_not_solution"]
    return []


def _lint_mcq(doc: Dict[str, Any]) -> List[str]:
    """Mirror question_store._is_executable: dict-style (A-D keys) OR
    list-style (cs_fundamentals: >=4 entries + resolvable answer) both count."""
    reasons: List[str] = []
    options = doc.get("options")
    if isinstance(options, list):
        if len(options) < 4:
            return ["mcq_options_must_have_at_least_4_entries"]
        texts = [_text(o) for o in options]
        if any(not t for t in texts):
            reasons.append("mcq_empty_option_entry")
        correct_text = _text(doc.get("correct_answer"))
        correct_idx = doc.get("correct_index")
        ok = (isinstance(correct_idx, int) and 0 <= correct_idx < len(options))
        ok = ok or (bool(correct_text) and correct_text in texts)
        if not ok:
            reasons.append("mcq_unresolvable_correct_answer")
        return reasons
    if not isinstance(options, dict) or len(options) != 4:
        return ["mcq_options_must_have_exactly_4_entries"]
    for key in ("A", "B", "C", "D"):
        if key not in options or not _text(options.get(key)):
            reasons.append(f"mcq_missing_or_empty_option_{key}")
    correct = _text(doc.get("correct_answer") or doc.get("correct_index")).upper()
    if correct not in ("A", "B", "C", "D"):
        reasons.append(f"mcq_invalid_correct_answer_{correct}")
    return reasons


def lint_question(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Lint one question intake dict.

    Returns {"verdict": "pass"|"needs_work"|"rejected", "reasons": [...]}.
    """
    reasons: List[str] = []
    warnings: List[str] = []

    title = _text(doc.get("question") or doc.get("question_title")
                  or doc.get("title"))
    if not title or title.lower() in ("untitled", "question", "problem"):
        reasons.append("missing_question_text")

    qtype = _text(doc.get("type") or "coding").lower()
    if qtype == "coding":
        reasons.extend(_lint_coding_solution(
            _text((doc.get("solution") or {}).get("code"))
            if isinstance(doc.get("solution"), dict) else ""))
        if not (doc.get("test_cases") or doc.get("testcases")
                or doc.get("examples")):
            warnings.append("missing_test_cases_and_examples")
    elif qtype in ("aptitude", "logical", "verbal", "hr",
                   "cs_fundamentals", "cs"):
        reasons.extend(_lint_mcq(doc))
    elif qtype in ("interview", "behavioral", "system_design", "debugging",
                   "sql", "gd", "group_discussion"):
        # Structural completeness for open-ended/rubric types is the
        # verifier's job; intake only requires a statement (checked above).
        pass
    else:
        warnings.append(f"unknown_type_{qtype}")

    if reasons:
        return {"verdict": "rejected", "reasons": reasons,
                "warnings": warnings}
    if warnings:
        return {"verdict": "needs_work", "reasons": [],
                "warnings": warnings}
    return {"verdict": "pass", "reasons": [], "warnings": []}


def lint_batch(docs: List[Dict[str, Any]]) -> Tuple[Dict[str, int], List[Dict[str, Any]]]:
    """Lint many docs. Returns (counts, rejected_details)."""
    counts = {"pass": 0, "needs_work": 0, "rejected": 0}
    rejected: List[Dict[str, Any]] = []
    for doc in docs:
        try:
            res = lint_question(doc if isinstance(doc, dict) else {})
        except Exception as e:
            res = {"verdict": "rejected",
                   "reasons": [f"lint_exception_{type(e).__name__}"],
                   "warnings": []}
        counts[res["verdict"]] += 1
        if res["verdict"] == "rejected":
            rejected.append({
                "id": doc.get("id") if isinstance(doc, dict) else None,
                "title": _text((doc.get("question") or "")[:80]) if isinstance(doc, dict) else "",
                "type": doc.get("type") if isinstance(doc, dict) else None,
                "source_bank": doc.get("source_bank") if isinstance(doc, dict) else None,
                "reasons": res["reasons"],
            })
    return counts, rejected
