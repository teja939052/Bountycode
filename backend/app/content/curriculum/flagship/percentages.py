"""
Flagship Lesson — Percentages
=====================================

Gold-standard interactive lesson for quantitative percentages.

This is the template flagship. It demonstrates the full teaching loop:
Hook → See → Understand → Touch → Predict → Change → Build → Break →
Fix → Retrieve → Transfer → Prove → Reward

Captain Byte is an authored deterministic mentor — not an LLM chatbot.
Visual primitives are instructional, not decorative.
"""
from typing import Dict, Any

SLUG = "percentages"

LESSON: Dict[str, Any] = {
    "lesson_id": "percentages_scale_room",
    "module_id": "aptitude:quantitative:percentages",
    "title": "The Scale Room",
    "description": "Master percentages: basic, successive, reverse, and real placement applications.",
    "difficulty": "beginner",
    "est_minutes": 15,
    "xp_reward": 130,
    "skills_taught": ["percentages", "quantitative", "aptitude"],
    "srs_concept_tag": "aptitude:percentages",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“Welcome to the Scale Room. Every merchant here lives by percentages — "
            "discounts, markups, shares, scores. Before you calculate anything, I want "
            "you to SEE what a percentage actually is. Not memorize. See.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You spotted the pattern before I gave you the formula.”",
            "🧭 **Captain Byte**\n“That’s it. You’re not guessing — you’re reasoning.”",
            "🧭 **Captain Byte**\n“Clean. You’ve got the idea now.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t memorize this yet. Look at what changed.”",
            "🧭 **Captain Byte**\n“You’re calculating before identifying the base. Let’s repair that.”",
            "🧭 **Captain Byte**\n“Close, but you’re treating the percent as an absolute number. Remember: it’s a slice of something.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now fix the formula and the whole thing works.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got the idea. I’m removing the training wheels. Go handle successive changes, reverse percents, and blends on your own.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. This time, identify the base first. What is the 100%?”",
    },
    "story_context": {
        "title": "The Scale Room",
        "narration": (
            "Every merchant in the market uses percentages: discounts, markups, "
            "population growth, and exam scores. Learn the four moves — basic, "
            "successive, reverse, and change — and the room opens."
        ),
        "setting": "scale_room",
        "character": "Captain Byte",
        "intro_text": (
            "Percentages turn fractions into decisions. A 20% discount, a 10% rise, "
            "a 25% score — all the same idea. Master the moves here and you will "
            "recognize them in every OA."
        ),
    },
    "discovery": {
        "title": "Weigh the Scales",
        "visual_primitives": ["highlight", "transform", "compare"],
        "steps": [
            {
                "action": "see_percent",
                "narration": "Before calculating, let's make the percentage visible.",
                "interaction": {
                    "type": "visual_primitive",
                    "primitive": "highlight",
                    "instruction": "Tap the bar to highlight 20% of ₹800.",
                    "visual": {
                        "type": "percent_bar",
                        "total": 800,
                        "percent": 20,
                        "segments": 10,
                        "highlight_segments": 2,
                    },
                    "answer": "160",
                    "hint": "20% means 20 out of every 100. 10% of 800 is 80. Another 10% is 80. Total = 160.",
                },
            },
            {
                "action": "basic_percent",
                "narration": "The simplest move: what is x% of y?",
                "interaction": {
                    "type": "inspect_code",
                    "code": "total = 200\nrate = 15\nresult = total * rate / 100\nprint(result)",
                    "expected_output": "30.0",
                    "hint": "15% of 200 is 30. Multiply first, then divide by 100.",
                },
            },
            {
                "action": "successive_percent",
                "narration": "Two moves in a row do not simply add.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "price = 100\nprice = price * 0.8\nprice = price * 0.9\nprint(price)",
                    "expected_output": "72.0",
                    "hint": "First discount gives 80. Second takes 10% off 80, giving 72.",
                },
            },
            {
                "action": "reverse_percent",
                "narration": "If 30 is 20% of a number, the number is larger.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "part = 30\npct = 20\nwhole = part * 100 / pct\nprint(whole)",
                    "expected_output": "150.0",
                    "hint": "Whole = part × 100 / percent.",
                },
            },
            {
                "action": "percentage_change",
                "narration": "A rise from 80 to 100 is not 20%.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "A price rises from 80 to 100. What is the percentage increase?",
                    "options": [
                        {"id": "a", "text": "25%", "correct": True},
                        {"id": "b", "text": "20%", "correct": False},
                        {"id": "c", "text": "80%", "correct": False},
                        {"id": "d", "text": "100%", "correct": False},
                    ],
                    "explanation": "Increase is 20. Base is 80. 20/80 × 100 = 25%.",
                },
            },
        ],
        "conclusion": (
            "Percentages are just scaled fractions. Basic, successive, reverse, and "
            "change each have one clean formula. Choose the right one and the room "
            "opens."
        ),
    },
    "prediction": {
        "title": "Before You Code",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before I calculate it, predict where the answer will land.”",
        "question": "A shirt costs ₹500. After a 10% discount and then a 10% tax on the discounted price, what is the final price?",
        "options": [
            {"id": "a", "text": "495", "correct": True, "explanation": "500 → 450 after discount → 495 after 10% tax."},
            {"id": "b", "text": "500", "correct": False, "explanation": "The two 10% moves do not cancel; they chain."},
            {"id": "c", "text": "450", "correct": False, "explanation": "450 is after discount only; tax is added next."},
            {"id": "d", "text": "550", "correct": False, "explanation": "550 would be a 10% rise, not a discount then tax."},
        ],
        "explanation": (
            "Discount: 500 × 0.9 = 450. Tax: 450 × 1.1 = 495. Successive percentages chain."
        ),
    },
    "explain": {
        "title": "Explain the Chain",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does a 10% discount followed by a 10% tax not return to the original price? Look at what changed.”",
        "prompt": "Why does a 10% discount followed by a 10% tax not return to the original price?",
        "answer_format": "short_answer",
        "keywords": ["base", "smaller", "discount", "tax", "chain", "successive", "different", "not same"],
        "min_words": 10,
        "model_answer": (
            "The discount reduces the base. The 10% tax is calculated on the reduced "
            "price, not the original. Because the bases differ, the two moves do not "
            "cancel; the final price is lower than the start."
        ),
        "intention": "The explanation must show that successive percentages chain on changing bases.",
    },
    "guided_build": {
        "title": "Price the Parcel",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the formulas. Start simple, then chain them.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Basic Percent",
                "captain_byte_moment": "🧭 **Captain Byte**\n“x% means x out of every 100. Multiply by y, then divide by 100. That’s it.”",
                "description": "Return x% of y.",
                "starter_code": "def percent_of(y, x):\n    # x percent of y\n    pass",
                "function_name": "percent_of",
                "signature": "def percent_of(y: float, x: float) -> float:",
                "test_cases": [
                    {"input": [200, 15], "expected": 30.0},
                    {"input": [100, 25], "expected": 25.0},
                ],
                "hidden_test_cases": [
                    {"input": [0, 10], "expected": 0.0},
                    {"input": [500, 5], "expected": 25.0},
                    {"input": [90, 50], "expected": 45.0},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "x% means x/100. Multiply by y."},
                    {"level": 2, "text": "return y * x / 100"},
                    {"level": 3, "text": "Order does not matter here: y * x / 100 is enough."},
                ],
            },
            {
                "step_order": 2,
                "title": "Successive Discount",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Two discounts chain. Each one shrinks the base for the next.”",
                "description": "Apply two discounts in sequence: first d1%, then d2% on the reduced price.",
                "starter_code": "def successive_discount(price, d1, d2):\n    # apply d1%, then d2%\n    pass",
                "function_name": "successive_discount",
                "signature": "def successive_discount(price: float, d1: float, d2: float) -> float:",
                "test_cases": [
                    {"input": [100, 20, 30], "expected": 56.0},
                    {"input": [500, 10, 10], "expected": 405.0},
                ],
                "hidden_test_cases": [
                    {"input": [200, 50, 50], "expected": 50.0},
                    {"input": [1000, 5, 5], "expected": 902.5},
                    {"input": [0, 20, 30], "expected": 0.0},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "After d1%, the price is price * (1 - d1/100)."},
                    {"level": 2, "text": "Then apply d2% on that result."},
                    {"level": 3, "text": "return price * (1 - d1/100) * (1 - d2/100)"},
                ],
            },
            {
                "step_order": 3,
                "title": "Reverse Percent",
                "captain_byte_moment": "🧭 **Captain Byte**\n“You have the part. You need the whole. Multiply by 100, then divide by the percent.”",
                "description": "If `part` is `pct`% of a whole, return the whole.",
                "starter_code": "def reverse_percent(part, pct):\n    # find the whole\n    pass",
                "function_name": "reverse_percent",
                "signature": "def reverse_percent(part: float, pct: float) -> float:",
                "test_cases": [
                    {"input": [30, 20], "expected": 150.0},
                    {"input": [50, 25], "expected": 200.0},
                ],
                "hidden_test_cases": [
                    {"input": [0, 10], "expected": 0.0},
                    {"input": [10, 50], "expected": 20.0},
                    {"input": [99, 33], "expected": 300.0},
                ],
                "diamonds": 40,
                "scaffolded_hints": [
                    {"level": 1, "text": "If 20% gives 30, then 100% gives more."},
                    {"level": 2, "text": "Multiply by 100, then divide by the percent."},
                    {"level": 3, "text": "return part * 100 / pct"},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Merchant's Mix",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same idea, new context. Two prices, two quantities. Blend them.”",
        "description": (
            "A merchant mixes two rice varieties. 20 kg at ₹40/kg and 30 kg at ₹60/kg. "
            "Find the effective per-kg cost."
        ),
        "function_name": "blended_cost",
        "signature": "def blended_cost(q1: int, p1: float, q2: int, p2: float) -> float:",
        "description_full": (
            "Return the blended cost per kg as a float.\n\n"
            "Example:\n"
            "  blended_cost(20, 40, 30, 60) -> 52.0\n\n"
            "Hidden tests use integer and float inputs."
        ),
        "test_cases": [
            {"input": [20, 40, 30, 60], "expected": 52.0},
            {"input": [10, 100, 10, 200], "expected": 150.0},
        ],
        "hidden_test_cases": [
            {"input": [0, 40, 30, 60], "expected": 60.0},
            {"input": [20, 40, 0, 60], "expected": 40.0},
            {"input": [1, 1, 1, 1], "expected": 1.0},
        ],
        "time_limit_minutes": 7,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Total cost = (q1 * p1) + (q2 * p2). Total kg = q1 + q2."},
            {"level": 2, "text": "Blended cost = total_cost / total_kg."},
            {"level": 3, "text": "Return a float; division does that automatically."},
        ],
    },
    "assessment": {
        "title": "Scale Room Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you’ve got it. Timed. No hints.”",
        "description": "Trace percentages through basic, successive, reverse, and a blend.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "p = 1000\np = p * 0.9\np = p * 1.1\nprint(p)",
                "answer_format": "single_number",
                "expected_answer": "990.0",
                "explanation": "1000 → 900 after 10% off → 990 after 10% tax on reduced price.",
            },
            {
                "type": "concept",
                "question": "If 40 is 25% of a number, what is the number?",
                "answer_format": "single_number",
                "keywords": ["160", "reverse", "whole", "part", "percent"],
                "expected_answer": "160",
                "explanation": "Whole = part * 100 / percent = 40 * 100 / 25 = 160.",
            },
            {
                "type": "debug",
                "code": "def discount(price, rate):\n    return price - rate\n# should apply a percent discount",
                "error": "discount(100, 20) must return 80.0, but returns 80.",
                "question": "Fix the formula.",
                "fix": "return price * (1 - rate / 100)",
                "explanation": "rate is a percent, not an absolute amount.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Wrong Base",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I gave you a broken solution. Find the wrong assumption before you fix it.”",
        "story": (
            "A clerk calculated a 20% rise on 120 by adding 20. The correct answer is 144. "
            "Find the wrong assumption."
        ),
        "buggy_code": "def rise(x):\n    return x + 20\n\nprint(rise(120))",
        "expected_output": "144",
        "actual_output": "140 (20 was added as an absolute number, not a percentage)",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "20 was added as an absolute value instead of computing 20% of 120", "correct": True, "why": "20% of 120 is 24; 120 + 24 = 144."},
                {"id": "b", "text": "The function should multiply instead of add", "correct": False, "why": "120 * 20 is 2400, not 144."},
                {"id": "c", "text": "The starting value is wrong", "correct": False, "why": "120 is correct."},
                {"id": "d", "text": "print should not be inside the function", "correct": False, "why": "print outside is fine."},
            ],
        },
        "fix": "return x + x * 20 / 100",
        "fixed_code": "def rise(x):\n    return x + x * 20 / 100\n\nprint(rise(120))",
        "explanation": (
            "20% of 120 is 24. Adding 24 gives 144. Adding 20 treats the percent as an absolute amount."
        ),
    },
    "srs_enrollment": {
        "concept_id": "aptitude:percentages",
        "concept_name": "Percentages",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "basic percent = part * 100 / whole",
            "successive percentages chain on changing bases",
            "reverse percent finds the whole from a part",
            "percentage change uses the original value as base",
        ],
        "spaced_fields": [
            "basic_percent",
            "successive_chain",
            "reverse_percent",
            "percentage_change",
        ],
    },
    "world_progression": {
        "world_id": "aptitude_world",
        "competency_id": "percentages",
        "unlocks_next": ["ratio_proportion"],
        "tower_badge": "scale_room",
        "world_node": {
            "level": 1,
            "title": "The Scale Room",
            "color": "amber",
            "icon": "⚖️",
            "description": "Master basic, successive, reverse, and change percentages",
        },
    },
}
