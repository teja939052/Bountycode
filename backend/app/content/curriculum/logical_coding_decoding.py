"""
Promoted Lesson: Coding-Decoding
=================================

Service-company logical reasoning foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company logical reasoning sections.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "logical_coding_decoding_01"
VERSION = "1.0.0"
SKILL_ID = "logical.coding_decoding"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

CODING_DECODING_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "logical_reasoning:coding_decoding",
    "title": "Coding-Decoding",
    "description": "Master letter/number code patterns — shift codes, symbol codes, and substitution.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["letter_shift", "number_code", "symbol_substitution", "mixed_code"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Identify letter-shift (Caesar cipher) patterns.",
        "Decode number-to-letter substitution.",
        "Recognize symbol-based codes.",
        "Apply the same rule to encode/decode new words.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Coding-Decoding",
        "text": (
            "Coding transforms a word into a code using a fixed rule. Decoding reverses it. "
            "Common rules: letter shift (A→B = +1), position value (A=1, B=2), reverse alphabet, symbol substitution."
        ),
        "key_formula": "A=1, B=2, ..., Z=26. Shift +1: A→B, B→C, ...",
    },
    "worked_example": {
        "title": "Letter shift code",
        "problem": "If CAT is coded as DBU, how is DOG coded?",
        "steps": [
            "C→D (+1), A→B (+1), T→U (+1). Rule: shift each letter +1.",
            "D→E, O→P, G→H.",
            "DOG = EPH.",
        ],
        "answer": "EPH",
    },
    "interactive_practice": [
        {
            "id": "cd_practice_1",
            "type": "mcq",
            "question": "If A=1, B=2, what is CODE?",
            "options": ["31545", "31455", "31554", "35145"],
            "correct_index": 0,
            "explanation": "C=3, O=15, D=4, E=5 → 31545.",
        },
        {
            "id": "cd_practice_2",
            "type": "mcq",
            "question": "If HELP is coded as 8-5-12-16, what is the code for WORK?",
            "options": ["23-15-18-11", "23-15-18-12", "23-15-17-11", "22-15-18-11"],
            "correct_index": 0,
            "explanation": "W=23, O=15, R=18, K=11 → 23-15-18-11.",
        },
    ],
    "misconception_feedback": {
        "position_vs_shift": {
            "title": "Common mistake: Confusing position value with shift",
            "text": "Position value (A=1) replaces letters with numbers. Shift (+1) changes letters to other letters.",
        },
    },
    "assessment": [
        {
            "id": "cd_assess_1",
            "type": "mcq",
            "question": "If DOG is coded as EPH (shift +1), how is CAT coded?",
            "options": ["DBU", "ECV", "DBS", "DAU"],
            "correct_index": 0,
            "explanation": "C→D, A→B, T→U → DBU.",
        },
        {
            "id": "cd_assess_2",
            "type": "mcq",
            "question": "If SUN = 19-21-14 (position values), what is MOON?",
            "options": ["13-15-15-14", "13-15-14-14", "12-15-15-14", "13-14-15-14"],
            "correct_index": 0,
            "explanation": "M=13, O=15, O=15, N=14 → 13-15-15-14.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Secret message",
        "problem": (
            "Decode: 8-5-12-12-15 using position values (A=1, B=2, ...)."
        ),
        "steps": [
            "8 = H, 5 = E, 12 = L, 12 = L, 15 = O.",
            "Word: HELLO.",
        ],
        "answer": "HELLO",
    },
    "deterministic_answer_key": {
        "cd_practice_1": 0,
        "cd_practice_2": 0,
        "cd_assess_1": 0,
        "cd_assess_2": 0,
        "transfer_task": "HELLO",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/logical-reasoning/coding-decoding/",
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
