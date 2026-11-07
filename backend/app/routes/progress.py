"""
Progress Tracking & Consistency Heatmap.
Track daily activity, streaks, and provide detailed progress analytics.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection,
    submissions_collection, gamification_collection
)

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


@router.get("/heatmap")
async def get_heatmap(
    days: int = Query(365, ge=7, le=365),
    user=Depends(get_current_user),
):
    """Get consistency heatmap data for the last N days."""
    solved_col = solved_problems_collection()
    submissions_col = submissions_collection()

    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Get daily solve counts
    pipeline = [
        {"$match": {
            "user_id": user["id"],
            "solved_at": {"$gte": start_date}
        }},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$solved_at"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]

    daily_solves = {}
    async for doc in solved_col.aggregate(pipeline):
        daily_solves[doc["_id"]] = doc["count"]

    # Get daily submission counts
    submission_pipeline = [
        {"$match": {
            "user_id": user["id"],
            "submitted_at": {"$gte": start_date}
        }},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$submitted_at"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]

    daily_submissions = {}
    async for doc in submissions_col.aggregate(submission_pipeline):
        daily_submissions[doc["_id"]] = doc["count"]

    # Build heatmap data
    heatmap = []
    today = datetime.now(timezone.utc).date()
    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.isoformat()
        solves = daily_solves.get(date_str, 0)
        submissions = daily_submissions.get(date_str, 0)
        total_activity = solves + submissions

        # Determine intensity level (0-4)
        if total_activity == 0:
            level = 0
        elif total_activity <= 2:
            level = 1
        elif total_activity <= 5:
            level = 2
        elif total_activity <= 10:
            level = 3
        else:
            level = 4

        heatmap.append({
            "date": date_str,
            "solves": solves,
            "submissions": submissions,
            "total": total_activity,
            "level": level,
        })

    return {
        "heatmap": heatmap,
        "total_days": days,
        "active_days": sum(1 for h in heatmap if h["total"] > 0),
        "max_activity": max(h["total"] for h in heatmap) if heatmap else 0,
    }


@router.get("/streak")
async def get_streak(user=Depends(get_current_user)):
    """Get current and longest streaks."""
    solved_col = solved_problems_collection()

    # Get all active days
    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$solved_at"}}}},
    ]

    active_days = set()
    async for doc in solved_col.aggregate(pipeline):
        active_days.add(doc["_id"])

    if not active_days:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_active_days": 0,
        }

    # Calculate current streak (from today backwards)
    today = datetime.now(timezone.utc).date()
    current_streak = 0
    check_date = today
    while check_date.isoformat() in active_days:
        current_streak += 1
        check_date -= timedelta(days=1)

    # Calculate longest streak
    sorted_days = sorted(active_days)
    longest_streak = 1
    current = 1
    for i in range(1, len(sorted_days)):
        d1 = datetime.fromisoformat(sorted_days[i - 1]).date()
        d2 = datetime.fromisoformat(sorted_days[i]).date()
        if (d2 - d1).days == 1:
            current += 1
            longest_streak = max(longest_streak, current)
        else:
            current = 1

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_active_days": len(active_days),
    }


@router.get("/topic-progress")
async def get_topic_progress(user=Depends(get_current_user)):
    """Get detailed progress per topic with stats."""
    # In-memory canonical store only (Residency Rule): never MongoDB.
    from app.services import question_store
    solved_col = solved_problems_collection()

    # Totals per topic with difficulty split (whole in-memory store)
    topic_totals = {}
    for q in question_store.find().prefer_verified().to_list():
        t = q.get("topic", "General")
        d = q.get("difficulty", "medium")
        entry = topic_totals.setdefault(t, {"total": 0, "easy": 0, "medium": 0, "hard": 0})
        entry["total"] += 1
        if d in ("easy", "medium", "hard"):
            entry[d] += 1

    # Solved per topic/difficulty joined to memory questions
    solved_data = {}
    async for s in solved_col.find({"user_id": user["id"]}):
        q = question_store.find_one({"id": str(s.get("question_id", ""))})
        if not q:
            continue
        topic = q.get("topic", "General")
        diff = q.get("difficulty", "medium")
        if topic not in solved_data:
            solved_data[topic] = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
        if diff in ("easy", "medium", "hard"):
            solved_data[topic][diff] += 1
        solved_data[topic]["total"] += 1

    # Build response
    topics = []
    for topic, totals in topic_totals.items():
        solved = solved_data.get(topic, {"easy": 0, "medium": 0, "hard": 0, "total": 0})
        percentage = round(solved["total"] / max(totals["total"], 1) * 100, 1)

        topics.append({
            "topic": topic,
            "total": totals["total"],
            "solved": solved["total"],
            "percentage": percentage,
            "easy": {"total": totals["easy"], "solved": solved.get("easy", 0)},
            "medium": {"total": totals["medium"], "solved": solved.get("medium", 0)},
            "hard": {"total": totals["hard"], "solved": solved.get("hard", 0)},
        })

    return {"topics": topics}


@router.get("/weekly-goal")
async def get_weekly_goal(user=Depends(get_current_user)):
    """Get weekly goal progress."""
    solved_col = solved_problems_collection()

    # Get this week's solve count
    today = datetime.now(timezone.utc).date()
    week_start = today - timedelta(days=today.weekday())

    pipeline = [
        {"$match": {
            "user_id": user["id"],
            "solved_at": {"$gte": datetime.combine(week_start, datetime.min.time()).replace(tzinfo=timezone.utc)}
        }},
        {"$count": "count"}
    ]

    count = 0
    async for doc in solved_col.aggregate(pipeline):
        count = doc.get("count", 0)

    # Default goal: 7 problems per week
    goal = 7
    percentage = round(count / goal * 100, 1)

    return {
        "week_start": week_start.isoformat(),
        "solved_this_week": count,
        "weekly_goal": goal,
        "percentage": min(percentage, 100),
        "goal_met": count >= goal,
    }


@router.get("/daily-goal")
async def get_daily_goal(user=Depends(get_current_user)):
    """Get daily goal progress."""
    solved_col = solved_problems_collection()

    today = datetime.now(timezone.utc).date()

    pipeline = [
        {"$match": {
            "user_id": user["id"],
            "solved_at": {"$gte": datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)}
        }},
        {"$count": "count"}
    ]

    count = 0
    async for doc in solved_col.aggregate(pipeline):
        count = doc.get("count", 0)

    # Default goal: 2 problems per day
    goal = 2
    percentage = round(count / goal * 100, 1)

    return {
        "date": today.isoformat(),
        "solved_today": count,
        "daily_goal": goal,
        "percentage": min(percentage, 100),
        "goal_met": count >= goal,
    }


@router.get("/overview")
async def get_progress_overview(user=Depends(get_current_user)):
    """Get comprehensive progress overview."""
    # Question totals from the in-memory canonical store (Residency Rule);
    # user counts from student-state collections (unchanged).
    from app.services import question_store
    solved_col = solved_problems_collection()
    submissions_col = submissions_collection()
    gam_col = gamification_collection()

    # Basic stats
    total_problems = question_store.count_documents({"type": "coding"})
    total_solved = await solved_col.count_documents({"user_id": user["id"]})
    total_submissions = await submissions_col.count_documents({"user_id": user["id"]})
    accepted = await submissions_col.count_documents({
        "user_id": user["id"],
        "status": "Accepted"
    })

    # Gamification
    gam_doc = await gam_col.find_one({"user_id": user["id"]})
    diamonds = gam_doc.get("diamonds", 0) if gam_doc else 0
    streak = gam_doc.get("streak", 0) if gam_doc else 0

    # Difficulty breakdown of solved, joined to memory questions
    diff_stats = {}
    async for s in solved_col.find({"user_id": user["id"]}):
        q = question_store.find_one({"id": str(s.get("question_id", ""))})
        if not q:
            continue
        d = q.get("difficulty", "medium")
        diff_stats[d] = diff_stats.get(d, 0) + 1

    return {
        "total_problems": total_problems,
        "total_solved": total_solved,
        "completion_percentage": round(total_solved / max(total_problems, 1) * 100, 1),
        "total_submissions": total_submissions,
        "accepted_submissions": accepted,
        "acceptance_rate": round(accepted / max(total_submissions, 1) * 100, 1),
        "diamonds": diamonds,
        "streak": streak,
        "difficulty_breakdown": {
            "easy": diff_stats.get("easy", 0),
            "medium": diff_stats.get("medium", 0),
            "hard": diff_stats.get("hard", 0),
        },
    }
