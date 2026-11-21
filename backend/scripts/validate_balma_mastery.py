"""
Phase 6 — BALMA Mastery Validation.

Tests learner scenarios A–H:
A. Repeatedly solves one question 20x → one unique contribution, 20 attempts
B. Solves 20 different trusted questions → unique evidence increases
C. Attempts untrusted questions → cannot inflate trusted mastery
D. Solves difficult questions but unmet prerequisites → capped at Practicing
E. Solves previously encountered questions repeatedly → no false unseen-transfer credit
F. Solves genuinely unseen validated transfer questions → transfer evidence recorded separately
G. Repeatedly fails same question → remediation triggered
H. Retention after interval → retention evidence reflects delayed performance

Also verifies question IDs, duplicate detection, difficulty, trust, and skill mapping
are preserved throughout the evidence trail.
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

logging.disable(logging.CRITICAL)

from app.services.mastery_engine import (
    record_solve,
    build_mastery_graph,
    calculate_mastery_level,
    calculate_mastery_from_stats,
    MASTERY_LEVELS,
)

results: list[dict] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    results.append({"check": name, "passed": bool(condition), "detail": detail})
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" - {detail}" if detail else ""))


def scenario_A_repeated_same_question() -> None:
    """A. Learner repeatedly solves one question 20x → one unique contribution, 20 attempts."""
    print("\n--- Scenario A: Repeated same question ---")
    stats = None
    for i in range(20):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-same-001",
            question_type="coding",
            difficulty="medium",
            is_correct=True,
            trust_status="verified",
            existing_stats=stats,
        )
    check("One unique question (not 20)",
          stats["unique_questions_attempted"] == 1,
          f"got {stats['unique_questions_attempted']}")
    check("20 total attempts recorded",
          stats["total_attempts"] == 20,
          f"got {stats['total_attempts']}")
    check("Level 1 (Introduced) for 1 unique question",
          stats["current_level"] == 1,
          f"got {stats['current_level']} ({stats['current_level_name']})")
    check("Accuracy based on unique questions (100%)",
          stats["accuracy"] == 1.0,
          f"got {stats['accuracy']}")


def scenario_B_twenty_different_questions() -> None:
    """B. Learner solves 20 different trusted questions → unique evidence increases."""
    print("\n--- Scenario B: Twenty different questions ---")
    stats = None
    for i in range(20):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id=f"q-diff-{i:03d}",
            question_type="coding",
            difficulty="medium",
            is_correct=True,
            trust_status="verified",
            existing_stats=stats,
        )
    check("20 unique questions attempted",
          stats["unique_questions_attempted"] == 20,
          f"got {stats['unique_questions_attempted']}")
    check("20 unique questions solved",
          stats["unique_questions_solved"] == 20,
          f"got {stats['unique_questions_solved']}")
    check("Level 5 (Mastered) for 20 unique solved",
          stats["current_level"] == 5,
          f"got {stats['current_level']} ({stats['current_level_name']})")
    check("Accuracy 100%",
          stats["accuracy"] == 1.0,
          f"got {stats['accuracy']}")


def scenario_C_untrusted_questions() -> None:
    """C. Attempts untrusted questions → cannot inflate trusted mastery evidence."""
    print("\n--- Scenario C: Untrusted questions ---")
    # First, build some trusted mastery
    stats = None
    for i in range(5):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id=f"q-trusted-{i}",
            question_type="coding",
            difficulty="medium",
            is_correct=True,
            trust_status="verified",
            existing_stats=stats,
        )
    trusted_level = stats["current_level"]
    trusted_unique = stats["unique_questions_attempted"]

    # Now add untrusted questions
    for i in range(10):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id=f"q-untrusted-{i}",
            question_type="coding",
            difficulty="hard",
            is_correct=True,
            trust_status="unverified",
            existing_stats=stats,
        )

    check("Untrusted questions don't add unique evidence",
          stats["unique_questions_attempted"] == trusted_unique,
          f"got {stats['unique_questions_attempted']}, expected {trusted_unique}")
    check("Level unchanged by untrusted questions",
          stats["current_level"] == trusted_level,
          f"got {stats['current_level']}, expected {trusted_level}")
    check("Total attempts includes untrusted",
          stats["total_attempts"] == trusted_unique + 10,
          f"got {stats['total_attempts']}")


def scenario_D_unmet_prerequisites() -> None:
    """D. Solves difficult questions but unmet prerequisites → capped at Practicing."""
    print("\n--- Scenario D: Unmet prerequisites ---")
    stats = None
    # Solve 25 different questions at 100% accuracy (would normally be Mastered)
    for i in range(25):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id=f"q-prereq-{i}",
            question_type="coding",
            difficulty="hard",
            is_correct=True,
            trust_status="verified",
            existing_stats=stats,
            prerequisites_met=False,
        )
    check("Level capped at 2 (Practicing) when prerequisites unmet",
          stats["current_level"] <= 2,
          f"got {stats['current_level']} ({stats['current_level_name']})")
    check("Prerequisite gating flagged",
          stats.get("details", {}).get("prerequisite_gated") is True,
          "prerequisite_gated not True")


def scenario_E_no_false_transfer_credit() -> None:
    """E. Solves previously encountered questions repeatedly → no false unseen-transfer credit."""
    print("\n--- Scenario E: No false unseen-transfer credit ---")
    stats = None
    # First solve the question normally (not transfer)
    stats = record_solve(
        topic="arrays", sub_topic="two_sum",
        question_id="q-transfer-test",
        question_type="coding",
        difficulty="medium",
        is_correct=True,
        trust_status="verified",
        existing_stats=stats,
        is_transfer=False,
    )
    evidence_before = stats["weighted_evidence"]

    # Now solve the SAME question again marked as transfer — should NOT count double
    stats = record_solve(
        topic="arrays", sub_topic="two_sum",
        question_id="q-transfer-test",
        question_type="coding",
        difficulty="medium",
        is_correct=True,
        trust_status="verified",
        existing_stats=stats,
        is_transfer=True,
    )
    check("Repeated question doesn't add new unique evidence",
          stats["unique_questions_attempted"] == 1,
          f"got {stats['unique_questions_attempted']}")
    check("Weighted evidence doesn't double for repeat transfer",
          stats["weighted_evidence"] == evidence_before,
          f"got {stats['weighted_evidence']}, expected {evidence_before}")


def scenario_F_genuine_transfer_credit() -> None:
    """F. Solves genuinely unseen validated transfer questions → transfer evidence recorded separately."""
    print("\n--- Scenario F: Genuine transfer credit ---")
    stats = None
    # 9 unique normal questions (would be Competent/Strong boundary)
    for i in range(9):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id=f"q-normal-{i}",
            question_type="coding",
            difficulty="medium",
            is_correct=True,
            trust_status="verified",
            existing_stats=stats,
            is_transfer=False,
        )
    level_before = stats["current_level"]
    evidence_before = stats["weighted_evidence"]

    # 1 genuinely unseen transfer question (different ID)
    stats = record_solve(
        topic="arrays", sub_topic="two_sum",
        question_id="q-genuine-transfer-001",
        question_type="coding",
        difficulty="hard",
        is_correct=True,
        trust_status="verified",
        existing_stats=stats,
        is_transfer=True,
    )
    check("Transfer question adds unique evidence",
          stats["unique_questions_attempted"] == 10,
          f"got {stats['unique_questions_attempted']}")
    check("Transfer evidence counts double",
          stats["weighted_evidence"] > evidence_before + 1.5,
          f"got {stats['weighted_evidence']}, expected > {evidence_before + 1.5}")
    check("Transfer evidence trail records is_transfer=True",
          any(e["is_transfer"] for e in stats["evidence_trail"]),
          "transfer evidence found in trail")


def scenario_G_repeated_failures_remediation() -> None:
    """G. Repeatedly fails same question → remediation triggered."""
    print("\n--- Scenario G: Repeated failures -> remediation ---")
    stats = None
    # First failure — no remediation yet
    stats = record_solve(
        topic="arrays", sub_topic="two_sum",
        question_id="q-fail-repeat",
        question_type="coding",
        difficulty="medium",
        is_correct=False,
        trust_status="verified",
        existing_stats=stats,
    )
    check("First failure doesn't trigger remediation",
          stats["remediation_needed"] is False,
          f"got {stats['remediation_needed']}")

    # Second failure on same question — remediation triggered
    stats = record_solve(
        topic="arrays", sub_topic="two_sum",
        question_id="q-fail-repeat",
        question_type="coding",
        difficulty="medium",
        is_correct=False,
        trust_status="verified",
        existing_stats=stats,
    )
    check("Second failure on same question triggers remediation",
          stats["remediation_needed"] is True,
          f"got {stats['remediation_needed']}")


def scenario_H_retention_after_interval() -> None:
    """H. Retention after interval → retention evidence reflects delayed performance."""
    print("\n--- Scenario H: Retention after interval ---")
    stats = None
    # Initial learning phase
    for i in range(5):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id=f"q-retention-{i}",
            question_type="coding",
            difficulty="medium",
            is_correct=True,
            trust_status="verified",
            existing_stats=stats,
        )
    initial_level = stats["current_level"]

    # After interval, delayed assessment — new unseen questions
    for i in range(3):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id=f"q-retention-delayed-{i}",
            question_type="coding",
            difficulty="medium",
            is_correct=True,
            trust_status="verified",
            existing_stats=stats,
            is_transfer=True,  # Unseen transfer after interval
        )
    check("Delayed transfer questions add unique evidence",
          stats["unique_questions_attempted"] == 8,
          f"got {stats['unique_questions_attempted']}")
    check("Level maintained or improved after delay",
          stats["current_level"] >= initial_level,
          f"got {stats['current_level']}, was {initial_level}")


def scenario_I_evidence_trail_preserved() -> None:
    """Verify question IDs, duplicate detection, difficulty, trust, skill mapping preserved."""
    print("\n--- Scenario I: Evidence trail integrity ---")
    stats = None
    stats = record_solve(
        topic="arrays", sub_topic="two_sum",
        question_id="q-trail-001",
        question_type="coding",
        difficulty="hard",
        is_correct=True,
        trust_status="verified",
        existing_stats=stats,
    )
    trail = stats["evidence_trail"]
    check("Evidence trail has entry",
          len(trail) == 1,
          f"got {len(trail)}")
    entry = trail[0]
    check("Question ID preserved",
          entry["question_id"] == "q-trail-001")
    check("Question type preserved",
          entry["question_type"] == "coding")
    check("Difficulty preserved",
          entry["difficulty"] == "hard")
    check("Trust status preserved",
          entry["trust_status"] == "verified")
    check("Difficulty weight recorded",
          entry["difficulty_weight"] == 2.0,
          f"got {entry['difficulty_weight']}")


def main() -> None:
    print("=" * 70)
    print("PHASE 6 - BALMA MASTERY VALIDATION (Learner Scenarios A-I)")
    print("=" * 70)

    scenario_A_repeated_same_question()
    scenario_B_twenty_different_questions()
    scenario_C_untrusted_questions()
    scenario_D_unmet_prerequisites()
    scenario_E_no_false_transfer_credit()
    scenario_F_genuine_transfer_credit()
    scenario_G_repeated_failures_remediation()
    scenario_H_retention_after_interval()
    scenario_I_evidence_trail_preserved()

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
