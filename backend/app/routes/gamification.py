from fastapi import APIRouter, Depends, HTTPException, Query, Body
from app.middleware.auth import get_current_user
from app.config import get_settings
from app.services.idempotency import (
    get_idempotency_manager,
    IdempotencyStatus,
)
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
    buy_streak_repair,
    get_streak_freeze_status,
    STREAK_REPAIR_COST,
    apply_streak_freeze_on_login,
    get_league_status,
    get_daily_goal,
    claim_daily_bonus,
    get_daily_bonus_history,
    get_nearby_leaderboard,
    get_streak_status,
    get_forest_state,
    alias_boss_with_storm,
    FOREST_ZONES,
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
from app.services.response_cache import cached

router = APIRouter(prefix="/api/v1/gamification", tags=["gamification"])
settings = get_settings()

VALID_ACTIVITY_TYPES = {
    "interview", "resume", "aptitude", "coding", "system_design",
    "cover_letter", "question_bank",
}
VALID_CHALLENGE_TYPES = {"weekly", "monthly"}


@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    await ensure_tower_fields(user["id"])
    profile = await get_gamification_profile(user["id"])
    return profile


@router.get("/forest")
async def forest_state(user=Depends(get_current_user)):
    """Nature-themed journey state: current zone, tree stage, sunlight (XP),
    watering (streak), seeds (badges) and the next seasonal storm."""
    await ensure_tower_fields(user["id"])
    return await get_forest_state(user["id"])


@router.post("/record")
async def record_activity(
    activity_type: str = Query(..., min_length=1, max_length=32),
    score: float = Query(default=0, ge=0, le=100),
    category: str = Query(default=None, max_length=64),
    skill: str = Query(default=None, max_length=64),
    metadata: dict = Body(default=None),
    user=Depends(get_current_user),
):
    if activity_type not in VALID_ACTIVITY_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid activity type. Must be one of: {', '.join(sorted(VALID_ACTIVITY_TYPES))}",
        )

    # Idempotency guard: prevent double-credit of XP/rewards if the same activity
    # is recorded twice (retries, double-clicks, replay). The key is bound to the
    # user + the full activity payload, so legitimately different activities are
    # never collapsed. Fail-open on manager errors so XP recording never breaks.
    idem = get_idempotency_manager()
    operation_data = {
        "activity_type": activity_type,
        "score": score,
        "category": category,
        "skill": skill,
        "metadata": metadata or {},
    }
    try:
        idempotency_key = await idem.create_key(
            user["id"], "xp_gain", operation_data
        )
        cached = await idem.get_operation_result(idempotency_key)
        if cached and cached.get("status") == IdempotencyStatus.SUCCESS:
            return cached.get("result", {"success": True, "deduplicated": True})
    except Exception:
        idempotency_key = None
        logger = __import__("logging").getLogger("app.routes.gamification")
        logger.warning("idempotency check failed for record_activity (fail-open)")

    result = await record_practice(user["id"], activity_type, score, metadata)

    if category and skill:
        await update_skill_score(user["id"], category, skill, score, score >= 7)

    if idempotency_key:
        try:
            await idem.record_operation(
                idempotency_key,
                user["id"],
                "xp_gain",
                IdempotencyStatus.SUCCESS,
                result,
            )
        except Exception:
            pass

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
        "streak": profile.get("streak", 0),
        "streak_multiplier": profile["streak_multiplier"],
        "coins": profile.get("coins", 0),
        "stars_total": profile.get("stars_total", 0),
        "power_ups": profile.get("power_ups", {}),
        "double_xp_expires": profile.get("double_xp_expires"),
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
    return {**alias_boss_with_storm(boss, boss_level), "level": boss_level, "defeated": defeated}


@router.post("/tower/boss/{boss_level}/defeat")
async def defeat_boss(boss_level: int, score: int = Query(..., ge=0), user=Depends(get_current_user)):
    from app.services.gamification import check_boss_eligibility
    boss = BOSS_BATTLES.get(boss_level)
    if not boss:
        raise HTTPException(status_code=404, detail="No boss at this level")
    profile = await get_gamification_profile(user["id"])
    if boss_level in (profile.get("bosses_defeated") or []):
        return {"defeated": True, "already_defeated": True}
    if score < boss.get("required_score", 0):
        return {"defeated": False, "reason": "Score too low", "required": boss.get("required_score", 0), "score": score}
    result = await check_boss_eligibility(user["id"], score, "boss_battle")
    if result:
        return {"defeated": True, **result}
    return {"defeated": False}


@router.post("/tower/powerup/use")
async def use_power_up_endpoint(
    power_up_id: str = Query(..., min_length=1, max_length=32),
    user=Depends(get_current_user),
):
    try:
        result = await use_power_up(user["id"], power_up_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.post("/tower/powerup/buy")
async def buy_power_up_endpoint(
    power_up_id: str = Query(..., min_length=1, max_length=32),
    user=Depends(get_current_user),
):
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


@router.post("/tower/streak-freeze/auto-apply")
async def auto_apply_streak_freeze(user=Depends(get_current_user)):
    """Login-time streak protection. Consumes a freeze if the user missed a day
    but opened the app within the recovery window, so the habit survives."""
    await ensure_tower_fields(user["id"])
    return await apply_streak_freeze_on_login(user["id"])


@router.get("/tower/streak-repair")
async def streak_repair_status(user=Depends(get_current_user)):
    """Status for the Streak Repair item: costs coins (or a free streak freeze).

    Free users get FREE_TIER_STREAK_REPAIRS/month; Pro/Lifetime unlimited.
    """
    profile = await get_gamification_profile(user["id"])
    freezes = profile.get("streak_freezes", 0)
    plan = user.get("plan", "free")
    if plan in ("pro", "lifetime"):
        quota = None
        remaining = None
    else:
        quota = getattr(get_settings(), "FREE_TIER_STREAK_REPAIRS", 1)
        used = user.get("streak_repairs_used", 0)
        remaining = max(0, quota - used)
    return {
        "cost": STREAK_REPAIR_COST,
        "streak_freezes": freezes,
        "can_repair_with_freeze": freezes > 0,
        "can_repair_with_coins": True,
        "plan": plan,
        "monthly_quota": quota,
        "remaining": remaining,
    }


@router.post("/tower/streak-repair/buy")
async def buy_streak_repair_endpoint(user=Depends(get_current_user)):
    """Repair a streak broken today (Duolingo Streak Repair). Uses a streak
    freeze if available, otherwise deducts coins."""
    await ensure_tower_fields(user["id"])
    return await buy_streak_repair(user["id"], user)


# ─── Weekly Leagues ───

@router.get("/league")
async def league_status(user=Depends(get_current_user)):
    return await get_league_status(user["id"])


@router.get("/startup")
async def startup_state(user=Depends(get_current_user)):
    """Lightweight login-time payload: streak protection + level for the evolve
    animation. Called once on app load. Does not mutate XP, only protects the
    streak via an already-held freeze (no-op if none needed)."""
    await ensure_tower_fields(user["id"])
    profile = await get_gamification_profile(user["id"])
    protection = await apply_streak_freeze_on_login(user["id"])
    league = await get_league_status(user["id"])
    return {
        "level": profile.get("level", 1),
        "xp": profile.get("xp", 0),
        "title": profile.get("title"),
        "title_emoji": profile.get("title_emoji"),
        "streak": profile.get("streak", 0),
        "longest_streak": profile.get("longest_streak", 0),
        "streak_freezes": profile.get("streak_freezes", 0),
        "streak_protected": protection.get("applied", False),
        "streak_protect_message": protection.get("message", ""),
        "league": league,
    }


# ─── Daily Goal ───

@router.get("/tower/daily-goal")
async def daily_goal_progress(user=Depends(get_current_user)):
    return await get_daily_goal(user["id"])


@router.get("/tower/challenges")
async def get_challenges_endpoint(user=Depends(get_current_user)):
    return await get_challenges(user["id"])


@router.post("/tower/challenges/claim")
async def claim_reward(
    challenge_type: str = Query(..., min_length=1, max_length=16),
    challenge_id: str = Query(..., min_length=1, max_length=64),
    user=Depends(get_current_user),
):
    if challenge_type not in VALID_CHALLENGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Type must be one of: {', '.join(sorted(VALID_CHALLENGE_TYPES))}",
        )
    return await claim_challenge_reward(user["id"], challenge_type, challenge_id)


@router.get("/leaderboard")
@cached(ttl=120, key_prefix="gamification")
async def leaderboard(limit: int = Query(default=10, ge=1, le=100)):
    return await get_leaderboard(limit)


@router.post("/daily-bonus")
async def daily_bonus(user=Depends(get_current_user)):
    return await claim_daily_bonus(user["id"])


@router.get("/daily-bonus/history")
async def daily_bonus_history(
    limit: int = Query(default=30, ge=1, le=90),
    user=Depends(get_current_user),
):
    return await get_daily_bonus_history(user["id"], limit)


@router.get("/leaderboard/nearby")
async def nearby_leaderboard(
    radius: int = Query(default=5, ge=1, le=20),
    limit: int = Query(default=10, ge=3, le=40),
    user=Depends(get_current_user),
):
    """Relative leaderboard: players near *your* rank (not the global top).

    Reduces discouragement for mid/low-ranked users (per gamification research
    on absolute leaderboards) while keeping a sense of direct competition.
    """
    return await get_nearby_leaderboard(user["id"], radius, limit)


@router.get("/streak/status")
async def streak_status(user=Depends(get_current_user)):
    """Lean login-time payload used to surface a streak-at-risk nudge."""
    return await get_streak_status(user["id"])


@router.get("/badges")
@cached(ttl=3600, key_prefix="gamification")
async def all_badges():
    return {"badges": BADGES}


# Skill Assessment endpoints
@router.get("/skills")
async def get_skills(user=Depends(get_current_user)):
    return await get_skill_graph(user["id"])


@router.get("/skills/weak")
async def weak_areas(user=Depends(get_current_user), top_n: int = Query(default=5, ge=1, le=20)):
    return await get_weak_areas(user["id"], top_n)


@router.get("/skills/readiness")
async def readiness(company: str = None, user=Depends(get_current_user)):
    return await get_readiness_score(user["id"], company)
