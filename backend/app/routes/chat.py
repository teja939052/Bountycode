"""Real-time chat — WebSocket fan-out with REST history fallback. ZERO AI.

Rooms:
  - global                      : everyone
  - guild:{guild_id}            : guild members only (defensive if `guilds` missing)
  - college:{college_name}      : users with a matching campus profile
  - dm:{friend_id}              : anyone can DM anyone

Messages persist to a single TTL-bounded collection (7 days). Live delivery
happens over WebSocket `/api/v1/chat/ws?token=...` with per-room fan-out; the
REST endpoints remain for history, rooms list and presence of emojis.
"""
import asyncio
import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from bson import ObjectId
from app.middleware.auth import get_current_user, get_current_user_ws
from app.database import (
    get_db,
    chat_messages_collection,
    campus_profiles_collection,
)

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

MAX_TEXT_LEN = 500
MAX_EMOJI_LEN = 32
MAX_MESSAGES = 100

REACTION_EMOJIS = ["🔥", "😂", "💯", "👍", "👏", "🎉", "🤯", "💀", "🐛", "🧠"]
CHAT_EMOJIS = ["😀", "😍", "😅", "🤝", "💪", "🚀", "🌟", "💡", "✅", "🙏", "🎯", "⚡"]


class ChatSendRequest(BaseModel):
    room_type: str
    room_id: Optional[str] = None
    text: str = ""
    emoji: str = ""


def _clean(value, max_len):
    return (value or "").strip()[:max_len]


def _serialize_message(doc) -> dict:
    created = doc.get("created_at")
    return {
        "id": str(doc.get("_id")),
        "user_id": doc.get("user_id"),
        "name": doc.get("name", "Anonymous"),
        "room_type": doc.get("room_type"),
        "room_id": doc.get("room_id"),
        "text": doc.get("text", ""),
        "emoji": doc.get("emoji", ""),
        "created_at": created.isoformat() if isinstance(created, datetime) else None,
    }


def _room_key(room_type: str, room_id: Optional[str]) -> str:
    return f"{room_type}:{room_id or ''}"


# ─── WebSocket presence / fan-out ────────────────────────────────────────

# room_key -> set of connected websockets (kept in memory only, no DB writes)
_room_connections: dict[str, set[WebSocket]] = {}


def _room_sockets(room_key: str) -> set[WebSocket]:
    return _room_connections.setdefault(room_key, set())


async def _broadcast(room_key: str, message: dict):
    """Fan a serialized message out to every socket in the room."""
    payload = json.dumps({"type": "message", "data": message})
    dead = []
    for ws in list(_room_sockets(room_key)):
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _room_sockets(room_key).discard(ws)


async def _guild_room_allowed(user, guild_id: str) -> bool:
    """Membership check for `guild:{id}` rooms. Defensive: if the guilds
    collection is missing or a lookup errors, allow through."""
    db = get_db()
    try:
        names = await db.list_collection_names()
    except Exception:
        return True
    if "guilds" not in names:
        return True
    try:
        guild = await db["guilds"].find_one({"_id": ObjectId(guild_id)})
    except Exception:
        return True
    if guild is None:
        return False
    return any(m.get("user_id") == user["id"] for m in guild.get("members", []))


async def _college_room_allowed(user, college_name: str) -> bool:
    """College room requires a matching campus profile. Defensive: if the
    campus_profiles collection is missing, allow through."""
    db = get_db()
    try:
        names = await db.list_collection_names()
    except Exception:
        return True
    if "campus_profiles" not in names:
        return True
    try:
        profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    except Exception:
        return True
    if not profile:
        return False
    mine = (profile.get("college") or "").lower()
    target = (college_name or "").lower()
    return bool(mine) and mine == target


async def _assert_room_access(user, room_type: str, room_id: Optional[str]):
    room_type = (room_type or "").lower().strip()
    if room_type == "global":
        return
    if room_type == "guild":
        if not room_id:
            raise HTTPException(status_code=400, detail="guild room requires room_id (guild id)")
        if not await _guild_room_allowed(user, room_id):
            raise HTTPException(status_code=403, detail="You are not a member of this guild")
        return
    if room_type == "college":
        if not room_id:
            raise HTTPException(status_code=400, detail="college room requires room_id (college name)")
        if not await _college_room_allowed(user, room_id):
            raise HTTPException(status_code=403, detail="Join this college first to chat")
        return
    if room_type == "dm":
        if not room_id:
            raise HTTPException(status_code=400, detail="dm room requires room_id (friend user id)")
        return
    raise HTTPException(status_code=400, detail=f"Unknown room type: {room_type}")


async def _persist_and_broadcast(user, room_type: str, room_id: Optional[str], text: str, emoji: str) -> dict:
    doc = {
        "user_id": user["id"],
        "name": user.get("name", "Anonymous"),
        "room_type": room_type,
        "room_id": room_id,
        "text": text,
        "emoji": emoji,
        "created_at": datetime.now(timezone.utc),
    }
    result = await chat_messages_collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    serialized = _serialize_message(doc)
    await _broadcast(_room_key(room_type, room_id), serialized)
    return serialized


@router.post("/send")
async def send_message(req: ChatSendRequest, user=Depends(get_current_user)):
    room_type = (req.room_type or "").lower().strip()
    room_id = _clean(req.room_id, 100)
    text = _clean(req.text, MAX_TEXT_LEN)
    emoji = _clean(req.emoji, MAX_EMOJI_LEN)

    if not room_type:
        raise HTTPException(status_code=400, detail="room_type is required")
    if not text and not emoji:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    await _assert_room_access(user, room_type, room_id)
    return await _persist_and_broadcast(user, room_type, room_id, text, emoji)


@router.websocket("/ws")
async def chat_websocket(
    websocket: WebSocket,
    room_type: str = Query("global"),
    room_id: Optional[str] = Query(None),
    token: Optional[str] = Query(None),
):
    """Live chat socket. Client joins `?room_type=&room_id=&token=` (token also
    accepted from the `pp_token` cookie). Broadcasts {type:'message',data:{...}}
    to everyone in the room. Client may send {type:'ping'} -> {type:'pong'}."""
    try:
        user = await get_current_user_ws(websocket, token)
    except HTTPException:
        await websocket.close(code=4401)
        return

    room_type = (room_type or "").lower().strip()
    room_id = _clean(room_id, 100)

    if not room_type or room_type not in {"global", "guild", "college", "dm"}:
        await websocket.close(code=4400)
        return

    try:
        await _assert_room_access(user, room_type, room_id)
    except HTTPException as e:
        await websocket.close(code=4403)
        return

    room_key = _room_key(room_type, room_id)
    await websocket.accept()

    # Announce presence (fire-and-forget so one failing socket can't kill others)
    presence = {
        "type": "presence",
        "data": {"user_id": user["id"], "name": user.get("name", "Anonymous"), "count": len(_room_sockets(room_key)) + 1},
    }
    for ws in list(_room_sockets(room_key)):
        try:
            await ws.send_text(json.dumps(presence))
        except Exception:
            pass

    _room_sockets(room_key).add(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                msg = {}
            mtype = msg.get("type")
            if mtype == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                continue
            if mtype == "send":
                text = _clean(msg.get("text", ""), MAX_TEXT_LEN)
                emoji = _clean(msg.get("emoji", ""), MAX_EMOJI_LEN)
                if not text and not emoji:
                    continue
                try:
                    await _persist_and_broadcast(user, room_type, room_id, text, emoji)
                except Exception:
                    pass
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        _room_sockets(room_key).discard(websocket)


@router.get("/messages")
async def get_messages(
    room_type: str = Query(..., description="Room type"),
    room_id: Optional[str] = Query(None, description="Room id"),
    limit: int = Query(50, ge=1, le=MAX_MESSAGES),
    after_id: Optional[str] = Query(None, description="Return only messages after this id"),
    user=Depends(get_current_user),
):
    room_type = (room_type or "").lower().strip()
    query = {"room_type": room_type, "room_id": room_id or ""}

    if after_id:
        try:
            query["_id"] = {"$gt": ObjectId(after_id)}
        except Exception:
            query["_id"] = {"$gt": ObjectId()}
        cursor = (
            chat_messages_collection()
            .find(query)
            .sort("_id", 1)
            .limit(limit)
        )
        docs = [doc async for doc in cursor]
    else:
        cursor = (
            chat_messages_collection()
            .find(query)
            .sort("_id", -1)
            .limit(limit)
        )
        docs = [doc async for doc in cursor]
        docs.reverse()

    return {"messages": [_serialize_message(d) for d in docs]}


@router.get("/recent")
async def recent_rooms(user=Depends(get_current_user)):
    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$sort": {"created_at": -1}},
        {
            "$group": {
                "_id": {"room_type": "$room_type", "room_id": "$room_id"},
                "last_message": {"$first": "$$ROOT"},
                "my_messages": {"$sum": 1},
            }
        },
        {"$sort": {"last_message.created_at": -1}},
        {"$limit": 50},
    ]
    rooms = []
    async for doc in chat_messages_collection().aggregate(pipeline):
        last = doc.get("last_message") or {}
        rooms.append(
            {
                "room_type": doc["_id"].get("room_type"),
                "room_id": doc["_id"].get("room_id"),
                "last_message": _serialize_message(last),
                "my_messages": doc.get("my_messages", 0),
            }
        )
    return {"rooms": rooms}


@router.get("/emotes")
async def emotes(user=Depends(get_current_user)):
    return {"reactions": REACTION_EMOJIS, "emojis": CHAT_EMOJIS}


class ReactionRequest(BaseModel):
    emoji: str


class ReadReceiptRequest(BaseModel):
    room_type: str
    room_id: Optional[str] = None


class TypingRequest(BaseModel):
    room_type: str
    room_id: Optional[str] = None


class CreateRoomRequest(BaseModel):
    room_type: str
    room_id: Optional[str] = None
    name: str = ""


class SearchRequest(BaseModel):
    room_type: str
    room_id: Optional[str] = None
    q: str = ""
    limit: int = 20


@router.post("/messages/{message_id}/reactions")
async def add_reaction(message_id: str, req: ReactionRequest, user=Depends(get_current_user)):
    emoji = _clean(req.emoji, MAX_EMOJI_LEN)
    if not emoji:
        raise HTTPException(status_code=400, detail="Emoji is required")

    msg = await chat_messages_collection().find_one({"_id": ObjectId(message_id)})
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    room_type = msg.get("room_type")
    room_id = msg.get("room_id")
    await _assert_room_access(user, room_type, room_id)

    reaction_key = f"reactions.{emoji}"
    await chat_messages_collection().update_one(
        {"_id": ObjectId(message_id)},
        {"$inc": {reaction_key: 1}, "$addToSet": {f"reaction_users.{emoji}": user["id"]}},
    )

    updated = await chat_messages_collection().find_one({"_id": ObjectId(message_id)})
    serialized = _serialize_message(updated)
    await _broadcast(_room_key(room_type, room_id), serialized)

    return {"message_id": message_id, "emoji": emoji, "status": "reacted"}


@router.post("/mark-read")
async def mark_read(req: ReadReceiptRequest, user=Depends(get_current_user)):
    room_type = (req.room_type or "").lower().strip()
    room_id = _clean(req.room_id, 100)

    await chat_messages_collection().update_many(
        {"room_type": room_type, "room_id": room_id, "user_id": {"$ne": user["id"]}, "read_by": {"$ne": user["id"]}},
        {"$addToSet": {"read_by": user["id"]}},
    )

    return {"room_type": room_type, "room_id": room_id, "marked_read": True}


@router.post("/typing")
async def send_typing(req: TypingRequest, user=Depends(get_current_user)):
    room_type = (req.room_type or "").lower().strip()
    room_id = _clean(req.room_id, 100)

    await _assert_room_access(user, room_type, room_id)

    typing_payload = {
        "type": "typing",
        "data": {"user_id": user["id"], "name": user.get("name", "Anonymous"), "room_type": room_type, "room_id": room_id},
    }
    await _broadcast(_room_key(room_type, room_id), typing_payload)

    return {"typing": True}


@router.get("/search")
async def search_messages(
    room_type: str = Query(..., description="Room type"),
    room_id: Optional[str] = Query(None, description="Room id"),
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    room_type = (room_type or "").lower().strip()
    query = {"room_type": room_type, "room_id": room_id or "", "text": {"$regex": q, "$options": "i"}}

    cursor = chat_messages_collection().find(query).sort("_id", -1).limit(limit)
    docs = [doc async for doc in cursor]

    return {"query": q, "results": [_serialize_message(d) for d in docs]}


@router.get("/unread")
async def unread_count(user=Depends(get_current_user)):
    pipeline = [
        {"$match": {"user_id": {"$ne": user["id"]}}},
        {"$group": {"_id": {"room_type": "$room_type", "room_id": "$room_id"}, "unread": {"$sum": 1}}},
        {"$sort": {"unread": -1}},
        {"$limit": 20},
    ]
    results = []
    async for doc in chat_messages_collection().aggregate(pipeline):
        key = doc["_id"]
        results.append({
            "room_type": key.get("room_type"),
            "room_id": key.get("room_id"),
            "unread_count": doc.get("unread", 0),
        })

    return {"unread_rooms": results, "total_unread": sum(r["unread_count"] for r in results)}


@router.post("/rooms")
async def create_room(req: CreateRoomRequest, user=Depends(get_current_user)):
    room_type = (req.room_type or "").lower().strip()
    room_id = _clean(req.room_id, 100)
    name = _clean(req.name, 100)

    if room_type not in {"global", "guild", "college", "dm"}:
        raise HTTPException(status_code=400, detail=f"Invalid room type: {room_type}")

    if room_type in ("guild", "college", "dm") and not room_id:
        raise HTTPException(status_code=400, detail=f"{room_type} room requires room_id")

    await _assert_room_access(user, room_type, room_id)

    return {
        "room_type": room_type,
        "room_id": room_id,
        "name": name or f"{room_type}:{room_id}",
        "created_by": user["id"],
        "created_at": datetime.now(timezone.utc),
    }


@router.post("/rooms/leave")
async def leave_room(req: ReadReceiptRequest, user=Depends(get_current_user)):
    room_type = (req.room_type or "").lower().strip()
    room_id = _clean(req.room_id, 100)

    if room_type == "global":
        raise HTTPException(status_code=400, detail="Cannot leave the global room")

    await _assert_room_access(user, room_type, room_id)

    return {"room_type": room_type, "room_id": room_id, "left": True}


@router.get("/rooms/{room_type}/{room_id}/members")
async def room_members(room_type: str, room_id: str, user=Depends(get_current_user)):
    room_type = (room_type or "").lower().strip()
    room_id = _clean(room_id, 100)

    await _assert_room_access(user, room_type, room_id)

    pipeline = [
        {"$match": {"room_type": room_type, "room_id": room_id}},
        {"$group": {"_id": "$user_id", "name": {"$first": "$name"}, "message_count": {"$sum": 1}, "last_seen": {"$max": "$created_at"}}},
        {"$sort": {"message_count": -1}},
        {"$limit": 50},
    ]
    members = []
    async for doc in chat_messages_collection().aggregate(pipeline):
        members.append({
            "user_id": doc["_id"],
            "name": doc.get("name", "Anonymous"),
            "message_count": doc.get("message_count", 0),
            "last_seen": doc.get("last_seen"),
        })

    return {"room_type": room_type, "room_id": room_id, "members": members, "total_members": len(members)}


@router.get("/stats")
async def message_stats(
    room_type: str = Query(..., description="Room type"),
    room_id: Optional[str] = Query(None, description="Room id"),
    user=Depends(get_current_user),
):
    room_type = (room_type or "").lower().strip()
    query = {"room_type": room_type, "room_id": room_id or ""}

    total = await chat_messages_collection().count_documents(query)

    pipeline = [
        {"$match": query},
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    top_senders = []
    async for doc in chat_messages_collection().aggregate(pipeline):
        top_senders.append({"user_id": doc["_id"], "message_count": doc["count"]})

    oldest = await chat_messages_collection().find_one(query, sort=[("created_at", 1)])
    newest = await chat_messages_collection().find_one(query, sort=[("created_at", -1)])

    return {
        "room_type": room_type,
        "room_id": room_id,
        "total_messages": total,
        "top_senders": top_senders,
        "first_message": _serialize_message(oldest) if oldest else None,
        "last_message": _serialize_message(newest) if newest else None,
    }
