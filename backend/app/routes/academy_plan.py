"""Deterministic personalized learning plan built from profile + diagnostic evidence."""
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_collection, srs_cards_collection
from app.middleware.auth import get_current_user
from app.services.learning_paths import get_all_company_tracks
from app.services.adaptive_learning import assess_user_skills
from app.services.spaced_repetition import deserialize_state, get_due_cards
from app.services.service_company_sprint import DOMAIN_ENTRY_LESSON, daily_focus_plan

router = APIRouter(prefix="/api/v1/academy/plan", tags=["academy-plan"])
_profiles = lambda: get_collection("academy_learner_profiles")
_diagnostics = lambda: get_collection("academy_diagnostic_sessions")
_plans = lambda: get_collection("academy_learning_plans")

# Prefer sprint entry lessons so Academy plan and Study Engine stay aligned.
LESSON_BY_DOMAIN = {
    **DOMAIN_ENTRY_LESSON,
    "programming_fundamentals": "variables_basics",
    "arrays_hashing": "arrays_basics",
    "quantitative_aptitude": "percentages",
    "logical_reasoning": "number_series",
    "verbal_ability": "reading_comprehension",
    "computer_science": "oops_basics",
    "sql": "dbms_basics",
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
    # Service-company default spine for campus placement aspirants.
    "undecided": ["programming_fundamentals", "quantitative_aptitude", "logical_reasoning", "verbal_ability", "arrays_hashing"],
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

    ordered: List[str] = []
    remaining = list(prioritized)
    while remaining:
        progressed = False
        for domain in list(remaining):
            prerequisites = [
                prerequisite
                for prerequisite in DOMAIN_PREREQUISITES.get(domain, [])
                if prerequisite in remaining
                and scores.get(prerequisite, -1) < 60
            ]
            if prerequisites and not all(item in ordered for item in prerequisites):
                continue
            ordered.append(domain)
            remaining.remove(domain)
            progressed = True
            break
        if not progressed:
            ordered.extend(remaining)
            break
    prioritized = ordered
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
                "Build this foundation before moving to dependent topics."
                if state in {"foundation_needed", "not_assessed"}
                else "Build consistency and improve problem-solving accuracy."
                if state in {"beginner", "developing"}
                else "Maintain this skill with mixed company-style practice."
            ),
            "prerequisite_status": (
                "complete"
                if all(scores.get(item, -1) >= 60 for item in DOMAIN_PREREQUISITES.get(domain, []))
                else "needs_foundation"
                if DOMAIN_PREREQUISITES.get(domain)
                else "none"
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

    # Sprint overlay: ordered focus tasks for service-company learners.
    weak_domains = [
        t["domain"] for t in selected
        if t.get("skill_level") in {"foundation_needed", "not_assessed", "beginner", "developing"}
    ]
    sprint_focus = daily_focus_plan(weak_domains=weak_domains, mock_ready=False)

    learning_preference = str(profile.get("learning_preference", "mixed") or "mixed").lower()
    routine_labels = {
        "mixed": ["Review previous mistakes", "Learn the next concept", "Solve guided and independent problems", "Check understanding and revise"],
        "examples_first": ["Recall one previous example", "Study a worked example", "Solve a similar problem independently", "Compare your reasoning and revise"],
        "hands_on": ["Warm up with a recall prompt", "Attempt a guided exercise", "Build or debug a small solution", "Review feedback and note the lesson"],
        "visual": ["Recall the last concept", "Trace a diagram, state or code path", "Practise with a visual trace", "Summarize the pattern you observed"],
        "reading": ["Review notes and revision cards", "Read the concept explanation", "Work through examples and exercises", "Write a short summary from memory"],
    }
    routine = routine_labels.get(learning_preference, routine_labels["mixed"])
    review_minutes = min(10, max(5, budget // 6))
    concept_minutes = max(5, budget // 3)
    practice_minutes = max(5, budget // 3)
    routine_minutes = [review_minutes, concept_minutes, practice_minutes, max(0, budget - review_minutes - concept_minutes - practice_minutes)]
    learning_strategy = {
        "mixed": "Combine clear explanations, worked examples and independent practice.",
        "examples_first": "Start with a solved example, understand each decision, then solve a similar problem yourself.",
        "hands_on": "Attempt guided tasks early, use hints progressively and read the explanation after each attempt.",
        "visual": "Follow concrete traces, state changes and step-by-step examples before generalizing the rule.",
        "reading": "Read the concept guide, key terms and common misconceptions, then recall and apply the idea.",
    }.get(learning_preference, "Combine clear explanations, worked examples and independent practice.")

    return {
        "target_role": role,
        "experience_level": profile.get("experience_level", "absolute_beginner"),
        "learning_preference": learning_preference,
        "learning_strategy": learning_strategy,
        "target_companies": profile.get("target_companies", []),
        "company_preparation": matched_tracks,
        "preferred_language": profile.get("preferred_language", "cpp"),
        "daily_minutes": daily_minutes,
        "diagnostic_completed": bool(diagnostic),
        "overall_diagnostic_score": (diagnostic or {}).get("overall_score"),
        "daily_tasks": selected,
        "curriculum": tasks,
        "sprint_focus": sprint_focus,
        "study_routine": [
            {"label": label, "minutes": minutes}
            for label, minutes in zip(routine, routine_minutes)
        ],
        "personalization_note": (
            "Complete the baseline diagnostic to replace self-reported levels with skill evidence."
            if not diagnostic else
            "Tasks follow diagnostic evidence and the service-company sprint order. "
            "Your learning preference shapes presentation; skill order follows assessed evidence."
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
