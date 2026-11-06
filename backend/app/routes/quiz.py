"""Quiz & Mock Interview API Routes.

Provides endpoints for:
  - Building quizzes (practice, quiz, mock_interview, speed_run, boss_battle)
  - Submitting answers and getting feedback
  - Getting progressive hints
  - Quiz results and analytics
  - Adaptive learning paths
  - Weak topic recommendations
  - Question statistics
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.database import practice_sessions_collection
from app.services.adaptive_learning import record_learning_activity
from app.services.gamification import record_practice
from app.services.quiz_service import (
    build_quiz,
    submit_quiz_answer,
    get_hint_for_question,
    build_learning_path,
    build_boss_battle,
    get_weak_topics,
    calculate_quiz_results,
    get_question_stats,
    get_question_by_id,
    get_questions_by_topic,
    get_questions_by_difficulty,
    get_questions_by_company,
    get_all_questions,
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/quiz", tags=["Quiz & Mock Interview"])


# =============================================================
# Pydantic Models
# =============================================================

class QuizRequest(BaseModel):
    mode: str = Field(default="practice", description="practice, quiz, mock_interview, speed_run, boss_battle")
    topics: Optional[List[str]] = Field(default=None)
    difficulty: Optional[str] = Field(default=None)
    company: Optional[str] = Field(default=None)
    num_questions: int = Field(default=5, ge=1, le=50)
    time_limit_seconds: int = Field(default=0)


class AnswerSubmission(BaseModel):
    quiz_id: str
    question_id: str
    user_answer: str
    time_taken_seconds: float = Field(ge=0, le=86400)
    # Kept for backwards compatibility. The route uses server-recorded hints.
    hints_used: int = Field(default=0, ge=0, le=10)


class HintRequest(BaseModel):
    question_id: str
    hint_level: int = Field(default=1, ge=1, le=10)
    hints_already_used: int = Field(default=0, ge=0)
    quiz_id: Optional[str] = None


class QuizResultsRequest(BaseModel):
    quiz_id: str
    # Retained as optional compatibility fields. The server deliberately
    # ignores them and calculates results from the persisted quiz session.
    questions: Optional[List[dict]] = None
    answers: Optional[List[dict]] = None
    total_time_seconds: float = Field(default=0, ge=0)


class LearningPathRequest(BaseModel):
    role_id: str = "sde"
    target_level: str = "advanced"  # foundation, core, advanced
    user_weak_topics: Optional[List[str]] = None
    num_questions: int = 10


class BossBattleRequest(BaseModel):
    boss_level: int = 1
    user_level: int = 1


# =============================================================
# Quiz Endpoints
# =============================================================

def _quiz_skill_domain(question: Dict[str, Any]) -> str:
    """Map a bank question to the adaptive engine's canonical skill domain."""
    from app.services.adaptive_learning import SKILL_DOMAINS, COMPANY_TOPIC_DOMAINS

    raw_values = [
        question.get("sub_topic"),
        question.get("topic"),
        question.get("pattern"),
        question.get("domain"),
    ]
    aliases = {
        "arrays & hashing": "arrays_hashing",
        "arrays": "arrays_hashing",
        "two pointers": "two_pointers",
        "sliding window": "sliding_window",
        "quantitative aptitude": "quantitative_aptitude",
        "aptitude": "quantitative_aptitude",
        "logical reasoning": "logical_reasoning",
        "reasoning": "logical_reasoning",
        "verbal ability": "verbal_ability",
        "programming fundamentals": "programming_fundamentals",
        "programming logic": "programming_fundamentals",
        "computer science fundamentals": "computer_science",
        "sql": "sql",
        "dsa": "arrays_hashing",
    }
    for raw in raw_values:
        if not raw:
            continue
        normalized = str(raw).strip().lower().replace("-", "_").replace(" ", "_")
        candidate = aliases.get(str(raw).strip().lower(), normalized)
        if candidate in SKILL_DOMAINS:
            return candidate
        mapped = COMPANY_TOPIC_DOMAINS.get(normalized)
        if mapped in SKILL_DOMAINS:
            return mapped
    return "programming_fundamentals"


def _quiz_time_expired(session: Dict[str, Any], now: Optional[datetime] = None) -> bool:
    """Return whether a server-timed quiz has passed its deadline."""
    limit = int(session.get("time_limit_seconds", 0) or 0)
    created_at = session.get("created_at")
    if limit <= 0 or not isinstance(created_at, datetime):
        return False
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return (current - created_at).total_seconds() > limit


async def _get_owned_quiz_session(user_id: str, quiz_id: str) -> Dict[str, Any]:
    session = await practice_sessions_collection.find_one({
        "user_id": user_id,
        "quiz_id": quiz_id,
        "session_type": "quiz",
    })
    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found.")
    return session


def _ordered_quiz_attempts(session: Dict[str, Any]) -> tuple[list, list]:
    """Return trusted question-bank docs and attempts in the original session order."""
    stored_answers = {
        item.get("question_id"): item
        for item in (session.get("answers") or [])
    }
    reward_map = session.get("answer_rewards") or {}
    questions = []
    answers = []
    for question_id in session.get("question_ids") or []:
        question = get_question_by_id(question_id) or {
            "id": question_id,
            "topic": "Other",
            "difficulty": "medium",
        }
        questions.append(question)
        answer = dict(stored_answers.get(question_id) or {
            "question_id": question_id,
            "is_correct": False,
            "xp_earned": 0,
            "hints_used": 0,
            "unanswered": True,
        })
        answer["xp_earned"] = int(reward_map.get(question_id, answer.get("xp_earned", 0)) or 0)
        answers.append(answer)
    return questions, answers


@router.post("/build")
async def build_quiz_session(req: QuizRequest, user=Depends(get_current_user)):
    """Build a new quiz session."""
    quiz = build_quiz(
        mode=req.mode,
        topics=req.topics,
        difficulty=req.difficulty,
        company=req.company,
        num_questions=req.num_questions,
        time_limit_seconds=req.time_limit_seconds,
        user_level=user.get("level", 1),
    )
    if not quiz.get("questions"):
        raise HTTPException(
            status_code=404,
            detail=quiz.get("empty_reason") or "No questions match this quiz configuration.",
        )

    now = datetime.now(timezone.utc)
    await practice_sessions_collection.insert_one({
        "user_id": user["id"],
        "session_type": "quiz",
        "quiz_id": quiz["quiz_id"],
        "mode": quiz.get("mode", req.mode),
        "question_ids": [question["id"] for question in quiz["questions"]],
        "answers": [],
        "hint_counts": {},
        "status": "in_progress",
        "filters": quiz.get("filters", {}),
        "time_limit_seconds": quiz.get("time_limit_seconds", 0),
        "created_at": now,
        "updated_at": now,
    })
    return {"success": True, "quiz": quiz}


@router.post("/answer")
async def submit_answer(submission: AnswerSubmission, user=Depends(get_current_user)):
    """Submit an answer and get feedback + Diamonds."""
    session = await _get_owned_quiz_session(user["id"], submission.quiz_id)
    if session.get("status") != "in_progress":
        raise HTTPException(status_code=409, detail="This quiz has already been submitted.")
    if _quiz_time_expired(session):
        raise HTTPException(status_code=409, detail="The assessment time limit has expired. Submit the quiz to view your results.")
    if submission.question_id not in (session.get("question_ids") or []):
        raise HTTPException(status_code=403, detail="This question was not served in your quiz.")

    if any(
        item.get("question_id") == submission.question_id
        for item in (session.get("answers") or [])
    ):
        raise HTTPException(status_code=409, detail="This question has already been answered.")

    question = get_question_by_id(submission.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    result = submit_quiz_answer(
        quiz_id=submission.quiz_id,
        question_id=submission.question_id,
        user_answer=submission.user_answer,
        time_taken_seconds=submission.time_taken_seconds,
        hints_used=submission.hints_used,
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    if result.get("requires_code_execution"):
        raise HTTPException(status_code=422, detail=result.get("error"))

    # Claim this question answer atomically before awarding or recording any
    # evidence. A concurrent/replayed request cannot award the same attempt twice.
    now = datetime.now(timezone.utc)
    server_hints_used = max(
        0, int((session.get("hint_counts") or {}).get(submission.question_id, 0) or 0)
    )
    answer_record = {
        "question_id": submission.question_id,
        "is_correct": bool(result.get("is_correct")),
        "time_taken_seconds": max(0.0, float(submission.time_taken_seconds)),
        "hints_used": server_hints_used,
        "xp_earned": 0,
        "answered_at": now,
    }
    claimed = await practice_sessions_collection.update_one(
        {
            "user_id": user["id"],
            "quiz_id": submission.quiz_id,
            "session_type": "quiz",
            "status": "in_progress",
            "question_ids": submission.question_id,
            "answers.question_id": {"$ne": submission.question_id},
        },
        {"$push": {"answers": answer_record}, "$set": {"updated_at": now}},
    )
    if claimed.modified_count == 0:
        raise HTTPException(status_code=409, detail="This answer was already submitted or the quiz has closed.")

    # Adaptive evidence is recorded for correct and incorrect answers. XP is
    # only awarded for server-graded correct answers through the canonical
    # gamification service, not by trusting the client.
    try:
        await record_learning_activity(
            user["id"],
            {
                "domain_id": _quiz_skill_domain(question),
                "type": "quiz_answer",
                "success": bool(result.get("is_correct")),
                "score_impact": 1,
                "question_id": submission.question_id,
                "assessment_id": submission.quiz_id,
                "time_spent_seconds": answer_record["time_taken_seconds"],
                "hints_used": answer_record["hints_used"],
                "company": (question.get("companies") or [None])[0],
            },
        )
    except Exception:
        logger.exception("Could not record adaptive evidence for quiz %s", submission.quiz_id)

    reward = None
    if result.get("is_correct"):
        try:
            reward = await record_practice(
                user_id=user["id"],
                activity_type="quiz",
                score=10,
                metadata={
                    "quiz_id": submission.quiz_id,
                    "question_id": submission.question_id,
                    # Do not use a client-supplied timer to mint speed bonuses.
                    "hint_used": answer_record["hints_used"] > 0,
                },
                role=user.get("role") or user.get("target_role") or "sde",
                activity_id=f"{submission.quiz_id}:{submission.question_id}",
            )
        except Exception:
            logger.exception("Could not award quiz reward for %s", submission.question_id)

    xp_earned = int((reward or {}).get("xp_gained", 0) or 0)
    await practice_sessions_collection.update_one(
        {"user_id": user["id"], "quiz_id": submission.quiz_id, "session_type": "quiz"},
        {"$set": {f"answer_rewards.{submission.question_id}": xp_earned}},
    )
    result["hints_used"] = server_hints_used
    result["xp_earned"] = xp_earned
    result["reward"] = reward
    return {"success": True, "result": result}


@router.post("/hint")
async def get_hint(req: HintRequest, user=Depends(get_current_user)):
    """Get a progressive hint for a question."""
    session = None
    actual_hints_used = max(0, int(req.hints_already_used))
    if req.quiz_id:
        session = await _get_owned_quiz_session(user["id"], req.quiz_id)
        if session.get("status") != "in_progress" or req.question_id not in (session.get("question_ids") or []):
            raise HTTPException(status_code=403, detail="This question is not available in the active quiz.")
        if any(item.get("question_id") == req.question_id for item in (session.get("answers") or [])):
            raise HTTPException(status_code=409, detail="This question has already been answered.")
        actual_hints_used = max(
            0, int((session.get("hint_counts") or {}).get(req.question_id, 0) or 0)
        )
        if req.hint_level != actual_hints_used + 1:
            raise HTTPException(status_code=409, detail="Request the next hint in sequence.")

    result = get_hint_for_question(
        question_id=req.question_id,
        hint_level=req.hint_level,
        hints_already_used=actual_hints_used,
    )
    if "error" in result and "No more" not in result.get("error", ""):
        raise HTTPException(status_code=404, detail=result.get("error"))
    if session and result.get("hint"):
        await practice_sessions_collection.update_one(
            {
                "user_id": user["id"],
                "quiz_id": req.quiz_id,
                "session_type": "quiz",
                "status": "in_progress",
            },
            {"$set": {f"hint_counts.{req.question_id}": int(result.get("hints_used", actual_hints_used))}},
        )
    return {"success": True, **result}


@router.post("/results")
async def quiz_results(req: QuizResultsRequest, user=Depends(get_current_user)):
    """Calculate comprehensive quiz results."""
    session = await _get_owned_quiz_session(user["id"], req.quiz_id)
    questions, answers = _ordered_quiz_attempts(session)
    already_completed = session.get("status") == "completed"
    if already_completed and session.get("results"):
        return {"success": True, "results": session["results"]}

    total_time = max(0.0, float(req.total_time_seconds or 0))
    results = calculate_quiz_results(
        quiz_id=req.quiz_id,
        questions=questions,
        answers=answers,
        total_time_seconds=total_time,
    )
    results["answered_questions"] = len(session.get("answers") or [])
    results["unanswered_questions"] = max(0, len(questions) - results["answered_questions"])
    results["mode"] = session.get("mode", "practice")
    results["filters"] = session.get("filters", {})
    now = datetime.now(timezone.utc)
    completed = await practice_sessions_collection.update_one(
        {
            "user_id": user["id"],
            "quiz_id": req.quiz_id,
            "session_type": "quiz",
            "status": "in_progress",
        },
        {
            "$set": {
                "status": "completed",
                "completed_at": now,
                "updated_at": now,
                "total_time_seconds": total_time,
                "results": results,
            },
        },
    )
    if completed.modified_count == 0:
        refreshed = await _get_owned_quiz_session(user["id"], req.quiz_id)
        if refreshed.get("results"):
            return {"success": True, "results": refreshed["results"]}
        raise HTTPException(status_code=409, detail="Quiz could not be finalized.")
    return {"success": True, "results": results}


# =============================================================
# Learning Path & Boss Battle
# =============================================================

@router.post("/learning-path")
async def get_learning_path(req: LearningPathRequest, user=Depends(get_current_user)):
    """Get an adaptive learning path."""
    path = build_learning_path(
        role_id=req.role_id,
        target_level=req.target_level,
        user_weak_topics=req.user_weak_topics,
        num_questions=req.num_questions,
    )
    return {"success": True, "path": path}


@router.post("/boss-battle")
async def start_boss_battle(req: BossBattleRequest, user=Depends(get_current_user)):
    """Start a boss battle with hard questions."""
    battle = build_boss_battle(
        boss_level=req.boss_level,
        user_level=req.user_level,
    )
    return {"success": True, "battle": battle}


# =============================================================
# Statistics & Recommendations
# =============================================================

@router.get("/stats")
async def quiz_stats():
    """Get overall question bank statistics."""
    return {"success": True, "stats": get_question_stats()}


@router.get("/weak-topics")
async def weak_topics(
    attempted: str = Query(default="[]", description="JSON string of attempts"),
    user=Depends(get_current_user),
):
    """Analyze attempts and return weak topics."""
    # Derive weak areas from server-persisted quiz attempts; never accept a
    # client-provided history as the source of truth.
    sessions = await practice_sessions_collection.find(
        {"user_id": user["id"], "session_type": "quiz"}
    ).to_list(1000)
    attempts = []
    for session in sessions:
        for answer in (session.get("answers") or []):
            question = get_question_by_id(answer.get("question_id", ""))
            if not question:
                continue
            attempts.append({
                "topic": question.get("sub_topic") or question.get("topic", ""),
                "is_correct": bool(answer.get("is_correct")),
                "time_taken": float(answer.get("time_taken_seconds", 0) or 0),
            })
    weak = get_weak_topics(attempted_questions=attempts)
    return {"success": True, "weak_topics": weak}


# =============================================================
# Question Browsing
# =============================================================

@router.get("/questions")
async def list_questions(
    topic: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    company: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """Browse questions with filters."""
    if topic:
        questions = get_questions_by_topic(topic)
    elif difficulty:
        questions = get_questions_by_difficulty(difficulty)
    elif company:
        questions = get_questions_by_company(company)
    else:
        questions = get_all_questions()

    total = len(questions)
    paginated = questions[offset:offset + limit]

    # Return summary only
    return {
        "success": True,
        "questions": [
            {
                "id": q.get("id"),
                "title": q.get("title"),
                "topic": q.get("topic"),
                "sub_topic": q.get("sub_topic"),
                "difficulty": q.get("difficulty"),
                "pattern": q.get("pattern"),
                "companies": q.get("companies", []),
                "xp_reward": q.get("xp_reward", 10),
                "has_solution": bool(q.get("solution", {}).get("code")),
            }
            for q in paginated
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/questions/{question_id}")
async def get_question_detail(question_id: str, user=Depends(get_current_user)):
    """Get full question detail with solution and learning content."""
    question = get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return {
        "success": True,
        "question": {
            "id": question.get("id"),
            "title": question.get("title"),
            "topic": question.get("topic"),
            "sub_topic": question.get("sub_topic"),
            "difficulty": question.get("difficulty"),
            "pattern": question.get("pattern"),
            "question": question.get("question"),
            "hints": question.get("hints", []),
            "solution": question.get("solution", {}),
            "explanation": question.get("explanation"),
            "why_this_matters": question.get("why_this_matters"),
            "real_world_use": question.get("real_world_use"),
            "pattern_recognition": question.get("pattern_recognition"),
            "anti_patterns": question.get("anti_patterns"),
            "common_mistakes": question.get("common_mistakes"),
            "test_cases": question.get("test_cases", []),
            "companies": question.get("companies", []),
            "follow_up": question.get("follow_up"),
            "prerequisite_concepts": question.get("prerequisite_concepts", []),
            "related_concepts": question.get("related_concepts", []),
            "similar_problems": question.get("similar_problems", []),
            "xp_reward": question.get("xp_reward", 10),
            "estimated_time": question.get("estimated_time"),
        }
    }
