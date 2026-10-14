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
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.services.study_engine import get_today, record_activity, generate_30_day_plan, diagnose_mock_oa
from app.data.study_materials import (
    get_categories,
    get_articles,
    get_article,
    get_related_articles,
    search_articles,
)

router = APIRouter(prefix="/api/v1/study", tags=["study-engine"])


@router.get("/today")
async def today(
    force: bool = Query(False, description="Force refresh the daily plan"),
    company: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    assessment_date: Optional[str] = Query(None),
    user=Depends(get_current_user),
):
    """Return the canonical daily learning plan for the authenticated user.

    Optional query params allow the frontend to set/override the campaign
    target without a separate save call:
        /api/v1/study/today?company=Google&role=SDE&assessment_date=2026-12-01
    """
    plan = await get_today(
        user["id"],
        force_refresh=force,
        company=company,
        role=role,
        assessment_date=assessment_date,
    )

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


# ---------------------------------------------------------------------------
# Extended study endpoints (migrated from study_extended.py)
# ---------------------------------------------------------------------------

@router.get("/30-day-plan")
async def get_30_day_plan(role: str, company: str = "", user=Depends(get_current_user)):
    """Generate a 30-day preparation plan for a role/company."""
    plan = await generate_30_day_plan(user["id"], role, company)
    return {"success": True, "plan": plan}


@router.post("/mock-oa/diagnose")
async def post_mock_oa_diagnosis(responses: dict, user=Depends(get_current_user)):
    """Analyze Mock OA results and generate diagnostic report."""
    diagnosis = await diagnose_mock_oa(user["id"], responses)
    return {"success": True, "diagnosis": diagnosis}


# ---------------------------------------------------------------------------
# Study Library endpoints (migrated from study_library.py)
# ---------------------------------------------------------------------------

@router.get("/categories")
async def list_categories(user=Depends(get_current_user)):
    """List all study material categories."""
    return {"categories": get_categories()}


@router.get("/articles")
async def list_articles(
    category: str | None = Query(None, description="Filter by category id"),
    q: str | None = Query(None, description="Search query"),
    user=Depends(get_current_user),
):
    """List study articles, optionally filtered by category or search."""
    if q:
        results = search_articles(q)
    else:
        results = get_articles(category)
    return {"articles": results, "total": len(results)}


@router.get("/related")
async def related_articles(
    language: str | None = Query(None, description="Curriculum language id (e.g. react, sql)"),
    q: str | None = Query(None, description="Topic/lesson query for keyword matching"),
    limit: int = Query(3, ge=1, le=10),
    user=Depends(get_current_user),
):
    """Suggest related study articles for a lesson (connect-the-dots)."""
    results = get_related_articles(language_id=language, query=q, limit=limit)
    return {"articles": results, "total": len(results)}


@router.get("/articles/{article_id}")
async def get_article_detail(
    article_id: str,
    user=Depends(get_current_user),
):
    """Get a single study article with full section content."""
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"article": article}


@router.get("/categories/{category_id}/articles")
async def list_category_articles(
    category_id: str,
    user=Depends(get_current_user),
):
    """List all articles within a category."""
    articles = get_articles(category_id)
    if not articles:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"category_id": category_id, "articles": articles, "total": len(articles)}
