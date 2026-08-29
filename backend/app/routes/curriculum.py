"""Curriculum routes — comprehensive curriculum API for all roles.

Serves:
  - Role curricula with phase-based progression
  - Learning module catalog
  - Company-specific preparation paths
  - Curriculum statistics and progress tracking
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.middleware.auth import get_current_user
from app.content.curriculum.role_curriculum import (
    ROLE_CURRICULA,
    ROLE_DISPLAY_ORDER,
    get_role,
    get_all_roles,
    get_skill_tree,
    get_total_target,
    get_phase_targets,
    CURRICULUM_META,
)
from app.content.curriculum.role_curriculum_v2 import (
    PHASES,
    LEARNING_MODULE_CATALOG,
    COMPANY_PATHS,
    get_phase,
    get_all_phases,
    get_learning_module,
    get_all_learning_modules,
    get_modules_by_phase,
    get_modules_by_topic,
    get_company_path,
    get_all_company_paths,
    get_curriculum_stats,
)

router = APIRouter(prefix="/api/v1/curriculum", tags=["Curriculum"])


# =============================================================
# Pydantic Models
# =============================================================

class RoleSummary(BaseModel):
    role_id: str
    display_name: str
    icon: str
    description: str
    target_companies: List[str]
    estimated_weeks: Optional[int] = None
    total_questions_target: Optional[int] = None
    skill_count: int
    total_target: int
    phases: List[str] = []


class SkillDetail(BaseModel):
    name: str
    target: int
    weight: float
    phase: Optional[str] = None
    prerequisites: List[str] = []
    est_hours: int
    sub_topics: List[str]
    patterns: List[str]
    learning_module_ids: List[str] = []
    company_sources: Dict[str, List[str]] = {}


class PhaseDetail(BaseModel):
    id: str
    name: str
    description: str
    duration_weeks: int
    color: str
    icon: str
    completion_criteria: str
    skills: List[str] = []
    learning_module_ids: List[str] = []
    milestone: Optional[str] = None


class RoleDetail(BaseModel):
    role_id: str
    display_name: str
    icon: str
    description: str
    target_companies: List[str]
    estimated_weeks: Optional[int] = None
    total_questions_target: Optional[int] = None
    skill_tree: Dict[str, Any]
    mock_test: Dict[str, Any]
    progression_phases: Dict[str, Any]
    company_specific_paths: Dict[str, Any] = {}


class LearningModuleSummary(BaseModel):
    id: str
    title: str
    phase: str
    topic: str
    difficulty: str
    estimated_time_minutes: int
    xp_reward: int
    step_count: int


class CompanyPath(BaseModel):
    id: str
    display_name: str
    icon: str
    color: str
    process: List[str]
    focus_skills: List[str]
    question_count: int
    duration_weeks: int
    difficulty_mix: Dict[str, int]
    key_topics: List[str]
    behavioral_focus: str


# =============================================================
# Endpoints
# =============================================================

@router.get("/meta")
async def get_meta():
    """Get curriculum metadata and statistics."""
    return {
        "meta": CURRICULUM_META,
        "stats": get_curriculum_stats(),
        "total_roles": len(ROLE_CURRICULA),
        "total_modules": len(LEARNING_MODULE_CATALOG),
        "total_companies": len(COMPANY_PATHS),
    }


@router.get("/phases")
async def list_phases():
    """List all progression phases."""
    return {"phases": list(PHASES.values())}


@router.get("/roles")
async def list_roles():
    """List all available roles with summaries."""
    roles = []
    for role_id in ROLE_DISPLAY_ORDER:
        role = ROLE_CURRICULA.get(role_id, {})
        if not role:
            continue
        skill_tree = role.get("skill_tree", {})
        phases_data = role.get("progression_phases", {})
        roles.append({
            "role_id": role_id,
            "display_name": role.get("display_name", role_id),
            "icon": role.get("icon", "📚"),
            "description": role.get("description", ""),
            "target_companies": role.get("target_companies", []),
            "estimated_weeks": role.get("estimated_weeks"),
            "total_questions_target": role.get("total_questions_target"),
            "skill_count": len(skill_tree),
            "total_target": sum(s.get("target", 0) for s in skill_tree.values()),
            "phases": list(phases_data.keys()) if phases_data else [],
        })
    return {"roles": roles, "total": len(roles)}


@router.get("/roles/{role_id}")
async def get_role_detail(role_id: str):
    """Get full details for a specific role including skill tree, phases, and company paths."""
    role = get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")

    return {
        "role": role,
        "phase_targets": get_phase_targets(role_id),
        "learning_modules": _resolve_learning_modules_for_role(role),
    }


@router.get("/roles/{role_id}/skill/{skill_id}")
async def get_skill_detail(role_id: str, skill_id: str):
    """Get detailed information about a specific skill in a role."""
    role = get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")

    skill_tree = role.get("skill_tree", {})
    skill = skill_tree.get(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found in role '{role_id}'")

    # Resolve learning modules
    learning_modules = []
    for module_id in skill.get("learning_module_ids", []):
        module = get_learning_module(module_id)
        if module:
            learning_modules.append(module)

    return {
        "skill_id": skill_id,
        "role_id": role_id,
        "skill": skill,
        "learning_modules": learning_modules,
    }


@router.get("/roles/{role_id}/phase/{phase_id}")
async def get_role_phase(role_id: str, phase_id: str):
    """Get the phase configuration for a specific role."""
    role = get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")

    phase_def = get_phase(phase_id)
    if not phase_def:
        raise HTTPException(status_code=404, detail=f"Phase '{phase_id}' not found")

    progression = role.get("progression_phases", {})
    role_phase = progression.get(phase_id, {})

    if not role_phase:
        raise HTTPException(
            status_code=404,
            detail=f"Phase '{phase_id}' not configured for role '{role_id}'"
        )

    # Get skills in this phase
    skills = role_phase.get("skills", [])
    skill_tree = role.get("skill_tree", {})

    phase_skills = []
    for skill_id in skills:
        if skill_id in skill_tree:
            skill_data = skill_tree[skill_id].copy()
            skill_data["skill_id"] = skill_id
            phase_skills.append(skill_data)

    # Get learning modules in this phase
    module_ids = role_phase.get("learning_module_ids", [])
    modules = []
    for module_id in module_ids:
        module = get_learning_module(module_id)
        if module:
            modules.append({**module, "id": module_id})

    return {
        "phase_id": phase_id,
        "phase_definition": phase_def,
        "role_phase": role_phase,
        "skills": phase_skills,
        "learning_modules": modules,
        "total_target": sum(s.get("target", 0) for s in phase_skills),
    }


@router.get("/modules")
async def list_learning_modules(
    phase: Optional[str] = Query(default=None),
    topic: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
):
    """List all learning modules with optional filters."""
    modules = []
    for module_id, module in LEARNING_MODULE_CATALOG.items():
        if phase and module.get("phase") != phase:
            continue
        if topic and module.get("topic") != topic:
            continue
        if difficulty and module.get("difficulty") != difficulty:
            continue

        modules.append({
            "id": module_id,
            "title": module.get("title"),
            "phase": module.get("phase"),
            "topic": module.get("topic"),
            "difficulty": module.get("difficulty"),
            "estimated_time_minutes": module.get("estimated_time_minutes"),
            "xp_reward": module.get("xp_reward"),
            "step_count": len(module.get("steps", [])),
        })

    return {"modules": modules, "total": len(modules)}


@router.get("/modules/{module_id}")
async def get_learning_module_detail(module_id: str):
    """Get full learning module details including all steps."""
    module = get_learning_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail=f"Learning module '{module_id}' not found")

    # Find which roles use this module
    used_in_roles = []
    for role_id, role in ROLE_CURRICULA.items():
        skill_tree = role.get("skill_tree", {})
        for skill_id, skill in skill_tree.items():
            if module_id in skill.get("learning_module_ids", []):
                used_in_roles.append({
                    "role_id": role_id,
                    "role_name": role.get("display_name"),
                    "skill_id": skill_id,
                    "skill_name": skill.get("name"),
                })

    return {
        "id": module_id,
        "module": module,
        "used_in_roles": used_in_roles,
    }


@router.get("/companies")
async def list_companies():
    """List all company-specific preparation paths."""
    companies = []
    for company_id, company in COMPANY_PATHS.items():
        companies.append({
            "id": company_id,
            "display_name": company.get("display_name"),
            "icon": company.get("icon"),
            "color": company.get("color"),
            "question_count": company.get("question_count"),
            "duration_weeks": company.get("duration_weeks"),
            "focus_skills": company.get("focus_skills", []),
        })
    return {"companies": companies, "total": len(companies)}


@router.get("/companies/{company_id}")
async def get_company_detail(company_id: str):
    """Get full company preparation path."""
    company = get_company_path(company_id)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{company_id}' not found")

    # Find which roles target this company
    matching_roles = []
    for role_id, role in ROLE_CURRICULA.items():
        if company_id in [c.lower() for c in role.get("target_companies", [])]:
            matching_roles.append({
                "role_id": role_id,
                "role_name": role.get("display_name"),
                "focus_areas": role.get("company_specific_paths", {}).get(company_id, {}).get("focus_areas", []),
            })

    return {
        "id": company_id,
        "company": company,
        "matching_roles": matching_roles,
    }


@router.get("/stats")
async def get_stats():
    """Get comprehensive curriculum statistics."""
    stats = get_curriculum_stats()

    # Add role statistics
    role_stats = []
    for role_id in ROLE_DISPLAY_ORDER:
        role = ROLE_CURRICULA.get(role_id, {})
        if not role:
            continue
        skill_tree = role.get("skill_tree", {})
        role_stats.append({
            "role_id": role_id,
            "display_name": role.get("display_name"),
            "skill_count": len(skill_tree),
            "total_target": sum(s.get("target", 0) for s in skill_tree.values()),
            "estimated_weeks": role.get("estimated_weeks"),
        })

    stats["roles"] = role_stats
    return stats


@router.get("/path")
async def get_curriculum_path(
    role_id: str = Query(..., description="Target role ID"),
    company: Optional[str] = Query(default=None, description="Target company ID"),
    user=Depends(get_current_user),
):
    """Get a personalized curriculum path for a user targeting a specific role/company."""
    role = get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")

    # Get company-specific path if provided
    company_data = None
    if company:
        company_data = get_company_path(company)
        if not company_data:
            # Check if company is in the role's targets
            role_company = role.get("company_specific_paths", {}).get(company.lower(), {})
            if role_company:
                company_data = {
                    "id": company.lower(),
                    "display_name": company.title(),
                    "focus_areas": role_company.get("focus_areas", []),
                    "question_count": role_company.get("question_count", 100),
                    "duration_weeks": role_company.get("duration_weeks", 4),
                    "key_topics": role_company.get("key_topics", []),
                }

    # Build the full path
    phases_order = ["foundation", "core", "advanced", "job-ready"]
    path = []

    progression = role.get("progression_phases", {})
    for phase_id in phases_order:
        phase_def = get_phase(phase_id)
        role_phase = progression.get(phase_id, {})

        if not phase_def or not role_phase:
            continue

        # Get skills for this phase
        phase_skills = []
        for skill_id in role_phase.get("skills", []):
            skill = role.get("skill_tree", {}).get(skill_id, {})
            if skill:
                phase_skills.append({
                    "skill_id": skill_id,
                    "name": skill.get("name"),
                    "target": skill.get("target", 0),
                    "est_hours": skill.get("est_hours", 0),
                })

        # Get learning modules
        modules = []
        for module_id in role_phase.get("learning_module_ids", []):
            module = get_learning_module(module_id)
            if module:
                modules.append({
                    "id": module_id,
                    "title": module.get("title"),
                    "estimated_time_minutes": module.get("estimated_time_minutes"),
                    "xp_reward": module.get("xp_reward"),
                })

        path.append({
            "phase_id": phase_id,
            "phase_name": phase_def["name"],
            "phase_description": phase_def["description"],
            "duration_weeks": phase_def["duration_weeks"],
            "milestone": role_phase.get("milestone"),
            "skills": phase_skills,
            "learning_modules": modules,
            "total_questions": sum(s.get("target", 0) for s in phase_skills),
        })

    return {
        "role_id": role_id,
        "role_name": role.get("display_name"),
        "company": company_data,
        "path": path,
        "total_weeks": sum(p.get("duration_weeks", 0) for p in path),
        "total_questions": sum(p.get("total_questions", 0) for p in path),
    }


# =============================================================
# Helper Functions
# =============================================================

def _resolve_learning_modules_for_role(role: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect all learning modules referenced by a role's skill tree."""
    module_ids = set()
    for skill in role.get("skill_tree", {}).values():
        for module_id in skill.get("learning_module_ids", []):
            module_ids.add(module_id)

    modules = []
    for module_id in module_ids:
        module = get_learning_module(module_id)
        if module:
            modules.append({
                "id": module_id,
                "title": module.get("title"),
                "phase": module.get("phase"),
                "topic": module.get("topic"),
                "difficulty": module.get("difficulty"),
            })
    return modules
