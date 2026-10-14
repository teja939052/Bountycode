"""
Flagship Lesson — Two Sum
 ==========================

 Gold-standard interactive lesson for the hash-map two-sum pattern.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "two_sum"

LESSON: Dict[str, Any] = {
    "lesson_id": "two_sum_complement_map",
    "module_id": "dsa:hash_map:two_sum",
    "title": "The Complement Ledger",
    "description": "Find two numbers that sum to a target using a hash map for O(n) lookup.",
    "difficulty": "intermediate",
    "est_minutes": 14,
    "xp_reward": 120,
    "skills_taught": ["hash_map", "two_sum", "complement_lookup"],
    "srs_concept_tag": "dsa:hash_map:two_sum",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Complement Ledger remembers every number you have seen. "
            "For each new number, it checks whether its complement — target minus that number — "
            "is already in the ledger. If yes, the pair is found. No nested loops. O(n).”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You stored the complement and looked it up instantly.”",
            "🧭 **Captain Byte**\n“Clean. The hash map turns O(n²) into O(n).”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t scan the array again. What did you already store?”",
            "🧭 **Captain Byte**\n“You’re doing nested loops. The hash map removes the inner loop.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now use the map correctly.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any complement-lookup problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Store what you need, then look it up in O(1).”",
    },
    "story_context": {
        "title": "The Complement Ledger",
        "narration": (
            "The Complement Ledger remembers every number you have seen. "
            "For each new number, it checks whether its complement — target minus that number — "
            "is already in the ledger. If yes, the pair is found. No nested loops. O(n)."
        ),
        "setting": "complement_ledger",
        "character": "Captain Byte",
        "intro_text": (
            "Two Sum is the canonical hash-map pattern. "
            "Instead of checking every pair, you remember what you have seen and "
            "ask: is the partner for this number already here?"
        ),
    },
    "discovery": {
        "title": "Read the Ledger",
        "visual_primitives": ["highlight", "compare", "trace"],
        "steps": [
            {
                "action": "complement_idea",
                "narration": "For each number x, the partner is target - x. If the partner is already seen, the pair is found.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "target = 9\nseen = {}\nfor x in [2, 7, 11, 15]:\n    partner = target - x\n    print(f'x={x}, partner={partner}, seen={seen}')\n    if partner in seen:\n        print('Found:', partner, x)\n    seen[x] = True",
                    "expected_output": "x=2, partner=7, seen={}\nx=7, partner=2, seen={2: True}\nFound: 2 7",
                    "hint": "When x = 7, partner = 2. 2 is already in seen. Pair found.",
                },
            },
            {
                "action": "dict_lookup",
                "narration": "A dictionary gives O(1) lookup. 'partner in seen' is instant.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "seen = {2: True, 7: True}. Is 2 in seen?",
                    "options": [
                        {"id": "a", "text": "Yes", "correct": True},
                        {"id": "b", "text": "No", "correct": False},
                        {"id": "c", "text": "Only if the value is True", "correct": False},
                        {"id": "d", "text": "Only if the key is first", "correct": False},
                    ],
                    "explanation": "'key in dict' checks keys only. 2 is a key, so it is found.",
                },
            },
            {
                "action": "why_not_nested",
                "narration": "A nested loop checks every pair: O(n²). The hash map stores seen numbers and checks in O(1).",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "For nums = [1, 2, 3, 4, 5], how many pairs does a nested loop check?",
                    "options": [
                        {"id": "a", "text": "5", "correct": False},
                        {"id": "b", "text": "10", "correct": True},
                        {"id": "c", "text": "25", "correct": False},
                        {"id": "d", "text": "20", "correct": False},
                    ],
                    "explanation": "n*(n-1)/2 = 10 pairs for 5 elements. O(n²).",
                },
            },
            {
                "action": "one_pass",
                "narration": "The hash map approach is one pass: O(n) time, O(n) space.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def two_sum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        partner = target - x\n        if partner in seen:\n            return [seen[partner], i]\n        seen[x] = i\n    return []\nprint(two_sum([2, 7, 11, 15], 9))",
                    "expected_output": "[0, 1]",
                    "hint": "At i=1, x=7, partner=2. 2 is in seen at index 0. Return [0, 1].",
                },
            },
        ],
        "conclusion": (
            "Two Sum is the canonical hash-map pattern. "
            "Store what you have seen; for each new number, ask whether its complement is already there."
        ),
    },
    "prediction": {
        "title": "Before You Map",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict the first pair.”",
        "question": "nums = [3, 5, 2, 8], target = 10. Which pair is found first?",
        "options": [
            {"id": "a", "text": "(2, 8)", "correct": True, "explanation": "3→seen{3}, 5→seen{3,5}, 2→partner=8 not in seen, seen{3,5,2}. 8→partner=2 in seen. Pair (2,8) at indices (2,3)."},
            {"id": "b", "text": "(5, 5)", "correct": False, "explanation": "No duplicate 5 in the array."},
            {"id": "c", "text": "(3, 7)", "correct": False, "explanation": "7 is not in the array."},
            {"id": "d", "text": "(8, 2)", "correct": False, "explanation": "8 comes after 2, so (2,8) is found first."},
        ],
        "explanation": "The hash map finds (2, 8) first because 2 is seen before 8 arrives.",
    },
    "explain": {
        "title": "Explain the Complement",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does storing complements turn O(n²) into O(n)?”",
        "prompt": "Why does storing complements turn O(n²) into O(n)?",
        "answer_format": "short_answer",
        "keywords": ["hash", "map", "dict", "o(1)", "lookup", "store", "complement", "once", "pass", "nested"],
        "min_words": 10,
        "model_answer": (
            "A nested loop checks every pair, giving O(n²). A hash map stores each number once. "
            "For each new number, we check whether its complement exists in the map in O(1). "
            "One pass, O(n) total."
        ),
        "intention": "The explanation must connect single-pass storage to O(1) lookup.",
    },
    "guided_build": {
        "title": "Write the Ledger",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the one-pass solution.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Two Sum",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Store numbers as you go. Ask for the complement in O(1).”",
                "description": "Return indices of two numbers that sum to target.",
                "starter_code": "def two_sum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        partner = target - x\n        if partner in seen:\n            return [seen[partner], i]\n        seen[x] = i\n    return []\n",
                "function_name": "two_sum",
                "signature": "def two_sum(nums: List[int], target: int) -> List[int]:",
                "test_cases": [
                    {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                    {"input": [[3, 2, 4], 6], "expected": [1, 2]},
                ],
                "hidden_test_cases": [
                    {"input": [[3, 3], 6], "expected": [0, 1]},
                    {"input": [[1, 5, 3, 7], 8], "expected": [1, 3]},
                    {"input": [[0, 4, 3, 0], 0], "expected": [0, 3]},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "Use a dict to store number -> index."},
                    {"level": 2, "text": "For each x, partner = target - x. Check if partner is in seen."},
                    {"level": 3, "text": "Store seen[x] = i AFTER checking, so you don’t reuse the same element."},
                ],
            },
            {
                "step_order": 2,
                "title": "Contains Duplicate II",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Same map, different question. Within k distance.”",
                "description": "Return True if there are two equal numbers within k indices of each other.",
                "starter_code": "def contains_nearby_duplicate(nums, k):\n    seen = {}\n    for i, x in enumerate(nums):\n        if x in seen and i - seen[x] <= k:\n            return True\n        seen[x] = i\n    return False\n",
                "function_name": "contains_nearby_duplicate",
                "signature": "def contains_nearby_duplicate(nums: List[int], k: int) -> bool:",
                "test_cases": [
                    {"input": [[1, 2, 3, 1], 3], "expected": True},
                    {"input": [[1, 0, 1, 1], 1], "expected": True},
                ],
                "hidden_test_cases": [
                    {"input": [[1, 2, 3, 4, 5, 6], 2], "expected": False},
                    {"input": [[1, 1], 1], "expected": True},
                ],
                "diamonds": 45,
                "scaffolded_hints": [
                    {"level": 1, "text": "Store the last index of each number."},
                    {"level": 2, "text": "When you see a duplicate, check if the index gap is <= k."},
                    {"level": 3, "text": "Always update seen[x] = i to keep the most recent index."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Anagram Check",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same hash-map idea. Count characters, not numbers.”",
        "description": (
            "Return True if two strings are anagrams of each other. "
            "An anagram has the same characters with the same counts."
        ),
        "function_name": "is_anagram",
        "signature": "def is_anagram(s: str, t: str) -> bool:",
        "description_full": (
            "Return True if t is an anagram of s.\n\n"
            "Example:\n"
            "  is_anagram('anagram', 'nagaram') -> True\n\n"
            "Use a hash map (collections.Counter or manual dict) to count characters."
        ),
        "test_cases": [
            {"input": ["anagram", "nagaram"], "expected": True},
            {"input": ["rat", "car"], "expected": False},
        ],
        "hidden_test_cases": [
            {"input": ["a", "a"], "expected": True},
            {"input": ["ab", "a"], "expected": False},
        ],
        "time_limit_minutes": 7,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Count characters in s, then decrement for t."},
            {"level": 2, "text": "If any count goes negative or a char is missing, not an anagram."},
            {"level": 3, "text": "Shortcut: return Counter(s) == Counter(t)"},
        ],
    },
    "assessment": {
        "title": "Complement Ledger Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove the hash-map pattern is automatic. Timed.”",
        "description": "Find the pair, explain O(n), and fix a nested-loop attempt.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "nums = [3, 5, 2, 8]\ntarget = 10\nseen = {}\nfor i, x in enumerate(nums):\n    partner = target - x\n    if partner in seen:\n        print(seen[partner], i)\n        break\n    seen[x] = i",
                "answer_format": "single_number",
                "expected_answer": "2 3",
                "explanation": "At i=2, x=2, partner=8 not in seen. seen{3:0, 5:1, 2:2}. At i=3, x=8, partner=2 in seen at index 2. Print 2 3.",
            },
            {
                "type": "concept",
                "question": "What is the time complexity of the hash-map two-sum approach?",
                "answer_format": "short_answer",
                "keywords": ["o(n)", "linear", "one pass", "single pass", "hash", "dict"],
                "explanation": "One pass through the array with O(1) dict lookups gives O(n) total.",
            },
            {
                "type": "debug",
                "code": "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []\n# should be O(n), not O(n^2)",
                "error": "two_sum on large input times out. O(n²) is too slow.",
                "question": "Replace the nested loop with a hash-map approach.",
                "fix": "seen = {}\nfor i, x in enumerate(nums):\n    partner = target - x\n    if partner in seen:\n        return [seen[partner], i]\n    seen[x] = i\nreturn []",
                "explanation": "A hash map replaces the inner loop with O(1) lookup, reducing total time to O(n).",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Reused Element",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I broke the ledger on purpose. Find the wrong assumption.”",
        "story": (
            "A student stored the current element in seen before checking the complement. "
            "On [3, 3] with target 6, the same element pairs with itself. Find the wrong assumption."
        ),
        "buggy_code": "def two_sum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        seen[x] = i\n        partner = target - x\n        if partner in seen:\n            return [seen[partner], i]\n    return []\n",
        "expected_output": "[0, 1]",
        "actual_output": "[0, 0] on [3, 3] — the element pairs with itself",
        "diagnosis": {
            "question": "Which assumption makes this solution reuse the same element?",
            "options": [
                {"id": "a", "text": "The element is stored in seen before checking the complement", "correct": True, "why": "Storing first means x can match with itself if x + x = target."},
                {"id": "b", "text": "The target is even", "correct": False, "why": "Target parity is irrelevant; the issue is the store order."},
                {"id": "c", "text": "The array contains duplicates", "correct": False, "why": "Duplicates are allowed; the issue is self-matching."},
                {"id": "d", "text": "The dict lookup is O(n)", "correct": False, "why": "Dict lookup is O(1); the logic order is the bug."},
            ],
        },
        "fix": "Check partner in seen BEFORE storing x in seen.",
        "fixed_code": "def two_sum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        partner = target - x\n        if partner in seen:\n            return [seen[partner], i]\n        seen[x] = i\n    return []\n",
        "explanation": (
            "Storing x before checking allows x to match with itself. "
            "Checking first ensures the complement is a PREVIOUS element, not the current one."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:hash_map:two_sum",
        "concept_name": "Two Sum",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "use a hash map to store seen numbers",
            "for each x, complement = target - x",
            "check complement in seen BEFORE storing x",
            "O(n) time, O(n) space",
        ],
        "spaced_fields": [
            "hash_map_storage",
            "complement_check",
            "store_after_check",
            "one_pass",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "two_sum",
        "unlocks_next": ["hash_map_patterns"],
        "tower_badge": "complement_ledger",
        "world_node": {
            "level": 13,
            "title": "The Complement Ledger",
            "color": "teal",
            "icon": "🗺️",
            "description": "Find two numbers summing to target in O(n) with a hash map",
        },
    },
}
