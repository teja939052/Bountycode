"""
Promoted Lesson: Arrays and Strings
===================================

Service-company DSA foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company coding assessments.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "dsa_arrays_strings_01"
VERSION = "1.0.0"
SKILL_ID = "dsa.arrays_strings"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 15
XP_REWARD = 120

ARRAYS_STRINGS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "data_structures:arrays_strings",
    "title": "Arrays and Strings",
    "description": "Master linear data structures — array traversal, string manipulation, two-pointer technique.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["array_traversal", "string_manipulation", "two_pointer", "linear_search"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Traverse an array with index-based loops.",
        "Perform basic string operations (concat, slice, search).",
        "Apply two-pointer technique for sorted arrays.",
        "Implement linear search.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Arrays and Strings",
        "text": (
            "An array stores elements in contiguous memory, accessible by index (0-based). "
            "Strings are sequences of characters. Two-pointer technique uses two indices "
            "moving toward each other or in the same direction to solve problems efficiently."
        ),
        "key_formula": "Array index: 0 to n-1. String: immutable sequence of chars.",
    },
    "worked_example": {
        "title": "Linear search",
        "problem": "Find if 7 exists in [3, 7, 2, 9, 1].",
        "code": "arr = [3, 7, 2, 9, 1]\ntarget = 7\nfor i in range(len(arr)):\n    if arr[i] == target:\n        print(f\"Found at index {i}\")\n        break",
        "explanation": "Loop checks each element. 7 is found at index 1.",
    },
    "interactive_practice": [
        {
            "id": "ds_practice_1",
            "type": "mcq",
            "question": "What is the index of the first element in an array?",
            "options": [0, 1, -1, None],
            "correct_index": 0,
            "explanation": "Arrays are 0-indexed — the first element is at index 0.",
        },
        {
            "id": "ds_practice_2",
            "type": "mcq",
            "question": "Which operation finds a character in a string?",
            "options": ["push", "pop", "find/index", "append"],
            "correct_index": 2,
            "explanation": "find() or index() locates a character/substring in a string.",
        },
    ],
    "misconception_feedback": {
        "string_immutability": {
            "title": "Common mistake: Assuming strings are mutable",
            "text": "In Python, strings are immutable — you cannot change a character in place. Create a new string instead.",
        },
    },
    "assessment": [
        {
            "id": "ds_assess_1",
            "type": "mcq",
            "question": "Time complexity of linear search?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
            "correct_index": 2,
            "explanation": "Linear search checks each element once — O(n).",
        },
        {
            "id": "ds_assess_2",
            "type": "mcq",
            "question": "len(\"hello\") returns?",
            "options": ["4", "5", "6", "Error"],
            "correct_index": 1,
            "explanation": "\"hello\" has 5 characters.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Find duplicate",
        "problem": (
            "Given a list of usernames, find if any username appears more than once "
            "using a single pass."
        ),
        "code": "seen = set()\nfor name in usernames:\n    if name in seen:\n        print(f\"Duplicate: {name}\")\n        break\n    seen.add(name)",
    },
    "deterministic_answer_key": {
        "ds_practice_1": 0,
        "ds_practice_2": 2,
        "ds_assess_1": 2,
        "ds_assess_2": 1,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.geeksforgeeks.org/arrays/",
            "https://wiki.python.org/moin/Strings",
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
        "initial_interval_days": 2,
        "ease_factor": 2.5,
        "retention_target": 0.85,
    },
}
