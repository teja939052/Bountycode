from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.database import get_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/api/enterprise", tags=["enterprise"])


class CreateCohortRequest(BaseModel):
    name: str
    institution: str
    student_ids: Optional[List[str]] = []


@router.post("/cohorts")
async def create_cohort(req: CreateCohortRequest, user=Depends(get_current_user)):
    col = get_collection("cohorts")
    cohort = {
        "name": req.name,
        "institution": req.institution,
        "admin_id": user["id"],
        "student_ids": req.student_ids or [],
        "created_at": datetime.now(timezone.utc),
    }
    result = await col.insert_one(cohort)
    return {"cohort_id": str(result.inserted_id), "name": req.name, "institution": req.institution}


@router.get("/cohorts")
async def list_cohorts(user=Depends(get_current_user)):
    col = get_collection("cohorts")
    cursor = col.find({"admin_id": user["id"]}).sort("created_at", -1)
    cohorts = []
    async for doc in cursor:
        cohorts.append({
            "cohort_id": str(doc["_id"]),
            "name": doc.get("name", ""),
            "institution": doc.get("institution", ""),
            "student_count": len(doc.get("student_ids", [])),
            "created_at": doc.get("created_at"),
        })
    return {"cohorts": cohorts}


@router.get("/cohorts/{cohort_id}/progress")
async def get_cohort_progress(cohort_id: str, user=Depends(get_current_user)):
    col = get_collection("cohorts")
    try:
        from bson import ObjectId
        cohort = await col.find_one({"_id": ObjectId(cohort_id), "admin_id": user["id"]})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid cohort ID")

    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")

    student_ids = cohort.get("student_ids", [])
    skill_col = get_collection("skill_graphs")
    gam_col = get_collection("gamification")

    students = []
    for sid in student_ids[:50]:
        skill = await skill_col.find_one({"user_id": sid})
        gam = await gam_col.find_one({"user_id": sid})
        students.append({
            "user_id": sid,
            "overall_score": (skill or {}).get("overall_score", 0),
            "xp": (gam or {}).get("xp", 0),
            "level": (gam or {}).get("level", 1),
            "streak": (gam or {}).get("streak", 0),
        })

    return {
        "cohort_id": cohort_id,
        "name": cohort.get("name", ""),
        "students": students,
        "count": len(students),
    }
