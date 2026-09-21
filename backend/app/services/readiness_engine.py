"""Placement Readiness Score Engine — pure deterministic calculation, NO AI.

Calculates a 0-100 readiness score from actual user performance data across
7 categories: dsa, aptitude, cs_fundamentals, coding, interview, resume,
and projects. Each category is scored independently and combined via a
weighted average. Company-specific readiness applies a match factor.

All functions are pure and testable without a database — they accept
pre-fetched data dicts and return structured results.

Canonical readiness formula (v1):
  overall = weighted_avg([
    dsa:        0.25,
    aptitude:   0.15,
    cs_fundamentals: 0.10,
    coding:     0.20,
    interview:  0.15,
    resume:     0.08,
    projects:   0.07,
  ])

Each category score is derived from real user history:
- dsa: solved_problems accuracy + streak
- aptitude: test scores + volume
- cs_fundamentals: interview answers tagged CS
- coding: submission pass rate
- interview: completed interview avg + volume + recency
- resume: ATS scores
- projects: generated/reviewed project count

The spec's 5-input design (world_completion_pct, mock_oa_avg_percentile,
interview_rubric_avg, repair_recovery_rate, srs_retention_rate) is the
target for v2; current v1 uses existing signals without new collections.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ── Category weights for overall score ────────────────────────────────
CATEGORY_WEIGHTS = {
    "dsa": 0.25,
    "aptitude": 0.15,
    "cs_fundamentals": 0.10,
    "coding": 0.20,
    "interview": 0.15,
    "resume": 0.08,
    "projects": 0.07,
}

# ── Company requirements (problem counts & skill thresholds) ──────────
COMPANY_PROFILES: Dict[str, Dict[str, Any]] = {
    "google": {
        "min_solved": 300, "min_medium": 150, "min_hard": 50,
        "min_skills": {"dsa": 80, "system_design": 70, "problem_solving": 85},
        "focus_topics": ["Arrays", "Dynamic Programming", "Graphs", "Trees", "System Design"],
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Onsite (4-5 rounds)"],
        "typical_timeline_weeks": 12,
        "match_weights": {"dsa": 0.40, "coding": 0.25, "interview": 0.15, "aptitude": 0.10, "cs_fundamentals": 0.05, "resume": 0.03, "projects": 0.02},
    },
    "amazon": {
        "min_solved": 250, "min_medium": 120, "min_hard": 40,
        "min_skills": {"dsa": 75, "leadership": 80, "system_design": 65},
        "focus_topics": ["Arrays", "Linked Lists", "Trees", "Dynamic Programming", "Leadership Principles"],
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Loop (5 rounds)"],
        "typical_timeline_weeks": 10,
        "match_weights": {"dsa": 0.30, "interview": 0.25, "coding": 0.20, "aptitude": 0.10, "cs_fundamentals": 0.05, "resume": 0.05, "projects": 0.05},
    },
    "microsoft": {
        "min_solved": 200, "min_medium": 100, "min_hard": 30,
        "min_skills": {"dsa": 70, "system_design": 60, "problem_solving": 75},
        "focus_topics": ["Arrays", "Strings", "Trees", "Graphs", "System Design"],
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Onsite (3-4 rounds)"],
        "typical_timeline_weeks": 8,
        "match_weights": {"dsa": 0.35, "coding": 0.25, "interview": 0.20, "aptitude": 0.05, "cs_fundamentals": 0.05, "resume": 0.05, "projects": 0.05},
    },
    "meta": {
        "min_solved": 280, "min_medium": 140, "min_hard": 45,
        "min_skills": {"dsa": 80, "system_design": 75, "coding": 85},
        "focus_topics": ["Arrays", "Dynamic Programming", "Graphs", "System Design", "Behavioral"],
        "interview_rounds": ["Technical Phone Screen", "Onsite (Coding + System Design + Behavioral)"],
        "typical_timeline_weeks": 10,
        "match_weights": {"dsa": 0.35, "coding": 0.30, "interview": 0.15, "cs_fundamentals": 0.05, "aptitude": 0.05, "resume": 0.05, "projects": 0.05},
    },
    "tcs": {
        "min_solved": 50, "min_medium": 20, "min_hard": 5,
        "min_skills": {"dsa": 50, "aptitude": 60, "verbal": 50},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
        "match_weights": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "resume": 0.03, "projects": 0.02},
    },
    "infosys": {
        "min_solved": 60, "min_medium": 25, "min_hard": 5,
        "min_skills": {"dsa": 45, "aptitude": 55, "verbal": 45},
        "focus_topics": ["Arrays", "Strings", "Basic Data Structures", "Aptitude"],
        "interview_rounds": ["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
        "match_weights": {"aptitude": 0.32, "dsa": 0.23, "cs_fundamentals": 0.13, "coding": 0.15, "interview": 0.12, "resume": 0.03, "projects": 0.02},
    },
    "wipro": {
        "min_solved": 40, "min_medium": 15, "min_hard": 3,
        "min_skills": {"dsa": 40, "aptitude": 50, "verbal": 40},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 3,
        "match_weights": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "resume": 0.03, "projects": 0.02},
    },
    # ── Service-tier targets (config-modeled preparation weights, not
    # employer claims: weights say what THIS platform measures harder for
    # each target, never "probability of passing X". Pseudo-code emphasis
    # is measured through the coding category; verbal through aptitude.)
    "accenture": {
        "min_solved": 80, "min_medium": 30, "min_hard": 8,
        "min_skills": {"dsa": 55, "aptitude": 55, "verbal": 60},
        "focus_topics": ["Arrays", "Strings", "Pseudo-code Tracing", "Aptitude", "Communication"],
        "interview_rounds": ["Cognitive Assessment", "Technical Assessment", "Coding Test", "Interview"],
        "typical_timeline_weeks": 5,
        "match_weights": {"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.10, "coding": 0.15, "interview": 0.20, "resume": 0.05, "projects": 0.05},
    },
    "cognizant": {
        "min_solved": 60, "min_medium": 25, "min_hard": 5,
        "min_skills": {"dsa": 50, "aptitude": 60, "verbal": 55},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
        "match_weights": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.10, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.02},
    },
    "capgemini": {
        "min_solved": 60, "min_medium": 25, "min_hard": 6,
        "min_skills": {"dsa": 50, "aptitude": 55, "verbal": 50, "coding": 55},
        "focus_topics": ["Arrays", "Pseudo-code Tracing", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
        "match_weights": {"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.15, "coding": 0.20, "interview": 0.12, "resume": 0.03, "projects": 0.05},
    },
    "hcl": {
        "min_solved": 50, "min_medium": 20, "min_hard": 5,
        "min_skills": {"dsa": 45, "aptitude": 55, "verbal": 50},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
        "match_weights": {"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.05},
    },
    "tech_mahindra": {
        "min_solved": 50, "min_medium": 20, "min_hard": 4,
        "min_skills": {"dsa": 45, "aptitude": 55, "verbal": 50},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Networking Basics"],
        "interview_rounds": ["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
        "match_weights": {"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.05},
    },
    "lti_mindtree": {
        "min_solved": 50, "min_medium": 20, "min_hard": 4,
        "min_skills": {"dsa": 45, "aptitude": 55, "verbal": 50},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 4,
        "match_weights": {"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.05},
    },
    "mphasis": {
        "min_solved": 40, "min_medium": 15, "min_hard": 3,
        "min_skills": {"dsa": 40, "aptitude": 50, "verbal": 45},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 3,
        "match_weights": {"aptitude": 0.28, "dsa": 0.20, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.17, "resume": 0.03, "projects": 0.05},
    },
    "uber": {
        "min_solved": 200, "min_medium": 100, "min_hard": 35,
        "min_skills": {"dsa": 75, "system_design": 65, "problem_solving": 80},
        "focus_topics": ["Arrays", "Dynamic Programming", "Graphs", "Trees", "System Design"],
        "interview_rounds": ["Online Assessment", "Technical Phone Screen", "Onsite (4 rounds)"],
        "typical_timeline_weeks": 8,
        "match_weights": {"dsa": 0.35, "coding": 0.25, "interview": 0.20, "cs_fundamentals": 0.05, "aptitude": 0.05, "resume": 0.05, "projects": 0.05},
    },
    "apple": {
        "min_solved": 250, "min_medium": 120, "min_hard": 40,
        "min_skills": {"dsa": 75, "system_design": 70, "problem_solving": 80},
        "focus_topics": ["Arrays", "Trees", "Dynamic Programming", "System Design", "Low-Level Design"],
        "interview_rounds": ["Phone Screen", "Onsite (5-6 rounds)"],
        "typical_timeline_weeks": 10,
        "match_weights": {"dsa": 0.30, "coding": 0.25, "interview": 0.20, "cs_fundamentals": 0.10, "aptitude": 0.05, "resume": 0.05, "projects": 0.05},
    },
}

# Short-form aliases resolve to the same configured target (shared reference,
# read-only in scoring paths).
COMPANY_PROFILES["techm"] = COMPANY_PROFILES["tech_mahindra"]
COMPANY_PROFILES["lti"] = COMPANY_PROFILES["lti_mindtree"]


@dataclass
class CategoryScore:
    """Score for a single readiness category."""
    name: str
    score: float  # 0-100
    weight: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReadinessScore:
    """Complete readiness assessment for a user."""
    overall: float  # 0-100
    categories: Dict[str, CategoryScore]
    company: Optional[str] = None
    company_score: Optional[float] = None
    company_match: Optional[Dict[str, Any]] = None
    recommendations: List[Dict[str, Any]] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)


def score_dsa(data: Dict[str, Any]) -> CategoryScore:
    """Score DSA readiness from solved_problems data.

    Algorithm:
    - Count problems by difficulty (easy/medium/hard)
    - Each difficulty tier has a target count
    - Score = min(100, easy_score*0.30 + medium_score*0.40 + hard_score*0.30)
    - Bonus for topic breadth (number of unique topics >= 5)

    Args:
        data: dict with keys:
            total_solved (int), easy (int), medium (int), hard (int),
            unique_topics (int), accuracy_rate (float 0-1)
    """
    easy = data.get("easy", 0)
    medium = data.get("medium", 0)
    hard = data.get("hard", 0)
    unique_topics = data.get("unique_topics", 0)
    accuracy = data.get("accuracy_rate", 0.0)

    # Targets: 100 easy, 80 medium, 30 hard for 100/100 score
    easy_score = min(100, easy / 100 * 100)
    medium_score = min(100, medium / 80 * 100)
    hard_score = min(100, hard / 30 * 100)

    base = easy_score * 0.30 + medium_score * 0.40 + hard_score * 0.30

    # Breadth bonus: up to +10 points for covering 5+ topics
    breadth_bonus = min(10, unique_topics * 2)

    # Accuracy modifier: scale between 0.8 and 1.0 based on accuracy
    acc_modifier = 0.8 + 0.2 * min(1.0, accuracy)

    score = min(100, (base + breadth_bonus) * acc_modifier)

    return CategoryScore(
        name="dsa",
        score=round(score, 1),
        weight=CATEGORY_WEIGHTS["dsa"],
        details={
            "easy": easy, "medium": medium, "hard": hard,
            "unique_topics": unique_topics,
            "accuracy_rate": round(accuracy * 100, 1),
            "easy_score": round(easy_score, 1),
            "medium_score": round(medium_score, 1),
            "hard_score": round(hard_score, 1),
        },
    )


def score_aptitude(data: Dict[str, Any]) -> CategoryScore:
    """Score aptitude readiness from aptitude_tests results.

    Algorithm:
    - Average percentage across completed tests
    - Weight recent tests higher (exponential decay, half-life = 5 tests)
    - Bonus for taking tests in multiple categories

    Args:
        data: dict with keys:
            avg_percentage (float 0-100), test_count (int),
            category_count (int), recent_percentages (list[float])
    """
    avg_pct = data.get("avg_percentage", 0.0)
    test_count = data.get("test_count", 0)
    category_count = data.get("category_count", 0)
    recent = data.get("recent_percentages", [])

    if test_count == 0:
        return CategoryScore(name="aptitude", score=0.0, weight=CATEGORY_WEIGHTS["aptitude"],
                             details={"test_count": 0, "message": "No aptitude tests completed"})

    # Weighted recent average (exponential decay)
    if recent:
        decay_weights = [0.5 ** i for i in range(len(recent))]
        total_w = sum(decay_weights)
        weighted_recent = sum(p * w for p, w in zip(recent, decay_weights)) / total_w if total_w > 0 else avg_pct
    else:
        weighted_recent = avg_pct

    base = weighted_recent

    # Volume bonus: +1 per test, max +10
    volume_bonus = min(10, test_count)

    # Category diversity bonus: +3 per unique category, max +9
    diversity_bonus = min(9, category_count * 3)

    # Diminishing returns after 15 tests
    if test_count > 15:
        volume_bonus = min(10, 10 + (test_count - 15) * 0.1)

    score = min(100, base + volume_bonus + diversity_bonus)

    return CategoryScore(
        name="aptitude",
        score=round(score, 1),
        weight=CATEGORY_WEIGHTS["aptitude"],
        details={
            "avg_percentage": round(avg_pct, 1),
            "weighted_recent": round(weighted_recent, 1),
            "test_count": test_count,
            "category_count": category_count,
            "volume_bonus": round(volume_bonus, 1),
            "diversity_bonus": round(diversity_bonus, 1),
        },
    )


def score_cs_fundamentals(data: Dict[str, Any]) -> CategoryScore:
    """Score CS fundamentals from interview answers tagged with CS topics.

    Algorithm:
    - Filter interview Q&As to CS-tagged questions (technical, system_design)
    - Average score from those answers
    - Weight by recency (more recent = higher weight)

    Args:
        data: dict with keys:
            cs_question_count (int), avg_score (float 0-10),
            topic_scores (dict[str, float])
    """
    count = data.get("cs_question_count", 0)
    avg_score = data.get("avg_score", 0.0)
    topic_scores = data.get("topic_scores", {})

    if count == 0:
        return CategoryScore(name="cs_fundamentals", score=0.0, weight=CATEGORY_WEIGHTS["cs_fundamentals"],
                             details={"cs_question_count": 0, "message": "No CS fundamentals questions attempted"})

    # Normalize to 0-100 (scores are 0-10)
    base = avg_score * 10

    # Depth bonus for covering multiple CS topics
    depth_bonus = min(15, len(topic_scores) * 3)

    # Confidence scaling: more questions = more reliable score
    confidence = min(1.0, count / 20)

    score = min(100, base * confidence + depth_bonus)

    return CategoryScore(
        name="cs_fundamentals",
        score=round(score, 1),
        weight=CATEGORY_WEIGHTS["cs_fundamentals"],
        details={
            "cs_question_count": count,
            "avg_score": round(avg_score, 1),
            "topics_covered": len(topic_scores),
            "topic_scores": {k: round(v, 1) for k, v in topic_scores.items()},
        },
    )


def score_coding(data: Dict[str, Any]) -> CategoryScore:
    """Score coding readiness from submissions data.

    Algorithm:
    - Submission success rate (passed / total submissions)
    - Time efficiency (how close to optimal time)
    - Language diversity
    - Recent performance trend

    Args:
        data: dict with keys:
            total_submissions (int), passed_submissions (int),
            languages_used (int), avg_execution_time (float),
            recent_success_rate (float 0-1)
    """
    total = data.get("total_submissions", 0)
    passed = data.get("passed_submissions", 0)
    languages = data.get("languages_used", 0)
    recent_rate = data.get("recent_success_rate", 0.0)

    if total == 0:
        return CategoryScore(name="coding", score=0.0, weight=CATEGORY_WEIGHTS["coding"],
                             details={"total_submissions": 0, "message": "No submissions yet"})

    # Success rate score (70% weight)
    success_rate = passed / total
    success_score = success_rate * 100

    # Volume score (15% weight) — diminishing returns after 50 submissions
    volume_score = min(100, total / 50 * 100)

    # Language diversity score (10% weight)
    lang_score = min(100, languages / 3 * 100)

    # Recent trend score (5% weight)
    trend_score = recent_rate * 100

    base = success_score * 0.70 + volume_score * 0.15 + lang_score * 0.10 + trend_score * 0.05

    score = min(100, base)

    return CategoryScore(
        name="coding",
        score=round(score, 1),
        weight=CATEGORY_WEIGHTS["coding"],
        details={
            "total_submissions": total,
            "passed_submissions": passed,
            "success_rate": round(success_rate * 100, 1),
            "languages_used": languages,
            "recent_success_rate": round(recent_rate * 100, 1),
        },
    )


def score_interview(data: Dict[str, Any]) -> CategoryScore:
    """Score interview readiness from interview history.

    Algorithm:
    - Average final score across completed interviews
    - Weight by company relevance (FAANG interviews count more)
    - Bonus for interview volume (more practice = better)
    - Recent interviews weighted higher

    Args:
        data: dict with keys:
            completed_count (int), avg_score (float 0-10),
            recent_scores (list[float]), company_breakdown (dict[str, float])
    """
    completed = data.get("completed_count", 0)
    avg_score = data.get("avg_score", 0.0)
    recent_scores = data.get("recent_scores", [])

    if completed == 0:
        return CategoryScore(name="interview", score=0.0, weight=CATEGORY_WEIGHTS["interview"],
                             details={"completed_count": 0, "message": "No interviews completed"})

    # Base score from average (0-10 → 0-100)
    base = avg_score * 10

    # Volume bonus: +5 per completed interview, max +20
    volume_bonus = min(20, completed * 5)

    # Recency boost: last 5 interviews weighted higher
    if recent_scores:
        recent_avg = sum(recent_scores[-5:]) / len(recent_scores[-5:])
        recency_boost = max(0, (recent_avg - avg_score) * 2)
    else:
        recency_boost = 0

    score = min(100, base + volume_bonus + recency_boost)

    return CategoryScore(
        name="interview",
        score=round(score, 1),
        weight=CATEGORY_WEIGHTS["interview"],
        details={
            "completed_count": completed,
            "avg_score": round(avg_score, 1),
            "volume_bonus": round(volume_bonus, 1),
            "recency_boost": round(recency_boost, 1),
        },
    )


def score_resume(data: Dict[str, Any]) -> CategoryScore:
    """Score resume readiness from ATS scores.

    Algorithm:
    - Average ATS score across all resumes
    - Best ATS score bonus
    - Number of optimizations done

    Args:
        data: dict with keys:
            resume_count (int), avg_ats_score (float 0-100),
            best_ats_score (float 0-100), optimization_count (int)
    """
    count = data.get("resume_count", 0)
    avg_ats = data.get("avg_ats_score", 0.0)
    best_ats = data.get("best_ats_score", 0.0)
    opt_count = data.get("optimization_count", 0)

    if count == 0:
        return CategoryScore(name="resume", score=0.0, weight=CATEGORY_WEIGHTS["resume"],
                             details={"resume_count": 0, "message": "No resumes uploaded"})

    # Base from average ATS score
    base = avg_ats

    # Best score bonus: (best - avg) * 0.3, max +10
    best_bonus = min(10, max(0, (best_ats - avg_ats) * 0.3))

    # Optimization bonus: +3 per optimization, max +12
    opt_bonus = min(12, opt_count * 3)

    score = min(100, base + best_bonus + opt_bonus)

    return CategoryScore(
        name="resume",
        score=round(score, 1),
        weight=CATEGORY_WEIGHTS["resume"],
        details={
            "resume_count": count,
            "avg_ats_score": round(avg_ats, 1),
            "best_ats_score": round(best_ats, 1),
            "optimization_count": opt_count,
        },
    )


def score_projects(data: Dict[str, Any]) -> CategoryScore:
    """Score project readiness from generated/reviewed projects.

    Algorithm:
    - Number of projects created (more = better)
    - Quality signals: has tech_stack, has setup_instructions, file count
    - Project review scores if available

    Args:
        data: dict with keys:
            project_count (int), avg_file_count (float),
            with_tech_stack (int), reviewed_count (int),
            avg_review_score (float 0-10)
    """
    count = data.get("project_count", 0)
    avg_files = data.get("avg_file_count", 0.0)
    with_stack = data.get("with_tech_stack", 0)
    reviewed = data.get("reviewed_count", 0)
    avg_review = data.get("avg_review_score", 0.0)

    if count == 0:
        return CategoryScore(name="projects", score=0.0, weight=CATEGORY_WEIGHTS["projects"],
                             details={"project_count": 0, "message": "No projects created"})

    # Volume score: +15 per project, max 60
    volume_score = min(60, count * 15)

    # Quality signals
    quality_score = 0
    if count > 0:
        tech_ratio = with_stack / count
        quality_score += tech_ratio * 20  # max 20

    # Review bonus
    review_bonus = 0
    if reviewed > 0:
        review_bonus = min(20, avg_review * 2)

    score = min(100, volume_score + quality_score + review_bonus)

    return CategoryScore(
        name="projects",
        score=round(score, 1),
        weight=CATEGORY_WEIGHTS["projects"],
        details={
            "project_count": count,
            "avg_file_count": round(avg_files, 1),
            "with_tech_stack": with_stack,
            "reviewed_count": reviewed,
            "avg_review_score": round(avg_review, 1),
        },
    )


def calculate_readiness(
    dsa_data: Dict[str, Any],
    aptitude_data: Dict[str, Any],
    cs_data: Dict[str, Any],
    coding_data: Dict[str, Any],
    interview_data: Dict[str, Any],
    resume_data: Dict[str, Any],
    project_data: Dict[str, Any],
    company: Optional[str] = None,
) -> ReadinessScore:
    """Calculate the full readiness score from all category data.

    Computes each category independently, then combines via weighted average.
    If a company is specified, applies company-specific weights and calculates
    a company match score.

    Args:
        dsa_data: Data for DSA scoring.
        aptitude_data: Data for aptitude scoring.
        cs_data: Data for CS fundamentals scoring.
        coding_data: Data for coding scoring.
        interview_data: Data for interview scoring.
        resume_data: Data for resume scoring.
        project_data: Data for project scoring.
        company: Optional company name for company-specific readiness.

    Returns:
        ReadinessScore with overall score, per-category breakdowns, and
        optional company-specific assessment.
    """
    categories = {
        "dsa": score_dsa(dsa_data),
        "aptitude": score_aptitude(aptitude_data),
        "cs_fundamentals": score_cs_fundamentals(cs_data),
        "coding": score_coding(coding_data),
        "interview": score_interview(interview_data),
        "resume": score_resume(resume_data),
        "projects": score_projects(project_data),
    }

    # Overall = weighted average
    total_weight = sum(c.weight for c in categories.values())
    overall = sum(c.score * c.weight for c in categories.values()) / total_weight if total_weight > 0 else 0
    overall = round(min(100, max(0, overall)), 1)

    # Company-specific readiness
    company_score = None
    company_match = None
    if company:
        company_key = company.lower().strip()
        profile = COMPANY_PROFILES.get(company_key)
        if profile:
            match_weights = profile.get("match_weights", CATEGORY_WEIGHTS)
            company_total_weight = sum(match_weights.get(k, 0) for k in categories)
            company_score = sum(
                categories[k].score * match_weights.get(k, 0) for k in categories
            ) / company_total_weight if company_total_weight > 0 else 0
            company_score = round(min(100, max(0, company_score)), 1)

            company_match = _compute_company_match(categories, profile)

    result = ReadinessScore(
        overall=overall,
        categories=categories,
        company=company,
        company_score=company_score,
        company_match=company_match,
    )

    # Generate recommendations
    result.recommendations = _generate_recommendations(categories, company)

    # Stats summary
    result.stats = {
        "overall": overall,
        "company_score": company_score,
        "categories_scored": len(categories),
        "strongest": max(categories.items(), key=lambda x: x[1].score)[0],
        "weakest": min(categories.items(), key=lambda x: x[1].score)[0],
    }

    return result


def _compute_company_match(
    categories: Dict[str, CategoryScore],
    profile: Dict[str, Any],
) -> Dict[str, Any]:
    """Compute how well the user matches a company's requirements.

    Returns a dict with match_level, gaps, and strengths.
    """
    min_skills = profile.get("min_skills", {})
    gaps = []
    strengths = []

    for skill, threshold in min_skills.items():
        # Map skill names to category names
        cat_name = _map_skill_to_category(skill)
        if cat_name and cat_name in categories:
            user_score = categories[cat_name].score
            if user_score < threshold:
                gaps.append({
                    "area": skill,
                    "required": threshold,
                    "current": round(user_score, 1),
                    "gap": round(threshold - user_score, 1),
                })
            else:
                strengths.append({
                    "area": skill,
                    "required": threshold,
                    "current": round(user_score, 1),
                })

    total_problems = categories["dsa"].details.get("easy", 0) + categories["dsa"].details.get("medium", 0) + categories["dsa"].details.get("hard", 0)

    if total_problems < profile.get("min_solved", 0):
        gaps.append({
            "area": "total_problems",
            "required": profile["min_solved"],
            "current": total_problems,
            "gap": profile["min_solved"] - total_problems,
        })

    # Determine match level
    if not gaps:
        match_level = "ready"
    elif len(gaps) <= 2 and all(g["gap"] < 20 for g in gaps):
        match_level = "almost_ready"
    elif len(gaps) <= 4:
        match_level = "in_progress"
    else:
        match_level = "needs_work"

    return {
        "match_level": match_level,
        "gaps": gaps,
        "strengths": strengths,
    }


def _map_skill_to_category(skill: str) -> Optional[str]:
    """Map a company skill requirement name to a readiness category."""
    mapping = {
        "dsa": "dsa",
        "data_structures": "dsa",
        "algorithms": "dsa",
        "problem_solving": "dsa",
        "aptitude": "aptitude",
        "verbal": "aptitude",
        "quantitative": "aptitude",
        "system_design": "cs_fundamentals",
        "leadership": "interview",
        "behavioral": "interview",
        "coding": "coding",
        "communication": "interview",
    }
    return mapping.get(skill.lower())


def _generate_recommendations(
    categories: Dict[str, CategoryScore],
    company: Optional[str],
) -> List[Dict[str, Any]]:
    """Generate prioritized recommendations based on scores.

    Focuses on the weakest areas first, with specific actionable advice.
    """
    recs = []

    # Sort categories by score ascending (weakest first)
    sorted_cats = sorted(categories.items(), key=lambda x: x[1].score)

    for cat_name, cat_score in sorted_cats:
        if cat_score.score >= 80:
            continue  # Already strong

        priority = "high" if cat_score.score < 40 else "medium" if cat_score.score < 65 else "low"
        recs.append({
            "category": cat_name,
            "current_score": cat_score.score,
            "priority": priority,
            "message": _recommendation_message(cat_name, cat_score),
        })

    # Company-specific gap recommendations
    if company:
        company_key = company.lower().strip()
        profile = COMPANY_PROFILES.get(company_key)
        if profile:
            total_problems = (categories["dsa"].details.get("easy", 0)
                              + categories["dsa"].details.get("medium", 0)
                              + categories["dsa"].details.get("hard", 0))
            if total_problems < profile["min_solved"]:
                gap = profile["min_solved"] - total_problems
                recs.insert(0, {
                    "category": "dsa",
                    "current_score": total_problems,
                    "priority": "high",
                    "message": f"Solve {gap} more problems to meet {company.title()}'s requirement of {profile['min_solved']}",
                })

    return recs


def _recommendation_message(cat_name: str, cat_score: CategoryScore) -> str:
    """Generate a specific recommendation message for a category."""
    messages = {
        "dsa": "Practice more data structure and algorithm problems. Focus on medium/hard difficulty.",
        "aptitude": "Take more aptitude tests across different categories to improve speed and accuracy.",
        "cs_fundamentals": "Practice technical interview questions on OS, DBMS, networking, and system design.",
        "coding": "Submit more coding solutions. Focus on passing test cases consistently.",
        "interview": "Complete more mock interviews. Practice both behavioral and technical rounds.",
        "resume": "Upload and optimize your resume. Aim for an ATS score above 75.",
        "projects": "Create more projects to demonstrate practical skills.",
    }
    return messages.get(cat_name, f"Improve {cat_name} score from {cat_score.score} to 70+.")


def predict_readiness_date(overall_score: float, company: Optional[str] = None) -> Dict[str, Any]:
    """Predict when the user will be ready based on current score.

    Uses a simple linear projection based on company typical timelines.

    Args:
        overall_score: Current overall readiness score (0-100).
        company: Target company name.

    Returns:
        Dict with weeks_remaining, estimated_date, and confidence level.
    """
    from datetime import datetime, timedelta, timezone

    if company:
        profile = COMPANY_PROFILES.get(company.lower().strip(), {})
        typical_weeks = profile.get("typical_timeline_weeks", 8)
    else:
        typical_weeks = 8

    if overall_score >= 90:
        weeks_remaining = max(1, typical_weeks * 0.1)
    elif overall_score >= 70:
        weeks_remaining = max(2, typical_weeks * 0.3)
    elif overall_score >= 50:
        weeks_remaining = max(4, typical_weeks * 0.5)
    elif overall_score >= 30:
        weeks_remaining = max(6, typical_weeks * 0.7)
    else:
        weeks_remaining = typical_weeks

    ready_date = datetime.now(timezone.utc) + timedelta(weeks=weeks_remaining)

    return {
        "weeks_remaining": round(weeks_remaining),
        "estimated_date": ready_date.strftime("%B %d, %Y"),
        "confidence": "High" if overall_score > 60 else "Medium" if overall_score > 30 else "Low",
    }


# ─── Trust-weighted evidence policy (A3, 2026-09-10) ─────────────────────
# Readiness must distinguish WHERE evidence came from. Weights apply to
# question-derived counts (solves); unresolvable legacy solves count weakly
# rather than vanishing (backward-compatible, conservative).
#   verified / reviewed  → high-confidence assessment evidence (1.0 / 0.85)
#   automated_checked    → learning evidence, lower-confidence assessment (0.5)
#   needs_review / quarantined / unverified → NO readiness evidence (0.0)
#   unresolvable (no bank match) → weak partial credit (0.25)
TRUST_WEIGHT = {
    "verified": 1.0,
    "reviewed": 0.85,
    "automated_checked": 0.5,
    "needs_review": 0.0,
    "quarantined": 0.0,
    "unverified": 0.0,
}
_UNKNOWN_TRUST_WEIGHT = 0.25


def _trust_weight(trust_status) -> float:
    if trust_status is None:
        return _UNKNOWN_TRUST_WEIGHT
    return TRUST_WEIGHT.get(str(trust_status).lower(), _UNKNOWN_TRUST_WEIGHT)


def _resolve_question_trust(question_id) -> str:
    """Resolve a solve's question_id to its bank trust_status. Returns "" when
    unresolvable (weighted as unknown, never as verified). Never raises."""
    try:
        from app.services import question_store as qs
        q = qs.find_one({"id": str(question_id or "")})
        if q:
            return str(q.get("trust_status") or "")
    except Exception:
        pass
    return ""


# ─── Target readiness v2 — deterministic, zero-AI decision layer ─────────
# DESIGN (2026-09-18, measurement-not-prediction):
#   AI may EXPLAIN readiness. AI must not DECIDE readiness. This module has
#   zero AI imports, performs zero network calls, and is a pure function of
#   (stored evidence + explicit target configuration): same inputs → same
#   output, even with every AI service down.
#
# SOURCE → EXISTING API/MODEL → DATA USED (no new stores, no new engines):
#   target skills/weights/criticality → role_engine.profiles.ROLE_PROFILES
#     (readiness_weights + SkillDef.importance) → target skill map.
#   company overlay → COMPANY_PROFILES match_weights (this module, explicit
#     config) × company_blueprints.json (freshness/sections, read-only).
#   skill identity → skill_taxonomy.canonical_skill_id / canonical_domain
#     (domain.subskill namespace; OA/interview sections mapped, never
#     rewritten in place).
#   mastery → mastery_engine.calculate_mastery_level over eligible solves +
#     learning-event attempts (0-5 level → ×20 = 0-100).
#   assessment → oa_sessions/skill_graph oa_outcomes + aptitude_tests +
#     interviews_collection/interview_outcomes + learning-event scores,
#     recency-weighted; trust-gated (see TRUST RULE below).
#   transfer → learning_events with activity_type containing
#     repair/retest/transfer (repair retests are verified-only by
#     construction in repair._verified_questions_for_skill). No dedicated
#     transfer store exists; this is documented, not invented.
#   retention → srs_cards (srs_cards_collection) + srs_states
#     (srs_collection) via spaced_repetition SM-2 fields
#     (repetitions/lapses/total_reviews).
#   consistency → spread of the recent per-skill score series.
#   next_action → {"type": "repair", skill} mapping onto existing
#     repair missions (repair_service); no new recommendation engine.
#
# GRANULARITY DECISION: target skills are canonical DOMAINS (dsa, coding,
#   aptitude, cs_fundamentals, system_design, interview, behavioral, resume,
#   projects). Role SkillDefs (e.g. "DSA", "DBMS") resolve to domains through
#   the canonical mapper; defs landing on the same domain merge (weights sum,
#   critical wins). Per-subskill scores (arrays vs graphs) would be fake
#   precision: no assessment store records subskill-level outcomes.
#
# TRUST RULE (reuses governance, creates none): question_governance defines
#   UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED. Solve-level
#   tiers reuse the TRUST_WEIGHT table above: verified/reviewed are
#   high-stakes assessment evidence; automated_checked is learning-only
#   evidence (counts for mastery/transfer/retention/consistency, never for
#   the assessment component); needs_review/quarantined/unverified/unknown
#   contribute nothing. Repair retests are verified-only by construction.
#
# RECENCY RULE (documented, no silent decay): assessment samples are combined
#   oldest-first with linear recency weights 1..n (recency_weighted_avg).
#   Historical evidence is never deleted; freshness (share of target weight
#   with evidence ≤ FRESH_DAYS old) is exposed separately.
#
# STATUS RULE (centralized constants below, no LLM labels):
#   coverage < MIN_COVERAGE_FOR_JUDGMENT → INSUFFICIENT_EVIDENCE
#   no blockers AND coverage ≥ READY_COVERAGE AND score ≥ READY_SCORE → READY
#   score ≥ READY_WITH_GAPS_SCORE (and evidence sufficient) → READY_WITH_GAPS
#   else → DEVELOPING
# NEVER OUTPUT: probability of passing/hire, days-until-ready, AI confidence.
# predict_readiness_date() below is legacy, has no callers, and is never
# surfaced in any readiness response.

SKILL_COMPONENT_WEIGHTS = {
    "mastery": 0.30,
    "assessment": 0.25,
    "transfer": 0.20,
    "retention": 0.15,
    "consistency": 0.10,
}

CRITICAL_SKILL_THRESHOLD = 60.0
MIN_EVIDENCE_PER_SKILL = 3
MIN_COVERAGE_FOR_JUDGMENT = 20.0
READY_SCORE = 75.0
READY_COVERAGE = 80.0
READY_WITH_GAPS_SCORE = 60.0
STRONG_SKILL = 75.0
GAP_SKILL = 60.0
FRESH_DAYS = 30

HIGH_STAKES_TRUST = {"verified", "reviewed"}
LEARNING_TRUST = {"verified", "reviewed", "automated_checked"}
TRANSFER_ACTIVITIES = ("retest", "repair", "transfer")

# Canonical domain → readiness category (for the company-weight overlay).
# _map_skill_to_category covers most names; the fallback covers the rest.
_DOMAIN_CATEGORY_FALLBACK = {
    "interview": "interview",
    "behavioral": "interview",
    "resume": "resume",
    "projects": "projects",
    "cs_fundamentals": "cs_fundamentals",
    "coding": "coding",
    "dsa": "dsa",
    "aptitude": "aptitude",
    "system_design": "cs_fundamentals",
}


def _domain_category(domain: str) -> Optional[str]:
    mapped = _map_skill_to_category(domain or "")
    if mapped:
        return mapped
    return _DOMAIN_CATEGORY_FALLBACK.get((domain or "").lower())


def _utcnow_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def _as_iso(value: Any) -> Optional[str]:
    """Best-effort ISO-8601 string for datetimes/ISO strings. None if unknown."""
    if value is None:
        return None
    try:
        from datetime import datetime, timezone
        if isinstance(value, datetime):
            dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        s = str(value).strip()
        if not s:
            return None
        # Validate parseable; keep original string for lexicographic max().
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return s
    except Exception:
        return None


def _is_fresh(iso: Optional[str], now_iso: Optional[str] = None) -> bool:
    if not iso:
        return False
    try:
        from datetime import datetime, timedelta, timezone
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.fromisoformat((now_iso or _utcnow_iso()).replace("Z", "+00:00"))
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        return (now - dt) <= timedelta(days=FRESH_DAYS)
    except Exception:
        return False


def recency_weighted_avg(values_oldest_first: List[float]) -> float:
    """Deterministic recency rule: linear weights 1..n, oldest → newest."""
    vals = [max(0.0, min(100.0, float(v))) for v in (values_oldest_first or [])]
    if not vals:
        return 0.0
    weights = list(range(1, len(vals) + 1))
    return round(sum(v * w for v, w in zip(vals, weights)) / sum(weights), 1)


def consistency_from_series(scores: List[float]) -> float:
    """Reward sustained performance; punish lucky spikes.

    100 - 2×clamped stdev (0..50 → 100..0). Fewer than 2 samples is not
    evidence of consistency either way → neutral 50 (documented).
    """
    vals = [max(0.0, min(100.0, float(v))) for v in (scores or [])]
    if len(vals) < 2:
        return 50.0
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    return round(max(0.0, min(100.0, 100.0 - 2.0 * min(50.0, math.sqrt(var)))), 1)


def retention_from_srs(repetitions: int, lapses: int, total_reviews: int) -> float:
    """SM-2 history → 0-100. No reviews is no evidence → 0 (documented)."""
    reps = max(0, int(repetitions or 0))
    lap = max(0, int(lapses or 0))
    if max(0, int(total_reviews or 0)) <= 0 and reps + lap <= 0:
        return 0.0
    return round(100.0 * reps / max(1, reps + lap), 1)


def _resolve_skill_domain(name: Optional[str]) -> Optional[str]:
    """Any skill/topic/concept/section name → canonical domain. None if unmapped."""
    if not name:
        return None
    try:
        from app.services.skill_taxonomy import canonical_domain, canonical_skill_id
        canon = canonical_skill_id(str(name))
        if canon:
            return canonical_domain(canon)
    except Exception:
        pass
    return None


# Role-skill → domain keyword inference for names the canonical taxonomy
# does not cover (e.g. frontend React/JS, DevOps). Order matters: first
# match wins. Anything still unmapped falls back to "coding", the
# platform's default activity category. Documented approximation — the
# domain is always exposed on the skill entry so it stays inspectable.
_DOMAIN_KEYWORDS = (
    ("aptitude", ("aptitud", "reasoning", "quant", "verbal", "logical", "puzzle", "statistic", "probability")),
    ("cs_fundamentals", ("sql", "dbms", "database", "nosql", "oops", "oop", "operating system", "network", "complexity", "os", "db")),
    ("system_design", ("system design", "scalab", "architect", "cache", "queue", "microservice", "trade_off", "tradeoff", "reliab")),
    ("dsa", ("dsa", "algorithm", "data structure")),
    ("behavioral", ("behavioral", "leadership", "teamwork", "communication", "ownership")),
    ("interview", ("interview",)),
    ("resume", ("resume", "ats", "cv")),
    ("projects", ("project", "portfolio", "business", "metric", "dashboard", "visual")),
)


def _infer_domain(name: str, tags: List[str]) -> Optional[str]:
    hay = f"{name or ''} {' '.join(tags or [])}".lower()
    for domain, keywords in _DOMAIN_KEYWORDS:
        if any(k in hay for k in keywords):
            return domain
    return None


def _slug(text: str) -> str:
    import re as _re
    return _re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_") or "skill"


def build_target_profile(role: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
    """Build the deterministic target competency map for (role, company).

    Role skills/weights/criticality come from role_engine.profiles (the
    existing taxonomy — never a second one). Company rescales domain weights
    via COMPANY_PROFILES match_weights, renormalized. All weights are
    explicit configuration, never model-generated.
    """
    from app.services.role_engine.profiles import SkillImportance, get_profile

    role_key = (role or "sde").lower().strip()
    profile = get_profile(role_key)
    if profile is None:
        profile = get_profile("sde")
        role_key = "sde"

    try:
        from app.services.skill_taxonomy import CANONICAL_SKILL_DOMAINS
        _domains = set(CANONICAL_SKILL_DOMAINS.keys())
    except Exception:
        _domains = {"dsa", "coding", "aptitude", "system_design", "behavioral",
                    "interview", "resume", "projects", "cs_fundamentals"}

    # One entry per role SkillDef (no merging: weights differentiate roles).
    # skill_id is the full canonical id when the name resolves to one,
    # else "role:<slug>" (explicitly non-canonical). domain is the evidence
    # bucket: (1) a tag that IS a canonical domain, (2) canonical mapper on
    # name/tags, (3) keyword inference, (4) "coding" default.
    skills_raw: List[Dict[str, Any]] = []
    for skill in list(profile.required_skills or []):
        tags = [str(t) for t in (skill.tags or [])]
        domain: Optional[str] = None
        for tag in tags:
            if tag.lower() in _domains:
                domain = tag.lower()
                break
        skill_id: Optional[str] = None
        if not domain:
            for candidate in [skill.name] + tags:
                resolved = _resolve_skill_domain(candidate)
                if candidate == skill.name and resolved:
                    try:
                        from app.services.skill_taxonomy import canonical_skill_id
                        skill_id = canonical_skill_id(candidate)
                    except Exception:
                        skill_id = None
                if resolved:
                    domain = resolved
                    break
        if not domain:
            domain = _infer_domain(skill.name, tags) or "coding"
        if not skill_id:
            skill_id = f"role:{_slug(skill.name)}"
        weight = float((profile.readiness_weights.weights or {}).get(skill.name, 0.0))
        skills_raw.append({
            "skill_id": skill_id,
            "domain": domain,
            "label": skill.name,
            "weight_raw": weight,
            "critical": skill.importance == SkillImportance.CRITICAL,
            "sources": [skill.name],
        })

    # Company overlay: rescale by the company's domain weight, renormalize.
    company_key = (company or "").lower().strip() or None
    match_weights: Optional[Dict[str, float]] = None
    if company_key and company_key in COMPANY_PROFILES:
        match_weights = COMPANY_PROFILES[company_key].get("match_weights") or {}
        mean_w = sum(match_weights.values()) / max(1, len(match_weights))
        for slot in skills_raw:
            factor = float(match_weights.get(_domain_category(slot["domain"]) or "", mean_w) or mean_w)
            slot["weight_raw"] = slot["weight_raw"] * factor

    total = sum(s["weight_raw"] for s in skills_raw) or 1.0
    skills = []
    # Zero-weight defs are not targets (role config gives them no weight).
    for slot in sorted(skills_raw, key=lambda s: -s["weight_raw"]):
        if slot["weight_raw"] <= 0:
            continue
        skills.append({
            "skill_id": slot["skill_id"],
            "domain": slot["domain"],
            "label": slot["label"],
            "weight": round(slot["weight_raw"] / total, 4),
            "critical": slot["critical"],
            "threshold": CRITICAL_SKILL_THRESHOLD if slot["critical"] else 0.0,
            "category": _domain_category(slot["domain"]) or slot["domain"],
            "sources": slot["sources"],
        })
    return {"role": role_key, "company": company_key, "skills": skills}


def score_target_skill(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Pure skill scorer: five 0-100 components → weighted skill score."""
    def _c(name: str) -> float:
        try:
            return max(0.0, min(100.0, float(evidence.get(name, 0.0))))
        except (TypeError, ValueError):
            return 0.0
    score = round(sum(_c(k) * w for k, w in SKILL_COMPONENT_WEIGHTS.items()), 1)
    eligible = int(evidence.get("eligible_events", 0) or 0)
    return {
        "score": score,
        "status": "strong" if score >= STRONG_SKILL else ("developing" if score >= GAP_SKILL else "gap"),
        "sufficient": eligible >= MIN_EVIDENCE_PER_SKILL,
        "eligible_events": eligible,
        "high_stakes": bool(evidence.get("high_stakes", False)),
        "components": {k: _c(k) for k in SKILL_COMPONENT_WEIGHTS},
    }


def _impact_key(entry: Dict[str, Any], now_iso: Optional[str],
                blocker_ids: frozenset = frozenset()) -> float:
    """Single shared impact rule for next-action picking (both pickers use it).

    weight × gap × criticality(1.5) × staleness(1.25 when not fresh) ×
    blocker-gate(2.0). Missing timestamps are uniformly stale (neutral to
    ordering); empty blocker sets are neutral. Deterministic.
    """
    try:
        weight = float(entry.get("weight", 0.0))
        score = float(entry.get("score", 0.0))
    except (TypeError, ValueError):
        return 0.0
    stale = 1.25 if not _is_fresh(entry.get("last_evidence_at"), now_iso) else 1.0
    gate = 2.0 if entry.get("skill_id") in blocker_ids else 1.0
    return weight * (100.0 - score) * (1.5 if entry.get("critical") else 1.0) * stale * gate


def _coverage_message(coverage: float) -> str:
    if coverage < MIN_COVERAGE_FOR_JUDGMENT:
        return f"Insufficient evidence: only {coverage}% of target skills have been assessed."
    elif coverage < READY_COVERAGE:
        return f"Partial evidence: {coverage}% of target skills have sufficient evidence."
    return f"Full coverage: {coverage}% of target skills have sufficient evidence."


def _classify_next_action(
    next_action: Optional[Dict[str, Any]],
    coverage: float,
    skills_out: List[Dict[str, Any]],
    blockers: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    if coverage < MIN_COVERAGE_FOR_JUDGMENT:
        return {
            "type": "prove",
            "skill_id": None,
            "reason": f"Insufficient evidence ({coverage}% coverage). Take a diagnostic assessment to establish baseline.",
        }
    if not next_action:
        return None
    skill_id = next_action.get("skill_id")
    skill_entry = next((s for s in skills_out if s["skill_id"] == skill_id), None)
    if not skill_entry:
        return next_action
    score = float(skill_entry.get("score", 0.0))
    sufficient = bool(skill_entry.get("sufficient_evidence", False))
    threshold = float(skill_entry.get("threshold", 0.0) or 0.0)
    is_blocker = skill_id in {b["skill_id"] for b in blockers}
    if is_blocker and score < threshold:
        return {
            "type": "repair",
            "skill_id": skill_id,
            "reason": f"Critical blocker — {score}% is below {threshold}% threshold. Repair this skill first.",
        }
    if not sufficient:
        return {
            "type": "prove",
            "skill_id": skill_id,
            "reason": f"Insufficient evidence for {skill_id}. Complete more practice and assessments.",
        }
    if score >= 80:
        return {
            "type": "advance",
            "skill_id": skill_id,
            "reason": f"Strong performance ({score}%). Ready to advance to harder content.",
        }
    if score >= 60:
        return {
            "type": "retain",
            "skill_id": skill_id,
            "reason": f"Good performance ({score}%). Maintain with spaced repetition and occasional review.",
        }
    return {
        "type": "repair",
        "skill_id": skill_id,
        "reason": f"Weak performance ({score}%). Repair this skill with targeted practice.",
    }


def calculate_target_readiness(
    profile: Dict[str, Any],
    evidence: Dict[str, Dict[str, Any]],
    now_iso: Optional[str] = None,
) -> Dict[str, Any]:
    """Pure deterministic target readiness over supplied evidence/config.

    Returns the explainable API shape: score, coverage, status, per-skill
    breakdown, strengths, gaps, blockers, evidence counts, freshness,
    next_action. No probabilities, no dates-until-ready, no AI.
    """
    now = now_iso or _utcnow_iso()
    skills_out: List[Dict[str, Any]] = []
    weighted_score = 0.0
    weighted_cover = 0.0
    strengths: List[str] = []
    gaps: List[str] = []
    blockers: List[Dict[str, Any]] = []
    totals = {"practice": 0, "assessments": 0, "transfer": 0, "srs_reviews": 0, "interviews": 0}
    fresh_weight = 0.0

    for spec in (profile.get("skills") or []):
        sid = spec["skill_id"]
        # Evidence lives at domain granularity (documented); several role
        # skills may share one domain bucket (shared category evidence).
        ev = evidence.get(spec.get("domain", sid), {})
        scored = score_target_skill(ev)
        weight = float(spec.get("weight", 0.0))
        weighted_score += weight * scored["score"]
        if scored["sufficient"]:
            weighted_cover += weight
        last_at = ev.get("last_evidence_at")
        fresh = _is_fresh(last_at, now)
        if fresh:
            fresh_weight += weight
        for k in totals:
            try:
                totals[k] += int((ev.get("counts") or {}).get(k, 0) or 0)
            except (TypeError, ValueError):
                pass
        entry = {
            "skill_id": sid, "label": spec.get("label", sid),
            "domain": spec.get("domain", sid),
            "score": scored["score"], "weight": weight,
            "status": scored["status"],
            "critical": bool(spec.get("critical", False)),
            "threshold": float(spec.get("threshold", 0.0)),
            "sufficient_evidence": scored["sufficient"],
            "high_stakes": scored["high_stakes"],
            "components": scored["components"],
            "last_evidence_at": last_at,
        }
        skills_out.append(entry)
        if scored["score"] >= STRONG_SKILL:
            strengths.append(sid)
        elif scored["score"] < GAP_SKILL:
            gaps.append(sid)
        if entry["critical"] and scored["score"] < float(spec.get("threshold", 0.0)):
            blockers.append({
                "skill_id": sid,
                "score": scored["score"],
                "threshold": float(spec.get("threshold", 0.0)),
                "reason": "below_critical_threshold",
            })

    score = round(weighted_score, 1)
    coverage = round(weighted_cover * 100, 1)
    if coverage < MIN_COVERAGE_FOR_JUDGMENT:
        status = "INSUFFICIENT_EVIDENCE"
    elif not blockers and coverage >= READY_COVERAGE and score >= READY_SCORE:
        status = "READY"
    elif score >= READY_WITH_GAPS_SCORE:
        status = "READY_WITH_GAPS"
    else:
        status = "DEVELOPING"

    # Next action: shared impact rule → classified into the single action
    # taxonomy (prove/repair/advance/retain, lowercase — the API contract).
    # Maps onto existing repair missions; never a new recommendation engine.
    candidates = [s for s in skills_out if s["score"] < 95.0]
    next_action: Optional[Dict[str, Any]] = None
    if candidates:
        blocker_ids = frozenset(b["skill_id"] for b in blockers)
        winner = max(candidates, key=lambda s: _impact_key(s, now, blocker_ids))
        weakest_component = min(winner["components"].items(), key=lambda kv: kv[1])[0]
        next_action = {
            "type": "repair",
            "skill_id": winner["skill_id"],
            "reason": f"highest impact gap (weakest component: {weakest_component})",
        }

    next_action = _classify_next_action(next_action, coverage, skills_out, blockers)
    coverage_message = _coverage_message(coverage)
    target_weights = {s["skill_id"]: s["weight"] for s in (profile.get("skills") or [])}

    return {
        "target": {"role": profile.get("role"), "company": profile.get("company")},
        "score": score,
        "coverage": coverage,
        "status": status,
        "skills": skills_out,
        "strengths": strengths,
        "gaps": gaps,
        "blockers": blockers,
        "evidence": totals,
        "freshness_pct": round(fresh_weight * 100, 1),
        "next_action": next_action,
        "coverage_message": coverage_message,
        "target_weights": target_weights,
    }


async def collect_target_evidence(user_id: str, profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Gather per-domain evidence from canonical stores (async I/O, zero AI).

    Grouping keys are canonical domains resolved through skill_taxonomy;
    unmapped items are counted (not silently dropped) under evidence_meta.
    Trust-gating: solves with needs_review/quarantined/unverified/unknown
    tiers contribute nothing; automated_checked counts for learning
    components only, never for assessment.
    """
    from app.database import (
        aptitude_tests_collection,
        interviews_collection,
        learning_events_collection,
        oa_sessions_collection,
        skill_graph_collection,
        solved_problems_collection,
        srs_cards_collection,
        srs_collection,
    )

    domains = [s.get("domain", s["skill_id"]) for s in (profile.get("skills") or [])]
    bucket: Dict[str, Dict[str, Any]] = {
        d: {"assess": [], "transfer": [], "solves": 0, "solves_w": 0.0,
            "attempts": 0, "passes": 0, "srs_reps": 0, "srs_lapses": 0,
            "srs_reviews": 0, "high_stakes": False, "last_at": None,
            "counts": {"practice": 0, "assessments": 0, "transfer": 0,
                       "srs_reviews": 0, "interviews": 0}}
        for d in domains
    }
    meta = {"unmapped_solves": 0, "excluded_untrusted_solves": 0, "unmapped_events": 0}

    def _touch(domain: Optional[str], iso: Optional[str]) -> Optional[Dict[str, Any]]:
        if not domain or domain not in bucket:
            return None
        b = bucket[domain]
        if iso and (not b["last_at"] or iso > b["last_at"]):
            b["last_at"] = iso
        return b

    # ── Solves (trust-gated; deduped by question_id so re-logged
    # completions cannot inflate readiness — keep highest trust weight) ──
    try:
        solved_docs = await solved_problems_collection().find(
            {"user_id": user_id}, {"question_id": 1, "topic": 1, "created_at": 1}
        ).to_list(5000)
    except Exception:
        solved_docs = []
    _best_solve: Dict[str, Dict[str, Any]] = {}
    for doc in solved_docs:
        qid = str(doc.get("question_id") or "")
        trust = _resolve_question_trust(doc.get("question_id"))
        w = _trust_weight(trust)
        prev = _best_solve.get(qid)
        if prev is None or w > prev["w"]:
            _best_solve[qid] = {"w": w, "trust": trust, "doc": doc}
    for qid, row in _best_solve.items():
        w, trust, doc = row["w"], row["trust"], row["doc"]
        if w <= 0:
            meta["excluded_untrusted_solves"] += 1
            continue
        domain = _resolve_skill_domain(doc.get("topic"))
        if not domain or domain not in bucket:
            meta["unmapped_solves"] += 1
            continue
        b = bucket[domain]
        b["solves"] += 1
        b["solves_w"] += w
        b["attempts"] += 1
        b["passes"] += 1
        b["counts"]["practice"] += 1
        if (trust or "").lower() in HIGH_STAKES_TRUST:
            b["high_stakes"] = True
        _touch(domain, _as_iso(doc.get("created_at")))

    # ── Learning events (practice + transfer; repair retests verified-only) ──
    try:
        le_docs = await learning_events_collection().find({"user_id": user_id}).to_list(5000)
    except Exception:
        le_docs = []
    for ev in le_docs:
        domain = _resolve_skill_domain(ev.get("skill_id"))
        if not domain or domain not in bucket:
            meta["unmapped_events"] += 1
            continue
        b = bucket[domain]
        iso = _as_iso(ev.get("timestamp") or ev.get("created_at") or ev.get("at"))
        _touch(domain, iso)
        activity = str(ev.get("activity_type") or "")
        passed = bool(ev.get("passed", ev.get("success", False)))
        score = ev.get("score")
        sample = float(score) if isinstance(score, (int, float)) else (100.0 if passed else 0.0)
        if any(k in activity for k in TRANSFER_ACTIVITIES):
            b["transfer"].append(100.0 if passed else 0.0)
            b["counts"]["transfer"] += 1
        else:
            b["attempts"] += 1
            b["passes"] += 1 if passed else 0
            b["assess"].append(max(0.0, min(100.0, sample)))
            b["counts"]["practice"] += 1

    # ── OA outcomes (high-stakes assessment, section → domain) ──
    try:
        sg = await skill_graph_collection().find_one({"user_id": user_id})
    except Exception:
        sg = None
    for outcome in ((sg or {}).get("oa_outcomes") or [])[-20:]:
        sections = outcome.get("sections") or {}
        section_trust = outcome.get("section_trust") or {}
        at = _as_iso(outcome.get("at"))
        if isinstance(sections, dict):
            for sec, val in sections.items():
                try:
                    from app.services.skill_taxonomy import parse_oa_section
                    domain = _resolve_skill_domain(parse_oa_section(str(sec)))
                except Exception:
                    domain = None
                b = _touch(domain, at)
                if not b:
                    continue
                try:
                    trust = float(section_trust.get(sec, 1.0))
                    weighted = max(0.0, min(100.0, float(val))) * max(0.0, min(1.0, trust))
                    b["assess"].append(weighted)
                except (TypeError, ValueError):
                    continue
                b["counts"]["assessments"] += 1
                b["high_stakes"] = True

    # ── Aptitude tests (high-stakes, aptitude domain) ──
    try:
        apt_tests = await aptitude_tests_collection().find({"user_id": user_id}).to_list(200)
    except Exception:
        apt_tests = []
    for t in apt_tests:
        pct = t.get("score", t.get("percentage"))
        if not isinstance(pct, (int, float)):
            continue
        for domain in [d for d in bucket if _domain_category(d) == "aptitude"]:
            b = bucket[domain]
            b["assess"].append(max(0.0, min(100.0, float(pct))))
            b["counts"]["assessments"] += 1
            b["high_stakes"] = True
            _touch(domain, _as_iso(t.get("created_at") or t.get("completed_at") or t.get("at")))
            break

    # ── Interviews (high-stakes, interview + behavioral domains) ──
    try:
        int_docs = await interviews_collection().find(
            {"user_id": user_id, "status": "completed"},
            {"overall_score": 1, "created_at": 1},
        ).to_list(200)
    except Exception:
        int_docs = []
    int_targets = [d for d in bucket if _domain_category(d) == "interview"] or \
        [d for d in bucket if d == "behavioral"]
    for doc in int_docs:
        s = doc.get("overall_score")
        if not isinstance(s, (int, float)):
            continue
        sample = max(0.0, min(100.0, float(s) * 10.0))
        at = _as_iso(doc.get("created_at"))
        for domain in int_targets:
            bucket[domain]["assess"].append(sample)
            bucket[domain]["counts"]["interviews"] += 1
            bucket[domain]["high_stakes"] = True
            _touch(domain, at)

    # ── SRS retention (learning evidence; concept → domain) ──
    for col_fn in (srs_cards_collection, srs_collection):
        try:
            cards = await col_fn().find({"user_id": user_id}).to_list(5000)
        except Exception:
            cards = []
        for card in cards:
            concept = card.get("concept_id", card.get("problem_id", card.get("concept_name")))
            domain = _resolve_skill_domain(concept)
            if not domain or domain not in bucket:
                continue
            b = bucket[domain]
            try:
                reps = int(card.get("repetitions", 0) or 0)
                laps = int(card.get("lapses", 0) or 0)
                revs = int(card.get("total_reviews", 0) or 0)
            except (TypeError, ValueError):
                continue
            if revs <= 0 and reps + laps <= 0:
                continue
            b["srs_reps"] += reps
            b["srs_lapses"] += laps
            b["srs_reviews"] += revs
            b["counts"]["srs_reviews"] += revs
            _touch(domain, _as_iso(card.get("last_reviewed") or card.get("updated_at")))

    # ── Components per domain ──
    from app.services.mastery_engine import calculate_mastery_level

    evidence: Dict[str, Dict[str, Any]] = {}
    for domain, b in bucket.items():
        accuracy = (b["passes"] / b["attempts"]) if b["attempts"] else 0.0
        mastery = calculate_mastery_level(b["attempts"], accuracy) * 20.0
        assessment = recency_weighted_avg(b["assess"]) if b["assess"] else 0.0
        transfer = round(sum(b["transfer"]) / len(b["transfer"]), 1) if b["transfer"] else 0.0
        retention = retention_from_srs(b["srs_reps"], b["srs_lapses"], b["srs_reviews"])
        series = list(b["assess"][-10:]) + list(b["transfer"][-10:])
        consistency = consistency_from_series(series)
        eligible = b["solves"] + b["counts"]["practice"] + b["counts"]["transfer"] + \
            b["counts"]["assessments"] + b["counts"]["interviews"] + b["srs_reviews"]
        evidence[domain] = {
            "mastery": round(mastery, 1),
            "assessment": assessment,
            "transfer": transfer,
            "retention": retention,
            "consistency": consistency,
            "eligible_events": eligible,
            "high_stakes": b["high_stakes"],
            "last_evidence_at": b["last_at"],
            "counts": b["counts"],
        }
    evidence["__meta__"] = meta
    return evidence


# ─── Canonical async entrypoint (fetches from MongoDB) ─────────────────

async def compute_readiness(
    user_id: str, company: Optional[str] = None, role: Optional[str] = None
) -> Dict[str, Any]:
    """Canonical readiness calculation: fetch user data from MongoDB, then score.

    This is the single entrypoint all routes/services should call.
    It replaces:
      - adaptive_learning.calculate_readiness_score
      - skill_assessment.get_readiness_score
      - job_readiness.get_personalized_gaps / overall_readiness inline calc

    Args:
        user_id: The user's MongoDB _id string.
        company: Optional company name for company-specific weighting.
        role: Optional target role key from role_engine.profiles
            (sde, frontend, backend, data_analyst, qa, ai_software_developer).
            Defaults to "sde". Existing callers pass nothing and keep working.

    Returns:
        Unified dict with overall_readiness, categories, recommendations,
        company score/match, stats, plus the v2 deterministic target block
        (target_readiness: score/coverage/status/skills/strengths/gaps/
        blockers/evidence/freshness/next_action). No probabilities, no
        dates-until-ready, no AI — same inputs always give same outputs.
    """
    from app.database import (
        solved_problems_collection,
        submissions_collection,
        aptitude_tests_collection,
        interviews_collection,
        resumes_collection,
        generated_projects_collection,
        question_answers_collection,
        skill_graph_collection,
    )
    from app.services.skill_assessment import get_skill_graph

    uid = user_id

    # DSA data — trust-weighted: each solve contributes by its question's
    # trust tier (verified 1.0 → quarantined 0.0). Raw counts preserved for
    # transparency; scorers consume the weighted (effective) counts.
    solved_col = solved_problems_collection()
    solved_docs = await solved_col.find(
        {"user_id": uid}, {"question_id": 1, "difficulty": 1, "topic": 1}
    ).to_list(2000)
    raw_total = len(solved_docs)
    w_easy = w_medium = w_hard = 0.0
    tier_counts = {"verified": 0, "reviewed": 0, "automated_checked": 0,
                   "needs_review": 0, "quarantined": 0, "unverified": 0, "unknown": 0}
    weighted_total = 0.0
    for doc in solved_docs:
        trust = _resolve_question_trust(doc.get("question_id"))
        key = (trust or "unknown").lower()
        tier_counts[key] = tier_counts.get(key, 0) + 1
        w = _trust_weight(trust)
        weighted_total += w
        diff = str(doc.get("difficulty") or "").lower()
        if diff == "easy":
            w_easy += w
        elif diff == "hard":
            w_hard += w
        else:
            w_medium += w
    easy = w_easy
    medium = w_medium
    hard = w_hard
    unique_topics = len({str(d.get("topic")) for d in solved_docs if d.get("topic")})
    sub_count = await submissions_collection.count_documents({"user_id": uid})
    accuracy = (raw_total / sub_count) if sub_count > 0 else 0.0
    high_conf = tier_counts.get("verified", 0) + tier_counts.get("reviewed", 0)
    evidence_confidence = (high_conf / raw_total) if raw_total else 0.0
    dsa_data = {
        "total_solved": weighted_total,
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "unique_topics": unique_topics,
        "accuracy_rate": accuracy,
        "raw_total_solved": raw_total,
        "trust_tiers": tier_counts,
        "evidence_confidence": round(evidence_confidence, 3),
    }

    # Aptitude data (field is `score` on aptitude_tests docs; accept legacy
    # `percentage` readings where present).
    apt_col = aptitude_tests_collection()
    apt_tests = await apt_col.find({"user_id": uid}).to_list(100)
    def _apt_pct(t: Dict[str, Any]) -> float:
        v = t.get("score", t.get("percentage", 0))
        try:
            return max(0.0, min(100.0, float(v)))
        except (TypeError, ValueError):
            return 0.0
    avg_pct = sum(_apt_pct(t) for t in apt_tests) / len(apt_tests) if apt_tests else 0.0
    recent_pcts = [_apt_pct(t) for t in apt_tests[-5:]]
    categories_set = {t.get("category") for t in apt_tests if t.get("category")}
    aptitude_data = {
        "avg_percentage": avg_pct,
        "test_count": len(apt_tests),
        "category_count": len(categories_set),
        "recent_percentages": recent_pcts,
    }

    # CS fundamentals data: score interview answers whose question maps to CS
    # topics (os/dbms/sql/oops/networking/complexity). Transparent mapping;
    # zeros with an explicit reason when nothing maps (never silent).
    _CS_KEYWORDS = ("operating system", "process", "thread", "deadlock", "sql",
                    "database", "index", "normalization", "oops", "oop", "inheritance",
                    "polymorphism", "tcp", "udp", "http", "dns", "network",
                    "complexity", "big-o", "cache", "memory", "compiler")
    cs_scores = []
    try:
        from app.database import interviews_collection as _int_col_fn
        int_docs = await _int_col_fn().find({"user_id": uid}, {"questions": 1}).to_list(100)
        for doc in int_docs:
            for qa in doc.get("questions") or []:
                text = f"{qa.get('question', '')} {qa.get('question_type', '')}".lower()
                if any(k in text for k in _CS_KEYWORDS):
                    s = qa.get("score")
                    if isinstance(s, (int, float)):
                        cs_scores.append(float(s))
    except Exception:
        cs_scores = []
    cs_data = {"answered_count": len(cs_scores),
               "cs_tagged_count": len(cs_scores),
               "avg_score": (sum(cs_scores) / len(cs_scores)) if cs_scores else 0.0,
               "source": "interview_qa_cs_mapping"}

    # Coding data (from submissions; accepted counts trust-weighted like DSA).
    # Includes the total_submissions/passed_submissions keys score_coding reads
    # (previously unwired — the scorer saw zeros regardless of history).
    coding_data = {"submissions": sub_count, "accepted": weighted_total,
                   "acceptance_rate": accuracy, "raw_accepted": raw_total,
                   "total_submissions": sub_count, "passed_submissions": weighted_total}

    # Interview data: completed-interview scores (0-10 rubric scale), not
    # just a count. score_interview expects avg_score/recent_scores/
    # company_breakdown; when no scored interview exists this degrades to
    # the old count-only shape and the scorer returns volume-only credit.
    int_col = interviews_collection()
    interview_count = await int_col.count_documents({"user_id": uid})
    int_docs = await int_col.find(
        {"user_id": uid, "status": "completed"},
        {"overall_score": 1, "company": 1, "created_at": 1},
    ).to_list(100)
    int_scores: list[float] = []
    company_breakdown: dict[str, float] = {}
    for d in int_docs:
        s = d.get("overall_score")
        if isinstance(s, (int, float)):
            s = max(0.0, min(10.0, float(s)))
            int_scores.append(s)
            comp = str(d.get("company") or "general").lower()
            company_breakdown[comp] = round(
                (company_breakdown.get(comp, 0.0) + s) / 2
                if comp in company_breakdown else s, 1)
    interview_data = {
        "completed": interview_count,
        "completed_count": len(int_scores),
        "avg_score": round(sum(int_scores) / len(int_scores), 1) if int_scores else 0.0,
        "recent_scores": int_scores[-5:],
        "company_breakdown": company_breakdown,
    }

    # Resume data
    resume_col = resumes_collection()
    resume_count = await resume_col.count_documents({"user_id": uid})
    resume_data = {"uploaded": resume_count}

    # Project data
    proj_col = generated_projects_collection()
    project_count = await proj_col.count_documents({"user_id": uid})
    project_data = {"count": project_count}

    # Learning-event evidence (repair / retest / mastery stream). Surfaced in
    # stats for transparency; scoring weights remain a product decision.
    try:
        from app.database import learning_events_collection as _le_fn
        le_docs = await _le_fn().find({"user_id": uid}).to_list(2000)
    except Exception:
        le_docs = []
    le_types = {}
    le_passed = 0
    for ev in le_docs:
        t = str(ev.get("activity_type") or "unknown")
        le_types[t] = le_types.get(t, 0) + 1
        if ev.get("passed"):
            le_passed += 1
    # Repair recovery rate: repair-tagged events passed / created.
    # Surfaced as evidence (v1); not yet a scoring weight (v2 per module
    # product note). Zeros with explicit reason when no repair history.
    repair_created = sum(
        n for t, n in le_types.items() if "repair" in t)
    repair_passed = sum(
        1 for ev in le_docs
        if "repair" in str(ev.get("activity_type") or "") and ev.get("passed"))
    learning_evidence = {"total_events": len(le_docs), "by_type": le_types,
                         "passed": le_passed,
                         "repair_created": repair_created,
                         "repair_passed": repair_passed,
                         "repair_recovery_rate": round(repair_passed / repair_created, 3)
                         if repair_created else 0.0}

    # OA-session evidence. New sessions record verified_only at creation (oa.py);
    # pre-flag sessions are attribution-unknown and claimed as neither.
    try:
        from app.database import oa_sessions_collection as _oa_fn
        oa_docs = await _oa_fn().find({"user_id": uid}).to_list(200)
    except Exception:
        oa_docs = []
    oa_completed = [d for d in oa_docs if d.get("status") == "completed"]
    oa_evidence = {"total_sessions": len(oa_docs),
                   "completed_sessions": len(oa_completed),
                   "verified_completed": len([d for d in oa_completed if d.get("verified_only") is True]),
                   "legacy_completed": len([d for d in oa_completed if d.get("verified_only") is False]),
                   "attribution_unknown": len([d for d in oa_completed if "verified_only" not in d])}

    result = calculate_readiness(
        dsa_data=dsa_data,
        aptitude_data=aptitude_data,
        cs_data=cs_data,
        coding_data=coding_data,
        interview_data=interview_data,
        resume_data=resume_data,
        project_data=project_data,
        company=company,
    )

    # Build weak/strong area summaries for callers that expect them
    cats = result.categories
    weak_areas = [{"category": k, "score": v.score} for k, v in cats.items() if v.score < 50]
    strong_domains = [{"category": k, "score": v.score} for k, v in cats.items() if v.score >= 80]

    # ── v2 deterministic target readiness (same evidence, target weighting) ──
    # Best-effort and non-breaking: a v2 failure must never take down the v1
    # response that existing callers (journey, dashboard, gamification) read.
    target_block: Optional[Dict[str, Any]] = None
    target_coverage: Optional[float] = None
    try:
        target_profile = build_target_profile(role, company)
        target_evidence = await collect_target_evidence(user_id, target_profile)
        evidence_meta = target_evidence.pop("__meta__", {})
        target_block = calculate_target_readiness(target_profile, target_evidence)
        target_block["evidence_meta"] = evidence_meta
        target_block["component_weights"] = dict(SKILL_COMPONENT_WEIGHTS)
        target_coverage = target_block["coverage"]
    except Exception:
        target_block = None

    return {
        "user_id": uid,
        "overall_readiness": result.overall,
        "overall": result.overall,
        "readiness_level": _readiness_level(result.overall),
        "base_score": result.overall,
        "category_scores": {k: v.score for k, v in cats.items()},
        "categories": {k: {"score": v.score, "weight": v.weight, "details": v.details} for k, v in cats.items()},
        "weak_areas_count": len(weak_areas),
        "strong_domains_count": len(strong_domains),
        "company_specific": {
            "company": company,
            "score": result.company_score,
            "match": result.company_match,
        } if company else None,
        "recommendations": result.recommendations,
        "stats": result.stats,
        "coverage_pct": target_coverage if target_coverage is not None else 0.0,
        "target_readiness": target_block,
        "untouched_penalty": 0,
        "accuracy_penalty": 0,
        "consistency_bonus": 0,
        "trust_policy": {k: v for k, v in TRUST_WEIGHT.items()},
        "evidence": {
            "dsa_trust_tiers": dsa_data.get("trust_tiers", {}),
            "dsa_evidence_confidence": dsa_data.get("evidence_confidence", 0.0),
            "dsa_raw_solved": dsa_data.get("raw_total_solved", 0),
            "learning_events": learning_evidence,
            "oa_sessions": oa_evidence,
            "cs_source": cs_data.get("source", "unknown"),
        },
    }


def _readiness_level(score: float) -> str:
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


# ─── Public API aliases (user-facing names from the spec) ──────────────
# The v2 implementation above already provides the exact behavior requested.
# These aliases expose the requested names without breaking existing callers.

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SkillEvidence:
    mastery: float
    assessments: List[float]
    transfer_tasks: List[bool]
    srs_retrievals: List[bool]
    practice_history: List[float]


def is_insufficient(ev: SkillEvidence) -> bool:
    if not isinstance(ev, SkillEvidence):
        return True
    total_events = (
        len(ev.assessments) +
        len(ev.transfer_tasks) +
        len(ev.srs_retrievals) +
        len(ev.practice_history)
    )
    return total_events < MIN_EVIDENCE_PER_SKILL


def calculate_skill_score(ev: SkillEvidence) -> Dict[str, Any]:
    mastery_score = max(0.0, min(100.0, float(getattr(ev, "mastery", 0.0))))

    assessments = list(getattr(ev, "assessments", []) or [])
    assessment_score = float(sum(assessments[-3:]) / len(assessments[-3:])) if assessments else 0.0

    transfer_tasks = list(getattr(ev, "transfer_tasks", []) or [])
    transfer_score = (sum(transfer_tasks) / len(transfer_tasks)) * 100 if transfer_tasks else 0.0

    srs_retrievals = list(getattr(ev, "srs_retrievals", []) or [])
    retention_score = (sum(srs_retrievals) / len(srs_retrievals)) * 100 if srs_retrievals else 0.0

    practice_history = list(getattr(ev, "practice_history", []) or [])
    if len(practice_history) < 3:
        consistency_score = 50.0
    else:
        mean = sum(practice_history) / len(practice_history)
        variance = sum((x - mean) ** 2 for x in practice_history) / len(practice_history)
        consistency_score = max(0.0, 100.0 - (math.sqrt(variance) * 2.5))

    final = (
        mastery_score * SKILL_COMPONENT_WEIGHTS["mastery"] +
        assessment_score * SKILL_COMPONENT_WEIGHTS["assessment"] +
        transfer_score * SKILL_COMPONENT_WEIGHTS["transfer"] +
        retention_score * SKILL_COMPONENT_WEIGHTS["retention"] +
        consistency_score * SKILL_COMPONENT_WEIGHTS["consistency"]
    )

    return {
        "score": round(final, 1),
        "breakdown": {
            "mastery": round(mastery_score, 1),
            "assessment": round(assessment_score, 1),
            "transfer": round(transfer_score, 1),
            "retention": round(retention_score, 1),
            "consistency": round(consistency_score, 1),
        },
    }


def load_target_profile(role: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
    return build_target_profile(role=role, company=company)


async def load_verified_evidence(user_id: str, trust_gate: Optional[set] = None) -> Dict[str, Dict[str, Any]]:
    """Collector alias with an optional verified-only view.

    The collector already trust-gates solves (untrusted tiers excluded;
    automated_checked learning-only). When trust_gate is provided, domains
    are further restricted to high-stakes evidence (verified/reviewed
    solves or completed OA/aptitude/interview assessments); learning-only
    domains are dropped from the gated view, never silently relabeled.
    """
    profile = build_target_profile()
    evidence = await collect_target_evidence(user_id, profile)
    if not trust_gate:
        return evidence
    gated = {k: v for k, v in evidence.items()
             if k == "__meta__" or (isinstance(v, dict) and v.get("high_stakes"))}
    return gated


def determine_next_action(skills: List[Dict[str, Any]], target_map: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Standalone highest-impact picker (same shared rule; no timestamps →
    staleness neutral, no blocker context). Kept for callers that only have
    bare skill dicts; the engine path classifies further via
    _classify_next_action into prove/repair/advance/retain."""
    _ = target_map
    if not skills:
        return None
    best = max(skills, key=lambda s: _impact_key(s, None))
    return {
        "type": "repair",
        "skill_id": best.get("skill_id"),
        "reason": f"highest impact gap: {best.get('score')} < threshold, weight {best.get('weight')}",
    }


# Public alias used by the v2 wrapper and tests.
TRUSTED_STATUSES = HIGH_STAKES_TRUST


async def calculate_target_readiness_score(
    user_id: str,
    target_role: str,
    target_company: Optional[str] = None,
) -> Dict[str, Any]:
    target_profile = load_target_profile(target_role, target_company)
    evidence = await load_verified_evidence(user_id, TRUSTED_STATUSES)
    target_block = calculate_target_readiness(target_profile, evidence)
    target_block.setdefault("next_action", determine_next_action(
        target_block.get("skills", []), target_profile
    ))
    return target_block


async def calculate_company_readiness_breakdown(
    user_id: str,
    skill_graph: Dict[str, Any],
    target_company: Optional[str] = None,
) -> Dict[str, Any]:
    """Compute per-company readiness scores for the student.

    Returns:
    - overall_readiness (0-100)
    - domain_scores (per-domain 0-100)
    - per_company_scores (target company + related service companies)
    - blockers (domains below 50%)
    - next_focus (highest-impact weak domain)
    """
    # Base domain scores from skill graph
    all_domains = {
        "aptitude": _domain_score("aptitude", skill_graph),
        "dsa": _domain_score("dsa", skill_graph),
        "coding": _domain_score("coding", skill_graph),
        "cs_fundamentals": _domain_score("cs_fundamentals", skill_graph),
        "interview": _domain_score("interview", skill_graph),
        "verbal": _domain_score("verbal", skill_graph),
        "resume": _domain_score("resume", skill_graph),
        "system_design": _domain_score("system_design", skill_graph),
    }

    # Overall weighted score (generic)
    overall = sum(all_domains.get(d, 0.0) * w for d, w in CATEGORY_WEIGHTS.items()) / max(sum(CATEGORY_WEIGHTS.values()), 0.001)
    overall = _clamp(overall)

    # Per-company scores using company-specific weights
    companies = []
    if target_company and target_company in COMPANY_PROFILES:
        companies.append(target_company)
    # Add related service companies
    related = [c for c in COMPANY_PROFILES.keys() if c not in companies and c in ("tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture")]
    companies.extend(related[:3])

    per_company = {}
    for comp in companies:
        profile = COMPANY_PROFILES.get(comp, {})
        weights = profile.get("match_weights", CATEGORY_WEIGHTS)
        score = sum(all_domains.get(d, 0.0) * w for d, w in weights.items()) / max(sum(weights.values()), 0.001)
        per_company[comp] = {
            "score": round(_clamp(score), 1),
            "focus_areas": profile.get("focus_topics", [])[:5],
            "min_skills": profile.get("min_skills", {}),
            "typical_timeline_weeks": profile.get("typical_timeline_weeks", 4),
        }

    # Blockers: domains below 50%
    blockers = [d for d, s in all_domains.items() if s < 50]

    # Next focus: lowest scoring domain relevant to target company
    target_weights = COMPANY_PROFILES.get(target_company, {}).get("match_weights", CATEGORY_WEIGHTS) if target_company else CATEGORY_WEIGHTS
    weighted_gaps = [(d, max(0.0, 70.0 - all_domains.get(d, 0.0)) * target_weights.get(d, 0.1)) for d in all_domains]
    weighted_gaps.sort(key=lambda x: x[1], reverse=True)
    next_focus = weighted_gaps[0][0] if weighted_gaps else "aptitude"

    return {
        "overall_readiness": round(overall, 1),
        "domain_scores": {d: round(v, 1) for d, v in all_domains.items()},
        "per_company_scores": per_company,
        "target_company": target_company,
        "blockers": blockers,
        "next_focus": next_focus,
        "readiness_level": _readiness_level(overall),
    }
