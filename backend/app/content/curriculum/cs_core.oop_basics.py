"""Lesson module — OOP Basics — Classes, Objects, Inheritance"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.oop_basics',
            'module_id': 'cs_core.oop_basics',
            'title': 'OOP Basics — Classes, Objects, Inheritance',
            'description': 'Object-oriented programming is tested in every technical interview. Understand classes, objects, inheritance, and polymorphism.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['OOP Basics'],
            'srs_concept_tag': 'cs_core.oop_basics',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': 'OOP organizes code around objects. A class is a blueprint. An object is an instance. Inheritance lets classes share behavior.',
            'correct': ['Right distinction.', 'You separated class from object.', 'Correct inheritance relation.'],
            'wrong': ['A class is a blueprint, not an object.', 'Inheritance shares behavior, it does not copy.', 'An object is an instance of a class.'],
            'after_break': 'You found the conceptual error. Now rebuild the class-object distinction.',
            'after_mastery': "You can now reason about OOP design. That's interview-ready CS skill.",
            'retry_prompt': 'Try again. State whether you are describing the blueprint or an instance.'
        },
            'story_context': {
            'title': 'OOP Basics — Classes, Objects, Inheritance',
            'narration': 'Object-oriented programming is tested in every technical interview. Understand classes, objects, inheritance, and polymorphism.',
            'setting': 'oop_basics',
            'character': 'Captain Byte',
            'intro_text': 'Object-oriented programming is tested in every technical interview. Understand classes, objects, inheritance, and polymorphism.'
        },
            'steps': {
            'discover': {
            'prompt': 'Car, Bike, and Truck share properties like wheels and methods like drive(). How do you avoid repeating code?',
            'question': 'Which OOP concept models this shared structure?',
            'options': ['Inheritance', 'Polymorphism', 'Encapsulation', 'Abstraction'],
            'interaction_kind': 'mcq_read'
        },
            'understand': 'A class defines attributes and methods. An object is a class instance. Inheritance lets a subclass reuse superclass behavior. Polymorphism lets subclass methods override superclass methods.',
            'manipulate': {
            'prompt': "Write a Vehicle base class with drive(). Make Car override drive() to print 'Car drives'.",
            'answer': "class Vehicle:\n    def drive(self):\n        print('Vehicle drives')\nclass Car(Vehicle):\n    def drive(self):\n        print('Car drives')",
            'hint': 'Use class Child(Parent): and redefine the method.',
            'interaction_kind': 'code_build'
        },
            'predict': {
            'prompt': "If v = Car() and v.drive() prints 'Car drives', which concept is demonstrated?",
            'answer': 'Polymorphism',
            'options': ['Inheritance', 'Polymorphism', 'Encapsulation', 'Abstraction'],
            'interaction_kind': 'mcq_bottleneck'
        },
            'build': {
            'prompt': 'Add an attribute color to Vehicle and set it via __init__ in Car.',
            'answer': "class Vehicle:\n    def __init__(self, color):\n        self.color = color\nclass Car(Vehicle):\n    pass\nc = Car('red')",
            'explanation': 'Child inherits __init__ unless overridden.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'Why does `class Car(Vehicle): pass` still create a Car instance?',
            'broken_code': "c = Car('red')\n# expected error because Car has no __init__",
            'expected_failure': 'Inheritance includes parent initialization.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Explain why Car inherits Vehicle.__init__ and how to override it.',
            'correct_code': 'class Car(Vehicle):\n    def __init__(self, color, seats):\n        super().__init__(color)\n        self.seats = seats',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'What is the difference between inheritance and composition?',
            'answer': "Inheritance is 'is-a'; composition is 'has-a'.",
            'alternative': ['Car is a Vehicle. Car has an Engine.'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Model a Student that IS-A Person and HAS-A ListOfCourses.',
            'answer': 'class Person:\n    def __init__(self, name):\n        self.name = name\nclass Student(Person):\n    def __init__(self, name, courses):\n        super().__init__(name)\n        self.courses = courses',
            'explanation': 'Use inheritance for identity, composition for owned parts.',
            'interaction_kind': 'code_build'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "Which relationship uses 'has-a'?",
            'answer': 'Composition',
            'options': ['Inheritance', 'Composition', 'Polymorphism', 'Abstraction'],
            'explanation': 'Composition models ownership.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }, {
            'kind': 'code',
            'prompt': 'Override a parent method in a child class.',
            'starter': "class Parent:\n    def greet(self):\n        print('hi')",
            'answer': "class Child(Parent):\n    def greet(self):\n        print('hello from child')",
            'language': ['wipro'],
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'proof': [{
            'id': 'p1-explain_inheritance_vs_composition_with_',
            'prompt': 'Explain inheritance vs composition with one example each.',
            'answer_format': 'text',
            'correct': 'Inheritance: class Dog(Animal). Composition: Car has Engine.',
            'explanation': "Pick examples that highlight 'is-a' versus 'has-a'.",
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_oop_basics', 'tcs_inheritance_questions'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: What is polymorphism?',
            'answer_format': 'text',
            'correct': 'Same interface, different implementations',
            'explanation': 'Polymorphism lets subclass methods override superclass methods.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'cs_core_oop_relationship_misconception',
            'signature': 'Student confuses inheritance with composition or thinks inheritance copies code statically.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_oop_relationships'
        }],
            'srs_key_points': ['Inheritance reuses parent behavior.', 'Polymorphism selects method by runtime type.', 'Encapsulation hides internals behind methods.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'oop_basics',
            'unlocks_next': [],
            'tower_badge': 'cs_core_oop_basics'
        }
        }

SLUG = 'cs_core.oop_basics'
