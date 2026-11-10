"""Trust-state regression tests for file-based question loading."""
from __future__ import annotations

import pytest

from app.services import content_loader


@pytest.fixture(autouse=True)
def reset_seen_ids():
    content_loader._SEEN_IDS.clear()
    yield
    content_loader._SEEN_IDS.clear()


def load_one(monkeypatch, record):
    captured = []
    monkeypatch.setattr(content_loader, "_load_file", lambda _path: record)
    monkeypatch.setattr(content_loader, "insert_question", lambda item: captured.append(item))
    result = content_loader.load_content_file("candidate.json")
    assert result["inserted"] == 1
    assert captured
    return captured[0], result


def test_metadata_only_human_reviewed_label_is_not_trusted(monkeypatch):
    doc, result = load_one(monkeypatch, {
        "topic": "percentages",
        "trust_status": "human_reviewed",
        "source": "bountycode_original",
        "questions": [{"id": "trust-test-1", "question": "Original item"}],
    })

    assert doc["trust_status"] == "unverified"
    assert result["untrusted"] == 1


def test_reviewed_requires_human_reviewer_and_approved_decision(monkeypatch):
    doc, result = load_one(monkeypatch, {
        "topic": "reasoning",
        "trust_status": "human_reviewed",
        "review_evidence": {
            "reviewer": "human:content-reviewer",
            "reviewed_at": "2026-11-10T10:00:00Z",
            "decision": "approved",
        },
        "questions": [{"id": "trust-test-2", "question": "Reviewed item"}],
    })

    assert doc["trust_status"] == "reviewed"
    assert result["untrusted"] == 0


def test_verified_requires_both_human_review_and_independent_validation(monkeypatch):
    doc, result = load_one(monkeypatch, {
        "topic": "coding",
        "trust_status": "verified",
        "review_evidence": {
            "reviewer": "human:content-reviewer",
            "reviewed_at": "2026-11-10T10:00:00Z",
            "decision": "approved",
        },
        "verification_evidence": {
            "status": "passed",
            "method": "independent_expected_output_and_edge_case_review",
            "checked_at": "2026-11-10T11:00:00Z",
            "evidence_id": "review-run-001",
        },
        "questions": [{"id": "trust-test-3", "question": "Verified item"}],
    })

    assert doc["trust_status"] == "verified"
    assert result["untrusted"] == 0


def test_verified_label_without_validation_is_quarantined(monkeypatch):
    doc, _ = load_one(monkeypatch, {
        "topic": "coding",
        "trust_status": "verified",
        "review_evidence": {
            "reviewer": "human:content-reviewer",
            "reviewed_at": "2026-11-10T10:00:00Z",
            "decision": "approved",
        },
        "questions": [{"id": "trust-test-4", "question": "Not independently validated"}],
    })

    assert doc["trust_status"] == "unverified"


def test_missing_provenance_is_not_fabricated(monkeypatch):
    doc, _ = load_one(monkeypatch, {
        "topic": "verbal",
        "questions": [{"id": "trust-test-5", "question": "Item without source label"}],
    })

    assert doc["source"] == "unspecified"
    assert doc["trust_status"] == "unverified"
