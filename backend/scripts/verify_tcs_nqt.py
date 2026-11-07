"""Verify all TCS NQT questions and produce serveable verified banks.

This script:
1. Normalizes `questions/tcs_nqt_all.json` MCQs into the canonical schema.
2. Runs deterministic structural checks on every TCS NQT entry.
3. Executes coding test cases where present.
4. Writes:
   - `app/data/tcs_nqt_mcq_verified.json`  (auto-checked MCQs)
   - `app/data/tcs_nqt_coding_auto_verified.json` (auto-checked coding)
   - `app/data/tcs_nqt_verification_report.json` (full report)
"""
from __future__ import annotations

import json
import logging
import os
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")
_QUESTIONS_DIR = os.path.join(_DATA_DIR, "questions")

_TCS_ALL = os.path.join(_QUESTIONS_DIR, "tcs_nqt_all.json")
_TCS_RAW = os.path.join(_DATA_DIR, "tcs_nqt_questions.json")
_OUT_MCQ = os.path.join(_DATA_DIR, "tcs_nqt_mcq_verified.json")
_OUT_CODING = os.path.join(_DATA_DIR, "tcs_nqt_coding_auto_verified.json")
_OUT_REPORT = os.path.join(_DATA_DIR, "tcs_nqt_verification_report.json")


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def _norm_mcq(q: Dict[str, Any]) -> Dict[str, Any]:
    content = q.get("content") or {}
    if not isinstance(content, dict):
        content = {}

    options = content.get("options") or []
    if isinstance(options, dict):
        options = [options[k] for k in sorted(options.keys()) if k in ("A", "B", "C", "D", "a", "b", "c", "d")]

    companies = []
    cr = q.get("company_relevance") or {}
    if isinstance(cr, dict):
        companies = [k for k, v in cr.items() if isinstance(v, (int, float)) and v > 0.5]
    if not companies:
        companies = ["TCS"]

    return {
        "id": str(q.get("id") or ""),
        "type": "aptitude",
        "question": str(q.get("question") or content.get("question") or "").strip(),
        "question_title": str(q.get("question") or content.get("question") or "")[:80].strip(),
        "topic": str(q.get("domain") or q.get("topic") or q.get("pattern") or "General").strip(),
        "sub_topic": str(q.get("skill") or q.get("sub_topic") or "").strip(),
        "difficulty": str(q.get("difficulty") or "medium").strip(),
        "companies": companies,
        "role": q.get("role") or ["campus"],
        "options": options,
        "correct_answer": str(content.get("correct_answer") or "").strip(),
        "explanation": str(content.get("explanation") or q.get("hints") or "").strip(),
        "worked_solution": str(content.get("explanation") or q.get("hints") or "").strip(),
        "trick": str(q.get("common_mistakes") or "").strip() or "None",
        "test_cases": [],
        "source_bank": "tcs_nqt_mcq_verified",
        "provenance": "TCS NQT Pattern — Original Composition",
        "trust_status": "unverified",
    }


def _norm_coding(q: Dict[str, Any]) -> Dict[str, Any]:
    tcs = q.get("testcases") or q.get("test_cases") or q.get("visible_test_cases") or []
    normalized_tcs = []
    for tc in tcs:
        if isinstance(tc, dict):
            normalized_tcs.append({
                "input": str(tc.get("input") or tc.get("stdin") or ""),
                "output": str(tc.get("output") or tc.get("expected") or tc.get("expected_output") or ""),
                "hidden": bool(tc.get("hidden") or tc.get("is_hidden") or False),
            })

    companies = q.get("company") or []
    if isinstance(companies, str):
        companies = [companies]
    if not companies:
        companies = ["TCS"]

    return {
        "id": str(q.get("id") or ""),
        "type": "coding",
        "question": str(q.get("question") or q.get("question_title") or q.get("title") or "").strip(),
        "question_title": str(q.get("question_title") or q.get("title") or q.get("question") or "")[:80].strip(),
        "topic": str(q.get("topic") or q.get("sub_topic") or "Coding").strip(),
        "sub_topic": str(q.get("sub_topic") or q.get("topic") or "").strip(),
        "difficulty": str(q.get("difficulty") or "medium").strip(),
        "companies": companies,
        "role": q.get("role") or ["campus"],
        "test_cases": normalized_tcs,
        "solution": q.get("solution") or {},
        "function_name": q.get("function_name") or "",
        "function_params": q.get("function_params") or [],
        "constraints": q.get("constraints") or [],
        "examples": q.get("examples") or [],
        "hints": q.get("hints") or [],
        "source_bank": "tcs_nqt_questions",
        "provenance": "TCS NQT Pattern — Original Composition",
        "trust_status": "unverified",
    }


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------

def _check_mcq(q: Dict[str, Any]) -> Tuple[bool, str]:
    options = q.get("options") or []
    if not isinstance(options, list) or len(options) < 2:
        return False, "missing_options"
    correct = str(q.get("correct_answer") or "").strip()
    if not correct:
        return False, "missing_correct_answer"
    if correct not in [str(o).strip() for o in options]:
        return False, f"correct_answer_not_in_options:{correct!r}"
    question = str(q.get("question") or "").strip()
    if len(question) < 10:
        return False, "question_too_short"
    return True, "ok"


def _check_coding(q: Dict[str, Any]) -> Tuple[bool, str]:
    tcs = q.get("test_cases") or []
    if not tcs:
        return False, "missing_test_cases"
    sol = q.get("solution") or {}
    sol_code = str(sol.get("code") or "") if isinstance(sol, dict) else ""
    if not sol_code or "implement optimal" in sol_code.lower():
        return False, "missing_or_placeholder_solution"
    question = str(q.get("question") or q.get("question_title") or "").strip()
    if len(question) < 5:
        return False, "missing_question_text"
    return True, "ok"


# ---------------------------------------------------------------------------
# Coding execution check
# ---------------------------------------------------------------------------

def _run_coding_tests(q: Dict[str, Any]) -> Tuple[bool, str, int, int]:
    """Execute coding question solution against test cases."""
    sol = q.get("solution") or {}
    if not isinstance(sol, dict):
        return False, "no_solution_dict", 0, len(q.get("test_cases") or [])
    sol_code = str(sol.get("code") or "")
    if not sol_code:
        return False, "no_solution_code", 0, len(q.get("test_cases") or [])

    tcs = q.get("test_cases") or []
    if not tcs:
        return False, "no_test_cases", 0, 0

    # Extract function from solution
    src = sol_code
    ns: Dict[str, Any] = {}
    try:
        import ast
        tree = ast.parse(src)
        parts = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
                try:
                    parts.append(ast.unparse(node))
                except Exception:
                    pass
        src = "\n".join(parts) if parts else sol_code
        exec(compile(ast.parse(src), "<verify>", "exec"), ns)
    except Exception as e:
        return False, f"exec_fail:{type(e).__name__}:{str(e)[:80]}", 0, len(tcs)

    fn_name = None
    fn_obj = None
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("def "):
            candidate = s.split("(")[0].replace("def ", "").strip()
            if candidate in ns and callable(ns[candidate]):
                if candidate == "main":
                    continue
                fn_name = candidate
                fn_obj = ns[candidate]
                break
    if not fn_name or not fn_obj:
        return False, "no_callable_found", 0, len(tcs)

    import inspect
    arity = len([p for p in inspect.signature(fn_obj).parameters.values()
                 if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)])

    passed = 0
    reason = ""
    for tc in tcs:
        raw_input = str(tc.get("input", "") or "").strip()
        exp = str(tc.get("output", "") or "").strip()

        def _parse_value(s: str) -> Any:
            import ast as _ast
            try:
                return _ast.literal_eval(s)
            except Exception:
                return s

        def _norm(x: Any) -> str:
            if isinstance(x, float):
                return repr(round(x, 6))
            if isinstance(x, (list, tuple)):
                return "[" + ",".join(_norm(v) for v in x) + "]"
            return str(x).strip()

        def _values_equal(actual: Any, expected_raw: Any) -> bool:
            exp = _parse_value(expected_raw)
            if isinstance(actual, str) and not isinstance(exp, str):
                parsed = _parse_value(actual)
                if not isinstance(parsed, str):
                    actual = parsed
            return _norm(actual) == _norm(exp)

        parts = [_parse_value(p) for p in raw_input.split("\n")] if "\n" in raw_input else [_parse_value(raw_input)]

        actual = None
        invoked = False
        chain_error = ""
        try:
            if len(parts) == 1 and isinstance(parts[0], dict):
                try:
                    actual = fn_obj(**parts[0])
                except TypeError:
                    actual = fn_obj(*parts[0].values())
            elif len(parts) > 1:
                try:
                    actual = fn_obj(*parts)
                except TypeError:
                    actual = fn_obj(parts)
            else:
                inp = parts[0]
                try:
                    actual = fn_obj(inp)
                except TypeError:
                    actual = fn_obj(*inp) if isinstance(inp, list) else fn_obj(inp)
            invoked = True
        except Exception as e:
            chain_error = f"{type(e).__name__}:{e}"[:120]

        if not invoked and arity == 1 and raw_input:
            try:
                actual = fn_obj(raw_input)
                invoked = True
                chain_error = ""
            except Exception as e:
                chain_error = f"{type(e).__name__}:{e}"[:120]

        matched = invoked and _values_equal(actual, exp)
        if matched:
            passed += 1
        elif not reason:
            reason = chain_error or f"mismatch:expected={exp!r} got={_norm(actual)!r}"[:120]

    if passed == len(tcs):
        return True, "all_tests_pass", passed, len(tcs)
    return False, reason or "mismatch", passed, len(tcs)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tcs_nqt_all": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "details": []},
        "tcs_nqt_questions": {"total": 0, "passed": 0, "failed": 0, "quarantined": 0, "skipped": 0, "details": []},
        "summary": {},
    }

    verified_mcqs: List[Dict[str, Any]] = []
    verified_coding: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # 1. Process tcs_nqt_all.json (2472 MCQs)
    # ------------------------------------------------------------------
    if os.path.exists(_TCS_ALL):
        with open(_TCS_ALL, "r", encoding="utf-8") as f:
            raw_mcqs = json.load(f)

        mcq_report = report["tcs_nqt_all"]
        mcq_report["total"] = len(raw_mcqs)

        for q in raw_mcqs:
            normed = _norm_mcq(q)
            ok, reason = _check_mcq(normed)
            if ok:
                normed["trust_status"] = "automated_checked"
                normed["verified_at"] = datetime.now(timezone.utc).isoformat()
                normed["verified_by"] = "auto_verify_tcs_nqt"
                normed["verification_version"] = "automated_checked_v1"
                verified_mcqs.append(normed)
                mcq_report["passed"] += 1
            else:
                normed["trust_status"] = "quarantined"
                normed["verification_failure"] = reason
                mcq_report["failed"] += 1
                mcq_report["details"].append({"id": normed["id"], "reason": reason})

        logger.info("MCQ bank: %d total, %d passed, %d failed", mcq_report["total"], mcq_report["passed"], mcq_report["failed"])
    else:
        logger.warning("Missing %s", _TCS_ALL)

    # ------------------------------------------------------------------
    # 2. Process tcs_nqt_questions.json (450 mixed)
    # ------------------------------------------------------------------
    if os.path.exists(_TCS_RAW):
        with open(_TCS_RAW, "r", encoding="utf-8") as f:
            raw_questions = json.load(f)

        q_report = report["tcs_nqt_questions"]
        q_report["total"] = len(raw_questions)

        for q in raw_questions:
            qtype = str(q.get("type") or "").lower()
            if qtype == "coding":
                normed = _norm_coding(q)
                ok, reason = _check_coding(normed)
                if not ok:
                    normed["trust_status"] = "quarantined"
                    normed["verification_failure"] = reason
                    q_report["quarantined"] += 1
                    q_report["details"].append({"id": normed["id"], "reason": f"structural:{reason}"})
                    continue

                passed, reason, passed_count, total_count = _run_coding_tests(normed)
                if passed:
                    normed["trust_status"] = "automated_checked"
                    normed["verified_at"] = datetime.now(timezone.utc).isoformat()
                    normed["verified_by"] = "auto_verify_tcs_nqt"
                    normed["verification_version"] = "automated_checked_v1"
                    normed.pop("verification_failure", None)
                    verified_coding.append(normed)
                    q_report["passed"] += 1
                else:
                    normed["trust_status"] = "quarantined"
                    normed["verification_failure"] = reason
                    q_report["failed"] += 1
                    q_report["details"].append({"id": normed["id"], "reason": f"test_fail:{reason}"})
            else:
                # aptitude / cs / logical / verbal without proper MCQ format => quarantine
                normed = _norm_coding(q)
                normed["type"] = qtype or "unknown"
                normed["trust_status"] = "quarantined"
                normed["verification_failure"] = "non_coding_without_mcq_format"
                q_report["quarantined"] += 1
                q_report["details"].append({"id": normed["id"], "type": qtype, "reason": "non_coding_without_mcq_format"})

        logger.info("Mixed bank: %d total, %d passed, %d failed, %d quarantined",
                     q_report["total"], q_report["passed"], q_report["failed"], q_report["quarantined"])
    else:
        logger.warning("Missing %s", _TCS_RAW)

    # ------------------------------------------------------------------
    # 3. Write outputs
    # ------------------------------------------------------------------
    with open(_OUT_MCQ, "w", encoding="utf-8") as f:
        json.dump(verified_mcqs, f, ensure_ascii=False, indent=2)
    logger.info("Wrote %d verified MCQs to %s", len(verified_mcqs), _OUT_MCQ)

    with open(_OUT_CODING, "w", encoding="utf-8") as f:
        json.dump(verified_coding, f, ensure_ascii=False, indent=2)
    logger.info("Wrote %d verified coding questions to %s", len(verified_coding), _OUT_CODING)

    report["summary"] = {
        "mcq_verified": len(verified_mcqs),
        "coding_verified": len(verified_coding),
        "total_verified": len(verified_mcqs) + len(verified_coding),
        "output_files": [_OUT_MCQ, _OUT_CODING, _OUT_REPORT],
    }

    with open(_OUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    logger.info("Wrote report to %s", _OUT_REPORT)

    return report


if __name__ == "__main__":
    main()
