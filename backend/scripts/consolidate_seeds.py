"""Consolidate all 17 Python seed files into a single JSON bank.

Usage:
    python -m scripts.consolidate_seeds
    # or
    python scripts/consolidate_seeds.py

Reads each seed file's ``questions`` list, merges them, deduplicates by id,
and writes the result to ``app/data/questions_bank.json``.

The JSON bank is loaded by ``app.services.question_store`` at startup for
faster cold starts (single file read vs. 17 importlib calls).
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import importlib.util
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


class _SafeEncoder(json.JSONEncoder):
    """Handle datetime and other non-serialisable objects by converting to str."""

    def default(self, o):
        if isinstance(o, (_dt.datetime, _dt.date)):
            return o.isoformat()
        if isinstance(o, set):
            return sorted(o)
        return super().default(o)

# ---------------------------------------------------------------------------
# Configuration — the 17 seed files in the same order question_store loads them
# ---------------------------------------------------------------------------
BACKEND_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BACKEND_DIR / "app" / "data"
OUTPUT_FILE = OUTPUT_DIR / "questions_bank.json"

SEED_FILES: list[str] = [
    "seed_questions_mega.py",
    "seed_questions_v2.py",
    "seed_questions_2000.py",
    "seed_questions.py",
    "seed_questions_extra.py",
    "seed_questions_faang.py",
    "seed_questions_500.py",
    "seed_questions_500_more.py",
    "seed_questions_300_more.py",
    "seed_questions_500_plus_2.py",
    "seed_questions_500_plus_3.py",
    "seed_questions_graph_dp.py",
    "massive_questions.py",
    "seed_questions_striver.py",
    "seed_questions_blind75.py",
    "seed_questions_neetcode150.py",
    "seed_questions_leetcode_extra.py",
]


def _load_questions_from_file(filepath: str) -> list[dict]:
    """Import a Python file and extract its ``questions`` variable."""
    try:
        spec = importlib.util.spec_from_file_location("_seed_mod", filepath)
        if not spec or not spec.loader:
            print(f"  SKIP  Could not create spec for {os.path.basename(filepath)}")
            return []
        mod = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(None):
            spec.loader.exec_module(mod)

        data = getattr(mod, "questions", None)
        if isinstance(data, list):
            return data
        # Some files expose a dict of lists
        if isinstance(data, dict):
            merged: list[dict] = []
            for v in data.values():
                if isinstance(v, list):
                    merged.extend(v)
            return merged
        print(f"  WARN  No 'questions' list in {os.path.basename(filepath)}")
        return []
    except Exception as exc:
        print(f"  ERROR Failed to load {os.path.basename(filepath)}: {exc}")
        return []


def _normalize_id(q: dict, fallback_idx: int) -> str:
    """Return a stable string id for a question."""
    if "_id" in q:
        return str(q.pop("_id"))
    if "id" in q:
        return str(q["id"])
    return f"q_{fallback_idx:06d}"


def _dedupe_by_id(questions: list[dict]) -> list[dict]:
    """Keep the first occurrence of each id (higher quality wins)."""
    seen: dict[str, dict] = {}
    for q in questions:
        qid = q.get("id", "")
        if qid in seen:
            # Keep whichever has more content (simple heuristic)
            existing = seen[qid]
            existing_score = sum(1 for k in ("testcases", "solution", "examples", "hints") if existing.get(k))
            new_score = sum(1 for k in ("testcases", "solution", "examples", "hints") if q.get(k))
            if new_score > existing_score:
                seen[qid] = q
        else:
            seen[qid] = q
    return list(seen.values())


def consolidate() -> None:
    """Main entry point: load all seeds, dedupe, write JSON, print stats."""
    print("=" * 60)
    print("  PlacementPro — Question Bank Consolidation")
    print("=" * 60)

    all_questions: list[dict] = []
    per_source: dict[str, int] = {}
    load_errors: list[str] = []

    for seed_file in SEED_FILES:
        filepath = str(BACKEND_DIR / seed_file)
        if not os.path.exists(filepath):
            print(f"  MISSING  {seed_file}")
            load_errors.append(seed_file)
            continue

        items = _load_questions_from_file(filepath)
        per_source[seed_file] = len(items)

        # Assign ids before merging
        for i, q in enumerate(items):
            if isinstance(q, dict):
                q["id"] = _normalize_id(q, len(all_questions) + i)
                all_questions.append(q)

        print(f"  OK  {seed_file:45s}  {len(items):>5d} questions")

    print("-" * 60)
    print(f"  Raw total before dedup: {len(all_questions)}")

    # Deduplicate by id
    deduped = _dedupe_by_id(all_questions)
    print(f"  After id dedup:         {len(deduped)}")

    # Stats by difficulty
    diff_counts: Counter = Counter(q.get("difficulty", "unknown") for q in deduped)
    # Stats by type
    type_counts: Counter = Counter(q.get("type", "unknown") for q in deduped)
    # Stats by topic (top 20)
    topic_counts: Counter = Counter(q.get("topic", "General") for q in deduped)

    # Write JSON
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=None, separators=(",", ":"), cls=_SafeEncoder)

    file_size = OUTPUT_FILE.stat().st_size
    print("-" * 60)
    print(f"  Written to: {OUTPUT_FILE}")
    print(f"  File size:  {file_size / (1024 * 1024):.1f} MB")
    print(f"  Questions:  {len(deduped)}")
    print()
    print("  Per-source counts:")
    for src, cnt in per_source.items():
        print(f"    {src:45s}  {cnt:>5d}")
    if load_errors:
        print(f"    {'MISSING/ERROR':45s}  {len(load_errors):>5d}")
    print()
    print("  Per-difficulty:")
    for diff, cnt in sorted(diff_counts.items()):
        print(f"    {diff:15s}  {cnt:>5d}")
    print()
    print("  Per-type:")
    for tp, cnt in sorted(type_counts.items()):
        print(f"    {tp:15s}  {cnt:>5d}")
    print()
    print("  Top 20 topics:")
    for topic, cnt in topic_counts.most_common(20):
        print(f"    {topic:30s}  {cnt:>5d}")
    print()
    print("  DONE")


if __name__ == "__main__":
    consolidate()
