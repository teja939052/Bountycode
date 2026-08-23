from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.middleware.auth import get_current_user
from app.services.code_executor import CodeExecutionEngine
from app.services.job_queue import get_job_queue, Job, JobType, JobStatus
from app.services.websocket_manager import get_connection_manager, WSEvents
from app.config import get_settings
from app.services.feature_flags import is_feature_enabled

router = APIRouter(prefix="/api/v1/compiler", tags=["compiler"])
engine = CodeExecutionEngine()
job_queue = get_job_queue()
ws_manager = get_connection_manager()
settings = get_settings()

SUPPORTED_LANGUAGE_IDS = set(engine.SUPPORTED_LANGUAGES.keys())


class ExecuteCodeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=120000)
    language: str = Field(..., min_length=1, max_length=32)
    stdin: Optional[str] = Field(default="", max_length=50000)
    timeout: Optional[int] = Field(default=5, ge=1, le=30)
    async_mode: bool = Field(default=False, description="Run asynchronously via job queue")

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
    async_mode: bool = Field(default=False, description="Run asynchronously via job queue")
    function_name: str = Field(default="", max_length=64, description="Entry function for function-call grading")

    def model_post_init(self, __context) -> None:
        if self.language.lower() not in SUPPORTED_LANGUAGE_IDS:
            raise ValueError(
                f"Language '{self.language}' not supported. "
                f"Valid: {', '.join(sorted(SUPPORTED_LANGUAGE_IDS))}"
            )


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/execute")
async def execute_code(req: ExecuteCodeRequest, user=Depends(get_current_user)):
    # Kill switch: operators can disable code execution instantly (admin, billing, etc.)
    # without a deploy. Set the "compiler" flag disabled to serve this 503.
    if not is_feature_enabled("compiler"):
        raise HTTPException(
            status_code=503,
            detail="Code execution is temporarily unavailable. Your saved work is safe. Please try again shortly.",
        )

    # Always cap the runtime timeout to the configured ceiling so a malicious or
    # malformed request can't pin a worker for minutes.
    max_timeout = settings.SANDBOX_TIMEOUT if not (req.async_mode or settings.DOCKER_SANDBOX_ENABLED) else settings.PISTON_TIMEOUT
    timeout = max(1, min(req.timeout or 5, max_timeout))

    if req.async_mode or settings.DOCKER_SANDBOX_ENABLED:
        # Async execution via job queue
        job = Job(
            type=JobType.CODE_EXECUTION,
            payload={
                "code": req.code,
                "language": req.language,
                "stdin": req.stdin or "",
                "timeout": timeout,
            },
            user_id=user["id"],
            priority=5,
        )
        job_id = await job_queue.enqueue(job)
        return {"job_id": job_id, "status": "queued", "message": "Execution queued. Connect to WebSocket for real-time updates."}
    else:
        # Synchronous execution (legacy)
        result = await engine.execute_code(
            code=req.code,
            language=req.language,
            stdin=req.stdin or "",
            timeout=timeout,
        )
        return result


@router.post("/execute-test-cases")
async def execute_test_cases(req: ExecuteTestCasesRequest, user=Depends(get_current_user)):
    if not is_feature_enabled("compiler"):
        raise HTTPException(
            status_code=503,
            detail="Code execution is temporarily unavailable. Your saved work is safe. Please try again shortly.",
        )

    if not req.test_cases:
        raise HTTPException(status_code=400, detail="No test cases provided")
    if len(req.test_cases) > 50:
        raise HTTPException(status_code=400, detail="Too many test cases")

    max_timeout = settings.SANDBOX_TIMEOUT if not (req.async_mode or settings.DOCKER_SANDBOX_ENABLED) else settings.PISTON_TIMEOUT
    timeout = max(1, min(req.timeout or 5, max_timeout))

    if req.async_mode or settings.DOCKER_SANDBOX_ENABLED:
        # Async execution via job queue
        job = Job(
            type=JobType.TEST_CASES,
            payload={
                "code": req.code,
                "language": req.language,
                "test_cases": req.test_cases,
                "timeout": timeout,
                "function_name": req.function_name or "",
            },
            user_id=user["id"],
            priority=5,
        )
        job_id = await job_queue.enqueue(job)
        return {"job_id": job_id, "status": "queued", "message": "Test execution queued. Connect to WebSocket for real-time updates."}
    else:
        # Synchronous execution (legacy)
        return await engine.execute_against_test_cases(
            source_code=req.code,
            language=req.language,
            test_cases=req.test_cases,
            function_name=getattr(req, "function_name", "") or "",
        )


@router.get("/job/{job_id}")
async def get_job_status(job_id: str, user=Depends(get_current_user)):
    """Poll for job status (fallback for non-WebSocket clients)."""
    # In a full implementation, this would check Redis or a job status store
    # For now, return a placeholder
    return {"job_id": job_id, "status": "unknown", "message": "Use WebSocket for real-time status"}


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
    if settings.DOCKER_SANDBOX_ENABLED:
        job = Job(
            type=JobType.EXECUTION_TRACE,
            payload={
                "code": req.code,
                "language": req.language,
                "stdin": req.stdin or "",
            },
            user_id=user["id"],
            priority=3,
        )
        job_id = await job_queue.enqueue(job)
        return {"job_id": job_id, "status": "queued", "message": "Trace generation queued."}
    else:
        return await engine.generate_execution_trace(
            code=req.code,
            language=req.language,
            stdin=req.stdin or "",
        )

