"""
Observability service — tracks the learner funnel and algorithm health metrics.

Funnel events (the core learner journey):
  onboarding_started
  onboarding_completed
  diagnostic_started
  diagnostic_completed
  first_plan_viewed
  first_lesson_started
  first_lesson_completed
  first_assessment_submitted
  repair_mission_started
  retest_completed
  mock_oa_completed
  readiness_viewed

Algorithm health metrics:
  recommendation_acceptance_rate
  recommendation_completion_rate
  repair_success_rate
  retest_improvement
  duplicate_recommendation_rate
  empty_content_rate
  time_to_first_useful_action
  daily_plan_stability
  readiness_score_changes_after_new_evidence
  quiz_retry_reproducibility
  assessment_abandonment
  answer_key_dispute_rate

Events are stored in MongoDB (telemetry_events collection) and aggregated for
dashboards. No PII is stored — only user_id (opaque), event names, and derived
metrics.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import users_collection


async def get_telemetry_collection():
    from app.database import get_db
    db = get_db()
    return db["telemetry_events"]


async def record_event(
    user_id: str,
    event: str,
    properties: Optional[Dict[str, Any]] = None,
) -> None:
    """Record a telemetry event. Never stores PII — only user_id + event data."""
    col = await get_telemetry_collection()
    await col.insert_one({
        "user_id": user_id,
        "event": event,
        "properties": properties or {},
        "ts": datetime.now(timezone.utc),
    })


# ── Funnel event names (canonical, must match dashboard expectations) ──
FUNNEL_EVENTS: List[str] = [
    "onboarding_started",
    "onboarding_completed",
    "diagnostic_started",
    "diagnostic_completed",
    "first_plan_viewed",
    "first_lesson_started",
    "first_lesson_completed",
    "first_assessment_submitted",
    "repair_mission_started",
    "retest_completed",
    "mock_oa_completed",
    "readiness_viewed",
]

# ── Algorithm health event names ──
ALGO_HEALTH_EVENTS: List[str] = [
    "recommendation_shown",
    "recommendation_accepted",
    "recommendation_completed",
    "repair_mission_started",
    "repair_mission_completed",
    "retest_completed",
    "duplicate_recommendation",
    "empty_content",
    "readiness_computed",
]


async def get_funnel_stats(user_id: str) -> Dict[str, Any]:
    """Return funnel completion stats for a user."""
    col = await get_telemetry_collection()
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": "$event", "count": {"$sum": 1}, "first_ts": {"$min": "$ts"}}},
    ]
    results = await col.aggregate(pipeline).to_list(None)
    stats: Dict[str, Any] = {}
    for r in results:
        stats[r["_id"]] = {
            "count": r["count"],
            "first_ts": r["first_ts"],
        }
    return {
        "events": stats,
        "completed_funnel": all(e in stats for e in FUNNEL_EVENTS),
    }


async def get_algorithm_health() -> Dict[str, Any]:
    """Return algorithm health metrics across all users (aggregated)."""
    col = await get_telemetry_collection()
    now = datetime.now(timezone.utc)
    last_7d = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # Use a simple count-based approach — no date arithmetic in aggregation
    # to keep it fast on large collections.
    pipeline = [
        {"$match": {"event": {"$in": ALGO_HEALTH_EVENTS}}},
        {"$group": {"_id": "$event", "count": {"$sum": 1}}},
    ]
    results = await col.aggregate(pipeline).to_list(None)
    counts: Dict[str, int] = {r["_id"]: r["count"] for r in results}

    shown = counts.get("recommendation_shown", 0)
    accepted = counts.get("recommendation_accepted", 0)
    completed = counts.get("recommendation_completed", 0)
    duplicates = counts.get("duplicate_recommendation", 0)
    empty = counts.get("empty_content", 0)
    repairs_started = counts.get("repair_mission_started", 0)
    repairs_completed = counts.get("repair_mission_completed", 0)
    retests = counts.get("retest_completed", 0)

    return {
        "recommendation_acceptance_rate": round(accepted / shown * 100, 1) if shown else 0.0,
        "recommendation_completion_rate": round(completed / accepted * 100, 1) if accepted else 0.0,
        "repair_success_rate": round(repairs_completed / repairs_started * 100, 1) if repairs_started else 0.0,
        "retest_completion_count": retests,
        "duplicate_recommendation_rate": round(duplicates / shown * 100, 1) if shown else 0.0,
        "empty_content_rate": round(empty / shown * 100, 1) if shown else 0.0,
        "event_counts": counts,
    }
