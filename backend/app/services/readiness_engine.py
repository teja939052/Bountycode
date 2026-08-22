"""Placement Readiness Score Engine — pure deterministic calculation, NO AI.

Calculates a 0-100 readiness score from actual user performance data across
7 categories: dsa, aptitude, cs_fundamentals, coding, interview, resume,
and projects. Each category is scored independently and combined via a
weighted average. Company-specific readiness applies a match factor.

All functions are pure and testable without a database — they accept
pre-fetched data dicts and return structured results.
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
        "match_weights": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "resume": 0.03, "projects": 0.02},
    },
    "wipro": {
        "min_solved": 40, "min_medium": 15, "min_hard": 3,
        "min_skills": {"dsa": 40, "aptitude": 50, "verbal": 40},
        "focus_topics": ["Arrays", "Strings", "Basic Algorithms", "Aptitude"],
        "interview_rounds": ["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        "typical_timeline_weeks": 3,
        "match_weights": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "resume": 0.03, "projects": 0.02},
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
