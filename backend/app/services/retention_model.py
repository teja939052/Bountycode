"""Small, explicit retention-decay baseline for spaced retrieval.

The exponential curve is a scheduling prior, not a claim that every learner
or skill forgets at the same rate. Half-life must eventually be calibrated per
skill/evidence family from delayed-recall observations.
"""
from __future__ import annotations

import math


def _positive_finite(value: float, field: str) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{field} must be a positive finite number")
    return float(value)


def estimate_retention(
    elapsed_days: float,
    *,
    half_life_days: float = 7.0,
) -> float:
    """Estimate retrieval probability using R(t) = 2 ** (-t / half-life)."""
    if not isinstance(elapsed_days, (int, float)) or not math.isfinite(elapsed_days):
        raise ValueError("elapsed_days must be finite")
    if elapsed_days < 0:
        raise ValueError("elapsed_days cannot be negative")
    half_life = _positive_finite(half_life_days, "half_life_days")
    return min(1.0, max(0.0, math.exp(-math.log(2.0) * float(elapsed_days) / half_life)))


def review_urgency(
    elapsed_days: float,
    *,
    half_life_days: float = 7.0,
    target_retention: float = 0.85,
) -> float:
    """Return a 0..1 urgency score once estimated retention falls below target."""
    if not isinstance(target_retention, (int, float)) or not math.isfinite(target_retention):
        raise ValueError("target_retention must be finite")
    if not 0.0 < target_retention < 1.0:
        raise ValueError("target_retention must be between 0 and 1 (exclusive)")
    retention = estimate_retention(elapsed_days, half_life_days=half_life_days)
    return round(min(1.0, max(0.0, (target_retention - retention) / target_retention)), 6)


def days_until_target_retention(
    *,
    half_life_days: float = 7.0,
    target_retention: float = 0.85,
) -> float:
    """Return the elapsed days at which the curve reaches target retention."""
    half_life = _positive_finite(half_life_days, "half_life_days")
    if not isinstance(target_retention, (int, float)) or not math.isfinite(target_retention):
        raise ValueError("target_retention must be finite")
    if not 0.0 < target_retention < 1.0:
        raise ValueError("target_retention must be between 0 and 1 (exclusive)")
    return round(-half_life * math.log(target_retention) / math.log(2.0), 6)
