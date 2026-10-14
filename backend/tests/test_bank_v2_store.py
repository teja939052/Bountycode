"""Integration tests: v2 banks inside question_store.

- store loads with v2 banks wired in
- sampled v2 ids are retrievable and servable
- per-type totals meet doubled minimums through the store's own counters
- MCQ grading accepts the stored correct answer and rejects a wrong one
- interviewed/system-design samples expose rubrics
"""
from __future__ import annotations

import pytest

from app.services.question_store import (
    _is_servable,
    count_documents,
    find_one,
    get_question_for_serving,
    load_all,
)


@pytest.fixture(scope="module")
def store():
    load_all()
    from app.services import question_store as qs

    return qs


_DOUBLED = {
    "coding": 20362,
    "aptitude": 11248,
    "verbal": 3786,
    "reasoning": 3050,
    "written_communication": 2440,
    "sql": 1876,
    "logical": 1794,
    "cs_fundamentals": 448,
    "interview": 306,
    "debugging": 266,
    "system_design": 48,
    "pseudocode": 20,
    "puzzle": 20,
    "cs": 20,
    "mcq": 18,
}


def test_store_loads_v2_volume(store):
    assert len(store._questions) >= 44000, len(store._questions)


@pytest.mark.parametrize("qtype,minimum", sorted(_DOUBLED.items()))
def test_store_type_totals_doubled(store, qtype, minimum):
    n = sum(1 for q in store._questions if q.get("type") == qtype)
    assert n >= minimum, f"{qtype}: {n} < {minimum}"


def test_sampled_v2_ids_retrievable_and_servable(store):
    sample_ids = [
        "log-v2-0001",
        "rsn-v2-0001",
        "sql-v2-0001",
        "dbg-v2-001",
        "csf-v2-g001",
        "verb-v2-0001",
        "int-v2-t001",
        "sd-v2-001",
        "pz-v2-001",
        "cs-v2-001",
        "mcq-v2-001",
    ]
    for qid in sample_ids:
        q = find_one({"id": qid}, allow_unverified=True)
        assert q is not None, f"{qid} not in store"
        assert _is_servable(q), f"{qid} not servable (status={q.get('trust_status')})"


def test_sql_section_now_servable(store):
    n = count_documents({"type": "sql"})
    assert n >= 938, f"servable sql {n} < 938 (section was 0 before v2)"


def test_mcq_grading_on_v2_samples():
    from app.routes.repair import _grade_mcq

    for qid in ("log-v2-0001", "verb-v2-0001", "csf-v2-g001"):
        q = find_one({"id": qid}, allow_unverified=True)
        assert q is not None, qid
        correct = q.get("correct_answer") or q.get("correct_index")
        assert _grade_mcq(q, correct) is True, f"correct rejected for {qid}"
        assert _grade_mcq(q, "ZZZ_WRONG_ANSWER") is False, f"wrong accepted for {qid}"


def test_interview_and_system_design_expose_rubrics():
    iv = find_one({"id": "int-v2-t001"}, allow_unverified=True)
    assert iv and (iv.get("rubric") or iv.get("evaluation_criteria") or iv.get("worked_solution"))
    sd = find_one({"id": "sd-v2-001"}, allow_unverified=True)
    assert sd and sd.get("rubric"), "sd-v2-001 missing rubric"


def test_serving_endpoint_shape_for_v2_coding():
    q = get_question_for_serving("code-v2-00001")
    assert q is not None
    assert q.get("trust_status") in ("verified", "reviewed")
