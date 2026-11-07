from datetime import datetime, timezone
import json
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection, system_design_collection
from app.middleware.auth import get_current_user
from app.services.ai_system_design import generate_system_design_question, evaluate_system_design_answer
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/v1/system-design", tags=["system-design"])
settings = get_settings()

# Canonical System Design bank (single source of truth, file-backed).
_SD_BANK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "system_design_bank.json"
)
_SD_BANK = []

# topic keyword -> bank sub_topic (served bank-first, AI fallback on miss)
_TOPIC_MAP = {
    "url": "url_shortener",
    "shortener": "url_shortener",
    "rate": "rate_limiter",
    "limiter": "rate_limiter",
    "notification": "notification_service",
    "chat": "chat_system",
    "whatsapp": "chat_system",
    "messaging": "chat_system",
    "payment": "payment_system",
    "stripe": "payment_system",
    "queue": "job_queue",
    "job": "job_queue",
    "analytics": "analytics",
    "dashboard": "analytics",
    "feed": "social_feed",
    "social": "social_feed",
    "twitter": "social_feed",
    "cache": "distributed_cache",
    "inventory": "inventory",
    "ecommerce": "inventory",
    "e-commerce": "inventory",
    "shop": "inventory",
}


def _load_sd_bank() -> List[dict]:
    global _SD_BANK
    if not _SD_BANK:
        try:
            with open(_SD_BANK_PATH, "r", encoding="utf-8") as f:
                _SD_BANK = json.load(f)
        except Exception:
            _SD_BANK = []
    return _SD_BANK


def _pick_bank_question(difficulty: str, topic: str) -> Optional[dict]:
    """Return a bank entry (as AI-shaped data) if one matches, else None."""
    bank = _load_sd_bank()
    if not bank:
        return None
    target = None
    tl = (topic or "").lower()
    # Prefer an explicit topic match.
    for key, sub in _TOPIC_MAP.items():
        if key in tl:
            target = sub
            break
    candidates = bank
    if target:
        candidates = [e for e in bank if e.get("sub_topic") == target]
    if not candidates:
        candidates = bank
    # Match difficulty when possible.
    diff = difficulty if difficulty in ("easy", "medium", "hard") else "medium"
    ranked = [e for e in candidates if e.get("difficulty") == diff]
    if not ranked:
        ranked = candidates
    entry = ranked[0]
    return {
        "question": entry.get("statement") or entry.get("question", ""),
        "hints": entry.get("hints", []),
        "expected_components": entry.get("key_components", []),
        "difficulty": entry.get("difficulty", diff),
        "topic": topic or entry.get("sub_topic", ""),
        "mental_model": entry.get("mental_model", ""),
        "reasoning_steps": entry.get("reasoning_steps", []),
        "explanation": entry.get("explanation", ""),
        "rubric": entry.get("rubric", {}),
        "follow_up": entry.get("follow_up", ""),
        "bank_id": entry.get("id"),
    }


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

    # Bank-first: serve canonical human-reviewed content when a topic matches.
    question_data = _pick_bank_question(req.difficulty, req.topic)
    if question_data is None:
        question_data = await generate_system_design_question(req.difficulty, req.topic)

    session_doc = {
        "user_id": user["id"],
        "type": "system_design",
        "difficulty": question_data.get("difficulty", req.difficulty),
        "topic": question_data.get("topic", "") or req.topic,
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
        "difficulty": question_data.get("difficulty", req.difficulty),
        "topic": question_data.get("topic", ""),
        "mental_model": question_data.get("mental_model", ""),
        "reasoning_steps": question_data.get("reasoning_steps", []),
        "explanation": question_data.get("explanation", ""),
        "rubric": question_data.get("rubric", {}),
        "follow_up": question_data.get("follow_up", ""),
        "bank_id": question_data.get("bank_id"),
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
