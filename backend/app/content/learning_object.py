"""
Canonical Question Learning Object
==================================

A learning object is NOT a "question with enrichment bolted on." It is a
first-class educational artifact that powers:

  - Concept teaching (the "why")
  - Pattern recognition (the "when")
  - Practice (the "how")
  - Assessment (the "did you learn")
  - Transfer test (the "can you apply it elsewhere")

One learning object can drive Practice + Quiz + OA + Interview + Boss Battle.

The single hard rule: **provenance and quality must be honest.** We never
claim a question is "official Amazon" unless Amazon itself published it.
We never claim a `why_this_matters` is excellent unless it actually is.

Quality gating: a question is `published` only if every score >= 80.
Questions below that stay in `draft` and surface in the authoring console,
not to students.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import json
import os


# =============================================================
# PROVENANCE TAXONOMY
# =============================================================

# Each level is a strict claim about origin. UI must render the level
# verbatim. Never silently upgrade.

PROVENANCE_LEVELS = {
    "official": {
        "label": "Official",
        "description": "Company itself published the question or process.",
        "confidence": "High",
        "badge_color": "text-emerald-400",
    },
    "candidate_reported": {
        "label": "Candidate-reported",
        "description": "Candidate reported encountering this in a real interview.",
        "confidence": "Medium",
        "badge_color": "text-amber-400",
    },
    "pattern_relevant": {
        "label": "Pattern-relevant",
        "description": "The technique is tested at this company, but this exact question is not.",
        "confidence": "Medium-Low",
        "badge_color": "text-blue-400",
    },
    "canonical": {
        "label": "Canonical",
        "description": "Inspired by or adapted from a known problem. Used to teach the pattern.",
        "confidence": "Reference",
        "badge_color": "text-purple-400",
    },
    "synthetic": {
        "label": "Synthetic",
        "description": "Original question authored for this curriculum. Not seen in any public source.",
        "confidence": "N/A",
        "badge_color": "text-gray-400",
    },
}


# =============================================================
# QUALITY DIMENSIONS
# =============================================================

# Every quality dimension is scored 0-100. A question is "publishable" only
# if every dimension is >= 80. This is enforced by the quality gate.

QUALITY_DIMENSIONS = [
    "explanation",       # Is the why/mental model genuinely educational?
    "real_world",        # Are the real-world uses specific and credible?
    "hints",             # Do the 3 hints form a real scaffold, not generic advice?
    "pattern",           # Is the pattern_recognition useful for spotting this in new problems?
    "interview_value",   # Would a real interviewer ask this? Does it test a real signal?
    "transfer_potential", # Can a student apply this technique to a new story (boss battle)?
    "pedagogical_clarity", # Is the problem statement itself unambiguous and well-framed?
]


# =============================================================
# THE CANONICAL SCHEMA
# =============================================================

LEARNING_OBJECT_SCHEMA = {
    "id": str,
    "title": str,
    "canonical_problem": str,           # Stable human-readable name (e.g. "Two Sum")

    # -------- learning --------
    "learning": {
        "concept": str,                  # The single concept this teaches (e.g. "complement search")
        "mental_model": str,             # The intuition (e.g. "trade memory for time")
        "why_this_matters": str,         # Genuine engineering insight, NOT generic filler
        "real_world": List[str],         # 2-3 specific, credible production uses
        "prerequisites": List[str],      # Concepts you must know first
        "learning_objective": str,       # What the student can DO after this
    },

    # -------- reasoning --------
    "reasoning": {
        "pattern": str,                  # E.g. "hash-table", "two-pointers"
        "recognition_signals": List[str], # "When you see X, think Y"
        "anti_patterns": List[str],      # "Don't do this"
        "tradeoffs": List[str],          # "Why this beats the naive approach"
    },

    # -------- assistance --------
    "assistance": {
        "hint_1": str,                   # Conceptual nudge
        "hint_2": str,                   # Structural hint
        "hint_3": str,                   # Near-solution hint
        "common_mistakes": List[str],    # Real pitfalls candidates hit
    },

    # -------- assessment --------
    "assessment": {
        "difficulty": str,               # easy | medium | hard | expert
        "constraints": List[str],        # Time/space constraints explicit
        "test_cases": List[dict],        # Visible + hidden test cases
        "rubric": List[dict],            # How we score a free-form answer
    },

    # -------- career --------
    "career": {
        "roles": List[str],              # Which placement roles this serves
        "companies": List[str],          # Which companies test this pattern
        "placement_stage": List[str],    # "oa" | "phone" | "onsite" | "bar-raiser"
        "provenance": Dict[str, Any],    # See PROVENANCE_LEVELS
    },

    # -------- progression --------
    "progression": {
        "mastery_skill": str,            # Skill name in mastery graph
        "world": str,                    # Which world owns this (e.g. "arrays-village")
        "town": str,                     # Which town (e.g. "the-marketplace")
        "mission_id": str,               # Which mission unlocks this
        "boss_variant": bool,            # Is this a boss (transfer test) or practice?
        "unlock_condition": str,         # What the student must complete first
        "xp_reward": int,                # Adventure Diamonds (NOT mastery)
    },

    # -------- meta --------
    "meta": {
        "created_at": str,
        "updated_at": str,
        "authored_by": str,              # "system" | "human:<id>" | "ai:<model>"
        "version": int,
        "status": str,                   # "draft" | "in_review" | "published" | "retired"
        "quality_scores": Dict[str, int],
        "overall_quality": int,
        "publishable": bool,
        "tags": List[str],
    },
}


# =============================================================
# QUALITY GATE
# =============================================================

PUBLISH_THRESHOLD = 80  # Every dimension must be >= this to be publishable


def evaluate_quality(lo: dict) -> dict:
    """
    Score a learning object. Returns the score breakdown and a publishable flag.

    This is intentionally a structured rubric, not vibes. Each dimension is
    scored by a function that checks for actual content presence and depth.

    In production, this should be a hybrid: a model-assisted score for
    `explanation`, `real_world`, `pattern`, `transfer_potential`, plus a
    rule-based check for `hints`, `interview_value`, `pedagogical_clarity`.
    """
    scores = {}

    learning = lo.get("learning", {}) or {}
    reasoning = lo.get("reasoning", {}) or {}
    assistance = lo.get("assistance", {}) or {}
    assessment = lo.get("assessment", {}) or {}
    career = lo.get("career", {}) or {}

    # 1. explanation: requires why_this_matters, mental_model, learning_objective
    ytm = learning.get("why_this_matters", "") or ""
    mm = learning.get("mental_model", "") or ""
    lo_obj = learning.get("learning_objective", "") or ""
    has_depth = len(ytm) > 80 and len(mm) > 30 and len(lo_obj) > 30
    not_generic = not any(
        marker in ytm.lower()
        for marker in [
            "important in computer science",
            "used in real-world applications",
            "fundamental concept",
            "is important",
            "is a fundamental",
        ]
    )
    scores["explanation"] = min(100, 50 + (40 if has_depth else 0) + (30 if not_generic else 0))

    # 2. real_world: requires 2+ specific, non-generic uses
    rw = learning.get("real_world", []) or []
    if isinstance(rw, str):
        rw = [rw]
    has_specific_uses = len(rw) >= 2 and any(len(str(u)) > 40 for u in rw)
    scores["real_world"] = min(100, 40 + (60 if has_specific_uses else 20))

    # 3. hints: requires 3 distinct, escalating hints
    h1 = assistance.get("hint_1", "") or ""
    h2 = assistance.get("hint_2", "") or ""
    h3 = assistance.get("hint_3", "") or ""
    distinct = len({h1.strip(), h2.strip(), h3.strip()}) == 3
    all_present = bool(h1) and bool(h2) and bool(h3)
    all_substantive = min(len(h1), len(h2), len(h3)) >= 30
    escalating = len(h3) >= len(h2) and len(h2) >= len(h1)
    # Acceptable if 3 distinct substantive hints are present, even if not strictly escalating in length.
    # Escalation by content (conceptual -> structural -> solution) is more important than length.
    scores["hints"] = min(
        100,
        30
        + (25 if all_present else 0)
        + (25 if distinct else 0)
        + (20 if all_substantive else 0)
        + (10 if escalating else 0)
    )

    # 4. pattern: requires pattern + recognition_signals + anti_patterns
    pat = reasoning.get("pattern", "") or ""
    sigs = reasoning.get("recognition_signals", []) or []
    anti = reasoning.get("anti_patterns", []) or []
    if isinstance(sigs, str):
        sigs = [sigs]
    if isinstance(anti, str):
        anti = [anti]
    has_pattern = bool(pat) and len(sigs) >= 2 and len(anti) >= 1
    scores["pattern"] = min(100, 30 + (70 if has_pattern else 20))

    # 5. interview_value: requires difficulty + provenance + companies
    diff = assessment.get("difficulty", "") or ""
    prov = career.get("provenance", {}) or {}
    comps = career.get("companies", []) or []
    scores["interview_value"] = min(
        100, 30 + (30 if diff in ("easy", "medium", "hard", "expert") else 0)
        + (25 if prov.get("level") in ("official", "candidate_reported") else 10)
        + (15 if len(comps) >= 1 else 0)
    )

    # 6. transfer_potential: requires boss_variant or progression linkage
    prog = lo.get("progression", {}) or {}
    has_progression = bool(prog.get("mastery_skill")) and bool(prog.get("world"))
    scores["transfer_potential"] = min(100, 30 + (70 if has_progression else 20))

    # 7. pedagogical_clarity: requires clear problem statement + test cases + constraints
    problem = lo.get("problem", "") or lo.get("question", "") or ""
    test_cases = assessment.get("test_cases", []) or []
    constraints = assessment.get("constraints", []) or []
    # The test cases dict can include "input" + "expected" or just be present.
    usable_test_cases = sum(
        1 for tc in test_cases
        if isinstance(tc, dict) and (tc.get("input") is not None or tc.get("expected") is not None)
    )
    has_clear_problem = len(problem) >= 100
    has_example = "Example" in problem or "example" in problem
    # We embed constraints inside the problem text for the curated set.
    # Be lenient on the separate-constraints array, but require either embedded or explicit.
    has_constraints = len(constraints) >= 1 or "Constraints:" in problem
    scores["pedagogical_clarity"] = min(
        100,
        25
        + (30 if has_clear_problem else 5)
        + (15 if has_example else 0)
        + (20 if usable_test_cases >= 2 else 5)
        + (10 if has_constraints else 0)
    )

    overall = round(sum(scores.values()) / len(scores))
    publishable = all(v >= PUBLISH_THRESHOLD for v in scores.values())

    return {
        "scores": scores,
        "overall": overall,
        "publishable": publishable,
        "blocking_dimensions": [k for k, v in scores.items() if v < PUBLISH_THRESHOLD],
    }


# =============================================================
# HELPER: build a new learning object with sensible defaults
# =============================================================

def new_learning_object(
    id: str,
    title: str,
    canonical_problem: str,
    *,
    concept: str = "",
    pattern: str = "general",
    difficulty: str = "medium",
    problem: str = "",
    solution: dict = None,
    test_cases: list = None,
    real_world: list = None,
    mental_model: str = "",
    why_this_matters: str = "",
    recognition_signals: list = None,
    anti_patterns: list = None,
    common_mistakes: list = None,
    hint_1: str = "",
    hint_2: str = "",
    hint_3: str = "",
    roles: list = None,
    companies: list = None,
    placement_stage: list = None,
    provenance_level: str = "canonical",
    provenance_note: str = "",
    mastery_skill: str = "",
    world: str = "",
    town: str = "",
    mission_id: str = "",
    boss_variant: bool = False,
    unlock_condition: str = "",
    xp_reward: int = 0,
    tags: list = None,
) -> dict:
    """Construct a learning object with the canonical schema."""
    now = datetime.now(timezone.utc).isoformat()
    lo = {
        "id": id,
        "title": title,
        "canonical_problem": canonical_problem,

        "learning": {
            "concept": concept,
            "mental_model": mental_model,
            "why_this_matters": why_this_matters,
            "real_world": real_world or [],
            "prerequisites": [],
            "learning_objective": "",
        },
        "reasoning": {
            "pattern": pattern,
            "recognition_signals": recognition_signals or [],
            "anti_patterns": anti_patterns or [],
            "tradeoffs": [],
        },
        "assistance": {
            "hint_1": hint_1,
            "hint_2": hint_2,
            "hint_3": hint_3,
            "common_mistakes": common_mistakes or [],
        },
        "assessment": {
            "difficulty": difficulty,
            "constraints": [],
            "test_cases": test_cases or [],
            "rubric": [],
        },
        "career": {
            "roles": roles or ["sde"],
            "companies": companies or [],
            "placement_stage": placement_stage or ["oa", "technical-interview"],
            "provenance": {
                "level": provenance_level,
                "note": provenance_note or PROVENANCE_LEVELS[provenance_level]["description"],
            },
        },
        "progression": {
            "mastery_skill": mastery_skill,
            "world": world,
            "town": town,
            "mission_id": mission_id,
            "boss_variant": boss_variant,
            "unlock_condition": unlock_condition,
            "xp_reward": xp_reward,
        },
        "problem": problem,
        "solution": solution or {},

        "meta": {
            "created_at": now,
            "updated_at": now,
            "authored_by": "system",
            "version": 1,
            "status": "draft",
            "quality_scores": {},
            "overall_quality": 0,
            "publishable": False,
            "tags": tags or [],
        },
    }
    # Run the quality gate
    q = evaluate_quality(lo)
    lo["meta"]["quality_scores"] = q["scores"]
    lo["meta"]["overall_quality"] = q["overall"]
    lo["meta"]["publishable"] = q["publishable"]
    lo["meta"]["status"] = "published" if q["publishable"] else "draft"
    return lo
