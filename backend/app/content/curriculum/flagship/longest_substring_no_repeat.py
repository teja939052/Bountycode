"""
Flagship Lesson — Longest Substring Without Repeating Characters
 ===============================================================

 Gold-standard interactive lesson for the sliding window pattern.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "longest_substring_no_repeat"

LESSON: Dict[str, Any] = {
    "lesson_id": "longest_substring_no_repeat_window",
    "module_id": "dsa:sliding_window:longest_substring",
    "title": "The Unique Window",
    "description": "Find the longest substring without repeating characters using a sliding window and a set.",
    "difficulty": "intermediate",
    "est_minutes": 15,
    "xp_reward": 120,
    "skills_taught": ["sliding_window", "longest_substring", "hash_set"],
    "srs_concept_tag": "dsa:sliding_window:longest_substring",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Unique Window expands right until it sees a duplicate, then it shrinks from the left "
            "until the window is clean again. The window never restarts — it just slides.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You expanded, then shrank — the window is doing the work.”",
            "🧭 **Captain Byte**\n“Clean. The frame slides, the invariant holds.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t restart for every right index. Keep the window.”",
            "🧭 **Captain Byte**\n“You’re losing O(n). The window must slide, not reset.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now keep the window state correct.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any subarray uniqueness problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Expand right, then shrink left while the window contains duplicates.”",
    },
    "story_context": {
        "title": "The Unique Window",
        "narration": (
            "The Unique Window expands right until it sees a duplicate, then it shrinks from the left "
            "until the window is clean again."
        ),
        "setting": "unique_window",
        "character": "Captain Byte",
        "intro_text": (
            "Sliding window turns O(n²) uniqueness checks into O(n). "
            "The window always represents the current candidate substring."
        ),
    },
    "discovery": {
        "title": "Slide the Window",
        "visual_primitives": ["move", "highlight", "trace"],
        "steps": [
            {
                "action": "expand_right",
                "narration": "Add characters to the window until you see a duplicate.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "s = \"abcabcbb\"\nseen = set()\nleft = 0\nmax_len = 0\nfor right, ch in enumerate(s):\n    while ch in seen:\n        seen.remove(s[left])\n        left += 1\n    seen.add(ch)\n    max_len = max(max_len, right - left + 1)\nprint(max_len)",
                    "expected_output": "3",
                    "hint": "The longest unique substrings are 'abc' and 'bca'.",
                },
            },
            {
                "action": "shrink_left",
                "narration": "When a duplicate appears, shrink from the left until it’s gone.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "Window is 'abca', duplicate 'a' appears. What should happen?",
                    "options": [
                        {"id": "a", "text": "Shrink from the left until 'a' is removed", "correct": True},
                        {"id": "b", "text": "Reset the window to empty", "correct": False},
                        {"id": "c", "text": "Ignore the duplicate", "correct": False},
                        {"id": "d", "text": "Keep both 'a's", "correct": False},
                    ],
                    "explanation": "Shrinking from the left preserves the O(n) guarantee.",
                },
            },
            {
                "action": "set_membership",
                "narration": "A set gives O(1) membership checks. 'ch in seen' is instant.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "seen = {'a', 'b', 'c'}. Is 'b' in seen?",
                    "options": [
                        {"id": "a", "text": "Yes", "correct": True},
                        {"id": "b", "text": "No", "correct": False},
                        {"id": "c", "text": "Only if added last", "correct": False},
                        {"id": "d", "text": "Only if the set is ordered", "correct": False},
                    ],
                    "explanation": "Set membership is O(1) regardless of insertion order.",
                },
            },
            {
                "action": "track_max",
                "narration": "Track the maximum window length seen so far after every valid expansion.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "s = \"pwwkew\"\nseen = set()\nleft = 0\nmax_len = 0\nfor right, ch in enumerate(s):\n    while ch in seen:\n        seen.remove(s[left])\n        left += 1\n    seen.add(ch)\n    max_len = max(max_len, right - left + 1)\nprint(max_len)",
                    "expected_output": "3",
                    "hint": "The longest unique substring is 'wke' or 'kew'.",
                },
            },
        ],
        "conclusion": (
            "The sliding window expands right, shrinks left on duplicates, and tracks the max length. "
            "A set gives O(1) membership checks, so the whole algorithm is O(n)."
        ),
    },
    "prediction": {
        "title": "Before You Slide",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict the window’s longest stretch.”",
        "question": "For 'abcabcbb', what is the length of the longest unique substring?",
        "options": [
            {"id": "a", "text": "3", "correct": True, "explanation": "'abc' is the longest unique substring."},
            {"id": "b", "text": "4", "correct": False, "explanation": "No 4-character unique substring exists in this string."},
            {"id": "c", "text": "2", "correct": False, "explanation": "Longer unique substrings exist."},
            {"id": "d", "text": "8", "correct": False, "explanation": "The whole string has duplicates."},
        ],
        "explanation": "'abc' is the longest substring without repeating characters.",
    },
    "explain": {
        "title": "Explain the Window",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why is the sliding window approach O(n) instead of O(n²)?”",
        "prompt": "Why is the sliding window approach O(n) instead of O(n²)?",
        "answer_format": "short_answer",
        "keywords": ["window", "slide", "shrink", "expand", "once", "character", "set", "o(n)", "linear"],
        "min_words": 10,
        "model_answer": (
            "Each character is added to the window once and removed once. "
            "The left and right pointers each move at most n steps, so the total work is O(n)."
        ),
        "intention": "The explanation must connect pointer movement to linear time.",
    },
    "guided_build": {
        "title": "Write the Window",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the sliding window.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Longest Unique Substring",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Expand right, shrink left on duplicate, track max.”",
                "description": "Return the length of the longest substring without repeating characters.",
                "starter_code": "def length_of_longest_substring(s):\n    seen = set()\n    left = 0\n    max_len = 0\n    for right, ch in enumerate(s):\n        while ch in seen:\n            seen.remove(s[left])\n            left += 1\n        seen.add(ch)\n        max_len = max(max_len, right - left + 1)\n    return max_len\n",
                "function_name": "length_of_longest_substring",
                "signature": "def length_of_longest_substring(s: str) -> int:",
                "test_cases": [
                    {"input": ["abcabcbb"], "expected": 3},
                    {"input": ["bbbbb"], "expected": 1},
                ],
                "hidden_test_cases": [
                    {"input": [""], "expected": 0},
                    {"input": ["pwwkew"], "expected": 3},
                    {"input": [" "], "expected": 1},
                ],
                "diamonds": 45,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use a set to track characters in the current window."},
                    {"level": 2, "text": "When you see a duplicate, shrink from the left until it's gone."},
                    {"level": 3, "text": "Track max_len = max(max_len, right - left + 1) after every expansion."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Fruit Basket",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same window idea. Collect at most two types of fruit.”",
        "description": (
            "Given an array of fruit types, return the length of the longest subarray "
            "containing at most two distinct types."
        ),
        "function_name": "total_fruit",
        "signature": "def total_fruit(fruits: List[int]) -> int:",
        "description_full": (
            "Return the length of the longest subarray with at most 2 distinct numbers.\n\n"
            "Example:\n"
            "  total_fruit([1, 2, 1]) -> 3\n\n"
            "This is the Fruit Into Baskets problem."
        ),
        "test_cases": [
            {"input": [[1, 2, 1]], "expected": 3},
            {"input": [[0, 1, 2, 2]], "expected": 3},
        ],
        "hidden_test_cases": [
            {"input": [[1, 2, 3, 2, 2]], "expected": 4},
            {"input": [[3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]], "expected": 5},
        ],
        "time_limit_minutes": 7,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Use a dict to count fruit types in the current window."},
            {"level": 2, "text": "When the dict has more than 2 keys, shrink from the left."},
            {"level": 3, "text": "Track max_len after every expansion."},
        ],
    },
    "assessment": {
        "title": "Unique Window Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove the window is automatic. Timed.”",
        "description": "Trace the window, explain O(n), and fix a reset bug.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "s = \"abba\"\nseen = set()\nleft = 0\nmax_len = 0\nfor right, ch in enumerate(s):\n    while ch in seen:\n        seen.remove(s[left])\n        left += 1\n    seen.add(ch)\n    max_len = max(max_len, right - left + 1)\nprint(max_len)",
                "answer_format": "single_number",
                "expected_answer": "2",
                "explanation": "Longest unique substrings are 'ab' and 'ba'. The window never restarts.",
            },
            {
                "type": "concept",
                "question": "Why does the sliding window approach run in O(n) time?",
                "answer_format": "short_answer",
                "keywords": ["window", "slide", "shrink", "expand", "once", "character", "set", "o(n)", "linear"],
                "explanation": "Each character is added and removed at most once.",
            },
            {
                "type": "debug",
                "code": "def length_of_longest_substring(s):\n    seen = set()\n    left = 0\n    max_len = 0\n    for right, ch in enumerate(s):\n        if ch in seen:\n            seen = set()\n            left = right + 1\n        seen.add(ch)\n        max_len = max(max_len, right - left + 1)\n    return max_len\n# should handle 'abba' correctly",
                "error": "On 'abba', returns 2 instead of 2 (works here) but fails on 'abba' because resetting loses 'b'.",
                "question": "Fix the window reset bug.",
                "fix": "while ch in seen:\n    seen.remove(s[left])\n    left += 1",
                "explanation": "Resetting the window to empty discards useful state. Shrinking from the left preserves O(n).",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Reset Window",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I replaced the shrink loop with a reset. Find the broken assumption.”",
        "story": (
            "A programmer reset the window to empty on duplicate instead of shrinking. "
            "On 'abba', the second 'a' causes a full reset, losing the 'b' that was still valid. "
            "What assumption is wrong?"
        ),
        "buggy_code": "def length_of_longest_substring(s):\n    seen = set()\n    left = 0\n    max_len = 0\n    for right, ch in enumerate(s):\n        if ch in seen:\n            seen = set()\n            left = right + 1\n        seen.add(ch)\n        max_len = max(max_len, right - left + 1)\n    return max_len\n",
        "expected_output": "2",
        "actual_output": "2 on 'abba' by luck, but breaks on longer strings like 'abbaef'",
        "diagnosis": {
            "question": "Which assumption makes this reset approach incorrect?",
            "options": [
                {"id": "a", "text": "It assumes resetting is equivalent to shrinking, but it discards valid characters", "correct": True, "why": "Resetting removes all characters, including ones that could still be part of the window."},
                {"id": "b", "text": "The set should be a dict", "correct": False, "why": "A set is sufficient for membership checks."},
                {"id": "c", "text": "The loop should be while instead of if", "correct": False, "why": "The loop condition is not the core issue; the reset is."},
                {"id": "d", "text": "The max_len update is wrong", "correct": False, "why": "max_len is updated correctly."},
            ],
        },
        "fix": "while ch in seen:\n    seen.remove(s[left])\n    left += 1",
        "fixed_code": "def length_of_longest_substring(s):\n    seen = set()\n    left = 0\n    max_len = 0\n    for right, ch in enumerate(s):\n        while ch in seen:\n            seen.remove(s[left])\n            left += 1\n        seen.add(ch)\n        max_len = max(max_len, right - left + 1)\n    return max_len\n",
        "explanation": (
            "Resetting the window discards characters that could still be part of a valid substring. "
            "Shrinking from the left preserves the window state and maintains O(n) time."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:sliding_window:longest_substring",
        "concept_name": "Longest Substring Without Repeating Characters",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "use a sliding window with left and right pointers",
            "use a set for O(1) membership checks",
            "shrink from the left when duplicate appears",
            "track max length after every expansion",
        ],
        "spaced_fields": [
            "window_expand",
            "window_shrink",
            "set_membership",
            "track_max",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "longest_substring_no_repeat",
        "unlocks_next": ["sliding_window_patterns"],
        "tower_badge": "unique_window",
        "world_node": {
            "level": 15,
            "title": "The Unique Window",
            "color": "teal",
            "icon": "🪟",
            "description": "Find longest unique substring in O(n) with sliding window",
        },
    },
}
