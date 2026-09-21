from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from app.middleware.auth import get_current_user
from app.data.aptitude_question_bank import (
    get_questions_by_category,
    get_questions_by_difficulty,
    get_random_questions,
    get_question_by_id,
    get_total_count,
    get_categories as bank_categories,
)
from app.services.repair_service import create_repair_mission

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
    answers: Dict[str, Any] = Field(default_factory=dict, description="Question index -> selected answer")
    category: Optional[str] = Field(None, description="Category attempted")
    questions: List[Dict[str, Any]] = Field(default_factory=list, description="Questions served during the test")


class AptitudeAnswerResult(BaseModel):
    question_index: int
    correct: bool
    selected_answer: Any
    correct_answer: Any
    explanation: str = ""


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
async def complete_aptitude_test(test_id: str, req: CompleteAptitudeTest, user=Depends(get_current_user)):
    """Complete an aptitude test, calculate score, and create repair missions for weak areas."""
    answers = req.answers or {}
    questions = req.questions or []
    category = req.category or ""
    
    # If no questions served payload, fall back to a stub response
    if not questions:
        return {
            "test_id": test_id,
            "score": 0,
            "total_questions": 0,
            "percentage": 0,
            "time_taken": req.time_taken,
            "weak_areas": [],
            "strong_areas": [],
            "repair_missions": [],
            "message": "Test completion - questions payload missing",
        }

    # Grade each answer against the served questions
    results: List[AptitudeAnswerResult] = []
    category_stats: Dict[str, Dict[str, int]] = {}
    for idx_str, selected in answers.items():
        try:
            idx = int(idx_str)
        except ValueError:
            continue
        if idx < 0 or idx >= len(questions):
            continue
        q = questions[idx]
        correct_idx = q.get("correct_index")
        correct_answer = q.get("correct_answer", str(correct_idx) if correct_idx is not None else "")
        is_correct = str(selected).strip().upper() == str(correct_idx).strip().upper() if correct_idx is not None else False
        
        results.append({
            "question_index": idx,
            "correct": is_correct,
            "selected_answer": selected,
            "correct_answer": correct_answer,
            "explanation": q.get("explanation", ""),
        })
        
        cat = q.get("category") or category or "general"
        stats = category_stats.setdefault(cat, {"correct": 0, "total": 0})
        stats["total"] += 1
        if is_correct:
            stats["correct"] += 1

    score = sum(1 for r in results if r["correct"])
    total = len(results)
    percentage = round((score / total * 100)) if total else 0
    
    weak_areas = [cat for cat, stats in category_stats.items() if (stats["correct"] / stats["total"] * 100) < 60]
    strong_areas = [cat for cat, stats in category_stats.items() if (stats["correct"] / stats["total"] * 100) >= 80]

    # Create repair missions for weak areas
    repair_missions = []
    for weakness in weak_areas[:3]:
        try:
            mission = await create_repair_mission(user["id"], [weakness], source="aptitude")
            repair_missions.append({
                "skill": weakness,
                "mission_title": mission.title,
                "recommended_lessons": getattr(mission, "recommended_lessons", []),
                "recommended_exercises": getattr(mission, "recommended_exercises", []),
                "recommended_quizzes": getattr(mission, "recommended_quizzes", []),
            })
        except Exception:
            continue

    return {
        "test_id": test_id,
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "time_taken": req.time_taken,
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
        "repair_missions": repair_missions,
        "questions_review": results,
        "message": "Test completed successfully" if total else "No answers recorded",
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