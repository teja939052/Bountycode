"""Placement Timeline — derived from EXISTING collections. Zero new storage.

No timeline_collection: milestones and activity are computed on demand from
real data (question answers, battles, interviews, offers, gamification).
Every user sees their journey without a single extra byte written to Mongo.
"""
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    users_collection,
    gamification_collection,
    question_answers_collection,
    battles_collection,
    interviews_collection,
    offers_collection,
)

router = APIRouter(prefix="/api/v1/timeline", tags=["Timeline"])

ACTIVITY_COLLECTIONS = [
    ("problem_solved", "question_answers", "created_at"),
    ("dungeon_clear", "gamification", "updated_at"),
    ("battle_win", "battles", "created_at"),
]

ACTIVITY_EVENT_TYPES = ("problem_solved", "dungeon_clear", "battle_win")


def _iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return None


async def _resolve_user_oid(user_id: str):
    try:
        return ObjectId(user_id)
    except Exception:
        return None


async def _user_name(oid) -> str:
    if not oid:
        return "Student"
    u = await users_collection().find_one({"_id": oid}, {"name": 1})
    return (u.get("name") or "Student") if u else "Student"


def _milestone(event_type, title, created_at, meta=None):
    return {
        "event_type": event_type,
        "title": title,
        "meta": meta or {},
        "created_at": _iso(created_at),
    }


async def _derive_milestones(user_id: str, oid):
    """Build the milestone list from real activity, newest first."""
    milestones = []

    # Problems solved
    try:
        async for a in (
            question_answers_collection()
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(15)
        ):
            title = (a.get("title") or a.get("question_title") or "Problem solved")
            milestones.append(
                _milestone("problem_solved", title, a.get("created_at"))
            )
    except Exception:
        pass

    # Battles won
    try:
        async for b in (
            battles_collection()
            .find({"$or": [{"player1_id": user_id}, {"player2_id": user_id}]})
            .sort("created_at", -1)
            .limit(10)
        ):
            if b.get("status") != "completed":
                continue
            winner_id = str(b.get("winner_id") or "")
            if winner_id == user_id:
                milestones.append(
                    _milestone("battle_win", "Won a 1v1 battle", b.get("created_at"))
                )
    except Exception:
        pass

    # Interviews
    try:
        async for it in (
            interviews_collection()
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(10)
        ):
            role = it.get("job_role") or it.get("role") or "Mock interview"
            milestones.append(_milestone("interview", role, it.get("created_at")))
    except Exception:
        pass

    # Offers
    try:
        async for o in (
            offers_collection()
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(5)
        ):
            company = o.get("company") or "a company"
            milestones.append(_milestone("offer", f"Offer from {company}", o.get("created_at")))
    except Exception:
        pass

    # Level ups from gamification profile (highest level + streak)
    try:
        gam = await gamification_collection().find_one({"user_id": user_id})
        if gam:
            level = gam.get("level") or 1
            milestones.append(_milestone("level_up", f"Reached Level {level}", gam.get("updated_at")))
    except Exception:
        pass

    milestones.sort(key=lambda m: m.get("created_at") or "", reverse=True)
    return milestones


async def _derive_activity(user_id: str, days: int):
    """Contribution graph computed from existing data. Zero new storage."""
    since = datetime.now(timezone.utc) - timedelta(days=days)
    activity = {}

    try:
        async for a in (
            question_answers_collection()
            .find({"user_id": user_id, "created_at": {"$gte": since}})
            .sort("created_at", 1)
        ):
            d = a.get("created_at")
            if d:
                day = d.strftime("%Y-%m-%d")
                activity[day] = activity.get(day, 0) + 1
    except Exception:
        pass

    try:
        async for b in (
            battles_collection()
            .find({"$or": [{"player1_id": user_id}, {"player2_id": user_id}],
                   "created_at": {"$gte": since}})
            .sort("created_at", 1)
        ):
            d = b.get("created_at")
            if d:
                day = d.strftime("%Y-%m-%d")
                activity[day] = activity.get(day, 0) + 1
    except Exception:
        pass

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days - 1)
    return {
        "days": days,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "activity": activity,
    }


@router.get("")
async def get_own_timeline(user=Depends(get_current_user)):
    """Derived journey: no storage, computed from real activity."""
    milestones = await _derive_milestones(user["id"], user.get("_id"))
    return {"timeline": milestones}


@router.get("/activity")
async def get_activity(days: int = 180, user=Depends(get_current_user)):
    days = max(1, min(int(days), 365))
    return await _derive_activity(user["id"], days)


@router.get("/{user_id}")
async def get_public_timeline(user_id: str):
    """Public journey for Alumni Heroes — derived, not stored."""
    oid = await _resolve_user_oid(user_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="User not found")
    target = await users_collection().find_one({"_id": oid}, {"name": 1})
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    milestones = await _derive_milestones(user_id, oid)
    return {
        "user": {"id": user_id, "name": target.get("name", "Student")},
        "timeline": milestones,
    }
