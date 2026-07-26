from datetime import datetime, timezone
from app.database import users_collection, skill_graph_collection
from bson import ObjectId


# Skill categories and their sub-skills
SKILL_CATEGORIES = {
    "dsa": {
        "name": "Data Structures & Algorithms",
        "skills": [
            "arrays", "strings", "linked_lists", "stacks_queues",
            "trees", "graphs", "hashing", "sorting", "searching",
            "dynamic_programming", "recursion", "greedy", "binary_search",
        ],
    },
    "system_design": {
        "name": "System Design",
        "skills": [
            "requirements_gathering", "high_level_design", "detailed_design",
            "scaling", "caching", "databases", "load_balancing",
            "message_queues", "microservices", "trade_offs",
        ],
    },
    "behavioral": {
        "name": "Behavioral",
        "skills": [
            "leadership", "conflict_resolution", "teamwork",
            "problem_solving", "communication", "adaptability",
            "time_management", "customer_focus", "innovation",
        ],
    },
    "aptitude": {
        "name": "Aptitude",
        "skills": [
            "quantitative", "logical_reasoning", "verbal_ability",
            "data_interpretation", "puzzles", "mental_ability",
        ],
    },
    "resume": {
        "name": "Resume & ATS",
        "skills": [
            "content_quality", "ats_optimization", "keyword_usage",
            "formatting", "impact_statements", "tailoring",
        ],
    },
}


async def initialize_skill_graph(user_id: str):
    """Initialize a skill graph for a new user."""
    skill_graph = {
        "user_id": user_id,
        "categories": {},
        "overall_score": 0,
        "assessments_completed": 0,
        "last_assessment": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    for cat_id, cat_info in SKILL_CATEGORIES.items():
        skill_graph["categories"][cat_id] = {
            "name": cat_info["name"],
            "score": 0,
            "skills": {skill: {"score": 0, "attempts": 0, "last_practiced": None}
                       for skill in cat_info["skills"]},
        }

    await skill_graph_collection.insert_one(skill_graph)
    return skill_graph


async def update_skill_score(user_id: str, category: str, skill: str, score: float, is_correct: bool):
    """Update a specific skill score based on practice results."""
    now = datetime.now(timezone.utc)

    # Get or create skill graph
    skill_graph = await skill_graph_collection.find_one({"user_id": user_id})
    if not skill_graph:
        skill_graph = await initialize_skill_graph(user_id)

    # Update the specific skill
    update_path = f"categories.{category}.skills.{skill}"

    # Calculate new score using weighted average
    current_skill = skill_graph.get("categories", {}).get(category, {}).get("skills", {}).get(skill, {})
    current_score = current_skill.get("score", 0)
    attempts = current_skill.get("attempts", 0)

    # Weighted average: new score has more weight as attempts increase
    weight = min(0.3, 1 / (attempts + 1))
    new_score = current_score * (1 - weight) + score * weight if is_correct else current_score * (1 - weight)

    await skill_graph_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                f"{update_path}.score": round(new_score, 2),
                f"{update_path}.attempts": attempts + 1,
                f"{update_path}.last_practiced": now,
                "updated_at": now,
            },
            "$inc": {"assessments_completed": 1},
        },
    )

    # Recalculate category average
    await _recalculate_category_score(user_id, category)


async def _recalculate_category_score(user_id: str, category: str):
    """Recalculate the average score for a category."""
    skill_graph = await skill_graph_collection.find_one({"user_id": user_id})
    if not skill_graph:
        return

    skills = skill_graph.get("categories", {}).get(category, {}).get("skills", {})
    if not skills:
        return

    scores = [s.get("score", 0) for s in skills.values() if s.get("attempts", 0) > 0]
    avg_score = sum(scores) / len(scores) if scores else 0

    await skill_graph_collection.update_one(
        {"user_id": user_id},
        {"$set": {f"categories.{category}.score": round(avg_score, 2)}},
    )

    # Recalculate overall score
    categories = skill_graph.get("categories", {})
    cat_scores = [c.get("score", 0) for c in categories.values() if c.get("score", 0) > 0]
    overall = sum(cat_scores) / len(cat_scores) if cat_scores else 0

    await skill_graph_collection.update_one(
        {"user_id": user_id},
        {"$set": {"overall_score": round(overall, 2)}},
    )


async def get_skill_graph(user_id: str) -> dict:
    """Get the full skill graph for a user."""
    skill_graph = await skill_graph_collection.find_one({"user_id": user_id})
    if not skill_graph:
        skill_graph = await initialize_skill_graph(user_id)

    skill_graph["id"] = str(skill_graph.pop("_id"))
    return skill_graph


async def get_weak_areas(user_id: str, top_n: int = 5) -> list:
    """Get the user's weakest skills across all categories."""
    skill_graph = await skill_graph_collection.find_one({"user_id": user_id})
    if not skill_graph:
        return []

    weak_skills = []
    for cat_id, cat_data in skill_graph.get("categories", {}).items():
        for skill_name, skill_data in cat_data.get("skills", {}).items():
            if skill_data.get("attempts", 0) > 0:
                weak_skills.append({
                    "category": cat_id,
                    "category_name": cat_data.get("name", ""),
                    "skill": skill_name,
                    "score": skill_data.get("score", 0),
                    "attempts": skill_data.get("attempts", 0),
                })

    # Sort by score ascending (weakest first)
    weak_skills.sort(key=lambda x: x["score"])
    return weak_skills[:top_n]


async def get_readiness_score(user_id: str, company: str = None) -> dict:
    """Calculate interview readiness score for a specific company or overall."""
    skill_graph = await skill_graph_collection.find_one({"user_id": user_id})
    if not skill_graph:
        return {"overall": 0, "categories": {}, "recommendations": []}

    categories = skill_graph.get("categories", {})
    scores = {}
    recommendations = []

    for cat_id, cat_data in categories.items():
        score = cat_data.get("score", 0)
        scores[cat_id] = score

        if score < 50:
            recommendations.append(f"Focus on improving {cat_data.get('name', cat_id)} (current: {score}%)")
        elif score < 70:
            recommendations.append(f"Practice more {cat_data.get('name', cat_id)} to reach 70%+")

    overall = sum(scores.values()) / len(scores) if scores else 0

    return {
        "overall": round(overall, 1),
        "categories": scores,
        "recommendations": recommendations,
        "company": company,
    }
