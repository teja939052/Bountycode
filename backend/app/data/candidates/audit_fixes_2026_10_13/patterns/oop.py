"""Pattern Pack — OOP Fundamentals.

Covers encapsulation, inheritance, and polymorphism through interactive
object-state manipulation.
"""
from __future__ import annotations

from typing import Any, Dict

pack: Dict[str, Any] = {
    "pattern_id": "oop",
    "name": "OOP Fundamentals",
    "emoji": "🏗️",
    "round_id": "cs-core",
    "purpose": "Recognize class/object boundaries, identify what should be private, and explain inheritance vs composition.",
    "prerequisites": ["variables", "functions"],
    "misconceptions": [
        {
            "id": "O1",
            "label": "Getter/setter confusion",
            "description": "Thinks accessors are the same as public fields.",
        },
        {
            "id": "O2",
            "label": "Inheritance misuse",
            "description": "Uses inheritance for code reuse even when 'is-a' does not hold.",
        },
        {
            "id": "O3",
            "label": "Polymorphism as overloading",
            "description": "Confuses compile-time overloading with runtime overriding.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "The bank account",
            "captain_message": "Should everyone be able to directly change your balance?",
            "render": {
                "kind": "object_boundary",
                "class_name": "BankAccount",
                "public_methods": ["deposit()", "withdraw()", "get_balance()"],
                "private_fields": ["balance"],
                "show_encapsulation": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Toggle visibility",
            "captain_message": "Make balance public. What breaks?",
            "render": {
                "kind": "visibility_toggle",
                "class_name": "BankAccount",
                "field": "balance",
                "options": ["private", "public", "protected"],
                "show_consequence": True,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the behavior",
            "captain_message": "If balance is public, what can a caller do?",
            "render": {
                "kind": "multiple_choice",
                "question": "With a public balance field, which of these is now possible?",
                "options": ["Only deposit/withdraw can change it", "Any code can set it directly", "It becomes read-only", "It is deleted"],
                "answer_index": 1,
                "explanation": "Public fields expose direct write access to any caller.",
            },
        },
        {
            "id": "change",
            "type": "change",
            "title": "Change one thing",
            "captain_message": "Change public balance back to private. What protects it now?",
            "render": {
                "kind": "compare_outputs",
                "original": "balance = 0  # public",
                "modified": "private: balance = 0",
                "highlight_diff": True,
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the class",
            "captain_message": "Write the deposit method with validation.",
            "render": {
                "kind": "fill_code",
                "language": "python",
                "starter": "class BankAccount:\n    def __init__(self):\n        self.__balance = 0\n    def deposit(self, amount):\n        if ___:\n            self.__balance += amount",
                "answer": "amount > 0",
                "placeholders": ["amount > 0"],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break it",
            "captain_message": "This inheritance looks clean. Find the flaw.",
            "render": {
                "kind": "debug_solution",
                "buggy_code": "class Car:\n    def refuel(self): pass\nclass Bicycle(Car):\n    pass",
                "question": "Is a Bicycle really a Car? What breaks at runtime?",
                "expected_failure": "'is-a' fails; Bicycle inherits refuel even though bicycles don't refuel.",
                "diagnosis_code": "inheritance_misuse",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix the design",
            "captain_message": "Replace bad inheritance with composition.",
            "render": {
                "kind": "fix_code",
                "broken": "class Bicycle(Car): pass",
                "fix_hint": "Use composition: a Bicycle has an Engine, it is not a Car.",
                "answer": "class Bicycle:\n    def __init__(self, engine):\n        self.engine = engine",
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer: real system",
            "captain_message": "Apply the same rule to a new context.",
            "render": {
                "kind": "classification",
                "question": "Which relationship is correct?",
                "pairs": [
                    {"class_a": "Dog", "class_b": "Animal", "relation": "is-a", "correct": True},
                    {"class_a": "Engine", "class_b": "Car", "relation": "is-a", "correct": False},
                    {"class_a": "Student", "class_b": "Person", "relation": "is-a", "correct": True},
                ],
                "explanation": "Use inheritance only when subclass is a specialized type of superclass.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "TCS-style proof",
            "captain_message": "No diagrams. 60 seconds.",
            "render": {
                "kind": "timed_question",
                "seconds": 60,
                "question": "Which principle hides internal state and requires all interaction through methods?",
                "options": ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"],
                "answer_index": 2,
                "explanation": "Encapsulation bundles data and restricts direct access.",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "oop-w1",
                "topic": "oop",
                "difficulty": "easy",
                "question": "A class is best described as:",
                "options": ["An object", "A blueprint for objects", "A function", "A variable"],
                "answer": "A blueprint for objects",
                "explanation": "A class defines structure; objects are instances.",
            },
        ],
        "drill": [
            {
                "id": "oop-d1",
                "topic": "oop",
                "difficulty": "medium",
                "question": "Encapsulation means:",
                "options": ["Hiding data behind methods", "Copying objects", "Reusing code", "Overloading functions"],
                "answer": "Hiding data behind methods",
                "explanation": "Encapsulation restricts direct access to internal state.",
            },
        ],
        "speed_run": [
            {
                "id": "oop-s1",
                "topic": "oop",
                "difficulty": "medium",
                "question": "Inheritance expresses:",
                "options": ["has-a", "is-a", "uses", "contains"],
                "answer": "is-a",
                "explanation": "Inheritance models 'is-a' relationships.",
            },
        ],
        "weakness_repair": [
            {
                "id": "oop-r1",
                "topic": "oop",
                "difficulty": "medium",
                "question": "A student uses inheritance to share a 'log()' method between Car and Employee. The flaw is:",
                "options": ["Inheritance is always bad", "'is-a' does not hold between Car and Employee", "log() should be static", "Method names must differ"],
                "answer": "'is-a' does not hold between Car and Employee",
                "explanation": "Neither is a subtype of the other. Use composition or a mixin.",
                "diagnosis_code": "inheritance_misuse",
            },
        ],
    },
    "assessment": [
        {
            "id": "oop-a1",
            "topic": "oop",
            "difficulty": "medium",
            "question": "Which is NOT a pillar of OOP?",
            "options": ["Encapsulation", "Abstraction", "Compilation", "Polymorphism"],
            "answer": "Compilation",
            "explanation": "The four pillars are encapsulation, abstraction, inheritance, polymorphism.",
        },
    ],
    "retention": [
        {
            "id": "oop-ret-1d",
            "due_days": 1,
            "prompt": "What does encapsulation protect?",
            "answer": "Internal state by restricting direct access.",
            "diagnosis_code": "getter_setter_confusion",
        },
        {
            "id": "oop-ret-3d",
            "due_days": 3,
            "prompt": "Inheritance represents which relationship?",
            "answer": "is-a",
            "diagnosis_code": "inheritance_misuse",
        },
        {
            "id": "oop-ret-7d",
            "due_days": 7,
            "prompt": "Polymorphism in OOP primarily enables:",
            "answer": "One interface, multiple implementations",
            "diagnosis_code": "polymorphism_overloading",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "TCS NQT OOP basics",
            "question_count": 3,
        },
        {
            "company": "accenture",
            "difficulty": "medium",
            "timing_seconds": 45,
            "context": "Accenture AMCAT OOP",
            "question_count": 2,
        },
    ],
    "interview_transfer": {
        "prompt": "Explain encapsulation to an interviewer in 30 seconds with a real-world analogy.",
        "model_answer": "Think of a bank account. You can deposit and withdraw using methods, but you cannot directly set the balance to any number. That restriction is encapsulation — it protects the object's internal state.",
        "success_criteria": ["bank-account or similar analogy", "direct access restriction", "methods as controlled interface"],
    },
}
