"""
Concept Clarity Slice: Complexity Intuition (Big-O)
===================================================

One exceptional hands-on lesson for the concept: how work scales.

Misconceptions attacked:
  1. "three loops in a row" ≠ "three times the work class" — 3n is still O(n);
     constants drop
  2. nested loops multiply: n × n = O(n^2)
  3. counting operations is the honest way to "see" complexity before you memorise symbols
"""
from typing import Dict, Any

COMPLEXITY_SLICE: Dict[str, Any] = {
    "lesson_id": "complexity_observatory",
    "module_id": "programming_fundamentals:complexity",
    "title": "The Complexity Observatory",
    "description": "Learn to read how fast work grows by counting operations through a telescope.",
    "difficulty": "intermediate",
    "est_minutes": 15,
    "xp_reward": 220,
    "skills_taught": ["loops", "iteration", "testing", "data_structures"],
    "srs_concept_tag": "programming_fundamentals:complexity",
    "story_context": {
        "title": "The Complexity Observatory",
        "narration": (
            "High above the bazaar, an astronomer studies how much work grows as the "
            "world gets bigger. Doubled the stars — does the work double, stay the same, "
            "or multiply fourfold? That shape of growth is Big-O, and the astronomer can "
            "see it by simply counting operations."
        ),
        "setting": "complexity_observatory",
        "character": "Astronomer",
        "intro_text": (
            "Welcome, apprentice. Do not memorize O(n), O(n^2). Watch a loop and count. "
            "One loop over n → n steps. A loop inside a loop → n × n. Numbers do the talking."
        ),
    },
    "discovery": {
        "title": "Counting the Work",
        "steps": [
            {
                "action": "linear_work",
                "narration": (
                    "This telescope sweeps once per star. 10 stars → 10 steps, 1000 stars → "
                    "1000 steps. Work grows like the input: that is O(n)."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "def sweep(n):\n    total = 0\n    for i in range(n):\n        total += 1\n    return total\n\nprint(sweep(10))",
                    "expected_output": "10",
                    "hint": "One pass per star. Five times as many stars → five times as much work.",
                },
            },
            {
                "action": "constant_work",
                "narration": "This glance reads one number no matter how many stars exist.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def peek(n):\n    return 1\n\nprint(peek(10))\nprint(peek(10_000_000))",
                    "expected_output": "1\n1",
                    "hint": "The loop-free body runs once regardless of n. That is O(1) — constant work.",
                },
            },
            {
                "action": "nested_work",
                "narration": "Now every star is compared to EVERY other star.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "Two nested loops each running n = 10 times. How many inner operations run?",
                    "options": [
                        {"id": "a", "text": "100 (10 × 10)", "correct": True},
                        {"id": "b", "text": "20 (10 + 10)", "correct": False},
                        {"id": "c", "text": "10", "correct": False},
                    ],
                    "explanation": "Nested loops multiply: 10 outer steps, each doing 10 inner steps = 100. That is O(n^2).",
                },
            },
            {
                "action": "rank_growth",
                "narration": (
                    "Arrange the star charts by how FAST the work grows. This is the whole "
                    "point of Big-O: which shape overtakes the others as n gets large?"
                ),
                "interaction": {
                    "type": "arrange",
                    "prompt": "Order these from LEAST work to MOST work as n grows.",
                    "items": [
                        {"id": "constant", "text": "No loop at all — work stays fixed (O(1))"},
                        {"id": "linear", "text": "One loop over n — work grows like n (O(n))"},
                        {"id": "nested", "text": "Nested loops n by n — work grows like n squared (O(n^2))"},
                    ],
                    "correct_order": ["constant", "linear", "nested"],
                    "explanation": "O(1) stays constant, O(n) grows in step with the input, O(n^2) outruns them both once n is large.",
                },
            },
        ],
        "conclusion": (
            "Count the operations. One loop over n → O(n). Two loops in a row → still O(n) "
            "(constants drop). A loop inside a loop → O(n^2) (they multiply). No loop → O(1)."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": "def triple(n):\n    total = 0\n    for i in range(n):\n        total += 1\n    for i in range(n):\n        total += 1\n    for i in range(n):\n        total += 1\n    return total\n\nprint(triple(1000))",
        "options": [
            {"id": "a", "text": "3000", "correct": True, "explanation": "Three loops in a row each add 1000: 3 × 1000 = 3000. Still O(n) overall."},
            {"id": "b", "text": "1000", "correct": False, "explanation": "1000 counts only one of the three loops."},
            {"id": "c", "text": "1000000000", "correct": False, "explanation": "10^9 would need the loops NESTED. In a row they add, not multiply — 3,000,000,000 is for n^3-style nesting."},
            {"id": "d", "text": "3", "correct": False, "explanation": "3 is the number of loops, not the accumulated count."},
        ],
        "explanation": (
            "Sequential loops ADD their work: n + n + n = 3n. Because constants drop, "
            "3n is called O(n). Nested loops MULTIPLY — that is the only way you get "
            "n × n."
        ),
    },
    "guided_build": {
        "title": "Measure Before You Guess",
        "steps": [
            {
                "step_order": 1,
                "title": "The Single Sweep",
                "description": "Count exactly how many times a single loop over range(n) runs.",
                "starter_code": """def count_linear(n):
    total = 0
    # loop once over range(n), increment total each pass
    pass""",
                "function_name": "count_linear",
                "signature": "def count_linear(n: int) -> int:",
                "test_cases": [
                    {"input": [5], "expected": 5},
                    {"input": [0], "expected": 0},
                ],
                "hidden_test_cases": [
                    {"input": [1], "expected": 1},
                    {"input": [1000], "expected": 1000},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "A for i in range(n) loop, with total += 1 in the body."},
                    {"level": 2, "text": "The counter exactly matches n — that is the O(n) shape measured by hand."},
                    {"level": 3, "text": "n = 0 has zero passes — the loop simply never runs."},
                ],
            },
            {
                "step_order": 2,
                "title": "The Double Sweep",
                "description": "Count how many times nested loops over range(n) x range(n) run.",
                "starter_code": """def count_nested(n):
    total = 0
    # for i in range(n):
    #     for j in range(n):
    #         total += 1
    pass""",
                "function_name": "count_nested",
                "signature": "def count_nested(n: int) -> int:",
                "test_cases": [
                    {"input": [2], "expected": 4},
                    {"input": [3], "expected": 9},
                ],
                "hidden_test_cases": [
                    {"input": [10], "expected": 100},
                    {"input": [0], "expected": 0},
                    {"input": [1], "expected": 1},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Outer loop over range(n), inner loop over range(n)." },
                    {"level": 2, "text": "Every outer step runs n inner steps: total = n × n."},
                    {"level": 3, "text": "count_nested(10) = 100 — that multiplication is why O(n^2) explodes quickly."},
                ],
            },
            {
                "step_order": 3,
                "title": "The Half Sweep",
                "description": "Count how many times a loop over range(n // 2) runs. Constants drop, but count honestly.",
                "starter_code": """def count_halved(n):
    total = 0
    # loop over range(n // 2), increment total each pass
    pass""",
                "function_name": "count_halved",
                "signature": "def count_halved(n: int) -> int:",
                "test_cases": [
                    {"input": [10], "expected": 5},
                    {"input": [1], "expected": 0},
                ],
                "hidden_test_cases": [
                    {"input": [100], "expected": 50},
                    {"input": [3], "expected": 1},
                    {"input": [2], "expected": 1},
                ],
                "diamonds": 55,
                "scaffolded_hints": [
                    {"level": 1, "text": "range(n // 2) visits floor(n/2) values — integer division truncates."},
                    {"level": 2, "text": "n = 10 → 5 passes; n = 3 → 1 pass (3 // 2 = 1)."},
                    {"level": 3, "text": "The /2 is a constant factor, so this is still O(n) — exactly the 'drop the constant' rule."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Star Survey",
        "description": (
            "Estimate the survey cost: count the operations of nested loops where the "
            "outer loop sweeps n stars and the inner loop sweeps half of them."
        ),
        "function_name": "work_units",
        "signature": "def work_units(n: int) -> int:",
        "description_full": (
            "Return how many times the inner body runs in this structure:\n\n"
            "    for i in range(n):\n        for j in range(n // 2):\n            <count this>\n\n"
            "The inner bound uses integer division, so for odd n it truncates down.\n\n"
            "Examples:\n"
            "  work_units(4)  -> 8    (outer 4 × inner 2)\n"
            "  work_units(6)  -> 18   (outer 6 × inner 3)\n"
            "  work_units(10) -> 50   (outer 10 × inner 5)\n\n"
            "Can you also name the growth class? n × n/2 still behaves like O(n^2)."
        ),
        "test_cases": [
            {"input": [4], "expected": 8},
            {"input": [6], "expected": 18},
        ],
        "hidden_test_cases": [
            {"input": [10], "expected": 50},
            {"input": [2], "expected": 2},
            {"input": [0], "expected": 0},
            {"input": [3], "expected": 3},
        ],
        "time_limit_minutes": 10,
        "diamonds": 110,
        "scaffolded_hints": [
            {"level": 1, "text": "The answer is n multiplied by n // 2 — just compute and return it."},
            {"level": 2, "text": "For n = 6 the inner runs 3 times per outer step: 6 × 3 = 18."},
            {"level": 3, "text": "n = 0 → inner runs zero times per outer step; outer never runs either → 0."},
        ],
    },
    "assessment": {
        "title": "Observatory Final Test",
        "description": (
            "Prove you can classify code by how fast its work grows — the skill behind "
            "every \"is this efficient?\" interview question."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": "total = 0\nfor i in range(3):\n    for j in range(3):\n        total += 1\n# What is total?",
                "answer_format": "single_number",
                "expected_answer": "9",
                "explanation": "Nested loops multiply: 3 outer steps × 3 inner steps = 9 operations.",
            },
            {
                "type": "concept",
                "question": "Why are three sequential loops over n still called O(n) rather than O(3n)?",
                "answer_format": "short_answer",
                "keywords": ["constant", "drop", "factor", "same growth", "linear", "ignore", "3"],
                "explanation": (
                    "3n and n grow at the same RATE. Big-O cares about the growth class, "
                    "so constant factors like 3 are dropped. Only nested looping changes "
                    "the class."
                ),
            },
            {
                "type": "debug",
                "code": "def sum_pairs(n):\n    total = 0\n    for i in range(n):\n        for j in range(n):\n            total += 1\n    return total\n# Bug (performance): O(n^2), spec wants O(n) work that returns n",
                "error": "The nested loop squares the cost. One line can replace both loops with a single O(n) pass.",
                "question": "What single line replaces the nested loops to make the function O(n) and return n?",
                "fix": "for i in range(n): total += 1",
                "explanation": (
                    "A single loop over range(n) with total += 1 runs n times → O(n), "
                    "and returns exactly n."
                ),
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 160,
    },
    "explain": {
        "title": "Explain the Dropped Constant",
        "prompt": "Why are three loops written one after another still called O(n) rather than O(3n)?",
        "answer_format": "short_answer",
        "keywords": ["constant", "drop", "same", "rate", "growth", "factor", "linear", "add"],
        "min_words": 8,
        "model_answer": (
            "Big-O describes the GROWTH RATE, not the exact count. 3n and n grow at the "
            "same rate, so the constant factor 3 is dropped and we say O(n). Only nesting "
            "changes the class — a loop inside a loop is n × n, not n + n."
        ),
        "intention": "The answer must connect constant-factor dropping to growth-rate equivalence.",
    },
    "break": {
        "title": "The Accidental Bombard",
        "story": (
            "An astronomer's sweep claims to visit each star once, but for 10 stars it "
            "does 100 operations. Somewhere in the chart, a second loop snuck inside the first."
        ),
        "buggy_code": "def sweep(n):\n    total = 0\n    for i in range(n):\n        for j in range(n):\n            total += 1\n    return total\n\nprint(sweep(10) == 10)",
        "expected_output": "True",
        "actual_output": "False (the nested loop runs n × n = 100 times, not n = 10)",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "The inner loop is nested inside the outer one, turning O(n) work into O(n^2) — 10 × 10 = 100", "correct": True, "why": "Nesting multiplies: each of the n outer steps runs the inner n times."},
                {"id": "b", "text": "range(n) produces one extra value", "correct": False, "why": "range(n) produces exactly n values — that is not the problem."},
                {"id": "c", "text": "total starts at 1 instead of 0", "correct": False, "why": "total = 0 is correct; it only tracks a count."},
                {"id": "d", "text": "== cannot compare integers", "correct": False, "why": "Integers compare fine — sweep(10) just does not equal 10."},
            ],
        },
        "fix": "for i in range(n): total += 1",
        "fixed_code": "def sweep(n):\n    total = 0\n    for i in range(n):\n        total += 1\n    return total\n\nprint(sweep(10) == 10)",
        "explanation": (
            "One single loop over range(n) runs exactly n times, so sweep(10) is 10 and "
            "the comparison prints True. The inner loop was the crime."
        ),
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:complexity",
        "concept_name": "Complexity Intuition",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "no loop → O(1): work stays the same no matter the input",
            "one loop over n → O(n): work grows like the input",
            "loops in a row add: n + n + n = 3n, still O(n)",
            "nested loops multiply: n × n = O(n^2)",
            "constant factors and half-sweeps drop: n/2 is still O(n)",
        ],
        "spaced_fields": [
            "constant_work",
            "linear_work",
            "sequential_loops_add",
            "nested_loops_multiply",
            "drop_constants",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "complexity",
        "unlocks_next": [],
        "tower_badge": "observatory_reader",
        "world_node": {
            "level": 7,
            "title": "The Complexity Observatory",
            "color": "violet",
            "icon": "🔭",
            "description": "Learn to classify how fast work grows",
        },
    },
}