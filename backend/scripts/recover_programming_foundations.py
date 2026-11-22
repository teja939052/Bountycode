"""
Phase 8 — Programming Foundations recovery classification report.

Investigates raw Programming Foundations questions (type=cs/cs_fundamentals
and topic/foundation-tagged content) and classifies each as:

  - Recoverable      — structurally complete, correct, can be promoted
  - Requires repair  — fixable: incorrect answer, broken solution, missing fields
  - Requires review  — correctness cannot be established automatically
  - Duplicate        — same normalized title as another question
  - Quarantine       — broken beyond repair, placeholder, or invalid

Does NOT automatically promote any question. Produces a report only.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

logging.disable(logging.CRITICAL)

from app.services import question_store
from app.services.question_quality import (
    validate_structure,
    validate_answer_correctness,
    validate_executability,
    assess_quality,
    score_question,
)

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BACKEND_ROOT, "app", "data", "quality_reports")


def _is_pf_question(q: Dict[str, Any]) -> bool:
    """Detect Programming Foundations questions by type and topic."""
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


def classify_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify a single Programming Foundations question.

    Returns a dict with classification and reasons. Never mutates the
    question or changes its trust status.
    """
    qid = str(q.get("id", ""))
    qtype = str(q.get("type", "")).lower()
    trust = str(q.get("trust_status", "unverified")).lower()
    title = str(q.get("question") or q.get("title") or "").strip()

    reasons: List[str] = []
    classification = "Quarantine"

    # Structural validation
    struct = validate_structure(q)
    correctness = validate_answer_correctness(q)
    exec_result = validate_executability(q)
    dims = assess_quality(q)
    score_result = score_question(q)

    # Check for placeholder / template content
    blob = f"{title} {q.get('description','')} {q.get('explanation','')}".lower()
    is_placeholder = any(p in blob for p in [
        "implement optimal solution here",
        "implement your solution here",
        "todo: implement",
        "placeholder",
        "lorem ipsum",
        "coming soon",
    ])
    is_empty = len(title) < 10 and not q.get("explanation") and not q.get("solution")

    # Check for duplicate (will be cross-referenced later)
    # (Duplicate detection done at report level)

    # Determine classification
    if is_placeholder or is_empty:
        classification = "Quarantine"
        reasons.append("placeholder_or_empty_content")
    elif trust == "quarantined":
        classification = "Quarantine"
        reasons.append("already_quarantined")
    elif not struct["all_required_present"]:
        # Missing required fields — could be repairable if the question
        # content itself is sound
        if correctness["automatable"] and correctness["score"] == 100:
            classification = "Requires repair"
            reasons.append("missing_required_fields")
        elif not correctness["automatable"]:
            classification = "Requires review"
            reasons.append("missing_required_fields_and_correctness_not_automatable")
        else:
            classification = "Requires repair"
            reasons.append("missing_required_fields")
    elif not exec_result["executable"]:
        classification = "Requires repair"
        reasons.append("not_executable")
    elif correctness["automatable"] and correctness["score"] < 100:
        classification = "Requires repair"
        reasons.append("incorrect_answer")
    elif not correctness["automatable"]:
        # Correctness not automatable — needs human review
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
        # Automated check passed but not human-reviewed
        if dims.structural_completeness and dims.structural_completeness >= 80:
            classification = "Requires review"
            reasons.append("automated_checked_needs_human_review")
        else:
            classification = "Requires review"
            reasons.append("automated_checked_structural_gaps")
    else:
        # unverified or needs_review
        if dims.structural_completeness and dims.structural_completeness >= 90:
            classification = "Requires review"
            reasons.append("unverified_but_high_structural_completeness")
        else:
            classification = "Requires review"
            reasons.append("unverified_needs_review")

    return {
        "id": qid,
        "type": qtype,
        "topic": q.get("topic"),
        "sub_topic": q.get("sub_topic"),
        "title": title[:100],
        "trust": trust,
        "tier": score_result["quality_tier"],
        "classification": classification,
        "reasons": reasons,
        "structural_completeness": dims.structural_completeness,
        "answer_correctness": correctness["score"] if correctness["automatable"] else None,
        "executability": exec_result["score"],
        "assessment_usefulness": dims.assessment_usefulness,
        "required_missing": struct["required_missing"],
        "automatable_correctness": correctness["automatable"],
        "executable": exec_result["executable"],
    }


def find_duplicates(questions: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Group questions by normalized title for duplicate detection."""
    groups: Dict[str, List[str]] = defaultdict(list)
    for q in questions:
        title = str(q.get("question") or q.get("title") or "")
        norm = "".join(c for c in title.lower() if c.isalnum())[:60]
        if norm:
            groups[norm].append(str(q.get("id", "")))
    return {k: v for k, v in groups.items() if len(v) >= 2}


def main() -> None:
    question_store.load_all()
    all_questions = list(question_store._questions)

    # Filter to Programming Foundations questions
    pf_questions = [q for q in all_questions if _is_pf_question(q)]

    # Find duplicates across the whole bank (PF questions that duplicate others)
    duplicates = find_duplicates(all_questions)
    duplicate_ids = set()
    for ids in duplicates.values():
        duplicate_ids.update(ids)

    # Classify each PF question
    classifications: List[Dict[str, Any]] = []
    for q in pf_questions:
        result = classify_question(q)
        qid = result["id"]
        if qid in duplicate_ids:
            if result["classification"] == "Quarantine":
                result["classification"] = "Quarantine"
                result["reasons"].append("duplicate")
            else:
                result["classification"] = "Duplicate"
                result["reasons"].append("duplicate_title")
        classifications.append(result)

    # Summary counts
    class_counts = Counter(c["classification"] for c in classifications)
    type_counts = Counter(c["type"] for c in classifications)
    trust_counts = Counter(c["trust"] for c in classifications)

    recoverable = [c for c in classifications if c["classification"] == "Recoverable"]
    repair = [c for c in classifications if c["classification"] == "Requires repair"]
    review = [c for c in classifications if c["classification"] == "Requires review"]
    dupes = [c for c in classifications if c["classification"] == "Duplicate"]
    quarantine = [c for c in classifications if c["classification"] == "Quarantine"]

    report = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "total_pf_questions": len(pf_questions),
        "classification_counts": dict(class_counts),
        "type_counts": dict(type_counts),
        "trust_counts": dict(trust_counts),
        "duplicate_cluster_count": len(duplicates),
        "classifications": classifications,
        "recoverable_ids": [c["id"] for c in recoverable],
        "requires_repair_ids": [c["id"] for c in repair],
        "requires_review_ids": [c["id"] for c in review],
        "duplicate_ids": [c["id"] for c in dupes],
        "quarantine_ids": [c["id"] for c in quarantine],
        "methodology": {
            "basis": "type-specific structure + correctness + executability + trust",
            "not_automatically_promoted": True,
            "recoverable_criteria": "structurally complete + correct + human-reviewed (verified/reviewed)",
            "repair_criteria": "fixable issues (missing fields, incorrect answer, not executable)",
            "review_criteria": "correctness not automatable or unverified",
            "quarantine_criteria": "placeholder, empty, already quarantined, or broken beyond repair",
        },
    }

    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, "programming_foundations_recovery_report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("=" * 70)
    print("PHASE 8 — PROGRAMMING FOUNDATIONS RECOVERY REPORT")
    print("=" * 70)
    print(f"Total PF questions: {len(pf_questions)}")
    print()
    print("--- Classification counts ---")
    for cls, count in sorted(class_counts.items()):
        print(f"  {cls:20s}: {count}")
    print()
    print("--- Type counts ---")
    for t, count in sorted(type_counts.items()):
        print(f"  {t:20s}: {count}")
    print()
    print("--- Trust counts ---")
    for t, count in sorted(trust_counts.items()):
        print(f"  {t:20s}: {count}")
    print()
    print(f"--- Recoverable ({len(recoverable)}) ---")
    for c in recoverable[:10]:
        print(f"  {c['id']} ({c['type']}): {c['topic']}")
    print()
    print(f"--- Requires repair ({len(repair)}) ---")
    for c in repair[:10]:
        print(f"  {c['id']} ({c['type']}): {', '.join(c['reasons'])}")
    print()
    print(f"--- Requires review ({len(review)}) ---")
    for c in review[:10]:
        print(f"  {c['id']} ({c['type']}): {', '.join(c['reasons'])}")
    print()
    print(f"--- Duplicates ({len(dupes)}) ---")
    for c in dupes[:10]:
        print(f"  {c['id']} ({c['type']}): {c['title'][:60]}")
    print()
    print(f"--- Quarantine ({len(quarantine)}) ---")
    for c in quarantine[:10]:
        print(f"  {c['id']} ({c['type']}): {', '.join(c['reasons'])}")
    print()
    print(f"Report saved to: {path}")
    print()
    print("NOTE: No questions were promoted or modified. This is a report only.")


if __name__ == "__main__":
    main()
