"""Pattern Pack — Strings."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "strings",
    "name": "Strings",
    "emoji": "🔤",
    "round_id": "coding",
    "purpose": "Predict output of slicing, concatenation, common methods, and ASCII-based transformations.",
    "prerequisites": ["variables", "conditions", "output-tracing"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "0-based vs 1-based indexing",
            "description": "Uses 1-based indexing for slice output.",
        },
        {
            "id": "M2",
            "label": "Mutability confusion",
            "description": "Expects original string to change after replace.",
        },
        {
            "id": "M3",
            "label": "Whitespace surprises",
            "description": "Forgets that strip() removes all leading/trailing whitespace characters.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Character positions",
            "captain_message": "Index every character. Count from 0.",
            "render": {
                "kind": "index_overlay",
                "text": "BountyCode",
                "highlight_range": [0, 5],
                "show_negative": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Slice the string",
            "captain_message": "Change start, stop, step.",
            "render": {
                "kind": "slice_editor",
                "text": "BountyCode",
                "default_slice": [0, 5, 1],
                "allow_negative": True,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict slice",
            "captain_message": "Choose the slice result.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "s = 'BountyCode'\ns[0:6]?",
                "options": ["Bounty", "BountyC", "Bount", "ounty"],
                "answer_index": 0,
                "explanation": "s[0:6] = characters 0..5 = 'Bounty'.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the transformation",
            "captain_message": "Write the method chain.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Original",
                        "placeholder": "s",
                        "answer": "s",
                    },
                    {
                        "label": "Lowercase",
                        "placeholder": "s.lower()",
                        "answer": "s.lower()",
                    },
                    {
                        "label": "Replace",
                        "placeholder": ".replace('a','@')",
                        "answer": ".replace('a','@')",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the immutability myth",
            "captain_message": "Strings are immutable. Methods return new strings.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "s='hi'; s.upper(); print(s)?",
                "options": ["HI", "hi", "Error", "None"],
                "answer_index": 1,
                "explanation": "s.upper() returns 'HI' but s stays 'hi'.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix split/join mistakes",
            "captain_message": "Split breaks string into list. Join combines list into string.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Split",
                        "placeholder": "s.split(',') → list",
                        "answer": "s.split(',') → list",
                    },
                    {
                        "label": "Join",
                        "placeholder": "' '.join(list) → string",
                        "answer": "' '.join(list) → string",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to parsing",
            "captain_message": "Same logic for CSV, URLs, and config parsing.",
            "render": {
                "kind": "recall",
                "prompt": "To extract domain from 'https://example.com/path', split on?",
                "answer": "'//' then '/'",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For palindrome check: compare s == s[::-1].",
            "render": {
                "kind": "recall",
                "prompt": "One-line palindrome check?",
                "answer": "s == s[::-1]",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Output: 'BountyCode'[1:5]?",
                "options": ["Bount", "ounty", "Bunty", "ount"],
                "answer": "ounty",
                "explanation": "Indices 1,2,3,4 = 'ounty'.",
            },
            {
                "id": "w2",
                "question": "Output: 'hello'.upper()?",
                "options": ["hello", "HELLO", "Hello", "Error"],
                "answer": "HELLO",
                "explanation": ".upper() returns uppercase.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Output: 'BountyCode'[-3:]?",
                "options": ["ode", "ode ", "Cod", "de"],
                "answer": "ode",
                "explanation": "Negative index counts from end: -3 is 'o', slice to end.",
            },
            {
                "id": "d2",
                "question": "Output: ','.join(['a','b','c'])?",
                "options": ["a,b,c", "abc", "a b c", "a,b,c,"],
                "answer": "a,b,c",
                "explanation": "Join inserts separator between items.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Output: '  hello  '.strip()?",
                "options": ["hello", "  hello  ", "hello  ", "  hello"],
                "answer": "hello",
                "explanation": ".strip() removes all leading/trailing whitespace.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Output: s='abc'; s.replace('a','x'); print(s)?",
                "options": ["xbc", "abc", "Error", "None"],
                "answer": "abc",
                "explanation": "replace returns new string, original unchanged.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Output: 'racecar' == 'racecar'[::-1]?",
            "options": ["True", "False", "Error", "None"],
            "answer": "True",
            "explanation": "'racecar' reversed is still 'racecar'.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Python string indexing starts at?",
            "answer": "0",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Are strings mutable?",
            "answer": "no, immutable",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "s[1:4] excludes which index?",
            "answer": "4",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Slicing, methods",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Quick string prediction",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Palindrome, reverse",
        },
    ],
    "interview_transfer": {
        "prompt": "How does string slicing logic apply to parsing log timestamps?",
        "model_answer": "Log timestamps have fixed-width fields; slice by index ranges just like string operations.",
    },
}
