from app.services.diagnosis import (
    CONCEPT_GAP,
    KNOWLEDGE_RECALL,
    diagnose_question_failure,
)


def test_wrong_quiz_answer_produces_structured_misconception_codes():
    diagnosis = diagnose_question_failure(
        score=0,
        answer_text="I selected option B",
        q_type="mcq",
        question={
            "topic": "SQL Joins",
            "explanation": "A LEFT JOIN preserves every row from the left table.",
        },
        metadata={"all_passed": False, "passed_count": 0, "total": 1},
    )

    assert CONCEPT_GAP in diagnosis["codes"]
    assert diagnosis["reason"]


def test_partial_mcq_performance_can_identify_recall_gap():
    diagnosis = diagnose_question_failure(
        score=6,
        answer_text="",
        q_type="mcq",
        question={},
        metadata={},
    )

    assert CONCEPT_GAP in diagnosis["codes"]
    assert KNOWLEDGE_RECALL in diagnosis["codes"]
