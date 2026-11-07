import asyncio

from app.routes import adaptive_learning as adaptive_routes
from app.services import adaptive_learning as adaptive_service
from app.services.adaptive_learning import (
    _assessment_summary,
    _calculate_mastery_score,
    _is_mastery_evidence_activity,
    record_learning_activity,
)


def test_only_server_graded_assessments_count_toward_mastery():
    assert _is_mastery_evidence_activity({
        "type": "quiz_answer",
        "source": "server",
        "success": True,
    })
    assert _is_mastery_evidence_activity({
        "type": "lesson_assessment",
        "source": "server",
        "success": False,
        "question_count": 10,
        "correct_count": 4,
    })
    assert _is_mastery_evidence_activity({
        "type": "diagnostic",
        "source": "server",
        "success": True,
    })


def test_engagement_and_client_telemetry_never_certify_mastery():
    assert not _is_mastery_evidence_activity({"type": "lesson_step", "success": True})
    # Legacy events without an explicit server provenance marker are not
    # silently trusted: older clients could write arbitrary event types.
    assert not _is_mastery_evidence_activity({"type": "quiz_answer", "success": True})
    assert not _is_mastery_evidence_activity({"type": "lesson_complete", "success": True})
    assert not _is_mastery_evidence_activity({
        "type": "quiz_answer",
        "source": "client_self_reported",
        "success": True,
    })
    assert not _is_mastery_evidence_activity({"type": "self_reported", "success": True})


def test_mastery_requires_repeated_question_level_evidence():
    one_lucky_answer = _calculate_mastery_score(1, 1)
    five_correct_answers = _calculate_mastery_score(5, 5)
    ten_correct_answers = _calculate_mastery_score(10, 10)

    assert one_lucky_answer < 10
    assert five_correct_answers < 50
    assert ten_correct_answers == 45
    assert _calculate_mastery_score(20, 20) == 100
    assert _calculate_mastery_score(0, 10) == 5
    assert _calculate_mastery_score(0, 0) == 0


def test_mastery_score_clamps_invalid_counts():
    assert _calculate_mastery_score(12, 10) == 45
    assert _calculate_mastery_score(-3, 10) == 5
    assert _calculate_mastery_score(0, -1) == 0



def test_public_activity_endpoint_discards_client_claimed_correctness(monkeypatch):
    captured = {}

    async def fake_record(_user_id, activity):
        captured.update(activity)
        return {"status": "success", "score_delta": 0}

    monkeypatch.setattr(adaptive_routes, "record_learning_activity", fake_record)
    response = asyncio.run(adaptive_routes.record_activity(
        {
            "domain_id": "sql",
            "type": "quiz_answer",
            "success": True,
            "score_impact": 100,
            "correct_count": 100,
            "question_count": 100,
        },
        {"id": "learner-1"},
    ))

    assert response["mastery_updated"] is False
    assert captured == {
        "domain_id": "sql",
        "type": "self_reported",
        "success": False,
        "score_impact": 0,
        "source": "client_self_reported",
    }


def test_activity_writer_rejects_untrusted_domain_paths():
    result = asyncio.run(record_learning_activity(
        "learner-1",
        {"domain_id": "skills.$set.score", "type": "quiz_answer", "success": True},
    ))
    assert result["status"] == "error"



def test_assessment_summary_separates_skill_score_from_domain_coverage():
    summary = _assessment_summary({
        "arrays_hashing": {"score": 70, "total_attempts": 10, "correct_count": 8},
        "sql": {"score": 0, "total_attempts": 0, "correct_count": 0},
    })

    assert summary["overall_score"] == 70
    assert summary["assessed_domains"] == 1
    assert summary["domain_coverage_pct"] == 50
    assert summary["total_attempts"] == 10
    assert summary["overall_accuracy"] == 80


def test_assessment_summary_handles_a_new_learner_without_evidence():
    summary = _assessment_summary({
        "arrays_hashing": {"score": 0, "total_attempts": 0, "correct_count": 0},
        "sql": {"score": 0, "total_attempts": 0, "correct_count": 0},
    })

    assert summary["overall_score"] == 0
    assert summary["assessed_domains"] == 0
    assert summary["domain_coverage_pct"] == 0



class _Cursor:
    def __init__(self, documents):
        self.documents = documents

    async def to_list(self, _limit):
        return list(self.documents)


class _Collection:
    def __init__(self, documents=None):
        self.documents = documents or []

    def find(self, _query):
        return _Cursor(self.documents)


class _Cache:
    async def get(self, *_args):
        return None

    async def set(self, *_args, **_kwargs):
        return None


def test_assess_user_skills_ignores_lesson_completion_and_step_engagement(monkeypatch):
    monkeypatch.setattr(adaptive_service, "cache", _Cache())
    monkeypatch.setattr(adaptive_service, "solved_problems_collection", _Collection())
    monkeypatch.setattr(adaptive_service, "submissions_collection", _Collection())
    monkeypatch.setattr(adaptive_service, "question_answers_collection", _Collection())
    monkeypatch.setattr(adaptive_service, "learning_progress_collection", _Collection([
        {
            "user_id": "learner-1",
            "activities": [
                {"domain_id": "arrays_hashing", "type": "lesson_step", "success": True},
                {"domain_id": "arrays_hashing", "type": "lesson_complete", "success": True},
                {"domain_id": "arrays_hashing", "type": "self_reported", "success": True},
            ],
        }
    ]))

    result = asyncio.run(adaptive_service.assess_user_skills("learner-1"))

    skill = result["skills"]["arrays_hashing"]
    assert skill["total_attempts"] == 0
    assert skill["score"] == 0
    assert result["assessed_domains"] == 0
    assert result["domain_coverage_pct"] == 0


def test_assess_user_skills_counts_server_graded_assessment_questions(monkeypatch):
    monkeypatch.setattr(adaptive_service, "cache", _Cache())
    monkeypatch.setattr(adaptive_service, "solved_problems_collection", _Collection())
    monkeypatch.setattr(adaptive_service, "submissions_collection", _Collection())
    monkeypatch.setattr(adaptive_service, "question_answers_collection", _Collection())
    monkeypatch.setattr(adaptive_service, "learning_progress_collection", _Collection([
        {
            "user_id": "learner-1",
            "activities": [{
                "domain_id": "sql",
                "type": "lesson_assessment",
                "source": "server",
                "success": True,
                "question_count": 10,
                "correct_count": 8,
            }],
        }
    ]))

    result = asyncio.run(adaptive_service.assess_user_skills("learner-1"))

    skill = result["skills"]["sql"]
    assert skill["total_attempts"] == 10
    assert skill["correct_count"] == 8
    assert skill["accuracy"] == 80
    assert skill["score"] == 37
    assert result["assessed_domains"] == 1
