"""Curated Blind 75 catalog for PlacementPro.

The canonical Blind 75 problem list, sourced from the sibling NeetCode 150
seed file so every entry is LeetCode-exact with runnable stdin/stdout code.
Each question is re-tagged with `curated_source="blind75"` and keeps the
`neetcode150` source tag; the store's dedupe merges tags so filtering by
`source=blind75` or `source=neetcode150` both work.

Loaded by `app.services.question_store` after the striver catalog and before
the full NeetCode 150 catalog (so the richer neetcode variant wins title ties
and carries the merged source list).
"""

from __future__ import annotations

import importlib.util
import os

_BASE = os.path.dirname(os.path.abspath(__file__))
_NC_PATH = os.path.join(_BASE, "seed_questions_neetcode150.py")

_spec = importlib.util.spec_from_file_location("seed_questions_neetcode150", _NC_PATH)
_nc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_nc)

# Canonical Blind 75 ids (slug ids from the NeetCode 150 catalog). These are
# the 75 unique problems in the classic Blind 75 roadmap — Merge K Sorted Lists
# appears under both Linked List and Heap but is one problem, hence 75 not 76.
_BLIND75_SLUGS = {
    # Array
    "nc-two-sum", "nc-best-time-buy-sell-stock", "nc-contains-duplicate",
    "nc-product-array-except-self", "nc-maximum-subarray",
    "nc-maximum-product-subarray", "nc-find-min-rotated-sorted-array",
    "nc-search-rotated-sorted-array", "nc-3sum", "nc-container-with-most-water",
    # Binary
    "nc-sum-two-integers", "nc-number-of-1-bits", "nc-counting-bits",
    "nc-missing-number", "nc-reverse-bits",
    # Dynamic Programming
    "nc-climbing-stairs", "nc-coin-change", "nc-longest-increasing-subsequence",
    "nc-longest-common-subsequence", "nc-word-break", "nc-combination-sum",
    "nc-house-robber", "nc-house-robber-ii", "nc-decode-ways",
    "nc-unique-paths", "nc-jump-game",
    # Graph
    "nc-clone-graph", "nc-course-schedule", "nc-pacific-atlantic-water-flow",
    "nc-number-of-islands", "nc-longest-consecutive-sequence",
    "nc-alien-dictionary", "nc-graph-valid-tree",
    "nc-number-of-connected-components",
    # Interval
    "nc-insert-interval", "nc-merge-intervals", "nc-non-overlapping-intervals",
    "nc-meeting-rooms", "nc-meeting-rooms-ii",
    # Linked List
    "nc-reverse-linked-list", "nc-linked-list-cycle",
    "nc-merge-two-sorted-lists", "nc-merge-k-sorted-lists",
    "nc-remove-nth-from-end", "nc-reorder-list",
    # Matrix
    "nc-set-matrix-zeroes", "nc-spiral-matrix", "nc-rotate-image",
    "nc-word-search",
    # String
    "nc-longest-substring-no-repeat", "nc-longest-repeating-char-replacement",
    "nc-minimum-window-substring", "nc-valid-anagram", "nc-group-anagrams",
    "nc-valid-parentheses", "nc-valid-palindrome",
    "nc-longest-palindromic-substring", "nc-palindromic-substrings",
    "nc-encode-decode-strings",
    # Tree
    "nc-max-depth-binary-tree", "nc-same-tree", "nc-invert-binary-tree",
    "nc-binary-tree-max-path-sum", "nc-binary-tree-level-order",
    "nc-serialize-deserialize-tree", "nc-subtree-of-another-tree",
    "nc-construct-binary-tree", "nc-validate-binary-search-tree",
    "nc-kth-smallest-bst", "nc-lowest-common-ancestor-bst",
    "nc-implement-trie", "nc-design-add-search-words", "nc-word-search-ii",
    # Heap
    "nc-top-k-frequent-elements", "nc-find-median-data-stream",
}

questions = []
for q in _nc.questions:
    if q.get("id") not in _BLIND75_SLUGS:
        continue
    tagged = dict(q)
    tagged["curated_source"] = "blind75"
    tagged["sources"] = ["blind75", "neetcode150"]
    tagged["dsa_guide"] = dict(q.get("dsa_guide") or {})
    tagged["solution"] = dict(q.get("solution") or {})
    questions.append(tagged)
