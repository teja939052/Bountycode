import json
from pathlib import Path

from app.services import question_store


def test_verified_placeholder_options_are_repaired_without_trust_promotion(tmp_path, monkeypatch):
    data_dir = tmp_path / "app" / "data"
    data_dir.mkdir(parents=True)
    payload = {
        "version": 1,
        "source_bank": "verified_placement_questions.json",
        "items": [{
            "id": "apt-001",
            "type": "aptitude",
            "options": ["10", "20", "30", "40"],
            "correct_index": 2,
            "correct_answer": "30",
        }],
        "demote_ids": [],
    }
    (data_dir / "verified_mcq_option_overrides.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(question_store, "_BACKEND_ROOT", str(tmp_path))
    questions = [{
        "id": "apt-001", "type": "aptitude", "trust_status": "verified",
        "options": {"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
    }]
    question_store._apply_mcq_option_overrides(questions)
    assert questions[0]["options"] == ["10", "20", "30", "40"]
    assert questions[0]["correct_index"] == 2
    assert questions[0]["correct_answer"] == "30"
    assert questions[0]["trust_status"] == "verified"


def test_unverified_question_is_never_changed_or_promoted(tmp_path, monkeypatch):
    data_dir = tmp_path / "app" / "data"
    data_dir.mkdir(parents=True)
    payload = {
        "version": 1, "source_bank": "verified_placement_questions.json",
        "items": [{
            "id": "apt-002", "type": "aptitude",
            "options": ["1", "2", "3", "4"], "correct_index": 0, "correct_answer": "1",
        }],
        "demote_ids": [],
    }
    (data_dir / "verified_mcq_option_overrides.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(question_store, "_BACKEND_ROOT", str(tmp_path))
    questions = [{
        "id": "apt-002", "type": "aptitude", "trust_status": "unverified",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    }]
    question_store._apply_mcq_option_overrides(questions)
    assert questions[0]["options"] == ["Option 1", "Option 2", "Option 3", "Option 4"]
    assert questions[0]["trust_status"] == "unverified"


def test_verified_placeholder_without_source_is_demoted(tmp_path, monkeypatch):
    data_dir = tmp_path / "app" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "verified_mcq_option_overrides.json").write_text(json.dumps({
        "version": 1, "items": [], "demote_ids": ["apt-003"],
    }), encoding="utf-8")
    monkeypatch.setattr(question_store, "_BACKEND_ROOT", str(tmp_path))
    questions = [{
        "id": "apt-003", "type": "aptitude", "trust_status": "verified",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    }]
    question_store._apply_mcq_option_overrides(questions)
    assert questions[0]["trust_status"] == "needs_review"
