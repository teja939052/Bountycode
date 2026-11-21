"""
Promoted Lesson: Percentages
=============================

Service-company quantitative aptitude foundation. Follows the full content contract:

- Stable lesson ID, version, canonical skill ID
- Company relevance classification
- Learning objectives, prerequisites
- Concept explanation, worked example
- Interactive practice, misconception-specific feedback
- Assessment, transfer task, deterministic answer key
- Source/provenance metadata, review state, accessibility metadata
- Estimated time, spaced-repetition metadata

Provenance: Pattern-relevant for TCS NQT, Infosys, Wipro, Cognizant, Capgemini,
Accenture service-company quantitative aptitude sections. Not a claim about any
private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "quant_percentages_01"
VERSION = "1.0.0"
SKILL_ID = "quant.percentages"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

PERCENTAGES_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "quantitative_aptitude:percentages",
    "title": "Percentages",
    "description": "Master percentage calculations — the foundation of service-company aptitude tests.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["percentages", "percentage_change", "profit_loss", "discounts"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Convert between percentages, fractions, and decimals.",
        "Calculate x% of a number.",
        "Find what percentage one number is of another.",
        "Compute percentage increase and decrease.",
        "Solve profit, loss, and discount problems using percentages.",
    ],
    "prerequisites": ["quant.number_systems_basics", "quant.fractions_decimals"],
    "concept_explanation": {
        "title": "What is a Percentage?",
        "text": (
            "A percentage expresses a number as a fraction of 100. The symbol % means "
            "\"per hundred\". So 25% = 25/100 = 0.25. Percentages are used everywhere in "
            "aptitude tests: marks, profit, loss, discounts, population growth, and more."
        ),
        "key_formula": "x% of N = (x / 100) × N",
    },
    "worked_example": {
        "title": "Find 15% of 240",
        "problem": "What is 15% of 240?",
        "steps": [
            "Write 15% as a fraction: 15/100 = 0.15.",
            "Multiply: 0.15 × 240 = 36.",
            "Answer: 36.",
        ],
        "answer": 36,
    },
    "interactive_practice": [
        {
            "id": "pct_practice_1",
            "type": "mcq",
            "question": "What is 20% of 150?",
            "options": [25, 30, 35, 40],
            "correct_index": 1,
            "explanation": "20% of 150 = 0.20 × 150 = 30.",
        },
        {
            "id": "pct_practice_2",
            "type": "mcq",
            "question": "If 40% of a number is 80, what is the number?",
            "options": [150, 200, 250, 300],
            "correct_index": 1,
            "explanation": "Let the number be x. 0.40 × x = 80, so x = 80 / 0.40 = 200.",
        },
    ],
    "misconception_feedback": {
        "confusing_percent_with_fraction": {
            "title": "Common mistake: Treating % as the number itself",
            "text": "25% is not 25 — it is 25/100 = 0.25. Always divide by 100 before multiplying.",
            "example": "25% of 200 = 0.25 × 200 = 50, NOT 25 × 200 = 5000.",
        },
        "percentage_point_vs_percent": {
            "title": "Common mistake: Percentage points vs percent change",
            "text": "Going from 20% to 25% is a 5 percentage-point increase, but a 25% relative increase ((25-20)/20 × 100).",
        },
    },
    "assessment": [
        {
            "id": "pct_assess_1",
            "type": "mcq",
            "question": "A shirt costs ₹800. It is on sale at 25% off. What is the sale price?",
            "options": [600, 650, 700, 750],
            "correct_index": 0,
            "explanation": "25% of 800 = 200. Sale price = 800 - 200 = ₹600.",
        },
        {
            "id": "pct_assess_2",
            "type": "mcq",
            "question": "Population increased from 50,000 to 60,000. What is the percentage increase?",
            "options": [10, 20, 25, 30],
            "correct_index": 1,
            "explanation": "Increase = 10,000. % increase = (10,000 / 50,000) × 100 = 20%.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Shopping discount",
        "problem": (
            "You buy three items: a shirt for ₹600 (30% off), jeans for ₹1,200 (20% off), "
            "and a belt for ₹400 (no discount). What is the total amount you pay?"
        ),
        "steps": [
            "Shirt: 30% of 600 = 180 off. Pay 600 - 180 = 420.",
            "Jeans: 20% of 1200 = 240 off. Pay 1200 - 240 = 960.",
            "Belt: No discount. Pay 400.",
            "Total: 420 + 960 + 400 = 1780.",
        ],
        "answer": 1780,
    },
    "deterministic_answer_key": {
        "pct_practice_1": 1,
        "pct_practice_2": 1,
        "pct_assess_1": 0,
        "pct_assess_2": 1,
        "transfer_task": 1780,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/quantitative-aptitude/percentages/",
            "https://www.geeksforgeeks.org/percentage-questions/",
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
