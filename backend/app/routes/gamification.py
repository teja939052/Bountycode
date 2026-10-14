from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.responses import Response
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
    use_power_up,
    buy_power_up,
    get_daily_goal,
    get_streak_status,
    get_forest_state,
    BADGES,
    get_daily_login_calendar,
    claim_daily_login,
    get_achievement_chains,
    get_powerups,
    get_tower_challenges,
    claim_tower_challenge,
    get_startup_state,
    get_combo_state,
    get_league_state,
    get_daily_bonus_history,
    get_leaderboard_nearby,
    streak_freeze,
    streak_repair,
)
from app.services.skill_assessment import (
    get_skill_graph,
    get_weak_areas,
    update_skill_score,
)
from app.services.readiness_engine import compute_readiness
from app.services.response_cache import cached
from app.database import gamification_collection, users_collection

router = APIRouter(prefix="/api/v1/gamification", tags=["gamification"])
settings = get_settings()

VALID_ACTIVITY_TYPES = {
    "interview", "resume", "aptitude", "coding", "system_design",
    "question_bank",
}
VALID_CHALLENGE_TYPES = {"weekly", "monthly"}


@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    profile = await get_gamification_profile(user["id"])
    if profile and "_id" in profile:
        profile["id"] = str(profile.pop("_id"))
    return profile


@router.post("/profile/target-company")
async def set_target_company(
    payload: dict = Body(...),
    user=Depends(get_current_user),
):
    company = (payload.get("company") or "").strip()
    if not company:
        raise HTTPException(status_code=400, detail="company is required")
    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$set": {"target_company": company.lower()}},
        upsert=True,
    )
    # Mirror to the users doc: journey_engine and worlds.py read the target
    # from there. Best-effort (no upsert — never mint user docs from here).
    try:
        await users_collection.update_one(
            {"user_id": user["id"]},
            {"$set": {"target_company": company.lower()}},
        )
    except Exception:
        pass
    return {"success": True, "target_company": company.lower()}


@router.get("/profile/title-progression")
async def title_progression(user=Depends(get_current_user)):
    profile = await get_gamification_profile(user["id"])
    company = profile.get("target_company")
    if not company:
        return {"company": None, "bands": {}}
    return {
        "company": company,
        "bands": get_company_title_progression(company),
    }


@router.get("/readiness")
async def readiness_score(user=Depends(get_current_user)):
    profile = await get_gamification_profile(user["id"])
    target_company = profile.get("target_company")
    from app.services.readiness_engine import calculate_company_readiness_breakdown
    result = await calculate_company_readiness_breakdown(user["id"], {}, target_company)
    return result


@router.get("/readiness/simulate")
async def readiness_simulate(
    company: str = Query(..., description="Target company id, e.g. tcs"),
    role: str = Query("sde"),
    date: Optional[str] = Query(None, description="ISO assessment date"),
    daily_minutes: Optional[int] = Query(None, ge=5, le=600),
    user=Depends(get_current_user),
):
    """Can-I-crack simulator: current readiness + honest preparation estimate.

    Read-only composite over the readiness breakdown and onboarding mission
    data. Hours and gains are labeled estimates from a fixed transparent
    rate — never a placement promise.
    """
    from app.routes.onboarding import _normalize_company as _canon
    from app.services.readiness_engine import (
        calculate_company_readiness_breakdown,
        CATEGORY_WEIGHTS,
    )
    from app.services.company_registry import get_readiness_profiles
    from datetime import datetime as _dt, timezone as _tz
    import math as _math

    canon = _canon(company)
    breakdown = await calculate_company_readiness_breakdown(user["id"], {}, canon)
    comp = (breakdown.get("per_company_scores") or {}).get(canon, {})
    score = float(comp.get("score", breakdown.get("overall_readiness", 0) or 0))
    domains = breakdown.get("domain_scores", {}) or {}

    # Mission inputs: explicit params win, onboarding values fill gaps.
    days_remaining = None
    minutes = daily_minutes
    try:
        from app.database import users_collection as _users
        from bson import ObjectId as _ObjectId
        try:
            _udoc = await _users.find_one({"_id": _ObjectId(user["id"])}) or {}
        except Exception:
            _udoc = {}
        _ob = _udoc.get("onboarding", {}) or {}
        if minutes is None and isinstance(_ob.get("daily_minutes"), (int, float)):
            minutes = int(_ob["daily_minutes"])
        iso = (date or _ob.get("placement_date") or "").strip()
        if iso:
            _target = _dt.fromisoformat(iso.replace("Z", "+00:00"))
            if _target.tzinfo is None:
                _target = _target.replace(tzinfo=_tz.utc)
            days_remaining = max(0, (_target.date() - _dt.now(_tz.utc).date()).days)
    except Exception:
        pass

    READY_AT = 70.0
    HOURS_PER_POINT = 1.5  # transparent planning rate, shown to the student
    gap = max(0.0, READY_AT - score)
    hours_needed = round(gap * HOURS_PER_POINT, 1)
    days_needed = (
        int(_math.ceil(hours_needed * 60 / minutes)) if minutes and gap > 0 else 0
    )

    if score >= READY_AT:
        verdict, verdict_detail = "ready", "At or above the readiness bar. Hold it with revision + mocks."
    elif days_remaining is None:
        verdict, verdict_detail = "unknown-date", "Set your assessment date to get a day plan."
    elif days_needed <= days_remaining:
        verdict, verdict_detail = "on-track", "Fits your available days at your daily pace."
    elif days_needed <= int(days_remaining * 1.3) + 1:
        verdict, verdict_detail = "tight", "Fits only with extra daily time or sharper focus."
    else:
        verdict, verdict_detail = "needs-more-time", "Needs more days or more minutes per day."

    _profiles = get_readiness_profiles()
    weights = (_profiles.get(canon, {}).get("match_weights") or CATEGORY_WEIGHTS)
    wsum = sum(weights.get(d, 0) for d in domains) or 1.0
    ranked = sorted(
        ((d, max(0.0, READY_AT - float(v or 0))) for d, v in domains.items()),
        key=lambda kv: kv[1] * weights.get(kv[0], 0),
        reverse=True,
    )
    impact = [
        {
            "domain": d,
            "current": round(float(domains[d] or 0), 1),
            "potential_gain": round(min(g, hours_needed * (weights.get(d, 0) / wsum) / HOURS_PER_POINT), 1),
        }
        for d, g in ranked[:3] if g > 0
    ]

    split = []
    if minutes:
        order = [r[0] for r in ranked[:2]]
        shares = [0.4, 0.3, 0.3]
        labels = (
            [f"Repair {order[0]}" if len(order) > 0 else "Repair weakest",
             f"Build {order[1]}" if len(order) > 1 else "Build next",
             "Revise + SRS"]
        )
        split = [
            {"focus": label, "minutes": int(round(minutes * share))}
            for label, share in zip(labels, shares)
        ]

    return {
        "company": canon,
        "role": role,
        "date": date,
        "days_remaining": days_remaining,
        "daily_minutes": minutes,
        "current": {
            "overall_readiness": breakdown.get("overall_readiness"),
            "company_score": round(score, 1),
            "readiness_level": breakdown.get("readiness_level"),
            "target_company": breakdown.get("target_company"),
        },
        "projection": {
            "hours_needed": hours_needed,
            "days_needed": days_needed,
            "verdict": verdict,
            "verdict_detail": verdict_detail,
            "hours_per_point": HOURS_PER_POINT,
            "note": "Planning estimate from current evidence, not a placement promise.",
        },
        "highest_impact": impact,
        "daily_split": split,
        "blockers": breakdown.get("blockers", []),
    }


@router.get("/forest")
async def forest_state(user=Depends(get_current_user)):
    """Nature-themed journey state: current zone, tree stage, sunlight (Diamonds),
    watering (streak), seeds (badges) and the next seasonal storm."""
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

    # Idempotency guard: prevent double-credit of Diamonds/rewards if the same activity
    # is recorded twice (retries, double-clicks, replay). The key is bound to the
    # user + the full activity payload, so legitimately different activities are
    # never collapsed. Fail-open on manager errors so Diamonds recording never breaks.
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

    role = user.get("role") or user.get("target_role") or "sde"
    result = await record_practice(user["id"], activity_type, score, metadata, role=role)

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
    profile = await get_gamification_profile(user["id"])
    return {
        "level": profile["level"],
        "diamonds": profile.get("diamonds", 0),
        "xp_to_next": profile.get("xp_to_next_level", 0),
        "xp_for_current": profile.get("xp_for_current_level", 0),
        "title": profile.get("title", ""),
        "title_emoji": profile.get("title_emoji", ""),
        "streak": profile.get("streak", 0),
        "streak_multiplier": profile.get("streak_multiplier", 1),
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
    if not boss:
        raise HTTPException(status_code=404, detail="No boss at this level")
    profile = await get_gamification_profile(user["id"])
    defeated = boss_level in (profile.get("bosses_defeated", []))


@router.post("/tower/boss/{boss_level}/defeat")
async def defeat_boss(boss_level: int, score: int = Query(..., ge=0), user=Depends(get_current_user)):
    from app.services.gamification import check_boss_eligibility
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


@router.get("/tower/daily-goal")
async def daily_goal_progress(user=Depends(get_current_user)):
    return await get_daily_goal(user["id"])


@router.get("/leaderboard")
@cached(ttl=120, key_prefix="gamification")
async def leaderboard(
    limit: int = Query(default=10, ge=1, le=100),
    timeframe: str = Query(default="all", description="all|weekly|monthly"),
):
    return await get_leaderboard(limit, timeframe)


@router.get("/leaderboard/league")
@cached(ttl=120, key_prefix="gamification")
async def league_leaderboard(
    timeframe: str = Query(default="weekly", description="all|weekly|monthly"),
    user=Depends(get_current_user),
):
    """Level-band league: only users within the caller's level band."""
    return await get_league_leaderboard(user["id"], timeframe=timeframe)


@router.get("/leaderboard/me")
async def my_leaderboard_position(
    timeframe: str = Query(default="weekly", description="all|weekly|monthly"),
    user=Depends(get_current_user),
):
    """The caller's own rank + Diamonds gap to the next rank up.

    Powers the "Diamonds to next rank" UI for users outside the top 50. All
    numbers derive from the same period counters the boards sort on —
    no client math, no second interpretation.
    """
    from app.database import gamification_collection
    tf = (timeframe or "weekly").lower()
    field = {"weekly": "weekly_league_xp", "monthly": "monthly_league_xp"}.get(tf, "diamonds")
    doc = await gamification_collection.find_one({"user_id": user["id"]}) or {}
    mine = int(doc.get(field, 0) or 0)
    above = await gamification_collection.count_documents({field: {"$gt": mine}})
    total = await gamification_collection.count_documents({})
    nxt = await gamification_collection.find({field: {"$gt": mine}}).sort(field, 1).limit(1).to_list(1)
    next_xp = int((nxt[0].get(field, 0) if nxt else 0) or 0)
    return {
        "timeframe": tf,
        "rank": above + 1,
        "of": max(total, 1),
        "period_xp": mine,
        "next_up": {"xp_gap": max(0, next_xp - mine), "target_xp": next_xp} if nxt else None,
    }


@router.get("/streak/status")
async def streak_status(user=Depends(get_current_user)):
    """Lean login-time payload used to surface a streak-at-risk nudge."""
    return await get_streak_status(user["id"])


@router.get("/badges")
@cached(ttl=3600, key_prefix="gamification")
async def all_badges():
    return {"badges": BADGES}


def _worlds_cleared(completed: dict) -> tuple[int, int]:
    """Count fully-cleared voyage worlds from persisted evidence.

    Single source of truth reused from routes.worlds (same gate the map
    and the attempt endpoints read): a world counts when done >= total.
    """
    from app.data.worlds_data import WORLD_REGISTRY
    from app.routes.worlds import world_progress
    total = len(WORLD_REGISTRY)
    cleared = 0
    for wid, world in WORLD_REGISTRY.items():
        prog = world_progress(wid, completed)
        if prog["total"] and prog["done"] >= prog["total"]:
            cleared += 1
    return cleared, total


@router.get("/badge/{user_id}.svg", response_class=Response)
async def voyage_badge(user_id: str):
    """Portable rank badge (CodeWars-style embed).

    Public on purpose: embeds on GitHub READMEs/resumes can't send auth.
    Shows only rank/level/worlds/streak — no name, email, or user id in
    the image. All values derive from real persisted progress, so the
    badge is a credential, not decoration.
    """
    from xml.sax.saxutils import escape
    from app.services.gamification import _calculate_level
    from app.services.gamification_core import voyage_rank_for_level
    # Raw read on purpose: get_gamification_profile auto-creates profiles,
    # and a public badge URL must never mint docs for arbitrary ids.
    doc = await gamification_collection.find_one({"user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="No voyage found for user")
    level = _calculate_level(doc.get("diamonds", 0))
    rank, emoji, _tier = voyage_rank_for_level(level)
    completed = doc.get("completed_competencies", {}) or {}
    cleared, total = _worlds_cleared(completed)
    rank = escape(str(rank))
    emoji = escape(str(emoji))
    streak = int(doc.get("streak", 0))
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="340" height="96" role="img"'
        ' aria-label="BountyCode voyage rank">'
        '<rect width="340" height="96" rx="14" fill="#0b1f2a"/>'
        '<rect x="1" y="1" width="338" height="94" rx="13" fill="none" stroke="#e8b64a" stroke-opacity="0.45"/>'
        f'<text x="18" y="34" font-size="26">{emoji}</text>'
        f'<text x="52" y="33" font-family="Verdana,sans-serif" font-size="17" font-weight="bold" fill="#f6d98a">{rank}</text>'
        f'<text x="52" y="54" font-family="Verdana,sans-serif" font-size="12" fill="#9fb3c8">BountyCode voyage · Lv {level}</text>'
        f'<text x="18" y="78" font-family="Verdana,sans-serif" font-size="12" fill="#e8b64a">{cleared}/{total} worlds cleared · {streak}-day streak</text>'
        "</svg>"
    )
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=300"},
    )


# Skill Assessment endpoints
@router.get("/skills")
async def get_skills(user=Depends(get_current_user)):
    return await get_skill_graph(user["id"])


@router.get("/skills/weak")
async def weak_areas(user=Depends(get_current_user), top_n: int = Query(default=5, ge=1, le=20)):
    return await get_weak_areas(user["id"], top_n)


@router.get("/skills/readiness")
async def readiness(company: str = None, user=Depends(get_current_user)):
    return await compute_readiness(user["id"], company)


@router.get("/daily-login")
async def daily_login_calendar(
    days: int = Query(default=7, ge=1, le=30),
    user=Depends(get_current_user),
):
    return await get_daily_login_calendar(user["id"], days)


@router.post("/daily-login/claim")
async def claim_daily_login_endpoint(user=Depends(get_current_user)):
    return await claim_daily_login(user["id"])


@router.get("/achievement-chains")
async def achievement_chains(user=Depends(get_current_user)):
    return await get_achievement_chains(user["id"])


@router.get("/startup")
async def startup_state(user=Depends(get_current_user)):
    return await get_startup_state(user["id"])


@router.get("/combo")
async def combo_state(user=Depends(get_current_user)):
    return await get_combo_state(user["id"])


@router.get("/league")
async def league_state(user=Depends(get_current_user)):
    return await get_league_state(user["id"])


@router.get("/tower/powerups")
async def tower_powerups(user=Depends(get_current_user)):
    return await get_powerups(user["id"])


@router.get("/tower/challenges")
async def tower_challenges(user=Depends(get_current_user)):
    return await get_tower_challenges(user["id"])


@router.post("/tower/challenges/claim")
async def claim_tower_challenge_endpoint(
    challenge_type: str = Query(...),
    challenge_id: str = Query(...),
    user=Depends(get_current_user),
):
    return await claim_tower_challenge(user["id"], challenge_type, challenge_id)


@router.post("/tower/streak-freeze")
async def tower_streak_freeze(user=Depends(get_current_user)):
    return await streak_freeze(user["id"])


@router.post("/tower/streak-freeze/buy")
async def buy_streak_freeze(user=Depends(get_current_user)):
    return await streak_freeze(user["id"])


@router.post("/tower/streak-freeze/auto-apply")
async def auto_apply_streak_freeze(user=Depends(get_current_user)):
    return await streak_freeze(user["id"])


@router.post("/tower/streak-repair")
async def tower_streak_repair(user=Depends(get_current_user)):
    return await streak_repair(user["id"])


@router.post("/tower/streak-repair/buy")
async def buy_streak_repair(user=Depends(get_current_user)):
    return await streak_repair(user["id"])


@router.post("/daily-bonus")
async def claim_daily_bonus(user=Depends(get_current_user)):
    return await get_daily_bonus(user["id"])


@router.get("/daily-bonus/history")
async def daily_bonus_history(
    limit: int = Query(default=30, ge=1, le=100),
    user=Depends(get_current_user),
):
    return await get_daily_bonus_history(user["id"], limit)


@router.get("/leaderboard/nearby")
async def nearby_leaderboard(
    limit: int = Query(default=10, ge=1, le=100),
    user=Depends(get_current_user),
):
    return await get_leaderboard_nearby(limit)
