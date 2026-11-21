"""
Promoted Lesson: Averages
=========================

Service-company quantitative aptitude foundation. Follows the full content contract.

Provenance: Pattern-relevant for TCS NQT, Infosys, Wipro, Cognizant, Capgemini,
Accenture service-company quantitative aptitude sections.
"""
from typing import Dict, List, Any

LESSON_ID = "quant_averages_01"
VERSION = "1.0.0"
SKILL_ID = "quant.averages"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 10
XP_REWARD = 90

AVERAGES_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "quantitative_aptitude:averages",
    "title": "Averages",
    "description": "Master average calculations — mean, weighted average, and average speed.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["simple_average", "weighted_average", "average_speed", "average_of_groups"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Calculate the simple average (mean) of a set of numbers.",
        "Compute weighted averages.",
        "Solve average speed problems.",
        "Find the missing number when average changes.",
    ],
    "prerequisites": ["quant.number_systems_basics"],
    "concept_explanation": {
        "title": "What is an Average?",
        "text": (
            "The average (arithmetic mean) is the sum of all values divided by the count of values. "
            "Average = Sum / Count."
        ),
        "key_formula": "Average = Sum of values / Number of values.",
    },
    "worked_example": {
        "title": "Average of 5 numbers",
        "problem": "Find the average of 10, 20, 30, 40, 50.",
        "steps": [
            "Sum = 10 + 20 + 30 + 40 + 50 = 150.",
            "Count = 5.",
            "Average = 150 / 5 = 30.",
        ],
        "answer": 30,
    },
    "interactive_practice": [
        {
            "id": "avg_practice_1",
            "type": "mcq",
            "question": "What is the average of 5, 10, 15, 20, 25?",
            "options": [10, 15, 20, 25],
            "correct_index": 1,
            "explanation": "Sum = 75, Count = 5. Average = 75/5 = 15.",
        },
        {
            "id": "avg_practice_2",
            "type": "mcq",
            "question": "The average of 3 numbers is 18. Two are 15 and 21. Find the third.",
            "options": [12, 15, 18, 21],
            "correct_index": 0,
            "explanation": "Total = 18 × 3 = 54. Third = 54 - 15 - 21 = 18.",
        },
    ],
    "misconception_feedback": {
        "average_is_not_middle": {
            "title": "Common mistake: Confusing average with median",
            "text": "Average is sum/count, not the middle number. For 1, 2, 100, the average is 34.33 but the median is 2.",
        },
    },
    "assessment": [
        {
            "id": "avg_assess_1",
            "type": "mcq",
            "question": "Average of first 5 even numbers?",
            "options": [4, 5, 6, 7],
            "correct_index": 2,
            "explanation": "First 5 even numbers: 2, 4, 6, 8, 10. Sum = 30. Average = 30/5 = 6.",
        },
        {
            "id": "avg_assess_2",
            "type": "mcq",
            "question": "A cricketer scores 45, 55, 65 in 3 matches. What is his average?",
            "options": [50, 55, 60, 65],
            "correct_index": 1,
            "explanation": "Sum = 165. Average = 165/3 = 55.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Exam average",
        "problem": (
            "A student scored 78, 82, 75, 85 in 4 tests. What must they score on the 5th test "
            "to have an average of 80?"
        ),
        "steps": [
            "Target total = 80 × 5 = 400.",
            "Current total = 78 + 82 + 75 + 85 = 320.",
            "5th test = 400 - 320 = 80.",
        ],
        "answer": 80,
    },
    "deterministic_answer_key": {
        "avg_practice_1": 1,
        "avg_practice_2": 2,
        "avg_assess_1": 2,
        "avg_assess_2": 1,
        "transfer_task": 80,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/quantitative-aptitude/averages/",
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
