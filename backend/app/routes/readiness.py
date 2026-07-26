"""
Hiring Readiness Score — Predict when a student is ready for interviews.
AI-powered analysis of skills, progress, and company-specific requirements.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, solved_problems_collection,
    question_answers_collection, skill_graph_collection,
    gamification_collection
)

router = APIRouter(prefix="/api/readiness", tags=["readiness"])

# Company readiness requirements (based on real interview data)
COMPANY_REQUIREMENTS = {
    "google": {
        "min_solved": 300,
        "min_medium": 150,
        "min_hard": 50,
        "min_skills": {"dsa": 80, "system_design": 70, "problem_solving": 85},
        "focus_topics": ["Arrays", "Dynamic Programming", "Graphs", "Trees", "System Design"],
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Onsite (4-5 rounds)"],
        "typical_timeline_weeks": 12,
    },
    "amazon": {
        "min_solved": 250,
        "min_medium": 120,
        "min_hard": 40,
        "min_skills": {"dsa": 75, "leadership": 80, "system_design": 65},
        "focus_topics": ["Arrays", "Linked Lists", "Trees", "Dynamic Programming", "Leadership Principles"],
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Loop (5 rounds)"],
        "typical_timeline_weeks": 10,
    },
    "microsoft": {
        "min_solved": 200,
        "min_medium": 100,
        "min_hard": 30,
        "min_skills": {"dsa": 70, "system_design": 60, "problem_solving": 75},
        "focus_topics": ["Arrays", "Strings", "Trees", "Graphs", "System Design"],
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Onsite (3-4 rounds)"],
        "typical_timeline_weeks": 8,
    },
    "tcs": {
        "min_solved": 50,
        "min_medium": 20,
        "min_hard": 5,
        "min_skills": {"dsa": 50, "aptitude": 60, "verbal": 50},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
    },
    "meta": {
        "min_solved": 280,
        "min_medium": 140,
        "min_hard": 45,
        "min_skills": {"dsa": 80, "system_design": 75, "coding": 85},
        "focus_topics": ["Arrays", "Dynamic Programming", "Graphs", "System Design", "Behavioral"],
        "interview_rounds": ["Technical Phone Screen", "Onsite (Coding + System Design + Behavioral)"],
        "typical_timeline_weeks": 10,
    },
}


def calculate_readiness_score(user_stats, company=None):
    """Calculate a 0-100 readiness score based on user stats and company requirements."""
    if company and company.lower() in COMPANY_REQUIREMENTS:
        req = COMPANY_REQUIREMENTS[company.lower()]
    else:
        # Generic requirements
        req = {
            "min_solved": 150,
            "min_medium": 75,
            "min_hard": 25,
            "min_skills": {"dsa": 65, "system_design": 50, "problem_solving": 70},
            "focus_topics": ["Arrays", "Trees", "Dynamic Programming"],
            "typical_timeline_weeks": 8,
        }

    scores = []

    # Problem solving score (40% weight)
    total_solved = user_stats.get("total_solved", 0)
    medium_solved = user_stats.get("medium_solved", 0)
    hard_solved = user_stats.get("hard_solved", 0)

    problem_score = min(100, (
        (total_solved / max(req["min_solved"], 1) * 40) +
        (medium_solved / max(req["min_medium"], 1) * 35) +
        (hard_solved / max(req["min_hard"], 1) * 25)
    ))
    scores.append(("problem_solving", problem_score, 0.4))

    # Skill scores (40% weight)
    skill_scores = user_stats.get("skill_scores", {})
    skill_components = []
    for skill, min_score in req["min_skills"].items():
        user_skill = skill_scores.get(skill, 0)
        skill_components.append(min(100, user_skill / max(min_score, 1) * 100))
    skill_avg = sum(skill_components) / len(skill_components) if skill_components else 50
    scores.append(("skills", skill_avg, 0.4))

    # Topic coverage score (20% weight)
    topic_coverage = user_stats.get("topic_coverage", {})
    topics_covered = sum(1 for t in req["focus_topics"] if topic_coverage.get(t, 0) > 0)
    topic_score = (topics_covered / len(req["focus_topics"])) * 100
    scores.append(("topics", topic_score, 0.2))

    # Calculate weighted score
    total_score = sum(score * weight for _, score, weight in scores)
    return min(100, max(0, round(total_score, 1)))


def predict_readiness_date(score, target_company):
    """Predict when the user will be ready based on current score and company requirements."""
    if target_company and target_company.lower() in COMPANY_REQUIREMENTS:
        req = COMPANY_REQUIREMENTS[target_company.lower()]
    else:
        req = COMPANY_REQUIREMENTS["microsoft"]  # Default

    typical_weeks = req["typical_timeline_weeks"]

    if score >= 90:
        weeks_remaining = max(1, typical_weeks * 0.1)
    elif score >= 70:
        weeks_remaining = max(2, typical_weeks * 0.3)
    elif score >= 50:
        weeks_remaining = max(4, typical_weeks * 0.5)
    elif score >= 30:
        weeks_remaining = max(6, typical_weeks * 0.7)
    else:
        weeks_remaining = typical_weeks

    ready_date = datetime.now(timezone.utc) + timedelta(weeks=weeks_remaining)
    return {
        "weeks_remaining": round(weeks_remaining),
        "estimated_date": ready_date.strftime("%B %d, %Y"),
        "confidence": "High" if score > 60 else "Medium" if score > 30 else "Low",
    }


@router.get("/score")
async def get_readiness_score(
    company: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get comprehensive hiring readiness score with timeline prediction."""
    solved_col = solved_problems_collection()
    answers_col = question_answers_collection()
    skill_col = skill_graph_collection()
    gam_col = gamification_collection()
    uid = user["id"]

    # Gather user stats
    total_solved = await solved_col.count_documents({"user_id": uid})

    # Difficulty breakdown
    diff_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {"_id": "$question.difficulty", "count": {"$sum": 1}}}
    ]
    diff_stats = {}
    async for doc in solved_col.aggregate(diff_pipeline):
        diff_stats[doc["_id"]] = doc["count"]

    # Topic coverage
    topic_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {"_id": "$question.topic", "count": {"$sum": 1}, "avg_score": {"$avg": "$score"}}}
    ]
    topic_coverage = {}
    async for doc in solved_col.aggregate(topic_pipeline):
        topic_coverage[doc["_id"]] = {
            "count": doc["count"],
            "avg_score": doc.get("avg_score", 0),
        }

    # Skill scores from skill graph
    skill_doc = await skill_col.find_one({"user_id": uid})
    skill_scores = {}
    if skill_doc and "categories" in skill_doc:
        for cat, data in skill_doc["categories"].items():
            skill_scores[cat] = data.get("score", 0)

    # Gamification stats
    gam_doc = await gam_col.find_one({"user_id": uid})
    streak = gam_doc.get("streak", 0) if gam_doc else 0
    xp = gam_doc.get("xp", 0) if gam_doc else 0

    # Build user stats
    user_stats = {
        "total_solved": total_solved,
        "easy_solved": diff_stats.get("easy", 0),
        "medium_solved": diff_stats.get("medium", 0),
        "hard_solved": diff_stats.get("hard", 0),
        "skill_scores": skill_scores,
        "topic_coverage": {k: v["count"] for k, v in topic_coverage.items()},
        "streak": streak,
        "xp": xp,
    }

    # Calculate readiness score
    readiness_score = calculate_readiness_score(user_stats, company)

    # Predict readiness date
    prediction = predict_readiness_date(readiness_score, company)

    # Generate improvement recommendations
    recommendations = []
    if company and company.lower() in COMPANY_REQUIREMENTS:
        req = COMPANY_REQUIREMENTS[company.lower()]

        # Check problem count
        if total_solved < req["min_solved"]:
            gap = req["min_solved"] - total_solved
            recommendations.append({
                "type": "problems",
                "message": f"Solve {gap} more problems to meet {company.title()}'s requirements",
                "priority": "high",
                "target": req["min_solved"],
                "current": total_solved,
            })

        # Check hard problems
        if diff_stats.get("hard", 0) < req["min_hard"]:
            gap = req["min_hard"] - diff_stats.get("hard", 0)
            recommendations.append({
                "type": "hard_problems",
                "message": f"Solve {gap} more hard problems",
                "priority": "high",
                "target": req["min_hard"],
                "current": diff_stats.get("hard", 0),
            })

        # Check skills
        for skill, min_score in req["min_skills"].items():
            user_skill = skill_scores.get(skill, 0)
            if user_skill < min_score:
                gap = min_score - user_skill
                recommendations.append({
                    "type": "skill",
                    "message": f"Improve {skill} by {gap} points",
                    "priority": "medium",
                    "target": min_score,
                    "current": user_skill,
                })

    # Company-specific readiness for all companies
    company_readiness = {}
    for comp_name, comp_req in COMPANY_REQUIREMENTS.items():
        score = calculate_readiness_score(user_stats, comp_name)
        company_readiness[comp_name] = {
            "score": score,
            "status": "Ready" if score >= 80 else "Almost Ready" if score >= 60 else "In Progress" if score >= 40 else "Needs Work",
        }

    return {
        "readiness_score": readiness_score,
        "company": company or "general",
        "prediction": prediction,
        "recommendations": recommendations,
        "company_readiness": company_readiness,
        "stats": {
            "total_solved": total_solved,
            "easy": diff_stats.get("easy", 0),
            "medium": diff_stats.get("medium", 0),
            "hard": diff_stats.get("hard", 0),
            "streak": streak,
            "xp": xp,
            "topics_mastered": sum(1 for v in topic_coverage.values() if v["count"] >= 10),
            "total_topics": len(topic_coverage),
        },
        "score_breakdown": {
            "problem_solving": round(user_stats["easy_solved"] / max(total_solved, 1) * 100),
            "skills": round(sum(skill_scores.values()) / max(len(skill_scores), 1)),
            "topic_coverage": round(len(topic_coverage) / 15 * 100),  # 15 topics max
        },
    }


@router.get("/company/{company_name}")
async def get_company_readiness(company_name: str, user=Depends(get_current_user)):
    """Get detailed readiness analysis for a specific company."""
    req = COMPANY_REQUIREMENTS.get(company_name.lower())
    if not req:
        return {"error": f"Unknown company: {company_name}"}

    # Get main score
    score_data = await get_readiness_score(company_name, user)

    return {
        "company": company_name,
        "requirements": {
            "min_problems": req["min_solved"],
            "min_medium": req["min_medium"],
            "min_hard": req["min_hard"],
            "focus_topics": req["focus_topics"],
            "interview_rounds": req["interview_rounds"],
            "typical_timeline": f"{req['typical_timeline_weeks']} weeks",
        },
        "your_stats": score_data["stats"],
        "readiness_score": score_data["readiness_score"],
        "prediction": score_data["prediction"],
        "recommendations": score_data["recommendations"],
    }
