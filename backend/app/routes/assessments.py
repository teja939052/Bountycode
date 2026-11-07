from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from app.services.assessment_engine import AssessmentEngine, engine as assessment_engine

router = APIRouter(prefix="/api/v1/assessments", tags=["assessments"])


def get_engine() -> AssessmentEngine:
    return assessment_engine


class StageAnswerBody(BaseModel):
    session_id: str = Field(..., min_length=4)
    answer: Dict[str, Any] = Field(default_factory=dict)


@router.post("/start/{definition_id}")
async def start_assessment(
    definition_id: str,
    ai_mode: str = Query("prohibited", description="AI mode: prohibited or allowed"),
    engine: AssessmentEngine = Depends(get_engine),
):
    result = engine.create_session(definition_id, ai_mode=ai_mode)
    if result is None:
        raise HTTPException(status_code=404, detail="Assessment definition not found")
    return result


@router.post("/submit/{stage_name}")
async def submit_stage_answer(
    stage_name: str,
    body: StageAnswerBody,
    engine: AssessmentEngine = Depends(get_engine),
):
    result = engine.submit_answer(body.session_id, stage_name, body.answer)
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message") or "Session not found")
    return result


@router.get("/report")
async def get_assessment_report(
    session_id: str = Query(..., min_length=4),
    engine: AssessmentEngine = Depends(get_engine),
):
    report = engine.end_session(session_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if report.get("status") == "assessment not completed":
        raise HTTPException(status_code=400, detail="Assessment not completed yet")
    return report


@router.get("/definitions")
async def list_definitions(engine: AssessmentEngine = Depends(get_engine)):
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
