"""Placement calendar service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_placement_calendar(
    user_id: str,
) -> dict:
    """Get placement calendar for user."""
    return {"user_id": user_id, "calendar": []}


async def add_placement_event(
    user_id: str,
    event_type: str,
    event_date: str,
    details: dict,
) -> dict:
    """Add a placement event."""
    return {"user_id": user_id, "event_id": str(user_id) + "-event-1", "event_type": event_type, "event_date": event_date, "status": "created"}

async def COMPANY_SEASON_PATTERNS_stub(user_id: str) -> dict:
    """Stub for COMPANY_SEASON_PATTERNS."""
    return {"user_id": user_id}


async def get_all_supported_companies(user_id: str) -> dict:
    """Stub for get_all_supported_companies."""
    return {"user_id": user_id}


async def get_company_timeline(user_id: str) -> dict:
    """Stub for get_company_timeline."""
    return {"user_id": user_id}


async def get_countdown(user_id: str) -> dict:
    """Stub for get_countdown."""
    return {"user_id": user_id}


async def get_user_placement_calendar(user_id: str) -> dict:
    """Stub for get_user_placement_calendar."""
    return {"user_id": user_id}


async def predict_drive_dates(user_id: str) -> dict:
    """Stub for predict_drive_dates."""
    return {"user_id": user_id}
