"""Journey Engine — the canonical orchestrator that determines the highest-value
next action for any student.

Per the architecture strategy doc (AGENTS.md): The Journey Engine sits *above*
the Study Engine and composes its output with career context, company targets,
mastery state, SRS due cards, gamification rewards, and readiness signals.

It does NOT create new engines. It reads from the canonical systems:
  * Study Engine (get_today) — NEXT + REVIEW + PRACTICE + CHALLENGE
  * Gamification (get_gamification_profile) — XP, level, coins, streak
  * Mastery (skill_assessment) — per-skill scores
  * Readiness (readiness_engine) — interview/OA readiness
  * Question Bank (curated_questions) — practice questions
  * World Registry (world_registry) — world/town/level progression
  * Company Blueprints — target company context

The single output is a canonical JourneyState that the frontend consumes,
and the one answer to "What do I do next?"
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.services.gamification import get_gamification_profile
from app.services.study_engine import get_today as study_get_today
from app.services.adaptive_learning import assess_user_skills, detect_weak_areas
from app.services.readiness_engine import calculate_readiness, compute_readiness as get_readiness
from app.content.world_registry import ALL_WORLDS, get_world
from app.database import gamification_collection, skill_graph_collection, \
    curated_questions_collection, users_collection
from app.services.spaced_repetition import get_due_cards, SRSState


router = APIRouter(prefix="/api/v1/journey", tags=["journey"])


# ─── Priority matrix ──────────────────────────────────────────────────
# Higher score = higher priority. These weights are the canonical priority
# engine. They consider SRS debt, company context, prerequisites, and
# recent performance so the student always gets the most meaningful next
# action.

PRIORITY_WEIGHTS = {
    "srs_overdue": 100,
    "failed_repair": 95,
    "prerequisite": 90,
    "company_critical": 85,
    "current_lesson": 80,
    "role_practice": 70,
    "mock_prep": 60,
    "challenge": 40,
    "exploration": 10,
}


# ─── Helpers ──────────────────────────────────────────────────────────


def _user_target_company(user: Dict[str, Any]) -> str:
    """Read target company from user profile, defaulting to ''."""
    return user.get("target_company", "") or user.get("company_target", "") or ""


def _user_career_stage(user: Dict[str, Any]) -> str:
    """Read career stage from user profile."""
    return user.get("career_stage", "placement") or "placement"


def _unlocked(world_id: str, town_id: str, level_id: str,
              completed: Dict[str, Any]) -> bool:
    """Check whether a level is unlocked in the world/town/level graph."""
    wprefix = f"{world_id}:"
    # Find the level's index in walk order
    world = get_world(world_id)
    all_level_ids: List[str] = []
    for town_data in world.towns:
        for lvl in town_data.levels:
            all_level_ids.append(lvl.id)

    level_idx = all_level_ids.index(level_id)
    if level_idx == 0:
        return True
    prev_key = f"{world_id}:{all_level_ids[level_idx - 1]}"
    prev_done = completed.get(prev_key, {}).get("completed", False)
    return prev_done


def _has_mastery_evidence(world_id: str, level_id: str, completed: Dict[str, Any]) -> bool:
    """Check if a level has evidence-based mastery (not just completion).

    Requires:
      1. Level is marked completed
      2. Score >= 70% (passing threshold)
      3. At least 3 steps completed (discover + predict + build/debug)
    """
    key = f"{world_id}:{level_id}"
    entry = completed.get(key, {})
    if not entry.get("completed"):
        return False
    score = entry.get("score", 0)
    steps_done = entry.get("steps_completed", 0)
    return score >= 70 and steps_done >= 3


def _unlocked_evidence_based(world_id: str, town_id: str, level_id: str,
                              completed: Dict[str, Any]) -> bool:
    """Check whether a level is unlocked using evidence-based mastery.

    Previous level must have mastery evidence (not just completion).
    """
    wprefix = f"{world_id}:"
    world = get_world(world_id)
    all_level_ids: List[str] = []
    for town_data in world.towns:
        for lvl in town_data.levels:
            all_level_ids.append(lvl.id)

    level_idx = all_level_ids.index(level_id)
    if level_idx == 0:
        return True
    prev_key = f"{world_id}:{all_level_ids[level_idx - 1]}"
    return _has_mastery_evidence(world_id, all_level_ids[level_idx - 1], completed)


# ─── Core: rank activities for a single student ───────────────────────


async def _rank_activities(user_id: str) -> Dict[str, Any]:
    """Rank all possible next activities by priority and return the winner.

    Returns a dict with per-category scores and the winning activity.
    """
    from app.services.ai import close_http_client  # avoid import cycle at top

    # ── Read user profile ────────────────────────────────────────────
    user = await users_collection().find_one({"user_id": user_id}) or {}
    # Also read from the in-memory get_current_user if available
    try:
        from app.middleware.auth import get_current_user as _gcu
        # get_current_user is a dependency, not a plain function — skip
    except Exception:
        pass

    # Read gamification profile
    g = await get_gamification_profile(user_id)
    completed: Dict[str, Any] = g.get("completed_competencies", {})
    level = g.get("level", 1)
    streak = g.get("streak", 0)
    coins = g.get("coins", 0)

    # Read Study Engine daily plan
    study_plan = await study_get_today(user_id, force_refresh=True)
    next_mission = study_plan.get("next")
    reviews = study_plan.get("reviews", [])
    practice = study_plan.get("practice", [])
    challenge = study_plan.get("challenge")

    # Read mastery/skill assessment
    assessment = await assess_user_skills(user_id)
    skills = assessment.get("skills", {})

    # Read readiness
    readiness = await get_readiness(user_id)
    interview_readiness = readiness.get("interview_readiness", 0)
    oa_readiness = readiness.get("oa_readiness", 0)

    # Read target company
    target_company = _user_target_company(user)

    # Read SRS due cards
    srs_due = await _get_srs_due(user_id)

    # ── Compute priority scores for each activity category ───────────
    scores: Dict[str, int] = {}

    # 1. SRS overdue — highest priority
    if srs_due:
        scores["srs_overdue"] = PRIORITY_WEIGHTS["srs_overdue"]

    # 2. Failed concept repair — if recent failures in skill graph
    failed_repairs = 0
    try:
        sg_doc = await skill_graph_collection().find_one({"user_id": user_id}) or {}
        categories = sg_doc.get("categories", {})
        for cat_name, cat_data in categories.items():
            if isinstance(cat_data, dict) and cat_data.get("score", 0) < 50:
                failed_repairs += 1
    except Exception:
        failed_repairs = 0
    if failed_repairs > 0:
        scores["failed_repair"] = PRIORITY_WEIGHTS["failed_repair"] * min(failed_repairs, 3)

    # 3. Prerequisite check — is the current world progression blocked?
    # Check if student is stuck (no unlocked incomplete levels beyond current)
    world_pos = next(
        (w for w in ALL_WORLDS.values()
         if any(k.startswith(w.id + ":") for k in completed)),
        None
    )
    prerequisite_blocked = False
    if world_pos:
        # Find the student's current position
        for town in world_pos.towns:
            for lvl in town.levels:
                key = f"{world_pos.id}:{lvl.id}"
                if completed.get(key, {}).get("completed"):
                    # Check if there's an unlocked incomplete level after this
                    pass
    # Simplified: if there's a current incomplete unlocked level, no block
    if next(_iter_unlockable(world_pos.id if world_pos else "", completed)):
        prerequisite_blocked = False
    else:
        # Check if all worlds are complete
        if not any(
            not all(
                completed.get(f"{w.id}:{lvl.id}", {}).get("completed", False)
                for town in w.towns
                for lvl in town.levels
            )
            for w in ALL_WORLDS.values()
        ):
            prerequisite_blocked = True

    if not prerequisite_blocked:
        scores["prerequisite"] = PRIORITY_WEIGHTS["prerequisite"]

    # 4. Company-critical weakness — if target company is set, boost
    # weaknesses in skills that company evaluates
    if target_company:
        company_profile = COMPANY_PROFILES.get(target_company.lower(), {})
        # Check if any critical skill for this company is weak
        critical_skills = company_profile.get("critical_skills", [])
        weak_critical = []
        for skill in critical_skills:
            if skill in skills:
                if skills[skill].get("score", 100) < 70:
                    weak_critical.append(skill)
        if weak_critical:
            scores["company_critical"] = PRIORITY_WEIGHTS["company_critical"] * min(
                len(weak_critical), 3)

    # 5. Current lesson — the Study Engine's next mission
    if next_mission:
        scores["current_lesson"] = PRIORITY_WEIGHTS["current_lesson"]

    # 6. Role practice — if we know the user's target role
    target_role = user.get("target_role", "") or user.get("role", "")
    if target_role and target_role != "student":
        # Check if role-specific practice is available
        scores["role_practice"] = PRIORITY_WEIGHTS["role_practice"]

    # 7. Mock preparation — if readiness is below threshold
    if interview_readiness < 70 or oa_readiness < 70:
        scores["mock_prep"] = PRIORITY_WEIGHTS["mock_prep"]

    # 8. Challenge — if student is ready (3+ mastered skills)
    mastered_count = sum(
        1 for s in skills.values()
        if s.get("mastery", "") in ("competent", "proficient", "master")
    )
    if mastered_count >= 3 and challenge:
        scores["challenge"] = PRIORITY_WEIGHTS["challenge"]

    # 9. Exploration — low priority optional
    # Only if there's "free time" (low total priority from other categories)
    if not scores and challenge is None:
        scores["exploration"] = PRIORITY_WEIGHTS["exploration"]

    # ── Select the winner ────────────────────────────────────────────
    winner_category = max(scores, key=scores.get) if scores else "exploration"
    winner_score = scores.get(winner_category, 0)

    return {
        "scores": scores,
        "winner_category": winner_category,
        "winner_score": winner_score,
        "target_company": target_company,
        "interview_readiness": interview_readiness,
        "oa_readiness": oa_readiness,
        "mastered_count": mastered_count,
        "prerequisite_blocked": prerequisite_blocked,
    }


async def _iter_unlockable(world_id: str, completed: Dict[str, Any]):
    """Yield (world, town, level) tuples for the first unlocked incomplete level."""
    from app.content.world_registry import ALL_WORLDS
    world = get_world(world_id) if world_id else None
    if not world:
        for w in ALL_WORLDS.values():
            async for result in _iter_unlockable(w.id, completed):
                yield result
        return

    all_level_ids: List[str] = []
    for town_data in world.towns:
        for lvl in town_data.levels:
            all_level_ids.append(lvl.id)

    seen_complete = True
    for town_data in world.towns:
        for lvl in town_data.levels:
            key = f"{world.id}:{lvl.id}"
            done = completed.get(key, {}).get("completed", False)
            if done:
                continue
            if not seen_complete:
                continue
            yield {"world_id": world.id, "town_id": town_data.id, "level_id": lvl.id}
            seen_complete = all(
                completed.get(f"{world.id}:{lvl2.id}", {}).get("completed", False)
                for lvl2 in town_data.levels
            )


# ─── Build the canonical JourneyState ─────────────────────────────────


async def build_journey_state(user_id: str) -> Dict[str, Any]:
    """Build the canonical JourneyState for the given user.

    This is the single entry point the frontend uses to determine:
      - Where the student is (character position)
      - What they should do next (priority action)
      - What reviews are due
      - What practice/challenge is available
      - Career readiness + company context

    The Study Engine provides the learning activities; the Journey Engine
    adds career context and ranks everything into a single next action.
    """

    # ── Rank activities and get winner ───────────────────────────────
    ranking = await _rank_activities(user_id)
    winner = ranking["winner_category"]
    scores = ranking["scores"]

    # ── Read user profile for context ────────────────────────────────
    from app.middleware.auth import get_current_user as _gcu_dep
    # We can't call the dependency directly, read from DB instead
    from app.database import users_collection as _uc
    user_doc = await _uc().find_one({"user_id": user_id}) or {}
    target_company = _user_target_company(user_doc)
    target_role = user_doc.get("target_role", "") or user_doc.get("role", "")

    # ── Re-read Study Engine plan (already refreshed in _rank_activities) ─
    # We already have it from _rank_activities; reuse where possible
    # For the full state, call study engine fresh:
    study_plan = await study_get_today(user_id, force_refresh=True)
    next_mission = study_plan.get("next")
    reviews = study_plan.get("reviews", [])
    practice = study_plan.get("practice", [])
    challenge = study_plan.get("challenge")

    # ── Read gamification ────────────────────────────────────────────
    g = await get_gamification_profile(user_id)
    level = g.get("level", 1)
    xp = g.get("xp", 0)
    coins = g.get("coins", 0)
    streak = g.get("streak", 0)
    badges = g.get("badges", [])

    # ── Read world/progression state ─────────────────────────────────
    # Find the character position: first unlocked incomplete level
    completed: Dict[str, Any] = g.get("completed_competencies", {})
    character_position = None

    # Walk worlds in order to find standing position
    for world in sorted(ALL_WORLDS.values(), key=lambda w: w.order):
        wprefix = world.id + ":"
        world_keys = [k for k in completed if k.startswith(wprefix)]
        if not world_keys:
            continue  # locked world

        # Check towns and levels
        for town in world.towns:
            town_levels = town.levels
            for idx, lvl in enumerate(town_levels):
                key = f"{world.id}:{lvl.id}"
                entry = completed.get(key, {})
                is_done = bool(entry.get("completed"))

                # Unlock rule
                all_level_ids = []
                for t in world.towns:
                    for lt in t.levels:
                        all_level_ids.append(lt.id)
                walk_idx = all_level_ids.index(lvl.id)
                if walk_idx == 0:
                    unlocked = True
                else:
                    prev_key = f"{world.id}:{all_level_ids[walk_idx - 1]}"
                    unlocked = bool(completed.get(prev_key, {}).get("completed"))

                if is_done:
                    status = "completed"
                elif unlocked and character_position is None:
                    status = "current"
                    character_position = {
                        "world_id": world.id,
                        "town_id": town.id,
                        "level_id": lvl.id,
                    }
                elif unlocked:
                    status = "unlocked"
                else:
                    status = "locked"

                # Don't override character_position if already set
                if character_position and (
                    character_position["world_id"] != world.id or
                    character_position["town_id"] != town.id or
                    character_position["level_id"] != lvl.id
                ):
                    # Already set, just continue
                    pass

        # If we found the character position, stop looking
        if character_position:
            break

    # Fallback: if nothing incomplete, stand on the last level of the last world
    if character_position is None:
        for world in sorted(ALL_WORLDS.values(), key=lambda w: w.order):
            world_keys = [k for k in completed if k.startswith(world.id + ":")]
            if world_keys and world.towns:
                last_town = world.towns[-1]
                if last_town.levels:
                    last_lvl = last_town.levels[-1]
                    character_position = {
                        "world_id": world.id,
                        "town_id": last_town.id,
                        "level_id": last_lvl.id,
                    }
                    break

    # ── Determine the single next action ─────────────────────────────
    # Based on the winner category from the priority engine:
    next_action: Dict[str, Any] = {}
    today = _today_key()

    if winner == "srs_overdue" and reviews:
        next_action = {
            "type": "review",
            "title": "Review SRS Cards",
            "description": f"{len(reviews)} spaced-repetition cards due",
            "kind": "srs",
            "estimated_minutes": sum(r.get("estimated_minutes", 5) for r in reviews),
            "xp_reward": 10 * len(reviews),
            "action": "review",
        }
    elif winner == "failed_repair":
        # Show the weakest skill needing repair
        weakest = min(
            (s for s in skills.values() if s.get("score", 100) < 70),
            key=lambda s: s.get("score", 100),
            default=None,
        )
        if weakest:
            next_action = {
                "type": "repair",
                "title": f"Repair {weakest.get('name', 'skill')}",
                "description": "This concept needs reinforcement",
                "kind": "mastery_repair",
                "skill_id": weakest.get("skill_id", ""),
                "estimated_minutes": 15,
                "xp_reward": 25,
                "action": "mastery_repair",
            }
    elif winner == "prerequisite":
        # Show the next unlockable level
        if character_position:
            w = get_world(character_position["world_id"])
            town = next(t for t in w.towns if t.id == character_position["town_id"])
            current_idx = None
            for i, lvl in enumerate(town.levels):
                if lvl.id == character_position["level_id"]:
                    current_idx = i
                    break
            if current_idx is not None and current_idx < len(town.levels) - 1:
                next_lvl = town.levels[current_idx + 1]
                next_action = {
                    "type": "unlock",
                    "title": f"Unlock: {next_lvl.title}",
                    "description": f"Move from {town.title} to {next_lvl.title}",
                    "kind": "progression",
                    "target_world": character_position["world_id"],
                    "target_town": character_position["town_id"],
                    "target_level": next_lvl.id,
                    "estimated_minutes": next_lvl.xp // 5 + 10,
                    "xp_reward": next_lvl.xp,
                    "action": "progression_unlock",
                }
            else:
                # Move to next town or world
                next_action = {
                    "type": "explore",
                    "title": "Continue Journey",
                    "description": "Move to the next area",
                    "kind": "progression",
                    "estimated_minutes": 5,
                    "xp_reward": 15,
                    "action": "progression",
                }
    elif winner == "current_lesson" and next_mission:
        next_action = {
            "type": "learn",
            "title": next_mission.get("title", "Lesson"),
            "description": next_mission.get("description", "Learn new concept"),
            "kind": "lesson",
            "world": next_mission.get("world", {}).get("id", ""),
            "town": next_mission.get("town", {}).get("id", ""),
            "level": next_mission.get("level", {}).get("id", ""),
            "estimated_minutes": next_mission.get("estimated_minutes", 12),
            "xp_reward": next_mission.get("xp_reward", 50),
            "lesson_content": next_mission.get("lesson_content"),
            "action": "learn_mission",
        }
    elif winner == "role_practice" and target_role:
        next_action = {
            "type": "practice",
            "title": f"Role Practice: {target_role}",
            "description": f"Practice problems aligned with {target_role}",
            "kind": "role_practice",
            "estimated_minutes": 20,
            "xp_reward": 30,
            "action": "role_practice",
        }
    elif winner == "mock_prep" and (ranking["interview_readiness"] < 70 or ranking["oa_readiness"] < 70):
        # Generate mock OA or interview session
        next_action = {
            "type": "mock_assessment",
            "title": "Mock Assessment",
            "description": "Test your readiness with a simulated assessment",
            "kind": "mock_oa",
            "estimated_minutes": 45,
            "xp_reward": 100,
            "target_company": target_company,
            "action": "mock_assessment",
        }
    elif winner == "challenge" and challenge:
        next_action = {
            "type": "challenge",
            "title": challenge.get("title", "Debugging Sprint"),
            "description": challenge.get("description", "Timed challenge"),
            "kind": "timed_challenge",
            "estimated_minutes": challenge.get("estimated_minutes", 12),
            "xp_reward": challenge.get("xp_reward", 60),
            "skill": challenge.get("skill", ""),
            "action": "challenge",
        }
    else:
        # Default: exploration / continue journey
        next_action = {
            "type": "explore",
            "title": "Continue Journey",
            "description": "Keep learning and progressing",
            "kind": "exploration",
            "estimated_minutes": 10,
            "xp_reward": 15,
            "action": "explore",
        }

    # ── Build and return the canonical JourneyState ──────────────────
    journey_state: Dict[str, Any] = {
        "character": {
            "level": level,
            "title": _title_for_level(level),
            "title_emoji": _emoji_for_level(level),
            "position": character_position or {"world_id": "", "town_id": "", "level_id": ""},
            "state": "idle",
        },
        "today": {
            "date": today,
            "next": next_action,
            "reviews": reviews,
            "practice": practice,
            "challenge": challenge,
        },
        "stats": {
            "xp": xp,
            "level": level,
            "coins": coins,
            "streak": streak,
            "badges_count": len(badges),
        },
        "readiness": {
            "interview_readiness": ranking["interview_readiness"],
            "oa_readiness": ranking["oa_readiness"],
            "mastered_count": ranking["mastered_count"],
        },
        "company": {
            "target": target_company,
            "target_role": target_role,
        },
        "priority": {
            "winner_category": winner,
            "scores": scores,
            "winner_score": ranking["winner_score"],
        },
    }

    return journey_state


def _today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _title_for_level(level: int) -> Dict[str, Any]:
    """Return character title info for a given level."""
    CHARACTER_TITLES = [
        {"min_level": 1, "title": "Rookie", "emoji": "🌱"},
        {"min_level": 10, "title": "Explorer", "emoji": "🧭"},
        {"min_level": 20, "title": "Problem Solver", "emoji": "🧩"},
        {"min_level": 30, "title": "Builder", "emoji": "🛠"},
        {"min_level": 40, "title": "Engineer", "emoji": "⚙️"},
        {"min_level": 50, "title": "Developer", "emoji": "🚀"},
        {"min_level": 60, "title": "Specialist", "emoji": "🧠"},
        {"min_level": 70, "title": "Architect", "emoji": "🏗"},
        {"min_level": 80, "title": "Senior Engineer", "emoji": "⚡"},
        {"min_level": 90, "title": "Expert", "emoji": "👑"},
        {"min_level": 100, "title": "Master Engineer", "emoji": "🌌"},
    ]
    pick = CHARACTER_TITLES[0]
    for t in CHARACTER_TITLES:
        if level >= t["min_level"]:
            pick = t
    return pick


def _emoji_for_level(level: int) -> str:
    return _title_for_level(level)["emoji"]


# ─── Router endpoint ──────────────────────────────────────────────────

@router.get("/state", summary="Return the canonical journey state for the user.")
async def journey_state_endpoint(user=Depends(get_current_user)):
    """Return the canonical JourneyState for the authenticated user.

    This is the single source of truth the frontend uses to render:
      - The student's character position on the world map
      - Today's next action (the answer to "What do I do next?")
      - SRS reviews due
      - Practice tasks
      - Optional challenge
      - Career readiness + company context
      - Priority scoring so the student understands why this action

    The Journey Engine composes from:
      * Study Engine (daily plan: NEXT + REVIEW + PRACTICE + CHALLENGE)
      * Gamification (XP, level, coins, streak)
      * Mastery (per-skill scores)
      * Readiness (interview + OA readiness)
      * Company blueprints (target company context)
      * World Registry (progression graph)

    Result: one canonical state, one next action, no ambiguity.
    """
    user_id = user["id"]
    state = await build_journey_state(user_id)

    # Cache for the day (state is deterministic unless user progress changes)
    try:
        from app.services.cache import cache
        import json as _json
        cached = await cache.get("journey", f"state:{user_id}:{_today_key()}")
        if cached:
            # Don't return cached if we just computed a new state —
            # the cache is best-effort for performance, not for correctness.
            pass
    except Exception:
        pass

    return {"success": True, "data": state}