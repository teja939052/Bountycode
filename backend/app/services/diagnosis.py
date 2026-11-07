"""Structured diagnosis engine.

Derives structured diagnosis codes from *observable evidence* (scores,
timing, answer content) — never from keyword matching on skill names alone.

Canonical diagnosis codes are defined in ``app.models.learning_event``.
This module provides evidence-based functions that decide *which* codes
apply given the actual performance signals.

Public entry points
    diagnose_question_failure  — single-question assessment events
    diagnose_interview_failure — per-dimension interview scores
    diagnose_oa_section_failure — OA section performance + timing
"""
from __future__ import annotations

from typing import Any, Dict, List

# Re-export canonical codes so callers can import from one place.
from app.models.learning_event import (
    CONCEPT_GAP,
    PATTERN_RECOGNITION,
    TRANSFER_FAILURE,
    TIME_MANAGEMENT,
    IMPLEMENTATION_ERROR,
    EDGE_CASE_FAILURE,
    COMPLEXITY_ERROR,
    KNOWLEDGE_RECALL,
    COMMUNICATION_DEPTH,
    TRADEOFF_REASONING,
    REQUIREMENT_MISREAD,
    CARELESS_ERROR,
    DEBUGGING,
    ALL_DIAGNOSIS_CODES,
)

# ── Code-specific aliases for readability ────────────────────────────────
CODE_CORRECTNESS = IMPLEMENTATION_ERROR
CODE_EFFICIENCY = COMPLEXITY_ERROR
EDGE_CASE_MISSED = EDGE_CASE_FAILURE
PARTIAL_UNDERSTANDING = CONCEPT_GAP
CONCEPTUAL_MISMATCH = CONCEPT_GAP
COMMUNICATION_CLARITY = COMMUNICATION_DEPTH
DEPTH_OF_KNOWLEDGE = COMMUNICATION_DEPTH
TECHNICAL_ACCURACY = CONCEPT_GAP
PROBLEM_SOLVING_APPROACH = TRADEOFF_REASONING

# Human-readable labels for each code
DIAGNOSIS_LABELS: Dict[str, str] = {
    CONCEPT_GAP: "Concept gap — missing prerequisite knowledge",
    PATTERN_RECOGNITION: "Pattern recognition — can't identify common problem patterns",
    IMPLEMENTATION_ERROR: "Implementation error — logic bug in solution",
    EDGE_CASE_FAILURE: "Edge case — missed boundary conditions",
    COMPLEXITY_ERROR: "Complexity error — suboptimal time/space",
    TIME_MANAGEMENT: "Time management — too slow or ran out of time",
    CARELESS_ERROR: "Careless error — minor avoidable mistake",
    DEBUGGING: "Debugging — can't locate/identify the bug",
    KNOWLEDGE_RECALL: "Knowledge recall — doesn't remember key facts",
    TRANSFER_FAILURE: "Transfer failure — can't apply concept in new context",
    COMMUNICATION_DEPTH: "Communication / depth",
    TRADEOFF_REASONING: "Trade-off reasoning",
    REQUIREMENT_MISREAD: "Requirement misread",
}

# ── Interview dimension → primary diagnosis code ────────────────────────
_INTERVIEW_DIMENSION_DEFAULTS: Dict[str, str] = {
    "technical": CONCEPT_GAP,
    "communication": COMMUNICATION_DEPTH,
    "problem_solving": TRADEOFF_REASONING,
    "depth": COMMUNICATION_DEPTH,
    "explanation": COMMUNICATION_DEPTH,
    "tradeoff": TRADEOFF_REASONING,
    "system_design": TRADEOFF_REASONING,
}

# Pattern keyword signals — evidence-based text classification of feedback
_PATTERN_SIGNALS: List[tuple[str, str]] = [
    ("pattern", PATTERN_RECOGNITION),
    ("recognize", PATTERN_RECOGNITION),
    ("algorithm", PATTERN_RECOGNITION),
    ("approach", TRADEOFF_REASONING),
    ("wrong direction", TRADEOFF_REASONING),
    ("complexity", COMPLEXITY_ERROR),
    ("inefficient", COMPLEXITY_ERROR),
    ("too slow", TIME_MANAGEMENT),
    ("time", TIME_MANAGEMENT),
    ("edge", EDGE_CASE_FAILURE),
    ("boundary", EDGE_CASE_FAILURE),
    ("arithmetic", CARELESS_ERROR),
    ("calculation", CARELESS_ERROR),
    ("logic error", IMPLEMENTATION_ERROR),
    ("wrong answer", IMPLEMENTATION_ERROR),
    ("debug", DEBUGGING),
    ("trace", DEBUGGING),
    ("partial", CONCEPT_GAP),
    ("incomplete", CONCEPT_GAP),
    ("confus", CONCEPT_GAP),
    ("missing", CONCEPT_GAP),
    ("transfer", TRANSFER_FAILURE),
    ("recall", KNOWLEDGE_RECALL),
    ("forgot", KNOWLEDGE_RECALL),
    ("tradeoff", TRADEOFF_REASONING),
    ("trade-off", TRADEOFF_REASONING),
]


def _classify_text(text: str) -> List[str]:
    """Return diagnosis codes matched against feedback/improvement text."""
    if not text:
        return []
    lowered = text.lower()
    codes: List[str] = []
    for keyword, code in _PATTERN_SIGNALS:
        if keyword in lowered and code not in codes:
            codes.append(code)
    return codes


# ── Question-answer assessment diagnosis ──────────────────────────────────

def diagnose_question_failure(
    score: float,
    answer_text: str,
    q_type: str,
    question: Dict[str, Any],
    metadata: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Derive structured diagnosis codes from a single-question assessment.

    Args:
        score: 0-10 numeric score (or 0-100 percentage — auto-normalized).
        answer_text: the student's answer (may be empty for code questions).
        q_type: "coding", "aptitude", "mcq", "text", etc.
        question: the question dict from the store.
        metadata: optional extra context (all_passed, passed_count, total).

    Returns:
        ``{"codes": [...], "reason": "..."}``
    """
    meta = metadata or {}
    codes: List[str] = []

    # Normalize score to 0-10
    normalized = score
    if normalized > 10:
        normalized = normalized / 10.0

    # ── Coding questions ──
    if q_type == "coding" or "code" in (q_type or ""):
        all_passed = meta.get("all_passed", False)
        passed_count = meta.get("passed_count", 0)
        total = meta.get("total", 0)

        if not all_passed:
            codes.append(IMPLEMENTATION_ERROR)
            if total and passed_count / total < 0.5:
                codes.append(PATTERN_RECOGNITION)
            if passed_count > 0 and passed_count < total:
                codes.append(EDGE_CASE_FAILURE)
            if meta.get("time_pressure"):
                codes.append(TIME_MANAGEMENT)

    # ── MCQ / aptitude questions ──
    elif q_type in ("mcq", "aptitude", "aptitude_mcq"):
        if normalized < 5:
            codes.append(CONCEPT_GAP)
        elif normalized < 7:
            codes.append(CONCEPT_GAP)
            codes.append(KNOWLEDGE_RECALL)
        else:
            codes.append(KNOWLEDGE_RECALL)

    # ── Text answer questions ──
    else:
        if normalized < 3:
            codes.append(CONCEPT_GAP)
        elif normalized < 5:
            codes.append(CONCEPT_GAP)
            codes.append(TRANSFER_FAILURE)
        elif normalized < 7:
            codes.append(CONCEPT_GAP)

    # Score threshold for complete miss
    if normalized == 0:
        codes.insert(0, CONCEPT_GAP)
    elif normalized <= 3:
        if CONCEPT_GAP not in codes:
            codes.append(CONCEPT_GAP)

    # ── Text classification supplementation ──
    text = ""
    if isinstance(question, dict):
        improvements = question.get("improvements")
        if isinstance(improvements, list):
            text = " ".join(str(x) for x in improvements)
        else:
            text = question.get("feedback", "") or question.get("explanation", "") or ""

    text_codes = _classify_text(text)
    for tc in text_codes:
        if tc not in codes:
            codes.append(tc)

    # Answer length heuristic for text answers
    if answer_text and len(answer_text.strip()) < 20 and normalized < 5:
        if CONCEPT_GAP not in codes:
            codes.append(CONCEPT_GAP)

    # Only default to CONCEPT_GAP for genuinely poor performance.
    # High scores (>= 7) with no other signals get an empty list (no diagnosis).
    if not codes and normalized < 7:
        codes = [CONCEPT_GAP]

    reason = DIAGNOSIS_LABELS.get(codes[0], codes[0]) if codes else "No diagnosis — performance acceptable"
    return {"codes": codes[:4], "reason": reason}


# ── Interview dimension diagnosis ────────────────────────────────────────

def diagnose_interview_failure(
    dimension: str,
    score: float,
    feedback: Dict[str, Any] | str | None,
    answer_text: str,
    question_topic: str | None = None,
) -> List[str]:
    """Derive diagnosis codes for a single interview dimension score.

    ``score`` is 0-10 (10 = perfect).  Below 5 → strong gap signals;
    5-6 → moderate gaps; 7-9 → minor polish areas.

    Returns a list of canonical code strings (may be empty if score >= 8).
    """
    if score >= 8:
        return []

    codes: List[str] = []
    default_code = _INTERVIEW_DIMENSION_DEFAULTS.get(dimension, CONCEPT_GAP)

    if score < 5:
        codes.append(default_code)
        if dimension in ("technical", "problem_solving"):
            codes.append(CONCEPT_GAP)
    elif score < 7:
        codes.append(default_code)
        codes.append(KNOWLEDGE_RECALL)
    else:
        codes.append(default_code)

    # Text-based supplementation from feedback
    text = ""
    if isinstance(feedback, dict):
        text = " ".join(
            str(x) for x in [
                feedback.get("feedback", ""),
                *feedback.get("improvements", []),
                *feedback.get("strengths", []),
            ]
        )
    elif isinstance(feedback, str):
        text = feedback

    text_codes = _classify_text(text)
    for tc in text_codes:
        if tc not in codes:
            codes.append(tc)

    return codes[:3]


# ── OA section diagnosis ─────────────────────────────────────────────────

def diagnose_oa_section_failure(
    section: str,
    avg_score: float,
    total: int,
    correct: int,
    time_per_question: List[int] | None = None,
    question_stats: List[Dict[str, Any]] | None = None,
) -> List[str]:
    """Derive diagnosis codes for an OA section based on accuracy + timing.

    Used by the OA completion flow to emit structured diagnosis codes
    alongside each ``oa_complete`` LearningEvent.

    Args:
        section: OA section name (e.g. "aptitude", "coding").
        avg_score: section average percentage (0-100).
        total: number of questions in the section.
        correct: number of correct answers.
        time_per_question: list of per-question times in seconds.
        question_stats: list of per-question dicts with ``correct`` and ``difficulty``.

    Returns:
        List of canonical diagnosis code strings.
    """
    codes: List[str] = []
    accuracy = correct / total if total > 0 else 0.0

    # ── Accuracy-based classification ──
    if accuracy < 0.3:
        codes.append(CONCEPT_GAP)
    elif accuracy < 0.5:
        codes.append(CONCEPT_GAP)
        codes.append(KNOWLEDGE_RECALL)
    elif accuracy < 0.7:
        codes.append(KNOWLEDGE_RECALL)
        codes.append(IMPLEMENTATION_ERROR)

    # ── Coding-specific: difficulty-level performance ──
    if section in ("coding", "dsa", "system_design", "arrays", "trees", "graphs", "dp"):
        if question_stats:
            hard_correct = sum(1 for q in question_stats if q.get("difficulty") == "hard" and q.get("correct"))
            hard_total = sum(1 for q in question_stats if q.get("difficulty") == "hard")
            if hard_total > 0 and hard_correct / hard_total < 0.3:
                codes.append(PATTERN_RECOGNITION)

    # ── Time management ──
    if time_per_question and avg_score > 0:
        avg_time = sum(time_per_question) / len(time_per_question)
        # If average time per question exceeds typical threshold and accuracy is low
        if avg_time > 120 and accuracy < 0.6:
            codes.append(TIME_MANAGEMENT)
        elif avg_time > 180:
            codes.append(TIME_MANAGEMENT)
        # Check for outlier slow questions
        slow_count = sum(1 for t in time_per_question if t > avg_time * 2)
        if slow_count >= 3 and accuracy < 0.7:
            codes.append(TIME_MANAGEMENT)

    # ── Zero score → fundamental gap ──
    if avg_score == 0:
        codes = [CONCEPT_GAP]

    return list(dict.fromkeys(codes))  # dedupe, preserve order
