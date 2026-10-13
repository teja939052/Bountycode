"""Pattern Pack — Encapsulation (OOP)."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "encapsulation",
    "name": "Encapsulation",
    "emoji": "🔒",
    "round_id": "technical-interview",
    "purpose": "Distinguish public/protected/private visibility, explain getters/setters, and identify encapsulation violations.",
    "prerequisites": ["oop", "variables", "functions"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Encapsulation = data hiding only",
            "description": "Ignores behavior bundling as part of encapsulation.",
        },
        {
            "id": "M2",
            "label": "Getter-setter makes encapsulated",
            "description": "Exposing fields via getters/setters still breaks encapsulation if invariants aren't enforced.",
        },
        {
            "id": "M3",
            "label": "Private = secure",
            "description": "Believes private fields can't be accessed via reflection or serialization.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Public vs private boundary",
            "captain_message": "See what is inside and outside the capsule.",
            "render": {
                "kind": "capsule",
                "public_fields": ["name"],
                "private_fields": ["_balance", "_id"],
                "public_methods": ["deposit", "withdraw"],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change visibility",
            "captain_message": "Make a field private. See access change.",
            "render": {
                "kind": "visibility_editor",
                "class_name": "BankAccount",
                "field": "balance",
                "default_visibility": "public",
                "target_visibility": "private",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict access",
            "captain_message": "Choose what can access the field.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Private field _balance is accessible from:",
                "options": ["Any function", "Class methods only", "Subclass only", "Anyone with reflection"],
                "answer_index": 1,
                "explanation": "Private fields are accessible only within class methods.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the getter/setter",
            "captain_message": "Write accessor with invariant check.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Private field",
                        "placeholder": "_balance",
                        "answer": "_balance",
                    },
                    {
                        "label": "Getter",
                        "placeholder": "return self._balance",
                        "answer": "return self._balance",
                    },
                    {
                        "label": "Setter with invariant",
                        "placeholder": "if amount >= 0: self._balance = amount",
                        "answer": "if amount >= 0: self._balance = amount",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break with invalid state",
            "captain_message": "Direct field access allows invalid balance.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Public field allows setting balance to?",
                "options": ["-100", "0", "1000", "All of these"],
                "answer_index": 3,
                "explanation": "Public field has no invariant enforcement.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix invariant violation",
            "captain_message": "Use setter to enforce non-negative balance.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Invalid set",
                        "placeholder": "account.balance = -100",
                        "answer": "account.balance = -100",
                    },
                    {
                        "label": "Valid set via setter",
                        "placeholder": "account.set_balance(-100) # rejected",
                        "answer": "account.set_balance(-100) # rejected",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to API design",
            "captain_message": "Same principle: hide internal state behind interfaces.",
            "render": {
                "kind": "recall",
                "prompt": "In API design, encapsulation maps to?",
                "answer": "hiding internal state behind stable interface",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Encapsulation = bundle state + valid behavior + controlled access.",
            "render": {
                "kind": "recall",
                "prompt": "Encapsulation bundles?",
                "answer": "state, behavior, and controlled access",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Which keyword creates private in Python?",
                "options": ["private", "__", "hidden", "secret"],
                "answer": "__",
                "explanation": "Double underscore triggers name mangling for private.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Public field vs getter/setter: main difference?",
                "options": ["Speed", "Encapsulation / invariants", "Memory", "None"],
                "answer": "Encapsulation / invariants",
                "explanation": "Getter/setter can enforce invariants.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Which is NOT an OOP pillar?",
                "options": ["Encapsulation", "Abstraction", "Compilation", "Polymorphism"],
                "answer": "Compilation",
                "explanation": "OOP pillars: encapsulation, abstraction, inheritance, polymorphism.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Getter/setter without invariant is still?",
                "options": ["Well encapsulated", "Poor encapsulation", "Abstract", "Polymorphic"],
                "answer": "Poor encapsulation",
                "explanation": "Exposing raw getters/setters without invariants leaks internal state.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Best encapsulation practice?",
            "options": ["All public fields", "Private fields with getters/setters", "No methods", "Global variables"],
            "answer": "Private fields with getters/setters",
            "explanation": "Private fields with controlled access preserve invariants.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Encapsulation bundles?",
            "answer": "state, behavior, and controlled access",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Private keyword in Python?",
            "answer": "__ (double underscore)",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Getter/setter purpose?",
            "answer": "enforce invariants and hide internals",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "OOP basics, visibility",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Design principles",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Abstraction, encapsulation",
        },
    ],
    "interview_transfer": {
        "prompt": "Why is encapsulation important in microservice design?",
        "model_answer": "Each service hides its data behind an API, preventing tight coupling and allowing independent evolution.",
    },
}
