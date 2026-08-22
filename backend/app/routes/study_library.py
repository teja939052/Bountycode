"""
Study Library routes — W3Schools/freeCodeCamp-style in-depth study articles.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import get_current_user
from app.data.study_materials import (
    get_categories,
    get_articles,
    get_article,
    get_related_articles,
    search_articles,
)

router = APIRouter(prefix="/api/v1/study", tags=["study"])


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
