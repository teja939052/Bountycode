from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, question_answers_collection,
    users_collection, solved_problems_collection
)
from app.models.question import SubmitAnswer, QuestionSubmission, QuestionVote
from app.services.ai import chat_completion, parse_json, assign_companies
from app.services.gamification import record_practice
from app.services.usage import check_and_reset_monthly_usage
from app.services.code_executor import CodeExecutionEngine
from app.services.cache import cache
from app.services import question_store
from app.services.explanation_cache import get_or_create_explanation
import random

router = APIRouter(prefix="/api/v1/questions", tags=["question-bank"])
code_engine = CodeExecutionEngine()


def _question_title(q: dict) -> str:
    return q.get("question") or q.get("question_title", "")


def _explain_compiler_error(error_message: str, source_code: str, language: str) -> str:
    error_lower = error_message.lower()
    if "compile" in error_lower or "syntax" in error_lower:
        return "Your code has a syntax error that stopped compilation before it could run. Check your syntax carefully."
    elif "timeout" in error_lower or "timelimit" in error_lower or "time limit" in error_lower:
        return "Your code exceeded the time limit. Try a more efficient algorithm."
    elif "memory" in error_lower or "mle" in error_lower or "out of memory" in error_lower:
        return "Your code exceeded the memory limit. Try using less memory-intensive data structures."
    elif "runtime" in error_lower or "exception" in error_lower or "error" in error_lower:
        return "Your code crashed during execution. Check for division by zero, null references, or out-of-bounds access."
    else:
        return "Your code failed to produce the expected output. Review your algorithm logic and edge cases."


def _is_correct_answer(user_ans: str, correct: str, q_type: str) -> bool:
    if not correct:
        return False
    if q_type == "aptitude":
        u = user_ans.lower().strip()
        c = correct.lower().strip()
        if u == c:
            return True
        try:
            return abs(float(u) - float(c)) / max(abs(float(c)), 1e-6) < 0.02
        except Exception:
            return False
    return bool(user_ans.strip())


@router.get("/browse")
async def browse_questions(
    company: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    sub_topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("frequency"),
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    user=Depends(get_current_user),
):
    query = {}
    if company:
        query["company"] = {"$in": [company, company.title(), company.upper()]}
    if role:
        query["role"] = role
    if topic:
        query["topic"] = topic
    if sub_topic:
        query["sub_topic"] = sub_topic
    if difficulty:
        query["difficulty"] = difficulty
    if type:
        query["type"] = type
    if search:
        query["$text"] = {"$search": search}

    if sort == "difficulty":
        sort_stage = [("difficulty", 1), ("frequency", -1)]
    elif sort == "companies":
        sort_stage = [("company", -1), ("frequency", -1)]
    elif sort == "acceptance":
        sort_stage = [("frequency", -1)]
    elif sort == "newest":
        sort_stage = [("frequency", -1)]
    elif sort == "alphabetical":
        sort_stage = [("question", 1)]
    else:
        sort_stage = [("frequency", -1)]

    total = question_store.count_documents(query)
    skip = (page - 1) * limit
    items = question_store.find(query).skip(skip).limit(limit).sort(sort_stage).to_list()

    return {
        "questions": items,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit if total > 0 else 1,
        "sort": sort,
    }


@router.get("/filters")
async def get_filters():
    cache_key = "question_filters_v3"
    cached = await cache.get("filters", cache_key)
    if cached:
        return cached

    result = question_store.get_filters()
    await cache.set("filters", cache_key, result, ttl=300)
    return result


@router.get("/stats")
async def get_my_stats(user=Depends(get_current_user)):
    collection = question_answers_collection()
    uid = user["id"]

    total_attempted = await collection.count_documents({"user_id": uid})
    pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {
            "_id": "$topic",
            "avg_score": {"$avg": "$score"},
            "count": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}},
        },
        {"$sort": {"avg_score": 1}},
    ]
    topic_stats = []
    async for doc in collection.aggregate(pipeline):
        topic_stats.append({
            "topic": doc["_id"],
            "avg_score": round(doc["avg_score"], 1),
            "count": doc["count"],
            "accuracy": round(doc["correct"] / doc["count"] * 100, 1) if doc["count"] > 0 else 0,
        })

    weak_areas = [t for t in topic_stats if t["avg_score"] < 6][:5]
    strong_areas = [t for t in topic_stats if t["avg_score"] >= 7][:5]

    return {
        "total_attempted": total_attempted,
        "topic_stats": topic_stats,
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
    }


@router.post("/submit")
async def submit_question(req: QuestionSubmission, user=Depends(get_current_user)):
    doc = req.model_dump()
    doc["submitted_by"] = user["id"]
    doc["upvotes"] = 0
    doc["downvotes"] = 0
    doc["reported"] = False
    doc["created_at"] = datetime.now(timezone.utc)
    doc["updated_at"] = datetime.now(timezone.utc)
    result = await curated_questions_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/upvote")
async def upvote_question(req: QuestionVote, user=Depends(get_current_user)):
    question = question_store.find_one({"id": req.question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    try:
        q_oid = ObjectId(req.question_id)
        await curated_questions_collection.update_one(
            {"_id": q_oid},
            {"$inc": {"upvotes": max(0, req.vote), "downvotes": max(0, -req.vote)}, "$set": {"updated_at": datetime.now(timezone.utc)}},
        )
        updated = await curated_questions_collection.find_one({"_id": q_oid})
        up = updated.get("upvotes", 0) if updated else question.get("upvotes", 0)
        down = updated.get("downvotes", 0) if updated else question.get("downvotes", 0)
    except Exception:
        up = question.get("upvotes", 0) + max(0, req.vote)
        down = question.get("downvotes", 0) + max(0, -req.vote)

    return {
        "question_id": req.question_id,
        "upvotes": up,
        "downvotes": down,
    }


from app.routes.questions_solve import router as solve_router

router.include_router(solve_router)