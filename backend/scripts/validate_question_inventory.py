"""
Phase 3 — Inventory revalidation and quality reporting.

Runs type-specific validators on all servable questions and produces:
- Per-type quality distribution
- Per-domain quality distribution
- Missing required fields
- Incorrect answer findings
- Broken reference solutions
- Invalid test cases
- Duplicate clusters
- Skill mapping gaps
- Manual-review requirements

Trust status, quality score, and serving eligibility are reported as
three separate systems — never combined into one number.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Suppress verbose trust-integrity warnings during batch load
logging.disable(logging.CRITICAL)

from app.services import question_store
from app.services.question_quality import (
    validate_structure,
    validate_answer_correctness,
    validate_executability,
    assess_quality,
    score_question,
    tier_for_score,
    QUESTION_TYPE_SCHEMAS,
    SERVABLE_TYPES,
    INAPPLICABLE_FIELDS,
)

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BACKEND_ROOT, "app", "data", "quality_reports")


def _ensure_report_dir() -> None:
    os.makedirs(REPORT_DIR, exist_ok=True)


def load_all_questions() -> List[Dict[str, Any]]:
    question_store.load_all()
    return list(question_store._questions)


def validate_inventory(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run all validators on every question and return a full quality report."""
    per_type: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "total": 0, "servable": 0, "structural_avg": 0.0,
        "correctness_avg": 0.0, "executability_avg": 0.0,
        "assessment_usefulness_avg": 0.0, "tiers": Counter(),
        "trust_states": Counter(), "missing_required": Counter(),
        "incorrect_answers": [], "broken_solutions": [],
        "invalid_test_cases": [], "needs_review": [],
    })
    per_domain: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "total": 0, "servable": 0, "structural_avg": 0.0,
        "correctness_avg": 0.0, "executability_avg": 0.0,
    })

    domain_map = {
        "coding": "DSA Coding", "sql": "SQL", "aptitude": "Quantitative Aptitude",
        "logical": "Logical Reasoning", "verbal": "Verbal Ability",
        "cs_fundamentals": "CS Fundamentals", "cs": "CS Fundamentals",
        "debugging": "Debugging", "system_design": "System Design",
        "interview": "Behavioral/Interview", "behavioral": "Behavioral/Interview",
        "hr": "Behavioral/Interview",
    }

    missing_required_fields = Counter()
    incorrect_answers = []
    broken_solutions = []
    invalid_test_cases = []
    duplicate_clusters: Dict[str, List[str]] = defaultdict(list)
    skill_mapping_gaps = []
    manual_review = []

    trust_breakdown = Counter()
    servable_breakdown = Counter()
    tier_breakdown = Counter()

    title_groups: Dict[str, List[str]] = defaultdict(list)

    for q in questions:
        qtype = str(q.get("type", "coding")).lower()
        qid = str(q.get("id", ""))
        title = str(q.get("question") or q.get("question_title") or q.get("title") or "")
        trust = str(q.get("trust_status", "unverified")).lower()
        domain = domain_map.get(qtype, "Other")

        # Duplicate clustering by normalized title
        norm_title = "".join(c for c in title.lower() if c.isalnum())[:60]
        if norm_title:
            title_groups[norm_title].append(qid)

        trust_breakdown[trust] += 1
        tier = score_question(q)["quality_tier"]
        tier_breakdown[tier] += 1

        pt = per_type[qtype]
        pt["total"] += 1
        pt["trust_states"][trust] += 1
        pt["tiers"][tier] += 1

        pd = per_domain[domain]
        pd["total"] += 1

        # Structural validation
        struct = validate_structure(q)
        pt["structural_avg"] += struct["score"]
        pd["structural_avg"] += struct["score"]

        for label in struct["required_missing"]:
            missing_required_fields[label] += 1
            pt["missing_required"][label] += 1

        # Answer correctness (skip code execution in batch mode — too slow;
        # coding/SQL/debugging correctness requires human review or separate
        # execution pipeline)
        correctness = {"automatable": False, "score": None, "passed": 0, "total": 0,
                       "details": [{"check": "answer_correctness", "pass": None,
                                    "detail": "Skipped in batch mode; requires human review or separate execution pipeline"}]}
        if qtype not in ("coding", "sql", "debugging"):
            correctness = validate_answer_correctness(q)
        if correctness["automatable"]:
            pt["correctness_avg"] += correctness["score"]
            pd["correctness_avg"] += correctness["score"]
            if correctness["score"] < 100:
                incorrect_answers.append({
                    "id": qid, "type": qtype, "domain": domain,
                    "score": correctness["score"],
                    "passed": correctness["passed"],
                    "total": correctness["total"],
                    "details": correctness["details"],
                })
                pt["incorrect_answers"].append(qid)

        # Executability
        exec_result = validate_executability(q)
        pt["executability_avg"] += exec_result["score"]
        pd["executability_avg"] += exec_result["score"]

        if not exec_result["executable"]:
            broken_solutions.append({
                "id": qid, "type": qtype, "domain": domain,
                "details": exec_result["details"],
            })
            pt["broken_solutions"].append(qid)

        # Test case validation (coding/sql/debugging)
        if qtype in ("coding", "sql", "debugging"):
            tcs = q.get("test_cases") or q.get("testcases") or []
            if not tcs:
                invalid_test_cases.append({
                    "id": qid, "type": qtype, "issue": "no_test_cases",
                })
                pt["invalid_test_cases"].append(qid)

        # Full quality assessment
        dims = assess_quality(q)
        pt["assessment_usefulness_avg"] += dims.assessment_usefulness

        # Servable check
        is_servable = question_store._is_servable(q)
        if is_servable:
            pt["servable"] += 1
            pd["servable"] += 1
            servable_breakdown[trust] += 1

        # Skill mapping gap
        if not q.get("canonical_skill_id"):
            skill_mapping_gaps.append({
                "id": qid, "type": qtype, "topic": q.get("topic"),
                "sub_topic": q.get("sub_topic"),
            })

        # Manual review requirements
        reasons = []
        if not struct["all_required_present"]:
            reasons.append("missing_required_fields")
        if correctness["automatable"] and correctness["score"] < 100:
            reasons.append("incorrect_answer")
        if not exec_result["executable"]:
            reasons.append("not_executable")
        if trust not in ("verified", "reviewed"):
            reasons.append("not_human_reviewed")
        if reasons:
            manual_review.append({
                "id": qid, "type": qtype, "domain": domain,
                "trust": trust, "tier": tier, "reasons": reasons,
            })
            pt["needs_review"].append(qid)

    # Average calculations
    for qtype, pt in per_type.items():
        n = pt["total"]
        pt["structural_avg"] = round(pt["structural_avg"] / n, 1) if n else 0
        pt["correctness_avg"] = round(pt["correctness_avg"] / n, 1) if n else 0
        pt["executability_avg"] = round(pt["executability_avg"] / n, 1) if n else 0
        pt["assessment_usefulness_avg"] = round(pt["assessment_usefulness_avg"] / n, 1) if n else 0
        pt["tiers"] = dict(pt["tiers"])
        pt["trust_states"] = dict(pt["trust_states"])
        pt["missing_required"] = dict(pt["missing_required"])

    for domain, pd in per_domain.items():
        n = pd["total"]
        pd["structural_avg"] = round(pd["structural_avg"] / n, 1) if n else 0
        pd["correctness_avg"] = round(pd["correctness_avg"] / n, 1) if n else 0
        pd["executability_avg"] = round(pd["executability_avg"] / n, 1) if n else 0

    # Duplicate clusters (2+ questions with same normalized title)
    duplicates = {k: v for k, v in title_groups.items() if len(v) >= 2}

    # Servable totals
    total_servable = sum(1 for q in questions if question_store._is_servable(q))

    report = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "total_questions": len(questions),
        "total_servable": total_servable,
        "servable_rate": round(total_servable / len(questions) * 100, 1) if questions else 0,
        "trust_breakdown": dict(trust_breakdown),
        "servable_breakdown": dict(servable_breakdown),
        "tier_breakdown": dict(tier_breakdown),
        "per_type": dict(per_type),
        "per_domain": dict(per_domain),
        "missing_required_fields": dict(missing_required_fields),
        "incorrect_answers": incorrect_answers,
        "broken_solutions": broken_solutions,
        "invalid_test_cases": invalid_test_cases,
        "duplicate_clusters": duplicates,
        "duplicate_cluster_count": len(duplicates),
        "skill_mapping_gaps": skill_mapping_gaps,
        "skill_mapping_gap_count": len(skill_mapping_gaps),
        "manual_review": manual_review,
        "manual_review_count": len(manual_review),
        "quality_systems": {
            "structural_completeness": "validate_structure() — per-type required/optional/inapplicable fields",
            "answer_correctness": "validate_answer_correctness() — automated where possible, None = human review",
            "executability": "validate_executability() — can the question actually be graded",
            "trust_status": "question_store.py — lifecycle state machine (unverified → verified)",
            "serving_eligibility": "question_store._is_servable() — trust in {verified, reviewed} AND executable",
            "quality_score": "score_question() — weighted field presence, never auto-grants verified",
        },
    }
    return report


def write_report(report: Dict[str, Any]) -> str:
    _ensure_report_dir()
    path = os.path.join(REPORT_DIR, "inventory_quality_report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return path


def print_summary(report: Dict[str, Any]) -> None:
    print("=" * 70)
    print("PHASE 3 — INVENTORY QUALITY REPORT")
    print("=" * 70)
    print(f"Total questions:     {report['total_questions']}")
    print(f"Total servable:      {report['total_servable']} ({report['servable_rate']}%)")
    print()
    print("--- Trust breakdown ---")
    for k, v in sorted(report["trust_breakdown"].items()):
        print(f"  {k:20s}: {v}")
    print()
    print("--- Tier breakdown ---")
    for k, v in sorted(report["tier_breakdown"].items()):
        print(f"  {k:10s}: {v}")
    print()
    print("--- Per-type quality ---")
    for qtype, pt in sorted(report["per_type"].items()):
        print(f"  {qtype:18s}: total={pt['total']:4d} servable={pt['servable']:4d} "
              f"struct={pt['structural_avg']:5.1f} correctness={pt['correctness_avg']:5.1f} "
              f"exec={pt['executability_avg']:5.1f} usefulness={pt['assessment_usefulness_avg']:5.1f}")
    print()
    print("--- Per-domain quality ---")
    for domain, pd in sorted(report["per_domain"].items()):
        print(f"  {domain:22s}: total={pd['total']:4d} servable={pd['servable']:4d} "
              f"struct={pd['structural_avg']:5.1f} correctness={pd['correctness_avg']:5.1f} "
              f"exec={pd['executability_avg']:5.1f}")
    print()
    print("--- Missing required fields ---")
    for label, count in sorted(report["missing_required_fields"].items(), key=lambda x: -x[1]):
        print(f"  {count:4d}  {label}")
    print()
    print(f"--- Incorrect answers: {len(report['incorrect_answers'])} ---")
    for item in report["incorrect_answers"][:10]:
        print(f"  {item['id']} ({item['type']}): {item['score']}/100 correctness")
    print()
    print(f"--- Broken solutions: {len(report['broken_solutions'])} ---")
    for item in report["broken_solutions"][:10]:
        print(f"  {item['id']} ({item['type']})")
    print()
    print(f"--- Invalid test cases: {len(report['invalid_test_cases'])} ---")
    for item in report["invalid_test_cases"][:10]:
        print(f"  {item['id']} ({item['type']}): {item['issue']}")
    print()
    print(f"--- Duplicate clusters: {report['duplicate_cluster_count']} ---")
    for norm, ids in list(report["duplicate_clusters"].items())[:10]:
        print(f"  '{norm}': {len(ids)} questions")
    print()
    print(f"--- Skill mapping gaps: {report['skill_mapping_gap_count']} ---")
    for gap in report["skill_mapping_gaps"][:10]:
        print(f"  {gap['id']} ({gap['type']}): topic={gap['topic']}")
    print()
    print(f"--- Manual review required: {report['manual_review_count']} ---")
    for item in report["manual_review"][:10]:
        print(f"  {item['id']} ({item['type']}): {', '.join(item['reasons'])}")
    print()
    print("Report saved to: app/data/quality_reports/inventory_quality_report.json")


def main() -> None:
    questions = load_all_questions()
    report = validate_inventory(questions)
    path = write_report(report)
    print_summary(report)
    print(f"\nFull report written to: {path}")


if __name__ == "__main__":
    main()
