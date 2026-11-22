"""
Phase 6 - Company Readiness Evidence Validation.

Tests multiple simulated learners:
- High question completion, low mastery
- Low question completion, high demonstrated mastery
- High mastery but poor retention
- High mastery but no unseen transfer
- Strong skills with unmet prerequisites
- Strong evidence aligned with a specific company role

Verifies readiness distinguishes:
- Demonstrated evidence vs internal predictions
- Official company-specific evidence vs internal prediction
- Insufficient evidence

Never presents internal prediction as official company cutoff.
"""

from __future__ import annotations

import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

logging.disable(logging.CRITICAL)

from app.services.readiness_engine import company_readiness_evidence_report, _domain_score

results: list[dict] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    results.append({"check": name, "passed": bool(condition), "detail": detail})
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" - {detail}" if detail else ""))


# -- Learner 1: High question completion, low mastery --
def test_high_completion_low_mastery() -> None:
    print("\n--- Learner 1: High question completion, low mastery ---")
    # Skill graph shows high completion (many questions) but low scores
    skill_graph = {
        "dsa": {"assessment_score": 25.0, "mastery_level": 1, "questions_completed": 200},
        "aptitude": {"assessment_score": 20.0, "mastery_level": 1, "questions_completed": 150},
        "coding": {"assessment_score": 30.0, "mastery_level": 1, "questions_completed": 180},
        "cs_fundamentals": {"assessment_score": 15.0, "mastery_level": 1, "questions_completed": 100},
        "interview": {"assessment_score": 10.0, "mastery_level": 0, "questions_completed": 50},
        "verbal": {"assessment_score": 20.0, "mastery_level": 1, "questions_completed": 80},
        "resume": {"assessment_score": 10.0, "mastery_level": 0, "questions_completed": 30},
        "system_design": {"assessment_score": 5.0, "mastery_level": 0, "questions_completed": 10},
    }
    report = company_readiness_evidence_report("user-1", skill_graph, target_company="tcs")
    check("Overall readiness is low despite high question completion",
          report["overall_readiness"] < 40,
          f"got {report['overall_readiness']}")
    check("Readiness level is not 'Interview Ready' for low mastery",
          report["readiness_level"] != "Interview Ready",
          f"got {report['readiness_level']}")
    check("Has blockers (domains below 50%)",
          len(report["blockers"]) > 0,
          f"blockers: {report['blockers']}")
    check("Not based on question count",
          report["methodology"]["not_based_on"] == "percentage_of_questions_completed")


# -- Learner 2: Low question completion, high demonstrated mastery --
def test_low_completion_high_mastery() -> None:
    print("\n--- Learner 2: Low question completion, high demonstrated mastery ---")
    skill_graph = {
        "dsa": {"assessment_score": 92.0, "mastery_level": 5, "questions_completed": 15},
        "aptitude": {"assessment_score": 88.0, "mastery_level": 5, "questions_completed": 10},
        "coding": {"assessment_score": 90.0, "mastery_level": 5, "questions_completed": 12},
        "cs_fundamentals": {"assessment_score": 85.0, "mastery_level": 4, "questions_completed": 8},
        "interview": {"assessment_score": 80.0, "mastery_level": 4, "questions_completed": 5},
        "verbal": {"assessment_score": 75.0, "mastery_level": 4, "questions_completed": 7},
        "resume": {"assessment_score": 70.0, "mastery_level": 3, "questions_completed": 3},
        "system_design": {"assessment_score": 65.0, "mastery_level": 3, "questions_completed": 2},
    }
    report = company_readiness_evidence_report("user-2", skill_graph, target_company="google")
    check("Overall readiness is high despite low question completion",
          report["overall_readiness"] > 70,
          f"got {report['overall_readiness']}")
    check("Readiness level reflects demonstrated mastery (not Interview Ready since <90)",
          report["readiness_level"] != "Interview Ready",
          f"got {report['readiness_level']}")
    check("Not based on question count",
          report["methodology"]["not_based_on"] == "percentage_of_questions_completed")


# -- Learner 3: High mastery but poor retention --
def test_high_mastery_poor_retention() -> None:
    print("\n--- Learner 3: High mastery but poor retention ---")
    skill_graph = {
        "dsa": {"assessment_score": 95.0, "mastery_level": 5, "retention_score": 30.0},
        "aptitude": {"assessment_score": 90.0, "mastery_level": 5, "retention_score": 25.0},
        "coding": {"assessment_score": 92.0, "mastery_level": 5, "retention_score": 35.0},
        "cs_fundamentals": {"assessment_score": 88.0, "mastery_level": 5, "retention_score": 20.0},
        "interview": {"assessment_score": 85.0, "mastery_level": 4, "retention_score": 40.0},
        "verbal": {"assessment_score": 80.0, "mastery_level": 4, "retention_score": 30.0},
        "resume": {"assessment_score": 75.0, "mastery_level": 4, "retention_score": 35.0},
        "system_design": {"assessment_score": 70.0, "mastery_level": 4, "retention_score": 25.0},
    }
    report = company_readiness_evidence_report("user-3", skill_graph)
    check("Readiness reflects retention penalty",
          report["overall_readiness"] < 90,
          f"got {report['overall_readiness']} despite high mastery")
    check("Evidence sources include retention",
          "retention" in report["evidence_sources"],
          f"sources: {report['evidence_sources']}")


# -- Learner 4: High mastery but no unseen transfer --
def test_high_mastery_no_transfer() -> None:
    print("\n--- Learner 4: High mastery but no unseen transfer ---")
    skill_graph = {
        "dsa": {"assessment_score": 95.0, "mastery_level": 5, "transfer_score": 0.0},
        "aptitude": {"assessment_score": 90.0, "mastery_level": 5, "transfer_score": 0.0},
        "coding": {"assessment_score": 92.0, "mastery_level": 5, "transfer_score": 0.0},
        "cs_fundamentals": {"assessment_score": 88.0, "mastery_level": 4, "transfer_score": 0.0},
        "interview": {"assessment_score": 85.0, "mastery_level": 4, "transfer_score": 0.0},
        "verbal": {"assessment_score": 80.0, "mastery_level": 4, "transfer_score": 0.0},
        "resume": {"assessment_score": 75.0, "mastery_level": 3, "transfer_score": 0.0},
        "system_design": {"assessment_score": 70.0, "mastery_level": 3, "transfer_score": 0.0},
    }
    report = company_readiness_evidence_report("user-4", skill_graph, target_company="microsoft")
    check("Readiness is capped without unseen transfer evidence",
          report["overall_readiness"] < 85,
          f"got {report['overall_readiness']}")
    check("Evidence sources include transfer",
          "transfer" in report["evidence_sources"],
          f"sources: {report['evidence_sources']}")


# -- Learner 5: Strong skills with unmet prerequisites --
def test_strong_skills_unmet_prereqs() -> None:
    print("\n--- Learner 5: Strong skills with unmet prerequisites ---")
    skill_graph = {
        "dsa": {"assessment_score": 95.0, "mastery_level": 5, "questions_completed": 50},
        "system_design": {"assessment_score": 90.0, "mastery_level": 5, "questions_completed": 30},
        # No aptitude/coding foundation but strong in advanced topics
        "aptitude": {"assessment_score": 20.0, "mastery_level": 1, "questions_completed": 5},
        "coding": {"assessment_score": 25.0, "mastery_level": 1, "questions_completed": 5},
        "cs_fundamentals": {"assessment_score": 15.0, "mastery_level": 1, "questions_completed": 3},
        "interview": {"assessment_score": 30.0, "mastery_level": 1, "questions_completed": 2},
        "verbal": {"assessment_score": 40.0, "mastery_level": 1, "questions_completed": 4},
        "resume": {"assessment_score": 35.0, "mastery_level": 1, "questions_completed": 1},
    }
    report = company_readiness_evidence_report("user-5", skill_graph, target_company="google")
    check("Readiness reflects missing foundational skills",
          report["overall_readiness"] < 60,
          f"got {report['overall_readiness']}")
    check("Has blockers for weak foundational domains",
          len(report["blockers"]) > 0,
          f"blockers: {report['blockers']}")


# -- Learner 6: Strong evidence aligned with specific company role --
def test_company_aligned_evidence() -> None:
    print("\n--- Learner 6: Strong evidence aligned with company role ---")
    # TCS-style: strong aptitude, moderate coding, strong cs_fundamentals
    skill_graph = {
        "aptitude": {"assessment_score": 95.0, "mastery_level": 5, "questions_completed": 30},
        "dsa": {"assessment_score": 85.0, "mastery_level": 4, "questions_completed": 25},
        "coding": {"assessment_score": 80.0, "mastery_level": 4, "questions_completed": 20},
        "cs_fundamentals": {"assessment_score": 88.0, "mastery_level": 4, "questions_completed": 15},
        "interview": {"assessment_score": 70.0, "mastery_level": 3, "questions_completed": 10},
        "verbal": {"assessment_score": 75.0, "mastery_level": 3, "questions_completed": 12},
        "resume": {"assessment_score": 65.0, "mastery_level": 3, "questions_completed": 5},
        "system_design": {"assessment_score": 60.0, "mastery_level": 2, "questions_completed": 3},
    }
    report = company_readiness_evidence_report("user-6", skill_graph, target_company="tcs")
    check("TCS readiness score is computed",
          "tcs" in report["per_company"],
          f"companies: {list(report['per_company'].keys())}")
    check("TCS score reflects aptitude strength",
          report["per_company"]["tcs"]["score"] > 70,
          f"got {report['per_company']['tcs']['score']}")
    check("Company-specific evidence separate from internal prediction",
          report["per_company"]["tcs"]["evidence"]["evidence_based"] is True)
    check("Internal prediction not presented as company cutoff",
          report["internal_prediction"]["overall_readiness"] != report["per_company"]["tcs"]["score"],
          f"internal={report['internal_prediction']['overall_readiness']}, "
          f"tcs={report['per_company']['tcs']['score']}")


# -- Learner 7: Insufficient evidence --
def test_insufficient_evidence() -> None:
    print("\n--- Learner 7: Insufficient evidence ---")
    skill_graph = {
        "dsa": {"assessment_score": 0.0, "mastery_level": 0},
        "aptitude": {"assessment_score": 0.0, "mastery_level": 0},
        "coding": {"assessment_score": 0.0, "mastery_level": 0},
        "cs_fundamentals": {"assessment_score": 0.0, "mastery_level": 0},
        "interview": {"assessment_score": 0.0, "mastery_level": 0},
        "verbal": {"assessment_score": 0.0, "mastery_level": 0},
        "resume": {"assessment_score": 0.0, "mastery_level": 0},
        "system_design": {"assessment_score": 0.0, "mastery_level": 0},
    }
    report = company_readiness_evidence_report("user-7", skill_graph)
    check("Readiness is 0 for no evidence",
          report["overall_readiness"] == 0.0,
          f"got {report['overall_readiness']}")
    check("Evidence confidence is 0",
          report["evidence_confidence"] == 0.0,
          f"got {report['evidence_confidence']}")
    check("All domains are blockers",
          len(report["blockers"]) == 8,
          f"got {len(report['blockers'])} blockers")


# -- Readiness distinguishes evidence types --
def test_readiness_distinguishes_evidence_types() -> None:
    print("\n--- Readiness distinguishes evidence types ---")
    skill_graph = {
        "dsa": {"assessment_score": 80.0, "mastery_level": 4},
        "aptitude": {"assessment_score": 70.0, "mastery_level": 3},
        "coding": {"assessment_score": 75.0, "mastery_level": 3},
        "cs_fundamentals": {"assessment_score": 60.0, "mastery_level": 2},
        "interview": {"assessment_score": 50.0, "mastery_level": 2},
        "verbal": {"assessment_score": 55.0, "mastery_level": 2},
        "resume": {"assessment_score": 40.0, "mastery_level": 1},
        "system_design": {"assessment_score": 30.0, "mastery_level": 1},
    }
    report = company_readiness_evidence_report("user-8", skill_graph, target_company="amazon")
    check("Demonstrated evidence present in domain_scores",
          all(s > 0 for s in report["domain_scores"].values()),
          f"domain_scores: {report['domain_scores']}")
    check("Internal prediction is separate from company evidence",
          report["internal_prediction"]["overall_readiness"] != report["per_company"]["amazon"]["score"],
          "internal == company score (should differ)")
    check("Company evidence includes domain breakdown",
          "domain_scores" in report["per_company"]["amazon"]["evidence"],
          "domain_scores present in company evidence")
    check("Readiness level is not 'hired' or 'guaranteed'",
          report["readiness_level"] not in ("Hired", "Guaranteed", "Offer"),
          f"got {report['readiness_level']}")


def main() -> None:
    print("=" * 70)
    print("PHASE 6 - COMPANY READINESS EVIDENCE VALIDATION")
    print("=" * 70)

    test_high_completion_low_mastery()
    test_low_completion_high_mastery()
    test_high_mastery_poor_retention()
    test_high_mastery_no_transfer()
    test_strong_skills_unmet_prereqs()
    test_company_aligned_evidence()
    test_insufficient_evidence()
    test_readiness_distinguishes_evidence_types()

    print("\n" + "=" * 70)
    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    print(f"Results: {passed} passed, {failed} failed, {len(results)} total")
    if failed:
        print("\nFAILURES:")
        for r in results:
            if not r["passed"]:
                print(f"  - {r['check']}: {r['detail']}")
    print("=" * 70)
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
