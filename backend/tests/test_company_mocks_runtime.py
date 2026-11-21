"""Focused tests for the company-mock coding session contract.

These tests mock persistence and the code judge so they are deterministic and
do not require MongoDB, Piston or an external service.
"""
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from bson import ObjectId
from fastapi import HTTPException

from app.routes import company_mocks as route


class _Collection:
    def __init__(self, session):
        self.session = session
        self.updated = None

    async def find_one(self, query):
        if query.get("_id") != self.session.get("_id"):
            return None
        if query.get("user_id") != self.session.get("user_id"):
            return None
        return self.session

    async def update_one(self, query, update):
        if query.get("user_id") != self.session.get("user_id"):
            return SimpleNamespace(modified_count=0)
        if query.get("status") and query["status"] != self.session.get("status"):
            return SimpleNamespace(modified_count=0)
        ne = query.get("answers.question_id", {}).get("$ne")
        if ne and any(a.get("question_id") == ne for a in self.session.get("answers", [])):
            return SimpleNamespace(modified_count=0)
        if "$push" in update:
            for key, value in update["$push"].items():
                self.session.setdefault(key, []).append(value)
        if "$inc" in update:
            for key, value in update["$inc"].items():
                self.session[key] = self.session.get(key, 0) + value
        if "$set" in update:
            self.session.update(update["$set"])
        return SimpleNamespace(modified_count=1)


class _DB:
    def __init__(self, collection):
        self.collection = collection

    def __getitem__(self, name):
        assert name == "company_mock_tests"
        return self.collection


@pytest.mark.asyncio
async def test_answer_is_graded_server_side_and_persisted(monkeypatch):
    session_id = str(ObjectId())
    question = {"id": "q-1", "round": "Online Assessment"}
    session = {
        "_id": ObjectId(session_id),
        "user_id": "user-1",
        "company": "google",
        "status": "in_progress",
        "ends_at": datetime.now(timezone.utc) + timedelta(minutes=20),
        "questions": [question],
        "answers": [],
    }
    collection = _Collection(session)
    monkeypatch.setattr(route, "get_db", lambda: _DB(collection))

    from app.services import question_store
    monkeypatch.setattr(
        question_store,
        "get_question_for_serving",
        lambda qid: {
            "id": qid,
            "topic": "arrays",
            "hidden_test_cases": [{"input": "2", "expected": "4"}],
        },
    )

    class _Judge:
        async def execute_against_test_cases(self, **kwargs):
            assert kwargs["test_cases"] == [
                {"input": "2", "expected": "4", "is_hidden": True}
            ]
            return {
                "success": True,
                "all_passed": True,
                "passed_count": 1,
                "total_count": 1,
                "score": 100,
                "summary": "1/1 passed",
            }

    monkeypatch.setattr(route, "CodeExecutionEngine", _Judge)
    monkeypatch.setattr(route, "get_current_user", lambda: {"id": "user-1"})

    result = await route.submit_company_mock_answer(
        session_id,
        {"question_id": "q-1", "code": "print(2 * 2)", "language": "python"},
        {"id": "user-1"},
    )
    assert result["is_correct"] is True
    assert result["score"] == 100
    assert session["answers"][0]["question_id"] == "q-1"
    assert session["total_score"] == 100


@pytest.mark.asyncio
async def test_answer_rejects_duplicate_question_submission(monkeypatch):
    session_id = str(ObjectId())
    session = {
        "_id": ObjectId(session_id),
        "user_id": "user-1",
        "status": "in_progress",
        "ends_at": datetime.now(timezone.utc) + timedelta(minutes=20),
        "questions": [{"id": "q-1"}],
        "answers": [{"question_id": "q-1"}],
    }
    monkeypatch.setattr(route, "get_db", lambda: _DB(_Collection(session)))

    with pytest.raises(HTTPException) as exc:
        await route.submit_company_mock_answer(
            session_id,
            {"question_id": "q-1", "code": "print(1)"},
            {"id": "user-1"},
        )
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_answer_enforces_user_ownership(monkeypatch):
    session_id = str(ObjectId())
    session = {
        "_id": ObjectId(session_id),
        "user_id": "owner",
        "status": "in_progress",
        "ends_at": datetime.now(timezone.utc) + timedelta(minutes=20),
        "questions": [{"id": "q-1"}],
        "answers": [],
    }
    monkeypatch.setattr(route, "get_db", lambda: _DB(_Collection(session)))

    with pytest.raises(HTTPException) as exc:
        await route.submit_company_mock_answer(
            session_id,
            {"question_id": "q-1", "code": "print(1)"},
            {"id": "intruder"},
        )
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_complete_is_idempotent_and_freezes_session(monkeypatch):
    session_id = str(ObjectId())
    session = {
        "_id": ObjectId(session_id),
        "user_id": "user-1",
        "company": "google",
        "status": "in_progress",
        "ends_at": datetime.now(timezone.utc) + timedelta(minutes=20),
        "questions": [],
        "answers": [],
        "total_score": 0,
        "config": {"passing_score": 70, "interview_tips": []},
    }
    collection = _Collection(session)
    monkeypatch.setattr(route, "get_db", lambda: _DB(collection))

    result = await route.complete_company_mock(session_id, {"id": "user-1"})
    assert result["session_id"] == session_id
    assert session["status"] == "completed"
    assert result["completed_at"]

    again = await route.complete_company_mock(session_id, {"id": "user-1"})
    assert again["session_id"] == session_id
    assert session["status"] == "completed"


@pytest.mark.asyncio
async def test_results_endpoint_handles_null_completed_at(monkeypatch):
    session_id = str(ObjectId())
    session = {
        "_id": ObjectId(session_id),
        "user_id": "user-1",
        "company": "google",
        "status": "in_progress",
        "questions": [],
        "answers": [],
        "total_score": 0,
        "config": {"passing_score": 70, "interview_tips": []},
        "completed_at": None,
    }
    monkeypatch.setattr(route, "get_db", lambda: _DB(_Collection(session)))
    result = await route.get_mock_results(session_id, {"id": "user-1"})
    assert result["session_id"] == session_id
    assert result["completed_at"]


def test_round_materialization_is_explicitly_coding_only():
    # Company configuration may advertise multiple interview rounds. The
    # start route intentionally reports non-coding round names separately.
    google = route.COMPANY_MOCK_CONFIGS["google"]
    non_coding = [
        item["name"] for item in google["rounds"]
        if item.get("type") != "coding"
    ]
    assert "System Design" in non_coding
    assert "Behavioral" in non_coding
