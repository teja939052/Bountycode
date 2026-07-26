"""
DSA Fingerprint + Company Predictor.
Aggregates user's solved problems into a skill fingerprint,
then calculates clearance probability for each of the 53 companies.
"""

from fastapi import APIRouter, Depends
from app.database import (
    solved_problems_collection, submissions_collection,
    curated_questions_collection, aptitude_collection,
    gamification_collection
)
from app.middleware.auth import get_current_user
from app.data.indian_companies import INDIAN_COMPANIES
from collections import defaultdict

router = APIRouter(prefix="/api/fingerprint", tags=["dsa-fingerprint"])

# Topic weights per company category
# Maps topic -> relevance weight per company category
COMPANY_TOPIC_WEIGHTS = {
    "mass_recruiter": {
        "Arrays": 0.9, "Strings": 0.8, "Math": 0.7, "Basic DS": 0.8,
        "Aptitude": 1.0, "Logical": 0.9, "English": 0.6,
        "Linked Lists": 0.5, "Trees": 0.4, "DP": 0.3, "Graphs": 0.2,
        "Sorting": 0.7, "Searching": 0.7, "Recursion": 0.4,
        "Stacks": 0.3, "Queues": 0.3, "Hashing": 0.5, "Greedy": 0.3,
        "Bit Manipulation": 0.2, "Tries": 0.1, "Heaps": 0.2,
    },
    "product_company": {
        "Arrays": 1.0, "Strings": 0.9, "Linked Lists": 0.8, "Trees": 0.9,
        "DP": 1.0, "Graphs": 0.9, "Hashing": 0.8, "Stacks": 0.7,
        "Queues": 0.6, "Greedy": 0.8, "Bit Manipulation": 0.5,
        "Tries": 0.7, "Heaps": 0.7, "Sorting": 0.6, "Searching": 0.6,
        "Recursion": 0.8, "Math": 0.5, "Backtracking": 0.7,
        "Sliding Window": 0.8, "Two Pointers": 0.8, "Binary Search": 0.7,
    },
    "global_mnc": {
        "Arrays": 1.0, "Strings": 0.9, "Linked Lists": 0.8, "Trees": 0.9,
        "DP": 1.0, "Graphs": 1.0, "Hashing": 0.8, "Stacks": 0.7,
        "Greedy": 0.8, "Tries": 0.7, "Heaps": 0.8, "Backtracking": 0.8,
        "System Design": 0.9, "Behavioral": 0.9,
    },
    "psu": {
        "Aptitude": 1.0, "Logical": 1.0, "English": 0.8,
        "Technical": 0.9, "GATE Topics": 1.0, "General Knowledge": 0.7,
    },
    "startup": {
        "Arrays": 1.0, "Strings": 0.9, "DP": 0.9, "Graphs": 0.8,
        "Hashing": 0.9, "System Design": 0.8, "Behavioral": 0.7,
        "Linked Lists": 0.7, "Trees": 0.8, "Greedy": 0.7,
    },
    "banking": {
        "Aptitude": 1.0, "Logical": 1.0, "English": 0.9,
        "Quantitative": 1.0, "Reasoning": 0.9, "General Awareness": 0.8,
    },
}

# Company category mapping
COMPANY_CATEGORIES = {
    "tcs": "mass_recruiter", "infosys": "mass_recruiter", "wipro": "mass_recruiter",
    "cognizant": "mass_recruiter", "hcl": "mass_recruiter", "accenture": "mass_recruiter",
    "capgemini": "mass_recruiter", "tech_mahindra": "mass_recruiter",
    "lti": "mass_recruiter", "mphasis": "mass_recruiter", "hexaware": "mass_recruiter",
    "cgi": "mass_recruiter", "virtusa": "mass_recruiter", "ibm": "mass_recruiter",
    "dell": "mass_recruiter", "coforge": "mass_recruiter",

    "google_india": "global_mnc", "microsoft_india": "global_mnc",
    "amazon_india": "global_mnc", "goldman_sachs": "global_mnc",
    "jp_morgan": "global_mnc",

    "flipkart": "product_company", "razorpay": "product_company",
    "zomato": "product_company", "phonepe": "product_company",
    "swiggy": "product_company", "paytm": "product_company",
    "ola": "product_company", "makemytrip": "product_company",
    "freshworks": "product_company", "zoho": "product_company",
    "byjus": "product_company", "dream11": "product_company",

    "drdo": "psu", "isro": "psu", "bel": "psu", "bhel": "psu",
    "ntpc": "psu", "sail": "psu", "iocl": "psu", "gail": "psu",

    "cars24": "startup", "meesho": "startup", "groww": "startup",
    "cred": "startup", "urban_company": "startup", "sharechat": "startup",

    "sbi": "banking", "hdfc": "banking", "icici": "banking",
    "tata_steel": "mass_recruiter", "reliance_jio": "product_company",
    "adani": "mass_recruiter",
}

# Difficulty multipliers
DIFFICULTY_WEIGHT = {"easy": 1.0, "medium": 1.5, "hard": 2.5}

# Topic name normalization
TOPIC_MAP = {
    "Arrays": ["Arrays", "Array"],
    "Strings": ["Strings", "String"],
    "Linked Lists": ["Linked Lists", "Linked List"],
    "Trees": ["Trees", "Binary Tree", "BST"],
    "DP": ["Dynamic Programming", "DP"],
    "Graphs": ["Graphs", "Graph"],
    "Hashing": ["Hashing", "Hash Map", "HashMap"],
    "Stacks": ["Stacks", "Stack"],
    "Queues": ["Queues", "Queue"],
    "Greedy": ["Greedy"],
    "Sorting": ["Sorting"],
    "Searching": ["Searching", "Binary Search"],
    "Recursion": ["Recursion"],
    "Bit Manipulation": ["Bit Manipulation", "Bits"],
    "Tries": ["Tries", "Trie"],
    "Heaps": ["Heaps", "Heap", "Priority Queue"],
    "Backtracking": ["Backtracking"],
    "Sliding Window": ["Sliding Window"],
    "Two Pointers": ["Two Pointers"],
    "Math": ["Math", "Mathematics"],
    "Basic DS": ["Basic DS", "Basic Data Structures"],
    "Aptitude": ["Aptitude", "Quantitative", "Quantitative Aptitude"],
    "Logical": ["Logical", "Logical Reasoning"],
    "English": ["English", "Verbal", "Verbal Ability"],
    "Behavioral": ["Behavioral", "HR"],
    "System Design": ["System Design", "HLD", "LLD"],
}


def normalize_topic(raw_topic: str) -> str:
    """Map a raw topic name to our canonical topic."""
    if not raw_topic:
        return "Other"
    raw_lower = raw_topic.lower().strip()
    for canonical, aliases in TOPIC_MAP.items():
        for alias in aliases:
            if raw_lower == alias.lower():
                return canonical
    return raw_topic


def calculate_company_probability(
    user_skills: dict,
    company_id: str,
) -> dict:
    """Calculate probability of user clearing a company's placement process."""
    category = COMPANY_CATEGORIES.get(company_id, "mass_recruiter")
    weights = COMPANY_TOPIC_WEIGHTS.get(category, COMPANY_TOPIC_WEIGHTS["mass_recruiter"])
    company = INDIAN_COMPANIES.get(company_id, {})

    # Get the company's focus areas for bonus
    focus_areas = [f.lower() for f in company.get("focus_areas", [])]

    total_weight = 0
    weighted_score = 0
    topic_breakdown = []

    for topic, weight in weights.items():
        skill = user_skills.get(topic, {"score": 0, "solved": 0})
        score = skill["score"]
        total_weight += weight

        # Bonus if topic matches company focus areas
        focus_bonus = 1.15 if any(topic.lower() in fa for fa in focus_areas) else 1.0

        weighted_score += score * weight * focus_bonus

        topic_breakdown.append({
            "topic": topic,
            "your_score": round(score, 1),
            "required_weight": round(weight * 100),
            "focus_match": focus_bonus > 1.0,
            "gap": max(0, round((70 - score) * weight, 1)),  # 70% is target
        })

    probability = round(min(weighted_score / max(total_weight, 1) * 100, 99), 1)
    probability = max(probability, 5)  # minimum 5% (luck exists)

    # Sort gaps by impact (highest first)
    topic_breakdown.sort(key=lambda x: x["gap"], reverse=True)

    # Top 3 gaps
    gaps = [t for t in topic_breakdown if t["gap"] > 0][:5]

    return {
        "company_id": company_id,
        "company_name": company.get("name", company_id),
        "probability": probability,
        "category": category,
        "package": company.get("package", "N/A"),
        "icon": company.get("icon", "🏢"),
        "color": company.get("color", "#666"),
        "exam_pattern": company.get("exam_pattern", "N/A"),
        "gaps": gaps,
        "topic_breakdown": topic_breakdown[:10],  # top 10 topics
    }


@router.get("/skill-profile")
async def get_skill_profile(user=Depends(get_current_user)):
    """Build the user's DSA/skill fingerprint from all solved problems and test history."""
    solved_col = solved_problems_collection()
    submissions_col = submissions_collection()
    questions_col = curated_questions_collection()
    aptitude_col = aptitude_collection()
    gamification_col = gamification_collection()

    # Aggregate solved problems by topic and difficulty
    topic_stats = defaultdict(lambda: {"solved": 0, "easy": 0, "medium": 0, "hard": 0, "total_submissions": 0})

    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": {"topic": "$question.topic", "difficulty": "$question.difficulty"},
            "count": {"$sum": 1}
        }}
    ]

    async for doc in solved_col.aggregate(pipeline):
        topic = normalize_topic(doc["_id"].get("topic", "Other"))
        diff = doc["_id"].get("difficulty", "medium")
        count = doc["count"]
        topic_stats[topic]["solved"] += count
        topic_stats[topic][diff] = topic_stats[topic].get(diff, 0) + count

    # Also get from submissions (includes failed attempts)
    submission_pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": "$question.topic",
            "total": {"$sum": 1},
            "passed": {"$sum": {"$cond": [{"$eq": ["$status", "passed"]}, 1, 0]}}
        }}
    ]

    async for doc in submissions_col.aggregate(submission_pipeline):
        topic = normalize_topic(doc.get("_id", "Other"))
        topic_stats[topic]["total_submissions"] = doc.get("total", 0)

    # Get aptitude test scores
    aptitude_pipeline = [
        {"$match": {"user_id": user["id"], "status": "completed"}},
        {"$group": {
            "_id": "$category",
            "avg_score": {"$avg": "$percentage"},
            "count": {"$sum": 1},
            "max_score": {"$max": "$percentage"}
        }}
    ]

    aptitude_scores = {}
    async for doc in aptitude_col.aggregate(aptitude_pipeline):
        cat = doc.get("_id", "general")
        aptitude_scores[cat] = {
            "avg_score": round(doc.get("avg_score", 0), 1),
            "tests_taken": doc.get("count", 0),
            "best_score": round(doc.get("max_score", 0), 1),
        }

    # Get gamification data
    gamification = await gamification_col.find_one({"user_id": user["id"]})
    total_xp = gamification.get("xp", 0) if gamification else 0
    streak = gamification.get("streak", 0) if gamification else 0

    # Calculate score per topic (0-100)
    # Score = solved problems weighted by difficulty, normalized
    MAX_EXPECTED = {"easy": 50, "medium": 30, "hard": 15}  # expected solves for "good"
    user_skills = {}

    for topic, stats in topic_stats.items():
        easy_score = min(stats.get("easy", 0) / MAX_EXPECTED["easy"], 1.0) * 30
        medium_score = min(stats.get("medium", 0) / MAX_EXPECTED["medium"], 1.0) * 40
        hard_score = min(stats.get("hard", 0) / MAX_EXPECTED["hard"], 1.0) * 30
        total_score = min(easy_score + medium_score + hard_score, 100)

        user_skills[topic] = {
            "score": round(total_score, 1),
            "solved": stats["solved"],
            "easy": stats.get("easy", 0),
            "medium": stats.get("medium", 0),
            "hard": stats.get("hard", 0),
        }

    # Ensure core topics exist even with 0 score
    core_topics = ["Arrays", "Strings", "Linked Lists", "Trees", "DP", "Graphs",
                    "Hashing", "Stacks", "Greedy", "Sorting", "Searching", "Recursion"]
    for topic in core_topics:
        if topic not in user_skills:
            user_skills[topic] = {"score": 0, "solved": 0, "easy": 0, "medium": 0, "hard": 0}

    # Add aptitude scores as skill topics
    for cat, scores in aptitude_scores.items():
        topic_name = cat.title() if cat else "Aptitude"
        user_skills[topic_name] = {
            "score": scores["avg_score"],
            "solved": scores["tests_taken"],
            "easy": 0, "medium": 0, "hard": 0,
        }

    # Calculate overall score
    all_scores = [v["score"] for v in user_skills.values() if v["score"] > 0]
    overall_score = round(sum(all_scores) / max(len(all_scores), 1), 1)

    # Find strongest and weakest topics
    sorted_topics = sorted(user_skills.items(), key=lambda x: x[1]["score"], reverse=True)
    strongest = [{"topic": t, **s} for t, s in sorted_topics[:5] if s["score"] > 0]
    weakest = [{"topic": t, **s} for t, s in sorted_topics[-5:] if s["score"] < 50]

    return {
        "user_id": user["id"],
        "overall_score": overall_score,
        "total_solved": sum(s["solved"] for s in user_skills.values()),
        "skills": user_skills,
        "strongest": strongest,
        "weakest": weakest,
        "aptitude_scores": aptitude_scores,
        "gamification": {
            "xp": total_xp,
            "streak": streak,
        },
    }


@router.get("/company-predictions")
async def get_company_predictions(user=Depends(get_current_user)):
    """Get clearance probability for all 53 companies based on user's skill profile."""
    # Get skill profile (reuse logic)
    solved_col = solved_problems_collection()
    questions_col = curated_questions_collection()
    aptitude_col = aptitude_collection()

    topic_stats = defaultdict(lambda: {"solved": 0, "easy": 0, "medium": 0, "hard": 0})

    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": {"topic": "$question.topic", "difficulty": "$question.difficulty"},
            "count": {"$sum": 1}
        }}
    ]

    async for doc in solved_col.aggregate(pipeline):
        topic = normalize_topic(doc["_id"].get("topic", "Other"))
        diff = doc["_id"].get("difficulty", "medium")
        topic_stats[topic]["solved"] += doc["count"]
        topic_stats[topic][diff] = topic_stats[topic].get(diff, 0) + doc["count"]

    # Calculate scores
    MAX_EXPECTED = {"easy": 50, "medium": 30, "hard": 15}
    user_skills = {}
    for topic, stats in topic_stats.items():
        easy_score = min(stats.get("easy", 0) / MAX_EXPECTED["easy"], 1.0) * 30
        medium_score = min(stats.get("medium", 0) / MAX_EXPECTED["medium"], 1.0) * 40
        hard_score = min(stats.get("hard", 0) / MAX_EXPECTED["hard"], 1.0) * 30
        user_skills[topic] = {"score": min(easy_score + medium_score + hard_score, 100), "solved": stats["solved"]}

    # Add aptitude
    aptitude_pipeline = [
        {"$match": {"user_id": user["id"], "status": "completed"}},
        {"$group": {"_id": "$category", "avg_score": {"$avg": "$percentage"}}}
    ]
    async for doc in aptitude_col.aggregate(aptitude_pipeline):
        user_skills[doc.get("_id", "Aptitude").title()] = {"score": doc.get("avg_score", 0), "solved": 1}

    # Calculate for all companies
    predictions = []
    for company_id in INDIAN_COMPANIES:
        pred = calculate_company_probability(user_skills, company_id)
        predictions.append(pred)

    # Sort by probability (highest first)
    predictions.sort(key=lambda x: x["probability"], reverse=True)

    # Categorize
    easy = [p for p in predictions if p["probability"] >= 70]
    medium = [p for p in predictions if 40 <= p["probability"] < 70]
    hard = [p for p in predictions if p["probability"] < 40]

    return {
        "overall_score": round(sum(p["probability"] for p in predictions) / max(len(predictions), 1), 1),
        "total_companies": len(predictions),
        "predictions": predictions,
        "summary": {
            "easy_clear": {"count": len(easy), "companies": [p["company_name"] for p in easy[:5]]},
            "moderate": {"count": len(medium), "companies": [p["company_name"] for p in medium[:5]]},
            "needs_work": {"count": len(hard), "companies": [p["company_name"] for p in hard[:5]]},
        },
    }


@router.get("/company/{company_id}")
async def get_company_detail_prediction(company_id: str, user=Depends(get_current_user)):
    """Get detailed prediction for a specific company with gap analysis."""
    solved_col = solved_problems_collection()
    aptitude_col = aptitude_collection()

    topic_stats = defaultdict(lambda: {"solved": 0, "easy": 0, "medium": 0, "hard": 0})

    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": {"topic": "$question.topic", "difficulty": "$question.difficulty"},
            "count": {"$sum": 1}
        }}
    ]

    async for doc in solved_col.aggregate(pipeline):
        topic = normalize_topic(doc["_id"].get("topic", "Other"))
        diff = doc["_id"].get("difficulty", "medium")
        topic_stats[topic]["solved"] += doc["count"]
        topic_stats[topic][diff] = topic_stats[topic].get(diff, 0) + doc["count"]

    MAX_EXPECTED = {"easy": 50, "medium": 30, "hard": 15}
    user_skills = {}
    for topic, stats in topic_stats.items():
        easy_score = min(stats.get("easy", 0) / MAX_EXPECTED["easy"], 1.0) * 30
        medium_score = min(stats.get("medium", 0) / MAX_EXPECTED["medium"], 1.0) * 40
        hard_score = min(stats.get("hard", 0) / MAX_EXPECTED["hard"], 1.0) * 30
        user_skills[topic] = {"score": min(easy_score + medium_score + hard_score, 100), "solved": stats["solved"]}

    aptitude_pipeline = [
        {"$match": {"user_id": user["id"], "status": "completed"}},
        {"$group": {"_id": "$category", "avg_score": {"$avg": "$percentage"}}}
    ]
    async for doc in aptitude_col.aggregate(aptitude_pipeline):
        user_skills[doc.get("_id", "Aptitude").title()] = {"score": doc.get("avg_score", 0), "solved": 1}

    pred = calculate_company_probability(user_skills, company_id)

    # Generate recommended problems for gaps
    recommendations = []
    for gap in pred.get("gaps", [])[:3]:
        topic = gap["topic"]
        # Find unsolved problems in this topic
        recs = []
        async for q in questions_col.find({"topic": topic}).limit(3):
            recs.append({
                "question": q.get("question_title", "Practice this topic"),
                "difficulty": q.get("difficulty", "medium"),
                "company": q.get("company", ""),
            })
        recommendations.append({
            "topic": topic,
            "gap_severity": "high" if gap["gap"] > 20 else "medium" if gap["gap"] > 10 else "low",
            "problems": recs,
        })

    return {
        **pred,
        "recommendations": recommendations,
    }
