"""
Lesson routes — serve any foundation lesson generically by slug.

GET  /api/v1/lesson/{slug}                  — full lesson content
GET  /api/v1/lesson/{slug}/step/{step_key} — individual step
POST /api/v1/lesson/{slug}/run             — execute code (explore step)
POST /api/v1/lesson/{slug}/build           — submit build step code
POST /api/v1/lesson/{slug}/transfer        — submit transfer challenge
POST /api/v1/lesson/{slug}/predict         — check prediction answer
POST /api/v1/lesson/{slug}/assess          — grade assessment
POST /api/v1/lesson/{slug}/complete        — record completion + rewards
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.middleware.auth import get_current_user
from app.services.lesson import LessonService
from app.content.curriculum.registry import get_lesson_dict

router = APIRouter(
    prefix="/api/v1/lesson",
    tags=["lesson", "vertical-slice"],
)


class RunCodeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=120000)
    language: str = Field(default="python", min_length=2, max_length=32)
    stdin: Optional[str] = Field(default="")


class BuildSubmitRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=120000)
    function_name: str = Field(..., min_length=1, max_length=64)
    language: str = Field(default="python", min_length=2, max_length=32)
    step_index: Optional[int] = None


class PredictRequest(BaseModel):
    answer: str


class AssessRequest(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)
    time_spent_seconds: int = Field(default=0, ge=0)


class CompleteRequest(BaseModel):
    score: float = Field(..., ge=0, le=100)
    time_spent_seconds: int = Field(default=0, ge=0)


def _service(slug: str) -> LessonService:
    lesson = get_lesson_dict(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {slug}")
    return LessonService(lesson)


@router.get("/{slug}", response_model=None)
async def get_lesson(slug: str, user=Depends(get_current_user)):
    return _service(slug).get_lesson()


@router.get("/{slug}/step/{step_key:path}")
async def get_step(slug: str, step_key: str, user=Depends(get_current_user)):
    step = _service(slug).get_step(step_key)
    if step is None:
        raise HTTPException(status_code=404, detail=f"Step not found: {step_key}")
    return {"step_key": step_key, "step": step}


@router.post("/{slug}/run")
async def run_code(slug: str, req: RunCodeRequest, user=Depends(get_current_user)):
    return await _service(slug).run_code(
        code=req.code,
        language=req.language,
        stdin=req.stdin or "",
    )


@router.post("/{slug}/build")
async def submit_build(slug: str, req: BuildSubmitRequest, user=Depends(get_current_user)):
    svc = _service(slug)
    lesson = svc.get_lesson()
    steps = lesson["guided_build"]["steps"]

    if req.step_index is not None:
        step = steps[req.step_index]
    else:
        step = steps[-1]

    result = await svc.submit_build_step(
        user_code=req.code,
        function_name=req.function_name,
        test_cases=step.get("test_cases", []),
        language=req.language,
    )

    if result.get("all_passed"):
        hidden_count = step.get("hidden_tests", 0) or len(step.get("hidden_test_cases", []))
        if hidden_count > 0:
            hidden_result = await svc.submit_build_step(
                user_code=req.code,
                function_name=req.function_name,
                test_cases=step.get("hidden_test_cases", []),
                language=req.language,
            )
            result["hidden_pass_rate"] = hidden_result.get("score", 0)
            result["hidden_results"] = hidden_result.get("results", [])

    return result


@router.post("/{slug}/transfer")
async def submit_transfer(slug: str, req: BuildSubmitRequest, user=Depends(get_current_user)):
    svc = _service(slug)
    lesson = svc.get_lesson()
    transfer = lesson["transfer_challenge"]

    result = await svc.submit_build_step(
        user_code=req.code,
        function_name=req.function_name,
        test_cases=transfer.get("test_cases", []),
        language=req.language,
    )

    if result.get("all_passed"):
        hidden_count = transfer.get("hidden_tests", 0) or len(transfer.get("hidden_test_cases", []))
        if hidden_count > 0:
            hidden_result = await svc.submit_build_step(
                user_code=req.code,
                function_name=req.function_name,
                test_cases=transfer.get("hidden_test_cases", []),
                language=req.language,
            )
            result["hidden_pass_rate"] = hidden_result.get("score", 0)
            result["hidden_results"] = hidden_result.get("results", [])

    return result


@router.post("/{slug}/predict")
async def check_prediction(slug: str, req: PredictRequest, user=Depends(get_current_user)):
    return _service(slug).check_prediction(req.answer)


@router.post("/{slug}/assess")
async def check_assessment(slug: str, req: AssessRequest, user=Depends(get_current_user)):
    return _service(slug).check_assessment(req.answers)


@router.post("/{slug}/complete")
async def complete_lesson(slug: str, req: CompleteRequest, user=Depends(get_current_user)):
    svc = _service(slug)
    result = await svc.complete_lesson(
        user_id=user["id"],
        score=req.score,
        time_spent_seconds=req.time_spent_seconds,
    )
    result["lesson_completed"] = req.score >= svc.get_lesson()["assessment"]["mastery_threshold"]
    return result
