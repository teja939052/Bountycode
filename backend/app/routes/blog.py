from fastapi import APIRouter, HTTPException

from app.services.blog_service import list_blogs, get_blog

router = APIRouter(prefix="/api/v1/blog", tags=["blog"])


@router.get("")
async def blogs(tag: str | None = None):
    return {"blogs": list_blogs(tag)}


@router.get("/{slug}")
async def blog(slug: str):
    data = get_blog(slug)
    if not data:
        raise HTTPException(status_code=404, detail="blog not found")
    return data
