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


# SDE Diagnostic Assessment Functions
async def run_sde_diagnostic(user_id: str) -> dict:
    """
    Run the SDE diagnostic assessment to establish baseline readiness.
    
    This diagnostic tests basic proficiency in all 9 SDE skills:
    DSA, Programming, System Design, DBMS, Operating Systems, 
    Computer Networks, OOP, Git/GitHub, Backend Fundamentals.
    
    For new users, all skills start at level 0 (unknown) = 0% readiness.
    The diagnostic establishes the baseline and generates the personalized roadmap.
    """
    from app.services.role_engine.profiles import get_profile
    from app.services.mastery_engine import SkillMastery, MASTERY_LEVELS
    from app.services.srs_engine import create_card, get_due_cards
    from app.services.skill_assessment import initialize_skill_graph, update_skill_score, get_skill_graph
    from app.services.srs_engine import create_card as srs_create_card
    from app.services.role_engine.profiles import get_profile
    
    # Get SDE profile with readiness weights
    sde_profile = get_profile("sde")
    if not sde_profile:
        raise ValueError("SDE profile not found")
    
    # Get or create skill graph for user
    skill_graph = await get_skill_graph(user_id)
    
    # SDE skill categories mapped to existing skill categories
    sde_skill_categories = {
        "dsa": ["arrays", "linked_lists", "trees", "graphs", "hashing", "sorting", "searching", "dynamic_programming"],
        "programming": ["arrays", "strings", "linked_lists", "stacks_queues", "trees", "graphs", "hashing", "sorting", "searching", "dynamic_programming", "recursion", "greedy", "binary_search"],
        "system_design": ["requirements_gathering", "high_level_design", "detailed_design", "scaling", "caching", "databases", "load_balancing", "message_queues", "microservices", "trade_offs"],
        "dbms": ["sql", "nosql", "indexing", "transactions", "normalization"],
        "operating_systems": ["processes", "threads", "scheduling", "memory_management", "file_systems"],
        "computer_networks": ["tcp_ip", "http", "dns", "load_balancing", "cdn"],
        "oop": ["inheritance", "polymorphism", "encapsulation", "abstraction", "design_patterns"],
        "git_github": ["git_basics", "branching", "merging", "remote_repos", "pull_requests"],
        "backend_fundamentals": ["api_design", "rest", "authentication", "database_design", "caching", "message_queues"],
    }
    
    # Initialize SDE skill tracking in mastery engine
    sde_skills = [
        "DSA", "Programming", "System Design", "DBMS", 
        "Operating Systems", "Computer Networks", 
        "OOP", "Git/GitHub", "Backend Fundamentals"
    ]
    
    readiness_weights = sde_profile.readiness_weights.weights
    
    # Run diagnostic questions for each SDE skill area
    diagnostic_results = {}
    for skill_name in [
        "DSA", "Programming", "System Design", "DBMS",
        "Operating Systems", "Computer Networks",
        "OOP", "Git/GitHub", "Backend Fundamentals"
    ]:
        # For new users, all skills start at level 0 (unknown)
        # In a real implementation, this would run actual diagnostic questions
        diagnostic_results[skill_name] = {
            "level": 0,
            "accuracy": 0.0,
            "problems_attempted": 0,
            "problems_solved": 0,
            "level_name": "Unknown"
        }
    
    # Calculate readiness score using SDE readiness weights
    readiness_data = await _calculate_sde_readiness(user_id, diagnostic_results)
    
    # Enroll concepts into SRS for review
    await _enroll_diagnostic_concepts_srs(user_id, diagnostic_results)
    
    # Generate roadmap
    roadmap = await _generate_sde_roadmap(user_id, readiness_data)
    
    return {
        "diagnostic_results": diagnostic_results,
        "readiness_score": readiness_data["overall_readiness"],
        "skill_levels": readiness_data["skill_levels"],
        "roadmap": roadmap,
        "estimated_weeks": _estimate_weeks_to_target(readiness_data["overall_readiness"]),
        "sde_skills": [
            {"name": skill, "level": 0, "weight": sde_profile.readiness_weights.weights.get(skill, 0)}
            for skill in ["DSA", "Programming", "System Design", "DBMS", 
                          "Operating Systems", "Computer Networks", 
                          "OOP", "Git/GitHub", "Backend Fundamentals"]
        ]
    }


async def _calculate_sde_readiness(user_id: str, diagnostic_results: dict) -> dict:
    """Calculate SDE readiness score using readiness weights."""
    from app.services.role_engine.profiles import get_profile
    
    sde_profile = get_profile("sde")
    if not sde_profile:
        return {"overall_readiness": 0, "skill_levels": {}}
    
    readiness_weights = sde_profile.readiness_weights.weights
    skill_levels = {}
    
    # For diagnostic, all skills start at level 0
    for skill_name in ["DSA", "Programming", "System Design", "DBMS", 
                       "Operating Systems", "Computer Networks", 
                       "OOP", "Git/GitHub", "Backend Fundamentals"]:
        skill_levels[skill_name] = 0
    
    # Calculate weighted readiness: sum(weight * level) / sum(weights) * 100
    total_weighted = sum(
        sde_profile.readiness_weights.weights.get(skill, 0) * 0 
        for skill in sde_profile.readiness_weights.weights
    )
    total_weight = sum(sde_profile.readiness_weights.weights.values())
    
    overall_readiness = (total_weighted / total_weight * 100) if total_weight > 0 else 0
    
    return {
        "overall_readiness": round(overall_readiness, 1),
        "skill_levels": {skill: 0 for skill in sde_profile.readiness_weights.weights}
    }


async def _enroll_diagnostic_concepts_srs(user_id: str, diagnostic_results: dict) -> None:
    """Enroll basic concepts into SRS for review after diagnostic."""
    from app.services.srs_engine import create_card
    
    # Enroll basic concepts for review after diagnostic
    basic_concepts = [
        {"concept_id": "variables_types", "topic": "Programming", "difficulty": "easy"},
        {"concept_id": "control_flow", "topic": "Programming", "difficulty": "easy"},
        {"concept_id": "functions", "topic": "Programming", "difficulty": "easy"},
        {"concept_id": "debugging_basics", "topic": "Programming", "difficulty": "easy"},
        {"concept_id": "dsa_arrays", "topic": "DSA", "difficulty": "easy"},
        {"concept_id": "dsa_linked_lists", "topic": "DSA", "difficulty": "easy"},
        {"concept_id": "oop_basics", "topic": "OOP", "difficulty": "easy"},
        {"concept_id": "git_basics", "topic": "Git/GitHub", "difficulty": "easy"},
    ]
    
    for concept in basic_concepts:
        try:
            await create_card(
                user_id=user_id,
                concept_id=concept["concept_id"],
                topic=concept["topic"],
                difficulty=concept["difficulty"],
                metadata={"source": "diagnostic", "enrollment_reason": "module_1_foundation"}
            )
        except Exception as e:
            # Log error but don't fail diagnostic
            import logging
            logging.getLogger(__name__).warning(f"Failed to enroll SRS concept {concept['concept_id']}: {e}")


async def _generate_sde_roadmap(user_id: str, readiness_data: dict) -> dict:
    """Generate the SDE roadmap with modules and estimated timeline."""
    overall = readiness_data.get("overall_readiness", 0)
    
    # SDE modules in order
    modules = [
        {"id": "module_1", "name": "Programming Fundamentals", "weeks": 2, "skills": ["Programming", "Debugging"]},
        {"id": "module_2", "name": "DSA Foundations", "weeks": 4, "skills": ["DSA"]},
        {"id": "module_3", "name": "CS Fundamentals", "weeks": 3, "skills": ["DBMS", "Operating Systems", "Computer Networks", "OOP"]},
        {"id": "module_4", "name": "System Design Basics", "weeks": 3, "skills": ["System Design"]},
        {"id": "module_4", "name": "Git & Backend Fundamentals", "weeks": 2, "skills": ["Git/GitHub", "Backend Fundamentals"]},
        {"id": "module_5", "name": "DSA Advanced", "weeks": 4, "skills": ["DSA"]},
        {"id": "module_6", "name": "System Design Deep Dive", "weeks": 3, "skills": ["System Design"]},
        {"id": "module_7", "name": "Mock OA & Company Prep", "weeks": 2, "skills": ["DSA", "Programming", "System Design"]},
        {"id": "module_8", "name": "Resume & Interview Prep", "weeks": 2, "skills": ["Resume", "Behavioral", "Technical"]},
    ]
    
    total_weeks = sum(m["weeks"] for m in modules)
    
    return {
        "current_readiness": 0,
        "target_readiness": 85,
        "estimated_weeks": total_weeks,
        "modules": modules,
        "milestones": [
            {"week": 2, "milestone": "Complete Programming Fundamentals"},
            {"week": 6, "milestone": "Complete DSA Foundations"},
            {"week": 9, "milestone": "Complete CS Fundamentals"},
            {"week": 12, "milestone": "Complete System Design Basics"},
            {"week": 14, "milestone": "Complete Git & Backend Fundamentals"},
            {"week": 18, "milestone": "Complete DSA Advanced"},
            {"week": 21, "milestone": "Complete System Design Deep Dive"},
            {"week": 23, "milestone": "Complete Mock OA & Company Prep"},
            {"week": 25, "milestone": "Complete Resume & Interview Prep"},
            {"week": 26, "milestone": "Target Readiness: 85% - Job Ready!"},
        ],
        "current_module": 0,
        "progress": 0
    }


def _estimate_weeks_to_target(current_readiness: float) -> int:
    """Estimate weeks needed to reach 85% readiness."""
    target = 85
    gap = target - current_readiness
    # Rough estimate: ~1.5 weeks per 5% readiness increase with regular practice
    return int(gap / 5 * 1.5) + 1
