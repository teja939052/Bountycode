"""
Personal Dashboard routes — weak area analysis, personalized recommendations.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from typing import Dict, List
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection,
    question_answers_collection, users_collection
)
from app.services.readiness_engine import compute_readiness

router = APIRouter(prefix="/api/v1/dashboard", tags=["personal-dashboard"])


@router.get("/personal")
async def get_personal_dashboard(user=Depends(get_current_user)):
    """Get comprehensive personal dashboard with weak area analysis."""
    # All question content resolved from the in-memory canonical store
    # (Residency Rule): never MongoDB.
    from app.services import question_store
    solved_col = solved_problems_collection()
    answers_col = question_answers_collection()
    uid = user["id"]

    # Solved stats per topic/difficulty with avg score
    solved_stats = {}
    async for s in solved_col.find({"user_id": uid}):
        q = question_store.find_one({"id": str(s.get("question_id", ""))})
        if not q:
            continue
        topic = q.get("topic", "General")
        diff = q.get("difficulty", "medium")
        entry = solved_stats.setdefault(
            topic, {"easy": 0, "medium": 0, "hard": 0, "total": 0, "_scores": []}
        )
        if diff in ("easy", "medium", "hard"):
            entry[diff] += 1
        entry["total"] += 1
        if isinstance(s.get("score"), (int, float)):
            entry["_scores"].append(s["score"])
    for entry in solved_stats.values():
        scores = entry.pop("_scores")
        entry["avg_score"] = round(sum(scores) / len(scores), 1) if scores else 0

    # Total problems per topic (whole in-memory store, first-seen order)
    topic_totals = {}
    for q in question_store.find().prefer_verified().to_list():
        t = q.get("topic", "General")
        if t not in topic_totals:
            topic_totals[t] = {"total": 0, "topic_order": q.get("topic_order", "")}
        topic_totals[t]["total"] += 1

    # Analyze weak areas
    weak_areas = []
    strong_areas = []
    for topic, total_data in topic_totals.items():
        solved = solved_stats.get(topic, {})
        solved_count = solved.get("total", 0)
        total = total_data["total"]
        percentage = (solved_count / total * 100) if total > 0 else 0
        avg_score = solved.get("avg_score", 0)

        topic_analysis = {
            "topic": topic,
            "solved": solved_count,
            "total": total,
            "percentage": round(percentage, 1),
            "avg_score": round(avg_score, 1),
            "difficulty_breakdown": {
                "easy": {"solved": solved.get("easy", 0), "total": 0},
                "medium": {"solved": solved.get("medium", 0), "total": 0},
                "hard": {"solved": solved.get("hard", 0), "total": 0},
            }
        }

        if percentage < 30:
            weak_areas.append(topic_analysis)
        elif percentage >= 70:
            strong_areas.append(topic_analysis)

    # Sort weak areas by percentage (lowest first)
    weak_areas.sort(key=lambda x: x["percentage"])

    # Recent activity: latest answers joined to in-memory questions
    recent_activity = []
    cursor = answers_col.find({"user_id": uid}).sort("created_at", -1).limit(10)
    async for doc in cursor:
        q = question_store.find_one({"id": str(doc.get("question_id", ""))}) or {}
        recent_activity.append({
            "_id": str(doc["_id"]),
            "question_title": q.get("question_title", "Unknown"),
            "topic": q.get("topic", "General"),
            "difficulty": q.get("difficulty", "medium"),
            "score": doc.get("score"),
            "is_correct": doc.get("is_correct"),
            "created_at": doc.get("created_at"),
        })

    # Generate personalized recommendations
    recommendations = []

    # Recommend weak topics
    if weak_areas:
        recommendations.append({
            "type": "practice",
            "priority": "high",
            "title": f"Focus on {weak_areas[0]['topic']}",
            "description": f"You've only solved {weak_areas[0]['solved']}/{weak_areas[0]['total']} problems in {weak_areas[0]['topic']}. Practice more to improve.",
            "action": f"/problems/{weak_areas[0]['topic']}",
        })

    # Recommend difficulty progression
    for topic, data in solved_stats.items():
        if data["easy"] > 0 and data["medium"] == 0:
            recommendations.append({
                "type": "progression",
                "priority": "medium",
                "title": f"Try Medium problems in {topic}",
                "description": f"You've solved {data['easy']} easy problems in {topic}. Time to level up!",
                "action": f"/problems/{topic}",
            })

    # Daily goal recommendation
    total_solved = sum(s.get("total", 0) for s in solved_stats.values())
    if total_solved < 10:
        recommendations.append({
            "type": "streak",
            "priority": "high",
            "title": "Start a Daily Streak",
            "description": "Solve at least 2 problems every day to build consistency.",
            "action": "/problems",
        })

    readiness = await compute_readiness(uid)
    readiness_score = readiness.get("overall_readiness", 0)

    return {
        "readiness_score": readiness_score,
        "total_solved": total_solved_all,
        "total_problems": total_problems,
        "weak_areas": weak_areas[:5],
        "strong_areas": strong_areas[:5],
        "recent_activity": recent_activity,
        "recommendations": recommendations[:5],
        "topic_progress": [
            {
                "topic": topic,
                "solved": solved_stats.get(topic, {}).get("total", 0),
                "total": data["total"],
                "percentage": round(solved_stats.get(topic, {}).get("total", 0) / data["total"] * 100, 1) if data["total"] > 0 else 0,
            }
            for topic, data in sorted(topic_totals.items(), key=lambda x: x[1]["topic_order"])
        ],
    }


@router.get("/weak-areas")
async def get_weak_areas(top_n: int = 5, user=Depends(get_current_user)):
    """Get user's weak areas with specific problem recommendations."""
    # In-memory canonical store only (Residency Rule): never MongoDB.
    from app.services import question_store
    solved_col = solved_problems_collection()
    uid = user["id"]

    # Solved problems per topic
    solved_counts = {}
    solved_ids = set()
    async for s in solved_col.find({"user_id": uid}):
        solved_ids.add(str(s.get("question_id", "")))
        q = question_store.find_one({"id": str(s.get("question_id", ""))})
        if not q:
            continue
        t = q.get("topic", "General")
        solved_counts[t] = solved_counts.get(t, 0) + 1

    # All topics with totals (whole in-memory store)
    topic_totals = {}
    for q in question_store.find().prefer_verified().to_list():
        t = q.get("topic", "General")
        topic_totals[t] = topic_totals.get(t, 0) + 1
    weak_areas = []
    for topic, total in topic_totals.items():
        solved = solved_counts.get(topic, 0)
        percentage = (solved / total * 100) if total > 0 else 0

        if percentage < 50:  # Less than 50% solved
            # Unsolved problems in this topic (in-memory, verified first)
            unsolved = []
            for q in question_store.find({"topic": topic}).prefer_verified().to_list():
                if str(q.get("id")) not in solved_ids:
                    doc = question_store.get_question_for_serving(q.get("id")) or dict(q)
                    doc["id"] = str(q.get("id", ""))
                    unsolved.append(doc)
                if len(unsolved) >= 5:
                    break

            weak_areas.append({
                "topic": topic,
                "solved": solved,
                "total": total,
                "percentage": round(percentage, 1),
                "recommended_problems": unsolved,
            })

    weak_areas.sort(key=lambda x: x["percentage"])
    return {"weak_areas": weak_areas[:top_n]}


@router.get("/recommendations")
async def get_recommendations(user=Depends(get_current_user)):
    """Get personalized study recommendations."""
    # In-memory canonical store only (Residency Rule): never MongoDB.
    from app.services import question_store
    solved_col = solved_problems_collection()
    uid = user["id"]

    # Strengths/weaknesses from solved history joined to memory questions
    stats = {}
    async for s in solved_col.find({"user_id": uid}):
        q = question_store.find_one({"id": str(s.get("question_id", ""))})
        if not q:
            continue
        topic = q.get("topic", "General")
        diff = q.get("difficulty", "medium")
        if topic not in stats:
            stats[topic] = {"easy": 0, "medium": 0, "hard": 0}
        if diff in stats[topic]:
            stats[topic][diff] += 1

    recommendations = []

    # Find topics where user can progress
    for topic, data in stats.items():
        if data["hard"] > 0:
            recommendations.append({
                "type": "mastery",
                "message": f"Great job mastering {topic}! Try helping others in study groups.",
                "priority": "low",
            })
        elif data["medium"] > 0 and data["hard"] == 0:
            recommendations.append({
                "type": "challenge",
                "message": f"You're doing well in {topic}! Challenge yourself with hard problems.",
                "priority": "medium",
                "action": f"/problems/{topic}",
            })
        elif data["easy"] > 0 and data["medium"] == 0:
            recommendations.append({
                "type": "progression",
                "message": f"Level up your {topic} skills with medium difficulty problems.",
                "priority": "high",
                "action": f"/problems/{topic}",
            })

    # General recommendations
    total_solved = sum(sum(d.values()) for d in stats.values())
    if total_solved == 0:
        recommendations.append({
            "type": "start",
            "message": "Welcome! Start with Arrays problems to build your foundation.",
            "priority": "high",
            "action": "/problems/Arrays",
        })
    elif total_solved < 20:
        recommendations.append({
            "type": "consistency",
            "message": f"You've solved {total_solved} problems. Keep going! Aim for 2 per day.",
            "priority": "medium",
        })
    elif total_solved < 100:
        recommendations.append({
            "type": "milestone",
            "message": f"Great progress with {total_solved} problems! You're building strong foundations.",
            "priority": "low",
        })

    return {"recommendations": recommendations[:10]}
