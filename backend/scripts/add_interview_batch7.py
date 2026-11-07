import json

new_questions = [
    {
        "id": "int-073",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "adaptability",
        "difficulty": "medium",
        "question": "Describe a time you had to quickly adapt to a major change in project requirements. What did you do?",
        "correct_answer": "STAR method: Situation - product manager changed core feature 1 week before launch. Task - adapt without derailing timeline. Action - assessed impact, identified what could be reused, proposed phased approach (ship core, add new feature in update). Result - shipped on time with core functionality, new feature in v2, no team burnout.",
        "options": [],
        "solution": {
            "code": "# Adaptability framework\n1. Assess what's changing and why\n2. Identify reusable components\n3. Propose realistic alternatives\n4. Communicate tradeoffs to stakeholders\n5. Protect team from whiplash",
            "explanation": "Adaptability tests resilience and problem-solving. Show you don't panic, you assess, you propose alternatives. Protect the team from constant context switching."
        },
        "testcases": [
            {
                "input": "I complained about the changing requirements",
                "expected": "Weak - focuses on problem, not solution"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows rapid reassessment and realistic replanning",
                "expected": "Strong - demonstrates adaptability"
            }
        ],
        "hints": [
            "Assess impact quickly",
            "Find what's reusable",
            "Propose phased approach"
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
        "id": "int-074",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "criticism",
        "difficulty": "medium",
        "question": "Tell me about a time you received harsh criticism. How did you respond?",
        "correct_answer": "STAR method: Situation - architect publicly criticized my design as 'over-engineered'. Task - handle feedback professionally. Action - asked for specific concerns privately, realized 30% was valid, refactored with simpler approach, presented improved design. Result - design accepted, earned architect's respect, learned to seek feedback earlier.",
        "options": [],
        "solution": {
            "code": "# Handling harsh criticism\n1. Don't react emotionally\n2. Ask for specifics\n3. Separate valid points from tone\n4. Make improvements\n5. Follow up to show growth",
            "explanation": "Criticism questions test ego and coachability. Show you can separate message from delivery. Focus on what you learned and how you improved. Don't hold grudges."
        },
        "testcases": [
            {
                "input": "I argued back and proved them wrong",
                "expected": "Weak - defensive, no growth"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows reflection, improvement, and relationship repair",
                "expected": "Strong - coachable and mature"
            }
        ],
        "hints": [
            "Separate message from delivery tone",
            "Find valid points and act on them",
            "Show growth and relationship repair"
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
        "id": "int-075",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "salary_negotiation",
        "difficulty": "medium",
        "question": "How do you approach salary negotiation?",
        "correct_answer": "Research-based approach: 'I research market rates using Levels.fyi, Glassdoor, and industry reports. I consider total compensation: base, bonus, equity, benefits. I present a range based on my experience and the value I bring. I'm flexible but know my worth. I focus on the total package, not just base salary. If the offer is below range, I explain why I'm worth more based on [specific achievements].'",
        "options": [],
        "solution": {
            "code": "# Negotiation strategy\n1. Research market rate beforehand\n2. Consider total compensation (base, bonus, equity)\n3. Present range, not single number\n4. Justify with specific achievements\n5. Be willing to walk away\n6. Get everything in writing",
            "explanation": "Negotiation tests self-worth and preparation. Research thoroughly. Show you understand total compensation. Justify ask with achievements. Be professional, not greedy."
        },
        "testcases": [
            {
                "input": "I just accept whatever they offer",
                "expected": "Weak - shows no self-worth or research"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows research, justification, and professionalism",
                "expected": "Strong - knows their worth"
            }
        ],
        "hints": [
            "Research market rates",
            "Consider total compensation",
            "Justify with achievements"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-076",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "system_design_ecommerce",
        "difficulty": "hard",
        "question": "Design an e-commerce checkout system. How would you handle inventory, payments, and order confirmation?",
        "correct_answer": "Components: 1. Cart service: manages items, calculates totals. 2. Inventory service: reserves stock, handles concurrency. 3. Payment gateway: integrates Stripe/PayPal, handles retries. 4. Order service: creates order, coordinates flow. 5. Notification service: sends confirmation. Flow: Create order -> reserve inventory (pessimistic lock or optimistic) -> process payment -> confirm order -> release inventory on failure. Idempotency keys prevent duplicate charges. Saga pattern for distributed transaction.",
        "options": [],
        "solution": {
            "code": "# Checkout flow\n1. POST /checkout (create pending order)\n2. Reserve inventory (pessimistic lock or decrement with version)\n3. Process payment (idempotency key)\n4. If payment succeeds: confirm order, deduct inventory\n5. If payment fails: release inventory, cancel order\n6. Send confirmation email/SMS\n\n# Distributed transaction with Saga\n- Compensating actions for rollback\n- Idempotency keys for retries\n- Dead letter queue for failed payments",
            "explanation": "E-commerce checkout needs consistency across inventory, payment, and order. Distributed transactions are hard - use Saga pattern with compensating actions. Idempotency prevents duplicate charges. Inventory locking prevents overselling."
        },
        "testcases": [
            {
                "input": "Use single database transaction for entire checkout",
                "expected": "Wrong - doesn't scale across services"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Discovers inventory locking, idempotency, and distributed consistency",
                "expected": "Strong - understands e-commerce systems"
            }
        ],
        "hints": [
            "Prevent overselling with inventory locking",
            "Handle payment failures gracefully",
            "Use idempotency to prevent duplicates"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 40,
        "estimated_time": "30-35 minutes"
    },
    {
        "id": "int-077",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "performance_optimization",
        "difficulty": "hard",
        "question": "A page load time increased from 2s to 8s after a deployment. How would you investigate and fix it?",
        "correct_answer": "Investigation: 1. Check deployment diff (what changed). 2. Profile: APM tools (New Relic, Datadog), browser devtools, database queries. 3. Identify bottleneck: N+1 queries, missing index, large payload, no caching. 4. Check infrastructure: server load, network, CDN. Fix: optimize query, add index, cache response, reduce payload, lazy load assets. Prevention: performance budgets, CI performance tests, monitoring alerts.",
        "options": [],
        "solution": {
            "code": "# Investigation steps\n1. Rollback and confirm it's the deployment\n2. Check APM for slow endpoints\n3. Database: EXPLAIN slow queries\n4. Frontend: Chrome DevTools Network tab\n5. Infrastructure: server metrics, CDN status\n\n# Common fixes\n- Add database index\n- Cache expensive queries\n- Reduce payload size\n- Lazy load non-critical assets\n- Use CDN for static files",
            "explanation": "Performance debugging is systematic. Start with rollback to confirm cause. Use profiling tools, not guessing. Common causes: N+1 queries, missing indexes, large responses. Prevention is better than reaction."
        },
        "testcases": [
            {
                "input": "Add more server resources",
                "expected": "Premature - find root cause first"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows systematic investigation and prevention",
                "expected": "Strong - understands performance debugging"
            }
        ],
        "hints": [
            "Rollback first to confirm cause",
            "Profile before optimizing",
            "Common causes: N+1, missing index, large payload"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "frontend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 35,
        "estimated_time": "25-30 minutes"
    },
    {
        "id": "int-078",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "authentication",
        "difficulty": "medium",
        "question": "Explain how JWT (JSON Web Token) authentication works. What are the advantages and disadvantages compared to session-based auth?",
        "correct_answer": "JWT: user logs in, server creates token with payload (user_id, expiry) and signs it with secret. Client stores and sends token in Authorization header. Server validates signature without DB lookup. Advantages: stateless, scalable across servers, good for mobile/SPA. Disadvantages: can't revoke before expiry (without blacklist), larger than session ID, XSS risk if stored in localStorage, secret key compromise is catastrophic. Session auth: server stores session in DB/Redis, sends session ID cookie. Revocable, smaller, but requires shared session store.",
        "options": [],
        "solution": {
            "code": "# JWT flow\n1. Client sends username/password\n2. Server validates, creates JWT\n   payload = {'user_id': 123, 'exp': datetime.utcnow() + timedelta(hours=1)}\n   token = jwt.encode(payload, SECRET, algorithm='HS256')\n3. Client stores token (httpOnly cookie or localStorage)\n4. Client sends: Authorization: Bearer <token>\n5. Server verifies signature, extracts user_id\n\n# Session flow\n1. Client sends username/password\n2. Server creates session in Redis\n3. Server sends session_id in httpOnly cookie\n4. Client sends cookie automatically\n5. Server looks up session in Redis",
            "explanation": "JWT is popular for SPAs and mobile apps. The key tradeoff: statelessness vs revocability. JWT can't be revoked easily (problem for logout/ban). Sessions require shared store but are revocable. Many systems use httpOnly cookies for both."
        },
        "testcases": [
            {
                "input": "JWT can be invalidated by the server anytime",
                "expected": "Wrong - that's the disadvantage of JWT"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains statelessness, revocation challenges, and security tradeoffs",
                "expected": "Strong - understands authentication deeply"
            }
        ],
        "hints": [
            "JWT is stateless, signed token",
            "Can't revoke before expiry easily",
            "Consider XSS and secret key security"
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
        "id": "int-079",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "circuit_breaker",
        "difficulty": "hard",
        "question": "What is the Circuit Breaker pattern? When would you use it and how does it work?",
        "correct_answer": "Circuit Breaker: prevents cascading failures in distributed systems. States: 1. Closed: requests flow, failures counted. If failures exceed threshold, open circuit. 2. Open: requests fail immediately, no calls to failing service. After timeout, go to Half-Open. 3. Half-Open: allow limited requests. If success, close circuit. If failure, open again. Use when: calling external services, microservices communication, any network call that can fail. Libraries: Hystrix, Polly, resilience4j.",
        "options": [],
        "solution": {
            "code": "# Circuit breaker states\nCLOSED -> (failures > threshold) -> OPEN\nOPEN -> (timeout expires) -> HALF_OPEN\nHALF_OPEN -> (success) -> CLOSED\nHALF_OPEN -> (failure) -> OPEN\n\n# Usage\n@circuit_breaker(failure_threshold=5, recovery_timeout=60)\ndef call_external_service(data):\n    return requests.post(URL, json=data, timeout=3)",
            "explanation": "Circuit breakers stop wasting resources on failing services. They give failing services time to recover. Essential for resilience in microservices. Fallback logic provides graceful degradation."
        },
        "testcases": [
            {
                "input": "Retry infinitely on failure",
                "expected": "Wrong - can overwhelm failing service"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains states and fallback behavior",
                "expected": "Strong - understands resilience patterns"
            }
        ],
        "hints": [
            "Three states: closed, open, half-open",
            "Prevents cascading failures",
            "Include fallback behavior"
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
        "id": "int-080",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "team_conflict",
        "difficulty": "medium",
        "question": "Describe a time you had to mediate a conflict between two team members. What was your approach?",
        "correct_answer": "STAR method: Situation - two engineers disagreed on architecture, blocking sprint. Task - resolve to meet deadline. Action - scheduled separate 1:1s to understand each perspective, found common ground (both wanted scalability), facilitated joint session focusing on data not opinions, proposed hybrid approach. Result - agreed on solution, delivered on time, both felt heard.",
        "options": [],
        "solution": {
            "code": "# Mediation approach\n1. Understand each side separately first\n2. Find shared goals\n3. Facilitate joint discussion\n4. Focus on data, not opinions\n5. Propose win-win solutions\n6. Document agreement",
            "explanation": "Mediation tests emotional intelligence and facilitation. Show you can remain neutral, understand both sides, and find common ground. Don't take sides - focus on team goals."
        },
        "testcases": [
            {
                "input": "I sided with the person I agreed with",
                "expected": "Weak - not neutral, no mediation"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows neutrality, understanding both sides, and win-win solution",
                "expected": "Strong - demonstrates mediation skill"
            }
        ],
        "hints": [
            "Listen to both sides separately",
            "Find shared goals",
            "Focus on data, not opinions"
        ],
        "companies": ["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
        "role": ["sde", "backend-engineer", "product-manager"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-081",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "relocation",
        "difficulty": "easy",
        "question": "Would you be willing to relocate or travel for work?",
        "correct_answer": "Show flexibility with conditions: 'Yes, I'm willing to relocate. I'm excited about the opportunity and the team. I can make the move within [reasonable timeframe]. I'm also open to occasional travel for conferences or client meetings if needed.' If not willing: be honest but emphasize interest in remote/hybrid options. Show enthusiasm for the role over logistics.",
        "options": [],
        "solution": {
            "code": "# If willing\nYes, I'm fully willing to relocate.\nI've researched the area and am excited about the opportunity.\nI can make the move within [timeframe].\n\n# If conditional\nI prefer [current location] but am flexible for the right opportunity.\nI'm open to hybrid arrangements.",
            "explanation": "Relocation questions test commitment. Companies want to know you'll actually join. Show enthusiasm. If you have constraints, mention them early but emphasize flexibility."
        },
        "testcases": [
            {
                "input": "No, I will never leave my city",
                "expected": "May disqualify for roles requiring mobility"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows flexibility and enthusiasm",
                "expected": "Strong - demonstrates commitment"
            }
        ],
        "hints": [
            "Show enthusiasm for the opportunity",
            "Be honest about constraints",
            "Emphasize commitment to role"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 10,
        "estimated_time": "5-10 minutes"
    },
    {
        "id": "int-082",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "oauth",
        "difficulty": "medium",
        "question": "Explain how OAuth 2.0 works. What is the difference between authorization code flow and implicit flow?",
        "correct_answer": "OAuth 2.0: authorization framework allowing third-party apps limited access without sharing credentials. Authorization Code Flow: 1. App redirects user to authorization server. 2. User authenticates and consents. 3. Server returns authorization code. 4. App exchanges code for access token (server-to-server). 5. App uses token to access resources. Secure because token never exposed to browser. Implicit Flow: access token returned directly in redirect fragment. Deprecated for SPAs due to security issues. Use Authorization Code + PKCE for SPAs.",
        "options": [],
        "solution": {
            "code": "# Authorization Code Flow\n1. GET /authorize?client_id=...&redirect_uri=...&response_type=code\n2. User logs in, consents\n3. Redirect to: /callback?code=AUTH_CODE\n4. POST /token with code + client_secret\n5. Receive access_token\n6. GET /api/resource with Authorization: Bearer token",
            "explanation": "OAuth 2.0 is the standard for delegated authorization. Authorization code flow is most secure. Implicit flow is deprecated due to token exposure. Always use PKCE for public clients (SPAs, mobile)."
        },
        "testcases": [
            {
                "input": "OAuth is for authentication",
                "expected": "Wrong - OAuth is for authorization, OpenID Connect is for authentication"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains flows with security implications",
                "expected": "Strong - understands OAuth deeply"
            }
        ],
        "hints": [
            "OAuth is authorization, not authentication",
            "Authorization code is most secure",
            "Implicit flow is deprecated"
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
        "id": "int-083",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "initiative",
        "difficulty": "medium",
        "question": "Tell me about a time you identified a problem that no one else noticed. What did you do?",
        "correct_answer": "STAR method: Situation - noticed our error logs were silently failing. Task - investigate and fix. Action - set up alerting, found 15% of requests failing silently, traced to timeout config, proposed fix, presented to team. Result - fixed in 2 days, prevented customer impact, team added monitoring for all critical paths.",
        "options": [],
        "solution": {
            "code": "# Initiative example\n1. Notice something others missed\n2. Investigate root cause\n3. Propose solution with data\n4. Implement or advocate\n5. Measure impact\n6. Prevent recurrence",
            "explanation": "Initiative questions test proactivity and ownership. Show you don't just wait for assignments. Find problems, propose solutions, measure impact. Great employees improve systems, not just tickets."
        },
        "testcases": [
            {
                "input": "I just reported it and moved on",
                "expected": "Weak - no ownership or follow-through"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows investigation, solution, and prevention",
                "expected": "Strong - demonstrates initiative"
            }
        ],
        "hints": [
            "Show you noticed something others missed",
            "Investigate root cause",
            "Propose and implement solution"
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
        "id": "int-084",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "motivation",
        "difficulty": "easy",
        "question": "What motivates you to do your best work?",
        "correct_answer": "Specific and genuine: 'I'm motivated by solving hard problems that have real impact. I like seeing users benefit from my work. I'm motivated by learning and growth - I enjoy figuring out how things work and improving them. I also thrive in collaborative environments where we can build something bigger together.' Avoid: money only, or generic 'I like challenges'.",
        "options": [],
        "solution": {
            "code": "# Good motivation\n1. Impact: solving real problems\n2. Growth: learning and mastery\n3. Autonomy: ownership of work\n4. Purpose: meaningful mission\n5. Collaboration: great team\n\n# Weak motivation\n- Money\n- 'I just like challenges' (too vague)",
            "explanation": "Motivation questions test cultural fit and drive. Show intrinsic motivators, not just extrinsic. Connect to the company's mission. Be specific about what energizes you."
        },
        "testcases": [
            {
                "input": "Money is my only motivation",
                "expected": "Red flag - no intrinsic drive"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows specific intrinsic motivators",
                "expected": "Strong - self-aware and driven"
            }
        ],
        "hints": [
            "Focus on intrinsic motivators",
            "Connect to company mission",
            "Be specific, not generic"
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
        "id": "int-085",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "eventual_consistency",
        "difficulty": "hard",
        "question": "What is eventual consistency? When would you accept it and when would you need strong consistency?",
        "correct_answer": "Eventual consistency: replicas may temporarily diverge but will eventually converge if no new writes. Accept when: user profiles, social media feeds, product catalogs, analytics - where slight staleness is acceptable and availability/partition tolerance matters. Need strong consistency when: banking (balance), inventory (overselling), booking systems (double booking). Tradeoff: CAP theorem - during partition, choose C or A. Use version vectors, CRDTs, or conflict resolution for eventual consistency.",
        "options": [],
        "solution": {
            "code": "# Eventual consistency example\nUser updates profile:\n- Write to primary DB\n- Async replicate to 3 replicas\n- Read may return old value for 100ms\n- Eventually all replicas match\n\n# Strong consistency\nBank transfer:\n- Read balance with lock\n- Update balance\n- Commit transaction\n- All readers see new balance immediately",
            "explanation": "Distributed systems must trade consistency for availability during partitions. Eventual consistency enables high availability but requires conflict resolution. Strong consistency is simpler but sacrifices availability."
        },
        "testcases": [
            {
                "input": "Eventual consistency is always preferable",
                "expected": "Wrong - depends on data criticality"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains tradeoffs with appropriate use cases",
                "expected": "Strong - understands distributed data"
            }
        ],
        "hints": [
            "Eventual: replicas converge over time",
            "Strong: immediate consistency",
            "Consider data criticality and availability needs"
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
        "id": "int-086",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "garbage_collection",
        "difficulty": "medium",
        "question": "What is garbage collection? Explain different GC algorithms and their tradeoffs.",
        "correct_answer": "GC: automatic memory management, reclaims unused objects. Algorithms: 1. Mark and Sweep: mark reachable objects, sweep unreachable. Simple but causes fragmentation. 2. Copying (Semispace): copy live objects to new space, swap. No fragmentation but wastes 50% memory. 3. Generational: young generation (frequent, fast GC) + old generation (infrequent, thorough GC). Most modern JVMs use this. 4. Reference Counting: count references, collect when 0. Fast but can't handle cycles. Tradeoffs: pause time vs throughput, memory overhead, fragmentation.",
        "options": [],
        "solution": {
            "code": "# Generational GC in JVM\nEden (new objects) -> Survivor S0/S1 -> Old Generation\n\nYoung GC (Minor GC):\n- Frequent, fast\n- Collects short-lived objects\n\nOld GC (Major GC):\n- Infrequent, slower\n- Collects long-lived objects",
            "explanation": "GC trades CPU for memory safety. Most objects die young (generational hypothesis). G1 and ZGC in Java optimize for low pause times. Understanding GC helps diagnose performance issues (GC pauses, memory leaks)."
        },
        "testcases": [
            {
                "input": "GC always pauses all threads",
                "expected": "Wrong - concurrent collectors minimize pauses"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains algorithms with tradeoffs",
                "expected": "Strong - understands memory management"
            }
        ],
        "hints": [
            "GC reclaims unused memory",
            "Generational: most objects die young",
            "Tradeoffs: pause time vs throughput"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    }
]

with open('backend/app/data/interview_practice_bank.json', 'r') as f:
    data = json.load(f)
data.extend(new_questions)
with open('backend/app/data/interview_practice_bank.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Added {len(new_questions)} questions. Total: {len(data)}')
