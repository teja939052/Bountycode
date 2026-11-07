"""Quantitative Aptitude — Interactive lessons for service-company placement.

Follows the exact teaching standard of World 1 Foundations:
discover → manipulate → predict → build → break → debug → retrieve → transfer → mastery.

Primary target: TCS NQT / Infosys / Wipro / Accenture Numerical Ability.
Every lesson teaches the underlying math first, then speed techniques.
"""
from __future__ import annotations

from app.content.lesson_definitions import (
    LessonDefinition,
    LessonStep,
    TownDefinition,
    WorldDefinition,
)


# ───────────────────────────────────────────────────────────────────
# TOWN 1 — PERCENTAGES (highest frequency in every service-company test)
# ───────────────────────────────────────────────────────────────────

PERCENTAGES_TOWN = TownDefinition(
    id="percentages",
    name="Percentages",
    icon="%",
    description="The language of change. Master this and half of Numerical Ability becomes easy.",
    order=1,
    mental_model="A percentage is always 'parts out of 100'. The original value is almost always the base.",
    canonical_skills=["aptitude.percentages"],
    competencies=[
        "percentage_meaning",
        "percent_of_quantity",
        "percentage_increase",
        "percentage_decrease",
        "successive_change",
        "reverse_percentage",
        "percentage_comparison",
    ],
    lessons=[
        # ─── Lesson 1: What % really means ───
        LessonDefinition(
            id="pct-1",
            title="What Percentage Means",
            icon="1",
            order=1,
            concept="percentage_meaning",
            mental_model="x% means x parts out of every 100 parts. It is a fraction with denominator 100.",
            canonical_skill="aptitude.percentages",
            location="Market Square — Price Board",
            npc="Ravi the Shopkeeper",
            npc_line="Every discount board says 20% off. Students still treat 20% as the number 20. Help them see it as a fraction of 100.",
            tutor_discover="Percentage is just a special fraction whose denominator is always 100.",
            tutor_explain="25% = 25/100 = 1/4 = 0.25. Saying '25 percent' is the same as saying 'one quarter'.",
            why_this_matters="Almost every numerical question in TCS NQT, Infosys and Wipro uses percentages. If the base is wrong, the entire answer is wrong.",
            engineering_context="In product metrics we talk about conversion rate, churn, growth — all percentages. In finance, returns and discounts are percentages. The concept is universal.",
            builds_toward="NQT Numerical Ability — every section",
            steps=[
                LessonStep(
                    step_type="discover",
                    title="The Price Board",
                    content="A shirt costs ₹1000. The board says '20% off'. What does 20% actually mean?",
                    visual="1000 ÷ 100 = 10  →  each 1% is ₹10  →  20% = 20 × 10 = ₹200 off",
                    interaction="select-value",
                    prompt="20% of 1000 is equal to:",
                    values=["20", "200", "0.20", "1000/20"],
                    answer="200",
                ),
                LessonStep(
                    step_type="manipulate",
                    title="Convert three ways",
                    content="Express 40% as a fraction, a decimal, and as 'parts out of 100'.",
                    template="40% = ___ / 100 = ___ (decimal) = ___ (simplified fraction)",
                    answer="40/100 = 0.40 = 2/5",
                    hint="Divide the percentage by 100 to get the decimal. Then simplify the fraction.",
                ),
                LessonStep(
                    step_type="predict",
                    title="What happens next?",
                    content="You see a number written as 0.15. What percentage is that?",
                    question="0.15 as a percentage is:",
                    options=[
                        {"id": "a", "text": "0.15%", "correct": False},
                        {"id": "b", "text": "1.5%", "correct": False},
                        {"id": "c", "text": "15%", "correct": True},
                        {"id": "d", "text": "150%", "correct": False},
                    ],
                    explanation="Multiply the decimal by 100 to convert to percentage: 0.15 × 100 = 15%.",
                ),
                LessonStep(
                    step_type="build",
                    title="Calculate the discount",
                    content="Write a function that returns x percent of n.",
                    function_name="percent_of",
                    signature="def percent_of(x: float, n: float) -> float:",
                    description="Return x% of n. Example: percent_of(20, 150) → 30.0",
                    test_cases=[
                        {"input": [20, 150], "expected": 30.0},
                        {"input": [25, 200], "expected": 50.0},
                        {"input": [12.5, 80], "expected": 10.0},
                    ],
                    hidden_tests=3,
                    repair_steps=[
                        {"trigger": "wrong_answer", "hint": "x% of n = (x / 100) * n. Do not forget the division by 100."}
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="break",
                    title="The classic trap",
                    content="A student calculates 25% of 80 as 25 × 80 = 2000.",
                    question="What did the student forget?",
                    options=[
                        {"id": "a", "text": "They forgot to divide by 100", "correct": True},
                        {"id": "b", "text": "They used the wrong number", "correct": False},
                        {"id": "c", "text": "Nothing, 2000 is correct", "correct": False},
                    ],
                    explanation="25% means 25/100. Forgetting the /100 turns a small percentage into a huge number.",
                ),
                LessonStep(
                    step_type="debug",
                    title="Fix the function",
                    content="This function is supposed to return x% of n but is broken.",
                    buggy_code="def percent_of(x, n):\n    return x * n   # wrong",
                    fix_steps=["Divide by 100: return (x * n) / 100 or return x / 100 * n"],
                    function_name="percent_of",
                    signature="def percent_of(x: float, n: float) -> float:",
                    description="Return x% of n correctly.",
                    test_cases=[{"input": [20, 150], "expected": 30.0}],
                    hidden_tests=2,
                    repair_steps=[],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="retrieve",
                    title="Recall without looking",
                    content="In one sentence: what does 15% mean?",
                    prompt="15% means...",
                    answer="15 parts out of every 100 parts (or 15/100 or 0.15)",
                ),
                LessonStep(
                    step_type="transfer",
                    title="New situation",
                    content="A battery shows 35% charge remaining. The full capacity is 4000 mAh. How much charge is left?",
                    function_name="remaining_charge",
                    signature="def remaining_charge(percent: float, capacity: float) -> float:",
                    description="Return the remaining mAh given percentage and full capacity.",
                    test_cases=[
                        {"input": [35, 4000], "expected": 1400.0},
                        {"input": [100, 4000], "expected": 4000.0},
                        {"input": [0, 4000], "expected": 0.0},
                    ],
                    hidden_tests=2,
                    repair_steps=[],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="mastery",
                    title="Prove it",
                    content="Mixed questions that require the core idea, not the same numbers.",
                    function_name="percent_mastery",
                    signature="def percent_of(x: float, n: float) -> float:",
                    description="Return x% of n. Must handle decimals and whole numbers.",
                    test_cases=[
                        {"input": [12.5, 64], "expected": 8.0},
                        {"input": [7.5, 200], "expected": 15.0},
                        {"input": [0, 500], "expected": 0.0},
                    ],
                    hidden_tests=4,
                    repair_steps=[],
                    passing_score=80,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=[
                "Convert between %, fraction and decimal",
                "Compute x% of any number",
                "Identify the 'forgot /100' mistake",
                "Apply the idea to a new context",
            ],
            unlocks="pct-2",
        ),

        # ─── Lesson 2: Percentage increase & decrease ───
        LessonDefinition(
            id="pct-2",
            title="Increase and Decrease",
            icon="2",
            order=2,
            concept="percentage_change",
            mental_model="The original value is the base. Increase multiplies by (1 + x/100). Decrease multiplies by (1 − x/100).",
            canonical_skill="aptitude.percentages",
            location="Market Square — Discount Counter",
            npc="Ravi the Shopkeeper",
            npc_line="Prices go up and down every week. Students keep using the new price as the base. That is the #1 error.",
            tutor_discover="When something increases or decreases by a percentage, the starting value is almost always the base.",
            why_this_matters="Salary hikes, price drops, population growth, mark-up and discount all use this exact idea. It appears in almost every company test.",
            engineering_context="In analytics we talk about week-over-week growth. In pricing engines we apply percentage mark-ups and discounts. The same formula powers both.",
            builds_toward="NQT Numerical + Profit & Loss",
            steps=[
                LessonStep(
                    step_type="discover",
                    title="Salary hike",
                    content="Salary is ₹50,000. It increases by 10%. What is the new salary?",
                    visual="50,000 × (1 + 10/100) = 50,000 × 1.10 = 55,000",
                    interaction="select-value",
                    prompt="The multiplier for a 10% increase is:",
                    values=["1.10", "0.10", "10", "1.01"],
                    answer="1.10",
                ),
                LessonStep(
                    step_type="predict",
                    title="Price drop",
                    content="A phone costs ₹20,000. It falls by 15%. New price?",
                    question="New price after 15% decrease:",
                    options=[
                        {"id": "a", "text": "₹17,000", "correct": True},
                        {"id": "b", "text": "₹18,000", "correct": False},
                        {"id": "c", "text": "₹15,000", "correct": False},
                        {"id": "d", "text": "₹23,000", "correct": False},
                    ],
                    explanation="20,000 × 0.85 = 17,000. Multiplier for 15% decrease is 1 − 0.15 = 0.85.",
                ),
                LessonStep(
                    step_type="build",
                    title="Apply the change",
                    function_name="apply_change",
                    signature="def apply_change(original: float, percent: float, increase: bool) -> float:",
                    description="If increase is True, raise original by percent%. Otherwise reduce it by percent%.",
                    test_cases=[
                        {"input": [100, 20, True], "expected": 120.0},
                        {"input": [200, 25, False], "expected": 150.0},
                        {"input": [50, 10, True], "expected": 55.0},
                    ],
                    hidden_tests=3,
                    repair_steps=[
                        {"trigger": "wrong_answer", "hint": "increase → original * (1 + percent/100); decrease → original * (1 - percent/100)"}
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="break",
                    title="Wrong base trap",
                    content="Price rises from 80 to 100. A student says 'increase = 20/100 = 20%'.",
                    question="Why is that wrong?",
                    options=[
                        {"id": "a", "text": "The base should be the original price 80, not 100", "correct": True},
                        {"id": "b", "text": "They should have used 100 as base", "correct": False},
                        {"id": "c", "text": "20% is actually correct", "correct": False},
                    ],
                    explanation="Percentage change is always measured against the original value: (100−80)/80 × 100 = 25%.",
                ),
                LessonStep(
                    step_type="retrieve",
                    title="Write the two multipliers",
                    content="Without looking, what is the multiplier for a 12% increase and for a 12% decrease?",
                    prompt="Increase multiplier: ___   Decrease multiplier: ___",
                    answer="1.12 and 0.88",
                ),
                LessonStep(
                    step_type="transfer",
                    title="Population growth",
                    content="A town has 12,000 people. Population grows 8% in one year. What is the new population?",
                    function_name="new_population",
                    signature="def new_population(current: float, growth_percent: float) -> float:",
                    description="Return population after the given percentage growth.",
                    test_cases=[
                        {"input": [12000, 8], "expected": 12960.0},
                        {"input": [5000, 10], "expected": 5500.0},
                    ],
                    hidden_tests=2,
                    repair_steps=[],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="mastery",
                    title="Mixed change",
                    content="Handle both directions correctly under one function.",
                    function_name="apply_change",
                    signature="def apply_change(original: float, percent: float, increase: bool) -> float:",
                    description="Correctly increase or decrease by the given percent.",
                    test_cases=[
                        {"input": [250, 20, True], "expected": 300.0},
                        {"input": [160, 25, False], "expected": 120.0},
                        {"input": [80, 12.5, True], "expected": 90.0},
                    ],
                    hidden_tests=4,
                    repair_steps=[],
                    passing_score=80,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=[
                "Apply percentage increase correctly",
                "Apply percentage decrease correctly",
                "Always use the original value as base",
                "Transfer the idea to a new domain",
            ],
            unlocks="pct-3",
        ),

        # ─── Lesson 3: Successive percentage change ───
        LessonDefinition(
            id="pct-3",
            title="Successive Changes",
            icon="3",
            order=3,
            concept="successive_percentage_change",
            mental_model="Apply each change to the current value, not the original. Percentages do not simply add or subtract.",
            canonical_skill="aptitude.percentages",
            location="Market Square — Double Discount Day",
            npc="Ravi the Shopkeeper",
            npc_line="Today we give 20% off then another 10% off. Students add 20+10=30 and get the wrong answer every time.",
            tutor_discover="Two successive percentage changes are multiplicative, never additive.",
            why_this_matters="This single idea appears in almost every higher-difficulty percentage question in TCS and Infosys papers.",
            engineering_context="Compound interest, successive discounts, multi-step growth rates — all use the same multiplicative model.",
            builds_toward="NQT medium/hard Numerical + Profit & Loss",
            steps=[
                LessonStep(
                    step_type="discover",
                    title="Double discount",
                    content="Price 100. First 20% off, then another 10% off. Final price?",
                    visual="100 × 0.80 = 80  →  80 × 0.90 = 72  (net 28% off, not 30%)",
                    interaction="select-value",
                    prompt="Net effect of +20% then −10% on 100 is:",
                    values=["+10%", "−8%", "−10%", "no change"],
                    answer="−8%",
                ),
                LessonStep(
                    step_type="predict",
                    title="Increase then decrease",
                    content="A number is first increased by 10% and then decreased by 10%. Net change?",
                    question="Net result:",
                    options=[
                        {"id": "a", "text": "No change", "correct": False},
                        {"id": "b", "text": "1% decrease", "correct": True},
                        {"id": "c", "text": "1% increase", "correct": False},
                        {"id": "d", "text": "10% decrease", "correct": False},
                    ],
                    explanation="100 × 1.10 × 0.90 = 99. Net = 1% decrease. The two 10%s do not cancel.",
                ),
                LessonStep(
                    step_type="build",
                    title="Successive multiplier",
                    function_name="successive",
                    signature="def successive(original: float, changes: list) -> float:",
                    description="changes is a list of signed percentages, e.g. [20, -10]. Apply them in order and return final value.",
                    test_cases=[
                        {"input": [100, [20, -10]], "expected": 108.0},
                        {"input": [200, [10, 10]], "expected": 242.0},
                        {"input": [100, [-20, -10]], "expected": 72.0},
                    ],
                    hidden_tests=3,
                    repair_steps=[
                        {"trigger": "wrong_answer", "hint": "For each change c: original = original * (1 + c/100). Do not add the percentages."}
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="break",
                    title="The additive trap",
                    content="Student says: 20% + 10% = 30% off, so 100 becomes 70.",
                    question="What is the correct final price?",
                    options=[
                        {"id": "a", "text": "70", "correct": False},
                        {"id": "b", "text": "72", "correct": True},
                        {"id": "c", "text": "80", "correct": False},
                    ],
                    explanation="100 × 0.8 × 0.9 = 72. Adding percentages ignores that the second discount acts on a smaller base.",
                ),
                LessonStep(
                    step_type="retrieve",
                    title="Net effect formula",
                    content="Two successive changes of a% and b%. What is the single equivalent percentage change?",
                    prompt="Equivalent % = ",
                    answer="a + b + (a*b)/100   (with signs)",
                ),
                LessonStep(
                    step_type="transfer",
                    title="Marked price story",
                    content="Cost price 100. Marked 50% above cost. Then two successive discounts of 10% and 10%. Final selling price and profit %?",
                    function_name="final_sp",
                    signature="def final_sp(cp: float, markup: float, d1: float, d2: float) -> float:",
                    description="Return the final selling price after markup and two discounts.",
                    test_cases=[
                        {"input": [100, 50, 10, 10], "expected": 121.5},
                    ],
                    hidden_tests=2,
                    repair_steps=[],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="mastery",
                    title="Prove successive mastery",
                    function_name="successive",
                    signature="def successive(original: float, changes: list) -> float:",
                    description="Apply any sequence of signed percentage changes correctly.",
                    test_cases=[
                        {"input": [100, [10, -10]], "expected": 99.0},
                        {"input": [500, [20, 10, -5]], "expected": 627.0},
                        {"input": [80, [-25, 20]], "expected": 72.0},
                    ],
                    hidden_tests=4,
                    repair_steps=[],
                    passing_score=80,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=[
                "Never add successive percentages",
                "Apply changes multiplicatively in order",
                "Compute net effect of two changes",
                "Solve real successive-discount problems",
            ],
            unlocks="pct-4",
        ),

        # ─── Lesson 4: Reverse percentage ───
        LessonDefinition(
            id="pct-4",
            title="Reverse Percentage",
            icon="4",
            order=4,
            concept="reverse_percentage",
            mental_model="When you are given the final value after a percentage change, divide by the multiplier to recover the original.",
            canonical_skill="aptitude.percentages",
            location="Market Square — After the Sale",
            npc="Ravi the Shopkeeper",
            npc_line="Customer says 'I paid 120 after 20% discount'. What was the original price? Most students subtract 20 instead of dividing.",
            tutor_discover="Going backwards from a percentage change means division, not subtraction.",
            why_this_matters="Many medium and hard NQT questions give the final figure and ask for the original. This is the exact skill required.",
            engineering_context="In analytics we often know the current metric and the growth rate and need the previous period value. Same reverse operation.",
            builds_toward="NQT medium/hard Numerical",
            steps=[
                LessonStep(
                    step_type="discover",
                    title="After the increase",
                    content="After a 20% increase the price is 120. What was the original?",
                    visual="Original × 1.20 = 120  →  Original = 120 / 1.20 = 100",
                    interaction="select-value",
                    prompt="Original price is:",
                    values=["100", "96", "140", "110"],
                    answer="100",
                ),
                LessonStep(
                    step_type="predict",
                    title="After the decrease",
                    content="After a 25% discount the price is 150. Original price?",
                    question="Original price:",
                    options=[
                        {"id": "a", "text": "200", "correct": True},
                        {"id": "b", "text": "187.5", "correct": False},
                        {"id": "c", "text": "175", "correct": False},
                        {"id": "d", "text": "125", "correct": False},
                    ],
                    explanation="150 is 75% of original. Original = 150 / 0.75 = 200.",
                ),
                LessonStep(
                    step_type="build",
                    title="Recover the original",
                    function_name="original_value",
                    signature="def original_value(final: float, percent: float, was_increase: bool) -> float:",
                    description="Given final value after a percentage change, return the original value.",
                    test_cases=[
                        {"input": [120, 20, True], "expected": 100.0},
                        {"input": [150, 25, False], "expected": 200.0},
                        {"input": [90, 10, False], "expected": 100.0},
                    ],
                    hidden_tests=3,
                    repair_steps=[
                        {"trigger": "wrong_answer", "hint": "If it was an increase: final / (1 + percent/100). If decrease: final / (1 - percent/100)."}
                    ],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="break",
                    title="Subtraction trap",
                    content="Student does 120 − 20 = 100 and gets lucky on one question, then fails the next.",
                    question="Why is subtracting the percentage dangerous?",
                    options=[
                        {"id": "a", "text": "It only works when the original is 100; otherwise it is wrong", "correct": True},
                        {"id": "b", "text": "It is always correct", "correct": False},
                        {"id": "c", "text": "It works for decreases only", "correct": False},
                    ],
                    explanation="Subtracting assumes the percentage is an absolute number. It coincides with the right answer only when the base happens to be 100.",
                ),
                LessonStep(
                    step_type="retrieve",
                    title="One-line rule",
                    content="How do you recover the original after a percentage change?",
                    prompt="Original = Final ÷ ...",
                    answer="the multiplier that was applied (1 ± percent/100)",
                ),
                LessonStep(
                    step_type="transfer",
                    title="Salary after hike",
                    content="After a 12% hike a salary became 56,000. What was the previous salary?",
                    function_name="previous_salary",
                    signature="def previous_salary(current: float, hike_percent: float) -> float:",
                    description="Return the salary before the given percentage hike.",
                    test_cases=[
                        {"input": [56000, 12], "expected": 50000.0},
                        {"input": [11000, 10], "expected": 10000.0},
                    ],
                    hidden_tests=2,
                    repair_steps=[],
                    passing_score=70,
                    max_attempts=3,
                ),
                LessonStep(
                    step_type="mastery",
                    title="Reverse mastery",
                    function_name="original_value",
                    signature="def original_value(final: float, percent: float, was_increase: bool) -> float:",
                    description="Recover original after either an increase or a decrease.",
                    test_cases=[
                        {"input": [121, 10, True], "expected": 110.0},
                        {"input": [85, 15, False], "expected": 100.0},
                        {"input": [240, 20, True], "expected": 200.0},
                    ],
                    hidden_tests=4,
                    repair_steps=[],
                    passing_score=80,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=[
                "Recover original after an increase",
                "Recover original after a decrease",
                "Never subtract the percentage number",
                "Solve real reverse-percentage word problems",
            ],
            unlocks="pct-boss",
        ),

        # ─── Boss: mixed percentages ───
        LessonDefinition(
            id="pct-boss",
            title="Percentages Boss",
            icon="B",
            kind="boss",
            order=5,
            concept="percentage_mastery",
            mental_model="Combine meaning, change, successive change and reverse in one problem.",
            canonical_skill="aptitude.percentages",
            diamonds=120,
            estimated_minutes=20,
            why_this_matters="Real NQT questions mix these ideas. The boss proves you can handle them together.",
            engineering_context="A pricing engine that applies mark-up then successive discounts and can reverse the calculation is exactly this skill set.",
            builds_toward="Full NQT Numerical readiness",
            steps=[
                LessonStep(
                    step_type="mastery",
                    title="Full percentage challenge",
                    function_name="solve_percentage",
                    signature="def solve_percentage(cp: float, markup: float, d1: float, d2: float) -> dict:",
                    description=(
                        "Cost price = cp. Marked up by markup%. Then successive discounts d1% and d2%. "
                        "Return dict with keys: marked_price, selling_price, profit_percent."
                    ),
                    test_cases=[
                        {
                            "input": [100, 50, 10, 10],
                            "expected": {"marked_price": 150.0, "selling_price": 121.5, "profit_percent": 21.5},
                        },
                    ],
                    hidden_tests=5,
                    repair_steps=[],
                    passing_score=80,
                    max_attempts=3,
                ),
            ],
            mastery_evidence=[
                "Compute marked price from cost and markup",
                "Apply successive discounts correctly",
                "Calculate true profit percentage",
                "Combine all percentage skills in one problem",
            ],
        ),
    ],
)


# ───────────────────────────────────────────────────────────────────
# WORLD DEFINITION
# ───────────────────────────────────────────────────────────────────

WORLD_APTITUDE_QUANT = WorldDefinition(
    id="aptitude_quant",
    name="Quantitative Aptitude",
    icon="%
",
    subtitle="Numerical Ability for service-company placements",
    description=(
        "Master the quantitative topics that appear in TCS NQT, Infosys, Wipro, "
        "Accenture and every major service-company test. Starts from absolute zero."
    ),
    order=20,  # can be reordered when integrated into the main journey
    theme="aptitude",
    towns=[PERCENTAGES_TOWN],
)
