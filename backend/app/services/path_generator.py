"""Deterministic personalization engine.

Produces explainable next-action recommendations from measured learner evidence.
Every recommendation carries reason codes so the learner understands *why* they
are being directed to a specific skill, not just *what* to do.

The engine is pure and deterministic: same inputs → same outputs, no AI,
no randomness. Backward-compatible with the legacy ``decide_next_action``
signature used by existing tests and callers.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# ─── Reason codes ────────────────────────────────────────────────────────
# Each code maps to a human-readable message shown to the learner.
REASON_MESSAGES: Dict[str, str] = {
    "LOW_FIRST_ATTEMPT_ACCURACY": "You missed most of your first attempts on this skill.",
    "RECENT_CORRECTNESS_DECLINE": "Your recent accuracy has dropped below your average.",
    "TRANSFER_EVIDENCE_MISSING": "You haven't demonstrated transfer ability for this skill yet.",
    "COMPANY_BLUEPRINT_REQUIRED": "This skill is required by your target company blueprint and needs more evidence.",
    "EVIDENCE_FRESHNESS_GAP": "You haven't practiced this skill recently; retention review is due.",
    "TRUSTED_CONTENT_INSUFFICIENT": "Not enough verified questions exist for this skill yet.",
    "TIME_EFFICIENCY_BELOW_TARGET": "You're solving correctly but slower than the target threshold.",
    "REPEATED_EXPOSURE_WITHOUT_MASTERY": "You've seen this skill multiple times without mastering it.",
    "HINT_HEAVY_SOLVING": "You've relied heavily on hints; try solving independently.",
    "READY_FOR_RETEST": "Your repair work is complete; retest to confirm mastery.",
    "STRONG_EVIDENCE_ADVANCE": "Your evidence is strong; you're ready to advance.",
    "MAINTAIN_WITH_SRS": "Your skill is adequate; spaced repetition will keep it fresh.",
    "INSUFFICIENT_EVIDENCE_PROVE": "Not enough evidence yet—complete an assessment to establish your baseline.",
}

REASON_CODE_GROUPS: Dict[str, List[str]] = {
    "repair": [
        "LOW_FIRST_ATTEMPT_ACCURACY",
        "RECENT_CORRECTNESS_DECLINE",
        "TRANSFER_EVIDENCE_MISSING",
        "COMPANY_BLUEPRINT_REQUIRED",
        "REPEATED_EXPOSURE_WITHOUT_MASTERY",
        "HINT_HEAVY_SOLVING",
    ],
    "practice": [
        "EVIDENCE_FRESHNESS_GAP",
        "TIME_EFFICIENCY_BELOW_TARGET",
    ],
    "drill": [
        "MAINTAIN_WITH_SRS",
    ],
    "mock": [
        "STRONG_EVIDENCE_ADVANCE",
    ],
    "prove": [
        "INSUFFICIENT_EVIDENCE_PROVE",
    ],
    "retain": [
        "MAINTAIN_WITH_SRS",
    ],
    "advance": [
        "STRONG_EVIDENCE_ADVANCE",
        "READY_FOR_RETEST",
    ],
}


@dataclass
class PersonalizationEvidence:
    """Raw evidence inputs for the personalization decision."""
    skill_id: str
    pattern: str
    mastery: float  # 0.0-1.0
    first_attempt_correctness: float = 0.0  # 0.0-1.0
    recent_correctness: float = 0.0  # 0.0-1.0
    difficulty: str = "medium"
    time_taken_seconds: float = 0.0
    hint_usage_count: int = 0
    repeated_exposure_count: int = 0
    transfer_performance: float = 0.0  # 0.0-1.0
    retention_gap_days: int = 0
    company_importance: float = 0.0  # 0.0-1.0
    evidence_freshness_days: int = 0
    trusted_content_sufficient: bool = True
    weakness_tier: str = "weak"


@dataclass
class PersonalizationDecision:
    """Structured next-action decision with explainable reason codes."""
    action: str  # repair/practice/drill/mock/advance/retain/prove
    skill_id: str
    reason_codes: List[str]
    reason: str  # Human-readable summary
    evidence_used: List[str] = field(default_factory=list)
    next_lesson_id: Optional[str] = None
    retest_after_days: Optional[int] = None
    estimated_minutes: int = 15
    weakness_tier: str = "weak"
    mastery: float = 0.0
    company_importance: float = 0.0


# ─── Scoring thresholds ─────────────────────────────────────────────────
CRITICAL_THRESHOLD = 0.40
WEAK_THRESHOLD = 0.60
ON_TRACK_THRESHOLD = 0.85
STRONG_THRESHOLD = 0.90

FIRST_ATTEMPT_LOW = 0.50
RECENT_DECLINE_DROP = 0.15
TRANSFER_MISSING_THRESHOLD = 0.0
RETENTION_GAP_DAYS = 7
TIME_EFFICIENCY_SLOW_RATIO = 1.5
REPEATED_EXPOSURE_COUNT = 3


def _classify_action(
    evidence: PersonalizationEvidence,
) -> str:
    """Classify the next action based on mastery tier and evidence signals."""
    m = evidence.mastery
    if m < CRITICAL_THRESHOLD:
        return "repair"
    if m < WEAK_THRESHOLD:
        return "practice"
    if m < ON_TRACK_THRESHOLD:
        return "drill"
    return "mock"


def _derive_reason_codes(
    evidence: PersonalizationEvidence,
    action: str,
) -> List[str]:
    """Derive explainable reason codes from evidence signals."""
    codes: List[str] = []

    # Mastery-tier-based codes
    if evidence.mastery < CRITICAL_THRESHOLD:
        if evidence.first_attempt_correctness < FIRST_ATTEMPT_LOW:
            codes.append("LOW_FIRST_ATTEMPT_ACCURACY")
        if evidence.repeated_exposure_count >= REPEATED_EXPOSURE_COUNT:
            codes.append("REPEATED_EXPOSURE_WITHOUT_MASTERY")
        if evidence.hint_usage_count > 0:
            codes.append("HINT_HEAVY_SOLVING")

    if evidence.mastery < WEAK_THRESHOLD:
        if evidence.recent_correctness < evidence.mastery - RECENT_DECLINE_DROP:
            codes.append("RECENT_CORRECTNESS_DECLINE")

    # Transfer evidence
    if evidence.transfer_performance <= TRANSFER_MISSING_THRESHOLD:
        codes.append("TRANSFER_EVIDENCE_MISSING")

    # Company blueprint requirement
    if evidence.company_importance > 0.5:
        codes.append("COMPANY_BLUEPRINT_REQUIRED")

    # Evidence freshness
    if evidence.evidence_freshness_days >= RETENTION_GAP_DAYS:
        codes.append("EVIDENCE_FRESHNESS_GAP")

    # Trusted content
    if not evidence.trusted_content_sufficient:
        codes.append("TRUSTED_CONTENT_INSUFFICIENT")

    # Time efficiency
    if evidence.time_taken_seconds > 0 and evidence.mastery >= WEAK_THRESHOLD:
        codes.append("TIME_EFFICIENCY_BELOW_TARGET")

    # Action-specific fallback codes
    if not codes:
        if action == "repair":
            codes.append("LOW_FIRST_ATTEMPT_ACCURACY")
        elif action == "practice":
            codes.append("EVIDENCE_FRESHNESS_GAP")
        elif action == "drill":
            codes.append("MAINTAIN_WITH_SRS")
        elif action == "mock":
            codes.append("STRONG_EVIDENCE_ADVANCE")
        elif action == "prove":
            codes.append("INSUFFICIENT_EVIDENCE_PROVE")
        elif action == "advance":
            codes.append("READY_FOR_RETEST")
        elif action == "retain":
            codes.append("MAINTAIN_WITH_SRS")

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for c in codes:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def _estimate_minutes(
    action: str,
    mastery: float,
    daily_minutes_cap: int = 30,
) -> int:
    """Estimate minutes for the recommended action."""
    base = {
        "repair": 15,
        "practice": 20,
        "drill": 15,
        "mock": 25,
        "prove": 20,
        "advance": 20,
        "retain": 10,
    }.get(action, 15)
    return min(base, daily_minutes_cap)


def _retest_after_days(action: str, mastery: float) -> Optional[int]:
    """Suggest days until retest based on action and mastery."""
    if action == "repair":
        return 3
    if action == "practice":
        return 7
    if action == "drill":
        return 14
    if action == "mock":
        return None
    return None


def decide_next_action_detailed(
    evidence: PersonalizationEvidence,
    daily_minutes_cap: int = 30,
) -> PersonalizationDecision:
    """Produce a structured, explainable next-action decision.

    Args:
        evidence: Raw learner evidence for the skill.
        daily_minutes_cap: Maximum minutes for the daily session.

    Returns:
        A PersonalizationDecision with action, reason codes, and metadata.
    """
    action = _classify_action(evidence)
    reason_codes = _derive_reason_codes(evidence, action)
    minutes = _estimate_minutes(action, evidence.mastery, daily_minutes_cap)
    retest_after = _retest_after_days(action, evidence.mastery)

    # Build a human-readable summary from the reason codes.
    messages = [REASON_MESSAGES.get(c, c) for c in reason_codes[:2]]
    if not messages:
        messages = [f"Mastery at {evidence.mastery:.0%}: {action} recommended."]
    reason = " ".join(messages)

    return PersonalizationDecision(
        action=action,
        skill_id=evidence.skill_id,
        reason_codes=reason_codes,
        reason=reason,
        estimated_minutes=minutes,
        weakness_tier=evidence.weakness_tier,
        mastery=round(evidence.mastery, 4),
        company_importance=round(evidence.company_importance, 4),
        next_lesson_id=None,
        retest_after_days=retest_after,
    )


# ─── Backward-compatible legacy API ─────────────────────────────────────

def decide_next_action(
    pattern: str,
    mastery: float,
    weakness_tier: str,
    daily_minutes_cap: int = 30,
    has_repair_available: bool = True,
) -> Dict[str, Any]:
    """Legacy API: returns a flat dict for existing callers.

    Delegates to ``decide_next_action_detailed`` internally so both paths
    share the same logic.
    """
    evidence = PersonalizationEvidence(
        skill_id=pattern,
        pattern=pattern,
        mastery=mastery,
        weakness_tier=weakness_tier,
    )
    decision = decide_next_action_detailed(evidence, daily_minutes_cap)
    return {
        "pattern": pattern,
        "mastery": decision.mastery,
        "weakness_tier": decision.weakness_tier,
        "action": decision.action,
        "estimated_minutes": decision.estimated_minutes,
        "reason": decision.reason,
        "has_repair_available": has_repair_available,
        # Extended fields (new callers can use these).
        "reason_codes": decision.reason_codes,
        "skill_id": decision.skill_id,
        "retest_after_days": decision.retest_after_days,
        "next_lesson_id": decision.next_lesson_id,
    }


def decide_for_skill(
    skill_id: str,
    mastery: float,
    *,
    first_attempt_correctness: float = 0.0,
    recent_correctness: float = 0.0,
    difficulty: str = "medium",
    time_taken_seconds: float = 0.0,
    hint_usage_count: int = 0,
    repeated_exposure_count: int = 0,
    transfer_performance: float = 0.0,
    retention_gap_days: int = 0,
    company_importance: float = 0.0,
    evidence_freshness_days: int = 0,
    trusted_content_sufficient: bool = True,
    weakness_tier: Optional[str] = None,
    daily_minutes_cap: int = 30,
) -> PersonalizationDecision:
    """Convenience builder for a full PersonalizationDecision from raw signals.

    Derives ``weakness_tier`` from mastery if not provided.
    """
    if weakness_tier is None:
        if mastery < CRITICAL_THRESHOLD:
            weakness_tier = "critical"
        elif mastery < WEAK_THRESHOLD:
            weakness_tier = "weak"
        elif mastery < ON_TRACK_THRESHOLD:
            weakness_tier = "on_track"
        else:
            weakness_tier = "strong"

    evidence = PersonalizationEvidence(
        skill_id=skill_id,
        pattern=skill_id,
        mastery=mastery,
        first_attempt_correctness=first_attempt_correctness,
        recent_correctness=recent_correctness,
        difficulty=difficulty,
        time_taken_seconds=time_taken_seconds,
        hint_usage_count=hint_usage_count,
        repeated_exposure_count=repeated_exposure_count,
        transfer_performance=transfer_performance,
        retention_gap_days=retention_gap_days,
        company_importance=company_importance,
        evidence_freshness_days=evidence_freshness_days,
        trusted_content_sufficient=trusted_content_sufficient,
        weakness_tier=weakness_tier,
    )
    return decide_next_action_detailed(evidence, daily_minutes_cap)
