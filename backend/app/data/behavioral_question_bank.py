"""High-Quality Behavioral Interview Question Bank with STAR Framework.

This module contains curated behavioral interview questions following the
STAR (Situation, Task, Action, Result) framework. Each question is designed
to assess specific competency areas that companies commonly evaluate.

Each question includes:
- id: Unique identifier
- title: The interview question
- category: Behavioral category (Leadership, Teamwork, Growth, Conflict, Situational, Amazon Leadership)
- sub_category: More specific category
- difficulty: easy / medium / hard
- companies: Companies that commonly ask this question
- star_framework: Situation, Task, Action, Result framework breakdown
- tips: Guidelines for answering
- red_flags: Warning signs in candidate responses
- example_answer: Sample high-quality response
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

# ============================================================
# STAR FRAMEWORK DATACLASS
# ============================================================

@dataclass
class STARFramework:
    """STAR framework breakdown for behavioral questions."""
    situation: str  # Describe the context/task
    task: str       # What was your responsibility?
    action: str     # What specific steps did you take?
    result: str     # What was the outcome/achievement?

# ============================================================
# BEHAVIORAL QUESTIONS (30+ questions)
# ============================================================

BEHAVIORAL_QUESTIONS: List[Dict[str, Any]] = [
    # ══════════════════════════════════════════════════════════════════════════
    # LEADERSHIP & INITIATIVE (8 questions)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-101",
        "title": "Tell me about a time you led a team through a difficult project",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": STARFramework(
            situation="Describe the project and its challenges",
            task="What was your specific role and responsibility?",
            action="What specific steps did you take to lead the team?",
            result="What was the outcome? Quantify if possible."
        ),
        "tips": [
            "Focus on YOUR actions, not the team's",
            "Show decision-making process",
            "Quantify results (time saved, money earned, etc.)",
            "Mention what you learned"
        ],
        "red_flags": ["Taking all credit", "Blaming team members", "No measurable outcome"],
        "example_answer": "In my final year project, our team of 4 was building a real-time chat application. Midway, two members had conflicting schedules. I reorganized tasks, created a shared kanban board, and held daily 15-minute standups. We delivered on time with 95% test coverage and positive client feedback.",
    },
    {
        "id": "BH-102",
        "title": "Describe a situation where you took initiative without being asked",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": STARFramework(
            situation="What was the context?",
            task="What problem did you identify?",
            action="What did you do proactively?",
            result="What impact did your initiative have?"
        ),
        "tips": [
            "Show you can identify problems independently",
            "Demonstrate ownership mentality",
            "Show the positive impact of your initiative"
        ],
        "red_flags": ["Waiting for permission", "Small impact", "No follow-through"],
        "example_answer": "I noticed our deployment process was manual and error-prone. Without being asked, I created a CI/CD pipeline using GitHub Actions that reduced deployment time from 2 hours to 5 minutes and eliminated human errors. This allowed the team to deploy daily instead of weekly.",
    },
    {
        "id": "BH-103",
        "title": "Tell me about a time you had to make a decision without complete information",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Meta"],
        "star_framework": STARFramework(
            situation="What was the incomplete information?",
            task="What decision did you need to make?",
            action="How did you gather what you could and decide?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show analytical thinking under uncertainty",
            "Explain your risk assessment process",
            "Demonstrate ability to course-correct"
        ],
        "red_flags": ["Rushing without thinking", "Ignoring available data", "No backup plan"],
        "example_answer": "During a production outage, I had to decide between two approaches without full root cause analysis. I chose the safer rollback approach, then investigated the root cause. This minimized downtime to 5 minutes instead of potential 30 minutes, and the issue was resolved within the SLA.",
    },
    {
        "id": "BH-104",
        "title": "Describe a time you had to influence others without direct authority",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": STARFramework(
            situation="What was the context?",
            task="What did you need to accomplish?",
            action="How did you influence without authority?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show persuasion skills",
            "Demonstrate empathy and understanding",
            "Show how you built consensus"
        ],
        "red_flags": ["Using threats", "Going over people's heads", "No relationship building"],
        "example_answer": "I convinced the backend team to adopt our new API standard by creating a demo showing 40% performance improvement and presenting at the team meeting. No authority, just data and persuasion. The team agreed and we implemented it company-wide, resulting in consistent API documentation.",
    },
    {
        "id": "BH-105",
        "title": "Tell me about a time you failed and what you learned",
        "category": "behavioral",
        "sub_category": "Growth",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta", "Apple"],
        "star_framework": STARFramework(
            situation="What was the failure?",
            task="What were you trying to achieve?",
            action="What went wrong and why?",
            result="What did you learn and how did you apply it?"
        ),
        "tips": [
            "Be honest about the failure",
            "Focus on LEARNING, not the failure itself",
            "Show how you applied the lesson"
        ],
        "red_flags": ["Blaming others", "No self-reflection", "Same mistake repeated"],
        "example_answer": "I once deployed a feature without proper testing, causing a 2-hour outage affecting 500+ users. I learned to always create staging environments and write integration tests. Since then, I've maintained a 99.9% deployment success rate and the team adopted a pre-deployment checklist.",
    },
    {
        "id": "BH-106",
        "title": "Describe a time you mentored or helped a junior team member grow",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": STARFramework(
            situation="What was the team member's challenge?",
            task="What was your role?",
            action="How did you help them grow?",
            result="What was the outcome for them?"
        ),
        "tips": [
            "Show mentoring ability",
            "Demonstrate patience and empathy",
            "Focus on their growth, not your glory"
        ],
        "red_flags": ["Taking credit for their work", "Doing the work for them", "No follow-up"],
        "example_answer": "A junior developer struggled with system design. I created a weekly study plan, pair-programmed on real features, and reviewed their design docs. Within 3 months, they led their first design review successfully and was promoted to senior level.",
    },
    {
        "id": "BH-107",
        "title": "Tell me about a time you identified and resolved a process improvement",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": STARFramework(
            situation="What was the inefficient process?",
            task="What needed to be improved?",
            action="What steps did you take to improve it?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show process thinking",
            "Quantify the improvement",
            "Show sustainability of the change"
        ],
        "red_flags": ["Fixing one thing while breaking another", "No long-term plan", "No team adoption"],
        "example_answer": "I noticed our bug reporting process took 3 days as tickets were emailed. I created a Jira project with a standardized form, automated triage with labels, and reduced resolution time to 24 hours. The team adopted it and customer satisfaction increased 15%.",
    },
    {
        "id": "BH-108",
        "title": "Describe a time you demonstrated ownership beyond your job description",
        "category": "behavioral",
        "sub_category": "Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": STARFramework(
            situation="What was outside your role?",
            task="Why did you take ownership?",
            action="What did you do?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show initiative and responsibility",
            "Demonstrate end-to-end thinking",
            "Show the impact of your ownership"
        ],
        "red_flags": ["Only doing assigned tasks", "No follow-through", "Low impact"],
        "example_answer": "I noticed our onboarding docs were outdated and causing 2-week ramp-up for new hires. I took ownership, interviewed 5 new hires, rewrote the docs, and created a video tutorial. New hire ramp-up time decreased from 2 weeks to 3 days, and the docs became a reference for the whole department.",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # TEAMWORK & COLLABORATION (7 questions)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-201",
        "title": "Describe a time you worked with a difficult team member",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": STARFramework(
            situation="What made the team member difficult?",
            task="What was your goal?",
            action="How did you handle the situation?",
            result="What was the outcome?"
        ),
        "tips": [
            "Stay professional and positive",
            "Focus on the work, not personal issues",
            "Show empathy and communication skills"
        ],
        "red_flags": ["Badmouthing the person", "Escalating immediately", "Giving up"],
        "example_answer": "A teammate consistently missed deadlines. Instead of complaining, I had a private conversation, learned they were struggling with the tech stack, and offered to pair-program. Their productivity improved 50% and we became good collaborators who helped each other on future tasks.",
    },
    {
        "id": "BH-202",
        "title": "Tell me about a time you collaborated with a cross-functional team",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": STARFramework(
            situation="What teams were involved?",
            task="What was the shared goal?",
            action="How did you coordinate across teams?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show communication across boundaries",
            "Demonstrate understanding of different perspectives",
            "Show how you aligned different priorities"
        ],
        "red_flags": ["Working in silos", "Ignoring other teams' needs", "No coordination"],
        "example_answer": "I worked with design, backend, and QA teams to launch a new feature. I created a shared specification doc, held weekly syncs, and ensured everyone was aligned. We launched 1 week ahead of schedule and received positive user feedback on the seamless experience.",
    },
    {
        "id": "BH-203",
        "title": "Describe a time you received critical feedback",
        "category": "behavioral",
        "sub_category": "Growth",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": STARFramework(
            situation="What was the feedback?",
            task="How did it affect you?",
            action="What did you do with the feedback?",
            result="How did you improve?"
        ),
        "tips": [
            "Show openness to feedback",
            "Demonstrate specific improvements",
            "Show growth mindset"
        ],
        "red_flags": ["Defensive reaction", "Ignoring feedback", "No visible improvement"],
        "example_answer": "My manager told my code reviews were too harsh and intimidating. I started framing feedback as questions and suggestions, asked more 'how might we' questions, and now my reviews are appreciated. My team's code quality improved 30% as junior developers felt more comfortable asking questions.",
    },
    {
        "id": "BH-204",
        "title": "Tell me about a time you disagreed with a decision",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": STARFramework(
            situation="What was the decision?",
            task="Why did you disagree?",
            action="How did you express your disagreement?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show respectful disagreement",
            "Demonstrate data-driven reasoning",
            "Show you can disagree and commit"
        ],
        "red_flags": ["Being insubordinate", "Not providing alternatives", "No resolution"],
        "example_answer": "I disagreed with using MongoDB for a relational data model due to performance concerns. I presented a comparison showing 3x slower joins for our use case. The team reconsidered and we chose PostgreSQL instead. The project succeeded with 40% better query performance and we documented the decision for future reference.",
    },
    {
        "id": "BH-205",
        "title": "Describe a time you helped a team member grow",
        "category": "behavioral",
        "sub_category": "Teamwork",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": STARFramework(
            situation="What was the team member's challenge?",
            task="What was your role?",
            action="How did you help them grow?",
            result="What was the outcome for them?"
        ),
        "tips": [
            "Show mentoring ability",
            "Demonstrate patience and empathy",
            "Focus on their growth, not your glory"
        ],
        "red_flags": ["Taking credit for their work", "Doing the work for them", "No follow-up"],
        "example_answer": "A junior developer struggled with system design. I created a weekly study plan, pair-programmed on real features, and reviewed their design docs. Within 3 months, they led their first design review successfully and was promoted to senior level.",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # PROBLEM SOLVING & CONFLICT (5 questions)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-301",
        "title": "Tell me about a time you solved a complex technical problem",
        "category": "behavioral",
        "sub_category": "Problem Solving",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "star_framework": STARFramework(
            situation="What was the technical challenge?",
            task="What was your goal?",
            action="What was your approach to solving it?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show your problem-solving process",
            "Explain technical decisions clearly",
            "Quantify the impact"
        ],
        "red_flags": ["No technical depth", "Taking too long to explain", "No measurable result"],
        "example_answer": "Our API response time was 5 seconds (P99). I identified N+1 queries as the bottleneck, implemented DataLoader pattern for batching, and reduced response time to 200ms (96% improvement). This directly improved conversion rate by 8% and user satisfaction scores.",
    },
    {
        "id": "BH-302",
        "title": "Describe a time you had to resolve a conflict between team members",
        "category": "behavioral",
        "sub_category": "Conflict",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": STARFramework(
            situation="What was the conflict?",
            task="What was your role?",
            action="How did you resolve it?",
            result="What was the outcome?"
        ),
        "tips": [
            "Stay neutral and professional",
            "Focus on facts, not emotions",
            "Find a win-win solution"
        ],
        "red_flags": ["Taking sides", "Ignoring the conflict", "No resolution"],
        "example_answer": "Two senior developers disagreed on architecture (microservices vs monolith). I facilitated a meeting where each presented their approach with benchmarks for latency and deployment complexity. We combined the best of both: core services as microservices and shared utilities in a monorepo. The hybrid approach met all requirements and reduced deployment time by 30%.",
    },
    {
        "id": "BH-303",
        "title": "Tell me about a time you worked under extreme pressure",
        "category": "behavioral",
        "sub_category": "Problem Solving",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": STARFramework(
            situation="What was the pressure?",
            task="What did you need to deliver?",
            action="How did you handle the pressure?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show calm under pressure",
            "Demonstrate prioritization skills",
            "Show you can still deliver quality"
        ],
        "red_flags": ["Panic", "Sacrificing quality", "No support from team"],
        "example_answer": "We had a critical production bug affecting 10,000 users during peak hours. I stayed calm, identified the root cause in 30 minutes from the logs, implemented a fix, and deployed within 2 hours. Zero data loss, full recovery, and I later added comprehensive tests to prevent recurrence.",
    },
    {
        "id": "BH-304",
        "title": "Describe a time you had to make a trade-off between quality and speed",
        "category": "behavioral",
        "sub_category": "Problem Solving",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "star_framework": STARFramework(
            situation="What was the trade-off?",
            task="What were the constraints?",
            action="How did you decide?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show strategic thinking",
            "Explain your decision-making process",
            "Show you can balance competing priorities"
        ],
        "red_flags": ["Always choosing speed", "No consideration of consequences", "No follow-up"],
        "example_answer": "For a hackathon with 48 hours, I chose to implement core features with basic tests rather than full test coverage. We won first place. In the following sprint, I added comprehensive test coverage and refactored the code. The product maintained quality while meeting the deadline.",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # AMAZON LEADERSHIP PRINCIPLES (6 questions)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-401",
        "title": "Customer Obsession: Tell me about a time you went above and beyond for a customer",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": STARFramework(
            situation="Who was the customer?",
            task="What did they need?",
            action="How did you go above and beyond?",
            result="What was the outcome?"
        ),
        "tips": [
            "Focus on customer needs, not company needs",
            "Show empathy and understanding",
            "Quantify the impact on customer satisfaction"
        ],
        "red_flags": ["No customer focus", "Only meeting minimum requirements", "No follow-up"],
        "example_answer": "A client needed a custom feature urgently for a product launch. I worked overtime for 3 days to deliver it, even though it wasn't in our sprint. They launched on time, renewed their contract, and gave us a 5-star review highlighting our flexibility.",
    },
    {
        "id": "BH-402",
        "title": "Ownership: Tell me about a time you took ownership of something outside your job description",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": STARFramework(
            situation="What was outside your role?",
            task="Why did you take ownership?",
            action="What did you do?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show initiative and responsibility",
            "Demonstrate end-to-end thinking",
            "Show the impact of your ownership"
        ],
        "red_flags": ["Only doing assigned tasks", "No follow-through", "Low impact"],
        "example_answer": "I noticed our onboarding docs were outdated. I took ownership, interviewed 5 new hires, rewrote the docs, and created a video tutorial. New hire ramp-up time decreased from 2 weeks to 3 days, and the docs became a reference for the whole department.",
    },
    {
        "id": "BH-403",
        "title": "Bias for Action: Tell me about a time you made a decision quickly",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": STARFramework(
            situation="What was the time pressure?",
            task="What decision did you need to make?",
            action="How did you decide quickly?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show calculated risk-taking",
            "Demonstrate you can act without perfect information",
            "Show the benefit of quick action"
        ],
        "red_flags": ["Reckless decisions", "No risk assessment", "Negative outcome"],
        "example_answer": "During a security incident, I blocked the affected IP range within 5 minutes of detection, preventing further attacks. Later analysis confirmed this was the right call and prevented potential data breach affecting 100+ users.",
    },
    {
        "id": "BH-404",
        "title": "Dive Deep: Tell me about a time you analyzed data to make a decision",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": STARFramework(
            situation="What data did you analyze?",
            task="What decision were you making?",
            action="How did you analyze the data?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show analytical skills",
            "Demonstrate data-driven decision making",
            "Show the impact of your analysis"
        ],
        "red_flags": ["No data backing", "Surface-level analysis", "Ignoring contradicting data"],
        "example_answer": "I analyzed 3 months of user behavior data and found that 40% of drop-offs happened during onboarding. I redesigned the flow, reducing drop-offs by 60% and increasing retention by 25% within 2 months. The changes were A/B tested and the results were statistically significant.",
    },
    {
        "id": "BH-405",
        "title": "Earn Trust: Tell me about a time you built trust with a stakeholder",
        "category": "behavioral",
        "sub_category": "Amazon Leadership",
        "difficulty": "medium",
        "companies": ["Amazon"],
        "star_framework": STARFramework(
            situation="What was the stakeholder relationship?",
            task="What did you need to build?",
            action="How did you build trust?",
            result="What was the outcome?"
        ),
        "tips": [
            "Show consistency and reliability",
            "Demonstrate transparency",
            "Show how you kept commitments"
        ],
        "red_flags": ["Making promises you can't keep", "Hiding mistakes", "No follow-through"],
        "example_answer": "I committed to delivering a feature by a certain date and missed it due to unforeseen complexity. I immediately informed the stakeholder, explained the issue, provided a revised timeline, and delivered early the next week. I maintained weekly updates until delivery. The stakeholder appreciated the transparency and we maintained a strong working relationship.",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # SITUATIONAL QUESTIONS (4 questions)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "BH-501",
        "title": "How would you handle a situation where your project deadline is impossible?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft"],
        "guidance": "Show prioritization, communication, and negotiation skills.",
        "ideal_answer": "I would first assess what's absolutely required vs. nice-to-have. Then I'd communicate with stakeholders, proposing a phased delivery: core features first, enhancements later. I'd also identify if resources can be reallocated or scope reduced.",
        "red_flags": ["Saying you'd just work harder", "No communication plan", "Ignoring the deadline"],
    },
    {
        "id": "BH-502",
        "title": "How would you handle discovering a critical bug in production?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "medium",
        "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "guidance": "Show urgency, systematic debugging, and communication.",
        "ideal_answer": "First, assess impact and communicate to stakeholders. Then, gather logs and reproduce. Fix the immediate issue (rollback if needed). Then investigate root cause and implement a permanent fix with tests.",
        "red_flags": ["Panicking", "Blaming others", "No rollback plan"],
    },
    {
        "id": "BH-503",
        "title": "How would you approach learning a completely new technology stack?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "easy",
        "companies": ["Amazon", "Google", "Microsoft"],
        "guidance": "Show structured learning and practical application.",
        "ideal_answer": "I'd start with official documentation and tutorials, then build a small project to apply concepts. I'd join community forums for questions and read production code from open-source projects. Within 2 weeks, I'd be productive.",
        "red_flags": ["No learning plan", "Only reading, no practice", "Expecting instant mastery"],
    },
    {
        "id": "BH-504",
        "title": "How would you handle a situation where you disagree with your manager's technical decision?",
        "category": "behavioral",
        "sub_category": "Situational",
        "difficulty": "hard",
        "companies": ["Amazon", "Google", "Microsoft"],
        "guidance": "Show respect, data-driven reasoning, and ability to disagree and commit.",
        "ideal_answer": "I'd prepare a data-backed comparison of alternatives. Present it respectfully in a 1-on-1. If the manager still decides differently, I'd commit fully to their decision while documenting my concerns for future reference.",
        "red_flags": ["Going over manager's head", "Passive-aggressive compliance", "No data to support disagreement"],
    },
]

# ============================================================
# COMBINED BEHAVIORAL QUESTION BANK
# ============================================================

BEHAVIORAL_QUESTION_BANK = {
    "leadership": [],
    "teamwork": [],
    "growth": [],
    "conflict": [],
    "situational": [],
    "problem_solving": [],
    "amazon_leadership": [],
}

# Categorize all questions by their sub_category (the real grouping signal).
# NOTE: q["category"] is the generic literal "behavioral"; the specific bucket
# is determined by q["sub_category"], e.g. "Leadership", "Problem Solving".
# Exact matches are used to avoid substring overlaps (e.g. "Amazon Leadership"
# must NOT also land in "leadership").
for q in BEHAVIORAL_QUESTIONS:
    sub = q.get("sub_category", "")
    if sub == "Leadership":
        BEHAVIORAL_QUESTION_BANK["leadership"].append(q)
    elif sub == "Teamwork":
        BEHAVIORAL_QUESTION_BANK["teamwork"].append(q)
    elif sub == "Growth":
        BEHAVIORAL_QUESTION_BANK["growth"].append(q)
    elif sub == "Conflict":
        BEHAVIORAL_QUESTION_BANK["conflict"].append(q)
    elif sub == "Situational":
        BEHAVIORAL_QUESTION_BANK["situational"].append(q)
    elif sub == "Problem Solving":
        BEHAVIORAL_QUESTION_BANK["problem_solving"].append(q)
    elif sub == "Amazon Leadership":
        BEHAVIORAL_QUESTION_BANK["amazon_leadership"].append(q)

# Count by category
counts = {k: len(v) for k, v in BEHAVIORAL_QUESTION_BANK.items()}
total = sum(counts.values())

if __name__ == "__main__":
    print(f"Behavioral Question Bank loaded: {total} questions")
    for cat, qs in counts.items():
        print(f"  {cat}: {qs} questions")

# Provide quick access functions
def get_questions_by_category(category: str) -> List[Dict[str, Any]]:
    """Get questions by behavioral category."""
    return BEHAVIORAL_QUESTION_BANK.get(category, [])

def get_random_question(category: str) -> Optional[Dict[str, Any]]:
    """Get a random question from a category."""
    import random
    qs = get_questions_by_category(category)
    return random.choice(qs) if qs else None