"""Question Content Governance — canonical ownership & trust contract.

This module is the single written source of truth for *which runtime system
owns which question model and which on-disk banks feed it*. It does NOT load,
serve, or transform any question. It exists so that the two purpose-specific
runtime readers (question_store and quiz_service) do not silently diverge into
conflicting sources of truth, and so that every on-disk bank has one clear owner.

ARCHITECTURE DECISION (Content Excellence Phase)
-----------------------------------------------
BountyCode maintains TWO purpose-specific runtime readers on purpose:

1. question_store  (app.services.question_store)
      Owner  : placement / coding question bank (DSA, LeetCode-style, Striver,
                difficulty+testcase+constraints model).
      Banks  : verified-only runtime pool from:
                app/data/verified_placement_questions.json (TRUSTED)
                app/data/sql_practice_bank.json (TRUSTED)
                app/data/interview_practice_bank.json (TRUSTED)
                app/data/india_placement_depth.json (TRUSTED)
      Consumers: browse, solve, daily problem, company prep, OA.
      High-stakes OA / readiness / company assessments MUST consume this pool
      (verified content only).
      Unverified/dirty banks are isolated and only loaded on explicit admin
      request via question_store.load_unverified() / find_unverified().

2. quiz_service   (app.services.quiz_service)
      Owner  : curated interactive-quiz model (MCQ, learning objects, practice
                modes, boss battle, mock-interview-with-timer).
      Banks  : app/content/questions/curated/curated.json,
                app/content/questions/curated/learning_objects.json,
                app/content/questions/curated/placement_questions.json.
      Consumers: quiz, practice, mock interview, boss battle, speed run, code golf.

Do NOT rewrite quiz_service to use question_store.
Do NOT create a third question system.
These models and responsibilities differ on purpose:
     question_store == the rigorous, test-cased coding/placement bank.
     quiz_service  == the curated, interactive learning-object model.

The shared quality standard that BOTH must respect lives in
app.services.question_standard (Placement Question Standard: fields, tiers,
role mapping). Treat question_standard as the non-negotiable quality gate.
"""

from __future__ import annotations

from typing import Dict, List

# ---------------------------------------------------------------------------
# Trust pipeline (Content Trust). Every bank maps to one of these states.
#   UNVERIFIED       -> raw imported content, never served to students.
#   AUTOMATED_CHECKED-> passes automated validation (solution executes, tests
#                        pass, no ambiguity flags).
#   HUMAN_REVIEWED   -> human verified correctness, relevance, quality.
#   TRUSTED          -> fully verified; safe as placement-quality.
# ---------------------------------------------------------------------------
TRUST_STATES = ("UNVERIFIED", "AUTOMATED_CHECKED", "HUMAN_REVIEWED", "TRUSTED")

# Publishing order is trust-gated: only TRUSTED/AUTOMATED_CHECKED content may
# enter high-stakes OA, readiness, and company assessments. quiz_service's
# curated set is interactively authored; question_store carries the verified
# runtime pool. Neither bypasses question_standard for paid/premium content.


# ---------------------------------------------------------------------------
# Ownership registry: every immutable runtime question bank file -> owner.
# This is the drift-prevention contract. Add new banks here, NOT in route files.
# ---------------------------------------------------------------------------
BANK_OWNERSHIP: List[Dict[str, str]] = [
    # Verified-only runtime banks (loaded by default into question_store).
    {"bank": "app/data/tranche_promoted.json",              "owner": "question_store", "trust": "TRUSTED"},
    {"bank": "app/data/verified_placement_questions.json",  "owner": "question_store", "trust": "TRUSTED"},
    {"bank": "app/data/sql_practice_bank.json",             "owner": "question_store", "trust": "TRUSTED"},
    {"bank": "app/data/interview_practice_bank.json",       "owner": "question_store", "trust": "TRUSTED"},
    {"bank": "app/data/india_placement_depth.json",         "owner": "question_store", "trust": "TRUSTED"},
    # Isolated unverified banks (not loaded by default; admin/candidate mode only).
    {"bank": "app/data/questions_bank.json",                "owner": "question_store", "trust": "UNVERIFIED"},
    {"bank": "app/data/leetcode_problems_seed.json",        "owner": "question_store", "trust": "UNVERIFIED"},
    {"bank": "app/data/striver_a2z_600.json",               "owner": "question_store", "trust": "UNVERIFIED"},
    {"bank": "app/data/tcs_nqt_questions.json",             "owner": "question_store", "trust": "UNVERIFIED"},
    {"bank": "app/data/infosys_questions.json",             "owner": "question_store", "trust": "UNVERIFIED"},
    {"bank": "app/data/legacy_enriched_coding.json",        "owner": "question_store", "trust": "UNVERIFIED"},
    # quiz_service owns the curated interactive-quiz universe.
    {"bank": "app/content/questions/curated/curated.json",                "owner": "quiz_service", "trust": "HUMAN_REVIEWED"},
    {"bank": "app/content/questions/curated/learning_objects.json",       "owner": "quiz_service", "trust": "HUMAN_REVIEWED"},
    {"bank": "app/content/questions/curated/placement_questions.json",    "owner": "quiz_service", "trust": "HUMAN_REVIEWED"},
]

# Offline production-pipeline artifacts (NOT runtime-served by default; trusted via the
# content_factory -> independent_verify -> repair_queue -> promote_pass flow).
# Isolated unverified banks are also listed here since they are no longer in the
# default serving pool.
OFFLINE_PIPELINE_ARTIFACTS: List[str] = [
    "app/content/questions/raw/questions_bank.json",
    "app/content/questions/rejected/rejected.json",
    "app/content/questions/review_duplicates/review_duplicates.json",
    "app/data/questions_bank_curated.json",
    "app/data/questions_trusted.json",
    "app/data/repair_queue.json",
    "app/data/trusted_packs.json",
    "app/data/leetcode_problems_seed.json",
    "app/data/striver_a2z_600.json",
    "app/data/tcs_nqt_questions.json",
    "app/data/infosys_questions.json",
    "app/data/legacy_enriched_coding.json",
    "app/data/auto_checked_from_bank.json",
    "app/data/bank_autocheck_report.json",
    "app/data/served_quarantine.json",
    "app/data/parametric_practice_bank.json",
    "app/data/parametric_bank_report.json",
    "app/data/parametric_verify_report.json",
    "app/data/sampling_report.json",
    "app/data/fix_log.json",
    "app/data/rejected.json",
    "app/data/tranche_log.json",
    "app/data/auto_promote_report.json",
    "app/data/question_reports.json",
    "app/data/needs_enrichment.json",
]


def owner_of(bank: str) -> str | None:
    """Return the owning runtime system for a bank path, or None if unknown."""
    for row in BANK_OWNERSHIP:
        if row["bank"] == bank:
            return row["owner"]
    return None


def trust_of(bank: str) -> str | None:
    """Return the declared trust state for a bank path, or None if unknown."""
    for row in BANK_OWNERSHIP:
        if row["bank"] == bank:
            return row["trust"]
    return None


def is_runtime_bank(bank: str) -> bool:
    """True if the bank is an immutable file served by a runtime reader."""
    return owner_of(bank) is not None


def get_banks_for(owner: str) -> List[str]:
    """Return the bank paths owned by a runtime system."""
    return [row["bank"] for row in BANK_OWNERSHIP if row["owner"] == owner]
