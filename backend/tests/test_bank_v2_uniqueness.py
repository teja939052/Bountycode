"""Uniqueness tests for the v2 banks.

- question text unique across all v2 banks (mirrors the store dedupe key)
- (id) unique (also covered in schema tests; re-asserted here cheaply)
- no v2 question duplicates text already present in legacy verified banks
"""
from __future__ import annotations

import json
import os
from collections import Counter

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

# Legacy verified banks whose text the v2 content must not repeat.
_LEGACY_FILES = [
    "verified_placement_questions.json",
    "sql_practice_bank.json",
    "interview_practice_bank.json",
    "india_placement_depth.json",
    "system_design_bank.json",
    "debugging_bank.json",
]


def _texts(name: str) -> list[str]:
    path = os.path.join(_DATA_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [str(q.get("question") or q.get("title") or "") for q in data if isinstance(q, dict)]


def test_question_text_unique_within_v2():
    texts = []
    for name in _V2_FILES:
        texts.extend(_texts(name))
    counts = Counter(texts)
    dupes = [t for t, c in counts.items() if c > 1 and t.strip()]
    assert not dupes, f"{len(dupes)} duplicate v2 question texts, e.g. {[d[:80] for d in dupes[:3]]}"


def test_v2_text_does_not_repeat_legacy_banks():
    legacy: set[str] = set()
    for name in _LEGACY_FILES:
        path = os.path.join(_DATA_DIR, name)
        if os.path.exists(path):
            legacy.update(_texts(name))
    collisions = []
    for name in _V2_FILES:
        for t in _texts(name):
            if t.strip() and t in legacy:
                collisions.append((name, t[:80]))
    assert not collisions, f"{len(collisions)} v2 texts collide with legacy, e.g. {collisions[:3]}"


def test_v2_files_all_nonempty_and_list_shaped():
    for name in _V2_FILES:
        texts = _texts(name)
        assert texts, f"{name} has no question texts"
        empty = sum(1 for t in texts if not t.strip())
        assert empty == 0, f"{name} has {empty} empty question texts"
