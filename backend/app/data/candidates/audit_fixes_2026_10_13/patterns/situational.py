"""Pattern Pack — Situational Judgment."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "situational",
    "name": "Situational Judgment",
    "emoji": "🎭",
    "round_id": "hr-managerial",
    "purpose": "Choose the best response to workplace scenarios involving ethics, priorities, and stakeholder management.",
    "prerequisites": ["verbal-reasoning", "grammar"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Most ethical is always best",
            "description": "Ignores business context and constraints.",
        },
        {
            "id": "M2",
            "label": "Escalate immediately",
            "description": "Always picks escalation instead of attempting resolution.",
        },
        {
            "id": "M3",
            "label": "Ignore stakeholder",
            "description": "Chooses action without considering impacted parties.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Stakeholder map",
            "captain_message": "See who is affected.",
            "render": {
                "kind": "stakeholder_map",
                "scenario": "deadline moved up by 2 days",
                "stakeholders": ["team", "manager", "customer"],
                "impacts": ["burnout", "quality", "trust"],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change priorities",
            "captain_message": "Reorder response options by effectiveness.",
            "render": {
                "kind": "sortable",
                "options": [
                    "Refuse and quit",
                    "Escalate with data",
                    "Silently work overtime",
                    "Negotiate scope with manager",
                ],
                "correct_order": ["Negotiate scope with manager", "Escalate with data", "Silently work overtime", "Refuse and quit"],
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict best response",
            "captain_message": "Choose the most professional action.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "You find a senior engineer violating security policy. First action?",
                "options": ["Ignore", "Confront publicly", "Speak privately then escalate if needed", "Report anonymously immediately"],
                "answer_index": 2,
                "explanation": "Speak privately first to understand context, then escalate if unresolved.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build decision framework",
            "captain_message": "Write criteria for choosing response.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Stakeholders",
                        "placeholder": "who is affected",
                        "answer": "who is affected",
                    },
                    {
                        "label": "Constraints",
                        "placeholder": "time, policy, risk",
                        "answer": "time, policy, risk",
                    },
                    {
                        "label": "Best response",
                        "placeholder": "action",
                        "answer": "action",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the ego response",
            "captain_message": "Don't make it about you.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Manager takes credit for your work. Best first step?",
                "options": ["Confront in meeting", "Document and schedule 1:1", "Quit", "Ignore"],
                "answer_index": 1,
                "explanation": "Document facts and discuss privately.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix escalation chain",
            "captain_message": "Use proper escalation: peer → manager → HR.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Try resolve",
                        "placeholder": "peer or self",
                        "answer": "peer or self",
                    },
                    {
                        "label": "Escalate manager",
                        "placeholder": "with data",
                        "answer": "with data",
                    },
                    {
                        "label": "Escalate HR",
                        "placeholder": "if unresolved or policy violation",
                        "answer": "if unresolved or policy violation",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to customer support",
            "captain_message": "Same framework: stakeholders, constraints, action.",
            "render": {
                "kind": "recall",
                "prompt": "Escalation principle?",
                "answer": "resolve at lowest level first with data",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For situational questions: prioritize data, then people, then process.",
            "render": {
                "kind": "recall",
                "prompt": "SJT priority order?",
                "answer": "data, people, process",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Best first action when seeing a bug in production?",
                "options": ["Ignore", "Fix immediately without telling", "Alert team and assess", "Blame QA"],
                "answer": "Alert team and assess",
                "explanation": "Communicate before acting.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Colleague misses deadline affecting you. Best action?",
                "options": ["Do their work", "Complain to manager", "Discuss timeline together", "Ignore"],
                "answer": "Discuss timeline together",
                "explanation": "Collaborate to adjust plan.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Manager asks you to skip testing. Best response?",
                "options": ["Do it", "Refuse and explain risk", "Quit", "Do it and hide"],
                "answer": "Refuse and explain risk",
                "explanation": "Professional pushback with data.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "You see a coworker steal. First step?",
                "options": ["Confront loudly", "Report to HR with evidence", "Ignore", "Join them"],
                "answer": "Report to HR with evidence",
                "explanation": "Document and escalate through proper channel.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Best response to unfair criticism in public?",
            "options": ["Argue back", "Stay silent then discuss privately", "Cry", "Quit"],
            "answer": "Stay silent then discuss privately",
            "explanation": "De-escalate public, resolve private.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "SJT priority?",
            "answer": "data, people, process",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Escalation starts at?",
            "answer": "lowest level with data",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Public conflict response?",
            "answer": "de-escalate, resolve privately",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Workplace scenarios",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Ethics, priorities",
        },
    ],
    "interview_transfer": {
        "prompt": "How does SJT thinking help in incident management?",
        "model_answer": "It trains prioritizing impact, communicating with data, and escalating through proper channels.",
    },
}
