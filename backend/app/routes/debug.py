"""Debug / error tracking endpoints.

Frontend errors (window.onerror, unhandled rejections, React error
boundaries) are POSTed here so crashes are visible instead of silent.
Logs are persisted in MongoDB and also printed via structured logging.
"""
import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.database import debug_logs_collection
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/debug", tags=["debug"])


class ClientErrorReport(BaseModel):
    message: str
    stack: Optional[str] = None
    url: Optional[str] = None
    component: Optional[str] = None
    level: str = "error"
    user_agent: Optional[str] = None


@router.post("/log")
async def log_client_error(report: ClientErrorReport):
    """Record a client-side error/exception for later inspection."""
    doc = {
        "message": report.message[:2000],
        "stack": report.stack[:8000] if report.stack else None,
        "url": report.url[:500] if report.url else None,
        "component": report.component[:200] if report.component else None,
        "level": report.level,
        "user_agent": report.user_agent[:500] if report.user_agent else None,
        "created_at": datetime.now(timezone.utc),
    }
    try:
        await debug_logs_collection.insert_one(doc)
    except Exception:
        logger.exception("Failed to persist client error log")

    logger.warning(
        "Client error: %s (component=%s url=%s)",
        doc["message"],
        doc["component"],
        doc["url"],
    )
    return {"status": "ok"}


@router.get("/logs")
async def list_debug_logs(limit: int = Query(50, ge=1, le=500), user=Depends(get_current_user)):
    """Return recent client error logs (newest first). Admin only."""
    is_admin = user.get("role") == "admin" or user.get("is_admin") is True
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        cursor = debug_logs_collection.find().sort("created_at", -1).limit(limit)
        logs = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            logs.append(doc)
        return {"logs": logs}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read debug logs: {exc}")
