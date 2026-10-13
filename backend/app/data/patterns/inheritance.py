"""Pattern Pack — Inheritance."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "inheritance",
    "name": "Inheritance",
    "emoji": "🧬",
    "round_id": "technical-interview",
    "purpose": "Distinguish single/multiple/multilevel inheritance, identify method overriding vs overloading, and explain super keyword.",
    "prerequisites": ["oop", "encapsulation", "functions"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Multiple inheritance always safe",
            "description": "Ignores diamond problem in languages without virtual inheritance.",
        },
        {
            "id": "M2",
            "label": "Overloading vs overriding",
            "description": "Confuses compile-time overloading with runtime overriding.",
        },
        {
            "id": "M3",
            "label": "Constructor inheritance",
            "description": "Assumes child constructor automatically calls parent.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Inheritance tree",
            "captain_message": "See parent and child relationship.",
            "render": {
                "kind": "class_tree",
                "nodes": [
                    {"name": "Animal", "methods": ["speak"]},
                    {"name": "Dog", "methods": ["speak", "fetch"]},
                ],
                "edges": [("Animal", "Dog")],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Override method",
            "captain_message": "Replace parent method in child.",
            "render": {
                "kind": "code_editor",
                "code": "class Animal:\n    def speak(self): return '...'\nclass Dog(Animal):\n    def speak(self): return 'woof'",
                "editable_lines": [4],
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict method resolution",
            "captain_message": "Choose which method runs.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "class A: f=lambda self:'A'\nclass B(A): f=lambda self:'B'\nprint(B().f())",
                "options": ["A", "B", "Error", "None"],
                "answer_index": 1,
                "explanation": "Child overrides parent. B().f() returns 'B'.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the override",
            "captain_message": "Write child method with same signature.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Parent method",
                        "placeholder": "def method(self):",
                        "answer": "def method(self):",
                    },
                    {
                        "label": "Child override",
                        "placeholder": "def method(self): # new behavior",
                        "answer": "def method(self): # new behavior",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break diamond problem",
            "captain_message": "Multiple inheritance can create ambiguity.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Class D inherits B and C, both inherit A. Which A's method does D use?",
                "options": ["B's A", "C's A", "Ambiguous", "Neither"],
                "answer_index": 2,
                "explanation": "Without virtual inheritance, diamond creates ambiguity.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix with super()",
            "captain_message": "Use super() to call parent constructor.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Child init",
                        "placeholder": "def __init__(self): super().__init__()",
                        "answer": "def __init__(self): super().__init__()",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to interface design",
            "captain_message": "Inheritance models 'is-a'. Composition models 'has-a'.",
            "render": {
                "kind": "recall",
                "prompt": "When to prefer composition over inheritance?",
                "answer": "when behavior needs to change at runtime",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Overloading = same name, different params. Overriding = same signature, parent-child.",
            "render": {
                "kind": "recall",
                "prompt": "Overriding requires?",
                "answer": "inheritance and same method signature",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "class A: x=1\nclass B(A): pass\nB().x?",
                "options": ["0", "1", "Error", "None"],
                "answer": "1",
                "explanation": "B inherits x from A.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Which is method overriding?",
                "options": ["Same name, different params", "Same name and params in child", "Overloading", "None"],
                "answer": "Same name and params in child",
                "explanation": "Overriding requires identical signature in subclass.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "super() refers to?",
                "options": ["Child class", "Parent class", "Current instance", "Module"],
                "answer": "Parent class",
                "explanation": "super() returns proxy to parent class.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Diamond problem is solved by?",
                "options": ["super()", "virtual inheritance / interfaces", "overloading", "abstraction"],
                "answer": "virtual inheritance / interfaces",
                "explanation": "Virtual inheritance or interfaces resolve ambiguity.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Best use case for inheritance?",
            "options": ["Code reuse only", "Is-a relationship", "Has-a relationship", "Performance"],
            "answer": "Is-a relationship",
            "explanation": "Inheritance models 'is-a' relationships.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Overloading vs overriding?",
            "answer": "overloading = same name, different params; overriding = same signature in child",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "super() calls?",
            "answer": "parent class method",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Diamond problem solved by?",
            "answer": "virtual inheritance or interfaces",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Inheritance basics, overriding",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "OOP design, diamond",
        },
    ],
    "interview_transfer": {
        "prompt": "When designing a framework, how does inheritance help?",
        "model_answer": "It lets users override hooks while reusing base behavior — but prefer composition for flexibility.",
    },
}
