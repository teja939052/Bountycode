"""Door 2 (dev) & Door 3 (beginner) launch endpoints."""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.services.onboarding_launch import (
    get_beginner_go,
    get_dev_launch,
    run_beginner_go,
    run_dev_launch,
)

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding-launch"])

VALID_TRACKS = {"programming", "cs", "algorithms", "backend", "ai"}

VALID_ROLES = {
    "sde", "frontend", "backend", "devops", "cybersecurity",
    "ai_software_developer", "data_analyst", "data_scientist",
    "qa_automation", "java_engineer", "ml_engineer", "product_analyst",
    "technical_assistant",
}


@router.get("/dev/start")
async def dev_start(track: Optional[str] = "programming", user=Depends(get_current_user)):
    if track not in VALID_TRACKS:
        track = "programming"
    return get_dev_launch(track)


@router.post("/dev/complete")
async def dev_complete(payload: Dict[str, Any], user=Depends(get_current_user)):
    track = payload.get("track", "programming")
    answers = payload.get("answers") or {}
    if track not in VALID_TRACKS:
        raise HTTPException(status_code=400, detail="Unknown track")
    uid = user.get("id") or user.get("_id")
    return await run_dev_launch(uid, track, answers)


@router.get("/beginner/start")
async def beginner_start(user=Depends(get_current_user)):
    return get_beginner_go()


@router.post("/beginner/complete")
async def beginner_complete(user=Depends(get_current_user)):
    uid = user.get("id") or user.get("_id")
    return await run_beginner_go(uid)
