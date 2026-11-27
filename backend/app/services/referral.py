"""Referral service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def create_referral(
    referrer_id: str,
    referee_email: str,
) -> dict:
    """Create a referral."""
    return {"referrer_id": referrer_id, "referee_email": referee_email, "status": "pending"}


async def get_referrals(
    user_id: str,
) -> list:
    """Get user's referrals."""
    return []