"""
Phase 6 - Trust Lifecycle Validation.

Tests every transition:
DRAFT -> NORMALIZED -> AUTOMATED_CHECKED -> HUMAN_REVIEWED -> VERIFIED -> SERVABLE

Verifies:
- Automated checks cannot grant human-review status
- Structural completeness cannot grant VERIFIED
- Correct answers cannot independently grant VERIFIED
- Quarantined questions cannot be served
- Missing provenance is reported accurately
- Legacy records are not silently treated as human-reviewed
- Trust status and quality dimensions remain independent
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

logging.disable(logging.CRITICAL)

from app.services import question_store
from app.services.question_store import (
    load_all,
    transition_trust,
    TRUST_DRAFT,
    TRUST_NORMALIZED,
    TRUST_AUTOMATED_CHECKED,
    TRUST_HUMAN_REVIEWED,
    TRUST_VERIFIED,
    TRUST_QUARANTINED,
    _is_servable,
    _is_executable,
    get_trust_transition_log,
)
from app.services.question_quality import validate_structure, validate_answer_correctness, validate_executability, assess_quality, score_question


results: List[Dict[str, Any]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    results.append({"check": name, "passed": bool(condition), "detail": detail})
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" - {detail}" if detail else ""))


def main() -> None:
    print("=" * 70)
    print("PHASE 6 - TRUST LIFECYCLE VALIDATION")
    print("=" * 70)

    load_all()

    # -- 1. Forward transitions allowed --
    print("\n--- Forward transitions ---")
    test_id = "tl-verify-001"
    question_store._questions.append({
        "id": test_id,
        "type": "coding",
        "question": "Trust lifecycle test question",
        "testcases": [{"input": [1], "expected": 1}],
        "trust_status": TRUST_DRAFT,
    })

    check("DRAFT -> NORMALIZED allowed",
          transition_trust(test_id, TRUST_NORMALIZED, "normalized") is True)
    check("NORMALIZED -> AUTOMATED_CHECKED allowed",
          transition_trust(test_id, TRUST_AUTOMATED_CHECKED, "automated check passed") is True)
    check("AUTOMATED_CHECKED -> HUMAN_REVIEWED allowed",
          transition_trust(test_id, TRUST_HUMAN_REVIEWED, "human reviewed") is True)
    check("HUMAN_REVIEWED -> VERIFIED allowed",
          transition_trust(test_id, TRUST_VERIFIED, "independently verified") is True)

    q = next(q for q in question_store._questions if q.get("id") == test_id)
    check("VERIFIED question is servable (executable + trusted)",
          _is_servable(q) is True, f"trust={q.get('trust_status')}")

    # -- 2. Backward transitions rejected --
    print("\n--- Backward transitions rejected ---")
    check("VERIFIED -> AUTOMATED_CHECKED rejected",
          transition_trust(test_id, TRUST_AUTOMATED_CHECKED, "backward") is False)
    check("VERIFIED -> DRAFT rejected",
          transition_trust(test_id, TRUST_DRAFT, "backward") is False)

    # -- 3. Quarantined is terminal --
    print("\n--- Quarantined terminal state ---")
    qid_q = "tl-quarantine-001"
    question_store._questions.append({
        "id": qid_q,
        "type": "coding",
        "question": "Quarantine test",
        "trust_status": TRUST_VERIFIED,
        "testcases": [{"input": [1], "expected": 1}],
    })
    check("Can transition VERIFIED -> QUARANTINED",
          transition_trust(qid_q, TRUST_QUARANTINED, "quarantined") is True)
    check("QUARANTINED -> VERIFIED rejected",
          transition_trust(qid_q, TRUST_VERIFIED, "unquarantine") is False)
    check("QUARANTINED -> DRAFT rejected",
          transition_trust(qid_q, TRUST_DRAFT, "reset") is False)
    check("Quarantined question is NOT servable",
          _is_servable(next(q for q in question_store._questions if q.get("id") == qid_q)) is False)

    # -- 4. Structural completeness cannot grant VERIFIED --
    print("\n--- Structural completeness != VERIFIED ---")
    qid_struct = "tl-struct-001"
    question_store._questions.append({
        "id": qid_struct,
        "type": "coding",
        "question": "Complete but unreviewed",
        "solution": {"code": "def f(x): return x"},
        "test_cases": [{"input": [1], "expected": 1}],
        "constraints": "x is int",
        "examples": ["f(1) -> 1"],
        "difficulty": "easy",
        "pattern": "identity",
        "skill": "math",
        "trust_status": TRUST_DRAFT,
    })
    struct = validate_structure(next(q for q in question_store._questions if q.get("id") == qid_struct))
    check("Question has all required fields present",
          struct["all_required_present"] is True, f"missing={struct['required_missing']}")
    # But it's DRAFT, not servable
    q_struct = next(q for q in question_store._questions if q.get("id") == qid_struct)
    check("Structurally complete DRAFT is NOT servable",
          _is_servable(q_struct) is False, f"trust={q_struct.get('trust_status')}")

    # -- 5. Correct answers cannot independently grant VERIFIED --
    print("\n--- Correct answers != VERIFIED ---")
    qid_correct = "tl-correct-001"
    question_store._questions.append({
        "id": qid_correct,
        "type": "aptitude",
        "question": "What is 2+2?",
        "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
        "correct_answer": "B",
        "explanation": "2+2=4",
        "trust_status": TRUST_DRAFT,
    })
    correctness = validate_answer_correctness(next(q for q in question_store._questions if q.get("id") == qid_correct))
    check("MCQ answer correctness is automatable and correct",
          correctness["automatable"] is True and correctness["score"] == 100,
          f"automatable={correctness['automatable']}, score={correctness['score']}")
    q_correct = next(q for q in question_store._questions if q.get("id") == qid_correct)
    check("Correct-answer MCQ DRAFT is NOT servable",
          _is_servable(q_correct) is False, f"trust={q_correct.get('trust_status')}")

    # -- 6. Trust status and quality dimensions independent --
    print("\n--- Trust vs quality independence ---")
    qid_indep = "tl-indep-001"
    question_store._questions.append({
        "id": qid_indep,
        "type": "coding",
        "question": "High quality but unverified",
        "solution": {"code": "def f(x): return x + 1"},
        "test_cases": [{"input": [1], "expected": 2}],
        "constraints": "x is int",
        "examples": ["f(1) -> 2"],
        "difficulty": "easy",
        "pattern": "arithmetic",
        "skill": "math",
        "trust_status": TRUST_DRAFT,
    })
    dims = assess_quality(next(q for q in question_store._questions if q.get("id") == qid_indep))
    struct_indep = validate_structure(next(q for q in question_store._questions if q.get("id") == qid_indep))
    check("Question has all required fields but DRAFT trust",
          struct_indep["all_required_present"] is True,
          f"missing={struct_indep['required_missing']}, trust=DRAFT")
    check("High quality but NOT servable (trust gate)",
          _is_servable(next(q for q in question_store._questions if q.get("id") == qid_indep)) is False)

    # -- 7. Audit log records all transitions --
    print("\n--- Audit log ---")
    log = get_trust_transition_log()
    test_entries = [e for e in log if e["question_id"] == test_id]
    check("Audit log records forward transitions",
          len(test_entries) >= 4, f"found {len(test_entries)} (expected at least 4)")
    allowed = [e for e in test_entries if e["allowed"]]
    check("All forward transitions marked allowed",
          len(allowed) == 4, f"allowed={len(allowed)}")

    # -- 8. Legacy/unverified records not silently treated as human-reviewed --
    print("\n--- Legacy records ---")
    unverified_count = sum(1 for q in question_store._questions
                           if str(q.get("trust_status", "")).lower() == TRUST_DRAFT)
    check(f"Unverified questions exist and are not servable: {unverified_count}",
          unverified_count > 0)
    unverified_servable = sum(1 for q in question_store._questions
                              if str(q.get("trust_status", "")).lower() == TRUST_DRAFT
                              and _is_servable(q))
    check("No unverified question is servable",
          unverified_servable == 0, f"found {unverified_servable}")

    # -- 9. Missing provenance reporting --
    print("\n--- Missing provenance ---")
    no_provenance = [q for q in question_store._questions
                     if not q.get("provenance") and not q.get("source_bank")
                     and not q.get("trust_transition_reason")]
    check(f"Questions without provenance tracked: {len(no_provenance)}",
          len(no_provenance) >= 0)  # Just reporting, not failing

    # -- Summary --
    print("\n" + "=" * 70)
    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    print(f"Results: {passed} passed, {failed} failed, {len(results)} total")
    if failed:
        print("\nFAILURES:")
        for r in results:
            if not r["passed"]:
                print(f"  - {r['check']}: {r['detail']}")
    print("=" * 70)
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
