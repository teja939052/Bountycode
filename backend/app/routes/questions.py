from datetime import datetime, timezone
import json
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, question_answers_collection,
    users_collection, solved_problems_collection
)
from app.models.question import SubmitAnswer, QuestionSubmission, QuestionVote
from app.services.ai import chat_completion, parse_json, assign_companies
from app.services.gamification import record_practice
from app.services.usage import check_and_reset_monthly_usage
from app.services.code_executor import CodeExecutionEngine
from app.services.response_cache import cached, invalidate_questions_cache
from app.services import question_store
from app.services.explanation_cache import get_or_create_explanation
import random
import os
import json
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]

router = APIRouter(prefix="/api/v1/questions", tags=["question-bank"])
code_engine = CodeExecutionEngine()

FREE_DAILY_PROBLEM_LIMIT = 3


def _is_paid(user: dict) -> bool:
    return user.get("plan") in ("pro", "lifetime")


def _daily_question_count(user: dict) -> int:
    daily = user.get("daily_usage") or {}
    today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return daily.get("questions_today", 0)


def _check_question_quota(user: dict):
    """Raise HTTPException if the user has exhausted their free daily quota."""
    if _is_paid(user):
        return
    if _daily_question_count(user) >= FREE_DAILY_PROBLEM_LIMIT:
        raise HTTPException(
            status_code=402,
            detail=(
                "⚠️ Your daily training stamina is depleted! "
                "You've used your 3 free problems today. "
                "Upgrade to the Pro Pass for unlimited practice, "
                "company-specific questions, and instant AI feedback."
            ),
        )


def _filter_curated(questions: list, company: str, pattern: str, role: str) -> list:
    """Apply company/pattern/role filters to the curated question list."""
    result = questions
    if company:
        result = [q for q in result if company.lower() in [c.lower() for c in q.get("company", [])]]
    if pattern:
        result = [q for q in result if q.get("pattern") == pattern]
    if role:
        result = [q for q in result if q.get("role") == role]
    return result


CURATED_EXTRA_BANKS = [
    BACKEND_ROOT / "app" / "data" / "leetcode_problems_seed.json",
    BACKEND_ROOT / "app" / "data" / "striver_a2z_600.json",
    BACKEND_ROOT / "app" / "data" / "tcs_nqt_questions.json",
    BACKEND_ROOT / "app" / "data" / "infosys_questions.json",
]

def _load_curated_questions() -> list:
    """Load the curated question bank from the content directory, then merge
    file-based laptop-storage banks (placement-grade, non-AI, no DB) so the
    browse API surfaces Striver + LeetCode problems."""
    questions: list = []
    curated_path = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "curated.json"
    if curated_path.exists():
        try:
            with open(curated_path, "r", encoding="utf-8") as f:
                questions = json.load(f)
        except Exception:
            questions = []
    for seed_path in CURATED_EXTRA_BANKS:
        if seed_path.exists():
            try:
                with open(seed_path, "r", encoding="utf-8") as f:
                    questions.extend(json.load(f))
            except Exception:
                pass
    return questions


def _question_title(q: dict) -> str:
    return q.get("question") or q.get("question_title", "")


def _explain_compiler_error(error_message: str, source_code: str, language: str) -> str:
    """Enhanced compiler error explanation with line references when possible."""
    import re
    error_lower = error_message.lower()
    line_match = re.search(r"line (\d+)", error_message)
    line_ref = f" (at line {line_match.group(1)})" if line_match else ""
    if "compile" in error_lower or "syntax" in error_lower:
        return f"Syntax error{line_ref}. Your code could not be compiled. Common causes: missing colon, mismatched parentheses, incorrect indentation.{line_ref}"
    elif "timeout" in error_lower or "timelimit" in error_lower or "time limit" in error_lower:
        return f"Time limit exceeded{line_ref}. Your code took too long. Consider optimizing your algorithm or reducing input size."
    elif "memory" in error_lower or "mle" in error_lower or "out of memory" in error_lower:
        return f"Memory limit exceeded{line_ref}. Your code used too much memory. Try using generators or more efficient data structures."
    elif "runtime" in error_lower or "exception" in error_lower or "error" in error_lower:
        if "nameerror" in error_lower:
            return f"Name error{line_ref}. You are using a variable or function that is not defined. Check spelling and imports."
        elif "typemerror" in error_lower or "type error" in error_lower:
            return f"Type error{line_ref}. You are trying to operate on incompatible types. Check your types and operators."
        elif "zero division" in error_lower or "division by zero" in error_lower:
            return f"Division by zero{line_ref}. You are dividing by zero. Add a check before dividing."
        elif "index error" in error_lower or "out of range" in error_lower:
            return f"Index error{line_ref}. You are accessing a list/tuple index that does not exist. Check your bounds."
        elif "key error" in error_lower:
            return f"Key error{line_ref}. You are accessing a dictionary key that does not exist. Use .get() or check existence first."
        else:
            return f"Runtime error{line_ref}. Your code crashed during execution. Check for edge cases, division by zero, or unexpected inputs.{line_ref}"
    else:
        return f"Execution failed{line_ref}. Your code did not produce the expected output. Review your algorithm logic and edge cases."


def _is_correct_answer(user_ans: str, correct: str, q_type: str) -> bool:
    if not correct:
        return False
    if q_type == "aptitude":
        u = user_ans.lower().strip()
        c = correct.lower().strip()
        if u == c:
            return True
        try:
            return abs(float(u) - float(c)) / max(abs(float(c)), 1e-6) < 0.02
        except Exception:
            return False
    return bool(user_ans.strip())


@router.get("/browse")
@cached(ttl=300, key_prefix="questions")
async def browse_questions(
    company: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    sub_topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    pattern: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("frequency"),
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    skip_quota: bool = Query(False, description="Internal: skip quota for verified free-access content"),
    context: Optional[str] = Query(None, description="Context for free-access verification: onboarding|tutorial|first_problem"),
    user=Depends(get_current_user),
):
    # Paywall: company-specific filters require Pro
    if company and not _is_paid(user):
        raise HTTPException(
            status_code=402,
            detail=(
                f"🔒 Company-specific question filters are locked. "
                f"Targeted {company} preparation requires a Pro Pass. "
                f"Upgrade for access to 53 company blueprints."
            ),
        )

    # Free-access verification: backend independently identifies whether the
    # requested content is legitimately onboarding/tutorial/first-problem.
    # The frontend cannot simply set skip_quota=true to bypass the quota.
    is_free_access = False
    if skip_quota and context in ("onboarding", "tutorial", "first_problem"):
        # Only allow free access if the user is actually eligible (free tier, not yet consumed today)
        if not _is_paid(user) and not _daily_question_count(user) >= FREE_DAILY_PROBLEM_LIMIT:
            is_free_access = True

    # Paywall: enforce daily free quota
    # Exception: allow onboarding diagnostic + first sample without consuming quota
    if not is_free_access:
        _check_question_quota(user)

    # Load from curated content store (clean JSON on disk, not MongoDB)
    all_questions = _load_curated_questions()

    # For production serving, only show placement-grade reviewed questions
    # Admin users and Pro can see all; free users get only reviewed ones
    if not _is_paid(user):
        all_questions = [q for q in all_questions if q.get("review_status") in ("placement_grade", "reviewed")]

    # Apply filters
    filtered = _filter_curated(all_questions, company, pattern, role)
    if topic:
        filtered = [q for q in filtered if q.get("topic", "").lower() == topic.lower()]
    if difficulty:
        filtered = [q for q in filtered if q.get("difficulty", "").lower() == difficulty.lower()]
    if type:
        filtered = [q for q in filtered if q.get("type", "").lower() == type.lower()]
    if search:
        search_lower = search.lower()
        filtered = [q for q in filtered if search_lower in (q.get("question", "") or "").lower()]

    # Sort
    if sort == "difficulty":
        filtered.sort(key=lambda q: (q.get("difficulty", "medium"),))
    elif sort == "alphabetical":
        filtered.sort(key=lambda q: q.get("question", ""))[:100]
    else:
        filtered.sort(key=lambda q: q.get("frequency", 0), reverse=True)

    total = len(filtered)
    skip = (page - 1) * limit
    items = filtered[skip:skip + limit]

    # Inject usage info for the frontend
    remaining = max(0, FREE_DAILY_PROBLEM_LIMIT - _daily_question_count(user)) if not _is_paid(user) else -1

    return {
        "questions": items,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit if total > 0 else 1,
        "sort": sort,
        "remaining_daily": remaining,
        "is_pro": _is_paid(user),
        "source": "curated",
    }


def _company_bank_overview(company_id: str) -> Optional[Dict[str, Any]]:
    """Build the Company Question Bank overview for a resolved bank id."""
    from app.data.interview_question_bank import (
        get_companies, get_questions_by_company, CATEGORY_LABELS,
    )
    for c in get_companies():
        if c["company_id"] == company_id:
            return c
    return None


def _coding_store_topics(company_key: str, limit: int = 8):
    """Real counts of coding questions tagged to this company in the main store."""
    variants = ("-v2", "-v3", "-v4")
    query = {"company": {"$in": [company_key, company_key.replace("_", " "), company_key.replace("_", "-")]}, "type": "coding"}
    counts: Dict[str, int] = {}
    for q in question_store.find(query).to_list():
        if str(q.get("id", "")).endswith(variants):
            continue
        topic = (q.get("topic") or "General").strip()
        counts[topic] = counts.get(topic, 0) + 1
    topics = [{"topic": t, "count": c} for t, c in sorted(counts.items(), key=lambda kv: kv[1], reverse=True)]
    return {"hits": sum(c["count"] for c in topics), "top_topics": topics[:limit]}


@router.get("/company/{company}")
@cached(ttl=600, key_prefix="questions")
async def company_question_bank(
    company: str,
    user=Depends(get_current_user),
):
    """
    GET: Company Question Bank overview — what a company actually asks.

    Combines the authored per-company interview bank (behavioral, coding,
    system design, SQL, HR...) with the curated coding store's company-tagged
    problems. All counts are real, derived from the question data itself.
    """
    from app.data.interview_question_bank import (
        resolve_company, get_questions_by_company, CATEGORY_LABELS,
    )

    company_id = resolve_company(company)
    overview = _company_bank_overview(company_id) if company_id else None

    focus_areas = []
    prep_name = None
    try:
        from app.routes.company_prep import TOP_COMPANIES
        meta = TOP_COMPANIES.get(company_id) if company_id else None
        if meta:
            focus_areas = list(meta.get("focus_areas", []))
            prep_name = meta.get("name")
    except Exception:
        pass

    display_name = (overview or {}).get("name") or prep_name or company.title()
    icon = (overview or {}).get("icon", "")
    color = (overview or {}).get("color", "")

    # Coding problems from the main store tagged to this company.
    coding = _coding_store_topics(company_id or company.lower().strip())

    # Sample questions: top bank categories + top coding topic.
    samples = []
    if overview:
        for cat in overview["categories"][:3]:
            for q in get_questions_by_company(company_id, cat["category"])[:2]:
                samples.append({
                    "id": q["id"],
                    "question": q["question"],
                    "category": q["category"],
                    "category_label": CATEGORY_LABELS.get(q["category"], q["category"]),
                    "difficulty": q.get("difficulty", "medium"),
                    "type": "bank",
                })
    if coding["top_topics"]:
        query = {"company": {"$in": [company_id or company.lower().strip()]}, "type": "coding"}
        for q in question_store.find(query).to_list():
            if str(q.get("id", "")).endswith(("-v2", "-v3", "-v4")):
                continue
            if len([s for s in samples if s["type"] == "coding"]) >= 3:
                break
            samples.append({
                "id": q["id"],
                "question": q.get("question") or q.get("statement", ""),
                "category": "coding",
                "category_label": "Coding",
                "difficulty": q.get("difficulty", "medium"),
                "topic": q.get("topic", ""),
                "type": "coding",
            })

    return {
        "company_id": company_id,
        "company": display_name,
        "icon": icon,
        "color": color,
        "in_bank": overview is not None,
        "total_bank_questions": (overview or {}).get("total_questions", 0),
        "categories": (overview or {}).get("categories", []),
        "leadership_principles": (overview or {}).get("leadership_principles", []),
        "focus_areas": focus_areas,
        "coding_store": coding,
        "sample_questions": samples[:12],
        "source": "Authored interview question bank + curated coding store",
    }


@router.get("/company/{company}/questions")
async def company_question_bank_list(
    company: str,
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    """
    GET: Full question list for a company's bank, optionally filtered by
    category and paginated. Returns non-variant authored questions only.
    """
    from app.data.interview_question_bank import (
        resolve_company, get_questions_by_company, CATEGORY_LABELS,
    )

    company_id = resolve_company(company)
    if not company_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company '{company}' has no authored question bank. Use /questions/company/{company} to see coding practice problems."
        )

    questions = get_questions_by_company(company_id, category)
    _DIFF_RANK = {"easy": 0, "medium": 1, "hard": 2}
    questions.sort(key=lambda q: (_DIFF_RANK.get(q.get("difficulty", "medium"), 3), q.get("id", "")))

    total = len(questions)
    start = (page - 1) * limit
    items = [
        {
            "id": q["id"],
            "question": q["question"],
            "category": q["category"],
            "category_label": CATEGORY_LABELS.get(q["category"], q["category"]),
            "difficulty": q.get("difficulty", "medium"),
        }
        for q in questions[start:start + limit]
    ]

    return {
        "company_id": company_id,
        "company": questions[0]["company"] if questions else company.title(),
        "category": category,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit if total > 0 else 1,
        "questions": items,
    }


@router.get("/filters")
@cached(ttl=3600, key_prefix="questions")
async def get_filters():
    return question_store.get_filters()


@router.get("/patterns")
async def get_patterns():
    """List all Striver-pattern categories with problem counts (sheet order)."""
    patterns = question_store.get_pattern_stats()
    return {"patterns": patterns, "total": sum(p["total"] for p in patterns)}


@router.get("/topics")
@cached(ttl=300, key_prefix="questions")
async def get_topics():
    topics = question_store.get_topic_stats()
    return {"topics": topics}


@router.get("/stats")
async def get_my_stats(user=Depends(get_current_user)):
    collection = question_answers_collection()
    uid = user["id"]

    total_attempted = await collection.count_documents({"user_id": uid})
    pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {
            "_id": "$topic",
            "avg_score": {"$avg": "$score"},
            "count": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}},
        },
        {"$sort": {"avg_score": 1}},
    ]
    topic_stats = []
    async for doc in collection.aggregate(pipeline):
        topic_stats.append({
            "topic": doc["_id"],
            "avg_score": round(doc["avg_score"], 1),
            "count": doc["count"],
            "accuracy": round(doc["correct"] / doc["count"] * 100, 1) if doc["count"] > 0 else 0,
        })

    weak_areas = [t for t in topic_stats if t["avg_score"] < 6][:5]
    strong_areas = [t for t in topic_stats if t["avg_score"] >= 7][:5]

    return {
        "total_attempted": total_attempted,
        "topic_stats": topic_stats,
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
    }


@router.post("/daily-increment")
async def increment_daily_question_count(user=Depends(get_current_user)):
    """Increment the user's daily question counter. Returns remaining daily quota."""
    if _is_paid(user):
        return {"remaining": -1, "is_pro": True}
    today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily = user.get("daily_usage") or {}
    last_reset = daily.get("questions_reset_date")
    if last_reset != today_key:
        daily["questions_today"] = 0
        daily["questions_reset_date"] = today_key
    daily["questions_today"] = daily.get("questions_today", 0) + 1
    remaining = max(0, FREE_DAILY_PROBLEM_LIMIT - daily["questions_today"])
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"daily_usage": daily}},
    )
    return {"remaining": remaining, "is_pro": False}


@router.post("/submit")
async def submit_question(req: QuestionSubmission, user=Depends(get_current_user)):
    doc = req.model_dump()
    doc["submitted_by"] = user["id"]
    doc["upvotes"] = 0
    doc["downvotes"] = 0
    doc["reported"] = False
    doc["created_at"] = datetime.now(timezone.utc)
    doc["updated_at"] = datetime.now(timezone.utc)
    result = await curated_questions_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    try:
        from app.services import question_store
        question_store.insert_question(doc)
    except Exception:
        pass
    await invalidate_questions_cache()
    return doc


@router.post("/upvote")
async def upvote_question(req: QuestionVote, user=Depends(get_current_user)):
    question = question_store.find_one({"id": req.question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    try:
        q_oid = ObjectId(req.question_id)
        await curated_questions_collection.update_one(
            {"_id": q_oid},
            {"$inc": {"upvotes": max(0, req.vote), "downvotes": max(0, -req.vote)}, "$set": {"updated_at": datetime.now(timezone.utc)}},
        )
        updated = await curated_questions_collection.find_one({"_id": q_oid})
        up = updated.get("upvotes", 0) if updated else question.get("upvotes", 0)
        down = updated.get("downvotes", 0) if updated else question.get("downvotes", 0)
    except Exception:
        up = question.get("upvotes", 0) + max(0, req.vote)
        down = question.get("downvotes", 0) + max(0, -req.vote)

    return {
        "question_id": req.question_id,
        "upvotes": up,
        "downvotes": down,
    }


from app.routes.questions_solve import router as solve_router

router.include_router(solve_router)