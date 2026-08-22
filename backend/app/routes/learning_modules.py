"""Learning Modules routes — Duolingo-style step-by-step coding lessons."""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId

from app.middleware.auth import get_current_user
from app.database import (
    learning_modules_collection,
    user_learning_progress_collection,
    users_collection,
)

router = APIRouter(prefix="/api/v1/learning-modules", tags=["Learning Modules"])


def _serialize_module(module: dict) -> dict:
    return {
        "id": str(module["_id"]),
        "question_id": module.get("question_id"),
        "title": module.get("title", ""),
        "description": module.get("description", ""),
        "difficulty": module.get("difficulty", "beginner"),
        "estimated_time_minutes": module.get("estimated_time_minutes", 0),
        "steps": module.get("steps", []),
        "xp_reward": module.get("xp_reward", 0),
        "badge_reward": module.get("badge_reward"),
        "company_tags": module.get("company_tags", []),
        "topic": module.get("topic", ""),
        "created_at": module.get("created_at"),
    }


def _calculate_progress(module: dict, progress: Optional[dict]) -> float:
    total_steps = len(module.get("steps", []))
    if total_steps == 0:
        return 0.0
    if progress and progress.get("completed_steps"):
        return round((len(progress["completed_steps"]) / total_steps) * 100, 1)
    return 0.0


async def _get_module_progress(user_id: str, module_id: str) -> Optional[dict]:
    return await user_learning_progress_collection().find_one({
        "user_id": user_id,
        "module_id": module_id,
    })


def _get_recommendation_reason(module: dict, target_company: Optional[str], progress: float) -> str:
    if progress > 0 and progress < 100:
        return "Continue your progress"
    if target_company and target_company.lower() in [c.lower() for c in module.get("company_tags", [])]:
        return f"Relevant for {target_company}"
    if module.get("difficulty") == "beginner":
        return "Great for building foundational skills"
    if module.get("difficulty") == "intermediate":
        return "Builds on core concepts"
    return "Expand your skills"


@router.get("")
async def list_modules(
    difficulty: Optional[str] = Query(default=None),
    topic: Optional[str] = Query(default=None),
    company: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=12, ge=1, le=50),
    user=Depends(get_current_user),
):
    user_id = user["id"]
    query = {}

    if difficulty:
        query["difficulty"] = difficulty.lower()
    if topic:
        query["topic"] = {"$regex": topic, "$options": "i"}
    if company:
        query["company_tags"] = {"$regex": company, "$options": "i"}

    skip = (page - 1) * limit

    modules = await learning_modules_collection().find(query).skip(skip).limit(limit).to_list(length=limit)
    total = await learning_modules_collection().count_documents(query)

    modules_with_progress = []
    for module in modules:
        progress = await _get_module_progress(user_id, str(module["_id"]))
        pct = _calculate_progress(module, progress)
        modules_with_progress.append({
            **_serialize_module(module),
            "user_progress": pct,
            "is_started": progress is not None,
        })

    return {"success": True, "modules": modules_with_progress, "total": total, "page": page}


@router.get("/{module_id}")
async def get_module(module_id: str, user=Depends(get_current_user)):
    try:
        module = await learning_modules_collection().find_one({"_id": ObjectId(module_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid module ID")

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    user_id = user["id"]
    progress = await _get_module_progress(user_id, module_id)

    await user_learning_progress_collection().update_one(
        {"user_id": user_id, "module_id": module_id},
        {
            "$setOnInsert": {
                "user_id": user_id,
                "module_id": module_id,
                "started_at": datetime.now(timezone.utc),
            },
            "$set": {
                "last_accessed_at": datetime.now(timezone.utc),
                "current_step": progress.get("current_step", 1) if progress else 1,
            },
        },
        upsert=True,
    )

    if progress:
        return {
            "success": True,
            "module": _serialize_module(module),
            "progress": {
                "completed_steps": progress.get("completed_steps", []),
                "current_step": progress.get("current_step", 1),
                "xp_earned": progress.get("xp_earned", 0),
                "badge_unlocked": progress.get("badge_unlocked"),
                "started_at": progress.get("started_at"),
                "progress_pct": _calculate_progress(module, progress),
            },
        }

    return {
        "success": True,
        "module": _serialize_module(module),
        "progress": None,
    }


@router.post("/{module_id}/start")
async def start_module(module_id: str, user=Depends(get_current_user)):
    try:
        module = await learning_modules_collection().find_one({"_id": ObjectId(module_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid module ID")

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    user_id = user["id"]
    now = datetime.now(timezone.utc)

    await user_learning_progress_collection().update_one(
        {"user_id": user_id, "module_id": module_id},
        {
            "$setOnInsert": {
                "user_id": user_id,
                "module_id": module_id,
                "started_at": now,
                "completed_steps": [],
                "current_step": 1,
                "xp_earned": 0,
            },
            "$set": {
                "last_accessed_at": now,
            },
        },
        upsert=True,
    )

    progress = await _get_module_progress(user_id, module_id)

    return {
        "success": True,
        "message": "Module started",
        "progress": {
            "completed_steps": progress.get("completed_steps", []) if progress else [],
            "current_step": progress.get("current_step", 1) if progress else 1,
            "xp_earned": progress.get("xp_earned", 0) if progress else 0,
            "badge_unlocked": progress.get("badge_unlocked") if progress else None,
            "progress_pct": _calculate_progress(module, progress),
        },
    }


@router.post("/{module_id}/steps/{step_number}/complete")
async def complete_step(module_id: str, step_number: int, user=Depends(get_current_user)):
    try:
        module = await learning_modules_collection().find_one({"_id": ObjectId(module_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid module ID")

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    steps = module.get("steps", [])
    if step_number < 1 or step_number > len(steps):
        raise HTTPException(status_code=400, detail="Invalid step number")

    user_id = user["id"]
    progress = await _get_module_progress(user_id, module_id)

    if not progress:
        raise HTTPException(status_code=404, detail="Module progress not found — start the module first")

    completed = progress.get("completed_steps", [])
    if step_number in completed:
        return {
            "success": True,
            "message": "Step already completed",
            "completed_steps": len(completed),
            "total_steps": len(steps),
            "progress_pct": _calculate_progress(module, progress),
            "xp_earned": 0,
            "badge_unlocked": None,
        }

    xp_per_step = module.get("xp_reward", 0) // max(len(steps), 1)
    xp_earned = xp_per_step

    now = datetime.now(timezone.utc)
    completed.append(step_number)
    completed.sort()

    total_xp = progress.get("xp_earned", 0) + xp_earned

    badge_unlocked = None
    if len(completed) == len(steps) and module.get("badge_reward"):
        badge_unlocked = module["badge_reward"]

    await user_learning_progress_collection().update_one(
        {"user_id": user_id, "module_id": module_id},
        {
            "$set": {
                "completed_steps": completed,
                "current_step": step_number + 1 if step_number < len(steps) else step_number,
                "xp_earned": total_xp,
                "completed_at": now if len(completed) == len(steps) else None,
                "badge_unlocked": badge_unlocked,
            },
        },
    )

    return {
        "success": True,
        "message": "Step completed" + (" — Module complete!" if badge_unlocked else ""),
        "completed_steps": len(completed),
        "total_steps": len(steps),
        "progress_pct": _calculate_progress(module, {"completed_steps": completed}),
        "xp_earned": xp_earned,
        "total_xp": total_xp,
        "badge_unlocked": badge_unlocked,
    }


@router.get("/user/progress")
async def get_user_progress(user=Depends(get_current_user)):
    user_id = user["id"]

    all_progress = await user_learning_progress_collection().find({"user_id": user_id}).to_list(length=100)

    completed_count = 0
    total_xp = 0
    all_badges = []

    for p in all_progress:
        mid = p.get("module_id")
        if not mid:
            continue
        module = await learning_modules_collection().find_one({"_id": ObjectId(mid)})
        if not module:
            continue
        completed_steps = p.get("completed_steps", [])
        total_steps = len(module.get("steps", []))
        if total_steps > 0 and len(completed_steps) == total_steps:
            completed_count += 1
        total_xp += p.get("xp_earned", 0)
        badge = p.get("badge_unlocked")
        if badge and badge not in all_badges:
            all_badges.append(badge)

    total_modules = await learning_modules_collection().count_documents({})
    overall_pct = round((completed_count / total_modules * 100), 1) if total_modules > 0 else 0.0

    user_doc = await users_collection().find_one({"_id": ObjectId(user_id)})
    streak = user_doc.get("learning_streak", 0) if user_doc else 0

    return {
        "success": True,
        "completed_modules": completed_count,
        "total_modules": total_modules,
        "overall_progress_pct": overall_pct,
        "current_streak": streak,
        "xp_earned_today": total_xp,
        "badges": all_badges,
    }


@router.get("/recommendations")
async def get_recommendations(
    company: Optional[str] = Query(default=None),
    user=Depends(get_current_user),
):
    user_id = user["id"]
    target_company = company or user.get("target_company")

    all_progress = await user_learning_progress_collection().find({"user_id": user_id}).to_list(length=100)
    completed_modules = set()

    for p in all_progress:
        mid = p.get("module_id")
        progress_doc = p
        module = await learning_modules_collection().find_one({"_id": ObjectId(mid)})
        if not module:
            continue
        steps = module.get("steps", [])
        completed = progress_doc.get("completed_steps", [])
        if len(steps) > 0 and len(completed) == len(steps):
            completed_modules.add(mid)

    query = {}
    if target_company:
        query["company_tags"] = {"$regex": target_company, "$options": "i"}

    if completed_modules:
        from bson import ObjectId as BSONObjectId
        oid_list = []
        for mid in completed_modules:
            try:
                oid_list.append(BSONObjectId(mid))
            except Exception:
                pass
        if oid_list:
            query["_id"] = {"$nin": oid_list}

    modules = await learning_modules_collection().find(query).limit(10).to_list(length=10)

    recommendations = []
    for module in modules:
        progress = await _get_module_progress(user_id, str(module["_id"]))
        pct = _calculate_progress(module, progress)
        recommendations.append({
            **_serialize_module(module),
            "user_progress": pct,
            "is_started": progress is not None,
            "recommendation_reason": _get_recommendation_reason(module, target_company, pct),
        })

    recommendations.sort(key=lambda m: m.get("user_progress", 0))

    return {"success": True, "recommendations": recommendations}