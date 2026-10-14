"""Company Prep Service — deep concept explanations + OA-style assessments.

Enhancements over existing company_prep:
  - Concept deep-dive with Captain Byte narration
  - Animation metadata for frontend visualizations
  - Most-asked topic extraction from blueprints + question bank
  - Randomized OA-style assessments with timer + score breakdown
  - Personalization via weak areas + company requirements
"""
from __future__ import annotations

import logging
import random
from typing import Any, Dict, List, Optional

from app.services import question_store
from app.services.adaptive_learning import detect_weak_areas
from app.services.gamification import record_practice

logger = logging.getLogger(__name__)


def get_company_blueprint(company_name: str) -> Optional[dict]:
    try:
        from app.data.company_blueprints import company_blueprints
        for key, bp in company_blueprints.get("company_blueprints", {}).items():
            if bp.get("name", "").lower() == company_name.lower():
                return bp
            if company_name.lower() in key.lower():
                return bp
    except Exception:
        pass
    return None


def list_company_tracks() -> List[Dict[str, Any]]:
    try:
        from app.data.learning_paths import COMPANY_TRACKS
        out = []
        for key, track in COMPANY_TRACKS.items():
            out.append({
                "id": key,
                "company_id": track.get("company_id", key),
                "name": track.get("name", key),
                "full_name": track.get("full_name", ""),
                "icon": track.get("icon", "🏢"),
                "color": track.get("color", "#3B82F6"),
                "role": track.get("role", ""),
                "package_range": track.get("package_range", {}),
                "duration_minutes": track.get("duration_minutes", 0),
                "difficulty": track.get("difficulty", "medium"),
                "description": track.get("description", ""),
                "total_sections": len(track.get("sections", [])),
                "total_modules": sum(len(s.get("modules", [])) for s in track.get("sections", [])),
            })
        return out
    except Exception:
        return []


def get_company_track(track_id: str) -> Optional[dict]:
    try:
        from app.data.learning_paths import COMPANY_TRACKS
        return COMPANY_TRACKS.get(track_id)
    except Exception:
        return None


def most_asked_topics(company: str, limit: int = 8) -> List[Dict[str, Any]]:
    topics: Dict[str, int] = {}
    try:
        qs = question_store.find({"companies": {"$in": [company]}}).prefer_verified().to_list()[:200]
        for q in qs:
            for tag in list(q.get("topics") or []) + list(q.get("tags") or []) + [q.get("topic", ""), q.get("sub_topic", "")]:
                if not tag:
                    continue
                tag = str(tag)
                topics[tag] = topics.get(tag, 0) + 1
    except Exception:
        pass
    ranked = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{"topic": t, "count": c} for t, c in ranked]


def get_most_asked_questions(company: str, frequency: str = "high", limit: int = 20) -> List[Dict[str, Any]]:
    """Return most/medium/least asked questions for a company.
    
    Uses frequency field if available, otherwise falls back to topic-based heuristics:
    - high: frequency >= 50 or topic matches company's most frequent topics
    - medium: 10 <= frequency < 50 or topic matches medium frequency topics
    - low: frequency < 10 and doesn't match high/medium topics
    """
    try:
        # Get all verified questions for this company
        pool = question_store.find({"companies": {"$in": [company]}}).prefer_verified().to_list()[:500]
        
        # Score questions by frequency
        freq_ranges = {
            "high": (50, 100),
            "medium": (10, 50),
            "low": (0, 10),
        }
        min_freq, max_freq = freq_ranges.get(frequency, (0, 100))
        
        # Filter and sort by frequency
        filtered = [q for q in pool if min_freq <= q.get("frequency", 0) < max_freq]
        
        # If not enough filtered questions, use topic-based heuristics
        if len(filtered) < limit:
            # Topic-based frequency mapping (from tag_question_frequency.py)
            topic_freq_map = {
                "tcs": {
                    "high": ["percentages", "profit and loss", "time and work", "time speed distance", "number series", "data interpretation", "seating arrangement", "syllogism", "coding decoding", "blood relations", "averages", "ratios", "verbal ability", "reasoning ability", "numerical ability"],
                    "medium": ["permutations and combinations", "probability", "geometry", "clocks", "direction sense", "data sufficiency", "compound interest", "simple interest"],
                },
                "infosys": {
                    "high": ["arrays", "strings", "dynamic programming", "linked lists", "trees", "recursion", "backtracking", "sorting", "searching", "hashing", "graphs", "stack", "queue"],
                    "medium": ["greedy", "binary search", "two pointers", "sliding window", "heap"],
                },
                "wipro": {
                    "high": ["time speed distance", "percentages", "profit and loss", "number series", "seating arrangement", "reading comprehension", "sentence correction", "blood relations", "arrays", "strings", "coding", "logical reasoning"],
                    "medium": ["clocks", "calendars", "data sufficiency", "direction sense", "syllogism"],
                },
            }
            
            company_topics = topic_freq_map.get(company.lower(), {})
            target_topics = company_topics.get(frequency, [])
            
            if target_topics and not filtered:
                # Fall back to topic matching
                topic_matched = []
                for q in pool:
                    topic = str(q.get("topic", "")).lower()
                    if any(t in topic for t in target_topics):
                        topic_matched.append(q)
                filtered = topic_matched
        
        # Final fallback: use all pool questions
        if not filtered:
            filtered = pool
        
        # Sort by frequency descending
        filtered.sort(key=lambda q: q.get("frequency", 0), reverse=True)
        return filtered[:limit]
    except Exception:
        return []


def concept_deep_dive(company: str, topic: str) -> Dict[str, Any]:
    bp = get_company_blueprint(company)
    matched_topic: Optional[Dict[str, Any]] = None
    if bp:
        structure = bp.get("structure", {})
        for stage in structure.values():
            if not isinstance(stage, dict):
                continue
            for item in stage.get("topics", {}).values() if isinstance(stage.get("topics"), dict) else []:
                if isinstance(item, dict) and item.get("name", "").lower() == topic.lower():
                    matched_topic = item
                    break
            if matched_topic:
                break
    return {
        "company": company,
        "topic": topic,
        "summary": matched_topic.get("summary") if matched_topic else f"{topic} concepts asked at {company}",
        "depth": matched_topic.get("depth") if matched_topic else "intermediate",
        "key_points": matched_topic.get("key_points") if matched_topic else [],
        "animations": matched_topic.get("animations") if matched_topic else [],
        "recommended_practice": matched_topic.get("recommended_practice") if matched_topic else [],
        "provenance": matched_topic.get("provenance") if matched_topic else "pattern-relevant",
    }


def start_oa_assessment(company: str, topic: Optional[str] = None, count: int = 10) -> Dict[str, Any]:
    pool: List[Dict[str, Any]] = []
    try:
        query: Dict[str, Any] = {"companies": {"$in": [company]}}
        if topic:
            query["$or"] = [
                {"topics": {"$in": [topic]}},
                {"tags": {"$in": [topic]}},
                {"topic": topic},
                {"sub_topic": topic},
            ]
        pool = question_store.find(query).prefer_verified().to_list()[:200]
    except Exception:
        pool = []
    if not pool:
        pool = question_store.find({}).prefer_verified().to_list()[:200]
    selected = random.sample(pool, min(count, len(pool))) if pool else []
    return {
        "company": company,
        "topic": topic,
        "assessment_id": f"oa:{company}:{topic or 'mixed'}:{random.randint(1000, 9999)}",
        "count": len(selected),
        "questions": selected,
        "rules": {
            "timer_minutes": max(15, len(selected) * 2),
            "allow_back": True,
            "show_result_after": True,
        },
    }


async def submit_oa_assessment(user_id: str, company: str, answers: Dict[str, Any], time_spent_seconds: int) -> Dict[str, Any]:
    questions = answers.get("questions", [])
    user_answers = answers.get("answers", {})
    correct = 0
    total = len(questions)
    for idx, q in enumerate(questions):
        expected = (q.get("expected_answer") or "").strip().lower()
        actual = str(user_answers.get(str(idx), "")).strip().lower()
        if expected and actual == expected:
            correct += 1
    score = round(correct / max(1, total) * 100, 1)
    weak = [q.get("topic") or q.get("sub_topic") for q in questions if str(user_answers.get(str(questions.index(q)), "")).strip().lower() != (q.get("expected_answer") or "").strip().lower()]
    try:
        await record_practice(user_id, "company_track", score / 10, {
            "action": "oa_assessment",
            "company": company,
            "score": score,
            "time_spent_seconds": time_spent_seconds,
        })
    except Exception:
        pass
    return {
        "company": company,
        "score": score,
        "correct": correct,
        "total": total,
        "time_spent_seconds": time_spent_seconds,
        "weak_topics": list(dict.fromkeys(weak))[:10],
        "next": "review weak topics + retake assessment",
    }
