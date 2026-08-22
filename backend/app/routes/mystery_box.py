"""Mystery Box — random daily reward (coins, XP, streak freezes, Double XP)."""
import random
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from app.database import gamification_collection
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

COOLDOWN_SECONDS = 3600  # 1 hour


@router.post("/claim")
async def claim_mystery_box(user=Depends(get_current_user)):
    """Claim a random mystery box reward. One per hour cooldown."""
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    if not profile:
        profile = {}

    last_claim = profile.get("last_mystery_box_claim")
    if last_claim:
        elapsed = (datetime.now(timezone.utc) - last_claim).total_seconds()
        if elapsed < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - elapsed)
            raise HTTPException(
                status_code=400,
                detail=f"Mystery box on cooldown. Come back in {remaining // 60} minutes!",
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

    # Apply reward to the gamification profile (where the tower reads coins/xp/etc.)
    inc: dict = {}
    set_ops: dict = {"last_mystery_box_claim": datetime.now(timezone.utc)}
    if chosen["type"] == "xp":
        inc["xp"] = chosen["amount"]
    elif chosen["type"] == "coins":
        inc["coins"] = chosen["amount"]
    elif chosen["type"] == "streak_freeze":
        inc["streak_freezes"] = chosen["amount"]
    elif chosen["type"] == "double_xp":
        # 24-hour double-XP window (read by record_practice)
        expires = (datetime.now(timezone.utc).timestamp() + 86400)
        set_ops["double_xp_expires"] = datetime.fromtimestamp(expires, tz=timezone.utc).isoformat()

    update_doc: dict = {}
    if inc:
        update_doc["$inc"] = inc
    if set_ops:
        update_doc["$set"] = set_ops
    await gamification_collection.update_one({"user_id": user["id"]}, update_doc, upsert=True)

    return {
        "reward": {
            "type": chosen["type"],
            "amount": chosen.get("amount", 0),
            "label": chosen["label"],
            "emoji": chosen["emoji"],
            "rarity": chosen.get("rarity", "common"),
        }
    }
