"""LeetCode metadata overlay — Part 3: Trees."""

LEETCODE_META = {
    "nc-invert-binary-tree": {
        "leetcode_number": 226,
        "statement": "Given the `root` of a binary tree, invert the tree, and return its root.",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 100].",
            "-100 <= Node.val <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Mirror the tree left-to-right: every left subtree becomes the right subtree and vice versa.",
        },
    },
    "nc-max-depth-binary-tree": {
        "leetcode_number": 104,
        "statement": "Given the `root` of a binary tree, return its maximum depth.\n\nA binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 10^4].",
            "-100 <= Node.val <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The longest root-to-leaf path is 3->9->20->15 (or 3->9->20->7), depth 3.",
        },
    },
    "nc-diameter-binary-tree": {
        "leetcode_number": 543,
        "statement": "Given the `root` of a binary tree, return the length of the diameter of the tree.\n\nThe diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.\n\nThe length of a path between two nodes is represented by the number of edges between them.",
        "constraints": [
            "The number of nodes in the tree is in the range [1, 10^4].",
            "-100 <= Node.val <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The longest path passes through node 1 using left depth 1 and right depth 2 (3 edges).",
        },
    },
    "nc-balanced-binary-tree": {
        "leetcode_number": 110,
        "statement": "Given a binary tree, determine if it is height-balanced.\n\nA height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 5000].",
            "-10^4 <= Node.val <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Every node's subtrees differ by at most 1 -> balanced.",
            1: "Node 2 has right subtree depth 2 vs left depth 0 -> difference 2 -> not balanced.",
        },
    },
    "nc-same-tree": {
        "leetcode_number": 100,
        "statement": "Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.\n\nTwo binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
        "constraints": [
            "The number of nodes in both trees is in the range [0, 100].",
            "-10^4 <= Node.val <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Both trees have the same structure and values.",
            1: "Right subtree values differ (2 vs 3).",
        },
    },
    "nc-subtree-of-another-tree": {
        "leetcode_number": 572,
        "statement": "Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.\n\nA subtree of a binary tree `tree` is a tree that consists of a node in `tree` and all of this node's descendants. The tree `tree` could also be considered as a subtree of itself.",
        "constraints": [
            "The number of nodes in the root tree is in the range [1, 2000].",
            "The number of nodes in the subRoot tree is in the range [0, 1000].",
            "-10^4 <= root.val <= 10^4",
            "-10^4 <= subRoot.val <= 10^4",
        ],
        "expected_time_complexity": "O(n * m)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The subtree rooted at node 4 in the main tree equals subRoot.",
            1: "The main tree is itself a subtree of itself.",
        },
    },
    "nc-lowest-common-ancestor-bst": {
        "leetcode_number": 235,
        "statement": "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.\n\nAccording to the definition of LCA on Wikipedia: \u201cThe lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in T that has both `p` and `q` as descendants (where we allow **a node to be a descendant of itself**).\u201d",
        "constraints": [
            "The number of nodes in the tree is in the range [2, 10^5].",
            "-10^9 <= Node.val <= 10^9",
            "All Node.val are unique.",
            "p != q",
            "p and q will exist in the BST.",
        ],
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "example_explanations": {
            0: "The LCA of 2 and 8 is 6.",
            1: "The LCA of 2 and 4 is 2 (a node can be its own descendant).",
        },
    },
    "nc-binary-tree-level-order": {
        "leetcode_number": 102,
        "statement": "Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 2000].",
            "-1000 <= Node.val <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Each level is collected left-to-right into its own list.",
        },
    },
    "nc-binary-tree-right-side-view": {
        "leetcode_number": 199,
        "statement": "Given the `root` of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 100].",
            "-100 <= Node.val <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "From the right side you see nodes 1, 3, 4.",
        },
    },
    "nc-validate-binary-search-tree": {
        "leetcode_number": 98,
        "statement": "Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).\n\nA valid BST is defined as follows:\n\n- The left subtree of a node contains only nodes with keys less than the node's key.\n- The right subtree of a node contains only nodes with keys greater than the node's key.\n- Both the left and right subtrees must also be binary search trees.",
        "constraints": [
            "The number of nodes in the tree is in the range [1, 10^4].",
            "-2^31 <= Node.val <= 2^31 - 1",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Every node satisfies the BST invariant with the open range (-inf, inf).",
            1: "Node 4 is in node 3's right subtree but 4 > 3, so the invariant is violated.",
        },
    },
    "nc-kth-smallest-bst": {
        "leetcode_number": 230,
        "statement": "Given the `root` of a binary search tree, and an integer `k`, return the `k-th` smallest value (1-indexed) of all the values of the nodes in the tree.",
        "constraints": [
            "The number of nodes in the tree is n.",
            "1 <= k <= n <= 10^4",
            "0 <= Node.val <= 10^4",
        ],
        "follow_up": "If the BST is modified often (i.e., we can do insert and delete operations) and you need to find the kth smallest frequently, how would you optimize?",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "In-order traversal gives [1,2,3]; the 1st smallest is 1.",
        },
    },
    "nc-construct-binary-tree": {
        "leetcode_number": 105,
        "statement": "Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.",
        "constraints": [
            "1 <= preorder.length <= 3000",
            "inorder.length == preorder.length",
            "-3000 <= preorder[i], inorder[i] <= 3000",
            "preorder and inorder consist of unique values.",
            "Each value of inorder also appears in preorder.",
            "preorder is guaranteed to be the preorder traversal of the tree.",
            "inorder is guaranteed to be the inorder traversal of the tree.",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The first preorder value 3 is the root; inorder splits the tree into left [9] and right [20,15,7].",
        },
    },
    "nc-binary-tree-max-path-sum": {
        "leetcode_number": 124,
        "statement": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.\n\nThe path sum of a path is the sum of the node's values in the path.\n\nGiven the `root` of a binary tree, return the maximum path sum of any non-empty path.",
        "constraints": [
            "The number of nodes in the tree is in the range [1, 3 * 10^4].",
            "-1000 <= Node.val <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The path 15 -> 20 -> 7 gives sum 42.",
        },
    },
    "nc-serialize-deserialize-tree": {
        "leetcode_number": 297,
        "statement": "Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.\n\nDesign an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.\n\nGiven the root of a binary tree, return the same tree after serializing and deserializing it.",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 10^4].",
            "-1000 <= Node.val <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "serialize -> '1,2,3,#,#,4,5'; deserialize rebuilds the identical tree.",
        },
    },
    "st-path-sum": {
        "leetcode_number": 112,
        "statement": "Given the `root` of a binary tree and an integer `targetSum`, return `true` if the tree has a root-to-leaf path such that adding up all the values along the path equals `targetSum`.\n\nA leaf is a node with no children.",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 5000].",
            "-1000 <= Node.val <= 1000",
            "-1000 <= targetSum <= 1000",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "The path 5->4->11->2 sums to 22.",
        },
    },
    "nc-count-good-nodes": {
        "leetcode_number": 1448,
        "statement": "Given a binary tree `root`, a node X in the tree is named **good** if in the path from root to X there are no nodes with a value greater than X.\n\nReturn the number of **good** nodes in the binary tree.",
        "constraints": [
            "The number of nodes in the binary tree is in the range [1, 10^5].",
            "-10^4 <= Node.val <= 10^4",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Good nodes: 3, 3, 4 (the 1 in the right subtree is worse than the 3 above it).",
        },
    },
    "nc-max-width-binary-tree": {
        "leetcode_number": 662,
        "statement": "Given the `root` of a binary tree, return the maximum width of the given tree.\n\nThe maximum width of a tree is the maximum width among all levels.\n\nThe width of one level is defined as the length between the end-nodes (the leftmost and rightmost non-null nodes), where the null nodes between the end-nodes that would be present in a complete binary tree extending down to that level are also counted into the length calculation.\n\nIt is guaranteed that the answer will be in the range of a 32-bit signed integer.",
        "constraints": [
            "The number of nodes in the tree is in the range [1, 3000].",
            "-100 <= Node.val <= 100",
        ],
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "example_explanations": {
            0: "Levels have widths 1, 2, 3 -> max 3.",
            1: "The bottom level spans from node 5 (index 8) to node 9 (index 13), width 8.",
        },
    },
}
