"""
Personal Dashboard routes — weak area analysis, personalized recommendations.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from typing import Dict, List
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, solved_problems_collection,
    question_answers_collection, users_collection
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["personal-dashboard"])


@router.get("/personal")
async def get_personal_dashboard(user=Depends(get_current_user)):
    """Get comprehensive personal dashboard with weak area analysis."""
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()
    answers_col = question_answers_collection()
    uid = user["id"]

    # Get all solved problems with their details
    solved_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {
            "_id": {
                "topic": "$question.topic",
                "difficulty": "$question.difficulty"
            },
            "count": {"$sum": 1},
            "avg_score": {"$avg": "$score"}
        }}
    ]
    solved_stats = {}
    async for doc in solved_col.aggregate(solved_pipeline):
        topic = doc["_id"]["topic"]
        diff = doc["_id"]["difficulty"]
        if topic not in solved_stats:
            solved_stats[topic] = {"easy": 0, "medium": 0, "hard": 0, "total": 0, "avg_score": 0}
        solved_stats[topic][diff] = doc["count"]
        solved_stats[topic]["total"] += doc["count"]
        solved_stats[topic]["avg_score"] = doc["avg_score"]

    # Get total problems per topic
    topic_pipeline = [
        {"$group": {"_id": "$topic", "total": {"$sum": 1}, "topic_order": {"$first": "$topic_order"}}},
        {"$sort": {"topic_order": 1}}
    ]
    topic_totals = {}
    async for doc in collection.aggregate(topic_pipeline):
        topic_totals[doc["_id"]] = {"total": doc["total"], "topic_order": doc["topic_order"]}

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

    # Get recent activity
    recent_pipeline = [
        {"$match": {"user_id": uid}},
        {"$sort": {"created_at": -1}},
        {"$limit": 10},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$project": {
            "question_title": "$question.question_title",
            "topic": "$question.topic",
            "difficulty": "$question.difficulty",
            "score": 1,
            "is_correct": 1,
            "created_at": 1
        }}
    ]
    recent_activity = []
    async for doc in answers_col.aggregate(recent_pipeline):
        doc["_id"] = str(doc.pop("_id"))
        recent_activity.append(doc)

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

    # Calculate readiness score
    total_problems = sum(t["total"] for t in topic_totals.values())
    total_solved_all = sum(s.get("total", 0) for s in solved_stats.values())
    readiness_score = round(total_solved_all / total_problems * 100, 1) if total_problems > 0 else 0

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
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()
    uid = user["id"]

    # Get solved problems per topic
    solved_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {"_id": "$question.topic", "count": {"$sum": 1}}}
    ]
    solved_counts = {}
    async for doc in solved_col.aggregate(solved_pipeline):
        solved_counts[doc["_id"]] = doc["count"]

    # Get all topics with totals
    topic_pipeline = [
        {"$group": {"_id": "$topic", "total": {"$sum": 1}, "topic_order": {"$first": "$topic_order"}}},
        {"$sort": {"topic_order": 1}}
    ]
    weak_areas = []
    async for doc in collection.aggregate(topic_pipeline):
        topic = doc["_id"]
        total = doc["total"]
        solved = solved_counts.get(topic, 0)
        percentage = (solved / total * 100) if total > 0 else 0

        if percentage < 50:  # Less than 50% solved
            # Find unsolved problems in this topic
            unsolved_cursor = collection.find(
                {"topic": topic, "_id": {"$nin": []}},
                {"question_title": 1, "difficulty": 1, "company": 1}
            ).limit(5)

            unsolved = []
            async for q in unsolved_cursor:
                q["id"] = str(q.pop("_id"))
                unsolved.append(q)

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
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()
    uid = user["id"]

    # Analyze user's strengths and weaknesses
    solved_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {
            "_id": {"topic": "$question.topic", "difficulty": "$question.difficulty"},
            "count": {"$sum": 1}
        }}
    ]
    stats = {}
    async for doc in solved_col.aggregate(solved_pipeline):
        topic = doc["_id"]["topic"]
        diff = doc["_id"]["difficulty"]
        if topic not in stats:
            stats[topic] = {"easy": 0, "medium": 0, "hard": 0}
        stats[topic][diff] = doc["count"]

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
