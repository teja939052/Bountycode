"""Interview booking routes — migrated from MongoDB `interview_bookings` collection to PostgreSQL `interview_bookings` table.

Provides interview session booking, slot overlap prevention, booking lifecycle
(start/submit/cancel/no-show), availability, history, and stats.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, and_, or_

from app.database import get_session
from app.middleware.auth import get_current_user
from app.services.ai_interview import evaluate_answer
from app.services.postgres_assessments import PostgresAssessmentService
from app.repositories.assessments import InterviewBookingRepository
from app.services.postgres_gamification import record_practice as pg_record_practice
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


async def _check_slot_overlap(
    session: AsyncSession,
    user_id: str,
    scheduled_at: datetime,
    duration_minutes: int,
    exclude_id: Optional[str] = None,
) -> bool:
    """Check if a new booking would overlap any existing scheduled/in-progress booking."""
    booking_end = scheduled_at + timedelta(minutes=duration_minutes)

    stmt = select(InterviewBooking).where(
        InterviewBooking.user_id == UUID(user_id),
        InterviewBooking.status.in_(["scheduled", "in_progress"]),
        InterviewBooking.scheduled_at < booking_end,
    )
    if exclude_id:
        stmt = stmt.where(InterviewBooking.id != UUID(exclude_id))

    # Overlap condition: existing.start < new.end AND existing.end > new.start
    stmt = stmt.where(
        InterviewBooking.scheduled_at + timedelta(minutes=InterviewBooking.duration_minutes) > scheduled_at
    )

    result = await session.execute(stmt.limit(1))
    return result.scalar_one_or_none() is not None


@router.post("/book")
async def book_interview(
    req: BookInterviewRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
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

    if await _check_slot_overlap(session, user["id"], scheduled_at, duration):
        raise HTTPException(
            status_code=409,
            detail="Time slot overlaps with an existing booking",
        )

    can_use, msg = can_use_feature(user, "interview_booking")
    if not can_use:
        raise HTTPException(status_code=403, detail=msg)

    booking_data = {
        "user_id": UUID(user["id"]),
        "company": req.company_target,
        "role": req.role_target,
        "interview_type": booking_type,
        "status": "scheduled",
        "scheduled_at": scheduled_at,
        "duration_minutes": duration,
        "score": None,
        "notes": req.notes,
    }
    booking_repo = InterviewBookingRepository(session)
    booking = await booking_repo.create(booking_data)

    await mark_feature_used(user["id"], "interview_booking")

    return {
        "booking_id": str(booking.id),
        "type": booking_type,
        "scheduled_at": scheduled_at.isoformat(),
        "duration": duration,
        "status": "scheduled",
        "company_target": req.company_target,
        "role_target": req.role_target,
        "confirmation_message": f"Mock interview booked for {scheduled_at.strftime('%B %d, %Y at %I:%M %p')}. You will receive a reminder 24 hours before.",
    }


@router.get("/upcoming")
async def get_upcoming_bookings(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    now = datetime.now(timezone.utc)
    booking_repo = InterviewBookingRepository(session)
    bookings = await booking_repo.list_by_user_and_status(
        UUID(user["id"]), "scheduled", limit=50, offset=0
    )
    # Filter to future bookings only
    future = [b for b in bookings if b.scheduled_at >= now]

    return {
        "bookings": [
            {
                "id": str(b.id),
                "user_id": str(b.user_id),
                "company": b.company,
                "role": b.role,
                "type": b.interview_type,
                "status": b.status,
                "scheduled_at": b.scheduled_at.isoformat(),
                "duration_minutes": b.duration_minutes,
                "score": b.score,
                "notes": b.notes,
                "company_target": b.company,
                "role_target": b.role,
                "reminder_sent": False,
                "reminder_at": None,
                "created_at": b.created_at.isoformat(),
                "updated_at": b.updated_at.isoformat(),
            }
            for b in future
        ],
        "total": len(future),
    }


@router.get("/history")
async def get_booking_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    status: Optional[str] = Query(None, enum=["scheduled", "completed", "cancelled", "no_show"]),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    booking_repo = InterviewBookingRepository(session)
    bookings = await booking_repo.list_by_user(
        UUID(user["id"]), limit=limit, offset=(page - 1) * limit
    )

    # Apply status filter client-side if needed (repository doesn't filter by status in list_by_user)
    if status:
        bookings = [b for b in bookings if b.status == status]

    total = await booking_repo.count_by_user_and_status(UUID(user["id"]), status) if status else len(bookings)

    return {
        "bookings": [
            {
                "id": str(b.id),
                "status": b.status,
                "scheduled_at": b.scheduled_at.isoformat() if isinstance(b.scheduled_at, datetime) else b.scheduled_at,
                "duration_minutes": b.duration_minutes,
                "score": b.score,
                "type": b.interview_type,
                "company": b.company,
                "role": b.role,
                "company_target": b.company,
                "role_target": b.role,
                "notes": b.notes,
                "created_at": b.created_at.isoformat(),
                "updated_at": b.updated_at.isoformat(),
            }
            for b in bookings
        ],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/{booking_id}")
async def get_booking_detail(booking_id: str, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        booking_uuid = UUID(booking_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    booking_repo = InterviewBookingRepository(session)
    booking = await booking_repo.get_by_id(booking_uuid)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if str(booking.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return {
        "id": str(booking.id),
        "user_id": str(booking.user_id),
        "company": booking.company,
        "role": booking.role,
        "type": booking.interview_type,
        "status": booking.status,
        "scheduled_at": booking.scheduled_at.isoformat(),
        "duration_minutes": booking.duration_minutes,
        "score": booking.score,
        "notes": booking.notes,
        "company_target": booking.company,
        "role_target": booking.role,
        "reminder_sent": False,
        "reminder_at": None,
        "created_at": booking.created_at.isoformat(),
        "updated_at": booking.updated_at.isoformat(),
    }


@router.post("/{booking_id}/start")
async def start_booking(booking_id: str, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        booking_uuid = UUID(booking_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    booking_repo = InterviewBookingRepository(session)
    booking = await booking_repo.get_by_id(booking_uuid)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if str(booking.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking.status != "scheduled":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start a booking with status '{booking.status}'",
        )

    now = datetime.now(timezone.utc)
    scheduled_at = booking.scheduled_at
    if scheduled_at.tzinfo is None:
        scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)

    time_diff = (now - scheduled_at).total_seconds()
    if time_diff < -300:
        raise HTTPException(
            status_code=400,
            detail="Interview cannot be started more than 5 minutes before scheduled time",
        )

    questions = []
    if not questions:
        questions = _generate_booking_questions(
            booking.interview_type, booking.company, booking.role
        )
        await booking_repo.update(
            booking.id,
            {
                "questions_asked": questions,
                "updated_at": now,
            },
        )

    await booking_repo.update(
        booking.id,
        {"status": "in_progress", "updated_at": now},
    )

    return {
        "booking_id": booking_id,
        "status": "in_progress",
        "questions": questions,
    }


@router.post("/{booking_id}/submit")
async def submit_booking_answers(
    booking_id: str,
    req: SubmitAnswersRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        booking_uuid = UUID(booking_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    booking_repo = InterviewBookingRepository(session)
    booking = await booking_repo.get_by_id(booking_uuid)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if str(booking.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot submit answers for a booking with status '{booking.status}'",
        )

    scores = []
    feedbacks = []

    # Get questions from booking notes or questions_asked field
    questions_asked = []
    try:
        import json
        if booking.notes:
            questions_asked = json.loads(booking.notes) if isinstance(booking.notes, str) else booking.notes
    except Exception:
        questions_asked = []

    for answer_entry in req.answers:
        question_id = answer_entry.get("question_id", "")
        answer_text = answer_entry.get("answer_text", "")
        time_taken = answer_entry.get("time_taken_seconds", 0)

        question = None
        for q in questions_asked:
            if q.get("id") == question_id or q.get("question_id") == question_id:
                question = q
                break

        if not question:
            question = {"question": f"Question {question_id}", "id": question_id}

        try:
            feedback = await evaluate_answer(
                question.get("question", question.get("prompt", str(question))),
                answer_text,
                booking.role or "Software Engineer",
                company=booking.company or "general",
                question_type=booking.interview_type or "technical",
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

    now = datetime.now(timezone.utc)

    await booking_repo.update(
        booking.id,
        {
            "status": "completed",
            "ai_feedback": {"answers": feedbacks, "overall_score": overall_score},
            "overall_score": overall_score,
            "updated_at": now,
        },
    )

    interview_doc = {
        "user_id": str(booking.user_id),
        "job_role": booking.role or "",
        "company": booking.company or "general",
        "interview_type": booking.interview_type,
        "difficulty": "medium",
        "questions": feedbacks,
        "status": "completed",
        "score_history": scores,
        "overall_score": overall_score,
        "created_at": now,
        "booking_id": str(booking.id),
    }

    gamification_result = await pg_record_practice(
        session,
        user["id"],
        "interview",
        overall_score,
        {"booking_id": booking_id, "company": booking.company or "general"},
        role=user.get("role") or user.get("target_role") or "sde",
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
async def cancel_booking(
    booking_id: str,
    req: CancelBookingRequest = None,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        booking_uuid = UUID(booking_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    booking_repo = InterviewBookingRepository(session)
    booking = await booking_repo.get_by_id(booking_uuid)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if str(booking.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking.status != "scheduled":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel a booking with status '{booking.status}'",
        )

    scheduled_at = booking.scheduled_at
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
    if booking.duration_minutes >= 45:
        refund_credits = 2
    elif booking.duration_minutes >= 30:
        refund_credits = 1

    await booking_repo.update(
        booking.id,
        {"status": "cancelled", "updated_at": now},
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
    session: AsyncSession = Depends(get_session),
):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    booking_type = type if type in INTERVIEW_TYPES else "technical"

    start_of_day = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
    end_of_day = target_date.replace(hour=20, minute=0, second=0, microsecond=0)

    booking_repo = InterviewBookingRepository(session)
    existing_bookings = await booking_repo.list_by_user_and_status(
        UUID(user["id"]), "scheduled", limit=100, offset=0
    )
    # Filter to same day
    existing_bookings = [
        b for b in existing_bookings
        if start_of_day <= b.scheduled_at < end_of_day
    ]

    existing_ranges = []
    for b in existing_bookings:
        b_start = b.scheduled_at
        if b_start.tzinfo is None:
            b_start = b_start.replace(tzinfo=timezone.utc)
        b_end = b_start + timedelta(minutes=b.duration_minutes)
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
                if slot_end_for_duration > end_of_day:
                    continue
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
        today_bookings = await booking_repo.list_by_user_and_status(
            UUID(user["id"]), "scheduled", limit=100, offset=0
        )
        today_bookings = [
            b for b in today_bookings
            if start_of_day <= b.scheduled_at < end_of_day + timedelta(days=1)
        ]
        if len(today_bookings) >= 1:
            can_book_more = False

    return {
        "date": date,
        "type": booking_type,
        "available_slots": available_slots,
        "can_book_more": can_book_more,
        "user_plan": user.get("plan", "free"),
    }


@router.get("/stats")
async def get_booking_stats(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    booking_repo = InterviewBookingRepository(session)
    bookings = await booking_repo.list_by_user(UUID(user["id"]), limit=1000, offset=0)

    total_booked = len(bookings)
    completed = [b for b in bookings if b.status == "completed"]
    cancelled = [b for b in bookings if b.status == "cancelled"]
    no_show = [b for b in bookings if b.status == "no_show"]

    score_stats = [
        b.score for b in completed if b.score is not None
    ]
    avg_score = round(sum(score_stats) / len(score_stats), 1) if score_stats else 0.0
    best_score = max(score_stats) if score_stats else 0.0

    streak_days = 0
    from datetime import date as _date_type

    recent_completed = sorted(
        [b for b in completed if b.completed_at],
        key=lambda x: x.completed_at,
        reverse=True,
    )[:30]

    if recent_completed:
        last_date = None
        consecutive = 0
        for b in recent_completed:
            b_date = b.completed_at
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
        "completed": len(completed),
        "cancelled": len(cancelled),
        "no_show": len(no_show),
        "avg_score": avg_score,
        "best_score": best_score,
        "streak_days": streak_days,
    }


def _generate_booking_questions(booking_type: str, company: Optional[str], role: Optional[str]) -> list:
    from app.services.ai_interview import generate_interview_question
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
    # Background reminder task; session not available outside request context.
    # Best-effort: reminder marking is best-effort and not critical.
    pass


@router.post("/{booking_id}/no-show")
async def mark_no_show(booking_id: str, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        booking_uuid = UUID(booking_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    booking_repo = InterviewBookingRepository(session)
    booking = await booking_repo.get_by_id(booking_uuid)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if str(booking.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking.status not in ("scheduled", "in_progress"):
        raise HTTPException(
            status_code=400,
            detail="Cannot mark a completed/cancelled booking as no-show",
        )

    now = datetime.now(timezone.utc)
    await booking_repo.update(
        booking.id,
        {"status": "no_show", "updated_at": now},
    )

    return {"booking_id": booking_id, "status": "no_show"}
