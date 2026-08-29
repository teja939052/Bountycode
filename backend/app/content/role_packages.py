"""Role-based learning packages.

Each role (SDE, Data Scientist, ML Engineer, DevOps, etc.) gets a curated
path through the 12 worlds. Not every role needs every world — but all of
them need Foundations (World 1).

This is a *configuration* layer, not a content layer. The worlds and lessons
already exist. This just maps roles → recommended paths.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RolePath(BaseModel):
    """A role's recommended learning path."""
    world_id: str
    reason: str  # why this role needs this world
    emphasis: List[str] = Field(default_factory=list)  # topics to emphasize


class RolePackage(BaseModel):
    """A complete role-based learning package."""
    id: str
    name: str
    icon: str = "💼"
    description: str = ""
    # The ordered list of worlds this role should complete
    path: List[RolePath] = Field(default_factory=list)
    # Key skills this role develops
    skills: List[str] = Field(default_factory=list)
    # Target companies / roles
    targets: List[str] = Field(default_factory=list)
    # Estimated hours to complete
    estimated_hours: int = 0


# ═══════════════════════════════════════════════════════════════════
# SDE (Software Development Engineer)
# ═══════════════════════════════════════════════════════════════════

SDE_PACKAGE = RolePackage(
    id="sde",
    name="Software Development Engineer",
    icon="💻",
    description="Build systems that scale. Full backend + algorithms + system design.",
    path=[
        RolePath(world_id="foundations", reason="Every SDE starts here — variables, logic, data structures.", emphasis=["variables", "conditionals", "loops", "functions", "collections"]),
        RolePath(world_id="problem_solver", reason="DSA is the gateway to every top company interview.", emphasis=["arrays", "trees", "graphs", "dp", "two_pointers"]),
        RolePath(world_id="build_systems", reason="SDEs build APIs and databases daily.", emphasis=["rest", "sql", "database_design"]),
        RolePath(world_id="software_engineering", reason="Git and testing are non-negotiable professional skills.", emphasis=["git", "testing", "code_review"]),
        RolePath(world_id="under_pressure", reason="OA and timed rounds filter candidates.", emphasis=["timed_coding", "pattern_recognition"]),
        RolePath(world_id="hiring_arena", reason="The final round: coding + system design.", emphasis=["coding_interviews", "system_design"]),
        RolePath(world_id="production", reason="Senior SDEs own reliability and scaling.", emphasis=["monitoring", "circuit_breaker", "scaling"]),
        RolePath(world_id="projects", reason="Ship something real for your portfolio.", emphasis=["api_design", "database", "caching", "deployment"]),
    ],
    skills=["Python/Java/C++", "DSA", "System Design", "APIs", "Databases", "Git", "Testing", "Reliability"],
    targets=["Google", "Amazon", "Microsoft", "Meta", "Flipkart", "Stripe", "Backend roles"],
    estimated_hours=120,
)


# ═══════════════════════════════════════════════════════════════════
# Data Scientist
# ═══════════════════════════════════════════════════════════════════

DATA_SCIENTIST_PACKAGE = RolePackage(
    id="data_scientist",
    name="Data Scientist",
    icon="📊",
    description="Extract insights from data. Statistics + SQL + Python + storytelling.",
    path=[
        RolePath(world_id="foundations", reason="Python fundamentals for data work.", emphasis=["variables", "collections", "functions"]),
        RolePath(world_id="work_with_data", reason="SQL and analytics are the daily tools.", emphasis=["sql", "aggregation", "window_functions", "etl"]),
        RolePath(world_id="build_systems", reason="Data pipelines need APIs and databases.", emphasis=["sql", "schema_design"]),
        RolePath(world_id="software_engineering", reason="Reproducible code needs version control.", emphasis=["git", "testing"]),
        RolePath(world_id="under_pressure", reason="Data rounds test SQL under time pressure.", emphasis=["timed_coding"]),
        RolePath(world_id="hiring_arena", reason="Case studies + SQL + product sense.", emphasis=["coding_interviews"]),
        RolePath(world_id="projects", reason="A data portfolio project gets you hired.", emphasis=["api_design", "deployment"]),
    ],
    skills=["Python", "SQL", "Statistics", "Data Analysis", "Visualization", "Storytelling", "A/B Testing"],
    targets=["Data Scientist", "Analyst", "Product Analyst", "Analytics Engineer"],
    estimated_hours=80,
)


# ═══════════════════════════════════════════════════════════════════
# ML Engineer
# ═══════════════════════════════════════════════════════════════════

ML_ENGINEER_PACKAGE = RolePackage(
    id="ml_engineer",
    name="Machine Learning Engineer",
    icon="🤖",
    description="Build and deploy ML systems. From models to production.",
    path=[
        RolePath(world_id="foundations", reason="Python is the language of ML.", emphasis=["variables", "functions", "collections"]),
        RolePath(world_id="problem_solver", reason="ML interviews test DSA heavily.", emphasis=["arrays", "dp", "graphs"]),
        RolePath(world_id="work_with_data", reason="ML starts with data — SQL + feature engineering.", emphasis=["sql", "aggregation", "etl"]),
        RolePath(world_id="ai_engineering", reason="The core: LLMs, RAG, evaluation.", emphasis=["prompting", "rag", "evaluation", "agents"]),
        RolePath(world_id="build_systems", reason="ML systems need APIs to serve predictions.", emphasis=["rest", "apis"]),
        RolePath(world_id="software_engineering", reason="ML code must be testable and versioned.", emphasis=["git", "testing"]),
        RolePath(world_id="hiring_arena", reason="ML interviews: coding + ML design.", emphasis=["coding_interviews", "system_design"]),
        RolePath(world_id="production", reason="ML in production: monitoring, reliability.", emphasis=["monitoring", "reliability"]),
        RolePath(world_id="projects", reason="An ML project in your portfolio is gold.", emphasis=["deployment", "caching"]),
    ],
    skills=["Python", "ML Algorithms", "Deep Learning", "LLMs", "RAG", "MLOps", "System Design", "Statistics"],
    targets=["ML Engineer", "Applied Scientist", "AI Engineer", "Research Engineer"],
    estimated_hours=150,
)


# ═══════════════════════════════════════════════════════════════════
# DevOps / SRE
# ═══════════════════════════════════════════════════════════════════

DEVOPS_PACKAGE = RolePackage(
    id="devops",
    name="DevOps / SRE",
    icon="⚙️",
    description="Keep systems running. Reliability, automation, infrastructure.",
    path=[
        RolePath(world_id="foundations", reason="Scripting fundamentals.", emphasis=["variables", "loops", "functions"]),
        RolePath(world_id="build_systems", reason="Understanding the systems you operate.", emphasis=["apis", "databases", "sql"]),
        RolePath(world_id="software_engineering", reason="Infrastructure as code needs Git + testing.", emphasis=["git", "testing"]),
        RolePath(world_id="production", reason="The core: monitoring, reliability, security.", emphasis=["monitoring", "alerting", "circuit_breaker", "security"]),
        RolePath(world_id="projects", reason="Ship infrastructure — CI/CD pipelines, monitoring.", emphasis=["deployment", "caching"]),
    ],
    skills=["Linux", "Docker", "Kubernetes", "CI/CD", "Monitoring", "Cloud (AWS/GCP)", "Networking", "Security"],
    targets=["DevOps Engineer", "SRE", "Platform Engineer", "Infrastructure Engineer"],
    estimated_hours=90,
)


# ═══════════════════════════════════════════════════════════════════
# Frontend Engineer
# ═══════════════════════════════════════════════════════════════════

FRONTEND_PACKAGE = RolePackage(
    id="frontend",
    name="Frontend Engineer",
    icon="🎨",
    description="Build interfaces users love. JavaScript + React + system design.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "conditionals", "loops", "functions", "collections"]),
        RolePath(world_id="problem_solver", reason="Frontend interviews still test DSA.", emphasis=["arrays", "trees", "strings"]),
        RolePath(world_id="build_systems", reason="Frontend talks to APIs — understand them.", emphasis=["rest", "http", "status_codes"]),
        RolePath(world_id="software_engineering", reason="Professional frontend needs Git + testing.", emphasis=["git", "testing"]),
        RolePath(world_id="under_pressure", reason="Timed coding rounds.", emphasis=["timed_coding"]),
        RolePath(world_id="hiring_arena", reason="Frontend interviews: coding + system design.", emphasis=["coding_interviews"]),
        RolePath(world_id="projects", reason="A polished frontend project is your portfolio.", emphasis=["api_design", "deployment"]),
    ],
    skills=["JavaScript", "TypeScript", "React", "HTML/CSS", "APIs", "Testing", "Performance", "Accessibility"],
    targets=["Frontend Engineer", "UI Engineer", "Full Stack Engineer"],
    estimated_hours=100,
)


# ═══════════════════════════════════════════════════════════════════
# Competitive Programmer
# ═══════════════════════════════════════════════════════════════════

CP_PACKAGE = RolePackage(
    id="cp",
    name="Competitive Programmer",
    icon="🏆",
    description="Master algorithms for competitions and tough interviews.",
    path=[
        RolePath(world_id="foundations", reason="Speed starts with fundamentals.", emphasis=["variables", "loops", "functions"]),
        RolePath(world_id="problem_solver", reason="The core: DSA patterns + speed.", emphasis=["arrays", "trees", "graphs", "dp", "two_pointers", "sliding_window", "binary_search"]),
        RolePath(world_id="under_pressure", reason="Competitions are timed.", emphasis=["timed_coding", "pattern_recognition", "optimization"]),
        RolePath(world_id="hiring_arena", reason="Interview rounds = competition rounds.", emphasis=["coding_interviews"]),
    ],
    skills=["C++", "Algorithms", "Data Structures", "Math", "Pattern Recognition", "Speed"],
    targets=["Google Code Jam", "ICPC", "LeetCode Contests", "Top-tier company interviews"],
    estimated_hours=200,
)


# ═══════════════════════════════════════════════════════════════════
# Registry
# ═══════════════════════════════════════════════════════════════════

ROLE_PACKAGES: Dict[str, RolePackage] = {
    SDE_PACKAGE.id: SDE_PACKAGE,
    DATA_SCIENTIST_PACKAGE.id: DATA_SCIENTIST_PACKAGE,
    ML_ENGINEER_PACKAGE.id: ML_ENGINEER_PACKAGE,
    DEVOPS_PACKAGE.id: DEVOPS_PACKAGE,
    FRONTEND_PACKAGE.id: FRONTEND_PACKAGE,
    CP_PACKAGE.id: CP_PACKAGE,
}


def get_role_package(role_id: str) -> Optional[RolePackage]:
    return ROLE_PACKAGES.get(role_id)


def all_roles() -> List[RolePackage]:
    return list(ROLE_PACKAGES.values())


def roles_for_world(world_id: str) -> List[RolePackage]:
    """Return all roles that include a given world in their path."""
    return [r for r in ROLE_PACKAGES.values() if any(p.world_id == world_id for p in r.path)]
