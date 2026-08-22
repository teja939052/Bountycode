"""Mission Engine — the 5-layer learning loop.

Layer 1: Story    — WHY we're learning this (context, motivation)
Layer 2: Concept  — THE IDEA (explanation, examples, visualization)
Layer 3: Interact — PLAY with it (predict, trace, manipulate, visualize)
Layer 4: Code     — BUILD it (write real code, run tests)
Layer 5: Mastery  — PROVE it (boss trial, mixed challenge types)

Every mission feeds into per-topic mastery which drives career readiness.
"""
from datetime import datetime, timezone
from app.database import (
    skill_graph_collection,
    gamification_collection,
    learning_progress_collection,
)

# ─── Interaction Types ───
INTERACTION_TYPES = {
    "predict": {
        "id": "predict",
        "name": "Predict the Output",
        "icon": "🔮",
        "description": "What does this code produce?",
        "xp_base": 15,
        "mastery_dimension": "prediction",
        "time_limit": 45,
    },
    "trace": {
        "id": "trace",
        "name": "Trace Mode",
        "icon": "🧠",
        "description": "Follow the execution step by step",
        "xp_base": 20,
        "mastery_dimension": "understanding",
        "time_limit": 60,
    },
    "bug_hunt": {
        "id": "bug_hunt",
        "name": "Hunt the Bug",
        "icon": "🐛",
        "description": "Find and fix the error",
        "xp_base": 25,
        "mastery_dimension": "debugging",
        "time_limit": 60,
    },
    "challenge": {
        "id": "challenge",
        "name": "Code Challenge",
        "icon": "⚔️",
        "description": "Write the solution yourself",
        "xp_base": 30,
        "mastery_dimension": "coding",
        "time_limit": 120,
    },
    "test_lab": {
        "id": "test_lab",
        "name": "Test Lab",
        "icon": "🧪",
        "description": "Run hidden tests and learn from failures",
        "xp_base": 20,
        "mastery_dimension": "coding",
        "time_limit": 90,
    },
    "speed_run": {
        "id": "speed_run",
        "name": "Speed Run",
        "icon": "🏎️",
        "description": "Solve under time pressure",
        "xp_base": 35,
        "mastery_dimension": "coding",
        "time_limit": 30,
    },
}

# ─── Mastery Dimensions ───
MASTERY_DIMENSIONS = {
    "understanding": {"name": "Understanding", "icon": "📖", "weight": 0.25},
    "prediction": {"name": "Prediction", "icon": "🔮", "weight": 0.20},
    "coding": {"name": "Coding", "icon": "💻", "weight": 0.30},
    "debugging": {"name": "Debugging", "icon": "🐛", "weight": 0.25},
}

# ─── Combo Thresholds ───
COMBO_THRESHOLDS = [
    {"streak": 3, "multiplier": 1.2, "label": "3× Learning Combo"},
    {"streak": 5, "multiplier": 1.5, "label": "5× Learning Combo"},
    {"streak": 8, "multiplier": 2.0, "label": "8× Learning Combo"},
    {"streak": 12, "multiplier": 3.0, "label": "12× GODLIKE Combo"},
]

# ─── Skill-Specific Ranks ───
SKILL_RANKS = [
    {"min_score": 0, "rank": "Novice", "icon": "🌱", "color": "#9CA3AF"},
    {"min_score": 20, "rank": "Apprentice", "icon": "⚔️", "color": "#22C55E"},
    {"min_score": 40, "rank": "Solver", "icon": "🧠", "color": "#3B82F6"},
    {"min_score": 60, "rank": "Expert", "icon": "🔥", "color": "#F59E0B"},
    {"min_score": 80, "rank": "Master", "icon": "💎", "color": "#A855F7"},
    {"min_score": 95, "rank": "Legend", "icon": "👑", "color": "#EF4444"},
]

# ─── Domain Definitions (what topics map to what career skills) ───
DOMAIN_MAP = {
    "variables": {"domain": "dsa", "sub_skill": "arrays", "readiness_weight": 0.05},
    "control_flow": {"domain": "dsa", "sub_skill": "recursion", "readiness_weight": 0.05},
    "loops": {"domain": "dsa", "sub_skill": "arrays", "readiness_weight": 0.05},
    "functions": {"domain": "dsa", "sub_skill": "recursion", "readiness_weight": 0.05},
    "arrays": {"domain": "dsa", "sub_skill": "arrays", "readiness_weight": 0.08},
    "strings": {"domain": "dsa", "sub_skill": "strings", "readiness_weight": 0.06},
    "linked_lists": {"domain": "dsa", "sub_skill": "linked_lists", "readiness_weight": 0.06},
    "stacks_queues": {"domain": "dsa", "sub_skill": "stacks_queues", "readiness_weight": 0.06},
    "trees": {"domain": "dsa", "sub_skill": "trees", "readiness_weight": 0.08},
    "graphs": {"domain": "dsa", "sub_skill": "graphs", "readiness_weight": 0.08},
    "sorting": {"domain": "dsa", "sub_skill": "sorting", "readiness_weight": 0.07},
    "searching": {"domain": "dsa", "sub_skill": "binary_search", "readiness_weight": 0.07},
    "hashing": {"domain": "dsa", "sub_skill": "hashing", "readiness_weight": 0.06},
    "dynamic_programming": {"domain": "dsa", "sub_skill": "dynamic_programming", "readiness_weight": 0.08},
    "recursion": {"domain": "dsa", "sub_skill": "recursion", "readiness_weight": 0.06},
    "greedy": {"domain": "dsa", "sub_skill": "greedy", "readiness_weight": 0.06},
    "dbms": {"domain": "system_design", "sub_skill": "databases", "readiness_weight": 0.06},
    "os": {"domain": "system_design", "sub_skill": "scaling", "readiness_weight": 0.05},
    "networks": {"domain": "system_design", "sub_skill": "load_balancing", "readiness_weight": 0.05},
    "system_design": {"domain": "system_design", "sub_skill": "high_level_design", "readiness_weight": 0.08},
    "oop": {"domain": "dsa", "sub_skill": "recursion", "readiness_weight": 0.04},
}


def get_skill_rank(score: float) -> dict:
    rank = SKILL_RANKS[0]
    for r in SKILL_RANKS:
        if score >= r["min_score"]:
            rank = r
    return rank


def get_combo_multiplier(consecutive_correct: int) -> dict:
    best = {"streak": 0, "multiplier": 1.0, "label": ""}
    for t in COMBO_THRESHOLDS:
        if consecutive_correct >= t["streak"]:
            best = t
    return best


async def get_topic_mastery(user_id: str, topic: str) -> dict:
    """Get multi-dimensional mastery for a specific topic."""
    doc = await skill_graph_collection.find_one({"user_id": user_id})
    if not doc:
        return _empty_mastery(topic)

    categories = doc.get("categories", {})
    domain_info = DOMAIN_MAP.get(topic, {"domain": "dsa", "sub_skill": topic})
    domain = domain_info["domain"]
    sub_skill = domain_info["sub_skill"]

    cat_data = categories.get(domain, {})
    skills = cat_data.get("skills", {})
    skill_data = skills.get(sub_skill, {})

    raw_score = skill_data.get("score", 0)
    attempts = skill_data.get("attempts", 0)

    dimensions = {}
    for dim_id, dim_info in MASTERY_DIMENSIONS.items():
        dim_score = skill_data.get(f"dim_{dim_id}", raw_score)
        dimensions[dim_id] = {
            "name": dim_info["name"],
            "icon": dim_info["icon"],
            "score": round(dim_score, 1),
            "attempts": skill_data.get(f"dim_{dim_id}_attempts", 0),
        }

    overall = sum(d["score"] * MASTERY_DIMENSIONS[k]["weight"] for k, d in dimensions.items())
    rank = get_skill_rank(overall)

    return {
        "topic": topic,
        "domain": domain,
        "sub_skill": sub_skill,
        "overall": round(overall, 1),
        "rank": rank,
        "dimensions": dimensions,
        "total_attempts": attempts,
        "last_practiced": skill_data.get("last_practiced"),
    }


def _empty_mastery(topic: str) -> dict:
    domain_info = DOMAIN_MAP.get(topic, {"domain": "dsa", "sub_skill": topic})
    return {
        "topic": topic,
        "domain": domain_info["domain"],
        "sub_skill": domain_info["sub_skill"],
        "overall": 0.0,
        "rank": SKILL_RANKS[0],
        "dimensions": {k: {"name": v["name"], "icon": v["icon"], "score": 0, "attempts": 0} for k, v in MASTERY_DIMENSIONS.items()},
        "total_attempts": 0,
        "last_practiced": None,
    }


async def update_topic_mastery(user_id: str, topic: str, interaction_type: str, score: float, is_correct: bool) -> dict:
    """Update per-topic mastery after an interaction. Returns updated mastery + XP earned + combo info."""
    domain_info = DOMAIN_MAP.get(topic, {"domain": "dsa", "sub_skill": topic})
    domain = domain_info["domain"]
    sub_skill = domain_info["sub_skill"]

    interaction = INTERACTION_TYPES.get(interaction_type, INTERACTION_TYPES["challenge"])
    dimension = interaction["mastery_dimension"]

    doc = await skill_graph_collection.find_one({"user_id": user_id})
    if not doc:
        doc = {"user_id": user_id, "categories": {}, "overall_score": 0, "assessments_completed": 0}

    categories = doc.get("categories", {})
    if domain not in categories:
        categories[domain] = {"name": domain, "score": 0, "skills": {}}
    if sub_skill not in categories[domain]["skills"]:
        categories[domain]["skills"][sub_skill] = {"score": 0, "attempts": 0, "last_practiced": None}

    skill = categories[domain]["skills"][sub_skill]

    old_dim_score = skill.get(f"dim_{dimension}", skill.get("score", 0))
    dim_attempts = skill.get(f"dim_{dimension}_attempts", 0)

    weight = min(0.3, 1 / (dim_attempts + 1))
    if is_correct:
        new_dim_score = old_dim_score * (1 - weight) + score * weight
    else:
        new_dim_score = old_dim_score * (1 - weight)

    skill[f"dim_{dimension}"] = round(new_dim_score, 2)
    skill[f"dim_{dimension}_attempts"] = dim_attempts + 1
    skill["attempts"] = skill.get("attempts", 0) + 1
    skill["last_practiced"] = datetime.now(timezone.utc).isoformat()

    dim_scores = [skill.get(f"dim_{d}", 0) for d in MASTERY_DIMENSIONS]
    skill["score"] = round(sum(dim_scores) / len(dim_scores), 2)

    dim_scores_with_attempts = [skill.get(f"dim_{d}", 0) for d in MASTERY_DIMENSIONS if skill.get(f"dim_{d}_attempts", 0) > 0]
    if dim_scores_with_attempts:
        categories[domain]["score"] = round(sum(dim_scores_with_attempts) / len(dim_scores_with_attempts), 2)

    all_cat_scores = [c["score"] for c in categories.values() if c.get("score", 0) > 0]
    overall = round(sum(all_cat_scores) / len(all_cat_scores), 2) if all_cat_scores else 0

    await skill_graph_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "categories": categories,
            "overall_score": overall,
            "assessments_completed": doc.get("assessments_completed", 0) + 1,
        }},
        upsert=True,
    )

    gam_doc = await gamification_collection.find_one({"user_id": user_id}) or {}
    combo_data = gam_doc.get("mission_combo", {"consecutive_correct": 0, "best_combo": 0})
    if is_correct:
        combo_data["consecutive_correct"] = combo_data.get("consecutive_correct", 0) + 1
    else:
        combo_data["consecutive_correct"] = 0

    combo = get_combo_multiplier(combo_data["consecutive_correct"])
    combo_data["best_combo"] = max(combo_data.get("best_combo", 0), combo_data["consecutive_correct"])

    base_xp = interaction["xp_base"]
    xp_earned = int(base_xp * combo["multiplier"])

    gam_xp = gam_doc.get("xp", 0) + xp_earned
    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$set": {"mission_combo": combo_data, "xp": gam_xp}},
        upsert=True,
    )

    domain_info_map = DOMAIN_MAP.get(topic, {})
    readiness_boost = 0
    if is_correct and domain_info_map.get("readiness_weight"):
        readiness_boost = round(domain_info_map["readiness_weight"] * (score / 100), 2)

    return {
        "mastery": await get_topic_mastery(user_id, topic),
        "xp_earned": xp_earned,
        "combo": combo,
        "consecutive_correct": combo_data["consecutive_correct"],
        "readiness_boost": readiness_boost,
    }


async def get_all_topic_mastery(user_id: str) -> list:
    """Get mastery for all topics across all domains."""
    doc = await skill_graph_collection.find_one({"user_id": user_id})
    if not doc:
        return [_empty_mastery(t) for t in DOMAIN_MAP]

    categories = doc.get("categories", {})
    results = []
    for topic, domain_info in DOMAIN_MAP.items():
        domain = domain_info["domain"]
        sub_skill = domain_info["sub_skill"]
        cat_data = categories.get(domain, {})
        skill_data = cat_data.get("skills", {}).get(sub_skill, {})

        raw_score = skill_data.get("score", 0)
        attempts = skill_data.get("attempts", 0)
        dimensions = {}
        for dim_id, dim_info in MASTERY_DIMENSIONS.items():
            dim_score = skill_data.get(f"dim_{dim_id}", raw_score)
            dimensions[dim_id] = {"name": dim_info["name"], "icon": dim_info["icon"], "score": round(dim_score, 1), "attempts": skill_data.get(f"dim_{dim_id}_attempts", 0)}

        overall = sum(d["score"] * MASTERY_DIMENSIONS[k]["weight"] for k, d in dimensions.items())
        rank = get_skill_rank(overall)
        results.append({
            "topic": topic, "domain": domain, "sub_skill": sub_skill,
            "overall": round(overall, 1), "rank": rank, "dimensions": dimensions,
            "total_attempts": attempts, "last_practiced": skill_data.get("last_practiced"),
        })

    return results


async def get_learning_stats(user_id: str) -> dict:
    """Get overall learning stats for the career XP dashboard."""
    mastery_data = await get_all_topic_mastery(user_id)
    gam_doc = await gamification_collection.find_one({"user_id": user_id}) or {}

    total_topics = len(mastery_data)
    practiced = [m for m in mastery_data if m["total_attempts"] > 0]
    mastered = [m for m in mastery_data if m["overall"] >= 80]
    combo = gam_doc.get("mission_combo", {"consecutive_correct": 0, "best_combo": 0})

    return {
        "total_topics": total_topics,
        "practiced_count": len(practiced),
        "mastered_count": len(mastered),
        "avg_mastery": round(sum(m["overall"] for m in practiced) / len(practiced), 1) if practiced else 0,
        "best_combo": combo.get("best_combo", 0),
        "current_combo": combo.get("consecutive_correct", 0),
        "rank_distribution": _rank_distribution(practiced),
    }


def _rank_distribution(mastery_list: list) -> dict:
    dist = {r["rank"]: 0 for r in SKILL_RANKS}
    for m in mastery_list:
        dist[m["rank"]["rank"]] = dist.get(m["rank"]["rank"], 0) + 1
    return dist


# ─── Hints System ───
HINT_LEVELS = [
    {"level": 1, "label": "Nudge", "description": "A gentle push in the right direction"},
    {"level": 2, "label": "Direction", "description": "Point toward the relevant concept"},
    {"level": 3, "label": "Approach", "description": "Describe the approach without the answer"},
]


def get_hint(topic: str, interaction_type: str, hint_level: int, context: dict = None) -> dict:
    """Generate a progressive hint. Never gives the answer directly."""
    level = max(1, min(3, hint_level))
    hint_info = HINT_LEVELS[level - 1]

    hints = {
        1: _nudge_hint(topic, interaction_type, context),
        2: _direction_hint(topic, interaction_type, context),
        3: _approach_hint(topic, interaction_type, context),
    }

    return {
        "level": level,
        "label": hint_info["label"],
        "text": hints.get(level, "Think about the core concept."),
        "xp_penalty": (level - 1) * 5,
    }


def _nudge_hint(topic: str, interaction_type: str, ctx: dict = None) -> str:
    nudges = {
        "variables": "Think about where data is stored in memory.",
        "control_flow": "Consider what happens when a condition is true vs false.",
        "loops": "How many times does the loop execute?",
        "functions": "What does the function return?",
        "arrays": "What's the index of each element?",
        "strings": "Strings are sequences of characters.",
        "linked_lists": "Each node points to the next one.",
        "trees": "Think about the parent-child relationship.",
        "graphs": "Consider visited nodes and the traversal order.",
        "sorting": "What does each iteration accomplish?",
        "searching": "How does the search space change each step?",
        "dynamic_programming": "Have you solved a smaller version of this problem?",
    }
    return nudges.get(topic, "Focus on what the code is trying to accomplish.")


def _direction_hint(topic: str, interaction_type: str, ctx: dict = None) -> str:
    directions = {
        "variables": "Look at the variable name and what value it holds.",
        "control_flow": "Trace the boolean condition at each branch.",
        "loops": "Count: what's the starting value, ending condition, and step?",
        "functions": "Follow the function call: what goes in, what comes out?",
        "arrays": "Access each index step by step.",
        "sorting": "Compare adjacent elements — what's the rule?",
        "searching": "Which half of the data can you eliminate?",
        "dynamic_programming": "Look for overlapping subproblems.",
    }
    return directions.get(topic, "Break the problem into smaller pieces.")


def _approach_hint(topic: str, interaction_type: str, ctx: dict = None) -> str:
    approaches = {
        "variables": "Identify the variable name, the assignment operator, and the value being stored.",
        "control_flow": "Write out: IF condition THEN action ELSE alternative.",
        "loops": "Set up: initialization → condition → update → body.",
        "functions": "Map: parameters → body logic → return value.",
        "arrays": "Use an index variable from 0 to length-1.",
        "sorting": "For each pass, move the largest unsorted element to its correct position.",
        "searching": "Maintain left and right pointers, calculate mid, compare.",
        "dynamic_programming": "Build a table from smallest subproblem to the target.",
    }
    return approaches.get(topic, "Start with the simplest case and work up.")
