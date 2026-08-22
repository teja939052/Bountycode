"""Study Squad Matching — deterministic peer matching for study groups.

Each user stores a lightweight "squad profile" (goals, topics, languages,
availability). The matcher scores every other profiled user by tag overlap +
availability compatibility and returns a deterministic, sorted shortlist
(no AI, no randomness). Invites build persistent squads with a message board.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import study_squads_collection
from app.services.sanitizer import sanitize_text

router = APIRouter(prefix="/api/v1/study-squads", tags=["Study Squads"])

GOALS = ["dsa", "system-design", "aptitude", "mock-interview", "behavioral", "coding", "resume", "hr-round"]
TOPICS = ["arrays", "graphs", "dp", "trees", "sorting", "searching", "sql", "oop", "dbms", "os", "networks", "math"]
LANGUAGES = ["python", "java", "cpp", "javascript", "go", "rust", "typescript"]
AVAILABILITIES = ["morning", "evening", "night", "weekend", "flexible"]


class SquadProfileRequest(BaseModel):
    goals: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    availability: str = Field("flexible", max_length=30)
    bio: str = Field("", max_length=300)


class InviteRequest(BaseModel):
    user_id: str = Field(..., min_length=1)


class MessageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


def _pick_valid(values, allowed):
    return [v for v in (values or []) if v in allowed][:10]


def _serialize_profile(doc) -> dict:
    return {
        "user_id": doc.get("user_id"),
        "user_name": doc.get("user_name", "Anonymous"),
        "goals": doc.get("goals", []),
        "topics": doc.get("topics", []),
        "languages": doc.get("languages", []),
        "availability": doc.get("availability", "flexible"),
        "bio": doc.get("bio", ""),
        "updated_at": doc.get("updated_at"),
    }


def _compat(a: dict, b: dict) -> dict:
    goals = len(set(a.get("goals", [])) & set(b.get("goals", [])))
    topics = len(set(a.get("topics", [])) & set(b.get("topics", [])))
    langs = len(set(a.get("languages", [])) & set(b.get("languages", [])))
    avail = 1 if a.get("availability") and a.get("availability") == b.get("availability") else 0
    score = goals * 3 + topics * 2 + langs * 2 + avail * 5
    return {
        "score": score,
        "goals_overlap": goals,
        "topics_overlap": topics,
        "languages_overlap": langs,
        "availability_match": bool(avail),
    }


def _serialize_squad(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "member_names": doc.get("member_names", []),
        "member_ids": doc.get("member_ids", []),
        "created_at": doc.get("created_at"),
    }


def _serialize_message(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "squad_id": doc.get("squad_id"),
        "user_id": doc.get("user_id"),
        "user_name": doc.get("user_name", "Anonymous"),
        "text": doc.get("text", ""),
        "created_at": doc.get("created_at"),
    }


# ─── Profile ──────────────────────────────────────────────────────────────

@router.get("/goals")
async def available_goals():
    return {"goals": GOALS, "topics": TOPICS, "languages": LANGUAGES, "availabilities": AVAILABILITIES}


@router.post("/profile")
async def upsert_profile(req: SquadProfileRequest, user=Depends(get_current_user)):
    doc = {
        "kind": "profile",
        "user_id": user["id"],
        "user_name": user.get("name", "Anonymous"),
        "goals": _pick_valid(req.goals, GOALS),
        "topics": _pick_valid(req.topics, TOPICS),
        "languages": _pick_valid(req.languages, LANGUAGES),
        "availability": req.availability if req.availability in AVAILABILITIES else "flexible",
        "bio": sanitize_text(req.bio.strip(), max_length=300),
        "updated_at": datetime.now(timezone.utc),
    }
    await study_squads_collection().update_one(
        {"kind": "profile", "user_id": user["id"]},
        {"$set": doc},
        upsert=True,
    )
    return _serialize_profile(doc)


@router.get("/me")
async def my_profile(user=Depends(get_current_user)):
    doc = await study_squads_collection().find_one({"kind": "profile", "user_id": user["id"]})
    return _serialize_profile(doc) if doc else None


# ─── Matching ─────────────────────────────────────────────────────────────

@router.get("/match")
async def match_squads(limit: int = 5, user=Depends(get_current_user)):
    mine = await study_squads_collection().find_one({"kind": "profile", "user_id": user["id"]})
    if not mine:
        return {"matches": [], "needs_profile": True}

    limit = max(1, min(limit, 10))
    matches = []
    cursor = study_squads_collection().find({
        "kind": "profile",
        "user_id": {"$ne": user["id"]},
    })
    async for other in cursor:
        compat = _compat(mine, other)
        if compat["score"] <= 0:
            continue
        profile = _serialize_profile(other)
        profile["compat"] = compat
        matches.append(profile)

    matches.sort(key=lambda m: (-m["compat"]["score"], m["user_id"]))
    return {"matches": matches[:limit], "needs_profile": False}


# ─── Invites & Squads ─────────────────────────────────────────────────────

@router.post("/invite")
async def send_invite(req: InviteRequest, user=Depends(get_current_user)):
    if req.user_id == user["id"]:
        raise HTTPException(status_code=400, detail="You cannot invite yourself")
    target = await study_squads_collection().find_one({"kind": "profile", "user_id": req.user_id})
    if not target:
        raise HTTPException(status_code=404, detail="That user has no squad profile yet")

    existing = await study_squads_collection().find_one({
        "kind": "invite", "from_id": user["id"], "to_id": req.user_id, "status": "pending",
    })
    if existing:
        raise HTTPException(status_code=400, detail="Invite already pending")

    doc = {
        "kind": "invite",
        "from_id": user["id"],
        "from_name": user.get("name", "Anonymous"),
        "to_id": req.user_id,
        "to_name": target.get("user_name", "Anonymous"),
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
    }
    result = await study_squads_collection().insert_one(doc)
    return {"id": str(result.inserted_id), "status": "pending"}


@router.get("/invites")
async def list_invites(user=Depends(get_current_user)):
    received, sent = [], []
    cursor = study_squads_collection().find({"kind": "invite"}).sort("created_at", -1).limit(50)
    async for d in cursor:
        item = {
            "id": str(d["_id"]),
            "from_id": d.get("from_id"),
            "from_name": d.get("from_name", "Anonymous"),
            "to_id": d.get("to_id"),
            "to_name": d.get("to_name", "Anonymous"),
            "status": d.get("status"),
            "created_at": d.get("created_at"),
        }
        if d["from_id"] == user["id"]:
            sent.append(item)
        elif d["to_id"] == user["id"]:
            received.append(item)
    return {"received": received, "sent": sent}


@router.post("/invites/{invite_id}/accept")
async def accept_invite(invite_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(invite_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid invite ID")
    invite = await study_squads_collection().find_one({"_id": oid, "kind": "invite"})
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    if invite["to_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not addressed to you")

    await study_squads_collection().update_one(
        {"_id": oid}, {"$set": {"status": "accepted"}},
    )
    names = [invite["from_name"], user.get("name", "Anonymous")]
    ids = [invite["from_id"], user["id"]]
    squad = {
        "kind": "squad",
        "name": f"{names[0]} × {names[1]}",
        "member_ids": ids,
        "member_names": names,
        "created_at": datetime.now(timezone.utc),
    }
    result = await study_squads_collection().insert_one(squad)
    return {"squad_id": str(result.inserted_id), "status": "accepted"}


@router.post("/invites/{invite_id}/decline")
async def decline_invite(invite_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(invite_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid invite ID")
    invite = await study_squads_collection().find_one({"_id": oid, "kind": "invite"})
    if not invite or invite["to_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Invite not found")
    await study_squads_collection().update_one({"_id": oid}, {"$set": {"status": "declined"}})
    return {"status": "declined"}


@router.get("/squads")
async def my_squads(user=Depends(get_current_user)):
    cursor = study_squads_collection().find({"kind": "squad", "member_ids": user["id"]}).sort("created_at", -1).limit(50)
    return {"squads": [_serialize_squad(d) async for d in cursor]}


@router.post("/{squad_id}/message")
async def post_message(squad_id: str, req: MessageRequest, user=Depends(get_current_user)):
    try:
        oid = ObjectId(squad_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid squad ID")
    squad = await study_squads_collection().find_one({"_id": oid, "kind": "squad"})
    if not squad or user["id"] not in squad.get("member_ids", []):
        raise HTTPException(status_code=404, detail="Squad not found")
    doc = {
        "kind": "message",
        "squad_id": squad_id,
        "user_id": user["id"],
        "user_name": user.get("name", "Anonymous"),
        "text": sanitize_text(req.text.strip(), max_length=500),
        "created_at": datetime.now(timezone.utc),
    }
    result = await study_squads_collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize_message(doc)


@router.get("/{squad_id}/messages")
async def squad_messages(squad_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(squad_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid squad ID")
    squad = await study_squads_collection().find_one({"_id": oid, "kind": "squad"})
    if not squad or user["id"] not in squad.get("member_ids", []):
        raise HTTPException(status_code=404, detail="Squad not found")
    cursor = study_squads_collection().find({"kind": "message", "squad_id": squad_id}).sort("created_at", -1).limit(100)
    messages = [_serialize_message(d) async for d in cursor]
    return {"squad_id": squad_id, "messages": messages[::-1]}
