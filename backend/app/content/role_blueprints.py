"""Role blueprints — five canonical placement role definitions.

Each blueprint describes a target role as:
- required skills (must-have)
- optional skills (nice-to-have)
- prerequisites (skills that must be mastered first)
- core curriculum (what to study first)
- advanced curriculum (what to study after core)
- assessment mix (which assessments to prioritize)
- interview skills (behavioral + technical)
- project skills (what to build for portfolio)
- readiness requirements (minimum bar before applying)

Role IDs are stable and canonical:
  software_developer, software_engineer, qa_test_engineer,
  data_analyst, data_scientist

These blueprints are read by:
- personalization.py (select next mission)
- readiness_engine.build_target_profile (compute target readiness)
- opportunity_graph (compute capability gaps)
- future Journey / curriculum selection layers

No second role system is introduced; existing role_packages.py and
role_curriculum.py continue to provide learning paths, while this module
provides the canonical capability/assessment definition.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.content.master_skill_graph import (
    get_skill,
    get_skills_for_role,
    get_prerequisites,
    get_all_skills,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class RolePrerequisite:
    """A prerequisite skill or milestone."""
    skill_id: str
    min_score: float = 60.0
    description: str = ""


@dataclass
class RoleBlueprint:
    """Complete blueprint for a placement role."""
    role_id: str
    display_name: str
    description: str
    icon: str
    required_skills: List[str] = field(default_factory=list)
    optional_skills: List[str] = field(default_factory=list)
    prerequisites: List[RolePrerequisite] = field(default_factory=list)
    core_curriculum: List[Dict[str, Any]] = field(default_factory=list)
    advanced_curriculum: List[Dict[str, Any]] = field(default_factory=list)
    assessment_mix: Dict[str, float] = field(default_factory=dict)
    interview_skills: List[str] = field(default_factory=list)
    project_skills: List[str] = field(default_factory=list)
    readiness_requirements: Dict[str, Any] = field(default_factory=dict)
    estimated_weeks: int = 12
    target_companies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role_id": self.role_id,
            "display_name": self.display_name,
            "description": self.description,
            "icon": self.icon,
            "required_skills": self.required_skills,
            "optional_skills": self.optional_skills,
            "prerequisites": [
                {"skill_id": p.skill_id, "min_score": p.min_score, "description": p.description}
                for p in self.prerequisites
            ],
            "core_curriculum": self.core_curriculum,
            "advanced_curriculum": self.advanced_curriculum,
            "assessment_mix": self.assessment_mix,
            "interview_skills": self.interview_skills,
            "project_skills": self.project_skills,
            "readiness_requirements": self.readiness_requirements,
            "estimated_weeks": self.estimated_weeks,
            "target_companies": self.target_companies,
        }


# ---------------------------------------------------------------------------
# Blueprint factory helpers
# ---------------------------------------------------------------------------

def _skill(skill_id: str, weight: float = 1.0, critical: bool = False) -> Dict[str, Any]:
    return {"skill_id": skill_id, "weight": weight, "critical": critical}


def _prereq(skill_id: str, min_score: float = 60.0, description: str = "") -> RolePrerequisite:
    return RolePrerequisite(skill_id=skill_id, min_score=min_score, description=description)


def _module(
    skill_id: str,
    topics: List[str],
    difficulty: str = "intermediate",
    estimated_hours: int = 4,
    lesson_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "skill_id": skill_id,
        "topics": topics,
        "difficulty": difficulty,
        "estimated_hours": estimated_hours,
        "lesson_ids": lesson_ids or [],
    }


# ---------------------------------------------------------------------------
# Blueprint definitions
# ---------------------------------------------------------------------------

def _build_software_developer() -> RoleBlueprint:
    return RoleBlueprint(
        role_id="software_developer",
        display_name="Software Developer",
        icon="💻",
        description="Build production-grade software. Strong DSA, coding fluency, and system design fundamentals.",
        required_skills=[
            _skill("foundation.programming_basics", 1.0, True),
            _skill("foundation.control_flow", 1.0, True),
            _skill("foundation.functions", 1.0, True),
            _skill("foundation.data_structures_lang", 1.0, True),
            _skill("dsa.arrays_hashing", 1.0, True),
            _skill("dsa.two_pointers", 0.9),
            _skill("dsa.binary_search", 0.9),
            _skill("dsa.strings", 0.9),
            _skill("dsa.linked_list", 0.8),
            _skill("dsa.stack_queue", 0.8),
            _skill("dsa.trees", 0.8),
            _skill("dsa.dp", 0.7),
            _skill("cs_fundamentals.oops", 0.8, True),
            _skill("cs_fundamentals.dbms", 0.7),
            _skill("cs_fundamentals.sql", 0.7),
        ],
        optional_skills=[
            _skill("dsa.graphs", 0.6),
            _skill("dsa.heaps", 0.6),
            _skill("dsa.tries", 0.5),
            _skill("dsa.bit_manipulation", 0.5),
            _skill("system_design.scalability", 0.7),
            _skill("system_design.hld", 0.7),
            _skill("cs_fundamentals.os", 0.6),
            _skill("cs_fundamentals.networks", 0.5),
        ],
        prerequisites=[
            _prereq("foundation.programming_basics", 70.0, "Must know variables, types, and basic I/O."),
            _prereq("foundation.control_flow", 70.0, "Must be comfortable with loops and conditionals."),
            _prereq("foundation.data_structures_lang", 70.0, "Must know arrays, lists, strings, and dicts."),
        ],
        core_curriculum=[
            _module("dsa.arrays_hashing", ["two_sum", "anagram", "group_anagrams", "longest_substring"], "intermediate", 6),
            _module("dsa.two_pointers", ["three_sum", "container_water", "trapping_rain"], "intermediate", 5),
            _module("dsa.binary_search", ["binary_search", "search_rotated", "find_peak"], "intermediate", 4),
            _module("dsa.strings", ["palindrome", "valid_anagram", "longest_palindrome"], "intermediate", 5),
            _module("dsa.linked_list", ["reverse_list", "detect_cycle", "merge_lists"], "intermediate", 5),
            _module("dsa.stack_queue", ["valid_parentheses", "min_stack", "daily_temperatures"], "intermediate", 5),
            _module("dsa.trees", ["traversals", "invert_tree", "max_depth"], "intermediate", 6),
            _module("dsa.dp", ["climbing_stairs", "house_robber", "coin_change"], "advanced", 8),
            _module("cs_fundamentals.sql", ["joins", "aggregations", "subqueries"], "intermediate", 4),
            _module("foundation.complexity", ["big_o", "time_space_analysis"], "intermediate", 3),
        ],
        advanced_curriculum=[
            _module("dsa.graphs", ["number_of_islands", "course_schedule", "alien_dictionary"], "advanced", 8),
            _module("dsa.heaps", ["top_k_frequent", "merge_k_sorted", "median_stream"], "advanced", 6),
            _module("dsa.backtracking", ["permutations", "subsets", "n_queens"], "advanced", 6),
            _module("system_design.scalability", ["rate_limiter", "consistent_hashing"], "advanced", 6),
            _module("system_design.hld", ["tinyurl", "web_crawler", "chat_system"], "advanced", 10),
        ],
        assessment_mix={
            "dsa": 0.35,
            "coding": 0.25,
            "aptitude": 0.15,
            "cs_fundamentals": 0.10,
            "interview": 0.10,
            "system_design": 0.05,
        },
        interview_skills=[
            "interview.technical_accuracy",
            "interview.communication",
            "interview.problem_solving",
            "interview.depth",
            "behavioral.communication",
            "behavioral.teamwork",
            "behavioral.problem_solving",
        ],
        project_skills=[
            "projects.portfolio",
            "projects.architecture",
            "role.sde.api_design",
            "role.sde.databases",
            "role.sde.testing",
            "role.sde.git",
        ],
        readiness_requirements={
            "min_overall_score": 70.0,
            "min_dsa_score": 65.0,
            "min_coding_score": 70.0,
            "min_solved_problems": 80,
            "min_mock_interviews": 3,
            "must_have_projects": 2,
        },
        estimated_weeks=16,
        target_companies=["Google", "Amazon", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Accenture", "Cognizant", "Capgemini"],
    )


def _build_software_engineer() -> RoleBlueprint:
    return RoleBlueprint(
        role_id="software_engineer",
        display_name="Software Engineer",
        icon="🛠️",
        description="Engineer reliable systems end-to-end. Strong fundamentals, testing discipline, and design maturity.",
        required_skills=[
            _skill("foundation.programming_basics", 1.0, True),
            _skill("foundation.control_flow", 1.0, True),
            _skill("foundation.functions", 1.0, True),
            _skill("foundation.data_structures_lang", 1.0, True),
            _skill("dsa.arrays_hashing", 1.0, True),
            _skill("dsa.binary_search", 0.9),
            _skill("dsa.strings", 0.9),
            _skill("dsa.trees", 0.8),
            _skill("dsa.dp", 0.7),
            _skill("cs_fundamentals.oops", 1.0, True),
            _skill("cs_fundamentals.dbms", 0.8, True),
            _skill("cs_fundamentals.sql", 0.8, True),
            _skill("role.sde.testing", 0.9, True),
            _skill("role.sde.git", 0.8, True),
        ],
        optional_skills=[
            _skill("dsa.graphs", 0.6),
            _skill("system_design.scalability", 0.7),
            _skill("system_design.hld", 0.7),
            _skill("system_design.dld", 0.5),
            _skill("cs_fundamentals.os", 0.6),
            _skill("cs_fundamentals.networks", 0.5),
        ],
        prerequisites=[
            _prereq("foundation.programming_basics", 75.0, "Solid grasp of language fundamentals."),
            _prereq("foundation.data_structures_lang", 75.0, "Comfortable with core data structures."),
            _prereq("cs_fundamentals.oops", 70.0, "Must understand OOP principles."),
        ],
        core_curriculum=[
            _module("dsa.arrays_hashing", ["two_sum", "longest_substring", "valid_sudoku"], "intermediate", 6),
            _module("dsa.binary_search", ["search_rotated", "find_min_rotated"], "intermediate", 4),
            _module("dsa.trees", ["level_order", "invert_tree", "path_sum"], "intermediate", 6),
            _module("dsa.dp", ["climbing_stairs", "house_robber", "longest_increasing"], "advanced", 8),
            _module("cs_fundamentals.sql", ["joins", "window_functions", "query_optimization"], "intermediate", 5),
            _module("role.sde.testing", ["unit_testing", "integration_testing", "test_doubles"], "intermediate", 5),
            _module("role.sde.git", ["branching", "rebase_vs_merge", "ci_cd_basics"], "intermediate", 3),
            _module("foundation.complexity", ["big_o", "amortized_analysis"], "intermediate", 3),
        ],
        advanced_curriculum=[
            _module("dsa.graphs", ["number_of_islands", "dijkstra", "topological_sort"], "advanced", 8),
            _module("system_design.scalability", ["load_balancing", "caching_strategies"], "advanced", 6),
            _module("system_design.hld", ["url_shortener", "web_crawler", "rate_limiter"], "advanced", 10),
            _module("system_design.dld", ["database_sharding", "message_queues", "circuit_breaker"], "expert", 10),
        ],
        assessment_mix={
            "dsa": 0.30,
            "coding": 0.25,
            "cs_fundamentals": 0.15,
            "aptitude": 0.10,
            "interview": 0.15,
            "system_design": 0.05,
        },
        interview_skills=[
            "interview.technical_accuracy",
            "interview.communication",
            "interview.problem_solving",
            "interview.depth",
            "behavioral.communication",
            "behavioral.teamwork",
            "behavioral.ownership",
        ],
        project_skills=[
            "projects.portfolio",
            "projects.architecture",
            "role.sde.api_design",
            "role.sde.databases",
            "role.sde.testing",
        ],
        readiness_requirements={
            "min_overall_score": 75.0,
            "min_dsa_score": 70.0,
            "min_coding_score": 75.0,
            "min_solved_problems": 100,
            "min_mock_interviews": 4,
            "must_have_projects": 2,
        },
        estimated_weeks=18,
        target_companies=["Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Uber", "Flipkart", "Stripe"],
    )


def _build_qa_test_engineer() -> RoleBlueprint:
    return RoleBlueprint(
        role_id="qa_test_engineer",
        display_name="QA / Test Engineer",
        icon="🧪",
        description="Ensure software quality through manual and automated testing. Strong attention to detail and test strategy.",
        required_skills=[
            _skill("foundation.programming_basics", 0.8, True),
            _skill("foundation.control_flow", 0.8, True),
            _skill("foundation.data_structures_lang", 0.8, True),
            _skill("dsa.arrays_hashing", 0.7),
            _skill("dsa.strings", 0.7),
            _skill("role.qa.test_strategy", 1.0, True),
            _skill("role.qa.automation", 0.9, True),
            _skill("role.qa.defect_management", 0.8, True),
            _skill("cs_fundamentals.sql", 0.6),
            _skill("cs_fundamentals.oops", 0.7),
        ],
        optional_skills=[
            _skill("role.qa.performance", 0.7),
            _skill("dsa.linked_list", 0.5),
            _skill("cs_fundamentals.dbms", 0.5),
            _skill("aptitude.verbal", 0.5),
        ],
        prerequisites=[
            _prereq("foundation.programming_basics", 60.0, "Must understand basic programming to write test scripts."),
            _prereq("role.qa.test_strategy", 50.0, "Must know test case design."),
        ],
        core_curriculum=[
            _module("role.qa.test_strategy", ["test_planning", "test_cases", "boundary_analysis", "equivalence_partitioning"], "intermediate", 6),
            _module("role.qa.automation", ["selenium_basics", "api_testing", "test_frameworks"], "intermediate", 8),
            _module("role.qa.defect_management", ["bug_lifecycle", "severity_priority", "root_cause_analysis"], "intermediate", 4),
            _module("dsa.arrays_hashing", ["two_sum", "valid_anagram"], "beginner", 4),
            _module("cs_fundamentals.sql", ["select_joins", "aggregations"], "intermediate", 4),
        ],
        advanced_curriculum=[
            _module("role.qa.performance", ["jmeter", "load_testing", "stress_testing", "benchmarking"], "advanced", 6),
            _module("role.qa.automation", ["ci_cd_integration", "bdd_cucumber", "mocking"], "advanced", 6),
            _module("dsa.strings", ["string_validation", "pattern_matching"], "intermediate", 4),
        ],
        assessment_mix={
            "dsa": 0.20,
            "coding": 0.20,
            "aptitude": 0.20,
            "cs_fundamentals": 0.15,
            "interview": 0.15,
            "system_design": 0.05,
            "verbal": 0.05,
        },
        interview_skills=[
            "interview.technical_accuracy",
            "interview.communication",
            "interview.problem_solving",
            "behavioral.communication",
            "behavioral.teamwork",
            "behavioral.adaptability",
        ],
        project_skills=[
            "projects.portfolio",
            "role.qa.automation",
            "role.qa.test_strategy",
            "role.sde.testing",
        ],
        readiness_requirements={
            "min_overall_score": 65.0,
            "min_dsa_score": 55.0,
            "min_coding_score": 60.0,
            "min_solved_problems": 40,
            "min_mock_interviews": 2,
            "must_have_projects": 1,
        },
        estimated_weeks=12,
        target_companies=["TCS", "Infosys", "Wipro", "Accenture", "Cognizant", "Capgemini", "HCLTech", "Tech Mahindra", "LTIMindtree", "Mphasis", "Coforge", "Persistent"],
    )


def _build_data_analyst() -> RoleBlueprint:
    return RoleBlueprint(
        role_id="data_analyst",
        display_name="Data Analyst",
        icon="📊",
        description="Turn data into decisions. SQL fluency, statistical reasoning, and visualization.",
        required_skills=[
            _skill("foundation.programming_basics", 0.7, True),
            _skill("cs_fundamentals.sql", 1.0, True),
            _skill("role.data_analyst.sql", 0.9, True),
            _skill("role.data_analyst.statistics", 0.9, True),
            _skill("role.data_analyst.visualization", 0.8, True),
            _skill("aptitude.quantitative", 0.8, True),
            _skill("aptitude.data_interpretation", 0.8, True),
        ],
        optional_skills=[
            _skill("role.data_analyst.etl", 0.7),
            _skill("dsa.arrays_hashing", 0.5),
            _skill("role.data_scientist.ml_fundamentals", 0.4),
            _skill("system_design.scalability", 0.3),
        ],
        prerequisites=[
            _prereq("foundation.programming_basics", 55.0, "Must read/write scripts for data processing."),
            _prereq("cs_fundamentals.sql", 65.0, "Must write intermediate SQL queries."),
        ],
        core_curriculum=[
            _module("cs_fundamentals.sql", ["joins", "aggregations", "group_by", "case_statements"], "intermediate", 6),
            _module("role.data_analyst.sql", ["window_functions", "cte", "pivot_queries"], "intermediate", 6),
            _module("role.data_analyst.statistics", ["descriptive_stats", "hypothesis_testing", "ab_testing"], "intermediate", 6),
            _module("role.data_analyst.visualization", ["matplotlib", "seaborn", "powerbi", "storytelling"], "intermediate", 5),
            _module("aptitude.quantitative", ["percentages", "ratios", "data_interpretation"], "intermediate", 5),
        ],
        advanced_curriculum=[
            _module("role.data_analyst.etl", ["pipelines", "data_quality", "scheduling"], "advanced", 6),
            _module("role.data_scientist.ml_fundamentals", ["linear_regression", "classification", "clustering"], "advanced", 8),
            _module("aptitude.data_interpretation", ["caselets", "graph_analysis", "table_analysis"], "advanced", 4),
        ],
        assessment_mix={
            "aptitude": 0.35,
            "dsa": 0.15,
            "coding": 0.15,
            "cs_fundamentals": 0.15,
            "interview": 0.15,
            "system_design": 0.05,
        },
        interview_skills=[
            "interview.technical_accuracy",
            "interview.communication",
            "interview.problem_solving",
            "behavioral.communication",
            "behavioral.problem_solving",
            "behavioral.adaptability",
        ],
        project_skills=[
            "projects.portfolio",
            "projects.architecture",
            "role.data_analyst.visualization",
            "role.data_analyst.etl",
            "role.data_analyst.sql",
        ],
        readiness_requirements={
            "min_overall_score": 65.0,
            "min_aptitude_score": 65.0,
            "min_sql_score": 70.0,
            "min_solved_problems": 30,
            "min_mock_interviews": 2,
            "must_have_projects": 1,
        },
        estimated_weeks=12,
        target_companies=["Google", "Amazon", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Accenture", "Cognizant", "Capgemini", "Flipkart", "Swiggy"],
    )


def _build_data_scientist() -> RoleBlueprint:
    return RoleBlueprint(
        role_id="data_scientist",
        display_name="Data Scientist",
        icon="🔬",
        description="Build predictive models and extract insights. Statistics, ML, and experimentation.",
        required_skills=[
            _skill("foundation.programming_basics", 0.8, True),
            _skill("foundation.data_structures_lang", 0.8, True),
            _skill("cs_fundamentals.sql", 0.9, True),
            _skill("role.data_analyst.statistics", 1.0, True),
            _skill("role.data_scientist.ml_fundamentals", 1.0, True),
            _skill("role.data_scientist.deep_learning", 0.7),
            _skill("aptitude.quantitative", 0.8, True),
            _skill("aptitude.data_interpretation", 0.7),
        ],
        optional_skills=[
            _skill("role.data_scientist.nlp", 0.6),
            _skill("role.data_scientist.mlops", 0.6),
            _skill("dsa.arrays_hashing", 0.5),
            _skill("system_design.scalability", 0.4),
            _skill("foundation.complexity", 0.5),
        ],
        prerequisites=[
            _prereq("foundation.programming_basics", 70.0, "Must write clean Python for modeling."),
            _prereq("cs_fundamentals.sql", 70.0, "Must extract and manipulate data."),
            _prereq("role.data_analyst.statistics", 65.0, "Must understand probability and inference."),
        ],
        core_curriculum=[
            _module("role.data_analyst.statistics", ["probability", "distributions", "hypothesis_testing", "ab_testing"], "intermediate", 8),
            _module("role.data_scientist.ml_fundamentals", ["linear_regression", "logistic_regression", "decision_trees", "evaluation_metrics"], "intermediate", 8),
            _module("cs_fundamentals.sql", ["joins", "window_functions", "cte"], "intermediate", 5),
            _module("role.data_analyst.visualization", ["matplotlib", "seaborn", "storytelling"], "intermediate", 4),
            _module("aptitude.quantitative", ["probability", "permutations", "statistics"], "intermediate", 6),
        ],
        advanced_curriculum=[
            _module("role.data_scientist.deep_learning", ["neural_networks", "cnn", "rnn", "transformers"], "advanced", 10),
            _module("role.data_scientist.nlp", ["tokenization", "embeddings", "llms", "rag"], "advanced", 8),
            _module("role.data_scientist.mlops", ["deployment", "monitoring", "feature_store"], "advanced", 6),
            _module("dsa.dp", ["sequences", "optimization"], "advanced", 6),
        ],
        assessment_mix={
            "dsa": 0.15,
            "coding": 0.15,
            "aptitude": 0.25,
            "cs_fundamentals": 0.10,
            "interview": 0.20,
            "system_design": 0.05,
            "projects": 0.10,
        },
        interview_skills=[
            "interview.technical_accuracy",
            "interview.communication",
            "interview.problem_solving",
            "interview.depth",
            "behavioral.communication",
            "behavioral.problem_solving",
        ],
        project_skills=[
            "projects.portfolio",
            "projects.architecture",
            "role.data_scientist.ml_fundamentals",
            "role.data_scientist.deep_learning",
            "role.data_analyst.visualization",
        ],
        readiness_requirements={
            "min_overall_score": 70.0,
            "min_aptitude_score": 70.0,
            "min_ml_score": 65.0,
            "min_solved_problems": 25,
            "min_mock_interviews": 3,
            "must_have_projects": 2,
        },
        estimated_weeks=16,
        target_companies=["Google", "Amazon", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Accenture", "Cognizant", "Capgemini", "Flipkart", "Swiggy", "Dream11", "Razorpay"],
    )


# ---------------------------------------------------------------------------
# Canonical registry
# ---------------------------------------------------------------------------

_ROLE_BUILDERS = {
    "software_developer": _build_software_developer,
    "software_engineer": _build_software_engineer,
    "qa_test_engineer": _build_qa_test_engineer,
    "data_analyst": _build_data_analyst,
    "data_scientist": _build_data_scientist,
}

_ROLES: Dict[str, RoleBlueprint] = {}


def _ensure_roles() -> Dict[str, RoleBlueprint]:
    global _ROLES
    if not _ROLES:
        _ROLES = {k: v() for k, v in _ROLE_BUILDERS.items()}
    return _ROLES


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_role(role_id: str) -> Optional[RoleBlueprint]:
    """Return a role blueprint by canonical role_id, or None."""
    return _ensure_roles().get(role_id.lower().strip())


def get_all_roles() -> Dict[str, RoleBlueprint]:
    """Return all role blueprints (read-only copy)."""
    return dict(_ensure_roles())


def get_role_ids() -> List[str]:
    """Return all canonical role IDs."""
    return list(_ensure_roles().keys())


def get_role_skill_ids(role_id: str) -> List[str]:
    """Return all skill_ids associated with a role (required + optional)."""
    bp = get_role(role_id)
    if not bp:
        return []
    return list(dict.fromkeys(bp.required_skills + bp.optional_skills))


def get_role_curriculum(role_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """Return core + advanced curriculum for a role."""
    bp = get_role(role_id)
    if not bp:
        return {"core_curriculum": [], "advanced_curriculum": []}
    return {
        "core_curriculum": bp.core_curriculum,
        "advanced_curriculum": bp.advanced_curriculum,
    }


def get_role_readiness_requirements(role_id: str) -> Dict[str, Any]:
    """Return readiness requirements for a role."""
    bp = get_role(role_id)
    if not bp:
        return {}
    return bp.readiness_requirements


def get_assessment_mix(role_id: str) -> Dict[str, float]:
    """Return the assessment mix for a role."""
    bp = get_role(role_id)
    if not bp:
        return {}
    return bp.assessment_mix


def build_role_skill_targets(role_id: str) -> Dict[str, Any]:
    """Build a target skill map for readiness_engine.build_target_profile.

    Returns a dict with 'role', 'skills' list compatible with the v2
    readiness target profile shape.
    """
    bp = get_role(role_id)
    if not bp:
        return {"role": role_id, "skills": []}

    graph = get_all_skills()
    targets = []
    seen: set = set()

    for skill_id in bp.required_skills + bp.optional_skills:
        if skill_id in seen:
            continue
        seen.add(skill_id)
        node = graph.get(skill_id)
        if not node:
            continue
        targets.append({
            "skill_id": skill_id,
            "label": node.name,
            "domain": node.domains[0] if node.domains else "coding",
            "weight": next(
                (s["weight"] for s in bp.required_skills + bp.optional_skills if s.get("skill_id") == skill_id),
                0.5,
            ),
            "critical": any(s.get("critical") for s in bp.required_skills if s.get("skill_id") == skill_id),
        })

    return {"role": bp.role_id, "skills": targets}
