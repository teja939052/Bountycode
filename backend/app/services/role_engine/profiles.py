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


# === AI SOFTWARE DEVELOPER PROFILE ===

AI_SWE_SKILLS = [
    SkillDef("Programming", SkillImportance.CRITICAL, ["programming", "python", "implementation"], "Programming fundamentals and implementation"),
    SkillDef("LLM & AI Fundamentals", SkillImportance.CRITICAL, ["ai", "llm", "transformers", "prompting"], "LLMs, prompting, embeddings, RAG"),
    SkillDef("DSA", SkillImportance.IMPORTANT, ["dsa", "algorithms"], "Data structures and algorithms"),
    SkillDef("Machine Learning Basics", SkillImportance.IMPORTANT, ["ml", "models", "training"], "Core ML concepts and pipelines"),
    SkillDef("Backend Fundamentals", SkillImportance.IMPORTANT, ["backend", "api", "rest"], "Backend APIs, services, model serving"),
    SkillDef("Databases & Vector Stores", SkillImportance.IMPORTANT, ["database", "sql", "vector"], "SQL and vector databases"),
    SkillDef("Prompt Engineering", SkillImportance.IMPORTANT, ["prompt", "rag", "agents"], "Prompt design, RAG, agent workflows"),
    SkillDef("Python & Libraries", SkillImportance.CRITICAL, ["python", "numpy", "pandas"], "Python + AI/ML libraries"),
]

AI_SWE_READINESS_WEIGHTS = RoleReadinessWeights(weights={
    "Programming": 20, "LLM & AI Fundamentals": 20, "DSA": 12,
    "Machine Learning Basics": 12, "Backend Fundamentals": 12,
    "Databases & Vector Stores": 10, "Prompt Engineering": 8,
    "Python & Libraries": 6,
})

ai_swe_profile = RoleProfile(
    role_name="AI Software Developer",
    description="AI software development and LLM application roles",
    required_skills=AI_SWE_SKILLS,
    target_companies=[
        TargetCompanyDef("OpenAI", "85-100", ["LLM architecture", "system design", "coding"]),
        TargetCompanyDef("Google DeepMind", "85-100", ["algorithm", "ml", "coding"]),
        TargetCompanyDef("Anthropic", "85-100", ["LLM reasoning", "system design"]),
        TargetCompanyDef("Microsoft AI", "80-95", ["ml", "coding", "system design"]),
        TargetCompanyDef("Meta AI", "80-95", ["system design", "ml", "coding"]),
    ],
    recommended_projects=[
        RecommendedProjectDef("RAG Chatbot", "Knowledge-base chatbot using embeddings + a vector store and an LLM", tags=["llm", "rag", "python", "vector"], estimated_hours=40),
        RecommendedProjectDef("LLM Evaluation Harness", "Evaluate and compare model outputs across quality dimensions", tags=["llm", "eval", "python"], estimated_hours=30),
        RecommendedProjectDef("Document Summarizer API", "REST API that summarizes documents via an LLM with caching", tags=["backend", "llm", "api"], estimated_hours=25),
    ],
    readiness_weights=AI_SWE_READINESS_WEIGHTS,
)
ROLE_PROFILES["ai_software_developer"] = ai_swe_profile
ROLE_PROFILES["ai_developer"] = ai_swe_profile  # alias


# === DATA ANALYST PROFILE ===

DATA_ANALYST_SKILLS = [
    SkillDef("SQL", SkillImportance.CRITICAL, ["sql", "queries", "joins"], "SQL queries, joins, aggregations"),
    SkillDef("Spreadsheets & Excel", SkillImportance.IMPORTANT, ["excel", "sheets"], "Excel/Google Sheets analysis"),
    SkillDef("Data Cleaning", SkillImportance.IMPORTANT, ["data", "cleaning", "pandas"], "Data cleaning and transformation"),
    SkillDef("Python for Data", SkillImportance.IMPORTANT, ["python", "pandas", "numpy"], "Python data manipulation"),
    SkillDef("Statistics", SkillImportance.IMPORTANT, ["statistics", "probability"], "Descriptive and inferential statistics"),
    SkillDef("Data Visualization", SkillImportance.IMPORTANT, ["viz", "charts", "dashboard"], "Charts, dashboards, storytelling"),
    SkillDef("Business Acumen", SkillImportance.NICE_TO_HAVE, ["business", "metrics"], "KPIs and business metrics"),
    SkillDef("Aptitude & Reasoning", SkillImportance.IMPORTANT, ["aptitude", "reasoning"], "Quantitative and logical reasoning"),
]

DATA_ANALYST_READINESS_WEIGHTS = RoleReadinessWeights(weights={
    "SQL": 25, "Data Cleaning": 15, "Python for Data": 15, "Statistics": 12,
    "Data Visualization": 12, "Spreadsheets & Excel": 8, "Aptitude & Reasoning": 8,
    "Business Acumen": 5,
})

data_analyst_profile = RoleProfile(
    role_name="Data Analyst",
    description="Data analysis, BI and reporting roles",
    required_skills=DATA_ANALYST_SKILLS,
    target_companies=[
        TargetCompanyDef("TCS", "65-80", ["SQL", "aptitude", "Excel"]),
        TargetCompanyDef("Infosys", "68-82", ["SQL", "statistics", "coding"]),
        TargetCompanyDef("Accenture", "70-85", ["SQL", "dashboarding", "aptitude"]),
        TargetCompanyDef("Deloitte", "72-86", ["SQL", "visualization", "case study"]),
        TargetCompanyDef("Amazon", "80-95", ["SQL", "analytics", "behavioral"]),
    ],
    recommended_projects=[
        RecommendedProjectDef("Sales KPI Dashboard", "Interactive dashboard tracking sales KPIs with filters and trends", tags=["sql", "dashboard", "python"], estimated_hours=25),
        RecommendedProjectDef("Customer Churn Analysis", "Exploratory analysis identifying churn drivers from a dataset", tags=["python", "analysis", "statistics"], estimated_hours=20),
        RecommendedProjectDef("A/B Test Report", "Design and analyze an A/B experiment with statistical rigor", tags=["statistics", "sql", "python"], estimated_hours=20),
    ],
    readiness_weights=DATA_ANALYST_READINESS_WEIGHTS,
)
ROLE_PROFILES["data_analyst"] = data_analyst_profile


# === QA / AUTOMATION PROFILE ===

QA_SKILLS = [
    SkillDef("Testing Fundamentals", SkillImportance.CRITICAL, ["testing", "qa"], "Test types, cases, test design"),
    SkillDef("Test Automation", SkillImportance.CRITICAL, ["automation", "selenium", "pytest"], "Automated test frameworks"),
    SkillDef("Programming", SkillImportance.IMPORTANT, ["programming", "python", "java"], "Programming for automation"),
    SkillDef("API Testing", SkillImportance.IMPORTANT, ["api", "rest", "postman"], "REST API testing"),
    SkillDef("SQL", SkillImportance.IMPORTANT, ["sql", "databases"], "SQL for test validation"),
    SkillDef("Bug Reporting", SkillImportance.IMPORTANT, ["bug", "jira"], "Defect lifecycle and reporting"),
    SkillDef("DevOps & CI/CD Basics", SkillImportance.NICE_TO_HAVE, ["ci", "devops", "pipeline"], "CI/CD and test pipelines"),
    SkillDef("Aptitude & Reasoning", SkillImportance.IMPORTANT, ["aptitude", "reasoning"], "Quantitative and logical reasoning"),
]

QA_READINESS_WEIGHTS = RoleReadinessWeights(weights={
    "Testing Fundamentals": 22, "Test Automation": 22, "Programming": 14,
    "API Testing": 12, "SQL": 8, "Bug Reporting": 8,
    "DevOps & CI/CD Basics": 6, "Aptitude & Reasoning": 8,
})

qa_profile = RoleProfile(
    role_name="QA / Automation Engineer",
    description="Quality assurance and test automation roles",
    required_skills=QA_SKILLS,
    target_companies=[
        TargetCompanyDef("TCS", "65-80", ["testing", "sql", "aptitude"]),
        TargetCompanyDef("Infosys", "68-82", ["automation", "sql", "reasoning"]),
        TargetCompanyDef("Wipro", "65-78", ["testing", "aptitude", "coding"]),
        TargetCompanyDef("Cognizant", "66-80", ["sql", "testing", "automation"]),
    ],
    recommended_projects=[
        RecommendedProjectDef("Automation Test Suite", "Pytest/Selenium suite covering core web flows", tags=["automation", "python", "selenium"], estimated_hours=25),
        RecommendedProjectDef("API Test Framework", "Reusable REST API test harness with assertions", tags=["api", "python", "pytest"], estimated_hours=20),
        RecommendedProjectDef("Bug Tracking Demo", "Reproduce and document a bug lifecycle for a sample app", tags=["qa", "bug", "jira"], estimated_hours=10),
    ],
    readiness_weights=QA_READINESS_WEIGHTS,
)
ROLE_PROFILES["qa"] = qa_profile
ROLE_PROFILES["qa_automation"] = qa_profile  # alias


# === FRONTEND DEVELOPER PROFILE ===

FRONTEND_SKILLS = [
    SkillDef("JavaScript/TypeScript", SkillImportance.CRITICAL, ["javascript", "typescript"], "JS/TS fundamentals"),
    SkillDef("HTML & CSS", SkillImportance.CRITICAL, ["html", "css"], "Markup and styling"),
    SkillDef("React & Component Design", SkillImportance.CRITICAL, ["react", "components", "hooks"], "React, components, state"),
    SkillDef("Web APIs & Browser", SkillImportance.IMPORTANT, ["dom", "browser", "fetch"], "Browser APIs and HTTP"),
    SkillDef("State Management", SkillImportance.IMPORTANT, ["state", "redux"], "State management and data flow"),
    SkillDef("Rest APIs Integration", SkillImportance.IMPORTANT, ["rest", "api"], "Consuming REST APIs"),
    SkillDef("DSA Basics", SkillImportance.IMPORTANT, ["dsa", "algorithms"], "Core DSA for frontend"),
    SkillDef("UI/UX & Accessibility", SkillImportance.NICE_TO_HAVE, ["ui", "ux", "accessibility"], "Design systems and a11y"),
]

FRONTEND_READINESS_WEIGHTS = RoleReadinessWeights(weights={
    "JavaScript/TypeScript": 22, "HTML & CSS": 18, "React & Component Design": 20,
    "Web APIs & Browser": 12, "State Management": 8, "Rest APIs Integration": 8,
    "DSA Basics": 8, "UI/UX & Accessibility": 4,
})

frontend_profile = RoleProfile(
    role_name="Frontend Developer",
    description="Frontend / web UI development roles",
    required_skills=FRONTEND_SKILLS,
    target_companies=[
        TargetCompanyDef("Flipkart", "75-90", ["react", "javascript", "dsa"]),
        TargetCompanyDef("Swiggy", "72-88", ["react", "javascript", "system design"]),
        TargetCompanyDef("Zomato", "72-88", ["react", "javascript", "dsa"]),
        TargetCompanyDef("Cognizant", "66-80", ["html", "css", "javascript"]),
    ],
    recommended_projects=[
        RecommendedProjectDef("Component Library", "Reusable React component library with docs", tags=["react", "typescript", "ui"], estimated_hours=30),
        RecommendedProjectDef("Data Dashboard UI", "Responsive dashboard with charts and filters", tags=["react", "dashboard", "api"], estimated_hours=30),
        RecommendedProjectDef("E-commerce Storefront", "Storefront with cart, state and checkout flow", tags=["react", "state", "api"], estimated_hours=35),
    ],
    readiness_weights=FRONTEND_READINESS_WEIGHTS,
)
ROLE_PROFILES["frontend"] = frontend_profile


# === BACKEND DEVELOPER PROFILE ===

BACKEND_SKILLS = [
    SkillDef("Programming", SkillImportance.CRITICAL, ["programming", "python", "java", "node"], "Server-side programming"),
    SkillDef("DSA", SkillImportance.IMPORTANT, ["dsa", "algorithms"], "Data structures and algorithms"),
    SkillDef("Backend Fundamentals", SkillImportance.CRITICAL, ["backend", "api", "rest"], "APIs, services, middleware"),
    SkillDef("Databases (SQL & NoSQL)", SkillImportance.CRITICAL, ["sql", "nosql", "database"], "SQL and NoSQL databases"),
    SkillDef("System Design", SkillImportance.IMPORTANT, ["system_design", "scalability"], "Architecture and scalability"),
    SkillDef("Operating Systems", SkillImportance.IMPORTANT, ["os", "processes", "threads"], "OS fundamentals"),
    SkillDef("Computer Networks", SkillImportance.IMPORTANT, ["networks", "tcp_ip", "http"], "Networking protocols"),
    SkillDef("DevOps & Docker", SkillImportance.NICE_TO_HAVE, ["docker", "devops", "deploy"], "Containerization and deployment"),
    SkillDef("Cache & Queues", SkillImportance.IMPORTANT, ["cache", "redis", "queue"], "Caching and message queues"),
]

BACKEND_READINESS_WEIGHTS = RoleReadinessWeights(weights={
    "Programming": 18, "Backend Fundamentals": 20, "Databases (SQL & NoSQL)": 15,
    "DSA": 12, "System Design": 12, "Cache & Queues": 8,
    "Operating Systems": 6, "Computer Networks": 6, "DevOps & Docker": 3,
})

backend_profile = RoleProfile(
    role_name="Backend Developer",
    description="Backend / API / services engineering roles",
    required_skills=BACKEND_SKILLS,
    target_companies=[
        TargetCompanyDef("Amazon", "80-95", ["system design", "algorithms", "coding"]),
        TargetCompanyDef("Google", "85-100", ["system design", "algorithms", "coding"]),
        TargetCompanyDef("Flipkart", "75-90", ["system design", "sql", "coding"]),
        TargetCompanyDef("Razorpay", "74-90", ["backend", "system design", "coding"]),
    ],
    recommended_projects=[
        RecommendedProjectDef("REST API Service", "Production-grade REST API with auth, caching and rate limiting", tags=["backend", "api", "sql", "auth"], estimated_hours=40),
        RecommendedProjectDef("URL Shortener", "Scalable URL shortening service with hashing and DB schema", tags=["backend", "cache", "system design"], estimated_hours=30),
        RecommendedProjectDef("Task Queue Worker", "Async job queue worker with retries and dead-letter handling", tags=["backend", "queue", "worker"], estimated_hours=30),
    ],
    readiness_weights=BACKEND_READINESS_WEIGHTS,
)
ROLE_PROFILES["backend"] = backend_profile

# Convenience accessor
def get_profile(role_name: str) -> RoleProfile | None:
    """Get role profile by name."""
    return ROLE_PROFILES.get(role_name.lower())

# List all registered profiles
def list_profiles() -> List[str]:
    """List all registered role profile names."""
    return list(ROLE_PROFILES.keys())


# Curated role options for the "I NEED A JOB" onboarding door.
# Each maps a public label + key to a registered role profile.
DOOR_JOB_ROLES = [
    {"key": "sde", "label": "Software Developer"},
    {"key": "ai_software_developer", "label": "AI Software Developer"},
    {"key": "data_analyst", "label": "Data Analyst"},
    {"key": "data_scientist", "label": "Data Scientist"},
    {"key": "qa_automation", "label": "QA / Automation"},
    {"key": "frontend", "label": "Frontend Developer"},
    {"key": "backend", "label": "Backend Developer"},
    {"key": "devops", "label": "DevOps"},
    {"key": "cybersecurity", "label": "Cybersecurity"},
]


def door_roles() -> List[Dict[str, str]]:
    """Role options surfaced on the 'I need a job' door."""
    return DOOR_JOB_ROLES


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
    "DOOR_JOB_ROLES",
    "door_roles",
    "SDE_SKILLS",
    "SDE_ASSESSMENTS",
    "SDE_INTERVIEW_TYPES",
    "SDE_RESUME_KEYWORDS",
    "SDE_PROJECTS",
    "SDE_COMPANIES",
    "SDE_READINESS_WEIGHTS",
]