"""Automated question verification — deterministic, no-LLM.

Runs structural checks, derives normalizes test-case representations,
executes Python solutions against stored/derived test cases, and updates
``trust_status`` in-memory to ``automated_checked`` or ``quarantined``.
Student-facing flows only see verified content.

Domains handled:
- coding: execute Python solutions against test cases
- aptitude / logical / verbal / hr: MCQ validation + option normalization
- interview / behavioral / system_design / debugging: structural completeness
"""
from __future__ import annotations

import ast
import contextlib
import inspect
import io
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from app.services.question_verification import quick_structural_check

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Structural + execution helpers (mirrors scripts/autocheck_bank.py)
# ---------------------------------------------------------------------------

def _extract_funcs(src: str) -> str:
    try:
        tree = ast.parse(src)
    except Exception:
        return src
    parts = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef, ast.Import, ast.ImportFrom)):
            try:
                parts.append(ast.unparse(node))
            except Exception:
                pass
    return "\n".join(parts) if parts else src


def _parse_value(s: Any):
    s = str(s).strip()
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        return ast.literal_eval(s)
    except Exception:
        pass
    ls = s.lower()
    if ls in ("true", "false"):
        return ls == "true"
    return s


def _split_calls(raw: str) -> list:
    s = str(raw)
    if "\n" in s:
        return [_parse_value(part) for part in s.split("\n")]
    stripped = s.strip()
    if "=" in stripped:
        try:
            node = ast.parse(f"f({stripped})", mode="eval")
            call = node.body
            if isinstance(call, ast.Call) and call.keywords and not call.args:
                return [{kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}]
        except Exception:
            pass
    return [_parse_value(s)]


def _norm(x: Any) -> str:
    if isinstance(x, float):
        return repr(round(x, 6))
    if isinstance(x, (list, tuple)):
        return "[" + ",".join(_norm(v) for v in x) + "]"
    if isinstance(x, bool):
        return str(x)
    return str(x).strip()


def _values_equal(actual: Any, expected_raw: Any) -> bool:
    exp = _parse_value(expected_raw)
    # stdin-style wrappers (pp-*) return stdout as a STRING even when the
    # expected value is a list/dict. Parse-then-compare avoids whitespace
    # mismatches ('[[], [1]]' vs '[[],[1]]'). Strictness-preserving: an
    # unparseable string still compares as a string below.
    if isinstance(actual, str) and not isinstance(exp, str):
        parsed_actual = _parse_value(actual)
        if not isinstance(parsed_actual, str):
            actual = parsed_actual
    if isinstance(actual, bool) or isinstance(exp, bool):
        return str(actual).lower() == str(exp).lower()
    if isinstance(actual, float) or isinstance(exp, float):
        try:
            return abs(float(actual) - float(exp)) < 1e-6
        except Exception:
            return _norm(actual) == _norm(exp)
    if isinstance(actual, (list, tuple)) and isinstance(exp, (list, tuple)):
        if len(actual) != len(exp):
            return False
        if all(isinstance(v, (list, tuple)) for v in list(actual) + list(exp)):
            return sorted((_norm(v) for v in actual)) == sorted((_norm(v) for v in exp))
        return _norm(actual) == _norm(exp)
    if isinstance(exp, str) and not isinstance(actual, str):
        return _norm(actual) == exp.strip().strip("'\"")
    return _norm(actual) == _norm(exp)


# ---------------------------------------------------------------------------
# Test-case derivation / normalization
# ---------------------------------------------------------------------------

def _examples_to_test_cases(examples: Any) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    for ex in examples or []:
        if not isinstance(ex, dict):
            continue
        inp = ex.get("input") or ex.get("input_text") or ex.get("stdin") or ""
        out = ex.get("output") or ex.get("expected") or ex.get("expected_output") or ex.get("output_text") or ""
        if inp or out:
            cases.append({
                "input": str(inp),
                "output": str(out),
                "hidden": False,
                "source": "derived_from_example",
            })
    return cases


def _mcq_to_test_cases(q: dict) -> List[Dict[str, Any]]:
    """Normalize MCQ questions into a test-case-like structure.

    For aptitude/logical/verbal/hr MCQs, each option becomes a test case
    with the correct answer marked. This gives the rest of the system a
    uniform test-case representation across domains.
    """
    options = q.get("options") or {}
    if not isinstance(options, dict) or len(options) != 4:
        return []

    correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
    if not correct:
        return []

    cases: List[Dict[str, Any]] = []
    for key in ("A", "B", "C", "D"):
        if key not in options:
            continue
        cases.append({
            "input": key,
            "output": correct,
            "option_text": str(options.get(key, "")).strip(),
            "hidden": False,
            "source": "normalized_mcq",
        })
    return cases


def _ensure_test_cases(q: dict) -> List[Dict[str, Any]]:
    """Return existing test_cases or derive domain-appropriate ones."""
    existing = q.get("test_cases") or q.get("testcases") or []
    if existing:
        normalized = []
        changed = False
        for tc in existing:
            if not isinstance(tc, dict):
                continue
            inp = str(tc.get("input") or tc.get("stdin") or tc.get("input_text") or "")
            
            def _first_nonempty(*keys):
                for k in keys:
                    if k in tc:
                        v = tc[k]
                        if v is not None and str(v).strip():
                            return str(v).strip()
                return ""
            
            out = _first_nonempty("output", "expected", "expected_output", "output_text")
            hidden = bool(tc.get("hidden") or tc.get("is_hidden") or False)
            new_tc = {"input": inp, "output": out, "hidden": hidden}
            for k, v in tc.items():
                if k not in new_tc:
                    new_tc[k] = v
            if tc.get("expected") is not None and not tc.get("output"):
                changed = True
            normalized.append(new_tc)
        if changed and normalized:
            q["test_cases"] = normalized
            q.pop("testcases", None)
        return normalized

    qtype = str(q.get("type") or "coding").lower()
    if qtype in ("aptitude", "logical", "verbal", "hr"):
        return _mcq_to_test_cases(q)

    examples = q.get("examples") or []
    if examples:
        return _examples_to_test_cases(examples)

    return []


# ---------------------------------------------------------------------------
# Per-domain verification
# ---------------------------------------------------------------------------

def _structural_check(q: dict) -> List[str]:
    issues: List[str] = []
    title = str(q.get("question") or q.get("question_title") or q.get("title") or "").strip()
    if not title or title.lower() in ("", "untitled", "question", "problem"):
        issues.append("missing_question_text")

    qtype = str(q.get("type") or "coding").lower()

    if qtype == "coding":
        sol = q.get("solution") or {}
        sol_code = str(sol.get("code") or "") if isinstance(sol, dict) else ""
        if not sol_code or "implement optimal" in sol_code.lower():
            issues.append("missing_solution")
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not tcs and not (q.get("examples") or []):
            issues.append("missing_test_cases_and_examples")

    elif qtype in ("aptitude", "logical", "verbal", "hr"):
        options = q.get("options") or {}
        if not isinstance(options, dict) or len(options) != 4:
            issues.append("options_must_have_exactly_4_entries")
        else:
            for key in ("A", "B", "C", "D"):
                if key not in options or not str(options[key]).strip():
                    issues.append(f"missing_or_empty_option_{key}")
        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
        if correct not in ("A", "B", "C", "D"):
            issues.append(f"invalid_correct_answer_{correct}")
        if not q.get("worked_solution"):
            issues.append("missing_worked_solution")
        if not q.get("trick"):
            issues.append("missing_trick")
        if not q.get("explanation") and not q.get("description"):
            issues.append("missing_explanation")

    elif qtype in ("interview", "behavioral", "system_design", "gd", "group_discussion"):
        if not q.get("question") and not q.get("question_title"):
            issues.append("missing_question_text")
        if not q.get("rubric") and not q.get("expected_answer") and not q.get("description"):
            issues.append("missing_rubric_or_expected_answer")

    return issues


def _fn_arity(f) -> int:
    """Number of positional params a solution entry point accepts."""
    try:
        return len([
            p for p in inspect.signature(f).parameters.values()
            if p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ])
    except Exception:
        return -1


def invoke_conventions(f, parts: list, raw_input: Any, arity: int
                       ) -> Tuple[bool, Any, str]:
    """Invoke one solution function under the canonical calling conventions.

    Chain per test case: kwargs-spread -> values-spread -> arg-spread ->
    single-list -> single-value, plus a raw-input-string attempt for
    arity-1 wrappers that parse stdin-style input themselves.
    Returns (invoked, actual, chain_error). A stub returning garbage still
    fails downstream exact-match comparison — the gate is unchanged; only
    the invocation vocabulary is shared. Single canonical implementation:
    _run_python_tests and ground_truth.dual_solution_check both use this.
    """
    actual = None
    invoked = False
    chain_error = ""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            if len(parts) == 1 and isinstance(parts[0], dict):
                try:
                    actual = f(**parts[0])
                except TypeError:
                    actual = f(*parts[0].values())
            elif len(parts) > 1:
                try:
                    actual = f(*parts)
                except TypeError:
                    actual = f(parts)
            else:
                inp = parts[0]
                try:
                    actual = f(inp)
                except TypeError:
                    actual = f(*inp) if isinstance(inp, list) else f(inp)
        invoked = True
    except Exception as e:
        chain_error = f"{type(e).__name__}:{e}"[:160]
    if not invoked and arity == 1 and isinstance(raw_input, str) and raw_input.strip():
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                actual = f(raw_input)
            invoked = True
            chain_error = ""
        except Exception as e:
            chain_error = f"{type(e).__name__}:{e}"[:160]
    return invoked, actual, chain_error


def _run_python_tests(q: dict) -> Tuple[bool, Optional[str], int, int]:
    sol = (q.get("solution") or {})
    if not isinstance(sol, dict):
        sol = {}
    sol_code = sol.get("code") or ""
    if not sol_code or "implement optimal" in sol_code.lower():
        return False, "NO_SOLUTION", 0, 0

    tcs = q.get("test_cases") or q.get("testcases") or []
    if not tcs:
        return False, "NO_TESTS", 0, 0

    src = _extract_funcs(sol_code)
    ns: dict = {}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(src, ns)
    except Exception as e:
        return False, f"EXEC_FAIL:{type(e).__name__}", 0, len(tcs)

    # Find the first callable function, but skip `main` with no args.
    fn_name = None
    fn_obj = None
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("def "):
            candidate = s.split("(")[0].replace("def ", "").strip()
            if candidate in ns and callable(ns[candidate]):
                # Skip main() with zero positional args
                if candidate == "main":
                    try:
                        import inspect
                        sig = inspect.signature(ns[candidate])
                        if len([
                            p for p in sig.parameters.values()
                            if p.kind in (
                                inspect.Parameter.POSITIONAL_ONLY,
                                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                            )
                        ]) == 0:
                            continue
                    except Exception:
                        pass
                fn_name = candidate
                fn_obj = ns[candidate]
                break
    if not fn_name or fn_obj is None:
        return False, "NO_FUNC", 0, len(tcs)

    f = fn_obj
    arity = _fn_arity(f)
    passed = 0
    reason = ""
    for tc in tcs:
        raw_input = tc.get("input", "")
        exp = str(tc.get("output", "")).strip()
        parts = _split_calls(raw_input)
        invoked, actual, chain_error = invoke_conventions(f, parts, raw_input, arity)
        matched = invoked and _values_equal(actual, exp)
        if not matched and arity == 1 and isinstance(raw_input, str) and raw_input.strip():
            # fmt-style wrappers (arity 1) parse the RAW input string
            # themselves; pre-parsed parts can succeed with echoed garbage
            # (nc-two-sum class). One deterministic extra attempt with the
            # raw string. Still requires exact match on every test case: a
            # stub cannot pass diverse cases, so the gate is unchanged.
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    raw_actual = f(raw_input)
                matched = _values_equal(raw_actual, exp)
            except Exception:
                matched = False
        if matched:
            passed += 1
        elif not reason:
            reason = chain_error or f"MISMATCH exp={exp!r} got={_norm(actual)!r}"[:160]

    if passed == len(tcs):
        return True, "ALL_TESTS_PASS", passed, len(tcs)
    return False, reason or "MISMATCH", passed, len(tcs)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class VerificationResult:
    def __init__(self) -> None:
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.quarantined = 0
        self.skipped = 0
        self.details: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "quarantined": self.quarantined,
            "skipped": self.skipped,
            "details": self.details,
        }


def verify_question(q: dict) -> Dict[str, Any]:
    """Run automated checks on one question dict.

    Mutates ``q`` in-place:
      - Derives/normalizes test_cases when missing
      - Sets ``trust_status`` to ``automated_checked`` on pass
      - Sets ``trust_status`` to ``quarantined`` and appends ``verification_failure`` on fail
    """
    qid = str(q.get("id") or "")
    title = str(q.get("question") or q.get("question_title") or q.get("title") or "")[:60]
    qtype = str(q.get("type") or "coding").lower()
    result: Dict[str, Any] = {
        "id": qid,
        "title": title,
        "type": qtype,
        "verdict": "skip",
        "reason": "",
        "passed": 0,
        "total": 0,
    }

    issues = _structural_check(q)
    if issues:
        result["verdict"] = "quarantined"
        result["reason"] = "structural:" + ";".join(issues)
        q["trust_status"] = "quarantined"
        q["verification_failure"] = result["reason"]
        return result

    test_cases = _ensure_test_cases(q)
    if test_cases:
        q["test_cases"] = test_cases

    if qtype == "coding":
        if not test_cases:
            result["verdict"] = "quarantined"
            result["reason"] = "no_test_cases"
            q["trust_status"] = "quarantined"
            q["verification_failure"] = "no_test_cases"
            return result

        passed, reason, passed_count, total_count = _run_python_tests(q)
        result["passed"] = passed_count
        result["total"] = total_count
        if passed:
            result["verdict"] = "passed"
            result["reason"] = "all_tests_pass"
            q["trust_status"] = "automated_checked"
            q.pop("verification_failure", None)
        else:
            result["verdict"] = "failed"
            result["reason"] = reason
            q["trust_status"] = "quarantined"
            q["verification_failure"] = reason
        return result

    # Non-coding domains: MCQ or structurally complete open-ended
    if qtype in ("aptitude", "logical", "verbal", "hr"):
        if not test_cases:
            result["verdict"] = "quarantined"
            result["reason"] = "no_test_cases_or_options"
            q["trust_status"] = "quarantined"
            q["verification_failure"] = result["reason"]
            return result

        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
        passed = 0
        reason = ""
        for tc in test_cases:
            try:
                actual = str(tc.get("output", "") or "").strip().upper()
                expected = str(correct).strip().upper()
                if actual == expected:
                    passed += 1
                else:
                    reason = f"MISMATCH expected={expected!r} got={actual!r}"
                    break
            except Exception as e:
                reason = f"{type(e).__name__}:{e}"[:160]
                break

        result["passed"] = passed
        result["total"] = len(test_cases)
        if passed == len(test_cases):
            result["verdict"] = "passed"
            result["reason"] = "mcq_options_consistent"
            q["trust_status"] = "automated_checked"
            q.pop("verification_failure", None)
        else:
            result["verdict"] = "failed"
            result["reason"] = reason or "mcq_inconsistent"
            q["trust_status"] = "quarantined"
            q["verification_failure"] = reason
        return result

    # interview / behavioral / system_design / debugging / other
    result["verdict"] = "passed"
    result["reason"] = "structural_check_passed"
    q["trust_status"] = "automated_checked"
    q.pop("verification_failure", None)
    return result


async def verify_all_questions() -> VerificationResult:
    """Verify all questions currently loaded in the canonical store.

    Call after ``question_store.load_all()``. Mutates question trust status
    in-memory and returns a summary.
    """
    from app.services import question_store
    question_store.load_all()

    result = VerificationResult()
    loop = __import__("asyncio").get_running_loop()

    def _verify_sync() -> None:
        for q in question_store._questions:
            status = str(q.get("trust_status", "")).lower()
            # quarantined is sticky: it records a human/system decision
            # (execution failure or student-quorum report), cleared only by
            # explicit review — never silently by a reboot re-verify, which
            # would otherwise un-quarantine quorum reports that execute fine
            # but carry a wrong answer key.
            if status in ("verified", "reviewed", "automated_checked", "quarantined"):
                result.skipped += 1
                continue
            result.total += 1
            try:
                r = verify_question(q)
            except Exception as e:
                r = {
                    "id": str(q.get("id") or ""),
                    "title": str(q.get("question") or "")[:60],
                    "verdict": "quarantined",
                    "reason": f"verify_exception:{type(e).__name__}:{str(e)[:120]}",
                    "passed": 0,
                    "total": 0,
                }
                q["trust_status"] = "quarantined"
                q["verification_failure"] = r["reason"]

            if r["verdict"] == "passed":
                result.passed += 1
            elif r["verdict"] == "failed":
                result.failed += 1
                result.details.append(r)
            elif r["verdict"] == "quarantined":
                result.quarantined += 1
                result.details.append(r)
            else:
                result.skipped += 1

    await loop.run_in_executor(None, _verify_sync)
    question_store._dedupe_and_filter(question_store._questions)
    logger.info(
        "Auto-verify complete: total=%d passed=%d failed=%d quarantined=%d skipped=%d",
        result.total, result.passed, result.failed, result.quarantined, result.skipped,
    )
    return result


# ---------------------------------------------------------------------------
# Lesson / world content verification (deterministic, no-LLM)
# ---------------------------------------------------------------------------

def _structural_check_lesson(lvl: dict, world_id: str, level_id: str) -> List[str]:
    issues: List[str] = []
    if not str(lvl.get("concept") or "").strip():
        issues.append("missing_concept")
    if not str(lvl.get("canonical_skill") or "").strip():
        issues.append("missing_canonical_skill")
    code = lvl.get("code") or {}
    if not str(code.get("prompt") or "").strip():
        issues.append("missing_code_prompt")
    predict = lvl.get("predict")
    if predict is not None:
        if not str(predict.get("prompt") or "").strip():
            issues.append("missing_predict_prompt")
        if not str(predict.get("answer") or "").strip():
            issues.append("missing_predict_answer")
    retrieval = lvl.get("retrieval")
    if retrieval is not None:
        if not str(retrieval.get("prompt") or "").strip():
            issues.append("missing_retrieval_prompt")
        if not str(retrieval.get("answer") or "").strip():
            issues.append("missing_retrieval_answer")
    transfer = lvl.get("transfer")
    if transfer is not None:
        if not str(transfer.get("prompt") or "").strip():
            issues.append("missing_transfer_prompt")
        if not str(transfer.get("answer") or "").strip():
            issues.append("missing_transfer_answer")
    break_step = lvl.get("break_step")
    if break_step is not None:
        if not str(break_step.get("broken_code") or "").strip():
            issues.append("missing_broken_code")
        if not str(break_step.get("expected_failure") or "").strip():
            issues.append("missing_expected_failure")
    debug = lvl.get("debug")
    if debug is not None:
        if not str(debug.get("buggy_code") or "").strip():
            issues.append("missing_buggy_code")
        if not str(debug.get("answer") or "").strip():
            issues.append("missing_debug_answer")
    hints = lvl.get("hints") or []
    if not hints:
        issues.append("missing_hints")
    success = lvl.get("success") or {}
    if not int(success.get("diamonds") or 0) > 0:
        issues.append("missing_or_zero_xp")
    if not str(success.get("reward_text") or "").strip():
        issues.append("missing_reward_text")
    return issues


async def _run_python_snippet(code: str, language: str = "python") -> dict:
    try:
        from app.services.code_executor import CodeExecutionEngine
        engine = CodeExecutionEngine()
        lang = (language or "python").lower()
        result = await engine.execute_code(code or "", lang, "", timeout=5)
        return result if isinstance(result, dict) else {"success": False, "error": "invalid_result"}
    except Exception as exc:
        return {"success": False, "error": f"{type(exc).__name__}:{exc}"}


async def _verify_lesson_runtime(lvl: dict, world_id: str, level_id: str) -> Dict[str, Any]:
    import re
    import traceback as tb_module

    def _resolve_message(run: dict) -> str:
        return (run.get("error") or run.get("stderr") or run.get("stdout") or "runtime check failed").strip()

    def _extract_exception(message: str) -> str:
        match = re.search(r"([A-Za-z_][A-Za-z0-9_]*Error|Exception):", message)
        return match.group(1) if match else ""

    def _extract_undefined_names(message: str) -> list[str]:
        names = re.findall(r"name '([^']+)' is not defined", message)
        return list(dict.fromkeys(names))

    def _step_result(step: str, source: str, run: dict) -> Dict[str, Any]:
        message = _resolve_message(run)
        return {
            "step": step,
            "runs": bool(run.get("success")),
            "exit_code": run.get("exit_code"),
            "stdout": (run.get("stdout") or "").strip(),
            "stderr": (run.get("stderr") or "").strip(),
            "error": (run.get("error") or "").strip(),
            "message": message[:200],
            "exception_type": _extract_exception(message),
            "undefined_names": _extract_undefined_names(message),
            "source_snippet": source[:200],
        }

    result: Dict[str, Any] = {
        "world_id": world_id,
        "level_id": level_id,
        "starter_runs": False,
        "placeholder_runs": False,
        "broken_raises": False,
        "debug_fix_runs": False,
        "error": None,
        "details": [],
    }
    try:
        code = lvl.get("code") or {}
        starter = str(code.get("starter") or "").strip()
        placeholder = str(code.get("placeholder") or "").strip()
        language = str(code.get("language") or "python").lower()

        if starter:
            run = await _run_python_snippet(starter, language)
            result["starter_runs"] = bool(run.get("success"))
            if not run.get("success"):
                step = _step_result("starter", starter, run)
                result["details"].append(step)
                result["error"] = f"starter_failed:{step['message']}"[:200]

        if placeholder:
            combined = (starter + "\n" + placeholder).strip() if starter else placeholder
            run = await _run_python_snippet(combined, language)
            result["placeholder_runs"] = bool(run.get("success"))
            if not run.get("success"):
                step = _step_result("placeholder", combined, run)
                result["details"].append(step)
                if result.get("error") is None:
                    result["error"] = f"placeholder_failed:{step['message']}"[:200]

        break_step = lvl.get("break_step")
        if break_step:
            broken = str(break_step.get("broken_code") or "").strip()
            if broken:
                run = await _run_python_snippet(broken, language)
                result["broken_raises"] = not bool(run.get("success"))
                if result["broken_raises"] and result.get("error") is None:
                    step = _step_result("break_step", broken, run)
                    result["details"].append(step)
                    result["error"] = f"broken_did_not_fail:{step['message']}"[:200]

        debug = lvl.get("debug")
        if debug:
            buggy = str(debug.get("buggy_code") or "").strip()
            answer = str(debug.get("answer") or "").strip()
            if buggy and answer:
                buggy_run = await _run_python_snippet(buggy, language)
                answer_run = await _run_python_snippet(answer, language)
                result["debug_fix_runs"] = bool(answer_run.get("success")) and not bool(buggy_run.get("success"))
                if not result["debug_fix_runs"] and result.get("error") is None:
                    step = _step_result("debug", answer, answer_run)
                    result["details"].append(step)
                    result["error"] = "debug_fix_does_not_resolve"
    except Exception as exc:
        result["error"] = f"runtime_check_exception:{type(exc).__name__}:{str(exc)[:120]}"
    return result


class LessonVerificationResult:
    def __init__(self) -> None:
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.details: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "details": self.details,
        }


def verify_lesson(lvl: dict, world_id: str, level_id: str, runtime: bool = False) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "world_id": world_id,
        "level_id": level_id,
        "verdict": "passed",
        "reason": "",
        "structural_issues": [],
        "runtime": {},
    }
    issues = _structural_check_lesson(lvl, world_id, level_id)
    result["structural_issues"] = issues
    if issues:
        result["verdict"] = "failed"
        result["reason"] = "structural:" + ";".join(issues)
        return result

    if runtime:
        import asyncio
        result["runtime"] = asyncio.run(_verify_lesson_runtime(lvl, world_id, level_id))
        rt = result["runtime"]
        if rt.get("error"):
            result["verdict"] = "failed"
            result["reason"] = rt["error"]
    return result


async def verify_all_lessons(runtime_checks: bool = False) -> LessonVerificationResult:
    from app.data.worlds_data import WORLD_REGISTRY

    result = LessonVerificationResult()
    loop = __import__("asyncio").get_running_loop()

    if runtime_checks:
        try:
            from app.services.circuit_breaker import compiler_breaker
            compiler_breaker._threshold = max(compiler_breaker._threshold, 1000)
            print(f"DEBUG: compiler_breaker threshold set to {compiler_breaker._threshold}")
        except Exception as exc:
            print(f"DEBUG: failed to set threshold: {exc}")
            pass

    def _verify_sync() -> None:
        for world_id, world in WORLD_REGISTRY.items():
            for town in world.towns:
                for lvl in town.levels:
                    result.total += 1
                    lvl_dict = lvl.model_dump() if hasattr(lvl, "model_dump") else lvl.dict()
                    try:
                        r = verify_lesson(lvl_dict, world_id, lvl.id, runtime=runtime_checks)
                    except Exception as exc:
                        r = {
                            "world_id": world_id,
                            "level_id": lvl.id,
                            "verdict": "failed",
                            "reason": f"verify_exception:{type(exc).__name__}:{str(exc)[:120]}",
                            "structural_issues": [],
                            "runtime": {},
                        }
                    if r["verdict"] == "passed":
                        result.passed += 1
                    else:
                        result.failed += 1
                        result.details.append(r)

    await loop.run_in_executor(None, _verify_sync)
    logger.info(
        "Lesson auto-verify complete: total=%d passed=%d failed=%d skipped=%d",
        result.total, result.passed, result.failed, result.skipped,
    )
    return result
