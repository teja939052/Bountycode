"""Study Engine routes — the single canonical daily-learning API.

Curriculum (service-company sprint) decides WHAT is learned.
Study Engine decides WHAT HAPPENS NEXT.
Mastery decides WHETHER it was learned.
"""
import asyncio

from fastapi import APIRouter, Depends, Query

from app.middleware.auth import get_current_user
from app.services.study_engine import get_today, record_activity

router = APIRouter(prefix="/api/v1/study", tags=["study-engine"])


@router.get("/today")
async def today(
    force: bool = Query(False, description="Force refresh the daily plan"),
    user=Depends(get_current_user),
):
    """Canonical daily plan — sprint-first for service-company prep."""
    plan = await get_today(user["id"], force_refresh=force)

    try:
        from app.services.analytics_service import track_event

        asyncio.create_task(
            track_event(
                event="beta_activation",
                path="/api/v1/study/today",
                user_id=user["id"],
                meta={"has_next": bool(plan.get("next")), "source": plan.get("curriculum_source")},
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
