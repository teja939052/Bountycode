"""Bridge: Study Engine ← service-company sprint curriculum.

Keeps one ordered learning path for India service-company prep.
Worlds / role content remain available as fallback only.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set

from app.services.service_company_sprint import (
    DOMAIN_ENTRY_LESSON,
    LESSON_DOMAIN,
    daily_focus_plan,
    ordered_lessons,
)

logger = logging.getLogger(__name__)


def sprint_plan_for_assessment(
    assessment: Dict[str, Any],
    *,
    mastered_lessons: Optional[Set[str]] = None,
    reviews: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    skills = assessment.get("skills") or {}
    weak_domains: List[str] = []
    for domain, evidence in skills.items():
        if not isinstance(evidence, dict):
            continue
        score = float(evidence.get("score") or evidence.get("accuracy") or 0)
        attempts = int(evidence.get("total_attempts") or evidence.get("attempts") or 0)
        domain_key = str(domain)
        if domain_key not in DOMAIN_ENTRY_LESSON:
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
    plan["overall"] = overall
    return plan


def task_to_next_mission(task: Dict[str, Any]) -> Dict[str, Any]:
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


async def get_today_sprint_first(user_id: str, force_refresh: bool = False) -> Dict[str, Any]:
    """Canonical TODAY: sprint curriculum first; legacy Study Engine for SRS/gamification."""
    from app.services.adaptive_learning import assess_user_skills
    from app.services.study_engine import get_today as legacy_get_today

    # Keep streak / reviews / cache side-effects from legacy engine
    try:
        legacy = await legacy_get_today(user_id, force_refresh=force_refresh)
    except Exception as exc:
        logger.warning("legacy get_today failed: %s", exc)
        legacy = {"date": "", "user_id": user_id, "streak": 0, "level": 1, "reviews": []}

    try:
        assessment = await assess_user_skills(user_id)
    except Exception as exc:
        logger.warning("assess_user_skills failed: %s", exc)
        assessment = {}

    sprint = sprint_plan_for_assessment(
        assessment,
        reviews=legacy.get("reviews") or [],
    )
    tasks = list(sprint.get("tasks") or [])

    next_task = None
    for t in tasks:
        if t.get("type") in ("next_mission", "practice") or t.get("kind") in ("lesson", "weak_area"):
            if t.get("type") == "next_mission" or t.get("kind") == "lesson":
                next_task = t
                break
    if next_task is None and tasks:
        next_task = tasks[0]

    practice = tasks_to_practice(tasks)
    # If practice empty, keep a couple of legacy practice items as soft fallback
    if not practice and legacy.get("practice"):
        practice = list(legacy.get("practice") or [])[:2]

    overall = float(sprint.get("overall") or assessment.get("overall_score") or 0)
    company = company_mock_mission(overall)
    # Prefer explicit sprint company mock task if present
    for t in tasks:
        if t.get("type") == "company_mission":
            company = {
                **t,
                "to": t.get("to") or "/service-oa",
                "curriculum_source": "service_company_sprint",
            }
            break

    next_payload = task_to_next_mission(next_task) if next_task else legacy.get("next")

    est = 0
    task_count = 0
    if next_payload:
        est += int(next_payload.get("estimated_minutes") or 12)
        task_count += 1
    reviews = legacy.get("reviews") or []
    est += sum(int(r.get("estimated_minutes") or 5) for r in reviews)
    task_count += len(reviews)
    est += sum(int(t.get("estimated_minutes") or 10) for t in practice)
    task_count += len(practice)
    if company:
        est += int(company.get("estimated_minutes") or 30)
        task_count += 1

    return {
        **legacy,
        "next": next_payload,
        "practice": practice,
        "company_mission": company,
        "sprint": {
            "title": sprint.get("title"),
            "sprints": sprint.get("sprints"),
            "weak_domains": sprint.get("weak_domains"),
            "ordered_lesson_count": sprint.get("ordered_lesson_count"),
            "tasks": tasks,
        },
        "curriculum_source": "service_company_sprint",
        "overall_score": overall or legacy.get("overall_score"),
        "totals": {"estimated_minutes": est, "task_count": task_count},
    }
