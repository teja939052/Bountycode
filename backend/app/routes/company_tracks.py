"""Company track routes — TCS, Accenture, Infosys, Wipro specific preparation."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from app.middleware.auth import get_current_user
from app.services.learning_paths import (
    get_all_company_tracks,
    get_company_track,
    enroll_in_track,
    complete_track_module,
    get_user_track_progress,
    get_all_user_tracks,
)
from app.models.learning_path import LearningPathEnroll

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/company-tracks", tags=["company-tracks"])


@router.get("/companies")
async def list_companies(user=Depends(get_current_user)):
    """List all available company-specific tracks."""
    tracks = get_all_company_tracks()
    enrolled = await get_all_user_tracks(user["id"])
    enrolled_map = {t["id"]: t for t in enrolled}
    result = []
    for t in tracks:
        et = enrolled_map.get(t["id"])
        result.append({
            **t,
            "enrolled": et is not None,
            "progress_pct": et.get("progress_pct", 0) if et else 0,
            "completed": et.get("completed", False) if et else False,
        })
    return {"tracks": result}


@router.get("/companies/{track_id}")
async def get_track(track_id: str, user=Depends(get_current_user)):
    """Get a single company track with section/module details."""
    track = get_company_track(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Company track not found")

    progress = await get_user_track_progress(user["id"], track_id)

    sections_with_status = []
    for section in track.get("sections", []):
        modules_with_status = []
        for m in section.get("modules", []):
            section_data = progress.get("sections", {}).get(section["id"], {})
            mod_progress = section_data.get("modules", {}).get(m["id"], {})
            modules_with_status.append({
                **m,
                "completed": mod_progress.get("completed", False),
                "locked": mod_progress.get("locked", False),
                "score": mod_progress.get("score"),
                "xp_earned": mod_progress.get("xp_earned", 0),
            })
        sections_with_status.append({
            **section,
            "modules": modules_with_status,
            "completed": all(m["completed"] for m in modules_with_status) if modules_with_status else False,
        })

    return {
        "id": track["id"],
        "company_id": track["company_id"],
        "name": track["name"],
        "full_name": track["full_name"],
        "icon": track["icon"],
        "color": track["color"],
        "role": track["role"],
        "package_range": track["package_range"],
        "duration_minutes": track["duration_minutes"],
        "difficulty": track["difficulty"],
        "description": track["description"],
        "sections": sections_with_status,
        "coding_patterns": track.get("coding_patterns", []),
        "hr_questions": track.get("hr_questions", []),
        "tips": track.get("tips", []),
        "success_rate": track.get("success_rate"),
        "enrolled": progress.get("enrolled", False),
        "completed": progress.get("completed", False),
        "total_xp_earned": progress.get("total_xp_earned", 0),
        "current_section_id": progress.get("current_section_id"),
    }


@router.post("/companies/enroll")
async def enroll_company(body: LearningPathEnroll, user=Depends(get_current_user)):
    """Enroll in a company-specific track."""
    try:
        result = await enroll_in_track(user["id"], body.path_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Track enrollment failed: {e}")
        raise HTTPException(status_code=500, detail="Enrollment failed")


@router.post("/companies/{track_id}/modules/{module_id}/complete")
async def complete_track_module_endpoint(
    track_id: str,
    module_id: str,
    score: Optional[float] = Query(None, ge=0, le=100),
    user=Depends(get_current_user),
):
    """Mark a track module as completed."""
    try:
        result = await complete_track_module(user["id"], track_id, module_id, score)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Track module completion failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete module")


@router.get("/my-tracks")
async def my_tracks(user=Depends(get_current_user)):
    """Get all enrolled company tracks with progress."""
    tracks = await get_all_user_tracks(user["id"])
    return {"tracks": tracks}
