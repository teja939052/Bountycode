"""Expand all worlds to be world-class with full teaching loops.

This script expands worlds 3-12 by adding more lessons and ensuring
all lessons have the full teaching loop pattern.

Governance: the served world set is the canonical 12-world manifest
(CANONICAL_WORLDS in backend/scripts/verify_world_governance.py).
"""
from __future__ import annotations

from app.content.lesson_definitions import (
    LessonDefinition, LessonStep, TownDefinition, WorldDefinition,
)
from app.content.worlds_3_to_6 import API_TOWN, DB_TOWN, DATA_TOWN, GIT_TOWN, TESTING_TOWN, OA_TOWN
from app.content.worlds_7_to_9 import CODING_INTERVIEW_TOWN, SYSTEM_DESIGN_TOWN, AMAZON_TOWN, LLM_TOWN
from app.content.worlds_10_to_12 import RELIABILITY_TOWN, SECURITY_TOWN, URL_SHORTENER_TOWN, OPEN_ENDED_TOWN

# ═══════════════════════════════════════════════════════════════════
# WORLD 3 — BUILD SYSTEMS (Expanded)
# ═══════════════════════════════════════════════════════════════════

AUTH_TOWN = TownDefinition(
    id="auth", name="Authentication", icon="🔐",
    description="Who are you? Prove it.",
    order=3, mental_model="Authentication = identity (who) + proof (password/token) + session (remember me).",
    canonical_skills=["backend.auth"], competencies=["jwt", "sessions", "oauth", "passwords"],
    lessons=[
        LessonDefinition(
            id="auth-1", title="Password Hashing", icon="🔒", order=1, concept="hashing",
            mental_model="Never store plaintext passwords. Hash with bcrypt/argon2 — one-way, salted, slow.",
            canonical_skill="backend.hashing",
            why_this_matters="Password databases are the #1 target in breaches. Plaintext passwords = immediate account takeover. Hashing means even if the DB leaks, attackers can't reverse passwords.",
            engineering_context="In production, bcrypt with cost factor 12 is standard. Each hash takes ~100ms, making brute-force attacks impractical. Salts prevent rainbow table attacks. This is non-negotiable security.",
            builds_toward="Backend Engineering — security fundamentals",
            steps=[
                LessonStep(step_type="discover", title="The Breach",
                    content="Adobe 2013: 150M passwords, plaintext. LinkedIn 2012: 6.5M passwords, unsalted SHA1. Both preventable with hashing."),
                LessonStep(step_type="predict", title="Hash or Plain?",
                    question="Which storage is secure?",
                    options=[
                        {"id":"a","text":"bcrypt with salt","correct":True},
                        {"id":"b","text":"plaintext","correct":False},
                        {"id":"c","text":"MD5 without salt","correct":False},
                    ],
                    explanation="bcrypt is slow and salted. MD5 is fast and unsalted. Plaintext is never acceptable.",
                ),
                LessonStep(step_type="build", title="Hash a Password",
                    function_name="hash_password", signature="def hash_password(password: str) -> str:",
                    description="Return a bcrypt hash of the password. Use bcrypt.hashpw().",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "import bcrypt\ndef solution(): pass", "java": "public static String solution() { return null; }", "cpp": "std::string solution() { return \"\"; }", "c": "char* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static String solution()", "cpp": "std::string solution()", "c": "char* solution()"},
                    test_cases=[{"input":["password123"],"expected":"hash"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Use bcrypt properly",
                            "content": "bcrypt.hashpw(password.encode(), bcrypt.gensalt()) returns a bytes hash. Decode to string if needed.",
                            "hint": "Don't roll your own crypto. Use the library.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="break", title="The Timing Attack",
                    content="bcrypt is slow (~100ms). Why is that a feature, not a bug?",
                    question="Why should password hashing be slow?",
                    options=[
                        {"id":"a","text":"To limit brute-force attempts","correct":True},
                        {"id":"b","text":"To save CPU","correct":False},
                    ],
                    explanation="Slow hashing makes each guess expensive. An attacker can only try ~10 passwords/second, not millions.",
                ),
                LessonStep(step_type="debug", title="Fix the Auth Bug",
                    content="This code stores plaintext passwords. Fix it.",
                    buggy_code="def register(username, password):\n    db.save(username, password)  # plaintext!",
                    fix_steps=["Hash the password before storing", "Use bcrypt.genhashpw()"],
                    function_name="register_secure",
                    signature="def register_secure(username: str, password: str) -> str:",
                    description="Return the hashed password to store.",
                    test_cases=[{"input":["admin","secret"],"expected":"hash"}], hidden_tests=2,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Hash Before Store",
                            "content": "Never store plaintext. Hash the password first: bcrypt.hashpw(password.encode(), bcrypt.gensalt()).",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="Recall: Hashing",
                    content="Without looking — why must password hashing be slow?",
                    prompt="Password hashing must be slow because…",
                    answer="it limits brute-force attempts",
                ),
                LessonStep(step_type="transfer", title="Secure the API",
                    content="Apply hashing to a new context: user registration endpoint.",
                    function_name="register_endpoint",
                    signature="def register_endpoint(username: str, password: str) -> dict:",
                    description="Return {username, password_hash} with password hashed via bcrypt.",
                    test_cases=[
                        {"input":["alice","secret"],"expected":{"username":"alice","password_hash":"hash"}},
                    ],
                    hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Return the Right Shape",
                            "content": "Return a dict with username and password_hash keys. The hash should be a string, not bytes.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="mastery", title="Auth System Design",
                    content="Design a complete authentication system.",
                    function_name="design_auth",
                    signature="def design_auth() -> dict:",
                    description="Return: hashing algorithm, salt strategy, session management, password reset flow.",
                    test_cases=[{"input":[],"expected":"auth"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover All Components",
                            "content": "Your auth system needs: hashing (bcrypt/argon2), salt (built-in to bcrypt), sessions (JWT or cookies), and password reset (token-based email).",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Hash passwords securely", "Explain why slow hashing matters", "Design auth systems"],
            unlocks="auth-2",
        ),
        LessonDefinition(
            id="auth-2", title="JWT Tokens", icon="🎫", order=2, concept="jwt",
            mental_model="JWT = header.payload.signature. Stateless auth: server doesn't store sessions, token proves identity.",
            canonical_skill="backend.jwt",
            why_this_matters="JWTs are how modern APIs authenticate users without sessions. Stateless = horizontally scalable. No Redis needed for sessions. The token IS the session.",
            engineering_context="In microservices, JWTs propagate identity across services: API gateway validates JWT, passes user_id to downstream services. No shared session store. This is the standard for distributed systems.",
            builds_toward="Backend Engineering — stateless authentication",
            steps=[
                LessonStep(step_type="build", title="Create a Token",
                    function_name="create_token", signature="def create_token(user_id: int) -> str:",
                    description="Return a JWT token with user_id in payload, signed with a secret.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "import jwt\ndef solution(): pass", "java": "public static String solution() { return null; }", "cpp": "std::string solution() { return \"\"; }", "c": "char* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static String solution()", "cpp": "std::string solution()", "c": "char* solution()"},
                    test_cases=[{"input":[1],"expected":"token"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Sign the Token",
                            "content": "Use jwt.encode({'user_id': user_id}, SECRET, algorithm='HS256'). Don't forget the algorithm.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="JWT Structure",
                    content="Without looking — what are the three parts of a JWT?",
                    prompt="JWT = header . payload . signature",
                    answer="header, payload, signature",
                ),
            ],
            mastery_evidence=["Create and validate JWT tokens"],
            unlocks="auth-boss",
        ),
        LessonDefinition(
            id="auth-boss", title="Auth Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Complete auth system: register, login, protected routes, token refresh.",
            canonical_skill="backend.auth", diamonds=100, estimated_minutes=20,
            engineering_context="A real auth system: POST /register (hash password), POST /login (verify hash, issue JWT), GET /me (validate JWT), POST /refresh (rotate tokens). This boss tests that full flow.",
            builds_toward="Backend Engineering — complete authentication system",
            steps=[
                LessonStep(step_type="mastery", title="Auth Flow",
                    function_name="auth_flow", signature="def auth_flow() -> dict:",
                    description="Return: register, login, protected route, token refresh endpoints with auth logic.",
                    test_cases=[{"input":[],"expected":"flow"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover the Full Flow",
                            "content": "Your auth system needs: registration with hashing, login with JWT issuance, protected route middleware, and token refresh logic.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Hash passwords", "Issue JWTs", "Design auth flows"],
        ),
    ],
)

CACHE_TOWN = TownDefinition(
    id="caching", name="Caching", icon="⚡",
    description="Speed through memory.",
    order=4, mental_model="Cache hot data in fast storage. Trade space for time. Invalidate when stale.",
    canonical_skills=["performance.caching"], competencies=["redis", "ttl", "eviction", "cache_aside", "write_through"],
    lessons=[
        LessonDefinition(
            id="cache-1", title="Cache Aside", icon="📦", order=1, concept="cache_aside",
            mental_model="Read: check cache → miss → query DB → write cache. Write: update DB → invalidate cache.",
            canonical_skill="performance.cache_aside",
            why_this_matters="Cache aside is the most common caching pattern. It's simple, works for reads, and handles DB failures gracefully. Every high-traffic system uses it.",
            engineering_context="In production, cache aside powers: user profiles, product catalogs, session data. Cache hit: <1ms. DB query: 10-100ms. The difference is user experience.",
            builds_toward="Performance Engineering — caching strategies",
            steps=[
                LessonStep(step_type="discover", title="The Pattern",
                    content="Cache miss → DB → Cache write. Next request: cache hit → instant response."),
                LessonStep(step_type="build", title="Implement Cache Aside",
                    function_name="get_user", signature="def get_user(user_id: int) -> dict:",
                    description="Return user from cache if present, else query DB and cache. Simulate with dict.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "cache = {}\ndef solution(): pass", "java": "public static Map<Integer, Object> cache = new HashMap<>(); public static Object solution() { return null; }", "cpp": "std::unordered_map<int, std::string> cache;\nstd::string solution() { return \"\"; }", "c": "// cache simulation\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static Object solution()", "cpp": "std::string solution()", "c": "char* solution()"},
                    test_cases=[{"input":[1],"expected":"user"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Check Cache First",
                            "content": "The pattern is: 1) Check cache, 2) If miss, query DB, 3) Write to cache, 4) Return. Don't skip the cache check.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="Cache Invalidation",
                    content="Without looking — when should you invalidate a cache entry?",
                    prompt="Invalidate cache when…",
                    answer="the underlying data changes",
                ),
            ],
            mastery_evidence=["Implement cache aside pattern", "Handle cache invalidation"],
            unlocks="cache-2",
        ),
        LessonDefinition(
            id="cache-2", title="TTL & Eviction", icon="⏰", order=2, concept="ttl",
            mental_model="Every cache entry needs a lifetime. TTL expires stale data. Eviction policies (LRU, LFU) decide what to remove when full.",
            canonical_skill="performance.ttl",
            why_this_matters="Without TTL, caches grow forever. Without eviction, full caches reject new entries. TTL + eviction = bounded, fresh cache.",
            engineering_context="In Redis, EXPIRE sets TTL. maxmemory-policy sets eviction: allkeys-lru (default), volatile-lru, allkeys-lfu. These settings determine cache behavior under pressure.",
            builds_toward="Performance Engineering — cache lifecycle management",
            steps=[
                LessonStep(step_type="predict", title="TTL Choice",
                    question="User profiles change rarely. What TTL makes sense?",
                    options=[
                        {"id":"a","text":"1 hour","correct":True},
                        {"id":"b","text":"1 second","correct":False},
                        {"id":"c","text":"Never expire","correct":False},
                    ],
                    explanation="1 hour balances freshness and hit rate. Too short = poor hit rate. Too long = stale data.",
                ),
            ],
            mastery_evidence=["Choose appropriate TTL and eviction policies"],
            unlocks="cache-boss",
        ),
        LessonDefinition(
            id="cache-boss", title="Cache Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Design a caching strategy for a high-traffic system.",
            canonical_skill="performance.caching", diamonds=100, estimated_minutes=20,
            engineering_context="In a real system, you'd: identify hot data, choose cache size, set TTLs, handle cache stampede, and design fallback. This boss tests that complete strategy.",
            builds_toward="Performance Engineering — complete caching design",
            steps=[
                LessonStep(step_type="mastery", title="Cache Strategy",
                    function_name="cache_strategy", signature="def cache_strategy() -> dict:",
                    description="Return: cache key design, TTL policy, eviction strategy, and fallback for cache failure.",
                    test_cases=[{"input":[],"expected":"strategy"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover the Strategy",
                            "content": "Your strategy needs: key naming convention, TTL values per data type, eviction policy, and what happens when cache is down.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design caching strategies", "Choose TTL and eviction", "Handle cache failures"],
        ),
    ],
)

WORLD_3_BUILD_SYSTEMS = WorldDefinition(
    id="build_systems", name="Build Systems", icon="🏗️",
    subtitle="APIs + Databases + Auth + Caching",
    description="Learn how real systems are built: APIs, databases, authentication, caching, and the backend logic connecting them.",
    order=3, theme="build_systems", towns=[API_TOWN, DB_TOWN, AUTH_TOWN, CACHE_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 4 — WORK WITH DATA (Expanded)
# ═══════════════════════════════════════════════════════════════════

ETL_TOWN = TownDefinition(
    id="etl", name="ETL Pipelines", icon="🔄",
    description="Extract, Transform, Load. Move data from A to B.",
    order=2, mental_model="ETL = pull from source → clean/transform → load to destination. The backbone of analytics.",
    canonical_skills=["data.etl"], competencies=["extraction", "transformation", "loading", "scheduling", "data_quality"],
    lessons=[
        LessonDefinition(
            id="etl-1", title="Extract & Clean", icon="🧹", order=1, concept="extraction",
            mental_model="Data is dirty. Extract from source, handle missing values, remove duplicates, standardize formats.",
            canonical_skill="data.extraction",
            why_this_matters="80% of data work is cleaning. Raw data has nulls, duplicates, wrong formats. ETL pipelines clean this before analysis. Bad data = bad decisions.",
            engineering_context="In production, ETL jobs run on Airflow: extract from DB/API, clean with Pandas/SQL, load to warehouse. Data quality checks (null counts, uniqueness) gate the pipeline.",
            builds_toward="Data Engineering — ETL and data quality",
            steps=[
                LessonStep(step_type="discover", title="Dirty Data",
                    content="A CSV has: null emails, duplicate rows, dates in 3 formats. Clean it before loading."),
                LessonStep(step_type="build", title="Clean the Data",
                    function_name="clean_data", signature="def clean_data(rows: list) -> list:",
                    description="Remove rows with null emails, deduplicate, standardize dates to ISO format.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static List<Map<String, Object>> solution() { return null; }", "cpp": "std::vector<std::map<std::string, std::string>> solution() { return {}; }", "c": "// data cleaning\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static List<Map<String, Object>> solution()", "cpp": "std::vector<std::map<std::string, std::string>> solution()", "c": "char* solution()"},
                    test_cases=[{"input":[[{'email':'a@b.com','date':'2024-01-01'},{'email':None,'date':'2024-01-02'}]],"expected":1}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Filter Nulls and Duplicates",
                            "content": "Remove rows where email is None/empty. Then deduplicate by email. Finally standardize date formats.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="Data Quality",
                    content="Without looking — what are the three most common data quality issues?",
                    prompt="Common issues: null values, duplicates, and…",
                    answer="inconsistent formats",
                ),
            ],
            mastery_evidence=["Clean raw data", "Handle missing values", "Remove duplicates"],
            unlocks="etl-2",
        ),
        LessonDefinition(
            id="etl-2", title="Transform & Load", icon="🚚", order=2, concept="transformation",
            mental_model="Transform: aggregate, join, pivot. Load: insert into target, handle conflicts, verify row counts.",
            canonical_skill="data.transformation",
            why_this_matters="Transformation turns raw data into analytics-ready tables. Loading writes it to the destination. Getting this wrong means dashboards show wrong numbers.",
            engineering_context="In production, dbt (data build tool) transforms data in the warehouse: SQL models that clean, join, and aggregate. Airflow orchestrates the schedule. Data quality tests gate promotion.",
            builds_toward="Data Engineering — transformation and loading",
            steps=[
                LessonStep(step_type="build", title="Transform Sales Data",
                    function_name="transform_sales", signature="def transform_sales(rows: list) -> dict:",
                    description="Group by category, sum amounts, return {category: total}.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static Map<String, Double> solution() { return null; }", "cpp": "std::map<std::string, double> solution() { return {}; }", "c": "// transform\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static Map<String, Double> solution()", "cpp": "std::map<std::string, double> solution()", "c": "char* solution()"},
                    test_cases=[{"input":[[{'category':'A','amount':10},{'category':'B','amount':20}]],"expected":{"A":10.0,"B":20.0}}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Group and Sum",
                            "content": "Iterate rows, accumulate amounts by category in a dict/map. Return the aggregated result.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Transform data with aggregation", "Load to destination"],
            unlocks="etl-boss",
        ),
        LessonDefinition(
            id="etl-boss", title="ETL Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Design a complete ETL pipeline for a real analytics use case.",
            canonical_skill="data.etl", diamonds=100, estimated_minutes=20,
            engineering_context="A real ETL pipeline: extract from transactional DB, clean nulls/duplicates, transform (daily aggregations), load to warehouse, verify with data quality checks.",
            builds_toward="Data Engineering — complete pipeline design",
            steps=[
                LessonStep(step_type="mastery", title="Daily Sales Pipeline",
                    function_name="daily_sales_pipeline", signature="def daily_sales_pipeline() -> dict:",
                    description="Return: extract query, clean rules, transform logic, load target, verification query.",
                    test_cases=[{"input":[],"expected":"pipeline"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: End-to-End Pipeline",
                            "content": "Your pipeline needs: extract (SELECT from source), clean (WHERE valid), transform (GROUP BY), load (INSERT), verify (COUNT check).",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design ETL pipelines", "Clean and transform data", "Verify data quality"],
        ),
    ],
)

WORLD_4_WORK_WITH_DATA = WorldDefinition(
    id="work_with_data", name="Work With Data", icon="📊",
    subtitle="SQL + Analytics + ETL",
    description="Turn raw data into decisions with SQL, aggregation, analytics, and ETL pipelines.",
    order=4, theme="work_with_data", towns=[DATA_TOWN, ETL_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 5 — SOFTWARE ENGINEERING (Expanded)
# ═══════════════════════════════════════════════════════════════════

CI_TOWN = TownDefinition(
    id="ci_cd", name="CI/CD", icon="🔄",
    description="Automate the pipeline. Code → Test → Deploy.",
    order=3, mental_model="CI runs tests on every commit. CD deploys if tests pass. Automation removes human error.",
    canonical_skills=["engineering.ci_cd"], competencies=["pipelines", "automated_testing", "deployment", "rollback"],
    lessons=[
        LessonDefinition(
            id="ci-1", title="GitHub Actions", icon="⚙️", order=1, concept="pipelines",
            mental_model="A CI pipeline is code: on push → install → test → lint → deploy. YAML defines the workflow.",
            canonical_skill="engineering.pipelines",
            why_this_matters="CI/CD is how teams ship fast and safe. Every commit runs automated tests. If tests pass, deploy. If not, block. This prevents bugs from reaching production.",
            engineering_context="In production, GitHub Actions/GitLab CI runs: checkout code → install dependencies → run tests → lint → security scan → build Docker image → deploy. All automated on every PR.",
            builds_toward="DevOps — automated delivery pipelines",
            steps=[
                LessonStep(step_type="discover", title="The Pipeline",
                    content="on: push\njobs:\n  test:\n    runs-on: ubuntu\n    steps:\n      - uses: actions/checkout\n      - run: pytest"),
                LessonStep(step_type="build", title="Write a Workflow",
                    function_name="ci_workflow", signature="def ci_workflow() -> str:",
                    description="Return YAML for a GitHub Action: on push to main, run pytest.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static String solution() { return null; }", "cpp": "std::string solution() { return \"\"; }", "c": "char* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static String solution()", "cpp": "std::string solution()", "c": "char* solution()"},
                    test_cases=[{"input":[],"expected":"yaml"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: YAML Structure",
                            "content": "GitHub Actions need: 'on:' trigger, 'jobs:' with job id, 'runs-on:', and 'steps:' with uses/run.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="CI Benefits",
                    content="Without looking — what does CI stand for and why does it matter?",
                    prompt="CI = Continuous Integration. It matters because…",
                    answer="it runs tests automatically on every commit",
                ),
            ],
            mastery_evidence=["Write CI pipeline configurations", "Explain CI/CD benefits"],
            unlocks="ci-2",
        ),
        LessonDefinition(
            id="ci-2", title="Automated Testing in CI", icon="🧪", order=2, concept="automated_testing",
            mental_model="CI runs unit, integration, and E2E tests. Fail fast: one failure blocks deploy.",
            canonical_skill="engineering.automated_testing",
            why_this_matters="Automated tests in CI catch bugs before they reach production. A failing test blocks the deploy, forcing the developer to fix before merging. This is how teams ship with confidence.",
            engineering_context="In production, CI runs: unit tests (pytest/jest), integration tests (Testcontainers), E2E tests (Playwright), and security scans (Snyk). All must pass for merge.",
            builds_toward="DevOps — quality gates in pipelines",
            steps=[
                LessonStep(step_type="build", title="Add Test Steps",
                    function_name="add_tests", signature="def add_tests() -> list:",
                    description="Return list of test commands: unit, integration, e2e, lint.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static List<String> solution() { return null; }", "cpp": "std::vector<std::string> solution() { return {}; }", "c": "// tests\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static List<String> solution()", "cpp": "std::vector<std::string> solution()", "c": "char* solution()"},
                    test_cases=[{"input":[],"expected":["pytest","lint"]}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover All Test Types",
                            "content": "Add: unit tests (pytest/jest), integration tests, E2E tests, and lint/typecheck. Each is a separate step.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Configure automated testing in CI"],
            unlocks="ci-boss",
        ),
        LessonDefinition(
            id="ci-boss", title="CI/CD Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Design a complete CI/CD pipeline for a real project.",
            canonical_skill="engineering.ci_cd", diamonds=100, estimated_minutes=20,
            engineering_context="A real pipeline: on PR → lint + unit tests. On merge to main → integration tests + build + deploy to staging. On tag → deploy to prod with smoke tests.",
            builds_toward="DevOps — complete delivery automation",
            steps=[
                LessonStep(step_type="mastery", title="Full Pipeline",
                    function_name="full_pipeline", signature="def full_pipeline() -> dict:",
                    description="Return: PR checks, main branch pipeline, production deploy, rollback strategy.",
                    test_cases=[{"input":[],"expected":"pipeline"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover All Stages",
                            "content": "Your pipeline needs: PR checks (lint, unit), main checks (integration, build), deploy (staging, prod), and rollback strategy.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design CI/CD pipelines", "Configure automated tests", "Plan deployment and rollback"],
        ),
    ],
)

WORLD_5_SOFTWARE_ENGINEERING = WorldDefinition(
    id="software_engineering", name="Software Engineering", icon="🛠️",
    subtitle="Git + Testing + CI/CD + Quality",
    description="Professional engineering practices: version control, testing, CI/CD, code review, and quality.",
    order=5, theme="software_engineering", towns=[GIT_TOWN, TESTING_TOWN, CI_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 6 — UNDER PRESSURE (Expanded)
# ═══════════════════════════════════════════════════════════════════

APTITUDE_TOWN = TownDefinition(
    id="aptitude", name="Aptitude", icon="🧮",
    description="Quant, logical, verbal — the Indian OA staple.",
    order=2, mental_model="Aptitude tests pattern recognition + speed. Know the formulas, practice the patterns, manage the time.",
    canonical_skills=["aptitude.quant"], competencies=["time_work", "percentages", "profit_loss", "ratio", "speed_distance"],
    lessons=[
        LessonDefinition(
            id="apt-1", title="Time & Work", icon="⏱️", order=1, concept="time_work",
            mental_model="Work = Rate × Time. Combined rates add. If A does 1/3/day and B does 1/4/day, together they do 7/12/day.",
            canonical_skill="aptitude.time_work",
            why_this_matters="Time & Work is the most common quant topic in TCS NQT, Infosys, Wipro. It's formula-based and fast to solve once you know the pattern.",
            engineering_context="In real projects, this maps to: if developer A finishes in 3 days and B in 4, together they take (3×4)/(3+4) = 12/7 days. Resource estimation uses the same math.",
            builds_toward="Indian Placement — quant aptitude",
            steps=[
                LessonStep(step_type="discover", title="The Formula",
                    content="A: 1/x, B: 1/y. Together: 1/(1/x + 1/y) = xy/(x+y)."),
                LessonStep(step_type="predict", title="Quick Calc",
                    question="A: 3 days, B: 6 days. Together?",
                    options=[
                        {"id":"a","text":"2 days","correct":True},
                        {"id":"b","text":"4 days","correct":False},
                        {"id":"c","text":"9 days","correct":False},
                    ],
                    explanation="Together: (3×6)/(3+6) = 18/9 = 2 days.",
                ),
                LessonStep(step_type="build", title="Solve Time & Work",
                    function_name="time_work", signature="def time_work(a: int, b: int) -> float:",
                    description="Return days for A and B working together. Round to 2 decimals.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static double solution() { return 0; }", "cpp": "double solution() { return 0; }", "c": "double solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static double solution()", "cpp": "double solution()", "c": "double solution()"},
                    test_cases=[{"input":[3,6],"expected":2.0}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Use the Formula",
                            "content": "Formula: (a*b)/(a+b). Don't forget to convert to float for decimal results.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="Recall: Time & Work",
                    content="Without looking — what's the formula for combined work rate?",
                    prompt="Combined rate = 1/(1/a + 1/b) = …",
                    answer="ab/(a+b)",
                ),
            ],
            mastery_evidence=["Solve time & work problems", "Apply combined rate formula"],
            unlocks="apt-2",
        ),
        LessonDefinition(
            id="apt-2", title="Percentages", icon="%", order=2, concept="percentages",
            mental_model="Percentage = (part/whole) × 100. Reverse: if x% of y = z, then x = (z/y) × 100.",
            canonical_skill="aptitude.percentages",
            why_this_matters="Percentages appear in every OA: profit/loss, discounts, data interpretation. Fast percentage math saves time.",
            engineering_context="In analytics, percentages normalize data: 'conversion rate = (purchases/visitors) × 100'. In finance, percentages drive ROI calculations.",
            builds_toward="Indian Placement — quant aptitude",
            steps=[
                LessonStep(step_type="build", title="Calculate Percentage",
                    function_name="percentage", signature="def percentage(part: int, whole: int) -> float:",
                    description="Return (part/whole)*100 rounded to 2 decimals.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static double solution() { return 0; }", "cpp": "double solution() { return 0; }", "c": "double solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static double solution()", "cpp": "double solution()", "c": "double solution()"},
                    test_cases=[{"input":[25,200],"expected":12.5}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Handle Division by Zero",
                            "content": "If whole is 0, return 0.0. Otherwise return (part/whole)*100.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Calculate percentages accurately"],
            unlocks="apt-boss",
        ),
        LessonDefinition(
            id="apt-boss", title="Aptitude Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Solve mixed aptitude problems under time pressure.",
            canonical_skill="aptitude.quant", diamonds=100, estimated_minutes=20,
            engineering_context="In a real OA, you get 20 quant questions in 30 minutes. You need to recognize the pattern and solve in <2 minutes each.",
            builds_toward="Indian Placement — full quant section",
            steps=[
                LessonStep(step_type="mastery", title="Quant Marathon",
                    function_name="quant_marathon", signature="def quant_marathon(problems: list) -> list:",
                    description="Solve a list of mixed quant problems. Return list of answers.",
                    test_cases=[{"input":[[{'type':'time_work','a':3,'b':6}]],"expected":[2.0]}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Handle All Types",
                            "content": "Support: time_work, percentage, profit_loss, ratio. Each has its own formula.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Solve mixed quant problems", "Manage time pressure", "Apply multiple formulas"],
        ),
    ],
)

WORLD_6_UNDER_PRESSURE = WorldDefinition(
    id="under_pressure", name="Under Pressure", icon="⚡",
    subtitle="OA + Aptitude + Debugging",
    description="Perform under time pressure: online assessments, aptitude, debugging, and optimization.",
    order=6, theme="under_pressure", towns=[OA_TOWN, APTITUDE_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 7 — HIRING ARENA (Expanded)
# ═══════════════════════════════════════════════════════════════════

BEHAVIORAL_TOWN = TownDefinition(
    id="behavioral", name="Behavioral", icon="🗣️",
    description="Tell stories that get you hired.",
    order=3, mental_model="Behavioral interviews test EQ: can you work with others, handle conflict, lead, learn from failure?",
    canonical_skills=["interview.behavioral"], competencies=["star_method", "conflict_resolution", "leadership", "failure_stories"],
    lessons=[
        LessonDefinition(
            id="beh-1", title="STAR Stories", icon="⭐", order=1, concept="star_method",
            mental_model="Structure answers: Situation → Task → Action → Result. Every story needs measurable outcomes.",
            canonical_skill="interview.star_method",
            why_this_matters="Behavioral rounds decide 40% of hires. STAR is the standard format. Without it, answers ramble. With it, interviewers get the signal they need.",
            engineering_context="In performance reviews, engineers use STAR: 'Situation: API slow. Task: reduce latency. Action: added caching. Result: 80% reduction.' Same structure, different context.",
            builds_toward="Interview Performance — behavioral interviews",
            steps=[
                LessonStep(step_type="discover", title="The Structure",
                    content="Situation: context. Task: your responsibility. Action: what YOU did. Result: measurable outcome."),
                LessonStep(step_type="build", title="Craft a STAR Story",
                    function_name="star_story", signature="def star_story() -> dict:",
                    description="Return a STAR story about resolving a technical conflict.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static Map<String, String> solution() { return null; }", "cpp": "std::map<std::string, std::string> solution() { return {}; }", "c": "// star\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static Map<String, String> solution()", "cpp": "std::map<std::string, std::string> solution()", "c": "char* solution()"},
                    test_cases=[{"input":[],"expected":"STAR"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Include All Four Parts",
                            "content": "Your story needs: Situation (context), Task (your role), Action (specific steps YOU took), Result (measurable outcome).",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="STAR Check",
                    content="Without looking — what does the 'A' in STAR stand for?",
                    prompt="A = …",
                    answer="Action",
                ),
            ],
            mastery_evidence=["Structure answers with STAR method"],
            unlocks="beh-2",
        ),
        LessonDefinition(
            id="beh-2", title="Conflict Resolution", icon="🤝", order=2, concept="conflict_resolution",
            mental_model="Conflict is inevitable. Handle it with data, empathy, and compromise. Never blame, always solve.",
            canonical_skill="interview.conflict_resolution",
            why_this_matters="Engineers spend 30% of time in meetings and conflict resolution. Interviewers test whether you can disagree professionally and find common ground.",
            engineering_context="In code reviews, engineers disagree about approaches. The best resolve with data: 'Both approaches work, but X has better performance per benchmark.' That's conflict resolution.",
            builds_toward="Interview Performance — soft skills",
            steps=[
                LessonStep(step_type="predict", title="How to Respond?",
                    question="A teammate insists on a slow algorithm. You know a faster one. What do you do?",
                    options=[
                        {"id":"a","text":"Overrule them because you're senior","correct":False},
                        {"id":"b","text":"Present benchmarks, discuss trade-offs, agree on the best","correct":True},
                        {"id":"c","text":"Let them have their way to avoid conflict","correct":False},
                    ],
                    explanation="Data-driven discussion with empathy. Present evidence, listen to concerns, find the best solution together.",
                ),
            ],
            mastery_evidence=["Handle professional conflict constructively"],
            unlocks="beh-boss",
        ),
        LessonDefinition(
            id="beh-boss", title="Behavioral Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Full behavioral interview: STAR stories for leadership, conflict, failure, and growth.",
            canonical_skill="interview.behavioral", diamonds=100, estimated_minutes=20,
            engineering_context="A real behavioral round: 5-7 questions covering leadership, conflict, failure, influence, and learning. Each answer needs a STAR story with measurable results.",
            builds_toward="Interview Performance — complete behavioral round",
            steps=[
                LessonStep(step_type="mastery", title="Behavioral Round",
                    function_name="behavioral_round", signature="def behavioral_round() -> dict:",
                    description="Return STAR stories for: leadership, conflict resolution, failure, and learning.",
                    test_cases=[{"input":[],"expected":"stories"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover All Questions",
                            "content": "Prepare STAR stories for: a time you led, a conflict you resolved, a failure you learned from, and a time you influenced a decision.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Tell compelling STAR stories", "Handle behavioral questions", "Demonstrate EQ"],
        ),
    ],
)

WORLD_7_HIRING_ARENA = WorldDefinition(
    id="hiring_arena", name="Hiring Arena", icon="🏆",
    subtitle="Interviews + System Design + Behavioral",
    description="The final round. Prove you can code, design, communicate, and lead.",
    order=7, theme="hiring_arena", towns=[CODING_INTERVIEW_TOWN, SYSTEM_DESIGN_TOWN, BEHAVIORAL_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 8 — COMPANY MISSIONS (Expanded)
# ═══════════════════════════════════════════════════════════════════

GOOGLE_TOWN = TownDefinition(
    id="google", name="Google", icon="🔍",
    description="Googlyness + technical depth.",
    order=2, mental_model="Google values: technical excellence, Googlyness (collaboration, doing the right thing), and impact at scale.",
    canonical_skills=["company.google"], competencies=["googlyness", "technical_depth", "scale", "ambiguity"],
    lessons=[
        LessonDefinition(
            id="goog-1", title="Googlyness", icon="🎯", order=1, concept="googlyness",
            mental_model="Googlyness = collaboration + doing the right thing + pushing boundaries. It's how you work, not just what you build.",
            canonical_skill="company.googlyness",
            why_this_matters="Google's unique culture. 'Googlyness' separates Google interviews from pure technical tests. They want engineers who collaborate, question assumptions, and care about impact.",
            engineering_context="In Google's real interviews, they ask: 'Tell me about a time you disagreed with a manager.' They're testing Googlyness — can you push back respectfully? Can you collaborate?",
            builds_toward="Company Interviews — Google culture and values",
            steps=[
                LessonStep(step_type="discover", title="The Values",
                    content="Googlyness: 1) Do the right thing, 2) Collaborate, 3) Push boundaries, 4) Care about users."),
                LessonStep(step_type="retrieve", title="Googlyness Example",
                    question="You see a teammate about to deploy broken code. What do you do?",
                    prompt="I'd…", answer="speak up immediately, explain the risk, and help fix it"),
            ],
            mastery_evidence=["Understand and apply Googlyness"],
            unlocks="goog-2",
        ),
        LessonDefinition(
            id="goog-2", title="Scale Thinking", icon="📈", order=2, concept="scale",
            mental_model="Google problems are at scale: millions of users, petabytes of data. Design for 10x, not 1x.",
            canonical_skill="company.scale",
            why_this_matters="Google systems serve billions. A design that works for 100 users fails at 100M. Scale thinking is how you pass Google system design.",
            engineering_context="In real Google systems: Bigtable handles petabytes, Spanner spans continents, Borg manages millions of containers. Every design decision considers scale.",
            builds_toward="Company Interviews — scale design",
            steps=[
                LessonStep(step_type="predict", title="Scale Estimate",
                    question="1B users, 10 queries/day each. QPS?",
                    options=[
                        {"id":"a","text":"~100K QPS","correct":True},
                        {"id":"b","text":"~1M QPS","correct":False},
                        {"id":"c","text":"~1K QPS","correct":False},
                    ],
                    explanation="1B × 10 / 86400 ≈ 116K QPS. Not 1M or 1K.",
                ),
            ],
            mastery_evidence=["Estimate scale for large systems"],
            unlocks="goog-boss",
        ),
        LessonDefinition(
            id="goog-boss", title="Google Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Full Google interview: technical + Googlyness + scale.",
            canonical_skill="company.google", diamonds=100, estimated_minutes=20,
            engineering_context="A real Google loop: 2 technical, 1 Googlyness/behavioral, 1 system design. Each round 45 minutes. This boss simulates the experience.",
            builds_toward="Company Interviews — complete Google loop",
            steps=[
                LessonStep(step_type="mastery", title="Google Interview",
                    function_name="google_interview", signature="def google_interview() -> dict:",
                    description="Return: technical solution + Googlyness story + scale considerations.",
                    test_cases=[{"input":[],"expected":"interview"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover All Rounds",
                            "content": "Your answer needs: clean technical solution, Googlyness story (collaboration, doing right thing), and scale estimates.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Solve technical problems", "Demonstrate Googlyness", "Think at scale"],
        ),
    ],
)

WORLD_8_COMPANY_MISSIONS = WorldDefinition(
    id="company_missions", name="Company Missions", icon="🎯",
    subtitle="Target-Company Preparation",
    description="Prepare for specific companies: Amazon, Google, Microsoft, and startups.",
    order=8, theme="company_missions", towns=[AMAZON_TOWN, GOOGLE_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 9 — AI ENGINEERING (Expanded)
# ═══════════════════════════════════════════════════════════════════

EVAL_TOWN = TownDefinition(
    id="evaluation", name="Evaluation", icon="📊",
    description="Measure AI quality. No metrics = no improvement.",
    order=2, mental_model="AI evaluation = ground truth + metric (accuracy/F1/BLEU) + test set. Measure to improve.",
    canonical_skills=["ai.evaluation"], competencies=["metrics", "benchmarks", "human_eval", "ab_testing"],
    lessons=[
        LessonDefinition(
            id="eval-1", title="Metrics That Matter", icon="📏", order=1, concept="metrics",
            mental_model="Accuracy isn't enough. Precision, recall, F1, BLEU, ROUGE — each metric tells a different story.",
            canonical_skill="ai.metrics",
            why_this_matters="Choosing the wrong metric leads to optimizing for the wrong thing. Accuracy on imbalanced data is meaningless. F1 balances precision and recall.",
            engineering_context="In production, ML teams track: precision (false positive rate), recall (false negative rate), F1 (balance), and business metrics (revenue impact). A/B tests validate real-world improvement.",
            builds_toward="AI Engineering — model evaluation",
            steps=[
                LessonStep(step_type="discover", title="The Metric Problem",
                    content="95% accuracy on fraud detection where 95% is legitimate = model always predicts 'not fraud'. Useless."),
                LessonStep(step_type="predict", title="Choose the Metric",
                    question="Imbalanced classes (95% negative). Which metric?",
                    options=[
                        {"id":"a","text":"Accuracy","correct":False},
                        {"id":"b","text":"F1 Score","correct":True},
                        {"id":"c","text":"Training loss","correct":False},
                    ],
                    explanation="F1 balances precision and recall. Accuracy is misleading on imbalanced data.",
                ),
            ],
            mastery_evidence=["Choose appropriate evaluation metrics for AI systems"],
            unlocks="eval-2",
        ),
        LessonDefinition(
            id="eval-2", title="Human Evaluation", icon="👥", order=2, concept="human_eval",
            mental_model="Automated metrics don't capture quality. Human evaluation catches: relevance, coherence, safety, bias.",
            canonical_skill="ai.human_eval",
            why_this_matters="LLMs generate text. BLEU scores don't measure helpfulness. Human evaluators rate: is it relevant? Is it coherent? Is it safe? This is how production AI is validated.",
            engineering_context="In production, human eval uses: Likert scales (1-5 rating), pairwise comparison (A vs B), and red-teaming (adversarial testing). Results drive model selection and prompt iteration.",
            builds_toward="AI Engineering — human-in-the-loop evaluation",
            steps=[
                LessonStep(step_type="build", title="Design an Eval Plan",
                    function_name="eval_plan", signature="def eval_plan() -> dict:",
                    description="Return: automated metrics, human eval criteria, sample size, passing threshold.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static Map<String, Object> solution() { return null; }", "cpp": "std::map<std::string, std::string> solution() { return {}; }", "c": "// eval\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static Map<String, Object> solution()", "cpp": "std::map<std::string, std::string> solution()", "c": "char* solution()"},
                    test_cases=[{"input":[],"expected":"plan"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover Both Automated and Human",
                            "content": "Your plan needs: automated metrics (accuracy, F1), human eval (relevance, coherence), sample size (100+), and passing threshold.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design AI evaluation plans", "Combine automated and human metrics"],
            unlocks="eval-boss",
        ),
        LessonDefinition(
            id="eval-boss", title="Eval Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Evaluate an AI system end-to-end: metrics, benchmarks, human eval, and iteration.",
            canonical_skill="ai.evaluation", diamonds=100, estimated_minutes=20,
            engineering_context="A real eval pipeline: run automated metrics on test set, sample 100 outputs for human eval, compare against baseline, decide whether to ship.",
            builds_toward="AI Engineering — complete evaluation pipeline",
            steps=[
                LessonStep(step_type="mastery", title="Full Eval Pipeline",
                    function_name="full_eval", signature="def full_eval() -> dict:",
                    description="Return: test set design, automated metrics, human eval protocol, passing criteria.",
                    test_cases=[{"input":[],"expected":"eval"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Complete Pipeline",
                            "content": "Your pipeline needs: representative test set, automated metrics (accuracy/F1), human eval (relevance/coherence), and clear passing criteria.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design eval pipelines", "Select metrics", "Plan human evaluation"],
        ),
    ],
)

WORLD_9_AI_ENGINEERING = WorldDefinition(
    id="ai_engineering", name="AI Engineering", icon="🤖",
    subtitle="LLMs + RAG + Evaluation",
    description="Build production AI: prompt engineering, RAG, evaluation, and agents.",
    order=9, theme="ai_engineering", towns=[LLM_TOWN, EVAL_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 10 — PRODUCTION (Expanded)
# ═══════════════════════════════════════════════════════════════════

OBS_TOWN = TownDefinition(
    id="observability", name="Observability", icon="🔍",
    description="See inside running systems.",
    order=3, mental_model="Observability = logs + metrics + traces. Three pillars. Without them, debugging production is guessing.",
    canonical_skills=["production.observability"], competencies=["logging", "metrics", "tracing", "distributed_tracing"],
    lessons=[
        LessonDefinition(
            id="obs-1", title="Structured Logging", icon="📋", order=1, concept="logging",
            mental_model="Logs are evidence. Structured (JSON) logs are searchable. Include: timestamp, level, service, trace_id, message.",
            canonical_skill="production.logging",
            why_this_matters="When production breaks, logs are your only evidence. 'Something went wrong' is useless. 'User 123 failed to checkout: payment_timeout at 14:32:01Z' is actionable.",
            engineering_context="In production, structured logging (JSON) enables: filtering by service, aggregating error rates, tracing requests across services, and alerting on patterns.",
            builds_toward="Production Engineering — observability",
            steps=[
                LessonStep(step_type="discover", title="Bad vs Good Logs",
                    content="Bad: 'Error'. Good: {'timestamp':'2024-01-01T10:00:00Z','level':'error','service':'payment','error':'timeout','user_id':123}"),
                LessonStep(step_type="build", title="Structured Logger",
                    function_name="log_event", signature="def log_event(level: str, service: str, message: str) -> dict:",
                    description="Return a structured log dict with timestamp, level, service, message.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "from datetime import datetime\ndef solution(): pass", "java": "public static Map<String, Object> solution() { return null; }", "cpp": "std::map<std::string, std::string> solution() { return {}; }", "c": "// logging\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static Map<String, Object> solution()", "cpp": "std::map<std::string, std::string> solution()", "c": "char* solution()"},
                    test_cases=[{"input":["error","payment","timeout"],"expected":"log"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Include All Fields",
                            "content": "Your log needs: timestamp (ISO format), level (info/warn/error), service name, and message. Use datetime.utcnow().isoformat() for timestamp.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="Why Structured?",
                    content="Without looking — why JSON logs over plain text?",
                    prompt="JSON logs are better because…",
                    answer="they're machine-parseable and searchable",
                ),
            ],
            mastery_evidence=["Write structured logs", "Explain observability pillars"],
            unlocks="obs-2",
        ),
        LessonDefinition(
            id="obs-2", title="Distributed Tracing", icon="🔗", order=2, concept="tracing",
            mental_model="A request touches 10 services. Tracing follows it everywhere. Trace ID = request fingerprint.",
            canonical_skill="production.tracing",
            why_this_matters="In microservices, a single request spans multiple services. Tracing shows the full path: API gateway → auth → orders → payments → DB. Without traces, debugging is impossible.",
            engineering_context="In production, OpenTelemetry traces every request. Jaeger/Zipkin visualizes the trace. You can see: which service was slow, where the error occurred, and the full call graph.",
            builds_toward="Production Engineering — debugging distributed systems",
            steps=[
                LessonStep(step_type="discover", title="The Trace",
                    content="Request ID 123: API Gateway (5ms) → Auth (20ms) → Orders (150ms) → DB (100ms). Trace shows where time went."),
                LessonStep(step_type="predict", title="Find the Bottleneck",
                    question="Trace shows: Gateway=5ms, Auth=20ms, Orders=150ms, DB=100ms. Where's the bottleneck?",
                    options=[
                        {"id":"a","text":"Orders service","correct":True},
                        {"id":"b","text":"Auth service","correct":False},
                        {"id":"c","text":"Gateway","correct":False},
                    ],
                    explanation="Orders took 150ms — the longest. That's the bottleneck to optimize.",
                ),
            ],
            mastery_evidence=["Trace requests across services", "Identify bottlenecks from traces"],
            unlocks="obs-boss",
        ),
        LessonDefinition(
            id="obs-boss", title="Observability Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Design observability for a distributed system.",
            canonical_skill="production.observability", diamonds=100, estimated_minutes=20,
            engineering_context="A real observability setup: structured logging (JSON), metrics (Prometheus), tracing (OpenTelemetry), alerts (PagerDuty). All correlated by trace_id.",
            builds_toward="Production Engineering — complete observability stack",
            steps=[
                LessonStep(step_type="mastery", title="Observability Stack",
                    function_name="obs_stack", signature="def obs_stack() -> dict:",
                    description="Return: logging format, metrics to collect, tracing strategy, alert rules.",
                    test_cases=[{"input":[],"expected":"stack"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover All Pillars",
                            "content": "Your stack needs: structured logs (JSON), metrics (latency/error/throughput), distributed tracing (trace_id), and alerts (error rate, latency SLO).",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design observability stacks", "Set up logging and tracing", "Define alert rules"],
        ),
    ],
)

WORLD_10_PRODUCTION = WorldDefinition(
    id="production", name="Production", icon="🏭",
    subtitle="Reliability + Security + Observability",
    description="Build systems that survive the real world: monitoring, circuit breakers, security, and observability.",
    order=10, theme="production", towns=[RELIABILITY_TOWN, SECURITY_TOWN, OBS_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 11 — PROJECTS (Expanded)
# ═══════════════════════════════════════════════════════════════════

CHAT_TOWN = TownDefinition(
    id="chat_system", name="Chat System", icon="💬",
    description="Build a real-time chat. The classic system design project.",
    order=2, mental_model="Chat = WebSocket connections + message queue + persistent storage + presence system.",
    canonical_skills=["projects.chat"], competencies=["websocket", "message_queue", "presence", "scaling"],
    lessons=[
        LessonDefinition(
            id="chat-1", title="WebSocket Server", icon="🔌", order=1, concept="websocket",
            mental_model="WebSocket = persistent TCP connection. Server pushes to client. No polling. Real-time.",
            canonical_skill="projects.websocket",
            why_this_matters="Chat, gaming, live dashboards — all need real-time. WebSocket is the standard. HTTP polling wastes bandwidth. WebSocket is efficient.",
            engineering_context="In production, Socket.IO or ws library handles WebSocket. Connection pooling, heartbeat/ping-pong, and reconnection logic are standard. Scale with Redis pub/sub across instances.",
            builds_toward="Project Engineering — real-time systems",
            steps=[
                LessonStep(step_type="discover", title="The Connection",
                    content="HTTP: request → response (stateless). WebSocket: connect → bidirectional messages (stateful)."),
                LessonStep(step_type="build", title="Chat Server",
                    function_name="chat_server", signature="def chat_server() -> dict:",
                    description="Return: WebSocket setup, message format, broadcast logic, connection handling.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "import asyncio\nasync def solution(): pass", "java": "public static String solution() { return null; }", "cpp": "std::string solution() { return \"\"; }", "c": "// chat\nchar* solution() { return \"\"; }"},
                    signatures={"python": "async def solution():", "java": "public static String solution()", "cpp": "std::string solution()", "c": "char* solution()"},
                    test_cases=[{"input":[],"expected":"server"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Handle Connections",
                            "content": "Your server needs: accept connections, receive messages, broadcast to all, handle disconnects. Use a list/dict of connected clients.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="WebSocket Benefits",
                    content="Without looking — why WebSocket over HTTP polling?",
                    prompt="WebSocket is better because…",
                    answer="it's bidirectional and persistent, no overhead per message",
                ),
            ],
            mastery_evidence=["Design WebSocket-based chat servers"],
            unlocks="chat-2",
        ),
        LessonDefinition(
            id="chat-2", title="Message Persistence", icon="💾", order=2, concept="persistence",
            mental_model="Chat history = messages stored in DB. New users load history. Real-time = new messages via WebSocket.",
            canonical_skill="projects.persistence",
            why_this_matters="Without persistence, messages disappear on restart. Every chat app stores history: Slack, WhatsApp, Discord — all persist messages.",
            engineering_context="In production, messages go to: Kafka (queue) → PostgreSQL (persist) → Redis (recent cache). WebSocket server reads from Redis for real-time, DB for history.",
            builds_toward="Project Engineering — data persistence in real-time systems",
            steps=[
                LessonStep(step_type="build", title="Persist Messages",
                    function_name="persist_message", signature="def persist_message(room: str, msg: str) -> str:",
                    description="Return SQL: INSERT INTO messages (room, text) VALUES (?, ?).",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static String solution() { return null; }", "cpp": "std::string solution() { return \"\"; }", "c": "char* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static String solution()", "cpp": "std::string solution()", "c": "char* solution()"},
                    test_cases=[{"input":["general","hello"],"expected":"INSERT"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: SQL Syntax",
                            "content": "INSERT INTO messages (room, text) VALUES ('room', 'text'). Use parameterized queries in production.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design message persistence for chat"],
            unlocks="chat-boss",
        ),
        LessonDefinition(
            id="chat-boss", title="Chat Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Complete chat system: WebSocket, persistence, presence, scaling.",
            canonical_skill="projects.chat", diamonds=150, estimated_minutes=30,
            engineering_context="A real chat system: Socket.IO server, Redis pub/sub for scaling across instances, PostgreSQL for history, presence via heartbeat. This boss tests that full architecture.",
            builds_toward="Project Engineering — complete real-time system",
            steps=[
                LessonStep(step_type="mastery", title="Chat Architecture",
                    function_name="chat_architecture", signature="def chat_architecture() -> dict:",
                    description="Return: WebSocket setup, message flow, persistence layer, presence system, scaling strategy.",
                    test_cases=[{"input":[],"expected":"architecture"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Cover All Components",
                            "content": "Your architecture needs: WebSocket server, message queue (Redis/Kafka), database (PostgreSQL), presence tracking, and horizontal scaling plan.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Design real-time chat systems", "Handle WebSocket connections", "Plan for scale"],
        ),
    ],
)

WORLD_11_PROJECTS = WorldDefinition(
    id="projects", name="Projects", icon="🚀",
    subtitle="Build and Ship Real Products",
    description="Go from idea to deployment. Build a URL shortener, chat system, and design your own project.",
    order=11, theme="projects", towns=[URL_SHORTENER_TOWN, CHAT_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 12 — CREATIVE (Expanded)
# ═══════════════════════════════════════════════════════════════════

PORTFOLIO_TOWN = TownDefinition(
    id="portfolio", name="Portfolio", icon="📁",
    description="Your portfolio is your proof.",
    order=2, mental_model="A portfolio isn't a list of projects — it's evidence you can ship, solve problems, and communicate.",
    canonical_skills=["creative.portfolio"], competencies=["project_selection", "documentation", "demo", "storytelling"],
    lessons=[
        LessonDefinition(
            id="port-1", title="Project Selection", icon="🎯", order=1, concept="project_selection",
            mental_model="Good portfolio projects show: complexity, real user value, technical depth, and your unique contribution.",
            canonical_skill="creative.project_selection",
            why_this_matters="Recruiters spend 6 seconds on a resume, 2 minutes on a portfolio. Your projects must instantly signal: 'This engineer can ship real things.'",
            engineering_context="In hiring, candidates with 2-3 deep projects get more interviews than those with 10 tutorial projects. Depth shows you can solve hard problems, not just follow tutorials.",
            builds_toward="Career Development — portfolio that gets interviews",
            steps=[
                LessonStep(step_type="discover", title="What Gets You Hired",
                    content="Best portfolio projects: 1) Solve a real problem, 2) Show technical depth, 3) Have a live demo, 4) Tell a story."),
                LessonStep(step_type="predict", title="Portfolio Review",
                    question="Which project impresses recruiters most?",
                    options=[
                        {"id":"a","text":"10 Todo apps in different languages","correct":False},
                        {"id":"b","text":"1 full-stack app with 1000 users, deployed, with metrics","correct":True},
                        {"id":"c","text":"5 LeetCode solutions","correct":False},
                    ],
                    explanation="Depth over breadth. One project with real users, deployed, with metrics > 10 tutorial projects.",
                ),
            ],
            mastery_evidence=["Select impactful portfolio projects"],
            unlocks="port-2",
        ),
        LessonDefinition(
            id="port-2", title="Tell the Story", icon="📖", order=2, concept="storytelling",
            mental_model="Every project needs a story: problem → solution → your contribution → impact. Data makes it credible.",
            canonical_skill="creative.storytelling",
            why_this_matters="Recruiters don't just want to see what you built — they want to understand why, how, and what impact it had. Storytelling turns code into evidence of skill.",
            engineering_context="In interviews, you have 2 minutes per project. Story: 'I built X because Y. I implemented Z using W. Result: V metric improved by N%.' That's a story, not a feature list.",
            builds_toward="Career Development — communication and storytelling",
            steps=[
                LessonStep(step_type="build", title="Craft Your Story",
                    function_name="project_story", signature="def project_story() -> dict:",
                    description="Return: problem, solution, your role, tech stack, metrics, demo link.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static Map<String, String> solution() { return null; }", "cpp": "std::map<std::string, std::string> solution() { return {}; }", "c": "// story\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static Map<String, String> solution()", "cpp": "std::map<std::string, std::string> solution()", "c": "char* solution()"},
                    test_cases=[{"input":[],"expected":"story"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Include Impact Metrics",
                            "content": "Your story needs: problem (1 sentence), solution (2-3 sentences), your specific contribution, tech stack, and measurable impact (e.g., '50% faster').",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(step_type="retrieve", title="Story Structure",
                    content="Without looking — what are the 5 parts of a good project story?",
                    prompt="Problem, solution, your role, tech stack, and…",
                    answer="measurable impact",
                ),
            ],
            mastery_evidence=["Craft compelling project narratives"],
            unlocks="port-3",
        ),
        LessonDefinition(
            id="port-3", title="Deploy & Demo", icon="🚀", order=3, concept="deployment",
            mental_model="A portfolio project without a live demo is just code. Deploy it: Vercel, Netlify, Railway, Render. Make it clickable.",
            canonical_skill="creative.deployment",
            why_this_matters="Recruiters won't clone and run your code. They want a link they can click. A live demo takes 5 minutes to set up and 10x your chances.",
            engineering_context="In production, engineers deploy to: Vercel (frontend), Railway/Render (backend), Cloud Run (containers). Each takes minutes. A deployed project is worth more than any certification.",
            builds_toward="Career Development — shipping and demonstrating work",
            steps=[
                LessonStep(step_type="discover", title="Deploy Options",
                    content="Frontend: Vercel/Netlify (drag-drop). Backend: Railway/Render (git push). Full-stack: Cloud Run/ECS."),
                LessonStep(step_type="build", title="Deploy Plan",
                    function_name="deploy_plan", signature="def deploy_plan() -> dict:",
                    description="Return: platform, steps, environment variables, custom domain.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static Map<String, String> solution() { return null; }", "cpp": "std::map<std::string, std::string> solution() { return {}; }", "c": "// deploy\nchar* solution() { return \"\"; }"},
                    signatures={"python": "def solution():", "java": "public static Map<String, String> solution()", "cpp": "std::map<std::string, std::string> solution()", "c": "char* solution()"},
                    test_cases=[{"input":[],"expected":"plan"}], hidden_tests=3,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Include All Steps",
                            "content": "Your plan needs: platform choice, deployment steps, environment variables, and custom domain setup.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Create deployment plans", "Set up live demos"],
            unlocks="port-boss",
        ),
        LessonDefinition(
            id="port-boss", title="Portfolio Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Complete portfolio: select projects, craft stories, deploy, and present.",
            canonical_skill="creative.portfolio", diamonds=200, estimated_minutes=30,
            engineering_context="A real portfolio: 2-3 deep projects, each with live demo, clean README, and compelling story. This is what gets you hired.",
            builds_toward="Career Development — complete portfolio",
            steps=[
                LessonStep(step_type="mastery", title="Portfolio Review",
                    function_name="portfolio_review", signature="def portfolio_review() -> dict:",
                    description="Return: 2-3 project stories with problem, solution, your role, metrics, and live demo links.",
                    test_cases=[{"input":[],"expected":"portfolio"}], hidden_tests=5,
                    repair_steps=[
                        {
                            "title": "Quick Repair: Show Depth",
                            "content": "Include 2-3 projects with: problem statement, your specific contribution, tech stack, measurable impact, and live demo links. Quality > quantity.",
                        },
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=["Curate portfolio projects", "Tell compelling stories", "Deploy and demo work"],
        ),
    ],
)

WORLD_12_CREATIVE = WorldDefinition(
    id="creative", name="Creative", icon="🌌",
    subtitle="Independent Creation & Portfolio",
    description="No more tutorials. Define your own problem, design your solution, build your portfolio, and get hired.",
    order=12, theme="creative", towns=[OPEN_ENDED_TOWN, PORTFOLIO_TOWN],
)

# ═══════════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def get_world_3() -> WorldDefinition: return WORLD_3_BUILD_SYSTEMS
def get_world_4() -> WorldDefinition: return WORLD_4_WORK_WITH_DATA
def get_world_5() -> WorldDefinition: return WORLD_5_SOFTWARE_ENGINEERING
def get_world_6() -> WorldDefinition: return WORLD_6_UNDER_PRESSURE
def get_world_7() -> WorldDefinition: return WORLD_7_HIRING_ARENA
def get_world_8() -> WorldDefinition: return WORLD_8_COMPANY_MISSIONS
def get_world_9() -> WorldDefinition: return WORLD_9_AI_ENGINEERING
def get_world_10() -> WorldDefinition: return WORLD_10_PRODUCTION
def get_world_11() -> WorldDefinition: return WORLD_11_PROJECTS
def get_world_12() -> WorldDefinition: return WORLD_12_CREATIVE

def all_lessons_w3() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_3_BUILD_SYSTEMS.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w4() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_4_WORK_WITH_DATA.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w5() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_5_SOFTWARE_ENGINEERING.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w6() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_6_UNDER_PRESSURE.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w7() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_7_HIRING_ARENA.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w8() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_8_COMPANY_MISSIONS.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w9() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_9_AI_ENGINEERING.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w10() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_10_PRODUCTION.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w11() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_11_PROJECTS.towns: lessons.extend(town.lessons)
    return lessons

def all_lessons_w12() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_12_CREATIVE.towns: lessons.extend(town.lessons)
    return lessons
