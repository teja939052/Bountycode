"""
LeetCode Problem Importer for PlacementPro.

Converts LeetCode-style problems to PlacementPro format and seeds them
into MongoDB or the in-memory question store.

Usage:
    python backend/scripts/seed_leetcode.py
    python backend/scripts/seed_leetcode.py --limit 100
    python backend/scripts/seed_leetcode.py --memory-only
"""
import asyncio
import os
import sys
import argparse
import logging
from datetime import datetime, timezone
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.services import question_store
from app.database import get_client

settings = get_settings()
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# LeetCode Problem Catalog
# ──────────────────────────────────────────────────────────────────────────────
# Format: (leetcode_id, title, difficulty, topic, companies, statement, examples, constraints, solution_code, time_complexity, space_complexity)

LEETCODE_PROBLEMS = [
    # ─── Arrays & Hashing ───
    (1, "Two Sum", "easy", "Arrays", ["Google", "Amazon", "Meta", "Microsoft"],
     "Given array nums and target, return indices of two numbers that add to target.",
     [{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}],
     "2 <= nums.length <= 10^4",
     "def twoSum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i",
     "O(n)", "O(n)"),

    (49, "Group Anagrams", "medium", "Arrays", ["Amazon", "Google", "Meta", "Microsoft"],
     "Group anagrams together from array of strings.",
     [{"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]'}],
     "1 <= strs.length <= 10^4",
     "def groupAnagrams(strs):\n    from collections import defaultdict\n    mp = defaultdict(list)\n    for s in strs:\n        mp[''.join(sorted(s))].append(s)\n    return list(mp.values())",
     "O(n*k*log k)", "O(n*k)"),

    (217, "Contains Duplicate", "easy", "Arrays", ["Amazon", "Google", "Microsoft"],
     "Return true if any value appears at least twice in array.",
     [{"input": "nums = [1,2,3,1]", "output": "true"}],
     "1 <= nums.length <= 10^5",
     "def containsDuplicate(nums):\n    return len(set(nums)) != len(nums)",
     "O(n)", "O(n)"),

    (238, "Product of Array Except Self", "medium", "Arrays", ["Amazon", "Google", "Meta", "Microsoft"],
     "Return array where answer[i] is product of all elements except nums[i]. O(n) without division.",
     [{"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]"}],
     "2 <= nums.length <= 10^5",
     "def productExceptSelf(nums):\n    n = len(nums); res = [1] * n; pref = 1\n    for i in range(n):\n        res[i] = pref; pref *= nums[i]\n    suff = 1\n    for i in range(n-1, -1, -1):\n        res[i] *= suff; suff *= nums[i]\n    return res",
     "O(n)", "O(1)"),

    (242, "Valid Anagram", "easy", "Strings", ["Amazon", "Google", "Microsoft"],
     "Return true if t is anagram of s.",
     [{"input": "s = 'anagram', t = 'nagaram'", "output": "true"}],
     "1 <= s.length, t.length <= 5 * 10^4",
     "def isAnagram(s, t):\n    if len(s) != len(t): return False\n    c = [0] * 26\n    for ch in s: c[ord(ch) - 97] += 1\n    for ch in t:\n        if c[ord(ch) - 97] == 0: return False\n        c[ord(ch) - 97] -= 1\n    return True",
     "O(n)", "O(1)"),

    (347, "Top K Frequent Elements", "medium", "Arrays", ["Google", "Amazon", "Meta", "Microsoft"],
     "Return k most frequent elements.",
     [{"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]"}],
     "1 <= nums.length <= 10^5",
     "def topKFrequent(nums, k):\n    from collections import Counter\n    freq = Counter(nums)\n    buckets = [[] for _ in range(len(nums) + 1)]\n    for num, f in freq.items():\n        buckets[f].append(num)\n    res = []\n    for i in range(len(buckets) - 1, 0, -1):\n        for num in buckets[i]:\n            res.append(num)\n            if len(res) == k: return res",
     "O(n)", "O(n)"),

    (424, "Longest Repeating Character Replacement", "medium", "Sliding Window", ["Amazon", "Google", "Microsoft"],
     "Return length of longest substring with same character after at most k replacements.",
     [{"input": "s = 'ABAB', k = 2", "output": "4"}],
     "1 <= s.length <= 10^5",
     "def characterReplacement(s, k):\n    c = [0] * 26; l = 0; mx = 0; best = 0\n    for r in range(len(s)):\n        idx = ord(s[r]) - 65; c[idx] += 1; mx = max(mx, c[idx])\n        while (r - l + 1) - mx > k:\n            c[ord(s[l]) - 65] -= 1; l += 1\n        best = max(best, r - l + 1)\n    return best",
     "O(n)", "O(1)"),

    (448, "Find All Numbers Disappeared in an Array", "easy", "Arrays", ["Google", "Amazon", "Microsoft"],
     "Return list of numbers missing from array [1,n].",
     [{"input": "nums = [4,3,2,7,8,2,3,1]", "output": "[5,6]"}],
     "1 <= nums.length <= 10^5",
     "def findDisappearedNumbers(nums):\n    for n in nums:\n        idx = abs(n) - 1\n        if nums[idx] > 0: nums[idx] *= -1\n    return [i + 1 for i, n in enumerate(nums) if n > 0]",
     "O(n)", "O(1)"),

    (53, "Maximum Subarray", "medium", "Arrays", ["Amazon", "Google", "Meta", "Microsoft"],
     "Return maximum sum of contiguous subarray (Kadane's).",
     [{"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6"}],
     "1 <= nums.length <= 10^5",
     "def maxSubArray(nums):\n    cur = glo = nums[0]\n    for n in nums[1:]:\n        cur = max(n, cur + n); glo = max(glo, cur)\n    return glo",
     "O(n)", "O(1)"),

    (73, "Set Matrix Zeroes", "medium", "Arrays", ["Amazon", "Google", "Microsoft"],
     "If element is 0, set entire row and column to 0 in-place.",
     [{"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]"}],
     "m, n <= 200",
     "def setZeroes(matrix):\n    m, n = len(matrix), len(matrix[0]); r0 = c0 = False\n    for j in range(n):\n        if matrix[0][j] == 0: r0 = True; break\n    for i in range(m):\n        if matrix[i][0] == 0: c0 = True; break\n    for i in range(1, m):\n        for j in range(1, n):\n            if matrix[i][j] == 0: matrix[i][0] = matrix[0][j] = 0\n    for i in range(1, m):\n        for j in range(1, n):\n            if matrix[i][0] == 0 or matrix[0][j] == 0: matrix[i][j] = 0\n    if r0:\n        for j in range(n): matrix[0][j] = 0\n    if c0:\n        for i in range(m): matrix[i][0] = 0",
     "O(m*n)", "O(1)"),

    (75, "Sort Colors", "medium", "Arrays", ["Amazon", "Google", "Microsoft"],
     "Sort array of 0s, 1s, and 2s in-place (Dutch National Flag).",
     [{"input": "nums = [2,0,2,1,1,0]", "output": "[0,0,1,1,2,2]"}],
     "1 <= nums.length <= 300",
     "def sortColors(nums):\n    l, m, h = 0, 0, len(nums) - 1\n    while m <= h:\n        if nums[m] == 0:\n            nums[l], nums[m] = nums[m], nums[l]; l += 1; m += 1\n        elif nums[m] == 1: m += 1\n        else:\n            nums[m], nums[h] = nums[h], nums[m]; h -= 1",
     "O(n)", "O(1)"),

    # ─── Two Pointers ───
    (11, "Container With Most Water", "medium", "Two Pointers", ["Amazon", "Google", "Meta", "Microsoft"],
     "Find two lines that together with x-axis form container with most water.",
     [{"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49"}],
     "2 <= height.length <= 10^5",
     "def maxArea(height):\n    l, r = 0, len(height) - 1; best = 0\n    while l < r:\n        w = r - l\n        if height[l] < height[r]:\n            best = max(best, height[l] * w); l += 1\n        else:\n            best = max(best, height[r] * w); r -= 1\n    return best",
     "O(n)", "O(1)"),

    (15, "3Sum", "medium", "Two Pointers", ["Amazon", "Google", "Meta", "Microsoft"],
     "Return all unique triplets that sum to 0.",
     [{"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"}],
     "3 <= nums.length <= 3000",
     "def threeSum(nums):\n    nums.sort(); res = []\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i-1]: continue\n        l, r = i + 1, len(nums) - 1\n        while l < r:\n            s = nums[i] + nums[l] + nums[r]\n            if s < 0: l += 1\n            elif s > 0: r -= 1\n            else:\n                res.append([nums[i], nums[l], nums[r]])\n                while l < r and nums[l] == nums[l+1]: l += 1\n                while l < r and nums[r] == nums[r-1]: r -= 1\n                l += 1; r -= 1\n    return res",
     "O(n^2)", "O(n)"),

    (19, "Remove Nth Node From End of List", "medium", "Linked Lists", ["Amazon", "Google", "Microsoft"],
     "Remove nth node from end of linked list in one pass.",
     [{"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"}],
     "1 <= sz <= 30",
     "def removeNthFromEnd(head, n):\n    dummy = ListNode(0, head); s = f = dummy\n    for _ in range(n): f = f.next\n    while f.next:\n        s = s.next; f = f.next\n    s.next = s.next.next\n    return dummy.next",
     "O(n)", "O(1)"),

    # ─── Sliding Window ───
    (3, "Longest Substring Without Repeating Characters", "medium", "Sliding Window", ["Amazon", "Google", "Meta", "Microsoft"],
     "Find length of longest substring without repeating characters.",
     [{"input": "s = 'abcabcbb'", "output": "3"}],
     "0 <= s.length <= 5 * 10^4",
     "def lengthOfLongestSubstring(s):\n    seen = set(); l = 0; mx = 0\n    for r in range(len(s)):\n        while s[r] in seen:\n            seen.remove(s[l]); l += 1\n        seen.add(s[r]); mx = max(mx, r - l + 1)\n    return mx",
     "O(n)", "O(min(m,n))"),

    (438, "Find All Anagrams in a String", "medium", "Sliding Window", ["Amazon", "Google", "Microsoft"],
     "Return all start indices of p's anagrams in s.",
     [{"input": "s = 'cbaebabacd', p = 'abc'", "output": "[0,6]"}],
     "1 <= s.length, p.length <= 3 * 10^4",
     "def findAnagrams(s, p):\n    if len(p) > len(s): return []\n    cp = [0] * 26; cs = [0] * 26; res = []\n    for ch in p: cp[ord(ch) - 97] += 1\n    for i in range(len(s)):\n        cs[ord(s[i]) - 97] += 1\n        if i >= len(p): cs[ord(s[i - len(p)]) - 97] -= 1\n        if i >= len(p) - 1 and cs == cp: res.append(i - len(p) + 1)\n    return res",
     "O(n)", "O(1)"),

    (567, "Permutation in String", "medium", "Sliding Window", ["Amazon", "Google", "Microsoft"],
     "Return true if s2 contains permutation of s1.",
     [{"input": "s1 = 'ab', s2 = 'eidbaooo'", "output": "true"}],
     "1 <= s1.length, s2.length <= 10^4",
     "def checkInclusion(s1, s2):\n    if len(s1) > len(s2): return False\n    c1 = [0] * 26; c2 = [0] * 26\n    for ch in s1: c1[ord(ch) - 97] += 1\n    for i in range(len(s2)):\n        c2[ord(s2[i]) - 97] += 1\n        if i >= len(s1): c2[ord(s2[i - len(s1)]) - 97] -= 1\n        if c1 == c2: return True\n    return False",
     "O(n)", "O(1)"),

    # ─── Binary Search ───
    (704, "Binary Search", "easy", "Binary Search", ["Amazon", "Google", "Microsoft"],
     "Return target index in sorted array or -1.",
     [{"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"}],
     "1 <= nums.length <= 10^4",
     "def search(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: lo = mid + 1\n        else: hi = mid - 1\n    return -1",
     "O(log n)", "O(1)"),

    (33, "Search in Rotated Sorted Array", "medium", "Binary Search", ["Amazon", "Google", "Microsoft"],
     "Search target in rotated sorted array.",
     [{"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"}],
     "1 <= nums.length <= 5000",
     "def search(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target: return mid\n        if nums[lo] <= nums[mid]:\n            if nums[lo] <= target < nums[mid]: hi = mid - 1\n            else: lo = mid + 1\n        else:\n            if nums[mid] < target <= nums[hi]: lo = mid + 1\n            else: hi = mid - 1\n    return -1",
     "O(log n)", "O(1)"),

    (34, "Find First and Last Position", "medium", "Binary Search", ["Amazon", "Google", "Microsoft"],
     "Find first and last position of target in sorted array.",
     [{"input": "nums = [5,7,7,8,8,10], target = 8", "output": "[3,4]"}],
     "0 <= nums.length <= 10^5",
     "def searchRange(nums, target):\n    def left():\n        lo, hi = 0, len(nums) - 1\n        while lo <= hi:\n            mid = (lo + hi) // 2\n            if nums[mid] < target: lo = mid + 1\n            else: hi = mid - 1\n        return lo\n    def right():\n        lo, hi = 0, len(nums) - 1\n        while lo <= hi:\n            mid = (lo + hi) // 2\n            if nums[mid] <= target: lo = mid + 1\n            else: hi = mid - 1\n        return hi\n    l = left()\n    if l >= len(nums) or nums[l] != target: return [-1, -1]\n    return [l, right()]",
     "O(log n)", "O(1)"),

    # ─── Linked Lists ───
    (21, "Merge Two Sorted Lists", "easy", "Linked Lists", ["Amazon", "Google", "Microsoft"],
     "Merge two sorted linked lists.",
     [{"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]"}],
     "0 <= list1.length, list2.length <= 50",
     "def mergeTwoLists(l1, l2):\n    dummy = ListNode(); cur = dummy\n    while l1 and l2:\n        if l1.val <= l2.val: cur.next = l1; l1 = l1.next\n        else: cur.next = l2; l2 = l2.next\n        cur = cur.next\n    cur.next = l1 or l2\n    return dummy.next",
     "O(n+m)", "O(1)"),

    (141, "Linked List Cycle", "easy", "Linked Lists", ["Amazon", "Google", "Microsoft"],
     "Determine if linked list has a cycle.",
     [{"input": "head = [3,2,0,-4], pos = 1", "output": "true"}],
     "0 <= n <= 10^4",
     "def hasCycle(head):\n    s = f = head\n    while f and f.next:\n        s = s.next; f = f.next.next\n        if s == f: return True\n    return False",
     "O(n)", "O(1)"),

    (206, "Reverse Linked List", "easy", "Linked Lists", ["Amazon", "Google", "Meta", "Microsoft"],
     "Reverse linked list iteratively.",
     [{"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"}],
     "0 <= n <= 500",
     "def reverseList(head):\n    prev = None; curr = head\n    while curr:\n        nxt = curr.next; curr.next = prev\n        prev = curr; curr = nxt\n    return prev",
     "O(n)", "O(1)"),

    # ─── Trees ───
    (104, "Maximum Depth of Binary Tree", "easy", "Trees", ["Amazon", "Google", "Microsoft"],
     "Return maximum depth of binary tree.",
     [{"input": "root = [3,9,20,null,null,15,7]", "output": "3"}],
     "0 <= n <= 10^4",
     "def maxDepth(root):\n    if not root: return 0\n    return 1 + max(maxDepth(root.left), maxDepth(root.right))",
     "O(n)", "O(n)"),

    (226, "Invert Binary Tree", "easy", "Trees", ["Google", "Amazon", "Microsoft"],
     "Invert binary tree (mirror).",
     [{"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]"}],
     "0 <= n <= 100",
     "def invertTree(root):\n    if not root: return None\n    root.left, root.right = invertTree(root.right), invertTree(root.left)\n    return root",
     "O(n)", "O(n)"),

    (235, "Lowest Common Ancestor of BST", "medium", "Trees", ["Amazon", "Google", "Microsoft"],
     "Find LCA of two nodes in BST.",
     [{"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "output": "6"}],
     "2 <= n <= 10^4",
     "def lowestCommonAncestor(root, p, q):\n    if not root: return None\n    if p.val < root.val and q.val < root.val:\n        return lowestCommonAncestor(root.left, p, q)\n    if p.val > root.val and q.val > root.val:\n        return lowestCommonAncestor(root.right, p, q)\n    return root",
     "O(h)", "O(h)"),

    # ─── Dynamic Programming ───
    (70, "Climbing Stairs", "easy", "DP", ["Amazon", "Google", "Microsoft"],
     "Climb n stairs, 1 or 2 steps at a time. Return ways.",
     [{"input": "n = 3", "output": "3"}],
     "1 <= n <= 45",
     "def climbStairs(n):\n    if n <= 2: return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b",
     "O(n)", "O(1)"),

    (198, "House Robber", "medium", "DP", ["Amazon", "Google", "Microsoft"],
     "Max amount robbed without robbing adjacent houses.",
     [{"input": "nums = [1,2,3,1]", "output": "4"}],
     "1 <= nums.length <= 100",
     "def rob(nums):\n    if not nums: return 0\n    if len(nums) == 1: return nums[0]\n    a, b = nums[0], max(nums[0], nums[1])\n    for i in range(2, len(nums)):\n        a, b = b, max(b, a + nums[i])\n    return b",
     "O(n)", "O(1)"),

    (300, "Longest Increasing Subsequence", "medium", "DP", ["Amazon", "Google", "Microsoft"],
     "Return length of longest increasing subsequence.",
     [{"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4"}],
     "1 <= nums.length <= 2500",
     "def lengthOfLIS(nums):\n    from bisect import bisect_left\n    tail = []\n    for n in nums:\n        i = bisect_left(tail, n)\n        if i == len(tail): tail.append(n)\n        else: tail[i] = n\n    return len(tail)",
     "O(n log n)", "O(n)"),

    # ─── Graphs ───
    (200, "Number of Islands", "medium", "Graphs", ["Amazon", "Google", "Meta", "Microsoft"],
     "Return number of islands in grid.",
     [{"input": "grid = [['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']]", "output": "3"}],
     "m, n <= 300",
     "def numIslands(grid):\n    if not grid: return 0\n    m, n = len(grid), len(grid[0]); count = 0\n    def dfs(i, j):\n        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1': return\n        grid[i][j] = '0'\n        dfs(i+1, j); dfs(i-1, j); dfs(i, j+1); dfs(i, j-1)\n    for i in range(m):\n        for j in range(n):\n            if grid[i][j] == '1':\n                dfs(i, j); count += 1\n    return count",
     "O(m*n)", "O(m*n)"),

    (733, "Flood Fill", "easy", "Graphs", ["Amazon", "Google", "Microsoft"],
     "Flood fill starting pixel and connected pixels of same color.",
     [{"input": "image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2", "output": "[[2,2,2],[2,2,0],[2,0,1]]"}],
     "m, n <= 50",
     "def floodFill(image, sr, sc, color):\n    if image[sr][sc] == color: return image\n    m, n = len(image), len(image[0]); old = image[sr][sc]\n    def dfs(i, j):\n        if i < 0 or i >= m or j < 0 or j >= n or image[i][j] != old: return\n        image[i][j] = color\n        dfs(i+1, j); dfs(i-1, j); dfs(i, j+1); dfs(i, j-1)\n    dfs(sr, sc)\n    return image",
     "O(m*n)", "O(m*n)"),

    # ─── Stacks ───
    (20, "Valid Parentheses", "easy", "Stacks", ["Amazon", "Google", "Microsoft", "Meta"],
     "Determine if input string of brackets is valid.",
     [{"input": "s = '()[]{}'", "output": "true"}],
     "1 <= s.length <= 10^4",
     "def isValid(s):\n    st = []; mp = {')':'(', '}':'{', ']':'['}\n    for c in s:\n        if c in mp:\n            if not st or st[-1] != mp[c]: return False\n            st.pop()\n        else: st.append(c)\n    return not st",
     "O(n)", "O(n)"),

    (155, "Min Stack", "medium", "Stacks", ["Amazon", "Google", "Microsoft"],
     "Design stack with O(1) getMin.",
     [{"input": "['MinStack','push','push','push','getMin','pop','top','getMin']", "output": "[null,null,null,null,-3,null,2,-2]"}],
     "-2^31 <= val <= 2^31 - 1",
     "class MinStack:\n    def __init__(self):\n        self.st = []; self.mn = []\n    def push(self, val):\n        self.st.append(val)\n        if not self.mn or val <= self.mn[-1]: self.mn.append(val)\n    def pop(self):\n        if self.st.pop() == self.mn[-1]: self.mn.pop()\n    def top(self): return self.st[-1]\n    def getMin(self): return self.mn[-1]",
     "O(1)", "O(n)"),

    # ─── Heaps ───
    (215, "Kth Largest Element in Array", "medium", "Heaps", ["Amazon", "Google", "Meta", "Microsoft"],
     "Find kth largest element in unsorted array.",
     [{"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5"}],
     "1 <= k <= nums.length <= 10^4",
     "def findKthLargest(nums, k):\n    import heapq\n    return heapq.nlargest(k, nums)[-1]",
     "O(n log k)", "O(k)"),

    # ─── Tries ───
    (208, "Implement Trie", "medium", "Tries", ["Amazon", "Google", "Microsoft"],
     "Implement Trie with insert, search, and startsWith.",
     [{"input": "['Trie','insert','search','startsWith']", "output": "[null,null,true,true]"}],
     "1 <= word.length, prefix.length <= 2000",
     "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    def insert(self, word):\n        node = self.root\n        for ch in word:\n            if ch not in node.children:\n                node.children[ch] = TrieNode()\n            node = node.children[ch]\n        node.is_end = True\n    def search(self, word):\n        node = self._find(word)\n        return node is not None and node.is_end\n    def startsWith(self, prefix):\n        return self._find(prefix) is not None\n    def _find(self, word):\n        node = self.root\n        for ch in word:\n            if ch not in node.children: return None\n            node = node.children[ch]\n        return node",
     "O(L)", "O(L)"),

    # ─── Design ───
    (146, "LRU Cache", "medium", "Design", ["Amazon", "Google", "Meta", "Microsoft"],
     "Design LRU cache with O(1) get and put.",
     [{"input": "['LRUCache','put','put','get','put','get','put','get','get']", "output": "[null,null,null,1,null,-1,null,-1,3]"}],
     "1 <= capacity <= 3000",
     "from collections import OrderedDict\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cap = capacity; self.cache = OrderedDict()\n    def get(self, key):\n        if key not in self.cache: return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n    def put(self, key, value):\n        if key in self.cache: self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.cap: self.cache.popitem(last=False)",
     "O(1)", "O(capacity)"),

    (380, "Insert Delete GetRandom O(1)", "medium", "Design", ["Amazon", "Google", "Microsoft"],
     "Design data structure with insert, remove, and getRandom in O(1).",
     [{"input": "['RandomizedSet','insert','remove','insert','getRandom']", "output": "[null,true,false,true,2]"}],
     "-2^31 <= val <= 2^31 - 1",
     "import random\nclass RandomizedSet:\n    def __init__(self):\n        self.vals = []; self.mp = {}\n    def insert(self, val):\n        if val in self.mp: return False\n        self.mp[val] = len(self.vals); self.vals.append(val); return True\n    def remove(self, val):\n        if val not in self.mp: return False\n        i = self.mp[val]; last = self.vals[-1]\n        self.vals[i] = last; self.mp[last] = i\n        self.vals.pop(); del self.mp[val]; return True\n    def getRandom(self):\n        return random.choice(self.vals)",
     "O(1) avg", "O(n)"),
]


def build_problem_doc(problem_id, title, difficulty, topic, companies, statement, examples, constraints,
                      solution_code, time_complexity, space_complexity) -> dict:
    """Convert a LeetCode problem definition to PlacementPro format."""
    examples = examples or []
    constraints = constraints or ""

    # Build visible test cases from examples
    visible_test_cases = []
    for ex in examples[:3]:
        visible_test_cases.append({
            "input": ex.get("input", ""),
            "expected": ex.get("output", ""),
        })

    return {
        "type": "coding",
        "company": companies,
        "companies": companies,
        "role": "SDE",
        "difficulty": difficulty,
        "topic": topic,
        "sub_topic": "",
        "question_title": title,
        "statement": statement,
        "question": statement,
        "options": [],
        "correct_answer": examples[0]["output"] if examples else "",
        "explanation": f"LeetCode {problem_id}: {title}",
        "hints": [
            "Think about the time/space complexity constraints.",
            "Consider edge cases: empty input, single element, duplicates.",
            "Try to optimize your solution after getting a working brute force.",
        ],
        "solution": {
            "code": solution_code,
            "language": "python",
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
        },
        "visible_test_cases": visible_test_cases,
        "constraints": [constraints] if isinstance(constraints, str) else constraints,
        "examples": examples,
        "frequency": 0,
        "source": f"LeetCode {problem_id}",
        "submitted_by": "system",
        "upvotes": 0,
        "downvotes": 0,
        "reported": False,
        "leetcode_id": problem_id,
        "leetcode_url": f"https://leetcode.com/problems/{title.lower().replace(' ', '-').replace(',', '').replace(chr(39), '')}/",
    }


async def seed_leetcode(limit: Optional[int] = None, memory_only: bool = False):
    """Seed LeetCode problems into MongoDB and/or memory."""
    db_client = None
    collection = None

    if not memory_only:
        db_client = get_client()
        db = db_client[settings.DATABASE_NAME]
        collection = db["curated_questions"]

    # Load existing questions to avoid duplicates
    question_store.load_all()
    existing_ids = {q.get("leetcode_id") for q in question_store._questions if q.get("leetcode_id")}
    existing_source = {q.get("source") for q in question_store._questions if q.get("source", "").startswith("LeetCode")}

    problems_to_seed = LEETCODE_PROBLEMS[:limit] if limit else LEETCODE_PROBLEMS

    inserted_mongo = 0
    inserted_memory = 0
    skipped = 0

    for problem_id, title, difficulty, topic, companies, statement, examples, constraints, solution_code, tc, sc in problems_to_seed:
        # Skip if already exists
        if problem_id in existing_ids or f"LeetCode {problem_id}" in existing_source:
            skipped += 1
            continue

        doc = build_problem_doc(problem_id, title, difficulty, topic, companies, statement, examples, constraints,
                                solution_code, tc, sc)

        # Insert into MongoDB
        if not memory_only and collection is not None:
            try:
                result = await collection.insert_one(doc)
                doc["id"] = str(result.inserted_id)
                inserted_mongo += 1
            except Exception as e:
                logger.warning("MongoDB insert failed for %s: %s", title, e)

        # Insert into memory
        try:
            question_store.insert_question(doc)
            inserted_memory += 1
        except Exception as e:
            logger.warning("Memory insert failed for %s: %s", title, e)

    total = len(problems_to_seed)
    logger.info("LeetCode seeding complete: %d total, %d skipped, %d to MongoDB, %d to memory",
                total, skipped, inserted_mongo, inserted_memory)
    print(f"\nLeetCode seeding complete!")
    print(f"  Total problems: {total}")
    print(f"  Skipped (already exists): {skipped}")
    print(f"  Inserted to MongoDB: {inserted_mongo}")
    print(f"  Inserted to memory: {inserted_memory}")
    print(f"  Total in memory: {len(question_store._questions)}")

    if not memory_only and collection is not None:
        mongo_count = await collection.count_documents({})
        print(f"  Total in MongoDB: {mongo_count}")


def main():
    parser = argparse.ArgumentParser(description="Seed LeetCode problems into PlacementPro")
    parser.add_argument("--limit", type=int, help="Limit number of problems to seed")
    parser.add_argument("--memory-only", action="store_true", help="Only insert into memory, skip MongoDB")
    args = parser.parse_args()

    asyncio.run(seed_leetcode(limit=args.limit, memory_only=args.memory_only))


if __name__ == "__main__":
    main()
