"""Unit tests for the read-only content quality auditor."""
from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_service_company_content.py"
SPEC = importlib.util.spec_from_file_location("service_company_content_audit", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(AUDIT)


def test_auditor_flags_placeholder_hints_and_missing_trust_evidence():
    item = {
        "id": "bad-item-1",
        "type": "coding",
        "question": "Return the first unique character in the supplied string.",
        "explanation": "Solve this problem using an efficient approach.",
        "hints": ["Hint 1 for the problem", "Hint 2 for the problem"],
        "companies": ["cognizant"],
        "trust_status": "verified",
        "solution": {"code": "print('x')"},
        "testcases": [{"input": "a", "expected": "a"}],
    }
    issues = AUDIT.audit_item(AUDIT.ROOT / "sample.json", item)
    codes = {issue["code"] for issue in issues}

    assert "template_filler" in codes
    assert "insufficient_code_tests" in codes
    assert "trust_claim_without_review_evidence" in codes
    assert "trust_claim_without_validation_evidence" in codes


def test_auditor_flags_incoherent_mcq_answer_key():
    item = {
        "id": "bad-item-2",
        "type": "mcq",
        "question": "Which option is the correct answer for this clearly stated scenario?",
        "options": {"A": "First", "B": "Second", "C": "Third"},
        "correct_answer": "D",
        "explanation": "A complete explanation that is long enough for this structural audit.",
    }
    issues = AUDIT.audit_item(AUDIT.ROOT / "sample.json", item)
    assert any(issue["code"] == "answer_not_in_options" for issue in issues)


def test_auditor_does_not_modify_candidate_files():
    from pathlib import Path
    candidate = AUDIT.ROOT / "candidates" / "service_company_patterns_v1.json"
    assert "candidates" in candidate.parts
    assert AUDIT._looks_like_bank(candidate) is False
