"""
Striver's SDE Sheet — 470+ curated DSA problems for placement preparation.
Each problem includes: statement, examples, constraints, test cases, solution, hints.
Organized by topic with sequential ordering.
"""
from .striver_basics import ADDITIONAL_PROBLEMS
from .striver_extra import EXTRA_PROBLEMS
from .striver_final import FINAL_PROBLEMS
from .striver_remaining import REMAINING_PROBLEMS
from .striver_complete_final import COMPLETE_FINAL
from .striver_ultimate import ULTIMATE_PROBLEMS
from .striver_final_batch import FINAL_BATCH
from .striver_last import LAST_BATCH
from .striver_complete_ultimate import COMPLETE_ULTIMATE
from .striver_final_complete import FINAL_COMPLETE
from .striver_ultimate_complete import ULTIMATE_COMPLETE
from .striver_last_complete import LAST_COMPLETE
from .striver_final_ultimate import FINAL_ULTIMATE
from .striver_complete_ultimate_final import COMPLETE_ULTIMATE_FINAL
from .striver_last_ultimate import LAST_ULTIMATE
from .striver_complete_last import COMPLETE_LAST
from .striver_ultimate_last import ULTIMATE_LAST
from .striver_complete_ultimate_last import COMPLETE_ULTIMATE_LAST
from .striver_last_final import LAST_FINAL
from .striver_final_ultimate_last import FINAL_ULTIMATE_LAST
from .striver_complete_final_last import COMPLETE_FINAL_LAST

PROBLEMS = [
    # ═══════════════════════════════════════════════════════════════════════════
    # TOPIC 1: ARRAYS (Part I) — 30 problems
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "A1-01", "topic": "Arrays", "topic_order": 1, "problem_order": 1,
        "question_title": "Set Matrix Zeroes",
        "statement": "Given an m x n integer matrix, if an element is 0, set its entire row and column to 0's. You must do it in place.",
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]"},
            {"input": "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "output": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]"}
        ],
        "constraints": ["m == matrix.length", "n == matrix[0].length", "1 <= m, n <= 200", "-2^31 <= matrix[i][j] <= 2^31 - 1"],
        "visible_test_cases": [
            {"input": "3\n3\n1 1 1\n1 0 1\n1 1 1", "expected": "1 0 1\n0 0 0\n1 0 1"},
            {"input": "2\n3\n0 1 2\n3 4 5", "expected": "0 0 0\n0 4 5"}
        ],
        "hidden_test_cases": [
            {"input": "1\n1\n0", "expected": "0"},
            {"input": "1\n3\n1 2 0", "expected": "0 0 0"},
            {"input": "3\n1\n1\n0\n1", "expected": "1\n0\n0"}
        ],
        "solution": {"approach": "Use first row and first column as markers. Mark zeros, then set rows/cols.", "code": "def setZeroes(matrix):\n    m, n = len(matrix), len(matrix[0])\n    first_row = any(matrix[0][j] == 0 for j in range(n))\n    first_col = any(matrix[i][0] == 0 for i in range(m))\n    for i in range(1, m):\n        for j in range(1, n):\n            if matrix[i][j] == 0:\n                matrix[i][0] = matrix[0][j] = 0\n    for i in range(1, m):\n        for j in range(1, n):\n            if matrix[i][0] == 0 or matrix[0][j] == 0:\n                matrix[i][j] = 0\n    if first_row:\n        for j in range(n): matrix[0][j] = 0\n    if first_col:\n        for i in range(m): matrix[i][0] = 0", "time_complexity": "O(m*n)", "space_complexity": "O(1)"},
        "hints": ["Use the first row and first column as markers for which rows/cols need to be zeroed.", "Handle the first row and column separately since they serve as markers.", "Process the matrix from bottom-right to avoid overwriting markers prematurely."],
        "topics": ["Matrix", "Array"], "companies": ["Amazon", "Microsoft", "Google", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-02", "topic": "Arrays", "topic_order": 1, "problem_order": 2,
        "question_title": "Pascal's Triangle",
        "statement": "Given an integer numRows, return the first numRows of Pascal's triangle. In Pascal's triangle, each number is the sum of the two numbers directly above it.",
        "examples": [
            {"input": "numRows = 5", "output": "[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]"},
            {"input": "numRows = 1", "output": "[[1]]"}
        ],
        "constraints": ["1 <= numRows <= 30"],
        "visible_test_cases": [
            {"input": "5", "expected": "1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1"},
            {"input": "1", "expected": "1"}
        ],
        "hidden_test_cases": [
            {"input": "3", "expected": "1\n1 1\n1 2 1"},
            {"input": "6", "expected": "1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1"}
        ],
        "solution": {"approach": "Build row by row. Each element = sum of two elements above it.", "code": "def generate(numRows):\n    result = []\n    for i in range(numRows):\n        row = [1] * (i + 1)\n        for j in range(1, i):\n            row[j] = result[i-1][j-1] + result[i-1][j]\n        result.append(row)\n    return result", "time_complexity": "O(numRows^2)", "space_complexity": "O(1) excluding output"},
        "hints": ["Start with [1] for the first row.", "For each subsequent row, start and end with 1.", "Middle elements are the sum of the two elements directly above."],
        "topics": ["Array", "Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-03", "topic": "Arrays", "topic_order": 1, "problem_order": 3,
        "question_title": "Next Permutation",
        "statement": "A permutation of an array of integers is an arrangement of its members into a sequence or linear order. Given an array of integers nums, find the next permutation of nums.",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[1,3,2]"},
            {"input": "nums = [3,2,1]", "output": "[1,2,3]"},
            {"input": "nums = [1,1,5]", "output": "[1,5,1]"}
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 100"],
        "visible_test_cases": [
            {"input": "3\n1 2 3", "expected": "1 3 2"},
            {"input": "3\n3 2 1", "expected": "1 2 3"}
        ],
        "hidden_test_cases": [
            {"input": "3\n1 1 5", "expected": "1 5 1"},
            {"input": "4\n1 3 5 4", "expected": "1 4 3 5"},
            {"input": "2\n1 2", "expected": "2 1"}
        ],
        "solution": {"approach": "Find largest i where nums[i] < nums[i+1]. Find largest j where nums[j] > nums[i]. Swap nums[i], nums[j]. Reverse from i+1.", "code": "def nextPermutation(nums):\n    n = len(nums)\n    i = n - 2\n    while i >= 0 and nums[i] >= nums[i + 1]:\n        i -= 1\n    if i >= 0:\n        j = n - 1\n        while nums[j] <= nums[i]:\n            j -= 1\n        nums[i], nums[j] = nums[j], nums[i]\n    nums[i+1:] = reversed(nums[i+1:])", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Scan from right to find the first element that breaks ascending order.", "Find the smallest element to the right that is larger than the breaking element.", "Swap them and reverse the suffix."],
        "topics": ["Array"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-04", "topic": "Arrays", "topic_order": 1, "problem_order": 4,
        "question_title": "Maximum Subarray",
        "statement": "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
            {"input": "nums = [1]", "output": "1"},
            {"input": "nums = [5,4,-1,7,8]", "output": "23"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "9\n-2 1 -3 4 -1 2 1 -5 4", "expected": "6"},
            {"input": "1\n1", "expected": "1"}
        ],
        "hidden_test_cases": [
            {"input": "5\n5 4 -1 7 8", "expected": "23"},
            {"input": "1\n-1", "expected": "-1"},
            {"input": "2\n-2 -1", "expected": "-1"}
        ],
        "solution": {"approach": "Kadane's Algorithm: track current_max and global_max.", "code": "def maxSubArray(nums):\n    current_max = global_max = nums[0]\n    for num in nums[1:]:\n        current_max = max(num, current_max + num)\n        global_max = max(global_max, current_max)\n    return global_max", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Think about what happens when the running sum becomes negative.", "Reset the running sum when it drops below the current element.", "Track the maximum sum seen so far."],
        "topics": ["Array", "Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-05", "topic": "Arrays", "topic_order": 1, "problem_order": 5,
        "question_title": "Sort an Array of 0s, 1s and 2s",
        "statement": "Given an array arr consisting of only 0s, 1s, and 2s. Sort the array in ascending order without using any sorting algorithm (Dutch National Flag problem).",
        "examples": [
            {"input": "arr = [0,1,2,0,1,2]", "output": "[0,0,1,1,2,2]"},
            {"input": "arr = [0,1,1,0,1,2,1,2,0,0,1]", "output": "[0,0,0,0,1,1,1,1,1,2,2]"}
        ],
        "constraints": ["1 <= arr.size() <= 10^6", "0 <= arr[i] <= 2"],
        "visible_test_cases": [
            {"input": "6\n0 1 2 0 1 2", "expected": "0 0 1 1 2 2"},
            {"input": "4\n0 1 2 1", "expected": "0 1 1 2"}
        ],
        "hidden_test_cases": [
            {"input": "1\n0", "expected": "0"},
            {"input": "5\n2 2 2 2 2", "expected": "2 2 2 2 2"},
            {"input": "3\n1 0 2", "expected": "0 1 2"}
        ],
        "solution": {"approach": "Three pointers: low, mid, high. Swap 0s to low, 2s to high.", "code": "def sort012(arr):\n    low, mid, high = 0, 0, len(arr) - 1\n    while mid <= high:\n        if arr[mid] == 0:\n            arr[low], arr[mid] = arr[mid], arr[low]\n            low += 1\n            mid += 1\n        elif arr[mid] == 1:\n            mid += 1\n        else:\n            arr[mid], arr[high] = arr[high], arr[mid]\n            high -= 1", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use three pointers: low, mid, high.", "Elements before low are 0, after high are 2.", "Mid is the current element being examined."],
        "topics": ["Array", "Sorting"], "companies": ["Amazon", "Microsoft", "TCS", "Wipro"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-06", "topic": "Arrays", "topic_order": 1, "problem_order": 6,
        "question_title": "Stock Buy and Sell",
        "statement": "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy and a single day to sell. Return the maximum profit. If no profit is possible, return 0.",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5"},
            {"input": "prices = [7,6,4,3,1]", "output": "0"}
        ],
        "constraints": ["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "6\n7 1 5 3 6 4", "expected": "5"},
            {"input": "5\n7 6 4 3 1", "expected": "0"}
        ],
        "hidden_test_cases": [
            {"input": "2\n1 2", "expected": "1"},
            {"input": "3\n2 4 1", "expected": "2"},
            {"input": "7\n2 1 2 1 2 1 2", "expected": "1"}
        ],
        "solution": {"approach": "Track min price so far and max profit.", "code": "def maxProfit(prices):\n    min_price = float('inf')\n    max_profit = 0\n    for price in prices:\n        min_price = min(min_price, price)\n        max_profit = max(max_profit, price - min_price)\n    return max_profit", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Track the minimum price seen so far.", "At each step, calculate profit if selling today.", "Keep the maximum profit."],
        "topics": ["Array"], "companies": ["Amazon", "Google", "Microsoft", "Goldman Sachs"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-07", "topic": "Arrays", "topic_order": 1, "problem_order": 7,
        "question_title": "Rotate Matrix by 90 degrees",
        "statement": "You are given an n x n 2D matrix representing an image. Rotate the image by 90 degrees (clockwise) in-place.",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[[7,4,1],[8,5,2],[9,6,3]]"},
            {"input": "matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "output": "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]"}
        ],
        "constraints": ["n == matrix.length", "n == matrix[i].length", "1 <= n <= 20", "-1000 <= matrix[i][j] <= 1000"],
        "visible_test_cases": [
            {"input": "3\n1 2 3\n4 5 6\n7 8 9", "expected": "7 4 1\n8 5 2\n9 6 3"},
            {"input": "2\n1 2\n3 4", "expected": "3 1\n4 2"}
        ],
        "hidden_test_cases": [
            {"input": "1\n1", "expected": "1"},
            {"input": "4\n5 1 9 11\n2 4 8 10\n13 3 6 7\n15 14 12 16", "expected": "15 13 2 5\n14 3 4 1\n12 6 8 9\n16 7 10 11"}
        ],
        "solution": {"approach": "Transpose the matrix, then reverse each row.", "code": "def rotate(matrix):\n    n = len(matrix)\n    for i in range(n):\n        for j in range(i + 1, n):\n            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]\n    for row in matrix:\n        row.reverse()", "time_complexity": "O(n^2)", "space_complexity": "O(1)"},
        "hints": ["First transpose the matrix (swap rows with columns).", "Then reverse each row.", "This gives a 90-degree clockwise rotation."],
        "topics": ["Matrix", "Array"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-08", "topic": "Arrays", "topic_order": 1, "problem_order": 8,
        "question_title": "Merge Overlapping Intervals",
        "statement": "Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals.",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"}
        ],
        "constraints": ["1 <= intervals.length <= 10^4", "intervals[i].length == 2", "0 <= starti <= endi <= 10^4"],
        "visible_test_cases": [
            {"input": "4\n1 3\n2 6\n8 10\n15 18", "expected": "1 6\n8 10\n15 18"},
            {"input": "2\n1 4\n4 5", "expected": "1 5"}
        ],
        "hidden_test_cases": [
            {"input": "1\n1 4", "expected": "1 4"},
            {"input": "3\n1 4\n0 4", "expected": "0 4"},
            {"input": "2\n1 4\n2 3", "expected": "1 4"}
        ],
        "solution": {"approach": "Sort by start time. Merge overlapping intervals.", "code": "def merge(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for start, end in intervals[1:]:\n        if start <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], end)\n        else:\n            merged.append([start, end])\n    return merged", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Sort intervals by start time.", "If the current interval overlaps with the last merged, extend it.", "Otherwise, add it to the result."],
        "topics": ["Array", "Sorting"], "companies": ["Google", "Amazon", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-09", "topic": "Arrays", "topic_order": 1, "problem_order": 9,
        "question_title": "Merge Two Sorted Arrays Without Extra Space",
        "statement": "Given two sorted arrays arr1[] and arr2[] of sizes n and m in non-decreasing order. Merge them into arr1[] such that the final sorted array is in arr1[].",
        "examples": [
            {"input": "arr1 = [1,4,8,10], arr2 = [2,3,9]", "output": "[1,2,3,4,8,9,10]"},
            {"input": "arr1 = [1,3,5,7], arr2 = [0,2,6,8,9]", "output": "[0,1,2,3,5,6,7,8,9]"}
        ],
        "constraints": ["1 <= n, m <= 10^5", "0 <= arr1[i], arr2[i] <= 10^6"],
        "visible_test_cases": [
            {"input": "4 3\n1 4 8 10\n2 3 9", "expected": "1 2 3 4 8 9 10"},
            {"input": "4 5\n1 3 5 7\n0 2 6 8 9", "expected": "0 1 2 3 5 6 7 8 9"}
        ],
        "hidden_test_cases": [
            {"input": "1 1\n1\n2", "expected": "1 2"},
            {"input": "3 0\n1 2 3\n", "expected": "1 2 3"},
            {"input": "2 2\n1 3\n2 4", "expected": "1 2 3 4"}
        ],
        "solution": {"approach": "Gap method: compare elements at distance gap, swap if needed, reduce gap.", "code": "def merge(arr1, arr2, n, m):\n    gap = (n + m + 1) // 2\n    while gap > 0:\n        for i in range(n + m - gap):\n            j = i + gap\n            if i < n and j < n:\n                if arr1[i] > arr1[j]:\n                    arr1[i], arr1[j] = arr1[j], arr1[i]\n            elif i < n and j >= n:\n                if arr1[i] > arr2[j - n]:\n                    arr1[i], arr2[j - n] = arr2[j - n], arr1[i]\n            else:\n                if arr2[i - n] > arr2[j - n]:\n                    arr2[i - n], arr2[j - n] = arr2[j - n], arr2[i - n]\n        if gap == 1: break\n        gap = (gap + 1) // 2", "time_complexity": "O((n+m)*log(n+m))", "space_complexity": "O(1)"},
        "hints": ["Think of both arrays as one combined array.", "Use the gap method (shell sort inspired).", "Compare elements at distance gap and swap if out of order."],
        "topics": ["Array", "Sorting"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-10", "topic": "Arrays", "topic_order": 1, "problem_order": 10,
        "question_title": "Find the Duplicate Number",
        "statement": "Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive. There is only one repeated number. Find and return this repeated number.",
        "examples": [
            {"input": "nums = [1,3,4,2,2]", "output": "2"},
            {"input": "nums = [3,1,3,4,2]", "output": "3"}
        ],
        "constraints": ["1 <= n <= 10^5", "nums.length == n + 1", "1 <= nums[i] <= n", "Only one repeated number"],
        "visible_test_cases": [
            {"input": "5\n1 3 4 2 2", "expected": "2"},
            {"input": "5\n3 1 3 4 2", "expected": "3"}
        ],
        "hidden_test_cases": [
            {"input": "2\n1 1", "expected": "1"},
            {"input": "5\n2 5 9 6 9 3 8 7 1 4", "expected": "9"}
        ],
        "solution": {"approach": "Floyd's cycle detection. Treat array as linked list where nums[i] is next node.", "code": "def findDuplicate(nums):\n    slow = fast = nums[0]\n    while True:\n        slow = nums[slow]\n        fast = nums[nums[fast]]\n        if slow == fast:\n            break\n    slow = nums[0]\n    while slow != fast:\n        slow = nums[slow]\n        fast = nums[fast]\n    return slow", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Treat the array as a linked list where index i points to nums[i].", "Use Floyd's tortoise and hare algorithm to find cycle.", "The start of the cycle is the duplicate number."],
        "topics": ["Array", "Two Pointers"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-11", "topic": "Arrays", "topic_order": 1, "problem_order": 11,
        "question_title": "Kadane's Algorithm",
        "statement": "Given an integer array nums, find the subarray with the largest sum, and return its sum. (This is the classic Kadane's Algorithm problem.)",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},
            {"input": "nums = [1]", "output": "1"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "9\n-2 1 -3 4 -1 2 1 -5 4", "expected": "6"},
            {"input": "1\n5", "expected": "5"}
        ],
        "hidden_test_cases": [
            {"input": "5\n5 -9 6 -2 3", "expected": "7"},
            {"input": "3\n-1 -2 -3", "expected": "-1"}
        ],
        "solution": {"approach": "Classic Kadane's: track current sum, reset when negative.", "code": "def maxSubArray(nums):\n    max_sum = nums[0]\n    curr_sum = nums[0]\n    for i in range(1, len(nums)):\n        curr_sum = max(nums[i], curr_sum + nums[i])\n        max_sum = max(max_sum, curr_sum)\n    return max_sum", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Initialize both max_sum and curr_sum with the first element.", "At each step, decide whether to extend or start fresh.", "The answer is the maximum curr_sum seen."],
        "topics": ["Array", "Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-12", "topic": "Arrays", "topic_order": 1, "problem_order": 12,
        "question_title": "Merge Two Sorted Arrays",
        "statement": "Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).",
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000"},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.50000"}
        ],
        "constraints": ["nums1.length == m", "nums2.length == n", "0 <= m <= 1000", "0 <= n <= 1000", "1 <= m + n <= 2000"],
        "visible_test_cases": [
            {"input": "2 1\n1 3\n2", "expected": "2.0"},
            {"input": "2 2\n1 2\n3 4", "expected": "2.5"}
        ],
        "hidden_test_cases": [
            {"input": "0 1\n\n1", "expected": "1.0"},
            {"input": "2 2\n1 1\n1 1", "expected": "1.0"},
            {"input": "1 0\n2\n", "expected": "2.0"}
        ],
        "solution": {"approach": "Binary search on the smaller array to partition both arrays correctly.", "code": "def findMedianSortedArrays(nums1, nums2):\n    if len(nums1) > len(nums2):\n        nums1, nums2 = nums2, nums1\n    m, n = len(nums1), len(nums2)\n    lo, hi = 0, m\n    while lo <= hi:\n        i = (lo + hi) // 2\n        j = (m + n + 1) // 2 - i\n        max_left_a = float('-inf') if i == 0 else nums1[i-1]\n        min_right_a = float('inf') if i == m else nums1[i]\n        max_left_b = float('-inf') if j == 0 else nums2[j-1]\n        min_right_b = float('inf') if j == n else nums2[j]\n        if max_left_a <= min_right_b and max_left_b <= min_right_a:\n            if (m + n) % 2 == 1:\n                return max(max_left_a, max_left_b)\n            else:\n                return (max(max_left_a, max_left_b) + min(min_right_a, min_right_b)) / 2\n        elif max_left_a > min_right_b:\n            hi = i - 1\n        else:\n            lo = i + 1", "time_complexity": "O(log(min(m,n)))", "space_complexity": "O(1)"},
        "hints": ["Binary search on the smaller array for correct partition.", "Left partition total size = (m+n+1)//2.", "Adjust binary search based on max_left vs min_right comparisons."],
        "topics": ["Array", "Binary Search"], "companies": ["Amazon", "Google", "Microsoft", "Goldman Sachs"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-13", "topic": "Arrays", "topic_order": 1, "problem_order": 13,
        "question_title": "Two Sum",
        "statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"}
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9", "Only one valid answer exists"],
        "visible_test_cases": [
            {"input": "4 9\n2 7 11 15", "expected": "0 1"},
            {"input": "3 6\n3 2 4", "expected": "1 2"}
        ],
        "hidden_test_cases": [
            {"input": "2 6\n3 3", "expected": "0 1"},
            {"input": "5 12\n1 5 3 7 9", "expected": "1 4"},
            {"input": "5 -8\n-1 -2 -3 -4 -5", "expected": "2 4"}
        ],
        "solution": {"approach": "Hash map: store seen values. Check complement at each step.", "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target - num], i]\n        seen[num] = i", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["For each number, check if its complement (target - num) exists.", "Use a hash map to store numbers you've seen.", "Return indices when complement is found."],
        "topics": ["Array", "Hash Table"], "companies": ["Google", "Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-14", "topic": "Arrays", "topic_order": 1, "problem_order": 14,
        "question_title": "Best Time to Buy and Sell Stock II",
        "statement": "You are given an array prices where prices[i] is the price of a given stock on the ith day. Find the maximum profit you can achieve. You may complete as many transactions as you like.",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "7"},
            {"input": "prices = [1,2,3,4,5]", "output": "4"}
        ],
        "constraints": ["1 <= prices.length <= 3 * 10^4", "0 <= prices[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "6\n7 1 5 3 6 4", "expected": "7"},
            {"input": "5\n1 2 3 4 5", "expected": "4"}
        ],
        "hidden_test_cases": [
            {"input": "5\n7 6 4 3 1", "expected": "0"},
            {"input": "3\n2 1 2", "expected": "1"},
            {"input": "6\n1 2 1 2 1 2", "expected": "3"}
        ],
        "solution": {"approach": "Greedy: add up all positive differences between consecutive days.", "code": "def maxProfit(prices):\n    profit = 0\n    for i in range(1, len(prices)):\n        if prices[i] > prices[i-1]:\n            profit += prices[i] - prices[i-1]\n    return profit", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["You can buy and sell on consecutive days.", "Just add up all positive price increases.", "This is a greedy approach — no need for complex DP."],
        "topics": ["Array", "Dynamic Programming"], "companies": ["Amazon", "Goldman Sachs", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-15", "topic": "Arrays", "topic_order": 1, "problem_order": 15,
        "question_title": "Repeat and Missing Number",
        "statement": "You are given a read-only array of n integers from 1 to n. Each number appears exactly once except for A which appears twice and B which is missing. Find A and B.",
        "examples": [
            {"input": "arr = [3,1,2,5,3]", "output": "3 4"},
            {"input": "arr = [1,1]", "output": "1 2"}
        ],
        "constraints": ["2 <= n <= 10^5", "1 <= arr[i] <= n"],
        "visible_test_cases": [
            {"input": "5\n3 1 2 5 3", "expected": "3 4"},
            {"input": "2\n1 1", "expected": "1 2"}
        ],
        "hidden_test_cases": [
            {"input": "3\n1 2 2", "expected": "2 3"},
            {"input": "4\n1 2 3 3", "expected": "3 4"},
            {"input": "6\n1 3 4 5 1 6", "expected": "1 2"}
        ],
        "solution": {"approach": "Use math: sum and sum of squares formulas to find A and B.", "code": "def findTwoElement(arr):\n    n = len(arr)\n    s = n * (n + 1) // 2\n    s2 = n * (n + 1) * (2 * n + 1) // 6\n    for num in arr:\n        s -= num\n        s2 -= num * num\n    missing = (s + s2 // s) // 2\n    repeat = missing - s\n    return [repeat, missing]", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use the formula for sum of first n natural numbers.", "Use the formula for sum of squares.", "Set up two equations with two unknowns."],
        "topics": ["Array", "Math"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-16", "topic": "Arrays", "topic_order": 1, "problem_order": 16,
        "question_title": "Count Inversions",
        "statement": "Given an array of integers arr[] of size n, find the count of pairs (i, j) such that i < j and arr[i] > arr[j].",
        "examples": [
            {"input": "arr = [2,4,3,5,1]", "output": "3"},
            {"input": "arr = [2,3,4,5,6]", "output": "0"}
        ],
        "constraints": ["1 <= n <= 10^5", "1 <= arr[i] <= 10^8"],
        "visible_test_cases": [
            {"input": "5\n2 4 3 5 1", "expected": "3"},
            {"input": "5\n2 3 4 5 6", "expected": "0"}
        ],
        "hidden_test_cases": [
            {"input": "1\n1", "expected": "0"},
            {"input": "4\n8 4 2 1", "expected": "6"},
            {"input": "3\n3 1 2", "expected": "2"}
        ],
        "solution": {"approach": "Modified merge sort: count inversions during merge step.", "code": "def mergeSort(arr, temp, left, right):\n    mid = (left + right) // 2\n    inv_count = 0\n    if left < right:\n        inv_count += mergeSort(arr, temp, left, mid)\n        inv_count += mergeSort(arr, temp, mid + 1, right)\n        inv_count += merge(arr, temp, left, mid, right)\n    return inv_count\ndef merge(arr, temp, left, mid, right):\n    i, j, k = left, mid + 1, left\n    inv_count = 0\n    while i <= mid and j <= right:\n        if arr[i] <= arr[j]:\n            temp[k] = arr[i]; i += 1\n        else:\n            temp[k] = arr[j]; j += 1; inv_count += (mid - i + 1)\n        k += 1\n    while i <= mid: temp[k] = arr[i]; i += 1; k += 1\n    while j <= right: temp[k] = arr[j]; j += 1; k += 1\n    for i in range(left, right + 1): arr[i] = temp[i]\n    return inv_count", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Use modified merge sort.", "Count inversions when right half element is smaller than left half.", "Inversions = mid - i + 1 for each such element."],
        "topics": ["Array", "Sorting"], "companies": ["Amazon", "Goldman Sachs", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-17", "topic": "Arrays", "topic_order": 1, "problem_order": 17,
        "question_title": "Reverse Pairs",
        "statement": "Given an integer array nums, return the number of reverse pairs. A reverse pair is a pair (i, j) where 0 <= i < j < n and nums[i] > 2 * nums[j].",
        "examples": [
            {"input": "nums = [1,3,2,3,1]", "output": "2"},
            {"input": "nums = [2,4,3,5,1]", "output": "3"}
        ],
        "constraints": ["1 <= nums.length <= 5 * 10^4", "-2^31 <= nums[i] <= 2^31 - 1"],
        "visible_test_cases": [
            {"input": "5\n1 3 2 3 1", "expected": "2"},
            {"input": "5\n2 4 3 5 1", "expected": "3"}
        ],
        "hidden_test_cases": [
            {"input": "1\n1", "expected": "0"},
            {"input": "4\n1 2 3 4", "expected": "0"},
            {"input": "4\n4 3 2 1", "expected": "4"}
        ],
        "solution": {"approach": "Modified merge sort with counting during merge step.", "code": "def reversePairs(nums):\n    def mergeSort(arr, left, right):\n        if left >= right: return 0\n        mid = (left + right) // 2\n        count = mergeSort(arr, left, mid) + mergeSort(arr, mid + 1, right)\n        j = mid + 1\n        for i in range(left, mid + 1):\n            while j <= right and arr[i] > 2 * arr[j]:\n                j += 1\n            count += j - (mid + 1)\n        arr[left:right+1] = sorted(arr[left:right+1])\n        return count\n    return mergeSort(nums, 0, len(nums) - 1)", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Similar to merge sort inversion count.", "During merge, count elements where arr[i] > 2*arr[j].", "Use two pointers in the merge step."],
        "topics": ["Array", "Sorting"], "companies": ["Amazon", "Google"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-18", "topic": "Arrays", "topic_order": 1, "problem_order": 18,
        "question_title": "Maximum Product Subarray",
        "statement": "Given an integer array nums, find a subarray that has the largest product, and return the product.",
        "examples": [
            {"input": "nums = [2,3,-2,4]", "output": "6"},
            {"input": "nums = [-2,0,-1]", "output": "0"}
        ],
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-10 <= nums[i] <= 10"],
        "visible_test_cases": [
            {"input": "4\n2 3 -2 4", "expected": "6"},
            {"input": "3\n-2 0 -1", "expected": "0"}
        ],
        "hidden_test_cases": [
            {"input": "3\n-2 3 -4", "expected": "24"},
            {"input": "5\n2 -5 -2 -4 3", "expected": "24"},
            {"input": "1\n-2", "expected": "-2"}
        ],
        "solution": {"approach": "Track both min and max products (negative can become positive).", "code": "def maxProduct(nums):\n    result = max(nums)\n    curr_min, curr_max = 1, 1\n    for num in nums:\n        vals = (num, num * curr_max, num * curr_min)\n        curr_max, curr_min = max(vals), min(vals)\n        result = max(result, curr_max)\n    return result", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Track both maximum and minimum products at each step.", "A negative number can flip min to max.", "Handle zero by resetting both trackers."],
        "topics": ["Array", "Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-19", "topic": "Arrays", "topic_order": 1, "problem_order": 19,
        "question_title": "Chocolate Distribution",
        "statement": "Given an array arr[] of n integers where arr[i] represents the number of chocolates in ith packet. There are m students, distribute chocolates such that each student gets exactly one packet and the difference between maximum and minimum chocolates is minimized.",
        "examples": [
            {"input": "arr = [7,3,2,4,9,12,56], m = 3", "output": "2"},
            {"input": "arr = [3,4,1,9,56,7,9,12], m = 5", "output": "5"}
        ],
        "constraints": ["2 <= n <= 10^5", "1 <= m <= n", "0 <= arr[i] <= 10^9"],
        "visible_test_cases": [
            {"input": "7 3\n7 3 2 4 9 12 56", "expected": "2"},
            {"input": "8 5\n3 4 1 9 56 7 9 12", "expected": "5"}
        ],
        "hidden_test_cases": [
            {"input": "3 2\n1 2 3", "expected": "1"},
            {"input": "4 3\n1 5 3 7", "expected": "2"}
        ],
        "solution": {"approach": "Sort array. Use sliding window of size m, find minimum difference.", "code": "def findMinDiff(arr, m):\n    arr.sort()\n    min_diff = float('inf')\n    for i in range(m - 1, len(arr)):\n        min_diff = min(min_diff, arr[i] - arr[i - m + 1])\n    return min_diff", "time_complexity": "O(n log n)", "space_complexity": "O(1)"},
        "hints": ["Sort the array first.", "Use a sliding window of size m.", "The minimum difference is the minimum of (last - first) in each window."],
        "topics": ["Array", "Sorting"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-20", "topic": "Arrays", "topic_order": 1, "problem_order": 20,
        "question_title": "Majority Element",
        "statement": "Given an array nums of size n, return the majority element (appears more than n/2 times).",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 5 * 10^4", "-10^9 <= nums[i] <= 10^9"],
        "visible_test_cases": [
            {"input": "3\n3 2 3", "expected": "3"},
            {"input": "7\n2 2 1 1 1 2 2", "expected": "2"}
        ],
        "hidden_test_cases": [
            {"input": "1\n1", "expected": "1"},
            {"input": "7\n1 2 1 2 1 2 1", "expected": "1"},
            {"input": "5\n6 5 5 5 5", "expected": "5"}
        ],
        "solution": {"approach": "Boyer-Moore Voting Algorithm.", "code": "def majorityElement(nums):\n    candidate, count = None, 0\n    for num in nums:\n        if count == 0:\n            candidate = num\n        count += 1 if num == candidate else -1\n    return candidate", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Think about what happens when you cancel out different elements.", "Use Boyer-Moore Voting Algorithm.", "The majority element survives the cancellation process."],
        "topics": ["Array"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-21", "topic": "Arrays", "topic_order": 1, "problem_order": 21,
        "question_title": "Trapping Rain Water",
        "statement": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"},
            {"input": "height = [4,2,0,3,2,5]", "output": "9"}
        ],
        "constraints": ["n == height.length", "1 <= n <= 2 * 10^4", "0 <= height[i] <= 10^5"],
        "visible_test_cases": [
            {"input": "12\n0 1 0 2 1 0 1 3 2 1 2 1", "expected": "6"},
            {"input": "6\n4 2 0 3 2 5", "expected": "9"}
        ],
        "hidden_test_cases": [
            {"input": "1\n1", "expected": "0"},
            {"input": "2\n1 1", "expected": "0"},
            {"input": "5\n4 2 0 2 4", "expected": "6"}
        ],
        "solution": {"approach": "Two pointers: track left_max and right_max, water = min(left_max, right_max) - height[i].", "code": "def trap(height):\n    left, right = 0, len(height) - 1\n    left_max, right_max = 0, 0\n    water = 0\n    while left < right:\n        if height[left] < height[right]:\n            if height[left] >= left_max:\n                left_max = height[left]\n            else:\n                water += left_max - height[left]\n            left += 1\n        else:\n            if height[right] >= right_max:\n                right_max = height[right]\n            else:\n                water += right_max - height[right]\n            right -= 1\n    return water", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Water at each position = min(left_max, right_max) - height[i].", "Use two pointers from both ends.", "Move the pointer with smaller height."],
        "topics": ["Array", "Stack"], "companies": ["Amazon", "Google", "Microsoft", "Goldman Sachs"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-22", "topic": "Arrays", "topic_order": 1, "problem_order": 22,
        "question_title": "3Sum",
        "statement": "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"},
            {"input": "nums = [0,1,1]", "output": "[]"}
        ],
        "constraints": ["3 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
        "visible_test_cases": [
            {"input": "6\n-1 0 1 2 -1 -4", "expected": "-1 -1 2\n-1 0 1"},
            {"input": "3\n0 1 1", "expected": ""}
        ],
        "hidden_test_cases": [
            {"input": "3\n0 0 0", "expected": "0 0 0"},
            {"input": "4\n-2 -1 1 2", "expected": "-2 1 1"}
        ],
        "solution": {"approach": "Sort array. Fix one element, use two pointers for the rest.", "code": "def threeSum(nums):\n    nums.sort()\n    result = []\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i-1]: continue\n        left, right = i + 1, len(nums) - 1\n        while left < right:\n            total = nums[i] + nums[left] + nums[right]\n            if total == 0:\n                result.append([nums[i], nums[left], nums[right]])\n                while left < right and nums[left] == nums[left+1]: left += 1\n                while left < right and nums[right] == nums[right-1]: right -= 1\n                left += 1; right -= 1\n            elif total < 0: left += 1\n            else: right -= 1\n    return result", "time_complexity": "O(n^2)", "space_complexity": "O(1)"},
        "hints": ["Sort the array first.", "Fix one element and use two pointers for the other two.", "Skip duplicates to avoid duplicate triplets."],
        "topics": ["Array", "Two Pointers"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-23", "topic": "Arrays", "topic_order": 1, "problem_order": 23,
        "question_title": "Container With Most Water",
        "statement": "Given n non-negative integers a1, a2, ..., an where each represents a point. Find two lines that together with the x-axis form a container that holds the most water.",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49"},
            {"input": "height = [1,1]", "output": "1"}
        ],
        "constraints": ["n == height.length", "2 <= n <= 10^5", "0 <= height[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "9\n1 8 6 2 5 4 8 3 7", "expected": "49"},
            {"input": "2\n1 1", "expected": "1"}
        ],
        "hidden_test_cases": [
            {"input": "3\n1 2 1", "expected": "2"},
            {"input": "4\n4 3 2 1 4", "expected": "16"},
            {"input": "5\n1 2 1 2 1", "expected": "4"}
        ],
        "solution": {"approach": "Two pointers from both ends. Move the shorter pointer inward.", "code": "def maxArea(height):\n    left, right = 0, len(height) - 1\n    max_water = 0\n    while left < right:\n        water = min(height[left], height[right]) * (right - left)\n        max_water = max(max_water, water)\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return max_water", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Start with the widest container.", "Move the pointer with smaller height inward.", "The width decreases but height might increase."],
        "topics": ["Array", "Two Pointers"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-24", "topic": "Arrays", "topic_order": 1, "problem_order": 24,
        "question_title": "Remove Duplicates from Sorted Array",
        "statement": "Given a sorted array nums, remove the duplicates in-place such that each element appears only once and return the new length.",
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2"},
            {"input": "nums = [0,0,1,1,1,2,2,3,3,4]", "output": "5"}
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-100 <= nums[i] <= 100", "nums is sorted in non-decreasing order"],
        "visible_test_cases": [
            {"input": "3\n1 1 2", "expected": "2"},
            {"input": "10\n0 0 1 1 1 2 2 3 3 4", "expected": "5"}
        ],
        "hidden_test_cases": [
            {"input": "3\n1 1 1", "expected": "1"},
            {"input": "5\n1 2 3 4 5", "expected": "5"},
            {"input": "1\n1", "expected": "1"}
        ],
        "solution": {"approach": "Two pointers: i for unique elements, j for scanning.", "code": "def removeDuplicates(nums):\n    if not nums: return 0\n    i = 0\n    for j in range(1, len(nums)):\n        if nums[j] != nums[i]:\n            i += 1\n            nums[i] = nums[j]\n    return i + 1", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use a pointer for the position of unique elements.", "When you find a new unique element, move it forward.", "The count of unique elements is i+1."],
        "topics": ["Array", "Two Pointers"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-25", "topic": "Arrays", "topic_order": 1, "problem_order": 25,
        "question_title": "Move All Zeroes to End",
        "statement": "Given an integer array nums, move all 0's to the end while maintaining the relative order of non-zero elements.",
        "examples": [
            {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]"},
            {"input": "nums = [0]", "output": "[0]"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 100"],
        "visible_test_cases": [
            {"input": "5\n0 1 0 3 12", "expected": "1 3 12 0 0"},
            {"input": "1\n0", "expected": "0"}
        ],
        "hidden_test_cases": [
            {"input": "3\n0 0 1", "expected": "0 0 1"},
            {"input": "4\n1 2 3 4", "expected": "1 2 3 4"},
            {"input": "5\n0 0 0 0 1", "expected": "0 0 0 0 1"}
        ],
        "solution": {"approach": "Two pointers: one for next non-zero position.", "code": "def moveZeroes(nums):\n    insert_pos = 0\n    for num in nums:\n        if num != 0:\n            nums[insert_pos] = num\n            insert_pos += 1\n    for i in range(insert_pos, len(nums)):\n        nums[i] = 0", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Keep a pointer for where the next non-zero should go.", "Move all non-zero elements forward.", "Fill the rest with zeros."],
        "topics": ["Array", "Two Pointers"], "companies": ["Amazon", "Microsoft", "TCS"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-26", "topic": "Arrays", "topic_order": 1, "problem_order": 26,
        "question_title": "Rotate Array",
        "statement": "Given an integer array nums, rotate the array to the right by k steps.",
        "examples": [
            {"input": "nums = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]"},
            {"input": "nums = [-1,-100,3,99], k = 2", "output": "[3,99,-1,-100]"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-2^31 <= nums[i] <= 2^31 - 1", "0 <= k <= 10^5"],
        "visible_test_cases": [
            {"input": "7 3\n1 2 3 4 5 6 7", "expected": "5 6 7 1 2 3 4"},
            {"input": "4 2\n-1 -100 3 99", "expected": "3 99 -1 -100"}
        ],
        "hidden_test_cases": [
            {"input": "3 2\n1 2 3", "expected": "2 3 1"},
            {"input": "3 0\n1 2 3", "expected": "1 2 3"},
            {"input": "2 1\n1 2", "expected": "2 1"}
        ],
        "solution": {"approach": "Reverse the entire array, then reverse first k elements, then reverse the rest.", "code": "def rotate(nums, k):\n    n = len(nums)\n    k %= n\n    nums.reverse()\n    nums[:k] = reversed(nums[:k])\n    nums[k:] = reversed(nums[k:])", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Handle k > n by doing k % n.", "Reverse the entire array first.", "Then reverse the first k elements and the remaining elements separately."],
        "topics": ["Array"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-27", "topic": "Arrays", "topic_order": 1, "problem_order": 27,
        "question_title": "Missing Number",
        "statement": "Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing.",
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2"},
            {"input": "nums = [0,1]", "output": "2"}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 10^4", "0 <= nums[i] <= n"],
        "visible_test_cases": [
            {"input": "3\n3 0 1", "expected": "2"},
            {"input": "2\n0 1", "expected": "2"}
        ],
        "hidden_test_cases": [
            {"input": "1\n0", "expected": "1"},
            {"input": "5\n9,6,4,2,3,5,7,0,1,8", "expected": "10"}
        ],
        "solution": {"approach": "XOR all indices and values. Missing = XOR of all.", "code": "def missingNumber(nums):\n    result = len(nums)\n    for i, num in enumerate(nums):\n        result ^= i ^ num\n    return result", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["XOR of a number with itself is 0.", "XOR all indices [0..n] with all array elements.", "The result is the missing number."],
        "topics": ["Array", "Math"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-28", "topic": "Arrays", "topic_order": 1, "problem_order": 28,
        "question_title": "Longest Consecutive Sequence",
        "statement": "Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence. Must run in O(n) time.",
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4"},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9"}
        ],
        "constraints": ["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "visible_test_cases": [
            {"input": "6\n100 4 200 1 3 2", "expected": "4"},
            {"input": "10\n0 3 7 2 5 8 4 6 0 1", "expected": "9"}
        ],
        "hidden_test_cases": [
            {"input": "0", "expected": "0"},
            {"input": "1\n0", "expected": "1"},
            {"input": "9\n0 3 7 2 5 8 4 6 0", "expected": "9"}
        ],
        "solution": {"approach": "Use a set. For each number, check if it's the start of a sequence.", "code": "def longestConsecutive(nums):\n    num_set = set(nums)\n    longest = 0\n    for num in num_set:\n        if num - 1 not in num_set:\n            current = num\n            length = 1\n            while current + 1 in num_set:\n                current += 1\n                length += 1\n            longest = max(longest, length)\n    return longest", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use a HashSet for O(1) lookups.", "Only start counting from sequence beginnings (num-1 not in set).", "Count consecutive numbers from each starting point."],
        "topics": ["Array", "Hash Table"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-29", "topic": "Arrays", "topic_order": 1, "problem_order": 29,
        "question_title": "Count of Smaller Numbers After Self",
        "statement": "Given an integer array nums, return an integer array counts where counts[i] is the number of smaller elements to the right of nums[i].",
        "examples": [
            {"input": "nums = [5,2,6,1]", "output": "[2,1,1,0]"},
            {"input": "nums = [-1]", "output": "[0]"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [
            {"input": "4\n5 2 6 1", "expected": "2 1 1 0"},
            {"input": "1\n-1", "expected": "0"}
        ],
        "hidden_test_cases": [
            {"input": "3\n3 2 1", "expected": "2 1 0"},
            {"input": "3\n1 2 3", "expected": "0 0 0"}
        ],
        "solution": {"approach": "Merge sort approach: count inversions during merge.", "code": "def countSmaller(nums):\n    def mergeSort(indices):\n        if len(indices) <= 1: return indices\n        mid = len(indices) // 2\n        left = mergeSort(indices[:mid])\n        right = mergeSort(indices[mid:])\n        merged = []\n        i = j = 0\n        while i < len(left) and j < len(right):\n            if nums[left[i]] <= nums[right[j]]:\n                merged.append(left[i])\n                count[left[i]] += j\n                i += 1\n            else:\n                merged.append(right[j])\n                j += 1\n        while i < len(left):\n            merged.append(left[i])\n            count[left[i]] += j\n            i += 1\n        merged.extend(right[j:])\n        return merged\n    count = [0] * len(nums)\n    mergeSort(list(range(len(nums))))\n    return count", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Use merge sort to count inversions.", "Track original indices through the sort.", "When a right element is smaller, count how many left elements are after it."],
        "topics": ["Array", "Sorting"], "companies": ["Amazon", "Google"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "A1-30", "topic": "Arrays", "topic_order": 1, "problem_order": 30,
        "question_title": "Subarray Sum Equals K",
        "statement": "Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.",
        "examples": [
            {"input": "nums = [1,1,1], k = 2", "output": "2"},
            {"input": "nums = [1,2,3], k = 3", "output": "2"}
        ],
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-1000 <= nums[i] <= 1000", "-10^7 <= k <= 10^7"],
        "visible_test_cases": [
            {"input": "3 2\n1 1 1", "expected": "2"},
            {"input": "3 3\n1 2 3", "expected": "2"}
        ],
        "hidden_test_cases": [
            {"input": "5 7\n3 4 7 2 -3 1 4 2", "expected": "2"},
            {"input": "1 0\n0", "expected": "1"}
        ],
        "solution": {"approach": "Prefix sum + hash map. For each prefix sum, check if (sum - k) exists.", "code": "def subarraySum(nums, k):\n    count = 0\n    prefix_sum = 0\n    seen = {0: 1}\n    for num in nums:\n        prefix_sum += num\n        if prefix_sum - k in seen:\n            count += seen[prefix_sum - k]\n        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1\n    return count", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use prefix sums.", "For each prefix sum, check if prefix_sum - k exists.", "Use a hash map to store prefix sum frequencies."],
        "topics": ["Array", "Hash Table"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # TOPIC 2: LINKED LISTS — 30 problems
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "LL-01", "topic": "Linked Lists", "topic_order": 2, "problem_order": 1,
        "question_title": "Reverse a Linked List",
        "statement": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "examples": [{"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"}, {"input": "head = [1,2]", "output": "[2,1]"}],
        "constraints": ["The number of nodes is in the range [0, 5000]", "-5000 <= Node.val <= 5000"],
        "visible_test_cases": [{"input": "5\n1 2 3 4 5", "expected": "5 4 3 2 1"}, {"input": "2\n1 2", "expected": "2 1"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "0", "expected": ""}, {"input": "3\n1 2 3", "expected": "3 2 1"}],
        "solution": {"approach": "Iterative: use prev, curr, next pointers to reverse links.", "code": "def reverseList(head):\n    prev, curr = None, head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use three pointers: prev, curr, next.", "Reverse each link as you traverse.", "prev will be the new head at the end."],
        "topics": ["Linked List"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-02", "topic": "Linked Lists", "topic_order": 2, "problem_order": 2,
        "question_title": "Find the Middle of Linked List",
        "statement": "Given the head of a singly linked list, return the middle node. If there are two middle nodes, return the second middle node.",
        "examples": [{"input": "head = [1,2,3,4,5]", "output": "[3,4,5]"}, {"input": "head = [1,2,3,4,5,6]", "output": "[4,5,6]"}],
        "constraints": ["The number of nodes is in the range [1, 100]", "1 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "5\n1 2 3 4 5", "expected": "3"}, {"input": "6\n1 2 3 4 5 6", "expected": "4"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "2\n1 2", "expected": "2"}, {"input": "3\n1 2 3", "expected": "2"}],
        "solution": {"approach": "Tortoise and hare: slow moves 1 step, fast moves 2 steps.", "code": "def middleNode(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use two pointers moving at different speeds.", "When fast reaches the end, slow is at the middle.", "This is the classic tortoise and hare algorithm."],
        "topics": ["Linked List", "Two Pointers"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-03", "topic": "Linked Lists", "topic_order": 2, "problem_order": 3,
        "question_title": "Merge Two Sorted Linked Lists",
        "statement": "Given the heads of two sorted linked lists list1 and list2, merge them into one sorted list.",
        "examples": [{"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]"}, {"input": "list1 = [], list2 = []", "output": "[]"}],
        "constraints": ["Both lists are sorted in non-decreasing order", "The number of nodes in each list is in [0, 50]"],
        "visible_test_cases": [{"input": "3\n1 2 4\n3\n1 3 4", "expected": "1 1 2 3 4 4"}, {"input": "0\n\n0\n", "expected": ""}],
        "hidden_test_cases": [{"input": "1\n1\n1\n2", "expected": "1 2"}, {"input": "2\n1 3\n1\n2", "expected": "1 2 3"}, {"input": "1\n5\n0\n", "expected": "5"}],
        "solution": {"approach": "Use a dummy node and two pointers to merge.", "code": "def mergeTwoLists(list1, list2):\n    dummy = ListNode(0)\n    curr = dummy\n    while list1 and list2:\n        if list1.val <= list2.val:\n            curr.next = list1\n            list1 = list1.next\n        else:\n            curr.next = list2\n            list2 = list2.next\n        curr = curr.next\n    curr.next = list1 or list2\n    return dummy.next", "time_complexity": "O(n+m)", "space_complexity": "O(1)"},
        "hints": ["Use a dummy node to simplify edge cases.", "Compare nodes and attach the smaller one.", "Attach the remaining list at the end."],
        "topics": ["Linked List"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-04", "topic": "Linked Lists", "topic_order": 2, "problem_order": 4,
        "question_title": "Remove N-th Node From End of List",
        "statement": "Given the head of a linked list, remove the n-th node from the end and return its head.",
        "examples": [{"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"}, {"input": "head = [1], n = 1", "output": "[]"}],
        "constraints": ["The number of nodes is in [1, 30]", "1 <= n <= size"],
        "visible_test_cases": [{"input": "5 2\n1 2 3 4 5", "expected": "1 2 3 5"}, {"input": "1 1\n1", "expected": ""}],
        "hidden_test_cases": [{"input": "2 1\n1 2", "expected": "1"}, {"input": "3 3\n1 2 3", "expected": "2 3"}, {"input": "2 2\n1 2", "expected": "2"}],
        "solution": {"approach": "Two pointers with n gap. Use dummy node.", "code": "def removeNthFromEnd(head, n):\n    dummy = ListNode(0, head)\n    fast = slow = dummy\n    for _ in range(n + 1): fast = fast.next\n    while fast:\n        fast = fast.next\n        slow = slow.next\n    slow.next = slow.next.next\n    return dummy.next", "time_complexity": "O(L)", "space_complexity": "O(1)"},
        "hints": ["Use a dummy node to handle edge cases.", "Advance fast pointer n steps ahead.", "When fast reaches end, slow is right before the target."],
        "topics": ["Linked List", "Two Pointers"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-05", "topic": "Linked Lists", "topic_order": 2, "problem_order": 5,
        "question_title": "Add Two Numbers",
        "statement": "You are given two non-empty linked lists representing two non-negative integers. Add the two numbers and return the sum as a linked list.",
        "examples": [{"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]"}, {"input": "l1 = [0], l2 = [0]", "output": "[0]"}],
        "constraints": ["Each list has [1, 100] nodes", "0 <= Node.val <= 9"],
        "visible_test_cases": [{"input": "3\n2 4 3\n3\n5 6 4", "expected": "7 0 8"}, {"input": "1\n0\n1\n0", "expected": "0"}],
        "hidden_test_cases": [{"input": "3\n9 9 9\n3\n9 9 9", "expected": "9 9 9 8"}, {"input": "1\n5\n1\n5", "expected": "0 1"}, {"input": "2\n2 4\n1\n5 6 4", "expected": "7 0 5"}],
        "solution": {"approach": "Simulate digit-by-digit addition with carry.", "code": "def addTwoNumbers(l1, l2):\n    dummy = ListNode(0)\n    curr = dummy\n    carry = 0\n    while l1 or l2 or carry:\n        val = carry\n        if l1: val += l1.val; l1 = l1.next\n        if l2: val += l2.val; l2 = l2.next\n        carry = val // 10\n        curr.next = ListNode(val % 10)\n        curr = curr.next\n    return dummy.next", "time_complexity": "O(max(m,n))", "space_complexity": "O(max(m,n))"},
        "hints": ["Traverse both lists simultaneously.", "Handle carry between digits.", "Don't forget the final carry."],
        "topics": ["Linked List", "Math"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-06", "topic": "Linked Lists", "topic_order": 2, "problem_order": 6,
        "question_title": "Detect a Cycle in Linked List",
        "statement": "Given head, the head of a linked list, determine if the linked list has a cycle in it.",
        "examples": [{"input": "head = [3,2,0,-4], pos = 1", "output": "true"}, {"input": "head = [1,2], pos = -1", "output": "false"}],
        "constraints": ["The number of nodes is in [0, 10^4]", "-10^5 <= Node.val <= 10^5"],
        "visible_test_cases": [{"input": "4 1\n3 2 0 -4", "expected": "true"}, {"input": "2 -1\n1 2", "expected": "false"}],
        "hidden_test_cases": [{"input": "1 0\n1", "expected": "true"}, {"input": "1 -1\n1", "expected": "false"}, {"input": "0 -1", "expected": "false"}],
        "solution": {"approach": "Floyd's cycle detection: slow and fast pointers.", "code": "def hasCycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use two pointers moving at different speeds.", "If they meet, there's a cycle.", "If fast reaches null, no cycle."],
        "topics": ["Linked List", "Two Pointers"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-07", "topic": "Linked Lists", "topic_order": 2, "problem_order": 7,
        "question_title": "Intersection of Two Linked Lists",
        "statement": "Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect.",
        "examples": [{"input": "listA = [4,1,8,4,5], listB = [5,6,1,8,4,5]", "output": "Node with value 8"}, {"input": "listA = [1,9,1], listB = [3]", "output": "null"}],
        "constraints": ["Both lists are non-cyclic", "The number of nodes in each list is in [0, 10^4]"],
        "visible_test_cases": [{"input": "5\n4 1 8 4 5\n6\n5 6 1 8 4 5", "expected": "8"}, {"input": "3\n1 9 1\n1\n3", "expected": "-1"}],
        "hidden_test_cases": [{"input": "2\n1 2\n2\n3 4", "expected": "-1"}, {"input": "1\n1\n1\n1", "expected": "1"}, {"input": "3\n1 2 3\n3\n4 5 3", "expected": "3"}],
        "solution": {"approach": "Two pointers: when one reaches end, redirect to other list's head.", "code": "def getIntersectionNode(headA, headB):\n    a, b = headA, headB\n    while a != b:\n        a = a.next if a else headB\n        b = b.next if b else headA\n    return a", "time_complexity": "O(m+n)", "space_complexity": "O(1)"},
        "hints": ["Both pointers traverse m+n steps total.", "When a pointer reaches the end, redirect it to the other head.", "They will meet at the intersection or both become null."],
        "topics": ["Linked List"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-08", "topic": "Linked Lists", "topic_order": 2, "problem_order": 8,
        "question_title": "Reverse Nodes in k-Group",
        "statement": "Given the head of a linked list, reverse the nodes k at a time and return the modified list.",
        "examples": [{"input": "head = [1,2,3,4,5], k = 2", "output": "[2,1,4,3,5]"}, {"input": "head = [1,2,3,4,5], k = 3", "output": "[3,2,1,4,5]"}],
        "constraints": ["1 <= k <= n <= 5000", "0 <= Node.val <= 1000"],
        "visible_test_cases": [{"input": "5 2\n1 2 3 4 5", "expected": "2 1 4 3 5"}, {"input": "5 3\n1 2 3 4 5", "expected": "3 2 1 4 5"}],
        "hidden_test_cases": [{"input": "3 2\n1 2 3", "expected": "2 1 3"}, {"input": "1 1\n1", "expected": "1"}, {"input": "4 4\n1 2 3 4", "expected": "4 3 2 1"}],
        "solution": {"approach": "Reverse k nodes at a time using a helper function.", "code": "def reverseKGroup(head, k):\n    def reverse(start, end):\n        prev, curr = None, start\n        while curr != end:\n            nxt = curr.next\n            curr.next = prev\n            prev = curr\n            curr = nxt\n        return prev\n    dummy = ListNode(0, head)\n    group_prev = dummy\n    while True:\n        kth = group_prev\n        for _ in range(k):\n            kth = kth.next\n            if not kth: return dummy.next\n        group_next = kth.next\n        prev, curr = group_prev.next, group_prev.next\n        for _ in range(k):\n            nxt = curr.next\n            curr.next = prev\n            prev = curr\n            curr = nxt\n        group_prev.next = prev\n        curr.next = group_next\n        group_prev = curr.next\n    return dummy.next", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["First check if there are k nodes remaining.", "Reverse the k nodes.", "Connect the reversed group back to the list."],
        "topics": ["Linked List"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-09", "topic": "Linked Lists", "topic_order": 2, "problem_order": 9,
        "question_title": "Rotate a Linked List",
        "statement": "Given the head of a linked list, rotate the list to the right by k places.",
        "examples": [{"input": "head = [1,2,3,4,5], k = 2", "output": "[4,5,1,2,3]"}, {"input": "head = [0,1,2], k = 4", "output": "[2,0,1]"}],
        "constraints": ["The number of nodes is in [0, 500]", "-10^9 <= Node.val <= 10^9"],
        "visible_test_cases": [{"input": "5 2\n1 2 3 4 5", "expected": "4 5 1 2 3"}, {"input": "3 4\n0 1 2", "expected": "2 0 1"}],
        "hidden_test_cases": [{"input": "1 0\n1", "expected": "1"}, {"input": "2 1\n1 2", "expected": "2 1"}, {"input": "3 0\n1 2 3", "expected": "1 2 3"}],
        "solution": {"approach": "Make it circular, break at the right point.", "code": "def rotateRight(head, k):\n    if not head or not head.next or k == 0: return head\n    length = 1\n    tail = head\n    while tail.next:\n        tail = tail.next\n        length += 1\n    k %= length\n    if k == 0: return head\n    tail.next = head\n    new_tail = head\n    for _ in range(length - k - 1):\n        new_tail = new_tail.next\n    new_head = new_tail.next\n    new_tail.next = None\n    return new_head", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Make the list circular by connecting tail to head.", "The new tail is at position (length - k - 1).", "Break the circle at the new tail."],
        "topics": ["Linked List"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-10", "topic": "Linked Lists", "topic_order": 2, "problem_order": 10,
        "question_title": "Palindrome Linked List",
        "statement": "Given the head of a singly linked list, return true if it is a palindrome.",
        "examples": [{"input": "head = [1,2,2,1]", "output": "true"}, {"input": "head = [1,2]", "output": "false"}],
        "constraints": ["The number of nodes is in [1, 10^5]", "0 <= Node.val <= 9"],
        "visible_test_cases": [{"input": "4\n1 2 2 1", "expected": "true"}, {"input": "2\n1 2", "expected": "false"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "true"}, {"input": "3\n1 2 1", "expected": "true"}, {"input": "2\n0 0", "expected": "true"}],
        "solution": {"approach": "Find middle, reverse second half, compare.", "code": "def isPalindrome(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    prev = None\n    while slow:\n        nxt = slow.next\n        slow.next = prev\n        prev = slow\n        slow = nxt\n    left, right = head, prev\n    while right:\n        if left.val != right.val: return False\n        left = left.next\n        right = right.next\n    return True", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Find the middle of the list using slow/fast pointers.", "Reverse the second half.", "Compare the first half with the reversed second half."],
        "topics": ["Linked List", "Two Pointers"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-11", "topic": "Linked Lists", "topic_order": 2, "problem_order": 11,
        "question_title": "Merge k Sorted Lists",
        "statement": "You are given an array of k linked-lists lists. Merge all the lists into one sorted list.",
        "examples": [{"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]"}, {"input": "lists = []", "output": "[]"}],
        "constraints": ["k == lists.length", "0 <= k <= 10^4", "0 <= Node.val <= 10^4"],
        "visible_test_cases": [{"input": "3\n3\n1 4 5\n3\n1 3 4\n2\n2 6", "expected": "1 1 2 3 4 4 5 6"}, {"input": "0", "expected": ""}],
        "hidden_test_cases": [{"input": "1\n1\n1", "expected": "1"}, {"input": "3\n1\n1\n1\n2\n1\n3", "expected": "1 2 3"}, {"input": "2\n0\n\n1\n0", "expected": "0"}],
        "solution": {"approach": "Use a min-heap to always pick the smallest node.", "code": "import heapq\ndef mergeKLists(lists):\n    dummy = ListNode(0)\n    curr = dummy\n    heap = []\n    for i, l in enumerate(lists):\n        if l: heapq.heappush(heap, (l.val, i, l))\n    while heap:\n        val, i, node = heapq.heappop(heap)\n        curr.next = node\n        curr = curr.next\n        if node.next:\n            heapq.heappush(heap, (node.next.val, i, node.next))\n    return dummy.next", "time_complexity": "O(N log k)", "space_complexity": "O(k)"},
        "hints": ["Use a min-heap (priority queue).", "Push the head of each list into the heap.", "Always pop the smallest and push its next node."],
        "topics": ["Linked List", "Heap"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-12", "topic": "Linked Lists", "topic_order": 2, "problem_order": 12,
        "question_title": "Copy List with Random Pointer",
        "statement": "A linked list of length n where each node has an additional random pointer that could point to any node in the list. Construct a deep copy.",
        "examples": [{"input": "head = [[7,null],[13,0],[11,4],[10,2],[1,0]]", "output": "Deep copy of the list"}, {"input": "head = [[1,1],[2,1]]", "output": "Deep copy of the list"}],
        "constraints": ["0 <= n <= 1000", "-10^4 <= Node.val <= 10^4"],
        "visible_test_cases": [{"input": "5\n7 -1\n13 0\n11 4\n10 2\n1 0", "expected": "copied"}, {"input": "2\n1 1\n2 1", "expected": "copied"}],
        "hidden_test_cases": [{"input": "1\n1 -1", "expected": "copied"}, {"input": "3\n1 1\n2 0\n3 -1", "expected": "copied"}, {"input": "0", "expected": ""}],
        "solution": {"approach": "Interleave new nodes, set random pointers, then separate.", "code": "def copyRandomList(head):\n    if not head: return None\n    curr = head\n    while curr:\n        new = ListNode(curr.val, curr.next, None)\n        curr.next = new\n        curr = new.next\n    curr = head\n    while curr:\n        if curr.random: curr.next.random = curr.random.next\n        curr = curr.next.next\n    new_head = head.next\n    curr = head\n    while curr:\n        copy = curr.next\n        curr.next = copy.next\n        if copy.next: copy.next = copy.next.next\n        curr = curr.next\n    return new_head", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Insert a copy of each node right after the original.", "Set random pointers using the interleaved structure.", "Separate the copied list from the original."],
        "topics": ["Linked List", "Hash Table"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-13", "topic": "Linked Lists", "topic_order": 2, "problem_order": 13,
        "question_title": "LRU Cache",
        "statement": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement get and put in O(1) time.",
        "examples": [{"input": "LRUCache(2), put(1,1), put(2,2), get(1), put(3,3), get(2)", "output": "1, -1"}, {"input": "LRUCache(1), put(2,1), get(2), put(3,2), get(2)", "output": "1, -1"}],
        "constraints": ["1 <= capacity <= 3000", "0 <= key <= 10^4", "0 <= value <= 10^5"],
        "visible_test_cases": [{"input": "2\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2", "expected": "1\n-1"}, {"input": "1\nput 2 1\nget 2\nput 3 2\nget 2", "expected": "1\n-1"}],
        "hidden_test_cases": [{"input": "2\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\nget 3", "expected": "1\n-1\n3"}, {"input": "3\nput 1 1\nput 2 2\nput 3 3\nget 1\nput 4 4\nget 2", "expected": "1\n-1"}, {"input": "2\nget 1", "expected": "-1"}],
        "solution": {"approach": "HashMap + doubly linked list for O(1) get/put.", "code": "class Node:\n    def __init__(self, key=0, val=0):\n        self.key, self.val = key, val\n        self.prev = self.next = None\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cap = capacity\n        self.cache = {}\n        self.head, self.tail = Node(), Node()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n    def _remove(self, node):\n        node.prev.next = node.next\n        node.next.prev = node.prev\n    def _add_front(self, node):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n    def get(self, key):\n        if key in self.cache:\n            node = self.cache[key]\n            self._remove(node)\n            self._add_front(node)\n            return node.val\n        return -1\n    def put(self, key, value):\n        if key in self.cache:\n            self._remove(self.cache[key])\n        node = Node(key, value)\n        self._add_front(node)\n        self.cache[key] = node\n        if len(self.cache) > self.cap:\n            lru = self.tail.prev\n            self._remove(lru)\n            del self.cache[lru.key]", "time_complexity": "O(1)", "space_complexity": "O(capacity)"},
        "hints": ["Use a HashMap for O(1) access and a doubly linked list for O(1) ordering.", "Move accessed nodes to the front.", "Evict the node before the tail when capacity exceeded."],
        "topics": ["Linked List", "Hash Table", "Design"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-14", "topic": "Linked Lists", "topic_order": 2, "problem_order": 14,
        "question_title": "Odd Even Linked List",
        "statement": "Group all odd-indexed nodes together followed by even-indexed nodes. Do not alter the values, only re-order nodes.",
        "examples": [{"input": "head = [1,2,3,4,5]", "output": "[1,3,5,2,4]"}, {"input": "head = [2,1,3,5,6,4,7]", "output": "[2,3,6,7,1,5,4]"}],
        "constraints": ["n == number of nodes", "0 <= n <= 10^4"],
        "visible_test_cases": [{"input": "5\n1 2 3 4 5", "expected": "1 3 5 2 4"}, {"input": "7\n2 1 3 5 6 4 7", "expected": "2 3 6 7 1 5 4"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "2\n1 2", "expected": "1 2"}, {"input": "0", "expected": ""}],
        "solution": {"approach": "Separate odd and even chains, then connect.", "code": "def oddEvenList(head):\n    if not head: return head\n    odd = head\n    even = head.next\n    even_head = even\n    while even and even.next:\n        odd.next = even.next\n        odd = odd.next\n        even.next = odd.next\n        even = even.next\n    odd.next = even_head\n    return head", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Keep two pointers: one for odd, one for even.", "Connect odd nodes together, even nodes together.", "Link the end of odd list to the head of even list."],
        "topics": ["Linked List"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-15", "topic": "Linked Lists", "topic_order": 2, "problem_order": 15,
        "question_title": "Swap Nodes in Pairs",
        "statement": "Given a linked list, swap every two adjacent nodes and return its head.",
        "examples": [{"input": "head = [1,2,3,4]", "output": "[2,1,4,3]"}, {"input": "head = [1]", "output": "[1]"}],
        "constraints": ["1 <= n <= 100", "0 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "4\n1 2 3 4", "expected": "2 1 4 3"}, {"input": "1\n1", "expected": "1"}],
        "hidden_test_cases": [{"input": "2\n1 2", "expected": "2 1"}, {"input": "3\n1 2 3", "expected": "2 1 3"}, {"input": "0", "expected": ""}],
        "solution": {"approach": "Use dummy node, swap pairs by relinking.", "code": "def swapPairs(head):\n    dummy = ListNode(0, head)\n    prev = dummy\n    while prev.next and prev.next.next:\n        a = prev.next\n        b = a.next\n        prev.next = b\n        a.next = b.next\n        b.next = a\n        prev = a\n    return dummy.next", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use a dummy node before the head.", "For each pair, relink three pointers.", "Move prev forward by 2 positions after each swap."],
        "topics": ["Linked List"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-16", "topic": "Linked Lists", "topic_order": 2, "problem_order": 16,
        "question_title": "Remove Duplicates from Sorted List",
        "statement": "Given the head of a sorted linked list, delete all duplicates such that each element appears only once.",
        "examples": [{"input": "head = [1,1,2]", "output": "[1,2]"}, {"input": "head = [1,1,2,3,3]", "output": "[1,2,3]"}],
        "constraints": ["The number of nodes is in [0, 300]", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "3\n1 1 2", "expected": "1 2"}, {"input": "5\n1 1 2 3 3", "expected": "1 2 3"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "0", "expected": ""}, {"input": "4\n1 1 1 1", "expected": "1"}],
        "solution": {"approach": "Compare current with next, skip duplicates.", "code": "def deleteDuplicates(head):\n    curr = head\n    while curr and curr.next:\n        if curr.val == curr.next.val:\n            curr.next = curr.next.next\n        else:\n            curr = curr.next\n    return head", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Compare each node with its next node.", "If they're equal, skip the next node.", "Otherwise, move to the next node."],
        "topics": ["Linked List"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-17", "topic": "Linked Lists", "topic_order": 2, "problem_order": 17,
        "question_title": "Reorder List",
        "statement": "Given a singly linked list L: L0→L1→…→Ln-1→Ln, reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…",
        "examples": [{"input": "head = [1,2,3,4]", "output": "[1,4,2,3]"}, {"input": "head = [1,2,3,4,5]", "output": "[1,5,2,4,3]"}],
        "constraints": ["1 <= n <= 5*10^4", "-1000 <= Node.val <= 1000"],
        "visible_test_cases": [{"input": "4\n1 2 3 4", "expected": "1 4 2 3"}, {"input": "5\n1 2 3 4 5", "expected": "1 5 2 4 3"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "2\n1 2", "expected": "1 2"}, {"input": "3\n1 2 3", "expected": "1 3 2"}],
        "solution": {"approach": "Find middle, reverse second half, merge alternately.", "code": "def reorderList(head):\n    if not head: return\n    slow, fast = head, head\n    while fast.next and fast.next.next:\n        slow = slow.next\n        fast = fast.next.next\n    prev, curr = None, slow.next\n    slow.next = None\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    first, second = head, prev\n    while second:\n        tmp1, tmp2 = first.next, second.next\n        first.next = second\n        second.next = tmp1\n        first = tmp1\n        second = tmp2", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Find the middle using slow/fast pointers.", "Reverse the second half.", "Merge the two halves alternately."],
        "topics": ["Linked List"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-18", "topic": "Linked Lists", "topic_order": 2, "problem_order": 18,
        "question_title": "Sort a Linked List",
        "statement": "Given the head of a linked list, return the list after sorting it in ascending order using merge sort.",
        "examples": [{"input": "head = [4,2,1,3]", "output": "[1,2,3,4]"}, {"input": "head = [-1,5,3,4,0]", "output": "[-1,0,3,4,5]"}],
        "constraints": ["The number of nodes is in [0, 5*10^4]", "-10^5 <= Node.val <= 10^5"],
        "visible_test_cases": [{"input": "4\n4 2 1 3", "expected": "1 2 3 4"}, {"input": "5\n-1 5 3 4 0", "expected": "-1 0 3 4 5"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "0", "expected": ""}, {"input": "2\n2 1", "expected": "1 2"}],
        "solution": {"approach": "Merge sort: find middle, recursively sort halves, merge.", "code": "def sortList(head):\n    if not head or not head.next: return head\n    slow, fast = head, head.next\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    mid = slow.next\n    slow.next = None\n    left = sortList(head)\n    right = sortList(mid)\n    dummy = ListNode(0)\n    curr = dummy\n    while left and right:\n        if left.val <= right.val:\n            curr.next = left; left = left.next\n        else:\n            curr.next = right; right = right.next\n        curr = curr.next\n    curr.next = left or right\n    return dummy.next", "time_complexity": "O(n log n)", "space_complexity": "O(log n)"},
        "hints": ["Use merge sort for linked lists.", "Find the middle using slow/fast pointers.", "Recursively sort each half and merge."],
        "topics": ["Linked List", "Sorting"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-19", "topic": "Linked Lists", "topic_order": 2, "problem_order": 19,
        "question_title": "Flatten a Multilevel Doubly Linked List",
        "statement": "Given a doubly linked list where each node has a next pointer and a child pointer. Flatten the list so that all nodes appear in a single-level doubly linked list.",
        "examples": [{"input": "head = [1,2,3,4,5,6,null,null,null,7,8,null,9,10]", "output": "[1,2,3,7,8,9,10,4,5,6]"}],
        "constraints": ["Number of nodes <= 1000", "-10^6 <= Node.val <= 10^6"],
        "visible_test_cases": [{"input": "flatten\n1 2 3\n| 7 8\n| 9 10\n4 5 6", "expected": "1 2 3 7 8 9 10 4 5 6"}, {"input": "1\n2\n3", "expected": "1 2 3"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "1\n| 2", "expected": "1 2"}, {"input": "1\n| 2\n| 3", "expected": "1 2 3"}],
        "solution": {"approach": "DFS: when finding a child, push next onto stack, flatten child.", "code": "def flatten(head):\n    if not head: return None\n    curr = head\n    while curr:\n        if curr.child:\n            child_head = flatten(curr.child)\n            nxt = curr.next\n            curr.next = child_head\n            child_head.prev = curr\n            curr.child = None\n            temp = child_head\n            while temp.next: temp = temp.next\n            temp.next = nxt\n            if nxt: nxt.prev = temp\n        curr = curr.next\n    return head", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["When you find a child node, flatten it recursively.", "Insert the flattened child between current and next.", "Don't forget to clear the child pointer."],
        "topics": ["Linked List", "Stack"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "LL-20", "topic": "Linked Lists", "topic_order": 2, "problem_order": 20,
        "question_title": "Reverse a Linked List II",
        "statement": "Reverse a linked list from position left to right (1-indexed). Do it in one pass.",
        "examples": [{"input": "head = [1,2,3,4,5], left = 2, right = 4", "output": "[1,4,3,2,5]"}, {"input": "head = [5], left = 1, right = 1", "output": "[5]"}],
        "constraints": ["1 <= n <= 500", "-5000 <= Node.val <= 5000", "1 <= left <= right <= n"],
        "visible_test_cases": [{"input": "5 2 4\n1 2 3 4 5", "expected": "1 4 3 2 5"}, {"input": "1 1 1\n5", "expected": "5"}],
        "hidden_test_cases": [{"input": "3 1 3\n1 2 3", "expected": "3 2 1"}, {"input": "3 2 3\n1 2 3", "expected": "1 3 2"}, {"input": "5 2 5\n1 2 3 4 5", "expected": "1 5 4 3 2"}],
        "solution": {"approach": "Find position left-1, reverse from left to right.", "code": "def reverseBetween(head, left, right):\n    if left == right: return head\n    dummy = ListNode(0, head)\n    prev = dummy\n    for _ in range(left - 1): prev = prev.next\n    curr = prev.next\n    for _ in range(right - left):\n        nxt = curr.next\n        curr.next = nxt.next\n        nxt.next = prev.next\n        prev.next = nxt\n    return dummy.next", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Use a dummy node to handle edge cases.", "Find the node before position left.", "Repeatedly move the next node to right after prev."],
        "topics": ["Linked List"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # TOPIC 3: STACKS & QUEUES — 20 problems
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "SQ-01", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 1,
        "question_title": "Valid Parentheses",
        "statement": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "examples": [{"input": "s = \"()\"", "output": "true"}, {"input": "s = \"()[]{}\"", "output": "true"}, {"input": "s = \"(]\"", "output": "false"}],
        "constraints": ["1 <= s.length <= 10^4", "s consists of parentheses only"],
        "visible_test_cases": [{"input": "()", "expected": "true"}, {"input": "()[]{}", "expected": "true"}],
        "hidden_test_cases": [{"input": "(]", "expected": "false"}, {"input": "([)]", "expected": "false"}, {"input": "{[]}", "expected": "true"}],
        "solution": {"approach": "Use a stack. Push opening brackets, pop on matching closing.", "code": "def isValid(s):\n    stack = []\n    mapping = {')':'(', '}':'{', ']':'['}\n    for char in s:\n        if char in mapping:\n            if not stack or stack[-1] != mapping[char]:\n                return False\n            stack.pop()\n        else:\n            stack.append(char)\n    return not stack", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Push opening brackets onto the stack.", "When you see a closing bracket, check if it matches the top.", "The stack should be empty at the end."],
        "topics": ["Stack", "String"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-02", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 2,
        "question_title": "Next Greater Element",
        "statement": "Given an array, for each element find the next greater element to its right. If none exists, use -1.",
        "examples": [{"input": "nums = [4,5,2,25]", "output": "[5,25,25,-1]"}, {"input": "nums = [13,7,6,12]", "output": "[12,12,-1,-1]"}],
        "constraints": ["1 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
        "visible_test_cases": [{"input": "4\n4 5 2 25", "expected": "5 25 25 -1"}, {"input": "4\n13 7 6 12", "expected": "12 12 -1 -1"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "-1"}, {"input": "3\n1 2 3", "expected": "2 3 -1"}, {"input": "3\n3 2 1", "expected": "-1 -1 -1"}],
        "solution": {"approach": "Use a monotonic stack. Traverse from right to left.", "code": "def nextGreaterElements(nums):\n    n = len(nums)\n    result = [-1] * n\n    stack = []\n    for i in range(n - 1, -1, -1):\n        while stack and stack[-1] <= nums[i]:\n            stack.pop()\n        if stack:\n            result[i] = stack[-1]\n        stack.append(nums[i])\n    return result", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use a stack to maintain elements in decreasing order.", "Traverse from right to left.", "Pop elements smaller than current from stack."],
        "topics": ["Stack", "Array"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-03", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 3,
        "question_title": "Min Stack",
        "statement": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.",
        "examples": [{"input": "MinStack push(-2), push(0), push(-3), getMin, pop, top, getMin", "output": "-3, 0, -2"}, {"input": "MinStack push(1), push(2), top, getMin, pop, getMin", "output": "2, 1, 1"}],
        "constraints": ["Methods pop, top and getMin will be called on non-empty stacks", "-2^31 <= val <= 2^31 - 1"],
        "visible_test_cases": [{"input": "push -2\npush 0\npush -3\ngetMin\npop\ntop\ngetMin", "expected": "-3\n0\n-2"}, {"input": "push 1\npush 2\ntop\ngetMin\npop\ngetMin", "expected": "2\n1\n1"}],
        "hidden_test_cases": [{"input": "push 0\npush 1\npush 0\ngetMin\npop\ngetMin", "expected": "0\n0"}, {"input": "push -1\ngetMin\ntop", "expected": "-1\n-1"}, {"input": "push 5\npush 1\npush 2\ngetMin", "expected": "1"}],
        "solution": {"approach": "Use two stacks: one for values, one for minimums.", "code": "class MinStack:\n    def __init__(self):\n        self.stack = []\n        self.min_stack = []\n    def push(self, val):\n        self.stack.append(val)\n        if not self.min_stack or val <= self.min_stack[-1]:\n            self.min_stack.append(val)\n    def pop(self):\n        val = self.stack.pop()\n        if val == self.min_stack[-1]:\n            self.min_stack.pop()\n    def top(self):\n        return self.stack[-1]\n    def getMin(self):\n        return self.min_stack[-1]", "time_complexity": "O(1)", "space_complexity": "O(n)"},
        "hints": ["Maintain a separate stack for minimum values.", "Push to min_stack when value <= current min.", "Pop from min_stack when popping the current min."],
        "topics": ["Stack", "Design"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-04", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 4,
        "question_title": "Largest Rectangle in Histogram",
        "statement": "Given n non-negative integers representing the histogram's bar width, find the area of the largest rectangle in the histogram.",
        "examples": [{"input": "heights = [2,1,5,6,2,3]", "output": "10"}, {"input": "heights = [2,4]", "output": "4"}],
        "constraints": ["1 <= heights.length <= 10^5", "0 <= heights[i] <= 10^4"],
        "visible_test_cases": [{"input": "6\n2 1 5 6 2 3", "expected": "10"}, {"input": "2\n2 4", "expected": "4"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "5\n2 1 2 1 2", "expected": "5"}, {"input": "4\n1 1 1 1", "expected": "4"}],
        "solution": {"approach": "Use a stack to find next smaller element on both sides.", "code": "def largestRectangleArea(heights):\n    stack = [-1]\n    max_area = 0\n    for i in range(len(heights)):\n        while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:\n            height = heights[stack.pop()]\n            width = i - stack[-1] - 1\n            max_area = max(max_area, height * width)\n        stack.append(i)\n    while stack[-1] != -1:\n        height = heights[stack.pop()]\n        width = len(heights) - stack[-1] - 1\n        max_area = max(max_area, height * width)\n    return max_area", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["For each bar, find the first smaller bar on left and right.", "Use a monotonic stack to do this efficiently.", "Area = height * (right_smaller - left_smaller - 1)."],
        "topics": ["Stack", "Array"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-05", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 5,
        "question_title": "Sliding Window Maximum",
        "statement": "Given an array nums and a sliding window of size k moving from left to right, return the max in each window position.",
        "examples": [{"input": "nums = [1,3,-1,-3,5,3,6,7], k = 3", "output": "[3,3,5,5,6,7]"}, {"input": "nums = [1], k = 1", "output": "[1]"}],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "1 <= k <= nums.length"],
        "visible_test_cases": [{"input": "8 3\n1 3 -1 -3 5 3 6 7", "expected": "3 3 5 5 6 7"}, {"input": "1 1\n1", "expected": "1"}],
        "hidden_test_cases": [{"input": "5 2\n1 2 3 4 5", "expected": "2 3 4 5"}, {"input": "3 2\n3 1 3", "expected": "3 3"}, {"input": "3 3\n1 2 3", "expected": "3"}],
        "solution": {"approach": "Use a monotonic deque to track maximums.", "code": "from collections import deque\ndef maxSlidingWindow(nums, k):\n    dq = deque()\n    result = []\n    for i in range(len(nums)):\n        while dq and dq[0] < i - k + 1:\n            dq.popleft()\n        while dq and nums[dq[-1]] < nums[i]:\n            dq.pop()\n        dq.append(i)\n        if i >= k - 1:\n            result.append(nums[dq[0]])\n    return result", "time_complexity": "O(n)", "space_complexity": "O(k)"},
        "hints": ["Use a deque (double-ended queue).", "Remove indices outside the current window from the front.", "Remove indices with smaller values from the back."],
        "topics": ["Stack", "Queue", "Sliding Window"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-06", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 6,
        "question_title": "Rotten Oranges",
        "statement": "Given a grid where 0 = empty, 1 = fresh orange, 2 = rotten orange. Every minute, any fresh orange adjacent (4-directionally) to a rotten one becomes rotten. Return the minimum number of minutes until no fresh orange remains.",
        "examples": [{"input": "grid = [[2,1,1],[1,1,0],[0,1,1]]", "output": "4"}, {"input": "grid = [[2,1,1],[0,1,1],[1,0,1]]", "output": "-1"}],
        "constraints": ["m == grid.length", "n == grid[i].length", "1 <= m, n <= 10"],
        "visible_test_cases": [{"input": "3 3\n2 1 1\n1 1 0\n0 1 1", "expected": "4"}, {"input": "3 3\n2 1 1\n0 1 1\n1 0 1", "expected": "-1"}],
        "hidden_test_cases": [{"input": "1 1\n2", "expected": "0"}, {"input": "1 1\n1", "expected": "-1"}, {"input": "2 2\n2 1\n1 1", "expected": "1"}],
        "solution": {"approach": "BFS from all rotten oranges simultaneously.", "code": "from collections import deque\ndef orangesRotting(grid):\n    q = deque()\n    fresh = 0\n    for i in range(len(grid)):\n        for j in range(len(grid[0])):\n            if grid[i][j] == 2: q.append((i, j))\n            elif grid[i][j] == 1: fresh += 1\n    if fresh == 0: return 0\n    minutes = 0\n    while q:\n        for _ in range(len(q)):\n            x, y = q.popleft()\n            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:\n                nx, ny = x+dx, y+dy\n                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:\n                    grid[nx][ny] = 2\n                    fresh -= 1\n                    q.append((nx, ny))\n        minutes += 1\n    return minutes - 1 if fresh == 0 else -1", "time_complexity": "O(m*n)", "space_complexity": "O(m*n)"},
        "hints": ["Start BFS from all rotten oranges at once.", "Count fresh oranges to know when all are rotten.", "Each BFS level represents one minute."],
        "topics": ["BFS", "Matrix"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-07", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 7,
        "question_title": "Next Greater Element II",
        "statement": "Given a circular integer array nums, return the next greater element for each element. The next greater is the first element that is greater, traversing circularly.",
        "examples": [{"input": "nums = [1,2,1]", "output": "[2,-1,2]"}, {"input": "nums = [1,2,3,4,3]", "output": "[2,3,4,-1,4]"}],
        "constraints": ["1 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
        "visible_test_cases": [{"input": "3\n1 2 1", "expected": "2 -1 2"}, {"input": "5\n1 2 3 4 3", "expected": "2 3 4 -1 4"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "-1"}, {"input": "2\n1 2", "expected": "2 -1"}, {"input": "3\n3 1 2", "expected": "-1 2 3"}],
        "solution": {"approach": "Use monotonic stack. Iterate twice through the array (circular).", "code": "def nextGreaterElements(nums):\n    n = len(nums)\n    result = [-1] * n\n    stack = []\n    for i in range(2 * n):\n        while stack and nums[stack[-1]] < nums[i % n]:\n            result[stack.pop()] = nums[i % n]\n        if i < n:\n            stack.append(i)\n    return result", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Traverse the array twice to handle circular nature.", "Use indices in the stack, not values.", "Only push indices from the first pass."],
        "topics": ["Stack", "Array"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-08", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 8,
        "question_title": "Daily Temperatures",
        "statement": "Given an array of integers temperatures, return an array answer where answer[i] is the number of days you have to wait after the ith day to get a warmer temperature.",
        "examples": [{"input": "temperatures = [73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]"}, {"input": "temperatures = [30,40,50,60]", "output": "[1,1,1,0]"}],
        "constraints": ["1 <= temperatures.length <= 10^5", "30 <= temperatures[i] <= 100"],
        "visible_test_cases": [{"input": "8\n73 74 75 71 69 72 76 73", "expected": "1 1 4 2 1 1 0 0"}, {"input": "4\n30 40 50 60", "expected": "1 1 1 0"}],
        "hidden_test_cases": [{"input": "3\n30 30 30", "expected": "0 0 0"}, {"input": "2\n30 40", "expected": "1 0"}, {"input": "5\n55 38 53 81 61 92 57 89", "expected": "4 1 1 2 1 0 0 0"}],
        "solution": {"approach": "Monotonic stack from right to left.", "code": "def dailyTemperatures(temperatures):\n    n = len(temperatures)\n    result = [0] * n\n    stack = []\n    for i in range(n - 1, -1, -1):\n        while stack and temperatures[stack[-1]] <= temperatures[i]:\n            stack.pop()\n        if stack:\n            result[i] = stack[-1] - i\n        stack.append(i)\n    return result", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use a stack to track indices of unresolved temperatures.", "Traverse from right to left.", "Pop elements from stack that are <= current temperature."],
        "topics": ["Stack", "Array"], "companies": ["Amazon", "Google", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-09", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 9,
        "question_title": "Decode String",
        "statement": "Given an encoded string, return its decoded string. The encoding rule is k[encoded_string], where the encoded_string is repeated k times.",
        "examples": [{"input": "s = \"3[a2[c]]\"", "output": "accaccacc"}, {"input": "s = \"2[abc]3[cd]ef\"", "output": "abcabccdcdcdef"}],
        "constraints": ["1 <= s.length <= 30", "s consists of lowercase English letters, digits, and '[]'.", "All digits are positive integers."],
        "visible_test_cases": [{"input": "3[a2[c]]", "expected": "accaccacc"}, {"input": "2[abc]3[cd]ef", "expected": "abcabccdcdcdef"}],
        "hidden_test_cases": [{"input": "abc", "expected": "abc"}, {"input": "3[a]", "expected": "aaa"}, {"input": "2[ab3[c]]", "expected": "abcccabccc"}],
        "solution": {"approach": "Use two stacks: one for counts, one for strings.", "code": "def decodeString(s):\n    stack = []\n    curr_str = ''\n    curr_num = 0\n    for char in s:\n        if char.isdigit():\n            curr_num = curr_num * 10 + int(char)\n        elif char == '[':\n            stack.append((curr_str, curr_num))\n            curr_str, curr_num = '', 0\n        elif char == ']':\n            prev_str, num = stack.pop()\n            curr_str = prev_str + curr_str * num\n        else:\n            curr_str += char\n    return curr_str", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use a stack to handle nested brackets.", "When you see '[', push current string and number.", "When you see ']', pop and repeat the string."],
        "topics": ["Stack", "String"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-10", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 10,
        "question_title": "Asteroid Collision",
        "statement": "Given an array asteroids of integers representing asteroids in a row. For each asteroid, the absolute value is its size and the sign is its direction (positive = right, negative = left). Return the state of all asteroids after all collisions.",
        "examples": [{"input": "asteroids = [5,10,-5]", "output": "[5,10]"}, {"input": "asteroids = [8,-8]", "output": "[]"}],
        "constraints": ["2 <= asteroids.length <= 10^4", "-1000 <= asteroids[i] <= 1000", "asteroids[i] != 0"],
        "visible_test_cases": [{"input": "3\n5 10 -5", "expected": "5 10"}, {"input": "2\n8 -8", "expected": ""}],
        "hidden_test_cases": [{"input": "2\n10 2", "expected": "10 2"}, {"input": "3\n-2 -1 1 2", "expected": "-2 -1 1 2"}, {"input": "3\n1 -2 -2", "expected": "-2 -2"}],
        "solution": {"approach": "Use a stack. Push right-moving asteroids, handle collisions.", "code": "def asteroidCollision(asteroids):\n    stack = []\n    for a in asteroids:\n        while stack and a < 0 and stack[-1] > 0:\n            if stack[-1] < -a:\n                stack.pop()\n            elif stack[-1] == -a:\n                stack.pop()\n                break\n            else:\n                break\n        else:\n            stack.append(a)\n    return stack", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use a stack to track surviving asteroids.", "Only right-moving (positive) and left-moving (negative) can collide.", "When they collide, the larger one survives."],
        "topics": ["Stack", "Array"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-11", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 11,
        "question_title": "Infix to Postfix",
        "statement": "Given an infix expression, convert it to postfix (Reverse Polish Notation).",
        "examples": [{"input": "infix = \"a+b*(c^d-e)^(f+g*h)-i\"", "output": "abcd^e-fgh*+^*+i-"}, {"input": "infix = \"A+B\"", "output": "AB+"}],
        "constraints": ["1 <= expression.length <= 10^3", "Expression contains operators +, -, *, /, ^, (, )"],
        "visible_test_cases": [{"input": "a+b*(c^d-e)^(f+g*h)-i", "expected": "abcd^e-fgh*+^*+i-"}, {"input": "A+B", "expected": "AB+"}],
        "hidden_test_cases": [{"input": "(a+b)", "expected": "ab+"}, {"input": "a+b*c", "expected": "abc*+"}, {"input": "a^b^c", "expected": "abc^^"}],
        "solution": {"approach": "Use a stack. Push operators based on precedence.", "code": "def infixToPostfix(s):\n    precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}\n    stack = []\n    output = ''\n    for char in s:\n        if char.isalnum():\n            output += char\n        elif char == '(':\n            stack.append(char)\n        elif char == ')':\n            while stack and stack[-1] != '(':\n                output += stack.pop()\n            stack.pop()\n        else:\n            while stack and stack[-1] != '(' and stack[-1] in precedence and precedence[stack[-1]] >= precedence[char]:\n                output += stack.pop()\n            stack.append(char)\n    while stack: output += stack.pop()\n    return output", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Operands go directly to output.", "Push '(' to stack, pop until '(' on ')'.", "Pop operators with >= precedence before pushing."],
        "topics": ["Stack", "String"], "companies": ["Amazon", "TCS", "Infosys"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-12", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 12,
        "question_title": "Implement Stack using Arrays",
        "statement": "Implement a stack using arrays. Support push, pop, top, and isEmpty operations.",
        "examples": [{"input": "push(1), push(2), top, pop, isEmpty", "output": "2, 2, false"}],
        "constraints": ["1 <= operations <= 100", "-100 <= val <= 100"],
        "visible_test_cases": [{"input": "push 1\npush 2\ntop\npop\nisEmpty", "expected": "2\n2\nfalse"}, {"input": "push 5\npop", "expected": "5"}],
        "hidden_test_cases": [{"input": "isEmpty", "expected": "true"}, {"input": "push 1\nisEmpty", "expected": "false"}, {"input": "push 1\npush 2\npush 3\npop\npop", "expected": "3\n2"}],
        "solution": {"approach": "Use a list with append and pop from end.", "code": "class MyStack:\n    def __init__(self):\n        self.arr = []\n    def push(self, x):\n        self.arr.append(x)\n    def pop(self):\n        return self.arr.pop()\n    def top(self):\n        return self.arr[-1]\n    def isEmpty(self):\n        return len(self.arr) == 0", "time_complexity": "O(1)", "space_complexity": "O(n)"},
        "hints": ["Use Python's list append and pop.", "Both operations are O(1) at the end of the list.", "Track the top index."],
        "topics": ["Stack", "Design"], "companies": ["TCS", "Infosys", "Wipro"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-13", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 13,
        "question_title": "Implement Queue using Arrays",
        "statement": "Implement a FIFO queue using arrays. Support push, pop, peek, and isEmpty operations.",
        "examples": [{"input": "push(1), push(2), peek, pop, isEmpty", "output": "1, 1, false"}],
        "constraints": ["1 <= operations <= 100", "-100 <= val <= 100"],
        "visible_test_cases": [{"input": "push 1\npush 2\npeek\npop\nisEmpty", "expected": "1\n1\nfalse"}, {"input": "push 1\npop\nisEmpty", "expected": "1\ntrue"}],
        "hidden_test_cases": [{"input": "isEmpty", "expected": "true"}, {"input": "push 1\npush 2\npop\npop", "expected": "1\n2"}, {"input": "push 3\npeek", "expected": "3"}],
        "solution": {"approach": "Use a list with deque-like behavior or pointer-based approach.", "code": "class MyQueue:\n    def __init__(self):\n        self.arr = []\n    def push(self, x):\n        self.arr.append(x)\n    def pop(self):\n        return self.arr.pop(0)\n    def peek(self):\n        return self.arr[0]\n    def isEmpty(self):\n        return len(self.arr) == 0", "time_complexity": "O(1) push, O(n) pop", "space_complexity": "O(n)"},
        "hints": ["Use a list and pop from the front.", "Alternatively, use two stacks.", "Consider using collections.deque for O(1) operations."],
        "topics": ["Queue", "Design"], "companies": ["TCS", "Infosys", "Wipro"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-14", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 14,
        "question_title": "Online Stock Span",
        "statement": "Design an algorithm that collects daily price quotes and returns the span of stock's price for the current day. The span is the maximum number of consecutive days where the price was less than or equal to today's price.",
        "examples": [{"input": "StockSpanner.next(100), next(80), next(60), next(70), next(60), next(75), next(85)", "output": "[1,1,1,2,1,4,6]"}],
        "constraints": ["1 <= price <= 10^5", "At most 10^4 calls to next"],
        "visible_test_cases": [{"input": "100\n80\n60\n70\n60\n75\n85", "expected": "1\n1\n1\n2\n1\n4\n6"}, {"input": "50\n60\n70", "expected": "1\n2\n3"}],
        "hidden_test_cases": [{"input": "10\n10\n10", "expected": "1\n2\n3"}, {"input": "5\n4\n3\n2\n1", "expected": "1\n1\n1\n1\n1"}, {"input": "1\n2\n3\n4\n5", "expected": "1\n2\n3\n4\n5"}],
        "solution": {"approach": "Use a stack of (price, span) pairs.", "code": "class StockSpanner:\n    def __init__(self):\n        self.stack = []\n    def next(self, price):\n        span = 1\n        while self.stack and self.stack[-1][0] <= price:\n            span += self.stack.pop()[1]\n        self.stack.append((price, span))\n        return span", "time_complexity": "O(n) total", "space_complexity": "O(n)"},
        "hints": ["Use a stack to track prices and their spans.", "When a new price comes, merge with previous smaller spans.", "The total operations are amortized O(n)."],
        "topics": ["Stack", "Design"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-15", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 15,
        "question_title": "Simplify Path",
        "statement": "Given a string path representing an absolute path for a Unix-style file system, simplify it to its canonical path.",
        "examples": [{"input": "path = \"/home/\"", "output": "/home"}, {"input": "path = \"/home//foo/\"", "output": "/home/foo"}, {"input": "path = \"/home/user/Documents/../Pictures\"", "output": "/home/user/Pictures"}],
        "constraints": ["1 <= path.length <= 3000", "path consists of English letters, digits, period '.', slash '/' or '_'."],
        "visible_test_cases": [{"input": "/home/", "expected": "/home"}, {"input": "/a/./b/../../c/", "expected": "/c"}],
        "hidden_test_cases": [{"input": "/../", "expected": "/"}, {"input": "/home//foo/", "expected": "/home/foo"}, {"input": "/a/./b/../../c/", "expected": "/c"}],
        "solution": {"approach": "Use a stack. Split by '/' and process each component.", "code": "def simplifyPath(path):\n    stack = []\n    for part in path.split('/'):\n        if part == '..':\n            if stack: stack.pop()\n        elif part and part != '.':\n            stack.append(part)\n    return '/' + '/'.join(stack)", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Split the path by '/'.", "Use a stack to track directories.", "'..' pops the last directory, '.' is ignored."],
        "topics": ["Stack", "String"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SQ-16", "topic": "Stacks & Queues", "topic_order": 3, "problem_order": 16,
        "question_title": "Basic Calculator",
        "statement": "Implement a basic calculator to evaluate a simple expression string. The expression string may contain open and closing parentheses, plus and minus signs, and non-negative integers.",
        "examples": [{"input": "s = \"1 + 1\"", "output": "2"}, {"input": "s = \" 2-1 + 2 \"", "output": "3"}, {"input": "s = \"(1+(4+5+2)-3)+(6+8)\"", "output": "23"}],
        "constraints": ["1 <= s.length <= 3 * 10^5", "s consists of digits, '+', '-', '(', ')', and ' '."],
        "visible_test_cases": [{"input": "1 + 1", "expected": "2"}, {"input": "2-1 + 2", "expected": "3"}],
        "hidden_test_cases": [{"input": "(1+(4+5+2)-3)+(6+8)", "expected": "23"}, {"input": "1", "expected": "1"}, {"input": "(1)", "expected": "1"}],
        "solution": {"approach": "Use a stack. Push results and signs when seeing '('.", "code": "def calculate(s):\n    stack = []\n    num = 0\n    sign = 1\n    result = 0\n    for char in s:\n        if char.isdigit():\n            num = num * 10 + int(char)\n        elif char in '+-':\n            result += sign * num\n            num = 0\n            sign = 1 if char == '+' else -1\n        elif char == '(':\n            stack.append(result)\n            stack.append(sign)\n            result, sign = 0, 1\n        elif char == ')':\n            result += sign * num\n            num = 0\n            result *= stack.pop()\n            result += stack.pop()\n    return result + sign * num", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use a stack to save the result and sign before '('.", "When you see ')', pop the sign and previous result.", "Handle multi-digit numbers carefully."],
        "topics": ["Stack", "Math"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # TOPIC 4: BINARY TREES — 25 problems
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "BT-01", "topic": "Binary Trees", "topic_order": 4, "problem_order": 1,
        "question_title": "Inorder Traversal of Binary Tree",
        "statement": "Given the root of a binary tree, return the inorder traversal of its nodes' values (Left, Root, Right).",
        "examples": [{"input": "root = [1,null,2,3]", "output": "[1,3,2]"}, {"input": "root = []", "output": "[]"}],
        "constraints": ["The number of nodes is in [0, 100]", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "1 null 2 3", "expected": "1 3 2"}, {"input": "empty", "expected": ""}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "1 2 3", "expected": "2 1 3"}, {"input": "5 3 6 2 4 null null 1", "expected": "1 2 3 4 5 6"}],
        "solution": {"approach": "Recursive or iterative using a stack.", "code": "def inorderTraversal(root):\n    result = []\n    stack = []\n    curr = root\n    while curr or stack:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        result.append(curr.val)\n        curr = curr.right\n    return result", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["Inorder = Left, Root, Right.", "Use a stack for iterative approach.", "Go as far left as possible, then process node, then go right."],
        "topics": ["Binary Tree", "Stack"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-02", "topic": "Binary Trees", "topic_order": 4, "problem_order": 2,
        "question_title": "Preorder Traversal of Binary Tree",
        "statement": "Given the root of a binary tree, return the preorder traversal of its nodes' values (Root, Left, Right).",
        "examples": [{"input": "root = [1,null,2,3]", "output": "[1,2,3]"}, {"input": "root = [1,2,3,4,5,null,null]", "output": "[1,2,4,5,3]"}],
        "constraints": ["0 <= number of nodes <= 100", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "1 null 2 3", "expected": "1 2 3"}, {"input": "1 2 3 4 5", "expected": "1 2 4 5 3"}],
        "hidden_test_cases": [{"input": "empty", "expected": ""}, {"input": "1", "expected": "1"}, {"input": "1 2 3", "expected": "1 2 3"}],
        "solution": {"approach": "Recursive or iterative using a stack.", "code": "def preorderTraversal(root):\n    if not root: return []\n    result = []\n    stack = [root]\n    while stack:\n        node = stack.pop()\n        result.append(node.val)\n        if node.right: stack.append(node.right)\n        if node.left: stack.append(node.left)\n    return result", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["Preorder = Root, Left, Right.", "Process node first, then push right then left to stack.", "Stack is LIFO so push right first."],
        "topics": ["Binary Tree", "Stack"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-03", "topic": "Binary Trees", "topic_order": 4, "problem_order": 3,
        "question_title": "Level Order Traversal of Binary Tree",
        "statement": "Given the root of a binary tree, return the level order traversal (breadth-first) of its nodes' values.",
        "examples": [{"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"}, {"input": "root = [1]", "output": "[[1]]"}],
        "constraints": ["The number of nodes is in [0, 2000]", "-1000 <= Node.val <= 1000"],
        "visible_test_cases": [{"input": "3 9 20 null null 15 7", "expected": "3\n9 20\n15 7"}, {"input": "1", "expected": "1"}],
        "hidden_test_cases": [{"input": "empty", "expected": ""}, {"input": "1 2 3 4 5", "expected": "1\n2 3\n4 5"}, {"input": "1 null 2 null 3", "expected": "1\n2\n3"}],
        "solution": {"approach": "BFS using a queue.", "code": "from collections import deque\ndef levelOrder(root):\n    if not root: return []\n    result = []\n    queue = deque([root])\n    while queue:\n        level = []\n        for _ in range(len(queue)):\n            node = queue.popleft()\n            level.append(node.val)\n            if node.left: queue.append(node.left)\n            if node.right: queue.append(node.right)\n        result.append(level)\n    return result", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use a queue for BFS.", "Process all nodes at current level before moving to next.", "Track level size before processing."],
        "topics": ["Binary Tree", "BFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-04", "topic": "Binary Trees", "topic_order": 4, "problem_order": 4,
        "question_title": "Maximum Depth of Binary Tree",
        "statement": "Given the root of a binary tree, return its maximum depth (number of nodes along the longest path from root to farthest leaf).",
        "examples": [{"input": "root = [3,9,20,null,null,15,7]", "output": "3"}, {"input": "root = [1,null,2]", "output": "2"}],
        "constraints": ["The number of nodes is in [0, 10^4]", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "3 9 20 null null 15 7", "expected": "3"}, {"input": "1 null 2", "expected": "2"}],
        "hidden_test_cases": [{"input": "empty", "expected": "0"}, {"input": "1", "expected": "1"}, {"input": "1 2 3 4 5", "expected": "3"}],
        "solution": {"approach": "DFS: return max depth of left and right subtrees + 1.", "code": "def maxDepth(root):\n    if not root: return 0\n    return 1 + max(maxDepth(root.left), maxDepth(root.right))", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["Base case: empty tree has depth 0.", "Recurse on left and right subtrees.", "Return the maximum of both + 1."],
        "topics": ["Binary Tree", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-05", "topic": "Binary Trees", "topic_order": 4, "problem_order": 5,
        "question_title": "Diameter of Binary Tree",
        "statement": "Given the root of a binary tree, return the length of the diameter (longest path between any two nodes).",
        "examples": [{"input": "root = [1,2,3,4,5]", "output": "3"}, {"input": "root = [1,2]", "output": "1"}],
        "constraints": ["1 <= n <= 10^4", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "1 2 3 4 5", "expected": "3"}, {"input": "1 2", "expected": "1"}],
        "hidden_test_cases": [{"input": "1", "expected": "0"}, {"input": "1 2 3", "expected": "2"}, {"input": "1 2 null 3", "expected": "2"}],
        "solution": {"approach": "DFS: at each node, diameter = left_depth + right_depth.", "code": "def diameterOfBinaryTree(root):\n    self.diameter = 0\n    def depth(node):\n        if not node: return 0\n        left = depth(node.left)\n        right = depth(node.right)\n        self.diameter = max(self.diameter, left + right)\n        return 1 + max(left, right)\n    depth(root)\n    return self.diameter", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["The diameter through a node = left_height + right_height.", "Track the global maximum during DFS.", "Return height to parent while updating diameter."],
        "topics": ["Binary Tree", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-06", "topic": "Binary Trees", "topic_order": 4, "problem_order": 6,
        "question_title": "Check if Binary Tree is Balanced",
        "statement": "Given the root of a binary tree, determine if it is height-balanced (left and right subtrees differ by at most 1).",
        "examples": [{"input": "root = [3,9,20,null,null,15,7]", "output": "true"}, {"input": "root = [1,2,2,3,3,null,null,4,4]", "output": "false"}],
        "constraints": ["The number of nodes is in [0, 5000]", "-10000 <= Node.val <= 10000"],
        "visible_test_cases": [{"input": "3 9 20 null null 15 7", "expected": "true"}, {"input": "1 2 2 3 3 null null 4 4", "expected": "false"}],
        "hidden_test_cases": [{"input": "empty", "expected": "true"}, {"input": "1", "expected": "true"}, {"input": "1 2 3 4 5 6 7", "expected": "true"}],
        "solution": {"approach": "DFS: return height, check balance at each node.", "code": "def isBalanced(root):\n    def check(node):\n        if not node: return 0\n        left = check(node.left)\n        if left == -1: return -1\n        right = check(node.right)\n        if right == -1: return -1\n        if abs(left - right) > 1: return -1\n        return 1 + max(left, right)\n    return check(root) != -1", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["Return -1 to indicate unbalanced subtree.", "Check balance at each node during DFS.", "If any subtree is unbalanced, propagate -1 up."],
        "topics": ["Binary Tree", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-07", "topic": "Binary Trees", "topic_order": 4, "problem_order": 7,
        "question_title": "Lowest Common Ancestor of a Binary Tree",
        "statement": "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q.",
        "examples": [{"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p=5, q=1", "output": "3"}, {"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p=5, q=4", "output": "5"}],
        "constraints": ["All node values are unique", "p != q", "p and q exist in the tree"],
        "visible_test_cases": [{"input": "3 5 1 6 2 0 8 null null 7 4\n5 1", "expected": "3"}, {"input": "3 5 1 6 2 0 8 null null 7 4\n5 4", "expected": "5"}],
        "hidden_test_cases": [{"input": "1 2\n1 2", "expected": "1"}, {"input": "2 1\n2 1", "expected": "2"}, {"input": "1 null 2\n1 2", "expected": "1"}],
        "solution": {"approach": "DFS: if current node is p or q, return it. Otherwise recurse on children.", "code": "def lowestCommonAncestor(root, p, q):\n    if not root or root == p or root == q:\n        return root\n    left = lowestCommonAncestor(root.left, p, q)\n    right = lowestCommonAncestor(root.right, p, q)\n    if left and right: return root\n    return left or right", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["If current node is null, p, or q, return it.", "Recurse on left and right subtrees.", "If both return non-null, current is LCA."],
        "topics": ["Binary Tree", "DFS"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-08", "topic": "Binary Trees", "topic_order": 4, "problem_order": 8,
        "question_title": "Same Tree",
        "statement": "Given the roots of two binary trees p and q, check if they are the same tree.",
        "examples": [{"input": "p = [1,2,3], q = [1,2,3]", "output": "true"}, {"input": "p = [1,2], q = [1,null,2]", "output": "false"}],
        "constraints": ["Both trees have [0, 100] nodes", "-10^4 <= Node.val <= 10^4"],
        "visible_test_cases": [{"input": "1 2 3\n1 2 3", "expected": "true"}, {"input": "1 2\n1 null 2", "expected": "false"}],
        "hidden_test_cases": [{"input": "empty\nempty", "expected": "true"}, {"input": "1\n2", "expected": "false"}, {"input": "1 2 1\n1 1 2", "expected": "false"}],
        "solution": {"approach": "Recursive comparison of both trees.", "code": "def isSameTree(p, q):\n    if not p and not q: return True\n    if not p or not q: return False\n    return p.val == q.val and isSameTree(p.left, q.left) and isSameTree(p.right, q.right)", "time_complexity": "O(min(m,n))", "space_complexity": "O(min(m,n))"},
        "hints": ["If both nodes are null, they're the same.", "If one is null and other isn't, they're different.", "Compare values and recurse on both children."],
        "topics": ["Binary Tree", "DFS"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-09", "topic": "Binary Trees", "topic_order": 4, "problem_order": 9,
        "question_title": "Invert Binary Tree",
        "statement": "Given the root of a binary tree, invert the tree (swap left and right children for every node).",
        "examples": [{"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]"}, {"input": "root = [2,1,3]", "output": "[2,3,1]"}],
        "constraints": ["The number of nodes in the tree is in [0, 100]", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "4 2 7 1 3 6 9", "expected": "4 7 2 9 6 3 1"}, {"input": "2 1 3", "expected": "2 3 1"}],
        "hidden_test_cases": [{"input": "empty", "expected": ""}, {"input": "1", "expected": "1"}, {"input": "1 2", "expected": "1 null 2"}],
        "solution": {"approach": "DFS: swap left and right children, recurse.", "code": "def invertTree(root):\n    if not root: return None\n    root.left, root.right = root.right, root.left\n    invertTree(root.left)\n    invertTree(root.right)\n    return root", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["Swap left and right children at each node.", "Recurse on both subtrees.", "Base case: null node returns null."],
        "topics": ["Binary Tree", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-10", "topic": "Binary Trees", "topic_order": 4, "problem_order": 10,
        "question_title": "Validate Binary Search Tree",
        "statement": "Given the root of a binary tree, determine if it is a valid BST.",
        "examples": [{"input": "root = [2,1,3]", "output": "true"}, {"input": "root = [5,1,4,null,null,3,6]", "output": "false"}],
        "constraints": ["The number of nodes is in [1, 10^4]", "-2^31 <= Node.val <= 2^31 - 1"],
        "visible_test_cases": [{"input": "2 1 3", "expected": "true"}, {"input": "5 1 4 null null 3 6", "expected": "false"}],
        "hidden_test_cases": [{"input": "1 1", "expected": "false"}, {"input": "2 1 3 null null null 4", "expected": "true"}, {"input": "5 4 6 null null 3 7", "expected": "false"}],
        "solution": {"approach": "DFS with valid range (min, max) for each node.", "code": "def isValidBST(root):\n    def validate(node, min_val, max_val):\n        if not node: return True\n        if node.val <= min_val or node.val >= max_val:\n            return False\n        return validate(node.left, min_val, node.val) and validate(node.right, node.val, max_val)\n    return validate(root, float('-inf'), float('inf'))", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["Each node must be within a valid range.", "Left subtree values must be < node value.", "Right subtree values must be > node value."],
        "topics": ["Binary Tree", "BST", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-11", "topic": "Binary Trees", "topic_order": 4, "problem_order": 11,
        "question_title": "Kth Smallest Element in BST",
        "statement": "Given the root of a BST and an integer k, return the kth smallest value.",
        "examples": [{"input": "root = [3,1,4,null,2], k = 1", "output": "1"}, {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "output": "3"}],
        "constraints": ["1 <= k <= n <= 10^4", "All values are unique"],
        "visible_test_cases": [{"input": "3 1 4 null 2\n1", "expected": "1"}, {"input": "5 3 6 2 4 null null 1\n3", "expected": "3"}],
        "hidden_test_cases": [{"input": "2 1\n2", "expected": "2"}, {"input": "1 null 2\n1", "expected": "1"}, {"input": "1 null 2\n2", "expected": "2"}],
        "solution": {"approach": "Inorder traversal — kth visit is the answer.", "code": "def kthSmallest(root, k):\n    stack = []\n    curr = root\n    while stack or curr:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        k -= 1\n        if k == 0: return curr.val\n        curr = curr.right", "time_complexity": "O(h + k)", "space_complexity": "O(h)"},
        "hints": ["Inorder traversal of BST gives sorted order.", "Use iterative inorder with a stack.", "Stop when you've visited k nodes."],
        "topics": ["Binary Tree", "BST"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-12", "topic": "Binary Trees", "topic_order": 4, "problem_order": 12,
        "question_title": "Convert Sorted Array to BST",
        "statement": "Given an integer array nums where elements are sorted in ascending order, convert it to a height-balanced BST.",
        "examples": [{"input": "nums = [-10,-3,0,5,9]", "output": "[0,-3,9,-10,null,5]"}, {"input": "nums = [1,3]", "output": "[3,1]"}],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [{"input": "5\n-10 -3 0 5 9", "expected": "0 -3 9 -10 null 5"}, {"input": "2\n1 3", "expected": "3 1"}],
        "hidden_test_cases": [{"input": "1\n0", "expected": "0"}, {"input": "3\n1 2 3", "expected": "2 1 3"}, {"input": "7\n-10 -3 0 5 9 12 15", "expected": "5 -3 12 -10 0 9 15"}],
        "solution": {"approach": "Pick middle element as root, recurse on halves.", "code": "def sortedArrayToBST(nums):\n    if not nums: return None\n    mid = len(nums) // 2\n    root = TreeNode(nums[mid])\n    root.left = sortedArrayToBST(nums[:mid])\n    root.right = sortedArrayToBST(nums[mid+1:])\n    return root", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Middle element is always the root.", "Left half goes to left subtree.", "Right half goes to right subtree."],
        "topics": ["Binary Tree", "BST", "Divide and Conquer"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-13", "topic": "Binary Trees", "topic_order": 4, "problem_order": 13,
        "question_title": "Binary Tree Right Side View",
        "statement": "Given the root of a binary tree, imagine yourself standing on the right side, return the values of the nodes you can see from top to bottom.",
        "examples": [{"input": "root = [1,2,3,null,5,null,4]", "output": "[1,3,4]"}, {"input": "root = [1,null,3]", "output": "[1,3]"}],
        "constraints": ["The number of nodes is in [0, 100]", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "1 2 3 null 5 null 4", "expected": "1 3 4"}, {"input": "1 null 3", "expected": "1 3"}],
        "hidden_test_cases": [{"input": "empty", "expected": ""}, {"input": "1", "expected": "1"}, {"input": "1 2 3 4", "expected": "1 3 4"}],
        "solution": {"approach": "BFS, take last node of each level.", "code": "from collections import deque\ndef rightSideView(root):\n    if not root: return []\n    result = []\n    queue = deque([root])\n    while queue:\n        level_size = len(queue)\n        for i in range(level_size):\n            node = queue.popleft()\n            if i == level_size - 1:\n                result.append(node.val)\n            if node.left: queue.append(node.left)\n            if node.right: queue.append(node.right)\n    return result", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use BFS level-order traversal.", "The rightmost node at each level is visible.", "Take the last node at each level."],
        "topics": ["Binary Tree", "BFS"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-14", "topic": "Binary Trees", "topic_order": 4, "problem_order": 14,
        "question_title": "Binary Tree Maximum Path Sum",
        "statement": "Given the root of a binary tree, find the maximum path sum. A path can start and end at any node.",
        "examples": [{"input": "root = [1,2,3]", "output": "6"}, {"input": "root = [-10,9,20,null,null,15,7]", "output": "42"}],
        "constraints": ["The number of nodes is in [1, 3 * 10^4]", "-1000 <= Node.val <= 1000"],
        "visible_test_cases": [{"input": "1 2 3", "expected": "6"}, {"input": "-10 9 20 null null 15 7", "expected": "42"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "-3", "expected": "-3"}, {"input": "2 -1", "expected": "2"}],
        "solution": {"approach": "DFS: at each node, max path = node + max(0, left) + max(0, right).", "code": "def maxPathSum(root):\n    self.max_sum = float('-inf')\n    def dfs(node):\n        if not node: return 0\n        left = max(0, dfs(node.left))\n        right = max(0, dfs(node.right))\n        self.max_sum = max(self.max_sum, node.val + left + right)\n        return node.val + max(left, right)\n    dfs(root)\n    return self.max_sum", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["At each node, consider path through it (left + node + right).", "Return max single-branch path to parent.", "Ignore negative subtrees by taking max with 0."],
        "topics": ["Binary Tree", "DFS"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-15", "topic": "Binary Trees", "topic_order": 4, "problem_order": 15,
        "question_title": "Construct Binary Tree from Preorder and Inorder",
        "statement": "Given two integer arrays preorder and inorder, construct and return the binary tree.",
        "examples": [{"input": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "output": "[3,9,20,null,null,15,7]"}, {"input": "preorder = [-1], inorder = [-1]", "output": "[-1]"}],
        "constraints": ["1 <= preorder.length <= 3000", "preorder and inorder values are unique"],
        "visible_test_cases": [{"input": "3 9 20 15 7\n9 3 15 20 7", "expected": "3 9 20 null null 15 7"}, {"input": "-1\n-1", "expected": "-1"}],
        "hidden_test_cases": [{"input": "1 2 3\n2 1 3", "expected": "1 2 null null 3"}, {"input": "1 2 4 5 3 6 7\n4 2 5 1 6 3 7", "expected": "1 2 3 4 5 6 7"}, {"input": "4 2 1 3\n1 2 3 4", "expected": "4 2 1 null null null 3"}],
        "solution": {"approach": "First element of preorder is root. Find it in inorder to split left/right.", "code": "def buildTree(preorder, inorder):\n    if not preorder or not inorder: return None\n    root = TreeNode(preorder[0])\n    mid = inorder.index(preorder[0])\n    root.left = buildTree(preorder[1:mid+1], inorder[:mid])\n    root.right = buildTree(preorder[mid+1:], inorder[mid+1:])\n    return root", "time_complexity": "O(n^2)", "space_complexity": "O(n)"},
        "hints": ["First element in preorder is always the root.", "Find the root in inorder to determine left and right subtrees.", "Recurse on the subtrees."],
        "topics": ["Binary Tree", "Array"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-16", "topic": "Binary Trees", "topic_order": 4, "problem_order": 16,
        "question_title": "Serialize and Deserialize Binary Tree",
        "statement": "Design an algorithm to serialize and deserialize a binary tree to/from a string.",
        "examples": [{"input": "root = [1,2,3,null,null,4,5]", "output": "Serialized string, then back to same tree"}, {"input": "root = []", "output": ""}],
        "constraints": ["The number of nodes is in [0, 10^4]", "-1000 <= Node.val <= 1000"],
        "visible_test_cases": [{"input": "1 2 3 null null 4 5", "expected": "1,2,N,N,3,4,N,N,5,N,N"}, {"input": "empty", "expected": "N"}],
        "hidden_test_cases": [{"input": "1", "expected": "1,N,N"}, {"input": "1 2", "expected": "1,2,N,N,N"}, {"input": "1 null 2", "expected": "1,N,2,N,N"}],
        "solution": {"approach": "Preorder traversal with 'N' for null nodes.", "code": "class Codec:\n    def serialize(self, root):\n        if not root: return 'N'\n        return f'{root.val},{self.serialize(root.left)},{self.serialize(root.right)}'\n    def deserialize(self, data):\n        def helper(nodes):\n            val = next(nodes)\n            if val == 'N': return None\n            node = TreeNode(int(val))\n            node.left = helper(nodes)\n            node.right = helper(nodes)\n            return node\n        return helper(iter(data.split(',')))", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use preorder traversal for serialization.", "Mark null nodes with a special character like 'N'.", "Use an iterator for efficient deserialization."],
        "topics": ["Binary Tree", "Design"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-17", "topic": "Binary Trees", "topic_order": 4, "problem_order": 17,
        "question_title": "Flatten Binary Tree to Linked List",
        "statement": "Given the root of a binary tree, flatten the tree to a linked list in-place (preorder).",
        "examples": [{"input": "root = [1,2,5,3,4,null,6]", "output": "[1,null,2,null,3,null,4,null,5,null,6]"}, {"input": "root = [0]", "output": "[0]"}],
        "constraints": ["The number of nodes is in [0, 2000]", "-100 <= Node.val <= 100"],
        "visible_test_cases": [{"input": "1 2 5 3 4 null 6", "expected": "1 null 2 null 3 null 4 null 5 null 6"}, {"input": "0", "expected": "0"}],
        "hidden_test_cases": [{"input": "empty", "expected": ""}, {"input": "1 2", "expected": "1 null 2"}, {"input": "1 null 2", "expected": "1 null 2"}],
        "solution": {"approach": "For each node, move left subtree to right, find rightmost of old right, attach.", "code": "def flatten(root):\n    curr = root\n    while curr:\n        if curr.left:\n            prev = curr.left\n            while prev.right:\n            prev.right = curr.right\n            curr.right = curr.left\n            curr.left = None\n        curr = curr.right", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["For each node, move the entire left subtree to the right.", "Find the rightmost node of the moved subtree.", "Attach original right subtree to that rightmost node."],
        "topics": ["Binary Tree", "Linked List"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-18", "topic": "Binary Trees", "topic_order": 4, "problem_order": 18,
        "question_title": "Populating Next Right Pointers",
        "statement": "Given a binary tree, populate each next pointer to point to its next right node. If there is no next right node, set next to NULL.",
        "examples": [{"input": "root = [1,2,3,4,5,6,7]", "output": "1 -> 2 -> 3, 4 -> 5, 6 -> 7"}, {"input": "root = []", "output": "[]"}],
        "constraints": ["The number of nodes is in [0, 2^12 - 1]", "-1000 <= Node.val <= 1000"],
        "visible_test_cases": [{"input": "1 2 3 4 5 6 7", "expected": "1 2 3 4 5 6 7"}, {"input": "1", "expected": "1"}],
        "hidden_test_cases": [{"input": "empty", "expected": ""}, {"input": "1 2", "expected": "1 2"}, {"input": "1 2 3", "expected": "1 2 3"}],
        "solution": {"approach": "Level-order BFS, connect nodes at each level.", "code": "def connect(root):\n    if not root: return root\n    queue = [root]\n    while queue:\n        next_queue = []\n        for i in range(len(queue)):\n            if i < len(queue) - 1:\n                queue[i].next = queue[i+1]\n            if queue[i].left: next_queue.append(queue[i].left)\n            if queue[i].right: next_queue.append(queue[i].right)\n        queue = next_queue\n    return root", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Process level by level using BFS.", "Connect each node to the next node in the same level.", "Use a queue to track nodes at each level."],
        "topics": ["Binary Tree", "BFS"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-19", "topic": "Binary Trees", "topic_order": 4, "problem_order": 19,
        "question_title": "Binary Search Tree Iterator",
        "statement": "Implement the BSTIterator class that represents an iterator over the in-order traversal of a BST.",
        "examples": [{"input": "BSTIterator(root = [7,3,15,null,null,9,20])", "output": "next()=3, next()=7, hasNext()=true, next()=9, next()=15, next()=20"},
        {"input": "BSTIterator(root = [1])", "output": "next()=1, hasNext()=false"}],
        "constraints": ["1 <= n <= 10^5", "0 <= Node.val <= 10^6"],
        "visible_test_cases": [{"input": "7 3 15 null null 9 20\nnext next hasNext next", "expected": "3 7 true 9"}, {"input": "1\nnext hasNext", "expected": "1 false"}],
        "hidden_test_cases": [{"input": "2 1\nnext hasNext next", "expected": "1 true 2"}, {"input": "5 3 7 2 4 6 8\nnext next next", "expected": "2 3 4"}, {"input": "10 5 15 3 7\nnext next next next next", "expected": "3 5 7 10 15"}],
        "solution": {"approach": "Flatten BST into a sorted list using inorder traversal.", "code": "class BSTIterator:\n    def __init__(self, root):\n        self.stack = []\n        self._push_left(root)\n    def _push_left(self, node):\n        while node:\n            self.stack.append(node)\n            node = node.left\n    def next(self):\n        node = self.stack.pop()\n        self._push_left(node.right)\n        return node.val\n    def hasNext(self):\n        return len(self.stack) > 0", "time_complexity": "O(1) amortized", "space_complexity": "O(h)"},
        "hints": ["Use a stack to simulate inorder traversal.", "Push all left nodes onto the stack.", "When popping, push all left nodes of the right child."],
        "topics": ["Binary Tree", "BST", "Stack", "Design"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BT-20", "topic": "Binary Trees", "topic_order": 4, "problem_order": 20,
        "question_title": "Vertical Order Traversal of Binary Tree",
        "statement": "Given the root of a binary tree, return the vertical order traversal. Nodes are sorted by their value when at the same position.",
        "examples": [{"input": "root = [3,9,20,null,null,15,7]", "output": "[[9],[3,15],[20],[7]]"}, {"input": "root = [1,2,3,4,5,6,7]", "output": "[[4],[2],[1,5,6],[3],[7]]"}],
        "constraints": ["The number of nodes is in [1, 1000]", "-1000 <= Node.val <= 1000"],
        "visible_test_cases": [{"input": "3 9 20 null null 15 7", "expected": "9\n3 15\n20\n7"}, {"input": "1 2 3 4 5 6 7", "expected": "4\n2\n1 5 6\n3\n7"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "1 2 3", "expected": "2\n1 3"}, {"input": "1 2 null 3", "expected": "3\n1\n2"}],
        "solution": {"approach": "BFS with column tracking. Sort by (col, row, val).", "code": "from collections import defaultdict, deque\ndef verticalTraversal(root):\n    col_map = defaultdict(list)\n    queue = deque([(root, 0, 0)])\n    while queue:\n        node, row, col = queue.popleft()\n        if node:\n            col_map[col].append((row, node.val))\n            queue.append((node.left, row + 1, col - 1))\n            queue.append((node.right, row + 1, col + 1))\n    result = []\n    for col in sorted(col_map.keys()):\n        col_map[col].sort()\n        result.append([val for _, val in col_map[col]])\n    return result", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Use BFS to traverse level by level with column indices.", "Group nodes by column.", "Sort each column by row, then by value."],
        "topics": ["Binary Tree", "BFS", "Sorting"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # TOPIC 5: GRAPHS — 20 problems
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "GR-01", "topic": "Graphs", "topic_order": 5, "problem_order": 1,
        "question_title": "BFS of Graph",
        "statement": "Given an undirected connected graph with V vertices and adjacency list, perform BFS traversal starting from vertex 0.",
        "examples": [{"input": "V=5, edges=[[1,2],[1,0],[2,3],[3,4]]", "output": "[0,1,2,3,4]"}, {"input": "V=3, edges=[[1,2]]", "output": "[0,1,2]"}],
        "constraints": ["1 <= V <= 10^4", "0 <= E <= 10^4"],
        "visible_test_cases": [{"input": "5\n1 2\n1 0\n2 3\n3 4", "expected": "0 1 2 3 4"}, {"input": "3\n1 2", "expected": "0 1 2"}],
        "hidden_test_cases": [{"input": "1", "expected": "0"}, {"input": "2\n0 1", "expected": "0 1"}, {"input": "4\n0 1\n0 2\n1 3\n2 3", "expected": "0 1 2 3"}],
        "solution": {"approach": "Use a queue. Visit node, mark visited, enqueue neighbors.", "code": "from collections import deque\ndef bfs(graph, V):\n    visited = [False] * V\n    result = []\n    queue = deque([0])\n    visited[0] = True\n    while queue:\n        node = queue.popleft()\n        result.append(node)\n        for neighbor in graph[node]:\n            if not visited[neighbor]:\n                visited[neighbor] = True\n                queue.append(neighbor)\n    return result", "time_complexity": "O(V + E)", "space_complexity": "O(V)"},
        "hints": ["Start from vertex 0.", "Use a queue for level-order traversal.", "Mark nodes as visited to avoid revisiting."],
        "topics": ["Graph", "BFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-02", "topic": "Graphs", "topic_order": 5, "problem_order": 2,
        "question_title": "DFS of Graph",
        "statement": "Given an undirected connected graph with V vertices and adjacency list, perform DFS traversal starting from vertex 0.",
        "examples": [{"input": "V=5, edges=[[1,2],[1,0],[2,3],[3,4]]", "output": "[0,1,2,3,4]"}, {"input": "V=3, edges=[[1,2]]", "output": "[0,1,2]"}],
        "constraints": ["1 <= V <= 10^4"],
        "visible_test_cases": [{"input": "5\n1 2\n1 0\n2 3\n3 4", "expected": "0 1 2 3 4"}, {"input": "3\n1 2", "expected": "0 1 2"}],
        "hidden_test_cases": [{"input": "1", "expected": "0"}, {"input": "4\n0 1\n0 2\n1 3\n2 3", "expected": "0 1 3 2"}, {"input": "2\n0 1", "expected": "0 1"}],
        "solution": {"approach": "Recursive or iterative DFS using stack.", "code": "def dfs(graph, V):\n    visited = [False] * V\n    result = []\n    def dfsHelper(node):\n        visited[node] = True\n        result.append(node)\n        for neighbor in graph[node]:\n            if not visited[neighbor]:\n                dfsHelper(neighbor)\n    dfsHelper(0)\n    return result", "time_complexity": "O(V + E)", "space_complexity": "O(V)"},
        "hints": ["Use recursion or an explicit stack.", "Mark nodes as visited before recursing.", "Visit all neighbors before returning."],
        "topics": ["Graph", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-03", "topic": "Graphs", "topic_order": 5, "problem_order": 3,
        "question_title": "Number of Provinces",
        "statement": "Given an n x n adjacency matrix isConnected where isConnected[i][j] = 1 means city i is directly connected to city j, return the number of provinces (connected components).",
        "examples": [{"input": "isConnected = [[1,1,0],[1,1,0],[0,0,1]]", "output": "2"}, {"input": "isConnected = [[1,0,0],[0,1,0],[0,0,1]]", "output": "3"}],
        "constraints": ["1 <= n <= 200", "isConnected[i][j] is 1 or 0"],
        "visible_test_cases": [{"input": "3\n1 1 0\n1 1 0\n0 0 1", "expected": "2"}, {"input": "3\n1 0 0\n0 1 0\n0 0 1", "expected": "3"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "2\n1 0\n0 1", "expected": "2"}, {"input": "2\n1 1\n1 1", "expected": "1"}],
        "solution": {"approach": "DFS/BFS on each unvisited node counts one province.", "code": "def findCircleNum(isConnected):\n    n = len(isConnected)\n    visited = [False] * n\n    provinces = 0\n    def dfs(node):\n        visited[node] = True\n        for j in range(n):\n            if isConnected[node][j] == 1 and not visited[j]:\n                dfs(j)\n    for i in range(n):\n        if not visited[i]:\n            dfs(i)\n            provinces += 1\n    return provinces", "time_complexity": "O(n^2)", "space_complexity": "O(n)"},
        "hints": ["Each connected component is a province.", "Use DFS/BFS to find connected components.", "Count the number of times you start a new DFS."],
        "topics": ["Graph", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-04", "topic": "Graphs", "topic_order": 5, "problem_order": 4,
        "question_title": "Is Graph Bipartite?",
        "statement": "Given an undirected graph, return true if and only if it is bipartite (can be colored with 2 colors).",
        "examples": [{"input": "graph = [[1,2,3],[0,2],[0,1,3],[0,2]]", "output": "false"}, {"input": "graph = [[1,3],[0,2],[1,3],[0,2]]", "output": "true"}],
        "constraints": ["n == graph.length", "1 <= n <= 100", "0 <= graph[i][j] < n"],
        "visible_test_cases": [{"input": "4\n1 2 3\n0 2\n0 1 3\n0 2", "expected": "false"}, {"input": "4\n1 3\n0 2\n1 3\n0 2", "expected": "true"}],
        "hidden_test_cases": [{"input": "1\nempty", "expected": "true"}, {"input": "2\n1\n0", "expected": "true"}, {"input": "3\n1 2\n0 2\n0 1", "expected": "false"}],
        "solution": {"approach": "BFS/DFS with 2-coloring. Try to color with alternating colors.", "code": "def isBipartite(graph):\n    n = len(graph)\n    color = [-1] * n\n    for i in range(n):\n        if color[i] != -1: continue\n        color[i] = 0\n        queue = [i]\n        while queue:\n            node = queue.pop()\n            for neighbor in graph[node]:\n                if color[neighbor] == -1:\n                    color[neighbor] = 1 - color[node]\n                    queue.append(neighbor)\n                elif color[neighbor] == color[node]:\n                    return False\n    return True", "time_complexity": "O(V + E)", "space_complexity": "O(V)"},
        "hints": ["Try to color the graph with 2 colors.", "Adjacent nodes must have different colors.", "If you find a conflict, it's not bipartite."],
        "topics": ["Graph", "BFS", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-05", "topic": "Graphs", "topic_order": 5, "problem_order": 5,
        "question_title": "Detect Cycle in Undirected Graph",
        "statement": "Given an undirected graph with V vertices and adjacency list, detect if there is a cycle.",
        "examples": [{"input": "V=5, edges=[[1,2],[2,3],[3,4],[4,1]]", "output": "true"}, {"input": "V=3, edges=[[1,2]]", "output": "false"}],
        "constraints": ["1 <= V <= 10^4"],
        "visible_test_cases": [{"input": "5\n1 2\n2 3\n3 4\n4 1", "expected": "true"}, {"input": "3\n1 2", "expected": "false"}],
        "hidden_test_cases": [{"input": "1", "expected": "false"}, {"input": "2\n0 1", "expected": "true"}, {"input": "4\n0 1\n1 2\n2 3", "expected": "false"}],
        "solution": {"approach": "DFS: if you find an adjacent visited node that's not the parent, cycle exists.", "code": "def isCycle(V, adj):\n    visited = [False] * V\n    def dfs(node, parent):\n        visited[node] = True\n        for neighbor in adj[node]:\n            if not visited[neighbor]:\n                if dfs(neighbor, node): return True\n            elif neighbor != parent:\n                return True\n        return False\n    for i in range(V):\n        if not visited[i]:\n            if dfs(i, -1): return True\n    return False", "time_complexity": "O(V + E)", "space_complexity": "O(V)"},
        "hints": ["Track the parent of each node during DFS.", "If you find a visited neighbor that isn't the parent, cycle exists.", "Handle disconnected components."],
        "topics": ["Graph", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-06", "topic": "Graphs", "topic_order": 5, "problem_order": 6,
        "question_title": "Topological Sort",
        "statement": "Given a directed acyclic graph (DAG) with V vertices and edges, find a topological ordering.",
        "examples": [{"input": "V=6, edges=[[2,3],[3,4],[1,2],[1,4]]", "output": "[1,2,3,4] or any valid order"}, {"input": "V=3, edges=[[1,2],[2,3]]", "output": "[1,2,3]"}],
        "constraints": ["1 <= V <= 10^4"],
        "visible_test_cases": [{"input": "4\n2 3\n3 4\n1 2\n1 4", "expected": "1 2 3 4"}, {"input": "3\n1 2\n2 3", "expected": "1 2 3"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "2\n1 2", "expected": "1 2"}, {"input": "4\n1 2\n1 3\n2 4\n3 4", "expected": "1 2 3 4"}],
        "solution": {"approach": "Kahn's algorithm: BFS with in-degree tracking.", "code": "from collections import deque\ndef topologicalSort(V, adj):\n    in_degree = [0] * V\n    for i in range(V):\n        for neighbor in adj[i]:\n            in_degree[neighbor] += 1\n    queue = deque([i for i in range(V) if in_degree[i] == 0])\n    result = []\n    while queue:\n        node = queue.popleft()\n        result.append(node)\n        for neighbor in adj[node]:\n            in_degree[neighbor] -= 1\n            if in_degree[neighbor] == 0:\n                queue.append(neighbor)\n    return result", "time_complexity": "O(V + E)", "space_complexity": "O(V)"},
        "hints": ["Compute in-degree of each node.", "Start with nodes having 0 in-degree.", "Reduce in-degree of neighbors as you process each node."],
        "topics": ["Graph", "Topological Sort", "BFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-07", "topic": "Graphs", "topic_order": 5, "problem_order": 7,
        "question_title": "Shortest Path in Weighted Graph (Dijkstra)",
        "statement": "Given a weighted directed graph with V vertices and source vertex S, find the shortest distance from S to all other vertices.",
        "examples": [{"input": "V=3, S=0, edges=[[0,1,1],[0,2,6],[1,2,3]]", "output": "[0,1,4]"}, {"input": "V=2, S=0, edges=[[0,1,5]]", "output": "[0,5]"}],
        "constraints": ["1 <= V <= 10^4"],
        "visible_test_cases": [{"input": "3 0\n0 1 1\n0 2 6\n1 2 3", "expected": "0 1 4"}, {"input": "2 0\n0 1 5", "expected": "0 5"}],
        "hidden_test_cases": [{"input": "1 0", "expected": "0"}, {"input": "3 0\n0 1 4\n0 2 2", "expected": "0 4 2"}, {"input": "4 0\n0 1 1\n0 2 5\n1 2 2\n2 3 1", "expected": "0 1 3 4"}],
        "solution": {"approach": "Min-heap (priority queue) with distance tracking.", "code": "import heapq\ndef dijkstra(V, adj, S):\n    dist = [float('inf')] * V\n    dist[S] = 0\n    heap = [(0, S)]\n    while heap:\n        d, node = heapq.heappop(heap)\n        if d > dist[node]: continue\n        for neighbor, weight in adj[node]:\n            if dist[node] + weight < dist[neighbor]:\n                dist[neighbor] = dist[node] + weight\n                heapq.heappush(heap, (dist[neighbor], neighbor))\n    return dist", "time_complexity": "O((V+E) log V)", "space_complexity": "O(V)"},
        "hints": ["Use a min-heap to always process the closest node.", "Relax edges: if shorter path found, update distance.", "Skip nodes already processed with shorter distance."],
        "topics": ["Graph", "Dijkstra", "Heap"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-08", "topic": "Graphs", "topic_order": 5, "problem_order": 8,
        "question_title": "Flood Fill Algorithm",
        "statement": "Given an image (2D grid) and a starting pixel, flood fill the image by changing all connected pixels of the same color to a new color.",
        "examples": [{"input": "image=[[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, newColor=2", "output": "[[2,2,2],[2,2,0],[2,0,1]]"}, {"input": "image=[[0,0,0],[0,0,0]], sr=0, sc=0, newColor=2", "output": "[[2,2,2],[2,2,2]]"}],
        "constraints": ["m == image.length", "n == image[i].length", "1 <= m, n <= 50"],
        "visible_test_cases": [{"input": "3 3\n1 1 1\n1 1 0\n1 0 1\n1 1 2", "expected": "2 2 2\n2 2 0\n2 0 1"}, {"input": "2 3\n0 0 0\n0 0 0\n0 0 2", "expected": "2 2 2\n2 2 2"}],
        "hidden_test_cases": [{"input": "1 1\n1\n0 0 5", "expected": "5"}, {"input": "2 2\n1 1\n1 1\n0 0 2", "expected": "2 2\n2 2"}, {"input": "3 3\n1 1 1\n1 0 1\n1 1 1\n1 1 2", "expected": "2 2 2\n2 0 2\n2 2 2"}],
        "solution": {"approach": "DFS/BFS from starting pixel, fill all connected same-color pixels.", "code": "def floodFill(image, sr, sc, newColor):\n    oldColor = image[sr][sc]\n    if oldColor == newColor: return image\n    def dfs(r, c):\n        if r < 0 or r >= len(image) or c < 0 or c >= len(image[0]): return\n        if image[r][c] != oldColor: return\n        image[r][c] = newColor\n        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)\n    dfs(sr, sc)\n    return image", "time_complexity": "O(m*n)", "space_complexity": "O(m*n)"},
        "hints": ["Check if new color equals old color to avoid infinite recursion.", "Use DFS or BFS to flood fill connected pixels.", "Check boundaries and color match before filling."],
        "topics": ["Graph", "DFS", "Matrix"], "companies": ["Amazon", "Microsoft", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-09", "topic": "Graphs", "topic_order": 5, "problem_order": 9,
        "question_title": "Number of Islands",
        "statement": "Given an m x n grid of '1's (land) and '0's (water), count the number of islands. An island is formed by connecting adjacent lands horizontally or vertically.",
        "examples": [{"input": "grid = [['1','1','0'],['1','1','0'],['0','0','1']]", "output": "2"}, {"input": "grid = [['1','1','1'],['0','1','0'],['1','1','1']]", "output": "1"}],
        "constraints": ["m == grid.length", "n == grid[i].length", "1 <= m, n <= 300"],
        "visible_test_cases": [{"input": "3 3\n1 1 0\n1 1 0\n0 0 1", "expected": "2"}, {"input": "3 3\n1 1 1\n0 1 0\n1 1 1", "expected": "1"}],
        "hidden_test_cases": [{"input": "1 1\n1", "expected": "1"}, {"input": "2 2\n0 0\n0 0", "expected": "0"}, {"input": "3 3\n1 0 1\n0 1 0\n1 0 1", "expected": "5"}],
        "solution": {"approach": "DFS/BFS: when you find a '1', flood fill to mark the entire island.", "code": "def numIslands(grid):\n    if not grid: return 0\n    count = 0\n    for i in range(len(grid)):\n        for j in range(len(grid[0])):\n            if grid[i][j] == '1':\n                count += 1\n                dfs(grid, i, j)\n    return count\ndef dfs(grid, i, j):\n    if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]) or grid[i][j] != '1':\n        return\n    grid[i][j] = '0'\n    dfs(grid, i+1, j); dfs(grid, i-1, j); dfs(grid, i, j+1); dfs(grid, i, j-1)", "time_complexity": "O(m*n)", "space_complexity": "O(m*n)"},
        "hints": ["Iterate through every cell in the grid.", "When you find a '1', it's a new island — increment count.", "Use DFS to mark all connected '1's as visited (set to '0')."],
        "topics": ["Graph", "DFS", "Matrix"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-10", "topic": "Graphs", "topic_order": 5, "problem_order": 10,
        "question_title": "Clone Graph",
        "statement": "Given a reference of a node in a connected undirected graph, return a deep copy of the graph.",
        "examples": [{"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "Deep copy with same structure"}, {"input": "adjList = [[]]", "output": "[[]]"}],
        "constraints": ["0 <= n <= 100", "-10^4 <= Node.val <= 10^4"],
        "visible_test_cases": [{"input": "4\n2 4\n1 3\n2 4\n1 3", "expected": "copied"}, {"input": "1\nempty", "expected": "copied"}],
        "hidden_test_cases": [{"input": "0", "expected": ""}, {"input": "1\nempty", "expected": "copied"}, {"input": "2\n2\n1", "expected": "copied"}],
        "solution": {"approach": "DFS/BFS with hash map to track cloned nodes.", "code": "def cloneGraph(node):\n    if not node: return None\n    clones = {node: Node(node.val)}\n    stack = [node]\n    while stack:\n        curr = stack.pop()\n        for neighbor in curr.neighbors:\n            if neighbor not in clones:\n                clones[neighbor] = Node(neighbor.val)\n                stack.append(neighbor)\n            clones[curr].neighbors.append(clones[neighbor])\n    return clones[node]", "time_complexity": "O(V + E)", "space_complexity": "O(V)"},
        "hints": ["Use a hash map to map original nodes to cloned nodes.", "When you encounter a new node, clone it and add to map.", "When you see an already-cloned node, use the existing clone."],
        "topics": ["Graph", "DFS", "Hash Table"], "companies": ["Amazon", "Google", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # TOPIC 6: DYNAMIC PROGRAMMING — 25 problems
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "DP-01", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 1,
        "question_title": "Climbing Stairs",
        "statement": "You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top?",
        "examples": [{"input": "n = 2", "output": "2"}, {"input": "n = 3", "output": "3"}],
        "constraints": ["1 <= n <= 45"],
        "visible_test_cases": [{"input": "2", "expected": "2"}, {"input": "3", "expected": "3"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "4", "expected": "5"}, {"input": "5", "expected": "8"}],
        "solution": {"approach": "Fibonacci pattern: dp[i] = dp[i-1] + dp[i-2].", "code": "def climbStairs(n):\n    if n <= 2: return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["The number of ways to reach step n is the sum of ways to reach n-1 and n-2.", "This is the Fibonacci sequence.", "Use constant space by tracking only the last two values."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-02", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 2,
        "question_title": "0/1 Knapsack Problem",
        "statement": "Given weights and values of n items, put them in a knapsack of capacity W to get the maximum total value. Each item can either be taken or not.",
        "examples": [{"input": "N=3, W=4, val=[1,2,3], wt=[4,5,1]", "output": "3"}, {"input": "N=3, W=3, val=[1,2,3], wt=[4,5,6]", "output": "0"}],
        "constraints": ["1 <= N <= 1000", "1 <= W <= 1000"],
        "visible_test_cases": [{"input": "3 4\n1 2 3\n4 5 1", "expected": "3"}, {"input": "3 3\n1 2 3\n4 5 6", "expected": "0"}],
        "hidden_test_cases": [{"input": "1 1\n1\n1", "expected": "1"}, {"input": "2 5\n10 20\n2 3", "expected": "30"}, {"input": "3 7\n10 20 30\n1 3 4", "expected": "50"}],
        "solution": {"approach": "2D DP: dp[i][w] = max value using first i items with capacity w.", "code": "def knapsack(W, wt, val, n):\n    dp = [[0]*(W+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for w in range(1, W+1):\n            if wt[i-1] <= w:\n                dp[i][w] = max(val[i-1]+dp[i-1][w-wt[i-1]], dp[i-1][w])\n            else:\n                dp[i][w] = dp[i-1][w]\n    return dp[n][W]", "time_complexity": "O(N*W)", "space_complexity": "O(N*W)"},
        "hints": ["For each item, decide to include or exclude it.", "If including: value = item_value + dp[item][remaining_weight].", "If excluding: value = dp[item-1][weight]."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-03", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 3,
        "question_title": "Longest Common Subsequence",
        "statement": "Given two strings text1 and text2, return the length of their longest common subsequence.",
        "examples": [{"input": "text1 = \"abcde\", text2 = \"ace\"", "output": "3"}, {"input": "text1 = \"abc\", text2 = \"def\"", "output": "0"}],
        "constraints": ["1 <= text1.length, text2.length <= 1000"],
        "visible_test_cases": [{"input": "abcde\nace", "expected": "3"}, {"input": "abc\ndef", "expected": "0"}],
        "hidden_test_cases": [{"input": "abc\nabc", "expected": "3"}, {"input": "abc\ndef", "expected": "0"}, {"input": "abcde\nace", "expected": "3"}],
        "solution": {"approach": "2D DP: if chars match, dp[i][j] = dp[i-1][j-1]+1, else max of diagonals.", "code": "def longestCommonSubsequence(text1, text2):\n    m, n = len(text1), len(text2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if text1[i-1] == text2[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]", "time_complexity": "O(m*n)", "space_complexity": "O(m*n)"},
        "hints": ["Create a 2D table where dp[i][j] = LCS length of first i chars of text1 and first j of text2.", "If characters match, extend the LCS.", "Otherwise, take the max of excluding one character from either string."],
        "topics": ["Dynamic Programming", "String"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-04", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 4,
        "question_title": "Longest Increasing Subsequence",
        "statement": "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "examples": [{"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4"}, {"input": "nums = [0,1,0,3,2,3]", "output": "4"}],
        "constraints": ["1 <= nums.length <= 2500", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [{"input": "8\n10 9 2 5 3 7 101 18", "expected": "4"}, {"input": "6\n0 1 0 3 2 3", "expected": "4"}],
        "hidden_test_cases": [{"input": "1\n0", "expected": "1"}, {"input": "4\n7 7 7 7", "expected": "1"}, {"input": "6\n0 1 0 3 2 3", "expected": "4"}],
        "solution": {"approach": "DP with binary search for O(n log n).", "code": "import bisect\ndef lengthOfLIS(nums):\n    tails = []\n    for num in nums:\n        pos = bisect.bisect_left(tails, num)\n        if pos == len(tails):\n            tails.append(num)\n        else:\n            tails[pos] = num\n    return len(tails)", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Use a tails array where tails[i] = smallest tail element for LIS of length i+1.", "For each element, find its position using binary search.", "Update or append to the tails array."],
        "topics": ["Dynamic Programming", "Binary Search"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-05", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 5,
        "question_title": "Coin Change",
        "statement": "Given an integer array coins and an integer amount, return the fewest coins needed to make up that amount. Return -1 if not possible.",
        "examples": [{"input": "coins = [1,5,11], amount = 15", "output": "3"}, {"input": "coins = [2], amount = 3", "output": "-1"}],
        "constraints": ["1 <= coins.length <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"],
        "visible_test_cases": [{"input": "3 15\n1 5 11", "expected": "3"}, {"input": "1 3\n2", "expected": "-1"}],
        "hidden_test_cases": [{"input": "1 0\n1", "expected": "0"}, {"input": "3 11\n1 2 5", "expected": "3"}, {"input": "1 1\n1", "expected": "1"}],
        "solution": {"approach": "Bottom-up DP: dp[i] = min coins to make amount i.", "code": "def coinChange(coins, amount):\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for i in range(1, amount + 1):\n        for coin in coins:\n            if coin <= i and dp[i - coin] + 1 < dp[i]:\n                dp[i] = dp[i - coin] + 1\n    return dp[amount] if dp[amount] != float('inf') else -1", "time_complexity": "O(amount * len(coins))", "space_complexity": "O(amount)"},
        "hints": ["dp[i] = minimum coins to make amount i.", "For each amount, try all coins and take the minimum.", "Base case: dp[0] = 0 (0 coins for amount 0)."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-06", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 6,
        "question_title": "Edit Distance",
        "statement": "Given two strings word1 and word2, return the minimum number of operations (insert, delete, replace) to convert word1 to word2.",
        "examples": [{"input": "word1 = \"horse\", word2 = \"ros\"", "output": "3"}, {"input": "word1 = \"intention\", word2 = \"execution\"", "output": "5"}],
        "constraints": ["0 <= word1.length, word2.length <= 500"],
        "visible_test_cases": [{"input": "horse\nros", "expected": "3"}, {"input": "intention\nexecution", "expected": "5"}],
        "hidden_test_cases": [{"input": "a\na", "expected": "0"}, {"input": "a\nb", "expected": "1"}, {"input": "abc\nadc", "expected": "1"}],
        "solution": {"approach": "2D DP: dp[i][j] = min operations to convert first i chars to first j chars.", "code": "def minDistance(word1, word2):\n    m, n = len(word1), len(word2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(m+1): dp[i][0] = i\n    for j in range(n+1): dp[0][j] = j\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if word1[i-1] == word2[j-1]:\n                dp[i][j] = dp[i-1][j-1]\n            else:\n                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n    return dp[m][n]", "time_complexity": "O(m*n)", "space_complexity": "O(m*n)"},
        "hints": ["If characters match, no operation needed (inherit diagonal).", "Otherwise, take min of: delete, insert, replace + 1.", "Base cases: converting empty string requires i or j operations."],
        "topics": ["Dynamic Programming", "String"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-07", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 7,
        "question_title": "Maximum Sum of Non-Adjacent Elements",
        "statement": "Given an array of positive integers, find the maximum sum of non-adjacent elements.",
        "examples": [{"input": "nums = [6, 5, 5, 7, 4]", "output": "15"}, {"input": "nums = [1, 2, 3]", "output": "4"}],
        "constraints": ["1 <= nums.length <= 10^5"],
        "visible_test_cases": [{"input": "5\n6 5 5 7 4", "expected": "15"}, {"input": "3\n1 2 3", "expected": "4"}],
        "hidden_test_cases": [{"input": "1\n5", "expected": "5"}, {"input": "2\n1 100", "expected": "100"}, {"input": "4\n3 2 5 10", "expected": "13"}],
        "solution": {"approach": "DP: at each element, max = max(include, exclude).", "code": "def maxSubsetSum(nums):\n    incl = excl = 0\n    for num in nums:\n        new_excl = max(incl, excl)\n        incl = excl + num\n        excl = new_excl\n    return max(incl, excl)", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["At each position, track two values: max including current and max excluding.", "If you include current, you must exclude previous.", "If you exclude current, take max of previous include/exclude."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-08", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 8,
        "question_title": "House Robber",
        "statement": "Given an integer array nums representing the amount of money at each house, return the maximum amount you can rob without robbing two adjacent houses.",
        "examples": [{"input": "nums = [1,2,3,1]", "output": "4"}, {"input": "nums = [2,7,9,3,1]", "output": "12"}],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 400"],
        "visible_test_cases": [{"input": "4\n1 2 3 1", "expected": "4"}, {"input": "5\n2 7 9 3 1", "expected": "12"}],
        "hidden_test_cases": [{"input": "1\n5", "expected": "5"}, {"input": "2\n1 2", "expected": "2"}, {"input": "3\n2 1 1", "expected": "3"}],
        "solution": {"approach": "DP: dp[i] = max(dp[i-1], dp[i-2] + nums[i]).", "code": "def rob(nums):\n    if len(nums) == 1: return nums[0]\n    a, b = nums[0], max(nums[0], nums[1])\n    for i in range(2, len(nums)):\n        a, b = b, max(b, a + nums[i])\n    return b", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["At each house, decide to rob or skip.", "If robbing, add to the best result from 2 houses back.", "If skipping, carry forward the best result from the previous house."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-09", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 9,
        "question_title": "Subset Sum Problem",
        "statement": "Given an array of non-negative integers and a target sum, determine if there is a subset with the given sum.",
        "examples": [{"input": "arr = [3,34,4,12,5,2], sum = 9", "output": "true"}, {"input": "arr = [3,34,4,12,5,2], sum = 30", "output": "false"}],
        "constraints": ["1 <= n <= 100", "1 <= arr[i] <= 1000", "1 <= sum <= 1000"],
        "visible_test_cases": [{"input": "6 9\n3 34 4 12 5 2", "expected": "true"}, {"input": "6 30\n3 34 4 12 5 2", "expected": "false"}],
        "hidden_test_cases": [{"input": "1 5\n5", "expected": "true"}, {"input": "3 0\n1 2 3", "expected": "true"}, {"input": "3 7\n1 2 3", "expected": "false"}],
        "solution": {"approach": "2D DP: dp[i][j] = True if subset of first i elements sums to j.", "code": "def isSubsetSum(arr, sum):\n    n = len(arr)\n    dp = [[False]*(sum+1) for _ in range(n+1)]\n    for i in range(n+1): dp[i][0] = True\n    for i in range(1, n+1):\n        for j in range(1, sum+1):\n            if arr[i-1] <= j:\n                dp[i][j] = dp[i-1][j] or dp[i-1][j-arr[i-1]]\n            else:\n                dp[i][j] = dp[i-1][j]\n    return dp[n][sum]", "time_complexity": "O(n*sum)", "space_complexity": "O(n*sum)"},
        "hints": ["For each element, decide to include or exclude it.", "If including: check if subset sums to (j - element).", "Base case: sum of 0 is always possible (empty subset)."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "TCS", "Infosys"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-10", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 10,
        "question_title": "Rod Cutting Problem",
        "statement": "Given a rod of length n and an array of prices for each piece, determine the maximum revenue by cutting up the rod.",
        "examples": [{"input": "n=8, price=[1,5,8,9,10,17,17,20]", "output": "22"}, {"input": "n=4, price=[2,5,7,8]", "output": "10"}],
        "constraints": ["1 <= n <= 1000"],
        "visible_test_cases": [{"input": "8\n1 5 8 9 10 17 17 20", "expected": "22"}, {"input": "4\n2 5 7 8", "expected": "10"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "2\n1 5", "expected": "5"}, {"input": "3\n1 5 8", "expected": "8"}],
        "solution": {"approach": "Unbounded knapsack variant: dp[i] = max revenue for rod of length i.", "code": "def cutRod(price, n):\n    dp = [0] * (n + 1)\n    for i in range(1, n + 1):\n        for j in range(i):\n            dp[i] = max(dp[i], price[j] + dp[i - j - 1])\n    return dp[n]", "time_complexity": "O(n^2)", "space_complexity": "O(n)"},
        "hints": ["For each length i, try all possible first cuts.", "dp[i] = max price[j] + dp[i-j-1] for all j < i.", "This is an unbounded knapsack variant."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Microsoft", "TCS"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-11", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 11,
        "question_title": "Grid Unique Paths",
        "statement": "There is a robot on an m x n grid. It starts at top-left and can only move down or right. How many unique paths to reach bottom-right?",
        "examples": [{"input": "m = 3, n = 7", "output": "28"}, {"input": "m = 3, n = 2", "output": "3"}],
        "constraints": ["1 <= m, n <= 100"],
        "visible_test_cases": [{"input": "3 7", "expected": "28"}, {"input": "3 2", "expected": "3"}],
        "hidden_test_cases": [{"input": "1 1", "expected": "1"}, {"input": "3 3", "expected": "6"}, {"input": "7 3", "expected": "28"}],
        "solution": {"approach": "DP: dp[i][j] = dp[i-1][j] + dp[i][j-1].", "code": "def uniquePaths(m, n):\n    dp = [[1]*n for _ in range(m)]\n    for i in range(1, m):\n        for j in range(1, n):\n            dp[i][j] = dp[i-1][j] + dp[i][j-1]\n    return dp[m-1][n-1]", "time_complexity": "O(m*n)", "space_complexity": "O(m*n)"},
        "hints": ["First row and first column are all 1 (only one way to reach).", "Each cell = sum of cell above and cell to the left.", "Bottom-right cell is the answer."],
        "topics": ["Dynamic Programming", "Math"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-12", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 12,
        "question_title": "Longest Palindromic Subsequence",
        "statement": "Given a string s, find the length of the longest palindromic subsequence.",
        "examples": [{"input": "s = \"bbbab\"", "output": "4"}, {"input": "s = \"cbbd\"", "output": "2"}],
        "constraints": ["1 <= s.length <= 1000"],
        "visible_test_cases": [{"input": "bbbab", "expected": "4"}, {"input": "cbbd", "expected": "2"}],
        "hidden_test_cases": [{"input": "a", "expected": "1"}, {"input": "abcba", "expected": "5"}, {"input": "abcda", "expected": "3"}],
        "solution": {"approach": "LCS of string and its reverse.", "code": "def longestPalindromeSubseq(s):\n    t = s[::-1]\n    n = len(s)\n    dp = [[0]*(n+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for j in range(1, n+1):\n            if s[i-1] == t[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[n][n]", "time_complexity": "O(n^2)", "space_complexity": "O(n^2)"},
        "hints": ["The longest palindromic subsequence is the LCS of the string and its reverse.", "Use standard LCS algorithm.", "Alternatively, use interval DP."],
        "topics": ["Dynamic Programming", "String"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-13", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 13,
        "question_title": "Word Break",
        "statement": "Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of dictionary words.",
        "examples": [{"input": "s = \"leetcode\", wordDict = [\"leet\",\"code\"]", "output": "true"}, {"input": "s = \"catsandog\", wordDict = [\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]", "output": "false"}],
        "constraints": ["1 <= s.length <= 300", "1 <= wordDict.length <= 1000"],
        "visible_test_cases": [{"input": "leetcode\nleet code", "expected": "true"}, {"input": "catsandog\ncats dog sand and cat", "expected": "false"}],
        "hidden_test_cases": [{"input": "applepen\napple pen", "expected": "true"}, {"input": "a\nb", "expected": "false"}, {"input": "a\na", "expected": "true"}],
        "solution": {"approach": "DP: dp[i] = True if s[0:i] can be segmented.", "code": "def wordBreak(s, wordDict):\n    words = set(wordDict)\n    dp = [False] * (len(s) + 1)\n    dp[0] = True\n    for i in range(1, len(s) + 1):\n        for j in range(i):\n            if dp[j] and s[j:i] in words:\n                dp[i] = True\n                break\n    return dp[len(s)]", "time_complexity": "O(n^2 * k)", "space_complexity": "O(n)"},
        "hints": ["dp[i] is True if s[0:i] can be segmented.", "For each position i, check all possible last words.", "If dp[j] is True and s[j:i] is in dictionary, dp[i] = True."],
        "topics": ["Dynamic Programming", "String"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-14", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 14,
        "question_title": "Minimum Path Sum",
        "statement": "Given a m x n grid filled with non-negative numbers, find a path from top-left to bottom-right that minimizes the sum of numbers along the path.",
        "examples": [{"input": "grid = [[1,3,1],[1,5,1],[4,2,1]]", "output": "7"}, {"input": "grid = [[1,2,3],[4,5,6]]", "output": "12"}],
        "constraints": ["m == grid.length", "n == grid[i].length", "1 <= m, n <= 200"],
        "visible_test_cases": [{"input": "3 3\n1 3 1\n1 5 1\n4 2 1", "expected": "7"}, {"input": "2 3\n1 2 3\n4 5 6", "expected": "12"}],
        "hidden_test_cases": [{"input": "1 1\n1", "expected": "1"}, {"input": "1 3\n1 2 3", "expected": "6"}, {"input": "3 1\n1\n2\n3", "expected": "6"}],
        "solution": {"approach": "DP: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]).", "code": "def minPathSum(grid):\n    m, n = len(grid), len(grid[0])\n    for i in range(m):\n        for j in range(n):\n            if i == 0 and j == 0: continue\n            elif i == 0: grid[i][j] += grid[i][j-1]\n            elif j == 0: grid[i][j] += grid[i-1][j]\n            else: grid[i][j] += min(grid[i-1][j], grid[i][j-1])\n    return grid[m-1][n-1]", "time_complexity": "O(m*n)", "space_complexity": "O(1)"},
        "hints": ["Start from top-left, accumulate minimum path sum.", "For each cell, add the minimum of the cell above or to the left.", "First row and first column have only one way to reach."],
        "topics": ["Dynamic Programming", "Matrix"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-15", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 15,
        "question_title": "Partition Equal Subset Sum",
        "statement": "Given a non-empty array of positive integers, determine if the array can be partitioned into two subsets with equal sum.",
        "examples": [{"input": "nums = [1,5,11,5]", "output": "true"}, {"input": "nums = [1,2,3,5]", "output": "false"}],
        "constraints": ["1 <= nums.length <= 200", "1 <= nums[i] <= 100"],
        "visible_test_cases": [{"input": "4\n1 5 11 5", "expected": "true"}, {"input": "4\n1 2 3 5", "expected": "false"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "false"}, {"input": "2\n1 1", "expected": "true"}, {"input": "3\n1 2 3", "expected": "true"}],
        "solution": {"approach": "Subset sum problem: check if any subset sums to total/2.", "code": "def canPartition(nums):\n    total = sum(nums)\n    if total % 2: return False\n    target = total // 2\n    dp = [False] * (target + 1)\n    dp[0] = True\n    for num in nums:\n        for j in range(target, num - 1, -1):\n            dp[j] = dp[j] or dp[j - num]\n    return dp[target]", "time_complexity": "O(n * target)", "space_complexity": "O(target)"},
        "hints": ["If total sum is odd, can't partition equally.", "Check if any subset sums to total/2.", "Use 1D DP (0/1 knapsack variant)."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # TOPIC 7: GREEDY — 15 problems
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "GRDY-01", "topic": "Greedy", "topic_order": 7, "problem_order": 1,
        "question_title": "Activity Selection Problem",
        "statement": "Given n activities with start and finish times, select the maximum number of activities that can be performed by a single person.",
        "examples": [{"input": "start=[1,3,0,5,8,5], finish=[2,4,6,7,9,9]", "output": "4"}, {"input": "start=[1,2], finish=[3,4]", "output": "2"}],
        "constraints": ["1 <= n <= 10^5"],
        "visible_test_cases": [{"input": "6\n1 3 0 5 8 5\n2 4 6 7 9 9", "expected": "4"}, {"input": "2\n1 2\n3 4", "expected": "2"}],
        "hidden_test_cases": [{"input": "1\n1\n2", "expected": "1"}, {"input": "3\n1 2 3\n2 3 4", "expected": "2"}, {"input": "4\n1 2 3 4\n5 6 7 8", "expected": "4"}],
        "solution": {"approach": "Greedy: sort by finish time, pick non-overlapping.", "code": "def activitySelection(start, finish):\n    activities = sorted(zip(finish, start))\n    count = 1\n    last_finish = activities[0][0]\n    for i in range(1, len(activities)):\n        if activities[i][1] >= last_finish:\n            count += 1\n            last_finish = activities[i][0]\n    return count", "time_complexity": "O(n log n)", "space_complexity": "O(1)"},
        "hints": ["Sort activities by finish time.", "Always pick the activity with the earliest finish time.", "Skip activities that overlap with the last selected one."],
        "topics": ["Greedy", "Sorting"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GRDY-02", "topic": "Greedy", "topic_order": 7, "problem_order": 2,
        "question_title": "Fractional Knapsack",
        "statement": "Given weights and values of n items and a knapsack of capacity W, find the maximum value. You can break items (take fractions).",
        "examples": [{"input": "N=3, W=50, values=[60,100,120], weights=[10,20,30]", "output": "240.00"}, {"input": "N=2, W=50, values=[60,100], weights=[10,20]", "output": "160.00"}],
        "constraints": ["1 <= N <= 10^4", "1 <= W <= 10^4"],
        "visible_test_cases": [{"input": "3 50\n60 100 120\n10 20 30", "expected": "240.00"}, {"input": "2 50\n60 100\n10 20", "expected": "160.00"}],
        "hidden_test_cases": [{"input": "1 10\n100\n5", "expected": "100.00"}, {"input": "3 10\n60 100 120\n10 20 30", "expected": "60.00"}, {"input": "2 15\n10 20\n5 10", "expected": "30.00"}],
        "solution": {"approach": "Greedy: sort by value/weight ratio, take as much as possible.", "code": "def fractionalKnapsack(W, val, wt):\n    items = sorted(zip(val, wt), key=lambda x: x[0]/x[1], reverse=True)\n    total = 0\n    for v, w in items:\n        if W >= w:\n            total += v\n            W -= w\n        else:\n            total += v * (W / w)\n            break\n    return total", "time_complexity": "O(n log n)", "space_complexity": "O(1)"},
        "hints": ["Sort items by value-to-weight ratio.", "Take as much as possible of the highest ratio item.", "If the item doesn't fit completely, take a fraction."],
        "topics": ["Greedy", "Sorting"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GRDY-03", "topic": "Greedy", "topic_order": 7, "problem_order": 3,
        "question_title": "Jump Game",
        "statement": "Given an integer array nums where nums[i] represents the maximum jump length from position i, determine if you can reach the last index.",
        "examples": [{"input": "nums = [2,3,1,1,4]", "output": "true"}, {"input": "nums = [3,2,1,0,4]", "output": "false"}],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 10^5"],
        "visible_test_cases": [{"input": "5\n2 3 1 1 4", "expected": "true"}, {"input": "5\n3 2 1 0 4", "expected": "false"}],
        "hidden_test_cases": [{"input": "1\n0", "expected": "true"}, {"input": "2\n2 0", "expected": "true"}, {"input": "3\n2 0 0", "expected": "true"}],
        "solution": {"approach": "Greedy: track the farthest reachable position.", "code": "def canJump(nums):\n    max_reach = 0\n    for i in range(len(nums)):\n        if i > max_reach: return False\n        max_reach = max(max_reach, i + nums[i])\n    return True", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Track the farthest position you can reach.", "If current index exceeds the farthest reachable, you're stuck.", "Update farthest reachable at each step."],
        "topics": ["Greedy", "Array"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GRDY-04", "topic": "Greedy", "topic_order": 7, "problem_order": 4,
        "question_title": "Job Sequencing Problem",
        "statement": "Given a set of n jobs with deadlines and profits, find the sequence of jobs that maximizes total profit. Each job takes 1 unit of time.",
        "examples": [{"input": "jobs = [(1,4,20),(2,1,10),(3,1,40),(4,1,30)]", "output": "[2,4,3], profit=60"}, {"input": "jobs = [(1,2,100),(2,1,19),(3,2,27),(4,1,25),(5,1,15)]", "output": "[2,1,4,5,3], profit=185"}],
        "constraints": ["1 <= n <= 10^5"],
        "visible_test_cases": [{"input": "4\n1 4 20\n2 1 10\n3 1 40\n4 1 30", "expected": "2 4 3"}, {"input": "5\n1 2 100\n2 1 19\n3 2 27\n4 1 25\n5 1 15", "expected": "2 1 4 5 3"}],
        "hidden_test_cases": [{"input": "1\n1 1 50", "expected": "1"}, {"input": "3\n1 1 10\n2 1 20\n3 1 30", "expected": "3 2 1"}, {"input": "2\n1 2 50\n2 1 10", "expected": "1 2"}],
        "solution": {"approach": "Greedy: sort by profit, assign each job to the latest available slot.", "code": "def jobScheduling(jobs):\n    jobs.sort(key=lambda x: x[2], reverse=True)\n    max_deadline = max(j[1] for j in jobs)\n    slots = [-1] * (max_deadline + 1)\n    total_profit = 0\n    count = 0\n    for job in jobs:\n        for j in range(job[1], 0, -1):\n            if slots[j] == -1:\n                slots[j] = job[0]\n                total_profit += job[2]\n                count += 1\n                break\n    return [i for i in slots if i != -1]", "time_complexity": "O(n^2)", "space_complexity": "O(max_deadline)"},
        "hints": ["Sort jobs by profit in descending order.", "Try to schedule each job at its deadline.", "If the slot is occupied, try earlier slots."],
        "topics": ["Greedy", "Sorting"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GRDY-05", "topic": "Greedy", "topic_order": 7, "problem_order": 5,
        "question_title": "Merge Intervals",
        "statement": "Given an array of intervals, merge all overlapping intervals and return the non-overlapping intervals.",
        "examples": [{"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"}, {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"}],
        "constraints": ["1 <= intervals.length <= 10^4"],
        "visible_test_cases": [{"input": "4\n1 3\n2 6\n8 10\n15 18", "expected": "1 6\n8 10\n15 18"}, {"input": "2\n1 4\n4 5", "expected": "1 5"}],
        "hidden_test_cases": [{"input": "1\n1 4", "expected": "1 4"}, {"input": "3\n1 4\n0 4", "expected": "0 4"}, {"input": "2\n1 4\n2 3", "expected": "1 4"}],
        "solution": {"approach": "Sort by start time, merge overlapping.", "code": "def merge(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for start, end in intervals[1:]:\n        if start <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], end)\n        else:\n            merged.append([start, end])\n    return merged", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Sort intervals by start time.", "If current overlaps with last merged, extend the end.", "Otherwise, add to result."],
        "topics": ["Greedy", "Sorting"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
]

# Add additional problems from all modules
PROBLEMS.extend(ADDITIONAL_PROBLEMS)
PROBLEMS.extend(EXTRA_PROBLEMS)
PROBLEMS.extend(FINAL_PROBLEMS)
PROBLEMS.extend(REMAINING_PROBLEMS)
PROBLEMS.extend(COMPLETE_FINAL)
PROBLEMS.extend(ULTIMATE_PROBLEMS)
PROBLEMS.extend(FINAL_BATCH)
PROBLEMS.extend(LAST_BATCH)
PROBLEMS.extend(COMPLETE_ULTIMATE)
PROBLEMS.extend(FINAL_COMPLETE)
PROBLEMS.extend(ULTIMATE_COMPLETE)
PROBLEMS.extend(LAST_COMPLETE)
PROBLEMS.extend(FINAL_ULTIMATE)
PROBLEMS.extend(COMPLETE_ULTIMATE_FINAL)
PROBLEMS.extend(LAST_ULTIMATE)
PROBLEMS.extend(COMPLETE_LAST)
PROBLEMS.extend(ULTIMATE_LAST)
PROBLEMS.extend(COMPLETE_ULTIMATE_LAST)
PROBLEMS.extend(LAST_FINAL)
PROBLEMS.extend(FINAL_ULTIMATE_LAST)
PROBLEMS.extend(COMPLETE_FINAL_LAST)
