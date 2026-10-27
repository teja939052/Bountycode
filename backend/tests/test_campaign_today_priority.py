"""Priority order for Today's single recommendation.

Directive order: repair -> overdue SRS -> guided next mission -> timed proof.
The frontend renders recommendations[0] as the one mission, so the array order
is the product contract.
"""
import asyncio

from app.services import campaign_service as cs


def _battlefield(weakness=None):
    async def fake_battlefield(user_id, company):
        return {
            "biggest_weakness": weakness,
            "total_patterns": 10,
            "mastered_patterns": 2,
            "weak_patterns": 3,
        }

    return fake_battlefield


def _gamification():
    async def fake_gamification(user_id):
        return {"streak": 3, "level": 4}

    return fake_gamification


def _plan():
    async def fake_plan(user_id, company=""):
        return {
            "target_role": "Software Developer",
            "assessment_date": "2026-12-01",
            "days_remaining": 30,
            "overall_score": 72.0,
            "reviews": [
                {"id": "srs-1", "skill_id": "arrays", "title": "SRS: Arrays",
                 "estimated_minutes": 8}
            ],
            "next": {"title": "Patterns", "topic": "patterns",
                     "estimated_minutes": 15},
            "daily_battle": [
                {"id": "battle-1", "topic": "loops", "estimated_minutes": 15}
            ],
            "practice": [],
        }

    return fake_plan


def _run(monkeypatch, weakness):
    monkeypatch.setattr(cs, "get_battlefield", _battlefield(weakness))
    monkeypatch.setattr(cs, "get_gamification_profile", _gamification())
    monkeypatch.setattr(cs, "study_get_today", _plan())
    return asyncio.run(cs.get_today_recommendations("user-1", "tcs"))


def test_repair_then_srs_then_guided_mission(monkeypatch):
    weakness = {
        "id": "loops",
        "name": "Loops",
        "mastery": 40,
        "emoji": "L",
        "diagnosis": ["off-by-one"],
    }
    result = _run(monkeypatch, weakness)
    assert [r["type"] for r in result["recommendations"]] == [
        "repair",
        "review",
        "learn",
    ]


def test_srs_outranks_guided_mission_and_battle(monkeypatch):
    result = _run(monkeypatch, None)
    assert [r["type"] for r in result["recommendations"]] == [
        "review",
        "learn",
        "battle",
    ]
