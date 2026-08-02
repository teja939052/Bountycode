"""
Multiplayer Coding Battles — CodinGame-style matchmaking, timed competitions,
and three battle modes (fastest, shortest, reverse). Polling-based (no WebSocket).
"""
from datetime import datetime, timezone, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import battles_collection, users_collection

router = APIRouter(prefix="/api/v1/battles", tags=["battles"])

# ─── 30 Battle Problems ───────────────────────────────────────────────

BATTLE_PROBLEMS = [
    {   # 1
        "title": "Reverse String",
        "description": "Write a function that takes a string and returns it reversed.",
        "examples": [{"input": '"hello"', "output": '"olleh"'}, {"input": '"world"', "output": '"dlrow"'}],
        "test_cases": [{"input": '"hello"', "expected": "olleh"}, {"input": '"racecar"', "expected": "racecar"}, {"input": '"12345"', "expected": "54321"}],
        "starter_code": "def reverse_string(s: str) -> str:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest", "reverse"],
    },
    {   # 2
        "title": "FizzBuzz",
        "description": "Return an array where for numbers 1 to n: 'FizzBuzz' if divisible by 15, 'Fizz' if by 3, 'Buzz' if by 5, else the number as string.",
        "examples": [{"input": "5", "output": '["1","2","Fizz","4","Buzz"]'}, {"input": "15", "output": '["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]'}],
        "test_cases": [{"input": "5", "expected": '["1","2","Fizz","4","Buzz"]'}, {"input": "3", "expected": '["1","2","Fizz"]'}, {"input": "15", "expected": '["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]'}],
        "starter_code": "def fizzbuzz(n: int) -> list:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 3
        "title": "Palindrome Check",
        "description": "Check if a given string is a palindrome (reads same forwards and backwards). Ignore case and non-alphanumeric characters.",
        "examples": [{"input": '"A man a plan a canal Panama"', "output": "true"}, {"input": '"hello"', "output": "false"}],
        "test_cases": [{"input": '"racecar"', "expected": "True"}, {"input": '"hello"', "expected": "False"}, {"input": '"A man a plan a canal Panama"', "expected": "True"}],
        "starter_code": "def is_palindrome(s: str) -> bool:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest", "reverse"],
    },
    {   # 4
        "title": "Two Sum",
        "description": "Given an array of integers and a target, return indices of the two numbers that add up to target. Assume exactly one solution.",
        "examples": [{"input": "[2,7,11,15], 9", "output": "[0,1]"}, {"input": "[3,2,4], 6", "output": "[1,2]"}],
        "test_cases": [{"input": "[2,7,11,15], 9", "expected": "[0,1]"}, {"input": "[3,2,4], 6", "expected": "[1,2]"}, {"input": "[3,3], 6", "expected": "[0,1]"}],
        "starter_code": "def two_sum(nums: list, target: int) -> list:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest", "reverse"],
    },
    {   # 5
        "title": "Max of Array",
        "description": "Find the maximum element in an array of integers.",
        "examples": [{"input": "[1, 5, 3, 9, 2]", "output": "9"}, {"input": "[-5, -2, -10]", "output": "-2"}],
        "test_cases": [{"input": "[1, 5, 3, 9, 2]", "expected": "9"}, {"input": "[-5, -2, -10]", "expected": "-2"}, {"input": "[100]", "expected": "100"}],
        "starter_code": "def find_max(nums: list) -> int:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 6
        "title": "Factorial",
        "description": "Compute the factorial of a non-negative integer n (n!).",
        "examples": [{"input": "5", "output": "120"}, {"input": "0", "output": "1"}],
        "test_cases": [{"input": "5", "expected": "120"}, {"input": "0", "expected": "1"}, {"input": "10", "expected": "3628800"}],
        "starter_code": "def factorial(n: int) -> int:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 7
        "title": "Fibonacci",
        "description": "Return the nth Fibonacci number (0-indexed: F(0)=0, F(1)=1).",
        "examples": [{"input": "6", "output": "8"}, {"input": "0", "output": "0"}],
        "test_cases": [{"input": "0", "expected": "0"}, {"input": "1", "expected": "1"}, {"input": "6", "expected": "8"}, {"input": "10", "expected": "55"}],
        "starter_code": "def fibonacci(n: int) -> int:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 8
        "title": "Anagram Check",
        "description": "Check if two strings are anagrams (contain the same characters in any order).",
        "examples": [{"input": '"listen", "silent"', "output": "true"}, {"input": '"hello", "world"', "output": "false"}],
        "test_cases": [{"input": "('listen', 'silent')", "expected": "True"}, {"input": "('hello', 'world')", "expected": "False"}, {"input": "('anagram', 'nagaram')", "expected": "True"}],
        "starter_code": "def is_anagram(s: str, t: str) -> bool:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest", "reverse"],
    },
    {   # 9
        "title": "Count Vowels",
        "description": "Count the number of vowels (a, e, i, o, u) in a string. Case-insensitive.",
        "examples": [{"input": '"hello world"', "output": "3"}, {"input": '"AEIOU"', "output": "5"}],
        "test_cases": [{"input": "'hello world'", "expected": "3"}, {"input": "'AEIOU'", "expected": "5"}, {"input": "'xyz'", "expected": "0"}],
        "starter_code": "def count_vowels(s: str) -> int:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 10
        "title": "Array Sum",
        "description": "Return the sum of all elements in an array.",
        "examples": [{"input": "[1, 2, 3, 4, 5]", "output": "15"}, {"input": "[-1, 0, 1]", "output": "0"}],
        "test_cases": [{"input": "[1, 2, 3, 4, 5]", "expected": "15"}, {"input": "[-1, 0, 1]", "expected": "0"}, {"input": "[42]", "expected": "42"}],
        "starter_code": "def array_sum(nums: list) -> int:\n    # Your code here\n    pass",
        "difficulty": "easy",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 11
        "title": "Valid Parentheses",
        "description": "Given a string containing '(){}[]', determine if brackets are balanced and correctly nested.",
        "examples": [{"input": '"()"', "output": "true"}, {"input": '"([)]"', "output": "false"}, {"input": '"{[]}"', "output": "true"}],
        "test_cases": [{"input": "'()'", "expected": "True"}, {"input": "'([)]'", "expected": "False"}, {"input": "'{[]}'", "expected": "True"}, {"input": "'('", "expected": "False"}],
        "starter_code": "def is_valid_parentheses(s: str) -> bool:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 12
        "title": "Binary Search",
        "description": "Given a sorted array of integers and a target, return the index of target or -1 if not found.",
        "examples": [{"input": "[-1,0,3,5,9,12], 9", "output": "4"}, {"input": "[-1,0,3,5,9,12], 2", "output": "-1"}],
        "test_cases": [{"input": "([-1,0,3,5,9,12], 9)", "expected": "4"}, {"input": "([-1,0,3,5,9,12], 2)", "expected": "-1"}, {"input": "([5], 5)", "expected": "0"}],
        "starter_code": "def binary_search(nums: list, target: int) -> int:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 13
        "title": "Merge Intervals",
        "description": "Given an array of intervals [start, end], merge all overlapping intervals and return the merged intervals.",
        "examples": [{"input": "[[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"}, {"input": "[[1,4],[4,5]]", "output": "[[1,5]]"}],
        "test_cases": [{"input": "[[1,3],[2,6],[8,10],[15,18]]", "expected": "[[1,6],[8,10],[15,18]]"}, {"input": "[[1,4],[4,5]]", "expected": "[[1,5]]"}, {"input": "[[1,4],[2,3]]", "expected": "[[1,4]]"}],
        "starter_code": "def merge_intervals(intervals: list) -> list:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 14
        "title": "Group Anagrams",
        "description": "Given an array of strings, group the anagrams together. Return sorted groups with sorted strings.",
        "examples": [{"input": '["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]'}],
        "test_cases": [{"input": "['eat','tea','tan','ate','nat','bat']", "expected": "[['bat'],['nat','tan'],['ate','eat','tea']]"}],
        "starter_code": "def group_anagrams(words: list) -> list:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 15
        "title": "Longest Substring Without Repeating Characters",
        "description": "Given a string, find the length of the longest substring without repeating characters.",
        "examples": [{"input": '"abcabcbb"', "output": "3"}, {"input": '"bbbbb"', "output": "1"}, {"input": '"pwwkew"', "output": "3"}],
        "test_cases": [{"input": "'abcabcbb'", "expected": "3"}, {"input": "'bbbbb'", "expected": "1"}, {"input": "'pwwkew'", "expected": "3"}, {"input": "''", "expected": "0"}],
        "starter_code": "def longest_substring(s: str) -> int:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 16
        "title": "Product of Array Except Self",
        "description": "Return an array where result[i] = product of all elements except nums[i]. Do not use division.",
        "examples": [{"input": "[1,2,3,4]", "output": "[24,12,8,6]"}, {"input": "[-1,1,0,-3,3]", "output": "[0,0,9,0,0]"}],
        "test_cases": [{"input": "[1,2,3,4]", "expected": "[24,12,8,6]"}, {"input": "[-1,1,0,-3,3]", "expected": "[0,0,9,0,0]"}],
        "starter_code": "def product_except_self(nums: list) -> list:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 17
        "title": "Find All Duplicates",
        "description": "Find all elements that appear twice in an array of integers where each element is in range [1, n].",
        "examples": [{"input": "[4,3,2,7,8,2,3,1]", "output": "[2,3]"}, {"input": "[1,1,2]", "output": "[1]"}],
        "test_cases": [{"input": "[4,3,2,7,8,2,3,1]", "expected": "[2,3]"}, {"input": "[1,1,2]", "expected": "[1]"}, {"input": "[1,2,3]", "expected": "[]"}],
        "starter_code": "def find_duplicates(nums: list) -> list:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 18
        "title": "Container With Most Water",
        "description": "Given array heights where each element is a vertical line, find two lines that together form a container holding the most water.",
        "examples": [{"input": "[1,8,6,2,5,4,8,3,7]", "output": "49"}, {"input": "[1,1]", "output": "1"}],
        "test_cases": [{"input": "[1,8,6,2,5,4,8,3,7]", "expected": "49"}, {"input": "[1,1]", "expected": "1"}, {"input": "[4,3,2,1,4]", "expected": "16"}],
        "starter_code": "def max_area(heights: list) -> int:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 19
        "title": "Rotate Array",
        "description": "Rotate an array to the right by k steps (k is non-negative). Modify in-place.",
        "examples": [{"input": "[1,2,3,4,5,6,7], 3", "output": "[5,6,7,1,2,3,4]"}, {"input": "[-1,-100,3,99], 2", "output": "[3,99,-1,-100]"}],
        "test_cases": [{"input": "([1,2,3,4,5,6,7], 3)", "expected": "[5,6,7,1,2,3,4]"}, {"input": "([-1,-100,3,99], 2)", "expected": "[3,99,-1,-100]"}],
        "starter_code": "def rotate_array(nums: list, k: int) -> list:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 20
        "title": "Valid Sudoku",
        "description": "Determine if a 9x9 Sudoku board is valid. Each row, column, and 3x3 sub-box must contain digits 1-9 without repetition.",
        "examples": [{"input": "board", "output": "true (valid board)"}],
        "test_cases": [{"input": "[['5','3','.','.','7','.','.','.','.'],['6','.','.','1','9','5','.','.','.'],['.','9','8','.','.','.','.','6','.'],['8','.','.','.','6','.','.','.','3'],['4','.','.','8','.','3','.','.','1'],['7','.','.','.','2','.','.','.','6'],['.','6','.','.','.','.','2','8','.'],['.','.','.','4','1','9','.','.','5'],['.','.','.','.','8','.','.','7','9']]", "expected": "True"}],
        "starter_code": "def is_valid_sudoku(board: list) -> bool:\n    # Your code here\n    pass",
        "difficulty": "medium",
        "mode_suitability": ["fastest"],
    },
    {   # 21
        "title": "LRU Cache",
        "description": "Implement a Least Recently Used (LRU) cache with get(key) and put(key, value) operations. Cache has fixed capacity. When full, evict the least recently used item.",
        "examples": [{"input": "capacity=2, put(1,1), put(2,2), get(1)=1, put(3,3) evicts key 2, get(2)=-1", "output": "LRU behavior verified"}],
        "test_cases": [{"input": "2, [1,1], [2,2], [1], [3,3], [2], [4,4], [1], [3], [4]", "expected": "[None,None,1,None,-1,None,-1,3,4]"}],
        "starter_code": "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n    def get(self, key: int) -> int:\n        pass\n    def put(self, key: int, value: int) -> None:\n        pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest"],
    },
    {   # 22
        "title": "Median of Two Sorted Arrays",
        "description": "Given two sorted arrays nums1 and nums2, return the median of the combined sorted array. O(log(m+n)) time.",
        "examples": [{"input": "[1,3], [2]", "output": "2.0"}, {"input": "[1,2], [3,4]", "output": "2.5"}],
        "test_cases": [{"input": "([1,3], [2])", "expected": "2.0"}, {"input": "([1,2], [3,4])", "expected": "2.5"}, {"input": "([0,0], [0,0])", "expected": "0.0"}],
        "starter_code": "def find_median_sorted(nums1: list, nums2: list) -> float:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest"],
    },
    {   # 23
        "title": "Regular Expression Matching",
        "description": "Implement regex matching with '.' (any char) and '*' (zero or more of preceding element). Must match the entire string.",
        "examples": [{"input": '"aa", "a"', "output": "false"}, {"input": '"aa", "a*"', "output": "true"}, {"input": '"ab", ".*"', "output": "true"}],
        "test_cases": [{"input": "('aa', 'a')", "expected": "False"}, {"input": "('aa', 'a*')", "expected": "True"}, {"input": "('ab', '.*')", "expected": "True"}, {"input": "('mississippi', 'mis*is*p*.')", "expected": "False"}],
        "starter_code": "def is_match(s: str, p: str) -> bool:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest"],
    },
    {   # 24
        "title": "Trapping Rain Water",
        "description": "Given n non-negative integers representing elevation map, compute how much water it can trap after raining.",
        "examples": [{"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"}, {"input": "[4,2,0,3,2,5]", "output": "9"}],
        "test_cases": [{"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected": "6"}, {"input": "[4,2,0,3,2,5]", "expected": "9"}, {"input": "[1,0,1]", "expected": "1"}],
        "starter_code": "def trap_rain_water(height: list) -> int:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 25
        "title": "Merge K Sorted Lists",
        "description": "Given k sorted arrays, merge them into one sorted array.",
        "examples": [{"input": "[[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]"}],
        "test_cases": [{"input": "[[1,4,5],[1,3,4],[2,6]]", "expected": "[1,1,2,3,4,4,5,6]"}, {"input": "[[1,2],[3,4],[5,6]]", "expected": "[1,2,3,4,5,6]"}],
        "starter_code": "def merge_k_sorted(lists: list) -> list:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 26
        "title": "Longest Palindromic Substring",
        "description": "Given a string, return the longest palindromic substring.",
        "examples": [{"input": '"babad"', "output": '"bab"'}, {"input": '"cbbd"', "output": '"bb"'}],
        "test_cases": [{"input": "'babad'", "expected": "'bab'"}, {"input": "'cbbd'", "expected": "'bb'"}, {"input": "'a'", "expected": "'a'"}, {"input": "'ac'", "expected": "'a'"}],
        "starter_code": "def longest_palindrome(s: str) -> str:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 27
        "title": "Sliding Window Maximum",
        "description": "Given an array and window size k, return the maximum element in each sliding window.",
        "examples": [{"input": "[1,3,-1,-3,5,3,6,7], 3", "output": "[3,3,5,5,6,7]"}, {"input": "[1], 1", "output": "[1]"}],
        "test_cases": [{"input": "([1,3,-1,-3,5,3,6,7], 3)", "expected": "[3,3,5,5,6,7]"}, {"input": "([1], 1)", "expected": "[1]"}, {"input": "([1,-1], 1)", "expected": "[1,-1]"}],
        "starter_code": "def max_sliding_window(nums: list, k: int) -> list:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest", "shortest"],
    },
    {   # 28
        "title": "Minimum Window Substring",
        "description": "Given two strings s and t, return the minimum window substring of s that contains all characters of t.",
        "examples": [{"input": '"ADOBECODEBANC", "ABC"', "output": '"BANC"'}, {"input": '"a", "a"', "output": '"a"'}],
        "test_cases": [{"input": "('ADOBECODEBANC', 'ABC')", "expected": "'BANC'"}, {"input": "('a', 'a')", "expected": "'a'"}, {"input": "('a', 'aa')", "expected": "''"}],
        "starter_code": "def min_window(s: str, t: str) -> str:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest"],
    },
    {   # 29
        "title": "Word Ladder",
        "description": "Given beginWord, endWord, and a word list, return the length of the shortest transformation sequence from beginWord to endWord. Each step changes one letter.",
        "examples": [{"input": '"hit", "cog", ["hot","dot","dog","lot","log","cog"]', "output": "5"}, {"input": '"hit", "cog", ["hot","dot","dog","lot","log"]', "output": "0"}],
        "test_cases": [{"input": "('hit', 'cog', ['hot','dot','dog','lot','log','cog'])", "expected": "5"}, {"input": "('hit', 'cog', ['hot','dot','dog','lot','log'])", "expected": "0"}],
        "starter_code": "def word_ladder(begin: str, end: str, words: list) -> int:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest"],
    },
    {   # 30
        "title": "Largest Rectangle in Histogram",
        "description": "Given an array of bar heights, find the largest rectangle that can be formed in the histogram.",
        "examples": [{"input": "[2,1,5,6,2,3]", "output": "10"}, {"input": "[2,4]", "output": "4"}],
        "test_cases": [{"input": "[2,1,5,6,2,3]", "expected": "10"}, {"input": "[2,4]", "expected": "4"}, {"input": "[1,2,3,4,5]", "expected": "9"}],
        "starter_code": "def largest_rectangle(heights: list) -> int:\n    # Your code here\n    pass",
        "difficulty": "hard",
        "mode_suitability": ["fastest", "shortest"],
    },
]

# ─── Helpers ────────────────────────────────────────────────────────────

def _select_problem(difficulty: str, mode: str) -> dict:
    pool = [p for p in BATTLE_PROBLEMS if p["difficulty"] == difficulty and mode in p["mode_suitability"]]
    if not pool:
        pool = [p for p in BATTLE_PROBLEMS if mode in p["mode_suitability"]]
    if not pool:
        pool = BATTLE_PROBLEMS
    return random.choice(pool)


def _calculate_score(mode: str, passed: int, total: int, time_ms: int, code: str, time_limit_ms: int) -> float:
    correctness = (passed / total) * 100 if total > 0 else 0
    if mode == "fastest":
        time_ratio = time_ms / time_limit_ms if time_limit_ms > 0 else 1
        speed_bonus = max(0, (1 - time_ratio) * 30)
        return round(correctness + speed_bonus, 1)
    if mode == "shortest":
        length_penalty = max(0, (len(code) - 50) / 500) * 20
        return round(max(0, correctness - length_penalty), 1)
    return round(correctness, 1)


async def _run_test_cases(code: str, test_cases: list, language: str = "python"):
    from app.services.code_executor import CodeExecutionEngine
    engine = CodeExecutionEngine()
    passed = 0
    total = len(test_cases)
    for tc in test_cases:
        try:
            result = await engine.execute_code(code, language, tc.get("input", ""), timeout=5)
            if result["success"]:
                actual = result["stdout"].strip()
                expected = tc["expected"].strip()
                if actual == expected:
                    passed += 1
        except Exception:
            pass
    return passed, total


# ─── In-Memory Matchmaking Queue ──────────────────────────────────────

import asyncio

_queue_lock = asyncio.Lock()
_queued_users = {}  # user_id -> { mode, difficulty, language, joined_at }
_matched_users = {}  # user_id -> battle_id (for matched users to discover via poll)


# ─── Routes ────────────────────────────────────────────────────────────

@router.post("/queue")
async def join_queue(
    mode: str = Query("fastest", regex="^(fastest|shortest|reverse)$"),
    difficulty: str = Query("easy", regex="^(easy|medium|hard)$"),
    language: str = Query("python", min_length=1, max_length=20),
    user=Depends(get_current_user),
):
    """Join matchmaking queue. If matching opponent found, creates and returns battle."""
    uid = user["id"]

    async with _queue_lock:
        # Check if already in queue
        if uid in _queued_users:
            raise HTTPException(status_code=400, detail="Already in queue")

        # Find matching opponent
        match_key = (mode, difficulty, language)
        opponent_id = None
        for q_uid, q_data in list(_queued_users.items()):
            if q_uid == uid:
                continue
            if (q_data["mode"], q_data["difficulty"], q_data["language"]) == match_key:
                opponent_id = q_uid
                break

        if opponent_id:
            p1_id, p2_id = uid, opponent_id
            if random.random() < 0.5:
                p1_id, p2_id = opponent_id, uid

            problem = _select_problem(difficulty, mode)
            now = datetime.now(timezone.utc)

            battle = {
                "player1_id": ObjectId(p1_id),
                "player2_id": ObjectId(p2_id),
                "status": "in_progress",
                "mode": mode,
                "difficulty": difficulty,
                "problem": problem,
                "player1_code": None,
                "player2_code": None,
                "player1_score": None,
                "player2_score": None,
                "player1_time_ms": None,
                "player2_time_ms": None,
                "winner_id": None,
                "created_at": now,
                "started_at": now,
                "completed_at": None,
                "time_limit_seconds": 900,
            }
            result = await battles_collection().insert_one(battle)
            battle_id = str(result.inserted_id)
            del _queued_users[uid]
            del _queued_users[opponent_id]
            _matched_users[uid] = battle_id
            _matched_users[opponent_id] = battle_id

            return {
                "matched": True,
                "battle_id": battle_id,
                "battle": {**battle, "_id": battle_id, "player1_id": str(p1_id), "player2_id": str(p2_id)},
            }

        _queued_users[uid] = {
            "mode": mode,
            "difficulty": difficulty,
            "language": language,
            "joined_at": datetime.now(timezone.utc),
        }
        return {"matched": False, "message": "Added to queue"}


@router.get("/queue/status")
async def queue_status(user=Depends(get_current_user)):
    """Check queue status: in_queue, position, or matched battle_id."""
    uid = user["id"]
    async with _queue_lock:
        if uid in _matched_users:
            battle_id = _matched_users.pop(uid)
            return {"in_queue": False, "matched": True, "battle_id": battle_id}
        if uid not in _queued_users:
            return {"in_queue": False, "position": 0, "matched": False}
        data = _queued_users[uid]
        position = 1
        for q_uid, q_data in list(_queued_users.items()):
            if q_uid == uid:
                break
            if (q_data["mode"], q_data["difficulty"], q_data["language"]) == (data["mode"], data["difficulty"], data["language"]):
                position += 1
        return {"in_queue": True, "position": position, **data, "matched": False}


@router.get("/history")
async def get_battle_history(user=Depends(get_current_user)):
    """User's battle history with win/loss record."""
    uid = user["id"]
    collection = battles_collection()
    cursor = collection.find({
        "$or": [{"player1_id": ObjectId(uid)}, {"player2_id": ObjectId(uid)}],
    }).sort("created_at", -1).limit(50)

    battles_list = []
    wins = 0
    losses = 0
    async for b in cursor:
        is_p1 = str(b["player1_id"]) == uid
        opp_id = b["player2_id"] if is_p1 else b["player1_id"]

        opp_user = await users_collection().find_one({"_id": opp_id})
        opp_name = opp_user.get("name", "Unknown") if opp_user else "Unknown"

        my_score = b.get("player1_score") if is_p1 else b.get("player2_score")
        opp_score = b.get("player2_score") if is_p1 else b.get("player1_score")

        won = False
        if b.get("winner_id") and str(b["winner_id"]) == uid:
            won = True
            wins += 1
        elif b.get("winner_id") and str(b["winner_id"]) != uid:
            losses += 1

        battles_list.append({
            "battle_id": str(b["_id"]),
            "mode": b["mode"],
            "difficulty": b["difficulty"],
            "status": b["status"],
            "opponent_name": opp_name,
            "my_score": my_score,
            "opponent_score": opp_score,
            "won": won if b["status"] == "completed" else None,
            "created_at": b["created_at"],
            "completed_at": b.get("completed_at"),
        })

    return {
        "battles": battles_list,
        "stats": {
            "total": len(battles_list),
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / max(1, wins + losses) * 100, 1) if wins + losses > 0 else 0,
        },
    }


@router.get("/leaderboard")
async def get_battle_leaderboard(limit: int = Query(20, ge=1, le=100)):
    """Battle leaderboard by wins, win rate, total battles."""
    collection = battles_collection()
    pipeline = [
        {"$match": {"status": "completed"}},
        {"$project": {
            "winner_str": {"$toString": "$winner_id"},
            "p1_str": {"$toString": "$player1_id"},
            "p2_str": {"$toString": "$player2_id"},
        }},
        {"$group": {
            "_id": "$winner_str",
            "wins": {"$sum": 1},
        }},
        {"$sort": {"wins": -1}},
        {"$limit": limit},
    ]
    leaderboard = []
    async for doc in collection.aggregate(pipeline):
        uid = doc["_id"]
        if not uid:
            continue
        total_battles = await collection.count_documents({
            "$or": [{"player1_id": ObjectId(uid)}, {"player2_id": ObjectId(uid)}],
            "status": "completed",
        })
        user_doc = await users_collection().find_one({"_id": ObjectId(uid)})
        leaderboard.append({
            "user_id": uid,
            "name": user_doc.get("name", "Unknown") if user_doc else "Unknown",
            "wins": doc["wins"],
            "total_battles": total_battles,
            "win_rate": round(doc["wins"] / max(1, total_battles) * 100, 1),
        })

    return {"leaderboard": leaderboard}


@router.post("/{battle_id}/submit")
async def submit_code(
    battle_id: str,
    code: str = Query(..., min_length=1, max_length=50000),
    user=Depends(get_current_user),
):
    """Submit code for a battle. Records time, runs test cases, calculates score."""
    try:
        b_oid = ObjectId(battle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid battle ID")

    collection = battles_collection()
    battle = await collection.find_one({"_id": b_oid})
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    if battle["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Battle is not in progress")

    uid = user["id"]
    p1_id = str(battle["player1_id"])
    p2_id = str(battle["player2_id"])
    if uid not in (p1_id, p2_id):
        raise HTTPException(status_code=403, detail="Not a participant")

    now = datetime.now(timezone.utc)
    started = battle["started_at"]
    time_ms = int((now - started).total_seconds() * 1000) if started else 0
    time_limit_ms = battle["time_limit_seconds"] * 1000

    if time_ms > time_limit_ms:
        raise HTTPException(status_code=400, detail="Time limit exceeded")

    test_cases = battle["problem"]["test_cases"]
    passed, total = await _run_test_cases(code, test_cases)
    score = _calculate_score(battle["mode"], passed, total, time_ms, code, time_limit_ms)

    field_key = "1" if uid == p1_id else "2"
    update = {
        f"player{field_key}_code": code,
        f"player{field_key}_score": score,
        f"player{field_key}_time_ms": time_ms,
    }

    await collection.update_one({"_id": b_oid}, {"$set": update})

    battle = await collection.find_one({"_id": b_oid})
    p1_done = battle.get("player1_score") is not None
    p2_done = battle.get("player2_score") is not None

    winner_id = None
    if p1_done and p2_done:
        s1 = battle["player1_score"]
        s2 = battle["player2_score"]
        if s1 > s2:
            winner_id = battle["player1_id"]
        elif s2 > s1:
            winner_id = battle["player2_id"]
        else:
            t1 = battle.get("player1_time_ms", 0)
            t2 = battle.get("player2_time_ms", 0)
            winner_id = battle["player1_id"] if t1 < t2 else battle["player2_id"]

        await collection.update_one(
            {"_id": b_oid},
            {"$set": {"status": "completed", "completed_at": now, "winner_id": winner_id}},
        )

    return {
        "passed": passed,
        "total": total,
        "score": score,
        "time_ms": time_ms,
        "opponent_done": p2_done if uid == p1_id else p1_done,
        "winner": str(winner_id) if winner_id else None,
    }


@router.get("/{battle_id}")
async def get_battle(battle_id: str, user=Depends(get_current_user)):
    """Get battle state. Used for polling (every 2s during battle)."""
    try:
        b_oid = ObjectId(battle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid battle ID")

    collection = battles_collection()
    battle = await collection.find_one({"_id": b_oid})
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    uid = user["id"]
    p1_id = str(battle["player1_id"])
    p2_id = str(battle["player2_id"])
    if uid not in (p1_id, p2_id):
        raise HTTPException(status_code=403, detail="Not a participant")

    is_p1 = uid == p1_id
    my_key = "1" if is_p1 else "2"
    opp_key = "2" if is_p1 else "1"
    opp_id = p2_id if is_p1 else p1_id

    now = datetime.now(timezone.utc)
    started = battle["started_at"]
    time_remaining = max(0, battle["time_limit_seconds"] - int((now - started).total_seconds())) if started else 0

    opp_user = await users_collection().find_one({"_id": ObjectId(opp_id)})
    opp_name = opp_user.get("name", "Unknown") if opp_user else "Unknown"

    return {
        "battle_id": battle_id,
        "status": battle["status"],
        "mode": battle["mode"],
        "difficulty": battle["difficulty"],
        "problem": battle["problem"],
        "my_score": battle.get(f"player{my_key}_score"),
        "opponent_score": battle.get(f"player{opp_key}_score"),
        "my_time_ms": battle.get(f"player{my_key}_time_ms"),
        "opponent_time_ms": battle.get(f"player{opp_key}_time_ms"),
        "opponent_name": opp_name,
        "opponent_submitted": battle.get(f"player{opp_key}_score") is not None,
        "my_submitted": battle.get(f"player{my_key}_score") is not None,
        "time_remaining_seconds": time_remaining,
        "time_limit_seconds": battle["time_limit_seconds"],
        "winner_id": str(battle["winner_id"]) if battle["winner_id"] else None,
        "completed_at": battle["completed_at"],
    }


@router.post("/{battle_id}/surrender")
async def surrender_battle(battle_id: str, user=Depends(get_current_user)):
    """Surrender a battle."""
    try:
        b_oid = ObjectId(battle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid battle ID")

    collection = battles_collection()
    battle = await collection.find_one({"_id": b_oid})
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")

    uid = user["id"]
    p1_id = str(battle["player1_id"])
    p2_id = str(battle["player2_id"])
    if uid not in (p1_id, p2_id):
        raise HTTPException(status_code=403, detail="Not a participant")
    if battle["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Battle not in progress")

    winner_id = battle["player2_id"] if uid == p1_id else battle["player1_id"]
    now = datetime.now(timezone.utc)

    await collection.update_one(
        {"_id": b_oid},
        {"$set": {"status": "completed", "completed_at": now, "winner_id": winner_id}},
    )

    return {"status": "completed", "winner_id": str(winner_id), "surrender": True}
