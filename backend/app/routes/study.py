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
from fastapi import APIRouter, Depends, Query

from app.middleware.auth import get_current_user
from app.services.study_engine import get_today, record_activity

router = APIRouter(prefix="/api/v1/study", tags=["study-engine"])


@router.get("/today")
async def today(force: bool = Query(False, description="Force refresh the daily plan"), user=Depends(get_current_user)):
    """Return the canonical daily learning plan for the authenticated user.

    Shape::

        {
          "date": "2026-08-28",
          "user_id": "...",
          "streak": 7,
          "level": 5,
          "overall_score": 72.0,
          "overall_mastery": "practicing",
          "next": {...mission...},
          "reviews": [...srs cards...],
          "practice": [...weak-skill tasks...],
          "challenge": {...optional...},
          "totals": {"estimated_minutes": 37, "task_count": 5}
        }
    """
    return await get_today(user["id"], force_refresh=force)


@router.post("/activity")
async def log_activity(activity: dict, user=Depends(get_current_user)):
    """Record a completed learning activity and fan-out to mastery / SRS / XP.

    This is the *canonical* completion sink.  Existing routes that call
    ``record_practice`` / ``update_skill_score`` directly are left in
    place for backward compatibility, but new activity should prefer
    this endpoint so the event is observable in one place.

    Body::

        {
          "type": "learn" | "review" | "practice" | "challenge",
          "skill_id": "coding.variables",
          "competency_id": "...",
          "passed": true,
          "score": 85,
          "attempts": 1,
          "time_spent": 420
        }
    """
    result = await record_activity(user["id"], activity)
    return {"success": True, "data": result}
