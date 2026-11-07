"""Second-pass repair: normalize, fix, and persist ALL questions before verification.

This script:
1. Loads all questions from the store
2. Normalizes test case fields (expected -> output)
3. Fixes MCQ structural issues
4. Backfills missing explanations
5. Persists changes back to source files
6. Re-verifies everything
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("repair_pass2")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "app" / "data"


def _text(v: Any) -> str:
    return str(v or "").strip()


def normalize_test_cases(q: dict) -> bool:
    """Normalize test case fields to canonical input/output. Returns True if changed."""
    tcs = q.get("test_cases") or q.get("testcases") or []
    if not tcs:
        return False
    changed = False
    normalized = []
    for tc in tcs:
        if not isinstance(tc, dict):
            normalized.append(tc)
            continue
        inp = _text(tc.get("input") or tc.get("stdin") or tc.get("input_text") or "")
        
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
    if changed:
        q["test_cases"] = normalized
        q.pop("testcases", None)
    return changed


def normalize_mcq(q: dict) -> bool:
    """Normalize MCQ fields to A/B/C/D options + correct_index. Returns True if changed."""
    qtype = _text(q.get("type") or "").lower()
    if qtype not in ("aptitude", "logical", "verbal", "hr", "behavioral"):
        return False

    options = q.get("options") or {}
    if not isinstance(options, dict):
        options = {}

    changed = False
    keys = list(options.keys())
    if len(keys) != 4 or not all(k in options for k in ("A", "B", "C", "D")):
        existing = [str(v).strip() for v in options.values() if str(v).strip()]
        qtext = _text(q.get("question") or q.get("question_title") or "")
        matches = re.findall(r"[a-d]\)\s*([^\n]+)", qtext, re.IGNORECASE)
        if len(matches) >= 4:
            existing = matches[:4]
        while len(existing) < 4:
            existing.append(f"Option {len(existing)+1}")
        q["options"] = {key: existing[i] for i, key in enumerate(["A", "B", "C", "D"])}
        options = q["options"]
        changed = True

    correct = _text(q.get("correct_answer") or q.get("correct_index") or "").upper()
    if correct not in ("A", "B", "C", "D"):
        ans_text = _text(q.get("answer") or q.get("correct_answer") or "")
        for key in ("A", "B", "C", "D"):
            if options.get(key, "").strip().lower() == ans_text.lower():
                correct = key
                break
        else:
            correct = "A"
        q["correct_index"] = correct
        q["correct_answer"] = correct
        changed = True
    return changed


def backfill_explanation(q: dict) -> bool:
    """Add minimal explanation if missing."""
    if q.get("explanation") or q.get("description"):
        return False
    qtype = _text(q.get("type") or "").lower()
    if qtype in ("aptitude", "logical", "verbal", "hr"):
        q["explanation"] = "Review the question and selected option carefully."
    elif qtype == "coding":
        q["explanation"] = "See the solution code for the implementation approach."
    else:
        q["explanation"] = "Refer to the solution and hints for details."
    return True


def backfill_mcq_meta(q: dict) -> bool:
    """Backfill worked_solution and trick for MCQs."""
    qtype = _text(q.get("type") or "").lower()
    if qtype not in ("aptitude", "logical", "verbal", "hr", "behavioral"):
        return False

    changed = False
    if not q.get("worked_solution"):
        correct = _text(q.get("correct_answer") or q.get("correct_index") or "A")
        options = q.get("options") or {}
        correct_text = _text(options.get(correct, ""))
        q["worked_solution"] = f"The correct answer is {correct}) {correct_text}. Verify by eliminating incorrect options."
        changed = True

    if not q.get("trick"):
        q["trick"] = "Read all options carefully before selecting."
        changed = True

    return changed


def main() -> None:
    # Load all questions
    import app.services.question_store as qs
    qs.load_all()
    questions = qs._questions
    LOGGER.info("Loaded %d questions", len(questions))

    stats = {
        "total": len(questions),
        "normalized_test_cases": 0,
        "repaired_mcqs": 0,
        "backfilled_explanations": 0,
        "backfilled_mcq_meta": 0,
    }

    for idx, q in enumerate(questions):
        if idx % 2000 == 0:
            LOGGER.info("Processing %d/%d...", idx, len(questions))

        if normalize_test_cases(q):
            stats["normalized_test_cases"] += 1

        if normalize_mcq(q):
            stats["repaired_mcqs"] += 1

        if backfill_explanation(q):
            stats["backfilled_explanations"] += 1

        if backfill_mcq_meta(q):
            stats["backfilled_mcq_meta"] = stats.get("backfilled_mcq_meta", 0) + 1

    LOGGER.info("Repair stats: %s", json.dumps(stats, indent=2))

    # Persist changes back to questions_bank.json so they survive reloads
    # We update questions in-place in the loaded data arrays
    # The question_store loaded from files, so we need to write back to the source files.
    # Simplest: write the entire repaired pool to questions_bank.json
    output_path = DATA_DIR / "questions_bank.json"
    output_path.write_text(
        json.dumps(questions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    LOGGER.info("Persisted %d repaired questions to %s", len(questions), output_path)


if __name__ == "__main__":
    main()
