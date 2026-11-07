from app.services.adaptive_learning import (
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
    assert ten_correct_answers == 100
    assert _calculate_mastery_score(0, 10) == 16
    assert _calculate_mastery_score(0, 0) == 0


def test_mastery_score_clamps_invalid_counts():
    assert _calculate_mastery_score(12, 10) == 100
    assert _calculate_mastery_score(-3, 10) == 16
    assert _calculate_mastery_score(0, -1) == 0
