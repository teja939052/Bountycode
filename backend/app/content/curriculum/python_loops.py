"""
Promoted Lesson: Python Loops — For and While
============================================================

Service-company programming foundation. Follows the full content contract:

- Stable lesson ID, version, canonical skill ID
- Company relevance classification
- Learning objectives, prerequisites
- Concept explanation, worked example
- Interactive practice, misconception-specific feedback
- Assessment, transfer task, deterministic answer key
- Source/provenance metadata, review state, accessibility metadata
- Estimated time, spaced-repetition metadata

Provenance: Pattern-relevant for TCS NQT, Infosys, Wipro, Cognizant,
Capgemini, Accenture service-company technical aptitude sections.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "python_loops_01"
VERSION = "1.0.0"
SKILL_ID = "coding.loops_basics"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 15
XP_REWARD = 120

PYTHON_LOOPS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:python_loops_basics",
    "title": "Python Loops — For and While",
    "description": "Master loop constructs: for loops, while loops, loop control statements, and nested iteration.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["loops", "for_loop", "while_loop", "loop_control", "nested_loops"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Explain what a loop does and why iteration exists.",
        "Write a for loop to iterate over sequences.",
        "Write a while loop with a terminating condition.",
        "Use break and continue to control loop flow.",
        "Debug off-by-one and infinite-loop errors.",
    ],
    "prerequisites": ["cs.python_basics", "quant.number_systems"],
    # ── Discovery: concept introduction ──
    "discovery": {
        "title": "Why loops?",
        "content": (
            "A loop repeats a block of code while a condition is true, or once for each item "
            "in a sequence. Instead of writing the same code over and over, you write it once "
            "and let Python repeat it. Python has two main loop types: for loops (iterate over "
            "a sequence) and while loops (repeat while a condition is true)."
        ),
    },
    # ── Prediction: predict_output step ──
    "prediction": {
        "title": "Predict the output",
        "content": "What does this print?\nfor i in range(3):\n    print(i)",
        "options": ["0 1 2", "1 2 3", "0 1 2 3", "1 2"],
        "correct_index": 0,
        "explanation": "range(3) produces 0, 1, 2 — three values, starting at 0 and stopping before 3.",
    },
    # ── Transfer task at end of lesson ──
    "transfer_challenge": {
        "title": "Real-world: Validate user input",
        "problem": (
            "Write a loop that keeps asking the user for a number until they enter a positive "
            "number (greater than 0). Once they do, print the number and stop."
        ),
        "steps": [
            "Use a while True loop (infinite until we break).",
            "Ask for input and convert to int.",
            "If the number is greater than 0, print it and break.",
            "Otherwise, print an error message and loop again.",
        ],
        "answer": "while True:\n    n = int(input('Enter a positive number: '))\n    if n > 0:\n        print(n)\n        break\n    print('Try again.')",
    },
    # ── Guided build steps ──
    "guided_build": {
        "steps": [
            {
                "step_id": "things-1",
                "step_type": "code",
                "title": "First loop",
                "code": "for i in range(3):\n    print(i)",
                "language": "python",
                "explanation": "range(3) produces 0, 1, 2.",
            },
            {
                "step_id": "things-2",
                "step_type": "code",
                "title": "While loop",
                "code": "i = 0\nwhile i < 3:\n    print(i)\n    i += 1",
                "language": "python",
                "explanation": "while loop repeats while condition is True.",
            },
        ],
    },
    # ── Assessment ──
    "assessment": {
        "questions": [
            {
                "id": "loops_assess_1",
                "type": "mcq",
                "question": "What is printed by: for i in range(1, 4): print(i)",
                "options": ["1 2 3", "1 2 3 4", "0 1 2", "0 1 2 3"],
                "correct_index": 0,
                "explanation": "range(1, 4) produces 1, 2, 3.",
            },
            {
                "id": "loops_assess_2",
                "type": "mcq",
                "question": "Which keyword exits a loop immediately?",
                "options": ["continue", "break", "return", "pass"],
                "correct_index": 1,
                "explanation": "break exits the loop immediately.",
            },
        ],
    },
    "misconception_feedback": {
        "off_by_one": {
            "title": "Common mistake: Off-by-one errors",
            "text": "range(5) produces 0, 1, 2, 3, 4 — NOT 1, 2, 3, 4, 5. The stop value is exclusive.",
            "example": "range(1, 6) produces 1, 2, 3, 4, 5 if you need to include 5.",
        },
        "infinite_loop": {
            "title": "Common mistake: Infinite while loops",
            "text": "A while loop runs forever if its condition never becomes False. Always make sure the loop variable changes toward the exit condition.",
            "example": "while x < 5: print(x)  # Forgot x += 1 — infinite loop!",
        },
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://docs.python.org/3/tutorial/controlflow.html",
            "https://wiki.python.org/moin/Loops",
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
    "deterministic_answer_key": {
        "loops_practice_1": 0,
        "loops_practice_2": 2,
        "loops_practice_3": 1,
        "loops_assess_1": 0,
        "loops_assess_2": 1,
        "transfer_task": "while True:\n    n = int(input('Enter a positive number: '))\n    if n > 0:\n        print(n)\n        break\n    print('Try again.')",
    },
}
