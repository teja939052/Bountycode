"""
Flagship Lesson — Binary Search
 ==================================

 Gold-standard interactive lesson for binary search.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "binary_search"

LESSON: Dict[str, Any] = {
    "lesson_id": "binary_search_divide_conquer",
    "module_id": "dsa:search:binary_search",
    "title": "The Halving Gate",
    "description": "Find any target in a sorted array in O(log n) by repeatedly halving the search space.",
    "difficulty": "intermediate",
    "est_minutes": 16,
    "xp_reward": 130,
    "skills_taught": ["binary_search", "divide_conquer", "sorted_search"],
    "srs_concept_tag": "dsa:binary_search",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Halving Gate only opens for sorted lists. You do not scan every room — "
            "you ask the middle guard which side the target lives on, then discard half. "
            "Repeat until the gate opens.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You halved the space again and again.",
            "🧭 **Captain Byte**\n“Clean. O(log n) beats O(n) every time.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t scan linearly. What does sorted data buy you?”",
            "🧭 **Captain Byte**\n“You’re checking every element. Use the middle.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now halve correctly.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any sorted-search problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Check the middle. Discard half. Repeat.”",
    },
    "story_context": {
        "title": "The Halving Gate",
        "narration": (
            "The Halving Gate only opens for sorted lists. You do not scan every room — "
            "you ask the middle guard which side the target lives on, then discard half. "
            "Repeat until the gate opens."
        ),
        "setting": "halving_gate",
        "character": "Captain Byte",
        "intro_text": (
            "Binary search turns a sorted array into a decision tree. "
            "Each comparison eliminates half the remaining candidates. "
            "Master the invariant: the target, if present, is always between lo and hi."
        ),
    },
    "discovery": {
        "title": "Open the Gate",
        "visual_primitives": ["split", "compare", "trace"],
        "steps": [
            {
                "action": "sorted_invariant",
                "narration": "Sorted order is the only requirement. The middle element tells you which half to keep.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "nums = [2, 5, 8, 12, 16, 23, 38, 56]\nlo, hi = 0, len(nums) - 1\nmid = (lo + hi) // 2\nprint(nums[mid])",
                    "expected_output": "16",
                    "hint": "Index 3 is the middle of 8 elements. nums[3] = 16.",
                },
            },
            {
                "action": "discard_half",
                "narration": "If target < middle, the right half is dead. If target > middle, the left half is dead.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "nums = [1, 3, 5, 7, 9]. Target = 7. mid index = 2, nums[mid] = 5. Which half survives?",
                    "options": [
                        {"id": "a", "text": "Left half [1, 3]", "correct": False},
                        {"id": "b", "text": "Right half [7, 9]", "correct": True},
                        {"id": "c", "text": "Both halves", "correct": False},
                        {"id": "d", "text": "Neither", "correct": False},
                    ],
                    "explanation": "7 > 5, so the left half is discarded. The target must be in the right half.",
                },
            },
            {
                "action": "lo_hi_move",
                "narration": "After discarding, move lo or hi past mid. The next mid is the new center.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "nums = [1, 3, 5, 7, 9]\nlo, hi = 0, 4\ntarget = 7\nmid = (lo + hi) // 2\nif nums[mid] < target:\n    lo = mid + 1\nprint(lo, hi, nums[lo])",
                    "expected_output": "3 4 7",
                    "hint": "mid = 2, nums[2] = 5 < 7, so lo becomes 3. Now nums[3] = 7.",
                },
            },
            {
                "action": "loop_condition",
                "narration": "The loop runs while lo <= hi. When lo passes hi, the target is not present.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "After several halvings, lo = 4 and hi = 3. What does this mean?",
                    "options": [
                        {"id": "a", "text": "The target is at index 4", "correct": False},
                        {"id": "b", "text": "The target is not in the array", "correct": True},
                        {"id": "c", "text": "The loop should continue", "correct": False},
                        {"id": "d", "text": "The array is broken", "correct": False},
                    ],
                    "explanation": "lo > hi means the search space is empty. The target was never found.",
                },
            },
        ],
        "conclusion": (
            "Binary search is one rule: compare the middle, discard half, repeat. "
            "The invariant is that the target, if present, is always between lo and hi inclusive."
        ),
    },
    "prediction": {
        "title": "Before You Halve",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict the middle.”",
        "question": "nums = [1, 2, 3, 4, 5, 6, 7, 8], target = 5. What is the first mid index?",
        "options": [
            {"id": "a", "text": "3", "correct": True, "explanation": "(0 + 7) // 2 = 3. nums[3] = 4."},
            {"id": "b", "text": "4", "correct": False, "explanation": "4 is the second mid, not the first."},
            {"id": "c", "text": "2", "correct": False, "explanation": "2 would be mid if the array were smaller."},
            {"id": "d", "text": "5", "correct": False, "explanation": "5 is past the middle."},
        ],
        "explanation": "The first mid is always (lo + hi) // 2. With 8 elements, that is index 3.",
    },
    "explain": {
        "title": "Explain the Halving",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does binary search run in O(log n) time?”",
        "prompt": "Why does binary search run in O(log n) time?",
        "answer_format": "short_answer",
        "keywords": ["half", "discard", "log", "comparison", "sorted", "invariant", "n", "steps"],
        "min_words": 10,
        "model_answer": (
            "Each comparison discards half the remaining candidates. After k steps, "
            "only n / 2^k elements remain. The loop stops when n / 2^k < 1, which means "
            "k = log2(n). That is why binary search is O(log n)."
        ),
        "intention": "The explanation must connect halving the search space to logarithmic steps.",
    },
    "guided_build": {
        "title": "Write the Gatekeeper",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the loop. lo, hi, mid — the three guards.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Classic Binary Search",
                "captain_byte_moment": "🧭 **Captain Byte**\n“lo, hi, mid — the three guards. While lo <= hi, compare and discard.”",
                "description": "Return the index of target in a sorted array, or -1 if not found.",
                "starter_code": "def binary_search(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n",
                "function_name": "binary_search",
                "signature": "def binary_search(nums: List[int], target: int) -> int:",
                "test_cases": [
                    {"input": [[1, 3, 5, 7, 9], 5], "expected": 2},
                    {"input": [[1, 3, 5, 7, 9], 2], "expected": -1},
                ],
                "hidden_test_cases": [
                    {"input": [[], 1], "expected": -1},
                    {"input": [[1], 1], "expected": 0},
                    {"input": [[1, 2, 3, 4, 5, 6, 7, 8], 8], "expected": 7},
                    {"input": [[2, 4, 6, 8, 10, 12], 1], "expected": -1},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "lo starts at 0, hi at len(nums) - 1."},
                    {"level": 2, "text": "mid = (lo + hi) // 2. Compare nums[mid] to target."},
                    {"level": 3, "text": "If nums[mid] < target, lo = mid + 1. Else hi = mid - 1."},
                ],
            },
            {
                "step_order": 2,
                "title": "First Bad Version",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Find the first bad version. The array is monotonic — use binary search on versions.”",
                "description": "Given n versions and an API isBadVersion(version), return the first bad version.",
                "starter_code": "# The isBadVersion API is already defined.\n# def isBadVersion(version: int) -> bool:\n\ndef first_bad_version(n):\n    lo, hi = 1, n\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if isBadVersion(mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n",
                "function_name": "first_bad_version",
                "signature": "def first_bad_version(n: int) -> int:",
                "test_cases": [
                    {"input": [5], "expected": 4},
                ],
                "hidden_test_cases": [
                    {"input": [1], "expected": 1},
                    {"input": [10], "expected": 3},
                ],
                "diamonds": 45,
                "scaffolded_hints": [
                    {"level": 1, "text": "The versions are monotonic: good... good bad... bad."},
                    {"level": 2, "text": "If mid is bad, the first bad is at mid or before."},
                    {"level": 3, "text": "Use hi = mid when mid is bad; lo = mid + 1 when mid is good."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Sorted Shift",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Sorted but rotated. The array has one pivot. Find the minimum.”",
        "description": (
            "A sorted array was rotated right by k steps. "
            "Find the minimum element in O(log n)."
        ),
        "function_name": "find_min_rotated",
        "signature": "def find_min_rotated(nums: List[int]) -> int:",
        "description_full": (
            "Return the minimum element in a rotated sorted array.\n\n"
            "Example:\n"
            "  find_min_rotated([4, 5, 6, 7, 0, 1, 2]) -> 0\n\n"
            "The array was originally sorted in ascending order and then rotated."
        ),
        "test_cases": [
            {"input": [[4, 5, 6, 7, 0, 1, 2]], "expected": 0},
            {"input": [[3, 4, 5, 1, 2]], "expected": 1},
        ],
        "hidden_test_cases": [
            {"input": [[1]], "expected": 1},
            {"input": [[2, 1]], "expected": 1},
            {"input": [[11, 13, 15, 17]], "expected": 11},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Compare mid with hi. If nums[mid] > nums[hi], the min is in the right half."},
            {"level": 2, "text": "If nums[mid] <= nums[hi], the min is at mid or in the left half."},
            {"level": 3, "text": "Track the minimum seen so far as you narrow the window."},
        ],
    },
    "assessment": {
        "title": "Halving Gate Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you can halve without scanning. Timed.”",
        "description": "Trace binary search, explain the invariant, and fix an off-by-one.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "nums = [1, 3, 5, 7, 9, 11]\nlo, hi = 0, 5\ntarget = 7\nmid = (lo + hi) // 2\nwhile lo <= hi:\n    if nums[mid] == target:\n        break\n    elif nums[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1\n    mid = (lo + hi) // 2\nprint(mid)",
                "answer_format": "single_number",
                "expected_answer": "3",
                "explanation": "First mid = 2 (value 5), lo becomes 3. Second mid = 4 (value 11), hi becomes 3. Third mid = 3 (value 7).",
            },
            {
                "type": "concept",
                "question": "Why must the input array be sorted for binary search to work?",
                "answer_format": "short_answer",
                "keywords": ["sorted", "order", "compare", "discard", "half", "invariant", "guarantee"],
                "explanation": "Sorted order guarantees that comparing to the middle tells you which half to discard.",
            },
            {
                "type": "debug",
                "code": "def bs(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < target:\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo\n# should return index of target or -1",
                "error": "bs([1, 3, 5], 5) must return 2, but loops forever.",
                "question": "Fix the loop condition and pointer updates.",
                "fix": "while lo <= hi:\n    mid = (lo + hi) // 2\n    if nums[mid] == target:\n        return mid\n    elif nums[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1\nreturn -1",
                "explanation": "lo < hi misses the single-element case and mid must advance past itself when discarding.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Infinite Mid",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I broke the gate on purpose. Find the wrong assumption.”",
        "story": (
            "A programmer wrote binary search with while lo < hi and lo = mid. "
            "On a two-element array, the loop never advances. Find the wrong assumption."
        ),
        "buggy_code": "def bs(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < target:\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo\n",
        "expected_output": "2",
        "actual_output": "infinite loop on [1, 3], target = 3",
        "diagnosis": {
            "question": "Which assumption makes this loop infinite?",
            "options": [
                {"id": "a", "text": "lo = mid does not advance past mid, so lo stays the same", "correct": True, "why": "With lo = mid and lo < hi, mid never changes if lo and hi are adjacent."},
                {"id": "b", "text": "The array is not sorted", "correct": False, "why": "The array is sorted; the bug is in the pointer update."},
                {"id": "c", "text": "The loop condition should be while True", "correct": False, "why": "An unconditional loop would be worse."},
                {"id": "d", "text": "mid should be (lo + hi) / 2", "correct": False, "why": "Integer division is correct; the pointer update is the issue."},
            ],
        },
        "fix": "lo = mid + 1",
        "fixed_code": "def bs(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n",
        "explanation": (
            "lo = mid + 1 advances past mid. lo = mid leaves lo unchanged, causing an infinite loop."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:binary_search",
        "concept_name": "Binary Search",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "input must be sorted",
            "compare middle element to target",
            "discard half the search space each step",
            "loop while lo <= hi",
            "update lo = mid + 1 or hi = mid - 1",
        ],
        "spaced_fields": [
            "sorted_invariant",
            "mid_compare",
            "half_discard",
            "loop_condition",
            "pointer_update",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "binary_search",
        "unlocks_next": ["binary_search_applications"],
        "tower_badge": "halving_gate",
        "world_node": {
            "level": 16,
            "title": "The Halving Gate",
            "color": "teal",
            "icon": "🔍",
            "description": "Find any target in a sorted array in O(log n)",
        },
    },
}
