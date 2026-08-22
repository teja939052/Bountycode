"""Role profiles for placement preparation paths.

Each role profile defines:
- Required skills with importance weights
- Optional skills
- Assessments and interview types
- Resume keywords
- Recommended projects
- Target companies
- Readiness weightings (how much each skill contributes to overall readiness)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum


class SkillImportance(Enum):
    CRITICAL = "critical"    # 30% weight toward readiness
    IMPORTANT = "important"  # 20% weight toward readiness
    NICE_TO_HAVE = "nice_to_have"  # 10% weight toward readiness


@dataclass
class SkillDef:
    """Definition of a skill for a role."""
    name: str
    importance: SkillImportance
    tags: List[str] = field(default_factory=list)  # e.g., ["dsa", "frontend", "backend"]
    description: str = ""


@dataclass
class AssessmentDef:
    """Definition of an assessment for a role."""
    name: str
    type: str  # "coding", "technical", "behavioral", "aptitude", "project"
    duration_minutes: int
    focus: List[str] = field(default_factory=list)  # e.g., ["dsa", "sql"]
    difficulty: str = "medium"


@dataclass
class InterviewTypeDef:
    """Definition of an interview type for a role."""
    name: str
    focus: List[str] = field(default_factory=list)
    duration_minutes: int = 60
    description: str = ""


@dataclass
class ResumeKeywordsDef:
    """Definition of resume keywords for a role."""
    keywords: List[str] = field(default_factory=list)
    importance: List[str] = field(default_factory=list)  # matching importance levels


@dataclass
class RecommendedProjectDef:
    """Definition of a recommended project for a role."""
    title: str
    description: str
    tags: List[str] = field(default_factory=list)
    estimated_hours: int = 20


@dataclass
class TargetCompanyDef:
    """Definition of a target company for a role."""
    name: str
    typical_score_range: str  # e.g., "70-85"
    common_questions: List[str] = field(default_factory=list)


@dataclass
class RoleReadinessWeights:
    """Weight of each skill toward overall readiness score."""
    weights: Dict[str, float] = field(default_factory=dict)  # skill_name -> 0-100%


@dataclass
class RoleProfile:
    """Complete role profile configuration."""
    role_name: str
    description: str
    required_skills: List[SkillDef]
    optional_skills: List[SkillDef] = field(default_factory=list)
    assessments: List[AssessmentDef] = field(default_factory=list)
    interview_types: List[InterviewTypeDef] = field(default_factory=list)
    resume_keywords: ResumeKeywordsDef = field(default_factory=ResumeKeywordsDef)
    recommended_projects: List[RecommendedProjectDef] = field(default_factory=list)
    target_companies: List[TargetCompanyDef] = field(default_factory=list)
    readiness_weights: RoleReadinessWeights = field(default_factory=RoleReadinessWeights)


# === SDE PROFILE ===

SDE_SKILLS = [
    SkillDef(
        name="DSA",
        importance=SkillImportance.CRITICAL,
        tags=["dsa", "algorithms", "data structures"],
        description="Data Structures and Algorithms fundamentals"
    ),
    SkillDef(
        name="Programming",
        importance=SkillImportance.CRITICAL,
        tags=["programming", "coding", "implementation"],
        description="Programming fundamentals and problem-solving"
    ),
    SkillDef(
        name="System Design",
        importance=SkillImportance.IMPORTANT,
        tags=["system_design", "scalability", "design"],
        description="System design and architecture"
    ),
    SkillDef(
        name="DBMS",
        importance=SkillImportance.IMPORTANT,
        tags=["database", "sql", "dbms"],
        description="Database Management Systems"
    ),
    SkillDef(
        name="Operating Systems",
        importance=SkillImportance.NICE_TO_HAVE,
        tags=["os", "processes", "threads", "scheduling"],
        description="OS fundamentals: processes, threads, scheduling"
    ),
    SkillDef(
        name="Computer Networks",
        importance=SkillImportance.NICE_TO_HAVE,
        tags=["networks", "tcp_ip", "http", "protocols"],
        description="Computer Networks fundamentals"
    ),
    SkillDef(
        name="OOP",
        importance=SkillImportance.CRITICAL,
        tags=["oop", "inheritance", "polymorphism", "encapsulation"],
        description="Object-Oriented Programming"
    ),
    SkillDef(
        name="Git/GitHub",
        importance=SkillImportance.IMPORTANT,
        tags=["git", "version_control", "github"],
        description="Version control and collaboration"
    ),
    SkillDef(
        name="Backend Fundamentals",
        importance=SkillImportance.IMPORTANT,
        tags=["backend", "api", "rest", "service"],
        description="Backend fundamentals: APIs, services"
    ),
]

SDE_ASSESSMENTS = [
    AssessmentDef(
        name="DSA Assessment",
        type="coding",
        duration_minutes=45,
        focus=["dsa", "algorithms"],
        difficulty="medium"
    ),
    AssessmentDef(
        name="System Design Interview",
        type="technical",
        duration_minutes=60,
        focus=["system_design", "scalability"],
        difficulty="medium"
    ),
    AssessmentDef(
        name="Coding Test",
        type="coding",
        duration_minutes=45,
        focus=["dsa", "sql"],
        difficulty="medium"
    ),
]

SDE_INTERVIEW_TYPES = [
    InterviewTypeDef(
        name="Technical Interview",
        focus=["dsa", "system_design", "coding"],
        duration_minutes=60,
        description="Standard technical interview for SDE roles"
    ),
    InterviewTypeDef(
        name="Behavioral Interview",
        focus=["behavioral", "leadership", "communication"],
        duration_minutes=30,
        description="Behavioral interview focusing on past experiences"
    ),
    InterviewTypeDef(
        name="System Design Interview",
        focus=["system_design", "scalability", "architecture"],
        duration_minutes=60,
        description="System design interview for senior SDE roles"
    ),
]

SDE_RESUME_KEYWORDS = ResumeKeywordsDef(
    keywords=[
        "Python", "Java", "C++", "Data Structures", "Algorithms",
        "SQL", "Git", "System Design", "REST API", "Microservices",
        "Docker", "GitHub", "Problem Solving", "Critical Thinking"
    ],
    importance=[
        "Python", "Java", "Data Structures", "Algorithms", "SQL"
    ]
)

SDE_PROJECTS = [
    RecommendedProjectDef(
        title="Library Management System",
        description="Full-stack application for managing book loans with user authentication, borrowing system, and admin panel",
        tags=["full_stack", "python", "sql", "authentication"],
        estimated_hours=30
    ),
    RecommendedProjectDef(
        title="Task Management App",
        description="React frontend with Node.js backend, task tracking, user authentication, and real-time updates",
        tags=["react", "nodejs", "sql", "real-time"],
        estimated_hours=40
    ),
    RecommendedProjectDef(
        title="E-commerce Dashboard",
        description="Dashboard for tracking sales, analytics, and user metrics with data visualization",
        tags=["react", "data_visualization", "api", "analytics"],
        estimated_hours=40
    ),
]

SDE_COMPANIES = [
    TargetCompanyDef(
        name="TCS",
        typical_score_range="65-80",
        common_questions=["DBMS questions", "OS questions", "Basic coding"]
    ),
    TargetCompanyDef(
        name="Infosys",
        typical_score_range="68-82",
        common_questions=["aptitude", "reasoning", "basic coding"]
    ),
    TargetCompanyDef(
        name="Wipro",
        typical_score_range="65-78",
        common_questions=["aptitude", "verbal", "basic coding"]
    ),
    TargetCompanyDef(
        name="Google",
        typical_score_range="85-100",
        common_questions=["system_design", "advanced_algorithms", "coding"]
    ),
    TargetCompanyDef(
        name="Amazon",
        typical_score_range="80-95",
        common_questions=["system_design", "leadership_principles", "coding"]
    ),
    TargetCompanyDef(
        name="Microsoft",
        typical_score_range="78-92",
        common_questions=["system_design", "coding", "oop"]
    ),
]

SDE_READINESS_WEIGHTS = RoleReadinessWeights(
    weights={
        "DSA": 25,
        "Programming": 20,
        "System Design": 15,
        "DBMS": 12,
        "Operating Systems": 8,
        "Computer Networks": 8,
        "OOP": 15,
        "Git/GitHub": 5,
    }
)


# Role profiles registry
ROLE_PROFILES: Dict[str, RoleProfile] = {}

# Register SDE profile
sde_profile = RoleProfile(
    role_name="Software Development Engineer",
    description="SDE role placement preparation path",
    required_skills=SDE_SKILLS,
    assessments=SDE_ASSESSMENTS,
    interview_types=SDE_INTERVIEW_TYPES,
    resume_keywords=SDE_RESUME_KEYWORDS,
    recommended_projects=SDE_PROJECTS,
    target_companies=SDE_COMPANIES,
    readiness_weights=SDE_READINESS_WEIGHTS,
)

ROLE_PROFILES["sde"] = sde_profile

# Add more roles here following the same pattern

# Convenience accessor
def get_profile(role_name: str) -> RoleProfile | None:
    """Get role profile by name."""
    return ROLE_PROFILES.get(role_name.lower())

# List all registered profiles
def list_profiles() -> List[str]:
    """List all registered role profile names."""
    return list(ROLE_PROFILES.keys())


# Export for use in other modules
__all__ = [
    "RoleProfile",
    "SkillDef",
    "AssessmentDef",
    "InterviewTypeDef",
    "ResumeKeywordsDef",
    "RecommendedProjectDef",
    "TargetCompanyDef",
    "RoleReadinessWeights",
    "ROLE_PROFILES",
    "get_profile",
    "list_profiles",
    "SDE_SKILLS",
    "SDE_ASSESSMENTS",
    "SDE_INTERVIEW_TYPES",
    "SDE_RESUME_KEYWORDS",
    "SDE_PROJECTS",
    "SDE_COMPANIES",
    "SDE_READINESS_WEIGHTS",
]