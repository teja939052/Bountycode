"""
Problem navigation routes — topic-wise listing, progress tracking, streaks.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, solved_problems_collection,
    question_answers_collection, users_collection
)

router = APIRouter(prefix="/api/problems", tags=["problems"])

# Pattern definitions for DSA problems
PATTERNS = {
    "Two Pointers": {
        "name": "Two Pointers",
        "description": "Use two pointers moving towards each other or in same direction",
        "icon": "👆👆",
        "topics": ["Arrays", "Strings", "Linked Lists"],
        "keywords": ["two pointer", "opposite ends", "same direction", "partition"],
        "problems_count": 0,
    },
    "Sliding Window": {
        "name": "Sliding Window",
        "description": "Maintain a window of elements and slide it across the array",
        "icon": "🪟",
        "topics": ["Arrays", "Strings", "Sliding Window"],
        "keywords": ["window", "substring", "subarray", "contiguous"],
        "problems_count": 0,
    },
    "Fast & Slow Pointers": {
        "name": "Fast & Slow Pointers",
        "description": "Use two pointers moving at different speeds (tortoise and hare)",
        "icon": "🐢🐇",
        "topics": ["Linked Lists", "Arrays"],
        "keywords": ["cycle", "middle", "detect", "tortoise", "hare"],
        "problems_count": 0,
    },
    "Merge Intervals": {
        "name": "Merge Intervals",
        "description": "Sort intervals and merge overlapping ones",
        "icon": "🔗",
        "topics": ["Arrays", "Sorting"],
        "keywords": ["interval", "merge", "overlap", "sort"],
        "problems_count": 0,
    },
    "Cyclic Sort": {
        "name": "Cyclic Sort",
        "description": "Place elements at their correct index in a cyclic manner",
        "icon": "🔄",
        "topics": ["Arrays"],
        "keywords": ["cyclic", "correct index", "swap", "missing", "duplicate"],
        "problems_count": 0,
    },
    "In-place Reversal": {
        "name": "In-place Reversal",
        "description": "Reverse linked list or subarray in-place",
        "icon": "🔃",
        "topics": ["Linked Lists"],
        "keywords": ["reverse", "in-place", "link", "pointer"],
        "problems_count": 0,
    },
    "Tree BFS": {
        "name": "Tree BFS (Level Order)",
        "description": "Process tree nodes level by level using a queue",
        "icon": "🌲",
        "topics": ["Binary Trees", "BST"],
        "keywords": ["level order", "bfs", "queue", "level"],
        "problems_count": 0,
    },
    "Tree DFS": {
        "name": "Tree DFS",
        "description": "Explore tree deeply using recursion or stack",
        "icon": "🔍",
        "topics": ["Binary Trees", "BST"],
        "keywords": ["inorder", "preorder", "postorder", "dfs", "recursive"],
        "problems_count": 0,
    },
    "Graph BFS": {
        "name": "Graph BFS",
        "description": "Traverse graph level by level",
        "icon": "🕸️",
        "topics": ["Graphs"],
        "keywords": ["bfs", "level", "shortest path", "unweighted"],
        "problems_count": 0,
    },
    "Graph DFS": {
        "name": "Graph DFS",
        "description": "Traverse graph deeply using recursion or stack",
        "icon": "🕸️",
        "topics": ["Graphs"],
        "keywords": ["dfs", "recursive", "cycle", "connected", "topological"],
        "problems_count": 0,
    },
    "Dynamic Programming": {
        "name": "Dynamic Programming",
        "description": "Optimal substructure with overlapping subproblems",
        "icon": "🧩",
        "topics": ["Dynamic Programming"],
        "keywords": ["dp", "memoization", "tabulation", "optimal", "subproblem"],
        "problems_count": 0,
    },
    "Backtracking": {
        "name": "Backtracking",
        "description": "Explore all possibilities and backtrack when needed",
        "icon": "🔙",
        "topics": ["Recursion", "Arrays"],
        "keywords": ["backtrack", "permutation", "combination", "subset"],
        "problems_count": 0,
    },
    "Binary Search": {
        "name": "Binary Search",
        "description": "Search in sorted array by eliminating half each time",
        "icon": "🎯",
        "topics": ["Binary Search", "Arrays"],
        "keywords": ["binary search", "sorted", "mid", "log n"],
        "problems_count": 0,
    },
    "Monotonic Stack": {
        "name": "Monotonic Stack",
        "description": "Stack that maintains elements in sorted order",
        "icon": "📚",
        "topics": ["Stacks & Queues", "Arrays"],
        "keywords": ["next greater", "previous smaller", "monotonic", "stack"],
        "problems_count": 0,
    },
    "Heap / Priority Queue": {
        "name": "Heap / Priority Queue",
        "description": "Use heap to efficiently get min/max element",
        "icon": "⛰️",
        "topics": ["Heaps"],
        "keywords": ["heap", "priority", "top k", "merge k", "min", "max"],
        "problems_count": 0,
    },
    "Greedy": {
        "name": "Greedy",
        "description": "Make locally optimal choice at each step",
        "icon": "💰",
        "topics": ["Greedy"],
        "keywords": ["greedy", "sort", "interval", "activity", "fractional"],
        "problems_count": 0,
    },
}


@router.get("/patterns")
async def get_patterns(user=Depends(get_current_user)):
    """Get all problem patterns with counts and user progress."""
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()

    # Get all problems with their topics
    problems = []
    async for doc in collection.find({}, {"topic": 1, "topics": 1, "question_title": 1}):
        problems.append(doc)

    # Count problems per pattern
    for pattern_key, pattern in PATTERNS.items():
        count = 0
        for p in problems:
            if p.get("topic") in pattern["topics"]:
                count += 1
            elif any(t in pattern["topics"] for t in p.get("topics", [])):
                count += 1
        pattern["problems_count"] = count

    # Get user's solved problems per pattern
    solved_count = {}
    async for doc in solved_col.find({"user_id": user["id"]}, {"question_id": 1}):
        solved_count[doc["question_id"]] = True

    # Calculate pattern progress
    patterns_with_progress = []
    for pattern_key, pattern in PATTERNS.items():
        solved_in_pattern = 0
        for p in problems:
            if p.get("topic") in pattern["topics"]:
                if str(p.get("_id", "")) in solved_count:
                    solved_in_pattern += 1
            elif any(t in pattern["topics"] for t in p.get("topics", [])):
                if str(p.get("_id", "")) in solved_count:
                    solved_in_pattern += 1

        patterns_with_progress.append({
            "id": pattern_key,
            "name": pattern["name"],
            "description": pattern["description"],
            "icon": pattern["icon"],
            "problems_count": pattern["problems_count"],
            "solved_count": solved_in_pattern,
            "progress": round(solved_in_pattern / max(pattern["problems_count"], 1) * 100, 1),
        })

    return {"patterns": patterns_with_progress}


@router.get("/pattern/{pattern_name}")
async def get_pattern_problems(
    pattern_name: str,
    sort: Optional[str] = "order",
    difficulty: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get all problems matching a specific pattern."""
    pattern = PATTERNS.get(pattern_name)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    collection = curated_questions_collection()

    # Build query to match pattern's topics
    query = {"$or": [{"topic": {"$in": pattern["topics"]}}]}

    if difficulty:
        query["difficulty"] = difficulty

    # Build sort
    if sort == "difficulty":
        sort_stage = [("difficulty", 1), ("problem_order", 1)]
    elif sort == "acceptance":
        sort_stage = [("acceptance_rate", -1)]
    else:
        sort_stage = [("topic_order", 1), ("problem_order", 1)]

    cursor = collection.find(
        query,
        {"statement": 0, "visible_test_cases": 0, "hidden_test_cases": 0, "solution": 0}
    ).sort(sort_stage)

    problems = []
    question_ids = []
    async for q in cursor:
        q["id"] = str(q.pop("_id"))
        problems.append(q)
        question_ids.append(q["id"])

    # Get solved status
    solved_map = {}
    if question_ids:
        solved_cursor = solved_col.find(
            {"user_id": user["id"], "question_id": {"$in": question_ids}},
            {"question_id": 1, "_id": 0}
        )
        async for doc in solved_cursor:
            solved_map[doc["question_id"]] = True

    for p in problems:
        p["solved"] = solved_map.get(p["id"], False)

    return {
        "pattern": pattern,
        "problems": problems,
        "total": len(problems),
        "solved_count": sum(1 for p in problems if p["solved"]),
    }


@router.get("/topics")
async def get_topics():
    """List all topics with problem counts and difficulty breakdown."""
    collection = curated_questions_collection()
    pipeline = [
        {"$group": {
            "_id": {"topic": "$topic", "topic_order": "$topic_order", "difficulty": "$difficulty"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.topic_order": 1}}
    ]
    topic_data = {}
    async for doc in collection.aggregate(pipeline):
        topic = doc["_id"]["topic"]
        diff = doc["_id"]["difficulty"]
        order = doc["_id"]["topic_order"]
        if topic not in topic_data:
            topic_data[topic] = {"topic": topic, "topic_order": order, "total": 0, "easy": 0, "medium": 0, "hard": 0}
        topic_data[topic]["total"] += doc["count"]
        topic_data[topic][diff] = doc["count"]

    topics = sorted(topic_data.values(), key=lambda x: x["topic_order"])
    return {"topics": topics}


@router.get("/topics/{topic}")
async def get_topic_problems(
    topic: str,
    sort: Optional[str] = "order",  # order, difficulty, companies, acceptance
    difficulty: Optional[str] = None,
    company: Optional[str] = None,
    search: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get all problems in a topic with sorting and filtering options."""
    collection = curated_questions_collection()

    # Build query
    query = {"topic": topic}
    if difficulty:
        query["difficulty"] = difficulty
    if company:
        query["$or"] = [{"company": company}, {"company": company.title()}, {"company": company.upper()}]
    if search:
        query["$text"] = {"$search": search}

    # Build sort
    if sort == "difficulty":
        sort_stage = [("difficulty", 1), ("problem_order", 1)]
    elif sort == "companies":
        sort_stage = [("company_frequency", -1), ("problem_order", 1)]
    elif sort == "acceptance":
        sort_stage = [("acceptance_rate", -1), ("total_submissions", -1)]
    elif sort == "newest":
        sort_stage = [("created_at", -1)]
    else:  # Default: sequential order
        sort_stage = [("topic_order", 1), ("problem_order", 1)]

    cursor = collection.find(
        query,
        {"statement": 0, "visible_test_cases": 0, "hidden_test_cases": 0, "solution": 0}
    ).sort(sort_stage)

    problems = []
    question_ids = []
    async for q in cursor:
        q["id"] = str(q.pop("_id"))
        problems.append(q)
        question_ids.append(q["id"])

    # Batch fetch solved statuses
    solved_map = {}
    if question_ids:
        solved_cursor = solved_problems_collection().find(
            {"user_id": user["id"], "question_id": {"$in": question_ids}},
            {"question_id": 1, "_id": 0}
        )
        async for doc in solved_cursor:
            solved_map[doc["question_id"]] = True

    for p in problems:
        p["solved"] = solved_map.get(p["id"], False)

    return {
        "topic": topic,
        "problems": problems,
        "total": len(problems),
        "solved_count": sum(1 for p in problems if p["solved"]),
    }


@router.get("/progress")
async def get_progress(user=Depends(get_current_user)):
    """Get user's progress across all topics."""
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()
    uid = user["id"]

    # Get total problems per topic
    topic_pipeline = [
        {"$group": {"_id": "$topic", "total": {"$sum": 1}, "topic_order": {"$first": "$topic_order"}}},
        {"$sort": {"topic_order": 1}}
    ]
    topic_totals = {}
    async for doc in collection.aggregate(topic_pipeline):
        topic_totals[doc["_id"]] = {"total": doc["total"], "topic_order": doc["topic_order"]}

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
        {"$group": {"_id": "$question.topic", "solved": {"$sum": 1}}}
    ]
    solved_counts = {}
    async for doc in solved_col.aggregate(solved_pipeline):
        solved_counts[doc["_id"]] = doc["solved"]

    # Build response
    topics = []
    total_all = 0
    solved_all = 0
    for topic_name, data in sorted(topic_totals.items(), key=lambda x: x[1]["topic_order"]):
        s = solved_counts.get(topic_name, 0)
        t = data["total"]
        total_all += t
        solved_all += s
        topics.append({
            "topic": topic_name,
            "total": t,
            "solved": s,
            "percentage": round(s / t * 100, 1) if t > 0 else 0,
        })

    return {
        "topics": topics,
        "total_problems": total_all,
        "total_solved": solved_all,
        "overall_percentage": round(solved_all / total_all * 100, 1) if total_all > 0 else 0,
    }


@router.get("/streak")
async def get_streak(user=Depends(get_current_user)):
    """Get user's daily practice streak."""
    solved_col = solved_problems_collection()
    uid = user["id"]

    # Get all solve dates (unique days)
    pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$solved_at"}}}}
    ]
    days = set()
    async for doc in solved_col.aggregate(pipeline):
        days.add(doc["_id"])

    if not days:
        return {"streak": 0, "longest_streak": 0, "active_days": 0}

    # Calculate current streak (from today backwards)
    today = datetime.now(timezone.utc).date()
    streak = 0
    check_date = today
    while check_date.isoformat() in days:
        streak += 1
        check_date -= timedelta(days=1)

    # Calculate longest streak
    sorted_days = sorted(days)
    longest = 1
    current = 1
    for i in range(1, len(sorted_days)):
        d1 = datetime.fromisoformat(sorted_days[i - 1]).date()
        d2 = datetime.fromisoformat(sorted_days[i]).date()
        if (d2 - d1).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return {
        "streak": streak,
        "longest_streak": longest,
        "active_days": len(days),
    }


@router.get("/stats")
async def get_stats(user=Depends(get_current_user)):
    """Get overall problem-solving statistics."""
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()
    answers_col = question_answers_collection()
    uid = user["id"]

    total_problems = await collection.count_documents({})
    total_solved = await solved_col.count_documents({"user_id": uid})
    total_attempted = await answers_col.count_documents({"user_id": uid})

    # Difficulty breakdown
    diff_pipeline = [
        {"$group": {"_id": "$difficulty", "count": {"$sum": 1}}}
    ]
    difficulty_stats = {}
    async for doc in collection.aggregate(diff_pipeline):
        difficulty_stats[doc["_id"]] = doc["count"]

    solved_diff_pipeline = [
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
    solved_diff = {}
    async for doc in solved_col.aggregate(solved_diff_pipeline):
        solved_diff[doc["_id"]] = doc["count"]

    return {
        "total_problems": total_problems,
        "total_solved": total_solved,
        "total_attempted": total_attempted,
        "difficulty_breakdown": {
            "easy": {"total": difficulty_stats.get("easy", 0), "solved": solved_diff.get("easy", 0)},
            "medium": {"total": difficulty_stats.get("medium", 0), "solved": solved_diff.get("medium", 0)},
            "hard": {"total": difficulty_stats.get("hard", 0), "solved": solved_diff.get("hard", 0)},
        },
    }


@router.get("/company/{company_name}")
async def get_company_problems(company_name: str, user=Depends(get_current_user)):
    """Get problems tagged with a specific company."""
    collection = curated_questions_collection()
    cursor = collection.find(
        {"$or": [{"company": company_name}, {"company": company_name.title()}, {"company": company_name.upper()}]},
        {"statement": 0, "visible_test_cases": 0, "hidden_test_cases": 0, "solution": 0}
    ).sort([("topic_order", 1), ("problem_order", 1)])

    problems = []
    question_ids = []
    async for q in cursor:
        q["id"] = str(q.pop("_id"))
        problems.append(q)
        question_ids.append(q["id"])

    # Batch fetch solved statuses
    solved_map = {}
    if question_ids:
        solved_cursor = solved_problems_collection().find(
            {"user_id": user["id"], "question_id": {"$in": question_ids}},
            {"question_id": 1, "_id": 0}
        )
        async for doc in solved_cursor:
            solved_map[doc["question_id"]] = True

    for p in problems:
        p["solved"] = solved_map.get(p["id"], False)

    # Stats
    diff_counts = {"easy": 0, "medium": 0, "hard": 0}
    for p in problems:
        d = p.get("difficulty", "medium")
        if d in diff_counts:
            diff_counts[d] += 1

    return {
        "company": company_name,
        "problems": problems,
        "total": len(problems),
        "solved_count": sum(1 for p in problems if p["solved"]),
        "difficulty_breakdown": diff_counts,
    }
