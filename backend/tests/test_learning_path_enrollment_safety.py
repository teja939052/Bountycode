"""Safety tests for learner path and company-track enrollment."""
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from app.services import learning_paths


def _matched_user_collection():
    return SimpleNamespace(
        update_one=AsyncMock(return_value=SimpleNamespace(matched_count=1))
    )


@pytest.mark.asyncio
async def test_role_path_enrollment_preserves_existing_progress_and_does_not_reward(monkeypatch):
    path_id = next(
        key for key, value in learning_paths.ROLES.items()
        if value.get("modules")
    )
    progress = SimpleNamespace(update_one=AsyncMock())
    users = _matched_user_collection()
    reward_writer = AsyncMock()

    monkeypatch.setattr(learning_paths, "user_learning_paths_collection", progress)
    monkeypatch.setattr(learning_paths, "users_collection", lambda: users)
    monkeypatch.setattr(learning_paths, "record_practice", reward_writer)

    result = await learning_paths.enroll_in_path(str(ObjectId()), path_id)

    assert result["success"] is True
    update = progress.update_one.await_args
    assert update.kwargs["upsert"] is True
    assert "$setOnInsert" in update.args[1]
    assert "$set" not in update.args[1]
    reward_writer.assert_not_awaited()


@pytest.mark.asyncio
async def test_company_track_enrollment_preserves_existing_progress_and_does_not_reward(monkeypatch):
    track_id = next(
        key for key, value in learning_paths.COMPANY_TRACKS.items()
        if value.get("sections")
    )
    progress = SimpleNamespace(update_one=AsyncMock())
    users = _matched_user_collection()
    reward_writer = AsyncMock()
    cache = SimpleNamespace(delete=AsyncMock())

    monkeypatch.setattr(learning_paths, "user_company_tracks_collection", progress)
    monkeypatch.setattr(learning_paths, "users_collection", lambda: users)
    monkeypatch.setattr(learning_paths, "record_practice", reward_writer)
    monkeypatch.setattr(learning_paths, "cache", cache)

    result = await learning_paths.enroll_in_track(str(ObjectId()), track_id)

    assert result["success"] is True
    update = progress.update_one.await_args
    assert update.kwargs["upsert"] is True
    assert "$setOnInsert" in update.args[1]
    assert "$set" not in update.args[1]
    assert cache.delete.await_count == 3
    reward_writer.assert_not_awaited()
