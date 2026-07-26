from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection, coding_challenges_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_coding_challenge
from app.services.coding_engine import CodingEngine
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.services.code_executor import CodeExecutionEngine
from app.services.gamification import record_practice
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/coding", tags=["coding"])
settings = get_settings()
code_engine = CodeExecutionEngine()
coding_engine = CodingEngine()

TOPICS = {
    "arrays": "Arrays & Strings",
    "linked-lists": "Linked Lists",
    "trees": "Trees & Graphs",
    "dynamic-programming": "Dynamic Programming",
    "sorting": "Sorting & Searching",
    "hashing": "Hash Maps & Sets",
    "stacks-queues": "Stacks & Queues",
    "recursion": "Recursion & Backtracking",
    "graphs": "Graph Algorithms",
    "system-design": "System Design Coding",
}

COMPANIES = ["google", "amazon", "meta", "microsoft", "tcs", "infosys", "wipro", "uber"]


class StartCodingChallenge(BaseModel):
    difficulty: str = "medium"
    topic: str = "arrays"
    language: str = "python"
    company: str = ""
    role: str = "SDE"


class SubmitCodingAnswer(BaseModel):
    challenge_id: str
    code: str
    time_taken: int = 0


class GetHintRequest(BaseModel):
    challenge_id: str
    hint_level: int = 1


class InterviewerReviewRequest(BaseModel):
    challenge_id: str
    code: str
    language: str = "python"


@router.get("/topics")
async def get_topics():
    return {
        "topics": [
            {"id": key, "name": name}
            for key, name in TOPICS.items()
        ],
        "companies": COMPANIES,
    }


@router.post("/start")
async def start_coding_challenge(req: StartCodingChallenge, user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)

    challenge_doc = {
        "user_id": user["id"],
        "difficulty": req.difficulty,
        "topic": req.topic,
        "language": req.language,
        "company": req.company,
        "role": req.role,
        "user_code": "",
        "status": "in_progress",
        "score": 0,
        "hints_used": 0,
        "created_at": datetime.now(timezone.utc),
    }

    if req.company and req.company.lower() in COMPANIES:
        result_data = await coding_engine.generate_challenge_with_hints(
            company=req.company.lower(),
            role=req.role,
            difficulty=req.difficulty,
        )
        challenge = result_data.get("challenge", {})
        challenge["hints_structured"] = result_data.get("hints", {})
        challenge["solution_approach"] = result_data.get("solution_approach", "")
        challenge["time_limit_seconds"] = result_data.get("time_limit", 2700)
    else:
        challenge = await generate_coding_challenge(req.difficulty, req.topic, req.language)

    challenge_doc["challenge"] = challenge
    result = await coding_challenges_collection.insert_one(challenge_doc)

    return {
        "challenge_id": str(result.inserted_id),
        "title": challenge.get("title", ""),
        "description": challenge.get("description", ""),
        "examples": challenge.get("examples", []),
        "constraints": challenge.get("constraints", []),
        "hints": challenge.get("hints", []),
        "time_limit": challenge.get("time_limit_seconds", 1800),
        "difficulty": req.difficulty,
        "topic": req.topic,
        "company": req.company,
        "solution_approach": challenge.get("solution_approach", ""),
    }


@router.post("/submit")
async def submit_coding_answer(req: SubmitCodingAnswer, user=Depends(get_current_user)):
    try:
        challenge = await coding_challenges_collection.find_one({"_id": ObjectId(req.challenge_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if challenge["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    test_cases = challenge.get("challenge", {}).get("test_cases", [])

    test_results = None
    score = 0
    if test_cases and req.code.strip():
        try:
            test_results = await code_engine.execute_against_test_cases(
                req.code, challenge.get("language", "python"), test_cases
            )
            score = test_results.get("score", 0)
        except Exception:
            test_results = None

    interviewer_eval = None
    if req.code.strip() and challenge.get("company"):
        try:
            problem_desc = f"{challenge.get('challenge', {}).get('title', '')}\n{challenge.get('challenge', {}).get('description', '')}"
            interviewer_eval = await coding_engine.evaluate_as_interviewer(
                req.code, challenge.get("language", "python"), problem_desc,
            )
        except Exception:
            interviewer_eval = None

    status = "completed" if score >= 80 else "submitted"

    await coding_challenges_collection.update_one(
        {"_id": ObjectId(req.challenge_id)},
        {"$set": {"user_code": req.code, "time_taken": req.time_taken, "status": status, "score": score}},
    )

    gamification_result = await record_practice(user["id"], "coding", score)

    return {
        "status": status,
        "challenge_id": req.challenge_id,
        "test_results": test_results,
        "score": score,
        "interviewer_eval": interviewer_eval,
        "xp_gained": gamification_result.get("xp_gained", 0),
        "level": gamification_result.get("level", 1),
        "new_badges": gamification_result.get("new_badges", []),
        "streak": gamification_result.get("new_streak", 0),
    }


@router.post("/hint")
async def get_hint(req: GetHintRequest, user=Depends(get_current_user)):
    try:
        challenge = await coding_challenges_collection.find_one({"_id": ObjectId(req.challenge_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if challenge["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    problem_desc = f"{challenge.get('challenge', {}).get('title', '')}\n{challenge.get('challenge', {}).get('description', '')}"
    current_code = challenge.get("user_code", "")

    level = max(1, min(3, req.hint_level))

    hints_structured = challenge.get("challenge", {}).get("hints_structured", {})
    if hints_structured and f"level_{level}" in hints_structured:
        hint_text = hints_structured[f"level_{level}"]
    else:
        hint_result = await coding_engine.get_hint(problem_desc, current_code, level)
        hint_text = hint_result.get("hint", "Try thinking about the approach differently.")

    await coding_challenges_collection.update_one(
        {"_id": ObjectId(req.challenge_id)},
        {"$inc": {"hints_used": 1}},
    )

    return {
        "hint": hint_text,
        "level": level,
        "next_level_available": level < 3,
        "hints_used": challenge.get("hints_used", 0) + 1,
    }


@router.post("/interviewer-review")
async def interviewer_review(req: InterviewerReviewRequest, user=Depends(get_current_user)):
    try:
        challenge = await coding_challenges_collection.find_one({"_id": ObjectId(req.challenge_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if challenge["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    problem_desc = f"{challenge.get('challenge', {}).get('title', '')}\n{challenge.get('challenge', {}).get('description', '')}"

    eval_result = await coding_engine.evaluate_as_interviewer(
        req.code, req.language, problem_desc,
    )

    return eval_result


@router.get("/{challenge_id}/solution")
async def get_solution(challenge_id: str, user=Depends(get_current_user)):
    try:
        challenge = await coding_challenges_collection.find_one({"_id": ObjectId(challenge_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid challenge ID")

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    if challenge["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    challenge_data = challenge.get("challenge", {})

    return {
        "title": challenge_data.get("title", ""),
        "description": challenge_data.get("description", ""),
        "examples": challenge_data.get("examples", []),
        "test_cases": challenge_data.get("test_cases", []),
        "hints": challenge_data.get("hints", []),
        "follow_up": challenge_data.get("follow_up", ""),
        "solution_approach": challenge_data.get("solution_approach", ""),
        "user_code": challenge.get("user_code", ""),
        "company": challenge.get("company", ""),
    }


@router.get("/history")
async def get_coding_history(user=Depends(get_current_user)):
    cursor = coding_challenges_collection.find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(20)

    challenges = []
    async for doc in cursor:
        challenges.append({
            "id": str(doc["_id"]),
            "title": doc.get("challenge", {}).get("title", ""),
            "difficulty": doc.get("difficulty", ""),
            "topic": doc.get("topic", ""),
            "company": doc.get("company", ""),
            "status": doc.get("status", ""),
            "score": doc.get("score", 0),
            "hints_used": doc.get("hints_used", 0),
            "created_at": doc.get("created_at"),
        })

    return {"challenges": challenges}
