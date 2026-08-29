"""Quiz & Mock Interview API Routes.

Provides endpoints for:
  - Building quizzes (practice, quiz, mock_interview, speed_run, boss_battle)
  - Submitting answers and getting feedback
  - Getting progressive hints
  - Quiz results and analytics
  - Adaptive learning paths
  - Weak topic recommendations
  - Question statistics
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.services.quiz_service import (
    build_quiz,
    submit_quiz_answer,
    get_hint_for_question,
    build_learning_path,
    build_boss_battle,
    get_weak_topics,
    calculate_quiz_results,
    get_question_stats,
    get_question_by_id,
    get_questions_by_topic,
    get_questions_by_difficulty,
    get_questions_by_company,
    get_all_questions,
)


router = APIRouter(prefix="/api/v1/quiz", tags=["Quiz & Mock Interview"])


# =============================================================
# Pydantic Models
# =============================================================

class QuizRequest(BaseModel):
    mode: str = Field(default="practice", description="practice, quiz, mock_interview, speed_run, boss_battle")
    topics: Optional[List[str]] = Field(default=None)
    difficulty: Optional[str] = Field(default=None)
    company: Optional[str] = Field(default=None)
    num_questions: int = Field(default=5, ge=1, le=50)
    time_limit_seconds: int = Field(default=0)


class AnswerSubmission(BaseModel):
    quiz_id: str
    question_id: str
    user_answer: str
    time_taken_seconds: float
    hints_used: int = 0


class HintRequest(BaseModel):
    question_id: str
    hint_level: int = 1
    hints_already_used: int = 0


class QuizResultsRequest(BaseModel):
    quiz_id: str
    questions: List[dict]
    answers: List[dict]
    total_time_seconds: float


class LearningPathRequest(BaseModel):
    role_id: str = "sde"
    target_level: str = "advanced"  # foundation, core, advanced
    user_weak_topics: Optional[List[str]] = None
    num_questions: int = 10


class BossBattleRequest(BaseModel):
    boss_level: int = 1
    user_level: int = 1


# =============================================================
# Quiz Endpoints
# =============================================================

@router.post("/build")
async def build_quiz_session(req: QuizRequest, user=Depends(get_current_user)):
    """Build a new quiz session."""
    quiz = build_quiz(
        mode=req.mode,
        topics=req.topics,
        difficulty=req.difficulty,
        company=req.company,
        num_questions=req.num_questions,
        time_limit_seconds=req.time_limit_seconds,
        user_level=user.get("level", 1),
    )
    return {"success": True, "quiz": quiz}


@router.post("/answer")
async def submit_answer(submission: AnswerSubmission, user=Depends(get_current_user)):
    """Submit an answer and get feedback + XP."""
    result = submit_quiz_answer(
        quiz_id=submission.quiz_id,
        question_id=submission.question_id,
        user_answer=submission.user_answer,
        time_taken_seconds=submission.time_taken_seconds,
        hints_used=submission.hints_used,
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"success": True, "result": result}


@router.post("/hint")
async def get_hint(req: HintRequest, user=Depends(get_current_user)):
    """Get a progressive hint for a question."""
    result = get_hint_for_question(
        question_id=req.question_id,
        hint_level=req.hint_level,
        hints_already_used=req.hints_already_used,
    )
    if "error" in result and "No more" not in result.get("error", ""):
        raise HTTPException(status_code=404, detail=result.get("error"))
    return {"success": True, **result}


@router.post("/results")
async def quiz_results(req: QuizResultsRequest, user=Depends(get_current_user)):
    """Calculate comprehensive quiz results."""
    results = calculate_quiz_results(
        quiz_id=req.quiz_id,
        questions=req.questions,
        answers=req.answers,
        total_time_seconds=req.total_time_seconds,
    )
    return {"success": True, "results": results}


# =============================================================
# Learning Path & Boss Battle
# =============================================================

@router.post("/learning-path")
async def get_learning_path(req: LearningPathRequest, user=Depends(get_current_user)):
    """Get an adaptive learning path."""
    path = build_learning_path(
        role_id=req.role_id,
        target_level=req.target_level,
        user_weak_topics=req.user_weak_topics,
        num_questions=req.num_questions,
    )
    return {"success": True, "path": path}


@router.post("/boss-battle")
async def start_boss_battle(req: BossBattleRequest, user=Depends(get_current_user)):
    """Start a boss battle with hard questions."""
    battle = build_boss_battle(
        boss_level=req.boss_level,
        user_level=req.user_level,
    )
    return {"success": True, "battle": battle}


# =============================================================
# Statistics & Recommendations
# =============================================================

@router.get("/stats")
async def quiz_stats():
    """Get overall question bank statistics."""
    return {"success": True, "stats": get_question_stats()}


@router.get("/weak-topics")
async def weak_topics(
    attempted: str = Query(default="[]", description="JSON string of attempts"),
    user=Depends(get_current_user),
):
    """Analyze attempts and return weak topics."""
    import json
    try:
        attempts = json.loads(attempted) if attempted else []
    except json.JSONDecodeError:
        attempts = []
    weak = get_weak_topics(attempted_questions=attempts)
    return {"success": True, "weak_topics": weak}


# =============================================================
# Question Browsing
# =============================================================

@router.get("/questions")
async def list_questions(
    topic: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    company: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """Browse questions with filters."""
    if topic:
        questions = get_questions_by_topic(topic)
    elif difficulty:
        questions = get_questions_by_difficulty(difficulty)
    elif company:
        questions = get_questions_by_company(company)
    else:
        questions = get_all_questions()

    total = len(questions)
    paginated = questions[offset:offset + limit]

    # Return summary only
    return {
        "success": True,
        "questions": [
            {
                "id": q.get("id"),
                "title": q.get("title"),
                "topic": q.get("topic"),
                "sub_topic": q.get("sub_topic"),
                "difficulty": q.get("difficulty"),
                "pattern": q.get("pattern"),
                "companies": q.get("companies", []),
                "xp_reward": q.get("xp_reward", 10),
                "has_solution": bool(q.get("solution", {}).get("code")),
            }
            for q in paginated
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/questions/{question_id}")
async def get_question_detail(question_id: str, user=Depends(get_current_user)):
    """Get full question detail with solution and learning content."""
    question = get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return {
        "success": True,
        "question": {
            "id": question.get("id"),
            "title": question.get("title"),
            "topic": question.get("topic"),
            "sub_topic": question.get("sub_topic"),
            "difficulty": question.get("difficulty"),
            "pattern": question.get("pattern"),
            "question": question.get("question"),
            "hints": question.get("hints", []),
            "solution": question.get("solution", {}),
            "explanation": question.get("explanation"),
            "why_this_matters": question.get("why_this_matters"),
            "real_world_use": question.get("real_world_use"),
            "pattern_recognition": question.get("pattern_recognition"),
            "anti_patterns": question.get("anti_patterns"),
            "common_mistakes": question.get("common_mistakes"),
            "test_cases": question.get("test_cases", []),
            "companies": question.get("companies", []),
            "follow_up": question.get("follow_up"),
            "prerequisite_concepts": question.get("prerequisite_concepts", []),
            "related_concepts": question.get("related_concepts", []),
            "similar_problems": question.get("similar_problems", []),
            "xp_reward": question.get("xp_reward", 10),
            "estimated_time": question.get("estimated_time"),
        }
    }
