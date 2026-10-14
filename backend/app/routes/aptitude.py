from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any

from app.middleware.auth import get_current_user
from app.database import aptitude_tests_collection
from app.data.aptitude_question_bank import (
    get_categories,
    get_random_questions,
    get_question_by_id,
    get_total_count,
)
from app.services.gamification import record_practice
from app.services.usage import check_and_reset_monthly_usage

import random

router = APIRouter(prefix="/api/v1/aptitude", tags=["aptitude"])


@router.get("/categories")
async def get_aptitude_categories(user=Depends(get_current_user)):
    categories = get_categories()
    return {"categories": [{"id": c, "name": c.replace("_", " ").title()} for c in categories]}


@router.post("/start")
async def start_aptitude_test(
    category: str = Query(...),
    difficulty: str = Query("medium"),
    question_count: int = Query(20),
    user=Depends(get_current_user),
):
    allowed, reset_info = await check_and_reset_monthly_usage(
        user_id=user["id"],
        feature="aptitude_tests",
    )
    if not allowed:
        raise HTTPException(status_code=429, detail="Monthly aptitude test limit reached.")

    questions = get_random_questions(category, count=question_count)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this category.")

    test_doc = {
        "user_id": user["id"],
        "category": category,
        "difficulty": difficulty,
        "questions": questions,
        "answers": {},
        "score": None,
        "status": "in_progress",
        "created_at": datetime.now(timezone.utc),
        "completed_at": None,
    }
    result = await aptitude_tests_collection.insert_one(test_doc)
    test_doc["id"] = str(result.inserted_id)
    test_doc.pop("_id", None)
    return test_doc


@router.post("/answer")
async def submit_aptitude_answer(
    payload: Dict[str, Any],
    user=Depends(get_current_user),
):
    test_id = payload.get("test_id")
    question_index = payload.get("question_index")
    answer = payload.get("answer")

    if test_id is None or question_index is None or answer is None:
        raise HTTPException(status_code=400, detail="test_id, question_index, and answer are required.")

    test = await aptitude_tests_collection.find_one({"_id": __import__("bson").ObjectId(test_id), "user_id": user["id"]})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found.")

    if test.get("status") != "in_progress":
        raise HTTPException(status_code=400, detail="Test is not in progress.")

    questions = test.get("questions", [])
    if question_index < 0 or question_index >= len(questions):
        raise HTTPException(status_code=400, detail="Invalid question index.")

    question = questions[question_index]
    correct = question.get("correct_index")
    is_correct = False
    if isinstance(correct, int):
        is_correct = int(answer) == correct
    elif isinstance(correct, str):
        is_correct = str(answer) == correct

    answers = test.get("answers", {})
    answers[str(question_index)] = {
        "answer": answer,
        "correct": is_correct,
        "question_id": question.get("id"),
    }

    await aptitude_tests_collection.update_one(
        {"_id": test["_id"]},
        {"$set": {"answers": answers}},
    )

    return {"correct": is_correct, "score": question.get("explanation")}


@router.post("/{test_id}/complete")
async def complete_aptitude_test(
    test_id: str,
    payload: Dict[str, Any],
    user=Depends(get_current_user),
):
    test = await aptitude_tests_collection.find_one({"_id": __import__("bson").ObjectId(test_id), "user_id": user["id"]})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found.")

    if test.get("status") == "completed":
        raise HTTPException(status_code=400, detail="Test already completed.")

    answers = test.get("answers", {})
    questions = test.get("questions", [])
    total = len(questions)
    correct_count = 0
    for idx, q in enumerate(questions):
        ans = answers.get(str(idx))
        if ans and ans.get("correct"):
            correct_count += 1

    score = round((correct_count / total) * 100, 2) if total else 0

    now = datetime.now(timezone.utc)
    await aptitude_tests_collection.update_one(
        {"_id": test["_id"]},
        {
            "$set": {
                "status": "completed",
                "score": score,
                "completed_at": now,
                "total_questions": total,
                "correct_count": correct_count,
            }
        },
    )

    await record_practice(
        user_id=user["id"],
        activity_type="aptitude",
        world_id="aptitude_gauntlet",
        score=score,
        max_score=100,
        metadata={"category": test.get("category"), "difficulty": test.get("difficulty")},
    )

    try:
        from app.services.study_engine import record_activity as record_study_activity
        from app.services.skill_taxonomy import canonical_skill_id
        skill_id = canonical_skill_id(f"aptitude.{test.get('category', 'general')}") or f"aptitude.{test.get('category', 'general')}"
        await record_study_activity(
            user_id=user["id"],
            activity={
                "type": "practice",
                "skill_id": skill_id,
                "passed": score >= 60,
                "score": score,
                "time_spent": 0,
                "idempotency_key": f"aptitude:{test_id}:{user['id']}",
            },
            role=user.get("role") or user.get("target_role") or "sde",
        )
    except Exception:
        pass

    updated = await aptitude_tests_collection.find_one({"_id": test["_id"]})
    updated["id"] = str(updated.pop("_id"))
    return updated


@router.get("/history")
async def get_aptitude_history(user=Depends(get_current_user)):
    cursor = aptitude_tests_collection.find({"user_id": user["id"], "status": "completed"}).sort("completed_at", -1).limit(20)
    history = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        history.append(doc)
    return history


@router.get("/{test_id}/result")
async def get_aptitude_result(test_id: str, user=Depends(get_current_user)):
    doc = await aptitude_tests_collection.find_one({"_id": __import__("bson").ObjectId(test_id), "user_id": user["id"]})
    if not doc:
        raise HTTPException(status_code=404, detail="Result not found.")
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("/theory-for/{category}")
async def get_theory_for_category(category: str, user=Depends(get_current_user)):
    questions = get_random_questions(category, count=10)
    topics = []
    seen = set()
    for q in questions:
        topic = q.get("topic") or category
        if topic in seen:
            continue
        seen.add(topic)
        topics.append({
            "id": topic,
            "title": topic.replace("_", " ").title(),
            "category": category,
            "definition": q.get("explanation", ""),
            "formulas": [],
            "worked_example": {
                "problem": q.get("question", ""),
                "solution": q.get("explanation", ""),
            },
            "triggers": q.get("companies", []),
            "pitfalls": [],
            "practice_category": category,
        })
    return {"category": category, "topics": topics}
