"""Role content service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_role_content(
    role: str,
) -> dict:
    """Get role-specific content."""
    return {"role": role, "content": []}


async def get_role_skills(
    role: str,
) -> list:
    """Get role-specific skills."""
    return []

async def get_next_role_activity(user_id: str) -> dict:
    """Stub for get_next_role_activity."""
    return {"user_id": user_id}


async def get_role_dashboard(user_id: str) -> dict:
    """Stub for get_role_dashboard."""
    return {"user_id": user_id}


async def record_role_activity(user_id: str) -> dict:
    """Stub for record_role_activity."""
    return {"user_id": user_id}
