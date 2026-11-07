import json

new_questions = [
    {
        "id": "int-037",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "influence",
        "difficulty": "medium",
        "question": "Describe a time you had to convince a team or manager to adopt your idea. How did you persuade them?",
        "correct_answer": "STAR method: Situation - team wanted to rewrite in new framework with high risk. Task - I advocated for incremental refactoring. Action - built POC showing 60% time savings without full rewrite, presented at team review, addressed concerns with data. Result - team agreed, delivered in timeline, no regression.",
        "options": [],
        "solution": {
            "code": "# Influence without authority\n1. Build small proof-of-concept\n2. Quantify benefit vs risk\n3. Address objections proactively\n4. Involve stakeholders early\n5. Make it easy to say yes",
            "explanation": "Influence tests persuasion and analytical communication. Show you used data, not just opinions. Anticipated objections and addressed them. Made the alternative attractive, not just attacked the status quo."
        },
        "testcases": [
            {
                "input": "I told them they were wrong and forced my idea",
                "expected": "Weak - aggressive, no persuasion"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows POC, data-driven persuasion, and addressing concerns",
                "expected": "Strong - demonstrates influence"
            }
        ],
        "hints": [
            "Show data-driven persuasion",
            "Address concerns proactively",
            "Make the alternative attractive"
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
        "id": "int-038",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "change_management",
        "difficulty": "medium",
        "question": "Tell me about a time you had to adapt quickly to a major change at work. How did you handle it?",
        "correct_answer": "STAR method: Situation - company pivoted product direction, 6 months of work deprecated. Task - quickly learn new domain and contribute. Action - immersed in new customer research, paired with domain expert, identified transferable patterns, proposed migration plan. Result - became go-to person for new domain within 2 months, led migration with 0 downtime.",
        "options": [],
        "solution": {
            "code": "# Adaptability\n1. Acknowledge change without complaining\n2. Identify what you already know that transfers\n3. Rapidly learn new domain\n4. Find quick wins to build confidence\n5. Help others adapt",
            "explanation": "Change is constant in tech. Show resilience, learning agility, and positivity. Don't dwell on what was lost - focus on what you can contribute now."
        },
        "testcases": [
            {
                "input": "I complained about the wasted work",
                "expected": "Weak - focuses on past, not future"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows rapid learning, quick wins, and helping others",
                "expected": "Strong - demonstrates adaptability"
            }
        ],
        "hints": [
            "Show resilience and positivity",
            "Focus on how you contributed after change",
            "Mention how you helped others adapt"
        ],
        "companies": ["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-039",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "prioritization",
        "difficulty": "medium",
        "question": "How do you prioritize work when you have multiple competing deadlines? Walk me through your framework.",
        "correct_answer": "Framework: 1. List all tasks with deadlines and impact. 2. Use Eisenhower Matrix: urgent-important first. 3. Communicate with stakeholders if deadlines are unrealistic. 4. Break large tasks into smaller deliverables. 5. Time-box work and track progress. Example: production bug (urgent-important) first, then feature deadline (important-not urgent), then refactoring (not urgent).",
        "options": [],
        "solution": {
            "code": "# Prioritization framework\n1. Impact vs Effort matrix\n2. Eisenhower Matrix (urgent/important)\n3. MoSCoW method (Must/Should/Could/Wont)\n4. Communicate tradeoffs to stakeholders\n5. Protect deep work time",
            "explanation": "Prioritization tests executive function and communication. Show you have a system, not just 'I work hard'. Mention stakeholder communication - sometimes deadlines are negotiable."
        },
        "testcases": [
            {
                "input": "I just work harder and longer hours",
                "expected": "Weak - no system, unsustainable"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows structured framework and stakeholder communication",
                "expected": "Strong - demonstrates executive function"
            }
        ],
        "hints": [
            "Use a proven framework (Eisenhower, MoSCoW)",
            "Mention stakeholder communication",
            "Show you protect important work"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "product-manager"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-040",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "testing",
        "difficulty": "medium",
        "question": "Explain different types of testing. When would you use unit tests vs integration tests vs E2E tests?",
        "correct_answer": "Unit tests: test individual functions/methods in isolation. Fast, cheap, many. Use for: business logic, edge cases. Integration tests: test how components work together. Medium speed, medium cost. Use for: API contracts, DB interactions, service boundaries. E2E tests: test full user flows. Slow, expensive, few. Use for: critical user journeys. Pyramid: many unit, fewer integration, few E2E.",
        "options": [],
        "solution": {
            "code": "# Testing pyramid\n# Many unit tests (fast, isolated)\ndef test_add():\n    assert add(1, 2) == 3\n\n# Fewer integration tests (with DB)\ndef test_user_api():\n    response = client.post('/users', json={'name': 'A'})\n    assert response.status == 201\n\n# Few E2E tests (full stack)\ndef test_checkout_flow():\n    login()\n    add_to_cart()\n    checkout()\n    assert 'Thank you' in page",
            "explanation": "Testing is about confidence and speed. Unit tests catch bugs fast. Integration tests catch contract breaks. E2E tests catch real user issues. Too many E2E tests = slow feedback, brittle suites."
        },
        "testcases": [
            {
                "input": "I only write E2E tests because they test everything",
                "expected": "Wrong - slow, brittle, poor feedback"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains pyramid and when to use each type",
                "expected": "Strong - understands testing strategy"
            }
        ],
        "hints": [
            "Unit: fast, isolated, many",
            "Integration: component interaction",
            "E2E: full user flow, slow, few"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "qa-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-041",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "ci_cd",
        "difficulty": "medium",
        "question": "What is CI/CD? Explain the typical stages in a CI/CD pipeline.",
        "correct_answer": "CI (Continuous Integration): developers merge code frequently, each merge triggers automated build and test. CD (Continuous Delivery/Deployment): automatically deploy passing builds to production. Typical stages: 1. Source: code commit triggers pipeline. 2. Build: compile, lint, dependency check. 3. Test: unit, integration, security scan. 4. Deploy to staging. 5. Approval gate. 6. Deploy to production (canary/blue-green). 7. Monitor and rollback if needed.",
        "options": [],
        "solution": {
            "code": "# GitHub Actions example\nname: CI/CD\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - run: npm install\n      - run: npm test\n      - run: npm run lint\n      - run: docker build .",
            "explanation": "CI/CD automates the path from code to production. Benefits: faster releases, fewer manual errors, consistent deployments. Tools: GitHub Actions, Jenkins, GitLab CI, CircleCI."
        },
        "testcases": [
            {
                "input": "CI/CD means you deploy every commit automatically to production",
                "expected": "Partial - that's continuous deployment, not all CI/CD"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains CI vs CD and typical pipeline stages",
                "expected": "Strong - understands DevOps fundamentals"
            }
        ],
        "hints": [
            "CI = merge frequently, test automatically",
            "CD = deploy automatically or with one click",
            "Typical stages: build, test, deploy"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "devops-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-042",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "devops",
        "difficulty": "medium",
        "question": "What is Docker and how is it different from a virtual machine?",
        "correct_answer": "Docker: containerization platform that packages apps with dependencies. Containers share host OS kernel, are lightweight (MBs), start in seconds. VMs: full guest OS, heavier (GBs), start in minutes. Docker uses namespaces and cgroups for isolation. Use Docker for: microservices, consistent dev/prod environments, quick scaling. Use VMs for: complete OS isolation, different OS kernels, legacy apps.",
        "options": [],
        "solution": {
            "code": "# Dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ['python', 'app.py']\n\n# Run\n# docker build -t myapp .\n# docker run -p 8000:8000 myapp",
            "explanation": "Containers virtualize the OS, VMs virtualize the hardware. Containers are lighter and faster because they share the kernel. Docker adds image management, networking, and volume management on top of Linux containers."
        },
        "testcases": [
            {
                "input": "Docker is just a lightweight VM",
                "expected": "Wrong - containers share kernel, VMs don't"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains kernel sharing vs full OS isolation",
                "expected": "Strong - understands containerization"
            }
        ],
        "hints": [
            "Containers share host OS kernel",
            "VMs have full guest OS",
            "Docker = containers with tooling"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "devops-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-043",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "situational",
        "difficulty": "medium",
        "question": "You notice a teammate consistently missing deadlines and it's affecting the team. What do you do?",
        "correct_answer": "Approach: 1. Understand first: talk privately, ask if they're blocked or overwhelmed. 2. Offer help: pair program, break down tasks, remove blockers. 3. Communicate to manager only if needed: frame as team risk, not complaint. 4. Adjust plan: re-scope if necessary. Never: gossip, blame publicly, or assume laziness. Example: teammate was struggling with new tech - I paired with them, we shared learning, deadlines met.",
        "options": [],
        "solution": {
            "code": "# Good approach\n1. Private conversation first\n2. Ask questions, don't accuse\n3. Offer concrete help\n4. Involve manager only if team is at risk\n5. Focus on team success, not blame",
            "explanation": "Situational questions test emotional intelligence and teamwork. Show empathy first, then action. Don't escalate immediately - assume good intent. Frame issues as team risks, not individual failures."
        },
        "testcases": [
            {
                "input": "I report them to the manager immediately",
                "expected": "Weak - skips empathy and direct conversation"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows private conversation, empathy, and team-first framing",
                "expected": "Strong - demonstrates emotional intelligence"
            }
        ],
        "hints": [
            "Talk privately first",
            "Assume positive intent",
            "Frame as team risk, not blame"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-044",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "expectations",
        "difficulty": "easy",
        "question": "What are your salary expectations?",
        "correct_answer": "Research-based range: 'Based on my research for similar roles in this market, I'm looking at 15-25 LPA for this level. I'm flexible based on the total package, including learning opportunities and growth.' For experienced: '$120k-150k base, depending on equity and benefits'. Show you researched, give a range, express flexibility. Avoid: 'whatever you offer' or a single number.",
        "options": [],
        "solution": {
            "code": "# Research first\n- Glassdoor, Levels.fyi, Payscale for market data\n- Consider: base, bonus, equity, benefits\n- Give a range, not a single number\n- Leave room for negotiation\n- Express enthusiasm for the role",
            "explanation": "Salary questions test preparation and self-worth. Research market rates. Give a range based on research, not arbitrary number. Show flexibility - total package matters more than base."
        },
        "testcases": [
            {
                "input": "I don't care, just give me whatever",
                "expected": "Weak - shows no research or self-worth"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Gives researched range with flexibility",
                "expected": "Strong - prepared and professional"
            }
        ],
        "hints": [
            "Research market rates beforehand",
            "Give a range, not single number",
            "Consider total package, not just base"
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
        "id": "int-045",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "cloud",
        "difficulty": "medium",
        "question": "What is the difference between IaaS, PaaS, and SaaS? Give examples of each.",
        "correct_answer": "IaaS (Infrastructure as a Service): rent VMs, storage, networks. You manage OS and above. Examples: AWS EC2, GCP Compute Engine. PaaS (Platform as a Service): platform to deploy apps. You manage code only. Examples: Heroku, AWS Elastic Beanstalk, Google App Engine. SaaS (Software as a Service): complete software product. You just use it. Examples: Gmail, Salesforce, Slack. Trend: IaaS gives most control, SaaS gives least.",
        "options": [],
        "solution": {
            "code": "# Cloud service models\nIaaS: raw infrastructure\n  You manage: OS, runtime, data, app\n  Provider manages: virtualization, networking, storage\n  Example: AWS EC2\n\nPaaS: deployment platform\n  You manage: app, data\n  Provider manages: OS, runtime, scaling\n  Example: Heroku\n\nSaaS: complete product\n  You manage: nothing (just use it)\n  Provider manages: everything\n  Example: Gmail",
            "explanation": "Cloud models trade control for convenience. IaaS is most flexible, SaaS is easiest. Most companies use mix: IaaS for custom workloads, PaaS for rapid deployment, SaaS for productivity."
        },
        "testcases": [
            {
                "input": "IaaS means you manage everything",
                "expected": "Wrong - provider manages physical infrastructure"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains responsibility split with examples",
                "expected": "Strong - understands cloud models"
            }
        ],
        "hints": [
            "IaaS: virtual machines, you manage OS",
            "PaaS: deploy code, they manage platform",
            "SaaS: complete product, you just use it"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "cloud-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-046",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "stress_management",
        "difficulty": "medium",
        "question": "Describe a time you had to handle a high-pressure situation with a tight deadline. How did you manage it?",
        "correct_answer": "STAR method: Situation - production outage 2 hours before release. Task - fix without delaying launch. Action - triaged issue, found root cause in 20 mins, implemented hotfix, ran regression tests, communicated status to stakeholders every 30 mins. Result - launched on time, postmortem revealed caching bug, added monitoring to prevent recurrence.",
        "options": [],
        "solution": {
            "code": "# High-pressure handling\n1. Stay calm - panic wastes time\n2. Triage: what's blocking vs nice-to-have\n3. Communicate status proactively\n4. Focus on solution, not blame\n5. Document for postmortem",
            "explanation": "Pressure situations test composure and process. Show you don't panic, you triage, you communicate, and you prevent recurrence. Don't just say 'I worked late' - show systematic approach."
        },
        "testcases": [
            {
                "input": "I just worked all night and pushed through",
                "expected": "Partial - shows effort but not process"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows triage, communication, and prevention",
                "expected": "Strong - handles pressure systematically"
            }
        ],
        "hints": [
            "Show systematic triage, not just hard work",
            "Communicate status proactively",
            "Focus on prevention after"
        ],
        "companies": ["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-047",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "ethical_decision",
        "difficulty": "hard",
        "question": "Describe a time you faced an ethical dilemma at work. How did you handle it?",
        "correct_answer": "STAR method: Situation - discovered colleague cutting corners on security to meet deadline. Task - ensure product security without derailing launch. Action - spoke to colleague privately, showed risk, proposed 2-day security sprint before launch, presented to manager with solution. Result - security review passed, colleague thanked me, team adopted mandatory security checklist.",
        "options": [],
        "solution": {
            "code": "# Ethical decision framework\n1. Identify the issue clearly\n2. Assess impact and stakeholders\n3. Talk directly to person first if safe\n4. Propose solution, not just problem\n5. Escalate only if necessary\n6. Document decision",
            "explanation": "Ethics questions test integrity and courage. Show you did the right thing even when hard. Don't just report anonymously - show you tried to resolve directly first. Frame as protecting team/customer, not getting someone in trouble."
        },
        "testcases": [
            {
                "input": "I ignored it because it wasn't my job",
                "expected": "Weak - lacks integrity and ownership"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows direct conversation, solution proposal, and team protection",
                "expected": "Strong - demonstrates ethical courage"
            }
        ],
        "hints": [
            "Show courage to do the right thing",
            "Try direct resolution first",
            "Frame as protecting team/customer"
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
        "id": "int-048",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "agile",
        "difficulty": "easy",
        "question": "What is Agile? Explain Scrum roles, ceremonies, and artifacts.",
        "correct_answer": "Agile: iterative development with customer feedback. Scrum framework: Roles - Product Owner (prioritizes backlog), Scrum Master (removes blockers), Dev Team (builds). Ceremonies - Sprint Planning (what to build), Daily Standup (sync), Sprint Review (demo), Sprint Retrospective (improve). Artifacts - Product Backlog (all work), Sprint Backlog (this sprint), Increment (shippable product). Sprint length: 2-4 weeks typically.",
        "options": [],
        "solution": {
            "code": "# Scrum in practice\nSprint Planning (2 hours for 2-week sprint):\n  - PO presents prioritized backlog\n  - Team selects work for sprint\n  - Define sprint goal\n\nDaily Standup (15 mins):\n  - What did yesterday?\n  - What will today?\n  - Any blockers?\n\nSprint Review (1 hour):\n  - Demo working software\n  - Get feedback\n\nRetrospective (45 mins):\n  - What went well?\n  - What to improve?\n  - Action items",
            "explanation": "Agile is a mindset, Scrum is a framework. Key: inspect and adapt, working software over documentation, customer collaboration. Common mistake: calling meetings Agile without delivering working software frequently."
        },
        "testcases": [
            {
                "input": "Agile means you don't need documentation or planning",
                "expected": "Wrong - Agile values working software but still needs docs"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains iterative delivery, ceremonies, and roles",
                "expected": "Strong - understands Agile/Scrum"
            }
        ],
        "hints": [
            "Agile = iterative, customer-focused",
            "Scrum has 3 roles, 4 ceremonies, 3 artifacts",
            "Sprint is time-boxed iteration"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "product-manager", "scrum-master"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-049",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "git",
        "difficulty": "easy",
        "question": "What is the difference between git merge and git rebase? When would you use each?",
        "correct_answer": "Git merge: creates a new merge commit that combines two branches. Preserves full history, non-destructive. Use for: public/shared branches. Git rebase: moves branch to start from latest commit of base, rewriting history. Linear history, cleaner. Use for: private feature branches before PR. Never rebase public/shared branches. Merge is safer, rebase is cleaner.",
        "options": [],
        "solution": {
            "code": "# Merge\ngit checkout main\ngit merge feature-branch\n# Creates merge commit\n\n# Rebase\ngit checkout feature-branch\ngit rebase main\n# Rewrites feature-branch on top of main",
            "explanation": "Both integrate branches. Merge preserves history with merge commits. Rebase rewrites history for linear log. Golden rule: never rebase commits that exist outside your repo."
        },
        "testcases": [
            {
                "input": "Rebase is always better because it's cleaner",
                "expected": "Wrong - dangerous on shared branches"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains both with safety rules and use cases",
                "expected": "Strong - understands Git workflows"
            }
        ],
        "hints": [
            "Merge: safe, preserves history",
            "Rebase: clean history, rewrite commits",
            "Never rebase public branches"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 15,
        "estimated_time": "10-15 minutes"
    },
    {
        "id": "int-050",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "team_fit",
        "difficulty": "easy",
        "question": "Describe your ideal team and work environment.",
        "correct_answer": "Show self-awareness and research: 'I thrive in small, autonomous teams with clear goals and psychological safety. I like collaborative problem-solving, code review culture, and continuous learning. I appreciate teams that ship often and learn from failures. Based on what I've read about your engineering culture, this seems like a great match.'",
        "options": [],
        "solution": {
            "code": "# Good answer components\n1. Specific traits you value (autonomy, collaboration)\n2. How you contribute to that environment\n3. Connect to company's stated values\n4. Show flexibility - you adapt to good teams",
            "explanation": "Team fit questions test culture alignment. Be specific about what you value, not just 'nice people'. Show you researched the company. Avoid unrealistic demands like 'I want to work alone'."
        },
        "testcases": [
            {
                "input": "I prefer to work alone without interruptions",
                "expected": "Red flag for most team-based roles"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows specific values and research about company",
                "expected": "Strong - culture-aware and prepared"
            }
        ],
        "hints": [
            "Be specific about team traits you value",
            "Connect to company's culture",
            "Show you contribute to that environment"
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
