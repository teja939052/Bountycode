from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.ai import generate_interview_question, evaluate_answer

router = APIRouter(prefix="/api/v1/free", tags=["free-practice"])


@router.post("/quick-interview")
async def quick_interview(
    job_role: str = "Software Engineer",
    user=Depends(get_current_user),
):
    """Free, quick interview practice - no quota consumed. The hook to get users in the door."""
    
    # Generate 3 quick questions
    questions = []
    for i in range(3):
        q = await generate_interview_question(job_role, [])
        questions.append({
            "question": q.get("question", ""),
            "type": q.get("question_type", "behavioral"),
            "tips": q.get("tips", ""),
        })
    
    return {
        "mode": "quick_practice",
        "job_role": job_role,
        "questions": questions,
        "message": "Complete this quick practice! Upgrade to Pro for unlimited sessions.",
        "is_free": True,
    }


@router.post("/quick-evaluate")
async def quick_evaluate(
    question: str,
    answer: str,
    job_role: str = "Software Engineer",
    user=Depends(get_current_user),
):
    """Quick evaluation for free practice - lighter feedback."""
    
    feedback = await evaluate_answer(question, answer, job_role)
    
    return {
        "score": feedback.get("score", 5),
        "quick_feedback": feedback.get("strengths", ["Good effort!"])[0] if feedback.get("strengths") else "Keep practicing!",
        "improvement_tip": feedback.get("improvements", ["Try to be more specific"])[0] if feedback.get("improvements") else "",
        "is_free": True,
        "upgrade_message": "Get detailed feedback, model answers, and unlimited practice with Pro!",
    }
