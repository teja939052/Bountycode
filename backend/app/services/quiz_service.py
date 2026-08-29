"""
Interactive Quiz & Mock Interview System
========================================

Provides multiple modes of practice:
  - Practice: Free practice with full solutions and hints
  - Quiz: Timed multiple choice without hints
  - Mock Interview: Realistic interview simulation with timer and pressure
  - Speed Run: Race against time for XP
  - Learning Path: Adaptive progression through curriculum
  - Boss Battle: Challenge rounds with multiple questions
  - Code Golf: Shortest code wins

Each mode tracks:
  - Score, time, attempts
  - XP earned, badges unlocked
  - Streak progress
  - Weak areas for recommendation
"""
import json
import os
import random
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict


# =============================================================
# QUESTION LOADING & INDEXING
# =============================================================

QUESTION_FILES = [
    "app/content/questions/curated/curated.json",
    "app/content/questions/curated/learning_objects.json",
    "app/content/questions/curated/placement_questions.json",
]

_questions_cache = None
_questions_by_id = None
_questions_by_topic = None
_questions_by_difficulty = None
_questions_by_company = None


def _load_questions() -> List[Dict[str, Any]]:
    """Load all questions from JSON files into memory."""
    global _questions_cache, _questions_by_id, _questions_by_topic, _questions_by_difficulty, _questions_by_company
    if _questions_cache is not None:
        return _questions_cache

    all_questions = []
    for f in QUESTION_FILES:
        if not os.path.exists(f):
            continue
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
            if isinstance(data, list):
                all_questions.extend(data)
            elif isinstance(data, dict) and "questions" in data:
                all_questions.extend(data["questions"])
        except Exception as e:
            print(f"Error loading {f}: {e}")

    # Deduplicate by ID
    seen = set()
    unique = []
    for q in all_questions:
        qid = q.get("id", "")
        if qid and qid not in seen:
            seen.add(qid)
            unique.append(q)

    _questions_cache = unique
    _questions_by_id = {q["id"]: q for q in unique if q.get("id")}
    _questions_by_topic = defaultdict(list)
    _questions_by_difficulty = defaultdict(list)
    _questions_by_company = defaultdict(list)
    for q in unique:
        topic = q.get("topic", "")
        if topic:
            _questions_by_topic[topic].append(q)
        diff = q.get("difficulty", "medium")
        if diff:
            _questions_by_difficulty[diff].append(q)
        for company in (q.get("companies") or []):
            if company:
                _questions_by_company[company.lower()].append(q)

    return unique


def get_question_by_id(qid: str) -> Optional[Dict[str, Any]]:
    _load_questions()
    return _questions_by_id.get(qid)


def get_questions_by_topic(topic: str) -> List[Dict[str, Any]]:
    _load_questions()
    return _questions_by_topic.get(topic, [])


def get_questions_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    _load_questions()
    return _questions_by_difficulty.get(difficulty, [])


def get_questions_by_company(company: str) -> List[Dict[str, Any]]:
    _load_questions()
    return _questions_by_company.get(company.lower(), [])


def get_all_questions() -> List[Dict[str, Any]]:
    return _load_questions()


def get_question_stats() -> Dict[str, Any]:
    """Get overall question bank statistics."""
    questions = _load_questions()
    if not questions:
        return {"total": 0}

    by_diff = defaultdict(int)
    by_topic = defaultdict(int)
    by_pattern = defaultdict(int)
    by_company = defaultdict(int)

    for q in questions:
        diff = q.get("difficulty", "medium")
        by_diff[diff] += 1
        topic = q.get("topic", "Other")
        by_topic[topic] += 1
        pattern = q.get("pattern", "general")
        by_pattern[pattern] += 1
        for company in (q.get("companies") or []):
            by_company[company] += 1

    def has_solution(q):
        sol = q.get("solution")
        if isinstance(sol, dict):
            return bool(sol.get("code"))
        return bool(sol)

    def has_hints(q):
        hints = q.get("hints", [])
        if not hints:
            return False
        # Count only if at least 3 hints
        return len(hints) >= 3

    return {
        "total": len(questions),
        "by_difficulty": dict(by_diff),
        "by_topic": dict(sorted(by_topic.items(), key=lambda x: -x[1])),
        "by_pattern": dict(by_pattern),
        "by_company": dict(sorted(by_company.items(), key=lambda x: -x[1])[:20]),
        "with_hints": sum(1 for q in questions if has_hints(q)),
        "with_solutions": sum(1 for q in questions if has_solution(q)),
        "with_real_world": sum(1 for q in questions if q.get("real_world_use") or q.get("real_world_context")),
        "enriched": sum(1 for q in questions if q.get("why_this_matters")),
    }


# =============================================================
# QUIZ MODES
# =============================================================

def build_quiz(
    mode: str = "practice",  # practice, quiz, mock_interview, speed_run, boss_battle
    topics: Optional[List[str]] = None,
    difficulty: Optional[str] = None,
    company: Optional[str] = None,
    num_questions: int = 5,
    time_limit_seconds: int = 0,
    randomize: bool = True,
    user_level: int = 1,
) -> Dict[str, Any]:
    """Build a quiz session based on mode and filters."""
    questions = _load_questions()

    # Filter
    filtered = questions
    if topics:
        filtered = [q for q in filtered if q.get("topic") in topics]
    if difficulty:
        filtered = [q for q in filtered if q.get("difficulty") == difficulty]
    if company:
        filtered = [q for q in filtered if company.lower() in [c.lower() for c in (q.get("companies") or [])]]

    if not filtered:
        filtered = questions

    # Mode-specific selection
    if mode == "mock_interview":
        # Mix difficulties: 1 easy, 2 medium, 2 hard
        by_diff = defaultdict(list)
        for q in filtered:
            by_diff[q.get("difficulty", "medium")].append(q)
        selected = (
            random.sample(by_diff.get("easy", []), min(1, len(by_diff.get("easy", []))))
            + random.sample(by_diff.get("medium", []), min(2, len(by_diff.get("medium", []))))
            + random.sample(by_diff.get("hard", []), min(2, len(by_diff.get("hard", []))))
        )
        if randomize:
            random.shuffle(selected)
        time_limit = time_limit_seconds or 90 * 60  # 90 min default
    elif mode == "boss_battle":
        # Hard questions only
        hard_qs = [q for q in filtered if q.get("difficulty") == "hard"]
        if not hard_qs:
            hard_qs = [q for q in filtered if q.get("difficulty") == "medium"]
        selected = random.sample(hard_qs, min(num_questions, len(hard_qs)))
        time_limit = time_limit_seconds or 30 * 60
    elif mode == "speed_run":
        selected = random.sample(filtered, min(num_questions, len(filtered)))
        time_limit = time_limit_seconds or 10 * 60
    else:  # practice or quiz
        selected = random.sample(filtered, min(num_questions, len(filtered)))
        time_limit = time_limit_seconds

    # Build quiz session
    quiz_id = f"quiz_{int(time.time())}_{random.randint(1000, 9999)}"
    questions_data = []
    for i, q in enumerate(selected):
        # Mode determines what we expose
        if mode == "mock_interview":
            # Hide hints, solution
            q_data = {
                "id": q.get("id"),
                "title": q.get("title", "Problem"),
                "question": q.get("question", ""),
                "topic": q.get("topic", ""),
                "difficulty": q.get("difficulty", "medium"),
                "companies": q.get("companies", []),
                "test_cases": q.get("test_cases", []),
                "xp_reward": q.get("xp_reward", 10),
            }
        elif mode == "speed_run":
            # Show only question and difficulty
            q_data = {
                "id": q.get("id"),
                "title": q.get("title", "Problem"),
                "question": q.get("question", ""),
                "topic": q.get("topic", ""),
                "difficulty": q.get("difficulty", "medium"),
                "xp_reward": q.get("xp_reward", 10) * 2,  # Bonus XP
            }
        else:  # practice or quiz
            q_data = {
                "id": q.get("id"),
                "title": q.get("title", "Problem"),
                "question": q.get("question", ""),
                "topic": q.get("topic", ""),
                "sub_topic": q.get("sub_topic", ""),
                "difficulty": q.get("difficulty", "medium"),
                "pattern": q.get("pattern", ""),
                "companies": q.get("companies", []),
                "hints": q.get("hints", []) if mode == "practice" else [],
                "test_cases": q.get("test_cases", []),
                "why_this_matters": q.get("why_this_matters", "") if mode == "practice" else "",
                "real_world_use": q.get("real_world_use", "") if mode == "practice" else "",
                "pattern_recognition": q.get("pattern_recognition", "") if mode == "practice" else "",
                "anti_patterns": q.get("anti_patterns", "") if mode == "practice" else "",
                "common_mistakes": q.get("common_mistakes", "") if mode == "practice" else "",
                "prerequisite_concepts": q.get("prerequisite_concepts", []),
                "solution": q.get("solution", {}) if mode == "practice" else {},
                "explanation": q.get("explanation", "") if mode == "practice" else "",
                "estimated_time": q.get("estimated_time", "15-25 minutes"),
                "xp_reward": q.get("xp_reward", 10),
            }
        q_data["index"] = i
        questions_data.append(q_data)

    return {
        "quiz_id": quiz_id,
        "mode": mode,
        "total_questions": len(questions_data),
        "time_limit_seconds": time_limit,
        "questions": questions_data,
        "filters": {
            "topics": topics,
            "difficulty": difficulty,
            "company": company,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "user_level": user_level,
    }


def submit_quiz_answer(
    quiz_id: str,
    question_id: str,
    user_answer: str,
    time_taken_seconds: float,
    hints_used: int = 0,
) -> Dict[str, Any]:
    """Evaluate a submitted answer and return feedback + XP."""
    question = get_question_by_id(question_id)
    if not question:
        return {"error": "Question not found"}

    # Determine if answer is correct (for coding, this is more about test cases)
    # In this system, we use a self-evaluation approach
    correct_answer = (question.get("correct_answer") or "").strip()
    is_correct = False
    if correct_answer:
        is_correct = user_answer.strip() == correct_answer
    else:
        # For coding problems, we trust the user's self-evaluation
        is_correct = user_answer.strip().lower() in ["true", "1", "yes", "solved"]

    # Calculate XP
    base_xp = question.get("xp_reward", 10)
    xp_earned = 0
    if is_correct:
        xp_earned = base_xp
        # Time bonus (faster = more XP)
        if time_taken_seconds < 300:  # < 5 min
            xp_earned = int(xp_earned * 1.5)
        elif time_taken_seconds < 600:  # < 10 min
            xp_earned = int(xp_earned * 1.2)
        # Hint penalty
        xp_earned -= hints_used * 2
        xp_earned = max(xp_earned, 1)

    # Get full solution
    solution = question.get("solution", {})

    return {
        "question_id": question_id,
        "is_correct": is_correct,
        "xp_earned": xp_earned,
        "time_taken_seconds": time_taken_seconds,
        "hints_used": hints_used,
        "correct_answer": correct_answer,
        "solution": solution,
        "explanation": question.get("explanation", ""),
        "why_this_matters": question.get("why_this_matters", ""),
        "real_world_use": question.get("real_world_use", ""),
        "common_mistakes": question.get("common_mistakes", ""),
        "follow_up": question.get("follow_up", ""),
        "related_concepts": question.get("related_concepts", []),
        "similar_problems": question.get("similar_problems", []),
    }


def get_hint_for_question(
    question_id: str, hint_level: int = 1, hints_already_used: int = 0
) -> Dict[str, Any]:
    """Get a progressive hint for a question."""
    question = get_question_by_id(question_id)
    if not question:
        return {"error": "Question not found"}

    hints = question.get("hints", [])
    if hint_level > len(hints):
        return {"error": "No more hints available", "hints_used": hints_already_used}

    hint = hints[hint_level - 1]
    if isinstance(hint, dict):
        return {
            "hint": hint,
            "hint_level": hint_level,
            "hints_used": hints_already_used + 1,
            "next_hint_available": hint_level < len(hints),
        }
    else:
        return {
            "hint": {"level": hint_level, "type": "general", "text": str(hint)},
            "hint_level": hint_level,
            "hints_used": hints_already_used + 1,
            "next_hint_available": hint_level < len(hints),
        }


# =============================================================
# ADAPTIVE LEARNING PATH
# =============================================================

def build_learning_path(
    role_id: str = "sde",
    target_level: str = "advanced",
    user_weak_topics: Optional[List[str]] = None,
    num_questions: int = 10,
) -> Dict[str, Any]:
    """Build an adaptive learning path based on user level and weak areas."""
    questions = _load_questions()

    # Role-based topic priorities
    role_topics = {
        "sde": ["Arrays & Hashing", "Two Pointers", "Trees", "Dynamic Programming", "Graphs", "Linked List"],
        "data-analyst": ["SQL", "Statistics", "Python", "Probability"],
        "ai-engineer": ["Deep Learning", "Machine Learning", "NLP", "Python", "Statistics"],
        "java-engineer": ["Core Java", "Spring", "Multithreading", "Design Patterns"],
    }

    target_topics = role_topics.get(role_id, role_topics["sde"])
    if user_weak_topics:
        # Prioritize weak topics
        target_topics = user_weak_topics + [t for t in target_topics if t not in user_weak_topics]

    # Difficulty progression
    level_to_difficulty = {
        "foundation": "easy",
        "core": "medium",
        "advanced": "hard",
    }
    target_difficulty = level_to_difficulty.get(target_level, "medium")

    # Select questions
    selected = []
    for topic in target_topics:
        topic_qs = [q for q in questions if q.get("topic") == topic]
        topic_qs = [q for q in topic_qs if q.get("difficulty") == target_difficulty]
        if topic_qs:
            selected.append(random.choice(topic_qs))
        if len(selected) >= num_questions:
            break

    # Fill with general questions if needed
    if len(selected) < num_questions:
        remaining = [q for q in questions if q not in selected and q.get("difficulty") == target_difficulty]
        selected.extend(random.sample(remaining, min(num_questions - len(selected), len(remaining))))

    return {
        "path_id": f"path_{int(time.time())}_{random.randint(1000, 9999)}",
        "role_id": role_id,
        "target_level": target_level,
        "target_difficulty": target_difficulty,
        "topics": target_topics[:num_questions],
        "weak_topics": user_weak_topics or [],
        "questions": [
            {
                "id": q.get("id"),
                "title": q.get("title"),
                "topic": q.get("topic"),
                "difficulty": q.get("difficulty"),
                "estimated_time": q.get("estimated_time", "15-25 minutes"),
            }
            for q in selected
        ],
        "estimated_total_time": f"{num_questions * 20}-{num_questions * 30} minutes",
    }


# =============================================================
# BOSS BATTLE & SPEED RUN
# =============================================================

def build_boss_battle(
    boss_level: int = 1,  # 1-10, higher = harder
    user_level: int = 1,
) -> Dict[str, Any]:
    """Build a boss battle session."""
    questions = _load_questions()

    # Boss level determines difficulty mix
    difficulty_mix = {
        1: {"easy": 3, "medium": 2, "hard": 0},
        2: {"easy": 2, "medium": 3, "hard": 0},
        3: {"easy": 1, "medium": 3, "hard": 1},
        4: {"easy": 1, "medium": 2, "hard": 2},
        5: {"easy": 0, "medium": 3, "hard": 2},
    }
    mix = difficulty_mix.get(min(boss_level, 5), difficulty_mix[5])

    selected = []
    for diff, count in mix.items():
        diff_qs = [q for q in questions if q.get("difficulty") == diff]
        selected.extend(random.sample(diff_qs, min(count, len(diff_qs))))

    random.shuffle(selected)

    return {
        "boss_battle_id": f"boss_{int(time.time())}_{random.randint(1000, 9999)}",
        "boss_level": boss_level,
        "user_level": user_level,
        "questions": [
            {
                "id": q.get("id"),
                "title": q.get("title"),
                "topic": q.get("topic"),
                "difficulty": q.get("difficulty"),
                "xp_reward": q.get("xp_reward", 10) * 2,
                "boss_multiplier": 2,
            }
            for q in selected
        ],
        "total_questions": len(selected),
        "time_limit_seconds": 60 * 60,  # 1 hour
        "rewards": {
            "xp_per_question": "2x base XP",
            "completion_bonus": 100,
            "perfect_run_bonus": 200,
        },
    }


# =============================================================
# RECOMMENDATION ENGINE
# =============================================================

def get_weak_topics(
    user_id: str = None,
    attempted_questions: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Analyze user's attempted questions and return weak topics."""
    if not attempted_questions:
        return []

    topic_stats = defaultdict(lambda: {"correct": 0, "total": 0, "avg_time": 0})
    for attempt in attempted_questions:
        topic = attempt.get("topic", "")
        if not topic:
            continue
        topic_stats[topic]["total"] += 1
        if attempt.get("is_correct"):
            topic_stats[topic]["correct"] += 1
        topic_stats[topic]["avg_time"] += attempt.get("time_taken", 0)

    weak = []
    for topic, stats in topic_stats.items():
        if stats["total"] >= 3:
            success_rate = stats["correct"] / stats["total"]
            avg_time = stats["avg_time"] / stats["total"]
            if success_rate < 0.6:
                weak.append({
                    "topic": topic,
                    "success_rate": round(success_rate, 2),
                    "questions_attempted": stats["total"],
                    "avg_time_seconds": round(avg_time, 1),
                    "recommended_difficulty": "easy" if success_rate < 0.4 else "medium",
                })

    return sorted(weak, key=lambda x: x["success_rate"])


# =============================================================
# QUIZ ANALYTICS
# =============================================================

def calculate_quiz_results(
    quiz_id: str,
    questions: List[Dict[str, Any]],
    answers: List[Dict[str, Any]],
    total_time_seconds: float,
) -> Dict[str, Any]:
    """Calculate comprehensive quiz results."""
    total = len(questions)
    correct = sum(1 for a in answers if a.get("is_correct"))
    total_xp = sum(a.get("xp_earned", 0) for a in answers)
    total_hints = sum(a.get("hints_used", 0) for a in answers)

    # Topic-wise breakdown
    topic_stats = defaultdict(lambda: {"correct": 0, "total": 0, "xp": 0})
    for i, q in enumerate(questions):
        if i < len(answers):
            ans = answers[i]
            topic = q.get("topic", "Other")
            topic_stats[topic]["total"] += 1
            if ans.get("is_correct"):
                topic_stats[topic]["correct"] += 1
            topic_stats[topic]["xp"] += ans.get("xp_earned", 0)

    # Difficulty-wise
    diff_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    for i, q in enumerate(questions):
        if i < len(answers):
            ans = answers[i]
            diff = q.get("difficulty", "medium")
            diff_stats[diff]["total"] += 1
            if ans.get("is_correct"):
                diff_stats[diff]["correct"] += 1

    # Identify weak areas
    weak_areas = []
    for topic, stats in topic_stats.items():
        if stats["total"] >= 2:
            success_rate = stats["correct"] / stats["total"]
            if success_rate < 0.5:
                weak_areas.append({
                    "topic": topic,
                    "success_rate": round(success_rate, 2),
                })

    # Calculate grade
    score = correct / total if total > 0 else 0
    grade = "F"
    if score >= 0.9: grade = "A+"
    elif score >= 0.8: grade = "A"
    elif score >= 0.7: grade = "B"
    elif score >= 0.6: grade = "C"
    elif score >= 0.5: grade = "D"

    return {
        "quiz_id": quiz_id,
        "total_questions": total,
        "correct": correct,
        "incorrect": total - correct,
        "score_percentage": round(score * 100, 1),
        "grade": grade,
        "total_xp": total_xp,
        "total_time_seconds": total_time_seconds,
        "avg_time_per_question": round(total_time_seconds / total, 1) if total else 0,
        "hints_used": total_hints,
        "topic_breakdown": {k: dict(v) for k, v in topic_stats.items()},
        "difficulty_breakdown": {k: dict(v) for k, v in diff_stats.items()},
        "weak_areas": weak_areas,
        "passed": score >= 0.6,
        "badge_earned": score >= 0.9,
        "perfect_run": correct == total and total_hints == 0,
    }


# =============================================================
# CACHE MANAGEMENT
# =============================================================

def clear_cache():
    """Clear the question cache (for testing)."""
    global _questions_cache, _questions_by_id, _questions_by_topic
    global _questions_by_difficulty, _questions_by_company
    _questions_cache = None
    _questions_by_id = None
    _questions_by_topic = None
    _questions_by_difficulty = None
    _questions_by_company = None
