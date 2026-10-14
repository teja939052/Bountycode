"""Pro trial lifecycle: start a 7-day no-card trial and check its status."""
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.trial import start_trial, check_trial_status, cancel_trial

router = APIRouter(prefix="/api/v1/trial", tags=["trial"])


@router.post("/start")
async def start(user=Depends(get_current_user)):
    return await start_trial(user["id"])


@router.get("/status")
async def status(user=Depends(get_current_user)):
    return await check_trial_status(user["id"])


@router.post("/cancel")
async def cancel(user=Depends(get_current_user)):
    return await cancel_trial(user["id"])
