import json

new_questions = [
    {
        "id": "int-087",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "monitoring",
        "difficulty": "medium",
        "question": "What is observability and how is it different from monitoring? What are the three pillars of observability?",
        "correct_answer": "Monitoring: checks known failure modes with predefined metrics and alerts. Observability: ability to understand system state from external outputs, explore unknown unknowns. Three pillars: 1. Metrics: numeric measurements over time (latency, error rate, CPU). 2. Logs: timestamped event records. 3. Traces: request path across distributed services. Tools: Prometheus/Grafana (metrics), ELK (logs), Jaeger/Zipkin (traces).",
        "options": [],
        "solution": {
            "code": "# Monitoring: 'Is the system up?'\n- Uptime checks\n- CPU/memory alerts\n- Error rate thresholds\n\n# Observability: 'Why is the system slow?'\n- Can query arbitrary dimensions\n- Correlate metrics, logs, traces\n- Debug unknown failure modes",
            "explanation": "Monitoring answers 'is it working?' Observability answers 'why?' The three pillars work together: metric spikes lead to log inspection, which connects to trace analysis. Modern systems need all three."
        },
        "testcases": [
            {
                "input": "Monitoring and observability are the same thing",
                "expected": "Wrong - monitoring is subset of observability"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains difference and three pillars with examples",
                "expected": "Strong - understands production systems"
            }
        ],
        "hints": [
            "Monitoring checks known issues",
            "Observability explores unknowns",
            "Three pillars: metrics, logs, traces"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "devops-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-088",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "diversity",
        "difficulty": "medium",
        "question": "Describe a time you worked on a diverse team with people from different backgrounds. What did you learn?",
        "correct_answer": "STAR method: Situation - international team across 4 countries, 3 time zones. Task - deliver feature on tight deadline. Action - established async communication norms, rotated meeting times fairly, documented decisions, valued different perspectives. Result - shipped on time, team felt included, I learned to check assumptions and communicate explicitly.",
        "options": [],
        "solution": {
            "code": "# Working in diverse teams\n1. Establish explicit communication norms\n2. Rotate inconvenient times fairly\n3. Document decisions for async members\n4. Value different perspectives\n5. Check cultural assumptions",
            "explanation": "Diversity questions test inclusivity and global collaboration. Show you adapt communication, don't assume shared context, and actively include remote/different perspectives."
        },
        "testcases": [
            {
                "input": "I preferred working with people like me",
                "expected": "Weak - shows bias"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows adaptation and inclusion of different perspectives",
                "expected": "Strong - demonstrates inclusivity"
            }
        ],
        "hints": [
            "Show communication adaptation",
            "Mention inclusive practices",
            "Highlight learning from diversity"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "product-manager"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-089",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "data_modeling",
        "difficulty": "hard",
        "question": "Design a data model for a social media platform with users, posts, comments, and likes. How would you handle scale?",
        "correct_answer": "Tables: Users(user_id PK, email, name, created_at). Posts(post_id PK, user_id FK, content, created_at, like_count, comment_count). Comments(comment_id PK, post_id FK, user_id FK, content, created_at). Likes(like_id PK, post_id FK, user_id FK, created_at, UNIQUE(post_id, user_id)). Scale: 1. Denormalize counts in Posts (like_count, comment_count) updated async. 2. Shard by user_id or post_id. 3. Cache hot posts in Redis. 4. Partition Likes by post_id for efficient queries. 5. Use CDN for media.",
        "options": [],
        "solution": {
            "code": "# Core schema\nCREATE TABLE Users (\n  user_id BIGINT PRIMARY KEY,\n  email VARCHAR(255) UNIQUE,\n  name VARCHAR(100),\n  created_at TIMESTAMP\n);\n\nCREATE TABLE Posts (\n  post_id BIGINT PRIMARY KEY,\n  user_id BIGINT,\n  content TEXT,\n  like_count INT DEFAULT 0,\n  comment_count INT DEFAULT 0,\n  created_at TIMESTAMP\n);\n\nCREATE TABLE Likes (\n  like_id BIGINT PRIMARY KEY,\n  post_id BIGINT,\n  user_id BIGINT,\n  UNIQUE KEY uk_post_user (post_id, user_id)\n) PARTITION BY HASH(post_id);",
            "explanation": "Social media data models balance normalization with read performance. Denormalized counts avoid COUNT() on every load. Unique constraints prevent duplicate likes. Partitioning handles scale."
        },
        "testcases": [
            {
                "input": "Count likes by SELECT COUNT(*) FROM Likes WHERE post_id = ? on every page load",
                "expected": "Slow at scale - denormalize count to Posts"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows denormalization, caching, and partitioning strategy",
                "expected": "Strong - understands data modeling at scale"
            }
        ],
        "hints": [
            "Denormalize counts for performance",
            "Use unique constraints to prevent duplicates",
            "Partition by hot dimension"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 35,
        "estimated_time": "25-30 minutes"
    },
    {
        "id": "int-090",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "remote_work",
        "difficulty": "easy",
        "question": "Are you comfortable working in a remote or hybrid environment?",
        "correct_answer": "Show self-awareness and adaptability: 'Yes, I'm comfortable with remote/hybrid work. I've worked remotely before and maintain productivity through structured routines, async communication, and regular check-ins. I use tools like Slack, Notion, and Zoom effectively. I believe in over-communicating status and being proactive about collaboration.' If prefer office: 'I prefer hybrid - office for collaboration, remote for deep work.'",
        "options": [],
        "solution": {
            "code": "# Remote work skills\n1. Self-discipline and time management\n2. Async communication (written clarity)\n3. Proactive status updates\n4. Video presence and participation\n5. Boundary between work and home\n6. Tool fluency (Slack, Notion, Figma)",
            "explanation": "Remote work tests self-motivation and communication. Show you're disciplined, proactive, and tool-fluent. Don't say 'I can work anytime' - show structure. Mention specific tools and practices."
        },
        "testcases": [
            {
                "input": "I need someone watching me to stay productive",
                "expected": "Red flag for remote roles"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows structure, tools, and proactive communication",
                "expected": "Strong - remote-ready"
            }
        ],
        "hints": [
            "Show self-discipline and structure",
            "Mention async communication skills",
            "Be honest about preferences"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 10,
        "estimated_time": "5-10 minutes"
    },
    {
        "id": "int-091",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "code_review",
        "difficulty": "medium",
        "question": "What do you look for when reviewing code? Walk me through your process.",
        "correct_answer": "Review process: 1. Correctness: does it solve the problem, handle edge cases. 2. Design: is it maintainable, follows patterns, single responsibility. 3. Performance: algorithmic complexity, unnecessary work. 4. Security: input validation, auth checks, injection risks. 5. Tests: coverage, meaningful assertions. 6. Style: readability, naming, comments where needed. 7. Documentation: README, API docs. Checklist: 1. Run tests. 2. Check edge cases. 3. Verify error handling.",
        "options": [],
        "solution": {
            "code": "# Code review checklist\n1. FUNCTIONALITY\n   - Does it solve the stated problem?\n   - Are edge cases handled?\n   - Is error handling robust?\n\n2. DESIGN\n   - Single responsibility?\n   - DRY principle\n   - Appropriate patterns?\n\n3. SECURITY\n   - Input validation\n   - SQL injection prevention\n   - Auth/authz checks\n\n4. PERFORMANCE\n   - Algorithmic complexity\n   - Database queries (N+1?)\n   - Memory leaks?",
            "explanation": "Code review is about quality, not style nitpicks. Focus on correctness, design, security, and tests. Good reviews are constructive, explain why, suggest alternatives. Bad reviews are 'LGTM' or bikeshedding."
        },
        "testcases": [
            {
                "input": "I only check for syntax errors and naming",
                "expected": "Weak - misses design, security, tests"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows systematic review covering correctness, design, security",
                "expected": "Strong - understands code review"
            }
        ],
        "hints": [
            "Correctness first",
            "Design and maintainability",
            "Security and edge cases"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-092",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "legacy_systems",
        "difficulty": "hard",
        "question": "How would you approach working with a legacy codebase that has no tests and poor documentation?",
        "correct_answer": "Strategy: 1. Understand: read code, talk to team, identify critical paths. 2. Characterize: add characterization tests (tests that document current behavior without changing it). 3. Safety net: add unit tests for critical functions before changes. 4. Refactor incrementally: small changes, each with tests. 5. Document: add README, inline comments for non-obvious code. 6. Modernize gradually: strangler fig pattern - new code replaces old via interfaces. Never: big bang rewrite, delete 'unused' code without understanding.",
        "options": [],
        "solution": {
            "code": "# Legacy code strategy\n1. Characterization tests first\n   'I don't know what this does, but I'll lock current behavior'\n\n2. Add unit tests before refactoring\n   'If it breaks, I'll know'\n\n3. Strangler fig pattern\n   - Create new interface\n   - Route new code through interface\n   - Gradually replace old implementation\n\n4. Document as you go\n   - README for setup\n   - ADRs for major decisions",
            "explanation": "Legacy code is reality in most jobs. Key: characterization tests before changes, incremental refactoring, never big bang. Strangler fig pattern lets you modernize without rewriting everything."
        },
        "testcases": [
            {
                "input": "I would rewrite the entire system from scratch",
                "expected": "Wrong - big bang rewrites fail 90% of the time"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows incremental approach with characterization tests",
                "expected": "Strong - pragmatic legacy strategy"
            }
        ],
        "hints": [
            "Characterization tests first",
            "Incremental refactoring",
            "Strangler fig pattern"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 30,
        "estimated_time": "25-30 minutes"
    },
    {
        "id": "int-093",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "technical_debt",
        "difficulty": "medium",
        "question": "What is technical debt? How do you decide when to pay it down vs when to take it on?",
        "correct_answer": "Technical debt: suboptimal code or design that ships now but requires future rework, like financial debt with interest. Take on when: 1. Time-to-market critical (startup MVP). 2. Prototyping to validate idea. 3. Temporary workaround for external dependency. Pay down when: 1. Debt slows new development. 2. Bug rate increases. 3. Onboarding new engineers becomes hard. Strategy: allocate 20% time to debt, track in backlog, quantify impact (time lost, bugs), get stakeholder buy-in.",
        "options": [],
        "solution": {
            "code": "# Technical debt framework\nINCREMENT:\n- MVP to validate business hypothesis\n- Temporary workaround for external blocker\n- Prototype to learn\n\nPAY DOWN:\n- Slows all future development\n- Causes recurring bugs\n- Makes onboarding hard\n- Security risks\n\n# Allocation\n- 20% of sprint capacity to debt\n- Track as visible backlog items\n- Quantify: 'This takes 3 days because of debt'",
            "explanation": "Technical debt is strategic, not accidental. Good teams take on debt intentionally and pay it down systematically. Bad teams accumulate debt unconsciously. Communicate debt in business terms, not just 'code quality'."
        },
        "testcases": [
            {
                "input": "I never write bad code, so I have no technical debt",
                "expected": "Wrong - debt is sometimes intentional"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows strategic approach to taking and paying debt",
                "expected": "Strong - understands software economics"
            }
        ],
        "hints": [
            "Debt is strategic, not accidental",
            "Take debt for speed, pay when it slows you",
            "Quantify impact in business terms"
        ],
        "companies": ["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
        "role": ["sde", "backend-engineer", "tech-lead"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-094",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "system_design_search",
        "difficulty": "hard",
        "question": "Design a search autocomplete system like Google Search suggestions. How would you handle 10B searches per day?",
        "correct_answer": "Components: 1. Trie data structure for prefix matching. 2. Pre-computed top queries by prefix from historical data. 3. Cache: Redis/Memcached for hot prefixes. 4. Personalization: user history + trending. 5. Ranking: frequency, recency, personal relevance. 6. API: low-latency endpoint. Scale: 1. Shard trie by prefix. 2. Cache hot prefixes at edge (CDN). 3. Batch update frequencies hourly. 4. Use approximate data structures (Bloom filter) for existence checks. 5. A/B test ranking algorithms.",
        "options": [],
        "solution": {
            "code": "# Autocomplete architecture\nClient -> CDN (hot prefixes) -> API Gateway -> Autocomplete Service\n                                                    -> Redis Cache\n                                                    -> Trie Store (sharded)\n                                                    -> Ranking Service\n                                                    -> Personalization Service\n\n# Trie node\n{\n  'prefix': 'app',\n  'frequency': 50000,\n  'children': {\n    'l': {'prefix': 'appl', 'frequency': 45000, ...},\n    'e': {'prefix': 'appe', 'frequency': 5000, ...}\n  }\n}",
            "explanation": "Autocomplete needs sub-100ms latency at scale. Pre-compute suggestions offline. Cache aggressively. Personalization adds complexity - balance relevance vs privacy. Trie is natural for prefix search but memory-heavy; compress with DAWG or use pre-computed lists."
        },
        "testcases": [
            {
                "input": "Query database on every keystroke",
                "expected": "Too slow - pre-compute and cache"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows trie, caching, and ranking strategy",
                "expected": "Strong - understands search systems"
            }
        ],
        "hints": [
            "Pre-compute suggestions offline",
            "Cache hot prefixes at edge",
            "Trie for prefix matching"
        ],
        "companies": ["google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 40,
        "estimated_time": "30-35 minutes"
    },
    {
        "id": "int-095",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "references",
        "difficulty": "easy",
        "question": "Who are your references?",
        "correct_answer": "Prepare 3-4 references: former manager, senior colleague, client (if applicable). Have their name, title, company, relationship, and contact info ready. Example: 'I can provide references from my manager at X, a senior engineer I worked with closely, and a client from the Y project.' If you're early career: professor or internship supervisor. Always ask permission beforehand and brief them on the role.",
        "options": [],
        "solution": {
            "code": "# Good references\n1. Former direct manager\n2. Senior colleague who saw your work\n3. Client or cross-functional partner\n4. Professor (for new grads)\n\n# Preparation\n- Ask permission beforehand\n- Brief them on the role\n- Provide resume/context\n- Have contact info ready",
            "explanation": "Reference questions test preparation and professional relationships. Have 3-4 ready. Always ask permission first. Brief them on what the new role involves so they can speak to relevant strengths."
        },
        "testcases": [
            {
                "input": "I don't have any references",
                "expected": "Weak - shows limited professional network"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Lists specific references with context",
                "expected": "Strong - prepared and professional"
            }
        ],
        "hints": [
            "Prepare 3-4 references",
            "Ask permission beforehand",
            "Brief them on the role"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 10,
        "estimated_time": "5-10 minutes"
    },
    {
        "id": "int-096",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "vision",
        "difficulty": "medium",
        "question": "Tell me about a time you had to build something from 0 to 1. What was your approach?",
        "correct_answer": "STAR method: Situation - company needed internal tool for data pipeline monitoring. Task - build MVP in 2 months with 1 engineer. Action: 1. Interviewed 10 users to identify must-haves. 2. Chose simple stack (Python + React). 3. Built core dashboard first. 4. Released to 5 pilot users, iterated weekly. Result - adopted by 200+ engineers, saved 10 hours/week per engineer. Lessons: user research first, iterate fast, measure adoption.",
        "options": [],
        "solution": {
            "code": "# 0 to 1 approach\n1. User research: what's the real pain?\n2. Define MVP: smallest useful version\n3. Choose boring technology\n4. Build core workflow first\n5. Release to pilot users\n6. Measure and iterate",
            "explanation": "0 to 1 tests product sense and execution. Show you start with users, not technology. Build MVP fast, measure adoption, iterate. Avoid over-engineering before validation."
        },
        "testcases": [
            {
                "input": "I started by choosing the tech stack",
                "expected": "Wrong - should start with user need"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows user research, MVP, and iteration",
                "expected": "Strong - demonstrates product execution"
            }
        ],
        "hints": [
            "Start with user research",
            "Define MVP scope",
            "Iterate based on feedback"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "product-manager"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-097",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "remote_work",
        "difficulty": "easy",
        "question": "Do you prefer working remotely or in an office?",
        "correct_answer": "Be honest and flexible: 'I'm flexible and productive in both environments. I appreciate office collaboration and spontaneous discussions, but I also thrive with deep focus time at home. For this role, I'm happy to follow the team's hybrid schedule. What matters most is clear communication and shared goals.' If strongly prefer one: be honest but emphasize adaptability.",
        "options": [],
        "solution": {
            "code": "# Balanced answer\nI work well in both environments.\n- Office: collaboration, brainstorming, team bonding\n- Remote: deep focus, flexible schedule, no commute\nI adapt to what the team needs.\n\n# If you prefer remote\nI prefer remote for deep work but value in-person for collaboration.\nI'm happy with hybrid arrangements.",
            "explanation": "Preference questions test culture fit. Show flexibility unless you have strong preference. Emphasize productivity and collaboration over logistics. Companies want team players, not rigid requirements."
        },
        "testcases": [
            {
                "input": "I will only work 100% remote, never office",
                "expected": "May limit opportunities for hybrid roles"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows flexibility and focus on productivity",
                "expected": "Strong - adaptable and team-focused"
            }
        ],
        "hints": [
            "Show flexibility",
            "Emphasize productivity in both",
            "Focus on team needs"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 10,
        "estimated_time": "5-10 minutes"
    },
    {
        "id": "int-098",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "data_warehousing",
        "difficulty": "medium",
        "question": "What is the difference between a data warehouse and a data lake? When would you use each?",
        "correct_answer": "Data Warehouse: structured, processed data, schema-on-write, optimized for SQL analytics, smaller (TB), expensive storage, fast queries. Use for: business intelligence, reporting, dashboards. Data Lake: raw/unprocessed data, schema-on-read, supports all formats, larger (PB), cheap storage, slower queries. Use for: machine learning, data exploration, log analysis. Modern: Delta Lake / Iceberg combine both with ACID and schema enforcement on raw storage.",
        "options": [],
        "solution": {
            "code": "# Data Warehouse\nStructured data -> ETL -> Warehouse -> BI Tools\n- Schema defined before loading\n- Optimized for SQL queries\n- Smaller, curated dataset\n\n# Data Lake\nRaw data -> Lake -> Processing on read\n- Store everything raw\n- Schema defined when querying\n- Large, cheap storage\n\n# Modern: Data Lakehouse\nRaw data + ACID + SQL + ML\n(Databricks, Snowflake, BigQuery)",
            "explanation": "Warehouses are for curated analytics. Lakes are for raw exploration. Lakehouses combine both with ACID guarantees and SQL performance on raw data. Choose based on use case, not hype."
        },
        "testcases": [
            {
                "input": "Data lakes are always better because they're more flexible",
                "expected": "Wrong - slower queries, requires more expertise"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains tradeoffs with appropriate use cases",
                "expected": "Strong - understands data architecture"
            }
        ],
        "hints": [
            "Warehouse: structured, schema-on-write, fast",
            "Lake: raw, schema-on-read, flexible",
            "Lakehouse: best of both"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-099",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "start_date",
        "difficulty": "easy",
        "question": "When can you start?",
        "correct_answer": "Show enthusiasm and professionalism: 'I can start immediately / within 2 weeks / after my notice period of 30 days. I'm excited about the opportunity and can adjust the timeline if needed. I want to ensure smooth transition from current role.' If currently unemployed: 'I'm available immediately and can start as soon as the offer is signed.'",
        "options": [],
        "solution": {
            "code": "# Good answer\n- State clearly when you can start\n- Show enthusiasm\n- Express flexibility if possible\n- Mention transition planning\n\n# Bad answer\n- 'I need 6 months off' (unless agreed)\n- 'I'm not sure' (shows lack of planning)\n- 'Immediately' without notice (unprofessional)",
            "explanation": "Start date questions test availability and professionalism. Be honest. Show enthusiasm. If you have commitments, mention them but show flexibility. Give concrete timeline."
        },
        "testcases": [
            {
                "input": "I can start in 6 months",
                "expected": "Red flag for most roles"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Gives concrete date with enthusiasm",
                "expected": "Strong - available and eager"
            }
        ],
        "hints": [
            "Give specific timeline",
            "Show enthusiasm",
            "Mention transition planning"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 10,
        "estimated_time": "5-10 minutes"
    },
    {
        "id": "int-100",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "reliability",
        "difficulty": "hard",
        "question": "How do you ensure reliability in a distributed system? What patterns and practices would you use?",
        "correct_answer": "Reliability patterns: 1. Retries with exponential backoff + jitter for transient failures. 2. Circuit breaker to stop calling failing services. 3. Timeouts on all external calls. 4. Bulkhead isolation to limit resource usage. 5. Health checks and graceful degradation. 6. Idempotency for safe retries. 7. Dead letter queues for failed messages. 8. Chaos engineering to test failures. Practices: monitoring, alerting, runbooks, blameless postmortems, SLI/SLO/SLA definition.",
        "options": [],
        "solution": {
            "code": "# Reliability patterns\n@retry(max_attempts=3, backoff='exponential')\n@circuit_breaker(failure_threshold=5, recovery_timeout=60)\n@timeout(seconds=3)\n@bulkhead(max_concurrent=10)\ndef call_external_service(data):\n    return requests.post(URL, json=data, timeout=2.5)\n\n# Graceful degradation\nif cache.get('homepage'):\n    return cache.get('homepage')\nelif db.ping():\n    return render_from_db()\nelse:\n    return static_fallback_page()",
            "explanation": "Reliability is about expecting failure. Retries, timeouts, and circuit breakers handle transient failures. Bulkheads prevent cascading failures. Graceful degradation keeps core functionality. Chaos engineering proves resilience."
        },
        "testcases": [
            {
                "input": "Retry infinitely on failure",
                "expected": "Wrong - can overwhelm failing service"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows multiple resilience patterns with appropriate use",
                "expected": "Strong - understands distributed reliability"
            }
        ],
        "hints": [
            "Retries with backoff and jitter",
            "Circuit breaker for failing services",
            "Timeouts on all external calls"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 35,
        "estimated_time": "25-30 minutes"
    }
]

with open('backend/app/data/interview_practice_bank.json', 'r') as f:
    data = json.load(f)
data.extend(new_questions)
with open('backend/app/data/interview_practice_bank.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Added {len(new_questions)} questions. Total: {len(data)}')
