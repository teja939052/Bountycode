import json

new_questions = [
    {
        "id": "int-025",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "amazon_lp_customer_obsession",
        "difficulty": "medium",
        "question": "Amazon Leadership Principle: Customer Obsession. Tell me about a time you went above and beyond for a customer or user.",
        "correct_answer": "STAR method: Situation - users were frustrated with slow search. Task - as eng lead, improve UX. Action - interviewed 20 users, found pagination was main pain point, built instant search with debouncing. Result - search time dropped 70%, NPS increased 25 points, feature became company standard.",
        "options": [],
        "solution": {
            "code": "# Customer obsession example\n1. Start with customer pain, not your solution\n2. Use data: support tickets, user interviews, analytics\n3. Measure impact on customer outcomes\n4. Show you championed the customer when others didnt",
            "explanation": "Amazon LP questions need concrete customer-impact stories. Show you prioritized customer over convenience, used data to understand pain, and measured outcome."
        },
        "testcases": [
            {
                "input": "I built a feature because my manager asked",
                "expected": "Weak - not customer-obsessed, just compliant"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows deep customer research and measurable improvement",
                "expected": "Strong - demonstrates customer obsession"
            }
        ],
        "hints": [
            "Start with customer pain, not your solution",
            "Quantify the customer impact",
            "Show you advocated for the customer"
        ],
        "companies": ["amazon"],
        "role": ["sde", "backend-engineer", "product-manager"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-026",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "amazon_lp_bias_for_action",
        "difficulty": "medium",
        "question": "Amazon Leadership Principle: Bias for Action. Tell me about a time you made a decision with 70 percent information instead of waiting for 100.",
        "correct_answer": "STAR method: Situation - production issue, root cause unclear. Task - restore service fast. Action - chose rollback (reversible) over deep investigation, restored in 10 mins, investigated cause during off-peak. Result - minimal user impact, root cause found and fixed, postmortem shared company-wide.",
        "options": [],
        "solution": {
            "code": "# Bias for Action\n1. Speed matters in many decisions\n2. Reversible decisions: make them fast with 70% info\n3. Irreversible decisions: gather more data\n4. Always have a rollback plan\n5. Distinguish disagree-and-commit from wait-and-see",
            "explanation": "Amazon values speed. Show you can calculate risk, choose reversible options when possible, and still be accountable for outcomes."
        },
        "testcases": [
            {
                "input": "I always gather 100% data before deciding",
                "expected": "Wrong - too slow for many business decisions"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows calculated risk with reversible action and fast outcome",
                "expected": "Strong - demonstrates bias for action"
            }
        ],
        "hints": [
            "Distinguish reversible vs irreversible decisions",
            "Show speed without recklessness",
            "Always include rollback plan"
        ],
        "companies": ["amazon"],
        "role": ["sde", "backend-engineer", "product-manager"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-027",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "amazon_lp_deliver_results",
        "difficulty": "medium",
        "question": "Amazon Leadership Principle: Deliver Results. Tell me about a time you were behind schedule. How did you catch up?",
        "correct_answer": "STAR method: Situation - 3 weeks behind on migration. Task - deliver without breaking prod. Action - cut scope to MVP, re-prioritized by risk, worked with PM to reset expectations, automated testing. Result - delivered core in 1 week, full migration next sprint, zero downtime.",
        "options": [],
        "solution": {
            "code": "# Deliver Results\n1. Acknowledge reality early\n2. Cut scope, not quality\n3. Re-negotiate deadlines with new data\n4. Remove blockers aggressively\n5. Communicate status transparently",
            "explanation": "Deliver results is about accountability under pressure. Show you don't just work harder - you re-scope, re-prioritize, and communicate."
        },
        "testcases": [
            {
                "input": "I just worked late nights and weekends",
                "expected": "Partial - shows effort but not problem-solving"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows scope negotiation, prioritization, and transparent communication",
                "expected": "Strong - delivers results through strategy"
            }
        ],
        "hints": [
            "Show you re-scoped, not just worked harder",
            "Mention communication with stakeholders",
            "Quantify the outcome"
        ],
        "companies": ["amazon"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-028",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "googleyness",
        "difficulty": "medium",
        "question": "Tell me about a time you failed and what you learned. How did that change how you approach problems?",
        "correct_answer": "STAR method: Situation - chose complex solution for simple problem. Task - deliver feature in 1 week. Action - built over-engineered system, missed deadline. Learned: start simple, measure before optimizing, get early feedback. Now: I prototype first, validate assumptions, then scale. Result - delivered last 3 features 2x faster.",
        "options": [],
        "solution": {
            "code": "# Growth from failure\n1. Be specific about failure\n2. Show genuine learning\n3. Connect learning to changed behavior\n4. Prove with subsequent results",
            "explanation": "Googleyness values learning agility and humility. Show you can fail, reflect, and change. Don't blame others or give trivial examples."
        },
        "testcases": [
            {
                "input": "I can't think of a real failure",
                "expected": "Red flag - no self-awareness"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows specific failure, learning, and changed behavior",
                "expected": "Strong - growth mindset"
            }
        ],
        "hints": [
            "Pick a real technical failure",
            "Show how you changed after",
            "Connect to better outcomes later"
        ],
        "companies": ["google"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-029",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "system_design_chat",
        "difficulty": "hard",
        "question": "Design a chat application like WhatsApp. How would you handle 1B messages per day with end-to-end encryption?",
        "correct_answer": "Components: 1. API gateway + load balancer. 2. Auth service (JWT + phone verification). 3. Message service: Kafka for ingestion, Redis for online user sessions, Cassandra for message history. 4. E2E encryption: Signal Protocol (Double Ratchet). 5. Push notifications: FCM/APNS. 6. Media: S3 + CDN. 7. Presence: WebSocket connections with heartbeat. Scale: partition by user_id, replicate across regions.",
        "options": [],
        "solution": {
            "code": "# High-level architecture\nClient -> API Gateway -> Auth Service\n                         -> Message Service\n                              -> Kafka (async fan-out)\n                              -> WebSocket Service (online users)\n                              -> Notification Service (offline)\n                         -> Media Service -> S3 + CDN\n\nE2E: Signal Protocol (Double Ratchet)\nStorage: Cassandra partitioned by conversation_id\nCache: Redis for sessions and online status",
            "explanation": "Chat systems need real-time delivery, message ordering, and end-to-end encryption. Key tradeoffs: consistency vs latency, online vs offline delivery, media handling. Signal Protocol is the gold standard for E2E."
        },
        "testcases": [
            {
                "input": "Design uses HTTP polling for messages",
                "expected": "Inefficient - WebSocket or push is needed for real-time"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Design includes message ordering, E2E encryption, offline storage",
                "expected": "Strong - addresses key chat system challenges"
            }
        ],
        "hints": [
            "Use WebSocket for real-time",
            "Handle offline users with push notifications",
            "Design for message ordering and E2E encryption",
            "Partition data by conversation"
        ],
        "companies": ["google", "meta", "microsoft"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 40,
        "estimated_time": "30-35 minutes"
    },
    {
        "id": "int-030",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "system_design_notification",
        "difficulty": "medium",
        "question": "Design a notification system that can send 100M push notifications per day. What are the key components?",
        "correct_answer": "Components: 1. Notification service: receives events, looks up users, dispatches. 2. Template service: manages notification content. 3. Channel routers: push (FCM/APNS), email (SES), SMS (Twilio). 4. Queue: Kafka/SQS for async processing. 5. User preferences: store opt-outs and channels. 6. Rate limiting: prevent spam. 7. Analytics: open rates, delivery success. Scale: partition by user_id, retry failed sends, idempotency keys.",
        "options": [],
        "solution": {
            "code": "# Notification flow\nEvent -> API -> Notification Service\n                      -> User Service (preferences)\n                      -> Template Service (render content)\n                      -> Message Queue\n                      -> Channel Workers\n                           -> FCM (Android push)\n                           -> APNS (iOS push)\n                           -> Email (SMTP/SES)\n                           -> SMS (Twilio)\n                      -> Analytics",
            "explanation": "Notification systems need: fan-out (one event to many users), channel abstraction, retry logic, rate limiting, and user preference management. Decouple with queue for resilience."
        },
        "testcases": [
            {
                "input": "Design sends notifications synchronously in the request path",
                "expected": "Wrong - blocks user, loses notifications on failure"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Design uses async queue, retries, and channel abstraction",
                "expected": "Strong - production-ready architecture"
            }
        ],
        "hints": [
            "Use async queue for resilience",
            "Abstract channel differences",
            "Include rate limiting and user preferences",
            "Design for retries with idempotency"
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
        "id": "int-031",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "concurrency",
        "difficulty": "hard",
        "question": "Explain the difference between a deadlock and a race condition. How would you prevent each?",
        "correct_answer": "Deadlock: two or more threads wait for each other indefinitely. Prevention: lock ordering, lock timeout, avoid nested locks, use tryLock. Race condition: outcome depends on non-deterministic timing of concurrent execution. Prevention: mutexes, atomic operations, immutable data, thread-safe collections. Example deadlock: T1 holds A waits for B, T2 holds B waits for A. Example race: two threads increment same counter without locking.",
        "options": [],
        "solution": {
            "code": "# Deadlock example\nlock_a = Lock()\nlock_b = Lock()\n# Thread 1\nlock_a.acquire()\nlock_b.acquire()  # waits if T2 has B\n# Thread 2\nlock_b.acquire()\nlock_a.acquire()  # waits if T1 has A -> DEADLOCK\n\n# Race condition example\ncounter = 0\n# Thread 1 and 2 both do counter += 1\n# Without lock, lost updates occur",
            "explanation": "Deadlock requires 4 conditions: mutual exclusion, hold and wait, no preemption, circular wait. Break any one to prevent. Race conditions happen when shared state is accessed without synchronization."
        },
        "testcases": [
            {
                "input": "Deadlock and race condition are the same thing",
                "expected": "Wrong - deadlock is waiting, race is incorrect result"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains both with prevention strategies and examples",
                "expected": "Strong - understands concurrency deeply"
            }
        ],
        "hints": [
            "Deadlock: threads waiting for each other",
            "Race: non-deterministic incorrect result",
            "Prevention: lock ordering, atomic ops, immutability"
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
        "id": "int-032",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "security",
        "difficulty": "medium",
        "question": "What is the difference between authentication and authorization? Give an example.",
        "correct_answer": "Authentication: verifying who you are (login with username/password, OAuth, MFA). Authorization: verifying what you can do (permissions, roles, scopes). Example: You authenticate to Gmail with email+password (or SSO). Once authenticated, you can read your emails (authorized) but not someone else's (not authorized). JWT contains identity (auth) and claims/roles (authz).",
        "options": [],
        "solution": {
            "code": "# AuthN vs AuthZ\n# Authentication (AuthN): who are you?\ndef login(username, password):\n    user = db.find_user(username)\n    if verify_password(password, user.password_hash):\n        return create_session(user)\n\n# Authorization (AuthZ): what can you do?\ndef can_delete_post(user, post):\n    return user.id == post.author_id or user.role == 'admin'",
            "explanation": "AuthN happens first (login), AuthZ happens on every request (permission check). Common mistake: conflating the two. RBAC (role-based) and ABAC (attribute-based) are AuthZ patterns."
        },
        "testcases": [
            {
                "input": "They are the same thing",
                "expected": "Wrong - distinct concepts, often confused"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains both with concrete example and implementation difference",
                "expected": "Strong - understands security architecture"
            }
        ],
        "hints": [
            "AuthN = who you are",
            "AuthZ = what you can do",
            "AuthN comes first, then AuthZ"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-033",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "security_owasp",
        "difficulty": "medium",
        "question": "What is SQL injection? How would you prevent it in your application?",
        "correct_answer": "SQL injection: attacker inserts malicious SQL into user input, executed by the database. Example: login field ' OR '1'='1' -- bypasses authentication. Prevention: 1. Use parameterized queries / prepared statements. 2. Use ORM with proper escaping. 3. Input validation (whitelist). 4. Principle of least privilege for DB user. 5. WAF (Web Application Firewall) as defense in depth. Never concatenate user input into SQL strings.",
        "options": [],
    "solution": {
      "code": "# Vulnerable\nquery = f\"SELECT * FROM users WHERE name = '{username}'\"\n# Input: ' OR '1'='1 -> SELECT * FROM users WHERE name = '' OR '1'='1'\n\n# Safe: parameterized query\nquery = \"SELECT * FROM users WHERE name = %s\"\ncursor.execute(query, (username,))\n\n# Safe: ORM\nuser = User.objects.get(name=username)",
      "explanation": "SQL injection is #1 in OWASP Top 10. Always use parameterized queries. Even ORMs can be vulnerable if you use raw() with string formatting. Also: escape output, validate input, use least privilege."
    },
    "testcases": [
      {
        "input": "I sanitize input by removing quotes",
        "expected": "Weak - blacklisting is bypassable, use parameterization"
      }
    ],
    "hidden_testcases": [
      {
        "input": "Uses parameterized queries and input validation",
        "expected": "Strong - follows secure coding practices"
      }
    ],
    "hints": [
      "Use parameterized queries / prepared statements",
      "Never concatenate user input into SQL",
      "Apply principle of least privilege to DB user"
    ],
    "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google"],
    "role": ["sde", "backend-engineer"],
    "provenance": "author-verified-2026",
    "source_bank": "interview_practice_bank",
    "trust_status": "verified",
    "stage": "placement",
    "xp_reward": 25,
    "estimated_time": "20-25 minutes"
  },
  {
    "id": "int-034",
    "type": "interview",
    "topic": "technical",
    "sub_topic": "scalability",
    "difficulty": "hard",
    "question": "Explain the difference between horizontal and vertical scaling. When would you choose each?",
    "correct_answer": "Vertical scaling (scale up): add more resources (CPU, RAM, disk) to a single server. Simple, no code changes, but limited by hardware ceiling and single point of failure. Horizontal scaling (scale out): add more servers behind a load balancer. Theoretically unlimited, better fault tolerance, but requires stateless design and distributed systems complexity. Choose vertical for: simple apps, databases (initially), quick wins. Choose horizontal for: high traffic, fault tolerance, cloud-native apps.",
    "options": [],
    "solution": {
      "code": "# Vertical: bigger box\n# 1 server with 64 CPU, 256GB RAM\n\n# Horizontal: more boxes\n# Load Balancer -> [Server1, Server2, Server3, Server4]\n# Requires: stateless app, shared session store, distributed DB",
      "explanation": "Vertical scaling hits hardware limits. Horizontal scaling needs stateless services, load balancers, and distributed data. Most cloud-native systems are horizontal. Databases are often vertically scaled first, then sharded."
    },
    "testcases": [
      {
        "input": "Horizontal scaling is always better",
        "expected": "Wrong - adds complexity, not always appropriate"
      }
    ],
    "hidden_testcases": [
      {
        "input": "Explains tradeoffs with appropriate use cases",
        "expected": "Strong - understands scaling fundamentals"
      }
    ],
    "hints": [
      "Vertical: scale up single server",
      "Horizontal: scale out to multiple servers",
      "Consider complexity, cost, and fault tolerance"
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
    "id": "int-035",
    "type": "interview",
    "topic": "technical",
    "sub_topic": "scalability",
    "difficulty": "hard",
    "question": "What is database sharding? Explain the difference between horizontal and vertical sharding with examples.",
    "correct_answer": "Sharding: splitting a database across multiple servers to scale. Horizontal sharding (row-based): split rows by key. Example: users 0-1M on shard 1, 1M-2M on shard 2. Shard key: user_id. Vertical sharding (column-based): split by feature. Example: user profile in one DB, orders in another, payments in a third. Horizontal is more common for scale. Challenges: cross-shard queries, rebalancing, consistent hashing.",
    "options": [],
    "solution": {
      "code": "# Horizontal sharding (by user_id)\nshard_1: users WHERE user_id % 4 = 0\nshard_2: users WHERE user_id % 4 = 1\nshard_3: users WHERE user_id % 4 = 2\nshard_4: users WHERE user_id % 4 = 3\n\n# Vertical sharding (by feature)\ndb_users: profile, preferences\ndb_orders: order history\ndb_analytics: events, logs",
      "explanation": "Sharding distributes load but adds complexity. Choose shard key carefully: high cardinality, even distribution, query patterns. Avoid cross-shard joins. Rebalancing is hard - plan ahead with consistent hashing."
    },
    "testcases": [
      {
        "input": "Sharding means putting tables in different databases",
        "expected": "Confused with vertical sharding only"
      }
    ],
    "hidden_testcases": [
      {
        "input": "Explains both types with shard key considerations",
        "expected": "Strong - understands database scaling"
      }
    ],
    "hints": [
      "Horizontal: split rows by key",
      "Vertical: split by feature/table",
      "Choose shard key carefully (cardinality, distribution)"
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
    "id": "int-036",
    "type": "interview",
    "topic": "technical",
    "sub_topic": "load_balancing",
    "difficulty": "medium",
    "question": "What is a load balancer? Explain different load balancing algorithms and their tradeoffs.",
    "correct_answer": "Load balancer: distributes traffic across multiple servers. Algorithms: 1. Round Robin: simple, equal distribution, doesn't consider server load. 2. Least Connections: routes to server with fewest active connections, good for variable session lengths. 3. Weighted Round Robin: assigns weights to servers based on capacity. 4. IP Hash: same client always goes to same server (sticky sessions). 5. Least Response Time: routes to fastest responding server. Tradeoffs: simplicity vs awareness, session affinity needs.",
    "options": [],
    "solution": {
      "code": "# Nginx example\nupstream backend {\n    least_conn;  # algorithm\n    server backend1.example.com weight=3;\n    server backend2.example.com weight=1;\n    server backend3.example.com;\n}\n\nserver {\n    location / {\n        proxy_pass http://backend;\n    }\n}",
      "explanation": "Load balancers are the entry point for horizontal scaling. Layer 4 (TCP) is faster but less smart. Layer 7 (HTTP) can route based on path, headers, cookies. Health checks prevent routing to dead servers."
    },
    "testcases": [
      {
        "input": "Round Robin is always the best algorithm",
        "expected": "Wrong - depends on workload characteristics"
      }
    ],
    "hidden_testcases": [
      {
        "input": "Explains multiple algorithms with appropriate use cases",
        "expected": "Strong - understands load balancing tradeoffs"
      }
    ],
    "hints": [
      "Round Robin: simple, equal",
      "Least Connections: for variable sessions",
      "Consider health checks and sticky sessions"
    ],
    "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google"],
    "role": ["sde", "backend-engineer"],
    "provenance": "author-verified-2026",
    "source_bank": "interview_practice_bank",
    "trust_status": "verified",
    "stage": "placement",
    "xp_reward": 25,
    "estimated_time": "20-25 minutes"
  }
]

# Write the new questions to a temp file
import json
with open('backend/app/data/interview_practice_bank.json', 'r') as f:
    data = json.load(f)
data.extend(new_questions)
with open('backend/app/data/interview_practice_bank.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Added {len(new_questions)} questions. Total: {len(data)}')
