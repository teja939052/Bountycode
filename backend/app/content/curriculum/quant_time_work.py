"""
Promoted Lesson: Time and Work
==============================

Service-company quantitative aptitude foundation. Follows the full content contract.

Provenance: Pattern-relevant for TCS NQT, Infosys, Wipro, Cognizant, Capgemini,
Accenture service-company quantitative aptitude sections.
"""
from typing import Dict, List, Any

LESSON_ID = "quant_time_work_01"
VERSION = "1.0.0"
SKILL_ID = "quant.time_work"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

TIME_WORK_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "quantitative_aptitude:time_work",
    "title": "Time and Work",
    "description": "Master work-rate problems — individual rates, combined rates, and efficiency.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["individual_work_rate", "combined_work_rate", "efficiency", "work_wages"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Compute individual work rate (1/day).",
        "Combine work rates of multiple workers.",
        "Find time taken when workers work together.",
        "Solve efficiency-based work problems.",
    ],
    "prerequisites": ["quant.fractions_decimals"],
    "concept_explanation": {
        "title": "Time and Work",
        "text": (
            "If A can complete a job in N days, A's one-day work is 1/N. When multiple people "
            "work together, their one-day work rates add up. Time taken together = 1 / (sum of rates)."
        ),
        "key_formula": "Work rate = 1 / days. Combined rate = sum of individual rates.",
    },
    "worked_example": {
        "title": "A and B together",
        "problem": "A can complete a task in 6 days. B can complete it in 12 days. How long together?",
        "steps": [
            "A's rate = 1/6 per day.",
            "B's rate = 1/12 per day.",
            "Combined rate = 1/6 + 1/12 = 2/12 + 1/12 = 3/12 = 1/4 per day.",
            "Time together = 1 / (1/4) = 4 days.",
        ],
        "answer": 4,
    },
    "interactive_practice": [
        {
            "id": "tw_practice_1",
            "type": "mcq",
            "question": "A can do a job in 10 days. B can do it in 15 days. Together?",
            "options": [5, 6, 7, 8],
            "correct_index": 1,
            "explanation": "1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6. Time = 6 days.",
        },
        {
            "id": "tw_practice_2",
            "type": "mcq",
            "question": "A completes 1/4 of a job in 3 days. How long for the full job?",
            "options": [9, 12, 15, 18],
            "correct_index": 1,
            "explanation": "1/4 in 3 days means full job in 3 × 4 = 12 days.",
        },
    ],
    "misconception_feedback": {
        "adding_days_instead_of_rates": {
            "title": "Common mistake: Adding days instead of rates",
            "text": "If A takes 6 days and B takes 12 days, together they do NOT take 6+12=18 days. They take 1/(1/6+1/12) = 4 days.",
        },
    },
    "assessment": [
        {
            "id": "tw_assess_1",
            "type": "mcq",
            "question": "A does a job in 8 days. B does it in 24 days. Together?",
            "options": [4, 5, 6, 7],
            "correct_index": 2,
            "explanation": "1/8 + 1/24 = 3/24 + 1/24 = 4/24 = 1/6. Time = 6 days.",
        },
        {
            "id": "tw_assess_2",
            "type": "mcq",
            "question": "3 men complete a job in 10 days. How long for 5 men?",
            "options": [4, 5, 6, 7],
            "correct_index": 0,
            "explanation": "Total man-days = 30. For 5 men: 30/5 = 6 days.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Painting a room",
        "problem": (
            "Alice can paint a room in 6 hours. Bob can paint it in 9 hours. "
            "If they work together, how long to paint the room?"
        ),
        "steps": [
            "Alice's rate = 1/6 per hour.",
            "Bob's rate = 1/9 per hour.",
            "Combined = 1/6 + 1/9 = 3/18 + 2/18 = 5/18 per hour.",
            "Time = 1 / (5/18) = 18/5 = 3.6 hours.",
        ],
        "answer": 3.6,
    },
    "deterministic_answer_key": {
        "tw_practice_1": 1,
        "tw_practice_2": 1,
        "tw_assess_1": 2,
        "tw_assess_2": 0,
        "transfer_task": 3.6,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/quantitative-aptitude/time-and-work/",
        ],
        "note": (
            "This preparation path targets commonly reported patterns and role expectations. "
            "It is not a claim about a private employer question bank."
        ),
    },
    "review_state": "human_reviewed",
    "accessibility_metadata": {
        "color_blind_safe": True,
        "screen_reader_friendly": True,
        "font_scale_support": True,
    },
    "spaced_repetition_metadata": {
        "initial_interval_days": 1,
        "ease_factor": 2.5,
        "retention_target": 0.85,
    },
}
