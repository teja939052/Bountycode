"""Lesson Player routes — unified teaching loop for coding, behavioral, system_design,
aptitude, reasoning, verbal, sql, and cs_core.

Routes (all under /api/v1/lesson-player, auth required):
  POST /start                          → create session, return step 0
  POST /session/{session_id}/submit    → grade response, diagnose, advance
  GET  /session/{session_id}           → session state
  POST /session/{session_id}/hint      → get hint / AI tutor guidance
  POST /session/{session_id}/reteach   → get reteach plan if diagnosis fired
  POST /session/{session_id}/complete  → finalize, award rewards
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.services.lesson_orchestrator import get_orchestrator, LessonOrchestrator, STEP_NAMES
from app.data.worlds_data import WORLD_REGISTRY

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/lesson-player", tags=["lesson-player"])


# ───────────────────────────────────────────────────────────────
# Request models
# ───────────────────────────────────────────────────────────────

class StartRequest(BaseModel):
    domain: str = Field(..., description="coding | behavioral | system_design | aptitude | reasoning | verbal | sql | cs_core")
    world_id: Optional[str] = Field(None, description="For coding: world id")
    level_id: Optional[str] = Field(None, description="For coding: level id")
    concept: Optional[str] = Field(None, description="Lesson slug / concept for non-coding domains")
    company: Optional[str] = Field(None, description="For behavioral/system_design")
    role: Optional[str] = Field(None, description="Target role")
    topic: Optional[str] = Field(None, description="Topic filter")
    difficulty: Optional[str] = Field(None, description="easy | medium | hard")
    mastery_threshold: Optional[int] = Field(None, ge=0, le=100)


class SubmitRequest(BaseModel):
    step_index: Optional[int] = Field(None, ge=0)
    answer: Optional[str] = Field(None, description="Text answer (behavioral/retrieval)")
    code: Optional[str] = Field(None, description="Code answer (coding/build/debug)")
    language: Optional[str] = Field("python", description="Programming language")
    selected_option: Optional[str] = Field(None, description="MCQ option id")
    selected_component: Optional[str] = Field(None, description="STAR component label")
    selected_issue: Optional[str] = Field(None, description="Break step issue")
    selected_failure: Optional[str] = Field(None, description="System design failure point")
    fixes_applied: Optional[List[str]] = Field(None, description="Debug fixes applied")
    matches: Optional[Dict[str, str]] = Field(None, description="Manipulate matches")
    improved_answer: Optional[str] = Field(None, description="Improved answer for debug")
    diagram_description: Optional[str] = Field(None, description="System design diagram")
    question: Optional[str] = Field(None, description="Question text for system_design")
    time_spent_seconds: int = Field(0, ge=0)


class HintRequest(BaseModel):
    step_index: Optional[int] = Field(None, ge=0)


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def _resolve_coding_context(req: StartRequest) -> tuple[Any, str, str]:
    """Resolve world level for coding domain. Returns (level, world_id, level_id)."""
    world_id = req.world_id or "foundations"
    level_id = req.level_id or "level-1"

    world = WORLD_REGISTRY.get(world_id)
    if world is None:
        raise HTTPException(status_code=404, detail=f"Unknown world: {world_id}")

    level = None
    for town in world.towns:
        for lvl in town.levels:
            if lvl.id == level_id:
                level = lvl
                break
        if level is not None:
            break

    if level is None:
        raise HTTPException(status_code=404, detail=f"Unknown level: {level_id}")

    return level, world_id, level_id


def _build_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Strip internal session state from response for frontend."""
    session = response.pop("session", {})
    return {
        **response,
        "session_id": response.get("session_id"),
        "current_step": response.get("current_step", 0),
        "total_steps": response.get("total_steps", len(STEP_NAMES)),
    }


# ───────────────────────────────────────────────────────────────
# Routes
# ───────────────────────────────────────────────────────────────

@router.post("/start")
async def start_lesson(req: StartRequest, user=Depends(get_current_user)):
    """Create a new lesson session and return the first step."""
    orchestrator: LessonOrchestrator = get_orchestrator()
    domain = req.domain.strip().lower()

    level_or_context = None
    company = req.company or ""
    role = req.role or user.get("target_role") or user.get("role") or "sde"
    mastery_threshold = req.mastery_threshold or 80

    if domain == "coding":
        level_or_context, _, _ = _resolve_coding_context(req)
    elif domain in ("behavioral", "system_design", "aptitude", "reasoning", "verbal", "sql", "cs_core"):
        level_or_context = _make_context(req)
        concept = req.concept or req.topic or ""
        if concept:
            try:
                object.__setattr__(level_or_context, "concept", concept)
            except Exception:
                pass
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported domain: {req.domain}")

    try:
        result = await orchestrator.start(
            user_id=user["id"],
            domain=domain,
            level_or_context=level_or_context,
            company=company,
            role=role,
            mastery_threshold=mastery_threshold,
        )
    except Exception as exc:
        logger.exception("lesson_player.start failed: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to start lesson") from exc

    return _build_response(result)


@router.post("/session/{session_id}/submit")
async def submit_step(session_id: str, req: SubmitRequest, user=Depends(get_current_user)):
    """Submit a response for the current step. Returns grade + next step or reteach."""
    orchestrator: LessonOrchestrator = get_orchestrator()

    response: Dict[str, Any] = {}
    if req.answer is not None:
        response["answer"] = req.answer
    if req.code is not None:
        response["code"] = req.code
    if req.language:
        response["language"] = req.language
    if req.selected_option is not None:
        response["selected_option"] = req.selected_option
    if req.selected_component is not None:
        response["selected_component"] = req.selected_component
    if req.selected_issue is not None:
        response["selected_issue"] = req.selected_issue
    if req.selected_failure is not None:
        response["selected_failure"] = req.selected_failure
    if req.fixes_applied is not None:
        response["fixes_applied"] = req.fixes_applied
    if req.matches is not None:
        response["matches"] = req.matches
    if req.improved_answer is not None:
        response["improved_answer"] = req.improved_answer
    if req.diagram_description is not None:
        response["diagram_description"] = req.diagram_description
    if req.question is not None:
        response["question"] = req.question

    step_index = req.step_index if req.step_index is not None else 0

    try:
        result = await orchestrator.submit_step(
            session_id=session_id,
            step_index=step_index,
            response=response,
            time_spent_seconds=req.time_spent_seconds,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("lesson_player.submit failed: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to submit step") from exc

    return _build_response(result)


@router.get("/session/{session_id}")
async def get_session(session_id: str, user=Depends(get_current_user)):
    """Get the current state of a lesson session."""
    orchestrator: LessonOrchestrator = get_orchestrator()
    session = await orchestrator.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/session/{session_id}/hint")
async def request_hint(session_id: str, req: HintRequest, user=Depends(get_current_user)):
    """Get a hint for the current step, with optional AI tutor guidance."""
    orchestrator: LessonOrchestrator = get_orchestrator()
    step_index = req.step_index if req.step_index is not None else 0

    try:
        result = await orchestrator.request_hint(session_id, step_index)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("lesson_player.hint failed: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to get hint") from exc

    return result


@router.post("/session/{session_id}/reteach")
async def get_reteach_plan(session_id: str, user=Depends(get_current_user)):
    """Get the reteach plan if a misconception was diagnosed."""
    orchestrator: LessonOrchestrator = get_orchestrator()
    try:
        result = await orchestrator.get_reteach_plan(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("lesson_player.reteach failed: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to get reteach plan") from exc

    return result


@router.post("/session/{session_id}/complete")
async def complete_session(session_id: str, user=Depends(get_current_user)):
    """Manually complete a session (normally auto-completed on mastery)."""
    orchestrator: LessonOrchestrator = get_orchestrator()
    session = orchestrator._sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session.completed = True
    session.updated_at = datetime.now(timezone.utc).isoformat()
    orchestrator.cleanup(session_id)

    return {
        "session_id": session_id,
        "completed": True,
        "mastery_unlocked": session.mastery_unlocked,
        "message": "Session completed.",
    }


# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────

def _make_context(req: StartRequest) -> Any:
    """Create a lightweight context object for non-coding domains."""
    return type("DomainContext", (), {
        "company": req.company or "general",
        "role": req.role or "sde",
        "topic": req.topic or "",
        "concept": req.concept or req.topic or "",
        "difficulty": req.difficulty or "medium",
        "domain": req.domain,
    })()
