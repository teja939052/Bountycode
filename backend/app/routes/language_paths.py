"""Language Learning Paths API - 7 languages x 100 levels x 80 modules.
Each language covers first principles -> DSA -> OOPs -> complex systems.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.utils.timeutil import utcnow
from app.middleware.auth import get_current_user
from app.database import get_db
from app.models.user import UserInDB
import uuid

router = APIRouter(prefix="/api/v1/languages", tags=["languages"])

LANGUAGES = [
    {"id": "python", "name": "Python", "icon": "🐍", "primary_use": "Web, Data Science, AI/ML, Automation"},
    {"id": "javascript", "name": "JavaScript", "icon": "🟨", "primary_use": "Web Frontend, Backend (Node.js), Mobile"},
    {"id": "java", "name": "Java", "icon": "☕", "primary_use": "Enterprise, Android, Web Backend"},
    {"id": "cpp", "name": "C++", "icon": "⚡", "primary_use": "Systems, Game Dev, High Performance"},
    {"id": "c", "name": "C", "icon": "🔷", "primary_use": "Systems Programming, Embedded, OS"},
    {"id": "go", "name": "Go", "icon": "🟢", "primary_use": "Cloud, Backend, DevOps, Microservices"},
    {"id": "rust", "name": "Rust", "icon": "🦀", "primary_use": "Systems, WebAssembly, Performance-Critical"},
]

class LanguagePath(BaseModel):
    id: str
    language_id: str
    language_name: str
    level: int
    tier: int
    module_index: int
    name: str
    description: str
    xp_reward: int
    difficulty: str
    type: str
    estimated_time: str
    content: Dict[str, Any]
    prerequisites: List[str]
    related_modules: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime

class LanguageLevel(BaseModel):
    language_id: str
    level: int
    tier: int
    name: str
    description: str
    modules: List[str]
    xp_required: int
    xp_reward: int
    unlocks_at: int
    is_review: bool
    badge: str

class LanguageProgress(BaseModel):
    language_id: str
    level: int
    xp: int
    completed_modules: List[str]
    completed_levels: List[int]
    started_at: datetime
    last_activity: datetime

class LanguageResponse(BaseModel):
    id: str
    name: str
    icon: str
    primary_use: str
    total_modules: int
    total_levels: int
    total_xp: int
    description: str

@router.get("/", response_model=List[LanguageResponse])
async def get_languages(
    current_user: UserInDB = Depends(get_current_user)
):
    """Get all available programming languages with learning paths."""
    db = get_db()
    languages = []
    for lang in LANGUAGES:
        module_count = await db.language_modules.count_documents({"language_id": lang["id"]})
        level_count = await db.language_levels.count_documents({"language_id": lang["id"]})
        total_xp = await db.language_modules.aggregate([
            {"$match": {"language_id": lang["id"]}},
            {"$group": {"_id": None, "total": {"$sum": "$xp_reward"}}}
        ]).to_list(1)
        total_xp_val = total_xp[0]["total"] if total_xp else 0
        languages.append(LanguageResponse(
            id=lang["id"],
            name=lang["name"],
            icon=lang["icon"],
            primary_use=lang["primary_use"],
            total_modules=module_count,
            total_levels=level_count,
            total_xp=total_xp_val,
            description=f"Complete {module_count} modules across {level_count} levels to master {lang['name']}."
        ))
    return languages

@router.get("/{language_id}", response_model=List[LanguagePath])
async def get_language_path(
    language_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Get the full learning path for a language (100 levels, 80 modules)."""
    if language_id not in [l["id"] for l in LANGUAGES]:
        raise HTTPException(status_code=404, detail="Language not found")
    db = get_db()
    modules = await db.language_modules.find({"language_id": language_id}).sort("module_index", 1).to_list(None)
    return [LanguagePath(**m) for m in modules]

@router.get("/{language_id}/levels", response_model=List[LanguageLevel])
async def get_language_levels(
    language_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Get all levels for a language."""
    if language_id not in [l["id"] for l in LANGUAGES]:
        raise HTTPException(status_code=404, detail="Language not found")
    db = get_db()
    levels = await db.language_levels.find({"language_id": language_id}).sort("level", 1).to_list(None)
    return [LanguageLevel(**l) for l in levels]

@router.get("/{language_id}/modules/{module_index}", response_model=LanguagePath)
async def get_module_detail(
    language_id: str,
    module_index: int,
    current_user: UserInDB = Depends(get_current_user)
):
    """Get detailed content for a specific module."""
    db = get_db()
    module = await db.language_modules.find_one({
        "language_id": language_id,
        "module_index": module_index
    })
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return LanguagePath(**module)

@router.get("/{language_id}/progress", response_model=LanguageProgress)
async def get_language_progress(
    language_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Get user's progress in a language learning path."""
    if language_id not in [l["id"] for l in LANGUAGES]:
        raise HTTPException(status_code=404, detail="Language not found")
    db = get_db()
    progress = await db.language_progress.find_one({
        "user_id": str(current_user.id),
        "language_id": language_id
    })
    if not progress:
        progress = LanguageProgress(
            language_id=language_id,
            level=1,
            xp=0,
            completed_modules=[],
            completed_levels=[],
            started_at=utcnow(),
            last_activity=utcnow()
        )
        await db.language_progress.insert_one(progress.dict())
    return LanguageProgress(**progress)

@router.post("/{language_id}/modules/{module_index}/complete", response_model=Dict[str, Any])
async def complete_module(
    language_id: str,
    module_index: int,
    current_user: UserInDB = Depends(get_current_user)
):
    """Mark a module as complete and award XP."""
    db = get_db()
    module = await db.language_modules.find_one({
        "language_id": language_id,
        "module_index": module_index
    })
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    progress = await db.language_progress.find_one({
        "user_id": str(current_user.id),
        "language_id": language_id
    })
    
    module_id = module["id"]
    xp_gained = module["xp_reward"]
    
    if not progress:
        progress = {
            "user_id": str(current_user.id),
            "language_id": language_id,
            "level": 1,
            "xp": 0,
            "completed_modules": [],
            "completed_levels": [],
            "started_at": utcnow(),
            "last_activity": utcnow()
        }
    
    if module_id not in progress["completed_modules"]:
        progress["completed_modules"].append(module_id)
        progress["xp"] += xp_gained
        progress["last_activity"] = utcnow()
        
        # Check if user leveled up
        new_level = min(progress["xp"] // 100 + 1, 100)
        if new_level > progress["level"]:
            progress["level"] = new_level
            if new_level not in progress["completed_levels"]:
                progress["completed_levels"].append(new_level)
        
        await db.language_progress.replace_one(
            {"user_id": str(current_user.id), "language_id": language_id},
            progress,
            upsert=True
        )
        
        # Award XP via gamification
        await db.gamification.update_one(
            {"user_id": str(current_user.id)},
            {"$inc": {"xp": xp_gained}},
            upsert=True
        )
    
    return {
        "success": True,
        "xp_gained": xp_gained,
        "total_xp": progress["xp"],
        "level": progress["level"],
        "new_level_unlocked": new_level > progress["level"] if progress.get("level") else False
    }

@router.get("/{language_id}/recommendations", response_model=List[LanguagePath])
async def get_recommendations(
    language_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Get recommended next modules based on user progress and weak areas."""
    if language_id not in [l["id"] for l in LANGUAGES]:
        raise HTTPException(status_code=404, detail="Language not found")
    
    db = get_db()
    progress = await db.language_progress.find_one({
        "user_id": str(current_user.id),
        "language_id": language_id
    })
    
    if not progress:
        # New user - recommend first 3 modules
        modules = await db.language_modules.find({
            "language_id": language_id,
            "module_index": {"$lte": 3}
        }).sort("module_index", 1).to_list(3)
        return [LanguagePath(**m) for m in modules]
    
    completed = set(progress["completed_modules"])
    completed_indices = [m["module_index"] for m in await db.language_modules.find(
        {"language_id": language_id, "id": {"$in": list(completed)}}
    ).to_list(None)]
    next_indices = [i for i in range(1, 81) if i not in completed_indices][:5]
    
    modules = await db.language_modules.find({
        "language_id": language_id,
        "module_index": {"$in": next_indices}
    }).sort("module_index", 1).to_list(5)
    
    return [LanguagePath(**m) for m in modules]