import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/merchant", tags=["merchant"])

SHOP_SLOTS = 4

ITEM_POOL = [
    {"id": "card_neon_samurai", "name": "Neon Samurai Card", "type": "card", "price": 80, "discount_pct": 50, "emoji": "🗡️"},
    {"id": "card_void_dragon", "name": "Void Dragon Card", "type": "card", "price": 120, "discount_pct": 25, "emoji": "🐉"},
    {"id": "card_astro_cat", "name": "Astro Cat Card", "type": "card", "price": 60, "discount_pct": 0, "emoji": "🐱"},
    {"id": "card_golden_phoenix", "name": "Golden Phoenix Card", "type": "card", "price": 150, "discount_pct": 50, "emoji": "🦅"},
    {"id": "card_tiny_griffin", "name": "Tiny Griffin Card", "type": "card", "price": 50, "discount_pct": 50, "emoji": "🦁"},
    {"id": "xp_potion_minor", "name": "Minor XP Potion", "type": "xp_potion", "price": 40, "discount_pct": 50, "emoji": "🧪"},
    {"id": "xp_potion_grand", "name": "Grand XP Potion", "type": "xp_potion", "price": 90, "discount_pct": 25, "emoji": "⚗️"},
    {"id": "xp_potion_legend", "name": "Legendary XP Elixir", "type": "xp_potion", "price": 140, "discount_pct": 0, "emoji": "🍾"},
    {"id": "double_xp_ember", "name": "Double XP Ember", "type": "double_xp_token", "price": 70, "discount_pct": 50, "emoji": "🔥"},
    {"id": "double_xp_bolt", "name": "Double XP Bolt", "type": "double_xp_token", "price": 85, "discount_pct": 0, "emoji": "⚡"},
    {"id": "avatar_cyber_ghost", "name": "Cyber Ghost Avatar", "type": "avatar", "price": 55, "discount_pct": 25, "emoji": "👻"},
    {"id": "avatar_circuit_robot", "name": "Circuit Robot Avatar", "type": "avatar", "price": 75, "discount_pct": 50, "emoji": "🤖"},
    {"id": "avatar_sword_maiden", "name": "Sword Maiden Avatar", "type": "avatar", "price": 95, "discount_pct": 0, "emoji": "⚔️"},
    {"id": "avatar_lunar_fox", "name": "Lunar Fox Avatar", "type": "avatar", "price": 65, "discount_pct": 25, "emoji": "🦊"},
    {"id": "border_royal", "name": "Royal Indigo Border", "type": "border", "price": 100, "discount_pct": 50, "emoji": "👑"},
    {"id": "border_abyss", "name": "Abyss Noir Border", "type": "border", "price": 130, "discount_pct": 25, "emoji": "🌌"},
    {"id": "border_emerald_vip", "name": "Emerald VIP Border", "type": "border", "price": 110, "discount_pct": 0, "emoji": "💎"},
]


class BuyItemRequest(BaseModel):
    item_id: str


def _today_str() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _final_price(item: dict) -> int:
    return item["price"] - (item["price"] * item["discount_pct"] // 100)


def _pick_items(date_key: str) -> list:
    ranked = []
    for item in ITEM_POOL:
        seed = int.from_bytes(hashlib.sha256((date_key + item["id"]).encode("utf-8")).digest()[:4], "big")
        ranked.append((seed, item))
    ranked.sort(key=lambda pair: pair[0])
    return [item for _, item in ranked[:SHOP_SLOTS]]


def _serialize_item(item: dict, purchased: bool) -> dict:
    return {
        "id": item["id"],
        "name": item["name"],
        "type": item["type"],
        "emoji": item["emoji"],
        "price": _final_price(item),
        "original_price": item["price"],
        "discount_pct": item["discount_pct"],
        "purchased": purchased,
    }


@router.get("")
async def get_shop(user=Depends(get_current_user)):
    db = get_db()
    today = _today_str()
    bought = set()
    async for p in db["merchant_purchases"].find({"user_id": user["id"], "date": today}):
        bought.add(p["item_id"])
    profile = await db["gamification"].find_one({"user_id": user["id"]})
    return {
        "date": today,
        "coins": (profile or {}).get("coins", 0),
        "items": [_serialize_item(item, item["id"] in bought) for item in _pick_items(today)],
    }


@router.post("/buy")
async def buy_item(req: BuyItemRequest, user=Depends(get_current_user)):
    db = get_db()
    item = next((i for i in ITEM_POOL if i["id"] == req.item_id), None)
    if not item:
        raise HTTPException(status_code=400, detail="Unknown item")

    today = _today_str()
    existing = await db["merchant_purchases"].find_one(
        {"user_id": user["id"], "date": today, "item_id": req.item_id}
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already bought today")

    await db["merchant_purchases"].insert_one({
        "user_id": user["id"],
        "date": today,
        "item_id": req.item_id,
        "created_at": datetime.now(timezone.utc),
    })

    xp_earned = 0
    reward = None
    if item["type"] == "xp_potion":
        try:
            result = await record_practice(user["id"], "merchant", 100)
            xp_earned = result.get("xp_gained", 0)
        except Exception:
            xp_earned = 0
        reward = {"type": "xp", "amount": xp_earned}
    else:
        await db["merchant_owned"].update_one(
            {"user_id": user["id"], "item_id": req.item_id},
            {"$set": {"owned_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        reward = {"type": item["type"], "item_id": req.item_id}

    return {
        "success": True,
        "item": _serialize_item(item, True),
        "reward": reward,
        "xp_earned": xp_earned,
    }
