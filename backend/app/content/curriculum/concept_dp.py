"""
Concept Clarity Slice: Dynamic Programming
============================================

Dynamic programming solves problems by breaking them into overlapping
subproblems and storing results so each subproblem is solved once. The two
signals: optimal substructure and overlapping subproblems.

Misconceptions attacked:
  1. "DP is memorization" — memoization is one flavor; tabulation is another
  2. "DP is only for recursion" — tabulation is often iterative
  3. "DP is always O(n^2)" — with state reduction it can be O(n)
"""
from typing import Dict, Any

DP_SLICE: Dict[str, Any] = {
    "lesson_id": "dp_climber",
    "module_id": "dsa:dp",
    "title": "The Stair Climber",
    "description": "Learn DP by counting ways to climb stairs with memoization and tabulation.",
    "difficulty": "medium",
    "est_minutes": 20,
    "xp_reward": 290,
    "skills_taught": ["dynamic_programming", "memoization", "tabulation", "recursion"],
    "srs_concept_tag": "dsa:dp",
    "story_context": {
        "title": "The Stair Climber",
        "narration": (
            "You may climb 1 or 2 steps at a time. How many ways reach the top of n "
            "stairs? The answer reuses smaller stair counts. That reuse is the DP signal."
        ),
        "setting": "stone_stairs",
        "character": "Guide Pem",
        "intro_text": (
            "Every landing remembers how many ways it took to get there. "
            "Reuse those counts instead of recalculating them."
        ),
    },
    "discovery": {
        "title": "Overlapping Subproblems",
        "steps": [
            {
                "action": "count_ways",
                "narration": (
                    "To reach step 3 you can come from step 2 or step 1. "
                    "Ways(3) = Ways(2) + Ways(1). The same subproblem appears many times."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "def ways(n):\n    if n <= 1:\n        return 1\n    return ways(n-1) + ways(n-2)\n\nprint('Ways(3):', ways(3))\nprint('Ways(4):', ways(4))",
                    "expected_output": "Ways(3): 3\nWays(4): 5",
                    "hint": "Ways(3) reuses Ways(2) and Ways(1).",
                },
            },
        ],
    },
    "manipulation": {
        "title": "Memoize the Climber",
        "steps": [
            {
                "action": "memoize",
                "narration": "Store each result so repeated calls return instantly.",
                "interaction": {
                    "type": "code",
                    "starter_code": "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef ways(n):\n    # TODO: base cases and recurrence\n    pass\n\nprint(ways(35))\n",
                    "solution": "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef ways(n):\n    if n <= 1:\n        return 1\n    return ways(n-1) + ways(n-2)\n\nprint(ways(35))\n",
                    "expected_output": "14930352\n",
                    "hint": "The recurrence is the same; the decorator caches results.",
                },
            },
        ],
    },
    "code": {
        "title": "Tabulated Climb Stairs",
        "starter_code": "def climb_stairs(n):\n    # TODO: iterative DP array\n    pass\n\nprint(climb_stairs(2))  # 2\nprint(climb_stairs(3))  # 3\nprint(climb_stairs(5))  # 8\n",
        "solution": "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n\nprint(climb_stairs(2))\nprint(climb_stairs(3))\nprint(climb_stairs(5))\n",
        "expected_output": "2\n3\n8\n",
    },
    "checks": [
        r"def climb_stairs\(",
        r"a, b = b, a \+ b",
        r"for _ in range\(",
    ],
    "success": {
        "before": "You recompute the same stair counts again and again.",
        "after": "You store results and reuse them in O(n) time.",
        "title": "Stair Climber — you can solve DP with memoization and tabulation.",
        "lesson": "DP turns exponential recursion into linear or polynomial work by caching.",
        "next": "Try knapsack or longest increasing subsequence next.",
    },
}
