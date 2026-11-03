"""Deterministic path generator."""
from typing import Any, Dict


def decide_next_action(
    pattern: str,
    mastery: float,
    weakness_tier: str,
    daily_minutes_cap: int = 30,
    has_repair_available: bool = True,
) -> Dict[str, Any]:
    if weakness_tier == "critical":
        action = "repair"
        minutes = min(15, daily_minutes_cap)
        reason = "Mastery critical (<0.40): targeted repair required before new content."
    elif weakness_tier == "weak":
        action = "practice"
        minutes = min(20, daily_minutes_cap)
        reason = "Mastery weak (0.40-0.60): focused practice to lift mastery."
    elif weakness_tier == "on_track":
        action = "drill"
        minutes = min(15, daily_minutes_cap)
        reason = "Mastery on track (0.60-0.85): mixed drill for retention."
    else:
        action = "mock"
        minutes = min(25, daily_minutes_cap)
        reason = "Mastery strong (>=0.85): challenge with a mock exam."
    return {
        "pattern": pattern,
        "mastery": round(mastery, 4),
        "weakness_tier": weakness_tier,
        "action": action,
        "estimated_minutes": minutes,
        "reason": reason,
        "has_repair_available": has_repair_available,
    }
