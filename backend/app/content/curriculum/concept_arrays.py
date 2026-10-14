"""
Concept Clarity Slice: Arrays / Lists & Indexing
================================================

One exceptional hands-on lesson for the concept: ordered collections.

A list is a row of numbered shelves. The numbering starts at 0, so the
last shelf is at index ``len - 1``. Misconceptions attacked:
  1. "the first box is box 1" — it is box 0
  2. ``len`` is mistaken for a valid index (it is not — off-by-one)
  3. lists are mutable: \u201changing boxes[2]\u201d changes the original list
"""
from typing import Dict, Any

ARRAY_SLICE: Dict[str, Any] = {
    "lesson_id": "arrays_warehouse",
    "module_id": "programming_fundamentals:arrays",
    "title": "The Warehouse Stack",
    "description": "Learn how lists and indexing work by walking a numbered warehouse aisle.",
    "difficulty": "beginner",
    "est_minutes": 12,
    "xp_reward": 200,
    "skills_taught": ["lists", "arrays", "iteration", "data_structures"],
    "srs_concept_tag": "programming_fundamentals:arrays",
    "story_context": {
        "title": "The Warehouse Stack",
        "narration": (
            "Deep underground, a warehouse stores every item on numbered shelves. The "
            "keepers count from zero — the first shelf is shelf 0. When they want the last "
            "shelf, they count the shelves first and step back one. Lists in code are "
            "exactly this warehouse."
        ),
        "setting": "warehouse_stacks",
        "character": "Warehouse Keeper",
        "intro_text": (
            "Welcome, apprentice. Every crate has a number, the aisle has a length, and "
            "there is exactly one crate per shelf. Let me teach you to read the numbers."
        ),
    },
    "discovery": {
        "title": "Numbered Shelves",
        "steps": [
            {
                "action": "read_shelf",
                "narration": (
                    "This list has three boxes. The first box lives at index 0, the third "
                    "lives at index 2. Count aloud: zero, one, two."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": 'boxes = ["apples", "bread", "coins"]\nprint(boxes[0])\nprint(boxes[2])',
                    "expected_output": "apples\ncoins",
                    "hint": "boxes[0] is the FIRST box. The index counts shelves from zero.",
                },
            },
            {
                "action": "find_last",
                "narration": (
                    "To reach the last box, the keeper counts the shelves (len) and then "
                    "steps back one. The last index is never len — it is len - 1."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": 'box = ["a", "b", "c", "d"]\nprint(len(box))\nprint(box[len(box) - 1])',
                    "expected_output": "4\nd",
                    "hint": "len is the NUMBER of shelves (4); the last one is index 3.",
                },
            },
            {
                "action": "avoid_out_of_range",
                "narration": "Read the error. Asking for a shelf that does not exist crashes the program.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "A list holds 4 boxes. What happens when code asks for box[4]?",
                    "options": [
                        {"id": "a", "text": "IndexError — index out of range", "correct": True},
                        {"id": "b", "text": "Returns the last box", "correct": False},
                        {"id": "c", "text": "Returns an empty crate", "correct": False},
                    ],
                    "explanation": "Valid indexes run 0..len-1, so 4 does not exist. The program crashes with IndexError.",
                },
            },
        ],
        "conclusion": (
            "A list is an ordered row of values, each at an index starting from 0. "
            "index = len - 1 reaches the last element; anything at index len or beyond "
            "crashes with IndexError."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": "items = [5, 1, 3]\nitems[0] = 9\nprint(items[0] + items[1])",
        "options": [
            {"id": "a", "text": "10", "correct": True, "explanation": "items[0] was replaced by 9; 9 + items[1] = 9 + 1 = 10."},
            {"id": "b", "text": "6", "correct": False, "explanation": "6 would be 5 + 1 — but items[0] changed to 9 first."},
            {"id": "c", "text": "8", "correct": False, "explanation": "8 is 5 + 3 — wrong boxes are being added."},
            {"id": "d", "text": "Error", "correct": False, "explanation": "Replacing items[0] is legal — lists are mutable."},
        ],
        "explanation": (
            "items[0] = 9 overwrites the first box. Then we add box 0 (9) to box 1 (1): 10. "
            "Lists can change after they are created — that is what 'mutable' means."
        ),
    },
    "guided_build": {
        "title": "Build Your List Skills",
        "steps": [
            {
                "step_order": 1,
                "title": "Sum the Crates",
                "description": "Return the total of every number in the list.",
                "starter_code": """def sum_list(nums):
    # total = 0
    # for x in nums: total += x
    # return total
    pass""",
                "function_name": "sum_list",
                "signature": "def sum_list(nums: list) -> int:",
                "test_cases": [
                    {"input": [[1, 2, 3]], "expected": 6},
                    {"input": [[5]], "expected": 5},
                ],
                "hidden_test_cases": [
                    {"input": [[]], "expected": 0},
                    {"input": [[-1, 1]], "expected": 0},
                    {"input": [[10, 20, 30]], "expected": 60},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "Set total = 0 before the loop."},
                    {"level": 2, "text": "for x in nums visits each crate in order."},
                    {"level": 3, "text": "An empty list must return 0 — the loop simply never runs."},
                ],
            },
            {
                "step_order": 2,
                "title": "Find the Crate",
                "description": "Return the index where target first appears, or -1 if it is not on any shelf.",
                "starter_code": """def find_index(nums, target):
    # walk over the list by index
    # return the first i where nums[i] == target
    # if not found, return -1
    pass""",
                "function_name": "find_index",
                "signature": "def find_index(nums: list, target: int) -> int:",
                "test_cases": [
                    {"input": [[4, 7, 9], 7], "expected": 1},
                    {"input": [[4, 7, 9], 2], "expected": -1},
                ],
                "hidden_test_cases": [
                    {"input": [[1], 1], "expected": 0},
                    {"input": [[3, 3], 3], "expected": 0},
                    {"input": [[], 2], "expected": -1},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use for i in range(len(nums)) so you can see the index."},
                    {"level": 2, "text": "Return i immediately the first time nums[i] == target."},
                    {"level": 3, "text": "If the loop finishes without a match, return -1 after it."},
                ],
            },
            {
                "step_order": 3,
                "title": "Flip the Aisle",
                "description": "Return a NEW list with the crates in reverse order.",
                "starter_code": """def reverse_list(nums):
    # build a new list: result = []
    # walk nums backwards and .append each crate
    pass""",
                "function_name": "reverse_list",
                "signature": "def reverse_list(nums: list) -> list:",
                "test_cases": [
                    {"input": [[1, 2, 3]], "expected": [3, 2, 1]},
                    {"input": [[5]], "expected": [5]},
                ],
                "hidden_test_cases": [
                    {"input": [[]], "expected": []},
                    {"input": [[1, 2, 3, 4]], "expected": [4, 3, 2, 1]},
                    {"input": [[0, 0]], "expected": [0, 0]},
                ],
                "diamonds": 60,
                "scaffolded_hints": [
                    {"level": 1, "text": "Start with result = [] and loop from the end: range(len(nums) - 1, -1, -1)."},
                    {"level": 2, "text": "Append nums[i] for each i as you walk backwards."},
                    {"level": 3, "text": "Reversing an empty list is just an empty list — no special case needed."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Rotating Rack",
        "description": (
            "A rotating rack spins the crates left by k positions. Move every crate "
            "k steps to the left, wrapping around the front."
        ),
        "function_name": "rotate_left",
        "signature": "def rotate_left(nums: list, k: int) -> list:",
        "description_full": (
            "Return a NEW list that is nums rotated left by k positions.\n\n"
            "If k is larger than the list, rotations repeat the same pattern (rotate by "
            "k % len(nums)). k == 0 or k equal to len(nums) returns the list unchanged.\n\n"
            "Examples:\n"
            "  rotate_left([1, 2, 3, 4, 5], 2) -> [3, 4, 5, 1, 2]\n"
            "  rotate_left([1, 2, 3], 1)      -> [2, 3, 1]\n"
            "  rotate_left([1, 2, 3], 3)      -> [1, 2, 3]\n\n"
            "Hint: two slices — the tail first, then the head — put together."
        ),
        "test_cases": [
            {"input": [[1, 2, 3, 4, 5], 2], "expected": [3, 4, 5, 1, 2]},
            {"input": [[1, 2, 3], 1], "expected": [2, 3, 1]},
            {"input": [[1, 2, 3, 4], 0], "expected": [1, 2, 3, 4]},
            {"input": [[1, 2, 3], 3], "expected": [1, 2, 3]},
        ],
        "hidden_test_cases": [
            {"input": [[1, 2, 3, 4, 5], 4], "expected": [5, 1, 2, 3, 4]},
            {"input": [[1], 5], "expected": [1]},
            {"input": [[10, 20, 30, 40], 2], "expected": [30, 40, 10, 20]},
            {"input": [[1, 2], 3], "expected": [2, 1]},
        ],
        "time_limit_minutes": 8,
        "diamonds": 100,
        "scaffolded_hints": [
            {"level": 1, "text": "Normalise the rotation first: k = k % len(nums)."},
            {"level": 2, "text": "Rotating left by k is: the tail from index k, then the head 0..k."},
            {"level": 3, "text": "So return nums[k:] + nums[:k]."},
        ],
    },
    "assessment": {
        "title": "Warehouse Final Test",
        "description": (
            "Prove you can index, read, and repair list code — the exact skills "
            "placement coding rounds test."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": "nums = [10, 20, 30]\nlast = nums[-1]\nnums[1] = last\n# What is nums[1] + nums[2]?",
                "answer_format": "single_number",
                "expected_answer": "60",
                "explanation": (
                    "nums[-1] is 30 (the last box). nums[1] becomes 30. "
                    "nums[1] + nums[2] = 30 + 30 = 60."
                ),
            },
            {
                "type": "concept",
                "question": "The 4th box lives at index 3, not index 4. Why?",
                "answer_format": "short_answer",
                "keywords": ["zero", "0", "starts", "start counting", "index"],
                "explanation": (
                    "Indexes are zero-based: first box = 0, second = 1, third = 2, "
                    "fourth = 3. That is why the last index is len - 1."
                ),
            },
            {
                "type": "debug",
                "code": "def first_and_last(nums):\n    first = nums[0]\n    last = nums[len(nums)]\n    return first, last\n# Bug: crashes with IndexError",
                "error": "IndexError near nums[len(nums)] — the last valid index is len(nums) - 1.",
                "question": "One line is wrong. What is the correct line?",
                "fix": "last = nums[len(nums) - 1]",
                "explanation": (
                    "len(nums) is one PAST the last shelf. The last element is at "
                    "len(nums) - 1. (nums[-1] works too, but only in Python.)"
                ),
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 150,
    },
    "explain": {
        "title": "Explain the Last Shelf",
        "prompt": "Why is the last index of a list holding 10 items 9, and not 10?",
        "answer_format": "short_answer",
        "keywords": ["zero", "0", "starts", "counting", "len", "minus", "1"],
        "min_words": 8,
        "model_answer": (
            "Indexes count from 0, so the first item sits at index 0. The 10th item "
            "therefore lives at index 9 = len - 1. Index 10 is one PAST the end and crashes."
        ),
        "intention": "The answer must tie index = len - 1 back to zero-based counting.",
    },
    "break": {
        "title": "The Vanished Crate",
        "story": (
            "A keeper tries to read the last crate in a three-crate aisle, but the program "
            "crashes. The shelves are numbered 0, 1, 2 — the keeper asked for shelf 3."
        ),
        "buggy_code": "def print_last(nums):\n    i = len(nums)\n    return nums[i]\n\nprint(print_last([1, 2, 3]))",
        "expected_output": "3",
        "actual_output": "IndexError: list index out of range (asked for index 3; valid indexes are 0..2)",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "len(nums) is the count (3), but the last valid index is len - 1 = 2", "correct": True, "why": "Indexes are zero-based, so the list of length 3 ends at index 2."},
                {"id": "b", "text": "The list is empty", "correct": False, "why": "The list has three values — it is not empty."},
                {"id": "c", "text": "print cannot show numbers", "correct": False, "why": "print shows numbers fine — the crash happens before print."},
                {"id": "d", "text": "nums[i] is not valid syntax", "correct": False, "why": "Subscripting with a variable is valid — the value of i is the problem."},
            ],
        },
        "fix": "i = len(nums) - 1",
        "fixed_code": "def print_last(nums):\n    i = len(nums) - 1\n    return nums[i]\n\nprint(print_last([1, 2, 3]))",
        "explanation": (
            "len(nums) returns the count (3), which is one past the last valid index. "
            "The last crate lives at len(nums) - 1 = 2."
        ),
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:arrays",
        "concept_name": "Lists and Indexing",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "indexes start at 0, so the first box is box 0",
            "the last valid index is len - 1, never len",
            "IndexError means you asked for a shelf that does not exist",
            "lists are mutable — assignment like items[0] = 9 changes the original",
            "for x in nums visits values; range(len(nums)) visits indexes",
        ],
        "spaced_fields": [
            "zero_based_indexing",
            "len_vs_last_index",
            "out_of_range",
            "mutation",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "arrays",
        "unlocks_next": ["strings", "functions"],
        "tower_badge": "list_keeper",
        "world_node": {
            "level": 3,
            "title": "The Warehouse Stack",
            "color": "sky",
            "icon": "📦",
            "description": "Learn ordered collections and zero-based indexing",
        },
    },
}