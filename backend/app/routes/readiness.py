"""Placement Readiness Score — deterministic readiness calculation from user data.

Provides GET /api/v1/readiness/score for full breakdown and
GET /api/v1/readiness/company/{company} for company-specific analysis.
All scoring is pure math — zero AI dependency.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection,
    submissions_collection,
    aptitude_tests_collection,
    interviews_collection,
    resumes_collection,
    generated_projects_collection,
    question_answers_collection,
)
from app.services.readiness_engine import (
    calculate_readiness,
    predict_readiness_date,
    COMPANY_PROFILES,
)

router = APIRouter(prefix="/api/v1/readiness", tags=["readiness"])


async def _gather_dsa_data(uid: str) -> dict:
    """Gather DSA performance data from solved_problems + curated_questions lookup."""
    solved_col = solved_problems_collection()

    total_solved = await solved_col.count_documents({"user_id": uid})

    # Difficulty breakdown via aggregation with curated_questions join
    diff_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": "$question.difficulty",
            "count": {"$sum": 1},
        }},
    ]
    diff_stats = {}
    async for doc in solved_col.aggregate(diff_pipeline):
        if doc["_id"]:
            diff_stats[doc["_id"]] = doc["count"]

    # Topic breakdown
    topic_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$question.topic", "count": {"$sum": 1}}},
    ]
    unique_topics = set()
    async for doc in solved_col.aggregate(topic_pipeline):
        if doc["_id"]:
            unique_topics.add(doc["_id"])

    # Accuracy from submissions
    subs_col = submissions_collection()
    total_subs = await subs_col.count_documents({"user_id": uid})
    passed_subs = await subs_col.count_documents({"user_id": uid, "status": "passed"})
    accuracy_rate = passed_subs / total_subs if total_subs > 0 else 0.0

    return {
        "total_solved": total_solved,
        "easy": diff_stats.get("easy", 0),
        "medium": diff_stats.get("medium", 0),
        "hard": diff_stats.get("hard", 0),
        "unique_topics": len(unique_topics),
        "accuracy_rate": accuracy_rate,
    }


async def _gather_aptitude_data(uid: str) -> dict:
    """Gather aptitude test performance data."""
    apt_col = aptitude_tests_collection()
    pipeline = [
        {"$match": {"user_id": uid, "status": "completed"}},
        {"$group": {
            "_id": "$category",
            "avg_pct": {"$avg": "$percentage"},
            "count": {"$sum": 1},
            "latest_pct": {"$max": "$completed_at"},
        }},
        {"$sort": {"latest_pct": -1}},
    ]

    category_data = {}
    total_count = 0
    async for doc in apt_col.aggregate(pipeline):
        cat = doc["_id"] or "general"
        category_data[cat] = {"avg": doc.get("avg_pct", 0), "count": doc.get("count", 0)}
        total_count += doc.get("count", 0)

    # Recent percentages across all categories
    recent_cursor = apt_col.find(
        {"user_id": uid, "status": "completed"},
        {"percentage": 1, "_id": 0},
    ).sort("completed_at", -1).limit(10)
    recent_pcts = [doc.get("percentage", 0) async for doc in recent_cursor]

    overall_avg = sum(c["avg"] * c["count"] for c in category_data.values()) / total_count if total_count > 0 else 0

    return {
        "avg_percentage": overall_avg,
        "test_count": total_count,
        "category_count": len(category_data),
        "recent_percentages": recent_pcts,
    }


async def _gather_cs_fundamentals_data(uid: str) -> dict:
    """Gather CS fundamentals data from interview answers tagged with technical topics."""
    ans_col = question_answers_collection()

    pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {
            "_id": None,
            "count": {"$sum": 1},
            "avg_score": {"$avg": "$score"},
        }},
    ]
    total_data = {"cs_question_count": 0, "avg_score": 0.0}

    async for doc in ans_col.aggregate(pipeline):
        total_data["cs_question_count"] = doc.get("count", 0)
        total_data["avg_score"] = doc.get("avg_score", 0.0)

    # Topic-level scores from question_answers
    topic_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": "$question.topic",
            "avg_score": {"$avg": "$score"},
            "count": {"$sum": 1},
        }},
    ]
    topic_scores = {}
    async for doc in ans_col.aggregate(topic_pipeline):
        if doc["_id"]:
            topic_scores[doc["_id"]] = doc.get("avg_score", 0)

    return {
        "cs_question_count": total_data["cs_question_count"],
        "avg_score": total_data["avg_score"],
        "topic_scores": topic_scores,
    }


async def _gather_coding_data(uid: str) -> dict:
    """Gather coding submission performance data."""
    subs_col = submissions_collection()
    total = await subs_col.count_documents({"user_id": uid})
    passed = await subs_col.count_documents({"user_id": uid, "status": "passed"})

    # Language diversity
    lang_pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {"_id": "$language"}},
    ]
    languages = set()
    async for doc in subs_col.aggregate(lang_pipeline):
        if doc["_id"]:
            languages.add(doc["_id"])

    # Recent success rate (last 20 submissions)
    recent_cursor = subs_col.find(
        {"user_id": uid},
        {"status": 1, "_id": 0},
    ).sort("submitted_at", -1).limit(20)
    recent_statuses = [doc.get("status", "") async for doc in recent_cursor]
    recent_passed = sum(1 for s in recent_statuses if s == "passed")
    recent_rate = recent_passed / len(recent_statuses) if recent_statuses else 0.0

    return {
        "total_submissions": total,
        "passed_submissions": passed,
        "languages_used": len(languages),
        "recent_success_rate": recent_rate,
    }


async def _gather_interview_data(uid: str) -> dict:
    """Gather interview performance data."""
    int_col = interviews_collection()

    pipeline = [
        {"$match": {"user_id": uid, "status": "completed"}},
        {"$group": {
            "_id": None,
            "count": {"$sum": 1},
            "avg_score": {"$avg": "$score_history"},
        }},
    ]
    summary = {"completed_count": 0, "avg_score": 0.0}
    async for doc in int_col.aggregate(pipeline):
        summary["completed_count"] = doc.get("count", 0)
        # avg_score from score_history arrays
        all_scores = doc.get("avg_score", 0)
        summary["avg_score"] = all_scores if isinstance(all_scores, (int, float)) else 0

    # Get individual interview final scores for recent trend
    cursor = int_col.find(
        {"user_id": uid, "status": "completed"},
        {"score_history": 1, "_id": 0},
    ).sort("created_at", -1).limit(10)

    recent_scores = []
    async for doc in cursor:
        scores = doc.get("score_history", [])
        if scores:
            recent_scores.append(sum(scores) / len(scores))

    # Recalculate avg from individual docs if aggregate didn't work well
    if recent_scores:
        summary["avg_score"] = sum(recent_scores) / len(recent_scores)

    return {
        "completed_count": summary["completed_count"],
        "avg_score": summary["avg_score"],
        "recent_scores": recent_scores,
        "company_breakdown": {},
    }


async def _gather_resume_data(uid: str) -> dict:
    """Gather resume/ATS performance data."""
    resume_col = resumes_collection()

    pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {
            "_id": None,
            "count": {"$sum": 1},
            "avg_ats": {"$avg": "$ats_score"},
            "max_ats": {"$max": "$ats_score"},
            "opt_count": {
                "$sum": {"$cond": [{"$ne": ["$optimized_text", None]}, 1, 0]},
            },
        }},
    ]
    result = {"resume_count": 0, "avg_ats_score": 0.0, "best_ats_score": 0.0, "optimization_count": 0}
    async for doc in resume_col.aggregate(pipeline):
        result["resume_count"] = doc.get("count", 0)
        result["avg_ats_score"] = doc.get("avg_ats", 0) or 0
        result["best_ats_score"] = doc.get("max_ats", 0) or 0
        result["optimization_count"] = doc.get("opt_count", 0)

    return result


async def _gather_project_data(uid: str) -> dict:
    """Gather project generation data."""
    proj_col = generated_projects_collection()

    total = await proj_col.count_documents({"user_id": uid})

    if total == 0:
        return {"project_count": 0, "avg_file_count": 0.0, "with_tech_stack": 0, "reviewed_count": 0, "avg_review_score": 0.0}

    pipeline = [
        {"$match": {"user_id": uid}},
        {"$project": {
            "file_count": {"$size": {"$ifNull": ["$files", []]}},
            "has_tech_stack": {"$gt": [{"$size": {"$ifNull": ["$tech_stack", []]}}, 0]},
            "has_review": {"$gt": [{"$size": {"$ifNull": ["$review_score", []]}}, 0]},
            "review_score": {"$avg": "$review_score"},
        }},
        {"$group": {
            "_id": None,
            "count": {"$sum": 1},
            "avg_files": {"$avg": "$file_count"},
            "with_stack": {"$sum": {"$cond": ["$has_tech_stack", 1, 0]}},
            "reviewed": {"$sum": {"$cond": ["$has_review", 1, 0]}},
            "avg_review": {"$avg": "$review_score"},
        }},
    ]
    result = {"project_count": total, "avg_file_count": 0.0, "with_tech_stack": 0, "reviewed_count": 0, "avg_review_score": 0.0}
    async for doc in proj_col.aggregate(pipeline):
        result["avg_file_count"] = doc.get("avg_files", 0) or 0
        result["with_tech_stack"] = doc.get("with_stack", 0)
        result["reviewed_count"] = doc.get("reviewed", 0)
        result["avg_review_score"] = doc.get("avg_review", 0) or 0

    return result


@router.get("/score")
async def get_readiness_score(
    company: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get comprehensive placement readiness score with full breakdown.

    Returns scores for 7 categories (dsa, aptitude, cs_fundamentals, coding,
    interview, resume, projects) weighted into an overall score 0-100.
    Optionally includes company-specific readiness assessment.
    """
    uid = user["id"]

    # Gather all data in parallel-ish (sequential but batched)
    dsa_data = await _gather_dsa_data(uid)
    aptitude_data = await _gather_aptitude_data(uid)
    cs_data = await _gather_cs_fundamentals_data(uid)
    coding_data = await _gather_coding_data(uid)
    interview_data = await _gather_interview_data(uid)
    resume_data = await _gather_resume_data(uid)
    project_data = await _gather_project_data(uid)

    result = calculate_readiness(
        dsa_data=dsa_data,
        aptitude_data=aptitude_data,
        cs_data=cs_data,
        coding_data=coding_data,
        interview_data=interview_data,
        resume_data=resume_data,
        project_data=project_data,
        company=company,
    )

    prediction = predict_readiness_date(result.overall, company)

    return {
        "overall": result.overall,
        "company": company or "general",
        "categories": {
            name: {
                "score": cat.score,
                "weight": cat.weight,
                "details": cat.details,
            }
            for name, cat in result.categories.items()
        },
        "company_score": result.company_score,
        "company_match": result.company_match,
        "recommendations": result.recommendations,
        "prediction": prediction,
        "stats": result.stats,
    }


@router.get("/company/{company_name}")
async def get_company_readiness(company_name: str, user=Depends(get_current_user)):
    """Get detailed readiness analysis for a specific company.

    Returns the full readiness breakdown with company-specific weights,
    gap analysis, and a prediction of when the user will be ready.
    """
    company_key = company_name.lower().strip()
    profile = COMPANY_PROFILES.get(company_key)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown company: {company_name}. Available: {', '.join(COMPANY_PROFILES.keys())}",
        )

    uid = user["id"]

    dsa_data = await _gather_dsa_data(uid)
    aptitude_data = await _gather_aptitude_data(uid)
    cs_data = await _gather_cs_fundamentals_data(uid)
    coding_data = await _gather_coding_data(uid)
    interview_data = await _gather_interview_data(uid)
    resume_data = await _gather_resume_data(uid)
    project_data = await _gather_project_data(uid)

    result = calculate_readiness(
        dsa_data=dsa_data,
        aptitude_data=aptitude_data,
        cs_data=cs_data,
        coding_data=coding_data,
        interview_data=interview_data,
        resume_data=resume_data,
        project_data=project_data,
        company=company_name,
    )

    prediction = predict_readiness_date(result.overall, company_name)

    return {
        "company": company_name,
        "requirements": {
            "min_problems": profile["min_solved"],
            "min_medium": profile["min_medium"],
            "min_hard": profile["min_hard"],
            "min_skills": profile["min_skills"],
            "focus_topics": profile["focus_topics"],
            "interview_rounds": profile["interview_rounds"],
            "typical_timeline": f"{profile['typical_timeline_weeks']} weeks",
        },
        "your_stats": {
            "total_problems": dsa_data.get("total_solved", 0),
            "easy": dsa_data.get("easy", 0),
            "medium": dsa_data.get("medium", 0),
            "hard": dsa_data.get("hard", 0),
            "aptitude_tests": aptitude_data.get("test_count", 0),
            "interviews_completed": interview_data.get("completed_count", 0),
            "submissions": coding_data.get("total_submissions", 0),
            "resumes": resume_data.get("resume_count", 0),
        },
        "overall_score": result.overall,
        "company_score": result.company_score,
        "company_match": result.company_match,
        "categories": {
            name: {"score": cat.score, "details": cat.details}
            for name, cat in result.categories.items()
        },
        "recommendations": result.recommendations,
        "prediction": prediction,
    }
