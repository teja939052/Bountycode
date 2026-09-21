"""Learning path routes — role-based curriculum (SDE, Data Analyst, QA, DevOps)."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from app.middleware.auth import get_current_user
from app.services.learning_paths import (
    get_all_roles,
    get_role_path,
    enroll_in_path,
    complete_path_module,
    get_user_path_progress,
    get_all_user_paths,
    get_recommended_paths,
)
from app.models.learning_path import LearningPathEnroll

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/learning-paths", tags=["learning-paths"])


@router.get("/roles")
async def list_roles(user=Depends(get_current_user)):
    """List all available role-based learning paths."""
    paths = get_all_roles()
    enrolled = await get_all_user_paths(user["id"])
    enrolled_map = {p["id"]: p for p in enrolled}
    result = []
    for p in paths:
        ep = enrolled_map.get(p["id"])
        result.append({
            **p,
            "enrolled": ep is not None,
            "progress_pct": ep.get("progress_pct", 0) if ep else 0,
            "completed": ep.get("completed", False) if ep else False,
        })
    return {"paths": result}


@router.get("/roles/{role_id}")
async def get_role(role_id: str, user=Depends(get_current_user)):
    """Get a single role-based learning path with module details."""
    role = get_role_path(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role path not found")

    progress = await get_user_path_progress(user["id"], role_id)
    modules_with_status = []
    for m in role["modules"]:
        mod_progress = progress.get("modules", {}).get(m["id"], {})
        modules_with_status.append({
            **m,
            "completed": mod_progress.get("completed", False),
            "locked": mod_progress.get("locked", not _is_unlocked(m, role["modules"], progress)),
            "score": mod_progress.get("score"),
            "xp_earned": mod_progress.get("xp_earned", 0),
            "attempts": mod_progress.get("attempts", 0),
        })

    return {
        "id": role["id"],
        "name": role["name"],
        "short_name": role["short_name"],
        "icon": role["icon"],
        "color": role["color"],
        "description": role["description"],
        "target_roles": role["target_roles"],
        "avg_package": role["avg_package"],
        "duration_weeks": role["duration_weeks"],
        "difficulty": role["difficulty"],
        "prerequisites": role["prerequisites"],
        "modules": modules_with_status,
        "final_project": role.get("final_project"),
        "certification": role.get("certification"),
        "enrolled": progress.get("enrolled", False),
        "completed": progress.get("completed", False),
        "total_xp_earned": progress.get("total_xp_earned", 0),
        "current_module_id": progress.get("current_module_id"),
    }


def _is_unlocked(module: Dict[str, Any], all_modules: List[Dict[str, Any]], progress: Dict[str, Any]) -> bool:
    """Check if a module should be unlocked based on dependencies."""
    depends_on = module.get("depends_on", [])
    if not depends_on:
        return True
    modules_progress = progress.get("modules", {})
    return all(modules_progress.get(dep, {}).get("completed", False) for dep in depends_on)


@router.post("/roles/enroll")
async def enroll_role(body: LearningPathEnroll, user=Depends(get_current_user)):
    """Enroll in a role-based learning path."""
    try:
        result = await enroll_in_path(user["id"], body.path_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Enrollment failed: {e}")
        raise HTTPException(status_code=500, detail="Enrollment failed")


@router.post("/roles/{role_id}/modules/{module_id}/complete")
async def complete_module(
    role_id: str,
    module_id: str,
    score: Optional[float] = Query(None, ge=0, le=100),
    user=Depends(get_current_user),
):
    """Mark a module as completed and unlock the next one."""
    try:
        result = await complete_path_module(user["id"], role_id, module_id, score)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Module completion failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete module")


@router.get("/my-paths")
async def my_paths(user=Depends(get_current_user)):
    """Get all enrolled learning paths with progress."""
    paths = await get_all_user_paths(user["id"])
    return {"paths": paths}


@router.get("/recommendations")
async def recommendations(user=Depends(get_current_user)):
    """Get personalized learning path recommendations."""
    recs = await get_recommended_paths(user["id"])
    return {"recommendations": recs}
