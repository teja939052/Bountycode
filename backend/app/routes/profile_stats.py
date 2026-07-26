from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.profile_stats import get_profile_stats, update_integrations

router = APIRouter(prefix="/api/profile", tags=["profile"])


class IntegrationUpdate(BaseModel):
    platform: str
    username: str


@router.get("/stats")
async def get_stats(user=Depends(get_current_user)):
    return await get_profile_stats(user["id"])


@router.put("/integrations")
async def update_integration(payload: IntegrationUpdate, user=Depends(get_current_user)):
    platform = payload.platform.lower()
    if platform not in ("github", "leetcode"):
        raise HTTPException(status_code=400, detail="Supported platforms: github, leetcode")
    return await update_integrations(user["id"], platform, payload.username)
