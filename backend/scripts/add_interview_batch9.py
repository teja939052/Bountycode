import json

new_questions = [
    {
        "id": "int-101",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "dependency_management",
        "difficulty": "medium",
        "question": "How do you manage dependencies in your projects? Explain semantic versioning and how you handle breaking changes.",
        "correct_answer": "Semantic versioning (SemVer): MAJOR.MINOR.PATCH. MAJOR: breaking changes. MINOR: new features, backward compatible. PATCH: bug fixes. Practices: 1. Lock files (package-lock.json, Pipfile.lock) for reproducible builds. 2. Regular updates with automated tools (Dependabot, Renovate). 3. Review breaking changes before upgrading major versions. 4. Use virtual environments/containers to isolate dependencies. 5. Minimize dependencies - each one is a risk. 6. Pin critical dependencies in production.",
        "options": [],
        "solution": {
            "code": "# Dependency management\n1. Lock files for reproducibility\n2. Semantic versioning understanding\n   - ^1.2.3: >=1.2.3 <2.0.0\n   - ~1.2.3: >=1.2.3 <1.3.0\n   - 1.2.3: exact\n3. Automated dependency updates\n4. Security scanning (npm audit, snyk)\n5. Regular cleanup of unused dependencies",
            "explanation": "Dependencies are a major source of vulnerabilities and breakage. Show you understand versioning, use lock files, and have a strategy for updates. Minimizing dependencies reduces attack surface."
        },
        "testcases": [
            {
                "input": "I always use latest versions of everything",
                "expected": "Wrong - latest can have breaking changes"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows versioning understanding and update strategy",
                "expected": "Strong - understands dependency management"
            }
        ],
        "hints": [
            "Understand semantic versioning",
            "Use lock files for reproducibility",
            "Update dependencies strategically"
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
        "id": "int-102",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "networking_https",
        "difficulty": "medium",
        "question": "What happens when you type a URL into a browser and press Enter? Walk me through the entire process.",
        "correct_answer": "1. Browser parses URL, checks DNS cache. 2. DNS resolution: browser -> OS cache -> DNS server -> IP address. 3. TCP handshake: SYN, SYN-ACK, ACK. 4. TLS handshake (if HTTPS): cipher negotiation, certificate verification, key exchange. 5. HTTP request sent: headers, cookies, body. 6. Server processes: load balancer -> app server -> database. 7. Response returned: HTML, CSS, JS. 8. Browser renders: DOM tree, CSSOM, render tree, layout, paint. 9. JavaScript execution, additional requests for resources.",
        "options": [],
        "solution": {
            "code": "# Simplified flow\n1. URL parsing\n   - Protocol: https://\n   - Domain: example.com\n   - Path: /page\n\n2. DNS lookup\n   - Browser cache -> OS cache -> DNS server\n   - Returns IP: 93.184.216.34\n\n3. TCP connection\n   - SYN -> SYN-ACK -> ACK\n\n4. TLS handshake\n   - Certificate verification\n   - Symmetric key exchange\n\n5. HTTP GET /page\n   - Headers: Host, User-Agent, Cookies\n\n6. Server response\n   - 200 OK\n   - HTML body\n\n7. Browser rendering\n   - Parse HTML -> DOM\n   - Parse CSS -> CSSOM\n   - Combine -> Render tree\n   - Layout -> Paint",
            "explanation": "This tests full-stack understanding. Show depth at each layer: DNS, TCP, TLS, HTTP, server processing, rendering. Mention optimizations: caching, CDNs, HTTP/2, connection pooling."
        },
        "testcases": [
            {
                "input": "The browser directly connects to the server IP without DNS",
                "expected": "Wrong - DNS resolution happens first"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows end-to-end flow with DNS, TCP, TLS, HTTP, rendering",
                "expected": "Strong - understands full stack"
            }
        ],
        "hints": [
            "DNS resolution first",
            "TCP handshake, then TLS for HTTPS",
            "Server processing, then rendering"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "frontend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
            "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-103",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "burnout",
        "difficulty": "medium",
        "question": "Tell me about a time you experienced burnout or saw a teammate burning out. What did you do?",
        "correct_answer": "STAR method: Situation - teammate working 80 hour weeks for 2 months. Task - prevent burnout without dropping ball. Action - 1:1 to understand workload, proposed re-prioritization with manager, redistributed tasks, set boundaries, encouraged time off. Result - teammate took vacation, returned refreshed, team adjusted sprint planning to prevent recurrence. For self: 'I recognized signs, took a mental health day, renegotiated deadlines, now maintain better boundaries.'",
        "options": [],
        "solution": {
            "code": "# Burnout prevention\n1. Recognize signs early\n   - Exhaustion, cynicism, reduced effectiveness\n2. Address root cause\n   - Unrealistic deadlines\n   - Lack of control\n   - Insufficient recovery\n3. Take action\n   - Renegotiate scope\n   - Redistribute work\n   - Take time off\n4. Systemic fixes\n   - Realistic sprint planning\n   - Encourage PTO\n   - Regular check-ins",
            "explanation": "Burnout questions test emotional intelligence and boundaries. Show you recognize signs, act early, and address root causes. Don't glorify overwork. Good teams prevent burnout, not reward it."
        },
        "testcases": [
            {
                "input": "I pushed through and worked harder",
                "expected": "Weak - ignores burnout, unsustainable"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows early recognition and systemic prevention",
                "expected": "Strong - emotionally intelligent"
            }
        ],
        "hints": [
            "Recognize signs early",
            "Address root cause, not symptoms",
            "Show systemic prevention"
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
        "id": "int-104",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "cdn",
        "difficulty": "medium",
        "question": "What is a CDN (Content Delivery Network)? How does it work and when would you use one?",
        "correct_answer": "CDN: distributed network of servers that cache content close to users. Works: 1. User requests resource. 2. DNS routes to nearest edge server. 3. If cached, serve immediately. 4. If not, fetch from origin, cache, serve. 5. TTL controls freshness. Use when: static assets (images, CSS, JS), large files (videos), high traffic from multiple regions, API response caching. Benefits: reduced latency, lower origin load, DDoS protection. Examples: Cloudflare, Akamai, AWS CloudFront.",
        "options": [],
        "solution": {
            "code": "# CDN flow\nUser in India -> CDN Edge (Mumbai)\n    - Cache hit: serve image (50ms)\n    - Cache miss: fetch from Origin (US), cache, serve\n\n# Cache headers\nCache-Control: public, max-age=86400\nETag: 'abc123'\nLast-Modified: Mon, 01 Jan 2024 00:00:00 GMT",
            "explanation": "CDNs bring content closer to users. Edge caching reduces latency and origin load. Cache invalidation is tricky - use TTL, versioned URLs, or purge APIs. CDNs also provide DDoS protection and WAF."
        },
        "testcases": [
            {
                "input": "CDN is only for static files",
                "expected": "Partial - can also cache API responses"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains edge caching, TTL, and use cases",
                "expected": "Strong - understands CDNs"
            }
        ],
        "hints": [
            "CDN caches content at edge locations",
            "Reduces latency and origin load",
            "Use for static assets and high-traffic content"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "frontend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-105",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "web_security",
        "difficulty": "hard",
        "question": "Explain XSS, CSRF, and SQL injection. How would you prevent each in a web application?",
        "correct_answer": "XSS (Cross-Site Scripting): attacker injects scripts into pages viewed by others. Prevention: output encoding, Content-Security-Policy, input sanitization. CSRF (Cross-Site Request Forgery): attacker tricks user into executing actions. Prevention: CSRF tokens, SameSite cookies, CORS. SQL Injection: attacker manipulates SQL queries. Prevention: parameterized queries, ORMs, input validation. All three are OWASP Top 10. Defense in depth: validate input, encode output, use security headers.",
        "options": [],
        "solution": {
            "code": "# XSS prevention\n@app.route('/search')\ndef search():\n    query = request.args.get('q', '')\n    # Encode output\n    return f'<h1>Results for {escape(query)}</h1>'\n\n# CSRF prevention\n@app.route('/transfer', methods=['POST'])\n@csrf.exempt  # or validate token\n def transfer():\n    if not validate_csrf_token(request.form['csrf_token']):\n        abort(403)\n    # process transfer\n\n# SQL injection prevention\n# Use parameterized queries\ncursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
            "explanation": "Web security is about trusting nothing from the client. XSS targets users, CSRF targets actions, SQLi targets database. Defense in depth: validate input, encode output, use security headers, keep dependencies updated."
        },
        "testcases": [
            {
                "input": "Sanitizing input by removing quotes prevents SQL injection",
                "expected": "Weak - use parameterized queries instead"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows parameterized queries, output encoding, and CSRF tokens",
                "expected": "Strong - understands web security"
            }
        ],
        "hints": [
            "XSS: encode output, use CSP",
            "CSRF: tokens, SameSite cookies",
            "SQLi: parameterized queries"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "frontend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 30,
        "estimated_time": "25-30 minutes"
    },
    {
        "id": "int-106",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "learning_agility",
        "difficulty": "medium",
        "question": "Describe a time you had to learn something completely outside your expertise. How did you approach it?",
        "correct_answer": "STAR method: Situation - needed to implement ML recommendation engine, only knew basic Python. Task - learn ML and ship in 2 months. Action - took online course (Coursera), read 3 books, built 5 small prototypes, found mentor in ML team, pair-programmed on first model. Result - shipped basic recommender, increased engagement 15%, now ML is my primary focus.",
        "options": [],
        "solution": {
            "code": "# Learning framework\n1. Identify smallest useful subset to learn\n2. Find quality resources (courses, docs, books)\n3. Build small prototypes immediately\n4. Find a mentor or community\n5. Apply in real project with safety net\n6. Teach others to solidify knowledge",
            "explanation": "Learning agility is a top hiring signal. Show you can learn independently and quickly. Structured approach beats random reading. Mentorship and real application accelerate learning."
        },
        "testcases": [
            {
                "input": "I read the documentation and figured it out",
                "expected": "Weak - passive learning, no proof of depth"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows structured learning with mentorship and application",
                "expected": "Strong - demonstrates learning agility"
            }
        ],
        "hints": [
            "Show structured approach",
            "Mention seeking help/mentorship",
            "Quantify outcome"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-107",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "weaknesses",
        "difficulty": "easy",
        "question": "What is your greatest weakness?",
        "correct_answer": "Pick a real weakness with improvement plan: 'I used to struggle with public speaking. I joined Toastmasters and now present at team tech talks monthly. I'm still not perfect, but I've improved significantly.' Or: 'I sometimes take on too much responsibility. I've learned to delegate more and set clearer boundaries.' Avoid: 'I'm a perfectionist' or 'I work too hard' - these are clichés.",
        "options": [],
        "solution": {
            "code": "# Good weakness\n- Genuine weakness, not a strength in disguise\n- Shows self-awareness\n- Has concrete improvement plan\n- Not a deal-breaker for the role\n\n# Bad weakness\n- 'I'm a perfectionist' (cliché)\n- 'I work too hard' (not a weakness)\n- 'I have no weaknesses' (lacks self-awareness)",
            "explanation": "Weakness questions test self-awareness and honesty. Pick a real weakness, not a disguised strength. Show you're actively improving. Make sure it's not a core requirement of the job."
        },
        "testcases": [
            {
                "input": "My greatest weakness is that I'm a perfectionist",
                "expected": "Cliché - interviewer has heard this 1000 times"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Genuine weakness with concrete improvement plan",
                "expected": "Strong - self-aware and growing"
            }
        ],
        "hints": [
            "Pick a real weakness",
            "Show improvement plan",
            "Avoid clichés"
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
        "id": "int-108",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "containerization",
        "difficulty": "medium",
        "question": "What is Docker? Explain the difference between Docker image and Docker container, and when you would use Docker Compose.",
        "correct_answer": "Docker: platform for containerization. Image: blueprint/template with app + dependencies + runtime. Immutable, versioned. Container: running instance of an image. Ephemeral, isolated. Docker Compose: tool for defining multi-container applications in YAML. Use when: app needs multiple services (web, db, cache), local development mirrors production, easy startup with one command. Example: docker-compose.yml defines web, database, redis services.",
        "options": [],
        "solution": {
            "code": "# Dockerfile (image blueprint)\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']\n\n# Build image\n# docker build -t myapp:1.0 .\n\n# Run container\n# docker run -p 8000:8000 myapp:1.0\n\n# Docker Compose\nversion: '3.8'\nservices:\n  web:\n    build: .\n    ports:\n      - '8000:8000'\n    depends_on:\n      - db\n  db:\n    image: postgres:15\n    environment:\n      POSTGRES_DB: myapp",
            "explanation": "Docker ensures consistency across environments. Images are versioned blueprints. Containers are lightweight, isolated, and ephemeral. Compose simplifies multi-service orchestration for development."
        },
        "testcases": [
            {
                "input": "Docker containers are lightweight VMs",
                "expected": "Wrong - containers share kernel, VMs don't"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains image vs container and Compose use cases",
                "expected": "Strong - understands containerization"
            }
        ],
        "hints": [
            "Image = blueprint, container = running instance",
            "Containers share host kernel",
            "Compose for multi-container apps"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "devops-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-109",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "overqualified",
        "difficulty": "medium",
        "question": "Are you overqualified for this position?",
        "correct_answer": "Address honestly and positively: 'I may have more experience than required, but I'm genuinely excited about this role and the team. I'm looking for [specific aspects: impact, technology, culture] rather than just a title. I'm committed to doing the work at hand and contributing at every level. If this role is a step back in title, it's a step forward in [specific interest].' Show enthusiasm, not arrogance. Emphasize fit and interest, not just qualifications.",
        "options": [],
        "solution": {
            "code": "# Good answer\n- Acknowledge the perception\n- Explain genuine interest\n- Emphasize what you'll contribute\n- Show humility and enthusiasm\n\n# Bad answer\n- 'I'm not overqualified' (defensive)\n- 'I need a job' (desperate)\n- 'I'll probably leave soon' (red flag)",
            "explanation": "Overqualified questions test whether you'll stay and be happy. Show you're interested in the work, not just the title. Address concerns directly. Emphasize what you'll contribute, not what you'll gain."
        },
        "testcases": [
            {
                "input": "I'm not overqualified, I'm perfectly qualified",
                "expected": "Defensive - doesn't address concern"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows humility, enthusiasm, and genuine interest",
                "expected": "Strong - addresses concern maturely"
            }
        ],
        "hints": [
            "Acknowledge without arrogance",
            "Explain genuine interest",
            "Emphasize contribution, not title"
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
        "id": "int-110",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "pagination",
        "difficulty": "medium",
        "question": "How would you implement pagination for a large dataset? Explain different pagination strategies and their tradeoffs.",
        "correct_answer": "Strategies: 1. Offset pagination: LIMIT 20 OFFSET 0. Simple but slow for deep pages (OFFSET scans skipped rows). 2. Cursor/keyset pagination: WHERE id > last_seen_id ORDER BY id LIMIT 20. Fast, consistent, but requires stable sort column. 3. Seek method: similar to cursor, uses indexed column. Tradeoffs: offset is easy but O(n) for deep pages. Cursor is O(1) but can't jump to arbitrary page. For infinite scroll: cursor. For page numbers: offset with limit (e.g., max 100 pages).",
        "options": [],
        "solution": {
            "code": "# Offset pagination\nSELECT * FROM products\nORDER BY created_at DESC\nLIMIT 20 OFFSET 1000;  -- Slow!\n\n# Cursor pagination\nSELECT * FROM products\nWHERE created_at < '2024-01-01'\nORDER BY created_at DESC\nLIMIT 20;  -- Fast!\n\n# Keyset pagination\nSELECT * FROM products\nWHERE id > 1000\nORDER BY id\nLIMIT 20;  -- Fast and stable",
            "explanation": "Pagination is deceptively complex. Offset pagination becomes slow for deep pages because DB must scan and discard rows. Cursor pagination uses indexed column for O(1) access. Choose based on UX: page numbers vs infinite scroll."
        },
        "testcases": [
            {
                "input": "Offset pagination is always the best approach",
                "expected": "Wrong - slow for deep pages"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains offset vs cursor with tradeoffs",
                "expected": "Strong - understands pagination deeply"
            }
        ],
        "hints": [
            "Offset is simple but slow for deep pages",
            "Cursor uses indexed column for speed",
            "Consider UX: page numbers vs infinite scroll"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-111",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "culture_fit",
        "difficulty": "easy",
        "question": "What type of work environment helps you do your best work?",
        "correct_answer": "Specific and balanced: 'I do my best work in environments with clear goals and autonomy. I like teams that trust each other, share feedback openly, and celebrate wins. I need some quiet focus time but also value collaboration. I thrive when I understand how my work impacts the bigger picture. I appreciate psychological safety where it's okay to say I don't know or make mistakes.'",
        "options": [],
        "solution": {
            "code": "# Environment factors\n1. Autonomy: trust me to deliver\n2. Clear goals: know what success looks like\n3. Feedback: regular, constructive, bidirectional\n4. Collaboration: smart people to learn from\n5. Psychological safety: admit mistakes, ask questions\n6. Impact: see how work matters",
            "explanation": "Culture fit is about mutual compatibility. Be specific about what you need, not just 'nice people'. Show you're self-aware and will thrive in their environment if it matches."
        },
        "testcases": [
            {
                "input": "I just want to work with nice people",
                "expected": "Too vague - no specifics"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows specific needs and self-awareness",
                "expected": "Strong - culture-aware"
            }
        ],
        "hints": [
            "Be specific about what you need",
            "Show self-awareness",
            "Connect to company values"
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
        "id": "int-112",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "web_sockets",
        "difficulty": "medium",
        "question": "What are WebSockets and when would you use them instead of HTTP?",
        "correct_answer": "WebSocket: full-duplex persistent TCP connection between client and server. Use when: real-time features (chat, live updates, gaming), frequent small messages, low latency needed. HTTP: request-response, stateless, simpler. Use for: REST APIs, file downloads, form submissions. WebSocket advantages: real-time push, lower overhead after handshake, full-duplex. Disadvantages: more complex, firewall issues, scaling harder (sticky sessions). Libraries: Socket.IO, ws, SignalR.",
        "options": [],
        "solution": {
            "code": "# WebSocket server (Node.js + ws)\nconst WebSocket = require('ws');\nconst wss = new WebSocket.Server({ port: 8080 });\n\nwss.on('connection', (ws) => {\n  ws.on('message', (data) => {\n    // Broadcast to all clients\n    wss.clients.forEach((client) => {\n      if (client.readyState === WebSocket.OPEN) {\n        client.send(data);\n      }\n    });\n  });\n});\n\n// Client\nconst ws = new WebSocket('ws://localhost:8080');\nws.onmessage = (event) => console.log(event.data);",
            "explanation": "WebSockets enable real-time bidirectional communication. HTTP polling is inefficient. WebSockets have connection overhead but low per-message cost. Scaling requires sticky sessions or pub/sub for multi-server."
        },
        "testcases": [
            {
                "input": "Use HTTP polling for real-time chat",
                "expected": "Inefficient - WebSocket is better for real-time"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains full-duplex nature and appropriate use cases",
                "expected": "Strong - understands real-time communication"
            }
        ],
        "hints": [
            "WebSocket is full-duplex persistent connection",
            "Use for real-time features",
            "HTTP for request-response patterns"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "frontend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-113",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "decision_making",
        "difficulty": "medium",
        "question": "Describe a time you made a decision that was unpopular. How did you handle it?",
        "correct_answer": "STAR method: Situation - team wanted to rewrite working code in new framework. Task - decide whether to approve. Action - analyzed tradeoffs (time, risk, benefit), presented data showing rewrite would delay 3 months with minimal gain, proposed incremental improvement instead. Result - team initially disappointed but accepted data-driven decision. Incremental approach shipped in 2 weeks, no issues. Team later thanked me.",
        "options": [],
        "solution": {
            "code": "# Unpopular decision framework\n1. Gather data and analyze tradeoffs\n2. Consider stakeholder perspectives\n3. Communicate decision with rationale\n4. Show empathy for disappointment\n5. Provide alternative path forward\n6. Follow through and prove outcome",
            "explanation": "Unpopular decisions test leadership and communication. Show you made hard calls with data, not ego. Show empathy for disappointed stakeholders. Prove the decision was right with outcomes."
        },
        "testcases": [
            {
                "input": "I just told them to deal with it",
                "expected": "Weak - no empathy or rationale"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows data-driven decision with empathy and proof",
                "expected": "Strong - demonstrates leadership"
            }
        ],
        "hints": [
            "Use data, not authority",
            "Show empathy for disappointment",
            "Prove decision with outcomes"
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
        "id": "int-114",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "idempotency",
        "difficulty": "hard",
        "question": "What is idempotency and why is it important in distributed systems? Give examples.",
        "correct_answer": "Idempotency: operation that produces same result when executed multiple times. Important in distributed systems because: 1. Network failures cause retries. 2. Duplicate messages in queues. 3. Users double-clicking buttons. Without idempotency: duplicate charges, double sends, inconsistent state. Examples: PUT is idempotent (same result), POST is not. Idempotency keys for payments. Database unique constraints. Distributed locks. Implementation: idempotency tokens, database constraints, check-before-act.",
        "options": [],
        "solution": {
            "code": "# Idempotent payment processing\n@app.route('/charge', methods=['POST'])\ndef charge():\n    idempotency_key = request.headers.get('Idempotency-Key')\n    \n    # Check if already processed\n    existing = db.find_payment(idempotency_key)\n    if existing:\n        return jsonify(existing)\n    \n    # Process payment\n    result = process_payment(request.json)\n    \n    # Store with idempotency key\n    db.save_payment(idempotency_key, result)\n    \n    return jsonify(result)\n\n# Idempotent database operation\nUPDATE users SET balance = balance - 100 WHERE id = 1;\n-- Running twice: first -100, second -0 (no change)",
            "explanation": "Idempotency is critical for reliability. Retries are inevitable in distributed systems. Design APIs so clients can safely retry. Idempotency keys prevent duplicate operations. Database constraints enforce uniqueness."
        },
        "testcases": [
            {
                "input": "POST requests are naturally idempotent",
                "expected": "Wrong - POST is not idempotent by default"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains idempotency with payment example and retry safety",
                "expected": "Strong - understands distributed systems"
            }
        ],
        "hints": [
            "Same result on multiple executions",
            "Critical for safe retries",
            "Use idempotency keys for operations"
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
        "id": "int-115",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "international_experience",
        "difficulty": "easy",
        "question": "Do you have experience working with international teams? How do you handle time zone differences?",
        "correct_answer": "Show adaptability: 'Yes, I've worked with teams across US, Europe, and Asia. I handle time zones by: 1. Setting clear async communication norms. 2. Rotating meeting times fairly. 3. Documenting decisions for those who can't attend. 4. Using tools like Slack, Notion, and shared calendars. 5. Being proactive about updates. I focus on outcomes, not hours logged.' If no experience: 'I'm adaptable and have experience with remote collaboration. I'm confident I can handle time zone differences with clear communication.'",
        "options": [],
        "solution": {
            "code": "# Remote collaboration best practices\n1. Async-first communication\n   - Write clear docs\n   - Use threaded discussions\n   - Record important meetings\n\n2. Meeting hygiene\n   - Rotate times fairly\n   - Always have agenda\n   - Record and share\n\n3. Overlap hours\n   - Identify 2-3 hour window where all zones overlap\n   - Use for synchronous meetings\n   - Rest is async",
            "explanation": "Global teams are common. Show you're adaptable and proactive. Focus on outcomes, not presence. Document everything. Be considerate of others' time zones."
        },
        "testcases": [
            {
                "input": "I need everyone to be online at my time zone",
                "expected": "Weak - shows lack of adaptability"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows async-first and fair meeting practices",
                "expected": "Strong - global collaboration skills"
            }
        ],
        "hints": [
            "Async-first communication",
            "Rotate meeting times fairly",
            "Document decisions"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 15,
        "estimated_time": "10-15 minutes"
    },
    {
        "id": "int-116",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "database_scaling",
        "difficulty": "hard",
        "question": "How would you scale a database that's reaching its limits? Explain read replicas, sharding, and when to use each.",
        "correct_answer": "Scale strategies: 1. Vertical scaling: bigger server. Quick fix but expensive, single point of failure. 2. Read replicas: copies of primary for reads. Use when: read-heavy workload (80%+ reads). Pros: simple, scales reads. Cons: replication lag, eventual consistency. 3. Sharding: split data across multiple databases. Use when: write-heavy, data too large for single server, geographic distribution. Challenges: cross-shard queries, rebalancing, complex joins. 4. Caching: Redis/Memcached for hot data. 5. Connection pooling. Typical progression: optimize queries -> add cache -> read replicas -> sharding.",
        "options": [],
        "solution": {
            "code": "# Scaling progression\n1. Optimize\n   - Add indexes\n   - Fix N+1 queries\n   - Connection pooling\n\n2. Cache\n   - Redis for hot data\n   - Application cache\n\n3. Read replicas\n   - Primary for writes\n   - N replicas for reads\n   - Replication lag: seconds\n\n4. Sharding\n   - Split by user_id, region, etc.\n   - Each shard is independent\n   - Cross-shard queries are hard",
            "explanation": "Database scaling is layered. Start with optimization before adding infrastructure. Read replicas are easiest but don't help writes. Sharding is last resort - adds massive complexity. Cache aggressively."
        },
        "testcases": [
            {
                "input": "Start with sharding when database is slow",
                "expected": "Wrong - optimize and cache first"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows progression from optimization to sharding",
                "expected": "Strong - understands database scaling"
            }
        ],
        "hints": [
            "Optimize before scaling",
            "Read replicas for read-heavy workloads",
            "Sharding as last resort"
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
        "id": "int-117",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "autoscaling",
        "difficulty": "medium",
        "question": "What is auto-scaling? How would you design an auto-scaling policy for a web application?",
        "correct_answer": "Auto-scaling: automatically adjust server count based on load. Metrics: CPU utilization (>70% scale out, <30% scale in), request rate, queue depth, response time. Policy: 1. Define min/max instances. 2. Scale out when metric exceeds threshold for N minutes. 3. Scale in when metric below threshold for M minutes. 4. Cooldown period to prevent flapping. 5. Predictive scaling based on historical patterns. Challenges: cold start latency, stateful services, scaling too fast/slow. Cloud: AWS Auto Scaling, GCP Instance Groups.",
        "options": [],
        "solution": {
            "code": "# Auto-scaling policy\nmin_instances = 2\nmax_instances = 20\ntarget_cpu = 70%\nscale_out_cooldown = 300  # 5 minutes\nscale_in_cooldown = 600   # 10 minutes\n\n# Scale out if:\n# - CPU > 70% for 2 minutes\n# - AND current < max\n# - AND cooldown expired\n\n# Scale in if:\n# - CPU < 30% for 5 minutes\n# - AND current > min\n# - AND cooldown expired",
            "explanation": "Auto-scaling balances cost and performance. Scale out before users notice slowdown. Scale in gradually to avoid thrashing. Consider cold starts - keep warm pool for predictable traffic."
        },
        "testcases": [
            {
                "input": "Auto-scaling reacts instantly to traffic spikes",
                "expected": "Wrong - needs cooldown and thresholds to prevent flapping"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows thresholds, cooldowns, and stateful considerations",
                "expected": "Strong - understands auto-scaling"
            }
        ],
        "hints": [
            "Use metrics like CPU or request rate",
            "Cooldown periods prevent flapping",
            "Consider cold start latency"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer", "devops-engineer"],
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
