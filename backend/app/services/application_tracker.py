from datetime import datetime, timezone
from typing import Dict, Any, List
from app.database import get_collection
from bson import ObjectId


def _app_col():
    return get_collection("applications")


PIPELINE_STAGES = {
    "interested": {"name": "Interested", "color": "gray", "order": 0},
    "applied": {"name": "Applied", "color": "blue", "order": 1},
    "oa_received": {"name": "OA Received", "color": "yellow", "order": 2},
    "interview_scheduled": {"name": "Interview Scheduled", "color": "purple", "order": 3},
    "interview_completed": {"name": "Interview Completed", "color": "indigo", "order": 4},
    "offer_received": {"name": "Offer Received", "color": "green", "order": 5},
    "accepted": {"name": "Accepted", "color": "emerald", "order": 6},
    "rejected": {"name": "Rejected", "color": "red", "order": 7},
    "withdrawn": {"name": "Withdrawn", "color": "gray", "order": 8},
}


async def create_application(user_id: str, company: str, role: str, job_url: str = "", notes: str = "") -> dict:
    col = _app_col()
    app = {
        "user_id": user_id,
        "company": company,
        "role": role,
        "job_url": job_url,
        "notes": notes,
        "stage": "interested",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await col.insert_one(app)
    return {"application_id": str(result.inserted_id), "company": company, "role": role, "stage": "interested"}


async def get_application_pipeline(user_id: str) -> list:
    col = _app_col()
    cursor = col.find({"user_id": user_id}).sort("updated_at", -1)
    apps = []
    async for doc in cursor:
        stage = doc.get("stage", "interested")
        stage_info = PIPELINE_STAGES.get(stage, PIPELINE_STAGES["interested"])
        apps.append({
            "id": str(doc["_id"]),
            "company": doc.get("company", ""),
            "role": doc.get("role", ""),
            "job_url": doc.get("job_url", ""),
            "notes": doc.get("notes", ""),
            "stage": stage,
            "stage_name": stage_info["name"],
            "stage_color": stage_info["color"],
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
        })
    return apps


async def update_application_stage(user_id: str, application_id: str, new_stage: str) -> dict:
    col = _app_col()
    if new_stage not in PIPELINE_STAGES:
        return {"success": False, "message": f"Invalid stage: {new_stage}"}
    try:
        result = await col.update_one(
            {"_id": ObjectId(application_id), "user_id": user_id},
            {"$set": {"stage": new_stage, "updated_at": datetime.now(timezone.utc)}},
        )
        if result.modified_count:
            return {"success": True, "message": f"Moved to {PIPELINE_STAGES[new_stage]['name']}"}
        return {"success": False, "message": "Application not found"}
    except Exception:
        return {"success": False, "message": "Invalid application ID"}


async def get_application_stats(user_id: str) -> dict:
    col = _app_col()
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": "$stage", "count": {"$sum": 1}}},
    ]
    stage_counts = {}
    async for doc in col.aggregate(pipeline):
        stage_counts[doc["_id"]] = doc["count"]
    total = sum(stage_counts.values())
    return {
        "total_applications": total,
        "by_stage": {stage: {"count": stage_counts.get(stage, 0), "name": info["name"], "color": info["color"]}
                     for stage, info in PIPELINE_STAGES.items()},
    }


async def delete_application(user_id: str, application_id: str) -> dict:
    col = _app_col()
    try:
        result = await col.delete_one({"_id": ObjectId(application_id), "user_id": user_id})
        if result.deleted_count:
            return {"success": True, "message": "Application deleted"}
        return {"success": False, "message": "Application not found"}
    except Exception:
        return {"success": False, "message": "Invalid application ID"}
