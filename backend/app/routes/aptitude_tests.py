"""
Aptitude Timed Tests — Complete test system with timer, scoring, and leaderboard.
Covers Quantitative, Logical, and Verbal reasoning for campus placements.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    aptitude_tests_collection, aptitude_leaderboard_collection,
    users_collection, gamification_collection
)
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/aptitude-tests", tags=["aptitude-tests"])

# Test configurations
TEST_CONFIGS = {
    "quick": {
        "name": "Quick Test",
        "description": "5 questions, 5 minutes",
        "questions": 5,
        "time_minutes": 5,
        "xp_per_question": 5,
    },
    "standard": {
        "name": "Standard Test",
        "description": "15 questions, 15 minutes",
        "questions": 15,
        "time_minutes": 15,
        "xp_per_question": 10,
    },
    "advanced": {
        "name": "Advanced Test",
        "description": "25 questions, 30 minutes",
        "questions": 25,
        "time_minutes": 30,
        "xp_per_question": 15,
    },
    "mock": {
        "name": "Campus Mock Test",
        "description": "40 questions, 45 minutes (TCS/Infosys style)",
        "questions": 40,
        "time_minutes": 45,
        "xp_per_question": 20,
    },
}

# Category definitions
CATEGORIES = {
    "quantitative": {
        "name": "Quantitative Aptitude",
        "icon": "🔢",
        "description": "Numbers, percentages, profit/loss, time-work, speed-distance",
        "sub_categories": ["Percentages", "Profit and Loss", "Time and Work", "Speed Distance Time",
                          "Averages", "Simple Interest", "Compound Interest", "Ratios",
                          "Number Systems", "Permutations", "Probability", "Mixture and Alligation"],
    },
    "logical": {
        "name": "Logical Reasoning",
        "icon": "🧠",
        "description": "Series, coding-decoding, blood relations, seating, syllogisms",
        "sub_categories": ["Series", "Coding-Decoding", "Blood Relations", "Seating Arrangement",
                          "Syllogisms", "Puzzles", "Direction Sense", "Clock Problems"],
    },
    "verbal": {
        "name": "Verbal Ability",
        "icon": "📝",
        "description": "Synonyms, antonyms, grammar, reading comprehension",
        "sub_categories": ["Synonyms", "Antonyms", "Grammar", "Reading Comprehension",
                          "Sentence Correction", "Idioms and Phrases", "One Word Substitution"],
    },
    "mixed": {
        "name": "Mixed Aptitude",
        "icon": "🎯",
        "description": "Mix of all categories — like real campus placement tests",
        "sub_categories": [],
    },
}


@router.get("/categories")
async def get_categories():
    """Get all aptitude categories with descriptions."""
    return {"categories": CATEGORIES}


@router.get("/configurations")
async def get_test_configurations():
    """Get available test configurations."""
    return {"configurations": TEST_CONFIGS}


@router.post("/start")
async def start_aptitude_test(
    category: str = "mixed",
    config: str = "standard",
    difficulty: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Start a new aptitude test with timer."""
    if config not in TEST_CONFIGS:
        raise HTTPException(status_code=400, detail="Invalid test configuration")

    test_config = TEST_CONFIGS[config]

    # Load questions from the aptitude problems module
    from scripts.aptitude_problems import APTITUDE_PROBLEMS
    from scripts.aptitude_batch2 import APTITUDE_BATCH2
    from scripts.aptitude_batch3 import APTITUDE_BATCH3
    from scripts.aptitude_batch4 import APTITUDE_BATCH4
    from scripts.aptitude_final import APTITUDE_FINAL
    from scripts.aptitude_extra import APTITUDE_EXTRA
    from scripts.aptitude_final_batch import APTITUDE_FINAL_BATCH
    from scripts.aptitude_ultra import APTITUDE_ULTRA
    from scripts.aptitude_ultimate import APTITUDE_ULTIMATE

    # Filter questions
    available = APTITUDE_PROBLEMS.copy() + APTITUDE_BATCH2.copy() + APTITUDE_BATCH3.copy() + APTITUDE_BATCH4.copy() + APTITUDE_FINAL.copy() + APTITUDE_EXTRA.copy() + APTITUDE_FINAL_BATCH.copy() + APTITUDE_ULTRA.copy() + APTITUDE_ULTIMATE.copy()
    if category != "mixed":
        available = [q for q in available if q.get("category") == category or q.get("sub_category", "").lower() in CATEGORIES.get(category, {}).get("sub_categories", [])]

    if difficulty:
        available = [q for q in available if q.get("difficulty") == difficulty]

    # Select questions randomly
    import random
    if len(available) < test_config["questions"]:
        selected = random.sample(available, len(available))
    else:
        selected = random.sample(available, test_config["questions"])

    # Remove correct answers from questions sent to client
    questions_for_client = []
    for q in selected:
        questions_for_client.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "category": q.get("category", "quantitative"),
            "sub_category": q.get("sub_category", ""),
            "difficulty": q.get("difficulty", "medium"),
            "time_limit": q.get("time_limit", 60),
        })

    # Create test session
    now = datetime.now(timezone.utc)
    ends_at = now + timedelta(minutes=test_config["time_minutes"])

    test_doc = {
        "user_id": user["id"],
        "category": category,
        "config": config,
        "config_name": test_config["name"],
        "questions": questions_for_client,
        "question_ids": [q["id"] for q in selected],
        "answers": [],
        "status": "in_progress",
        "score": 0,
        "total_questions": len(selected),
        "correct_answers": 0,
        "time_limit_minutes": test_config["time_minutes"],
        "started_at": now,
        "ends_at": ends_at,
        "completed_at": None,
        "xp_earned": 0,
    }

    result = await aptitude_tests_collection().insert_one(test_doc)
    test_id = str(result.inserted_id)

    return {
        "test_id": test_id,
        "config": test_config,
        "category": category,
        "questions": questions_for_client,
        "total_questions": len(selected),
        "time_limit_minutes": test_config["time_minutes"],
        "ends_at": ends_at.isoformat(),
        "message": f"Test started! You have {test_config['time_minutes']} minutes.",
    }


@router.post("/{test_id}/answer")
async def submit_answer(
    test_id: str,
    question_index: int,
    answer: str,
    time_taken: Optional[float] = None,
    user=Depends(get_current_user),
):
    """Submit an answer for a specific question in the test."""
    collection = aptitude_tests_collection()

    try:
        t_oid = ObjectId(test_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    test = await collection.find_one({"_id": t_oid, "user_id": user["id"]})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    if test["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Test is not in progress")

    # Check time limit
    if datetime.now(timezone.utc) > test["ends_at"]:
        await collection.update_one({"_id": t_oid}, {"$set": {"status": "timed_out"}})
        raise HTTPException(status_code=400, detail="Time is up!")

    # Load full question data to check answer
    from scripts.aptitude_problems import APTITUDE_PROBLEMS
    from scripts.aptitude_batch2 import APTITUDE_BATCH2
    from scripts.aptitude_batch3 import APTITUDE_BATCH3
    from scripts.aptitude_batch4 import APTITUDE_BATCH4
    from scripts.aptitude_final import APTITUDE_FINAL
    from scripts.aptitude_extra import APTITUDE_EXTRA
    from scripts.aptitude_final_batch import APTITUDE_FINAL_BATCH
    from scripts.aptitude_ultra import APTITUDE_ULTRA
    from scripts.aptitude_ultimate import APTITUDE_ULTIMATE
    all_questions = APTITUDE_PROBLEMS + APTITUDE_BATCH2 + APTITUDE_BATCH3 + APTITUDE_BATCH4 + APTITUDE_FINAL + APTITUDE_EXTRA + APTITUDE_FINAL_BATCH + APTITUDE_ULTRA + APTITUDE_ULTIMATE
    question_id = test["question_ids"][question_index]
    full_question = next((q for q in all_questions if q["id"] == question_id), None)

    if not full_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check answer
    correct_answer = full_question["correct_answer"]
    is_correct = answer.strip().lower() == correct_answer.strip().lower()

    # Record answer
    answer_doc = {
        "question_index": question_index,
        "question_id": question_id,
        "answer": answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "explanation": full_question.get("explanation", ""),
        "time_taken": time_taken,
        "submitted_at": datetime.now(timezone.utc),
    }

    await collection.update_one(
        {"_id": t_oid},
        {"$push": {"answers": answer_doc}}
    )

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": full_question.get("explanation", ""),
    }


@router.post("/{test_id}/complete")
async def complete_test(test_id: str, user=Depends(get_current_user)):
    """Complete the aptitude test and get results."""
    collection = aptitude_tests_collection()

    try:
        t_oid = ObjectId(test_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    test = await collection.find_one({"_id": t_oid, "user_id": user["id"]})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    if test["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Test already completed")

    # Calculate score
    answers = test.get("answers", [])
    correct = sum(1 for a in answers if a.get("is_correct"))
    total = test["total_questions"]
    score = round(correct / max(total, 1) * 100, 1)

    # Calculate time taken
    time_taken = 0
    if test.get("started_at"):
        time_taken = (datetime.now(timezone.utc) - test["started_at"]).total_seconds()

    # Calculate XP
    test_config = TEST_CONFIGS.get(test.get("config", "standard"), TEST_CONFIGS["standard"])
    xp_earned = correct * test_config["xp_per_question"]

    # Bonus for perfect score
    if correct == total:
        xp_earned += 100

    # Update test
    await collection.update_one(
        {"_id": t_oid},
        {"$set": {
            "status": "completed",
            "score": score,
            "correct_answers": correct,
            "time_taken": round(time_taken),
            "completed_at": datetime.now(timezone.utc),
            "xp_earned": xp_earned,
        }}
    )

    # Record gamification
    await record_practice(user["id"], "aptitude", score)

    # Update leaderboard
    await update_leaderboard(user["id"], user.get("name", "User"), score, correct, total, time_taken)

    # Analyze weak areas
    weak_areas = []
    from scripts.aptitude_problems import APTITUDE_PROBLEMS
    from scripts.aptitude_batch2 import APTITUDE_BATCH2
    from scripts.aptitude_batch3 import APTITUDE_BATCH3
    from scripts.aptitude_batch4 import APTITUDE_BATCH4
    from scripts.aptitude_final import APTITUDE_FINAL
    from scripts.aptitude_extra import APTITUDE_EXTRA
    from scripts.aptitude_final_batch import APTITUDE_FINAL_BATCH
    from scripts.aptitude_ultra import APTITUDE_ULTRA
    from scripts.aptitude_ultimate import APTITUDE_ULTIMATE
    all_q = APTITUDE_PROBLEMS + APTITUDE_BATCH2 + APTITUDE_BATCH3 + APTITUDE_BATCH4 + APTITUDE_FINAL + APTITUDE_EXTRA + APTITUDE_FINAL_BATCH + APTITUDE_ULTRA + APTITUDE_ULTIMATE
    category_stats = {}
    for answer in answers:
        qid = answer.get("question_id")
        full_q = next((q for q in all_q if q["id"] == qid), None)
        if full_q:
            cat = full_q.get("sub_category", "Unknown")
            if cat not in category_stats:
                category_stats[cat] = {"correct": 0, "total": 0}
            category_stats[cat]["total"] += 1
            if answer.get("is_correct"):
                category_stats[cat]["correct"] += 1

    for cat, stats in category_stats.items():
        accuracy = stats["correct"] / max(stats["total"], 1) * 100
        if accuracy < 60:
            weak_areas.append({"category": cat, "accuracy": round(accuracy, 1), "solved": stats["correct"], "total": stats["total"]})

    return {
        "test_id": test_id,
        "score": score,
        "correct_answers": correct,
        "total_questions": total,
        "time_taken": round(time_taken),
        "xp_earned": xp_earned,
        "weak_areas": weak_areas,
        "category_stats": category_stats,
        "message": f"Test completed! Score: {score}% ({correct}/{total})",
    }


@router.get("/history")
async def get_test_history(
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    """Get user's aptitude test history."""
    collection = aptitude_tests_collection()
    query = {"user_id": user["id"], "status": "completed"}
    if category:
        query["category"] = category

    cursor = collection.find(query, {"answers": 0}).sort("completed_at", -1).limit(limit)
    tests = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        tests.append(doc)

    return {"tests": tests, "total": len(tests)}


@router.get("/stats")
async def get_aptitude_stats(user=Depends(get_current_user)):
    """Get comprehensive aptitude statistics."""
    collection = aptitude_tests_collection()

    total_tests = await collection.count_documents({"user_id": user["id"], "status": "completed"})
    pipeline = [
        {"$match": {"user_id": user["id"], "status": "completed"}},
        {"$group": {
            "_id": None,
            "avg_score": {"$avg": "$score"},
            "total_correct": {"$sum": "$correct_answers"},
            "total_questions": {"$sum": "$total_questions"},
            "best_score": {"$max": "$score"},
            "total_xp": {"$sum": "$xp_earned"},
        }}
    ]

    stats = {"avg_score": 0, "total_correct": 0, "total_questions": 0, "best_score": 0, "total_xp": 0}
    async for doc in collection.aggregate(pipeline):
        stats = {
            "avg_score": round(doc.get("avg_score", 0), 1),
            "total_correct": doc.get("total_correct", 0),
            "total_questions": doc.get("total_questions", 0),
            "best_score": round(doc.get("best_score", 0), 1),
            "total_xp": doc.get("total_xp", 0),
        }

    return {
        "total_tests": total_tests,
        **stats,
        "accuracy": round(stats["total_correct"] / max(stats["total_questions"], 1) * 100, 1),
    }


@router.get("/leaderboard")
async def get_leaderboard(
    timeframe: str = "all",  # all, weekly, monthly
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
):
    """Get aptitude test leaderboard."""
    collection = aptitude_leaderboard_collection()
    query = {}
    if timeframe == "weekly":
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        query["last_test_at"] = {"$gte": week_ago}
    elif timeframe == "monthly":
        month_ago = datetime.now(timezone.utc) - timedelta(days=30)
        query["last_test_at"] = {"$gte": month_ago}
    if category:
        query["category"] = category

    pipeline = [
        {"$match": query},
        {"$sort": {"best_score": -1, "total_tests": -1}},
        {"$limit": limit},
        {"$project": {
            "user_name": 1,
            "best_score": 1,
            "avg_score": {"$round": ["$avg_score", 1]},
            "total_tests": 1,
            "total_correct": 1,
            "accuracy": {"$round": [{"$multiply": [{"$divide": ["$total_correct", {"$max": ["$total_questions", 1]}]}, 100]}, 1]},
        }}
    ]

    leaderboard = []
    rank = 1
    async for doc in collection.aggregate(pipeline):
        doc["rank"] = rank
        leaderboard.append(doc)
        rank += 1

    return {
        "leaderboard": leaderboard,
        "timeframe": timeframe,
        "category": category,
    }


@router.get("/leaderboard/my-rank")
async def get_my_rank(user=Depends(get_current_user)):
    """Get user's current rank on the leaderboard."""
    collection = aptitude_leaderboard_collection()
    my_stats = await collection.find_one({"user_id": user["id"]})

    if not my_stats:
        return {"rank": None, "message": "No tests completed yet"}

    # Count users with better scores
    better_count = await collection.count_documents({"best_score": {"$gt": my_stats.get("best_score", 0)}})
    rank = better_count + 1

    # Total participants
    total = await collection.count_documents({})

    return {
        "rank": rank,
        "total_participants": total,
        "best_score": my_stats.get("best_score", 0),
        "avg_score": round(my_stats.get("avg_score", 0), 1),
        "total_tests": my_stats.get("total_tests", 0),
        "accuracy": round(my_stats.get("total_correct", 0) / max(my_stats.get("total_questions", 1), 1) * 100, 1),
    }


async def update_leaderboard(user_id, user_name, score, correct, total, time_taken):
    """Update leaderboard entry for a user."""
    collection = aptitude_leaderboard_collection()

    existing = await collection.find_one({"user_id": user_id})

    if existing:
        new_best = max(existing.get("best_score", 0), score)
        new_total_tests = existing.get("total_tests", 0) + 1
        new_total_correct = existing.get("total_correct", 0) + correct
        new_total_questions = existing.get("total_questions", 0) + total
        new_avg = ((existing.get("avg_score", 0) * existing.get("total_tests", 0)) + score) / new_total_tests

        await collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "user_name": user_name,
                "best_score": new_best,
                "avg_score": new_avg,
                "total_tests": new_total_tests,
                "total_correct": new_total_correct,
                "total_questions": new_total_questions,
                "last_test_at": datetime.now(timezone.utc),
            }}
        )
    else:
        await collection.insert_one({
            "user_id": user_id,
            "user_name": user_name,
            "best_score": score,
            "avg_score": score,
            "total_tests": 1,
            "total_correct": correct,
            "total_questions": total,
            "last_test_at": datetime.now(timezone.utc),
        })
