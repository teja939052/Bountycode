"""Metrics routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])


@router.get("/system")
async def system_metrics(user=Depends(get_current_user)):
    """Get system metrics."""
    return {"cpu_usage": 0, "memory_usage": 0, "disk_usage": 0}


@router.get("/usage")
async def usage_metrics(user=Depends(get_current_user)):
    """Get user usage metrics."""
    return {"user_id": user["id"], "requests_today": 0, "errors_today": 0}