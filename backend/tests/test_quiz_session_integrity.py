"""Tests for trusted, persistent generic quiz sessions."""
from __future__ import annotations

import pytest
from fastapi import HTTPException
from mongomock_motor import AsyncMongoMockClient

from app.routes import quiz as quiz_routes
from app.services import quiz_service


def _question():
    return {
        "id": "quiz_q_1",
        "title": "Array output",
        "question": "What is the result?",
        "topic": "Arrays & Hashing",
        "sub_topic": "Array Basics",
        "difficulty": "easy",
        "correct_answer": "4",
        "xp_reward": 10,
        "hints": [{"level": 1, "text": "Trace the index."}],
        "solution": {"code": "print(4)", "language": "python"},
        "explanation": "The selected value is 4.",
    }


@pytest.fixture
def quiz_collection(monkeypatch):
    client = AsyncMongoMockClient()
    collection = client["bountycode_test"]["practice_sessions"]
    monkeypatch.setattr(quiz_routes, "practice_sessions_collection", collection)
    return collection


def test_company_or_topic_filters_never_fall_back_to_global_questions(monkeypatch):
    monkeypatch.setattr(quiz_service, "_load_questions", lambda: [_question()])

    result = quiz_service.build_quiz(
        mode="quiz",
        topics=["topic-that-does-not-exist"],
        num_questions=5,
    )

    assert result["questions"] == []
    assert result["total_questions"] == 0
    assert result["empty_reason"]


def test_practice_quiz_does_not_reveal_hints_or_solution_before_answer(monkeypatch):
    monkeypatch.setattr(quiz_service, "_load_questions", lambda: [_question()])

    result = quiz_service.build_quiz(mode="practice", num_questions=1)
    served = result["questions"][0]

    assert served["id"] == "quiz_q_1"
    assert served["hint_count"] == 1
    assert "hints" not in served
    assert "solution" not in served
    assert "explanation" not in served
    assert "correct_answer" not in served


def test_code_question_without_answer_key_cannot_be_self_graded(monkeypatch):
    question = {
        "id": "code_q_1",
        "type": "coding",
        "topic": "Arrays & Hashing",
        "question": "Implement a function.",
        "solution": {"code": "def solve(): return 1"},
    }
    monkeypatch.setattr(quiz_service, "get_question_by_id", lambda _qid: question)

    result = quiz_service.submit_quiz_answer(
        quiz_id="quiz_1",
        question_id="code_q_1",
        user_answer="solved",
        time_taken_seconds=20,
    )

    assert result["is_correct"] is False
    assert result["requires_code_execution"] is True
    assert result["xp_earned"] == 0


@pytest.mark.asyncio
async def test_quiz_answers_and_results_are_owned_and_server_backed(monkeypatch, quiz_collection):
    question = _question()
    served_quiz = {
        "quiz_id": "quiz_session_1",
        "mode": "practice",
        "total_questions": 1,
        "time_limit_seconds": 120,
        "questions": [{"id": question["id"], "title": question["title"], "index": 0}],
        "filters": {"topics": [question["topic"]], "difficulty": "easy", "company": None},
    }
    monkeypatch.setattr(quiz_routes, "build_quiz", lambda **_kwargs: served_quiz)
    monkeypatch.setattr(quiz_routes, "get_question_by_id", lambda _qid: question)
    monkeypatch.setattr(quiz_service, "get_question_by_id", lambda _qid: question)

    async def fake_record_activity(_user_id, _activity):
        return {"status": "success"}

    async def fake_record_practice(**_kwargs):
        return {"xp_gained": 12}

    monkeypatch.setattr(quiz_routes, "record_learning_activity", fake_record_activity)
    monkeypatch.setattr(quiz_routes, "record_practice", fake_record_practice)

    built = await quiz_routes.build_quiz_session(
        quiz_routes.QuizRequest(mode="practice", topics=[question["topic"]], num_questions=1),
        user={"id": "user-a", "level": 1, "role": "sde"},
    )
    assert built["quiz"]["quiz_id"] == "quiz_session_1"

    with pytest.raises(HTTPException) as not_owner:
        await quiz_routes.submit_answer(
            quiz_routes.AnswerSubmission(
                quiz_id="quiz_session_1",
                question_id=question["id"],
                user_answer="4",
                time_taken_seconds=12,
            ),
            user={"id": "user-b"},
        )
    assert not_owner.value.status_code == 404

    answer = await quiz_routes.submit_answer(
        quiz_routes.AnswerSubmission(
            quiz_id="quiz_session_1",
            question_id=question["id"],
            user_answer="4",
            time_taken_seconds=12,
        ),
        user={"id": "user-a", "role": "sde"},
    )
    assert answer["result"]["is_correct"] is True
    assert answer["result"]["xp_earned"] == 12

    with pytest.raises(HTTPException) as duplicate:
        await quiz_routes.submit_answer(
            quiz_routes.AnswerSubmission(
                quiz_id="quiz_session_1",
                question_id=question["id"],
                user_answer="4",
                time_taken_seconds=12,
            ),
            user={"id": "user-a"},
        )
    assert duplicate.value.status_code == 409

    # Forged client answers are ignored; the result uses the stored server grade.
    results = await quiz_routes.quiz_results(
        quiz_routes.QuizResultsRequest(
            quiz_id="quiz_session_1",
            questions=[{"id": "forged", "topic": "Wrong topic"}],
            answers=[{"is_correct": False}],
            total_time_seconds=12,
        ),
        user={"id": "user-a"},
    )
    assert results["results"]["total_questions"] == 1
    assert results["results"]["correct"] == 1
    assert results["results"]["score_percentage"] == 100.0

    stored = await quiz_collection.find_one({"quiz_id": "quiz_session_1"})
    assert stored["status"] == "completed"
    assert stored["answers"][0]["is_correct"] is True



def test_multiple_choice_answers_are_graded_by_server_answer_key(monkeypatch):
    question = {
        "id": "mcq_1",
        "options": ["10", "20", "30", "40"],
        "correct_index": 2,
        "explanation": "The correct choice is 30.",
        "xp_reward": 10,
    }
    monkeypatch.setattr(quiz_service, "get_question_by_id", lambda _qid: question)

    result = quiz_service.submit_quiz_answer(
        quiz_id="quiz_mcq",
        question_id="mcq_1",
        user_answer="2",
        time_taken_seconds=5,
    )

    assert result["is_correct"] is True
    assert result["correct_answer"] == "30"
    assert result["explanation"] == "The correct choice is 30."


@pytest.mark.asyncio
async def test_hints_are_owned_and_consumed_in_sequence(monkeypatch, quiz_collection):
    await quiz_collection.insert_one({
        "user_id": "user-a",
        "session_type": "quiz",
        "quiz_id": "quiz_hint",
        "question_ids": ["quiz_q_1"],
        "answers": [],
        "hint_counts": {},
        "status": "in_progress",
    })

    def fake_hint(question_id, hint_level, hints_already_used):
        return {
            "hint": {"level": hint_level, "text": f"Hint {hint_level}"},
            "hint_level": hint_level,
            "hints_used": hints_already_used + 1,
        }

    monkeypatch.setattr(quiz_routes, "get_hint_for_question", fake_hint)
    request = quiz_routes.HintRequest(
        question_id="quiz_q_1",
        quiz_id="quiz_hint",
        hint_level=1,
        hints_already_used=0,
    )
    first = await quiz_routes.get_hint(request, user={"id": "user-a"})
    assert first["hint"]["text"] == "Hint 1"

    with pytest.raises(HTTPException) as repeated:
        await quiz_routes.get_hint(request, user={"id": "user-a"})
    assert repeated.value.status_code == 409

    second = await quiz_routes.get_hint(
        quiz_routes.HintRequest(
            question_id="quiz_q_1",
            quiz_id="quiz_hint",
            hint_level=2,
            hints_already_used=0,  # Client value is ignored.
        ),
        user={"id": "user-a"},
    )
    assert second["hint"]["text"] == "Hint 2"

    with pytest.raises(HTTPException) as not_owner:
        await quiz_routes.get_hint(request, user={"id": "user-b"})
    assert not_owner.value.status_code == 404
