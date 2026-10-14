"""Opportunity Graph — maps learner evidence to company/role requirements.

This service provides the Opportunity Graph half of the canonical architecture:

```text
LEARNER GRAPH
       ↕
OPPORTUNITY GRAPH
```

It answers:
- What capabilities are required for a target opportunity?
- Where is each capability tested?
- What is the learner's gap for a specific company/role?
- What is the optimal learning path for this opportunity?

This does NOT create new scoring engines. It reads from existing canonical
systems and adds opportunity-specific adaptation.

Primary data source: company_overlays.py (the unified company registry).
Backward-compat fallback: readiness_engine.COMPANY_PROFILES (to be removed
once all callers migrate).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.services.readiness_engine import COMPANY_PROFILES, calculate_readiness

logger = logging.getLogger(__name__)


def get_opportunity(company: str, role: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get an opportunity profile by company name.

    Returns the versioned company profile, or None if not found.
    Reads from company_overlays.py first; falls back to COMPANY_PROFILES.
    """
    key = company.lower().strip()

    # Primary source: company_overlays
    try:
        from app.content.company_overlays import to_readiness_profile
        overlay = to_readiness_profile(key)
        if overlay:
            result = dict(overlay)
            if role:
                result["role"] = role
            return result
    except Exception as exc:
        logger.debug("company_overlays unavailable for %s: %s", company, exc)

    # Fallback: legacy COMPANY_PROFILES
    profile = COMPANY_PROFILES.get(key)
    if not profile:
        return None

    result = dict(profile)
    if role:
        result["role"] = role
    return result


def list_opportunities() -> List[Dict[str, Any]]:
    """List all available opportunity profiles."""
    profiles: Dict[str, Any] = {}
    try:
        from app.content.company_overlays import get_all_companies
        for cid, co in get_all_companies().items():
            profiles[cid] = {
                "company": cid,
                "assessment_variant": co.role,
                "version": co.version,
                "effective_date": co.effective_from,
                "interview_rounds": co.interview_rounds,
                "typical_timeline_weeks": co.typical_timeline_weeks,
            }
    except Exception as exc:
        logger.debug("company_overlays unavailable for list: %s", exc)

    # Merge fallback
    for key, profile in COMPANY_PROFILES.items():
        if key not in profiles:
            profiles[key] = {
                "company": key,
                "assessment_variant": profile.get("assessment_variant"),
                "version": profile.get("version"),
                "effective_date": profile.get("effective_date"),
                "interview_rounds": profile.get("interview_rounds"),
                "typical_timeline_weeks": profile.get("typical_timeline_weeks"),
            }

    return list(profiles.values())


def required_capabilities(company: str, role: Optional[str] = None) -> Dict[str, Any]:
    """Get the capabilities required for a target opportunity.

    Returns a dict of capability_id → required_level/threshold.
    """
    opportunity = get_opportunity(company, role)
    if not opportunity:
        return {}

    capabilities = {}
    for skill, threshold in opportunity.get("min_skills", {}).items():
        capabilities[skill] = {
            "required": threshold,
            "source": "company_overlay" if "company_overlays" in str(get_opportunity.__module__) else "company_profile",
            "company": company,
            "version": opportunity.get("version"),
            "effective_date": opportunity.get("effective_date"),
        }

    # Add problem-solving capability from min_solved
    min_solved = opportunity.get("min_solved", 0)
    if min_solved:
        capabilities["problem_solving_volume"] = {
            "required": min_solved,
            "source": "company_overlay" if "company_overlays" in str(get_opportunity.__module__) else "company_profile",
            "company": company,
            "version": opportunity.get("version"),
            "effective_date": opportunity.get("effective_date"),
        }

    return capabilities


def capability_gaps(
    learner_state: Dict[str, Any],
    company: str,
    role: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Compute capability gaps between learner state and opportunity requirements.

    Returns a list of gaps, sorted by severity.
    """
    required = required_capabilities(company, role)
    if not required:
        return []

    learner_skills = learner_state.get("skills", {})
    gaps = []

    for capability, req in required.items():
        current = learner_skills.get(capability)
        current_score = current.get("score") if isinstance(current, dict) else (current or 0)
        if not isinstance(current_score, (int, float)):
            current_score = 0

        threshold = req.get("required", 0)
        if current_score < threshold:
            gaps.append({
                "capability": capability,
                "current": round(float(current_score), 1),
                "required": round(float(threshold), 1),
                "gap": round(float(threshold - current_score), 1),
                "source": req.get("source"),
                "company": req.get("company"),
                "version": req.get("version"),
                "effective_date": req.get("effective_date"),
            })

    gaps.sort(key=lambda g: g["gap"], reverse=True)
    return gaps


def opportunity_fit(
    learner_state: Dict[str, Any],
    company: str,
    role: Optional[str] = None,
) -> Dict[str, Any]:
    """Compute how well the learner fits a target opportunity.

    Returns:
        Dict with fit_score, gaps, strengths, and recommended actions.
    """
    opportunity = get_opportunity(company, role)
    if not opportunity:
        return {
            "company": company,
            "role": role,
            "fit_score": 0.0,
            "status": "unknown_opportunity",
            "gaps": [],
            "strengths": [],
            "next_actions": [],
        }

    gaps = capability_gaps(learner_state, company, role)
    learner_skills = learner_state.get("skills", {})
    required = required_capabilities(company, role)

    strengths = []
    for capability, req in required.items():
        current = learner_skills.get(capability)
        current_score = current.get("score") if isinstance(current, dict) else (current or 0)
        if not isinstance(current_score, (int, float)):
            current_score = 0
        threshold = req.get("required", 0)
        if current_score >= threshold:
            strengths.append({
                "capability": capability,
                "current": round(float(current_score), 1),
                "required": round(float(threshold), 1),
            })

    # Fit score: inverse of gap severity
    total_gap = sum(g["gap"] for g in gaps)
    max_possible_gap = sum(req.get("required", 0) for req in required.values()) or 1
    fit_score = max(0.0, min(100.0, 100.0 - (total_gap / max_possible_gap * 100)))

    # Status
    if not gaps:
        status = "ready"
    elif len(gaps) <= 2 and all(g["gap"] < 20 for g in gaps):
        status = "almost_ready"
    elif len(gaps) <= 4:
        status = "in_progress"
    else:
        status = "needs_work"

    # Next actions: address biggest gaps first
    next_actions = []
    for gap in gaps[:3]:
        next_actions.append({
            "capability": gap["capability"],
            "action": "repair",
            "priority": "high" if gap["gap"] > 30 else "medium",
            "company": company,
            "version": gap.get("version"),
            "effective_date": gap.get("effective_date"),
        })

    return {
        "company": company,
        "role": role,
        "assessment_variant": opportunity.get("assessment_variant"),
        "version": opportunity.get("version"),
        "effective_date": opportunity.get("effective_date"),
        "fit_score": round(fit_score, 1),
        "status": status,
        "gaps": gaps,
        "strengths": strengths,
        "next_actions": next_actions,
    }


def adaptive_plan(
    learner_state: Dict[str, Any],
    company: Optional[str] = None,
    role: Optional[str] = None,
    deadline_days: Optional[int] = None,
) -> Dict[str, Any]:
    """Generate an adaptive plan based on learner state and target opportunity.

    The planner chooses the highest-impact actions:
    1. Repair critical gaps for target company
    2. Practice weak areas
    3. Advance current capability
    4. Review due SRS cards

    Returns a dict with prioritized actions and time allocation.
    """
    actions = []

    # Company-specific gaps take priority
    if company:
        fit = opportunity_fit(learner_state, company, role)
        for gap in fit.get("gaps", [])[:2]:
            actions.append({
                "type": "repair",
                "capability": gap["capability"],
                "reason": f"Required for {company} (v{fit.get('version', 'latest')})",
                "priority": 1,
            })

    # Weak areas from learner state
    weak_areas = learner_state.get("evidence", {}).get("weak_areas", [])
    for weak in weak_areas[:2]:
        actions.append({
            "type": "practice",
            "capability": weak.get("capability") or weak.get("category"),
            "reason": "Weak area identified",
            "priority": 2,
        })

    # Current world progression
    current_world = learner_state.get("capability", {}).get("current_world")
    current_concept = learner_state.get("capability", {}).get("current_concept")
    if current_concept:
        actions.append({
            "type": "learn",
            "capability": current_concept,
            "reason": f"Current progression: {current_world}/{current_concept}",
            "priority": 3,
        })

    # SRS reviews
    srs_due = learner_state.get("srs", {}).get("due_cards", 0)
    if srs_due > 0:
        actions.append({
            "type": "review",
            "capability": "srs",
            "reason": f"{srs_due} cards due",
            "priority": 4,
        })

    # Sort by priority
    actions.sort(key=lambda a: a["priority"])

    return {
        "company": company,
        "role": role,
        "deadline_days": deadline_days,
        "actions": actions,
        "total_actions": len(actions),
    }
