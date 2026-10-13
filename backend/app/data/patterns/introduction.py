"""Pattern Pack — Self Introduction."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "introduction",
    "name": "Self Introduction",
    "emoji": "🙋",
    "round_id": "hr-managerial",
    "purpose": "Craft a 60-90 second self-introduction covering background, skills, projects, and goals.",
    "prerequisites": ["verbal-reasoning", "grammar"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Too long",
            "description": "Rambles beyond 2 minutes.",
        },
        {
            "id": "M2",
            "label": "Too academic",
            "description": "Lists grades only, no skills or projects.",
        },
        {
            "id": "M3",
            "label": "No structure",
            "description": "Jumps between past, present, future randomly.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Intro structure",
            "captain_message": "Past, present, future in 3 sentences.",
            "render": {
                "kind": "timeline",
                "segments": ["past", "present", "future"],
                "duration_seconds": 90,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Reorder sections",
            "captain_message": "Drag blocks into best order.",
            "render": {
                "kind": "sortable",
                "blocks": ["Education", "Projects", "Skills", "Goals"],
                "correct_order": ["Education", "Skills", "Projects", "Goals"],
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict best hook",
            "captain_message": "Choose the strongest opening.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Best intro hook?",
                "options": ["I'm good at coding", "I built 3 full-stack projects serving 500 users", "I like computers", "I want a job"],
                "answer_index": 1,
                "explanation": "Quantified achievement is memorable.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build your intro",
            "captain_message": "Write past, present, future sentences.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Past",
                        "placeholder": "I studied...",
                        "answer": "I studied...",
                    },
                    {
                        "label": "Present",
                        "placeholder": "I built...",
                        "answer": "I built...",
                    },
                    {
                        "label": "Future",
                        "placeholder": "I'm excited to...",
                        "answer": "I'm excited to...",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break generic answers",
            "captain_message": "Avoid 'I'm a hard worker'. Show proof.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Which intro is strongest?",
                "options": ["I'm a hard worker", "I led a team of 4 to ship in 3 weeks", "I want to learn", "I need money"],
                "answer_index": 1,
                "explanation": "Specific achievement with metric.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix length",
            "captain_message": "Trim to 60-90 seconds.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Current words",
                        "placeholder": "~200",
                        "answer": "~200",
                    },
                    {
                        "label": "Target words",
                        "placeholder": "~120",
                        "answer": "~120",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to LinkedIn",
            "captain_message": "Same structure: past, present, future.",
            "render": {
                "kind": "recall",
                "prompt": "LinkedIn About section mirrors?",
                "answer": "self-introduction structure",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Hook = quantified achievement. Close = role-specific goal.",
            "render": {
                "kind": "recall",
                "prompt": "Intro closing should mention?",
                "answer": "target role and company fit",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Ideal intro length?",
                "options": ["30s", "60-90s", "3 min", "5 min"],
                "answer": "60-90s",
                "explanation": "60-90 seconds is ideal for interviews.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Best order for intro?",
                "options": ["Future, past, present", "Past, present, future", "Present, past, future", "Random"],
                "answer": "Past, present, future",
                "explanation": "Past → present → future is the standard structure.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Strongest hook?",
                "options": ["I'm smart", "I won 3 hackathons", "I want to learn", "I have a degree"],
                "answer": "I won 3 hackathons",
                "explanation": "Quantified achievement.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Weakness: 'I'm a hard worker'. Fix?",
                "options": ["Add proof", "Say it louder", "Add 'very'", "Repeat"],
                "answer": "Add proof",
                "explanation": "Back claims with evidence.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Best intro close?",
            "options": ["Hire me", "I'm excited to contribute to backend systems at your company", "I need a job", "I'm the best"],
            "answer": "I'm excited to contribute to backend systems at your company",
            "explanation": "Role-specific close shows focus.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Intro structure?",
            "answer": "past, present, future",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Ideal intro length?",
            "answer": "60-90 seconds",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Hook formula?",
            "answer": "quantified achievement",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 6,
            "focus": "Structure, clarity",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 8,
            "focus": "Conciseness, impact",
        },
    ],
    "interview_transfer": {
        "prompt": "Why does self-intro structure help in system design interviews?",
        "model_answer": "It trains starting with requirements (past), current approach (present), and design goals (future).",
    },
}
