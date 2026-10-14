"""Verification tests for bulk-added verified company questions.

Validates:
- File counts by section meet minimums
- New questions have required MCQ fields
- question_store loads them without error
- MCQ grading works on new questions
"""
from __future__ import annotations

import json
import os

import pytest

from app.services.question_store import load_all, find, find_one

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")

_COMPANY_FILES = {
    "cognizant": "cognizant_genc_verified.json",
    "wipro": "wipro_nlth_verified.json",
    "capgemini": "capgemini_accenture_verified.json",
    "infosys": "infosys_infytq_verified.json",
    "tcs": "tcs_nqt_coding_verified.json",
    "tcs_codevita": "tcs_codevita_verified.json",
    "tech_mahindra": "tech_mahindra_verified.json",
    "ltimindtree": "ltimindtree_verified.json",
    "hcl": "hcl_verified.json",
}

_MIN_CODING = 300
_MIN_MCQ = 1000
_MIN_PER_SECTION = 300


def _load_file(name: str) -> list[dict]:
    path = os.path.join(_DATA_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_company_files_have_minimum_coding_count():
    totals = {}
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        coding = sum(1 for q in data if q.get("type") == "coding")
        totals[company] = coding
    total_coding = sum(totals.values())
    assert total_coding >= _MIN_CODING, f"total coding {total_coding} < {_MIN_CODING}; per company: {totals}"


def test_company_files_have_minimum_mcq_count():
    mcq_types = {"aptitude", "verbal", "reasoning", "pseudocode", "puzzle", "written_communication"}
    totals = {}
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        mcqs = [q for q in data if q.get("type") in mcq_types]
        totals[company] = len(mcqs)
    total_mcqs = sum(totals.values())
    assert total_mcqs >= _MIN_MCQ, f"total mcqs {total_mcqs} < {_MIN_MCQ}; per company: {totals}"


def test_per_section_counts_meet_minimum():
    mcq_types = {"aptitude", "verbal", "reasoning", "pseudocode", "puzzle", "written_communication"}
    section_totals = {}
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        for q in data:
            t = q.get("type", "")
            if t in mcq_types:
                section_totals[t] = section_totals.get(t, 0) + 1
    for section, count in section_totals.items():
        if section in {"pseudocode", "puzzle"}:
            assert count >= 10, f"section {section} has {count} < 10"
        else:
            assert count >= _MIN_PER_SECTION, f"section {section} has {count} < {_MIN_PER_SECTION}"


def test_new_questions_have_required_mcq_fields():
    mcq_types = {"aptitude", "verbal", "reasoning", "pseudocode", "puzzle", "written_communication"}
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        mcqs = [q for q in data if q.get("type") in mcq_types and q.get("options")]
        assert mcqs, f"no mcqs with options found in {filename}"
        bad = [q.get("id") for q in mcqs if not q.get("correct_answer")]
        assert not bad, f"{len(bad)} mcqs missing correct_answer in {filename}: {bad[:5]}"


def test_new_questions_have_verified_trust_status():
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        bad = [q.get("id") for q in data if q.get("trust_status") != "verified"]
        assert not bad, f"{len(bad)} questions not verified in {filename}: {bad[:5]}"


def test_question_store_loads_company_banks():
    load_all()
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        # Check last 10 questions (newly added ones) to avoid pre-existing
        # cross-file title collisions that get deduplicated by question_store.
        for q in data[-10:]:
            loaded = find_one({"id": q["id"]}, allow_unverified=True)
            assert loaded, f"question_store missing {q['id']} from {filename}"


def test_mcq_grading_returns_true_for_correct_answer():
    from app.routes.repair import _grade_mcq
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        mcqs = [q for q in data if q.get("type") in {"aptitude", "verbal", "reasoning"} and q.get("correct_answer")]
        assert mcqs, f"no gradable mcqs in {filename}"
        sample = mcqs[0]
        correct = sample.get("correct_answer")
        assert _grade_mcq(sample, correct) is True, f"correct answer failed for {sample['id']}"


def test_mcq_grading_returns_false_for_wrong_answer():
    from app.routes.repair import _grade_mcq
    for company, filename in _COMPANY_FILES.items():
        data = _load_file(filename)
        mcqs = [q for q in data if q.get("type") in {"aptitude", "verbal", "reasoning"} and q.get("correct_answer")]
        assert mcqs, f"no gradable mcqs in {filename}"
        sample = mcqs[0]
        wrong = "ZZZ_WRONG_ANSWER"
        assert _grade_mcq(sample, wrong) is False, f"wrong answer passed for {sample['id']}"
