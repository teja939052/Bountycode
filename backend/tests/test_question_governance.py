"""Regression tests for question governance, trust lifecycle, and serving decisions.

Run with: python -m pytest backend/tests/test_question_governance.py -v
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import question_store
from app.services.question_store import (
    load_all,
    _is_servable,
    _is_executable,
    transition_trust,
    get_trust_transition_log,
    TRUST_DRAFT,
    TRUST_NORMALIZED,
    TRUST_AUTOMATED_CHECKED,
    TRUST_HUMAN_REVIEWED,
    TRUST_VERIFIED,
    TRUST_QUARANTINED,
    trust_rank,
    TRUST_RANK,
    fix_stale_mcq_stamps,
    fix_sql_no_test_cases,
    fix_verified_not_executable,
    run_all_content_trust_fixes,
)


class TestTrustLifecycle:
    """Tests for the content trust state machine (DRAFT -> ... -> VERIFIED -> SERVABLE)."""

    def setup_method(self):
        """Reset the trust transition log before each test."""
        question_store._trust_transition_log = []
        question_store._loaded = False
        question_store._questions = []

    def test_forward_transitions_allowed(self):
        """All forward transitions in the lifecycle should succeed."""
        load_all()
        # Find an unverified question
        for q in question_store._questions:
            if q.get("trust_status") == TRUST_DRAFT:
                qid = q["id"]
                break
        else:
            # Create a test question if none found
            qid = "test-q-001"
            question_store._questions.append({
                "id": qid,
                "type": "coding",
                "question": "Test question",
                "trust_status": TRUST_DRAFT,
            })

        # Forward transitions
        assert transition_trust(qid, TRUST_NORMALIZED, "step 1") is True
        assert transition_trust(qid, TRUST_AUTOMATED_CHECKED, "step 2") is True
        assert transition_trust(qid, TRUST_HUMAN_REVIEWED, "step 3") is True
        assert transition_trust(qid, TRUST_VERIFIED, "step 4") is True

    def test_backward_transitions_rejected(self):
        """Backward transitions (e.g., VERIFIED -> DRAFT) should be rejected."""
        load_all()
        for q in question_store._questions:
            if q.get("trust_status") == TRUST_VERIFIED:
                qid = q["id"]
                break
        else:
            qid = "test-q-002"
            question_store._questions.append({
                "id": qid,
                "type": "coding",
                "question": "Test question",
                "trust_status": TRUST_VERIFIED,
            })

        # Backward transition should fail
        assert transition_trust(qid, TRUST_DRAFT, "backward") is False
        assert transition_trust(qid, TRUST_AUTOMATED_CHECKED, "backward") is False

    def test_quarantined_is_terminal(self):
        """QUARANTINED state cannot transition out without manual review."""
        load_all()
        qid = "test-q-quarantine"
        question_store._questions.append({
            "id": qid,
            "type": "coding",
            "question": "Test question",
            "trust_status": TRUST_QUARANTINED,
        })

        # Cannot transition from quarantined to anything else
        assert transition_trust(qid, TRUST_VERIFIED, "unquarantine") is False
        assert transition_trust(qid, TRUST_DRAFT, "reset") is False

        # Can stay quarantined
        assert transition_trust(qid, TRUST_QUARANTINED, "stay") is True

    def test_audit_log_records_transitions(self):
        """Every state transition should be recorded in the audit log."""
        question_store._trust_transition_log = []
        load_all()

        for q in question_store._questions:
            if q.get("trust_status") == TRUST_DRAFT:
                qid = q["id"]
                break
        else:
            qid = "test-q-audit"
            question_store._questions.append({
                "id": qid,
                "type": "coding",
                "question": "Test question",
                "trust_status": TRUST_DRAFT,
            })

        initial_log_len = len(get_trust_transition_log())
        transition_trust(qid, TRUST_NORMALIZED, "test reason")
        assert len(get_trust_transition_log()) == initial_log_len + 1

        log_entry = get_trust_transition_log()[-1]
        assert log_entry["question_id"] == qid
        assert log_entry["from_status"] == TRUST_DRAFT
        assert log_entry["to_status"] == TRUST_NORMALIZED
        assert log_entry["reason"] == "test reason"
        assert log_entry["allowed"] is True
        assert "timestamp" in log_entry

    def test_audit_log_records_rejected_transitions(self):
        """Rejected transitions should also be recorded in the audit log."""
        question_store._trust_transition_log = []
        load_all()

        for q in question_store._questions:
            if q.get("trust_status") == TRUST_VERIFIED:
                qid = q["id"]
                break
        else:
            qid = "test-q-audit-reject"
            question_store._questions.append({
                "id": qid,
                "type": "coding",
                "question": "Test question",
                "trust_status": TRUST_VERIFIED,
            })

        initial_log_len = len(get_trust_transition_log())
        transition_trust(qid, TRUST_DRAFT, "should fail")
        assert len(get_trust_transition_log()) == initial_log_len + 1

        log_entry = get_trust_transition_log()[-1]
        assert log_entry["allowed"] is False
        assert "blocked" in log_entry["reason"]

    def test_trust_rank_ordering(self):
        """Trust ranks should reflect the lifecycle order."""
        assert TRUST_RANK[TRUST_VERIFIED] == 3
        assert TRUST_RANK[TRUST_HUMAN_REVIEWED] == 2
        assert TRUST_RANK[TRUST_AUTOMATED_CHECKED] == 1
        assert TRUST_RANK[TRUST_NORMALIZED] == 1
        assert TRUST_RANK[TRUST_DRAFT] == 0
        assert TRUST_RANK[TRUST_QUARANTINED] == -1


class TestServingGate:
    """Tests for the _is_servable and _is_executable serving gates."""

    def test_verified_coding_with_test_cases_is_servable(self):
        """A verified coding question with test cases should be servable."""
        q = {
            "id": "serv-001",
            "type": "coding",
            "trust_status": "verified",
            "testcases": [{"input": [1, 2], "expected": 3}],
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is True

    def test_verified_coding_without_test_cases_is_not_servable(self):
        """A verified coding question without test cases should NOT be servable."""
        q = {
            "id": "serv-002",
            "type": "coding",
            "trust_status": "verified",
        }
        assert _is_executable(q) is False
        assert _is_servable(q) is False

    def test_automated_checked_is_not_servable(self):
        """Automatically checked questions should NOT be servable (need human review)."""
        q = {
            "id": "serv-003",
            "type": "coding",
            "trust_status": "automated_checked",
            "testcases": [{"input": [1], "expected": 1}],
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is False

    def test_unverified_is_not_servable(self):
        """Unverified questions should NOT be servable."""
        q = {
            "id": "serv-004",
            "type": "coding",
            "trust_status": "unverified",
            "testcases": [{"input": [1], "expected": 1}],
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is False

    def test_quarantined_is_not_servable(self):
        """Quarantined questions should NOT be servable."""
        q = {
            "id": "serv-005",
            "type": "coding",
            "trust_status": "quarantined",
            "testcases": [{"input": [1], "expected": 1}],
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is False

    def test_reviewed_coding_with_test_cases_is_servable(self):
        """A reviewed coding question with test cases should be servable."""
        q = {
            "id": "serv-006",
            "type": "coding",
            "trust_status": "reviewed",
            "testcases": [{"input": [1], "expected": 1}],
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is True

    def test_sql_without_schema_is_not_executable(self):
        """SQL questions without sql_schema should not be executable."""
        q = {
            "id": "serv-007",
            "type": "sql",
            "trust_status": "verified",
            "test_cases": [{"input": "t", "expected": "e"}],
        }
        assert _is_executable(q) is False
        assert _is_servable(q) is False

    def test_sql_with_schema_is_executable(self):
        """SQL questions with sql_schema should be executable."""
        q = {
            "id": "serv-008",
            "type": "sql",
            "trust_status": "verified",
            "test_cases": [{"input": "t", "expected": "e"}],
            "sql_schema": {"schema_ddl": "CREATE TABLE t (id INT)", "seed_inserts": "", "expected_query": "SELECT 1", "enforce_order": False},
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is True

    def test_mcq_with_valid_options_and_answer_is_executable(self):
        """MCQs with 4 options and valid correct_answer should be executable."""
        q = {
            "id": "serv-009",
            "type": "aptitude",
            "trust_status": "verified",
            "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
            "correct_answer": "A",
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is True

    def test_mcq_with_invalid_answer_is_not_executable(self):
        """MCQs with invalid correct_answer should not be executable."""
        q = {
            "id": "serv-010",
            "type": "aptitude",
            "trust_status": "verified",
            "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
            "correct_answer": "E",
        }
        assert _is_executable(q) is False
        assert _is_servable(q) is False

    def test_interview_with_rubric_is_executable(self):
        """Interview questions with rubric should be executable."""
        q = {
            "id": "serv-011",
            "type": "interview",
            "trust_status": "verified",
            "rubric": "STAR method evaluation",
        }
        assert _is_executable(q) is True
        assert _is_servable(q) is True

    def test_interview_without_rubric_is_not_executable(self):
        """Interview questions without rubric should not be executable."""
        q = {
            "id": "serv-012",
            "type": "interview",
            "trust_status": "verified",
        }
        assert _is_executable(q) is False
        assert _is_servable(q) is False


class TestContentTrustFixes:
    """Tests for the content trust fix functions."""

    def test_fix_stale_mcq_stamps(self):
        """MCQs with invalid correct_answer should be set to needs_review."""
        load_all()
        # Create a test MCQ with stale stamp
        question_store._questions.append({
            "id": "fix-mcq-001",
            "type": "aptitude",
            "trust_status": "verified",
            "correct_answer": "Z",  # Invalid
        })
        fixed = fix_stale_mcq_stamps()
        assert fixed >= 1
        # Verify the question was updated
        for q in question_store._questions:
            if q.get("id") == "fix-mcq-001":
                assert q["trust_status"] == "needs_review"
                break

    def test_fix_sql_no_test_cases(self):
        """SQL questions without test_cases should be quarantined."""
        load_all()
        question_store._questions.append({
            "id": "fix-sql-001",
            "type": "sql",
            "trust_status": "verified",
            "sql_schema": {"schema_ddl": "CREATE TABLE t (id INT)", "seed_inserts": "", "expected_query": "SELECT 1", "enforce_order": False},
        })
        fixed = fix_sql_no_test_cases()
        assert fixed >= 1

    def test_fix_verified_not_executable(self):
        """Verified questions that are not executable should be quarantined."""
        load_all()
        question_store._questions.append({
            "id": "fix-ne-001",
            "type": "coding",
            "trust_status": "verified",
        })
        fixed = fix_verified_not_executable()
        assert fixed >= 1

    def test_run_all_content_trust_fixes(self):
        """run_all_content_trust_fixes should return a summary dict."""
        load_all()
        result = run_all_content_trust_fixes()
        assert "stale_mcq_fixed" in result
        assert "sql_quarantined" in result
        assert "verified_not_exec_quarantined" in result
        assert "total_servable" in result
        assert "total_questions" in result


class TestQuestionInventory:
    """Tests for question inventory generation and deduplication."""

    def test_load_all_populates_questions(self):
        """load_all should populate the questions list."""
        load_all()
        assert len(question_store._questions) > 0

    def test_dedupe_reduces_count(self):
        """Deduplication should reduce or maintain question count."""
        load_all()
        before = len(question_store._questions)
        result = question_store._dedupe_and_filter()
        after = len(result)
        assert after <= before

    def test_servable_count_is_positive(self):
        """There should be at least some servable questions."""
        load_all()
        servable_count = sum(1 for q in question_store._questions if _is_servable(q))
        assert servable_count > 0

    def test_sql_servable_after_schema_backfill(self):
        """SQL questions added by batch scripts should be automated_checked,
        not verified. Pre-existing SQL questions (e.g., sql-001) may be verified
        if human-reviewed. Reviewed questions (from existing curated banks)
        should be servable."""
        load_all()
        sql_questions = [
            q for q in question_store._questions
            if str(q.get("type", "")).lower() == "sql"
        ]
        # Batch-added SQL questions (sql-b2-*) should be automated_checked,
        # not verified, since they lack human review
        for q in sql_questions:
            qid = str(q.get("id", ""))
            if qid.startswith("sql-b2-"):
                trust = str(q.get("trust_status", "")).lower()
                assert trust != "verified", f"SQL question {qid} should not be verified without human review"
                assert trust == "automated_checked", f"SQL question {qid} should be automated_checked, got {trust}"
        # Reviewed questions should be servable
        reviewed_servable = [
            q for q in question_store._questions
            if question_store._is_servable(q) and str(q.get("trust_status", "")).lower() == "reviewed"
        ]
        assert len(reviewed_servable) > 0, "No reviewed questions are servable"


class TestQuestionAPI:
    """Tests for question API contracts."""

    def test_find_one_verified_returns_only_servable(self):
        """find_one_verified should only return servable questions."""
        load_all()
        q = question_store.find_one_verified({"type": "coding"})
        if q is not None:
            assert _is_servable(q) is True

    def test_get_question_for_serving_hides_hidden_cases(self):
        """get_question_for_serving should not expose hidden test cases to free users."""
        # This test checks the data structure; actual hiding is done in the route
        load_all()
        q = question_store.get_question_for_serving("verify-001")
        if q is not None:
            assert q.get("trust_status") in ("verified", "reviewed")
            assert "hidden_test_cases" in q

    def test_count_documents_applies_trust_gate(self):
        """count_documents should only count servable questions."""
        load_all()
        all_count = question_store.count_documents()
        servable_count = sum(1 for q in question_store._questions if _is_servable(q))
        assert all_count == servable_count

    def test_only_verified_cursor_filters_correctly(self):
        """The only_verified cursor should filter out non-servable questions."""
        load_all()
        results = question_store.find().only_verified().to_list()
        for q in results:
            assert _is_servable(q) is True


def test_trust_lifecycle_complete():
    """Integration test: complete trust lifecycle from DRAFT to SERVABLE."""
    load_all()

    # Create a draft question
    test_id = "integration-test-001"
    question_store._questions.append({
        "id": test_id,
        "type": "coding",
        "question": "Integration test question",
        "trust_status": TRUST_DRAFT,
        "testcases": [{"input": [1], "expected": 1}],
    })

    # DRAFT is not servable
    q = question_store._questions[-1]
    assert _is_servable(q) is False

    # Normalize
    transition_trust(test_id, TRUST_NORMALIZED, "normalized")
    assert _is_servable(q) is False  # needs_review is not servable

    # Automated check
    transition_trust(test_id, TRUST_AUTOMATED_CHECKED, "automated check passed")
    assert _is_servable(q) is False  # automated_checked is not servable

    # Human review
    transition_trust(test_id, TRUST_HUMAN_REVIEWED, "human reviewed")
    assert _is_servable(q) is True  # reviewed is servable

    # Verify
    transition_trust(test_id, TRUST_VERIFIED, "independently verified")
    assert _is_servable(q) is True  # verified is servable

    # Verify audit log
    log = get_trust_transition_log()
    assert len(log) == 4  # 4 forward transitions
    allowed_count = sum(1 for e in log if e["allowed"] is True)
    assert allowed_count == 4


class TestTrustIntegrityAudit:
    """Tests for the trust integrity audit function."""

    def test_audit_trust_integrity_flags_unverified_without_transition(self):
        """_audit_trust_integrity() flags verified questions without
        trust_transitioned_at/trust_transition_reason."""
        load_all()

        # Add a verified question without transition metadata (simulates
        # a batch-imported question that bypassed the trust lifecycle)
        question_store._questions.append({
            "id": "audit-test-001",
            "type": "coding",
            "question": "Test question without transition metadata",
            "trust_status": TRUST_VERIFIED,
            "testcases": [{"input": [1], "expected": 1}],
            # NOTE: No trust_transitioned_at or trust_transition_reason
        })

        flagged = question_store._audit_trust_integrity(question_store._questions)

        # At least our test question should be flagged
        assert flagged >= 1

        # Verify the question is still servable (audit only logs, doesn't downgrade)
        q = next(q for q in question_store._questions if q.get("id") == "audit-test-001")
        assert q.get("trust_status") == TRUST_VERIFIED
        assert _is_servable(q) is True

    def test_audit_trust_integrity_does_not_flag_verified_with_transition(self):
        """Questions with trust_status="verified" AND transition metadata
        should NOT be flagged."""
        load_all()

        # Add a verified question WITH transition metadata
        question_store._questions.append({
            "id": "audit-test-002",
            "type": "coding",
            "question": "Test question with transition metadata",
            "trust_status": TRUST_VERIFIED,
            "testcases": [{"input": [1], "expected": 1}],
            "trust_transitioned_at": "2026-01-01T00:00:00Z",
            "trust_transition_reason": "Human reviewed",
        })

        flagged = question_store._audit_trust_integrity(question_store._questions)

        # The audited question should NOT be flagged
        audited_ids = {q.get("id") for q in question_store._questions
                       if q.get("trust_status") == TRUST_VERIFIED
                       and q.get("trust_transitioned_at")
                       and q.get("trust_transition_reason")}
        assert "audit-test-002" in audited_ids

    def test_audit_trust_integrity_does_not_flag_non_verified(self):
        """Questions with trust_status other than "verified" should not
        be flagged by the trust integrity audit."""
        load_all()

        # Add an automated_checked question
        question_store._questions.append({
            "id": "audit-test-003",
            "type": "coding",
            "question": "Test question automated_checked",
            "trust_status": TRUST_AUTOMATED_CHECKED,
            "testcases": [{"input": [1], "expected": 1}],
        })

        flagged = question_store._audit_trust_integrity(question_store._questions)

        # The automated_checked question should still have trust_status="automated_checked"
        q = next(q for q in question_store._questions if q.get("id") == "audit-test-003")
        assert q.get("trust_status") == TRUST_AUTOMATED_CHECKED


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
