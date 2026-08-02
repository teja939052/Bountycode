"""Guild Castle — shared guild defense rooms, resource pools, cross-guild battles.
Reuses guilds_collection (members), battle_pass_collection (castle upgrades).
Bounded castle_states collection: 1 doc/guild."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from app.middleware.auth import get_current_user
from app.database import get_db, guilds_collection, gamification_collection, battle_pass_collection
from app.services.gamification import record_practice
import logging, random, secrets

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/castle", tags=["guild-castle"])

CASTLE_ZONES = ["outer_wall", "inner_keep", "treasure_vault"]
ZONE_HP = {"outer_wall": 1000, "inner_keep": 500, "treasure_vault": 200}
ZONE_DEFENSE = {"outer_wall": 5, "inner_keep": 15, "treasure_vault": 30}

CASTLE_REWARDS = {
    "outer_wall": {"xp": 50, "coins": 25, "badge": "wall_guard"},
    "inner_keep": {"xp": 100, "coins": 50, "badge": "keep_defender"},
    "treasure_vault": {"xp": 200, "coins": 100, "badge": "vault_protector"},
}

UPGRADES = {
    "wall_strength": {"name": "Wall Reinforcement", "cost": 100, "effect": "+10% defense"},
    "guard_tower": {"name": "Guard Tower", "cost": 200, "effect": "+5% XP bonus"},
    "treasure_chest": {"name": "Treasure Chest", "cost": 150, "effect": "+25% coin bonus"},
    "spy_network": {"name": "Spy Network", "cost": 300, "effect": "Reveal enemy strategy"},
}


@router.get("/{guild_id}")
async def get_castle(guild_id: str, user=Depends(get_current_user)):
    """Get castle state for a guild."""
    db = get_db()
    castle = await db["castle_states"].find_one({"guild_id": guild_id})
    if not castle:
        castle = {
            "guild_id": guild_id,
            "zones": {z: {"hp": ZONE_HP[z], "max_hp": ZONE_HP[z], "defense": ZONE_DEFENSE[z]} for z in CASTLE_ZONES},
            "resources": {"coins": 0, "gems": 0},
            "upgrades": {},
            "last_attacked": None,
            "members_online": 0,
        }
        await db["castle_states"].insert_one(castle)

    return castle


@router.post("/{guild_id}/defend")
async def defend_castle(
    guild_id: str,
    zone: str = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Defend a castle zone. Consumes energy, grants XP + coins."""
    if zone not in CASTLE_ZONES:
        raise HTTPException(400, "Invalid zone")

    db = get_db()
    castle = await db["castle_states"].find_one({"guild_id": guild_id})
    if not castle:
        raise HTTPException(404, "Castle not found")

    # Check user is guild member
    guild = await guilds_collection().find_one({"_id": guild_id})
    if not guild or user["id"] not in guild.get("members", []):
        raise HTTPException(403, "Not a guild member")

    zone_data = castle["zones"][zone]
    damage = random.randint(10, 30)
    zone_data["hp"] = max(0, zone_data["hp"] - damage)
    zone_data["defense"] += 1

    reward = CASTLE_REWARDS[zone]
    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": reward["xp"], "coins": reward["coins"]}},
        upsert=True,
    )

    await record_practice(user["id"], "castle_defend", reward["xp"], {"zone": zone, "guild_id": guild_id})

    await db["castle_states"].update_one(
        {"guild_id": guild_id},
        {"$set": {f"zones.{zone}": zone_data}},
    )

    return {
        "zone": zone,
        "damage_taken": damage,
        "hp_remaining": zone_data["hp"],
        "reward": reward,
        "message": f"Defended {zone}! +{reward['xp']} XP, +{reward['coins']} coins",
    }


@router.post("/{guild_id}/attack")
async def attack_castle(
    guild_id: str,
    zone: str = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Attack an enemy guild's castle zone."""
    if zone not in CASTLE_ZONES:
        raise HTTPException(400, "Invalid zone")

    db = get_db()
    target_castle = await db["castle_states"].find_one({"guild_id": guild_id})
    if not target_castle:
        raise HTTPException(404, "Target castle not found")

    zone_data = target_castle["zones"][zone]
    attack_power = random.randint(20, 50)
    zone_data["hp"] = max(0, zone_data["hp"] - attack_power)

    success = zone_data["hp"] <= 0
    if success:
        await record_practice(user["id"], "castle_attack", 150, {"zone": zone, "guild_id": guild_id})
        await gamification_collection().update_one(
            {"user_id": user["id"]},
            {"$inc": {"xp": 150, "coins": 75}},
            upsert=True,
        )
        message = f"Zone {zone} destroyed! +150 XP, +75 coins"
    else:
        await record_practice(user["id"], "castle_attack", 25, {"zone": zone, "guild_id": guild_id})
        await gamification_collection().update_one(
            {"user_id": user["id"]},
            {"$inc": {"xp": 25, "coins": 10}},
            upsert=True,
        )
        message = f"Attacked {zone}! HP: {zone_data['hp']}/{target_castle['zones'][zone]['max_hp']}"

    await db["castle_states"].update_one(
        {"guild_id": guild_id},
        {"$set": {f"zones.{zone}": zone_data}},
    )

    return {
        "zone": zone,
        "attack_power": attack_power,
        "hp_remaining": zone_data["hp"],
        "zone_destroyed": success,
        "message": message,
    }


@router.post("/{guild_id}/upgrade")
async def upgrade_castle(
    guild_id: str,
    upgrade_id: str = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Purchase a castle upgrade."""
    if upgrade_id not in UPGRADES:
        raise HTTPException(400, "Invalid upgrade")

    upgrade = UPGRADES[upgrade_id]
    db = get_db()
    castle = await db["castle_states"].find_one({"guild_id": guild_id})
    if not castle:
        raise HTTPException(404, "Castle not found")

    # Check if user is guild leader/officer
    guild = await guilds_collection().find_one({"_id": guild_id})
    if not guild or user["id"] not in guild.get("members", []):
        raise HTTPException(403, "Not a guild member")

    # Check coins (deduct from guild resources)
    if castle["resources"]["coins"] < upgrade["cost"]:
        raise HTTPException(403, "Not enough guild coins")

    castle["resources"]["coins"] -= upgrade["cost"]
    castle["upgrades"][upgrade_id] = castle["upgrades"].get(upgrade_id, 0) + 1

    await db["castle_states"].update_one(
        {"guild_id": guild_id},
        {"$set": {"resources": castle["resources"], "upgrades": castle["upgrades"]}},
    )

    await record_practice(user["id"], "castle_upgrade", 50, {"upgrade": upgrade_id, "guild_id": guild_id})

    return {
        "upgrade": upgrade_id,
        "name": upgrade["name"],
        "effect": upgrade["effect"],
        "cost": upgrade["cost"],
        "level": castle["upgrades"][upgrade_id],
        "message": f"{upgrade['name']} upgraded to level {castle['upgrades'][upgrade_id]}!",
    }


@router.get("/{guild_id}/leaderboard")
async def get_castle_leaderboard(guild_id: str, limit: int = 20):
    """Top defenders for a guild's castle."""
    db = get_db()
    castle = await db["castle_states"].find_one({"guild_id": guild_id})
    if not castle:
        return {"guild_id": guild_id, "leaderboard": []}

    # Get guild members sorted by castle XP
    members = guild.get("members", []) if (guild := await guilds_collection().find_one({"_id": guild_id})) else []
    leaderboard = []
    for member_id in members[:limit]:
        gam = await gamification_collection().find_one({"user_id": member_id})
        if gam:
            leaderboard.append({
                "user_id": member_id,
                "xp": gam.get("xp", 0),
                "castle_points": gam.get("castle_points", 0),
            })

    leaderboard.sort(key=lambda x: x["castle_points"], reverse=True)
    return {"guild_id": guild_id, "leaderboard": leaderboard}


@router.post("/{guild_id}/daily-bonus")
async def daily_castle_bonus(guild_id: str, user=Depends(get_current_user)):
    """Daily bonus for castle defense activity."""
    db = get_db()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    castle = await db["castle_states"].find_one({"guild_id": guild_id})
    if not castle:
        raise HTTPException(404, "Castle not found")

    last_bonus = castle.get("last_daily_bonus")
    if last_bonus == today:
        return {"message": "Already claimed today", "bonus": 0}

    bonus_xp = 30
    bonus_coins = 15

    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": bonus_xp, "coins": bonus_coins}},
        upsert=True,
    )

    await db["castle_states"].update_one(
        {"guild_id": guild_id},
        {"$set": {"last_daily_bonus": today}},
    )

    await record_practice(user["id"], "castle_daily", bonus_xp, {"guild_id": guild_id})

    return {"message": f"Daily bonus claimed! +{bonus_xp} XP, +{bonus_coins} coins", "xp": bonus_xp, "coins": bonus_coins}