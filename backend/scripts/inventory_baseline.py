"""
Lightweight inventory validation — gets baseline counts from the runtime
question store without per-question code execution (which is slow).
"""

from __future__ import annotations

import json
import logging
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

logging.disable(logging.CRITICAL)

from app.services import question_store
from app.services.question_quality import (
    validate_structure,
    validate_answer_correctness,
    validate_executability,
    score_question,
)

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BACKEND_ROOT, "app", "data", "quality_reports")


def main() -> None:
    print("Loading question store...")
    question_store.load_all()
    questions = list(question_store._questions)
    print(f"Total loaded records: {len(questions)}")

    # Trust breakdown
    trust = Counter(str(q.get("trust_status", "unverified")).lower() for q in questions)
    print(f"\nTrust breakdown: {dict(trust)}")

    # Type breakdown
    types = Counter(str(q.get("type", "coding")).lower() for q in questions)
    print(f"\nType breakdown: {dict(types)}")

    # Servable count
    servable = [q for q in questions if question_store._is_servable(q)]
    print(f"\nServable count: {len(servable)}")
    print(f"Servable rate: {len(servable) / len(questions) * 100:.1f}%")

    # Servable by trust
    servable_trust = Counter(str(q.get("trust_status", "unverified")).lower() for q in servable)
    print(f"Servable by trust: {dict(servable_trust)}")

    # Servable by type
    servable_types = Counter(str(q.get("type", "coding")).lower() for q in servable)
    print(f"Servable by type: {dict(servable_types)}")

    # Unique IDs
    ids = [str(q.get("id", "")) for q in questions]
    unique_ids = set(ids)
    print(f"\nUnique canonical question IDs: {len(unique_ids)}")
    print(f"Duplicate ID records: {len(ids) - len(unique_ids)}")

    # Duplicate clusters by normalized title
    title_groups: Dict[str, List[str]] = defaultdict(list)
    for q in questions:
        title = str(q.get("question") or q.get("question_title") or q.get("title") or "")
        norm = "".join(c for c in title.lower() if c.isalnum())[:60]
        if norm:
            title_groups[norm].append(str(q.get("id", "")))
    duplicates = {k: v for k, v in title_groups.items() if len(v) >= 2}
    print(f"\nDuplicate clusters (by normalized title): {len(duplicates)}")
    for norm, ids_list in list(duplicates.items())[:10]:
        print(f"  '{norm}': {len(ids_list)} questions")

    # Structural validation (fast, no code execution)
    print("\n--- Structural validation (sample) ---")
    struct_results = Counter()
    missing_required = Counter()
    for q in questions[:500]:  # Sample first 500 for speed
        struct = validate_structure(q)
        if struct["all_required_present"]:
            struct_results["all_required_present"] += 1
        else:
            struct_results["missing_required"] += 1
        for label in struct["required_missing"]:
            missing_required[label] += 1
    print(f"Sampled 500 questions: {struct_results['all_required_present']} all required present, {struct_results['missing_required']} missing required")
    print(f"Top missing required: {missing_required.most_common(5)}")

    # Executability (fast)
    print("\n--- Executability ---")
    exec_results = Counter()
    for q in questions:
        exec_r = validate_executability(q)
        exec_results["executable" if exec_r["executable"] else "not_executable"] += 1
    print(f"Executable: {exec_results['executable']}, Not executable: {exec_results['not_executable']}")

    # Answer correctness for non-code types (fast)
    print("\n--- Answer correctness (non-code types only) ---")
    correctness_results = Counter()
    for q in questions:
        qtype = str(q.get("type", "")).lower()
        if qtype in ("coding", "sql", "debugging"):
            continue  # Skip code execution in lightweight mode
        correctness = validate_answer_correctness(q)
        if correctness["automatable"]:
            correctness_results["automatable"] += 1
            if correctness["score"] == 100:
                correctness_results["correct"] += 1
            else:
                correctness_results["incorrect"] += 1
        else:
            correctness_results["not_automatable"] += 1
    print(f"Correctness results: {dict(correctness_results)}")

    # Skill mapping gaps
    print("\n--- Skill mapping ---")
    mapped = sum(1 for q in questions if q.get("canonical_skill_id"))
    print(f"Mapped to canonical skill: {mapped}")
    print(f"Unmapped: {len(questions) - mapped}")

    # Write report
    os.makedirs(REPORT_DIR, exist_ok=True)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_loaded": len(questions),
        "unique_ids": len(unique_ids),
        "duplicate_id_records": len(ids) - len(unique_ids),
        "trust_breakdown": dict(trust),
        "type_breakdown": dict(types),
        "servable_count": len(servable),
        "servable_rate": round(len(servable) / len(questions) * 100, 1) if questions else 0,
        "servable_by_trust": dict(servable_trust),
        "servable_by_type": dict(servable_types),
        "duplicate_clusters": len(duplicates),
        "skill_mapped": mapped,
        "skill_unmapped": len(questions) - mapped,
    }
    path = os.path.join(REPORT_DIR, "inventory_baseline.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to: {path}")


if __name__ == "__main__":
    main()
