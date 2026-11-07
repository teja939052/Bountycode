"""Lesson service — reusable exam-style learning infrastructure.

Reuses existing question_store, code execution, skill_assessment,
path_generator, and gamification infrastructure. No duplicate systems.

Content is loaded from backend/app/services/lessons/ modules.

Grading truth rules (see docs/learning/BOUNTYCODE_LESSON_AUDIT.md):
- Answer keys never leave the server. ``sanitize_lesson`` is the only shape
  the API may return to a learner.
- Quizzes and exercises are graded here, from the raw catalog, never client-side.
- A wrong answer never records step completion and never awards XP.
- Only graded (verified) attempts produce skill evidence.
- Exercises whose tests have no concrete expected output cannot be verified:
  they are recorded as practice, award no mastery, and do not count toward
  verified completion/XP.
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.database import get_collection
from app.services.code_executor import CodeExecutionEngine
from app.services.skill_assessment import (
    SKILL_CATEGORIES,
    get_skill_graph,
    update_skill_score,
)
from app.services.path_generator import decide_next_action
from app.services.lessons import _LESSONS

logger = logging.getLogger(__name__)

GRADED_TYPES = {"quiz", "exercise"}
_ANSWER_KEYS = ("correctIndex", "solution", "tests")


def _progress_collection():
    """Resolve the lesson-progress collection on every access.

    ``get_collection`` hands back the raw Motor collection bound to the live
    client. The client is recreated when its event loop closes (tests, dev
    reloads), which clears ``database._collections`` but leaves any module-level
    handle pointing at the dead client. Resolving per access always follows the
    live client, so there is no import-time handle to go stale.
    """
    return get_collection("lesson_progress")

# Track -> (skill category, skill) used for evidence. Only real entries from
# SKILL_CATEGORIES are ever written; unmapped tracks record no evidence.
_TRACK_SKILL: Dict[str, Tuple[str, str]] = {
    "python": ("programming", "python"),
    "java": ("programming", "java"),
    "cpp": ("programming", "cpp"),
    "oop": ("programming", "oop"),
    "dbms": ("programming", "dbms"),
    "os": ("programming", "operating_systems"),
    "networks": ("programming", "computer_networks"),
    "aptitude": ("aptitude", "quantitative"),
    "logical": ("aptitude", "logical_reasoning"),
    "verbal": ("aptitude", "verbal_ability"),
    "company_prep": ("behavioral", "problem_solving"),
    "debugging": ("debugging", "debugging_workflow"),
    "system_design": ("system_design", "requirements_gathering"),
    "behavioral": ("behavioral", "communication"),
}

# DSA lessons map to the specific DSA sub-skill their content is about.
_DSA_SKILL_KEYWORDS: Tuple[Tuple[str, str], ...] = (
    ("linked list", "linked_lists"),
    ("binary search tree", "trees"),
    ("tree", "trees"),
    ("graph", "graphs"),
    ("dynamic programming", "dynamic_programming"),
    ("recursion", "recursion"),
    ("greedy", "greedy"),
    ("sort", "sorting"),
    ("hash", "hashing"),
    ("binary search", "binary_search"),
    ("stack", "stacks_queues"),
    ("queue", "stacks_queues"),
    ("array", "arrays"),
    ("string", "strings"),
)

_TRACK_LANGUAGE = {"python": "python", "java": "java", "cpp": "cpp"}

_ENGINE: Optional[CodeExecutionEngine] = None


def _engine() -> CodeExecutionEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = CodeExecutionEngine()
    return _ENGINE


# ═════════════════════════════════════════════════════════════════════
# Answer-key scrubbing — the only lesson shape the API may expose
# ═════════════════════════════════════════════════════════════════════

def sanitize_step(step: dict) -> dict:
    """Copy a step without anything that reveals its answer."""
    clean = {
        k: (list(v) if isinstance(v, list) else v)
        for k, v in step.items()
        if k not in _ANSWER_KEYS
    }
    if step.get("type") in GRADED_TYPES:
        # Quiz/exercise explanations state the answer; explain-step
        # explanations are teaching content and stay.
        clean.pop("explanation", None)
    if step.get("type") == "exercise":
        # Be explicit about machine-grading: an exercise without a concrete
        # expected output is practice only, awards no mastery, and cannot
        # verify a lesson.
        clean["practice_only"] = not runnable_tests(step)
    return clean


def sanitize_lesson(lesson: dict) -> dict:
    """Copy a lesson so graders/answer keys never reach the client."""
    out = dict(lesson)
    out["steps"] = [sanitize_step(s) for s in lesson.get("steps", [])]
    return out


# ═════════════════════════════════════════════════════════════════════
# Catalog
# ═════════════════════════════════════════════════════════════════════

def list_lessons(track: Optional[str] = None) -> List[dict]:
    """Return all lessons, optionally filtered by track."""
    lessons = list(_LESSONS.values())
    if track:
        lessons = [l for l in lessons if l["track"] == track]
    return lessons


def search_lessons(query: str, track: Optional[str] = None) -> List[dict]:
    """Search lessons by title, description, step title/content."""
    q = query.lower()
    results = []
    for lesson in _LESSONS.values():
        if track and lesson["track"] != track:
            continue
        haystack = f"{lesson['title']} {lesson.get('description', '')} "
        for step in lesson.get("steps", []):
            haystack += f" {step.get('title', '')} {step.get('content', '')} {step.get('instruction', '')} {step.get('question', '')}"
        if q in haystack.lower():
            results.append(lesson)
    return results


def get_lesson(lesson_id: str) -> Optional[dict]:
    """Return a single raw lesson by id (server-side use only)."""
    return _LESSONS.get(lesson_id)


def get_public_lesson(lesson_id: str) -> Optional[dict]:
    """Return a lesson safe to send to a learner."""
    lesson = get_lesson(lesson_id)
    return sanitize_lesson(lesson) if lesson else None


# ═════════════════════════════════════════════════════════════════════
# Grading (server-side, trusted)
# ═════════════════════════════════════════════════════════════════════

def _option_index(step: dict, answer: Any) -> Optional[int]:
    """Resolve a submitted answer (index or option text) to an option index."""
    options = step.get("options") or []
    if answer is None:
        return None
    text = str(answer).strip()
    if text == "":
        return None
    if text.isdigit() and 0 <= int(text) < len(options):
        return int(text)
    for idx, option in enumerate(options):
        if str(option).strip().casefold() == text.casefold():
            return idx
    return None


def grade_quiz(step: dict, answer: Any) -> dict:
    """Grade a quiz answer against the server-side key."""
    options = step.get("options") or []
    correct = step.get("correctIndex")
    selected = _option_index(step, answer)

    if selected is None:
        return {
            "is_correct": None,
            "graded": False,
            "attempted": answer is not None and str(answer).strip() != "",
            "feedback": "Choose one of the options before submitting.",
            "test_results": None,
        }
    if not isinstance(correct, int) or not 0 <= correct < len(options):
        logger.error(
            "Quiz step %r has no usable correctIndex; cannot grade", step.get("id")
        )
        return {
            "is_correct": None,
            "graded": False,
            "attempted": True,
            "feedback": "This question has no answer key configured, so it cannot be graded yet.",
            "test_results": None,
        }
    if selected != correct:
        return {
            "is_correct": False,
            "graded": True,
            "attempted": True,
            "feedback": "Not quite — review the lesson and try again.",
            "test_results": None,
        }
    return {
        "is_correct": True,
        "graded": True,
        "attempted": True,
        "feedback": "Correct!",
        "test_results": None,
    }


def runnable_tests(step: dict) -> List[dict]:
    """Return only tests that carry a concrete expected output."""
    tests: List[dict] = []
    for case in step.get("tests") or []:
        if not isinstance(case, dict):
            continue
        expected = case.get("expected", case.get("expected_output"))
        if expected is None or str(expected) == "":
            continue
        stdin = case.get("input", case.get("stdin")) or ""
        tests.append({"input": str(stdin), "expected": str(expected)})
    return tests


async def grade_exercise(lesson: dict, step: dict, code: str) -> dict:
    """Run an exercise's tests. Non-runnable tests are practice only."""
    source = (code or "").strip()
    if not source:
        return {
            "is_correct": None,
            "graded": False,
            "attempted": False,
            "feedback": "Write your answer before submitting.",
            "test_results": None,
        }

    tests = runnable_tests(step)
    language = lesson.get("language") or _TRACK_LANGUAGE.get(lesson.get("track", ""))

    if not tests or not language:
        reason = (
            "This exercise has no automated check yet, so it is recorded as "
            "practice. It does not count toward verified mastery or XP."
        )
        return {
            "is_correct": None,
            "graded": False,
            "attempted": True,
            "feedback": reason,
            "test_results": None,
        }

    result = await _engine().execute_against_test_cases(source, language, tests)
    if not result.get("success"):
        return {
            "is_correct": False,
            "graded": True,
            "attempted": True,
            "feedback": f"Could not run your code: {result.get('error', 'execution failed')}",
            "test_results": None,
        }

    results = result.get("results") or []
    passed = result.get("passed_count", 0)
    total = result.get("total_count", len(tests))
    all_passed = bool(result.get("all_passed"))

    if all_passed:
        feedback = f"All {total} test(s) passed."
    else:
        first_fail = next((r for r in results if not r.get("passed")), None)
        if first_fail and not first_fail.get("is_hidden"):
            feedback = (
                f"{passed}/{total} test(s) passed. "
                f"Expected {first_fail.get('expected', '')!r}, "
                f"got {first_fail.get('actual', '')!r}."
            )
        else:
            feedback = f"{passed}/{total} test(s) passed. Keep going."

    return {
        "is_correct": all_passed,
        "graded": True,
        "attempted": True,
        "feedback": feedback,
        "test_results": [
            {
                "index": r.get("test_case_index"),
                "passed": r.get("passed", False),
                "expected": r.get("expected"),
                "actual": r.get("actual"),
            }
            for r in results
            if not r.get("is_hidden")
        ],
        "score": round(passed / total * 100, 1) if total else 0.0,
    }


def skill_for_lesson(lesson: dict) -> Optional[Tuple[str, str]]:
    """Map a lesson to a real (category, skill) in the skill graph."""
    track = lesson.get("track", "")
    if track == "dsa":
        text = f"{lesson.get('id', '')} {lesson.get('title', '')}".lower()
        normalized = text.replace("-", " ").replace("_", " ")
        for keyword, skill in _DSA_SKILL_KEYWORDS:
            if keyword in normalized:
                return "dsa", skill
        return None

    mapping = _TRACK_SKILL.get(track)
    if not mapping:
        return None
    category, skill = mapping
    known = SKILL_CATEGORIES.get(category, {}).get("skills", [])
    if skill not in known:
        logger.error("Skill %r is not part of category %r", skill, category)
        return None
    return category, skill


# ═════════════════════════════════════════════════════════════════════
# Progress tracking
# ═════════════════════════════════════════════════════════════════════

async def get_progress(user_id: str) -> dict:
    """Get the user's lesson progress."""
    doc = await _progress_collection().find_one({"user_id": user_id})
    if not doc:
        return {
            "completed": {},
            "current_lesson": None,
            "xp_earned": 0,
            "verified_lessons": [],
            "awarded_lessons": [],
        }
    return {
        "completed": doc.get("completed", {}),
        "current_lesson": doc.get("current_lesson"),
        "xp_earned": doc.get("xp_earned", 0),
        "verified_lessons": doc.get("verified_lessons", []),
        "awarded_lessons": doc.get("awarded_lessons", []),
    }


def weakness_tier_for(mastery: float) -> str:
    """Deterministic tier from measured mastery (0.0-1.0)."""
    if mastery < 0.40:
        return "critical"
    if mastery < 0.60:
        return "weak"
    if mastery < 0.85:
        return "on_track"
    return "strong"


async def _record_evidence(
    user_id: str,
    lesson: dict,
    step: dict,
    graded: bool,
    is_correct: bool,
    score: float,
) -> Optional[Tuple[str, str]]:
    """Record a verified attempt against the matching real skill."""
    if not graded:
        return None
    target = skill_for_lesson(lesson)
    if not target:
        return None
    category, skill = target
    try:
        await update_skill_score(
            user_id=user_id,
            category=category,
            skill=skill,
            score=score,
            is_correct=is_correct,
        )
    except Exception:
        logger.exception(
            "Failed to record skill evidence for %s/%s", category, skill
        )
        return None
    return target


async def _award_gamification_xp(user_id: str, lesson_id: str, xp: int) -> int:
    """Mirror verified lesson XP into gamification exactly once.

    Imported lazily: gamification imports the database layer eagerly and this
    module must stay importable from the catalog alone (tests, scripts).
    """
    try:
        from app.services.gamification import award_lesson_xp

        return await award_lesson_xp(user_id, lesson_id, xp)
    except Exception:
        logger.exception(
            "Failed to mirror %s XP from lesson %s into gamification", xp, lesson_id
        )
        return 0


async def complete_step(
    user_id: str,
    lesson_id: str,
    step_id: str,
    code: str = "",
    answer: Optional[str] = None,
) -> dict:
    """Grade and record a lesson step, then return the next action."""
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise ValueError(f"Lesson {lesson_id} not found")

    step = next((s for s in lesson["steps"] if s["id"] == step_id), None)
    if not step:
        raise ValueError(f"Step {step_id} not found")

    step_type = step.get("type")
    step_key = f"{lesson_id}:{step_id}"
    now = datetime.now(timezone.utc)

    if step_type == "quiz":
        outcome = grade_quiz(step, answer)
        stored_value, stored_field = str(answer if answer is not None else ""), "answer"
    elif step_type == "exercise":
        outcome = await grade_exercise(lesson, step, code)
        stored_value, stored_field = code, "code"
    elif step_type == "explain":
        # Reading content is a real progress action but produces no evidence.
        outcome = {
            "is_correct": None,
            "graded": False,
            "attempted": True,
            "feedback": "",
            "test_results": None,
        }
        stored_value, stored_field = "", "code"
    else:
        raise ValueError(f"Unsupported step type {step_type!r}")

    graded = bool(outcome.get("graded"))
    is_correct = outcome.get("is_correct")
    attempted = bool(outcome.get("attempted"))

    # Wrong answers and empty submissions never complete a step.
    if not attempted:
        step_completed = False
    elif graded:
        step_completed = is_correct is True
    else:
        step_completed = step_type in ("exercise", "explain")

    # Verified attempts are the only source of personalization evidence.
    # Re-submitting a step that is already verified correct must not inflate
    # mastery, so a replay records no new evidence.
    progress = await get_progress(user_id)
    completed = dict(progress.get("completed", {}))
    previous = completed.get(step_key)
    already_verified = bool(previous and previous.get("verified") is True)

    evidence = None
    if graded and not (already_verified and is_correct is True):
        score = outcome.get("score")
        if score is None:
            score = 100.0 if is_correct else 0.0
        evidence = await _record_evidence(
            user_id, lesson, step, graded, bool(is_correct), float(score)
        )

    if step_completed:
        # Never downgrade an already-verified step with a practice submission.
        if not previous or previous.get("is_correct") is not True:
            completed[step_key] = {
                "completed_at": now.isoformat(),
                stored_field: stored_value,
                "is_correct": is_correct,
                "graded": graded,
                "verified": graded and is_correct is True,
            }

    lesson_step_ids = [s["id"] for s in lesson["steps"]]
    lesson_done = all(f"{lesson_id}:{sid}" in completed for sid in lesson_step_ids)

    graded_records = []
    for sid in lesson_step_ids:
        record = completed.get(f"{lesson_id}:{sid}")
        if not record:
            continue
        step_def = next(s for s in lesson["steps"] if s["id"] == sid)
        if step_def.get("type") in GRADED_TYPES and record.get("graded"):
            graded_records.append(record)
    lesson_verified = (
        lesson_done
        and any(r.get("is_correct") is True for r in graded_records)
        and all(r.get("is_correct") is True for r in graded_records)
    )

    awarded = set(progress.get("awarded_lessons", []))
    xp_awarded = 0
    if lesson_verified and lesson_id not in awarded:
        xp_awarded = int(lesson.get("xpReward", 0) or 0)
        awarded.add(lesson_id)
    total_xp = int(progress.get("xp_earned", 0)) + xp_awarded

    verified_lessons = set(progress.get("verified_lessons", []))
    if lesson_verified:
        verified_lessons.add(lesson_id)

    await _progress_collection().update_one(
        {"user_id": user_id},
        {
            "$set": {
                "completed": completed,
                "current_lesson": lesson_id if not lesson_done else None,
                "xp_earned": total_xp,
                "verified_lessons": sorted(verified_lessons),
                "awarded_lessons": sorted(awarded),
                "updated_at": now,
            }
        },
        upsert=True,
    )

    # Mirror verified lesson XP into the gamification ledger. Lesson rewards
    # persist in lesson_progress while the dashboard reads the separate
    # gamification collection; without this bridge lesson XP would be invisible
    # to levels, streaks, and the tower.
    gamification_xp_awarded = 0
    if xp_awarded > 0:
        gamification_xp_awarded = await _award_gamification_xp(
            user_id, lesson_id, xp_awarded
        )

    # Next action from measured mastery only.
    mastery, attempts, category_score = 0.0, 0, 0.0
    if evidence:
        category, skill = evidence
        graph = await get_skill_graph(user_id)
        cat = (graph.get("categories") or {}).get(category, {}) or {}
        skill_data = (cat.get("skills") or {}).get(skill, {}) or {}
        attempts = int(skill_data.get("attempts", 0) or 0)
        category_score = float(cat.get("score", 0) or 0)
        if attempts:
            mastery = round(float(skill_data.get("score", 0) or 0) / 100.0, 4)

    next_action = decide_next_action(
        pattern=lesson["track"],
        mastery=mastery,
        weakness_tier=weakness_tier_for(mastery),
    )
    next_action["attempts"] = attempts
    next_action["category_score"] = category_score
    if evidence:
        next_action["category"], next_action["skill"] = evidence

    return {
        "is_correct": is_correct,
        "graded": graded,
        "verified": graded and is_correct is True,
        "feedback": outcome.get("feedback", ""),
        "test_results": outcome.get("test_results"),
        "step_completed": step_completed,
        "lesson_complete": lesson_done,
        "lesson_verified": lesson_verified,
        "xp_earned": xp_awarded,
        "gamification_xp_awarded": gamification_xp_awarded,
        "total_xp": total_xp,
        "next_action": next_action,
    }


async def submit_exercise(
    user_id: str, lesson_id: str, step_id: str, code: str
) -> dict:
    """Submit an exercise answer (alias for complete_step)."""
    return await complete_step(user_id, lesson_id, step_id, code=code)


async def next_lesson(user_id: str, current_lesson_id: str) -> Optional[dict]:
    """Return the next recommended lesson."""
    progress = await get_progress(user_id)
    completed = set(
        k.split(":")[0]
        for k, v in progress.get("completed", {}).items()
        if not k.startswith("_")
    )
    for lesson in _LESSONS.values():
        if lesson["id"] not in completed:
            prereqs = lesson.get("prerequisites", [])
            if all(p in completed for p in prereqs):
                return lesson
    return None
