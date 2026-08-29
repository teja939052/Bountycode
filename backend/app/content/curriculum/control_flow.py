"""
Vertical Slice: Control Flow
===========================

A fully authored game-based learning experience for the concept:
  decisions (conditions) and repetition (loops)

Path: SDE -> Programming Foundations -> Control Flow

This is the SECOND foundation slice. It follows the exact same simulation
loop as the Memory Palace (variables_state) so the LessonPage frontend can
render either lesson generically by slug:
  story_context -> discovery -> prediction -> guided_build ->
  immediate_feedback -> scaffolded_hints -> transfer_challenge ->
  mastery -> srs_enrollment
"""
from typing import Dict, List, Any

CONTROL_FLOW_SLICE = {
    "lesson_id": "control_flow_forking_path",
    "module_id": "programming_fundamentals:control_flow",
    "title": "The Forking Path",
    "description": "Learn how a program chooses a path and repeats steps by walking the branching garden.",
    "difficulty": "beginner",
    "est_minutes": 10,
    "xp_reward": 180,
    "skills_taught": ["conditionals", "branching", "loops", "iteration"],
    "srs_concept_tag": "programming_fundamentals:control_flow",
    "story_context": {
        "title": "The Forking Path",
        "narration": (
            "Beyond the Memory Palace lies a garden of living paths. Each path splits: "
            "go left if the gate is open, go right if it is shut. Some paths repeat, "
            "lighting one lantern after another until the row is complete. "
            "Your job: become the Pathkeeper who decides where the traveller goes."
        ),
        "setting": "forking_path",
        "character": "Pathkeeper",
        "intro_text": (
            "Welcome, Pathkeeper. I am the garden guide. Here, code makes choices. "
            "A condition is a gate; a loop is a lantern row that lights itself again and again. "
            "Let me show you how a program decides and repeats."
        ),
    },
    "discovery": {
        "title": "Gates and Lantern Rows",
        "steps": [
            {
                "action": "inspect_condition",
                "room_name": "gate",
                "room_value": "open",
                "narration": (
                    "This gate checks one thing: is the traveller old enough? "
                    "If yes, the left path opens. Code expresses this with 'if'."
                ),
                "interaction": {
                    "type": "reveal_value",
                    "prompt": "What do you think happens when the condition is false?",
                    "reveal_after": "The program skips the indented block and takes the 'else' path.",
                },
            },
            {
                "action": "type_inspection",
                "room_name": "choice",
                "room_value": "left",
                "narration": (
                    "A condition compares values. Here we test if age is at least 18. "
                    "The result is either True or False — a boolean."
                ),
                "interaction": {
                    "type": "inspect_type",
                    "code": 'age = 20\nprint(age >= 18)',
                    "expected_output": "True",
                    "hint": ">= means 'greater than or equal to'. The comparison returns a bool.",
                },
            },
            {
                "action": "loop_observation",
                "room_name": "lanterns",
                "room_value": "row of 3",
                "narration": (
                    "Instead of writing the same line three times, a loop lights each lantern "
                    "in turn. 'for' walks a fixed collection; 'while' repeats while a condition holds."
                ),
                "interaction": {
                    "type": "inspect_type",
                    "code": 'for i in range(3):\n    print("lantern", i)',
                    "expected_output": "lantern 0\nlantern 1\nlantern 2",
                    "hint": "range(3) produces 0, 1, 2. The loop body runs once per value.",
                },
            },
        ],
        "conclusion": (
            "Conditions (if/elif/else) let a program choose. Loops (for/while) let it repeat. "
            "Together they turn a straight line of code into a branching, cycling journey."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What will this code print?",
        "code": 'x = 5\nif x > 3:\n    x = x * 2\nelse:\n    x = x + 1\nprint(x)',
        "options": [
            {"id": "a", "text": "10", "correct": True, "explanation": "x=5 is greater than 3, so x becomes 5*2 = 10"},
            {"id": "b", "text": "6", "correct": False, "explanation": "6 would be the result if the else branch ran (5+1), but the if branch is taken"},
            {"id": "c", "text": "5", "correct": False, "explanation": "x is reassigned inside the taken branch, so it is no longer 5"},
            {"id": "d", "text": "Error", "correct": False, "explanation": "This code is valid Python — no error occurs"},
        ],
        "explanation": (
            "The condition x > 3 is True (5 > 3), so the if-branch runs and x becomes 10. "
            "The else-branch is skipped entirely."
        ),
    },
    "guided_build": {
        "title": "Build Your First Decisions and Loops",
        "steps": [
            {
                "step_order": 1,
                "title": "Grade Classifier",
                "description": "Use if/elif/else to turn a numeric score into a letter grade.",
                "starter_code": 'def classify(score):\n    # TODO: return "A" if >=90, "B" if >=80, "C" if >=70,\n    # "D" if >=60, else "F"\n    pass',
                "function_name": "classify",
                "signature": "def classify(score: int) -> str:",
                "test_cases": [
                    {"input": [95], "expected": "A"},
                    {"input": [85], "expected": "B"},
                    {"input": [72], "expected": "C"},
                    {"input": [61], "expected": "D"},
                    {"input": [50], "expected": "F"},
                ],
                "hidden_test_cases": [
                    {"input": [100], "expected": "A"},
                    {"input": [89], "expected": "B"},
                    {"input": [70], "expected": "C"},
                    {"input": [60], "expected": "D"},
                    {"input": [0], "expected": "F"},
                ],
                "xp": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Start with the highest threshold: if score >= 90: return 'A'"},
                    {"level": 2, "text": "Chain downward with elif for 80, 70, 60, then a final else for 'F'."},
                    {"level": 3, "text": "Order matters — check the largest first, otherwise 95 would match the 80 branch."},
                ],
            },
            {
                "step_order": 2,
                "title": "Countdown with a While Loop",
                "description": "Build a list counting down from n to 1 using a while loop.",
                "starter_code": 'def countdown(n):\n    # TODO: return a list of integers from n down to 1\n    # e.g. countdown(5) -> [5, 4, 3, 2, 1]\n    pass',
                "function_name": "countdown",
                "signature": "def countdown(n: int) -> list:",
                "test_cases": [
                    {"input": [5], "expected": [5, 4, 3, 2, 1]},
                    {"input": [3], "expected": [3, 2, 1]},
                    {"input": [1], "expected": [1]},
                ],
                "hidden_test_cases": [
                    {"input": [10], "expected": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]},
                    {"input": [2], "expected": [2, 1]},
                    {"input": [0], "expected": []},
                ],
                "xp": 55,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use result = [] and a while n > 0: loop."},
                    {"level": 2, "text": "Inside the loop: append n, then do n -= 1 to move toward the stop condition."},
                    {"level": 3, "text": "If you forget n -= 1 the condition stays True forever (an infinite loop)."},
                ],
            },
            {
                "step_order": 3,
                "title": "Triangle of Stars",
                "description": "Use a for loop to build a right-angled triangle of stars.",
                "starter_code": 'def triangle(n):\n    # TODO: return a list of strings, row i has i stars\n    # e.g. triangle(3) -> ["*", "**", "***"]\n    pass',
                "function_name": "triangle",
                "signature": "def triangle(n: int) -> list:",
                "test_cases": [
                    {"input": [3], "expected": ["*", "**", "***"]},
                    {"input": [1], "expected": ["*"]},
                    {"input": [0], "expected": []},
                ],
                "hidden_test_cases": [
                    {"input": [5], "expected": ["*", "**", "***", "****", "*****"]},
                    {"input": [4], "expected": ["*", "**", "***", "****"]},
                    {"input": [2], "expected": ["*", "**"]},
                ],
                "xp": 60,
                "scaffolded_hints": [
                    {"level": 1, "text": "Loop with for i in range(1, n + 1):"},
                    {"level": 2, "text": "Build each row with '*' * i and append it to a list."},
                    {"level": 3, "text": "range(1, n+1) gives 1..n inclusive, which matches the row counts."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The FizzBuzz Grove",
        "description": (
            "Combine conditions AND loops: light the lanterns of a grove where every third "
            "lantern is 'Fizz', every fifth is 'Buzz', and every fifteenth is 'FizzBuzz'."
        ),
        "function_name": "fizzbuzz",
        "signature": "def fizzbuzz(n: int) -> list:",
        "starter_code": 'def fizzbuzz(n):\n    # TODO: return a list of n strings.\n    # For i in 1..n: if i % 15 == 0 -> "FizzBuzz",\n    # elif i % 3 == 0 -> "Fizz", elif i % 5 == 0 -> "Buzz", else str(i)\n    pass',
        "description_full": (
            "Return a list of n strings, one per integer i from 1 to n.\n"
            "Rule: if i is divisible by 3 AND 5 -> 'FizzBuzz'; else if divisible by 3 -> 'Fizz'; "
            "else if divisible by 5 -> 'Buzz'; otherwise the number as a string.\n\n"
            "This is the classic test of whether you can combine a loop with branching correctly."
        ),
        "test_cases": [
            {
                "input": [5],
                "expected": ["1", "2", "Fizz", "4", "Buzz"],
            },
            {
                "input": [15],
                "expected": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"],
            },
        ],
        "hidden_test_cases": [
            {"input": [10], "expected": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz"]},
            {"input": [20], "expected": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz", "16", "17", "Fizz", "19", "Buzz"]},
            {"input": [3], "expected": ["1", "2", "Fizz"]},
        ],
        "time_limit_minutes": 8,
        "xp": 120,
        "scaffolded_hints": [
            {"level": 1, "text": "Use result = [] and for i in range(1, n + 1):"},
            {"level": 2, "text": "Check the combined condition i % 15 == 0 FIRST, then % 3, then % 5."},
            {"level": 3, "text": "Order is critical: test FizzBuzz before Fizz/Buzz, or you'll never reach it."},
        ],
    },
    "assessment": {
        "title": "Forking Path Final Challenge",
        "description": (
            "You are the Pathkeeper. A program branches and loops. Predict and repair its behaviour."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": 'for i in range(3):\n    i = i * 2\nprint(i)',
                "answer_format": "final value of i?",
                "expected_answer": "2",
                "explanation": (
                    "range(3) yields 0, 1, 2. Inside the loop i is doubled, but the next iteration "
                    "re-assigns i to the next value from range. After the last iteration i is 2."
                ),
            },
            {
                "type": "concept",
                "question": "When would you choose a while loop instead of a for loop?",
                "answer_format": "short_answer",
                "keywords": ["unknown", "condition", "until", "dynamic"],
                "explanation": (
                    "A for loop is best when you know the number of iterations (e.g. over a list or range). "
                    "A while loop is best when repetition depends on a condition that may change unpredictably, "
                    "such as 'keep going until the user types quit'."
                ),
            },
            {
                "type": "debug",
                "code": 'def is_even(n):\n    if n % 2 = 0:\n        return True\n    return False\n\nprint(is_even(4))',
                "error": "SyntaxError: invalid syntax",
                "question": "Fix the bug.",
                "fix": 'if n % 2 == 0:',
                "explanation": "Comparison uses == not =. A single = is assignment, which is not allowed in an if condition.",
            },
        ],
        "mastery_threshold": 70,
        "xp": 180,
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:control_flow",
        "concept_name": "Control Flow",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "if / elif / else choose between paths based on a boolean condition",
            "Conditions use comparison operators (==, !=, <, >, <=, >=)",
            "for loops iterate over a known collection or range",
            "while loops repeat while a condition stays True — always make progress toward stopping",
            "Check the most specific / combined condition first (e.g. FizzBuzz before Fizz)",
        ],
        "spaced_fields": [
            "if_elif_else",
            "comparison_operators",
            "for_loop_range",
            "while_loop_progress",
            "branch_ordering",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "control_flow",
        "unlocks_next": ["functions", "data_types"],
        "tower_badge": "first_control_flow",
        "world_node": {
            "level": 2,
            "title": "The Forking Path",
            "color": "green",
            "icon": "🌿",
            "description": "Decide which path code takes with conditions and loops",
        },
    },
}
