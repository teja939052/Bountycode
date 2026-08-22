"""Audit logging service for admin actions."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.database import audit_logs_collection
from bson import ObjectId

logger = logging.getLogger(__name__)


async def log_audit(
    user_id: str,
    action: str,
    resource: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> None:
    """Log an admin action to the audit logs collection."""
    try:
        doc = {
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "resource_id": resource_id,
            "details": details or {},
            "ip_address": ip_address or "unknown",
            "timestamp": datetime.now(timezone.utc),
        }
        await audit_logs_collection.insert_one(doc)
    except Exception as e:
        logger.warning(f"Failed to log audit entry: {e}")


async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list:
    """Retrieve audit logs with optional filtering."""
    try:
        query = {}
        if user_id:
            query["user_id"] = user_id
        if action:
            query["action"] = action

        cursor = audit_logs_collection.find(query).sort("timestamp", -1).skip(offset).limit(limit)
        return await cursor.to_list(length=limit)
    except Exception as e:
        logger.warning(f"Failed to retrieve audit logs: {e}")
        return []