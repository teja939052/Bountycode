"""Friend system — invite-by-UID friending + friend graph for DM chat.

Every user gets a shareable chat ID (`UID_XXXXXX`). Friends are added by
sending a request addressed to another user's UID; accepting the request
creates a persistent friendship used to scope DM chat rooms (see chat.py).
"""
import secrets
import string
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import friend_requests_collection, friends_collection, users_collection

router = APIRouter(prefix="/api/v1/friends", tags=["Friends"])

UID_PREFIX = "UID_"
UID_LENGTH = 6
UID_ALPHABET = string.ascii_uppercase.replace("I", "").replace("O", "") + "23456789"
MAX_PENDING_SENT = 50


class UidRequest(BaseModel):
    uid: str = Field(..., min_length=4, max_length=64)


def _now():
    return datetime.now(timezone.utc)


def _serialize_friend(doc: dict, my_id: str) -> dict:
    ids = doc.get("user_ids") or []
    other = next((u for u in ids if u != my_id), None)
    names = doc.get("names") or {}
    uids = doc.get("uids") or {}
    return {
        "friend_id": other,
        "name": names.get(other) or (names.get(my_id) or "Unknown"),
        "uid": uids.get(other) or "",
        "since": doc.get("created_at"),
    }


def _serialize_request(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "from_id": doc.get("from_id"),
        "from_name": doc.get("from_name", "Anonymous"),
        "from_uid": doc.get("from_uid", ""),
        "to_id": doc.get("to_id"),
        "to_name": doc.get("to_name", "Anonymous"),
        "to_uid": doc.get("to_uid", ""),
        "status": doc.get("status"),
        "created_at": doc.get("created_at"),
    }


async def _get_user_by_uid(uid: str):
    clean = (uid or "").strip().upper()
    return await users_collection().find_one({"uid": clean})


async def _is_friend(a: str, b: str) -> bool:
    if a == b:
        return False
    lo, hi = sorted([a, b])
    doc = await friends_collection().find_one({"user_ids": [lo, hi]})
    return doc is not None


async def _ensure_uid(user_id: str) -> str:
    """Return the user's UID, generating and persisting one if missing."""
    user = await users_collection().find_one({"_id": ObjectId(user_id)})
    if user and user.get("uid"):
        return user["uid"]

    for _ in range(5):
        uid = UID_PREFIX + "".join(secrets.choice(UID_ALPHABET) for _ in range(UID_LENGTH))
        try:
            await users_collection().update_one(
                {"_id": ObjectId(user_id)},
                {"$setOnInsert": {"uid": uid}},
                upsert=True,
            )
        except Exception:
            continue
        await users_collection().update_one(
            {"_id": ObjectId(user_id), "uid": {"$exists": False}},
            {"$set": {"uid": uid}},
        )
        return uid
    raise HTTPException(status_code=500, detail="Could not allocate chat ID")


@router.get("/uid")
async def my_uid(user=Depends(get_current_user)):
    """Get (and lazily allocate) my shareable chat ID."""
    uid = await _ensure_uid(user["id"])
    return {"uid": uid}


@router.get("/overview")
async def friends_overview(user=Depends(get_current_user)):
    """Full friend graph: my UID, friends, received + sent requests."""
    uid = await _ensure_uid(user["id"])
    me = user["id"]

    friends = []
    cursor = friends_collection().find({"user_ids": me}).sort("created_at", -1).limit(200)
    async for doc in cursor:
        friends.append(_serialize_friend(doc, me))

    received, sent = [], []
    cursor = friend_requests_collection().find(
        {"$or": [{"from_id": me}, {"to_id": me}]}
    ).sort("created_at", -1).limit(100)
    async for doc in cursor:
        item = _serialize_request(doc)
        if doc["from_id"] == me:
            sent.append(item)
        elif doc["to_id"] == me:
            received.append(item)

    return {"uid": uid, "friends": friends, "received": received, "sent": sent}


@router.get("/me")
async def friends_overview_alias(user=Depends(get_current_user)):
    return await friends_overview(user)


@router.post("/request")
async def send_request(req: UidRequest, user=Depends(get_current_user)):
    """Send a friend request to a user identified by their chat ID (UID_XXXXXX)."""
    me = user["id"]
    target = await _get_user_by_uid(req.uid)
    if not target:
        raise HTTPException(status_code=404, detail="No user found with that chat ID")

    target_id = str(target["_id"])
    if target_id == me:
        raise HTTPException(status_code=400, detail="You cannot add yourself")

    if await _is_friend(me, target_id):
        raise HTTPException(status_code=400, detail="You are already friends")

    existing = await friend_requests_collection().find_one({
        "from_id": me, "to_id": target_id, "status": "pending",
    })
    if existing:
        raise HTTPException(status_code=400, detail="Request already pending")

    reverse = await friend_requests_collection().find_one({
        "from_id": target_id, "to_id": me, "status": "pending",
    })
    if reverse:
        # Auto-accept mutual requests (the other person already asked us).
        await accept_request(reverse["_id"], user)
        return {"status": "accepted", "mutual": True}

    pending = await friend_requests_collection().count_documents({"from_id": me, "status": "pending"})
    if pending >= MAX_PENDING_SENT:
        raise HTTPException(status_code=400, detail="Too many pending requests — accept or cancel some first")

    target_name = target.get("name") or "Anonymous"
    target_uid = target.get("uid") or await _ensure_uid(target_id)
    doc = {
        "kind": "request",
        "from_id": me,
        "from_name": user.get("name", "Anonymous"),
        "from_uid": await _ensure_uid(me),
        "to_id": target_id,
        "to_name": target_name,
        "to_uid": target_uid,
        "status": "pending",
        "created_at": _now(),
    }
    result = await friend_requests_collection().insert_one(doc)
    return {"id": str(result.inserted_id), "status": "pending"}


@router.post("/lookup")
async def lookup_uid(req: UidRequest, user=Depends(get_current_user)):
    """Resolve a chat ID to a user's public profile (name + id)."""
    target = await _get_user_by_uid(req.uid)
    if not target:
        raise HTTPException(status_code=404, detail="No user found with that chat ID")
    return {
        "user_id": str(target["_id"]),
        "name": target.get("name", "Anonymous"),
        "uid": target.get("uid"),
    }


async def accept_request(request_id, user):
    me = user["id"]
    request = await friend_requests_collection().find_one({"_id": request_id, "status": "pending"})
    if not request:
        raise HTTPException(status_code=404, detail="Request not found or already handled")
    if request["to_id"] != me:
        raise HTTPException(status_code=403, detail="Not addressed to you")

    a, b = request["from_id"], me
    lo, hi = sorted([a, b])
    await friends_collection().update_one(
        {"user_ids": [lo, hi]},
        {
            "$setOnInsert": {
                "user_ids": [lo, hi],
                "names": {
                    a: request["from_name"],
                    b: user.get("name", "Anonymous"),
                },
                "uids": {
                    a: request["from_uid"],
                    b: await _ensure_uid(me),
                },
                "created_at": _now(),
            }
        },
        upsert=True,
    )
    await friend_requests_collection().update_one(
        {"_id": request_id}, {"$set": {"status": "accepted"}},
    )
    # Decline any pending requests from the same two users (both directions).
    await friend_requests_collection().update_many(
        {
            "status": "pending",
            "$or": [
                {"from_id": a, "to_id": b},
                {"from_id": b, "to_id": a},
            ],
        },
        {"$set": {"status": "accepted"}},
    )
    return True


@router.post("/requests/{request_id}/accept")
async def accept_request_route(request_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(request_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request ID")
    await accept_request(oid, user)
    return {"status": "accepted"}


@router.post("/requests/{request_id}/decline")
async def decline_request(request_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(request_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request ID")
    request = await friend_requests_collection().find_one({"_id": oid})
    if not request or request["to_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Request not found")
    await friend_requests_collection().update_one({"_id": oid}, {"$set": {"status": "declined"}})
    return {"status": "declined"}


@router.post("/requests/{request_id}/cancel")
async def cancel_request(request_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(request_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request ID")
    request = await friend_requests_collection().find_one({"_id": oid})
    if not request or request["from_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Request not found")
    await friend_requests_collection().update_one({"_id": oid}, {"$set": {"status": "cancelled"}})
    return {"status": "cancelled"}


@router.delete("/{friend_id}")
async def remove_friend(friend_id: str, user=Depends(get_current_user)):
    me = user["id"]
    lo, hi = sorted([me, friend_id])
    result = await friends_collection().delete_one({"user_ids": [lo, hi]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Friend not found")
    await friend_requests_collection().update_many(
        {
            "$or": [
                {"from_id": me, "to_id": friend_id},
                {"from_id": friend_id, "to_id": me},
            ]
        },
        {"$set": {"status": "removed"}},
    )
    return {"removed": True}


@router.get("/suggestions")
async def suggestions(
    q: Optional[str] = Query(None, max_length=60),
    limit: int = Query(10, ge=1, le=20),
    user=Depends(get_current_user),
):
    """Suggest people to add — name search or a random sampling of users."""
    me = user["id"]
    query: dict = {}
    if q and q.strip():
        query["name"] = {"$regex": q.strip(), "$options": "i"}
    cursor = users_collection().find(query).limit(200)
    suggestions = []
    async for doc in cursor:
        uid_str = str(doc["_id"])
        if uid_str == me:
            continue
        if await _is_friend(me, uid_str):
            continue
        pending = await friend_requests_collection().find_one({
            "from_id": me, "to_id": uid_str, "status": "pending",
        })
        if pending:
            continue
        suggestions.append({
            "user_id": uid_str,
            "name": doc.get("name", "Anonymous"),
            "uid": doc.get("uid") or "",
        })
        if len(suggestions) >= limit:
            break
    return {"suggestions": suggestions}
