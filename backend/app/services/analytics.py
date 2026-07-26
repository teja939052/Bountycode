"""
Analytics service — aggregates data from existing collections
to power the Analytics Dashboard.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from collections import defaultdict
from bson import ObjectId

from app.database import (
    applications_collection,
    skill_graph_collection,
    predictions_collection,
    gamification_collection,
    interviews_collection,
    resumes_collection,
    aptitude_collection,
    coding_challenges_collection,
    company_mock_tests_collection,
    question_answers_collection,
)
from app.services.placement_engine import PlacementEngine

engine = PlacementEngine()


async def get_overview(user_id: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    seven_days_ago = now - timedelta(days=7)

    apps_col = applications_collection()
    gam_col = gamification_collection()
    skill_col = skill_graph_collection()

    # Application stats
    total_apps = await apps_col.count_documents({"user_id": user_id})
    apps_30d = await apps_col.count_documents({"user_id": user_id, "created_at": {"$gte": thirty_days_ago}})
    offers = await apps_col.count_documents({"user_id": user_id, "stage": "offer_received"})
    accepted = await apps_col.count_documents({"user_id": user_id, "stage": "accepted"})

    # Gamification stats
    gam = await gam_col.find_one({"user_id": user_id}) or {}
    xp = gam.get("xp", 0)
    level = gam.get("level", 1)
    streak = gam.get("streak", 0)

    # Skill graph
    skill_graph = await skill_col.find_one({"user_id": user_id}) or {}
    overall_score = skill_graph.get("overall_score", 0)
    categories = skill_graph.get("categories", {})

    # Activity counts from various collections
    interviews_30d = await interviews_collection.count_documents({"user_id": user_id, "created_at": {"$gte": thirty_days_ago}})
    resumes_30d = await resumes_collection.count_documents({"user_id": user_id, "created_at": {"$gte": thirty_days_ago}})
    aptitude_30d = await aptitude_collection.count_documents({"user_id": user_id, "created_at": {"$gte": thirty_days_ago}})
    coding_30d = await coding_challenges_collection.count_documents({"user_id": user_id, "created_at": {"$gte": thirty_days_ago}})
    mocks_30d = await company_mock_tests_collection.count_documents({"user_id": user_id, "created_at": {"$gte": thirty_days_ago}})
    questions_30d = await question_answers_collection.count_documents({"user_id": user_id, "created_at": {"$gte": thirty_days_ago}})

    return {
        "total_applications": total_apps,
        "applications_30d": apps_30d,
        "offers_received": offers,
        "offers_accepted": accepted,
        "offer_rate": round((offers / total_apps * 100), 1) if total_apps else 0,
        "xp": xp,
        "level": level,
        "streak": streak,
        "overall_skill_score": overall_score,
        "activity_30d": {
            "interviews": interviews_30d,
            "resumes": resumes_30d,
            "aptitude": aptitude_30d,
            "coding": coding_30d,
            "mocks": mocks_30d,
            "questions": questions_30d,
            "total": interviews_30d + resumes_30d + aptitude_30d + coding_30d + mocks_30d + questions_30d,
        },
        "skill_categories": {
            cat_id: {
                "name": cat.get("name", cat_id),
                "score": cat.get("score", 0),
            }
            for cat_id, cat in categories.items()
        },
    }


async def get_funnel(user_id: str) -> Dict[str, Any]:
    apps_col = applications_collection()
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": "$stage", "count": {"$sum": 1}}},
    ]
    stage_counts: Dict[str, int] = {}
    async for doc in apps_col.aggregate(pipeline):
        stage_counts[doc["_id"]] = doc["count"]

    stages = ["interested", "applied", "oa_received", "interview_scheduled", "interview_completed", "offer_received", "accepted"]
    funnel = []
    for stage in stages:
        count = stage_counts.get(stage, 0)
        funnel.append({"stage": stage, "count": count})

    total = sum(s["count"] for s in funnel)
    for s in funnel:
        s["percentage"] = round((s["count"] / total * 100), 1) if total else 0

    return {"funnel": funnel, "total": total}


async def get_skill_progression(user_id: str, days: int = 30) -> Dict[str, Any]:
    skill_col = skill_graph_collection()
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    cursor = skill_col.find({
        "user_id": user_id,
        "updated_at": {"$gte": cutoff},
    }).sort("updated_at", 1)

    history = []
    async for doc in cursor:
        history.append({
            "date": doc.get("updated_at"),
            "overall_score": doc.get("overall_score", 0),
            "categories": {
                cat_id: cat.get("score", 0)
                for cat_id, cat in doc.get("categories", {}).items()
            },
        })

    current = await skill_col.find_one({"user_id": user_id}) or {}
    categories = current.get("categories", {})

    return {
        "history": history,
        "current": {
            "overall": current.get("overall_score", 0),
            "categories": {
                cat_id: {
                    "name": cat.get("name", cat_id),
                    "score": cat.get("score", 0),
                }
                for cat_id, cat in categories.items()
            },
        },
    }


async def get_company_stats(user_id: str) -> Dict[str, Any]:
    apps_col = applications_collection()
    pred_col = predictions_collection()

    apps_by_company: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "stages": defaultdict(int)})
    cursor = apps_col.find({"user_id": user_id})
    async for doc in cursor:
        co = doc.get("company", "Unknown")
        apps_by_company[co]["count"] += 1
        apps_by_company[co]["stages"][doc.get("stage", "unknown")] += 1

    cursor = pred_col.find({"user_id": user_id}).sort("created_at", -1).limit(50)
    predictions = []
    async for doc in cursor:
        predictions.append({
            "company": doc.get("company", ""),
            "probability": doc.get("probability", 0),
            "date": doc.get("created_at"),
            "skill_scores": doc.get("skill_scores", {}),
        })

    company_list = []
    for co, data in apps_by_company.items():
        stages = data["stages"]
        interviews = stages.get("interview_scheduled", 0) + stages.get("interview_completed", 0)
        offers = stages.get("offer_received", 0)
        company_list.append({
            "company": co,
            "total_applications": data["count"],
            "interviews": interviews,
            "offers": offers,
            "interview_rate": round((interviews / data["count"] * 100), 1) if data["count"] else 0,
            "offer_rate": round((offers / data["count"] * 100), 1) if data["count"] else 0,
        })
    company_list.sort(key=lambda x: -x["total_applications"])

    return {
        "companies": company_list,
        "predictions": predictions,
    }


async def get_insights(user_id: str) -> Dict[str, Any]:
    apps_col = applications_collection()
    pred_col = predictions_collection()

    total_apps = await apps_col.count_documents({"user_id": user_id})
    offers = await apps_col.count_documents({"user_id": user_id, "stage": "offer_received"})
    accepted = await apps_col.count_documents({"user_id": user_id, "stage": "accepted"})

    cursor = pred_col.find({"user_id": user_id}).sort("created_at", -1).limit(20)
    predictions = []
    async for doc in cursor:
        predictions.append(doc.get("probability", 0))

    avg_probability = round(sum(predictions) / len(predictions), 1) if predictions else 0
    best_company = None
    if predictions:
        best_doc = await pred_col.find_one({"user_id": user_id}, sort=[("probability", -1)])
        if best_doc:
            best_company = best_doc.get("company", "").title()

    weak_areas: List[str] = []
    skill_col = skill_graph_collection()
    skill_graph = await skill_col.find_one({"user_id": user_id}) or {}
    categories = skill_graph.get("categories", {})
    for cat_id, cat in categories.items():
        if cat.get("score", 0) < 50:
            weak_areas.append(cat.get("name", cat_id))

    return {
        "total_applications": total_apps,
        "offers_received": offers,
        "offers_accepted": accepted,
        "average_probability": avg_probability,
        "best_company": best_company,
        "weak_areas": weak_areas[:5],
        "predictions_count": len(predictions),
    }
