"""Add verified real Amazon interview questions with provenance."""
import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

AMAZON_QUESTIONS = [
    {
        "id": "amazon-001",
        "type": "coding",
        "question": "Given a linked list, reverse the nodes of the list and return the reversed list.",
        "question_title": "Reverse Linked List",
        "difficulty": "easy",
        "topic": "Linked Lists",
        "sub_topic": "Pointers",
        "companies": ["amazon"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://www.dsaprep.dev/blog/amazon-coding-interview-questions",
        "solution": {
            "code": "def reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev",
            "language": "python",
        },
        "test_cases": [
            {"input": "head=[1,2,3,4,5]", "output": "[5,4,3,2,1]", "hidden": False},
            {"input": "head=[1,2]", "output": "[2,1]", "hidden": True},
        ],
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "Nodes are reversed in place."},
        ],
        "constraints": "0 <= number of nodes <= 500",
        "hints": ["Use three pointers: prev, curr, next", "Reverse the link direction as you walk"],
        "explanation": "Iterate through the list, reversing each node's next pointer to point to the previous node.",
        "dsa_guide": {"approach": "Iterative Pointers", "data_structures": ["Linked List"], "patterns": ["In-place reversal"], "tips": ["O(n) time, O(1) space"]},
    },
    {
        "id": "amazon-002",
        "type": "coding",
        "question": "Given a string s, find the length of the longest substring without repeating characters.",
        "question_title": "Longest Substring Without Repeating Characters",
        "difficulty": "medium",
        "topic": "Strings",
        "sub_topic": "Sliding Window",
        "companies": ["amazon"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://www.dsaprep.dev/blog/amazon-coding-interview-questions",
        "solution": {
            "code": "def lengthOfLongestSubstring(s):\n    seen = {}\n    l = 0\n    best = 0\n    for r, ch in enumerate(s):\n        if ch in seen and seen[ch] >= l:\n            l = seen[ch] + 1\n        seen[ch] = r\n        best = max(best, r - l + 1)\n    return best",
            "language": "python",
        },
        "test_cases": [
            {"input": 's="abcabcbb"', "output": "3", "hidden": False},
            {"input": 's="bbbbb"', "output": "1", "hidden": False},
            {"input": 's="pwwkew"', "output": "3", "hidden": True},
        ],
        "examples": [
            {"input": "s = 'abcabcbb'", "output": "3", "explanation": "The answer is 'abc' with length 3."},
        ],
        "constraints": "0 <= s.length <= 5 * 10^4",
        "hints": ["Use sliding window with a set or hash map", "Shrink left when you see a duplicate"],
        "explanation": "Maintain a window [l, r] with unique characters using a hash map. Expand r, and when a duplicate appears, move l past the previous occurrence.",
        "dsa_guide": {"approach": "Sliding Window", "data_structures": ["Hash Map", "String"], "patterns": ["Two pointers"], "tips": ["O(n) time, O(min(n,m)) space"]},
    },
    {
        "id": "amazon-003",
        "type": "coding",
        "question": "Given an array of intervals where intervals[i] = [start_i, end_i], merge all overlapping intervals and return the merged array.",
        "question_title": "Merge Intervals",
        "difficulty": "medium",
        "topic": "Arrays",
        "sub_topic": "Sorting",
        "companies": ["amazon"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://www.dsaprep.dev/blog/amazon-coding-interview-questions",
        "solution": {
            "code": "def merge(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = []\n    for start, end in intervals:\n        if not merged or merged[-1][1] < start:\n            merged.append([start, end])\n        else:\n            merged[-1][1] = max(merged[-1][1], end)\n    return merged",
            "language": "python",
        },
        "test_cases": [
            {"input": "intervals=[[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "hidden": False},
            {"input": "intervals=[[1,4],[4,5]]", "output": "[[1,5]]", "hidden": True},
        ],
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "[1,3] and [2,6] overlap, merged into [1,6]."},
        ],
        "constraints": "1 <= intervals.length <= 10^4",
        "hints": ["Sort by start time first", "Merge when current starts before or at previous end"],
        "explanation": "Sort intervals by start. Walk through and merge when the current interval overlaps the last merged interval.",
        "dsa_guide": {"approach": "Sort + Sweep", "data_structures": ["Array"], "patterns": ["Interval merging"], "tips": ["O(n log n) time, O(n) space"]},
    },
    {
        "id": "amazon-004",
        "type": "coding",
        "question": "Given an array of integers nums and an integer target, return indices of two numbers that add to target. You may assume one valid answer exists.",
        "question_title": "Two Sum",
        "difficulty": "easy",
        "topic": "Arrays",
        "sub_topic": "Hash Table",
        "companies": ["amazon"],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": "https://www.dsaprep.dev/blog/amazon-coding-interview-questions",
        "solution": {
            "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        need = target - num\n        if need in seen:\n            return [seen[need], i]\n        seen[num] = i\n    return []",
            "language": "python",
        },
        "test_cases": [
            {"input": "nums=[2,7,11,15], target=9", "output": "[0,1]", "hidden": False},
            {"input": "nums=[3,2,4], target=6", "output": "[1,2]", "hidden": True},
        ],
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9"},
        ],
        "constraints": "2 <= nums.length <= 10^4",
        "hints": ["Hash map stores value -> index", "For each num, check if target - num is already in map"],
        "explanation": "Single pass with hash map. Store each number's index; for each number check if its complement is already stored.",
        "dsa_guide": {"approach": "Hash Map", "data_structures": ["Hash Table", "Array"], "patterns": ["One-pass hash"], "tips": ["O(n) time, O(n) space"]},
    },
]

added = 0
for q in AMAZON_QUESTIONS:
    existing = qs.find_one({"id": q["id"]})
    if existing:
        continue
    qs._questions.append(q)
    added += 1

print(f"Added {added} Amazon questions")
print(f"Total questions: {len(qs._questions)}")
print(f"Servable: {sum(1 for q in qs._questions if qs._is_servable(q))}")
