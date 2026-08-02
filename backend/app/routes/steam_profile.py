"""
Steam-style profile page.
Aggregates a user's entire identity from EXISTING collections only —
no new collections are created. Every query is guarded so a failing
collection never crashes the endpoint.
"""
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    get_db,
    users_collection,
    gamification_collection,
    question_answers_collection,
    interviews_collection,
    battles_collection,
    offers_collection,
    showcase_collection,
    analytics_events_collection,
    cards_collection,
)

router = APIRouter(prefix="/api/v1/profile/steam", tags=["Steam Profile"])


def _date_str(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return str(value)[:10]


async def _recent_activity(user_id: str):
    """Last 7 days of activity — analytics events, falling back to question answers."""
    today = datetime.now(timezone.utc).date()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    counts = {d: 0 for d in days}

    try:
        since = days[0]
        pipeline = [
            {"$match": {"user_id": user_id, "date": {"$gte": since}}},
            {"$group": {"_id": "$date", "count": {"$sum": 1}}},
        ]
        async for doc in analytics_events_collection().aggregate(pipeline):
            d = doc.get("_id")
            if d in counts:
                counts[d] = doc.get("count", 0)
    except Exception:
        try:
            since_dt = datetime.combine(today - timedelta(days=6), datetime.min.time(), tzinfo=timezone.utc)
            cursor = question_answers_collection().find(
                {"user_id": user_id, "created_at": {"$gte": since_dt}},
                {"created_at": 1},
            )
            async for doc in cursor:
                created = doc.get("created_at")
                if created:
                    d = _date_str(created)
                    if d in counts:
                        counts[d] += 1
        except Exception:
            pass

    return [{"date": d, "count": counts[d]} for d in days]


async def _collection_count(user_id: str):
    """Count owned cards/inventory items (collections that already exist)."""
    total = 0
    try:
        total += await cards_collection().count_documents({"user_id": user_id})
    except Exception:
        pass
    try:
        total += await get_db()["inventory"].count_documents({"user_id": user_id})
    except Exception:
        pass
    return {"count": total}


async def _build_profile(user_id: str):
    """Aggregate a user's entire identity from existing collections."""
    try:
        user = await users_collection().find_one({"_id": ObjectId(user_id)})
    except Exception:
        user = None
    if not user:
        return None

    payload = {
        "user": {
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "college": user.get("college", ""),
            "created_at": _date_str(user.get("created_at")) if user.get("created_at") else None,
        },
        "gamification": {"level": 1, "xp": 0, "streak": 0, "badges": [], "titles": []},
        "stats": {"problems": 0, "interviews": 0, "battles": 0, "offers": 0},
        "guild": None,
        "showcase": [],
        "recent_activity": [],
        "collection": {"count": 0},
    }

    try:
        gam = await gamification_collection().find_one({"user_id": user_id}) or {}
        payload["gamification"] = {
            "level": gam.get("level", 1),
            "xp": gam.get("xp", 0),
            "streak": gam.get("streak", 0),
            "badges": gam.get("badges", []),
            "titles": gam.get("titles", []),
        }
    except Exception:
        pass

    try:
        payload["stats"]["problems"] = await question_answers_collection().count_documents({"user_id": user_id})
    except Exception:
        pass
    try:
        payload["stats"]["interviews"] = await interviews_collection().count_documents({"user_id": user_id})
    except Exception:
        pass
    try:
        payload["stats"]["battles"] = await battles_collection().count_documents({
            "$or": [{"player1_id": ObjectId(user_id)}, {"player2_id": ObjectId(user_id)}]
        })
    except Exception:
        pass
    try:
        payload["stats"]["offers"] = await offers_collection().count_documents({"user_id": user_id})
    except Exception:
        pass

    try:
        guild = await get_db()["guilds"].find_one({"members.user_id": user_id})
        if guild:
            members = guild.get("members", [])
            mine = next((m for m in members if m.get("user_id") == user_id), None)
            payload["guild"] = {
                "id": str(guild.get("_id")),
                "name": guild.get("name", ""),
                "xp": guild.get("xp", 0),
                "level": guild.get("level", 1),
                "title": guild.get("level_title", ""),
                "member_count": len(members),
                "my_role": "owner" if guild.get("owner_id") == user_id else "member",
                "my_contribution": (mine or {}).get("xp_contributed", 0),
            }
    except Exception:
        pass

    try:
        projects = []
        cursor = showcase_collection().find({"author_id": ObjectId(user_id)}).sort("created_at", -1).limit(6)
        async for p in cursor:
            projects.append({
                "id": str(p.get("_id", "")),
                "title": p.get("title", ""),
                "language": p.get("language", ""),
                "likes": p.get("likes", 0),
                "views": p.get("views", 0),
            })
        payload["showcase"] = projects
    except Exception:
        pass

    payload["recent_activity"] = await _recent_activity(user_id)
    payload["collection"] = await _collection_count(user_id)

    return payload


@router.get("")
async def my_steam_profile(user=Depends(get_current_user)):
    profile = await _build_profile(user["id"])
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return profile


@router.get("/{user_id}")
async def public_steam_profile(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    profile = await _build_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return profile
