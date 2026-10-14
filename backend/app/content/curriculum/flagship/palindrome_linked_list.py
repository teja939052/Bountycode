"""
Flagship Lesson — Palindrome Linked List
 =========================================

 Gold-standard interactive lesson for fast/slow pointer palindrome check.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "palindrome_linked_list"

LESSON: Dict[str, Any] = {
    "lesson_id": "palindrome_linked_list_fast_slow",
    "module_id": "dsa:linked_list:palindrome",
    "title": "The Mirror Check",
    "description": "Check if a linked list is a palindrome using fast/slow pointers and in-place reversal.",
    "difficulty": "intermediate",
    "est_minutes": 16,
    "xp_reward": 130,
    "skills_taught": ["linked_list", "palindrome", "fast_slow_pointers"],
    "srs_concept_tag": "dsa:linked_list:palindrome",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Mirror Check uses two tricks: fast/slow pointers to find the middle, "
            "and in-place reversal to compare the first half with the reversed second half. "
            "O(n) time, O(1) space.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You found the middle and compared halves.”",
            "🧭 **Captain Byte**\n“Clean. Fast/slow + reverse = O(n) time, O(1) space.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t build an array. Use the pointers.”",
            "🧭 **Captain Byte**\n“You’re comparing from the start. The second half is reversed.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now reverse only the second half.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any linked-list palindrome.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Find middle with fast/slow, reverse second half, compare.”",
    },
    "story_context": {
        "title": "The Mirror Check",
        "narration": (
            "The Mirror Check uses two tricks: fast/slow pointers to find the middle, "
            "and in-place reversal to compare the first half with the reversed second half."
        ),
        "setting": "mirror_check",
        "character": "Captain Byte",
        "intro_text": (
            "A linked list palindrome can be checked in O(n) time and O(1) extra space. "
            "The trick: reverse the second half in place, then compare node by node."
        ),
    },
    "discovery": {
        "title": "Find the Middle",
        "visual_primitives": ["move", "compare", "trace"],
        "steps": [
            {
                "action": "fast_slow",
                "narration": "Fast moves two steps, slow moves one. When fast reaches the end, slow is at the middle.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "fast = slow = head\nwhile fast and fast.next:\n    fast = fast.next.next\n    slow = slow.next\nprint('Middle:', slow.val if slow else None)",
                    "expected_output": "Middle: 2",
                    "hint": "For 1->2->3->4->5, slow stops at 3 (the middle node).",
                },
            },
            {
                "action": "reverse_second",
                "narration": "Reverse the second half starting from slow. Then compare head with the reversed half.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def reverse(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev\n\n# 1->2->3->2->1\n# After reverse from middle: 1->2->3<-2<-1",
                    "expected_output": "Reversed second half: 1->2->3",
                    "hint": "The second half (2->1) becomes 1->2 when reversed.",
                },
            },
            {
                "action": "compare",
                "narration": "Compare the first half with the reversed second half node by node.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "First half: 1->2->3, reversed second half: 1->2->3. Are they equal?",
                    "options": [
                        {"id": "a", "text": "Yes — palindrome", "correct": True},
                        {"id": "b", "text": "No — not a palindrome", "correct": False},
                        {"id": "c", "text": "Only if lengths match", "correct": False},
                        {"id": "d", "text": "Depends on values", "correct": False},
                    ],
                    "explanation": "Both halves have the same values in order, so the list is a palindrome.",
                },
            },
            {
                "action": "odd_length",
                "narration": "For odd-length lists, skip the middle node before comparing.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "List: 1->2->3->2->1. After fast/slow, slow points to 3. What should we do?",
                    "options": [
                        {"id": "a", "text": "Reverse from slow.next to skip the middle", "correct": True},
                        {"id": "b", "text": "Reverse from slow including the middle", "correct": False},
                        {"id": "c", "text": "Compare from slow", "correct": False},
                        {"id": "d", "text": "No special handling needed", "correct": False},
                    ],
                    "explanation": "The middle node doesn't need comparison. Skip it by reversing from slow.next.",
                },
            },
        ],
        "conclusion": (
            "Fast/slow pointers find the middle in one pass. "
            "In-place reversal of the second half lets you compare node by node in O(1) extra space."
        ),
    },
    "prediction": {
        "title": "Before You Check",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict whether this list is a palindrome.”",
        "question": "Is the linked list 1 -> 2 -> 2 -> 1 a palindrome?",
        "options": [
            {"id": "a", "text": "Yes", "correct": True, "explanation": "The list reads the same forward and backward."},
            {"id": "b", "text": "No", "correct": False, "explanation": "1, 2, 2, 1 is symmetric."},
            {"id": "c", "text": "Only if length is even", "correct": False, "explanation": "Palindrome property is independent of length parity."},
            {"id": "d", "text": "Depends on the values", "correct": False, "explanation": "The values clearly form a palindrome."},
        ],
        "explanation": "1 -> 2 -> 2 -> 1 is a palindrome because it reads the same forward and backward.",
    },
    "explain": {
        "title": "Explain the Mirror",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does reversing the second half use O(1) extra space?”",
        "prompt": "Why does reversing the second half use O(1) extra space?",
        "answer_format": "short_answer",
        "keywords": ["in-place", "pointer", "rewire", "next", "reverse", "constant", "extra", "space", "node"],
        "min_words": 10,
        "model_answer": (
            "In-place reversal only rewires the next pointers of existing nodes. "
            "It does not create new nodes or allocate extra data structures. "
            "Only a few pointer variables are used, so the extra space is O(1)."
        ),
        "intention": "The explanation must distinguish pointer rewiring from allocation.",
    },
    "guided_build": {
        "title": "Write the Mirror",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the fast/slow + reverse check.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Palindrome Linked List",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Fast/slow to middle, reverse second half, compare.”",
                "description": "Return True if the linked list is a palindrome, O(n) time and O(1) space.",
                "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef is_palindrome(head):\n    if not head or not head.next:\n        return True\n    fast = slow = head\n    while fast and fast.next:\n        fast = fast.next.next\n        slow = slow.next\n    prev = None\n    curr = slow\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    left, right = head, prev\n    while right:\n        if left.val != right.val:\n            return False\n        left = left.next\n        right = right.next\n    return True\n",
                "function_name": "is_palindrome",
                "signature": "def is_palindrome(head: Optional[ListNode]) -> bool:",
                "test_cases": [
                    {"input": ["[1,2,2,1]"], "expected": True},
                    {"input": ["[1,2]"], "expected": False},
                ],
                "hidden_test_cases": [
                    {"input": ["[1]"], "expected": True},
                    {"input": ["[1,0,1]"], "expected": True},
                    {"input": ["[1,2,3,2,1]"], "expected": True},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use fast/slow pointers to find the middle."},
                    {"level": 2, "text": "Reverse the second half in place."},
                    {"level": 3, "text": "Compare the first half with the reversed second half node by node."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Palindrome Partition",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same palindrome idea, different problem. Cut into the fewest palindromic substrings.”",
        "description": (
            "Given a string s, partition it so that every substring is a palindrome. "
            "Return the minimum number of cuts needed."
        ),
        "function_name": "min_cut",
        "signature": "def min_cut(s: str) -> int:",
        "description_full": (
            "Return the minimum cuts needed for a palindrome partitioning.\n\n"
            "Example:\n"
            "  min_cut('aab') -> 1  ('aa' | 'b')\n\n"
            "Hint: precompute palindrome table, then DP on cuts."
        ),
        "test_cases": [
            {"input": ["aab"], "expected": 1},
            {"input": ["a"], "expected": 0},
        ],
        "hidden_test_cases": [
            {"input": ["ab"], "expected": 1},
            {"input": ["aba"], "expected": 0},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Precompute is_palindrome[i][j] for all substrings."},
            {"level": 2, "text": "If s[i:j+1] is palindrome, cuts[j] = min(cuts[j], cuts[i-1] + 1)."},
            {"level": 3, "text": "Handle the empty prefix case: cuts[-1] = -1 conceptually."},
        ],
    },
    "assessment": {
        "title": "Mirror Check Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you can mirror any chain. Timed.”",
        "description": "Check palindrome, explain O(1) space, and fix a broken reverse.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "head = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))\nfast = slow = head\nwhile fast and fast.next:\n    fast = fast.next.next\n    slow = slow.next\nprev = None\ncurr = slow\nwhile curr:\n    nxt = curr.next\n    curr.next = prev\n    prev = curr\n    curr = nxt\nleft, right = head, prev\npal = True\nwhile right:\n    if left.val != right.val:\n        pal = False\n        break\n    left = left.next\n    right = right.next\nprint(pal)",
                "answer_format": "single_choice",
                "expected_answer": "True",
                "options": [
                    {"id": "a", "text": "True", "correct": True},
                    {"id": "b", "text": "False", "correct": False},
                ],
                "explanation": "The reversed second half matches the first half. Palindrome confirmed.",
            },
            {
                "type": "concept",
                "question": "Why does reversing the second half use O(1) extra space?",
                "answer_format": "short_answer",
                "keywords": ["in-place", "pointer", "rewire", "next", "reverse", "constant", "extra", "space", "node"],
                "explanation": "Only pointer variables are used; no new nodes are allocated.",
            },
            {
                "type": "debug",
                "code": "def is_palindrome(head):\n    fast = slow = head\n    while fast and fast.next:\n        fast = fast.next.next\n        slow = slow.next\n    slow = reverse(slow)\n    while slow:\n        if head.val != slow.val:\n            return False\n        head = head.next\n        slow = slow.next\n    return True\n# should not modify the original list permanently",
                "error": "The list is permanently modified after the function runs.",
                "question": "Fix the in-place reversal so the list can be restored.",
                "fix": "After comparison, reverse the second half again to restore the original list.",
                "explanation": "In-place reversal modifies next pointers. Reversing again restores the original order.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Wrong Half",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I reversed the first half instead of the second. Find the broken assumption.”",
        "story": (
            "A programmer reversed the first half of the list. On 1->2->2->1, "
            "the comparison fails because the first half is now 2->1 instead of 1->2. "
            "What assumption is wrong?"
        ),
        "buggy_code": "def is_palindrome(head):\n    fast = slow = head\n    prev = None\n    while fast and fast.next:\n        fast = fast.next.next\n        nxt = slow.next\n        slow.next = prev\n        prev = slow\n        slow = nxt\n    left, right = prev, slow\n    while right:\n        if left.val != right.val:\n            return False\n        left = left.next\n        right = right.next\n    return True\n",
        "expected_output": "True",
        "actual_output": "False on 1->2->2->1 because the first half is reversed",
        "diagnosis": {
            "question": "Which assumption makes this check fail?",
            "options": [
                {"id": "a", "text": "It reverses the first half instead of the second half", "correct": True, "why": "Reversing the first half changes the order of the first half, so comparison fails."},
                {"id": "b", "text": "Fast/slow pointers are wrong", "correct": False, "why": "Fast/slow correctly finds the middle."},
                {"id": "c", "text": "The comparison loop is wrong", "correct": False, "why": "The comparison logic is correct; the reversed half is wrong."},
                {"id": "d", "text": "The list has an even number of nodes", "correct": False, "why": "Even/odd length is not the issue; the reversed half is."},
            ],
        },
        "fix": "Reverse only the second half starting from slow, not the first half.",
        "fixed_code": "def is_palindrome(head):\n    if not head or not head.next:\n        return True\n    fast = slow = head\n    while fast and fast.next:\n        fast = fast.next.next\n        slow = slow.next\n    prev = None\n    curr = slow\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    left, right = head, prev\n    while right:\n        if left.val != right.val:\n            return False\n        left = left.next\n        right = right.next\n    return True\n",
        "explanation": (
            "Reversing the first half destroys the original order. "
            "The second half must be reversed so the first half can be compared against it in original order."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:linked_list:palindrome",
        "concept_name": "Palindrome Linked List",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "fast/slow pointers find the middle",
            "reverse the second half in place",
            "compare first half with reversed second half",
            "restore the list if needed",
        ],
        "spaced_fields": [
            "fast_slow_middle",
            "reverse_second_half",
            "compare_halves",
            "in_place_space",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "palindrome_linked_list",
        "unlocks_next": ["linked_list_advanced"],
        "tower_badge": "mirror_check",
        "world_node": {
            "level": 20,
            "title": "The Mirror Check",
            "color": "teal",
            "icon": "🪞",
            "description": "Check linked list palindrome in O(n) time and O(1) space",
        },
    },
}
