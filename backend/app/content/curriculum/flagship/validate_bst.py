"""
Flagship Lesson — Validate Binary Search Tree
 ==============================================

 Gold-standard interactive lesson for BST validation.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "validate_bst"

LESSON: Dict[str, Any] = {
    "lesson_id": "validate_bst_range_check",
    "module_id": "dsa:trees:validate_bst",
    "title": "The Range Check",
    "description": "Validate a binary tree using recursive min/max bounds.",
    "difficulty": "intermediate",
    "est_minutes": 15,
    "xp_reward": 120,
    "skills_taught": ["bst", "validate_bst", "recursion"],
    "srs_concept_tag": "dsa:trees:validate_bst",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Range Check passes each node a legal interval: (min, max). "
            "A BST node must lie in its inherited interval. The left child tightens the max; "
            "the right child tightens the min. One bad value breaks the whole chain.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You checked the bounds, not just the immediate parent.”",
            "🧭 **Captain Byte**\n“Clean. The recursive range is the correct BST invariant.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t compare only to the parent. Check the full inherited range.”",
            "🧭 **Captain Byte**\n“You’re missing an ancestor constraint. The max bound matters.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now propagate min/max bounds correctly.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any BST validation.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Pass (min, max) down. Left tightens max, right tightens min.”",
    },
    "story_context": {
        "title": "The Range Check",
        "narration": (
            "The Range Check passes each node a legal interval: (min, max). "
            "A BST node must lie in its inherited interval."
        ),
        "setting": "range_check",
        "character": "Captain Byte",
        "intro_text": (
            "A BST is not just 'left smaller, right bigger' at each node. "
            "Every node inherits constraints from all its ancestors."
        ),
    },
    "discovery": {
        "title": "Trace the Bounds",
        "visual_primitives": ["compare", "trace", "reveal"],
        "steps": [
            {
                "action": "local_check",
                "narration": "At each node, left must be smaller and right must be larger. But that is not enough.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "Root is 5. Left child is 4. Right child of 4 is 6. Is this a BST?",
                    "options": [
                        {"id": "a", "text": "No — 6 violates the ancestor bound from 5", "correct": True},
                        {"id": "b", "text": "Yes — each node is locally correct", "correct": False},
                        {"id": "c", "text": "Yes — 6 > 4", "correct": False},
                        {"id": "d", "text": "Depends on depth", "correct": False},
                    ],
                    "explanation": "6 is in the left subtree of 5, so it must be < 5. It is not.",
                },
            },
            {
                "action": "range_propagation",
                "narration": "Pass (min, max) down recursively. Left child gets max=parent.val; right child gets min=parent.val.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):\n    if not root:\n        return True\n    if not (min_val < root.val < max_val):\n        return False\n    return (is_valid_bst(root.left, min_val, root.val) and\n            is_valid_bst(root.right, root.val, max_val))\n\n# Valid BST: 2 <- 1 -> 3\nprint(is_valid_bst(TreeNode(2, TreeNode(1), TreeNode(3))))",
                    "expected_output": "True",
                    "hint": "1 is in (-inf, 2), 3 is in (2, inf). Both pass.",
                },
            },
            {
                "action": "inorder_shortcut",
                "narration": "An inorder traversal of a BST produces a strictly increasing sequence.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def is_valid_bst(root):\n    prev = [float('-inf')]\n    def inorder(node):\n        if not node:\n            return True\n        if not inorder(node.left):\n            return False\n        if node.val <= prev[0]:\n            return False\n        prev[0] = node.val\n        return inorder(node.right)\n    return inorder(root)\n\nprint(is_valid_bst(TreeNode(2, TreeNode(1), TreeNode(3))))",
                    "expected_output": "True",
                    "hint": "Inorder: 1, 2, 3. Strictly increasing.",
                },
            },
            {
                "action": "edge_equal",
                "narration": "BSTs usually require strictly less/greater. Equal values break validity.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "A tree has root 2, left child 2. Is this a valid BST?",
                    "options": [
                        {"id": "a", "text": "No — duplicate values violate BST property", "correct": True},
                        {"id": "b", "text": "Yes — equal values are allowed on the left", "correct": False},
                        {"id": "c", "text": "Depends on implementation", "correct": False},
                        {"id": "d", "text": "Yes — left can equal parent", "correct": False},
                    ],
                    "explanation": "Standard BST definition requires left < parent < right. Equal values are not allowed.",
                },
            },
        ],
        "conclusion": (
            "A BST is valid only if every node respects min/max bounds inherited from all ancestors. "
            "The recursive range check or inorder monotonicity both verify this in O(n)."
        ),
    },
    "prediction": {
        "title": "Before You Validate",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict whether this tree is a BST.”",
        "question": "Is the tree [5, 1, 4, null, null, 3, 6] a valid BST?",
        "options": [
            {"id": "a", "text": "No — 3 is in the right subtree of 5 but is less than 5", "correct": True, "explanation": "3 is in the right subtree of 5, violating the BST property."},
            {"id": "b", "text": "Yes — each node is locally correct", "correct": False, "explanation": "Local correctness is insufficient; ancestor bounds matter."},
            {"id": "c", "text": "Yes — 3 > 1 and 3 < 4", "correct": False, "explanation": "3 must also be > 5 because it is in 5's right subtree."},
            {"id": "d", "text": "Depends on insertion order", "correct": False, "explanation": "BST validity is structural, not historical."},
        ],
        "explanation": "3 is in the right subtree of 5 but is less than 5, violating the BST property.",
    },
    "explain": {
        "title": "Explain the Range",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why is checking only the parent node insufficient for BST validation?”",
        "prompt": "Why is checking only the parent node insufficient for BST validation?",
        "answer_format": "short_answer",
        "keywords": ["ancestor", "bound", "range", "inherited", "min", "max", "grandparent", "constraint"],
        "min_words": 10,
        "model_answer": (
            "A node inherits constraints from all its ancestors, not just its parent. "
            "A node in the left subtree of the root must be less than the root, even if it is "
            "greater than its immediate parent. Checking only the parent misses ancestor violations."
        ),
        "intention": "The explanation must show that ancestor constraints propagate through the tree.",
    },
    "guided_build": {
        "title": "Write the Validator",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the recursive range check.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Validate BST",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Pass (min, max) down. Left tightens max, right tightens min.”",
                "description": "Return True if the binary tree is a valid BST.",
                "starter_code": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):\n    if not root:\n        return True\n    if not (min_val < root.val < max_val):\n        return False\n    return (is_valid_bst(root.left, min_val, root.val) and\n            is_valid_bst(root.right, root.val, max_val))\n",
                "function_name": "is_valid_bst",
                "signature": "def is_valid_bst(root: Optional[TreeNode], min_val: float = float('-inf'), max_val: float = float('inf')) -> bool:",
                "test_cases": [
                    {"input": ["[2,1,3]"], "expected": True},
                    {"input": ["[5,1,4,null,null,3,6]"], "expected": False},
                ],
                "hidden_test_cases": [
                    {"input": ["[1]"], "expected": True},
                    {"input": ["[2,2,2]"], "expected": False},
                ],
                "diamonds": 45,
                "scaffolded_hints": [
                    {"level": 1, "text": "Each node must satisfy min_val < node.val < max_val."},
                    {"level": 2, "text": "Left child inherits max_val = node.val; right child inherits min_val = node.val."},
                    {"level": 3, "text": "Base case: empty tree is valid."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Recover Tree",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same BST idea. Two nodes are swapped. Find them.”",
        "description": (
            "A BST was modified by swapping exactly two nodes. "
            "Return the values of the two swapped nodes in ascending order."
        ),
        "function_name": "recover_tree",
        "signature": "def recover_tree(root: Optional[TreeNode]) -> List[int]:",
        "description_full": (
            "Find the two swapped nodes in a BST.\n\n"
            "Example:\n"
            "  recover_tree([3, 1, 4, null, null, 2]) -> [1, 2]\n\n"
            "Hint: inorder traversal should be strictly increasing. Find the two violations."
        ),
        "test_cases": [
            {"input": ["[3,1,4,null,null,2]"], "expected": [1, 2]},
        ],
        "hidden_test_cases": [
            {"input": ["[1,3,null,null,2]"], "expected": [1, 3]},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Inorder traversal of a BST must be strictly increasing."},
            {"level": 2, "text": "Find the two positions where inorder[i] > inorder[i+1]."},
            {"level": 3, "text": "Swap the first violation's left element with the second violation's right element."},
        ],
    },
    "assessment": {
        "title": "Range Check Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove the range is automatic. Timed.”",
        "description": "Validate a BST, explain ancestor bounds, and fix a local-check bug.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "root = TreeNode(5, TreeNode(3), TreeNode(7, TreeNode(4), TreeNode(8)))\nprint(is_valid_bst(root))",
                "answer_format": "single_choice",
                "expected_answer": "False",
                "options": [
                    {"id": "a", "text": "False", "correct": True},
                    {"id": "b", "text": "True", "correct": False},
                ],
                "explanation": "4 is in the right subtree of 5 but less than 5, violating the BST property.",
            },
            {
                "type": "concept",
                "question": "Why is checking only parent-child relationships insufficient for BST validation?",
                "answer_format": "short_answer",
                "keywords": ["ancestor", "bound", "range", "inherited", "min", "max", "grandparent", "constraint"],
                "explanation": "A node must satisfy constraints from all ancestors, not just its parent.",
            },
            {
                "type": "debug",
                "code": "def is_valid_bst(root):\n    if not root:\n        return True\n    if root.left and root.left.val >= root.val:\n        return False\n    if root.right and root.right.val <= root.val:\n        return False\n    return is_valid_bst(root.left) and is_valid_bst(root.right)\n# should catch ancestor violations",
                "error": "is_valid_bst([5,3,7,2,4,6,8]) returns True even though 4 is in 5's right subtree.",
                "question": "Fix the validator to check ancestor bounds.",
                "fix": "def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):\n    if not root:\n        return True\n    if not (min_val < root.val < max_val):\n        return False\n    return (is_valid_bst(root.left, min_val, root.val) and\n            is_valid_bst(root.right, root.val, max_val))",
                "explanation": "Passing min/max bounds down ensures every node respects all ancestor constraints.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Local Check",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I only checked parent-child. Find the broken assumption.”",
        "story": (
            "A validator checked only parent-child relationships. "
            "On a tree where 5 is root, 3 is left, and 4 is right child of 3, "
            "it returned True even though 4 < 5 violates the BST property. "
            "What assumption is wrong?"
        ),
        "buggy_code": "def is_valid_bst(root):\n    if not root:\n        return True\n    if root.left and root.left.val >= root.val:\n        return False\n    if root.right and root.right.val <= root.val:\n        return False\n    return is_valid_bst(root.left) and is_valid_bst(root.right)\n",
        "expected_output": "False",
        "actual_output": "True — missed the ancestor violation",
        "diagnosis": {
            "question": "Which assumption makes this validator unsafe?",
            "options": [
                {"id": "a", "text": "It assumes parent-child checks are sufficient, ignoring ancestor bounds", "correct": True, "why": "A node must satisfy constraints from all ancestors, not just its parent."},
                {"id": "b", "text": "It uses >= instead of >", "correct": False, "why": "The comparison is correct; the scope is the issue."},
                {"id": "c", "text": "It doesn't handle null children", "correct": False, "why": "Null checks are handled correctly."},
                {"id": "d", "text": "It checks left before right", "correct": False, "why": "Order of checks doesn't matter."},
            ],
        },
        "fix": "Pass (min_val, max_val) bounds down recursively.",
        "fixed_code": "def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):\n    if not root:\n        return True\n    if not (min_val < root.val < max_val):\n        return False\n    return (is_valid_bst(root.left, min_val, root.val) and\n            is_valid_bst(root.right, root.val, max_val))\n",
        "explanation": (
            "Local parent-child checks ignore ancestor constraints. "
            "Recursive min/max bounds ensure every node respects the full inherited range."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:trees:validate_bst",
        "concept_name": "Validate BST",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "use recursive min/max bounds",
            "left child tightens max to parent.val",
            "right child tightens min to parent.val",
            "inorder traversal is an alternative O(n) check",
        ],
        "spaced_fields": [
            "min_max_bounds",
            "left_tightens_max",
            "right_tightens_min",
            "inorder_alternative",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "validate_bst",
        "unlocks_next": ["bst_operations"],
        "tower_badge": "range_check",
        "world_node": {
            "level": 23,
            "title": "The Range Check",
            "color": "teal",
            "icon": "📐",
            "description": "Validate BST using recursive min/max bounds in O(n)",
        },
    },
}
