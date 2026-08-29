"""Worlds — generic World → Town → Level → Boss learning game layer.

World
  → Town[]
       → Level[] + Boss

Persistence
  completed_competencies["<world_id>:<level_id>"] in gamification collection
  skill_graph via update_skill_score (category derived from canonical_skill)
  XP via record_practice(activity_type=<world_id>)
  SRS via srs_cards_collection (canonical spaced_repetition)

Routes (all under /api/v1/worlds, auth required):
  GET  /{world_id}                  → world definition + user progress overlay
  GET  /{world_id}/progress         → progress only (character pos, unlocked)
  POST /{world_id}/levels/{id}/attempt  → deterministic judge + hint ladder
  POST /{world_id}/levels/{id}/complete → mark done, XP, mastery, unlock
  POST /{world_id}/levels/{id}/hint     → record hint usage (instrumentation)
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.data.worlds_data import WORLD_REGISTRY
from app.database import gamification_collection, skill_graph_collection
from app.middleware.auth import get_current_user
from app.models.world import (
    Boss,
    BreakStep,
    Build,
    Code,
    Debug,
    Discover,
    Level,
    LevelBase,
    Manipulate,
    Predict,
    Retrieval,
    Story,
    Success,
    Town,
    Transfer,
    Tutor,
    World,
)

router = APIRouter(prefix="/api/v1/worlds", tags=["Worlds"])



def get_world(world_id: str) -> World:
    world = WORLD_REGISTRY.get(world_id)
    if not world:
        raise HTTPException(status_code=404, detail=f"Unknown world: {world_id}")
    return world


# ─────────────────────────────────────────────
# Generic helpers (no longer hardcoded to "foundations")
# ─────────────────────────────────────────────

def _all_level_ids(world: World) -> list[str]:
    out: list[str] = []
    for town in world.towns:
        for lvl in town.levels:
            out.append(lvl.id)
    return out


def _level_index(level_id: str, all_ids: list[str]) -> int:
    try:
        return all_ids.index(level_id)
    except ValueError:
        return -1


def _is_unlocked(level_id: str, all_ids: list[str], completed: dict, world_prefix: str) -> bool:
    idx = _level_index(level_id, all_ids)
    if idx <= 0:
        return True
    prev = all_ids[idx - 1]
    prog = completed.get(f"{world_prefix}:{prev}", {})
    return bool(prog.get("completed"))


def judge_level(lvl: LevelBase, code: str) -> tuple[bool, str, Optional[int]]:
    patterns: list[str] = lvl.checks.required_patterns if lvl.checks else []
    code_norm = code.strip()
    for pat in patterns:
        if not re.search(pat, code_norm, re.MULTILINE):
            failed_idx = patterns.index(pat)
            hint = min(failed_idx, 2) if len(patterns) > 1 else 0
            if not code_norm:
                return False, "Write some code to try!", 0
            return False, lvl.hints[hint], hint
    return True, lvl.success.world_reaction, None


def _level_by_id(world: World, level_id: str) -> LevelBase | None:
    for town in world.towns:
        for lvl in town.levels:
            if lvl.id == level_id:
                return lvl
    return None


def _canonical_skill_for_level(lvl: LevelBase) -> str:
    return lvl.canonical_skill or ""


# ─────────────────────────────────────────────
# Progress / persistence
# ─────────────────────────────────────────────

async def _get_completed(user_id: str) -> dict:
    doc = await gamification_collection.find_one({"user_id": user_id}) or {}
    return doc.get("completed_competencies", {})


async def _get_skill_score(user_id: str, category: str = "coding") -> float:
    doc = await skill_graph_collection.find_one({"user_id": user_id}) or {}
    cat = doc.get("categories", {}).get(category, {})
    return float(cat.get("score", 0) if cat else 0)


async def _ensure_srs_card(user_id: str, problem_id: str, is_correct: bool, difficulty: str = "easy"):
    """Create/update SRS card for a world level."""
    try:
        from app.database import srs_cards_collection
        from app.services.spaced_repetition import SpacedRepetitionEngine, SRSState, ReviewGrade
        from dataclasses import asdict

        col = srs_cards_collection()
        existing = await col.find_one({"user_id": user_id, "problem_id": problem_id})
        engine = SpacedRepetitionEngine()
        if existing:
            state = SRSState(
                concept_id=problem_id,
                user_id=user_id,
                interval=existing.get("interval_days", existing.get("interval", 0)),
                repetitions=existing.get("review_count", existing.get("repetitions", 0)),
                ease_factor=existing.get("ease_factor", 2.5),
            )
            grade = ReviewGrade.GOOD if is_correct else ReviewGrade.AGAIN
            state = engine.review(state, grade)
        else:
            state = engine.create_new_card(problem_id, user_id)

        doc = asdict(state)
        doc["problem_id"] = problem_id
        doc["user_id"] = user_id
        doc["difficulty"] = difficulty
        await col.update_one(
            {"user_id": user_id, "problem_id": problem_id},
            {"$set": doc},
            upsert=True,
        )
    except Exception:
        pass  # SRS is best-effort, never break the level flow


async def _record_skill_touch(user_id: str, canonical_skill: str, passed: bool):
    if not canonical_skill:
        return
    try:
        from app.services.skill_assessment import update_skill_score
        parts = canonical_skill.split(".")
        category = parts[0] if parts else "coding"
        sub = parts[1] if len(parts) > 1 else "general"
        await update_skill_score(user_id, category, sub, 85 if passed else 35, passed)
    except Exception:
        pass


async def _award_xp(user_id: str, world_id: str, xp: int, meta: dict | None = None):
    try:
        from app.services.gamification import record_practice
        await record_practice(user_id, world_id, xp, meta or {})
    except Exception:
        doc = await gamification_collection.find_one({"user_id": user_id}) or {"xp": 0}
        cur_xp = doc.get("xp", 0)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"xp": cur_xp + xp}},
            upsert=True,
        )


# ─────────────────────────────────────────────
# Progress builder (generic over world)
# ─────────────────────────────────────────────

async def _build_progress(world: World, user_id: str) -> dict:
    completed = await _get_completed(user_id)
    world_prefix = world.id
    all_ids = _all_level_ids(world)

    levels = []
    for town in world.towns:
        for lvl in town.levels:
            key = f"{world_prefix}:{lvl.id}"
            prog = completed.get(key, {})
            done = bool(prog.get("completed"))
            levels.append(
                {
                    "id": lvl.id,
                    "title": lvl.title,
                    "icon": lvl.icon,
                    "kind": lvl.kind,
                    "order": lvl.order,
                    "completed": done,
                    "score": prog.get("score", 0),
                    "best_score": prog.get("best_score", 0),
                    "attempts": prog.get("attempts", 0),
                    "failed_attempts": prog.get("failed_attempts", 0),
                    "hints_used": prog.get("hints_used", []),
                    "total_time_seconds": prog.get("total_time_seconds", 0),
                    "mastery_before": prog.get("mastery_before"),
                    "mastery_after": prog.get("mastery_after"),
                    "unlocked": _is_unlocked(lvl.id, all_ids, completed, world_prefix),
                    "xp": lvl.success.xp if isinstance(lvl, LevelBase) else 0,
                }
            )

    pos_idx = 0
    for i, lv in enumerate(levels):
        if not lv["completed"] and lv["unlocked"]:
            pos_idx = i
            break
        if lv["completed"]:
            pos_idx = min(i + 1, len(levels) - 1)

    done_count = sum(1 for lv in levels if lv["completed"])
    total = len(levels)
    boss_done = any(lv.get("kind") == "boss" and lv["completed"] for lv in levels)
    return {
        "levels": levels,
        "character_pos": pos_idx,
        "completed_count": done_count,
        "total_count": total,
        "progress_pct": round(done_count / total * 100) if total else 0,
        "boss_defeated": boss_done,
        "next_town_unlocked": boss_done,
    }


# ─────────────────────────────────────────────
# Routes (generic over world_id)
# ─────────────────────────────────────────────

class AttemptRequest(BaseModel):
    code: str = ""
    time_spent_seconds: int = 0


class HintRequest(BaseModel):
    hint_index: int = 0
    time_spent_seconds: int = 0


@router.get("/{world_id}")
async def get_world_view(world_id: str, user=Depends(get_current_user)):
    """World definition with per-level unlocked/completed overlay."""
    world = get_world(world_id)
    progress = await _build_progress(world, user["id"])
    towns_out = []
    for town in world.towns:
        levels_out = []
        for lvl in town.levels:
            ov = next((x for x in progress["levels"] if x["id"] == lvl.id), {})
            levels_out.append(
                {
                    "id": lvl.id,
                    "title": lvl.title,
                    "icon": lvl.icon,
                    "kind": lvl.kind,
                    "order": lvl.order,
                    "concept": lvl.concept,
                    "mental_model": lvl.mental_model or lvl.concept,
                    "canonical_skill": lvl.canonical_skill,
                    "maps_to_competency": lvl.maps_to_competency,
                    "story": lvl.story.model_dump() if hasattr(lvl.story, "model_dump") else lvl.story.dict(),
                    "tutor": lvl.tutor.model_dump() if hasattr(lvl.tutor, "model_dump") else lvl.tutor.dict(),
                    "discover": lvl.discover.model_dump() if hasattr(lvl.discover, "model_dump") else lvl.discover.dict(),
                    "manipulate": lvl.manipulate.model_dump() if hasattr(lvl.manipulate, "model_dump") else lvl.manipulate.dict(),
                    "predict": lvl.predict.model_dump() if hasattr(lvl, "predict") and lvl.predict else None,
                    "build": lvl.build.model_dump() if hasattr(lvl, "build") and lvl.build else None,
                    "break": lvl.break_step.model_dump() if hasattr(lvl, "break_step") and lvl.break_step else None,
                    "debug": lvl.debug.model_dump() if hasattr(lvl, "debug") and lvl.debug else None,
                    "code": lvl.code.model_dump() if hasattr(lvl.code, "model_dump") else lvl.code.dict(),
                    "checks": lvl.checks.model_dump() if hasattr(lvl.checks, "model_dump") else lvl.checks.dict(),
                    "hints": lvl.hints,
                    "retrieval": lvl.retrieval.model_dump() if hasattr(lvl, "retrieval") and lvl.retrieval else None,
                    "transfer": lvl.transfer.model_dump() if hasattr(lvl, "transfer") and lvl.transfer else None,
                    "mastery_threshold": lvl.mastery_threshold,
                    "estimated_minutes": lvl.estimated_minutes,
                    "success": lvl.success.model_dump() if hasattr(lvl.success, "model_dump") else lvl.success.dict(),
                    "completed": ov.get("completed", False),
                    "unlocked": ov.get("unlocked", False),
                    "score": ov.get("score", 0),
                    "attempts": ov.get("attempts", 0),
                    "xp": ov.get("xp", lvl.success.xp),
                }
            )
        town_payload = town.model_dump() if hasattr(town, "model_dump") else town.dict()
        town_payload["levels"] = levels_out
        towns_out.append(town_payload)

    world_out = world.model_dump() if hasattr(world, "model_dump") else world.dict()
    mastery = await _get_skill_score(user["id"])
    return {
        "world": {**world_out, "towns": towns_out},
        "progress": progress,
        "mastery": {_canonical_skill_for_level(world.towns[0].levels[0]) if world.towns and world.towns[0].levels else "coding.variables": mastery},
    }


@router.get("/{world_id}/progress")
async def get_world_progress(world_id: str, user=Depends(get_current_user)):
    world = get_world(world_id)
    return await _build_progress(world, user["id"])


@router.post("/{world_id}/levels/{level_id}/hint")
async def record_hint(world_id: str, level_id: str, req: HintRequest, user=Depends(get_current_user)):
    world = get_world(world_id)
    lvl = _level_by_id(world, level_id)
    if not lvl:
        raise HTTPException(status_code=404, detail=f"Unknown level: {level_id}")
    key = f"{world_id}:{level_id}"
    doc = await gamification_collection.find_one({"user_id": user["id"]}) or {"user_id": user["id"], "completed_competencies": {}}
    comp = doc.get("completed_competencies", {})
    entry = comp.get(key, {"completed": False, "score": 0, "best_score": 0, "attempts": 0, "failed_attempts": 0, "hints_used": [], "total_time_seconds": 0})
    hints = entry.get("hints_used", [])
    if req.hint_index not in hints:
        hints.append(req.hint_index)
    entry["hints_used"] = sorted(hints)
    entry["total_time_seconds"] = entry.get("total_time_seconds", 0) + int(req.time_spent_seconds or 0)
    comp[key] = entry
    await gamification_collection.update_one(
        {"user_id": user["id"]}, {"$set": {"completed_competencies": comp}}, upsert=True
    )
    return {"hints_used": entry["hints_used"]}


@router.post("/{world_id}/levels/{level_id}/attempt")
async def attempt_level(world_id: str, level_id: str, req: AttemptRequest, user=Depends(get_current_user)):
    world = get_world(world_id)
    lvl = _level_by_id(world, level_id)
    if not lvl:
        raise HTTPException(status_code=404, detail=f"Unknown level: {level_id}")

    completed = await _get_completed(user["id"])
    all_ids = _all_level_ids(world)
    if not _is_unlocked(level_id, all_ids, completed, world_id):
        raise HTTPException(status_code=403, detail="Level locked. Complete previous levels first.")

    mastery_before = await _get_skill_score(user["id"])
    passed, message, hint_idx = judge_level(lvl, req.code)

    key = f"{world_id}:{level_id}"
    doc = await gamification_collection.find_one({"user_id": user["id"]}) or {"user_id": user["id"], "completed_competencies": {}}
    comp = doc.get("completed_competencies", {})
    entry = comp.get(key, {"completed": False, "score": 0, "best_score": 0, "attempts": 0, "failed_attempts": 0, "hints_used": [], "total_time_seconds": 0})
    entry["attempts"] = entry.get("attempts", 0) + 1
    if not passed:
        entry["failed_attempts"] = entry.get("failed_attempts", 0) + 1
    entry["total_time_seconds"] = entry.get("total_time_seconds", 0) + int(req.time_spent_seconds or 0)
    if entry.get("mastery_before") is None:
        entry["mastery_before"] = mastery_before
    entry["last_attempt_code"] = req.code[:2000]
    entry["last_attempt_passed"] = passed
    comp[key] = entry
    await gamification_collection.update_one(
        {"user_id": user["id"]}, {"$set": {"completed_competencies": comp}}, upsert=True
    )

    await _record_skill_touch(user["id"], _canonical_skill_for_level(lvl), passed)

    mastery_after = await _get_skill_score(user["id"])
    entry["mastery_after"] = mastery_after
    comp[key] = entry
    await gamification_collection.update_one(
        {"user_id": user["id"]}, {"$set": {"completed_competencies": comp}}, upsert=True
    )

    if not passed and entry.get("failed_attempts", 0) >= 2:
        difficulty = "hard" if lvl.kind == "boss" else ("medium" if lvl.order >= 4 else "easy")
        await _ensure_srs_card(user["id"], f"{world_id}:{level_id}", is_correct=False, difficulty=difficulty)

    xp_preview = lvl.success.xp if isinstance(lvl, LevelBase) else 0
    if passed:
        return {"passed": True, "message": message, "hint_index": None, "xp_preview": xp_preview, "mastery_before": mastery_before, "mastery_after": mastery_after}
    else:
        return {
            "passed": False,
            "message": message,
            "hint_index": hint_idx,
            "hint": lvl.hints[hint_idx] if hint_idx is not None else lvl.hints[0],
            "mastery_before": mastery_before,
            "mastery_after": mastery_after,
        }


@router.post("/{world_id}/levels/{level_id}/complete")
async def complete_level(world_id: str, level_id: str, req: AttemptRequest, user=Depends(get_current_user)):
    world = get_world(world_id)
    lvl = _level_by_id(world, level_id)
    if not lvl:
        raise HTTPException(status_code=404, detail=f"Unknown level: {level_id}")

    completed = await _get_completed(user["id"])
    all_ids = _all_level_ids(world)
    if not _is_unlocked(level_id, all_ids, completed, world_id):
        raise HTTPException(status_code=403, detail="Level locked.")

    mastery_before = await _get_skill_score(user["id"])
    passed, _, _ = judge_level(lvl, req.code)
    if not passed:
        raise HTTPException(status_code=400, detail="Code does not yet pass. Use /attempt to get hints.")

    uid = user["id"]
    now = datetime.now(timezone.utc)
    doc = await gamification_collection.find_one({"user_id": uid}) or {"user_id": uid, "completed_competencies": {}}
    comp = doc.get("completed_competencies", {})
    key = f"{world_id}:{level_id}"
    entry = comp.get(key, {"completed": False, "score": 0, "best_score": 0, "attempts": 0, "failed_attempts": 0, "hints_used": [], "total_time_seconds": 0})
    entry["completed"] = True
    entry["score"] = 100
    entry["best_score"] = max(entry.get("best_score", 0), 100)
    entry["completed_at"] = now.isoformat()
    if entry.get("mastery_before") is None:
        entry["mastery_before"] = mastery_before
    entry["total_time_seconds"] = entry.get("total_time_seconds", 0) + int(req.time_spent_seconds or 0)
    entry["boss_passed"] = lvl.kind == "boss"
    comp[key] = entry

    xp_gain = lvl.success.xp if isinstance(lvl, LevelBase) else 0
    update: dict = {"completed_competencies": comp, "updated_at": now}
    await _award_xp(uid, world_id, xp_gain, {"level_id": level_id, "world": world_id})
    fresh = await gamification_collection.find_one({"user_id": uid}) or {}
    fresh_comp = fresh.get("completed_competencies", {})
    fresh_comp[key] = entry
    await gamification_collection.update_one(
        {"user_id": uid}, {"$set": {"completed_competencies": fresh_comp, "updated_at": now}}, upsert=True
    )

    await _record_skill_touch(uid, _canonical_skill_for_level(lvl), True)

    mastery_after = await _get_skill_score(uid)
    entry["mastery_after"] = mastery_after
    fresh2 = await gamification_collection.find_one({"user_id": uid}) or {}
    fresh_comp2 = fresh2.get("completed_competencies", {})
    if key in fresh_comp2:
        fresh_comp2[key]["mastery_after"] = mastery_after
        await gamification_collection.update_one({"user_id": uid}, {"$set": {"completed_competencies": fresh_comp2}}, upsert=True)

    difficulty = "hard" if lvl.kind == "boss" else ("medium" if lvl.order >= 4 else "easy")
    await _ensure_srs_card(uid, f"{world_id}:{level_id}", is_correct=True, difficulty=difficulty)

    progress = await _build_progress(world, uid)
    next_id = None
    if lvl.order + 1 <= len(all_ids):
        next_id = all_ids[lvl.order] if lvl.order < len(all_ids) else None

    return {
        "completed": True,
        "level_id": level_id,
        "xp_awarded": xp_gain,
        "world_reaction": lvl.success.world_reaction,
        "world_before": lvl.success.world_before,
        "world_after": lvl.success.world_after,
        "byte_line": lvl.success.byte_line,
        "reward_text": lvl.success.reward_text,
        "next_level_id": next_id,
        "progress": progress,
        "mastery_before": mastery_before,
        "mastery_after": mastery_after,
    }


@router.get("/")
async def list_worlds(user=Depends(get_current_user)):
    """List all worlds with basic metadata and user progress."""
    completed = await _get_completed(user["id"])
    out = []
    for w in WORLD_REGISTRY.values():
        total = sum(len(t.levels) for t in w.towns)
        done = 0
        for t in w.towns:
            for lvl in t.levels:
                key = f"{w.id}:{lvl.id}"
                if completed.get(key, {}).get("completed"):
                    done += 1
        out.append({
            "id": w.id,
            "name": w.name,
            "subtitle": w.subtitle,
            "description": w.description,
            "icon": w.icon,
            "order": w.order,
            "theme": w.theme,
            "recommended_roles": w.recommended_roles,
            "prerequisites": w.prerequisites,
            "towns_count": len(w.towns),
            "levels_count": total,
            "completed_count": done,
            "progress_pct": round(done / total * 100) if total else 0,
            "unlocked": all(
                _is_unlocked(t.levels[0].id, _all_level_ids(w), completed, w.id)
                for t in w.towns if t.levels
            ) if w.prerequisites == [] or any(
                completed.get(f"{w.id}:{lvl.id}", {}).get("completed")
                for t in w.towns for lvl in t.levels
            ) else False,
        })
    return {"worlds": sorted(out, key=lambda x: x["order"])}


@router.get("/{world_id}/towns")
async def list_towns(world_id: str, user=Depends(get_current_user)):
    """List all towns for a world with progress."""
    world = get_world(world_id)
    completed = await _get_completed(user["id"])
    out = []
    for town in world.towns:
        total = len(town.levels)
        done = sum(1 for lvl in town.levels if completed.get(f"{world_id}:{lvl.id}", {}).get("completed"))
        boss = town.levels[-1] if town.levels and town.levels[-1].kind == "boss" else None
        out.append({
            "id": town.id,
            "name": town.name,
            "icon": town.icon,
            "description": town.description,
            "order": town.order,
            "mental_model": town.mental_model,
            "canonical_skills": town.canonical_skills,
            "competencies": town.competencies,
            "levels_count": total,
            "completed_count": done,
            "progress_pct": round(done / total * 100) if total else 0,
            "boss_defeated": bool(boss and completed.get(f"{world_id}:{boss.id}", {}).get("completed")),
        })
    return {"towns": sorted(out, key=lambda x: x["order"])}

