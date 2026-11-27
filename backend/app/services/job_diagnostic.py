"""Job diagnostic service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_job_diagnostic(
    user_id: str,
) -> dict:
    """Get job diagnostic for user."""
    return {"user_id": user_id, "diagnostic": {}}


async def submit_job_diagnostic(
    user_id: str,
    answers: dict,
) -> dict:
    """Submit job diagnostic answers."""
    return {"user_id": user_id, "diagnostic_id": str(user["id"]) + "-diag-1", "score": 0}

async def get_diagnostic_questions(user_id: str) -> dict:
    """Stub for get_diagnostic_questions."""
    return {"user_id": user_id}


async def run_job_diagnostic(user_id: str) -> dict:
    """Stub for run_job_diagnostic."""
    return {"user_id": user_id}
