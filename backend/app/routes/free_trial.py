from datetime import datetime, timezone
from fastapi import APIRouter, Request
from app.data.curriculum import get_level, get_lesson
from app.data.lesson_content import get_lesson_content

router = APIRouter(prefix="/api/v1/free-trial", tags=["free-trial"])

FREE_LESSONS = [
    {"id": "c-l01-01", "title": "What is Programming?", "type": "theory", "xp": 10, "level_id": "l01"},
    {"id": "c-l01-02", "title": "Your First C Program", "type": "practice", "xp": 10, "level_id": "l01"},
    {"id": "c-l01-03", "title": "Variables & Data", "type": "theory", "xp": 10, "level_id": "l01"},
]

CONVERSION_PROMPT = {
    "messages": [
        "You have completed 3 free lessons! You just scratched the surface.",
        "With the Pro plan, unlock all C++ and Java lessons + 50+ more features.",
        "Users who complete the free trial are 3x more likely to crack their placement interview.",
    ],
    "features": [
        "All 4 languages (C, C++, Java, Python) — 160+ levels",
        "2000+ curated placement questions",
        "AI-powered mock interviews with feedback",
        "ATS resume optimizer for tech jobs",
        "Company-specific prep for 53+ companies",
        "Gamification: XP levels, streaks, badges, leaderboards",
        "Coding compiler with real test cases",
    ],
    "pricing": {
        "pro_monthly": "$9/month",
        "lifetime": "$39 one-time",
        "student_discount": "50% off with .edu or student ID",
    },
}

TRIAL_ATTEMPTS = {}


@router.get("/lessons")
async def get_free_trial_lessons():
    lessons = []
    for fl in FREE_LESSONS:
        lesson_meta = get_lesson("c", fl["level_id"], fl["id"])
        content = get_lesson_content("c", fl["id"], fl["title"], fl["type"])
        lessons.append({
            "id": fl["id"],
            "title": fl["title"],
            "type": fl["type"],
            "xp": fl["xp"],
            "content": content,
        })
    return {"lessons": lessons, "total_lessons": len(lessons)}


@router.post("/complete")
async def complete_free_trial():
    return {
        "completed": True,
        "message": "You've completed all free lessons! Sign up to continue your journey.",
        "upgrade_url": "/register",
    }


@router.get("/conversion-prompt")
async def get_conversion_prompt():
    return CONVERSION_PROMPT


@router.post("/track-trial")
async def track_trial(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    body = await request.json()
    completed_count = body.get("completedCount", 0)
    total_count = body.get("totalCount", 3)
    conversion_signal = body.get("conversionSignal", False)

    key = client_ip
    now = datetime.now(timezone.utc).isoformat()

    if key not in TRIAL_ATTEMPTS:
        TRIAL_ATTEMPTS[key] = []

    TRIAL_ATTEMPTS[key].append({
        "timestamp": now,
        "completed_count": completed_count,
        "total_count": total_count,
        "conversion_signal": conversion_signal,
    })

    recent = TRIAL_ATTEMPTS[key][-10:]
    conversion_count = sum(1 for t in recent if t.get("conversion_signal"))

    return {
        "tracked": True,
        "timestamp": now,
        "completed_count": completed_count,
        "total_count": total_count,
        "conversion_signal": conversion_signal,
        "ip": client_ip,
    }