"""Learning routes — interaction action logging and diagnosis."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.middleware.auth import get_current_user
from app.services.action_trace_logger import log_interaction_action
from app.services.misconception_diagnosis import diagnose_misconception

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


class InteractionActionRequest(BaseModel):
    atom_id: str
    session_id: str
    interaction_type: str
    action: str
    data: Dict[str, Any] = {}
    misconception_codes: Optional[List[str]] = None


@router.post("/interaction-action")
async def log_action(req: InteractionActionRequest, user=Depends(get_current_user)):
    misconception_codes = req.misconception_codes or []
    diagnosis = log_interaction_action(
        user_id=user.get("id", ""),
        atom_id=req.atom_id,
        session_id=req.session_id,
        interaction_type=req.interaction_type,
        action=req.action,
        data=req.data,
        misconception_codes=misconception_codes,
    )
    return {"success": True, "diagnosis": diagnosis}


@router.post("/diagnose")
async def diagnose(req: InteractionActionRequest, user=Depends(get_current_user)):
    action_trace = [{"type": req.action, "data": req.data}]
    result = diagnose_misconception(
        action_trace=action_trace,
        concept=req.atom_id,
        misconception_codes=req.misconception_codes or [],
    )
    return {"success": True, "diagnosis": result}
