"""Questions routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.models.question import CuratedQuestion

router = APIRouter(prefix="/api/v1/questions", tags=["questions"])


@router.get("/browse")
async def browse_questions(
    user=Depends(get_current_user),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    company: Optional[str] = Query(None, description="Filter by company"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
):
    """Browse questions from the question bank."""
    async with get_session() as session:
        query = select(CuratedQuestion)
        if topic:
            query = query.where(CuratedQuestion.topic == topic)
        if difficulty:
            query = query.where(CuratedQuestion.difficulty == difficulty)
        if company:
            query = query.where(CuratedQuestion.company.contains([company]))
        
        count_result = await session.execute(select(func.count()).select_from(CuratedQuestion).where(CuratedQuestion.topic == topic if topic else CuratedQuestion.id.is_not(None)))
        total = count_result.scalar_one() or 0
        
        result = await session.execute(query.offset((page - 1) * limit).limit(limit))
        questions = result.scalars().all()
    
    return {
        "questions": [
            {
                "id": q.id,
                "type": q.type,
                "company": q.company,
                "role": q.role,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "sub_topic": q.sub_topic,
                "question": q.question,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
                "hints": q.hints,
                "solution": q.solution,
                "frequency": q.frequency,
                "source": q.source,
                "submitted_by": q.submitted_by,
                "upvotes": q.upvotes,
                "downvotes": q.downvotes,
                "reported": q.reported,
                "created_at": q.created_at.isoformat() if q.created_at else None,
                "updated_at": q.updated_at.isoformat() if q.updated_at else None,
                "sql_schema": q.sql_schema,
                "test_cases": q.test_cases,
                "trust_status": q.trust_status,
                "is_executable": q.is_executable,
            }
            for q in questions
        ],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/{question_id}")
async def get_question_detail(
    question_id: str,
    user=Depends(get_current_user),
):
    """Get full question detail."""
    async with get_session() as session:
        result = await session.execute(
            select(CuratedQuestion).where(CuratedQuestion.id == question_id)
        )
        question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "id": question.id,
        "type": question.type,
        "company": question.company,
        "role": question.role,
        "difficulty": question.difficulty,
        "topic": question.topic,
        "sub_topic": question.sub_topic,
        "question": question.question,
        "options": question.options,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "hints": question.hints,
        "solution": question.solution,
        "frequency": question.frequency,
        "source": question.source,
        "submitted_by": question.submitted_by,
        "upvotes": question.upvotes,
        "downvotes": question.downvotes,
        "reported": question.reported,
        "created_at": question.created_at.isoformat() if question.created_at else None,
        "updated_at": question.updated_at.isoformat() if question.updated_at else None,
        "sql_schema": question.sql_schema,
        "test_cases": question.test_cases,
        "trust_status": question.trust_status,
        "is_executable": question.is_executable,
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


@router.get("/{question_id}/solution/progressive")
async def get_progressive_hints(
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


@router.get("/filters")
async def get_question_filters(user=Depends(get_current_user)):
    """Get available question filters."""
    return {
        "companies": [],
        "topics": [],
        "difficulties": ["beginner", "intermediate", "advanced", "expert"],
        "types": ["mcq", "coding", "short_answer"],
    }


@router.get("/{question_id}/solved")
async def check_if_solved(
    question_id: str,
    user=Depends(get_current_user),
):
    """Check if user has solved this question."""
    from app.repositories.assessments import SolvedProblemRepository
    async with get_session() as session:
        repo = SolvedProblemRepository(session)
        solved = await repo.get_by_user_and_question(user["id"], question_id)
    return {"solved": bool(solved)}