"""
Flagship Lesson — House Robber
 ==============================

 Gold-standard interactive lesson for 1D DP with house robber.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "house_robber"

LESSON: Dict[str, Any] = {
    "lesson_id": "house_robber_dp_choose",
    "module_id": "dsa:dp_1d:house_robber",
    "title": "The Safe Pick",
    "description": "Maximize loot without robbing two adjacent houses using 1D DP.",
    "difficulty": "intermediate",
    "est_minutes": 14,
    "xp_reward": 120,
    "skills_taught": ["dynamic_programming", "house_robber", "optimization"],
    "srs_concept_tag": "dsa:dp_1d:house_robber",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Safe Pick has one rule: you cannot rob adjacent houses. "
            "At each house, choose the maximum of robbing it plus dp[i-2] or skipping to dp[i-1]. "
            "That choice is the recurrence.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You chose the better of two options at each house.”",
            "🧭 **Captain Byte**\n“Clean. The recurrence captures the adjacency constraint.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t greedily rob every other house. The recurrence decides.”",
            "🧭 **Captain Byte**\n“You’re summing all houses. Adjacent houses cannot both be robbed.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now respect the adjacency constraint.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any ‘choose or skip’ DP problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. At each house: rob it plus dp[i-2], or skip and keep dp[i-1].”",
    },
    "story_context": {
        "title": "The Safe Pick",
        "narration": (
            "The Safe Pick has one rule: you cannot rob adjacent houses. "
            "At each house, choose the maximum of robbing it plus dp[i-2] or skipping to dp[i-1]."
        ),
        "setting": "safe_pick",
        "character": "Captain Byte",
        "intro_text": (
            "House Robber is the canonical ‘choose or skip’ DP pattern. "
            "The recurrence is dp[i] = max(dp[i-1], nums[i] + dp[i-2])."
        ),
    },
    "discovery": {
        "title": "Choose or Skip",
        "visual_primitives": ["compare", "transform", "highlight"],
        "steps": [
            {
                "action": "recurrence",
                "narration": "At house i, you can rob it and skip i-1, or skip it and keep the best up to i-1.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def rob(nums):\n    a = b = 0\n    for x in nums:\n        a, b = b, max(b, a + x)\n    return b\n\nprint(rob([1, 2, 3, 1]))",
                    "expected_output": "4",
                    "hint": "Rob house 1 (1) and house 3 (3) = 4. Or rob house 2 (2) and house 4 (1) = 3. Max = 4.",
                },
            },
            {
                "action": "base_cases",
                "narration": "With no houses, loot is 0. With one house, loot is that house’s value.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "nums = [5]. What is the maximum loot?",
                    "options": [
                        {"id": "a", "text": "5", "correct": True},
                        {"id": "b", "text": "0", "correct": False},
                        {"id": "c", "text": "10", "correct": False},
                        {"id": "d", "text": "Depends on adjacency", "correct": False},
                    ],
                    "explanation": "With one house, you rob it. Loot = 5.",
                },
            },
            {
                "action": "why_not_greedy",
                "narration": "Greedy ‘rob every other house’ fails when values are uneven.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "nums = [2, 1, 1, 2]. Greedy every-other gives 2+1=3. What is optimal?",
                    "options": [
                        {"id": "a", "text": "4 — rob houses 1 and 4", "correct": True},
                        {"id": "b", "text": "3 — greedy is optimal", "correct": False},
                        {"id": "c", "text": "2 — rob only house 1", "correct": False},
                        {"id": "d", "text": "5 — rob all houses", "correct": False},
                    ],
                    "explanation": "Rob houses 1 and 4: 2 + 2 = 4. Greedy misses this.",
                },
            },
            {
                "action": "space_optimize",
                "narration": "Only the previous two values matter. O(1) space is enough.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def rob(nums):\n    a = b = 0\n    for x in nums:\n        a, b = b, max(b, a + x)\n    return b\n\nprint(rob([2, 7, 9, 3, 1]))",
                    "expected_output": "12",
                    "hint": "Rob 2 + 9 + 1 = 12. Or 7 + 3 = 10. Max = 12.",
                },
            },
        ],
        "conclusion": (
            "House Robber is dp[i] = max(dp[i-1], nums[i] + dp[i-2]). "
            "Only two previous values matter, so O(1) space suffices."
        ),
    },
    "prediction": {
        "title": "Before You Pick",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict the optimal loot.”",
        "question": "nums = [1, 2, 3, 1]. What is the maximum loot?",
        "options": [
            {"id": "a", "text": "4", "correct": True, "explanation": "Rob house 1 (1) and house 3 (3) = 4."},
            {"id": "b", "text": "3", "correct": False, "explanation": "Rob house 2 (2) and house 4 (1) = 3, but 4 is better."},
            {"id": "c", "text": "5", "correct": False, "explanation": "You cannot rob adjacent houses."},
            {"id": "d", "text": "2", "correct": False, "explanation": "Robbing only house 2 is suboptimal."},
        ],
        "explanation": "Rob house 1 and house 3: 1 + 3 = 4. This is optimal.",
    },
    "explain": {
        "title": "Explain the Choice",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does the recurrence use dp[i-2] when robbing house i?”",
        "prompt": "Why does the recurrence use dp[i-2] when robbing house i?",
        "answer_format": "short_answer",
        "keywords": ["adjacent", "skip", "i-1", "i-2", "rob", "cannot", "two", "house"],
        "min_words": 10,
        "model_answer": (
            "If you rob house i, you cannot rob house i-1 because they are adjacent. "
            "The best loot up to i-2 is dp[i-2]. Adding nums[i] gives the total when robbing i. "
            "Comparing with dp[i-1] (skipping i) yields the maximum."
        ),
        "intention": "The explanation must connect adjacency constraint to skipping i-1.",
    },
    "guided_build": {
        "title": "Write the Safe Pick",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the O(1) space DP.”",
        "steps": [
            {
                "step_order": 1,
                "title": "House Robber",
                "captain_byte_moment": "🧭 **Captain Byte**\n“dp[i] = max(dp[i-1], nums[i] + dp[i-2]). Keep only last two.”",
                "description": "Return the maximum amount of money you can rob without alerting the police.",
                "starter_code": "def rob(nums):\n    a = b = 0\n    for x in nums:\n        a, b = b, max(b, a + x)\n    return b\n",
                "function_name": "rob",
                "signature": "def rob(nums: List[int]) -> int:",
                "test_cases": [
                    {"input": [[1, 2, 3, 1]], "expected": 4},
                    {"input": [[2, 7, 9, 3, 1]], "expected": 12},
                ],
                "hidden_test_cases": [
                    {"input": [[]], "expected": 0},
                    {"input": [[5]], "expected": 5},
                    {"input": [[2, 1, 1, 2]], "expected": 4},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "At each house, choose: rob it + dp[i-2], or skip and keep dp[i-1]."},
                    {"level": 2, "text": "Only two previous values matter. Use a and b."},
                    {"level": 3, "text": "a = dp[i-2], b = dp[i-1]. Update: a, b = b, max(b, a + x)."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Circle of Houses",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Houses form a circle. The first and last are adjacent.”",
        "description": (
            "Houses are arranged in a circle. Rob the maximum amount without robbing adjacent houses."
        ),
        "function_name": "rob_circle",
        "signature": "def rob_circle(nums: List[int]) -> int:",
        "description_full": (
            "Return the maximum loot from circular houses.\n\n"
            "Example:\n"
            "  rob_circle([2, 3, 2]) -> 3\n\n"
            "Hint: run House Robber twice: once excluding first, once excluding last."
        ),
        "test_cases": [
            {"input": [[2, 3, 2]], "expected": 3},
            {"input": [[1, 2, 3, 1]], "expected": 4},
        ],
        "hidden_test_cases": [
            {"input": [[1, 2, 3]], "expected": 3},
            {"input": [[0]], "expected": 0},
        ],
        "time_limit_minutes": 7,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Run House Robber on nums[1:] and nums[:-1] separately."},
            {"level": 2, "text": "The first and last houses cannot both be robbed."},
            {"level": 3, "text": "Return max of the two runs."},
        ],
    },
    "assessment": {
        "title": "Safe Pick Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove the choose-or-skip pattern is automatic. Timed.”",
        "description": "Maximize loot, explain the recurrence, and fix a greedy bug.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "def rob(nums):\n    a = b = 0\n    for x in nums:\n        a, b = b, max(b, a + x)\n    return b\n\nprint(rob([2, 1, 1, 2]))",
                "answer_format": "single_number",
                "expected_answer": "4",
                "explanation": "Rob house 1 (2) and house 4 (2) = 4.",
            },
            {
                "type": "concept",
                "question": "Why can’t you simply sum every other house for maximum loot?",
                "answer_format": "short_answer",
                "keywords": ["adjacent", "skip", "greedy", "optimal", "choose", "recurrence", "dp"],
                "explanation": "Greedy every-other fails when values are uneven. The recurrence chooses optimally.",
            },
            {
                "type": "debug",
                "code": "def rob(nums):\n    return sum(nums[::2])\n# greedy every-other",
                "error": "rob([2, 1, 1, 2]) returns 3 instead of 4.",
                "question": "Fix the greedy approach with DP.",
                "fix": "a = b = 0\nfor x in nums:\n    a, b = b, max(b, a + x)\nreturn b",
                "explanation": "Greedy every-other misses the optimal 2+2=4. DP considers all valid combinations.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Greedy Grab",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I used greedy every-other. Find the broken assumption.”",
        "story": (
            "A programmer summed every other house. On [2, 1, 1, 2], they got 3 instead of 4. "
            "What assumption is wrong?"
        ),
        "buggy_code": "def rob(nums):\n    return sum(nums[::2])\n",
        "expected_output": "4",
        "actual_output": "3 — greedy every-other misses the optimal",
        "diagnosis": {
            "question": "Which assumption makes the greedy approach fail?",
            "options": [
                {"id": "a", "text": "It assumes every-other is always optimal", "correct": True, "why": "Greedy every-other misses cases like [2,1,1,2] where 2+2=4 is better."},
                {"id": "b", "text": "It uses slicing instead of a loop", "correct": False, "why": "Slicing is not the issue; the logic is."},
                {"id": "c", "text": "It doesn't handle empty arrays", "correct": False, "why": "Empty arrays would return 0, which is correct."},
                {"id": "d", "text": "It sums instead of maximizing", "correct": False, "why": "Summing every-other is the greedy approach; the issue is optimality."},
            ],
        },
        "fix": "Use DP: dp[i] = max(dp[i-1], nums[i] + dp[i-2])",
        "fixed_code": "def rob(nums):\n    a = b = 0\n    for x in nums:\n        a, b = b, max(b, a + x)\n    return b\n",
        "explanation": (
            "Greedy every-other assumes the optimal solution alternates houses, which is false. "
            "DP considers both choices at each house and picks the maximum."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:dp_1d:house_robber",
        "concept_name": "House Robber",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "dp[i] = max(dp[i-1], nums[i] + dp[i-2])",
            "cannot rob adjacent houses",
            "base cases: dp[0] = 0, dp[1] = nums[0]",
            "space optimization keeps only last two values",
        ],
        "spaced_fields": [
            "choose_or_skip",
            "adjacency_constraint",
            "recurrence",
            "space_optimize",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "house_robber",
        "unlocks_next": ["dp_1d_patterns"],
        "tower_badge": "safe_pick",
        "world_node": {
            "level": 27,
            "title": "The Safe Pick",
            "color": "teal",
            "icon": "💰",
            "description": "Maximize loot with 1D DP in O(n) time and O(1) space",
        },
    },
}
