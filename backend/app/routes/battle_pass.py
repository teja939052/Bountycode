"""Battle Pass — seasonal tiered rewards system.
Free track: 20 tiers unlocked by daily XP.
Premium track: 40 tiers with exclusive cosmetic rewards.
Storage: 1 doc/user in battle_pass_collection (bounded)."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from app.middleware.auth import get_current_user
from app.database import get_db, users_collection, gamification_collection
from app.services.gamification import record_practice
from app.database import battle_pass_collection
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/pass", tags=["battle-pass"])

# ┃ 20 free tiers + 20 premium tiers = 40 max
FREE_TRACK_REWARDS = [
    {"tier": 1, "reward": "title:Newbie"},
    {"tier": 2, "reward": "emote:wave"},
    {"tier": 3, "reward": "coins:100"},
    {"tier": 4, "reward": "avatar_frame:blue_circuit"},
    {"tier": 5, "reward": "title:Problem Solver"},
    {"tier": 6, "reward": "emote:fire"},
    {"tier": 7, "reward": "coins:250"},
    {"tier": 8, "reward": "weapon_skin:default"},
    {"tier": 9, "reward": "emote:sparkles"},
    {"tier": 10, "reward": "title:Code Warrior"},
    {"tier": 11, "reward": "coins:400"},
    {"tier": 12, "reward": "avatar_frame:red_dragon"},
    {"tier": 13, "reward": "emote:thumbs_up"},
    {"tier": 14, "reward": "coins:600"},
    {"tier": 15, "reward": "title:Debugging Dynamo"},
    {"tier": 16, "reward": "emote:clap"},
    {"tier": 17, "reward": "coins:800"},
    {"tier": 18, "reward": "avatar_frame:golden_flame"},
    {"tier": 19, "reward": "emote:mind_blown"},
    {"tier": 20, "reward": "title:Algorithm Apprentice"},
]

PREMIUM_TRACK_REWARDS = [
    {"tier": 21, "reward": "cosmetic:premium_visor"},
    {"tier": 22, "reward": "title:Leader's Edge"},
    {"tier": 23, "reward": "emote:robot"},
    {"tier": 24, "reward": "coins:1000"},
    {"tier": 25, "reward": "avatar_frame:neon_grid"},
    {"tier": 26, "reward": "weapon_skin:plasma"},
    {"tier": 27, "reward": "emote:suspense"},
    {"tier": 28, "reward": "coins:1500"},
    {"tier": 29, "reward": "title:FAANG Aspirant"},
    {"tier": 30, "reward": "cosmetic:dragon_wing"},
]


@router.get("/track")
async def get_track(user=Depends(get_current_user)):
    """Get user's battle pass progress: current tier, XP, claimed rewards, shop."""
    db = get_db()
    bp_doc = await battle_pass_collection().find_one({"user_id": user["id"]})
    if not bp_doc:
        bp_doc = {"xp": 0, "claimed": [], "has_pass": False, "daily_logins": 0, "last_login": None}

    total_xp = bp_doc.get("xp", 0)
    has_pass = bp_doc.get("has_pass", False)
    claimed = set(bp_doc.get("claimed", []))

    # Tiers: 0 XP per tier (linear track)
    current_tier = 1
    for tier in range(1, 41):
        xp_req = tier * 50
        if total_xp >= xp_req:
            current_tier = tier
        else:
            break

    # Streak check
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    last_login = bp_doc.get("last_login")
    streak_active = False
    daily_bonus = 0
    if last_login:
        last_day = datetime.strptime(last_login[:10], "%Y-%m-%d")
        if (datetime.now(timezone.utc) - last_day).days <= 1:
            streak_active = True
            daily_bonus = 50  # streak bonus XP
        else:
            await battle_pass_collection().update_one(
                {"user_id": user["id"]},
                {"$set": {"daily_logins": 0}},
            )

    # Build reward list
    all_rewards = FREE_TRACK_REWARDS + (PREMIUM_TRACK_REWARDS if has_pass else [])
    rewards = []
    for r in all_rewards:
        unlocked = r["tier"] <= current_tier
        is_premium = r["tier"] > 20
        if is_premium and not has_pass:
            continue
        key = f"{r['tier']}:{r['reward']}"
        rewards.append({
            "tier": r["tier"],
            "reward": r["reward"],
            "unlocked": unlocked,
            "claimed": key in claimed,
            "premium": is_premium,
        })

    return {
        "current_tier": current_tier,
        "max_tier": 40,
        "total_xp": total_xp,
        "xp_for_next": (current_tier + 1) * 50 - total_xp if current_tier < 40 else 0,
        "claimed": len(claimed),
        "has_premium": has_pass,
        "daily_bonus_available": streak_active and today != last_login[:10],
        "daily_login_count": bp_doc.get("daily_logins", 0),
        "rewards": rewards,
    }


@router.post("/claim")
async def claim_reward(
    tier: int = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Claim a reward at a specific tier."""
    db = get_db()
    bp_doc = await battle_pass_collection().find_one({"user_id": user["id"]})
    total_xp = bp_doc.get("xp", 0) if bp_doc else 0
    has_pass = bp_doc.get("has_pass", False) if bp_doc else False
    claimed = set(bp_doc.get("claimed", [])) if bp_doc else set()

    if tier < 1 or tier > 40:
        raise HTTPException(400, "Invalid tier")

    # Check if premium tier requires pass
    if tier > 20 and not has_pass:
        raise HTTPException(400, "Premium track required")

    # Check XP threshold (50 XP per tier)
    if total_xp < tier * 50:
        raise HTTPException(400, f"Need {tier * 50} XP for Tier {tier}")

    # Find the reward
    all_rewards = FREE_TRACK_REWARDS + PREMIUM_TRACK_REWARDS
    reward_entry = next((r for r in all_rewards if r["tier"] == tier), None)
    if not reward_entry:
        raise HTTPException(404, "Reward not found")

    key = f"{tier}:{reward_entry['reward']}"
    if key in claimed:
        raise HTTPException(400, "Already claimed")

    await battle_pass_collection().update_one(
        {"user_id": user["id"]},
        {"$push": {"claimed": key}},
        upsert=True,
    )
    await record_practice(user["id"], "battle_pass_claim", 10, {"tier": tier, "reward": reward_entry["reward"]})

    return {"tier": tier, "reward": reward_entry["reward"], "message": "Claimed!"}


@router.post("/daily-login")
async def daily_login(user=Depends(get_current_user)):
    """Claim daily login XP bonus. Maintains streak."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    db = get_db()
    bp_doc = await battle_pass_collection().find_one({"user_id": user["id"]})
    if not bp_doc:
        bp_doc = {"xp": 0, "claimed": [], "has_pass": False, "daily_logins": 0, "last_login": None}

    last_login = bp_doc.get("last_login")
    streak_count = bp_doc.get("daily_logins", 0)

    if last_login and last_login[:10] == today:
        return {"xp_gained": 0, "message": "Already checked in today!", "streak": streak_count}

    # Check streak continuation
    if last_login:
        last_day = datetime.strptime(last_login[:10], "%Y-%m-%d")
        days_diff = (datetime.now(timezone.utc) - last_day).days
        if days_diff == 1:
            streak_count += 1
        elif days_diff > 1:
            streak_count = 1  # reset
    else:
        streak_count = 1

    xp_gained = 25 + (10 * min(streak_count, 7))  # up to +70 XP bonus on day 7

    await battle_pass_collection().update_one(
        {"user_id": user["id"]},
        {
            "$inc": {"xp": xp_gained},
            "$set": {"last_login": today, "daily_logins": streak_count},
        },
        upsert=True,
    )
    await record_practice(user["id"], "daily_login", xp_gained, {"streak": streak_count})

    return {"xp_gained": xp_gained, "streak": streak_count, "message": f"Checked in! +{xp_gained} XP (Streak: {streak_count} days)"}


@router.post("/premium")
async def activate_premium(user=Depends(get_current_user)):
    """Activate premium battle pass (e.g., via purchase)."""
    db = get_db()
    await battle_pass_collection().update_one(
        {"user_id": user["id"]},
        {"$set": {"has_pass": True}},
        upsert=True,
    )
    return {"success": True, "message": "Premium Battle Pass activated!"}
