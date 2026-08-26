"""
Seed script: populates curated_questions with a small initial bank.
Run: python backend/seed_questions.py
"""

import asyncio
import random
from datetime import datetime, timezone
from bson import ObjectId

from app.database import get_db, curated_questions_collection
from app.services.cache import cache

COMPANIES = ["Google", "Amazon", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Accenture"]
TYPES = ["coding"]
TOPICS = {
    "coding": ["Arrays", "Strings", "DP", "Graphs", "Trees", "Sliding Window", "Binary Search"],
}
DIFFICULTIES = ["easy", "medium", "hard"]

CODING_PROBLEMS = [
    {
        "question_title": "Two Sum",
        "statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"},
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9", "Only one valid answer exists."],
        "visible_test_cases": [
            {"input": "2 7 11 15\n9", "expected": "[0, 1]"},
            {"input": "3 2 4\n6", "expected": "[1, 2]"},
        ],
        "hidden_test_cases": [
            {"input": "3 3\n6", "expected": "[0, 1]"},
            {"input": "1 5 3 7 9\n12", "expected": "[1, 4]"},
            {"input": "-1 -2 -3 -4 -5\n-8", "expected": "[2, 4]"},
        ],
        "solution": {"approach": "Use a hash map to store seen values and their indices.", "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target - num], i]\n        seen[num] = i"},
        "topics": ["Array", "Hash Table"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Valid Parentheses",
        "statement": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "examples": [
            {"input": "s = \"()\"", "output": "true"},
            {"input": "s = \"()[]{}\"", "output": "true"},
            {"input": "s = \"(]\"", "output": "false"},
        ],
        "constraints": ["1 <= s.length <= 10^4", "s consists of parentheses only '()[]{}'."],
        "visible_test_cases": [
            {"input": "()", "expected": "true"},
            {"input": "()[]{}", "expected": "true"},
            {"input": "(]", "expected": "false"},
        ],
        "hidden_test_cases": [
            {"input": "([)]", "expected": "false"},
            {"input": "((()))", "expected": "true"},
            {"input": "]", "expected": "false"},
            {"input": "", "expected": "true"},
        ],
        "solution": {"approach": "Use a stack. Push opening brackets, pop when matching closing bracket appears.", "code": "def isValid(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            if not stack or stack[-1] != mapping[char]:\n                return False\n            stack.pop()\n        else:\n            stack.append(char)\n    return not stack"},
        "topics": ["String", "Stack"],
        "companies": ["Amazon", "Microsoft", "Meta"],
    },
    {
        "question_title": "Merge Two Sorted Lists",
        "statement": "You are given the heads of two sorted linked lists list1 and list2.\n\nMerge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.\n\nReturn the head of the merged linked list.",
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]"},
            {"input": "list1 = [], list2 = []", "output": "[]"},
        ],
        "constraints": ["The number of nodes in both lists is in the range [0, 50].", "-100 <= Node.val <= 100", "Both list1 and list2 are sorted in non-decreasing order."],
        "visible_test_cases": [
            {"input": "1 2 4\n1 3 4", "expected": "1 1 2 3 4 4"},
            {"input": "\n\n", "expected": ""},
        ],
        "hidden_test_cases": [
            {"input": "1 3 5\n2 4 6", "expected": "1 2 3 4 5 6"},
            {"input": "1\n", "expected": "1"},
            {"input": "\n1 2", "expected": "1 2"},
        ],
        "solution": {"approach": "Use two pointers. Compare nodes and attach the smaller one to the merged list.", "code": "def mergeTwoLists(list1, list2):\n    dummy = ListNode()\n    current = dummy\n    while list1 and list2:\n        if list1.val <= list2.val:\n            current.next = list1\n            list1 = list1.next\n        else:\n            current.next = list2\n            list2 = list2.next\n        current = current.next\n    current.next = list1 or list2\n    return dummy.next"},
        "topics": ["Linked List", "Recursion"],
        "companies": ["Amazon", "Google", "Apple"],
    },
    {
        "question_title": "Maximum Subarray",
        "statement": "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
            {"input": "nums = [1]", "output": "1"},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "-2 1 -3 4 -1 2 1 -5 4", "expected": "6"},
            {"input": "1", "expected": "1"},
        ],
        "hidden_test_cases": [
            {"input": "5 4 -1 7 8", "expected": "23"},
            {"input": "-1", "expected": "-1"},
            {"input": "-2 -1", "expected": "-1"},
        ],
        "solution": {"approach": "Kadane's Algorithm: track current_max and global_max.", "code": "def maxSubArray(nums):\n    current_max = global_max = nums[0]\n    for num in nums[1:]:\n        current_max = max(num, current_max + num)\n        global_max = max(global_max, current_max)\n    return global_max"},
        "topics": ["Array", "DP", "Divide and Conquer"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Climbing Stairs",
        "statement": "You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "1. 1 step + 1 step\n2. 2 steps"},
            {"input": "n = 3", "output": "3"},
        ],
        "constraints": ["1 <= n <= 45"],
        "visible_test_cases": [
            {"input": "2", "expected": "2"},
            {"input": "3", "expected": "3"},
        ],
        "hidden_test_cases": [
            {"input": "1", "expected": "1"},
            {"input": "4", "expected": "5"},
            {"input": "5", "expected": "8"},
            {"input": "10", "expected": "89"},
        ],
        "solution": {"approach": "Fibonacci pattern. dp[i] = dp[i-1] + dp[i-2]", "code": "def climbStairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b"},
        "topics": ["Math", "DP", "Memoization"],
        "companies": ["Amazon", "Google", "TCS"],
    },
    {
        "question_title": "Best Time to Buy and Sell Stock",
        "statement": "You are given an array prices where prices[i] is the price of a given stock on the ith day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5."},
        ],
        "constraints": ["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "7 1 5 3 6 4", "expected": "5"},
            {"input": "7 6 4 3 1", "expected": "0"},
        ],
        "hidden_test_cases": [
            {"input": "1 2", "expected": "1"},
            {"input": "2 1 2 1 2 1 2", "expected": "1"},
            {"input": "3 3 3 3", "expected": "0"},
        ],
        "solution": {"approach": "Track min price so far and max profit.", "code": "def maxProfit(prices):\n    min_price = float('inf')\n    max_profit = 0\n    for price in prices:\n        min_price = min(min_price, price)\n        max_profit = max(max_profit, price - min_price)\n    return max_profit"},
        "topics": ["Array", "DP"],
        "companies": ["Amazon", "Microsoft", "Goldman Sachs"],
    },
    {
        "question_title": "Reverse Linked List",
        "statement": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
        ],
        "constraints": ["The number of nodes in the list is in the range [0, 5000].", "-5000 <= Node.val <= 5000"],
        "visible_test_cases": [
            {"input": "1 2 3 4 5", "expected": "5 4 3 2 1"},
        ],
        "hidden_test_cases": [
            {"input": "1 2", "expected": "2 1"},
            {"input": "1", "expected": "1"},
            {"input": "", "expected": ""},
        ],
        "solution": {"approach": "Iterative: use prev, curr, next pointers.", "code": "def reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        next_temp = curr.next\n        curr.next = prev\n        prev = curr\n        curr = next_temp\n    return prev"},
        "topics": ["Linked List", "Recursion"],
        "companies": ["Amazon", "Apple", "Meta"],
    },
    {
        "question_title": "Binary Search",
        "statement": "Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, return its index. Otherwise, return -1.",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"},
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 < nums[i], target < 10^4", "All integers in nums are unique.", "nums is sorted in ascending order."],
        "visible_test_cases": [
            {"input": "-1 0 3 5 9 12\n9", "expected": "4"},
            {"input": "-1 0 3 5 9 12\n2", "expected": "-1"},
        ],
        "hidden_test_cases": [
            {"input": "5\n5", "expected": "0"},
            {"input": "1 2 3 4 5\n6", "expected": "-1"},
            {"input": "-10 -5 0 5 10\n-5", "expected": "1"},
        ],
        "solution": {"approach": "Classic binary search: low, high, mid.", "code": "def search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1"},
        "topics": ["Array", "Binary Search"],
        "companies": ["Google", "Amazon", "Uber"],
    },
    {
        "question_title": "Palindrome Number",
        "statement": "Given an integer x, return true if x is a palindrome, and false otherwise.\n\nAn integer is a palindrome when it reads the same forward and backward.",
        "examples": [
            {"input": "x = 121", "output": "true", "explanation": "121 reads as 121 from left to right and from right to left."},
            {"input": "x = -121", "output": "false", "explanation": "From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome."},
        ],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "visible_test_cases": [
            {"input": "121", "expected": "true"},
            {"input": "-121", "expected": "false"},
        ],
        "hidden_test_cases": [
            {"input": "10", "expected": "false"},
            {"input": "0", "expected": "true"},
            {"input": "12321", "expected": "true"},
            {"input": "-2147483648", "expected": "false"},
        ],
        "solution": {"approach": "Reverse half the number and compare. Handle edge cases (negative, ending with 0).", "code": "def isPalindrome(x):\n    if x < 0 or (x % 10 == 0 and x != 0):\n        return False\n    reversed_half = 0\n    while x > reversed_half:\n        reversed_half = reversed_half * 10 + x % 10\n        x //= 10\n    return x == reversed_half or x == reversed_half // 10"},
        "topics": ["Math"],
        "companies": ["Amazon", "Microsoft", "Bloomberg"],
    },
    {
        "question_title": "Longest Common Prefix",
        "statement": "Write a function to find the longest common prefix string amongst an array of strings.\n\nIf there is no common prefix, return an empty string \"\".",
        "examples": [
            {"input": 'strs = ["flower","flow","flight"]', "output": '"fl"'},
            {"input": 'strs = ["dog","racecar","car"]', "output": '""', "explanation": "There is no common prefix among the input strings."},
        ],
        "constraints": ["1 <= strs.length <= 200", "0 <= strs[i].length <= 200", "strs[i] consists of only lowercase English letters."],
        "visible_test_cases": [
            {"input": "flower flow flight", "expected": "fl"},
            {"input": "dog racecar car", "expected": ""},
        ],
        "hidden_test_cases": [
            {"input": "a", "expected": "a"},
            {"input": "ab abc abcd", "expected": "ab"},
            {"input": "abc def ghi", "expected": ""},
        ],
        "solution": {"approach": "Vertical scanning or horizontal scanning. Compare character by character.", "code": "def longestCommonPrefix(strs):\n    if not strs:\n        return \"\"\n    prefix = strs[0]\n    for s in strs[1:]:\n        while not s.startswith(prefix):\n            prefix = prefix[:-1]\n            if not prefix:\n                return \"\"\n    return prefix"},
        "topics": ["String", "Trie"],
        "companies": ["Google", "Amazon", "Apple"],
    },
    {
        "question_title": "Roman to Integer",
        "statement": "Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.\n\nGiven a roman numeral, convert it to an integer.",
        "examples": [
            {"input": "s = \"III\"", "output": "3"},
            {"input": "s = \"LVIII\"", "output": "58"},
            {"input": "s = \"MCMXCIV\"", "output": "1994"},
        ],
        "constraints": ["1 <= s.length <= 15", "s contains only the characters 'I', 'V', 'X', 'L', 'C', 'D', 'M'."],
        "visible_test_cases": [
            {"input": "III", "expected": "3"},
            {"input": "LVIII", "expected": "58"},
        ],
        "hidden_test_cases": [
            {"input": "MCMXCIV", "expected": "1994"},
            {"input": "IV", "expected": "4"},
            {"input": "IX", "expected": "9"},
        ],
        "solution": {"approach": "Map Roman symbols to values. Iterate and subtract when smaller value appears before larger.", "code": "def romanToInt(s):\n    values = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}\n    total = 0\n    for i in range(len(s)):\n        if i+1 < len(s) and values[s[i]] < values[s[i+1]]:\n            total -= values[s[i]]\n        else:\n            total += values[s[i]]\n    return total"},
        "topics": ["Math", "String"],
        "companies": ["Amazon", "Microsoft", "Bloomberg"],
    },
    {
        "question_title": "Merge Sorted Array",
        "statement": "You are given two integer arrays nums1 and nums2, sorted in non-decreasing order. Merge them into a single sorted array in non-decreasing order.",
        "examples": [
            {"input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3", "output": "[1,2,2,3,5,6]"},
        ],
        "constraints": ["nums1.length == m + n", "nums2.length == n", "0 <= m, n <= 200", "1 <= m + n <= 200"],
        "visible_test_cases": [
            {"input": "1 2 3 0 0 0\n3\n2 5 6\n3", "expected": "1 2 2 3 5 6"},
        ],
        "hidden_test_cases": [
            {"input": "1\n1\n\n0", "expected": "1"},
            {"input": "0\n0\n1\n1", "expected": "1"},
        ],
        "solution": {"approach": "Three pointers from the end. Fill nums1 from right to left.", "code": "def merge(nums1, m, nums2, n):\n    i, j, k = m-1, n-1, m+n-1\n    while j >= 0:\n        if i >= 0 and nums1[i] > nums2[j]:\n            nums1[k] = nums1[i]\n            i -= 1\n        else:\n            nums1[k] = nums2[j]\n            j -= 1\n        k -= 1"},
        "topics": ["Array", "Two Pointers"],
        "companies": ["Amazon", "Microsoft", "Apple"],
    },
    {
        "question_title": "Valid Anagram",
        "statement": "Given two strings s and t, return true if t is an anagram of s, and false otherwise.",
        "examples": [
            {"input": "s = \"anagram\", t = \"nagaram\"", "output": "true"},
            {"input": "s = \"rat\", t = \"car\"", "output": "false"},
        ],
        "constraints": ["1 <= s.length, t.length <= 5 * 10^4", "s and t consist of lowercase English letters."],
        "visible_test_cases": [
            {"input": "anagram\nnagaram", "expected": "true"},
            {"input": "rat\ncar", "expected": "false"},
        ],
        "hidden_test_cases": [
            {"input": "a\nab", "expected": "false"},
            {"input": "ab\na", "expected": "false"},
            {"input": "aa\naa", "expected": "true"},
        ],
        "solution": {"approach": "Sort both strings or use character frequency counter.", "code": "def isAnagram(s, t):\n    return sorted(s) == sorted(t)"},
        "topics": ["String", "Sorting", "Hash Table"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Symmetric Tree",
        "statement": "Given the root of a binary tree, check whether it is a mirror of itself (symmetric around its center).",
        "examples": [
            {"input": "root = [1,2,2,3,4,4,3]", "output": "true"},
            {"input": "root = [1,2,2,null,3,null,3]", "output": "false"},
        ],
        "constraints": ["The number of nodes in the tree is in the range [1, 1000].", "-100 <= Node.val <= 100"],
        "visible_test_cases": [
            {"input": "1 2 2 3 4 4 3", "expected": "true"},
            {"input": "1 2 2 null 3 null 3", "expected": "false"},
        ],
        "hidden_test_cases": [
            {"input": "1", "expected": "true"},
            {"input": "1 2 3", "expected": "false"},
        ],
        "solution": {"approach": "Recursive: check left subtree against right subtree mirrored.", "code": "def isSymmetric(root):\n    def isMirror(l, r):\n        if not l and not r: return True\n        if not l or not r: return False\n        return l.val == r.val and isMirror(l.left, r.right) and isMirror(l.right, r.left)\n    return isMirror(root, root)"},
        "topics": ["Tree", "DFS", "BFS"],
        "companies": ["Amazon", "Microsoft", "Apple"],
    },
    {
        "question_title": "Search Insert Position",
        "statement": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be inserted.",
        "examples": [
            {"input": "nums = [1,3,5,6], target = 5", "output": "2"},
            {"input": "nums = [1,3,5,6], target = 2", "output": "1"},
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4", "nums contains distinct values sorted in ascending order."],
        "visible_test_cases": [
            {"input": "1 3 5 6\n5", "expected": "2"},
            {"input": "1 3 5 6\n2", "expected": "1"},
        ],
        "hidden_test_cases": [
            {"input": "1 3 5 6\n7", "expected": "4"},
            {"input": "1 3 5 6\n0", "expected": "0"},
            {"input": "1\n0", "expected": "0"},
        ],
        "solution": {"approach": "Binary search for insertion point.", "code": "def searchInsert(nums, target):\n    left, right = 0, len(nums)-1\n    while left <= right:\n        mid = (left+right)//2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return left"},
        "topics": ["Array", "Binary Search"],
        "companies": ["Google", "Amazon", "Uber"],
    },
    {
        "question_title": "Remove Duplicates from Sorted Array",
        "statement": "Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once.",
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2, nums = [1,2]"},
            {"input": "nums = [0,0,1,1,1,2,2,3,3,4]", "output": "5, nums = [0,1,2,3,4]"},
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-100 <= nums[i] <= 100", "nums is sorted in non-decreasing order."],
        "visible_test_cases": [
            {"input": "1 1 2", "expected": "2"},
            {"input": "0 0 1 1 1 2 2 3 3 4", "expected": "5"},
        ],
        "hidden_test_cases": [
            {"input": "1 1 1", "expected": "1"},
            {"input": "1 2 3 4 5", "expected": "5"},
        ],
        "solution": {"approach": "Two pointers: one for current unique, one for scanning.", "code": "def removeDuplicates(nums):\n    if not nums: return 0\n    i = 0\n    for j in range(1, len(nums)):\n        if nums[j] != nums[i]:\n            i += 1\n            nums[i] = nums[j]\n    return i + 1"},
        "topics": ["Array", "Two Pointers"],
        "companies": ["Amazon", "Microsoft", "Facebook"],
    },
    {
        "question_title": "Plus One",
        "statement": "Given a large integer represented as an integer array digits, increment the large integer by one and return the resulting array of digits.",
        "examples": [
            {"input": "digits = [1,2,3]", "output": "[1,2,4]"},
            {"input": "digits = [4,3,2,1]", "output": "[4,3,2,2]"},
        ],
        "constraints": ["1 <= digits.length <= 100", "0 <= digits[i] <= 9", "digits does not contain any leading 0's except the zero itself."],
        "visible_test_cases": [
            {"input": "1 2 3", "expected": "1 2 4"},
            {"input": "4 3 2 1", "expected": "4 3 2 2"},
        ],
        "hidden_test_cases": [
            {"input": "9", "expected": "1 0"},
            {"input": "9 9 9", "expected": "1 0 0 0"},
        ],
        "solution": {"approach": "Start from least significant digit, handle carry.", "code": "def plusOne(digits):\n    for i in range(len(digits)-1, -1, -1):\n        if digits[i] < 9:\n            digits[i] += 1\n            return digits\n        digits[i] = 0\n    return [1] + digits"},
        "topics": ["Array", "Math"],
        "companies": ["Google", "Amazon"],
    },
    {
        "question_title": "Length of Last Word",
        "statement": "Given a string s consisting of words and spaces, return the length of the last word in the string.",
        "examples": [
            {"input": "s = \"Hello World\"", "output": "5"},
            {"input": "s = \"   fly me   to   the moon  \"", "output": "4"},
        ],
        "constraints": ["1 <= s.length <= 10^4", "s consists of English letters and spaces ' '.", "There will be at least one word in s."],
        "visible_test_cases": [
            {"input": "Hello World", "expected": "5"},
            {"input": "   fly me   to   the moon  ", "expected": "4"},
        ],
        "hidden_test_cases": [
            {"input": "a", "expected": "1"},
            {"input": "a ", "expected": "1"},
        ],
        "solution": {"approach": "Split by spaces and return last non-empty segment, or iterate from end.", "code": "def lengthOfLastWord(s):\n    words = s.strip().split()\n    return len(words[-1]) if words else 0"},
        "topics": ["String"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Fizz Buzz",
        "statement": "Given an integer n, return a string array answer where answer[i] is the string representation of i+1 with the following rules: FizzBuzz if divisible by 3 and 5, Fizz if by 3, Buzz if by 5.",
        "examples": [
            {"input": "n = 3", "output": "[\"1\",\"2\",\"Fizz\"]"},
            {"input": "n = 5", "output": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\"]"},
        ],
        "constraints": ["1 <= n <= 10^4"],
        "visible_test_cases": [
            {"input": "3", "expected": "1\n2\nFizz"},
            {"input": "5", "expected": "1\n2\nFizz\n4\nBuzz"},
        ],
        "hidden_test_cases": [
            {"input": "15", "expected": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"},
        ],
        "solution": {"approach": "Loop from 1 to n and check modulo conditions.", "code": "def fizzBuzz(n):\n    result = []\n    for i in range(1, n+1):\n        if i % 15 == 0:\n            result.append('FizzBuzz')\n        elif i % 3 == 0:\n            result.append('Fizz')\n        elif i % 5 == 0:\n            result.append('Buzz')\n        else:\n            result.append(str(i))\n    return result"},
        "topics": ["Math", "String", "Simulation"],
        "companies": ["Google", "Amazon", "TCS"],
    },
    {
        "question_title": "Count Primes",
        "statement": "Given an integer n, return the number of prime numbers that are strictly less than n.",
        "examples": [
            {"input": "n = 10", "output": "4", "explanation": "There are 4 primes less than 10: 2, 3, 5, 7."},
        ],
        "constraints": ["0 <= n <= 5 * 10^6"],
        "visible_test_cases": [
            {"input": "10", "expected": "4"},
            {"input": "0", "expected": "0"},
        ],
        "hidden_test_cases": [
            {"input": "1", "expected": "0"},
            {"input": "100", "expected": "25"},
        ],
        "solution": {"approach": "Sieve of Eratosthenes.", "code": "def countPrimes(n):\n    if n <= 2: return 0\n    is_prime = [True] * n\n    is_prime[0] = is_prime[1] = False\n    for i in range(2, int(n**0.5)+1):\n        if is_prime[i]:\n            for j in range(i*i, n, i):\n                is_prime[j] = False\n    return sum(is_prime)"},
        "topics": ["Array", "Math", "Enumeration"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Single Number",
        "statement": "Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1"},
            {"input": "nums = [4,1,2,1,2]", "output": "4"},
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-3 * 10^4 <= nums[i] <= 3 * 10^4", "Each element in the array appears twice except for one element which appears only once."],
        "visible_test_cases": [
            {"input": "2 2 1", "expected": "1"},
            {"input": "4 1 2 1 2", "expected": "4"},
        ],
        "hidden_test_cases": [
            {"input": "1", "expected": "1"},
            {"input": "1 1 2 2 3 3 4", "expected": "4"},
        ],
        "solution": {"approach": "Use XOR. a ^ a = 0, a ^ 0 = a. XOR all numbers.", "code": "def singleNumber(nums):\n    result = 0\n    for num in nums:\n        result ^= num\n    return result"},
        "topics": ["Array", "Bit Manipulation"],
        "companies": ["Amazon", "Google", "Microsoft"],
    },
    {
        "question_title": "Happy Number",
        "statement": "Write an algorithm to determine if a number n is happy. A happy number is defined by replacing the number with the sum of squares of its digits, repeating until it equals 1 or loops endlessly.",
        "examples": [
            {"input": "n = 19", "output": "true"},
            {"input": "n = 2", "output": "false"},
        ],
        "constraints": ["1 <= n <= 2^31 - 1"],
        "visible_test_cases": [
            {"input": "19", "expected": "true"},
            {"input": "2", "expected": "false"},
        ],
        "hidden_test_cases": [
            {"input": "1", "expected": "true"},
            {"input": "7", "expected": "true"},
        ],
        "solution": {"approach": "Use Floyd's cycle detection (slow and fast pointers) or a seen set.", "code": "def isHappy(n):\n    seen = set()\n    while n != 1 and n not in seen:\n        seen.add(n)\n        n = sum(int(d)**2 for d in str(n))\n    return n == 1"},
        "topics": ["Hash Table", "Math", "Two Pointers"],
        "companies": ["Amazon", "Microsoft", "Apple"],
    },
    {
        "question_title": "Remove Element",
        "statement": "Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. Return the number of elements in nums which are not equal to val.",
        "examples": [
            {"input": "nums = [3,2,2,3], val = 3", "output": "2, nums = [2,2]"},
        ],
        "constraints": ["0 <= nums.length <= 100", "0 <= nums[i] <= 50", "0 <= val <= 100"],
        "visible_test_cases": [
            {"input": "3 2 2 3\n3", "expected": "2"},
        ],
        "hidden_test_cases": [
            {"input": "0 1 2 2 3 0 4 2\n2", "expected": "5"},
        ],
        "solution": {"approach": "Two pointers: overwrite non-val elements.", "code": "def removeElement(nums, val):\n    i = 0\n    for num in nums:\n        if num != val:\n            nums[i] = num\n            i += 1\n    return i"},
        "topics": ["Array", "Two Pointers"],
        "companies": ["Amazon", "Google"],
    },
    {
        "question_title": "First Unique Character in a String",
        "statement": "Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.",
        "examples": [
            {"input": "s = \"leetcode\"", "output": "0"},
            {"input": "s = \"loveleetcode\"", "output": "2"},
        ],
        "constraints": ["1 <= s.length <= 10^5", "s consists of only lowercase English letters."],
        "visible_test_cases": [
            {"input": "leetcode", "expected": "0"},
            {"input": "loveleetcode", "expected": "2"},
        ],
        "hidden_test_cases": [
            {"input": "aabb", "expected": "-1"},
            {"input": "abcabc", "expected": "-1"},
        ],
        "solution": {"approach": "Count frequencies, then find first with count 1.", "code": "def firstUniqChar(s):\n    from collections import Counter\n    count = Counter(s)\n    for i, ch in enumerate(s):\n        if count[ch] == 1:\n            return i\n    return -1"},
        "topics": ["String", "Hash Table", "Queue"],
        "companies": ["Amazon", "Microsoft", "Bloomberg"],
    },
    {
        "question_title": "Ransom Note",
        "statement": "Given two strings ransomNote and magazine, return true if ransomNote can be constructed from magazine. Each letter in magazine can only be used once.",
        "examples": [
            {"input": "ransomNote = \"a\", magazine = \"b\"", "output": "false"},
            {"input": "ransomNote = \"aa\", magazine = \"aab\"", "output": "true"},
        ],
        "constraints": ["1 <= ransomNote.length, magazine.length <= 10^5", "ransomNote and magazine consist of lowercase English letters."],
        "visible_test_cases": [
            {"input": "a\nb", "expected": "false"},
            {"input": "aa\naab", "expected": "true"},
        ],
        "hidden_test_cases": [
            {"input": "aa\nab", "expected": "false"},
            {"input": "abc\nabc", "expected": "true"},
        ],
        "solution": {"approach": "Count characters in magazine, decrement for ransomNote.", "code": "def canConstruct(ransomNote, magazine):\n    from collections import Counter\n    c = Counter(magazine)\n    for ch in ransomNote:\n        if c[ch] <= 0:\n            return False\n        c[ch] -= 1\n    return True"},
        "topics": ["String", "Hash Table", "Counting"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Majority Element",
        "statement": "Given an array nums of size n, return the majority element that appears more than floor(n/2) times.",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"},
        ],
        "constraints": ["n == nums.length", "1 <= n <= 5 * 10^4", "-10^9 <= nums[i] <= 10^9"],
        "visible_test_cases": [
            {"input": "3 2 3", "expected": "3"},
            {"input": "2 2 1 1 1 2 2", "expected": "2"},
        ],
        "hidden_test_cases": [
            {"input": "1", "expected": "1"},
            {"input": "1 2 1 2 1 2 1", "expected": "1"},
        ],
        "solution": {"approach": "Boyer-Moore majority vote algorithm.", "code": "def majorityElement(nums):\n    count = 0\n    candidate = None\n    for num in nums:\n        if count == 0:\n            candidate = num\n        count += 1 if num == candidate else -1\n    return candidate"},
        "topics": ["Array", "Hash Table", "Divide and Conquer"],
        "companies": ["Amazon", "Microsoft", "Google"],
    },
    {
        "question_title": "Excel Sheet Column Number",
        "statement": "Given a string columnTitle that represents the column title as appears in an Excel sheet, return its corresponding column number.",
        "examples": [
            {"input": "columnTitle = \"A\"", "output": "1"},
            {"input": "columnTitle = \"AB\"", "output": "28"},
        ],
        "constraints": ["1 <= columnTitle.length <= 7", "columnTitle consists of uppercase English letters."],
        "visible_test_cases": [
            {"input": "A", "expected": "1"},
            {"input": "AB", "expected": "28"},
        ],
        "hidden_test_cases": [
            {"input": "ZY", "expected": "701"},
            {"input": "FXSHRXW", "expected": "2147483647"},
        ],
        "solution": {"approach": "Treat as base-26 number.", "code": "def titleToNumber(columnTitle):\n    result = 0\n    for ch in columnTitle:\n        result = result * 26 + (ord(ch) - ord('A') + 1)\n    return result"},
        "topics": ["Math", "String"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Reverse Bits",
        "statement": "Reverse the bits of a given 32-bit unsigned integer.",
        "examples": [
            {"input": "n = 00000010100101000001111010011100", "output": "964176192"},
        ],
        "constraints": ["The input must be a binary string of length 32"],
        "visible_test_cases": [
            {"input": "00000010100101000001111010011100", "expected": "964176192"},
        ],
        "hidden_test_cases": [
            {"input": "11111111111111111111111111111101", "expected": "3221225471"},
        ],
        "solution": {"approach": "Bit manipulation: shift and OR reversed bits.", "code": "def reverseBits(n):\n    result = 0\n    for _ in range(32):\n        result = (result << 1) | (n & 1)\n        n >>= 1\n    return result"},
        "topics": ["Bit Manipulation", "Divide and Conquer"],
        "companies": ["Amazon", "Google", "Apple"],
    },
]


async def seed_questions():
    db = get_db()
    collection = curated_questions_collection()
    await collection.create_index("company")
    await collection.create_index("topic")
    await collection.create_index("type")

    total = 0
    for problem in CODING_PROBLEMS:
        for company in problem.get("companies", ["Google"]):
            doc = {
                "topic": problem.get("topics", ["Coding"])[0],
                "company": [company],
                "role": "SDE",
                "difficulty": random.choice(DIFFICULTIES),
                "type": "coding",
                "question_title": problem["question_title"],
                "statement": problem.get("statement", ""),
                "question": problem.get("statement", ""),
                "examples": problem.get("examples", []),
                "constraints": problem.get("constraints", []),
                "visible_test_cases": problem.get("visible_test_cases", []),
                "hidden_test_cases": problem.get("hidden_test_cases", []),
                "solution": problem.get("solution", {}),
                "hints": problem.get("hints", []),
                "topics": problem.get("topics", []),
                "companies": problem.get("companies", [company]),
                "options": [],
                "correct_answer": "",
                "explanation": "",
                "practice_count": random.randint(0, 500),
                "upvotes": random.randint(0, 120),
                "downvotes": random.randint(0, 10),
                "reported": False,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            }
            await collection.insert_one(doc)
            total += 1

    print(f"Seeded {total} coding problems.")
    cache.delete("question_filters")


if __name__ == "__main__":
    asyncio.run(seed_questions())
