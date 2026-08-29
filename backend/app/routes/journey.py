"""Journey State — the canonical endpoint for the unified journey game layer.

This supersedes the old ``journey.py`` + ``progression_systems`` + ``foundations_world``
stack.  The new JourneyState is *derived* from the canonical systems:

* ``WORLD_REGISTRY`` (``routes/worlds.py``) — world / town / level structure.
* ``gamification_collection.completed_competencies`` — per-level completion.
* ``gamification_collection`` — XP, level, coins, streak.
* ``Study Engine`` (``services/study_engine.py``) — today's recommended activity.

The result is a single ``GET /api/v1/journey/state`` payload that the frontend
renders as a vertical scrolling adventure map with a character whose position
is driven by *actual learning progress*, not animation.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user
from app.content.world_registry import ALL_WORLDS, get_world
from app.services.gamification import get_gamification_profile
from app.services.study_engine import get_today

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/journey", tags=["journey"])


# ─── Character title table (clean 11-tier progression) ─────────────
# Mirrors the gamification ``TOWER_TITLES`` but exposes a smaller, cleaner
# set for the journey UI.  The underlying gamification level is unchanged.

CHARACTER_TITLES: List[Dict[str, Any]] = [
    {"min_level": 1,   "title": "Rookie",          "emoji": "🌱"},
    {"min_level": 10,  "title": "Explorer",        "emoji": "🧭"},
    {"min_level": 20,  "title": "Problem Solver",  "emoji": "🧩"},
    {"min_level": 30,  "title": "Builder",         "emoji": "🛠"},
    {"min_level": 40,  "title": "Engineer",        "emoji": "⚙️"},
    {"min_level": 50,  "title": "Developer",       "emoji": "🚀"},
    {"min_level": 60,  "title": "Specialist",      "emoji": "🧠"},
    {"min_level": 70,  "title": "Architect",       "emoji": "🏗"},
    {"min_level": 80,  "title": "Senior Engineer", "emoji": "⚡"},
    {"min_level": 90,  "title": "Expert",          "emoji": "👑"},
    {"min_level": 100, "title": "Master Engineer", "emoji": "🌌"},
]


def _title_for_level(level: int) -> Dict[str, Any]:
    pick = CHARACTER_TITLES[0]
    for t in CHARACTER_TITLES:
        if level >= t["min_level"]:
            pick = t
    return pick


# ─── World status helper ────────────────────────────────────────────

def _world_status(world_id: str, completed: Dict[str, Any]) -> str:
    """Return ``completed``, ``active``, or ``locked`` for a world."""
    wprefix = world_id + ":"
    world_keys = [k for k in completed if k.startswith(wprefix)]
    if not world_keys:
        return "locked"
    all_done = all(
        completed.get(f"{world_id}:{lvl.id}", {}).get("completed")
        for town in get_world(world_id).towns
        for lvl in town.levels
    )
    return "completed" if all_done else "active"


# ─── Main endpoint ──────────────────────────────────────────────────

@router.get("/state")
async def journey_state(user=Depends(get_current_user)):
    """Return the full journey state for the authenticated user.

    Shape::

        {
          "character": { "level", "title", "title_emoji", "position", "state" },
          "worlds":    [ { "id", "title", "icon", "status", "towns": [ ... ] } ],
          "today":     { "next", "reviews", "practice", "challenge" },
          "stats":     { "xp", "level", "coins", "streak" }
        }
    """
    user_id = user["id"]
    now = datetime.now(timezone.utc)

    # ── Progress + gamification context ──
    g = await get_gamification_profile(user_id)
    completed: Dict[str, Any] = g.get("completed_competencies", {})
    level = g.get("level", 1)
    title_info = _title_for_level(level)

    # ── Study Engine's recommendation ──
    try:
        today = await get_today(user_id)
    except Exception as exc:
        logger.warning("Study Engine unavailable for %s: %s", user_id, exc)
        today = None

    # ── Build the world map with per-level status ──
    worlds_out: List[Dict[str, Any]] = []
    character_position: Optional[Dict[str, Any]] = None

    for world in sorted(ALL_WORLDS.values(), key=lambda w: w.order):
        wprefix = world.id + ":"
        towns_out: List[Dict[str, Any]] = []

        # Collect all level ids in walk order for unlock computation.
        all_level_ids: List[str] = []
        for town in world.towns:
            for lvl in town.levels:
                all_level_ids.append(lvl.id)

        for town in world.towns:
            levels_out: List[Dict[str, Any]] = []
            for idx, lvl in enumerate(town.levels):
                key = f"{world.id}:{lvl.id}"
                entry = completed.get(key, {})
                is_done = bool(entry.get("completed"))

                # Unlock rule: first level is always unlocked; every other
                # level is unlocked when the *previous* level (in walk order)
                # is completed.
                walk_idx = all_level_ids.index(lvl.id)
                if walk_idx == 0:
                    unlocked = True
                else:
                    prev_key = f"{world.id}:{all_level_ids[walk_idx - 1]}"
                    unlocked = bool(completed.get(prev_key, {}).get("completed"))

                if is_done:
                    status = "completed"
                elif unlocked:
                    status = "current" if character_position is None else "unlocked"
                else:
                    status = "locked"

                # The first unlocked, incomplete level is where the character
                # stands.
                if status == "current" and character_position is None:
                    character_position = {
                        "world_id": world.id,
                        "town_id": town.id,
                        "level_id": lvl.id,
                    }

                levels_out.append({
                    "id": lvl.id,
                    "title": lvl.title,
                    "icon": getattr(lvl, "icon", "📄"),
                    "kind": lvl.kind,
                    "order": lvl.order,
                    "concept": getattr(lvl, "concept", ""),
                    "canonical_skill": getattr(lvl, "canonical_skill", ""),
                    "status": status,
                    "mastery": entry.get("score", 0) if is_done else 0,
                    "attempts": entry.get("attempts", 0),
                    "xp": getattr(lvl.success, "xp", 50) if hasattr(lvl, "success") else 50,
                })

            towns_out.append({
                "id": town.id,
                "title": town.name,
                "icon": getattr(town, "icon", "🏠"),
                "order": town.order,
                "levels": levels_out,
            })

        worlds_out.append({
            "id": world.id,
            "title": world.name,
            "subtitle": getattr(world, "subtitle", ""),
            "icon": getattr(world, "icon", "🌍"),
            "order": world.order,
            "theme": getattr(world, "theme", "default"),
            "status": _world_status(world.id, completed),
            "towns": towns_out,
        })

    # Fallback position: if nothing is incomplete, stand on the last level.
    if character_position is None and worlds_out:
        last_world = worlds_out[0]
        if last_world["towns"]:
            last_town = last_world["towns"][-1]
            if last_town["levels"]:
                last_lvl = last_town["levels"][-1]
                character_position = {
                    "world_id": last_world["id"],
                    "town_id": last_town["id"],
                    "level_id": last_lvl["id"],
                }

    return {
        "character": {
            "level": level,
            "title": title_info["title"],
            "title_emoji": title_info["emoji"],
            "position": character_position,
            "state": "idle",
        },
        "worlds": worlds_out,
        "today": today,
        "stats": {
            "xp": g.get("xp", 0),
            "level": level,
            "coins": g.get("coins", 0),
            "streak": g.get("streak", 0),
            "badges_count": len(g.get("badges", [])),
        },
    }
