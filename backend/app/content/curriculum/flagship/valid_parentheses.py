"""
Flagship Lesson — Valid Parentheses
 =====================================

 Gold-standard interactive lesson for the stack-based parentheses validator.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "valid_parentheses"

LESSON: Dict[str, Any] = {
    "lesson_id": "valid_parentheses_stack_gate",
    "module_id": "dsa:stack:valid_parentheses",
    "title": "The Stack Gate",
    "description": "Validate bracket sequences using a stack. Open pushes, close pops, mismatch fails.",
    "difficulty": "intermediate",
    "est_minutes": 14,
    "xp_reward": 120,
    "skills_taught": ["stack", "valid_parentheses", "balanced_brackets"],
    "srs_concept_tag": "dsa:stack:valid_parentheses",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Stack Gate checks every bracket pair in order. Open brackets push onto the stack. "
            "Close brackets must match the top of the stack. If they do not, the gate fails. "
            "At the end, the stack must be empty.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You pushed opens and matched closes.”",
            "🧭 **Captain Byte**\n“Clean. The stack is empty at the end.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t count brackets. Track the ORDER with a stack.”",
            "🧭 **Captain Byte**\n“You’re missing a close. The stack must be empty at the end.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now match the closes correctly.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any bracket-validation problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Push opens, match closes, empty stack at the end.”",
    },
    "story_context": {
        "title": "The Stack Gate",
        "narration": (
            "The Stack Gate checks every bracket pair in order. Open brackets push onto the stack. "
            "Close brackets must match the top of the stack. If they do not, the gate fails. "
            "At the end, the stack must be empty."
        ),
        "setting": "stack_gate",
        "character": "Captain Byte",
        "intro_text": (
            "A stack reverses order. The last opening bracket must be closed first. "
            "Use this property to validate any bracket sequence in linear time."
        ),
    },
    "discovery": {
        "title": "Pass Through the Gate",
        "visual_primitives": ["move", "compare", "trace"],
        "steps": [
            {
                "action": "push_open",
                "narration": "Every open bracket is a ticket. You stack them in order.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "stack = []\nstack.append('(')\nstack.append('[')\nprint(stack)",
                    "expected_output": "['(', '[']",
                    "hint": "append adds to the top of the stack. The last element is the most recent open.",
                },
            },
            {
                "action": "pop_match",
                "narration": "A close bracket must match the top open. If it does not, the gate fails.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "Stack top is '('. Next char is ']'. What happens?",
                    "options": [
                        {"id": "a", "text": "Pop '(' and continue", "correct": False},
                        {"id": "b", "text": "Gate fails — mismatch", "correct": True},
                        {"id": "c", "text": "Push ']' onto the stack", "correct": False},
                        {"id": "d", "text": "Ignore the ']'", "correct": False},
                    ],
                    "explanation": "'(' and ']' do not match. The gate fails immediately.",
                },
            },
            {
                "action": "empty_at_end",
                "narration": "After processing every character, the stack must be empty. Any remaining opens are unmatched.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "After processing '(()', the stack contains ['(']. Is the sequence valid?",
                    "options": [
                        {"id": "a", "text": "Yes, all closes matched", "correct": False},
                        {"id": "b", "text": "No — unmatched open remains", "correct": True},
                        {"id": "c", "text": "Yes, because there are no mismatches", "correct": False},
                        {"id": "d", "text": "Depends on the closing bracket type", "correct": False},
                    ],
                    "explanation": "An open with no matching close makes the sequence invalid.",
                },
            },
            {
                "action": "map_pairs",
                "narration": "Map each close bracket to its matching open. The map is the gate’s rulebook.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "pairs = {')': '(', ']': '[', '}': '{'}\nprint(pairs[']'])",
                    "expected_output": "[",
                    "hint": "The dictionary maps each close bracket to its matching open.",
                },
            },
        ],
        "conclusion": (
            "A stack validates bracket sequences in one pass. "
            "Push opens, match closes against the top, and ensure the stack is empty at the end."
        ),
    },
    "prediction": {
        "title": "Before You Push",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict whether this sequence passes.”",
        "question": "Is the sequence '([{}])' valid?",
        "options": [
            {"id": "a", "text": "Yes", "correct": True, "explanation": "Each close matches the most recent open. Stack empties at the end."},
            {"id": "b", "text": "No", "correct": False, "explanation": "All brackets match correctly."},
            {"id": "c", "text": "Only if brackets are of the same type", "correct": False, "explanation": "Different types are valid if properly nested."},
            {"id": "d", "text": "Depends on the order of opening", "correct": False, "explanation": "The given order is valid."},
        ],
        "explanation": "([{}]) nests correctly: ( contains [ contains { }, then ], then ), then ]. Stack empties.",
    },
    "explain": {
        "title": "Explain the Stack Rule",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why is a stack the right data structure for bracket validation?”",
        "prompt": "Why is a stack the right data structure for bracket validation?",
        "answer_format": "short_answer",
        "keywords": ["last", "first", "lifo", "reverse", "order", "match", "top", "nest", "close", "open"],
        "min_words": 10,
        "model_answer": (
            "A stack is LIFO: the last open bracket pushed must be the first one closed. "
            "Bracket validation requires matching each close bracket to the most recent unmatched open, "
            "which is exactly what a stack provides."
        ),
        "intention": "The explanation must connect LIFO order to bracket matching.",
    },
    "guided_build": {
        "title": "Write the Gatekeeper",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the validator. Stack, map, loop.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Valid Parentheses",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Push opens, match closes, empty stack at the end.”",
                "description": "Return True if the bracket string is valid, False otherwise.",
                "starter_code": "def is_valid(s):\n    stack = []\n    pairs = {')': '(', ']': '[', '}': '{'}\n    for c in s:\n        if c in pairs.values():\n            stack.append(c)\n        elif c in pairs:\n            if not stack or stack[-1] != pairs[c]:\n                return False\n            stack.pop()\n    return not stack\n",
                "function_name": "is_valid",
                "signature": "def is_valid(s: str) -> bool:",
                "test_cases": [
                    {"input": ["()"], "expected": True},
                    {"input": ["()[]{}"], "expected": True},
                    {"input": ["(]"], "expected": False},
                ],
                "hidden_test_cases": [
                    {"input": ["([)]"], "expected": False},
                    {"input": ["{[]}"], "expected": True},
                    {"input": ["["], "expected": False},
                    {"input": ["]["], "expected": False},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use a list as a stack: append to push, pop() to remove top."},
                    {"level": 2, "text": "Map each close bracket to its matching open with a dictionary."},
                    {"level": 3, "text": "At the end, the stack must be empty: return not stack."},
                ],
            },
            {
                "step_order": 2,
                "title": "Min Stack",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Track the minimum in O(1). Every push updates the min stack.”",
                "description": "Design a stack that supports push, pop, top, and getMin in O(1) time.",
                "starter_code": "class MinStack:\n    def __init__(self):\n        self.stack = []\n        self.min_stack = []\n\n    def push(self, val):\n        self.stack.append(val)\n        if not self.min_stack or val <= self.min_stack[-1]:\n            self.min_stack.append(val)\n\n    def pop(self):\n        if self.stack.pop() == self.min_stack[-1]:\n            self.min_stack.pop()\n\n    def top(self):\n        return self.stack[-1]\n\n    def getMin(self):\n        return self.min_stack[-1]\n",
                "function_name": None,
                "signature": "class MinStack",
                "test_cases": [],
                "hidden_test_cases": [],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Maintain a second stack that tracks minimums."},
                    {"level": 2, "text": "Push to min_stack only when the new value is <= current min."},
                    {"level": 3, "text": "Pop from min_stack when the popped value equals the current min."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Daily Temperature",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same stack idea, different problem. Wait for a warmer day.”",
        "description": (
            "Given daily temperatures, return an array where each element is the number of days "
            "until a warmer temperature. If none, use 0."
        ),
        "function_name": "daily_temperatures",
        "signature": "def daily_temperatures(temps: List[int]) -> List[int]:",
        "description_full": (
            "Return an array of days until a warmer temperature.\n\n"
            "Example:\n"
            "  daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) -> [1, 1, 4, 2, 1, 1, 0, 0]"
        ),
        "test_cases": [
            {"input": [[73, 74, 75, 71, 69, 72, 76, 73]], "expected": [1, 1, 4, 2, 1, 1, 0, 0]},
        ],
        "hidden_test_cases": [
            {"input": [[30, 40, 50, 60]], "expected": [1, 1, 1, 0]},
            {"input": [[30, 20, 10]], "expected": [0, 0, 0]},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Use a stack to track indices of decreasing temperatures."},
            {"level": 2, "text": "When a warmer temp arrives, pop all colder temps and record the gap."},
            {"level": 3, "text": "Store indices on the stack, not values."},
        ],
    },
    "assessment": {
        "title": "Stack Gate Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove the stack is second nature. Timed.”",
        "description": "Validate brackets, explain LIFO, and fix a stack underflow.",
        "questions": [
            {
                "type": "concept",
                "question": "Why must a stack be empty at the end of bracket validation?",
                "answer_format": "short_answer",
                "keywords": ["empty", "unmatched", "open", "close", "remaining", "stack"],
                "explanation": "Any remaining opens are unmatched closes. The stack must be empty for full validity.",
            },
            {
                "type": "code_tracing",
                "code": "s = \"{[]}\"\nstack = []\npairs = {'}': '{', ')': '(', ']': '['}\nfor c in s:\n    if c in '{[(':\n        stack.append(c)\n    else:\n        if not stack or stack[-1] != pairs[c]:\n            print(False)\n            break\n        stack.pop()\nelse:\n    print(not stack)",
                "answer_format": "single_choice",
                "expected_answer": "True",
                "options": [
                    {"id": "a", "text": "True", "correct": True},
                    {"id": "b", "text": "False", "correct": False},
                ],
                "explanation": "Each close matches its open. Stack empties at the end. Sequence is valid.",
            },
            {
                "type": "debug",
                "code": "def is_valid(s):\n    stack = []\n    pairs = {')': '(', ']': '[', '}': '{'}\n    for c in s:\n        if c in '({[':\n            stack.append(c)\n        if c in ')}]':\n            if stack[-1] != pairs[c]:\n                return False\n            stack.pop()\n    return True\n",
                "error": "is_valid(')(') crashes with IndexError instead of returning False.",
                "question": "Fix the stack underflow and the final check.",
                "fix": "if not stack or stack[-1] != pairs[c]:\n            return False\n    return not stack",
                "explanation": "Check that the stack is non-empty before accessing stack[-1]. Return not stack at the end.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Mismatched Close",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I broke the validator. Find the unsafe assumption.”",
        "story": (
            "A validator accepted '([)]' as valid because it only counted brackets, "
            "not their order. What assumption is wrong?"
        ),
        "buggy_code": "def is_valid(s):\n    count = {}\n    for c in s:\n        count[c] = count.get(c, 0) + 1\n    return count.get('(', 0) == count.get(')', 0)\n",
        "expected_output": "False",
        "actual_output": "True — it only counts, ignoring order",
        "diagnosis": {
            "question": "Which assumption makes this validator unsafe?",
            "options": [
                {"id": "a", "text": "It assumes equal counts guarantee correct nesting order", "correct": True, "why": "Equal counts do not ensure proper nesting; '([)]' has equal counts but wrong order."},
                {"id": "b", "text": "It uses a dict instead of a stack", "correct": False, "why": "The data structure is not the core issue; the logic is."},
                {"id": "c", "text": "It returns True too early", "correct": False, "why": "The return happens after the loop, not too early."},
                {"id": "d", "text": "It does not handle empty strings", "correct": False, "why": "Empty strings would pass both implementations."},
            ],
        },
        "fix": "Use a stack to track opens; match each close to the top of the stack.",
        "fixed_code": "def is_valid(s):\n    stack = []\n    pairs = {')': '(', ']': '[', '}': '{'}\n    for c in s:\n        if c in '({[':\n            stack.append(c)\n        elif c in ')}]':\n            if not stack or stack[-1] != pairs[c]:\n                return False\n            stack.pop()\n    return not stack\n",
        "explanation": (
            "Equal counts do not enforce nesting order. A stack tracks the order of opens, "
            "so every close matches the most recent unmatched open."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:stack:valid_parentheses",
        "concept_name": "Valid Parentheses",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "use a stack to track open brackets",
            "map each close bracket to its matching open",
            "mismatch or empty stack on close means invalid",
            "stack must be empty at the end",
        ],
        "spaced_fields": [
            "push_opens",
            "match_closes",
            "lifo_order",
            "empty_at_end",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "valid_parentheses",
        "unlocks_next": ["stack_patterns"],
        "tower_badge": "stack_gate",
        "world_node": {
            "level": 21,
            "title": "The Stack Gate",
            "color": "teal",
            "icon": "🚪",
            "description": "Validate bracket sequences using a stack in O(n)",
        },
    },
}
