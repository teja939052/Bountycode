"""
Discussion Board — Community-driven Q&A with AI-powered summaries.
Users can post solutions, ask questions, and get AI-generated summaries.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, discussions_collection,
    users_collection
)
from app.services.ai import chat_completion, parse_json

router = APIRouter(prefix="/api/v1/discussions", tags=["discussions"])


# Create discussions collection index on startup
async def init_discussions_indexes():
    from app.database import get_db
    db = get_db()
    await db["discussions"].create_index("question_id")
    await db["discussions"].create_index([("question_id", 1), ("created_at", -1)])
    await db["discussions"].create_index("user_id")
    await db["discussions"].create_index([("upvotes", -1)])


@router.post("/{question_id}")
async def create_discussion(
    question_id: str,
    content: str,
    code: Optional[str] = None,
    language: Optional[str] = None,
    discussion_type: str = "solution",  # solution, question, explanation
    user=Depends(get_current_user),
):
    """Create a new discussion post for a problem."""
    from app.database import get_db
    db = get_db()

    # Verify question exists
    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await curated_questions_collection().find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Create discussion post
    post = {
        "question_id": question_id,
        "user_id": user["id"],
        "user_name": user.get("name", "Anonymous"),
        "content": content,
        "code": code,
        "language": language,
        "discussion_type": discussion_type,
        "upvotes": 0,
        "downvotes": 0,
        "replies": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = await db["discussions"].insert_one(post)
    post["id"] = str(result.inserted_id)

    return post


@router.get("/{question_id}")
async def get_discussions(
    question_id: str,
    sort: str = "best",  # best, newest, oldest
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    """Get all discussions for a problem."""
    from app.database import get_db
    db = get_db()

    # Build sort
    if sort == "best":
        sort_stage = [("upvotes", -1), ("created_at", -1)]
    elif sort == "newest":
        sort_stage = [("created_at", -1)]
    else:
        sort_stage = [("created_at", 1)]

    skip = (page - 1) * limit
    total = await db["discussions"].count_documents({"question_id": question_id})

    cursor = db["discussions"].find(
        {"question_id": question_id}
    ).sort(sort_stage).skip(skip).limit(limit)

    posts = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        # Check if current user has voted
        doc["user_upvoted"] = user["id"] in doc.get("upvoted_by", [])
        doc["user_downvoted"] = user["id"] in doc.get("downvoted_by", [])
        posts.append(doc)

    return {
        "discussions": posts,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.post("/{discussion_id}/upvote")
async def upvote_discussion(discussion_id: str, user=Depends(get_current_user)):
    """Upvote a discussion post."""
    from app.database import get_db
    db = get_db()

    try:
        d_oid = ObjectId(discussion_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid discussion ID")

    post = await db["discussions"].find_one({"_id": d_oid})
    if not post:
        raise HTTPException(status_code=404, detail="Discussion not found")

    # Check if already upvoted
    upvoted_by = post.get("upvoted_by", [])
    if user["id"] in upvoted_by:
        # Remove upvote
        await db["discussions"].update_one(
            {"_id": d_oid},
            {"$inc": {"upvotes": -1}, "$pull": {"upvoted_by": user["id"]}}
        )
        return {"upvotes": post["upvotes"] - 1, "action": "removed"}
    else:
        # Add upvote, remove downvote if exists
        await db["discussions"].update_one(
            {"_id": d_oid},
            {
                "$inc": {"upvotes": 1, "downvotes": -1 if user["id"] in post.get("downvoted_by", []) else 0},
                "$addToSet": {"upvoted_by": user["id"]},
                "$pull": {"downvoted_by": user["id"]}
            }
        )
        return {"upvotes": post["upvotes"] + 1, "action": "added"}


@router.post("/{discussion_id}/reply")
async def add_reply(
    discussion_id: str,
    content: str,
    user=Depends(get_current_user),
):
    """Add a reply to a discussion post."""
    from app.database import get_db
    db = get_db()

    try:
        d_oid = ObjectId(discussion_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid discussion ID")

    post = await db["discussions"].find_one({"_id": d_oid})
    if not post:
        raise HTTPException(status_code=404, detail="Discussion not found")

    reply = {
        "id": str(ObjectId()),
        "user_id": user["id"],
        "user_name": user.get("name", "Anonymous"),
        "content": content,
        "upvotes": 0,
        "created_at": datetime.now(timezone.utc),
    }

    await db["discussions"].update_one(
        {"_id": d_oid},
        {"$push": {"replies": reply}}
    )

    return reply


@router.get("/{question_id}/summary")
async def get_ai_summary(question_id: str, user=Depends(get_current_user)):
    """Get AI-generated summary of top discussions."""
    from app.database import get_db
    db = get_db()

    # Get top discussions
    cursor = db["discussions"].find(
        {"question_id": question_id}
    ).sort("upvotes", -1).limit(10)

    discussions = []
    async for doc in cursor:
        discussions.append({
            "content": doc.get("content", ""),
            "code": doc.get("code", ""),
            "language": doc.get("language", ""),
            "upvotes": doc.get("upvotes", 0),
        })

    if not discussions:
        return {"summary": "No discussions yet for this problem."}

    # Get question details
    try:
        q_oid = ObjectId(question_id)
        question = await curated_questions_collection().find_one({"_id": q_oid})
        question_title = question.get("question_title", "Unknown") if question else "Unknown"
    except Exception:
        question_title = "Unknown"

    # Build AI summary prompt
    disc_text = "\n\n".join([
        f"Solution {i+1} ({d['upvotes']} upvotes):\n{d['content']}\nCode: {d['code'][:200] if d['code'] else 'N/A'}"
        for i, d in enumerate(discussions[:5])
    ])

    prompt = f"""Summarize the top community solutions for this coding problem:

Problem: {question_title}

Top Solutions:
{disc_text}

Provide a JSON response with:
{{
  "summary": "2-3 sentence summary of the main approaches discussed",
  "key_insights": ["insight1", "insight2", "insight3"],
  "common_approaches": [
    {{"name": "Approach 1", "description": "...", "complexity": "O(n)"}},
    {{"name": "Approach 2", "description": "...", "complexity": "O(n log n)"}}
  ],
  "pro_tips": ["tip1", "tip2"]
}}

Be concise and focus on the most valuable insights."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=1000,
        )
        summary = parse_json(result)
    except Exception:
        summary = {
            "summary": f"Found {len(discussions)} community solutions. Top approaches include various optimization techniques.",
            "key_insights": ["Community has shared multiple approaches", "Most solutions focus on optimal time complexity"],
            "common_approaches": [],
            "pro_tips": ["Read multiple solutions to understand different perspectives"],
        }

    return summary
