"""Canonical reference solutions for platform problems.

The platform authors know the correct answer to every problem. These
solutions are the single source of truth used to:
  1. Precompute/verify expected test-case outputs offline (zero AI, zero
     external execution at runtime) via scripts/precompute_expected_outputs.py
  2. Serve "official solution" views without generating content on the fly

Keyed by slugified problem title. Each entry maps a problem to its Python
reference implementation. Function signature must match the starter code's
entry function (the same name used by the function-call oracle grader).
"""
from __future__ import annotations

from typing import Callable, Dict, Optional


def _reverse_string(s: str) -> str:
    return s[::-1]


def _fizzbuzz(n: int) -> list:
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out


def _is_palindrome(s: str) -> bool:
    t = "".join(c.lower() for c in s if c.isalnum())
    return t == t[::-1]


def _two_sum(nums: list, target: int) -> list:
    seen = {}
    for i, v in enumerate(nums):
        if target - v in seen:
            return [seen[target - v], i]
        seen[v] = i
    return []


def _max_of_array(nums: list) -> int:
    return max(nums)


def _factorial(n: int) -> int:
    import math
    return math.factorial(n)


def _fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _is_anagram(a: str, b: str) -> bool:
    from collections import Counter
    return Counter(a) == Counter(b)


def _count_vowels(s: str) -> int:
    return sum(1 for c in s.lower() if c in "aeiou")


def _array_sum(nums: list) -> int:
    return sum(nums)


def _is_valid_parentheses(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in "([{":
            stack.append(c)
        elif c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack


def _binary_search(nums: list, target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def _merge_intervals(intervals: list) -> list:
    intervals = sorted((list(i) for i in intervals), key=lambda x: x[0])
    merged = []
    for iv in intervals:
        if merged and iv[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], iv[1])
        else:
            merged.append(iv)
    return [tuple(m) for m in merged] if False else merged


def _group_anagrams(words: list) -> list:
    from collections import defaultdict
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return sorted(sorted(g) for g in groups.values())


def _length_of_longest_substring(s: str) -> int:
    last, start, best = {}, 0, 0
    for i, c in enumerate(s):
        if c in last and last[c] >= start:
            start = last[c] + 1
        last[c] = i
        best = max(best, i - start + 1)
    return best


def _product_except_self(nums: list) -> list:
    n = len(nums)
    res = [1] * n
    left = 1
    for i in range(n):
        res[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        res[i] *= right
        right *= nums[i]
    return res


def _find_duplicates(nums: list) -> list:
    out = []
    for v in nums:
        i = abs(v) - 1
        if nums[i] < 0:
            out.append(abs(v))
        else:
            nums[i] = -nums[i]
    for i in range(len(nums)):
        nums[i] = abs(nums[i])
    return out


def _max_area(heights: list) -> int:
    l, r, best = 0, len(heights) - 1, 0
    while l < r:
        best = max(best, min(heights[l], heights[r]) * (r - l))
        if heights[l] < heights[r]:
            l += 1
        else:
            r -= 1
    return best


def _rotate_array(nums: list, k: int) -> list:
    k %= len(nums)
    return nums[-k:] + nums[:-k]


def _is_valid_sudoku(board: list) -> bool:
    rows, cols, boxes = set(), set(), set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == ".":
                continue
            key = (r // 3, c // 3)
            if (r, v) in rows or (c, v) in cols or (key, v) in boxes:
                return False
            rows.add((r, v))
            cols.add((c, v))
            boxes.add((key, v))
    return True


class _LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data: Dict = {}
        self.ops = []

    def get(self, key):
        self.ops.append(("get", key))
        return self.data.get(key, None)

    def put(self, key, value):
        self.ops.append(("put", key))
        self.data[key] = value
        if len(self.data) > self.capacity:
            for k, kind in self.ops:
                if kind == "put" and k in self.data and len(self.data) > self.capacity:
                    del self.data[k]
                    break


def _median_two_sorted(a: list, b: list) -> float:
    merged = sorted(a + b)
    n = len(merged)
    mid = n // 2
    if n % 2:
        return float(merged[mid])
    return (merged[mid - 1] + merged[mid]) / 2.0


def _trapping_rain_water(h: list) -> int:
    if not h:
        return 0
    left, right = [0] * len(h), [0] * len(h)
    left[0], right[-1] = h[0], h[-1]
    for i in range(1, len(h)):
        left[i] = max(left[i - 1], h[i])
    for i in range(len(h) - 2, -1, -1):
        right[i] = max(right[i + 1], h[i])
    return sum(min(left[i], right[i]) - h[i] for i in range(len(h)))


def _merge_k_lists(lists: list) -> list:
    vals = sorted(v for lst in lists for v in lst)
    return vals


def _longest_palindrome(s: str) -> str:
    if len(s) < 2:
        return s
    start, maxlen = 0, 1
    for i in range(len(s)):
        for j in (i + maxlen, i + maxlen + 1):
            if j <= len(s) and s[i:j] == s[i:j][::-1]:
                start, maxlen = i, j - i
    return s[start:start + maxlen]


def _max_sliding_window(nums: list, k: int) -> list:
    from collections import deque
    dq, out = deque(), []
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def _min_window(s: str, t: str) -> str:
    from collections import Counter
    need, missing = Counter(t), len(t)
    best = (float("inf"), 0, 0)
    l = 0
    for r, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        if missing == 0:
            while need[s[l]] < 0:
                need[s[l]] += 1
                l += 1
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r + 1)
    return "" if best[0] == float("inf") else s[best[1]:best[2]]


def _word_ladder(begin: str, end: str, word_list: list) -> int:
    words = set(word_list)
    if end not in words:
        return 0
    frontier = [(begin, 1)]
    visited = {begin}
    while frontier:
        word, depth = frontier.pop(0)
        if word == end:
            return depth
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + c + word[i + 1:]
                if nxt in words and nxt not in visited:
                    visited.add(nxt)
                    frontier.append((nxt, depth + 1))
    return 0


def _largest_rectangle(heights: list) -> int:
    stack, best = [], 0
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best


# slug → {"function_name": str, "python": source string}
REFERENCE_SOLUTIONS: Dict[str, Dict[str, str]] = {}


def register(slug: str, function_name: str, fn: Callable):
    import inspect
    source = inspect.getsource(fn)
    # Rename the (possibly underscore-prefixed) def to the public entry name
    source = source.replace(f"def {fn.__name__}(", f"def {function_name}(", 1)
    REFERENCE_SOLUTIONS[slug] = {
        "function_name": function_name,
        "python": source,
    }


register("reverse-string", "reverse_string", _reverse_string)
register("fizzbuzz", "fizzbuzz", _fizzbuzz)
register("palindrome-check", "is_palindrome", _is_palindrome)
register("two-sum", "two_sum", _two_sum)
register("max-of-array", "max_of_array", _max_of_array)
register("factorial", "factorial", _factorial)
register("fibonacci", "fibonacci", _fibonacci)
register("anagram-check", "is_anagram", _is_anagram)
register("count-vowels", "count_vowels", _count_vowels)
register("array-sum", "array_sum", _array_sum)
register("valid-parentheses", "is_valid_parentheses", _is_valid_parentheses)
register("binary-search", "binary_search", _binary_search)
register("merge-intervals", "merge_intervals", _merge_intervals)
register("group-anagrams", "group_anagrams", _group_anagrams)
register(
    "longest-substring-without-repeating-characters",
    "length_of_longest_substring",
    _length_of_longest_substring,
)
register("product-of-array-except-self", "product_except_self", _product_except_self)
register("find-all-duplicates", "find_duplicates", _find_duplicates)
register("container-with-most-water", "max_area", _max_area)
register("rotate-array", "rotate_array", _rotate_array)
register("valid-sudoku", "is_valid_sudoku", _is_valid_sudoku)
register("median-of-two-sorted-arrays", "median_two_sorted", _median_two_sorted)
register("trapping-rain-water", "trapping_rain_water", _trapping_rain_water)
register("merge-k-sorted-lists", "merge_k_lists", _merge_k_lists)
register("longest-palindromic-substring", "longest_palindrome", _longest_palindrome)
register("sliding-window-maximum", "max_sliding_window", _max_sliding_window)
register("minimum-window-substring", "min_window", _min_window)
register("word-ladder", "word_ladder", _word_ladder)
register("largest-rectangle-in-histogram", "largest_rectangle", _largest_rectangle)


def slugify(title: str) -> str:
    return title.strip().lower().replace(" ", "-")


def get_reference_solution(problem_id_or_title: str, language: str = "python") -> Optional[Dict[str, str]]:
    """Look up a reference solution by slug, id, or human title."""
    key = slugify(problem_id_or_title)
    sol = REFERENCE_SOLUTIONS.get(key)
    if sol:
        return sol
    # try matching by slug of any registered entry against the raw string
    for slug, candidate in REFERENCE_SOLUTIONS.items():
        if slugify(problem_id_or_title) in slug or slug in slugify(problem_id_or_title):
            return candidate
    return None
