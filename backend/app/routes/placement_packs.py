from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Optional
from datetime import datetime, timezone
from app.middleware.auth import get_current_user
from app.content.curriculum.sde_placement_pack import (
    COMPANY_BLUEPRINTS,
    SDE_SKILL_TREE,
    TOTAL_SDE_QUESTIONS_TARGET,
)
from app.content.curriculum.role_curriculum import (
    ROLE_CURRICULA,
    ROLE_DISPLAY_ORDER,
)
import os
import json
from app.database import interview_bookings_collection
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
LEARNING_OBJECTS_PATH = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "learning_objects.json"
LEARNING_PATHS_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "learning_paths.json"
FINAL_CURRICULUM_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "final_curriculum.json"
MOCK_TESTS_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "mock_tests.json"
ALL_ROLES_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "all_role_curricula.json"

router = APIRouter(prefix="/api/v1/placement-packs", tags=["placement-packs"])


@router.get("/sde")
async def get_sde_placement_pack(
    user=Depends(get_current_user),
):
    """Get the SDE skill progression tree with question targets."""
    return {
        "role": "SDE",
        "skill_tree": SDE_SKILL_TREE,
        "total_questions_target": sum(s["question_target"] for s in SDE_SKILL_TREE.values()),
    }


@router.get("/companies")
async def get_company_blueprints(
    user=Depends(get_current_user),
):
    """List all available company blueprints."""
    return {
        "companies": [
            {
                "company_id": c["company_id"],
                "display_name": c["display_name"],
                "icon": c.get("icon", ""),
                "focus_areas_count": len(c.get("focus_areas", [])),
                "process_steps": len(c.get("process", [])),
            }
            for c in COMPANY_BLUEPRINTS.values()
        ]
    }


@router.get("/companies/{company_id}")
async def get_company_blueprint(
    company_id: str,
    user=Depends(get_current_user),
):
    """Get full blueprint for a specific company (requires Pro for full access)."""
    blueprint = COMPANY_BLUEPRINTS.get(company_id.lower())
    if not blueprint:
        raise HTTPException(
            status_code=404,
            detail=f"No placement blueprint found for '{company_id}'",
        )

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    if not is_pro:
        # Free users get overview + first step only
        return {
            "company_id": blueprint["company_id"],
            "display_name": blueprint["display_name"],
            "icon": blueprint.get("icon", ""),
            "color": blueprint.get("color", ""),
            "assessment_ready_score": 0,
            "focus_areas": blueprint.get("focus_areas", [])[:2],
            "process": blueprint.get("process", [])[:1],
            "source_type": blueprint.get("source_type", {}),
            "upgrade_message": (
                f"Unlock the full {blueprint['display_name']} placement pack "
                "with a Pro Pass for company-specific OAs, mock interviews, "
                "and readiness tracking."
            ),
        }

    return blueprint


@router.get("/learning-objects")
async def get_learning_objects(
    limit: int = Query(50, ge=1, le=200),
    topic: Optional[str] = Query(None),
    user=Depends(get_current_user),
):
    """List learning objects for the SDE skill tree.

    Free users see only placement_grade learning objects.
    Pro/Lifetime users see all enriched learning objects.
    """
    if not LEARNING_OBJECTS_PATH.exists():
        return {"learning_objects": [], "total": 0}

    with open(LEARNING_OBJECTS_PATH, "r", encoding="utf-8") as f:
        los = json.load(f)

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    if not is_pro:
        los = [lo for lo in los if lo.get("review_status") == "placement_grade"]

    if topic:
        los = [lo for lo in los if topic.lower() in (lo.get("topic", "") or "").lower()]

    total = len(los)
    los = los[:limit]

    return {
        "learning_objects": los,
        "total": total,
        "is_pro": is_pro,
    }


@router.get("/learning-objects/{lo_id}")
async def get_learning_object(
    lo_id: str,
    user=Depends(get_current_user),
):
    """Fetch a single learning object by ID."""
    if not LEARNING_OBJECTS_PATH.exists():
        raise HTTPException(404, "Learning objects not found")

    with open(LEARNING_OBJECTS_PATH, "r", encoding="utf-8") as f:
        los = json.load(f)

    lo = None
    for item in los:
        if item.get("id") == lo_id or item.get("learning_object", {}).get("id") == lo_id:
            lo = item
            break

    if not lo:
        raise HTTPException(404, "Learning object not found")

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")
    if not is_pro and lo.get("review_status") != "placement_grade":
        raise HTTPException(
            status_code=402,
            detail="This learning object requires a Pro Pass.",
        )

    return lo


@router.get("/curation-health")
async def get_curation_health(
    user=Depends(get_current_user),
):
    """Return content pipeline metrics (admin-only data, public overview)."""
    curated_path = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "curated.json"
    rejected_path = BACKEND_ROOT / "app" / "content" / "questions" / "rejected" / "rejected.json"
    review_path = BACKEND_ROOT / "app" / "content" / "questions" / "review_duplicates" / "review_duplicates.json"
    los_path = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "learning_objects.json"

    def _count_safe(path):
        if not path.exists():
            return 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                return len(json.load(f))
        except Exception:
            return 0

    return {
        "pipeline": {
            "curated_candidates": _count_safe(curated_path),
            "fully_authored_learning_objects": _count_safe(los_path),
            "rejected": _count_safe(rejected_path),
            "semantic_duplicates_needing_review": _count_safe(review_path),
        },
        "sde_pack": {
            "total_target": TOTAL_SDE_QUESTIONS_TARGET,
            "current_learning_objects": _count_safe(los_path),
            "progress_percent": round(min(_count_safe(los_path) / TOTAL_SDE_QUESTIONS_TARGET * 100, 100), 1),
        },
    }


@router.get("/learning-paths")
async def get_learning_paths(
    user=Depends(get_current_user),
):
    """Get the complete structured learning paths for all 18 SDE skill areas."""
    if not LEARNING_PATHS_PATH.exists():
        raise HTTPException(500, "Curriculum not generated. Run generate_curriculum.py")

    with open(LEARNING_PATHS_PATH, "r", encoding="utf-8") as f:
        paths = json.load(f)

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    # Free users get only the path overview (count + difficulty distribution)
    # Pro users get full question IDs, patterns, and hints
    if not is_pro:
        for skill_id, info in paths["curriculum"].items():
            for stage_name in ("learn", "guided_practice", "placement_practice"):
                stage = info["learning_path"][stage_name]
                for item in stage:
                    item.pop("id", None)
                    item.pop("pattern", None)
                    item.pop("hint_count", None)
                    item.pop("test_case_count", None)

    return paths


@router.get("/learning-paths/{skill_id}")
async def get_learning_path(
    skill_id: str,
    user=Depends(get_current_user),
):
    """Get the learning path for a specific skill area."""
    if not LEARNING_PATHS_PATH.exists():
        raise HTTPException(500, "Curriculum not generated. Run generate_curriculum.py")

    with open(LEARNING_PATHS_PATH, "r", encoding="utf-8") as f:
        paths = json.load(f)

    curriculum = paths.get("curriculum", {})
    if skill_id not in curriculum:
        raise HTTPException(404, f"No learning path for skill: {skill_id}")

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    skill_info = curriculum[skill_id]
    if not is_pro:
        # Strip question-level details for free users
        for stage_name in ("learn", "guided_practice", "placement_practice"):
            stage = skill_info["learning_path"][stage_name]
            for item in stage:
                item.clear()
                item["count"] = 0
        # Actually just return counts
        skill_info_return = {
            "skill_id": skill_info["skill_id"],
            "name": skill_info["name"],
            "description": skill_info["description"],
            "question_target": skill_info["question_target"],
            "current_total": skill_info["current_total"],
            "coverage_percent": skill_info["coverage_percent"],
            "difficulty_distribution": skill_info["difficulty_distribution"],
            "learning_path": {
                "learn_count": len(skill_info["learning_path"]["learn"]),
                "guided_practice_count": len(skill_info["learning_path"]["guided_practice"]),
                "placement_practice_count": len(skill_info["learning_path"]["placement_practice"]),
            },
            "upgrade_message": "Pro Pass required to see specific questions, patterns, and hints.",
        }
        return skill_info_return

    skill_info["company_oa_patterns"] = COMPANY_BLUEPRINTS
    skill_info["total_questions"] = paths.get("total_questions")
    skill_info["sde_pack_target"] = TOTAL_SDE_QUESTIONS_TARGET
    return skill_info


@router.get("/mock-tests")
async def get_mock_tests(
    user=Depends(get_current_user),
):
    """List all company-specific mock tests with booking slots."""
    if not MOCK_TESTS_PATH.exists():
        raise HTTPException(500, "Mock tests not generated. Run finalize_curriculum.py")

    with open(MOCK_TESTS_PATH, "r", encoding="utf-8") as f:
        mocks = json.load(f)

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    # Free users: can only take 1 mock/month (limited to TCS pattern companies per free tier)
    free_companies = {"tcs", "infosys", "wipro"}

    result = []
    for comp_id, mock in mocks.items():
        config = mock["mock_config"]
        is_free_company = comp_id.lower() in free_companies
        can_access = is_pro or is_free_company

        result.append({
            "company_id": comp_id,
            "name": config["name"],
            "description": config["description"],
            "total_questions": mock["total_questions"],
            "time_limit_minutes": config["time_limit_minutes"],
            "patterns_covered": mock["patterns_covered"],
            "avg_quality": mock["avg_quality"],
            "can_access": can_access,
            "booking_slots": mock["booking_slots"],
            "upgrade_message": None if can_access else "Pro Pass required for mock tests from this company.",
        })

    return {"mock_tests": result}


@router.get("/mock-tests/{company_id}")
async def get_mock_test(
    company_id: str,
    user=Depends(get_current_user),
):
    """Get full mock test configuration with questions for a specific company."""
    if not MOCK_TESTS_PATH.exists():
        raise HTTPException(500, "Mock tests not generated. Run finalize_curriculum.py")

    with open(MOCK_TESTS_PATH, "r", encoding="utf-8") as f:
        mocks = json.load(f)

    mock = mocks.get(company_id.lower())
    if not mock:
        raise HTTPException(404, f"No mock test found for {company_id}")

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")
    free_companies = {"tcs", "infosys", "wipro"}

    if not is_pro and company_id.lower() not in free_companies:
        raise HTTPException(
            status_code=402,
            detail=(
                f"Mock tests for {company_id} require a Pro Pass. "
                "Free users can only take TCS/Infosys/Wipro mocks."
            ),
        )

    return mock


@router.get("/mock-tests/{company_id}/schedule")
async def schedule_mock_interview(
    company_id: str,
    date: Optional[str] = Query(None, description="Target date (YYYY-MM-DD)"),
    user=Depends(get_current_user),
):
    """Generate available booking slots for a mock interview."""
    if not MOCK_TESTS_PATH.exists():
        raise HTTPException(500, "Mock tests not generated. Run finalize_curriculum.py")

    with open(MOCK_TESTS_PATH, "r", encoding="utf-8") as f:
        mocks = json.load(f)

    mock = mocks.get(company_id.lower())
    if not mock:
        raise HTTPException(404, f"No mock test found for {company_id}")

    slots = mock.get("booking_slots", {})
    available_hours = slots.get("available_hours", [])
    duration = slots.get("duration_minutes", 60)

    result = []
    for hour in available_hours:
        h, m = hour.split(":")
        result.append({
            "company_id": company_id,
            "scheduled_at": date if date else "today",
            "time": hour,
            "duration_minutes": duration,
            "slot_id": f"mock_{company_id}_{hour.replace(':','')}",
        })

    return {
        "company_id": company_id,
        "available_slots": result,
        "duration_minutes": duration,
    }


@router.post("/mock-tests/{company_id}/book")
async def book_mock_interview(
    company_id: str,
    request: Request,
    user=Depends(get_current_user),
):
    """Book a mock interview slot (records the booking in user's profile)."""
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    slot_id = body.get("slot_id", "")
    scheduled_at = body.get("scheduled_at", "")

    if not slot_id or not scheduled_at:
        raise HTTPException(400, detail="slot_id and scheduled_at required")

    from datetime import datetime

    booking = {
        "user_id": user["id"],
        "company_id": company_id.lower(),
        "slot_id": slot_id,
        "scheduled_at": scheduled_at,
        "status": "scheduled",
        "created_at": datetime.now(timezone.utc),
        "mock_type": "company_mock",
    }

    result = await interview_bookings_collection.insert_one(booking)
    booking["_id"] = str(result.inserted_id)

    return {
        "status": "scheduled",
        "booking_id": booking["_id"],
        "company": company_id,
        "scheduled_at": scheduled_at,
        "slot_id": slot_id,
        "confirmation": f"Mock interview booked for {company_id} on {scheduled_at}",
    }


# =============================================================
# MULTI-ROLE CURRICULUM ENDPOINTS
# =============================================================

@router.get("/roles")
async def get_all_roles(user=Depends(get_current_user)):
    """List all placement roles with metadata."""
    roles = []
    for role_id in ROLE_DISPLAY_ORDER:
        role = ROLE_CURRICULA.get(role_id, {})
        roles.append({
            "role_id": role_id,
            "display_name": role.get("display_name", ""),
            "icon": role.get("icon", ""),
            "description": role.get("description", ""),
            "target_companies": role.get("target_companies", []),
            "skill_areas": len(role.get("skill_tree", {})),
            "difficulty_distribution": {},  # filled if curriculum exists
        })

    # Fill in progress data from generated curriculum
    if ALL_ROLES_PATH.exists():
        with open(ALL_ROLES_PATH, "r", encoding="utf-8") as f:
            all_roles_data = json.load(f)
        for role in roles:
            role_data = all_roles_data.get("roles", {}).get(role["role_id"], {})
            role["total_questions"] = role_data.get("total_questions", 0)
            role["matched_questions"] = role_data.get("matched_questions", 0)
            role["generated_stubs"] = role_data.get("generated_stubs", 0)
            role["coverage_percent"] = role_data.get("coverage_percent", 0.0)
            role["difficulty_distribution"] = role_data.get("difficulty_distribution", {})

    return {"roles": roles, "display_order": ROLE_DISPLAY_ORDER}


@router.get("/roles/{role_id}")
async def get_role_curriculum(
    role_id: str,
    detail: bool = Query(False, description="Include full question details (Pro only)"),
    user=Depends(get_current_user),
):
    """Get the full independent curriculum for a specific role."""
    role = ROLE_CURRICULA.get(role_id.lower())
    if not role:
        raise HTTPException(404, f"Unknown role: {role_id}")

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    # Load the generated curriculum if available
    role_data = None
    if ALL_ROLES_PATH.exists():
        with open(ALL_ROLES_PATH, "r", encoding="utf-8") as f:
            all_roles = json.load(f)
        role_data = all_roles.get("roles", {}).get(role_id.lower())

    # Free users see overview only; Pro sees full learning paths + mock config
    result = {
        "role_id": role_id,
        "display_name": role["display_name"],
        "icon": role["icon"],
        "description": role["description"],
        "target_companies": role["target_companies"],
        "skill_tree": {
            sid: {"name": s["name"], "target": s["target"]}
            for sid, s in role["skill_tree"].items()
        },
        "total_target": sum(s["target"] for s in role["skill_tree"].values()),
        "mock_test": {
            "name": role["mock_test"]["name"],
            "total_questions": role["mock_test"]["total_questions"],
            "time_limit_minutes": role["mock_test"]["time_limit_minutes"],
            "section_count": len(role["mock_test"]["sections"]),
        },
        "progress": {},
    }

    if role_data:
        result["progress"] = {
            "total_questions": role_data.get("total_questions", 0),
            "matched_questions": role_data.get("matched_questions", 0),
            "generated_stubs": role_data.get("generated_stubs", 0),
            "coverage_percent": role_data.get("coverage_percent", 0.0),
            "difficulty_distribution": role_data.get("difficulty_distribution", {}),
        }

    if is_pro and detail:
        result["learning_paths"] = role_data.get("learning_paths", {}) if role_data else {}
        result["mock_test_full"] = role["mock_test"]
        result["difficulty_distribution"] = role_data.get("difficulty_distribution", {}) if role_data else {}
    elif not is_pro:
        result["upgrade_message"] = (
            "Pro Pass required to view full learning paths, question details, "
            "and company-specific mock tests for this role."
        )

    return result


@router.get("/roles/{role_id}/mock-test")
async def get_role_mock_test(
    role_id: str,
    user=Depends(get_current_user),
):
    """Get the mock test configuration for a specific role."""
    role = ROLE_CURRICULA.get(role_id.lower())
    if not role:
        raise HTTPException(404, f"Unknown role: {role_id}")

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    mock = role["mock_test"]
    result = {
        "role_id": role_id,
        "mock_test": {
            "name": mock["name"],
            "description": mock.get("description", ""),
            "total_questions": mock["total_questions"],
            "time_limit_minutes": mock["time_limit_minutes"],
            "sections": mock["sections"],
        },
        "company_patterns": {},
    }

    # Add company-specific patterns
    for comp in role["target_companies"]:
        comp_lower = comp.lower()
        if comp_lower in COMPANY_BLUEPRINTS:
            result["company_patterns"][comp_lower] = {
                "display_name": COMPANY_BLUEPRINTS[comp_lower]["display_name"],
                "focus_areas": COMPANY_BLUEPRINTS[comp_lower].get("focus_areas", []),
                "process": COMPANY_BLUEPRINTS[comp_lower].get("process", []),
            }

    if not is_pro:
        result["upgrade_message"] = "Pro Pass required to access full mock test details and question sets."

    return result


@router.get("/roles/{role_id}/skill/{skill_id}")
async def get_role_skill_path(
    role_id: str,
    skill_id: str,
    user=Depends(get_current_user),
):
    """Get the learning path for a specific skill within a role."""
    role = ROLE_CURRICULA.get(role_id.lower())
    if not role:
        raise HTTPException(404, f"Unknown role: {role_id}")

    skill = role["skill_tree"].get(skill_id)
    if not skill:
        raise HTTPException(404, f"Unknown skill: {skill_id} for role {role_id}")

    plan = user.get("plan", "free")
    is_pro = plan in ("pro", "lifetime")

    # Load learning objects for this skill
    all_los = []
    if ALL_ROLES_PATH.exists():
        with open(ALL_ROLES_PATH, "r", encoding="utf-8") as f:
            all_roles = json.load(f)
        role_data = all_roles.get("roles", {}).get(role_id.lower(), {})
        for stage_name in ("learn", "guided_practice", "interview"):
            stage = role_data.get("learning_paths", {}).get(stage_name, [])
            for item in stage:
                if item.get("pattern") == skill_id or skill_id in item.get("pattern", ""):
                    all_los.append({**item, "stage": stage_name})

    result = {
        "role_id": role_id,
        "skill_id": skill_id,
        "skill_name": skill["name"],
        "target": skill["target"],
        "weight": skill.get("weight", 1.0),
        "questions_found": len(all_los),
    }

    if is_pro:
        result["learning_path"] = {
            "learn": [item for item in all_los if item["stage"] == "learn"],
            "guided_practice": [item for item in all_los if item["stage"] == "guided_practice"],
            "interview": [item for item in all_los if item["stage"] == "interview"],
        }
    else:
        result["staging"] = {
            "learn_count": sum(1 for item in all_los if item["stage"] == "learn"),
            "guided_practice_count": sum(1 for item in all_los if item["stage"] == "guided_practice"),
            "interview_count": sum(1 for item in all_los if item["stage"] == "interview"),
        }
        result["upgrade_message"] = "Pro Pass required to see specific questions and hints for this skill path."

    return result
