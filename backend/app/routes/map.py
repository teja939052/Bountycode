"""Adventure Map — thin presentation layer over canonical systems.

Composes (never duplicates):
- Worlds registry (``app.data.worlds_data.WORLD_REGISTRY``) — WHAT is learned
- Progress helpers from ``app.routes.worlds`` — unlock rule + evidence
  (``completed_competencies`` in the gamification collection)
- Gamification profile — Diamonds/level/coins/streak (single rewarder)

No new collections. No new Diamonds math. No new curriculum engine. No writes:
completion still flows through ``POST /api/v1/worlds/.../complete``,
``POST /api/v1/lesson/.../complete`` and ``POST /api/v1/study/activity``,
both of which are idempotent against retry/double-tap.

Returns deterministic serpentine (x,y) node positions, fog-of-war horizon
(next 8 visible), 1-3 stars from evidence (best score + hints), plus the
per-node evidence (attempts / failed attempts / hints) so a student who
struggled through a repair loop looks different from a first-pass clear.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query

from app.data.worlds_data import WORLD_REGISTRY
from app.middleware.auth import get_current_user
from app.routes.worlds import (
    _all_level_ids,
    _get_completed,
    _is_unlocked,
    get_world,
    is_world_unlocked,
    stars_for_entry,
    world_progress,
)
from app.services.gamification import get_gamification_profile

router = APIRouter(prefix="/api/v1/map", tags=["map", "adventure"])

# Adventure identity — presentation only, never a new curriculum.
# Every world is a different place: name + color + terrain + BGM mood.
WORLD_ADVENTURE_NAMES = {
    "foundations": "Boot Camp",
    "searchlands": "Pirate Cove",
    "sorting": "Blacksmith Isle",
    "recursion": "Skull Peaks",
    "linked": "Chain Islands",
    "stack": "Cannon Tower",
    "queue": "Harbor Plaza",
    "hashing": "Treasure Harbor",
    "trees": "Jungle Isle",
    "graphs": "Serpent Sea",
    "dynamic": "Monsoon Delta",
    "alpine": "Kraken Summit",
}

WORLD_THEMES = {
    "foundations": {"color": "#22C55E", "terrain": "beach", "bgm": "meadow"},
    "searchlands": {"color": "#3B82F6", "terrain": "cove", "bgm": "pirate"},
    "sorting": {"color": "#D97706", "terrain": "forge", "bgm": "plains"},
    "recursion": {"color": "#A855F7", "terrain": "peaks", "bgm": "embers"},
    "linked": {"color": "#14B8A6", "terrain": "chain", "bgm": "plains"},
    "stack": {"color": "#EAB308", "terrain": "tower", "bgm": "plains"},
    "queue": {"color": "#06B6D4", "terrain": "plaza", "bgm": "plains"},
    "hashing": {"color": "#0891B2", "terrain": "harbor", "bgm": "pirate"},
    "trees": {"color": "#16A34A", "terrain": "jungle", "bgm": "meadow"},
    "graphs": {"color": "#7C3AED", "terrain": "sea", "bgm": "pirate"},
    "dynamic": {"color": "#EC4899", "terrain": "delta", "bgm": "embers"},
    "alpine": {"color": "#EF4444", "terrain": "summit", "bgm": "embers"},
}

_DEFAULT_THEME = {"color": "#22C55E", "terrain": "meadow", "bgm": "meadow"}


def _world_summary(world, completed: Dict[str, Any]) -> Dict[str, Any]:
    # Gate rule lives in routes.worlds (single source of truth shared with
    # the attempt/hint/complete endpoints); this layer only presents it.
    prog = world_progress(world.id, completed)
    if prog["total"] and prog["done"] >= prog["total"]:
        status = "completed"
    elif prog["done"] > 0:
        status = "active"
    elif is_world_unlocked(world.id, completed):
        status = "unlocked"
    else:
        status = "locked"
    return {
        "id": world.id,
        "adventure_name": WORLD_ADVENTURE_NAMES.get(world.id, world.name),
        "title": world.name,
        "theme": WORLD_THEMES.get(world.id, _DEFAULT_THEME),
        "status": status,
        "done": prog["done"],
        "total": prog["total"],
        "order": world.order,
    }

HORIZON_VISIBLE_AHEAD = 8


def _serpentine_xy(index: int, total: int, width: float = 340.0, height: float = 620.0) -> Dict[str, float]:
    """Deterministic winding path positions. Author-tuned curve, no auto-DAG."""
    if total <= 1:
        return {"x": width / 2, "y": height - 60}
    f = index / (total - 1)
    y = (height - 60) - f * (height - 120)
    swing = math.sin(f * math.pi * 3.2) * (width * 0.32)
    x = width / 2 + swing
    x = max(48.0, min(width - 48.0, x))
    return {"x": round(x, 1), "y": round(y, 1)}


# Thin alias: the single source lives in routes.worlds.stars_for_entry.
_stars_for_entry = stars_for_entry


def _pick_default_world(completed: Dict[str, Any]):
    """First world (by order) with an unfinished unlocked level, else foundations."""
    ordered = sorted(WORLD_REGISTRY.values(), key=lambda w: w.order)
    for world in ordered:
        all_ids = _all_level_ids(world)
        for lid in all_ids:
            prog = completed.get(f"{world.id}:{lid}", {})
            if not prog.get("completed") and _is_unlocked(lid, all_ids, completed, world.id):
                return world
    return WORLD_REGISTRY.get("foundations") or ordered[0]


def _campfire_node(world_id: str, due_count: int) -> Dict[str, Any]:
    """Transient rest node. Never persisted: it exists in the response only
    while SRS cards are actually due, and vanishes once reviews clear."""
    return {
        "node_id": f"{world_id}:campfire_rest",
        "level_id": "campfire_rest",
        "town_id": "",
        "title": "Campfire Rest",
        "kind": "srs_campfire",
        "position": {"x": 0.0, "y": 0.0},  # assigned with all nodes below
        "path_next": [],
        "status": "unlocked",
        "stars": 0,
        "mastery": 0.0,
        "score": 0.0,
        "best_score": 0.0,
        "attempts": 0,
        "failed_attempts": 0,
        "hints_used": 0,
        "recovered": False,
        "diamonds": 0,
        "visible": True,
        "fogged": False,
        "is_current": False,
        "is_boss": False,
        "due_count": due_count,
    }


TRANSIENT_KINDS = {"srs_campfire", "repair"}


def _should_offer_repair(entry: Dict[str, Any]) -> bool:
    """Deterministic struggle trigger: failed attempt(s) or heavy hint use.

    Mirrors the spec (wrong answer OR >= 2 hints): the branch appears only
    from real evidence on the current node, never from a schedule.
    """
    if entry.get("completed"):
        return False
    failed = int(entry.get("failed_attempts", 0) or 0)
    hints = len(entry.get("hints_used", []) or [])
    return failed >= 1 or hints >= 2


def _repair_node(
    world_id: str,
    level_id: str,
    town_id: str,
    parent_title: str,
    weak_label: Optional[str],
    parent_pos: Dict[str, float],
) -> Dict[str, Any]:
    """Transient repair detour. Never persisted: it exists only while the
    parent node shows struggle evidence, and completing the parent clears
    it automatically (the trigger re-evaluates every fetch)."""
    x = max(48.0, min(292.0, parent_pos["x"] + 72.0))
    label = f"Repair: {weak_label}" if weak_label else "Repair: steady the basics"
    return {
        "node_id": f"{world_id}:{level_id}_repair",
        "level_id": level_id,
        "town_id": town_id,
        "title": label,
        "kind": "repair",
        "position": {"x": round(x, 1), "y": round(max(60.0, parent_pos["y"] - 6.0), 1)},
        "path_next": [f"{world_id}:{level_id}"],  # merge back onto the parent
        "status": "unlocked",
        "stars": 0,
        "mastery": 0.0,
        "score": 0.0,
        "best_score": 0.0,
        "attempts": 0,
        "failed_attempts": 0,
        "hints_used": 0,
        "recovered": False,
        "diamonds": 0,
        "visible": True,
        "fogged": False,
        "is_current": False,
        "is_boss": False,
        "is_branch": True,
        "branch_from": f"{world_id}:{level_id}",
        "parent_title": parent_title,
    }


def _inject_campfire(nodes: List[Dict[str, Any]], due_count: int) -> int:
    """Insert a campfire node immediately before the first boss node.

    Returns the insertion index, or -1 when there is nothing to protect
    (no boss in this world) or nothing due. Positions and path chains are
    (re)assigned by the caller AFTER injection so the path stays continuous.
    """
    if due_count <= 0:
        return -1
    for i, node in enumerate(nodes):
        if node.get("is_boss"):
            nodes.insert(i, _campfire_node(node["node_id"].split(":")[0], due_count))
            return i
    return -1


@router.get("/state")
async def map_state(
    world_id: Optional[str] = Query(default=None, max_length=64),
    user=Depends(get_current_user),
) -> Dict[str, Any]:
    completed = await _get_completed(user["id"])
    world = get_world(world_id) if world_id else _pick_default_world(completed)

    all_ids = _all_level_ids(world)
    flat: List[Any] = []
    for town in sorted(world.towns, key=lambda t: t.order):
        for lvl in sorted(town.levels, key=lambda l: l.order):
            flat.append({"town": town, "level": lvl})
    total = len(flat)

    # Character position: first unlocked incomplete level; stand on the last
    # node when everything is cleared. Never indexes past the end: when the
    # authored content runs out, the path simply ends (no fog over void).
    current_idx = 0
    for i, item in enumerate(flat):
        key = f"{world.id}:{item['level'].id}"
        done = bool(completed.get(key, {}).get("completed"))
        if done:
            current_idx = min(total - 1, i + 1)
            continue
        if _is_unlocked(item["level"].id, all_ids, completed, world.id):
            current_idx = i
            break
        current_idx = min(total - 1, i + 1)

    nodes: List[Dict[str, Any]] = []
    for i, item in enumerate(flat):
        lvl = item["level"]
        town = item["town"]
        key = f"{world.id}:{lvl.id}"
        entry = completed.get(key, {})
        done = bool(entry.get("completed"))
        unlocked = done or _is_unlocked(lvl.id, all_ids, completed, world.id)
        status = "completed" if done else ("current" if i == current_idx else ("unlocked" if unlocked else "locked"))
        attempts = int(entry.get("attempts", 0) or 0)
        failed = int(entry.get("failed_attempts", 0) or 0)
        hints = entry.get("hints_used", []) or []
        nodes.append({
            "node_id": key,
            "level_id": lvl.id,
            "town_id": town.id,
            "title": lvl.title,
            "kind": "world_boss" if (lvl.kind == "boss" and i == total - 1) else ("mini_boss" if lvl.kind == "boss" else "battle"),
            "position": {"x": 0.0, "y": 0.0},  # assigned after campfire injection
            "path_next": [],
            "status": status,
            "stars": _stars_for_entry(entry),
            "mastery": float(entry.get("best_score", 0) or 0),
            "score": float(entry.get("score", 0) or 0),
            "best_score": float(entry.get("best_score", 0) or 0),
            "attempts": attempts,
            "failed_attempts": failed,
            "hints_used": len(hints),
            # A recovered student (failed then cleared) renders differently
            # from a first-pass clear — same systems, honest signal.
            "recovered": done and (failed > 0 or attempts > 1),
            "diamonds": lvl.success.diamonds if getattr(lvl, "success", None) else 0,
            "visible": True,  # recomputed after injection below
            "fogged": False,
            "is_current": i == current_idx,
            "is_boss": lvl.kind == "boss",
        })

    # Campfire: transient SRS rest-stop before the boss. Best-effort and
    # read-only — SRS state is never written here, and the node disappears
    # the moment reviews clear. A nudge, never a gate: path order and the
    # unlock rule are untouched.
    due_count = 0
    try:
        from app.services.study_engine import _get_due_reviews
        due_count = len(await _get_due_reviews(user["id"], limit=5) or [])
    except Exception:
        due_count = 0
    camp_at = _inject_campfire(nodes, due_count)
    if camp_at >= 0 and current_idx >= camp_at:
        current_idx += 1

    total = len(nodes)
    for i, node in enumerate(nodes):
        node["position"] = _serpentine_xy(i, total)
        node["path_next"] = [nodes[i + 1]["node_id"]] if i + 1 < total else []
        node["visible"] = i <= current_idx + HORIZON_VISIBLE_AHEAD
        node["fogged"] = not node["visible"]
        node["is_current"] = (i == current_idx)

    # Repair detour: transient branch off the struggling node. Best-effort
    # and read-only — a nudge, never a gate: the main path, unlock rule and
    # current position are untouched, and clearing the parent dissolves it.
    repair_node: Optional[Dict[str, Any]] = None
    if nodes and 0 <= current_idx < len(nodes):
        parent = nodes[current_idx]
        if parent.get("kind") not in TRANSIENT_KINDS:
            parent_entry = completed.get(parent["node_id"], {})
            if _should_offer_repair(parent_entry):
                weak_label = None
                try:
                    from app.services.skill_assessment import get_weak_areas
                    _weak = await get_weak_areas(user["id"], top_n=5) or []
                    _weak = [w for w in _weak if (w.get("score", 100) or 0) < 70]
                    if _weak:
                        weak_label = _weak[0].get("skill") or _weak[0].get("category_name")
                except Exception:
                    weak_label = None
                repair_node = _repair_node(
                    world.id, parent["level_id"], parent["town_id"],
                    parent["title"], weak_label, parent["position"],
                )
                repair_node["visible"] = parent["visible"]
                repair_node["fogged"] = parent["fogged"]
                nodes.append(repair_node)

    total = len(nodes)
    visible_count = sum(1 for n in nodes if n["visible"])
    profile = await get_gamification_profile(user["id"])

    level_nodes = [n for n in nodes if n.get("kind") not in TRANSIENT_KINDS]
    done_count = sum(1 for n in level_nodes if n["status"] == "completed")
    world_status = "completed" if level_nodes and done_count == len(level_nodes) else (
        "active" if done_count or world.id == "foundations" else "locked"
    )

    all_worlds = [
        _world_summary(w, completed)
        for w in sorted(WORLD_REGISTRY.values(), key=lambda w: w.order)
    ]
    # Keep single-world status consistent with the summary table.
    _self = next((s for s in all_worlds if s["id"] == world.id), None)
    if _self is not None:
        world_status = _self["status"]

    return {
        "world": {
            "id": world.id,
            "adventure_name": WORLD_ADVENTURE_NAMES.get(world.id, world.name),
            "title": world.name,
            "theme": WORLD_THEMES.get(world.id, _DEFAULT_THEME),
            "status": world_status,
        },
        "all_worlds": all_worlds,
        "nodes": nodes,
        "character": {
            "node_index": current_idx,
            "node_id": nodes[current_idx]["node_id"] if nodes else None,
        },
        "stats": {
            "diamonds": profile.get("diamonds", 0),
            "level": profile.get("level", 1),
            "coins": profile.get("coins", 0),
            "streak": profile.get("streak", 0),
            "badges_count": len(profile.get("badges", [])),
        },
        "horizon": HORIZON_VISIBLE_AHEAD,
        "total": total,
        "visible_count": visible_count,
        "fogged_count": total - visible_count,
        "campfire": {"due_count": due_count} if due_count > 0 else None,
        # Completion still uses existing canonical endpoints — listed here so
        # clients never invent a new write path.
        "complete_via": {
            "worlds": "POST /api/v1/worlds/{world_id}/levels/{level_id}/complete",
            "foundations_lesson": "POST /api/v1/lesson/{slug}/complete",
            "default": "POST /api/v1/study/activity",
            "reward": "POST /api/v1/gamification/record",
        },
    }
