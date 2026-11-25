"""
Aptitude Timed Tests — Complete test system with timer, scoring, and leaderboard.
Covers Quantitative, Logical, and Verbal reasoning for campus placements.

Migrated to PostgreSQL: assessment_attempts (assessment_type="aptitude").
Leaderboard derived from assessment_attempts queries.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_

from app.middleware.auth import get_current_user
from app.database import get_session
from app.services.postgres_assessments import PostgresAssessmentService
from app.services.postgres_gamification import record_practice as pg_record_practice
from app.services.structured_logging import get_logger, log_context, request_id_var
from app.models.assessments import AssessmentAttempt

router = APIRouter(prefix="/api/v1/aptitude-tests", tags=["aptitude-tests"])
logger = get_logger(__name__)

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
    session: AsyncSession = Depends(get_session),
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
    available = (APTITUDE_PROBLEMS.copy() + APTITUDE_BATCH2.copy() + APTITUDE_BATCH3.copy()
                 + APTITUDE_BATCH4.copy() + APTITUDE_FINAL.copy() + APTITUDE_EXTRA.copy()
                 + APTITUDE_FINAL_BATCH.copy() + APTITUDE_ULTRA.copy() + APTITUDE_ULTIMATE.copy())
    if category != "mixed":
        available = [q for q in available if q.get("category") == category
                     or q.get("sub_category", "").lower()
                     in CATEGORIES.get(category, {}).get("sub_categories", [])]

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

    # Create test session in PostgreSQL
    now = datetime.now(timezone.utc)
    ends_at = now + timedelta(minutes=test_config["time_minutes"])

    assessment_service = PostgresAssessmentService(session)
    attempt = await assessment_service.create_assessment_attempt(
        user_id=UUID(user["id"]),
        assessment_id="aptitude",  # Fixed assessment ID for aptitude tests
        variant_id=f"{config}_{category}",
        idempotency_key=f"aptitude_{user['id']}_{config}_{category}_{now.isoformat()}",
    )

    # Store questions and config in attempt metadata
    attempt_metadata = {
        "category": category,
        "config": config,
        "config_name": test_config["name"],
        "questions": questions_for_client,
        "question_ids": [q["id"] for q in selected],
        "answers": [],
        "total_questions": len(selected),
        "time_limit_minutes": test_config["time_minutes"],
        "xp_earned": 0,
    }

    # Update attempt with metadata
    from sqlalchemy import update
    from app.models.assessments import AssessmentAttempt
    await session.execute(
        update(AssessmentAttempt)
        .where(AssessmentAttempt.id == attempt.id)
        .values(attempt_metadata=attempt_metadata)
    )

    rid = request_id_var.get("")
    logger.info(
        "assessment.attempt.started",
        extra=log_context(
            event="assessment.attempt.started",
            assessment_type="aptitude",
            category=category,
            config=config,
            attempt_id=str(attempt.id),
            request_id=rid,
        ),
    )

    return {
        "test_id": str(attempt.id),
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
    session: AsyncSession = Depends(get_session),
):
    """Submit an answer for a specific question in the test."""
    assessment_service = PostgresAssessmentService(session)

    try:
        attempt_id = UUID(test_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    attempt = await assessment_service.get_assessment_attempt(attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Test not found")

    if str(attempt.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if attempt.status != "in_progress":
        raise HTTPException(status_code=400, detail="Test is not in progress")

    # Check time limit
    metadata = attempt.attempt_metadata or {}
    ends_at_str = metadata.get("ends_at")
    if ends_at_str:
        ends_at = datetime.fromisoformat(ends_at_str)
        if datetime.now(timezone.utc) > ends_at:
            await assessment_service.attempt_repo.complete(attempt_id, None)
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
    all_questions = (APTITUDE_PROBLEMS + APTITUDE_BATCH2 + APTITUDE_BATCH3 + APTITUDE_BATCH4
                     + APTITUDE_FINAL + APTITUDE_EXTRA + APTITUDE_FINAL_BATCH
                     + APTITUDE_ULTRA + APTITUDE_ULTIMATE)
    question_ids = metadata.get("question_ids", [])
    if question_index >= len(question_ids):
        raise HTTPException(status_code=400, detail="Invalid question index")
    question_id = question_ids[question_index]
    full_question = next((q for q in all_questions if q["id"] == question_id), None)

    if not full_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check answer
    correct_answer = full_question["correct_answer"]
    is_correct = answer.strip().lower() == correct_answer.strip().lower()

    # Record answer in metadata
    answers = metadata.get("answers", [])
    answer_doc = {
        "question_index": question_index,
        "question_id": question_id,
        "answer": answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "explanation": full_question.get("explanation", ""),
        "time_taken": time_taken,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }
    answers.append(answer_doc)
    metadata["answers"] = answers

    await session.execute(
        update(attempt.__class__)
        .where(attempt.__class__.id == attempt.id)
        .values(attempt_metadata=metadata)
    )

    rid = request_id_var.get("")
    logger.info(
        "assessment.attempt.answer_recorded",
        extra=log_context(
            event="assessment.attempt.answer_recorded",
            assessment_type="aptitude",
            question_index=question_index,
            question_id=question_id,
            is_correct=is_correct,
            attempt_id=str(attempt.id),
            request_id=rid,
        ),
    )

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": full_question.get("explanation", ""),
    }


@router.post("/{test_id}/complete")
async def complete_test(
    test_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Complete the aptitude test and get results."""
    assessment_service = PostgresAssessmentService(session)

    try:
        attempt_id = UUID(test_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    attempt = await assessment_service.get_assessment_attempt(attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Test not found")

    if str(attempt.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if attempt.status != "in_progress":
        raise HTTPException(status_code=400, detail="Test already completed")

    metadata = attempt.attempt_metadata or {}

    # Calculate score
    answers = metadata.get("answers", [])
    correct = sum(1 for a in answers if a.get("is_correct"))
    total = metadata.get("total_questions", len(answers))
    score = round(correct / max(total, 1) * 100, 1)

    # Calculate time taken
    time_taken = 0
    if attempt.started_at:
        time_taken = (datetime.now(timezone.utc) - attempt.started_at).total_seconds()

    # Calculate XP
    test_config = TEST_CONFIGS.get(metadata.get("config", "standard"), TEST_CONFIGS["standard"])
    xp_earned = correct * test_config["xp_per_question"]

    # Bonus for perfect score
    if correct == total:
        xp_earned += 100

    # Update attempt metadata with results
    metadata.update({
        "status": "completed",
        "score": score,
        "correct_answers": correct,
        "time_taken": round(time_taken),
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "xp_earned": xp_earned,
    })

    # Complete the attempt
    completed = await assessment_service.attempt_repo.complete(
        attempt_id, score, completed_at=datetime.now(timezone.utc)
    )
    if completed:
        await session.execute(
            update(attempt.__class__)
            .where(attempt.__class__.id == attempt.id)
            .values(attempt_metadata=metadata)
        )

    # Record gamification
    await pg_record_practice(session, user["id"], "aptitude", score,
                             role=user.get("role") or user.get("target_role") or "sde")

    # Analyze weak areas
    from scripts.aptitude_problems import APTITUDE_PROBLEMS
    from scripts.aptitude_batch2 import APTITUDE_BATCH2
    from scripts.aptitude_batch3 import APTITUDE_BATCH3
    from scripts.aptitude_batch4 import APTITUDE_BATCH4
    from scripts.aptitude_final import APTITUDE_FINAL
    from scripts.aptitude_extra import APTITUDE_EXTRA
    from scripts.aptitude_final_batch import APTITUDE_FINAL_BATCH
    from scripts.aptitude_ultra import APTITUDE_ULTRA
    from scripts.aptitude_ultimate import APTITUDE_ULTIMATE
    all_q = (APTITUDE_PROBLEMS + APTITUDE_BATCH2 + APTITUDE_BATCH3 + APTITUDE_BATCH4
             + APTITUDE_FINAL + APTITUDE_EXTRA + APTITUDE_FINAL_BATCH
             + APTITUDE_ULTRA + APTITUDE_ULTIMATE)
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

    weak_areas = []
    for cat, stats in category_stats.items():
        accuracy = stats["correct"] / max(stats["total"], 1) * 100
        if accuracy < 60:
            weak_areas.append({
                "category": cat,
                "accuracy": round(accuracy, 1),
                "solved": stats["correct"],
                "total": stats["total"],
            })

    rid = request_id_var.get("")
    logger.info(
        "assessment.attempt.completed",
        extra=log_context(
            event="assessment.attempt.completed",
            assessment_type="aptitude",
            score=score,
            correct_answers=correct,
            total_questions=total,
            xp_earned=xp_earned,
            attempt_id=str(attempt.id),
            request_id=rid,
        ),
    )

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
    session: AsyncSession = Depends(get_session),
):
    """Get user's aptitude test history."""
    assessment_service = PostgresAssessmentService(session)
    attempts = await assessment_service.get_user_attempts(
        UUID(user["id"]), limit=limit, offset=0
    )

    tests = []
    for attempt in attempts:
        metadata = attempt.attempt_metadata or {}
        if metadata.get("assessment_type") != "aptitude" and attempt.assessment_id != "aptitude":
            continue
        if category and metadata.get("category") != category:
            continue
        tests.append({
            "id": str(attempt.id),
            "category": metadata.get("category"),
            "config": metadata.get("config"),
            "config_name": metadata.get("config_name"),
            "score": attempt.score,
            "correct_answers": metadata.get("correct_answers"),
            "total_questions": metadata.get("total_questions"),
            "time_taken": metadata.get("time_taken"),
            "xp_earned": metadata.get("xp_earned"),
            "status": attempt.status,
            "started_at": attempt.started_at.isoformat() if attempt.started_at else None,
            "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
        })

    return {"tests": tests, "total": len(tests)}


@router.get("/stats")
async def get_aptitude_stats(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get comprehensive aptitude statistics."""
    assessment_service = PostgresAssessmentService(session)
    attempts = await assessment_service.get_user_attempts(
        UUID(user["id"]), limit=1000, offset=0
    )

    aptitude_attempts = [
        a for a in attempts
        if (a.attempt_metadata or {}).get("category") or a.assessment_id == "aptitude"
    ]

    completed = [a for a in aptitude_attempts if a.status == "completed"]
    total_tests = len(completed)

    if completed:
        scores = [a.score for a in completed if a.score is not None]
        total_correct = sum((a.attempt_metadata or {}).get("correct_answers", 0) for a in completed)
        total_questions = sum((a.attempt_metadata or {}).get("total_questions", 0) for a in completed)
        total_xp = sum((a.attempt_metadata or {}).get("xp_earned", 0) for a in completed)
    else:
        scores = []
        total_correct = 0
        total_questions = 0
        total_xp = 0

    stats = {
        "avg_score": round(sum(scores) / max(len(scores), 1), 1) if scores else 0,
        "total_correct": total_correct,
        "total_questions": total_questions,
        "best_score": max(scores) if scores else 0,
        "total_xp": total_xp,
    }

    return {
        "total_tests": total_tests,
        **stats,
        "accuracy": round(total_correct / max(total_questions, 1) * 100, 1),
    }


@router.get("/leaderboard")
async def get_leaderboard(
    timeframe: str = "all",
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get aptitude test leaderboard."""
    from app.models.identity import User

    # Query completed aptitude attempts, ordered by best score
    query = select(
        AssessmentAttempt.user_id,
        func.max(AssessmentAttempt.score).label("best_score"),
        func.count(AssessmentAttempt.id).label("total_tests"),
    ).where(
        AssessmentAttempt.status == "completed",
        AssessmentAttempt.assessment_id == "aptitude",
    ).group_by(AssessmentAttempt.user_id)

    if category:
        # Filter by category in metadata (SQLite/PostgreSQL JSON containment)
        query = query.where(
            AssessmentAttempt.attempt_metadata["category"].astext == category
        )

    query = query.order_by(desc("best_score")).limit(limit)

    result = await session.execute(query)
    rows = result.all()

    leaderboard = []
    rank = 1
    for row in rows:
        user_result = await session.execute(
            select(User).where(User.id == row.user_id)
        )
        user_obj = user_result.scalar_one_or_none()
        leaderboard.append({
            "rank": rank,
            "user_name": user_obj.name if user_obj else "Unknown",
            "best_score": round(row.best_score, 1) if row.best_score else 0,
            "total_tests": row.total_tests,
        })
        rank += 1

    return {
        "leaderboard": leaderboard,
        "timeframe": timeframe,
        "category": category,
    }


@router.get("/leaderboard/my-rank")
async def get_my_rank(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get user's current rank on the leaderboard."""
    from app.models.identity import User

    # Get user's best score
    result = await session.execute(
        select(
            func.max(AssessmentAttempt.score).label("best_score"),
            func.count(AssessmentAttempt.id).label("total_tests"),
            func.sum(func.coalesce(AssessmentAttempt.attempt_metadata["correct_answers"].astext.cast(int), 0)).label("total_correct"),
            func.sum(func.coalesce(AssessmentAttempt.attempt_metadata["total_questions"].astext.cast(int), 0)).label("total_questions"),
        ).where(
            AssessmentAttempt.user_id == UUID(user["id"]),
            AssessmentAttempt.status == "completed",
            AssessmentAttempt.assessment_id == "aptitude",
        )
    )
    row = result.first()

    if not row or not row.best_score:
        return {"rank": None, "message": "No tests completed yet"}

    # Count users with better scores
    better_result = await session.execute(
        select(func.count(func.distinct(AssessmentAttempt.user_id)))
        .where(
            AssessmentAttempt.status == "completed",
            AssessmentAttempt.assessment_id == "aptitude",
            AssessmentAttempt.score > row.best_score,
        )
    )
    better_count = better_result.scalar() or 0
    rank = better_count + 1

    total_correct = row.total_correct or 0
    total_questions = row.total_questions or 0

    return {
        "rank": rank,
        "total_participants": better_count + 1,
        "best_score": round(row.best_score, 1),
        "avg_score": round(row.best_score, 1),
        "total_tests": row.total_tests,
        "accuracy": round(total_correct / max(total_questions, 1) * 100, 1),
    }
