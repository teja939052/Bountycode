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
    "quantitative_aptitude": "number_systems",
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
ASSESSMENT_TRACK_LABELS = {
    "service_company_core": "Service-company core",
    "tcs_foundation": "TCS Foundation",
    "tcs_advanced": "TCS Advanced",
    "infosys_infytq": "Infosys InfyTQ",
    "hackwithinfy": "HackWithInfy",
    "wipro": "Wipro WILP / NTH",
    "accenture": "Accenture campus",
    "cognizant": "Cognizant GenC",
}
ASSESSMENT_BLUEPRINTS = {
    "service_company_core": {
        "sections": ["Numerical Ability", "Logical Reasoning", "Verbal Ability", "Programming and SQL"],
        "duration_minutes": None,
        "confidence": "Product recommendation",
        "source_label": "Shared service-company foundation",
        "source_url": None,
        "notice": "Use your current employer invitation for the exact sections, timing and eligibility.",
    },
    "tcs_foundation": {
        "sections": ["Numerical Ability", "Verbal Ability", "Reasoning Ability"],
        "duration_minutes": 75,
        "confidence": "Official drive pattern",
        "source_label": "TCS All India NQT drive",
        "source_url": "https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring",
        "notice": "The 75-minute Foundation pattern belongs to the cited TCS drive; verify the current hall ticket.",
    },
    "tcs_advanced": {
        "sections": ["Advanced Quantitative and Reasoning Ability", "Advanced Coding"],
        "duration_minutes": 115,
        "confidence": "Official drive pattern",
        "source_label": "TCS All India NQT drive",
        "source_url": "https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring",
        "notice": "The 115-minute Advanced pattern belongs to the cited TCS drive; verify the current hall ticket.",
    },
    "infosys_infytq": {
        "sections": ["Programming", "DBMS and SQL", "Aptitude", "OOP and DSA"],
        "duration_minutes": None,
        "confidence": "Edition-dependent",
        "source_label": "Infosys InfyTQ",
        "source_url": "https://www.infosys.com/insights/human-potential/industry-grade-certification.html",
        "notice": "InfyTQ patterns change by certification cycle. Use the live Infosys notice as the source of truth.",
    },
    "hackwithinfy": {
        "sections": ["Timed Coding Round", "Constraints and Efficiency"],
        "duration_minutes": 180,
        "confidence": "Official 2026 terms",
        "source_label": "HackWithInfy 2026",
        "source_url": "https://www.infosys.com/careers/hackwithinfy/2026/hwi-terms-conditions.pdf",
        "notice": "The three-hour coding round is specific to the cited 2026 terms and is not a universal Infosys pattern.",
    },
    "wipro": {
        "sections": ["Verbal Ability", "Analytical Ability", "Quantitative Ability", "Written Communication", "Voice Assessment"],
        "duration_minutes": 100,
        "confidence": "Official cohort pattern",
        "source_label": "Wipro WILP cohort listing",
        "source_url": "https://app.joinsuperset.com/company/wipro/wilp.html",
        "notice": "The cited WILP cohort lists 80 minutes online plus a 20-minute voice assessment; verify your cohort invitation.",
    },
    "accenture": {
        "sections": ["Cognitive and Logical Reasoning", "Technical Skills", "Coding", "Communication"],
        "duration_minutes": None,
        "confidence": "Invitation-dependent",
        "source_label": "Accenture India assessment guidance",
        "source_url": "https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture",
        "notice": "Accenture sections and duration depend on the role and invitation; do not treat this as a guaranteed pattern.",
    },
    "cognizant": {
        "sections": ["Communication", "Aptitude", "Role-based Technical Skills"],
        "duration_minutes": None,
        "confidence": "Role-dependent",
        "source_label": "Cognizant GenC process",
        "source_url": "https://careers.cognizant.com/india-en/pathways-to-cognizant/genc-program/",
        "notice": "Cognizant says assessments vary by role. Verify the current candidate-platform communication.",
    },
}
LEVEL_PATH = [
    {"id": 0, "title": "Orientation", "focus": "Profile, diagnostic and exam readiness", "unlock": "Start here"},
    {"id": 1, "title": "Foundations", "focus": "Numerical, verbal, reasoning and programming basics", "unlock": "Build reliable fundamentals"},
    {"id": 2, "title": "Core skills", "focus": "DSA, SQL, OOP, CS concepts and debugging", "unlock": "Apply concepts to varied problems"},
    {"id": 3, "title": "Applied readiness", "focus": "Mixed practice, edge cases and role-specific tasks", "unlock": "Transfer skills across formats"},
    {"id": 4, "title": "Timed performance", "focus": "Sectional drills and employer-style online assessments", "unlock": "Prove speed and accuracy"},
    {"id": 5, "title": "Interview ready", "focus": "Communication, projects, behavioural and technical interviews", "unlock": "Explain and defend your work"},
]


def _level_path(diagnostic: Dict[str, Any] | None, scores: Dict[str, int]) -> tuple[int, List[dict]]:
    observed = [score for score in scores.values() if score >= 0]
    overall = (diagnostic or {}).get("overall_score")
    average = int(overall) if overall is not None else (sum(observed) // len(observed) if observed else -1)
    current = 0 if average < 0 else 1 if average < 35 else 2 if average < 60 else 3 if average < 75 else 4 if average < 85 else 5
    return current, [
        {**level, "status": "complete" if level["id"] < current else "current" if level["id"] == current else "locked"}
        for level in LEVEL_PATH
    ]


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
    current_level, level_path = _level_path(diagnostic, scores)
    assessment_track = str(profile.get("assessment_track", "service_company_core") or "service_company_core").lower()
    assessment_blueprint = ASSESSMENT_BLUEPRINTS.get(assessment_track, ASSESSMENT_BLUEPRINTS["service_company_core"])
    readiness_actions = [
        "Complete your baseline diagnostic before attempting a full mock.",
        "Repair your weakest foundations, then use short sectional practice.",
        "Mix core skills and add edge-case and debugging practice.",
        "Start timed sectional mocks and review speed, accuracy and unanswered items.",
        "Run employer-format mocks, then practise communication and interview answers.",
        "Maintain with mixed transfer practice and rehearse your interview evidence.",
    ]

    return {
        "target_role": role,
        "experience_level": profile.get("experience_level", "absolute_beginner"),
        "learning_preference": learning_preference,
        "learning_strategy": learning_strategy,
        "target_companies": profile.get("target_companies", []),
        "assessment_track": assessment_track,
        "assessment_track_label": ASSESSMENT_TRACK_LABELS.get(assessment_track, ASSESSMENT_TRACK_LABELS["service_company_core"]),
        "assessment_date": profile.get("assessment_date"),
        "assessment_blueprint": assessment_blueprint,
        "assessment_readiness": {
            "stage": "diagnostic" if current_level == 0 else "build" if current_level < 3 else "timed" if current_level < 5 else "interview",
            "action": readiness_actions[current_level],
            "mock_ready": current_level >= 3,
        },
        "weekly_minutes": int(profile.get("daily_minutes", 60)) * int(profile.get("weekly_days", 5)),
        "current_level": current_level,
        "level_path": level_path,
        "company_preparation": matched_tracks,
        "preferred_language": profile.get("preferred_language", "cpp"),
        "daily_minutes": daily_minutes,
        "diagnostic_completed": bool(diagnostic),
        "overall_diagnostic_score": (diagnostic or {}).get("overall_score"),
        "daily_tasks": selected,
        "next_action": selected[0] if selected else {"title": "Complete your diagnostic", "to": "/academy", "reason": "We need evidence before choosing the next level."},
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
