"""
Flagship Lesson — Climbing Stairs
 =================================

 Gold-standard interactive lesson for 1D DP fundamentals.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "climbing_stairs"

LESSON: Dict[str, Any] = {
    "lesson_id": "climbing_stairs_dp_fib",
    "module_id": "dsa:dp_1d:climbing_stairs",
    "title": "The Step Builder",
    "description": "Count ways to climb n stairs taking 1 or 2 steps using 1D DP.",
    "difficulty": "intermediate",
    "est_minutes": 14,
    "xp_reward": 120,
    "skills_taught": ["dynamic_programming", "climbing_stairs", "fibonacci"],
    "srs_concept_tag": "dsa:dp_1d:climbing_stairs",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Step Builder is the gateway to 1D DP. To reach step n, you can come from step n-1 or step n-2. "
            "The recurrence is dp[n] = dp[n-1] + dp[n-2]. Every 1D DP problem asks: what are the subproblems, "
            "and how do they combine?”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You identified the recurrence and built up from base cases.”",
            "🧭 **Captain Byte**\n“Clean. DP turns exponential recursion into linear time.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t brute-force all paths. What is the recurrence?”",
            "🧭 **Captain Byte**\n“You’re recomputing subproblems. Cache them.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now build from base cases upward.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any 1D DP problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. What are the base cases? What is the recurrence?”",
    },
    "story_context": {
        "title": "The Step Builder",
        "narration": (
            "The Step Builder is the gateway to 1D DP. To reach step n, you can come from step n-1 or step n-2. "
            "The recurrence is dp[n] = dp[n-1] + dp[n-2]."
        ),
        "setting": "step_builder",
        "character": "Captain Byte",
        "intro_text": (
            "1D DP problems are solved by identifying the recurrence and building from base cases. "
            "Climbing Stairs is the Fibonacci recurrence in disguise."
        ),
    },
    "discovery": {
        "title": "Build the Steps",
        "visual_primitives": ["transform", "merge", "highlight"],
        "steps": [
            {
                "action": "base_cases",
                "narration": "To reach step 0, there is 1 way (do nothing). To reach step 1, there is 1 way (one 1-step).",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "How many ways to reach step 0?",
                    "options": [
                        {"id": "a", "text": "1 (empty sequence)", "correct": True},
                        {"id": "b", "text": "0", "correct": False},
                        {"id": "c", "text": "1 (one 1-step)", "correct": False},
                        {"id": "d", "text": "Depends on n", "correct": False},
                    ],
                    "explanation": "There is exactly 1 way to stay at step 0: do nothing.",
                },
            },
            {
                "action": "recurrence",
                "narration": "To reach step n, you can come from n-1 (1 step) or n-2 (2 steps). The ways add.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n\nprint(climb_stairs(5))",
                    "expected_output": "8",
                    "hint": "Ways to reach 5: 11111, 1112, 1121, 1211, 2111, 122, 212, 221.",
                },
            },
            {
                "action": "memoization",
                "narration": "The naive recursive solution recomputes the same subproblems. Memoization caches them.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "from functools import lru_cache\n\ndef climb_stairs(n):\n    @lru_cache(None)\n    def dp(i):\n        if i <= 2:\n            return i\n        return dp(i - 1) + dp(i - 2)\n    return dp(n)\n\nprint(climb_stairs(5))",
                    "expected_output": "8",
                    "hint": "Memoization turns O(2^n) recursion into O(n).",
                },
            },
            {
                "action": "tabulation",
                "narration": "Tabulation builds the dp array from bottom to top, avoiding recursion entirely.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "What is the time complexity of the tabulated DP solution?",
                    "options": [
                        {"id": "a", "text": "O(n)", "correct": True},
                        {"id": "b", "text": "O(2^n)", "correct": False},
                        {"id": "c", "text": "O(n^2)", "correct": False},
                        {"id": "d", "text": "O(log n)", "correct": False},
                    ],
                    "explanation": "The loop runs n times, doing O(1) work each iteration.",
                },
            },
        ],
        "conclusion": (
            "Climbing Stairs is dp[n] = dp[n-1] + dp[n-2] with base cases dp[1] = 1, dp[2] = 2. "
            "Memoization or tabulation both give O(n) time."
        ),
    },
    "prediction": {
        "title": "Before You Build",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict the recurrence.”",
        "question": "How many ways to climb 4 stairs taking 1 or 2 steps at a time?",
        "options": [
            {"id": "a", "text": "5", "correct": True, "explanation": "1111, 1112, 1121, 1211, 2111, 122, 212, 221 — actually 5 is wrong, correct is 5 ways."},
            {"id": "b", "text": "4", "correct": False, "explanation": "There are more than 4 ways."},
            {"id": "c", "text": "6", "correct": False, "explanation": "The correct count is 5."},
            {"id": "d", "text": "8", "correct": False, "explanation": "8 is for 5 stairs, not 4."},
        ],
        "explanation": "There are 5 ways to climb 4 stairs: 1111, 1112, 1121, 1211, 2111, 122, 212, 221 — wait, that's 8. Let me recalculate: for n=4, dp[4] = dp[3] + dp[2] = 3 + 2 = 5. Ways: 1111, 1112, 1121, 1211, 2111, 122, 212, 221 — that's 8. Actually dp[4] = 5 is correct: 1111, 1112, 1121, 1211, 2111, 122, 212, 221 = 8? No wait: for n=3: 111, 12, 21 = 3. For n=4: 1111, 112, 121, 211, 22 = 5. Yes, 5 is correct.",
    },
    "explain": {
        "title": "Explain the Recurrence",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why is dp[n] = dp[n-1] + dp[n-2]?”",
        "prompt": "Why is dp[n] = dp[n-1] + dp[n-2]?",
        "answer_format": "short_answer",
        "keywords": ["last", "step", "one", "two", "n-1", "n-2", "recurrence", "combine"],
        "min_words": 10,
        "model_answer": (
            "To reach step n, the last move must be a 1-step from n-1 or a 2-step from n-2. "
            "The ways to reach n are the sum of ways to reach n-1 and ways to reach n-2. "
            "These subproblems are independent, so we add them."
        ),
        "intention": "The explanation must connect the last move to the recurrence.",
    },
    "guided_build": {
        "title": "Write the Builder",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the tabulated DP.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Climb Stairs",
                "captain_byte_moment": "🧭 **Captain Byte**\n“dp[n] = dp[n-1] + dp[n-2]. Base: dp[1] = 1, dp[2] = 2.”",
                "description": "Return the number of distinct ways to climb n stairs.",
                "starter_code": "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n",
                "function_name": "climb_stairs",
                "signature": "def climb_stairs(n: int) -> int:",
                "test_cases": [
                    {"input": [2], "expected": 2},
                    {"input": [3], "expected": 3},
                ],
                "hidden_test_cases": [
                    {"input": [4], "expected": 5},
                    {"input": [5], "expected": 8},
                    {"input": [1], "expected": 1},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "dp[1] = 1, dp[2] = 2."},
                    {"level": 2, "text": "dp[n] = dp[n-1] + dp[n-2]."},
                    {"level": 3, "text": "Only keep the last two values to save space."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Jump Array",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same DP idea. You can jump up to nums[i] steps from index i.”",
        "description": (
            "Given an array of max jump lengths, return the minimum number of jumps to reach the last index."
        ),
        "function_name": "jump",
        "signature": "def jump(nums: List[int]) -> int:",
        "description_full": (
            "Return the minimum number of jumps to reach the last index.\n\n"
            "Example:\n"
            "  jump([2, 3, 1, 1, 4]) -> 2\n\n"
            "You start at index 0. Each nums[i] is the max jump length from that position."
        ),
        "test_cases": [
            {"input": [[2, 3, 1, 1, 4]], "expected": 2},
            {"input": [[2, 3, 0, 1, 4]], "expected": 2},
        ],
        "hidden_test_cases": [
            {"input": [[1, 2]], "expected": 1},
            {"input": [[1, 1, 1, 1]], "expected": 3},
        ],
        "time_limit_minutes": 7,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Track the farthest reachable index at each step."},
            {"level": 2, "text": "When current index exceeds current end, increment jumps and update end."},
            {"level": 3, "text": "The answer is the number of times you cross a current-end boundary."},
        ],
    },
    "assessment": {
        "title": "Step Builder Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove the recurrence is automatic. Timed.”",
        "description": "Count ways, explain dp[n], and fix a base-case bug.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\nprint(climb_stairs(5))",
                "answer_format": "single_number",
                "expected_answer": "8",
                "explanation": "dp[3]=3, dp[4]=5, dp[5]=8.",
            },
            {
                "type": "concept",
                "question": "Why is dp[n] = dp[n-1] + dp[n-2] for climbing stairs?",
                "answer_format": "short_answer",
                "keywords": ["last", "step", "one", "two", "n-1", "n-2", "recurrence", "combine"],
                "explanation": "The last move is either 1 step or 2 steps. The ways add.",
            },
            {
                "type": "debug",
                "code": "def climb_stairs(n):\n    if n == 0:\n        return 0\n    if n == 1:\n        return 1\n    return climb_stairs(n-1) + climb_stairs(n-2)\n# should return 2 for n=2",
                "error": "climb_stairs(0) returns 0 instead of 1. The base case is wrong.",
                "question": "Fix the base case for n = 0.",
                "fix": "if n == 0:\n    return 1",
                "explanation": "There is 1 way to climb 0 stairs: do nothing.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Missing Base",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I removed the n=0 base case. Find the broken assumption.”",
        "story": (
            "A programmer wrote dp[0] = 0 instead of dp[0] = 1. "
            "On n=2, the recurrence gives dp[2] = dp[1] + dp[0] = 1 + 0 = 1 instead of 2. "
            "What assumption is wrong?"
        ),
        "buggy_code": "def climb_stairs(n):\n    if n == 0:\n        return 0\n    if n == 1:\n        return 1\n    a, b = 1, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n",
        "expected_output": "2",
        "actual_output": "1 for n=2 — wrong base case",
        "diagnosis": {
            "question": "Which assumption makes this DP fail?",
            "options": [
                {"id": "a", "text": "It assumes dp[0] = 0, but there is 1 way to climb 0 stairs", "correct": True, "why": "dp[0] = 1 is the correct base case for the recurrence to work."},
                {"id": "b", "text": "The recurrence is wrong", "correct": False, "why": "dp[n] = dp[n-1] + dp[n-2] is correct."},
                {"id": "c", "text": "The loop starts at the wrong index", "correct": False, "why": "The loop range is correct."},
                {"id": "d", "text": "The return value is wrong", "correct": False, "why": "Returning b is correct."},
            ],
        },
        "fix": "if n == 0:\n    return 1",
        "fixed_code": "def climb_stairs(n):\n    if n == 0:\n        return 1\n    if n == 1:\n        return 1\n    a, b = 1, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n",
        "explanation": (
            "dp[0] = 1 represents the empty sequence of moves. "
            "Without it, the recurrence undercounts for n >= 2."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:dp_1d:climbing_stairs",
        "concept_name": "Climbing Stairs",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "base cases: dp[0] = 1, dp[1] = 1",
            "recurrence: dp[n] = dp[n-1] + dp[n-2]",
            "tabulation builds from bottom up",
            "space optimization keeps only last two values",
        ],
        "spaced_fields": [
            "base_cases",
            "recurrence",
            "tabulation",
            "space_optimize",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "climbing_stairs",
        "unlocks_next": ["dp_1d_patterns"],
        "tower_badge": "step_builder",
        "world_node": {
            "level": 26,
            "title": "The Step Builder",
            "color": "teal",
            "icon": "🪜",
            "description": "Count climbing ways with 1D DP in O(n) time and O(1) space",
        },
    },
}
