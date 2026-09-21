import json

new_questions = [
    {
        "id": "int-061",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "presentation",
        "difficulty": "medium",
        "question": "Describe a time you had to present a complex technical idea to a non-technical audience. How did you approach it?",
        "correct_answer": "STAR method: Situation - needed executive approval for infrastructure upgrade. Task - explain why $500K investment was needed. Action - created visual comparison (before/after architecture diagrams), used analogy (upgrading from bicycle to car), focused on business impact (downtime cost, scalability), kept slides minimal. Result - approved within a week, project delivered 20% under budget.",
        "options": [],
        "solution": {
            "code": "# Presentation framework for non-technical audience\n1. Start with 'why' - business impact\n2. Use analogies and metaphors\n3. Visual over text (diagrams, charts)\n4. Tell a story with problem -> solution -> outcome\n5. Avoid jargon, or explain it simply\n6. Anticipate questions and prepare answers",
            "explanation": "Communication is as important as technical skill. Show you can translate technical concepts to business value. Use stories, not specs. executives care about ROI, risk, and timeline."
        },
        "testcases": [
            {
                "input": "I showed them the technical architecture diagrams",
                "expected": "Weak - too technical for non-technical audience"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows business framing, analogies, and visual communication",
                "expected": "Strong - demonstrates communication skill"
            }
        ],
        "hints": [
            "Focus on business impact, not technical details",
            "Use analogies and stories",
            "Keep slides minimal and visual"
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
        "id": "int-062",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "work_life_balance",
        "difficulty": "medium",
        "question": "How do you manage work-life balance, especially during crunch times?",
        "correct_answer": "Honest and structured: 'I plan proactively with timeboxing and prioritization. During normal times, I maintain boundaries. During crunch, I focus on what's essential, communicate status early, and ensure I recover after. For example, during launch I worked extended hours but planned recovery time. I believe sustainable pace produces better code than burnout.' Avoid: 'I work 80 hour weeks regularly' or 'I never work extra'.",
        "options": [],
        "solution": {
            "code": "# Sustainable approach\n1. Timebox work and protect personal time\n2. Prioritize ruthlessly during crunch\n3. Communicate blockers early\n4. Take real breaks (Pomodoro, walks)\n5. Recover after crunch periods\n6. Say no to unrealistic deadlines early",
            "explanation": "Work-life balance questions test maturity and sustainability. Show you can work hard when needed but don't glorify burnout. Companies want sustainable performers, not short-term sprinters who burn out."
        },
        "testcases": [
            {
                "input": "I work 80 hour weeks every week",
                "expected": "Red flag - unsustainable, poor boundaries"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows boundaries, planning, and sustainable approach",
                "expected": "Strong - mature and realistic"
            }
        ],
        "hints": [
            "Show you have boundaries",
            "Plan proactively, not reactively",
            "Emphasize sustainability over burnout"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 15,
        "estimated_time": "10-15 minutes"
    },
    {
        "id": "int-063",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "leaving_current_job",
        "difficulty": "easy",
        "question": "Why are you leaving your current job?",
        "correct_answer": "Frame positively: 'I've learned a lot at my current role, but I'm looking for new challenges in [specific area]. I'm particularly excited about your work on [specific product/tech] because it aligns with my interests in [domain]. I want to grow in an environment where I can contribute to larger-scale systems.' Avoid: badmouthing current employer, 'I want more money', 'I don't like my manager'.",
        "options": [],
        "solution": {
            "code": "# Good framing\n- Acknowledge what you learned\n- State what you're seeking next\n- Connect to the new role specifically\n- Show it's about growth, not escape\n\n# Bad framing\n- 'My company is terrible'\n- 'I want more money'\n- 'My manager is awful'",
            "explanation": "This tests why you're job searching and whether you'll badmouth them later. Frame as seeking growth, not escaping problems. Be specific about what excites you at the new company."
        },
        "testcases": [
            {
                "input": "My current company is terrible and my boss is toxic",
                "expected": "Red flag - will badmouth us too"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Frames as growth and connects to new role",
                "expected": "Strong - positive and forward-looking"
            }
        ],
        "hints": [
            "Frame as growth, not escape",
            "Be specific about what excites you",
            "Don't badmouth current employer"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 15,
        "estimated_time": "10-15 minutes"
    },
    {
        "id": "int-064",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "design_patterns",
        "difficulty": "medium",
        "question": "Explain the Singleton design pattern. When would you use it and what are its drawbacks?",
        "correct_answer": "Singleton: ensures a class has only one instance, provides global access point. Use for: database connections, logging, configuration, thread pools. Implementation: private constructor, static instance variable, thread-safe initialization. Drawbacks: 1. Global state makes testing hard. 2. Violates Single Responsibility. 3. Hidden dependencies. 4. Difficult to subclass. 5. Can become bottleneck in multi-threaded context.",
        "options": [],
        "solution": {
            "code": "# Python Singleton\nclass DatabaseConnection:\n    _instance = None\n    \n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n            cls._instance.connection = create_connection()\n        return cls._instance\n\n# Usage\n db1 = DatabaseConnection()\ndb2 = DatabaseConnection()\nassert db1 is db2  # Same instance",
            "explanation": "Singletons are controversial. They're useful for resource management but create hidden dependencies. Dependency injection is often better. In multi-threaded apps, need thread-safe initialization."
        },
        "testcases": [
            {
                "input": "Singleton is always the best pattern for shared resources",
                "expected": "Wrong - has significant drawbacks"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains use cases and tradeoffs",
                "expected": "Strong - understands design patterns critically"
            }
        ],
        "hints": [
            "One instance, global access",
            "Use for shared resources",
            "Consider testability and hidden dependencies"
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
        "id": "int-065",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "database_indexing",
        "difficulty": "hard",
        "question": "What is a database index? Explain different types of indexes and when you would use each.",
        "correct_answer": "Index: data structure (usually B-tree) that speeds up queries at cost of slower writes. Types: 1. B-tree: default, good for range queries and equality. 2. Hash: O(1) equality lookups, not for ranges. 3. Composite: multi-column index, order matters. 4. Full-text: for text search. 5. Bitmap: for low-cardinality columns (gender, status). Use when: frequent WHERE/JOIN/ORDER BY on column. Avoid when: table is small, column has low selectivity, write-heavy workload.",
        "options": [],
        "solution": {
            "code": "# B-tree index (default)\nCREATE INDEX idx_users_email ON Users(email);\n-- Good for: WHERE email = ?, ORDER BY email\n\n# Composite index\nCREATE INDEX idx_orders_user_date ON Orders(user_id, order_date);\n-- Good for: WHERE user_id = ? AND order_date > ?\n-- Order matters! (user_id, date) != (date, user_id)\n\n# Full-text index\nCREATE FULLTEXT INDEX idx_products_desc ON Products(description);\n-- Good for: MATCH(description) AGAINST('query')",
            "explanation": "Indexes trade write speed for read speed. B-tree is default and versatile. Composite indexes follow leftmost prefix rule. Too many indexes slow down INSERT/UPDATE/DELETE. Monitor with EXPLAIN."
        },
        "testcases": [
            {
                "input": "Indexes always improve performance",
                "expected": "Wrong - slow down writes, not always needed"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains types with appropriate use cases",
                "expected": "Strong - understands indexing deeply"
            }
        ],
        "hints": [
            "B-tree is default, good for ranges",
            "Composite index order matters",
            "Indexes slow down writes"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 30,
        "estimated_time": "25-30 minutes"
    },
    {
        "id": "int-066",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "conflict_management",
        "difficulty": "medium",
        "question": "Describe a time you had a disagreement with your manager. How did you handle it?",
        "correct_answer": "STAR method: Situation - manager wanted to cut testing to meet deadline. Task - ensure quality without missing deadline. Action - scheduled 1:1, showed data on bug rates from skipping tests, proposed compromise: automate critical tests first, defer low-priority tests. Result - agreed on 80% automation, shipped on time, zero production bugs. Manager later adopted testing-first approach.",
        "options": [],
        "solution": {
            "code": "# Disagreeing with manager\n1. Request private conversation\n2. Present data, not opinions\n3. Understand their constraints\n4. Propose alternatives, not just objections\n5. Be willing to disagree and commit\n6. Preserve relationship",
            "explanation": "Disagreeing with manager tests courage and communication. Show you can advocate for what's right with data, not just argue. Preserve relationship. Be ready to 'disagree and commit' if decision goes other way."
        },
        "testcases": [
            {
                "input": "I just did what my manager said",
                "expected": "Weak - no independent thinking"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows data-driven advocacy and relationship preservation",
                "expected": "Strong - demonstrates professional courage"
            }
        ],
        "hints": [
            "Use data, not opinions",
            "Propose alternatives",
            "Preserve the relationship"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-067",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "rest_api_design",
        "difficulty": "medium",
        "question": "What are RESTful API design best practices? How would you handle versioning, authentication, and error responses?",
        "correct_answer": "Best practices: 1. Use nouns not verbs: /users not /getUsers. 2. Proper HTTP methods: GET (read), POST (create), PUT (update), DELETE (delete). 3. Versioning: /v1/ or Accept header. 4. Authentication: JWT in Authorization header or OAuth2. 5. Error responses: consistent format with status code, message, code, details. 6. Pagination: cursor or offset. 7. Filtering: query params. 8. Rate limiting: X-RateLimit-* headers.",
        "options": [],
        "solution": {
            "code": "# Good API design\nGET    /v1/users          # List users\nPOST   /v1/users          # Create user\nGET    /v1/users/:id      # Get user\nPUT    /v1/users/:id      # Update user\nDELETE /v1/users/:id      # Delete user\n\n# Error response format\n{\n  'error': {\n    'code': 'VALIDATION_ERROR',\n    'message': 'Email is required',\n    'details': [{'field': 'email', 'issue': 'required'}]\n  }\n}\n\n# Headers\nAuthorization: Bearer <jwt>\nX-RateLimit-Limit: 100\nX-RateLimit-Remaining: 45",
            "explanation": "Good API design is about consistency and developer experience. REST uses HTTP semantics. Versioning prevents breaking changes. Standard error formats reduce client confusion. Authentication should be stateless (JWT) for scalability."
        },
        "testcases": [
            {
                "input": "Design uses verbs like /getUsers, /createUser",
                "expected": "Non-RESTful - should use nouns and HTTP methods"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows REST conventions, versioning, and error format",
                "expected": "Strong - understands API design"
            }
        ],
        "hints": [
            "Use nouns, not verbs",
            "Use HTTP methods correctly",
            "Version APIs to prevent breaking changes"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-068",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "microservices_patterns",
        "difficulty": "hard",
        "question": "What are common microservices communication patterns? When would you use synchronous vs asynchronous communication?",
        "correct_answer": "Patterns: 1. Request/Response (REST, gRPC): synchronous, direct. Use for: queries, commands needing immediate response. 2. Event-driven (message queue): asynchronous, decoupled. Use for: notifications, analytics, eventual consistency. 3. Pub/Sub: one-to-many async. Use for: notifications, logging, cache invalidation. 4. Saga pattern: distributed transactions via choreography or orchestration. Use for: multi-service transactions. Synchronous when: immediate response needed, simple flow. Asynchronous when: resilience needed, fan-out, or eventual consistency acceptable.",
        "options": [],
        "solution": {
            "code": "# Synchronous: direct call\n@app.route('/order', methods=['POST'])\ndef create_order():\n    user = requests.get(f'http://user-service/users/{user_id}')\n    payment = requests.post(f'http://payment-service/charge', json=...)\n    return jsonify(order)\n\n# Asynchronous: event-driven\n@app.route('/order', methods=['POST'])\ndef create_order():\n    order = create_order_in_db()\n    event_bus.publish('order.created', order)\n    return jsonify(order), 202\n\n# Consumer\ndef on_order_created(event):\n    send_email(event['user_id'])\n    update_inventory(event['items'])",
            "explanation": "Synchronous is simple but creates coupling and cascading failures. Asynchronous is resilient but complex (ordering, idempotency, dead letter queues). Use synchronous for user-facing requests, async for background work."
        },
        "testcases": [
            {
                "input": "Always use synchronous communication for simplicity",
                "expected": "Wrong - creates tight coupling and failure cascades"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains patterns with appropriate use cases",
                "expected": "Strong - understands microservices communication"
            }
        ],
        "hints": [
            "Synchronous: immediate response needed",
            "Asynchronous: decoupling and resilience",
            "Consider failure modes and latency"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 35,
        "estimated_time": "25-30 minutes"
    },
    {
        "id": "int-069",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "message_queues",
        "difficulty": "medium",
        "question": "What is the difference between Kafka and RabbitMQ? When would you use each?",
        "correct_answer": "Kafka: distributed streaming platform, log-based, high throughput, persistent, replayable. Use for: event sourcing, activity streams, log aggregation, real-time analytics. RabbitMQ: traditional message broker, smart routing, multiple protocols (AMQP), lower throughput but rich features. Use for: task queues, complex routing, microservices communication where ordering matters per queue. Key difference: Kafka is for high-volume event streams, RabbitMQ is for reliable task distribution.",
        "options": [],
        "solution": {
            "code": "# Kafka: high-throughput stream\nproducer.send(ProducerRecord('user-events', user_id, event))\n# Multiple consumers read same stream at own pace\n\n# RabbitMQ: task queue\nchannel.basic_publish(\n    exchange='',\n    routing_key='email-tasks',\n    body=json.dumps(task)\n)\n# One consumer gets each message",
            "explanation": "Kafka stores streams durably and allows multiple consumers. RabbitMQ routes messages intelligently but typically one consumer per message. Kafka for 'fire and forget' streams, RabbitMQ for 'process once' tasks."
        },
        "testcases": [
            {
                "input": "Kafka and RabbitMQ are interchangeable",
                "expected": "Wrong - different architectures and use cases"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains architecture differences and use cases",
                "expected": "Strong - understands messaging systems"
            }
        ],
        "hints": [
            "Kafka: streaming, high throughput, replay",
            "RabbitMQ: routing, protocols, task queues",
            "Consider throughput vs features"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-070",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "expectations",
        "difficulty": "easy",
        "question": "What do you expect from your manager?",
        "correct_answer": "Show maturity: 'I expect clear direction and priorities, regular constructive feedback, trust and autonomy, support for growth, and psychological safety. I want a manager who removes blockers, advocates for the team, and celebrates wins. I believe in bidirectional feedback - I'll communicate openly and expect the same.'",
        "options": [],
        "solution": {
            "code": "# Good expectations\n1. Clear direction and priorities\n2. Regular feedback (not just annual review)\n3. Trust and autonomy\n4. Support for growth and learning\n5. Psychological safety\n6. Transparency about team health",
            "explanation": "This tests whether you understand good management and whether you'll be easy to manage. Show you're self-directed but value guidance. Avoid: 'I expect to be told exactly what to do' or 'I expect minimal oversight'."
        },
        "testcases": [
            {
                "input": "I expect to be micromanaged and told exactly what to do",
                "expected": "Weak - shows lack of initiative"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows maturity, clear expectations, and two-way relationship",
                "expected": "Strong - understands good manager relationship"
            }
        ],
        "hints": [
            "Show you want growth and feedback",
            "Mention psychological safety",
            "Show you're self-directed"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 15,
        "estimated_time": "10-15 minutes"
    },
    {
        "id": "int-071",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "api_gateway",
        "difficulty": "medium",
        "question": "What is an API gateway? What problems does it solve?",
        "correct_answer": "API gateway: single entry point for all client requests, routes to appropriate microservices. Solves: 1. Routing: directs requests to correct service. 2. Authentication/Authorization: centralizes security. 3. Rate limiting: protects services. 4. Request/response transformation: format conversion, protocol translation. 5. Caching: reduces backend load. 6. Monitoring: centralized logging and metrics. 7. Circuit breaking: prevents cascading failures. Examples: Kong, AWS API Gateway, NGINX Plus.",
        "options": [],
        "solution": {
            "code": "# API Gateway flow\nClient -> API Gateway\n              -> Route to Service A (users)\n              -> Route to Service B (orders)\n              -> Route to Service C (payments)\n\n# Gateway responsibilities\n- Auth: validate JWT\n- Rate limit: 100 req/min per user\n- Transform: JSON to gRPC\n- Cache: cache /products/123\n- Log: record request/response",
            "explanation": "API gateway is the front door to microservices. It centralizes cross-cutting concerns so services don't repeat code. Tradeoff: adds latency and single point of failure (mitigate with clustering)."
        },
        "testcases": [
            {
                "input": "API gateway is just a load balancer",
                "expected": "Partial - gateway does more than load balancing"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Lists multiple gateway responsibilities beyond routing",
                "expected": "Strong - understands API gateway role"
            }
        ],
        "hints": [
            "Single entry point for clients",
            "Centralizes cross-cutting concerns",
            "Routes to backend services"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-072",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "team_culture",
        "difficulty": "easy",
        "question": "What kind of team culture do you thrive in?",
        "correct_answer": "Specific and researched: 'I thrive in teams with psychological safety where people are comfortable admitting mistakes. I like collaborative environments with code review culture, knowledge sharing, and clear ownership. I appreciate teams that ship incrementally and learn from failures. From what I've seen about your culture, the emphasis on [specific value] really resonates with me.'",
        "options": [],
        "solution": {
            "code": "# Good answer\n1. Specific cultural traits (psychological safety, learning)\n2. How you contribute to that culture\n3. Connect to company's stated values\n4. Show you've researched them",
            "explanation": "Culture fit is critical for retention and performance. Show you know what environments you do well in. Be specific, not generic ('nice people'). Research the company's values and connect."
        },
        "testcases": [
            {
                "input": "I just want to work with nice people",
                "expected": "Too vague - no specifics"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows specific values and research about company",
                "expected": "Strong - culture-aware and prepared"
            }
        ],
        "hints": [
            "Be specific about cultural traits",
            "Connect to company's stated values",
            "Show you contribute to that culture"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 15,
        "estimated_time": "10-15 minutes"
    }
]

with open('backend/app/data/interview_practice_bank.json', 'r') as f:
    data = json.load(f)
data.extend(new_questions)
with open('backend/app/data/interview_practice_bank.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Added {len(new_questions)} questions. Total: {len(data)}')
