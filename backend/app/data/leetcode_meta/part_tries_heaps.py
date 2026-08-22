"""LeetCode metadata overlay — Part 4: Tries, Heap / Priority Queue, Intervals."""

LEETCODE_META = {
    "nc-implement-trie": {
        "leetcode_number": 208,
        "statement": "A trie (pronounced as \"try\") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.\n\nImplement the Trie class:\n\n- `Trie()` Initializes the trie object.\n- `void insert(String word)` Inserts the string word into the trie.\n- `boolean search(String word)` Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.\n- `boolean startsWith(String prefix)` Returns true if there is a previously inserted string word that has the prefix, and false otherwise.",
        "constraints": [
            "1 <= word.length, prefix.length <= 2000",
            "word and prefix consist only of lowercase English letters.",
            "At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.",
        ],
        "expected_time_complexity": "O(n) per operation",
        "expected_space_complexity": "O(n * k) total",
        "example_explanations": {
            0: "After insert('apple'), search('apple') is true and startsWith('app') is true.",
        },
    },
    "nc-design-add-search-words": {
        "leetcode_number": 211,
        "statement": "Design a data structure that supports adding new words and finding if a string matches any previously added string.\n\nImplement the `WordDictionary` class:\n\n- `WordDictionary()` Initializes the object.\n- `void addWord(word)` Adds word to the data structure, it can be matched later.\n- `bool search(word)` Returns true if there is any string in the data structure that matches word or false otherwise. word may contain dots `'.'` where dots can be matched with any letter.",
        "constraints": [
            "1 <= word.length <= 25",
            "word in addWord consists of lowercase English letters.",
            "word in search consist of '.' or lowercase English letters.",
            "There will be at most 3 dots in word for search operations.",
            "At most 10^4 calls will be made to addWord and search.",
        ],
        "follow_up": "Could you solve it by applying the Trie data structure? What if the word length is very large and only a few words share prefixes?",
        "expected_time_complexity": "O(n) insert, O(n * 26^d) search worst case",
        "expected_space_complexity": "O(words * n)",
        "example_explanations": {
            0: "addWord('bad') then search('pad') is false, search('.ad') matches 'bad', search('b..') matches 'bad'.",
        },
    },
    "nc-word-search-ii": {
        "leetcode_number": 212,
        "statement": "Given an `m x n` `board` of characters and a list of strings `words`, return all words on the board.\n\nEach word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.",
        "constraints": [
            "m == board.length",
            "n == board[i].length",
            "1 <= m, n <= 12",
            "1 <= words.length <= 3 * 10^4",
            "1 <= words[i].length <= 10",
            "1 <= words[i].length <= 10",
            "words[i] consists of lowercase English letters.",
            "All the strings of words are unique.",
        ],
        "expected_time_complexity": "O(m * n * 4^l) worst case",
        "expected_space_complexity": "O(words * l)",
        "example_explanations": {
            0: "'oath' and 'eat' can be traced on the board; 'oath' cannot (no 'o' then 'a' chain).",
        },
    },
    "nc-kth-largest-stream": {
        "leetcode_number": 703,
        "statement": "Design a class to find the `k-th` largest element in a stream. Note that it is the `k-th` largest element in the sorted order, not the `k-th` distinct element.\n\nImplement `KthLargest` class:\n\n- `KthLargest(int k, int[] nums)` Initializes the object with the integer k and the stream of integers nums.\n- `int add(int val)` Appends the integer val to the stream and returns the element representing the `k-th` largest element in the stream.",
        "constraints": [
            "1 <= k <= 10^4",
            "0 <= nums.length <= 10^4",
            "-10^4 <= nums[i] <= 10^4",
            "-10^4 <= val <= 10^4",
            "At most 10^4 calls will be made to add.",
            "It is guaranteed that there will be at least k elements in the array when you search for the kth element.",
        ],
        "expected_time_complexity": "O(log k) per add",
        "expected_space_complexity": "O(k)",
        "example_explanations": {
            0: "With k=3, adding 3 -> kth largest is 4; adding 5 -> 5; adding 10 -> 5; adding 9 -> 8.",
        },
    },
    "nc-last-stone-weight": {
        "leetcode_number": 1046,
        "statement": "You are given an array of integers `stones` where `stones[i]` is the weight of the `i-th` stone.\n\nWe are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:\n\n- If `x == y`, both stones are destroyed, and\n- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.\n\nAt the end of the game, there is at most one stone left.\n\nReturn the weight of the last remaining stone. If there are no stones left, return `0`.",
        "constraints": [
            "1 <= stones.length <= 30",
            "1 <= stones[i] <= 1000",
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "7 and 8 smash -> 1; then 2 and 4 -> 2; then 1 and 2 -> 1; one stone of weight 1 remains.",
        },
    },
    "nc-k-closest-points-origin": {
        "leetcode_number": 973,
        "statement": "Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.\n\nThe distance between two points on the X-Y plane is the Euclidean distance (i.e., `sqrt((x1 - x2)^2 + (y1 - y2)^2)`).\n\nYou may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).",
        "constraints": [
            "1 <= k <= points.length <= 10^4",
            "-10^4 <= xi, yi <= 10^4",
        ],
        "expected_time_complexity": "O(n log k)",
        "expected_space_complexity": "O(k)",
        "example_explanations": {
            0: "Points at distance 1 are (1,3), (-2,2); the closest two are (1,3) and (-2,2) (either order).",
        },
    },
    "nc-kth-largest-array": {
        "leetcode_number": 215,
        "statement": "Given an integer array `nums` and an integer `k`, return the `k-th` largest element in the array.\n\nNote that it is the `k-th` largest element in the sorted order, not the `k-th` distinct element.\n\nCan you solve it without sorting?",
        "constraints": [
            "1 <= k <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
        ],
        "expected_time_complexity": "O(n log k)",
        "expected_space_complexity": "O(k)",
        "example_explanations": {
            0: "Sorted descending: [6,5,4,3,2,1]; the 2nd largest is 5.",
        },
    },
    "nc-find-median-data-stream": {
        "leetcode_number": 295,
        "statement": "The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.\n\n- For example, for `arr = [2,3,4]`, the median is `3`.\n- For example, for `arr = [2,3]`, the median is `(2 + 3) / 2 = 2.5`.\n\nImplement the MedianFinder class:\n\n- `MedianFinder()` initializes the MedianFinder object.\n- `void addNum(int num)` adds the integer num from the data stream to the data structure.\n- `double findMedian()` returns the median of all elements so far. Answers within `10^-5` of the actual answer will be accepted.",
        "constraints": [
            "-10^5 <= num <= 10^5",
            "There will be at least one element in the data structure before calling findMedian.",
            "At most 5 * 10^4 calls will be made to addNum and findMedian.",
        ],
        "follow_up": "If all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?",
        "expected_time_complexity": "O(log n) per add",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Stream 1,2,3 -> medians 1, 1.5, 2.",
        },
    },
    "nc-top-k-frequent-elements": {
        "leetcode_number": 347,
        "statement": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
            "k is in the range [1, the number of unique elements in the array].",
            "It is guaranteed that the answer is unique.",
        ],
        "follow_up": "Your algorithm's time complexity must be better than O(n log n), where n is the array's size.",
        "expected_time_complexity": "O(n log k)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "1 appears 3 times, 2 twice; the top 2 are [1,2].",
        },
    },
    "nc-task-scheduler": {
        "leetcode_number": 621,
        "statement": "You are given an array of CPU `tasks`, each labeled with a letter from A to Z, and a cooling time `n`. Each cycle or interval allows the completion of one task. Tasks can be completed in any order, but there's a constraint: identical tasks must be separated by at least `n` intervals due to cooling time.\n\nReturn the minimum number of intervals required to complete all tasks.",
        "constraints": [
            "1 <= task.length <= 10^4",
            "tasks[i] is an uppercase English letter.",
            "0 <= n <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "With cooling 2, the schedule A->B->idle->A->B->idle->A->B uses 8 intervals.",
        },
    },
    "nc-merge-intervals": {
        "leetcode_number": 56,
        "statement": "Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.",
        "constraints": [
            "1 <= intervals.length <= 10^4",
            "intervals[i].length == 2",
            "0 <= starti <= endi <= 10^4",
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "[1,3] and [2,6] overlap into [1,6]; [8,10] and [15,18] stay separate.",
        },
    },
    "nc-insert-interval": {
        "leetcode_number": 57,
        "statement": "You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [starti, endi]` represent the start and the end of the `i-th` interval and `intervals` is sorted in ascending order by `starti`. You are also given an interval `newInterval = [start, end]` that represents the start and end of another interval.\n\nInsert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order by `starti` and `intervals` still does not have any overlapping intervals (merge overlapping intervals if necessary).\n\nReturn `intervals` after the insertion.",
        "constraints": [
            "0 <= intervals.length <= 10^4",
            "intervals[i].length == 2",
            "0 <= starti <= endi <= 10^4",
            "intervals is sorted by starti in ascending order.",
            "0 <= start <= end <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Inserting [4,8] merges [3,5] and [6,7] into [3,8].",
        },
    },
    "nc-non-overlapping-intervals": {
        "leetcode_number": 435,
        "statement": "Given an array of intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        "constraints": [
            "1 <= intervals.length <= 10^5",
            "intervals[i].length == 2",
            "-5 * 10^4 <= starti < endi <= 5 * 10^4",
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Removing [1,3] leaves [2,4] and [5,6] disjoint.",
        },
    },
    "nc-meeting-rooms": {
        "leetcode_number": 252,
        "statement": "Given an array of meeting time `intervals` where `intervals[i] = [starti, endi]`, determine if a person could attend all meetings.",
        "constraints": [
            "0 <= intervals.length <= 10^4",
            "intervals[i].length == 2",
            "0 <= starti < endi <= 10^6",
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Meeting [7,10] overlaps with [9,12], so attendance is impossible.",
        },
    },
    "nc-meeting-rooms-ii": {
        "leetcode_number": 253,
        "statement": "Given an array of meeting time intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number of conference rooms required.",
        "constraints": [
            "1 <= intervals.length <= 10^4",
            "0 <= starti < endi <= 10^6",
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Meetings [0,30],[5,10],[15,20] require 2 rooms (the 0-30 meeting shares none, the other two overlap).",
        },
    },
}
