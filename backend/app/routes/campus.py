from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument
from app.middleware.auth import get_current_user, optional_get_current_user
from app.database import (
    users_collection,
    campus_profiles_collection,
    campus_leaderboard_collection,
    campus_winners_collection,
    campus_events_collection,
)

router = APIRouter(prefix="/api/v1/campus", tags=["campus"])

MAX_COLLEGE_LEN = 60
MAX_REASON_LEN = 100


def current_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


async def add_college_points(user, amount, reason):
    college = user.get("college")
    if not college:
        raise HTTPException(status_code=400, detail="Join a college first")

    month = current_month()
    now = datetime.now(timezone.utc)
    user_id = user["id"]

    profile = await campus_profiles_collection().find_one({"user_id": user_id})
    is_new_member = (
        profile is None
        or profile.get("month") != month
        or profile.get("college") != college
    )

    if is_new_member:
        new_points = amount
        await campus_profiles_collection().update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "college": college,
                    "points": new_points,
                    "month": month,
                    "updated_at": now,
                }
            },
            upsert=True,
        )
    else:
        updated = await campus_profiles_collection().find_one_and_update(
            {"user_id": user_id},
            {"$inc": {"points": amount}, "$set": {"updated_at": now}},
            return_document=ReturnDocument.AFTER,
        )
        new_points = updated.get("points", amount)

    await campus_leaderboard_collection().update_one(
        {"college": college, "month": month},
        {
            "$inc": {"points": amount},
            "$setOnInsert": {"members": 0},
            "$set": {"updated_at": now},
        },
        upsert=True,
    )

    if is_new_member:
        await campus_leaderboard_collection().update_one(
            {"college": college, "month": month},
            {"$inc": {"members": 1}},
        )

    await campus_events_collection().update_one(
        {"month": month},
        {
            "$inc": {"points": amount},
            "$set": {"updated_at": now, "kind": "campus_event"},
        },
        upsert=True,
    )

    return new_points


@router.post("/profile")
async def set_profile(body: dict, user=Depends(get_current_user)):
    college = (body.get("college") or "").strip()[:MAX_COLLEGE_LEN]
    if not college:
        raise HTTPException(status_code=400, detail="College name is required")

    now = datetime.now(timezone.utc)
    month = current_month()

    await users_collection().update_one(
        {"_id": user["_id"]},
        {"$set": {"college": college, "updated_at": now}},
    )

    await campus_profiles_collection().update_one(
        {"user_id": user["id"]},
        {
            "$set": {
                "college": college,
                "points": 0,
                "month": month,
                "updated_at": now,
            }
        },
        upsert=True,
    )

    return {"college": college}


@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    month = current_month()
    profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    college = profile.get("college") if profile else user.get("college")
    points = 0
    rank = None

    if college:
        if profile and profile.get("month") == month:
            points = profile.get("points", 0)
        entry = await campus_leaderboard_collection().find_one(
            {"college": college, "month": month}
        )
        if entry:
            ahead = await campus_leaderboard_collection().count_documents(
                {"month": month, "points": {"$gt": entry.get("points", 0)}}
            )
            rank = ahead + 1

    return {
        "college": college,
        "points": points,
        "rank": rank,
        "month": month,
    }


@router.post("/points")
async def add_points(body: dict, user=Depends(get_current_user)):
    try:
        amount = int(body.get("amount", 0))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="amount must be a number")
    if amount < 1 or amount > 500:
        raise HTTPException(status_code=400, detail="amount must be between 1 and 500")

    reason = (body.get("reason") or "").strip()[:MAX_REASON_LEN] or "activity"
    new_points = await add_college_points(user, amount, reason)
    return {"points": new_points}


@router.get("/leaderboard")
async def get_leaderboard(user=Depends(optional_get_current_user)):
    month = current_month()
    cursor = (
        campus_leaderboard_collection()
        .find({"month": month})
        .sort("points", -1)
        .limit(50)
    )
    colleges = []
    user_rank = None
    rank = 1
    async for doc in cursor:
        colleges.append(
            {
                "rank": rank,
                "college": doc.get("college"),
                "points": doc.get("points", 0),
                "members": doc.get("members", 0),
            }
        )
        if user and user.get("college") and doc.get("college") == user.get("college"):
            user_rank = rank
        rank += 1

    return {
        "month": month,
        "leaderboard": colleges,
        "user_college": user.get("college") if user else None,
        "user_rank": user_rank,
    }


@router.get("/global")
async def get_global():
    month = current_month()
    event = await campus_events_collection().find_one(
        {"month": month, "kind": "campus_event"}
    )
    if not event:
        event = await campus_events_collection().find_one({"month": month})
    total = event.get("points", 0) if event else 0
    top = await campus_leaderboard_collection().find_one(
        {"month": month}, sort=[("points", -1)]
    )
    return {
        "month": month,
        "total_points": total,
        "top_college": top.get("college") if top else None,
        "top_points": top.get("points", 0) if top else 0,
    }


@router.get("/winners")
async def get_winners():
    cursor = campus_winners_collection().find().sort("month", -1).limit(3)
    winners = [
        {
            "month": w.get("month"),
            "college": w.get("college"),
            "points": w.get("points", 0),
        }
        async for w in cursor
    ]
    return {"winners": winners}


@router.post("/finalize")
async def finalize_month(user=Depends(get_current_user)):
    month = current_month()
    now = datetime.now(timezone.utc)
    latest = await campus_leaderboard_collection().find_one(
        {"month": {"$ne": month}}, sort=[("month", -1)]
    )
    if not latest:
        return {"message": "No completed months to finalize"}

    winner_month = latest["month"]
    top = await campus_leaderboard_collection().find_one(
        {"month": winner_month}, sort=[("points", -1)]
    )
    if not top:
        return {"message": "No entries to finalize"}

    result = await campus_winners_collection().update_one(
        {"month": winner_month},
        {
            "$set": {
                "college": top.get("college"),
                "points": top.get("points", 0),
                "updated_at": now,
            }
        },
        upsert=True,
    )

    return {
        "month": winner_month,
        "college": top.get("college"),
        "points": top.get("points", 0),
        "new": result.upserted_id is not None,
    }
