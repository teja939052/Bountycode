"""Company lessons routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import get_current_user
from app.database import get_session
from app.data.company_blueprints import get_blueprint
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/company-lessons", tags=["company-lessons"])


@router.get("/companies/{company_id}/lessons")
async def list_company_lessons(
    company_id: str,
    user=Depends(get_current_user),
    topic: str = Query(None, description="Filter by topic"),
    difficulty: str = Query(None, description="Filter by difficulty"),
    limit: int = Query(50, ge=1, le=200),
):
    blueprint = get_blueprint(company_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Company not found")
    lessons = blueprint.get("lessons", [])
    if topic:
        lessons = [l for l in lessons if l.get("topic") == topic]
    if difficulty:
        lessons = [l for l in lessons if l.get("difficulty") == difficulty]
    return {"lessons": lessons[:limit], "total": len(lessons)}


@router.get("/companies/{company_id}/lessons/{lesson_id}")
async def get_company_lesson_detail(
    company_id: str,
    lesson_id: str,
    user=Depends(get_current_user),
):
    blueprint = get_blueprint(company_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Company not found")
    lesson = next((l for l in blueprint.get("lessons", []) if l.get("id") == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/search")
async def search_lessons(
    user=Depends(get_current_user),
    q: str = Query("", min_length=1),
    topic: str = Query(None, description="Filter by topic"),
    difficulty: str = Query(None, description="Filter by difficulty"),
):
    all_lessons = []
    blueprint = {}  # Would be fetched per company
    # Search across all company blueprints
    for company_id in blueprint if isinstance(blueprint, dict) else []:
        company_blueprint = get_blueprint(company_id)
        if company_blueprint:
            all_lessons.extend(company_blueprint.get("lessons", []))
    
    if q:
        lessons = [l for l in all_lessons if q.lower() in l.get("title", "").lower() or q.lower() in l.get("description", "").lower()]
    else:
        lessons = all_lessons
    if topic:
        lessons = [l for l in lessons if l.get("topic") == topic]
    if difficulty:
        lessons = [l for l in lessons if l.get("difficulty") == difficulty]
    return {"count": len(lessons), "lessons": lessons}