from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.data.hr_question_bank import (
    HR_QUESTIONS,
    get_questions_by_category,
    get_random_question,
)

router = APIRouter(prefix="/api/v1/hr", tags=["hr"])


# Request/Response models
class HRQuestionRequest(BaseModel):
    category: str = Field("hiring", description="HR category")
    count: int = Field(1, ge=1, le=5, description="Number of questions")


class HRAnswerRequest(BaseModel):
    question_id: str = Field(..., description="Question ID")
    user_reflection: str = Field("", description="User's reflection/answer summary")


# Route: Get random HR question
@router.get("/question")
async def get_hr_question(category: str = "hiring", user=Depends(get_current_user)):
    """Get a random HR/people management question."""
    question = get_random_question(category)
    if not question:
        # Try a different category if specified one has none
        for cat in HR_QUESTION_BANK.keys():
            question = get_random_question(cat)
            if question:
                category = cat
                break
    
    if not question:
        raise HTTPException(status_code=404, detail="No HR questions available")
    
    return {
        "question_id": question["id"],
        "question": question["question"],
        "category": question["category"],
        "difficulty": question["difficulty"],
        "companies": question.get("companies", []),
        "ideal_answer": question.get("ideal_answer", ""),
        "red_flags": question.get("red_flags", []),
    }


# Route: Get questions by category with count
@router.post("/questions")
async def get_hr_questions(req: HRQuestionRequest, user=Depends(get_current_user)):
    """Get random HR questions by category."""
    questions = []
    for _ in range(req.count):
        question = get_random_question(req.category)
        if question:
            questions.append({
                "question_id": question["id"],
                "question": question["question"],
                "category": question["category"],
                "difficulty": question["difficulty"],
                "companies": question.get("companies", []),
                "ideal_answer": question.get("ideal_answer", ""),
                "red_flags": question.get("red_flags", []),
            })
    
    return {
        "category": req.category,
        "questions": questions,
        "total_in_category": len(get_questions_by_category(req.category)),
    }


# Route: Get all HR categories
@router.get("/categories")
async def get_hr_categories(user=Depends(get_current_user)):
    """Get all HR question categories."""
    categories = {
        "hiring": "Hiring & Recruitment",
        "performance": "Performance Management",
        "conflict": "Conflict Resolution",
        "development": "Employee Development",
        "policy": "HR Policy & Compliance",
    }
    return {"categories": categories}


# Route: Get feedback on user's reflection
@router.post("/feedback")
async def hr_feedback(req: HRAnswerRequest, user=Depends(get_current_user)):
    """Provide guidance on HR scenario responses."""
    question = get_random_question(req.question_id.split("-")[0] if "-" in req.question_id else req.question_id)
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    category = question["category"]
    
    return {
        "question_id": question["id"],
        "question": question["question"],
        "category": category,
        "guidance": f"Focus on: {question.get('ideal_answer', '')[:200]}..." if question.get("ideal_answer") else "Provide a structured response using the STAR framework where applicable.",
        "red_flags": question.get("red_flags", []),
        "key_points": [
            "Be specific and provide examples",
            "Focus on actions and outcomes",
            "Show alignment with company values",
            "Keep it concise and professional",
        ],
    }