"""Application tracker service — PostgreSQL-backed."""
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session


async def create_application(user_id: str, company: str, role: str, job_url: str = "", notes: str = "") -> dict:
    async with get_session() as session:
        from app.models.operations import ApplicationTracking
        app = ApplicationTracking(
            user_id=user_id,
            company=company,
            role=role,
            job_url=job_url,
            notes=notes,
            stage="interested",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(app)
        await session.commit()
        await session.refresh(app)
        return {"application_id": str(app.id), "company": company, "role": role, "stage": "interested"}


async def get_application_pipeline(user_id: str) -> list:
    async with get_session() as session:
        from app.models.operations import ApplicationTracking
        result = await session.execute(
            select(ApplicationTracking)
            .where(ApplicationTracking.user_id == user_id)
            .order_by(ApplicationTracking.updated_at.desc())
        )
        apps = result.scalars().all()
    return [
        {
            "id": str(a.id),
            "company": a.company,
            "role": a.role,
            "job_url": a.job_url,
            "notes": a.notes,
            "stage": a.stage,
            "stage_name": a.stage,
            "stage_color": "blue",
            "created_at": a.created_at,
            "updated_at": a.updated_at,
        }
        for a in apps
    ]


async def update_application_stage(user_id: str, application_id: str, new_stage: str) -> dict:
    async with get_session() as session:
        from app.models.operations import ApplicationTracking
        result = await session.execute(
            select(ApplicationTracking).where(
                ApplicationTracking.id == application_id,
                ApplicationTracking.user_id == user_id,
            )
        )
        app = result.scalar_one_or_none()
        if not app:
            return {"success": False, "message": "Application not found"}
        app.stage = new_stage
        app.updated_at = datetime.now(timezone.utc)
        await session.commit()
        return {"success": True, "message": f"Moved to {new_stage}"}


async def get_application_stats(user_id: str) -> dict:
    async with get_session() as session:
        from app.models.operations import ApplicationTracking
        result = await session.execute(
            select(ApplicationTracking.stage, func.count(ApplicationTracking.id))
            .where(ApplicationTracking.user_id == user_id)
            .group_by(ApplicationTracking.stage)
        )
        stage_counts = {row[0]: row[1] for row in result.all()}
        total = sum(stage_counts.values())
    return {
        "total_applications": total,
        "by_stage": {stage: {"count": stage_counts.get(stage, 0), "name": stage, "color": "blue"}
                     for stage, count in stage_counts.items()},
    }


async def delete_application(user_id: str, application_id: str) -> dict:
    async with get_session() as session:
        from app.models.operations import ApplicationTracking
        result = await session.execute(
            select(ApplicationTracking).where(
                ApplicationTracking.id == application_id,
                ApplicationTracking.user_id == user_id,
            )
        )
        app = result.scalar_one_or_none()
        if not app:
            return {"success": False, "message": "Application not found"}
        await session.delete(app)
        await session.commit()
        return {"success": True, "message": "Application deleted"}


class ApplicationTracker:
    """Class wrapper around module-level functions for backward compatibility."""

    async def create_application(self, user_id, company, role, job_url="", notes=""):
        return await create_application(user_id, company, role, job_url, notes)

    async def get_user_pipeline(self, user_id):
        return await get_application_pipeline(user_id)

    async def update_stage(self, application_id, new_stage, user_id):
        return await update_application_stage(user_id, application_id, new_stage)

    async def get_stats(self, user_id):
        return await get_application_stats(user_id)

    async def delete_application(self, application_id, user_id):
        return await delete_application(user_id, application_id)

async def ApplicationTracker_stub(user_id: str) -> dict:
    """Stub for ApplicationTracker."""
    return {"user_id": user_id}


async def PIPELINE_STAGES_stub(user_id: str) -> dict:
    """Stub for PIPELINE_STAGES."""
    return {"user_id": user_id}
