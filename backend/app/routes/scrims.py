from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user, optional_get_current_user
from app.database import scrims_collection
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/scrims", tags=["scrims"])

TOPICS = [
    "arrays", "linked-lists", "stack", "graph", "sorting", "dp",
    "sql", "system-design", "strings", "trees", "recursion", "binary-search"
]
DIFFICULTIES = ["beginner", "intermediate", "advanced"]
LANGUAGES = ["python", "javascript", "java", "cpp", "sql"]


def serialize_scrim(s, include_snapshots=False):
    data = {
        "id": str(s["_id"]),
        "title": s.get("title", ""),
        "description": s.get("description", ""),
        "topic": s.get("topic", ""),
        "difficulty": s.get("difficulty", ""),
        "language": s.get("language", ""),
        "duration_seconds": s.get("duration_seconds", 0),
        "author_id": str(s.get("author_id", "")),
        "author_name": s.get("author_name", ""),
        "tags": s.get("tags", []),
        "views": s.get("views", 0),
        "likes": s.get("likes", 0),
        "created_at": s.get("created_at", datetime.now(timezone.utc)).isoformat() if isinstance(s.get("created_at"), datetime) else s.get("created_at", ""),
    }
    if include_snapshots:
        data["snapshots"] = s.get("snapshots", [])
        data["final_code"] = s.get("final_code", "")
    return data


@router.get("")
async def browse_scrims(
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
):
    query = {}
    if topic:
        query["topic"] = topic
    if difficulty:
        query["difficulty"] = difficulty
    if language:
        query["language"] = language
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
        ]

    total = await scrims_collection().count_documents(query)
    cursor = scrims_collection().find(query).sort("created_at", -1).skip((page - 1) * limit).limit(limit)
    scrims = []
    async for s in cursor:
        scrims.append(serialize_scrim(s))

    return {
        "scrims": scrims,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/topics")
async def get_scrim_topics():
    return {"topics": TOPICS}


@router.get("/{scrim_id}")
async def get_scrim(scrim_id: str, user=Depends(optional_get_current_user)):
    try:
        scrim = await scrims_collection().find_one({"_id": ObjectId(scrim_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Scrim not found")

    if not scrim:
        raise HTTPException(status_code=404, detail="Scrim not found")

    await scrims_collection().update_one({"_id": ObjectId(scrim_id)}, {"$inc": {"views": 1}})
    scrim["views"] = scrim.get("views", 0) + 1

    return serialize_scrim(scrim, include_snapshots=True)


@router.post("")
async def create_scrim(body: dict, user=Depends(get_current_user)):
    required = ["title", "topic", "difficulty", "language", "snapshots"]
    for field in required:
        if field not in body:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    if body.get("topic") not in TOPICS:
        raise HTTPException(status_code=400, detail=f"Invalid topic. Must be one of: {', '.join(TOPICS)}")
    if body.get("difficulty") not in DIFFICULTIES:
        raise HTTPException(status_code=400, detail=f"Invalid difficulty. Must be one of: {', '.join(DIFFICULTIES)}")
    if body.get("language") not in LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Invalid language. Must be one of: {', '.join(LANGUAGES)}")

    if not isinstance(body["snapshots"], list) or len(body["snapshots"]) < 2:
        raise HTTPException(status_code=400, detail="At least 2 snapshots required")

    total_duration = body["snapshots"][-1].get("timestamp_ms", 0)
    scrim_doc = {
        "title": body["title"],
        "description": body.get("description", ""),
        "topic": body["topic"],
        "difficulty": body["difficulty"],
        "language": body["language"],
        "duration_seconds": total_duration // 1000,
        "author_id": ObjectId(user["_id"]),
        "author_name": user.get("name", "Anonymous"),
        "snapshots": body["snapshots"],
        "final_code": body.get("final_code", body["snapshots"][-1]["code"]),
        "tags": body.get("tags", []),
        "views": 0,
        "likes": 0,
        "created_at": datetime.now(timezone.utc),
    }

    result = await scrims_collection().insert_one(scrim_doc)
    scrim_doc["_id"] = result.inserted_id
    try:
        await record_practice(user["id"], "scrims", 20)
    except Exception:
        pass
    return serialize_scrim(scrim_doc)


@router.post("/{scrim_id}/like")
async def toggle_like(scrim_id: str, user=Depends(get_current_user)):
    try:
        scrim = await scrims_collection().find_one({"_id": ObjectId(scrim_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Scrim not found")

    if not scrim:
        raise HTTPException(status_code=404, detail="Scrim not found")

    likes = scrim.get("likes", 0)
    await scrims_collection().update_one({"_id": ObjectId(scrim_id)}, {"$set": {"likes": likes + 1}})
    return {"likes": likes + 1}


@router.delete("/{scrim_id}")
async def delete_scrim(scrim_id: str, user=Depends(get_current_user)):
    try:
        scrim = await scrims_collection().find_one({"_id": ObjectId(scrim_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Scrim not found")

    if not scrim:
        raise HTTPException(status_code=404, detail="Scrim not found")

    if str(scrim.get("author_id", "")) != str(user["_id"]):
        raise HTTPException(status_code=403, detail="You can only delete your own scrims")

    await scrims_collection().delete_one({"_id": ObjectId(scrim_id)})
    return {"success": True}
