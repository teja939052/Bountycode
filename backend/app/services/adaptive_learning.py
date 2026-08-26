"""
Adaptive Learning Engine — AI-powered personalized learning path.
Assesses skills, detects weak areas, generates daily plans, tracks mastery.
"""
import json
import logging
import random
import math
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from bson import ObjectId

from app.database import (
    users_collection, progress_collection, submissions_collection,
    solved_problems_collection, question_answers_collection,
    learning_progress_collection, skill_graph_collection,
    gamification_collection, curated_questions_collection
)
from app.services.ai_core import chat_completion, parse_json
from app.services.cache import cache

logger = logging.getLogger(__name__)

# ─── Skill taxonomy ───
SKILL_DOMAINS = {
    "arrays_hashing": {"name": "Arrays & Hashing", "emoji": "📊", "color": "#3B82F6"},
    "two_pointers": {"name": "Two Pointers", "emoji": "👆", "color": "#8B5CF6"},
    "sliding_window": {"name": "Sliding Window", "emoji": "🪟", "color": "#06B6D4"},
    "stack": {"name": "Stacks", "emoji": "📚", "color": "#F59E0B"},
    "binary_search": {"name": "Binary Search", "emoji": "🔍", "color": "#10B981"},
    "linked_list": {"name": "Linked Lists", "emoji": "⛓️", "color": "#EC4899"},
    "trees": {"name": "Trees", "emoji": "🌳", "color": "#22C55E"},
    "tries": {"name": "Tries", "emoji": "🔤", "color": "#6366F1"},
    "heap": {"name": "Heaps", "emoji": "⛰️", "color": "#F97316"},
    "graph": {"name": "Graphs", "emoji": "🕸️", "color": "#A855F7"},
    "dp": {"name": "Dynamic Programming", "emoji": "🧠", "color": "#EF4444"},
    "greedy": {"name": "Greedy", "emoji": "💰", "color": "#EAB308"},
    "backtracking": {"name": "Backtracking", "emoji": "↩️", "color": "#14B8A6"},
    "math_geometry": {"name": "Math & Geometry", "emoji": "📐", "color": "#7C3AED"},
    "bit_manipulation": {"name": "Bit Manipulation", "emoji": "🔢", "color": "#DB2777"},
    "system_design": {"name": "System Design", "emoji": "🏗️", "color": "#0EA5E9"},
    "behavioral": {"name": "Behavioral", "emoji": "💬", "color": "#84CC16"},
    "aptitude": {"name": "Aptitude", "emoji": "🧮", "color": "#D946EF"},
    "sql": {"name": "SQL & Databases", "emoji": "🗄️", "color": "#0284C7"},
    "language_c": {"name": "C Programming", "emoji": "⚙️", "color": "#64748B"},
    "language_cpp": {"name": "C++", "emoji": "🔷", "color": "#2563EB"},
    "language_java": {"name": "Java", "emoji": "☕", "color": "#EA580C"},
    "language_python": {"name": "Python", "emoji": "🐍", "color": "#16A34A"},
}

DIFFICULTY_ORDER = ["easy", "medium", "hard"]
DIFFICULTY_SCORE = {"easy": 1, "medium": 2, "hard": 3}

MASTERY_LEVELS = [
    {"id": "untouched", "label": "Not Started", "min_score": 0, "color": "#6B7280"},
    {"id": "beginner", "label": "Beginner", "min_score": 10, "color": "#EF4444"},
    {"id": "learning", "label": "Learning", "min_score": 30, "color": "#F59E0B"},
    {"id": "practicing", "label": "Practicing", "min_score": 50, "color": "#3B82F6"},
    {"id": "competent", "label": "Competent", "min_score": 70, "color": "#10B981"},
    {"id": "proficient", "label": "Proficient", "min_score": 85, "color": "#06B6D4"},
    {"id": "master", "label": "Mastered", "min_score": 95, "color": "#8B5CF6"},
]

# ─── Helpers ───

def _get_mastery_label(score: float) -> dict:
    for level in reversed(MASTERY_LEVELS):
        if score >= level["min_score"]:
            return level
    return MASTERY_LEVELS[0]

def _score_to_percent(correct: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round(correct / total * 100, 1)


# ─── Skill Assessment ───

async def assess_user_skills(user_id: str) -> Dict[str, Any]:
    """Comprehensive skill assessment across all domains."""
    cached = await cache.get("adaptive", f"skills:{user_id}")
    if cached:
        return json.loads(cached)

    # Gather data from all sources
    solved = await solved_problems_collection.find({"user_id": user_id}).to_list(1000)
    submissions = await submissions_collection.find({"user_id": user_id}).to_list(1000)
    answers = await question_answers_collection.find({"user_id": user_id}).to_list(500)
    learning = await learning_progress_collection.find({"user_id": user_id}).to_list(100)
    skill_graph = await skill_graph_collection.find_one({"user_id": user_id})

    # Build skill scores
    skills = {}
    for domain_id, domain_info in SKILL_DOMAINS.items():
        domain_solved = [s for s in solved if s.get("topic", "").lower().replace(" ", "_") == domain_id or s.get("domain", "") == domain_id]
        domain_submissions = [s for s in submissions if s.get("topic", "").lower().replace(" ", "_") == domain_id or s.get("domain", "") == domain_id]
        domain_answers = [a for a in answers if a.get("topic", "").lower().replace(" ", "_") == domain_id or a.get("domain", "") == domain_id]

        total_attempts = len(domain_solved) + len(domain_submissions) + len(domain_answers)
        correct_count = 0
        weighted_score = 0

        for s in domain_solved:
            if s.get("status") == "accepted" or s.get("passed", False):
                correct_count += 1
                diff = s.get("difficulty", "easy")
                weighted_score += DIFFICULTY_SCORE.get(diff, 1) * 20

        for s in domain_submissions:
            if s.get("passed", False):
                correct_count += 1
                diff = s.get("difficulty", "easy")
                weighted_score += DIFFICULTY_SCORE.get(diff, 1) * 15

        for a in domain_answers:
            if a.get("is_correct", False):
                correct_count += 1
                weighted_score += 10

        # Add learning progress
        domain_learning = [l for l in learning if l.get("language", "") == domain_id or l.get("domain", "") == domain_id]
        for l in domain_learning:
            completed = len(l.get("completed_lessons", []))
            weighted_score += completed * 5

        # Merge existing skill graph data
        existing_score = 0
        if skill_graph and domain_id in skill_graph.get("skills", {}):
            existing_score = skill_graph["skills"][domain_id].get("score", 0)

        # Combine scores (existing graph data + new evidence)
        if total_attempts > 0:
            accuracy = correct_count / total_attempts * 100
            new_score = min(100, weighted_score / max(1, total_attempts))
            combined = max(existing_score, new_score)
        else:
            combined = existing_score if existing_score > 0 else 0

        mastery = _get_mastery_label(combined)
        next_milestone = None
        for ml in MASTERY_LEVELS:
            if ml["min_score"] > combined:
                next_milestone = ml
                break

        skills[domain_id] = {
            "score": round(combined, 1),
            "mastery": mastery["id"],
            "mastery_label": mastery["label"],
            "mastery_color": mastery["color"],
            "total_attempts": total_attempts,
            "correct_count": correct_count,
            "accuracy": _score_to_percent(correct_count, max(1, total_attempts)),
            "next_milestone": {
                "label": next_milestone["label"] if next_milestone else "Max",
                "needed": next_milestone["min_score"] - combined if next_milestone else 0,
                "color": next_milestone["color"] if next_milestone else mastery["color"],
            } if next_milestone and next_milestone["min_score"] > combined else None,
        }

    # Overall stats
    overall_score = round(sum(s["score"] for s in skills.values()) / max(1, len(skills)), 1)
    total_solved = sum(s["total_attempts"] for s in skills.values())
    total_correct = sum(s["correct_count"] for s in skills.values())

    result = {
        "user_id": user_id,
        "overall_score": overall_score,
        "overall_mastery": _get_mastery_label(overall_score)["id"],
        "overall_mastery_label": _get_mastery_label(overall_score)["label"],
        "total_attempts": total_solved,
        "total_correct": total_correct,
        "overall_accuracy": _score_to_percent(total_correct, max(1, total_solved)),
        "skills": skills,
        "last_assessed": datetime.now(timezone.utc).isoformat(),
    }

    await cache.set("adaptive", f"skills:{user_id}", json.dumps(result), ttl=300)
    return result


async def detect_weak_areas(user_id: str, min_attempts: int = 2) -> List[Dict[str, Any]]:
    """Find weakest skill domains that need improvement."""
    assessment = await assess_user_skills(user_id)
    weak = []

    for domain_id, skill in assessment["skills"].items():
        domain_info = SKILL_DOMAINS.get(domain_id, {})
        is_weak = False
        reason = None

        if skill["mastery"] in ("untouched", "beginner"):
            if skill["total_attempts"] >= min_attempts:
                is_weak = True
                reason = f"Low accuracy ({skill['accuracy']}%) — needs focused practice"
            elif skill["total_attempts"] == 0:
                is_weak = True
                reason = "Not started yet — has high growth potential"
            else:
                is_weak = True
                reason = "Just beginning — consistent practice needed"

        elif skill["mastery"] == "learning":
            is_weak = True
            reason = f"In early stages ({skill['score']}/100) — more repetition needed"

        if is_weak:
            weak.append({
                "domain_id": domain_id,
                "name": domain_info.get("name", domain_id),
                "emoji": domain_info.get("emoji", "📌"),
                "color": domain_info.get("color", "#6B7280"),
                "score": skill["score"],
                "mastery": skill["mastery"],
                "mastery_label": skill["mastery_label"],
                "accuracy": skill["accuracy"],
                "total_attempts": skill["total_attempts"],
                "reason": reason,
                "priority": _calculate_priority(domain_id, skill),
            })

    weak.sort(key=lambda x: (x["priority"], x["score"]))
    return weak


def _calculate_priority(domain_id: str, skill: dict) -> int:
    """Higher priority = more urgent to address."""
    priority = 0
    if skill["mastery"] == "untouched":
        priority = 5
    elif skill["mastery"] == "beginner":
        priority = 4
    elif skill["mastery"] == "learning":
        priority = 3

    # Bonus priority for foundational domains
    foundational = ["arrays_hashing", "language_python", "language_java"]
    if domain_id in foundational:
        priority += 2

    # Bonus for high-growth domains (many low-accuracy attempts)
    if skill["total_attempts"] >= 5 and skill["accuracy"] < 40:
        priority += 3

    return priority


# ─── Daily Learning Plan ───

async def generate_daily_plan(user_id: str, force_refresh: bool = False) -> Dict[str, Any]:
    """Generate a personalized daily learning plan."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cache_key = f"daily_plan:{user_id}:{today}"

    if not force_refresh:
        cached = await cache.get("adaptive", cache_key)
        if cached:
            return json.loads(cached)

    weak_areas = await detect_weak_areas(user_id)
    assessment = await assess_user_skills(user_id)
    gamification = await gamification_collection.find_one({"user_id": user_id})
    streak = gamification.get("streak", 0) if gamification else 0
    level = gamification.get("level", 1) if gamification else 1

    plan = {
        "user_id": user_id,
        "date": today,
        "streak": streak,
        "level": level,
        "overall_score": assessment["overall_score"],
        "overall_mastery_label": assessment["overall_mastery_label"],
    }

    # Pick today's focus areas (up to 3)
    focus = weak_areas[:3]
    plan["focus_areas"] = []
    plan["tasks"] = []
    total_estimated_minutes = 0

    for area in focus:
        domain_info = SKILL_DOMAINS.get(area["domain_id"], {})
        task = _create_learning_task(area, domain_info, user_id)
        if task:
            plan["focus_areas"].append({
                "domain_id": area["domain_id"],
                "name": area["name"],
                "emoji": area["emoji"],
                "color": area["color"],
                "score": area["score"],
                "mastery_label": area["mastery_label"],
                "reason": area["reason"],
            })
            plan["tasks"].append(task)
            total_estimated_minutes += task.get("estimated_minutes", 15)

    # If no weak areas, suggest advanced practice
    if not plan["tasks"]:
        plan["message"] = "Great job! You're ahead in all areas. Here's some advanced practice."
        top_skills = sorted(assessment["skills"].items(), key=lambda x: x[1]["score"], reverse=True)[:2]
        for domain_id, skill in top_skills:
            domain_info = SKILL_DOMAINS.get(domain_id, {})
            task = {
                "id": f"advanced_{domain_id}_{today}",
                "type": "advanced_challenge",
                "domain_id": domain_id,
                "title": f"Advanced: {domain_info.get('name', domain_id)}",
                "emoji": domain_info.get("emoji", "🏆"),
                "color": domain_info.get("color", "#8B5CF6"),
                "description": f"Master-level challenge in {domain_info.get('name', domain_id)}",
                "difficulty": "hard",
                "estimated_minutes": 30,
                "xp_reward": 50,
                "hint": "Focus on optimization and edge cases",
            }
            plan["tasks"].append(task)
            plan["focus_areas"].append({
                "domain_id": domain_id,
                "name": domain_info.get("name", domain_id),
                "emoji": domain_info.get("emoji", "🏆"),
                "color": domain_info.get("color", "#8B5CF6"),
                "score": skill["score"],
                "mastery_label": "Advanced",
                "reason": "Push beyond mastery",
            })
            total_estimated_minutes += 30

    # Add a warm-up task (easy, quick)
    warm_up = _create_warmup(user_id, assessment)
    if warm_up:
        plan["tasks"].insert(0, warm_up)
        total_estimated_minutes += warm_up.get("estimated_minutes", 5)

    plan["total_estimated_minutes"] = total_estimated_minutes
    plan["task_count"] = len(plan["tasks"])

    await cache.set("adaptive", cache_key, json.dumps(plan), ttl=3600)
    return plan


def _create_learning_task(area: dict, domain_info: dict, user_id: str) -> Optional[Dict]:
    """Create a specific learning task for a weak area."""
    tasks_by_mastery = {
        "untouched": [
            {"type": "lesson", "title": f"Learn {domain_info.get('name', area['domain_id'])} Basics", "difficulty": "easy", "estimated_minutes": 15, "xp_reward": 20},
            {"type": "video", "title": f"Watch: {domain_info.get('name', area['domain_id'])} Intro", "difficulty": "easy", "estimated_minutes": 10, "xp_reward": 10},
        ],
        "beginner": [
            {"type": "practice", "title": f"Practice: {domain_info.get('name', area['domain_id'])} Fundamentals", "difficulty": "easy", "estimated_minutes": 20, "xp_reward": 25},
            {"type": "problem", "title": f"Solve: Easy {domain_info.get('name', area['domain_id'])} Problem", "difficulty": "easy", "estimated_minutes": 25, "xp_reward": 30},
        ],
        "learning": [
            {"type": "problem", "title": f"Solve: Medium {domain_info.get('name', area['domain_id'])} Problem", "difficulty": "medium", "estimated_minutes": 30, "xp_reward": 40},
            {"type": "challenge", "title": f"Challenge: {domain_info.get('name', area['domain_id'])} Sprint", "difficulty": "medium", "estimated_minutes": 20, "xp_reward": 35},
        ],
        "practicing": [
            {"type": "problem", "title": f"Solve: Hard {domain_info.get('name', area['domain_id'])} Problem", "difficulty": "hard", "estimated_minutes": 40, "xp_reward": 50},
            {"type": "project", "title": f"Build: {domain_info.get('name', area['domain_id'])} Mini-Project", "difficulty": "hard", "estimated_minutes": 45, "xp_reward": 60},
        ],
    }

    tasks = tasks_by_mastery.get(area["mastery"], tasks_by_mastery["learning"])
    chosen = random.choice(tasks) if tasks else None
    if not chosen:
        return None

    return {
        "id": f"{area['domain_id']}_{area['mastery']}_{random.randint(1000, 9999)}",
        "domain_id": area["domain_id"],
        "emoji": domain_info.get("emoji", "📌"),
        "color": domain_info.get("color", "#6B7280"),
        "description": None,
        "hint": None,
        **chosen,
    }


def _create_warmup(user_id: str, assessment: dict) -> Optional[Dict]:
    """Create a quick warm-up task."""
    # Pick a domain the user has some familiarity with
    practiced_skills = [(d, s) for d, s in assessment["skills"].items() if s["score"] > 20 and s["score"] < 80]
    if not practiced_skills:
        return None

    domain_id, skill = random.choice(practiced_skills)
    domain_info = SKILL_DOMAINS.get(domain_id, {})
    return {
        "id": f"warmup_{domain_id}_{random.randint(1000, 9999)}",
        "type": "warmup",
        "domain_id": domain_id,
        "title": f"Warm-up: Quick {domain_info.get('name', domain_id)} Review",
        "emoji": "🔥",
        "color": "#F59E0B",
        "description": f"A quick {domain_info.get('name', domain_id)} refresher to start your session",
        "difficulty": "easy",
        "estimated_minutes": 5,
        "xp_reward": 10,
    }


# ─── Progress Tracking ───

async def record_learning_activity(user_id: str, activity: Dict[str, Any]) -> Dict[str, Any]:
    """Record a learning activity and update skill scores."""
    domain_id = activity.get("domain_id")
    if not domain_id:
        return {"status": "error", "message": "domain_id required"}

    activity_type = activity.get("type", "practice")
    success = activity.get("success", True)
    score_impact = activity.get("score_impact", 1)

    # Update learning_progress
    progress_doc = await learning_progress_collection.find_one({"user_id": user_id})
    if not progress_doc:
        progress_doc = {
            "user_id": user_id,
            "activities": [],
            "daily_logs": {},
            "skill_delta": {},
            "created_at": datetime.now(timezone.utc),
        }
        await learning_progress_collection.insert_one(progress_doc)

    # Add activity
    activity_entry = {
        "domain_id": domain_id,
        "type": activity_type,
        "success": success,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    await learning_progress_collection.update_one(
        {"user_id": user_id},
        {"$push": {"activities": activity_entry}}
    )

    # Update skill_graph
    delta = 5 if success else 1
    if activity_type == "challenge" or activity_type == "project":
        delta = 8 if success else 2

    await skill_graph_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {f"skills.{domain_id}.score": delta},
            "$set": {f"skills.{domain_id}.last_activity": datetime.now(timezone.utc).isoformat()},
        },
        upsert=True
    )

    # Invalidate cache
    await cache.delete("adaptive", f"skills:{user_id}")

    return {
        "status": "success",
        "score_delta": delta,
        "domain_id": domain_id,
    }


# ─── AI-Powered Recommendations ───

async def generate_personalized_recommendations(user_id: str) -> Dict[str, Any]:
    """Use AI to generate personalized learning recommendations."""
    assessment = await assess_user_skills(user_id)
    weak_areas = await detect_weak_areas(user_id)
    plan = await generate_daily_plan(user_id)

    prompt = f"""You are an AI career coach for PlacementPro. Based on this user's skill data, generate 3 personalized recommendations.

User's overall score: {assessment['overall_score']}/100
Mastery level: {assessment['overall_mastery_label']}

Weak areas (top 3):
{json.dumps([{'name': w['name'], 'score': w['score'], 'reason': w['reason']} for w in weak_areas[:3]], indent=2)}

All skills:
{json.dumps({d: {'score': s['score'], 'mastery': s['mastery_label']} for d, s in assessment['skills'].items() if s['score'] > 0}, indent=2)}

Respond with JSON:
{{
  "recommendations": [
    {{
      "title": "Short actionable title",
      "description": "Why this matters and what to do",
      "domain": "skill_domain_id",
      "impact": "high/medium/low",
      "estimated_hours": 2,
      "type": "practice/learn/build/review",
      "concrete_action": "Specific next step"
    }}
  ],
  "career_insight": "1-2 sentence insight about their progress trajectory",
  "next_milestone": "What to aim for next"
}}"""

    try:
        messages = [
            {"role": "system", "content": "You are an AI career coach. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        ai_response = await chat_completion(messages, use_cache=True)
        result = parse_json(ai_response)
        if not result or "recommendations" not in result:
            raise ValueError("Invalid AI response")
    except Exception as e:
        logger.warning(f"AI recommendations failed, using fallback: {e}")
        result = _fallback_recommendations(assessment, weak_areas)

    result["assessment"] = {
        "overall_score": assessment["overall_score"],
        "overall_mastery_label": assessment["overall_mastery_label"],
        "weak_count": len(weak_areas),
    }
    result["daily_plan"] = {
        "tasks": plan.get("tasks", []),
        "total_minutes": plan.get("total_estimated_minutes", 0),
    }
    return result


def _fallback_recommendations(assessment: dict, weak_areas: list) -> dict:
    """Fallback when AI is unavailable."""
    recs = []
    for area in weak_areas[:2]:
        recs.append({
            "title": f"Master {area['name']}",
            "description": f"Your {area['name']} score is {area['score']}/100. Focus on fundamentals and practice problems.",
            "domain": area["domain_id"],
            "impact": "high",
            "estimated_hours": 3,
            "type": "practice",
            "concrete_action": f"Solve 5 {area['name']} problems this week",
        })

    # Find a strength to leverage
    strengths = [(d, s) for d, s in assessment["skills"].items() if s["score"] >= 70]
    if strengths:
        d, s = strengths[0]
        domain_info = SKILL_DOMAINS.get(d, {})
        recs.append({
            "title": f"Deepen {domain_info.get('name', d)} Expertise",
            "description": f"You're strong in {domain_info.get('name', d)} ({s['score']}/100). Push further with advanced challenges.",
            "domain": d,
            "impact": "medium",
            "estimated_hours": 2,
            "type": "build",
            "concrete_action": f"Build a project using {domain_info.get('name', d)} concepts",
        })

    return {
        "recommendations": recs,
        "career_insight": "Consistent daily practice is the fastest path to interview readiness.",
        "next_milestone": "Reach 70+ in all core DSA domains",
    }


# ─── Learning Path Generation ───

async def generate_learning_path(user_id: str, target_company: Optional[str] = None) -> Dict[str, Any]:
    """Generate a structured multi-week learning path."""
    assessment = await assess_user_skills(user_id)
    weak_areas = await detect_weak_areas(user_id)

    # Determine focus areas by priority
    high_priority = [w for w in weak_areas if w["priority"] >= 4]
    medium_priority = [w for w in weak_areas if w["priority"] == 3]
    low_priority = [w for w in weak_areas if w["priority"] <= 2]

    weeks = []
    week_number = 1
    total_domains = set()

    # Week 1-2: High priority domains
    for area in high_priority[:3]:
        domain_info = SKILL_DOMAINS.get(area["domain_id"], {})
        weeks.append(_create_week_plan(week_number, area, domain_info, "Foundation"))
        total_domains.add(area["domain_id"])
        week_number += 1

    # Week 3-4: Medium priority
    for area in medium_priority[:3]:
        if area["domain_id"] not in total_domains:
            domain_info = SKILL_DOMAINS.get(area["domain_id"], {})
            weeks.append(_create_week_plan(week_number, area, domain_info, "Development"))
            total_domains.add(area["domain_id"])
            week_number += 1

    # Week 5-6: Low priority + integration
    remaining = [w for w in low_priority if w["domain_id"] not in total_domains][:4]
    for area in remaining:
        domain_info = SKILL_DOMAINS.get(area["domain_id"], {})
        weeks.append(_create_week_plan(week_number, area, domain_info, "Growth"))
        total_domains.add(area["domain_id"])
        week_number += 1

    # Final week: Integration & mock interviews
    weeks.append({
        "week": week_number,
        "title": "Integration & Mock Interviews",
        "phase": "Mastery",
        "focus": "All domains",
        "emoji": "🏆",
        "color": "#8B5CF6",
        "daily_plan": [
            "Day 1: Mixed topic review (2 easy + 1 medium problem)",
            "Day 2: Timed coding challenge (45 min)",
            "Day 3: Mock interview (system design)",
            "Day 4: Behavioral prep (STAR method)",
            "Day 5: Full-length mock interview",
            "Day 6: Review mistakes & weak areas",
            "Day 7: Rest & reflection",
        ],
        "goal": "Build interview stamina and confidence",
        "estimated_hours": 15,
    })

    total_weeks = len(weeks)
    total_hours = sum(w.get("estimated_hours", 10) for w in weeks)

    return {
        "user_id": user_id,
        "total_weeks": total_weeks,
        "total_hours": total_hours,
        "target_company": target_company,
        "current_level": assessment["overall_mastery_label"],
        "current_score": assessment["overall_score"],
        "weeks": weeks,
        "weak_areas_summary": [{"name": w["name"], "score": w["score"], "priority": w["priority"]} for w in weak_areas[:5]],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def _create_week_plan(week_num: int, area: dict, domain_info: dict, phase: str) -> dict:
    """Create a week-long plan for a specific domain."""
    return {
        "week": week_num,
        "title": f"{domain_info.get('name', area['domain_id'])} {phase}",
        "phase": phase,
        "focus": area["name"],
        "emoji": domain_info.get("emoji", "📌"),
        "color": domain_info.get("color", "#6B7280"),
        "domain_id": area["domain_id"],
        "current_score": area["score"],
        "target_score": min(100, area["score"] + 30),
        "daily_plan": [
            f"Day 1: Study {area['name']} fundamentals (concepts + examples)",
            f"Day 2: Solve 2 easy {area['name']} problems",
            f"Day 3: Solve 2 medium {area['name']} problems",
            f"Day 4: Review solutions & learn optimal approaches",
            f"Day 5: Solve 1 hard {area['name']} problem",
            f"Day 6: Practice sprint — 3 problems in 60 min",
            f"Day 7: Review week's progress & revise weak points",
        ],
        "goal": f"Bring {area['name']} from {area['score']}/100 to {min(100, area['score'] + 30)}/100",
        "estimated_hours": 10 + (area["priority"] * 2),
    }


# ─── Readiness Score ───

async def calculate_readiness_score(user_id: str, company: Optional[str] = None) -> Dict[str, Any]:
    """Calculate interview readiness score (0-100) with breakdown."""
    assessment = await assess_user_skills(user_id)
    weak_areas = await detect_weak_areas(user_id)

    # Base score from overall skill assessment
    base_score = assessment["overall_score"]

    # Penalty for untouched domains
    untouched = sum(1 for s in assessment["skills"].values() if s["mastery"] == "untouched")
    untouched_penalty = untouched * 5

    # Penalty for weak accuracy
    weak_accuracy = sum(1 for s in assessment["skills"].values() if 0 < s["accuracy"] < 30)
    accuracy_penalty = weak_accuracy * 3

    # Bonus for consistency
    strong_domains = sum(1 for s in assessment["skills"].values() if s["mastery"] in ("proficient", "master"))
    consistency_bonus = strong_domains * 3

    # Domain coverage
    total_domains = len(SKILL_DOMAINS)
    covered = sum(1 for s in assessment["skills"].values() if s["score"] > 0)
    coverage_pct = covered / total_domains * 100

    readiness = max(0, min(100, base_score - untouched_penalty - accuracy_penalty + consistency_bonus))

    category_scores = {}
    categories = {
        "dsa": ["arrays_hashing", "two_pointers", "sliding_window", "stack", "binary_search", "linked_list", "trees", "tries", "heap", "graph", "dp", "greedy", "backtracking"],
        "languages": ["language_c", "language_cpp", "language_java", "language_python"],
        "fundamentals": ["math_geometry", "bit_manipulation", "sql"],
        "soft_skills": ["system_design", "behavioral"],
        "aptitude": ["aptitude"],
    }

    for cat_id, domain_ids in categories.items():
        scores = [assessment["skills"].get(d, {}).get("score", 0) for d in domain_ids]
        valid = [s for s in scores if s > 0]
        category_scores[cat_id] = round(sum(valid) / max(1, len(valid)), 1) if valid else 0

    return {
        "user_id": user_id,
        "overall_readiness": round(readiness, 1),
        "readiness_level": _get_readiness_level(readiness),
        "base_score": round(base_score, 1),
        "untouched_penalty": untouched_penalty,
        "accuracy_penalty": accuracy_penalty,
        "consistency_bonus": consistency_bonus,
        "coverage_pct": round(coverage_pct, 1),
        "category_scores": category_scores,
        "weak_areas_count": len(weak_areas),
        "strong_domains_count": strong_domains,
        "company_specific": None,
    }


def _get_readiness_level(score: float) -> str:
    if score >= 90:
        return "Interview Ready"
    elif score >= 75:
        return "Almost There"
    elif score >= 60:
        return "Progressing"
    elif score >= 40:
        return "Building Foundation"
    else:
        return "Getting Started"
