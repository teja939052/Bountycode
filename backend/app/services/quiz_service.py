"""
Interactive Quiz & Mock Interview System
========================================

Provides multiple modes of practice:
  - Practice: Free practice with full solutions and hints
  - Quiz: Timed multiple choice without hints
  - Mock Interview: Realistic interview simulation with timer and pressure
  - Speed Run: Race against time for Diamonds
  - Learning Path: Adaptive progression through curriculum
  - Boss Battle: Challenge rounds with multiple questions
  - Code Golf: Shortest code wins

Each mode tracks:
  - Score, time, attempts
  - Diamonds earned, badges unlocked
  - Streak progress
  - Weak areas for recommendation

Canonical question ownership: all question loading flows through
``app.services.question_store`` (verified + executable only). This module
never independently scans or loads question files.
"""
import random
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from collections import defaultdict

from app.services import question_store as _qs


def _question_companies(question: Dict[str, Any]) -> List[str]:
    """Normalize company tags from both current and legacy question schemas."""
    raw = question.get("companies") or question.get("company") or []
    if isinstance(raw, str):
        raw = [raw]
    return [str(item).strip() for item in raw if str(item).strip()]


def _servable_questions() -> List[Dict[str, Any]]:
    """Return the canonical, trust-gated question pool from question_store.

    Only independently verified + executable questions are servable.
    Question content never lives in MongoDB; it is loaded once at startup
    from versioned files under backend/app/data/.
    """
    _qs.load_all()
    return [q for q in _qs._questions if _qs._is_servable(q)]
    """Fetch one complete question from the canonical store (verified only)."""
    return _qs.find_one_verified({"id": str(qid)})


def get_questions_by_topic(topic: str) -> List[Dict[str, Any]]:
    """Return servable questions matching a topic."""
    _qs.load_all()
    return [
        dict(q) for q in _qs._questions
        if _qs._is_servable(q) and str(q.get("topic", "")).strip().lower() == topic.strip().lower()
    ]


def get_questions_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    """Return servable questions matching a difficulty."""
    _qs.load_all()
    return [
        dict(q) for q in _qs._questions
        if _qs._is_servable(q) and str(q.get("difficulty") or "medium").strip().lower() == difficulty.strip().lower()
    ]


def get_questions_by_company(company: str) -> List[Dict[str, Any]]:
    """Return servable questions matching a company."""
    _qs.load_all()
    company_lower = company.strip().lower()
    return [
        dict(q) for q in _qs._questions
        if _qs._is_servable(q) and company_lower in {
            item.lower() for item in _question_companies(q)
        }
    ]

def get_all_questions() -> List[Dict[str, Any]]:
    """Return all servable questions from the canonical store."""
    return _servable_questions()


def get_question_stats() -> Dict[str, Any]:
    """Get overall question bank statistics for servable (verified + executable) questions."""
    questions = _servable_questions()
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
        for company in _question_companies(q):
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
    adaptive: bool = False,
    selection_seed: Optional[str] = None,
    evidence: Optional[Dict[str, Any]] = None,
    target_skills: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a quiz session based on mode and filters."""
    questions = _servable_questions()

    # Filter
    filtered = questions
    if topics:
        wanted_topics = {
            str(topic).strip().lower() for topic in topics if str(topic).strip()
        }
        filtered = [
            q for q in filtered
            if wanted_topics.intersection({
                str(q.get(field) or "").strip().lower()
                for field in ("topic", "sub_topic", "pattern")
            })
        ]
    if difficulty:
        filtered = [
            q for q in filtered
            if str(q.get("difficulty") or "medium").lower() == difficulty.lower()
        ]
    if company:
        requested_company = _normalize_company_tag(company)
        filtered = [
            q for q in filtered
            if requested_company in {
                _normalize_company_tag(item) for item in _question_companies(q)
            }
        ]

    # Interactive quiz sessions only include items with a server-side grading
    # key. Coding prompts without an answer key belong in compiler submissions.
    filtered = [
        q for q in filtered
        if str(q.get("correct_answer") or "").strip()
        or (
            bool(q.get("options"))
            and q.get("correct_index") is not None
        )
    ]

    # A constrained company/topic assessment must never silently turn into
    # an unrelated global quiz. Empty matches are explicit so the UI can offer
    # a safer alternative instead of teaching the wrong syllabus.
    if not filtered:
        return {
            "quiz_id": f"quiz_{int(time.time())}_{random.randint(1000, 9999)}",
            "mode": mode,
            "total_questions": 0,
            "time_limit_seconds": time_limit_seconds,
            "questions": [],
            "filters": {
                "topics": topics,
                "difficulty": difficulty,
                "company": company,
            },
            "created_at": datetime.now(timezone.utc).isoformat(),
            "user_level": user_level,
            "empty_reason": "No questions match the selected filters.",
        }

    selection_metadata: Dict[str, Any] = {}
    # Practice and quiz forms can opt into deterministic evidence-first
    # composition. Legacy modes retain their original difficulty contracts.
    if adaptive and mode in {"practice", "quiz"}:
        from app.services.adaptive_quiz_composer import compose_quiz

        composed = compose_quiz(
            filtered,
            num_questions=num_questions,
            seed=selection_seed or "anonymous-form-v1",
            evidence=evidence,
            company=company,
            difficulty=difficulty,
            target_skills=target_skills,
        )
        selected = composed["questions"]
        selection_metadata = {
            "selection_strategy": composed["strategy"],
            "selection_seed": composed["seed"],
            "selection_evidence": composed["selection_evidence"],
            "skill_distribution": composed["skill_distribution"],
            "evidence_summary": composed["evidence_summary"],
        }
        time_limit = time_limit_seconds
    elif mode == "mock_interview":
        # Mix difficulties: 1 easy, 2 medium, 2 hard
        by_diff = defaultdict(list)
        for q in filtered:
            by_diff[q.get("difficulty", "medium")].append(q)
        selected = (
            rng.sample(by_diff.get("easy", []), min(1, len(by_diff.get("easy", []))))
            + rng.sample(by_diff.get("medium", []), min(2, len(by_diff.get("medium", []))))
            + rng.sample(by_diff.get("hard", []), min(2, len(by_diff.get("hard", []))))
        )
        if randomize:
            rng.shuffle(selected)
        time_limit = time_limit_seconds or 90 * 60  # 90 min default
    elif mode == "boss_battle":
        # Hard questions only
        hard_qs = [q for q in filtered if q.get("difficulty") == "hard"]
        if not hard_qs:
            hard_qs = [q for q in filtered if q.get("difficulty") == "medium"]
        selected = rng.sample(hard_qs, min(num_questions, len(hard_qs)))
        time_limit = time_limit_seconds or 30 * 60
    elif mode == "speed_run":
        selected = rng.sample(filtered, min(num_questions, len(filtered)))
        time_limit = time_limit_seconds or 10 * 60
    else:  # practice or quiz
        selected = rng.sample(filtered, min(num_questions, len(filtered)))
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
                "companies": _question_companies(q),
                "type": q.get("type", "mcq" if q.get("options") else "short_answer"),
                "options": q.get("options", []) or [],
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
                "type": q.get("type", "mcq" if q.get("options") else "short_answer"),
                "options": q.get("options", []) or [],
                "xp_reward": q.get("xp_reward", 10) * 2,  # Bonus Diamonds
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
                "companies": _question_companies(q),
                "type": q.get("type", "mcq" if q.get("options") else "short_answer"),
                "options": q.get("options", []) or [],
                # Hints are delivered one at a time through /hint. Solutions,
                # expected answers and explanations are returned only after
                # the server has graded the submitted response.
                "hint_count": len(q.get("hints", []) or []),
                "test_case_count": len(q.get("test_cases", []) or []),
                "why_this_matters": q.get("why_this_matters", "") if mode == "practice" else "",
                "real_world_use": q.get("real_world_use", "") if mode == "practice" else "",
                "pattern_recognition": q.get("pattern_recognition", "") if mode == "practice" else "",
                "anti_patterns": q.get("anti_patterns", "") if mode == "practice" else "",
                "common_mistakes": q.get("common_mistakes", "") if mode == "practice" else "",
                "prerequisite_concepts": q.get("prerequisite_concepts", []),
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
        **selection_metadata,
    }


def submit_quiz_answer(
    quiz_id: str,
    question_id: str,
    user_answer: str,
    time_taken_seconds: float,
    hints_used: int = 0,
) -> Dict[str, Any]:
    """Evaluate a submitted answer and return feedback + Diamonds."""
    question = get_question_by_id(question_id)
    if not question:
        return {"error": "Question not found"}

    # Only grade answers for which the content bank contains a deterministic
    # answer key. Code submissions without a test-runner must not be passed by
    # typing "solved"/"yes" or by self-attestation.
    options = question.get("options") or []
    expected_index = question.get("correct_index")
    if options and expected_index is not None:
        try:
            selected_index = int(user_answer.strip())
        except (TypeError, ValueError):
            selected_index = next(
                (index for index, option in enumerate(options) if str(option).strip() == user_answer.strip()),
                -1,
            )
        try:
            expected_index = int(expected_index)
        except (TypeError, ValueError):
            expected_index = -1
        if expected_index < 0 or expected_index >= len(options):
            return {"error": "The question has an invalid answer key."}
        is_correct = selected_index == expected_index
        correct_answer = str(options[expected_index])
    else:
        correct_answer = str(question.get("correct_answer") or "").strip()
        if not correct_answer:
            return {
                "question_id": question_id,
                "is_correct": False,
                "requires_code_execution": True,
                "xp_earned": 0,
                "time_taken_seconds": time_taken_seconds,
                "hints_used": hints_used,
                "solution": {},
                "explanation": "",
                "error": "This question requires code execution and test-case grading; self-reported completion is disabled.",
            }
        is_correct = user_answer.strip() == correct_answer

    # Calculate Diamonds
    base_xp = question.get("xp_reward", 10)
    xp_earned = 0
    if is_correct:
        xp_earned = base_xp
        # Time bonus (faster = more Diamonds)
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
    questions = _servable_questions()

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
    questions = _servable_questions()

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
            "xp_per_question": "2x base Diamonds",
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
    topic_stats = defaultdict(lambda: {"correct": 0, "total": 0, "diamonds": 0})
    for i, q in enumerate(questions):
        if i < len(answers):
            ans = answers[i]
            topic = q.get("topic", "Other")
            topic_stats[topic]["total"] += 1
            if ans.get("is_correct"):
                topic_stats[topic]["correct"] += 1
            topic_stats[topic]["diamonds"] += ans.get("xp_earned", 0)

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
    _questions_by_company = None
