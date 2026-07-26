"""
Submission Distribution Graphs — Compare your runtime/memory with other users.
Shows histograms and percentile rankings for each problem.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, submissions_collection,
    solved_problems_collection
)

router = APIRouter(prefix="/api/distributions", tags=["distributions"])


@router.get("/runtime/{question_id}")
async def get_runtime_distribution(
    question_id: str,
    language: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get runtime distribution for a problem."""
    collection = curated_questions_collection()
    submissions_col = submissions_collection()

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Get all accepted submissions for this problem
    query = {"question_id": question_id, "status": "Accepted"}
    if language:
        query["language"] = language

    runtimes = []
    async for doc in submissions_col.find(query, {"execution_time": 1, "language": 1, "user_id": 1}):
        rt = doc.get("execution_time", 0)
        if rt and rt > 0:
            runtimes.append({
                "runtime": round(rt * 1000, 2),  # Convert to ms
                "language": doc.get("language", "unknown"),
                "is_user": doc["user_id"] == user["id"],
            })

    if not runtimes:
        return {
            "question_id": question_id,
            "distribution": [],
            "user_percentile": None,
            "message": "No submission data available yet"
        }

    # Sort by runtime
    runtimes.sort(key=lambda x: x["runtime"])

    # Create histogram buckets
    if runtimes:
        min_rt = runtimes[0]["runtime"]
        max_rt = runtimes[-1]["runtime"]
        range_rt = max_rt - min_rt if max_rt > min_rt else 1
        bucket_size = range_rt / 20  # 20 buckets

        buckets = []
        for i in range(20):
            bucket_min = min_rt + i * bucket_size
            bucket_max = min_rt + (i + 1) * bucket_size
            count = sum(1 for r in runtimes if bucket_min <= r["runtime"] < bucket_max)
            buckets.append({
                "min": round(bucket_min, 2),
                "max": round(bucket_max, 2),
                "count": count,
            })

        # Calculate user's percentile
        user_runtimes = [r for r in runtimes if r["is_user"]]
        user_percentile = None
        if user_runtimes:
            user_best = min(r["runtime"] for r in user_runtimes)
            users_faster = sum(1 for r in runtimes if r["runtime"] <= user_best)
            user_percentile = round(users_faster / len(runtimes) * 100, 1)

        # Stats
        avg_runtime = sum(r["runtime"] for r in runtimes) / len(runtimes)
        median_runtime = runtimes[len(runtimes) // 2]["runtime"]

        return {
            "question_id": question_id,
            "total_submissions": len(runtimes),
            "distribution": buckets,
            "user_percentile": user_percentile,
            "user_runtimes": user_runtimes,
            "stats": {
                "average": round(avg_runtime, 2),
                "median": round(median_runtime, 2),
                "fastest": round(runtimes[0]["runtime"], 2),
                "slowest": round(runtimes[-1]["runtime"], 2),
            }
        }

    return {"question_id": question_id, "distribution": [], "user_percentile": None}


@router.get("/memory/{question_id}")
async def get_memory_distribution(
    question_id: str,
    language: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get memory distribution for a problem."""
    submissions_col = submissions_collection()

    query = {"question_id": question_id, "status": "Accepted"}
    if language:
        query["language"] = language

    memories = []
    async for doc in submissions_col.find(query, {"memory_usage": 1, "language": 1, "user_id": 1}):
        mem = doc.get("memory_usage", 0)
        if mem and mem > 0:
            memories.append({
                "memory": round(mem / 1024, 2),  # Convert to MB
                "language": doc.get("language", "unknown"),
                "is_user": doc["user_id"] == user["id"],
            })

    if not memories:
        return {
            "question_id": question_id,
            "distribution": [],
            "user_percentile": None,
            "message": "No memory data available yet"
        }

    memories.sort(key=lambda x: x["memory"])

    # Histogram
    min_mem = memories[0]["memory"]
    max_mem = memories[-1]["memory"]
    range_mem = max_mem - min_mem if max_mem > min_mem else 1
    bucket_size = range_mem / 20

    buckets = []
    for i in range(20):
        bucket_min = min_mem + i * bucket_size
        bucket_max = min_mem + (i + 1) * bucket_size
        count = sum(1 for m in memories if bucket_min <= m["memory"] < bucket_max)
        buckets.append({
            "min": round(bucket_min, 2),
            "max": round(bucket_max, 2),
            "count": count,
        })

    # User percentile
    user_mems = [m for m in memories if m["is_user"]]
    user_percentile = None
    if user_mems:
        user_best = min(m["memory"] for m in user_mems)
        users_less = sum(1 for m in memories if m["memory"] <= user_best)
        user_percentile = round(users_less / len(memories) * 100, 1)

    return {
        "question_id": question_id,
        "total_submissions": len(memories),
        "distribution": buckets,
        "user_percentile": user_percentile,
        "user_memories": user_mems,
    }


@router.get("/comparison/{question_id}")
async def get_submission_comparison(
    question_id: str,
    user=Depends(get_current_user),
):
    """Get a comprehensive comparison of user's submission vs others."""
    submissions_col = submissions_collection()

    # Get user's submissions
    user_subs = []
    async for doc in submissions_col.find(
        {"question_id": question_id, "user_id": user["id"]}
    ).sort("submitted_at", -1).limit(5):
        user_subs.append({
            "runtime": round(doc.get("execution_time", 0) * 1000, 2),
            "memory": round(doc.get("memory_usage", 0) / 1024, 2),
            "language": doc.get("language", "unknown"),
            "status": doc.get("status", "Unknown"),
            "submitted_at": doc.get("submitted_at", datetime.now(timezone.utc)).isoformat(),
        })

    # Get all accepted submissions stats
    all_subs = []
    async for doc in submissions_col.find(
        {"question_id": question_id, "status": "Accepted"}
    ):
        rt = doc.get("execution_time", 0)
        if rt and rt > 0:
            all_subs.append({
                "runtime": round(rt * 1000, 2),
                "memory": round(doc.get("memory_usage", 0) / 1024, 2),
                "language": doc.get("language", "unknown"),
            })

    # Calculate stats
    if all_subs:
        all_runtimes = [s["runtime"] for s in all_subs]
        avg_runtime = sum(all_runtimes) / len(all_runtimes)

        # Language breakdown
        lang_stats = {}
        for sub in all_subs:
            lang = sub["language"]
            if lang not in lang_stats:
                lang_stats[lang] = {"count": 0, "avg_runtime": 0, "total_runtime": 0}
            lang_stats[lang]["count"] += 1
            lang_stats[lang]["total_runtime"] += sub["runtime"]

        for lang in lang_stats:
            lang_stats[lang]["avg_runtime"] = round(lang_stats[lang]["total_runtime"] / lang_stats[lang]["count"], 2)
            del lang_stats[lang]["total_runtime"]

        return {
            "question_id": question_id,
            "user_submissions": user_subs,
            "total_accepted": len(all_subs),
            "stats": {
                "average_runtime": round(avg_runtime, 2),
                "fastest": round(min(all_runtimes), 2),
                "slowest": round(max(all_runtimes), 2),
            },
            "language_breakdown": lang_stats,
            "user_best_runtime": user_subs[0]["runtime"] if user_subs else None,
        }

    return {
        "question_id": question_id,
        "user_submissions": user_subs,
        "total_accepted": 0,
        "message": "No submission data available"
    }
