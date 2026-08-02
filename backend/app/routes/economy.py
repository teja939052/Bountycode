"""Economy/Marketplace — in-app currency and marketplace."""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
import random
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/economy", tags=["economy"])

CURRENCY_NAME = "PlacementCoin"
CURRENCY_SYMBOL = "🪙"

ITEMS = {
    "powerup_extra_time": {"name": "Extra Time Power-Up", "emoji": "⏰", "cost": 10, "type": "powerup", "rarity": "common"},
    "powerup_hint": {"name": "Hint Reveal", "emoji": "💡", "cost": 15, "type": "powerup", "rarity": "common"},
    "powerup_retry": {"name": "Retry Token", "emoji": "🔄", "cost": 25, "type": "powerup", "rarity": "uncommon"},
    "powerup_double_xp": {"name": "Double XP Token", "emoji": "✨", "cost": 50, "type": "powerup", "rarity": "rare"},
    "powerup_skip_boss": {"name": "Skip Boss Token", "emoji": "🚫", "cost": 75, "type": "powerup", "rarity": "rare"},
    "powerup_show_answer": {"name": "Show Answer Token", "emoji": "👁️", "cost": 100, "type": "powerup", "rarity": "legendary"},
    "theme_dark": {"name": "Dark Theme", "emoji": "🌙", "cost": 20, "type": "theme", "rarity": "common"},
    "theme_neon": {"name": "Neon Theme", "emoji": "💜", "cost": 30, "type": "theme", "rarity": "uncommon"},
    "theme_gold": {"name": "Gold Theme", "emoji": "🥇", "cost": 50, "type": "theme", "rarity": "rare"},
    "avatar_hat_crown": {"name": "Crown Hat", "emoji": "👑", "cost": 25, "type": "avatar", "rarity": "rare"},
    "avatar_hat_wizard": {"name": "Wizard Hat", "emoji": "🧙", "cost": 20, "type": "avatar", "rarity": "common"},
    "avatar_hat_helmet": {"name": "Helmet", "emoji": "⚔️", "cost": 30, "type": "avatar", "rarity": "uncommon"},
    "badge_gold": {"name": "Gold Badge", "emoji": "🥇", "cost": 100, "type": "badge", "rarity": "legendary"},
    "badge_silver": {"name": "Silver Badge", "emoji": "🥈", "cost": 50, "type": "badge", "rarity": "rare"},
    "badge_bronze": {"name": "Bronze Badge", "emoji": "🥉", "cost": 25, "type": "badge", "rarity": "uncommon"},
}

DAILY_BONUS_AMOUNT = 10
STREAK_BONUS_AMOUNT = 25


@router.get("/balance")
async def get_balance(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    balance = user_gam.get("currency_balance", 0) if user_gam else 0
    inventory = user_gam.get("inventory", []) if user_gam else []

    return {
        "currency": CURRENCY_NAME,
        "symbol": CURRENCY_SYMBOL,
        "balance": balance,
        "inventory": inventory,
    }


@router.post("/earn")
async def earn_currency(req: dict, user=Depends(get_current_user)):
    amount = req.get("amount", 0)
    source = req.get("source", "manual")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": {"currency_balance": amount}},
        upsert=True,
    )

    return {"earned": amount, "source": source, "new_balance": amount}


@router.post("/daily-bonus")
async def daily_bonus(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    last_daily = user_gam.get("last_daily_bonus") if user_gam else None

    if last_daily:
        last_daily_dt = datetime.fromisoformat(last_daily) if isinstance(last_daily, str) else last_daily
        if (datetime.now(timezone.utc) - last_daily_dt).days < 1:
            raise HTTPException(status_code=400, detail="Already claimed today")

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": {"currency_balance": DAILY_BONUS_AMOUNT}, "$set": {"last_daily_bonus": datetime.now(timezone.utc)}},
        upsert=True,
    )

    return {"earned": DAILY_BONUS_AMOUNT, "new_balance": DAILY_BONUS_AMOUNT}


@router.get("/shop")
async def get_shop(user=Depends(get_current_user)):
    return {"items": ITEMS}


@router.post("/buy")
async def buy_item(req: dict, user=Depends(get_current_user)):
    item_id = req.get("item_id")
    if not item_id:
        raise HTTPException(status_code=400, detail="item_id is required")

    item = ITEMS.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    balance = user_gam.get("currency_balance", 0) if user_gam else 0

    if balance < item["cost"]:
        raise HTTPException(status_code=400, detail=f"Insufficient {CURRENCY_NAME}. Need {item['cost']}, have {balance}")

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": {"currency_balance": -item["cost"]}, "$push": {"inventory": item_id}},
        upsert=True,
    )

    return {"purchased": item_id, "item": item["name"], "cost": item["cost"], "remaining_balance": balance - item["cost"]}


@router.post("/sell")
async def sell_item(req: dict, user=Depends(get_current_user)):
    item_id = req.get("item_id")
    if not item_id:
        raise HTTPException(status_code=400, detail="item_id is required")

    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    inventory = user_gam.get("inventory", []) if user_gam else []

    if item_id not in inventory:
        raise HTTPException(status_code=400, detail="Item not in inventory")

    item = ITEMS.get(item_id)
    sell_price = max(1, int(item["cost"] * 0.5)) if item else 1

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": {"currency_balance": sell_price}, "$pull": {"inventory": item_id}},
    )

    return {"sold": item_id, "earned": sell_price}


@router.get("/transactions")
async def get_transactions(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    transactions = user_gam.get("transactions", []) if user_gam else []
    return {"transactions": transactions[-20:]}