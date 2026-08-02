"""
Placement aptitude questions with company tags.
Serves pre-built question bank for practice mode with filtering by category, difficulty, and company.
"""

import random
from collections import Counter
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user

try:
    from app.data.placement_aptitude_questions import PLACEMENT_APTITUDE_QUESTIONS
except ImportError:
    PLACEMENT_APTITUDE_QUESTIONS = []

router = APIRouter(prefix="/api/v1/placement-questions", tags=["placement-questions"])


def _strip_correct_answer(q: dict) -> dict:
    """Return a question dict without the correct answer (practice mode safe)."""
    return {
        "id": q["id"],
        "category": q["category"],
        "difficulty": q["difficulty"],
        "question": q["question"],
        "options": q["options"],
        "companies": q.get("companies", []),
        "topic": q.get("topic", ""),
    }


@router.get("/random")
async def get_random_questions(
    category: str = None,
    difficulty: str = None,
    company: str = None,
    count: int = 10,
    user=Depends(get_current_user),
):
    """Get random placement aptitude questions with optional filters.
    Returns questions without correct_answer for practice mode.
    Includes company tags for motivational display."""
    if not PLACEMENT_APTITUDE_QUESTIONS:
        raise HTTPException(status_code=503, detail="Question bank not loaded")

    if count < 1:
        count = 1
    if count > 50:
        count = 50

    pool = PLACEMENT_APTITUDE_QUESTIONS

    if category:
        category_lower = category.lower()
        pool = [q for q in pool if q["category"] == category_lower]
        if not pool:
            raise HTTPException(
                status_code=404,
                detail=f"No questions found for category '{category}'. "
                       f"Available: quantitative, logical, verbal",
            )

    if difficulty:
        diff_lower = difficulty.lower()
        pool = [q for q in pool if q["difficulty"] == diff_lower]
        if not pool:
            raise HTTPException(
                status_code=404,
                detail=f"No questions found for difficulty '{difficulty}'. "
                       f"Available: easy, medium, hard",
            )

    if company:
        company_lower = company.lower()
        pool = [q for q in pool if company_lower in [c.lower() for c in q.get("companies", [])]]
        if not pool:
            raise HTTPException(
                status_code=404,
                detail=f"No questions found for company '{company}'",
            )

    sampled = random.sample(pool, min(count, len(pool)))

    return {
        "questions": [_strip_correct_answer(q) for q in sampled],
        "total_available": len(pool),
        "returned": len(sampled),
        "filters": {
            "category": category,
            "difficulty": difficulty,
            "company": company,
        },
    }


@router.get("/by-company/{company_name}")
async def get_questions_by_company(
    company_name: str,
    count: int = 10,
    user=Depends(get_current_user),
):
    """Get questions commonly asked at a specific company."""
    if not PLACEMENT_APTITUDE_QUESTIONS:
        raise HTTPException(status_code=503, detail="Question bank not loaded")

    if count < 1:
        count = 1
    if count > 50:
        count = 50

    company_lower = company_name.lower()
    pool = [q for q in PLACEMENT_APTITUDE_QUESTIONS if company_lower in [c.lower() for c in q.get("companies", [])]]

    if not pool:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for company '{company_name}'",
        )

    sampled = random.sample(pool, min(count, len(pool)))

    category_counts = Counter(q["category"] for q in pool)
    difficulty_counts = Counter(q["difficulty"] for q in pool)

    return {
        "company": company_name,
        "questions": [_strip_correct_answer(q) for q in sampled],
        "total_questions": len(pool),
        "returned": len(sampled),
        "breakdown": {
            "by_category": dict(category_counts),
            "by_difficulty": dict(difficulty_counts),
        },
    }


@router.get("/stats")
async def get_question_stats(user=Depends(get_current_user)):
    """Get stats about available questions per category, difficulty, and company."""
    if not PLACEMENT_APTITUDE_QUESTIONS:
        return {
            "total": 0,
            "by_category": {},
            "by_difficulty": {},
            "by_company": {},
            "top_companies": [],
            "message": "Question bank not loaded",
        }

    total = len(PLACEMENT_APTITUDE_QUESTIONS)

    category_counts = Counter(q["category"] for q in PLACEMENT_APTITUDE_QUESTIONS)
    difficulty_counts = Counter(q["difficulty"] for q in PLACEMENT_APTITUDE_QUESTIONS)

    company_counter = Counter()
    for q in PLACEMENT_APTITUDE_QUESTIONS:
        for c in q.get("companies", []):
            company_counter[c] += 1

    topic_counter = Counter()
    for q in PLACEMENT_APTITUDE_QUESTIONS:
        topic_counter[q.get("topic", "General")] += 1

    return {
        "total": total,
        "by_category": dict(category_counts),
        "by_difficulty": dict(difficulty_counts),
        "by_company": dict(company_counter.most_common()),
        "top_companies": [
            {"company": c, "count": n}
            for c, n in company_counter.most_common(10)
        ],
        "topics": dict(topic_counter.most_common()),
    }
