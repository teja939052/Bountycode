"""Regression tests for Phase B P0 lesson issues.

Covers the audit findings:
- catalog uniqueness, prerequisites, and template filler
- answer keys are never exposed by lesson GET/list/search payloads
- quizzes and exercises are graded server-side
- wrong answers do not complete steps, lessons, or award XP
- explain-only / unverifiable content produces no verified mastery
- skill evidence uses a real category/skill and measured mastery
"""
import copy
from types import SimpleNamespace

import pytest

from app.services import lesson_service
from app.services.lesson_service import (
    grade_quiz,
    get_public_lesson,
    sanitize_lesson,
    skill_for_lesson,
    weakness_tier_for,
)
from app.services.lessons import _DROPPED_DUPLICATES, _LESSONS

ANSWER_KEYS = ("correctIndex", "solution", "tests")


# ═════════════════════════════════════════════════════════════════════
# Fixtures: in-memory progress + fake skill evidence
# ═════════════════════════════════════════════════════════════════════

class FakeCollection:
    def __init__(self):
        self.docs = {}

    async def find_one(self, query):
        return copy.deepcopy(self.docs.get(query.get("user_id")))

    async def update_one(self, query, update, upsert=False):
        uid = query["user_id"]
        doc = self.docs.setdefault(uid, {"user_id": uid})
        for key, value in update.get("$set", {}).items():
            doc[key] = copy.deepcopy(value)


@pytest.fixture
def env(monkeypatch):
    collection = FakeCollection()
    evidence = []
    mastery = {"attempts": 0, "score": 0.0, "category_score": 0.0}

    async def fake_update_skill_score(user_id, category, skill, score, is_correct):
        evidence.append(
            {
                "user_id": user_id,
                "category": category,
                "skill": skill,
                "score": score,
                "is_correct": is_correct,
            }
        )

    async def fake_get_skill_graph(user_id):
        return {
            "categories": {
                "programming": {
                    "score": mastery["category_score"],
                    "skills": {
                        "python": {
                            "attempts": mastery["attempts"],
                            "score": mastery["score"],
                        }
                    },
                }
            }
        }

    monkeypatch.setattr(
        lesson_service, "_progress_collection", lambda: collection
    )
    monkeypatch.setattr(lesson_service, "update_skill_score", fake_update_skill_score)
    monkeypatch.setattr(lesson_service, "get_skill_graph", fake_get_skill_graph)

    gamification = []

    async def fake_award_gamification_xp(user_id, lesson_id, xp):
        gamification.append({"user_id": user_id, "lesson_id": lesson_id, "xp": xp})
        return xp

    monkeypatch.setattr(
        lesson_service, "_award_gamification_xp", fake_award_gamification_xp
    )
    return SimpleNamespace(
        collection=collection, evidence=evidence, mastery=mastery, gamification=gamification
    )


def step_of(lesson_id, step_type):
    lesson = _LESSONS[lesson_id]
    return next(s for s in lesson["steps"] if s["type"] == step_type)


# ═════════════════════════════════════════════════════════════════════
# Catalog integrity (audit P0: duplicates, filler, broken prerequisites)
# ═════════════════════════════════════════════════════════════════════

def test_catalog_has_no_duplicate_ids():
    assert _DROPPED_DUPLICATES == [], f"duplicate lesson ids: {_DROPPED_DUPLICATES}"
    listed = [l["id"] for l in _LESSONS.values()]
    assert len(listed) == len(set(listed))


def test_catalog_has_no_broken_prerequisites():
    ids = set(_LESSONS)
    broken = [
        (lesson_id, prereq)
        for lesson_id, lesson in _LESSONS.items()
        for prereq in (lesson.get("prerequisites") or [])
        if prereq not in ids
    ]
    assert broken == []


def test_catalog_has_no_template_filler():
    filler = [
        lesson_id
        for lesson_id, lesson in _LESSONS.items()
        if "Example code here" in str(lesson) or "hands-on examples" in str(lesson)
    ]
    assert filler == []


@pytest.mark.parametrize("lesson_id", sorted(_LESSONS))
def test_every_lesson_has_gradable_shape(lesson_id):
    """Every lesson must teach or test something; no empty shells."""
    lesson = _LESSONS[lesson_id]
    assert lesson["steps"], f"{lesson_id} has no steps"
    for step in lesson["steps"]:
        assert step["type"] in ("explain", "exercise", "quiz")
        if step["type"] == "quiz":
            assert step.get("options"), f"{lesson_id}/{step['id']} quiz has no options"
            assert isinstance(step.get("correctIndex"), int), (
                f"{lesson_id}/{step['id']} quiz has no server answer key"
            )


# ═════════════════════════════════════════════════════════════════════
# Answer-key scrubbing (audit P0: GET payloads leaked answers)
# ═════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("lesson_id", sorted(_LESSONS))
def test_public_lesson_never_leaks_answer_keys(lesson_id):
    public = get_public_lesson(lesson_id)
    assert public is not None
    for step in public["steps"]:
        for key in ANSWER_KEYS:
            assert key not in step, f"{lesson_id}/{step['id']} leaked {key}"
        if step["type"] in ("quiz", "exercise"):
            assert "explanation" not in step, (
                f"{lesson_id}/{step['id']} leaked graded explanation"
            )


def test_explain_step_keeps_teaching_explanation():
    public = get_public_lesson("python-hello")
    explain = next(s for s in public["steps"] if s["id"] == "hello-1")
    assert explain.get("explanation")


def test_public_payload_is_a_copy_not_the_catalog():
    public = get_public_lesson("python-hello")
    step = next(s for s in public["steps"] if s["id"] == "hello-4")
    step["options"].append("mutated")
    assert "mutated" not in _LESSONS["python-hello"]["steps"][3]["options"]


async def test_lesson_routes_return_sanitized_payloads():
    from app.routes.lessons import get_lesson_route, list_all_lessons, search_lessons_route

    lesson = await get_lesson_route("python-hello")
    assert all(key not in str(lesson) for key in ANSWER_KEYS)

    listing = await list_all_lessons(track="python")
    assert listing["lessons"]
    assert all(key not in str(l) for l in listing["lessons"] for key in ANSWER_KEYS)

    search = await search_lessons_route("print")
    assert all(key not in str(l) for l in search["lessons"] for key in ANSWER_KEYS)


def test_static_lesson_routes_precede_dynamic_route():
    """`/progress` and `/next` must not be captured by `/{lesson_id}`."""
    from app.routes.lessons import router

    paths = [route.path for route in router.routes]
    dynamic = paths.index("/api/v1/lessons/{lesson_id}")
    assert paths.index("/api/v1/lessons/progress") < dynamic
    assert paths.index("/api/v1/lessons/next") < dynamic


# ═════════════════════════════════════════════════════════════════════
# Quiz grading (audit P0: quizzes were graded in the browser)
# ═════════════════════════════════════════════════════════════════════

def test_quiz_accepts_option_index():
    step = step_of("python-hello", "quiz")
    result = grade_quiz(step, str(step["correctIndex"]))
    assert result["is_correct"] is True
    assert result["graded"] is True


def test_quiz_accepts_option_text():
    step = step_of("python-hello", "quiz")
    result = grade_quiz(step, step["options"][step["correctIndex"]])
    assert result["is_correct"] is True


def test_quiz_rejects_wrong_option():
    step = step_of("python-hello", "quiz")
    wrong = "1" if step["correctIndex"] != 1 else "0"
    result = grade_quiz(step, wrong)
    assert result["is_correct"] is False
    assert result["graded"] is True
    # The wrong-answer feedback must never reveal the correct option.
    assert step["options"][step["correctIndex"]] not in result["feedback"]


def test_quiz_rejects_unknown_answer():
    step = step_of("python-hello", "quiz")
    result = grade_quiz(step, "not an option")
    assert result["is_correct"] is None
    assert result["graded"] is False


async def test_wrong_quiz_does_not_complete_step_or_lesson(env):
    lesson_id = "python-hello"
    step = step_of(lesson_id, "quiz")
    wrong = "1" if step["correctIndex"] != 1 else "0"

    result = await lesson_service.complete_step(
        "u1", lesson_id, step["id"], code="", answer=wrong
    )
    assert result["is_correct"] is False
    assert result["step_completed"] is False
    assert result["lesson_complete"] is False
    assert result["lesson_verified"] is False
    assert result["xp_earned"] == 0

    progress = await lesson_service.get_progress("u1")
    assert f"{lesson_id}:{step['id']}" not in progress["completed"]


async def test_correct_quiz_completes_lesson_and_awards_xp_once(env):
    lesson_id = "python-hello"
    lesson = _LESSONS[lesson_id]
    quiz = step_of(lesson_id, "quiz")

    for step in lesson["steps"]:
        if step["type"] == "explain":
            await lesson_service.complete_step("u2", lesson_id, step["id"])
        elif step["type"] == "exercise":
            await lesson_service.complete_step(
                "u2", lesson_id, step["id"], code='print("Ada")'
            )

    first = await lesson_service.complete_step(
        "u2", lesson_id, quiz["id"], answer=str(quiz["correctIndex"])
    )
    assert first["is_correct"] is True
    assert first["lesson_complete"] is True
    assert first["xp_earned"] == lesson["xpReward"]

    again = await lesson_service.complete_step(
        "u2", lesson_id, quiz["id"], answer=str(quiz["correctIndex"])
    )
    assert again["xp_earned"] == 0, "XP must not be awarded twice"
    progress = await lesson_service.get_progress("u2")
    assert progress["xp_earned"] == lesson["xpReward"]


# ═════════════════════════════════════════════════════════════════════
# Exercise grading (audit P0: tests never ran, solution was compared)
# ═════════════════════════════════════════════════════════════════════

async def test_runnable_exercise_runs_tests_and_passes(env):
    lesson_id = "python-comprehensions"
    step = step_of(lesson_id, "exercise")

    result = await lesson_service.complete_step(
        "u3",
        lesson_id,
        step["id"],
        code="cubes = [x**3 for x in range(1, 6)]\nprint(cubes)",
    )
    assert result["graded"] is True
    assert result["is_correct"] is True
    assert result["step_completed"] is True
    assert result["test_results"][0]["passed"] is True


async def test_runnable_exercise_rejects_wrong_output(env):
    lesson_id = "python-comprehensions"
    step = step_of(lesson_id, "exercise")

    result = await lesson_service.complete_step(
        "u4", lesson_id, step["id"], code="print(123)"
    )
    assert result["graded"] is True
    assert result["is_correct"] is False
    assert result["step_completed"] is False

    progress = await lesson_service.get_progress("u4")
    assert f"{lesson_id}:{step['id']}" not in progress["completed"]


async def test_unverifiable_exercise_is_practice_not_mastery(env):
    lesson_id = "python-hello"
    step = step_of(lesson_id, "exercise")

    result = await lesson_service.complete_step(
        "u5", lesson_id, step["id"], code='print("Ada")'
    )
    assert result["graded"] is False
    assert result["verified"] is False
    assert result["lesson_verified"] is False
    assert result["xp_earned"] == 0
    assert "practice" in result["feedback"].lower()
    # No skill evidence from an unverifiable submission.
    assert env.evidence == []


async def test_blank_exercise_submission_is_not_attempted(env):
    lesson_id = "python-hello"
    step = step_of(lesson_id, "exercise")

    result = await lesson_service.complete_step("u6", lesson_id, step["id"], code="  ")
    assert result["step_completed"] is False
    progress = await lesson_service.get_progress("u6")
    assert progress["completed"] == {}


# ═════════════════════════════════════════════════════════════════════
# Skill evidence (audit P0: hardcoded category/score/mastery)
# ═════════════════════════════════════════════════════════════════════

async def test_quiz_records_real_category_and_correctness(env):
    lesson_id = "python-hello"
    quiz = step_of(lesson_id, "quiz")

    await lesson_service.complete_step(
        "u7", lesson_id, quiz["id"], answer=str(quiz["correctIndex"])
    )
    assert env.evidence, "verified quiz attempt must record skill evidence"
    record = env.evidence[-1]
    assert record["category"] == "programming"
    assert record["skill"] == "python"
    assert record["is_correct"] is True
    assert record["score"] == 100.0


async def test_wrong_quiz_records_failure_evidence(env):
    lesson_id = "python-hello"
    quiz = step_of(lesson_id, "quiz")
    wrong = "1" if quiz["correctIndex"] != 1 else "0"

    await lesson_service.complete_step(
        "u8", lesson_id, quiz["id"], answer=wrong
    )
    assert env.evidence[-1]["is_correct"] is False
    assert env.evidence[-1]["score"] == 0.0


def test_dsa_lessons_map_to_content_skill():
    assert skill_for_lesson(_LESSONS["dsa-linked-list"]) == ("dsa", "linked_lists")
    assert skill_for_lesson(_LESSONS["dsa-binary-search-tree"]) == ("dsa", "trees")
    assert skill_for_lesson(_LESSONS["dsa-arrays-intro"]) == ("dsa", "arrays")


def test_every_track_maps_to_a_declared_skill():
    from app.services.skill_assessment import SKILL_CATEGORIES

    for lesson in _LESSONS.values():
        target = skill_for_lesson(lesson)
        assert target is not None, f"{lesson['id']} has no skill mapping"
        category, skill = target
        assert skill in SKILL_CATEGORIES[category]["skills"]


def test_weakness_tiers_are_derived_from_mastery():
    assert weakness_tier_for(0.0) == "critical"
    assert weakness_tier_for(0.39) == "critical"
    assert weakness_tier_for(0.40) == "weak"
    assert weakness_tier_for(0.59) == "weak"
    assert weakness_tier_for(0.60) == "on_track"
    assert weakness_tier_for(0.85) == "strong"


async def test_next_action_uses_measured_mastery(env):
    env.mastery.update({"attempts": 4, "score": 30.0, "category_score": 30.0})
    lesson_id = "python-hello"
    quiz = step_of(lesson_id, "quiz")

    result = await lesson_service.complete_step(
        "u9", lesson_id, quiz["id"], answer=str(quiz["correctIndex"])
    )
    action = result["next_action"]
    assert action["mastery"] == 0.3
    assert action["weakness_tier"] == "critical"
    assert action["attempts"] == 4
    assert action["category"] == "programming"
    assert action["skill"] == "python"


async def test_explain_only_lesson_is_unverified(env, monkeypatch):
    """Explain-only content must not produce verified mastery or XP."""
    lesson = {
        "id": "zz-explain-only",
        "title": "Explain only",
        "track": "python",
        "description": "no grading",
        "difficulty": "beginner",
        "xpReward": 40,
        "steps": [{"id": "e1", "type": "explain", "title": "Read", "content": "text"}],
    }
    monkeypatch.setitem(_LESSONS, lesson["id"], lesson)

    result = await lesson_service.complete_step("u10", "zz-explain-only", "e1")
    assert result["lesson_complete"] is True
    assert result["lesson_verified"] is False
    assert result["xp_earned"] == 0
    assert env.evidence == []


def test_new_debugging_system_design_and_behavioral_tracks_are_registered():
    expected = {
        "debugging": {
            "debugging-workflow",
            "debugging-trace-and-edge-cases",
        },
        "system_design": {
            "system-design-requirements",
            "system-design-scalability",
        },
        "behavioral": {
            "behavioral-star-method",
            "behavioral-teamwork-conflict",
        },
    }
    for track, lesson_ids in expected.items():
        actual = {
            lesson_id
            for lesson_id, lesson in _LESSONS.items()
            if lesson.get("track") == track
        }
        assert lesson_ids <= actual
        for lesson_id in lesson_ids:
            assert lesson_service.skill_for_lesson(_LESSONS[lesson_id]) is not None
