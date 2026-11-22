"""Observability routes — funnel metrics and algorithm health.

Endpoints:
  POST   /api/v1/observability/events          record a telemetry event
  GET    /api/v1/observability/funnel          funnel stats for current user
  GET    /api/v1/observability/algorithm-health algorithm health (aggregated)
  GET    /api/v1/observability/health          service health check
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.middleware.auth import get_current_user
from app.services.observability import (
    record_event,
    get_funnel_stats,
    get_algorithm_health,
    FUNNEL_EVENTS,
    ALGO_HEALTH_EVENTS,
)

router = APIRouter(prefix="/observability", tags=["observability"])


class EventRecord(BaseModel):
    event: str
    properties: Optional[Dict[str, Any]] = None


@router.post("/events")
async def record_telemetry_event(
    payload: EventRecord,
    user=Depends(get_current_user),
) -> Dict[str, Any]:
    """Record a telemetry event for the current user."""
    allowed = set(FUNNEL_EVENTS) | set(ALGO_HEALTH_EVENTS)
    if payload.event not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown event: {payload.event}. Allowed: {sorted(allowed)}",
        )
    await record_event(user["id"], payload.event, payload.properties)
    return {"recorded": True, "event": payload.event}


@router.get("/funnel")
async def funnel_stats(
    user=Depends(get_current_user),
) -> Dict[str, Any]:
    """Return funnel completion stats for the current user."""
    return await get_funnel_stats(user["id"])


@router.get("/algorithm-health")
async def algorithm_health() -> Dict[str, Any]:
    """Return aggregated algorithm health metrics (no auth required — public stats)."""
    return await get_algorithm_health()


@router.get("/health")
async def observability_health() -> Dict[str, str]:
    """Service health check for the observability subsystem."""
    return {"status": "ok", "service": "observability"}
