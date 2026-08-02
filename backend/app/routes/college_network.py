"""College Network — reuses EXISTING collections, zero new storage.

Membership lives in `campus_profiles_collection` (already keyed by user_id +
college). Feed events reuse `campus_events_collection`. Leaderboards/stats are
computed at request time. No new Mongo collections are created.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import get_current_user
from app.database import (
    users_collection,
    gamification_collection,
    offers_collection,
    campus_profiles_collection,
    campus_events_collection,
)

router = APIRouter(prefix="/api/v1/college", tags=["College Network"])

MAX_COLLEGE_LEN = 60
MAX_BRANCH_LEN = 40
VALID_YEARS = {"1", "2", "3", "4", "5"}


def _clean_text(value, max_len):
    return (value or "").strip()[:max_len]


def _clean_year(value):
    year = str(value or "").strip()[:4]
    if year and year not in VALID_YEARS:
        raise HTTPException(status_code=400, detail="Year must be 1-5")
    return year


async def _resolve_college(user, college):
    college = _clean_text(college, MAX_COLLEGE_LEN)
    if not college and user:
        profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
        if profile:
            college = profile.get("college")
    if not college:
        raise HTTPException(status_code=400, detail="College is required")
    return college


def _serialize_profile(doc):
    return {
        "user_id": doc.get("user_id"),
        "college": doc.get("college"),
        "branch": doc.get("branch", ""),
        "year": doc.get("year", ""),
        "name": doc.get("name", ""),
        "xp": doc.get("xp", 0),
        "joined_at": doc.get("joined_at"),
        "updated_at": doc.get("updated_at"),
    }


async def _user_lookup():
    return {
        "from": "users",
        "let": {"uid": "$user_id"},
        "pipeline": [
            {"$match": {"$expr": {"$eq": [{"$toString": "$_id"}, "$$uid"]}}},
            {"$project": {"name": 1, "email": 1}},
        ],
        "as": "user",
    }


async def _gam_lookup():
    return {
        "from": "gamification",
        "let": {"uid": "$user_id"},
        "pipeline": [
            {"$match": {"$expr": {"$eq": ["$user_id", "$$uid"]}}},
            {"$project": {"xp": 1}},
        ],
        "as": "gam",
    }


async def record_college_feed(user_id, college, event_type, text, name=""):
    """Insert an event into the shared campus_events feed (best-effort)."""
    try:
        await campus_events_collection().insert_one(
            {
                "user_id": user_id,
                "college": college,
                "name": name,
                "event_type": event_type,
                "text": text,
                "kind": "feed",
                "created_at": datetime.now(timezone.utc),
            }
        )
    except Exception:
        pass


@router.post("/join")
async def join_college(body: dict, user=Depends(get_current_user)):
    college = _clean_text(body.get("college"), MAX_COLLEGE_LEN)
    if not college:
        raise HTTPException(status_code=400, detail="College name is required")
    branch = _clean_text(body.get("branch"), MAX_BRANCH_LEN)
    if not branch:
        raise HTTPException(status_code=400, detail="Branch is required")
    year = _clean_year(body.get("year"))
    if not year:
        raise HTTPException(status_code=400, detail="Year is required")

    now = datetime.now(timezone.utc)
    user_id = user["id"]
    name = user.get("name", "")

    gam = await gamification_collection().find_one({"user_id": user_id})
    xp = gam.get("xp", 0) if gam else 0

    existing = await campus_profiles_collection().find_one({"user_id": user_id})
    changed = (
        existing is None
        or existing.get("college") != college
        or existing.get("branch") != branch
        or existing.get("year") != year
    )

    await campus_profiles_collection().update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "college": college,
                "branch": branch,
                "year": year,
                "name": name,
                "xp": xp,
                "updated_at": now,
            },
            "$setOnInsert": {"joined_at": now},
        },
        upsert=True,
    )

    await users_collection().update_one(
        {"_id": user["_id"]},
        {"$set": {"college": college, "updated_at": now}},
    )

    if changed:
        await record_college_feed(
            user_id, college, "joined",
            f"{name or 'A student'} joined {college}",
            name=name,
        )

    profile = await campus_profiles_collection().find_one({"user_id": user_id})
    return {"profile": _serialize_profile(profile)}


@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    if not profile:
        return {"profile": None, "stats": None}

    college = profile.get("college")
    stats = {"total_students": 0, "avg_xp": 0}
    if college:
        pipeline = [
            {"$match": {"college": college}},
            await _gam_lookup(),
            {"$unwind": {"path": "$gam", "preserveNullAndEmptyArrays": True}},
            {
                "$group": {
                    "_id": None,
                    "total_students": {"$sum": 1},
                    "avg_xp": {"$avg": {"$ifNull": ["$gam.xp", 0]}},
                }
            },
        ]
        docs = await campus_profiles_collection().aggregate(pipeline).to_list(1)
        if docs:
            stats = {
                "total_students": docs[0].get("total_students", 0),
                "avg_xp": round(docs[0].get("avg_xp", 0) or 0),
            }

    return {"profile": _serialize_profile(profile), "stats": stats}


@router.get("/leaderboard")
async def get_leaderboard(
    college: str = Query(None),
    user=Depends(get_current_user),
):
    college = _resolve_college(user, college)

    pipeline = [
        {"$match": {"college": college}},
        await _user_lookup(),
        {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}},
        await _gam_lookup(),
        {"$unwind": {"path": "$gam", "preserveNullAndEmptyArrays": True}},
        {"$sort": {"gam.xp": -1}},
        {"$limit": 100},
    ]

    students = []
    rank = 1
    async for doc in campus_profiles_collection().aggregate(pipeline):
        gam = doc.get("gam") or {}
        u = doc.get("user") or {}
        students.append(
            {
                "rank": rank,
                "user_id": doc.get("user_id"),
                "name": u.get("name") or doc.get("name") or "Anonymous",
                "branch": doc.get("branch", ""),
                "year": doc.get("year", ""),
                "xp": gam.get("xp", 0),
                "is_me": doc.get("user_id") == user["id"],
            }
        )
        rank += 1

    return {"college": college, "leaderboard": students, "total": len(students)}


@router.get("/feed")
async def get_feed(
    college: str = Query(None),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    college = _resolve_college(user, college)

    cursor = (
        campus_events_collection()
        .find({"college": college, "kind": "feed"})
        .sort("created_at", -1)
        .limit(limit)
    )
    events = []
    async for doc in cursor:
        events.append(
            {
                "id": str(doc.get("_id")),
                "user_id": doc.get("user_id"),
                "name": doc.get("name", "Anonymous"),
                "event_type": doc.get("event_type", "update"),
                "text": doc.get("text", ""),
                "created_at": doc.get("created_at"),
            }
        )

    return {"college": college, "events": events}


@router.get("/same-batch")
async def get_same_batch(
    branch: str = Query(None),
    year: str = Query(None),
    user=Depends(get_current_user),
):
    profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    if not profile:
        raise HTTPException(status_code=400, detail="Join a college first")

    college = profile.get("college")
    branch = _clean_text(branch, MAX_BRANCH_LEN) or profile.get("branch", "")
    year = _clean_year(year) or profile.get("year", "")

    cursor = (
        campus_profiles_collection()
        .find({"college": college, "branch": branch, "year": year})
        .limit(100)
    )
    peers = []
    async for doc in cursor:
        if doc.get("user_id") == user["id"]:
            continue
        gam = await gamification_collection().find_one({"user_id": doc.get("user_id")})
        peers.append(
            {
                "user_id": doc.get("user_id"),
                "name": doc.get("name") or "Anonymous",
                "branch": doc.get("branch", ""),
                "year": doc.get("year", ""),
                "xp": gam.get("xp", 0) if gam else 0,
            }
        )

    return {"college": college, "branch": branch, "year": year, "peers": peers}


@router.get("/cell")
async def get_placement_cell(user=Depends(get_current_user)):
    profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    college = profile.get("college") if profile else None
    if not college:
        raise HTTPException(status_code=400, detail="Join a college first")

    pipeline = [
        {"$match": {"college": college}},
        await _user_lookup(),
        {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}},
        await _gam_lookup(),
        {"$unwind": {"path": "$gam", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "offers",
                "let": {"uid": "$user_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$user_id", "$$uid"]}}},
                    {"$project": {"_id": 1}},
                ],
                "as": "offers",
            }
        },
        {
            "$group": {
                "_id": None,
                "total_students": {"$sum": 1},
                "avg_xp": {"$avg": {"$ifNull": ["$gam.xp", 0]}},
                "offers_count": {"$sum": {"$size": "$offers"}},
                "students": {
                    "$push": {
                        "user_id": "$user_id",
                        "name": {"$ifNull": ["$user.name", "$name"]},
                        "branch": "$branch",
                        "year": "$year",
                        "xp": {"$ifNull": ["$gam.xp", 0]},
                    }
                },
            }
        },
    ]

    docs = await campus_profiles_collection().aggregate(pipeline).to_list(1)
    if not docs:
        return {
            "college": college,
            "total_students": 0,
            "avg_xp": 0,
            "top_student": None,
            "offers_count": 0,
        }

    d = docs[0]
    students = d.get("students", [])
    top = max(students, key=lambda s: s.get("xp", 0)) if students else None
    return {
        "college": college,
        "total_students": d.get("total_students", 0),
        "avg_xp": round(d.get("avg_xp", 0) or 0),
        "top_student": top,
        "offers_count": d.get("offers_count", 0),
    }
