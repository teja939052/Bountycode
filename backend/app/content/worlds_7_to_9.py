"""Worlds 7-9: Hiring Arena, Company Missions, AI Engineering."""
from __future__ import annotations

from app.content.lesson_definitions import (
    LessonDefinition, LessonStep, TownDefinition, WorldDefinition,
)

# ═══════════════════════════════════════════════════════════════════
# WORLD 7 — HIRING ARENA
# ═══════════════════════════════════════════════════════════════════

CODING_INTERVIEW_TOWN = TownDefinition(
    id="coding_interview", name="Coding Interviews", icon="💻",
    description="The technical round. Solve, explain, optimize.",
    order=1, mental_model="Interviews test communication as much as coding — think aloud, clarify, then code.",
    canonical_skills=["interview.coding"], competencies=["problem_clarification", "thinking_aloud", "testing", "optimization"],
    lessons=[
        LessonDefinition(
            id="coding-1", title="Clarify First", icon="❓", order=1, concept="clarification",
            mental_model="Before coding, clarify: input types, edge cases, constraints. 2 minutes of questions saves 20 minutes of wrong code.",
            canonical_skill="interview.clarification",
            why_this_matters="In real interviews, jumping straight to code without clarifying is the #1 mistake. Interviewers want to see how you handle ambiguity — because real engineering is ambiguous. Clarifying shows maturity.",
            engineering_context="In real sprint planning, engineers ask clarifying questions before estimating: 'What happens if the API is down?' 'What's the expected load?' 'What's the fallback?' This same skill gets you hired.",
            builds_toward="Interview Performance — structured problem solving",
            steps=[
                LessonStep(step_type="discover", title="The Ambiguous Question",
                    content="'Sort this array.' What questions do you ask? Size? Sorted order? Duplicates allowed? Memory constraints?"),
                LessonStep(step_type="retrieve", title="What Do You Ask?",
                    question="Before coding, what should you clarify?",
                    prompt="I'd ask about input size, edge cases, and…", answer="expected output format and constraints"),
            ],
            mastery_evidence=["Ask clarifying questions before coding"],
            unlocks="coding-2",
        ),
        LessonDefinition(
            id="coding-2", title="Think Aloud", icon="🗣️", order=2, concept="thinking_aloud",
            mental_model="Narrate your thinking — interviewers evaluate your process, not just your solution.",
            canonical_skill="interview.thinking_aloud",
            why_this_matters="Interviewers can't read your mind. If you think silently, they assume you're stuck. Narrating your process — even wrong directions — shows how you think, which is what they're evaluating.",
            engineering_context="In pair programming and code reviews, engineers narrate their thinking: 'I'm considering a hash map here because we need O(1) lookups.' This transparency is how teams collaborate.",
            builds_toward="Interview Performance — communication during problem solving",
            steps=[
                LessonStep(step_type="discover", title="Narrate Your Process",
                    content="'I see this is a sorted array, so binary search could work. Let me think about the O(log n) approach...'"),
            ],
            mastery_evidence=["Articulate your problem-solving process"],
            unlocks="coding-3",
        ),
        LessonDefinition(
            id="coding-3", title="Test Your Code", icon="✅", order=3, concept="testing",
            mental_model="After coding, test with: normal case, edge case (empty/single), and large input. Find your own bugs before they do.",
            canonical_skill="interview.testing",
            why_this_matters="Candidates who test their code catch their own bugs. Candidates who don't, fail when the interviewer finds the bug. Testing is the difference between a hire and a no-hire.",
            engineering_context="In production, engineers write tests before merging. In interviews, manually tracing through your code with test cases is the equivalent. It shows you care about correctness.",
            builds_toward="Interview Performance — verifying your solution",
            steps=[
                LessonStep(step_type="build", title="Trace Through Manually",
                    function_name="binary_search", signature="def binary_search(nums: list, target: int) -> int:",
                    description="Implement binary search. Return index of target, or -1 if not found.",
                    test_cases=[{"input":[[1,3,5,7,9],5],"expected":2}], hidden_tests=5),
            ],
            mastery_evidence=["Test code with edge cases", "Trace through manually"],
            unlocks="coding-boss",
        ),
        LessonDefinition(
            id="coding-boss", title="Coding Boss", icon="🐉", kind="boss", order=4,
            concept="transfer", mental_model="Full interview simulation: clarify, think aloud, code, test.",
            canonical_skill="interview.coding", xp=100, estimated_minutes=25,
            engineering_context="A real interview gives you 30-45 minutes: 5 min clarification, 20 min coding, 5 min testing. This boss simulates that full cycle under time pressure.",
            builds_toward="Interview Performance — full interview simulation",
            steps=[
                LessonStep(step_type="mastery", title="Merge Two Sorted Lists",
                    function_name="merge_sorted", signature="def merge_sorted(a: list, b: list) -> list:",
                    description="Merge two sorted lists into one sorted list. O(n+m) time.",
                    test_cases=[{"input":[[1,3,5],[2,4,6]],"expected":[1,2,3,4,5,6]}], hidden_tests=5),
            ],
            mastery_evidence=["Clarify requirements", "Think aloud", "Implement correctly", "Test thoroughly"],
        ),
    ],
)

SYSTEM_DESIGN_TOWN = TownDefinition(
    id="system_design", name="System Design", icon="🏛️",
    description="Design systems that scale. The senior engineer's skill.",
    order=2, mental_model="System design = requirements → estimate → data model → API → scaling.",
    canonical_skills=["interview.system_design"], competencies=["requirements", "estimation", "data_modeling", "scaling", "tradeoffs"],
    lessons=[
        LessonDefinition(
            id="sd-1", title="Requirements First", icon="📋", order=1, concept="requirements",
            mental_model="Before designing, pin down: functional requirements (what it does) and non-functional (scale, latency, reliability).",
            canonical_skill="sd.requirements",
            why_this_matters="System design interviews test whether you can handle ambiguity. Real systems start with unclear requirements. The engineer who asks 'how many users?' and 'what's the read/write ratio?' stands out.",
            engineering_context="In real system design (designing a URL shortener, a chat system), requirements drive every decision. 100 users vs 10 million users means completely different architectures.",
            builds_toward="System Design Interviews — structured design process",
            steps=[
                LessonStep(step_type="discover", title="Ask the Right Questions",
                    content="Design Twitter. Questions: How many users? Read-heavy or write-heavy? What features? Timeline?"),
                LessonStep(step_type="retrieve", title="Non-Functional Requirements",
                    question="What are non-functional requirements?",
                    prompt="Non-functional requirements describe…", answer="scale, latency, reliability, availability"),
            ],
            mastery_evidence=["Identify functional and non-functional requirements"],
            unlocks="sd-2",
        ),
        LessonDefinition(
            id="sd-2", title="Back-of-Envelope", icon="🧮", order=2, concept="estimation",
            mental_model="Estimate storage, bandwidth, and QPS to guide architecture decisions. Rough numbers prevent wrong designs.",
            canonical_skill="sd.estimation",
            why_this_matters="Estimation tells you whether a single server suffices or you need distributed systems. Without estimates, you're guessing. With them, you're engineering.",
            engineering_context="In capacity planning, engineers estimate: '1M users × 10 requests/day = 10M requests/day = ~116 QPS.' These numbers determine server count, database choice, and caching strategy.",
            builds_toward="System Design Interviews — capacity planning",
            steps=[
                LessonStep(step_type="discover", title="Estimate Storage",
                    content="100M users, 100 tweets/user, 280 chars/tweet. Storage = 100M × 100 × 280 = 2.8 TB."),
            ],
            mastery_evidence=["Estimate storage and QPS for system design"],
            unlocks="sd-3",
        ),
        LessonDefinition(
            id="sd-3", title="Trade-offs", icon="⚖️", order=3, concept="tradeoffs",
            mental_model="Every design choice has trade-offs: SQL vs NoSQL, consistency vs availability, latency vs throughput. Name them.",
            canonical_skill="sd.tradeoffs",
            why_this_matters="Senior engineers don't just pick solutions — they explain trade-offs. 'We use Redis for caching because we accept eventual consistency for faster reads.' That's the senior mindset.",
            engineering_context="In real architecture decisions, engineers document trade-offs: 'We chose PostgreSQL over MongoDB because we need ACID transactions, at the cost of horizontal scaling flexibility.'",
            builds_toward="System Design Interviews — architectural decision making",
            steps=[
                LessonStep(step_type="predict", title="SQL or NoSQL?",
                    question="You need complex transactions and strong consistency. Which database?",
                    options=[{"id":"a","text":"PostgreSQL (SQL)","correct":True},{"id":"b","text":"MongoDB (NoSQL)","correct":False},{"id":"c","text":"Redis (cache)","correct":False}]),
            ],
            mastery_evidence=["Analyze trade-offs in architectural decisions"],
            unlocks="sd-boss",
        ),
        LessonDefinition(
            id="sd-boss", title="System Design Boss", icon="🐉", kind="boss", order=4,
            concept="transfer", mental_model="Full system design: requirements → estimate → design → trade-offs.",
            canonical_skill="sd.system_design", xp=100, estimated_minutes=30,
            engineering_context="In a real system design interview, you'd design a complete system (e.g., a chat service) covering: API design, data model, storage choice, caching, and scaling strategy.",
            builds_toward="System Design Interviews — complete system design",
            steps=[
                LessonStep(step_type="mastery", title="Design a URL Shortener",
                    function_name="design_url_shortener", signature="def design_url_shortener() -> dict:",
                    description="Return design: API endpoints, data model, storage choice, and scaling strategy.",
                    test_cases=[{"input":[],"expected":"design"}], hidden_tests=3),
            ],
            mastery_evidence=["Gather requirements", "Estimate capacity", "Design data model", "Analyze trade-offs"],
        ),
    ],
)

WORLD_7_HIRING_ARENA = WorldDefinition(
    id="hiring_arena", name="Hiring Arena", icon="🏆",
    subtitle="Interviews + System Design + Behavioral",
    description="The final round. Prove you can code, design, and communicate.",
    order=7, theme="hiring_arena", towns=[CODING_INTERVIEW_TOWN, SYSTEM_DESIGN_TOWN],
)


# ═══════════════════════════════════════════════════════════════════
# WORLD 8 — COMPANY MISSIONS
# ═══════════════════════════════════════════════════════════════════

AMAZON_TOWN = TownDefinition(
    id="amazon", name="Amazon", icon="📦",
    description="Leadership principles + bar raiser rounds.",
    order=1, mental_model="Amazon evaluates against 16 Leadership Principles — every answer maps to one.",
    canonical_skills=["company.amazon"], competencies=["leadership_principles", "customer_obsession", "bias_for_action", "bar_raiser"],
    lessons=[
        LessonDefinition(
            id="amz-1", title="Customer Obsession", icon="❤️", order=1, concept="customer_obsession",
            mental_model="Start with the customer and work backward. Every decision: does this help the customer?",
            canonical_skill="company.customer_obsession",
            why_this_matters="Amazon's #1 principle. In interviews, every answer should connect back to customer impact. 'I chose this architecture because it reduces latency for users' — that's customer obsession.",
            engineering_context="In real Amazon teams, engineers write PR FAQs (press release + FAQ) before building: 'What does the customer experience look like?' This customer-first thinking drives product decisions.",
            builds_toward="Company Interviews — Amazon leadership principles",
            steps=[
                LessonStep(step_type="discover", title="Start with the Customer",
                    content="Before building a feature, Amazon writes a press release. What's the customer benefit?"),
                LessonStep(step_type="retrieve", title="Map to a Principle",
                    question="You improved page load time by 50%. Which principle does this demonstrate?",
                    prompt="This demonstrates…", answer="Customer Obsession — faster pages help customers"),
            ],
            mastery_evidence=["Connect engineering decisions to customer impact"],
            unlocks="amz-2",
        ),
        LessonDefinition(
            id="amz-2", title="STAR Method", icon="⭐", order=2, concept="star_method",
            mental_model="Structure behavioral answers: Situation → Task → Action → Result. Every story needs all four.",
            canonical_skill="company.star_method",
            why_this_matters="Behavioral rounds decide hires. The STAR method is the standard format: describe the situation, your task, what you DID, and the measurable result. Without STAR, answers ramble.",
            engineering_context="In real performance reviews and promotion packets, engineers use STAR to describe impact: 'Situation: API was slow. Task: reduce latency. Action: added caching. Result: 80% latency reduction.'",
            builds_toward="Company Interviews — behavioral interview performance",
            steps=[
                LessonStep(step_type="build", title="Tell a STAR Story",
                    function_name="star_story", signature="def star_story() -> dict:",
                    description="Return a STAR story: {situation, task, action, result} for a time you solved a hard problem.",
                    test_cases=[{"input":[],"expected":"STAR"}], hidden_tests=3),
            ],
            mastery_evidence=["Structure behavioral answers with STAR"],
            unlocks="amz-boss",
        ),
        LessonDefinition(
            id="amz-boss", title="Amazon Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Full behavioral + technical round in Amazon style.",
            canonical_skill="company.amazon", xp=100, estimated_minutes=20,
            engineering_context="A real Amazon loop: 1 technical round, 1 system design, 2 behavioral (each mapping to leadership principles). This boss tests whether you can connect technical work to leadership principles.",
            builds_toward="Company Interviews — full Amazon loop simulation",
            steps=[
                LessonStep(step_type="mastery", title="Leadership + Technical",
                    function_name="amazon_answer", signature="def amazon_answer() -> dict:",
                    description="Return: technical solution + which leadership principle it demonstrates + STAR format.",
                    test_cases=[{"input":[],"expected":"answer"}], hidden_tests=3),
            ],
            mastery_evidence=["Apply leadership principles", "Use STAR method", "Connect technical to behavioral"],
        ),
    ],
)

WORLD_8_COMPANY_MISSIONS = WorldDefinition(
    id="company_missions", name="Company Missions", icon="🎯",
    subtitle="Target-Company Preparation",
    description="Prepare for specific companies: Amazon, Google, Microsoft, startups.",
    order=8, theme="company_missions", towns=[AMAZON_TOWN],
)


# ═══════════════════════════════════════════════════════════════════
# WORLD 9 — AI ENGINEERING
# ═══════════════════════════════════════════════════════════════════

LLM_TOWN = TownDefinition(
    id="llm", name="LLMs", icon="🤖",
    description="Large Language Models — the hottest skill in tech.",
    order=1, mental_model="LLMs predict the next token. Your job: prompt them well, ground them in data, evaluate their output.",
    canonical_skills=["ai.llm_engineering"], competencies=["prompting", "rag", "evaluation", "agents", "fine_tuning"],
    lessons=[
        LessonDefinition(
            id="llm-1", title="Prompt Engineering", icon="✍️", order=1, concept="prompting",
            mental_model="A good prompt is specific, gives context, shows examples, and defines the output format.",
            canonical_skill="ai.prompting",
            why_this_matters="Prompt engineering is the fastest-growing engineering skill. Companies pay premiums for engineers who can get reliable output from LLMs. It's the difference between a toy demo and a production AI feature.",
            engineering_context="In production AI features, prompts are engineered with: system instructions, few-shot examples, output format specs, and guardrails. A well-engineered prompt can take accuracy from 60% to 95%.",
            builds_toward="AI Engineering — building reliable AI features",
            steps=[
                LessonStep(step_type="discover", title="Anatomy of a Good Prompt",
                    content="System: 'You are a code reviewer.' Context: 'Review this Python function.' Example: 'Good: clear naming.' Format: 'Return JSON with issues[]'."),
                LessonStep(step_type="build", title="Write a Prompt",
                    function_name="write_prompt", signature="def write_prompt() -> str:",
                    description="Return a prompt that asks an LLM to review code and return JSON with issues and severity.",
                    test_cases=[{"input":[],"expected":"prompt"}], hidden_tests=3),
            ],
            mastery_evidence=["Write effective prompts with context and format"],
            unlocks="llm-2",
        ),
        LessonDefinition(
            id="llm-2", title="RAG", icon="🔍", order=2, concept="rag",
            mental_model="RAG = Retrieve relevant docs → Augment the prompt → Generate grounded answers. No hallucinations.",
            canonical_skill="ai.rag",
            why_this_matters="RAG is how companies deploy LLMs without hallucination. Instead of hoping the LLM knows the answer, you feed it the actual documents. It's the architecture behind every enterprise AI feature.",
            engineering_context="In production, RAG pipelines: chunk documents → embed into vector DB → retrieve top-k relevant chunks → inject into prompt → generate. Companies like Gartner say 80% of enterprise AI uses RAG.",
            builds_toward="AI Engineering — production AI systems",
            steps=[
                LessonStep(step_type="discover", title="The RAG Pipeline",
                    content="Question → Embed → Search vector DB → Retrieve top chunks → Inject into prompt → Generate answer."),
                LessonStep(step_type="retrieve", title="Why RAG?",
                    question="Why use RAG instead of just asking the LLM?",
                    prompt="RAG prevents…", answer="hallucination by grounding answers in real documents"),
            ],
            mastery_evidence=["Explain the RAG pipeline and its purpose"],
            unlocks="llm-3",
        ),
        LessonDefinition(
            id="llm-3", title="Evaluation", icon="📊", order=3, concept="evaluation",
            mental_model="If you can't measure it, you can't improve it. Evaluate AI outputs with automated metrics + human review.",
            canonical_skill="ai.evaluation",
            why_this_matters="AI without evaluation is just hope. Production AI systems need automated evaluation: accuracy, relevance, hallucination rate, latency. Without evals, you don't know if your changes help or hurt.",
            engineering_context="In production AI teams, evals are run on every model/prompt change. A typical eval suite: 100+ test cases, automated scoring, human review of edge cases. Evals are the CI/CD of AI.",
            builds_toward="AI Engineering — reliable AI evaluation",
            steps=[
                LessonStep(step_type="build", title="Build an Eval",
                    function_name="build_eval", signature="def build_eval() -> dict:",
                    description="Return an eval suite: {test_cases: [...], metrics: [accuracy, relevance, latency]}.",
                    test_cases=[{"input":[],"expected":"eval"}], hidden_tests=3),
            ],
            mastery_evidence=["Design evaluation suites for AI systems"],
            unlocks="llm-boss",
        ),
        LessonDefinition(
            id="llm-boss", title="AI Engineering Boss", icon="🐉", kind="boss", order=4,
            concept="transfer", mental_model="Design a complete AI feature: prompt, RAG, evaluation.",
            canonical_skill="ai.llm_engineering", xp=100, estimated_minutes=25,
            engineering_context="In a real AI feature (e.g., 'AI support agent'), you'd design: the system prompt, RAG over company docs, evaluation suite, and guardrails. This boss tests that complete design.",
            builds_toward="AI Engineering — complete AI feature design",
            steps=[
                LessonStep(step_type="mastery", title="Design an AI Agent",
                    function_name="design_ai_agent", signature="def design_ai_agent() -> dict:",
                    description="Return: prompt strategy, RAG architecture, evaluation plan, and guardrails.",
                    test_cases=[{"input":[],"expected":"design"}], hidden_tests=3),
            ],
            mastery_evidence=["Engineer prompts", "Design RAG pipelines", "Build evaluation suites", "Combine into complete AI feature"],
        ),
    ],
)

WORLD_9_AI_ENGINEERING = WorldDefinition(
    id="ai_engineering", name="AI Engineering", icon="🤖",
    subtitle="LLMs + RAG + Agents + Evaluation",
    description="Build production AI systems: prompting, retrieval, evaluation, and agents.",
    order=9, theme="ai_engineering", towns=[LLM_TOWN],
)

def get_world_7() -> WorldDefinition: return WORLD_7_HIRING_ARENA
def get_world_8() -> WorldDefinition: return WORLD_8_COMPANY_MISSIONS
def get_world_9() -> WorldDefinition: return WORLD_9_AI_ENGINEERING

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
