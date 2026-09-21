"""Deterministic bank autocheck (no LLM, no MongoDB).

Reads backend/app/data/questions_bank.json (UNVERIFIED pool), executes each
solution against its own stored test_cases in an isolated namespace with
stdout suppressed, and writes two offline artifacts:
- app/data/auto_checked_from_bank.json (AUTOMATED_CHECKED candidates only)
- app/data/bank_autocheck_report.json (counts + quarantine reasons)

Nothing is promoted to TRUSTED here. TRUSTED requires HUMAN_REVIEWED per
Content Trust Pipeline (AGENTS.md). Student serving (question_store.load_all)
does NOT load these artifacts.
"""
import ast
import contextlib
import inspect
import io
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BANK = BASE / "app" / "data" / "questions_bank.json"
OUT_CHECKED = BASE / "app" / "data" / "auto_checked_from_bank.json"
OUT_REPORT = BASE / "app" / "data" / "bank_autocheck_report.json"


def extract_funcs(src: str) -> str:
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


def parse_value(s):
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


def split_calls(raw: str):
    """Deterministic arg splitting (no guessing content):
    - multiline 'a\\nb' -> [parse(a), parse(b)] (LeetCode multi-arg form)
    - 'k=v, ...' kwarg form -> ({kwargs},) marker
    - else [parse(raw)]
    """
    s = str(raw)
    if "\n" in s:
        return [parse_value(part) for part in s.split("\n")]
    stripped = s.strip()
    if "=" in stripped:
        try:
            node = ast.parse(f"f({stripped})", mode="eval")
            call = node.body
            if isinstance(call, ast.Call) and call.keywords and not call.args:
                kwargs = {}
                for kw in call.keywords:
                    kwargs[kw.arg] = ast.literal_eval(kw.value)
                return [kwargs]
        except Exception:
            pass
    return [parse_value(s)]


def norm(x):
    if isinstance(x, float):
        return repr(round(x, 6))
    if isinstance(x, (list, tuple)):
        return "[" + ",".join(norm(v) for v in x) + "]"
    if isinstance(x, bool):
        return str(x)
    return str(x).strip()


def values_equal(actual, expected_raw: str) -> bool:
    exp = parse_value(expected_raw)
    # stdin-style wrappers return stdout as a STRING for list/dict
    # expectations. Parse-then-compare avoids whitespace mismatches.
    # Strictness-preserving: unparseable strings compare as strings.
    if isinstance(actual, str) and not isinstance(exp, str):
        parsed_actual = parse_value(actual)
        if not isinstance(parsed_actual, str):
            actual = parsed_actual
    if isinstance(actual, bool) or isinstance(exp, bool):
        return str(actual).lower() == str(exp).lower()
    if isinstance(actual, float) or isinstance(exp, float):
        try:
            return abs(float(actual) - float(exp)) < 1e-6
        except Exception:
            return norm(actual) == norm(exp)
    if isinstance(actual, (list, tuple)) and isinstance(exp, (list, tuple)):
        if len(actual) != len(exp):
            return False
        if all(isinstance(v, (list, tuple)) for v in list(actual) + list(exp)):
            key = lambda v: norm(v)
            return sorted((norm(v) for v in actual)) == sorted((norm(v) for v in exp))
        return norm(actual) == norm(exp)
    if isinstance(exp, str) and not isinstance(actual, str):
        return norm(actual) == exp.strip().strip("'\"")
    return norm(actual) == norm(exp)


def check_one(q: dict):
    sol = (q.get("solution") or {}).get("code", "")
    if not sol or "implement optimal" in sol.lower():
        return False, "NO_SOLUTION", 0, 0
    tcs = q.get("test_cases") or []
    if not tcs:
        return False, "NO_TESTS", 0, 0
    src = extract_funcs(sol)
    ns: dict = {}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(src, ns)
    except Exception as e:
        return False, f"EXEC_FAIL:{type(e).__name__}", 0, len(tcs)
    fn = None
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("def "):
            fn = s.split("(")[0].replace("def ", "").strip()
            break
    if not fn or fn not in ns:
        return False, "NO_FUNC", 0, len(tcs)
    f = ns[fn]
    try:
        arity = len([
            p for p in inspect.signature(f).parameters.values()
            if p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ])
    except Exception:
        arity = -1
    passed = 0
    reason = ""
    for tc in tcs:
        raw_input = tc.get("input", "")
        exp = str(tc.get("output", "")).strip()
        actual = None
        invoked = False
        chain_error = ""
        try:
            parts = split_calls(raw_input)
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
        matched = invoked and values_equal(actual, exp)
        if not matched and arity == 1 and isinstance(raw_input, str) and raw_input.strip():
            # fmt-style wrappers (arity 1) parse the RAW input string
            # themselves. One deterministic extra attempt, exact match
            # required on every test case — gate unchanged.
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    raw_actual = f(raw_input)
                matched = values_equal(raw_actual, exp)
            except Exception:
                matched = False
        if matched:
            passed += 1
        elif not reason:
            reason = chain_error or f"MISMATCH exp={exp!r} got={norm(actual)!r}"[:160]
    if passed == len(tcs):
        return True, "ALL_TESTS_PASS", passed, len(tcs)
    return False, reason or "MISMATCH", passed, len(tcs)


def to_canonical(q: dict, passed: int, total: int) -> dict:
    tcs = q.get("test_cases") or []
    visible = [{"input": t.get("input", ""), "expected": str(t.get("output", ""))}
               for t in tcs if not t.get("hidden")]
    hidden = [{"input": t.get("input", ""), "expected": str(t.get("output", ""))}
              for t in tcs if t.get("hidden")]
    sol = q.get("solution") or {}
    return {
        "id": f"autocheck-{q.get('id')}",
        "type": q.get("type", "coding"),
        "title": q.get("title", ""),
        "question": q.get("description") or q.get("title", ""),
        "statement": q.get("description") or q.get("title", ""),
        "difficulty": q.get("difficulty", "medium"),
        "topic": q.get("topic", "General"),
        "sub_topic": q.get("sub_topic", ""),
        "companies": q.get("companies") or [],
        "role": q.get("role", ""),
        "constraints": q.get("constraints", ""),
        "examples": [],
        "testcases": visible,
        "hidden_testcases": hidden,
        "solution": {"code": sol.get("code", ""), "language": sol.get("language", "python")},
        "hints": q.get("hints") or [],
        "explanation": q.get("explanation") or "",
        "trust_status": "automated_checked",
        "source_bank": "questions_bank.json",
        "provenance": "pattern-relevant; auto-executed, needs human review",
        "trust_report": {"engine": "autocheck_bank.py", "passed": passed, "total": total},
    }


def main():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    checked = []
    quarantine: dict = {}
    for q in bank:
        ok, reason, p, t = check_one(q)
        if ok:
            checked.append(to_canonical(q, p, t))
        else:
            key = reason.split(":")[0]
            quarantine[key] = quarantine.get(key, 0) + 1
    OUT_CHECKED.write_text(json.dumps(checked, indent=1), encoding="utf-8")
    report = {
        "total": len(bank),
        "automated_checked": len(checked),
        "quarantined": len(bank) - len(checked),
        "quarantine_reasons": quarantine,
        "note": ("AUTOMATED_CHECKED only. TRUSTED requires human review. "
                 "Not loaded by student serving."),
    }
    OUT_REPORT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"AUTOMATED_CHECKED {len(checked)}/{len(bank)}")
    print(f"QUARANTINED {len(bank) - len(checked)} {quarantine}")


if __name__ == "__main__":
    main()
