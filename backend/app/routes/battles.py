"""
1v1 Real-Time Battles — Challenge friends or get matched with opponents.
Socket.io-powered live coding battles with scoring and leaderboards.
"""
from datetime import datetime, timezone, timedelta
import random
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, solved_problems_collection,
    battles_collection, users_collection
)

router = APIRouter(prefix="/api/battles", tags=["battles"])

# Battle configuration
BATTLE_CONFIGS = {
    "quick": {
        "name": "Quick Battle",
        "description": "1 problem, 10 minutes",
        "problems": 1,
        "time_minutes": 10,
        "difficulty": "mixed",
        "xp_multiplier": 1.5,
    },
    "standard": {
        "name": "Standard Battle",
        "description": "3 problems, 30 minutes",
        "problems": 3,
        "time_minutes": 30,
        "difficulty": "mixed",
        "xp_multiplier": 2.0,
    },
    "marathon": {
        "name": "Marathon Battle",
        "description": "5 problems, 60 minutes",
        "problems": 5,
        "time_minutes": 60,
        "difficulty": "mixed",
        "xp_multiplier": 3.0,
    },
    "speed": {
        "name": "Speed Round",
        "description": "2 problems, 5 minutes",
        "problems": 2,
        "time_minutes": 5,
        "difficulty": "easy",
        "xp_multiplier": 2.5,
    },
}

# Penalty presets
PENALTY_PRESETS = {
    "standard": {"wrong_answer": 5, "compile_error": 2, "tle": 3},
    "strict": {"wrong_answer": 10, "compile_error": 5, "tle": 5},
    "relaxed": {"wrong_answer": 2, "compile_error": 1, "tle": 1},
}


@router.post("/create")
async def create_battle(
    config: str = "standard",
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Create a new battle room."""
    if config not in BATTLE_CONFIGS:
        raise HTTPException(status_code=400, detail="Invalid battle config")

    battle_config = BATTLE_CONFIGS[config]

    # Select problems
    collection = curated_questions_collection()
    query = {"type": "coding"}
    if difficulty:
        query["difficulty"] = difficulty
    if topic:
        query["topic"] = topic

    pipeline = [
        {"$match": query},
        {"$sample": {"size": battle_config["problems"]}},
        {"$project": {
            "question_title": 1,
            "difficulty": 1,
            "topic": 1,
            "visible_test_cases": 1,
            "constraints": 1,
            "examples": 1,
        }}
    ]

    problems = []
    async for doc in collection.aggregate(pipeline):
        doc["id"] = str(doc.pop("_id"))
        problems.append(doc)

    if len(problems) < battle_config["problems"]:
        raise HTTPException(status_code=400, detail="Not enough problems available")

    # Create battle
    battle = {
        "creator_id": user["id"],
        "creator_name": user.get("name", "Player 1"),
        "opponent_id": None,
        "opponent_name": None,
        "config": config,
        "config_name": battle_config["name"],
        "problems": problems,
        "penalty": PENALTY_PRESETS["standard"],
        "status": "waiting",
        "started_at": None,
        "ends_at": None,
        "time_limit_minutes": battle_config["time_minutes"],
        "xp_multiplier": battle_config["xp_multiplier"],
        "scores": {},
        "submissions": {},
        "chat": [],
        "winner": None,
        "created_at": datetime.now(timezone.utc),
    }

    result = await battles_collection().insert_one(battle)
    battle["id"] = str(result.inserted_id)

    # Generate invite code
    invite_code = battle["id"][:8].upper()
    await battles_collection().update_one(
        {"_id": result.inserted_id},
        {"$set": {"invite_code": invite_code}}
    )
    battle["invite_code"] = invite_code

    return {
        "battle": battle,
        "message": f"Battle created! Share invite code: {invite_code}",
    }


@router.post("/join/{invite_code}")
async def join_battle(invite_code: str, user=Depends(get_current_user)):
    """Join a battle using invite code."""
    collection = battles_collection()

    battle = await collection.find_one({"invite_code": invite_code.upper()})
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    if battle["status"] != "waiting":
        raise HTTPException(status_code=400, detail="Battle already started or finished")

    if battle["creator_id"] == user["id"]:
        raise HTTPException(status_code=400, detail="Cannot join your own battle")

    # Join the battle
    await collection.update_one(
        {"_id": battle["_id"]},
        {"$set": {
            "opponent_id": user["id"],
            "opponent_name": user.get("name", "Player 2"),
            "status": "ready",
        }}
    )

    return {
        "battle_id": str(battle["_id"]),
        "message": "Joined battle! Both players are ready.",
    }


@router.post("/matchmaking")
async def quick_match(user=Depends(get_current_user)):
    """Find a random opponent for quick match."""
    collection = battles_collection()

    # Find waiting battles
    waiting = await collection.find_one({
        "status": "waiting",
        "creator_id": {"$ne": user["id"]},
    })

    if waiting:
        # Join existing battle
        await collection.update_one(
            {"_id": waiting["_id"]},
            {"$set": {
                "opponent_id": user["id"],
                "opponent_name": user.get("name", "Player 2"),
                "status": "ready",
            }}
        )
        return {
            "battle_id": str(waiting["_id"]),
            "matched": True,
            "opponent": waiting.get("creator_name", "Player 1"),
            "config": waiting.get("config", "standard"),
        }
    else:
        # Create new battle and wait
        config = BATTLE_CONFIGS["standard"]
        collection2 = curated_questions_collection()
        pipeline = [
            {"$match": {"type": "coding"}},
            {"$sample": {"size": config["problems"]}},
            {"$project": {"question_title": 1, "difficulty": 1, "topic": 1, "visible_test_cases": 1, "constraints": 1, "examples": 1}}
        ]
        problems = []
        async for doc in collection2.aggregate(pipeline):
            doc["id"] = str(doc.pop("_id"))
            problems.append(doc)

        battle = {
            "creator_id": user["id"],
            "creator_name": user.get("name", "Player 1"),
            "opponent_id": None,
            "opponent_name": None,
            "config": "standard",
            "config_name": "Standard Battle",
            "problems": problems,
            "penalty": PENALTY_PRESETS["standard"],
            "status": "waiting",
            "started_at": None,
            "ends_at": None,
            "time_limit_minutes": config["time_minutes"],
            "xp_multiplier": config["xp_multiplier"],
            "scores": {},
            "submissions": {},
            "chat": [],
            "winner": None,
            "created_at": datetime.now(timezone.utc),
        }

        result = await collection.insert_one(battle)
        invite_code = str(result.inserted_id)[:8].upper()
        await collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"invite_code": invite_code}}
        )

        return {
            "battle_id": str(result.inserted_id),
            "matched": False,
            "message": "Waiting for opponent... Share invite code: " + invite_code,
            "invite_code": invite_code,
        }


@router.post("/start/{battle_id}")
async def start_battle(battle_id: str, user=Depends(get_current_user)):
    """Start a battle (both players must be ready)."""
    collection = battles_collection()

    try:
        b_oid = ObjectId(battle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid battle ID")

    battle = await collection.find_one({"_id": b_oid})
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    if battle["status"] != "ready":
        raise HTTPException(status_code=400, detail="Battle not ready to start")

    if user["id"] not in (battle["creator_id"], battle["opponent_id"]):
        raise HTTPException(status_code=403, detail="Not a participant in this battle")

    # Start the battle
    now = datetime.now(timezone.utc)
    ends_at = now + timedelta(minutes=battle["time_limit_minutes"])

    await collection.update_one(
        {"_id": b_oid},
        {"$set": {
            "status": "active",
            "started_at": now,
            "ends_at": ends_at,
            "scores": {
                battle["creator_id"]: {"score": 0, "penalty": 0, "solved": []},
                battle["opponent_id"]: {"score": 0, "penalty": 0, "solved": []},
            }
        }}
    )

    return {
        "battle_id": battle_id,
        "status": "active",
        "ends_at": ends_at.isoformat(),
        "time_limit_minutes": battle["time_limit_minutes"],
    }


@router.post("/submit/{battle_id}")
async def submit_battle_code(
    battle_id: str,
    problem_index: int,
    code: str,
    language: str,
    user=Depends(get_current_user),
):
    """Submit code during a battle."""
    from app.services.code_executor import CodeExecutionEngine

    engine = CodeExecutionEngine()
    collection = battles_collection()

    try:
        b_oid = ObjectId(battle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid battle ID")

    battle = await collection.find_one({"_id": b_oid})
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    if battle["status"] != "active":
        raise HTTPException(status_code=400, detail="Battle is not active")

    if user["id"] not in (battle["creator_id"], battle["opponent_id"]):
        raise HTTPException(status_code=403, detail="Not a participant")

    # Check time limit
    if datetime.now(timezone.utc) > battle["ends_at"]:
        await collection.update_one({"_id": b_oid}, {"$set": {"status": "finished"}})
        raise HTTPException(status_code=400, detail="Battle time is up!")

    # Get problem
    if problem_index >= len(battle["problems"]):
        raise HTTPException(status_code=400, detail="Invalid problem index")

    problem = battle["problems"][problem_index]

    # Execute code against test cases
    hidden_cases = problem.get("visible_test_cases", [])
    results = []
    passed_count = 0
    total_cases = len(hidden_cases)

    for case in hidden_cases:
        result = await engine.execute_code(code, language, case.get("input", ""), timeout=5)
        if result["success"]:
            actual = result["stdout"].strip()
            expected = case.get("expected", "").strip()
            passed = actual == expected
            if passed:
                passed_count += 1
        else:
            actual = result.get("error", "Failed")
            passed = False
        results.append({"passed": passed, "actual": actual})

    all_passed = passed_count == total_cases
    score = round(passed_count / total_cases * 100, 1) if total_cases > 0 else 0

    # Calculate penalty
    penalty = 0
    if not all_passed:
        penalty = battle["penalty"].get("wrong_answer", 5)

    # Update scores
    user_id = user["id"]
    current_scores = battle.get("scores", {}).get(user_id, {"score": 0, "penalty": 0, "solved": []})
    current_scores["score"] += score
    current_scores["penalty"] += penalty
    if all_passed and problem_index not in current_scores["solved"]:
        current_scores["solved"].append(problem_index)

    await collection.update_one(
        {"_id": b_oid},
        {"$set": {f"scores.{user_id}": current_scores}}
    )

    # Record submission
    submission = {
        "user_id": user_id,
        "problem_index": problem_index,
        "code": code,
        "language": language,
        "all_passed": all_passed,
        "score": score,
        "penalty": penalty,
        "results": results,
        "submitted_at": datetime.now(timezone.utc),
    }

    await collection.update_one(
        {"_id": b_oid},
        {"$push": {f"submissions.{user_id}": submission}}
    )

    # Check if battle should end (all problems solved by both)
    all_problems_solved = True
    for pid in (battle["creator_id"], battle["opponent_id"]):
        scores = battle.get("scores", {}).get(pid, {})
        if len(scores.get("solved", [])) < len(battle["problems"]):
            all_problems_solved = False
            break

    if all_problems_solved:
        # Determine winner
        creator_score = battle["scores"].get(battle["creator_id"], {}).get("score", 0)
        opponent_score = battle["scores"].get(battle["opponent_id"], {}).get("score", 0)
        winner = battle["creator_id"] if creator_score >= opponent_score else battle["opponent_id"]

        await collection.update_one(
            {"_id": b_oid},
            {"$set": {"status": "finished", "winner": winner}}
        )

    return {
        "all_passed": all_passed,
        "score": score,
        "penalty": penalty,
        "total_cases": total_cases,
        "passed_count": passed_count,
        "results": results,
    }


@router.get("/status/{battle_id}")
async def get_battle_status(battle_id: str, user=Depends(get_current_user)):
    """Get current battle status."""
    collection = battles_collection()

    try:
        b_oid = ObjectId(battle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid battle ID")

    battle = await collection.find_one({"_id": b_oid})
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    if user["id"] not in (battle["creator_id"], battle["opponent_id"]):
        raise HTTPException(status_code=403, detail="Not a participant")

    # Check if time is up
    if battle["status"] == "active" and datetime.now(timezone.utc) > battle["ends_at"]:
        await collection.update_one({"_id": b_oid}, {"$set": {"status": "finished"}})
        battle["status"] = "finished"

    # Time remaining
    time_remaining = 0
    if battle["status"] == "active" and battle["ends_at"]:
        time_remaining = max(0, (battle["ends_at"] - datetime.now(timezone.utc)).total_seconds())

    return {
        "battle_id": battle_id,
        "status": battle["status"],
        "config": battle.get("config_name", "Standard"),
        "creator": battle.get("creator_name"),
        "opponent": battle.get("opponent_name"),
        "problems_count": len(battle.get("problems", [])),
        "scores": battle.get("scores", {}),
        "time_remaining": int(time_remaining),
        "winner": battle.get("winner"),
    }


@router.get("/history")
async def get_battle_history(user=Depends(get_current_user)):
    """Get user's battle history."""
    collection = battles_collection()
    cursor = collection.find({
        "$or": [
            {"creator_id": user["id"]},
            {"opponent_id": user["id"]},
        ]
    }).sort("created_at", -1).limit(20)

    battles = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        doc["is_creator"] = doc["creator_id"] == user["id"]
        doc["opponent_name"] = doc.get("opponent_name") if doc["is_creator"] else doc.get("creator_name")
        battles.append(doc)

    return {"battles": battles}


@router.get("/leaderboard")
async def get_battle_leaderboard(limit: int = Query(20, ge=1, le=100)):
    """Get battle leaderboard."""
    collection = battles_collection()

    pipeline = [
        {"$match": {"status": "finished", "winner": {"$ne": None}}},
        {"$group": {
            "_id": "$winner",
            "wins": {"$sum": 1}
        }},
        {"$sort": {"wins": -1}},
        {"$limit": limit},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {
            "user_name": "$user.name",
            "wins": 1,
        }}
    ]

    leaderboard = []
    async for doc in collection.aggregate(pipeline):
        leaderboard.append(doc)

    return {"leaderboard": leaderboard}
