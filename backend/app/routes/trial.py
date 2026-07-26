from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middleware.auth import get_current_user
from app.services.trial import start_trial, check_trial_status, cancel_trial

router = APIRouter(prefix="/api/trial", tags=["trial"])


@router.post("/start")
async def start_user_trial(user=Depends(get_current_user)):
    existing = await check_trial_status(user["id"])
    if existing.get("active"):
        return existing
    return await start_trial(user["id"])


@router.get("/status")
async def get_trial_status(user=Depends(get_current_user)):
    return await check_trial_status(user["id"])


@router.post("/cancel")
async def cancel_user_trial(user=Depends(get_current_user)):
    return await cancel_trial(user["id"])
