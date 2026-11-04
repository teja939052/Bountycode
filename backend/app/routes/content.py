from fastapi import APIRouter, HTTPException

from app.services.content_service import list_topics, get_topic_content

router = APIRouter(prefix="/api/v1/content", tags=["content"])


@router.get("/topics")
async def topics():
    return {"topics": list_topics()}


@router.get("/{topic}")
async def topic(topic: str):
    data = get_topic_content(topic)
    if not data:
        raise HTTPException(status_code=404, detail="topic not found")
    return data
