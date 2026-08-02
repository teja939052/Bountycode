from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.services.code_executor import CodeExecutionEngine

router = APIRouter(prefix="/api/v1/compiler", tags=["compiler"])
engine = CodeExecutionEngine()

SUPPORTED_LANGUAGE_IDS = set(engine.SUPPORTED_LANGUAGES.keys())


class ExecuteCodeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=120000)
    language: str = Field(..., min_length=1, max_length=32)
    stdin: Optional[str] = Field(default="", max_length=50000)
    timeout: Optional[int] = Field(default=5, ge=1, le=30)

    def model_post_init(self, __context) -> None:
        if self.language.lower() not in SUPPORTED_LANGUAGE_IDS:
            raise ValueError(
                f"Language '{self.language}' not supported. "
                f"Valid: {', '.join(sorted(SUPPORTED_LANGUAGE_IDS))}"
            )


class ExecuteTestCasesRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=120000)
    language: str = Field(..., min_length=1, max_length=32)
    test_cases: List[dict] = Field(default_factory=list, max_length=50)
    timeout: Optional[int] = Field(default=5, ge=1, le=30)

    def model_post_init(self, __context) -> None:
        if self.language.lower() not in SUPPORTED_LANGUAGE_IDS:
            raise ValueError(
                f"Language '{self.language}' not supported. "
                f"Valid: {', '.join(sorted(SUPPORTED_LANGUAGE_IDS))}"
            )


@router.post("/execute")
async def execute_code(req: ExecuteCodeRequest, user=Depends(get_current_user)):
    result = await engine.execute_code(
        code=req.code,
        language=req.language,
        stdin=req.stdin or "",
        timeout=req.timeout or 5,
    )
    return result


@router.post("/execute-test-cases")
async def execute_test_cases(req: ExecuteTestCasesRequest, user=Depends(get_current_user)):
    if not req.test_cases:
        raise HTTPException(status_code=400, detail="No test cases provided")
    if len(req.test_cases) > 50:
        raise HTTPException(status_code=400, detail="Too many test cases")
    return await engine.execute_against_test_cases(
        source_code=req.code,
        language=req.language,
        test_cases=req.test_cases,
    )


@router.get("/languages")
async def get_supported_languages():
    return {
        "languages": engine.get_supported_languages()
    }


class BoilerplateRequest(BaseModel):
    language: str = Field(..., min_length=1, max_length=32)
    topics: List[str] = Field(default_factory=list, max_length=10)

    def model_post_init(self, __context) -> None:
        if self.language.lower() not in SUPPORTED_LANGUAGE_IDS:
            raise ValueError(
                f"Language '{self.language}' not supported. "
                f"Valid: {', '.join(sorted(SUPPORTED_LANGUAGE_IDS))}"
            )


@router.post("/boilerplate")
async def get_boilerplate(req: BoilerplateRequest):
    """Get starter code boilerplate for a language and problem type."""
    boilerplate = engine.get_problem_boilerplate(req.language, req.topics)
    return {"boilerplate": boilerplate}


class TraceCodeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=120000)
    language: str = Field(..., min_length=1, max_length=32)
    stdin: Optional[str] = Field(default="", max_length=50000)

    def model_post_init(self, __context) -> None:
        if self.language.lower() not in SUPPORTED_LANGUAGE_IDS:
            raise ValueError(
                f"Language '{self.language}' not supported. "
                f"Valid: {', '.join(sorted(SUPPORTED_LANGUAGE_IDS))}"
            )


@router.post("/trace")
async def trace_code_execution(req: TraceCodeRequest, user=Depends(get_current_user)):
    """Generate step-by-step execution trace for the algorithm visualizer."""
    return await engine.generate_execution_trace(
        code=req.code,
        language=req.language,
        stdin=req.stdin or "",
    )

