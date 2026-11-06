"""Regression tests for the service-company learning loop.

These tests cover lesson discovery, answer-key privacy, server-side assessment
grading, and the hand-off from a passed lesson to company-track mastery.
"""
from __future__ import annotations

import os

import pytest
from fastapi import HTTPException

from app.routes import company_lessons


async def _fake_record_learning_activity(_user_id, _activity):
    return {"status": "success"}


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
    assert "correct_index" not in result["data"]["steps"][0]
    assert "explanation" not in result["data"]["steps"][0]


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
async def test_failed_assessment_records_attempt_without_mastery(monkeypatch):
    lesson = _lesson()
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    _seed_passed_required_steps(fake_learning_progress, lesson)
    monkeypatch.setattr(company_lessons, "record_learning_activity", _fake_record_learning_activity)
    calls = []

    async def fake_record_topic_mastery(**kwargs):
        calls.append(kwargs)
        return {"module_completed": False, "topic_mastered": False, "xp_earned": 0}

    monkeypatch.setattr(
        company_lessons, "record_track_topic_mastery", fake_record_topic_mastery
    )

    request = company_lessons.CompleteRequest(
        answers={"0": 1, "1": 1},  # one of two correct: 50%
        track_id="tcs_nqt",
        module_id="tcs_f1",
        topic_id="percentages",
    )
    result = await company_lessons.complete_lesson(
        "successive_percentage_change", request, user={"id": "test-user"}
    )

    assert result["data"]["passed"] is False
    assert result["data"]["score"] == 50.0
    assert result["data"]["xp_earned"] == 0
    assert result["data"]["module_completed"] is False
    assert len(calls) == 1
    assert calls[0]["score"] == 50.0


@pytest.mark.asyncio
async def test_passed_assessment_records_company_module_mastery(monkeypatch):
    lesson = _lesson()
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    _seed_passed_required_steps(fake_learning_progress, lesson)
    monkeypatch.setattr(company_lessons, "record_learning_activity", _fake_record_learning_activity)
    calls = []

    async def fake_complete_track_module(**kwargs):
        calls.append(kwargs)
        return {"success": True, "module_completed": False, "topic_mastered": True, "topic_id": "percentages", "xp_earned": 0}

    monkeypatch.setattr(
        company_lessons, "record_track_topic_mastery", fake_complete_track_module
    )

    request = company_lessons.CompleteRequest(
        answers={"0": 1, "1": 2},
        track_id="tcs_nqt",
        module_id="tcs_f1",
        topic_id="percentages",
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


@pytest.mark.asyncio
async def test_step_answer_is_server_graded_and_records_evidence(monkeypatch):
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: _lesson())
    recorded = []

    async def fake_record_learning_activity(user_id, activity):
        recorded.append((user_id, activity))
        return {"status": "success"}

    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    result = await company_lessons.answer_lesson_step(
        "successive_percentage_change",
        0,
        company_lessons.StepAnswerRequest(answer_index=0),
        user={"id": "test-user"},
    )

    assert result["data"]["correct"] is True
    assert result["data"]["correct_index"] == 0
    assert len(recorded) == 1
    assert recorded[0][0] == "test-user"
    assert recorded[0][1]["success"] is True
    stored = fake_learning_progress.document["lesson_progress"]["successive_percentage_change"]["step_evidence"]["0"]
    assert stored["passed"] is True
    assert stored["attempts"] == 1
    assert stored["fingerprint"] == company_lessons._step_fingerprint(_lesson()["steps"][0])


@pytest.mark.asyncio
async def test_step_answer_rejects_out_of_range_choice(monkeypatch):
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: _lesson())
    request = company_lessons.StepAnswerRequest(answer_index=4)

    with pytest.raises(HTTPException) as exc:
        await company_lessons.answer_lesson_step(
            "successive_percentage_change", 0, request, user={"id": "test-user"}
        )

    assert exc.value.status_code == 422



class _FakeLearningProgressCollection:
    def __init__(self):
        self.document = {}

    async def find_one(self, query):
        if self.document.get("user_id") == query.get("user_id"):
            return self.document
        return None

    async def update_one(self, query, update, upsert=False):
        if not self.document:
            self.document = {"user_id": query["user_id"], "activities": []}
        for operator in ("$set", "$inc"):
            for dotted_key, value in update.get(operator, {}).items():
                cursor = self.document
                parts = dotted_key.split(".")
                for part in parts[:-1]:
                    cursor = cursor.setdefault(part, {})
                if operator == "$inc":
                    cursor[parts[-1]] = cursor.get(parts[-1], 0) + value
                else:
                    cursor[parts[-1]] = value


@pytest.fixture(autouse=True)
def fake_learning_progress(monkeypatch):
    collection = _FakeLearningProgressCollection()
    monkeypatch.setattr(company_lessons, "learning_progress_collection", collection)
    return collection


def _seed_passed_required_steps(collection, lesson, user_id="test-user"):
    evidence = {}
    for index in company_lessons._required_step_indices(lesson):
        step = lesson["steps"][index]
        evidence[str(index)] = {
            "attempts": 1,
            "passed": True,
            "passed_at": "2026-11-06T00:00:00+00:00",
            "fingerprint": company_lessons._step_fingerprint(step),
        }
    collection.document = {
        "user_id": user_id,
        "lesson_progress": {lesson["slug"]: {"step_evidence": evidence}},
    }


@pytest.mark.asyncio
async def test_final_assessment_cannot_skip_required_interactive_step(monkeypatch):
    lesson = _lesson()
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    request = company_lessons.CompleteRequest(answers={"0": 1, "1": 2})

    with pytest.raises(HTTPException) as exc:
        await company_lessons.complete_lesson(
            lesson["slug"], request, user={"id": "test-user"}
        )

    assert exc.value.status_code == 409
    assert exc.value.detail["missing_steps"] == [
        {"step_index": 0, "step_number": 1, "title": "Warm-up"}
    ]


@pytest.mark.asyncio
async def test_saved_resume_position_does_not_satisfy_lesson_evidence_gate(monkeypatch):
    lesson = _lesson()
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    await company_lessons.save_lesson_progress(
        lesson["slug"],
        company_lessons.LessonProgressRequest(current_step=0),
        user={"id": "test-user"},
    )

    request = company_lessons.CompleteRequest(answers={"0": 1, "1": 2})
    with pytest.raises(HTTPException) as exc:
        await company_lessons.complete_lesson(
            lesson["slug"], request, user={"id": "test-user"}
        )

    assert exc.value.status_code == 409
    assert "step_evidence" not in fake_learning_progress.document["lesson_progress"][lesson["slug"]]


@pytest.mark.asyncio
async def test_old_step_pass_is_invalidated_when_authored_content_changes(monkeypatch):
    lesson = _lesson()
    _seed_passed_required_steps(fake_learning_progress, lesson)
    lesson["steps"][0]["prompt"] = "A materially revised prompt."
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)

    request = company_lessons.CompleteRequest(answers={"0": 1, "1": 2})
    with pytest.raises(HTTPException) as exc:
        await company_lessons.complete_lesson(
            lesson["slug"], request, user={"id": "test-user"}
        )

    assert exc.value.status_code == 409
    assert exc.value.detail["missing_steps"][0]["step_index"] == 0


@pytest.mark.asyncio
async def test_evidence_store_failure_blocks_step_success_response(monkeypatch):
    lesson = _lesson()
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)

    class FailingCollection:
        async def update_one(self, *_args, **_kwargs):
            raise RuntimeError("database unavailable")

    monkeypatch.setattr(company_lessons, "learning_progress_collection", FailingCollection())
    recorded = []

    async def fake_record_learning_activity(user_id, activity):
        recorded.append(activity)

    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    with pytest.raises(HTTPException) as exc:
        await company_lessons.answer_lesson_step(
            lesson["slug"], 0, company_lessons.StepAnswerRequest(answer_index=0),
            user={"id": "test-user"},
        )

    assert exc.value.status_code == 503
    assert recorded == []


@pytest.mark.asyncio
async def test_lesson_progress_can_be_saved_and_resumed(monkeypatch):
    lesson = _lesson()
    lesson["steps"].append({
        "step_number": 2,
        "step_type": "explain",
        "title": "Continue learning",
        "content": "A second step.",
    })
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    collection = _FakeLearningProgressCollection()
    monkeypatch.setattr(company_lessons, "learning_progress_collection", collection)

    saved = await company_lessons.save_lesson_progress(
        "successive_percentage_change",
        company_lessons.LessonProgressRequest(current_step=1),
        user={"id": "test-user"},
    )
    restored = await company_lessons.get_lesson_progress(
        "successive_percentage_change",
        user={"id": "test-user"},
    )

    assert saved["data"]["current_step"] == 1
    assert restored["data"]["current_step"] == 1
    assert restored["data"]["has_progress"] is True
    assert collection.document["lesson_progress"]["successive_percentage_change"]["current_step"] == 1


@pytest.mark.asyncio
async def test_lesson_progress_rejects_a_step_outside_the_lesson(monkeypatch):
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: _lesson())
    collection = _FakeLearningProgressCollection()
    monkeypatch.setattr(company_lessons, "learning_progress_collection", collection)

    with pytest.raises(HTTPException) as exc:
        await company_lessons.save_lesson_progress(
            "successive_percentage_change",
            company_lessons.LessonProgressRequest(current_step=1),
            user={"id": "test-user"},
        )

    assert exc.value.status_code == 422
    assert collection.document == {}



@pytest.mark.asyncio
async def test_typed_code_trace_answer_is_server_graded_and_key_stays_private(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1,
        "step_type": "predict_output",
        "title": "Predict the output",
        "prompt": "What does this program print?",
        "code": "total = 1 + 2\nprint(total)",
        "expected_answer": "3",
        "accepted_answers": ["3", "03"],
        "explanation": "The expression evaluates to 3 before print runs.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    recorded = []

    async def fake_record_learning_activity(user_id, activity):
        recorded.append((user_id, activity))
        return {"status": "success"}

    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    public = await company_lessons.get_lesson(
        "successive_percentage_change", user={"id": "test-user"}
    )
    result = await company_lessons.answer_lesson_step(
        "successive_percentage_change",
        0,
        company_lessons.StepAnswerRequest(answer_text="  03  "),
        user={"id": "test-user"},
    )

    public_step = public["data"]["steps"][0]
    assert "expected_answer" not in public_step
    assert "accepted_answers" not in public_step
    assert "explanation" not in public_step
    assert public_step["code"] == "total = 1 + 2\nprint(total)"
    assert result["data"]["correct"] is True
    assert result["data"]["correct_answer"] == "3"
    assert result["data"]["correct_index"] is None
    assert recorded[0][1]["success"] is True


@pytest.mark.asyncio
async def test_typed_code_trace_wrong_answer_records_learning_evidence(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1,
        "step_type": "predict_output",
        "title": "Predict the output",
        "prompt": "What does this program print?",
        "code": "print('Hello')",
        "expected_answer": "Hello",
        "explanation": "The print call outputs the string Hello.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    recorded = []

    async def fake_record_learning_activity(user_id, activity):
        recorded.append(activity)
        return {"status": "success"}

    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    result = await company_lessons.answer_lesson_step(
        "successive_percentage_change",
        0,
        company_lessons.StepAnswerRequest(answer_text="Goodbye"),
        user={"id": "test-user"},
    )

    assert result["data"]["correct"] is False
    assert result["data"]["correct_answer"] == "Hello"
    assert recorded[0]["success"] is False



@pytest.mark.asyncio
async def test_order_steps_are_graded_server_side_and_answer_key_is_private(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1,
        "step_type": "order_steps",
        "title": "Order the process",
        "prompt": "Arrange the operations.",
        "options": ["Run body", "Initialize", "Check condition"],
        "correct_order": [1, 2, 0],
        "explanation": "Initialize, check, then run the body.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    recorded = []

    async def fake_record_learning_activity(user_id, activity):
        recorded.append((user_id, activity))
        return {"status": "success"}

    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    public = await company_lessons.get_lesson(
        "successive_percentage_change", user={"id": "test-user"}
    )
    assert "correct_order" not in public["data"]["steps"][0]

    result = await company_lessons.answer_lesson_step(
        "successive_percentage_change",
        0,
        company_lessons.StepAnswerRequest(answer_order=[1, 2, 0]),
        user={"id": "test-user"},
    )
    assert result["data"]["correct"] is True
    assert result["data"]["correct_order"] == [1, 2, 0]
    assert recorded[0][1]["success"] is True


@pytest.mark.asyncio
async def test_order_steps_rejects_duplicate_positions(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1,
        "step_type": "order_steps",
        "title": "Order the process",
        "prompt": "Arrange the operations.",
        "options": ["Run body", "Initialize", "Check condition"],
        "correct_order": [1, 2, 0],
        "explanation": "Initialize, check, then run the body.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)

    with pytest.raises(HTTPException) as exc:
        await company_lessons.answer_lesson_step(
            "successive_percentage_change",
            0,
            company_lessons.StepAnswerRequest(answer_order=[1, 1, 0]),
            user={"id": "test-user"},
        )

    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_code_lab_expected_output_is_private_until_submission(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1, "step_type": "code_lab", "title": "Run a code exercise",
        "prompt": "Print the required output.", "language": "javascript",
        "starter_code": "console.log('done')", "expected_output": "done",
        "explanation": "The output is produced by console.log.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    public = await company_lessons.get_lesson("successive_percentage_change", user={"id": "test-user"})
    assert "expected_output" not in public["data"]["steps"][0]
    assert "explanation" not in public["data"]["steps"][0]


@pytest.mark.asyncio
async def test_code_lab_output_is_formative_only_without_mastery_evidence(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1, "step_type": "code_lab", "title": "Run a code exercise",
        "expected_output": "42", "explanation": "The sum is 42.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    recorded = []
    async def fake_record_learning_activity(user_id, activity):
        recorded.append(activity)
        return {"status": "success"}
    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    result = await company_lessons.answer_lesson_step(
        "successive_percentage_change", 0,
        company_lessons.StepAnswerRequest(answer_text="42"),
        user={"id": "test-user"},
    )
    assert result["data"]["correct"] is True
    assert result["data"]["correct_answer"] is None
    assert "42" not in str(result["data"].get("feedback"))
    assert result["data"]["evidence_recorded"] is False
    assert result["data"]["formative_only"] is True
    assert recorded == []


@pytest.mark.asyncio
async def test_sql_lab_hides_grading_data_and_grades_query(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1, "step_type": "sql_lab", "title": "Select assigned employees",
        "prompt": "Return names and department names.",
        "schema_preview": "employees(id, name, department_id)", "sample_data": "1 | Asha | 10",
        "schema_ddl": "CREATE TABLE employees(id INTEGER, name TEXT, department_id INTEGER); CREATE TABLE departments(id INTEGER, name TEXT);",
        "seed_inserts": "INSERT INTO employees VALUES (1, 'Asha', 10); INSERT INTO departments VALUES (10, 'Sales');",
        "expected_query": "SELECT e.name, d.name FROM employees e JOIN departments d ON e.department_id = d.id;",
        "explanation": "Join the matching department id.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    recorded = []
    async def fake_record_learning_activity(user_id, activity):
        recorded.append(activity)
        return {"status": "success"}
    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    public = await company_lessons.get_lesson("successive_percentage_change", user={"id": "test-user"})
    public_step = public["data"]["steps"][0]
    for secret in ("schema_ddl", "seed_inserts", "expected_query"):
        assert secret not in public_step

    result = await company_lessons.answer_lesson_step(
        "successive_percentage_change", 0,
        company_lessons.StepAnswerRequest(answer_text="SELECT e.name, d.name FROM employees e JOIN departments d ON e.department_id = d.id;"),
        user={"id": "test-user"},
    )
    assert result["data"]["correct"] is True
    assert result["data"]["evidence_recorded"] is True
    assert recorded[0]["success"] is True



@pytest.mark.asyncio
async def test_debug_choice_hides_diagnostic_key_and_returns_selected_misconception_feedback(monkeypatch):
    lesson = _lesson()
    lesson["steps"][0] = {
        "step_number": 1,
        "step_type": "debug_choice",
        "title": "Find the loop bug",
        "prompt": "Why does this loop skip the first number?",
        "code": "for i in range(1, len(values)): print(values[i])",
        "options": ["It starts at index 1", "print is inside the loop", "range includes the stop value"],
        "correct_index": 0,
        "feedback_by_option": {
            "1": "Printing inside the loop is expected here; the starting index is the actual issue.",
            "2": "range stops before its upper bound. The first value is skipped because the start is 1.",
        },
        "explanation": "Start at index zero to visit every element.",
    }
    monkeypatch.setattr(company_lessons, "_load_lesson", lambda _slug: lesson)
    recorded = []

    async def fake_record_learning_activity(user_id, activity):
        recorded.append(activity)
        return {"status": "success"}

    monkeypatch.setattr(company_lessons, "record_learning_activity", fake_record_learning_activity)

    public = await company_lessons.get_lesson("successive_percentage_change", user={"id": "test-user"})
    public_step = public["data"]["steps"][0]
    assert "correct_index" not in public_step
    assert "feedback_by_option" not in public_step
    assert "explanation" not in public_step

    result = await company_lessons.answer_lesson_step(
        "successive_percentage_change",
        0,
        company_lessons.StepAnswerRequest(answer_index=1),
        user={"id": "test-user"},
    )
    assert result["data"]["correct"] is False
    assert "starting index" in result["data"]["feedback"]
    assert recorded[0]["success"] is False
