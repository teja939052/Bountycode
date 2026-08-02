import hashlib
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.middleware.auth import get_current_user, optional_get_current_user
from app.database import (
    daily_boss_collection, daily_boss_damage_collection, daily_boss_claims_collection,
    seasons_collection, season_xp_collection, combos_collection,
)
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/game", tags=["game-events"])

BOSS_POOL = [
    "Amazon OA #421", "Google Phone Screen #837", "Meta Onsite #502",
    "Netflix Culture Fit #113", "Microsoft Interview Day #269",
    "Atlassian System Design #744", "Stripe Tech Screen #608",
    "Uber Backend Loop #317", "LinkedIn Top Bar #891",
    "Airbnb Hiring Bar #452", "Flipkart SDE Loop #635", "TCS NQT #204",
    "Infosys System Test #518", "Wipro Turbo Hire #777",
    "Zoho Programming Round #340", "PayPal Code Exercise #922",
    "Shopify Product Round #586", "Samsung R&D #439",
    "Oracle Interview #663", "Cisco Virtual Onsite #275",
]

BOSS_HP_TOTAL = 1200000
BOSS_DURATION_HOURS = 8

SEASON_THEMES = [
    "Cyberpunk", "Neon City", "Crystal Caverns", "Desert Storm",
    "Frostbound", "Ember Arena", "Galactic Frontier", "Neo Tokyo",
    "Wild West", "Medieval Quest", "Steampunk", "Solar Flare",
    "Deep Sea", "Jungle Run", "Volcanic Isle", "Ice Palace",
    "Sky Pirates", "Underground", "Time Rift", "Void Runner",
]

BASE_SEASON_DATE = datetime(2026, 1, 1)
SEASON_DURATION_DAYS = 30


def _today_str() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _pick_boss_name(day_key: str) -> str:
    seed = int.from_bytes(hashlib.sha256(day_key.encode("utf-8")).digest()[:4], "big")
    return BOSS_POOL[seed % len(BOSS_POOL)]


def _pick_theme(season_number: int) -> str:
    return SEASON_THEMES[(season_number - 1) % len(SEASON_THEMES)]


def _serialize_boss(boss: dict, today_damage: int = 0) -> dict:
    hp_total = boss.get("hp_total", BOSS_HP_TOTAL)
    hp_remaining = max(0, boss.get("hp_remaining", 0))
    percent = round(hp_remaining / hp_total * 100, 2) if hp_total > 0 else 0.0
    return {
        "id": str(boss["_id"]),
        "boss_id": str(boss["_id"]),
        "name": boss.get("name", ""),
        "boss_name": boss.get("name", ""),
        "date": boss.get("date", ""),
        "hp_total": hp_total,
        "hp_remaining": hp_remaining,
        "percent": percent,
        "started_at": boss.get("started_at").isoformat() if isinstance(boss.get("started_at"), datetime) else None,
        "ends_at": boss.get("ends_at").isoformat() if isinstance(boss.get("ends_at"), datetime) else None,
        "defeated": hp_remaining <= 0,
        "defeated_at": boss.get("defeated_at").isoformat() if isinstance(boss.get("defeated_at"), datetime) else None,
        "today_player_damage": today_damage,
    }


@router.get("/boss")
async def get_today_boss(user=Depends(optional_get_current_user)):
    today = _today_str()
    boss = await daily_boss_collection().find_one({"date": today})
    if not boss:
        now = datetime.now(timezone.utc)
        doc = {
            "date": today,
            "name": _pick_boss_name(today),
            "hp_total": BOSS_HP_TOTAL,
            "hp_remaining": BOSS_HP_TOTAL,
            "started_at": now,
            "ends_at": now + timedelta(hours=BOSS_DURATION_HOURS),
        }
        try:
            await daily_boss_collection().insert_one(doc)
        except DuplicateKeyError:
            boss = await daily_boss_collection().find_one({"date": today})
            if not boss:
                raise HTTPException(status_code=500, detail="Failed to create today's boss")
        else:
            boss = doc

    today_damage = 0
    if user:
        pipeline = [
            {"$match": {"boss_id": str(boss["_id"]), "user_id": user["id"]}},
            {"$group": {"_id": None, "total": {"$sum": "$damage"}}},
        ]
        async for entry in daily_boss_damage_collection().aggregate(pipeline):
            today_damage = entry.get("total", 0)

    return _serialize_boss(boss, today_damage)


@router.post("/boss/{boss_id}/damage")
async def boss_damage(boss_id: str, body: dict, user=Depends(get_current_user)):
    try:
        oid = ObjectId(boss_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Boss not found")

    damage = body.get("damage")
    if not isinstance(damage, int):
        raise HTTPException(status_code=400, detail="Damage must be an integer")
    if damage < 1 or damage > 2000:
        raise HTTPException(status_code=400, detail="Damage must be between 1 and 2000")

    boss = await daily_boss_collection().find_one({"_id": oid})
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")
    if boss.get("defeated_at") or boss.get("hp_remaining", 0) <= 0:
        raise HTTPException(status_code=400, detail="Boss already defeated")

    hp_remaining = max(0, boss.get("hp_remaining", 0) - damage)
    update = {"$set": {"hp_remaining": hp_remaining}}
    defeated = hp_remaining <= 0
    if defeated:
        update["$set"]["defeated_at"] = datetime.now(timezone.utc)
    await daily_boss_collection().update_one({"_id": oid}, update)

    await daily_boss_damage_collection().insert_one({
        "boss_id": str(oid),
        "user_id": user["id"],
        "damage": damage,
        "created_at": datetime.now(timezone.utc),
    })

    result = {
        "boss_id": str(oid),
        "damage": damage,
        "hp_remaining": hp_remaining,
        "hp_total": boss.get("hp_total", BOSS_HP_TOTAL),
        "percent": round(hp_remaining / boss.get("hp_total", 1) * 100, 2),
        "defeated": defeated,
    }
    if defeated:
        try:
            await record_practice(user["id"], "daily_boss", 100)
        except Exception:
            pass
        result["reward_xp"] = 100
    return result


@router.post("/boss/{boss_id}/claim")
async def claim_boss_reward(boss_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(boss_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Boss not found")

    boss = await daily_boss_collection().find_one({"_id": oid})
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")
    if not boss.get("defeated_at") or boss.get("hp_remaining", 0) > 0:
        raise HTTPException(status_code=400, detail="Boss not defeated yet")

    claim = {
        "boss_id": str(oid),
        "user_id": user["id"],
        "claimed_at": datetime.now(timezone.utc),
    }
    try:
        await daily_boss_claims_collection().insert_one(claim)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Already claimed today's reward")

    try:
        await record_practice(user["id"], "daily_boss_claim", 50)
    except Exception:
        pass
    return {"boss_id": str(oid), "reward_xp": 50, "claimed": True}


def _current_season_number(now=None) -> int:
    if now is None:
        now = datetime.now(timezone.utc)
    return (now.year - BASE_SEASON_DATE.year) * 12 + (now.month - BASE_SEASON_DATE.month) + 1


@router.get("/seasons")
async def get_current_season():
    now = datetime.now(timezone.utc)
    season_number = _current_season_number(now)
    season = await seasons_collection().find_one({"season_number": season_number})
    if not season:
        theme = _pick_theme(season_number)
        start_date = BASE_SEASON_DATE + timedelta(days=(season_number - 1) * SEASON_DURATION_DAYS)
        end_date = start_date + timedelta(days=SEASON_DURATION_DAYS)
        doc = {
            "season_number": season_number,
            "name": f"Season {season_number} — {theme}",
            "theme": theme,
            "start_date": start_date,
            "end_date": end_date,
            "exclusive_card": f"Legendary {theme} Card",
            "badge": f"{theme} Champion",
            "created_at": now,
        }
        try:
            await seasons_collection().insert_one(doc)
        except DuplicateKeyError:
            season = await seasons_collection().find_one({"season_number": season_number})
            if not season:
                raise HTTPException(status_code=500, detail="Failed to create current season")
        else:
            season = doc

    return {
        "id": str(season["_id"]),
        "season_id": str(season["_id"]),
        "season_number": season.get("season_number"),
        "name": season.get("name", ""),
        "theme": season.get("theme", ""),
        "start_date": season.get("start_date").isoformat() if isinstance(season.get("start_date"), datetime) else None,
        "end_date": season.get("end_date").isoformat() if isinstance(season.get("end_date"), datetime) else None,
        "exclusive_card": season.get("exclusive_card", ""),
        "badge": season.get("badge", ""),
    }


@router.get("/seasons/{season_id}/leaderboard")
async def season_leaderboard(season_id: str):
    try:
        oid = ObjectId(season_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Season not found")

    season = await seasons_collection().find_one({"_id": oid})
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    pipeline = [
        {"$match": {"season_id": str(oid)}},
        {"$sort": {"xp": -1}},
        {"$limit": 50},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user",
        }},
        {"$unwind": "$user"},
        {"$project": {
            "user_id": 1,
            "user_name": "$user.name",
            "xp": 1,
        }},
    ]
    leaderboard = []
    async for entry in season_xp_collection().aggregate(pipeline):
        leaderboard.append({
            "user_id": entry.get("user_id"),
            "user_name": entry.get("user_name", "Anonymous"),
            "xp": entry.get("xp", 0),
        })

    return {
        "season_id": str(oid),
        "leaderboard": leaderboard,
        "total_participants": await season_xp_collection().count_documents({"season_id": str(oid)}),
    }


@router.post("/seasons/{season_id}/xp")
async def add_season_xp(season_id: str, body: dict, user=Depends(get_current_user)):
    try:
        oid = ObjectId(season_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Season not found")

    season = await seasons_collection().find_one({"_id": oid})
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    amount = body.get("amount")
    if not isinstance(amount, int):
        raise HTTPException(status_code=400, detail="Amount must be an integer")
    if amount < 1 or amount > 1000:
        raise HTTPException(status_code=400, detail="Amount must be between 1 and 1000")

    await season_xp_collection().update_one(
        {"season_id": str(oid), "user_id": user["id"]},
        {"$inc": {"xp": amount}, "$setOnInsert": {"created_at": datetime.now(timezone.utc)}},
        upsert=True,
    )
    entry = await season_xp_collection().find_one({"season_id": str(oid), "user_id": user["id"]})
    return {
        "season_id": str(oid),
        "user_id": user["id"],
        "xp": entry.get("xp", amount) if entry else amount,
    }


@router.post("/combo/record")
async def record_combo(body: dict, user=Depends(get_current_user)):
    success = body.get("success")
    if not isinstance(success, bool):
        raise HTTPException(status_code=400, detail="success must be a boolean")

    now = datetime.now(timezone.utc)
    combo = await combos_collection().find_one({"user_id": user["id"]})
    if not combo:
        combo = {"user_id": user["id"], "consecutive_count": 0, "best": 0, "updated_at": now}
        await combos_collection().insert_one(combo)

    if success:
        consecutive = combo.get("consecutive_count", 0) + 1
        best = max(combo.get("best", 0), consecutive)
        await combos_collection().update_one(
            {"user_id": user["id"]},
            {"$set": {"consecutive_count": consecutive, "best": best, "updated_at": now}},
        )
        multiplier = min(5, 1 + consecutive // 3)
        bonus_xp = 10 * (multiplier - 1)
        if bonus_xp > 0:
            try:
                await record_practice(user["id"], "combo", bonus_xp)
            except Exception:
                pass
    else:
        consecutive = 0
        best = combo.get("best", 0)
        multiplier = 1
        bonus_xp = 0
        await combos_collection().update_one(
            {"user_id": user["id"]},
            {"$set": {"consecutive_count": 0, "updated_at": now}},
        )

    return {
        "consecutive": consecutive,
        "multiplier": multiplier,
        "bonus_xp": bonus_xp,
        "best": best,
    }


@router.get("/combo")
async def get_combo(user=Depends(get_current_user)):
    combo = await combos_collection().find_one({"user_id": user["id"]})
    if not combo:
        return {"consecutive": 0, "multiplier": 1, "best": 0}
    consecutive = combo.get("consecutive_count", 0)
    return {
        "consecutive": consecutive,
        "multiplier": min(5, 1 + consecutive // 3),
        "best": combo.get("best", 0),
    }
