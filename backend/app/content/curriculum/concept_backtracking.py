"""
Concept Clarity Slice: Backtracking
====================================

Backtracking is depth-first search with a undo step. You build a solution
incrementally, and when the current path can never become valid, you back out
and try a different choice.

Misconceptions attacked:
  1. "Backtracking is recursion" — the recursion is just the shape; the undo is the point
  2. "We explore every permutation" — no; we prune invalid branches early
  3. "Backtracking is always slow" — with pruning it is often the fastest exact solver
"""
from typing import Dict, Any

BACKTRACK_SLICE: Dict[str, Any] = {
    "lesson_id": "backtracking_garden",
    "module_id": "dsa:backtracking",
    "title": "The Maze Garden",
    "description": "Learn backtracking by exploring a maze and undoing dead-end moves.",
    "difficulty": "medium",
    "est_minutes": 18,
    "xp_reward": 280,
    "skills_taught": ["backtracking", "recursion", "dfs", "pruning"],
    "srs_concept_tag": "dsa:backtracking",
    "story_context": {
        "title": "The Maze Garden",
        "narration": (
            "The Maze Garden has hedges, open paths, and one exit. You may walk forward, "
            "but if a path dead-ends you must step back to the last choice and try a different "
            "direction. That step-back is backtracking."
        ),
        "setting": "maze_garden",
        "character": "Guide Rowan",
        "intro_text": (
            "Every path you take here can be undone. Choose a direction, walk forward, "
            "and if the hedge blocks you, come back and try the next opening."
        ),
    },
    "discovery": {
        "title": "Choose and Undo",
        "steps": [
            {
                "action": "walk_path",
                "narration": (
                    "At a fork, you choose left. After two steps the path ends. "
                    "Backtrack to the fork, then choose right."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "def walk(path):\n    if path == ['left', 'left', 'dead']:\n        return 'backtrack'\n    return 'continue'\n\nprint(walk(['left', 'left', 'dead']))",
                    "expected_output": "backtrack",
                    "hint": "Dead ends trigger the undo step.",
                },
            },
        ],
    },
    "manipulation": {
        "title": "Permute a Mini List",
        "steps": [
            {
                "action": "permute",
                "narration": "Generate permutations of [1, 2] by choosing an element, recursing, and undoing the choice.",
                "interaction": {
                    "type": "code",
                    "starter_code": "def permute(path, choices):\n    if not choices:\n        print(path)\n        return\n    # TODO: try each choice, recurse, then backtrack\n    pass\n\npermute([], [1, 2])\n",
                    "solution": "def permute(path, choices):\n    if not choices:\n        print(path)\n        return\n    for i, choice in enumerate(choices):\n        path.append(choice)\n        remaining = choices[:i] + choices[i+1:]\n        permute(path, remaining)\n        path.pop()\n\npermute([], [1, 2])\n",
                    "expected_output": "[1, 2]\n[2, 1]\n",
                    "hint": "Append, recurse, then pop to undo.",
                },
            },
        ],
    },
    "code": {
        "title": "Subset Sum via Backtracking",
        "starter_code": "def subset_sum(nums, target):\n    # TODO: return True if some subset sums to target\n    pass\n\nprint(subset_sum([2, 3, 5], 8))  # True: 3 + 5\nprint(subset_sum([1, 2, 5], 4))  # False\n",
        "solution": "def subset_sum(nums, target):\n    def backtrack(i, current):\n        if current == target:\n            return True\n        if i == len(nums) or current > target:\n            return False\n        # Take nums[i]\n        if backtrack(i + 1, current + nums[i]):\n            return True\n        # Skip nums[i]\n        if backtrack(i + 1, current):\n            return True\n        return False\n    return backtrack(0, 0)\n\nprint(subset_sum([2, 3, 5], 8))  # True\nprint(subset_sum([1, 2, 5], 4))  # False\n",
        "expected_output": "True\nFalse\n",
    },
    "checks": [
        r"def subset_sum\(",
        r"backtrack\(",
        r"current \+=",
    ],
    "success": {
        "before": "You try every combination blindly.",
        "after": "You explore only promising branches and undo dead ends fast.",
        "title": "Maze Garden — you can prune and backtrack with purpose.",
        "lesson": "Backtracking turns exponential search into a guided search with undo.",
        "next": "Try N-Queens or Sudoku solver next.",
    },
}
