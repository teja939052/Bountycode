"""LeetCode metadata overlay — Part 7: 2-D DP, Backtracking, Bit Manipulation."""

LEETCODE_META = {
    "nc-unique-paths": {
        "leetcode_number": 62,
        "statement": "There is a robot on an `m x n` grid. The robot is initially located at the top-left corner (i.e., `grid[0][0]`). The robot tries to move to the bottom-right corner (i.e., `grid[m - 1][n - 1]`). The robot can only move either down or right at any point in time.\n\nGiven the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.\n\nThe test cases are generated so that the answer will be less than or equal to `2 * 10^9`.",
        "constraints": [
            "1 <= m, n <= 100",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "Every path uses exactly 2 downs and 2 rights -> C(4,2) = 6 paths.",
        },
    },
    "nc-longest-common-subsequence": {
        "leetcode_number": 1143,
        "statement": "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.\n\nA subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.\n\n- For example, `\"ace\"` is a subsequence of `\"abcde\"`.\n\nA common subsequence of two strings is a subsequence that is common to both strings.",
        "constraints": [
            "1 <= text1.length, text2.length <= 1000",
            "text1 and text2 consist of only lowercase English characters.",
        ],
        "expected_time_complexity": "O(n * m)",
        "expected_space_complexity": "O(n * m)",
        "example_explanations": {
            0: "\"ace\" is the longest common subsequence, length 3.",
        },
    },
    "nc-best-time-buy-sell-stock": {
        "leetcode_number": 121,
        "statement": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\nYou want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.",
        "constraints": [
            "1 <= prices.length <= 10^5",
            "0 <= prices[i] <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Buy at 7's day (price 1) and sell at 7 -> profit 5.",
            1: "Prices only decrease -> profit 0.",
        },
    },
    "nc-word-search": {
        "leetcode_number": 79,
        "statement": "Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.\n\nThe word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.",
        "constraints": [
            "m == board.length",
            "n = board[i].length",
            "1 <= m, n <= 6",
            "1 <= word.length <= 15",
            "board and word consists of only lowercase and uppercase English letters.",
        ],
        "expected_time_complexity": "O(m * n * 4^l)",
        "expected_space_complexity": "O(l)",
        "example_explanations": {
            0: "\"ABCCED\" can be traced without reusing cells.",
            1: "No path spells \"ABCB\" without reusing the B at (1,0).",
        },
    },
    "nc-subsets": {
        "leetcode_number": 78,
        "statement": "Given an integer array `nums` of **unique** elements, return all possible subsets (the power set).\n\nThe solution set must not contain duplicate subsets. Return the solution in any order.",
        "constraints": [
            "1 <= nums.length <= 10",
            "-10 <= nums[i] <= 10",
            "All the numbers of nums are unique.",
        ],
        "expected_time_complexity": "O(n * 2^n)",
        "expected_space_complexity": "O(n * 2^n)",
        "example_explanations": {
            0: "All 8 subsets of [1,2,3].",
        },
    },
    "nc-combination-sum": {
        "leetcode_number": 39,
        "statement": "Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the combinations in any order.\n\nThe **same** number may be chosen from `candidates` an **unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.\n\nThe test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.",
        "constraints": [
            "1 <= candidates.length <= 30",
            "2 <= candidates[i] <= 40",
            "All elements of candidates are distinct.",
            "1 <= target <= 40",
        ],
        "expected_time_complexity": "O(2^(t/m) )",
        "expected_space_complexity": "O(t/m)",
        "example_explanations": {
            0: "2+2+3, 7 hit target 7.",
        },
    },
    "nc-combination-sum-ii": {
        "leetcode_number": 40,
        "statement": "Given a collection of candidate numbers (`candidates`) and a target number (`target`), find all unique combinations in `candidates` where the candidate numbers sum to `target`.\n\nEach number in `candidates` may only be used **once** in the combination.\n\nNote: The solution set must not contain duplicate combinations.",
        "constraints": [
            "1 <= candidates.length <= 100",
            "1 <= candidates[i] <= 50",
            "1 <= target <= 30",
        ],
        "expected_time_complexity": "O(2^n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Unique combos summing to 8: [1,1,6], [1,2,5], [1,7], [2,6].",
        },
    },
    "nc-subsets-ii": {
        "leetcode_number": 90,
        "statement": "Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set).\n\nThe solution set must not contain duplicate subsets. Return the solution in any order.",
        "constraints": [
            "1 <= nums.length <= 10",
            "-10 <= nums[i] <= 10",
        ],
        "expected_time_complexity": "O(n * 2^n)",
        "expected_space_complexity": "O(n * 2^n)",
        "example_explanations": {
            0: "Subsets of [1,2,2]; [2] and [1,2] each appear once.",
        },
    },
    "nc-permutations": {
        "leetcode_number": 46,
        "statement": "Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.",
        "constraints": [
            "1 <= nums.length <= 6",
            "-10 <= nums[i] <= 10",
            "All the integers of nums are unique.",
        ],
        "expected_time_complexity": "O(n * n!)",
        "expected_space_complexity": "O(n * n!)",
        "example_explanations": {
            0: "All 6 orderings of [1,2,3].",
        },
    },
    "nc-palindrome-partitioning": {
        "leetcode_number": 131,
        "statement": "Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of `s`.",
        "constraints": [
            "1 <= s.length <= 16",
            "s contains only lowercase English letters.",
        ],
        "expected_time_complexity": "O(2^n)",
        "expected_space_complexity": "O(n * 2^n)",
        "example_explanations": {
            0: "Partitions: [\"a\",\"a\",\"b\"] and [\"aa\",\"b\"].",
        },
    },
    "nc-letter-combinations-phone": {
        "leetcode_number": 17,
        "statement": "Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in **any order**.\n\nA mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.",
        "constraints": [
            "0 <= digits.length <= 4",
            "digits[i] is a digit in the range ['2', '9'].",
        ],
        "expected_time_complexity": "O(4^n * n)",
        "expected_space_complexity": "O(4^n)",
        "example_explanations": {
            0: "2 -> abc, 3 -> def; all 9 combinations.",
        },
    },
    "nc-n-queens": {
        "leetcode_number": 51,
        "statement": "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.\n\nGiven an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in **any order**.\n\nEach solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively.",
        "constraints": [
            "1 <= n <= 9",
        ],
        "expected_time_complexity": "O(n!)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Two distinct arrangements of 4 queens on a 4x4 board.",
            1: "Single queen on a 1x1 board.",
        },
    },
    "nc-number-of-1-bits": {
        "leetcode_number": 191,
        "statement": "Write a function that takes the binary representation of a positive integer and returns the number of set bits it has (also known as the Hamming weight).",
        "constraints": [
            "The input must be a binary string of length 32.",
        ],
        "follow_up": "If this function is called many times, how would you optimize it?",
        "expected_time_complexity": "O(1)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Binary 1011 has three set bits.",
        },
    },
    "nc-counting-bits": {
        "leetcode_number": 338,
        "statement": "Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the **number of `1`'s** in the binary representation of `i`.",
        "constraints": [
            "0 <= n <= 10^5",
        ],
        "follow_up": "It is very easy to come up with a solution with a runtime of O(n log n). Can you do it in linear time O(n) and possibly in a single pass? Can you do it without using any built-in function (i.e., like __builtin_popcount) in C++?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Popcounts of 0..5 are 0,1,1,2,1,2.",
        },
    },
    "nc-reverse-bits": {
        "leetcode_number": 190,
        "statement": "Reverse bits of a given 32 bits unsigned integer.",
        "constraints": [
            "The input must be a binary string of length 32.",
        ],
        "follow_up": "If this function is called many times, how would you optimize it?",
        "expected_time_complexity": "O(1)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "00000010100101000001111010011100 reversed is 00111001011110000010100101000000 (964176192).",
        },
    },
}
