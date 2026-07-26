"""
Profile stats aggregation service.
Powers the Profile Sidebar with stats, streak, badges, skills, and activity heatmap.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict
from bson import ObjectId

from app.database import (
    users_collection,
    gamification_collection,
    skill_graph_collection,
    question_answers_collection,
    interviews_collection,
    resumes_collection,
    coding_challenges_collection,
    company_mock_tests_collection,
    aptitude_collection,
    system_design_collection,
)


async def get_profile_stats(user_id: str) -> Dict[str, Any]:
    uid = ObjectId(user_id)

    # 1) User basics
    user = await users_collection.find_one({"_id": uid})
    name = (user or {}).get("name", "")
    email = (user or {}).get("email", "")
    plan = (user or {}).get("plan", "free")
    avatar_url = (user or {}).get("avatar_url", "")
    github_username = (user or {}).get("github_username", "")
    leetcode_username = (user or {}).get("leetcode_username", "")

    # 2) Gamification
    gam = await gamification_collection.find_one({"user_id": user_id}) or {}
    streak = gam.get("streak", 0)
    longest_streak = gam.get("longest_streak", 0)
    xp = gam.get("xp", 0)
    level = gam.get("level", 1)

    badges_raw = gam.get("badges", [])
    if isinstance(badges_raw, list):
        badges = sorted(badges_raw, key=lambda b: b.get("earned_at", 0) if isinstance(b, dict) else 0, reverse=True)[:3]
    else:
        badges = []

    # 3) Skill graph
    skill_graph = await skill_graph_collection.find_one({"user_id": user_id}) or {}
    categories = skill_graph.get("categories", {})
    skills = {
        "dsa": categories.get("dsa", {}).get("score", 0) if isinstance(categories.get("dsa"), dict) else categories.get("dsa", 0),
        "system_design": categories.get("system_design", {}).get("score", 0) if isinstance(categories.get("system_design"), dict) else categories.get("system_design", 0),
        "behavioral": categories.get("behavioral", {}).get("score", 0) if isinstance(categories.get("behavioral"), dict) else categories.get("behavioral", 0),
        "aptitude": categories.get("aptitude", {}).get("score", 0) if isinstance(categories.get("aptitude"), dict) else categories.get("aptitude", 0),
        "resume": categories.get("resume", {}).get("score", 0) if isinstance(categories.get("resume"), dict) else categories.get("resume", 0),
    }
    overall_score = skill_graph.get("overall_score", 0)

    # 4) Counts from various collections
    total_questions = await question_answers_collection.count_documents({"user_id": user_id})
    total_interviews = await interviews_collection.count_documents({"user_id": user_id})
    total_resumes = await resumes_collection.count_documents({"user_id": user_id})
    total_coding = await coding_challenges_collection.count_documents({"user_id": user_id})
    total_mocks = await company_mock_tests_collection.count_documents({"user_id": user_id})
    total_aptitude = await aptitude_collection.count_documents({"user_id": user_id})
    total_system_design = await system_design_collection.count_documents({"user_id": user_id})

    total_solved = total_questions + total_interviews + total_coding + total_aptitude + total_system_design

    # 5) Activity heatmap (last 365 days)
    one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
    activity_map: Dict[str, int] = defaultdict(int)

    # Question answers
    cursor = question_answers_collection.find({
        "user_id": user_id,
        "created_at": {"$gte": one_year_ago},
    })
    async for doc in cursor:
        created = doc.get("created_at")
        if created:
            date_str = created.strftime("%Y-%m-%d") if isinstance(created, datetime) else str(created)[:10]
            activity_map[date_str] += 1

    # Interviews
    cursor = interviews_collection.find({
        "user_id": user_id,
        "created_at": {"$gte": one_year_ago},
    })
    async for doc in cursor:
        created = doc.get("created_at")
        if created:
            date_str = created.strftime("%Y-%m-%d") if isinstance(created, datetime) else str(created)[:10]
            activity_map[date_str] += 1

    # Coding challenges
    cursor = coding_challenges_collection.find({
        "user_id": user_id,
        "created_at": {"$gte": one_year_ago},
    })
    async for doc in cursor:
        created = doc.get("created_at")
        if created:
            date_str = created.strftime("%Y-%m-%d") if isinstance(created, datetime) else str(created)[:10]
            activity_map[date_str] += 1

    # Resumes
    cursor = resumes_collection.find({
        "user_id": user_id,
        "created_at": {"$gte": one_year_ago},
    })
    async for doc in cursor:
        created = doc.get("created_at")
        if created:
            date_str = created.strftime("%Y-%m-%d") if isinstance(created, datetime) else str(created)[:10]
            activity_map[date_str] += 1

    heatmap = [{"date": k, "count": v} for k, v in sorted(activity_map.items())]

    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "plan": plan,
        "avatar_url": avatar_url,
        "github_username": github_username,
        "leetcode_username": leetcode_username,
        "streak": streak,
        "longest_streak": longest_streak,
        "xp": xp,
        "level": level,
        "badges": badges,
        "skills": skills,
        "overall_score": overall_score,
        "total_solved": total_solved,
        "total_questions": total_questions,
        "total_interviews": total_interviews,
        "total_resumes": total_resumes,
        "total_coding": total_coding,
        "total_mocks": total_mocks,
        "total_aptitude": total_aptitude,
        "total_system_design": total_system_design,
        "heatmap": heatmap,
    }


async def update_integrations(user_id: str, platform: str, username: str) -> Dict[str, Any]:
    field = f"{platform}_username"
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {field: username}},
    )
    return {"status": "updated", "platform": platform, "username": username}
