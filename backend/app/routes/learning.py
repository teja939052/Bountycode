"""
Learning Hub routes — languages, levels, lessons, progress, daily goals, quick practice.
"""
from fastapi import APIRouter, Depends, HTTPException, Path
from app.middleware.auth import get_current_user
from app.services.learning import (
    get_user_progress,
    get_language_progress,
    complete_lesson,
    is_lesson_unlocked,
    get_daily_goal,
    get_quick_practice,
    get_leaderboard,
    get_streak,
)
from app.data.curriculum import (
    get_language,
    get_all_languages,
    get_level,
    get_lesson,
    get_next_lesson,
    LANGUAGES,
    LEVEL_THEMES,
)
from app.data.lesson_content import get_lesson_content
# Enrich curriculum with JavaScript track and extra content
import app.data.curriculum_enrichment  # noqa: F401

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


@router.get("/languages")
async def list_languages(user=Depends(get_current_user)):
    """List all available languages with progress stats."""
    langs = get_all_languages()
    progress = await get_user_progress(user["id"])
    lang_progress = progress.get("languages", {})
    daily = await get_daily_goal(user["id"])
    streak = await get_streak(user["id"])

    result = []
    for lang in langs:
        lp = lang_progress.get(lang["id"], {})
        completed_count = len(lp.get("completed_lessons", []))
        quest_counts = {"practice": 0, "challenge": 0, "project": 0, "boss": 0, "theory": 0}
        for level in lang["levels"].values():
            for lesson in level["lessons"]:
                ltype = lesson.get("type", "theory")
                quest_counts[ltype] = quest_counts.get(ltype, 0) + 1
        result.append({
            "id": lang["id"],
            "name": lang["name"],
            "icon": lang["icon"],
            "color": lang["color"],
            "description": lang["description"],
            "total_lessons": lang["total_lessons"],
            "lessons_completed": completed_count,
            "total_xp": lp.get("total_xp", 0),
            "progress_pct": round(completed_count / lang["total_lessons"] * 100) if lang["total_lessons"] > 0 else 0,
            "practice_lessons": quest_counts.get("practice", 0),
            "challenge_lessons": quest_counts.get("challenge", 0),
            "project_lessons": quest_counts.get("project", 0),
            "boss_lessons": quest_counts.get("boss", 0),
            "quest_lessons": quest_counts.get("practice", 0) + quest_counts.get("challenge", 0) + quest_counts.get("project", 0),
        })

    return {
        "languages": result,
        "total_xp": progress.get("total_xp", 0),
        "total_lessons": progress.get("total_lessons_completed", 0),
        "daily_goal": daily,
        "streak": streak,
    }


@router.get("/themes")
async def get_themes():
    """Get level theme data for frontend rendering."""
    return {"themes": LEVEL_THEMES}


@router.get("/daily-goal")
async def daily_goal(user=Depends(get_current_user)):
    """Get today's learning goal status."""
    return await get_daily_goal(user["id"])


VALID_LANG_ID = Path(..., min_length=1, max_length=32, pattern=r"^[a-z0-9_-]+$")
VALID_LEVEL_ID = Path(..., min_length=1, max_length=32, pattern=r"^[a-z0-9_-]+$")
VALID_LESSON_ID = Path(..., min_length=1, max_length=32, pattern=r"^[a-z0-9_-]+$")


@router.get("/quick-practice/{language_id}")
async def quick_practice(language_id: str = VALID_LANG_ID, user=Depends(get_current_user)):
    """Get a denser pack of quick practice lessons."""
    lessons = await get_quick_practice(language_id, 6)
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons available")
    return {"lessons": lessons}


@router.get("/leaderboard")
async def leaderboard(user=Depends(get_current_user)):
    """Get top learners leaderboard."""
    board = await get_leaderboard(20)
    return {"leaderboard": board}


@router.get("/streak")
async def streak(user=Depends(get_current_user)):
    """Get learning streak."""
    return await get_streak(user["id"])


@router.get("/{language_id}/levels")
async def list_levels(language_id: str = VALID_LANG_ID, user=Depends(get_current_user)):
    """List levels for a language with completion stats."""
    lang = get_language(language_id)
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")

    progress = await get_language_progress(user["id"], language_id)
    completed = set(progress.get("completed_lessons", []))

    levels = []
    for level in lang["levels"].values():
        lessons_completed = sum(1 for l in level["lessons"] if l["id"] in completed)
        total = len(level["lessons"])
        quest_counts = {"practice": 0, "challenge": 0, "project": 0, "boss": 0, "theory": 0}
        for lesson in level["lessons"]:
            ltype = lesson.get("type", "theory")
            quest_counts[ltype] = quest_counts.get(ltype, 0) + 1
        levels.append({
            "id": level["id"],
            "name": level["name"],
            "emoji": level.get("emoji", ""),
            "color": level.get("color", "#fff"),
            "bg": level.get("bg", ""),
            "border": level.get("border", ""),
            "text": level.get("text", ""),
            "order": level["order"],
            "description": level["description"],
            "total_lessons": total,
            "lessons_completed": lessons_completed,
            "progress_pct": round(lessons_completed / total * 100) if total > 0 else 0,
            "total_xp": level.get("total_xp", 0),
            "xp_earned": sum(l["xp"] for l in level["lessons"] if l["id"] in completed),
            "practice_lessons": quest_counts.get("practice", 0),
            "challenge_lessons": quest_counts.get("challenge", 0),
            "project_lessons": quest_counts.get("project", 0),
            "boss_lessons": quest_counts.get("boss", 0),
            "quest_lessons": quest_counts.get("practice", 0) + quest_counts.get("challenge", 0) + quest_counts.get("project", 0),
        })

    return {
        "language": {"id": lang["id"], "name": lang["name"], "icon": lang["icon"]},
        "levels": levels,
        "total_xp": progress.get("total_xp", 0),
    }


@router.get("/{language_id}/{level_id}/lessons")
async def list_lessons(
    language_id: str = VALID_LANG_ID,
    level_id: str = VALID_LEVEL_ID,
    user=Depends(get_current_user),
):
    """List lessons for a level with unlock status."""
    level = get_level(language_id, level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    progress = await get_language_progress(user["id"], language_id)
    completed = set(progress.get("completed_lessons", []))

    lessons = []
    for i, lesson in enumerate(level["lessons"]):
        is_completed = lesson["id"] in completed
        if i == 0:
            is_unlocked = True
        else:
            prev_id = level["lessons"][i - 1]["id"]
            is_unlocked = prev_id in completed

        lessons.append({
            **lesson,
            "completed": is_completed,
            "unlocked": is_unlocked,
            "index": i,
        })

    return {
        "language_id": language_id,
        "level": {
            "id": level["id"],
            "name": level["name"],
            "emoji": level.get("emoji", ""),
            "color": level.get("color", "#fff"),
            "order": level["order"],
        },
        "lessons": lessons,
    }


@router.get("/{language_id}/{level_id}/{lesson_id}")
async def get_lesson_detail(
    language_id: str = VALID_LANG_ID,
    level_id: str = VALID_LEVEL_ID,
    lesson_id: str = VALID_LESSON_ID,
    user=Depends(get_current_user),
):
    """Get full lesson content including theory, code examples, and quiz data."""
    lesson = get_lesson(language_id, level_id, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    level = get_level(language_id, level_id)
    unlocked = await is_lesson_unlocked(user["id"], language_id, lesson_id, level["lessons"])
    if not unlocked:
        raise HTTPException(status_code=403, detail="Lesson is locked. Complete the previous lesson first.")

    progress = await get_language_progress(user["id"], language_id)
    is_completed = lesson_id in progress.get("completed_lessons", [])

    next_lesson = get_next_lesson(language_id, level_id, lesson_id)

    content = get_lesson_content(language_id, lesson_id, lesson["title"], lesson["type"])

    return {
        "lesson": lesson,
        "completed": is_completed,
        "next_lesson": next_lesson,
        "level": {
            "id": level["id"],
            "name": level["name"],
            "emoji": level.get("emoji", ""),
            "color": level.get("color", "#fff"),
        },
        "content": content,
    }


@router.post("/{language_id}/{level_id}/{lesson_id}/complete")
async def complete_lesson_route(
    language_id: str = VALID_LANG_ID,
    level_id: str = VALID_LEVEL_ID,
    lesson_id: str = VALID_LESSON_ID,
    user=Depends(get_current_user),
):
    """Mark a lesson as completed and award XP."""
    lesson = get_lesson(language_id, level_id, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    level = get_level(language_id, level_id)
    unlocked = await is_lesson_unlocked(user["id"], language_id, lesson_id, level["lessons"])
    if not unlocked:
        raise HTTPException(status_code=403, detail="Lesson is locked")

    progress = await get_language_progress(user["id"], language_id)
    if lesson_id in progress.get("completed_lessons", []):
        return {"message": "Already completed", "xp_gained": 0, "already_completed": True}

    result = await complete_lesson(user["id"], language_id, lesson_id, lesson["xp"])
    return result


@router.get("/progress")
async def get_overall_progress(user=Depends(get_current_user)):
    """Get overall learning progress across all languages."""
    progress = await get_user_progress(user["id"])
    return progress


@router.get("/{language_id}/stats")
async def get_language_stats(language_id: str = VALID_LANG_ID, user=Depends(get_current_user)):
    """Get detailed stats for a language."""
    lang = get_language(language_id)
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")

    progress = await get_language_progress(user["id"], language_id)
    completed = set(progress.get("completed_lessons", []))

    type_counts = {}
    type_completed = {}
    diff_counts = {1: 0, 2: 0, 3: 0}
    diff_completed = {1: 0, 2: 0, 3: 0}

    for level in lang["levels"].values():
        for lesson in level["lessons"]:
            t = lesson.get("type", "theory")
            d = lesson.get("difficulty", 1)
            type_counts[t] = type_counts.get(t, 0) + 1
            diff_counts[d] = diff_counts.get(d, 0) + 1
            if lesson["id"] in completed:
                type_completed[t] = type_completed.get(t, 0) + 1
                diff_completed[d] = diff_completed.get(d, 0) + 1

    return {
        "language_id": language_id,
        "total_xp": progress.get("total_xp", 0),
        "lessons_completed": len(completed),
        "lessons_total": lang["total_lessons"],
        "by_type": {t: {"completed": type_completed.get(t, 0), "total": type_counts.get(t, 0)} for t in type_counts},
        "by_difficulty": {
            "easy": {"completed": diff_completed.get(1, 0), "total": diff_counts.get(1, 0)},
            "medium": {"completed": diff_completed.get(2, 0), "total": diff_counts.get(2, 0)},
            "hard": {"completed": diff_completed.get(3, 0), "total": diff_counts.get(3, 0)},
        },
    }
