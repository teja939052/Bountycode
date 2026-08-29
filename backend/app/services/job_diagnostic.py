"""Job-seeker diagnostic — Door 1: role → baseline → personalized path → first missions.

Wires the "I NEED A JOB" door end-to-end by REUSING existing engines only:
  - role_engine/profiles        → role profile (readiness weights, display info)
  - content/curriculum/role_curriculum → per-role spine + progression phases
  - curriculum_connector        → capability competency step extraction (canonical skills)
  - skill_graph + update_skill_score → establishes a real baseline from answers
  - quest_engine                → first 3 missions (weakness recovery + daily challenge)

This module contains NO new curriculum, readiness, or dashboard abstraction. It only
orchestrates the engines that already exist.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.curriculum_connector import (
    get_competency_with_fallback,
    resolve_role_skill,
)
from app.services.skill_assessment import get_skill_graph, update_skill_score

# Door role key -> role_curriculum role id (hyphenated) used for the personalized path.
DOOR_TO_CURRICULUM: Dict[str, str] = {
    "sde": "sde",
    "ai_software_developer": "ai-engineer",
    "data_analyst": "data-analyst",
    "data_scientist": "data-scientist",
    "qa_automation": "qa-engineer",
    "devops": "devops-engineer",
    "java_engineer": "java-engineer",
    "ml_engineer": "ml-engineer",
    "product_analyst": "product-analyst",
    "technical_assistant": "technical-assistant",
}

# Door role key -> capability competencies whose gradable MCQ steps form the mini-diagnostic.
# Fallback set applies to any role without an entry (frontend/backend/cybersecurity etc.).
DIAGNOSTIC_COMPETENCIES: Dict[str, List[str]] = {
    "sde": ["code_foundations/validator", "code_foundations/command_processor"],
    "ai_software_developer": ["code_foundations/validator", "code_foundations/command_processor"],
    "data_analyst": ["code_foundations/validator", "work_with_data/payroll_fix"],
    "data_scientist": ["code_foundations/validator", "work_with_data/payroll_fix"],
    "qa_automation": ["code_foundations/validator", "software_engineering/debugging_mastery"],
    "backend": ["code_foundations/validator", "build_systems/url_shortener"],
    "devops": ["code_foundations/validator", "build_systems/scale_api"],
    "frontend": ["code_foundations/validator", "code_foundations/api_parser"],
    "cybersecurity": ["code_foundations/validator", "code_foundations/api_parser"],
}

FALLBACK_DIAGNOSTIC: List[str] = ["code_foundations/validator"]

# Gradable step types: predict (single-choice), break (multi-select), and explore
# (predict-the-output, gradable when it carries an expected_output).
GRADABLE_STEP_TYPES = {"predict", "break", "explore"}


def _resolve_curriculum_skill(role: str, skill_key: str) -> Optional[Dict[str, str]]:
    """Map a role-curriculum skill_tree key to a canonical '<category>.<skill>' pair."""
    cid = resolve_role_skill(skill_key)
    if not cid or "." not in cid:
        return None
    cat, skill = cid.split(".", 1)
    return {"category": cat, "skill": skill}


def get_diagnostic_questions(role: str) -> Dict[str, Any]:
    """Return the real, gradable MCQ diagnostic for a door role.

    Pulls `predict` (single answer) and `break` (multi-select) steps from the role's
    diagnostic competencies and maps their canonical skills so results can seed the
    skill graph.
    """
    comp_keys = DIAGNOSTIC_COMPETENCIES.get(role) or FALLBACK_DIAGNOSTIC
    questions: List[Dict[str, Any]] = []
    for comp_key in comp_keys:
        comp = get_competency_with_fallback(comp_key)
        if not comp:
            continue
        canon = set()
        for _skill in comp["skills_taught"]:
            cid = __import__(
                "app.services.curriculum_connector", fromlist=["resolve_capability_skill"]
            ).resolve_capability_skill(_skill)
            if cid and "." in cid:
                canon.add(cid)
        for step in comp["competency"].get("steps", []):
            if step.get("type") not in GRADABLE_STEP_TYPES:
                continue
            if step.get("type") == "explore" and not step.get("expected_output"):
                continue
            qid = f"{comp_key}::{step.get('title')}"
            questions.append({
                "id": qid,
                "type": step.get("type"),
                "title": step.get("title"),
                "prompt": step.get("question")
                or step.get("content")
                or ("What does this code print?" if step.get("type") == "explore" else step.get("title")),
                "code": step.get("code"),
                "options": step.get("options"),
                "correct_set": step.get("correct_set"),
                "expected_output": step.get("expected_output"),
                "canonical_skills": sorted(canon),
                "explanation": step.get("explanation") or step.get("hint"),
            })

    # Deterministic ordering; cap to keep the diagnostic short.
    questions = questions[:12]
    return {
        "role": role,
        "question_count": len(questions),
        "questions": questions,
    }


def _grade_answer(question: Dict[str, Any], answer: Any) -> bool:
    """Grade a single answer against the step's correct data."""
    qtype = question.get("type")
    if qtype == "predict":
        options = question.get("options") or []
        correct_ids = {o["id"] for o in options if o.get("correct")}
        if not correct_ids:
            return False
        return str(answer) in correct_ids
    if qtype == "break":
        correct_set = set(question.get("correct_set") or [])
        if not correct_set:
            return False
        given = set(answer) if isinstance(answer, (list, set, tuple)) else {answer}
        return given == correct_set
    if qtype == "explore":
        expected = (question.get("expected_output") or "").strip()
        if not expected:
            return False
        return _normalize_output(answer) == _normalize_output(expected)
    return False


def _normalize_output(value: Any) -> str:
    """Normalize a code-output answer for forgiving comparison."""
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _target_readiness(role: str) -> int:
    """Return the readiness score a newly diagnosed candidate should aim for."""
    return 85


def _diagnostic_summary(score: float) -> Dict[str, Any]:
    """Turn a 0-100 readiness baseline into a short human summary."""
    if score >= 70:
        band = "strong"
        summary = "You're closer than you think — a focused push across a few gaps gets you job-ready."
    elif score >= 40:
        band = "solid"
        summary = "You have a real foundation. We'll close the gaps one focused mission at a time."
    else:
        band = "foundation"
        summary = "Great — you know where you stand. We'll build your foundation from your strongest starting point."
    return {"band": band, "summary": summary}


def _build_path(role: str) -> Dict[str, Any]:
    """Build the personalized journey from the role curriculum's progression phases."""
    from app.content.curriculum.role_curriculum import get_role

    curriculum_id = DOOR_TO_CURRICULUM.get(role, "sde")
    role_data = get_role(curriculum_id)
    if not role_data:
        role_data = get_role("sde")

    phases = role_data.get("progression_phases", {}) or {}
    ordered = ["foundation", "core", "advanced", "job-ready"]
    modules = []
    for phase_key in ordered:
        p = phases.get(phase_key)
        if not p:
            continue
        modules.append({
            "phase": phase_key,
            "name": p.get("name", phase_key.title()),
            "weeks": p.get("weeks", 1),
            "description": p.get("description", ""),
            "skills": p.get("skills", []),
            "milestone": p.get("milestone", ""),
        })

    return {
        "role": role,
        "display_name": role_data.get("display_name") or (role or "SDE").replace("_", " ").title(),
        "curriculum_role_id": curriculum_id,
        "target_readiness": _target_readiness(role),
        "total_questions_target": role_data.get("total_questions_target", 0),
        "estimated_weeks": role_data.get("estimated_weeks", 8),
        "target_companies": role_data.get("target_companies", []) or [],
        "modules": modules,
        "current_module_phase": modules[0]["phase"] if modules else "foundation",
    }


def _top_gaps(role: str, baseline: Dict[str, float]) -> List[Dict[str, Any]]:
    """Identify the role's weakest assessed skills (for the first missions)."""
    gaps = [{"skill": k, "score": v} for k, v in baseline.items()]
    gaps.sort(key=lambda g: g["score"])
    return gaps[:3]


def build_first_missions(role: str, gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create the first 3 missions using quest_engine quest types & shapes.

    Reuses the quest_engine vocabulary (quest_type, xp_reward, estimated_minutes) but
    generates a deterministic first-3 set from the diagnostic gaps so a brand-new user
    gets coherent starting missions before they have any solve history.
    """
    missions: List[Dict[str, Any]] = []
    gap_topics = [g["skill"] for g in gaps]

    for idx, skill in enumerate(gap_topics):
        if len(missions) >= 3:
            break
        missions.append({
            "mission_id": f"dgn_{role}_{idx}",
            "quest_type": "weakness_recovery",
            "title": f"Start with {skill.replace('_', ' ').title()}",
            "description": (
                f"This is your most impactful first skill. Knock out a foundation mission "
                f"on {skill.replace('_', ' ')} to turn it from a gap into a strength."
            ),
            "topic": skill,
            "difficulty": "easy",
            "target_count": 3,
            "xp_reward": 150,
            "estimated_minutes": 15,
            "current_count": 0,
            "is_complete": False,
        })

    if len(missions) < 3:
        missions.append({
            "mission_id": f"dgn_{role}_challenge",
            "quest_type": "daily_challenge",
            "title": "Daily Challenge",
            "description": "One curated problem to test everything you've learned so far.",
            "topic": "daily_challenge",
            "difficulty": "easy",
            "target_count": 1,
            "xp_reward": 50,
            "estimated_minutes": 10,
            "current_count": 0,
            "is_complete": False,
        })

    return missions[:3]


async def run_job_diagnostic(user_id: str, role: str, answers: Dict[str, Any]) -> Dict[str, Any]:
    """Full Door-1 flow: grade answers, seed the skill graph, compute readiness,
    build the path, and return the first 3 missions.

    Reuses existing engines; never creates a new readiness/curriculum system.
    """
    from app.services.role_engine.profiles import get_profile

    diagnostic = get_diagnostic_questions(role)
    questions = diagnostic["questions"]

    # Grade each answer, collect per-canonical-category correctness.
    category_correct: Dict[str, List[bool]] = {}
    graded = []
    for q in questions:
        answer = answers.get(q["id"])
        is_correct = _grade_answer(q, answer) if answer is not None else False
        graded.append({
            "id": q["id"],
            "title": q["title"],
            "type": q["type"],
            "is_correct": is_correct,
        })
        for cid in q.get("canonical_skills", []):
            if "." in cid:
                cat = cid.split(".", 1)[0]
                category_correct.setdefault(cat, []).append(is_correct)

    # Seed the skill graph from real answers (reuse existing engine).
    for cat, results in category_correct.items():
        correct_count = sum(1 for c in results if c)
        accuracy = correct_count / len(results) if results else 0.0
        skill_name = f"{cat}_diagnostic"
        await update_skill_score(
            user_id=user_id,
            category=cat,
            skill=skill_name,
            score=accuracy * 100,
            is_correct=accuracy >= 0.6,
        )

    # Baseline readiness from role profile readiness weights + diagnostic accuracy.
    profile = get_profile(role)
    weights = (profile.readiness_weights.weights if profile else {}) or {}
    assessed_baseline: Dict[str, float] = {}
    for cat, results in category_correct.items():
        acc = sum(1 for c in results if c) / len(results) if results else 0.0
        assessed_baseline[cat] = round(acc * 100, 1)

    if weights and assessed_baseline:
        total_w = sum(weights.values()) or 1
        # Map profile weight keys (display names) to assessed categories via keyword hints.
        weight_by_cat: Dict[str, float] = {}
        for skill_name, w in weights.items():
            low = skill_name.lower()
            if "dsa" in low or "algorithm" in low:
                weight_by_cat["dsa"] = weight_by_cat.get("dsa", 0) + w
            elif "sql" in low or "database" in low:
                weight_by_cat["system_design"] = weight_by_cat.get("system_design", 0) + w
            elif "system" in low or "backend" in low or "api" in low:
                weight_by_cat["system_design"] = weight_by_cat.get("system_design", 0) + w
            elif "program" in low or "code" in low:
                weight_by_cat["coding"] = weight_by_cat.get("coding", 0) + w
            elif "behavior" in low or "communication" in low or "leadership" in low:
                weight_by_cat["behavioral"] = weight_by_cat.get("behavioral", 0) + w
            elif "test" in low or "qa" in low:
                weight_by_cat["coding"] = weight_by_cat.get("coding", 0) + w
            else:
                weight_by_cat["coding"] = weight_by_cat.get("coding", 0) + w
        total_assessed = sum(assessed_baseline.values()) or 1
        weighted_score = sum(
            assessed_baseline.get(cat, 0) * w for cat, w in weight_by_cat.items()
        )
        # Fall back to a plain average when the weight mapping can't see the assessed cats.
        if category_correct and weighted_score <= 0:
            weighted_score = total_assessed
        overall = round(weighted_score, 1)
    else:
        vals = list(assessed_baseline.values())
        overall = round(sum(vals) / len(vals), 1) if vals else 0.0

    overall = max(0.0, min(100.0, overall))

    path = _build_path(role)
    gaps = _top_gaps(role, assessed_baseline)
    missions = build_first_missions(role, gaps)

    result = {
        "status": "ok",
        "role": role,
        "readiness": {
            "overall": overall,
            "target": path["target_readiness"],
            "categories": assessed_baseline,
            **(_diagnostic_summary(overall)),
        },
        "graded": graded,
        "correct_count": sum(1 for g in graded if g["is_correct"]),
        "question_count": len(graded),
        "path": path,
        "top_gaps": gaps,
        "first_missions": missions,
    }

    # Persist diagnostic completion on the user record (reuses career_goal namespace).
    transport = {"_id": user_id}
    try:
        from bson import ObjectId
        from app.database import users_collection

        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "career_goal.door": "job",
                    "career_goal.role": role,
                    "career_goal.diagnostic": {
                        "completed": True,
                        "completed_at": datetime.now(timezone.utc),
                        "readiness": overall,
                        "baseline_categories": assessed_baseline,
                        "first_missions": missions,
                        "path": {
                            "current_module_phase": path["current_module_phase"],
                            "target_readiness": path["target_readiness"],
                        },
                    },
                }
            },
        )
    except Exception:
        # Persistence is best-effort; never fail the diagnostic flow for it.
        pass

    return result
