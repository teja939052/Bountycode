"""Mystery box + hint system for DSA problems.

Mystery boxes are gamified hint unlocks. Instead of just showing hints,
students open mystery boxes to reveal them — adding surprise and delight.

Each mystery box contains:
  - A hint (progressive: vague → specific)
  - A mental model reminder
  - Sometimes a small Diamonds bonus or coin reward
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MysteryBox(BaseModel):
    """One mystery box — a gamified hint unlock."""
    id: str
    title: str
    icon: str = "🎁"
    description: str = ""
    hint: str
    mental_model: str = ""  # the core insight to remember
    xp_reward: int = 5  # small Diamonds for opening
    coin_reward: int = 0
    # Visual style
    rarity: str = "common"  # common, rare, epic, legendary
    color: str = "#3B82F6"


class HintLadder(BaseModel):
    """A progressive sequence of hints for a problem.

    Students unlock hints one at a time. Each hint gets more specific.
    The first hint is a nudge; the last is essentially the approach.
    """
    problem_id: str
    boxes: List[MysteryBox] = Field(default_factory=list)

    def get_box(self, index: int) -> Optional[MysteryBox]:
        if 0 <= index < len(self.boxes):
            return self.boxes[index]
        return None

    def total_boxes(self) -> int:
        return len(self.boxes)


# ─── Predefined hint ladders for common DSA patterns ────────────────

def two_sum_hints() -> HintLadder:
    return HintLadder(
        problem_id="two_sum",
        boxes=[
            MysteryBox(
                id="ts_1", title="Think About Lookup", icon="🔍",
                description="What if you could check if a number exists in O(1)?",
                hint="For each number, ask: what partner do I need? Then check if that partner already appeared.",
                mental_model="Hash maps turn 'find this element' from O(n) to O(1).",
                xp_reward=5, rarity="common",
            ),
            MysteryBox(
                id="ts_2", title="The Complement Trick", icon="🔢",
                description="For each number, there's exactly one partner that adds to target.",
                hint="For each num, compute complement = target - num. Check if complement is in a hash map. If yes, return indices. If no, add num to map.",
                mental_model="Instead of checking all pairs, check if the complement exists.",
                xp_reward=10, rarity="rare",
            ),
            MysteryBox(
                id="ts_3", title="Walk Through an Example", icon="🚶",
                description="Let's trace through [2, 7, 11, 15] with target = 9.",
                hint="num=2, complement=7, map empty → add {2:0}. num=7, complement=2, 2 in map → return [0,1]. Done in one pass.",
                mental_model="Single pass: check complement, then store current.",
                xp_reward=15, rarity="epic", color="#8B5CF6",
            ),
        ],
    )


def sliding_window_hints() -> HintLadder:
    return HintLadder(
        problem_id="sliding_window",
        boxes=[
            MysteryBox(
                id="sw_1", title="The Window", icon="🪟",
                description="Imagine a frame that slides across the array.",
                hint="Maintain a window [left, right]. Expand right to include new elements. Contract left when the window violates constraints.",
                mental_model="Sliding window = dynamic subarray that grows and shrinks.",
                xp_reward=5, rarity="common",
            ),
            MysteryBox(
                id="sw_2", title="Track the State", icon="📊",
                description="What changes when the window moves?",
                hint="Track what matters: current sum, current length, or current character set. Update incrementally — don't recompute from scratch.",
                mental_model="Incremental updates make it O(n) instead of O(n²).",
                xp_reward=10, rarity="rare",
            ),
            MysteryBox(
                id="sw_3", title="The Pattern Template", icon="📋",
                description="Most sliding window problems follow the same skeleton.",
                hint="Initialize left=0. For each right: add element, while invalid: remove left, move left. Track best answer. Return best.",
                mental_model="Expand → contract → track. That's the pattern.",
                xp_reward=15, rarity="epic", color="#8B5CF6",
            ),
        ],
    )


def binary_search_hints() -> HintLadder:
    return HintLadder(
        problem_id="binary_search",
        boxes=[
            MysteryBox(
                id="bs_1", title="Halve the Search", icon="✂️",
                description="Sorted array? You can eliminate half the candidates at once.",
                hint="Compare target to middle element. If target < middle, search left half. If target > middle, search right half. Repeat.",
                mental_model="Binary search = divide and conquer on sorted data. O(log n).",
                xp_reward=5, rarity="common",
            ),
            MysteryBox(
                id="bs_2", title="The Invariant", icon="🔒",
                description="Maintain: target is always between left and right.",
                hint="left=0, right=n-1. While left <= right: mid=(left+right)//2. If nums[mid]==target: return mid. If < target: left=mid+1. If >: right=mid-1.",
                mental_model="The loop invariant guarantees you never lose the target.",
                xp_reward=10, rarity="rare",
            ),
        ],
    )


def tree_dfs_hints() -> HintLadder:
    return HintLadder(
        problem_id="tree_dfs",
        boxes=[
            MysteryBox(
                id="td_1", title="Go Deep First", icon="⬇️",
                description="Trees are recursive structures. Use recursive thinking.",
                hint="Visit node → recurse left → recurse right. Base case: null node. That's the skeleton of every tree problem.",
                mental_model="Tree recursion: process node, then recurse on children.",
                xp_reward=5, rarity="common",
            ),
            MysteryBox(
                id="td_2", title="What to Return", icon="↩️",
                description="Each recursive call should return something useful.",
                hint="Decide: does each call return a value (max depth, sum) or does it mutate a global (collect paths)? Choose your pattern.",
                mental_model="Return values for bottom-up. Mutate globals for top-down.",
                xp_reward=10, rarity="rare",
            ),
        ],
    )


def dp_hints() -> HintLadder:
    return HintLadder(
        problem_id="dp",
        boxes=[
            MysteryBox(
                id="dp_1", title="Overlapping Subproblems", icon="🔄",
                description="Are you computing the same thing multiple times?",
                hint="If f(n) depends on f(n-1) and f(n-2), compute each once and store it. That's memoization — the heart of DP.",
                mental_model="DP = recursion + memoization. Solve each subproblem once.",
                xp_reward=5, rarity="common",
            ),
            MysteryBox(
                id="dp_2", title="The State", icon="📋",
                description="What's the minimum info you need to describe a subproblem?",
                hint="Define state: dp[i] = answer for subproblem of size i. Find recurrence: dp[i] = f(dp[i-1], dp[i-2], ...). That's your DP.",
                mental_model="State + recurrence + base case = DP solution.",
                xp_reward=10, rarity="rare",
            ),
            MysteryBox(
                id="dp_3", title="Bottom-Up vs Top-Down", icon="🔽",
                description="Two ways to fill the table.",
                hint="Top-down: recursive + memo. Natural but stack overhead. Bottom-up: iterative + array. Faster but less intuitive. Start top-down.",
                mental_model="Top-down = think recursively. Bottom-up = think iteratively.",
                xp_reward=15, rarity="epic", color="#8B5CF6",
            ),
        ],
    )


# ─── Registry ──────────────────────────────────────────────────────

HINT_LADDERS: Dict[str, HintLadder] = {
    "two_sum": two_sum_hints(),
    "sliding_window": sliding_window_hints(),
    "binary_search": binary_search_hints(),
    "tree_dfs": tree_dfs_hints(),
    "dp": dp_hints(),
}


def get_hint_ladder(problem_id: str) -> Optional[HintLadder]:
    return HINT_LADDERS.get(problem_id)


def get_hint(problem_id: str, box_index: int) -> Optional[MysteryBox]:
    ladder = HINT_LADDERS.get(problem_id)
    if ladder:
        return ladder.get_box(box_index)
    return None


def total_boxes_for_problem(problem_id: str) -> int:
    ladder = HINT_LADDERS.get(problem_id)
    return ladder.total_boxes() if ladder else 0
