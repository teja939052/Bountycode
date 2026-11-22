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


# =============================================================================
# Service-company placement packages (India)
# =============================================================================

TCS_PACKAGE = RolePackage(
    id="tcs",
    name="TCS NQT Preparation",
    icon="🎉",
    description="TCS National Qualifier Test — Ninja, Digital, Prime tracks. Foundation aptitude + advanced coding.",
    path=[
        RolePath(world_id="foundations", reason="TCS NQT Foundation section tests aptitude and reasoning.", emphasis=["variables", "conditionals", "loops", "functions"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude is 20 questions in Foundation section.", emphasis=["percentages", "profit_loss", "ratio_proportion", "time_work", "time_distance"]),
        RolePath(world_id="aptitude_reasoning", reason="Reasoning ability is 20 questions in Foundation section.", emphasis=["series", "coding_decoding", "blood_relation", "direction_sense"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability is 25 questions in Foundation section.", emphasis=["reading_comprehension", "sentence_correction"]),
        RolePath(world_id="problem_solver", reason="Advanced Coding section gates Digital/Prime eligibility.", emphasis=["arrays", "strings", "hashing", "two_pointers"]),
        RolePath(world_id="under_pressure", reason="190-minute integrated test with section time limits.", emphasis=["timed_coding", "pattern_recognition"]),
        RolePath(world_id="hiring_arena", reason="Ninja/Digital/Prime interview rounds.", emphasis=["coding_interviews"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "C Programming", "DSA Basics"],
    targets=["TCS Ninja", "TCS Digital", "TCS Prime"],
    estimated_hours=100,
)

INFOSYS_PACKAGE = RolePackage(
    id="infosys",
    name="Infosys Preparation",
    icon="🌱",
    description="Infosys Systems Engineer and Specialist Programmer — aptitude + coding + behavioral.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals for coding round.", emphasis=["variables", "loops", "functions", "collections"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "time_work", "time_distance", "averages"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation", "syllogisms"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar", "vocabulary"]),
        RolePath(world_id="problem_solver", reason="Coding round tests DSA and problem solving.", emphasis=["arrays", "sorting", "searching", "hashing"]),
        RolePath(world_id="communication", reason="HR and behavioral interview round.", emphasis=["spoken_english", "email_writing", "behavioral_star"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Java/Python", "DSA Basics", "Communication"],
    targets=["Infosys Systems Engineer", "Infosys Specialist Programmer"],
    estimated_hours=90,
)

WIPRO_PACKAGE = RolePackage(
    id="wipro",
    name="Wipro NLTH Preparation",
    icon="🐀",
    description="Wipro National Level Talent Hunt — aptitude, coding, written communication.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "conditionals", "loops", "functions"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "profit_loss", "time_work", "time_distance"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation", "direction_sense"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "sentence_correction"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "strings", "basic_programming"]),
        RolePath(world_id="communication", reason="Written communication assessment.", emphasis=["email_writing", "grammar"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews", "behavioral_star"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "C/Java/Python", "Written Communication"],
    targets=["Wipro ELITE", "Wipro Turbo"],
    estimated_hours=80,
)

ACCENTURE_PACKAGE = RolePackage(
    id="accenture",
    name="Accenture Preparation",
    icon="💻",
    description="Accenture hiring — cognitive assessment, coding, communication, system design.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "loops", "functions", "collections"]),
        RolePath(world_id="aptitude_quant", reason="Cognitive assessment - numerical ability.", emphasis=["percentages", "time_work", "time_distance", "averages"]),
        RolePath(world_id="aptitude_reasoning", reason="Cognitive assessment - logical ability.", emphasis=["series", "coding_decoding", "blood_relation", "syllogisms"]),
        RolePath(world_id="aptitude_verbal", reason="Cognitive assessment - verbal ability.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Coding assessment.", emphasis=["arrays", "sorting", "searching"]),
        RolePath(world_id="communication", reason="Communication assessment.", emphasis=["spoken_english", "email_writing"]),
        RolePath(world_id="cs_fundamentals", reason="Technical interview - CS fundamentals.", emphasis=["oops", "operating_systems", "networking"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews", "system_design"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Java/Python", "CS Fundamentals", "Communication"],
    targets=["Accenture Associate", "Accenture Application Developer"],
    estimated_hours=100,
)

CAPGEMINI_PACKAGE = RolePackage(
    id="capgemini",
    name="Capgemini Preparation",
    icon="👨‍💻",
    description="Capgemini hiring — aptitude, pseudocode, behavioral.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals for pseudocode round.", emphasis=["variables", "conditionals", "loops", "functions"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "profit_loss", "time_work"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Pseudocode and coding round.", emphasis=["basic_programming", "arrays", "loops"]),
        RolePath(world_id="communication", reason="Behavioral interview.", emphasis=["spoken_english", "behavioral_star"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Pseudocode", "C/Java", "Behavioral"],
    targets=["Capgemini Associate", "Capgemini Analyst"],
    estimated_hours=80,
)

IBM_PACKAGE = RolePackage(
    id="ibm",
    name="IBM Preparation",
    icon="📀",
    description="IBM hiring — cognitive ability, coding, technical interview.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "loops", "functions", "collections"]),
        RolePath(world_id="aptitude_quant", reason="Cognitive ability - numerical.", emphasis=["percentages", "time_work", "time_distance"]),
        RolePath(world_id="aptitude_reasoning", reason="Cognitive ability - logical.", emphasis=["series", "coding_decoding", "blood_relation"]),
        RolePath(world_id="aptitude_verbal", reason="Cognitive ability - verbal.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "strings", "hashing"]),
        RolePath(world_id="cs_fundamentals", reason="Technical interview - CS fundamentals.", emphasis=["oops", "operating_systems", "dbms"]),
        RolePath(world_id="sql_dbms", reason="SQL questions in technical round.", emphasis=["sql_select", "sql_where", "sql_joins"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews", "system_design"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Java/Python", "CS Fundamentals", "SQL"],
    targets=["IBM Associate System Engineer", "IBM Application Developer"],
    estimated_hours=90,
)

COGNIZANT_PACKAGE = RolePackage(
    id="cognizant",
    name="Cognizant GenC Preparation",
    icon="\U0001f4e6",
    description="Cognizant GenC hiring — aptitude, communication, coding, behavioral.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals for aptitude round.", emphasis=["variables", "conditionals", "loops", "functions"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "profit_loss", "time_work", "time_distance"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation", "direction_sense"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar", "vocabulary"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "strings", "basic_programming"]),
        RolePath(world_id="communication", reason="Communication round.", emphasis=["spoken_english", "email_writing", "group_discussion"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews", "behavioral_star"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "C/Java/Python", "Communication", "Behavioral"],
    targets=["Cognizant GenC", "Cognizant GenC Next"],
    estimated_hours=85,
)

HCLTECH_PACKAGE = RolePackage(
    id="hcltech",
    name="HCLTech Preparation",
    icon="\U0001f4bb",
    description="HCLTech hiring — aptitude, coding, technical interview.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "loops", "functions", "collections"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "time_work", "time_distance", "averages"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation", "syllogisms"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "sorting", "searching", "hashing"]),
        RolePath(world_id="cs_fundamentals", reason="Technical interview - CS fundamentals.", emphasis=["oops", "operating_systems", "networking"]),
        RolePath(world_id="communication", reason="Communication round.", emphasis=["spoken_english", "behavioral_star"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Java/Python", "CS Fundamentals", "Communication"],
    targets=["HCLTech Graduate Engineer Trainee"],
    estimated_hours=85,
)

TECH_MAHINDRA_PACKAGE = RolePackage(
    id="tech_mahindra",
    name="Tech Mahindra Preparation",
    icon="\U0001f310",
    description="Tech Mahindra hiring — aptitude, English, coding, behavioral.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "conditionals", "loops", "functions"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "profit_loss", "time_work"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "strings", "basic_programming"]),
        RolePath(world_id="communication", reason="English and communication round.", emphasis=["spoken_english", "email_writing"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews", "behavioral_star"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "C/Java/Python", "Communication", "Behavioral"],
    targets=["Tech Mahindra GET"],
    estimated_hours=80,
)

LTIMINDTREE_PACKAGE = RolePackage(
    id="lti_mindtree",
    name="LTIMindtree Preparation",
    icon="\U0001f4f1",
    description="LTIMindtree hiring — aptitude, coding, communication, CS fundamentals.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "loops", "functions", "collections"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "time_work", "time_distance"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation", "syllogisms"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "sorting", "searching"]),
        RolePath(world_id="cs_fundamentals", reason="Technical interview - CS fundamentals.", emphasis=["oops", "operating_systems", "dbms"]),
        RolePath(world_id="communication", reason="Communication round.", emphasis=["spoken_english", "email_writing"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews", "system_design"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Java/Python", "CS Fundamentals", "Communication"],
    targets=["LTIMindtree GET"],
    estimated_hours=90,
)

MPHASIS_PACKAGE = RolePackage(
    id="mphasis",
    name="Mphasis Preparation",
    icon="\U0001f4ca",
    description="Mphasis hiring — aptitude, logical reasoning, coding, behavioral.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "conditionals", "loops", "functions"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "profit_loss", "ratio_proportion", "time_work"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation", "direction_sense"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "sentence_correction"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "strings", "basic_programming"]),
        RolePath(world_id="communication", reason="Behavioral interview.", emphasis=["spoken_english", "behavioral_star"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "C/Java/Python", "Behavioral"],
    targets=["Mphasis Associate Software Engineer"],
    estimated_hours=80,
)

HEXAWARE_PACKAGE = RolePackage(
    id="hexaware",
    name="Hexaware Preparation",
    icon="\U0001f4d0",
    description="Hexaware hiring — aptitude, coding, communication, technical interview.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "loops", "functions", "collections"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "time_work", "time_distance"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "sorting", "searching"]),
        RolePath(world_id="communication", reason="Communication round.", emphasis=["spoken_english", "email_writing"]),
        RolePath(world_id="cs_fundamentals", reason="Technical interview - CS fundamentals.", emphasis=["oops", "dbms"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Java/Python", "CS Fundamentals", "Communication"],
    targets=["Hexaware Trainee Engineer"],
    estimated_hours=80,
)

PERSISTENT_PACKAGE = RolePackage(
    id="persistent",
    name="Persistent Systems Preparation",
    icon="\U0001f527",
    description="Persistent Systems hiring — aptitude, coding, CS fundamentals, technical interview.",
    path=[
        RolePath(world_id="foundations", reason="Programming fundamentals.", emphasis=["variables", "loops", "functions", "collections"]),
        RolePath(world_id="aptitude_quant", reason="Quantitative aptitude section.", emphasis=["percentages", "time_work", "time_distance"]),
        RolePath(world_id="aptitude_reasoning", reason="Logical reasoning section.", emphasis=["series", "coding_decoding", "blood_relation"]),
        RolePath(world_id="aptitude_verbal", reason="Verbal ability section.", emphasis=["reading_comprehension", "grammar"]),
        RolePath(world_id="problem_solver", reason="Coding round.", emphasis=["arrays", "strings", "hashing"]),
        RolePath(world_id="cs_fundamentals", reason="Technical interview - CS fundamentals.", emphasis=["oops", "operating_systems", "networking", "dbms"]),
        RolePath(world_id="sql_dbms", reason="SQL questions in technical round.", emphasis=["sql_select", "sql_where", "sql_joins"]),
        RolePath(world_id="communication", reason="Communication round.", emphasis=["spoken_english", "behavioral_star"]),
        RolePath(world_id="hiring_arena", reason="Technical and HR interviews.", emphasis=["coding_interviews", "system_design"]),
    ],
    skills=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Java/Python", "CS Fundamentals", "SQL", "Communication"],
    targets=["Persistent Systems GET"],
    estimated_hours=90,
)

# =============================================================================
# Registry
# =============================================================================

ROLE_PACKAGES: Dict[str, RolePackage] = {
    SDE_PACKAGE.id: SDE_PACKAGE,
    DATA_SCIENTIST_PACKAGE.id: DATA_SCIENTIST_PACKAGE,
    ML_ENGINEER_PACKAGE.id: ML_ENGINEER_PACKAGE,
    DEVOPS_PACKAGE.id: DEVOPS_PACKAGE,
    FRONTEND_PACKAGE.id: FRONTEND_PACKAGE,
    CP_PACKAGE.id: CP_PACKAGE,
    TCS_PACKAGE.id: TCS_PACKAGE,
    INFOSYS_PACKAGE.id: INFOSYS_PACKAGE,
    WIPRO_PACKAGE.id: WIPRO_PACKAGE,
    ACCENTURE_PACKAGE.id: ACCENTURE_PACKAGE,
    CAPGEMINI_PACKAGE.id: CAPGEMINI_PACKAGE,
    IBM_PACKAGE.id: IBM_PACKAGE,
    COGNIZANT_PACKAGE.id: COGNIZANT_PACKAGE,
    HCLTECH_PACKAGE.id: HCLTECH_PACKAGE,
    TECH_MAHINDRA_PACKAGE.id: TECH_MAHINDRA_PACKAGE,
    LTIMINDTREE_PACKAGE.id: LTIMINDTREE_PACKAGE,
    MPHASIS_PACKAGE.id: MPHASIS_PACKAGE,
    HEXAWARE_PACKAGE.id: HEXAWARE_PACKAGE,
    PERSISTENT_PACKAGE.id: PERSISTENT_PACKAGE,
}
def get_role_package(role_id: str) -> Optional[RolePackage]:
    return ROLE_PACKAGES.get(role_id)


def all_roles() -> List[RolePackage]:
    return list(ROLE_PACKAGES.values())


def roles_for_world(world_id: str) -> List[RolePackage]:
    """Return all roles that include a given world in their path."""
    return [r for r in ROLE_PACKAGES.values() if any(p.world_id == world_id for p in r.path)]
