"""Company Preparation Layer.

Combines role + company + assessment into a targeted preparation journey.

Example: Software Engineer + TCS -> TCS Placement Journey
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CompanyStage(BaseModel):
    """One stage in a company preparation journey."""
    order: int
    title: str
    description: str
    skills: List[str] = Field(default_factory=list)
    exercise_ids: List[str] = Field(default_factory=list)
    quiz_ids: List[str] = Field(default_factory=list)
    assessment_type: str = "quiz"
    passing_score: float = 70.0


class CompanyJourney(BaseModel):
    """A complete company-specific preparation journey."""
    company_id: str
    role_id: str
    stages: List[CompanyStage] = Field(default_factory=list)
    total_hours: int = 0


# Company journey definitions
COMPANY_JOURNEYS: Dict[str, Dict[str, CompanyJourney]] = {
    "sde": {
        "tcs": CompanyJourney(
            company_id="tcs", role_id="sde",
            stages=[
                CompanyStage(order=1, title="Programming Foundations",
                    description="Variables, conditionals, loops, functions",
                    skills=["variables", "conditionals", "loops", "functions"]),
                CompanyStage(order=2, title="Aptitude and Reasoning",
                    description="Quantitative, logical, verbal reasoning",
                    skills=["aptitude"]),
                CompanyStage(order=3, title="Coding Patterns",
                    description="Arrays, strings, sorting, searching",
                    skills=["arrays", "strings", "sorting"]),
                CompanyStage(order=4, title="TCS Coding Assessment",
                    description="Timed coding round with hidden tests",
                    skills=["dsa", "coding"], assessment_type="mock_oa"),
                CompanyStage(order=5, title="Technical Interview",
                    description="DSA + system design questions",
                    skills=["dsa", "system_design"], assessment_type="ai_interview"),
                CompanyStage(order=6, title="HR and Behavioral",
                    description="STAR method + leadership principles",
                    skills=["behavioral"], assessment_type="ai_interview"),
            ],
            total_hours=40,
        ),
        "amazon": CompanyJourney(
            company_id="amazon", role_id="sde",
            stages=[
                CompanyStage(order=1, title="Leadership Principles",
                    description="Amazons 16 LPs with behavioral examples",
                    skills=["behavioral"]),
                CompanyStage(order=2, title="Data Structures",
                    description="Arrays, trees, graphs, hash maps",
                    skills=["arrays", "trees", "graphs"]),
                CompanyStage(order=3, title="Algorithms",
                    description="Sorting, searching, DP, greedy",
                    skills=["sorting", "dp", "greedy"]),
                CompanyStage(order=4, title="System Design",
                    description="Design scalable systems",
                    skills=["system_design"]),
                CompanyStage(order=5, title="Online Assessment",
                    description="2 coding problems in 90 minutes",
                    skills=["dsa", "coding"], assessment_type="mock_oa"),
                CompanyStage(order=6, title="Technical Phone Screen",
                    description="1 hour coding + behavioral",
                    skills=["dsa", "behavioral"], assessment_type="ai_interview"),
                CompanyStage(order=7, title="Onsite Loop",
                    description="4-5 rounds: coding, design, behavioral",
                    skills=["dsa", "system_design", "behavioral"], assessment_type="ai_interview"),
            ],
            total_hours=60,
        ),
    },
    "data_scientist": {
        "meta": CompanyJourney(
            company_id="meta", role_id="data_scientist",
            stages=[
                CompanyStage(order=1, title="SQL Fundamentals",
                    description="Joins, aggregations, window functions",
                    skills=["sql"]),
                CompanyStage(order=2, title="Product Sense",
                    description="Metrics, experiments, trade-offs",
                    skills=["product_sense", "ab_testing"]),
                CompanyStage(order=3, title="Statistics",
                    description="Hypothesis testing, distributions",
                    skills=["statistics", "probability"]),
                CompanyStage(order=4, title="Python for Data",
                    description="Pandas, NumPy, data manipulation",
                    skills=["python", "pandas"]),
                CompanyStage(order=5, title="Technical Screen",
                    description="SQL + product case study",
                    skills=["sql", "product_sense"], assessment_type="mock_oa"),
                CompanyStage(order=6, title="Onsite",
                    description="SQL, product sense, behavioral",
                    skills=["sql", "product_sense", "behavioral"], assessment_type="ai_interview"),
            ],
            total_hours=40,
        ),
    },
    "devops": {
        "google": CompanyJourney(
            company_id="google", role_id="devops",
            stages=[
                CompanyStage(order=1, title="Linux and Scripting",
                    description="Bash, Python, automation",
                    skills=["linux", "scripting"]),
                CompanyStage(order=2, title="Networking",
                    description="TCP/IP, DNS, load balancing",
                    skills=["networking"]),
                CompanyStage(order=3, title="Infrastructure",
                    description="Docker, Kubernetes, Terraform",
                    skills=["docker", "kubernetes", "terraform"]),
                CompanyStage(order=4, title="Monitoring",
                    description="Observability, alerting, SLOs",
                    skills=["monitoring", "observability"]),
                CompanyStage(order=5, title="Technical Interview",
                    description="System design + troubleshooting",
                    skills=["system_design", "troubleshooting"], assessment_type="ai_interview"),
                CompanyStage(order=6, title="Onsite",
                    description="Coding, system design, behavioral",
                    skills=["coding", "system_design", "behavioral"], assessment_type="ai_interview"),
            ],
            total_hours=50,
        ),
    },
}


def get_company_journey(role_id: str, company_id: str) -> Optional[CompanyJourney]:
    """Get a company-specific journey for a role."""
    return COMPANY_JOURNEYS.get(role_id, {}).get(company_id)


def get_companies_for_role(role_id: str) -> List[str]:
    """Get list of available companies for a role."""
    return list(COMPANY_JOURNEYS.get(role_id, {}).keys())


def get_all_companies() -> Dict[str, List[str]]:
    """Get all company mappings."""
    return {role: list(companies.keys()) for role, companies in COMPANY_JOURNEYS.items()}


async def evaluate_stage(user_id: str, stage: CompanyStage, responses: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate a student's performance on a company stage."""
    score = 0.0
    feedback = []
    weaknesses = []

    if stage.assessment_type == "quiz":
        # Grade quiz responses
        correct = sum(1 for q in responses.get("answers", []) if q.get("correct"))
        total = len(responses.get("answers", []))
        score = (correct / max(total, 1)) * 100
        if score < stage.passing_score:
            weaknesses = stage.skills

    elif stage.assessment_type == "mock_oa":
        # Grade coding assessment
        problems_solved = responses.get("problems_solved", 0)
        total_problems = responses.get("total_problems", 1)
        score = (problems_solved / total_problems) * 100
        if score < stage.passing_score:
            weaknesses = stage.skills

    elif stage.assessment_type == "ai_interview":
        # AI interview evaluation
        score = responses.get("overall_score", 0)
        weaknesses = responses.get("weaknesses", stage.skills)

    passed = score >= stage.passing_score

    return {
        "score": score,
        "passed": passed,
        "feedback": feedback,
        "weaknesses": weaknesses,
        "next_action": "advance" if passed else "repair",
        "repair_skills": weaknesses if not passed else [],
    }
