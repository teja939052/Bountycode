"""LeetCode metadata overlay — Part 5: Graphs."""

LEETCODE_META = {
    "nc-number-of-islands": {
        "leetcode_number": 200,
        "statement": "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.\n\nAn island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.",
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 300",
            "grid[i][j] is '0' or '1'.",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "Four isolated/connected groups of 1s form 1 island each.",
            1: "A single island of 1s.",
        },
    },
    "nc-clone-graph": {
        "leetcode_number": 133,
        "statement": "Given a reference of a node in a connected undirected graph.\n\nReturn a deep copy (clone) of the graph.\n\nEach node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors.\n\nTest case format:\n\nFor simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with `val == 1`, the second node with `val == 2`, and so on. The graph is represented in the test case using an adjacency list.\n\nReturn the node whose value is 1 in the cloned graph.",
        "constraints": [
            "The number of nodes in the graph is in the range [0, 100].",
            "1 <= Node.val <= 100",
            "Node.val is unique for each node.",
            "There are no repeated edges and no self-loops in the graph.",
            "The Graph is connected and all nodes can be visited starting from the given node.",
        ],
        "expected_time_complexity": "O(n + m)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "A deep copy mirrors the adjacency structure without sharing node objects.",
        },
    },
    "nc-pacific-atlantic-water-flow": {
        "leetcode_number": 417,
        "statement": "There is an `m x n` rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.\n\nThe island is partitioned into a grid of square cells. You are given an `m x n` integer matrix `heights` where `heights[r][c]` represents the height above sea level of the cell at coordinate `(r, c)`.\n\nThe island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is **less than or equal to** the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.\n\nReturn a 2D list of grid coordinates `result` where `result[i] = [ri, ci]` denotes that rain water can flow from cell `(ri, ci)` to both the Pacific and Atlantic oceans.",
        "constraints": [
            "m == heights.length",
            "n == heights[r].length",
            "1 <= m, n <= 200",
            "0 <= heights[r][c] <= 10^5",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "The cells [0,4], [1,3], [1,4], [2,2], [3,0], [3,1], [4,0] can drain to both oceans.",
        },
    },
    "nc-surrounded-regions": {
        "leetcode_number": 130,
        "statement": "Given an `m x n` matrix `board` containing `'X'` and `'O'`, capture all regions that are 4-directionally surrounded by `'X'`.\n\nA region is captured by flipping all `'O'`s into `'X'`s in that surrounded region.",
        "constraints": [
            "m == board.length",
            "n == board[i].length",
            "1 <= m, n <= 200",
            "board[i][j] is 'X' or 'O'.",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "The only O-region touching the border (row 3) survives; interior Os become X.",
        },
    },
    "nc-rotting-oranges": {
        "leetcode_number": 994,
        "statement": "You are given an `m x n` grid where each cell can have one of three values:\n\n- `0` representing an empty cell,\n- `1` representing a fresh orange, or\n- `2` representing a rotten orange.\n\nEvery minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.\n\nReturn the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return `-1`.",
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 10",
            "grid[i][j] is 0, 1, or 2.",
        ],
        "expected_time_complexity": "O(m * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "Rotting spreads over 4 minutes to all fresh oranges.",
            1: "The orange at (0,1) is unreachable and never rots -> -1.",
        },
    },
    "nc-course-schedule": {
        "leetcode_number": 207,
        "statement": "There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.\n\n- For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.\n\nReturn `true` if you can finish all courses. Otherwise, return `false`.",
        "constraints": [
            "1 <= numCourses <= 2000",
            "0 <= prerequisites.length <= 5000",
            "prerequisites[i].length == 2",
            "0 <= ai, bi < numCourses",
            "All the pairs prerequisites[i] are unique.",
        ],
        "expected_time_complexity": "O(n + m)",
        "expected_space_complexity": "O(n + m)",
        "example_explanations": {
            0: "Take course 1 then course 0 -> possible.",
            1: "0 requires 1 and 1 requires 0 -> a cycle makes it impossible.",
        },
    },
    "nc-course-schedule-ii": {
        "leetcode_number": 210,
        "statement": "There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.\n\n- For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.\n\nReturn the ordering of courses you should take to finish all courses. If there are many valid answers, return **any** of them. If it is impossible to finish all courses, return an empty array.",
        "constraints": [
            "1 <= numCourses <= 2000",
            "0 <= prerequisites.length <= numCourses * (numCourses - 1)",
            "prerequisites[i].length == 2",
            "0 <= ai, bi < numCourses",
            "All the pairs prerequisites[i] are unique.",
        ],
        "expected_time_complexity": "O(n + m)",
        "expected_space_complexity": "O(n + m)",
        "example_explanations": {
            0: "Take course 0, then 1, then 2, then 3.",
        },
    },
    "nc-graph-valid-tree": {
        "leetcode_number": 261,
        "statement": "You have a graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer `n` and a list of `edges` where `edges[i] = [ai, bi]` indicates that there is an undirected edge between nodes `ai` and `bi` in the graph.\n\nReturn `true` if the edges of the given graph make up a valid tree, and `false` otherwise.",
        "constraints": [
            "1 <= n <= 2000",
            "0 <= edges.length <= 5000",
            "edges[i].length == 2",
            "0 <= ai, bi < n",
            "ai != bi",
            "There are no self-loops.",
        ],
        "expected_time_complexity": "O(n + m)",
        "expected_space_complexity": "O(n + m)",
        "example_explanations": {
            0: "n=5 with 4 edges forming no cycle -> valid tree.",
            1: "n=5 with a cycle (0-1,1-2,2-3,3-1) and a disconnected node 4 -> not a tree.",
        },
    },
    "nc-number-of-connected-components": {
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
    "nc-redundant-connection": {
        "leetcode_number": 684,
        "statement": "In this problem, a tree is an undirected graph that is connected and has no cycles.\n\nYou are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional edge added. The added edge has two different vertices chosen from `1` to `n`, and was not an edge that already existed. The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` indicates that there is an edge between nodes `ai` and `bi` in the graph.\n\nReturn an edge that can be removed so that the resulting graph is a tree of `n` nodes. If there are multiple answers, return the answer that occurs last in the input.",
        "constraints": [
            "n == edges.length",
            "3 <= n <= 1000",
            "edges[i].length == 2",
            "1 <= ai < bi <= edges.length",
            "ai != bi",
            "There are no repeated edges.",
            "The given graph is connected.",
        ],
        "expected_time_complexity": "O(n * alpha(n))",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Removing either [1,2] or [2,3] breaks the cycle; [2,3] is later in the input.",
        },
    },
    "nc-word-ladder": {
        "leetcode_number": 127,
        "statement": "A transformation sequence from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:\n\n- Every adjacent pair of words differs by a single letter.\n- Every `si` for `1 <= i <= k` is in `wordList`. Note that `beginWord` does not need to be in `wordList`.\n- `sk == endWord`.\n\nGiven two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence from `beginWord` to `endWord`, or `0` if no such sequence exists.",
        "constraints": [
            "1 <= beginWord.length <= 10",
            "endWord.length == beginWord.length",
            "1 <= wordList.length <= 5000",
            "wordList[i].length == beginWord.length",
            "beginWord, endWord, and wordList[i] consist of lowercase English letters.",
            "beginWord != endWord",
            "All the words in wordList are unique.",
        ],
        "expected_time_complexity": "O(m^2 * n)",
        "expected_space_complexity": "O(m * n)",
        "example_explanations": {
            0: "Shortest chain is hit -> hot -> dot -> dog -> cog (5 words).",
        },
    },
    "nc-alien-dictionary": {
        "leetcode_number": 269,
        "statement": "There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.\n\nYou are given a list of strings `words` from the alien language's dictionary, where the strings are sorted lexicographically by the rules of this new language.\n\nReturn a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there is no solution, return `\"\"`. If there are multiple solutions, return any of them.",
        "constraints": [
            "1 <= words.length <= 100",
            "1 <= words[i].length <= 100",
            "words[i] consists of only lowercase English letters.",
        ],
        "expected_time_complexity": "O(c)",
        "expected_space_complexity": "O(c)",
        "example_explanations": {
            0: "wrt precedes wrf => t before f; rtt precedes rdd => t before d; rww precedes rdd => w before d; ordering: wertf.",
        },
    },
    "nc-min-cost-connect-points": {
        "leetcode_number": 1584,
        "statement": "You are given an array `points` representing integer coordinates of some points on a 2D-plane, where `points[i] = [xi, yi]`.\n\nThe cost of connecting two points `[xi, yi]` and `[xj, yj]` is the manhattan distance between them: `|xi - xj| + |yi - yj|`.\n\nReturn the minimum cost to connect all points. In other words, you need to connect all points with the minimum possible total edge cost (i.e., the minimum cost of a spanning tree of the graph formed by the points).",
        "constraints": [
            "1 <= points.length <= 1000",
            "-10^6 <= xi, yi <= 10^6",
            "All pairs (xi, yi) are distinct.",
        ],
        "expected_time_complexity": "O(n^2)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Connect (0,0)-(2,2) cost 4, (2,2)-(3,10) cost 9, (3,10)-(5,2) cost 10 -> total 20.",
        },
    },
    "st-network-delay": {
        "leetcode_number": 743,
        "statement": "You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = (ui, vi, wi)`, where `ui` is the source node, `vi` is the target node, and `wi` is the time it takes for a signal to travel from source to target.\n\nWe will send a signal from a given node `k`. Return the minimum time it takes for all the `n` nodes to receive the signal. If it is impossible for all the `n` nodes to receive the signal, return `-1`.",
        "constraints": [
            "1 <= k <= n <= 100",
            "1 <= times.length <= 6000",
            "times[i].length == 3",
            "1 <= ui, vi <= n",
            "ui != vi",
            "0 <= wi <= 100",
            "All the pairs (ui, vi) are unique. (i.e., no multiple edges.)",
        ],
        "expected_time_complexity": "O((n + e) log n)",
        "expected_space_complexity": "O(n + e)",
        "example_explanations": {
            0: "From node 2, times to 1,3,4 are 2,1,1; node 3 is reached last at time 2.",
        },
    },
    "st-account-merge": {
        "leetcode_number": 721,
        "statement": "Given a list of `accounts` where each element `accounts[i]` is a list of strings, where the first element `accounts[i][0]` is a name, and the rest of the elements are emails representing emails of the account.\n\nNow, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.\n\nAfter merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails **in sorted order**. The accounts themselves can be returned in any order.",
        "constraints": [
            "1 <= accounts.length <= 1000",
            "2 <= accounts[i].length <= 10",
            "1 <= accounts[i][j].length <= 30",
            "accounts[i][0] consists of English letters.",
            "accounts[i][j] (for j > 0) is a valid email.",
        ],
        "expected_time_complexity": "O(n * e * alpha(n))",
        "expected_space_complexity": "O(n * e)",
        "example_explanations": {
            0: "Emails 'johnsmith@mail.com' merge the first and third accounts; 'john00@mail.com' stays separate.",
        },
    },
}
