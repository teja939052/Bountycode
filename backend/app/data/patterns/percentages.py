"""Pattern Pack — Percentages.

Authoring notes:
- teaching[i].type is one of: visual, manipulate, predict, change, build,
  break, fix, recall, transfer, placement
- Each teaching step has a ``render`` block that the frontend turns into
  an interactive React component.
- Practice questions are trusted question-bank IDs or inline fallbacks.
- Retention cards are SRS prompts.
"""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "percentages",
    "name": "Percentages",
    "emoji": "📐",
    "round_id": "aptitude",
    "purpose": "Convert between fractions, decimals, and percentages; calculate percentage change; handle successive changes without error.",
    "prerequisites": ["fractions", "decimals", "basic-multiplication"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Percentage vs percentage points",
            "description": "Treats a change from 20% to 25% as 5 percentage points but answers '25%'.",
        },
        {
            "id": "M2",
            "label": "Wrong base",
            "description": "Applies the percent to the wrong quantity in 'x% of y' or 'y is x% of ?'.",
        },
        {
            "id": "M3",
            "label": "Additive successive changes",
            "description": "Adds two percentage changes instead of multiplying their factors.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "What does % mean?",
            "captain_message": "Most students calculate everything. You're going to learn to see the change first.",
            "render": {
                "kind": "bar",
                "base": 1000,
                "discount_pct": 20,
                "highlight_final": True,
                "show_fraction": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Move the discount",
            "captain_message": "Change the percentage. Watch the bar shrink.",
            "render": {
                "kind": "slider",
                "base": 1000,
                "min": 0,
                "max": 100,
                "default": 20,
                "show_final_price": True,
                "formula": "final = base * (1 - pct/100)",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict before calculating",
            "captain_message": "Don't touch the slider. Choose the final price from memory.",
            "render": {
                "kind": "multiple_choice",
                "base": 1000,
                "pct": 25,
                "options": [250, 750, 725, 775],
                "answer_index": 1,
                "explanation": "25% of 1000 is 250. Final = 1000 - 250 = 750.",
            },
        },
        {
            "id": "change",
            "type": "change",
            "title": "Change the base",
            "captain_message": "Now the marked price is ₹2,000. Same 25%. What changes?",
            "render": {
                "kind": "slider",
                "base": 2000,
                "min": 0,
                "max": 100,
                "default": 25,
                "show_final_price": True,
                "prompt": "Is the discount amount the same? Is the final price doubled?",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the calculation",
            "captain_message": "Write the two-step formula. Not the number — the structure.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "discount amount",
                        "placeholder": "base * percent / 100",
                        "answer": "base * percent / 100",
                    },
                    {
                        "label": "final price",
                        "placeholder": "base - discount_amount",
                        "answer": "base - discount_amount",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break it",
            "captain_message": "This answer looks reasonable. That's why it's dangerous.",
            "render": {
                "kind": "debug_solution",
                "buggy_code": "final = base - percent",
                "question": "A shirt costs ₹1,200. 20% discount. Student wrote: 1200 - 20 = 1180.",
                "expected_failure": "Subtracts the percentage number directly instead of the discount amount.",
                "diagnosis_code": "wrong_base",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix the mistake",
            "captain_message": "Find the line and repair it.",
            "render": {
                "kind": "fix_expression",
                "broken": "final = base - percent",
                "fix_hint": "discount = base * percent / 100",
                "answer": "final = base - (base * percent / 100)",
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer: successive changes",
            "captain_message": "Same idea. Different surface. Don't add the percentages.",
            "render": {
                "kind": "successive_change",
                "base": 1000,
                "first_pct": 15,
                "second_pct": 10,
                "common_wrong": 1000 * (1 - (15+10)/100),
                "correct": 1000 * 0.85 * 0.90,
                "explanation": "Successive decreases multiply: 0.85 × 0.90 = 0.765.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "TCS-style proof",
            "captain_message": "No bar. No slider. Just you and the clock.",
            "render": {
                "kind": "timed_question",
                "seconds": 60,
                "question": "A product is marked ₹500. It is sold at a 20% discount, then the shopkeeper adds a 10% profit on the selling price. What is the final selling price?",
                "options": ["₹440", "₹450", "₹460", "₹480"],
                "answer_index": 0,
                "explanation": "SP after discount = 500 × 0.8 = 400. Profit = 400 × 0.10 = 40. Final = 440.",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "pct-w1",
                "topic": "percentages",
                "difficulty": "easy",
                "question": "What is 25% of 200?",
                "options": ["25", "50", "75", "100"],
                "answer": "50",
                "explanation": "25% = 1/4. 200/4 = 50.",
            },
            {
                "id": "pct-w2",
                "topic": "percentages",
                "difficulty": "easy",
                "question": "40 is what % of 200?",
                "options": ["10%", "20%", "25%", "40%"],
                "answer": "20%",
                "explanation": "(40/200) × 100 = 20%.",
            },
            {
                "id": "pct-w3",
                "topic": "percentages",
                "difficulty": "easy",
                "question": "If a number increases by 20%, the new number is what % of the original?",
                "options": ["80%", "100%", "120%", "125%"],
                "answer": "120%",
                "explanation": "Original + 20% of original = 120%.",
            },
        ],
        "drill": [
            {
                "id": "pct-d1",
                "topic": "percentages",
                "difficulty": "medium",
                "question": "A student scored 60% marks and failed by 30 marks. Another scored 72% and passed by 18 marks. What is the maximum marks?",
                "options": ["300", "450", "500", "600"],
                "answer": "500",
                "explanation": "Let max = x. 0.6x + 30 = passing = 0.72x - 18 → x = 500.",
            },
        ],
        "speed_run": [
            {
                "id": "pct-s1",
                "topic": "percentages",
                "difficulty": "medium",
                "question": "If 40% of a number is 80, what is 60% of the same number?",
                "options": ["100", "110", "120", "130"],
                "answer": "120",
                "explanation": "40% → 80, so 1% → 2. 60% → 120.",
            },
        ],
        "weakness_repair": [
            {
                "id": "pct-r1",
                "topic": "percentages",
                "difficulty": "medium",
                "question": "A number is increased by 20% and then decreased by 20%. The net change is:",
                "options": ["0%", "4% decrease", "4% increase", "2% decrease"],
                "answer": "4% decrease",
                "explanation": "1.2 × 0.8 = 0.96. Net = -4%. Common error: add/subtract percentages.",
                "diagnosis_code": "additive_successive",
            },
        ],
    },
    "assessment": [
        {
            "id": "pct-a1",
            "topic": "percentages",
            "difficulty": "medium",
            "question": "A shopkeeper marks his goods 30% above cost price and allows a discount of 15%. What is his profit %?",
            "options": ["10.5%", "12%", "13.5%", "15%"],
            "answer": "10.5%",
            "explanation": "MP = 1.3 CP. SP = 1.3 × 0.85 = 1.105 CP. Profit = 10.5%.",
        },
    ],
    "retention": [
        {
            "id": "pct-ret-1d",
            "due_days": 1,
            "prompt": "A price rises 10%, then falls 10%. Is the final price equal to the original?",
            "answer": "No — it is 0.99 × original.",
            "diagnosis_code": "additive_successive",
        },
        {
            "id": "pct-ret-3d",
            "due_days": 3,
            "prompt": "If 30% of x = 90, what is 50% of x?",
            "answer": "150",
            "diagnosis_code": "wrong_base",
        },
        {
            "id": "pct-ret-7d",
            "due_days": 7,
            "prompt": "Two successive discounts of 20% and 10% are equivalent to a single discount of:",
            "answer": "28%",
            "options": ["30%", "28%", "25%", "22%"],
            "diagnosis_code": "additive_successive",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "TCS NQT quantitative ability",
            "question_count": 3,
        },
        {
            "company": "infosys",
            "difficulty": "medium",
            "timing_seconds": 45,
            "context": "InfyTQ quantitative",
            "question_count": 2,
        },
        {
            "company": "wipro",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "Wipro NLTH quant",
            "question_count": 3,
        },
    ],
    "interview_transfer": {
        "prompt": "Explain percentage change to a non-technical interviewer in 30 seconds.",
        "model_answer": "Percentage change measures relative movement. A 20% increase followed by 20% decrease is not zero — it is a 4% net loss because the second change applies to the already-increased base.",
        "success_criteria": ["mentions base change", "mentions multiplicative not additive", "gives numeric example"],
    },
}
