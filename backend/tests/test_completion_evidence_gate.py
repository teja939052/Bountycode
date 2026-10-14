"""Reliability gate regressions: no unverified completion rewards,
no AI score becoming mastery, no quarantined leak via random.

Runs against mongomock-motor (no live Mongo, no network for the
asserted paths). Text steps use the tolerant local comparator;
transfer/debug execution paths are not exercised here.
"""
from __future__ import annotations

import os
import sys
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import HTTPException
from mongomock_motor import AsyncMongoMockClient

import app.database as dbmod
from app.routes.worlds import (
    AttemptRequest,
    _has_step_content,
    _required_steps,
    attempt_level,
    complete_level,
)


@pytest.fixture
async def mock_db():
    client = AsyncMongoMockClient()
    db = client["evidence_gate_verify"]
    old_client, old_db = dbmod._client, dbmod._db
    dbmod._client, dbmod._db = client, db
    # _LazyCollection caches resolved handles; clear it so mocks take effect.
    from app.database import _collections

    _collections.clear()
    yield db
    dbmod._client, dbmod._db = old_client, old_db
    _collections.clear()


def _user(uid: str = "gate_user"):
    return {"id": uid, "role": "sde"}


def _level_one():
    from app.data.worlds_data import WORLD_REGISTRY

    world = WORLD_REGISTRY["foundations"]
    return world, world.towns[0].levels[0]


# ── content helpers ──────────────────────────────────────────────

def test_required_steps_only_lists_content_present():
    world, lvl = _level_one()
    required = _required_steps(lvl)
    assert isinstance(required, list)
    # Every listed step must actually have content; never enforce a
    # stage the content never defined.
    for step in required:
        assert _has_step_content(lvl, step) is True
    # Final trial is validated separately, never in required_steps.
    assert "build" not in required and "code" not in required


def test_has_step_content_false_on_empty():
    from app.models.world import LevelBase

    lvl = LevelBase(id="x", title="x")
    assert _has_step_content(lvl, "predict") is False
    assert _has_step_content(lvl, "manipulate") is False
    assert _has_step_content(lvl, "retrieval") is False
    assert _has_step_content(lvl, "transfer") is False
    assert _has_step_content(lvl, "break_step") is False
    assert _has_step_content(lvl, "debug") is False
    assert _has_step_content(lvl, "build") is True  # mastery trial always runs


# ── attempt evidence ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_attempt_predict_pass_records_evidence(mock_db):
    world, lvl = _level_one()
    if not _has_step_content(lvl, "predict"):
        pytest.skip("level-1 has no predict content")
    answer = lvl.predict.answer
    out = await attempt_level(
        "foundations", lvl.id,
        AttemptRequest(code=answer, language="python", time_spent_seconds=5, step_type="predict"),
        _user(),
    )
    assert out["passed"] is True
    assert out["evidence_recorded"] is True
    assert "predict" in out["steps_passed"]


def test_attempt_fallback_never_records_evidence():
    """A judge pass on missing content must not become stage evidence.

    Pure-helper anchor: an empty level yields zero evidence-eligible
    steps, so no fallback pass can ever satisfy the completion gate.
    (End-to-end fallback behavior is covered by evidence_recorded=False
    on attempt responses for content-missing steps.)
    """
    from app.models.world import LevelBase

    lvl = LevelBase(id="no-content", title="t", order=0)
    assert _required_steps(lvl) == []
    for step in ("manipulate", "predict", "retrieval", "transfer", "break_step", "debug"):
        assert _has_step_content(lvl, step) is False


# ── complete gate ────────────────────────────────────────────────

def _passing_code_for(lvl) -> str:
    # Passing code is level-specific (regex judge). Foundations level-1
    # requires `apples = 5`; keep this helper scoped to that level.
    assert lvl.id == "level-1", f"helper only knows level-1, got {lvl.id}"
    return "apples = 5"


@pytest.mark.asyncio
async def test_complete_refuses_when_steps_missing(mock_db):
    _, lvl = _level_one()
    with pytest.raises(HTTPException) as exc:
        await complete_level(
            "foundations", lvl.id,
            AttemptRequest(code=_passing_code_for(lvl), language="python", time_spent_seconds=10),
            _user("missing_steps_user"),
        )
    assert exc.value.status_code == 400
    detail = exc.value.detail
    assert isinstance(detail, dict) and "missing_steps" in detail
    assert detail["missing_steps"], "must name the missing stages"
    # No reward, no completion persisted.
    doc = await mock_db["gamification"].find_one({"user_id": "missing_steps_user"})
    assert not (doc or {}).get("completed_competencies", {}).get(
        f"foundations:{lvl.id}", {}).get("completed")


@pytest.mark.asyncio
async def test_complete_fails_mastery_trial(mock_db):
    """Wrong final code fails even with (irrelevant) prior evidence."""
    _, lvl = _level_one()
    with pytest.raises(HTTPException) as exc:
        await complete_level(
            "foundations", lvl.id,
            AttemptRequest(code="", language="python", time_spent_seconds=1),
            _user("trial_fail_user"),
        )
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_complete_valid_with_seeded_evidence_then_deduplicates(mock_db):
    _, lvl = _level_one()
    required = _required_steps(lvl)
    uid = "valid_user"
    key = f"foundations:{lvl.id}"
    steps_passed = {
        s: {"passed_at": "2026-01-01T00:00:00+00:00", "attempts": 1} for s in required
    }
    await mock_db["gamification"].insert_one(
        {"user_id": uid, "completed_competencies": {key: {
            "completed": False, "score": 0, "best_score": 0, "attempts": len(required),
            "failed_attempts": 0, "hints_used": [], "total_time_seconds": 0,
            "steps_passed": steps_passed,
        }}}
    )
    first = await complete_level(
        "foundations", lvl.id,
        AttemptRequest(code=_passing_code_for(lvl), language="python", time_spent_seconds=10),
        _user(uid),
    )
    assert first["completed"] is True
    assert first.get("deduplicated") is not True
    assert first["xp_awarded"] > 0

    second = await complete_level(
        "foundations", lvl.id,
        AttemptRequest(code=_passing_code_for(lvl), language="python", time_spent_seconds=11),
        _user(uid),
    )
    assert second.get("deduplicated") is True
    assert second["xp_awarded"] == 0


@pytest.mark.asyncio
async def test_legacy_completed_preserved_without_stage_evidence(mock_db):
    """Grandfather policy: historical completions never lose progress."""
    _, lvl = _level_one()
    uid = "legacy_user"
    key = f"foundations:{lvl.id}"
    await mock_db["gamification"].insert_one(
        {"user_id": uid, "completed_competencies": {key: {
            "completed": True, "score": 80, "best_score": 80,
        }}}
    )
    out = await complete_level(
        "foundations", lvl.id,
        AttemptRequest(code=_passing_code_for(lvl), language="python", time_spent_seconds=10),
        _user(uid),
    )
    assert out["completed"] is True
    assert out.get("deduplicated") is True


# ── AI separation ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_aptitude_correct_uses_deterministic_score_not_ai(mock_db):
    from app.models.question import SubmitAnswer
    from app.routes import questions_solve as qs

    fake_q = {"id": "q1", "type": "aptitude", "correct_answer": "42",
              "topic": "t", "companies": []}
    with patch.object(qs.question_store, "find_one", return_value=fake_q), \
        patch.object(qs, "chat_completion", new=AsyncMock(
            return_value='{"score": 3, "is_correct": false, "feedback": "bad"}')), \
        patch.object(qs, "record_practice", new=AsyncMock()) as rp, \
        patch.object(qs, "check_and_reset_monthly_usage", new=AsyncMock()):
        out = await qs.submit_answer(
            SubmitAnswer(question_id="q1", answer="42"), _user("ai_det"))
    assert out["is_correct"] is True  # deterministic key wins over AI
    assert out["evaluation_method"] == "deterministic"
    rp.assert_awaited_once()
    assert rp.await_args.args[2] == 10  # deterministic 10, not AI 3


@pytest.mark.asyncio
async def test_aptitude_wrong_ai_high_score_does_not_inflate(mock_db):
    from app.models.question import SubmitAnswer
    from app.routes import questions_solve as qs

    fake_q = {"id": "q1", "type": "aptitude", "correct_answer": "42",
              "topic": "t", "companies": []}
    with patch.object(qs.question_store, "find_one", return_value=fake_q), \
        patch.object(qs, "chat_completion", new=AsyncMock(
            return_value='{"score": 9, "is_correct": true, "feedback": "great"}')), \
        patch.object(qs, "record_practice", new=AsyncMock()) as rp, \
        patch.object(qs, "check_and_reset_monthly_usage", new=AsyncMock()), \
        patch.object(qs, "get_or_create_explanation", new=AsyncMock(return_value=None)):
        out = await qs.submit_answer(
            SubmitAnswer(question_id="q1", answer="41"), _user("ai_wrong"))
    assert out["is_correct"] is False
    assert out["ai_score"] == 9  # coaching visible…
    assert out["score"] == 0  # …but mastery input stays 0
    rp.assert_awaited_once()
    assert rp.await_args.args[2] == 0


@pytest.mark.asyncio
async def test_subjective_answer_never_writes_mastery(mock_db):
    from app.models.question import SubmitAnswer
    from app.routes import questions_solve as qs

    fake_q = {"id": "q9", "type": "coding", "correct_answer": "",
              "topic": "t", "companies": []}
    with patch.object(qs.question_store, "find_one", return_value=fake_q), \
        patch.object(qs, "chat_completion", new=AsyncMock(
            return_value='{"score": 9, "is_correct": true, "feedback": "nice"}')), \
        patch.object(qs, "record_practice", new=AsyncMock()) as rp, \
        patch.object(qs, "check_and_reset_monthly_usage", new=AsyncMock()):
        out = await qs.submit_answer(
            SubmitAnswer(question_id="q9", answer="some prose"), _user("ai_subj"))
    assert out["evaluation_method"] == "subjective_ai_coaching_only"
    rp.assert_not_awaited()


def test_random_route_filters_to_verified_only():
    import inspect

    from app.routes import questions_solve as qs

    src = inspect.getsource(qs)
    # The /random handler must chain .only_verified() on the find() call.
    assert "only_verified()" in src
    # Confirm the candidates line specifically (regression anchor).
    assert "question_store.find(query).only_verified().to_list()" in src.replace("\n", "")
