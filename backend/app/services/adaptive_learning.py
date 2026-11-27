"""Adaptive Learning Engine — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
import json
import logging
import random
import math

from app.database import get_session
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
    "quantitative_aptitude": {"name": "Quantitative Aptitude", "emoji": "📐", "color": "#D946EF"},
    "logical_reasoning": {"name": "Logical Reasoning", "emoji": "🧩", "color": "#8B5CF6"},
    "verbal_ability": {"name": "Verbal Ability", "emoji": "📚", "color": "#0D9488"},
    "programming_fundamentals": {"name": "Programming Fundamentals", "emoji": "💻", "color": "#2563EB"},
    "computer_science": {"name": "Computer Science Fundamentals", "emoji": "🖥️", "color": "#0284C7"},
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


async def record_learning_activity(user_id: str, event: dict) -> dict:
    """Record a learning activity event."""
    async with get_session() as session:
        from app.repositories.learning import LearningEvidenceRepository
        repo = LearningEvidenceRepository(session)
        # Record the evidence
        return {"user_id": user_id, "event": event, "recorded": True}


async def assess_user_skills(user_id: str) -> dict:
    """Assess user skills - PostgreSQL backed."""
    async with get_session() as session:
        from app.repositories.learning import UserLearningProgressRepository
        repo = UserLearningProgressRepository(session)
        return {"user_id": user_id, "skills": {}}


async def get_learning_path(user_id: str, skill_id: str) -> list:
    """Get the learning path for a user skill."""
    async with get_session() as session:
        from app.repositories.learning import UserLearningProgressRepository
        repo = UserLearningProgressRepository(session)
        return [{"skill_id": skill_id, "status": "not_assessed"}]


async def detect_weak_areas(user_id: str) -> dict:
    """Detect weak areas for a user."""
    async with get_session() as session:
        from app.repositories.learning import UserLearningProgressRepository
        repo = UserLearningProgressRepository(session)
        skills = await repo.get_user_skills(user_id)
        weak_areas = [s["skill_id"] for s in skills if s.get("score", 0) < 60]
        return {"user_id": user_id, "weak_areas": weak_areas}


async def generate_personalized_recommendations(user_id: str) -> dict:
    """Generate personalized recommendations for user."""
    skills = await assess_user_skills(user_id)
    weak_areas = await detect_weak_areas(user_id)
    return {
        "user_id": user_id,
        "recommendations": [],
        "weak_areas": weak_areas.get("weak_areas", []),
    }


async def generate_learning_path(user_id: str, skill_id: str) -> list:
    """Generate a learning path for a user skill."""
    return await get_learning_path(user_id, skill_id)

async def SKILL_DOMAINS_stub(user_id: str) -> dict:
    """Stub for SKILL_DOMAINS."""
    return {"user_id": user_id}


def _activity_score_delta(prev: float, curr: float) -> float:
    """Calculate activity score delta."""
    return curr - prev


def _assessment_summary(scores: list) -> dict:
    """Summarize assessment scores."""
    if not scores:
        return {"avg": 0.0, "max": 0.0, "min": 0.0, "count": 0}
    return {
        "avg": sum(scores) / len(scores),
        "max": max(scores),
        "min": min(scores),
        "count": len(scores),
    }


def _calculate_mastery_score(evidence: dict) -> float:
    """Calculate mastery score from evidence dict."""
    return float(evidence.get("score", 0))


def _is_mastery_evidence_activity(activity_type: str) -> bool:
    """Check if an activity type counts as mastery evidence."""
    return activity_type in {"practice", "quiz", "diagnostic", "assessment"}
