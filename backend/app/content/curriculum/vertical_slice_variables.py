"""
Vertical Slice: Variables & State
=================================

A fully authored game-based learning experience for the concept:
  variables and mutable program state

Path: SDE → Programming Foundations → Variables/State

The mission follows the simulation loop:
  story_context → discovery → prediction → guided_build →
  immediate_feedback → scaffolded_hints → transfer_challenge → mastery → srs_enrollment
"""
from typing import Dict, List, Any

VERTICAL_SLICE = {
    "lesson_id": "variables_state_memory_palace",
    "module_id": "programming_fundamentals:variables",
    "title": "Memory Palace",
    "description": "Discover how a computer stores data by exploring memory as a palace of rooms.",
    "difficulty": "beginner",
    "est_minutes": 8,
    "xp_reward": 150,
    "skills_taught": ["variables", "memory_model", "assignment", "type_checking"],
    "srs_concept_tag": "programming_fundamentals:variables",
    "story_context": {
        "title": "The Memory Palace",
        "narration": (
            "Computer memory is like a vast palace. Each room has a name (a variable) "
            "and holds exactly one thing (a value). When you put something new in a room, "
            "the old thing vanishes forever. Your job: become the caretaker of this palace."
        ),
        "setting": "memory_palace",
        "character": "Memory Keeper",
        "intro_text": (
            "Welcome, Memory Keeper. I am the palace guide. Each room in this palace "
            "is a variable — it has a name and holds one value. Let me show you how it works."
        ),
    },
    "discovery": {
        "title": "Rooms in the Palace",
        "steps": [
            {
                "action": "inspect_room",
                "room_name": "age",
                "room_value": 21,
                "narration": (
                    "This room is called 'age'. Right now, it holds the number 21. "
                    "The number 21 lives inside — it occupies that space."
                ),
                "interaction": {
                    "type": "reveal_value",
                    "prompt": "What do you think happens if we put a new number into this room?",
                    "reveal_after": "The old value disappears. The room now holds the new number.",
                },
            },
            {
                "action": "change_value",
                "room_name": "age",
                "old_value": 21,
                "new_value": 22,
                "narration": (
                    "We put 22 into the room named 'age'. The 21 vanished. "
                    "The room now contains 22."
                ),
                "interaction": {
                    "type": "drag_and_drop",
                    "prompt": "Drag the number 22 into the room 'age'. Watch the old value disappear.",
                },
            },
            {
                "action": "type_inspection",
                "room_name": "name",
                "room_value": "Rahul",
                "narration": (
                    "Not every room holds numbers. Some hold words. This room named 'name' "
                    "holds the word 'Rahul'. The word 'Rahul' is a string."
                ),
                "interaction": {
                    "type": "inspect_type",
                    "code": 'name = "Rahul"\nprint(type(name))',
                    "expected_output": "<class 'str'>",
                    "hint": "type() tells you what kind of thing lives in a room.",
                },
            },
        ],
        "conclusion": (
            "Variables are names you give to memory locations. Each variable holds one value. "
            "Putting a new value in a variable 'overwrites' the old one."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What will this code print?",
        "code": 'a = 10\nb = a\na = 25\nprint(b)',
        "options": [
            {"id": "a", "text": "10", "correct": True, "explanation": "b got a copy of the value 10, not a link to a"},
            {"id": "b", "text": "25", "correct": False, "explanation": "b was set to a's value (10) before a changed"},
            {"id": "c", "text": "Error", "correct": False, "explanation": "No error — this code is valid Python"},
            {"id": "d", "text": "None", "correct": False, "explanation": "b holds the value 10, not None"},
        ],
        "explanation": (
            "When we write b = a, Python copies the VALUE 10 into a new room called b. "
            "Later changing a does not affect b. Variables hold values, not other variables."
        ),
    },
    "guided_build": {
        "title": "Build Your First Variable Operations",
        "steps": [
            {
                "step_order": 1,
                "title": "Store and Retrieve",
                "description": "Create variables to store student information, then build a summary string.",
                "starter_code": 'def build_summary(name, age, score):\n    # TODO: store name, age, score in variables\n    # then return "Name: <name>, Age: <age>, Score: <score>"\n    pass',
                "function_name": "build_summary",
                "signature": "def build_summary(name, age, score) -> str:",
                "test_cases": [
                    {"input": ["Alice", 20, 85], "expected": "Name: Alice, Age: 20, Score: 85"},
                    {"input": ["Bob", 22, 92], "expected": "Name: Bob, Age: 22, Score: 92"},
                ],
                "hidden_test_cases": [
                    {"input": ["Charlie", 19, 77], "expected": "Name: Charlie, Age: 19, Score: 77"},
                    {"input": ["Diana", 23, 100], "expected": "Name: Diana, Age: 23, Score: 100"},
                    {"input": ["Eve", 21, 88], "expected": "Name: Eve, Age: 21, Score: 88"},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use three assignment statements: name_var = name, etc."},
                    {"level": 2, "text": "Use an f-string: f\"Name: {name_var}, Age: {age_var}, Score: {score_var}\""},
                    {"level": 3, "text": "The f-string evaluates variables at creation time. Make sure your variables hold the right values."},
                ],
            },
            {
                "step_order": 2,
                "title": "Swap Without a Third Variable",
                "description": "In Python, you can swap two variables in one line. Explore this.",
                "starter_code": 'def swap_values(a, b):\n    # TODO: swap the values of a and b\n    # Then return (a, b)\n    pass',
                "function_name": "swap_values",
                "signature": "def swap_values(a, b) -> tuple:",
                "test_cases": [
                    {"input": [1, 2], "expected": (2, 1)},
                    {"input": [10, 20], "expected": (20, 10)},
                ],
                "hidden_test_cases": [
                    {"input": [0, 0], "expected": (0, 0)},
                    {"input": [-5, 5], "expected": (5, -5)},
                    {"input": [100, 200], "expected": (200, 100)},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Try: a, b = b, a"},
                    {"level": 2, "text": "Python evaluates the right side first, then assigns left to right."},
                    {"level": 3, "text": "This uses tuple packing/unpacking under the hood. No temp variable needed."},
                ],
            },
            {
                "step_order": 3,
                "title": "Type Conversion Challenge",
                "description": "Variables can change type. Handle safe type conversion.",
                "starter_code": 'def safe_convert(value):\n    # TODO: try to convert value to int\n    # if that fails, try float\n    # if that also fails, return the string unchanged\n    # return the converted value\n    pass',
                "function_name": "safe_convert",
                "signature": "def safe_convert(value):",
                "test_cases": [
                    {"input": ["42"], "expected": 42},
                    {"input": ["3.14"], "expected": 3.14},
                    {"input": ["hello"], "expected": "hello"},
                    {"input": [100], "expected": 100},
                ],
                "hidden_test_cases": [
                    {"input": ["0"], "expected": 0},
                    {"input": ["-5"], "expected": -5},
                    {"input": ["2.5"], "expected": 2.5},
                    {"input": ["3.0"], "expected": 3.0},
                ],
                "diamonds": 60,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use try/except blocks. Try int(value) first."},
                    {"level": 2, "text": "If int() raises ValueError, try float(value). If that also raises, return str(value)."},
                    {"level": 3, "text": "Edge cases: what about '3.0'? int('3.0') fails, so float('3.0') gives 3.0. That's correct behavior."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "Bank Account State Machine",
        "description": (
            "Build a simple bank account that tracks balance through multiple transactions. "
            "Each transaction updates the account's state (the balance variable)."
        ),
        "function_name": "bank_account",
        "signature": "def bank_account(initial_balance: float, transactions: list) -> dict:",
        "description_full": (
            "Process a list of transactions. Each transaction is a dict: "
            "{'type': 'deposit'|'withdrawal'|'interest', 'amount': float}. "
            "Track the running balance. Return {'final_balance': float, 'transactions_processed': N, 'failed': [...]}.\n\n"
            "Withdrawals that would make balance negative are failed (not processed). "
            "Interest is 2% applied to current balance (type='interest', amount ignored)."
        ),
        "test_cases": [
            {
                "input": [100.0, [{"type": "deposit", "amount": 50}, {"type": "withdrawal", "amount": 30}]],
                "expected": {"final_balance": 120.0, "transactions_processed": 2, "failed": []},
            },
            {
                "input": [100.0, [{"type": "withdrawal", "amount": 200}]],
                "expected": {"final_balance": 100.0, "transactions_processed": 0, "failed": ["withdrawal:200"]},
            },
        ],
        "hidden_test_cases": [
            {"input": [100.0, [{"type": "deposit", "amount": 50}, {"type": "interest"}, {"type": "withdrawal", "amount": 20}]], "expected": {"final_balance": 133.0, "transactions_processed": 3, "failed": []}},
            {"input": [50.0, [{"type": "withdrawal", "amount": 50}, {"type": "withdrawal", "amount": 10}]], "expected": {"final_balance": 0.0, "transactions_processed": 1, "failed": ["withdrawal:10"]}},
            {"input": [500.0, [{"type": "interest"}, {"type": "deposit", "amount": 100}, {"type": "withdrawal", "amount": 50}]], "expected": {"final_balance": 561.0, "transactions_processed": 3, "failed": []}},
        ],
        "time_limit_minutes": 8,
        "diamonds": 100,
        "scaffolded_hints": [
            {"level": 1, "text": "Start with balance = initial_balance. Loop through transactions."},
            {"level": 2, "text": "For each transaction, check the type. Update balance only if valid."},
            {"level": 3, "text": "Use a list to track failed transactions. For interest: balance *= 1.02"},
        ],
    },
    "assessment": {
        "title": "Memory Palace Final Challenge",
        "description": (
            "You are the Memory Keeper. A program runs and manipulates several variables. "
            "Predict the final state of all variables after execution."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": 'x = 5\ny = x\nx = x + 10\nz = y * 2\nx = z - x\n# What are the final values of x, y, z?',
                "answer_format": "x=?, y=?, z=?",
                "expected_answer": "x=-5, y=5, z=10",
                "explanation": (
                    "Trace step by step: x=5, y=x=5, x=x+10=15, z=y*2=10, x=z-x=10-15=-5. "
                    "Final: x=-5, y=5, z=10."
                ),
            },
            {
                "type": "concept",
                "question": "Why can changing variable 'a' not affect variable 'b' after 'b = a'?",
                "answer_format": "short_answer",
                "keywords": ["copy", "value", "reference"],
                "explanation": (
                    "In Python, b = a copies the value from a into b's memory location. "
                    "They are independent. (Except for mutable objects like lists — but for "
                    "primitive types like int, str, float, it's always a value copy.)"
                ),
            },
            {
                "type": "debug",
                "code": 'def calculate_total(price, tax_rate):\n    total = price + price * tax_rate\n    return "Total: " + total\n\nprint(calculate_total(100, 0.1))',
                "error": 'TypeError: can only concatenate str (not "float") to str',
                "question": "Fix the bug.",
                "fix": 'return "Total: " + str(total)',
                "explanation": "total is a float, but you can't concatenate a string with a float directly. Wrap it in str().",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 150,
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:variables",
        "concept_name": "Variables and State",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "Variables store values, not references (for primitives)",
            "Assignment copies the value",
            "Python uses dynamic typing — a variable can hold different types",
            "type() reveals what kind of value a variable holds",
            "Overwriting a variable loses the old value forever",
        ],
        "spaced_fields": [
            "assignment_overwrite",
            "type_inspection",
            "value_copy_vs_reference",
            "dynamic_typing",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "variables_state",
        "unlocks_next": ["control_flow", "data_types"],
        "tower_badge": "first_variables",
        "world_node": {
            "level": 1,
            "title": "Memory Palace",
            "color": "mint",
            "icon": "🏠",
            "description": "Learn how variables store data in memory",
        },
    },
}
