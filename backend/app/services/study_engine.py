"""Study Engine — the single orchestrator that decides what a student does next.

Canonical architecture (per AGENTS.md strategy doc):

    Curriculum decides WHAT is learned.
    Study Engine decides WHAT HAPPENS NEXT.
    Mastery decides WHETHER it was learned.
    Gamification REWARDS the outcome.
    Readiness reports career preparedness.

This module owns the ``TODAY`` loop:

    NEXT (curriculum mission)
        +
    REVIEW (SRS cards due)
        +
    PRACTICE (weak-skill reinforcement)
        +
    CHALLENGE (higher-difficulty activity)

Every other subsystem (adaptive_learning, spaced_repetition, mastery_engine,
gamification, worlds) remains intact; this engine *composes* them rather
than duplicating their logic.  The existing
``GET /api/v1/adaptive/daily-plan`` endpoint is now a thin alias over
``get_today`` so the frontend has one canonical entry point.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import asdict

# World data: we use the worlds.py registry (World models with towns/levels)
# rather than capability_curriculum (competencies/steps) because worlds.py
# is where progress tracking (completed_competencies) and the playable level
# graph live.  capability_curriculum is the *content* source; worlds.py is
# the *presentation + progress* source.
# NOTE: the import is deferred into _get_next_mission to avoid a circular
# import at module load (worlds.py imports gamification/skill_assessment).
from app.services.adaptive_learning import (
    assess_user_skills,
    detect_weak_areas,
)
from app.services.gamification import (
    record_practice,
    get_gamification_profile,
)
from app.services.spaced_repetition import get_due_cards, SRSState, ReviewGrade

logger = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─── Today's date key (UTC) ──────────────────────────────────────────

def _today_key() -> str:
    return _now().strftime("%Y-%m-%d")


# ─── 1. NEXT — the next curriculum mission (world/level) ────────────

async def _get_next_mission(user_id: str) -> Optional[Dict[str, Any]]:
    """Resolve the next un-completed level in the currently-active world.

    Priority:
      1. An in-progress world with an unlocked-but-incomplete level.
      2. The first level of World 1 if nothing is started.

    Returns ``None`` when all worlds are complete.
    """
    from app.database import gamification_collection
    from app.content.world_registry import ALL_WORLDS, get_world

    doc = await gamification_collection.find_one({"user_id": user_id}) or {}
    completed = doc.get("completed_competencies", {})

    # Prefer the world the student is farthest into.
    active_world_id = None
    for world in sorted(ALL_WORLDS.values(), key=lambda w: w.order):
        wprefix = world.id + ":"
        if any(k.startswith(wprefix) for k in completed):
            active_world_id = world.id

    if not active_world_id:
        first = sorted(ALL_WORLDS.values(), key=lambda w: w.order)[0]
        active_world_id = first.id

    world = get_world(active_world_id)

    all_ids: List[str] = []
    for town in world.towns:
        for lvl in town.levels:
            all_ids.append(lvl.id)

    # Walk levels in order; return the first unlocked + incomplete one.
    seen_complete = True
    for town in world.towns:
        for lvl in town.levels:
            key = f"{world.id}:{lvl.id}"
            entry = completed.get(key, {})
            done = bool(entry.get("completed"))
            if done:
                continue
            if not seen_complete:
                continue
            return _serialize_level_for_frontend(world, town, lvl, entry)
        seen_complete = all(
            completed.get(f"{world.id}:{lvl.id}", {}).get("completed")
            for lvl in town.levels
        )

    return None


# ─── Lesson content lookup ──────────────────────────────────────────
# The Study Engine resolves *which* level is next from WORLD_REGISTRY, but
# the *content* of that level (steps, story, tutor) lives in the content
# module.  This helper bridges the two.

_LESSON_CONTENT_CACHE: Dict[str, Any] = {}


def _get_lesson_content(level_id: str) -> Optional[Dict[str, Any]]:
    """Return the LessonDefinition content for a level id, or None."""
    if level_id in _LESSON_CONTENT_CACHE:
        return _LESSON_CONTENT_CACHE[level_id]
    try:
        from app.content.world_registry import get_lesson_by_id
        lesson = get_lesson_by_id(level_id)
        if lesson:
            _LESSON_CONTENT_CACHE[level_id] = lesson.model_dump()
            return _LESSON_CONTENT_CACHE[level_id]
    except Exception:
        pass
    return None


def _serialize_level_for_frontend(
    world: Any,
    town: Any,
    lvl: Any,
    entry: Dict[str, Any],
) -> Dict[str, Any]:
    """Shape a curriculum level into a NEXT-mission payload."""
    return {
        "type": "next_mission",
        "world": {
            "id": world.id,
            "title": world.title,
            "icon": world.icon,
        },
        "town": {
            "id": town.id,
            "title": town.title,
            "icon": getattr(town, "icon", "🏠"),
        },
        "level": {
            "id": lvl.id,
            "title": lvl.title,
            "kind": lvl.kind,
            "icon": getattr(lvl, "icon", "📄"),
            "order": lvl.order,
            "concept": getattr(lvl, "concept", ""),
            "canonical_skill": getattr(lvl, "canonical_skill", ""),
            "maps_to_competency": getattr(lvl, "maps_to_competency", ""),
        },
        "attempt": {
            "completed": bool(entry.get("completed")),
            "score": entry.get("score", 0),
            "attempts": entry.get("attempts", 0),
            "best_score": entry.get("best_score", 0),
        },
        "estimated_minutes": getattr(lvl, "estimated_minutes", 12),
        "xp_reward": getattr(lvl, "xp", 50),
        "lesson_content": _get_lesson_content(lvl.id),
    }


# ─── 2. REVIEW — SRS cards due now ──────────────────────────────────

async def _get_due_reviews(user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Pull due spaced-repetition cards and serialise them.

    Tolerates the SRS collection being empty/absent (returns ``[]``).
    """
    from app.database import srs_cards_collection
    from app.services.spaced_repetition import serialize_state

    col = srs_cards_collection()
    cursor = col.find({"user_id": user_id})
    raw_cards: List[SRSState] = []
    try:
        async for doc in cursor:
            try:
                raw_cards.append(SRSState(**doc))
            except Exception:
                continue
    except Exception as exc:
        logger.warning("SRS fetch failed for %s: %s", user_id, exc)
        return []

    if not raw_cards:
        return []

    due = get_due_cards(raw_cards, limit=limit)
    out: List[Dict[str, Any]] = []
    for card in due:
        payload = serialize_state(card)
        payload["skill_id"] = card.concept_id
        out.append(payload)
    return out


# ─── 3. PRACTICE — weak-skill reinforcement ──────────────────────────

async def _get_practice_tasks(
    user_id: str,
    assessment: Dict[str, Any],
    weak_areas: List[Dict[str, Any]],
    limit: int = 3,
) -> List[Dict[str, Any]]:
    """Pick 1–3 weak-skill practice tasks from the question bank.

    Uses ``adaptive_learning.detect_weak_areas`` for priority ordering and
    pulls a few random accepted questions per weak domain from
    ``curated_questions`` so the practice is *relevant*, not random.
    """
    from app.database import curated_questions_collection

    tasks: List[Dict[str, Any]] = []
    for area in weak_areas[:limit]:
        domain_id = area["domain_id"]
        # Map the adaptive-learning domain id back to a skill concept that
        # the question bank tags with.  Many tags already match (e.g.
        # "arrays_hashing", "sql"), but guard with a fallback.
        topics: List[str] = []
        for tag in (domain_id, area.get("skill", "")):
            if tag:
                topics.append(tag)

        col = curated_questions_collection()
        query: Dict[str, Any] = {}
        if topics:
            query["topic"] = {"$in": topics}

        pool: List[Dict[str, Any]] = []
        try:
            async for q in col.find(query).limit(50):
                pool.append(q)
        except Exception as exc:
            logger.warning("question-bank fetch failed for %s: %s", domain_id, exc)
            pool = []

        if not pool:
            # Fallback: just surface the weak-area metadata so the student
            # always gets something actionable.
            tasks.append({
                "type": "practice",
                "kind": "weak_area",
                "domain_id": domain_id,
                "title": area.get("name", domain_id),
                "emoji": area.get("emoji", "📌"),
                "skill": domain_id,
                "reason": area.get("reason"),
                "mastery": area.get("mastery"),
                "mastery_label": area.get("mastery_label"),
                "score": area.get("score", 0),
                "estimated_minutes": 8,
                "xp_reward": 15,
            })
            continue

        import random as _random
        pick = _random.sample(pool, min(1, len(pool)))[0]
        tasks.append({
            "type": "practice",
            "kind": "question",
            "domain_id": domain_id,
            "question_id": pick.get("id") or pick.get("_id"),
            "title": pick.get("title") or pick.get("question", ""),
            "difficulty": pick.get("difficulty", "medium"),
            "skill": domain_id,
            "reason": area.get("reason"),
            "estimated_minutes": pick.get("estimated_minutes", 10),
            "xp_reward": 25,
        })

    return tasks


# ─── 4. CHALLENGE — optional higher-difficulty activity ─────────────

async def _get_optional_challenge(
    user_id: str,
    assessment: Dict[str, Any],
    weak_areas: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Propose a single timed/challenge activity if the student is ready.

    Only surfaced when the student already has 3+ non-zero mastery domains,
    so it never blocks a new learner.  Returns ``None`` when not applicable.
    """
    mastered = [d for d, s in assessment["skills"].items() if s["mastery"] in ("competent", "proficient", "master")]
    if len(mastered) < 3:
        return None

    import random as _random
    pick = _random.choice(mastered)
    return {
        "type": "challenge",
        "kind": "timed_debug",
        "title": "Debugging Sprint",
        "description": f"3 timed bugs in {pick} — can you fix them under pressure?",
        "estimated_minutes": 12,
        "xp_reward": 60,
        "skill": pick,
    }


# ─── Orchestrator ────────────────────────────────────────────────────

async def get_today(user_id: str, force_refresh: bool = False) -> Dict[str, Any]:
    """Return the canonical daily learning plan for *user_id*.

    Shape::

        {
          "date": "2026-08-28",
          "user_id": "...",
          "streak": 7,
          "level": 5,
          "overall_score": 72.0,
          "overall_mastery": "practicing",
          "next": {...mission...},
          "reviews": [...srs cards...],
          "practice": [...weak-skill tasks...],
          "challenge": {...optional...},
          "totals": {"estimated_minutes": 37, "task_count": 5}
        }
    """
    today = _today_key()

    # Light cache: one canonical plan per user per UTC day.
    try:
        from app.services.cache import cache
        if not force_refresh:
            cached = await cache.get("study", f"today:{user_id}:{today}")
            if cached:
                import json as _json
                return _json.loads(cached)
    except Exception:
        pass  # cache is best-effort

    # ── Inputs from the canonical subsystems ──
    assessment = await assess_user_skills(user_id)
    weak_areas = await detect_weak_areas(user_id)

    next_mission = await _get_next_mission(user_id)
    reviews = await _get_due_reviews(user_id)
    practice = await _get_practice_tasks(user_id, assessment, weak_areas)
    challenge = await _get_optional_challenge(user_id, assessment, weak_areas)

    # Gamification context for the header tile.
    try:
        g = await get_gamification_profile(user_id)
        streak = g.get("streak", 0)
        level = g.get("level", 1)
    except Exception:
        streak = 0
        level = 1

    plan: Dict[str, Any] = {
        "date": today,
        "user_id": user_id,
        "streak": streak,
        "level": level,
        "overall_score": assessment.get("overall_score", 0.0),
        "overall_mastery": assessment.get("overall_mastery", "untouched"),
        "overall_mastery_label": assessment.get("overall_mastery_label", "Not Started"),
        "next": next_mission,
        "reviews": reviews,
        "practice": practice,
        "challenge": challenge,
    }

    est = 0
    task_count = 0
    if next_mission:
        est += next_mission.get("estimated_minutes", 12); task_count += 1
    est += sum(r.get("estimated_minutes", 5) for r in reviews); task_count += len(reviews)
    est += sum(t.get("estimated_minutes", 10) for t in practice); task_count += len(practice)
    if challenge:
        est += challenge.get("estimated_minutes", 12); task_count += 1

    plan["totals"] = {"estimated_minutes": est, "task_count": task_count}

    # Cache for the day (plan is deterministic unless a skill/level changes).
    try:
        from app.services.cache import cache
        import json as _json
        await cache.set("study", f"today:{user_id}:{today}", _json.dumps(plan), ttl=3600)
    except Exception:
        pass

    return plan


# ─── Activity recording — the single completion event ────────────────

async def record_activity(
    user_id: str,
    activity: Dict[str, Any],
) -> Dict[str, Any]:
    """Record one LearningEvent and fan-out to mastery / SRS / XP.

    This is the *canonical* completion sink.  Existing routes that call
    ``record_practice`` / ``update_skill_score`` directly are left in place
    for backward compatibility, but new activity should prefer this entry
    point so the event is observable in one place.

    ``activity`` keys:

        type            : "learn" | "review" | "practice" | "challenge"
        skill_id        : canonical skill (e.g. "coding.variables")
        competency_id   : optional curriculum competency
        passed          : bool
        score           : 0-100 (optional)
        attempts        : int
        time_spent      : seconds
    """
    result: Dict[str, Any] = {"recorded": False}

    activity_type = activity.get("type", "practice")
    skill_id = activity.get("skill_id", "")
    passed = bool(activity.get("passed", False))
    score = float(activity.get("score", 100.0 if passed else 0.0))
    time_spent = int(activity.get("time_spent", 0))

    # ── Mastery update ──
    mastery_before = None
    if skill_id:
        try:
            from app.services.skill_assessment import update_skill_score
            parts = skill_id.split(".")
            category = parts[0] if parts else "coding"
            sub = parts[1] if len(parts) > 1 else "general"
            mastery_before = await _fetch_skill_score(user_id, category)
            await update_skill_score(user_id, category, sub, score, passed)
        except Exception as exc:
            logger.warning("mastery update failed for %s: %s", user_id, exc)

    # ── SRS card update ──
    try:
        from app.services.spaced_repetition import SpacedRepetitionEngine, SRSState
        from app.database import srs_cards_collection

        if skill_id or activity.get("competency_id"):
            prob_id = skill_id or activity.get("competency_id")
            col = srs_cards_collection()
            existing = await col.find_one({"user_id": user_id, "problem_id": prob_id})
            if existing:
                state = SRSState(**existing)
                grade = ReviewGrade.GOOD if passed else ReviewGrade.AGAIN
                engine = SpacedRepetitionEngine()
                state = engine.review(state, grade)
                await col.update_one(
                    {"user_id": user_id, "problem_id": prob_id},
                    {"$set": asdict(state)},
                    upsert=True,
                )
    except Exception as exc:
        logger.warning("SRS update skipped for %s: %s", user_id, exc)

    # ── Gamification / XP ──
    xp = _xp_for_activity(activity_type, score, passed)
    try:
        await record_practice(
            user_id,
            activity=activity_type,
            score=score,
            metadata={"skill_id": skill_id, "time_spent": time_spent, "passed": passed},
        )
        result["xp_awarded"] = xp
        result["xp_applied"] = True
    except Exception as exc:
        logger.warning("gamification record failed for %s: %s", user_id, exc)
        result["xp_applied"] = False

    result.update({
        "recorded": True,
        "activity_type": activity_type,
        "skill_id": skill_id,
        "passed": passed,
        "score": score,
        "xp": xp,
        "mastery_before": mastery_before,
    })
    return result


async def _fetch_skill_score(user_id: str, category: str) -> Optional[float]:
    """Best-effort fetch of a domain score *before* the update lands."""
    from app.database import skill_graph_collection
    try:
        doc = await skill_graph_collection().find_one({"user_id": user_id})
        if not doc:
            return None
        cat = doc.get("categories", {}).get(category, {})
        return cat.get("score")
    except Exception:
        return None


def _xp_for_activity(activity_type: str, score: float, passed: bool) -> int:
    """Map a completed activity to XP.  Mirrors gamification._calculate_xp
    shape so the two stay in sync without importing the private helper."""
    base = {
        "learn": 30,
        "review": 10,
        "practice": 25,
        "challenge": 60,
    }.get(activity_type, 20)
    if passed:
        bonus = 40 if score >= 10 else (20 if score >= 8 else 0)
    else:
        bonus = -10
    return max(0, base + bonus)
