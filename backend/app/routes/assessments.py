from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any

from app.services.assessment_engine import AssessmentEngine, AssessmentSession, AssessmentDefinition

router = APIRouter(prefix="/api/v1/assessments", tags=["assessments"])


def get_engine() -> AssessmentEngine:
    """Dependency injection for the assessment engine."""
    return engine


@router.post("/start/{definition_id}")
async def start_assessment(
    definition_id: str,
    ai_mode: str = Query("prohibited", description="AI mode: prohibited or allowed"),
    engine: AssessmentEngine = Depends(get_engine),
):
    """Start a new assessment session."""
    result = engine.create_session(definition_id, ai_mode=ai_mode)
    if result is None:
        raise HTTPException(status_code=404, detail="Assessment definition not found")
    return result


@router.post("/submit/{stage_name}")
async def submit_stage_answer(
    stage_name: str,
    answer: dict,
    engine: AssessmentEngine = Depends(get_engine),
):
    """Submit an answer for a stage."""
    result = engine.submit_answer("stub_session", stage_name, answer)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to submit stage answer")
    return result


@router.get("/report")
async def get_assessment_report(
    engine: AssessmentEngine = Depends(get_engine),
):
    """Get final evidence report for a completed assessment."""
    # In real app, would look up session by ID from request
    report = engine.get_session_report("stub_session")
    if report.get("status") == "stub":
        raise HTTPException(
            status_code=400, detail="No completed session found - start an assessment first"
        )
    return report


@router.get("/definitions")
async def list_definitions(engine: AssessmentEngine = Depends(get_engine)):
    """List all available assessment definitions."""
    definitions = []
    for def_id, def_obj in engine.definitions.items():
        definitions.append(
            {
                "id": def_obj.id,
                "role": def_obj.role,
                "level": def_obj.level,
                "duration_minutes": def_obj.duration_minutes,
                "competencies": def_obj.competencies,
                "stages_count": len(def_obj.stages),
            }
        )
    return {"definitions": definitions}


@router.get("/definitions/{definition_id}")
async def get_definition(
    definition_id: str,
    engine: AssessmentEngine = Depends(get_engine),
):
    """Get a specific assessment definition."""
    definition = engine.get_definition(definition_id)
    if not definition:
        raise HTTPException(status_code=404, detail="Assessment definition not found")
    return {
        "id": definition.id,
        "role": definition.role,
        "level": definition.level,
        "duration_minutes": definition.duration_minutes,
        "competencies": definition.competencies,
        "stages": [
            {
                "stage": s.get("stage"),
                "type": s.get("type"),
                "points": s.get("points"),
                "questions": s.get("questions"),
                "allowed_ai_mode": s.get("allowed_ai_mode"),
            }
            for s in definition.stages
        ],
        "rubric": definition.rubric,
    }