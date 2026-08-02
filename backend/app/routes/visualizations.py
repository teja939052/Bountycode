"""
Visual Dry Runs — Step-by-step algorithm visualization.
50+ pre-built templates + AI-generated traces for any code.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import curated_questions_collection
from app.services.ai import chat_completion, parse_json
from app.services.code_tracer import execute_with_trace, detect_algorithm_type

router = APIRouter(prefix="/api/v1/visualizations", tags=["visualizations"])


class TraceRequest(BaseModel):
    code: str
    language: str = "python"
    stdin: str = ""


# ─────────────────────────────────────────────
#  50+ PRE-BUILT VISUALIZATION TEMPLATES
# ─────────────────────────────────────────────
VISUALIZATION_TEMPLATES: Dict[str, Dict[str, Any]] = {
    # ── SORTING (8) ──
    "bubble_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Bubble sort — repeatedly swap adjacent elements",
        "example_input": [5, 3, 8, 1, 2],
        "steps": [
            {"step": 1, "array": [5, 3, 8, 1, 2], "compare": [0, 1], "action": "Compare 5 and 3 → swap"},
            {"step": 2, "array": [3, 5, 8, 1, 2], "compare": [1, 2], "action": "Compare 5 and 8 → keep"},
            {"step": 3, "array": [3, 5, 8, 1, 2], "compare": [2, 3], "action": "Compare 8 and 1 → swap"},
            {"step": 4, "array": [3, 5, 1, 8, 2], "compare": [3, 4], "action": "Compare 8 and 2 → swap"},
            {"step": 5, "array": [3, 5, 1, 2, 8], "sorted": [4], "action": "Pass 1 done, 8 is sorted"},
            {"step": 6, "array": [3, 5, 1, 2, 8], "compare": [0, 1], "action": "Compare 3 and 5 → keep"},
            {"step": 7, "array": [3, 5, 1, 2, 8], "compare": [1, 2], "action": "Compare 5 and 1 → swap"},
            {"step": 8, "array": [3, 1, 5, 2, 8], "compare": [2, 3], "action": "Compare 5 and 2 → swap"},
            {"step": 9, "array": [3, 1, 2, 5, 8], "sorted": [3, 4], "action": "Pass 2 done"},
            {"step": 10, "array": [1, 2, 3, 5, 8], "action": "Array is sorted!"},
        ]
    },
    "selection_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Selection sort — find minimum, place at front",
        "example_input": [64, 25, 12, 22, 11],
        "steps": [
            {"step": 1, "array": [64, 25, 12, 22, 11], "scan": [0, 1, 2, 3, 4], "action": "Find minimum from index 0 → found 11"},
            {"step": 2, "array": [11, 25, 12, 22, 64], "sorted": [0], "action": "Swap 11 with 64"},
            {"step": 3, "array": [11, 25, 12, 22, 64], "scan": [1, 2, 3, 4], "action": "Find minimum from index 1 → found 12"},
            {"step": 4, "array": [11, 12, 25, 22, 64], "sorted": [0, 1], "action": "Swap 12 with 25"},
            {"step": 5, "array": [11, 12, 22, 25, 64], "sorted": [0, 1, 2], "action": "Array is sorted!"},
        ]
    },
    "insertion_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Insertion sort — insert each element into sorted portion",
        "example_input": [5, 2, 4, 6, 1, 3],
        "steps": [
            {"step": 1, "array": [5, 2, 4, 6, 1, 3], "sorted": [0], "key": 2, "action": "Key=2, shift 5 right"},
            {"step": 2, "array": [2, 5, 4, 6, 1, 3], "sorted": [0, 1], "key": 4, "action": "Key=4, shift 5 right"},
            {"step": 3, "array": [2, 4, 5, 6, 1, 3], "sorted": [0, 1, 2], "key": 6, "action": "Key=6, already in place"},
            {"step": 4, "array": [2, 4, 5, 6, 1, 3], "sorted": [0, 1, 2, 3], "key": 1, "action": "Key=1, shift 6,5,4,2 right"},
            {"step": 5, "array": [1, 2, 4, 5, 6, 3], "sorted": [0, 1, 2, 3, 4], "key": 3, "action": "Key=3, shift 6,5,4 right"},
            {"step": 6, "array": [1, 2, 3, 4, 5, 6], "sorted": [0, 1, 2, 3, 4, 5], "action": "Array is sorted!"},
        ]
    },
    "merge_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Merge sort — divide, sort, merge",
        "example_input": [38, 27, 43, 3, 9, 82, 10],
        "steps": [
            {"step": 1, "array": [38, 27, 43, 3, 9, 82, 10], "action": "Split: [38,27,43] and [3,9,82,10]"},
            {"step": 2, "array": [38, 27, 43], "action": "Split: [38] and [27,43]"},
            {"step": 3, "array": [27, 43], "action": "Split: [27] and [43]"},
            {"step": 4, "array": [27, 43], "action": "Merge [27] + [43] → [27,43]"},
            {"step": 5, "array": [27, 38, 43], "action": "Merge [38] + [27,43] → [27,38,43]"},
            {"step": 6, "array": [3, 9, 82, 10], "action": "Split: [3,9] and [82,10]"},
            {"step": 7, "array": [3, 9], "action": "Merge [3] + [9] → [3,9]"},
            {"step": 8, "array": [10, 82], "action": "Merge [82] + [10] → [10,82]"},
            {"step": 9, "array": [3, 9, 10, 82], "action": "Merge [3,9] + [10,82] → [3,9,10,82]"},
            {"step": 10, "array": [3, 9, 10, 27, 38, 43, 82], "action": "Merge [27,38,43] + [3,9,10,82] → sorted!"},
        ]
    },
    "quick_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Quick sort — partition around pivot",
        "example_input": [10, 7, 8, 9, 1, 5],
        "steps": [
            {"step": 1, "array": [10, 7, 8, 9, 1, 5], "pivot": 5, "action": "Pivot = 5 (last element)"},
            {"step": 2, "array": [1, 7, 8, 9, 10, 5], "pivot": 5, "action": "Partition: elements ≤5 left, >5 right"},
            {"step": 3, "array": [1, 5, 8, 9, 10, 7], "pivot_idx": 1, "action": "Place pivot at index 1"},
            {"step": 4, "array": [1, 5, 8, 9, 10, 7], "action": "Recurse on left [1] and right [8,9,10,7]"},
            {"step": 5, "array": [1, 5, 7, 8, 9, 10], "action": "Sort right partition → [7,8,9,10]"},
            {"step": 6, "array": [1, 5, 7, 8, 9, 10], "action": "Array is sorted!"},
        ]
    },
    "heap_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Heap sort — build max heap, extract max repeatedly",
        "example_input": [12, 11, 13, 5, 6, 7],
        "steps": [
            {"step": 1, "array": [12, 11, 13, 5, 6, 7], "action": "Build max heap"},
            {"step": 2, "array": [13, 11, 12, 5, 6, 7], "action": "Heap property restored"},
            {"step": 3, "array": [12, 11, 7, 5, 6, 13], "action": "Extract max (13), swap with last"},
            {"step": 4, "array": [12, 11, 7, 5, 6, 13], "action": "Heapify → [12, 11, 7, 5, 6]"},
            {"step": 5, "array": [11, 6, 7, 5, 12, 13], "action": "Extract max (12), swap with last"},
            {"step": 6, "array": [5, 6, 7, 11, 12, 13], "action": "Sorted!"},
        ]
    },
    "counting_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Counting sort — count occurrences, place in order",
        "example_input": [4, 2, 2, 8, 3, 3, 1],
        "steps": [
            {"step": 1, "count": [0, 1, 2, 2, 1, 0, 0, 0, 1], "action": "Count occurrences: {1:1, 2:2, 3:2, 4:1, 8:1}"},
            {"step": 2, "count": [0, 1, 3, 5, 6, 6, 6, 6, 7], "action": "Prefix sums"},
            {"step": 3, "array": [1, 2, 2, 3, 3, 4, 8], "action": "Place elements using prefix sums"},
        ]
    },
    "radix_sort": {
        "type": "bars",
        "category": "sorting",
        "description": "Radix sort — sort digit by digit",
        "example_input": [170, 45, 75, 90, 802, 24, 2, 66],
        "steps": [
            {"step": 1, "array": [170, 45, 75, 90, 802, 24, 2, 66], "action": "Sort by ones digit"},
            {"step": 2, "array": [170, 90, 802, 2, 24, 45, 75, 66], "action": "Sorted by ones digit"},
            {"step": 3, "array": [802, 2, 24, 45, 66, 170, 75, 90], "action": "Sort by tens digit"},
            {"step": 4, "array": [2, 24, 45, 66, 75, 90, 170, 802], "action": "Sort by hundreds digit → sorted!"},
        ]
    },
    # ── SEARCH (4) ──
    "binary_search": {
        "type": "array",
        "category": "search",
        "description": "Binary search — halve search space each step",
        "example_input": [1, 3, 5, 7, 9, 11, 13, 15], "target": 7,
        "steps": [
            {"step": 1, "low": 0, "high": 7, "mid": 3, "value": 7, "action": "mid=3, arr[3]=7, found!"},
            {"step": 2, "low": 0, "high": 7, "mid": 3, "value": 7, "action": "target=7, arr[mid]=7 → return mid"},
        ]
    },
    "linear_search": {
        "type": "array",
        "category": "search",
        "description": "Linear search — scan left to right",
        "example_input": [4, 2, 7, 1, 9, 3], "target": 7,
        "steps": [
            {"step": 1, "index": 0, "value": 4, "action": "Check index 0: 4 ≠ 7, continue"},
            {"step": 2, "index": 1, "value": 2, "action": "Check index 1: 2 ≠ 7, continue"},
            {"step": 3, "index": 2, "value": 7, "action": "Check index 2: 7 = 7, found!"},
        ]
    },
    "two_sum": {
        "type": "array",
        "category": "search",
        "description": "Hash map lookup for complement",
        "example_input": [2, 7, 11, 15], "target": 9,
        "steps": [
            {"step": 1, "hashmap": {}, "index": 0, "value": 2, "action": "Need 9-2=7, not in map, store {2:0}"},
            {"step": 2, "hashmap": {"2": 0}, "index": 1, "value": 7, "action": "Need 9-7=2, found in map! Return [0,1]"},
        ]
    },
    "kth_largest": {
        "type": "array",
        "category": "search",
        "description": "Find kth largest using min-heap",
        "example_input": [3, 2, 1, 5, 6, 4], "k": 2,
        "steps": [
            {"step": 1, "heap": [3], "action": "Push 3 into min-heap"},
            {"step": 2, "heap": [2, 3], "action": "Push 2"},
            {"step": 3, "heap": [1, 3, 2], "action": "Push 1"},
            {"step": 4, "heap": [1, 3, 2, 5], "action": "Push 5, size=4, pop 1 → heap=[2,3,5]"},
            {"step": 5, "heap": [2, 5, 3, 6], "action": "Push 6, pop 2 → heap=[3,5,6]"},
            {"step": 6, "heap": [3, 5, 6, 4], "action": "Push 4, pop 3 → heap=[4,5,6]"},
            {"step": 7, "result": 4, "action": "Heap has 2 elements, top=4 → kth largest = 4"},
        ]
    },
    # ── LINKED LIST (5) ──
    "linked_list_reverse": {
        "type": "linked_list",
        "category": "linked_list",
        "description": "Reverse a linked list in-place",
        "example_input": [1, 2, 3, 4, 5],
        "steps": [
            {"step": 1, "list": [1, 2, 3, 4, 5], "prev": "null", "curr": 1, "action": "Init prev=null, curr=1"},
            {"step": 2, "list": [1, 2, 3, 4, 5], "prev": 1, "curr": 2, "action": "Reverse 1→null, move to 2"},
            {"step": 3, "list": [2, 1, 3, 4, 5], "prev": 2, "curr": 3, "action": "Reverse 2→1, move to 3"},
            {"step": 4, "list": [3, 2, 1, 4, 5], "prev": 3, "curr": 4, "action": "Reverse 3→2, move to 4"},
            {"step": 5, "list": [4, 3, 2, 1, 5], "prev": 4, "curr": 5, "action": "Reverse 4→3, move to 5"},
            {"step": 6, "list": [5, 4, 3, 2, 1], "prev": 5, "curr": None, "action": "Reverse 5→4, curr=None → done!"},
        ]
    },
    "detect_cycle": {
        "type": "linked_list",
        "category": "linked_list",
        "description": "Floyd's cycle detection (tortoise & hare)",
        "example_input": [1, 2, 3, 4, 5, 3],
        "steps": [
            {"step": 1, "slow": 1, "fast": 1, "action": "Both start at head"},
            {"step": 2, "slow": 2, "fast": 3, "action": "slow moves 1, fast moves 2"},
            {"step": 3, "slow": 3, "fast": 5, "action": "slow=3, fast=5"},
            {"step": 4, "slow": 4, "fast": 3, "action": "fast cycles back to 3"},
            {"step": 5, "slow": 5, "fast": 5, "action": "slow=5, fast=5 → cycle detected!"},
        ]
    },
    "merge_two_sorted": {
        "type": "linked_list",
        "category": "linked_list",
        "description": "Merge two sorted linked lists",
        "example_input": {"list1": [1, 3, 5], "list2": [2, 4, 6]},
        "steps": [
            {"step": 1, "result": [], "l1": 1, "l2": 2, "action": "Compare 1 vs 2 → pick 1"},
            {"step": 2, "result": [1], "l1": 3, "l2": 2, "action": "Compare 3 vs 2 → pick 2"},
            {"step": 3, "result": [1, 2], "l1": 3, "l2": 4, "action": "Compare 3 vs 4 → pick 3"},
            {"step": 4, "result": [1, 2, 3], "l1": 5, "l2": 4, "action": "Compare 5 vs 4 → pick 4"},
            {"step": 5, "result": [1, 2, 3, 4], "l1": 5, "l2": 6, "action": "Compare 5 vs 6 → pick 5"},
            {"step": 6, "result": [1, 2, 3, 4, 5, 6], "action": "Append remaining 6 → merged!"},
        ]
    },
    "add_two_numbers": {
        "type": "linked_list",
        "category": "linked_list",
        "description": "Add two numbers represented as linked lists",
        "example_input": {"l1": [2, 4, 3], "l2": [5, 6, 4]},
        "steps": [
            {"step": 1, "carry": 0, "sum": 2 + 5 + 0, "result": [7], "action": "2+5+carry=7, no carry"},
            {"step": 2, "carry": 0, "sum": 4 + 6 + 0, "result": [7, 0], "action": "4+6=10, digit=0, carry=1"},
            {"step": 3, "carry": 1, "sum": 3 + 4 + 1, "result": [7, 0, 8], "action": "3+4+1=8 → result: 708"},
        ]
    },
    "flatten_multilevel": {
        "type": "linked_list",
        "category": "linked_list",
        "description": "Flatten a multilevel doubly linked list",
        "example_input": [1, 2, 3, "↓", 7, 8, "↓", 11, 12, 4, 5, 6],
        "steps": [
            {"step": 1, "stack": [1], "action": "Start at node 1"},
            {"step": 2, "stack": [1, 2], "action": "Go to child 2"},
            {"step": 3, "stack": [1, 2, 7], "action": "Found child at 2→7, push 7"},
            {"step": 4, "flattened": [1, 2, 7, 8], "action": "Flatten child: 7→8"},
            {"step": 5, "flattened": [1, 2, 7, 8, 3], "action": "Continue main: →3"},
        ]
    },
    # ── TREE (6) ──
    "binary_tree_bfs": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Level-order traversal using BFS",
        "example_input": {"root": 1, "left": {"root": 2, "left": 4, "right": 5}, "right": {"root": 3, "left": 6, "right": 7}},
        "steps": [
            {"step": 1, "queue": [1], "visited": [], "level": 0, "action": "Enqueue root 1"},
            {"step": 2, "queue": [2, 3], "visited": [1], "level": 1, "action": "Process 1, enqueue children 2,3"},
            {"step": 3, "queue": [3, 4, 5], "visited": [1, 2], "level": 2, "action": "Process 2, enqueue 4,5"},
            {"step": 4, "queue": [4, 5, 6, 7], "visited": [1, 2, 3], "level": 2, "action": "Process 3, enqueue 6,7"},
            {"step": 5, "queue": [5, 6, 7], "visited": [1, 2, 3, 4], "level": 3, "action": "Process 4 (leaf)"},
            {"step": 6, "visited": [1, 2, 3, 4, 5, 6, 7], "action": "Traversal complete: [1,2,3,4,5,6,7]"},
        ]
    },
    "binary_tree_inorder": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Inorder traversal: left → root → right",
        "example_input": {"root": 4, "left": {"root": 2, "left": 1, "right": 3}, "right": {"root": 6, "left": 5, "right": 7}},
        "steps": [
            {"step": 1, "stack": [4], "action": "Start at root 4, go left"},
            {"step": 2, "stack": [4, 2], "action": "Go left to 2"},
            {"step": 3, "stack": [4, 2, 1], "action": "Go left to 1"},
            {"step": 4, "visited": [1], "action": "1 has no left, visit 1"},
            {"step": 5, "visited": [1, 2], "action": "Back to 2, visit 2"},
            {"step": 6, "visited": [1, 2, 3], "action": "Go right to 3, visit 3"},
            {"step": 7, "visited": [1, 2, 3, 4], "action": "Back to root, visit 4"},
            {"step": 8, "visited": [1, 2, 3, 4, 5, 6, 7], "action": "Traverse right subtree → [1,2,3,4,5,6,7]"},
        ]
    },
    "lowest_common_ancestor": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Find LCA of two nodes in binary tree",
        "example_input": {"root": 6, "p": 2, "q": 8, "tree": "6(2(0,4),8(7,9))"},
        "steps": [
            {"step": 1, "current": 6, "action": "At root 6. Neither p nor q, search both sides"},
            {"step": 2, "current": 2, "action": "At node 2. Found p=2! Return 2"},
            {"step": 3, "current": 8, "action": "At node 8. Found q=8! Return 8"},
            {"step": 4, "lca": 6, "action": "Left returns 2, right returns 8 → current 6 is LCA"},
        ]
    },
    "bst_insert": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Insert into Binary Search Tree",
        "example_input": {"tree": [5, 3, 7, 1, 4], "insert": 6},
        "steps": [
            {"step": 1, "current": 5, "action": "6 > 5, go right"},
            {"step": 2, "current": 7, "action": "6 < 7, go left"},
            {"step": 3, "current": None, "action": "Empty spot, insert 6"},
            {"step": 4, "tree": [5, 3, 7, 1, 4, 6], "action": "6 inserted between 5's right and 7's left"},
        ]
    },
    "validate_bst": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Validate if tree is a valid BST",
        "example_input": {"root": 5, "left": {"root": 1, "right": {"root": 4, "left": 3, "right": 6}}},
        "steps": [
            {"step": 1, "node": 5, "range": "(-∞, +∞)", "action": "Root 5 in valid range"},
            {"step": 2, "node": 1, "range": "(-∞, 5)", "action": "Left child 1 in range"},
            {"step": 3, "node": 4, "range": (1, 5), "action": "Right child 4 in range"},
            {"step": 4, "node": 3, "range": (1, 4), "action": "3 in range"},
            {"step": 5, "node": 6, "range": (4, 5), "action": "6 > 5, violates BST! Not valid"},
        ]
    },
    "trie_operations": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Trie insert and search",
        "example_input": {"words": ["cat", "car", "card", "dog"], "search": "car"},
        "steps": [
            {"step": 1, "action": "Insert 'cat': root→c→a→t"},
            {"step": 2, "action": "Insert 'car': root→c→a→r (reuse c,a)"},
            {"step": 3, "action": "Insert 'card': root→c→a→r→d (reuse c,a,r)"},
            {"step": 4, "action": "Insert 'dog': root→d→o→g"},
            {"step": 5, "action": "Search 'car': follow c→a→r, end marked → found!"},
        ]
    },
    # ── GRAPH (5) ──
    "bfs": {
        "type": "graph",
        "category": "graph",
        "description": "Breadth-first search — level by level",
        "example_input": {"edges": [[0,1],[0,2],[1,3],[2,3],[3,4]], "start": 0},
        "steps": [
            {"step": 1, "queue": [0], "visited": [0], "action": "Start BFS from node 0"},
            {"step": 2, "queue": [1, 2], "visited": [0, 1, 2], "action": "Dequeue 0, enqueue neighbors 1,2"},
            {"step": 3, "queue": [2, 3], "visited": [0, 1, 2, 3], "action": "Dequeue 1, enqueue 3"},
            {"step": 4, "queue": [3, 4], "visited": [0, 1, 2, 3, 4], "action": "Dequeue 2, enqueue 4"},
            {"step": 5, "queue": [4], "visited": [0, 1, 2, 3, 4], "action": "Dequeue 3, all neighbors visited"},
            {"step": 6, "visited": [0, 1, 2, 3, 4], "action": "Dequeue 4, no neighbors → done!"},
        ]
    },
    "dfs": {
        "type": "graph",
        "category": "graph",
        "description": "Depth-first search — go deep, then backtrack",
        "example_input": {"edges": [[0,1],[0,2],[1,3],[2,3],[3,4]], "start": 0},
        "steps": [
            {"step": 1, "stack": [0], "visited": [0], "action": "Start DFS from node 0"},
            {"step": 2, "stack": [0, 1], "visited": [0, 1], "action": "Visit 1 from 0"},
            {"step": 3, "stack": [0, 1, 3], "visited": [0, 1, 3], "action": "Visit 3 from 1"},
            {"step": 4, "stack": [0, 1, 3, 4], "visited": [0, 1, 3, 4], "action": "Visit 4 from 3"},
            {"step": 5, "stack": [0, 1], "visited": [0, 1, 3, 4], "action": "Backtrack: 4 done, 3 done, 1 done"},
            {"step": 6, "stack": [0, 2], "visited": [0, 1, 2, 3, 4], "action": "Visit 2 from 0"},
            {"step": 7, "visited": [0, 1, 2, 3, 4], "action": "2's neighbor 3 already visited → done!"},
        ]
    },
    "dijkstra": {
        "type": "graph",
        "category": "graph",
        "description": "Dijkstra's shortest path",
        "example_input": {"edges": [[0,1,4],[0,2,1],[1,3,1],[2,1,2],[2,3,5]], "start": 0},
        "steps": [
            {"step": 1, "distances": {"0": 0, "1": "∞", "2": "∞", "3": "∞"}, "action": "Initialize distances: 0=0, others=∞"},
            {"step": 2, "current": 0, "distances": {"0": 0, "1": 4, "2": 1, "3": "∞"}, "action": "Visit 0: update neighbors 1→4, 2→1"},
            {"step": 3, "current": 2, "distances": {"0": 0, "1": 3, "2": 1, "3": 6}, "action": "Visit 2 (min dist=1): 1→3, 3→6"},
            {"step": 4, "current": 1, "distances": {"0": 0, "1": 3, "2": 1, "3": 4}, "action": "Visit 1 (dist=3): 3→min(6,3+1)=4"},
            {"step": 5, "current": 3, "distances": {"0": 0, "1": 3, "2": 1, "3": 4}, "action": "Visit 3 (dist=4): shortest paths found!"},
        ]
    },
    "topological_sort": {
        "type": "graph",
        "category": "graph",
        "description": "Topological sort (Kahn's algorithm)",
        "example_input": {"edges": [[0,1],[0,2],[1,3],[2,3],[3,4]], "vertices": 5},
        "steps": [
            {"step": 1, "in_degree": {0: 0, 1: 1, 2: 1, 3: 2, 4: 1}, "action": "Calculate in-degrees"},
            {"step": 2, "queue": [0], "result": [], "action": "Enqueue nodes with in-degree 0: [0]"},
            {"step": 3, "queue": [1, 2], "result": [0], "action": "Process 0, reduce neighbors' in-degree"},
            {"step": 4, "queue": [2, 3], "result": [0, 1], "action": "Process 1, 3's in-degree=1"},
            {"step": 5, "queue": [3], "result": [0, 1, 2], "action": "Process 2, 3's in-degree=0"},
            {"step": 6, "queue": [4], "result": [0, 1, 2, 3], "action": "Process 3"},
            {"step": 7, "result": [0, 1, 2, 3, 4], "action": "Topological order: [0,1,2,3,4]"},
        ]
    },
    "bellman_ford": {
        "type": "graph",
        "category": "graph",
        "description": "Bellman-Ford shortest path (handles negative weights)",
        "example_input": {"edges": [[0,1,4],[0,2,5],[1,2,-3],[2,3,4],[1,3,8]], "start": 0, "vertices": 4},
        "steps": [
            {"step": 1, "dist": [0, "∞", "∞", "∞"], "action": "Initialize: dist[0]=0, others=∞"},
            {"step": 2, "dist": [0, 4, 5, "∞"], "action": "Relax edges from 0: 1→4, 2→5"},
            {"step": 3, "dist": [0, 4, 1, "∞"], "action": "Relax edge 1→2: dist[2]=min(5,4-3)=1"},
            {"step": 4, "dist": [0, 4, 1, 5], "action": "Relax 2→3: dist[3]=min(∞,1+4)=5"},
            {"step": 5, "dist": [0, 4, 1, 5], "action": "Relax 1→3: dist[3]=min(5,4+8)=5. No changes → done!"},
        ]
    },
    # ── STACK & QUEUE (4) ──
    "valid_parentheses": {
        "type": "stack",
        "category": "stack",
        "description": "Match brackets using stack",
        "example_input": "({[]})",
        "steps": [
            {"step": 1, "stack": ["("], "char": "(", "action": "Push '(' onto stack"},
            {"step": 2, "stack": ["(", "{"], "char": "{", "action": "Push '{' onto stack"},
            {"step": 3, "stack": ["(", "{", "["], "char": "[", "action": "Push '[' onto stack"},
            {"step": 4, "stack": ["(", "{"], "char": "]", "action": "']' matches '[' → pop"},
            {"step": 5, "stack": ["("], "char": "}", "action": "'}' matches '{' → pop"},
            {"step": 6, "stack": [], "char": ")", "action": "')' matches '(' → pop. Stack empty → valid!"},
        ]
    },
    "min_stack": {
        "type": "stack",
        "category": "stack",
        "description": "Stack that supports getMin() in O(1)",
        "example_input": ["push(-2)", "push(0)", "push(-3)", "getMin()", "pop()", "getMin()"],
        "steps": [
            {"step": 1, "stack": [-2], "min": -2, "action": "push(-2): stack=[-2], min=-2"},
            {"step": 2, "stack": [-2, 0], "min": -2, "action": "push(0): stack=[-2,0], min=-2"},
            {"step": 3, "stack": [-2, 0, -3], "min": -3, "action": "push(-3): stack=[-2,0,-3], min=-3"},
            {"step": 4, "result": -3, "action": "getMin() → -3"},
            {"step": 5, "stack": [-2, 0], "min": -2, "action": "pop() removes -3, min=-2"},
            {"step": 6, "result": -2, "action": "getMin() → -2"},
        ]
    },
    "queue_using_stacks": {
        "type": "queue",
        "category": "stack",
        "description": "Implement queue using two stacks",
        "example_input": ["enqueue(1)", "enqueue(2)", "dequeue()", "enqueue(3)", "dequeue()"],
        "steps": [
            {"step": 1, "inbox": [1], "outbox": [], "action": "enqueue(1): push to inbox"},
            {"step": 2, "inbox": [1, 2], "outbox": [], "action": "enqueue(2): push to inbox"},
            {"step": 3, "inbox": [], "outbox": [2, 1], "action": "dequeue(): transfer inbox→outbox, pop 1"},
            {"step": 4, "result": 1, "action": "Dequeued 1 (FIFO order)"},
            {"step": 5, "inbox": [3], "outbox": [2], "action": "enqueue(3): push to inbox"},
            {"step": 6, "result": 2, "action": "dequeue(): outbox not empty, pop 2"},
        ]
    },
    "next_greater_element": {
        "type": "stack",
        "category": "stack",
        "description": "Find next greater element for each element",
        "example_input": [4, 5, 2, 25],
        "steps": [
            {"step": 1, "stack": [4], "action": "Push 4, no greater found yet"},
            {"step": 2, "stack": [], "result": {4: 5}, "action": "5 > 4, so next greater of 4 is 5"},
            {"step": 3, "stack": [2], "action": "Push 2, 5 already popped"},
            {"step": 4, "stack": [], "result": {4: 5, 5: 25, 2: 25}, "action": "25 > 2, next greater of 2 is 25"},
            {"step": 5, "result": {4: 5, 5: 25, 2: 25, 25: -1}, "action": "25 has no greater → -1"},
        ]
    },
    # ── DYNAMIC PROGRAMMING (8) ──
    "fibonacci": {
        "type": "array",
        "category": "dp",
        "description": "Fibonacci with memoization",
        "example_input": 6,
        "steps": [
            {"step": 1, "dp": [0, 1, 0, 0, 0, 0, 0], "action": "Base: fib(0)=0, fib(1)=1"},
            {"step": 2, "dp": [0, 1, 1, 0, 0, 0, 0], "action": "fib(2) = fib(1)+fib(0) = 1"},
            {"step": 3, "dp": [0, 1, 1, 2, 0, 0, 0], "action": "fib(3) = fib(2)+fib(1) = 2"},
            {"step": 4, "dp": [0, 1, 1, 2, 3, 0, 0], "action": "fib(4) = fib(3)+fib(2) = 3"},
            {"step": 5, "dp": [0, 1, 1, 2, 3, 5, 0], "action": "fib(5) = fib(4)+fib(3) = 5"},
            {"step": 6, "dp": [0, 1, 1, 2, 3, 5, 8], "action": "fib(6) = fib(5)+fib(4) = 8"},
        ]
    },
    "knapsack": {
        "type": "dp_table",
        "category": "dp",
        "description": "0/1 Knapsack problem",
        "example_input": {"weights": [1, 3, 4, 5], "values": [1, 4, 5, 7], "capacity": 7},
        "steps": [
            {"step": 1, "dp_table": "4x8 grid (all 0)", "action": "Initialize dp[i][w]=0"},
            {"step": 2, "dp_table": "w=1→val=1, rest 0", "action": "Item 1 (w=1,v=1): fits in w≥1"},
            {"step": 3, "dp_table": "updated row 2", "action": "Item 2 (w=3,v=4): max of include/exclude"},
            {"step": 4, "dp_table": "updated row 3", "action": "Item 3 (w=4,v=5): update cells w≥4"},
            {"step": 5, "dp_table": "filled", "action": "Item 4 (w=5,v=7): dp[4][7]=9 (items 2+4)"},
            {"step": 6, "result": 9, "action": "dp[4][7]=9 → max value = 9"},
        ]
    },
    "longest_common_subsequence": {
        "type": "dp_table",
        "category": "dp",
        "description": "LCS of two strings",
        "example_input": {"s1": "ABCBDAB", "s2": "BDCAB"},
        "steps": [
            {"step": 1, "dp_table": "8x6 grid", "action": "Initialize dp[0][j]=0, dp[i][0]=0"},
            {"step": 2, "dp_table": "filling...", "action": "Compare A vs B: no match, dp=max(up,left)"},
            {"step": 3, "dp_table": "filling...", "action": "Compare B vs B: match! dp=diagonal+1"},
            {"step": 4, "dp_table": "filling...", "action": "Continue filling table..."},
            {"step": 5, "dp_table": "complete", "action": "dp[7][5]=4 → LCS length = 4"},
            {"step": 6, "result": "BCAB", "action": "Backtrack → LCS = 'BCAB'"},
        ]
    },
    "coin_change": {
        "type": "dp_table",
        "category": "dp",
        "description": "Minimum coins to make change",
        "example_input": {"coins": [1, 5, 10, 25], "amount": 30},
        "steps": [
            {"step": 1, "dp": [0, "∞", "∞", ..., "∞"], "action": "dp[0]=0, rest=infinity"},
            {"step": 2, "dp": [0, 1, 2, 3, 4, 5, ...], "action": "Using coin 1: dp[i]=i"},
            {"step": 3, "dp": [0, 1, 2, 3, 4, 1, ...], "action": "Using coin 5: dp[5]=min(5,0+1)=1"},
            {"step": 4, "dp": [0, 1, 2, 3, 4, 1, 2, ...], "action": "dp[10]=1 (one 10-cent coin)"},
            {"step": 5, "dp": [..., 2], "action": "dp[30]=2 (one 25 + one 5)"},
            {"step": 6, "result": 2, "action": "Minimum coins for 30 = 2 (25+5)"},
        ]
    },
    "longest_increasing_subsequence": {
        "type": "dp_table",
        "category": "dp",
        "description": "LIS using patience sorting",
        "example_input": [10, 9, 2, 5, 3, 7, 101, 18],
        "steps": [
            {"step": 1, "tails": [10], "action": "Start: tails=[10]"},
            {"step": 2, "tails": [9], "action": "9 < 10, replace → tails=[9]"},
            {"step": 3, "tails": [2], "action": "2 < 9, replace → tails=[2]"},
            {"step": 4, "tails": [2, 5], "action": "5 > 2, append → tails=[2,5]"},
            {"step": 5, "tails": [2, 3], "action": "3 < 5, replace → tails=[2,3]"},
            {"step": 6, "tails": [2, 3, 7], "action": "7 > 3, append → tails=[2,3,7]"},
            {"step": 7, "tails": [2, 3, 7, 101], "action": "101 > 7, append"},
            {"step": 8, "tails": [2, 3, 7, 18], "action": "18 < 101, replace → length=4"},
        ]
    },
    "edit_distance": {
        "type": "dp_table",
        "category": "dp",
        "description": "Levenshtein distance between two strings",
        "example_input": {"s1": "horse", "s2": "ros"},
        "steps": [
            {"step": 1, "dp_table": "4x6 grid", "action": "Initialize: dp[i][0]=i, dp[0][j]=j"},
            {"step": 2, "dp_table": "filling...", "action": "h→r: no match, dp=1+min(up,left,diag)"},
            {"step": 3, "dp_table": "filling...", "action": "o→o: match! dp=diagonal"},
            {"step": 4, "dp_table": "filling...", "action": "Continue computing..."},
            {"step": 5, "result": 3, "action": "dp[5][3]=3 → horse→ros needs 3 edits (h→r, remove second r, remove e)"},
        ]
    },
    "climbing_stairs": {
        "type": "dp_table",
        "category": "dp",
        "description": "Ways to climb n stairs (1 or 2 steps)",
        "example_input": 5,
        "steps": [
            {"step": 1, "dp": [1, 1, 0, 0, 0, 0], "action": "Base: 0 stairs=1 way, 1 stair=1 way"},
            {"step": 2, "dp": [1, 1, 2, 0, 0, 0], "action": "dp[2] = dp[1]+dp[0] = 2"},
            {"step": 3, "dp": [1, 1, 2, 3, 0, 0], "action": "dp[3] = dp[2]+dp[1] = 3"},
            {"step": 4, "dp": [1, 1, 2, 3, 5, 0], "action": "dp[4] = dp[3]+dp[2] = 5"},
            {"step": 5, "dp": [1, 1, 2, 3, 5, 8], "action": "dp[5] = dp[4]+dp[3] = 8"},
        ]
    },
    "house_robber": {
        "type": "dp_table",
        "category": "dp",
        "description": "Max money robbing houses (can't rob adjacent)",
        "example_input": [2, 7, 9, 3, 1],
        "steps": [
            {"step": 1, "dp": [2, 7, 0, 0, 0], "action": "dp[0]=2, dp[1]=max(2,7)=7"},
            {"step": 2, "dp": [2, 7, 16, 0, 0], "action": "dp[2]=9+max(dp[0])=11? No: dp[2]=max(7,9+2)=11? dp[2]=max(dp[1],dp[0]+9)=11"},
            {"step": 3, "dp": [2, 7, 11, 10, 0], "action": "dp[3]=max(dp[2],dp[1]+3)=max(11,10)=11"},
            {"step": 4, "dp": [2, 7, 11, 11, 12], "action": "dp[4]=max(dp[3],dp[2]+1)=max(11,12)=12"},
            {"step": 5, "result": 12, "action": "Max profit = 12 (rob houses 0,2,4 → 2+9+1=12)"},
        ]
    },
    # ── MATRIX (3) ──
    "matrix_rotation": {
        "type": "matrix",
        "category": "matrix",
        "description": "Rotate matrix 90° clockwise",
        "example_input": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "steps": [
            {"step": 1, "matrix": [[1,2,3],[4,5,6],[7,8,9]], "action": "Transpose: swap rows↔cols"},
            {"step": 2, "matrix": [[1,4,7],[2,5,8],[3,6,9]], "action": "Transposed matrix"},
            {"step": 3, "matrix": [[7,4,1],[8,5,2],[9,6,3]], "action": "Reverse each row → rotated 90°!"},
        ]
    },
    "spiral_order": {
        "type": "matrix",
        "category": "matrix",
        "description": "Traverse matrix in spiral order",
        "example_input": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "steps": [
            {"step": 1, "result": [1, 2, 3], "action": "Top row: → 1,2,3"},
            {"step": 2, "result": [1, 2, 3, 6, 9], "action": "Right col: ↓ 6,9"},
            {"step": 3, "result": [1, 2, 3, 6, 9, 8, 7], "action": "Bottom row: ← 8,7"},
            {"step": 4, "result": [1, 2, 3, 6, 9, 8, 7, 4], "action": "Left col: ↑ 4"},
            {"step": 5, "result": [1, 2, 3, 6, 9, 8, 7, 4, 5], "action": "Center: 5 → [1,2,3,6,9,8,7,4,5]"},
        ]
    },
    "island_count": {
        "type": "matrix",
        "category": "matrix",
        "description": "Count connected islands (DFS/BFS flood fill)",
        "example_input": [[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]],
        "steps": [
            {"step": 1, "grid": "mark (0,0)", "islands": 1, "action": "Found island at (0,0), DFS mark connected"},
            {"step": 2, "grid": "island 1 marked", "islands": 1, "action": "Marked (0,0),(0,1),(1,0),(1,1)"},
            {"step": 3, "grid": "mark (2,2)", "islands": 2, "action": "Found island at (2,2)"},
            {"step": 4, "grid": "mark (3,3)", "islands": 3, "action": "Found island at (3,3), mark (3,3),(3,4)"},
            {"step": 5, "result": 3, "action": "Total islands = 3"},
        ]
    },
    # ── STRING (4) ──
    "kmp_pattern_match": {
        "type": "array",
        "category": "string",
        "description": "Knuth-Morris-Pratt string matching",
        "example_input": {"text": "ABABDABACDABABCABAB", "pattern": "ABABCABAB"},
        "steps": [
            {"step": 1, "lps": [0, 0, 1, 2, 0, 1, 2, 3, 4], "action": "Build LPS array for pattern"},
            {"step": 2, "i": 0, "j": 0, "action": "Start matching text vs pattern"},
            {"step": 3, "i": 4, "j": 0, "action": "Mismatch at text[4]='D', use LPS → j=0"},
            {"step": 4, "i": 10, "j": 5, "action": "Partial match, backtracking via LPS"},
            {"step": 5, "i": 18, "j": 9, "action": "Full match at index 9!"},
        ]
    },
    "manachers_palindrome": {
        "type": "array",
        "category": "string",
        "description": "Longest palindromic substring in O(n)",
        "example_input": "babad",
        "steps": [
            {"step": 1, "transformed": "^#b#a#b#a#d#$", "action": "Transform string to handle odd/even"},
            {"step": 2, "P": [0, 1, 0, 3, 0, 5, 0, 3, 0, 1, 0], "action": "Compute palindrome radii"},
            {"step": 3, "center": 4, "max_len": 5, "action": "Max radius=5 at center 4"},
            {"step": 4, "result": "bab", "action": "Longest palindrome = 'bab' (or 'aba')"},
        ]
    },
    "anagram_groups": {
        "type": "array",
        "category": "string",
        "description": "Group anagrams together using sorted key",
        "example_input": ["eat", "tea", "tan", "ate", "nat", "bat"],
        "steps": [
            {"step": 1, "map": {"aet": ["eat"]}, "action": "Sort 'eat' → 'aet', add to map"},
            {"step": 2, "map": {"aet": ["eat","tea"]}, "action": "Sort 'tea' → 'aet', group"},
            {"step": 3, "map": {"aet": ["eat","tea"], "ant": ["tan"]}, "action": "Sort 'tan' → 'ant'"},
            {"step": 4, "map": {"aet": ["eat","tea","ate"], "ant": ["tan"]}, "action": "Sort 'ate' → 'aet', group"},
            {"step": 5, "map": {"aet": ["eat","tea","ate"], "ant": ["tan","nat"]}, "action": "Sort 'nat' → 'ant', group"},
            {"step": 6, "result": [["eat","tea","ate"], ["tan","nat"], ["bat"]], "action": "Grouped! 'bat' is alone"},
        ]
    },
    "longest_substring_no_repeat": {
        "type": "array",
        "category": "string",
        "description": "Sliding window for longest unique substring",
        "example_input": "abcabcbb",
        "steps": [
            {"step": 1, "window": "a", "set": {"a"}, "max_len": 1, "action": "Add 'a', window='a'"},
            {"step": 2, "window": "ab", "set": {"a","b"}, "max_len": 2, "action": "Add 'b', window='ab'"},
            {"step": 3, "window": "abc", "set": {"a","b","c"}, "max_len": 3, "action": "Add 'c', window='abc'"},
            {"step": 4, "window": "bca", "set": {"b","c","a"}, "max_len": 3, "action": "Duplicate 'a', shrink → 'bca'"},
            {"step": 5, "window": "cab", "set": {"c","a","b"}, "max_len": 3, "action": "Duplicate 'b', shrink → 'cab'"},
            {"step": 6, "window": "abc", "max_len": 3, "action": "Continues... max stays 3"},
        ]
    },
    # ── BACKTRACKING (3) ──
    "n_queens": {
        "type": "matrix",
        "category": "backtracking",
        "description": "Place N queens on NxN board without conflicts",
        "example_input": 4,
        "steps": [
            {"step": 1, "board": ".Q..", "queens": 1, "action": "Place queen at (0,1)"},
            {"step": 2, "board": ["..Q.", ".Q.."], "queens": 2, "action": "Place queen at (1,1)? Conflict! Try (2,0)"},
            {"step": 3, "board": ["..Q.", ".Q..", "Q..."], "queens": 3, "action": "Place queen at (2,0)"},
            {"step": 4, "board": ["..Q.", ".Q..", "Q...", "...Q"], "queens": 4, "action": "Place queen at (3,2) → solution found!"},
        ]
    },
    "subset_sum": {
        "type": "dp_table",
        "category": "backtracking",
        "description": "Find subsets that sum to target",
        "example_input": {"nums": [3, 34, 4, 12, 5, 2], "target": 9},
        "steps": [
            {"step": 1, "path": [], "remaining": 9, "action": "Start with empty subset"},
            {"step": 2, "path": [3], "remaining": 6, "action": "Include 3, remaining=6"},
            {"step": 3, "path": [3, 4], "remaining": 2, "action": "Include 4, remaining=2"},
            {"step": 4, "path": [3, 4, 2], "remaining": 0, "action": "Include 2, remaining=0 → found! [3,4,2]"},
            {"step": 5, "path": [4, 5], "remaining": 0, "action": "Another solution: [4,5]"},
        ]
    },
    "permutations": {
        "type": "array",
        "category": "backtracking",
        "description": "Generate all permutations of array",
        "example_input": [1, 2, 3],
        "steps": [
            {"step": 1, "current": [], "remaining": [1, 2, 3], "action": "Start backtracking"},
            {"step": 2, "current": [1], "remaining": [2, 3], "action": "Pick 1, recurse"},
            {"step": 3, "current": [1, 2], "remaining": [3], "action": "Pick 2, recurse"},
            {"step": 4, "current": [1, 2, 3], "permutation": [1, 2, 3], "action": "Found permutation: [1,2,3]"},
            {"step": 5, "current": [1, 3, 2], "permutation": [1, 3, 2], "action": "Backtrack → [1,3,2]"},
            {"step": 6, "permutations": ["[1,2,3]","[1,3,2]","[2,1,3]","[2,3,1]","[3,1,2]","[3,2,1]"], "action": "6 permutations total (3!)"},
        ]
    },
    # ── SLIDING WINDOW (3) ──
    "sliding_window_max": {
        "type": "array",
        "category": "window",
        "description": "Maximum in each sliding window of size k",
        "example_input": {"arr": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3},
        "steps": [
            {"step": 1, "window": [1, 3, -1], "max": 3, "action": "Window [1,3,-1], max=3"},
            {"step": 2, "window": [3, -1, -3], "max": 3, "action": "Window [3,-1,-3], max=3"},
            {"step": 3, "window": [-1, -3, 5], "max": 5, "action": "Window [-1,-3,5], max=5"},
            {"step": 4, "window": [-3, 5, 3], "max": 5, "action": "Window [-3,5,3], max=5"},
            {"step": 5, "window": [5, 3, 6], "max": 6, "action": "Window [5,3,6], max=6"},
            {"step": 6, "window": [3, 6, 7], "max": 7, "action": "Window [3,6,7], max=7"},
            {"step": 7, "result": [3, 3, 5, 5, 6, 7], "action": "Result: [3,3,5,5,6,7]"},
        ]
    },
    "min_window_substring": {
        "type": "array",
        "category": "window",
        "description": "Minimum window containing all chars of target",
        "example_input": {"s": "ADOBECODEBANC", "t": "ABC"},
        "steps": [
            {"step": 1, "window": "ADOBEC", "left": 0, "right": 6, "action": "First valid window: 'ADOBEC'"},
            {"step": 2, "window": "CODEBA", "left": 3, "right": 9, "action": "Shrink left, expand right"},
            {"step": 3, "window": "CODEBANC", "left": 3, "right": 12, "action": "Found 'BANC' in window"},
            {"step": 4, "window": "BANC", "left": 9, "right": 12, "action": "Minimum window: 'BANC' (length 4)"},
        ]
    },
    "max_average_subarray": {
        "type": "array",
        "category": "window",
        "description": "Maximum average of subarray of size k",
        "example_input": {"arr": [1, 12, -5, -6, 50, 3], "k": 4},
        "steps": [
            {"step": 1, "window": [1, 12, -5, -6], "sum": 2, "avg": 0.5, "action": "First window sum=2, avg=0.5"},
            {"step": 2, "window": [12, -5, -6, 50], "sum": 51, "avg": 12.75, "action": "New max! avg=12.75"},
            {"step": 3, "window": [-5, -6, 50, 3], "sum": 42, "avg": 10.5, "action": "avg=10.5 < 12.75, keep max"},
            {"step": 4, "result": 12.75, "action": "Maximum average = 12.75"},
        ]
    },
    # ── TREE / MISC (5) ──
    "serialize_deserialize_tree": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Serialize and deserialize binary tree",
        "example_input": {"tree": "1(2(3,4),5(,6(7,)))"},
        "steps": [
            {"step": 1, "action": "Serialize: preorder traversal"},
            {"step": 2, "serialized": "1,2,3,#,#,4,#,#,5,#,6,7,#,#,#", "action": "String representation with # for null"},
            {"step": 3, "action": "Deserialize: rebuild from string"},
            {"step": 4, "tree": {"root": 1, "left": {"root": 2, "left": 3, "right": 4}, "right": {"root": 5, "right": {"root": 6, "left": 7}}}, "action": "Tree reconstructed!"},
        ]
    },
    "max_path_sum": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Maximum path sum in binary tree",
        "example_input": {"tree": "1(2,3)"},
        "steps": [
            {"step": 1, "node": 2, "max_through": 2, "action": "Leaf node 2, max through=2"},
            {"step": 2, "node": 3, "max_through": 3, "action": "Leaf node 3, max through=3"},
            {"step": 3, "node": 1, "max_through": 6, "action": "Path through 1: 2+1+3=6"},
            {"step": 4, "result": 6, "action": "Maximum path sum = 6"},
        ]
    },
    "word_ladder": {
        "type": "graph",
        "category": "graph",
        "description": "Shortest transformation sequence (BFS)",
        "example_input": {"begin": "hit", "end": "cog", "words": ["hot", "dot", "dog", "lot", "log", "cog"]},
        "steps": [
            {"step": 1, "queue": ["hit"], "visited": {"hit"}, "action": "BFS from 'hit'"},
            {"step": 2, "queue": ["hot"], "visited": {"hit", "hot"}, "action": "Transform hit→hot (change i→o)"},
            {"step": 3, "queue": ["dot", "lot"], "visited": {"hit","hot","dot","lot"}, "action": "hot→dot, hot→lot"},
            {"step": 4, "queue": ["lot", "dog", "log"], "visited": {"...","dog","log"}, "action": "dot→dog, dot→log..."},
            {"step": 5, "queue": ["dog", "log", "cog"], "action": "lot→log, dog→cog"},
            {"step": 6, "result": 5, "action": "hit→hot→dot→dog→cog: 5 steps"},
        ]
    },
    "trie_prefix_search": {
        "type": "binary_tree",
        "category": "tree",
        "description": "Trie-based prefix search",
        "example_input": {"words": ["apple", "app", "ape", "banana", "band"], "prefix": "app"},
        "steps": [
            {"step": 1, "action": "Build trie from words"},
            {"step": 2, "action": "Insert: app→apple→ape (shared prefix 'ap')"},
            {"step": 3, "action": "Insert: banana→band (shared prefix 'ban')"},
            {"step": 4, "action": "Search prefix 'app': follow a→p→p"},
            {"step": 5, "result": ["app", "apple"], "action": "Found 2 words with prefix 'app'"},
        ]
    },
    # ── GRAPH ADDITIONS (5) ──
    "prim_mst": {
        "type": "graph", "category": "graph",
        "description": "Prim's Minimum Spanning Tree",
        "example_input": {"edges": [[0,1,4],[0,2,8],[1,2,2],[1,3,6],[2,3,3],[2,4,9],[3,4,5]], "start": 0},
        "steps": [
            {"step": 1, "visited": [0], "pq": [], "action": "Start at 0, add edges (0-1:4), (0-2:8)"},
            {"step": 2, "visited": [0,1], "pq": [(2,1,2),(8,0,2),(6,1,3)], "action": "Pick min edge 0-1 (4), add 1's edges"},
            {"step": 3, "visited": [0,1,2], "pq": [(3,2,3),(9,2,4)], "action": "Pick min edge 1-2 (2), add 2's edges"},
            {"step": 4, "visited": [0,1,2,3], "pq": [(5,3,4)], "action": "Pick min edge 2-3 (3), add 3's edges"},
            {"step": 5, "visited": [0,1,2,3,4], "mst": [(0,1),(1,2),(2,3),(3,4)], "action": "Pick edge 3-4 (5). MST weight = 4+2+3+5=14"},
        ]
    },
    "kruskal_mst": {
        "type": "graph", "category": "graph",
        "description": "Kruskal's Minimum Spanning Tree",
        "example_input": {"edges": [[0,1,10],[0,2,6],[0,3,5],[1,3,15],[2,3,4]], "vertices": 4},
        "steps": [
            {"step": 1, "sorted": [[2,3,4],[0,3,5],[0,2,6],[0,1,10],[1,3,15]], "action": "Sort edges by weight"},
            {"step": 2, "mst": [(2,3,4)], "sets": "{2,3},{0},{1}", "action": "Add 2-3 (4), no cycle"},
            {"step": 3, "mst": [(2,3,4),(0,3,5)], "sets": "{0,2,3},{1}", "action": "Add 0-3 (5), no cycle"},
            {"step": 4, "mst": [(2,3,4),(0,3,5),(0,2,6)], "sets": "{0,2,3},{1}", "action": "Skip 0-2 (6) → cycle!"},
            {"step": 5, "mst": [(2,3,4),(0,3,5),(0,1,10)], "sets": "{0,1,2,3}", "action": "Add 0-1 (10). MST weight=4+5+10=19"},
        ]
    },
    # ── RECURSION TREE (6) ──
    "tower_of_hanoi": {
        "type": "recursion_tree", "category": "recursion",
        "description": "Tower of Hanoi recursive solution",
        "example_input": {"disks": 3},
        "steps": [
            {"step": 1, "call": "hanoi(3,A→C,B)", "action": "Move 3 disks from A to C using B"},
            {"step": 2, "call": "hanoi(2,A→B,C)", "action": "Recurse: move 2 disks A→B using C"},
            {"step": 3, "call": "hanoi(1,A→C,B)", "action": "Recurse: move 1 disk A→C: move A→C"},
            {"step": 4, "call": "hanoi(1,B→C,A)", "action": "Move B→C"},
            {"step": 5, "result": "Move A→C, A→B, C→B, A→C, B→A, B→C, A→C", "action": "7 moves total for 3 disks"},
        ]
    },
    "n_queens": {
        "type": "recursion_tree", "category": "recursion",
        "description": "N-Queens backtracking solution",
        "example_input": {"n": 4},
        "steps": [
            {"step": 1, "board": [[0,0,0,0]], "row": 0, "action": "Place queen at (0,0)"},
            {"step": 2, "board": [[1,0,0,0],[0,0,0,0]], "row": 1, "action": "Row 1: (1,2) is safe, place"},
            {"step": 3, "board": [[1,0,0,0],[0,0,1,0],[0,0,0,0]], "row": 2, "action": "Row 2: no safe col → backtrack"},
            {"step": 4, "board": [[1,0,0,0],[0,0,0,0]], "row": 1, "action": "Backtrack: try (1,3)"},
            {"step": 5, "board": [[1,0,0,0],[0,0,0,1],[0,1,0,0],[0,0,0,0]], "action": "Solution found!"},
        ]
    },
    "sudoku_solver": {
        "type": "matrix", "category": "recursion",
        "description": "Sudoku solver using backtracking",
        "example_input": {"board": [[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]},
        "steps": [
            {"step": 1, "action": "Find empty cell (0,2)"},
            {"step": 2, "action": "Try 1,2,3... 4 is valid, place 4"},
            {"step": 3, "action": "Continue filling..."},
            {"step": 4, "action": "Backtrack at cell (1,2), try next number"},
            {"step": 5, "action": "Board complete! Sudoku solved!"},
        ]
    },
    # ── MORE DP (6) ──
    "partition_equal_subset": {
        "type": "dp_table", "category": "dp",
        "description": "Can partition array into equal sum subsets",
        "example_input": [1, 5, 11, 5],
        "steps": [
            {"step": 1, "total": 22, "target": 11, "action": "Sum=22, target=11. Find subset sum=11"},
            {"step": 2, "dp": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "action": "dp[0]=True (empty set sums to 0)"},
            {"step": 3, "dp": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "action": "Include 1: dp[1]=True"},
            {"step": 4, "dp": [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], "action": "Include 5: dp[5]=dp[6]=True"},
            {"step": 5, "dp": "dp[11]=True!", "action": "Include 11: dp[11]=True → can partition!"},
        ]
    },
    "word_break": {
        "type": "dp_table", "category": "dp",
        "description": "Can string be segmented into dictionary words",
        "example_input": {"s": "leetcode", "wordDict": ["leet", "code"]},
        "steps": [
            {"step": 1, "dp": [1, 0, 0, 0, 0, 0, 0, 0, 0], "action": "dp[0]=True (empty string)"},
            {"step": 2, "dp": [1, 0, 0, 0, 1, 0, 0, 0, 0], "action": "Check: 'leet' found → dp[4]=True"},
            {"step": 3, "dp": [1, 0, 0, 0, 1, 0, 0, 0, 1], "action": "From idx 4: 'code' found → dp[8]=True"},
            {"step": 4, "result": True, "action": "dp[8]=True → can be segmented!"},
        ]
    },
    # ── ADDITIONAL SORTING (2) ──
    "bucket_sort": {
        "type": "bars", "category": "sorting",
        "description": "Bucket sort — distribute into buckets, sort individually",
        "example_input": [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68],
        "steps": [
            {"step": 1, "buckets": [[],[],[],[],[],[],[],[],[],[]], "action": "Create 10 empty buckets"},
            {"step": 2, "buckets": "Distribute: 0.78→7, 0.17→1, 0.39→3...", "action": "Place each element in bucket by 10×value"},
            {"step": 3, "buckets": "[[0.12],[0.17],[0.21,0.23,0.26],[0.39],[0.68],[0.72,0.78],[0.94],[],...]", "action": "Elements distributed into buckets"},
            {"step": 4, "result": [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94], "action": "Sorted! Concatenate buckets in order"},
        ]
    },
    "shell_sort": {
        "type": "bars", "category": "sorting",
        "description": "Shell sort — insertion sort with diminishing gaps",
        "example_input": [23, 29, 15, 19, 31, 7, 9, 5, 2],
        "steps": [
            {"step": 1, "gap": 4, "action": "Gap=4: sort subarrays (23,31,2), (29,7), (15,9), (19,5)"},
            {"step": 2, "array": [2, 7, 9, 5, 23, 29, 15, 19, 31], "action": "After gap 4 pass: partially sorted"},
            {"step": 3, "gap": 2, "action": "Gap=2: sort interleaved pairs"},
            {"step": 4, "array": [2, 5, 9, 7, 15, 19, 23, 29, 31], "action": "After gap 2 pass: much closer to sorted"},
            {"step": 5, "gap": 1, "action": "Gap=1: final insertion sort pass"},
            {"step": 6, "array": [2, 5, 7, 9, 15, 19, 23, 29, 31], "action": "Sorted!"},
        ]
    },
    # ── SLIDING WINDOW (2) ──
    "max_sliding_window": {
        "type": "array", "category": "sliding_window",
        "description": "Maximum element in every sliding window of size k",
        "example_input": {"nums": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3},
        "steps": [
            {"step": 1, "deque": [1], "action": "Window [1,3,-1]: deque=[1], then 3>1 → pop, deque=[3], then -1<3 → deque=[3,-1], max=3"},
            {"step": 2, "deque": [3, -1, -3], "max": 3, "action": "Window [3,-1,-3]: -1>-3 → deque=[3,-1,-3], max=3"},
            {"step": 3, "deque": [5], "max": 5, "action": "Window [-1,-3,5]: 5 > all, deque=[5], max=5"},
            {"step": 4, "deque": [6], "max": 6, "action": "Window [-3,5,3]: deque=[5,3], then 6→deque=[6], max=6"},
            {"step": 5, "deque": [7], "max": 7, "action": "Window [5,3,6]: 6 windows done. Result=[3,3,5,5,6,7]"},
        ]
    },
    "min_window_substring": {
        "type": "array", "category": "sliding_window",
        "description": "Minimum window containing all target characters",
        "example_input": {"s": "ADOBECODEBANC", "t": "ABC"},
        "steps": [
            {"step": 1, "window": "ADOBEC", "action": "Expand right: found A,D,O,B,E,C → 'ADOBEC' has A,B,C. Shrink left"},
            {"step": 2, "window": "DOBEC", "action": "Shrink: remove A, still has B,C. Expand: no"},
            {"step": 3, "window": "OBEC", "action": "Shrink: remove D. Need A, expand..."},
            {"step": 4, "window": "BECODEBA", "action": "Expand right until A found. Continue sliding..."},
            {"step": 5, "window": "BANC", "action": "Found 'BANC' = min window with A,B,C → length 4"},
        ]
    },
}

# ─── Comparison Mode — run two algorithms side by side ───
COMPARISON_PAIRS = {
    "sorting_bfs_vs_dfs": {
        "title": "BFS vs DFS Traversal",
        "algorithms": ["bfs", "dfs"],
        "description": "Compare BFS (level-order) vs DFS (depth-first) traversal on the same graph",
    },
    "sorting_bubble_vs_quick": {
        "title": "Bubble Sort vs Quick Sort",
        "algorithms": ["bubble_sort", "quick_sort"],
        "description": "Compare O(n²) bubble sort vs O(n log n) quick sort",
    },
    "sorting_merge_vs_quick": {
        "title": "Merge Sort vs Quick Sort",
        "algorithms": ["merge_sort", "quick_sort"],
        "description": "Compare stable merge sort vs in-place quick sort",
    },
    "search_linear_vs_binary": {
        "title": "Linear Search vs Binary Search",
        "algorithms": ["linear_search", "binary_search"],
        "description": "Compare O(n) linear search vs O(log n) binary search",
    },
    "dijkstra_vs_bellman": {
        "title": "Dijkstra vs Bellman-Ford",
        "algorithms": ["dijkstra", "bellman_ford"],
        "description": "Compare Dijkstra (no negatives) vs Bellman-Ford (handles negatives)",
    },
    "prim_vs_kruskal": {
        "title": "Prim's vs Kruskal's MST",
        "algorithms": ["prim_mst", "kruskal_mst"],
        "description": "Compare Prim's (grows from start) vs Kruskal's (sorts all edges)",
    },
}

@router.get("/compare")
async def list_comparisons():
    """List available algorithm comparison pairs."""
    result = []
    for key, val in COMPARISON_PAIRS.items():
        result.append({"id": key, "title": val["title"], "description": val["description"]})
    return {"comparisons": result, "total": len(result)}


@router.get("/compare/{comparison_id}")
async def run_comparison(comparison_id: str):
    """Run a side-by-side comparison of two algorithms."""
    if comparison_id not in COMPARISON_PAIRS:
        raise HTTPException(status_code=404, detail=f"Comparison '{comparison_id}' not found")
    pair = COMPARISON_PAIRS[comparison_id]
    algo_a_id, algo_b_id = pair["algorithms"]
    algo_a = VISUALIZATION_TEMPLATES.get(algo_a_id)
    algo_b = VISUALIZATION_TEMPLATES.get(algo_b_id)
    if not algo_a or not algo_b:
        raise HTTPException(status_code=404, detail=f"Algorithm template not found")
    return {
        "title": pair["title"],
        "description": pair["description"],
        "algorithms": [
            {"id": algo_a_id, "name": algo_a_id.replace("_", " ").title(), "type": algo_a["type"], "steps": algo_a["steps"], "example_input": algo_a.get("example_input")},
            {"id": algo_b_id, "name": algo_b_id.replace("_", " ").title(), "type": algo_b["type"], "steps": algo_b["steps"], "example_input": algo_b.get("example_input")},
        ]
    }


@router.get("/templates")
async def get_visualization_templates():
    """Get all available visualization templates grouped by category."""
    categories: Dict[str, List] = {}
    for key, template in VISUALIZATION_TEMPLATES.items():
        cat = template.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            "id": key,
            "type": template["type"],
            "description": template["description"],
        })
    return {"templates": categories, "total": len(VISUALIZATION_TEMPLATES)}


@router.get("/template/{template_id}")
async def get_template(template_id: str):
    """Get a specific visualization template with full step data."""
    if template_id not in VISUALIZATION_TEMPLATES:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    return VISUALIZATION_TEMPLATES[template_id]


@router.post("/generate/{question_id}")
async def generate_visualization(
    question_id: str,
    test_case_input: str,
    user=Depends(get_current_user),
):
    """Generate a step-by-step visualization for a problem's execution."""
    collection = curated_questions_collection()

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    title = question.get("question_title", "Unknown")
    statement = question.get("statement", "")
    topics = question.get("topics", [])
    solution = question.get("solution", {})
    solution_code = solution.get("code", "")

    prompt = f"""You are an algorithm visualization expert. Generate a step-by-step dry run for this coding problem.

Problem: {title}
Statement: {statement}
Topics: {', '.join(topics)}
Solution Code:
```python
{solution_code}
```

Input for this run: {test_case_input}

Generate a detailed step-by-step execution trace in this EXACT JSON format:
{{
  "title": "{title}",
  "algorithm": "name of the algorithm used",
  "input": "{test_case_input}",
  "steps": [
    {{
      "step": 1,
      "line": <line number in code>,
      "action": "description of what this line does",
      "variables": {{"var1": "value1", "var2": "value2"}},
      "highlight": "which part of the code to highlight",
      "explanation": "why this step is important"
    }}
  ],
  "output": "final output of the algorithm",
  "complexity": {{
    "time": "O(n)",
    "space": "O(1)"
  }},
  "key_insights": ["insight1", "insight2"]
}}

Make the steps clear, educational, and easy to follow. Show variable states at each step."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=2000,
        )
        visualization = parse_json(result)
    except Exception:
        visualization = {
            "title": title,
            "algorithm": "Unknown",
            "input": test_case_input,
            "steps": [
                {"step": 1, "action": "Initialize variables", "variables": {}, "explanation": "Start the algorithm"}
            ],
            "output": "N/A",
            "complexity": {"time": "O(n)", "space": "O(1)"},
            "key_insights": ["Visualization generation failed. Please try again."],
        }

    return visualization


@router.post("/trace")
async def generate_code_trace(req: TraceRequest, user=Depends(get_current_user)):
    """Generate a step-by-step trace for arbitrary user code.
    For Python: uses AST-level instrumentation (real execution trace).
    For other languages: uses AI-generated traces.
    """
    # ── Python: AST-based real execution trace ──
    if req.language.lower() == "python":
        trace_result = execute_with_trace(req.code, req.stdin)

        if trace_result["steps"] and not trace_result["error"]:
            # Successfully traced via AST
            algo = detect_algorithm_type(req.code, trace_result["steps"])
            steps = []
            for s in trace_result["steps"]:
                steps.append({
                    "step": s.get("step", 0),
                    "line": s.get("line", 0),
                    "action": f"Line {s.get('line', '?')}",
                    "variables": s.get("vars", {}),
                })
            return {
                "algorithm": algo,
                "steps": steps,
                "output": trace_result.get("output", ""),
                "time_complexity": "detected",
                "space_complexity": "detected",
                "key_insights": [
                    f"Traced {len(steps)} execution steps via AST instrumentation",
                    f"Detected algorithm pattern: {algo}",
                ],
                "source": "ast_trace",
            }

    # ── Fallback: AI-generated trace for any language ──
    prompt = f"""You are an algorithm visualization expert. Trace the execution of this code step by step.

Language: {req.language}
Code:
```{req.language}
{req.code}
```

Input: {req.stdin or "(no input)"}

Generate a trace in this EXACT JSON format:
{{
  "algorithm": "name of the algorithm/pattern detected",
  "steps": [
    {{
      "step": 1,
      "line": <line number>,
      "action": "what this line does",
      "variables": {{"var1": "value1"}},
      "explanation": "educational explanation"
    }}
  ],
  "output": "final output",
  "time_complexity": "O(...)",
  "space_complexity": "O(...)",
  "key_insights": ["insight1", "insight2"]
}}

Make every step educational. Show variable values changing at each step.
If the code has loops, show how variables change each iteration.
If the code has recursion, show the call stack depth."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=3000,
        )
        trace = parse_json(result)
        if not isinstance(trace, dict):
            raise ValueError("Invalid trace format")
        trace["source"] = "ai_trace"
        return trace
    except Exception:
        return {
            "algorithm": "Unknown",
            "steps": [
                {"step": 1, "action": "Code execution started", "variables": {}, "explanation": "Trace generation failed — try simpler code"}
            ],
            "output": "N/A",
            "time_complexity": "O(?)",
            "space_complexity": "O(?)",
            "key_insights": ["Could not generate trace. Try reducing code complexity."],
            "source": "fallback",
        }


@router.get("/algorithm/{algorithm_name}")
async def get_algorithm_explanation(algorithm_name: str):
    """Get detailed explanation of an algorithm with visualization."""
    name = algorithm_name.lower().replace("-", "_").replace(" ", "_")

    # Check if it's a pre-built template
    if name in VISUALIZATION_TEMPLATES:
        template = VISUALIZATION_TEMPLATES[name]
        return {
            "name": name.replace("_", " ").title(),
            "description": template["description"],
            "category": template.get("category", "other"),
            "visualization": template,
        }

    # Extended algorithm explanations
    algorithms = {
        "two_pointer": {
            "name": "Two Pointers",
            "description": "Use two pointers to traverse an array, often from opposite ends or same direction.",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "when_to_use": ["Sorted array", "Pair problems", "Palindrome check"],
            "key_concept": "Move pointers based on comparison with target",
        },
        "dynamic_programming": {
            "name": "Dynamic Programming",
            "description": "Solve complex problems by breaking them into overlapping subproblems and storing solutions.",
            "time_complexity": "O(n) to O(n*m)",
            "space_complexity": "O(n) to O(n*m)",
            "when_to_use": ["Optimal substructure", "Overlapping subproblems", "Counting problems"],
            "key_concept": "Build solutions from smaller subproblems",
        },
        "greedy": {
            "name": "Greedy Algorithm",
            "description": "Make locally optimal choice at each step for global optimum.",
            "time_complexity": "O(n log n) typically",
            "space_complexity": "O(1) to O(n)",
            "when_to_use": ["Activity selection", "Huffman coding", "Fractional knapsack"],
            "key_concept": "Always pick the best immediate option",
        },
        "divide_and_conquer": {
            "name": "Divide and Conquer",
            "description": "Break problem into smaller subproblems, solve recursively, combine results.",
            "time_complexity": "O(n log n) typically",
            "space_complexity": "O(log n) to O(n)",
            "when_to_use": ["Merge sort", "Quick sort", "Binary search"],
            "key_concept": "Divide → Conquer → Combine",
        },
        "bit_manipulation": {
            "name": "Bit Manipulation",
            "description": "Use bitwise operations for efficient computation.",
            "time_complexity": "O(1) to O(n)",
            "space_complexity": "O(1)",
            "when_to_use": ["Toggle/check/set bits", "XOR tricks", "Power of 2 checks"],
            "key_concept": "Use &, |, ^, ~, <<, >> for optimization",
        },
    }

    if name not in algorithms:
        raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm_name}' not found")

    return algorithms[name]


@router.get("/algorithms")
async def list_algorithms():
    """List all available algorithm visualizations."""
    by_category: Dict[str, List] = {}
    for key, template in VISUALIZATION_TEMPLATES.items():
        cat = template.get("category", "other")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append({
            "id": key,
            "name": key.replace("_", " ").title(),
            "type": template["type"],
            "description": template["description"],
        })

    return {
        "algorithms": by_category,
        "total": len(VISUALIZATION_TEMPLATES),
        "categories": list(by_category.keys()),
    }
