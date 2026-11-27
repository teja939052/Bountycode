"""Personal dashboard routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/personal-dashboard", tags=["personal-dashboard"])


@router.get("/overview")
async def get_personal_dashboard(user=Depends(get_current_user)):
    """Get user's personal dashboard overview."""
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
        "name": user_obj.name,
        "email": user_obj.email,
        "plan": user_obj.plan,
        "total_xp": 0,
        "current_level": 1,
        "current_streak": 0,
        "total_badges": 0,
        "recent_activity": [],
    }