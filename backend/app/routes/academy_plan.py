"""Deterministic personalized learning plan built from profile + diagnostic evidence."""
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_collection, srs_cards_collection
from app.middleware.auth import get_current_user
from app.services.learning_paths import get_all_company_tracks
from app.services.adaptive_learning import assess_user_skills
from app.services.spaced_repetition import deserialize_state, get_due_cards

router = APIRouter(prefix="/api/v1/academy/plan", tags=["academy-plan"])
_profiles = lambda: get_collection("academy_learner_profiles")
_diagnostics = lambda: get_collection("academy_diagnostic_sessions")
_plans = lambda: get_collection("academy_learning_plans")

LESSON_BY_DOMAIN = {
    "programming_fundamentals": "programming_languages",
    "arrays_hashing": "arrays_basics",
    "quantitative_aptitude": "arithmetic_algebra",
    "logical_reasoning": "logical_puzzles",
    "verbal_ability": "reading_comprehension",
    "computer_science": "dbms_basics",
    "sql": "sql_select_basics",
}
DOMAIN_PREREQUISITES = {
    "arrays_hashing": ["programming_fundamentals"],
    "sql": ["programming_fundamentals"],
    "computer_science": ["programming_fundamentals"],
}
ROLE_SKILLS = {
    "software_engineer": ["programming_fundamentals", "arrays_hashing", "computer_science", "sql"],
    "full_stack_developer": ["programming_fundamentals", "arrays_hashing", "sql", "computer_science"],
    "backend_developer": ["programming_fundamentals", "arrays_hashing", "sql", "computer_science"],
    "frontend_developer": ["programming_fundamentals", "arrays_hashing", "verbal_ability"],
    "qa_engineer": ["programming_fundamentals", "sql", "logical_reasoning", "computer_science"],
    "data_analyst": ["sql", "quantitative_aptitude", "programming_fundamentals"],
    "devops_engineer": ["programming_fundamentals", "computer_science", "logical_reasoning"],
    "support_engineer": ["programming_fundamentals", "logical_reasoning", "verbal_ability"],
    "undecided": ["programming_fundamentals", "arrays_hashing", "quantitative_aptitude", "logical_reasoning"],
}


def build_plan(profile: Dict[str, Any], diagnostic: Dict[str, Any] | None, company_tracks: List[dict] | None = None, adaptive_skills: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Prioritize weak prerequisite skills, then role-specific skills."""
    skills = (diagnostic or {}).get("skills", [])
    diagnostic_scores = {item.get("domain"): int(item.get("score", 0)) for item in skills}
    adaptive_skills = adaptive_skills or {}
    scores = {
        domain: int(evidence.get("score", 0)) if int(evidence.get("total_attempts", 0) or 0) > 0 else diagnostic_scores.get(domain, -1)
        for domain, evidence in adaptive_skills.items()
    }
    for domain, score in diagnostic_scores.items():
        scores.setdefault(domain, score)
    role = profile.get("target_role", "undecided")
    desired = list(dict.fromkeys(ROLE_SKILLS.get(role, ROLE_SKILLS["undecided"])))
    for item in skills:
        domain = item.get("domain")
        if domain and domain not in desired:
            desired.append(domain)

    prioritized = sorted(
        desired,
        key=lambda domain: (scores.get(domain, -1), desired.index(domain)),
    )
    tasks: List[dict] = []
    for domain in prioritized:
        score = scores.get(domain)
        if score is None or score < 0:
            state = "not_assessed"
        elif score < 35:
            state = "foundation_needed"
        elif score < 60:
            state = "beginner"
        elif score < 80:
            state = "developing"
        else:
            state = "strong"
        tasks.append({
            "domain": domain,
            "title": domain.replace("_", " ").title(),
            "lesson_slug": LESSON_BY_DOMAIN.get(domain),
            "estimated_minutes": 20 if state in {"foundation_needed", "not_assessed"} else 15,
            "priority": "high" if state in {"foundation_needed", "not_assessed"} else "normal",
            "skill_level": state,
            "diagnostic_score": diagnostic_scores.get(domain),
            "adaptive_score": scores.get(domain) if domain in adaptive_skills and int(adaptive_skills[domain].get("total_attempts", 0) or 0) > 0 else None,
            "effective_score": None if scores.get(domain, -1) < 0 else scores[domain],
            "prerequisites": DOMAIN_PREREQUISITES.get(domain, []),
            "reason": (
                "Start with this foundation before advanced topics."
                if state in {"foundation_needed", "not_assessed"}
                else "Build consistency and improve problem-solving accuracy."
                if state in {"beginner", "developing"}
                else "Maintain this skill with mixed company-style practice."
            ),
        })

    target_companies = set(profile.get("target_companies", []))
    matched_tracks = [
        {"id": track["id"], "company_id": track["company_id"], "name": track["name"], "description": track.get("description", "")}
        for track in (company_tracks or [])
        if track.get("company_id") in target_companies
    ]
    daily_minutes = int(profile.get("daily_minutes", 60))
    budget = max(15, daily_minutes)
    selected = []
    used = 0
    for task in tasks:
        if used + task["estimated_minutes"] <= budget or not selected:
            selected.append(task)
            used += task["estimated_minutes"]
    return {
        "target_role": role,
        "target_companies": profile.get("target_companies", []),
        "company_preparation": matched_tracks,
        "preferred_language": profile.get("preferred_language", "cpp"),
        "daily_minutes": daily_minutes,
        "diagnostic_completed": bool(diagnostic),
        "overall_diagnostic_score": (diagnostic or {}).get("overall_score"),
        "daily_tasks": selected,
        "curriculum": tasks,
        "study_routine": [
            {"label": "Review yesterday's concepts", "minutes": min(10, max(5, budget // 6))},
            {"label": "Learn the next concept", "minutes": max(5, budget // 3)},
            {"label": "Solve guided and independent problems", "minutes": max(5, budget // 3)},
            {"label": "Check understanding and revise mistakes", "minutes": max(0, budget - (min(10, max(5, budget // 6)) + 2 * max(5, budget // 3)))},
        ],
        "personalization_note": (
            "Complete the baseline diagnostic to replace self-reported levels with skill evidence."
            if not diagnostic else
            "Tasks are prioritized using your diagnostic results and selected role."
        ),
    }


@router.get("")
async def get_personalized_plan(user=Depends(get_current_user)):
    profile_doc = await _profiles().find_one({"user_id": user["id"]})
    if not profile_doc or not profile_doc.get("onboarding_complete"):
        raise HTTPException(status_code=409, detail="Complete your learner profile first.")
    diagnostic_doc = await _diagnostics().find_one(
        {"user_id": user["id"], "status": "completed"},
        sort=[("completed_at", -1)],
    )
    diagnostic = (diagnostic_doc or {}).get("result")
    skill_assessment = await assess_user_skills(user["id"])
    plan = build_plan(profile_doc, diagnostic, get_all_company_tracks(), skill_assessment.get("skills", {}))
    plan["overall_mastery"] = skill_assessment.get("overall_mastery_label")
    plan["overall_accuracy"] = skill_assessment.get("overall_accuracy")
    stored_cards = await srs_cards_collection().find({"user_id": user["id"]}).to_list(500)
    review_states = []
    for card in stored_cards:
        try:
            review_states.append(deserialize_state(card))
        except Exception:
            continue
    due_cards = get_due_cards(review_states, limit=5)
    plan["revision"] = {
        "due_count": len(get_due_cards(review_states, limit=500)),
        "sample_problem_ids": [card.concept_id for card in due_cards],
    }
    plan["generated_at"] = datetime.now(timezone.utc).isoformat()
    await _plans().update_one(
        {"user_id": user["id"]},
        {"$set": {"user_id": user["id"], "plan": plan, "updated_at": datetime.now(timezone.utc)}},
        upsert=True,
    )
    return {"success": True, "plan": plan}
