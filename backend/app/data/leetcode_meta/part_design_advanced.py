"""LeetCode metadata overlay — Part 8: Design, Advanced DP, Advanced Graphs, Greedy, Bits + remaining st-* slugs."""

LEETCODE_META = {
    "nc-lru-cache": {
        "leetcode_number": 146,
        "statement": "Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.\n\nImplement the `LRUCache` class:\n\n- `LRUCache(int capacity)` Initialize the LRU cache with positive size capacity.\n- `int get(int key)` Return the value of the key if the key exists, otherwise return `-1`.\n- `void put(int key, int value)` Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.\n\nThe functions `get` and `put` must each run in `O(1)` average time complexity.",
        "constraints": [
            "1 <= capacity <= 3000",
            "0 <= key <= 10^4",
            "0 <= value <= 10^5",
            "At most 2 * 10^5 calls will be made to get and put.",
        ],
        "follow_up": "Can you do both operations in O(1) time complexity?",
        "expected_time_complexity": "O(1) per operation",
        "expected_space_complexity": "O(capacity)",
        "example_explanations": {
            0: "get(1) -> 1; get(2) -> -1 (key 2 not present); put(3) evicts key 1 (LRU); get(1) -> -1; get(3) -> 3; get(4) -> 4.",
        },
    },
    "nc-time-based-key-value-store": {
        "leetcode_number": 981,
        "statement": "Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.\n\nImplement the `TimeMap` class:\n\n- `TimeMap()` Initializes the object of the data structure.\n- `void set(String key, String value, int timestamp)` Stores the key with the value at the given time timestamp.\n- `String get(String key, int timestamp)` Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns `\"\"`.",
        "constraints": [
            "1 <= key.length, value.length <= 100",
            "key and value consist of lowercase English letters and digits.",
            "1 <= timestamp <= 10^7",
            "All the timestamps timestamp of set are strictly increasing.",
            "At most 2 * 10^5 calls will be made to set and get.",
        ],
        "expected_time_complexity": "O(log n) per get, O(1) per set",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "set foo=bar@1; get(1)->bar; get(3)->bar (largest ts <= 3 is 1); set foo=bar2@4; get(4)->bar2; get(5)->bar2.",
        },
    },
    "nc-detect-squares": {
        "leetcode_number": 2013,
        "statement": "You are given a stream of points on the X-Y plane. Design an algorithm that:\n\n- **Adds** new points from the stream into a data structure. Duplicate points are allowed and should be treated as different points.\n- Given a query point, **counts** the number of ways to choose three points from the data structure such that the three points and the query point form an axis-aligned square with **positive area**.\n\nAn **axis-aligned square** is a square whose edges are all the same length and are either parallel to the x-axis or y-axis.\n\nImplement the `DetectSquares` class:\n\n- `DetectSquares()` Initializes the object with an empty data structure.\n- `void add(int[] point)` Adds a new point point = [x, y] to the data structure.\n- `int count(int[] point)` Counts the number of ways to form axis-aligned squares with point point = [x, y] as described above.",
        "constraints": [
            "point.length == 2",
            "0 <= x, y <= 1000",
            "At most 3000 calls in total will be made to add and count.",
        ],
        "expected_time_complexity": "O(n) per count, O(1) per add",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "After adding [3,10],[11,2],[3,2], query [11,10] forms exactly one square (side 8).",
        },
    },
    "nc-sum-two-integers": {
        "leetcode_number": 371,
        "statement": "Given two integers `a` and `b`, return the sum of the two integers without using the operators `+` and `-`.",
        "constraints": [
            "-1000 <= a, b <= 1000",
        ],
        "expected_time_complexity": "O(1)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "1 + 2 = 3 using only bitwise operations.",
            1: "2 + 3 = 5.",
        },
    },
    "nc-edit-distance": {
        "leetcode_number": 72,
        "statement": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.\n\nYou have the following three operations permitted on a word:\n\n- Insert a character\n- Delete a character\n- Replace a character",
        "constraints": [
            "0 <= word1.length, word2.length <= 500",
            "word1 and word2 consist of lowercase English letters.",
        ],
        "expected_time_complexity": "O(n * m)",
        "expected_space_complexity": "O(n * m)",
        "example_explanations": {
            0: "horse -> rorse (replace h with r) -> rose (remove r) -> ros (remove e): 3 ops.",
        },
    },
    "nc-interleaving-string": {
        "leetcode_number": 97,
        "statement": "Given strings `s1`, `s2`, and `s3`, find whether `s3` is formed by an interleaving of `s1` and `s2`.\n\nAn interleaving of two strings `s` and `t` is a configuration where `s` and `t` are divided into `n` and `m` substrings respectively, such that:\n\n- `s = s1 + s2 + ... + sn`\n- `t = t1 + t2 + ... + tm`\n- `|n - m| <= 1`\n- The interleaving is `s1 + t1 + s2 + t2 + s3 + t3 + ...` or `t1 + s1 + t2 + s2 + t3 + s3 + ...`\n\nNote: `a + b` is the concatenation of strings `a` and `b`.",
        "constraints": [
            "0 <= s1.length, s2.length <= 100",
            "0 <= s3.length <= 200",
            "s1, s2, and s3 consist of lowercase English letters.",
        ],
        "follow_up": "Could you solve it using only O(s2.length) additional memory space?",
        "expected_time_complexity": "O(n * m)",
        "expected_space_complexity": "O(n * m)",
        "example_explanations": {
            0: "s3 can be formed by interleaving aabcc from aabc and abd.",
        },
    },
    "nc-longest-increasing-path-matrix": {
        "leetcode_number": 329,
        "statement": "Given an `m x n` integers `matrix`, return the length of the longest increasing path in `matrix`.\n\nFrom each cell, you can either move in four directions: left, right, up, or down. You **may not** move diagonally or move outside the boundary (i.e., wrap-around is not allowed).",
        "constraints": [
            "m == matrix.length",
            "n == matrix[i].length",
            "1 <= m, n <= 200",
            "0 <= matrix[i][j] <= 2^31 - 1",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "The longest increasing path is 1 -> 2 -> 6 -> 9 (length 4).",
        },
    },
    "nc-generate-parentheses": {
        "leetcode_number": 22,
        "statement": "Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.",
        "constraints": [
            "1 <= n <= 8",
        ],
        "expected_time_complexity": "O(4^n / sqrt(n))",
        "expected_space_complexity": "O(4^n / sqrt(n))",
        "example_explanations": {
            0: "All three well-formed combinations for n=3.",
        },
    },
    "nc-coin-change-ii": {
        "leetcode_number": 518,
        "statement": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return `0`.\n\nYou may assume that you have an infinite number of each kind of coin.\n\nThe answer is guaranteed to fit into a signed 32-bit integer.",
        "constraints": [
            "1 <= coins.length <= 300",
            "1 <= coins[i] <= 5000",
            "All the values of coins are unique.",
            "0 <= amount <= 5000",
        ],
        "expected_time_complexity": "O(n * amount)",
        "expected_space_complexity": "O(amount)",
        "example_explanations": {
            0: "Ways to make 5 with [1,2,5]: 5, 2+2+1, 2+1+1+1, 1+1+1+1+1 -> 4.",
        },
    },
    "nc-stock-cooldown": {
        "leetcode_number": 309,
        "statement": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\nFind the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:\n\n- After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).",
        "constraints": [
            "1 <= prices.length <= 5000",
            "0 <= prices[i] <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Buy on day 2 (1), sell on day 3 (2), cooldown day 4, buy day 5 (0), sell day 6 (3) -> 3.",
        },
    },
    "nc-stock-fee": {
        "leetcode_number": 714,
        "statement": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day, and an integer `fee` representing a transaction fee.\n\nFind the maximum profit you can achieve. You may complete as many transactions as you like, but you need to pay the transaction fee for each transaction.\n\n**Note:** You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).",
        "constraints": [
            "1 <= prices.length <= 5 * 10^4",
            "0 < prices[i], fee < 5 * 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Buy day 1 (1), sell day 3 (3), fee 2 -> 0; buy day 2 (1), sell day 4 (4), fee 2 -> 1; total profit 8.",
        },
    },
    "nc-target-sum": {
        "leetcode_number": 494,
        "statement": "You are given an integer array `nums` and an integer `target`.\n\nYou want to build an expression out of nums by adding one of the symbols `'+'` and `'-'` before each integer in nums and then concatenate all the integers.\n\n- For example, if `nums = [2, 1]`, you can add a `'+'` before `2` and a `'-'` before `1` and concatenate them to build the expression `\"+2-1\"`.\n\nReturn the number of different expressions that you can build, which evaluates to `target`.",
        "constraints": [
            "1 <= nums.length <= 20",
            "0 <= nums[i] <= 1000",
            "0 <= sum(nums[i]) <= 1000",
            "-1000 <= target <= 1000",
        ],
        "expected_time_complexity": "O(n * sum)",
        "expected_space_complexity": "O(sum)",
        "example_explanations": {
            0: "The 5 sign assignments that sum to 3.",
        },
    },
    "nc-valid-parenthesis-string": {
        "leetcode_number": 678,
        "statement": "Given a string `s` containing only three types of characters: `'('`, `')'` and `'*'`, return `true` if `s` is **valid**.\n\nThe following rules define a **valid** string:\n\n- Any left parenthesis `'('` must have a corresponding right parenthesis `')'`.\n- Any right parenthesis `')'` must have a corresponding left parenthesis `'('`.\n- Left parenthesis `'('` must go before the corresponding right parenthesis `')'`.\n- `'*'` could be treated as a single right parenthesis `')'` or a single left parenthesis `'('` or an empty string `\"\"`.",
        "constraints": [
            "1 <= s.length <= 100",
            "s[i] is '(' , ')' or '*'.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The two '*' can act as '(' and ')' to balance the string.",
        },
    },
    "nc-merge-triplets": {
        "leetcode_number": 1899,
        "statement": "A triplet is an array of three integers. You are given a 2D integer array `triplets`, where `triplets[i] = [ai, bi, ci]` describes the `i-th` triplet. You are also given an integer array `target = [x, y, z]` that describes the triplet you want to obtain.\n\nTo obtain `target`, you may apply the following operation on `triplets` any number of times (possibly zero):\n\n- Choose two indices (0-indexed) `i` and `j` (`i != j`) and update `triplets[j]` to become `[max(ai, aj), max(bi, bj), max(ci, cj)]`.\n\nReturn `true` if it is possible to obtain the `target` triplet as an element of `triplets`, or `false` otherwise.",
        "constraints": [
            "1 <= triplets.length <= 10^5",
            "triplets[i].length == target.length == 3",
            "1 <= ai, bi, ci, x, y, z <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Merge [2,5,3] and [1,8,4] to get [2,8,4] == target.",
        },
    },
    "nc-partition-labels": {
        "leetcode_number": 763,
        "statement": "You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in at most one part.\n\nNote that the partition is done so that after concatenating all the parts in order, the resultant string should be `s`.\n\nReturn a list of integers representing the size of these parts.",
        "constraints": [
            "1 <= s.length <= 500",
            "s consists of lowercase English letters.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The partition is 'ababcbaca' | 'defegde' | 'hijhklij' with sizes 9, 7, 8.",
        },
    },
    "nc-minimum-interval-queries": {
        "leetcode_number": 1851,
        "statement": "You are given a 2D integer array `intervals`, where `intervals[i] = [lefti, righti]` describes the `i-th` interval starting at `lefti` and ending at `righti` (inclusive). The **size** of an interval is defined as the number of integers it contains, or more formally `righti - lefti + 1`.\n\nYou are also given an integer array `queries`. The answer to the `j-th` query is the size of the **smallest interval** `i` such that `lefti <= queries[j] <= righti`. If there is no such interval, return `-1`.\n\nReturn an array containing the answers to the queries.",
        "constraints": [
            "1 <= intervals.length <= 10^5",
            "1 <= queries.length <= 10^5",
            "intervals[i].length == 2",
            "1 <= lefti <= righti <= 10^7",
            "1 <= queries[j] <= 10^7",
        ],
        "expected_time_complexity": "O((n + q) log n)",
        "expected_space_complexity": "O(n + q)",
        "example_explanations": {
            0: "query 2 -> interval [2,3] size 2; query 19 -> interval [17,22] size 6; query 5 -> [2,5] or [4,5] size 2; query 22 -> size 6.",
        },
    },
    "nc-walls-and-gates": {
        "leetcode_number": 286,
        "statement": "You are given an `m x n` grid `rooms` initialized with these three possible values.\n\n- `-1` A wall or an obstacle.\n- `0` A gate.\n- `INF` Infinity means an empty room. We use the value `2^31 - 1 = 2147483647` to represent `INF` as you may assume that the distance to a gate is less than `2147483647`.\n\nFill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled with `INF`.",
        "constraints": [
            "m == rooms.length",
            "n == rooms[i].length",
            "1 <= m, n <= 250",
            "rooms[i][j] is -1, 0, or 2^31 - 1.",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "Each empty cell is filled with the BFS distance to the nearest gate.",
        },
    },
    "nc-reconstruct-itinerary": {
        "leetcode_number": 332,
        "statement": "You are given a list of airline `tickets` where `tickets[i] = [fromi, toi]` represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.\n\nAll of the tickets belong to a man who departs from `\"JFK\"`, thus, the itinerary must begin with `\"JFK\"`. If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string.\n\n- For example, the itinerary `[\"JFK\", \"LGA\"]` has a smaller lexical order than `[\"JFK\", \"LGB\"]`.\n\nYou may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.",
        "constraints": [
            "1 <= tickets.length <= 300",
            "tickets[i].length == 2",
            "fromi.length == 3",
            "toi.length == 3",
            "fromi and toi consist of uppercase English letters.",
            "fromi != toi",
        ],
        "expected_time_complexity": "O(E log E)",
        "expected_space_complexity": "O(E)",
        "example_explanations": {
            0: "JFK -> NRT -> JFK -> KUL (the alternative JFK->KUL visits KUL first but yields no full circuit; smallest lexical valid path chosen).",
        },
    },
    "nc-cheapest-flights-k-stops": {
        "leetcode_number": 787,
        "statement": "There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [fromi, toi, pricei]` indicates that there is a flight from city `fromi` to city `toi` with cost `pricei`.\n\nYou are also given three integers `src`, `dst`, and `k`, return the **cheapest price** from `src` to `dst` with at most `k` stops. If there is no such route, return `-1`.",
        "constraints": [
            "1 <= n <= 100",
            "0 <= flights.length <= (n * (n - 1) / 2)",
            "flights[i].length == 3",
            "0 <= fromi, toi < n",
            "fromi != toi",
            "1 <= pricei <= 10^4",
            "There will not be any multiple flights between two cities.",
            "0 <= src, dst, k < n",
            "src != dst",
        ],
        "expected_time_complexity": "O(k * (n + e))",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The two-leg route 0->1->3 costs 300 + 100 = 400 with exactly 1 stop.",
        },
    },
    "nc-swim-rising-water": {
        "leetcode_number": 778,
        "statement": "You are given an `n x n` integer matrix `grid` where each value `grid[i][j]` represents the elevation at that point `(i, j)`.\n\nThe rain starts to fall. At time `t`, the depth of the water everywhere is `t`. You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most `t`. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.\n\nYou start at the top left square `(0, 0)`. Return the least time until you can reach the bottom right square `(n - 1, n - 1)`.",
        "constraints": [
            "n == grid.length",
            "n == grid[i].length",
            "1 <= n <= 50",
            "0 <= grid[i][j] < n^2",
            "Each value grid[i][j] is unique.",
        ],
        "expected_time_complexity": "O(n^2 log n)",
        "expected_space_complexity": "O(n^2)",
        "example_explanations": {
            0: "The least time to reach (2,2) is 16: swim through 0,1,2,... while water stays <= 16.",
        },
    },
    "st-majority-element": {
        "leetcode_number": 169,
        "statement": "Given an array `nums` of size `n`, return the majority element.\n\nThe majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.",
        "constraints": [
            "n == nums.length",
            "1 <= n <= 5 * 10^4",
            "-10^9 <= nums[i] <= 10^9",
        ],
        "follow_up": "Could you solve the problem in linear time and in O(1) space?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "3 appears more than 3 times -> majority.",
        },
    },
    "st-find-first-last": {
        "leetcode_number": 34,
        "statement": "Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value.\n\nIf `target` is not found in the array, return `[-1, -1]`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "constraints": [
            "0 <= nums.length <= 10^5",
            "-10^9 <= nums[i] <= 10^9",
            "nums is a non-decreasing array.",
            "-10^9 <= target <= 10^9",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The target 8 occupies indices 3..4.",
        },
    },
    "st-number-connected-components": {
        "leetcode_number": 323,
        "statement": "You have a graph of `n` nodes. You are given an integer `n` and an array `edges` where `edges[i] = [ai, bi]` indicates that there is an undirected edge between nodes `ai` and `bi`.\n\nReturn the number of connected components in the graph.",
        "constraints": [
            "1 <= n <= 2000",
            "0 <= edges.length <= 5000",
            "edges[i].length == 2",
            "0 <= ai, bi < n",
            "ai != bi",
            "There are no repeated edges.",
        ],
        "expected_time_complexity": "O(n + m)",
        "expected_space_complexity": "O(n + m)",
        "example_explanations": {
            0: "Edges connect {0,1,2} and {3,4} -> 2 components.",
        },
    },
}
