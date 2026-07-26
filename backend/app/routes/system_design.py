from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection, system_design_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_system_design_question, evaluate_system_design_answer
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/system-design", tags=["system-design"])
settings = get_settings()


class StartSystemDesign(BaseModel):
    difficulty: str = "medium"
    topic: str = ""


class SubmitSystemDesignAnswer(BaseModel):
    session_id: str
    question: str
    answer: str
    diagram_description: str = ""


@router.post("/start")
async def start_system_design(req: StartSystemDesign, user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)

    if not can_use_feature(user, "interview"):
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limit reached ({settings.FREE_TIER_INTERVIEW_LIMIT} interviews/month). Upgrade to Pro for unlimited.",
        )

    question_data = await generate_system_design_question(req.difficulty, req.topic)

    session_doc = {
        "user_id": user["id"],
        "type": "system_design",
        "difficulty": req.difficulty,
        "topic": req.topic or question_data.get("topic", ""),
        "questions": [],
        "status": "in_progress",
        "created_at": datetime.now(timezone.utc),
    }

    result = await system_design_collection.insert_one(session_doc)
    session_id = str(result.inserted_id)

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$inc": {"interviews_used": 1}},
    )

    return {
        "session_id": session_id,
        "question": question_data.get("question", ""),
        "hints": question_data.get("hints", []),
        "expected_components": question_data.get("expected_components", []),
        "difficulty": req.difficulty,
        "topic": question_data.get("topic", ""),
    }


@router.post("/answer")
async def submit_system_design_answer(req: SubmitSystemDesignAnswer, user=Depends(get_current_user)):
    try:
        session = await system_design_collection.find_one({"_id": ObjectId(req.session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    feedback = await evaluate_system_design_answer(
        req.question, req.answer, req.diagram_description,
    )

    qa_pair = {
        "question": req.question,
        "answer": req.answer,
        "diagram_description": req.diagram_description,
        "feedback": feedback,
        "score": feedback.get("score", 5),
    }

    await system_design_collection.update_one(
        {"_id": ObjectId(req.session_id)},
        {"$push": {"questions": qa_pair}},
    )

    return {
        "feedback": feedback,
        "score": feedback.get("score", 5),
    }


@router.get("/{session_id}/result")
async def get_system_design_result(session_id: str, user=Depends(get_current_user)):
    try:
        session = await system_design_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    questions = session.get("questions", [])
    scores = [q["score"] for q in questions if q.get("score")]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    return {
        "session_id": session_id,
        "topic": session.get("topic", ""),
        "difficulty": session.get("difficulty", ""),
        "overall_score": avg_score,
        "questions": questions,
        "total_questions": len(questions),
    }


@router.get("/history")
async def get_system_design_history(user=Depends(get_current_user)):
    cursor = system_design_collection.find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(20)

    sessions = []
    async for doc in cursor:
        questions = doc.get("questions", [])
        scores = [q["score"] for q in questions if q.get("score")]
        sessions.append({
            "id": str(doc["_id"]),
            "topic": doc.get("topic", ""),
            "difficulty": doc.get("difficulty", ""),
            "overall_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "total_questions": len(questions),
            "created_at": doc.get("created_at"),
        })

    return {"sessions": sessions}
