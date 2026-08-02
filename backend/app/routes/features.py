"""
Remaining Platform Features — Random Pick, Bookmarks, Notes, Company Filtering.
Essential LeetCode-style features for complete platform experience.
"""
from datetime import datetime, timezone
import random
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, bookmarks_collection,
    notes_collection, solved_problems_collection
)

router = APIRouter(prefix="/api/v1/features", tags=["features"])


# ═══════════════════════════════════════════════════════════════════════════
# RANDOM PROBLEM PICK
# ═══════════════════════════════════════════════════════════════════════════
@router.get("/random")
async def get_random_problem(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    company: Optional[str] = None,
    unsolved_only: bool = False,
    user=Depends(get_current_user),
):
    """Get a random problem with optional filters."""
    collection = curated_questions_collection()
    query = {"type": "coding"}

    if difficulty:
        query["difficulty"] = difficulty
    if topic:
        query["topic"] = topic
    if company:
        query["$or"] = [{"company": company}, {"company": company.title()}]

    if unsolved_only:
        solved_ids = []
        async for doc in solved_problems_collection().find(
            {"user_id": user["id"]}, {"question_id": 1}
        ):
            solved_ids.append(doc["question_id"])
        if solved_ids:
            query["_id"] = {"$nin": [ObjectId(sid) for sid in solved_ids if ObjectId.is_valid(sid)]}

    # Get random problem
    pipeline = [
        {"$match": query},
        {"$sample": {"size": 1}},
        {"$project": {
            "statement": 0,
            "visible_test_cases": 0,
            "hidden_test_cases": 0,
            "solution": 0,
        }}
    ]

    problem = None
    async for doc in collection.aggregate(pipeline):
        doc["id"] = str(doc.pop("_id"))
        problem = doc

    if not problem:
        # Fallback: any random problem
        pipeline = [{"$sample": {"size": 1}}]
        async for doc in collection.aggregate(pipeline):
            doc["id"] = str(doc.pop("_id"))
            problem = doc

    if not problem:
        raise HTTPException(status_code=404, detail="No problems available")

    return {
        "problem": problem,
        "filters_applied": {
            "difficulty": difficulty,
            "topic": topic,
            "company": company,
            "unsolved_only": unsolved_only,
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
# BOOKMARKS
# ═══════════════════════════════════════════════════════════════════════════
@router.post("/bookmarks/{question_id}")
async def toggle_bookmark(
    question_id: str,
    user=Depends(get_current_user),
):
    """Toggle bookmark for a problem."""
    collection = bookmarks_collection()

    existing = await collection.find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })

    if existing:
        await collection.delete_one({"_id": existing["_id"]})
        return {"bookmarked": False, "message": "Bookmark removed"}
    else:
        # Verify question exists
        try:
            q_oid = ObjectId(question_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid question ID")

        question = await curated_questions_collection().find_one({"_id": q_oid})
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        bookmark = {
            "user_id": user["id"],
            "question_id": question_id,
            "question_title": question.get("question_title", "Unknown"),
            "topic": question.get("topic", "Unknown"),
            "difficulty": question.get("difficulty", "medium"),
            "created_at": datetime.now(timezone.utc),
        }

        await collection.insert_one(bookmark)
        return {"bookmarked": True, "message": "Bookmark added"}


@router.get("/bookmarks")
async def get_bookmarks(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get all bookmarked problems."""
    collection = bookmarks_collection()
    query = {"user_id": user["id"]}

    if topic:
        query["topic"] = topic
    if difficulty:
        query["difficulty"] = difficulty

    cursor = collection.find(query).sort("created_at", -1)
    bookmarks = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        bookmarks.append(doc)

    return {
        "bookmarks": bookmarks,
        "total": len(bookmarks),
    }


# ═══════════════════════════════════════════════════════════════════════════
# NOTES
# ═══════════════════════════════════════════════════════════════════════════
@router.post("/notes/{question_id}")
async def create_or_update_note(
    question_id: str,
    content: str,
    user=Depends(get_current_user),
):
    """Create or update a note for a problem."""
    collection = notes_collection()

    existing = await collection.find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })

    if existing:
        await collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {
                "content": content,
                "updated_at": datetime.now(timezone.utc),
            }}
        )
        return {"note_id": str(existing["_id"]), "message": "Note updated"}
    else:
        note = {
            "user_id": user["id"],
            "question_id": question_id,
            "content": content,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = await collection.insert_one(note)
        return {"note_id": str(result.inserted_id), "message": "Note created"}


@router.get("/notes/{question_id}")
async def get_note(question_id: str, user=Depends(get_current_user)):
    """Get note for a specific problem."""
    collection = notes_collection()
    note = await collection.find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })

    if not note:
        return {"note": None, "content": ""}

    note["id"] = str(note.pop("_id"))
    return {"note": note, "content": note.get("content", "")}


@router.get("/notes")
async def get_all_notes(user=Depends(get_current_user)):
    """Get all notes by the user."""
    collection = notes_collection()
    cursor = collection.find({"user_id": user["id"]}).sort("updated_at", -1)
    notes = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        notes.append(doc)

    return {
        "notes": notes,
        "total": len(notes),
    }


# ═══════════════════════════════════════════════════════════════════════════
# COMPANY FILTERING (Pro Feature)
# ═══════════════════════════════════════════════════════════════════════════
@router.get("/company/{company_name}")
async def get_company_problems(
    company_name: str,
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    sort: Optional[str] = "frequency",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    """Get problems for a specific company (Pro feature)."""
    collection = curated_questions_collection()
    query = {"type": "coding"}

    # Match company (case-insensitive)
    query["$or"] = [
        {"company": company_name},
        {"company": company_name.title()},
        {"company": company_name.upper()},
    ]

    if difficulty:
        query["difficulty"] = difficulty
    if topic:
        query["topic"] = topic

    # Build sort
    if sort == "difficulty":
        sort_stage = [("difficulty", 1)]
    elif sort == "newest":
        sort_stage = [("created_at", -1)]
    else:  # frequency
        sort_stage = [("frequency", -1)]

    total = await collection.count_documents(query)
    skip = (page - 1) * limit

    cursor = collection.find(query).sort(sort_stage).skip(skip).limit(limit)
    problems = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        problems.append(doc)

    # Company stats
    company_pipeline = [
        {"$match": query},
        {"$group": {
            "_id": "$difficulty",
            "count": {"$sum": 1}
        }}
    ]
    diff_stats = {}
    async for doc in collection.aggregate(company_pipeline):
        diff_stats[doc["_id"]] = doc["count"]

    return {
        "company": company_name,
        "problems": problems,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "stats": {
            "total": total,
            "easy": diff_stats.get("easy", 0),
            "medium": diff_stats.get("medium", 0),
            "hard": diff_stats.get("hard", 0),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
# PROBLEM DETAIL ENHANCEMENTS
# ═══════════════════════════════════════════════════════════════════════════
@router.get("/problem/{question_id}/enhanced")
async def get_enhanced_problem_detail(question_id: str, user=Depends(get_current_user)):
    """Get enhanced problem detail with submission status, bookmarks, notes."""
    collection = curated_questions_collection()

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    q = {
        "id": str(question["_id"]),
        "question_title": question.get("question_title", "Unknown"),
        "statement": question.get("statement", ""),
        "examples": question.get("examples", []),
        "constraints": question.get("constraints", []),
        "visible_test_cases": question.get("visible_test_cases", []),
        "difficulty": question.get("difficulty", "medium"),
        "topic": question.get("topic", "Unknown"),
        "topics": question.get("topics", []),
        "company": question.get("company", []),
        "company_frequency": question.get("company_frequency", {}),
        "hints": question.get("hints", []),
        "approaches": question.get("approaches", []),
        "video_urls": question.get("video_urls", []),
        "leetcode_url": question.get("leetcode_url", ""),
        "acceptance_rate": question.get("acceptance_rate", 0),
        "total_submissions": question.get("total_submissions", 0),
    }

    # Get solved status
    solved = await solved_problems_collection().find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })
    q["solved"] = bool(solved)
    q["solved_at"] = solved.get("solved_at").isoformat() if solved else None

    # Get bookmark status
    bookmarked = await bookmarks_collection().find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })
    q["bookmarked"] = bool(bookmarked)

    # Get note
    note = await notes_collection().find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })
    q["note"] = note.get("content", "") if note else ""

    # Hide hidden test cases and solution for free users
    plan = user.get("plan", "free")
    if plan not in ("pro", "lifetime") and not solved:
        q["hidden_test_cases"] = []
        q["solution"] = {"locked": True, "message": "Solve this problem or upgrade to Pro to unlock the solution"}
    else:
        q["hidden_test_cases"] = question.get("hidden_test_cases", [])
        q["solution"] = question.get("solution", {})

    return q


# ═══════════════════════════════════════════════════════════════════════════
# SIMILAR PROBLEMS
# ═══════════════════════════════════════════════════════════════════════════
@router.get("/problem/{question_id}/similar")
async def get_similar_problems(
    question_id: str,
    limit: int = Query(5, ge=1, le=10),
    user=Depends(get_current_user),
):
    """Get similar problems based on topic, difficulty, and companies."""
    collection = curated_questions_collection()

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    topic = question.get("topic", "")
    difficulty = question.get("difficulty", "medium")
    companies = question.get("company", [])
    topics = question.get("topics", [])

    # Build similarity query
    query = {
        "_id": {"$ne": q_oid},
        "type": "coding",
    }

    # Prefer same topic and difficulty
    similar = []

    # First: same topic, same difficulty
    if topic:
        q1 = {**query, "topic": topic, "difficulty": difficulty}
        async for doc in collection.find(q1).limit(limit):
            doc["id"] = str(doc.pop("_id"))
            doc["similarity_reason"] = f"Same topic ({topic}) and difficulty"
            similar.append(doc)

    # Second: same topic, different difficulty
    if len(similar) < limit and topic:
        q2 = {**query, "topic": topic}
        existing_ids = [s["id"] for s in similar]
        async for doc in collection.find({**q2, "_id": {"$nin": [ObjectId(i) for i in existing_ids] if existing_ids else []}}).limit(limit - len(similar)):
            doc["id"] = str(doc.pop("_id"))
            if doc["id"] not in existing_ids:
                doc["similarity_reason"] = f"Same topic ({topic})"
                similar.append(doc)

    # Third: same companies
    if len(similar) < limit and companies:
        existing_ids = [s["id"] for s in similar]
        q3 = {**query, "company": {"$in": companies[:3]}}
        if existing_ids:
            q3["_id"]["$in"] = []
            q3["_id"]["$nin"] = [ObjectId(i) for i in existing_ids]
        async for doc in collection.find(q3).limit(limit - len(similar)):
            doc["id"] = str(doc.pop("_id"))
            if doc["id"] not in existing_ids:
                doc["similarity_reason"] = f"Asked at {', '.join(companies[:2])}"
                similar.append(doc)

    return {
        "similar_problems": similar[:limit],
        "total": len(similar),
    }


# ═══════════════════════════════════════════════════════════════════════════
# ACCEPTANCE RATE
# ═══════════════════════════════════════════════════════════════════════════
@router.get("/problem/{question_id}/acceptance")
async def get_acceptance_rate(question_id: str, user=Depends(get_current_user)):
    """Get acceptance rate and submission count for a problem."""
    collection = curated_questions_collection()

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    total_submissions = question.get("total_submissions", 0)
    total_accepted = question.get("total_accepted", 0)
    acceptance_rate = round(total_accepted / max(total_submissions, 1) * 100, 1)

    return {
        "question_id": question_id,
        "acceptance_rate": acceptance_rate,
        "total_submissions": total_submissions,
        "total_accepted": total_accepted,
    }
