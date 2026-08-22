from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.data.aptitude_question_bank import (
    get_questions_by_category,
    get_questions_by_difficulty,
    get_random_questions,
    get_question_by_id,
    get_total_count,
    get_categories as bank_categories,
)

router = APIRouter(prefix="/api/v1/aptitude", tags=["aptitude"])


# Request/Response models
class StartAptitudeTest(BaseModel):
    category: str = Field(..., description="Category name")
    difficulty: str = Field("medium", description="Difficulty level: easy/medium/hard")
    question_count: int = Field(5, ge=1, le=50, description="Number of questions")


class SubmitAptitudeAnswer(BaseModel):
    test_id: str = Field(..., description="Test/attempt ID")
    question_index: int = Field(..., ge=0, description="Question index")
    answer: str = Field(..., description="Selected answer option")


class CompleteAptitudeTest(BaseModel):
    test_id: str = Field(..., description="Test/attempt ID")
    time_taken: int = Field(0, ge=0, description="Time taken in seconds")


# Category name mapping
CATEGORY_NAMES = {
    "quantitative": "Quantitative Aptitude",
    "logical": "Logical Reasoning",
    "verbal": "Verbal Ability",
    "technical": "Technical Aptitude",
}


@router.get("/categories")
def get_categories():
    """Get all available aptitude categories."""
    categories = bank_categories()
    return {
        "categories": [
            {
                "id": cat_id,
                "name": CATEGORY_NAMES.get(cat_id, cat_id),
                "description": "",
            }
            for cat_id in categories
        ]
    }


@router.post("/start")
def start_aptitude_test(req: StartAptitudeTest, user=Depends(get_current_user)):
    """Start a new aptitude test with random questions."""
    questions = get_random_questions(req.category, req.question_count)

    if not questions:
        raise HTTPException(status_code=400, detail=f"No questions found for category: {req.category}")

    formatted_questions = [
        {
            "index": i,
            "question": q["question"],
            "options": q["options"],
            "time_limit": 60,
            "companies": q.get("companies", []),
            "difficulty": q["difficulty"],
            "category": q["topic"],
        }
        for i, q in enumerate(questions)
    ]

    return {
        "test_id": f"test_{req.category}_{datetime.now().timestamp()}",
        "category": req.category,
        "questions": formatted_questions,
        "total_questions": len(questions),
        "message": f"Started {req.question_count} questions in {req.category}",
    }


@router.post("/answer")
def submit_aptitude_answer(req: SubmitAptitudeAnswer, user=Depends(get_current_user)):
    """Submit an answer and check if correct."""
    # Get questions by category from the bank
    category = getattr(req, 'category', 'quantitative')
    questions = get_questions_by_category(category)

    if req.question_index < 0 or req.question_index >= len(questions):
        raise HTTPException(status_code=400, detail="Invalid question index")

    q = questions[req.question_index]

    # Check answer - correct_index is 0-based
    correct_idx = q.get("correct_index", 0)
    is_correct = str(req.answer).strip().upper() == str(correct_idx).strip().upper() if isinstance(correct_idx, int) else False

    return {
        "is_correct": is_correct,
        "correct_answer": q.get("correct_answer", str(correct_idx)),
        "explanation": q.get("explanation", ""),
        "question_index": req.question_index,
        "total_answered": 1,
        "question": q.get("question", ""),
        "options": q.get("options", []),
    }


@router.post("/{test_id}/complete")
def complete_aptitude_test(test_id: str, time_taken: int = 0, user=Depends(get_current_user)):
    """Complete an aptitude test and calculate score."""
    return {
        "test_id": test_id,
        "score": 0,
        "total_questions": 0,
        "percentage": 0,
        "time_taken": time_taken,
        "weak_areas": [],
        "strong_areas": [],
        "message": "Test completion - full implementation requires test storage",
    }


@router.get("/history")
def get_aptitude_history(user=Depends(get_current_user)):
    """Get aptitude test history."""
    return {"tests": [], "message": "History - full implementation requires database integration"}


@router.get("/stats")
def get_aptitude_stats(user=Depends(get_current_user)):
    """Get aptitude statistics."""
    return {
        "total_tests": 0,
        "total_questions_attempted": 0,
        "average_score": 0,
        "categories": {},
        "message": "Stats - full implementation requires database integration",
    }


@router.get("/quick-{category}")
def quick_aptitude_category(category: str, user=Depends(get_current_user)):
    """Quick get 3 random questions from a category."""
    questions = get_random_questions(category, 3)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for category: {category}")

    formatted = [
        {
            "index": i,
            "question": q["question"],
            "options": q["options"],
            "correct_answer": q.get("correct_answer", str(q.get("correct_index", 0))),
            "explanation": q.get("explanation", ""),
            "difficulty": q.get("difficulty", "medium"),
            "companies": q.get("companies", []),
        }
        for i, q in enumerate(questions)
    ]

    return {
        "category": category,
        "questions": formatted,
        "total_available": len(get_questions_by_category(category)),
    }