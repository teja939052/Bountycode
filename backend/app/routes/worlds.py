"""Worlds — generic World → Town → Level → Boss learning game layer.

World
  → Town[]
       → Level[] + Boss

Persistence
  completed_competencies["<world_id>:<level_id>"] in gamification collection
  skill_graph via update_skill_score (category derived from canonical_skill)
  Diamonds via record_practice(activity_type=<world_id>)
  SRS via srs_cards_collection (canonical spaced_repetition)

Routes (all under /api/v1/worlds, auth required):
  GET  /{world_id}                  → world definition + user progress overlay
  GET  /{world_id}/progress         → progress only (character pos, unlocked)
  POST /{world_id}/levels/{id}/attempt  → deterministic judge + hint ladder
  POST /{world_id}/levels/{id}/complete → mark done, Diamonds, mastery, unlock
  POST /{world_id}/levels/{id}/hint     → record hint usage (instrumentation)
"""

from __future__ import annotations

import re
import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.data.worlds_data import WORLD_REGISTRY
from app.database import gamification_collection, skill_graph_collection, srs_cards_collection
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


def world_progress(world_id: str, completed: dict) -> dict:
    """Done/total counts for one world from persisted evidence."""
    world = WORLD_REGISTRY.get(world_id)
    if world is None:
        return {"done": 0, "total": 0}
    total = sum(len(t.levels) for t in world.towns)
    done = sum(
        1 for t in world.towns for lvl in t.levels
        if completed.get(f"{world_id}:{lvl.id}", {}).get("completed")
    )
    return {"done": done, "total": total}


def is_world_unlocked(world_id: str, completed: dict) -> bool:
    """Cross-world gate, read from the registry's own prerequisites.

    Single source of truth: the map switcher, the voyage summary, and the
    attempt/hint/complete endpoints below all call this. Unlocked when the
    world has no prerequisites, the student has any progress inside it
    (earned progress is never locked out), or every prerequisite world is
    fully cleared. Viewing (GET) is never gated — only progress writes.
    """
    world = WORLD_REGISTRY.get(world_id)
    if world is None:
        return False
    prereqs = list(getattr(world, "prerequisites", []) or [])
    if not prereqs:
        return True
    if world_progress(world_id, completed)["done"] > 0:
        return True
    for pid in prereqs:
        pre = world_progress(pid, completed)
        if pre["total"] and pre["done"] < pre["total"]:
            return False
    return True


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


# ─────────────────────────────────────────────
# Real judge — grade journeys by execution, not just regex
# ─────────────────────────────────────────────

_SUPPORTED_RUNTIMES = {"python", "java", "cpp", "c"}


def _normalize_answer(s: str) -> str:
    return " ".join(str(s or "").strip().lower().split())


def _looks_like_runnable_code(s: str) -> bool:
    s = (s or "").strip()
    if not s:
        return False
    if "\n" in s:
        return True
    return bool(re.search(r"=|\+|-|\*|/|print\s*\(|def\s+|return\s+|\binput\s*\(", s))


def _text_pass(actual: str, expected: str) -> bool:
    """Tolerant answer comparison for predict/retrieval/break_step.

    Exact-normalized match always passes. Short canonical answers (a number or a
    word) must match in full so '18' can never pass by containment inside
    'the tip is 10'. Longer answers may pass by containment either way.
    """
    a = _normalize_answer(actual)
    e = _normalize_answer(expected)
    if not e or not a:
        return False
    if a == e:
        return True
    if len(e) <= 6:
        return False
    return e in a or a in e


async def _run_student_code(code: str, language: str) -> dict | None:
    """Execute via the canonical judge engine.

    Returns the engine result dict on success, or None when the execution
    backend is unavailable (infra). Callers must fall back to static grading —
    a student must never be failed because Piston is down.
    """
    try:
        from app.services.code_executor import CodeExecutionEngine
        engine = CodeExecutionEngine()
        lang = (language or "python").lower()
        if lang not in _SUPPORTED_RUNTIMES:
            lang = "python"
        result = await engine.execute_code(code or "", lang, "", timeout=5)
        return result if isinstance(result, dict) and "success" in result else None
    except Exception:
        return None


def _failure_error(result: dict) -> str:
    """Best human-readable failure reason from a run result dict."""
    return (result.get("error") or result.get("compile_error") or result.get("stderr") or "").strip()


def _evidence(student: dict | None, reference: dict | None = None, **extra) -> dict | None:
    """Build the run-output evidence block shown to the student.

    Only present when a real execution actually happened. Contains what the
    student's program printed/raised plus the expected ground truth, so a wrong
    answer becomes a lesson instead of just a red message.
    """
    if not student:
        return None
    return {
        "stdout": (student.get("stdout") or "").strip(),
        "stderr": (student.get("stderr") or "").strip(),
        "error": _failure_error(student),
        "expected": (reference.get("stdout") or "").strip() if reference else None,
        **extra,
    }


async def _judge_execution(
    student_code: str, reference_code: str, language: str
) -> tuple[bool, str, dict | None] | None:
    """Run the student's code AND the canonical answer; compare normalized stdout.

    Returns (passed, message, evidence) when the reference actually ran (ground
    truth), or None when the backend is unavailable / the reference is not runnable.
    """
    if not _looks_like_runnable_code(reference_code):
        return None
    student, reference = await asyncio.gather(
        _run_student_code(student_code, language),
        _run_student_code(reference_code, language),
    )
    if student is None or reference is None:
        return None
    # The canonical answer must run clean; if it does not, do not trust execution.
    if not reference.get("success"):
        return None
    expected_out = _normalize_answer(reference.get("stdout"))
    if not student.get("success"):
        err = _failure_error(student)
        return False, f"Your code failed to run{': ' + err if err else '.'}", _evidence(student, reference)
    actual_out = _normalize_answer(student.get("stdout"))
    if actual_out == expected_out:
        return True, "Correct! Your program runs and produces the expected output.", _evidence(student, reference)
    # A canonical answer that prints nothing cannot distinguish implementations —
    # a clean run is sufficient evidence then.
    if not expected_out:
        return True, "Correct! Your program runs cleanly.", _evidence(student, reference)
    return (
        False,
        f"Not yet. Your program printed: «{actual_out or '(nothing)'}». Expected: «{expected_out}».",
        _evidence(student, reference),
    )


async def _judge_code_run(
    student_code: str, language: str, lvl: LevelBase
) -> tuple[bool, str, Optional[int], dict | None] | None:
    """Execution + authored-pattern judge for code/build steps.

    Runs the student's code; only then applies the level's required_patterns so a
    payload that merely matches text but crashes is never accepted.
    Returns None when the backend is unavailable (regex-only fallback upstream).
    """
    run = await _run_student_code(student_code, language)
    if run is None:
        return None
    if not run.get("success"):
        err = _failure_error(run)
        return False, f"Your code failed to run{': ' + err if err else '.'}", 0, _evidence(run)
    passed, message, hint_idx = judge_level(lvl, student_code)
    return passed, message, hint_idx, _evidence(run)


async def _judge_break_step(
    student_code: str, broken_code: str, expected_failure: str, language: str
) -> tuple[bool, str, dict | None]:
    """Grade the student's prediction of what happens when broken code runs.

    Grounds truth in the ACTUAL runtime failure when the engine is available;
    falls back to the authored expected_failure (tolerant text match) otherwise.
    Accepts either source of truth so an authored expectation that disagrees with
    the real interpreter does not penalize the student.
    """
    truth = _normalize_answer(expected_failure)
    truth_hits = bool(truth) and _text_pass(student_code, truth)
    run = await _run_student_code(broken_code, language)
    if run is None:
        if truth_hits:
            return True, "Correct! That is exactly what happens.", None
        return False, f"Not quite. The expected failure is: {truth or 'a runtime error'}. Try again.", None
    if run.get("success"):
        # Broken code ran clean — the failure is conceptual, so use the authored truth.
        if truth_hits:
            return True, "Correct!", _evidence(run)
        return False, f"Not quite. The expected failure is: {truth or 'a runtime error'}. Try again.", _evidence(run)
    err = _failure_error(run)
    types = re.findall(r"\b([A-Z][A-Za-z_]*Error)\b", err)
    failure_type = types[-1] if types else err
    evidence = _evidence(run, expected=truth or None, error_type=failure_type)
    if _text_pass(student_code, failure_type) or truth_hits:
        return True, f"Correct! Running it raises {failure_type}.", evidence
    return False, f"Not quite. Running the code raises: {failure_type[:200]}. Try again.", evidence


def stars_for_entry(entry: Dict[str, Any]) -> int:
    """1-3 stars from persisted evidence (0-100 best score + hints used).

    Single source of truth: the map AND the complete response both read
    this (it lives here, next to the entries it scores — map.py imports it).
    Forward progress needs only 1 star; 3 stars require independence
    (high best with <=1 hint), so repair-then-recover can still earn 3.
    """
    if not entry.get("completed"):
        return 0
    best = float(entry.get("best_score", 0) or 0)
    hints = len(entry.get("hints_used", []) or [])
    if best >= 85 and hints <= 1:
        return 3
    if best >= 60:
        return 2
    return 1


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


async def _award_xp(user_id: str, world_id: str, diamonds: int, meta: dict | None = None, role: str = "sde"):
    """Award Diamonds for a world-level completion via the canonical gamification service.

    LAW: record_practice is the ONLY writer of Diamonds. There is no fallback
    $inc/$set path — a silent fallback is how mastery got polluted, and a
    smaller wrong number is worse than an explicit pending flag.

    Contract: activity_type is the canonical "lesson" (score 0-10: a pass is
    10.0); world/level travel in metadata so per-world counters don't
    fragment into total_foundationss-style junk. (Payout base shifts 70->75
    pre-multiplier vs the old unknown-type fallback; role multipliers now
    apply, which is the correct behavior.)

    On engine failure the caller persists the completion entry with
    rewards_pending=True and returns completed:true + rewards_pending:true
    (entry saved, Diamonds missing but flagged, never silently short). Raises.
    Skill-graph mastery is NOT affected (fixed 85/True via
    ``_record_skill_touch``); map stars are NOT affected (entry best_score).
    Returns the ``record_practice`` result (with ``xp_gained``).
    """
    import logging as _logging

    _log = _logging.getLogger("app.routes.worlds")
    from app.services.gamification import record_practice
    meta = dict(meta or {})
    meta.setdefault("world_id", world_id)
    result = await record_practice(user_id, "lesson", 10.0, meta, role=role)
    stored = (result or {}).get("xp_gained")
    # Evidence trail: nominal request vs canonical award. Stored is
    # routinely larger by design (streak / first-of-day / combo / crit).
    _log.debug(
        "xp_award user=%s world=%s level=%s nominal=%s stored=%s",
        user_id, world_id, meta.get("level_id"), diamonds, stored,
    )
    if stored is not None and int(stored) < int(diamonds):
        _log.warning(
            "xp_underpay user=%s world=%s level=%s nominal=%s stored=%s",
            user_id, world_id, meta.get("level_id"), diamonds, stored,
        )
    return result


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
                    "diamonds": lvl.success.diamonds if isinstance(lvl, LevelBase) else 0,
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
    language: str = "python"
    time_spent_seconds: int = 0
    step_type: str = "code"


class HintRequest(BaseModel):
    hint_index: int = 0
    time_spent_seconds: int = 0


@router.get("/{world_id}")
async def get_world_view(world_id: str, user=Depends(get_current_user)):
    """World definition with per-level unlocked/completed overlay.

    Levels are ordered by relevance to the student's target_role and
    target_company when those are set on the user profile. Canonical
    order is preserved within each relevance bucket.
    """
    world = get_world(world_id)
    progress = await _build_progress(world, user["id"])
    target_role = (user.get("target_role") or user.get("role") or "").strip().lower()
    target_company = (user.get("target_company") or "").strip().lower()

    def _relevance(lvl):
        role_match = bool(target_role and getattr(lvl, "role_relevance", None) and target_role in (lvl.role_relevance or "").lower())
        company_match = bool(target_company and getattr(lvl, "company_relevance", None) and target_company in (lvl.company_relevance or "").lower())
        if role_match and company_match:
            return 0
        if role_match:
            return 1
        if company_match:
            return 2
        return 3

    towns_out = []
    for town in world.towns:
        sorted_levels = sorted(town.levels, key=lambda l: (_relevance(l), l.order))
        levels_out = []
        for lvl in sorted_levels:
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
                    "role_relevance": getattr(lvl, "role_relevance", None),
                    "company_relevance": getattr(lvl, "company_relevance", None),
                    "story": lvl.story.model_dump() if hasattr(lvl.story, "model_dump") else lvl.story.dict(),
                    "tutor": lvl.tutor.model_dump() if hasattr(lvl.tutor, "model_dump") else lvl.tutor.dict(),
                    "discover": lvl.discover.model_dump() if hasattr(lvl.discover, "model_dump") else lvl.discover.dict(),
                    "manipulate": lvl.manipulate.model_dump() if hasattr(lvl.manipulate, "model_dump") else lvl.manipulate.dict(),
                    "predict": lvl.predict.model_dump() if hasattr(lvl, "predict") and lvl.predict else None,
                    "build": lvl.build.model_dump() if hasattr(lvl, "build") and lvl.build else None,
                    "break_step": lvl.break_step.model_dump() if hasattr(lvl, "break_step") and lvl.break_step else None,
                    "debug": lvl.debug.model_dump() if hasattr(lvl, "debug") and lvl.debug else None,
                    "code": lvl.code.model_dump() if hasattr(lvl.code, "model_dump") else lvl.code.dict(),
                    "checks": lvl.checks.model_dump() if hasattr(lvl.checks, "model_dump") else lvl.checks.dict(),
                    "hints": lvl.hints,
                    "retrieval": lvl.retrieval.model_dump() if hasattr(lvl, "retrieval") and lvl.retrieval else None,
                    "transfer": lvl.transfer.model_dump() if hasattr(lvl, "transfer") and lvl.transfer else None,
                    "mastery": getattr(lvl, "mastery", None),
                    "mastery_evidence": getattr(lvl, "mastery_evidence", []),
                    "mastery_threshold": lvl.mastery_threshold,
                    "estimated_minutes": lvl.estimated_minutes,
                    "success": lvl.success.model_dump() if hasattr(lvl.success, "model_dump") else lvl.success.dict(),
                    "completed": ov.get("completed", False),
                    "unlocked": ov.get("unlocked", False),
                    "score": ov.get("score", 0),
                    "attempts": ov.get("attempts", 0),
                    "diamonds": ov.get("diamonds", lvl.success.diamonds),
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
        "content_routing": {
            "target_role": target_role or None,
            "target_company": target_company or None,
            "sort_key": "role_relevance, company_relevance, order",
        },
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
    if not is_world_unlocked(world_id, await _get_completed(user["id"])):
        raise HTTPException(status_code=403, detail="World locked. Clear the previous world first.")
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
    if not is_world_unlocked(world_id, completed):
        raise HTTPException(status_code=403, detail="World locked. Clear the previous world first.")
    if not _is_unlocked(level_id, all_ids, completed, world_id):
        raise HTTPException(status_code=403, detail="Level locked. Complete previous levels first.")

    mastery_before = await _get_skill_score(user["id"])
    step_type = (getattr(req, "step_type", "code") or "code").strip().lower()
    language = (req.language or "python").strip().lower()
    if language not in _SUPPORTED_RUNTIMES:
        language = "python"

    passed = False
    message = ""
    hint_idx: Optional[int] = None
    evidence: dict | None = None

    if step_type == "predict":
        if (hasattr(lvl, "predict") and lvl.predict and (lvl.predict.answer or "").strip()):
            # Real input, real canonical grading — tolerant comparator so a
            # student who nails the failure type is not punished for phrasing.
            passed = _text_pass(req.code, lvl.predict.answer)
            message = lvl.predict.explanation or ("Correct!" if passed else f"Not quite. Expected: {lvl.predict.answer}")
        else:
            logger.warning("content_fallback world=%s level=%s step_type=predict reason=missing_content", world_id, level_id)
            passed, message, hint_idx = judge_level(lvl, req.code)
    elif step_type == "manipulate":
        if (hasattr(lvl, "manipulate") and lvl.manipulate and (lvl.manipulate.answer or "").strip()):
            passed = _text_pass(req.code, lvl.manipulate.answer)
            message = lvl.manipulate.hint or ("Correct!" if passed else f"Not quite. Expected: {lvl.manipulate.answer}")
            hint_idx = None
        else:
            logger.warning("content_fallback world=%s level=%s step_type=manipulate reason=missing_content", world_id, level_id)
            passed, message, hint_idx = judge_level(lvl, req.code)
    elif step_type == "retrieval":
        if (hasattr(lvl, "retrieval") and lvl.retrieval and (lvl.retrieval.answer or "").strip()):
            passed = _text_pass(req.code, lvl.retrieval.answer)
            message = lvl.retrieval.explanation or ("Correct!" if passed else f"Not quite. Expected: {lvl.retrieval.answer}")
            hint_idx = None
            if passed:
                await _ensure_srs_card(user["id"], f"{world_id}:{level_id}:retrieval", is_correct=True, difficulty="easy")
            else:
                await _ensure_srs_card(user["id"], f"{world_id}:{level_id}:retrieval", is_correct=False, difficulty="medium")
        else:
            logger.warning("content_fallback world=%s level=%s step_type=retrieval reason=missing_content", world_id, level_id)
            passed, message, hint_idx = judge_level(lvl, req.code)
    elif step_type == "transfer":
        if (hasattr(lvl, "transfer") and lvl.transfer and (lvl.transfer.answer or "").strip()):
            verdict = await _judge_execution(req.code, lvl.transfer.answer, language)
            if verdict is not None:
                passed, message, evidence = verdict
            elif _text_pass(req.code, lvl.transfer.answer):
                passed, message = True, "Correct!"
            else:
                passed, message, hint_idx = judge_level(lvl, req.code)
        else:
            logger.warning("content_fallback world=%s level=%s step_type=transfer reason=missing_content", world_id, level_id)
            passed, message, hint_idx = judge_level(lvl, req.code)
    elif step_type == "break_step":
        if (hasattr(lvl, "break_step") and lvl.break_step):
            passed, message, evidence = await _judge_break_step(req.code, lvl.break_step.broken_code, lvl.break_step.expected_failure, language)
        else:
            logger.warning("content_fallback world=%s level=%s step_type=break_step reason=missing_content", world_id, level_id)
            passed, message, hint_idx = judge_level(lvl, req.code)
    elif step_type == "debug":
        if (hasattr(lvl, "debug") and lvl.debug and (lvl.debug.answer or "").strip()):
            verdict = await _judge_execution(req.code, lvl.debug.answer, language)
            if verdict is not None:
                passed, message, evidence = verdict
            else:
                passed, message, hint_idx = judge_level(lvl, req.code)
        else:
            logger.warning("content_fallback world=%s level=%s step_type=debug reason=missing_content", world_id, level_id)
            passed, message, hint_idx = judge_level(lvl, req.code)
    else:
        # code / build — run the code for real, then apply authored patterns.
        verdict = await _judge_code_run(req.code, language, lvl)
        if verdict is not None:
            passed, message, hint_idx, evidence = verdict
        elif step_type in ("predict", "retrieval"):
            logger.warning(
                "content_fallback world=%s level=%s step_type=%s reason=missing_content",
                world_id, level_id, step_type,
            )
            passed, message, hint_idx = judge_level(lvl, req.code)
        else:
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

    xp_preview = lvl.success.diamonds if isinstance(lvl, LevelBase) else 0
    run_output = evidence or None
    if passed:
        return {"passed": True, "message": message, "hint_index": None, "xp_preview": xp_preview, "mastery_before": mastery_before, "mastery_after": mastery_after, "run_output": run_output}
    else:
        return {
            "passed": False,
            "message": message,
            "hint_index": hint_idx,
            "hint": lvl.hints[hint_idx] if hint_idx is not None else lvl.hints[0],
            "mastery_before": mastery_before,
            "mastery_after": mastery_after,
            "run_output": run_output,
        }


@router.post("/{world_id}/levels/{level_id}/complete")
async def complete_level(world_id: str, level_id: str, req: AttemptRequest, user=Depends(get_current_user)):
    world = get_world(world_id)
    lvl = _level_by_id(world, level_id)
    if not lvl:
        raise HTTPException(status_code=404, detail=f"Unknown level: {level_id}")

    completed = await _get_completed(user["id"])
    all_ids = _all_level_ids(world)
    if not is_world_unlocked(world_id, completed):
        raise HTTPException(status_code=403, detail="World locked. Clear the previous world first.")
    if not _is_unlocked(level_id, all_ids, completed, world_id):
        raise HTTPException(status_code=403, detail="Level locked.")

    mastery_before = await _get_skill_score(user["id"])
    passed, _, _ = judge_level(lvl, req.code)
    if not passed:
        raise HTTPException(status_code=400, detail="Code does not yet pass. Use /attempt to get hints.")

    uid = user["id"]
    now = datetime.now(timezone.utc)
    key = f"{world_id}:{level_id}"
    # Idempotency, including CONCURRENT double-tap: the claim below is a
    # single atomic op. Of two requests landing at the same instant, exactly
    # one matches the "not completed" filter and proceeds to award Diamonds; the
    # loser sees no match and returns deduplicated. A plain read-then-write
    # check cannot guarantee this. Ship position derives from completed
    # flags, so the character can never advance twice from one completion.
    await gamification_collection.update_one(
        {"user_id": uid},
        {"$setOnInsert": {"user_id": uid, "completed_competencies": {}}},
        upsert=True,
    )
    claimed = await gamification_collection.find_one_and_update(
        {"user_id": uid, f"completed_competencies.{key}.completed": {"$ne": True}},
        {"$set": {
            f"completed_competencies.{key}.completed": True,
            f"completed_competencies.{key}.claimed_at": now.isoformat(),
            "updated_at": now,
        }},
    )
    if claimed is None:
        progress = await _build_progress(world, uid)
        return {
            "completed": True,
            "deduplicated": True,
            "level_id": level_id,
            "xp_awarded": 0,
            "progress": progress,
        }
    doc = await gamification_collection.find_one({"user_id": uid}) or {"user_id": uid, "completed_competencies": {}}
    comp = doc.get("completed_competencies", {})
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

    xp_gain = lvl.success.diamonds if isinstance(lvl, LevelBase) else 0
    update: dict = {"completed_competencies": comp, "updated_at": now}
    # Persist the completion entry BEFORE awarding: if the reward engine
    # fails, the entry (and a rewards_pending flag) still lands — a failed
    # award must never lose the completion, and must never silently short it.
    # Report the ACTUAL canonical award, not the nominal level reward:
    # response.xp_awarded == stored $inc delta == profile delta.
    fresh = await gamification_collection.find_one({"user_id": uid}) or {}
    fresh_comp = fresh.get("completed_competencies", {})
    fresh_comp[key] = entry
    await gamification_collection.update_one(
        {"user_id": uid}, {"$set": {"completed_competencies": fresh_comp, "updated_at": now}}, upsert=True
    )
    rewards_pending = False
    reward_breakdown: dict = {}
    try:
        xp_result = await _award_xp(uid, world_id, xp_gain, {"level_id": level_id, "world": world_id}, role=user.get("role") or user.get("target_role") or "sde")
        xp_awarded = (xp_result or {}).get("xp_gained", xp_gain)
        # Forward the engine's own breakdown so the result banner renders
        # real numbers (no second fetch, no client math).
        reward_breakdown = {
            "combo": ((xp_result or {}).get("combo") or {}).get("current", 0),
            "streak_multiplier": (xp_result or {}).get("streak_multiplier", 1.0),
            "critical_hit": bool((xp_result or {}).get("critical_hit", False)),
            "new_streak": (xp_result or {}).get("new_streak", 0),
        }
    except Exception as exc:
        import logging as _logging2
        _logging2.getLogger("app.routes.worlds").warning(
            "xp_award_failed user=%s world=%s level=%s err=%s", uid, world_id, level_id, exc)
        xp_awarded = 0
        rewards_pending = True
        entry["rewards_pending"] = True
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
        "xp_awarded": xp_awarded,
        "xp_nominal": xp_gain,
        "rewards_pending": rewards_pending,
        "reward": reward_breakdown,
        "stars": stars_for_entry(entry),
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

