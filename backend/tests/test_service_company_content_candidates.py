"""The new service-company content is editorial-only until reviewed."""
from __future__ import annotations

import json
from pathlib import Path


DATA_ROOT = Path(__file__).resolve().parents[1] / "app" / "data"
CANDIDATE_FILE = DATA_ROOT / "candidates" / "service_company_patterns_v1.json"
CONTENT_ROOT = DATA_ROOT / "content"
LESSONS_ROOT = DATA_ROOT / "lessons"


def load_pack():
    return json.loads(CANDIDATE_FILE.read_text(encoding="utf-8"))


def test_candidate_pack_is_not_registered_for_student_serving():
    pack = load_pack()

    assert pack["status"] == "candidate_unverified"
    assert pack["publication_policy"]["student_serving"] is False
    assert CANDIDATE_FILE.parent != CONTENT_ROOT
    assert CANDIDATE_FILE.parent != LESSONS_ROOT
    assert CONTENT_ROOT not in CANDIDATE_FILE.parents
    assert LESSONS_ROOT not in CANDIDATE_FILE.parents

    from app.services import question_store

    registered_banks = (
        question_store.VERIFIED_EXTRA_BANKS
        + question_store.UNVERIFIED_EXTRA_BANKS
        + question_store.AUTO_CHECKED_BANKS
    )
    assert all("service_company_patterns_v1.json" not in item for item in registered_banks)


def test_every_candidate_has_stable_identity_and_unverified_provenance():
    pack = load_pack()
    items = pack["items"]
    ids = [item["id"] for item in items]

    assert len(items) >= 17
    assert len(ids) == len(set(ids))

    for item in items:
        assert item["id"].startswith("svc-")
        assert item["meta"]["authored_by"].startswith("ai:")
        assert item["meta"]["status"] == "draft"
        assert item["meta"]["publishable"] is False
        assert item["meta"]["overall_quality"] == 0
        assert item["career"]["provenance"]["level"] == "synthetic"
        assert "not" in item["career"]["provenance"]["note"].lower() or "original" in item["career"]["provenance"]["note"].lower()
        assert item["learning"]["learning_objective"]
        assert len(item["learning"]["real_world"]) >= 2
        assert len(item["reasoning"]["recognition_signals"]) >= 2
        assert item["reasoning"]["anti_patterns"]
        assert len(item["reasoning"]["tradeoffs"]) >= 2
        assert len(item["assistance"]["hint_1"]) >= 30
        assert len(item["assistance"]["hint_2"]) >= 30
        assert len(item["assistance"]["hint_3"]) >= 30
        assert item["assessment"]["test_cases"]
        assert item["solution"]
        assert item["assessment"]["constraints"]
        assert item["assessment"]["rubric"]
        assert item["career"]["roles"]
        assert item["career"]["companies"]
        assert item["career"]["placement_stage"]
        assert item["progression"]["mastery_skill"]
        assert item["progression"]["world"]
        assert item["meta"]["version"] == 1


def test_candidate_pack_covers_the_major_service_company_skill_domains():
    items = load_pack()["items"]
    domains = {tag for item in items for tag in item["meta"]["tags"]}

    assert any("quantitative_aptitude" in tag or "percentages" in tag for tag in domains)
    assert "data_interpretation" in domains
    assert "logical_reasoning" in domains
    assert "verbal" in domains
    assert "pseudocode" in domains
    assert "coding" in domains
    assert "technical_interview" in domains


def test_deterministic_candidate_answers_and_examples_are_consistent():
    items = {item["id"]: item for item in load_pack()["items"]}

    assert items["svc-quant-successive-change-001"]["solution"]["final_amount"] == "₹100,800"
    assert items["svc-quant-work-rate-001"]["solution"]["duration_days"] == 7.2
    assert items["svc-pseudo-nested-loop-001"]["solution"]["output"] == 18
    assert items["svc-coding-first-unique-001"]["solution"]["algorithm"][-1].startswith("Return")


def test_candidate_provenance_never_claims_exact_company_questions():
    for item in load_pack()["items"]:
        note = item["career"]["provenance"]["note"].lower()
        assert "not" in note or "original" in note
