"""
Concept Clarity Slice: Segment Tree
=====================================

A segment tree stores an array in a binary tree where each node represents a
range and stores a combined value (sum, min, max). Range queries and point
updates both run in O(log n).

Misconceptions attacked:
  1. "Segment tree is only for sum" — any associative operation works (min, max, gcd)
  2. "You need 4N space" — 4N is a safe upper bound; actual usage is closer to 2N
  3. "It is the same as a binary indexed tree" — BIT is simpler but not all operations fit
"""
from typing import Dict, Any

SEGMENT_SLICE: Dict[str, Any] = {
    "lesson_id": "segment_tree_guard",
    "module_id": "dsa:segment_tree",
    "title": "The Range Guard",
    "description": "Learn segment trees by protecting ranges of a village watch log.",
    "difficulty": "hard",
    "est_minutes": 22,
    "xp_reward": 320,
    "skills_taught": ["segment_tree", "range_query", "point_update", "divide_conquer"],
    "srs_concept_tag": "dsa:segment_tree",
    "story_context": {
        "title": "The Range Guard",
        "narration": (
            "The village watch log records guard counts per tower. When a messenger asks "
            "'how many guards from tower 2 to 7?', the Range Guard does not recount every "
            "tower. It returns the answer from precomputed ranges in O(log n)."
        ),
        "setting": "village_watch",
        "character": "Captain Veyra",
        "intro_text": (
            "Every tower belongs to a range. I combine ranges so any question about "
            "a sub-range can be answered quickly."
        ),
    },
    "discovery": {
        "title": "Ranges Inside Ranges",
        "steps": [
            {
                "action": "split_range",
                "narration": (
                    "A watch log of 8 towers is split into halves, then halves again. "
                    "Each node stores the sum of its towers."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "arr = [1, 2, 3, 4, 5, 6, 7, 8]\n# total = 36\nprint(sum(arr))",
                    "expected_output": "36",
                    "hint": "The root stores the total. Children store halves.",
                },
            },
        ],
    },
    "manipulation": {
        "title": "Build a Sum Segment Tree",
        "steps": [
            {
                "action": "build",
                "narration": "Build a segment tree for sums from an array of length 8.",
                "interaction": {
                    "type": "code",
                    "starter_code": "def build(arr, node=0, l=0, r=None):\n    if r is None:\n        r = len(arr) - 1\n    # TODO: store sum at tree[node]\n    pass\n\narr = [1, 2, 3, 4, 5, 6, 7, 8]\nbuild(arr)\n",
                    "solution": "tree = [0] * 32\n\ndef build(arr, node=0, l=0, r=None):\n    if r is None:\n        r = len(arr) - 1\n    if l == r:\n        tree[node] = arr[l]\n    else:\n        mid = (l + r) // 2\n        build(arr, node * 2 + 1, l, mid)\n        build(arr, node * 2 + 2, mid + 1, r)\n        tree[node] = tree[node * 2 + 1] + tree[node * 2 + 2]\n\narr = [1, 2, 3, 4, 5, 6, 7, 8]\nbuild(arr)\nprint(tree[0])  # 36\n",
                    "expected_output": "36\n",
                    "hint": "Leaf nodes store one array value; parents store the sum of children.",
                },
            },
        ],
    },
    "code": {
        "title": "Range Sum Query",
        "starter_code": "tree = [0] * 32\n\ndef build(arr, node=0, l=0, r=None):\n    if r is None:\n        r = len(arr) - 1\n    if l == r:\n        tree[node] = arr[l]\n    else:\n        mid = (l + r) // 2\n        build(arr, node * 2 + 1, l, mid)\n        build(arr, node * 2 + 2, mid + 1, r)\n        tree[node] = tree[node * 2 + 1] + tree[node * 2 + 2]\n\narr = [1, 2, 3, 4, 5, 6, 7, 8]\nbuild(arr)\n\ndef query(node, l, r, ql, qr):\n    # TODO: return sum on [ql, qr]\n    pass\n\nprint(query(0, 0, 7, 2, 5))  # 3 + 4 + 5 + 6 = 18\n",
        "solution": "tree = [0] * 32\n\ndef build(arr, node=0, l=0, r=None):\n    if r is None:\n        r = len(arr) - 1\n    if l == r:\n        tree[node] = arr[l]\n    else:\n        mid = (l + r) // 2\n        build(arr, node * 2 + 1, l, mid)\n        build(arr, node * 2 + 2, mid + 1, r)\n        tree[node] = tree[node * 2 + 1] + tree[node * 2 + 2]\n\narr = [1, 2, 3, 4, 5, 6, 7, 8]\nbuild(arr)\n\ndef query(node, l, r, ql, qr):\n    if ql > r or qr < l:\n        return 0\n    if ql <= l and r <= qr:\n        return tree[node]\n    mid = (l + r) // 2\n    left = query(node * 2 + 1, l, mid, ql, qr)\n    right = query(node * 2 + 2, mid + 1, r, ql, qr)\n    return left + right\n\nprint(query(0, 0, 7, 2, 5))  # 18\n",
        "expected_output": "18\n",
    },
    "checks": [
        r"def query\(",
        r"return left \+ right",
    ],
    "success": {
        "before": "You recount towers for every range query.",
        "after": "You answer range queries in O(log n) using precomputed ranges.",
        "title": "Range Guard — you can build and query a segment tree.",
        "lesson": "Segment trees turn range problems into tree traversals.",
        "next": "Try range minimum queries or lazy propagation next.",
    },
}
