"""
Deep Curriculum — 50+ topics, 200+ exercises, real-world projects.
Uses plain dicts for curriculum data (no class overhead).
"""

from typing import List, Dict, Any, Optional

# ============================================================
# Exercise dicts
# ============================================================

js_ex_1_1 = {
    "id": "js-ex-1-1",
    "title": "Variable Declaration",
    "description": "Declare variables using var, let, and const",
    "challenge_type": "code",
    "difficulty": "beginner",
    "prompt": "Create three variables: a name (string), age (number), and isStudent (boolean). Log them to the console.",
    "estimated_time": 5,
}
js_ex_1_2 = {
    "id": "js-ex-1-2",
    "title": "Data Types",
    "description": "Identify and use different data types",
    "challenge_type": "mcq",
    "difficulty": "beginner",
    "prompt": "Which of the following is NOT a JavaScript data type? A) string B) boolean C) integer D) float",
    "estimated_time": 3,
}
js_ex_2_1 = {
    "id": "js-ex-2-1", "title": "Function Basics",
    "description": "Create a function that takes two numbers and returns their sum",
    "challenge_type": "code", "difficulty": "beginner",
    "prompt": "Write a function `add(a, b)` that returns `a + b`. Call it with `add(3, 5)` and log the result.",
    "estimated_time": 5,
}
js_ex_2_2 = {
    "id": "js-ex-2-2", "title": "Closures",
    "description": "Understand and create closures",
    "challenge_type": "code", "difficulty": "intermediate",
    "prompt": "Write a function `makeCounter()` that returns a function. Each call to the returned function increments and logs a counter.",
    "estimated_time": 8,
}
py_ex_1_1 = {
    "id": "py-ex-1-1", "title": "Hello World",
    "description": "Print 'Hello, World!' to the console",
    "challenge_type": "code", "difficulty": "beginner",
    "prompt": "Print exactly: Hello, World!", "estimated_time": 2,
}
py_ex_2_1 = {
    "id": "py-ex-2-1", "title": "FizzBuzz",
    "description": "Print numbers 1-100, replacing multiples of 3 with 'Fizz', 5 with 'Buzz', and both with 'FizzBuzz'",
    "challenge_type": "code", "difficulty": "beginner",
    "prompt": "Write a loop from 1 to 100. If n%3==0 print 'Fizz', if n%5==0 print 'Buzz', if both print 'FizzBuzz'.",
    "estimated_time": 5,
}
sd_ex_1_1 = {
    "id": "sd-ex-1-1", "title": "Scaling Decision",
    "description": "Given a traffic pattern, decide scaling strategy",
    "challenge_type": "theory", "difficulty": "advanced",
    "prompt": "Your database is getting 10K reads/sec and 1K writes/sec. Your primary is in US-East. Users are global. Design a scaling strategy including replication and partitioning.",
    "estimated_time": 15,
}


# ============================================================
# Topic dicts
# ============================================================

js_topic_1 = {
    "id": "js-basics-1", "title": "Variables & Data Types",
    "description": "Learn variables, let/const, primitives, and type coercion",
    "order_index": 1,
    "exercises": [js_ex_1_1, js_ex_1_2],
    "key_concepts": ["variables", "let", "const", "data types"],
    "related_topics": ["js-basics-2"],
    "prerequisites": [],
}
js_topic_2 = {
    "id": "js-basics-2", "title": "Functions & Scope",
    "description": "Function declarations, expressions, closures, and lexical scope",
    "order_index": 2,
    "exercises": [js_ex_2_1, js_ex_2_2],
    "key_concepts": ["functions", "closures", "scope"],
    "related_topics": ["js-basics-3"],
    "prerequisites": ["js-basics-1"],
}
py_topic_1 = {
    "id": "py-basics-1", "title": "Python Fundamentals",
    "description": "Variables, data types, basic input/output",
    "order_index": 1,
    "exercises": [py_ex_1_1],
    "key_concepts": ["print", "strings"],
    "related_topics": ["py-basics-2"],
    "prerequisites": [],
}
py_topic_2 = {
    "id": "py-basics-2", "title": "Control Flow",
    "description": "If/elif/else and loops",
    "order_index": 2,
    "exercises": [py_ex_2_1],
    "key_concepts": ["if", "elif", "else", "for", "while"],
    "related_topics": ["py-basics-3"],
    "prerequisites": ["py-basics-1"],
}
sd_topic_1 = {
    "id": "sd-scalability-1", "title": "Scaling Databases",
    "description": "Vertical vs horizontal scaling, read replicas, sharding",
    "order_index": 1,
    "exercises": [sd_ex_1_1],
    "key_concepts": ["replication", "sharding", "read-replicas"],
    "related_topics": ["sd-monitoring-1"],
    "prerequisites": [],
}


# ============================================================
# Skill Path dicts
# ============================================================

js_fundamentals_path = {
    "id": "js-fundamentals",
    "title": "JavaScript Fundamentals",
    "description": "Master JavaScript from variables to async patterns",
    "order_index": 1,
    "topics": [js_topic_1, js_topic_2],
    "total_estimated_minutes": 45,
    "difficulty": "beginner",
    "premium_only": False,
    "completion_badge": "js-fundamentals-badge",
}
py_fundamentals_path = {
    "id": "py-fundamentals",
    "title": "Python Fundamentals",
    "description": "Start programming with Python the right way",
    "order_index": 2,
    "topics": [py_topic_1, py_topic_2],
    "total_estimated_minutes": 30,
    "difficulty": "beginner",
    "premium_only": False,
    "completion_badge": "py-fundamentals-badge",
}
sd_scalability_path = {
    "id": "sd-scalability",
    "title": "System Design: Scalability",
    "description": "Design distributed systems that scale",
    "order_index": 3,
    "topics": [sd_topic_1],
    "total_estimated_minutes": 45,
    "difficulty": "advanced",
    "premium_only": True,
    "completion_badge": "system-design-badge",
}

curriculum_skill_paths: List[Dict[str, Any]] = [js_fundamentals_path, py_fundamentals_path, sd_scalability_path]

# Build lookup maps
topic_id_map: Dict[str, Dict[str, Any]] = {}
exercise_id_map: Dict[str, Dict[str, Any]] = {}
for path in curriculum_skill_paths:
    for topic in path["topics"]:
        topic_id_map[topic["id"]] = topic
        for ex in topic["exercises"]:
            exercise_id_map[ex["id"]] = ex


def get_skill_path(path_id: str):
    for p in curriculum_skill_paths:
        if p["id"] == path_id:
            return p
    return None


def get_topic(topic_id: str):
    return topic_id_map.get(topic_id)


def get_exercise(exercise_id: str):
    return exercise_id_map.get(exercise_id)


def get_all_topics():
    result = []
    for path in curriculum_skill_paths:
        result.extend(path["topics"])
    return result


def get_path_with_progress(user_progress: Dict[str, set]):
    """Given user progress (set of completed exercise IDs per path), return enriched path data."""
    result = []
    for path in curriculum_skill_paths:
        completed_exercises: set = set()
        for topic in path["topics"]:
            for ex in topic["exercises"]:
                if exercise_id_map.get(ex["id"]) and exercise_id_map[ex["id"]].get("id") in user_progress.get(path["id"], set()):
                    completed_exercises.add(ex["id"])
        total = sum(len(t["exercises"]) for t in path["topics"])
        completed = len(completed_exercises)
        result.append({
            "path_id": path["id"],
            "title": path["title"],
            "description": path["description"],
            "difficulty": path["difficulty"],
            "premium_only": path["premium_only"],
            "completion_pct": round(completed / total * 100, 1) if total else 0,
            "completed": completed,
            "total": total,
            "badge": path["completion_badge"],
            "topics": [
                {
                    "title": t["title"],
                    "exercises": len(t["exercises"]),
                    "completed": sum(1 for t_ex in t["exercises"]
                                     if exercise_id_map.get(t_ex["id"]) and exercise_id_map[t_ex["id"]].get("id") in user_progress.get(path["id"], set())),
                    "exercise_ids": [t_ex["id"] for t_ex in t["exercises"]],
                }
                for t in path["topics"]
            ],
        })
    return result