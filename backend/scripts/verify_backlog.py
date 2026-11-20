"""Backlog verification triage (deterministic, no LLM, no network, no MongoDB).

Reuses autocheck_bank.check_one for executable coding items. Adds the gate
that did not exist for the main bank: MCQ / SQL structural + answer-key
integrity, which catches placeholder options ("Option 1..4") and answer keys
that do not resolve to a real option.

Emits two artefacts ONLY:
  app/data/backlog_verification_report.json   counts + reasons + sample ids
  app/data/backlog_verified_candidates.json   items passing every gate,
                                              stamped automated_checked

Nothing is promoted to verified/reviewed/trusted: that needs human review per
the Content Trust Pipeline (AGENTS.md). question_store._is_servable() refuses
automated_checked, so these candidates are not student-facing.
"""
from __future__ import annotations

import ast
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from scripts.autocheck_bank import check_one  # noqa: E402

BANK = BASE / "app" / "data" / "questions_bank.json"
OUT_REPORT = BASE / "app" / "data" / "backlog_verification_report.json"
OUT_CANDIDATES = BASE / "app" / "data" / "backlog_verified_candidates.json"

MCQ_TYPES = {"aptitude", "logical", "verbal", "cs_fundamentals", "cs"}
PLACEHOLDER_OPTION = re.compile(r"^option\s*[0-9a-d]{1,2}$", re.I)
BOILERPLATE_EXPLANATION = (
    "apply logical reasoning to determine the answer",
    "solve using the appropriate formula",
    "refer to the solution and hints for details",
    "use standard reasoning",
)


def _as_obj(value):
    """Options may be a list, a dict, or a repr string of either."""
    if isinstance(value, (list, dict)):
        return value
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = ast.literal_eval(value)
    except Exception:
        try:
            parsed = json.loads(value)
        except Exception:
            return None
    return parsed if isinstance(parsed, (list, dict)) else None


def _key_to_index(key, options):
    """Resolve correct_index/correct_answer key to a 0..n-1 position."""
    if isinstance(options, dict):
        keys = list(options.keys())
        if isinstance(key, int) and 0 <= key < len(keys):
            return key
        if isinstance(key, str):
            if key in options:
                return keys.index(key)
            if key.strip().isdigit():
                i = int(key)
                return i if 0 <= i < len(keys) else None
        return None
    if isinstance(key, int):
        return key if 0 <= key < len(options) else None
    if isinstance(key, str):
        s = key.strip()
        if s.isdigit():
            i = int(s)
            return i if 0 <= i < len(options) else None
        if len(s) == 1 and s.isalpha():
            i = ord(s.upper()) - ord("A")
            return i if 0 <= i < len(options) else None
    return None


def check_mcq(q: dict) -> tuple[bool, str]:
    """Structural + answer-key integrity for a non-executable MCQ item."""
    options = _as_obj(q.get("options"))
    if options is None:
        return False, "SCHEMA_BROKEN:options_unparseable"

    values = list(options.values()) if isinstance(options, dict) else list(options)
    if len(values) != 4:
        return False, f"SCHEMA_BROKEN:option_count_{len(values)}"

    cleaned = [str(v).strip() for v in values]
    if any(not v for v in cleaned):
        return False, "SCHEMA_BROKEN:empty_option"
    if len(set(cleaned)) != 4:
        return False, "SCHEMA_BROKEN:duplicate_options"
    if all(PLACEHOLDER_OPTION.match(v) for v in cleaned):
        return False, "PLACEHOLDER:all_options_placeholder"
    if sum(1 for v in cleaned if PLACEHOLDER_OPTION.match(v)) >= 2:
        return False, "PLACEHOLDER:majority_options_placeholder"

    key = q.get("correct_index")
    if key is None:
        key = q.get("correct_answer")
    idx = _key_to_index(key, options)
    if idx is None:
        return False, "SCHEMA_BROKEN:unresolvable_answer_key"

    # The answer key must land on a real option, and the stored answer text
    # (when it is text rather than a letter) must match that option.
    answer_text = q.get("correct_answer")
    if isinstance(answer_text, str) and answer_text.strip() and not (
        len(answer_text.strip()) == 1 and answer_text.strip().isalpha()
    ):
        chosen = cleaned[idx]
        if answer_text.strip().lower() not in chosen.lower():
            return False, "SCHEMA_BROKEN:answer_key_option_mismatch"

    # A generic explanation is a quality-repair item, NOT a correctness
    # failure: the question still has real, distinct options and a resolvable
    # answer key. Blocking on it would quarantine answerable questions
    # (e.g. cs-001 "Which data structure operates LIFO?" with real options),
    # which the Trust Rule does not ask for. Reported separately instead.
    explanation = str(q.get("explanation") or "").strip().lower()
    if explanation and any(b in explanation for b in BOILERPLATE_EXPLANATION):
        return True, "MCQ_STRUCTURE_OK:boilerplate_explanation"
    return True, "MCQ_STRUCTURE_OK"


def check_sql(q: dict) -> tuple[bool, str]:
    sol = q.get("solution")
    code = ""
    if isinstance(sol, dict):
        code = str(sol.get("code") or "")
    elif isinstance(sol, str):
        code = sol
    answer = str(q.get("correct_answer") or "")
    probe = (code or answer).strip()
    if not probe:
        return False, "CONTENT_MISSING:no_sql"
    if not re.search(r"\b(select|with|insert|update|delete|create)\b", probe, re.I):
        return False, "CONTENT_BROKEN:not_a_query"
    if re.search(r"\btodo\b|your query here", probe, re.I):
        return False, "PLACEHOLDER:query_stub"
    return True, "SQL_OK"


TEST_CASE_CONTAINERS = ("test_cases", "testcases", "visible_test_cases")


def normalize_test_cases(q: dict) -> list:
    """Return test cases in the shape autocheck_bank.check_one expects.

    Two schema drift problems exist in the served bank and both silently
    break execution checks:
      * the container may be `testcases` / `visible_test_cases`, not
        `test_cases` -> check_one reports a false NO_TESTS
      * the expected value may live under `expected`, not `output` ->
        check_one reads "" and reports a false MISMATCH
    Both are pure key renames; values are not altered. Where a case carries
    both keys they differ only by serialization (list vs its repr string),
    which values_equal already normalizes.
    """
    tcs = []
    for key in TEST_CASE_CONTAINERS:
        value = q.get(key)
        if isinstance(value, list) and value:
            tcs = value
            break
    normalized = []
    for tc in tcs:
        if not isinstance(tc, dict):
            normalized.append(tc)
            continue
        case = dict(tc)
        if case.get("output") in (None, "") and case.get("expected") is not None:
            case["output"] = case["expected"]
        normalized.append(case)
    return normalized


def _with_normalized_cases(q: dict) -> dict:
    """Shallow copy carrying test cases under the keys check_one reads."""
    staged = dict(q)
    staged["test_cases"] = normalize_test_cases(q)
    return staged


def classify(q: dict) -> tuple[str, str]:
    """Return (verdict, reason). verdict in PASS | FAIL | SKIP."""
    qtype = str(q.get("type") or "").strip().lower()
    if qtype == "coding":
        ok, reason, passed, total = check_one(_with_normalized_cases(q))
        if ok:
            return "PASS", f"EXEC_OK:{passed}/{total}"
        head = reason.split(":")[0]
        if head == "STDIN_STYLE":
            # No argument-accepting callable: harness limit, not a defect.
            return "SKIP", "STDIN_STYLE_UNSUPPORTED"
        return "FAIL", head
    if qtype == "sql":
        ok, reason = check_sql(q)
        return ("PASS" if ok else "FAIL"), reason
    if qtype in MCQ_TYPES:
        ok, reason = check_mcq(q)
        return ("PASS" if ok else "FAIL"), reason
    if qtype in ("interview", "system_design", "debugging"):
        # Prose-answer types have no executable oracle.
        return "SKIP", "NO_ORACLE"
    return "SKIP", f"UNHANDLED_TYPE:{qtype or 'none'}"


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    started = time.time()

    verdicts = Counter()
    by_type: dict[str, Counter] = defaultdict(Counter)
    reasons: Counter = Counter()
    samples: dict[str, list] = defaultdict(list)
    candidates = []

    for q in bank:
        verdict, reason = classify(q)
        qtype = str(q.get("type") or "none").lower()
        verdicts[verdict] += 1
        by_type[qtype][verdict] += 1
        if verdict != "PASS":
            reasons[reason] += 1
            bucket = reason.split(":")[0]
            if len(samples[bucket]) < 5:
                samples[bucket].append(
                    {"id": q.get("id"), "type": qtype, "reason": reason,
                     "question": str(q.get("question") or q.get("title"))[:110]}
                )
        else:
            staged = dict(q)
            staged["trust_status"] = "automated_checked"
            staged["verification"] = {"engine": "verify_backlog.py",
                                      "result": reason,
                                      "promoted_to": "automated_checked"}
            candidates.append(staged)

    elapsed = time.time() - started
    total = len(bank)

    report = {
        "generated_by": "scripts/verify_backlog.py",
        "engine": "deterministic exec + schema gate (no LLM, no network)",
        "bank": BANK.name,
        "total": total,
        "verdicts": dict(verdicts),
        "pass_rate": round(verdicts["PASS"] / total * 100, 2) if total else 0.0,
        "elapsed_seconds": round(elapsed, 2),
        "by_type": {t: dict(c) for t, c in sorted(by_type.items())},
        "reasons": dict(reasons.most_common()),
        "sample_failures": dict(samples),
        "trust_policy": {
            "written_trust_status": "automated_checked",
            "servable": False,
            "note": ("automated_checked is refused by question_store._is_servable(); "
                     "promotion to verified/reviewed requires human review."),
        },
    }
    OUT_REPORT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    OUT_CANDIDATES.write_text(json.dumps(candidates, indent=1), encoding="utf-8")

    print(f"BANK {total}  PASS {verdicts['PASS']}  FAIL {verdicts['FAIL']}  SKIP {verdicts['SKIP']}  ({elapsed:.1f}s)")
    print(f"pass rate {report['pass_rate']}%\n")
    print("by type:")
    for t, c in sorted(by_type.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(c.values())
        print(f"  {t:17s} total={n:6d} pass={c['PASS']:6d} fail={c['FAIL']:6d} skip={c['SKIP']:5d}")
    print("\ntop reasons:")
    for r, n in reasons.most_common(12):
        print(f"  {r:42s} {n:6d}")
    print(f"\nwrote {OUT_REPORT.name} ({len(candidates)} candidates in {OUT_CANDIDATES.name})")


if __name__ == "__main__":
    main()
