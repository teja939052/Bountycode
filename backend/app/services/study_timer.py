"""Study Timer — session tracking with focus scoring and activity attribution."""
from datetime import datetime, timezone, timedelta
from app.database import gamification_collection


async def start_session(user_id: str, activity_type: str, topic: str = None) -> dict:
    """Start a study session. Returns session_id for later completion."""
    session_id = f"{user_id}_{int(datetime.now(timezone.utc).timestamp())}"
    doc = {
        "session_id": session_id,
        "user_id": user_id,
        "activity_type": activity_type,
        "topic": topic,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed": False,
        "duration_seconds": 0,
        "focus_score": 0,
        "pauses": 0,
    }
    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$push": {"study_sessions": {"$each": [doc], "$slice": -200}}},
        upsert=True,
    )
    return {"session_id": session_id, "started_at": doc["started_at"]}


async def pause_session(user_id: str, session_id: str) -> dict:
    """Record a pause during a session."""
    gam = await gamification_collection.find_one({"user_id": user_id})
    if not gam:
        raise ValueError("No gamification doc")
    sessions = gam.get("study_sessions", [])
    for s in sessions:
        if s["session_id"] == session_id and not s["completed"]:
            s["pauses"] = s.get("pauses", 0) + 1
            await gamification_collection.update_one(
                {"user_id": user_id},
                {"$set": {"study_sessions": sessions}},
            )
            return {"pauses": s["pauses"]}
    raise ValueError("Session not found or already completed")


async def complete_session(user_id: str, session_id: str) -> dict:
    """Complete a study session. Calculates focus score and grants XP."""
    now = datetime.now(timezone.utc)
    gam = await gamification_collection.find_one({"user_id": user_id}) or {}
    sessions = gam.get("study_sessions", [])

    target = None
    for s in sessions:
        if s["session_id"] == session_id and not s["completed"]:
            target = s
            break

    if not target:
        raise ValueError("Session not found or already completed")

    started = datetime.fromisoformat(target["started_at"])
    duration = int((now - started).total_seconds())
    target["duration_seconds"] = duration
    target["completed"] = True

    pauses = target.get("pauses", 0)
    focus_score = max(0, min(100, 100 - pauses * 10 - max(0, (duration - 3600) // 600) * 5))
    target["focus_score"] = focus_score

    xp_earned = max(5, int(duration / 60) * 2 + focus_score // 10)

    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$set": {"study_sessions": sessions}},
    )

    return {
        "session_id": session_id,
        "duration_seconds": duration,
        "duration_formatted": _format_duration(duration),
        "focus_score": focus_score,
        "pauses": pauses,
        "xp_earned": xp_earned,
    }


async def get_stats(user_id: str) -> dict:
    """Get study timer stats for the user."""
    gam = await gamification_collection.find_one({"user_id": user_id}) or {}
    sessions = [s for s in gam.get("study_sessions", []) if s.get("completed")]

    if not sessions:
        return {
            "total_sessions": 0,
            "total_seconds": 0,
            "total_formatted": "0h 0m",
            "avg_focus": 0,
            "streak_days": 0,
            "today_seconds": 0,
            "today_formatted": "0h 0m",
            "recent_sessions": [],
        }

    total_seconds = sum(s.get("duration_seconds", 0) for s in sessions)
    avg_focus = round(sum(s.get("focus_score", 0) for s in sessions) / len(sessions))

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_sessions = [
        s for s in sessions
        if datetime.fromisoformat(s["started_at"]) >= today_start
    ]
    today_seconds = sum(s.get("duration_seconds", 0) for s in today_sessions)

    streak = _calculate_streak(sessions)

    recent = sessions[-10:]
    recent.reverse()
    for s in recent:
        s["duration_formatted"] = _format_duration(s.get("duration_seconds", 0))

    return {
        "total_sessions": len(sessions),
        "total_seconds": total_seconds,
        "total_formatted": _format_duration(total_seconds),
        "avg_focus": avg_focus,
        "streak_days": streak,
        "today_seconds": today_seconds,
        "today_formatted": _format_duration(today_seconds),
        "recent_sessions": [
            {
                "session_id": s["session_id"],
                "activity_type": s.get("activity_type", "general"),
                "topic": s.get("topic"),
                "duration_seconds": s.get("duration_seconds", 0),
                "duration_formatted": s.get("duration_formatted", _format_duration(s.get("duration_seconds", 0))),
                "focus_score": s.get("focus_score", 0),
                "started_at": s.get("started_at"),
            }
            for s in recent
        ],
    }


def _format_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"


def _calculate_streak(sessions: list) -> int:
    if not sessions:
        return 0
    dates = set()
    for s in sessions:
        try:
            d = datetime.fromisoformat(s["started_at"]).date()
            dates.add(d)
        except Exception:
            continue
    if not dates:
        return 0
    streak = 0
    current = datetime.now(timezone.utc).date()
    while current in dates:
        streak += 1
        current -= timedelta(days=1)
    return streak
