"""Campaign service — the canonical source of truth for company battlefield state.

Reuses existing systems rather than creating duplicates:
- ``study_engine.get_today`` for the daily plan
- ``adaptive_learning.detect_weak_areas`` for weakness detection
- ``question_store`` for pattern question pools
- ``gamification`` for user state
- ``placement_engine`` for company profiles

Does NOT create a new question engine, a new mastery system, or a new
learning path system. It composes them.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import (
    users_collection,
    gamification_collection,
    question_answers_collection,
    solved_problems_collection,
    user_question_state_collection,
)
from app.services.study_engine import get_today as study_get_today
from app.services.adaptive_learning import detect_weak_areas, assess_user_skills
from app.services.gamification import get_gamification_profile
from app.services.placement_engine import PlacementEngine
from app.services.question_store import find as question_find
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# ---------------------------------------------------------------------------
# Canonical rounds for service-company placement prep
# ---------------------------------------------------------------------------
ROUNDS: List[Dict[str, Any]] = [
    {
        "id": "aptitude",
        "name": "Aptitude",
        "icon": "🔢",
        "description": "Quantitative, Reasoning, Verbal",
        "patterns": [
            {"id": "percentages", "name": "Percentages", "emoji": "📐"},
            {"id": "ratio-proportion", "name": "Ratio & Proportion", "emoji": "⚖️"},
            {"id": "averages", "name": "Averages", "emoji": "📊"},
            {"id": "profit-loss", "name": "Profit & Loss", "emoji": "💰"},
            {"id": "time-work", "name": "Time & Work", "emoji": "⏱️"},
            {"id": "blood-relations", "name": "Blood Relations", "emoji": "👨‍👩‍👧"},
            {"id": "directions", "name": "Directions", "emoji": "🧭"},
            {"id": "series", "name": "Series", "emoji": "🔗"},
            {"id": "sentence-correction", "name": "Sentence Correction", "emoji": "✍️"},
            {"id": "reading-comprehension", "name": "Reading Comprehension", "emoji": "📖"},
        ],
    },
    {
        "id": "coding",
        "name": "Coding",
        "icon": "💻",
        "description": "Output Tracing, Loops, Arrays, Strings",
        "patterns": [
            {"id": "output-tracing", "name": "Output Tracing", "emoji": "🔍"},
            {"id": "loops", "name": "Loops", "emoji": "🔄"},
            {"id": "arrays", "name": "Arrays", "emoji": "📋"},
            {"id": "strings", "name": "Strings", "emoji": "🔤"},
            {"id": "conditions", "name": "Conditions", "emoji": "🔀"},
            {"id": "functions", "name": "Functions", "emoji": "🧩"},
        ],
    },
    {
        "id": "cs-core",
        "name": "CS Core",
        "icon": "🗄️",
        "description": "OOP, DBMS, SQL, OS",
        "patterns": [
            {"id": "oop", "name": "OOP", "emoji": "🏗️"},
            {"id": "dbms", "name": "DBMS", "emoji": "🛢️"},
            {"id": "sql-joins", "name": "SQL JOINs", "emoji": "🔗"},
            {"id": "os", "name": "Operating Systems", "emoji": "⚙️"},
            {"id": "cn", "name": "Computer Networks", "emoji": "🌐"},
        ],
    },
    {
        "id": "technical-interview",
        "name": "Technical Interview",
        "icon": "🎤",
        "description": "Concepts, communication, problem-solving",
        "patterns": [
            {"id": "encapsulation", "name": "Encapsulation", "emoji": "🔒"},
            {"id": "inheritance", "name": "Inheritance", "emoji": "🧬"},
            {"id": "normalization", "name": "Normalization", "emoji": "📑"},
            {"id": "deadlock", "name": "Deadlock", "emoji": "🚧"},
            {"id": "tcp-ip", "name": "TCP/IP", "emoji": "📡"},
        ],
    },
    {
        "id": "hr-managerial",
        "name": "HR / Managerial",
        "icon": "🤝",
        "description": "Behavioral, situational, strengths",
        "patterns": [
            {"id": "introduction", "name": "Self Introduction", "emoji": "🙋"},
            {"id": "strengths-weaknesses", "name": "Strengths & Weaknesses", "emoji": "⚖️"},
            {"id": "situational", "name": "Situational Judgment", "emoji": "🎭"},
            {"id": "conflict-resolution", "name": "Conflict Resolution", "emoji": "🕊️"},
        ],
    },
]

# ---------------------------------------------------------------------------
# Topic-to-pattern mapping for question bank integration
# ---------------------------------------------------------------------------
TOPIC_TO_PATTERN_MAP: Dict[str, List[str]] = {
    "Quantitative Aptitude": [
        "percentages", "ratio-proportion", "averages", "profit-loss", "time-work"
    ],
    "Aptitude": [
        "percentages", "ratio-proportion", "averages", "profit-loss", "time-work",
        "blood-relations", "directions", "series", "sentence-correction", "reading-comprehension"
    ],
    "Logical Reasoning": [
        "blood-relations", "directions", "series", "syllogism"
    ],
    "Verbal Ability": [
        "sentence-correction", "reading-comprehension"
    ],
    "Programming": [
        "output-tracing", "loops", "arrays", "strings", "conditions", "functions",
        "oop", "dbms", "sql-joins", "os", "cn"
    ],
    "Arrays": ["arrays"],
    "Dynamic Programming": ["arrays"],
    "Strings": ["strings"],
    "Graphs": ["cn"],
    "Trees": ["oop"],
    "Stack": ["conditions"],
    "Linked Lists": ["arrays"],
    "Design": ["system-design"],
    "Array": ["arrays"],
    "Tree": ["oop"],
    "Matrix": ["arrays"],
    "Graph": ["cn"],
    "Hash Table": ["arrays"],
    "Sorting": ["arrays"],
    "Linked List": ["arrays"],
    "Math": ["percentages", "averages"],
    "Averages": ["averages"],
    "Time and Work": ["time-work"],
    "Time and Distance": ["directions", "time-work"],
    "Sliding Window": ["arrays"],
    "Bit Manipulation": ["conditions"],
    "Recursion & Backtracking": ["functions"],
    "Intervals": ["arrays"],
    "Backtracking": ["functions"],
    "Trie": ["strings"],
    "Permutation and Combination": ["series"],
    "BFS": ["cn"],
    "String": ["strings"],
    "Greedy": ["arrays"],
    "Stacks": ["conditions"],
    "Recursion": ["functions"],
}

# ---------------------------------------------------------------------------
# Campaign state helpers
# ---------------------------------------------------------------------------


async def get_campaign_state(user_id: str) -> Dict[str, Any]:
    """Get the user's current campaign target."""
    try:
        user = await users_collection.find_one({"user_id": user_id}) or {}
        return {
            "company": user.get("target_company", ""),
            "role": user.get("target_role", ""),
            "assessment_date": user.get("assessment_date", ""),
        }
    except Exception:
        return {"company": "", "role": "", "assessment_date": ""}


async def set_campaign_state(user_id: str, company: str, role: str, assessment_date: str) -> Dict[str, Any]:
    """Persist the user's campaign target."""
    now = datetime.now(timezone.utc)
    try:
        await users_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "target_company": company.lower().strip(),
                    "target_role": role.strip(),
                    "assessment_date": assessment_date,
                    "updated_at": now,
                }
            },
            upsert=True,
        )
    except Exception as exc:
        logger.warning("Failed to save campaign state for %s: %s", user_id, exc)
    return {"company": company, "role": role, "assessment_date": assessment_date}


# ---------------------------------------------------------------------------
# Pattern mastery computation
# ---------------------------------------------------------------------------


def _patterns_for_topic(topic: str) -> List[str]:
    """Map a question topic to pattern IDs."""
    return TOPIC_TO_PATTERN_MAP.get(topic, [])


async def _count_questions_for_pattern(pattern_id: str) -> int:
    """Count trusted questions for a pattern using topic mapping."""
    count = 0
    try:
        pool = question_find({"topic": pattern_id}).prefer_verified().to_list(50)
        count += len(pool)
    except Exception:
        pass
    for topic, patterns in TOPIC_TO_PATTERN_MAP.items():
        if pattern_id in patterns:
            try:
                pool = question_find({"topic": topic}).prefer_verified().to_list(50)
                count += len(pool)
            except Exception:
                pass
    return count


async def _get_pattern_mastery(user_id: str, pattern_id: str) -> Dict[str, Any]:
    """Compute mastery for a single pattern from diagnostic + practice history.

    Returns:
        mastery: 0-100
        attempts: total attempts
        accuracy: correct / attempts
        diagnosis: list of failure reasons
        last_practiced: ISO timestamp or None
    """
    attempts = 0
    correct = 0
    diagnosis: List[str] = []
    last_practiced: Optional[str] = None

    try:
        # Question answers for this pattern/topic
        mapped_topics = [pattern_id] + [
            topic for topic, patterns in TOPIC_TO_PATTERN_MAP.items()
            if pattern_id in patterns
        ]
        cursor = question_answers_collection.find(
            {"user_id": user_id, "topic": {"$in": mapped_topics}}
        ).sort("created_at", -1).limit(50)
        async for doc in cursor:
            attempts += 1
            if doc.get("is_correct"):
                correct += 1
            else:
                reason = doc.get("diagnosis_code") or doc.get("error_type") or "incorrect"
                if reason not in diagnosis:
                    diagnosis.append(reason)
            if last_practiced is None:
                last_practiced = doc.get("created_at", {}).get("iso", "") if isinstance(doc.get("created_at"), dict) else str(doc.get("created_at", ""))

        # Solved problems tagged with this pattern
        cursor2 = solved_problems_collection.find(
            {"user_id": user_id, "topic": {"$in": mapped_topics}}
        ).sort("solved_at", -1).limit(20)
        async for doc in cursor2:
            attempts += 1
            if doc.get("passed"):
                correct += 1
            if last_practiced is None:
                last_practiced = doc.get("solved_at", {}).get("iso", "") if isinstance(doc.get("solved_at"), dict) else str(doc.get("solved_at", ""))
    except Exception as exc:
        logger.debug("Pattern mastery fetch failed for %s/%s: %s", user_id, pattern_id, exc)

    accuracy = round((correct / attempts) * 100, 1) if attempts > 0 else None
    mastery = round(accuracy, 1) if accuracy is not None else 0.0

    return {
        "mastery": mastery,
        "attempts": attempts,
        "accuracy": accuracy,
        "diagnosis": diagnosis[:3],
        "last_practiced": last_practiced,
    }


async def get_battlefield(user_id: str, company: str) -> Dict[str, Any]:
    """Build the full battlefield structure for a company.

    Returns rounds with patterns, each pattern having:
        - id, name, emoji
        - mastery: 0-100
        - attempts, accuracy
        - diagnosis: top failure reasons
        - question_count: available trusted questions
        - recommended: bool (is this the biggest weakness?)
    """
    # Get weak areas from adaptive learning
    try:
        weak_areas = await detect_weak_areas(user_id)
        weak_ids = {area.get("domain_id", "") for area in weak_areas}
        weak_scores = {area.get("domain_id", ""): area.get("score", 0) for area in weak_areas}
    except Exception:
        weak_ids = set()
        weak_scores = {}

    # Get diagnostic baseline if available
    try:
        user = await users_collection.find_one({"user_id": user_id}) or {}
        diagnostic = (((user.get("career_goal") or {}).get("diagnostic") or {})).get("baseline_categories", {})
    except Exception:
        diagnostic = {}

    rounds_out = []
    for round_ in ROUNDS:
        patterns_out = []
        for pattern in round_["patterns"]:
            pid = pattern["id"]
            mastery_info = await _get_pattern_mastery(user_id, pid)

            # Blend diagnostic + practice mastery
            diag_score = diagnostic.get(pid, diagnostic.get(pid.replace("-", "_"), None))
            if diag_score is not None:
                try:
                    diag_score = float(diag_score)
                    if mastery_info["attempts"] == 0:
                        mastery_info["mastery"] = round(diag_score, 1)
                        mastery_info["accuracy"] = round(diag_score, 1)
                except (TypeError, ValueError):
                    pass

            # Question count from trusted store (direct + mapped topics)
            q_count = await _count_questions_for_pattern(pid)

            # Is this the biggest weakness?
            is_weak = pid in weak_ids or (mastery_info["mastery"] < 40)
            is_lowest = False
            if not is_lowest:
                lowest_pid = min(weak_scores, key=weak_scores.get) if weak_scores else None
                is_lowest = pid == lowest_pid

            patterns_out.append({
                **pattern,
                **mastery_info,
                "question_count": q_count,
                "is_weak": is_weak,
                "is_lowest": is_lowest,
                "status": _mastery_status(mastery_info["mastery"]),
            })

        rounds_out.append({**round_, "patterns": patterns_out})

    # Identify the biggest weakness (lowest mastery across all patterns)
    all_patterns = [p for r in rounds_out for p in r["patterns"]]
    all_patterns_sorted = sorted(all_patterns, key=lambda p: p["mastery"])
    biggest_weakness = all_patterns_sorted[0] if all_patterns_sorted else None

    return {
        "company": company,
        "rounds": rounds_out,
        "biggest_weakness": biggest_weakness,
        "total_patterns": len(all_patterns),
        "mastered_patterns": sum(1 for p in all_patterns if p["mastery"] >= 70),
        "weak_patterns": sum(1 for p in all_patterns if p["mastery"] < 40),
    }


def _mastery_status(mastery: float) -> str:
    if mastery >= 80:
        return "mastered"
    if mastery >= 60:
        return "competent"
    if mastery >= 40:
        return "developing"
    if mastery > 0 or mastery == 0:
        return "weak"
    return "untouched"


# ---------------------------------------------------------------------------
# Today recommendations
# ---------------------------------------------------------------------------


async def get_today_recommendations(user_id: str, company: str) -> Dict[str, Any]:
    """Return the top 3 recommended actions for today with causal reasons.

    This replaces the generic daily plan with a company-battlefield-aware
    recommendation engine.
    """
    battlefield = await get_battlefield(user_id, company)
    g = await get_gamification_profile(user_id)
    streak = g.get("streak", 0)
    level = g.get("level", 1)

    # Get the canonical daily plan from study engine (for context)
    try:
        plan = await study_get_today(user_id, company=company)
    except Exception:
        plan = {}

    recommendations: List[Dict[str, Any]] = []
    total_minutes = 0

    # 1. Biggest weakness repair (highest priority)
    bw = battlefield.get("biggest_weakness")
    if bw and bw.get("mastery", 100) < 60:
        recommendations.append({
            "id": f"repair-{bw['id']}",
            "type": "repair",
            "priority": 1,
            "title": f"Fix {bw['name']}",
            "subtitle": f"{bw['mastery']}% mastery — {bw.get('diagnosis', ['needs practice'])[0] if bw.get('diagnosis') else 'needs practice'}",
            "emoji": bw.get("emoji", "🔧"),
            "estimated_minutes": 12,
            "pattern_id": bw["id"],
            "round_id": _pattern_to_round(bw["id"]),
            "reason": _repair_reason(bw),
            "action": "learn",
        })
        total_minutes += 12

    # 2. Next pattern to learn (from study engine's next mission)
    next_mission = plan.get("next")
    if next_mission and len(recommendations) < 3:
        topic = (next_mission.get("topic") or next_mission.get("skill") or "").lower()
        if topic:
            recommendations.append({
                "id": f"learn-{topic}",
                "type": "learn",
                "priority": 2,
                "title": next_mission.get("title", "Next Mission"),
                "subtitle": next_mission.get("reason") or "Continue your progression",
                "emoji": "📚",
                "estimated_minutes": next_mission.get("estimated_minutes") or 15,
                "pattern_id": topic,
                "round_id": _pattern_to_round(topic),
                "reason": "Builds on what you learned yesterday",
                "action": "learn",
            })
            total_minutes += next_mission.get("estimated_minutes") or 15

    # 3. Daily battle or timed prove
    daily_battle = plan.get("daily_battle", [])
    if daily_battle and len(recommendations) < 3:
        q = daily_battle[0]
        recommendations.append({
            "id": f"battle-{q.get('id', 'daily')}",
            "type": "battle",
            "priority": 3,
            "title": "Daily Battle",
            "subtitle": f"{q.get('topic', 'Mixed')} — timed questions",
            "emoji": "⚔️",
            "estimated_minutes": q.get("estimated_minutes") or 15,
            "pattern_id": q.get("topic", ""),
            "round_id": _pattern_to_round(q.get("topic", "")),
            "reason": "Prove your skills under time pressure",
            "action": "test",
        })
        total_minutes += q.get("estimated_minutes") or 15

    # Fallback: if fewer than 3, add practice/review
    if len(recommendations) < 3:
        reviews = plan.get("reviews", [])
        if reviews:
            r = reviews[0]
            recommendations.append({
                "id": f"review-{r.get('id', r.get('skill_id', 'srs'))}",
                "type": "review",
                "priority": len(recommendations) + 1,
                "title": r.get("title") or "SRS Review",
                "subtitle": "Spaced repetition review",
                "emoji": "🧠",
                "estimated_minutes": r.get("estimated_minutes") or 8,
                "pattern_id": r.get("skill_id", ""),
                "round_id": _pattern_to_round(r.get("skill_id", "")),
                "reason": "Keep what you learned from fading",
                "action": "practice",
            })
            total_minutes += r.get("estimated_minutes") or 8

    if len(recommendations) < 3:
        practice = plan.get("practice", [])
        if practice:
            p = practice[0]
            recommendations.append({
                "id": f"practice-{p.get('id', p.get('domain_id', 'weak'))}",
                "type": "practice",
                "priority": len(recommendations) + 1,
                "title": p.get("title") or "Weakness Practice",
                "subtitle": p.get("reason") or "Reinforce weak areas",
                "emoji": "🎯",
                "estimated_minutes": p.get("estimated_minutes") or 10,
                "pattern_id": p.get("domain_id") or p.get("skill", ""),
                "round_id": _pattern_to_round(p.get("domain_id") or p.get("skill", "")),
                "reason": "Targeted practice on your weak spots",
                "action": "practice",
            })
            total_minutes += p.get("estimated_minutes") or 10

    # Ensure we always have at least 1 recommendation
    if not recommendations:
        recommendations.append({
            "id": "diagnostic",
            "type": "diagnostic",
            "priority": 1,
            "title": "Take the Diagnostic",
            "subtitle": "Establish your baseline across all rounds",
            "emoji": "🧭",
            "estimated_minutes": 20,
            "pattern_id": None,
            "round_id": None,
            "reason": "We need a baseline to build your campaign",
            "action": "learn",
        })
        total_minutes += 20

    return {
        "company": company,
        "role": plan.get("target_role", ""),
        "assessment_date": plan.get("assessment_date", ""),
        "days_remaining": plan.get("days_remaining"),
        "streak": streak,
        "level": level,
        "overall_score": plan.get("overall_score", 0.0),
        "overall_mastery": plan.get("overall_mastery", "untouched"),
        "overall_mastery_label": plan.get("overall_mastery_label", "Not Started"),
        "recommendations": recommendations[:3],
        "totals": {
            "estimated_minutes": total_minutes,
            "task_count": len(recommendations[:3]),
        },
        "biggest_weakness": battlefield.get("biggest_weakness"),
        "battlefield_summary": {
            "total_patterns": battlefield.get("total_patterns", 0),
            "mastered_patterns": battlefield.get("mastered_patterns", 0),
            "weak_patterns": battlefield.get("weak_patterns", 0),
        },
    }


def _pattern_to_round(pattern_id: str) -> Optional[str]:
    """Map a pattern ID to its parent round ID."""
    for round_ in ROUNDS:
        for p in round_["patterns"]:
            if p["id"] == pattern_id:
                return round_["id"]
    return None


def _repair_reason(pattern: Dict[str, Any]) -> str:
    """Generate a human-readable reason for a repair recommendation."""
    diagnosis = pattern.get("diagnosis", [])
    mastery = pattern.get("mastery", 0)
    attempts = pattern.get("attempts", 0)

    if not attempts:
        return "Not attempted yet — start here"
    if mastery < 30:
        return f"Failed {attempts} attempts — {diagnosis[0] if diagnosis else 'fundamental gap'}"
    if mastery < 50:
        return f"Partial understanding — {diagnosis[0] if diagnosis else 'needs reinforcement'}"
    return f"{mastery}% mastery — close the gap"


# ---------------------------------------------------------------------------
# Pattern detail
# ---------------------------------------------------------------------------


async def get_pattern_detail(user_id: str, pattern_id: str, company: str) -> Dict[str, Any]:
    """Get full detail for a pattern including available questions and missions."""
    mastery_info = await _get_pattern_mastery(user_id, pattern_id)
    round_id = _pattern_to_round(pattern_id)

    # Find pattern metadata
    pattern_meta = None
    for round_ in ROUNDS:
        for p in round_["patterns"]:
            if p["id"] == pattern_id:
                pattern_meta = {**p, "round_id": round_["id"], "round_name": round_["name"]}
                break
        if pattern_meta:
            break

    if not pattern_meta:
        pattern_meta = {"id": pattern_id, "name": pattern_id.replace("-", " ").title(), "emoji": "📌", "round_id": round_id, "round_name": round_id or "General"}

    # Question count from trusted store (direct + mapped topics)
    question_count = await _count_questions_for_pattern(pattern_id)

    # Mission slug mapping
    mission_slug = pattern_id
    mission_map = {
        "percentages": "percentages",
        "ratio-proportion": "ratio",
        "averages": "averages",
        "profit-loss": "profit-loss",
        "time-work": "time-work",
        "blood-relations": "blood-relations",
        "directions": "directions",
        "series": "series",
        "sentence-correction": "grammar",
        "reading-comprehension": "reading-comprehension",
        "output-tracing": "coding-decoding",
        "loops": "loops",
        "arrays": "arrays",
        "strings": "strings",
        "conditions": "conditions",
        "functions": "variables",
        "oop": "oop",
        "dbms": "dbms",
        "sql-joins": "sql-joins",
        "os": "dbms",
        "cn": "cs-fundamentals",
        "encapsulation": "oop",
        "inheritance": "oop",
        "normalization": "dbms",
        "deadlock": "os",
        "tcp-ip": "cn",
        "introduction": "interview",
        "strengths-weaknesses": "interview",
        "situational": "interview",
        "conflict-resolution": "interview",
    }
    mission_slug = mission_map.get(pattern_id, pattern_id)

    return {
        **pattern_meta,
        **mastery_info,
        "question_count": question_count,
        "mission_slug": mission_slug,
        "company": company,
        "status": _mastery_status(mastery_info["mastery"]),
        "why": _pattern_why(mastery_info),
        "pack": __import__("app.services.pattern_pack_service", fromlist=["get_pattern_pack"]).get_pattern_pack(pattern_id),
    }


def _pattern_why(mastery_info: Dict[str, Any]) -> str:
    """Generate the 'why you need this' explanation for a pattern."""
    mastery = mastery_info.get("mastery", 0)
    diagnosis = mastery_info.get("diagnosis", [])
    attempts = mastery_info.get("attempts", 0)

    if not attempts:
        return "Not practiced yet — this is your starting point"
    if mastery < 40:
        return f"You're struggling with this. {diagnosis[0] if diagnosis else 'Needs fundamental repair'}"
    if mastery < 70:
        return f"Partial mastery. {diagnosis[0] if diagnosis else 'Strengthen under time pressure'}"
    return "Solid foundation — test under timed conditions"


# ---------------------------------------------------------------------------
# Mission evidence recording
# ---------------------------------------------------------------------------


async def record_mission_evidence(
    user_id: str,
    pattern_id: str,
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """Record mission completion evidence and update mastery.

    Evidence shape::
        {
            "stages": [{"stageId": "visual", "passed": true}, ...],
            "finalPassed": true,
            "timeSpentSeconds": 120
        }
    """
    now = datetime.now(timezone.utc)

    # Calculate stage scores
    stages = evidence.get("stages", [])
    passed_stages = sum(1 for s in stages if s.get("passed"))
    total_stages = len(stages)
    stage_score = round((passed_stages / total_stages) * 100, 1) if total_stages > 0 else 0.0
    final_passed = evidence.get("finalPassed", False)

    # Store evidence in question_answers (as a learning event)
    try:
        await question_answers_collection.insert_one({
            "user_id": user_id,
            "topic": pattern_id,
            "is_correct": final_passed,
            "score": stage_score,
            "diagnosis_code": "mission_complete" if final_passed else "mission_incomplete",
            "created_at": now,
            "source": "mission_evidence",
            "evidence": {
                "stages": stages,
                "finalPassed": final_passed,
                "timeSpentSeconds": evidence.get("timeSpentSeconds", 0),
                "stageScore": stage_score,
            },
        })
    except Exception as exc:
        logger.debug("Mission evidence insert failed: %s", exc)

    # Update user_question_state for SRS
    try:
        await user_question_state_collection.update_one(
            {"user_id": user_id, "topic": pattern_id},
            {
                "$set": {
                    "last_attempted": now,
                    "last_score": stage_score,
                    "last_passed": final_passed,
                    "attempts": {"$inc": 1},
                },
                "$setOnInsert": {"user_id": user_id, "topic": pattern_id},
            },
            upsert=True,
        )
    except Exception as exc:
        logger.debug("Question state update failed: %s", exc)

    # Award diamonds via record_practice (the ONLY writer)
    try:
        from app.services.gamification import record_practice
        activity_score = 10.0 if final_passed else 5.0
        await record_practice(
            user_id=user_id,
            activity_type="question_bank",
            score=activity_score,
            metadata={"pattern_id": pattern_id, "stage_score": stage_score, "source": "mission"},
        )
    except Exception as exc:
        logger.debug("Diamond award failed: %s", exc)

    return {
        "success": True,
        "pattern_id": pattern_id,
        "stage_score": stage_score,
        "final_passed": final_passed,
        "mastery_update": round(stage_score, 1),
    }
