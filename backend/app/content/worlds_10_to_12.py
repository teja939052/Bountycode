"""Worlds 10-12: Production, Projects, Creative."""
from __future__ import annotations

from app.content.lesson_definitions import (
    LessonDefinition, LessonStep, TownDefinition, WorldDefinition,
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 10 — PRODUCTION
# ═══════════════════════════════════════════════════════════════════

RELIABILITY_TOWN = TownDefinition(
    id="reliability", name="Reliability", icon="🛡️",
    description="Systems that don't break. The difference between junior and senior.",
    order=1, mental_model="Reliability = redundancy + monitoring + graceful degradation. Plan for failure.",
    canonical_skills=["production.reliability"], competencies=["monitoring", "alerting", "circuit_breaker", "retries", "graceful_degradation"],
    lessons=[
        LessonDefinition(
            id="rel-1", title="Monitor Everything", icon="📊", order=1, concept="monitoring",
            mental_model="You can't fix what you can't see. Monitor: latency, error rate, throughput, saturation — the four golden signals.",
            canonical_skill="production.monitoring",
            why_this_matters="Production systems fail. The question is: do you know before your users tell you? Monitoring is how senior engineers sleep at night. Without it, you're flying blind.",
            engineering_context="In production, engineers set up dashboards for the four golden signals: latency (p50/p99), error rate (5xx/min), throughput (QPS), and saturation (CPU/memory). Alerts fire when thresholds breach.",
            builds_toward="Production Engineering — observability and reliability",
            steps=[
                LessonStep(step_type="discover", title="The Four Golden Signals",
                    content="Latency: how long? Error rate: how many failures? Throughput: how much traffic? Saturation: how full?"),
                LessonStep(step_type="retrieve", title="What to Alert On",
                    question="What's the most important thing to alert on?",
                    prompt="Alert on…", answer="error rate and latency SLO breaches"),
            ],
            mastery_evidence=["Identify the four golden signals for monitoring"],
            unlocks="rel-2",
        ),
        LessonDefinition(
            id="rel-2", title="Circuit Breaker", icon="⚡", order=2, concept="circuit_breaker",
            mental_model="When a dependency fails, stop calling it. Fail fast, recover gracefully. Don't cascade failures.",
            canonical_skill="production.circuit_breaker",
            why_this_matters="Without circuit breakers, one slow dependency cascades to bring down your entire system. In 2021, a major cloud outage cascaded because one service kept retrying a failing dependency. Circuit breakers prevent that.",
            engineering_context="In microservices, circuit breakers are standard: after N failures, stop calling the service for T seconds. Return a fallback or cached response. Libraries like Hystrix (Java) or resilience4j implement this pattern.",
            builds_toward="Production Engineering — preventing cascading failures",
            steps=[
                LessonStep(step_type="discover", title="The Pattern",
                    content="Closed (normal) → Open (failing, stop calling) → Half-Open (test if recovered)."),
            ],
            mastery_evidence=["Explain the circuit breaker pattern and its states"],
            unlocks="rel-boss",
        ),
        LessonDefinition(
            id="rel-boss", title="Reliability Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Design a reliable system: monitoring, circuit breakers, graceful degradation.",
            canonical_skill="production.reliability", xp=100, estimated_minutes=20,
            engineering_context="In a real reliability review, you'd design: monitoring dashboards, alert thresholds, circuit breaker configs, retry policies, and fallback strategies. This boss tests that combination.",
            builds_toward="Production Engineering — complete reliability design",
            steps=[
                LessonStep(step_type="mastery", title="Design for Failure",
                    function_name="design_reliable", signature="def design_reliable() -> dict:",
                    description="Return: monitoring signals, alert thresholds, circuit breaker config, and fallback strategy.",
                    test_cases=[{"input":[],"expected":"design"}], hidden_tests=3),
            ],
            mastery_evidence=["Set up monitoring", "Implement circuit breakers", "Design graceful degradation"],
        ),
    ],
)

SECURITY_TOWN = TownDefinition(
    id="security", name="Security", icon="🔒",
    description="Build systems that don't get hacked. Security is everyone's job.",
    order=2, mental_model="Security = validate input + least privilege + encrypt data + never trust the client.",
    canonical_skills=["production.security"], competencies=["input_validation", "authentication", "encryption", "owasp", "least_privilege"],
    lessons=[
        LessonDefinition(
            id="sec-1", title="Validate Input", icon="🛡️", order=1, concept="input_validation",
            mental_model="Never trust user input. Validate type, length, format, and range. Most attacks exploit unvalidated input.",
            canonical_skill="production.input_validation",
            why_this_matters="The #1 security vulnerability is unvalidated input. SQL injection, XSS, command injection — all come from trusting user input. Input validation is the cheapest security win.",
            engineering_context="In production, every API endpoint validates input: type checking, length limits, format regex, range checks. Libraries like Pydantic (Python) or Joi (Node) automate this. Security reviews check input validation first.",
            builds_toward="Production Engineering — secure system design",
            steps=[
                LessonStep(step_type="build", title="Validate an Email",
                    function_name="validate_email", signature="def validate_email(email: str) -> bool:",
                    description="Return True if email is valid: contains @, has domain, no spaces.",
                    test_cases=[{"input":["test@example.com"],"expected":True}], hidden_tests=4),
            ],
            mastery_evidence=["Validate user input for security"],
            unlocks="sec-2",
        ),
        LessonDefinition(
            id="sec-2", title="Least Privilege", icon="🔑", order=2, concept="least_privilege",
            mental_model="Give every component the minimum access it needs. A web server doesn't need database admin rights.",
            canonical_skill="production.least_privilege",
            why_this_matters="When every service has admin access, one breach compromises everything. Least privilege limits blast radius. It's the principle behind IAM roles, database permissions, and container security.",
            engineering_context="In cloud engineering, IAM roles follow least privilege: a Lambda function gets read-only access to one S3 bucket, not full S3 access. In Kubernetes, pods run as non-root users with minimal capabilities.",
            builds_toward="Production Engineering — access control and IAM",
            steps=[
                LessonStep(step_type="predict", title="Right Permission?",
                    question="A service reads from one S3 bucket. What permission should it have?",
                    options=[{"id":"a","text":"Full S3 admin","correct":False},{"id":"b","text":"Read-only on that bucket","correct":True},{"id":"c","text":"No permissions","correct":False}]),
            ],
            mastery_evidence=["Apply least privilege principle to access control"],
            unlocks="sec-boss",
        ),
        LessonDefinition(
            id="sec-boss", title="Security Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Secure an API: validate input, enforce least privilege, encrypt data.",
            canonical_skill="production.security", xp=100, estimated_minutes=20,
            engineering_context="In a real security review, you'd check: input validation on all endpoints, authentication/authorization, encryption at rest and in transit, and least-privilege access. This boss tests that complete review.",
            builds_toward="Production Engineering — complete security review",
            steps=[
                LessonStep(step_type="mastery", title="Secure an API Endpoint",
                    function_name="secure_endpoint", signature="def secure_endpoint() -> dict:",
                    description="Return security measures: input validation, auth check, rate limiting, encryption.",
                    test_cases=[{"input":[],"expected":"security"}], hidden_tests=3),
            ],
            mastery_evidence=["Validate input", "Enforce least privilege", "Design secure APIs"],
        ),
    ],
)

WORLD_10_PRODUCTION = WorldDefinition(
    id="production", name="Production", icon="🏭",
    subtitle="Reliability + Scale + Security",
    description="Build systems that survive the real world: monitoring, circuit breakers, security.",
    order=10, theme="production", towns=[RELIABILITY_TOWN, SECURITY_TOWN],
)


# ═══════════════════════════════════════════════════════════════════
# WORLD 11 — PROJECTS
# ═══════════════════════════════════════════════════════════════════

URL_SHORTENER_TOWN = TownDefinition(
    id="url_shortener", name="URL Shortener", icon="🔗",
    description="Build a complete system from scratch. The classic first project.",
    order=1, mental_model="A complete project: API → database → caching → deployment. Every piece connects.",
    canonical_skills=["projects.system_build"], competencies=["api_design", "database", "caching", "deployment", "testing"],
    lessons=[
        LessonDefinition(
            id="url-1", title="Design the API", icon="📋", order=1, concept="api_design",
            mental_model="Start with the contract: POST /shorten → {short_url}, GET /{code} → redirect.",
            canonical_skill="projects.api_design",
            why_this_matters="Every real project starts with API design. Before writing code, you define: what endpoints exist, what they accept, what they return. Good API design makes the rest of the project easy.",
            engineering_context="In a real sprint, you'd write an API spec (OpenAPI/Swagger) before coding. The spec is reviewed by frontend, backend, and QA. It's the contract everyone builds against.",
            builds_toward="Project Engineering — building complete systems",
            steps=[
                LessonStep(step_type="build", title="Define Endpoints",
                    function_name="define_endpoints", signature="def define_endpoints() -> dict:",
                    description="Return: POST /shorten {url} → {short_code}, GET /{code} → redirect 301.",
                    test_cases=[{"input":[],"expected":"endpoints"}], hidden_tests=3),
            ],
            mastery_evidence=["Design API endpoints for a complete system"],
            unlocks="url-2",
        ),
        LessonDefinition(
            id="url-2", title="Add a Database", icon="🗄️", order=2, concept="database",
            mental_model="Persist the mapping: short_code → original_url. Database makes it survive restarts.",
            canonical_skill="projects.database",
            why_this_matters="Without a database, your data dies when the server restarts. Every production system needs persistence. Choosing the right database and schema is a core engineering skill.",
            engineering_context="In production, you'd use PostgreSQL or DynamoDB to store the URL mapping. The schema: short_code (PK), original_url, created_at, click_count. Index on short_code for fast lookups.",
            builds_toward="Project Engineering — data persistence",
            steps=[
                LessonStep(step_type="build", title="Design the Schema",
                    function_name="design_schema", signature="def design_schema() -> dict:",
                    description="Return: table 'urls' with columns: short_code (PK), original_url, created_at, clicks.",
                    test_cases=[{"input":[],"expected":"schema"}], hidden_tests=3),
            ],
            mastery_evidence=["Design database schemas for projects"],
            unlocks="url-3",
        ),
        LessonDefinition(
            id="url-3", title="Add Caching", icon="⚡", order=3, concept="caching",
            mental_model="Cache hot URLs in memory. Database for truth, cache for speed. The most common performance pattern.",
            canonical_skill="projects.caching",
            why_this_matters="Caching is the #1 performance optimization. Google's shortener serves billions of redirects — it can't hit the database for each one. Cache hot data, serve from memory, fall back to DB.",
            engineering_context="In production, Redis caches hot URL mappings. Cache hit: serve in <1ms. Cache miss: query DB, populate cache, serve. TTL expires stale entries. This pattern powers most high-traffic systems.",
            builds_toward="Project Engineering — performance optimization",
            steps=[
                LessonStep(step_type="retrieve", title="Cache Strategy",
                    question="A URL is accessed 1000x/second. How do you serve it fast?",
                    prompt="I'd cache…", answer="the URL mapping in Redis with a TTL"),
            ],
            mastery_evidence=["Apply caching to improve performance"],
            unlocks="url-boss",
        ),
        LessonDefinition(
            id="url-boss", title="Deploy It", icon="🚀", kind="boss", order=4,
            concept="transfer", mental_model="Complete project: API + database + cache + tests + deploy.",
            canonical_skill="projects.system_build", xp=150, estimated_minutes=30,
            why_this_matters="Building it locally isn't enough. Real engineers ship. Deployment — even to a free tier — proves you can take a project from idea to production.",
            engineering_context="In a real project, you'd deploy to AWS/GCP: containerize with Docker, deploy to ECS/Cloud Run, set up a database, configure a custom domain, and add monitoring. That's the full lifecycle.",
            builds_toward="Project Engineering — shipping complete products",
            steps=[
                LessonStep(step_type="mastery", title="Deployment Plan",
                    function_name="deployment_plan", signature="def deployment_plan() -> dict:",
                    description="Return: containerization, hosting, database setup, domain config, monitoring.",
                    test_cases=[{"input":[],"expected":"plan"}], hidden_tests=3),
            ],
            mastery_evidence=["Design APIs", "Add databases", "Apply caching", "Deploy complete systems"],
        ),
    ],
)

WORLD_11_PROJECTS = WorldDefinition(
    id="projects", name="Projects", icon="🚀",
    subtitle="Build and Ship Real Products",
    description="Go from idea to deployment. Build a URL shortener, then design your own project.",
    order=11, theme="projects", towns=[URL_SHORTENER_TOWN],
)


# ═══════════════════════════════════════════════════════════════════
# WORLD 12 — CREATIVE
# ═══════════════════════════════════════════════════════════════════

OPEN_ENDED_TOWN = TownDefinition(
    id="open_ended", name="Open World", icon="🌌",
    description="No more tutorials. Design and build something that's yours.",
    order=1, mental_model="Real engineering is open-ended: no spec, no solution, no answer key. You define the problem and solve it.",
    canonical_skills=["creative.independent"], competencies=["problem_definition", "system_design", "self_direction", "portfolio", "documentation"],
    lessons=[
        LessonDefinition(
            id="creative-1", title="Define Your Problem", icon="🎯", order=1, concept="problem_definition",
            mental_model="Before solving, define: what problem? who has it? what does success look like? Engineers who can define problems are more valuable than those who just solve them.",
            canonical_skill="creative.problem_definition",
            why_this_matters="In real engineering, problems aren't handed to you. A PM says 'users are churning' — you have to define WHY and what to build. Problem definition is the skill that gets you promoted to senior.",
            engineering_context="In real teams, engineers write RFCs (Request for Comments) or design docs: problem statement, proposed solution, trade-offs, success metrics. This document drives the project.",
            builds_toward="Senior Engineering — problem definition and ownership",
            steps=[
                LessonStep(step_type="build", title="Write a Problem Statement",
                    function_name="problem_statement", signature="def problem_statement() -> dict:",
                    description="Return: problem, who_has_it, success_metrics, constraints.",
                    test_cases=[{"input":[],"expected":"statement"}], hidden_tests=3),
            ],
            mastery_evidence=["Define problems clearly before solving them"],
            unlocks="creative-2",
        ),
        LessonDefinition(
            id="creative-2", title="Design Your Solution", icon="🏗️", order=2, concept="system_design",
            mental_model="Given a problem, design: components, data flow, APIs, trade-offs. There's no single right answer.",
            canonical_skill="creative.system_design",
            why_this_matters="Open-ended design is what senior engineers do daily. No tutorial, no answer key. You propose a solution, defend its trade-offs, and iterate. This is the skill that separates coders from engineers.",
            engineering_context="In real architecture, you'd propose: 'We'll use a message queue for async processing, PostgreSQL for persistence, and Redis for caching.' Then defend: 'Why not MongoDB? Why not Kafka?' Trade-offs are the job.",
            builds_toward="Senior Engineering — architectural decision making",
            steps=[
                LessonStep(step_type="build", title="Propose an Architecture",
                    function_name="propose_architecture", signature="def propose_architecture() -> dict:",
                    description="Return: components, data flow, technology choices, and trade-offs.",
                    test_cases=[{"input":[],"expected":"architecture"}], hidden_tests=3),
            ],
            mastery_evidence=["Design system architectures with trade-offs"],
            unlocks="creative-3",
        ),
        LessonDefinition(
            id="creative-3", title="Document It", icon="📝", order=3, concept="documentation",
            mental_model="If it's not documented, it doesn't exist. Good docs = good engineering. Write for your future teammate.",
            canonical_skill="creative.documentation",
            why_this_matters="In real engineering, documentation is how knowledge spreads. A well-documented project gets contributors. An undocumented one gets abandoned. Documentation is a force multiplier.",
            engineering_context="In real teams, engineers write: READMEs (how to run), API docs (how to use), ADRs (why we chose X), and runbooks (what to do when it breaks). Documentation is part of the job, not an afterthought.",
            builds_toward="Senior Engineering — technical writing and knowledge sharing",
            steps=[
                LessonStep(step_type="build", title="Write a README",
                    function_name="write_readme", signature="def write_readme() -> dict:",
                    description="Return: title, description, setup instructions, API docs, trade-offs.",
                    test_cases=[{"input":[],"expected":"readme"}], hidden_tests=3),
            ],
            mastery_evidence=["Write clear technical documentation"],
            unlocks="creative-boss",
        ),
        LessonDefinition(
            id="creative-boss", title="Ship Your Portfolio", icon="🏆", kind="boss", order=4,
            concept="transfer", mental_model="Define, design, build, document, deploy. The complete engineering cycle.",
            canonical_skill="creative.independent", xp=200, estimated_minutes=45,
            why_this_matters="Your portfolio is what gets you hired. Not certificates — projects. A complete project with docs, tests, and deployment proves you can ship. That's what interviewers want to see.",
            engineering_context="In real job searches, candidates with deployed projects get 3x more interviews. A GitHub repo with a live demo, clean README, and documented trade-offs is worth more than any certification.",
            builds_toward="Job Readiness — portfolio that gets you hired",
            steps=[
                LessonStep(step_type="mastery", title="Complete Project",
                    function_name="complete_project", signature="def complete_project() -> dict:",
                    description="Return: problem statement, architecture, implementation plan, docs, deployment.",
                    test_cases=[{"input":[],"expected":"project"}], hidden_tests=3),
            ],
            mastery_evidence=["Define problems", "Design solutions", "Document work", "Ship complete projects"],
        ),
    ],
)

WORLD_12_CREATIVE = WorldDefinition(
    id="creative", name="Creative", icon="🌌",
    subtitle="Independent Creation",
    description="No more tutorials. Define your own problem, design your solution, build your portfolio.",
    order=12, theme="creative", towns=[OPEN_ENDED_TOWN],
)

def get_world_10() -> WorldDefinition: return WORLD_10_PRODUCTION
def get_world_11() -> WorldDefinition: return WORLD_11_PROJECTS
def get_world_12() -> WorldDefinition: return WORLD_12_CREATIVE

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
