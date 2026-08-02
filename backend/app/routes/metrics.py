from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])

ALLOWED_FEATURES = [
    "daily_quest", "merchant", "guild", "dungeon", "battle", "campus",
    "boss", "season", "combo", "showcase", "scrim", "assignment",
    "collection", "events", "world", "prestige", "login",
]

ACTIVE_CAP = 2000


class TrackEventRequest(BaseModel):
    feature: str
    event: str
    value: Optional[float] = None


@router.post("/event")
async def track_event(req: TrackEventRequest, user=Depends(get_current_user)):
    db = get_db()
    if req.feature not in ALLOWED_FEATURES:
        raise HTTPException(status_code=400, detail="Invalid feature")
    if not req.event.strip() or len(req.event) > 50:
        raise HTTPException(status_code=400, detail="Invalid event")
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user["id"],
        "feature": req.feature,
        "event": req.event,
        "value": req.value,
        "day": now.strftime("%Y-%m-%d"),
        "created_at": now,
    }
    await db["feature_events"].insert_one(doc)
    return {"ok": True}


@router.get("/features")
async def list_features():
    return {"features": ALLOWED_FEATURES}


@router.get("/retention")
async def get_retention(user=Depends(get_current_user)):
    db = get_db()
    today = datetime.now(timezone.utc).date()
    since_day = (today - timedelta(days=6)).strftime("%Y-%m-%d")
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

    totals = {}
    async for row in db["feature_events"].aggregate([
        {"$group": {"_id": "$feature", "count": {"$sum": 1}}},
    ]):
        totals[row["_id"]] = row["count"]

    breakdown = {}
    async for row in db["feature_events"].aggregate([
        {"$group": {"_id": {"feature": "$feature", "event": "$event"}, "count": {"$sum": 1}}},
    ]):
        feature = row["_id"]["feature"]
        breakdown.setdefault(feature, []).append({"event": row["_id"]["event"], "count": row["count"]})

    active = {}
    async for row in db["feature_events"].aggregate([
        {"$match": {"day": {"$gte": since_day}}},
        {"$group": {"_id": "$feature", "users": {"$addToSet": "$user_id"}}},
        {"$project": {"_id": 0, "feature": "$_id", "active_users": {"$size": {"$slice": ["$users", ACTIVE_CAP]}}}},
    ]):
        active[row["feature"]] = row["active_users"]

    total_active_users_7d = 0
    async for row in db["feature_events"].aggregate([
        {"$match": {"day": {"$gte": since_day}}},
        {"$group": {"_id": None, "users": {"$addToSet": "$user_id"}}},
        {"$project": {"_id": 0, "count": {"$size": {"$slice": ["$users", ACTIVE_CAP]}}}},
    ]):
        total_active_users_7d = row["count"]

    events_last_7d = await db["feature_events"].count_documents({"day": {"$gte": since_day}})

    daily_map = {}
    async for row in db["feature_events"].aggregate([
        {"$match": {"day": {"$gte": since_day}}},
        {"$group": {"_id": "$day", "users": {"$addToSet": "$user_id"}}},
        {"$project": {"_id": 0, "day": "$_id", "users": {"$size": {"$slice": ["$users", ACTIVE_CAP]}}}},
    ]):
        daily_map[row["day"]] = row["users"]

    daily_active = [{"day": d, "users": daily_map.get(d, 0)} for d in days]

    features = []
    for feature in ALLOWED_FEATURES:
        evts = sorted(breakdown.get(feature, []), key=lambda x: x["count"], reverse=True)
        features.append({
            "feature": feature,
            "total_events": totals.get(feature, 0),
            "active_users": active.get(feature, 0),
            "event_breakdown": evts,
        })

    return {
        "features": features,
        "overall": {
            "total_active_users_7d": total_active_users_7d,
            "events_last_7d": events_last_7d,
            "daily_active": daily_active,
        },
    }
