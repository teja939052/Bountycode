"""Pattern Pack — Reading Comprehension."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "reading-comprehension",
    "name": "Reading Comprehension",
    "emoji": "📖",
    "round_id": "aptitude",
    "purpose": "Answer inference, detail, and vocabulary-in-context questions from short placement passages under time pressure.",
    "prerequisites": ["basic-grammar", "vocabulary", "verbal-reasoning"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Outside knowledge",
            "description": "Brings prior beliefs into the answer instead of relying on the passage.",
        },
        {
            "id": "M2",
            "label": "Keyword matching",
            "description": "Chooses the option containing the passage word even if context changes meaning.",
        },
        {
            "id": "M3",
            "label": "Speed over accuracy",
            "description": "Skims so fast that inference questions fail.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Passage map",
            "captain_message": "Map the passage in 3 sentences before answering.",
            "render": {
                "kind": "passage_map",
                "passage": "AI adoption is accelerating, but trust gaps remain. Regulators demand explainability. Companies that invest in transparency will lead.",
                "highlight_main_idea": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Active reading",
            "captain_message": "Highlight the claim and the evidence.",
            "render": {
                "kind": "highlight",
                "passage": "Remote work increased productivity by 15% in the first quarter, but collaboration scores dropped 8%.",
                "highlight_claim": True,
                "highlight_evidence": True,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the main idea",
            "captain_message": "Choose the main idea before reading the questions.",
            "render": {
                "kind": "multiple_choice",
                "passage": "The gig economy offers flexibility but lacks benefits. Workers trade stability for autonomy.",
                "options": ["Gig workers love autonomy", "Gig economy trades stability for flexibility", "Benefits are increasing", "Remote work is hard"],
                "answer_index": 1,
                "explanation": "Main idea captures the trade-off: flexibility vs stability.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build evidence notes",
            "captain_message": "Write claim-evidence pairs.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Claim",
                        "placeholder": "what the author asserts",
                        "answer": "what the author asserts",
                    },
                    {
                        "label": "Evidence",
                        "placeholder": "supporting detail from passage",
                        "answer": "supporting detail from passage",
                    },
                    {
                        "label": "Inference",
                        "placeholder": "what is implied",
                        "answer": "what is implied",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the trap of 'not in passage'",
            "captain_message": "If it's not in the passage, it's not the answer.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Passage discusses AI. Which answer is outside knowledge?",
                "options": ["AI needs data", "AI is perfect", "AI has bias", "AI needs compute"],
                "answer_index": 1,
                "explanation": "'AI is perfect' is not supported by any realistic passage.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix inference gaps",
            "captain_message": "Inference is implied, not stated.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Locate clue",
                        "placeholder": "sentence implying answer",
                        "answer": "sentence implying answer",
                    },
                    {
                        "label": "Bridge words",
                        "placeholder": "however, therefore, implies",
                        "answer": "however, therefore, implies",
                    },
                    {
                        "label": "Inference",
                        "placeholder": "what must be true",
                        "answer": "what must be true",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to email triage",
            "captain_message": "Scan long emails for claim-evidence pairs before replying.",
            "render": {
                "kind": "recall",
                "prompt": "First pass of a long email should find?",
                "answer": "the sender's main request and supporting evidence",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For inference questions: eliminate literal restatements.",
            "render": {
                "kind": "recall",
                "prompt": "Inference answers are?",
                "answer": "implied, not directly stated",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Passage: 'Rainfall decreased 20%. Reservoirs fell to 40%.' Main idea?",
                "options": ["Rain is nice", "Drought risk rises", "Water is cheap", "Reservoirs overflow"],
                "answer": "Drought risk rises",
                "explanation": "Decreased rainfall and lower reservoirs imply drought risk.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Author implies that flexible work: (passage about productivity vs collaboration)",
                "options": ["Is always better", "Has trade-offs", "Saves money", "Fails always"],
                "answer": "Has trade-offs",
                "explanation": "Passage mentions productivity up but collaboration down → trade-offs.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Vocab in context: 'The policy was nebulous.' Nebulous means?",
                "options": ["Clear", "Vague", "Strict", "Long"],
                "answer": "Vague",
                "explanation": "Nebulous = vague, unclear.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Which is an inference, not a detail?",
                "options": ["The cat sat on the mat", "The cat was tired", "The mat was red", "The cat is a mammal"],
                "answer": "The cat was tired",
                "explanation": "Inference is implied, not directly stated in the passage.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Passage: 'Electric vehicle sales doubled in two years.' Inference?",
            "options": ["EVs are cheap", "EV adoption is accelerating", "Gas cars are dead", "Batteries failed"],
            "answer": "EV adoption is accelerating",
            "explanation": "Doubling sales in two years implies accelerating adoption.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Main idea vs detail?",
            "answer": "main idea is the point; detail supports it",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Inference is?",
            "answer": "implied, not directly stated",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "If answer is not in passage, it is?",
            "answer": "wrong for reading comprehension",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Detail and inference",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Fast reading, vocab in context",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Main idea, tone",
        },
    ],
    "interview_transfer": {
        "prompt": "How does RC training help in a system design interview?",
        "model_answer": "It trains extracting requirements, distinguishing stated from implied constraints, and avoiding outside-knowledge assumptions.",
    },
}
