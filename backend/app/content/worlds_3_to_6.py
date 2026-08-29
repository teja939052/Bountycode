"""Worlds 3-6: Build Systems, Data, Software Engineering, Under Pressure."""
from __future__ import annotations

from app.content.lesson_definitions import (
    LessonDefinition, LessonStep, TownDefinition, WorldDefinition,
)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# WORLD 3 â€” BUILD SYSTEMS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

API_TOWN = TownDefinition(
    id="apis", name="APIs", icon="ðŸ”Œ", description="How systems talk to each other.",
    order=1, mental_model="An API is a contract: request in, response out.",
    canonical_skills=["backend.apis"], competencies=["rest", "http", "endpoints", "status_codes"],
    lessons=[
        LessonDefinition(
            id="apis-1", title="REST Basics", icon="ðŸŒ", order=1, concept="rest",
            mental_model="REST maps CRUD to HTTP verbs: GET(read), POST(create), PUT(update), DELETE(delete).",
            canonical_skill="backend.rest",
            why_this_matters="REST APIs are how 90% of web services communicate. Every app you use â€” from Twitter to banking â€” runs on REST. Understanding REST is understanding how the modern web works.",
            engineering_context="In backend engineering, you design REST endpoints for every feature. GET /users/123 fetches a user. POST /orders creates an order. The URL structure IS your API design.",
            builds_toward="Backend Engineering â€” API design and implementation",
            steps=[
                LessonStep(step_type="discover", title="HTTP Verbs",
                    content="GET /users â†’ list users. POST /users â†’ create. PUT /users/1 â†’ update. DELETE /users/1 â†’ remove."),
                LessonStep(step_type="build", title="Design Endpoints",
                    function_name="design_endpoints", signature="def design_endpoints(resource: str) -> dict:",
                    description="Return {GET, POST, PUT, DELETE} URLs for a resource. E.g. 'users' â†’ {GET:'/users',...}.",
                    test_cases=[{"input":["users"],"expected":{"/users": "GET list", "/users": "POST create", "/users/:id": "GET one", "/users/:id": "PUT update", "/users/:id": "DELETE"}}], hidden_tests=3),
            ],
            mastery_evidence=["Map CRUD operations to HTTP verbs"],
            unlocks="apis-2",
        ),
        LessonDefinition(
            id="apis-2", title="Status Codes", icon="ðŸ“¡", order=2, concept="status_codes",
            mental_model="Status codes tell the client what happened: 200 OK, 201 Created, 404 Not Found, 500 Error.",
            canonical_skill="backend.status_codes",
            why_this_matters="Status codes are how APIs communicate success or failure. A 201 vs 200 tells the client whether something was created. A 429 tells it to slow down. Without proper codes, clients can't respond correctly.",
            engineering_context="In production APIs, status codes drive client behavior. Mobile apps retry on 503, show errors on 400, redirect on 301. Monitoring systems alert on 5xx rates. They're essential for observability.",
            builds_toward="Backend Engineering â€” API reliability and client communication",
            steps=[
                LessonStep(step_type="predict", title="What Code?",
                    question="A user was successfully created. What status code?",
                    options=[{"id":"a","text":"200 OK","correct":False},{"id":"b","text":"201 Created","correct":True},{"id":"c","text":"204 No Content","correct":False}]),
            ],
            mastery_evidence=["Choose correct HTTP status codes"],
            unlocks="apis-boss",
        ),
        LessonDefinition(
            id="apis-boss", title="APIs Boss", icon="ðŸ‰", kind="boss", order=3,
            concept="transfer", mental_model="Design a complete REST API for a real resource.",
            canonical_skill="backend.apis", xp=100, estimated_minutes=15,
            engineering_context="In a real sprint, you'd design endpoints for a new feature: 'users can bookmark articles.' You need GET/POST/DELETE endpoints, proper status codes, and error handling.",
            builds_toward="Backend Engineering â€” feature API design",
            steps=[
                LessonStep(step_type="mastery", title="Bookmark API",
                    function_name="bookmark_endpoints", signature="def bookmark_endpoints() -> dict:",
                    description="Return all REST endpoints for a bookmark feature: list, create, delete bookmarks.",
                    test_cases=[{"input":[],"expected":"endpoints"}], hidden_tests=3),
            ],
            mastery_evidence=["Design REST endpoints", "Use status codes", "Handle CRUD operations"],
        ),
    ],
)

DB_TOWN = TownDefinition(
    id="databases", name="Databases", icon="ðŸ—„ï¸", description="Where data lives forever.",
    order=2, mental_model="Databases store data structured for fast queries.",
    canonical_skills=["backend.databases"], competencies=["sql", "schema", "joins", "indexing"],
    lessons=[
        LessonDefinition(
            id="db-1", title="SQL Queries", icon="ðŸ”", order=1, concept="sql",
            mental_model="SQL declares WHAT you want, not HOW to get it. The database figures out the how.",
            canonical_skill="backend.sql",
            why_this_matters="SQL is the language of data. Every application queries databases. Data analysts, backend engineers, and ML engineers all use SQL daily. It's one of the most in-demand skills in tech.",
            engineering_context="In backend engineering, you write queries to fetch user data, generate reports, and power features. Poor queries cause slow APIs. Good queries with proper indexes make systems fast.",
            builds_toward="Backend Engineering â€” data access and query optimization",
            steps=[
                LessonStep(step_type="build", title="Write a Query",
                    function_name="write_query", signature="def write_query() -> str:",
                    description="Return SQL: SELECT name, email FROM users WHERE active=1 ORDER BY created_at DESC.",
                    test_cases=[{"input":[],"expected":"SELECT"}], hidden_tests=3),
            ],
            mastery_evidence=["Write basic SQL queries"],
            unlocks="db-2",
        ),
        LessonDefinition(
            id="db-2", title="Joins", icon="ðŸ”—", order=2, concept="joins",
            mental_model="Joins combine tables by matching keys â€” inner join for matches only, left join for all from one side.",
            canonical_skill="backend.joins",
            why_this_matters="Real data is spread across tables. Users have orders, orders have items. Joins combine them. Understanding joins is understanding how relational data works â€” and how to query it efficiently.",
            engineering_context="In e-commerce, showing 'your order history' requires joining users â†’ orders â†’ items. Poor join choices cause slow queries that time out. Indexing join columns is a core optimization skill.",
            builds_toward="Backend Engineering â€” relational data modeling and querying",
            steps=[
                LessonStep(step_type="predict", title="Inner vs Left",
                    question="You want ALL users, even those without orders. Which join?",
                    options=[{"id":"a","text":"INNER JOIN","correct":False},{"id":"b","text":"LEFT JOIN","correct":True},{"id":"c","text":"RIGHT JOIN","correct":False}],
                ),
            ],
            mastery_evidence=["Choose the right join type"],
            unlocks="db-boss",
        ),
        LessonDefinition(
            id="db-boss", title="Databases Boss", icon="ðŸ‰", kind="boss", order=3,
            concept="transfer", mental_model="Design a schema and query it.",
            canonical_skill="backend.databases", xp=100, estimated_minutes=15,
            engineering_context="In a real system design, you'd design tables for a feature (e.g., 'comments on posts'), write the queries to fetch them, and add indexes for performance. This boss tests that combination.",
            builds_toward="Backend Engineering â€” schema design and querying",
            steps=[
                LessonStep(step_type="mastery", title="Design a Schema",
                    function_name="design_schema", signature="def design_schema() -> dict:",
                    description="Return table definitions for: users(id,name), posts(id,user_id,title), comments(id,post_id,user_id,text).",
                    test_cases=[{"input":[],"expected":"schema"}], hidden_tests=3),
            ],
            mastery_evidence=["Write SQL queries", "Choose join types", "Design database schemas"],
        ),
    ],
)

WORLD_3_BUILD_SYSTEMS = WorldDefinition(
    id="build_systems", name="Build Systems", icon="ðŸ—",
    subtitle="APIs + Backend + Databases",
    description="Learn how real systems are built: APIs, databases, and the backend logic connecting them.",
    order=3, theme="build_systems", towns=[API_TOWN, DB_TOWN],
)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# WORLD 4 â€” WORK WITH DATA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

DATA_TOWN = TownDefinition(
    id="data", name="Data", icon="ðŸ“Š", description="Turn raw data into decisions.",
    order=1, mental_model="Data becomes useful when you aggregate, filter, and visualize it.",
    canonical_skills=["data.sql", "data.analytics"], competencies=["aggregation", "grouping", "window_functions", "etl"],
    lessons=[
        LessonDefinition(
            id="data-1", title="Aggregation", icon="ðŸ“ˆ", order=1, concept="aggregation",
            mental_model="Aggregation collapses many rows into one: COUNT, SUM, AVG, MAX, MIN.",
            canonical_skill="data.aggregation",
            why_this_matters="Business decisions run on aggregations. Daily active users, revenue per cohort, average order value â€” all aggregations. Data engineers and analysts build these queries daily.",
            engineering_context="In analytics dashboards, every metric is an aggregation. In monitoring, every alert threshold is an aggregation over time. In ML, feature engineering is aggregation.",
            builds_toward="Data Engineering â€” analytics and reporting",
            steps=[
                LessonStep(step_type="build", title="Count and Sum",
                    function_name="aggregate", signature="def aggregate() -> str:",
                    description="Return SQL: SELECT category, COUNT(*), SUM(price) FROM products GROUP BY category.",
                    test_cases=[{"input":[],"expected":"SELECT"}], hidden_tests=3),
            ],
            mastery_evidence=["Write aggregation queries"],
            unlocks="data-2",
        ),
        LessonDefinition(
            id="data-2", title="Window Functions", icon="ðŸªŸ", order=2, concept="window_functions",
            mental_model="Window functions compute across related rows without collapsing â€” running totals, rankings, moving averages.",
            canonical_skill="data.window_functions",
            why_this_matters="Window functions solve problems that are painful with GROUP BY: running totals, top-N per group, month-over-month growth. They're the difference between junior and senior SQL.",
            engineering_context="In finance, window functions compute running balances. In analytics, they rank products by sales. In ML feature engineering, they create lag features for time series.",
            builds_toward="Data Engineering â€” advanced analytics",
            steps=[
                LessonStep(step_type="build", title="Rank Products",
                    function_name="rank_products", signature="def rank_products() -> str:",
                    description="Return SQL: SELECT name, RANK() OVER (ORDER BY sales DESC) FROM products.",
                    test_cases=[{"input":[],"expected":"RANK"}], hidden_tests=3),
            ],
            mastery_evidence=["Use window functions for advanced analytics"],
            unlocks="data-boss",
        ),
        LessonDefinition(
            id="data-boss", title="Data Boss", icon="ðŸ‰", kind="boss", order=3,
            concept="transfer", mental_model="Combine aggregations and window functions for real analytics.",
            canonical_skill="data.analytics", xp=100, estimated_minutes=15,
            engineering_context="In a real analytics task, you'd combine everything: aggregate sales by category, rank within each, compute month-over-month growth. That's the combination this boss tests.",
            builds_toward="Data Engineering â€” complex analytics pipelines",
            steps=[
                LessonStep(step_type="mastery", title="Sales Report",
                    function_name="sales_report", signature="def sales_report() -> str:",
                    description="Return SQL: monthly sales with running total and MoM growth using window functions.",
                    test_cases=[{"input":[],"expected":"WITH"}], hidden_tests=3),
            ],
            mastery_evidence=["Write aggregations", "Use window functions", "Combine for complex reports"],
        ),
    ],
)

WORLD_4_WORK_WITH_DATA = WorldDefinition(
    id="work_with_data", name="Work With Data", icon="ðŸ“Š",
    subtitle="SQL + Schemas + Analytics",
    description="Turn raw data into decisions with SQL, aggregation, and analytics.",
    order=4, theme="work_with_data", towns=[DATA_TOWN],
)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# WORLD 5 â€” SOFTWARE ENGINEERING
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

GIT_TOWN = TownDefinition(
    id="git", name="Git & Collaboration", icon="ðŸ”€", description="Code is teamwork.",
    order=1, mental_model="Git tracks every change â€” branch, commit, merge, collaborate.",
    canonical_skills=["engineering.git"], competencies=["branching", "commits", "merging", "pull_requests"],
    lessons=[
        LessonDefinition(
            id="git-1", title="Branching", icon="ðŸŒ¿", order=1, concept="branching",
            mental_model="Branches let you work on features without breaking main. Branch â†’ code â†’ commit â†’ merge.",
            canonical_skill="engineering.branching",
            why_this_matters="Git is the universal collaboration tool. Every engineering team uses it. Without Git, you can't collaborate on code, review changes, or deploy safely. It's non-negotiable.",
            engineering_context="In real teams, you branch for every feature, open a pull request, get code reviewed, run CI tests, then merge. Git branching strategy (GitFlow, trunk-based) is a team decision.",
            builds_toward="Software Engineering â€” collaborative development",
            steps=[
                LessonStep(step_type="discover", title="The Branch Workflow",
                    content="main â†’ feature branch â†’ commits â†’ pull request â†’ review â†’ merge."),
                LessonStep(step_type="retrieve", title="Git Commands",
                    question="What command creates and switches to a new branch?",
                    prompt="git ??? -b feature-name", answer="checkout"),
            ],
            mastery_evidence=["Understand Git branching workflow"],
            unlocks="git-boss",
        ),
        LessonDefinition(
            id="git-boss", title="Git Boss", icon="ðŸ‰", kind="boss", order=2,
            concept="transfer", mental_model="Navigate a full Git collaboration workflow.",
            canonical_skill="engineering.git", xp=100, estimated_minutes=15,
            engineering_context="In a real sprint, you'd branch, commit, push, open a PR, address review comments, and merge. This boss tests whether you understand the full cycle.",
            builds_toward="Software Engineering â€” team collaboration",
            steps=[
                LessonStep(step_type="mastery", title="Resolve a Merge Conflict",
                    function_name="resolve_conflict", signature="def resolve_conflict() -> str:",
                    description="Return the steps to resolve a merge conflict: identify, edit, add, commit.",
                    test_cases=[{"input":[],"expected":"steps"}], hidden_tests=3),
            ],
            mastery_evidence=["Branch and merge", "Handle pull requests", "Resolve conflicts"],
        ),
    ],
)

TESTING_TOWN = TownDefinition(
    id="testing", name="Testing", icon="ðŸ§ª", description="Prove your code works.",
    order=2, mental_model="Tests are executable specifications â€” they prove your code does what you claim.",
    canonical_skills=["engineering.testing"], competencies=["unit_tests", "edge_cases", "tdd", "integration"],
    lessons=[
        LessonDefinition(
            id="testing-1", title="Unit Tests", icon="âœ…", order=1, concept="unit_tests",
            mental_model="A unit test checks one function with one input â†’ one expected output. Small, fast, isolated.",
            canonical_skill="engineering.unit_tests",
            why_this_matters="Tests prevent regressions. Without them, every change is a gamble. Companies with good test coverage deploy confidently. Companies without tests fear Fridays.",
            engineering_context="In production, tests run on every commit (CI). If tests fail, the merge is blocked. A typical codebase has more test code than production code. Testing is engineering.",
            builds_toward="Software Engineering â€” quality assurance and CI/CD",
            steps=[
                LessonStep(step_type="build", title="Write a Test",
                    function_name="test_add", signature="def test_add():",
                    description="Write a test: assert add(2,3) == 5 and add(-1,1) == 0 and add(0,0) == 0.",
                    starter="def test_add():\n    # write three assertions\n",
                    test_cases=[{"input":[],"expected":"assertions"}], hidden_tests=3),
            ],
            mastery_evidence=["Write unit tests with assertions"],
            unlocks="testing-2",
        ),
        LessonDefinition(
            id="testing-2", title="Edge Cases", icon="ðŸ”", order=2, concept="edge_cases",
            mental_model="Bugs hide at boundaries: empty input, single element, negative numbers, maximum values. Test those.",
            canonical_skill="engineering.edge_cases",
            why_this_matters="Most production bugs are edge cases: empty lists, null values, integer overflow, off-by-one errors. Testing edge cases is what separates careful engineers from careless ones.",
            engineering_context="In code reviews, reviewers specifically look for untested edge cases. 'What if the list is empty?' 'What if the user is null?' These questions prevent production incidents.",
            builds_toward="Software Engineering â€” defensive programming and code review",
            steps=[
                LessonStep(step_type="predict", title="What Could Break?",
                    question="A function finds the max of a list. What input would break it?",
                    options=[{"id":"a","text":"A list with one element","correct":False},{"id":"b","text":"An empty list","correct":True},{"id":"c","text":"A list of positive numbers","correct":False}],
                ),
            ],
            mastery_evidence=["Identify and test edge cases"],
            unlocks="testing-boss",
        ),
        LessonDefinition(
            id="testing-boss", title="Testing Boss", icon="ðŸ‰", kind="boss", order=3,
            concept="transfer", mental_model="Write tests that cover normal cases AND edge cases.",
            canonical_skill="engineering.testing", xp=100, estimated_minutes=15,
            engineering_context="In a real PR, you'd write tests for your function covering: normal input, empty input, single element, negative numbers, and large input. That coverage is what reviewers expect.",
            builds_toward="Software Engineering â€” test coverage and quality",
            steps=[
                LessonStep(step_type="mastery", title="Test a Reverse Function",
                    function_name="test_reverse", signature="def test_reverse():",
                    description="Write 4 tests for reverse(): normal list, empty list, single element, two elements.",
                    starter="def test_reverse():\n    # 4 test cases\n",
                    test_cases=[{"input":[],"expected":"4 tests"}], hidden_tests=3),
            ],
            mastery_evidence=["Write unit tests", "Test edge cases", "Cover normal and boundary cases"],
        ),
    ],
)

WORLD_5_SOFTWARE_ENGINEERING = WorldDefinition(
    id="software_engineering", name="Software Engineering", icon="ðŸ› ",
    subtitle="Git + Testing + Quality",
    description="Professional engineering practices: version control, testing, code review.",
    order=5, theme="software_engineering", towns=[GIT_TOWN, TESTING_TOWN],
)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# WORLD 6 â€” UNDER PRESSURE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

OA_TOWN = TownDefinition(
    id="oa", name="Online Assessments", icon="â±ï¸", description="Solve under constraints.",
    order=1, mental_model="OA problems test pattern recognition under time pressure â€” know the patterns, save time.",
    canonical_skills=["interview.oa"], competencies=["timed_coding", "pattern_recognition", "optimization", "debugging_under_pressure"],
    lessons=[
        LessonDefinition(
            id="oa-1", title="Pattern Recognition", icon="ðŸ”", order=1, concept="pattern_recognition",
            mental_model="Most OA problems are standard patterns in disguise. Recognize the pattern, apply the template.",
            canonical_skill="interview.pattern_recognition",
            why_this_matters="In a 60-minute OA, you don't have time to invent solutions. You need to recognize: this is BFS, this is two pointers, this is a hash map. Pattern recognition is the skill that gets you hired.",
            engineering_context="In interviews, candidates who recognize patterns solve problems in 20 minutes. Those who don't, run out of time. Companies know this â€” that's why they test standard patterns.",
            builds_toward="Interview Performance â€” speed and accuracy",
            steps=[
                LessonStep(step_type="predict", title="What Pattern?",
                    question="'Find if an array has duplicates.' What's the fastest approach?",
                    options=[{"id":"a","text":"Nested loops O(nÂ²)","correct":False},{"id":"b","text":"Hash set O(n)","correct":True},{"id":"c","text":"Sort then scan O(n log n)","correct":False}],
                ),
            ],
            mastery_evidence=["Recognize common problem patterns"],
            unlocks="oa-2",
        ),
        LessonDefinition(
            id="oa-2", title="Optimization", icon="âš¡", order=2, concept="optimization",
            mental_model="First make it work, then make it fast. Optimize by identifying the bottleneck and choosing the right data structure.",
            canonical_skill="interview.optimization",
            why_this_matters="In OA, a correct O(nÂ²) solution might pass sample tests but fail hidden tests with large input. You need to optimize to O(n) or O(n log n). That's the difference between passing and failing.",
            engineering_context="In production, an O(nÂ²) algorithm that works for 100 users will crash with 1,000,000 users. Optimization isn't academic â€” it's the difference between a system that scales and one that doesn't.",
            builds_toward="Interview Performance â€” writing efficient solutions",
            steps=[
                LessonStep(step_type="build", title="Optimize the Solution",
                    function_name="two_sum_optimized", signature="def two_sum_optimized(nums: list, target: int) -> list:",
                    description="Solve Two Sum in O(n) using a hash map. Return indices.",
                    test_cases=[{"input":[[2,7,11,15],9],"expected":[0,1]}], hidden_tests=5),
            ],
            mastery_evidence=["Optimize from O(nÂ²) to O(n)"],
            unlocks="oa-boss",
        ),
        LessonDefinition(
            id="oa-boss", title="OA Boss", icon="ðŸ‰", kind="boss", order=3,
            concept="transfer", mental_model="Solve a timed problem: recognize pattern, implement correctly, optimize.",
            canonical_skill="interview.oa", xp=100, estimated_minutes=20,
            engineering_context="A real OA gives you 2-3 problems in 60-90 minutes. You have to read, recognize the pattern, implement without bugs, and optimize. This boss simulates that pressure.",
            builds_toward="Interview Performance â€” performing under time pressure",
            steps=[
                LessonStep(step_type="mastery", title="Valid Anagram",
                    function_name="is_anagram", signature="def is_anagram(s: str, t: str) -> bool:",
                    description="Return True if t is an anagram of s. O(n) time, O(1) space (26 letters).",
                    test_cases=[{"input":["anagram","nagaram"],"expected":True}], hidden_tests=5),
            ],
            mastery_evidence=["Recognize patterns quickly", "Implement correctly", "Optimize solutions"],
        ),
    ],
)

WORLD_6_UNDER_PRESSURE = WorldDefinition(
    id="under_pressure", name="Under Pressure", icon="âš¡",
    subtitle="OA + Timed Problems + Debugging",
    description="Perform under time pressure: online assessments, debugging, optimization.",
    order=6, theme="under_pressure", towns=[OA_TOWN],
)

def get_world_3() -> WorldDefinition: return WORLD_3_BUILD_SYSTEMS
def get_world_4() -> WorldDefinition: return WORLD_4_WORK_WITH_DATA
def get_world_5() -> WorldDefinition: return WORLD_5_SOFTWARE_ENGINEERING
def get_world_6() -> WorldDefinition: return WORLD_6_UNDER_PRESSURE

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
