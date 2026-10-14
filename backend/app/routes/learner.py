"""Learner + personalization routes.

Exposes:
- GET /api/v1/learner/state
- GET /api/v1/learner/next-mission
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.services.learner_state import get_learner_state
from app.services.personalization import select_next_mission

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/learner", tags=["learner"])


@router.get("/state")
async def get_learner_state_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Return the canonical learner state for the authenticated user."""
    user_id = current_user.get("id") or current_user.get("_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        state = await get_learner_state(user_id)
        if not state:
            raise HTTPException(status_code=404, detail="Learner state not found")
        return state
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to build learner state for %s", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to load learner state: {type(exc).__name__}: {exc}") from exc


@router.get("/next-mission")
async def get_next_mission(
    current_user: Dict[str, Any] = Depends(get_current_user),
    company: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    session_minutes: Optional[int] = Query(None, ge=1, le=180),
) -> Dict[str, Any]:
    """Return the next best mission and why it was chosen."""
    user_id = current_user.get("id") or current_user.get("_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        mission = await select_next_mission(
            user_id=user_id,
            company=company,
            role=role,
            session_minutes=session_minutes,
        )
        return mission
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to select next mission for %s", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to select next mission: {type(exc).__name__}: {exc}") from exc
