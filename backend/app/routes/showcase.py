from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import showcase_collection
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/showcase", tags=["showcase"])

LANGUAGES = ["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust", "sql", "html"]


def serialize_review(r):
    return {
        "id": str(r.get("_id", "")) if r.get("_id") else "",
        "author_id": str(r.get("author_id", "")),
        "author_name": r.get("author_name", ""),
        "comment": r.get("comment", ""),
        "rating": r.get("rating", 0),
        "created_at": r.get("created_at", datetime.now(timezone.utc)).isoformat() if isinstance(r.get("created_at"), datetime) else r.get("created_at", ""),
    }


def serialize_preview(p):
    code = p.get("code", "")
    return {
        "id": str(p["_id"]),
        "title": p.get("title", ""),
        "description": p.get("description", ""),
        "code_preview": code[:200] + ("..." if len(code) > 200 else ""),
        "language": p.get("language", ""),
        "tags": p.get("tags", []),
        "author_id": str(p.get("author_id", "")),
        "author_name": p.get("author_name", ""),
        "views": p.get("views", 0),
        "likes": p.get("likes", 0),
        "review_count": len(p.get("reviews", [])),
        "created_at": p.get("created_at", datetime.now(timezone.utc)).isoformat() if isinstance(p.get("created_at"), datetime) else p.get("created_at", ""),
    }


def serialize_detail(p):
    data = serialize_preview(p)
    data["code"] = p.get("code", "")
    data["reviews"] = [serialize_review(r) for r in p.get("reviews", [])]
    return data


@router.get("")
async def browse_projects(
    tag: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
):
    query = {}
    if tag:
        query["tags"] = tag

    total = await showcase_collection().count_documents(query)
    cursor = showcase_collection().find(query).sort("created_at", -1).skip((page - 1) * limit).limit(limit)
    projects = []
    async for p in cursor:
        projects.append(serialize_preview(p))

    return {
        "projects": projects,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/tags")
async def get_project_tags():
    tags = await showcase_collection().distinct("tags")
    return {"tags": sorted(tags)}


@router.get("/{project_id}")
async def get_project(project_id: str):
    try:
        project = await showcase_collection().find_one({"_id": ObjectId(project_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await showcase_collection().update_one({"_id": ObjectId(project_id)}, {"$inc": {"views": 1}})
    project["views"] = project.get("views", 0) + 1

    return serialize_detail(project)


@router.post("")
async def create_project(body: dict, user=Depends(get_current_user)):
    title = (body.get("title") or "").strip()
    code = (body.get("code") or "").strip()

    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")

    tags = body.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    tags = [str(t).strip()[:30] for t in tags if str(t).strip()][:10]

    project_doc = {
        "title": title,
        "description": (body.get("description") or "").strip(),
        "code": code,
        "language": body.get("language") or "python",
        "tags": tags,
        "author_id": ObjectId(user["_id"]),
        "author_name": user.get("name", "Anonymous"),
        "views": 0,
        "likes": 0,
        "reviews": [],
        "created_at": datetime.now(timezone.utc),
    }

    result = await showcase_collection().insert_one(project_doc)
    project_doc["_id"] = result.inserted_id
    try:
        await record_practice(user["id"], "showcase", 15)
    except Exception:
        pass
    return serialize_detail(project_doc)


@router.post("/{project_id}/like")
async def like_project(project_id: str, user=Depends(get_current_user)):
    try:
        project = await showcase_collection().find_one({"_id": ObjectId(project_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await showcase_collection().update_one({"_id": ObjectId(project_id)}, {"$inc": {"likes": 1}})
    return {"likes": project.get("likes", 0) + 1}


@router.post("/{project_id}/reviews")
async def add_review(project_id: str, body: dict, user=Depends(get_current_user)):
    try:
        project = await showcase_collection().find_one({"_id": ObjectId(project_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    comment = (body.get("comment") or "").strip()
    if not comment:
        raise HTTPException(status_code=400, detail="Review comment is required")

    try:
        rating = int(body.get("rating", 0))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Rating must be a number between 1 and 5")
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    review = {
        "_id": ObjectId(),
        "author_id": ObjectId(user["_id"]),
        "author_name": user.get("name", "Anonymous"),
        "comment": comment,
        "rating": rating,
        "created_at": datetime.now(timezone.utc),
    }

    await showcase_collection().update_one(
        {"_id": ObjectId(project_id)},
        {"$push": {"reviews": review}},
    )

    try:
        await record_practice(user["id"], "peer_review", float(rating))
    except Exception:
        pass

    return serialize_review(review)


@router.delete("/{project_id}")
async def delete_project(project_id: str, user=Depends(get_current_user)):
    try:
        project = await showcase_collection().find_one({"_id": ObjectId(project_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if str(project.get("author_id", "")) != str(user["_id"]):
        raise HTTPException(status_code=403, detail="You can only delete your own projects")

    await showcase_collection().delete_one({"_id": ObjectId(project_id)})
    return {"success": True}
