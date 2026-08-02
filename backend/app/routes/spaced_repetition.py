from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.middleware.auth import get_current_user
from app.database import users_collection, srs_collection
from app.services.spaced_repetition import (
    SpacedRepetitionEngine, 
    SRSState, 
    ReviewGrade, 
    DSA_CONCEPTS,
    initialize_user_srs,
    get_all_concept_ids,
)
from app.services.usage import check_and_reset_monthly_usage
from bson import ObjectId

router = APIRouter(prefix="/api/v1/srs", tags=["spaced-repetition"])
engine = SpacedRepetitionEngine()


class ReviewRequest(BaseModel):
    concept_id: str = Field(..., min_length=1)
    grade: int = Field(..., ge=0, le=3)  # 0=Again, 1=Hard, 2=Good, 3=Easy


class BulkReviewRequest(BaseModel):
    reviews: List[ReviewRequest] = Field(..., max_length=50)


class InitializeSRSRequest(BaseModel):
    concept_ids: Optional[List[str]] = None  # If None, use all DSA concepts


@router.post("/initialize")
async def initialize_srs(req: InitializeSRSRequest, user=Depends(get_current_user)):
    """Initialize SRS for a user (run once on first access)"""
    existing = await srs_collection.count_documents({"user_id": user["id"]})
    if existing > 0:
        return {"message": "SRS already initialized", "count": existing}
    
    concept_ids = req.concept_ids or get_all_concept_ids()
    states = initialize_user_srs(user["id"])
    
    # Filter if specific concept_ids provided
    if req.concept_ids:
        states = [s for s in states if s.concept_id in req.concept_ids]
    
    # Convert to dict for MongoDB
    docs = []
    for state in states:
        doc = {
            "user_id": state.user_id,
            "concept_id": state.concept_id,
            "interval": state.interval,
            "repetitions": state.repetitions,
            "ease_factor": state.ease_factor,
            "next_review": state.next_review,
            "last_reviewed": state.last_reviewed,
            "learning_step": state.learning_step,
            "total_reviews": state.total_reviews,
            "lapses": state.lapses,
            "created_at": state.created_at,
            "updated_at": state.updated_at,
        }
        docs.append(doc)
    
    if docs:
        await srs_collection.insert_many(docs)
    
    return {"message": "SRS initialized", "count": len(docs)}


def _state_from_doc(doc: dict) -> SRSState:
    """Convert MongoDB doc to SRSState"""
    return SRSState(
        concept_id=doc["concept_id"],
        user_id=doc["user_id"],
        interval=doc.get("interval", 0),
        repetitions=doc.get("repetitions", 0),
        ease_factor=doc.get("ease_factor", 2.5),
        next_review=doc.get("next_review", datetime.now(timezone.utc)),
        last_reviewed=doc.get("last_reviewed"),
        learning_step=doc.get("learning_step", 0),
        total_reviews=doc.get("total_reviews", 0),
        lapses=doc.get("lapses", 0),
        created_at=doc.get("created_at", datetime.now(timezone.utc)),
        updated_at=doc.get("updated_at", datetime.now(timezone.utc)),
    )


@router.post("/review")
async def review_concept(req: ReviewRequest, user=Depends(get_current_user)):
    """Submit a review for a concept"""
    doc = await srs_collection.find_one({
        "user_id": user["id"],
        "concept_id": req.concept_id
    })
    
    if not doc:
        # Auto-create if missing
        state = SRSState(
            concept_id=req.concept_id,
            user_id=user["id"],
            interval=0,
            repetitions=0,
            ease_factor=2.5,
            next_review=datetime.now(timezone.utc),
        )
    else:
        state = _state_from_doc(doc)
    
    # Validate grade
    if req.grade not in [0, 1, 2, 3]:
        raise HTTPException(status_code=400, detail="Grade must be 0-3")
    
    grade = ReviewGrade(req.grade)
    new_state = engine.review(state, grade)
    
    # Update in MongoDB
    update_doc = {
        "interval": new_state.interval,
        "repetitions": new_state.repetitions,
        "ease_factor": new_state.ease_factor,
        "next_review": new_state.next_review,
        "last_reviewed": new_state.last_reviewed,
        "learning_step": new_state.learning_step,
        "total_reviews": new_state.total_reviews,
        "lapses": new_state.lapses,
        "updated_at": new_state.updated_at,
    }
    
    await srs_collection.update_one(
        {"user_id": user["id"], "concept_id": req.concept_id},
        {"$set": update_doc},
        upsert=True
    )
    
    return {
        "concept_id": req.concept_id,
        "grade": req.grade,
        "new_interval": new_state.interval,
        "new_ease_factor": round(new_state.ease_factor, 2),
        "next_review": new_state.next_review.isoformat() if new_state.next_review else None,
        "repetitions": new_state.repetitions,
        "is_learning": new_state.interval == 0,
        "learning_step": new_state.learning_step,
    }


@router.post("/review/bulk")
async def bulk_review(req: BulkReviewRequest, user=Depends(get_current_user)):
    """Submit multiple reviews at once"""
    results = []
    for review in req.reviews:
        try:
            result = await review_concept(review, user)
            results.append({"concept_id": review.concept_id, "success": True, **result})
        except Exception as e:
            results.append({"concept_id": review.concept_id, "success": False, "error": str(e)})
    
    return {"results": results}


@router.get("/due")
async def get_due_cards(limit: int = 20, user=Depends(get_current_user)):
    """Get cards due for review"""
    cursor = srs_collection.find({
        "user_id": user["id"],
        "next_review": {"$lte": datetime.now(timezone.utc)}
    }).limit(limit)
    
    cards = []
    async for doc in cursor:
        state = _state_from_doc(doc)
        
        # Get concept metadata
        concept_info = _get_concept_info(state.concept_id)
        
        cards.append({
            "concept_id": state.concept_id,
            "topic": concept_info["topic"],
            "subtopic": concept_info["subtopic"],
            "interval": state.interval,
            "ease_factor": round(state.ease_factor, 2),
            "repetitions": state.repetitions,
            "overdue_days": (datetime.now(timezone.utc) - state.next_review).days if state.next_review < datetime.now(timezone.utc) else 0,
            "is_learning": state.interval == 0,
            "learning_step": state.learning_step,
            "next_review": state.next_review.isoformat() if state.next_review else None,
        })
    
    return {"cards": cards, "count": len(cards)}


@router.get("/stats")
async def get_srs_stats(user=Depends(get_current_user)):
    """Get SRS statistics for the user"""
    cursor = srs_collection.find({"user_id": user["id"]})
    states = []
    async for doc in cursor:
        states.append(_state_from_doc(doc))
    
    stats = engine.get_stats(states)
    
    # Add topic breakdown
    topic_stats = {}
    for state in states:
        info = _get_concept_info(state.concept_id)
        topic = info["topic"]
        if topic not in topic_stats:
            topic_stats[topic] = {"total": 0, "due": 0, "mastered": 0, "learning": 0}
        topic_stats[topic]["total"] += 1
        if state.next_review <= datetime.now(timezone.utc):
            topic_stats[topic]["due"] += 1
        if state.interval >= 21:  # 3+ weeks = mastered
            topic_stats[topic]["mastered"] += 1
        if state.interval == 0:
            topic_stats[topic]["learning"] += 1
    
    stats["topic_breakdown"] = topic_stats
    return stats


@router.get("/concepts")
async def get_all_concepts(user=Depends(get_current_user)):
    """Get all DSA concepts with their SRS state"""
    # Get user's SRS states
    cursor = srs_collection.find({"user_id": user["id"]})
    state_map = {}
    async for doc in cursor:
        state = _state_from_doc(doc)
        state_map[state.concept_id] = state
    
    # Build full tree with states
    topics = []
    for topic_id, topic_data in DSA_CONCEPTS.items():
        subtopics = []
        for sub in topic_data["subtopics"]:
            cid = f"{topic_id}:{sub}"
            state = state_map.get(cid)
            if state:
                subtopics.append({
                    "id": cid,
                    "name": sub.replace("-", " ").title(),
                    "interval": state.interval,
                    "ease_factor": round(state.ease_factor, 2),
                    "repetitions": state.repetitions,
                    "next_review": state.next_review.isoformat() if state.next_review else None,
                    "is_due": state.next_review <= datetime.now(timezone.utc) if state.next_review else True,
                    "is_learning": state.interval == 0,
                    "mastery": _get_mastery_level(state),
                })
            else:
                subtopics.append({
                    "id": cid,
                    "name": sub.replace("-", " ").title(),
                    "interval": 0,
                    "ease_factor": 2.5,
                    "repetitions": 0,
                    "next_review": None,
                    "is_due": True,
                    "is_learning": True,
                    "mastery": "new",
                })
        
        topics.append({
            "id": topic_id,
            "name": topic_data["name"],
            "subtopics": subtopics,
            "progress": _calculate_topic_progress(subtopics),
        })
    
    return {"topics": topics}


def _get_concept_info(concept_id: str) -> Dict[str, str]:
    """Parse concept_id into topic and subtopic"""
    parts = concept_id.split(":", 1)
    if len(parts) == 2:
        topic_id, subtopic = parts
        topic_name = DSA_CONCEPTS.get(topic_id, {}).get("name", topic_id)
        return {"topic": topic_name, "subtopic": subtopic.replace("-", " ").title()}
    return {"topic": "Unknown", "subtopic": concept_id}


def _get_mastery_level(state: SRSState) -> str:
    """Get mastery level label from SRS state"""
    if state.interval == 0:
        if state.repetitions == 0:
            return "new"
        return "learning"
    elif state.interval < 1:
        return "learning"
    elif state.interval < 7:
        return "young"
    elif state.interval < 30:
        return "maturing"
    elif state.interval < 90:
        return "mature"
    else:
        return "mastered"


def _calculate_topic_progress(subtopics: List[Dict]) -> Dict[str, Any]:
    """Calculate progress for a topic"""
    total = len(subtopics)
    if total == 0:
        return {"mastered": 0, "learning": 0, "new": 0, "pct": 0}
    
    mastered = sum(1 for s in subtopics if s["mastery"] == "mastered")
    learning = sum(1 for s in subtopics if s["mastery"] in ["learning", "young"])
    new = sum(1 for s in subtopics if s["mastery"] == "new")
    
    return {
        "mastered": mastered,
        "learning": learning,
        "new": new,
        "pct": round((mastered / total) * 100, 1),
    }


@router.get("/forecast")
async def get_forecast(days: int = 30, user=Depends(get_current_user)):
    """Get review forecast for next N days"""
    cursor = srs_collection.find({"user_id": user["id"]})
    states = []
    async for doc in cursor:
        states.append(_state_from_doc(doc))
    
    # Aggregate forecast
    forecast = {}
    for state in states:
        for f in engine.simulate_forecast(state, days):
            date = f["date"]
            if date not in forecast:
                forecast[date] = 0
            forecast[date] += f["reviews_due"]
    
    # Convert to sorted list
    forecast_list = [
        {"date": date, "reviews_due": count}
        for date, count in sorted(forecast.items())
    ]
    
    return {"forecast": forecast_list}