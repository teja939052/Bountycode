"""Study Engine routes — canonical daily-learning API (sprint-first)."""
import asyncio

from fastapi import APIRouter, Depends, Query

from app.middleware.auth import get_current_user
from app.services.study_engine import record_activity
from app.services.study_sprint_bridge import get_today_sprint_first

router = APIRouter(prefix="/api/v1/study", tags=["study-engine"])


@router.get("/today")
async def today(
    force: bool = Query(False, description="Force refresh the daily plan"),
    user=Depends(get_current_user),
):
    """Daily plan: service-company sprint is the curriculum source of truth."""
    plan = await get_today_sprint_first(user["id"], force_refresh=force)

    try:
        from app.services.analytics_service import track_event

        asyncio.create_task(
            track_event(
                event="beta_activation",
                path="/api/v1/study/today",
                user_id=user["id"],
                meta={
                    "has_next": bool(plan.get("next")),
                    "source": plan.get("curriculum_source"),
                },
            )
        )
    except Exception:
        pass

    return plan


@router.post("/activity")
async def log_activity(activity: dict, user=Depends(get_current_user)):
    result = await record_activity(
        user["id"],
        activity,
        role=user.get("role") or user.get("target_role") or "sde",
    )
    try:
        if activity.get("type") == "learn" and activity.get("passed"):
            from app.services.analytics_service import track_event

            asyncio.create_task(
                track_event(
                    event="beta_first_mission_complete",
                    path="/api/v1/study/activity",
                    user_id=user["id"],
                    meta={
                        "skill_id": activity.get("skill_id"),
                        "score": activity.get("score"),
                        "time_spent": activity.get("time_spent"),
                    },
                )
            )
    except Exception:
        pass
    return {"success": True, "data": result}
