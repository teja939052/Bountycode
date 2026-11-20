"""
Promoted Lesson: Logical Series
===============================

Service-company logical reasoning foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company logical reasoning sections.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "logical_series_01"
VERSION = "1.0.0"
SKILL_ID = "logical.series"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 10
XP_REWARD = 90

LOGICAL_SERIES_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "logical_reasoning:series",
    "title": "Logical Series",
    "description": "Master number and letter series — arithmetic, geometric, Fibonacci, and mixed patterns.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["arithmetic_series", "geometric_series", "fibonacci", "mixed_patterns"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Identify arithmetic series (constant difference).",
        "Identify geometric series (constant ratio).",
        "Recognize Fibonacci-like series (sum of previous two).",
        "Find the next term or missing term in a series.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Number Series",
        "text": (
            "A series is a sequence following a rule. Arithmetic: add/subtract the same number. "
            "Geometric: multiply/divide by the same number. Fibonacci: each term is the sum of "
            "the previous two. Look at differences between consecutive terms to find the rule."
        ),
        "key_formula": "Arithmetic: a, a+d, a+2d... Geometric: a, ar, ar²...",
    },
    "worked_example": {
        "title": "Find next term",
        "problem": "2, 5, 8, 11, ?",
        "steps": [
            "Check differences: 5-2=3, 8-5=3, 11-8=3.",
            "Constant difference = 3 → arithmetic series.",
            "Next term = 11 + 3 = 14.",
        ],
        "answer": 14,
    },
    "interactive_practice": [
        {
            "id": "series_practice_1",
            "type": "mcq",
            "question": "3, 6, 9, 12, ?",
            "options": [13, 14, 15, 16],
            "correct_index": 2,
            "explanation": "Add 3 each time. 12 + 3 = 15.",
        },
        {
            "id": "series_practice_2",
            "type": "mcq",
            "question": "2, 4, 8, 16, ?",
            "options": [20, 24, 30, 32],
            "correct_index": 3,
            "explanation": "Multiply by 2 each time. 16 × 2 = 32.",
        },
    ],
    "misconception_feedback": {
        "check_differences_first": {
            "title": "Common mistake: Not checking differences",
            "text": "Always compute differences between consecutive terms first — that reveals arithmetic patterns quickly.",
        },
    },
    "assessment": [
        {
            "id": "series_assess_1",
            "type": "mcq",
            "question": "1, 1, 2, 3, 5, ?",
            "options": [6, 7, 8, 9],
            "correct_index": 2,
            "explanation": "Fibonacci series: each term is sum of previous two. 3 + 5 = 8.",
        },
        {
            "id": "series_assess_2",
            "type": "mcq",
            "question": "10, 7, 4, 1, ?",
            "options": [-2, -1, 0, 2],
            "correct_index": 0,
            "explanation": "Subtract 3 each time. 1 - 3 = -2.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Savings pattern",
        "problem": (
            "You save ₹100 in week 1, ₹150 in week 2, ₹200 in week 3. "
            "How much do you save in week 7 if the pattern continues?"
        ),
        "steps": [
            "Difference = 50 each week → arithmetic series.",
            "Week n: 100 + (n-1) × 50.",
            "Week 7: 100 + 6 × 50 = 100 + 300 = 400.",
        ],
        "answer": 400,
    },
    "deterministic_answer_key": {
        "series_practice_1": 2,
        "series_practice_2": 3,
        "series_assess_1": 2,
        "series_assess_2": 0,
        "transfer_task": 400,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/logical-reasoning/number-series/",
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
