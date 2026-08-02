"""
Practice for This Role — backend route + service.
Zero-LLM path: reuses curated_questions + existing company mock blueprint logic.
AI-enhanced path: can also call ai.generate_* for dynamic question generation.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from app.middleware.auth import get_current_user
from app.services import company_conversion as conv
from app.services.placement_engine import PlacementEngine
from app.services.career_profile import get_profile
from app.services.ai import chat_completion, parse_json
from app.config import get_settings
from datetime import datetime, timezone
from bson import ObjectId
from app.database import (
    users_collection,
    curated_questions_collection,
    practice_sessions_collection,
    skill_graph_collection,
    gamification_collection,
)

router = APIRouter(prefix="/api/v1/practice", tags=["practice"])
settings = get_settings()
engine = PlacementEngine()


class PracticeSessionRequest(BaseModel):
    company: str = Field(..., min_length=2)
    role: str = "SDE"
    focus_areas: Optional[List[str]] = None  # e.g. ["dsa", "behavioral"]


class PracticeSessionResponse(BaseModel):
    session_id: str
    company: str
    role: str
    focus_areas: List[str]
    coding: List[dict]
    behavioral: List[dict]
    system_design: List[dict]
    weak_areas: List[str]
    strong_areas: List[str]
    probability_before: float
    probability_after_target: float


@router.post("/session", response_model=PracticeSessionResponse)
async def create_practice_session(req: PracticeSessionRequest, user=Depends(get_current_user)):
    company = req.company.lower().strip()
    role = req.role.strip() or "SDE"

    # 1) Load user state
    profile = await get_profile(user["id"])
    prediction = await engine.calculate_probability(user["id"], company, role)
    prob_before = prediction["current_probability"]

    # 2) Weak/strong areas from skill graph
    skill_graph = await skill_graph_collection.find_one({"user_id": user["id"]})
    categories = (skill_graph or {}).get("categories", {})
    weak_areas = [cid for cid, c in categories.items() if c.get("score", 0) < 60]
    strong_areas = [cid for cid, c in categories.items() if c.get("score", 0) >= 75]

    # 3) Pick questions from bank — company-tagged, role-relevant
    coding = await conv._pick_questions(company, "coding", 3)
    behavioral = await conv._pick_questions(company, "behavioral", 2)
    system_design = await conv._pick_questions(company, "system_design", 1)

    def serialize(q):
        return {
            "question_id": str(q.get("_id")),
            "question_title": q.get("question_title", ""),
            "topic": q.get("topic", ""),
            "type": q.get("type", ""),
            "difficulty": q.get("difficulty", "medium"),
            "company": q.get("company", company.title()),
            "question_link": q.get("question_link"),
        }

    session_doc = {
        "user_id": user["id"],
        "company": company,
        "role": role,
        "focus_areas": req.focus_areas or weak_areas[:3],
        "coding": [serialize(q) for q in coding],
        "behavioral": [serialize(q) for q in behavioral],
        "system_design": [serialize(q) for q in system_design],
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
        "probability_before": prob_before,
        "status": "in_progress",
        "created_at": datetime.now(timezone.utc),
    }

    result = await practice_sessions_collection.insert_one(session_doc)
    session_id = str(result.inserted_id)

    target_prob = min(99.0, prob_before + 12.0)
    return {
        "session_id": session_id,
        "company": company.title(),
        "role": role,
        "focus_areas": session_doc["focus_areas"],
        "coding": session_doc["coding"],
        "behavioral": session_doc["behavioral"],
        "system_design": session_doc["system_design"],
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
        "probability_before": round(prob_before, 1),
        "probability_after_target": round(target_prob, 1),
    }


@router.post("/session/{session_id}/complete")
async def complete_practice_session(session_id: str, user=Depends(get_current_user)):
    try:
        oid = ObjectId(session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    session = await practice_sessions_collection.find_one({"_id": oid, "user_id": user["id"]})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    company = session.get("company", "")
    # Recompute probability post-practice
    try:
        updated = await engine.calculate_probability(user["id"], company, session.get("role", "SDE"))
        prob_after = updated["current_probability"]
    except Exception:
        prob_after = session.get("probability_before", 0)

    now = datetime.now(timezone.utc)
    await practice_sessions_collection.update_one(
        {"_id": oid},
        {"$set": {"status": "completed", "completed_at": now, "probability_after": prob_after}},
    )

    return {
        "session_id": session_id,
        "status": "completed",
        "probability_before": session.get("probability_before", 0),
        "probability_after": round(prob_after, 1),
        "boost": round(prob_after - session.get("probability_before", 0), 1),
    }


@router.get("/sessions")
async def list_practice_sessions(user=Depends(get_current_user)):
    cursor = practice_sessions_collection.find({"user_id": user["id"]}).sort("created_at", -1).limit(20)
    sessions = []
    async for s in cursor:
        sessions.append({
            "session_id": str(s["_id"]),
            "company": s.get("company", "").title(),
            "role": s.get("role", ""),
            "status": s.get("status", ""),
            "probability_before": s.get("probability_before"),
            "probability_after": s.get("probability_after"),
            "created_at": s.get("created_at"),
            "completed_at": s.get("completed_at"),
        })
    return {"sessions": sessions, "total": len(sessions)}


async def init_db():
    db = get_db()
    if "practice_sessions" not in await db.list_collection_names():
        await db.create_collection("practice_sessions")
    await db["practice_sessions"].create_index("user_id")
    await db["practice_sessions"].create_index([("user_id", 1), ("created_at", -1)])
    await db["practice_sessions"].create_index("status")
