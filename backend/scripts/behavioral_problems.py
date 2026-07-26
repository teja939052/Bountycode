"""
Behavioral Interview Problems with STAR Method Framework.
50+ questions covering leadership, teamwork, conflict, and growth.
"""

BEHAVIORAL_PROBLEMS = [
    # ═══════════════════════════════════════════════════════════════════════════
    # LEADERSHIP & INITIATIVE (15 problems)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-001", "title": "Tell me about a time you led a team through a difficult project",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": {
            "situation": "Describe the project and its challenges",
            "task": "What was your specific role and responsibility?",
            "action": "What specific steps did you take to lead the team?",
            "result": "What was the outcome? Quantify if possible."
        },
        "tips": [
            "Focus on YOUR actions, not the team's",
            "Show decision-making process",
            "Quantify results (time saved, money earned, etc.)",
            "Mention what you learned"
        ],
        "red_flags": ["Taking all credit", "Blaming team members", "No measurable outcome"],
        "example_answer": "In my final year project, our team of 4 was building a real-time chat application. Midway, two members had conflicting schedules. I reorganized tasks, created a shared kanban board, and held daily 15-minute standups. We delivered on time with 95% test coverage.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-002", "title": "Describe a situation where you took initiative without being asked",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": {
            "situation": "What was the context?",
            "task": "What problem did you identify?",
            "action": "What did you do proactively?",
            "result": "What impact did your initiative have?"
        },
        "tips": [
            "Show you can identify problems independently",
            "Demonstrate ownership mentality",
            "Show the positive impact of your initiative"
        ],
        "red_flags": ["Waiting for permission", "Small impact", "No follow-through"],
        "example_answer": "I noticed our deployment process was manual and error-prone. Without being asked, I created a CI/CD pipeline using GitHub Actions that reduced deployment time from 2 hours to 5 minutes and eliminated human errors.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-003", "title": "Tell me about a time you had to make a decision without complete information",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Meta"],
        "star_framework": {
            "situation": "What was the incomplete information?",
            "task": "What decision did you need to make?",
            "action": "How did you gather what you could and decide?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show analytical thinking under uncertainty",
            "Explain your risk assessment process",
            "Demonstrate ability to course-correct"
        ],
        "red_flags": ["Rushing without thinking", "Ignoring available data", "No backup plan"],
        "example_answer": "During a production outage, I had to decide between two approaches without full root cause analysis. I chose the safer rollback approach, then investigated the root cause. This minimized downtime to 5 minutes instead of potential 30 minutes.",
        "difficulty_level": "hard",
    },
    {
        "id": "BH-004", "title": "Describe a time you had to influence others without direct authority",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": {
            "situation": "What was the context?",
            "task": "What did you need to accomplish?",
            "action": "How did you influence without authority?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show persuasion skills",
            "Demonstrate empathy and understanding",
            "Show how you built consensus"
        ],
        "red_flags": ["Using threats", "Going over people's heads", "No relationship building"],
        "example_answer": "I convinced the backend team to adopt our new API standard by creating a demo showing 40% performance improvement, then presenting at the team meeting. No authority, just data and persuasion.",
        "difficulty_level": "hard",
    },
    {
        "id": "BH-005", "title": "Tell me about a time you failed and what you learned",
        "category": "behavioral",
        "sub_category": "Growth",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta", "Apple"],
        "star_framework": {
            "situation": "What was the failure?",
            "task": "What were you trying to achieve?",
            "action": "What went wrong and why?",
            "result": "What did you learn and how did you apply it?"
        },
        "tips": [
            "Be honest about the failure",
            "Focus on LEARNING, not the failure itself",
            "Show how you applied the lesson"
        ],
        "red_flags": ["Blaming others", "No self-reflection", "Same mistake repeated"],
        "example_answer": "I once deployed a feature without proper testing, causing a 2-hour outage. I learned to always create staging environments and write integration tests. Since then, I've maintained a 99.9% deployment success rate.",
        "difficulty_level": "medium",
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # TEAMWORK & COLLABORATION (15 problems)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-010", "title": "Describe a time you worked with a difficult team member",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": {
            "situation": "What made the team member difficult?",
            "task": "What was your goal?",
            "action": "How did you handle the situation?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Stay professional and positive",
            "Focus on the work, not personal issues",
            "Show empathy and communication skills"
        ],
        "red_flags": ["Badmouthing the person", "Escalating immediately", "Giving up"],
        "example_answer": "A teammate consistently missed deadlines. Instead of complaining, I had a private conversation, learned they were struggling with the tech stack, and offered to pair-program. Their productivity improved 50% and we became good collaborators.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-011", "title": "Tell me about a time you had to collaborate with a cross-functional team",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": {
            "situation": "What teams were involved?",
            "task": "What was the shared goal?",
            "action": "How did you coordinate across teams?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show communication across boundaries",
            "Demonstrate understanding of different perspectives",
            "Show how you aligned different priorities"
        ],
        "red_flags": ["Working in silos", "Ignoring other teams' needs", "No coordination"],
        "example_answer": "I worked with design, backend, and QA teams to launch a new feature. I created a shared specification doc, held weekly syncs, and ensured everyone was aligned. We launched 1 week ahead of schedule.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-012", "title": "Describe a time you received critical feedback",
        "category": "behavioral",
        "sub_category": "Growth",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": {
            "situation": "What was the feedback?",
            "task": "How did it affect you?",
            "action": "What did you do with the feedback?",
            "result": "How did you improve?"
        },
        "tips": [
            "Show openness to feedback",
            "Demonstrate specific improvements",
            "Show growth mindset"
        ],
        "red_flags": ["Defensive reaction", "Ignoring feedback", "No visible improvement"],
        "example_answer": "My manager told my code reviews were too harsh. I started framing feedback as suggestions, asked more questions, and now my reviews are appreciated. My team's code quality improved 30%.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-013", "title": "Tell me about a time you disagreed with a decision",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": {
            "situation": "What was the decision?",
            "task": "Why did you disagree?",
            "action": "How did you express your disagreement?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show respectful disagreement",
            "Demonstrate data-driven reasoning",
            "Show you can disagree and commit"
        ],
        "red_flags": ["Being insubordinate", "Not providing alternatives", "No resolution"],
        "example_answer": "I disagreed with using MongoDB for a relational data model. I presented a comparison showing 3x slower joins. The team reconsidered and we chose PostgreSQL. The project succeeded with 40% better query performance.",
        "difficulty_level": "hard",
    },
    {
        "id": "BH-014", "title": "Describe a time you helped a team member grow",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": {
            "situation": "What was the team member's challenge?",
            "task": "What was your role?",
            "action": "How did you help them grow?",
            "result": "What was the outcome for them?"
        },
        "tips": [
            "Show mentoring ability",
            "Demonstrate patience and empathy",
            "Focus on their growth, not your glory"
        ],
        "red_flags": ["Taking credit for their work", "Doing the work for them", "No follow-up"],
        "example_answer": "A junior developer struggled with system design. I created a weekly study plan, pair-programmed on real features, and reviewed their design docs. Within 3 months, they led their first design review successfully.",
        "difficulty_level": "medium",
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # PROBLEM SOLVING & CONFLICT (10 problems)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-020", "title": "Tell me about a time you solved a complex technical problem",
        "category": "behavioral",
        "sub_category": "Problem Solving",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": {
            "situation": "What was the technical challenge?",
            "task": "What was your goal?",
            "action": "What was your approach to solving it?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show your problem-solving process",
            "Explain technical decisions clearly",
            "Quantify the impact"
        ],
        "red_flags": ["No technical depth", "Taking too long to explain", "No measurable result"],
        "example_answer": "Our API response time was 5 seconds (P99). I identified N+1 queries as the bottleneck, implemented DataLoader pattern for batching, and reduced response time to 200ms (96% improvement).",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-021", "title": "Describe a time you had to resolve a conflict between team members",
        "category": "behavioral",
        "sub_category": "Conflict",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": {
            "situation": "What was the conflict?",
            "task": "What was your role?",
            "action": "How did you resolve it?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Stay neutral and professional",
            "Focus on facts, not emotions",
            "Find a win-win solution"
        ],
        "red_flags": ["Taking sides", "Ignoring the conflict", "No resolution"],
        "example_answer": "Two senior devs disagreed on architecture. I facilitated a meeting where each presented their approach with benchmarks. We combined the best of both, resulting in a solution that met all requirements.",
        "difficulty_level": "hard",
    },
    {
        "id": "BH-022", "title": "Tell me about a time you worked under extreme pressure",
        "category": "behavioral",
        "sub_category": "Problem Solving",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": {
            "situation": "What was the pressure?",
            "task": "What did you need to deliver?",
            "action": "How did you handle the pressure?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show calm under pressure",
            "Demonstrate prioritization skills",
            "Show you can still deliver quality"
        ],
        "red_flags": ["Panic", "Sacrificing quality", "No support from team"],
        "example_answer": "We had a critical production bug affecting 10K users. I stayed calm, identified the root cause in 30 minutes, implemented a fix, and deployed within 2 hours. Zero data loss, full recovery.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-023", "title": "Describe a time you had to make a trade-off between quality and speed",
        "category": "behavioral",
        "sub_category": "Problem Solving",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": {
            "situation": "What was the trade-off?",
            "task": "What were the constraints?",
            "action": "How did you decide?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show strategic thinking",
            "Explain your decision-making process",
            "Show you can balance competing priorities"
        ],
        "red_flags": ["Always choosing speed", "No consideration of consequences", "No follow-up"],
        "example_answer": "For a hackathon, we had 48 hours. I chose to implement core features with basic tests rather than full test coverage. We won first place, then added comprehensive tests in the following sprint.",
        "difficulty_level": "medium",
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # AMAZON LEADERSHIP PRINCIPLES (10 problems)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-030", "title": "Customer Obsession: Tell me about a time you went above and beyond for a customer",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": {
            "situation": "Who was the customer?",
            "task": "What did they need?",
            "action": "How did you go above and beyond?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Focus on customer needs, not company needs",
            "Show empathy and understanding",
            "Quantify the impact on customer satisfaction"
        ],
        "red_flags": ["No customer focus", "Only meeting minimum requirements", "No follow-up"],
        "example_answer": "A client needed a feature urgently for a product launch. I worked overtime for 3 days to deliver it, even though it wasn't in our sprint. They launched on time and renewed their contract.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-031", "title": "Ownership: Tell me about a time you took ownership of something outside your job description",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": {
            "situation": "What was outside your role?",
            "task": "Why did you take ownership?",
            "action": "What did you do?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show initiative and responsibility",
            "Demonstrate end-to-end thinking",
            "Show the impact of your ownership"
        ],
        "red_flags": ["Only doing assigned tasks", "No follow-through", "Low impact"],
        "example_answer": "I noticed our onboarding docs were outdated. I took ownership, interviewed 5 new hires, rewrote the docs, and created a video tutorial. New hire ramp-up time decreased from 2 weeks to 3 days.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-032", "title": "Bias for Action: Tell me about a time you made a decision quickly",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": {
            "situation": "What was the time pressure?",
            "task": "What decision did you need to make?",
            "action": "How did you decide quickly?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show calculated risk-taking",
            "Demonstrate you can act without perfect information",
            "Show the benefit of quick action"
        ],
        "red_flags": ["Reckless decisions", "No risk assessment", "Negative outcome"],
        "example_answer": "During a security incident, I blocked the affected IP range within 5 minutes of detection, preventing further attacks. Later analysis confirmed this was the right call.",
        "difficulty_level": "medium",
    },
    {
        "id": "BH-033", "title": "Dive Deep: Tell me about a time you analyzed data to make a decision",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": {
            "situation": "What data did you analyze?",
            "task": "What decision were you making?",
            "action": "How did you analyze the data?",
            "result": "What was the outcome?"
        },
        "tips": [
            "Show analytical skills",
            "Demonstrate data-driven decision making",
            "Show the impact of your analysis"
        ],
        "red_flags": ["No data backing", "Surface-level analysis", "Ignoring contradicting data"],
        "example_answer": "I analyzed 3 months of user behavior data and found that 40% of drop-offs happened during onboarding. I redesigned the flow, reducing drop-offs by 60% and increasing retention by 25%.",
        "difficulty_level": "medium",
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # SITUATIONAL QUESTIONS (10 problems)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-040", "title": "How would you handle a situation where your project deadline is impossible?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "guidance": "Show prioritization, communication, and negotiation skills.",
        "ideal_answer": "I would first assess what's absolutely required vs. nice-to-have. Then I'd communicate with stakeholders, proposing a phased delivery: core features first, enhancements later. I'd also identify if resources can be reallocated or scope reduced.",
        "red_flags": ["Saying you'd just work harder", "No communication plan", "Ignoring the deadline"],
    },
    {
        "id": "BH-041", "title": "How would you handle discovering a critical bug in production?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "guidance": "Show urgency, systematic debugging, and communication.",
        "ideal_answer": "First, assess impact and communicate to stakeholders. Then, gather logs and reproduce. Fix the immediate issue (rollback if needed). Then investigate root cause and implement a permanent fix with tests.",
        "red_flags": ["Panicking", "Blaming others", "No rollback plan"],
    },
    {
        "id": "BH-042", "title": "How would you approach learning a completely new technology stack?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "easy",
        "companies": ["Amazon", "Google", "Microsoft"],
        "guidance": "Show structured learning and practical application.",
        "ideal_answer": "I'd start with official documentation and tutorials, then build a small project to apply concepts. I'd join community forums for questions and read production code from open-source projects. Within 2 weeks, I'd be productive.",
        "red_flags": ["No learning plan", "Only reading, no practice", "Expecting instant mastery"],
    },
    {
        "id": "BH-043", "title": "How would you handle a situation where you disagree with your manager's technical decision?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft"],
        "guidance": "Show respect, data-driven reasoning, and ability to disagree and commit.",
        "ideal_answer": "I'd prepare a data-backed comparison of alternatives. Present it respectfully in a 1-on-1. If the manager still decides differently, I'd commit fully to their decision while documenting my concerns for future reference.",
        "red_flags": ["Going over manager's head", "Passive-aggressive compliance", "No data to support disagreement"],
    },
    {
        "id": "BH-044", "title": "How would you handle a situation where you need to deliver bad news to a client?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "guidance": "Show honesty, empathy, and solution-oriented thinking.",
        "ideal_answer": "I'd be transparent about the situation, explain the impact, and present a mitigation plan. I'd take ownership, apologize if appropriate, and focus on what we can do to fix it.",
        "red_flags": ["Hiding the bad news", "Blaming others", "No mitigation plan"],
    },
]
