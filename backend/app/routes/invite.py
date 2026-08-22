"""Unified Invite System — consolidates study squad invites, campus connect
duel invites, and friend requests under a single API with a `kind` discriminator.

Endpoints:
  POST   /api/v1/invite/generate     — create an invite (kind: friend|study_squad|campus_connect)
  GET    /api/v1/invite/inbox        — received invites
  GET    /api/v1/invite/outbox       — sent invites
  POST   /api/v1/invite/{invite_id}/accept  — accept invite
  POST   /api/v1/invite/{invite_id}/decline  — decline invite
"""
from datetime import datetime, timezone
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import get_db


router = APIRouter(prefix="/api/v1/invite", tags=["Invite"])


# ─── Request models ────────────────────────────────────────────────────────

class GenerateInviteReq(BaseModel):
    kind: Literal["friend", "study_squad", "campus_connect"]
    target_user_id: Optional[str] = Field(None, description="Target user ID (friend/study_squad)")
    college: Optional[str] = Field(None, description="College name (campus_connect)")


class AcceptDeclineReq(BaseModel):
    invite_id: str = Field(..., description="Invite ObjectId string")


class InboxItem(BaseModel):
    id: str
    kind: str
    from_id: str
    from_name: str
    to_id: str
    to_name: str
    status: str
    created_at: datetime
    extra: dict = {}


# ─── Helpers ────────────────────────────────────────────────────────────────

def _now():
    return datetime.now(timezone.utc)


def _to_objectid(s: str) -> ObjectId:
    try:
        return ObjectId(s)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid invite ID format")


# ─── POST /api/v1/invite/generate ──────────────────────────────────────────

@router.post("/generate", summary="Generate a unified invite")
async def generate_invite(req: GenerateInviteReq, user=Depends(get_current_user)):
    kind = req.kind

    if kind == "friend":
        if not req.target_user_id:
            raise HTTPException(status_code=400, detail="target_user_id is required for friend invites")
        if req.target_user_id == user["id"]:
            raise HTTPException(status_code=400, detail="You cannot invite yourself")

        # Check if already friends or pending
        existing_friend = await get_db()["friends_collection"].find_one(
            {"$or": [{"user_ids": [user["id"], req.target_user_id]}, {"user_ids": [req.target_user_id, user["id"]]}] }
        )
        if existing_friend:
            raise HTTPException(status_code=400, detail="Already friends or a pending request exists")

        # Check for existing pending invite either direction
        existing = await get_db()["invite_requests"].find_one({
            "kind": "friend",
            "$or": [
                {"from_id": user["id"], "to_id": req.target_user_id, "status": "pending"},
                {"from_id": req.target_user_id, "to_id": user["id"], "status": "pending"},
            ],
        })
        if existing:
            raise HTTPException(status_code=400, detail="Invite already pending")

        doc = {
            "kind": "friend",
            "from_id": user["id"],
            "from_name": user.get("name", "Anonymous"),
            "to_id": req.target_user_id,
            "to_name": "",
            "status": "pending",
            "created_at": _now(),
            "extra": {},
        }
        result = await get_db()["invite_requests"].insert_one(doc)
        return {"id": str(result.inserted_id), "status": "pending", "kind": "friend"}

    if kind == "study_squad":
        if not req.target_user_id:
            raise HTTPException(status_code=400, detail="target_user_id is required for study_squad invites")
        if req.target_user_id == user["id"]:
            raise HTTPException(status_code=400, detail="You cannot invite yourself")

        # Check target has a profile
        target_profile = await get_db()["study_squads_collection"].find_one({"kind": "profile", "user_id": req.target_user_id})
        if not target_profile:
            raise HTTPException(status_code=404, detail="Target user has no squad profile yet")

        # Check for existing pending invite
        existing = await get_db()["invite_requests"].find_one({
            "kind": "study_squad",
            "$or": [
                {"from_id": user["id"], "to_id": req.target_user_id, "status": "pending"},
                {"from_id": req.target_user_id, "to_id": user["id"], "status": "pending"},
            ],
        })
        if existing:
            raise HTTPException(status_code=400, detail="Invite already pending")

        doc = {
            "kind": "study_squad",
            "from_id": user["id"],
            "from_name": user.get("name", "Anonymous"),
            "to_id": req.target_user_id,
            "to_name": target_profile.get("user_name", "Anonymous"),
            "status": "pending",
            "created_at": _now(),
            "extra": {"target_goals": target_profile.get("goals", [])},
        }
        result = await get_db()["invite_requests"].insert_one(doc)
        return {"id": str(result.inserted_id), "status": "pending", "kind": "study_squad"}

    if kind == "campus_connect":
        if not req.college:
            raise HTTPException(status_code=400, detail="college is required for campus_connect invites")
        if not req.target_user_id:
            raise HTTPException(status_code=400, detail="target_user_id is required for campus_connect invites")
        if req.target_user_id == user["id"]:
            raise HTTPException(status_code=400, detail="You cannot invite yourself")

        # Check for existing pending invite
        existing = await get_db()["invite_requests"].find_one({
            "kind": "campus_connect",
            "$or": [
                {"from_id": user["id"], "to_id": req.target_user_id, "status": "pending"},
                {"from_id": req.target_user_id, "to_id": user["id"], "status": "pending"},
            ],
            "extra.college": req.college,
        })
        if existing:
            raise HTTPException(status_code=400, detail="Invite already pending")

        doc = {
            "kind": "campus_connect",
            "from_id": user["id"],
            "from_name": user.get("name", "Anonymous"),
            "to_id": req.target_user_id,
            "to_name": "",
            "status": "pending",
            "created_at": _now(),
            "extra": {"college": req.college},
        }
        result = await get_db()["invite_requests"].insert_one(doc)
        return {"id": str(result.inserted_id), "status": "pending", "kind": "campus_connect"}

    raise HTTPException(status_code=400, detail=f"Unknown invite kind: {kind}")


# ─── GET /api/v1/invite/inbox ──────────────────────────────────────────────

@router.get("/inbox", summary="List received invites")
async def list_inbox(user=Depends(get_current_user)):
    invites = []
    cursor = get_db()["invite_requests"].find({"to_id": user["id"], "status": "pending"}).sort("created_at", -1)
    async for doc in cursor:
        invites.append(
            InboxItem(
                id=str(doc["_id"]),
                kind=doc["kind"],
                from_id=doc["from_id"],
                from_name=doc.get("from_name", "Anonymous"),
                to_id=doc["to_id"],
                to_name=doc.get("to_name", "Anonymous"),
                status=doc["status"],
                created_at=doc["created_at"],
                extra=doc.get("extra", {}),
            ).dict()
        )
    return {"invites": invites}


# ─── GET /api/v1/invite/outbox ─────────────────────────────────────────────

@router.get("/outbox", summary="List sent invites")
async def list_outbox(user=Depends(get_current_user)):
    invites = []
    cursor = get_db()["invite_requests"].find({"from_id": user["id"], "status": "pending"}).sort("created_at", -1)
    async for doc in cursor:
        invites.append(
            InboxItem(
                id=str(doc["_id"]),
                kind=doc["kind"],
                from_id=doc["from_id"],
                from_name=doc.get("from_name", "Anonymous"),
                to_id=doc["to_id"],
                to_name=doc.get("to_name", "Anonymous"),
                status=doc["status"],
                created_at=doc["created_at"],
                extra=doc.get("extra", {}),
            ).dict()
        )
    return {"invites": invites}


# ─── POST /api/v1/invite/{invite_id}/accept ────────────────────────────────

@router.post("/{invite_id}/accept", summary="Accept a unified invite")
async def accept_invite(invite_id: str, user=Depends(get_current_user)):
    oid = _to_objectid(invite_id)
    doc = await get_db()["invite_requests"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Invite not found")
    if doc["to_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not addressed to you")
    if doc["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invite already processed")

    kind = doc["kind"]
    now = _now()

    if kind == "friend":
        # Add mutual friendship
        await get_db()["friends_collection"].update_one(
            {"$or": [{"user_ids": [user["id"], doc["from_id"]]}, {"user_ids": [doc["from_id"], user["id"]]}]},
            {"$set": {"user_ids": sorted([user["id"], doc["from_id"]]), "updated_at": now}},
            upsert=True,
        )
        # Update invite target name
        await get_db()["invite_requests"].update_one({"_id": oid}, {"$set": {"to_name": user.get("name", "Anonymous"), "status": "accepted"}})
        return {"status": "accepted", "kind": "friend"}

    if kind == "study_squad":
        # Create a squad with two members
        names = [doc.get("from_name", "Anonymous"), user.get("name", "Anonymous")]
        ids = [doc["from_id"], user["id"]]
        squad = {
            "kind": "squad",
            "name": f"{names[0]} × {names[1]}",
            "member_ids": ids,
            "member_names": names,
            "created_at": now,
        }
        result = await get_db()["study_squads_collection"].insert_one(squad)
        # Mark invite as accepted
        await get_db()["invite_requests"].update_one({"_id": oid}, {"$set": {"status": "accepted"}})
        return {"status": "accepted", "kind": "study_squad", "squad_id": str(result.inserted_id)}

    if kind == "campus_connect":
        # Create a matched record for campus connect duel
        college = doc.get("extra", {}).get("college", "")
        match_doc = {
            "kind": "campus_connect_match",
            "college": college,
            "player1_id": doc["from_id"],
            "player2_id": user["id"],
            "status": "matched",
            "created_at": now,
        }
        # Use alumni_experiences collection as the match repository
        await get_db()["alumni_experiences_collection"].insert_one(match_doc)
        # Mark invite as accepted
        await get_db()["invite_requests"].update_one({"_id": oid}, {"$set": {"status": "accepted"}})
        return {"status": "accepted", "kind": "campus_connect"}

    await get_db()["invite_requests"].update_one({"_id": oid}, {"$set": {"status": "accepted"}})
    return {"status": "accepted", "kind": kind}


# ─── POST /api/v1/invite/{invite_id}/decline ────────────────────────────────

@router.post("/{invite_id}/decline", summary="Decline a unified invite")
async def decline_invite(invite_id: str, user=Depends(get_current_user)):
    oid = _to_objectid(invite_id)
    doc = await get_db()["invite_requests"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Invite not found")
    if doc["to_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not addressed to you")
    if doc["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invite already processed")

    await get_db()["invite_requests"].update_one({"_id": oid}, {"$set": {"status": "declined"}})
    return {"status": "declined", "kind": doc["kind"]}