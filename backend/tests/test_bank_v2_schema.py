"""Schema validation for every question in the v2 banks.

Type-specific rules mirror `question_store._is_executable` plus structural
requirements (options shape, test-case shape, required grading fields).
File-level only (no question_store load) so it stays fast.
"""
from __future__ import annotations

import json
import os

import pytest

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")

_V2_FILES = [
    "bank_thin_v2.json",
    "bank_debugging_v2.json",
    "bank_interview_v2.json",
    "bank_csfund_v2.json",
    "bank_logical_v2.json",
    "bank_reasoning_v2.json",
    "bank_sql_v2.json",
    "bank_written_v2.json",
    "bank_verbal_v2.json",
    "bank_aptitude_v2.json",
    "bank_coding_v2.json",
]

_MCQ_TYPES = {"aptitude", "logical", "verbal", "cs_fundamentals", "cs"}


def _load_all_v2() -> list[dict]:
    out = []
    for name in _V2_FILES:
        path = os.path.join(_DATA_DIR, name)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for q in data:
            q["_file"] = name
            out.append(q)
    return out


_ALL_V2 = None


def _v2():
    global _ALL_V2
    if _ALL_V2 is None:
        _ALL_V2 = _load_all_v2()
    return _ALL_V2


def test_mcq_options_and_answer_valid():
    bad = []
    for q in _v2():
        if q.get("type") not in _MCQ_TYPES:
            continue
        opts = q.get("options")
        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
        if isinstance(opts, dict):
            if len(opts) < 4 or correct not in ("A", "B", "C", "D"):
                bad.append(q["id"])
            elif correct not in [str(k).upper() for k in opts]:
                bad.append(q["id"])
        elif isinstance(opts, list):
            if len(opts) < 4:
                bad.append(q["id"])
                continue
            ci = q.get("correct_index")
            ok_idx = isinstance(ci, int) and 0 <= ci < len(opts)
            ok_text = str(q.get("correct_answer") or "").strip() in [str(o).strip() for o in opts]
            if not (ok_idx or ok_text):
                bad.append(q["id"])
        else:
            bad.append(q["id"])
    assert not bad, f"{len(bad)} MCQ schema failures, e.g. {bad[:5]}"


def test_coding_has_solution_and_testcases():
    bad = []
    for q in _v2():
        if q.get("type") != "coding":
            continue
        tcs = q.get("test_cases") or q.get("testcases") or []
        sol = (q.get("solution") or {}).get("code") if isinstance(q.get("solution"), dict) else q.get("solution")
        if not tcs or not sol:
            bad.append(q["id"])
            continue
        for tc in tcs:
            if "expected" not in tc and "output" not in tc:
                bad.append(q["id"])
                break
    assert not bad, f"{len(bad)} coding schema failures, e.g. {bad[:5]}"


def test_sql_has_schema_and_testcases():
    bad = []
    for q in _v2():
        if q.get("type") != "sql":
            continue
        if not q.get("sql_schema"):
            bad.append((q["id"], "no sql_schema"))
            continue
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not tcs:
            bad.append((q["id"], "no test_cases"))
            continue
        if not (q.get("correct_answer") or q.get("correct_query")):
            bad.append((q["id"], "no reference query"))
    assert not bad, f"{len(bad)} sql schema failures, e.g. {bad[:5]}"


def test_debugging_has_buggy_and_fixed_code():
    bad = []
    for q in _v2():
        if q.get("type") != "debugging":
            continue
        if not q.get("buggy_code") or not q.get("correct_code"):
            bad.append(q["id"])
            continue
        if q.get("buggy_code") == q.get("correct_code"):
            bad.append(q["id"])
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not tcs:
            bad.append(q["id"])
    assert not bad, f"{len(bad)} debugging schema failures, e.g. {bad[:5]}"


def test_interview_has_rubric_or_criteria():
    bad = [
        q["id"]
        for q in _v2()
        if q.get("type") == "interview"
        and not (q.get("rubric") or q.get("evaluation_criteria") or q.get("worked_solution"))
    ]
    assert not bad, f"{len(bad)} interview schema failures, e.g. {bad[:5]}"


def test_system_design_has_rubric():
    bad = [q["id"] for q in _v2() if q.get("type") == "system_design" and not q.get("rubric")]
    assert not bad, f"{len(bad)} system_design missing rubric, e.g. {bad[:5]}"


def test_reasoning_and_written_have_list_options():
    bad = []
    for q in _v2():
        if q.get("type") not in ("reasoning", "written_communication"):
            continue
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) < 4:
            bad.append(q["id"])
        elif str(q.get("correct_answer") or "") not in [str(o) for o in opts]:
            bad.append(q["id"])
    assert not bad, f"{len(bad)} reasoning/written schema failures, e.g. {bad[:5]}"


def test_ids_unique_within_v2_banks():
    seen: dict = {}
    dupes = []
    for q in _v2():
        qid = q.get("id")
        if qid in seen:
            dupes.append(qid)
        seen[qid] = q["_file"]
    assert not dupes, f"{len(dupes)} duplicate ids, e.g. {dupes[:5]}"
