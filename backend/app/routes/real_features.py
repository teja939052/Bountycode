from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.services.real_ats import RealATSScanner
from app.services.code_executor import CodeExecutionEngine as CodeExecutor
from app.services.smart_prompts import SmartPrompts
from app.services.ai import chat_completion, parse_json

router = APIRouter(prefix="/api/v1/real", tags=["real-features"])

# Initialize services
ats_scanner = RealATSScanner()
code_executor = CodeExecutor()


# ============================================
# REAL ATS SCANNER (No auth required for free tier)
# ============================================

class ATSScanRequest(BaseModel):
    resume_text: str
    job_description: str = ""


@router.post("/ats/scan")
async def real_ats_scan(req: ATSScanRequest):
    """
    Real ATS scan that simulates how actual ATS software parses resumes.
    No auth required - this is the marketing hook.
    """
    return ats_scanner.full_scan(req.resume_text, req.job_description or None)


# ============================================
# CODE EXECUTION
# ============================================

class ExecuteCodeRequest(BaseModel):
    code: str
    language: str
    stdin: str = ""


class RunTestCasesRequest(BaseModel):
    code: str
    language: str
    test_cases: List[dict]


@router.post("/code/execute")
async def execute_code(req: ExecuteCodeRequest, user=Depends(get_current_user)):
    """Execute code and return output."""
    return await code_executor.execute_code(req.code, req.language, req.stdin)


@router.post("/code/run-tests")
async def run_test_cases(req: RunTestCasesRequest, user=Depends(get_current_user)):
    """Run code against multiple test cases."""
    return await code_executor.run_test_cases(req.code, req.language, req.test_cases)


@router.get("/code/boilerplate/{language}")
async def get_boilerplate(language: str, problem_type: str = "general"):
    """Get starter code boilerplate."""
    return {"boilerplate": code_executor.get_boilerplate(language, problem_type)}


# ============================================
# SMART INTERVIEW (Using improved prompts)
# ============================================

class InterviewRequest(BaseModel):
    job_role: str
    company: str
    difficulty: str = "medium"
    history: List[dict] = []


@router.post("/interview/question")
async def get_smart_question(req: InterviewRequest, user=Depends(get_current_user)):
    """Get interview question with company-context-aware prompt."""
    prompt = SmartPrompts.get_interview_question_prompt(
        req.job_role, req.company, req.difficulty, req.history
    )

    messages = [
        {"role": "system", "content": prompt["system"]},
        {"role": "user", "content": prompt["user"]},
    ]

    response = await chat_completion(messages)
    return parse_json(response)


class EvaluateAnswerRequest(BaseModel):
    question: str
    answer: str
    job_role: str
    company: str
    question_type: str = "technical"


@router.post("/interview/evaluate")
async def evaluate_answer_smart(req: EvaluateAnswerRequest, user=Depends(get_current_user)):
    """Evaluate answer with context-aware feedback."""
    prompt = SmartPrompts.get_answer_evaluation_prompt(
        req.question, req.answer, req.job_role, req.company, req.question_type
    )

    messages = [
        {"role": "system", "content": prompt["system"]},
        {"role": "user", "content": prompt["user"]},
    ]

    response = await chat_completion(messages)
    return parse_json(response)


# ============================================
# SMART RESUME (Using improved prompts)
# ============================================

class ImproveBulletRequest(BaseModel):
    bullet: str
    job_role: str = ""
    company: str = ""
    industry: str = "tech"


@router.post("/resume/improve-bullet")
async def improve_bullet_smart(req: ImproveBulletRequest, user=Depends(get_current_user)):
    """Improve bullet with company-context-aware prompt."""
    prompt = SmartPrompts.get_resume_improvement_prompt(
        req.bullet, req.job_role, req.company, req.industry
    )

    messages = [
        {"role": "system", "content": prompt["system"]},
        {"role": "user", "content": prompt["user"]},
    ]

    response = await chat_completion(messages)
    return parse_json(response)


class STARRequest(BaseModel):
    question: str
    company: str
    role: str


@router.post("/behavioral/star-template")
async def get_star_template_smart(req: STARRequest, user=Depends(get_current_user)):
    """Get STAR template with company-context-aware prompt."""
    prompt = SmartPrompts.get_star_answer_prompt(req.question, req.company, req.role)

    messages = [
        {"role": "system", "content": prompt["system"]},
        {"role": "user", "content": prompt["user"]},
    ]

    response = await chat_completion(messages)
    return parse_json(response)


# ============================================
# SYSTEM DESIGN (Using improved prompts)
# ============================================

class SystemDesignRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    company: str = "google"


@router.post("/system-design/question")
async def get_system_design_question_smart(req: SystemDesignRequest, user=Depends(get_current_user)):
    """Get system design question with company-context-aware prompt."""
    prompt = SmartPrompts.get_system_design_prompt(req.topic, req.difficulty, req.company)

    messages = [
        {"role": "system", "content": prompt["system"]},
        {"role": "user", "content": prompt["user"]},
    ]

    response = await chat_completion(messages)
    return parse_json(response)
