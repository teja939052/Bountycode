"""Pattern Pack — Ratio & Proportion.

Authoring notes:
- teaching[i].type is one of: visual, manipulate, predict, change, build,
  break, fix, recall, transfer, placement
"""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "ratio-proportion",
    "name": "Ratio & Proportion",
    "emoji": "⚖️",
    "round_id": "aptitude",
    "purpose": "Compare quantities using ratios, solve direct/indirect proportion problems, and apply ratios to mixtures, partnerships, and time-speed-distance.",
    "prerequisites": ["fractions", "basic-multiplication", "unitary-method"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Ratio vs fraction",
            "description": "Treats 2:3 as the fraction 2/3 instead of 2/5 or '2 parts out of 5'.",
        },
        {
            "id": "M2",
            "label": "Inverse proportion direction",
            "description": "Keeps speed and time in direct proportion for TSD, causing constant-distance errors.",
        },
        {
            "id": "M3",
            "label": "Proportion cross-multiply sign errors",
            "description": "Cross-multiplies but flips one side: a/b = c/d → a*d = b/c.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Parts, not just numbers",
            "captain_message": "A ratio describes sharing. Visualize parts before computing.",
            "render": {
                "kind": "bar",
                "parts": [2, 3],
                "total": 50,
                "highlight_unit_value": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the total",
            "captain_message": "Adjust the total quantity. See how each part scales.",
            "render": {
                "kind": "slider",
                "parts": [2, 3],
                "min_total": 20,
                "max_total": 200,
                "default_total": 50,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the share",
            "captain_message": "Don't calculate. Choose the share from memory.",
            "render": {
                "kind": "multiple_choice",
                "ratio": "3:2",
                "total": 100,
                "options": [40.0, 60.0, 30.0, 50.0],
                "answer_index": 1,
                "explanation": "3+2 = 5 parts. One part = 20. Share = 3*20 = 60.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the proportion",
            "captain_message": "Write the cross-multiplication setup. No final number.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Set up equivalent ratios",
                        "placeholder": "a/b = c/d",
                        "answer": "a/b = c/d",
                    },
                    {
                        "label": "Cross-multiply",
                        "placeholder": "a*d = b*c",
                        "answer": "a*d = b*c",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the inverse case",
            "captain_message": "More workers means less time. Prove it with numbers.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "If 6 workers need 12 days, how many days for 8 workers?",
                "options": [8, 9, 10, 14],
                "answer_index": 1,
                "explanation": "Workers and days are inversely proportional. 6*12 = 8*x → x = 9.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix the mixture setup",
            "captain_message": "Water and wine in different ratios. Find the mixing ratio.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Alcohol in first mixture",
                        "placeholder": "quantity1 * ratio1",
                        "answer": "quantity1 * ratio1",
                    },
                    {
                        "label": "Alcohol in second mixture",
                        "placeholder": "quantity2 * ratio2",
                        "answer": "quantity2 * ratio2",
                    },
                    {
                        "label": "Final ratio equation",
                        "placeholder": "final_ratio = (alc1 + alc2) / (q1 + q2)",
                        "answer": "final_ratio = (alc1 + alc2) / (q1 + q2)",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to partnership",
            "captain_message": "Investment time maps to ratio. Apply it to profit sharing.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "A invests ₹50k for 6 months, B invests ₹40k for 5 months. Profit ratio?",
                "options": ["3:2", "5:4", "6:5", "25:20"],
                "answer_index": 0,
                "explanation": "A:B = 50k*6 : 40k*5 = 300:200 = 3:2.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "When one quantity changes by x/y, the other changes by y/x in inverse proportion.",
            "render": {
                "kind": "recall",
                "prompt": "For inverse proportion, if speed increases by 3/2, time changes by?",
                "answer": "2/3",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Divide ₹500 in the ratio 3:2.",
                "options": ["₹300, ₹200", "₹250, ₹250", "₹350, ₹150", "₹200, ₹300"],
                "answer": "₹300, ₹200",
                "explanation": "5 parts = 500 → 1 part = 100. 3 parts = 300, 2 parts = 200.",
            },
            {
                "id": "w2",
                "question": "If a:b = 2:3 and b:c = 4:5, find a:c.",
                "options": ["8:15", "2:5", "6:15", "4:5"],
                "answer": "8:15",
                "explanation": "Make b equal: a:b = 8:12, b:c = 12:15 → a:c = 8:15.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "A mixture contains alcohol and water in ratio 4:1. After adding 10L water, ratio becomes 2:3. Find initial alcohol.",
                "answer": "8L",
                "explanation": "Let alcohol = 4x, water = x. After adding 10L water: 4x/(x+10) = 2/3.",
            },
            {
                "id": "d2",
                "question": "If 7 workers can build a wall in 12 days, how many days for 9 workers?",
                "answer": "28/3 days ≈ 9.33 days",
                "explanation": "Workers and days are inversely proportional: 7×12 = 9×x → x = 28/3.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Salaries of A, B, C are in ratio 5:3:2. If C gets ₹2000, what is A?",
                "answer": "₹5000",
                "explanation": "2 parts = 2000 → 1 part = 1000. A gets 5 parts = 5000.",
            },
            {
                "id": "s2",
                "question": "Seats increased by 40% and then decreased by 40%. Net change?",
                "options": ["0%", "-8%", "-16%", "-24%"],
                "answer": "-16%",
                "explanation": "Multiplicative: 1.4 × 0.6 = 0.84. Net change = -16%.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "A is 20% more than B. B is what percent less than A?",
                "options": ["16.67%", "20%", "25%", "10%"],
                "answer": "16.67%",
                "explanation": "If B = 100, A = 120. B is 20/120 = 16.67% less than A. Base changes.",
            },
            {
                "id": "wr2",
                "question": "If price increases by 10% and consumption decreases by 10%, expenditure?",
                "options": ["Increases 1%", "Decreases 1%", "No change", "Increases 10%"],
                "answer": "Decreases 1%",
                "explanation": "Expenditure = price × quantity. Multiplicative: 1.1 × 0.9 = 0.99.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Two numbers are in ratio 3:5. If 8 is added to each, ratio becomes 2:3. Find the numbers.",
            "options": ["12, 20", "15, 25", "18, 30", "9, 15"],
            "answer": "12, 20",
            "explanation": "Let numbers be 3x, 5x. (3x+8)/(5x+8) = 2/3 → x = 4. Numbers = 12, 20.",
        },
        {
            "id": "a2",
            "question": "A can do a piece of work in 20 days, B in 30 days. They work together for 5 days, then A leaves. How many more days does B take?",
            "answer": "15 days",
            "explanation": "Combined rate = 1/20 + 1/30 = 5/60 = 1/12. In 5 days they do 5/12. Remaining 7/12 at B's rate 1/30 → 7/12 × 30 = 17.5 days.",
        },
        {
            "id": "a3",
            "question": "In what ratio must tea at ₹60/kg be mixed with tea at ₹80/kg to get mixture worth ₹68/kg?",
            "options": ["3:2", "2:3", "1:2", "4:3"],
            "answer": "3:2",
            "explanation": "Allegation: (80-68):(68-60) = 12:8 = 3:2.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "What is the formula for direct proportion?",
            "answer": "a/b = c/d or a = k×b",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "If 12 workers need 15 days, how many days for 18 workers?",
            "answer": "10 days",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "In inverse proportion, if x doubles, y?",
            "answer": "Halves",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Simpler ratio, direct/inverse, basic TSD",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Fast arithmetic, mixture, partnership",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Proportion basics, TSD, work",
        },
        {
            "company": "google",
            "timing_seconds": 90,
            "question_count": 6,
            "focus": "Analytical ratio puzzles, scaling",
        },
    ],
    "interview_transfer": {
        "prompt": "A product manager says engagement dropped 20% and active users grew 10%. How do you evaluate net impact?",
        "model_answer": "Use multiplicative change: engagement rate × users. Treat proportions independently, not additively. Break into cohort-level ratios if available.",
    },
}
