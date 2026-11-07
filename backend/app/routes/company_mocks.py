"""
Company-Specific Mock Portals — Real interview simulation for specific companies.
Each company has its own format, difficulty, and focus areas.
"""
from datetime import datetime, timezone, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection,
    company_mock_tests_collection,
    get_db,
)
from app.services.ai_core import chat_completion, parse_json

router = APIRouter(prefix="/api/v1/company-mocks", tags=["company-mocks"])

# Company-specific mock test configurations
COMPANY_MOCK_CONFIGS = {
    "google": {
        "name": "Google SWE Mock",
        "description": "Google-style coding interview simulation",
        "rounds": [
            {
                "name": "Online Assessment",
                "type": "coding",
                "questions": 2,
                "time_minutes": 90,
                "difficulty": "medium",
                "focus": ["Arrays", "Dynamic Programming", "Graphs"],
                "format": "Each problem has 2 visible and 3 hidden test cases",
            },
            {
                "name": "Technical Phone Screen",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "hard",
                "focus": ["Trees", "Graphs", "System Design"],
                "format": "One hard problem with follow-ups",
            },
            {
                "name": "Onsite Coding",
                "type": "coding",
                "questions": 2,
                "time_minutes": 60,
                "difficulty": "hard",
                "focus": ["Advanced Data Structures", "Algorithms"],
                "format": "Two medium-hard problems",
            },
            {
                "name": "System Design",
                "type": "system_design",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "hard",
                "focus": ["Scalability", "Distributed Systems"],
                "format": "Design a large-scale system",
            },
            {
                "name": "Behavioral",
                "type": "behavioral",
                "questions": 3,
                "time_minutes": 30,
                "difficulty": "medium",
                "focus": ["Leadership", "Collaboration", "Problem Solving"],
                "format": "STAR method questions",
            },
        ],
        "total_time_minutes": 270,
        "passing_score": 70,
        "interview_tips": [
            "Think out loud - Google values your thought process",
            "Ask clarifying questions before coding",
            "Start with a brute force approach, then optimize",
            "Discuss time and space complexity",
            "Handle edge cases explicitly",
        ],
    },
    "amazon": {
        "name": "Amazon SDE Mock",
        "description": "Amazon-style interview with Leadership Principles",
        "rounds": [
            {
                "name": "Online Assessment",
                "type": "coding",
                "questions": 2,
                "time_minutes": 70,
                "difficulty": "medium",
                "focus": ["Arrays", "Strings", "Linked Lists"],
                "format": "Two coding problems",
            },
            {
                "name": "Technical Phone Screen",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Trees", "Dynamic Programming"],
                "format": "One coding problem",
            },
            {
                "name": "Loop Round 1 - Coding",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Arrays", "Trees"],
                "format": "One coding problem",
            },
            {
                "name": "Loop Round 2 - System Design",
                "type": "system_design",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Scalability", "API Design"],
                "format": "System design question",
            },
            {
                "name": "Loop Round 3 - Leadership Principles",
                "type": "behavioral",
                "questions": 4,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Customer Obsession", "Ownership", "Bias for Action", "Dive Deep"],
                "format": "Behavioral questions using STAR method",
            },
        ],
        "total_time_minutes": 250,
        "passing_score": 70,
        "leadership_principles": [
            "Customer Obsession",
            "Ownership",
            "Invent and Simplify",
            "Are Right, A Lot",
            "Learn and Be Curious",
            "Hire and Develop the Best",
            "Insist on the Highest Standards",
            "Think Big",
            "Bias for Action",
            "Frugality",
            "Earn Trust",
            "Dive Deep",
            "Have Backbone; Disagree and Commit",
            "Deliver Results",
        ],
        "interview_tips": [
            "Use STAR method for all behavioral questions",
            "Reference Amazon's Leadership Principles explicitly",
            "Show customer obsession in your answers",
            "Demonstrate ownership and accountability",
            "Be ready for follow-up questions",
        ],
    },
    "microsoft": {
        "name": "Microsoft SDE Mock",
        "description": "Microsoft-style interview focusing on clean code",
        "rounds": [
            {
                "name": "Online Assessment",
                "type": "coding",
                "questions": 2,
                "time_minutes": 60,
                "difficulty": "medium",
                "focus": ["Arrays", "Strings", "Trees"],
                "format": "Two coding problems",
            },
            {
                "name": "Technical Phone Screen",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Data Structures", "Algorithms"],
                "format": "One coding problem with discussion",
            },
            {
                "name": "Onsite Round 1",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "hard",
                "focus": ["Advanced Algorithms"],
                "format": "One hard coding problem",
            },
            {
                "name": "Onsite Round 2 - System Design",
                "type": "system_design",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Scalability", "Cloud"],
                "format": "System design question",
            },
            {
                "name": "Onsite Round 3 - Behavioral",
                "type": "behavioral",
                "questions": 3,
                "time_minutes": 30,
                "difficulty": "medium",
                "focus": ["Teamwork", "Problem Solving", "Growth Mindset"],
                "format": "Behavioral questions",
            },
        ],
        "total_time_minutes": 225,
        "passing_score": 70,
        "interview_tips": [
            "Write clean, readable code",
            "Microsoft values growth mindset",
            "Show collaboration and teamwork",
            "Discuss trade-offs in your solutions",
            "Ask thoughtful questions about the team",
        ],
    },
    # TCS NQT — two-stage structure (Foundation + Advanced). Fixed duplicate
    # `tcs` keys (the second silently overwrote the first); this is now a
    # single accurate "pattern-relevant" config mirroring TCS_NQT_STRUCTURE in
    # routes/oa.py (per public exam-pattern analysis, not exact verified counts).
    "tcs": {
        "name": "TCS NQT Simulation",
        "description": "TCS National Qualifier Test — two-stage simulation (Foundation aptitude + Advanced programming). Pattern-relevant.",
        "rounds": [
            {
                "name": "Foundation: Numerical Ability",
                "type": "aptitude",
                "questions": 21,
                "time_minutes": 40,
                "difficulty": "easy",
                "focus": ["Percentages", "Time & Work", "Profit/Loss", "Averages", "Probability"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Foundation: Reasoning Ability",
                "type": "logical",
                "questions": 25,
                "time_minutes": 50,
                "difficulty": "easy",
                "focus": ["Number Series", "Coding-Decoding", "Blood Relations", "Direction Sense"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Foundation: Verbal Ability",
                "type": "verbal",
                "questions": 20,
                "time_minutes": 30,
                "difficulty": "easy",
                "focus": ["Sentence Completion", "Grammar", "Comprehension"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Advanced: Programming Logic (MCQ)",
                "type": "cs_fundamentals",
                "questions": 10,
                "time_minutes": 25,
                "difficulty": "medium",
                "focus": ["Output prediction", "Pointers/data structures", "Debugging"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Advanced: Coding",
                "type": "coding",
                "questions": 2,
                "time_minutes": 60,
                "difficulty": "medium",
                "focus": ["Arrays", "Strings", "Basic Logic"],
                "format": "Two coding problems",
            },
        ],
        "total_time_minutes": 190,
        "passing_score": 60,
        "provenance": "pattern-relevant",
        "interview_tips": [
            "No negative marking in the real NQT — never leave a question unanswered",
            "Foundation sections are time-boxed: move when the timer forces section end",
            "Practice basic coding patterns — the Advanced coding round favors clean, working solutions",
            "Review aptitude formulas (percentages, time & work) before attempting",
            "TCS values accuracy over complexity",
        ],
    },
}


@router.get("/companies")
async def list_company_mocks(user=Depends(get_current_user)):
    """List all available company-specific mock tests."""
    companies = []
    for company_id, config in COMPANY_MOCK_CONFIGS.items():
        companies.append({
            "id": company_id,
            "name": config["name"],
            "description": config["description"],
            "total_time_minutes": config["total_time_minutes"],
            "rounds_count": len(config["rounds"]),
            "passing_score": config["passing_score"],
        })
    return {"companies": companies}


@router.get("/{company_id}/config")
async def get_company_config(company_id: str, user=Depends(get_current_user)):
    """Get detailed configuration for a company mock test."""
    config = COMPANY_MOCK_CONFIGS.get(company_id.lower())
    if not config:
        raise HTTPException(status_code=404, detail="Company not found")
    return config


@router.post("/{company_id}/start")
async def start_company_mock(
    company_id: str,
    round_name: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Start a company-specific mock test."""
    config = COMPANY_MOCK_CONFIGS.get(company_id.lower())
    if not config:
        raise HTTPException(status_code=404, detail="Company not found")

    # Determine which round to start
    if round_name:
        target_round = next((r for r in config["rounds"] if r["name"] == round_name), None)
        if not target_round:
            raise HTTPException(status_code=404, detail="Round not found")
        rounds_to_run = [target_round]
    else:
        rounds_to_run = config["rounds"]

    # Get questions for each round
    all_questions = []
    for round_config in rounds_to_run:
        if round_config["type"] == "coding":
            # In-memory canonical store only (Residency Rule, AGENTS.md):
            # verified company-tagged items first, general verified backfill.
            # Never MongoDB, never legacy unverified content.
            from app.services import question_store
            bank = question_store.company_verified_bank(company_id)
            tagged_ids = {q.get("id") for q in bank["items"]}
            pool = question_store.find({
                "type": "coding",
                "difficulty": round_config["difficulty"],
                "topic": {"$in": round_config["focus"]},
            }).only_verified().to_list()
            pool.sort(key=lambda q: (0 if q.get("id") in tagged_ids else 1,))
            for q in random.sample(pool, min(round_config["questions"], len(pool))):
                doc = question_store.get_question_for_serving(q.get("id")) or dict(q)
                doc["id"] = q.get("id")
                doc["round"] = round_config["name"]
                # Compat keys matching the legacy projection shape.
                doc.setdefault("topics", [doc.get("topic", "General")])
                doc.setdefault("company", company_id)
                all_questions.append(doc)

    # Create mock test session
    session = {
        "user_id": user["id"],
        "company": company_id,
        "config": config,
        "rounds": rounds_to_run,
        "questions": all_questions,
        "answers": [],
        "current_round": 0,
        "current_question": 0,
        "status": "in_progress",
        "started_at": datetime.now(timezone.utc),
        "ends_at": datetime.now(timezone.utc) + timedelta(minutes=config["total_time_minutes"]),
        "total_score": 0,
    }

    db = get_db()
    result = await db["company_mock_tests"].insert_one(session)
    session_id = str(result.inserted_id)

    return {
        "session_id": session_id,
        "company": company_id,
        "config": config,
        "rounds": rounds_to_run,
        "questions": all_questions,
        "ends_at": session["ends_at"].isoformat(),
    }


@router.get("/{session_id}/status")
async def get_mock_status(session_id: str, user=Depends(get_current_user)):
    """Get current mock test status."""
    db = get_db()

    try:
        session = await db["company_mock_tests"].find_one({
            "_id": ObjectId(session_id),
            "user_id": user["id"],
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    now = datetime.now(timezone.utc)
    time_remaining = max(0, (session["ends_at"] - now).total_seconds())

    return {
        "session_id": session_id,
        "status": session["status"],
        "time_remaining_seconds": int(time_remaining),
        "current_round": session["current_round"],
        "questions_answered": len(session.get("answers", [])),
        "total_questions": len(session["questions"]),
    }


@router.get("/{session_id}/results")
async def get_mock_results(session_id: str, user=Depends(get_current_user)):
    """Get complete mock test results."""
    db = get_db()

    try:
        session = await db["company_mock_tests"].find_one({
            "_id": ObjectId(session_id),
            "user_id": user["id"],
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Calculate round-wise scores
    round_scores = {}
    for answer in session.get("answers", []):
        round_name = answer.get("round", "Unknown")
        if round_name not in round_scores:
            round_scores[round_name] = {"total": 0, "score": 0, "count": 0}
        round_scores[round_name]["total"] += answer.get("total_cases", 0)
        round_scores[round_name]["score"] += answer.get("passed_count", 0)
        round_scores[round_name]["count"] += 1

    # Calculate overall score
    total_score = session.get("total_score", 0)
    passing_score = session["config"].get("passing_score", 70)
    passed = total_score >= passing_score

    return {
        "session_id": session_id,
        "company": session["company"],
        "total_score": total_score,
        "passing_score": passing_score,
        "passed": passed,
        "round_scores": round_scores,
        "completed_at": session.get("completed_at", datetime.now(timezone.utc)).isoformat(),
        "interview_tips": session["config"].get("interview_tips", []),
    }
