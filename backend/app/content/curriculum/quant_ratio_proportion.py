"""
Promoted Lesson: Ratio and Proportion
=====================================

Service-company quantitative aptitude foundation. Follows the full content contract.

Provenance: Pattern-relevant for TCS NQT, Infosys, Wipro, Cognizant, Capgemini,
Accenture service-company quantitative aptitude sections.
"""
from typing import Dict, List, Any

LESSON_ID = "quant_ratio_proportion_01"
VERSION = "1.0.0"
SKILL_ID = "quant.ratio_proportion"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

RATIO_PROPORTION_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "quantitative_aptitude:ratio_proportion",
    "title": "Ratio and Proportion",
    "description": "Master ratios, proportions, and their applications in aptitude problems.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["ratios", "proportions", "direct_proportion", "inverse_proportion", "mixtures"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Express and simplify ratios.",
        "Divide quantities in a given ratio.",
        "Solve proportion problems (a:b = c:d).",
        "Apply direct and inverse proportion.",
        "Solve mixture and alligation problems.",
    ],
    "prerequisites": ["quant.percentages", "quant.fractions_decimals"],
    "concept_explanation": {
        "title": "Ratio and Proportion",
        "text": (
            "A ratio compares two quantities of the same kind, written as a:b or a/b. "
            "A proportion states that two ratios are equal: a:b = c:d, which means ad = bc."
        ),
        "key_formula": "If a:b = c:d, then ad = bc (cross-multiplication).",
    },
    "worked_example": {
        "title": "Divide ₹1,200 in ratio 3:2",
        "problem": "Divide ₹1,200 between A and B in the ratio 3:2.",
        "steps": [
            "Total parts = 3 + 2 = 5 parts.",
            "Value of one part = 1200 / 5 = ₹240.",
            "A's share = 3 × 240 = ₹720.",
            "B's share = 2 × 240 = ₹480.",
        ],
        "answer": {"A": 720, "B": 480},
    },
    "interactive_practice": [
        {
            "id": "ratio_practice_1",
            "type": "mcq",
            "question": "The ratio of boys to girls in a class is 3:5. If there are 24 boys, how many girls?",
            "options": [30, 35, 40, 45],
            "correct_index": 2,
            "explanation": "3 parts = 24 boys, so 1 part = 8. Girls = 5 × 8 = 40.",
        },
        {
            "id": "ratio_practice_2",
            "type": "mcq",
            "question": "If 5:7 = x:21, find x.",
            "options": [10, 15, 20, 25],
            "correct_index": 1,
            "explanation": "5/7 = x/21, so x = 5 × 21 / 7 = 15.",
        },
    ],
    "misconception_feedback": {
        "ratio_order_matters": {
            "title": "Common mistake: Ignoring order in ratios",
            "text": "Ratio 3:2 is not the same as 2:3. Order matters — 3:2 means 3 parts of the first to 2 parts of the second.",
        },
        "cross_multiplication": {
            "title": "Common mistake: Incorrect cross-multiplication",
            "text": "For a:b = c:d, the cross-product is a×d = b×c, NOT a×c = b×d.",
        },
    },
    "assessment": [
        {
            "id": "ratio_assess_1",
            "type": "mcq",
            "question": "₹900 is divided between two people in ratio 4:5. What is the smaller share?",
            "options": [300, 400, 450, 500],
            "correct_index": 1,
            "explanation": "Total parts = 9. One part = 100. Smaller share = 4 × 100 = 400.",
        },
        {
            "id": "ratio_assess_2",
            "type": "mcq",
            "question": "If a:b = 2:3 and b:c = 4:5, find a:c.",
            "options": ["8:15", "6:15", "2:5", "1:2"],
            "correct_index": 0,
            "explanation": "Make b common: a:b = 8:12, b:c = 12:15. So a:c = 8:15.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Recipe scaling",
        "problem": (
            "A recipe for 4 people needs 2 cups flour, 1 cup sugar, 3 eggs. "
            "How much flour is needed for 10 people?"
        ),
        "steps": [
            "Flour per person = 2 / 4 = 0.5 cups.",
            "For 10 people: 0.5 × 10 = 5 cups.",
        ],
        "answer": 5,
    },
    "deterministic_answer_key": {
        "ratio_practice_1": 2,
        "ratio_practice_2": 1,
        "ratio_assess_1": 1,
        "ratio_assess_2": 0,
        "transfer_task": 5,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/quantitative-aptitude/ratio-and-proportion/",
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
