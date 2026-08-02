"""Shareable Achievements — generate viral share cards, track shares.
Reuses users_collection, gamification_collection.
Bounded shares_collection: 1 doc/user/day, TTL 30 days."""
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from app.middleware.auth import get_current_user
from app.database import get_db, users_collection, gamification_collection
from app.services.cache import get_cache
import json, hashlib, random

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/share", tags=["shareable-achievements"])

CARD_TEMPLATES = [
    {"name": "victory", "bg": "from-indigo-600 to-purple-700", "icon": "🏆", "label": "Victory"},
    {"name": "streak", "bg": "from-amber-500 to-orange-600", "icon": "🔥", "label": "Streak"},
    {"name": "smart", "bg": "from-emerald-500 to-teal-600", "icon": "🧠", "label": "Smart Move"},
    {"name": "legend", "bg": "from-rose-500 to-pink-600", "icon": "👑", "label": "Legend"},
    {"name": "rocket", "bg": "from-sky-500 to-blue-600", "icon": "🚀", "label": "Rocket"},
]

SHARE_TYPES = {
    "interview_complete": {"icon": "🎙️", "label": "Completed Interview"},
    "aptitude_score": {"icon": "📝", "label": "Aptitude Score"},
    "coding_solved": {"icon": "💻", "label": "Coding Challenge Solved"},
    "castle_defend": {"icon": "🏰", "label": "Castle Defender"},
    "daily_streak": {"icon": "🔥", "label": "Daily Streak"},
    "level_up": {"icon": "⬆️", "label": "Level Up"},
    "badge_earned": {"icon": "🎖️", "label": "Badge Earned"},
    "tower_climb": {"icon": "🏗️", "label": "Tower Climb"},
}


def _generate_card_url(user, achievement_type, score_data):
    """Generate a deterministic share card URL (SVG-based, no storage needed)."""
    template = random.choice(CARD_TEMPLATES)
    payload = {
        "u": user["id"],
        "n": user.get("name", "Player"),
        "t": achievement_type,
        "s": score_data,
        "v": template["name"],
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    token = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
    return f"/api/v1/share/card/{token}"


@router.post("/generate")
async def generate_share_card(
    achievement_type: str = Body(..., embed=True),
    score_data: dict = Body(default_factory=dict),
    user=Depends(get_current_user),
):
    """Generate a shareable achievement card."""
    if achievement_type not in SHARE_TYPES:
        raise HTTPException(400, "Invalid achievement type")

    db = get_db()
    card_url = _generate_card_url(user, achievement_type, score_data)

    share_record = {
        "user_id": user["id"],
        "achievement_type": achievement_type,
        "card_url": card_url,
        "score_data": score_data,
        "template": random.choice(CARD_TEMPLATES)["name"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "shares": 0,
    }

    await db["shares_collection"].update_one(
        {"user_id": user["id"], "achievement_type": achievement_type, "date": datetime.now(timezone.utc).strftime("%Y-%m-%d")},
        {"$set": share_record},
        upsert=True,
    )

    # Award XP for sharing
    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": 5, "coins": 2}},
        upsert=True,
    )

    return {
        "card_url": card_url,
        "share_text": SHARE_TYPES[achievement_type]["label"],
        "icon": SHARE_TYPES[achievement_type]["icon"],
        "xp_earned": 5,
        "coins_earned": 2,
    }


@router.get("/card/{token}")
async def get_share_card(token: str):
    """Serve share card data (SVG generation endpoint)."""
    db = get_db()
    record = await db["shares_collection"].find_one({"card_url": f"/api/v1/share/card/{token}"})
    if not record:
        raise HTTPException(404, "Share card not found")

    user = await users_collection().find_one({"id": record["user_id"]}, {"name": 1, "email": 1, "avatar": 1})
    if not user:
        raise HTTPException(404, "User not found")

    template = next((t for t in CARD_TEMPLATES if t["name"] == record.get("template", "victory")), CARD_TEMPLATES[0])

    return {
        "card_url": record["card_url"],
        "user_name": user.get("name", "Player"),
        "achievement": SHARE_TYPES.get(record["achievement_type"], {"icon": "⭐", "label": "Achievement"}),
        "score_data": record.get("score_data", {}),
        "template": template,
        "share_text": f"I just earned '{record['achievement_type']}' on PlacementPro! Can you beat my score?",
    }


@router.post("/{token}/share")
async def record_share(token: str, user=Depends(get_current_user)):
    """Record a social share and award bonus XP."""
    db = get_db()
    record = await db["shares_collection"].find_one({"card_url": f"/api/v1/share/card/{token}"})
    if not record:
        raise HTTPException(404, "Share card not found")

    await db["shares_collection"].update_one(
        {"_id": record["_id"]},
        {"$inc": {"shares": 1}},
    )

    # Bonus XP for sharing
    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": 10, "coins": 5}},
        upsert=True,
    )

    return {"message": "Share recorded! +10 XP, +5 coins", "total_shares": record.get("shares", 0) + 1}


@router.get("/my-cards")
async def my_share_cards(user=Depends(get_current_user)):
    """Get user's shareable achievement cards."""
    db = get_db()
    cards = []
    async for doc in db["shares_collection"].find({"user_id": user["id"]}).sort("created_at", -1).limit(20):
        doc["_id"] = str(doc["_id"])
        cards.append(doc)
    return {"cards": cards, "total": len(cards)}


@router.get("/leaderboard")
async def share_leaderboard(limit: int = 10):
    """Top sharers by total shares."""
    cache = await get_cache()
    cache_key = f"share_leaderboard:{limit}"
    cached = await cache.get("share", cache_key)
    if cached:
        return cached

    db = get_db()
    pipeline = [
        {"$group": {"_id": "$user_id", "total_shares": {"$sum": "$shares"}}},
        {"$sort": {"total_shares": -1}},
        {"$limit": limit},
    ]
    results = []
    async for doc in db["shares_collection"].aggregate(pipeline):
        user = await users_collection().find_one({"id": doc["_id"]}, {"name": 1})
        results.append({
            "user_id": doc["_id"],
            "user_name": user.get("name", "Anonymous") if user else "Anonymous",
            "total_shares": doc["total_shares"],
        })
    await cache.set("share", cache_key, results, ttl=300)
    return {"leaderboard": results}