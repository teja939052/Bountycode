"""
Concept Clarity Slice: Sorting Intuition
========================================

One exceptional hands-on lesson for the concept: ordering data.

Misconceptions attacked:
  1. swapping without a temporary variable loses a value
  2. one comparison sweep is not a sort — the largest bubbles to the end each pass,
     so the work shrinks by one each time
  3. a sorted list still needs comparing neighbours; "sorted" is a property you CHECK
"""
from typing import Dict, Any

SORTING_SLICE: Dict[str, Any] = {
    "lesson_id": "sorting_bazaar",
    "module_id": "programming_fundamentals:sorting",
    "title": "The Sorting Bazaar",
    "description": "Learn how sorting works from first principles by arranging bazaar crates.",
    "difficulty": "intermediate",
    "est_minutes": 16,
    "xp_reward": 240,
    "skills_taught": ["sorting", "arrays", "loops", "iteration"],
    "srs_concept_tag": "programming_fundamentals:sorting",
    "story_context": {
        "title": "The Sorting Bazaar",
        "narration": (
            "A thousand vendors trade at the bazaar, and every crate must ship in order of "
            "size. The keeper compares two neighbouring crates, swaps them if they are "
            "wrong, and moves down the row. At the end of one sweep the biggest crate is "
            "guaranteed to be at the very end — so the next sweep can stop one crate sooner."
        ),
        "setting": "sorting_bazaar",
        "character": "Bazaar Keeper",
        "intro_text": (
            "Welcome, apprentice. Sorting looks simple — compare, swap, repeat — but the "
            "swap itself trips everyone up. Watch this closely."
        ),
    },
    "discovery": {
        "title": "Swapping Crates",
        "steps": [
            {
                "action": "swap_boxes",
                "narration": (
                    "To swap two crates you need a third pair of hands. This is the temp "
                    "variable: hold one crate, free its shelf, move the other, then place "
                    "the held crate."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "a, b = 5, 2\ntemp = a\na = b\nb = temp\nprint(a, b)",
                    "expected_output": "2 5",
                    "hint": "a = b alone would overwrite a and destroy 5 forever — that is why temp exists.",
                },
            },
            {
                "action": "one_sweep",
                "narration": (
                    "One sweep compares neighbours and swaps when the left is bigger. Watch: "
                    "the biggest number lands at the end, but the rest are NOT sorted yet."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "nums = [2, 3, 1]\nfor i in range(len(nums) - 1):\n    if nums[i] > nums[i + 1]:\n        nums[i], nums[i + 1] = nums[i + 1], nums[i]\nprint(nums)",
                    "expected_output": "[2, 1, 3]",
                    "hint": "3 floated to the end (index 2). But 2 and 1 are still wrong — one sweep is only one pass.",
                },
            },
            {
                "action": "shrinking_work",
                "narration": "After a sweep, the biggest crate is locked in place. Why ignore it next time?",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "After one full sweep, how much work does the next sweep save?",
                    "options": [
                        {"id": "a", "text": "One crate — the last one is already in its final spot", "correct": True},
                        {"id": "b", "text": "Nothing — every sweep is identical", "correct": False},
                        {"id": "c", "text": "Half the row", "correct": False},
                    ],
                    "explanation": "The largest value always bubbles to the end of the swept range, so each pass can be one step shorter.",
                },
            },
        ],
        "conclusion": (
            "Swapping needs a temporary holder. One comparison sweep pushes the largest "
            "value to the end of its range. Repeating sweeps, each one crate shorter, "
            "eventually sorts the whole row."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": "nums = [4, 2, 3]\nfor i in range(len(nums) - 1):\n    if nums[i] > nums[i + 1]:\n        nums[i], nums[i + 1] = nums[i + 1], nums[i]\nprint(nums)",
        "options": [
            {"id": "a", "text": "[2, 3, 4]", "correct": True, "explanation": "4 swaps right twice: [4,2,3] → [2,4,3] → [2,3,4]."},
            {"id": "b", "text": "[4, 2, 3]", "correct": False, "explanation": "Unchanged would mean no swaps happened — but 4 > 2 and 4 > 3 force swaps."},
            {"id": "c", "text": "[3, 2, 4]", "correct": False, "explanation": "[3,2,4] would need 4 to move only one step — it keeps bubbling to the end."},
            {"id": "d", "text": "[2, 4, 3]", "correct": False, "explanation": "That is the state after the FIRST swap — the sweep is not finished."},
        ],
        "explanation": (
            "One sweep: 4 vs 2 → swap (2,4,3); 4 vs 3 → swap (2,3,4). The largest value "
            "bubbles all the way to the end. Here it also happens to finish the sort."
        ),
    },
    "guided_build": {
        "title": "Sort Like the Keeper",
        "steps": [
            {
                "step_order": 1,
                "title": "Swap the Ends",
                "description": "Return a copy of the list with the first and last crates swapped.",
                "starter_code": """def swap_first_last(nums):
    # swap positions 0 and -1
    pass""",
                "function_name": "swap_first_last",
                "signature": "def swap_first_last(nums: list) -> list:",
                "test_cases": [
                    {"input": [[1, 2, 3]], "expected": [3, 2, 1]},
                    {"input": [[1]], "expected": [1]},
                ],
                "hidden_test_cases": [
                    {"input": [[]], "expected": []},
                    {"input": [[1, 2, 3, 4]], "expected": [4, 2, 3, 1]},
                    {"input": [[7, 7]], "expected": [7, 7]},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "nums[-1] is the last crate; nums[0] is the first."},
                    {"level": 2, "text": "One line works in Python: nums[0], nums[-1] = nums[-1], nums[0]."},
                    {"level": 3, "text": "A single crate or an empty row is its own swap — no special handling breaks."},
                ],
            },
            {
                "step_order": 2,
                "title": "One Bubble Sweep",
                "description": "Return the list after exactly ONE full sweep of adjacent swaps.",
                "starter_code": """def bubble_pass(nums):
    # compare each neighbour pair once from start to end
    # swap when the left is bigger
    pass""",
                "function_name": "bubble_pass",
                "signature": "def bubble_pass(nums: list) -> list:",
                "test_cases": [
                    {"input": [[3, 1, 2]], "expected": [1, 2, 3]},
                    {"input": [[2, 3, 1]], "expected": [2, 1, 3]},
                ],
                "hidden_test_cases": [
                    {"input": [[5, 4, 3, 2, 1]], "expected": [4, 3, 2, 1, 5]},
                    {"input": [[1, 2, 3]], "expected": [1, 2, 3]},
                    {"input": [[1, 1]], "expected": [1, 1]},
                ],
                "diamonds": 55,
                "scaffolded_hints": [
                    {"level": 1, "text": "Loop i over range(len(nums) - 1) — the last pair is nums[-2], nums[-1]."},
                    {"level": 2, "text": "If nums[i] > nums[i + 1], swap that pair with tuple unpacking."},
                    {"level": 3, "text": "One sweep only. [2,3,1] must come out as [2,1,3], proving one pass is not a full sort."},
                ],
            },
            {
                "step_order": 3,
                "title": "Find the Smallest Shelf",
                "description": "Return the index of the smallest crate in the row. If several are equal, use the first.",
                "starter_code": """def min_index(nums):
    # track the best (smallest) index found so far
    pass""",
                "function_name": "min_index",
                "signature": "def min_index(nums: list) -> int:",
                "test_cases": [
                    {"input": [[3, 1, 2]], "expected": 1},
                    {"input": [[5, 5, 5]], "expected": 0},
                ],
                "hidden_test_cases": [
                    {"input": [[1]], "expected": 0},
                    {"input": [[9, 0, 9]], "expected": 1},
                    {"input": [[2, 4]], "expected": 0},
                ],
                "diamonds": 55,
                "scaffolded_hints": [
                    {"level": 1, "text": "Assume the first element is smallest: best = 0."},
                    {"level": 2, "text": "Walk the rest with for i in range(len(nums)) and update best when nums[i] < nums[best]."},
                    {"level": 3, "text": "Using < (not <=) keeps the FIRST of equal smallest values; that is the selection-sort behaviour."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Quality Gate",
        "description": (
            "The shipping clerk must check whether a row of crates is already in order "
            "— without sorting it. Write the checker."
        ),
        "function_name": "is_sorted",
        "signature": "def is_sorted(nums: list) -> bool:",
        "description_full": (
            "Return True if the list is sorted in non-decreasing order (every element is "
            "less than or equal to the one after it), otherwise False.\n\n"
            "This is the kind of small, boring check that appears again and again in "
            "real sorting bugs — and in placement coding rounds.\n\n"
            "Examples:\n"
            "  is_sorted([1, 2, 3])   -> True\n"
            "  is_sorted([3, 2, 1])   -> False\n"
            "  is_sorted([1, 1, 2])   -> True\n"
            "  is_sorted([])          -> True"
        ),
        "test_cases": [
            {"input": [[1, 2, 3]], "expected": True},
            {"input": [[3, 2, 1]], "expected": False},
            {"input": [[1, 1, 2]], "expected": True},
        ],
        "hidden_test_cases": [
            {"input": [[]], "expected": True},
            {"input": [[5]], "expected": True},
            {"input": [[2, 2, 2]], "expected": True},
            {"input": [[1, 3, 2]], "expected": False},
        ],
        "time_limit_minutes": 8,
        "diamonds": 100,
        "scaffolded_hints": [
            {"level": 1, "text": "Walk neighbour pairs: for i in range(len(nums) - 1)."},
            {"level": 2, "text": "If you ever find nums[i] > nums[i + 1], the row is NOT sorted: return False."},
            {"level": 3, "text": "Empty and single-element rows are trivially sorted — return True."},
        ],
    },
    "assessment": {
        "title": "Sorting Bazaar Final Test",
        "description": (
            "Prove you understand swaps, sweeps, and sortedness — the logic that makes "
            "every sorting algorithm in every language work."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": "nums = [2, 5, 1, 3]\n# one bubble sweep happens\n# after the sweep, nums = [2, 1, 3, 5]\n# What is nums[0]?",
                "answer_format": "single_number",
                "expected_answer": "2",
                "explanation": (
                    "Sweep: 2 vs 5 no swap; 5 vs 1 swap → [2,1,5,3]; 5 vs 3 swap → [2,1,3,5]. "
                    "The first crate stays 2 — only 5 bubbled to the end."
                ),
            },
            {
                "type": "concept",
                "question": "Why do you need a temporary variable (or Python's a, b = b, a) to swap two values?",
                "answer_format": "short_answer",
                "keywords": ["overwrite", "lose", "lost", "temp", "temporary", "holder"],
                "explanation": (
                    "Assignment overwrites the old value. Writing a = b destroys a's original "
                    "value before you can give it to b. A temp holds it in the meantime."
                ),
            },
            {
                "type": "debug",
                "code": "def swap(nums, i, j):\n    nums[i] = nums[j]\n    nums[j] = nums[i]\n    return nums\n# Bug: both positions end up equal",
                "error": "The first assignment overwrites nums[i] before its old value can be placed into nums[j].",
                "question": "One line is wrong. What is the correct single line?",
                "fix": "nums[i], nums[j] = nums[j], nums[i]",
                "explanation": (
                    "Tuple unpacking swaps without a temp. It reads both old values first, "
                    "then assigns both — nothing is lost."
                ),
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 160,
    },
    "explain": {
        "title": "Explain the Sweep",
        "prompt": "Why is one full sweep of bubble sort not a complete sort?",
        "answer_format": "short_answer",
        "keywords": ["one", "largest", "bubbles", "end", "pass", "rest", "not sorted", "moves"],
        "min_words": 8,
        "model_answer": (
            "One sweep compares neighbours from left to right, so the largest value bubbles "
            "to the end of its range. The other values may have moved by one step only — "
            "the rest of the row still needs further passes."
        ),
        "intention": "The answer must say the sweep guarantees only the largest value's final position.",
    },
    "break": {
        "title": "The Vanishing Crate Swap",
        "story": (
            "Two crates must trade places: [1, 2] should become [2, 1]. The keeper wrote a "
            "swap, but both shelves end up holding 2. One crate has vanished."
        ),
        "buggy_code": "def swap(nums, i, j):\n    nums[i] = nums[j]\n    nums[j] = nums[i]\n    return nums\n\na = [1, 2]\nprint(swap(a, 0, 1))",
        "expected_output": "[2, 1]",
        "actual_output": "[2, 2] (the original nums[i] is overwritten before it can be moved)",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "The first assignment overwrites nums[i], destroying its original value before nums[j] can get it", "correct": True, "why": "Assignment replaces the value; nums[i] must be held somewhere first."},
                {"id": "b", "text": "i and j are swapped in the call", "correct": False, "why": "The call uses (0, 1) which matches the positions — the call is fine."},
                {"id": "c", "text": "Python lists cannot change length", "correct": False, "why": "The list keeps its length; two positions were written, not removed."},
                {"id": "d", "text": "print cannot show a list", "correct": False, "why": "print handles lists fine — the wrong values are what it shows."},
            ],
        },
        "fix": "nums[i], nums[j] = nums[j], nums[i]",
        "fixed_code": "def swap(nums, i, j):\n    nums[i], nums[j] = nums[j], nums[i]\n    return nums\n\na = [1, 2]\nprint(swap(a, 0, 1))",
        "explanation": (
            "Tuple unpacking reads BOTH old values first, then assigns both — nothing is "
            "destroyed. (A temporary variable works for the same reason: it holds one crate "
            "while the shelf is emptied.)"
        ),
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:sorting",
        "concept_name": "Sorting Intuition",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "swapping needs a temp holder (or tuple unpacking)",
            "one sweep pushes the largest value to the end of its range",
            "each pass can be one crate shorter than the last",
            "sorted means every neighbour pair is in non-decreasing order",
            "checking sortedness is O(n); sorting naively is O(n^2)",
        ],
        "spaced_fields": [
            "temp_swap",
            "bubble_pass",
            "shrinking_pass",
            "sorted_check",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "sorting",
        "unlocks_next": ["complexity"],
        "tower_badge": "bazaar_sorter",
        "world_node": {
            "level": 6,
            "title": "The Sorting Bazaar",
            "color": "emerald",
            "icon": "⚖️",
            "description": "Learn sorting from comparisons and swaps",
        },
    },
}