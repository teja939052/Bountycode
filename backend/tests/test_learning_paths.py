"""Regression tests for the language-path lesson API (learning routes).

The audit found the language-path lesson endpoint leaked quiz answer keys
(``quiz.correct``) and graded quizzes nowhere, so a lesson could be completed
without passing its quiz. These tests pin the fixed behaviour:

- GET lesson payloads never contain ``correct`` or quiz ``explanation``
- the quiz grade endpoint decides correctness server-side
- the explanation is only revealed after a correct answer
- only a passed quiz is persisted as a pass
- completing a lesson requires every quiz in it to be passed
- the free-trial content endpoint is sanitized the same way
"""
import pytest
from fastapi import HTTPException

from app.data.lesson_content import (
    get_lesson_content,
    lesson_quizzes,
    public_lesson_content,
)
from app.routes import free_trial, learning

LESSON = ("c", "l01", "c-l01-03")  # hand-authored C lesson with a 4-option quiz
USER = {"id": "u-test"}


def _content():
    language_id, level_id, lesson_id = LESSON
    from app.data.curriculum import get_lesson

    lesson = get_lesson(language_id, level_id, lesson_id)
    return get_lesson_content(language_id, lesson_id, lesson["title"], lesson["type"])


# ═════════════════════════════════════════════════════════════════════
# Sanitizer
# ═════════════════════════════════════════════════════════════════════

def test_content_really_has_a_quiz_with_answer_key():
    """Guard the fixture: this test is meaningless if the lesson has no quiz."""
    content = _content()
    quizzes = lesson_quizzes(content)
    assert quizzes, "expected c-l01-03 to carry a quiz"
    assert isinstance(quizzes[0]["correct"], int)


def test_public_content_strips_answer_keys():
    public = public_lesson_content(_content())
    for quiz in lesson_quizzes(public):
        assert "correct" not in quiz
        assert "explanation" not in quiz
        assert quiz["question"]
        assert quiz["options"]


def test_public_content_is_a_deep_copy():
    original = _content()
    public = public_lesson_content(original)
    for quiz in lesson_quizzes(public):
        quiz["options"].append("injected")
    for quiz in lesson_quizzes(original):
        assert "injected" not in quiz["options"]


# ═════════════════════════════════════════════════════════════════════
# GET lesson detail
# ═════════════════════════════════════════════════════════════════════

async def _detail(monkeypatch, passes=()):
    async def unlocked(*args, **kwargs):
        return True

    async def progress(*args, **kwargs):
        return {"completed_lessons": []}

    async def quiz_passes(*args, **kwargs):
        return set(passes)

    monkeypatch.setattr(learning, "is_lesson_unlocked", unlocked)
    monkeypatch.setattr(learning, "get_language_progress", progress)
    monkeypatch.setattr(learning, "get_quiz_passes", quiz_passes)
    return await learning.get_lesson_detail(*LESSON, user=USER)


async def test_lesson_detail_never_leaks_quiz_answers(monkeypatch):
    payload = await _detail(monkeypatch)
    quizzes = lesson_quizzes(payload["content"])
    assert quizzes
    for quiz in quizzes:
        assert "correct" not in quiz
        assert "explanation" not in quiz
    # Also guard against a key leaking anywhere else in the payload.
    assert "'correct'" not in str(payload["content"])


async def test_lesson_detail_reports_quiz_progress(monkeypatch):
    payload = await _detail(monkeypatch)
    required = payload["quiz_progress"]["required"]
    assert required == [f"{LESSON[2]}:0"]
    assert payload["quiz_progress"]["passed"] == []

    payload = await _detail(monkeypatch, passes={f"{LESSON[2]}:0"})
    assert payload["quiz_progress"]["passed"] == [0]


# ═════════════════════════════════════════════════════════════════════
# Quiz grading
# ═════════════════════════════════════════════════════════════════════

async def test_correct_quiz_is_graded_and_recorded(monkeypatch):
    recorded = []

    async def record(user_id, language_id, lesson_id, quiz_index):
        recorded.append((user_id, language_id, lesson_id, quiz_index))

    monkeypatch.setattr(learning, "record_quiz_pass", record)

    quiz = lesson_quizzes(_content())[0]
    result = await learning.grade_lesson_quiz(
        learning.QuizAnswer(quiz_index=0, choice=quiz["correct"]),
        *LESSON,
        user=USER,
    )
    assert result["is_correct"] is True
    assert result["explanation"] == quiz["explanation"]
    assert recorded == [("u-test", "c", LESSON[2], 0)]


async def test_wrong_quiz_is_not_recorded_and_hides_explanation(monkeypatch):
    recorded = []

    async def record(*args, **kwargs):
        recorded.append(args)

    monkeypatch.setattr(learning, "record_quiz_pass", record)

    quiz = lesson_quizzes(_content())[0]
    wrong = next(i for i in range(len(quiz["options"])) if i != quiz["correct"])
    result = await learning.grade_lesson_quiz(
        learning.QuizAnswer(quiz_index=0, choice=wrong),
        *LESSON,
        user=USER,
    )
    assert result["is_correct"] is False
    assert result["explanation"] is None
    assert recorded == []


async def test_quiz_index_out_of_range_is_rejected(monkeypatch):
    with pytest.raises(HTTPException) as exc:
        await learning.grade_lesson_quiz(
            learning.QuizAnswer(quiz_index=9, choice=0), *LESSON, user=USER
        )
    assert exc.value.status_code == 400


# ═════════════════════════════════════════════════════════════════════
# Completion gating
# ═════════════════════════════════════════════════════════════════════

async def _complete(monkeypatch, passes):
    calls = []

    async def unlocked(*args, **kwargs):
        return True

    async def progress(*args, **kwargs):
        return {"completed_lessons": []}

    async def quiz_passes(*args, **kwargs):
        return set(passes)

    async def complete(user_id, language_id, lesson_id, xp):
        calls.append((user_id, language_id, lesson_id, xp))
        return {"xp_gained": xp, "already_completed": False}

    monkeypatch.setattr(learning, "is_lesson_unlocked", unlocked)
    monkeypatch.setattr(learning, "get_language_progress", progress)
    monkeypatch.setattr(learning, "get_quiz_passes", quiz_passes)
    monkeypatch.setattr(learning, "complete_lesson", complete)
    return calls


async def test_completion_requires_passing_the_quiz(monkeypatch):
    calls = await _complete(monkeypatch, passes=set())
    with pytest.raises(HTTPException) as exc:
        await learning.complete_lesson_route(*LESSON, user=USER)
    assert exc.value.status_code == 400
    assert calls == [], "a lesson must not be completed without a quiz pass"


async def test_completion_proceeds_after_quiz_pass(monkeypatch):
    calls = await _complete(monkeypatch, passes={f"{LESSON[2]}:0"})
    result = await learning.complete_lesson_route(*LESSON, user=USER)
    assert result["xp_gained"] > 0
    assert len(calls) == 1


# ═════════════════════════════════════════════════════════════════════
# Free-trial content endpoint (same leak class)
# ═════════════════════════════════════════════════════════════════════

async def test_free_trial_lessons_do_not_leak_quiz_answers():
    payload = await free_trial.get_free_trial_lessons()
    assert payload["lessons"]
    for lesson in payload["lessons"]:
        for quiz in lesson_quizzes(lesson["content"]):
            assert "correct" not in quiz
            assert "explanation" not in quiz
