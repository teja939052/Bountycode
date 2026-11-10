"""Bridge: Study Engine ← service-company sprint curriculum.

Keeps one ordered learning path for India service-company prep.
Worlds / role content remain available as fallback only.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from app.services.service_company_sprint import (
    DOMAIN_ENTRY_LESSON,
    LESSON_DOMAIN,
    daily_focus_plan,
    ordered_lessons,
)


def sprint_plan_for_assessment(
    assessment: Dict[str, Any],
    *,
    mastered_lessons: Optional[Set[str]] = None,
    reviews: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Map adaptive skill assessment → sprint daily_focus_plan."""
    skills = assessment.get("skills") or {}
    weak_domains: List[str] = []
    for domain, evidence in skills.items():
        if not isinstance(evidence, dict):
            continue
        score = float(evidence.get("score") or evidence.get("accuracy") or 0)
        attempts = int(evidence.get("total_attempts") or evidence.get("attempts") or 0)
        # Domain ids may be skill taxonomy ids — map loosely
        domain_key = str(domain)
        if domain_key not in DOMAIN_ENTRY_LESSON:
            # try normalize
            for known in DOMAIN_ENTRY_LESSON:
                if known in domain_key or domain_key in known:
                    domain_key = known
                    break
        if attempts > 0 and score < 70 and domain_key in DOMAIN_ENTRY_LESSON:
            if domain_key not in weak_domains:
                weak_domains.append(domain_key)

    overall = float(
        assessment.get("overall_accuracy")
        or assessment.get("overall_score")
        or 0
    )
    plan = daily_focus_plan(
        mastered=mastered_lessons or set(),
        weak_domains=weak_domains[:4],
        reviews=reviews or [],
        mock_ready=overall >= 55,
    )
    plan["curriculum_source"] = "service_company_sprint"
    plan["ordered_lesson_count"] = len(ordered_lessons())
    plan["weak_domains"] = weak_domains[:5]
    return plan


def task_to_next_mission(task: Dict[str, Any]) -> Dict[str, Any]:
    """Shape a sprint task into Study Engine `next` payload."""
    slug = task.get("slug") or ""
    return {
        "type": task.get("type") or "next_mission",
        "kind": task.get("kind") or "lesson",
        "slug": slug,
        "title": task.get("title") or slug.replace("_", " ").title(),
        "domain": task.get("domain") or LESSON_DOMAIN.get(slug, "programming_fundamentals"),
        "sprint_id": task.get("sprint_id"),
        "sprint_name": task.get("sprint_name"),
        "reason": task.get("reason") or "Next step on the service-company path.",
        "to": task.get("to") or (f"/learn/lesson/{slug}" if slug else "/academy"),
        "estimated_minutes": task.get("estimated_minutes") or 20,
        "curriculum_source": "service_company_sprint",
    }


def tasks_to_practice(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for t in tasks:
        if t.get("kind") in ("weak_area", "practice") or t.get("type") == "practice":
            out.append(
                {
                    "type": "practice",
                    "kind": "weak_area",
                    "slug": t.get("slug"),
                    "domain_id": t.get("domain"),
                    "title": t.get("title"),
                    "reason": t.get("reason"),
                    "to": t.get("to"),
                    "estimated_minutes": t.get("estimated_minutes") or 15,
                    "curriculum_source": "service_company_sprint",
                }
            )
    return out


def company_mock_mission(overall: float) -> Optional[Dict[str, Any]]:
    if overall < 55:
        return None
    return {
        "type": "company_mission",
        "title": "Service-company OA mock",
        "description": "Timed quant / reasoning / verbal / programming logic under real OA pressure.",
        "to": "/service-oa",
        "estimated_minutes": 30,
        "reason": "Measure placement readiness against TCS / Infy / Wipro patterns.",
        "curriculum_source": "service_company_sprint",
    }
