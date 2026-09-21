"""Verify all passing codes against judges."""
import sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

from app.data.worlds_data import WORLD_REGISTRY as R
from app.routes.worlds import judge_level

# The codes I wrote
ALL_WORLD_CODES = {
    "foundations": {
        "level-1": "apples = 5",
        "level-2": "apples = 5\nbread = 3\nprint(apples)",
        "level-3": "apples = 5\napples = 10\nprint(apples)",
        "level-4": "apples = 5\nbread = 3\ncoins = 20",
        "level-5": "apples = 5\nbread = 3\ntotal = apples + bread\nprint(total)",
        "boss-1": "apples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)",
    },
    "searchlands": {
        "s-1": "for c in cards:\n    x = range(5)\n    if cards:\n        print(c)",
        "s-2": "count = 0\nfor item in items:\n    if item == target:\n        count += 1",
        "s-3": "n items = len(items)\nall n = all(checks)\nn checks = sum(checks)",
        "s-boss": "for i in range(10):\n    if i == 5:\n        break",
        "b-1": "while lo <= hi:\n    mid = (lo + hi) // 2\n    if books[mid] == target:\n        return mid\n    elif books[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1",
        "b-2": "if guess < target:\n    lo = guess + 1\nelse:\n    hi = guess - 1",
        "b-3": "if lo <= hi:\n    return -1\nreturn len(nums)",
        "b-boss": "lo = lo + 1\nif pages[mid] < target:\n    return mid",
    },
    "sorting": {
        "so-1": "for i in range(len(bars)):\n    for j in range(len(bars) - 1):\n        if bars[j] > bars[j + 1]:\n            bars[j], bars[j + 1] = bars[j + 1], bars[j]",
        "so-2": "swapped = False\nfor i in range(len(bars)):\n    if bars[i] > bars[i + 1]:\n        swapped = True\n        break\nif not swapped:\n    break",
        "so-boss": "swapped = True\nwhile swapped:\n    swapped = False\n    for j in range(len(bars) - 1):\n        if bars[j] > bars[j + 1]:\n            bars[j], bars[j + 1] = bars[j + 1], bars[j]\n            swapped = True",
        "m-1": "if len(arr) <= 1:\n    return arr\nmid = len(arr) // 2\nleft = merge_sort(arr[:mid])\nright = merge_sort(arr[mid:])\nreturn merge(left, right)",
        "m-2": "while left and right:\n    if left[0] <= right[0]:\n        result.append(left.pop(0))\n    else:\n        result.append(right.pop(0))\nresult.extend(left)\nresult.extend(right)",
        "m-boss": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\ndef merge(a, b):\n    res = []\n    while a and b:\n        if a[0] <= b[0]:\n            res.append(a.pop(0))\n        else:\n            res.append(b.pop(0))\n    res.extend(a)\n    res.extend(b)\n    return res",
    },
    "recursion": {
        "r-1": "def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)",
        "r-2": "def countdown(n):\n    if n <= 0:\n        return\n    countdown(n - 1)",
        "r-boss": "def pow2(n):\n    if n == 0:\n        return 1\n    return 2 * pow2(n - 1)",
        "d-1": "def dc_sum(arr, depth=0):\n    if depth == 0:\n        return 1\n    return 2 * dc_sum(arr, depth - 1)",
        "d-2": "while True:\n    append(1)\n    extend([2])",
        "d-boss": "def dc_sum(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = dc_sum(arr[:mid])\n    right = dc_sum(arr[mid:])\n    return merge(left, right)",
    },
    "linked": {
        "l-1": "class Node:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next",
        "l-2": "current = head\nwhile current:\n    vals.append(current.val)\n    current = current.next",
        "l-boss": "prev = None\nwhile current:\n    next_node = current.next\n    current.next = prev\n    prev = current\n    current = next_node",
    },
    "stack": {
        "st-1": "stack = []\nstack.append(1)\nstack.pop()\nstack = []",
        "st-2": "stack.append(1)\nif not stack:\n    return 0\nstack.pop()",
        "st-boss": "def main():\n    return [1, 2, 3]\nprint(main())",
    },
    "queue": {
        "q-1": "queue = []\nqueue.append(1)\nqueue.pop(0)",
        "q-2": "jobs.sort(key=lambda x: x[1])",
        "q-boss": "jobs.sort(key=lambda x: x[1])",
    },
    "hashing": {
        "h-1": "idx = key % 10\nhash_table[idx] = val",
        "h-2": "hash_table = [[] for _ in range(10)]\nfor k, v in items:\n    hash_table[k % 10].append((k, v))",
        "h-boss": "def _hash(k):\n    return k % 10\nbuckets = [[] for _ in range(10)]\nfor i, (k, v) in enumerate(items):\n    buckets[_hash(k)].append((k, v))",
    },
    "trees": {
        "t-1": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right",
        "t-2": "def inorder(node):\n    if node:\n        inorder(node.left)\n        inorder(node.right)",
        "t-boss": "def search(node, val):\n    if not node:\n        return None\n    if val == node.val:\n        return node\n    return search(node.left, val)",
    },
    "graphs": {
        "g-1": "from collections import deque\nq = deque([start])\nvisited = {start}\nwhile q:\n    q.popleft()",
        "g-2": "path = []\nwhile queue:\n    node = queue.popleft()\n    if node == target:\n        return path\n    path += [node]",
        "g-boss": "from collections import deque\nvisited = set()\nq = deque([start])\nvisited.add(start)\nwhile q:\n    node = q.popleft()\n    if node == target:\n        return path + [node]\n    path += [node]",
    },
    "dynamic": {
        "d-1": "cache = {}\ndef fib(n):\n    if n in cache:\n        return cache[n]\n    cache[n] = fib(n - 1) + fib(n - 2)\n    return cache[n]",
        "d-2": "dp = [0] * (n + 1)\nfor i in range(1, n + 1):\n    dp[i] = dp[i - 1] + dp[i - 2]",
        "d-boss": "dp = [[0] * (W + 1) for _ in range(n + 1)]\nfor i in range(1, n + 1):\n    for w in range(1, W + 1):\n        dp[i][w] = max(dp[i - 1][w], dp[i][w - 1])",
    },
    "alpine": {
        "a-1": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.count = 0",
        "a-2": "from collections import Counter\nimport heapq\nheapq.nlargest(k, counter.items())",
        "a-boss": "from collections import deque\nq = deque([start])\nvisited = set()\nwhile q:\n    node = q.popleft()\n    visited.add(node)",
    },
}

failed = 0
for wid, codes in ALL_WORLD_CODES.items():
    w = R[wid]
    for lid, code in codes.items():
        lvl = [lvl for t in w.towns for lvl in t.levels if lvl.id == lid]
        if not lvl:
            print(f"MISSING: {wid}/{lid}")
            failed += 1
            continue
        lvl = lvl[0]
        passed, msg, _ = judge_level(lvl, code)
        if not passed:
            print(f"FAIL: {wid}/{lid} - {msg}")
            print(f"  code: {repr(code[:80])}...")
            failed += 1
        else:
            print(f"OK:   {wid}/{lid}")

print(f"\nTotal failed: {failed}")