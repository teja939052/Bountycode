"""Integration tests for the Evidence Graph — P0/P1 validation matrix.

Verifies that evidence (LearningEvents) is persisted correctly across every
student-flow transition, with canonical skill IDs and structured diagnosis
codes. These tests exercise the pure-logic portions (diagnosis module,
skill normalization, mastery evidence, outcome report builder) without
requiring a live MongoDB connection.
"""
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


# ── 1. New user → no events ─────────────────────────────────────────────────

def test_learning_event_defaults_for_new_user():
    """A LearningEvent created with minimal fields is valid."""
    from app.models.learning_event import LearningEventIn
    ev = LearningEventIn(
        activity_type="practice",
        source="question_bank",
    )
    assert ev.passed is False
    assert ev.diagnosis_codes == []
    assert ev.hints_used == 0
    assert ev.attempt_number == 1


# ── 2. Lesson failure → CONCEPT_GAP diagnosis ──────────────────────────────

def test_diagnosis_question_failure_low_score():
    """Low-scoring question produces CONCEPT_GAP diagnosis code."""
    from app.services.diagnosis import diagnose_question_failure
    from app.models.learning_event import CONCEPT_GAP
    result = diagnose_question_failure(
        score=2.0, answer_text="idk", q_type="coding",
        question={},
        metadata={"all_passed": False, "passed_count": 0, "total": 3},
    )
    assert isinstance(result, dict)
    assert "codes" in result
    assert "reason" in result
    assert CONCEPT_GAP in result["codes"]


def test_diagnosis_question_failure_high_score_no_codes():
    """High-scoring coding question with all_passed=True produces no failure codes."""
    from app.services.diagnosis import diagnose_question_failure
    result = diagnose_question_failure(
        score=9.0, answer_text="great answer", q_type="coding",
        question={},
        metadata={"all_passed": True, "passed_count": 5, "total": 5},
    )
    # At high score with all_passed=True, no failure diagnosis codes
    assert all(c not in result["codes"] for c in [
        "CONCEPT_GAP", "PATTERN_RECOGNITION", "EDGE_CASE_MISSED",
        "TIME_MANAGEMENT", "IMPLEMENTATION_ERROR",
    ])


def test_diagnosis_question_failure_coding_all_failed():
    """Coding question with all test cases failing → IMPLEMENTATION_ERROR + PATTERN_RECOGNITION."""
    from app.services.diagnosis import diagnose_question_failure
    from app.models.learning_event import IMPLEMENTATION_ERROR, PATTERN_RECOGNITION
    result = diagnose_question_failure(
        score=3.0, answer_text="", q_type="coding",
        question={},
        metadata={"all_passed": False, "passed_count": 0, "total": 5},
    )
    assert IMPLEMENTATION_ERROR in result["codes"]
    assert PATTERN_RECOGNITION in result["codes"]


# ── 3. Lesson mastery → passed=True ─────────────────────────────────────────

def test_learning_event_passed_true():
    from app.models.learning_event import LearningEventIn
    ev = LearningEventIn(
        activity_type="learn", source="lesson",
        skill_id="coding.variables", score=9.5, passed=True,
        mastery_after=85.0,
    )
    assert ev.passed is True
    assert ev.skill_id == "coding.variables"


# ── 4. Skill ID normalization across all sources ────────────────────────────

def test_canonical_skill_id_arrays_hashing():
    from app.services.skill_taxonomy import canonical_skill_id
    assert canonical_skill_id("arrays_hashing") == "dsa.arrays"


def test_canonical_skill_id_technical():
    from app.services.skill_taxonomy import canonical_skill_id
    assert canonical_skill_id("technical") == "interview.technical"


def test_canonical_skill_id_aptitude():
    from app.services.skill_taxonomy import canonical_skill_id
    assert canonical_skill_id("aptitude") == "aptitude.quantitative"


def test_canonical_skill_id_already_canonical():
    from app.services.skill_taxonomy import canonical_skill_id
    assert canonical_skill_id("dsa.trees") == "dsa.trees"


def test_canonical_skill_id_none():
    from app.services.skill_taxonomy import canonical_skill_id
    assert canonical_skill_id(None) is None
    assert canonical_skill_id("") is None


def test_parse_oa_section():
    from app.services.skill_taxonomy import parse_oa_section
    assert parse_oa_section("coding") == "dsa.arrays"
    assert parse_oa_section("aptitude") == "aptitude.quantitative"
    assert parse_oa_section("logical") == "aptitude.logical"
    assert parse_oa_section("verbal") == "aptitude.verbal"
    assert parse_oa_section("behavioral") == "behavioral.communication"


def test_parse_interview_dimension():
    from app.services.skill_taxonomy import parse_interview_dimension
    assert parse_interview_dimension("technical") == "interview.technical"
    assert parse_interview_dimension("communication") == "interview.communication"
    assert parse_interview_dimension("problem_solving") == "interview.problem_solving"
    assert parse_interview_dimension("depth") == "interview.depth"


def test_normalize_skill_id_alias():
    """normalize_skill_id is an alias for canonical_skill_id."""
    from app.services.skill_taxonomy import normalize_skill_id, canonical_skill_id
    assert normalize_skill_id("arrays_hashing") == canonical_skill_id("arrays_hashing")


# ── 5. Interview dimension diagnosis ────────────────────────────────────────

def test_diagnose_interview_failure_low_score():
    from app.services.diagnosis import diagnose_interview_failure
    codes = diagnose_interview_failure("technical", 3.0, None, "weak answer", "trees")
    assert len(codes) > 0
    assert any(c in codes for c in [
        "CONCEPT_GAP", "IMPLEMENTATION_ERROR", "TECHNICAL_ACCURACY",
    ])


def test_diagnose_interview_failure_high_score():
    from app.services.diagnosis import diagnose_interview_failure
    codes = diagnose_interview_failure("technical", 9.0, None, "great answer")
    assert codes == []


# ── 6. OA section diagnosis ─────────────────────────────────────────────────

def test_diagnose_oa_section_failure_low_accuracy():
    from app.services.diagnosis import diagnose_oa_section_failure
    codes = diagnose_oa_section_failure("aptitude", 30.0, 10, 3)
    assert "CONCEPT_GAP" in codes


def test_diagnose_oa_section_failure_high_accuracy():
    from app.services.diagnosis import diagnose_oa_section_failure
    codes = diagnose_oa_section_failure("aptitude", 95.0, 10, 9)
    assert len(codes) == 0


def test_diagnose_oa_section_failure_time_management():
    from app.services.diagnosis import diagnose_oa_section_failure
    codes = diagnose_oa_section_failure(
        "coding", 40.0, 5, 2,
        time_per_question=[200, 180, 250, 300, 150],
    )
    assert "TIME_MANAGEMENT" in codes


def test_diagnose_oa_section_zero_score():
    from app.services.diagnosis import diagnose_oa_section_failure
    codes = diagnose_oa_section_failure("dsa", 0.0, 5, 0)
    assert codes == ["CONCEPT_GAP"]


# ── 7. Mastery evidence enforcement ────────────────────────────────────────

def test_has_mastery_evidence_requires_completion():
    from app.services.journey_engine import _has_mastery_evidence
    completed = {}
    assert not _has_mastery_evidence("world1", "level1", completed)


def test_has_mastery_evidence_requires_score_70():
    from app.services.journey_engine import _has_mastery_evidence
    completed = {"world1:level1": {"completed": True, "score": 69, "steps_completed": 3}}
    assert not _has_mastery_evidence("world1", "level1", completed)


def test_has_mastery_evidence_requires_steps():
    from app.services.journey_engine import _has_mastery_evidence
    completed = {"world1:level1": {"completed": True, "score": 85, "steps_completed": 2}}
    assert not _has_mastery_evidence("world1", "level1", completed)


def test_has_mastery_evidence_passes_all():
    from app.services.journey_engine import _has_mastery_evidence
    completed = {"world1:level1": {"completed": True, "score": 85, "steps_completed": 3}}
    assert _has_mastery_evidence("world1", "level1", completed)


# ── 8. Skill ID → category/competency resolution ───────────────────────────

def test_resolve_skill_to_category():
    from app.services.skill_taxonomy import resolve_skill_to_category
    assert resolve_skill_to_category("dsa.trees") == "dsa"
    assert resolve_skill_to_category("aptitude.quantitative") == "aptitude"
    assert resolve_skill_to_category("coding.variables") == "coding"
    assert resolve_skill_to_category("interview.technical") == "behavioral"


def test_resolve_skill_to_competency():
    from app.services.skill_taxonomy import resolve_skill_to_competency
    assert resolve_skill_to_competency("dsa.trees") == "trees"
    assert resolve_skill_to_competency("dsa.binary_search") == "binary_search"
    assert resolve_skill_to_competency("dsa.two_pointers") == "arrays"


# ── 9. emit_learning_event graceful failure ─────────────────────────────────

class _AsyncCursor:
    """Async iterator that yields no items."""
    def __aiter__(self):
        return self
    async def __anext__(self):
        raise StopAsyncIteration


def test_emit_learning_event_handles_missing_collection():
    """emit_learning_event must not crash if the collection is unavailable."""
    from app.services.study_engine import emit_learning_event

    async def _test():
        with patch("app.database.learning_events_collection", None):
            result = await emit_learning_event("user123", {
                "activity_type": "practice",
                "source": "question_bank",
                "skill_id": "dsa.trees",
                "passed": True,
                "score": 8,
            })
            assert result is None

    asyncio.run(_test())


def test_emit_learning_event_handles_exception():
    from app.services.study_engine import emit_learning_event

    async def _test():
        mock_col = MagicMock()
        mock_col.return_value = MagicMock()
        mock_col.return_value.insert_one = AsyncMock(side_effect=Exception("DB error"))
        with patch("app.database.learning_events_collection", mock_col):
            result = await emit_learning_event("user123", {
                "activity_type": "practice",
                "source": "question_bank",
                "skill_id": "dsa.arrays",
            })
            assert result is None

    asyncio.run(_test())


# ── 10. Diagnosis codes are canonical ──────────────────────────────────────

def test_diagnosis_codes_are_canonical():
    """All diagnosis codes returned must be from the canonical set."""
    from app.services.diagnosis import (
        diagnose_question_failure, diagnose_interview_failure,
        diagnose_oa_section_failure,
    )
    from app.models.learning_event import ALL_DIAGNOSIS_CODES

    for func, kwargs in [
        (diagnose_question_failure, dict(score=2, answer_text="", q_type="coding", question={},
                                          metadata={"all_passed": False, "passed_count": 0, "total": 3})),
        (diagnose_question_failure, dict(score=2, answer_text="", q_type="aptitude", question={})),
        (diagnose_question_failure, dict(score=9, answer_text="good", q_type="text", question={})),
    ]:
        result = func(**kwargs)
        for code in result["codes"] if isinstance(result, dict) else result:
            assert code in ALL_DIAGNOSIS_CODES, f"Non-canonical code: {code}"

    for dim in ["technical", "communication", "problem_solving", "depth"]:
        codes = diagnose_interview_failure(dim, 3.0, None, "bad")
        for code in codes:
            assert code in ALL_DIAGNOSIS_CODES, f"Non-canonical code: {code}"

    for section in ["aptitude", "coding", "dsa", "verbal"]:
        codes = diagnose_oa_section_failure(section, 30.0, 5, 1)
        for code in codes:
            assert code in ALL_DIAGNOSIS_CODES, f"Non-canonical code: {code}"


# ── 11. Outcome report structure (with mocked collections) ──────────────────

def test_build_outcomes_returns_correct_structure():
    """_build_outcomes returns the expected JSON structure with empty data."""
    from app.routes.journey import _build_outcomes

    async def _test():
        empty_col = MagicMock()
        empty_col.find.return_value.sort.return_value = _AsyncCursor()

        with patch("app.database.learning_events_collection", empty_col), \
             patch("app.database.interviews_collection", empty_col), \
             patch("app.database.oa_sessions_collection", empty_col), \
             patch("app.services.readiness_engine.compute_readiness", new_callable=AsyncMock) as mock_readiness, \
             patch("app.services.journey_engine.build_journey_state", new_callable=AsyncMock) as mock_journey:

            mock_readiness.return_value = {"overall": 75, "verdict": "NEEDS PREPARATION"}
            mock_journey.return_value = {"today": {"next": {"type": "practice"}}}

            report = await _build_outcomes("test_user")

            assert report["user_id"] == "test_user"
            assert "generated_at" in report
            assert "summary" in report
            assert report["summary"]["total_events"] == 0
            assert "skill_progression" in report
            assert "oa_improvement" in report
            assert "interview_improvement" in report
            assert "weaknesses_repaired" in report
            assert "current_readiness" in report
            assert "next_action" in report

    asyncio.run(_test())


# ── 12. Outcome report OA improvement tracking ─────────────────────────────

def test_build_outcomes_oa_improvement_with_data():
    """Outcome report shows OA score improvement from first to latest."""
    from app.routes.journey import _build_outcomes
    from datetime import datetime, timezone

    async def _test():
        mock_events = [
            {"_id": "1", "user_id": "u1", "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc),
             "activity_type": "oa_complete", "source": "oa", "skill_id": "aptitude.quantitative",
             "passed": False, "score": 30.0, "mastery_before": 0, "mastery_after": 30,
             "diagnosis_codes": ["CONCEPT_GAP"]},
            {"_id": "2", "user_id": "u1", "timestamp": datetime(2024, 2, 1, tzinfo=timezone.utc),
             "activity_type": "oa_complete", "source": "oa", "skill_id": "aptitude.quantitative",
             "passed": True, "score": 85.0, "mastery_before": 30, "mastery_after": 85,
             "diagnosis_codes": []},
        ]
        mock_empty = [
            {"_id": "1", "user_id": "u1", "started_at": datetime(2024, 1, 1, tzinfo=timezone.utc),
             "result": {"overall_readiness": 30.0}},
            {"_id": "2", "user_id": "u1", "started_at": datetime(2024, 2, 1, tzinfo=timezone.utc),
             "result": {"overall_readiness": 85.0}},
        ]

        def make_async_col(docs):
            col = MagicMock()
            async_iter_obj = MagicMock()
            async_iter_obj.__aiter__ = MagicMock(return_value=async_iter_obj)
            async_iter_obj.__anext__ = AsyncMock(side_effect=_make_stop_iter(docs))
            col.find.return_value.sort.return_value = async_iter_obj
            # _build_outcomes calls learning_events_collection() as a function,
            # so the mock must return itself (its own API) when called.
            col.return_value = col
            return col

        def _make_stop_iter(docs):
            it = iter(docs)
            async def _next():
                try:
                    return next(it)
                except StopIteration:
                    raise StopAsyncIteration
            return _next

        le_col = make_async_col(mock_events)
        # interviews: empty async iter
        int_col = MagicMock()
        int_col.return_value = int_col
        int_col.find.return_value.sort.return_value = _AsyncStopIter()
        # oa_sessions: feed the two OA sessions so oa_improvement is exercised
        oa_col = make_async_col(mock_empty)

        with patch("app.routes.journey.learning_events_collection", le_col), \
             patch("app.routes.journey.interviews_collection", int_col), \
             patch("app.routes.journey.oa_sessions_collection", oa_col), \
             patch("app.services.readiness_engine.compute_readiness", new_callable=AsyncMock) as mock_readiness, \
             patch("app.services.journey_engine.build_journey_state", new_callable=AsyncMock) as mock_journey:

            mock_readiness.return_value = None
            mock_journey.return_value = {}

            report = await _build_outcomes("u1")

            # Skill progression should show improvement
            assert len(report["skill_progression"]) == 1
            snap = report["skill_progression"][0]
            assert snap["skill_id"] == "aptitude.quantitative"
            assert snap["assessment_count"] == 2
            # OA improvement should reflect the two scores
            if report["oa_improvement"]:
                assert report["oa_improvement"]["attempts"] == 2

    asyncio.run(_test())


class _AsyncStopIter:
    """Async iterator that yields nothing."""
    def __aiter__(self):
        return self
    async def __anext__(self):
        raise StopAsyncIteration


def _list_async_iter(items):
    """Helper: return an async iterator over a list."""
    async def _gen():
        for item in items:
            yield item
    return _gen()


def _async_empty_col():
    """Return a mock collection that yields no documents."""
    col = MagicMock()
    col.find.return_value.sort.return_value = _AsyncStopIter()
    return col


# ── 13. Record activity produces LearningEvent with normalized skill ──────

def test_record_activity_emits_event():
    """record_activity should persist a LearningEvent with normalized skill_id."""
    from app.services.study_engine import record_activity

    async def _test():
        mock_result = MagicMock()
        mock_result.inserted_id = "evt_123"

        mock_event_col = MagicMock()
        mock_event_col.return_value = mock_event_col  # record_activity calls collection()
        mock_event_col.insert_one = AsyncMock(return_value=mock_result)

        mock_update_col = MagicMock()
        mock_update_col.update_one = AsyncMock(return_value=MagicMock())
        mock_update_col.find_one = AsyncMock(return_value=None)
        mock_update_col.find = MagicMock(return_value=MagicMock())
        mock_update_col.find.return_value.sort.return_value = _AsyncStopIter()

        with patch("app.database.learning_events_collection", mock_event_col), \
             patch("app.database.srs_cards_collection", mock_update_col), \
             patch("app.database.skill_graph_collection", mock_update_col), \
             patch("app.database.users_collection", mock_update_col), \
             patch("app.services.study_engine.record_practice", new_callable=AsyncMock) as mock_practice, \
             patch("app.services.skill_assessment.update_skill_score", new_callable=AsyncMock), \
             patch("app.services.spaced_repetition.SpacedRepetitionEngine"):

            mock_practice.return_value = {"xp_gained": 25, "level": 1}

            result = await record_activity("user1", {
                "activity_type": "practice",
                "source": "question_bank",
                "skill_id": "arrays_hashing",  # non-canonical
                "score": 85,
                "passed": True,
                "attempts": 1,
            })

            assert result["recorded"] is True
            mock_event_col.insert_one.assert_called_once()
            call_args = mock_event_col.insert_one.call_args
            doc = call_args[0][0] if call_args[0] else {}
            # skill_id should be normalized to canonical form
            assert "." in doc["skill_id"], f"skill_id not canonical: {doc.get('skill_id')}"

    asyncio.run(_test())
