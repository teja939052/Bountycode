"""LeetCode metadata overlay — Part 6: 1-Dimensional DP."""

LEETCODE_META = {
    "nc-climbing-stairs": {
        "leetcode_number": 70,
        "statement": "You are climbing a staircase. It takes `n` steps to reach the top.\n\nEach time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?",
        "constraints": [
            "1 <= n <= 45",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Ways: 1+1, 2.",
            1: "Ways: 1+1+1, 1+2, 2+1.",
        },
    },
    "nc-min-cost-climbing-stairs": {
        "leetcode_number": 746,
        "statement": "You are given an integer array `cost` where `cost[i]` is the cost of `i-th` step on a staircase. Once you pay the cost, you can either climb one or two steps.\n\nYou can either start from the step with index `0`, or the step with index `1`.\n\nReturn the minimum cost to reach the top of the floor.",
        "constraints": [
            "2 <= cost.length <= 1000",
            "0 <= cost[i] <= 999",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Start at index 0: pay 10, go to 15, pay 15, finish -> 25 (vs 15+20=35).",
        },
    },
    "nc-house-robber": {
        "leetcode_number": 198,
        "statement": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and **it will automatically contact the police if two adjacent houses were broken into on the same night**.\n\nGiven an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight **without alerting the police**.",
        "constraints": [
            "1 <= nums.length <= 100",
            "0 <= nums[i] <= 400",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Rob houses 1 (1) and 3 (3) -> 4.",
            1: "Rob houses 1 (2), 3 (9), and 5 (1) -> 12.",
        },
    },
    "nc-house-robber-ii": {
        "leetcode_number": 213,
        "statement": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and **it will automatically contact the police if two adjacent houses were broken into on the same night**.\n\nGiven an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight **without alerting the police**.",
        "constraints": [
            "1 <= nums.length <= 100",
            "0 <= nums[i] <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Rob house 1 (2), house 3 (9), and house 4 (1) -> 12 (never rob the adjacent first+last).",
        },
    },
    "nc-longest-palindromic-substring": {
        "leetcode_number": 5,
        "statement": "Given a string `s`, return the longest palindromic substring in `s`.",
        "constraints": [
            "1 <= s.length <= 1000",
            "s consist of only digits and English letters.",
        ],
        "expected_time_complexity": "O(n^2)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "\"bab\" is a palindrome of length 3.",
            1: "\"bb\" is a palindrome; the whole string is not.",
        },
    },
    "nc-palindromic-substrings": {
        "leetcode_number": 647,
        "statement": "Given a string `s`, return the number of palindromic substrings in it.\n\nA string is a palindrome when it reads the same backward as forward.\n\nA substring is a contiguous sequence of characters within the string.",
        "constraints": [
            "1 <= s.length <= 1000",
            "s consists of lowercase English letters.",
        ],
        "expected_time_complexity": "O(n^2)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Palindromic substrings: \"a\",\"b\",\"c\",\"aa\",\"aaa\" -> 6.",
        },
    },
    "nc-decode-ways": {
        "leetcode_number": 91,
        "statement": "A message containing letters from `A-Z` can be **encoded** into numbers using the following mapping:\n\n`'A' -> \"1\"`, `'B' -> \"2\"`, ..., `'Z' -> \"26\"`\n\nTo decode an encoded message, all the digits must be grouped then mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, `\"11106\"` can be mapped into:\n\n- `\"AAJF\"` with the grouping `(1 1 10 6)`\n- `\"KJF\"` with the grouping `(11 10 6)`\n\nNote that the grouping `(1 11 06)` is invalid because `\"06\"` cannot be mapped into `'F'` since `\"6\"` is different from `\"06\"`.\n\nGiven a string `s` containing only digits, return the **number** of ways to decode it.\n\nThe test cases are generated so that the answer fits in a 32-bit integer.",
        "constraints": [
            "1 <= s.length <= 100",
            "s contains only digits and may contain leading zero(s).",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "\"12\" decodes as \"AB\" (1 2) or \"L\" (12) -> 2.",
            1: "Leading zero cannot stand alone -> 0 ways.",
        },
    },
    "nc-coin-change": {
        "leetcode_number": 322,
        "statement": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.\n\nYou may assume that you have an infinite number of each kind of coin.",
        "constraints": [
            "1 <= coins.length <= 12",
            "1 <= coins[i] <= 2^31 - 1",
            "0 <= amount <= 10^4",
        ],
        "expected_time_complexity": "O(n * amount)",
        "expected_space_complexity": "O(amount)",
        "example_explanations": {
            0: "11 = 5 + 5 + 1 (3 coins).",
        },
    },
    "nc-maximum-product-subarray": {
        "leetcode_number": 152,
        "statement": "Given an integer array `nums`, find a subarray that has the largest product, and return the product.\n\nThe test cases are generated so that the answer will fit in a 32-bit integer.",
        "constraints": [
            "1 <= nums.length <= 2 * 10^4",
            "-10 <= nums[i] <= 10",
            "The product of any subarray is guaranteed to fit in a 32-bit integer.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The subarray [2,3] gives the max product 6.",
            1: "The subarray [4] has product 4; negatives cancel only with another negative.",
        },
    },
    "nc-word-break": {
        "leetcode_number": 139,
        "statement": "Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.\n\nNote that the same word in the dictionary may be reused multiple times in the segmentation.",
        "constraints": [
            "1 <= s.length <= 300",
            "1 <= wordDict.length <= 1000",
            "1 <= wordDict[i].length <= 20",
            "s and wordDict[i] consist of only lowercase English letters.",
            "All the strings of wordDict are unique.",
        ],
        "expected_time_complexity": "O(n * m)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "\"leetcode\" = \"leet\" + \"code\".",
        },
    },
    "nc-longest-increasing-subsequence": {
        "leetcode_number": 300,
        "statement": "Given an integer array `nums`, return the length of the longest strictly increasing subsequence.",
        "constraints": [
            "1 <= nums.length <= 2500",
            "-10^4 <= nums[i] <= 10^4",
        ],
        "follow_up": "Can you come up with an algorithm that runs in O(n log(n)) time complexity?",
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The LIS [2,3,7,101] has length 4.",
        },
    },
    "nc-partition-equal-subset-sum": {
        "leetcode_number": 416,
        "statement": "Given an integer array `nums`, return `true` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `false` otherwise.",
        "constraints": [
            "1 <= nums.length <= 200",
            "1 <= nums[i] <= 100",
        ],
        "expected_time_complexity": "O(n * sum)",
        "expected_space_complexity": "O(sum)",
        "example_explanations": {
            0: "Sum is 22; split [1,5,5] and [11] both sum to 11.",
        },
    },
}
