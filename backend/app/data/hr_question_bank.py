"""High-Quality HR & People Management Question Bank.

This module contains curated HR and people management interview questions
focused on practical scenarios that hiring managers and HR professionals
commonly evaluate. Questions cover the full employee lifecycle.

Each question includes:
- id: Unique identifier
- question: The interview question
- category: HR category (Hiring, Performance, Conflict, Development, Policy)
- difficulty: easy / medium / hard
- companies: Companies that commonly ask this topic
- ideal_answer: Guide for what a strong answer should cover
- red_flags: Warning signs in candidate responses
"""

from typing import List, Dict, Any, Optional

# ============================================================
# HR QUESTIONS (20+ questions)
# ============================================================

HR_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "HR-001",
        "question": "What approach do you take when recruiting for a technical role where you need to assess both technical skills and cultural fit?",
        "category": "hiring",
        "difficulty": "medium",
        "companies": ["tcs", "infosys", "wipro", "accenture"],
        "ideal_answer": "I use a structured interview process with standardized technical assessments, behavioral questions using STAR framework, and involve multiple interviewers to reduce bias. I also include a practical task or coding exercise relevant to the role, and conduct cultural fit assessments through values-alignment questions and peer interviews.",
        "red_flags": ["Relying only on resumes", "No structured assessment", "Cannot articulate company values", "Overemphasizing cultural fit as exclusionary"],
    },
    {
        "id": "HR-002",
        "question": "How do you handle a situation where an employee consistently misses deadlines?",
        "category": "performance",
        "difficulty": "medium",
        "companies": ["tcs", "infosys", "wipro"],
        "ideal_answer": "I first have a private conversation to understand the root cause - whether it's workload, skill gaps, personal issues, or unclear expectations. Then I work with the employee to create a performance improvement plan with clear milestones, provide necessary support/training, and set regular check-ins. If the pattern continues despite support, I follow the formal PIP (Performance Improvement Plan) process.",
        "red_flags": ["Blaming the employee immediately", "No documentation", "Skipping the conversation step", "Inconsistent treatment of other employees"],
    },
    {
        "id": "HR-003",
        "question": "How do you conduct a fair and unbiased performance review?",
        "category": "performance",
        "difficulty": "medium",
        "companies": ["wipro", "accenture"],
        "ideal_answer": "I use a combination of quantitative metrics (KPIs, deliverables) and qualitative feedback (peer reviews, manager observations). I ensure the employee has had regular check-ins throughout the period, provide specific examples, give the employee a chance to self-assess, and align ratings to clear rubrics. I also calibrate with other managers to reduce bias.",
        "red_flags": ["Recency bias (only recent performance matters)", "Halo/horn effect (one quality colors everything)", "No documented evidence", "No self-assessment opportunity"],
    },
    {
        "id": "HR-004",
        "question": "How do you handle a salary negotiation where the candidate's expectations exceed the budget?",
        "category": "hiring",
        "difficulty": "medium",
        "companies": ["infosys", "wipro"],
        "ideal_answer": "I first understand their motivations - is it purely financial, or do they value growth, work-life balance, or specific projects? Then I explain our total compensation package including benefits, learning opportunities, and career progression. If there's a gap, I explore creative solutions like sign-on bonuses, flexible work arrangements, or a performance review timeline for salary adjustment.",
        "red_flags": ["Being rigid without understanding candidate needs", "Making promises that can't be delivered", "Apologizing excessively without solutions"],
    },
    {
        "id": "HR-005",
        "question": "Describe how you would handle a workplace conflict between two team members that's affecting productivity.",
        "category": "conflict",
        "difficulty": "medium",
        "companies": ["tcs", "infosys", "wipro"],
        "ideal_answer": "I would first speak with each person individually to understand their perspective without judgment. Then I'd bring them together for a mediated conversation focused on facts, not emotions, and guide them to identify common goals and solutions. I'd establish clear expectations for future collaboration and follow up regularly.",
        "red_flags": ["Taking sides immediately", "Meeting with both together before individual conversations", "Ignoring the impact on productivity"],
    },
    {
        "id": "HR-006",
        "question": "How do you support employee development and career growth?",
        "category": "development",
        "difficulty": "medium",
        "companies": ["tcs", "infosys", "wipro"],
        "ideal_answer": "I believe in a personalized development approach. I start by having career conversations to understand each employee's goals and aspirations. Then I create individual development plans (IDPs) that may include mentorship, stretch assignments, training courses, certifications, and regular check-ins. I also ensure opportunities for internal mobility and cross-functional exposure.",
        "red_flags": ["One-size-fits-all approach", "No follow-through on development plans", "Only focusing on technical skills, ignoring soft skills"],
    },
    {
        "id": "HR-007",
        "question": "How do you handle an employee who is technically excellent but has a negative attitude that affects team morale?",
        "category": "performance",
        "difficulty": "hard",
        "companies": ["wipro", "accenture"],
        "ideal_answer": "I address this through a direct but empathetic conversation. I specific behavior examples and their impact on the team. I understand the root cause - sometimes it's burnout, personal issues, or misalignment with the role. I work on a improvement plan that may include role reassignment, mentorship, or if necessary, a performance improvement plan. The goal is to either improve the situation or part ways constructively.",
        "red_flags": ["Avoiding the conversation", "Only focusing on technical performance", "Being aggressive or confrontational"],
    },
    {
        "id": "HR-008",
        "question": "What is your approach to onboarding new employees?",
        "category": "hiring",
        "difficulty": "easy",
        "companies": ["infosys", "wipro"],
        "ideal_answer": "I use a structured 90-day onboarding plan that includes: first-day orientation and setup, week 1: team introductions and role clarification, weeks 2-4: hands-on projects with mentor support, weeks 5-8: increasing responsibility and cross-team exposure, weeks 9-90: check-ins, feedback sessions, and goal setting. I also create a 30-60-90 day plan with the manager and new hire.",
        "red_flags": ["Sink or swim approach", "No formal structure", "No check-ins or feedback loops"],
    },
    {
        "id": "HR-009",
        "question": "How do you promote diversity and inclusion in the workplace?",
        "category": "policy",
        "difficulty": "medium",
        "companies": ["tcs", "infosys", "wipro", "accenture"],
        "ideal_answer": "I advocate for D&I at every stage: unbiased job descriptions, diverse interview panels, structured interviews to reduce bias, blind resume screening when appropriate, employee resource groups, mentorship programs for underrepresented groups, and regular diversity metrics and audits. I also foster an inclusive culture through training, open dialogue, and leadership accountability.",
        "red_flags": ["Diversity without inclusion initiatives", "Tokenism", "No metrics or accountability", "Resistance to feedback on D&I efforts"],
    },
    {
        "id": "HR-010",
        "question": "How do you handle redundancy or layoffs fairly?",
        "category": "policy",
        "difficulty": "hard",
        "companies": ["tcs", "infosys"],
        "ideal_answer": "I ensure transparency, fairness, and compliance with all labor laws. This includes: clear selection criteria based on objective factors (skills, performance, business needs), individual meetings with affected employees, severance packages, outplacement support, notice periods, and outplacement coaching. I also maintain morale among remaining employees through honest communication about the situation and future plans.",
        "red_flags": ["No clear criteria", "Sudden announcements without process", "No support for departing employees", "No communication with remaining staff"],
    },
    {
        "id": "HR-011",
        "question": "What would you do if you suspected an employee was engaging in harassment or discrimination?",
        "category": "policy",
        "difficulty": "hard",
        "companies": ["wipro", "accenture"],
        "ideal_answer": "I would follow the company's legal and HR protocols immediately. This includes documenting specific incidents, reporting to the appropriate HR business partner or legal team, ensuring a confidential and thorough investigation, taking appropriate action based on findings, and supporting both the victim and the accused during the process. I would also implement preventative measures like training and policy reviews.",
        "red_flags": ["Ignoring or minimizing the concern", "Investigating without HR/legal involvement", "Breaching confidentiality", "Retaliation against the complainant"],
    },
    {
        "id": "HR-012",
        "question": "How do you measure employee engagement and satisfaction?",
        "category": "performance",
        "difficulty": "medium",
        "companies": ["tcs", "infosys"],
        "ideal_answer": "I use a combination of quantitative and qualitative methods: regular employee pulse surveys (eNPS - Employee Net Promoter Score), stay interviews, one-on-one meetings, turnover analysis, and feedback tools. I analyze trends, identify root causes of dissatisfaction, and act on the feedback with visible follow-through, which is critical for trust.",
        "red_flags": ["Surveying without acting on results", "Only measuring once a year", "Ignoring negative trends", "No follow-up on feedback"],
    },
    {
        "id": "HR-013",
        "question": "How do you handle a situation where two departments are competing for the same resources?",
        "category": "conflict",
        "difficulty": "medium",
        "companies": ["infosys", "wipro"],
        "ideal_answer": "I facilitate a discussion between the department heads to understand the business impact of each request. I help prioritize based on company objectives, timelines, and ROI. I may explore compromises like shared resources, phased allocation, or revised timelines. The goal is to align with company objectives rather than departmental silos.",
        "red_flags": ["Taking sides without business justification", "No connection to company goals", "Ignoring one department's needs"],
    },
    {
        "id": "HR-014",
        "question": "What would you do if an employee consistently violates company policy?",
        "category": "policy",
        "difficulty": "medium",
        "companies": ["tcs", "wipro"],
        "ideal_answer": "I would follow the progressive discipline process: 1) Private conversation and coaching, 2) Written warning with specific expectations, 3) Final warning with consequences clearly outlined, 4) If no improvement, separation following due process and legal requirements. I ensure all actions are documented and consistent with how similar situations were handled previously.",
        "red_flags": ["Skipping progressive steps", "Inconsistent application", "No documentation"],
    },
    {
        "id": "HR-015",
        "question": "How do you foster a culture of continuous learning and improvement?",
        "category": "development",
        "difficulty": "medium",
        "companies": ["tcs", "infosys", "wipro"],
        "ideal_answer": "I promote learning through: dedicated learning time (e.g., 10% time), lunch-and-learn sessions, conference budgets, certification reimbursements, internal knowledge-sharing sessions, hackathons, and celebrating learning achievements. I also lead by example by sharing what I'm learning and creating psychological safety for others to admit knowledge gaps and ask questions.",
        "red_flags": ["No budget or time allocated for learning", "Punishing mistakes", "No recognition of learning achievements"],
    },
    {
        "id": "HR-016",
        "question": "How do you handle remote work performance management?",
        "category": "performance",
        "difficulty": "medium",
        "companies": ["wipro", "accenture"],
        "ideal_answer": "I focus on outcomes and deliverables rather than activity monitoring. I set clear KPIs and expectations, have regular check-ins (video calls), use collaboration tools effectively, maintain team connectivity through virtual social events, and ensure employees have the necessary equipment and support. I watch for burnout signs and encourage work-life balance.",
        "red_flags": ["Micromanaging activity instead of results", "No regular check-ins", "Ignoring remote work challenges"],
    },
    {
        "id": "HR-017",
        "question": "What would you do if an employee discloses a personal crisis affecting their work?",
        "category": "policy",
        "difficulty": "medium",
        "companies": ["tcs", "infosys"],
        "ideal_answer": "I handle this with confidentiality, empathy, and flexibility. I first listen without judgment, then discuss options such as flexible work hours, remote work temporarily, Employee Assistance Program (EAP) referral, or temporary leave. I work with the employee to create a support plan and set a check-in timeline. I maintain strict confidentiality and do not share details with others unless necessary.",
        "red_flags": ["Sharing the disclosure with others", "Making promises I can't keep", "No follow-up or support plan"],
    },
    {
        "id": "HR-018",
        "question": "How do you align HR initiatives with business objectives?",
        "category": "policy",
        "difficulty": "hard",
        "companies": ["accenture"],
        "ideal_answer": "I start by understanding the company's strategic goals for the quarter/year. Then I ensure HR initiatives - recruiting, learning, performance, culture - directly support those goals. For example, if the business objective is expanding into new markets, I focus recruitment on candidates with relevant experience, multilingual skills, or geographic knowledge. I regularly report HR metrics that connect to business outcomes.",
        "red_flags": ["HR initiatives in a vacuum", "No connection to business goals", "Reporting vanity metrics"],
    },
    {
        "id": "HR-019",
        "question": "How do you handle exit interviews and what do you do with the feedback?",
        "category": "policy",
        "difficulty": "medium",
        "companies": ["tcs", "infosys"],
        "ideal_answer": "I conduct structured exit interviews using consistent questions to ensure comparability. I focus on understanding the 'why' behind the departure, gather feedback on management, culture, growth opportunities, and compensation. I analyze trends, share anonymized insights with leadership, and implement changes where possible. I also ensure a positive offboarding experience to maintain alumni relationships.",
        "red_flags": ["No structured interview process", "Defensive reaction to feedback", "No follow-through on insights", "Making promises during exit that can't be kept"],
    },
    {
        "id": "HR-020",
        "question": "How do you build a strong employer brand",
        "category": "hiring",
        "difficulty": "medium",
        "companies": ["infosys", "wipro"],
        "ideal_answer": "I focus on Employee Value Proposition (EVP): what makes working at our company unique and valuable. This includes authentic employee stories, career growth opportunities, culture, work-life balance, benefits, and community involvement. I leverage social media, employee advocacy, review sites (Glassdoor), and recruitment marketing. I ensure the candidate experience aligns with the employer brand promise.",
        "red_flags": ["Inauthentic messaging", "Disconnect between brand and reality", "No employee involvement in brand building"],
    },
]

# ============================================================
# COMBINED HR QUESTION BANK
# ============================================================

HR_QUESTION_BANK = {
    "hiring": [],
    "performance": [],
    "conflict": [],
    "development": [],
    "policy": [],
}

# Categorize all questions
for q in HR_QUESTIONS:
    cat = q["category"]
    if cat not in HR_QUESTION_BANK:
        HR_QUESTION_BANK[cat] = []
    HR_QUESTION_BANK[cat].append(q)

# Count by category
counts = {k: len(v) for k, v in HR_QUESTION_BANK.items()}
total = sum(counts.values())

if __name__ == "__main__":
    print(f"HR Question Bank loaded: {total} questions")
    for cat, qs in counts.items():
        print(f"  {cat}: {qs} questions")

# Provide quick access functions
def get_questions_by_category(category: str) -> List[Dict[str, Any]]:
    """Get questions by HR category."""
    return HR_QUESTION_BANK.get(category, [])

def get_random_question(category: str) -> Optional[Dict[str, Any]]:
    """Get a random question from a category."""
    import random
    qs = get_questions_by_category(category)
    return random.choice(qs) if qs else None