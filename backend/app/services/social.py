"""Social service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_social_data(
    user_id: str,
) -> dict:
    """Get user's social data."""
    return {"user_id": user_id, "friends": [], "connections": []}


async def add_friend(
    user_id: str,
    friend_id: str,
) -> dict:
    """Add a friend."""
    return {"user_id": user_id, "friend_id": friend_id, "status": "pending"}