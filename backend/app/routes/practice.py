"""Practice — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/practice", tags=["practice"])


class PracticeSessionResponse:
    """Response for a practice session."""
    def __init__(self, session_id: str, company: str, role: str, 
                 focus_areas: List[str], coding: List[dict], 
                 behavioral: List[dict], system_design: List[dict],
                 weak_areas: List[str], strong_areas: List[str],
                 probability_before: float, probability_after_target: float):
        self.session_id = session_id
        self.company = company
        self.role = role
        self.focus_areas = focus_areas
        self.coding = coding
        self.behavioral = behavioral
        self.system_design = system_design
        self.weak_areas = weak_areas
        self.strong_areas = strong_areas
        self.probability_before = probability_before
        self.probability_after_target = probability_after_target


router = APIRouter(prefix="/api/v1/practice", tags=["practice"])


@router.post("/session")
async def practice_session(company: str = "", role: str = "SDE", focus_areas: List[str] = None, user=Depends(get_current_user)):
    """Create a practice session."""
    session_id = str(user["id"]) + "-" + str(datetime.now().timestamp())
    
    return {
        "session_id": session_id,
        "company": company,
        "role": role,
        "focus_areas": focus_areas or [],
        "coding": [],
        "behavioral": [],
        "system_design": [],
        "weak_areas": [],
        "strong_areas": [],
        "probability_before": 0.0,
        "probability_after_target": 0.0,
    }


@router.get("/profile")
async def practice_profile(user=Depends(get_current_user)):
    """Get user's practice profile."""
    return {"profile": {"companies": [], "roles": [], "focus_areas": []}}


@router.post("/company-blueprint")
async def company_blueprint_endpoint(company: str, user=Depends(get_current_user)):
    """Get company-specific practice blueprint."""
    return {"blueprint": {"company": company, "topics": [], "difficulty": "mixed"}}