"""GD Practice Rooms — scheduled group-discussion rooms (4-6 students) with a
topic, a shared countdown timer, an in-room chat, and peer rubric ratings
(clarity / listening / initiative). WebSocket fan-out for presence, speaking and
timer; REST for lifecycle and ratings. ZERO AI — fully deterministic.
"""
import asyncio
import json
import random
import string
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from bson import ObjectId
from app.middleware.auth import get_current_user, get_current_user_ws
from app.database import gd_rooms_collection, gd_ratings_collection, users_collection

router = APIRouter(prefix="/api/v1/gd", tags=["GD Rooms"])

MAX_PARTICIPANTS = 6
MIN_PARTICIPANTS = 4
MAX_DURATION_MIN = 60
DEFAULT_DURATION_MIN = 15
MAX_MESSAGES = 100

GD_TOPICS = [
    "Should AI be allowed in college exams?",
    "Remote work vs office work for freshers",
    "Is coding the new literacy?",
    "Impact of social media on student focus",
    "Startup vs placement: which first?",
    "Should college placement drives be open to all years?",
    "Is memorization overrated in modern education?",
    "Gen AI: job killer or job creator?",
    "Is the 10th/12th board percentage still relevant?",
    "Online classes vs offline classes",
    "Should internships be mandatory for graduation?",
    "Is competition healthy among students?",
    "Impact of gaming on academics",
    "Are group studies more effective than solo study?",
    "Should students pay for premium placement prep?",
    "Is a gap year a bad idea?",
    "Freelancing vs full-time employment for graduates",
    "Are soft skills more important than hard skills?",
    "Should colleges teach entrepreneurship?",
    "Does tier of college matter for career success?",
    "Is it fair to compare students by CGPA?",
    "Should coding bootcamps replace traditional degrees?",
    "Is work-life balance realistic for freshers?",
    "Does the pressure of placements harm mental health?",
]

RUBRIC_KEYS = ["clarity", "listening", "initiative"]
RUBRIC_LABELS = {
    "clarity": "Clarity of communication",
    "listening": "Listening & responding to others",
    "initiative": "Taking initiative / speaking up",
}

_TIMER_TASKS: dict[str, asyncio.Task] = {}


class CreateGDRoomRequest(BaseModel):
    topic: str = ""
    duration_minutes: int = DEFAULT_DURATION_MIN
    max_participants: int = MAX_PARTICIPANTS


class RatePeerRequest(BaseModel):
    target_user_id: str
    clarity: int = Field(3, ge=1, le=5)
    listening: int = Field(3, ge=1, le=5)
    initiative: int = Field(3, ge=1, le=5)
    comment: str = ""


# ─── Helpers ─────────────────────────────────────────────────────────────

def _now():
    return datetime.now(timezone.utc)


def _clean(value, max_len):
    return (value or "").strip()[:max_len]


def _gen_join_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


def _serialize_message(m: dict) -> dict:
    created = m.get("created_at")
    return {
        "user_id": m.get("user_id"),
        "name": m.get("name", "Anonymous"),
        "text": m.get("text", ""),
        "created_at": created.isoformat() if isinstance(created, datetime) else None,
    }


def _serialize_room(doc) -> dict:
    return {
        "room_id": str(doc["_id"]),
        "topic": doc.get("topic", ""),
        "host_id": doc.get("host_id"),
        "status": doc.get("status", "open"),
        "duration_minutes": doc.get("duration_minutes", DEFAULT_DURATION_MIN),
        "max_participants": doc.get("max_participants", MAX_PARTICIPANTS),
        "join_code": doc.get("join_code"),
        "participants": doc.get("participants", []),
        "participant_count": len(doc.get("participants", [])),
        "messages": [_serialize_message(m) for m in (doc.get("messages") or [])],
        "created_at": doc.get("created_at"),
        "started_at": doc.get("started_at"),
        "ended_at": doc.get("ended_at"),
        "timer_end_at": doc.get("timer_end_at"),
    }


def _room_key(room_id: str) -> str:
    return f"gd:{room_id}"


def _participant_ids(doc) -> set:
    return {p.get("user_id") for p in doc.get("participants", [])}


def _in_room(doc, user_id: str) -> bool:
    return user_id in _participant_ids(doc)


# ─── WebSocket fan-out ────────────────────────────────────────────────────

_room_connections: dict[str, set[WebSocket]] = {}
_speaking: dict[str, dict[str, bool]] = {}


def _room_sockets(room_key: str) -> set[WebSocket]:
    return _room_connections.setdefault(room_key, set())


async def _broadcast(room_key: str, message: dict, exclude: Optional[WebSocket] = None):
    payload = json.dumps(message)
    dead = []
    for ws in list(_room_sockets(room_key)):
        if ws == exclude:
            continue
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _room_sockets(room_key).discard(ws)
    if not _room_sockets(room_key):
        _room_connections.pop(room_key, None)


async def _cancel_timer(room_id: str):
    task = _TIMER_TASKS.pop(room_id, None)
    if task and not task.done():
        task.cancel()


async def _schedule_timer_done(room_id: str, end_at: datetime):
    delay = (end_at - _now()).total_seconds()
    if delay <= 0:
        return
    await asyncio.sleep(delay)
    await _broadcast(_room_key(room_id), {"type": "timer_done", "data": {"room_id": room_id}})


# ─── Routes ───────────────────────────────────────────────────────────────

@router.get("/topics")
async def gd_topics(user=Depends(get_current_user)):
    return {"topics": GD_TOPICS}


@router.post("/rooms")
async def create_gd_room(req: CreateGDRoomRequest, user=Depends(get_current_user)):
    topic = _clean(req.topic, 200)
    if not topic:
        topic = random.choice(GD_TOPICS)
    duration = max(1, min(MAX_DURATION_MIN, req.duration_minutes))
    max_p = max(MIN_PARTICIPANTS, min(MAX_PARTICIPANTS, req.max_participants))

    join_code = _gen_join_code()
    while await gd_rooms_collection().find_one({"join_code": join_code}):
        join_code = _gen_join_code()

    doc = {
        "topic": topic,
        "host_id": user["id"],
        "status": "open",
        "duration_minutes": duration,
        "max_participants": max_p,
        "join_code": join_code,
        "participants": [{"user_id": user["id"], "name": user.get("name", "Anonymous"), "joined_at": _now()}],
        "messages": [],
        "created_at": _now(),
        "started_at": None,
        "ended_at": None,
        "timer_end_at": None,
    }
    result = await gd_rooms_collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize_room(doc)


@router.get("/rooms")
async def list_gd_rooms(status: Optional[str] = Query(None, pattern="^(open|ongoing|completed)$"), user=Depends(get_current_user)):
    query = {}
    if status:
        query["status"] = status
    else:
        query["status"] = {"$in": ["open", "ongoing"]}
    cursor = gd_rooms_collection().find(query).sort("created_at", -1).limit(50)
    rooms = [_serialize_room(doc) async for doc in cursor]
    return {"rooms": rooms, "total": len(rooms)}


@router.get("/rooms/{room_id}")
async def get_gd_room(room_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")
    return _serialize_room(doc)


@router.post("/rooms/join-by-code")
async def join_by_code(join_code: str = Query(..., min_length=6, max_length=6), user=Depends(get_current_user)):
    doc = await gd_rooms_collection().find_one({"join_code": join_code.upper()})
    if not doc:
        raise HTTPException(status_code=404, detail="No room found with that code")
    room_id = str(doc["_id"])
    if doc["status"] != "open":
        raise HTTPException(status_code=400, detail="Room is no longer open")
    if _in_room(doc, user["id"]):
        return _serialize_room(doc)
    if doc["status"] == "open" and len(doc["participants"]) >= doc["max_participants"]:
        raise HTTPException(status_code=400, detail="Room is full")
    await gd_rooms_collection().update_one(
        {"_id": doc["_id"]},
        {"$push": {"participants": {"user_id": user["id"], "name": user.get("name", "Anonymous"), "joined_at": _now()}}},
    )
    updated = await gd_rooms_collection().find_one({"_id": doc["_id"]})
    return _serialize_room(updated)


@router.post("/rooms/{room_id}/join")
async def join_gd_room(room_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")
    if doc["status"] != "open":
        raise HTTPException(status_code=400, detail="Room is no longer open")
    if _in_room(doc, user["id"]):
        return _serialize_room(doc)
    if len(doc["participants"]) >= doc["max_participants"]:
        raise HTTPException(status_code=400, detail="Room is full")
    await gd_rooms_collection().update_one(
        {"_id": oid},
        {"$push": {"participants": {"user_id": user["id"], "name": user.get("name", "Anonymous"), "joined_at": _now()}}},
    )
    updated = await gd_rooms_collection().find_one({"_id": oid})
    return _serialize_room(updated)


@router.post("/rooms/{room_id}/leave")
async def leave_gd_room(room_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")
    if not _in_room(doc, user["id"]):
        return {"room_id": room_id, "left": True}
    await gd_rooms_collection().update_one(
        {"_id": oid},
        {"$pull": {"participants": {"user_id": user["id"]}}},
    )
    return {"room_id": room_id, "left": True}


@router.post("/rooms/{room_id}/start")
async def start_gd_room(room_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")
    if doc["host_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only the host can start the session")
    if doc["status"] != "open":
        raise HTTPException(status_code=400, detail="Session already started or ended")
    if len(doc["participants"]) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 participants to start")
    await gd_rooms_collection().update_one(
        {"_id": oid},
        {"$set": {"status": "ongoing", "started_at": _now()}},
    )
    updated = await gd_rooms_collection().find_one({"_id": oid})
    await _broadcast(_room_key(room_id), {
        "type": "session_start",
        "data": {"room_id": room_id, "status": "ongoing"},
    })
    return _serialize_room(updated)


@router.post("/rooms/{room_id}/end")
async def end_gd_room(room_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")
    if doc["host_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only the host can end the session")
    if doc["status"] == "completed":
        return _serialize_room(doc)
    await _cancel_timer(room_id)
    await gd_rooms_collection().update_one(
        {"_id": oid},
        {"$set": {"status": "completed", "ended_at": _now(), "timer_end_at": None}},
    )
    updated = await gd_rooms_collection().find_one({"_id": oid})
    await _broadcast(_room_key(room_id), {
        "type": "session_end",
        "data": {"room_id": room_id, "status": "completed"},
    })
    return _serialize_room(updated)


@router.post("/rooms/{room_id}/timer")
async def set_room_timer(room_id: str, seconds: int = Query(60, ge=15, le=3600), user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")
    if doc["host_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only the host can set the timer")
    if doc["status"] != "ongoing":
        raise HTTPException(status_code=400, detail="Session is not running")

    await _cancel_timer(room_id)
    end_at = _now() + timedelta(seconds=seconds)
    await gd_rooms_collection().update_one({"_id": oid}, {"$set": {"timer_end_at": end_at}})
    task = asyncio.create_task(_schedule_timer_done(room_id, end_at))
    _TIMER_TASKS[room_id] = task
    await _broadcast(_room_key(room_id), {
        "type": "timer",
        "data": {"room_id": room_id, "end_at": end_at.isoformat(), "duration_seconds": seconds},
    })
    return {"room_id": room_id, "end_at": end_at.isoformat(), "duration_seconds": seconds}


@router.post("/rooms/{room_id}/rate")
async def rate_peer(room_id: str, req: RatePeerRequest, user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")

    if req.target_user_id == user["id"]:
        raise HTTPException(status_code=400, detail="You cannot rate yourself")
    if not _in_room(doc, req.target_user_id):
        raise HTTPException(status_code=400, detail="Target is not a participant")

    ratings = {
        "clarity": max(1, min(5, req.clarity)),
        "listening": max(1, min(5, req.listening)),
        "initiative": max(1, min(5, req.initiative)),
    }
    comment = _clean(req.comment, 500)

    await gd_ratings_collection().update_one(
        {"room_id": room_id, "rater_id": user["id"], "target_id": req.target_user_id},
        {"$set": {**ratings, "comment": comment, "rated_at": _now()}},
        upsert=True,
    )
    return {"room_id": room_id, "target_user_id": req.target_user_id, **ratings, "rated": True}


@router.get("/rooms/{room_id}/feedback")
async def my_feedback(room_id: str, user=Depends(get_current_user)):
    docs = [
        doc async for doc in gd_ratings_collection().find({"room_id": room_id, "target_id": user["id"]})
    ]
    return _aggregate_ratings(docs)


@router.get("/rooms/{room_id}/scores")
async def room_scores(room_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid room ID")
    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Room not found")
    if not _in_room(doc, user["id"]):
        raise HTTPException(status_code=403, detail="Join the room to view scores")

    results = []
    for p in doc.get("participants", []):
        pid = p["user_id"]
        rating_docs = [
            r async for r in gd_ratings_collection().find({"room_id": room_id, "target_id": pid})
        ]
        agg = _aggregate_ratings(rating_docs)
        results.append({
            "user_id": pid,
            "name": p.get("name", "Anonymous"),
            "ratings_count": agg["ratings_count"],
            "averages": agg["averages"],
            "overall": agg["overall"],
        })
    results.sort(key=lambda r: r["overall"], reverse=True)
    return {"room_id": room_id, "scores": results}


def _aggregate_ratings(docs) -> dict:
    if not docs:
        return {
            "ratings_count": 0,
            "averages": {k: None for k in RUBRIC_KEYS},
            "overall": None,
            "comments": [],
        }
    totals = {k: 0 for k in RUBRIC_KEYS}
    comments = []
    for d in docs:
        for k in RUBRIC_KEYS:
            totals[k] += d.get(k, 0)
        if d.get("comment"):
            comments.append({"rater_id": d.get("rater_id"), "comment": d["comment"]})
    n = len(docs)
    averages = {k: round(totals[k] / n, 1) for k in RUBRIC_KEYS}
    overall = round(sum(averages.values()) / len(RUBRIC_KEYS), 1)
    return {"ratings_count": n, "averages": averages, "overall": overall, "comments": comments}


@router.get("/rooms/{room_id}/rubric")
async def rubric(room_id: str, user=Depends(get_current_user)):
    return {"rubric": RUBRIC_KEYS, "labels": RUBRIC_LABELS, "scale": "1-5"}


# ─── WebSocket room socket ───────────────────────────────────────────────

@router.websocket("/rooms/{room_id}/ws")
async def gd_room_websocket(
    websocket: WebSocket,
    room_id: str,
    token: Optional[str] = Query(None),
):
    try:
        user = await get_current_user_ws(websocket, token)
    except HTTPException:
        await websocket.close(code=4401)
        return

    try:
        oid = ObjectId(room_id)
    except Exception:
        await websocket.close(code=4400)
        return

    doc = await gd_rooms_collection().find_one({"_id": oid})
    if not doc:
        await websocket.close(code=4404)
        return
    if not _in_room(doc, user["id"]):
        await websocket.close(code=4403)
        return

    await websocket.accept()
    room_key = _room_key(room_id)
    uid = user["id"]

    # Fresh snapshot on join (reconnect-friendly)
    speaking_snapshot = {uid_: bool(sp) for uid_, sp in _speaking.get(room_key, {}).items()}
    await websocket.send_text(json.dumps({
        "type": "sync",
        "data": {
            "room_id": room_id,
            "status": doc["status"],
            "topic": doc.get("topic", ""),
            "host_id": doc.get("host_id"),
            "participants": doc.get("participants", []),
            "timer_end_at": doc.get("timer_end_at"),
            "speaking": speaking_snapshot,
            "messages": [_serialize_message(m) for m in (doc.get("messages") or [])],
        },
    }))

    presence = {
        "type": "presence",
        "data": {"user_id": uid, "name": user.get("name", "Anonymous"), "count": len(_room_sockets(room_key)) + 1},
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
            if mtype == "speak":
                speaking = bool(msg.get("speaking"))
                _speaking.setdefault(room_key, {})[uid] = speaking
                await _broadcast(room_key, {
                    "type": "speak",
                    "data": {"user_id": uid, "name": user.get("name", "Anonymous"), "speaking": speaking},
                }, exclude=websocket)
                continue
            if mtype == "message":
                text = _clean(msg.get("text", ""), 500)
                if not text:
                    continue
                msg_doc = {"user_id": uid, "name": user.get("name", "Anonymous"), "text": text, "created_at": _now()}
                await gd_rooms_collection().update_one(
                    {"_id": oid},
                    {"$push": {"messages": {"$each": [msg_doc], "$position": 0, "$slice": MAX_MESSAGES}}},
                )
                await _broadcast(room_key, {"type": "message", "data": _serialize_message(msg_doc)})
                continue
            if mtype == "start_timer":
                if doc["host_id"] != uid:
                    await websocket.send_text(json.dumps({"type": "error", "data": {"error": "Only the host can set the timer"}}))
                    continue
                try:
                    seconds = max(15, min(3600, int(msg.get("seconds") or 60)))
                except (TypeError, ValueError):
                    continue
                end_at = _now() + timedelta(seconds=seconds)
                await gd_rooms_collection().update_one({"_id": oid}, {"$set": {"timer_end_at": end_at}})
                await _cancel_timer(room_id)
                _TIMER_TASKS[room_id] = asyncio.create_task(_schedule_timer_done(room_id, end_at))
                await _broadcast(room_key, {
                    "type": "timer",
                    "data": {"room_id": room_id, "end_at": end_at.isoformat(), "duration_seconds": seconds},
                })
                continue
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        _room_sockets(room_key).discard(websocket)
        if not _room_sockets(room_key):
            _room_connections.pop(room_key, None)
        if uid in _speaking.get(room_key, {}):
            _speaking[room_key][uid] = False
        await _broadcast(room_key, {
            "type": "presence",
            "data": {"user_id": uid, "name": user.get("name", "Anonymous"), "count": len(_room_sockets(room_key))},
        }, exclude=websocket)
