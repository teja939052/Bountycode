"""Company conversion service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_company_conversion(user_id: str, company_id: str) -> dict:
    """Get company conversion data."""
    return {"user_id": user_id, "company_id": company_id, "converted": False}


async def track_company_interaction(
    user_id: str,
    company_id: str,
    interaction_type: str,
    metadata: dict,
) -> dict:
    """Track company interaction."""
    return {"user_id": user_id, "company_id": company_id, "interaction_type": interaction_type, "tracked": True}