from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.sanitizer import sanitize_text

router = APIRouter(prefix="/api/v1/community", tags=["community"])


class CreatePostRequest(BaseModel):
    content: str
    type: str = "post"
    code: Optional[str] = None
    language: Optional[str] = None


class AddCommentRequest(BaseModel):
    content: str


@router.get("/feed")
async def get_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    db = get_db()
    skip = (page - 1) * limit
    cursor = db["community_posts"].find().sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    total = await db["community_posts"].count_documents({})

    result = []
    for p in posts:
        result.append({
            "id": str(p["_id"]),
            "user_id": p["user_id"],
            "user_name": p["user_name"],
            "user_avatar": p.get("user_avatar", p["user_name"][0].upper()),
            "content": p["content"],
            "type": p.get("type", "post"),
            "code": p.get("code"),
            "language": p.get("language"),
            "likes": p.get("likes", 0),
            "liked_by": p.get("liked_by", []),
            "comments": p.get("comments", []),
            "created_at": p["created_at"].isoformat(),
        })

    return {
        "posts": result,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.post("/feed")
async def create_post(
    req: CreatePostRequest,
    user=Depends(get_current_user),
):
    db = get_db()
    if req.type not in ("post", "achievement", "streak", "solve"):
        raise HTTPException(status_code=400, detail="Invalid post type")

    doc = {
        "user_id": user["id"],
        "user_name": user.get("name", "Anonymous"),
        "user_avatar": user.get("name", "A")[0].upper(),
        "content": sanitize_text(req.content, max_length=10000),
        "type": req.type,
        "code": req.code,
        "language": req.language,
        "likes": 0,
        "liked_by": [],
        "comments": [],
        "created_at": datetime.now(timezone.utc),
    }
    result = await db["community_posts"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc["created_at"] = doc["created_at"].isoformat()
    return doc


@router.post("/feed/{post_id}/like")
async def toggle_like(post_id: str, user=Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db["community_posts"].find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    liked_by = post.get("liked_by", [])
    user_id = user["id"]
    if user_id in liked_by:
        await db["community_posts"].update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"liked_by": user_id}, "$inc": {"likes": -1}},
        )
        liked = False
    else:
        await db["community_posts"].update_one(
            {"_id": ObjectId(post_id)},
            {"$push": {"liked_by": user_id}, "$inc": {"likes": 1}},
        )
        liked = True

    updated = await db["community_posts"].find_one({"_id": ObjectId(post_id)})
    return {"likes": updated["likes"], "liked": liked}


@router.post("/feed/{post_id}/comment")
async def add_comment(post_id: str, req: AddCommentRequest, user=Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    comment = {
        "id": str(ObjectId()),
        "user_id": user["id"],
        "user_name": user.get("name", "Anonymous"),
        "content": sanitize_text(req.content, max_length=2000),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = await db["community_posts"].update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"comment": comment}


@router.delete("/feed/{post_id}")
async def delete_post(post_id: str, user=Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await db["community_posts"].find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="You can only delete your own posts")

    await db["community_posts"].delete_one({"_id": ObjectId(post_id)})
    return {"message": "Post deleted"}
