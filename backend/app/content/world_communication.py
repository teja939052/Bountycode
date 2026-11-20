"""Communication and Professional Readiness world.

Maps to canonical skills:
- behavioral.communication
- interview.communication
"""

from __future__ import annotations

from app.content.lesson_definitions import (
    LessonDefinition, LessonStep, TownDefinition, WorldDefinition,
)

SPOKEN_ENGLISH_LESSON = LessonDefinition(
    id="spoken_english",
    title="Spoken English for Interviews",
    icon="\ud83d\udcdd",
    kind="level",
    order=1,
    concept="Fluency, clarity, pacing, and pronunciation in interview settings.",
    mental_model="Speak clearly, at a moderate pace, with structured thoughts.",
    canonical_skill="behavioral.communication",
    estimated_minutes=15,
    diamonds=40,
    location="Communication Lab",
    npc="Speech Coach",
    npc_line="Clarity beats accent every time.",
    tutor_discover="Pause between thoughts. Use simple words. Structure your answer with STAR.",
    tutor_explain="Practice common interview questions aloud. Record yourself and listen for filler words.",
    steps=[
        LessonStep(
            step_type="discover",
            title="Interview Speaking",
            content="Introduce yourself in 60 seconds — name, background, why this role.",
            visual="interview setting",
            interaction="select-value",
            prompt="What matters most in spoken interview English?",
            values=[{"id": "clarity", "text": "Clarity"}, {"id": "accent", "text": "Perfect accent"}, {"id": "speed", "text": "Fast speed"}],
            answer="clarity",
        ),
        LessonStep(
            step_type="build",
            title="Self-Introduction",
            content="Write a 60-second self-introduction for a software developer role.",
            language="sql",
            starter="",
            test_cases=[{"input": [], "expected": "A structured introduction with name, background, and motivation"}],
            passing_score=80,
        ),
    ],
    mastery_evidence=["Can deliver a clear, structured 60-second self-introduction"],
    why_this_matters="The first impression in an interview is your spoken introduction.",
    engineering_context="Daily standups, code reviews, and client calls all require clear spoken English.",
    builds_toward="Communication and professional readiness",
)

EMAIL_WRITING_LESSON = LessonDefinition(
    id="email_writing",
    title="Professional Email Writing",
    icon="\u2709\ufe0f",
    kind="level",
    order=2,
    concept="Clear subject lines, structure, tone, and call-to-action in professional emails.",
    mental_model="Subject tells what, body tells why and what next.",
    canonical_skill="behavioral.communication",
    estimated_minutes=15,
    diamonds=40,
    location="Inbox Hall",
    npc="Editor",
    npc_line="Busy people skim — make your email scannable.",
    tutor_discover="Subject line summarizes the ask. First paragraph states purpose. Last paragraph states next step.",
    tutor_explain="Use bullets for multiple points. Bold key dates and actions. Keep it under 150 words.",
    steps=[
        LessonStep(
            step_type="discover",
            title="Email Structure",
            content="Requesting a meeting with a hiring manager.",
            visual="email with subject, greeting, body, closing",
            interaction="select-value",
            prompt="What makes a good subject line?",
            values=[{"id": "summary", "text": "Summarizes the request"}, {"id": "vague", "text": "Vague and short"}, {"id": "allcaps", "text": "ALL CAPS"}],
            answer="summary",
        ),
        LessonStep(
            step_type="build",
            title="Write Request Email",
            content="Write an email requesting a 30-minute informational interview.",
            language="sql",
            starter="Subject: ",
            test_cases=[{"input": [], "expected": "A professional email with clear subject, purpose, and call to action"}],
            passing_score=80,
        ),
    ],
    mastery_evidence=["Can write a clear, scannable professional email with subject, purpose, and call-to-action"],
    why_this_matters="Recruiters and hiring managers evaluate written communication from the first email.",
    engineering_context="Engineers write daily emails, Slack messages, and documentation — clarity matters.",
    builds_toward="Communication and professional readiness",
)

GROUP_DISCUSSION_LESSON = LessonDefinition(
    id="group_discussion",
    title="Group Discussion",
    icon="\ud83d\udc65\ufe0f",
    kind="level",
    order=3,
    concept="Listen, build on others' ideas, stay on topic, summarize.",
    mental_model="A group discussion is a collaboration, not a debate to win.",
    canonical_skill="behavioral.communication",
    estimated_minutes=15,
    diamonds=40,
    location="Discussion Room",
    npc="Facilitator",
    npc_line="Build on what others say — don't just wait to speak.",
    tutor_discover="Listen actively. Acknowledge others' points before adding yours. Keep the group on track.",
    tutor_explain="Use phrases like 'Building on X's point...' and 'To summarize what we've discussed...'",
    steps=[
        LessonStep(
            step_type="discover",
            title="GD Dynamics",
            content="5 candidates discuss 'Should remote work be mandatory?'",
            visual="circle of candidates",
            interaction="select-value",
            prompt="What's the most important GD skill?",
            values=[{"id": "listening", "text": "Active listening"}, {"id": "dominating", "text": "Dominating conversation"}, {"id": "interrupting", "text": "Interrupting others"}],
            answer="listening",
        ),
        LessonStep(
            step_type="build",
            title="Build on Others",
            content="Respond to: 'I think remote work saves commute time.'",
            language="sql",
            starter="",
            test_cases=[{"input": [], "expected": "A response that builds on the point and adds a related perspective"}],
            passing_score=80,
        ),
    ],
    mastery_evidence=["Can participate constructively in a group discussion, building on others' ideas"],
    why_this_matters="Service companies use group discussions to filter candidates before technical rounds.",
    engineering_context="Team meetings, standups, and brainstorming sessions are workplace group discussions.",
    builds_toward="Communication and professional readiness",
)

BEHAVIORAL_LESSON = LessonDefinition(
    id="behavioral_star",
    title="Behavioral Interview — STAR Method",
    icon="\u2605",
    kind="level",
    order=4,
    concept="Situation, Task, Action, Result — structure behavioral answers.",
    mental_model="STAR gives your story a clear beginning, middle, and end.",
    canonical_skill="interview.communication",
    estimated_minutes=20,
    diamonds=50,
    location="Interview Prep Room",
    npc="Interviewer",
    npc_line="Tell me about a time you handled conflict — use STAR.",
    tutor_discover="Situation = context. Task = your responsibility. Action = what YOU did. Result = outcome with metrics.",
    tutor_explain="Focus on your actions (not the team's). Quantify results when possible.",
    steps=[
        LessonStep(
            step_type="discover",
            title="STAR Components",
            content="'Tell me about a time you resolved a conflict with a teammate.'",
            visual="STAR diagram",
            interaction="select-value",
            prompt="Which STAR part describes what YOU specifically did?",
            values=[{"id": "action", "text": "Action"}, {"id": "situation", "text": "Situation"}, {"id": "result", "text": "Result"}],
            answer="action",
        ),
        LessonStep(
            step_type="build",
            title="Write STAR Answer",
            content="Write a STAR answer for: 'Tell me about a time you missed a deadline.'",
            language="sql",
            starter="Situation: ",
            test_cases=[{"input": [], "expected": "A complete STAR-structured response"}],
            passing_score=80,
        ),
    ],
    mastery_evidence=["Can structure behavioral interview answers using the STAR method"],
    why_this_matters="Behavioral rounds are gatekeepers at TCS, Infosys, Wipro, and most service companies.",
    engineering_context="Promotion and performance reviews also use behavioral storytelling.",
    builds_toward="Communication and professional readiness",
)

COMM_TOWN = TownDefinition(
    id="comm_town",
    name="Communication Town",
    icon="\ud83d\udcac",
    description="Spoken English, email writing, group discussion, behavioral interviews.",
    order=1,
    mental_model="Clear communication multiplies the impact of your technical skills.",
    canonical_skills=["behavioral.communication", "interview.communication"],
    competencies=["spoken_english", "email_writing", "group_discussion", "behavioral_star"],
    lessons=[
        SPOKEN_ENGLISH_LESSON,
        EMAIL_WRITING_LESSON,
        GROUP_DISCUSSION_LESSON,
        BEHAVIORAL_LESSON,
    ],
)

WORLD_COMMUNICATION = WorldDefinition(
    id="communication",
    name="Communication & Professional Readiness",
    subtitle="Speak, write, and interview with confidence",
    description="Communication skills for service-company placement — spoken English, email, group discussion, behavioral interviews.",
    icon="\ud83d\udcac",
    order=15,
    theme="communication",
    recommended_roles=["developer", "backend", "frontend", "data-analyst", "qa-automation", "ai-engineer"],
    prerequisites=["foundations"],
    towns=[COMM_TOWN],
)
