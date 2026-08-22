"""Mission Engine routes — the 5-layer learning loop API."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.mission_engine import (
    get_topic_mastery, update_topic_mastery, get_all_topic_mastery,
    get_learning_stats, get_hint, INTERACTION_TYPES, MASTERY_DIMENSIONS,
    SKILL_RANKS, DOMAIN_MAP, HINT_LEVELS,
)
from app.data.mission_data import ALL_MISSIONS

router = APIRouter(prefix="/api/v1/missions", tags=["Mission Engine"])


@router.get("/content")
async def all_mission_content():
    """Return all available mission content (public, no auth)."""
    return {"missions": list(ALL_MISSIONS.keys()), "count": len(ALL_MISSIONS)}


@router.get("/content/{topic}")
async def mission_content(topic: str):
    """Return full 5-layer mission content for a topic."""
    if topic not in ALL_MISSIONS:
        raise HTTPException(404, f"No mission content for topic: {topic}")
    return ALL_MISSIONS[topic]


@router.get("/interaction-types")
async def interaction_types():
    return {"types": list(INTERACTION_TYPES.values())}


@router.get("/mastery-dimensions")
async def mastery_dimensions():
    return {"dimensions": list(MASTERY_DIMENSIONS.values())}


@router.get("/skill-ranks")
async def skill_ranks():
    return {"ranks": SKILL_RANKS}


@router.get("/topics")
async def topic_list():
    topics = []
    for topic, info in DOMAIN_MAP.items():
        topics.append({"id": topic, "domain": info["domain"], "sub_skill": info["sub_skill"], "readiness_weight": info["readiness_weight"]})
    return {"topics": topics}


@router.get("/mastery/{topic}")
async def topic_mastery(topic: str, user=Depends(get_current_user)):
    if topic not in DOMAIN_MAP:
        raise HTTPException(404, f"Unknown topic: {topic}")
    return await get_topic_mastery(user["id"], topic)


@router.get("/mastery")
async def all_mastery(user=Depends(get_current_user)):
    return await get_all_topic_mastery(user["id"])


@router.get("/stats")
async def learning_stats(user=Depends(get_current_user)):
    return await get_learning_stats(user["id"])


class InteractionSubmit(BaseModel):
    topic: str
    interaction_type: str
    score: float
    is_correct: bool
    time_taken: Optional[float] = None
    answer: Optional[str] = None


@router.post("/interact")
async def submit_interaction(req: InteractionSubmit, user=Depends(get_current_user)):
    if req.topic not in DOMAIN_MAP:
        raise HTTPException(404, f"Unknown topic: {req.topic}")
    if req.interaction_type not in INTERACTION_TYPES:
        raise HTTPException(400, f"Unknown interaction type: {req.interaction_type}")
    if not 0 <= req.score <= 100:
        raise HTTPException(400, "Score must be 0-100")

    result = await update_topic_mastery(
        user_id=user["id"],
        topic=req.topic,
        interaction_type=req.interaction_type,
        score=req.score,
        is_correct=req.is_correct,
    )
    return result


class HintRequest(BaseModel):
    topic: str
    interaction_type: str
    hint_level: int = 1
    context: Optional[dict] = None


@router.post("/hint")
async def request_hint(req: HintRequest, user=Depends(get_current_user)):
    if req.topic not in DOMAIN_MAP:
        raise HTTPException(404, f"Unknown topic: {req.topic}")
    return get_hint(req.topic, req.interaction_type, req.hint_level, req.context)


@router.get("/rank/{topic}")
async def topic_rank_info(topic: str, user=Depends(get_current_user)):
    mastery = await get_topic_mastery(user["id"], topic)
    return {
        "topic": topic,
        "current_rank": mastery["rank"],
        "overall": mastery["overall"],
        "next_rank": _next_rank(mastery["overall"]),
        "dimensions": mastery["dimensions"],
    }


def _next_rank(current_score: float) -> Optional[dict]:
    for r in SKILL_RANKS:
        if current_score < r["min_score"]:
            return {"rank": r["rank"], "icon": r["icon"], "min_score": r["min_score"], "gap": round(r["min_score"] - current_score, 1)}
    return None


@router.get("/domain/{domain}")
async def domain_progress(domain: str, user=Depends(get_current_user)):
    all_mastery = await get_all_topic_mastery(user["id"])
    domain_topics = [m for m in all_mastery if m["domain"] == domain]
    if not domain_topics:
        raise HTTPException(404, f"Unknown domain: {domain}")

    avg = sum(t["overall"] for t in domain_topics) / len(domain_topics) if domain_topics else 0
    mastered = sum(1 for t in domain_topics if t["overall"] >= 80)
    practiced = sum(1 for t in domain_topics if t["total_attempts"] > 0)

    return {
        "domain": domain,
        "topics": domain_topics,
        "avg_mastery": round(avg, 1),
        "mastered_count": mastered,
        "practiced_count": practiced,
        "total_topics": len(domain_topics),
    }
