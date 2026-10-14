"""
Concept Clarity Slice: Loops & Repetition
=========================================

One exceptional hands-on lesson for the concept: repetition.

Teaching loop implemented as the live vertical-slice contract that
LessonService consumes:
  story_context -> discovery -> prediction -> guided_build ->
  transfer_challenge -> assessment -> srs_enrollment -> world_progression

The lesson attacks the three misconceptions that sink placement
coding rounds and output-prediction MCQs:
  1. ``range(n)`` yields 0..n-1, never 1..n
  2. accumulators must be initialised to 0 (or 1 for products) BEFORE the loop
  3. a loop is a machine with an exit condition, not a magic repeat button
"""
from typing import Dict, Any

LOOP_SLICE: Dict[str, Any] = {
    "lesson_id": "loops_lantern_row",
    "module_id": "programming_fundamentals:loops",
    "title": "The Lantern Row",
    "description": "Learn how loops repeat work by lighting one lantern at a time up the hill.",
    "difficulty": "beginner",
    "est_minutes": 10,
    "xp_reward": 180,
    "skills_taught": ["loops", "iteration", "conditions", "booleans"],
    "srs_concept_tag": "programming_fundamentals:loops",
    "story_context": {
        "title": "The Lantern Row",
        "narration": (
            "Beyond the Forking Path, a long staircase climbs the hill. Every evening the "
            "Lamplighter walks the same route: step 0, light a lantern, step 1, light a "
            "lantern. She never climbs by magic — she repeats one action until the row is "
            "done. That is a loop: one instruction, repeated, with a known finish."
        ),
        "setting": "lantern_row",
        "character": "Lamplighter",
        "intro_text": (
            "Welcome, apprentice. A loop is the same motion done many times — but you must "
            "know exactly when to stop. Let me show you how a program counts its steps."
        ),
    },
    "discovery": {
        "title": "Lighting Step by Step",
        "steps": [
            {
                "action": "show_range",
                "narration": (
                    "This loop lights the first five lanterns. Notice carefully: the first "
                    "lantern is numbered 0, not 1. That is the first thing beginners get wrong."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "for i in range(5):\n    print(i)",
                    "expected_output": "0\n1\n2\n3\n4",
                    "hint": "range(5) is five lanterns numbered 0,1,2,3,4. The last number is never the stop value.",
                },
            },
            {
                "action": "accumulate",
                "narration": (
                    "Watch the lantern light counter. Before the loop starts the total is 0. "
                    "Each step adds the current lantern number to the total."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "total = 0\nfor i in range(1, 6):\n    total += i\nprint(total)",
                    "expected_output": "15",
                    "hint": "The accumulator starts at 0. Each pass adds the step number: 1+2+3+4+5 = 15.",
                },
            },
            {
                "action": "manipulate_stop",
                "narration": (
                    "Manipulate the machine: run the loop, then change the stop value and "
                    "run it again. Watch how one number controls how many times the body runs."
                ),
                "interaction": {
                    "type": "manipulate",
                    "prompt": "Run this. Then change the stop value 5 to 7 and run again.",
                    "code": "for i in range(5):\n    print(i)",
                    "expected_output": "0\n1\n2\n3\n4",
                    "hint": "The stop value is exclusive — change it and the loop simply lights that many more lanterns.",
                },
            },
            {
                "action": "finite_loop",
                "narration": (
                    "A loop without a way to stop is a disaster — it runs forever. The row has "
                    "a fixed length, so the loop must know its limit before it starts."
                ),
                "interaction": {
                    "type": "choose_stop",
                    "prompt": "Which of these loops visits EXACTLY 3 lanterns?",
                    "options": [
                        {"id": "a", "text": "range(3) → 0,1,2", "correct": True},
                        {"id": "b", "text": "range(1, 3) → 1,2 only", "correct": False},
                        {"id": "c", "text": "range(1, 4) → 1,2,3", "correct": False},
                    ],
                    "explanation": "range(3) = 0,1,2 (three lanterns). range(1,3) = two lanterns. range(1,4) = three but starts at 1.",
                },
            },
        ],
        "conclusion": (
            "A loop repeats one body of work. for loops count over a known range; "
            "range(n) starts at 0 and never includes n. Accumulators must be set before "
            "the loop, and the loop must always have a defined stop."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": "count = 0\nfor i in range(4):\n    count = count + i\nprint(count)",
        "options": [
            {"id": "a", "text": "6", "correct": True, "explanation": "0+0, then +1, then +2, then +3 = 6. i goes 0,1,2,3."},
            {"id": "b", "text": "10", "correct": False, "explanation": "10 is 1+2+3+4 — but i starts at 0, not 1."},
            {"id": "c", "text": "4", "correct": False, "explanation": "4 is the number of steps, not the accumulated total."},
            {"id": "d", "text": "Error", "correct": False, "explanation": "count = 0 + 0 is perfectly valid — no error."},
        ],
        "explanation": (
            "i takes the values 0, 1, 2, 3. count grows 0 → 0 → 1 → 3 → 6. "
            "The classic off-by-one: range(4) means four steps starting at 0."
        ),
    },
    "guided_build": {
        "title": "Build Your Loop Legs",
        "steps": [
            {
                "step_order": 1,
                "title": "Sum One to N",
                "description": "Return the sum of every integer from 1 to n, inclusive.",
                "starter_code": """def sum_one_to_n(n):
    # total starts at 0
    # for i in range(1, n + 1): total += i
    # return total
    pass""",
                "function_name": "sum_one_to_n",
                "signature": "def sum_one_to_n(n: int) -> int:",
                "test_cases": [
                    {"input": [5], "expected": 15},
                    {"input": [3], "expected": 6},
                ],
                "hidden_test_cases": [
                    {"input": [1], "expected": 1},
                    {"input": [100], "expected": 5050},
                    {"input": [0], "expected": 0},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "Set total = 0 before the loop runs."},
                    {"level": 2, "text": "Use range(1, n + 1) so n itself is included — range stops before the end."},
                    {"level": 3, "text": "Inside the loop: total += i, then return total after the loop finishes."},
                ],
            },
            {
                "step_order": 2,
                "title": "Count the Evens",
                "description": "Given a list of numbers, return how many of them are even.",
                "starter_code": """def count_evens(nums):
    # walk over nums with for x in nums
    # count how many satisfy x % 2 == 0
    pass""",
                "function_name": "count_evens",
                "signature": "def count_evens(nums: list) -> int:",
                "test_cases": [
                    {"input": [[1, 2, 3, 4]], "expected": 2},
                    {"input": [[2, 4, 6]], "expected": 3},
                ],
                "hidden_test_cases": [
                    {"input": [[]], "expected": 0},
                    {"input": [[1, 3, 5]], "expected": 0},
                    {"input": [[0, 10, 7]], "expected": 2},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Keep an even_count = 0 accumulator."},
                    {"level": 2, "text": "x % 2 == 0 tells you x is even. The % operator is the remainder."},
                    {"level": 3, "text": "Increment the counter only inside the if, then return it after the loop."},
                ],
            },
            {
                "step_order": 3,
                "title": "Square Series",
                "description": "Return a list of the squares of 1 through n: [1, 4, 9, ...].",
                "starter_code": """def square_series(n):
    # build the list inside a loop with .append(i * i)
    pass""",
                "function_name": "square_series",
                "signature": "def square_series(n: int) -> list:",
                "test_cases": [
                    {"input": [3], "expected": [1, 4, 9]},
                    {"input": [1], "expected": [1]},
                ],
                "hidden_test_cases": [
                    {"input": [5], "expected": [1, 4, 9, 16, 25]},
                    {"input": [0], "expected": []},
                    {"input": [2], "expected": [1, 4]},
                ],
                "diamonds": 60,
                "scaffolded_hints": [
                    {"level": 1, "text": "Create result = [] before the loop."},
                    {"level": 2, "text": "For each i in range(1, n + 1), append i * i."},
                    {"level": 3, "text": "square_series(0) must return an empty list — the loop runs zero times."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Toll Booth",
        "description": (
            "The gatekeeper records how many lanterns a visitor passes by counting digits. "
            "Turn a number into a count of its digits WITHOUT converting it to a string."
        ),
        "function_name": "count_digits",
        "signature": "def count_digits(n: int) -> int:",
        "description_full": (
            "Return the number of decimal digits in a non-negative integer n, using a "
            "while loop. Trick: repeatedly divide by 10 and count the divisions until the "
            "number reaches 0.\n\n"
            "Examples:\n"
            "  count_digits(123) -> 3\n"
            "  count_digits(7)   -> 1\n"
            "  count_digits(0)   -> 1   (special case: zero still has one digit)\n\n"
            "A while loop needs a condition — while n > 0. Think about what must happen "
            "inside the loop or it will never stop."
        ),
        "test_cases": [
            {"input": [123], "expected": 3},
            {"input": [7], "expected": 1},
            {"input": [1000], "expected": 4},
        ],
        "hidden_test_cases": [
            {"input": [0], "expected": 1},
            {"input": [123456], "expected": 6},
            {"input": [999], "expected": 3},
            {"input": [1000000000], "expected": 10},
        ],
        "time_limit_minutes": 8,
        "diamonds": 100,
        "scaffolded_hints": [
            {"level": 1, "text": "Handle 0 first: if n == 0, return 1 right away."},
            {"level": 2, "text": "Start with count = 0. While n > 0: n //= 10, then count += 1."},
            {"level": 3, "text": "n //= 10 chops off the last digit. Each chop is one digit counted."},
        ],
    },
    "assessment": {
        "title": "Lantern Row Final Test",
        "description": (
            "Prove you can read, predict, and fix loops — exactly what output-prediction "
            "questions and placement coding rounds demand."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": "n = 3\nresult = 1\nfor i in range(1, n + 1):\n    result *= i\n# What is result?",
                "answer_format": "single_number",
                "expected_answer": "6",
                "explanation": (
                    "result starts at 1. i = 1 → result = 1*1 = 1. i = 2 → 2. i = 3 → 6. "
                    "range(1, 4) visits 1, 2, 3 (3 is included because we wrote n + 1)."
                ),
            },
            {
                "type": "concept",
                "question": "Why does range(5) produce 0,1,2,3,4 instead of 1,2,3,4,5?",
                "answer_format": "short_answer",
                "keywords": ["zero", "0", "start", "exclude", "stop value"],
                "explanation": (
                    "range(n) starts at 0 and stops BEFORE n — the stop value is never "
                    "included. To get 1..5 you must write range(1, 6)."
                ),
            },
            {
                "type": "debug",
                "code": "def sum_list(nums):\n    total = 0\n    for x in nums:\n        total = x\n    return total\n# Bug: returns the last element, not the sum",
                "error": "The function returns 7 for nums=[1, 2, 7] instead of 10.",
                "question": "One line is wrong. What is the correct line?",
                "fix": "total += x",
                "explanation": (
                    "total = x replaces the total each time (you end with the last element). "
                    "total += x ADDS each value into the accumulator, producing the real sum."
                ),
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 150,
    },
    "explain": {
        "title": "Explain the Off-by-One",
        "prompt": "Why does range(5) produce 0,1,2,3,4 instead of 1,2,3,4,5?",
        "answer_format": "short_answer",
        "keywords": ["zero", "0", "start", "stop", "before", "exclude", "stop value"],
        "min_words": 8,
        "model_answer": (
            "range(5) starts at 0 and stops BEFORE 5 — the stop value is never "
            "emitted. So it visits 0,1,2,3,4. To reach 5 you must write range(6)."
        ),
        "intention": "The explanation must show that range starts at 0 and excludes the stop value.",
    },
    "break": {
        "title": "The Summing Crime",
        "story": (
            "A counter is meant to total 1 + 2 + 3 = 6 inside the first three lanterns, "
            "but it reports 3. Inspect the code: the loop is finishing one step too early."
        ),
        "buggy_code": "def sum_first_three():\n    result = 0\n    for i in range(1, 3):\n        result += i\n    return result\n\nprint(sum_first_three())",
        "expected_output": "6",
        "actual_output": "3 (range(1, 3) visits only 1 and 2 — the stop value 3 is never included)",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "range(1, 3) stops before 3, so the loop misses the final value", "correct": True, "why": "range excludes its stop value, so only 1 + 2 = 3 is summed."},
                {"id": "b", "text": "result starts at the wrong number", "correct": False, "why": "result = 0 is the correct starting point for a sum."},
                {"id": "c", "text": "print is in the wrong place", "correct": False, "why": "print outside the function is fine."},
                {"id": "d", "text": "The loop never runs", "correct": False, "why": "range(1, 3) is not empty — it runs twice."},
            ],
        },
        "fix": "for i in range(1, 4):",
        "fixed_code": "def sum_first_three():\n    result = 0\n    for i in range(1, 4):\n        result += i\n    return result\n\nprint(sum_first_three())",
        "explanation": (
            "range(1, 3) yields 1, 2 — the stop value 3 is never emitted. Changing the "
            "line to range(1, 4) includes 3, so the sum becomes 1 + 2 + 3 = 6."
        ),
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:loops",
        "concept_name": "Loops and Repetition",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "range(n) starts at 0 and never includes n",
            "range(1, n + 1) visits 1..n inclusive",
            "accumulators must start before the loop (0 for sums, 1 for products)",
            "a while loop needs a condition and must change something each pass to avoid infinite loops",
            "i in range(4) takes values 0, 1, 2, 3",
        ],
        "spaced_fields": [
            "range_off_by_one",
            "accumulator_initialisation",
            "for_vs_while",
            "loop_termination",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "loops",
        "unlocks_next": ["arrays", "strings"],
        "tower_badge": "first_loops",
        "world_node": {
            "level": 2,
            "title": "The Lantern Row",
            "color": "amber",
            "icon": "🏮",
            "description": "Learn to repeat work with loops",
        },
    },
}