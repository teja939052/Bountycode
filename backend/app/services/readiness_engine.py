"""Readiness Engine — PostgreSQL-backed, no MongoDB."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean, pstdev
from typing import Dict, List, Optional

from app.database import get_session


# ── Component weights (must sum to 1.0) ──────────────────────────────────────

SKILL_COMPONENT_WEIGHTS: Dict[str, float] = {
    "mastery": 0.30,
    "assessment": 0.25,
    "transfer": 0.20,
    "retention": 0.15,
    "consistency": 0.10,
}

# ── Constants ────────────────────────────────────────────────────────────────

MIN_EVIDENCE_PER_SKILL = 2
STRONG_SKILL = 75.0
GAP_SKILL = 50.0
CRITICAL_SKILL_THRESHOLD = 40.0
MIN_COVERAGE_FOR_JUDGMENT = 0.6
READY_COVERAGE = 0.8
READY_SCORE = 70.0


# ── SkillEvidence dataclass ──────────────────────────────────────────────────

@dataclass
class SkillEvidence:
    """Skill evidence record."""

    mastery: float = 0.0
    assessments: List[float] = field(default_factory=list)
    transfer_tasks: List[bool] = field(default_factory=list)
    srs_retrievals: List[bool] = field(default_factory=list)
    practice_history: List[float] = field(default_factory=list)


# ── calculate_skill_score ────────────────────────────────────────────────────

def _assessment_score(scores: List[float]) -> float:
    if not scores:
        return 0.0
    return mean(scores[-3:])


def _transfer_score(tasks: List[bool]) -> float:
    if not tasks:
        return 0.0
    return 100.0 * sum(1 for t in tasks if t) / len(tasks)


def _retention_score(retrievals: List[bool]) -> float:
    if not retrievals:
        return 0.0
    return 100.0 * sum(1 for r in retrievals if r) / len(retrievals)


def _consistency_score(history: List[float]) -> float:
    if len(history) < 3:
        return 50.0
    m = mean(history)
    sd = pstdev(history)
    return max(0.0, min(100.0, 100.0 - 2.5 * sd))


def calculate_skill_score(ev: SkillEvidence) -> dict:
    """Calculate a weighted skill score from evidence."""
    mastery = ev.mastery
    assessment = _assessment_score(ev.assessments)
    transfer = _transfer_score(ev.transfer_tasks)
    retention = _retention_score(ev.srs_retrievals)
    consistency = _consistency_score(ev.practice_history)

    breakdown = {
        "mastery": round(mastery, 1),
        "assessment": round(assessment, 1),
        "transfer": round(transfer, 1),
        "retention": round(retention, 1),
        "consistency": round(consistency, 1),
    }

    score = (
        mastery * SKILL_COMPONENT_WEIGHTS["mastery"]
        + assessment * SKILL_COMPONENT_WEIGHTS["assessment"]
        + transfer * SKILL_COMPONENT_WEIGHTS["transfer"]
        + retention * SKILL_COMPONENT_WEIGHTS["retention"]
        + consistency * SKILL_COMPONENT_WEIGHTS["consistency"]
    )

    return {"score": round(score, 1), "breakdown": breakdown}


# ── is_insufficient ──────────────────────────────────────────────────────────

def is_insufficient(ev: Optional[SkillEvidence]) -> bool:
    """Return True if there is not enough evidence to judge a skill."""
    if not isinstance(ev, SkillEvidence):
        return True
    total = (
        len(ev.assessments)
        + len(ev.transfer_tasks)
        + len(ev.srs_retrievals)
        + len(ev.practice_history)
    )
    return total < MIN_EVIDENCE_PER_SKILL


# ── load_target_profile ──────────────────────────────────────────────────────

def _default_skills(company: Optional[str] = None) -> List[dict]:
    """Return default SDE skill profile with weights."""
    skills = [
        {"skill_id": "dsa", "domain": "dsa", "label": "DSA",
         "weight": 0.35, "critical": True, "threshold": 60.0,
         "category": "dsa", "sources": ["dsa"]},
        {"skill_id": "coding", "domain": "coding", "label": "Coding",
         "weight": 0.25, "critical": True, "threshold": 60.0,
         "category": "coding", "sources": ["coding"]},
        {"skill_id": "system_design", "domain": "system_design", "label": "System Design",
         "weight": 0.20, "critical": False, "threshold": 50.0,
         "category": "system_design", "sources": ["system_design"]},
        {"skill_id": "debugging", "domain": "debugging", "label": "Debugging",
         "weight": 0.10, "critical": False, "threshold": 50.0,
         "category": "debugging", "sources": ["debugging"]},
        {"skill_id": "testing", "domain": "testing", "label": "Testing",
         "weight": 0.10, "critical": False, "threshold": 50.0,
         "category": "testing", "sources": ["testing"]},
    ]
    total = sum(s["weight"] for s in skills)
    if abs(total - 1.0) > 0.01:
        # Normalize to sum to 1.0
        for s in skills:
            s["weight"] = round(s["weight"] / total, 2)
    return skills


def load_target_profile(role: str = "sde", company: Optional[str] = None) -> dict:
    """Load a target readiness profile for a role/company."""
    return {
        "role": role,
        "company": company,
        "skills": _default_skills(company),
    }


# ── determine_next_action ────────────────────────────────────────────────────

def determine_next_action(skills: List[dict], target_map: dict) -> Optional[dict]:
    """Determine the next action for a set of skills."""
    if not skills:
        return None

    target_skills = target_map.get("skills", []) if isinstance(target_map, dict) else []
    target_by_id = {s["skill_id"]: s for s in target_skills}

    best_skill = None
    best_impact = -1.0

    for skill in skills:
        sid = skill.get("skill_id", "")
        score = skill.get("score", 0.0)
        weight = skill.get("weight", 0.0)
        critical = skill.get("critical", False)

        # Impact = weight * (100 - score) for critical skills, weighted otherwise
        gap = max(0.0, 100.0 - score)
        impact = weight * gap
        if critical:
            impact *= 1.5

        if impact > best_impact:
            best_impact = impact
            best_skill = skill

    if best_skill is None:
        return None

    sid = best_skill.get("skill_id", "")
    score = best_skill.get("score", 0.0)
    critical = best_skill.get("critical", False)

    if score >= STRONG_SKILL:
        action_type = "advance"
    elif score <= CRITICAL_SKILL_THRESHOLD and critical:
        action_type = "repair"
    elif score < GAP_SKILL:
        action_type = "repair"
    else:
        action_type = "retain"

    return {
        "skill_id": sid,
        "type": action_type,
        "score": score,
        "impact": round(best_impact, 2),
    }


# ── calculate_target_readiness ───────────────────────────────────────────────

def _score_from_evidence(ev: dict) -> float:
    """Compute a skill score from a flat evidence dict."""
    return (
        ev.get("mastery", 0.0) * SKILL_COMPONENT_WEIGHTS["mastery"]
        + ev.get("assessment", 0.0) * SKILL_COMPONENT_WEIGHTS["assessment"]
        + ev.get("transfer", 0.0) * SKILL_COMPONENT_WEIGHTS["transfer"]
        + ev.get("retention", 0.0) * SKILL_COMPONENT_WEIGHTS["retention"]
        + ev.get("consistency", 0.0) * SKILL_COMPONENT_WEIGHTS["consistency"]
    )


def calculate_target_readiness(profile: dict, evidence: dict) -> dict:
    """Calculate target readiness and determine next action."""
    skills = profile.get("skills", [])
    company = profile.get("company")
    role = profile.get("role")

    # Build skill score list from evidence
    scored_skills = []
    for skill in skills:
        sid = skill.get("skill_id", "")
        ev = evidence.get(sid, {})
        score = _score_from_evidence(ev)
        scored_skills.append({
            "skill_id": sid,
            "score": round(score, 1),
            "weight": skill.get("weight", 0.0),
            "critical": skill.get("critical", False),
        })

    # Coverage
    total_weight = sum(s["weight"] for s in skills)
    covered_weight = sum(
        s["weight"] for s in scored_skills
        if evidence.get(s["skill_id"], {}).get("eligible_events", 0) > 0
    )
    coverage = covered_weight / total_weight if total_weight > 0 else 0.0

    # Coverage message
    pct = round(coverage * 100, 1)
    if coverage < MIN_COVERAGE_FOR_JUDGMENT:
        coverage_message = f"Insufficient evidence: {pct}% coverage"
    else:
        coverage_message = f"Sufficient evidence: {pct}% coverage"

    # Determine next action
    target_map = {"skills": skills}
    next_action = determine_next_action(scored_skills, target_map)

    if next_action is None:
        next_action = {"type": "prove", "reason": "no skills to evaluate"}

    if coverage < MIN_COVERAGE_FOR_JUDGMENT and next_action["type"] != "prove":
        next_action = {"type": "prove", "reason": "insufficient coverage or evidence"}

    # Target weights
    target_weights = {s["skill_id"]: s["weight"] for s in skills}

    # Overall readiness
    overall_score = sum(
        s["score"] * s["weight"] for s in scored_skills
    ) / total_weight if total_weight > 0 else 0.0

    return {
        "role": role,
        "company": company,
        "overall_readiness": round(overall_score, 1),
        "coverage": round(coverage, 2),
        "coverage_message": coverage_message,
        "next_action": next_action,
        "target_weights": target_weights,
        "skills": scored_skills,
    }


# ── score_target_skill ───────────────────────────────────────────────────────

def score_target_skill(evidence: dict) -> dict:
    """Score a target skill from flat evidence dict."""
    score = _score_from_evidence(evidence)
    return {
        "score": round(score, 1),
        "breakdown": {
            "mastery": evidence.get("mastery", 0.0),
            "assessment": evidence.get("assessment", 0.0),
            "transfer": evidence.get("transfer", 0.0),
            "retention": evidence.get("retention", 0.0),
            "consistency": evidence.get("consistency", 0.0),
        },
    }


# ── Legacy functions (stubs for backward compatibility) ──────────────────────

async def calculate_readiness(user_id: str) -> dict:
    """Calculate readiness score for a user."""
    return {"user_id": user_id, "readiness_score": 0, "ready": False}


async def compute_readiness(user_id: str) -> dict:
    """Compute readiness for user - alias for calculate_readiness."""
    return await calculate_readiness(user_id)


async def get_readiness_details(user_id: str) -> dict:
    """Get detailed readiness information for user."""
    return {"user_id": user_id, "detailed_readiness": {}}


async def calculate_target_readiness_async(user_id: str) -> dict:
    """Stub for calculate_target_readiness."""
    return {"user_id": user_id}


async def collect_target_evidence(user_id: str) -> dict:
    """Stub for collect_target_evidence."""
    return {"user_id": user_id}


def build_target_profile(user_id: str, skills: Optional[List[str]] = None) -> dict:
    """Build a target readiness profile for a user."""
    return {
        "user_id": user_id,
        "skills": skills or [],
        "target_readiness": 0,
        "ready": False,
    }
