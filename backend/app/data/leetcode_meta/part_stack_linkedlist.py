"""LeetCode metadata overlay — Part 2: Stack & Linked List."""

LEETCODE_META = {
    "nc-valid-parentheses": {
        "leetcode_number": 20,
        "statement": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "constraints": [
            "1 <= s.length <= 10^4",
            "s consists of parentheses only '()[]{}'.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The brackets close in the correct order.",
            1: "The opening bracket has no matching closer.",
            2: "(] mismatches, so it is invalid.",
        },
    },
    "nc-min-stack": {
        "leetcode_number": 155,
        "statement": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.\n\nImplement the `MinStack` class:\n\n- `MinStack()` initializes the stack object.\n- `void push(int val)` pushes the element val onto the stack.\n- `void pop()` removes the element on the top of the stack.\n- `int top()` gets the top element of the stack.\n- `int getMin()` retrieves the minimum element in the stack.\n\nYou must implement a solution with `O(1)` time complexity for each function.",
        "constraints": [
            "-2^31 <= val <= 2^31 - 1",
            "Methods pop, top and getMin operations will always be called on non-empty stacks.",
            "At most 3 * 10^4 calls will be made to push, pop, top, and getMin.",
        ],
        "expected_time_complexity": "O(1) per operation",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Push -2, 0, -3 -> getMin is -3; pop -> top is 0; getMin is -2.",
        },
    },
    "nc-evaluate-reverse-polish-notation": {
        "leetcode_number": 150,
        "statement": "You are given an array of strings `tokens` that represents an arithmetic expression in a Reverse Polish Notation.\n\nEvaluate the expression. Return an integer that represents the value of the expression.\n\nNote that:\n\n- The valid operators are `'+'`, `'-'`, `'*'`, and `'/'`.\n- Each operand may be an integer or another expression.\n- The division between two integers always truncates toward zero.\n- There will not be any division by zero.\n- The input represents a valid arithmetic expression in a reverse polish notation.\n- The answer and all the intermediate calculations can be represented in a 32-bit integer.",
        "constraints": [
            "1 <= tokens.length <= 10^4",
            "tokens[i] is either an operator: '+', '-', '*', or '/', or an integer in the range [-200, 200].",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "((2 + 1) * 3) = 9.",
            1: "(4 + (13 / 5)) = 6.",
        },
    },
    "nc-daily-temperatures": {
        "leetcode_number": 739,
        "statement": "Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0` instead.",
        "constraints": [
            "1 <= temperatures.length <= 10^5",
            "30 <= temperatures[i] <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "For day 1 (73), the next warmer day is day 2 (74), so answer is 1; for day 5 (76), wait 2 days until 75 -> 80.",
        },
    },
    "nc-car-fleet": {
        "leetcode_number": 853,
        "statement": "There are `n` cars going to the same destination along a one-lane road. The destination is `target` miles away.\n\nYou are given two integer array `position` and `speed`, both of length `n`, where `position[i]` is the position of the `i-th` car and `speed[i]` is the speed of the `i-th` car (in miles per hour).\n\nA car can never pass another car ahead of it, but it can catch up and drive bumper to bumper at the same speed. The faster car will slow down to match the slower car's speed. The distance between these two cars is ignored (i.e., they are assumed to have the same position).\n\nA car fleet is some non-empty set of cars driving at the same position and same speed. Note that a single car is also a car fleet.\n\nIf a car catches up to a car fleet right at the destination point, it will still be considered as one car fleet.\n\nReturn the number of car fleets that will arrive at the destination.",
        "constraints": [
            "n == position.length == speed.length",
            "1 <= n <= 10^5",
            "0 < target <= 10^6",
            "0 <= position[i] < target",
            "All the values of position are unique.",
            "0 < speed[i] <= 10^6",
        ],
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Three fleets arrive: [0,1], [3], and [4,2] merged according to arrival times.",
        },
    },
    "nc-largest-rectangle-histogram": {
        "leetcode_number": 84,
        "statement": "Given an array of integers `heights` representing the histogram's bar height where the width of each bar is `1`, return the area of the largest rectangle in the histogram.",
        "constraints": [
            "1 <= heights.length <= 10^5",
            "0 <= heights[i] <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The largest rectangle uses heights 2 and 1 -> the 6-unit rectangle spanning bars 2..4, or the two-bar 5x2 = 10. The maximum is 10.",
        },
    },
    "nc-reverse-linked-list": {
        "leetcode_number": 206,
        "statement": "Given the `head` of a singly linked list, reverse the list, and return the reversed list.",
        "constraints": [
            "The number of nodes in the list is the range [0, 5000].",
            "-5000 <= Node.val <= 5000",
        ],
        "follow_up": "A linked list can be reversed either iteratively or recursively. Could you implement both?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The list 1->2->3->4->5 reversed is 5->4->3->2->1.",
        },
    },
    "nc-merge-two-sorted-lists": {
        "leetcode_number": 21,
        "statement": "You are given the heads of two sorted linked lists `list1` and `list2`.\n\nMerge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.\n\nReturn the head of the merged linked list.",
        "constraints": [
            "The number of nodes in both lists is in the range [0, 50].",
            "-100 <= Node.val <= 100",
            "Both list1 and list2 are sorted in non-decreasing order.",
        ],
        "expected_time_complexity": "O(n + m)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Merging 1->2->4 and 1->3->4 gives 1->1->2->3->4->4.",
        },
    },
    "nc-reorder-list": {
        "leetcode_number": 143,
        "statement": "You are given the head of a singly linked-list. The list can be represented as:\n\n`L0 -> L1 -> ... -> Ln-1 -> Ln`\n\nReorder the list to be on the following form:\n\n`L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...`\n\nYou may not modify the values in the list's nodes. Only nodes themselves may be changed.",
        "constraints": [
            "The number of nodes in the list is in the range [1, 5 * 10^4].",
            "1 <= Node.val <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The list 1->2->3->4 is reordered to 1->4->2->3.",
        },
    },
    "nc-remove-nth-from-end": {
        "leetcode_number": 19,
        "statement": "Given the `head` of a linked list, remove the `n-th` node from the end of the list and return its head.",
        "constraints": [
            "The number of nodes in the list is sz.",
            "1 <= sz <= 30",
            "0 <= Node.val <= 100",
            "1 <= n <= sz",
        ],
        "follow_up": "Could you do this in one pass?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "Removing the 2nd node from the end of 1->2->3->4->5 leaves 1->2->3->5.",
        },
    },
    "nc-copy-list-random-pointer": {
        "leetcode_number": 138,
        "statement": "A linked list of length `n` is given such that each node contains an additional random pointer, which could point to any node in the list, or `null`.\n\nConstruct a deep copy of the list. The deep copy should consist of exactly `n` brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the `next` and `random` pointers of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.\n\nReturn the head of the copied linked list.",
        "constraints": [
            "0 <= n <= 1000",
            "-10^4 <= Node.val <= 10^4",
            "Node.random is null or is pointing to some node in the linked list.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The deep copy keeps values and random links identical.",
        },
    },
    "nc-add-two-numbers": {
        "leetcode_number": 2,
        "statement": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.",
        "constraints": [
            "The number of nodes in each linked list is in the range [1, 100].",
            "0 <= Node.val <= 9",
            "It is guaranteed that the list represents a number that does not have leading zeros.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "342 + 465 = 807, stored reversed as 7->0->8.",
        },
    },
    "nc-linked-list-cycle": {
        "leetcode_number": 141,
        "statement": "Given `head`, the head of a linked list, determine if the linked list has a cycle in it.\n\nThere is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. Note that `pos` is not passed as a parameter.\n\nReturn `true` if there is a cycle in the linked list. Otherwise, return `false`.",
        "constraints": [
            "The number of the nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "pos is -1 or a valid index in the linked-list.",
        ],
        "follow_up": "Can you solve it using O(1) (i.e. constant) memory?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "There is a cycle in the list: node 3 loops back to node 1.",
            1: "No cycle, tail points to null.",
        },
    },
    "nc-merge-k-sorted-lists": {
        "leetcode_number": 23,
        "statement": "You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.\n\nMerge all the linked-lists into one sorted linked-list and return it.",
        "constraints": [
            "k == lists.length",
            "0 <= k <= 10^4",
            "0 <= lists[i].length <= 500",
            "-10^4 <= lists[i][j] <= 10^4",
            "The sum of lists[i].length will not exceed 10^4.",
        ],
        "expected_time_complexity": "O(n log k)",
        "expected_space_complexity": "O(k)",
        "example_explanations": {
            0: "Merging the three lists yields 1->1->2->3->4->4->5->6.",
        },
    },
    "nc-reverse-nodes-k-group": {
        "leetcode_number": 25,
        "statement": "Given the `head` of a linked list, reverse the nodes of the list `k` at a time, and return the modified list.\n\n`k` is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of `k` then left-out nodes, in the end, should remain as it is.\n\nYou may not alter the values in the list's nodes, only nodes themselves may be changed.",
        "constraints": [
            "The number of nodes in the list is n.",
            "1 <= k <= n <= 5000",
            "0 <= Node.val <= 1000",
        ],
        "follow_up": "Can you solve the problem in O(1) extra memory space?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "k=2: reverse pairs -> 2->1->4->3->5.",
            1: "k=3: reverse triples -> 3->2->1->4->5 (the trailing 2 nodes are kept as-is).",
        },
    },
    "st-middle-linked-list": {
        "leetcode_number": 876,
        "statement": "Given the head of a singly linked list, return the middle node of the linked list.\n\nIf there are two middle nodes, return the second middle node.",
        "constraints": [
            "The number of nodes in the list is in the range [1, 100].",
            "1 <= Node.val <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The middle node of 1->2->3->4->5 is node 3.",
            1: "Two middles exist (3 and 4); the second middle 4 is returned.",
        },
    },
    "nc-design-twitter": {
        "leetcode_number": 355,
        "statement": "Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user's news feed.\n\nImplement the `Twitter` class:\n\n- `Twitter()` Initializes your twitter object.\n- `void postTweet(int userId, int tweetId)` Composes a new tweet with ID tweetId by the user userId. Each call to this function will be made with a unique tweetId.\n- `List<Integer> getNewsFeed(int userId)` Retrieves the 10 most recent tweet IDs in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themself. Tweets must be ordered from most recent to least recent.\n- `void follow(int followerId, int followeeId)` The user with ID followerId started following the user with ID followeeId.\n- `void unfollow(int followerId, int followeeId)` The user with ID followerId started unfollowing the user with ID followeeId.",
        "constraints": [
            "1 <= userId, followerId, followeeId <= 500",
            "0 <= tweetId <= 10^4",
            "All the tweets have unique IDs.",
            "At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, and unfollow.",
        ],
        "expected_time_complexity": "O(n) per getNewsFeed (n = followed users)",
        "expected_space_complexity": "O(tweets + follows)",
        "example_explanations": {
            0: "User 1 posts 5, feeds [5]; follows user 2, user 2 posts 6, feed becomes [6, 5].",
        },
    },
}
