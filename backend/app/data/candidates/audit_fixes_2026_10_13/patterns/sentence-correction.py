"""Pattern Pack — Sentence Correction."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "sentence-correction",
    "name": "Sentence Correction",
    "emoji": "✍️",
    "round_id": "aptitude",
    "purpose": "Identify subject-verb agreement errors, tense mismatches, preposition mistakes, and redundancy in placement-style English sentences.",
    "prerequisites": ["basic-grammar", "parts-of-speech", "tenses"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Proximity agreement",
            "description": "Makes verb agree with nearest noun instead of the true subject.",
        },
        {
            "id": "M2",
            "label": "Tense stacking",
            "description": "Mixes past and present in reported speech without backshifting.",
        },
        {
            "id": "M3",
            "label": "Redundancy blindness",
            "description": "Misses redundant phrases like 'return back' or 'basic fundamentals'.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Subject and verb",
            "captain_message": "Find the subject first. Then choose the verb.",
            "render": {
                "kind": "sentence_diagram",
                "sentence": "The list of items are on the desk.",
                "highlight_subject": True,
                "highlight_verb": True,
                "show_correction": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Swap subject position",
            "captain_message": "Move prepositional phrases around. See subject stay the same.",
            "render": {
                "kind": "sentence_swap",
                "subject": "The list",
                "prepositional": "of items",
                "verb": "is",
                "bad_verb": "are",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the error",
            "captain_message": "Choose the error type without reading the full sentence.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Neither the manager nor the employees ____ present.",
                "options": ["was", "were", "has been", "is"],
                "answer_index": 1,
                "explanation": "With neither/nor, verb agrees with nearer subject: employees → were.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the correction",
            "captain_message": "Write the corrected clause.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Find subject",
                        "placeholder": "subject",
                        "answer": "subject",
                    },
                    {
                        "label": "Find verb",
                        "placeholder": "verb",
                        "answer": "verb",
                    },
                    {
                        "label": "Corrected sentence",
                        "placeholder": "corrected",
                        "answer": "corrected",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the proximity trap",
            "captain_message": "Ignore the nearest noun. Find the true subject.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "The quality of the products ____ improved.",
                "options": ["have", "has", "are", "were"],
                "answer_index": 1,
                "explanation": "Subject is 'quality', singular. Verb = has.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix reported speech",
            "captain_message": "Backshift tense and change pronouns.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Reporting verb",
                        "placeholder": "said / told",
                        "answer": "said / told",
                    },
                    {
                        "label": "Backshift tense",
                        "placeholder": "present → past",
                        "answer": "present → past",
                    },
                    {
                        "label": "Change pronouns",
                        "placeholder": "I → he/she",
                        "answer": "I → he/she",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to email writing",
            "captain_message": "Same rules apply in professional writing.",
            "render": {
                "kind": "recall",
                "prompt": "In professional emails, avoid:",
                "answer": "redundancy, vague subjects, tense shifts",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Eliminate options by checking subject-verb and tense first.",
            "render": {
                "kind": "recall",
                "prompt": "First filter in sentence correction?",
                "answer": "subject-verb agreement",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "The dog and the cat ____ running.",
                "options": ["is", "are", "was", "has"],
                "answer": "are",
                "explanation": "Compound subject = plural → are.",
            },
            {
                "id": "w2",
                "question": "She said she ____ coming tomorrow.",
                "options": ["is", "was", "were", "be"],
                "answer": "was",
                "explanation": "Reported speech backshift: is → was.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Each of the students ____ given a prize.",
                "options": ["were", "was", "have", "are"],
                "answer": "was",
                "explanation": "'Each' is singular. Verb = was.",
            },
            {
                "id": "d2",
                "question": "Not only he but also his brothers ____ involved.",
                "options": ["was", "is", "were", "has"],
                "answer": "were",
                "explanation": "With 'not only...but also', verb agrees with nearer subject: brothers → were.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Neither the teacher nor the students ____ aware.",
                "options": ["was", "were", "is", "has"],
                "answer": "were",
                "explanation": "Nearest subject 'students' is plural → were.",
            },
            {
                "id": "s2",
                "question": "The news ____ spreading fast.",
                "options": ["are", "is", "were", "have"],
                "answer": "is",
                "explanation": "'News' is uncountable singular. Verb = is.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "He doesn't likes coffee.",
                "options": ["like", "likes", "is liking", "liked"],
                "answer": "like",
                "explanation": "Auxiliary 'doesn't' takes base form: doesn't like.",
            },
            {
                "id": "wr2",
                "question": "I am looking forward to ____ from you.",
                "options": ["hear", "hearing", "heard", "hears"],
                "answer": "hearing",
                "explanation": "'Look forward to' ends with preposition 'to', so gerund follows.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "The number of students ____ increasing.",
            "options": ["are", "is", "were", "have"],
            "answer": "is",
            "explanation": "'Number' is singular. Verb = is.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Subject-verb agreement rule for 'each/every'?",
            "answer": "singular verb",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Backshift rule in reported speech?",
            "answer": "present → past, past → past perfect",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "'Look forward to' is followed by?",
            "answer": "gerund (-ing form)",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Subject-verb, tenses",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Error spotting speed",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Prepositions, phrases",
        },
    ],
    "interview_transfer": {
        "prompt": "How does sentence correction thinking help in writing clear product requirements?",
        "model_answer": "It trains subject-verb clarity, removes ambiguity, and enforces tense consistency — all critical for precise PRDs.",
    },
}
