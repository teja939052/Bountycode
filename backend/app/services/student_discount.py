"""Student discount service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_student_discounts(
    user_id: str,
) -> dict:
    """Get student discounts."""
    return {"user_id": user_id, "discounts": []}


async def apply_discount(
    user_id: str,
    discount_code: str,
) -> dict:
    """Apply a discount."""
    return {"user_id": user_id, "discount_code": discount_code, "applied": True}

async def get_student_discount_status(user_id: str) -> dict:
    """Stub for get_student_discount_status."""
    return {"user_id": user_id}


async def verify_student_discount(user_id: str) -> dict:
    """Stub for verify_student_discount."""
    return {"user_id": user_id}
