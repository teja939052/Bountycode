from datetime import datetime, timezone
from typing import Optional
import re
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user, require_admin
from app.database import (
    users_collection,
    content_modules_collection,
    assignments_collection,
    assignment_submissions_collection,
)
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/admin/content", tags=["admin-content"])
assignments_router = APIRouter(prefix="/api/v1/assignments", tags=["assignments"])

EDITABLE_CONTENT_FIELDS = ("title", "description", "category", "difficulty", "body", "order")


def _iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value or ""


def serialize_content(c):
    return {
        "id": str(c["_id"]),
        "title": c.get("title", ""),
        "description": c.get("description", ""),
        "category": c.get("category", ""),
        "difficulty": c.get("difficulty", ""),
        "body": c.get("body", ""),
        "order": c.get("order", 0),
        "created_at": _iso(c.get("created_at")),
        "updated_at": _iso(c.get("updated_at")),
    }


def serialize_assignment(a):
    return {
        "id": str(a["_id"]),
        "title": a.get("title", ""),
        "description": a.get("description", ""),
        "content_id": str(a["content_id"]) if a.get("content_id") else None,
        "content_title": a.get("content_title", ""),
        "assigned_to": a.get("assigned_to", []),
        "due_date": _iso(a.get("due_date")),
        "max_score": a.get("max_score", 0),
        "created_at": _iso(a.get("created_at")),
    }


def serialize_submission(s):
    return {
        "id": str(s["_id"]),
        "assignment_id": s.get("assignment_id", ""),
        "user_id": s.get("user_id", ""),
        "answer_text": s.get("answer_text", ""),
        "status": s.get("status", "submitted"),
        "score": s.get("score"),
        "feedback": s.get("feedback", ""),
        "submitted_at": _iso(s.get("submitted_at")),
        "graded_at": _iso(s.get("graded_at")),
    }


async def _find_content_or_404(content_id: str):
    try:
        content = await content_modules_collection().find_one({"_id": ObjectId(content_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Content module not found")
    if not content:
        raise HTTPException(status_code=404, detail="Content module not found")
    return content


async def _find_assignment_or_404(assignment_id: str):
    try:
        assignment = await assignments_collection().find_one({"_id": ObjectId(assignment_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.post("")
async def create_content(body: dict, admin=Depends(require_admin)):
    if not body.get("title"):
        raise HTTPException(status_code=400, detail="Missing required field: title")
    if not body.get("body"):
        raise HTTPException(status_code=400, detail="Missing required field: body")

    now = datetime.now(timezone.utc)
    content_doc = {
        "title": body["title"],
        "description": body.get("description", ""),
        "category": body.get("category", "dsa"),
        "difficulty": body.get("difficulty", "beginner"),
        "body": body["body"],
        "order": int(body.get("order", 0)),
        "created_at": now,
        "updated_at": now,
    }
    result = await content_modules_collection().insert_one(content_doc)
    content_doc["_id"] = result.inserted_id
    return serialize_content(content_doc)


@router.get("")
async def list_content(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    admin=Depends(require_admin),
):
    query = {}
    if category:
        query["category"] = category
    if search:
        safe_search = re.escape(search)
        query["$or"] = [
            {"title": {"$regex": safe_search, "$options": "i"}},
            {"description": {"$regex": safe_search, "$options": "i"}},
        ]

    total = await content_modules_collection().count_documents(query)
    cursor = content_modules_collection().find(query).sort("order", 1).skip((page - 1) * limit).limit(limit)
    content = []
    async for c in cursor:
        content.append(serialize_content(c))

    return {
        "content": content,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/{content_id}")
async def get_content(content_id: str, admin=Depends(require_admin)):
    content = await _find_content_or_404(content_id)
    return serialize_content(content)


@router.put("/{content_id}")
async def update_content(content_id: str, body: dict, admin=Depends(require_admin)):
    await _find_content_or_404(content_id)
    updates = {k: v for k, v in body.items() if k in EDITABLE_CONTENT_FIELDS}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    if "order" in updates:
        try:
            updates["order"] = int(updates["order"])
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="order must be an integer")
    updates["updated_at"] = datetime.now(timezone.utc)
    await content_modules_collection().update_one({"_id": ObjectId(content_id)}, {"$set": updates})
    updated = await content_modules_collection().find_one({"_id": ObjectId(content_id)})
    return serialize_content(updated)


@router.delete("/{content_id}")
async def delete_content(content_id: str, admin=Depends(require_admin)):
    try:
        result = await content_modules_collection().delete_one({"_id": ObjectId(content_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Content module not found")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Content module not found")
    return {"success": True}


@assignments_router.post("")
async def create_assignment(body: dict, admin=Depends(require_admin)):
    if not body.get("title"):
        raise HTTPException(status_code=400, detail="Missing required field: title")

    assigned_to = body.get("assigned_to")
    if not assigned_to:
        raise HTTPException(status_code=400, detail="Missing required field: assigned_to")
    if isinstance(assigned_to, str):
        if assigned_to.strip().lower() == "all":
            assigned_to = "all"
        else:
            assigned_to = [e.strip().lower() for e in assigned_to.replace(";", ",").split(",") if e.strip()]
    elif isinstance(assigned_to, list):
        assigned_to = [str(e).strip().lower() for e in assigned_to if str(e).strip()]
    else:
        raise HTTPException(status_code=400, detail="assigned_to must be a list of emails or 'all'")
    if not assigned_to:
        raise HTTPException(status_code=400, detail="assigned_to must not be empty")

    content_id = body.get("content_id")
    content_title = ""
    if content_id:
        content = await _find_content_or_404(content_id)
        content_title = content.get("title", "")

    due_date = None
    if body.get("due_date"):
        try:
            due_date = datetime.fromisoformat(str(body["due_date"]).replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(status_code=400, detail="due_date must be a valid ISO datetime string")

    try:
        max_score = int(body.get("max_score", 100))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="max_score must be an integer")

    assignment_doc = {
        "title": body["title"],
        "description": body.get("description", ""),
        "content_id": content_id or None,
        "content_title": content_title,
        "assigned_to": assigned_to,
        "due_date": due_date,
        "max_score": max_score,
        "created_at": datetime.now(timezone.utc),
    }
    result = await assignments_collection().insert_one(assignment_doc)
    assignment_doc["_id"] = result.inserted_id
    return serialize_assignment(assignment_doc)


@assignments_router.get("")
async def my_assignments(user=Depends(get_current_user)):
    email = user.get("email")
    query = {"$or": [{"assigned_to": "all"}]}
    if email:
        query["$or"].append({"assigned_to": email})
    user_id = str(user["_id"])

    assignments = []
    async for a in assignments_collection().find(query).sort("created_at", -1):
        item = serialize_assignment(a)
        submission = await assignment_submissions_collection().find_one(
            {"assignment_id": item["id"], "user_id": user_id}
        )
        if submission:
            item["submission_status"] = submission.get("status", "submitted")
            item["score"] = submission.get("score")
            item["feedback"] = submission.get("feedback", "")
            item["answer_text"] = submission.get("answer_text", "")
            item["submitted_at"] = _iso(submission.get("submitted_at"))
            item["graded_at"] = _iso(submission.get("graded_at"))
        else:
            item["submission_status"] = "pending"
            item["score"] = None
            item["feedback"] = ""
            item["answer_text"] = ""
            item["submitted_at"] = None
            item["graded_at"] = None
        assignments.append(item)

    return {"assignments": assignments}


@assignments_router.get("/admin")
async def admin_assignments(admin=Depends(require_admin)):
    assignments = []
    async for a in assignments_collection().find({}).sort("created_at", -1):
        item = serialize_assignment(a)
        item["submission_count"] = await assignment_submissions_collection().count_documents(
            {"assignment_id": item["id"]}
        )
        item["graded_count"] = await assignment_submissions_collection().count_documents(
            {"assignment_id": item["id"], "status": "graded"}
        )
        assignments.append(item)
    return {"assignments": assignments}


@assignments_router.post("/{assignment_id}/submit")
async def submit_assignment(assignment_id: str, body: dict, user=Depends(get_current_user)):
    assignment = await _find_assignment_or_404(assignment_id)

    email = user.get("email")
    assigned_to = assignment.get("assigned_to", [])
    if assigned_to != "all" and (not email or email not in assigned_to):
        raise HTTPException(status_code=403, detail="This assignment is not assigned to you")

    answer_text = body.get("answer_text")
    if not answer_text or not str(answer_text).strip():
        raise HTTPException(status_code=400, detail="answer_text is required")

    now = datetime.now(timezone.utc)
    filter_query = {"assignment_id": assignment_id, "user_id": str(user["_id"])}
    existing = await assignment_submissions_collection().find_one(filter_query)
    if existing:
        await assignment_submissions_collection().update_one(filter_query, {"$set": {
            "answer_text": str(answer_text).strip(),
            "status": "submitted",
            "submitted_at": now,
            "score": None,
            "feedback": "",
            "graded_at": None,
        }})
    else:
        submission_doc = {
            "assignment_id": assignment_id,
            "user_id": str(user["_id"]),
            "answer_text": str(answer_text).strip(),
            "status": "submitted",
            "submitted_at": now,
        }
        result = await assignment_submissions_collection().insert_one(submission_doc)
        submission_doc["_id"] = result.inserted_id
        try:
            await record_practice(user["id"], "assignment", 10)
        except Exception:
            pass
        return serialize_submission(submission_doc)

    updated = await assignment_submissions_collection().find_one(filter_query)
    return serialize_submission(updated)


@assignments_router.post("/{assignment_id}/review")
async def review_submission(assignment_id: str, body: dict, admin=Depends(require_admin)):
    await _find_assignment_or_404(assignment_id)

    user_id = body.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    filter_query = {"assignment_id": assignment_id, "user_id": str(user_id)}
    submission = await assignment_submissions_collection().find_one(filter_query)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found for this user")

    try:
        score = int(body.get("score", 0))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="score must be an integer")

    await assignment_submissions_collection().update_one(filter_query, {"$set": {
        "status": "graded",
        "score": score,
        "feedback": body.get("feedback", ""),
        "graded_at": datetime.now(timezone.utc),
    }})

    updated = await assignment_submissions_collection().find_one(filter_query)
    return serialize_submission(updated)


@assignments_router.get("/submissions")
async def all_submissions(
    assignment_id: Optional[str] = Query(None),
    admin=Depends(require_admin),
):
    query = {}
    if assignment_id:
        query["assignment_id"] = assignment_id

    submissions = []
    async for s in assignment_submissions_collection().find(query).sort("submitted_at", -1):
        item = serialize_submission(s)
        if ObjectId.is_valid(item["user_id"]):
            user = await users_collection().find_one({"_id": ObjectId(item["user_id"])})
            item["user_email"] = user.get("email", "") if user else ""
            item["user_name"] = user.get("name", "") if user else ""
        else:
            item["user_email"] = ""
            item["user_name"] = ""
        if ObjectId.is_valid(item["assignment_id"]):
            assignment = await assignments_collection().find_one({"_id": ObjectId(item["assignment_id"])})
            item["assignment_title"] = assignment.get("title", "") if assignment else ""
        else:
            item["assignment_title"] = ""
        submissions.append(item)

    return {"submissions": submissions}
