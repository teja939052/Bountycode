"""Company track routes — company-specific preparation."""
from datetime import datetime, timezone
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from app.middleware.auth import get_current_user
from app.services.learning_paths import get_all_company_tracks

router = APIRouter(prefix="/api/v1/company-tracks", tags=["company-tracks"])


@router.get("/companies")
async def list_companies():
    """List all company tracks."""
    return await get_all_company_tracks()


@router.get("/tracks")
async def list_tracks():
    """List all learning tracks."""
    return {"tracks": [{"id": "sde", "name": "Software Development Engineer"}]}


@router.get("/user-progress")
async def user_progress(user=Depends(get_current_user)):
    """Get user's track progress."""
    return {"user_id": user["id"], "tracks": []}


@router.get("/track/{track_id}")
async def get_track(track_id: str):
    """Get track details."""
    return {"track_id": track_id, "name": track_id, "modules": []}