"""Deterministic tests for readiness_engine public API.

NO AI imports. All inputs are handcrafted; expected outputs are exact numbers.
"""
from __future__ import annotations

import math
from app.services.readiness_engine import (
    SkillEvidence,
    calculate_skill_score,
    is_insufficient,
    load_target_profile,
    determine_next_action,
    calculate_target_readiness,
    SKILL_COMPONENT_WEIGHTS,
    MIN_EVIDENCE_PER_SKILL,
    STRONG_SKILL,
    GAP_SKILL,
    CRITICAL_SKILL_THRESHOLD,
    MIN_COVERAGE_FOR_JUDGMENT,
    READY_COVERAGE,
    READY_SCORE,
)


# ── helpers ────────────────────────────────────────────────────────────────

def assert_eq(got, want, label=""):
    assert got == want, f"{label}: got {got!r}, want {want!r}"


def _profile(skills):
    return {"role": "test", "company": None,
            "skills": [{"skill_id": sid, "domain": sid, "label": sid,
                        "weight": w, "critical": c, "threshold": 60.0 if c else 0.0,
                        "category": sid, "sources": [sid]}
                       for sid, w, c in skills]}


# ── 1. SkillEvidence dataclass ─────────────────────────────────────────────

def test_skill_evidence_dataclass():
    ev = SkillEvidence(
        mastery=80.0,
        assessments=[70.0, 80.0, 90.0],
        transfer_tasks=[True, False, True],
        srs_retrievals=[True, True, False],
        practice_history=[75.0, 80.0, 85.0, 90.0],
    )
    assert_eq(ev.mastery, 80.0)
    assert_eq(len(ev.assessments), 3)
    assert_eq(len(ev.transfer_tasks), 3)
    assert_eq(len(ev.srs_retrievals), 3)
    assert_eq(len(ev.practice_history), 4)


# ── 2. calculate_skill_score — all zeros ───────────────────────────────────

def test_calculate_skill_score_all_zeros():
    ev = SkillEvidence(
        mastery=0.0,
        assessments=[],
        transfer_tasks=[],
        srs_retrievals=[],
        practice_history=[],
    )
    result = calculate_skill_score(ev)
    # consistency defaults to 50.0 when <3 practice_history items: 50.0 * 0.10 = 5.0
    assert_eq(result["score"], 5.0)
    assert_eq(result["breakdown"]["mastery"], 0.0)
    assert_eq(result["breakdown"]["assessment"], 0.0)
    assert_eq(result["breakdown"]["transfer"], 0.0)
    assert_eq(result["breakdown"]["retention"], 0.0)
    assert_eq(result["breakdown"]["consistency"], 50.0)


# ── 3. calculate_skill_score — full marks ──────────────────────────────────

def test_calculate_skill_score_full_marks():
    ev = SkillEvidence(
        mastery=100.0,
        assessments=[100.0, 100.0, 100.0],
        transfer_tasks=[True, True, True],
        srs_retrievals=[True, True, True],
        practice_history=[100.0, 100.0, 100.0],
    )
    result = calculate_skill_score(ev)
    expected = round(
        100.0 * SKILL_COMPONENT_WEIGHTS["mastery"] +
        100.0 * SKILL_COMPONENT_WEIGHTS["assessment"] +
        100.0 * SKILL_COMPONENT_WEIGHTS["transfer"] +
        100.0 * SKILL_COMPONENT_WEIGHTS["retention"] +
        100.0 * SKILL_COMPONENT_WEIGHTS["consistency"],
        1,
    )
    assert_eq(result["score"], expected)
    assert_eq(result["breakdown"]["mastery"], 100.0)
    assert_eq(result["breakdown"]["consistency"], 100.0)


# ── 4. calculate_skill_score — mixed / weighted correctness ────────────────

def test_calculate_skill_score_weighted_mix():
    # mastery=80, assessment avg of last 3 of [70,80]=75, transfer=50%, retention=50%
    # consistency: [82,84,87,89] -> mean=85.5, var=7.25, std=2.6926, score=100-6.73=93.27
    ev = SkillEvidence(
        mastery=80.0,
        assessments=[70.0, 80.0],
        transfer_tasks=[True, False],
        srs_retrievals=[True, False],
        practice_history=[82.0, 84.0, 87.0, 89.0],
    )
    result = calculate_skill_score(ev)
    expected = round(
        80.0 * 0.30 +
        75.0 * 0.25 +
        50.0 * 0.20 +
        50.0 * 0.15 +
        93.27 * 0.10,
        1,
    )
    assert_eq(result["score"], expected)
    assert_eq(result["breakdown"]["mastery"], 80.0)
    assert_eq(result["breakdown"]["assessment"], 75.0)
    assert_eq(result["breakdown"]["transfer"], 50.0)
    assert_eq(result["breakdown"]["retention"], 50.0)


# ── 5. is_insufficient — too few events ────────────────────────────────────

def test_is_insufficient_few_events():
    ev = SkillEvidence(
        mastery=50.0,
        assessments=[60.0],
        transfer_tasks=[True],
        srs_retrievals=[False],
        practice_history=[50.0],
    )
    # total = 1 + 1 + 1 + 1 = 4 < MIN_EVIDENCE_PER_SKILL (3)? Wait 4 >= 3 so sufficient
    # Actually total events = assessments(1) + transfer_tasks(1) + srs_retrievals(1) + practice_history(1) = 4
    # MIN_EVIDENCE_PER_SKILL = 3, so 4 >= 3 -> sufficient
    # Let me use fewer
    ev2 = SkillEvidence(
        mastery=50.0,
        assessments=[60.0],
        transfer_tasks=[],
        srs_retrievals=[],
        practice_history=[],
    )
    assert is_insufficient(ev2) is True


# ── 6. is_insufficient — enough events ────────────────────────────────────

def test_is_insufficient_enough_events():
    ev = SkillEvidence(
        mastery=50.0,
        assessments=[60.0, 70.0],
        transfer_tasks=[True, False],
        srs_retrievals=[True, False],
        practice_history=[50.0, 55.0],
    )
    # total = 2 + 2 + 2 + 2 = 8 >= 3
    assert is_insufficient(ev) is False


# ── 7. is_insufficient — non-SkillEvidence input ───────────────────────────

def test_is_insufficient_non_skill_evidence():
    assert is_insufficient(None) is True
    assert is_insufficient("not a SkillEvidence") is True
    assert is_insufficient(42) is True


# ── 8. load_target_profile — SDE default ───────────────────────────────────

def test_load_target_profile_sde_default():
    profile = load_target_profile(role="sde")
    assert_eq(profile["role"], "sde")
    assert "skills" in profile
    assert len(profile["skills"]) > 0
    # Every skill must have weight, critical, threshold
    for skill in profile["skills"]:
        assert "skill_id" in skill
        assert "weight" in skill
        assert "critical" in skill
        assert "threshold" in skill


# ── 9. load_target_profile — TCS ───────────────────────────────────────────

def test_load_target_profile_tcs():
    profile = load_target_profile(role="sde", company="tcs")
    assert_eq(profile["role"], "sde")
    assert_eq(profile["company"], "tcs")
    total_weight = sum(s["weight"] for s in profile["skills"])
    assert abs(total_weight - 1.0) < 0.01


# ── 10. load_target_profile — Amazon ───────────────────────────────────────

def test_load_target_profile_amazon():
    profile = load_target_profile(role="sde", company="amazon")
    assert_eq(profile["company"], "amazon")
    assert_eq(profile["role"], "sde")
    assert len(profile["skills"]) > 0
    total_weight = sum(s["weight"] for s in profile["skills"])
    assert abs(total_weight - 1.0) < 0.01


# ── 11. load_target_profile — Infosys ──────────────────────────────────────

def test_load_target_profile_infosys():
    profile = load_target_profile(role="sde", company="infosys")
    assert_eq(profile["company"], "infosys")
    assert len(profile["skills"]) > 0


# ── 12. load_target_profile — Wipro ────────────────────────────────────────

def test_load_target_profile_wipro():
    profile = load_target_profile(role="sde", company="wipro")
    assert_eq(profile["company"], "wipro")
    assert len(profile["skills"]) > 0


# ── 13. determine_next_action — no skills ──────────────────────────────────

def test_determine_next_action_empty():
    result = determine_next_action([], {})
    assert result is None


# ── 14. determine_next_action — highest impact gap wins ────────────────────

def test_determine_next_action_highest_impact():
    skills = [
        {"skill_id": "easy", "score": 90.0, "weight": 0.1, "critical": False},
        {"skill_id": "hard", "score": 30.0, "weight": 0.4, "critical": True},
        {"skill_id": "mid", "score": 50.0, "weight": 0.2, "critical": False},
    ]
    target_map = {"skills": skills}
    result = determine_next_action(skills, target_map)
    assert result is not None
    assert_eq(result["skill_id"], "hard")
    assert_eq(result["type"], "repair")


# ── 15. calculate_skill_score — consistency high variance ──────────────────

def test_calculate_skill_score_consistency_high_variance():
    # [90, 42, 91, 88] -> mean=77.75, var=394.1875, std=19.85, score=100-49.63=50.37
    ev = SkillEvidence(
        mastery=80.0,
        assessments=[],
        transfer_tasks=[],
        srs_retrievals=[],
        practice_history=[90.0, 42.0, 91.0, 88.0],
    )
    result = calculate_skill_score(ev)
    consistency = result["breakdown"]["consistency"]
    assert consistency < 60.0, f"High variance should give low consistency, got {consistency}"


# ── 16. calculate_skill_score — consistency low variance ───────────────────

def test_calculate_skill_score_consistency_low_variance():
    # [82, 84, 87, 89] -> mean=85.5, var=5.25, std=2.29, score=100-5.73=94.27
    ev = SkillEvidence(
        mastery=80.0,
        assessments=[],
        transfer_tasks=[],
        srs_retrievals=[],
        practice_history=[82.0, 84.0, 87.0, 89.0],
    )
    result = calculate_skill_score(ev)
    consistency = result["breakdown"]["consistency"]
    assert consistency > 90.0, f"Low variance should give high consistency, got {consistency}"


# ── 17. Action taxonomy: PROVE when coverage insufficient ────────────────────

def test_action_taxonomy_prove_insufficient_coverage():
    profile = load_target_profile(role="sde")
    evidence = {}
    result = __import__("app.services.readiness_engine", fromlist=["calculate_target_readiness"]).calculate_target_readiness(profile, evidence)
    assert result["next_action"]["type"] == "prove"
    assert "coverage" in result["next_action"]["reason"] or "evidence" in result["next_action"]["reason"]


# ── 18. Action taxonomy: REPAIR for critical blocker ─────────────────────────

def test_action_taxonomy_repair_critical_blocker():
    p = _profile([("dsa", 0.6, True), ("coding", 0.4, False)])
    ev = {"dsa": {"mastery": 30, "assessment": 30, "transfer": 30, "retention": 30,
                  "consistency": 50, "eligible_events": 10, "high_stakes": True,
                  "last_evidence_at": "2026-09-01T00:00:00+00:00",
                  "counts": {"practice": 10, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}},
          "coding": {"mastery": 95, "assessment": 95, "transfer": 95, "retention": 95,
                     "consistency": 95, "eligible_events": 10, "high_stakes": True,
                     "last_evidence_at": "2026-09-01T00:00:00+00:00",
                     "counts": {"practice": 10, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}}}
    result = calculate_target_readiness(p, ev)
    assert result["next_action"]["type"] == "repair"
    assert result["next_action"]["skill_id"] == "dsa"


# ── 19. Action taxonomy: ADVANCE for strong skill ───────────────────────────

def test_action_taxonomy_advance_strong_skill():
    p = _profile([("dsa", 0.5, False), ("coding", 0.5, False)])
    ev = {"dsa": {"mastery": 90, "assessment": 85, "transfer": 80, "retention": 85,
                  "consistency": 90, "eligible_events": 10, "high_stakes": True,
                  "last_evidence_at": "2026-09-01T00:00:00+00:00",
                  "counts": {"practice": 10, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}},
          "coding": {"mastery": 90, "assessment": 85, "transfer": 80, "retention": 85,
                     "consistency": 90, "eligible_events": 10, "high_stakes": True,
                     "last_evidence_at": "2026-09-01T00:00:00+00:00",
                     "counts": {"practice": 10, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}}}
    result = calculate_target_readiness(p, ev)
    assert result["next_action"]["type"] == "advance"


# ── 20. Action taxonomy: RETAIN for good skill ───────────────────────────────

def test_action_taxonomy_retain_good_skill():
    p = _profile([("dsa", 0.5, False), ("coding", 0.5, False)])
    ev = {"dsa": {"mastery": 70, "assessment": 65, "transfer": 60, "retention": 65,
                  "consistency": 70, "eligible_events": 10, "high_stakes": True,
                  "last_evidence_at": "2026-09-01T00:00:00+00:00",
                  "counts": {"practice": 10, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}},
          "coding": {"mastery": 70, "assessment": 65, "transfer": 60, "retention": 65,
                     "consistency": 70, "eligible_events": 10, "high_stakes": True,
                     "last_evidence_at": "2026-09-01T00:00:00+00:00",
                     "counts": {"practice": 10, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}}}
    result = calculate_target_readiness(p, ev)
    assert result["next_action"]["type"] == "retain"


# ── 21. Coverage message ─────────────────────────────────────────────────────

def test_coverage_message():
    p = _profile([("dsa", 0.5, False)])
    ev = {}
    result = calculate_target_readiness(p, ev)
    assert "coverage_message" in result
    assert "Insufficient evidence" in result["coverage_message"]
    assert "0.0%" in result["coverage_message"]


# ── 22. Target weights present ───────────────────────────────────────────────

def test_target_weights_present():
    p = _profile([("dsa", 0.6, True), ("coding", 0.4, False)])
    ev = {"dsa": {"mastery": 50, "assessment": 50, "transfer": 50, "retention": 50,
                  "consistency": 50, "eligible_events": 5, "high_stakes": True,
                  "last_evidence_at": "2026-09-01T00:00:00+00:00",
                  "counts": {"practice": 5, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}},
          "coding": {"mastery": 50, "assessment": 50, "transfer": 50, "retention": 50,
                     "consistency": 50, "eligible_events": 5, "high_stakes": True,
                     "last_evidence_at": "2026-09-01T00:00:00+00:00",
                     "counts": {"practice": 5, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}}}
    result = calculate_target_readiness(p, ev)
    assert "target_weights" in result
    assert result["target_weights"]["dsa"] == 0.6
    assert result["target_weights"]["coding"] == 0.4
