"""
Promoted Lesson: Number Systems
===============================

Service-company quantitative aptitude foundation. Follows the full content contract.

Provenance: Pattern-relevant for TCS NQT, Infosys, Wipro, Cognizant, Capgemini,
Accenture service-company quantitative aptitude sections.
"""
from typing import Dict, List, Any

LESSON_ID = "quant_number_systems_01"
VERSION = "1.0.0"
SKILL_ID = "quant.number_systems"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

NUMBER_SYSTEMS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "quantitative_aptitude:number_systems",
    "title": "Number Systems",
    "description": "Master number properties — divisibility, HCF, LCM, remainders, and digits.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["divisibility", "hcf_lcm", "remainders", "unit_digit", "factors"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Apply divisibility rules for 2, 3, 5, 9, 11.",
        "Compute HCF (GCD) and LCM of two numbers.",
        "Find remainders using modular arithmetic.",
        "Find the unit digit of large powers.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Number Systems",
        "text": (
            "Number properties are the building blocks of aptitude questions. HCF is the largest "
            "number that divides both; LCM is the smallest number divisible by both. HCF × LCM = product of the two numbers."
        ),
        "key_formula": "HCF(a,b) × LCM(a,b) = a × b.",
    },
    "worked_example": {
        "title": "HCF and LCM of 12 and 18",
        "problem": "Find HCF and LCM of 12 and 18.",
        "steps": [
            "12 = 2² × 3, 18 = 2 × 3².",
            "HCF = 2 × 3 = 6 (common factors with lowest powers).",
            "LCM = 2² × 3² = 36 (all factors with highest powers).",
            "Check: 6 × 36 = 216 = 12 × 18.",
        ],
        "answer": {"hcf": 6, "lcm": 36},
    },
    "interactive_practice": [
        {
            "id": "ns_practice_1",
            "type": "mcq",
            "question": "Which number is divisible by 9? 123, 234, 345, 456",
            "options": [123, 234, 345, 456],
            "correct_index": 1,
            "explanation": "A number is divisible by 9 if the sum of its digits is divisible by 9. 2+3+4=9, so 234 works.",
        },
        {
            "id": "ns_practice_2",
            "type": "mcq",
            "question": "LCM of 4 and 6?",
            "options": [12, 24, 8, 10],
            "correct_index": 0,
            "explanation": "Multiples of 4: 4,8,12... Multiples of 6: 6,12... LCM = 12.",
        },
    ],
    "misconception_feedback": {
        "hcf_vs_lcm": {
            "title": "Common mistake: Confusing HCF and LCM",
            "text": "HCF is always smaller than or equal to the smaller number. LCM is always larger than or equal to the larger number.",
        },
    },
    "assessment": [
        {
            "id": "ns_assess_1",
            "type": "mcq",
            "question": "HCF of 24 and 36?",
            "options": [6, 8, 12, 24],
            "correct_index": 2,
            "explanation": "24 = 2³ × 3, 36 = 2² × 3². HCF = 2² × 3 = 12.",
        },
        {
            "id": "ns_assess_2",
            "type": "mcq",
            "question": "Remainder when 23 is divided by 5?",
            "options": [1, 2, 3, 4],
            "correct_index": 2,
            "explanation": "23 = 4 × 5 + 3. Remainder = 3.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Scheduling",
        "problem": (
            "Two bells ring every 6 minutes and 8 minutes respectively. If they ring together now, "
            "after how many minutes will they ring together again?"
        ),
        "steps": [
            "Find LCM of 6 and 8.",
            "6 = 2 × 3, 8 = 2³.",
            "LCM = 2³ × 3 = 24.",
            "They ring together again after 24 minutes.",
        ],
        "answer": 24,
    },
    "deterministic_answer_key": {
        "ns_practice_1": 1,
        "ns_practice_2": 0,
        "ns_assess_1": 2,
        "ns_assess_2": 2,
        "transfer_task": 24,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/quantitative-aptitude/number-system/",
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
