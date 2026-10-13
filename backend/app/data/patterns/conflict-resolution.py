"""Pattern Pack — Conflict Resolution."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "conflict-resolution",
    "name": "Conflict Resolution",
    "emoji": "🕊️",
    "round_id": "hr-managerial",
    "purpose": "Apply mediation steps, identify interests vs positions, and choose win-win strategies in team conflicts.",
    "prerequisites": ["verbal-reasoning", "situational"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Compromise = win-win",
            "description": "Confuses compromise with collaborative problem-solving.",
        },
        {
            "id": "M2",
            "label": "Avoid conflict",
            "description": "Believes avoiding conflict is always best.",
        },
        {
            "id": "M3",
            "label": "Win-lose framing",
            "description": "Treats every conflict as a battle to win.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Conflict styles",
            "captain_message": "See competing, collaborating, compromising, avoiding, accommodating.",
            "render": {
                "kind": "conflict_quadrant",
                "x": "assertiveness",
                "y": "cooperativeness",
                "styles": ["competing", "collaborating", "compromising", "avoiding", "accommodating"],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Reframe position to interest",
            "captain_message": "Behind 'I want X' is 'I need Y'.",
            "render": {
                "kind": "reframe",
                "position": "I need a raise",
                "interest": "I want recognition for my impact",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict best style",
            "captain_message": "Choose the conflict style.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "High importance, good relationship: which style?",
                "options": ["Avoiding", "Competing", "Collaborating", "Accommodating"],
                "answer_index": 2,
                "explanation": "Collaborating is best for high-importance, good-relationship situations.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build mediation steps",
            "captain_message": "Write the mediation sequence.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Step 1",
                        "placeholder": "let each party speak",
                        "answer": "let each party speak",
                    },
                    {
                        "label": "Step 2",
                        "placeholder": "identify interests behind positions",
                        "answer": "identify interests behind positions",
                    },
                    {
                        "label": "Step 3",
                        "placeholder": "brainstorm options",
                        "answer": "brainstorm options",
                    },
                    {
                        "label": "Step 4",
                        "placeholder": "agree on action",
                        "answer": "agree on action",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break win-lose",
            "captain_message": "Winning the argument can lose the relationship.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Two teammates argue about design. Best first step?",
                "options": ["Manager decides", "Listen to both, find common goal", "Vote", "Ignore"],
                "answer_index": 1,
                "explanation": "Listen to both and align on shared goal.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix with interest-based negotiation",
            "captain_message": "Separate people from problem.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Separate",
                        "placeholder": "people from problem",
                        "answer": "people from problem",
                    },
                    {
                        "label": "Focus",
                        "placeholder": "interests not positions",
                        "answer": "interests not positions",
                    },
                    {
                        "label": "Options",
                        "placeholder": "generate multiple options",
                        "answer": "generate multiple options",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to negotiation",
            "captain_message": "Same principles in salary negotiation.",
            "render": {
                "kind": "recall",
                "prompt": "In negotiation, focus on?",
                "answer": "interests not positions",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Conflict = interest mismatch. Resolution = align interests.",
            "render": {
                "kind": "recall",
                "prompt": "First step in conflict resolution?",
                "answer": "identify underlying interests",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Conflict style for high assertiveness, low cooperativeness?",
                "options": ["Collaborating", "Competing", "Avoiding", "Accommodating"],
                "answer": "Competing",
                "explanation": "Competing = high assertiveness, low cooperativeness.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Best style when relationship matters more than outcome?",
                "options": ["Competing", "Collaborating", "Accommodating", "Avoiding"],
                "answer": "Accommodating",
                "explanation": "Accommodating gives in to preserve relationship.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Win-win maps to?",
                "options": ["Compromising", "Collaborating", "Competing", "Avoiding"],
                "answer": "Collaborating",
                "explanation": "Collaborating seeks win-win.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Avoiding conflict leads to?",
                "options": ["Resolution", " resentment buildup", "Win-win", "Speed"],
                "answer": " resentment buildup",
                "explanation": "Avoidance lets issues fester.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Best response to teammate blocking your work?",
            "options": ["Yell", "Discuss dependencies and align", "Ignore", "Report immediately"],
            "answer": "Discuss dependencies and align",
            "explanation": "Address directly with focus on shared goal.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Conflict = ?",
            "answer": "interest mismatch",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Win-win style?",
            "answer": "collaborating",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "First mediation step?",
            "answer": "let each party speak",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Workplace conflict",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Team scenarios",
        },
    ],
    "interview_transfer": {
        "prompt": "How does conflict resolution help in technical leadership?",
        "model_answer": "It lets you align stakeholders around trade-offs instead of forcing a single view.",
    },
}
