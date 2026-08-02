from datetime import datetime, timezone, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from bson import ObjectId
from app.database import interview_bookings_collection, interviews_collection, users_collection
from app.middleware.auth import get_current_user
from app.services.ai import evaluate_answer
from app.services.gamification import record_practice
from app.config import get_settings
from app.services.usage import can_use_feature, mark_feature_used

settings = get_settings()

router = APIRouter(prefix="/api/v1/interview-booking", tags=["interview-booking"])

INTERVIEW_TYPES = ["technical", "behavioral", "system_design", "hr", "full_round"]
DURATIONS = [15, 30, 45, 60]
COMPANIES = [
    "Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Tesla", "Nvidia",
    "Twitter/X", "LinkedIn", "Stripe", "Uber", "Airbnb", "Spotify", "Pinterest",
    "Snapchat", "TikTok", "Discord", "Slack", "Notion", "Atlassian", "Salesforce",
    "Oracle", "SAP", "IBM", "Intel", "AMD", "Qualcomm", "Broadcom", "Palantir",
    "SpaceX", "Goldman Sachs", "JPMorgan", "Morgan Stanley", "Citadel", "Two Sigma",
    "Jane Street", "Bloomberg", "TCS", "Infosys", "Wipro", "Cognizant", "HCL Tech",
    "Tech Mahindra", "L&T Infotech", "Mphasis", "Hexaware", "Accenture", "Capgemini",
    "Deloitte", "Ernst & Young", "KPMG", "PwC", "Zomato", "Razorpay", "Flipkart",
    "Swiggy", "PhonePe", "Paytm", "Adobe", "Shopify", "Twilio", "Databricks",
    "Snowflake", "Datadog", "Cloudflare", "Vercel", "Supabase",
]
ROLES = [
    "Software Engineer", "Senior Software Engineer", "Staff Engineer", "Principal Engineer",
    "Product Manager", "Senior Product Manager", "Engineering Manager", "Tech Lead",
    "Data Scientist", "Senior Data Scientist", "ML Engineer", "Data Engineer",
    "UX Designer", "Senior UX Designer", "Product Designer", "Design Lead",
    "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer",
    "Business Analyst", "Consultant", "Solution Architect", "Security Engineer",
    "Mobile Engineer", "iOS Engineer", "Android Engineer", "Frontend Engineer",
    "Backend Engineer", "Full Stack Engineer", "QA Engineer", "Tech Writer",
]


class BookInterviewRequest(BaseModel):
    type: str = Field(..., description="Interview type")
    scheduled_at: datetime = Field(..., description="Scheduled date and time")
    duration_minutes: int = Field(default=30, ge=15, le=60)
    company_target: Optional[str] = None
    role_target: Optional[str] = None
    notes: str = ""


class SubmitAnswersRequest(BaseModel):
    answers: List[dict] = Field(..., description="List of {question_id, answer_text, time_taken_seconds}")


class CancelBookingRequest(BaseModel):
    reason: Optional[str] = None


def _validate_booking_type(booking_type: str) -> str:
    if booking_type not in INTERVIEW_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid interview type. Must be one of: {', '.join(INTERVIEW_TYPES)}",
        )
    return booking_type


def _validate_duration(duration: int) -> int:
    if duration not in DURATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid duration. Must be one of: {DURATIONS}",
        )
    return duration


def _check_slot_overlap(user_id: str, scheduled_at: datetime, duration_minutes: int, exclude_id: Optional[str] = None) -> bool:
    booking_end = scheduled_at + timedelta(minutes=duration_minutes)
    query = {
        "user_id": user_id,
        "status": {"$in": ["scheduled", "in_progress"]},
        "scheduled_at": {"$lt": booking_end},
    }
    if exclude_id:
        query["_id"] = {"$ne": ObjectId(exclude_id)}

    overlap_end_query = dict(query)
    overlap_end_query["$expr"] = {
        "$lt": [
            {"$add": ["$scheduled_at", {"$multiply": ["$duration_minutes", 60000]}]},
            scheduled_at.timestamp() * 1000,
        ]
    }
    overlap_booking = interview_bookings_collection.find_one(query)
    if overlap_booking:
        return True

    return False


@router.post("/book")
async def book_interview(req: BookInterviewRequest, user=Depends(get_current_user)):
    booking_type = _validate_booking_type(req.type)
    duration = _validate_duration(req.duration_minutes)

    now = datetime.now(timezone.utc)
    scheduled_at = req.scheduled_at
    if scheduled_at.tzinfo is None:
        scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)

    if scheduled_at <= now + timedelta(minutes=5):
        raise HTTPException(
            status_code=400,
            detail="Booking must be scheduled at least 5 minutes from now",
        )

    if _check_slot_overlap(user["id"], scheduled_at, duration):
        raise HTTPException(
            status_code=409,
            detail="Time slot overlaps with an existing booking",
        )

    can_use, msg = can_use_feature(user, "interview_booking")
    if not can_use:
        raise HTTPException(status_code=403, detail=msg)

    booking_doc = {
        "user_id": user["id"],
        "type": booking_type,
        "status": "scheduled",
        "scheduled_at": scheduled_at,
        "duration_minutes": duration,
        "ai_mistake": None,
        "ai_feedback": None,
        "questions_asked": [],
        "overall_score": None,
        "recorded_notes": req.notes,
        "company_target": req.company_target,
        "role_target": req.role_target,
        "reminder_sent": False,
        "reminder_at": None,
        "created_at": now,
        "updated_at": now,
    }

    result = await interview_bookings_collection.insert_one(booking_doc)
    booking_id = str(result.inserted_id)

    await mark_feature_used(user["id"], "interview_booking")

    return {
        "booking_id": booking_id,
        "type": booking_type,
        "scheduled_at": scheduled_at.isoformat(),
        "duration": duration,
        "status": "scheduled",
        "company_target": req.company_target,
        "role_target": req.role_target,
        "confirmation_message": f"Mock interview booked for {scheduled_at.strftime('%B %d, %Y at %I:%M %p')}. You will receive a reminder 24 hours before.",
    }


@router.get("/upcoming")
async def get_upcoming_bookings(user=Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    cursor = interview_bookings_collection.find(
        {
            "user_id": user["id"],
            "status": {"$in": ["scheduled", "in_progress"]},
            "scheduled_at": {"$gte": now},
        },
        {"_id": 0},
    ).sort("scheduled_at", 1)

    bookings = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["scheduled_at"] = doc["scheduled_at"].isoformat() if isinstance(doc["scheduled_at"], datetime) else doc["scheduled_at"]
        del doc["_id"]
        bookings.append(doc)

    return {"bookings": bookings, "total": len(bookings)}


@router.get("/history")
async def get_booking_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    status: Optional[str] = Query(None, enum=["scheduled", "completed", "cancelled", "no_show"]),
    user=Depends(get_current_user),
):
    query = {"user_id": user["id"]}
    if status:
        query["status"] = status

    total = await interview_bookings_collection.count_documents(query)
    skip = (page - 1) * limit

    cursor = interview_bookings_collection.find(query, {"_id": 0}).skip(skip).limit(limit).sort("scheduled_at", -1)

    bookings = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["scheduled_at"] = doc["scheduled_at"].isoformat() if isinstance(doc["scheduled_at"], datetime) else doc["scheduled_at"]
        del doc["_id"]
        bookings.append(doc)

    return {"bookings": bookings, "total": total, "page": page, "limit": limit}


@router.get("/{booking_id}")
async def get_booking_detail(booking_id: str, user=Depends(get_current_user)):
    try:
        booking = await interview_bookings_collection.find_one({"_id": ObjectId(booking_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    booking["id"] = str(booking["_id"])
    if isinstance(booking.get("scheduled_at"), datetime):
        booking["scheduled_at"] = booking["scheduled_at"].isoformat()
    if isinstance(booking.get("created_at"), datetime):
        booking["created_at"] = booking["created_at"].isoformat()
    if isinstance(booking.get("updated_at"), datetime):
        booking["updated_at"] = booking["updated_at"].isoformat()
    if isinstance(booking.get("reminder_at"), datetime):
        booking["reminder_at"] = booking["reminder_at"].isoformat()
    if isinstance(booking.get("scheduled_at"), datetime):
        pass

    del booking["_id"]
    return booking


@router.post("/{booking_id}/start")
async def start_booking(booking_id: str, user=Depends(get_current_user)):
    try:
        booking = await interview_bookings_collection.find_one({"_id": ObjectId(booking_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking["status"] != "scheduled":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start a booking with status '{booking['status']}'",
        )

    now = datetime.now(timezone.utc)
    scheduled_at = booking["scheduled_at"]
    if scheduled_at.tzinfo is None:
        scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)

    time_diff = (now - scheduled_at).total_seconds()
    if time_diff < -300:
        raise HTTPException(
            status_code=400,
            detail="Interview cannot be started more than 5 minutes before scheduled time",
        )

    questions = booking.get("questions_asked", [])
    if not questions:
        questions = _generate_booking_questions(booking["type"], booking.get("company_target"), booking.get("role_target"))
        await interview_bookings_collection.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"questions_asked": questions, "updated_at": now}},
        )

    await interview_bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "in_progress", "updated_at": now}},
    )

    return {
        "booking_id": booking_id,
        "status": "in_progress",
        "questions": questions,
    }


@router.post("/{booking_id}/submit")
async def submit_booking_answers(booking_id: str, req: SubmitAnswersRequest, user=Depends(get_current_user)):
    try:
        booking = await interview_bookings_collection.find_one({"_id": ObjectId(booking_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking["status"] != "in_progress":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot submit answers for a booking with status '{booking['status']}'",
        )

    scores = []
    feedbacks = []

    for answer_entry in req.answers:
        question_id = answer_entry.get("question_id", "")
        answer_text = answer_entry.get("answer_text", "")
        time_taken = answer_entry.get("time_taken_seconds", 0)

        question = None
        for q in booking.get("questions_asked", []):
            if q.get("id") == question_id or q.get("question_id") == question_id:
                question = q
                break

        if not question:
            question = {"question": f"Question {question_id}", "id": question_id}

        try:
            feedback = await evaluate_answer(
                question.get("question", question.get("prompt", str(question))),
                answer_text,
                booking.get("role_target", "Software Engineer"),
                company=booking.get("company_target", "general"),
                question_type=booking.get("type", "technical"),
            )
        except Exception:
            feedback = {
                "score": 5,
                "strengths": ["Attempted"],
                "improvements": ["Provide more detailed answers"],
                "feedback": "",
                "reaction": "memo",
                "breakdown": {"technical": 5, "communication": 5, "problem_solving": 5},
            }

        score = feedback.get("score", 5)
        scores.append(score)
        feedbacks.append({
            "question_id": question_id,
            "question": question.get("question", question.get("prompt", "")),
            "answer": answer_text,
            "score": score,
            "feedback": feedback,
            "time_taken_seconds": time_taken,
        })

    overall_score = round(sum(scores) / len(scores), 1) if scores else 0

    updated_booking = await interview_bookings_collection.find_one({"_id": ObjectId(booking_id)})

    now = datetime.now(timezone.utc)
    await interview_bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {
            "$set": {
                "status": "completed",
                "ai_feedback": {"answers": feedbacks, "overall_score": overall_score},
                "overall_score": overall_score,
                "updated_at": now,
            }
        },
    )

    interview_doc = {
        "user_id": booking["user_id"],
        "job_role": booking.get("role_target", ""),
        "company": booking.get("company_target", "general"),
        "interview_type": booking.get("type", "technical"),
        "difficulty": "medium",
        "questions": feedbacks,
        "status": "completed",
        "score_history": scores,
        "overall_score": overall_score,
        "created_at": now,
        "booking_id": booking_id,
    }
    await interviews_collection.insert_one(interview_doc)

    gamification_result = await record_practice(
        user["id"], "interview_booking", overall_score,
    )

    badges = []
    if overall_score >= 9:
        badges.append("Interview Master")
    if overall_score >= 7:
        badges.append("Strong Performer")
    if overall_score >= 5:
        badges.append("Getting There")
    if overall_score < 5:
        badges.append("Keep Practicing")
    if len(req.answers) >= 5:
        badges.append("Full Session")

    return {
        "booking_id": booking_id,
        "overall_score": overall_score,
        "feedback": {
            "answers": feedbacks,
            "overall_score": overall_score,
            "strength_areas": feedbacks[0]["feedback"].get("strengths", []) if feedbacks else [],
            "improvement_areas": feedbacks[0]["feedback"].get("improvements", []) if feedbacks else [],
        },
        "badges": badges,
        "xp_gained": gamification_result.get("xp_gained", 0),
        "level": gamification_result.get("level", 1),
        "new_badges": gamification_result.get("new_badges", []),
        "streak": gamification_result.get("new_streak", 0),
    }


@router.post("/{booking_id}/cancel")
async def cancel_booking(booking_id: str, req: CancelBookingRequest = None, user=Depends(get_current_user)):
    try:
        booking = await interview_bookings_collection.find_one({"_id": ObjectId(booking_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking["status"] != "scheduled":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel a booking with status '{booking['status']}'",
        )

    scheduled_at = booking["scheduled_at"]
    if scheduled_at.tzinfo is None:
        scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    time_until = (scheduled_at - now).total_seconds()
    if time_until < 3600:
        raise HTTPException(
            status_code=400,
            detail="Can only cancel bookings more than 1 hour before scheduled time",
        )

    refund_credits = 0
    if booking.get("duration_minutes", 30) >= 45:
        refund_credits = 2
    elif booking.get("duration_minutes", 30) >= 30:
        refund_credits = 1

    await interview_bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "cancelled", "updated_at": now}},
    )

    return {
        "booking_id": booking_id,
        "status": "cancelled",
        "refund_credits": refund_credits,
        "cancelled_at": now.isoformat(),
    }


@router.get("/available-slots")
async def get_available_slots(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    type: Optional[str] = Query(None, description="Interview type filter"),
    user=Depends(get_current_user),
):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    booking_type = type if type in INTERVIEW_TYPES else "technical"

    start_of_day = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
    end_of_day = target_date.replace(hour=20, minute=0, second=0, microsecond=0)

    existing_bookings = []
    cursor = interview_bookings_collection.find(
        {
            "user_id": user["id"],
            "status": {"$in": ["scheduled", "in_progress"]},
            "scheduled_at": {"$gte": start_of_day, "$lt": end_of_day},
        },
        {"scheduled_at": 1, "duration_minutes": 1, "_id": 0},
    )
    async for doc in cursor:
        existing_bookings.append(doc)

    existing_ranges = []
    for b in existing_bookings:
        b_start = b["scheduled_at"]
        if b_start.tzinfo is None:
            b_start = b_start.replace(tzinfo=timezone.utc)
        b_end = b_start + timedelta(minutes=b.get("duration_minutes", 30))
        existing_ranges.append((b_start, b_end))

    available_slots = []
    current_time = start_of_day
    while current_time < end_of_day:
        slot_end = current_time + timedelta(minutes=30)
        if slot_end > end_of_day:
            break

        is_overlapping = False
        for b_start, b_end in existing_ranges:
            if current_time < b_end and slot_end > b_start:
                is_overlapping = True
                break

        if not is_overlapping:
            for duration in DURATIONS:
                slot_end_for_duration = current_time + timedelta(minutes=duration)
                if slot_end_for_duration <= end_of_day:
                    overlaps = False
                    for b_start, b_end in existing_ranges:
                        if current_time < b_end and slot_end_for_duration > b_start:
                            overlaps = True
                            break
                    if not overlaps:
                        available_slots.append({
                            "time": current_time.strftime("%H:%M"),
                            "duration": duration,
                            "type": booking_type,
                            "slot_end": slot_end_for_duration.strftime("%H:%M"),
                        })

        current_time = slot_end

    can_book_more = True
    if user.get("plan") == "free":
        today_bookings = await interview_bookings_collection.count_documents(
            {
                "user_id": user["id"],
                "status": "scheduled",
                "scheduled_at": {
                    "$gte": start_of_day,
                    "$lt": end_of_day + timedelta(days=1),
                },
            }
        )
        if today_bookings >= 1:
            can_book_more = False

    return {
        "date": date,
        "type": booking_type,
        "available_slots": available_slots,
        "can_book_more": can_book_more,
        "user_plan": user.get("plan", "free"),
    }


@router.get("/stats")
async def get_booking_stats(user=Depends(get_current_user)):
    total_booked = await interview_bookings_collection.count_documents({"user_id": user["id"]})
    completed = await interview_bookings_collection.count_documents(
        {"user_id": user["id"], "status": "completed"}
    )
    cancelled = await interview_bookings_collection.count_documents(
        {"user_id": user["id"], "status": "cancelled"}
    )
    no_show = await interview_bookings_collection.count_documents(
        {"user_id": user["id"], "status": "no_show"}
    )

    pipeline = [
        {"$match": {"user_id": user["id"], "status": "completed", "overall_score": {"$ne": None}}},
        {"$group": {
            "_id": None,
            "avg_score": {"$avg": "$overall_score"},
            "best_score": {"$max": "$overall_score"},
            "total": {"$sum": 1},
        }},
    ]
    score_stats = []
    async for doc in interview_bookings_collection.aggregate(pipeline):
        score_stats.append(doc)

    avg_score = round(score_stats[0]["avg_score"], 1) if score_stats and score_stats[0]["avg_score"] else 0.0
    best_score = score_stats[0]["best_score"] if score_stats and score_stats[0].get("best_score") else 0.0

    streak_days = 0
    from datetime import date as _date_type

    recent = await interview_bookings_collection.find(
        {"user_id": user["id"], "status": "completed"},
        {"scheduled_at": 1, "_id": 0},
    ).sort("scheduled_at", -1).limit(30).to_list(length=30)

    if recent:
        last_date = None
        consecutive = 0
        for b in sorted(recent, key=lambda x: x.get("scheduled_at", datetime.now(timezone.utc)), reverse=True):
            b_date = b.get("scheduled_at")
            if isinstance(b_date, datetime):
                b_date = b_date.date()
            elif isinstance(b_date, str):
                try:
                    b_date = datetime.fromisoformat(b_date).date()
                except Exception:
                    continue
            if not isinstance(b_date, _date_type):
                continue

            if last_date is None:
                consecutive = 1
                last_date = b_date
            elif (last_date - b_date).days == 1:
                consecutive += 1
                last_date = b_date
            elif (last_date - b_date).days == 0:
                pass
            else:
                break
        streak_days = consecutive

    return {
        "total_booked": total_booked,
        "completed": completed,
        "cancelled": cancelled,
        "no_show": no_show,
        "avg_score": avg_score,
        "best_score": best_score,
        "streak_days": streak_days,
    }


def _generate_booking_questions(booking_type: str, company: Optional[str], role: Optional[str]) -> list:
    from app.services.ai import generate_interview_question
    import asyncio

    questions = []
    num_questions = 3 if booking_type in ["hr", "behavioral"] else 5

    for i in range(num_questions):
        q_id = f"q_{i + 1}"
        questions.append({
            "id": q_id,
            "question_id": q_id,
            "type": booking_type,
            "order": i + 1,
        })

    return questions


async def _send_reminder(booking_id: str, scheduled_at: datetime, user_id: str):
    try:
        await interview_bookings_collection.update_one(
            {"_id": ObjectId(booking_id)},
            {
                "$set": {
                    "reminder_sent": True,
                    "reminder_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
    except Exception:
        pass


@router.post("/{booking_id}/no-show")
async def mark_no_show(booking_id: str, user=Depends(get_current_user)):
    try:
        booking = await interview_bookings_collection.find_one({"_id": ObjectId(booking_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking["status"] not in ("scheduled", "in_progress"):
        raise HTTPException(status_code=400, detail="Cannot mark a completed/cancelled booking as no-show")

    now = datetime.now(timezone.utc)
    await interview_bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "no_show", "updated_at": now}},
    )

    return {"booking_id": booking_id, "status": "no_show"}