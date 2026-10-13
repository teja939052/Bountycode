"""Pattern Pack — Conditions."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "conditions",
    "name": "Conditions",
    "emoji": "🔀",
    "round_id": "coding",
    "purpose": "Evaluate if/elif/else, nested conditions, ternary operators, and boolean logic to predict control flow.",
    "prerequisites": ["variables", "operators", "output-tracing"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "elif confusion",
            "description": "Treats elif as independent if instead of mutually exclusive branch.",
        },
        {
            "id": "M2",
            "label": "Boolean short-circuit wrong",
            "description": "Assumes both sides of && always evaluate.",
        },
        {
            "id": "M3",
            "label": "Nested if depth",
            "description": "Misses which nested if executes when multiple conditions are true.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Decision tree",
            "captain_message": "See conditions as branches.",
            "render": {
                "kind": "decision_tree",
                "conditions": [
                    {"expr": "x > 0", "label": "positive"},
                    {"expr": "x == 0", "label": "zero"},
                    {"expr": "x < 0", "label": "negative"},
                ],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the condition",
            "captain_message": "Edit boolean expressions.",
            "render": {
                "kind": "code_editor",
                "code": "x = 5\nif x > 0 and x < 10:\n    print('in range')\nelse:\n    print('out')",
                "editable_lines": [2],
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict branch",
            "captain_message": "Choose the output.",
            "render": {
                "kind": "multiple_choice",
                "code": "x = 15\nif x > 10:\n    print('A')\nelif x > 5:\n    print('B')\nelse:\n    print('C')",
                "options": ["A", "B", "C", "Error"],
                "answer_index": 0,
                "explanation": "First condition true → prints A. elif not checked.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the truth table",
            "captain_message": "Write T/F for each condition.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Condition 1",
                        "placeholder": "x > 0 ? T/F",
                        "answer": "x > 0 ? T/F",
                    },
                    {
                        "label": "Condition 2",
                        "placeholder": "x < 10 ? T/F",
                        "answer": "x < 10 ? T/F",
                    },
                    {
                        "label": "Branch taken",
                        "placeholder": "which branch",
                        "answer": "which branch",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break short-circuit",
            "captain_message": "In A and B, if A is false, B is not evaluated.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "False and (1/0) raises?",
                "options": ["ZeroDivisionError", "False", "True", "None"],
                "answer_index": 1,
                "explanation": "Short-circuit: second operand not evaluated, returns False.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix nested conditions",
            "captain_message": "Flatten with elif when branches are mutually exclusive.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Nested if",
                        "placeholder": "if a: if b:",
                        "answer": "if a: if b:",
                    },
                    {
                        "label": "Flattened",
                        "placeholder": "if a and b:",
                        "answer": "if a and b:",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to guard clauses",
            "captain_message": "Use early returns to reduce nesting.",
            "render": {
                "kind": "recall",
                "prompt": "Guard clause pattern?",
                "answer": "check invalid case first and return early",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For multiple conditions, evaluate truth values in order.",
            "render": {
                "kind": "recall",
                "prompt": "In if/elif/else, how many branches execute?",
                "answer": "at most one",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Output: x=7\nif x%2:\n    print('odd')\nelse:\n    print('even')",
                "options": ["odd", "even", "error", "none"],
                "answer": "odd",
                "explanation": "7%2 = 1 → truthy → odd.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Output: x=0\nif x:\n    print('yes')\nelif x is None:\n    print('none')\nelse:\n    print('zero')",
                "options": ["yes", "none", "zero", "error"],
                "answer": "zero",
                "explanation": "x=0 is falsy and not None → else → zero.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Output: x=5\nif x>3: print('A')\nif x>5: print('B')\nelse: print('C')",
                "options": ["A C", "A", "B C", "C"],
                "answer": "A C",
                "explanation": "First if true → A. Second if false → else → C.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Output: a,b=5,3\nif a>b:\n    if a>0:\n        print('yes')\nelse:\n    print('no')",
                "options": ["yes", "no", "error", "none"],
                "answer": "yes",
                "explanation": "a>b true, then a>0 true → yes.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Output: x='hello'\nif x.isupper():\n    print('upper')\nelif x.islower():\n    print('lower')\nelse:\n    print('mixed')",
            "options": ["upper", "lower", "mixed", "error"],
            "answer": "lower",
            "explanation": "'hello' is lowercase → lower.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "In if/elif/else, how many branches run?",
            "answer": "at most one",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Short-circuit in 'and'?",
            "answer": "if first is false, second is not evaluated",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Truthiness of 0, empty string, None?",
            "answer": "all falsy",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "if/else, logical operators",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Nested conditions",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Boolean logic",
        },
    ],
    "interview_transfer": {
        "prompt": "How does condition tracing help in debugging feature flags?",
        "model_answer": "It trains evaluating multiple boolean guards in order, exactly like flag checks that gate feature rollout.",
    },
}
