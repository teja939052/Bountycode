"""Door 2 (dev) & Door 3 (beginner) launch flows.

Door 2 ("I want to become a developer"): the learner picks an adventure track, we run
a short interactive probe from that track's capability world, seed the skill graph,
show the world progression as their path, and hand back the first 3 missions.

Door 3 ("I'm new to tech"): the learner bypasses any diagnosis and gets one tiny,
non-graded interactive mission from the very first capability competency so they feel
immediate progress from zero.

REUSES existing engines only (capability_curriculum, curriculum_connector, skill_graph,
quest_engine). No new curriculum/readiness/dashboard abstraction.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.data.capability_curriculum import ALL_WORLDS
from app.services.curriculum_connector import get_competency_with_fallback

# Door-2 adventure track -> capability world it starts in.
TRACK_WORLD: Dict[str, str] = {
    "programming": "code_foundations",
    "cs": "software_engineering",
    "algorithms": "problem_solver",
    "backend": "build_systems",
    "ai": "work_with_data",
}

# Ordered capability progression. Everything after the chosen track is their path.
WORLD_ORDER: List[str] = [
    "code_foundations",
    "problem_solver",
    "build_systems",
    "work_with_data",
    "software_engineering",
    "under_pressure",
    "hiring_arena",
]

GRADABLE_STEP_TYPES = {"predict", "break", "explore"}


def _world_row(world_id: str) -> Dict[str, Any]:
    w = ALL_WORLDS.get(world_id) or {}
    return {
        "world_id": world_id,
        "title": w.get("title", world_id.replace("_", " ").title()),
        "description": w.get("description", ""),
        "competency_count": len(w.get("competencies", [])),
    }


def _gradable_steps(competency_key: str) -> List[Dict[str, Any]]:
    """Extract gradable MCQ/output steps from a competency, mapped to canonical skills."""
    comp = get_competency_with_fallback(competency_key)
    if not comp:
        return []
    canon: set = set()
    from app.services.curriculum_connector import resolve_capability_skill

    for _skill in comp["skills_taught"]:
        cid = resolve_capability_skill(_skill)
        if cid and "." in cid:
            canon.add(cid)
    out = []
    for step in comp["competency"].get("steps", []):
        if step.get("type") not in GRADABLE_STEP_TYPES:
            continue
        if step.get("type") == "explore" and not step.get("expected_output"):
            continue
        out.append({
            "id": f"{competency_key}::{step.get('title')}",
            "type": step.get("type"),
            "title": step.get("title"),
            "prompt": step.get("question")
            or step.get("content")
            or ("What does this code print?" if step.get("type") == "explore" else step.get("title")),
            "code": step.get("code"),
            "options": step.get("options"),
            "correct_set": step.get("correct_set"),
            "expected_output": step.get("expected_output"),
            "canonical_skills": sorted(canon),
            "explanation": step.get("explanation") or step.get("hint"),
        })
    return out[:8]


def _grade(question: Dict[str, Any], answer: Any) -> bool:
    qtype = question.get("type")
    if qtype == "predict":
        options = question.get("options") or []
        correct = {o["id"] for o in options if o.get("correct")}
        return bool(correct) and str(answer) in correct
    if qtype == "break":
        correct = set(question.get("correct_set") or [])
        if not correct:
            return False
        given = set(answer) if isinstance(answer, (list, set, tuple)) else {answer}
        return given == correct
    if qtype == "explore":
        expected = (question.get("expected_output") or "").strip()
        return bool(expected) and _norm(answer) == _norm(expected)
    return False


def _norm(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _build_path(track: str) -> Dict[str, Any]:
    start = TRACK_WORLD.get(track, "code_foundations")
    order = WORLD_ORDER
    start_idx = order.index(start) if start in order else 0
    segments = order[start_idx:]
    return {
        "track": track,
        "start_world": start,
        "start_world_title": _world_row(start)["title"],
        "worlds": [_world_row(w) for w in segments],
        "current_world_idx": 0,
    }


def _first_missions(track: str, gaps: List[str]) -> List[Dict[str, Any]]:
    missions: List[Dict[str, Any]] = []
    start = TRACK_WORLD.get(track, "code_foundations")
    comp = (ALL_WORLDS.get(start) or {}).get("competencies", [])
    first_comp = comp[0].get("id") if comp else "validator"

    missions.append({
        "mission_id": f"dev_{track}_0",
        "quest_type": "adventure_start",
        "title": f"Enter the {ALL_WORLDS.get(start, {}).get('title', start)}",
        "description": (
            f"Your first world: {_world_row(start)['title']}. Complete its opening "
            f"challenge to unlock the path ahead."
        ),
        "topic": start,
        "competency_id": f"{start}/{first_comp}",
        "difficulty": "easy",
        "target_count": 1,
        "xp_reward": 100,
        "estimated_minutes": 10,
        "current_count": 0,
        "is_complete": False,
    })
    if gaps:
        missions.append({
            "mission_id": f"dev_{track}_weak",
            "quest_type": "weakness_recovery",
            "title": f"Sharpen your {gaps[0].replace('_', ' ').title()}",
            "description": "One focused exercise to turn an early gap into a strength.",
            "topic": gaps[0],
            "difficulty": "easy",
            "target_count": 2,
            "xp_reward": 120,
            "estimated_minutes": 12,
            "current_count": 0,
            "is_complete": False,
        })
    missions.append({
        "mission_id": f"dev_{track}_rhythm",
        "quest_type": "streak_maintenance",
        "title": "Build the habit",
        "description": "Come back tomorrow — consistency is how learning becomes skill.",
        "topic": "general",
        "difficulty": "easy",
        "target_count": 1,
        "xp_reward": 50,
        "estimated_minutes": 8,
        "current_count": 0,
        "is_complete": False,
    })
    return missions[:3]


def get_dev_launch(track: str) -> Dict[str, Any]:
    if track not in TRACK_WORLD:
        track = "programming"
    start = TRACK_WORLD[track]
    comp_key = f"{start}/{(ALL_WORLDS[start]['competencies'][0]['id'])}"
    questions = _gradable_steps(comp_key)
    # The capability curriculum only holds gradable MCQ/output steps inside
    # code_foundations today. For tracks whose world has none yet, probe the
    # universal coding baseline so every learner still gets a real, short check.
    if not questions:
        questions = _gradable_steps("code_foundations/validator")
    return {
        "track": track,
        "start_world": _world_row(start),
        "path": _build_path(track),
        "questions": questions,
    }


async def run_dev_launch(user_id: str, track: str, answers: Dict[str, Any]) -> Dict[str, Any]:
    from app.services.skill_assessment import update_skill_score

    data = get_dev_launch(track)
    questions = data["questions"]

    cat_correct: Dict[str, List[bool]] = {}
    graded = []
    for q in questions:
        ok = _grade(q, answers.get(q["id"])) if answers.get(q["id"]) is not None else False
        graded.append({"id": q["id"], "title": q["title"], "type": q["type"], "is_correct": ok})
        for cid in q.get("canonical_skills", []):
            if "." in cid:
                cat = cid.split(".", 1)[0]
                cat_correct.setdefault(cat, []).append(ok)

    for cat, results in cat_correct.items():
        acc = sum(1 for c in results if c) / len(results) if results else 0.0
        await update_skill_score(user_id, cat, f"{cat}_adventure", acc * 100, acc >= 0.6)

    baseline = {
        cat: round(sum(1 for c in r if c) / len(r) * 100, 1) for cat, r in cat_correct.items()
    }
    gaps = sorted(baseline, key=lambda k: baseline[k])[:2] if baseline else []

    result = {
        "status": "ok",
        "track": track,
        "path": data["path"],
        "graded": graded,
        "correct_count": sum(1 for g in graded if g["is_correct"]),
        "question_count": len(graded),
        "baseline_categories": baseline,
        "first_missions": _first_missions(track, gaps),
    }

    try:
        from bson import ObjectId
        from app.database import users_collection

        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "career_goal.door": "dev",
                "career_goal.dev_track": track,
                "career_goal.launch": {
                    "completed": True,
                    "completed_at": datetime.now(timezone.utc),
                    "start_world": data["start_world"]["world_id"],
                    "first_missions": result["first_missions"],
                },
            }},
        )
    except Exception:
        pass

    return result


def get_beginner_go() -> Dict[str, Any]:
    """Return the tiny, non-graded first mission content for a brand-new learner."""
    comp_key = "code_foundations/validator"
    comp = get_competency_with_fallback(comp_key)
    steps = []
    if comp:
        for s in comp["competency"].get("steps", [])[:4]:
            steps.append({
                "type": s.get("type"),
                "title": s.get("title"),
                "content": s.get("content"),
                "code": s.get("code"),
                "simulation": s.get("simulation"),
            })
    path = _build_path("programming")
    return {
        "status": "ok",
        "title": "Your first step from zero",
        "intro": (
            "No prior knowledge needed. We start with what happens when a program "
            "reads input — then build from there, one gentle step at a time."
        ),
        "steps": steps,
        "path": path,
    }


async def run_beginner_go(user_id: str) -> Dict[str, Any]:
    data = get_beginner_go()
    try:
        from bson import ObjectId
        from app.database import users_collection

        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "career_goal.door": "beginner",
                "career_goal.launch": {
                    "completed": True,
                    "completed_at": datetime.now(timezone.utc),
                    "start_world": "code_foundations",
                    "first_module": "code_foundations/validator",
                },
            }},
        )
    except Exception:
        pass
    return data
