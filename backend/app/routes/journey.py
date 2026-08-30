"""Journey State — the canonical endpoint for the unified journey game layer.

This uses the Journey Engine (``services.journey_engine``) as the single
orchestrator that composes from the canonical systems:

* ``Study Engine`` (``services/study_engine.py``) — daily plan: NEXT + REVIEW + PRACTICE + CHALLENGE
* ``Gamification`` (``services/gamification.py``) — XP, level, coins, streak
* ``Mastery`` (``services/skill_assessment.py``) — per-skill scores
* ``Readiness`` (``services/readiness_engine.py``) — interview + OA readiness
* ``World Registry`` (``content.world_registry``) — world / town / level structure
* ``Company Blueprints`` — target company context

The result is a single ``GET /api/v1/journey/state`` payload that the frontend
renders as the student's current reality with one clear next action.

The Journey Engine sits *above* the Study Engine and adds career context,
company targets, mastery state, SRS due cards, gamification rewards, and
readiness signals.  It does NOT create new engines — it composes existing
canonical systems.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user
from app.services.journey_engine import build_journey_state

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/journey", tags=["journey"])


@router.get("/state", summary="Return the canonical journey state for the user.")
async def journey_state(user=Depends(get_current_user)):
    """Return the canonical JourneyState for the authenticated user.

    This is the single source of truth the frontend uses to render:
      - The student's character position on the world map
      - Today's next action (the answer to "What do I do next?")
      - SRS reviews due
      - Practice tasks
      - Optional challenge
      - Career readiness + company context
      - Priority scoring so the student understands why this action

    The Journey Engine composes from:
      * Study Engine (daily plan: NEXT + REVIEW + PRACTICE + CHALLENGE)
      * Gamification (XP, level, coins, streak)
      * Mastery (per-skill scores)
      * Readiness (interview + OA readiness)
      * Company blueprints (target company context)
      * World Registry (progression graph)

    Result: one canonical state, one next action, no ambiguity.
    """
    user_id = user["id"]
    state = await build_journey_state(user_id)
    return {"success": True, "data": state}