"""Campus Connect — college-focused 1v1 duels with invite economy + tournaments."""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from app.middleware.auth import get_current_user
from app.database import get_db, gamification_collection, users_collection
import logging, secrets, asyncio

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/campus-connect", tags=["campus-connect"])

# ┃ Indian college list for scoped matchmaking
INDIAN_COLLEGES = [
    "IIT Bombay", "IIT Delhi", "IIT Madras", "IIT Kharagpur", "IIT Kanpur",
    "IIT Roorkee", "IIT Guwahati", "IIT Ropar", "IIT Mandi", "IIT Indore",
    "IIT Gandhinagar", "IIT Hyderabad", "IIT Jodhpur", "IIT Patna", "IIT Bhubaneswar",
    "IIT Dhanbad", "IIT Bhilai", "IIT Bhubaneswar", "IIT Goa", "IIT Jammu",
    "NIT Trichy", "NIT Surathkal", "NIT Warangal", "NIT Calicut", "NIT Surat",
    "NIT Rourkela", "NIT Kurukshetra", "NIT Jamshedpur", "NIT Raipur", "NIT Agartala",
    "IIIT Hyderabad", "IIIT Bangalore", "IIIT Delhi", "IIIT Mumbai", "IIIT Chennai",
    "BITS Pilani", "BITS Goa", "BITS Hyderabad", "BITS Pilani K.K. Birla Goa",
    "VIT Vellore", "VIT Chennai", "SRM University", "Amity University",
    "Manipal Institute of Technology", "Thapar Institute", "PSG College of Technology",
    "College of Engineering Pune", "Delhi Technological University",
    "National Institute of Technology, Tiruchirappalli",
]

# ┃ Active invitation tokens: token -> {college, referrer, expires_at}
_invite_tokens = {}

# ┃ Active duels: duel_id -> {players, problem, deadline, status, submissions}
_active_duels = {}


@router.get("/colleges")
async def get_colleges():
    return {"colleges": INDIAN_COLLEGES}


@router.post("/invite")
async def generate_invite(college: str = Body(..., embed=True),
                         user=Depends(get_current_user)):
    """Generate an invite link for your college. Other students join via the link."""
    if college not in INDIAN_COLLEGES:
        raise HTTPException(400, "Invalid college")
    token = secrets.token_urlsafe(8)
    _invite_tokens[token] = {
        "college": college,
        "referrer_id": user["id"],
        "referrer_name": user.get("name", "Someone"),
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc).timestamp() + 86400,
    }
    invite_url = f"https://placementpro.live/campus/invite/{token}"
    logger.info(f"Invite generated: {college} by {user.get('name', user['id'])}")
    return {"token": token, "invite_url": invite_url, "college": college}


@router.get("/invite/{token}")
async def get_invite(token: str):
    """Decode an invite token."""
    info = _invite_tokens.get(token)
    if not info:
        raise HTTPException(404, "Invite not found or expired")
    return {
        "college": info["college"],
        "referrer_name": info["referrer_name"],
        "expires_at": info["expires_at"],
    }


@router.post("/duel")
async def start_duel(
    college: str = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Start a 1v1 duel. Puts user in a queue for their college."""
    if college not in INDIAN_COLLEGES:
        raise HTTPException(400, "Invalid college")
    duel_id = secrets.token_hex(6)
    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$push": {"recent_duel_invites": {"duel_id": duel_id, "college": college}}},
        upsert=True,
    )
    logger.info(f"Duel started: {duel_id} [{college}] by {user.get('name','?')}")
    return {
        "duel_id": duel_id,
        "college": college,
        "status": "waiting",
        "message": "Challenge sent! Share the duel ID with a classmate to compete.",
    }


@router.post("/duel/{duel_id}/join")
async def join_duel(duel_id: str, user=Depends(get_current_user)):
    """Join an existing duel."""
    return {
        "duel_id": duel_id,
        "status": "ready",
        "problem": _generate_duel_problem(),
        "deadline_seconds": 86400,
    }


async def _run_duel_submission(duel_id: str, user_id: str, problem_id: str,
                               code: str, language: str):
    """Execute code against hidden test cases and return score."""
    from app.services.code_executor import execute_code
    result = await execute_code(problem_id, code, language)
    return result


def _generate_duel_problem():
    """Pick a random easy/medium problem for the duel."""
    problems = [
        {"id": "two_sum", "title": "Two Sum", "difficulty": "easy",
         "description": "Given an array, return indices of two numbers adding to target."},
        {"id": "reverse_ll", "title": "Reverse Linked List", "difficulty": "medium",
         "description": "Reverse a singly linked list."},
        {"id": "binary_tree_inorder", "title": "Binary Tree Inorder", "difficulty": "easy",
         "description": "Return inorder traversal of a binary tree."},
    ]
    import random
    return random.choice(problems)


@router.get("/leaderboard/{college}")
async def get_college_leaderboard(college: str, limit: int = 20):
    """Top performers from a specific college."""
    db = get_db()
    cursor = (
        db["campus_duels"]
        .find({"college": college, "winner_id": {"$exists": True}})
        .sort("created_at", -1)
        .limit(limit)
    )
    results = []
    wins = {}
    async for duel in cursor:
        winner = str(duel.get("winner_id"))
        wins[winner] = wins.get(winner, 0) + 1
    sorted_wins = sorted(wins.items(), key=lambda x: x[1], reverse=True)[:limit]
    return {
        "college": college,
        "leaderboard": [
            {"user_id": uid, "wins": count} for uid, count in sorted_wins
        ],
    }
