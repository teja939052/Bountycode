"""
Concept Clarity Slice: Functions & Scope
========================================

One exceptional hands-on lesson for the concept: reusable logic.

Misconceptions attacked:
  1. printing is NOT returning — a function with no ``return`` gives back None
  2. variables created inside a function stay inside it (local scope)
  3. primitive arguments are passed by value: changing them inside does not
     change the caller's variable
"""
from typing import Dict, Any

FUNCTION_SLICE: Dict[str, Any] = {
    "lesson_id": "functions_function_forge",
    "module_id": "programming_fundamentals:functions",
    "title": "The Function Forge",
    "description": "Learn how functions take inputs, do work, and hand back outputs by smithing tools.",
    "difficulty": "beginner",
    "est_minutes": 14,
    "xp_reward": 220,
    "skills_taught": ["functions", "parameters", "return", "error_handling"],
    "srs_concept_tag": "programming_fundamentals:functions",
    "story_context": {
        "title": "The Function Forge",
        "narration": (
            "At the Function Forge, a smith makes tools from a recipe. The recipe names "
            "its ingredients (parameters), heats and hammers them in a workshop (the body), "
            "and finally hands the finished tool out the door (return). What happens inside "
            "the workshop stays inside — nothing leaks out unless the smith deliberately "
            "hands it over."
        ),
        "setting": "function_forge",
        "character": "Smith",
        "intro_text": (
            "Welcome, apprentice. A function turns inputs into an output. The trick is "
            "knowing the door: return hands the result to the caller; print only shows "
            "it to the screen. Big difference."
        ),
    },
    "discovery": {
        "title": "The Smith's Recipe",
        "steps": [
            {
                "action": "call_double",
                "narration": (
                    "Here a recipe named double takes one ingredient x and hands back x * 2. "
                    "Calling double(4) drops 4 into the recipe; the answer 8 comes out the door."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "def double(x):\n    return x * 2\n\nprint(double(4))",
                    "expected_output": "8",
                    "hint": "x is the parameter. return x * 2 is the door the result exits through.",
                },
            },
            {
                "action": "return_vs_print",
                "narration": (
                    "This smith yells the answer instead of handing it over. The function "
                    "prints 5 to the screen, but it hands back nothing — so y is None."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "def add(a, b):\n    result = a + b\n    print(result)\n\ny = add(2, 3)\nprint(y)",
                    "expected_output": "5\nNone",
                    "hint": "print shows output but is NOT the return value. A function with no return hands back None.",
                },
            },
            {
                "action": "local_scope",
                "narration": "Tools hammered inside the workshop do not walk out on their own.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def setup():\n    secret = \"hidden\"\n\nprint(secret)",
                    "expected_output": "NameError: name 'secret' is not defined",
                    "hint": "secret was made inside setup() — it only exists there. Read it outside and Python says NameError.",
                },
            },
            {
                "action": "compare_return_print",
                "narration": (
                    "Compare the two smiths side by side. Both put an answer on the table, "
                    "but only one HANDS it to the caller."
                ),
                "interaction": {
                    "type": "compare",
                    "prompt": "Which smith hands a usable value back to the caller?",
                    "code_a": "def one(x):\n    print(x * 2)",
                    "code_b": "def two(x):\n    return x * 2",
                    "options": [
                        {"id": "a", "text": "two(x) — return hands the value back; one(x) only prints it", "correct": True, "explanation": "two returns 2x to the caller; one shows it on screen but hands back None."},
                        {"id": "b", "text": "one(x) — printing already gives the caller the value", "correct": False, "explanation": "print writes to the screen; the caller still receives None."},
                        {"id": "c", "text": "Both do the same thing", "correct": False, "explanation": "They differ: returning a value is not the same as printing it."},
                    ],
                    "explanation": "return makes the result usable by the caller; print only displays it.",
                },
            },
        ],
        "conclusion": (
            "A function declares ingredients (parameters), does work in its body, and "
            "hands back exactly one value with return. Without return, the caller gets "
            "None. Variables made inside a function are local — they vanish at the closing "
            "brace."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": "def add_one(n):\n    return n + 1\n\ndef apply_twice(f, x):\n    return f(f(x))\n\nprint(apply_twice(add_one, 5))",
        "options": [
            {"id": "a", "text": "7", "correct": True, "explanation": "add_one runs twice: 5 → 6 → 7. Functions can take other functions as inputs."},
            {"id": "b", "text": "6", "correct": False, "explanation": "6 would be add_one applied once. apply_twice applies it TWO times."},
            {"id": "c", "text": "5", "correct": False, "explanation": "5 is the original input — nothing changed it here but the nested calls."},
            {"id": "d", "text": "Error", "correct": False, "explanation": "Passing a function name as an argument is valid Python."},
        ],
        "explanation": (
            "f(f(x)) calls add_one twice: f(5)=6, then f(6)=7. This is why functions "
            "compose — the output of one is the input of the next."
        ),
    },
    "guided_build": {
        "title": "Forge Your Own Tools",
        "steps": [
            {
                "step_order": 1,
                "title": "The Temperature Converter",
                "description": "Convert Celsius to Fahrenheit: F = C * 9 / 5 + 32.",
                "starter_code": """def celsius_to_fahrenheit(c):
    # return c * 9 / 5 + 32
    pass""",
                "function_name": "celsius_to_fahrenheit",
                "signature": "def celsius_to_fahrenheit(c: float) -> float:",
                "test_cases": [
                    {"input": [0], "expected": 32.0},
                    {"input": [100], "expected": 212.0},
                ],
                "hidden_test_cases": [
                    {"input": [20], "expected": 68.0},
                    {"input": [-40], "expected": -40.0},
                    {"input": [37], "expected": 98.6},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "This is one return statement: return c * 9 / 5 + 32."},
                    {"level": 2, "text": "Order of operations: multiply first, then divide by 5, then add 32."},
                    {"level": 3, "text": "Test the edge: -40C equals -40F — the formula should reproduce it."},
                ],
            },
            {
                "step_order": 2,
                "title": "The Rectangle Stencil",
                "description": "Return the area of a rectangle given width and height.",
                "starter_code": """def rect_area(w, h):
    # return w * h
    pass""",
                "function_name": "rect_area",
                "signature": "def rect_area(w: float, h: float) -> float:",
                "test_cases": [
                    {"input": [3, 4], "expected": 12},
                    {"input": [5, 5], "expected": 25},
                ],
                "hidden_test_cases": [
                    {"input": [0, 10], "expected": 0},
                    {"input": [2.5, 4], "expected": 10.0},
                    {"input": [7, 1], "expected": 7},
                ],
                "diamonds": 45,
                "scaffolded_hints": [
                    {"level": 1, "text": "A recipe with two ingredients and one output."},
                    {"level": 2, "text": "return w * h — multiply, then hand it out the door."},
                    {"level": 3, "text": "Zero width means zero area — no special case, multiplication handles it."},
                ],
            },
            {
                "step_order": 3,
                "title": "The Absolute Difference",
                "description": "Return the absolute difference between two numbers: |a - b|.",
                "starter_code": """def absolute_difference(a, b):
    # the difference, made non-negative
    pass""",
                "function_name": "absolute_difference",
                "signature": "def absolute_difference(a: float, b: float) -> float:",
                "test_cases": [
                    {"input": [10, 3], "expected": 7},
                    {"input": [3, 10], "expected": 7},
                ],
                "hidden_test_cases": [
                    {"input": [0, 0], "expected": 0},
                    {"input": [-5, 5], "expected": 10},
                    {"input": [8, 8], "expected": 0},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "abs(a - b) is the direct answer."},
                    {"level": 2, "text": "abs() removes a negative sign, so order does not matter."},
                    {"level": 3, "text": "Equal numbers give 0 — abs(0) is 0."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Quality Inspector",
        "description": (
            "The forge must only sell prime-quality tools. You build the inspection: a "
            "function that tells whether a number is prime."
        ),
        "function_name": "is_prime",
        "signature": "def is_prime(n: int) -> bool:",
        "description_full": (
            "Return True if n is a prime number, otherwise False. A prime is a whole "
            "number greater than 1 that has no divisors other than 1 and itself.\n\n"
            "Plan it as small steps you can verify:\n"
            "  1. n below 2 can never be prime\n"
            "  2. check the divisors from 2 up to the square root of n\n"
            "  3. if any divides evenly, it is not prime\n\n"
            "Examples:\n"
            "  is_prime(7)   -> True\n"
            "  is_prime(10)  -> False\n"
            "  is_prime(1)   -> False"
        ),
        "test_cases": [
            {"input": [7], "expected": True},
            {"input": [10], "expected": False},
            {"input": [2], "expected": True},
        ],
        "hidden_test_cases": [
            {"input": [0], "expected": False},
            {"input": [1], "expected": False},
            {"input": [3], "expected": True},
            {"input": [97], "expected": True},
            {"input": [100], "expected": False},
        ],
        "time_limit_minutes": 10,
        "diamonds": 110,
        "scaffolded_hints": [
            {"level": 1, "text": "First line: if n < 2: return False."},
            {"level": 2, "text": "Loop from 2 to the square root: for d in range(2, int(n ** 0.5) + 1)."},
            {"level": 3, "text": "If n % d == 0 for any d, it is composite: return False. Survive the loop → return True."},
        ],
    },
    "assessment": {
        "title": "Function Forge Final Test",
        "description": (
            "Prove you know the difference between returning and printing, and can trace "
            "what a function really hands back."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": "def mystery(x):\n    x = x * 10\n    return x\n\ny = 5\nz = mystery(y)\n# What is z?",
                "answer_format": "single_number",
                "expected_answer": "50",
                "explanation": (
                    "mystery multiplies its copy of the input: 5 * 10 = 50 and returns it. "
                    "y stays 5 (the argument was copied), but z receives the return value 50."
                ),
            },
            {
                "type": "concept",
                "question": "Your function computes the right answer but the caller still receives None. What did you forget?",
                "answer_format": "short_answer",
                "keywords": ["return", "returned", "return value", "return statement", "hand"],
                "explanation": (
                    "Without a return statement a function hands back None. Printing the "
                    "answer to the screen is not the same as giving it to the caller."
                ),
            },
            {
                "type": "debug",
                "code": "def area(w, h):\n    print(w * h)\n\nresult = area(2, 3)\n# Bug: result is None, so result == 6 is False\n# Fix it so the function hands back the number",
                "error": "area prints 6 but returns None. The caller's if can never fire.",
                "question": "One line is wrong. What is the correct line?",
                "fix": "return w * h",
                "explanation": (
                    "Replace print(w * h) with return w * h. Then area hands back the "
                    "number 6 and the caller sees result == 6."
                ),
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 150,
    },
    "explain": {
        "title": "Explain Return vs Print",
        "prompt": "Your function computes the right answer and prints it, but the caller still receives None. Explain why, in your own words.",
        "answer_format": "short_answer",
        "keywords": ["return", "return statement", "return value", "hand", "caller", "none", "print"],
        "min_words": 8,
        "model_answer": (
            "print writes text to the screen; return hands a value back to the caller. "
            "If the function never executes a return statement, it hands back None — "
            "even though it printed the correct answer."
        ),
        "intention": "The answer must distinguish showing output (print) from handing it back (return).",
    },
    "break": {
        "title": "The Silent Forge",
        "story": (
            "A smith computes 2 + 3 = 5 for a customer who wants to double it. The forge "
            "shows the answer on the wall — but hands the customer nothing."
        ),
        "buggy_code": "def add(a, b):\n    result = a + b\n    print(result)\n\nprint(add(2, 3) * 2)",
        "expected_output": "10",
        "actual_output": "5 then TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "add prints 5 but returns None, so the caller multiplies None * 2", "correct": True, "why": "Without a return statement the function hands back None."},
                {"id": "b", "text": "The formula 2 + 3 is wrong", "correct": False, "why": "2 + 3 is correctly 5 — the arithmetic is not the problem."},
                {"id": "c", "text": "print cannot be used after another print", "correct": False, "why": "Multiple prints are fine — the crash is a NoneType multiply."},
                {"id": "d", "text": "Python cannot multiply numbers", "correct": False, "why": "Multiplying numbers works; multiplying None does not."},
            ],
        },
        "fix": "return result",
        "fixed_code": "def add(a, b):\n    result = a + b\n    return result\n\nprint(add(2, 3) * 2)",
        "explanation": (
            "Replacing print(result) with return result hands the value 5 to the caller, "
            "so print(add(2, 3) * 2) becomes print(10)."
        ),
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:functions",
        "concept_name": "Functions and Scope",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "parameters are the inputs a function declares",
            "return hands a value to the caller; print only shows it",
            "functions with no return hand back None",
            "local variables die at the end of the function",
            "calls nest: the output of one function feeds another",
        ],
        "spaced_fields": [
            "return_vs_print",
            "local_scope",
            "pass_by_value",
            "function_composition",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "functions",
        "unlocks_next": ["sorting", "complexity"],
        "tower_badge": "forge_smith",
        "world_node": {
            "level": 5,
            "title": "The Function Forge",
            "color": "orange",
            "icon": "🔨",
            "description": "Learn reusable logic, parameters, and return values",
        },
    },
}