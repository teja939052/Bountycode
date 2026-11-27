"""Progress routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


@router.get("/overview")
async def get_progress_overview(user=Depends(get_current_user)):
    """Get user's progress overview."""
    async with get_session() as session:
        from app.models.identity import User
        result = await session.execute(
            select(User).where(User.id == user["id"])
        )
        user_obj = result.scalar_one_or_none()
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user["id"],
        "total_lessons_completed": 0,
        "total_questions_solved": 0,
        "current_level": 1,
        "skills_mastered": 0,
        "recent_activity": [],
    }