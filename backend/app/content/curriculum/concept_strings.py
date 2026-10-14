"""
Concept Clarity Slice: Strings & Immutability
=============================================

One exceptional hands-on lesson for the concept: text as sequences.

Misconceptions attacked:
  1. "I can change one letter of a string" — strings are immutable; you build a new one
  2. slicing s[a:b] includes b — it stops BEFORE b (same rule as range)
  3. '+' builds a fresh string every time, so reuse is worse than you think (bridges into complexity)
"""
from typing import Dict, Any

STRING_SLICE: Dict[str, Any] = {
    "lesson_id": "strings_stringed_loom",
    "module_id": "programming_fundamentals:strings",
    "title": "The Stringed Loom",
    "description": "Learn how text is stored as character threads that cannot be cut — only rewoven.",
    "difficulty": "beginner",
    "est_minutes": 12,
    "xp_reward": 200,
    "skills_taught": ["strings", "string_methods", "types", "input_output"],
    "srs_concept_tag": "programming_fundamentals:strings",
    "story_context": {
        "title": "The Stringed Loom",
        "narration": (
            "On the third hill a loom weaves words from single threads. Each thread is one "
            "character, and the whole word is a length of cloth called a string. Here is "
            "the loom's secret rule: once a cloth is woven you cannot unpick a single "
            "thread — to change one letter you must weave an entirely new cloth."
        ),
        "setting": "stringed_loom",
        "character": "Weaver",
        "intro_text": (
            "Welcome, apprentice. A string is a sequence of characters, numbered from 0 "
            "like shelves. Read it, count it, cut a piece of it — but to change it, "
            "you reweave. Let me show you."
        ),
    },
    "discovery": {
        "title": "Threads of the Cloth",
        "steps": [
            {
                "action": "read_threads",
                "narration": (
                    "A word is a row of character threads. Like list shelves, the first "
                    "thread is at index 0. len() counts the whole cloth."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": 'word = "hello"\nprint(word[0])\nprint(len(word))',
                    "expected_output": "h\n5",
                    "hint": "word[0] is 'h'. len('hello') is 5 — h,e,l,l,o.",
                },
            },
            {
                "action": "try_rewrite",
                "narration": "Now try to fix a typo by replacing one thread in place. Watch what happens.",
                "interaction": {
                    "type": "inspect_code",
                    "code": 'word = "hollo"\nword[1] = "e"',
                    "expected_output": "TypeError: 'str' object does not support item assignment",
                    "hint": "Strings refuse to change in place. That error IS the immutability rule in action.",
                },
            },
            {
                "action": "cut_cloth",
                "narration": (
                    "To take a piece of cloth, you cut a slice. The cut takes threads "
                    "from index a up to — but never including — index b."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": 'word = "hello"\nprint(word[1:4])\nprint(word[:3])',
                    "expected_output": "ell\nhel",
                    "hint": "word[1:4] = e,l,l — the b (index 4) is not included, same rule as range.",
                },
            },
        ],
        "conclusion": (
            "Strings are sequences of characters indexed from 0. They are immutable: you "
            "cannot change a character in place — you build a new string. Slicing "
            "s[a:b] stops before b."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "question": "What does this code print?",
        "code": 's = "bounty"\nchunk = s[1:4]\nprint(chunk)',
        "options": [
            {"id": "a", "text": "oun", "correct": True, "explanation": "s[1:4] = b,o,u,n,t,y → indexes 1,2,3 = o,u,n. Index 4 is excluded."},
            {"id": "b", "text": "ount", "correct": False, "explanation": "ount would need s[1:5] — the slice never includes index 4."},
            {"id": "c", "text": "un", "correct": False, "explanation": "un skips the first character; the slice starts at index 1, not 2."},
            {"id": "d", "text": "Error", "correct": False, "explanation": "Slicing is always legal — no error here."},
        ],
        "explanation": (
            "b(o)(u)(n)(t)(y): s[1:4] takes o, u, n — stop before index 4. "
            "The same 'stop before the end' rule you learned for range() applies to slicing."
        ),
    },
    "guided_build": {
        "title": "Weave Some Cloth",
        "steps": [
            {
                "step_order": 1,
                "title": "Count the Vowel Threads",
                "description": "Return the number of vowels (a, e, i, o, u) in a piece of text. Case does not matter.",
                "starter_code": """def count_vowels(text):
    # walk over each character
    # count it if it is a, e, i, o, or u (case-insensitive)
    pass""",
                "function_name": "count_vowels",
                "signature": "def count_vowels(text: str) -> int:",
                "test_cases": [
                    {"input": ["hello"], "expected": 2},
                    {"input": ["rhythm"], "expected": 0},
                ],
                "hidden_test_cases": [
                    {"input": ["BOUNTY"], "expected": 2},
                    {"input": [""], "expected": 0},
                    {"input": ["aeiou"], "expected": 5},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "Loop with for ch in text. Compare ch.lower() so 'A' counts as 'a'."},
                    {"level": 2, "text": "Use a set or string of vowels: if ch.lower() in 'aeiou'."},
                    {"level": 3, "text": "An empty string simply yields 0 — the loop never runs."},
                ],
            },
            {
                "step_order": 2,
                "title": "The Mirror Cloth",
                "description": "Return True if the text reads the same forwards and backwards.",
                "starter_code": """def is_palindrome(text):
    # a palindrome is equal to its own reverse
    # compare text to text[::-1]
    pass""",
                "function_name": "is_palindrome",
                "signature": "def is_palindrome(text: str) -> bool:",
                "test_cases": [
                    {"input": ["racecar"], "expected": True},
                    {"input": ["hello"], "expected": False},
                ],
                "hidden_test_cases": [
                    {"input": [""], "expected": True},
                    {"input": ["a"], "expected": True},
                    {"input": ["level"], "expected": True},
                    {"input": ["abc"], "expected": False},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "text[::-1] creates the reversed copy with a full slice."},
                    {"level": 2, "text": "A palindrome satisfies text == text[::-1]."},
                    {"level": 3, "text": "Empty and single-character strings are palindromes by definition."},
                ],
            },
            {
                "step_order": 3,
                "title": "Capitalise the Cloth",
                "description": "Return a new string with every word's first letter capitalised and the rest lowercased.",
                "starter_code": """def title_case(text):
    # split into words, capitalise each, join with spaces
    pass""",
                "function_name": "title_case",
                "signature": "def title_case(text: str) -> str:",
                "test_cases": [
                    {"input": ["hello world"], "expected": "Hello World"},
                    {"input": ["bounty code"], "expected": "Bounty Code"},
                ],
                "hidden_test_cases": [
                    {"input": [""], "expected": ""},
                    {"input": ["a"], "expected": "A"},
                    {"input": ["one two three"], "expected": "One Two Three"},
                ],
                "diamonds": 60,
                "scaffolded_hints": [
                    {"level": 1, "text": "words = text.split() breaks on spaces."},
                    {"level": 2, "text": "w.capitalize() uppercases the first letter and lowers the rest."},
                    {"level": 3, "text": "Join back with ' '.join(...). Empty text splits to an empty list — join gives ''."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "Find the Pattern in the Cloth",
        "description": (
            "The weaver repeats a motif inside a long cloth. Find where a pattern first "
            "appears WITHOUT using s.find — hand-build the search with loops and slices."
        ),
        "function_name": "first_occurrence",
        "signature": "def first_occurrence(s: str, sub: str) -> int:",
        "description_full": (
            "Return the lowest index i such that the slice starting at i matches sub. "
            "If sub never appears, return -1.\n\n"
            "Examples:\n"
            "  first_occurrence(\"hello\", \"ll\")  -> 2\n"
            "  first_occurrence(\"hello\", \"z\")   -> -1\n"
            "  first_occurrence(\"abcabc\", \"abc\") -> 0\n\n"
            "Do not call s.find or s.index — write the loop yourself, comparing slices. "
            "Think about how far the starting index may travel before a full match is impossible."
        ),
        "test_cases": [
            {"input": ["hello", "ll"], "expected": 2},
            {"input": ["hello", "z"], "expected": -1},
            {"input": ["hello", "ello"], "expected": 1},
            {"input": ["abcabc", "ab"], "expected": 0},
        ],
        "hidden_test_cases": [
            {"input": ["banana", "na"], "expected": 2},
            {"input": ["aaaa", "aa"], "expected": 0},
            {"input": ["hello", "hello"], "expected": 0},
            {"input": ["ab", "abc"], "expected": -1},
        ],
        "time_limit_minutes": 8,
        "diamonds": 100,
        "scaffolded_hints": [
            {"level": 1, "text": "If len(sub) > len(s), no match is possible: return -1."},
            {"level": 2, "text": "The last starting index is len(s) - len(sub). Loop range(len(s) - len(sub) + 1)."},
            {"level": 3, "text": "At each i compare s[i:i + len(sub)] == sub and return the first match."},
        ],
    },
    "assessment": {
        "title": "Stringed Loom Final Test",
        "description": (
            "Prove you understand immutability, slicing, and string arithmetic — "
            "favourite territory of output-prediction MCQs."
        ),
        "questions": [
            {
                "type": "code_tracing",
                "code": 's = "ab"\nt = s + s + s\n# What is len(t)?',
                "answer_format": "single_number",
                "expected_answer": "6",
                "explanation": "s is 2 characters. t = 'ab' + 'ab' + 'ab' = 'ababab', which has 6 characters.",
            },
            {
                "type": "concept",
                "question": "Why can you not write word[0] = 'j' to fix a typo in a Python string?",
                "answer_format": "short_answer",
                "keywords": ["immutable", "cannot change", "can't change", "new string", "read only", "read-only"],
                "explanation": (
                    "Strings are immutable: the characters of an existing string can never "
                    "be changed in place. You must build a brand-new string instead."
                ),
            },
            {
                "type": "debug",
                "code": "def initials(first, last):\n    result = first[0] + '.' + last[1]\n    return result\n# Bug: 'Alan', 'Turing' gives 'A.i', should be 'A.T'",
                "error": "The 'i' comes from last[1]. The last name's first letter is at index 0, not 1.",
                "question": "One line is wrong. What is the correct line?",
                "fix": "result = first[0] + '.' + last[0]",
                "explanation": (
                    "last[1] is the SECOND letter of the last name. The first letter lives "
                    "at last[0] — same zero-based rule as every other sequence."
                ),
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 150,
    },
    "explain": {
        "title": "Explain Immutability",
        "prompt": "Why does the line word[0] = 'j' raise a TypeError when word is a string?",
        "answer_format": "short_answer",
        "keywords": ["immutable", "cannot", "can't", "change", "in place", "new string", "rebuilt", "copy"],
        "min_words": 8,
        "model_answer": (
            "Strings are immutable: the characters of an existing string can never be "
            "changed in place. Item assignment is forbidden on a string, so Python raises "
            "TypeError. Any change must build a brand-new string."
        ),
        "intention": "The answer must state that strings cannot be modified in place and that changes build a new string.",
    },
    "break": {
        "title": "The Uncuttable Thread",
        "story": (
            "A weaver wants to capitalise the first thread of a cloth, but the loom "
            "refuses. Strings cannot be edited in place — the weaver must reweave."
        ),
        "buggy_code": "def capitalize_first(word):\n    word[0] = word[0].upper()\n    return word\n\nprint(capitalize_first(\"hello\"))",
        "expected_output": "Hello",
        "actual_output": "TypeError: 'str' object does not support item assignment",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "Strings are immutable — word[0] = ... is forbidden, so we must build a new string", "correct": True, "why": "Immutability means no in-place edit exists for strings."},
                {"id": "b", "text": "upper() is undefined", "correct": False, "why": "upper() exists — the failure happens before it on the assignment."},
                {"id": "c", "text": "hello has no index 0", "correct": False, "why": "String indexes start at 0 like every sequence — 'h' is at index 0."},
                {"id": "d", "text": "The function returns before printing", "correct": False, "why": "The error is raised inside the function on the assignment line."},
            ],
        },
        "fix": "return word[0].upper() + word[1:]",
        "fixed_code": "def capitalize_first(word):\n    return word[0].upper() + word[1:]\n\nprint(capitalize_first(\"hello\"))",
        "explanation": (
            "Instead of editing in place (impossible), build the new cloth: the first "
            "thread uppercased, then the rest of the word sliced on."
        ),
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:strings",
        "concept_name": "Strings and Immutability",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "a string is a sequence of characters indexed from 0",
            "strings are immutable — change means building a new string",
            "s[a:b] stops before b (same rule as range)",
            "s[::-1] reverses; len(s) counts characters",
            "'+' on strings creates a fresh string each time",
        ],
        "spaced_fields": [
            "immutability",
            "slice_end_exclusive",
            "index_vs_length",
            "string_building_cost",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "strings",
        "unlocks_next": ["functions", "sorting"],
        "tower_badge": "thread_weaver",
        "world_node": {
            "level": 4,
            "title": "The Stringed Loom",
            "color": "rose",
            "icon": "🧵",
            "description": "Learn text as immutable character sequences",
        },
    },
}