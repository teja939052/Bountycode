"""Learning modules routes — Duolingo-style step-by-step lessons."""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.middleware.auth import get_current_user
from app.database import learning_modules_collection, user_learning_progress_collection
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/learning-modules", tags=["learning-modules"])


class StepCompleteRequest(BaseModel):
    step_index: int
    passed: bool = True


class StartModuleRequest(BaseModel):
    pass


def _serialize(module: dict) -> dict:
    if not module:
        return module
    out = dict(module)
    out["id"] = str(out.pop("_id", out.get("id", "")))
    return out


@router.get("")
async def list_modules(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    company: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    query: Dict[str, Any] = {}
    if difficulty:
        query["difficulty"] = difficulty
    if topic:
        query["topic"] = topic
    if company:
        query.setdefault("company_tags", {})["$elemMatch"] = {"$eq": company}

    cursor = learning_modules_collection.find(query).skip((page - 1) * limit).limit(limit)
    modules = []
    async for m in cursor:
        modules.append(_serialize(m))
    return {"modules": modules, "page": page, "limit": limit}


@router.get("/{module_id}")
async def get_module(module_id: str, user=Depends(get_current_user)):
    module = await learning_modules_collection.find_one({"_id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    progress = await user_learning_progress_collection.find_one(
        {"user_id": user["id"], "module_id": module_id}
    )
    data = _serialize(module)
    data["user_progress"] = progress.get("progress", 0) if progress else 0
    data["is_started"] = bool(progress)
    return data


@router.post("/{module_id}/start")
async def start_module(module_id: str, user=Depends(get_current_user)):
    module = await learning_modules_collection.find_one({"_id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    await user_learning_progress_collection.update_one(
        {"user_id": user["id"], "module_id": module_id},
        {"$setOnInsert": {"started_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()}},
        upsert=True,
    )
    return {"success": True}


@router.post("/{module_id}/steps/{step_number}/complete")
async def complete_step(module_id: str, step_number: int, body: StepCompleteRequest, user=Depends(get_current_user)):
    module = await learning_modules_collection.find_one({"_id": module_id})
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    steps = module.get("steps", [])
    if step_number < 0 or step_number >= len(steps):
        raise HTTPException(status_code=400, detail="Invalid step index")
    progress = await user_learning_progress_collection.find_one(
        {"user_id": user["id"], "module_id": module_id}
    )
    completed = progress.get("completed_steps", []) if progress else []
    if step_number not in completed:
        completed.append(step_number)
    pct = int((len(completed) / len(steps)) * 100) if steps else 0
    await user_learning_progress_collection.update_one(
        {"user_id": user["id"], "module_id": module_id},
        {"$set": {"completed_steps": completed, "progress": pct, "updated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()}},
        upsert=True,
    )
    if pct == 100:
        await record_practice(user_id=user["id"], activity_type="module_complete", score=100)
    return {"success": True, "progress": pct}


@router.get("/user/progress")
async def get_user_progress(user=Depends(get_current_user)):
    cursor = user_learning_progress_collection.find({"user_id": user["id"]})
    items = []
    async for p in cursor:
        items.append({"module_id": p.get("module_id"), "progress": p.get("progress", 0), "completed_steps": p.get("completed_steps", [])})
    return {"progress": items}


@router.get("/recommendations")
async def get_recommendations(company: Optional[str] = None, user=Depends(get_current_user)):
    query: Dict[str, Any] = {}
    if company:
        query["company_tags"] = {"$elemMatch": {"$eq": company}}
    cursor = learning_modules_collection.find(query).limit(10)
    modules = []
    async for m in cursor:
        modules.append(_serialize(m))
    return {"recommendations": modules}
