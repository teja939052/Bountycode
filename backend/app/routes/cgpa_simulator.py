"""CGPA Simulator — deterministic semester / cumulative GPA planning tool.

Pure math, no AI:
  - calculate: semester-wise subjects (credits + grade points) -> per-semester
    GPA, weighted cumulative CGPA and a placement classification.
  - target: what-if planning — given current CGPA, credits completed and a
    target CGPA, compute the GPA required in the remaining credits plus a
    grade-breakdown table (which grade you need for each of the remaining
    semesters to hit the target).
"""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.middleware.auth import get_current_user
from app.database import cgpa_calculations_collection

router = APIRouter(prefix="/api/v1/cgpa", tags=["CGPA Simulator"])

GRADE_SCALE = [
    {"grade": "S", "points": 10},
    {"grade": "A", "points": 9},
    {"grade": "B", "points": 8},
    {"grade": "C", "points": 7},
    {"grade": "D", "points": 6},
    {"grade": "E", "points": 5},
    {"grade": "F", "points": 0},
]


class Subject(BaseModel):
    name: str = ""
    credits: int = Field(3, ge=1, le=10)
    grade_point: float = Field(0, ge=0, le=10)


class SemesterCalc(BaseModel):
    name: str = "Semester 1"
    subjects: List[Subject]


class CalculateRequest(BaseModel):
    semesters: List[SemesterCalc]
    max_scale: float = Field(10, ge=1, le=10)


class TargetRequest(BaseModel):
    current_cgpa: float = Field(..., ge=0, le=10)
    credits_completed: int = Field(0, ge=0)
    target_cgpa: float = Field(..., ge=0, le=10)
    credits_remaining: int = Field(1, ge=1)
    max_scale: float = Field(10, ge=1, le=10)


class SaveRequest(BaseModel):
    title: str = ""
    kind: str = "calculate"
    result: dict


def _classify(cgpa: float) -> str:
    if cgpa >= 9:
        return "Outstanding"
    if cgpa >= 8:
        return "Excellent"
    if cgpa >= 7:
        return "First Class with Distinction"
    if cgpa >= 6:
        return "First Class"
    if cgpa >= 5:
        return "Second Class"
    return "Below Second Class"


def _round(v, nd=2):
    return round(v, nd)


# ─── Routes ───────────────────────────────────────────────────────────────

@router.get("/grade-scale")
async def grade_scale(user=Depends(get_current_user)):
    return {"scale": GRADE_SCALE}


@router.post("/calculate")
async def calculate_cgpa(req: CalculateRequest, user=Depends(get_current_user)):
    if not req.semesters:
        raise HTTPException(status_code=400, detail="At least one semester is required")

    semester_results = []
    total_credits = 0
    total_points = 0.0

    for sem in req.semesters:
        if not sem.subjects:
            continue
        credits = sum(s.credits for s in sem.subjects)
        points = sum(s.credits * s.grade_point for s in sem.subjects)
        if credits <= 0:
            continue
        gpa = points / credits
        total_credits += credits
        total_points += points
        semester_results.append({
            "name": sem.name,
            "credits": credits,
            "grade_points": _round(points),
            "gpa": _round(gpa),
        })

    if total_credits <= 0:
        raise HTTPException(status_code=400, detail="No valid subjects provided")

    cumulative = total_points / total_credits
    cumulative = min(cumulative, req.max_scale)

    result = {
        "kind": "calculate",
        "max_scale": req.max_scale,
        "semesters": semester_results,
        "total_credits": total_credits,
        "total_grade_points": _round(total_points),
        "cumulative_cgpa": _round(cumulative),
        "classification": _classify(cumulative),
        "calculated_at": datetime.now(timezone.utc),
    }
    return result


@router.post("/target")
async def target_cgpa(req: TargetRequest, user=Depends(get_current_user)):
    if req.current_cgpa > req.max_scale:
        raise HTTPException(status_code=400, detail="Current CGPA exceeds max scale")
    if req.target_cgpa > req.max_scale:
        raise HTTPException(status_code=400, detail="Target CGPA exceeds max scale")

    total_credits = req.credits_completed + req.credits_remaining
    target_points = req.target_cgpa * total_credits
    current_points = req.current_cgpa * req.credits_completed
    required_points = target_points - current_points
    required_gpa = required_points / req.credits_remaining if req.credits_remaining > 0 else 0.0

    feasible = required_gpa <= req.max_scale + 1e-9
    shortfall = max(0.0, required_gpa - req.max_scale) if not feasible else 0.0

    # What-if table: if every remaining credit gets this grade, final CGPA = ...
    breakdown = []
    for g in GRADE_SCALE:
        final_cgpa = (current_points + g["points"] * req.credits_remaining) / total_credits
        breakdown.append({
            "grade": g["grade"],
            "points": g["points"],
            "final_cgpa": _round(min(final_cgpa, req.max_scale)),
            "hits_target": final_cgpa + 1e-9 >= req.target_cgpa,
        })

    result = {
        "kind": "target",
        "max_scale": req.max_scale,
        "current_cgpa": req.current_cgpa,
        "credits_completed": req.credits_completed,
        "target_cgpa": req.target_cgpa,
        "credits_remaining": req.credits_remaining,
        "required_gpa": _round(required_gpa),
        "feasible": bool(feasible),
        "shortfall": _round(shortfall),
        "breakdown": breakdown,
        "calculated_at": datetime.now(timezone.utc),
    }
    return result


@router.post("/save")
async def save_calculation(req: SaveRequest, user=Depends(get_current_user)):
    doc = {
        "user_id": user["id"],
        "title": (req.title or "").strip()[:100] or "Untitled",
        "kind": req.kind,
        "result": req.result,
        "created_at": datetime.now(timezone.utc),
    }
    result = await cgpa_calculations_collection().insert_one(doc)
    return {"id": str(result.inserted_id), "saved": True}


@router.get("/history")
async def calculation_history(limit: int = 20, user=Depends(get_current_user)):
    cursor = cgpa_calculations_collection().find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(max(1, min(limit, 100)))
    items = []
    async for doc in cursor:
        items.append({
            "id": str(doc["_id"]),
            "title": doc.get("title", "Untitled"),
            "kind": doc.get("kind", "calculate"),
            "result": doc.get("result"),
            "created_at": doc.get("created_at"),
        })
    return {"history": items}
