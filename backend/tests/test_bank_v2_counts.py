"""Doubling / volume tests for the v2 question-bank expansion.

Asserts every section meets its doubled minimum:
- per-file minimums for each bank_thin/debugging/... bank file
- per-type totals across the whole data dir meet 2x the pre-expansion baseline
"""
from __future__ import annotations

import json
import os

import pytest

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")

# Minimum items each v2 bank file must hold (the doubling deltas).
_FILE_MINIMUMS = {
    "bank_thin_v2.json": 63,
    "bank_debugging_v2.json": 133,
    "bank_interview_v2.json": 157,  # 153 + 4 top-up
    "bank_csfund_v2.json": 225,  # 224 + 1 top-up
    "bank_logical_v2.json": 897,
    "bank_reasoning_v2.json": 1525,
    "bank_sql_v2.json": 938,
    "bank_written_v2.json": 1220,
    "bank_verbal_v2.json": 1893,
    "bank_aptitude_v2.json": 5624,
    "bank_coding_v2.json": 10181,
}

# Pre-expansion (post-dedupe) baselines per type -> doubled minimums.
_TYPE_DOUBLED_MINIMUMS = {
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


def _load_bank(name: str) -> list:
    path = os.path.join(_DATA_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list), f"{name} is not a JSON list"
    return data


@pytest.mark.parametrize("filename,minimum", sorted(_FILE_MINIMUMS.items()))
def test_v2_bank_file_meets_minimum(filename, minimum):
    assert os.path.exists(os.path.join(_DATA_DIR, filename)), f"missing {filename}"
    data = _load_bank(filename)
    assert len(data) >= minimum, f"{filename}: {len(data)} < {minimum}"


def test_all_v2_questions_marked_verified():
    for filename in _FILE_MINIMUMS:
        data = _load_bank(filename)
        bad = [q.get("id") for q in data if q.get("trust_status") != "verified"]
        assert not bad, f"{filename}: {len(bad)} not verified, e.g. {bad[:3]}"


def test_all_v2_questions_have_ids_and_types():
    for filename in _FILE_MINIMUMS:
        data = _load_bank(filename)
        for q in data:
            assert q.get("id"), f"{filename}: question missing id"
            assert q.get("type"), f"{filename}: {q.get('id')} missing type"
            assert q.get("question") or q.get("title"), f"{filename}: {q.get('id')} missing text"


def test_per_type_totals_meet_doubled_minimums():
    from collections import Counter

    totals: Counter = Counter()
    for fname in os.listdir(_DATA_DIR):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(_DATA_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        for q in data:
            if isinstance(q, dict) and q.get("type"):
                totals[q["type"]] += 1
    for qtype, minimum in sorted(_TYPE_DOUBLED_MINIMUMS.items()):
        assert totals.get(qtype, 0) >= minimum, (
            f"type {qtype}: {totals.get(qtype, 0)} < doubled minimum {minimum}"
        )
