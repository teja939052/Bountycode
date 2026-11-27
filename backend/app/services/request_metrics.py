"""Request metrics service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

# Metrics object for compatibility with ai_core.py
metrics = {
    "requests": 0,
    "errors": 0,
}

async def get_request_metrics(
    user_id: str,
) -> dict:
    """Get request metrics for user."""
    return {"user_id": user_id, "requests": metrics["requests"], "errors": metrics["errors"]}


async def record_request_metric(
    user_id: str,
    endpoint: str,
    status_code: int,
    duration_ms: float,
) -> None:
    """Record a request metric."""
    metrics["requests"] += 1
    if status_code >= 400:
        metrics["errors"] += 1

async def metrics(user_id: str) -> dict:
    """Stub for metrics."""
    return {"user_id": user_id}
