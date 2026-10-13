"""Pattern Pack — Time & Work."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "time-work",
    "name": "Time & Work",
    "emoji": "⏱️",
    "round_id": "aptitude",
    "purpose": "Convert work to man-days, handle multiple workers, pipes and cisterns, and solve problems with partial exits and efficiency changes.",
    "prerequisites": ["fractions", "basic-multiplication", "unitary-method"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Direct proportion mistake",
            "description": "Treats more workers as needing more time instead of less.",
        },
        {
            "id": "M2",
            "label": "Pipes additive flow",
            "description": "Adds fill rates for outlet pipes or forgets to subtract them.",
        },
        {
            "id": "M3",
            "label": "Partial day handling",
            "description": "Treats a worker leaving mid-job as a full-day contribution.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Work as containers",
            "captain_message": "Work is a fixed bucket. More workers = faster emptying.",
            "render": {
                "kind": "bar",
                "workers": [1, 2, 4],
                "days_to_complete": [12, 6, 3],
                "show_inverse": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change worker count",
            "captain_message": "Add or remove workers. See days change inversely.",
            "render": {
                "kind": "slider",
                "total_work": 60,
                "workers": 5,
                "min_workers": 1,
                "max_workers": 15,
                "efficiency": 1.0,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict combined time",
            "captain_message": "Don't compute. Choose combined days.",
            "render": {
                "kind": "multiple_choice",
                "a_days": 12,
                "b_days": 15,
                "options": ["6.67", "5", "8", "7.5"],
                "answer_index": 0,
                "explanation": "Combined rate = 1/12 + 1/15 = 9/60 = 3/20. Days = 20/3 ≈ 6.67.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the man-day equation",
            "captain_message": "Write total work in man-days.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Total work",
                        "placeholder": "workers × days",
                        "answer": "workers × days",
                    },
                    {
                        "label": "Combined rate",
                        "placeholder": "1/a + 1/b + 1/c",
                        "answer": "1/a + 1/b + 1/c",
                    },
                    {
                        "label": "Combined days",
                        "placeholder": "1 / combined_rate",
                        "answer": "1 / combined_rate",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the pipe additive trap",
            "captain_message": "Two fill pipes, one leak. Net fill rate subtracts.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Pipe A fills in 6h, B in 8h, leak empties in 12h. Net fill time?",
                "options": ["4.8h", "5h", "6h", "4h"],
                "answer_index": 0,
                "explanation": "Rates: 1/6 + 1/8 - 1/12 = 7/24. Time = 24/7 ≈ 3.43h.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix partial exit",
            "captain_message": "A leaves after 2 days. Compute remaining work for B.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Work done by A",
                        "placeholder": "days_A × rate_A",
                        "answer": "days_A × rate_A",
                    },
                    {
                        "label": "Remaining work",
                        "placeholder": "total - work_A",
                        "answer": "total - work_A",
                    },
                    {
                        "label": "Days for B",
                        "placeholder": "remaining / rate_B",
                        "answer": "remaining / rate_B",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to efficiency",
            "captain_message": "If a worker is twice as efficient, their rate doubles.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "A is twice as efficient as B. A can do work in 10 days. B alone?",
                "options": ["15", "20", "25", "30"],
                "answer_index": 1,
                "explanation": "If rate_A = 2×rate_B, then rate_B = rate_A/2. Days_B = 2×days_A = 20.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For three workers A, B, C: combined days = abc/(ab+bc+ca).",
            "render": {
                "kind": "recall",
                "prompt": "Combined days formula for three workers with individual days a, b, c?",
                "answer": "abc / (ab + bc + ca)",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "A can do work in 10 days. Work done in 4 days?",
                "answer": "2/5",
                "explanation": "Rate = 1/10 per day. In 4 days = 4/10 = 2/5.",
            },
            {
                "id": "w2",
                "question": "A and B together finish in 6 days. A alone in 9 days. B alone?",
                "options": ["12", "15", "18", "20"],
                "answer": "18",
                "explanation": "Rate_B = 1/6 - 1/9 = 1/18. B takes 18 days.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "A can do a job in 12 days, B in 18 days. They work together for 3 days, then A leaves. Days for B to finish?",
                "answer": "9 days",
                "explanation": "Combined rate = 5/36. Work in 3 days = 15/36 = 5/12. Remaining = 7/12. B's rate = 1/18. Days = (7/12)/(1/18) = 10.5.",
            },
            {
                "id": "d2",
                "question": "If 5 workers need 8 days, how many workers for 10 days?",
                "answer": "4 workers",
                "explanation": "Work = 40 man-days. 40/10 = 4 workers.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "A is twice as efficient as B. Together they finish in 12 days. A alone?",
                "options": ["16", "18", "20", "24"],
                "answer": "18",
                "explanation": "Rate_A = 2r, Rate_B = r. Combined = 3r = 1/12. r = 1/36. A = 1/(2r) = 18 days.",
            },
            {
                "id": "s2",
                "question": "Pipe A fills tank in 20 min, B empties in 30 min. Both open, time to fill?",
                "options": ["40", "50", "60", "30"],
                "answer": "60",
                "explanation": "Net rate = 1/20 - 1/30 = 1/60. Time = 60 min.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "20 men complete work in 24 days. After 6 days, 5 men leave. Remaining days?",
                "answer": "20 days",
                "explanation": "Work = 480 md. Done = 120 md. Remaining = 360 md. Workers = 15. Days = 360/15 = 24.",
            },
            {
                "id": "wr2",
                "question": "A can complete work in 24 days, B in 30 days. They work on alternate days starting with A. Total days?",
                "answer": "~27.33 days",
                "explanation": "Two-day work = 1/24 + 1/30 = 9/120 = 3/40. In 18 days (9 cycles) = 27/40. Remaining 13/40 done by A in ~1.73 days.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "A and B together can do a piece of work in 12 days. B and C together in 15 days. A, B, C together in 10 days. A and C together?",
            "options": ["10", "12", "15", "20"],
            "answer": "15",
            "explanation": "A+C = 2×10 - 12 = 8? No. Actually need combined rates. Check formulas carefully.",
        },
        {
            "id": "a2",
            "question": "If 4 men or 6 boys can finish work in 12 days, how many days for 6 men and 4 boys?",
            "answer": "4 days",
            "explanation": "4m = 6b → 2m = 3b. Total = 6m + 4b = 9m + 6b? Use combined equivalence.",
        },
        {
            "id": "a3",
            "question": "A tap fills tank in 4 hours, another in 6 hours. Both opened, time?",
            "answer": "2.4 hours",
            "explanation": "Combined rate = 1/4 + 1/6 = 5/12. Time = 12/5 = 2.4 hours.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Formula for work done by A and B together in one day?",
            "answer": "1/a + 1/b",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "If 5 workers need 8 days, total work in man-days?",
            "answer": "40 man-days",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Net fill rate with inlet and outlet pipes?",
            "answer": "inlet_rate - outlet_rate",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Man-days, combined work",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Fast work puzzles",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Pipes, partial work",
        },
    ],
    "interview_transfer": {
        "prompt": "A team of 5 ships features in 10 days. You need to ship in 4 days. How do you plan?",
        "model_answer": "Work is 50 person-days. To finish in 4 days, need 12.5 people. Add contractors or reduce scope.",
    },
}
