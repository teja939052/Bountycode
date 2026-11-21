"""Pattern Pack — Functions."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "functions",
    "name": "Functions",
    "emoji": "🧩",
    "round_id": "coding",
    "purpose": "Trace function calls, return values, parameter passing, scope, and recursion.",
    "prerequisites": ["variables", "conditions", "output-tracing"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Return vs print",
            "description": "Confuses return value with printed output.",
        },
        {
            "id": "M2",
            "label": "Scope leak",
            "description": "Assumes local variable exists outside function.",
        },
        {
            "id": "M3",
            "label": "Mutable default",
            "description": "Does not realize default mutable args are shared across calls.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Call stack",
            "captain_message": "See how calls stack and unwind.",
            "render": {
                "kind": "call_stack",
                "calls": ["main", "foo", "bar"],
                "returns": [None, 10, 5],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the argument",
            "captain_message": "Pass different values. See return change.",
            "render": {
                "kind": "code_editor",
                "code": "def square(x):\n    return x*x\nprint(square(5))",
                "editable_lines": [2],
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict return",
            "captain_message": "Choose the return value.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "def f(x):\n    return x+1\nprint(f(f(3)))",
                "options": ["3", "4", "5", "6"],
                "answer_index": 2,
                "explanation": "f(3)=4, f(4)=5.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the trace",
            "captain_message": "Write parameter and return for each call.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Call 1",
                        "placeholder": "f(a) returns?",
                        "answer": "f(a) returns?",
                    },
                    {
                        "label": "Call 2",
                        "placeholder": "f(f(a)) returns?",
                        "answer": "f(f(a)) returns?",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break scope",
            "captain_message": "Local variable does not escape.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "def f():\n    x=10\nf()\nprint(x)",
                "options": ["10", "0", "NameError", "None"],
                "answer_index": 2,
                "explanation": "x is local. Accessing it outside raises NameError.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix mutable default",
            "captain_message": "Use None as default and init inside.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Bad",
                        "placeholder": "def f(x=[]):",
                        "answer": "def f(x=[]):",
                    },
                    {
                        "label": "Good",
                        "placeholder": "def f(x=None): x = x or []",
                        "answer": "def f(x=None): x = x or []",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to recursion",
            "captain_message": "Recursion is just self-call with base case.",
            "render": {
                "kind": "recall",
                "prompt": "Recursion needs?",
                "answer": "base case and recursive step",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For tracing: list inputs and outputs per call in order.",
            "render": {
                "kind": "recall",
                "prompt": "First step in function tracing?",
                "answer": "list calls in execution order",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "def add(a,b): return a+b\nadd(2,3)?",
                "options": ["2", "3", "5", "Error"],
                "answer": "5",
                "explanation": "2+3=5.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "def f(x):\n    return x*2\ny = f(3) + f(4)\ny?",
                "options": ["12", "14", "10", "7"],
                "answer": "14",
                "explanation": "f(3)=6, f(4)=8, sum=14.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "def f(x):\n    if x==0: return 0\n    return x + f(x-1)\nf(4)?",
                "options": ["6", "8", "10", "12"],
                "answer": "10",
                "explanation": "4+3+2+1+0 = 10.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "def f(x=[]):\n    x.append(1)\n    return x\nf(); f()",
                "options": ["[1], [1]", "[1], [1,1]", "[1], [2]", "Error"],
                "answer": "[1], [1,1]",
                "explanation": "Mutable default is shared across calls.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "def f(a,b):\n    a=10\n    b=20\n    return a+b\nx=1; y=2; f(x,y); print(x,y)",
            "options": ["1 2", "10 20", "30 0", "Error"],
            "answer": "1 2",
            "explanation": "Parameters are local. x,y unchanged.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Return vs print?",
            "answer": "return passes value back; print outputs text",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Local variable scope?",
            "answer": "exists only inside function",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Mutable default arg pitfall?",
            "answer": "shared across calls",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Functions, scope",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Recursion, tracing",
        },
    ],
    "interview_transfer": {
        "prompt": "How does understanding function scope help in debugging state bugs?",
        "model_answer": "It trains tracking where state is created, mutated, and consumed — exactly like tracing auth context or request-scoped data.",
    },
}
