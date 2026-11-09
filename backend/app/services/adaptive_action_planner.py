"""Explainable next-best-action selection for BALMA/BLPA.

The v1 policy ranks already-authored actions. It does not generate content or
claim calibrated learning gains. Candidate estimates must be supplied by
trusted platform services and measured through offline/online evaluation.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class PlannerWeights:
    """Versioned policy weights; tune only through measured evaluation."""

    retention: float = 0.15
    uncertainty: float = 0.10
    minimum_content_quality: float = 0.55
    version: str = "blpa-v1-heuristic"

    def __post_init__(self) -> None:
        for name in ("retention", "uncertainty", "minimum_content_quality"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if not self.version:
            raise ValueError("version must be non-empty")


DEFAULT_PLANNER_WEIGHTS = PlannerWeights()
PREREQUISITE_BYPASS_KINDS = {"diagnostic", "prerequisite_lesson", "review"}


def _unit(value: Any, field: str, default: float | None = None) -> float:
    if value is None and default is not None:
        return default
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{field} must be a finite number")
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{field} must be between 0 and 1")
    return value


def score_action(
    candidate: Mapping[str, Any],
    *,
    time_budget_minutes: float,
    weights: PlannerWeights = DEFAULT_PLANNER_WEIGHTS,
) -> dict[str, Any]:
    """Score one eligible action using expected value per minute.

    v1 heuristic:
      benefit = expected mastery gain × goal relevance × dependency value
                + retention urgency + uncertainty reduction
      score = benefit × content quality × difficulty fit × novelty / minutes
              - fatigue penalty

    Hard constraints (availability, time, prerequisites and content quality)
    are evaluated before ranking. Prerequisite bypass is limited to diagnostic,
    prerequisite lesson and review actions.
    """
    if not isinstance(candidate, Mapping):
        raise ValueError("candidate must be a mapping")
    if not isinstance(time_budget_minutes, (int, float)) or not math.isfinite(time_budget_minutes):
        raise ValueError("time_budget_minutes must be finite")
    if time_budget_minutes <= 0:
        raise ValueError("time_budget_minutes must be positive")

    action_id = str(candidate.get("action_id") or "").strip()
    skill_id = str(candidate.get("skill_id") or "").strip()
    kind = str(candidate.get("kind") or "").strip().lower()
    if not action_id or not skill_id or not kind:
        raise ValueError("action_id, skill_id and kind are required")

    if candidate.get("available", True) is not True:
        raise ValueError("action_unavailable")
    minutes = candidate.get("estimated_minutes")
    if not isinstance(minutes, (int, float)) or not math.isfinite(minutes) or minutes <= 0:
        raise ValueError("invalid_estimated_minutes")
    if minutes > time_budget_minutes:
        raise ValueError("exceeds_time_budget")

    prerequisites_met = candidate.get("prerequisites_met", True)
    if not isinstance(prerequisites_met, bool):
        raise ValueError("prerequisites_met must be bool")
    if not prerequisites_met and kind not in PREREQUISITE_BYPASS_KINDS:
        raise ValueError("prerequisites_not_met")

    gain = _unit(candidate.get("expected_mastery_gain"), "expected_mastery_gain")
    goal = _unit(candidate.get("goal_relevance"), "goal_relevance", 0.5)
    dependency = _unit(candidate.get("dependency_importance"), "dependency_importance", 0.5)
    retention = _unit(candidate.get("retention_urgency"), "retention_urgency", 0.0)
    uncertainty = _unit(candidate.get("uncertainty_reduction"), "uncertainty_reduction", 0.0)
    quality = _unit(candidate.get("content_quality"), "content_quality", 1.0)
    difficulty_fit = _unit(candidate.get("difficulty_fit"), "difficulty_fit", 1.0)
    novelty = _unit(candidate.get("novelty"), "novelty", 1.0)
    fatigue = _unit(candidate.get("fatigue_penalty"), "fatigue_penalty", 0.0)

    if quality < weights.minimum_content_quality:
        raise ValueError("content_quality_below_release_threshold")

    mastery_value = gain * (0.5 + 0.5 * goal) * (0.75 + 0.25 * dependency)
    retention_value = weights.retention * retention
    uncertainty_value = weights.uncertainty * uncertainty
    raw_benefit = mastery_value + retention_value + uncertainty_value

    quality_factor = 0.5 + 0.5 * quality
    difficulty_factor = 0.5 + 0.5 * difficulty_fit
    novelty_factor = 0.5 + 0.5 * novelty
    value_per_minute = (
        raw_benefit * quality_factor * difficulty_factor * novelty_factor / float(minutes)
    )
    final_score = max(0.0, value_per_minute - 0.10 * fatigue)

    rationale: list[str] = []
    if gain > 0:
        rationale.append("expected mastery gain")
    if retention > 0:
        rationale.append("retention need")
    if uncertainty > 0:
        rationale.append("useful diagnostic information")
    if not rationale:
        rationale.append("no measurable benefit supplied")

    return {
        "action_id": action_id,
        "skill_id": skill_id,
        "kind": kind,
        "score": round(final_score, 8),
        "estimated_minutes": float(minutes),
        "benefit_per_minute": round(value_per_minute, 8),
        "components": {
            "mastery_value": round(mastery_value, 6),
            "retention_value": round(retention_value, 6),
            "uncertainty_value": round(uncertainty_value, 6),
            "content_quality_factor": round(quality_factor, 6),
            "difficulty_fit_factor": round(difficulty_factor, 6),
            "novelty_factor": round(novelty_factor, 6),
            "fatigue_penalty": round(0.10 * fatigue, 6),
        },
        "rationale": rationale,
        "policy_version": weights.version,
    }


def rank_actions(
    candidates: Iterable[Mapping[str, Any]],
    *,
    time_budget_minutes: float,
    weights: PlannerWeights = DEFAULT_PLANNER_WEIGHTS,
) -> dict[str, Any]:
    """Return deterministic ranking plus explicit rejection reasons."""
    ranked: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []

    for candidate in candidates:
        candidate_id = str(candidate.get("action_id") or "unknown")
        try:
            ranked.append(score_action(
                candidate,
                time_budget_minutes=time_budget_minutes,
                weights=weights,
            ))
        except (TypeError, ValueError) as exc:
            rejected.append({"action_id": candidate_id, "reason": str(exc)})

    ranked.sort(key=lambda item: (-item["score"], item["estimated_minutes"],
                                  item["skill_id"], item["action_id"]))
    return {
        "status": "ranked" if ranked else "no_feasible_action",
        "selected": ranked[0] if ranked else None,
        "ranked_actions": ranked,
        "rejected_actions": rejected,
        "time_budget_minutes": float(time_budget_minutes),
        "policy_version": weights.version,
        "policy_note": "Heuristic v1; validate against a fixed-curriculum baseline.",
    }
