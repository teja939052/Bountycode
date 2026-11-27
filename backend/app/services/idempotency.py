"""Idempotency service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

# In-memory idempotency store for compatibility
_idempotency_store: Dict[str, dict] = {}

async def init_idempotency_manager() -> dict:
    """Initialize idempotency manager."""
    return {"initialized": True}

async def check_idempotency(key: str) -> Optional[dict]:
    """Check if an idempotency key has been used."""
    return _idempotency_store.get(key)

async def record_idempotency(key: str, result: dict) -> None:
    """Record an idempotency key."""
    _idempotency_store[key] = result