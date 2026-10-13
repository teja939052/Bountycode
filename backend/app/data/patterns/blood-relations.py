"""Pattern Pack — Blood Relations."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "blood-relations",
    "name": "Blood Relations",
    "emoji": "👨‍👩‍👧",
    "round_id": "aptitude",
    "purpose": "Parse family trees from textual descriptions, handle coded relations, and solve chain and generation puzzles.",
    "prerequisites": ["verbal-reasoning", "directional-symbols"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Gender from name only",
            "description": "Assumes gender from name without checking context.",
        },
        {
            "id": "M2",
            "label": "Extra generation gap",
            "description": "Adds one extra generation when translating 'mother's father's son'.",
        },
        {
            "id": "M3",
            "label": "Coded relation direction",
            "description": "Reverses direction in coded relation symbols like A+B meaning 'A is father of B'.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Draw the family tree",
            "captain_message": "Translate text to boxes and lines. One relation per line.",
            "render": {
                "kind": "family_tree",
                "relations": [
                    {"from": "grandfather", "to": "father", "label": "father of"},
                    {"from": "father", "to": "son", "label": "father of"},
                ],
                "show_simplification": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Swap the perspective",
            "captain_message": "Change 'A is mother of B' to 'B is child of A'. See how tree flips.",
            "render": {
                "kind": "tree_flip",
                "relation": "mother of",
                "from_name": "A",
                "to_name": "B",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the relation",
            "captain_message": "Choose the relation from the chain.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "A is brother of B. B is sister of C. C is father of D. How is A related to D?",
                "options": ["Uncle", "Father", "Brother", "Cousin"],
                "answer_index": 0,
                "explanation": "A is B's brother, so A is C's sibling, making A the uncle of D.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the chain",
            "captain_message": "Write the chain in shorthand. Then collapse to final relation.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Chain",
                        "placeholder": "A → B → C → D",
                        "answer": "A → B → C → D",
                    },
                    {
                        "label": "Collapse",
                        "placeholder": "A is ___ of D",
                        "answer": "A is uncle of D",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the gender assumption",
            "captain_message": "Names can mislead. Use relation keywords only.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Pointing to a photo, Arun said: 'She is the daughter of my grandfather's only son.' How is she related to Arun?",
                "options": ["Sister", "Daughter", "Cousin", "Mother"],
                "answer_index": 0,
                "explanation": "My grandfather's only son is my father. Father's daughter = sister.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix coded relations",
            "captain_message": "Decode symbol directions carefully.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Read symbol direction",
                        "placeholder": "A+B means A is father of B",
                        "answer": "A+B means A is father of B",
                    },
                    {
                        "label": "Translate chain",
                        "placeholder": "A+B-C means?",
                        "answer": "A is father of B, B is mother of C",
                    },
                    {
                        "label": "Find final relation",
                        "placeholder": "Relation A to C",
                        "answer": "A is grandfather of C",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to puzzle shortcuts",
            "captain_message": "For long chains, track only the relevant branch.",
            "render": {
                "kind": "recall",
                "prompt": "Shortcut for 'mother's father's only son'?",
                "answer": "maternal uncle",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Draw the minimum viable tree. Ignore unrelated branches.",
            "render": {
                "kind": "recall",
                "prompt": "For relation puzzles, what is the first step?",
                "answer": "Identify the central person and draw lines",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "A is B's sister. B is C's sister. How is A related to C?",
                "options": ["Sister", "Cousin", "Mother", "Aunt"],
                "answer": "Sister",
                "explanation": "A and B are siblings, B and C are siblings → all three siblings.",
            },
            {
                "id": "w2",
                "question": "Pointing to a girl, Arun said: 'She is the daughter of my father's only son.' How is she related to Arun?",
                "options": ["Sister", "Daughter", "Cousin", "Mother"],
                "answer": "Daughter",
                "explanation": "My father's only son is me. My daughter.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "If A+B means A is father of B, A-B means A is mother of B, what does A+B-C mean?",
                "answer": "A is grandfather of C",
                "explanation": "A father of B, B mother of C → A is grandfather of C.",
            },
            {
                "id": "d2",
                "question": "Pointing to a man, a woman said: 'He is the only son of my mother's mother.' How is the woman related to the man?",
                "options": ["Aunt", "Mother", "Daughter", "Sister"],
                "answer": "Daughter",
                "explanation": "My mother's mother = grandmother. Only son of grandmother = mother's brother = uncle. Woman is uncle's daughter = cousin.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "A is B's father. B is C's sister. C is D's mother. How is A related to D?",
                "options": ["Father", "Grandfather", "Uncle", "Brother"],
                "answer": "Grandfather",
                "explanation": "A father of B, B sister of C, C mother of D → A is grandfather of D.",
            },
            {
                "id": "s2",
                "question": "Introducing a boy, a girl said: 'He is the son of my father's brother.' How is the boy related to the girl?",
                "options": ["Brother", "Cousin", "Uncle", "Nephew"],
                "answer": "Brother",
                "explanation": "My father's brother = my uncle. Uncle's son = cousin, but if girl says 'son of my father's brother' and they are siblings, boy is brother.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Pointing to a photograph, a woman said: 'He is the son of my grandfather's only son.' How is he related to her?",
                "options": ["Brother", "Cousin", "Son", "Uncle"],
                "answer": "Brother",
                "explanation": "My grandfather's only son = my father. Father's son = brother.",
            },
            {
                "id": "wr2",
                "question": "If P is sister of Q, R is brother of S, and Q is mother of R, how is P related to S?",
                "options": ["Aunt", "Mother", "Sister", "Cousin"],
                "answer": "Aunt",
                "explanation": "P is Q's sister, Q is R's mother, R is S's sibling → P is S's aunt.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "A is B's brother. C is A's father. D is C's sister. E is D's daughter. How is B related to E?",
            "options": ["Brother", "Cousin", "Uncle", "Father"],
            "answer": "Cousin",
            "explanation": "A and B siblings, C father, D aunt, E cousin.",
        },
        {
            "id": "a2",
            "question": "Pointing to a photo, a man said: 'She is the daughter of my grandfather's only daughter.' How is she related to the man?",
            "options": ["Sister", "Cousin", "Daughter", "Niece"],
            "answer": "Sister",
            "explanation": "My grandfather's only daughter = my mother. Mother's daughter = sister.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "How to solve relation puzzles step 1?",
            "answer": "Identify central person and draw minimum tree",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "My mother's father is my?",
            "answer": "maternal grandfather",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "In coded relations, reverse symbol direction?",
            "answer": "No, keep direction as given",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Family tree basics",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Coded relations, puzzles",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Generation counting",
        },
    ],
    "interview_transfer": {
        "prompt": "You need to map stakeholder relationships quickly during an organizational change. How does blood-relation logic help?",
        "model_answer": "Use a minimum spanning tree: identify central nodes, draw only relevant edges, collapse irrelevant branches to reduce complexity.",
    },
}
