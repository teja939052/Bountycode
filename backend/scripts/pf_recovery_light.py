"""
Lightweight Programming Foundations recovery classification.
Uses already-loaded question store data for fast classification.
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


def _is_pf_question(q: Dict[str, Any]) -> bool:
    qtype = str(q.get("type", "")).lower()
    topic = str(q.get("topic", "")).lower()
    sub = str(q.get("sub_topic", "")).lower()
    title = str(q.get("question") or q.get("title") or "").lower()

    pf_types = {"cs", "cs_fundamentals"}
    pf_topics = {"programming", "programming foundations", "code foundations",
                 "variables", "types", "conditions", "loops", "functions",
                 "strings", "data structures", "exceptions", "input output",
                 "error handling", "debugging", "testing", "git", "http",
                 "apis", "logging", "error analysis", "modules", "files"}

    if qtype in pf_types:
        return True
    if any(t in topic for t in pf_topics):
        return True
    if any(t in sub for t in pf_topics):
        return True
    if "foundation" in title or "programming" in title:
        return True
    return False


def main() -> None:
    print("Loading question store...")
    question_store.load_all()
    questions = list(question_store._questions)
    print(f"Total loaded: {len(questions)}")

    # Find duplicates across all questions
    title_groups: Dict[str, List[str]] = defaultdict(list)
    for q in questions:
        title = str(q.get("question") or q.get("title") or "")
        norm = "".join(c for c in title.lower() if c.isalnum())[:60]
        if norm:
            title_groups[norm].append(str(q.get("id", "")))
    duplicate_ids = set()
    for ids in title_groups.values():
        if len(ids) >= 2:
            duplicate_ids.update(ids)

    # Filter PF questions
    pf_questions = [q for q in questions if _is_pf_question(q)]
    print(f"PF questions found: {len(pf_questions)}")

    # Classify
    classifications = []
    for q in pf_questions:
        qid = str(q.get("id", ""))
        qtype = str(q.get("type", "")).lower()
        trust = str(q.get("trust_status", "unverified")).lower()
        title = str(q.get("question") or q.get("title") or "").strip()

        struct = validate_structure(q)
        correctness = validate_answer_correctness(q)
        exec_r = validate_executability(q)
        score_result = score_question(q)

        reasons: List[str] = []
        classification = "Quarantine"

        blob = f"{title} {q.get('description', '')} {q.get('explanation', '')}".lower()
        is_placeholder = any(p in blob for p in [
            "implement optimal solution here", "implement your solution here",
            "todo: implement", "placeholder", "lorem ipsum", "coming soon",
        ])
        is_empty = len(title) < 10 and not q.get("explanation") and not q.get("solution")

        if is_placeholder or is_empty:
            classification = "Quarantine"
            reasons.append("placeholder_or_empty_content")
        elif trust == "quarantined":
            classification = "Quarantine"
            reasons.append("already_quarantined")
        elif not struct["all_required_present"]:
            if correctness["automatable"] and correctness["score"] == 100:
                classification = "Requires repair"
                reasons.append("missing_required_fields")
            elif not correctness["automatable"]:
                classification = "Requires review"
                reasons.append("missing_required_fields_and_correctness_not_automatable")
            else:
                classification = "Requires repair"
                reasons.append("missing_required_fields")
        elif not exec_r["executable"]:
            classification = "Requires repair"
            reasons.append("not_executable")
        elif correctness["automatable"] and correctness["score"] < 100:
            classification = "Requires repair"
            reasons.append("incorrect_answer")
        elif not correctness["automatable"]:
            if trust in ("verified", "reviewed"):
                classification = "Recoverable"
                reasons.append("human_reviewed_and_structurally_complete")
            else:
                classification = "Requires review"
                reasons.append("correctness_not_automatable_not_human_reviewed")
        elif trust in ("verified", "reviewed"):
            classification = "Recoverable"
            reasons.append("structurally_complete_correct_human_reviewed")
        elif trust == "automated_checked":
            classification = "Requires review"
            reasons.append("automated_checked_needs_human_review")
        else:
            classification = "Requires review"
            reasons.append("unverified_needs_review")

        if qid in duplicate_ids:
            if classification == "Quarantine":
                reasons.append("duplicate")
            else:
                classification = "Duplicate"
                reasons.append("duplicate_title")

        classifications.append({
            "id": qid,
            "type": qtype,
            "topic": q.get("topic"),
            "title": title[:80],
            "trust": trust,
            "tier": score_result["quality_tier"],
            "classification": classification,
            "reasons": reasons,
            "structural_completeness": struct["score"],
            "answer_correctness": correctness["score"] if correctness["automatable"] else None,
            "executability": exec_r["score"],
        })

    # Summary
    class_counts = Counter(c["classification"] for c in classifications)
    print("\n" + "=" * 60)
    print("PROGRAMMING FOUNDATIONS RECOVERY CLASSIFICATION")
    print("=" * 60)
    print(f"Total PF questions: {len(pf_questions)}")
    print()
    for cls, count in sorted(class_counts.items()):
        print(f"  {cls:20s}: {count}")

    recoverable = [c for c in classifications if c["classification"] == "Recoverable"]
    repair = [c for c in classifications if c["classification"] == "Requires repair"]
    review = [c for c in classifications if c["classification"] == "Requires review"]
    dupes = [c for c in classifications if c["classification"] == "Duplicate"]
    quarantine = [c for c in classifications if c["classification"] == "Quarantine"]

    print(f"\n  Recoverable: {len(recoverable)}")
    print(f"  Requires repair: {len(repair)}")
    print(f"  Requires review: {len(review)}")
    print(f"  Duplicate: {len(dupes)}")
    print(f"  Quarantine: {len(quarantine)}")

    # Write report
    os.makedirs(REPORT_DIR, exist_ok=True)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_pf_questions": len(pf_questions),
        "classification_counts": dict(class_counts),
        "recoverable_ids": [c["id"] for c in recoverable],
        "requires_repair_ids": [c["id"] for c in repair],
        "requires_review_ids": [c["id"] for c in review],
        "duplicate_ids": [c["id"] for c in dupes],
        "quarantine_ids": [c["id"] for c in quarantine],
        "classifications": classifications,
    }
    path = os.path.join(REPORT_DIR, "programming_foundations_recovery.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to: {path}")
    print("\nNOTE: No questions were promoted or modified. This is a report only.")


if __name__ == "__main__":
    main()
