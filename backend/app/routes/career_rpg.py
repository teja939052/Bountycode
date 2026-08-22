"""Career RPG API routes -- 13 endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.services.career_rpg import (
    get_rpg_profile, get_career_rank, get_rank_ladder,
    get_skill_tree, get_quest_chains, get_skill_bosses,
    get_company_dungeons, get_achievement_collections,
    SKILL_BOSSES, COMPANY_DUNGEONS, QUEST_CHAINS
)
from app.database import gamification_collection
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/rpg", tags=["Career RPG"])


@router.get("/profile")
async def rpg_profile(user=Depends(get_current_user)):
    profile = await get_rpg_profile(user["id"])
    return profile


@router.get("/ranks")
async def ranks():
    return get_rank_ladder()


@router.get("/rank/{level}")
async def rank_detail(level: int):
    if level < 1 or level > 100:
        raise HTTPException(400, "Level must be 1-100")
    return get_career_rank(level)


@router.get("/skill-tree")
async def skill_tree(user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    level = (profile or {}).get("level", 1)
    return get_skill_tree(level)


@router.get("/quests")
async def quest_chains(user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    level = (profile or {}).get("level", 1)
    progress = (profile or {}).get("rpg_progress", {})
    return get_quest_chains(level, progress)


class QuestStepComplete(BaseModel):
    quest_id: str
    step_id: str


@router.post("/quests/complete-step")
async def complete_quest_step(req: QuestStepComplete, user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    if not profile:
        profile = {"user_id": user["id"], "xp": 0, "level": 1, "streak": 0, "badges": [], "bosses_defeated": [], "rpg_progress": {"completed_steps": []}}
    rpg = profile.get("rpg_progress", {"completed_steps": []})
    steps = set(rpg.get("completed_steps", []))
    chain = next((c for c in QUEST_CHAINS if c["id"] == req.quest_id), None)
    if not chain:
        raise HTTPException(404, "Quest chain not found")
    step = next((s for s in chain["steps"] if s["id"] == req.step_id), None)
    if not step:
        raise HTTPException(404, "Step not found in chain")
    step_key = f"{req.quest_id}_{req.step_id}"
    was_new = step_key not in steps
    steps.add(step_key)
    xp_earned = 0
    if was_new:
        xp_earned = step.get("xp_reward", 20)
    new_steps = list(steps)
    rpg["completed_steps"] = new_steps
    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$set": {"rpg_progress": rpg, "xp": profile.get("xp", 0) + xp_earned}},
        upsert=True
    )
    chain_progress = sum(1 for s in chain["steps"] if f"{req.quest_id}_{s['id']}" in steps)
    return {
        "success": True,
        "step_completed": step_key,
        "xp_earned": xp_earned,
        "chain_progress": {"completed": chain_progress, "total": len(chain["steps"])},
        "chain_complete": chain_progress >= len(chain["steps"]),
        "chain_reward": {"xp": chain["reward_xp"], "badge": chain["reward_badge"]} if chain_progress >= len(chain["steps"]) else None
    }


@router.get("/bosses")
async def bosses(user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    level = (profile or {}).get("level", 1)
    defeated = (profile or {}).get("bosses_defeated", [])
    bosses = get_skill_bosses(level)
    for b in bosses:
        b["defeated"] = b["id"] in defeated
    return bosses


@router.get("/boss/{boss_id}")
async def boss_detail(boss_id: str, user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    level = (profile or {}).get("level", 1)
    boss = SKILL_BOSSES.get(boss_id)
    if not boss:
        raise HTTPException(404, "Boss not found")
    defeated = (profile or {}).get("bosses_defeated", [])
    return {**boss, "unlocked": level >= boss["unlock_level"], "defeated": boss_id in defeated}


class BossChallengeComplete(BaseModel):
    boss_id: str
    score: float


@router.post("/boss/challenge")
async def boss_challenge(req: BossChallengeComplete, user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    if not profile:
        profile = {"user_id": user["id"], "xp": 0, "level": 1, "streak": 0, "badges": [], "bosses_defeated": [], "rpg_progress": {}}
    boss = SKILL_BOSSES.get(req.boss_id)
    if not boss:
        raise HTTPException(404, "Boss not found")
    level = profile.get("level", 1)
    if level < boss["unlock_level"]:
        raise HTTPException(403, f"Boss unlocked at Level {boss['unlock_level']}")
    defeated = profile.get("bosses_defeated", [])
    already = req.boss_id in defeated
    won = req.score >= boss["pass_score"]
    xp_earned = 0
    new_badge = None
    if won and not already:
        defeated.append(req.boss_id)
        xp_earned = boss["reward_xp"]
        new_badge = boss["reward_badge"]
        badges = profile.get("badges", [])
        if new_badge not in badges:
            badges.append(new_badge)
            await gamification_collection.update_one(
                {"user_id": user["id"]},
                {"$set": {"badges": badges, "bosses_defeated": defeated, "xp": profile.get("xp", 0) + xp_earned}},
                upsert=True
            )
        else:
            await gamification_collection.update_one(
                {"user_id": user["id"]},
                {"$set": {"bosses_defeated": defeated, "xp": profile.get("xp", 0) + xp_earned}},
                upsert=True
            )
    return {
        "boss_id": req.boss_id,
        "score": req.score,
        "pass_score": boss["pass_score"],
        "defeated": won and not already,
        "already_defeated": already,
        "xp_earned": xp_earned,
        "badge_earned": new_badge
    }


@router.get("/dungeons")
async def dungeons(user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    readiness = 0.0
    try:
        from app.services.skill_assessment import get_readiness_score
        data = await get_readiness_score(user["id"])
        readiness = data.get("overall_readiness", 0.0)
    except Exception:
        pass
    cleared = (profile or {}).get("dungeons_cleared", [])
    dungeons = get_company_dungeons(readiness)
    for d in dungeons:
        d["cleared"] = d["id"] in cleared
    return dungeons


@router.get("/dungeon/{dungeon_id}")
async def dungeon_detail(dungeon_id: str, user=Depends(get_current_user)):
    dungeon = COMPANY_DUNGEONS.get(dungeon_id)
    if not dungeon:
        raise HTTPException(404, "Dungeon not found")
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    cleared = (profile or {}).get("dungeons_cleared", [])
    readiness = 0.0
    try:
        from app.services.skill_assessment import get_readiness_score
        data = await get_readiness_score(user["id"])
        readiness = data.get("overall_readiness", 0.0)
    except Exception:
        pass
    gate_progress = {}
    for gate in dungeon["gates"]:
        gate_progress[gate["id"]] = {"completed": False, "score": 0}
    return {**dungeon, "cleared": dungeon_id in cleared, "unlocked": readiness >= dungeon["min_readiness"], "gate_progress": gate_progress}


class DungeonGateComplete(BaseModel):
    dungeon_id: str
    gate_id: str
    score: float


@router.post("/dungeon/gate")
async def dungeon_gate_complete(req: DungeonGateComplete, user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    if not profile:
        profile = {"user_id": user["id"], "xp": 0, "level": 1, "streak": 0, "badges": [], "dungeons_cleared": [], "rpg_progress": {}}
    dungeon = COMPANY_DUNGEONS.get(req.dungeon_id)
    if not dungeon:
        raise HTTPException(404, "Dungeon not found")
    gate = next((g for g in dungeon["gates"] if g["id"] == req.gate_id), None)
    if not gate:
        raise HTTPException(404, "Gate not found")
    cleared = profile.get("dungeons_cleared", [])
    already_cleared = req.dungeon_id in cleared
    gate_key = f"{req.dungeon_id}_{req.gate_id}"
    dungeon_progress = profile.get("dungeon_progress", {})
    if already_cleared:
        dungeon_progress[gate_key] = {"completed": True, "score": max(req.score, dungeon_progress.get(gate_key, {}).get("score", 0))}
    else:
        dungeon_progress[gate_key] = {"completed": True, "score": req.score}
    all_gates_done = all(dungeon_progress.get(f"{req.dungeon_id}_{g['id']}", {}).get("completed", False) for g in dungeon["gates"])
    dungeon_cleared = False
    badge = None
    if all_gates_done and not already_cleared:
        cleared.append(req.dungeon_id)
        badge = dungeon["reward_badge"]
        badges = profile.get("badges", [])
        if badge not in badges:
            badges.append(badge)
        xp = profile.get("xp", 0) + sum(g["xp_reward"] for g in dungeon["gates"]) + dungeon["final_boss"]["xp_reward"]
        await gamification_collection.update_one(
            {"user_id": user["id"]},
            {"$set": {"dungeons_cleared": cleared, "dungeon_progress": dungeon_progress, "badges": badges, "xp": xp}},
            upsert=True
        )
        dungeon_cleared = True
    else:
        xp = profile.get("xp", 0) + gate["xp_reward"]
        await gamification_collection.update_one(
            {"user_id": user["id"]},
            {"$set": {"dungeon_progress": dungeon_progress, "xp": xp}},
            upsert=True
        )
    return {
        "gate_id": req.gate_id,
        "score": req.score,
        "passed": req.score >= gate["required_score"],
        "xp_earned": gate["xp_reward"],
        "dungeon_cleared": dungeon_cleared,
        "badge_earned": badge,
        "all_gates_complete": all_gates_done
    }


@router.get("/collections")
async def collections(user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    badges = (profile or {}).get("badges", [])
    return get_achievement_collections(badges)
