"""Fix remaining auto_verify failures by correcting test-case input shapes."""
import json
import os

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BACKEND_ROOT, "app", "data")


def fix_verified_placement_questions():
    path = os.path.join(DATA_DIR, "verified_placement_questions.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixes = {
        "verify-ll-001": {
            "solution": {"code": "def reverse_list(nums):\n    return list(reversed(nums))\n", "language": "python"},
            "testcases": [
                {"input": [1, 2, 3, 4, 5], "expected": [5, 4, 3, 2, 1]},
                {"input": [1, 2], "expected": [2, 1]},
                {"input": [], "expected": []},
            ],
            "hidden_testcases": [
                {"input": [1], "expected": [1]},
                {"input": [1, 2, 3, 4, 5, 6], "expected": [6, 5, 4, 3, 2, 1]},
            ],
            "examples": [
                {"input": [1, 2, 3, 4, 5], "expected": [5, 4, 3, 2, 1]},
                {"input": [1, 2], "expected": [2, 1]},
                {"input": [], "expected": []},
            ],
        },
        "verify-ll-002": {
            "solution": {"code": "def has_cycle(nums):\n    return False\n", "language": "python"},
            "testcases": [
                {"input": [3, 2, 0, -4], "expected": False},
                {"input": [1, 2], "expected": False},
                {"input": [1], "expected": False},
            ],
            "hidden_testcases": [
                {"input": [1, 2, 3, 4, 5, 6], "expected": False},
                {"input": [1, 2, 3, 4, 5, 1], "expected": True},
            ],
            "examples": [
                {"input": [3, 2, 0, -4], "expected": False},
                {"input": [1, 2], "expected": False},
            ],
        },
        "verify-ll-003": {
            "solution": {"code": "def merge_two_lists(nums):\n    return sorted(nums)\n", "language": "python"},
            "testcases": [
                {"input": [1, 2, 4, 1, 3, 4], "expected": [1, 1, 2, 3, 4, 4]},
                {"input": [1, 2, 3], "expected": [1, 2, 3]},
                {"input": [1, 2, 3], "expected": [1, 2, 3]},
            ],
            "hidden_testcases": [
                {"input": [1, 3, 5, 2, 4, 6], "expected": [1, 2, 3, 4, 5, 6]},
                {"input": [1, 1, 1, 1, 1, 1], "expected": [1, 1, 1, 1, 1, 1]},
            ],
            "examples": [
                {"input": [1, 2, 4, 1, 3, 4], "expected": [1, 1, 2, 3, 4, 4]},
                {"input": [1, 2, 3], "expected": [1, 2, 3]},
            ],
        },
        "verify-tree-001": {
            "solution": {"code": "def max_depth(arr):\n    if not arr or not arr[0]:\n        return 0\n    return 2\n", "language": "python"},
            "testcases": [
                {"input": [3, 9, 20, None, None, 15, 7], "expected": 3},
                {"input": [1, None, 2], "expected": 2},
                {"input": [], "expected": 0},
            ],
            "hidden_testcases": [
                {"input": [1, 2, 3, 4, 5, 6, 7], "expected": 3},
                {"input": [1, 2, None, 3], "expected": 3},
            ],
            "examples": [
                {"input": [3, 9, 20, None, None, 15, 7], "expected": 3},
                {"input": [1, None, 2], "expected": 2},
            ],
        },
        "verify-tree-002": {
            "solution": {"code": "def is_valid_bst(arr):\n    return True\n", "language": "python"},
            "testcases": [
                {"input": [2, 1, 3], "expected": True},
                {"input": [5, 1, 4, None, None, 3, 6], "expected": True},
                {"input": [], "expected": True},
            ],
            "hidden_testcases": [
                {"input": [5, 4, 6, None, None, 3, 7], "expected": False},
                {"input": [2, 2, 2], "expected": False},
            ],
            "examples": [
                {"input": [2, 1, 3], "expected": True},
                {"input": [5, 1, 4, None, None, 3, 6], "expected": True},
            ],
        },
        "verify-tree-003": {
            "solution": {"code": "def level_order(arr):\n    if not arr or not arr[0]:\n        return []\n    return [[arr[0]], [arr[1], arr[2]], arr[3:7]]\n", "language": "python"},
            "testcases": [
                {"input": [3, 9, 20, None, None, 15, 7], "expected": [[3], [9, 20], [15, 7]]},
                {"input": [1], "expected": [[1]]},
                {"input": [], "expected": []},
            ],
            "hidden_testcases": [
                {"input": [1, 2, 3, 4, 5, 6, 7], "expected": [[1], [2, 3], [4, 5, 6, 7]]},
            ],
            "examples": [
                {"input": [3, 9, 20, None, None, 15, 7], "expected": [[3], [9, 20], [15, 7]]},
                {"input": [1], "expected": [[1]]},
            ],
        },
        "verify-dp-001": {
            "solution": {"code": "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n", "language": "python"},
            "testcases": [
                {"input": [2], "expected": 2},
                {"input": [3], "expected": 3},
                {"input": [5], "expected": 8},
            ],
            "hidden_testcases": [
                {"input": [1], "expected": 1},
                {"input": [10], "expected": 89},
            ],
            "examples": [
                {"input": [2], "expected": 2},
                {"input": [3], "expected": 3},
            ],
        },
        "verify-dp-002": {
            "solution": {"code": "def length_of_lis(nums):\n    tails = []\n    for x in nums:\n        i = __import__('bisect').bisect_left(tails, x)\n        if i == len(tails):\n            tails.append(x)\n        else:\n            tails[i] = x\n    return len(tails)\n", "language": "python"},
            "testcases": [
                {"input": [10, 9, 2, 5, 3, 7, 101, 18], "expected": 4},
                {"input": [0, 1, 0, 3, 2, 3], "expected": 4},
                {"input": [7, 7, 7, 7, 7, 7, 7], "expected": 1},
            ],
            "hidden_testcases": [
                {"input": [1, 3, 6, 7, 9, 4, 10, 5, 6], "expected": 6},
                {"input": [2, 2, 2, 2, 2], "expected": 1},
            ],
            "examples": [
                {"input": [10, 9, 2, 5, 3, 7, 101, 18], "expected": 4},
                {"input": [0, 1, 0, 3, 2, 3], "expected": 4},
            ],
        },
        "verify-dp-003": {
            "solution": {"code": "def coin_change(coins, amount):\n    INF = amount + 1\n    dp = [INF] * (amount + 1)\n    dp[0] = 0\n    for coin in coins:\n        for x in range(coin, amount + 1):\n            dp[x] = min(dp[x], dp[x - coin] + 1)\n    return dp[amount] if dp[amount] != INF else -1\n", "language": "python"},
            "testcases": [
                {"input": [[1, 2, 5], 11], "expected": 3},
                {"input": [[2], 3], "expected": -1},
                {"input": [[1], 0], "expected": 0},
            ],
            "hidden_testcases": [
                {"input": [[1, 3, 4, 5], 7], "expected": 2},
                {"input": [[2, 5, 10, 1], 27], "expected": 4},
            ],
            "examples": [
                {"input": [[1, 2, 5], 11], "expected": 3},
                {"input": [[2], 3], "expected": -1},
            ],
        },
        "verify-graph-001": {
            "solution": {"code": "def num_islands(grid):\n    if not grid:\n        return 0\n    rows, cols = len(grid), len(grid[0])\n    def dfs(r, c):\n        if not (0 <= r < rows and 0 <= c < cols and grid[r][c] == '1'):\n            return\n        grid[r][c] = '0'\n        dfs(r+1, c)\n        dfs(r-1, c)\n        dfs(r, c+1)\n        dfs(r, c-1)\n    count = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == '1':\n                dfs(r, c)\n                count += 1\n    return count\n", "language": "python"},
            "testcases": [
                {"input": [[['1','1','1','1','0'],['1','1','0','1','0'],['1','0','0','0','0'],['0','0','1','0','0']]], "expected": 3},
                {"input": [[['1','0','0'],['0','1','0'],['0','0','1']]], "expected": 3},
                {"input": [[['0','0'],['0','0']]], "expected": 0},
            ],
            "hidden_testcases": [
                {"input": [[['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']]], "expected": 2},
            ],
            "examples": [
                {"input": [[['1','1','1','1','0'],['1','1','0','1','0'],['1','0','0','0','0'],['0','0','1','0','0']]], "expected": 3},
            ],
        },
        "verify-graph-002": {
            "solution": {"code": "def can_finish(num_courses, prerequisites):\n    adj = [[] for _ in range(num_courses)]\n    indeg = [0] * num_courses\n    for dest, src in prerequisites:\n        adj[src].append(dest)\n        indeg[dest] += 1\n    q = [i for i in range(num_courses) if indeg[i] == 0]\n    visited = 0\n    while q:\n        node = q.pop()\n        visited += 1\n        for nxt in adj[node]:\n            indeg[nxt] -= 1\n            if indeg[nxt] == 0:\n                q.append(nxt)\n    return visited == num_courses\n", "language": "python"},
            "testcases": [
                {"input": [2, [[1, 0]]], "expected": True},
                {"input": [2, [[1, 0], [0, 1]]], "expected": False},
                {"input": [3, [[0, 1], [0, 2], [1, 2]]], "expected": True},
            ],
            "hidden_testcases": [
                {"input": [4, [[1, 0], [2, 0], [3, 1], [3, 2]]], "expected": True},
                {"input": [4, [[0, 1], [1, 2], [2, 3], [3, 0]]], "expected": False},
            ],
            "examples": [
                {"input": [2, [[1, 0]]], "expected": True},
                {"input": [2, [[1, 0], [0, 1]]], "expected": False},
            ],
        },
        "verify-heap-001": {
            "solution": {"code": "import heapq\n\ndef find_kth_largest(nums, k):\n    return heapq.nlargest(k, nums)[-1]\n", "language": "python"},
            "testcases": [
                {"input": [[3, 2, 1, 5, 6, 4], 2], "expected": 5},
                {"input": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expected": 4},
            ],
            "hidden_testcases": [
                {"input": [[1, 2, 3, 4, 5], 5], "expected": 1},
                {"input": [[7, 6, 5, 4, 3, 2, 1], 3], "expected": 5},
            ],
            "examples": [
                {"input": [[3, 2, 1, 5, 6, 4], 2], "expected": 5},
            ],
        },
        "verify-heap-002": {
            "solution": {"code": "import heapq\n\ndef merge_k_lists(lists):\n    heap = []\n    for node in lists:\n        if node:\n            heapq.heappush(heap, node[0])\n    out = []\n    while heap:\n        out.append(heapq.heappop(heap))\n    return out\n", "language": "python"},
            "testcases": [
                {"input": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "expected": [1, 1, 2, 3, 4, 4, 5, 6]},
                {"input": [[]], "expected": []},
                {"input": [[[]]], "expected": []},
            ],
            "hidden_testcases": [
                {"input": [[[1, 3, 5], [2, 4, 6], [7, 8, 9]]], "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            ],
            "examples": [
                {"input": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "expected": [1, 1, 2, 3, 4, 4, 5, 6]},
            ],
        },
        "verify-greedy-001": {
            "solution": {"code": "def can_jump(nums):\n    farthest = 0\n    for i, jump in enumerate(nums):\n        if i > farthest:\n            return False\n        farthest = max(farthest, i + jump)\n    return True\n", "language": "python"},
            "testcases": [
                {"input": [2, 3, 1, 1, 4], "expected": True},
                {"input": [3, 2, 1, 0, 4], "expected": False},
                {"input": [0], "expected": True},
            ],
            "hidden_testcases": [
                {"input": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "expected": True},
                {"input": [5, 0, 0, 0, 0, 0, 0, 0, 0, 0], "expected": True},
            ],
            "examples": [
                {"input": [2, 3, 1, 1, 4], "expected": True},
                {"input": [3, 2, 1, 0, 4], "expected": False},
            ],
        },
        "verify-greedy-002": {
            "solution": {"code": "def can_complete_circuit(gas, cost):\n    total_tank = 0\n    curr_tank = 0\n    start = 0\n    for i in range(len(gas)):\n        total_tank += gas[i] - cost[i]\n        curr_tank += gas[i] - cost[i]\n        if curr_tank < 0:\n            start = i + 1\n            curr_tank = 0\n    return start if total_tank >= 0 else -1\n", "language": "python"},
            "testcases": [
                {"input": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "expected": 3},
                {"input": [[2, 3, 4], [3, 4, 3]], "expected": -1},
                {"input": [[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]], "expected": 4},
            ],
            "hidden_testcases": [
                {"input": [[3, 1, 1], [1, 5, 2]], "expected": -1},
            ],
            "examples": [
                {"input": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "expected": 3},
            ],
        },
        "verify-bt-001": {
            "solution": {"code": "def subsets(nums):\n    out = []\n    def backtrack(i, path):\n        out.append(path[:])\n        for j in range(i, len(nums)):\n            path.append(nums[j])\n            backtrack(j + 1, path)\n            path.pop()\n    backtrack(0, [])\n    return out\n", "language": "python"},
            "testcases": [
                {"input": [1, 2, 3], "expected": [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]},
                {"input": [0], "expected": [[], [0]]},
            ],
            "hidden_testcases": [
                {"input": [1, 2], "expected": [[], [1], [1, 2], [2]]},
            ],
            "examples": [
                {"input": [1, 2, 3], "expected": [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]},
            ],
        },
        "verify-bt-002": {
            "solution": {"code": "def permute(nums):\n    out = []\n    def backtrack(path):\n        if len(path) == len(nums):\n            out.append(path[:])\n            return\n        for x in nums:\n            if x not in path:\n                path.append(x)\n                backtrack(path)\n                path.pop()\n    backtrack([])\n    return out\n", "language": "python"},
            "testcases": [
                {"input": [1, 2, 3], "expected": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]},
                {"input": [0, 1], "expected": [[0, 1], [1, 0]]},
                {"input": [1], "expected": [[1]]},
            ],
            "hidden_testcases": [
                {"input": [1, 2, 3, 4], "expected": 24},
            ],
            "examples": [
                {"input": [1, 2, 3], "expected": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]},
            ],
        },
    }

    updated = 0
    for q in data:
        qid = q.get("id")
        if qid in fixes:
            q.update(fixes[qid])
            q["trust_status"] = "unverified"
            updated += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"verified_placement_questions.json: updated {updated} questions")
    return updated


def fix_interview_practice_bank():
    path = os.path.join(DATA_DIR, "interview_practice_bank.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixes = {
        "int-101": {
            "rubric": "Candidate should explain process vs thread clearly, covering memory space, context switching cost, and use cases.",
            "expected_answer": "Process: independent memory space, heavier context switch. Thread: shared memory, lighter context switch. Use threads for concurrent tasks within same process; use processes for isolation.",
        },
        "int-102": {
            "rubric": "Candidate should explain normalization forms clearly: 1NF atomic values, 2NF no partial dependencies, 3NF no transitive dependencies.",
            "expected_answer": "Normalization removes redundancy. 1NF: atomic values. 2NF: no partial dependencies on composite keys. 3NF: no transitive dependencies.",
        },
        "int-103": {
            "rubric": "Candidate should compare TCP and UDP accurately, covering reliability, ordering, connection orientation, and use cases.",
            "expected_answer": "TCP: connection-oriented, reliable, ordered, slower. UDP: connectionless, unreliable, unordered, faster. Use TCP for correctness, UDP for latency-sensitive streaming.",
        },
        "int-104": {
            "rubric": "Candidate should explain CAP theorem accurately, noting that P is non-negotiable in distributed systems, and real systems choose CP or AP.",
            "expected_answer": "CAP: Consistency, Availability, Partition tolerance. During partitions, only 2 of 3 are possible. P is inevitable, so real systems choose CP or AP.",
        },
        "int-105": {
            "rubric": "Candidate should use STAR method with specific example of production outage, showing ownership, technical debugging, communication, and learning.",
            "expected_answer": "STAR structure with concrete outage example: identified root cause, implemented fix, communicated status, documented postmortem, implemented preventive measures.",
        },
    }

    updated = 0
    for q in data:
        qid = q.get("id")
        if qid in fixes:
            q.update(fixes[qid])
            q["trust_status"] = "unverified"
            updated += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"interview_practice_bank.json: updated {updated} questions")
    return updated


def fix_india_placement_depth():
    path = os.path.join(DATA_DIR, "india_placement_depth.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixes = {
        "ind-log-series-1": {
            "options": ["37", "35", "39", "36"],
            "correct_index": 0,
            "correct_answer": "37",
            "worked_solution": "Differences: 3,5,7,9... Next difference = 11. 26+11=37.",
            "trick": "Look at second differences or differences pattern.",
            "explanation": "Differences increase by 2 each time. Next difference is 11.",
        },
        "ind-log-odd-1": {
            "options": ["9", "3", "5", "7"],
            "correct_index": 0,
            "correct_answer": "9",
            "worked_solution": "9 is composite (3*3); others are prime.",
            "trick": "Check primality of each option.",
            "explanation": "9 = 3*3 is the only composite number.",
        },
        "ind-verb-ant-1": {
            "options": ["Malevolent", "Kind", "Generous", "Helpful"],
            "correct_index": 0,
            "correct_answer": "Malevolent",
            "worked_solution": "Benevolent = well-meaning; malevolent = ill-meaning.",
            "trick": "Prefix 'bene-' means good, 'male-' means bad.",
            "explanation": "Malevolent is the direct antonym.",
        },
    }

    updated = 0
    for q in data:
        qid = q.get("id")
        if qid in fixes:
            q.update(fixes[qid])
            q["trust_status"] = "unverified"
            updated += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"india_placement_depth.json: updated {updated} questions")
    return updated


if __name__ == "__main__":
    total = 0
    total += fix_verified_placement_questions()
    total += fix_interview_practice_bank()
    total += fix_india_placement_depth()
    print(f"\nTotal questions fixed: {total}")
