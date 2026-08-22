"""Peer Code Review Queue — deterministic peer review of submitted code.

Flow:
  submit -> pending -> (claim by another user) -> claimed -> (review) -> reviewed
A submission can receive multiple independent reviews (each reviewer claims
once). Queue assignment avoids your own items and items you already claimed.
ZERO AI — reviews are written by peers, and the endpoint only stores + tallies
them.
"""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import peer_reviews_collection, users_collection

router = APIRouter(prefix="/api/v1/peer-review", tags=["Peer Review"])

CODE_MAX_LEN = 20000


class SubmitRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    language: str = Field("python", max_length=30)
    code: str = Field(..., min_length=10, max_length=CODE_MAX_LEN)
    description: str = Field("", max_length=2000)


class ReviewRequest(BaseModel):
    comments: str = Field(..., min_length=10, max_length=3000)
    rating: int = Field(3, ge=1, le=5)
    strengths: str = Field("", max_length=2000)
    improvements: str = Field("", max_length=2000)


def _serialize_item(doc, include_code=False) -> dict:
    item = {
        "id": str(doc["_id"]),
        "user_id": doc.get("user_id"),
        "user_name": doc.get("user_name", "Anonymous"),
        "title": doc.get("title", ""),
        "language": doc.get("language", "python"),
        "description": doc.get("description", ""),
        "status": doc.get("status", "pending"),
        "reviewer_id": doc.get("reviewer_id"),
        "reviews_count": doc.get("reviews_count", 0),
        "avg_rating": doc.get("avg_rating"),
        "created_at": doc.get("created_at"),
    }
    if include_code:
        item["code"] = doc.get("code", "")
    return item


def _serialize_review(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "item_id": doc.get("item_id"),
        "reviewer_id": doc.get("reviewer_id"),
        "reviewer_name": doc.get("reviewer_name", "Anonymous"),
        "rating": doc.get("rating"),
        "comments": doc.get("comments", ""),
        "strengths": doc.get("strengths", ""),
        "improvements": doc.get("improvements", ""),
        "created_at": doc.get("created_at"),
    }


# ─── Routes ───────────────────────────────────────────────────────────────

@router.post("/submit")
async def submit_for_review(req: SubmitRequest, user=Depends(get_current_user)):
    doc = {
        "user_id": user["id"],
        "user_name": user.get("name", "Anonymous"),
        "title": req.title.strip(),
        "language": req.language.strip()[:30] or "python",
        "code": req.code,
        "description": req.description.strip(),
        "status": "pending",
        "reviewer_id": None,
        "reviews_count": 0,
        "avg_rating": None,
        "created_at": datetime.now(timezone.utc),
    }
    result = await peer_reviews_collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize_item(doc, include_code=True)


@router.get("/my")
async def my_submissions(user=Depends(get_current_user)):
    cursor = peer_reviews_collection().find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(50)

    items = []
    for item_doc in [d async for d in cursor]:
        reviews = [
            r async for r in peer_reviews_collection().find({"kind": "review", "item_id": str(item_doc["_id"])}).sort("created_at", 1)
        ]
        items.append({
            ** _serialize_item(item_doc, include_code=True),
            "reviews": [_serialize_review(r) for r in reviews],
        })
    return {"items": items}


@router.get("/queue")
async def review_queue(limit: int = 20, user=Depends(get_current_user)):
    uid = user["id"]
    cursor = peer_reviews_collection().find({
        "user_id": {"$ne": uid},
        "status": {"$in": ["pending", "claimed"]},
    }).sort("created_at", 1).limit(max(1, min(limit, 50)))

    items = []
    for doc in [d async for d in cursor]:
        already = await peer_reviews_collection().find_one({
            "kind": "review", "item_id": str(doc["_id"]), "reviewer_id": uid,
        })
        if already:
            continue
        if doc.get("status") == "claimed" and doc.get("reviewer_id") and doc.get("reviewer_id") != uid:
            continue
        items.append(_serialize_item(doc, include_code=True))
    return {"items": items}


@router.post("/{item_id}/claim")
async def claim_review(item_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")

    item = await peer_reviews_collection().find_one({"_id": oid})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item["user_id"] == user["id"]:
        raise HTTPException(status_code=400, detail="You cannot review your own code")

    already = await peer_reviews_collection().find_one({
        "kind": "review", "item_id": item_id, "reviewer_id": user["id"],
    })
    if already:
        raise HTTPException(status_code=400, detail="You already reviewed this item")

    await peer_reviews_collection().update_one(
        {"_id": oid},
        {"$set": {"status": "claimed", "reviewer_id": user["id"]}},
    )
    return {"item_id": item_id, "claimed": True}


@router.post("/{item_id}/review")
async def submit_review(item_id: str, req: ReviewRequest, user=Depends(get_current_user)):
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")

    item = await peer_reviews_collection().find_one({"_id": oid})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item["user_id"] == user["id"]:
        raise HTTPException(status_code=400, detail="You cannot review your own code")

    review_doc = {
        "kind": "review",
        "item_id": item_id,
        "reviewer_id": user["id"],
        "reviewer_name": user.get("name", "Anonymous"),
        "rating": max(1, min(5, req.rating)),
        "comments": req.comments.strip(),
        "strengths": req.strengths.strip(),
        "improvements": req.improvements.strip(),
        "created_at": datetime.now(timezone.utc),
    }
    await peer_reviews_collection().insert_one(review_doc)

    count = await peer_reviews_collection().count_documents({"kind": "review", "item_id": item_id})
    avg = await peer_reviews_collection().aggregate([
        {"$match": {"kind": "review", "item_id": item_id}},
        {"$group": {"_id": None, "avg": {"$avg": "$rating"}}},
    ]).to_list(length=1)
    avg_rating = round(avg[0]["avg"], 1) if avg else None

    await peer_reviews_collection().update_one(
        {"_id": oid},
        {"$set": {"status": "reviewed", "reviews_count": count, "avg_rating": avg_rating}},
    )
    return {"item_id": item_id, "reviewed": True, "reviews_count": count, "avg_rating": avg_rating}


@router.get("/{item_id}/reviews")
async def item_reviews(item_id: str, user=Depends(get_current_user)):
    try:
        ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    cursor = peer_reviews_collection().find({"kind": "review", "item_id": item_id}).sort("created_at", 1)
    reviews = [_serialize_review(r) async for r in cursor]
    return {"item_id": item_id, "reviews": reviews}
