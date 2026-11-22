"""
Promoted Lesson: OOP Basics
===========================

Service-company technical foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company technical aptitude.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "cs_oop_basics_01"
VERSION = "1.0.0"
SKILL_ID = "cs.oop_basics"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 15
XP_REWARD = 120

OOP_BASICS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:oop_basics",
    "title": "OOP Basics",
    "description": "Master object-oriented programming — classes, objects, inheritance, encapsulation, polymorphism.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["class_object", "encapsulation", "inheritance", "polymorphism", "abstraction"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Define a class and create objects.",
        "Explain encapsulation (data hiding).",
        "Describe inheritance (is-a relationship).",
        "Identify polymorphism (same interface, different behavior).",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Object-Oriented Programming",
        "text": (
            "OOP models real-world entities as objects with state (attributes) and behavior (methods). "
            "A class is a blueprint; an object is an instance. Four pillars: encapsulation, inheritance, polymorphism, abstraction."
        ),
        "key_formula": "class → object: instantiation.",
    },
    "worked_example": {
        "title": "Car class example",
        "code": "class Car:\n    def __init__(self, brand):\n        self.brand = brand\n    def drive(self):\n        print(f\"{self.brand} is driving\")\nmy_car = Car(\"Toyota\")\nmy_car.drive()",
        "explanation": "Car is the class, my_car is the object, drive() is a method.",
    },
    "interactive_practice": [
        {
            "id": "oop_practice_1",
            "type": "mcq",
            "question": "Which OOP pillar hides internal data?",
            "options": ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"],
            "correct_index": 2,
            "explanation": "Encapsulation bundles data and methods, hiding internal state.",
        },
        {
            "id": "oop_practice_2",
            "type": "mcq",
            "question": "'Dog is-a Animal' demonstrates which pillar?",
            "options": ["Encapsulation", "Inheritance", "Polymorphism", "Abstraction"],
            "correct_index": 1,
            "explanation": "Inheritance models is-a relationships.",
        },
    ],
    "misconception_feedback": {
        "class_vs_object": {
            "title": "Common mistake: Confusing class and object",
            "text": "A class is the blueprint; an object is the actual instance created from it.",
        },
    },
    "assessment": [
        {
            "id": "oop_assess_1",
            "type": "mcq",
            "question": "Which pillar allows one interface, multiple forms?",
            "options": ["Encapsulation", "Inheritance", "Polymorphism", "Abstraction"],
            "correct_index": 2,
            "explanation": "Polymorphism means many forms — same interface, different implementations.",
        },
        {
            "id": "oop_assess_2",
            "type": "mcq",
            "question": "Which keyword creates a class in Python?",
            "options": ["def", "class", "object", "struct"],
            "correct_index": 1,
            "explanation": "class is the keyword to define a class in Python.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Vehicle hierarchy",
        "problem": (
            "Design a class hierarchy: Vehicle (base) → Car, Bike (subclasses). "
            "Each has a start() method. Car prints 'Car started', Bike prints 'Bike started'."
        ),
        "code": "class Vehicle:\n    def start(self):\n        print(\"Vehicle started\")\n\nclass Car(Vehicle):\n    def start(self):\n        print(\"Car started\")\n\nclass Bike(Vehicle):\n    def start(self):\n        print(\"Bike started\")",
    },
    "deterministic_answer_key": {
        "oop_practice_1": 2,
        "oop_practice_2": 1,
        "oop_assess_1": 2,
        "oop_assess_2": 1,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/",
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
