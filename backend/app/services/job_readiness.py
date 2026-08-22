"""Job Readiness Engine — the outcome loop.

JOB TARGET → SKILL REQUIREMENTS → DIAGNOSTIC → GAP → CURRICULUM → PRACTICE → ASSESSMENT → PROOF → INTERVIEW → READINESS

This is the core differentiator. Not an LMS, not LeetCode, not a resume builder.
A system that closes the gap between "I want this job" and "I'm ready for this job."
"""
from datetime import datetime, timezone
from app.database import (
    skill_graph_collection, gamification_collection,
    solved_problems_collection, submissions_collection,
    interviews_collection, resumes_collection,
    question_answers_collection, aptitude_tests_collection,
    generated_projects_collection,
)
from app.services.skill_assessment import SKILL_CATEGORIES
from app.services.mission_engine import DOMAIN_MAP, get_skill_rank

# ─── Role Definitions ───
# Each role has required skill categories with minimum proficiency levels
ROLE_PROFILES = {
    "sde": {
        "id": "sde",
        "title": "Software Engineer",
        "icon": "💻",
        "description": "Full-stack or backend software development",
        "required_skills": {
            "dsa": {"weight": 0.30, "min_score": 60, "critical_topics": ["arrays", "trees", "graphs", "dynamic_programming", "hashing", "sorting", "searching"]},
            "coding": {"weight": 0.20, "min_score": 65, "critical_topics": ["python", "javascript", "system_design"]},
            "system_design": {"weight": 0.15, "min_score": 40, "critical_topics": ["high_level_design", "databases", "caching", "load_balancing"]},
            "behavioral": {"weight": 0.15, "min_score": 50, "critical_topics": ["leadership", "teamwork", "conflict_resolution"]},
            "aptitude": {"weight": 0.10, "min_score": 50, "critical_topics": ["quantitative", "logical_reasoning"]},
            "resume": {"weight": 0.10, "min_score": 55, "critical_topics": ["impact_statements", "ats_optimization"]},
        },
        "mission_topics": ["variables", "control_flow", "loops", "functions", "arrays", "strings", "sorting", "searching", "linked_lists", "stacks_queues", "trees", "graphs", "hashing", "recursion", "dynamic_programming", "greedy", "oop"],
        "interview_types": ["technical", "behavioral", "system_design"],
        "typical_companies": ["tcs", "infosys", "wipro", "google", "amazon", "microsoft", "meta", "apple"],
    },
    "data_analyst": {
        "id": "data_analyst",
        "title": "Data Analyst",
        "icon": "📊",
        "description": "Data analysis, visualization, and business intelligence",
        "required_skills": {
            "dsa": {"weight": 0.15, "min_score": 40, "critical_topics": ["arrays", "hashing"]},
            "coding": {"weight": 0.20, "min_score": 55, "critical_topics": ["python", "sql", "statistics"]},
            "aptitude": {"weight": 0.25, "min_score": 65, "critical_topics": ["quantitative", "data_interpretation", "logical_reasoning"]},
            "behavioral": {"weight": 0.15, "min_score": 50, "critical_topics": ["communication", "problem_solving"]},
            "resume": {"weight": 0.15, "min_score": 55, "critical_topics": ["impact_statements", "ats_optimization"]},
            "system_design": {"weight": 0.10, "min_score": 30, "critical_topics": ["databases"]},
        },
        "mission_topics": ["variables", "control_flow", "loops", "functions", "arrays", "strings", "hashing", "sorting", "searching", "dbms", "networks"],
        "interview_types": ["technical", "behavioral", "case_study"],
        "typical_companies": ["google", "amazon", "flipkart", "swiggy", "razorpay"],
    },
    "data_scientist": {
        "id": "data_scientist",
        "title": "Data Scientist",
        "icon": "🔬",
        "description": "Machine learning, statistical modeling, AI",
        "required_skills": {
            "dsa": {"weight": 0.20, "min_score": 50, "critical_topics": ["arrays", "hashing", "dynamic_programming"]},
            "coding": {"weight": 0.25, "min_score": 60, "critical_topics": ["python", "ml_algorithms", "statistics"]},
            "aptitude": {"weight": 0.15, "min_score": 55, "critical_topics": ["quantitative", "data_interpretation"]},
            "behavioral": {"weight": 0.15, "min_score": 50, "critical_topics": ["communication", "problem_solving"]},
            "resume": {"weight": 0.15, "min_score": 55, "critical_topics": ["impact_statements", "ats_optimization"]},
            "system_design": {"weight": 0.10, "min_score": 35, "critical_topics": ["databases", "scaling"]},
        },
        "mission_topics": ["variables", "control_flow", "loops", "functions", "arrays", "strings", "hashing", "sorting", "dynamic_programming", "recursion", "dbms"],
        "interview_types": ["technical", "behavioral", "case_study"],
        "typical_companies": ["google", "amazon", "microsoft", "flipkart", "phonepe"],
    },
    "qa_engineer": {
        "id": "qa_engineer",
        "title": "QA / SDET Engineer",
        "icon": "🧪",
        "description": "Quality assurance, test automation, SDET",
        "required_skills": {
            "dsa": {"weight": 0.15, "min_score": 40, "critical_topics": ["arrays", "strings", "sorting"]},
            "coding": {"weight": 0.25, "min_score": 60, "critical_topics": ["python", "java", "testing_frameworks"]},
            "aptitude": {"weight": 0.20, "min_score": 55, "critical_topics": ["logical_reasoning", "verbal_ability"]},
            "behavioral": {"weight": 0.15, "min_score": 50, "critical_topics": ["teamwork", "attention_to_detail"]},
            "resume": {"weight": 0.15, "min_score": 55, "critical_topics": ["impact_statements"]},
            "system_design": {"weight": 0.10, "min_score": 30, "critical_topics": ["databases"]},
        },
        "mission_topics": ["variables", "control_flow", "loops", "functions", "arrays", "strings", "hashing", "sorting", "searching", "oop", "dbms"],
        "interview_types": ["technical", "behavioral", "testing"],
        "typical_companies": ["tcs", "infosys", "wipro", "amazon", "microsoft"],
    },
    "devops": {
        "id": "devops",
        "title": "DevOps Engineer",
        "icon": "🔧",
        "description": "CI/CD, cloud infrastructure, automation",
        "required_skills": {
            "dsa": {"weight": 0.10, "min_score": 30, "critical_topics": ["arrays"]},
            "coding": {"weight": 0.20, "min_score": 50, "critical_topics": ["python", "shell_scripting"]},
            "system_design": {"weight": 0.30, "min_score": 55, "critical_topics": ["scaling", "caching", "load_balancing", "microservices", "databases"]},
            "behavioral": {"weight": 0.15, "min_score": 50, "critical_topics": ["teamwork", "problem_solving"]},
            "aptitude": {"weight": 0.10, "min_score": 40, "critical_topics": ["logical_reasoning"]},
            "resume": {"weight": 0.15, "min_score": 55, "critical_topics": ["ats_optimization"]},
        },
        "mission_topics": ["variables", "control_flow", "loops", "functions", "arrays", "dbms", "os", "networks", "system_design"],
        "interview_types": ["technical", "behavioral", "system_design"],
        "typical_companies": ["google", "amazon", "microsoft", "flipkart"],
    },
    "product_manager": {
        "id": "product_manager",
        "title": "Product Manager",
        "icon": "🎯",
        "description": "Product strategy, user research, execution",
        "required_skills": {
            "dsa": {"weight": 0.05, "min_score": 20, "critical_topics": []},
            "coding": {"weight": 0.10, "min_score": 30, "critical_topics": ["technical_communication"]},
            "system_design": {"weight": 0.15, "min_score": 45, "critical_topics": ["requirements_gathering", "trade_offs"]},
            "behavioral": {"weight": 0.35, "min_score": 70, "critical_topics": ["leadership", "communication", "customer_focus", "innovation"]},
            "aptitude": {"weight": 0.20, "min_score": 60, "critical_topics": ["data_interpretation", "logical_reasoning", "verbal_ability"]},
            "resume": {"weight": 0.15, "min_score": 60, "critical_topics": ["impact_statements", "tailoring"]},
        },
        "mission_topics": ["variables", "control_flow", "arrays", "dbms", "networks", "system_design"],
        "interview_types": ["behavioral", "case_study", "product_sense"],
        "typical_companies": ["google", "amazon", "microsoft", "flipkart", "swiggy"],
    },
}


# ─── Company Profiles (enhanced) ───
COMPANY_DEEP_PROFILES = {
    "google": {
        "id": "google",
        "title": "Google",
        "icon": "🔵",
        "tier": "faang",
        "color": "#4285F4",
        "min_readiness": 75,
        "skill_requirements": {
            "dsa": 80, "coding": 75, "system_design": 60,
            "behavioral": 65, "aptitude": 55, "resume": 65,
        },
        "oa_format": "2 coding problems (medium+hard), 90 min",
        "interview_rounds": ["Online Assessment", "Phone Screen", "Onsite (4-5 rounds)"],
        "focus_areas": ["Graph algorithms", "Dynamic programming", "System design", "Googleyness"],
        "leadership_principles": ["Focus on the user", "Think big", "Bias for action"],
    },
    "amazon": {
        "id": "amazon",
        "title": "Amazon",
        "icon": "🟠",
        "tier": "faang",
        "color": "#FF9900",
        "min_readiness": 70,
        "skill_requirements": {
            "dsa": 70, "coding": 65, "system_design": 55,
            "behavioral": 75, "aptitude": 50, "resume": 60,
        },
        "oa_format": "2 coding problems + work simulation, 80 min",
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Loop (5 rounds)"],
        "focus_areas": ["Leadership Principles", "STAR stories", "OOP design", "Arrays/Strings/HashMaps"],
        "leadership_principles": ["Customer Obsession", "Ownership", "Bias for Action", "Dive Deep", "Deliver Results"],
    },
    "microsoft": {
        "id": "microsoft",
        "title": "Microsoft",
        "icon": "🟢",
        "tier": "faang",
        "color": "#00A4EF",
        "min_readiness": 68,
        "skill_requirements": {
            "dsa": 68, "coding": 65, "system_design": 55,
            "behavioral": 60, "aptitude": 50, "resume": 58,
        },
        "oa_format": "2 coding problems, 60 min",
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Onsite (3-4 rounds)"],
        "focus_areas": ["Trees/Graphs", "Dynamic Programming", "OOP design", "Problem decomposition"],
        "leadership_principles": ["Growth mindset", "Customer obsession", "Bias for impact"],
    },
    "tcs": {
        "id": "tcs",
        "title": "TCS",
        "icon": "🔷",
        "tier": "mass",
        "color": "#0072C6",
        "min_readiness": 45,
        "skill_requirements": {
            "dsa": 45, "coding": 40, "system_design": 25,
            "behavioral": 40, "aptitude": 55, "resume": 40,
        },
        "oa_format": "Aptitude + coding + email writing",
        "interview_rounds": ["Online Assessment", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Basic coding", "Communication", "CS fundamentals"],
        "leadership_principles": [],
    },
    "infosys": {
        "id": "infosys",
        "title": "Infosys",
        "icon": "🔵",
        "tier": "mass",
        "color": "#007CC3",
        "min_readiness": 42,
        "skill_requirements": {
            "dsa": 40, "coding": 38, "system_design": 20,
            "behavioral": 38, "aptitude": 55, "resume": 38,
        },
        "oa_format": "Aptitude + programming logic",
        "interview_rounds": ["Online Assessment", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Programming basics", "Communication"],
        "leadership_principles": [],
    },
    "meta": {
        "id": "meta",
        "title": "Meta",
        "icon": "🔵",
        "tier": "faang",
        "color": "#0668E1",
        "min_readiness": 72,
        "skill_requirements": {
            "dsa": 75, "coding": 70, "system_design": 65,
            "behavioral": 60, "aptitude": 50, "resume": 60,
        },
        "oa_format": "2 coding problems, 45 min each",
        "interview_rounds": ["Technical Phone Screen", "Onsite (Coding + System Design + Behavioral)"],
        "focus_areas": ["Graphs", "DP", "System Design", "Behavioral"],
        "leadership_principles": ["Move fast", "Be bold", "Focus on long-term impact"],
    },
}


# ─── JD Analysis ───
# Map common JD keywords to our skill categories
JD_KEYWORD_MAP = {
    # DSA topics
    "data structures": ("dsa", "arrays", 0.8),
    "algorithms": ("dsa", "sorting", 0.8),
    "arrays": ("dsa", "arrays", 0.9),
    "linked list": ("dsa", "linked_lists", 0.7),
    "trees": ("dsa", "trees", 0.8),
    "graphs": ("dsa", "graphs", 0.8),
    "dynamic programming": ("dsa", "dynamic_programming", 0.9),
    "sorting": ("dsa", "sorting", 0.7),
    "searching": ("dsa", "searching", 0.7),
    "binary search": ("dsa", "binary_search", 0.7),
    "recursion": ("dsa", "recursion", 0.7),
    "hashing": ("dsa", "hashing", 0.7),
    "greedy": ("dsa", "greedy", 0.6),
    "stack": ("dsa", "stacks_queues", 0.6),
    "queue": ("dsa", "stacks_queues", 0.6),
    "bst": ("dsa", "trees", 0.8),
    "binary tree": ("dsa", "trees", 0.8),
    "heap": ("dsa", "trees", 0.7),
    "trie": ("dsa", "trees", 0.6),
    "backtracking": ("dsa", "recursion", 0.7),
    # Programming
    "python": ("coding", "python", 0.9),
    "java": ("coding", "java", 0.9),
    "javascript": ("coding", "javascript", 0.9),
    "react": ("coding", "frontend", 0.7),
    "node": ("coding", "backend", 0.7),
    "rest api": ("coding", "api_design", 0.7),
    "api": ("coding", "api_design", 0.6),
    "sql": ("dsa", "dbms", 0.8),
    "database": ("dsa", "dbms", 0.8),
    "mysql": ("dsa", "dbms", 0.7),
    "postgresql": ("dsa", "dbms", 0.7),
    "mongodb": ("dsa", "dbms", 0.6),
    # System design
    "system design": ("system_design", "high_level_design", 0.9),
    "distributed": ("system_design", "scaling", 0.8),
    "microservices": ("system_design", "microservices", 0.8),
    "scalability": ("system_design", "scaling", 0.8),
    "load balanc": ("system_design", "load_balancing", 0.7),
    "caching": ("system_design", "caching", 0.7),
    "redis": ("system_design", "caching", 0.6),
    "kafka": ("system_design", "message_queues", 0.6),
    "docker": ("system_design", "microservices", 0.5),
    "kubernetes": ("system_design", "microservices", 0.5),
    "cloud": ("system_design", "scaling", 0.5),
    "aws": ("system_design", "scaling", 0.5),
    "azure": ("system_design", "scaling", 0.5),
    # OS / Networks
    "operating system": ("dsa", "os", 0.7),
    "linux": ("dsa", "os", 0.5),
    "process": ("dsa", "os", 0.6),
    "thread": ("dsa", "os", 0.6),
    "tcp": ("dsa", "networks", 0.6),
    "http": ("dsa", "networks", 0.6),
    "networking": ("dsa", "networks", 0.7),
    # Behavioral
    "leadership": ("behavioral", "leadership", 0.9),
    "teamwork": ("behavioral", "teamwork", 0.8),
    "communication": ("behavioral", "communication", 0.9),
    "problem solving": ("behavioral", "problem_solving", 0.8),
    "conflict": ("behavioral", "conflict_resolution", 0.7),
    "agile": ("behavioral", "teamwork", 0.5),
    "scrum": ("behavioral", "teamwork", 0.5),
    # Aptitude
    "quantitative": ("aptitude", "quantitative", 0.8),
    "analytical": ("aptitude", "logical_reasoning", 0.7),
    "logical": ("aptitude", "logical_reasoning", 0.7),
}


def analyze_job_description(jd_text: str) -> dict:
    """Parse a job description and extract skill requirements.
    Returns skill gaps mapped to our system's categories.
    """
    jd_lower = jd_text.lower()
    detected_skills = {}
    skill_scores = {}

    for keyword, (category, topic, importance) in JD_KEYWORD_MAP.items():
        if keyword in jd_lower:
            key = f"{category}:{topic}"
            if key not in detected_skills or detected_skills[key][2] < importance:
                detected_skills[key] = (category, topic, importance)

    # Group by category
    requirements = {}
    for key, (category, topic, importance) in detected_skills.items():
        if category not in requirements:
            requirements[category] = {"topics": [], "importance": 0}
        requirements[category]["topics"].append({"topic": topic, "importance": importance})
        requirements[category]["importance"] = max(requirements[category]["importance"], importance)

    # Determine role match
    best_role = None
    best_match = 0
    for role_id, role in ROLE_PROFILES.items():
        match = 0
        total = 0
        for cat, req in role["required_skills"].items():
            if cat in requirements:
                match += req["weight"]
            total += req["weight"]
        score = match / total if total > 0 else 0
        if score > best_match:
            best_match = score
            best_role = role

    return {
        "detected_skills": requirements,
        "skill_count": sum(len(r["topics"]) for r in requirements.values()),
        "category_count": len(requirements),
        "matched_role": best_role["id"] if best_role else None,
        "role_match_score": round(best_match * 100),
    }


# ─── Competency Graph ───
def get_competency_graph(role_id: str) -> dict:
    """Get the competency graph for a role: nodes = skills, edges = prerequisites."""
    role = ROLE_PROFILES.get(role_id)
    if not role:
        return {"error": "Unknown role"}

    nodes = []
    edges = []

    for cat_id, req in role["required_skills"].items():
        cat_info = SKILL_CATEGORIES.get(cat_id, {})
        node = {
            "id": cat_id,
            "name": cat_info.get("name", cat_id),
            "weight": req["weight"],
            "min_score": req["min_score"],
            "critical_topics": req["critical_topics"],
            "sub_skills": cat_info.get("skills", []),
        }
        nodes.append(node)

    # Build prerequisite edges (DSA → coding, coding → system_design, etc.)
    edge_rules = {
        "dsa": ["coding", "system_design"],
        "coding": ["system_design"],
        "aptitude": ["behavioral"],
        "behavioral": ["resume"],
    }
    for source, targets in edge_rules.items():
        for target in targets:
            if any(n["id"] == source for n in nodes) and any(n["id"] == target for n in nodes):
                edges.append({"from": source, "to": target})

    return {
        "role": role,
        "nodes": nodes,
        "edges": edges,
        "total_weight": sum(n["weight"] for n in nodes),
    }


# ─── Personalized Gap Analysis ───
async def get_personalized_gaps(user_id: str, role_id: str = "sde") -> dict:
    """Compare user's current skills against role requirements. Returns gap analysis."""
    role = ROLE_PROFILES.get(role_id, ROLE_PROFILES["sde"])

    skill_graph = await skill_graph_collection.find_one({"user_id": user_id}) or {}
    categories = skill_graph.get("categories", {})

    gaps = []
    for cat_id, req in role["required_skills"].items():
        cat_data = categories.get(cat_id, {})
        current_score = cat_data.get("score", 0)
        target_score = req["min_score"]
        gap = max(0, target_score - current_score)
        gap_pct = round((gap / target_score * 100) if target_score > 0 else 0)

        status = "strong" if current_score >= target_score else ("close" if gap <= 15 else "critical")

        gaps.append({
            "category": cat_id,
            "name": SKILL_CATEGORIES.get(cat_id, {}).get("name", cat_id),
            "current": round(current_score, 1),
            "target": target_score,
            "gap": round(gap, 1),
            "gap_pct": gap_pct,
            "weight": req["weight"],
            "status": status,
            "critical_topics": req["critical_topics"],
        })

    gaps.sort(key=lambda g: g["weight"] * g["gap"], reverse=True)

    overall_readiness = sum(
        min(100, g["current"] / g["target"] * 100) * g["weight"]
        for g in gaps if g["target"] > 0
    )

    return {
        "role": role,
        "overall_readiness": round(overall_readiness, 1),
        "gaps": gaps,
        "critical_gaps": [g for g in gaps if g["status"] == "critical"],
        "close_gaps": [g for g in gaps if g["status"] == "close"],
        "strong_areas": [g for g in gaps if g["status"] == "strong"],
    }


# ─── Curriculum Builder ───
def build_curriculum(gaps: list, role: dict, mission_progress: dict = None) -> list:
    """Build a personalized curriculum from gaps. Returns ordered study plan."""
    curriculum = []
    progress = mission_progress or {}

    for gap in gaps:
        if gap["status"] == "strong":
            continue

        category = gap["category"]
        for topic in gap["critical_topics"]:
            mission_done = progress.get(topic, {}).get("overall", 0) >= 80
            curriculum.append({
                "topic": topic,
                "category": category,
                "priority": "high" if gap["status"] == "critical" else "medium",
                "estimated_minutes": 30 if gap["status"] == "critical" else 15,
                "mission_link": f"/mission/{topic}",
                "completed": mission_done,
            })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    curriculum.sort(key=lambda x: (priority_order.get(x["priority"], 2), -x["estimated_minutes"]))

    return curriculum


# ─── JD → Full Pipeline ───
async def analyze_jd_and_build_plan(user_id: str, jd_text: str) -> dict:
    """Complete pipeline: JD → skill extraction → gap analysis → curriculum."""
    jd_analysis = analyze_job_description(jd_text)
    matched_role = jd_analysis.get("matched_role", "sde")
    gaps_data = await get_personalized_gaps(user_id, matched_role)

    # Get mission progress
    mastery_doc = await skill_graph_collection.find_one({"user_id": user_id}) or {}
    mission_progress = {}
    for cat_id, cat_data in mastery_doc.get("categories", {}).items():
        for skill_id, skill_data in cat_data.get("skills", {}).items():
            mission_progress[skill_id] = {"overall": skill_data.get("score", 0)}

    curriculum = build_curriculum(gaps_data["gaps"], gaps_data["role"], mission_progress)

    # Calculate estimated weeks
    total_minutes = sum(c["estimated_minutes"] for c in curriculum if not c["completed"])
    hours_per_week = 10
    estimated_weeks = max(1, round(total_minutes / 60 / hours_per_week))

    return {
        "jd_analysis": jd_analysis,
        "role": gaps_data["role"],
        "readiness": gaps_data["overall_readiness"],
        "gaps": gaps_data["gaps"],
        "critical_gaps": gaps_data["critical_gaps"],
        "curriculum": curriculum,
        "curriculum_stats": {
            "total_topics": len(curriculum),
            "completed": sum(1 for c in curriculum if c["completed"]),
            "remaining": sum(1 for c in curriculum if not c["completed"]),
            "estimated_weeks": estimated_weeks,
            "estimated_minutes": total_minutes,
        },
    }
