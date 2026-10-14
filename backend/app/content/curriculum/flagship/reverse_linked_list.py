"""
Flagship Lesson — Reverse Linked List
 ======================================

 Gold-standard interactive lesson for linked list reversal.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "reverse_linked_list"

LESSON: Dict[str, Any] = {
    "lesson_id": "reverse_linked_list_pointer_dance",
    "module_id": "dsa:linked_list:reverse",
    "title": "The Pointer Dance",
    "description": "Reverse a singly linked list by rewiring next pointers in one pass.",
    "difficulty": "intermediate",
    "est_minutes": 16,
    "xp_reward": 130,
    "skills_taught": ["linked_list", "reverse", "pointer_manipulation"],
    "srs_concept_tag": "dsa:linked_list:reverse",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Pointer Dance has three partners: prev, curr, and nxt. "
            "You walk the chain, saving the next node before you cut the link. "
            "Then you point curr back to prev and advance all three. "
            "When curr reaches the end, prev is the new head.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You tracked all three pointers.”",
            "🧭 **Captain Byte**\n“Clean. The chain is reversed without extra space.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t lose the next node. Save nxt before you cut.”",
            "🧭 **Captain Byte**\n“You’re overwriting curr.next before saving it. Track nxt.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken link. Now save nxt before you move.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any linked-list reversal.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. prev, curr, nxt — save nxt first.”",
    },
    "story_context": {
        "title": "The Pointer Dance",
        "narration": (
            "The Pointer Dance has three partners: prev, curr, and nxt. "
            "You walk the chain, saving the next node before you cut the link. "
            "Then you point curr back to prev and advance all three. "
            "When curr reaches the end, prev is the new head."
        ),
        "setting": "pointer_dance",
        "character": "Captain Byte",
        "intro_text": (
            "Reversing a linked list is the canonical pointer-manipulation problem. "
            "Three pointers, one pass, O(1) extra space. "
            "The key insight: always save the next node before you overwrite curr.next."
        ),
    },
    "discovery": {
        "title": "Learn the Steps",
        "visual_primitives": ["move", "trace", "compare"],
        "steps": [
            {
                "action": "three_pointers",
                "narration": "prev starts at None, curr at head, nxt saves curr.next before the link changes.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "prev = None\ncurr = head  # 1 -> 2 -> 3\nnxt = curr.next\nprint('prev:', prev, 'curr:', curr.val, 'nxt:', nxt.val if nxt else None)",
                    "expected_output": "prev: None curr: 1 nxt: 2",
                    "hint": "prev is None (nothing before head). curr is node 1. nxt is node 2.",
                },
            },
            {
                "action": "rewire",
                "narration": "Cut the forward link and point curr backward. Then advance all three.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "prev = None\ncurr = Node(1)\nnxt = curr.next  # Node(2)\ncurr.next = prev\nprev = curr\ncurr = nxt\nprint('prev:', prev.val, 'curr:', curr.val if curr else None)",
                    "expected_output": "prev: 1 curr: 2",
                    "hint": "curr.next = None (reversed). prev moves to node 1. curr moves to node 2.",
                },
            },
            {
                "action": "iterate",
                "narration": "Repeat until curr is None. prev is the new head.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "After reversing 1->2->3, what is the new head?",
                    "options": [
                        {"id": "a", "text": "Node 1", "correct": False},
                        {"id": "b", "text": "Node 2", "correct": False},
                        {"id": "c", "text": "Node 3", "correct": True},
                        {"id": "d", "text": "None", "correct": False},
                    ],
                    "explanation": "The last node processed becomes prev, which is the new head. That is node 3.",
                },
            },
            {
                "action": "edge_empty",
                "narration": "An empty list or single node is already reversed. The loop handles both.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "If head is None, what does the algorithm return?",
                    "options": [
                        {"id": "a", "text": "None", "correct": True},
                        {"id": "b", "text": "An error", "correct": False},
                        {"id": "c", "text": "Node(None)", "correct": False},
                        {"id": "d", "text": "Empty list", "correct": False},
                    ],
                    "explanation": "If head is None, prev stays None and the algorithm returns None.",
                },
            },
        ],
        "conclusion": (
            "Reversing a linked list requires three pointers and one pass. "
            "Save nxt before cutting curr.next, then advance all three. "
            "When curr is None, prev is the new head."
        ),
    },
    "prediction": {
        "title": "Before You Dance",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict the final state.”",
        "question": "After reversing 1 -> 2 -> 3 -> None, what is the new tail's next pointer?",
        "options": [
            {"id": "a", "text": "None", "correct": True, "explanation": "The new tail (old head) points to None."},
            {"id": "b", "text": "1", "correct": False, "explanation": "The old head becomes the tail and points to None."},
            {"id": "c", "text": "2", "correct": False, "explanation": "2 is in the middle."},
            {"id": "d", "text": "3", "correct": False, "explanation": "3 is the new head."},
        ],
        "explanation": "The old head (1) becomes the tail. Its next must be None.",
    },
    "explain": {
        "title": "Explain the Dance",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why must you save nxt before overwriting curr.next?”",
        "prompt": "Why must you save nxt before overwriting curr.next?",
        "answer_format": "short_answer",
        "keywords": ["save", "lose", "forward", "link", "nxt", "overwrite", "next", "before", "reference"],
        "min_words": 10,
        "model_answer": (
            "If you set curr.next = prev before saving nxt, you overwrite the forward link. "
            "You lose the reference to the rest of the list. Saving nxt preserves the forward "
            "chain so you can advance curr after reversing the link."
        ),
        "intention": "The explanation must show that losing nxt breaks the forward chain.",
    },
    "guided_build": {
        "title": "Write the Dance",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the three-pointer loop.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Reverse Linked List",
                "captain_byte_moment": "🧭 **Captain Byte**\n“prev, curr, nxt — the three partners. Save nxt first.”",
                "description": "Reverse a singly linked list and return the new head.",
                "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverse_list(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev\n",
                "function_name": "reverse_list",
                "signature": "def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:",
                "test_cases": [
                    {"input": ["[1,2,3,4,5]"], "expected": "[5,4,3,2,1]"},
                ],
                "hidden_test_cases": [
                    {"input": ["[]"], "expected": "[]"},
                    {"input": ["[1]"], "expected": "[1]"},
                    {"input": ["[1,2]"], "expected": "[2,1]"},
                ],
                "diamonds": 45,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use three pointers: prev, curr, nxt."},
                    {"level": 2, "text": "Save nxt = curr.next BEFORE changing curr.next."},
                    {"level": 3, "text": "curr.next = prev; prev = curr; curr = nxt. Return prev."},
                ],
            },
            {
                "step_order": 2,
                "title": "Reverse Between",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Reverse only positions left to right. The rest of the chain stays intact.”",
                "description": "Reverse the nodes of a linked list from position left to right.",
                "starter_code": "def reverse_between(head, left, right):\n    dummy = ListNode(0, head)\n    prev = dummy\n    for _ in range(left - 1):\n        prev = prev.next\n    curr = prev.next\n    for _ in range(right - left):\n        nxt = curr.next\n        curr.next = nxt.next\n        nxt.next = prev.next\n        prev.next = nxt\n    return dummy.next\n",
                "function_name": "reverse_between",
                "signature": "def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:",
                "test_cases": [
                    {"input": ["[1,2,3,4,5]", 2, 4], "expected": "[1,4,3,2,5]"},
                ],
                "hidden_test_cases": [
                    {"input": ["[5]", 1, 1], "expected": "[5]"},
                    {"input": ["[1,2,3,4,5]", 1, 5], "expected": "[5,4,3,2,1]"},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use a dummy node before head to simplify edge cases."},
                    {"level": 2, "text": "Move prev to the node before position left."},
                    {"level": 3, "text": "Insert each node between prev and prev.next by rewiring three pointers."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Palindrome Check",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same chain, different question. Is it a palindrome?”",
        "description": (
            "Determine if a singly linked list is a palindrome. "
            "Use O(n) time and O(1) extra space."
        ),
        "function_name": "is_palindrome",
        "signature": "def is_palindrome(head: Optional[ListNode]) -> bool:",
        "description_full": (
            "Return True if the linked list values form a palindrome.\n\n"
            "Example:\n"
            "  1 -> 2 -> 2 -> 1 is a palindrome\n"
            "  1 -> 2 -> 3 is not\n\n"
            "Hint: reverse the second half, then compare."
        ),
        "test_cases": [
            {"input": ["[1,2,2,1]"], "expected": True},
            {"input": ["[1,2]"], "expected": False},
        ],
        "hidden_test_cases": [
            {"input": ["[1]"], "expected": True},
            {"input": ["[1,0,1]"], "expected": True},
            {"input": ["[1,2,3,2,1]"], "expected": True},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Find the middle with slow and fast pointers."},
            {"level": 2, "text": "Reverse the second half of the list."},
            {"level": 3, "text": "Compare the first half with the reversed second half."},
        ],
    },
    "assessment": {
        "title": "Pointer Dance Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you can rewire any chain. Timed.”",
        "description": "Reverse a list, explain the pointer order, and fix a lost-node bug.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "head = ListNode(1, ListNode(2, ListNode(3)))\nprev = None\ncurr = head\nwhile curr:\n    nxt = curr.next\n    curr.next = prev\n    prev = curr\n    curr = nxt\nprint(prev.val if prev else None, prev.next.val if prev and prev.next else None)",
                "answer_format": "single_choice",
                "expected_answer": "3 2",
                "options": [
                    {"id": "a", "text": "3 2", "correct": True},
                    {"id": "b", "text": "1 2", "correct": False},
                    {"id": "c", "text": "2 3", "correct": False},
                    {"id": "d", "text": "None", "correct": False},
                ],
                "explanation": "After reversal, prev is node 3, and prev.next is node 2.",
            },
            {
                "type": "concept",
                "question": "Why does reversing a linked list require O(1) extra space?",
                "answer_format": "short_answer",
                "keywords": ["pointer", "rewire", "in-place", "three", "prev", "curr", "nxt", "no", "extra"],
                "explanation": "Only three pointers are needed regardless of list length. The links are rewired in place.",
            },
            {
                "type": "debug",
                "code": "def reverse_list(head):\n    prev = None\n    curr = head\n    while curr:\n        curr.next = prev\n        prev = curr\n        curr = curr.next\n    return prev\n# should reverse the list",
                "error": "reverse_list([1,2,3]) crashes or loops forever because nxt is never saved.",
                "question": "Fix the lost-node bug.",
                "fix": "nxt = curr.next\ncurr.next = prev\nprev = curr\ncurr = nxt",
                "explanation": "curr.next = prev overwrites the forward link. Saving nxt first preserves the rest of the list.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Lost Chain",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I broke the dance on purpose. Find the lost node.”",
        "story": (
            "A programmer reversed a list but forgot to save nxt. After the first iteration, "
            "the rest of the chain is lost. Find the wrong assumption."
        ),
        "buggy_code": "def reverse_list(head):\n    prev = None\n    curr = head\n    while curr:\n        curr.next = prev\n        prev = curr\n        curr = curr.next\n    return prev\n",
        "expected_output": "[3, 2, 1]",
        "actual_output": "Only the first node is reversed; the rest of the list is lost",
        "diagnosis": {
            "question": "Which assumption makes this reversal lose the rest of the chain?",
            "options": [
                {"id": "a", "text": "curr.next is overwritten before saving nxt", "correct": True, "why": "After curr.next = prev, the forward link is gone. curr.next now points to prev, not the next node."},
                {"id": "b", "text": "prev should start at head", "correct": False, "why": "prev must start at None to make the old head the new tail."},
                {"id": "c", "text": "The loop condition is wrong", "correct": False, "why": "while curr works correctly."},
                {"id": "d", "text": "The return value is wrong", "correct": False, "why": "Returning prev is correct; prev becomes the new head."},
            ],
        },
        "fix": "nxt = curr.next",
        "fixed_code": "def reverse_list(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev\n",
        "explanation": (
            "Overwriting curr.next before saving nxt severs the forward chain. "
            "Saving nxt first preserves the rest of the list so you can continue walking it."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:linked_list:reverse",
        "concept_name": "Reverse Linked List",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "use three pointers: prev, curr, nxt",
            "save nxt before changing curr.next",
            "rewire curr.next = prev",
            "advance all three pointers",
            "return prev as the new head",
        ],
        "spaced_fields": [
            "three_pointers",
            "save_nxt",
            "rewire_link",
            "advance_all",
            "return_prev",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "reverse_linked_list",
        "unlocks_next": ["linked_list_advanced"],
        "tower_badge": "pointer_dance",
        "world_node": {
            "level": 19,
            "title": "The Pointer Dance",
            "color": "teal",
            "icon": "🔗",
            "description": "Reverse a singly linked list in O(n) time and O(1) space",
        },
    },
}
