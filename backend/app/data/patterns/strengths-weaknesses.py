"""Pattern Pack — Strengths & Weaknesses."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "strengths-weaknesses",
    "name": "Strengths & Weaknesses",
    "emoji": "⚖️",
    "round_id": "hr-managerial",
    "purpose": "Answer strengths and weaknesses questions with evidence, showing self-awareness and growth mindset.",
    "prerequisites": ["verbal-reasoning", "grammar"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Fake weakness",
            "description": "Uses cliché 'perfectionism' weakness.",
        },
        {
            "id": "M2",
            "label": "Strength without proof",
            "description": "States 'I'm a leader' without example.",
        },
        {
            "id": "M3",
            "label": "Too many weaknesses",
            "description": "Lists 3+ weaknesses.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Honest self-map",
            "captain_message": "See strengths and growth areas.",
            "render": {
                "kind": "radar",
                "axes": ["Technical", "Communication", "Leadership", "Learning"],
                "scores": [8, 6, 7, 9],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Reframe weakness",
            "captain_message": "Turn weakness into growth story.",
            "render": {
                "kind": "reframe",
                "weakness": "public speaking",
                "reframe": "took Toastmasters, now present weekly",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict best answer",
            "captain_message": "Choose the best weakness.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Best weakness to say?",
                "options": ["Perfectionism", "I take on too much responsibility", "I'm lazy", "I hate teamwork"],
                "answer_index": 1,
                "explanation": "'I take on too much responsibility' shows drive with a manageable downside.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the answer",
            "captain_message": "Write weakness + action + result.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Weakness",
                        "placeholder": "real but fixable weakness",
                        "answer": "real but fixable weakness",
                    },
                    {
                        "label": "Action",
                        "placeholder": "what I did to improve",
                        "answer": "what I did to improve",
                    },
                    {
                        "label": "Result",
                        "placeholder": "measurable improvement",
                        "answer": "measurable improvement",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break cliché answers",
            "captain_message": "Perfectionism is overused.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Which is a cliché weakness?",
                "options": ["Delegation", "Perfectionism", "Public speaking", "Impatience"],
                "answer_index": 1,
                "explanation": "Perfectionism is a well-known cliché.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix with STAR",
            "captain_message": "Situation, Task, Action, Result.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Situation",
                        "placeholder": "context",
                        "answer": "context",
                    },
                    {
                        "label": "Task",
                        "placeholder": "challenge",
                        "answer": "challenge",
                    },
                    {
                        "label": "Action",
                        "placeholder": "what I did",
                        "answer": "what I did",
                    },
                    {
                        "label": "Result",
                        "placeholder": "outcome",
                        "answer": "outcome",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to feedback",
            "captain_message": "Same structure for performance reviews.",
            "render": {
                "kind": "recall",
                "prompt": "Feedback formula?",
                "answer": "situation, behavior, impact",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Strength = proof. Weakness = growth story.",
            "render": {
                "kind": "recall",
                "prompt": "Weakness answer should include?",
                "answer": "action taken and result",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Best weakness format?",
                "options": ["Cliché", "Real + growth story", "None", "Too many"],
                "answer": "Real + growth story",
                "explanation": "Honest weakness with improvement story.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Strength without evidence is?",
                "options": ["Convincing", "Unsubstantiated", "Strong", "Modest"],
                "answer": "Unsubstantiated",
                "explanation": "Strengths need proof.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "STAR stands for?",
                "options": ["Situation Task Action Result", "Strength Team Action Result", "Situation Test Action Result", "None"],
                "answer": "Situation Task Action Result",
                "explanation": "STAR = Situation, Task, Action, Result.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "'Perfectionism' weakness is?",
                "options": ["Good", "Cliché", "Honest", "Strong"],
                "answer": "Cliché",
                "explanation": "Perfectionism is overused and seen as insincere.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Best weakness answer structure?",
            "options": ["Just say it", "Weakness + action + result", "Blame others", "Avoid question"],
            "answer": "Weakness + action + result",
            "explanation": "Show self-awareness and growth.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "STAR stands for?",
            "answer": "Situation, Task, Action, Result",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Weakness answer should include?",
            "answer": "action taken and measurable result",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Strength needs?",
            "answer": "proof or example",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 6,
            "focus": "Self-awareness, growth",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 8,
            "focus": "STAR, specificity",
        },
    ],
    "interview_transfer": {
        "prompt": "How does weakness framing help in leadership?",
        "model_answer": "It builds trust by showing vulnerability and a growth mindset, encouraging teams to do the same.",
    },
}
