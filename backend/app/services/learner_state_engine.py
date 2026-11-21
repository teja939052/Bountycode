"""Deterministic Bayesian learner-state estimation for Bountycode.

This is a conservative BKT v1 implementation. It consumes normalized,
server-graded observations; it does not read client-submitted scores or award
mastery from XP, streaks, lesson opens, or completion flags.

Calibration note: the default parameters are explicit starting assumptions,
not empirically calibrated Bountycode parameters. Persist the parameter
version with every estimate and evaluate it against held-out delayed outcomes.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class BKTParameters:
    """Bayesian Knowledge Tracing parameters for one skill/evidence family."""

    p_l0: float = 0.10
    p_t: float = 0.12
    p_g: float = 0.20
    p_s: float = 0.10
    version: str = "bkt-v1-initial"

    def __post_init__(self) -> None:
        for name in ("p_l0", "p_t", "p_g", "p_s"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite number")
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.p_g >= 1.0 or self.p_s >= 1.0:
            raise ValueError("guess and slip probabilities must be below 1")
        if self.p_g + self.p_s >= 1.0:
            raise ValueError("guess + slip must be below 1 for an informative model")
        if not self.version or not self.version.strip():
            raise ValueError("version must be a non-empty string")


DEFAULT_BKT_PARAMETERS = BKTParameters()


def _probability(value: float, name: str) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return float(value)


def update_bkt(
    prior_mastery: float,
    correct: bool,
    parameters: BKTParameters = DEFAULT_BKT_PARAMETERS,
) -> dict[str, float | bool | str]:
    """Apply one binary observation and one learning-transition step.

    The observation update is Bayesian:
      P(L | correct) = P(L)(1-S) / [P(L)(1-S) + (1-P(L))G]
      P(L | wrong)   = P(L)S / [P(L)S + (1-P(L))(1-G)]

    Then apply the learning transition:
      P(L_next) = P(L_observed) + (1-P(L_observed))T
    """
    prior = _probability(prior_mastery, "prior_mastery")
    if not isinstance(correct, bool):
        raise ValueError("correct must be a bool")
    if not isinstance(parameters, BKTParameters):
        raise TypeError("parameters must be BKTParameters")

    guess = parameters.p_g
    slip = parameters.p_s
    transition = parameters.p_t

    if correct:
        numerator = prior * (1.0 - slip)
        denominator = numerator + (1.0 - prior) * guess
    else:
        numerator = prior * slip
        denominator = numerator + (1.0 - prior) * (1.0 - guess)

    if denominator <= 1e-12:
        # A degenerate observation has no safe Bayesian update. Preserve the
        # prior rather than divide by zero or manufacture certainty.
        posterior = prior
    else:
        posterior = min(1.0, max(0.0, numerator / denominator))

    after_learning = posterior + (1.0 - posterior) * transition
    predicted_correct = prior * (1.0 - slip) + (1.0 - prior) * guess

    return {
        "prior_mastery": prior,
        "posterior_after_observation": posterior,
        "mastery_after_transition": min(1.0, max(0.0, after_learning)),
        "predicted_correct_probability": min(1.0, max(0.0, predicted_correct)),
        "correct": correct,
        "parameter_version": parameters.version,
    }


def estimate_skill_state(
    skill_id: str,
    observations: Iterable[Mapping[str, Any]],
    *,
    parameters: BKTParameters = DEFAULT_BKT_PARAMETERS,
    min_distinct_questions: int = 3,
    mastery_threshold: float = 0.80,
) -> dict[str, Any]:
    """Estimate one skill from oldest-first, normalized observations.

    Each accepted observation must contain:
      question_id: stable question identity
      correct: server-graded boolean result
      server_graded: literal True, set only by trusted backend code

    Only the first observation for each distinct question updates BKT. This
    conservative v1 rule prevents retries on the same item from masquerading
    as independent evidence. Callers must supply events in chronological
    (oldest-first) order. Untrusted or malformed rows are ignored.
    """
    if not skill_id or not isinstance(skill_id, str):
        raise ValueError("skill_id must be a non-empty string")
    if min_distinct_questions < 1:
        raise ValueError("min_distinct_questions must be at least 1")
    threshold = _probability(mastery_threshold, "mastery_threshold")

    mastery = parameters.p_l0
    seen_questions: set[str] = set()
    accepted = 0
    ignored = 0
    trace: list[dict[str, Any]] = []

    for observation in observations:
        if not isinstance(observation, Mapping):
            ignored += 1
            continue
        question_id = str(observation.get("question_id") or "").strip()
        correct = observation.get("correct")
        if observation.get("server_graded") is not True or not question_id:
            ignored += 1
            continue
        if not isinstance(correct, bool):
            ignored += 1
            continue
        if question_id in seen_questions:
            ignored += 1
            continue

        seen_questions.add(question_id)
        result = update_bkt(mastery, correct, parameters)
        mastery = float(result["mastery_after_transition"])
        accepted += 1
        trace.append({
            "question_id": question_id,
            "correct": correct,
            "mastery_after": round(mastery, 6),
        })

    if accepted < min_distinct_questions:
        status = "insufficient_evidence"
    elif mastery >= threshold:
        status = "mastered"
    else:
        status = "developing"

    return {
        "skill_id": skill_id,
        "mastery_probability": round(mastery, 6),
        "status": status,
        "mastery_threshold": threshold,
        "distinct_questions": accepted,
        "minimum_distinct_questions": min_distinct_questions,
        "evidence_coverage": round(min(1.0, accepted / min_distinct_questions), 4),
        "ignored_observations": ignored,
        "parameter_version": parameters.version,
        "parameters": asdict(parameters),
        "trace": trace,
        "model_note": "Initial BKT parameters; calibrate on held-out Bountycode outcomes.",
    }
