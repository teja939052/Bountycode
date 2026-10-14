"""Expand verified banks with additional sourced questions.

This script adds new questions to the verified banks from legitimate public
sources. Each question includes:
- Real problem statement
- Real solution code
- Real test cases with expected outputs
- Proper metadata

After adding, run auto_verify.py to set trust_status correctly.
"""
import json
import os
from datetime import datetime, timezone

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BACKEND_ROOT, "app", "data")


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _base_question(qid, qtype, title, question, difficulty, topic, sub_topic="",
                   pattern="", skill="", companies=None, role=None,
                   provenance="public-source-2026", source_bank=""):
    return {
        "id": qid,
        "type": qtype,
        "title": title,
        "question": question,
        "difficulty": difficulty,
        "topic": topic,
        "sub_topic": sub_topic,
        "pattern": pattern or topic,
        "skill": skill or topic,
        "companies": companies or [],
        "role": role or ["student", "sde"],
        "provenance": provenance,
        "source_bank": source_bank,
        "trust_status": "unverified",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }


def _coding_question(qid, title, question, difficulty, topic, sub_topic, pattern,
                     solution_code, testcases, hidden_testcases=None,
                     companies=None, role=None, explanation="", hints=None,
                     constraints=None, common_trap="", dsa_guide=None):
    q = _base_question(
        qid, "coding", title, question, difficulty, topic, sub_topic, pattern,
        skill=topic, companies=companies, role=role,
        provenance="public-source-2026", source_bank="verified_placement_questions",
    )
    q["solution"] = {"code": solution_code, "language": "python"}
    q["testcases"] = testcases
    q["hidden_testcases"] = hidden_testcases or []
    q["examples"] = testcases[:3] if testcases else []
    q["explanation"] = explanation
    q["hints"] = hints or []
    q["constraints"] = constraints or []
    q["common_trap"] = common_trap
    q["dsa_guide"] = dsa_guide or {
        "approach": "", "data_structures": [], "patterns": [pattern or topic], "tips": []
    }
    return q


def _sql_question(qid, question, correct_answer, difficulty, sub_topic,
                  options, correct_index, explanation, hints,
                  companies=None, role=None, testcases=None, hidden_testcases=None):
    q = _base_question(
        qid, "sql", question, question, difficulty, "sql", sub_topic,
        pattern="sql", skill="sql", companies=companies, role=role,
        provenance="public-source-2026", source_bank="sql_practice_bank",
    )
    q["correct_answer"] = correct_answer
    q["options"] = options
    q["correct_index"] = correct_index
    q["solution"] = {
        "code": correct_answer,
        "explanation": explanation,
    }
    q["testcases"] = testcases or []
    q["hidden_testcases"] = hidden_testcases or []
    q["hints"] = hints or []
    q["common_trap"] = ""
    q["reasoning_steps"] = []
    return q


def _interview_question(qid, question, topic, sub_topic, difficulty,
                        correct_answer, companies=None, role=None,
                        explanation="", hints=None, testcases=None, hidden_testcases=None):
    q = _base_question(
        qid, "interview", question, question, difficulty, topic, sub_topic,
        pattern=topic, skill=topic, companies=companies, role=role,
        provenance="public-source-2026", source_bank="interview_practice_bank",
    )
    q["correct_answer"] = correct_answer
    q["options"] = []
    q["solution"] = {
        "code": "",
        "explanation": explanation or correct_answer,
    }
    q["testcases"] = testcases or []
    q["hidden_testcases"] = hidden_testcases or []
    q["hints"] = hints or []
    q["common_trap"] = ""
    q["reasoning_steps"] = []
    return q


def _aptitude_question(qid, question, topic, sub_topic, difficulty,
                       options, correct_index, explanation, hints,
                       companies=None, role=None, testcases=None, hidden_testcases=None):
    q = _base_question(
        qid, "aptitude", question, question, difficulty, topic, sub_topic,
        pattern="aptitude", skill=topic, companies=companies, role=role,
        provenance="public-source-2026", source_bank="india_placement_depth",
    )
    q["options"] = options
    q["correct_index"] = correct_index
    q["correct_answer"] = options[correct_index] if correct_index < len(options) else ""
    q["solution"] = {
        "code": "",
        "explanation": explanation,
    }
    q["testcases"] = testcases or []
    q["hidden_testcases"] = hidden_testcases or []
    q["hints"] = hints or []
    q["common_trap"] = ""
    q["reasoning_steps"] = []
    return q


def expand_verified_placement_questions():
    """Add coding and aptitude questions to verified_placement_questions.json."""
    path = os.path.join(DATA_DIR, "verified_placement_questions.json")
    with open(path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {q.get("id") for q in existing}
    new_questions = []

    # ---------- Coding: Linked Lists ----------
    linked_list_questions = [
        _coding_question(
            "verify-ll-001",
            "Reverse Linked List",
            "Given the head of a singly linked list, reverse the list and return the reversed list.",
            "easy", "linked-lists", " reversal", "Linked Lists",
            "def reverse_list(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev\n",
            testcases=[
                {"input": "1->2->3->4->5", "expected": "5->4->3->2->1"},
                {"input": "1->2", "expected": "2->1"},
                {"input": "[]", "expected": "[]"},
            ],
            hidden_testcases=[
                {"input": "1", "expected": "1"},
                {"input": "1->2->3->4->5->6", "expected": "6->5->4->3->2->1"},
            ],
            companies=["amazon", "microsoft", "meta", "google"],
            role=["sde", "backend-engineer"],
            explanation="Iterate through the list, reversing each link. Time O(n), space O(1).",
            hints=["Keep track of prev, curr, next", "Update curr.next to prev before moving forward"],
            constraints=["1 <= n <= 10^5"],
            common_trap="Losing the next pointer before redirecting curr.next",
            dsa_guide={"approach": "Iterative pointer reversal", "data_structures": ["Linked List"], "patterns": ["Linked Lists"], "tips": ["Use three pointers"]},
        ),
        _coding_question(
            "verify-ll-002",
            "Linked List Cycle",
            "Given head of a linked list, determine if the list contains a cycle.",
            "easy", "linked-lists", "cycle-detection", "Linked Lists",
            "def has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            return True\n    return False\n",
            testcases=[
                {"input": "3->2->0->-4 (cycle at pos 1)", "expected": True},
                {"input": "1->2 (no cycle)", "expected": False},
                {"input": "1 (no cycle)", "expected": False},
            ],
            hidden_testcases=[
                {"input": "1->2->3->4->5->6 (no cycle)", "expected": False},
                {"input": "1->2->3->4->5->1 (cycle)", "expected": True},
            ],
            companies=["amazon", "microsoft", "meta"],
            role=["sde", "backend-engineer"],
            explanation="Use Floyd's Tortoise and Hare. If slow == fast, cycle exists.",
            hints=["Two pointers at different speeds", "If they meet, cycle exists"],
            constraints=["1 <= n <= 10^4"],
            common_trap="Comparing values instead of node references",
            dsa_guide={"approach": "Floyd cycle detection", "data_structures": ["Linked List"], "patterns": ["Linked Lists", "Two Pointers"], "tips": ["Slow moves 1, fast moves 2"]},
        ),
        _coding_question(
            "verify-ll-003",
            "Merge Two Sorted Lists",
            "Merge two sorted linked lists and return the merged list.",
            "easy", "linked-lists", "merge", "Linked Lists",
            "def merge_two_lists(l1, l2):\n    dummy = node = type('Node', (), {'val': 0, 'next': None})()\n    while l1 and l2:\n        if l1.val < l2.val:\n            node.next = l1\n            l1 = l1.next\n        else:\n            node.next = l2\n            l2 = l2.next\n        node = node.next\n    node.next = l1 or l2\n    return dummy.next\n",
            testcases=[
                {"input": "1->2->4, 1->3->4", "expected": "1->1->2->3->4->4"},
                {"input": "[], 1->2->3", "expected": "1->2->3"},
                {"input": "1->2->3, []", "expected": "1->2->3"},
            ],
            hidden_testcases=[
                {"input": "1->3->5, 2->4->6", "expected": "1->2->3->4->5->6"},
                {"input": "1->1->1, 1->1->1", "expected": "1->1->1->1->1->1"},
            ],
            companies=["amazon", "microsoft", "google"],
            role=["sde", "backend-engineer"],
            explanation="Use a dummy head. Attach the smaller node each step. Append remainder.",
            hints=["Maintain a tail pointer", "Attach remaining list at end"],
            constraints=["0 <= n <= 50"],
            common_trap="Forgetting to advance the chosen list pointer",
            dsa_guide={"approach": "Two-pointer merge with dummy head", "data_structures": ["Linked List"], "patterns": ["Linked Lists", "Two Pointers"], "tips": ["Reuse existing nodes"]},
        ),
    ]

    # ---------- Coding: Trees ----------
    tree_questions = [
        _coding_question(
            "verify-tree-001",
            "Maximum Depth of Binary Tree",
            "Given the root of a binary tree, return its maximum depth.",
            "easy", "trees", "depth", "Trees",
            "def max_depth(root):\n    if not root:\n        return 0\n    return 1 + max(max_depth(root.left), max_depth(root.right))\n",
            testcases=[
                {"input": "[3,9,20,null,null,15,7]", "expected": 3},
                {"input": "[1,null,2]", "expected": 2},
                {"input": "[]", "expected": 0},
            ],
            hidden_testcases=[
                {"input": "[1,2,3,4,5,6,7]", "expected": 3},
                {"input": "[1,2,null,3]", "expected": 3},
            ],
            companies=["amazon", "microsoft", "meta", "google"],
            role=["sde", "backend-engineer"],
            explanation="Recursively compute depth = 1 + max(left, right). Base: empty tree = 0.",
            hints=["Base case: None returns 0", "Depth = 1 + max(left, right)"],
            constraints=["0 <= n <= 10^4"],
            common_trap="Counting nodes instead of edges",
            dsa_guide={"approach": "DFS recursion", "data_structures": ["Binary Tree"], "patterns": ["Trees"], "tips": ["Post-order traversal"]},
        ),
        _coding_question(
            "verify-tree-002",
            "Validate Binary Search Tree",
            "Given the root of a binary tree, determine if it is a valid BST.",
            "medium", "trees", "bst", "Binary Search Trees",
            "def is_valid_bst(root):\n    def helper(node, low, high):\n        if not node:\n            return True\n        if not (low < node.val < high):\n            return False\n        return helper(node.left, low, node.val) and helper(node.right, node.val, high)\n    return helper(root, float('-inf'), float('inf'))\n",
            testcases=[
                {"input": "[2,1,3]", "expected": True},
                {"input": "[5,1,4,null,null,3,6]", "expected": False},
                {"input": "[]", "expected": True},
            ],
            hidden_testcases=[
                {"input": "[5,4,6,null,null,3,7]", "expected": False},
                {"input": "[2,2,2]", "expected": False},
            ],
            companies=["amazon", "microsoft", "google", "meta"],
            role=["sde", "backend-engineer"],
            explanation="Each node must lie in (low, high). Recurse with updated bounds.",
            hints=["Use min/max bounds per node", "Left subtree must be < node.val"],
            constraints=["-10^4 <= node.val <= 10^4"],
            common_trap="Only checking immediate children, not the whole subtree",
            dsa_guide={"approach": "DFS with bounds", "data_structures": ["Binary Search Tree"], "patterns": ["Binary Search Trees"], "tips": ["Pass min/max down"]},
        ),
        _coding_question(
            "verify-tree-003",
            "Binary Tree Level Order Traversal",
            "Return the level order traversal of a binary tree's node values.",
            "medium", "trees", "bfs", "BFS & DFS",
            "from collections import deque\n\ndef level_order(root):\n    if not root:\n        return []\n    q = deque([root])\n    out = []\n    while q:\n        level = []\n        for _ in range(len(q)):\n            node = q.popleft()\n            level.append(node.val)\n            if node.left:\n                q.append(node.left)\n            if node.right:\n                q.append(node.right)\n        out.append(level)\n    return out\n",
            testcases=[
                {"input": "[3,9,20,null,null,15,7]", "expected": "[[3],[9,20],[15,7]]"},
                {"input": "[1]", "expected": "[[1]]"},
                {"input": "[]", "expected": "[]"},
            ],
            hidden_testcases=[
                {"input": "[1,2,3,4,5,6,7]", "expected": "[[1],[2,3],[4,5,6,7]]"},
            ],
            companies=["amazon", "microsoft", "meta"],
            role=["sde", "backend-engineer"],
            explanation="BFS with queue. Snapshot queue length per level.",
            hints=["Use deque for O(1) pops", "Process exactly len(q) nodes per level"],
            constraints=["0 <= n <= 2000"],
            common_trap="Mixing levels because queue length changes mid-loop",
            dsa_guide={"approach": "BFS with level snapshots", "data_structures": ["Queue", "Binary Tree"], "patterns": ["BFS & DFS"], "tips": ["For loop over len(q) locks the level"]},
        ),
    ]

    # ---------- Coding: Dynamic Programming ----------
    dp_questions = [
        _coding_question(
            "verify-dp-001",
            "Climbing Stairs",
            "You are climbing stairs. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. Return the number of distinct ways to reach the top.",
            "easy", "dynamic-programming", "1d-dp", "Dynamic Programming 1D",
            "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n",
            testcases=[
                {"input": 2, "expected": 2},
                {"input": 3, "expected": 3},
                {"input": 5, "expected": 8},
            ],
            hidden_testcases=[
                {"input": 1, "expected": 1},
                {"input": 10, "expected": 89},
            ],
            companies=["amazon", "google", "microsoft", "meta"],
            role=["sde", "backend-engineer"],
            explanation="Ways(n) = Ways(n-1) + Ways(n-2). Use two variables.",
            hints=["Fibonacci pattern", "O(1) space with two variables"],
            constraints=["1 <= n <= 45"],
            common_trap="Off-by-one on base cases",
            dsa_guide={"approach": "Bottom-up DP with rolling variables", "data_structures": [], "patterns": ["Dynamic Programming 1D"], "tips": ["Fibonacci recurrence"]},
        ),
        _coding_question(
            "verify-dp-002",
            "Longest Increasing Subsequence",
            "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
            "medium", "dynamic-programming", "lis", "Dynamic Programming 1D",
            "def length_of_lis(nums):\n    tails = []\n    for x in nums:\n        i = __import__('bisect').bisect_left(tails, x)\n        if i == len(tails):\n            tails.append(x)\n        else:\n            tails[i] = x\n    return len(tails)\n",
            testcases=[
                {"input": "[10,9,2,5,3,7,101,18]", "expected": 4},
                {"input": "[0,1,0,3,2,3]", "expected": 4},
                {"input": "[7,7,7,7,7,7,7]", "expected": 1},
            ],
            hidden_testcases=[
                {"input": "[1,3,6,7,9,4,10,5,6]", "expected": 6},
                {"input": "[2,2,2,2,2]", "expected": 1},
            ],
            companies=["amazon", "google", "microsoft", "meta"],
            role=["sde", "backend-engineer"],
            explanation="Patience sorting with binary search. tails[i] = smallest tail of all increasing subarrays of length i+1.",
            hints=["Maintain tails array", "Use bisect_left"],
            constraints=["1 <= nums.length <= 2500"],
            common_trap="Using O(n^2) DP without realizing binary search optimization",
            dsa_guide={"approach": "Patience sorting / binary search on tails", "data_structures": ["Array"], "patterns": ["Dynamic Programming 1D", "Binary Search"], "tips": ["tails is not the LIS, only its length"]},
        ),
        _coding_question(
            "verify-dp-003",
            "Coin Change",
            "Given coin denominations and a total amount, return the fewest number of coins needed.",
            "medium", "dynamic-programming", "knapsack", "Dynamic Programming 1D",
            "def coin_change(coins, amount):\n    INF = amount + 1\n    dp = [INF] * (amount + 1)\n    dp[0] = 0\n    for coin in coins:\n        for x in range(coin, amount + 1):\n            dp[x] = min(dp[x], dp[x - coin] + 1)\n    return dp[amount] if dp[amount] != INF else -1\n",
            testcases=[
                {"input": "[1,2,5], 11", "expected": 3},
                {"input": "[2], 3", "expected": -1},
                {"input": "[1], 0", "expected": 0},
            ],
            hidden_testcases=[
                {"input": "[1,3,4,5], 7", "expected": 2},
                {"input": "[2,5,10,1], 27", "expected": 4},
            ],
            companies=["amazon", "microsoft", "google"],
            role=["sde", "backend-engineer"],
            explanation="Unbounded knapsack: dp[amount] = min(dp[amount], dp[amount - coin] + 1).",
            hints=["Initialize dp[0]=0, others=INF", "Unbounded: inner loop forward"],
            constraints=["1 <= coins.length <= 12", "1 <= amount <= 10^4"],
            common_trap="Using 1-indexed amounts or forgetting INF sentinel",
            dsa_guide={"approach": "Bottom-up unbounded knapsack", "data_structures": ["Array"], "patterns": ["Dynamic Programming 1D"], "tips": ["Forward loop for unbounded"]},
        ),
    ]

    # ---------- Coding: Graphs ----------
    graph_questions = [
        _coding_question(
            "verify-graph-001",
            "Number of Islands",
            "Given a 2D grid of '1's (land) and '0's (water), return the number of islands.",
            "medium", "graphs", "bfs-dfs", "BFS & DFS",
            "def num_islands(grid):\n    if not grid:\n        return 0\n    rows, cols = len(grid), len(grid[0])\n    def dfs(r, c):\n        if not (0 <= r < rows and 0 <= c < cols and grid[r][c] == '1'):\n            return\n        grid[r][c] = '0'\n        dfs(r+1, c)\n        dfs(r-1, c)\n        dfs(r, c+1)\n        dfs(r, c-1)\n    count = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == '1':\n                dfs(r, c)\n                count += 1\n    return count\n",
            testcases=[
                {"input": "[['1','1','1','1','0'],['1','1','0','1','0'],['1','0','0','0','0'],['0','0','1','0','0']]", "expected": 3},
                {"input": "[['1','0','0'],['0','1','0'],['0','0','1']]", "expected": 3},
                {"input": "[['0','0'],['0','0']]", "expected": 0},
            ],
            hidden_testcases=[
                {"input": "[['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']]", "expected": 2},
            ],
            companies=["amazon", "microsoft", "meta", "google"],
            role=["sde", "backend-engineer"],
            explanation="Sink each island with DFS/BFS. Count how many times you start a new search.",
            hints=["Mutate grid in-place to mark visited", "Recurse in 4 directions"],
            constraints=["1 <= m,n <= 300"],
            common_trap="Out-of-bounds access on edges",
            dsa_guide={"approach": "DFS flood fill", "data_structures": ["Matrix"], "patterns": ["BFS & DFS", "Graphs"], "tips": ["Mark visited by setting to '0'"]},
        ),
        _coding_question(
            "verify-graph-002",
            "Course Schedule",
            "Return True if you can finish all courses given prerequisites.",
            "medium", "graphs", "topological-sort", "Graphs",
            "def can_finish(num_courses, prerequisites):\n    adj = [[] for _ in range(num_courses)]\n    indeg = [0] * num_courses\n    for dest, src in prerequisites:\n        adj[src].append(dest)\n        indeg[dest] += 1\n    q = [i for i in range(num_courses) if indeg[i] == 0]\n    visited = 0\n    while q:\n        node = q.pop()\n        visited += 1\n        for nxt in adj[node]:\n            indeg[nxt] -= 1\n            if indeg[nxt] == 0:\n                q.append(nxt)\n    return visited == num_courses\n",
            testcases=[
                {"input": "2, [[1,0]]", "expected": True},
                {"input": "2, [[1,0],[0,1]]", "expected": False},
                {"input": "3, [[0,1],[0,2],[1,2]]", "expected": True},
            ],
            hidden_testcases=[
                {"input": "4, [[1,0],[2,0],[3,1],[3,2]]", "expected": True},
                {"input": "4, [[0,1],[1,2],[2,3],[3,0]]", "expected": False},
            ],
            companies=["amazon", "microsoft", "meta", "google"],
            role=["sde", "backend-engineer"],
            explanation="Kahn's algorithm: remove nodes with indegree 0. If all removed, no cycle.",
            hints=["Build adjacency list and indegree array", "Queue nodes with indegree 0"],
            constraints=["1 <= num_courses <= 2000"],
            common_trap="Forgetting to decrement indegree before enqueue",
            dsa_guide={"approach": "Topological sort / Kahn's algorithm", "data_structures": ["Queue", "Graph"], "patterns": ["Graphs", "Topological Sort"], "tips": ["Count processed nodes"]},
        ),
    ]

    # ---------- Coding: Heaps / Priority Queue ----------
    heap_questions = [
        _coding_question(
            "verify-heap-001",
            "Kth Largest Element in an Array",
            "Return the kth largest element in the array.",
            "medium", "heaps", "priority-queue", "Heaps / Priority Queue",
            "import heapq\n\ndef find_kth_largest(nums, k):\n    return heapq.nlargest(k, nums)[-1]\n",
            testcases=[
                {"input": "[3,2,1,5,6,4], 2", "expected": 5},
                {"input": "[3,2,3,1,2,4,5,5,6], 4", "expected": 4},
            ],
            hidden_testcases=[
                {"input": "[1,2,3,4,5], 5", "expected": 1},
                {"input": "[7,6,5,4,3,2,1], 3", "expected": 5},
            ],
            companies=["amazon", "microsoft", "meta"],
            role=["sde", "backend-engineer"],
            explanation="Use a min-heap of size k, or nth-element. heapq.nlargest(k)[-1] is fine.",
            hints=["Maintain heap of size k", "nlargest returns descending order"],
            constraints=["1 <= k <= nums.length <= 10^5"],
            common_trap="Sorting when k is small relative to n",
            dsa_guide={"approach": "Min-heap of size k or quickselect", "data_structures": ["Heap"], "patterns": ["Heaps / Priority Queue"], "tips": ["O(n log k)"]},
        ),
        _coding_question(
            "verify-heap-002",
            "Merge K Sorted Lists",
            "Merge k sorted linked lists and return it as one sorted list.",
            "hard", "linked-lists", "merge", "Heaps / Priority Queue",
            "import heapq\n\ndef merge_k_lists(lists):\n    heap = []\n    for i, node in enumerate(lists):\n        if node:\n            heapq.heappush(heap, (node.val, i, node))\n    dummy = node = type('Node', (), {'val': 0, 'next': None})()\n    while heap:\n        _, i, curr = heapq.heappop(heap)\n        node.next = curr\n        node = node.next\n        if curr.next:\n            heapq.heappush(heap, (curr.next.val, i, curr.next))\n    return dummy.next\n",
            testcases=[
                {"input": "[[1,4,5],[1,3,4],[2,6]]", "expected": "1->1->2->3->4->4->5->6"},
                {"input": "[]", "expected": "[]"},
                {"input": "[[]]", "expected": "[]"},
            ],
            hidden_testcases=[
                {"input": "[[1,3,5],[2,4,6],[7,8,9]]", "expected": "1->2->3->4->5->6->7->8->9"},
            ],
            companies=["amazon", "microsoft", "google", "meta"],
            role=["sde", "backend-engineer"],
            explanation="Push head of each list into min-heap. Pop smallest, advance that list.",
            hints=["Use (value, list_index, node) tuple", "Advance list after pop"],
            constraints=["0 <= k <= 10^4"],
            common_trap="Not storing list index for tie-breaking when values equal",
            dsa_guide={"approach": "Min-heap merge", "data_structures": ["Heap", "Linked List"], "patterns": ["Linked Lists", "Heaps / Priority Queue"], "tips": ["O(N log k)"]},
        ),
    ]

    # ---------- Coding: Greedy ----------
    greedy_questions = [
        _coding_question(
            "verify-greedy-001",
            "Jump Game",
            "Given an array of non-negative integers, return True if you can reach the last index.",
            "medium", "greedy", "jump-game", "Greedy",
            "def can_jump(nums):\n    farthest = 0\n    for i, jump in enumerate(nums):\n        if i > farthest:\n            return False\n        farthest = max(farthest, i + jump)\n    return True\n",
            testcases=[
                {"input": "[2,3,1,1,4]", "expected": True},
                {"input": "[3,2,1,0,4]", "expected": False},
                {"input": "[0]", "expected": True},
            ],
            hidden_testcases=[
                {"input": "[1,1,1,1,1,1,1,1,1,1]", "expected": True},
                {"input": "[5,0,0,0,0,0,0,0,0,0]", "expected": True},
            ],
            companies=["amazon", "microsoft", "google"],
            role=["sde", "backend-engineer"],
            explanation="Track farthest reachable index. If current index > farthest, stuck.",
            hints=["Greedy: keep max reach", "If i exceeds farthest, return False"],
            constraints=["1 <= nums.length <= 10^4"],
            common_trap="Confusing current position with farthest reach",
            dsa_guide={"approach": "Greedy farthest-reach scan", "data_structures": [], "patterns": ["Greedy"], "tips": ["O(n) scan, no DP needed"]},
        ),
        _coding_question(
            "verify-greedy-002",
            "Gas Station",
            "There are n gas stations. Return the starting index if you can complete the circuit.",
            "medium", "greedy", "gas-station", "Greedy",
            "def can_complete_circuit(gas, cost):\n    total_tank = 0\n    curr_tank = 0\n    start = 0\n    for i in range(len(gas)):\n        total_tank += gas[i] - cost[i]\n        curr_tank += gas[i] - cost[i]\n        if curr_tank < 0:\n            start = i + 1\n            curr_tank = 0\n    return start if total_tank >= 0 else -1\n",
            testcases=[
                {"input": "[1,2,3,4,5], [3,4,5,1,2]", "expected": 3},
                {"input": "[2,3,4], [3,4,3]", "expected": -1},
                {"input": "[5,1,2,3,4], [4,4,1,5,1]", "expected": 4},
            ],
            hidden_testcases=[
                {"input": "[3,1,1], [1,5,2]", "expected": -1},
            ],
            companies=["amazon", "microsoft", "google"],
            role=["sde", "backend-engineer"],
            explanation="If total gas >= total cost, solution exists. Reset start when tank goes negative.",
            hints=["Check total gas vs total cost first", "Greedy restart on negative tank"],
            constraints=["gas.length == cost.length", "1 <= n <= 10^5"],
            common_trap="Brute force O(n^2) instead of greedy O(n)",
            dsa_guide={"approach": "Greedy circuit completion", "data_structures": [], "patterns": ["Greedy"], "tips": ["Total tank check first"]},
        ),
    ]

    # ---------- Coding: Backtracking ----------
    backtrack_questions = [
        _coding_question(
            "verify-bt-001",
            "Subsets",
            "Given an array of distinct integers, return all possible subsets.",
            "medium", "recursion-backtracking", "subsets", "Recursion & Backtracking",
            "def subsets(nums):\n    out = []\n    def backtrack(i, path):\n        out.append(path[:])\n        for j in range(i, len(nums)):\n            path.append(nums[j])\n            backtrack(j + 1, path)\n            path.pop()\n    backtrack(0, [])\n    return out\n",
            testcases=[
                {"input": "[1,2,3]", "expected": "[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]"},
                {"input": "[0]", "expected": "[[],[0]]"},
            ],
            hidden_testcases=[
                {"input": "[1,2]", "expected": "[[],[1],[1,2],[2]]"},
            ],
            companies=["amazon", "microsoft", "meta", "google"],
            role=["sde", "backend-engineer"],
            explanation="For each index, choose to include or skip. Backtrack restores state.",
            hints=["Decision: include nums[i] or not", "Append path copy at every node"],
            constraints=["1 <= nums.length <= 10"],
            common_trap="Appending path reference instead of copy",
            dsa_guide={"approach": "DFS with include/skip decisions", "data_structures": [], "patterns": ["Recursion & Backtracking"], "tips": ["Copy path on append"]},
        ),
        _coding_question(
            "verify-bt-002",
            "Permutations",
            "Given an array of distinct integers, return all possible permutations.",
            "medium", "recursion-backtracking", "permutations", "Recursion & Backtracking",
            "def permute(nums):\n    out = []\n    def backtrack(path):\n        if len(path) == len(nums):\n            out.append(path[:])\n            return\n        for x in nums:\n            if x not in path:\n                path.append(x)\n                backtrack(path)\n                path.pop()\n    backtrack([])\n    return out\n",
            testcases=[
                {"input": "[1,2,3]", "expected": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"},
                {"input": "[0,1]", "expected": "[[0,1],[1,0]]"},
                {"input": "[1]", "expected": "[[1]]"},
            ],
            hidden_testcases=[
                {"input": "[1,2,3,4]", "expected": "24 permutations"},
            ],
            companies=["amazon", "microsoft", "meta"],
            role=["sde", "backend-engineer"],
            explanation="Build permutation by choosing unused elements. Backtrack to try next choice.",
            hints=["Track used elements or use 'not in path'", "Base case: len(path) == n"],
            constraints=["1 <= nums.length <= 6"],
            common_trap="Including duplicates when nums has repeats",
            dsa_guide={"approach": "DFS permutation builder", "data_structures": [], "patterns": ["Recursion & Backtracking"], "tips": ["Track visited set"]},
        ),
    ]

    all_new = (
        linked_list_questions + tree_questions + dp_questions +
        graph_questions + heap_questions + greedy_questions + backtrack_questions
    )

    added = 0
    for q in all_new:
        if q["id"] not in existing_ids:
            existing.append(q)
            existing_ids.add(q["id"])
            added += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"verified_placement_questions.json: added {added} new questions")
    return added


def expand_sql_practice_bank():
    """Add SQL questions to sql_practice_bank.json."""
    path = os.path.join(DATA_DIR, "sql_practice_bank.json")
    with open(path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {q.get("id") for q in existing}
    new_questions = [
        _sql_question(
            "sql-055",
            "Find the second highest salary from the Employees table.",
            "SELECT name, salary FROM Employees WHERE salary = (SELECT DISTINCT salary FROM Employees ORDER BY salary DESC LIMIT 1 OFFSET 1);",
            "medium", "subquery",
            [
                "SELECT MAX(salary) FROM Employees;",
                "SELECT name FROM Employees ORDER BY salary DESC LIMIT 1 OFFSET 1;",
                "SELECT name, salary FROM Employees WHERE salary = (SELECT DISTINCT salary FROM Employees ORDER BY salary DESC LIMIT 1 OFFSET 1);",
                "SELECT * FROM Employees WHERE salary = (SELECT MAX(salary) FROM Employees);",
            ],
            2,
            "Use a subquery with ORDER BY DESC and OFFSET 1 to skip the top salary.",
            ["Use DISTINCT in subquery", "OFFSET 1 skips the first row"],
            companies=["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon"],
            role=["student", "sde", "data-analyst"],
            testcases=[
                {"input": "Employees: [(1,'A',80000),(2,'B',90000),(3,'C',90000),(4,'D',70000)]", "expected": "A(80000) or D(70000) depending on distinct handling"}
            ],
            hidden_testcases=[
                {"input": "Employees: [(1,'A',100000)]", "expected": "No second highest"}
            ],
        ),
        _sql_question(
            "sql-056",
            "Find duplicate records in a table Orders(order_id, customer_id, product_id, order_date).",
            "SELECT customer_id, product_id, COUNT(*) FROM Orders GROUP BY customer_id, product_id HAVING COUNT(*) > 1;",
            "medium", "group_by_having",
            [
                "SELECT * FROM Orders WHERE COUNT(*) > 1;",
                "SELECT customer_id, product_id FROM Orders GROUP BY customer_id, product_id HAVING COUNT(*) > 1;",
                "SELECT customer_id, COUNT(*) FROM Orders;",
                "SELECT * FROM Orders GROUP BY customer_id;",
            ],
            1,
            "GROUP BY customer_id and product_id, then HAVING COUNT(*) > 1 filters duplicates.",
            ["GROUP BY requires HAVING for aggregate filter", "COUNT(*) counts rows per group"],
            companies=["tcs", "infosys", "wipro", "cognizant"],
            role=["student", "sde", "data-analyst"],
            testcases=[
                {"input": "Orders: [(1,101,201),(2,101,201),(3,102,301)]", "expected": "(101, 201) appears twice"}
            ],
            hidden_testcases=[
                {"input": "Orders: [(1,101,201),(2,101,202),(3,101,201)]", "expected": "(101, 201) appears twice"}
            ],
        ),
        _sql_question(
            "sql-057",
            "Delete all customers who have never placed an order using a LEFT JOIN.",
            "DELETE Customers FROM Customers LEFT JOIN Orders ON Customers.customer_id = Orders.customer_id WHERE Orders.order_id IS NULL;",
            "medium", "delete_join",
            [
                "DELETE FROM Customers WHERE customer_id NOT IN (SELECT customer_id FROM Orders);",
                "DELETE Customers FROM Customers LEFT JOIN Orders ON Customers.customer_id = Orders.customer_id WHERE Orders.order_id IS NULL;",
                "DELETE * FROM Customers WHERE Orders.order_id IS NULL;",
                "DROP TABLE Customers WHERE customer_id NOT IN Orders;",
            ],
            1,
            "LEFT JOIN keeps all customers; IS NULL identifies those with no orders.",
            ["LEFT JOIN preserves left rows", "IS NULL catches unmatched rows"],
            companies=["tcs", "infosys", "wipro", "accenture"],
            role=["student", "sde", "data-analyst"],
            testcases=[
                {"input": "Customers: [1,2,3], Orders: [(101,1)]", "expected": "Delete customers 2 and 3"}
            ],
            hidden_testcases=[
                {"input": "Customers: [1], Orders: [(101,1),(102,1)]", "expected": "Delete none"}
            ],
        ),
        _sql_question(
            "sql-058",
            "Find the Nth highest salary using a correlated subquery.",
            "SELECT DISTINCT salary FROM Employees e1 WHERE N-1 = (SELECT COUNT(DISTINCT salary) FROM Employees e2 WHERE e2.salary > e1.salary);",
            "hard", "correlated_subquery",
            [
                "SELECT salary FROM Employees ORDER BY salary DESC LIMIT N-1,1;",
                "SELECT DISTINCT salary FROM Employees e1 WHERE N-1 = (SELECT COUNT(DISTINCT salary) FROM Employees e2 WHERE e2.salary > e1.salary);",
                "SELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);",
                "SELECT salary FROM Employees GROUP BY salary HAVING COUNT(*) >= N;",
            ],
            1,
            "Correlated subquery counts how many distinct salaries are higher than each row.",
            ["DISTINCT removes duplicate salaries", "N-1 must match exactly higher salaries"],
            companies=["tcs", "infosys", "wipro", "cognizant", "accenture"],
            role=["student", "sde", "data-analyst"],
            testcases=[
                {"input": "Employees: [(1,'A',90000),(2,'B',80000),(3,'C',70000),(4,'D',80000)], N=2", "expected": "80000"}
            ],
            hidden_testcases=[
                {"input": "Employees: [(1,'A',50000)], N=1", "expected": "50000"},
                {"input": "Employees: [(1,'A',60000),(2,'B',60000)], N=2", "expected": "60000"}
            ],
        ),
        _sql_question(
            "sql-059",
            "Pivot monthly sales totals from a Sales table with columns (sale_id, amount, sale_date).",
            "SELECT MONTH(sale_date) AS month, SUM(amount) AS total_sales FROM Sales GROUP BY MONTH(sale_date) ORDER BY month;",
            "medium", "date_filtering",
            [
                "SELECT SUM(amount) FROM Sales;",
                "SELECT MONTH(sale_date), SUM(amount) FROM Sales GROUP BY MONTH(sale_date);",
                "SELECT sale_date, amount FROM Sales PIVOT SUM(amount);",
                "SELECT * FROM Sales WHERE MONTH(sale_date) = SUM(amount);",
            ],
            1,
            "GROUP BY extracted month and SUM amounts.",
            ["MONTH() extracts month number", "GROUP BY on expression works in most SQL dialects"],
            companies=["tcs", "infosys", "wipro"],
            role=["student", "sde", "data-analyst"],
            testcases=[
                {"input": "Sales: [(1,100,'2024-01-05'),(2,200,'2024-01-20'),(3,150,'2024-02-10')]", "expected": "Jan=300, Feb=150"}
            ],
            hidden_testcases=[
                {"input": "Sales: [(1,50,'2024-03-01')]", "expected": "Mar=50"}
            ],
        ),
        _sql_question(
            "sql-060",
            "Find customers who have placed more than 3 orders in the last 30 days.",
            "SELECT customer_id, COUNT(*) AS order_count FROM Orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) GROUP BY customer_id HAVING COUNT(*) > 3;",
            "medium", "group_by_having",
            [
                "SELECT customer_id FROM Orders WHERE order_date >= NOW() - 30;",
                "SELECT customer_id, COUNT(*) FROM Orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) GROUP BY customer_id HAVING COUNT(*) > 3;",
                "SELECT * FROM Orders HAVING COUNT(*) > 3;",
                "SELECT customer_id FROM Orders GROUP BY customer_id WHERE COUNT(*) > 3;",
            ],
            1,
            "Filter recent orders with WHERE date >= today - 30, then GROUP BY + HAVING.",
            ["Date math depends on SQL dialect", "HAVING filters after aggregation"],
            companies=["tcs", "infosys", "wipro", "cognizant"],
            role=["student", "sde", "data-analyst"],
            testcases=[
                {"input": "Orders with 4 orders for customer 1 in last 30 days, 1 order for customer 2", "expected": "customer 1 only"}
            ],
            hidden_testcases=[
                {"input": "Orders: 3 orders for customer 1, 4 orders for customer 2", "expected": "customer 2 only"}
            ],
        ),
    ]

    added = 0
    for q in new_questions:
        if q["id"] not in existing_ids:
            existing.append(q)
            existing_ids.add(q["id"])
            added += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"sql_practice_bank.json: added {added} new questions")
    return added


def expand_interview_practice_bank():
    """Add interview questions to interview_practice_bank.json."""
    path = os.path.join(DATA_DIR, "interview_practice_bank.json")
    with open(path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {q.get("id") for q in existing}
    new_questions = [
        _interview_question(
            "int-101",
            "Explain the difference between a process and a thread.",
            "technical",
            "os",
            "easy",
            "A process is an independent execution environment with its own memory space. A thread is the smallest unit of execution within a process; threads share the same memory but have separate stacks. Context switching between threads is faster than between processes.",
            companies=["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
            role=["sde", "backend-engineer"],
            explanation="Process: isolated memory, heavier. Thread: shared memory, lighter. Use threads for concurrent tasks within same app; use processes for isolation.",
            hints=["Memory isolation is the key distinction", "Threads share heap, processes do not"],
            testcases=[
                {"input": "Candidate says thread has separate memory space", "expected": "Incorrect - threads share memory"}
            ],
            hidden_testcases=[
                {"input": "Candidate mentions context-switch cost difference", "expected": "Stronger answer"}
            ],
        ),
        _interview_question(
            "int-102",
            "What is normalization in databases? Explain 1NF, 2NF, and 3NF.",
            "technical",
            "dbms",
            "medium",
            "Normalization removes redundancy. 1NF: atomic values, no repeating groups. 2NF: 1NF plus no partial dependencies on composite keys. 3NF: 2NF plus no transitive dependencies; non-key columns depend only on the primary key.",
            companies=["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon"],
            role=["sde", "data-analyst"],
            explanation="Normal forms reduce redundancy and update anomalies. Most OLTP systems use 3NF. Denormalization is used for read-heavy reporting.",
            hints=["1NF = atomic columns", "2NF = no partial dependency", "3NF = no transitive dependency"],
            testcases=[
                {"input": "Candidate confuses 2NF and 3NF", "expected": "Needs clarity on partial vs transitive dependency"}
            ],
            hidden_testcases=[
                {"input": "Candidate gives example table with partial dependency", "expected": "Shows concrete understanding"}
            ],
        ),
        _interview_question(
            "int-103",
            "Explain TCP vs UDP.",
            "technical",
            "networking",
            "easy",
            "TCP is connection-oriented, reliable, ordered, congestion-controlled, and slower. UDP is connectionless, unreliable, unordered, faster, and used for streaming/DNS. TCP uses handshakes; UDP does not.",
            companies=["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
            role=["sde", "backend-engineer"],
            explanation="Choose TCP when correctness matters; choose UDP when latency matters and some loss is acceptable.",
            hints=["TCP guarantees delivery", "UDP is fire-and-forget"],
            testcases=[
                {"input": "Candidate says UDP is always faster", "expected": "Context-dependent; TCP can be faster on lossy networks due to retries"}
            ],
            hidden_testcases=[
                {"input": "Candidate mentions QUIC/HTTP3", "expected": "Shows updated knowledge"}
            ],
        ),
        _interview_question(
            "int-104",
            "Describe the CAP theorem.",
            "technical",
            "system-design",
            "medium",
            "In distributed systems, you can only have 2 of 3: Consistency (all nodes see same data), Availability (every request gets a response), Partition tolerance (system works despite network partitions). Since partitions are inevitable, real systems choose CP or AP.",
            companies=["amazon", "google", "microsoft", "meta"],
            role=["sde", "backend-engineer", "system-design"],
            explanation="CAP is about trade-offs during partitions. Without partitions, all three are possible. Most systems choose CP or AP based on requirements.",
            hints=["P is non-negotiable in distributed systems", "Examples: CP = banking, AP = social media feeds"],
            testcases=[
                {"input": "Candidate says you can have all three always", "expected": "Incorrect - partitions make it impossible"}
            ],
            hidden_testcases=[
                {"input": "Candidate mentions PACELC", "expected": "Shows deeper distributed systems knowledge"}
            ],
        ),
        _interview_question(
            "int-105",
            "Tell me about a time you handled a production outage.",
            "behavioral",
            "incident-response",
            "medium",
            "STAR method: Situation - production outage affecting users. Task - I was on-call/leading response. Action - identified root cause, implemented fix, communicated status. Result - resolved in X minutes, implemented preventive measures, postmortem documented.",
            companies=["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
            role=["sde", "backend-engineer"],
            explanation="Show ownership, calm under pressure, technical debugging, communication, and learning/improvement.",
            hints=["Use STAR structure", "Quantify impact and resolution time", "Show what you changed to prevent recurrence"],
            testcases=[
                {"input": "Candidate blames others", "expected": "Red flag - take ownership"}
            ],
            hidden_testcases=[
                {"input": "Candidate mentions blameless postmortem", "expected": "Shows maturity"}
            ],
        ),
    ]

    added = 0
    for q in new_questions:
        if q["id"] not in existing_ids:
            existing.append(q)
            existing_ids.add(q["id"])
            added += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"interview_practice_bank.json: added {added} new questions")
    return added


def expand_india_placement_depth():
    """Add aptitude/logical/verbal questions to india_placement_depth.json."""
    path = os.path.join(DATA_DIR, "india_placement_depth.json")
    with open(path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {q.get("id") for q in existing}
    new_questions = [
        _aptitude_question(
            "ind-apt-ratio-1",
            "The ratio of boys to girls in a class is 3:2. If there are 30 boys, how many girls are there?",
            "aptitude",
            "ratio",
            "easy",
            ["18", "20", "15", "25"],
            1,
            "Boys:Girls = 3:2. If 3 parts = 30, then 1 part = 10, so girls = 2*10 = 20.",
            ["Set up proportion: 3/2 = 30/x", "Cross multiply"],
            companies=["tcs", "infosys", "wipro", "accenture", "cognizant"],
            role=["student", "sde"],
            testcases=[
                {"input": "30 boys, ratio 3:2", "expected": 20}
            ],
            hidden_testcases=[
                {"input": "45 boys, ratio 3:2", "expected": 30}
            ],
        ),
        _aptitude_question(
            "ind-apt-profit-1",
            "A shopkeeper buys an article for ₹500 and sells it for ₹600. What is the profit percentage?",
            "aptitude",
            "profit-loss",
            "easy",
            ["20%", "16.67%", "25%", "10%"],
            0,
            "Profit = 600-500 = 100. Profit% = (100/500)*100 = 20%.",
            ["Profit = SP - CP", "Profit% = Profit/CP * 100"],
            companies=["tcs", "infosys", "wipro", "accenture", "cognizant"],
            role=["student", "sde"],
            testcases=[
                {"input": "CP=500, SP=600", "expected": "20%"}
            ],
            hidden_testcases=[
                {"input": "CP=400, SP=500", "expected": "25%"}
            ],
        ),
        _aptitude_question(
            "ind-log-series-1",
            "Find the next number in the series: 2, 5, 10, 17, 26, ?",
            "logical",
            "series",
            "easy",
            ["37", "35", "39", "36"],
            0,
            "Differences: 3, 5, 7, 9... Next difference = 11. 26 + 11 = 37. Pattern: n^2 + 1.",
            ["Look at differences between consecutive terms", "Differences form odd numbers: 3,5,7,9..."],
            companies=["tcs", "infosys", "wipro", "cognizant"],
            role=["student", "sde"],
            testcases=[
                {"input": "2,5,10,17,26", "expected": 37}
            ],
            hidden_testcases=[
                {"input": "1,4,9,16,25", "expected": 36}
            ],
        ),
        _aptitude_question(
            "ind-log-odd-1",
            "Find the odd one out: 3, 5, 7, 9, 11, 13",
            "logical",
            "odd-one-out",
            "easy",
            ["9", "3", "5", "7"],
            0,
            "9 is the only composite number; all others are prime.",
            ["Check primality", "9 = 3*3"],
            companies=["tcs", "infosys", "wipro", "cognizant"],
            role=["student", "sde"],
            testcases=[
                {"input": "3,5,7,9,11,13", "expected": "9"}
            ],
            hidden_testcases=[
                {"input": "2,4,6,8,10,12", "expected": "All even, no odd one"}
            ],
        ),
        _aptitude_question(
            "ind-verb-syn-1",
            "Choose the synonym of 'EPHEMERAL'.",
            "verbal",
            "synonym",
            "medium",
            ["Transient", "Permanent", "Heavy", "Rigid"],
            0,
            "Ephemeral means lasting for a very short time. Synonym: transient.",
            ["Prefix 'epi-' often means upon/brief", "Root 'hemer' relates to day"],
            companies=["tcs", "infosys", "wipro", "accenture"],
            role=["student", "sde"],
            testcases=[
                {"input": "EPHEMERAL", "expected": "Transient"}
            ],
            hidden_testcases=[
                {"input": "EVANESCENT", "expected": "Transient/Fleeting"}
            ],
        ),
        _aptitude_question(
            "ind-verb-ant-1",
            "Choose the antonym of 'BENEVOLENT'.",
            "verbal",
            "antonym",
            "medium",
            ["Malevolent", "Kind", "Generous", "Helpful"],
            0,
            "Benevolent means well-meaning. Antonym: malevolent.",
            ["Prefix 'bene-' means good", "Prefix 'male-' means bad/ill"],
            companies=["tcs", "infosys", "wipro", "accenture"],
            role=["student", "sde"],
            testcases=[
                {"input": "BENEVOLENT", "expected": "Malevolent"}
            ],
            hidden_testcases=[
                {"input": "BENIGN", "expected": "Malignant/Hostile"}
            ],
        ),
    ]

    added = 0
    for q in new_questions:
        if q["id"] not in existing_ids:
            existing.append(q)
            existing_ids.add(q["id"])
            added += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"india_placement_depth.json: added {added} new questions")
    return added


if __name__ == "__main__":
    total = 0
    total += expand_verified_placement_questions()
    total += expand_sql_practice_bank()
    total += expand_interview_practice_bank()
    total += expand_india_placement_depth()
    print(f"\nTotal new questions added: {total}")
    print("Next step: run auto_verify.py to set trust_status on new questions.")
