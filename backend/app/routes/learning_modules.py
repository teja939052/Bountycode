"""Learning Modules routes — Duolingo-style step-by-step coding lessons.
Migrated from MongoDB `learning_modules` collection to PostgreSQL repositories.
"""
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.repositories.learning import (
    LearningModuleRepository,
    UserLearningProgressRepository,
)
from app.models.learning import LearningModule, UserLearningProgress
from app.services.postgres_gamification import record_practice as pg_record_practice

router = APIRouter(prefix="/api/v1/learning-modules", tags=["Learning Modules"])


def _serialize_module(module: LearningModule) -> dict:
    return {
        "id": str(module.id),
        "question_id": module.question_id,
        "title": module.title,
        "description": module.description,
        "difficulty": module.difficulty,
        "estimated_time_minutes": module.estimated_time_minutes,
        "steps": module.steps,
        "xp_reward": module.xp_reward,
        "badge_reward": module.badge_reward,
        "company_tags": module.company_tags,
        "topic": module.topic,
        "created_at": module.created_at.isoformat() if module.created_at else None,
    }


def _calculate_progress(module: LearningModule, progress: Optional[UserLearningProgress]) -> float:
    total_steps = len(module.steps)
    if total_steps == 0:
        return 0.0
    if progress and progress.completed_steps:
        return round((len(progress.completed_steps) / total_steps) * 100, 1)
    return 0.0


async def _get_module_progress(session: AsyncSession, user_id: UUID, module_id: UUID) -> Optional[UserLearningProgress]:
    repo = UserLearningProgressRepository(session)
    return await repo.get_by_user_and_module(user_id, module_id)


def _get_recommendation_reason(module: LearningModule, target_company: Optional[str], progress: float) -> str:
    if progress > 0 and progress < 100:
        return "Continue your progress"
    if target_company and target_company.lower() in [c.lower() for c in module.company_tags]:
        return f"Relevant for {target_company}"
    if module.difficulty == "beginner":
        return "Great for building foundational skills"
    if module.difficulty == "intermediate":
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
    session: AsyncSession = Depends(get_session),
):
    repo = LearningModuleRepository(session)
    progress_repo = UserLearningProgressRepository(session)

    # Build filter
    filters = {}
    if difficulty:
        filters["difficulty"] = difficulty.lower()
    if topic:
        filters["topic"] = topic
    if company:
        filters["company_tags"] = company

    modules = await repo.list(filters=filters, skip=(page - 1) * limit, limit=limit)
    total = await repo.count(filters=filters)

    modules_with_progress = []
    for module in modules:
        progress = await _get_module_progress(session, UUID(user["id"]), module.id)
        pct = _calculate_progress(module, progress)
        modules_with_progress.append({
            **_serialize_module(module),
            "user_progress": pct,
            "is_started": progress is not None,
        })

    return {"success": True, "modules": modules_with_progress, "total": total, "page": page}


@router.get("/{module_id}")
async def get_module(module_id: str, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        module_id_uuid = UUID(module_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid module ID")

    repo = LearningModuleRepository(session)
    module = await repo.get_by_id(module_id_uuid)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    progress_repo = UserLearningProgressRepository(session)
    progress = await progress_repo.get_by_user_and_module(UUID(user["id"]), module_id_uuid)

    await progress_repo.update(
        module_id_uuid,
        {
            "last_accessed_at": datetime.now(timezone.utc),
            "current_step": progress.current_step if progress else 1,
        },
    )

    if progress:
        return {
            "success": True,
            "module": _serialize_module(module),
            "progress": {
                "completed_steps": progress.completed_steps,
                "current_step": progress.current_step,
                "xp_earned": progress.xp_earned,
                "badge_unlocked": progress.badge_unlocked,
                "started_at": progress.started_at.isoformat() if progress.started_at else None,
                "progress_pct": _calculate_progress(module, progress),
            },
        }

    return {
        "success": True,
        "module": _serialize_module(module),
        "progress": None,
    }


@router.post("/{module_id}/start")
async def start_module(module_id: str, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        module_id_uuid = UUID(module_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid module ID")

    repo = LearningModuleRepository(session)
    module = await repo.get_by_id(module_id_uuid)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    user_id = UUID(user["id"])
    now = datetime.now(timezone.utc)

    progress_repo = UserLearningProgressRepository(session)
    await progress_repo.create(
        user_id=user_id,
        module_id=module_id,
        started_at=now,
        completed_steps=[],
        current_step=1,
        xp_earned=0,
    )

    progress = await progress_repo.get_by_user_and_module(user_id, module_id)

    return {
        "success": True,
        "message": "Module started",
        "progress": {
            "completed_steps": progress.completed_steps if progress else [],
            "current_step": progress.current_step if progress else 1,
            "xp_earned": progress.xp_earned if progress else 0,
            "badge_unlocked": progress.badge_unlocked if progress else None,
            "progress_pct": _calculate_progress(module, progress),
        },
    }


@router.post("/{module_id}/steps/{step_number}/complete")
async def complete_step(module_id: str, step_number: int, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    repo = LearningModuleRepository(session)
    module = await repo.get_by_id(UUID(module_id))

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    steps = module.steps
    if step_number < 1 or step_number > len(steps):
        raise HTTPException(status_code=400, detail="Invalid step number")

    user_id = UUID(user["id"])
    progress_repo = UserLearningProgressRepository(session)
    progress = await progress_repo.get_by_user_and_module(user_id, module_id)

    if not progress:
        raise HTTPException(status_code=404, detail="Module progress not found — start the module first")

    completed = list(progress.completed_steps)
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

    xp_per_step = module.xp_reward // max(len(steps), 1)
    xp_earned = xp_per_step

    now = datetime.now(timezone.utc)
    completed.append(step_number)
    completed.sort()

    total_xp = progress.xp_earned + xp_earned

    badge_unlocked = None
    if len(completed) == len(steps) and module.badge_reward:
        badge_unlocked = module.badge_reward

    await progress_repo.update(
        module.id,
        {
            "completed_steps": completed,
            "current_step": step_number + 1 if step_number < len(steps) else step_number,
            "xp_earned": total_xp,
            "completed_at": now if len(completed) == len(steps) else None,
            "badge_unlocked": badge_unlocked,
        },
    )

    return {
        "success": True,
        "message": "Step completed" + (" — Module complete!" if badge_unlocked else ""),
        "completed_steps": len(completed),
        "total_steps": len(steps),
        "progress_pct": _calculate_progress(module, type("M", (), {"steps": module.steps})()),
        "xp_earned": xp_earned,
        "total_xp": total_xp,
        "badge_unlocked": badge_unlocked,
    }


@router.get("/user/progress")
async def get_user_progress(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_id = UUID(user["id"])
    progress_repo = UserLearningProgressRepository(session)
    module_repo = LearningModuleRepository(session)

    all_progress = await progress_repo.list_by_user(user_id, limit=100, offset=0)

    completed_count = 0
    total_xp = 0
    all_badges = []

    for p in all_progress:
        module = await module_repo.get_by_id(p.module_id)
        if not module:
            continue
        completed_steps = p.completed_steps
        total_steps = len(module.steps)
        if total_steps > 0 and len(completed_steps) == total_steps:
            completed_count += 1
        total_xp += p.xp_earned
        badge = p.badge_unlocked
        if badge and badge not in all_badges:
            all_badges.append(badge)

    total_modules = await module_repo.count(filters={})
    overall_pct = round((completed_count / total_modules * 100), 1) if total_modules > 0 else 0.0

    return {
        "success": True,
        "completed_modules": completed_count,
        "total_modules": total_modules,
        "overall_progress_pct": overall_pct,
        "current_streak": 0,  # Streak tracked in gamification profile
        "xp_earned_today": total_xp,
        "badges": all_badges,
    }


@router.get("/recommendations")
async def get_recommendations(
    company: Optional[str] = Query(default=None),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    user_id = UUID(user["id"])
    target_company = company or user.get("target_company")

    progress_repo = UserLearningProgressRepository(session)
    module_repo = LearningModuleRepository(session)

    all_progress = await progress_repo.list_by_user(user_id, limit=100, offset=0)
    completed_modules = set()

    for p in all_progress:
        completed_steps = p.completed_steps
        module = await module_repo.get_by_id(p.module_id)
        if not module:
            continue
        total_steps = len(module.steps)
        if total_steps > 0 and len(completed_steps) == total_steps:
            completed_modules.add(p.module_id)

    query = {}
    if target_company:
        query["company_tags"] = target_company

    if completed_modules:
        oid_list = []
        for mid in completed_modules:
            try:
                oid_list.append(UUID(mid))
            except Exception:
                pass
        if oid_list:
            query["_id"] = {"$nin": oid_list}

    modules = await module_repo.list(filters=query, limit=10, offset=0)

    recommendations = []
    for module in modules:
        progress = await progress_repo.get_by_user_and_module(user_id, module.id)
        pct = _calculate_progress(module, progress)
        recommendations.append({
            **_serialize_module(module),
            "user_progress": pct,
            "is_started": progress is not None,
            "recommendation_reason": _get_recommendation_reason(module, target_company, pct),
        })

    recommendations.sort(key=lambda m: m.get("user_progress", 0))

    return {"success": True, "recommendations": recommendations}