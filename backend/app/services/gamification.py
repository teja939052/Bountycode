"""Gamification service module.

This module contains the complete gamification system including:
- Level/Diamonds/streak math and progression
- Tower titles, boss battles
- Power-ups, challenges, badges
- Daily bonuses, mystery boxes
- Practice recording and profile management

Extracted split (behavioral no-op):
- gamification_core.py: pure constants (titles, bosses, zones, power-ups,
  streak multipliers) and pure math helpers (Diamonds, level, stars, multipliers).
  All are re-exported below, so consumers are unchanged.
"""
from datetime import datetime, timezone, timedelta
from app.database import users_collection, gamification_collection, get_client
from bson import ObjectId
import logging
from app.services.usage import can_use_feature, mark_feature_used

logger = logging.getLogger(__name__)

# Activity types that auto-record a milestone on the placement timeline.

from app.services.gamification_core import (
    TOWER_TITLES, BOSS_BATTLES, FOREST_ZONES, SEASONAL_STORMS, POWER_UPS,
    STREAK_MULTIPLIERS, WEEKLY_CHALLENGES, MONTHLY_CHALLENGES, BADGES,
    ACTIVITY_COUNTER_FIELD, BADGE_CONDITIONS, badge_condition_met,
    VOYAGE_RANKS, voyage_rank_for_level, normalize_badge_ids,
    _calculate_xp, _calculate_level, xp_for_level,
    xp_for_next_level, get_title_for_level, forest_zone_for_level,
    seasonal_storm_for_boss, alias_boss_with_storm, compute_forest_state,
    calculate_streak_multiplier, calculate_stars, get_xp_with_multiplier,
    get_role_xp_multiplier, get_level_color, get_role_badge_priority,
    get_role_champion_title, get_company_title_progression,
    calculate_proof, calculate_bounty, proof_for_xp, bounty_for_coins,
    PROOF_BY_ACTIVITY, BOUNTY_BY_ACTIVITY,
)


async def get_forest_state(user_id: str) -> dict:
    """Lightweight forest-journey payload for a user."""
    profile = await get_gamification_profile(user_id)
    if "forest_state" in profile:
        return profile["forest_state"]
    return compute_forest_state(
        level=profile.get("level", 1),
        diamonds=profile.get("diamonds", 0),
        streak=profile.get("streak", 0),
        badges=profile.get("badges", []),
        bosses_defeated=profile.get("bosses_defeated", []),
    )


async def initialize_gamification(user_id: str):
    """Initialize gamification profile for a new user."""
    profile = {
        "user_id": user_id,
        "diamonds": 0,
        "level": 1,
        "streak": 0,
        "longest_streak": 0,
        "last_practice_date": None,
        "badges": [],
        "achievements": [],
        "total_interviews": 0,
        "total_resumes": 0,
        "total_aptitude": 0,
        "total_coding": 0,
        "total_system_design": 0,
        "target_company": None,
        "proof": 0,
        "bounty": 0,
        # Per-activity counters for power-up / perfect-score badge families
        # (incremented by use_power_up / record_practice respectively).
        "total_powerups_used": 0,
        "total_perfect_scores": 0,
        # Tower fields
        "stars_total": 0,
        "stars_per_problem": {},
        "coins": 0,
        "power_ups": {
            "extra_time": 0, "hint_reveal": 0, "retry": 0,
            "double_xp": 0, "skip_boss": 0, "show_answer": 0,
            "speed_boost": 0, "shield": 0, "x2_coins": 0,
            "auto_save": 0, "night_mode": 0, "focus_mode": 0,
        },
        "bosses_defeated": [],
        "first_solve_today": None,
        "weekly_challenges": [],
        "monthly_challenges": [],
        "weekly_league_xp": 0,
        "weekly_league_week": None,
        "current_combo": 0,
        "max_combo": 0,
        "last_combo_at": None,
        "daily_login_streak": 0,
        "last_daily_login_date": None,
        "achievements": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    await gamification_collection.insert_one(profile)
    return profile


async def record_practice(user_id: str, activity_type: str, score: float = 0, metadata: dict = None, role: str = None, activity_id: str = None):
    """Record a practice activity and update gamification with tower mechanics.

    LAW: this is the ONLY writer of diamonds/coins/stars/streak/combo/badges/
    weekly_league_xp. Callers pass a 0-10 pedagogical score (never Diamonds) and a
    canonical activity_type; world/level/language travel in metadata.

    Every award appends one immutable gamification_events row (inputs +
    outputs + policy version) so profile.diamonds == sum(ledger) is checkable.
    activity_id is caller-supplied when the caller has a stable identity
    for the attempt (else a uuid); endpoint-level atomic claims remain the
    dedupe mechanism (see worlds complete, challenge claims).
    """
    import uuid as _uuid
    event_id = _uuid.uuid4().hex
    act_id = activity_id or event_id
    if role is None:
        try:
            from bson import ObjectId
            from app.database import users_collection
            user_doc = await users_collection.find_one({"_id": ObjectId(user_id)})
            role = (user_doc.get("role") or user_doc.get("target_role") or "sde") if user_doc else "sde"
        except Exception:
            role = "sde"
    now = datetime.now(timezone.utc)
    today = now.date()

    # Score normalization: the canonical contract is 0-10, but several
    # callers historically pass 0-100 (aptitude percent, coding percent).
    # Values >10 are treated as percent and scaled — otherwise every such
    # caller silently mints perfect bonuses and 3 stars for partial work
    # (the daily_challenge class of bug). Badge checks below keep the RAW
    # caller scale: they are tuned per activity (e.g. aptitude_perfect>=100).
    try:
        _score_num = float(score or 0)
    except (TypeError, ValueError):
        _score_num = 0.0
    score10 = round(_score_num / 10, 1) if _score_num > 10 else round(_score_num, 1)

    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    # Ensure tower fields exist (migration for existing users)
    tower_defaults = {
        "stars_total": 0, "coins": 0,
        "power_ups": {k: 0 for k in POWER_UPS},
        "bosses_defeated": [],
        "first_solve_today": None,
        "weekly_challenges": [], "monthly_challenges": [],
        "streak_freezes": 1,
        "daily_goal_count": 0,
        "daily_goal_target": 5,
        "daily_goal_date": None,
        "current_combo": 0,
        "max_combo": 0,
        "last_combo_at": None,
        "daily_login_streak": 0,
        "last_daily_login_date": None,
        "achievements": [],
        # Lazy-migrated counter seed for existing profiles (the $inc below
        # creates them anyway; seeding keeps them visible in get_gamification_profile).
        "total_powerups_used": 0,
        "total_perfect_scores": 0,
    }
    missing = {k: v for k, v in tower_defaults.items() if k not in profile}
    if missing:
        await gamification_collection.update_one({"user_id": user_id}, {"$set": missing})
        profile.update(missing)

    # Capture the pre-activity streak for milestone-chest detection (the
    # profile object is re-read with the *new* streak after the writes below).
    old_streak = profile.get("streak", 0)

    # Update streak — with streak freeze support
    last_date = profile.get("last_practice_date")
    streak_freezes = profile.get("streak_freezes", 0)
    streak_frozen_today = False

    if last_date:
        last_date = last_date.date() if isinstance(last_date, datetime) else last_date
        days_diff = (today - last_date).days
        if days_diff == 1:
            new_streak = profile.get("streak", 0) + 1
        elif days_diff == 0:
            new_streak = profile.get("streak", 0)
        elif days_diff == 2 and streak_freezes > 0:
            # Streak freeze: missed 1 day, use freeze to preserve streak
            new_streak = profile.get("streak", 0) + 1
            streak_freezes -= 1
            streak_frozen_today = True
        else:
            new_streak = 1
    else:
        new_streak = 1

    longest_streak = max(profile.get("longest_streak", 0), new_streak)

    # First solve of day?
    first_solve = profile.get("first_solve_today")
    is_first_today = False
    if first_solve:
        first_date = first_solve.date() if isinstance(first_solve, datetime) else first_solve
        is_first_today = first_date != today
    else:
        is_first_today = True

    # Update daily goal
    daily_goal_date = profile.get("daily_goal_date")
    if daily_goal_date:
        dg_date = daily_goal_date.date() if isinstance(daily_goal_date, datetime) else daily_goal_date
        if dg_date != today:
            daily_goal_count = 1
        else:
            daily_goal_count = profile.get("daily_goal_count", 0) + 1
    else:
        daily_goal_count = 1

    # Combo tracking: rapid-fire activities multiply Diamonds
    # Mongo returns naive datetimes (tz_aware=False driver default) while
    # `now` is aware — normalize before subtracting, or every comparison
    # raises TypeError into the bare except and combo silently never grows.
    last_combo_at = _naive_utc(profile.get("last_combo_at"))
    current_combo = profile.get("current_combo", 0)
    max_combo = profile.get("max_combo", 0)
    if last_combo_at:
        try:
            combo_delta = (_naive_utc(now) - last_combo_at).total_seconds()
            if combo_delta < COMBO_WINDOW_SECONDS:
                current_combo += 1
            else:
                current_combo = 1
        except Exception:
            current_combo = 1
    else:
        current_combo = 1
    max_combo = max(max_combo, current_combo)
    combo_mult = _combo_multiplier(current_combo)

    # Calculate Diamonds with multiplier (normalized 0-10 score)
    base_xp = _calculate_xp(activity_type, score10, role=role)
    xp_gained = get_xp_with_multiplier(base_xp, new_streak, is_first_today)

    # Calculate stars (normalized 0-10 score)
    time_taken = metadata.get("time_taken") if metadata else None
    stars = calculate_stars(score10, time_taken)

    # Coins earned
    coins_earned = 10 + (stars * 5)  # 15-25 coins per activity

    # Proof/Bounty: earned alongside Diamonds/Coins but never spent on
    # power-ups. Proof = mastery signal, Bounty = cosmetic currency.
    proof_earned = calculate_proof(activity_type)
    bounty_earned = calculate_bounty(activity_type)

    # Apply active Double Diamonds power-up (time-limited, set via use_power_up)
    dxp_expires = profile.get("double_xp_expires")
    dxp_active = False
    if dxp_expires:
        try:
            exp_dt = datetime.fromisoformat(str(dxp_expires))
            if exp_dt > now:
                dxp_active = True
                xp_gained = int(xp_gained * 2)
                coins_earned = int(coins_earned * 2)
        except (ValueError, TypeError):
            pass

    # Apply combo multiplier
    if combo_mult > 1.0:
        xp_gained = int(xp_gained * combo_mult)
        coins_earned = int(coins_earned * combo_mult)

    # Performance-linked bonus (NO RNG — deterministic skill signals only).
    # Replaces the old 5% random "critical hit": every bonus must tell a
    # story (independent solve / precise solve), never "you got lucky".
    # See BOUNTYCODE_GAME_ENGINE_V2.md §8.
    hint_used = bool((metadata or {}).get("used_hint") or (metadata or {}).get("hint_used"))
    try:
        time_num = float(time_taken) if time_taken is not None else None
    except (TypeError, ValueError):
        time_num = None
    # Precision: solved quickly AND correctly (≤5 min on a problem activity).
    is_quick = time_num is not None and 0 <= time_num <= 300
    precision_hit = score10 >= 9 and is_quick
    # Independent: correct without a hint consumed.
    independent_hit = not hint_used and score10 >= 8
    performance_mult = 1.0
    performance_reasons = []
    if precision_hit:
        performance_mult *= 1.25
        performance_reasons.append("precision")
    elif independent_hit:
        performance_mult *= 1.5
        performance_reasons.append("independent")
    if performance_mult > 1.0:
        xp_gained = int(xp_gained * performance_mult)
        coins_earned = int(coins_earned * performance_mult)
    critical_hit = False
    critical_bonus = 0

    # Update counters — canonical activity counter (see ACTIVITY_COUNTER_FIELD
    # in gamification_core): the historical f"total_{activity_type}s" produced
    # total_aptitudes/total_codings that no reader consumed, while badges,
    # models, tiers, placement_engine and daily_drill all read the singular
    # canonical fields. Writing the canonical field keeps every counter-based
    # badge (aptitude/coding/system_design families) actually earnable.
    counter_field = ACTIVITY_COUNTER_FIELD.get(activity_type, f"total_{activity_type}s")
    week_id = _league_week_id()
    # ISO-week lazy reset (UTC), as its OWN write before the award below:
    # same-update $set+$inc ordering on one field is not something to rely
    # on. The $ne filter collapses concurrent resets; without this reset,
    # "weekly" is all-time accumulation and every rank from it is a lie.
    # Last week's snapshot is frozen for the recap screen.
    if profile.get("weekly_league_week") != week_id:
        await gamification_collection.update_one(
            {"user_id": user_id, "weekly_league_week": {"$ne": week_id}},
            {"$set": {
                "weekly_league_week": week_id,
                "weekly_league_xp": 0,
                "weekly_league_last": {
                    "week": profile.get("weekly_league_week"),
                    "diamonds": profile.get("weekly_league_xp", 0),
                    "rank": profile.get("weekly_league_rank"),
                },
            }},
        )
    # Monthly league mirrors the weekly pattern (YYYY-MM key). The
    # leaderboard's monthly tab sorts on this; without it "monthly" would
    # silently show all-time exactly like the old weekly lie.
    month_id = now.strftime("%Y-%m")
    if profile.get("monthly_league_month") != month_id:
        await gamification_collection.update_one(
            {"user_id": user_id, "monthly_league_month": {"$ne": month_id}},
            {"$set": {
                "monthly_league_month": month_id,
                "monthly_league_xp": 0,
            }},
        )
    update_ops = {
        "$set": {
            "last_practice_date": now,
            "streak": new_streak,
            "longest_streak": longest_streak,
            "daily_goal_count": daily_goal_count,
            "daily_goal_date": today.isoformat(),
            "weekly_league_week": week_id,
            "current_combo": current_combo,
            "max_combo": max_combo,
            "last_combo_at": now,
        },
        "$inc": {
            "diamonds": xp_gained,
            "coins": coins_earned,
            "proof": proof_earned,
            "bounty": bounty_earned,
            "stars_total": stars,
            counter_field: 1,
            "total_perfect_scores": 1 if score10 >= 10 else 0,
            "weekly_league_xp": xp_gained,
            "monthly_league_xp": xp_gained,
        },
        "$currentDate": {"updated_at": True},
    }

    # Update first_solve_today
    if is_first_today:
        update_ops["$set"]["first_solve_today"] = now

    # Deduct streak freeze if used
    if streak_frozen_today:
        update_ops["$set"]["streak_freezes"] = streak_freezes

    # ─── Transactional multi-step write ───
    # Wraps: activity update + level recalc + challenge progress in a
    # MongoDB transaction for atomicity on replica-set deployments.
    try:
        client = get_client()
        async with await client.start_session() as session:
            async with session.start_transaction():
                # 1. Record activity (streak, Diamonds, coins, counters)
                coll = gamification_collection()
                await coll.update_one({"user_id": user_id}, update_ops, session=session)

                # 2. Re-read profile within transaction for consistent level calc
                profile = await coll.find_one({"user_id": user_id}, session=session)
                old_level = profile.get("level", 1)
                new_level = _calculate_level(profile.get("diamonds", 0))
                level_up = new_level != old_level

                if level_up:
                    await coll.update_one(
                        {"user_id": user_id},
                        {"$set": {"level": new_level}},
                        session=session,
                    )
                # 3. Update challenge progress inside the same transaction
                await _update_challenge_progress_tx(
                    user_id, activity_type, score, new_streak, new_level, session
                )
    except Exception as exc:
        logger.warning(
            f"Gamification transaction failed, falling back to atomic writes: {exc}"
        )
        # ── Fallback: same logic without transactions (standalone mongod) ──
        await gamification_collection.update_one({"user_id": user_id}, update_ops)
        profile = await gamification_collection.find_one({"user_id": user_id})
        old_level = profile.get("level", 1)
        new_level = _calculate_level(profile.get("diamonds", 0))
        level_up = new_level != old_level

        if level_up:
            await gamification_collection.update_one(
                {"user_id": user_id},
                {"$set": {"level": new_level}},
            )
        await _update_challenge_progress(user_id, activity_type, score, new_streak, new_level)

    # Check for new badges
    new_badges = await _check_badges(user_id, activity_type, score, new_streak)

    # Check achievement chains after badges update
    badge_ids = [b.get("id") for b in new_badges] if new_badges else []
    all_badge_ids = normalize_badge_ids(list(profile.get("badges", [])) + badge_ids)
    new_achievements = await _check_achievement_chains(user_id, all_badge_ids)

    # Check streak milestone chests (real inventory rewards at 7/14/30/60/100 days)
    milestone_rewards = await _check_streak_milestones(user_id, new_streak, old_streak)

    # Check if current level is a boss level
    boss_level = new_level if new_level % 10 == 0 and new_level <= 100 else None
    is_boss_defeated = boss_level in (profile.get("bosses_defeated") or [])

    # Auto-check boss eligibility after recording the activity
    boss_result = await check_boss_eligibility(user_id, score10, activity_type)

    result = {
        "event_id": event_id,
        "activity_id": act_id,
        "xp_gained": xp_gained,
        "coins_earned": coins_earned,
        "stars_earned": stars,
        # Antecedents for the RewardShowcase: the frontend renders these
        # verbatim and must never back-compute base from the total.
        "base_xp": base_xp,
        "multipliers": {
            "streak": calculate_streak_multiplier(new_streak)[0],
            "combo": combo_mult,
            "first_of_day": is_first_today,
            "performance": performance_mult,
            "performance_reasons": performance_reasons,
            "double_xp": bool(dxp_active),
        },
        "new_streak": new_streak,
        "new_badges": new_badges,
        "new_achievements": new_achievements,
        "level": new_level,
        "level_up": level_up,
        "old_level": old_level,
        "is_first_today": is_first_today,
        "combo": {
            "current": current_combo,
            "max": max_combo,
            "multiplier": combo_mult,
        },
        "critical_hit": critical_hit,
        "critical_bonus": critical_bonus,
        "boss_level": boss_level if boss_level and not is_boss_defeated else None,
        "streak_multiplier": calculate_streak_multiplier(new_streak)[0],
        "streak_frozen": streak_frozen_today,
        "streak_freezes_remaining": streak_freezes,
        "daily_goal_count": daily_goal_count,
        "daily_goal_target": profile.get("daily_goal_target", 5),
        "milestone": milestone_rewards,
        "milestone_coins_bonus": sum(r["items"].get("coins", 0) for r in milestone_rewards.values()),
    }

    if boss_result:
        result["boss_defeated"] = boss_result

    # Immutable reward ledger (audit trail, not dedupe mechanism — endpoint
    # atomic claims remain the dedupe layer). One row per award: inputs,
    # outputs, policy version. Reconcile: sum(xp_awarded) per user == delta
    # of profile.diamonds over the same window (modulo pre-ledger history).
    try:
        from app.database import gamification_events_collection
        await gamification_events_collection.insert_one({
            "event_id": event_id,
            "user_id": user_id,
            "activity_id": act_id,
            "activity_type": activity_type,
            "score": score10,
            "score_raw": score,
            "base_xp": base_xp,
            "multipliers": {
                "streak": calculate_streak_multiplier(new_streak)[0],
                "combo": combo_mult,
                "first_of_day": is_first_today,
                "performance": performance_mult,
                "performance_reasons": performance_reasons,
                "double_xp": bool(dxp_active),
            },
            "xp_awarded": xp_gained,
            "coins_awarded": coins_earned,
            "stars_awarded": stars,
            "new_badges": [b.get("id") if isinstance(b, dict) else b for b in (new_badges or [])],
            "level_after": new_level,
            "reward_policy_version": REWARD_POLICY_VERSION,
            "metadata": metadata or {},
            "created_at": now,
        })
    except Exception as exc:
        logger.warning(f"Reward ledger insert failed for {user_id}: {exc}")

    return result


REWARD_POLICY_VERSION = "2026.1"


async def award_bonus_xp(user_id: str, diamonds: int, coins: int, reason: str, metadata: dict | None = None) -> bool:
    """Award bonus Diamonds/coins outside the normal activity pipeline (boss defeats,
    daily bonuses, challenge claims, etc.). Writes a ledger row so
    profile.diamonds == sum(ledger) reconciliation holds.

    This is the ONLY acceptable way to write Diamonds/coins outside record_practice().
    """
    import uuid as _uuid
    from datetime import datetime, timezone
    diamonds = int(diamonds or 0)
    coins = int(coins or 0)
    if diamonds <= 0 and coins <= 0:
        return False

    now = datetime.now(timezone.utc)
    update_ops: dict = {}
    if diamonds > 0:
        update_ops["$inc"] = {"diamonds": diamonds}
    if coins > 0:
        if "$inc" in update_ops:
            update_ops["$inc"]["coins"] = coins
        else:
            update_ops["$inc"] = {"coins": coins}
    update_ops["$currentDate"] = {"updated_at": True}

    await gamification_collection.update_one({"user_id": user_id}, update_ops)

    # Recalculate level after Diamonds award
    profile = await gamification_collection.find_one({"user_id": user_id})
    new_level = _calculate_level(profile.get("diamonds", 0))
    if new_level != profile.get("level", 1):
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"level": new_level}},
        )

    # Write ledger row for reconciliation
    try:
        from app.database import gamification_events_collection
        await gamification_events_collection.insert_one({
            "event_id": _uuid.uuid4().hex,
            "user_id": user_id,
            "activity_id": _uuid.uuid4().hex,
            "activity_type": f"bonus_{reason}",
            "score": 0,
            "score_raw": 0,
            "base_xp": diamonds,
            "multipliers": {},
            "xp_awarded": diamonds,
            "coins_awarded": coins,
            "stars_awarded": 0,
            "new_badges": [],
            "level_after": new_level,
            "reward_policy_version": REWARD_POLICY_VERSION,
            "metadata": {"reason": reason, **(metadata or {})},
            "created_at": now,
        })
    except Exception as exc:
        logger.warning(f"Bonus Diamonds ledger insert failed for {user_id}: {exc}")
    return True


async def spend_xp(user_id: str, amount: int, reason: str, metadata: dict | None = None) -> bool:
    """Spend Diamonds (shop purchases). The engine-side counterpart to awards.

    Atomic $gte guard: concurrent double-buys collapse to exactly one debit
    (loser sees insufficient funds). Writes a negative ledger row so
    reconcile (profile.diamonds == sum(ledger)) holds across spends too.
    Returns True when debited, False when funds are insufficient.
    """
    import uuid as _uuid
    from datetime import datetime, timezone
    amount = int(amount or 0)
    if amount <= 0:
        return False
    res = await gamification_collection.update_one(
        {"user_id": user_id, "diamonds": {"$gte": amount}},
        {"$inc": {"diamonds": -amount}},
    )
    if res.matched_count == 0:
        return False
    try:
        from app.database import gamification_events_collection
        await gamification_events_collection.insert_one({
            "event_id": _uuid.uuid4().hex,
            "user_id": user_id,
            "activity_id": _uuid.uuid4().hex,
            "activity_type": "shop_spend",
            "score": 0,
            "score_raw": 0,
            "base_xp": 0,
            "multipliers": {},
            "xp_awarded": -amount,
            "coins_awarded": 0,
            "stars_awarded": 0,
            "new_badges": [],
            "level_after": None,
            "reward_policy_version": REWARD_POLICY_VERSION,
            "metadata": {"reason": reason, **(metadata or {})},
            "created_at": datetime.now(timezone.utc),
        })
    except Exception as exc:
        logger.warning(f"Reward ledger insert failed for {user_id}: {exc}")
    return True




async def _check_badges(user_id: str, activity_type: str, score: float, streak: int) -> list:
    """Evaluate every catalogued badge condition against the profile + event.

    Conditions live declaratively in BADGE_CONDITIONS (gamification_core).
    A badge with no condition can never be earned — the CI parity test
    rejects that. Score-based conditions keep the RAW caller scale per
    activity (interview/system_design 0-10, aptitude/coding/resume 0-100);
    the ENGINE computes level from Diamonds server-side. Badges are written
    as string IDs via $addToSet (idempotent by construction).
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return []
    existing_badges = set(normalize_badge_ids(profile.get("badges", [])))
    new_badges = []
    for badge_id, condition in BADGE_CONDITIONS.items():
        if badge_id in existing_badges:
            continue
        if badge_condition_met(condition, profile, activity_type, score, streak):
            new_badges.append(badge_id)
            await gamification_collection.update_one(
                {"user_id": user_id},
                {"$addToSet": {"badges": badge_id}},
            )
    return [BADGES[b] for b in new_badges if b in BADGES]


async def _update_challenge_progress_tx(
    user_id: str,
    activity_type: str,
    score: float,
    streak: int,
    level: int,
    session,
):
    """Transaction-aware version of _update_challenge_progress.

    Accepts a ``motor`` session object so it participates in the caller's
    transaction.  Reads and writes are routed through the session to ensure
    snapshot-level isolation.
    """
    coll = gamification_collection()
    profile = await coll.find_one({"user_id": user_id}, session=session)
    if not profile:
        return

    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    month_key = f"{now.year}-{now.month}"

    if profile.get("challenge_week") != week_num and profile.get("challenge_month") != month_key:
        return

    weekly = profile.get("weekly_challenges", [])
    monthly = profile.get("monthly_challenges", [])
    updated = False

    for ch in weekly:
        if ch.get("completed"):
            continue
        metric = ch.get("metric", "")
        if metric == "problems_solved" and activity_type in ("question_bank", "coding"):
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "streak" and streak >= ch["target"]:
            ch["progress"] = streak
            ch["completed"] = True
            updated = True
        elif metric == "aptitude_90plus" and activity_type == "aptitude" and score >= 90:
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "interviews" and activity_type == "interview":
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "hard_solved" and activity_type in ("question_bank", "coding") and score >= 8:
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True

    for ch in monthly:
        if ch.get("completed"):
            continue
        metric = ch.get("metric", "")
        if metric == "problems_solved" and activity_type in ("question_bank", "coding"):
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "level" and level >= ch["target"]:
            ch["progress"] = level
            ch["completed"] = True
            updated = True
        elif metric == "interviews" and activity_type == "interview":
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "streak" and streak >= ch["target"]:
            ch["progress"] = streak
            ch["completed"] = True
            updated = True

    if updated:
        update_ops = {}
        if weekly:
            update_ops["weekly_challenges"] = weekly
        if monthly:
            update_ops["monthly_challenges"] = monthly
        if update_ops:
            await coll.update_one(
                {"user_id": user_id}, {"$set": update_ops}, session=session
            )


async def _update_challenge_progress(user_id: str, activity_type: str, score: float, streak: int, level: int):
    """Increment challenge progress counters based on activity."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return

    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    month_key = f"{now.year}-{now.month}"

    # Only update if challenges are for current period
    if profile.get("challenge_week") != week_num and profile.get("challenge_month") != month_key:
        return

    weekly = profile.get("weekly_challenges", [])
    monthly = profile.get("monthly_challenges", [])
    updated = False

    for ch in weekly:
        if ch.get("completed"):
            continue
        metric = ch.get("metric", "")
        if metric == "problems_solved" and activity_type in ("question_bank", "coding"):
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "streak" and streak >= ch["target"]:
            ch["progress"] = streak
            ch["completed"] = True
            updated = True
        elif metric == "aptitude_90plus" and activity_type == "aptitude" and score >= 90:
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "interviews" and activity_type == "interview":
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "hard_solved" and activity_type in ("question_bank", "coding") and score >= 8:
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True

    for ch in monthly:
        if ch.get("completed"):
            continue
        metric = ch.get("metric", "")
        if metric == "problems_solved" and activity_type in ("question_bank", "coding"):
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "level" and level >= ch["target"]:
            ch["progress"] = level
            ch["completed"] = True
            updated = True
        elif metric == "interviews" and activity_type == "interview":
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "streak" and streak >= ch["target"]:
            ch["progress"] = streak
            ch["completed"] = True
            updated = True

    if updated:
        update_ops = {}
        if weekly:
            update_ops["weekly_challenges"] = weekly
        if monthly:
            update_ops["monthly_challenges"] = monthly
        if update_ops:
            await gamification_collection.update_one({"user_id": user_id}, {"$set": update_ops})


async def ensure_tower_fields(user_id: str):
    """Add missing tower fields to existing users (migration)."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return await initialize_gamification(user_id)

    defaults = {
        "stars_total": 0,
        "stars_per_problem": {},
        "coins": 0,
        "power_ups": {k: 0 for k in POWER_UPS},
        "bosses_defeated": [],
        "first_solve_today": None,
        "weekly_challenges": [],
        "monthly_challenges": [],
        "current_combo": 0,
        "max_combo": 0,
        "last_combo_at": None,
        "daily_login_streak": 0,
        "last_daily_login_date": None,
        "achievements": [],
    }

    missing = {k: v for k, v in defaults.items() if k not in profile}
    if missing:
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": missing},
        )

    return profile


async def get_gamification_profile(user_id: str) -> dict:
    """Get the full gamification profile with tower data."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    # Derive role from user doc so it stays in sync with auth/profile state
    user_role = "sde"
    try:
        from bson import ObjectId
        user_doc = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            user_role = user_doc.get("role") or user_doc.get("target_role") or "sde"
    except Exception:
        user_role = "sde"

    level = _calculate_level(profile.get("diamonds", 0))
    target_company = profile.get("target_company")
    # NOTE: the module-level get_title_for_level() below shadows the
    # company-aware gamification_core import, so call the core explicitly.
    from app.services.gamification_core import get_title_for_level as _core_title_for_level
    title, emoji = _core_title_for_level(level, company_id=target_company)
    rank_title, rank_emoji, rank_tier = voyage_rank_for_level(level)
    mult, bonus = calculate_streak_multiplier(profile.get("streak", 0))

    # Current boss info
    boss_level = level if level % 10 == 0 and level <= 100 else None
    current_boss = None
    if boss_level and boss_level not in (profile.get("bosses_defeated") or []):
        current_boss = alias_boss_with_storm(BOSS_BATTLES.get(boss_level), boss_level)

    profile["id"] = str(profile.pop("_id"))
    profile["badges"] = normalize_badge_ids(profile.get("badges", []))
    profile["badges_details"] = [
        {**BADGES[b], "id": b}
        for b in profile["badges"]
        if b in BADGES
    ]
    profile["level"] = level
    profile["xp_to_next_level"] = xp_for_next_level(level) - profile.get("diamonds", 0)
    profile["xp_for_current_level"] = xp_for_level(level)
    # Explicit progress numbers so the client never recomputes the curve:
    # into = diamonds earned inside this level, span = level width.
    profile["xp_into_level"] = max(0, profile.get("diamonds", 0) - xp_for_level(level))
    profile["xp_level_span"] = max(1, xp_for_next_level(level) - xp_for_level(level))
    profile["title"] = title
    profile["title_emoji"] = emoji
    profile["rank_title"] = rank_title
    profile["rank_emoji"] = rank_emoji
    profile["rank_tier"] = rank_tier
    profile["streak_multiplier"] = mult
    profile["streak_bonus_xp"] = bonus
    profile["current_boss"] = current_boss
    profile["boss_level"] = boss_level
    profile["role"] = user_role
    profile["forest_state"] = compute_forest_state(
        level=level,
        diamonds=profile.get("diamonds", 0),
        streak=profile.get("streak", 0),
        badges=profile.get("badges", []),
        bosses_defeated=profile.get("bosses_defeated", []),
    )
    profile["power_ups"] = profile.get("power_ups", POWER_UPS.fromkeys([k for k in POWER_UPS], 0))
    profile["coins"] = profile.get("coins", 0)
    profile["bounty"] = profile.get("bounty", 0)
    profile["proof"] = profile.get("proof", 0)
    profile["stars_total"] = profile.get("stars_total", 0)
    profile["streak_freezes"] = profile.get("streak_freezes", 0)
    profile["color"] = get_level_color(level)
    profile["target_company"] = target_company

    # Daily goal
    now = datetime.now(timezone.utc)
    today = now.date()
    daily_goal_date = profile.get("daily_goal_date")
    if daily_goal_date:
        dg_date = daily_goal_date.date() if isinstance(daily_goal_date, datetime) else daily_goal_date
        daily_goal_count = profile.get("daily_goal_count", 0) if dg_date == today else 0
    else:
        daily_goal_count = 0

    profile["daily_goal_count"] = daily_goal_count
    profile["daily_goal_target"] = profile.get("daily_goal_target", 5)
    profile["daily_goal_completed"] = daily_goal_count >= profile.get("daily_goal_target", 5)

    profile["current_combo"] = profile.get("current_combo", 0)
    profile["max_combo"] = profile.get("max_combo", 0)
    profile["combo_multiplier"] = _combo_multiplier(profile.get("current_combo", 0))
    profile["daily_login_streak"] = profile.get("daily_login_streak", 0)
    profile["last_daily_login_date"] = profile.get("last_daily_login_date")
    profile["achievements"] = profile.get("achievements", [])
    profile["badge_priority"] = get_role_badge_priority(user_role)
    profile["champion_title"] = get_role_champion_title(user_role)

    return profile


# ─── Tower-specific functions ───

async def check_boss_eligibility(user_id: str, activity_score: float, activity_type: str) -> dict | None:
    """Check if the user qualifies to defeat their current boss after an activity.

    Boss levels are multiples of 10 (10, 20, ..., 100).
    A boss is auto-defeated when:
      - The user's current level is a boss level (level % 10 == 0)
      - The boss hasn't been defeated yet
      - The activity_score >= the boss's required_score

    Returns boss defeat info dict or None.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return None

    level = profile.get("level", 1)
    if level % 10 != 0 or level > 100:
        return None

    defeated_list = profile.get("bosses_defeated") or []
    if level in defeated_list:
        return None

    boss = BOSS_BATTLES.get(level)
    if not boss:
        return None

    if activity_score < boss["required_score"]:
        return None

    bonus_xp = level * 10
    bonus_coins = level * 5

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$push": {"bosses_defeated": level},
        },
    )
    # Award boss bonus through canonical pipeline (Gamification Law)
    await award_bonus_xp(user_id, bonus_xp, bonus_coins, "boss_defeat", {"boss_level": level})

    return {
        "boss_defeated": True,
        "boss_level": level,
        "boss_name": boss["name"],
        "boss_emoji": boss["emoji"],
        "bonus_xp": bonus_xp,
        "bonus_coins": bonus_coins,
    }


async def use_power_up(user_id: str, power_up_id: str) -> dict:
    """Use a power-up if user has enough."""
    if power_up_id not in POWER_UPS:
        raise ValueError("Invalid power-up")

    profile = await gamification_collection.find_one({"user_id": user_id})
    pows = profile.get("power_ups", {})
    count = pows.get(power_up_id, 0)
    if count <= 0:
        return {"success": False, "message": "No power-ups left"}

    if power_up_id == "double_xp":
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {
                "$inc": {f"power_ups.{power_up_id}": -1, "total_powerups_used": 1},
                "$set": {"double_xp_expires": expires_at.isoformat()},
            },
        )
        return {
            "success": True,
            "power_up": POWER_UPS[power_up_id],
            "double_xp_expires": expires_at.isoformat(),
            "double_xp_minutes": 60,
        }
    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$inc": {f"power_ups.{power_up_id}": -1, "total_powerups_used": 1}},
    )
    return {"success": True, "power_up": POWER_UPS[power_up_id]}


async def buy_power_up(user_id: str, power_up_id: str) -> dict:
    """Buy a power-up with coins."""
    if power_up_id not in POWER_UPS:
        raise ValueError("Invalid power-up")

    up = POWER_UPS[power_up_id]
    profile = await gamification_collection.find_one({"user_id": user_id})
    coins = profile.get("coins", 0)
    if coins < up["cost"]:
        return {"success": False, "message": f"Need {up['cost']} coins, have {coins}"}

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {"coins": -up["cost"], f"power_ups.{power_up_id}": 1},
        },
    )
    return {"success": True, "power_up": up, "coins_remaining": coins - up["cost"]}


# ─── Streak Freeze ───

STREAK_FREEZE_COST = 50  # coins
STREAK_REPAIR_COST = 100  # coins — restores a broken streak (Duolingo "Streak Repair")

# Daily login bonus calendar (Duolingo-style escalating streak calendar).
# Bonus pays out as Diamonds (10 → 50) + coins; coins only unlock at tier 3+.
DAILY_BONUS_TIERS = {
    0: {"coins": 0},
    1: {"coins": 0},
    2: {"coins": 5},
    3: {"coins": 10},
    4: {"coins": 15},
    5: {"coins": 25},
    6: {"coins": 40},
}

async def buy_streak_freeze(user_id: str) -> dict:
    """Buy a streak freeze for coins."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    coins = profile.get("coins", 0)
    if coins < STREAK_FREEZE_COST:
        return {"success": False, "message": f"Need {STREAK_FREEZE_COST} coins, have {coins}"}

    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"coins": -STREAK_FREEZE_COST, "streak_freezes": 1}},
    )
    return {"success": True, "cost": STREAK_FREEZE_COST, "coins_remaining": coins - STREAK_FREEZE_COST}


async def get_streak_freeze_status(user_id: str) -> dict:
    """Get streak freeze status."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    freezes = profile.get("streak_freezes", 0)
    streak = profile.get("streak", 0)

    # Check if streak is in danger (no practice today yet)
    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    days_since = 0
    if last_date:
        ld = last_date.date() if isinstance(last_date, datetime) else last_date
        days_since = (today - ld).days

    return {
        "streak_freezes": freezes,
        "streak": streak,
        "days_since_practice": days_since,
        "streak_in_danger": days_since >= 1 and streak > 0,
        "can_freeze": freezes > 0 and days_since == 1 and streak > 0,
        "cost": STREAK_FREEZE_COST,
    }


async def buy_streak_repair(user_id: str, user: dict = None) -> dict:
    """Restore a broken practice streak for coins (Duolingo-style Streak Repair).

    Free users get 1 Streak Repair/month; Pro/Lifetime = unlimited. If the user
    has a streak_freeze token, it is consumed instead of costing coins.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    # Tier gate: free users limited to FREE_TIER_STREAK_REPAIRS per month.
    if user is not None and user.get("plan") not in ("pro", "lifetime"):
        allowed, reason = can_use_feature(user, "streak_repair")
        if not allowed:
            return {"success": False, "upgrade_required": True, "message": reason}

    coins = profile.get("coins", 0)
    if coins < STREAK_REPAIR_COST:
        return {"success": False, "message": f"Need {STREAK_REPAIR_COST} coins, have {coins}"}

    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    if last_date:
        ld = last_date.date() if isinstance(last_date, datetime) else last_date
        days_since = (today - ld).days
    else:
        days_since = 0

    # Only repair a streak broken today (missed exactly yesterday's check).
    if days_since != 1 or profile.get("streak", 0) <= 0:
        return {
            "success": False,
            "message": "Streak not eligible for repair (no streak broken today)",
        }

    streak_freezes = profile.get("streak_freezes", 0)

    # Determine cost source: use a streak_freeze token if available, else coins.
    if streak_freezes > 0:
        update = {
            "$inc": {"streak_freezes": -1},
            "$set": {
                "last_practice_date": now,
                "daily_goal_count": profile.get("daily_goal_count", 0) + 1,
                "daily_goal_date": today.isoformat(),
            },
        }
        message = "Streak repaired using a streak freeze"
        cost = 0
    else:
        update = {
            "$inc": {"coins": -STREAK_REPAIR_COST},
            "$set": {
                "last_practice_date": now,
                "daily_goal_count": profile.get("daily_goal_count", 0) + 1,
                "daily_goal_date": today.isoformat(),
            },
        }
        message = "Streak repaired"
        cost = STREAK_REPAIR_COST

    await gamification_collection.update_one({"user_id": user_id}, update)
    if user is not None and user.get("plan") not in ("pro", "lifetime"):
        await mark_feature_used(user["id"], "streak_repair")
    return {"success": True, "cost": cost, "message": message}


# ─── Streak Milestone Chests (real inventory rewards, not just Diamonds) ───

# Research (Duolingo teardown): milestone celebrations must deliver *real*
# in-game value, not symbolic confetti. Each chest grants functional items.
STREAK_MILESTONE_REWARDS = {
    7:  {"title": "Firestarter", "items": {"streak_freezes": 1, "coins": 100}, "emoji": "🔥"},
    14: {"title": "Hot Streak",  "items": {"streak_freezes": 1, "coins": 250}, "emoji": "🌶️"},
    30: {"title": "Month Master", "items": {"streak_freezes": 2, "coins": 500, "double_xp": 1}, "emoji": "🌙"},
    60: {"title": "Unbreakable",  "items": {"streak_freezes": 3, "coins": 1000, "double_xp": 2}, "emoji": "💎"},
    100: {"title": "Centurion",   "items": {"streak_freezes": 5, "coins": 2000, "double_xp": 3, "skip_boss": 1}, "emoji": "🏯"},
}
STREAK_MILESTONE_DAYS = sorted(STREAK_MILESTONE_REWARDS.keys())


async def _check_streak_milestones(user_id: str, new_streak: int, old_streak: int) -> dict:
    """Grant real inventory rewards when a streak crosses a milestone day.

    Returns a dict describing the milestone chest opened (or empty). Mirrors
    Duolingo's "milestone = chest of real value" design: functional items
    (freezes, Diamonds boosts, coins) the user can hold.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {}

    claimed = set(profile.get("streak_milestones_claimed", []))
    result = {}
    crossed = [
        m for m in STREAK_MILESTONE_DAYS
        if old_streak < m <= new_streak and m not in claimed
    ]
    if not crossed:
        return result

    inc = {}
    for m in crossed:
        reward = STREAK_MILESTONE_REWARDS[m]
        result[m] = reward
        for k, v in reward["items"].items():
            if k == "coins":
                inc["coins"] = inc.get("coins", 0) + v
            elif k == "streak_freezes":
                inc["streak_freezes"] = inc.get("streak_freezes", 0) + v
            else:
                # power-up slot
                pu = profile.get("power_ups", {})
                inc[f"power_ups.{k}"] = inc.get(f"power_ups.{k}", 0) + v

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$push": {"streak_milestones_claimed": {"$each": crossed}},
            "$inc": inc,
        },
    )
    return result


async def apply_streak_freeze_on_login(user_id: str) -> dict:
    """Login-time streak protection.

    If the user opened the app after missing exactly one day and still has a
    streak freeze, auto-consume a freeze so opening the app protects the habit
    (recovery mechanic must exist at login — the moment a streak is most
    likely to die). Returns status for the login banner.
    """
    from app.services.gamification import ensure_tower_fields
    await ensure_tower_fields(user_id)
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"applied": False, "reason": "no_profile"}

    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    if not last_date:
        return {"applied": False, "reason": "no_practice_yet"}
    last_day = last_date.date() if isinstance(last_date, datetime) else last_date
    days_since = (today - last_day).days
    streak = profile.get("streak", 0)
    freezes = profile.get("streak_freezes", 0)

    if days_since == 1 and streak > 0 and freezes > 0:
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"streak_freezes": -1, "streak": 1},
             "$set": {"last_practice_date": now,
                      "streak_frozen_today": True}},
        )
        return {
            "applied": True,
            "streak": streak + 1,
            "freezes_remaining": freezes - 1,
            "message": "🔥 Streak protected! You keep your streak.",
        }
    return {"applied": False, "freezes_remaining": freezes, "days_since_practice": days_since}


# ─── Weekly Leagues (cohort-based promotion/relegation) ───

# Research (Duolingo): weekly reset cadence + promotion/relegation among
# beatable peers drives return visits. Ranks reset each week (Sunday UTC).
LEAGUE_TIERS = [
    {"key": "bronze",  "name": "Bronze",   "icon": "🥉", "min_xp": 0,   "color": "#CD7F32"},
    {"key": "silver",  "name": "Silver",   "icon": "🥈", "min_xp": 500, "color": "#C0C0C0"},
    {"key": "gold",    "name": "Gold",     "icon": "🥇", "min_xp": 1500,"color": "#FFD700"},
    {"key": "platinum","name": "Platinum", "icon": "💎", "min_xp": 4000,"color": "#E5E4E2"},
    {"key": "diamond", "name": "Diamond",  "icon": "♦️", "min_xp": 10000,"color": "#B9F2FF"},
]

def _league_week_id() -> str:
    """UTC ISO week id (Monday boundary). Single week definition for the
    whole league system — do not introduce wall-clock/IST variants."""
    now = datetime.now(timezone.utc)
    iso_year, iso_week, _ = now.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def _naive_utc(dt):
    """Strip tzinfo for arithmetic against naive Mongo datetimes.

    The driver returns naive UTC (tz_aware=False) while code uses aware
    `now`; subtracting mixed types raises TypeError. All datetimes here
    are UTC by convention (see app/utils/timeutil.py), so dropping tzinfo
    is comparison-safe. Returns None for unparseable input.
    """
    try:
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        if isinstance(dt, datetime) and dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt if isinstance(dt, datetime) else None
    except Exception:
        return None


def _league_for_xp(diamonds: int):
    tier = LEAGUE_TIERS[0]
    for t in LEAGUE_TIERS:
        if diamonds >= t["min_xp"]:
            tier = t
    return tier


async def get_league_status(user_id: str) -> dict:
    """Compute the user's weekly league tier + rank within their cohort.

    Cohort: all users with season_xp this week (stored in season_xp_collection
    with season_id matching the weekly league id). Rank is by weekly Diamonds.
    Mirrors Duolingo-style weekly reset + promotion/relegation.
    """
    week_id = _league_week_id()
    season_id = f"league-{week_id}"

    profile = await gamification_collection.find_one({"user_id": user_id})
    weekly_xp = profile.get("weekly_league_xp", 0) if profile else 0

    tier = _league_for_xp(weekly_xp)

    # Compute rank: count how many users have strictly more weekly_xp this week
    higher = await gamification_collection.count_documents({"weekly_league_xp": {"$gt": weekly_xp}})
    total = await gamification_collection.count_documents({})
    rank = higher + 1

    return {
        "week": week_id,
        "season_id": season_id,
        "weekly_xp": weekly_xp,
        "rank": rank,
        "of": max(total, 1),
        "tier": tier,
        "promoted_next_week": False,
        "relegated_next_week": False,
        "tiers": LEAGUE_TIERS,
    }


# ─── Daily Goal ───

async def get_daily_goal(user_id: str) -> dict:
    """Get daily goal progress."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"count": 0, "target": 5, "completed": False, "xp_reward": 15}

    now = datetime.now(timezone.utc)
    today = now.date()
    daily_goal_date = profile.get("daily_goal_date")

    if daily_goal_date:
        dg_date = daily_goal_date.date() if isinstance(daily_goal_date, datetime) else daily_goal_date
        if dg_date != today:
            count = 0
        else:
            count = profile.get("daily_goal_count", 0)
    else:
        count = 0

    target = profile.get("daily_goal_target", 5)
    completed = count >= target

    return {
        "count": count,
        "target": target,
        "completed": completed,
        "xp_reward": 15 if not completed else 0,
    }


async def get_challenges(user_id: str) -> dict:
    """Get weekly and monthly challenges for a user."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    month_key = f"{now.year}-{now.month}"

    # Check if challenges need refresh
    stored_week = profile.get("challenge_week")
    stored_month = profile.get("challenge_month")

    weekly = profile.get("weekly_challenges", [])
    monthly = profile.get("monthly_challenges", [])

    if stored_week != week_num:
        # Generate new weekly challenges (pick 3 random)
        import random
        weekly = []
        available = WEEKLY_CHALLENGES.copy()
        for _ in range(min(3, len(available))):
            ch = random.choice(available)
            weekly.append({**ch, "progress": 0, "completed": False, "claimed": False})
            available.remove(ch)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"weekly_challenges": weekly, "challenge_week": week_num}},
        )

    if stored_month != month_key:
        import random
        monthly = []
        available = MONTHLY_CHALLENGES.copy()
        for _ in range(min(3, len(available))):
            ch = random.choice(available)
            monthly.append({**ch, "progress": 0, "completed": False, "claimed": False})
            available.remove(ch)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"monthly_challenges": monthly, "challenge_month": month_key}},
        )

    return {"weekly": weekly, "monthly": monthly}


async def claim_challenge_reward(user_id: str, challenge_type: str, challenge_id: str) -> dict:
    """Claim a completed challenge reward.

    Atomic single-update claim: the array-filter matches only an
    unclaimed+completed element, so concurrent double-claims collapse to
    exactly one award (modified_count 0 => already claimed). Read-then-write
    here would double-award under concurrent double-taps.
    """
    profile = await gamification_collection.find_one(
        {"user_id": user_id}, {"diamonds": 1})
    if not profile:
        return {"success": False, "message": "Profile not found"}
    field = f"{challenge_type}_challenges"
    # Need the reward amount; read is fine — the AWARD below is conditional.
    full = await gamification_collection.find_one(
        {"user_id": user_id}, {field: 1})
    reward = 0
    for ch in (full.get(field, []) if full else []):
        if ch.get("id") == challenge_id and ch.get("completed"):
            reward = int(ch.get("xp_reward", 0) or 0)
            break
    if not reward:
        return {"success": False, "message": "Challenge not completed or already claimed"}
    # The $elemMatch in the query is the mutex: the doc matches only while
    # an unclaimed+completed element exists, so concurrent double-claims
    # collapse to exactly one award. (modified_count can't be the signal —
    # the unconditional $inc would mark every attempt modified.)
    res = await gamification_collection.update_one(
        {"user_id": user_id,
         field: {"$elemMatch": {"id": challenge_id, "completed": True, "claimed": False}}},
        {
            "$set": {f"{field}.$[c].claimed": True},
        },
        array_filters=[{"c.id": challenge_id}],
    )
    if res.matched_count == 0:
        return {"success": False, "message": "Challenge not completed or already claimed"}
    # Award challenge reward through canonical pipeline (Gamification Law)
    await award_bonus_xp(user_id, reward, reward // 5, "challenge_claim", {"challenge_id": challenge_id})
    return {"success": True, "xp_earned": reward}


async def get_leaderboard(limit: int = 10, timeframe: str = "all", level_min: int | None = None, level_max: int | None = None) -> list:
    """Top users by Diamonds. timeframe actually filters: weekly/monthly sort on
    the period counters (which reset), all on lifetime diamonds."""
    field = {"weekly": "weekly_league_xp", "monthly": "monthly_league_xp"}.get(
        (timeframe or "all").lower(), "diamonds")
    query: dict = {}
    if level_min is not None or level_max is not None:
        query["level"] = {}
        if level_min is not None:
            query["level"]["$gte"] = level_min
        if level_max is not None:
            query["level"]["$lte"] = level_max
    cursor = gamification_collection.find(query).sort(field, -1).limit(limit)

    leaderboard = []
    async for doc in cursor:
        level = doc.get("level") or _calculate_level(doc.get("diamonds", 0))
        title, emoji = get_title_for_level(level)
        rank_title, rank_emoji, rank_tier = voyage_rank_for_level(level)
        color = get_level_color(level)
        leaderboard.append({
            "user_id": doc.get("user_id", ""),
            "diamonds": doc.get("diamonds", 0),
            "period_xp": doc.get(field, 0),
            "timeframe": (timeframe or "all").lower(),
            "level": level,
            "title": title,
            "title_emoji": emoji,
            "rank_title": rank_title,
            "rank_emoji": rank_emoji,
            "rank_tier": rank_tier,
            "color": color,
            "streak": doc.get("streak", 0),
            "badges_count": len(doc.get("badges", [])),
        })

    return leaderboard


async def get_league_leaderboard(user_id: str, timeframe: str = "weekly", band_size: int = 5) -> dict:
    """Level-band league leaderboard.

    Groups users into bands of `band_size` levels. Sorts each band by the
    requested timeframe counter. Marks top/bottom users with promotion/
    demotion zones so the UI can render honest league state.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    my_level = profile.get("level") or _calculate_level(profile.get("diamonds", 0))
    band_start = ((my_level - 1) // band_size) * band_size + 1
    band_end = band_start + band_size - 1
    field = {"weekly": "weekly_league_xp", "monthly": "monthly_league_xp"}.get(
        (timeframe or "weekly").lower(), "diamonds"
    )
    cursor = gamification_collection.find({
        "level": {"$gte": band_start, "$lte": band_end}
    }).sort(field, -1)

    entries = []
    async for doc in cursor:
        level = doc.get("level") or _calculate_level(doc.get("diamonds", 0))
        title, emoji = get_title_for_level(level)
        rank_title, rank_emoji, rank_tier = voyage_rank_for_level(level)
        color = get_level_color(level)
        entries.append({
            "user_id": doc.get("user_id", ""),
            "diamonds": doc.get("diamonds", 0),
            "period_xp": doc.get(field, 0),
            "timeframe": (timeframe or "weekly").lower(),
            "level": level,
            "title": title,
            "title_emoji": emoji,
            "rank_title": rank_title,
            "rank_emoji": rank_emoji,
            "rank_tier": rank_tier,
            "color": color,
            "streak": doc.get("streak", 0),
            "badges_count": len(doc.get("badges", [])),
        })

    total = len(entries)
    promotion_cut = max(1, int(total * 0.1))
    demotion_cut = total - max(1, int(total * 0.1))
    for idx, entry in enumerate(entries):
        if idx < promotion_cut:
            entry["zone"] = "promotion"
        elif idx >= demotion_cut:
            entry["zone"] = "demotion"
        else:
            entry["zone"] = "safe"

    my_index = next((i for i, e in enumerate(entries) if e["user_id"] == user_id), None)
    return {
        "entries": entries,
        "user_index": my_index,
        "user_rank": (my_index + 1) if my_index is not None else None,
        "band_start": band_start,
        "band_end": band_end,
        "timeframe": (timeframe or "weekly").lower(),
        "total": total,
    }


async def get_nearby_leaderboard(user_id: str, radius: int = 5, limit: int = 10) -> list:
    """Relative leaderboard: users near *your* Diamonds rank (not absolute top).

    Returns `radius` users above and below the caller's rank, plus the caller.
    Per the gamification literature, relative ("tiered") leaderboards keep
    mid/low performers engaged far longer than a single global absolute board.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    my_xp = profile.get("diamonds", 0)

    above = gamification_collection.find({"diamonds": {"$gt": my_xp}}).sort("diamonds", 1).limit(radius)
    below = (
        gamification_collection.find({"diamonds": {"$lt": my_xp}})
        .sort("diamonds", -1)
        .limit(radius)
    )

    async def _compact(cursor):
        out = []
        async for doc in cursor:
            level = _calculate_level(doc.get("diamonds", 0))
            title, emoji = get_title_for_level(level)
            rank_title, rank_emoji, rank_tier = voyage_rank_for_level(level)
            color = get_level_color(level)
            out.append(
                {
                    "user_id": doc.get("user_id", ""),
                    "diamonds": doc.get("diamonds", 0),
                    "level": level,
                    "title": title,
                    "title_emoji": emoji,
                    "rank_title": rank_title,
                    "rank_emoji": rank_emoji,
                    "rank_tier": rank_tier,
                    "color": color,
                    "streak": doc.get("streak", 0),
                    "badges_count": len(doc.get("badges", [])),
                }
            )
        return out

    above_rows = await _compact(above)
    below_rows = await _compact(below)
    my_level = _calculate_level(my_xp)
    my_title, my_emoji = get_title_for_level(my_level)
    my_rank, my_rank_emoji, my_tier = voyage_rank_for_level(my_level)
    my_color = get_level_color(my_level)
    me = {
        "user_id": user_id,
        "diamonds": my_xp,
        "level": my_level,
        "title": my_title,
        "title_emoji": my_emoji,
        "rank_title": my_rank,
        "rank_emoji": my_rank_emoji,
        "rank_tier": my_tier,
        "color": my_color,
        "streak": profile.get("streak", 0),
        "badges_count": len(profile.get("badges", [])),
        "is_me": True,
        "rank": len(below_rows) + 1,
    }
    return {
        "entries": below_rows + [me] + above_rows,
        "user_rank": len(below_rows) + 1,
        "user_xp": my_xp,
        "next_entry_xp": above_rows[0]["diamonds"] if above_rows else my_xp,
    }


async def get_streak_status(user_id: str) -> dict:
    """Lean payload for the streak-at-risk nudge (login-time notification).

    Reuses the same logic as get_streak_freeze_status but returns a minimal,
    notification-friendly shape without plan gating so it can be polled cheaply.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    days_since = 0
    last_ok = False
    if last_date:
        ld = last_date.date() if isinstance(last_date, datetime) else last_date
        days_since = (today - ld).days
        last_ok = True

    streak = profile.get("streak", 0)
    streak_freezes = profile.get("streak_freezes", 0)
    return {
        "streak": streak,
        "days_since_practice": days_since,
        "streak_in_danger": last_ok and days_since >= 1 and streak > 0,
        "streak_freezes": streak_freezes,
        "can_self_repair": streak > 0 and (days_since == 1 or (days_since == 2 and streak_freezes > 0)),
        "daily_bonus_claimed_today": profile.get("last_daily_bonus_date") == today.isoformat(),
    }


async def get_daily_bonus_history(user_id: str, limit: int = 30) -> dict:
    """Return the user's daily login-bonus calendar history (most recent first)."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    history = profile.get("daily_bonus_history", []) or []
    history_sorted = sorted(history, key=lambda x: x.get("date", ""), reverse=True)
    login_streak = profile.get("daily_bonus_login_streak", 0)
    last_date = profile.get("last_daily_bonus_date")

    # 60-day calendar grid (most recent 60 days), each cell flagged claimed + diamonds.
    calendar = _daily_bonus_calendar_grid(history_sorted, login_streak)

    return {
        "login_streak": login_streak,
        "last_claimed": last_date,
        "history": [
            {**h, "count": h.get("diamonds", 0)} for h in history_sorted[:limit]
        ],
        "calendar": calendar,
    }


def _daily_bonus_calendar_grid(history: list, login_streak: int, days: int = 60) -> list:
    """Build a 60-day login-bonus calendar grid for heatmaps.

    Each entry: {date, claimed, diamonds, coins, badge}. Unclaimed prior days count
    as a broken-streak break; today is flagged separately for the frontend.
    """
    today = datetime.now(timezone.utc).date()
    by_date = {h.get("date"): h for h in history}
    grid = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        d_key = d.isoformat()
        h = by_date.get(d_key)
        entry = {
            "date": d_key,
            "claimed": h is not None,
            "diamonds": h.get("diamonds", 0) if h else 0,
            "coins": h.get("coins", 0) if h else 0,
            "badge": h.get("badge") if h else None,
        }
        if d_key == today.isoformat():
            entry["today"] = True
        grid.append(entry)
    return grid


async def claim_daily_bonus(user_id: str) -> dict:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    last_bonus = profile.get("last_daily_bonus_date")
    if last_bonus and last_bonus == today:
        return {
            "claimed": False,
            "xp_bonus": 0,
            "streak_bonus": 0,
            "badge_unlocked": None,
            "message": "Already claimed today",
        }

    import random
    # Escalating daily bonus: the more days in a row you claim, the bigger the
    # payout. Mirrors Duolingo's streak-calendar reward curve (10 -> 50 + bonus).
    login_streak = profile.get("daily_bonus_login_streak", 0)
    xp_bonus = min(10 + (login_streak * 5), 50)
    streak_bonus = 0
    streak = profile.get("streak", 0)

    if streak >= 30:
        streak_bonus = 200
    elif streak >= 7:
        streak_bonus = 50

    bonus_tier = min(login_streak, 6)
    bonus_rewards = DAILY_BONUS_TIERS[bonus_tier]
    badge_unlocked = None
    if random.random() < 0.1 or bonus_tier >= 5:
        # LAW: badges are canonical string IDs, awarded idempotently.
        # The old path appended ad-hoc objects with random ids (unbounded
        # growth + crashed profile reads on unhashable dicts).
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"badges": "lucky_streak"}},
        )
        badge_unlocked = {"id": "lucky_streak", **BADGES["lucky_streak"]}

    total_xp = xp_bonus + streak_bonus
    coin_reward = bonus_rewards.get("coins", 0)

    # Atomic daily claim: the date guard in the filter collapses concurrent
    # double-claims to exactly one award (same race family as challenge
    # claims and world completions).
    claimed = await gamification_collection.update_one(
        {"user_id": user_id, "last_daily_bonus_date": {"$ne": today}},
        {
            "$set": {
                "last_daily_bonus_date": today,
                "daily_bonus_login_streak": login_streak + 1,
            },
            "$push": {
                "daily_bonus_history": {
                    "date": today,
                    "diamonds": total_xp,
                    "coins": coin_reward,
                    "badge": badge_unlocked["id"] if badge_unlocked else None,
                }
            },
        }
    )
    if claimed.matched_count == 0:
        return {
            "claimed": False,
            "xp_bonus": 0,
            "streak_bonus": 0,
            "badge_unlocked": None,
            "message": "Already claimed today",
        }

    # Award daily bonus through canonical pipeline (Gamification Law)
    await award_bonus_xp(user_id, total_xp, coin_reward, "daily_bonus", {"login_streak": login_streak + 1})

    return {
        "claimed": True,
        "xp_bonus": xp_bonus,
        "streak_bonus": streak_bonus,
        "coins_bonus": coin_reward,
        "login_streak": login_streak + 1,
        "bonus_tier": bonus_tier,
        "badge_unlocked": badge_unlocked,
    }


# ─── Combo System ───

COMBO_MULTIPLIERS = [
    (0, 1.0),
    (3, 1.25),
    (5, 1.5),
    (8, 2.0),
    (12, 2.5),
    (20, 3.0),
]

COMBO_WINDOW_SECONDS = 90

# ─── Daily Login Calendar ───

DAILY_LOGIN_REWARDS = [
    {"day": 1, "diamonds": 10,  "coins": 5,  "power_up": None,         "label": "Day 1"},
    {"day": 2, "diamonds": 15,  "coins": 10, "power_up": "hint_reveal", "label": "Day 2"},
    {"day": 3, "diamonds": 25,  "coins": 15, "power_up": None,         "label": "Day 3"},
    {"day": 4, "diamonds": 40,  "coins": 25, "power_up": "speed_boost","label": "Day 4"},
    {"day": 5, "diamonds": 60,  "coins": 40, "power_up": None,         "label": "Day 5"},
    {"day": 6, "diamonds": 100, "coins": 60, "power_up": "double_xp",  "label": "Day 6"},
    {"day": 7, "diamonds": 200, "coins": 100,"power_up": "skip_boss",  "label": "Day 7 — Jackpot"},
]

# ─── Achievement Chains ───

ACHIEVEMENT_CHAINS = {
    "interview_mastery": {
        "name": "Interview Mastery",
        "description": "Complete all interview badges",
        "emoji": "🎯",
        "badges_required": ["first_interview", "interview_10", "interview_50", "perfect_score", "high_score_streak"],
        "reward": {"diamonds": 500, "coins": 200, "title": "Interview Master"},
    },
    "coding_mastery": {
        "name": "Coding Mastery",
        "description": "Complete all coding badges",
        "emoji": "💻",
        "badges_required": ["first_coding", "coding_10", "coding_25", "coding_50", "coding_100", "hard_problem", "first_accepted"],
        "reward": {"diamonds": 800, "coins": 350, "title": "Code Legend"},
    },
    "streak_mastery": {
        "name": "Streak Mastery",
        "description": "Earn all streak badges",
        "emoji": "🔥",
        "badges_required": ["streak_3", "streak_7", "streak_30"],
        "reward": {"diamonds": 300, "coins": 150, "title": "Unstoppable"},
    },
    "aptitude_mastery": {
        "name": "Aptitude Mastery",
        "description": "Complete all aptitude badges",
        "emoji": "🧮",
        "badges_required": ["first_aptitude", "aptitude_perfect", "aptitude_50"],
        "reward": {"diamonds": 400, "coins": 180, "title": "Aptitude Wizard"},
    },
}


def _combo_multiplier(combo: int) -> float:
    mult = 1.0
    for threshold, m in COMBO_MULTIPLIERS:
        if combo >= threshold:
            mult = m
    return mult


async def _check_achievement_chains(user_id: str, badges: list) -> list:
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return []
    existing = set(profile.get("achievements", []))
    new_achievements = []
    for chain_id, chain in ACHIEVEMENT_CHAINS.items():
        if chain_id in existing:
            continue
        required = set(chain.get("badges_required", []))
        if required.issubset(set(badges or [])):
            new_achievements.append(chain)
            await gamification_collection.update_one(
                {"user_id": user_id},
                {"$push": {"achievements": chain_id}},
            )
            # Pay the declared chain reward — an "achievement" whose reward is
            # shown but never paid is a lie (BOUNTYCODE_GAME_ENGINE_V2 §10).
            # Diamonds + coins flow through the canonical pipeline + ledger.
            reward = chain.get("reward", {})
            await award_bonus_xp(
                user_id,
                int(reward.get("diamonds", 0) or 0),
                int(reward.get("coins", 0) or 0),
                f"achievement_{chain_id}",
                {"chain_id": chain_id, "title": reward.get("title")},
            )
            if reward.get("title"):
                titles = list(profile.get("titles", []) or [])
                if reward["title"] not in titles:
                    titles.append(reward["title"])
                    await gamification_collection.update_one(
                        {"user_id": user_id},
                        {"$set": {"titles": titles}},
                    )
    return new_achievements


async def get_combo_status(user_id: str) -> dict:
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"current_combo": 0, "max_combo": 0, "multiplier": 1.0, "combo_decay_seconds": 0, "decay_warning": False}
    now = datetime.now(timezone.utc)
    last_combo_at = profile.get("last_combo_at")
    decay_seconds = 0
    decay_warning = False
    if last_combo_at:
        try:
            if isinstance(last_combo_at, str):
                last_combo_at = datetime.fromisoformat(last_combo_at)
            delta = (_naive_utc(now) - _naive_utc(last_combo_at)).total_seconds()
            decay_seconds = max(0, int(COMBO_WINDOW_SECONDS - delta))
            decay_warning = decay_seconds <= 10 and decay_seconds > 0
        except Exception:
            decay_seconds = 0
            decay_warning = False
    return {
        "current_combo": profile.get("current_combo", 0),
        "max_combo": profile.get("max_combo", 0),
        "multiplier": _combo_multiplier(profile.get("current_combo", 0)),
        "combo_decay_seconds": decay_seconds,
        "decay_warning": decay_warning,
    }


async def get_daily_login_calendar(user_id: str, days: int = 7) -> dict:
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"streak": 0, "calendar": [], "next_reward": DAILY_LOGIN_REWARDS[0]}
    login_streak = profile.get("daily_login_streak", 0)
    last_login = profile.get("last_daily_login_date")
    calendar = []
    for reward in DAILY_LOGIN_REWARDS[:days]:
        claimed = False
        if last_login:
            try:
                last_d = datetime.fromisoformat(last_login).date()
                claimed = login_streak >= reward["day"]
            except Exception:
                claimed = False
        calendar.append({**reward, "claimed": claimed})
    next_reward = None
    for reward in DAILY_LOGIN_REWARDS:
        if not any(c["day"] == reward["day"] and c["claimed"] for c in calendar):
            next_reward = reward
            break
    return {
        "streak": login_streak,
        "calendar": calendar,
        "next_reward": next_reward,
    }


async def claim_daily_login(user_id: str) -> dict:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    last_login = profile.get("last_daily_login_date")
    if last_login == today:
        return {"claimed": False, "message": "Already claimed today", "streak": profile.get("daily_login_streak", 0)}
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    login_streak = profile.get("daily_login_streak", 0)
    if last_login == yesterday:
        login_streak += 1
    elif last_login != today:
        login_streak = 1
    reward = DAILY_LOGIN_REWARDS[min(login_streak, len(DAILY_LOGIN_REWARDS)) - 1]
    updates = {
        "$set": {
            "last_daily_login_date": today,
            "daily_login_streak": login_streak,
        },
    }
    if reward.get("power_up"):
        updates["$inc"] = {f"power_ups.{reward['power_up']}": 1}
    await gamification_collection.update_one({"user_id": user_id}, updates)
    # Award daily login Diamonds/coins through canonical pipeline (Gamification Law)
    await award_bonus_xp(user_id, reward["diamonds"], reward["coins"], "daily_login", {"login_streak": login_streak})
    return {
        "claimed": True,
        "streak": login_streak,
        "reward": reward,
        "diamonds": reward["diamonds"],
        "coins": reward["coins"],
    }


async def get_achievement_chains(user_id: str) -> dict:
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    badges = profile.get("badges", [])
    achievements = profile.get("achievements", [])
    result = []
    for chain_id, chain in ACHIEVEMENT_CHAINS.items():
        required = set(chain.get("badges_required", []))
        progress = {
            "chain_id": chain_id,
            "name": chain["name"],
            "description": chain["description"],
            "emoji": chain["emoji"],
            "completed": chain_id in achievements,
            "progress": len(required & set(badges)),
            "total": len(required),
            "reward": chain.get("reward"),
        }
        result.append(progress)
    return {"chains": result}
