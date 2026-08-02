import random
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.database import users_collection
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/mystery-box", tags=["mystery-box"])

MYSTERY_BOX_REWARDS = [
    {"type": "xp", "amount": 25, "label": "XP Boost", "emoji": "⚡", "weight": 30},
    {"type": "xp", "amount": 50, "label": "XP Boost", "emoji": "⚡", "weight": 20},
    {"type": "xp", "amount": 75, "label": "XP Boost", "emoji": "⚡", "weight": 10},
    {"type": "xp", "amount": 100, "label": "XP Boost", "emoji": "⚡", "weight": 5},
    {"type": "xp", "amount": 200, "label": "Jackpot XP", "emoji": "⚡", "weight": 2},
    {"type": "coins", "amount": 10, "label": "Coins", "emoji": "🪙", "weight": 20},
    {"type": "coins", "amount": 20, "label": "Coins", "emoji": "🪙", "weight": 15},
    {"type": "coins", "amount": 50, "label": "Coins", "emoji": "🪙", "weight": 5},
    {"type": "streak_freeze", "amount": 1, "label": "Streak Freeze", "emoji": "❄️", "weight": 15},
    {"type": "double_xp", "amount": 1, "label": "Double XP (24h)", "emoji": "×2", "weight": 10},
    {"type": "badge", "label": "Lucky Adventurer", "emoji": "🍀", "rarity": "uncommon", "weight": 8},
]

@router.post("/claim")
async def claim_mystery_box(user=Depends(get_current_user)):
    """Claim a random mystery box reward."""
    last_claim = user.get("last_mystery_box_claim")
    if last_claim:
        if isinstance(last_claim, str):
            from datetime import datetime as dt
            last_claim = dt.fromisoformat(last_claim)
        elapsed = (datetime.now(timezone.utc) - last_claim).total_seconds()
        if elapsed < 3600:
            remaining = int(3600 - elapsed)
            raise HTTPException(
                status_code=400,
                detail=f"Mystery box on cooldown. Come back in {remaining // 60} minutes!"
            )

    total_weight = sum(r["weight"] for r in MYSTERY_BOX_REWARDS)
    rand_val = random.randint(1, total_weight)
    cumulative = 0
    chosen = MYSTERY_BOX_REWARDS[0]
    for reward in MYSTERY_BOX_REWARDS:
        cumulative += reward["weight"]
        if rand_val <= cumulative:
            chosen = reward
            break

    if chosen["type"] == "xp":
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$inc": {"xp": chosen["amount"]}}
        )
    elif chosen["type"] == "coins":
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$inc": {"coins": chosen["amount"]}}
        )
    elif chosen["type"] == "streak_freeze":
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$inc": {"streak_freezes": chosen["amount"]}}
        )
    elif chosen["type"] == "double_xp":
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"double_xp_active": True, "double_xp_expires": datetime.now(timezone.utc).isoformat()}}
        )

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_mystery_box_claim": datetime.now(timezone.utc)}}
    )

    return {
        "reward": {
            "type": chosen["type"],
            "amount": chosen.get("amount", 0),
            "label": chosen["label"],
            "emoji": chosen["emoji"],
            "rarity": chosen.get("rarity", "common"),
        }
    }
