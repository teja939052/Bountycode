"""
System Design Section — AI evaluation, model answers, and practice.
Covers architecture, scalability, distributed systems, and design patterns.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    system_design_tests_collection, system_design_leaderboard_collection,
    users_collection
)
from app.services.ai import chat_completion, parse_json
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/system-design-tests", tags=["system-design-tests"])

# System design categories
SD_CATEGORIES = {
    "hld": {
        "name": "High-Level Design (HLD)",
        "icon": "🏗️",
        "description": "System architecture, scalability, distributed systems",
        "subcategories": {
            "Social Media": "Twitter, Instagram, WhatsApp, News Feed",
            "E-commerce": "Amazon, Food Delivery, Ride-sharing",
            "Streaming": "YouTube, Netflix, Live Streaming",
            "Infrastructure": "URL Shortener, Rate Limiter, Cache, CDN",
            "Data": "Search Engine, Analytics, Data Pipelines",
            "Finance": "Payment Systems, Banking",
            "Misc": "Parking Lot, Chess, Ticket Booking, Leaderboard",
        },
    },
    "lld": {
        "name": "Low-Level Design (LLD)",
        "icon": "🔧",
        "description": "Class design, design patterns, OOP, API design",
        "subcategories": {
            "Data Structures": "Linked List, Stack, Queue, Trie, BST, Heap, Graph",
            "Design Patterns": "Singleton, Factory, Observer, Strategy, Decorator, Command",
            "OOP Design": "Vending Machine, Elevator, Library, Hotel, Snake & Ladder",
            "API Design": "REST APIs for Blog, Social Network",
            "Database Design": "E-commerce schema, Social Network schema",
            "Algorithm Design": "Randomized Set, Parking System, Snapshot Array",
            "Concurrency": "Thread Pool, Producer-Consumer, Read-Write Lock",
        },
    },
}

# Evaluation rubric
EVALUATION_RUBRIC = {
    "requirements_gathering": {
        "name": "Requirements Gathering",
        "weight": 15,
        "criteria": {
            5: "Identifies functional and non-functional requirements clearly",
            4: "Identifies most requirements with minor gaps",
            3: "Identifies basic requirements",
            2: "Missing key requirements",
            1: "No clear requirements",
        }
    },
    "high_level_design": {
        "name": "High-Level Design",
        "weight": 25,
        "criteria": {
            5: "Clear architecture with all major components identified",
            4: "Good architecture with minor gaps",
            3: "Basic architecture identified",
            2: "Incomplete architecture",
            1: "No clear architecture",
        }
    },
    "deep_dive": {
        "name": "Deep Dive",
        "weight": 25,
        "criteria": {
            5: "Excellent understanding of internals, databases, APIs",
            4: "Good understanding with minor gaps",
            3: "Basic understanding of key components",
            2: "Missing critical details",
            1: "No deep dive",
        }
    },
    "scalability": {
        "name": "Scalability & Trade-offs",
        "weight": 20,
        "criteria": {
            5: "Excellent scalability discussion with clear trade-offs",
            4: "Good scalability with some trade-offs",
            3: "Basic scalability mentioned",
            2: "No scalability discussion",
            1: "No awareness of scale",
        }
    },
    "communication": {
        "name": "Communication",
        "weight": 15,
        "criteria": {
            5: "Clear, structured, well-organized presentation",
            4: "Good communication with minor issues",
            3: "Adequate communication",
            2: "Unclear or disorganized",
            1: "Poor communication",
        }
    },
}


@router.get("/categories")
async def get_categories():
    """Get all system design categories."""
    return {"categories": SD_CATEGORIES}


@router.get("/problems")
async def list_problems(
    category: Optional[str] = None,
    type: Optional[str] = None,  # hld or lld
    subcategory: Optional[str] = None,
    difficulty: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    user=Depends(get_current_user),
):
    """List system design problems with filtering."""
    # Load problems from all modules
    from scripts.system_design_problems import SYSTEM_DESIGN_PROBLEMS
    from scripts.hld_problems import HLD_PROBLEMS
    from scripts.hld_problems_batch2 import HLD_BATCH2
    from scripts.hld_extra import HLD_EXTRA
    from scripts.hld_final import HLD_FINAL
    from scripts.lld_problems import LLD_PROBLEMS
    from scripts.lld_problems_batch2 import LLD_BATCH2
    from scripts.lld_final import LLD_FINAL
    from scripts.lld_extra import LLD_EXTRA
    from scripts.lld_final2 import LLD_FINAL2
    from scripts.lld_final3 import LLD_FINAL3
    from scripts.lld_ultra import LLD_ULTRA

    problems = SYSTEM_DESIGN_PROBLEMS.copy() + HLD_PROBLEMS.copy() + HLD_BATCH2.copy() + HLD_EXTRA.copy() + HLD_FINAL.copy() + LLD_PROBLEMS.copy() + LLD_BATCH2.copy() + LLD_FINAL.copy() + LLD_EXTRA.copy() + LLD_FINAL2.copy() + LLD_FINAL3.copy() + LLD_ULTRA.copy()

    if type:
        problems = [p for p in problems if p.get("category") == type]
    if subcategory:
        problems = [p for p in problems if p.get("subcategory") == subcategory]
    if difficulty:
        problems = [p for p in problems if p.get("difficulty") == difficulty]

    total = len(problems)
    start = (page - 1) * limit
    problems = problems[start:start + limit]

    return {
        "problems": problems,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/problem/{problem_id}")
async def get_problem(problem_id: str, user=Depends(get_current_user)):
    """Get a specific system design problem with full details."""
    from scripts.system_design_problems import SYSTEM_DESIGN_PROBLEMS

    problem = next((p for p in SYSTEM_DESIGN_PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    return problem


@router.post("/evaluate/{problem_id}")
async def evaluate_system_design(
    problem_id: str,
    answer: str,
    user=Depends(get_current_user),
):
    """AI-evaluate a system design answer with detailed rubric scoring."""
    from scripts.system_design_problems import SYSTEM_DESIGN_PROBLEMS

    problem = next((p for p in SYSTEM_DESIGN_PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    prompt = f"""You are a senior system design interviewer at a FAANG company. Evaluate this system design answer.

Problem: {problem['title']}
Description: {problem.get('statement', '')}
Key Components Expected: {', '.join(problem.get('key_components', []))}
Estimated Scale: {problem.get('estimated_users', 'N/A')}

Student's Answer:
{answer}

Evaluate the answer using this rubric and respond in EXACT JSON format:
{{
  "overall_score": <1-10>,
  "breakdown": {{
    "requirements_gathering": {{
      "score": <1-5>,
      "feedback": "<specific feedback>"
    }},
    "high_level_design": {{
      "score": <1-5>,
      "feedback": "<specific feedback>"
    }},
    "deep_dive": {{
      "score": <1-5>,
      "feedback": "<specific feedback>"
    }},
    "scalability": {{
      "score": <1-5>,
      "feedback": "<specific feedback>"
    }},
    "communication": {{
      "score": <1-5>,
      "feedback": "<specific feedback>"
    }}
  }},
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"],
  "missing_concepts": ["concept1", "concept2"],
  "model_answer_summary": "Brief summary of what an ideal answer would include",
  "recommended_reading": ["topic1", "topic2"]
}}

Be specific, constructive, and thorough. Compare against industry standards."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=False,
            max_tokens=2000,
        )
        evaluation = parse_json(result)
    except Exception:
        evaluation = {
            "overall_score": 5,
            "breakdown": {
                "requirements_gathering": {"score": 3, "feedback": "Basic requirements identified"},
                "high_level_design": {"score": 3, "feedback": "Basic architecture shown"},
                "deep_dive": {"score": 3, "feedback": "Some details provided"},
                "scalability": {"score": 3, "feedback": "Basic scalability mentioned"},
                "communication": {"score": 3, "feedback": "Adequate presentation"},
            },
            "strengths": ["Attempted to address the problem"],
            "improvements": ["Add more details to the architecture", "Discuss scalability trade-offs"],
            "missing_concepts": ["Database sharding", "Caching strategies"],
            "model_answer_summary": "A good answer would cover requirements, high-level architecture, database design, API design, and scalability.",
            "recommended_reading": ["System Design Interview by Alex Xu"],
        }

    # Save evaluation
    test_doc = {
        "user_id": user["id"],
        "problem_id": problem_id,
        "problem_title": problem["title"],
        "answer": answer,
        "evaluation": evaluation,
        "overall_score": evaluation.get("overall_score", 5),
        "created_at": datetime.now(timezone.utc),
    }
    await system_design_tests_collection().insert_one(test_doc)

    # Record gamification
    score = evaluation.get("overall_score", 5)
    xp = score * 10
    await record_practice(user["id"], "system_design", score)

    return {
        "evaluation": evaluation,
        "xp_gained": xp,
    }


@router.get("/model-answer/{problem_id}")
async def get_model_answer(problem_id: str, user=Depends(get_current_user)):
    """Get AI-generated model answer for a system design problem."""
    from scripts.system_design_problems import SYSTEM_DESIGN_PROBLEMS

    problem = next((p for p in SYSTEM_DESIGN_PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    prompt = f"""You are a senior system designer. Provide a comprehensive model answer for this problem.

Problem: {problem['title']}
Description: {problem.get('statement', '')}
Requirements: {', '.join(problem.get('requirements', []))}
Key Components: {', '.join(problem.get('key_components', []))}
Estimated Scale: {problem.get('estimated_users', 'N/A')}

Provide a detailed model answer in this EXACT JSON format:
{{
  "title": "{problem['title']}",
  "introduction": "2-3 sentence overview of the problem and approach",
  "requirements": {{
    "functional": ["functional req 1", "functional req 2"],
    "non_functional": ["non-functional req 1", "non-functional req 2"]
  }},
  "high_level_design": {{
    "components": [
      {{"name": "Component 1", "description": "What it does", "technology": "Tech stack"}},
      {{"name": "Component 2", "description": "What it does", "technology": "Tech stack"}}
    ],
    "data_flow": "How data flows between components",
    "api_design": ["API endpoint 1", "API endpoint 2"]
  }},
  "database_design": {{
    "tables": [
      {{"name": "Table 1", "columns": ["col1", "col2"], "key": "primary key"}}
    ],
    "indexes": ["index 1", "index 2"]
  }},
  "scalability": {{
    "horizontal_scaling": "How to scale horizontally",
    "caching": "Caching strategy",
    "cdn": "CDN usage if applicable"
  }},
  "trade_offs": [
    {{"decision": "Decision 1", "pros": "Pros", "cons": "Cons"}},
    {{"decision": "Decision 2", "pros": "Pros", "cons": "Cons"}}
  ],
  "estimated_complexity": {{
    "time": "O(1) lookup",
    "space": "O(n) storage"
  }}
}}

Be thorough and provide industry-standard solutions."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=2000,
        )
        model_answer = parse_json(result)
    except Exception:
        model_answer = {
            "title": problem["title"],
            "introduction": f"Design a system for {problem['title']}.",
            "requirements": {"functional": problem.get("requirements", []), "non_functional": ["High availability", "Low latency"]},
            "high_level_design": {"components": [{"name": c, "description": f"Handles {c.lower()} functionality", "technology": "Microservice"} for c in problem.get("key_components", [])], "data_flow": "Request → Load Balancer → Service → Database", "api_design": ["GET /api/resource", "POST /api/resource"]},
            "database_design": {"tables": [{"name": "main_table", "columns": ["id", "data"], "key": "id"}], "indexes": ["Primary key index"]},
            "scalability": {"horizontal_scaling": "Add more service instances", "caching": "Redis for hot data", "cdn": "CloudFront for static assets"},
            "trade_offs": [{"decision": "SQL vs NoSQL", "pros": "ACID compliance", "cons": "Less flexible"}],
        }

    return model_answer


@router.get("/rubric")
async def get_evaluation_rubric():
    """Get the evaluation rubric for system design."""
    return {"rubric": EVALUATION_RUBRIC}


@router.get("/history")
async def get_history(
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    """Get user's system design practice history."""
    collection = system_design_tests_collection()
    cursor = collection.find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(limit)

    history = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        history.append(doc)

    return {"history": history, "total": len(history)}


@router.get("/stats")
async def get_stats(user=Depends(get_current_user)):
    """Get system design practice statistics."""
    collection = system_design_tests_collection()

    total = await collection.count_documents({"user_id": user["id"]})
    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$group": {
            "_id": None,
            "avg_score": {"$avg": "$overall_score"},
            "total_evaluations": {"$sum": 1},
            "best_score": {"$max": "$overall_score"},
        }}
    ]

    stats = {"avg_score": 0, "total_evaluations": 0, "best_score": 0}
    async for doc in collection.aggregate(pipeline):
        stats = {
            "avg_score": round(doc.get("avg_score", 0), 1),
            "total_evaluations": doc.get("total_evaluations", 0),
            "best_score": doc.get("best_score", 0),
        }

    # Score breakdown
    breakdown_pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$group": {
            "_id": None,
            "avg_requirements": {"$avg": "$evaluation.breakdown.requirements_gathering.score"},
            "avg_design": {"$avg": "$evaluation.breakdown.high_level_design.score"},
            "avg_deep_dive": {"$avg": "$evaluation.breakdown.deep_dive.score"},
            "avg_scalability": {"$avg": "$evaluation.breakdown.scalability.score"},
            "avg_communication": {"$avg": "$evaluation.breakdown.communication.score"},
        }}
    ]

    breakdown = {}
    async for doc in collection.aggregate(breakdown_pipeline):
        breakdown = {
            "requirements_gathering": round(doc.get("avg_requirements", 0), 1),
            "high_level_design": round(doc.get("avg_design", 0), 1),
            "deep_dive": round(doc.get("avg_deep_dive", 0), 1),
            "scalability": round(doc.get("avg_scalability", 0), 1),
            "communication": round(doc.get("avg_communication", 0), 1),
        }

    return {**stats, "total_practiced": total, "breakdown": breakdown}


@router.get("/leaderboard")
async def get_leaderboard(limit: int = Query(20, ge=1, le=100)):
    """Get system design leaderboard."""
    collection = system_design_tests_collection()

    pipeline = [
        {"$group": {
            "_id": "$user_id",
            "avg_score": {"$avg": "$overall_score"},
            "total_evaluations": {"$sum": 1},
            "best_score": {"$max": "$overall_score"},
        }},
        {"$sort": {"avg_score": -1, "total_evaluations": -1}},
        {"$limit": limit},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {
            "user_name": "$user.name",
            "avg_score": {"$round": ["$avg_score", 1]},
            "total_evaluations": 1,
            "best_score": 1,
        }}
    ]

    leaderboard = []
    rank = 1
    async for doc in collection.aggregate(pipeline):
        doc["rank"] = rank
        leaderboard.append(doc)
        rank += 1

    return {"leaderboard": leaderboard}
