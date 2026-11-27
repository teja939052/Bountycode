"""Question solve routes — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import get_current_user
from app.database import get_session
from app.services.code_executor import CodeExecutionEngine
from app.services.ai_coding import evaluate_coding_answer
from app.config import get_settings
from app.models.question import CuratedQuestion
from app.repositories.assessments import CodingSubmission, CodingSubmissionRepository

router = APIRouter(prefix="/api/v1/questions/solve", tags=["question-solve"])


class SubmitAnswer(BaseModel):
    question_id: str
    answer: str
    time_taken: int
    confidence: Optional[int] = None


@router.post("/submit")
async def submit_answer(
    question_id: str,
    payload: SubmitAnswer,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Submit code solution for a question."""
    # Fetch question from question store (in-memory canonical content)
    question = question_store.find_one({"id": question_id}, allow_unverified=True)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    code = payload.answer
    language = payload.language if hasattr(payload, 'language') else "python"

    engine = CodeExecutionEngine()
    test_cases = question.get("visible_test_cases", []) + question.get("hidden_test_cases", [])

    passed = 0
    total = len(test_cases)
    for case in test_cases:
        result = await engine.execute_code(code, language, case.get("input", ""), timeout=5)
        if result.get("success"):
            actual = result.get("stdout", "").strip()
            expected = case.get("expected", "").strip()
            if actual == expected:
                passed += 1

    all_passed = total == 0 or passed == total
    xp_gained = 50 if all_passed else max(0, 25 - (total - passed) * 5)

    # Create submission record
    submission = CodingSubmission(
        user_id=user["id"],
        question_id=question_id,
        code=code,
        language=language,
        status="solved" if all_passed else "attempted",
        score=int(xp_gained / 5),
        created_at=datetime.now(timezone.utc),
    )
    session.add(submission)
    await session.commit()

    score_10 = round(passed / total * 10, 1) if total > 0 else 10.0
    result = await pg_record_practice(
        session,
        user["id"],
        "coding",
        score_10,
        {"problem_id": question_id, "language": language,
         "skill_id": "coding.question", "passed": passed, "total": total},
        role=user.get("role") or user.get("target_role") or "sde",
    )
    xp_gained = int((result or {}).get("xp_gained", 0))

    return {
        "all_passed": all_passed,
        "passed_count": passed,
        "total_cases": total,
        "xp_gained": xp_gained,
        "solved": all_passed,
    }


@router.get("/{question_id}/solution")
async def get_question_solution(
    question_id: str,
    hint_level: int = Query(1, ge=1, le=5),
    user=Depends(get_current_user),
):
    """Get progressive hints for a question."""
    async with get_session() as session:
        result = await session.execute(
            select(CuratedQuestion).where(CuratedQuestion.id == question_id)
        )
        question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    hints = question.hints or []
    visible_hints = hints[:hint_level] if hint_level <= len(hints) else hints
    return {
        "question_id": question_id,
        "hint_level": hint_level,
        "total_hints": len(hints),
        "hints": visible_hints,
    }