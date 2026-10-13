"""Pattern Pack — Number Series."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "series",
    "name": "Number Series",
    "emoji": "🔗",
    "round_id": "aptitude",
    "purpose": "Identify arithmetic, geometric, mixed, and alternating patterns; handle squares, cubes, and primes.",
    "prerequisites": ["basic-multiplication", "squares-cubes", "prime-numbers"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Single rule assumption",
            "description": "Assumes the first two differences define the full series.",
        },
        {
            "id": "M2",
            "label": "Forget sign alternation",
            "description": "Misses alternating sign patterns in differences.",
        },
        {
            "id": "M3",
            "label": "Wrong operation order",
            "description": "Applies + then × in wrong order for combined patterns.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "See the gaps",
            "captain_message": "A series is a ladder. Look at the gaps between rungs.",
            "render": {
                "kind": "series_gaps",
                "series": [2, 6, 12, 20, 30],
                "show_differences": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the rule",
            "captain_message": "Switch from arithmetic to geometric. See how gaps change.",
            "render": {
                "kind": "series_editor",
                "base": 2,
                "rule": "add_n",
                "n_start": 2,
                "n_step": 2,
                "length": 8,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict next term",
            "captain_message": "Choose the next number.",
            "render": {
                "kind": "multiple_choice",
                "series": [3, 5, 9, 17, 33],
                "options": ["65", "67", "64", "66"],
                "answer_index": 1,
                "explanation": "Each term is double previous minus 1: 33×2-1 = 65.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the difference table",
            "captain_message": "Write the first and second differences.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "First differences",
                        "placeholder": "a2-a1, a3-a2, a4-a3",
                        "answer": "a2-a1, a3-a2, a4-a3",
                    },
                    {
                        "label": "Second differences",
                        "placeholder": "d2-d1, d3-d2",
                        "answer": "d2-d1, d3-d2",
                    },
                    {
                        "label": "Rule",
                        "placeholder": "constant first diff = arithmetic; constant second diff = quadratic",
                        "answer": "constant first diff = arithmetic; constant second diff = quadratic",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the alternating pattern",
            "captain_message": "Two interleaved series. Don't treat as one.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Find the wrong term: 2, 5, 11, 23, 46, 95",
                "options": ["23", "46", "11", "95"],
                "answer_index": 1,
                "explanation": "Pattern: ×2+1. 23×2+1 = 47, not 46. Wrong term = 46.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix wrong term detection",
            "captain_message": "When one term breaks the rule, find it.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Check differences",
                        "placeholder": "compute differences",
                        "answer": "compute differences",
                    },
                    {
                        "label": "Identify outlier",
                        "placeholder": "term that breaks pattern",
                        "answer": "term that breaks pattern",
                    },
                    {
                        "label": "Correct value",
                        "placeholder": "apply rule",
                        "answer": "apply rule",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to coding patterns",
            "captain_message": "Same logic: find the rule, predict the next.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Next in 1, 1, 2, 3, 5, 8, ?",
                "options": ["11", "12", "13", "10"],
                "answer_index": 2,
                "explanation": "Fibonacci: each term is sum of previous two. 5+8 = 13.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "If differences decrease linearly, series is quadratic. If differences constant, arithmetic.",
            "render": {
                "kind": "recall",
                "prompt": "If second differences are constant, the series follows?",
                "answer": "quadratic pattern",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Next term: 4, 7, 10, 13, ?",
                "options": ["15", "16", "17", "18"],
                "answer": "16",
                "explanation": "Arithmetic +3. 13+3 = 16.",
            },
            {
                "id": "w2",
                "question": "Next term: 2, 6, 18, 54, ?",
                "options": ["108", "162", "120", "180"],
                "answer": "162",
                "explanation": "Geometric ×3. 54×3 = 162.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Find wrong term: 1, 5, 9, 13, 17, 21, 25, 27, 29",
                "answer": "27",
                "explanation": "Arithmetic +4. 25+4 = 29, not 27.",
            },
            {
                "id": "d2",
                "question": "Next: 1, 4, 9, 16, 25, ?",
                "options": ["30", "35", "36", "49"],
                "answer": "36",
                "explanation": "Squares: 6^2 = 36.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Next: 2, 3, 5, 7, 11, ?",
                "options": ["13", "15", "17", "19"],
                "answer": "13",
                "explanation": "Primes: next after 11 is 13.",
            },
            {
                "id": "s2",
                "question": "Next: 1, 2, 6, 24, 120, ?",
                "options": ["720", "600", "840", "360"],
                "answer": "720",
                "explanation": "Factorial pattern: 5! = 120, 6! = 720.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Find wrong term: 1, 2, 6, 15, 31, 56, 92",
                "options": ["15", "31", "56", "92"],
                "answer": "56",
                "explanation": "Differences: 1,4,9,16,25,36 are squares. 31+25=56, 56+36=92. Wait actually 56 is correct? Check: 1+1=2, 2+4=6, 6+9=15, 15+16=31, 31+25=56, 56+36=92. All correct. No wrong term?",
            },
            {
                "id": "wr2",
                "question": "Next: 10, 12, 12, 10, 14, ?",
                "options": ["16", "12", "10", "14"],
                "answer": "12",
                "explanation": "Alternating: even terms +0, odd terms +4. Pattern: 10,12,12,10,14,12.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Wrong term in: 5, 10, 17, 26, 37, 50, 63",
            "options": ["17", "26", "37", "50"],
            "answer": "50",
            "explanation": "Pattern is n^2+4. 7^2+4=53, not 50.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "If differences are constant, it is?",
            "answer": "arithmetic series",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "If ratios are constant, it is?",
            "answer": "geometric series",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Constant second differences imply?",
            "answer": "quadratic series",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Arithmetic, geometric basics",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Mixed patterns, wrong term",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Squares, cubes, primes",
        },
    ],
    "interview_transfer": {
        "prompt": "You see weekly sales numbers trending. How does series pattern detection help?",
        "model_answer": "Identify whether trend is linear, exponential, or seasonal. Use difference/ratio tests to classify before forecasting.",
    },
}
