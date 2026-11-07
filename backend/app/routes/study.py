"""Study Engine routes — the single canonical daily-learning API.

Per the canonical architecture:

    Curriculum decides WHAT is learned.
    Study Engine decides WHAT HAPPENS NEXT  ← this file
    Mastery decides WHETHER it was learned.
    Gamification REWARDS the outcome.
    Readiness reports career preparedness.

The home screen calls ``GET /api/v1/study/today`` and renders whatever
shape the Study Engine returns — the frontend does not need to know
which subsystem (curriculum, SRS, adaptive learning, gamification)
supplied each activity.

Legacy endpoints:

    * ``GET /api/v1/adaptive/daily-plan`` — kept as a thin alias so
      existing frontends keep working; new code should prefer
      ``/study/today``.
"""

import asyncio
from fastapi import APIRouter, Depends, Query

from app.middleware.auth import get_current_user
from app.services.study_engine import get_today, record_activity

router = APIRouter(prefix="/api/v1/study", tags=["study-engine"])


@router.get("/today")
async def today(force: bool = Query(False, description="Force refresh the daily plan"), user=Depends(get_current_user)):
    """Return the canonical daily learning plan for the authenticated user."""
    plan = await get_today(user["id"], force_refresh=force)

    # Beta funnel: track first activation (first time getting a plan)
    try:
        from app.services.analytics_service import track_event
        asyncio.create_task(track_event(
            event="beta_activation",
            path="/api/v1/study/today",
            user_id=user["id"],
            meta={"has_next": bool(plan.get("next"))},
        ))
    except Exception:
        pass

    return plan


@router.get("/prerequisites/{target_skill_id}")
async def prerequisite_learning_step(
    target_skill_id: str,
    user=Depends(get_current_user),
):
    """Return the next prerequisite lesson/diagnostic step for a target skill.

    Progress is derived from persisted, distinct server-graded question-bank
    events. Client-provided scores and lesson-completion flags are not accepted.
    """
    from app.services.prerequisite_graph import get_user_prerequisite_learning_step

    result = await get_user_prerequisite_learning_step(
        user["id"],
        target_skill_id,
    )
    return {"success": True, **result}


@router.post("/activity")
async def log_activity(activity: dict, user=Depends(get_current_user)):
    """Record a completed learning activity and fan-out to mastery / SRS / Diamonds."""
    result = await record_activity(user["id"], activity, role=user.get("role") or user.get("target_role") or "sde")

    # Beta funnel: track first mission completion
    try:
        if activity.get("type") == "learn" and activity.get("passed"):
            from app.services.analytics_service import track_event
            asyncio.create_task(track_event(
                event="beta_first_mission_complete",
                path="/api/v1/study/activity",
                user_id=user["id"],
                meta={
                    "skill_id": activity.get("skill_id"),
                    "score": activity.get("score"),
                    "time_spent": activity.get("time_spent"),
                },
            ))
    except Exception:
        pass

    return {"success": True, "data": result}
