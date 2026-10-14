"""
World 1, Chapter 1 — "The Program": Read + trace state
============================================================

Five beginner-first lessons that establish the very first capability of
the World 1 ladder — READING code as input -> state -> output — before any
real coding happens. Pure Python, no classes, no functions-of-advanced
concepts beyond `def` + `return`, no imports.

Slugs (registry keys):
  program_io          -> What a Program Does (input -> state -> output)
  assignment_boxes    -> Variables as Named Boxes
  types_values        -> Values, Types, and Type Errors
  expressions_order   -> Order of Evaluation
  trace_mini          -> Chapter Transfer: read the whole

Every lesson implements the full vertical-slice contract consumed by
LessonService (discovery -> prediction -> explain -> guided_build ->
break -> transfer_challenge -> assessment -> srs_enrollment ->
world_progression) and passes scripts/verify_concept_clarity.py with its
expected outputs EXECUTED, not authored.
"""
from typing import Dict, Any

# ──────────────────────────────────────────────────────────────────────
# L1 · program_io — What a Program Does
# ──────────────────────────────────────────────────────────────────────

PROGRAM_IO_SLICE: Dict[str, Any] = {
    "lesson_id": "program_io_dawn_gate",
    "module_id": "programming_fundamentals:input_output",
    "title": "The Gate at Dawn",
    "description": "Learn what a program is: data goes in, state changes, a result comes out.",
    "difficulty": "beginner",
    "est_minutes": 8,
    "xp_reward": 120,
    "skills_taught": ["program structure", "variables", "output"],
    "srs_concept_tag": "programming_fundamentals:input_output",
    "story_context": {
        "title": "The Gate at Dawn",
        "narration": (
            "Every morning the Guard opens the city gate and counts who passes: "
            "people enter, the counter changes, and at sunset the final number is "
            "written in the ledger. That is all a program is. Data goes in, the "
            "program changes its state, and a result comes out."
        ),
        "setting": "dawn_gate",
        "character": "Guard",
        "intro_text": (
            "Welcome, apprentice. You have never written code, and that is fine. "
            "Before you write anything, you will learn to READ a program the way "
            "you would read a recipe: what goes in, what changes, what is served."
        ),
    },
    "discovery": {
        "title": "Watch the Ledger Change",
        "steps": [
            {
                "action": "show_io",
                "narration": (
                    "Three visitors pass the gate. The program puts 3 into the "
                    "counter, adds 2 more, then writes the final value."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "visitors = 3\nvisitors = visitors + 2\nprint(visitors)",
                    "expected_output": "5",
                    "hint": "Start with 3, add 2, print the newest value: 5.",
                },
            },
            {
                "action": "show_state",
                "narration": (
                    "The basket held 12 eggs. The baker cracked 3. What is left "
                    "in the basket? The program keeps the answer in a named box."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "eggs = 12\ncracked = 3\nwhole = eggs - cracked\nprint(whole)",
                    "expected_output": "9",
                    "hint": "12 minus 3 is 9. The result is stored in whole.",
                },
            },
        ],
        "conclusion": (
            "A program is input -> state -> output. Lines run top to bottom, each "
            "assignment replaces the value in a named box, and print() reveals the "
            "final value. Reading code is just watching the boxes change."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": "x = 4\nx = x + 1\nprint(x)",
        "options": [
            {"id": "a", "text": "4", "correct": False, "explanation": "4 is the starting value, not the final one."},
            {"id": "b", "text": "5", "correct": True, "explanation": "x becomes 4 + 1 = 5, then prints 5."},
            {"id": "c", "text": "6", "correct": False, "explanation": "That would be x + 2, not x + 1."},
            {"id": "d", "text": "Error", "correct": False, "explanation": "This is valid Python."},
        ],
        "explanation": "The final value of x is 5.",
    },
    "guided_build": {
        "title": "Build Your Own Ledger",
        "steps": [
            {
                "step_order": 1,
                "title": "The Simple Counter",
                "description": "Write a program that counts 3 visitors and prints the total.",
                "starter_code": "visitors = 3\n# add 2 more\nprint(visitors)",
                "function_name": "",
                "signature": "",
                "test_cases": [
                    {"input": [], "expected": 5},
                ],
                "hidden_test_cases": [
                    {"input": [], "expected": 5},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use visitors = visitors + 2 to add more."},
                    {"level": 2, "text": "Then print(visitors) to show the result."},
                ],
            }
        ],
    },
    "transfer_challenge": {
        "title": "New Input, Same Logic",
        "description": "Change the program to handle 10 apples and 4 eaten. What remains?",
        "function_name": "",
        "signature": "",
        "starter_code": "apples = 10\neaten = 4\n# calculate remaining\nprint(remaining)",
        "description_full": "Apply the input -> state -> output pattern to a new scenario.",
        "test_cases": [
            {"input": [], "expected": 6},
        ],
        "hidden_test_cases": [
            {"input": [], "expected": 6},
        ],
        "diamonds": 40,
        "scaffolded_hints": [
            {"level": 1, "text": "remaining = apples - eaten"},
            {"level": 2, "text": "Then print(remaining)"},
        ],
    },
    "assessment": {
        "title": "Program IO Final Check",
        "description": "Prove you can read a program and predict its output.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "a = 1\nb = 2\na = b\nb = 3\nprint(a, b)",
                "answer_format": "single_number",
                "expected_answer": "2 3",
                "explanation": "a gets b's value (2), then b becomes 3. Final: a=2, b=3.",
            },
            {
                "type": "concept",
                "question": "What does print() do in a program?",
                "answer_format": "short_answer",
                "keywords": ["output", "screen", "display", "show", "result"],
                "explanation": "print() sends output to the screen so you can see it.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 50,
    },
    "explain": {
        "title": "Explain Input -> State -> Output",
        "prompt": "In your own words, what happens between the first line and print()?",
        "answer_format": "short_answer",
        "keywords": ["input", "state", "output", "variable", "change"],
        "min_words": 8,
        "model_answer": "The program takes input, stores it in variables (state), processes it, and prints the output.",
        "intention": "The answer must describe the flow from input through state to output.",
    },
    "break": {
        "title": "The Missing Print",
        "story": "A program computes the answer but never shows it.",
        "buggy_code": "answer = 5 + 3\n# missing print\n",
        "expected_output": "8",
        "actual_output": "(nothing)",
        "diagnosis": {
            "question": "Why is there no output?",
            "options": [
                {"id": "a", "text": "The program never prints the answer", "correct": True, "why": "Without print(), the result stays in memory only."},
                {"id": "b", "text": "answer is wrong", "correct": False, "why": "5+3=8 is correct; the issue is no output."},
                {"id": "c", "text": "Python is broken", "correct": False, "why": "Python works fine; the code is missing print()."},
            ],
        },
        "fix": "print(answer)",
        "fixed_code": "answer = 5 + 3\nprint(answer)",
        "explanation": "Adding print(answer) displays the computed value.",
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:input_output",
        "concept_name": "What a Program Does",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "Programs are input -> state -> output",
            "print() shows output",
            "Variables store state",
            "Lines run top to bottom",
        ],
        "spaced_fields": ["input_output", "variables", "print"],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "program_io",
        "unlocks_next": ["assignment_boxes"],
        "tower_badge": "world1_program_io",
        "world_node": {
            "level": 1,
            "title": "The Gate at Dawn",
            "color": "green",
            "icon": "🏛️",
            "description": "Learn what a program is: input, state, output",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────
# L2 · assignment_boxes — Variables as Named Boxes
# ──────────────────────────────────────────────────────────────────────

ASSIGNMENT_SLICE: Dict[str, Any] = {
    "lesson_id": "assignment_boxes_post_room",
    "module_id": "programming_fundamentals:variables",
    "title": "Variables as Named Boxes",
    "description": "Model x = 5 as putting 5 in a box named x; read boxes after a few assignments.",
    "difficulty": "beginner",
    "est_minutes": 8,
    "xp_reward": 120,
    "skills_taught": ["variables", "assignment", "naming"],
    "srs_concept_tag": "programming_fundamentals:variables",
    "story_context": {
        "title": "The Post Room",
        "narration": (
            "The village post room has boxes. Each box has a name. "
            "You put a value in a box by writing name = value. "
            "Later you can look inside any box and see what is there."
        ),
        "setting": "post_room",
        "character": "Clerk",
        "intro_text": (
            "A variable is a named box. The = sign means 'put this value in this box', "
            "not 'these two things are equal'."
        ),
    },
    "discovery": {
        "title": "Label the Boxes",
        "steps": [
            {
                "action": "show_assignment",
                "narration": "apples = 5 puts the value 5 in the box named apples.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "apples = 5\nprint(apples)",
                    "expected_output": "5",
                    "hint": "apples is the box name, 5 is the value inside it.",
                },
            },
            {
                "action": "reassign",
                "narration": "A second assignment replaces what is in the box.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "apples = 5\napples = 8\nprint(apples)",
                    "expected_output": "8",
                    "hint": "The second line replaces 5 with 8 in the same box.",
                },
            },
        ],
        "conclusion": (
            "Variables are named boxes. = stores a value. "
            "A later assignment replaces the old value in the same box."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": "x = 3\nx = x + 2\nprint(x)",
        "options": [
            {"id": "a", "text": "3", "correct": False, "explanation": "3 is the starting value."},
            {"id": "b", "text": "5", "correct": True, "explanation": "x becomes 3 + 2 = 5."},
            {"id": "c", "text": "6", "correct": False, "explanation": "That would be x + 3."},
            {"id": "d", "text": "Error", "correct": False, "explanation": "Valid Python."},
        ],
        "explanation": "x becomes 5.",
    },
    "guided_build": {
        "title": "Build Your Own Boxes",
        "steps": [
            {
                "step_order": 1,
                "title": "Three Boxes",
                "description": "Create variables a=10, b=20, c=30 and print their sum.",
                "starter_code": "a = 10\nb = 20\nc = 30\n# print the sum\n",
                "function_name": "",
                "signature": "",
                "test_cases": [
                    {"input": [], "expected": 60},
                ],
                "hidden_test_cases": [
                    {"input": [], "expected": 60},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "total = a + b + c"},
                    {"level": 2, "text": "print(total)"},
                ],
            }
        ],
    },
    "transfer_challenge": {
        "title": "The Shop Total",
        "description": "Calculate total price of 3 items: pen=10, notebook=25, ruler=5.",
        "function_name": "",
        "signature": "",
        "starter_code": "pen = 10\nnotebook = 25\nruler = 5\n# calculate and print total\n",
        "description_full": "Use variables to store item prices and compute the total.",
        "test_cases": [
            {"input": [], "expected": 40},
        ],
        "hidden_test_cases": [
            {"input": [], "expected": 40},
        ],
        "diamonds": 40,
        "scaffolded_hints": [
            {"level": 1, "text": "total = pen + notebook + ruler"},
            {"level": 2, "text": "print(total)"},
        ],
    },
    "assessment": {
        "title": "Assignment Boxes Final Check",
        "description": "Prove you understand variables as named boxes.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "x = 1\ny = x\nx = 2\nprint(y)",
                "answer_format": "single_number",
                "expected_answer": "1",
                "explanation": "y gets x's value (1) before x changes to 2. y stays 1.",
            },
            {
                "type": "concept",
                "question": "What does x = 5 mean in programming?",
                "answer_format": "short_answer",
                "keywords": ["store", "put", "box", "name", "value"],
                "explanation": "It stores the value 5 in the variable (box) named x.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 50,
    },
    "explain": {
        "title": "Explain Variables",
        "prompt": "What is a variable, in your own words?",
        "answer_format": "short_answer",
        "keywords": ["named", "box", "store", "value", "name"],
        "min_words": 8,
        "model_answer": "A variable is a named box that stores a value. You can change the value later by assigning a new one.",
        "intention": "The answer must describe variables as named storage.",
    },
    "break": {
        "title": "The Equality Trap",
        "story": "A student thinks x = y means x and y are the same thing forever.",
        "buggy_code": "x = 5\ny = x\nx = 10\n# student expects y to be 10",
        "expected_output": "5",
        "actual_output": "10 (wrong expectation)",
        "diagnosis": {
            "question": "What is y after x changes to 10?",
            "options": [
                {"id": "a", "text": "y is still 5", "correct": True, "why": "y got a copy of x's value at assignment time."},
                {"id": "b", "text": "y becomes 10 automatically", "correct": False, "why": "Variables don't stay linked after assignment."},
            ],
        },
        "fix": "y is a copy; x changing doesn't affect y",
        "fixed_code": "x = 5\ny = x\nx = 10\nprint(y)  # still 5",
        "explanation": "Assignment copies the value, not a live link.",
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:variables",
        "concept_name": "Variables as Named Boxes",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "Variables are named boxes",
            "= means store, not equals",
            "Later assignments replace the value",
        ],
        "spaced_fields": ["variables", "assignment", "naming"],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "variables",
        "unlocks_next": ["types_values"],
        "tower_badge": "world1_assignment_boxes",
        "world_node": {
            "level": 2,
            "title": "Variables as Named Boxes",
            "color": "green",
            "icon": "📦",
            "description": "Model x = 5 as putting 5 in a box named x",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────
# L4 · types_values — Values, Types, and Type Errors
# ──────────────────────────────────────────────────────────────────────

TYPES_SLICE: Dict[str, Any] = {
    "lesson_id": "types_values_counting_house",
    "module_id": "programming_fundamentals:types",
    "title": "Values, Types, and Type Errors",
    "description": "Classify int/float/str/bool; read type() output; predict TypeError outcomes.",
    "difficulty": "beginner",
    "est_minutes": 8,
    "xp_reward": 120,
    "skills_taught": ["types", "type errors", "type()"],
    "srs_concept_tag": "programming_fundamentals:types",
    "story_context": {
        "title": "The Counting House",
        "narration": (
            "The Counting House sorts values by kind: whole numbers, decimals, "
            "text, and true/false. Mixing kinds causes type errors."
        ),
        "setting": "counting_house",
        "character": "Accountant",
        "intro_text": (
            "Every value in Python has a type. 5 is int, 3.14 is float, "
            "'hello' is str, True is bool. Mixing types incorrectly causes TypeError."
        ),
    },
    "discovery": {
        "title": "Sort the Values",
        "steps": [
            {
                "action": "show_types",
                "narration": "Each value wears a type label.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "print(type(5))\nprint(type(3.14))\nprint(type('hi'))\nprint(type(True))",
                    "expected_output": "<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>",
                    "hint": "type() shows the kind of value.",
                },
            },
        ],
        "conclusion": (
            "Values have types: int, float, str, bool. "
            "Some operations only work with matching types."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What happens when you add an int and a str?",
        "code": "print(5 + ' apples')",
        "options": [
            {"id": "a", "text": "5 apples", "correct": False, "explanation": "Python doesn't auto-convert int to str for +."},
            {"id": "b", "text": "TypeError", "correct": True, "explanation": "Cannot add int and str in Python."},
            {"id": "c", "text": "'5 apples'", "correct": False, "explanation": "That would require str(5) + ' apples'."},
        ],
        "explanation": "Python raises TypeError for int + str.",
    },
    "guided_build": {
        "title": "Build Type-Safe Code",
        "steps": [
            {
                "step_order": 1,
                "title": "Convert and Concatenate",
                "description": "Convert 5 to string and concatenate with ' apples'.",
                "starter_code": "count = 5\n# convert count to string and add ' apples'\n",
                "function_name": "",
                "signature": "",
                "test_cases": [
                    {"input": [], "expected": "5 apples"},
                ],
                "hidden_test_cases": [
                    {"input": [], "expected": "5 apples"},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use str(count) to convert to string."},
                    {"level": 2, "text": "Then + ' apples' to concatenate."},
                ],
            }
        ],
    },
    "transfer_challenge": {
        "title": "The Price Tag",
        "description": "Create a receipt string: 'Total: $' + str(price) for price=25.",
        "function_name": "",
        "signature": "",
        "starter_code": "price = 25\n# create receipt string\n",
        "description_full": "Convert numeric price to a formatted receipt string.",
        "test_cases": [
            {"input": [], "expected": "Total: $25"},
        ],
        "hidden_test_cases": [
            {"input": [], "expected": "Total: $25"},
        ],
        "diamonds": 40,
        "scaffolded_hints": [
            {"level": 1, "text": "Use str(price) to convert."},
            {"level": 2, "text": "'Total: $' + str(price)"},
        ],
    },
    "assessment": {
        "title": "Types Final Check",
        "description": "Prove you understand types and type errors.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "x = 10\ny = '20'\n# What happens next?",
                "answer_format": "single_word",
                "expected_answer": "TypeError",
                "explanation": "int + str raises TypeError in Python.",
            },
            {
                "type": "concept",
                "question": "How do you convert a number to a string?",
                "answer_format": "short_answer",
                "keywords": ["str()", "str", "convert", "string"],
                "explanation": "Use str(number) to convert a number to a string.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 50,
    },
    "explain": {
        "title": "Explain Type Errors",
        "prompt": "Why does 5 + ' apples' fail in Python?",
        "answer_format": "short_answer",
        "keywords": ["type", "error", "int", "str", "cannot", "add"],
        "min_words": 8,
        "model_answer": "Python cannot add an int and a str. They are different types. You must convert one to match the other.",
        "intention": "The answer must explain the type mismatch.",
    },
    "break": {
        "title": "The Type Mixer",
        "story": "A program tries to add a number and a word.",
        "buggy_code": "age = 25\nmessage = 'I am ' + age + ' years old'\nprint(message)",
        "expected_output": "I am 25 years old",
        "actual_output": "TypeError",
        "diagnosis": {
            "question": "Why does this fail?",
            "options": [
                {"id": "a", "text": "Cannot add str and int", "correct": True, "why": "Python needs both sides to be strings for +."},
                {"id": "b", "text": "age is not defined", "correct": False, "why": "age is defined as 25."},
            ],
        },
        "fix": "message = 'I am ' + str(age) + ' years old'",
        "fixed_code": "age = 25\nmessage = 'I am ' + str(age) + ' years old'\nprint(message)",
        "explanation": "Convert age to string before concatenation.",
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:types",
        "concept_name": "Values, Types, and Type Errors",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "Every value has a type",
            "int + str raises TypeError",
            "str() converts to string",
        ],
        "spaced_fields": ["types", "type_errors", "conversion"],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "types",
        "unlocks_next": ["expressions_order"],
        "tower_badge": "world1_types_values",
        "world_node": {
            "level": 4,
            "title": "Values, Types, and Type Errors",
            "color": "green",
            "icon": "🏷️",
            "description": "Classify int/float/str/bool and predict type errors",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────
# L5 · expressions_order — Order of Evaluation
# ──────────────────────────────────────────────────────────────────────

EXPRESSIONS_SLICE: Dict[str, Any] = {
    "lesson_id": "expressions_order_assayers_scale",
    "module_id": "programming_fundamentals:expressions",
    "title": "Order of Evaluation",
    "description": "Use precedence () > ** > * / // % > + - to read/write compound expressions.",
    "difficulty": "beginner",
    "est_minutes": 8,
    "xp_reward": 120,
    "skills_taught": ["operators", "precedence", "expressions"],
    "srs_concept_tag": "programming_fundamentals:expressions",
    "story_context": {
        "title": "The Assayer's Scale",
        "narration": (
            "The assayer weighs gold in stages: first the heavy pieces, then the fine. "
            "Expressions also have stages. Multiplication happens before addition "
            "unless parentheses say otherwise."
        ),
        "setting": "assayers_scale",
        "character": "Assayer",
        "intro_text": (
            "Python evaluates expressions in a fixed order: "
            "parentheses first, then exponentiation, then multiply/divide, then add/subtract."
        ),
    },
    "discovery": {
        "title": "Weigh the Expression",
        "steps": [
            {
                "action": "show_precedence",
                "narration": "2 + 3 * 4 is not 20. Multiplication wins.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "print(2 + 3 * 4)\nprint((2 + 3) * 4)",
                    "expected_output": "14\n20",
                    "hint": "3*4=12, then +2 = 14. Parentheses force 2+3=5, then *4 = 20.",
                },
            },
        ],
        "conclusion": (
            "Operator precedence: () > ** > * / // % > + -. "
            "Parentheses override the default order."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does 10 - 2 * 3 evaluate to?",
        "code": "print(10 - 2 * 3)",
        "options": [
            {"id": "a", "text": "24", "correct": False, "explanation": "That would be (10-2)*3."},
            {"id": "b", "text": "4", "correct": True, "explanation": "2*3=6, then 10-6=4."},
            {"id": "c", "text": "8", "correct": False, "explanation": "That would be 10-2."},
        ],
        "explanation": "2*3=6, then 10-6=4.",
    },
    "guided_build": {
        "title": "Build Expressions",
        "steps": [
            {
                "step_order": 1,
                "title": "The Discount Formula",
                "description": "Write price * 0.8 for a 20% discount, then add 5 for shipping.",
                "starter_code": "price = 100\n# 20% discount then +5 shipping\n",
                "function_name": "",
                "signature": "",
                "test_cases": [
                    {"input": [], "expected": 85.0},
                ],
                "hidden_test_cases": [
                    {"input": [], "expected": 85.0},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "discounted = price * 0.8"},
                    {"level": 2, "text": "total = discounted + 5"},
                ],
            }
        ],
    },
    "transfer_challenge": {
        "title": "The Compound Interest",
        "description": "Calculate (1 + rate) ** years for rate=0.05, years=3.",
        "function_name": "",
        "signature": "",
        "starter_code": "rate = 0.05\nyears = 3\n# calculate compound factor\n",
        "description_full": "Use ** for exponentiation in the compound interest formula.",
        "test_cases": [
            {"input": [], "expected": 1.157625},
        ],
        "hidden_test_cases": [
            {"input": [], "expected": 1.157625},
        ],
        "diamonds": 40,
        "scaffolded_hints": [
            {"level": 1, "text": "factor = (1 + rate) ** years"},
            {"level": 2, "text": "print(factor)"},
        ],
    },
    "assessment": {
        "title": "Expressions Final Check",
        "description": "Prove you understand operator precedence.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "print(3 + 2 ** 2)",
                "answer_format": "single_number",
                "expected_answer": "7",
                "explanation": "** has higher precedence than +. 2**2=4, then 3+4=7.",
            },
            {
                "type": "concept",
                "question": "What is the correct precedence for * vs +?",
                "answer_format": "short_answer",
                "keywords": ["multiply", "before", "add", "precedence", "* first"],
                "explanation": "Multiplication happens before addition unless parentheses override.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 50,
    },
    "explain": {
        "title": "Explain Precedence",
        "prompt": "Why does 2 + 3 * 4 give 14, not 20?",
        "answer_format": "short_answer",
        "keywords": ["precedence", "multiply", "before", "add", "order"],
        "min_words": 8,
        "model_answer": "Multiplication has higher precedence than addition, so 3*4 is evaluated first (12), then 2+12=14.",
        "intention": "The answer must mention operator precedence.",
    },
    "break": {
        "title": "The Missing Parentheses",
        "story": "A receipt calculates discount after tax instead of before.",
        "buggy_code": "price = 100\ntax = 1.1\ndiscount = 0.9\ntotal = price * tax * discount\n# should discount first",
        "expected_output": "99.0",
        "actual_output": "108.0 (wrong order)",
        "diagnosis": {
            "question": "Why is the total wrong?",
            "options": [
                {"id": "a", "text": "Discount should apply before tax", "correct": True, "why": "price * discount first, then * tax gives 99."},
                {"id": "b", "text": "Tax rate is wrong", "correct": False, "why": "Tax is 10%; the issue is order of operations."},
            ],
        },
        "fix": "total = price * discount * tax",
        "fixed_code": "price = 100\ntax = 1.1\ndiscount = 0.9\ntotal = price * discount * tax\nprint(total)",
        "explanation": "Apply discount first, then tax.",
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:expressions",
        "concept_name": "Order of Evaluation",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "Operator precedence matters",
            "* / // % happen before + -",
            "Parentheses override precedence",
        ],
        "spaced_fields": ["precedence", "operators", "parentheses"],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "expressions",
        "unlocks_next": ["strings_words"],
        "tower_badge": "world1_expressions_order",
        "world_node": {
            "level": 5,
            "title": "Order of Evaluation",
            "color": "green",
            "icon": "⚖️",
            "description": "Use precedence () > ** > * / // % > + -",
        },
    },
}

# ──────────────────────────────────────────────────────────────────────
# L6 · trace_mini — Chapter Transfer: Read the Whole
# ──────────────────────────────────────────────────────────────────────

TRACE_MINI_SLICE: Dict[str, Any] = {
    "lesson_id": "trace_mini_chapter_transfer",
    "module_id": "programming_fundamentals:trace_mini",
    "title": "Chapter Transfer: Read the Whole",
    "description": "Trace a 7-10 line program mixing L1-L6 without running it first.",
    "difficulty": "beginner",
    "est_minutes": 10,
    "xp_reward": 150,
    "skills_taught": ["code tracing", "state tracking", "transfer"],
    "srs_concept_tag": "programming_fundamentals:trace_mini",
    "story_context": {
        "title": "The Ledger Review",
        "narration": (
            "The Guard asks you to read a full morning's ledger without running it. "
            "Can you track every box from first line to last?"
        ),
        "setting": "ledger_review",
        "character": "Guard",
        "intro_text": (
            "Trace the program line by line. Track each variable. "
            "What is the final output?"
        ),
    },
    "discovery": {
        "title": "Trace the Ledger",
        "steps": [
            {
                "action": "trace_intro",
                "narration": "Read this program. Don't run it. What does it print?",
                "interaction": {
                    "type": "inspect_code",
                    "code": "x = 1\ny = 2\nx = y + 1\ny = x - 1\nprint(x, y)",
                    "expected_output": "3 2",
                    "hint": "Track x and y line by line.",
                },
            },
        ],
        "conclusion": (
            "Tracing means following each line and updating variables mentally. "
            "The final print shows the last values of x and y."
        ),
    },
    "prediction": {
        "title": "Trace This",
        "question": "What does this print?",
        "code": "a = 5\nb = a\na = 3\nprint(b)",
        "options": [
            {"id": "a", "text": "5", "correct": True, "explanation": "b got a's value (5) before a changed."},
            {"id": "b", "text": "3", "correct": False, "explanation": "3 is a's new value, not b's."},
        ],
        "explanation": "b is 5.",
    },
    "guided_build": {
        "title": "Trace and Predict",
        "steps": [
            {
                "step_order": 1,
                "title": "Full Trace",
                "description": "Trace this program and write the final output.",
                "starter_code": "x = 10\ny = x + 5\nx = y - 2\nz = x + y\nprint(z)",
                "function_name": "",
                "signature": "",
                "test_cases": [
                    {"input": [], "expected": 28},
                ],
                "hidden_test_cases": [
                    {"input": [], "expected": 28},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "Track x and y after each line."},
                    {"level": 2, "text": "x=10, y=15, x=13, z=13+15=28"},
                ],
            }
        ],
    },
    "transfer_challenge": {
        "title": "New Ledger",
        "description": "Trace this unseen program and predict the output.",
        "function_name": "",
        "signature": "",
        "starter_code": "a = 2\nb = 3\nc = a + b\na = c + 1\nprint(a, c)",
        "description_full": "Trace without running. Track all variables.",
        "test_cases": [
            {"input": [], "expected": "6 5"},
        ],
        "hidden_test_cases": [
            {"input": [], "expected": "6 5"},
        ],
        "diamonds": 50,
        "scaffolded_hints": [
            {"level": 1, "text": "a=2, b=3, c=5, a=6"},
            {"level": 2, "text": "Final: a=6, c=5, so print(6, 5)"},
        ],
    },
    "assessment": {
        "title": "Trace Mini Final Check",
        "description": "Prove you can trace a program without running it.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "x = 1\ny = 2\nx = y\ny = x + 1\nprint(y)",
                "answer_format": "single_number",
                "expected_answer": "3",
                "explanation": "x becomes 2, then y = 2 + 1 = 3.",
            },
            {
                "type": "concept",
                "question": "What is the key skill in code tracing?",
                "answer_format": "short_answer",
                "keywords": ["track", "variable", "line", "update", "state"],
                "explanation": "Track each variable's value after every line.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 50,
    },
    "explain": {
        "title": "Explain Tracing",
        "prompt": "How do you trace a program without running it?",
        "answer_format": "short_answer",
        "keywords": ["track", "variable", "line", "update", "state"],
        "min_words": 8,
        "model_answer": "Read each line, update variable values in order, and track the final state before any print.",
        "intention": "The answer must describe line-by-line state tracking.",
    },
    "break": {
        "title": "The Off-By-One Trace",
        "story": "A traced program gives the wrong final value.",
        "buggy_code": "x = 1\nfor i in range(3):\n    x = x + 1\nprint(x)",
        "expected_output": "4",
        "actual_output": "3 (wrong trace)",
        "diagnosis": {
            "question": "How many times does the loop run?",
            "options": [
                {"id": "a", "text": "3 times: x becomes 2, 3, 4", "correct": True, "why": "range(3) gives 0,1,2 — three iterations."},
                {"id": "b", "text": "2 times", "correct": False, "why": "range(3) has three values, not two."},
            ],
        },
        "fix": "Loop runs 3 times; x starts at 1, ends at 4",
        "fixed_code": "x = 1\nfor i in range(3):\n    x = x + 1\nprint(x)  # 4",
        "explanation": "range(3) iterates three times.",
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:trace_mini",
        "concept_name": "Read the Whole",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "Trace line by line",
            "Track variable updates",
            "Predict final output before running",
        ],
        "spaced_fields": ["tracing", "state", "prediction"],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "chapter1_read",
        "unlocks_next": ["booleans_compare"],
        "tower_badge": "world1_trace_mini",
        "world_node": {
            "level": 7,
            "title": "Chapter Transfer: Read the Whole",
            "color": "green",
            "icon": "📜",
            "description": "Trace a program without running it",
        },
    },
}
