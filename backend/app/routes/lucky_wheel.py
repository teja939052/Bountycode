from datetime import datetime, timezone, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument
from app.middleware.auth import get_current_user
from app.database import lucky_spins_collection
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/wheel", tags=["Wheel"])

WHEEL_REWARDS = [
    {"id": "xp_100", "label": "100 XP", "emoji": "✨", "weight": 30},
    {"id": "coins_50", "label": "50 Coins", "emoji": "🪙", "weight": 25},
    {"id": "xp_200", "label": "200 XP", "emoji": "⚡", "weight": 15},
    {"id": "rare_card", "label": "Rare Card", "emoji": "🃏", "weight": 10},
    {"id": "double_xp", "label": "Double XP (24h)", "emoji": "🔥", "weight": 8},
    {"id": "merchant_ticket", "label": "Merchant Ticket", "emoji": "🎫", "weight": 7},
    {"id": "epic_chest", "label": "Epic Chest", "emoji": "🧰", "weight": 3},
    {"id": "legendary_skin", "label": "Legendary Skin", "emoji": "👑", "weight": 2},
]

REWARD_PRIORITY = {
    "100 XP": 1,
    "50 Coins": 2,
    "200 XP": 3,
    "Rare Card": 4,
    "Double XP (24h)": 5,
    "Merchant Ticket": 6,
    "Epic Chest": 7,
    "Legendary Skin": 8,
}


def today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def pick_reward() -> str:
    labels = [r["label"] for r in WHEEL_REWARDS]
    weights = [r["weight"] for r in WHEEL_REWARDS]
    return random.choices(labels, weights=weights, k=1)[0]


@router.get("/state")
async def wheel_state(user=Depends(get_current_user)):
    today = today_str()
    doc = await lucky_spins_collection().find_one({"user_id": user["id"]})
    spun_today = bool(doc and doc.get("date") == today)

    remaining = 0
    if spun_today:
        now = datetime.now(timezone.utc)
        reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        remaining = max(0, int((reset - now).total_seconds()))

    return {
        "can_spin": not spun_today,
        "rewards": WHEEL_REWARDS,
        "last_reward": doc.get("reward") if doc else None,
        "remaining_in_24h_seconds": remaining,
    }


@router.post("/spin")
async def spin_wheel(user=Depends(get_current_user)):
    today = today_str()
    now = datetime.now(timezone.utc)
    user_id = user["id"]

    existing = await lucky_spins_collection().find_one({"user_id": user_id, "date": today})
    if existing:
        raise HTTPException(status_code=429, detail="Come back tomorrow — wheel resets daily")

    reward = pick_reward()

    doc = await lucky_spins_collection().find_one_and_update(
        {"user_id": user_id},
        {
            "$set": {"date": today, "reward": reward, "last_spun_at": now, "spin_count": 1},
            "$inc": {"total_spins": 1},
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    best = doc.get("best_reward")
    if not best or REWARD_PRIORITY.get(reward, 0) > REWARD_PRIORITY.get(best, 0):
        best = reward
    reward_counts = doc.get("reward_counts") or {}
    reward_counts[reward] = reward_counts.get(reward, 0) + 1
    await lucky_spins_collection().update_one(
        {"user_id": user_id},
        {"$set": {"best_reward": best, "reward_counts": reward_counts}},
    )

    if "XP" in reward:
        try:
            await record_practice(user_id, "wheel", 10)
        except Exception:
            pass

    return {
        "reward": reward,
        "message": f"You won {reward}!",
        "spin_count": doc.get("spin_count", 1),
        "total_spins": doc.get("total_spins", 1),
    }


@router.get("/stats")
async def wheel_stats(user=Depends(get_current_user)):
    user_id = user["id"]
    doc = await lucky_spins_collection().find_one({"user_id": user_id})

    earned = {}
    cursor = lucky_spins_collection().aggregate(
        [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": "$reward", "count": {"$sum": 1}}},
        ]
    )
    async for entry in cursor:
        if entry.get("_id"):
            earned[entry["_id"]] = entry["count"]

    stored = (doc or {}).get("reward_counts") or {}
    for label, count in stored.items():
        earned[label] = max(earned.get(label, 0), count)

    return {
        "total_spins": (doc or {}).get("total_spins", 0),
        "best_reward": (doc or {}).get("best_reward"),
        "reward_counts": earned,
        "spins_today": 1 if doc and doc.get("date") == today_str() else 0,
    }
