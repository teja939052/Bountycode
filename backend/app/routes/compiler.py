from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.services.code_executor import CodeExecutionEngine

router = APIRouter(prefix="/api/compiler", tags=["compiler"])
engine = CodeExecutionEngine()


class ExecuteCodeRequest(BaseModel):
    code: str
    language: str
    stdin: Optional[str] = ""
    timeout: Optional[int] = 5


class ExecuteTestCasesRequest(BaseModel):
    code: str
    language: str
    test_cases: List[dict]
    timeout: Optional[int] = 5


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

    results = []
    all_passed = True
    passed_count = 0

    for idx, case in enumerate(req.test_cases):
        stdin = case.get("input", "")
        expected = case.get("expected", case.get("expected_output", "")).strip()
        is_hidden = case.get("is_hidden", False)

        execution = await engine.execute_code(
            code=req.code,
            language=req.language,
            stdin=stdin,
            timeout=req.timeout or 5,
        )

        if execution["success"]:
            actual = execution["stdout"].strip()
            passed = actual == expected
            if passed:
                passed_count += 1
            else:
                all_passed = False
        else:
            actual = execution.get("error", "Execution failed")
            passed = False
            all_passed = False

        results.append({
            "test_case_index": idx + 1,
            "passed": passed,
            "is_hidden": is_hidden,
            "input": stdin if not is_hidden else "[HIDDEN]",
            "expected": expected if not is_hidden else "[HIDDEN]",
            "actual": actual if not is_hidden else "[HIDDEN]",
            "error": execution.get("error") if not execution["success"] else None,
            "execution_time": execution.get("execution_time", 0),
        })

    total = len(req.test_cases)
    return {
        "success": True,
        "all_passed": all_passed,
        "passed_count": passed_count,
        "total_count": total,
        "score": round(passed_count / total * 100, 1) if total else 0,
        "summary": f"{passed_count}/{total} Test Cases Passed",
        "results": results,
    }


@router.get("/languages")
async def get_supported_languages():
    return {
        "languages": engine.get_supported_languages()
    }


class BoilerplateRequest(BaseModel):
    language: str
    topics: List[str] = []


@router.post("/boilerplate")
async def get_boilerplate(req: BoilerplateRequest):
    """Get starter code boilerplate for a language and problem type."""
    boilerplate = engine.get_problem_boilerplate(req.language, req.topics)
    return {"boilerplate": boilerplate}
