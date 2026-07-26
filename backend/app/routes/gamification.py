from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middleware.auth import get_current_user
from app.services.gamification import (
    get_gamification_profile,
    record_practice,
    get_leaderboard,
    ensure_tower_fields,
    use_power_up,
    buy_power_up,
    get_challenges,
    claim_challenge_reward,
    buy_streak_freeze,
    get_streak_freeze_status,
    get_daily_goal,
    BADGES,
    POWER_UPS,
    BOSS_BATTLES,
)
from app.services.skill_assessment import (
    get_skill_graph,
    get_weak_areas,
    get_readiness_score,
    update_skill_score,
)
from app.config import get_settings

router = APIRouter(prefix="/api/gamification", tags=["gamification"])
settings = get_settings()


@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    await ensure_tower_fields(user["id"])
    profile = await get_gamification_profile(user["id"])
    return profile


@router.post("/record")
async def record_activity(
    activity_type: str,
    score: float = 0,
    category: str = None,
    skill: str = None,
    user=Depends(get_current_user),
):
    if activity_type not in ["interview", "resume", "aptitude", "coding", "system_design", "cover_letter", "question_bank"]:
        raise HTTPException(status_code=400, detail="Invalid activity type")

    result = await record_practice(user["id"], activity_type, score)

    if category and skill:
        await update_skill_score(user["id"], category, skill, score, score >= 7)

    return result


@router.get("/tower")
async def get_tower(user=Depends(get_current_user)):
    await ensure_tower_fields(user["id"])
    profile = await get_gamification_profile(user["id"])
    return {
        "level": profile["level"],
        "xp": profile.get("xp", 0),
        "xp_to_next": profile["xp_to_next_level"],
        "xp_for_current": profile["xp_for_current_level"],
        "title": profile["title"],
        "title_emoji": profile["title_emoji"],
        "wizard_outfit": profile["wizard_outfit"],
        "streak": profile.get("streak", 0),
        "streak_multiplier": profile["streak_multiplier"],
        "coins": profile.get("coins", 0),
        "stars_total": profile.get("stars_total", 0),
        "power_ups": profile.get("power_ups", {}),
        "current_boss": profile.get("current_boss"),
        "boss_level": profile.get("boss_level"),
        "bosses_defeated": profile.get("bosses_defeated", []),
        "streak_freezes": profile.get("streak_freezes", 0),
        "daily_goal_count": profile.get("daily_goal_count", 0),
        "daily_goal_target": profile.get("daily_goal_target", 5),
        "daily_goal_completed": profile.get("daily_goal_completed", False),
    }


@router.get("/tower/boss/{boss_level}")
async def get_boss(boss_level: int, user=Depends(get_current_user)):
    boss = BOSS_BATTLES.get(boss_level)
    if not boss:
        raise HTTPException(status_code=404, detail="No boss at this level")
    profile = await get_gamification_profile(user["id"])
    defeated = boss_level in (profile.get("bosses_defeated", []))
    return {**boss, "level": boss_level, "defeated": defeated}


@router.post("/tower/powerup/use")
async def use_power_up_endpoint(power_up_id: str, user=Depends(get_current_user)):
    try:
        result = await use_power_up(user["id"], power_up_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.post("/tower/powerup/buy")
async def buy_power_up_endpoint(power_up_id: str, user=Depends(get_current_user)):
    try:
        result = await buy_power_up(user["id"], power_up_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.get("/tower/powerups")
async def get_power_ups():
    return {"power_ups": POWER_UPS}


# ─── Streak Freeze ───

@router.get("/tower/streak-freeze")
async def streak_freeze_status(user=Depends(get_current_user)):
    return await get_streak_freeze_status(user["id"])


@router.post("/tower/streak-freeze/buy")
async def buy_streak_freeze_endpoint(user=Depends(get_current_user)):
    return await buy_streak_freeze(user["id"])


# ─── Daily Goal ───

@router.get("/tower/daily-goal")
async def daily_goal_progress(user=Depends(get_current_user)):
    return await get_daily_goal(user["id"])


@router.get("/tower/challenges")
async def get_challenges_endpoint(user=Depends(get_current_user)):
    return await get_challenges(user["id"])


@router.post("/tower/challenges/claim")
async def claim_reward(challenge_type: str, challenge_id: str, user=Depends(get_current_user)):
    if challenge_type not in ("weekly", "monthly"):
        raise HTTPException(status_code=400, detail="Type must be 'weekly' or 'monthly'")
    return await claim_challenge_reward(user["id"], challenge_type, challenge_id)


@router.get("/leaderboard")
async def leaderboard(limit: int = 10):
    return await get_leaderboard(limit)


@router.get("/badges")
async def all_badges():
    return {"badges": BADGES}


# Skill Assessment endpoints
@router.get("/skills")
async def get_skills(user=Depends(get_current_user)):
    return await get_skill_graph(user["id"])


@router.get("/skills/weak")
async def weak_areas(user=Depends(get_current_user), top_n: int = 5):
    return await get_weak_areas(user["id"], top_n)


@router.get("/skills/readiness")
async def readiness(company: str = None, user=Depends(get_current_user)):
    return await get_readiness_score(user["id"], company)
