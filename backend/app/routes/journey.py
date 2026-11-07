"""Journey State — the canonical endpoint for the unified journey game layer.

This uses the Journey Engine (``services.journey_engine``) as the single
orchestrator that composes from the canonical systems:

* ``Study Engine`` (``services/study_engine.py``) — daily plan: NEXT + REVIEW + PRACTICE + CHALLENGE
* ``Gamification`` (``services/gamification.py``) — Diamonds, level, coins, streak
* ``Mastery`` (``services/skill_assessment.py``) — per-skill scores
* ``Readiness`` (``services/readiness_engine.py``) — interview + OA readiness
* ``World Registry`` (``content.world_registry``) — world / town / level structure
* ``Company Blueprints`` — target company context

The result is a single ``GET /api/v1/journey/state`` payload that the frontend
renders as the student's current reality with one clear next action.

The Journey Engine sits *above* the Study Engine and adds career context,
company targets, mastery state, SRS due cards, gamification rewards, and
readiness signals.  It does NOT create new engines — it composes existing
canonical systems.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user
from app.services.journey_engine import build_journey_state
from app.database import learning_events_collection, interviews_collection, oa_sessions_collection

logger = logging.getLogger(__name__)


# ─── Canonical outcome-report builder ──────────────────────────────────────

from app.services.readiness_engine import compute_readiness


async def _build_outcomes(user_id: str) -> Dict[str, Any]:
    """Build a longitudinal outcome report from persisted LearningEvents.

    All numbers are derived from *persisted evidence only* — never simulated
    or extrapolated. When a source is absent, it is omitted rather than
    invented.
    """

    # ── Learning events (chronological) ──
    col = learning_events_collection()
    cursor = col.find({"user_id": user_id}).sort("timestamp", 1)
    events: list[dict] = []
    try:
        async for doc in cursor:
            events.append(doc)
    except Exception:
        pass

    # ── Skill-level progression from events ──
    skill_progression: dict[str, list[dict]] = {}
    for ev in events:
        sid = ev.get("skill_id")
        if not sid:
            continue
        skill_progression.setdefault(sid, []).append({
            "timestamp": ev.get("timestamp"),
            "activity_type": ev.get("activity_type"),
            "passed": ev.get("passed", False),
            "score": ev.get("score"),
            "mastery_before": ev.get("mastery_before"),
            "mastery_after": ev.get("mastery_after"),
            "diagnosis_codes": ev.get("diagnosis_codes", []),
        })

    # ── Per-skill mastery snapshots (first known → latest) ──
    skill_snapshots: list[dict] = []
    for sid, evs in skill_progression.items():
        first = evs[0]
        latest = evs[-1]
        before = first.get("mastery_before")
        after = latest.get("mastery_after")
        skill_snapshots.append({
            "skill_id": sid,
            "mastery_before": before,
            "mastery_after": after,
            "improved": (after or 0) > (before or 0),
            "assessment_count": len(evs),
            "latest_diagnosis": latest.get("diagnosis_codes", []),
        })
        # Update before/after on first and latest events for consistency
        if before is not None:
            skill_snapshots[-1]["mastery_before"] = before
        if after is not None:
            skill_snapshots[-1]["mastery_after"] = after

    # ── OA improvement (first OA score → latest OA score) ──
    oa_scores: list[float] = []
    try:
        oa_col = oa_sessions_collection()
        async for doc in oa_col.find({"user_id": user_id}).sort("started_at", 1):
            result = doc.get("result") or {}
            score = result.get("overall_readiness") or result.get("score")
            if score is not None:
                oa_scores.append(float(score))
    except Exception:
        pass

    oa_improvement: Optional[Dict[str, Any]] = None
    if len(oa_scores) >= 1:
        first_score = oa_scores[0]
        latest_score = oa_scores[-1]
        oa_improvement = {
            "first_score": first_score,
            "latest_score": latest_score,
            "improvement": round(latest_score - first_score, 1),
            "attempts": len(oa_scores),
        }

    # ── Interview improvement (first interview score → latest) ──
    interview_scores: list[float] = []
    try:
        int_col = interviews_collection()
        async for doc in int_col.find({"user_id": user_id}).sort("started_at", 1):
            score_history = doc.get("score_history", [])
            if score_history:
                avg = sum(score_history) / len(score_history) * 10  # scale 0-10 to 0-100
                interview_scores.append(round(avg, 1))
    except Exception:
        pass

    interview_improvement: Optional[Dict[str, Any]] = None
    if len(interview_scores) >= 1:
        first_score = interview_scores[0]
        latest_score = interview_scores[-1]
        interview_improvement = {
            "first_score": first_score,
            "latest_score": latest_score,
            "improvement": round(latest_score - first_score, 1),
            "attempts": len(interview_scores),
        }

    # ── Weakness → repair pipeline from events ──
    weaknesses_repaired: list[dict] = []
    repair_events = [e for e in events if e.get("activity_type") == "retest" and e.get("passed")]
    for rev in repair_events:
        weaknesses_repaired.append({
            "skill_id": rev.get("skill_id"),
            "repair_id": rev.get("repair_id"),
            "score": rev.get("score"),
            "timestamp": rev.get("timestamp"),
        })

    # ── Current readiness ──
    current_readiness: Optional[Dict[str, Any]] = None
    try:
        current_readiness = await compute_readiness(user_id)
    except Exception:
        current_readiness = None

    # ── Next best action from journey engine ──
    next_action: Optional[Dict[str, Any]] = None
    try:
        state = await build_journey_state(user_id)
        next_action = state.get("today", {}).get("next")
        if not next_action:
            next_action = state.get("priority", {}).get("winner_category")
            if next_action and isinstance(next_action, str):
                next_action = {"type": next_action}
    except Exception:
        pass

    # ── Overall trajectory summary ──
    total_events = len(events)
    total_passed = sum(1 for e in events if e.get("passed"))
    total_failed = total_events - total_passed

    return {
        "user_id": user_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_events": total_events,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "pass_rate": round(total_passed / total_events * 100, 1) if total_events else 0,
            "skills_tracked": len(skill_progression),
        },
        "skill_progression": skill_snapshots,
        "oa_improvement": oa_improvement,
        "interview_improvement": interview_improvement,
        "weaknesses_repaired": weaknesses_repaired,
        "current_readiness": current_readiness,
        "next_action": next_action,
    }

router = APIRouter(prefix="/api/v1/journey", tags=["journey"])


@router.get("/state", summary="Return the canonical journey state for the user.")
async def journey_state(user=Depends(get_current_user)):
    """Return the canonical JourneyState for the authenticated user.

    This is the single source of truth the frontend uses to render:
      - The student's character position on the world map
      - Today's next action (the answer to "What do I do next?")
      - SRS reviews due
      - Practice tasks
      - Optional challenge
      - Career readiness + company context
      - Priority scoring so the student understands why this action

    The Journey Engine composes from:
      * Study Engine (daily plan: NEXT + REVIEW + PRACTICE + CHALLENGE)
      * Gamification (Diamonds, level, coins, streak)
      * Mastery (per-skill scores)
      * Readiness (interview + OA readiness)
      * Company blueprints (target company context)
      * World Registry (progression graph)

    Result: one canonical state, one next action, no ambiguity.
    """
    user_id = user["id"]
    state = await build_journey_state(user_id)
    return {"success": True, "data": state}


@router.get("/outcomes", summary="Unified longitudinal outcome report from persisted evidence.")
async def journey_outcomes(user=Depends(get_current_user)):
    """Return a longitudinal outcome report built from persisted LearningEvents.

    This is the single endpoint that answers: "How has this student improved?"

    It aggregates evidence from the canonical LearningEvent store — never
    from simulated or extrapolated data. Each section is omitted when the
    underlying evidence source is absent.

    Sections:
      - summary       : aggregate pass/fail across all events
      - skill_progression : per-skill mastery before → after snapshots
      - oa_improvement  : first OA score → latest (with attempt count)
      - interview_improvement : first interview → latest (with attempt count)
      - weaknesses_repaired : skills repaired via the retest loop
      - current_readiness    : company-aware readiness via readiness_engine
      - next_action   : single next best action from the journey engine
    """
    report = await _build_outcomes(user["id"])
    return {"success": True, "data": report}