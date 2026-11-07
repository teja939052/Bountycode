"""Tests for topic-level progression in the company-aware Study Engine."""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app import database
from app.services import study_engine


@pytest.mark.asyncio
async def test_company_mission_advances_to_next_unmastered_topic(monkeypatch):
    async def user_profile(_user_id):
        return {
            "company_track": "tcs_nqt",
            "target_company": "tcs",
            "target_role": "SDE",
        }

    monkeypatch.setattr(study_engine, "_get_user_profile", user_profile)

    progress = {
        "user_id": "student-1",
        "track_id": "tcs_nqt",
        "sections": {
            "tcs_foundation": {
                "section_id": "tcs_foundation",
                "title": "Foundation Round",
                "completed": False,
                "modules": {
                    "tcs_f1": {
                        "completed": False,
                        "topic_mastery": {
                            "percentages": {
                                "mastered": True,
                                "score": 90.0,
                            }
                        },
                    }
                },
            }
        },
    }
    fake_collection = SimpleNamespace(find_one=AsyncMock(return_value=progress))
    monkeypatch.setattr(database, "user_company_tracks_collection", fake_collection)

    mission = await study_engine._get_company_mission("student-1")

    assert mission is not None
    assert mission["track_id"] == "tcs_nqt"
    assert mission["module_id"] == "tcs_f1"
    assert mission["topic_id"] == "profit_loss"
    assert mission["topic_name"] == "profit loss"
    assert mission["mastered_topic_count"] == 1
    assert mission["required_topic_count"] == 3
    assert "profit loss" in mission["title"].lower()


@pytest.mark.asyncio
async def test_company_mission_does_not_repeat_topics_below_mastery_threshold(monkeypatch):
    async def user_profile(_user_id):
        return {"company_track": "tcs_nqt", "target_company": "tcs"}

    monkeypatch.setattr(study_engine, "_get_user_profile", user_profile)

    progress = {
        "sections": {
            "tcs_foundation": {
                "completed": False,
                "modules": {
                    "tcs_f1": {
                        "completed": False,
                        "topic_mastery": {
                            "percentages": {"mastered": True, "score": 85.0},
                            # A score below 70 is an attempt, not mastery.
                            "profit_loss": {"mastered": False, "last_score": 55.0},
                        },
                    }
                },
            }
        }
    }
    fake_collection = SimpleNamespace(find_one=AsyncMock(return_value=progress))
    monkeypatch.setattr(database, "user_company_tracks_collection", fake_collection)

    mission = await study_engine._get_company_mission("student-1")

    assert mission is not None
    assert mission["topic_id"] == "profit_loss"
    assert mission["mastered_topic_count"] == 1
    assert mission["required_topic_count"] == 3
