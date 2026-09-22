"""Company-aware roadmap generator.

Given a target company, current skill state, and optional timeline,
returns an ordered list of missions/patterns to practice with
day-by-day allocation. No AI involved — deterministic curriculum
selection from the verified in-memory question store and curriculum.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Mission:
    """One daily contract item."""
    title: str
    category: str
    topic: str
    pattern: str
    minutes: int
    question_count: int
    difficulty: str
    company_relevance: str
    reason: str


@dataclass
class Roadmap:
    """Complete 30-day roadmap for a target company."""
    target_company: str
    target_role: str
    timeline_days: int
    daily_minutes: int
    overall_readiness: float
    domain_scores: Dict[str, float]
    missions: List[Mission]
    milestones: List[Dict[str, Any]]
    next_focus: str


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def _company_focus(company_id: str) -> Dict[str, float]:
    """Return domain weight emphasis for a company."""
    profiles: Dict[str, Dict[str, float]] = {
        "tcs": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "verbal": 0.05},
        "infosys": {"aptitude": 0.32, "dsa": 0.23, "cs_fundamentals": 0.13, "coding": 0.15, "interview": 0.12, "verbal": 0.05},
        "wipro": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "verbal": 0.05},
        "cognizant": {"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.10, "coding": 0.15, "interview": 0.15, "verbal": 0.05},
        "capgemini": {"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.15, "coding": 0.20, "interview": 0.12, "verbal": 0.08},
        "accenture": {"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.10, "coding": 0.15, "interview": 0.20, "verbal": 0.10},
        "hcl": {"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "verbal": 0.08},
        "tech_mahindra": {"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "verbal": 0.08},
        "lti_mindtree": {"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "verbal": 0.08},
        "mphasis": {"aptitude": 0.28, "dsa": 0.20, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.17, "verbal": 0.08},
        "google": {"dsa": 0.40, "coding": 0.25, "system_design": 0.15, "interview": 0.10, "aptitude": 0.05, "cs_fundamentals": 0.05},
        "amazon": {"dsa": 0.30, "interview": 0.25, "coding": 0.20, "system_design": 0.10, "aptitude": 0.05, "cs_fundamentals": 0.05, "behavioral": 0.05},
        "microsoft": {"dsa": 0.35, "coding": 0.25, "interview": 0.20, "system_design": 0.10, "aptitude": 0.05, "cs_fundamentals": 0.05},
        "meta": {"dsa": 0.35, "coding": 0.30, "system_design": 0.15, "interview": 0.10, "cs_fundamentals": 0.05, "aptitude": 0.05},
        "uber": {"dsa": 0.35, "coding": 0.25, "system_design": 0.20, "interview": 0.10, "aptitude": 0.05, "cs_fundamentals": 0.05},
        "apple": {"dsa": 0.30, "coding": 0.25, "system_design": 0.20, "interview": 0.15, "cs_fundamentals": 0.05, "aptitude": 0.05},
    }
    return profiles.get(company_id.lower(), {"aptitude": 0.20, "dsa": 0.30, "cs_fundamentals": 0.10, "coding": 0.25, "interview": 0.10, "verbal": 0.05})


def _domain_score(domain: str, skill_graph: Dict[str, Any]) -> float:
    cat = skill_graph.get("categories", {}).get(domain, {})
    if isinstance(cat, dict):
        return float(cat.get("score", 0.0))
    return float(cat) if isinstance(cat, (int, float)) else 0.0


def _weakest_domains(skill_graph: Dict[str, Any], focus: Dict[str, float], count: int = 3) -> List[str]:
    """Return domains with lowest score *and* high company relevance."""
    scored = []
    for domain, weight in focus.items():
        s = _domain_score(domain, skill_graph)
        # Blend current score gap with company relevance
        gap = max(0.0, 70.0 - s)
        scored.append((domain, gap * weight, s))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [d for d, _, _ in scored[:count]]


def _pattern_for_domain(domain: str) -> List[str]:
    mapping = {
        "aptitude": ["Percentages", "Ratio & Proportion", "Time & Work", "Profit/Loss", "Averages", "Number Series", "Data Interpretation"],
        "verbal": ["Reading Comprehension", "Grammar", "Vocabulary", "Sentence Correction", "Para Jumbles"],
        "dsa": ["Arrays", "Strings", "Linked Lists", "Trees", "Graphs", "Dynamic Programming", "Sorting", "Searching", "Stacks & Queues", "Hashing"],
        "coding": ["Basic Programming", "Loop Tracing", "Conditionals", "Functions", "Recursion", "OOP Basics"],
        "cs_fundamentals": ["OS Basics", "DBMS Basics", "Networking Basics", "OOP Concepts", "SQL Queries"],
        "interview": ["Behavioral", "STAR Method", "HR Questions", "Communication"],
        "system_design": ["Scalability", "API Design", "Database Design", "Caching", "Load Balancing"],
        "behavioral": ["Leadership Principles", "STAR Stories", "Conflict Resolution", "Ownership Examples"],
    }
    return mapping.get(domain, [domain.replace("_", " ").title()])


def _minutes_for_domain(domain: str) -> int:
    return {
        "aptitude": 30,
        "verbal": 20,
        "dsa": 40,
        "coding": 30,
        "cs_fundamentals": 25,
        "interview": 20,
        "system_design": 45,
        "behavioral": 20,
    }.get(domain, 25)


def _difficulty_for_score(score: float) -> str:
    if score < 40:
        return "easy"
    if score < 70:
        return "medium"
    return "hard"


def generate_roadmap(
    target_company: str,
    skill_graph: Dict[str, Any],
    timeline_days: int = 30,
    daily_minutes: int = 60,
    target_role: str = "sde",
) -> Roadmap:
    """Generate a personalized 30-day roadmap."""
    focus = _company_focus(target_company)
    domain_scores = {d: _domain_score(d, skill_graph) for d in focus}
    overall = sum(domain_scores.get(d, 0.0) * w for d, w in focus.items()) / max(sum(focus.values()), 0.001)
    overall = _clamp(overall)

    weak = _weakest_domains(skill_graph, focus, count=min(5, len(focus)))
    missions: List[Mission] = []

    # Distribute days across weak domains weighted by gap * company relevance
    weights = []
    for domain in weak:
        gap = max(0.0, 70.0 - _domain_score(domain, skill_graph))
        weights.append(max(0.01, gap * focus.get(domain, 0.1)))
    total_w = sum(weights) or 1.0
    days_per_domain = [max(1, round(timeline_days * w / total_w)) for w in weights]
    # Trim to timeline
    days_per_domain = [min(d, timeline_days) for d in days_per_domain]

    day = 1
    for domain, days in zip(weak, days_per_domain):
        patterns = _pattern_for_domain(domain)
        base_min = _minutes_for_domain(domain)
        score = domain_scores.get(domain, 0.0)
        diff = _difficulty_for_score(score)
        for i in range(min(days, timeline_days - day + 1)):
            pattern = patterns[i % len(patterns)]
            missions.append(Mission(
                title=f"{domain.title()}: {pattern}",
                category=domain,
                topic=pattern,
                pattern=pattern,
                minutes=base_min,
                question_count=max(3, base_min // 5),
                difficulty=diff,
                company_relevance=f"{target_company.upper()} focus",
                reason=f"Weakness repair: {domain} at {round(score)}% readiness",
            ))
            day += 1
            if day > timeline_days:
                break
        if day > timeline_days:
            break

    # Backfill if under-filled
    while len(missions) < timeline_days:
        domain = weak[len(missions) % len(weak)] if weak else "aptitude"
        pattern = _pattern_for_domain(domain)[0]
        missions.append(Mission(
            title=f"{domain.title()}: {pattern}",
            category=domain,
            topic=pattern,
            pattern=pattern,
            minutes=_minutes_for_domain(domain),
            question_count=3,
            difficulty="medium",
            company_relevance=f"{target_company.upper()} focus",
            reason=f"Weakness repair: {domain}",
        ))

    missions = missions[:timeline_days]

    milestones = [
        {"day": timeline_days // 4, "readiness": 50, "label": f"Day {timeline_days // 4}: 50% readiness target"},
        {"day": timeline_days // 2, "readiness": 65, "label": f"Day {timeline_days // 2}: 65% readiness target"},
        {"day": (timeline_days * 3) // 4, "readiness": 80, "label": f"Day {(timeline_days * 3) // 4}: 80% readiness target"},
        {"day": timeline_days, "readiness": 90, "label": f"Day {timeline_days}: 90%+ readiness — ready for OA!"},
    ]

    next_focus = weak[0] if weak else "aptitude"

    return Roadmap(
        target_company=target_company,
        target_role=target_role,
        timeline_days=timeline_days,
        daily_minutes=daily_minutes,
        overall_readiness=round(overall, 1),
        domain_scores={d: round(v, 1) for d, v in domain_scores.items()},
        missions=missions,
        milestones=milestones,
        next_focus=next_focus,
    )
