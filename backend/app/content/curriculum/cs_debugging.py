"""
Promoted Lesson: Debugging
==========================

Service-company technical foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company technical aptitude.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "cs_debugging_01"
VERSION = "1.0.0"
SKILL_ID = "cs.debugging"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

DEBUGGING_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:debugging",
    "title": "Debugging",
    "description": "Master systematic debugging — read errors, trace logic, use print/logging, isolate bugs.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["read_error_messages", "trace_code", "print_debugging", "isolate_bugs"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Read and interpret error messages and stack traces.",
        "Trace code execution step by step.",
        "Use print statements to isolate bugs.",
        "Identify off-by-one and null-reference errors.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Debugging Fundamentals",
        "text": (
            "Debugging is the systematic process of finding and fixing defects. Start by reading "
            "the error message — it tells you what went wrong and where. Then trace execution "
            "to find why, and isolate the bug with targeted prints or logs."
        ),
        "key_formula": "Read error → Trace execution → Isolate → Fix → Verify.",
    },
    "worked_example": {
        "title": "Off-by-one error",
        "problem": "Find the bug: for i in range(len(arr)): print(arr[i+1])",
        "bug": "IndexError when i = len(arr)-1, because arr[i+1] goes out of bounds.",
        "fix": "Change to arr[i] or range(len(arr)-1).",
        "explanation": "When i reaches the last index, i+1 exceeds the array length.",
    },
    "interactive_practice": [
        {
            "id": "dbg_practice_1",
            "type": "mcq",
            "question": "NameError in Python means what?",
            "options": ["Wrong type", "Undefined variable", "Wrong indentation", "Wrong import"],
            "correct_index": 1,
            "explanation": "NameError means a variable/function name is not defined.",
        },
        {
            "id": "dbg_practice_2",
            "type": "mcq",
            "question": "IndexError means what?",
            "options": ["Wrong key", "Out-of-bounds index", "Division by zero", "File missing"],
            "correct_index": 1,
            "explanation": "IndexError means accessing an index outside the valid range.",
        },
    ],
    "misconception_feedback": {
        "error_line_is_not_always_bug_line": {
            "title": "Common mistake: Assuming the error line is where the bug is",
            "text": "The error line is where Python detected the problem, not necessarily where you introduced it. Trace backward.",
        },
    },
    "assessment": [
        {
            "id": "dbg_assess_1",
            "type": "mcq",
            "question": "Which tool shows the call stack at crash time?",
            "options": ["print()", "traceback", "input()", "len()"],
            "correct_index": 1,
            "explanation": "traceback shows the call stack leading to the error.",
        },
        {
            "id": "dbg_assess_2",
            "type": "mcq",
            "question": "Best first step when code crashes?",
            "options": ["Rewrite everything", "Read the error message", "Ignore it", "Restart computer"],
            "correct_index": 1,
            "explanation": "Read the error message first — it contains the answer most of the time.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Find the off-by-one",
        "problem": (
            "Code: for i in range(1, n+1): total += arr[i]. "
            "It crashes with IndexError when n = len(arr). Why?"
        ),
        "steps": [
            "range(1, n+1) produces 1 to n.",
            "When i = n, arr[n] is out of bounds (valid indices: 0 to n-1).",
            "Fix: use range(n) or arr[i-1].",
        ],
        "answer": "arr[n] is out of bounds; array indices go from 0 to n-1.",
    },
    "deterministic_answer_key": {
        "dbg_practice_1": 1,
        "dbg_practice_2": 1,
        "dbg_assess_1": 1,
        "dbg_assess_2": 1,
        "transfer_task": "arr[n] is out of bounds; array indices go from 0 to n-1.",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://wiki.python.org/moin/Debugging",
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
