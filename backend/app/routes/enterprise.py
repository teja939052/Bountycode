"""Enterprise features — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/enterprise", tags=["enterprise"])


@router.post("/cohorts")
async def create_cohort(
    name: str,
    institution: str,
    student_ids: Optional[List[str]] = None,
    user=Depends(get_current_user),
):
    async with get_session() as session:
        cohort_id = str(user["id"]) + "-" + str(datetime.now().timestamp())
        await session.execute(
            """INSERT INTO cohorts (id, name, institution, admin_id, student_ids, created_at)
               VALUES (:id, :name, :institution, :admin_id, :student_ids, :created_at)""",
            {
                "id": cohort_id,
                "name": name,
                "institution": institution,
                "admin_id": user["id"],
                "student_ids": student_ids or [],
                "created_at": datetime.now(timezone.utc),
            },
        )
        await session.commit()
    return {"cohort_id": cohort_id, "name": name, "institution": institution}


@router.get("/cohorts")
async def list_cohorts(user=Depends(get_current_user)):
    async with get_session() as session:
        result = await session.execute(
            select(Cohort.id, Cohort.name, Cohort.institution, Cohort.created_at)
            .where(Cohort.admin_id == user["id"])
            .order_by(Cohort.created_at.desc())
        )
        cohorts = result.fetchall()
    output = []
    for c in cohorts:
        output.append({
            "cohort_id": c[0],
            "name": c[1],
            "institution": c[2],
            "created_at": c[3],
        })
    return {"cohorts": output}


@router.get("/cohorts/{cohort_id}/progress")
async def get_cohort_progress(cohort_id: str, user=Depends(get_current_user)):
    async with get_session() as session:
        # Get cohort
        result = await session.execute(
            select(Cohort.id, Cohort.name, Cohort.student_ids)
            .where(Cohort.id == cohort_id, Cohort.admin_id == user["id"])
        )
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Cohort not found")

        student_ids = row[2] or []
        # Get skill and gamification data
        skill_result = await session.execute(
            select(User.skill_graphs).where(User.id == user["id"])
        )  # Simplified - would need proper join
        gam_result = await session.execute(
            select(User.gamification).where(User.id == user["id"])
        )  # Simplified

        students = []
        for sid in student_ids[:50]:
            students.append({
                "user_id": sid,
                "overall_score": 0,  # Placeholder
                "diamonds": 0,
                "level": 1,
                "streak": 0,
            })

    return {
        "cohort_id": cohort_id,
        "name": row[1],
        "students": students,
        "count": len(students),
    }