"""
Remaining Platform Features — Random Pick, Bookmarks, Notes, Company Filtering.
Essential LeetCode-style features for complete platform experience.
"""
from datetime import datetime, timezone
import random
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import (
    bookmarks_collection,
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
    # In-memory canonical store only (Residency Rule): verified first.
    from app.services import question_store
    base = {"type": "coding"}
    if difficulty:
        base["difficulty"] = difficulty
    if topic:
        base["topic"] = topic
    pool = question_store.find(base).prefer_verified().to_list()
    if company:
        variants = {company.lower(), company.title().lower(), company.upper().lower()}
        pool = [
            q for q in pool
            if variants & {str(c).lower() for c in (q.get("companies") or [])}
        ]
    if unsolved_only:
        solved_ids = set()
        async for doc in solved_problems_collection().find(
            {"user_id": user["id"]}, {"question_id": 1}
        ):
            solved_ids.add(str(doc["question_id"]))
        if solved_ids:
            pool = [q for q in pool if str(q.get("id")) not in solved_ids]

    def _public_pick(q: dict) -> dict:
        doc = question_store.get_question_for_serving(q.get("id")) or dict(q)
        doc["id"] = str(q.get("id", ""))
        # Mirror the legacy projection: metadata only, no grading material.
        for k in ("solution", "hidden_test_cases", "hidden_testcases"):
            doc.pop(k, None)
        return doc

    problem = None
    if pool:
        problem = _public_pick(random.choice(pool))

    if not problem:
        # Fallback: any random problem
        fb = question_store.find({"type": "coding"}).prefer_verified().to_list()
        if fb:
            problem = _public_pick(random.choice(fb))

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
        # Verify question exists in the in-memory canonical store
        # (Residency Rule): never MongoDB.
        from app.services import question_store
        question = question_store.get_question_for_serving(question_id)
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
    # In-memory verified company bank (Residency Rule): explicit company tags,
    # deterministic, no LLM.
    from app.services import question_store
    bank = question_store.company_verified_bank(company_name)
    items = [q for q in bank["items"] if q.get("type") == "coding"]
    if difficulty:
        items = [q for q in items if q.get("difficulty") == difficulty]
    if topic:
        items = [q for q in items if str(q.get("topic", "")).lower() == topic.lower()]

    # Build sort
    if sort == "difficulty":
        order = {"easy": 0, "medium": 1, "hard": 2}
        items = sorted(items, key=lambda q: order.get(q.get("difficulty"), 1))
    elif sort == "newest":
        items = sorted(items, key=lambda q: str(q.get("created_at", "")), reverse=True)
    else:  # frequency
        items = sorted(items, key=lambda q: q.get("frequency", 0), reverse=True)

    total = len(items)
    skip = (page - 1) * limit

    problems = []
    for q in items[skip:skip + limit]:
        doc = question_store.get_question_for_serving(q.get("id")) or dict(q)
        doc["id"] = str(q.get("id", ""))
        problems.append(doc)

    # Difficulty stats over the filtered set
    diff_stats = {}
    for q in items:
        d = q.get("difficulty", "medium")
        diff_stats[d] = diff_stats.get(d, 0) + 1

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
    # In-memory canonical store only (Residency Rule): never MongoDB.
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    q = {
        "id": str(question.get("id", question_id)),
        "question_title": question.get("question_title", "Unknown"),
        "statement": question.get("statement", ""),
        "examples": question.get("examples", []),
        "constraints": question.get("constraints", []),
        "visible_test_cases": question.get("visible_test_cases", []),
        "difficulty": question.get("difficulty", "medium"),
        "topic": question.get("topic", "Unknown"),
        "topics": question.get("topics") or [question.get("topic", "General")],
        "company": question.get("company", question.get("companies", [])),
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
    # In-memory canonical store only (Residency Rule): verified first.
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    topic = str(question.get("topic", "")).lower()
    difficulty = question.get("difficulty", "medium")
    companies = question.get("companies") or []
    if isinstance(companies, str):
        companies = [companies]
    legacy_co = question.get("company")
    if legacy_co:
        companies += legacy_co if isinstance(legacy_co, list) else [legacy_co]
    companies = [str(c) for c in companies if c]

    pool = [
        q for q in question_store.find({"type": "coding"}).prefer_verified().to_list()
        if str(q.get("id")) != str(question.get("id"))
    ]

    def _public(doc: dict, reason: str) -> dict:
        out = question_store.get_question_for_serving(doc.get("id")) or dict(doc)
        out["id"] = str(doc.get("id", ""))
        out["similarity_reason"] = reason
        return out

    # Prefer same topic and difficulty
    similar = []

    # First: same topic, same difficulty
    if topic:
        for doc in pool:
            if len(similar) >= limit:
                break
            if str(doc.get("topic", "")).lower() == topic and doc.get("difficulty") == difficulty:
                similar.append(_public(doc, f"Same topic ({question.get('topic')}) and difficulty"))

    # Second: same topic, different difficulty
    if len(similar) < limit and topic:
        seen = {s["id"] for s in similar}
        for doc in pool:
            if len(similar) >= limit:
                break
            if str(doc.get("id")) not in seen and str(doc.get("topic", "")).lower() == topic:
                seen.add(str(doc.get("id")))
                similar.append(_public(doc, f"Same topic ({question.get('topic')})"))

    # Third: shared company tags (pattern-relevant alignment, never asked-at claims)
    if len(similar) < limit and companies:
        wanted = {c.lower() for c in companies[:3]}
        seen = {s["id"] for s in similar}
        for doc in pool:
            if len(similar) >= limit:
                break
            tags = {str(c).lower() for c in (doc.get("companies") or [])}
            if str(doc.get("id")) not in seen and (tags & wanted):
                seen.add(str(doc.get("id")))
                similar.append(_public(
                    doc,
                    f"Shares company tags ({', '.join(companies[:2])}) — pattern-relevant",
                ))

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
    # In-memory canonical store only (Residency Rule). Note: legacy
    # per-question submission counters lived on Mongo docs; in-memory items
    # report 0 until counters are re-homed onto telemetry (student state).
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
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
