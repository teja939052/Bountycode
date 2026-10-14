"""
Lesson routes — serve any foundation lesson generically by slug.

GET  /api/v1/lesson/{slug}                  — full lesson content
GET  /api/v1/lesson/{slug}/step/{step_key} — individual step
POST /api/v1/lesson/{slug}/run             — execute code (explore step)
POST /api/v1/lesson/{slug}/build           — submit build step code
POST /api/v1/lesson/{slug}/transfer        — submit transfer challenge
POST /api/v1/lesson/{slug}/predict         — check prediction answer
POST /api/v1/lesson/{slug}/explain         — grade explaining-stage answer
POST /api/v1/lesson/{slug}/break           — grade breaking-stage diagnosis + fix
POST /api/v1/lesson/{slug}/assess          — grade assessment
POST /api/v1/lesson/{slug}/complete        — record completion + rewards
GET  /api/v1/lesson/plan/{concept_id}      — adaptive lesson plan
GET  /api/v1/lesson/next-action            — next best learning action
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


class ExplainRequest(BaseModel):
    answer: str = Field(..., max_length=4000)


class BreakRequest(BaseModel):
    diagnosis: str = Field(..., max_length=100)
    fix: str = Field(..., max_length=400)


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


# NOTE: static paths must be declared BEFORE "/{slug}" or FastAPI matches the
# literal segment as a slug and the handler is never reached.
@router.get("/curriculum")
async def get_curriculum(user=Depends(get_current_user)):
    """Return the placement curriculum structure: worlds + lessons."""
    from app.content.curriculum.canonical_worlds import get_all_worlds, get_all_levels, LEVEL_TEMPLATES
    from app.content.curriculum.registry import LESSON_REGISTRY

    WORLD_ID_ALIASES = {
        "code_foundations": "coding_foundations",
        "aptitude_world": "aptitude_gauntlet",
        "communication_world": "interview_arena",
        "cs_world": "cs_core",
        "company_world": "company_quests",
        "placement_world": "placement_readiness",
    }

    def _normalize_world_id(raw: str | None) -> str:
        if not raw:
            return ""
        return WORLD_ID_ALIASES.get(raw, raw)

    worlds = []
    for w in get_all_worlds():
        worlds.append({
            "world_id": w["world_id"],
            "name": w["name"],
            "icon": w["icon"],
            "subtitle": w["subtitle"],
            "description": w["description"],
            "color": w["color"],
            "levels": w["levels"],
        })

    lessons: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()
    for slug, lesson in LESSON_REGISTRY.items():
        wp = lesson.get("world_progression") or {}
        raw_world_id = wp.get("world_id") or _guess_world_id_from_slug(slug, lesson)
        world_id = _normalize_world_id(raw_world_id)
        entry = {
            "slug": slug,
            "lesson_id": lesson.get("lesson_id", slug),
            "title": lesson.get("title", slug),
            "description": lesson.get("description", ""),
            "difficulty": lesson.get("difficulty", "intermediate"),
            "est_minutes": lesson.get("est_minutes", 15),
            "diamonds": lesson.get("world_progression", {}).get("world_node", {}).get("level", 0),
            "world_id": world_id,
            "icon": lesson.get("world_progression", {}).get("world_node", {}).get("icon", ""),
        }
        lessons.append(entry)
        seen_slugs.add(slug)

    # Backfill level-template entries for worlds that still have no mapped lessons.
    for w in get_all_worlds():
        wid = w["world_id"]
        has_any = any(l["world_id"] == wid for l in lessons)
        if has_any:
            continue
        for level in get_all_levels(wid)[:8]:
            lessons.append({
                "slug": f"{wid}::{level['concept']}",
                "lesson_id": level["concept"],
                "title": level["title"],
                "description": level.get("concept", ""),
                "difficulty": level.get("difficulty", "intermediate"),
                "est_minutes": level.get("est_minutes", 15),
                "diamonds": level.get("diamonds", 20),
                "world_id": wid,
                "icon": w.get("icon", ""),
            })

    return {"worlds": worlds, "lessons": lessons, "total_lessons": len(lessons)}


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

    passing_score = step.get("passing_score", 70)
    passed_visible = result.get("score", 0) >= passing_score

    if passed_visible:
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
            result["all_passed"] = hidden_result.get("all_passed", False)
            result["passed"] = result["all_passed"]

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

    passing_score = transfer.get("passing_score", 70)
    passed_visible = result.get("score", 0) >= passing_score

    if passed_visible:
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
            result["all_passed"] = hidden_result.get("all_passed", False)
            result["passed"] = result["all_passed"]

    return result


@router.post("/{slug}/predict")
async def check_prediction(slug: str, req: PredictRequest, user=Depends(get_current_user)):
    return _service(slug).check_prediction(req.answer)


@router.post("/{slug}/explain")
async def check_explain(slug: str, req: ExplainRequest, user=Depends(get_current_user)):
    return _service(slug).check_explain(req.answer)


@router.post("/{slug}/break")
async def check_break(slug: str, req: BreakRequest, user=Depends(get_current_user)):
    return _service(slug).check_break(diagnosis=req.diagnosis, fix=req.fix)


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
        role=user.get("role") or user.get("target_role") or "sde",
    )
    # Server-authoritative completion: derive from actual evidence, not client-provided score.
    try:
        lesson = svc.get_lesson()
        mastery_threshold = lesson.get("assessment", {}).get("mastery_threshold", 70)
        result["lesson_completed"] = (result.get("score", 0) >= mastery_threshold) or result.get("mastery_unlocked", False)
    except Exception:
        result["lesson_completed"] = result.get("mastery_unlocked", False)
    return result


def _guess_world_id_from_slug(slug: str, lesson: dict[str, Any]) -> str:
    title = lesson.get("title", "").lower()
    text = f"{slug} {title} {lesson.get('description', '')}".lower()
    if any(k in text for k in ["percentage", "percent", "quant", "reason", "verbal", "aptitude", "blood relation", "coding-decoding"]):
        return "aptitude_gauntlet"
    if any(k in text for k in ["interview", "hr ", "behavioral", "tell me about"]):
        return "interview_arena"
    if any(k in text for k in ["dbms", "sql", "os ", "operating system", "computer network", "oop", "object oriented"]):
        return "cs_core"
    if any(k in text for k in ["company", "tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini"]):
        return "company_quests"
    if any(k in text for k in ["diagnostic", "baseline", "readiness", "campaign", "placement"]):
        return "placement_readiness"
    return "coding_foundations"
