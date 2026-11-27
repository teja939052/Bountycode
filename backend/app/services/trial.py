"""Trial service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session


async def start_trial(user_id: str, plan: str = "free") -> dict:
    """Start a trial for a user."""
    async with get_session() as session:
        from app.models.identity import User
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.plan = plan
            user.trial_start = datetime.now(timezone.utc)
            await session.commit()
        return {"user_id": user_id, "plan": plan, "status": "started"}


async def check_trial_status(user_id: str) -> dict:
    """Check trial status for a user."""
    async with get_session() as session:
        from app.models.identity import User
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return {"user_id": user_id, "trial_active": user is not None and user.plan == "trial"}


async def cancel_trial(user_id: str) -> dict:
    """Cancel a user's trial."""
    async with get_session() as session:
        from app.models.identity import User
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.plan = "free"
            await session.commit()
        return {"user_id": user_id, "status": "cancelled"}

async def get_trial_status(user_id: str) -> dict:
    """Stub for get_trial_status."""
    return {"user_id": user_id}
