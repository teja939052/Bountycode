"""Regression tests for the service-company learning loop.

These tests cover lesson discovery, answer-key privacy, server-side assessment
grading, and the hand-off from a passed lesson to company-track mastery.
"""
from __future__ import annotations

import os

import pytest
from fastapi import HTTPException

from app.routes import company_lessons


def _lesson():
    return {
        "id": "lesson_test_001",
        "slug": "successive_percentage_change",
        "title": "Test lesson",
        "domain": "Reasoning",
        "difficulty": "easy",
        "duration_min": 10,
        "xp_reward": 50,
        "mastery_threshold": 0.7,
        "steps": [
            {
                "step_number": 1,
                "step_type": "interactive",
                "title": "Warm-up",
                "prompt": "Select the correct answer.",
                "options": ["A", "B"],
                "correct_index": 0,
                "explanation": "A is correct.",
            }
        ],
        "assessment": {
            "mastery_threshold": 0.7,
            "questions": [
                {
                    "prompt": "Question one?",
                    "options": ["A", "B", "C", "D"],
                    "correct_index": 1,
                    "explanation": "The second option is correct.",
                },
                {
                    "prompt": "Question two?",
                    "options": ["A", "B", "C", "D"],
                    "correct_index": 2,
                    "explanation": "The third option is correct.",
                },
            ],
        },
    }


@pytest.mark.asyncio
async def test_company_lesson_catalog_points_at_authored_lesson_files():
    assert os.path.isdir(company_lessons._LESSONS_DIR)

    result = await company_lessons.list_lessons(user={"id": "test-user"})
    slugs = {item["slug"] for item in result["data"]}

    assert {
        "arrays_basics",
        "blood_relations",
        "flowchart_basics",
        "reading_comprehension",
        "successive_percentage_change",
    }.issubset(slugs)
    # This file is a pattern-bank payload, not a step-based LessonPlayer lesson.
    assert "sliding_window" not in slugs


@pytest.mark.asyncio
async def test_final_assessment_answer_key_is_not_sent_to_client(monkeypatch):
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: _lesson())

    result = await company_lessons.get_lesson(
        "successive_percentage_change", user={"id": "test-user"}
    )

    question = result["data"]["assessment"]["questions"][0]
    assert "correct_index" not in question
    assert "correct_answer" not in question
    assert result["data"]["steps"][0]["correct_index"] == 0


@pytest.mark.asyncio
async def test_client_supplied_score_cannot_complete_a_lesson(monkeypatch):
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: _lesson())

    # Legacy clients may still send a score, but score is not an accepted
    # completion signal. With no server-graded answers the request is rejected.
    request = company_lessons.CompleteRequest(**{"score": 100})
    with pytest.raises(HTTPException) as exc:
        await company_lessons.complete_lesson(
            "successive_percentage_change", request, user={"id": "test-user"}
        )

    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_failed_assessment_does_not_complete_company_module(monkeypatch):
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: _lesson())
    called = False

    async def fake_complete_track_module(**_kwargs):
        nonlocal called
        called = True
        return {"passed": True, "xp_earned": 50}

    monkeypatch.setattr(
        company_lessons, "record_track_topic_mastery", fake_complete_track_module
    )

    request = company_lessons.CompleteRequest(
        answers={"0": 1, "1": 1},  # one of two correct: 50%
        track_id="tcs_nqt",
        module_id="tcs_f1",
    )
    result = await company_lessons.complete_lesson(
        "successive_percentage_change", request, user={"id": "test-user"}
    )

    assert result["data"]["passed"] is False
    assert result["data"]["score"] == 50.0
    assert result["data"]["xp_earned"] == 0
    assert called is False


@pytest.mark.asyncio
async def test_passed_assessment_records_company_module_mastery(monkeypatch):
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: _lesson())
    calls = []

    async def fake_complete_track_module(**kwargs):
        calls.append(kwargs)
        return {"success": True, "passed": True, "xp_earned": 50}

    monkeypatch.setattr(
        company_lessons, "complete_track_module", fake_complete_track_module
    )

    request = company_lessons.CompleteRequest(
        answers={"0": 1, "1": 2},
        track_id="tcs_nqt",
        module_id="tcs_f1",
        time_spent_seconds=90,
    )
    result = await company_lessons.complete_lesson(
        "successive_percentage_change", request, user={"id": "test-user", "target_role": "SDE"}
    )

    assert result["data"]["passed"] is True
    assert result["data"]["module_completed"] is False
    assert result["data"]["xp_earned"] == 0
    assert len(calls) == 1
    assert calls[0]["track_id"] == "tcs_nqt"
    assert calls[0]["module_id"] == "tcs_f1"
    assert calls[0]["score"] == 100.0
    assert calls[0]["topic_id"] == "percentages"
