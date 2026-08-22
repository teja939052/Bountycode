from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.data.behavioral_question_bank import (
    BEHAVIORAL_QUESTION_BANK,
    get_questions_by_category,
    get_random_question,
)

router = APIRouter(prefix="/api/v1/behavioral", tags=["behavioral"])


# Request/Response models
class BehavioralQuestionRequest(BaseModel):
    category: str = Field("leadership", description="Behavioral category")
    count: int = Field(1, ge=1, le=10, description="Number of questions")


class BehavioralAnswerRequest(BaseModel):
    question_id: str = Field(..., description="Question ID")
    user_response: str = Field(..., description="User's STAR response summary")


# Route: Get random behavioral question
@router.get("/question")
async def get_behavioral_question(category: str = "leadership", user=Depends(get_current_user)):
    """Get a random behavioral question with STAR framework."""
    question = get_random_question(category)
    if not question:
        raise HTTPException(status_code=404, detail=f"No questions found for category: {category}")

    return {
        "question_id": question["id"],
        "title": question["title"],
        "category": question["category"],
        "sub_category": question.get("sub_category", ""),
        "difficulty": question["difficulty"],
        "companies": question.get("companies", []),
        "star_framework": question.get("star_framework", {}),
        "tips": question.get("tips", []),
        "example_answer": question.get("example_answer", ""),
    }


# Route: Get questions by category
@router.get("/categories")
async def get_behavioral_categories(user=Depends(get_current_user)):
    """Get all behavioral question categories."""
    categories = {
        "leadership": "Leadership & Initiative",
        "teamwork": "Teamwork & Collaboration",
        "growth": "Personal Growth",
        "conflict": "Problem Solving & Conflict",
        "situational": "Situational Judgment",
        "problem_solving": "Problem Solving",
        "amazon_leadership": "Amazon Leadership Principles",
    }
    return {"categories": categories}


# Route: Get questions by category with count
@router.post("/questions")
async def get_behavioral_questions(req: BehavioralQuestionRequest, user=Depends(get_current_user)):
    """Get random behavioral questions by category."""
    questions = []
    for _ in range(req.count):
        question = get_random_question(req.category)
        if question:
            questions.append({
                "question_id": question["id"],
                "title": question["title"],
                "category": question["category"],
                "sub_category": question.get("sub_category", ""),
                "difficulty": question["difficulty"],
                "companies": question.get("companies", []),
                "star_framework": question.get("star_framework", {}),
                "tips": question.get("tips", []),
                "example_answer": question.get("example_answer", ""),
            })
    
    return {
        "category": req.category,
        "questions": questions,
        "total_in_category": len(get_questions_by_category(req.category)),
    }


# Route: Validate/feedback on STAR response (simulated)
@router.post("/feedback")
async def behavioral_feedback(req: BehavioralAnswerRequest, user=Depends(get_current_user)):
    """Provide feedback on a STAR response (simulated evaluation)."""
    # In full implementation, would use AI to evaluate STAR response
    # For now, return structured feedback based on question type
    question = get_random_question(req.question_id.split("-")[0] if "-" in req.question_id else req.question_id)
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Simulated feedback based on question categories
    category = question["category"]
    tips = question.get("tips", [])
    
    return {
        "question_id": question["id"],
        "title": question["title"],
        "feedback": f"Great use of the STAR framework! Focus on: {', '.join(tips[:2]) if tips else 'quantifying results and learning'}.",
        "strengths": "Clear structure, good detail in situation",
        "areas_for_improvement": "Quantify results more specifically",
        "model_answer_guide": question.get("example_answer", ""),
    }