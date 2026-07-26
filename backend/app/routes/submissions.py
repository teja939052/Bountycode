"""
Submission History & Solved Status Tracking.
Track every code submission, solved problems, and provide detailed stats.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, solved_problems_collection,
    question_answers_collection, submissions_collection
)

router = APIRouter(prefix="/api/submissions", tags=["submissions"])


@router.post("/{question_id}/submit")
async def submit_code(
    question_id: str,
    code: str,
    language: str,
    user=Depends(get_current_user),
):
    """Submit code for a problem and record submission history."""
    from app.services.code_executor import CodeExecutionEngine

    engine = CodeExecutionEngine()

    # Get the question
    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await curated_questions_collection().find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Execute against hidden test cases
    hidden_cases = question.get("hidden_test_cases", [])
    visible_cases = question.get("visible_test_cases", [])
    all_cases = visible_cases + hidden_cases

    results = []
    passed_count = 0
    total_cases = len(all_cases)
    total_time = 0

    for case in all_cases:
        result = await engine.execute_code(code, language, case.get("input", ""), timeout=5)
        if result["success"]:
            actual = result["stdout"].strip()
            expected = case.get("expected", "").strip()
            passed = actual == expected
            if passed:
                passed_count += 1
        else:
            actual = result.get("error", "Execution failed")
            passed = False

        exec_time = result.get("execution_time", 0)
        total_time += exec_time

        results.append({
            "passed": passed,
            "input": case.get("input", ""),
            "expected": case.get("expected", ""),
            "actual": actual if passed else "[FAILED]",
            "is_hidden": case.get("is_hidden", False),
            "execution_time": exec_time,
            "error": result.get("error") if not result["success"] else None,
        })

    all_passed = passed_count == total_cases
    score = round(passed_count / total_cases * 100, 1) if total_cases > 0 else 0
    status = "Accepted" if all_passed else "Wrong Answer"

    if not all_passed:
        has_error = any(r.get("error") for r in results)
        has_timeout = any("timeout" in (r.get("error") or "").lower() for r in results)
        if has_timeout:
            status = "Time Limit Exceeded"
        elif has_error:
            status = "Runtime Error"

    # Record submission
    submission = {
        "user_id": user["id"],
        "question_id": question_id,
        "code": code,
        "language": language,
        "status": status,
        "score": score,
        "passed_count": passed_count,
        "total_cases": total_cases,
        "results": results,
        "execution_time": round(total_time, 3),
        "submitted_at": datetime.now(timezone.utc),
    }

    result = await submissions_collection().insert_one(submission)
    submission["id"] = str(result.inserted_id)

    # Update solved status if all passed
    if all_passed:
        await solved_problems_collection().update_one(
            {"user_id": user["id"], "question_id": question_id},
            {"$set": {
                "user_id": user["id"],
                "question_id": question_id,
                "code": code,
                "language": language,
                "score": score,
                "solved_at": datetime.now(timezone.utc),
                "best_time": total_time,
            }},
            upsert=True,
        )

    # Update question stats
    await curated_questions_collection().update_one(
        {"_id": q_oid},
        {"$inc": {"total_submissions": 1, "total_accepted": 1 if all_passed else 0}},
    )

    # Calculate acceptance rate
    question = await curated_questions_collection().find_one({"_id": q_oid})
    total_sub = question.get("total_submissions", 0)
    total_acc = question.get("total_accepted", 0)
    acceptance_rate = round(total_acc / max(total_sub, 1) * 100, 1)

    return {
        "submission_id": submission["id"],
        "status": status,
        "score": score,
        "passed_count": passed_count,
        "total_cases": total_cases,
        "all_passed": all_passed,
        "execution_time": round(total_time, 3),
        "results": results,
        "acceptance_rate": acceptance_rate,
        "xp_gained": 50 if all_passed else 0,
    }


@router.get("/history")
async def get_submission_history(
    question_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    """Get user's submission history."""
    collection = submissions_collection()
    query = {"user_id": user["id"]}

    if question_id:
        query["question_id"] = question_id
    if status:
        query["status"] = status

    cursor = collection.find(query, {"results": 0}).sort("submitted_at", -1).limit(limit)
    submissions = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        submissions.append(doc)

    return {
        "submissions": submissions,
        "total": await collection.count_documents(query),
    }


@router.get("/problem/{question_id}")
async def get_problem_submissions(
    question_id: str,
    limit: int = Query(10, ge=1, le=50),
    user=Depends(get_current_user),
):
    """Get submissions for a specific problem."""
    collection = submissions_collection()
    cursor = collection.find(
        {"user_id": user["id"], "question_id": question_id}
    ).sort("submitted_at", -1).limit(limit)

    submissions = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        submissions.append(doc)

    return {
        "submissions": submissions,
        "total": await collection.count_documents({
            "user_id": user["id"],
            "question_id": question_id,
        }),
    }


@router.get("/status/{question_id}")
async def get_solved_status(question_id: str, user=Depends(get_current_user)):
    """Get solved status for a problem."""
    solved = await solved_problems_collection().find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })

    # Get submission stats
    collection = submissions_collection()
    total_submissions = await collection.count_documents({
        "user_id": user["id"],
        "question_id": question_id,
    })
    accepted_submissions = await collection.count_documents({
        "user_id": user["id"],
        "question_id": question_id,
        "status": "Accepted",
    })

    return {
        "solved": bool(solved),
        "solved_at": solved.get("solved_at").isoformat() if solved else None,
        "best_time": solved.get("best_time") if solved else None,
        "total_submissions": total_submissions,
        "accepted_submissions": accepted_submissions,
        "acceptance_rate": round(accepted_submissions / max(total_submissions, 1) * 100, 1),
    }


@router.get("/solved")
async def get_solved_problems(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get all solved problems with filtering."""
    collection = solved_problems_collection()
    query = {"user_id": user["id"]}

    pipeline = [
        {"$match": query},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
    ]

    if topic:
        pipeline.append({"$match": {"question.topic": topic}})
    if difficulty:
        pipeline.append({"$match": {"question.difficulty": difficulty}})

    pipeline.append({"$sort": {"solved_at": -1}})

    solved = []
    async for doc in collection.aggregate(pipeline):
        doc["id"] = str(doc.pop("_id"))
        doc["question_title"] = doc["question"].get("question_title", "Unknown")
        doc["topic"] = doc["question"].get("topic", "Unknown")
        doc["difficulty"] = doc["question"].get("difficulty", "medium")
        doc["company"] = doc["question"].get("company", [])
        del doc["question"]
        solved.append(doc)

    return {
        "solved": solved,
        "total": len(solved),
    }


@router.get("/stats")
async def get_submission_stats(user=Depends(get_current_user)):
    """Get comprehensive submission statistics."""
    solved_col = solved_problems_collection()
    submissions_col = submissions_collection()
    questions_col = curated_questions_collection()

    total_solved = await solved_col.count_documents({"user_id": user["id"]})
    total_submissions = await submissions_col.count_documents({"user_id": user["id"]})
    accepted = await submissions_col.count_documents({
        "user_id": user["id"],
        "status": "Accepted",
    })
    total_problems = await questions_col.count_documents({"type": "coding"})

    # Difficulty breakdown
    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {"_id": "$question.difficulty", "count": {"$sum": 1}}}
    ]
    difficulty_solved = {}
    async for doc in solved_col.aggregate(pipeline):
        difficulty_solved[doc["_id"]] = doc["count"]

    # Topic breakdown
    topic_pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {"_id": "$question.topic", "count": {"$sum": 1}}}
    ]
    topic_solved = {}
    async for doc in solved_col.aggregate(topic_pipeline):
        topic_solved[doc["_id"]] = doc["count"]

    # Language breakdown
    lang_pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$group": {"_id": "$language", "count": {"$sum": 1}}}
    ]
    language_stats = {}
    async for doc in submissions_col.aggregate(lang_pipeline):
        language_stats[doc["_id"]] = doc["count"]

    return {
        "total_solved": total_solved,
        "total_problems": total_problems,
        "completion_percentage": round(total_solved / max(total_problems, 1) * 100, 1),
        "total_submissions": total_submissions,
        "accepted_submissions": accepted,
        "acceptance_rate": round(accepted / max(total_submissions, 1) * 100, 1),
        "difficulty_solved": difficulty_solved,
        "topic_solved": topic_solved,
        "language_stats": language_stats,
    }
