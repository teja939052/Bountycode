"""Pattern Pack — Profit & Loss."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "profit-loss",
    "name": "Profit & Loss",
    "emoji": "💰",
    "round_id": "aptitude",
    "purpose": "Compute profit/loss percentages, handle discounts and marked price, and solve successive profit/loss and true-cost problems.",
    "prerequisites": ["percentages", "fractions", "basic-multiplication"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Profit on cost vs selling price",
            "description": "Applies profit percent to selling price instead of cost price.",
        },
        {
            "id": "M2",
            "label": "Additive successive changes",
            "description": "Adds two successive profit percentages instead of multiplying factors.",
        },
        {
            "id": "M3",
            "label": "Discount direction",
            "description": "Treats discount as increasing the marked price instead of decreasing it.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Cost, MRP, and selling price",
            "captain_message": "See the three prices. Profit sits between cost and selling price.",
            "render": {
                "kind": "bar",
                "cost": 800,
                "marked": 1000,
                "sell": 900,
                "highlight_profit_region": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Move the discount",
            "captain_message": "Change the discount percent. See MRP and SP move.",
            "render": {
                "kind": "slider",
                "cost": 800,
                "marked": 1200,
                "min_discount": 0,
                "max_discount": 50,
                "default_discount": 20,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict profit percent",
            "captain_message": "Don't calculate. Choose the right profit percent.",
            "render": {
                "kind": "multiple_choice",
                "cost": 500,
                "sell": 600,
                "options": ["16.67%", "20%", "25%", "10%"],
                "answer_index": 1,
                "explanation": "Profit = 100 on cost 500 → 100/500 = 20%.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the discount formula",
            "captain_message": "Write the relationship between MRP, discount, and SP.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Discount amount",
                        "placeholder": "mrp * discount_percent / 100",
                        "answer": "mrp * discount_percent / 100",
                    },
                    {
                        "label": "Selling price",
                        "placeholder": "mrp - discount_amount",
                        "answer": "mrp - discount_amount",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break successive profit",
            "captain_message": "Two successive profits of 20% each. Is total 40%?",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Successive profits of 20% and 20%. Net profit?",
                "options": ["40%", "44%", "36%", "42%"],
                "answer_index": 1,
                "explanation": "Multiplicative: 1.2 × 1.2 = 1.44. Net profit = 44%.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix true cost from profit on selling price",
            "captain_message": "Profit is 10% on SP. Find true profit percent on CP.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Assume SP",
                        "placeholder": "sp = 100",
                        "answer": "sp = 100",
                    },
                    {
                        "label": "Find CP",
                        "placeholder": "cp = sp / 1.1",
                        "answer": "cp = sp / 1.1",
                    },
                    {
                        "label": "Profit percent on CP",
                        "placeholder": "profit = (sp - cp) / cp * 100",
                        "answer": "profit = (sp - cp) / cp * 100",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to discount pass-through",
            "captain_message": "A shopkeeper gives 10% discount but adds 10% extra cost. Net?",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Markup 10% then discount 10%. Net profit/loss?",
                "options": ["1% loss", "1% profit", "No change", "0.1% profit"],
                "answer_index": 1,
                "explanation": "Multiplicative: 1.1 × 0.9 = 0.99 → 1% loss on cost.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For successive changes, multiply factors: (1 + p1/100)(1 + p2/100) - 1.",
            "render": {
                "kind": "recall",
                "prompt": "Net change formula for successive +20% and -10%?",
                "answer": "(1.2 × 0.9) - 1 = 0.08 = 8%",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "CP = ₹200, SP = ₹250. Profit percent?",
                "answer": "25%",
                "explanation": "Profit = 50. Profit% = 50/200 × 100 = 25%.",
            },
            {
                "id": "w2",
                "question": "Marked price ₹1000, discount 10%. Selling price?",
                "answer": "₹900",
                "explanation": "Discount = 100. SP = 1000 - 100 = 900.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "A shopkeeper gains 20% by selling 10 apples for ₹12. Cost per apple?",
                "answer": "₹1",
                "explanation": "SP of 10 = 12. CP of 10 = 12/1.2 = 10. Per apple = 1.",
            },
            {
                "id": "d2",
                "question": "If CP of 5 articles equals SP of 4 articles, profit percent?",
                "options": ["20%", "25%", "16.67%", "30%"],
                "answer": "25%",
                "explanation": "Assume CP = 20/ea, 5 CP = 100 = 4 SP → SP = 25. Profit = 5 on 20 = 25%.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "A fan listed at ₹1500 with 10% discount. What discount on marked price to keep SP same?",
                "options": ["10%", "11.11%", "9%", "12%"],
                "answer": "11.11%",
                "explanation": "SP = 1500×0.9 = 1350. To get 1350 from 1500, discount = 150/1500 = 10%.",
            },
            {
                "id": "s2",
                "question": "A trader marks goods 50% above CP and gives 20% discount. Profit percent?",
                "answer": "20%",
                "explanation": "MP = 150, SP = 120. Profit = 20 on 100 = 20%.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "A sells to B at 20% profit, B to C at 25% profit. If C pays ₹300, what did A pay?",
                "answer": "₹200",
                "explanation": "Work backwards: CP_A × 1.2 × 1.25 = 300 → CP_A = 300/1.5 = 200.",
            },
            {
                "id": "wr2",
                "question": "Loss of 10% on SP means what percent loss on CP?",
                "answer": "11.11%",
                "explanation": "Loss = 10 on SP = 100 → CP = 110. Loss% on CP = 10/110 × 100 ≈ 9.09%.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "By selling an article for ₹1200, a shopkeeper loses 20%. What is CP?",
            "answer": "₹1500",
            "explanation": "SP = 80% of CP. CP = 1200/0.8 = 1500.",
        },
        {
            "id": "a2",
            "question": "A dishonest shopkeeper uses 950g for 1kg and sells at CP. Profit percent?",
            "answer": "5.26%",
            "explanation": "He gives 950g but charges for 1000g. Profit = 50/950 × 100 ≈ 5.26%.",
        },
        {
            "id": "a3",
            "question": "If profit percent is 25% on CP, what is it on SP?",
            "answer": "20%",
            "explanation": "SP = 125, profit = 25. Profit% on SP = 25/125 × 100 = 20%.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Profit percent formula on cost price?",
            "answer": "(SP - CP) / CP × 100",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "Formula for selling price after discount?",
            "answer": "MP × (1 - discount_percent/100)",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Net change for two successive profits of x% and y%?",
            "answer": "x + y + xy/100",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Profit%, discount, successive changes",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Fast profit puzzles",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Discount, CP/SP basics",
        },
    ],
    "interview_transfer": {
        "prompt": "A startup's revenue grew 40% but costs grew 50%. How do you explain the margin impact?",
        "model_answer": "Use multiplicative model: new margin = revenue×1.4 / cost×1.5. Compare percent changes relative to bases, not additively.",
    },
}
