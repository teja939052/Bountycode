"""
Timed Mock Interview routes — real interview simulation with countdown timer.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, question_answers_collection,
    solved_problems_collection, users_collection
)
from app.services.ai import chat_completion, parse_json
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/mock-interview", tags=["mock-interview"])

# Interview configurations by company
COMPANY_CONFIGS = {
    "google": {
        "total_questions": 5,
        "time_limit_minutes": 45,
        "difficulty_distribution": {"easy": 1, "medium": 2, "hard": 2},
        "focus_areas": ["Arrays", "Dynamic Programming", "Graphs", "Trees"],
        "interview_style": "Google-style: Focus on optimal solutions, follow-up questions, and system design thinking.",
    },
    "amazon": {
        "total_questions": 5,
        "time_limit_minutes": 45,
        "difficulty_distribution": {"easy": 1, "medium": 3, "hard": 1},
        "focus_areas": ["Arrays", "Linked Lists", "Trees", "Dynamic Programming"],
        "interview_style": "Amazon-style: Leadership principles, scalable solutions, and real-world applications.",
    },
    "microsoft": {
        "total_questions": 5,
        "time_limit_minutes": 40,
        "difficulty_distribution": {"easy": 2, "medium": 2, "hard": 1},
        "focus_areas": ["Arrays", "Strings", "Trees", "Graphs"],
        "interview_style": "Microsoft-style: Clean code, edge cases, and efficient algorithms.",
    },
    "tcs": {
        "total_questions": 8,
        "time_limit_minutes": 30,
        "difficulty_distribution": {"easy": 4, "medium": 3, "hard": 1},
        "focus_areas": ["Arrays", "Strings", "Basic Algorithms"],
        "interview_style": "TCS-style: Focus on fundamentals, aptitude, and basic coding.",
    },
    "generic": {
        "total_questions": 5,
        "time_limit_minutes": 45,
        "difficulty_distribution": {"easy": 1, "medium": 3, "hard": 1},
        "focus_areas": ["Arrays", "Strings", "Trees", "Dynamic Programming", "Graphs"],
        "interview_style": "Standard coding interview with mixed difficulty.",
    },
}


@router.post("/start")
async def start_mock_interview(
    company: str = "generic",
    difficulty: str = "mixed",
    user=Depends(get_current_user),
):
    """Start a timed mock interview with questions selected by company/difficulty."""
    config = COMPANY_CONFIGS.get(company.lower(), COMPANY_CONFIGS["generic"])
    collection = curated_questions_collection()

    # Build query based on config
    query = {"type": "coding"}
    if difficulty != "mixed":
        query["difficulty"] = difficulty

    # Get questions from focus areas
    if config["focus_areas"]:
        query["$or"] = [{"topic": {"$in": config["focus_areas"]}}]

    # Get questions with randomness
    pipeline = [
        {"$match": query},
        {"$sample": {"size": config["total_questions"]}},
        {"$project": {
            "question_title": 1,
            "statement": 1,
            "difficulty": 1,
            "topics": 1,
            "company": 1,
            "visible_test_cases": 1,
            "constraints": 1,
            "examples": 1,
            "hints": 1,
        }}
    ]

    questions = []
    async for q in collection.aggregate(pipeline):
        q["id"] = str(q.pop("_id"))
        questions.append(q)

    if not questions:
        # Fallback: get any coding questions
        fallback_query = {"type": "coding"}
        if difficulty != "mixed":
            fallback_query["difficulty"] = difficulty
        cursor = collection.find(fallback_query).limit(config["total_questions"])
        async for q in cursor:
            q["id"] = str(q.pop("_id"))
            questions.append(q)

    # Create interview session
    session = {
        "user_id": user["id"],
        "company": company,
        "config": config,
        "questions": questions,
        "answers": [],
        "current_question": 0,
        "status": "in_progress",
        "started_at": datetime.now(timezone.utc),
        "ends_at": datetime.now(timezone.utc) + timedelta(minutes=config["time_limit_minutes"]),
        "time_limit_minutes": config["time_limit_minutes"],
        "total_score": 0,
    }

    # Save to DB
    from app.database import get_db
    db = get_db()
    result = await db["mock_interviews"].insert_one(session)
    session_id = str(result.inserted_id)

    return {
        "session_id": session_id,
        "company": company,
        "time_limit_minutes": config["time_limit_minutes"],
        "ends_at": session["ends_at"].isoformat(),
        "total_questions": len(questions),
        "interview_style": config["interview_style"],
        "questions": questions,
    }


@router.post("/{session_id}/submit")
async def submit_answer(
    session_id: str,
    question_index: int,
    code: str,
    language: str,
    user=Depends(get_current_user),
):
    """Submit an answer for a question in the mock interview."""
    from app.database import get_db
    db = get_db()

    try:
        session = await db["mock_interviews"].find_one({
            "_id": ObjectId(session_id),
            "user_id": user["id"],
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Interview is not in progress")

    # Check if time is up
    if datetime.now(timezone.utc) > session["ends_at"]:
        await db["mock_interviews"].update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"status": "timed_out"}}
        )
        raise HTTPException(status_code=400, detail="Time is up!")

    # Get question
    if question_index >= len(session["questions"]):
        raise HTTPException(status_code=400, detail="Invalid question index")

    question = session["questions"][question_index]

    # Execute code against test cases
    from app.services.code_executor import CodeExecutionEngine
    engine = CodeExecutionEngine()

    visible_cases = question.get("visible_test_cases", [])
    results = []
    passed_count = 0

    for case in visible_cases:
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
        results.append({
            "passed": passed,
            "input": case.get("input", ""),
            "expected": case.get("expected", ""),
            "actual": actual if passed else "[FAILED]",
        })

    score = round(passed_count / len(visible_cases) * 100, 1) if visible_cases else 0

    # Update session
    answer_record = {
        "question_index": question_index,
        "question_title": question["question_title"],
        "code": code,
        "language": language,
        "score": score,
        "passed_count": passed_count,
        "total_cases": len(visible_cases),
        "results": results,
        "submitted_at": datetime.now(timezone.utc),
    }

    await db["mock_interviews"].update_one(
        {"_id": ObjectId(session_id)},
        {"$push": {"answers": answer_record}}
    )

    # Check if all questions answered
    total_answered = len(session.get("answers", [])) + 1
    finished = total_answered >= len(session["questions"])

    if finished:
        # Calculate final score
        total_score = sum(a["score"] for a in session.get("answers", [])) / len(session["questions"])
        await db["mock_interviews"].update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"status": "completed", "total_score": total_score, "completed_at": datetime.now(timezone.utc)}}
        )

        # Record gamification
        await record_practice(user["id"], "mock_interview", total_score)

    return {
        "score": score,
        "passed_count": passed_count,
        "total_cases": len(visible_cases),
        "results": results,
        "finished": finished,
        "questions_answered": total_answered,
        "total_questions": len(session["questions"]),
    }


@router.get("/{session_id}/status")
async def get_interview_status(session_id: str, user=Depends(get_current_user)):
    """Get current interview status including time remaining."""
    from app.database import get_db
    db = get_db()

    try:
        session = await db["mock_interviews"].find_one({
            "_id": ObjectId(session_id),
            "user_id": user["id"],
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    now = datetime.now(timezone.utc)
    ends_at = session["ends_at"]
    time_remaining = max(0, (ends_at - now).total_seconds())
    is_timed_out = now > ends_at and session["status"] == "in_progress"

    if is_timed_out:
        await db["mock_interviews"].update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"status": "timed_out"}}
        )

    return {
        "session_id": session_id,
        "status": session["status"],
        "time_remaining_seconds": int(time_remaining),
        "ends_at": ends_at.isoformat(),
        "questions_answered": len(session.get("answers", [])),
        "total_questions": len(session["questions"]),
        "total_score": session.get("total_score", 0),
    }


@router.get("/history")
async def get_interview_history(user=Depends(get_current_user)):
    """Get user's mock interview history."""
    from app.database import get_db
    db = get_db()

    cursor = db["mock_interviews"].find(
        {"user_id": user["id"]},
        {"answers.code": 0}
    ).sort("started_at", -1).limit(20)

    interviews = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        interviews.append(doc)

    return {"interviews": interviews}
