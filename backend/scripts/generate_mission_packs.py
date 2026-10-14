"""Generate ALL mission pack JSON files for BountyCode's A-to-Z placement curriculum.

Run:
    python backend/scripts/generate_mission_packs.py

Outputs:
    backend/app/content/mission_packs/<pack_id>.json

Skips packs that already exist on disk.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = REPO_ROOT / "backend" / "app" / "content" / "mission_packs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DONE = {
    "aptitude.percentages",
    "aptitude.averages",
    "aptitude.time_work",
    "aptitude.blood_relations",
    "coding.variables",
    "coding.conditions",
    "cs_core.sql_joins",
    "company.tcs",
    "company.infosys",
    "company.wipro",
    "company.amazon",
    "company.google",
    "company.microsoft",
}


def _pack(path: str, data: Dict[str, Any]) -> None:
    target = OUT_DIR / f"{path}.json"
    if target.exists() or path in DONE:
        print(f"  SKIP  {path}")
        return
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  CREATE {path}")


def _srs() -> List[int]:
    return [1, 3, 7, 14, 30]


def _captain(intro, correct, wrong, after_break, after_mastery, retry):
    return {
        "intro": intro,
        "correct": correct,
        "wrong": wrong,
        "after_break": after_break,
        "after_mastery": after_mastery,
        "retry_prompt": retry,
    }


def _miscon(code, sig, route, action):
    return {"code": code, "signature": sig, "reteach_route": route, "reteach_action": action}


def _practice(*items):
    return list(items)


def _proof(*items):
    return list(items)


def _cv(company, role="sde", difficulty="medium", extra=None, proof_questions=None):
    return {
        "company": company,
        "role": role,
        "difficulty": difficulty,
        "extra_practice": extra or [],
        "proof_questions": proof_questions or [],
    }


def base(pid, title, domain, concept, skill_id, tags, difficulty, minutes, threshold, why, prereqs=None, miscon=None, captain=None, discover=None, understand=None, manipulate=None, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, practice=None, proof=None, company_variants=None, srs=None):
    return {
        "id": pid,
        "title": title,
        "domain": domain,
        "concept": concept,
        "skill_id": skill_id,
        "tags": tags,
        "difficulty": difficulty,
        "estimated_minutes": minutes,
        "mastery_threshold": threshold,
        "why_it_matters": why,
        "prerequisites": prereqs or [],
        "misconceptions": miscon or [],
        "captain_byte": captain or _captain("", [], [], "", "", ""),
        "discover": discover or {},
        "understand": understand or {},
        "manipulate": manipulate or {},
        "predict": predict or {},
        "build": build or {},
        "break_step": break_step or {},
        "debug": debug or {},
        "retrieval": retrieval or {},
        "transfer": transfer or {},
        "practice": practice or [],
        "proof": proof or [],
        "company_variants": company_variants or [],
        "srs_key_points": srs or [],
        "srs_review_intervals": _srs(),
    }


# ═══════════════════════════════════════════════════════════════
# APTITUDE
# ═══════════════════════════════════════════════════════════════

def gen_time_speed_distance():
    pid = "aptitude.time_speed_distance"
    return base(
        pid, "Time Speed Distance", "aptitude", "Time Speed Distance", pid,
        ["aptitude", "quant", "tcs", "infosys", "wipro"],
        "medium", 25, 75,
        "TSD is a staple in TCS NQT, Infosys InfyTQ, and Wipro.",
        ["aptitude.percentages"],
        [_miscon("speed_additive", "Adds speeds instead of using relative speed.", "worked_example", "show_relative_speed")],
        _captain("D = S × T. Relative speed = sum for opposite, difference for same direction.", ["Relative speed locked!"], ["Remember: relative speed depends on direction."], "Now you see the trap.", "TSD mastered.", "Try again with D = S × T."),
        {"prompt": "A train 200m passes a pole in 10s. Speed in km/h?", "question": "A train 200m passes a pole in 10s. Speed in km/h?", "options": ["72", "36", "18", "54"], "interaction_kind": "mcq_read"},
        {"prompt": "Speed = Distance/Time. Convert m/s to km/h: ×18/5.", "explanation": "200/10 = 20 m/s = 72 km/h.", "interaction_kind": "read_explanation"},
        {"prompt": "Car at 60 km/h for 2.5h. Distance?", "answer": "150", "hint": "D = S × T", "interaction_kind": "numeric_input"},
        {"prompt": "Two trains 200m, 300m at 40, 50 km/h opposite. Time to cross?", "answer": "18.18", "options": ["12", "18.18", "20", "24"], "interaction_kind": "numeric_input"},
        {"prompt": "Person walks at 5 km/h, misses bus by 2 min. At 6 km/h, reaches 3 min early. Distance?", "answer": "1.5", "explanation": "d/5 - d/6 = 5 min = 1/12 hr → d = 1.5 km.", "interaction_kind": "word_problem"},
        {"prompt": "Student adds speeds of opposite trains without units. Wrong?", "common_mistake": "Adding speeds without converting units.", "correct_reasoning": "Relative speed = S1+S2. Convert to m/s first.", "interaction_kind": "mcq_diagnose"},
        {"prompt": "Fix: time = (L1+L2)/(S1-S2) for opposite directions.", "correct_formula": "time = (L1+L2)/(S1+S2) for opposite directions", "interaction_kind": "formula_fix"},
        {"prompt": "State the three TSD formulas.", "answer": "Speed = Distance/Time; Distance = Speed×Time; Time = Distance/Speed", "alternative": ["S=D/T", "D=S×T", "T=D/S"], "interaction_kind": "recall_formula"},
        {"prompt": "Boat goes 30km upstream and back in 5h. Stream = 5 km/h. Find still-water speed.", "answer": "13", "explanation": "30/(x-5) + 30/(x+5) = 5 → x≈13.", "interaction_kind": "word_problem"},
        _practice(
            {"kind": "mcq", "prompt": "Man walks 4 km/h covers distance in 2h45m. Running at 16 km/h, time?", "answer": "20.625", "options": ["20.625", "25", "30", "15"], "explanation": "D = 4×2.75 = 11 km. t = 11/16 hr.", "difficulty": "medium", "company_tags": ["tcs", "infosys"]},
            {"kind": "mcq", "prompt": "Two trains 120m each at 30, 20 km/h opposite. Time to cross?", "answer": "17.28", "options": ["10.28", "12.48", "17.28", "8.64"], "explanation": "Relative = 50 km/h = 125/9 m/s. t = 240/(125/9) = 17.28s.", "difficulty": "medium", "company_tags": ["tcs", "wipro"]},
        ),
        _proof(
            {"id": "p1", "prompt": "Train 150m passes man running 6 km/h in 9s. Train speed?", "answer_format": "numeric", "correct": "66", "explanation": "Relative = 150/9 m/s = 60 km/h. Train = 60+6 = 66.", "time_limit_seconds": 60, "company_tags": ["tcs"]},
            {"id": "p2", "prompt": "Two cyclists from A,B towards each other at 15, 12 km/h. Distance = 54 km. Meet after?", "answer_format": "numeric", "correct": "2", "explanation": "Relative = 27 km/h. t = 54/27 = 2h.", "time_limit_seconds": 60, "company_tags": ["infosys", "wipro"]},
        ),
        [_cv("tcs", proof_questions=[{"id": "tcs-p1", "prompt": "TCS: Train crosses 240m platform in 30s. Length 160m. Speed?", "answer_format": "numeric", "correct": "48", "explanation": "D=400m. v=400/30 m/s = 48 km/h.", "time_limit_seconds": 60, "company_tags": ["tcs"]}])],
        ["D = S × T", "Relative speed = S1±S2", "Meeting time = total distance / relative speed", "Stream: upstream = x-s, downstream = x+s", "Convert m/s ↔ km/h: ×18/5 or ×5/18"],
    )


def gen_profit_loss():
    pid = "aptitude.profit_loss"
    return base(
        pid, "Profit and Loss", "aptitude", "Profit Loss", pid,
        ["aptitude", "quant", "tcs", "infosys", "wipro"],
        "easy", 20, 75,
        "Profit/Loss is high-frequency in TCS NQT and Infosys.",
        ["aptitude.percentages"],
        [_miscon("cp_sp_confusion", "Confuses CP and SP.", "worked_example", "label_cp_sp"), _miscon("discount_on_sp", "Calculates discount on SP instead of MP.", "compare_worlds", "highlight_mp_vs_sp")],
        _captain("Profit% = (SP-CP)/CP×100. Discount always on MP.", ["Profit locked!"], ["Remember: profit% on CP, not SP.", "Discount on MP, not SP."], "Now you see the trap.", "P/L mastered.", "Write the formulas."),
        {"prompt": "Bought for 100, sold for 120. Profit %?", "question": "Bought for Rs. 100, sold for Rs. 120. Profit %?", "options": ["20%", "25%", "16.67%", "15%"], "interaction_kind": "mcq_read"},
        {"prompt": "Profit% = (SP-CP)/CP×100. Loss% = (CP-SP)/CP×100. Discount% = (MP-SP)/MP×100.", "explanation": "Profit = 20. Profit% = 20/100×100 = 20%.", "interaction_kind": "read_explanation"},
        {"prompt": "CP = 200, want 25% profit. SP?", "answer": "250", "hint": "SP = CP × (1 + profit%/100)", "interaction_kind": "numeric_input"},
        {"prompt": "Sold at 10% loss, SP = 270. CP?", "answer": "300", "options": ["250", "270", "300", "330"], "interaction_kind": "numeric_input"},
        {"prompt": "Marked 40% above CP, 20% discount. Profit %?", "answer": "12", "explanation": "MP=140, SP=112, Profit%=12%.", "interaction_kind": "word_problem"},
        {"prompt": "Student uses (SP-CP)/SP×100 for profit%. Wrong?", "common_mistake": "Using SP as base instead of CP.", "correct_reasoning": "Profit% is always on CP.", "interaction_kind": "mcq_diagnose"},
        {"prompt": "Fix: discount = (SP-MP)/SP×100.", "correct_formula": "discount = (MP-SP)/MP×100", "interaction_kind": "formula_fix"},
        {"prompt": "Formula for profit percent.", "answer": "(SP-CP)/CP×100", "alternative": ["Profit divided by CP times 100"], "interaction_kind": "recall_formula"},
        {"prompt": "Sell 45 articles for 1200 at 20% loss. How many for 1200 at 20% gain?", "answer": "27", "explanation": "CP of 45 = 1500. SP for 20% gain = 1800. Articles = 1800/(1500/45) = 27.", "interaction_kind": "word_problem"},
        _practice(
            {"kind": "mcq", "prompt": "Cycle bought for 1400, sold at 15% loss. SP?", "answer": "1190", "options": ["1190", "1300", "1100", "1250"], "explanation": "Loss = 210. SP = 1190.", "difficulty": "easy", "company_tags": ["tcs", "infosys"]},
            {"kind": "mcq", "prompt": "10% discount on MP, still 8% profit. MP above CP?", "answer": "20", "options": ["10", "15", "20", "25"], "explanation": "MP=120, CP=100. Mark-up = 20%.", "difficulty": "medium", "company_tags": ["wipro", "tcs"]},
        ),
        _proof(
            {"id": "p1", "prompt": "Dishonest shopkeeper uses 900g for 1kg. Profit %?", "answer_format": "numeric", "correct": "11.11", "explanation": "Sells 900g at CP of 1kg. Profit% = 100/900×100 = 11.11%.", "time_limit_seconds": 60, "company_tags": ["tcs", "infosys"]},
            {"id": "p2", "prompt": "CP of 10 = SP of 8. Profit %?", "answer_format": "numeric", "correct": "25", "explanation": "Profit per 10 = 2. Profit% = 2/8×100 = 25%.", "time_limit_seconds": 60, "company_tags": ["wipro"]},
        ),
        [_cv("tcs", proof_questions=[{"id": "tcs-p1", "prompt": "TCS: Buys 6 for 5, sells 5 for 6. Profit %?", "answer_format": "numeric", "correct": "44.44", "explanation": "CP of 30 = 25, SP of 30 = 36. Profit% = 44.44%.", "time_limit_seconds": 60, "company_tags": ["tcs"]}])],
        ["Profit% = (SP-CP)/CP×100", "Loss% = (CP-SP)/CP×100", "Discount always on MP", "Successive profits: P1+P2+P1P2/100", "CP of x = SP of y → ratio method"],
    )


def gen_ratio_proportion():
    pid = "aptitude.ratio_proportion"
    return base(
        pid, "Ratio and Proportion", "aptitude", "Ratio Proportion", pid,
        ["aptitude", "quant", "tcs", "infosys", "wipro"],
        "easy", 20, 75,
        "Ratio & Proportion is the backbone of mixture and partnership problems.",
        ["aptitude.percentages"],
        [_miscon("ratio_add", "Adds ratios directly.", "worked_example", "show_ratio_as_fraction"), _miscon("proportion_mix", "Confuses direct and inverse.", "compare_worlds", "highlight_direct_vs_inverse")],
        _captain("Ratio compares quantities. a:b = c:d means ad=bc. Invert and multiply.", ["Ratio locked!"], ["Remember: a:b=c:d means ad=bc.", "Inverse: more workers → less time."], "Now you see why adding ratios fails.", "Ratio mastered.", "Retry with a:b=c:d."),
        {"prompt": "A:B=2:3, B:C=4:5. A:C?", "question": "If A:B=2:3 and B:C=4:5, what is A:C?", "options": ["8:15", "2:5", "4:5", "8:12"], "interaction_kind": "mcq_read"},
        {"prompt": "To combine ratios, make common term equal using LCM.", "explanation": "LCM(3,4)=12. A:B=8:12, B:C=12:15 → A:C=8:15.", "interaction_kind": "read_explanation"},
        {"prompt": "a:b=3:4, b:c=6:7. Find a:b:c.", "answer": "9:12:14", "hint": "Make b=LCM(4,6)=12.", "interaction_kind": "numeric_input"},
        {"prompt": "4 men in 10 days. 8 men?", "answer": "5", "options": ["5", "20", "8", "10"], "interaction_kind": "numeric_input"},
        {"prompt": "A,B invest 5000,7000 for 6,8 months. Profit ratio?", "answer": "15:28", "explanation": "5000×6 : 7000×8 = 15:28.", "interaction_kind": "word_problem"},
        {"prompt": "Student adds 2:3 and 4:5 to get 6:8. Wrong?", "common_mistake": "Adding corresponding terms without scaling.", "correct_reasoning": "Scale to common term first.", "interaction_kind": "mcq_diagnose"},
        {"prompt": "Fix: A:C = 6:8 from 2:3 and 4:5.", "correct_formula": "A:C = (2×4):(3×5) = 8:15 after scaling.", "interaction_kind": "formula_fix"},
        {"prompt": "Condition for four quantities in proportion?", "answer": "a:b = c:d implies ad = bc", "alternative": ["Product of means = extremes"], "interaction_kind": "recall_formula"},
        {"prompt": "A in 20 days, B in 30. Together. A leaves after 5 days. B finishes in?", "answer": "20", "explanation": "Together rate = 1/12. Work in 5 days = 5/12. Remaining = 7/12. B takes 17.5 days.", "interaction_kind": "word_problem"},
        _practice(
            {"kind": "mcq", "prompt": "a:b=3:5, b:c=4:7. a:c?", "answer": "12:35", "options": ["3:7", "12:35", "7:12", "3:5"], "explanation": "Scale b to 20: a:b=12:20, b:c=20:35.", "difficulty": "easy", "company_tags": ["tcs", "infosys"]},
            {"kind": "mcq", "prompt": "Mixture 5:3. Replace 10L with water → 5:4. Initial quantity?", "answer": "40", "options": ["30", "40", "50", "60"], "explanation": "Let total=x. 5x/8 - 2.5 = 5x/9 → x=40.", "difficulty": "medium", "company_tags": ["wipro", "tcs"]},
        ),
        _proof(
            {"id": "p1", "prompt": "Three numbers 2:3:5, sum=150. Largest?", "answer_format": "numeric", "correct": "75", "explanation": "5/10 × 150 = 75.", "time_limit_seconds": 60, "company_tags": ["tcs", "infosys"]},
            {"id": "p2", "prompt": "A:B=2:3, B:C=4:5. Find (A+B):(B+C).", "answer_format": "text", "correct": "20:27", "explanation": "A=8k, B=12k, C=15k. (A+B):(B+C) = 20:27.", "time_limit_seconds": 60, "company_tags": ["wipro"]},
        ),
        [_cv("tcs", proof_questions=[{"id": "tcs-p1", "prompt": "TCS: Salaries 2:3:5. Increments 15%,10%,20%. New ratio?", "answer_format": "text", "correct": "23:33:60", "explanation": "New = 2.3:3.3:6 → 23:33:60.", "time_limit_seconds": 90, "company_tags": ["tcs"]}])],
        ["Combine ratios using LCM", "Direct: a/b = c/d", "Inverse: a×b = c×d", "Partnership: investment × time", "Mixture: allegation for two mixtures"],
    )


def gen_simple_interest():
    pid = "aptitude.simple_interest"
    return base(
        pid, "Simple Interest", "aptitude", "Simple Interest", pid,
        ["aptitude", "quant", "tcs", "infosys", "wipro"],
        "easy", 20, 75,
        "SI is the foundation for CI and is heavily tested in TCS NQT.",
        ["aptitude.percentages"],
        [_miscon("si_on_amount", "Calculates SI on Amount instead of Principal.", "worked_example", "highlight_principal"), _miscon("rate_percent", "Forgets to divide rate by 100.", "compare_worlds", "show_rate_as_decimal")],
        _captain("SI = P×R×T/100. Always on Principal.", ["SI locked!"], ["Remember: rate R/100.", "SI only on original principal."], "Now you see the trap.", "SI mastered. CI builds on this.", "Write SI=PRT/100."),
        {"prompt": "SI on 1000 at 5% for 2 years?", "question": "SI on Rs. 1000 at 5% per annum for 2 years?", "options": ["50", "100", "150", "200"], "interaction_kind": "mcq_read"},
        {"prompt": "SI = (P×R×T)/100. Amount = P+SI.", "explanation": "SI = 1000×5×2/100 = 100. Amount = 1100.", "interaction_kind": "read_explanation"},
        {"prompt": "SI=180, R=6%, T=3. Find P.", "answer": "1000", "hint": "P = SI×100/(R×T)", "interaction_kind": "numeric_input"},
        {"prompt": "Sum doubles in 8 years at SI. Rate?", "answer": "12.5", "options": ["10", "12.5", "15", "8"], "interaction_kind": "numeric_input"},
        {"prompt": "Sum trebles in 10 years. When 5 times?", "answer": "20", "explanation": "To treble: interest=2P in 10yr → P in 5yr. To 5x: need 4P → 20yr.", "interaction_kind": "word_problem"},
        {"prompt": "Student uses Amount as principal. Wrong?", "common_mistake": "SI is only on original principal.", "correct_reasoning": "SI = P×R×T/100, not Amount.", "interaction_kind": "mcq_diagnose"},
        {"prompt": "Fix: SI = (P+R)×T/100.", "correct_formula": "SI = P×R×T/100", "interaction_kind": "formula_fix"},
        {"prompt": "SI and Amount formulas?", "answer": "SI=P×R×T/100; Amount=P+SI", "alternative": ["PRT/100"], "interaction_kind": "recall_formula"},
        {"prompt": "SI for 6 years is 30% of P. Find rate.", "answer": "5", "explanation": "0.30P = P×R×6/100 → R=5%.", "interaction_kind": "word_problem"},
        _practice(
            {"kind": "mcq", "prompt": "At what rate will 2000 amount to 2600 in 5 years?", "answer": "6", "options": ["4", "5", "6", "7"], "explanation": "SI=600. R=600×100/(2000×5)=6%.", "difficulty": "easy", "company_tags": ["tcs", "infosys"]},
            {"kind": "mcq", "prompt": "Amounts to 11200 in 2yr, 11800 in 3yr. P and R?", "answer": "10000, 6", "options": ["10000,6", "10000,5", "11000,6", "12000,5"], "explanation": "1yr SI=600. R=600×100/(10000×1)=6%.", "difficulty": "medium", "company_tags": ["wipro", "tcs"]},
        ),
        _proof(
            {"id": "p1", "prompt": "Sum becomes 4x in 15 years at SI. When 5x?", "answer_format": "numeric", "correct": "20", "explanation": "Interest=3P in 15yr → P in 5yr. To 5x: need 4P → 20yr.", "time_limit_seconds": 60, "company_tags": ["tcs", "infosys"]},
            {"id": "p2", "prompt": "Difference SI and CI on 10000 for 2 years at 5%?", "answer_format": "numeric", "correct": "25", "explanation": "Diff = P(R/100)² = 10000×0.01 = 25.", "time_limit_seconds": 90, "company_tags": ["wipro"]},
        ),
        [_cv("tcs", proof_questions=[{"id": "tcs-p1", "prompt": "TCS: Sum triples in 8 years. When 9x?", "answer_format": "numeric", "correct": "32", "explanation": "2P in 8yr → P in 4yr. To 9x: need 8P → 32yr.", "time_limit_seconds": 60, "company_tags": ["tcs"]}])],
        ["SI = P×R×T/100", "Amount = P+SI", "If sum doubles in n years, rate = 100/n %", "Diff CI-SI for 2yr = P(R/100)²", "For fractional years: days/365 or 360"],
    )


def gen_hcf_lcm():
    pid = "aptitude.hcf_lcm"
    return base(
        pid, "HCF and LCM", "aptitude", "HCF LCM", pid,
        ["aptitude", "quant", "tcs", "infosys", "wipro"],
        "easy", 20, 75,
        "HCF/LCM is foundational for number theory problems.",
        ["aptitude.number_system"],
        [_miscon("hcf_lcm_formula", "Confuses product formula.", "worked_example", "show_product_formula"), _miscon("hcf_of_primes", "Thinks HCF of primes is 0.", "compare_worlds", "show_hcf_of_primes")],
        _captain("HCF divides all. LCM divisible by all. HCF×LCM = a×b for two numbers.", ["HCF/LCM locked!"], ["Remember: HCF×LCM = a×b.", "HCF of primes = 1."], "Now you see why HCF of primes is 1.", "HCF/LCM mastered.", "Write product formula."),
        {"prompt": "HCF of 12 and 18?", "question": "Find HCF of 12 and 18.", "options": ["2", "3", "6", "9"], "interaction_kind": "mcq_read"},
        {"prompt": "HCF = highest common factor. LCM = lowest common multiple. HCF×LCM = a×b.", "explanation": "Factors of 12: 1,2,3,4,6,12. Factors of 18: 1,2,3,6,9,18. HCF=6.", "interaction_kind": "read_explanation"},
        {"prompt": "LCM of 12 and 18 using prime factors?", "answer": "36", "hint": "2² × 3² = 36.", "interaction_kind": "numeric_input"},
        {"prompt": "HCF of two co-prime numbers?", "answer": "1", "options": ["0", "1", "2", "product"], "interaction_kind": "mcq_read"},
        {"prompt": "Greatest number dividing 1305,4665,6905 leaving same remainder?", "answer": "480", "explanation": "HCF(3360,2240,5600) = 480.", "interaction_kind": "word_problem"},
        {"prompt": "Student says HCF(7,11)=0. Wrong?", "common_mistake": "Confusing no common factors with HCF=0.", "correct_reasoning": "Every pair has HCF ≥ 1. HCF(7,11)=1.", "interaction_kind": "mcq_diagnose"},
        {"prompt": "Fix: HCF×LCM = a+b.", "correct_formula": "HCF×LCM = a×b for two numbers", "interaction_kind": "formula_fix"},
        {"prompt": "Relationship between HCF and LCM?", "answer": "HCF×LCM = product of two numbers", "alternative": ["a×b = HCF×LCM"], "interaction_kind": "recall_formula"},
        {"prompt": "HCF=12, LCM=240, one=60. Other?", "answer": "48", "explanation": "12×240 = 60×x → x=48.", "interaction_kind": "word_problem"},
        _practice(
            {"kind": "mcq", "prompt": "LCM of 15,20,30?", "answer": "60", "options": ["30", "60", "120", "300"], "explanation": "2²×3×5 = 60.", "difficulty": "easy", "company_tags": ["tcs", "infosys"]},
            {"kind": "mcq", "prompt": "Greatest number dividing 135,225,315 leaving same remainder?", "answer": "90", "options": ["45", "60", "90", "135"], "explanation": "HCF(90,90,180) = 90.", "difficulty": "medium", "company_tags": ["wipro", "tcs"]},
        ),
        _proof(
            {"id": "p1", "prompt": "Least number divisible by 12,15,20,27?", "answer_format": "numeric", "correct": "540", "explanation": "LCM = 2²×3³×5 = 540.", "time_limit_seconds": 60, "company_tags": ["tcs", "infosys"]},
            {"id": "p2", "prompt": "HCF=23, other LCM factors 13,14. Largest number?", "answer_format": "numeric", "correct": "322", "explanation": "Numbers = 23×13, 23×14. Largest = 322.", "time_limit_seconds": 60, "company_tags": ["wipro"]},
        ),
        [_cv("tcs", proof_questions=[{"id": "tcs-p1", "prompt": "TCS: HCF of fractions 2/3,4/6,5/9?", "answer_format": "text", "correct": "1/9", "explanation": "HCF(num)/LCM(den) = 1/9.", "time_limit_seconds": 60, "company_tags": ["tcs"]}])],
        ["HCF×LCM = a×b (two numbers)", "HCF of fractions = HCF(num)/LCM(den)", "LCM of fractions = LCM(num)/HCF(den)", "Prime factorization is most reliable", "For >2 numbers: HCF = HCF(HCF(a,b),c)"],
    )


def gen_permutations_combinations():
    pid = "aptitude.permutations_combinations"
    return base(
        pid, "Permutations and Combinations", "aptitude", "P&C", pid,
        ["aptitude", "quant", "tcs", "infosys", "wipro"],
        "medium", 30, 70,
        "P&C is high-difficulty, high-weightage in TCS NQT and Infosys.",
        ["aptitude.number_system"],
        [_miscon("perm_comb_confusion", "Cannot decide if order matters.", "worked_example", "show_order_matters"), _miscon("repetition_ignored", "Ignores repetition constraints.", "compare_worlds", "highlight_repetition")],
        _captain("P = order matters. C = order doesn't. nPr=n!/(n-r)!. nCr=n!/(r!(n-r)!).", ["P&C locked!"], ["P=arrangement, C=selection.", "Use n!/(n-r)! for P."], "Now you see order determines P vs C.", "P&C mastered.", "Write both formulas."),
        {"prompt": "Arrange 'CAT'. How many ways?", "question": "How many ways can you arrange the letters of 'CAT'?", "options": ["3", "6", "9", "12"], "interaction_kind": "mcq_read"},
        {"prompt": "Permutation = order matters. 3P3 = 3! = 6.", "explanation": "CAT, CTA, ACT, ATC, TCA, TAC = 6.", "interaction_kind": "read_explanation"},
        {"prompt": "Choose 2 from 4 fruits?", "answer": "6", "hint": "4C2 = 4!/(2!×2!) = 6", "interaction_kind": "numeric_input"},
        {"prompt": "3-digit numbers from 1,2,3,4 without repetition?", "answer": "24", "options": ["12", "24", "64", "4"], "interaction_kind": "numeric_input"},
        {"prompt": "Committee of 3 from 5 men, 4 women with ≥1 woman?", "answer": "74", "explanation": "Total 9C3=84. All men=5C3=10. 84-10=74.", "interaction_kind": "word_problem"},
        {"prompt": "Uses 5C3=10 for seating 3 from 5. Wrong?", "common_mistake": "Using C for arrangement where order matters.", "correct_reasoning": "Seating is permutation: 5P3 = 60.", "interaction_kind": "mcq_diagnose"},
        {"prompt": "Fix: 3-letter words from 5 letters = 5C3.", "correct_formula": "5P3 = 5!/(5-3)! = 60", "interaction_kind": "formula_fix"},
        {"prompt": "When permutation vs combination?", "answer": "Permutation when order matters; combination when order doesn't", "alternative": ["P=arrangement, C=selection"], "interaction_kind": "recall_formula"},
        {"prompt": "Diagonals in a hexagon?", "answer": "9", "explanation": "6C2 total lines - 6 sides = 15-6 = 9.", "interaction_kind": "word_problem"},
        _practice(
            {"kind": "mcq", "prompt": "4 men, 3 women in row, women in even places?", "answer": "144", "options": ["120", "144", "720", "36"], "explanation": "Men: 4! = 24. Women: 3! = 6. Total = 144.", "difficulty": "medium", "company_tags": ["tcs", "infosys"]},
            {"kind": "mcq", "prompt": "5 red, 4 blue, 3 green. Choose 2 same color?", "answer": "19", "options": ["12", "19", "22", "31"], "explanation": "5C2 + 4C2 + 3C2 = 10+6+3 = 19.", "difficulty": "medium", "company_tags": ["wipro", "tcs"]},
        ),
        _proof(
            {"id": "p1", "prompt": "4-letter words from 'EXAM' without repetition?", "answer_format": "numeric", "correct": "24", "explanation": "4P4 = 4! = 24.", "time_limit_seconds": 60, "company_tags": ["tcs", "infosys"]},
            {"id": "p2", "prompt": "8 persons at round table?", "answer_format": "numeric", "correct": "5040", "explanation": "(8-1)! = 7! = 5040.", "time_limit_seconds": 60, "company_tags": ["wipro"]},
        ),
        [_cv("tcs", proof_questions=[{"id": "tcs-p1", "prompt": "TCS: 10 people meet. Handshakes?", "answer_format": "numeric", "correct": "45", "explanation": "10C2 = 45.", "time_limit_seconds": 60, "company_tags": ["tcs"]}])],
        ["P = order matters: nPr = n!/(n-r)!", "C = order doesn't: nCr = n!/(r!(n-r)!)", "Circular: (n-1)!", "Check repetition constraints", "nCr = nC(n-r)"],
    )


def gen_probability():
    pid = "aptitude.probability"
    return base(
        pid, "Probability", "aptitude", "Probability", pid,
        ["aptitude", "quant", "tcs", "infosys", "wipro"],
        "medium", 25, 70,
        "Probability is tested in TCS NQT and Infosys, often mixed with P&C.",
        ["aptitude.permutations_combinations"],
        [_miscon("probability_gt_one", "Thinks probability can exceed 1.", "worked_example", "show_range_0_to_1"), _miscon("mutually_exclusive", "Forgets mutual exclusivity.", "compare_worlds", "highlight_addition_rule")],
        _captain("P = favorable/total, 0≤P≤1. P(A∪B)=P(A)+P(B)-P(A∩B).", ["Probability locked!"], ["Remember: 0 to 1 always.", "Mutually exclusive: add."], "Now you see P>1 is impossible.", "Probability mastered.", "Write P=favorable/total."),
        {"prompt": "Fair die rolled. P(6)?", "question": "A fair die is rolled. P(getting a 6)?", "options": ["1/2", "1/3", "1/6", "1/4"], "interaction_kind": "mcq_read"},
        {"prompt": "P = favorable/total. For die: 1/6.", "explanation": "Total=6, favorable=1. P=1/6.", "interaction_kind": "read_explanation"},
        {"prompt": "Card from 52. P(ace or king)?", "answer": "2/13", "hint": "4 aces + 4 kings = 8. 8/52 = 2/13.", "interaction_kind": "numeric_input"},
        {"prompt": "Two coins tossed. P(at least one head)?", "answer": "3/4", "options": ["1/2", "1/4", "3/4", "1"], "interaction_kind": "numeric_input"},
        {"prompt": "Bag: 5 red, 3 blue. Two drawn without replacement. P(both red)?", "answer": "5/14", "explanation": "5/8 × 4/7 = 20/56 = 5/14.", "interaction_kind": "word_problem"},
        {"prompt": "Student adds P(H)+P(T)=2. Wrong?", "common_mistake": "Confusing addition rule with total probability.", "correct_reasoning": "P(H or T) = 1/2+1/2 = 1.", "interaction_kind": "mcq_diagnose"},
        {"prompt": "Fix: P(A and B) = P(A)+P(B) for independent.", "correct_formula": "P(A and B) = P(A)×P(B) for independent", "interaction_kind": "formula_fix"},
        {"prompt": "P(A or B) when mutually exclusive?", "answer": "P(A or B) = P(A) + P(B)", "alternative": ["Addition rule"], "interaction_kind": "recall_formula"},
        {"prompt": "A truth 70%, B 80%. Both agree. P both truth?", "answer": "56", "explanation": "0.7×0.8 = 0.56 = 56%.", "interaction_kind": "word_problem"},
        _practice(
            {"kind": "mcq", "prompt": "Die rolled. P(even)?", "answer": "1/2", "options": ["1/2", "1/3", "1/6", "2/3"], "explanation": "Favorable=3 (2,4,6). P=3/6=1/2.", "difficulty": "easy", "company_tags": ["tcs", "infosys"]},
            {"kind": "mcq", "prompt": "Two dice. P(sum=7)?", "answer": "1/6", "options": ["1/6", "1/12", "1/4", "5/36"], "explanation": "Favorable=6. Total=36. P=6/36=1/6.", "difficulty": "medium", "company_tags": ["wipro", "tcs"]},
        ),
        _proof(
            {"id": "p1", "prompt": "Box: 3 red, 2 blue, 4 green. P(red or blue)?", "answer_format": "text", "correct": "5/9", "explanation": "Favorable=5, total=9. P=5/9.", "time_limit_seconds": 60, "company_tags": ["tcs", "infosys"]},
            {"id": "p2", "prompt": "Coin tossed 3 times. P(exactly 2 heads)?", "answer_format": "text", "correct": "3/8", "explanation": "Favorable=3 (HTT, THT, TTH). Total=8.", "time_limit_seconds": 60, "company_tags": ["wipro"]},
        ),
        [_cv("tcs", proof_questions=[{"id": "tcs-p1", "prompt": "TCS: Two cards from 52. P(both aces)?", "answer_format": "text", "correct": "1/221", "explanation": "4C2/52C2 = 6/1326 = 1/221.", "time_limit_seconds": 60, "company_tags": ["tcs"]}])],
        ["P = favorable/total (0≤P≤1)", "Mutually exclusive: P(A∪B)=P(A)+P(B)", "Independent: P(A∩B)=P(A)×P(B)", "Without replacement: adjust total", "Complement: P(not A)=1-P(A)"],
    )


# ═══════════════════════════════════════════════════════════════
# Generate all packs
# ═══════════════════════════════════════════════════════════════

ALL = [
    ("aptitude.time_speed_distance", gen_time_speed_distance),
    ("aptitude.profit_loss", gen_profit_loss),
    ("aptitude.ratio_proportion", gen_ratio_proportion),
    ("aptitude.simple_interest", gen_simple_interest),
    ("aptitude.hcf_lcm", gen_hcf_lcm),
    ("aptitude.permutations_combinations", gen_permutations_combinations),
    ("aptitude.probability", gen_probability),
]


def main() -> int:
    created = 0
    for pid, fn in ALL:
        try:
            pack = fn()
            _pack(pid, pack)
            if not (OUT_DIR / f"{pid}.json").exists():
                created += 1
        except Exception as exc:
            print(f"  FAIL  {pid}: {exc}")
    print(f"\nDone. Created {created} new packs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
