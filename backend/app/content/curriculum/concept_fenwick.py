"""
Concept Clarity Slice: Fenwick Tree / Binary Indexed Tree
==========================================================

A Fenwick tree stores prefix sums in an array. It answers prefix-sum queries
and point updates in O(log n) using only O(n) space and a neat bit trick:
every index is responsible for a range whose size is its lowest set bit.

Misconceptions attacked:
  1. "Fenwick tree is hard to implement" — the core loop is only two lines
  2. "It can do any range query" — only prefix sums (or invertible operations)
  3. "It is slower than segment tree" — for pure prefix sums it is usually faster
"""
from typing import Dict, Any

FENWICK_SLICE: Dict[str, Any] = {
    "lesson_id": "fenwick_beacon",
    "module_id": "dsa:fenwick_tree",
    "title": "The Beacon Array",
    "description": "Learn Fenwick trees by maintaining prefix sums with point updates.",
    "difficulty": "hard",
    "est_minutes": 20,
    "xp_reward": 300,
    "skills_taught": ["fenwick_tree", "binary_indexed_tree", "prefix_sum", "bit_manipulation"],
    "srs_concept_tag": "dsa:fenwick_tree",
    "story_context": {
        "title": "The Beacon Array",
        "narration": (
            "The lighthouse beacon array records light intensity per tower. When a tower "
            "brightens, you must update every prefix that includes it. The Fenwick tree "
            "does exactly that using bit tricks."
        ),
        "setting": "lighthouse_array",
        "character": "Keeper Nolum",
        "intro_text": (
            "Each beacon stores a range of totals. I can update one tower and refresh "
            "only the ranges that include it."
        ),
    },
    "discovery": {
        "title": "Lowest Set Bit",
        "steps": [
            {
                "action": "inspect_bit",
                "narration": (
                    "Index 6 is 110 in binary. Its lowest set bit is 2, so node 6 is "
                    "responsible for a range of size 2."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "i = 6\nprint('Binary:', bin(i))\nprint('Lowest set bit:', i & -i)",
                    "expected_output": "Binary: 0b110\nLowest set bit: 2",
                    "hint": "x & -x isolates the lowest set bit.",
                },
            },
        ],
    },
    "manipulation": {
        "title": "Point Update",
        "steps": [
            {
                "action": "update",
                "narration": "Add 3 to index 2 and update every Fenwick node that covers it.",
                "interaction": {
                    "type": "code",
                    "starter_code": "fenwick = [0] * 9\n\ndef update(i, delta):\n    # TODO: walk upward using lowest set bit\n    pass\n\nupdate(2, 3)\nprint(fenwick[2], fenwick[4], fenwick[8])\n",
                    "solution": "fenwick = [0] * 9\n\ndef update(i, delta):\n    while i < len(fenwick):\n        fenwick[i] += delta\n        i += i & -i\n\nupdate(2, 3)\nprint(fenwick[2], fenwick[4], fenwick[8])\n",
                    "expected_output": "3 3 3\n",
                    "hint": "i += i & -i jumps to the next responsible node.",
                },
            },
        ],
    },
    "code": {
        "title": "Prefix Sum Query",
        "starter_code": "fenwick = [0] * 9\n\ndef update(i, delta):\n    while i < len(fenwick):\n        fenwick[i] += delta\n        i += i & -i\n\nupdate(1, 5)\nupdate(2, 3)\nupdate(3, 7)\n\ndef query(i):\n    # TODO: sum prefix [1..i]\n    pass\n\nprint(query(3))  # 5 + 3 + 7 = 15\n",
        "solution": "fenwick = [0] * 9\n\ndef update(i, delta):\n    while i < len(fenwick):\n        fenwick[i] += delta\n        i += i & -i\n\nupdate(1, 5)\nupdate(2, 3)\nupdate(3, 7)\n\ndef query(i):\n    s = 0\n    while i > 0:\n        s += fenwick[i]\n        i -= i & -i\n    return s\n\nprint(query(3))  # 15\n",
        "expected_output": "15\n",
    },
    "checks": [
        r"def query\(",
        r"i -= i & -i",
        r"while i > 0",
    ],
    "success": {
        "before": "You recompute prefix sums from scratch every time.",
        "after": "You update and query prefix sums in O(log n).",
        "title": "Beacon Array — you can build and use a Fenwick tree.",
        "lesson": "Fenwick trees trade range flexibility for speed and simplicity.",
        "next": "Try range sum with point updates on a larger array.",
    },
}
