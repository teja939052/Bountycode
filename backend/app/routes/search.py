"""Global search across questions, lessons, companies, and study materials."""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("/global")
async def global_search(
    q: str = Query(..., min_length=1, description="Search query"),
    types: Optional[str] = Query(None, description="Comma-separated: questions,lessons,companies,articles"),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    """Search across the entire platform."""
    query = q.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    requested_types = [t.strip() for t in (types or "questions,lessons,companies,articles").split(",") if t.strip()]
    results: Dict[str, List[Dict[str, Any]]] = {}

    # Search questions
    if "questions" in requested_types:
        try:
            from app.services import question_store
            q_lower = query.lower()
            matched = []
            for question in question_store._questions:
                text = " ".join([
                    str(question.get("question", "")),
                    str(question.get("question_title", "")),
                    str(question.get("topic", "")),
                    str(question.get("sub_topic", "")),
                    str(question.get("company", "")),
                ]).lower()
                if q_lower in text:
                    matched.append({
                        "id": question.get("id"),
                        "title": question.get("question_title") or question.get("question", "")[:120],
                        "type": question.get("type"),
                        "topic": question.get("topic"),
                        "difficulty": question.get("difficulty"),
                        "url": f"/solve/{question.get('id')}",
                    })
                    if len(matched) >= limit:
                        break
            results["questions"] = matched
        except Exception:
            results["questions"] = []

    # Search lessons/curriculum
    if "lessons" in requested_types:
        try:
            from app.data.study_materials import search_articles
            articles = search_articles(query)[:limit]
            results["lessons"] = [
                {
                    "id": a.get("id"),
                    "title": a.get("title"),
                    "category": a.get("category"),
                    "url": f"/lab/lesson/{a.get('id')}",
                }
                for a in articles
            ]
        except Exception:
            results["lessons"] = []

    # Search companies
    if "companies" in requested_types:
        try:
            from app.data.companies_2026_2027 import COMPANIES
            q_lower = query.lower()
            matched = []
            for c in COMPANIES:
                text = " ".join([
                    str(c.get("name", "")),
                    str(c.get("type", "")),
                    str(c.get("tier", "")),
                    ", ".join(c.get("focus_areas", [])),
                    ", ".join(c.get("tags", [])),
                ]).lower()
                if q_lower in text:
                    matched.append({
                        "id": c.get("id"),
                        "name": c.get("name"),
                        "type": c.get("type"),
                        "tier": c.get("tier"),
                        "url": f"/mock-oa?company={c.get('id')}",
                    })
                    if len(matched) >= limit:
                        break
            results["companies"] = matched
        except Exception:
            results["companies"] = []

    # Search study articles
    if "articles" in requested_types:
        try:
            from app.data.study_materials import search_articles
            articles = search_articles(query)[:limit]
            results["articles"] = [
                {
                    "id": a.get("id"),
                    "title": a.get("title"),
                    "category": a.get("category"),
                    "url": f"/learn/article/{a.get('id')}",
                }
                for a in articles
            ]
        except Exception:
            results["articles"] = []

    total = sum(len(v) for v in results.values())
    return {
        "query": query,
        "total": total,
        "results": results,
    }


@router.get("/questions")
async def search_questions(
    q: str = Query(..., min_length=1),
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    limit: int = Query(30, ge=1, le=100),
    user=Depends(get_current_user),
):
    """Dedicated question search with filters."""
    try:
        from app.services import question_store
        q_lower = q.lower()
        matched = []
        for question in question_store._questions:
            text = " ".join([
                str(question.get("question", "")),
                str(question.get("question_title", "")),
                str(question.get("topic", "")),
                str(question.get("sub_topic", "")),
                str(question.get("company", "")),
            ]).lower()
            if q_lower not in text:
                continue
            if topic and topic.lower() != str(question.get("topic", "")).lower():
                continue
            if difficulty and difficulty.lower() != str(question.get("difficulty", "")).lower():
                continue
            if type and type.lower() != str(question.get("type", "")).lower():
                continue
            matched.append({
                "id": question.get("id"),
                "title": question.get("question_title") or question.get("question", "")[:120],
                "type": question.get("type"),
                "topic": question.get("topic"),
                "difficulty": question.get("difficulty"),
                "url": f"/solve/{question.get('id')}",
            })
            if len(matched) >= limit:
                break
        return {"query": q, "total": len(matched), "results": matched}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
