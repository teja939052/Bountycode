"""Study Engine â€” the single orchestrator that decides what a student does next.

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
from app.services.skill_taxonomy import canonical_skill_id
from app.models.learning_event import (
    LearningEventIn, CONCEPT_GAP, PATTERN_RECOGNITION,
    IMPLEMENTATION_ERROR, EDGE_CASE_FAILURE, COMPLEXITY_ERROR,
    TIME_MANAGEMENT, CARELESS_ERROR, KNOWLEDGE_RECALL,
    TRANSFER_FAILURE, DEBUGGING, COMMUNICATION_DEPTH,
    TRADEOFF_REASONING, REQUIREMENT_MISREAD,
)

logger = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(timezone.utc)


# â”€â”€â”€ Today's date key (UTC) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _today_key() -> str:
    return _now().strftime("%Y-%m-%d")


# â”€â”€â”€ 1. NEXT â€” the next curriculum mission (world/level) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def _get_next_mission(user_id: str) -> Optional[Dict[str, Any]]:
    """Resolve the next un-completed level in the currently-active world.

    Priority:
      1. An in-progress world with an unlocked-but-incomplete level.
      2. The first level of World 1 if nothing is started.

    Returns ``None`` when all worlds are complete.
    """
    from app.database import gamification_collection
    from app.data.worlds_data import WORLD_REGISTRY

    doc = await gamification_collection.find_one({"user_id": user_id}) or {}
    completed = doc.get("completed_competencies", {})

    # Prefer the world the student is farthest into.
    active_world_id = None
    for world in sorted(WORLD_REGISTRY.values(), key=lambda w: w.order):
        wprefix = world.id + ":"
        if any(k.startswith(wprefix) for k in completed):
            active_world_id = world.id

    if not active_world_id:
        first = sorted(WORLD_REGISTRY.values(), key=lambda w: w.order)[0]
        active_world_id = first.id

    world = WORLD_REGISTRY.get(active_world_id)

    all_ids: List[str] = []
    for town in world.towns:
        for lvl in town.lessons:
            all_ids.append(lvl.id)

    # Walk levels in order; return the first unlocked + incomplete one.
    seen_complete = True
    for town in world.towns:
        for lvl in town.lessons:
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
            for lvl in town.lessons
        )

    return None


# â”€â”€â”€ Lesson content lookup â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# The Study Engine resolves *which* level is next from WORLD_REGISTRY, but
# the *content* of that level (steps, story, tutor) lives in the content
# module.  This helper bridges the two.

_LESSON_CONTENT_CACHE: Dict[str, Any] = {}


def _get_lesson_content(level_id: str) -> Optional[Dict[str, Any]]:
    """Return the LessonDefinition content for a level id, or None."""
    if level_id in _LESSON_CONTENT_CACHE:
        return _LESSON_CONTENT_CACHE[level_id]
    try:
        from app.data.worlds_data import WORLD_REGISTRY
        for world in WORLD_REGISTRY.values():
            for town in world.towns:
                for lvl in town.levels:
                    if lvl.id == level_id:
                        _LESSON_CONTENT_CACHE[level_id] = lvl.model_dump()
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
            "title": world.name,
            "icon": world.icon,
        },
        "town": {
            "id": town.id,
            "title": town.name,
            "icon": getattr(town, "icon", "ðŸ "),
        },
        "level": {
            "id": lvl.id,
            "title": lvl.title,
            "kind": lvl.kind,
            "icon": getattr(lvl, "icon", "ðŸ“„"),
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
        "xp_reward": getattr(lvl, "diamonds", 50),
        "lesson_content": _get_lesson_content(lvl.id),
    }


# â”€â”€â”€ 2. REVIEW â€” SRS cards due now â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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


# â”€â”€â”€ 3. PRACTICE â€” weak-skill reinforcement â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def _get_practice_tasks(
    user_id: str,
    assessment: Dict[str, Any],
    weak_areas: List[Dict[str, Any]],
    limit: int = 3,
) -> List[Dict[str, Any]]:
    """Pick 1–3 weak-skill practice tasks from the question bank.

    Uses ``adaptive_learning.detect_weak_areas`` for priority ordering and
    pulls a few random accepted questions per weak domain from the in-memory
    canonical store so the practice is *relevant*, not random.

    When a company track is enrolled, practice tasks are filtered to
    company-relevant topics (company requirement × student weakness ×
    prerequisite × evidence freshness × assessment relevance).
    """
    # In-memory canonical store only (Residency Rule): never MongoDB.
    from app.services import question_store

    # ── Read user goal for company-aware filtering ──
    company_relevant_topics: List[str] = []
    try:
        from app.database import users_collection
        user_doc = await users_collection().find_one({"user_id": user_id}) or {}
        company_track = user_doc.get("company_track", "")
        if company_track:
            from app.data.learning_paths import COMPANY_TRACKS
            track = COMPANY_TRACKS.get(company_track)
            if track:
                # Collect all topics from all sections
                for section in track.get("sections", []):
                    for topic in section.get("topics", []):
                        for sub in topic.get("sub_topics", []):
                            company_relevant_topics.append(sub)
    except Exception:
        pass

    tasks: List[Dict[str, Any]] = []
    for area in weak_areas[:limit]:
        domain_id = area["domain_id"]
        topics: List[str] = []
        for tag in (domain_id, area.get("skill", "")):
            if tag:
                topics.append(tag)

        query: Dict[str, Any] = {}
        if topics:
            query["topic"] = {"$in": topics}

        pool: List[Dict[str, Any]] = []
        try:
            pool = question_store.find(query).prefer_verified().to_list()[:50]
        except Exception as exc:
            logger.warning("question-bank fetch failed for %s: %s", domain_id, exc)
            pool = []

        # �� Company-aware filtering: prefer questions tagged with
        # company-relevant topics when a company track is enrolled ��
        if company_relevant_topics and pool:
            lowered = [str(t).lower() for t in company_relevant_topics]

            def _tagged(q: dict) -> bool:
                hay = list(q.get("topics") or []) + list(q.get("tags") or [])
                hay += [q.get("topic", ""), q.get("sub_topic", ""),
                        q.get("pattern", "")]
                hay += list(q.get("companies") or [])
                hay_l = [str(h).lower() for h in hay if h]
                return any(t in hay_l for t in lowered)

            company_pool = [q for q in pool if _tagged(q)]
            if company_pool:
                pool = company_pool

        if not pool:
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


# â”€â”€â”€ 4. CHALLENGE â€” optional higher-difficulty activity â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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
        "description": f"3 timed bugs in {pick} â€” can you fix them under pressure?",
        "estimated_minutes": 12,
        "xp_reward": 60,
        "skill": pick,
    }


# â”€â”€â”€ 5. ROLE ACTIVITY â€” role-specific practice â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def _get_role_activity(user_id: str) -> Optional[Dict[str, Any]]:
    """Get the next role-specific activity for the student.

    Checks if the student has selected a role, then recommends:
    1. SRS reviews for role concepts due now
    2. Role exercises matching weak skills
    3. Role challenges when ready
    4. Mock OA / AI Interview when mastery is high enough
    """
    # Get the student's selected role from their profile
    role_id = await _get_user_role(user_id)
    if not role_id:
        return None

    from app.services.role_content_service import get_next_role_activity
    return await get_next_role_activity(user_id, role_id)


async def _get_user_role(user_id: str) -> Optional[str]:
    """Get the student's selected role from their profile."""
    try:
        from app.database import users_collection
        user = await users_collection.find_one({"user_id": user_id})
        if user:
            return user.get("selected_role")
    except Exception:
        pass
    return None


# â”€â”€â”€ 6. COMPANY MISSION â€” company-aligned daily objective â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def _get_company_mission(user_id: str) -> Optional[Dict[str, Any]]:
    """Get the next company-aligned mission for the student.

    When a company track is enrolled, surfaces:
    - Company-specific coding patterns
    - Company exam-pattern practice
    - Company HR question practice
    """
    try:
        from app.database import users_collection
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            return None

        company_track = user.get("company_track", "")
        target_company = user.get("target_company", "")
        if not company_track and not target_company:
            return None

        from app.data.learning_paths import COMPANY_TRACKS
        track = COMPANY_TRACKS.get(company_track)
        if not track:
            return None

        # Find the first incomplete section
        from app.database import user_company_tracks_collection
        progress = await user_company_tracks_collection.find_one(
            {"user_id": user_id, "track_id": company_track}
        )
        if not progress:
            return None

        sections = progress.get("sections", {})
        for sec_id, sec_data in sections.items():
            if sec_data.get("completed"):
                continue
            modules = sec_data.get("modules", {})
            for mod_id, mod_data in modules.items():
                if mod_data.get("completed"):
                    continue
                return {
                    "type": "company_mission",
                    "title": f"{track['name']}: {sec_data.get('title', 'Practice')}",
                    "description": mod_data.get("module_id", ""),
                    "kind": "company_track",
                    "company": track.get("company_id", ""),
                    "track_id": company_track,
                    "section_id": sec_id,
                    "module_id": mod_id,
                    "estimated_minutes": 30,
                    "xp_reward": 50,
                    "action": "company_track",
                }

        return None
    except Exception:
        return None


# â”€â”€â”€ Orchestrator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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

    # â”€â”€ Inputs from the canonical subsystems â”€â”€
    assessment = await assess_user_skills(user_id)
    weak_areas = await detect_weak_areas(user_id)

    next_mission = await _get_next_mission(user_id)
    reviews = await _get_due_reviews(user_id)
    practice = await _get_practice_tasks(user_id, assessment, weak_areas)
    challenge = await _get_optional_challenge(user_id, assessment, weak_areas)

    # â”€â”€ Role-specific activities (if role selected) â”€â”€
    role_activity = await _get_role_activity(user_id)

    # Company-aligned mission (if company track enrolled)
    company_mission = await _get_company_mission(user_id)

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
        "role_activity": role_activity,
        "company_mission": company_mission,
    }

    est = 0
    task_count = 0
    if next_mission:
        est += next_mission.get("estimated_minutes", 12); task_count += 1
    est += sum(r.get("estimated_minutes", 5) for r in reviews); task_count += len(reviews)
    est += sum(t.get("estimated_minutes", 10) for t in practice); task_count += len(practice)
    if challenge:
        est += challenge.get("estimated_minutes", 12); task_count += 1
    if company_mission:
        est += company_mission.get("estimated_minutes", 30); task_count += 1

    plan["totals"] = {"estimated_minutes": est, "task_count": task_count}

    # Cache for the day (plan is deterministic unless a skill/level changes).
    try:
        from app.services.cache import cache
        import json as _json
        await cache.set("study", f"today:{user_id}:{today}", _json.dumps(plan), ttl=3600)
    except Exception:
        pass

    return plan


# â”€â”€â”€ Activity recording â€” the single completion event â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def record_activity(
    user_id: str,
    activity: Dict[str, Any],
    role: str = "sde",
) -> Dict[str, Any]:
    """Record one LearningEvent and fan-out to mastery / SRS / Diamonds.

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
    raw_skill_id = activity.get("skill_id", "")
    # Normalize any subsystem naming to canonical domain.subskill
    skill_id = canonical_skill_id(raw_skill_id) or raw_skill_id or None
    passed = bool(activity.get("passed", False))
    score = float(activity.get("score", 100.0 if passed else 0.0))
    time_spent = int(activity.get("time_spent", 0))
    diagnosis_codes = list(activity.get("diagnosis_codes", []))
    idempotency_key = activity.get("idempotency_key")

    # ── Idempotency: same key replayed → prior result, zero re-award ──
    # Refresh/replay of a completion endpoint must not farm XP or mastery.
    # Keys are caller-supplied per attempt (e.g. one UUID per mission try).
    if idempotency_key:
        try:
            from app.database import learning_events_collection
            prior = await learning_events_collection().find_one(
                {"user_id": user_id, "idempotency_key": idempotency_key})
            if prior:
                return {
                    "recorded": False,
                    "deduplicated": True,
                    "activity_type": prior.get("activity_type", activity_type),
                    "skill_id": prior.get("skill_id", skill_id),
                    "passed": bool(prior.get("passed", False)),
                    "score": float(prior.get("score") or 0),
                    "diamonds": 0,
                    "xp_awarded": 0,
                    "xp": 0,
                    "xp_applied": False,
                    "mastery_before": prior.get("mastery_before"),
                    "mastery_after": prior.get("mastery_after"),
                    "diagnosis_codes": prior.get("diagnosis_codes", []),
                }
        except Exception as exc:
            logger.warning("idempotency lookup failed for %s: %s", user_id, exc)

    # ── Failure → diagnosis + repair mission (close the loop) ──
    # A failed activity with no caller-supplied codes gets auto-diagnosed,
    # and a repair mission is opened best-effort (mirrors the OA retest
    # path). Passes never open repair. Same-key replays hit the idempotency
    # return above, so repair cannot duplicate for one attempt.
    repair_id = activity.get("repair_id")
    if not passed and skill_id:
        try:
            if not diagnosis_codes:
                from app.services.diagnosis import diagnose_question_failure
                diag = diagnose_question_failure(
                    score, "", "mcq", {},
                    metadata={"all_passed": False, "passed_count": 0, "total": 1,
                              "time_spent": time_spent,
                              "hints_used": int(activity.get("hints_used", 0))},
                )
                if isinstance(diag, dict):
                    diagnosis_codes = diag.get("codes", []) or diagnosis_codes
        except Exception as exc:
            logger.warning("auto-diagnosis failed for %s: %s", user_id, exc)
        try:
            from app.services.repair_service import create_repair_mission
            mission = await create_repair_mission(user_id, [skill_id], source="study_activity")
            if mission is not None:
                repair_id = getattr(mission, "id", None)
        except Exception as exc:
            logger.warning("auto-repair mission failed for %s: %s", user_id, exc)

    # â”€â”€ Mastery update â”€â”€
    mastery_before = None
    mastery_after = None
    if skill_id:
        try:
            from app.services.skill_assessment import update_skill_score
            from app.services.skill_taxonomy import resolve_skill_to_category, resolve_skill_to_competency
            category = resolve_skill_to_category(skill_id)
            sub = resolve_skill_to_competency(skill_id)
            mastery_before = await _fetch_skill_score(user_id, category)
            await update_skill_score(user_id, category, sub, score, passed)
            mastery_after = await _fetch_skill_score(user_id, category)
        except Exception as exc:
            logger.warning("mastery update failed for %s: %s", user_id, exc)

    # â”€â”€ SRS card update â”€â”€
    try:
        from app.services.spaced_repetition import SpacedRepetitionEngine, SRSState
        from app.database import srs_cards_collection

        if skill_id or activity.get("competency_id"):
            prob_id = skill_id or activity.get("competency_id")
            col = srs_cards_collection()
            existing = await col.find_one({"user_id": user_id, "problem_id": prob_id})
            engine = SpacedRepetitionEngine()
            grade = ReviewGrade.GOOD if passed else ReviewGrade.AGAIN
            if existing:
                existing.pop("_id", None)
                state = SRSState(**existing)
                state = engine.review(state, grade)
            else:
                state = engine.create_new_card(concept_id=prob_id, user_id=user_id)
                state = engine.review(state, grade)
            await col.update_one(
                {"user_id": user_id, "problem_id": prob_id},
                {"$set": asdict(state)},
                upsert=True,
            )
    except Exception as exc:
        logger.warning("SRS update skipped for %s: %s", user_id, exc)

    # â”€â”€ Gamification / Diamonds â”€â”€
    diamonds = _xp_for_activity(activity_type, score, passed)
    try:
        prac_result = await record_practice(
            user_id,
            activity_type=activity_type,
            score=score,
            metadata={
                "skill_id": skill_id,
                "time_spent": time_spent,
                "passed": passed,
                # Content Trust instrumentation (additive): lets the team
                # measure % of attempts powered by independently verified
                # content. Present only when the caller supplies it.
                "question_id": activity.get("question_id"),
                "trust_status": activity.get("trust_status"),
                "source_bank": activity.get("source_bank"),
                "verification_version": activity.get("verification_version"),
            },
            role=role,
            activity_id=idempotency_key or None,
        )
        if isinstance(prac_result, dict) and prac_result.get("xp_gained") is not None:
            diamonds = int(prac_result["xp_gained"])
        result["xp_awarded"] = diamonds
        result["xp_applied"] = True
    except Exception as exc:
        logger.warning("gamification record failed for %s: %s", user_id, exc)
        result["xp_awarded"] = diamonds
        result["xp_applied"] = False

    # â”€â”€ Persist canonical LearningEvent â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    try:
        from app.database import learning_events_collection
        from app.models.learning_event import LearningEventIn
        event_in = LearningEventIn(
            activity_type=activity_type,
            source=activity.get("source", "study_engine"),
            skill_id=skill_id,
            subskill_id=activity.get("subskill_id"),
            question_id=activity.get("question_id"),
            assessment_id=activity.get("assessment_id"),
            role=activity.get("role"),
            company=activity.get("company"),
            passed=passed,
            score=score,
            time_spent_seconds=time_spent,
            hints_used=int(activity.get("hints_used", 0)),
            attempt_number=int(activity.get("attempts", 1)),
            mastery_before=mastery_before,
            mastery_after=mastery_after,
            diagnosis_codes=diagnosis_codes,
            repair_id=repair_id,
            idempotency_key=idempotency_key,
            metadata={
                "source_bank": activity.get("source_bank"),
                "trust_status": activity.get("trust_status"),
                "verification_version": activity.get("verification_version"),
            },
        )
        await learning_events_collection().insert_one({
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc),
            **event_in.model_dump(exclude_none=True),
        })
        result["event_id"] = "recorded"
    except Exception as exc:
        logger.warning("LearningEvent persistence failed for %s: %s", user_id, exc)

    result.update({
        "recorded": True,
        "activity_type": activity_type,
        "skill_id": skill_id,
        "passed": passed,
        "score": score,
        "diamonds": diamonds,
        "mastery_before": mastery_before,
        "mastery_after": mastery_after,
        "diagnosis_codes": diagnosis_codes,
        "repair_id": repair_id,
    })
    return result


async def emit_learning_event(user_id: str, event_data: Dict[str, Any]) -> Optional[str]:
    """Emit a single canonical LearningEvent without the full fan-out.

    Use this from routes that produce evidence (OA, interview, question
    submission, repair, retest, SRS) but don't need the full mastery/SRS/Diamonds
    recalculation that record_activity performs.

    Returns the persisted event _id, or None on failure.
    """
    raw_skill = event_data.get("skill_id", "")
    skill_id = canonical_skill_id(raw_skill) or raw_skill or None
    try:
        from app.database import learning_events_collection
        from app.models.learning_event import LearningEventIn
        event_in = LearningEventIn(
            activity_type=event_data.get("activity_type", "practice"),
            source=event_data.get("source", "unknown"),
            skill_id=skill_id,
            subskill_id=event_data.get("subskill_id"),
            question_id=event_data.get("question_id"),
            assessment_id=event_data.get("assessment_id"),
            role=event_data.get("role"),
            company=event_data.get("company"),
            passed=event_data.get("passed", False),
            score=event_data.get("score"),
            time_spent_seconds=int(event_data.get("time_spent_seconds", 0)),
            hints_used=int(event_data.get("hints_used", 0)),
            attempt_number=int(event_data.get("attempt_number", 1)),
            mastery_before=event_data.get("mastery_before"),
            mastery_after=event_data.get("mastery_after"),
            diagnosis_codes=event_data.get("diagnosis_codes", []),
            repair_id=event_data.get("repair_id"),
            metadata=event_data.get("metadata", {}),
        )
        result = await learning_events_collection().insert_one({
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc),
            **event_in.model_dump(exclude_none=True),
        })
        return str(result.inserted_id)
    except Exception as exc:
        logger.warning("emit_learning_event failed for %s: %s", user_id, exc)
        return None


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
    """Map a completed activity to Diamonds.  Mirrors gamification._calculate_xp
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


# â”€â”€â”€ 30-Day Preparation Plan â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def generate_30_day_plan(user_id: str, role_id: str, company_id: str = "") -> Dict[str, Any]:
    """Generate a structured 30-day preparation plan.

    Combines role curriculum + company requirements into a day-by-day plan.
    Each day has: learn, practice, review, and optional assessment.
    """
    from app.content.role_packages import get_role_package
    from app.content.company_journeys import get_company_journey

    role_package = get_role_package(role_id)
    company_journey = get_company_journey(role_id, company_id) if company_id else None

    # Assess current skill level
    assessment = await assess_user_skills(user_id)
    current_level = assessment.get("overall_level", 1)

    days: List[Dict[str, Any]] = []

    for day in range(1, 31):
        day_plan: Dict[str, Any] = {
            "day": day,
            "date": "",
            "phase": _get_phase_for_day(day),
            "activities": [],
            "assessment": None,
        }

        # Week 1: Foundations
        if day <= 7:
            day_plan["activities"].append({
                "type": "learn",
                "title": f"World 1: Day {day} lesson",
                "estimated_minutes": 20,
            })
            day_plan["activities"].append({
                "type": "practice",
                "title": f"Day {day} practice problems",
                "estimated_minutes": 15,
            })

        # Week 2: Role-specific practice
        elif day <= 14:
            day_plan["activities"].append({
                "type": "learn",
                "title": f"Role concept: Day {day}",
                "estimated_minutes": 15,
            })
            day_plan["activities"].append({
                "type": "practice",
                "title": "Role exercises",
                "estimated_minutes": 20,
            })
            day_plan["activities"].append({
                "type": "review",
                "title": "SRS reviews",
                "estimated_minutes": 10,
            })

        # Week 3: Mock assessments
        elif day <= 21:
            day_plan["activities"].append({
                "type": "review",
                "title": "SRS reviews",
                "estimated_minutes": 10,
            })
            day_plan["activities"].append({
                "type": "practice",
                "title": "Timed practice",
                "estimated_minutes": 30,
            })
            if day in [14, 21]:
                day_plan["assessment"] = {
                    "type": "mock_oa",
                    "title": f"Day {day} Mock OA",
                    "duration_minutes": 90,
                }

        # Week 4: Interview prep
        else:
            day_plan["activities"].append({
                "type": "review",
                "title": "Weakness repair",
                "estimated_minutes": 15,
            })
            if day in [25, 28, 30]:
                day_plan["assessment"] = {
                    "type": "ai_interview",
                    "title": f"Day {day} Mock Interview",
                    "duration_minutes": 45,
                }

        days.append(day_plan)

    return {
        "role": role_package.model_dump() if role_package else None,
        "company": company_journey.model_dump() if company_journey else None,
        "current_level": current_level,
        "total_days": 30,
        "days": days,
    }


def _get_phase_for_day(day: int) -> str:
    """Return the preparation phase for a given day."""
    if day <= 7:
        return "foundations"
    elif day <= 14:
        return "practice"
    elif day <= 21:
        return "assessment"
    else:
        return "interview"


# â”€â”€â”€ Mock OA Diagnostic â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def diagnose_mock_oa(user_id: str, responses: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze Mock OA results and generate diagnostic report.

    Returns section analysis, topic weaknesses, time management insights,
    and recommended repair missions.
    """
    score = responses.get("score", 0)
    total = responses.get("total_questions", 1)
    percentage = (score / total) * 100 if total > 0 else 0

    section_analysis = {}
    time_analysis = {}
    weaknesses = []

    # Analyze by section
    for section, results in responses.get("sections", {}).items():
        section_score = results.get("correct", 0)
        section_total = results.get("total", 1)
        section_pct = (section_score / section_total) * 100
        section_analysis[section] = {
            "score": section_score,
            "total": section_total,
            "percentage": section_pct,
            "strength": "strong" if section_pct >= 80 else ("medium" if section_pct >= 60 else "weak"),
        }
        if section_pct < 70:
            weaknesses.append(section)

    # Time management analysis
    time_per_question = responses.get("time_per_question", [])
    if time_per_question:
        avg_time = sum(time_per_question) / len(time_per_question)
        slow_questions = [i for i, t in enumerate(time_per_question) if t > avg_time * 1.5]
        time_analysis = {
            "average_seconds": avg_time,
            "slow_questions": slow_questions,
            "time_management": "good" if len(slow_questions) < len(time_per_question) * 0.2 else "needs_improvement",
        }

    # Generate diagnostic message
    if percentage >= 80:
        diagnostic = "Strong performance. Focus on maintaining consistency."
    elif percentage >= 60:
        diagnostic = f"Good foundation. Losing points on: {', '.join(weaknesses[:3])}. Targeted repair recommended."
    else:
        diagnostic = f"Needs improvement. Key weaknesses: {', '.join(weaknesses[:3])}. Structured repair plan recommended."

    # Create repair missions for weaknesses
    repair_missions = []
    for weakness in weaknesses[:3]:
        repair_missions.append({
            "skill": weakness,
            "priority": "high",
            "recommended_actions": [
                f"Review {weakness} fundamentals",
                f"Practice 5 {weakness} problems",
                f"Take {weakness} quiz",
            ],
        })

    return {
        "overall_score": percentage,
        "correct": score,
        "total": total,
        "section_analysis": section_analysis,
        "time_analysis": time_analysis,
        "weaknesses": weaknesses,
        "diagnostic_message": diagnostic,
        "repair_missions": repair_missions,
        "next_action": "advance" if percentage >= 70 else "repair",
    }


async def record_attempt_diagnostics(
    user_id: str,
    question_id: str,
    selected_option_index: int,
    question_options: List[Any],
) -> Optional[Dict[str, Any]]:
    """Record diagnostics for a single MCQ attempt.

    If the selected option carries a misconception_tag, queue a targeted
    repair mission and record the weakness trigger.

    Args:
        user_id: The student
        question_id: Question attempted
        selected_option_index: Zero-based index of chosen option
        question_options: Raw options list from the question document

    Returns:
        Repair mission payload if a misconception was tagged, else None
    """
    if selected_option_index < 0 or selected_option_index >= len(question_options):
        return None

    selected_option = question_options[selected_option_index]

    # Support both plain-string options and dict metadata options
    if isinstance(selected_option, dict):
        tag = selected_option.get("misconception_tag")
        option_text = selected_option.get("text", "")
    elif isinstance(selected_option, str):
        tag = None
        option_text = selected_option
    else:
        return None

    if not tag:
        return None

    try:
        from app.database import user_weaknesses_collection
        from datetime import datetime, timezone

        await user_weaknesses_collection.update_one(
            {"user_id": user_id, "misconception_tag": tag},
            {
                "$inc": {"trigger_count": 1},
                "$set": {
                    "last_triggered": datetime.now(timezone.utc).isoformat(),
                    "status": "remediation_queued",
                },
                "$setOnInsert": {
                    "user_id": user_id,
                    "misconception_tag": tag,
                    "question_id": question_id,
                    "option_text": option_text,
                },
            },
            upsert=True,
        )

        return {
            "type": "repair_mission",
            "misconception_tag": tag,
            "question_id": question_id,
            "option_text": option_text,
        }
    except Exception:
        return None
