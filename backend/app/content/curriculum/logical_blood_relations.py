"""
Promoted Lesson: Blood Relations
================================

Service-company logical reasoning foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company logical reasoning sections.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "logical_blood_relations_01"
VERSION = "1.0.0"
SKILL_ID = "logical.blood_relations"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

BLOOD_RELATIONS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "logical_reasoning:blood_relations",
    "title": "Blood Relations",
    "description": "Master family relationship puzzles — decode 'A is B's father' style statements.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["direct_relations", "indirect_relations", "family_tree", "coded_relations"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Decode direct relation statements ('A is B's mother').",
        "Build a family tree from multiple statements.",
        "Answer 'How is X related to Y?' questions.",
        "Handle gender-neutral and coded relation symbols.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Blood Relations",
        "text": (
            "Blood relation questions describe family connections. Key terms: father/mother "
            "(parents), son/daughter (children), brother/sister (siblings), husband/wife (spouse), "
            "grandfather/grandmother (grandparents), grandson/granddaughter (grandchildren), "
            "uncle/aunt (parents' siblings), cousin (siblings' children). Draw a tree diagram."
        ),
        "key_formula": "Draw generations top-down; connect spouse horizontally, parent-child vertically.",
    },
    "worked_example": {
        "title": "Pointing to a photograph",
        "problem": "Pointing to a photo, Ravi says: 'She is the daughter of my grandfather's only son.' How is she related to Ravi?",
        "steps": [
            "Ravi's grandfather's only son = Ravi's father (or Ravi himself if only child).",
            "If Ravi's father: daughter of Ravi's father = Ravi's sister.",
            "If Ravi himself: daughter of Ravi = Ravi's daughter.",
            "Standard interpretation: she is Ravi's sister.",
        ],
        "answer": "Sister",
    },
    "interactive_practice": [
        {
            "id": "br_practice_1",
            "type": "mcq",
            "question": "A is B's father. C is A's daughter. How is C related to B?",
            "options": ["Sister", "Daughter", "Mother", "Aunt"],
            "correct_index": 0,
            "explanation": "A is B's father. C is A's daughter, so C is B's sister (or B herself). Standard: Sister.",
        },
        {
            "id": "br_practice_2",
            "type": "mcq",
            "question": "X is Y's mother. Z is Y's father. How is Z related to X?",
            "options": ["Husband", "Wife", "Brother", "Father"],
            "correct_index": 0,
            "explanation": "If X is Y's mother and Z is Y's father, Z is X's husband.",
        },
    ],
    "misconception_feedback": {
        "assume_gender": {
            "title": "Common mistake: Assuming gender from name",
            "text": "Don't assume gender from names unless stated. Use the explicit relation words (mother/father/sister/brother).",
        },
    },
    "assessment": [
        {
            "id": "br_assess_1",
            "type": "mcq",
            "question": "P is Q's brother. R is P's mother. How is R related to Q?",
            "options": ["Mother", "Sister", "Daughter", "Aunt"],
            "correct_index": 0,
            "explanation": "R is P's mother, and P is Q's brother, so R is Q's mother.",
        },
        {
            "id": "br_assess_2",
            "type": "mcq",
            "question": "M is N's son. O is M's sister. How is O related to N?",
            "options": ["Son", "Daughter", "Brother", "Father"],
            "correct_index": 1,
            "explanation": "O is M's sister, so O is also N's child → N's daughter.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Family introduction",
        "problem": (
            "At a party, Sita says: 'He is the only son of my mother's mother.' "
            "How is he related to Sita?"
        ),
        "steps": [
            "Sita's mother's mother = Sita's maternal grandmother.",
            "Grandmother's only son = Sita's maternal uncle (mother's brother).",
            "He is Sita's maternal uncle.",
        ],
        "answer": "Maternal uncle",
    },
    "deterministic_answer_key": {
        "br_practice_1": 0,
        "br_practice_2": 0,
        "br_assess_1": 0,
        "br_assess_2": 1,
        "transfer_task": "Maternal uncle",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/logical-reasoning/blood-relations/",
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
