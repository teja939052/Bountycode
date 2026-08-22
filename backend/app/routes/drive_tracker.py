"""Drive Outcome Tracker — track campus placement drive progress and outcomes.

Deterministic lifecycle tracking (no AI):
  - stages: applied -> shortlisted -> online_assessment -> technical_interview ->
    hr_interview -> offer -> joined  (plus rejected as a terminal state)
  - per-drive notes, dates and a status flag
  - aggregate stats: counts per stage, offer/selection rates and a funnel view
"""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import drive_trackers_collection

router = APIRouter(prefix="/api/v1/drives/tracker", tags=["Drive Tracker"])

STAGES = [
    "applied",
    "shortlisted",
    "online_assessment",
    "technical_interview",
    "hr_interview",
    "offer",
    "joined",
]
TERMINAL = {"offer", "joined", "rejected"}
STAGE_ORDER = {s: i for i, s in enumerate(STAGES)}


class DriveCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=120)
    role: str = Field("", max_length=120)
    location: str = Field("", max_length=120)
    package_lpa: Optional[float] = Field(None, ge=0, le=200)
    stage: str = Field("applied", max_length=40)
    notes: str = Field("", max_length=2000)


class DriveUpdate(BaseModel):
    company: Optional[str] = Field(None, min_length=1, max_length=120)
    role: Optional[str] = Field(None, max_length=120)
    location: Optional[str] = Field(None, max_length=120)
    package_lpa: Optional[float] = Field(None, ge=0, le=200)
    stage: Optional[str] = Field(None, max_length=40)
    status: Optional[str] = Field(None, pattern="^(active|rejected)$")
    notes: Optional[str] = Field(None, max_length=2000)


def _validate_stage(stage: str):
    if stage not in STAGES and stage != "rejected":
        raise HTTPException(status_code=400, detail=f"Unknown stage: {stage}")


def _serialize(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "company": doc.get("company", ""),
        "role": doc.get("role", ""),
        "location": doc.get("location", ""),
        "package_lpa": doc.get("package_lpa"),
        "stage": doc.get("stage", "applied"),
        "status": doc.get("status", "active"),
        "notes": doc.get("notes", ""),
        "applied_date": doc.get("applied_date"),
        "updated_at": doc.get("updated_at"),
    }


# ─── Routes ───────────────────────────────────────────────────────────────

@router.get("/stages")
async def stages(user=Depends(get_current_user)):
    return {"stages": STAGES, "order": {s: i for i, s in enumerate(STAGES)}}


@router.get("")
async def list_drives(user=Depends(get_current_user)):
    cursor = drive_trackers_collection().find({"user_id": user["id"]}).sort("applied_date", -1).limit(200)
    drives = [_serialize(doc) async for doc in cursor]
    return {"drives": drives}


@router.post("")
async def create_drive(req: DriveCreate, user=Depends(get_current_user)):
    _validate_stage(req.stage)
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user["id"],
        "company": req.company.strip(),
        "role": req.role.strip(),
        "location": req.location.strip(),
        "package_lpa": req.package_lpa,
        "stage": req.stage,
        "status": "rejected" if req.stage == "rejected" else "active",
        "notes": req.notes.strip(),
        "applied_date": now,
        "updated_at": now,
    }
    result = await drive_trackers_collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize(doc)


@router.put("/{drive_id}")
async def update_drive(drive_id: str, req: DriveUpdate, user=Depends(get_current_user)):
    try:
        oid = ObjectId(drive_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid drive ID")

    existing = await drive_trackers_collection().find_one({"_id": oid, "user_id": user["id"]})
    if not existing:
        raise HTTPException(status_code=404, detail="Drive not found")

    update = {}
    if req.company is not None:
        update["company"] = req.company.strip()
    if req.role is not None:
        update["role"] = req.role.strip()
    if req.location is not None:
        update["location"] = req.location.strip()
    if req.package_lpa is not None:
        update["package_lpa"] = req.package_lpa
    if req.stage is not None:
        _validate_stage(req.stage)
        update["stage"] = req.stage
        if req.stage == "rejected":
            update["status"] = "rejected"
    if req.status is not None:
        update["status"] = req.status
    if req.notes is not None:
        update["notes"] = req.notes.strip()

    if not update:
        return _serialize(existing)

    update["updated_at"] = datetime.now(timezone.utc)
    await drive_trackers_collection().update_one({"_id": oid}, {"$set": update})
    updated = await drive_trackers_collection().find_one({"_id": oid})
    return _serialize(updated)


@router.delete("/{drive_id}")
async def delete_drive(drive_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(drive_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid drive ID")
    result = await drive_trackers_collection().delete_one({"_id": oid, "user_id": user["id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Drive not found")
    return {"deleted": True}


@router.get("/stats")
async def drive_stats(user=Depends(get_current_user)):
    cursor = drive_trackers_collection().find({"user_id": user["id"]})
    drives = [doc async for doc in cursor]

    total = len(drives)
    by_stage = {s: 0 for s in STAGES}
    by_stage["rejected"] = 0
    active = 0
    offers = 0
    joined = 0
    rejected = 0

    for d in drives:
        stage = d.get("stage", "applied")
        if d.get("status") == "rejected" or stage == "rejected":
            rejected += 1
            by_stage["rejected"] += 1
            continue
        by_stage[stage] = by_stage.get(stage, 0) + 1
        if stage == "offer":
            offers += 1
        if stage == "joined":
            joined += 1
            offers += 1
        if stage not in TERMINAL:
            active += 1

    # Funnel: cumulative retention through each stage
    funnel = []
    for i, s in enumerate(STAGES):
        cum = 0
        for d in drives:
            stage = d.get("stage", "applied")
            if d.get("status") == "rejected" or stage == "rejected":
                continue
            if STAGE_ORDER.get(stage, -1) >= i:
                cum += 1
        funnel.append({"stage": s, "count": cum, "rate": round(cum / max(1, total) * 100, 1)})

    return {
        "total": total,
        "active": active,
        "offers": offers,
        "joined": joined,
        "rejected": rejected,
        "offer_rate": round(offers / max(1, total) * 100, 1),
        "selection_rate": round((offers + active) / max(1, total) * 100, 1),
        "by_stage": by_stage,
        "funnel": funnel,
    }
