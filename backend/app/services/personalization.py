"""Personalization engine — selects the next best mission/experience.

Priority order:
1. REQUIRED PREREQUISITE
2. FAILED CONCEPT / REPAIR
3. OVERDUE RECALL / SRS
4. TARGET-COMPANY REQUIRED SKILL
5. LOWEST IMPORTANT MASTERY
6. TRANSFER / INTERLEAVING
7. SESSION-TIME FIT

This service is deterministic and does not call LLMs.

Reads from the master curriculum system:
- master_skill_graph (prerequisites, skill relevance)
- role_blueprints (required skills per role)
- company_overlays (company-specific weights)
- pattern_taxonomy (question pattern mapping)

Existing callers continue to receive the same dict shape.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.services.learner_state import get_learner_state
from app.services.opportunity_graph import get_opportunity, required_capabilities

logger = logging.getLogger(__name__)


async def select_next_mission(
    user_id: str,
    company: Optional[str] = None,
    role: Optional[str] = None,
    session_minutes: Optional[int] = None,
) -> Dict[str, Any]:
    """Select the next best learning/practice mission for the learner.

    Returns the same dict shape as the previous implementation so existing
    frontend routes remain compatible.
    """
    state = await get_learner_state(user_id)
    categories = state.get("categories") or {}
    weak_areas = state.get("weak_areas") or []
    misconceptions = state.get("misconceptions") or []
    srs = state.get("srs") or {}
    repair = state.get("repair") or {}

    # 1) REQUIRED PREREQUISITE (from master skill graph)
    prereq = _find_blocked_prerequisite(categories, role)
    if prereq:
        return _mission("prerequisite", prereq, state, {
            "why": "This concept is a prerequisite for material you want to learn.",
            "priority": 1,
        })

    # 2) FAILED CONCEPT / REPAIR
    open_repair = repair.get("open_repairs", 0)
    if open_repair > 0:
        recent = (repair.get("recent_repairs") or [])[0]
        concept = recent.get("concept") if recent else None
        if concept:
            return _mission("repair", concept, state, {
                "why": "Finish your open repair before moving on.",
                "priority": 2,
                "repair_id": recent.get("id"),
            })

    # 3) OVERDUE RECALL / SRS
    due_cards = int(srs.get("due_cards", 0) or 0)
    if due_cards > 0:
        return _mission("srs", weak_areas[0].get("skill") if weak_areas else "recall", state, {
            "why": "You have cards due for review. Spaced repetition protects what you already learned.",
            "priority": 3,
            "due_cards": due_cards,
        })

    # 4) TARGET-COMPANY REQUIRED SKILL (from company_overlays + role_blueprints)
    if company:
        company_req = _company_priority_skill(categories, company, role)
        if company_req:
            return _mission("company_required", company_req, state, {
                "why": f"Your target company/role weights this skill highly.",
                "priority": 4,
                "company": company,
                "role": role,
            })

    # 5) LOWEST IMPORTANT MASTERY (from role blueprint + skill graph)
    if weak_areas:
        bp = _get_role_blueprint(role)
        if bp:
            required_ids = set(bp.required_skills)
            for wa in weak_areas:
                skill_id = wa.get("skill")
                if skill_id in required_ids:
                    return _mission("weak_area", skill_id, state, {
                        "why": "Strengthen a required weak area while it still matters.",
                        "priority": 5,
                        "weak_area": wa,
                    })
        return _mission("weak_area", weak_areas[0].get("skill"), state, {
            "why": "Strengthen a weak area while it still matters.",
            "priority": 5,
            "weak_area": weak_areas[0],
        })

    # 6) TRANSFER / INTERLEAVING
    transfer = _pick_transfer(categories, misconceptions)
    if transfer:
        return _mission("transfer", transfer, state, {
            "why": "Practice applying what you know in a new context.",
            "priority": 6,
        })

    # 7) SESSION-TIME FIT
    if session_minutes is not None and session_minutes < 10:
        return _mission("srs", "recall", state, {
            "why": "Quick review to keep your streak alive.",
            "priority": 7,
        })

    return _mission("explore", "aptitude", state, {
        "why": "Keep exploring the curriculum.",
        "priority": 8,
    })


def _get_role_blueprint(role: Optional[str]) -> Optional[Any]:
    """Resolve the best-matching role blueprint."""
    if not role:
        return None
    try:
        from app.content.role_blueprints import get_role
        return get_role(role)
    except Exception:
        return None


def _find_blocked_prerequisite(categories: Dict[str, Any], role: Optional[str]) -> Optional[str]:
    """Return a skill/concept whose prerequisites are not met, considering role focus."""
    try:
        from app.content.master_skill_graph import get_skills_for_role, get_prerequisites, get_all_skills
        graph = get_all_skills()
        role_skills = get_skills_for_role(role or "software_developer")
        mastered = set()
        for cat_id, cat_data in (categories or {}).items():
            if not isinstance(cat_data, dict):
                continue
            for skill_name, skill_data in (cat_data.get("skills") or {}).items():
                if not isinstance(skill_data, dict):
                    continue
                attempts = int(skill_data.get("attempts", 0) or 0)
                score = float(skill_data.get("score", 0) or 0)
                if attempts > 0 and score >= 60:
                    # Try to match to a graph skill_id
                    for sid, node in graph.items():
                        if node.name.lower() == skill_name.lower() or sid.endswith(skill_name.lower().replace(" ", "_")):
                            mastered.add(sid)
        for node in role_skills:
            if node.skill_id in mastered:
                continue
            prereqs = get_prerequisites(node.skill_id)
            unmet = [p for p in prereqs if p not in mastered]
            if unmet:
                # Return the most upstream unmet prerequisite
                return unmet[0]
    except Exception as exc:
        logger.debug("Prerequisite check failed: %s", exc)
    # Fallback to original simplified logic
    for cat_id, cat_data in (categories or {}).items():
        if not isinstance(cat_data, dict):
            continue
        for skill_name, skill_data in (cat_data.get("skills") or {}).items():
            if not isinstance(skill_data, dict):
                continue
            attempts = int(skill_data.get("attempts", 0) or 0)
            if attempts <= 0:
                continue
            score = float(skill_data.get("score", 0) or 0)
            if score < 40:
                return skill_name
    return None


def _company_priority_skill(
    categories: Dict[str, Any],
    company: str,
    role: Optional[str],
) -> Optional[str]:
    """Return a weak skill that is also high-priority for the target company.

    Uses company_overlays + role_blueprints to find high-relevance skills.
    Falls back to opportunity_graph.get_opportunity for backward compat.
    """
    try:
        opportunity = get_opportunity(company, role)
        if not opportunity:
            return None
        required = opportunity.get("min_skills", {})
        if not required:
            return None

        # Resolve to master graph skill IDs where possible
        bp = _get_role_blueprint(role)
        role_required_ids = set()
        if bp:
            role_required_ids = {s.get("skill_id") for s in bp.required_skills}

        weak_known = []
        for cat_id, cat_data in categories.items():
            if not isinstance(cat_data, dict):
                continue
            for skill_name, skill_data in (cat_data.get("skills") or {}).items():
                if not isinstance(skill_data, dict):
                    continue
                score = float(skill_data.get("score", 0) or 0)
                attempts = int(skill_data.get("attempts", 0) or 0)
                if attempts > 0 and score < 70:
                    # Check if this skill is in company required skills or role required skills
                    is_company_req = skill_name.lower() in {k.lower() for k in required}
                    is_role_req = any(
                        sid.lower().endswith(skill_name.lower().replace(" ", "_"))
                        for sid in role_required_ids
                    )
                    if is_company_req or is_role_req:
                        weak_known.append((score, skill_name))

        weak_known.sort()
        return weak_known[0][1] if weak_known else None
    except Exception:
        return None


def _pick_transfer(
    categories: Dict[str, Any],
    misconceptions: List[Dict[str, Any]],
) -> Optional[str]:
    """Pick a strong skill for transfer practice, or a misconception for repair."""
    if misconceptions:
        return misconceptions[0].get("concept")
    strong = []
    for cat_id, cat_data in categories.items():
        if not isinstance(cat_data, dict):
            continue
        for skill_name, skill_data in (cat_data.get("skills") or {}).items():
            if not isinstance(skill_data, dict):
                continue
            score = float(skill_data.get("score", 0) or 0)
            attempts = int(skill_data.get("attempts", 0) or 0)
            if attempts >= 3 and score >= 80:
                strong.append((score, skill_name))
    strong.sort(reverse=True)
    return strong[0][1] if strong else None


def _mission(
    kind: str,
    concept: Optional[str],
    state: Dict[str, Any],
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "kind": kind,
        "concept": concept,
        "why": meta.get("why", ""),
        "priority": meta.get("priority", 99),
        "company": meta.get("company"),
        "role": meta.get("role"),
        "repair_id": meta.get("repair_id"),
        "due_cards": meta.get("due_cards"),
        "weak_area": meta.get("weak_area"),
        "learner_state": state,
    }
