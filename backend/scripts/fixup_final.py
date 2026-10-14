"""Final fixup: make remaining new questions actually pass auto_verify."""
import json
import os

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BACKEND_ROOT, "app", "data")


def fix_verified_placement_questions():
    path = os.path.join(DATA_DIR, "verified_placement_questions.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixes = {
        "verify-tree-001": {
            "solution": {"code": "def max_depth(arr):\n    if not arr or arr[0] is None:\n        return 0\n    depth = 0\n    i = 0\n    while i < len(arr):\n        depth += 1\n        level_size = 1 << depth\n        i += level_size\n    return depth\n", "language": "python"},
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
        "verify-tree-003": {
            "solution": {"code": "def level_order(arr):\n    if not arr or arr[0] is None:\n        return []\n    out = [[arr[0]]]\n    i = 1\n    n = len(arr)\n    while i < n:\n        level = []\n        for _ in range(len(out[-1]) * 2):\n            if i < n and arr[i] is not None:\n                level.append(arr[i])\n            i += 1\n        if level:\n            out.append(level)\n    return out\n", "language": "python"},
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
        "verify-graph-001": {
            "solution": {"code": "def num_islands(grid):\n    if not grid:\n        return 0\n    rows, cols = len(grid), len(grid[0])\n    def dfs(r, c):\n        if not (0 <= r < rows and 0 <= c < cols and grid[r][c] == '1'):\n            return\n        grid[r][c] = '0'\n        dfs(r+1, c)\n        dfs(r-1, c)\n        dfs(r, c+1)\n        dfs(r, c-1)\n    count = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == '1':\n                dfs(r, c)\n                count += 1\n    return count\n", "language": "python"},
            "testcases": [
                {"input": [['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']], "expected": 3},
                {"input": [['1','0','0'],['0','1','0'],['0','0','1']], "expected": 3},
                {"input": [['0','0'],['0','0']], "expected": 0},
            ],
            "hidden_testcases": [
                {"input": [['1','1','1','1','0'],['1','1','0','1','0'],['1','0','0','0','0'],['0','0','1','0','0']], "expected": 2},
            ],
            "examples": [
                {"input": [['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']], "expected": 3},
            ],
        },
        "verify-heap-002": {
            "solution": {"code": "import heapq\n\ndef merge_k_lists(lists):\n    heap = []\n    for i, node in enumerate(lists):\n        if node:\n            heapq.heappush(heap, (node[0], i, 0))\n    out = []\n    while heap:\n        val, i, j = heapq.heappop(heap)\n        out.append(val)\n        if j + 1 < len(lists[i]):\n            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))\n    return out\n", "language": "python"},
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


if __name__ == "__main__":
    total = 0
    total += fix_verified_placement_questions()
    
    # Also fix MCQ format in india_placement_depth.json
    path = os.path.join(DATA_DIR, "india_placement_depth.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    mcq_fixes = {
        "ind-apt-ratio-1": {
            "options": {"A": "18", "B": "20", "C": "15", "D": "25"},
            "correct_index": 1,
            "correct_answer": "B",
        },
        "ind-apt-profit-1": {
            "options": {"A": "20%", "B": "16.67%", "C": "25%", "D": "10%"},
            "correct_index": 0,
            "correct_answer": "A",
        },
        "ind-log-series-1": {
            "options": {"A": "37", "B": "35", "C": "39", "D": "36"},
            "correct_index": 0,
            "correct_answer": "A",
            "worked_solution": "Differences: 3,5,7,9... Next difference = 11. 26+11=37.",
            "trick": "Look at second differences or differences pattern.",
            "explanation": "Differences increase by 2 each time. Next difference is 11.",
        },
        "ind-log-odd-1": {
            "options": {"A": "9", "B": "3", "C": "5", "D": "7"},
            "correct_index": 0,
            "correct_answer": "A",
            "worked_solution": "9 is composite (3*3); others are prime.",
            "trick": "Check primality of each option.",
            "explanation": "9 = 3*3 is the only composite number.",
        },
        "ind-verb-syn-1": {
            "options": {"A": "Transient", "B": "Permanent", "C": "Heavy", "D": "Rigid"},
            "correct_index": 0,
            "correct_answer": "A",
            "worked_solution": "Ephemeral means lasting for a very short time. Synonym: transient.",
            "trick": "Prefix 'epi-' often means upon/brief",
            "explanation": "Transient is the closest synonym.",
        },
        "ind-verb-ant-1": {
            "options": {"A": "Malevolent", "B": "Kind", "C": "Generous", "D": "Helpful"},
            "correct_index": 0,
            "correct_answer": "A",
            "worked_solution": "Benevolent = well-meaning; malevolent = ill-meaning.",
            "trick": "Prefix 'bene-' means good, 'male-' means bad.",
            "explanation": "Malevolent is the direct antonym.",
        },
    }
    mcq_updated = 0
    for q in data:
        qid = q.get("id")
        if qid in mcq_fixes:
            q.update(mcq_fixes[qid])
            q["trust_status"] = "unverified"
            mcq_updated += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"india_placement_depth.json: updated {mcq_updated} questions")
    total += mcq_updated
    
    print(f"\nTotal questions fixed: {total}")
