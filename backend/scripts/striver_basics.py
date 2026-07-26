"""
Striver's A2Z Sheet — Additional problems for complete coverage.
Topics: Basics, Sorting, Binary Search, Strings, Recursion, Bit Manipulation,
Heaps, Sliding Window, BST, Tries, and more DP/Graph problems.
"""

ADDITIONAL_PROBLEMS = [
    # ═══════════════════════════════════════════════════════════════════════════
    # BASICS & MATH (topic_order=0)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "B-01", "topic": "Basics", "topic_order": 0, "problem_order": 1,
        "question_title": "Print 1 to N using Recursion",
        "statement": "Given an integer n, print numbers from 1 to n using recursion.",
        "examples": [{"input": "n = 5", "output": "1 2 3 4 5"}, {"input": "n = 3", "output": "1 2 3"}],
        "constraints": ["1 <= n <= 10000"],
        "visible_test_cases": [{"input": "5", "expected": "1 2 3 4 5"}, {"input": "3", "expected": "1 2 3"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "10", "expected": "1 2 3 4 5 6 7 8 9 10"}],
        "solution": {"approach": "Print after recursive call for ascending order.", "code": "def printN(n):\n    if n == 0: return\n    printN(n-1)\n    print(n, end=' ')", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Use recursion with base case n=0.", "Make recursive call first, then print.", "Stack unwinding gives reverse order."],
        "topics": ["Recursion"], "companies": ["TCS", "Infosys"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "B-02", "topic": "Basics", "topic_order": 0, "problem_order": 2,
        "question_title": "Sum of First N Numbers",
        "statement": "Find the sum of first n natural numbers using recursion.",
        "examples": [{"input": "n = 5", "output": "15"}, {"input": "n = 3", "output": "6"}],
        "constraints": ["1 <= n <= 100000"],
        "visible_test_cases": [{"input": "5", "expected": "15"}, {"input": "3", "expected": "6"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "10", "expected": "55"}],
        "solution": {"approach": "Recursive: f(n) = n + f(n-1).", "code": "def sumN(n):\n    if n == 0: return 0\n    return n + sumN(n-1)", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Base case: sum(0) = 0.", "Recursive case: sum(n) = n + sum(n-1).", "Can also use formula n*(n+1)/2."],
        "topics": ["Recursion", "Math"], "companies": ["TCS", "Wipro"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "B-03", "topic": "Basics", "topic_order": 0, "problem_order": 3,
        "question_title": "Factorial of N",
        "statement": "Find factorial of n using recursion.",
        "examples": [{"input": "n = 5", "output": "120"}, {"input": "n = 0", "output": "1"}],
        "constraints": ["0 <= n <= 20"],
        "visible_test_cases": [{"input": "5", "expected": "120"}, {"input": "0", "expected": "1"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "10", "expected": "3628800"}],
        "solution": {"approach": "Recursive: fact(n) = n * fact(n-1).", "code": "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n-1)", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Base case: factorial(0) = 1.", "Recursive case: factorial(n) = n * factorial(n-1)."],
        "topics": ["Recursion", "Math"], "companies": ["TCS", "Infosys"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "B-04", "topic": "Basics", "topic_order": 0, "problem_order": 4,
        "question_title": "Check Palindrome using Recursion",
        "statement": "Check if a string is a palindrome using recursion.",
        "examples": [{"input": "s = 'racecar'", "output": "true"}, {"input": "s = 'hello'", "output": "false"}],
        "constraints": ["1 <= s.length <= 10^5"],
        "visible_test_cases": [{"input": "racecar", "expected": "true"}, {"input": "hello", "expected": "false"}],
        "hidden_test_cases": [{"input": "a", "expected": "true"}, {"input": "ab", "expected": "false"}, {"input": "aba", "expected": "true"}],
        "solution": {"approach": "Compare first and last chars, recurse on middle.", "code": "def isPalindrome(s, l=0):\n    if l >= len(s)//2: return True\n    if s[l] != s[len(s)-1-l]: return False\n    return isPalindrome(s, l+1)", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Compare characters from both ends.", "Move pointers inward with each recursive call."],
        "topics": ["Recursion", "String"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "B-05", "topic": "Basics", "topic_order": 0, "problem_order": 5,
        "question_title": "Fibonacci Number",
        "statement": "Find the nth Fibonacci number using recursion.",
        "examples": [{"input": "n = 5", "output": "5"}, {"input": "n = 0", "output": "0"}],
        "constraints": ["0 <= n <= 30"],
        "visible_test_cases": [{"input": "5", "expected": "5"}, {"input": "0", "expected": "0"}],
        "hidden_test_cases": [{"input": "1", "expected": "1"}, {"input": "10", "expected": "55"}],
        "solution": {"approach": "Recursive: fib(n) = fib(n-1) + fib(n-2).", "code": "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)", "time_complexity": "O(2^n)", "space_complexity": "O(n)"},
        "hints": ["Base cases: fib(0)=0, fib(1)=1.", "Each number is sum of two preceding."],
        "topics": ["Recursion", "Math"], "companies": ["Amazon", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # SORTING (topic_order=0.5)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "S-01", "topic": "Sorting", "topic_order": 0, "problem_order": 10,
        "question_title": "Selection Sort",
        "statement": "Implement selection sort algorithm.",
        "examples": [{"input": "arr = [64, 25, 12, 22, 11]", "output": "[11, 12, 22, 25, 64]"}],
        "constraints": ["1 <= n <= 1000"],
        "visible_test_cases": [{"input": "5\n64 25 12 22 11", "expected": "11 12 22 25 64"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "3\n3 1 2", "expected": "1 2 3"}],
        "solution": {"approach": "Find minimum in unsorted part, swap with first unsorted.", "code": "def selectionSort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i+1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr", "time_complexity": "O(n^2)", "space_complexity": "O(1)"},
        "hints": ["Find minimum element in unsorted portion.", "Swap it with the first unsorted element."],
        "topics": ["Sorting"], "companies": ["TCS", "Infosys"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "S-02", "topic": "Sorting", "topic_order": 0, "problem_order": 11,
        "question_title": "Bubble Sort",
        "statement": "Implement bubble sort algorithm.",
        "examples": [{"input": "arr = [64, 34, 25, 12, 22, 11, 90]", "output": "[11, 12, 22, 25, 34, 64, 90]"}],
        "constraints": ["1 <= n <= 1000"],
        "visible_test_cases": [{"input": "7\n64 34 25 12 22 11 90", "expected": "11 12 22 25 34 64 90"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "5\n5 4 3 2 1", "expected": "1 2 3 4 5"}],
        "solution": {"approach": "Compare adjacent elements, swap if out of order.", "code": "def bubbleSort(arr):\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n                swapped = True\n        if not swapped: break\n    return arr", "time_complexity": "O(n^2)", "space_complexity": "O(1)"},
        "hints": ["Bubble largest element to end in each pass.", "Optimize with swapped flag."],
        "topics": ["Sorting"], "companies": ["TCS", "Wipro"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "S-03", "topic": "Sorting", "topic_order": 0, "problem_order": 12,
        "question_title": "Insertion Sort",
        "statement": "Implement insertion sort algorithm.",
        "examples": [{"input": "arr = [12, 11, 13, 5, 6]", "output": "[5, 6, 11, 12, 13]"}],
        "constraints": ["1 <= n <= 1000"],
        "visible_test_cases": [{"input": "5\n12 11 13 5 6", "expected": "5 6 11 12 13"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "4\n4 3 2 1", "expected": "1 2 3 4"}],
        "solution": {"approach": "Insert each element into its correct position in sorted part.", "code": "def insertionSort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j] > key:\n            arr[j+1] = arr[j]\n            j -= 1\n        arr[j+1] = key\n    return arr", "time_complexity": "O(n^2)", "space_complexity": "O(1)"},
        "hints": ["Assume first element is sorted.", "Insert each subsequent element into correct position."],
        "topics": ["Sorting"], "companies": ["TCS", "Infosys"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "S-04", "topic": "Sorting", "topic_order": 0, "problem_order": 13,
        "question_title": "Merge Sort",
        "statement": "Implement merge sort algorithm.",
        "examples": [{"input": "arr = [38, 27, 43, 3, 9, 82, 10]", "output": "[3, 9, 10, 27, 38, 43, 82]"}],
        "constraints": ["1 <= n <= 10^5"],
        "visible_test_cases": [{"input": "7\n38 27 43 3 9 82 10", "expected": "3 9 10 27 38 43 82"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "5\n5 4 3 2 1", "expected": "1 2 3 4 5"}],
        "solution": {"approach": "Divide array in halves, sort recursively, merge.", "code": "def mergeSort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr) // 2\n    left = mergeSort(arr[:mid])\n    right = mergeSort(arr[mid:])\n    return merge(left, right)\ndef merge(l, r):\n    result = []\n    i = j = 0\n    while i < len(l) and j < len(r):\n        if l[i] <= r[j]:\n            result.append(l[i]); i += 1\n        else:\n            result.append(r[j]); j += 1\n    result.extend(l[i:])\n    result.extend(r[j:])\n    return result", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Divide until single elements.", "Merge two sorted halves."],
        "topics": ["Sorting", "Divide and Conquer"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "S-05", "topic": "Sorting", "topic_order": 0, "problem_order": 14,
        "question_title": "Quick Sort",
        "statement": "Implement quicksort algorithm.",
        "examples": [{"input": "arr = [10, 7, 8, 9, 1, 5]", "output": "[1, 5, 7, 8, 9, 10]"}],
        "constraints": ["1 <= n <= 10^5"],
        "visible_test_cases": [{"input": "6\n10 7 8 9 1 5", "expected": "1 5 7 8 9 10"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "5\n5 4 3 2 1", "expected": "1 2 3 4 5"}],
        "solution": {"approach": "Pick pivot, partition around it, recurse on subarrays.", "code": "def quickSort(arr, low, high):\n    if low < high:\n        pi = partition(arr, low, high)\n        quickSort(arr, low, pi-1)\n        quickSort(arr, pi+1, high)\ndef partition(arr, low, high):\n    pivot = arr[high]\n    i = low - 1\n    for j in range(low, high):\n        if arr[j] < pivot:\n            i += 1\n            arr[i], arr[j] = arr[j], arr[i]\n    arr[i+1], arr[high] = arr[high], arr[i+1]\n    return i + 1", "time_complexity": "O(n log n) avg", "space_complexity": "O(log n)"},
        "hints": ["Choose a pivot element.", "Partition array so smaller elements are left of pivot."],
        "topics": ["Sorting", "Divide and Conquer"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # BINARY SEARCH (topic_order=1.5)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "BS-01", "topic": "Binary Search", "topic_order": 1, "problem_order": 25,
        "question_title": "Binary Search",
        "statement": "Implement binary search on a sorted array.",
        "examples": [{"input": "arr = [2,3,4,10,40], target = 10", "output": "3"}],
        "constraints": ["1 <= n <= 10^5", "Array is sorted"],
        "visible_test_cases": [{"input": "5 10\n2 3 4 10 40", "expected": "3"}, {"input": "5 5\n2 3 4 10 40", "expected": "-1"}],
        "hidden_test_cases": [{"input": "1 1\n1", "expected": "0"}, {"input": "3 3\n1 2 3", "expected": "2"}],
        "solution": {"approach": "Compare target with mid, eliminate half each time.", "code": "def binarySearch(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: lo = mid + 1\n        else: hi = mid - 1\n    return -1", "time_complexity": "O(log n)", "space_complexity": "O(1)"},
        "hints": ["Always search in sorted array.", "Eliminate half the search space each step."],
        "topics": ["Binary Search"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BS-02", "topic": "Binary Search", "topic_order": 1, "problem_order": 26,
        "question_title": "Search in Rotated Sorted Array",
        "statement": "Search for a target in a rotated sorted array.",
        "examples": [{"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"}],
        "constraints": ["1 <= nums.length <= 5000", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [{"input": "7 0\n4 5 6 7 0 1 2", "expected": "4"}, {"input": "7 3\n4 5 6 7 0 1 2", "expected": "-1"}],
        "hidden_test_cases": [{"input": "1 1\n1", "expected": "0"}, {"input": "2 1\n1 2", "expected": "0"}, {"input": "2 2\n1 2", "expected": "1"}],
        "solution": {"approach": "Modified binary search: identify which half is sorted.", "code": "def search(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target: return mid\n        if nums[lo] <= nums[mid]:\n            if nums[lo] <= target < nums[mid]: hi = mid - 1\n            else: lo = mid + 1\n        else:\n            if nums[mid] < target <= nums[hi]: lo = mid + 1\n            else: hi = mid - 1\n    return -1", "time_complexity": "O(log n)", "space_complexity": "O(1)"},
        "hints": ["One half is always sorted.", "Check which half is sorted, then search there."],
        "topics": ["Binary Search"], "companies": ["Amazon", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BS-03", "topic": "Binary Search", "topic_order": 1, "problem_order": 27,
        "question_title": "Find Peak Element",
        "statement": "Find a peak element (greater than neighbors) in an array.",
        "examples": [{"input": "nums = [1,2,3,1]", "output": "2"}, {"input": "nums = [1,2,1,3,5,6,4]", "output": "5"}],
        "constraints": ["1 <= nums.length <= 1000", "-2^31 <= nums[i] <= 2^31 - 1"],
        "visible_test_cases": [{"input": "4\n1 2 3 1", "expected": "2"}, {"input": "7\n1 2 1 3 5 6 4", "expected": "5"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "0"}, {"input": "2\n1 2", "expected": "1"}, {"input": "2\n2 1", "expected": "0"}],
        "solution": {"approach": "Binary search: move towards the larger neighbor.", "code": "def findPeakElement(nums):\n    lo, hi = 0, len(nums) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < nums[mid + 1]:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo", "time_complexity": "O(log n)", "space_complexity": "O(1)"},
        "hints": ["If nums[mid] < nums[mid+1], peak is on right.", "Otherwise, peak is on left or at mid."],
        "topics": ["Binary Search"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BS-04", "topic": "Binary Search", "topic_order": 1, "problem_order": 28,
        "question_title": "Find First and Last Position",
        "statement": "Find first and last position of target in sorted array.",
        "examples": [{"input": "nums = [5,7,7,8,8,10], target = 8", "output": "[3,4]"}],
        "constraints": ["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "visible_test_cases": [{"input": "6 8\n5 7 7 8 8 10", "expected": "3 4"}, {"input": "6 6\n5 7 7 8 8 10", "expected": "-1 -1"}],
        "hidden_test_cases": [{"input": "1 1\n1", "expected": "0 0"}, {"input": "3 1\n1 2 3", "expected": "0 0"}],
        "solution": {"approach": "Two binary searches: one for first, one for last.", "code": "def searchRange(nums, target):\n    def findFirst():\n        lo, hi, res = 0, len(nums)-1, -1\n        while lo <= hi:\n            mid = (lo+hi)//2\n            if nums[mid] == target: res = mid; hi = mid-1\n            elif nums[mid] < target: lo = mid+1\n            else: hi = mid-1\n        return res\n    def findLast():\n        lo, hi, res = 0, len(nums)-1, -1\n        while lo <= hi:\n            mid = (lo+hi)//2\n            if nums[mid] == target: res = mid; lo = mid+1\n            elif nums[mid] < target: lo = mid+1\n            else: hi = mid-1\n        return res\n    return [findFirst(), findLast()]", "time_complexity": "O(log n)", "space_complexity": "O(1)"},
        "hints": ["First occurrence: when found, keep searching left.", "Last occurrence: when found, keep searching right."],
        "topics": ["Binary Search"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BS-05", "topic": "Binary Search", "topic_order": 1, "problem_order": 29,
        "question_title": "Search in 2D Matrix",
        "statement": "Search for a target in a row-sorted and column-sorted matrix.",
        "examples": [{"input": "matrix = [[1,3,5],[7,10,11],[12,15,16]], target = 3", "output": "true"}],
        "constraints": ["m, n <= 300", "-10^9 <= matrix[i][j] <= 10^9"],
        "visible_test_cases": [{"input": "3 3\n1 3 5\n7 10 11\n12 15 16\n3", "expected": "true"}, {"input": "3 3\n1 3 5\n7 10 11\n12 15 16\n13", "expected": "false"}],
        "hidden_test_cases": [{"input": "1 1\n1\n1", "expected": "true"}, {"input": "2 2\n1 2\n3 4\n5", "expected": "false"}],
        "solution": {"approach": "Start from top-right corner, eliminate row or column.", "code": "def searchMatrix(matrix, target):\n    if not matrix: return False\n    row, col = 0, len(matrix[0]) - 1\n    while row < len(matrix) and col >= 0:\n        if matrix[row][col] == target: return True\n        elif matrix[row][col] > target: col -= 1\n        else: row += 1\n    return False", "time_complexity": "O(m+n)", "space_complexity": "O(1)"},
        "hints": ["Start from top-right corner.", "If current > target, move left.", "If current < target, move down."],
        "topics": ["Binary Search", "Matrix"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # STRINGS (topic_order=2)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "STR-01", "topic": "Strings", "topic_order": 2, "problem_order": 35,
        "question_title": "Reverse Words in a String",
        "statement": "Reverse the order of words in a string.",
        "examples": [{"input": "s = 'the sky is blue'", "output": "blue is sky the"}, {"input": "s = '  hello world  '", "output": "world hello"}],
        "constraints": ["1 <= s.length <= 10^4", "s contains English letters and digits"],
        "visible_test_cases": [{"input": "the sky is blue", "expected": "blue is sky the"}, {"input": "  hello world  ", "expected": "world hello"}],
        "hidden_test_cases": [{"input": "a", "expected": "a"}, {"input": "  good   example  ", "expected": "example good"}],
        "solution": {"approach": "Split by spaces, reverse the list, join.", "code": "def reverseWords(s):\n    return ' '.join(s.split()[::-1])", "time_complexity": "O(n)", "space_complexity": "O(n)"},
        "hints": ["Split the string by spaces.", "Reverse the resulting list.", "Join with single spaces."],
        "topics": ["String"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "STR-02", "topic": "Strings", "topic_order": 2, "problem_order": 36,
        "question_title": "Longest Palindromic Substring",
        "statement": "Find the longest palindromic substring.",
        "examples": [{"input": "s = 'babad'", "output": "bab"}, {"input": "s = 'cbbd'", "output": "bb"}],
        "constraints": ["1 <= s.length <= 1000"],
        "visible_test_cases": [{"input": "babad", "expected": "bab"}, {"input": "cbbd", "expected": "bb"}],
        "hidden_test_cases": [{"input": "a", "expected": "a"}, {"input": "ac", "expected": "a"}, {"input": "racecar", "expected": "racecar"}],
        "solution": {"approach": "Expand around center for each possible center.", "code": "def longestPalindrome(s):\n    def expand(l, r):\n        while l >= 0 and r < len(s) and s[l] == s[r]:\n            l -= 1; r += 1\n        return s[l+1:r]\n    result = ''\n    for i in range(len(s)):\n        odd = expand(i, i)\n        even = expand(i, i+1)\n        result = max(result, odd, even, key=len)\n    return result", "time_complexity": "O(n^2)", "space_complexity": "O(1)"},
        "hints": ["Each character can be center of odd-length palindrome.", "Each gap between characters can be center of even-length."],
        "topics": ["String", "Dynamic Programming"], "companies": ["Amazon", "Microsoft", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "STR-03", "topic": "Strings", "topic_order": 2, "problem_order": 37,
        "question_title": "Anagram Check",
        "statement": "Check if two strings are anagrams of each other.",
        "examples": [{"input": "s = 'anagram', t = 'nagaram'", "output": "true"}, {"input": "s = 'rat', t = 'car'", "output": "false"}],
        "constraints": ["1 <= s.length, t.length <= 5 * 10^4"],
        "visible_test_cases": [{"input": "anagram\nnagaram", "expected": "true"}, {"input": "rat\ncar", "expected": "false"}],
        "hidden_test_cases": [{"input": "a\na", "expected": "true"}, {"input": "ab\na", "expected": "false"}],
        "solution": {"approach": "Sort both strings and compare.", "code": "def isAnagram(s, t):\n    return sorted(s) == sorted(t)", "time_complexity": "O(n log n)", "space_complexity": "O(n)"},
        "hints": ["Sort both strings.", "If sorted versions are equal, they're anagrams."],
        "topics": ["String", "Hash Table"], "companies": ["Amazon", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "STR-04", "topic": "Strings", "topic_order": 2, "problem_order": 38,
        "question_title": "Roman to Integer",
        "statement": "Convert a Roman numeral to an integer.",
        "examples": [{"input": "s = 'III'", "output": "3"}, {"input": "s = 'LVIII'", "output": "58"}, {"input": "s = 'MCMXCIV'", "output": "1994"}],
        "constraints": ["1 <= s.length <= 15"],
        "visible_test_cases": [{"input": "III", "expected": "3"}, {"input": "LVIII", "expected": "58"}],
        "hidden_test_cases": [{"input": "IV", "expected": "4"}, {"input": "IX", "expected": "9"}, {"input": "MCMXCIV", "expected": "1994"}],
        "solution": {"approach": "Map values, subtract when smaller before larger.", "code": "def romanToInt(s):\n    values = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}\n    result = 0\n    for i in range(len(s)):\n        if i+1 < len(s) and values[s[i]] < values[s[i+1]]:\n            result -= values[s[i]]\n        else:\n            result += values[s[i]]\n    return result", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["Map Roman symbols to values.", "If current < next, subtract current."],
        "topics": ["String", "Math"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # RECURSION (topic_order=3)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "REC-01", "topic": "Recursion", "topic_order": 3, "problem_order": 45,
        "question_title": "Power Set",
        "statement": "Generate all subsets (power set) of a given set.",
        "examples": [{"input": "nums = [1,2,3]", "output": "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]"}],
        "constraints": ["1 <= nums.length <= 10", "-10 <= nums[i] <= 10"],
        "visible_test_cases": [{"input": "3\n1 2 3", "expected": "1 2 3\n1 2\n1 3\n1\n2 3\n2\n3\n"}, {"input": "1\n1", "expected": "1\n"}],
        "hidden_test_cases": [{"input": "2\n1 2", "expected": "1 2\n1\n2\n"}],
        "solution": {"approach": "Recursion: include or exclude each element.", "code": "def subsets(nums):\n    result = []\n    def backtrack(start, path):\n        result.append(path[:])\n        for i in range(start, len(nums)):\n            path.append(nums[i])\n            backtrack(i+1, path)\n            path.pop()\n    backtrack(0, [])\n    return result", "time_complexity": "O(2^n)", "space_complexity": "O(n)"},
        "hints": ["For each element, decide to include or exclude.", "Use backtracking to generate all combinations."],
        "topics": ["Recursion", "Backtracking"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "REC-02", "topic": "Recursion", "topic_order": 3, "problem_order": 46,
        "question_title": "Combination Sum",
        "statement": "Find all unique combinations that sum to a target (elements can be reused).",
        "examples": [{"input": "candidates = [2,3,6,7], target = 7", "output": "[[2,2,3],[7]]"}],
        "constraints": ["1 <= candidates.length <= 30", "2 <= candidates[i] <= 40"],
        "visible_test_cases": [{"input": "4 7\n2 3 6 7", "expected": "2 2 3\n7"}, {"input": "3 8\n2 3 5", "expected": "2 2 2 2\n2 3 3\n3 5"}],
        "hidden_test_cases": [{"input": "1 1\n1", "expected": "1"}, {"input": "2 1\n2 3", "expected": ""}],
        "solution": {"approach": "Backtracking: try each candidate, allow reuse.", "code": "def combinationSum(candidates, target):\n    result = []\n    def backtrack(start, path, remaining):\n        if remaining == 0:\n            result.append(path[:])\n            return\n        for i in range(start, len(candidates)):\n            if candidates[i] <= remaining:\n                path.append(candidates[i])\n                backtrack(i, path, remaining - candidates[i])\n                path.pop()\n    backtrack(0, [], target)\n    return result", "time_complexity": "O(n^(T/min))", "space_complexity": "O(T/min)"},
        "hints": ["Sort candidates to enable pruning.", "Allow reusing same element by passing i (not i+1)."],
        "topics": ["Recursion", "Backtracking"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "REC-03", "topic": "Recursion", "topic_order": 3, "problem_order": 47,
        "question_title": "Subset Sum II",
        "statement": "Generate all unique subsets (no duplicates).",
        "examples": [{"input": "nums = [1,2,2]", "output": "[[],[1],[1,2],[1,2,2],[2],[2,2]]"}],
        "constraints": ["1 <= nums.length <= 10", "-10 <= nums[i] <= 10"],
        "visible_test_cases": [{"input": "3\n1 2 2", "expected": "1 2 2\n1 2\n1\n2 2\n2\n"}],
        "hidden_test_cases": [{"input": "2\n1 1", "expected": "1 1\n1\n"}],
        "solution": {"approach": "Sort, skip duplicates at same level.", "code": "def subsetsWithDup(nums):\n    nums.sort()\n    result = []\n    def backtrack(start, path):\n        result.append(path[:])\n        for i in range(start, len(nums)):\n            if i > start and nums[i] == nums[i-1]: continue\n            path.append(nums[i])\n            backtrack(i+1, path)\n            path.pop()\n    backtrack(0, [])\n    return result", "time_complexity": "O(2^n)", "space_complexity": "O(n)"},
        "hints": ["Sort array first.", "Skip duplicate elements at the same recursion level."],
        "topics": ["Recursion", "Backtracking"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # BIT MANIPULATION (topic_order=4)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "BIT-01", "topic": "Bit Manipulation", "topic_order": 4, "problem_order": 55,
        "question_title": "Single Number",
        "statement": "Find the element that appears once (all others appear twice).",
        "examples": [{"input": "nums = [2,2,1]", "output": "1"}, {"input": "nums = [4,1,2,1,2]", "output": "4"}],
        "constraints": ["1 <= nums.length <= 3 * 10^4"],
        "visible_test_cases": [{"input": "3\n2 2 1", "expected": "1"}, {"input": "5\n4 1 2 1 2", "expected": "4"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "3\n1 1 2", "expected": "2"}],
        "solution": {"approach": "XOR all numbers. a^a=0, a^0=a.", "code": "def singleNumber(nums):\n    result = 0\n    for num in nums:\n        result ^= num\n    return result", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["XOR of same numbers is 0.", "XOR of all gives the unique number."],
        "topics": ["Bit Manipulation"], "companies": ["Amazon", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BIT-02", "topic": "Bit Manipulation", "topic_order": 4, "problem_order": 56,
        "question_title": "Count Set Bits",
        "statement": "Count the number of 1-bits (set bits) in an integer.",
        "examples": [{"input": "n = 11", "output": "3"}, {"input": "n = 128", "output": "1"}],
        "constraints": ["0 <= n <= 2^31 - 1"],
        "visible_test_cases": [{"input": "11", "expected": "3"}, {"input": "128", "expected": "1"}],
        "hidden_test_cases": [{"input": "0", "expected": "0"}, {"input": "1", "expected": "1"}, {"input": "7", "expected": "3"}],
        "solution": {"approach": "Brian Kernighan's algorithm: n & (n-1) clears lowest set bit.", "code": "def countBits(n):\n    count = 0\n    while n:\n        n &= n - 1\n        count += 1\n    return count", "time_complexity": "O(number of set bits)", "space_complexity": "O(1)"},
        "hints": ["n & (n-1) removes the lowest set bit.", "Count how many times you can do this."],
        "topics": ["Bit Manipulation"], "companies": ["Amazon", "Microsoft"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BIT-03", "topic": "Bit Manipulation", "topic_order": 4, "problem_order": 57,
        "question_title": "Power of Two",
        "statement": "Check if a number is a power of two.",
        "examples": [{"input": "n = 16", "output": "true"}, {"input": "n = 3", "output": "false"}],
        "constraints": ["-2^31 <= n <= 2^31 - 1"],
        "visible_test_cases": [{"input": "16", "expected": "true"}, {"input": "3", "expected": "false"}],
        "hidden_test_cases": [{"input": "1", "output": "true"}, {"input": "0", "expected": "false"}, {"input": "2147483647", "expected": "false"}],
        "solution": {"approach": "n & (n-1) == 0 for powers of two.", "code": "def isPowerOfTwo(n):\n    return n > 0 and (n & (n - 1)) == 0", "time_complexity": "O(1)", "space_complexity": "O(1)"},
        "hints": ["Power of two has exactly one set bit.", "n & (n-1) removes that bit."],
        "topics": ["Bit Manipulation", "Math"], "companies": ["Amazon", "Google"],
        "difficulty": "easy", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # HEAPS (topic_order=5)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "HP-01", "topic": "Heaps", "topic_order": 5, "problem_order": 65,
        "question_title": "Kth Largest Element",
        "statement": "Find the kth largest element in an unsorted array.",
        "examples": [{"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5"}, {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4"}],
        "constraints": ["1 <= k <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [{"input": "6 2\n3 2 1 5 6 4", "expected": "5"}, {"input": "9 4\n3 2 3 1 2 4 5 5 6", "expected": "4"}],
        "hidden_test_cases": [{"input": "1 1\n1", "expected": "1"}, {"input": "2 1\n2 1", "expected": "2"}],
        "solution": {"approach": "Use min-heap of size k.", "code": "import heapq\ndef findKthLargest(nums, k):\n    heap = nums[:k]\n    heapq.heapify(heap)\n    for num in nums[k:]:\n        if num > heap[0]:\n            heapq.heapreplace(heap, num)\n    return heap[0]", "time_complexity": "O(n log k)", "space_complexity": "O(k)"},
        "hints": ["Maintain a min-heap of size k.", "For each element, if larger than heap min, replace."],
        "topics": ["Heap", "Sorting"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "HP-02", "topic": "Heaps", "topic_order": 5, "problem_order": 66,
        "question_title": "Top K Frequent Elements",
        "statement": "Find the k most frequent elements.",
        "examples": [{"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]"}],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "visible_test_cases": [{"input": "6 2\n1 1 1 2 2 3", "expected": "1 2"}, {"input": "1 1\n1", "expected": "1"}],
        "hidden_test_cases": [{"input": "3 1\n1 1 1", "expected": "1"}, {"input": "4 2\n1 2 2 3", "expected": "2 1"}],
        "solution": {"approach": "Count frequencies, use min-heap of size k.", "code": "from collections import Counter\nimport heapq\ndef topKFrequent(nums, k):\n    count = Counter(nums)\n    return [x for x, _ in heapq.nlargest(k, count.items(), key=lambda x: x[1])]", "time_complexity": "O(n log k)", "space_complexity": "O(n)"},
        "hints": ["Count frequency of each element.", "Use heap to get top k by frequency."],
        "topics": ["Heap", "Hash Table"], "companies": ["Amazon", "Google", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "HP-03", "topic": "Heaps", "topic_order": 5, "problem_order": 67,
        "question_title": "Merge K Sorted Arrays",
        "statement": "Merge k sorted arrays into one sorted array.",
        "examples": [{"input": "arrays = [[1,3],[2,4],[5,6]]", "output": "[1,2,3,4,5,6]"}],
        "constraints": ["1 <= k <= 100", "0 <= arrays[i].length <= 100"],
        "visible_test_cases": [{"input": "3\n2\n1 3\n2\n2 4\n2\n5 6", "expected": "1 2 3 4 5 6"}, {"input": "1\n3\n1 2 3", "expected": "1 2 3"}],
        "hidden_test_cases": [{"input": "0", "expected": ""}, {"input": "2\n1\n1\n1\n2", "expected": "1 2"}],
        "solution": {"approach": "Use min-heap with (value, array_index, element_index).", "code": "import heapq\ndef mergeKArrays(arrays):\n    heap = []\n    result = []\n    for i, arr in enumerate(arrays):\n        if arr:\n            heapq.heappush(heap, (arr[0], i, 0))\n    while heap:\n        val, arr_i, elem_i = heapq.heappop(heap)\n        result.append(val)\n        if elem_i + 1 < len(arrays[arr_i]):\n            heapq.heappush(heap, (arrays[arr_i][elem_i+1], arr_i, elem_i+1))\n    return result", "time_complexity": "O(N log k)", "space_complexity": "O(k)"},
        "hints": ["Push first element of each array to heap.", "Pop smallest, push next from same array."],
        "topics": ["Heap", "Merge Sort"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDING WINDOW & TWO POINTER (topic_order=5.5)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "SW-01", "topic": "Sliding Window", "topic_order": 5, "problem_order": 70,
        "question_title": "Longest Substring Without Repeating Characters",
        "statement": "Find the length of the longest substring without repeating characters.",
        "examples": [{"input": "s = 'abcabcbb'", "output": "3"}, {"input": "s = 'bbbbb'", "output": "1"}],
        "constraints": ["0 <= s.length <= 5 * 10^4"],
        "visible_test_cases": [{"input": "abcabcbb", "expected": "3"}, {"input": "bbbbb", "expected": "1"}],
        "hidden_test_cases": [{"input": "", "expected": "0"}, {"input": "pwwkew", "expected": "3"}, {"input": "au", "expected": "2"}],
        "solution": {"approach": "Sliding window with hash set.", "code": "def lengthOfLongestSubstring(s):\n    char_set = set()\n    left = 0\n    max_len = 0\n    for right in range(len(s)):\n        while s[right] in char_set:\n            char_set.remove(s[left])\n            left += 1\n        char_set.add(s[right])\n        max_len = max(max_len, right - left + 1)\n    return max_len", "time_complexity": "O(n)", "space_complexity": "O(min(n, alphabet))"},
        "hints": ["Use a sliding window with two pointers.", "Expand right, shrink left when duplicate found."],
        "topics": ["Sliding Window", "Hash Table"], "companies": ["Amazon", "Google", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "SW-02", "topic": "Sliding Window", "topic_order": 5, "problem_order": 71,
        "question_title": "Minimum Window Substring",
        "statement": "Find the minimum window in s that contains all characters of t.",
        "examples": [{"input": "s = 'ADOBECODEBANC', t = 'ABC'", "output": "BANC"}],
        "constraints": ["m, n <= 10^5", "s and t consist of English letters"],
        "visible_test_cases": [{"input": "ADOBECODEBANC\nABC", "expected": "BANC"}, {"input": "a\na", "expected": "a"}],
        "hidden_test_cases": [{"input": "a\naa", "expected": ""}, {"input": "ab\nb", "expected": "b"}],
        "solution": {"approach": "Sliding window with character count map.", "code": "from collections import Counter\ndef minWindow(s, t):\n    if not t or not s: return ''\n    need = Counter(t)\n    missing = len(t)\n    start = 0\n    min_start, min_len = 0, float('inf')\n    for end in range(len(s)):\n        if need[s[end]] > 0:\n            missing -= 1\n        need[s[end]] -= 1\n        while missing == 0:\n            if end - start < min_len:\n                min_len = end - start + 1\n                min_start = start\n            need[s[start]] += 1\n            if need[s[start]] > 0:\n                missing += 1\n            start += 1\n    return '' if min_len == float('inf') else s[min_start:min_start+min_len]", "time_complexity": "O(n)", "space_complexity": "O(alphabet)"},
        "hints": ["Count characters in t.", "Expand window until all chars covered.", "Shrink from left to minimize window."],
        "topics": ["Sliding Window", "Hash Table"], "companies": ["Amazon", "Google", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # BINARY SEARCH TREES (topic_order=7)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "BST-01", "topic": "BST", "topic_order": 7, "problem_order": 80,
        "question_title": "Validate Binary Search Tree",
        "statement": "Check if a binary tree is a valid BST.",
        "examples": [{"input": "root = [2,1,3]", "output": "true"}, {"input": "root = [5,1,4,null,null,3,6]", "output": "false"}],
        "constraints": ["1 <= n <= 10^4", "-2^31 <= Node.val <= 2^31 - 1"],
        "visible_test_cases": [{"input": "2 1 3", "expected": "true"}, {"input": "5 1 4 null null 3 6", "expected": "false"}],
        "hidden_test_cases": [{"input": "1 1", "expected": "false"}, {"input": "5 4 6 null null 3 7", "expected": "false"}],
        "solution": {"approach": "DFS with valid range (min, max) for each node.", "code": "def isValidBST(root):\n    def validate(node, min_val, max_val):\n        if not node: return True\n        if node.val <= min_val or node.val >= max_val:\n            return False\n        return validate(node.left, min_val, node.val) and validate(node.right, node.val, max_val)\n    return validate(root, float('-inf'), float('inf'))", "time_complexity": "O(n)", "space_complexity": "O(h)"},
        "hints": ["Each node must be within a valid range.", "Left subtree < node < right subtree."],
        "topics": ["BST", "DFS"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "BST-02", "topic": "BST", "topic_order": 7, "problem_order": 81,
        "question_title": "Kth Smallest in BST",
        "statement": "Find the kth smallest element in a BST.",
        "examples": [{"input": "root = [3,1,4,null,2], k = 1", "output": "1"}],
        "constraints": ["1 <= k <= n <= 10^4"],
        "visible_test_cases": [{"input": "3 1 4 null 2\n1", "expected": "1"}, {"input": "5 3 6 2 4 null null 1\n3", "expected": "3"}],
        "hidden_test_cases": [{"input": "2 1\n2", "expected": "2"}, {"input": "1 null 2\n1", "expected": "1"}],
        "solution": {"approach": "Inorder traversal — kth visit is the answer.", "code": "def kthSmallest(root, k):\n    stack = []\n    curr = root\n    while stack or curr:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        k -= 1\n        if k == 0: return curr.val\n        curr = curr.right", "time_complexity": "O(h + k)", "space_complexity": "O(h)"},
        "hints": ["Inorder traversal gives sorted order.", "Stop when you've visited k nodes."],
        "topics": ["BST", "Stack"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # TRIES (topic_order=8)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "TR-01", "topic": "Tries", "topic_order": 8, "problem_order": 90,
        "question_title": "Implement Trie",
        "statement": "Implement a trie with insert, search, and startsWith.",
        "examples": [{"input": "Trie, insert('apple'), search('apple'), startsWith('app')", "output": "true, true"}],
        "constraints": ["1 <= word.length, prefix.length <= 2000"],
        "visible_test_cases": [{"input": "insert apple\nsearch apple\nsearch app\nstartsWith app\nsearch app", "expected": "true\ntrue\ntrue\nfalse"}],
        "hidden_test_cases": [{"input": "insert a\nsearch a\nstartsWith a\nsearch b", "expected": "true\ntrue\nfalse"}],
        "solution": {"approach": "Each node has children map and end-of-word flag.", "code": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    def insert(self, word):\n        node = self.root\n        for c in word:\n            if c not in node.children:\n                node.children[c] = TrieNode()\n            node = node.children[c]\n        node.is_end = True\n    def search(self, word):\n        node = self.root\n        for c in word:\n            if c not in node.children: return False\n            node = node.children[c]\n        return node.is_end\n    def startsWith(self, prefix):\n        node = self.root\n        for c in prefix:\n            if c not in node.children: return False\n            node = node.children[c]\n        return True", "time_complexity": "O(m)", "space_complexity": "O(m)"},
        "hints": ["Each node stores a map of children.", "Mark end of word for complete words."],
        "topics": ["Trie", "Design"], "companies": ["Amazon", "Google", "Microsoft"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL DP PROBLEMS (topic_order=6)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "DP-16", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 16,
        "question_title": "House Robber II",
        "statement": "House Robber but houses are in a circle (can't rob first and last).",
        "examples": [{"input": "nums = [2,3,2]", "output": "3"}, {"input": "nums = [1,2,3,1]", "output": "4"}],
        "constraints": ["1 <= nums.length <= 100"],
        "visible_test_cases": [{"input": "3\n2 3 2", "expected": "3"}, {"input": "4\n1 2 3 1", "expected": "4"}],
        "hidden_test_cases": [{"input": "1\n1", "expected": "1"}, {"input": "2\n1 2", "expected": "2"}],
        "solution": {"approach": "Run House Robber on [0:n-1] and [1:n], take max.", "code": "def rob(nums):\n    if len(nums) == 1: return nums[0]\n    def robRange(nums):\n        a, b = 0, 0\n        for num in nums:\n            a, b = b, max(b, a + num)\n        return b\n    return max(robRange(nums[:-1]), robRange(nums[1:]))", "time_complexity": "O(n)", "space_complexity": "O(1)"},
        "hints": ["First and last can't both be robbed.", "Run linear robber on two ranges."],
        "topics": ["Dynamic Programming"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-17", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 17,
        "question_title": "Longest Palindromic Subsequence",
        "statement": "Find the length of the longest palindromic subsequence.",
        "examples": [{"input": "s = 'bbbab'", "output": "4"}, {"input": "s = 'cbbd'", "output": "2"}],
        "constraints": ["1 <= s.length <= 1000"],
        "visible_test_cases": [{"input": "bbbab", "expected": "4"}, {"input": "cbbd", "expected": "2"}],
        "hidden_test_cases": [{"input": "a", "expected": "1"}, {"input": "abcba", "expected": "5"}],
        "solution": {"approach": "LCS of string and its reverse.", "code": "def longestPalindromeSubseq(s):\n    t = s[::-1]\n    n = len(s)\n    dp = [[0]*(n+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for j in range(1, n+1):\n            if s[i-1] == t[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[n][n]", "time_complexity": "O(n^2)", "space_complexity": "O(n^2)"},
        "hints": ["LPS = LCS of string and its reverse.", "Use standard LCS algorithm."],
        "topics": ["Dynamic Programming", "String"], "companies": ["Amazon", "Google"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "DP-18", "topic": "Dynamic Programming", "topic_order": 6, "problem_order": 18,
        "question_title": "Minimum Insertions to Make Palindrome",
        "statement": "Find minimum insertions to make string a palindrome.",
        "examples": [{"input": "s = 'abcde'", "output": "4"}, {"input": "s = 'abcba'", "output": "0"}],
        "constraints": ["1 <= s.length <= 500"],
        "visible_test_cases": [{"input": "abcde", "expected": "4"}, {"input": "abcba", "expected": "0"}],
        "hidden_test_cases": [{"input": "a", "expected": "0"}, {"input": "ab", "expected": "1"}],
        "solution": {"approach": "min insertions = n - LPS length.", "code": "def minInsertions(s):\n    n = len(s)\n    t = s[::-1]\n    dp = [[0]*(n+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for j in range(1, n+1):\n            if s[i-1] == t[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return n - dp[n][n]", "time_complexity": "O(n^2)", "space_complexity": "O(n^2)"},
        "hints": ["Find LPS length.", "Insertions = n - LPS."],
        "topics": ["Dynamic Programming", "String"], "companies": ["Amazon"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL GRAPH PROBLEMS (topic_order=5)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "striver_id": "GR-11", "topic": "Graphs", "topic_order": 5, "problem_order": 11,
        "question_title": "Course Schedule (Topological Sort)",
        "statement": "Determine if you can finish all courses given prerequisites (detect cycle in DAG).",
        "examples": [{"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true"}, {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "false"}],
        "constraints": ["1 <= numCourses <= 2000", "0 <= prerequisites.length <= 5000"],
        "visible_test_cases": [{"input": "2\n1 0", "expected": "true"}, {"input": "2\n1 0\n0 1", "expected": "false"}],
        "hidden_test_cases": [{"input": "1", "expected": "true"}, {"input": "3\n1 0\n2 1", "expected": "true"}],
        "solution": {"approach": "Topological sort using Kahn's algorithm.", "code": "from collections import deque\ndef canFinish(numCourses, prerequisites):\n    in_degree = [0] * numCourses\n    graph = [[] for _ in range(numCourses)]\n    for dest, src in prerequisites:\n        graph[src].append(dest)\n        in_degree[dest] += 1\n    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])\n    count = 0\n    while queue:\n        node = queue.popleft()\n        count += 1\n        for neighbor in graph[node]:\n            in_degree[neighbor] -= 1\n            if in_degree[neighbor] == 0:\n                queue.append(neighbor)\n    return count == numCourses", "time_complexity": "O(V + E)", "space_complexity": "O(V + E)"},
        "hints": ["Model as graph: courses are nodes, prerequisites are edges.", "Topological sort succeeds only if no cycle."],
        "topics": ["Graph", "Topological Sort"], "companies": ["Amazon", "Google", "Meta"],
        "difficulty": "medium", "type": "coding", "role": "SDE"
    },
    {
        "striver_id": "GR-12", "topic": "Graphs", "topic_order": 5, "problem_order": 12,
        "question_title": "Word Ladder",
        "statement": "Find the shortest transformation sequence from beginWord to endWord.",
        "examples": [{"input": "beginWord = 'hit', endWord = 'cog', wordList = ['hot','dot','dog','lot','log','cog']", "output": "5"}],
        "constraints": ["1 <= beginWord.length <= 10", "0 <= wordList.length <= 5000"],
        "visible_test_cases": [{"input": "hit\ncog\nhot dot dog lot log cog", "expected": "5"}, {"input": "hit\ncog\ndot dog lot log", "expected": "0"}],
        "hidden_test_cases": [{"input": "a\nc\na b c", "expected": "2"}, {"input": "red\ntax\nred ted tex ted", "expected": "4"}],
        "solution": {"approach": "BFS: each word is a node, differ by one char = edge.", "code": "from collections import deque\ndef ladderLength(beginWord, endWord, wordList):\n    wordSet = set(wordList)\n    if endWord not in wordSet: return 0\n    queue = deque([(beginWord, 1)])\n    visited = {beginWord}\n    while queue:\n        word, length = queue.popleft()\n        for i in range(len(word)):\n            for c in 'abcdefghijklmnopqrstuvwxyz':\n                new_word = word[:i] + c + word[i+1:]\n                if new_word == endWord: return length + 1\n                if new_word in wordSet and new_word not in visited:\n                    visited.add(new_word)\n                    queue.append((new_word, length + 1))\n    return 0", "time_complexity": "O(M^2 * N)", "space_complexity": "O(M^2 * N)"},
        "hints": ["BFS finds shortest path.", "Generate all one-character variations."],
        "topics": ["Graph", "BFS"], "companies": ["Amazon", "Google", "Meta"],
        "difficulty": "hard", "type": "coding", "role": "SDE"
    },
]
