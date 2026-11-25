from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from app.database import get_session
from app.middleware.auth import get_current_user
from app.services import question_store
from app.services.ai_coding import generate_coding_challenge
from app.services.coding_engine import CodingEngine
from app.services.code_executor import CodeExecutionEngine
from app.services.postgres_assessments import PostgresAssessmentService
from app.services.postgres_gamification import record_practice as pg_record_practice
from app.services.question_quality import score_question
from app.services.mastery_engine import record_solve
from app.config import get_settings
from bson import ObjectId
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/coding", tags=["coding"])
settings = get_settings()
code_engine = CodeExecutionEngine()
coding_engine = CodingEngine()

TOPICS = {
    "arrays": "Arrays & Strings",
    "linked-lists": "Linked Lists",
    "trees": "Trees & Graphs",
    "dynamic-programming": "Dynamic Programming",
    "sorting": "Sorting & Searching",
    "hashing": "Hash Maps & Sets",
    "stacks-queues": "Stacks & Queues",
    "recursion": "Recursion & Backtracking",
    "graphs": "Graph Algorithms",
    "system-design": "System Design Coding",
}

COMPANIES = ["google", "amazon", "meta", "microsoft", "tcs", "infosys", "wipro", "uber"]


class StartCodingChallenge(BaseModel):
    difficulty: str = "medium"
    topic: str = "arrays"
    language: str = "python"
    company: str = ""
    role: str = "SDE"


class SubmitCodingAnswer(BaseModel):
    challenge_id: str
    code: str
    time_taken: int = 0


class GetHintRequest(BaseModel):
    challenge_id: str
    hint_level: int = 1


class InterviewerReviewRequest(BaseModel):
    challenge_id: str
    code: str
    language: str = "python"


@router.get("/topics")
async def get_topics():
    return {
        "topics": [
            {"id": key, "name": name}
            for key, name in TOPICS.items()
        ],
        "companies": COMPANIES,
    }


@router.post("/start")
async def start_coding_challenge(
    req: StartCodingChallenge,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    user = await check_and_reset_monthly_usage(user)

    assessment_service = PostgresAssessmentService(session)

    challenge_doc = {
        "user_id": user["id"],
        "difficulty": req.difficulty,
        "topic": req.topic,
        "language": req.language,
        "company": req.company,
        "role": req.role,
        "user_code": "",
        "status": "in_progress",
        "score": 0,
        "hints_used": 0,
        "created_at": datetime.now(timezone.utc),
    }

    if req.company and req.company.lower() in COMPANIES:
        result_data = await coding_engine.generate_challenge_with_hints(
            company=req.company.lower(),
            role=req.role,
            difficulty=req.difficulty,
        )
        challenge = result_data.get("challenge", {})
        challenge["hints_structured"] = result_data.get("hints", {})
        challenge["solution_approach"] = result_data.get("solution_approach", "")
        challenge["time_limit_seconds"] = result_data.get("time_limit", 2700)
    else:
        challenge = await generate_coding_challenge(req.difficulty, req.topic, req.language)

    challenge_doc["challenge"] = challenge

    # Store submission in PostgreSQL
    submission = await assessment_service.create_coding_submission(
        user_id=UUID(user["id"]),
        question_id="pending",  # Will be updated with actual ID
        code="",
        language=req.language,
        idempotency_key=None,
    )
    submission_id = str(submission.id)

    # Store challenge content in execution_result (internal, not returned in API)
    execution_result = {
        "challenge": challenge,
        "status": "in_progress",
    }
    await assessment_service.submission_repo.update_result(
        submission.id, "in_progress", execution_result, None
    )

    return {
        "challenge_id": submission_id,
        "title": challenge.get("title", ""),
        "description": challenge.get("description", ""),
        "examples": challenge.get("examples", []),
        "constraints": challenge.get("constraints", []),
        "hints": challenge.get("hints", []),
        "time_limit": challenge.get("time_limit_seconds", 1800),
        "difficulty": req.difficulty,
        "topic": req.topic,
        "company": req.company,
        "solution_approach": challenge.get("solution_approach", ""),
    }


@router.post("/submit")
async def submit_coding_answer(
    req: SubmitCodingAnswer,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    assessment_service = PostgresAssessmentService(session)

    try:
        submission = await assessment_service.get_coding_submission(UUID(req.challenge_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not submission:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if str(submission.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Get test cases from internal execution_result (not returned in API)
    execution_result = submission.execution_result or {}
    challenge_content = execution_result.get("challenge", {})
    test_cases = challenge_content.get("test_cases", [])

    test_results = None
    score = 0
    if test_cases and req.code.strip():
        try:
            test_results = await code_engine.execute_against_test_cases(
                req.code, submission.language, test_cases,
                function_name=challenge_content.get("function_name", "") or "",
            )
            score = test_results.get("score", 0)
        except Exception:
            test_results = None

    interviewer_eval = None
    if req.code.strip() and challenge_content.get("company"):
        try:
            problem_desc = f"{challenge_content.get('title', '')}\\n{challenge_content.get('description', '')}"
            interviewer_eval = await coding_engine.evaluate_as_interviewer(
                req.code, submission.language, problem_desc,
            )
        except Exception:
            interviewer_eval = None

    status = "completed" if score >= 80 else "submitted"

    # Update submission with code, score, and execution results
    await assessment_service.update_submission_result(
        submission.id, status, execution_result, score
    )

    # Store individual test case results
    if test_results:
        test_case_results = []
        for tc in test_results.get("test_case_results", []):
            test_case_results.append({
                "test_case_id": tc.get("test_case_id", ""),
                "passed": tc.get("passed", False),
                "execution_time_ms": tc.get("execution_time_ms", 0),
            })
        await assessment_service.store_execution_results(submission.id, test_case_results)

    # Score question quality and record mastery
    question = None
    for q in question_store._questions:
        if str(q.get("id", "")) == req.challenge_id:
            question = dict(q)
            break

    quality_tier = "unknown"
    question_quality_score = 0
    if question:
        quality_result = score_question(question)
        question_quality_score = quality_result["score"]
        quality_tier = quality_result["quality_tier"]

    gamification_result = await pg_record_practice(session, user["id"], "coding", score, role=user.get("role") or user.get("target_role") or "sde")

    mastery_result = None
    if question:
        mastery_result = await record_solve(
            topic=str(question.get("topic", "")),
            sub_topic=str(question.get("sub_topic", "")),
            question_id=req.challenge_id,
            question_type=str(question.get("type", "coding")).lower(),
            difficulty=str(question.get("difficulty", "medium")).lower(),
            is_correct=score >= 80,
            trust_status=str(question.get("trust_status", "unverified")).lower(),
        )

    return {
        "status": status,
        "challenge_id": req.challenge_id,
        "test_results": test_results,
        "score": score,
        "interviewer_eval": interviewer_eval,
        "xp_gained": gamification_result.get("xp_gained", 0),
        "level": gamification_result.get("level", 1),
        "new_badges": gamification_result.get("new_badges", []),
        "streak": gamification_result.get("new_streak", 0),
    }


@router.post("/hint")
async def get_hint(
    req: GetHintRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    assessment_service = PostgresAssessmentService(session)
    try:
        submission = await assessment_service.get_coding_submission(UUID(req.challenge_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not submission:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if str(submission.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    execution_result = submission.execution_result or {}
    challenge_content = execution_result.get("challenge", {})
    problem_desc = f"{challenge_content.get('title', '')}\\n{challenge_content.get('description', '')}"
    current_code = submission.code or ""

    level = max(1, min(3, req.hint_level))

    hints_structured = challenge_content.get("hints_structured", {})
    if hints_structured and f"level_{level}" in hints_structured:
        hint_text = hints_structured[f"level_{level}"]
    else:
        hint_result = await coding_engine.get_hint(problem_desc, current_code, level)
        hint_text = hint_result.get("hint", "Try thinking about the approach differently.")

    # Update hints_used in execution_result
    execution_result["hints_used"] = execution_result.get("hints_used", 0) + 1
    await assessment_service.submission_repo.update_result(
        submission.id, submission.status, execution_result, submission.score
    )

    return {
        "hint": hint_text,
        "level": level,
        "next_level_available": level < 3,
        "hints_used": execution_result["hints_used"],
    }


@router.post("/interviewer-review")
async def interviewer_review(
    req: InterviewerReviewRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    assessment_service = PostgresAssessmentService(session)
    try:
        submission = await assessment_service.get_coding_submission(UUID(req.challenge_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not submission:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if str(submission.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    execution_result = submission.execution_result or {}
    challenge_content = execution_result.get("challenge", {})
    problem_desc = f"{challenge_content.get('title', '')}\\n{challenge_content.get('description', '')}"

    eval_result = await coding_engine.evaluate_as_interviewer(
        req.code, req.language, problem_desc,
    )

    return eval_result


@router.get("/{challenge_id}/solution")
async def get_solution(
    challenge_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    assessment_service = PostgresAssessmentService(session)
    try:
        submission = await assessment_service.get_coding_submission(UUID(challenge_id))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not submission:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if str(submission.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    execution_result = submission.execution_result or {}
    challenge_data = execution_result.get("challenge", {})

    return {
        "title": challenge_data.get("title", ""),
        "description": challenge_data.get("description", ""),
        "examples": challenge_data.get("examples", []),
        "test_cases": challenge_data.get("test_cases", []),
        "hints": challenge_data.get("hints", []),
        "follow_up": challenge_data.get("follow_up", ""),
        "solution_approach": challenge_data.get("solution_approach", ""),
        "user_code": submission.code,
        "company": challenge_data.get("company", ""),
    }


@router.get("/history")
async def get_coding_history(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    assessment_service = PostgresAssessmentService(session)
    submissions = await assessment_service.submission_repo.list_by_user(UUID(user["id"]), limit=20)

    challenges = []
    for sub in submissions:
        execution_result = sub.execution_result or {}
        challenge_data = execution_result.get("challenge", {})
        challenges.append({
            "id": str(sub.id),
            "title": challenge_data.get("title", ""),
            "difficulty": challenge_data.get("difficulty", ""),
            "topic": sub.question_id,
            "company": challenge_data.get("company", ""),
            "status": sub.status,
            "score": sub.score or 0,
            "hints_used": execution_result.get("hints_used", 0),
            "created_at": sub.submitted_at,
        })

    return {"challenges": challenges}
