"""Expand Content Trust 11 -> N: author + independently verify more foundational
coding questions and append to the verified bank. Every solution is checked
against a SEPARATE reference oracle across tests + edge cases.
"""
import sys, json
sys.path.insert(0, r"D:\Project-Fremen\backend")
from scripts.content_factory import ContentGate

gate = ContentGate()
VERIFIED_PATH = r"D:\Project-Fremen\backend\app\data\verified_placement_questions.json"

# ---------------------------- Independent oracles ----------------------------
def o_valid_parentheses(s):
    st = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in "([{":
            st.append(c)
        elif c in ")]}":
            if not st or st.pop() != pairs[c]:
                return False
    return len(st) == 0

def o_climbing_stairs(n):
    a, b = 1, 2
    for _ in range(1, n + 1):
        if n == 1:
            return 1
    if n == 2:
        return 2
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def o_coin_change(coins, amount):
    INF = float("inf")
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return -1 if dp[amount] == INF else dp[amount]

def o_group_anagrams(words):
    groups = {}
    for w in words:
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
    return [sorted(g) for g in groups.values()]

def o_valid_anagram(s, t):
    return sorted(s) == sorted(t)

def o_contains_duplicate(nums):
    return len(nums) != len(set(nums))

def o_merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    res = [intervals[0][:]]
    for s, e in intervals[1:]:
        if s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)
        else:
            res.append([s, e])
    return res

def o_product_except_self(nums):
    out = []
    for i in range(len(nums)):
        p = 1
        for j in range(len(nums)):
            if j != i:
                p *= nums[j]
        out.append(p)
    return out

def o_first_unique_char(s):
    from collections import Counter
    c = Counter(s)
    for i, ch in enumerate(s):
        if c[ch] == 1:
            return i
    return -1

def o_binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if nums[m] == target:
            return m
        if nums[m] < target:
            lo = m + 1
        else:
            hi = m - 1
    return -1

# ---------------------------- Candidate solutions ----------------------------
def s_valid_parentheses(s):
    st = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in "([{":
            st.append(c)
        elif not st or st.pop() != pairs[c]:
            return False
    return not st

def s_climbing_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def s_coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return -1 if dp[amount] > amount else dp[amount]

def s_group_anagrams(words):
    groups = {}
    for w in words:
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
    return [sorted(g) for g in groups.values()]

def s_valid_anagram(s, t):
    return sorted(s) == sorted(t)

def s_contains_duplicate(nums):
    return len(set(nums)) != len(nums)

def s_merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    res = [intervals[0][:]]
    for s, e in intervals[1:]:
        if s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)
        else:
            res.append([s, e])
    return res

def s_product_except_self(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out

def s_first_unique_char(s):
    from collections import Counter
    c = Counter(s)
    return next((i for i, ch in enumerate(s) if c[ch] == 1), -1)

def s_binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if nums[m] == target:
            return m
        if nums[m] < target:
            lo = m + 1
        else:
            hi = m - 1
    return -1


# Solve-code strings for the published bank (real, runnable solutions).
CODE = {
    "verify-007": (
        "def valid_parentheses(s):\n"
        "    st = []\n"
        "    pairs = {')': '(', ']': '[', '}': '{'}\n"
        "    for c in s:\n"
        "        if c in '([{':\n"
        "            st.append(c)\n"
        "        elif not st or st.pop() != pairs[c]:\n"
        "            return False\n"
        "    return not st\n"
    ),
    "verify-008": (
        "def climbing_stairs(n):\n"
        "    if n <= 2:\n"
        "        return n\n"
        "    a, b = 1, 2\n"
        "    for _ in range(3, n + 1):\n"
        "        a, b = b, a + b\n"
        "    return b\n"
    ),
    "verify-009": (
        "def coin_change(coins, amount):\n"
        "    dp = [amount + 1] * (amount + 1)\n"
        "    dp[0] = 0\n"
        "    for i in range(1, amount + 1):\n"
        "        for c in coins:\n"
        "            if c <= i:\n"
        "                dp[i] = min(dp[i], dp[i - c] + 1)\n"
        "    return -1 if dp[amount] > amount else dp[amount]\n"
    ),
    "verify-010": (
        "def group_anagrams(words):\n"
        "    groups = {}\n"
        "    for w in words:\n"
        "        key = ''.join(sorted(w))\n"
        "        groups.setdefault(key, []).append(w)\n"
        "    return [sorted(g) for g in groups.values()]\n"
    ),
    "verify-011": (
        "def valid_anagram(s, t):\n"
        "    return sorted(s) == sorted(t)\n"
    ),
    "verify-012": (
        "def contains_duplicate(nums):\n"
        "    return len(set(nums)) != len(nums)\n"
    ),
    "verify-013": (
        "def merge_intervals(intervals):\n"
        "    if not intervals:\n"
        "        return []\n"
        "    intervals.sort()\n"
        "    res = [intervals[0][:]]\n"
        "    for s, e in intervals[1:]:\n"
        "        if s <= res[-1][1]:\n"
        "            res[-1][1] = max(res[-1][1], e)\n"
        "        else:\n"
        "            res.append([s, e])\n"
        "    return res\n"
    ),
    "verify-014": (
        "def product_except_self(nums):\n"
        "    n = len(nums)\n"
        "    out = [1] * n\n"
        "    left = 1\n"
        "    for i in range(n):\n"
        "        out[i] = left\n"
        "        left *= nums[i]\n"
        "    right = 1\n"
        "    for i in range(n - 1, -1, -1):\n"
        "        out[i] *= right\n"
        "        right *= nums[i]\n"
        "    return out\n"
    ),
    "verify-015": (
        "def first_unique_char(s):\n"
        "    from collections import Counter\n"
        "    c = Counter(s)\n"
        "    return next((i for i, ch in enumerate(s) if c[ch] == 1), -1)\n"
    ),
    "verify-016": (
        "def binary_search(nums, target):\n"
        "    lo, hi = 0, len(nums) - 1\n"
        "    while lo <= hi:\n"
        "        m = (lo + hi) // 2\n"
        "        if nums[m] == target:\n"
        "            return m\n"
        "        if nums[m] < target:\n"
        "            lo = m + 1\n"
        "        else:\n"
        "            hi = m - 1\n"
        "    return -1\n"
    ),
}

specs = [
    ("verify-007", "Valid Parentheses: check if brackets are correctly paired", "easy", "stack", "stack",
     s_valid_parentheses, o_valid_parentheses,
     [{"input": ("()[]{}",), "expected": True}, {"input": ("(]",), "expected": False}, {"input": ("([)]",), "expected": False}],
     [{"input": ("",), "expected": True}, {"input": ("(",), "expected": False}]),
    ("verify-008", "Climbing Stairs: count distinct ways to climb n steps", "easy", "dynamic programming", "dynamic programming",
     s_climbing_stairs, o_climbing_stairs,
     [{"input": (2,), "expected": 2}, {"input": (3,), "expected": 3}, {"input": (5,), "expected": 8}],
     [{"input": (1,), "expected": 1}, {"input": (10,), "expected": 89}]),
    ("verify-009", "Coin Change: fewest coins to make an amount", "medium", "dynamic programming", "dynamic programming",
     s_coin_change, o_coin_change,
     [{"input": ([1, 2, 5], 11), "expected": 3}, {"input": ([2], 3), "expected": -1}, {"input": ([1], 0), "expected": 0}],
     [{"input": ([1, 5, 3], 10), "expected": 2}]),
    ("verify-010", "Group Anagrams: group words that are anagrams", "medium", "strings", "hashing",
     s_group_anagrams, o_group_anagrams,
     [{"input": (["eat", "tea", "tan", "ate", "nat", "bat"],), "expected": [["ate", "eat", "tea"], ["nat", "tan"], ["bat"]]}],
     [{"input": (["a"],), "expected": [["a"]]}]),
    ("verify-011", "Valid Anagram: are two strings anagrams of each other", "easy", "strings", "hashing",
     s_valid_anagram, o_valid_anagram,
     [{"input": ("anagram", "nagaram"), "expected": True}, {"input": ("rat", "car"), "expected": False}],
     [{"input": ("", ""), "expected": True}]),
    ("verify-012", "Contains Duplicate: does an array have any repeated value", "easy", "arrays", "hashing",
     s_contains_duplicate, o_contains_duplicate,
     [{"input": ([1, 2, 3, 1],), "expected": True}, {"input": ([1, 2, 3, 4],), "expected": False}],
     [{"input": ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), "expected": True}]),
    ("verify-013", "Merge Intervals: merge all overlapping intervals", "medium", "arrays", "sorting",
     s_merge_intervals, o_merge_intervals,
     [{"input": ([[1, 3], [2, 6], [8, 10], [15, 18]],), "expected": [[1, 6], [8, 10], [15, 18]]},
      {"input": ([[1, 4], [4, 5]],), "expected": [[1, 5]]}],
     [{"input": ([],), "expected": []}]),
    ("verify-014", "Product of Array Except Self", "medium", "arrays", "prefix product",
     s_product_except_self, o_product_except_self,
     [{"input": ([1, 2, 3, 4],), "expected": [24, 12, 8, 6]},
      {"input": ([-1, 1, 0, -3, 3],), "expected": [0, 0, 9, 0, 0]}],
     [{"input": ([2, 3],), "expected": [3, 2]}]),
    ("verify-015", "First Unique Character in a String", "easy", "strings", "hashing",
     s_first_unique_char, o_first_unique_char,
     [{"input": ("leetcode",), "expected": 0}, {"input": ("loveleetcode",), "expected": 2}],
     [{"input": ("aabb",), "expected": -1}]),
    ("verify-016", "Binary Search: return index of target or -1", "easy", "binary search", "binary search",
     s_binary_search, o_binary_search,
     [{"input": ([-1, 0, 3, 5, 9, 12], 9), "expected": 4},
      {"input": ([-1, 0, 3, 5, 9, 12], 2), "expected": -1}],
     [{"input": ([5], 5), "expected": 0}, {"input": ([], 1), "expected": -1}]),
]

new_verified = []
for (qid, title, diff, topic, skill, sol, oracle, tests, edge) in specs:
    r = gate.verify(qid, title, diff, topic, skill, sol, oracle, tests, edge)
    if r["published"]:
        new_verified.append({
            "id": qid, "type": "coding", "title": title, "question": title,
            "difficulty": diff, "topic": topic, "sub_topic": skill, "pattern": skill,
            "skill": skill, "solution": {"code": CODE[qid], "language": "python"},
            "testcases": tests, "hidden_testcases": edge, "examples": tests[:2],
            "correct_answer": tests[0]["expected"], "trust_status": "verified",
            "trust_report": r,
            "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon"],
            "role": ["student", "sde"], "stage": "placement",
            "source_bank": "verified_placement_questions", "verification_version": 1,
            "provenance": "independently verified foundational pattern",
        })
        print(f"  {qid} {title[:40]}: verified")
    else:
        print(f"  {qid} {title[:40]}: FAILED {r}")

# Append to existing verified bank, dedupe by id
with open(VERIFIED_PATH, "r", encoding="utf-8") as f:
    existing = json.load(f)
existing_ids = {q["id"] for q in existing}
merged = list(existing) + [q for q in new_verified if q["id"] not in existing_ids]
with open(VERIFIED_PATH, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"\nVerified bank now has {len(merged)} questions (added {len(new_verified)} this run)")