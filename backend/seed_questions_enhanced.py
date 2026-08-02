import asyncio
from datetime import datetime, timezone
import random
from app.database import curated_questions_collection

ADDITIONAL_PROBLEMS = [
    {
        "question_title": "Valid Palindrome",
        "statement": "A phrase is a palindrome if, after converting all uppercase letters into lowercase and removing non-alphanumeric characters, it reads the same forward and backward.",
        "examples": [
            {"input": "s = \"A man, a plan, a canal: Panama\"", "output": "true"},
            {"input": "s = \"race a car\"", "output": "false"},
        ],
        "constraints": ["1 <= s.length <= 200000", "s consists of printable ASCII characters."],
        "visible_test_cases": [
            {"input": "\"A man, a plan, a canal: Panama\"", "expected": "true"},
            {"input": "\"race a car\"", "expected": "false"},
        ],
        "hidden_test_cases": [
            {"input": "\" \"", "expected": "true"},
            {"input": "\"0P\"", "expected": "false"},
            {"input": "\"a\"", "expected": "true"},
        ],
        "solution": {"approach": "Two pointers skipping non-alphanumeric chars.", "code": "def isPalindrome(s):\n    l, r = 0, len(s) - 1\n    while l < r:\n        while l < r and not s[l].isalnum(): l += 1\n        while l < r and not s[r].isalnum(): r -= 1\n        if s[l].lower() != s[r].lower(): return False\n        l += 1; r -= 1\n    return True"},
        "topics": ["Two Pointers", "String"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Happy Number",
        "statement": "Determine if a number n is happy. Replace by sum of squares of digits, repeat until 1 or loops. Happy numbers end in 1.",
        "examples": [
            {"input": "n = 19", "output": "true"},
            {"input": "n = 2", "output": "false"},
        ],
        "constraints": ["1 <= n <= 2147483647"],
        "visible_test_cases": [{"input": "19", "expected": "true"}],
        "hidden_test_cases": [
            {"input": "2", "expected": "false"},
            {"input": "7", "expected": "true"},
            {"input": "1111111", "expected": "true"},
        ],
        "solution": {"approach": "Floyd cycle detection.", "code": "def isHappy(n):\n    seen = set()\n    while n != 1 and n not in seen:\n        seen.add(n)\n        n = sum(int(d)**2 for d in str(n))\n    return n == 1"},
        "topics": ["Hash Table", "Math"],
        "companies": ["Google", "Amazon"],
    },
    {
        "question_title": "Valid Anagram",
        "statement": "Given strings s and t, return true if t is an anagram of s.",
        "examples": [
            {"input": "s = \"anagram\", t = \"nagaram\"", "output": "true"},
            {"input": "s = \"rat\", t = \"car\"", "output": "false"},
        ],
        "constraints": ["1 <= len(s), len(t) <= 50000", "Lowercase English only."],
        "visible_test_cases": [{"input": "\"anagram\"\n\"nagaram\"", "expected": "true"}],
        "hidden_test_cases": [
            {"input": "\"rat\"\n\"car\"", "expected": "false"},
            {"input": "\"a\"\n\"ab\"", "expected": "false"},
            {"input": "\"\"\n\"\"", "expected": "true"},
        ],
        "solution": {"approach": "Sort or count frequencies.", "code": "def isAnagram(s, t):\n    if len(s) != len(t): return False\n    return sorted(s) == sorted(t)"},
        "topics": ["Hash Table", "String"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Single Number",
        "statement": "Every element appears twice except one. Find it with linear runtime and constant space.",
        "examples": [
            {"input": "nums = [4,1,2,1,2]", "output": "4"},
            {"input": "nums = [2,2,1]", "output": "1"},
        ],
        "constraints": ["1 <= nums.length <= 30000", "-30000 <= nums[i] <= 30000"],
        "visible_test_cases": [{"input": "[4,1,2,1,2]", "expected": "4"}],
        "hidden_test_cases": [
            {"input": "[2,2,1]", "expected": "1"},
            {"input": "[1]", "expected": "1"},
            {"input": "[1,2,3,3,2]", "expected": "1"},
        ],
        "solution": {"approach": "XOR all elements.", "code": "def singleNumber(nums):\n    r = 0\n    for n in nums: r ^= n\n    return r"},
        "topics": ["Array", "Bit Manipulation"],
        "companies": ["Google", "Amazon", "Microsoft", "Apple"],
    },
    {
        "question_title": "Remove Element",
        "statement": "Remove all occurrences of val in nums in-place. Return k, the count of remaining elements.",
        "examples": [
            {"input": "nums = [3,2,2,3], val = 3", "output": "2, nums = [2,2]"},
            {"input": "nums = [0,1,2,2,3,0,4,2], val = 2", "output": "5"},
        ],
        "constraints": ["0 <= nums.length <= 100", "0 <= nums[i] <= 50", "0 <= val <= 100"],
        "visible_test_cases": [{"input": "[3,2,2,3]\n3", "expected": "2"}],
        "hidden_test_cases": [
            {"input": "[0,1,2,2,3,0,4,2]\n2", "expected": "5"},
            {"input": "[]\n1", "expected": "0"},
            {"input": "[1]\n1", "expected": "0"},
        ],
        "solution": {"approach": "Two-pointer write technique.", "code": "def removeElement(nums, val):\n    k = 0\n    for i in range(len(nums)):\n        if nums[i] != val:\n            nums[k] = nums[i]\n            k += 1\n    return k"},
        "topics": ["Array", "Two Pointers"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Longest Common Prefix",
        "statement": "Find the longest common prefix among an array of strings.",
        "examples": [
            {"input": "strs = [\"flower\",\"flow\",\"flight\"]", "output": "\"fl\""},
            {"input": "strs = [\"dog\",\"racecar\",\"car\"]", "output": "\"\""},
        ],
        "constraints": ["1 <= strs.length <= 200", "0 <= len(strs[i]) <= 200"],
        "visible_test_cases": [{"input": "[\"flower\",\"flow\",\"flight\"]", "expected": "\"fl\""}],
        "hidden_test_cases": [
            {"input": "[\"dog\",\"racecar\",\"car\"]", "expected": "\"\""},
            {"input": "[\"abc\"]", "expected": "\"abc\""},
            {"input": "[\"ab\",\"a\"]", "expected": "\"a\"},
        ],
        "solution": {"approach": "Column-wise character comparison.", "code": "def longestCommonPrefix(strs):\n    if not strs: return \"\"\n    for i, c in enumerate(strs[0]):\n        for s in strs[1:]:\n            if i >= len(s) or s[i] != c: return strs[0][:i]\n    return strs[0]"},
        "topics": ["String", "Trie"],
        "companies": ["TCS", "Amazon", "Google"],
    },
    {
        "question_title": "Symmetric Tree",
        "statement": "Check if a binary tree is a mirror of itself.",
        "examples": [
            {"input": "root = [1,2,2,3,4,4,3]", "output": "true"},
            {"input": "root = [1,2,2,null,3,null,3]", "output": "false"},
        ],
        "constraints": ["1 <= nodes <= 1000", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "[1,2,2,3,4,4,3]", "expected": "true"}],
        "hidden_test_cases": [
            {"input": "[1,2,2,null,3,null,3]", "expected": "false"},
            {"input": "[1]", "expected": "true"},
            {"input": "[]", "expected": "true"},
        ],
        "solution": {"approach": "Recursively check mirror symmetry.", "code": "def isSymmetric(root):\n    if not root: return True\n    def mirror(l, r):\n        if not l and not r: return True\n        if not l or not r: return False\n        return l.val == r.val and mirror(l.left, r.right) and mirror(l.right, r.left)\n    return mirror(root.left, root.right)"},
        "topics": ["Tree", "DFS", "BFS"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Search Insert Position",
        "statement": "Given sorted array and target, return index if found, else insertion index.",
        "examples": [
            {"input": "nums = [1,3,5,6], target = 5", "output": "2"},
            {"input": "nums = [1,3,5,6], target = 2", "output": "1"},
        ],
        "constraints": ["1 <= nums.length <= 10000", "nums is sorted ascending.", "-10000 <= target <= 10000"],
        "visible_test_cases": [{"input": "[1,3,5,6]\n5", "expected": "2"}],
        "hidden_test_cases": [
            {"input": "[1,3,5,6]\n2", "expected": "1"},
            {"input": "[1,3,5,6]\n7", "expected": "4"},
            {"input": "[1,3,5,6]\n0", "expected": "0"},
        ],
        "solution": {"approach": "Binary search.", "code": "def searchInsert(nums, target):\n    l, r = 0, len(nums)-1\n    while l <= r:\n        m = (l+r)//2\n        if nums[m] == target: return m\n        elif nums[m] < target: l = m+1\n        else: r = m-1\n    return l"},
        "topics": ["Binary Search", "Array"],
        "companies": ["Google", "Amazon"],
    },
    {
        "question_title": "Remove Duplicates from Sorted Array",
        "statement": "Remove duplicates in-place, return count of unique elements.",
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2, nums = [1,2]"},
        ],
        "constraints": ["1 <= nums.length <= 30000", "nums is sorted non-decreasing."],
        "visible_test_cases": [{"input": "[1,1,2]", "expected": "2"}],
        "hidden_test_cases": [
            {"input": "[0,0,1,1,1,2,2,3,3,4]", "expected": "5"},
            {"input": "[1]", "expected": "1"},
        ],
        "solution": {"approach": "Two-pointer technique.", "code": "def removeDuplicates(nums):\n    if not nums: return 0\n    k = 1\n    for i in range(1, len(nums)):\n        if nums[i] != nums[i-1]:\n            nums[k] = nums[i]\n            k += 1\n    return k"},
        "topics": ["Array", "Two Pointers"],
        "companies": ["TCS", "Wipro"],
    },
    {
        "question_title": "Plus One",
        "statement": "Increment a large integer represented as an array of digits by one.",
        "examples": [
            {"input": "digits = [1,2,3]", "output": "[1,2,4]"},
            {"input": "digits = [9]", "output": "[1,0]"},
        ],
        "constraints": ["1 <= digits.length <= 100", "0 <= digits[i] <= 9"],
        "visible_test_cases": [{"input": "[1,2,3]", "expected": "[1,2,4]"}],
        "hidden_test_cases": [
            {"input": "[9]", "expected": "[1,0]"},
            {"input": "[9,9,9]", "expected": "[1,0,0,0]"},
        ],
        "solution": {"approach": "Process right to left, handle carry.", "code": "def plusOne(digits):\n    for i in range(len(digits)-1, -1, -1):\n        digits[i] += 1\n        if digits[i] < 10: return digits\n        digits[i] = 0\n    return [1] + digits"},
        "topics": ["Array", "Math"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Length of Last Word",
        "statement": "Return the length of the last word in a string.",
        "examples": [
            {"input": "s = \"Hello World\"", "output": "5"},
            {"input": "s = \"   fly me   to   the moon  \"", "output": "4"},
        ],
        "constraints": ["1 <= s.length <= 10000"],
        "visible_test_cases": [{"input": "\"Hello World\"", "expected": "5"}],
        "hidden_test_cases": [
            {"input": "\"   fly me   to   the moon  \"", "expected": "4"},
            {"input": "\"luffy is still joyboy\"", "expected": "6"},
            {"input": "\"a\"", "expected": "1"},
        ],
        "solution": {"code": "def lengthOfLastWord(s):\n    return len(s.rstrip().split(\" \")[-1])"},
        "topics": ["String"],
        "companies": ["Amazon", "TCS"],
    },
    {
        "question_title": "Count Primes",
        "statement": "Count the number of primes strictly less than n using Sieve of Eratosthenes.",
        "examples": [
            {"input": "n = 10", "output": "4"},
            {"input": "n = 0", "output": "0"},
        ],
        "constraints": ["0 <= n <= 5000000"],
        "visible_test_cases": [{"input": "10", "expected": "4"}],
        "hidden_test_cases": [
            {"input": "0", "expected": "0"},
            {"input": "100", "expected": "25"},
        ],
        "solution": {"code": "def countPrimes(n):\n    if n <= 2: return 0\n    s = [True]*n\n    s[0] = s[1] = False\n    for i in range(2, int(n**0.5)+1):\n        if s[i]:\n            for j in range(i*i, n, i): s[j] = False\n    return sum(s)"},
        "topics": ["Math", "Sieve"],
        "companies": ["Google", "Amazon"],
    },
    {
        "question_title": "First Unique Character in a String",
        "statement": "Find the index of the first non-repeating character in a string.",
        "examples": [
            {"input": "s = \"leetcode\"", "output": "0"},
            {"input": "s = \"loveleetcode\"", "output": "2"},
            {"input": "s = \"aabb\"", "output": "-1"},
        ],
        "constraints": ["1 <= s.length <= 100000", "Lowercase English only."],
        "visible_test_cases": [{"input": "\"leetcode\"", "expected": "0"}],
        "hidden_test_cases": [
            {"input": "\"loveleetcode\"", "expected": "2"},
            {"input": "\"aabb\"", "expected": "-1"},
            {"input": "\"z\"", "expected": "0"},
        ],
        "solution": {"code": "def firstUniqChar(s):\n    from collections import Counter\n    c = Counter(s)\n    for i, ch in enumerate(s):\n        if c[ch] == 1: return i\n    return -1"},
        "topics": ["Hash Table", "String"],
        "companies": ["Amazon", "Google"],
    },
    {
        "question_title": "Ransom Note",
        "statement": "Check if ransomNote can be constructed from magazine letters.",
        "examples": [
            {"input": "ransomNote = \"a\", magazine = \"b\"", "output": "false"},
            {"input": "ransomNote = \"aa\", magazine = \"aab\"", "output": "true"},
        ],
        "constraints": ["1 <= lengths <= 100000", "Lowercase English only."],
        "visible_test_cases": [{"input": "\"a\"\n\"b\"", "expected": "false"}],
        "hidden_test_cases": [
            {"input": "\"aa\"\n\"ab\"", "expected": "false"},
            {"input": "\"aa\"\n\"aab\"", "expected": "true"},
        ],
        "solution": {"code": "def canConstruct(ransomNote, magazine):\n    from collections import Counter\n    m = Counter(magazine)\n    for c in ransomNote:\n        if m[c] <= 0: return False\n        m[c] -= 1\n    return True"},
        "topics": ["Hash Table", "String"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Majority Element",
        "statement": "Find the majority element (appears more than n/2 times).",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"},
        ],
        "constraints": ["n == nums.length", "1 <= n <= 50000", "-10^9 <= nums[i] <= 10^9"],
        "visible_test_cases": [{"input": "[3,2,3]", "expected": "3"}],
        "hidden_test_cases": [
            {"input": "[2,2,1,1,1,2,2]", "expected": "2"},
            {"input": "[1]", "expected": "1"},
        ],
        "solution": {"code": "def majorityElement(nums):\n    count = 0; candidate = None\n    for num in nums:\n        if count == 0: candidate = num\n        count += (1 if num == candidate else -1)\n    return candidate"},
        "topics": ["Array", "Boyer-Moore"],
        "companies": ["Google", "Amazon", "Meta"],
    },
    {
        "question_title": "Two Sum",
        "statement": "Return indices of two numbers that add up to target.",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"},
        ],
        "constraints": ["2 <= nums.length <= 10000", "-10^9 <= nums[i], target <= 10^9"],
        "visible_test_cases": [{"input": "2 7 11 15\n9", "expected": "[0, 1]"}],
        "hidden_test_cases": [
            {"input": "3 3\n6", "expected": "[0, 1]"},
            {"input": "1 5 3 7 9\n12", "expected": "[1, 4]"},
        ],
        "solution": {"code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen: return [seen[target - num], i]\n        seen[num] = i"},
        "topics": ["Array", "Hash Table"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Valid Parentheses",
        "statement": "Check if parentheses string is valid (matching open/close, correct order).",
        "examples": [
            {"input": "s = \"()\"", "output": "true"},
            {"input": "s = \"(]\"", "output": "false"},
        ],
        "constraints": ["1 <= s.length <= 10000", "Only ()[]{} characters."],
        "visible_test_cases": [{"input": "()", "expected": "true"}],
        "hidden_test_cases": [
            {"input": "{[]}", "expected": "true"},
            {"input": "((", "expected": "false"},
        ],
        "solution": {"code": "def isValid(s):\n    stack = []; m = {\")\":\"(\", \"]\":\"[\", \}\":\"{\\\"}\n    for c in s:\n        if c in m:\n            if not stack or stack.pop() != m[c]: return False\n        else: stack.append(c)\n    return not stack"},
        "topics": ["Stack", "String"],
        "companies": ["Google", "Amazon", "Microsoft"],
    },
    {
        "question_title": "Maximum Subarray",
        "statement": "Find the contiguous subarray with the largest sum.",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},
            {"input": "nums = [1]", "output": "1"},
        ],
        "constraints": ["1 <= nums.length <= 100000", "-10000 <= nums[i] <= 10000"],
        "visible_test_cases": [{"input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected": "6"}],
        "hidden_test_cases": [
            {"input": "[1]", "expected": "1"},
            {"input": "[5,4,-1,7,8]", "expected": "23"},
        ],
        "solution": {"code": "def maxSubArray(nums):\n    mx = cur = nums[0]\n    for i in range(1, len(nums)):\n        cur = max(nums[i], cur + nums[i])\n        mx = max(mx, cur)\n    return mx"},
        "topics": ["Array", "Dynamic Programming"],
        "companies": ["Google", "Amazon", "Microsoft", "Meta"],
    },
    {
        "question_title": "Climbing Stairs",
        "statement": "Count distinct ways to climb n stairs taking 1 or 2 steps at a time.",
        "examples": [
            {"input": "n = 2", "output": "2"},
            {"input": "n = 3", "output": "3"},
        ],
        "constraints": ["1 <= n <= 45"],
        "visible_test_cases": [{"input": "2", "expected": "2"}],
        "hidden_test_cases": [
            {"input": "3", "expected": "3"},
            {"input": "45", "expected": "1836311903"},
        ],
        "solution": {"code": "def climbStairs(n):\n    if n <= 2: return n\n    a, b = 1, 2\n    for _ in range(3, n+1): a, b = b, a+b\n    return b"},
        "topics": ["Math", "Dynamic Programming"],
        "companies": ["Google", "Amazon", "TCS"],
    },
    {
        "question_title": "Reverse Linked List",
        "statement": "Reverse a singly linked list.",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
            {"input": "head = []", "output": "[]"},
        ],
        "constraints": ["0 <= nodes <= 5000", "-5000 <= Node.val <= 5000"],
        "visible_test_cases": [{"input": "[1,2,3,4,5]", "expected": "[5,4,3,2,1]"}],
        "hidden_test_cases": [
            {"input": "[]", "expected": "[]"},
            {"input": "[1]", "expected": "[1]"},
        ],
        "solution": {"code": "def reverseList(head):\n    prev = None\n    while head:\n        nxt = head.next\n        head.next = prev\n        prev = head\n        head = nxt\n    return prev"},
        "topics": ["Linked List", "Recursion"],
        "companies": ["Amazon", "Microsoft"],
    },
    {
        "question_title": "Fizz Buzz",
        "statement": "For i from 1 to n, return FizzBuzz for multiples of 3 and 5, Fizz for 3, Buzz for 5, else the number.",
        "examples": [
            {"input": "n = 3", "output": "[\"1\",\"2\",\"Fizz\"]"},
            {"input": "n = 5", "output": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\"]"},
        ],
        "constraints": ["1 <= n <= 10000"],
        "visible_test_cases": [{"input": "3", "expected": "[\"1\",\"2\",\"Fizz\"]"}],
        "hidden_test_cases": [
            {"input": "15", "expected": "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\",\"Fizz\",\"7\",\"8\",\"Fizz\",\"Buzz\",\"11\",\"Fizz\",\"13\",\"14\",\"FizzBuzz\"]"},
        ],
        "solution": {"code": "def fizzBuzz(n):\n    r = []\n    for i in range(1, n+1):\n        if i%3==0 and i%5==0: r.append(\"FizzBuzz\")\n        elif i%3==0: r.append(\"Fizz\")\n        elif i%5==0: r.append(\"Buzz\")\n        else: r.append(str(i))\n    return r"},
        "topics": ["Math", "String"],
        "companies": ["TCS", "Infosys", "Wipro", "Accenture"],
    },
]


async def seed():
    collection = curated_questions_collection()
    existing = await collection.count_documents({})
    print(f"Current: {existing}")
    new_count = 0
    for p in ADDITIONAL_PROBLEMS:
        p["type"] = "coding"
        p.setdefault("hints", [])
        p.setdefault("frequency", random.randint(1, 100))
        p.setdefault("acceptance_rate", round(random.uniform(0.2, 0.8), 2))
        p.setdefault("total_submissions", random.randint(100, 10000))
        p["created_at"] = datetime.now(timezone.utc)
        p["updated_at"] = datetime.now(timezone.utc)
        await collection.insert_one(p)
        new_count += 1
    print(f"Added {new_count} problems. Total: {existing + new_count}")

async def main():
    await seed()

if __name__ == "__main__":
    asyncio.run(main())