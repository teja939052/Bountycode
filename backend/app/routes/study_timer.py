"""Study Timer API routes — session tracking with focus scoring."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.study_timer import start_session, pause_session, complete_session, get_stats

router = APIRouter(prefix="/api/v1/study-timer", tags=["Study Timer"])


class StartSessionReq(BaseModel):
    activity_type: str = "general"
    topic: Optional[str] = None


class PauseSessionReq(BaseModel):
    session_id: str


class CompleteSessionReq(BaseModel):
    session_id: str


@router.post("/start")
async def api_start_session(req: StartSessionReq, user=Depends(get_current_user)):
    return await start_session(user["id"], req.activity_type, req.topic)


@router.post("/pause")
async def api_pause_session(req: PauseSessionReq, user=Depends(get_current_user)):
    try:
        return await pause_session(user["id"], req.session_id)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/complete")
async def api_complete_session(req: CompleteSessionReq, user=Depends(get_current_user)):
    try:
        return await complete_session(user["id"], req.session_id)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/stats")
async def api_study_stats(user=Depends(get_current_user)):
    return await get_stats(user["id"])
