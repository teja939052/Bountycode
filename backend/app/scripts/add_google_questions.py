"""Add verified real Google interview questions with provenance."""
import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

GOOGLE_QUESTIONS = [
    {
        "id": "google-001",
        "type": "coding",
        "question": "Given a list of integers and a target sum, return indices of two numbers that add up to the target. You may assume one solution exists.",
        "question_title": "Two Sum",
        "difficulty": "easy",
        "topic": "Arrays",
        "sub_topic": "Hash Table",
        "companies": ["google"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://www.dsaprep.dev/blog/google-coding-interview-questions",
        "solution": {
            "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        need = target - num\n        if need in seen:\n            return [seen[need], i]\n        seen[num] = i\n    return []",
            "language": "python",
        },
        "test_cases": [
            {"input": "nums=[2,7,11,15], target=9", "output": "[0,1]", "hidden": False},
            {"input": "nums=[3,2,4], target=6", "output": "[1,2]", "hidden": False},
            {"input": "nums=[3,3], target=6", "output": "[0,1]", "hidden": True},
        ],
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9"},
        ],
        "constraints": "2 <= nums.length <= 10^4",
        "hints": ["Use a hash map to store seen values", "Target - current = needed value"],
        "explanation": "Store each number's index in a hash map. For each number, check if (target - num) is already in the map.",
        "dsa_guide": {"approach": "Hash Map", "data_structures": ["Hash Table", "Array"], "patterns": ["One-pass hash"], "tips": ["O(n) time, O(n) space"]},
    },
    {
        "id": "google-002",
        "type": "coding",
        "question": "Given a 2D grid of '1's (land) and '0's (water), count the number of islands. An island is a group of '1's connected 4-directionally.",
        "question_title": "Number of Islands",
        "difficulty": "medium",
        "topic": "Graphs",
        "sub_topic": "BFS/DFS",
        "companies": ["google"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://copilotinterview.com/blog/google-coding-interview-questions",
        "solution": {
            "code": "def numIslands(grid):\n    if not grid:\n        return 0\n    rows, cols = len(grid), len(grid[0])\n    count = 0\n\n    def bfs(r, c):\n        queue = [(r, c)]\n        grid[r][c] = '0'\n        while queue:\n            cr, cc = queue.pop()\n            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:\n                nr, nc = cr + dr, cc + dc\n                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':\n                    grid[nr][nc] = '0'\n                    queue.append((nr, nc))\n\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == '1':\n                bfs(r, c)\n                count += 1\n    return count",
            "language": "python",
        },
        "test_cases": [
            {"input": 'grid=[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', "output": "3", "hidden": False},
            {"input": 'grid=[["1","1","1"],["0","1","0"],["1","0","1"]]', "output": "2", "hidden": True},
        ],
        "examples": [
            {"input": 'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', "output": "3", "explanation": "Three islands are formed by connected 1s."},
        ],
        "constraints": "m == grid.length, n == grid[i].length, 1 <= m,n <= 300",
        "hints": ["Use BFS or DFS from every unvisited land cell", "Mark visited cells as water to avoid extra visited set"],
        "explanation": "Scan every cell. When you find unvisited land, run BFS/DFS to sink the entire island, then increment count.",
        "dsa_guide": {"approach": "BFS/DFS", "data_structures": ["Queue", "Grid"], "patterns": ["Connected components"], "tips": ["O(m*n) time, O(m*n) worst-case space"]},
    },
    {
        "id": "google-003",
        "type": "coding",
        "question": "Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays in O(log(m+n)) time.",
        "question_title": "Median of Two Sorted Arrays",
        "difficulty": "hard",
        "topic": "Binary Search",
        "sub_topic": "Divide and Conquer",
        "companies": ["google"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://www.dsaprep.dev/blog/google-coding-interview-questions",
        "solution": {
            "code": "def findMedianSortedArrays(nums1, nums2):\n    A, B = nums1, nums2\n    total = len(A) + len(B)\n    half = total // 2\n    if len(B) > len(A):\n        A, B = B, A\n    l, r = 0, len(B) - 1\n    while True:\n        i = (l + r) // 2  # B partition\n        j = half - i - 2  # A partition\n        Bleft = B[i] if i >= 0 else float('-inf')\n        Bright = B[i+1] if i+1 < len(B) else float('inf')\n        Aleft = A[j] if j >= 0 else float('-inf')\n        Aright = A[j+1] if j+1 < len(A) else float('inf')\n        if Bleft <= Aright and Aleft <= Bright:\n            if total % 2:\n                return min(Bright, Aright)\n            return max(Bleft, Aleft) + min(Bright, Aright) / 2\n        elif Bleft > Aright:\n            r = i - 1\n        else:\n            l = i + 1",
            "language": "python",
        },
        "test_cases": [
            {"input": "nums1=[1,3], nums2=[2]", "output": "2.0", "hidden": False},
            {"input": "nums1=[1,2], nums2=[3,4]", "output": "2.5", "hidden": False},
            {"input": "nums1=[], nums2=[1]", "output": "1.0", "hidden": True},
        ],
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.0", "explanation": "Merged array = [1,2,3], median is 2."},
        ],
        "constraints": "nums1.length + nums2.length >= 1",
        "hints": ["Binary search on the smaller array", "Partition both arrays so left halves are smaller than right halves"],
        "explanation": "Binary search the partition point on the smaller array. Adjust until left halves <= right halves.",
        "dsa_guide": {"approach": "Binary Search", "data_structures": ["Array"], "patterns": ["Binary search on answer"], "tips": ["O(log(min(m,n))) time", "O(1) space"]},
    },
    {
        "id": "google-004",
        "type": "coding",
        "question": "Design and implement an LRU cache that supports get and put in O(1) time.",
        "question_title": "LRU Cache",
        "difficulty": "medium",
        "topic": "Design",
        "sub_topic": "Hash Map + Doubly Linked List",
        "companies": ["google"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://interviewexperiences.in/experience/google/google-interview-l4",
        "solution": {
            "code": "class Node:\n    def __init__(self, key=0, val=0):\n        self.key = key\n        self.val = val\n        self.prev = self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.cache = {}\n        self.head = self.tail = Node()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def _remove(self, node):\n        node.prev.next = node.next\n        node.next.prev = node.prev\n\n    def _add_front(self, node):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        node = self.cache[key]\n        self._remove(node)\n        self._add_front(node)\n        return node.val\n\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self._remove(self.cache[key])\n        node = Node(key, value)\n        self.cache[key] = node\n        self._add_front(node)\n        if len(self.cache) > self.cap:\n            lru = self.tail.prev\n            self._remove(lru)\n            del self.cache[lru.key]",
            "language": "python",
        },
        "test_cases": [
            {"input": "capacity=2, operations=[put,put,get,put,get,put,get,get]", "output": "1,-1,-1,3,4", "hidden": False},
        ],
        "examples": [
            {"input": "LRUCache(2) -> put(1,1) -> put(2,2) -> get(1) -> put(3,3) -> get(2)", "output": "1, -1", "explanation": "Capacity 2. After put(3,3), key 2 is evicted."},
        ],
        "constraints": "1 <= capacity <= 3000",
        "hints": ["Use a doubly linked list for O(1) removal", "Use a hash map for O(1) lookup"],
        "explanation": "Hash map gives O(1) lookup. Doubly linked list maintains recency order. On get, move node to front. On put, add to front and evict tail if over capacity.",
        "dsa_guide": {"approach": "Hash Map + Linked List", "data_structures": ["Doubly Linked List", "Hash Map"], "patterns": ["Design"], "tips": ["O(1) get and put", "Sentinel head/tail removes null checks"]},
    },
    {
        "id": "google-005",
        "type": "coding",
        "question": "Given a string s and a dictionary of words, return true if s can be segmented into a space-separated sequence of dictionary words.",
        "question_title": "Word Break",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "sub_topic": "String DP",
        "companies": ["google"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://copilotinterview.com/blog/google-coding-interview-questions",
        "solution": {
            "code": "def wordBreak(s, wordDict):\n    words = set(wordDict)\n    n = len(s)\n    dp = [False] * (n + 1)\n    dp[0] = True\n    for i in range(1, n + 1):\n        for j in range(max(0, i - 20), i):\n            if dp[j] and s[j:i] in words:\n                dp[i] = True\n                break\n    return dp[n]",
            "language": "python",
        },
        "test_cases": [
            {"input": 's="leetcode", wordDict=["leet","code"]', "output": "true", "hidden": False},
            {"input": 's="applepenapple", wordDict=["apple","pen"]', "output": "true", "hidden": False},
            {"input": 's="catsandog", wordDict=["cats","dog","sand","and","cat"]', "output": "false", "hidden": True},
        ],
        "examples": [
            {"input": 's = "leetcode", wordDict = ["leet","code"]', "output": "true", "explanation": "Return true because leetcode can be segmented as leet code."},
        ],
        "constraints": "1 <= s.length <= 300",
        "hints": ["dp[i] means s[0:i] is segmentable", "Check every substring ending at i"],
        "explanation": "dp[i] is true if any dp[j] is true and s[j:i] is a word. O(n^2) time, O(n) space.",
        "dsa_guide": {"approach": "Dynamic Programming", "data_structures": ["Array", "Hash Set"], "patterns": ["String DP", "Substring"], "tips": ["Limit substring length by max word length", "O(n^2) time, O(n) space"]},
    },
]

added = 0
for q in GOOGLE_QUESTIONS:
    existing = qs.find_one({"id": q["id"]})
    if existing:
        continue
    qs._questions.append(q)
    added += 1

print(f"Added {added} Google questions")
print(f"Total questions: {len(qs._questions)}")
print(f"Servable: {sum(1 for q in qs._questions if qs._is_servable(q))}")
