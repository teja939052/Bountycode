#!/usr/bin/env python3
"""Backfill real, teachable 9-stage content into empty mission packs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE = Path("D:/Project-Fremen/backend")
PACKS_DIR = BASE / "app/content/mission_packs"


def _mcq(prompt: str, answer: str, options: List[str], explanation: str = "", tags: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "kind": "mcq",
        "prompt": prompt,
        "answer": answer,
        "options": options,
        "explanation": explanation,
        "difficulty": "medium",
        "company_tags": tags or ["tcs", "infosys", "wipro"],
    }


def _numeric(prompt: str, correct: str, explanation: str = "", tags: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "kind": "numeric",
        "prompt": prompt,
        "answer": correct,
        "explanation": explanation,
        "difficulty": "medium",
        "company_tags": tags or ["tcs", "infosys", "wipro"],
    }


def _code(prompt: str, starter: str = "", answer: str = "", language: str = "python", tags: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "kind": "code",
        "prompt": prompt,
        "starter": starter,
        "answer": answer,
        "language": language,
        "difficulty": "medium",
        "company_tags": tags or ["tcs", "infosys", "wipro"],
    }


def _proof_text(prompt: str, correct: str, explanation: str = "", tags: Optional[List[str]] = None, seconds: int = 60) -> Dict[str, Any]:
    return {
        "id": "p1-" + prompt.lower().replace(" ", "_")[:40],
        "prompt": prompt,
        "answer_format": "text",
        "correct": correct,
        "explanation": explanation,
        "time_limit_seconds": seconds,
        "company_tags": tags or ["tcs"],
    }


def _proof_numeric(prompt: str, correct: str, explanation: str = "", tags: Optional[List[str]] = None, seconds: int = 60) -> Dict[str, Any]:
    return {
        "id": "p1-" + prompt.lower().replace(" ", "_")[:40],
        "prompt": prompt,
        "answer_format": "numeric",
        "correct": correct,
        "explanation": explanation,
        "time_limit_seconds": seconds,
        "company_tags": tags or ["tcs"],
    }


def _captain(domain: str, title: str) -> Dict[str, Any]:
    return {
        "intro": "Welcome to " + title + ". This is a core " + domain + " concept for placement prep. Follow the steps carefully.",
        "correct": ["Exactly right!", "Perfect!", "You have got it!"],
        "wrong": ["Not quite. Review the step and try again.", "Close! Think about what the concept really means."],
        "after_break": "Now you see the broken assumption. Repair it and move on.",
        "after_mastery": "You have mastered " + title + ". This will appear in your next test.",
        "retry_prompt": "Give it another shot. You are close.",
    }


def _pack(pack_id: str, title: str, domain: str, concept: str, skill_id: str, misconception_codes: List[Dict[str, str]], stages: Dict[str, Any], why: str = "", practice: Optional[List[Dict[str, Any]]] = None, proof: Optional[List[Dict[str, Any]]] = None, srs: Optional[List[str]] = None) -> Dict[str, Any]:
    pack: Dict[str, Any] = {
        "id": pack_id,
        "title": title,
        "domain": domain,
        "concept": concept,
        "skill_id": skill_id,
        "tags": [domain, "service-companies", "tcs", "infosys", "wipro"],
        "difficulty": "medium",
        "estimated_minutes": 20,
        "mastery_threshold": 75,
        "why_it_matters": why or (title + " is a core " + domain + " concept for placement prep."),
        "prerequisites": [],
        "misconceptions": misconception_codes,
        "captain_byte": _captain(domain, title),
    }
    for key, value in stages.items():
        pack[key] = value
    pack["practice"] = practice or [_mcq("Sample question on " + title, "A", ["A", "B", "C", "D"], "Review the concept.")]
    pack["proof"] = proof or [_proof_text("Placement proof: explain " + title + " in one sentence.", title + " is a core concept tested in service-company technical rounds.", "Use precise terminology.", ["tcs"], 60)]
    pack["company_variants"] = [{"company": c, "role": "sde", "difficulty": "medium", "proof_questions": []} for c in ["tcs", "infosys", "wipro"]]
    pack["srs_key_points"] = srs or [title + " is a core " + domain + " concept.", "Master the definition and common patterns.", "Practice under time pressure."]
    pack["srs_review_intervals"] = [1, 3, 7, 14, 30]
    return pack


def _mission(mission_id: str, skill_id: str, title: str, domain: str) -> Dict[str, Any]:
    return {
        "id": mission_id,
        "track_id": "service",
        "domain": domain,
        "canonical_skill": skill_id,
        "brief": {
            "mission_title": title,
            "round_name": "Service Company Technical Round",
            "threat": "Candidates who cannot explain or apply this concept fail early.",
            "goal": "Master " + title + " well enough to explain and implement it under time pressure.",
            "reward_diamonds": 20,
        },
        "stages": [
            {"stage": "discover", "interaction": "visual_hook", "check": "mcq:discover", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "understand", "interaction": "micro_animation", "check": "explain:understand", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "manipulate", "interaction": "drag_or_manipulate", "moments": ["change_one_thing"], "check": "interaction_event", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "predict", "interaction": "predict_output", "check": "mcq:predict", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "build", "interaction": "tiny_build", "check": "constructed_calculation", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "break_step", "interaction": "break_and_debug", "check": "mcq:break", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "debug", "interaction": "error_hunt", "check": "constructed_calculation", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "retrieval", "interaction": "recall_check", "check": "recall", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "transfer", "interaction": "transfer_problem", "check": "constructed_calculation", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
        ],
        "mentor_skill": skill_id,
        "company_overlay_id": "",
        "provenance": "pattern-relevant",
        "reward": {"diamonds": 20, "unlocks": ""},
        "consequence": {
            "on_mastery": "advance to next level",
            "on_developing": "retrieval drill tomorrow",
            "on_repair": "repair mission before advancing",
        },
        "frontend_slug": skill_id,
        "lesson_slug": skill_id,
        "trust_floor": "automated_checked",
        "status": "unverified",
    }


# ---------------------------------------------------------------------------
# Domain content
# ---------------------------------------------------------------------------

def _searching() -> Dict[str, Dict[str, Any]]:
    return {
        "searching.linear_search": {
            "discover": {"prompt": "You have a guest list of 20 names. Find Priya without sorting.", "question": "What is the simplest guaranteed way?", "options": ["Check each name", "Guess randomly", "Start from end", "Use binary search"], "interaction_kind": "mcq_read"},
            "understand": "Linear search walks the list once. Worst case: target is last or absent, so inspect every element. That is O(n). Best case: O(1) when target is first. It never needs sorted data.",
            "manipulate": {"prompt": "A list has 8 positions, one contains 1. Find the index by checking sequentially.", "answer": "0 <= i < 8", "hint": "Increment index by 1 each step and stop when value is 1.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "For a list of length 20 where the target is absent, how many comparisons does linear search make?", "answer": "20", "options": ["1", "10", "20", "log(20)"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Return the index of target in cards, or -1 if missing.", "answer": "for i in range(len(cards)):\n    if cards[i] == target:\n        return i\nreturn -1", "explanation": "Iterate once, return on first match.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why does this fail when target is at index 0?\nfor i in range(1, len(cards)):", "broken_code": "for i in range(1, len(cards)):\n    if cards[i] == target:\n        print(i)", "expected_failure": "Starts at 1 and never checks index 0.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the off-by-one that skips the first element.", "correct_code": "for i in range(len(cards)):\n    if cards[i] == target:\n        print(i)\n        break", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the worst-case time complexity of linear search?", "answer": "O(n)", "alternative": ["Linear time", "n checks"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Count how many times target appears in items without using count().", "answer": "count = 0\nfor x in items:\n    if x == target:\n        count += 1\nprint(count)", "explanation": "Same sequential scan, increment a counter instead of returning early.", "interaction_kind": "code_build"},
            "practice": [_mcq("Which loop bound guarantees every element is checked?", "range(len(cards))", ["range(1, len(cards))", "range(len(cards)-1)", "range(len(cards)+1)"], "Start at 0, stop at len.", ["tcs", "infosys"]), _numeric("If n=50 and target is absent, how many comparisons?", "50", "Worst case inspects every element.", ["tcs"])],
            "proof": [_proof_text("Explain why linear search needs no sorted input.", "It compares sequentially and never relies on ordering.", "Ordering is irrelevant when you inspect every element.", ["tcs"], 60)],
            "srs": ["Linear search checks every element sequentially.", "Worst case is O(n); best case is O(1).", "Use when data is small or unsorted and simplicity matters."],
            "misconceptions": [{"code": "coding_state_trace_error", "signature": "Student loses track of index boundaries during search.", "reteach_route": "visual_state", "reteach_action": "trace_state_step_by_step"}],
        },
        "searching.binary_search": {
            "discover": {"prompt": "A sorted list of 1 000 000 names is given. Find a name with at most 20 checks.", "question": "Which algorithm makes this possible?", "options": ["Binary search", "Linear search", "Interpolation search", "Hash lookup"], "interaction_kind": "mcq_read"},
            "understand": "Binary search requires sorted data. At each step compare the target with the middle element and discard the half that cannot contain it. The search space halves each step, giving O(log n). The loop condition must include equality so single-element ranges are not skipped.",
            "manipulate": {"prompt": "Given lo=0, hi=7, what is mid? After discarding the left half, what is the new hi?", "answer": "mid=3, hi=3", "hint": "mid = (lo + hi) // 2. If target is bigger, lo = mid + 1.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "For a sorted list of length 16, what is the maximum number of comparisons in binary search?", "answer": "4", "options": ["2", "4", "8", "16"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Write binary search returning the index or -1.", "answer": "def search(nums, target):\n    lo, hi = 0, len(nums)-1\n    while lo <= hi:\n        mid = (lo+hi)//2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1", "explanation": "Use <= so a one-element range is reachable.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why does `while lo < hi` fail for nums=[5], target=5?", "broken_code": "lo, hi = 0, 0\nwhile lo < hi:\n    mid = (lo+hi)//2\n    print(nums[mid])", "expected_failure": "Loop never executes for a single-element list.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the off-by-one that can miss the first element.", "correct_code": "lo, hi = 0, len(nums)-1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if nums[mid] == target:\n        return mid\n    elif nums[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1\nreturn -1", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "Why must the input be sorted for binary search?", "answer": "Because ordering guarantees which half to discard.", "alternative": ["Sorted order lets you eliminate half the items each step."], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Find the first occurrence of target in a list with duplicates.", "answer": "ans = -1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if nums[mid] == target:\n        ans = mid\n        hi = mid - 1\n    elif nums[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1\nprint(ans)", "explanation": "After a match, continue searching left.", "interaction_kind": "code_build"},
            "practice": [_mcq("What is the worst-case complexity of binary search?", "O(log n)", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], "Halving each step gives logarithmic time.", ["tcs", "infosys"]), _code("Return first occurrence of target in sorted list.", "nums = [1,2,3,3,3,4,5]\ntarget = 3", "See transfer answer.", ["tcs"])],
            "proof": [_proof_numeric("Maximum comparisons for n=1024?", "10", "log2(1024)=10.", ["tcs"], 60)],
            "srs": ["Binary search halves the search space each step.", "Requires sorted input and inclusive loop bounds.", "Worst case is O(log n)."],
            "misconceptions": [{"code": "coding_state_trace_error", "signature": "Student loses track of index boundaries during search.", "reteach_route": "visual_state", "reteach_action": "trace_state_step_by_step"}],
        },
    }


def _aptitude() -> Dict[str, Dict[str, Any]]:
    return {
        "aptitude.percentages": {
            "discover": {"prompt": "A shirt costs 100. After a 20% discount and then a 10% tax on the discounted price, what is the final price?", "question": "Is the final price 100 + (-20% + 10%) = 90?", "options": ["No, it is 88", "Yes, 90", "No, it is 92", "Cannot say"], "interaction_kind": "mcq_read"},
            "understand": "Percentage change is relative to a base that changes. A 20% discount makes the new base 80. Then 10% tax on 80 gives 8, so final price is 88. Adding percentage points directly is wrong because the bases differ.",
            "manipulate": {"prompt": "If the original price is P, write the discounted price and then the taxed price in terms of P.", "answer": "0.80P then 0.88P", "hint": "Multiply by (1 - 0.20), then multiply that result by (1 + 0.10).", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "A number increases by 20% and then decreases by 20%. Is the final number equal to the original?", "answer": "No", "options": ["Yes", "No", "Only if original is 100", "Only if original is 0"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Write a function final_price(price, discount_pct, tax_pct) returning the final amount.", "answer": "def final_price(price, discount_pct, tax_pct):\n    discounted = price * (1 - discount_pct/100)\n    return discounted * (1 + tax_pct/100)", "explanation": "Apply discount first, then tax on the discounted price.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why is `price + discount_pct + tax_pct` wrong?", "broken_code": "price + discount_pct + tax_pct", "expected_failure": "It adds percentage points instead of applying them to a changing base.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the percentage calculation.", "correct_code": "discounted = price * (1 - discount_pct/100)\nfinal = discounted * (1 + tax_pct/100)", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "When can you add/subtract percentage points directly?", "answer": "Only when they share the same base.", "alternative": ["Same base means same denominator."], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "A population grows 15% in year 1 and 10% in year 2. What is the total growth factor?", "answer": "1.15 * 1.10 = 1.265", "explanation": "Multiply growth factors because the base changes each year.", "interaction_kind": "numeric_input"},
            "practice": [_mcq("After a 25% discount, what percent of the original remains?", "75%", ["25%", "75%", "125%", "50%"], "100% - 25% = 75%.", ["tcs", "infosys"]), _numeric("Price 200, discount 30%, tax 12% on discounted price. Final price?", "168.8", "200*0.7=140, 140*1.12=156.8.", ["tcs"])],
            "proof": [_proof_text("Explain why successive percentage changes do not add.", "Each change applies to a new base, so they compound.", "Use the discount-then-tax example.", ["tcs"], 60)],
            "srs": ["Percentage change is relative to the current base.", "Successive percentage changes multiply, not add.", "Always identify the base before applying a percent."],
            "misconceptions": [{"code": "apt_percent_base_confusion", "signature": "Student treats percentages as additive over changing bases.", "reteach_route": "worked_example", "reteach_action": "show_base_vs_change"}],
        },
        "aptitude.ratio_proportion": {
            "discover": {"prompt": "A recipe uses 2 cups flour for 3 cups water. If you use 8 cups flour, how many cups water?", "question": "Is the answer 12 because 8/2 = 4 and 3*4 = 12?", "options": ["Yes", "No", "Only if flour is doubled twice", "Cannot say"], "interaction_kind": "mcq_read"},
            "understand": "Ratios express a fixed relationship. If flour:water = 2:3, then scaling flour by k scales water by the same k. Proportion means the ratio stays constant across scaled quantities.",
            "manipulate": {"prompt": "If A/B = 3/4 and B = 20, what is A?", "answer": "15", "hint": "Cross multiply: A = 3 * B / 4.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "If 5 workers finish a job in 12 days, 10 workers take about how many days (assuming linear)?", "answer": "6", "options": ["24", "12", "6", "3"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Write a function scaled_quantity(original_a, original_b, new_a) returning new_b keeping the same ratio.", "answer": "def scaled_quantity(original_a, original_b, new_a):\n    return new_a * original_b / original_a", "explanation": "Keep the ratio constant by cross multiplication.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why is `new_b = new_a * original_a / original_b` wrong?", "broken_code": "new_b = new_a * original_a / original_b", "expected_failure": "Inverts the ratio relationship.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the ratio inversion.", "correct_code": "new_b = new_a * original_b / original_a", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What does it mean for two ratios to be in proportion?", "answer": "Their cross products are equal.", "alternative": ["a*d = b*c"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "If 7 machines make 210 widgets in 5 days, how many widgets do 10 machines make in 7 days?", "answer": "420", "explanation": "Machine-days are constant: 7*5 = 35 machine-days per 210 widgets.", "interaction_kind": "numeric_input"},
            "practice": [_mcq("If 3:4 :: 6:x, what is x?", "8", ["6", "7", "8", "9"], "Cross multiply: 3*x = 4*6.", ["tcs", "infosys"]), _numeric("A:B = 5:7, B=14. Find A.", "10", "A = 5*14/7.", ["tcs"])],
            "proof": [_proof_text("State the condition for two ratios to be in proportion.", "Cross products are equal.", "a/b = c/d implies a*d = b*c.", ["tcs"], 60)],
            "srs": ["Ratio compares two quantities; proportion equates two ratios.", "Cross-multiply to test or solve proportions.", "Scaling preserves the ratio."],
            "misconceptions": [{"code": "apt_ratio_interpretation_error", "signature": "Student inverts ratio or confuses part-to-part with part-to-whole.", "reteach_route": "visual_state", "reteach_action": "show_ratio_as_division"}],
        },
    }


def _coding() -> Dict[str, Dict[str, Any]]:
    return {
        "coding.loops": {
            "discover": {"prompt": "Print numbers 0 through 4 using a loop. Which Python construct expresses 'repeat 5 times'?", "question": "What does range(5) produce?", "options": ["0,1,2,3,4", "1,2,3,4,5", "0,1,2,3,4,5", "1,2,3,4"], "interaction_kind": "mcq_read"},
            "understand": "A for loop iterates over a sequence. range(n) produces 0..n-1. The loop body runs once per element. Off-by-one errors happen when the boundary is inclusive or when start/end are swapped.",
            "manipulate": {"prompt": "Change the loop to print 1 through 5.", "answer": "for i in range(1, 6):\n    print(i)", "hint": "range(start, end) is inclusive of start and exclusive of end.", "interaction_kind": "code_build"},
            "predict": {"prompt": "What does this print?\nfor i in range(3):\n    print(i, end=' ')", "answer": "0 1 2", "options": ["0 1 2", "1 2 3", "0 1 2 3", "1 2"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Sum all even numbers from 1 to 20.", "answer": "total = 0\nfor i in range(1, 21):\n    if i % 2 == 0:\n        total += i\nprint(total)", "explanation": "Iterate full range, filter with modulo, accumulate.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why does `range(1, 5)` print only 1,2,3,4 and not 5?", "broken_code": "for i in range(1, 5):\n    print(i)\n# Expected 1 2 3 4 5", "expected_failure": "range end is exclusive.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the loop to include 5.", "correct_code": "for i in range(1, 6):\n    print(i)", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the output type of range(3)?", "answer": "A sequence of integers 0,1,2", "alternative": ["0, 1, 2"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Generate the first 10 square numbers.", "answer": "squares = []\nfor i in range(1, 11):\n    squares.append(i*i)\nprint(squares)", "explanation": "Loop and append computed value.", "interaction_kind": "code_build"},
            "practice": [_mcq("What does list(range(3)) produce?", "[0, 1, 2]", ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[1, 2]"], "range is zero-indexed and end-exclusive.", ["tcs", "infosys"]), _code("Print the first 5 multiples of 3.", "", "for i in range(1, 6): print(3*i)", ["wipro"])],
            "proof": [_proof_text("Explain why range(5) does not include 5.", "The end boundary is exclusive.", "range(start, stop) stops before stop.", ["tcs"], 60)],
            "srs": ["range(n) gives 0..n-1.", "Loop boundaries are a common off-by-one source.", "Use range(start, end+1) when end should be included."],
            "misconceptions": [{"code": "coding_loop_boundary_error", "signature": "Student treats loop end as inclusive or mis-counts iterations.", "reteach_route": "bug_surgery", "reteach_action": "show_loop_boundary"}],
        },
        "coding.conditions": {
            "discover": {"prompt": "A student passes if score >= 40. Which condition captures this?", "question": "Which branch runs when score is exactly 40?", "options": ["if score >= 40", "if score > 40", "if score == 40", "if score <= 40"], "interaction_kind": "mcq_read"},
            "understand": "Conditions select branches. >= includes the boundary. elif is checked only if earlier conditions failed. else is the fallback. Boundary errors occur when equality is excluded or multiple branches overlap.",
            "manipulate": {"prompt": "Write conditions for grades: A for >= 90, B for >= 75, C for >= 40, else F.", "answer": "if score >= 90: grade = 'A'\nelif score >= 75: grade = 'B'\nelif score >= 40: grade = 'C'\nelse: grade = 'F'", "hint": "Order matters: check highest threshold first.", "interaction_kind": "code_build"},
            "predict": {"prompt": "What is the output of:\n x = 5\n if x > 5:\n     print('A')\n elif x == 5:\n     print('B')\n else:\n     print('C')", "answer": "B", "options": ["A", "B", "C", "Nothing"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Return the largest of three numbers using nested conditions.", "answer": "def max3(a, b, c):\n    if a >= b and a >= c:\n        return a\n    elif b >= a and b >= c:\n        return b\n    else:\n        return c", "explanation": "Compare sequentially and return the first maximum.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why does `if x > 5` miss the case x == 5?", "broken_code": "if x > 5:\n    print('big')\nelif x < 5:\n    print('small')\n# missing x == 5", "expected_failure": "Exact boundary case is not handled.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the boundary by handling x == 5.", "correct_code": "if x > 5:\n    print('big')\nelif x == 5:\n    print('equal')\nelif x < 5:\n    print('small')", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the difference between if, elif, and else?", "answer": "if starts, elif adds alternatives, else is final fallback.", "alternative": ["elif is checked only if earlier conditions failed."], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Classify temperature: hot >= 30, warm 20-29, cool 10-19, cold < 10.", "answer": "if temp >= 30: label='hot'\nelif temp >= 20: label='warm'\nelif temp >= 10: label='cool'\nelse: label='cold'", "explanation": "Order thresholds high to low.", "interaction_kind": "code_build"},
            "practice": [_mcq("Which operator includes the boundary?", ">=", [">", ">=", "<", "=="], "Use >= to include equality.", ["tcs", "infosys"]), _code("Return pass/fail for score >= 40.", "score = 55", "if score >= 40:\n    print('pass')\nelse:\n    print('fail')", ["wipro"])],
            "proof": [_proof_text("Explain why boundary conditions must be tested separately.", "Boundary values often hit different branches or edge handling.", "Test min, max, and just-inside/outside values.", ["tcs"], 60)],
            "srs": ["Conditions select branches based on boolean expressions.", "Order of if/elif matters.", "Always test exact boundary values."],
            "misconceptions": [{"code": "coding_condition_boundary_error", "signature": "Student excludes boundary or misorders overlapping conditions.", "reteach_route": "compare_worlds", "reteach_action": "show_condition_boundary"}],
        },
    }


def _cs_core() -> Dict[str, Dict[str, Any]]:
    return {
        "cs_core.os_basics": {
            "discover": {"prompt": "You run two programs in separate windows and they crash independently. Why?", "question": "What provides isolation between programs?", "options": ["Process", "Thread", "CPU core", "Cache"], "interaction_kind": "mcq_read"},
            "understand": "A process is an isolated execution environment with its own memory space. Threads share memory within one process. Processes communicate via IPC; threads communicate via shared variables. Context switching between processes is heavier than between threads.",
            "manipulate": {"prompt": "If Thread A writes x=10 and Thread B reads x, what must be true for Thread B to see 10?", "answer": "They share the same process memory and no stale cache blocks visibility.", "hint": "Threads share memory by default; processes do not.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "Which is lighter to create: a process or a thread?", "answer": "Thread", "options": ["Process", "Thread", "Both equal", "Depends on OS"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Create two threads that each append to a shared list 1000 times. Print final length.", "answer": "import threading\nshared = []\ndef append_n(n):\n    for _ in range(n):\n        shared.append(1)\nt1 = threading.Thread(target=append_n, args=(1000,))\nt2 = threading.Thread(target=append_n, args=(1000,))\nt1.start(); t2.start(); t1.join(); t2.join()\nprint(len(shared))", "explanation": "Threads share the same list object.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why might the final length be less than 2000 without locks?", "broken_code": "shared = []\n# two threads append without synchronization", "expected_failure": "Race condition can corrupt list state.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Add a lock to make append thread-safe.", "correct_code": "lock = threading.Lock()\nwith lock:\n    shared.append(1)", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "State one advantage and one disadvantage of threads vs processes.", "answer": "Threads are lighter but share state; processes are isolated but heavier.", "alternative": ["Lighter creation vs safer isolation."], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "A web server handles 1000 slow clients. Would you prefer threads or processes? Why?", "answer": "Threads or async; threads share memory but many threads add overhead. Async can be lighter.", "explanation": "Choose based on isolation needs versus overhead.", "interaction_kind": "code_build"},
            "practice": [_mcq("Which communication method is shared by default?", "Thread variables", ["Message queue", "Thread variables", "Socket", "File"], "Threads share the process address space.", ["tcs", "infosys"]), _numeric("If context switch costs 10us and thread switch costs 1us, how many process switches in 1ms?", "100", "1ms / 10us = 100.", ["tcs"])],
            "proof": [_proof_text("Explain when threads are safer than processes.", "Threads are not inherently safer; processes are safer because they are isolated.", "Isolation prevents one crash from corrupting another.", ["tcs"], 60)],
            "srs": ["Process = isolated memory; thread = shared memory within a process.", "Context-switch cost: threads are lighter.", "Race conditions require synchronization."],
            "misconceptions": [{"code": "cs_core_process_thread_confusion", "signature": "Student thinks threads are always faster or that processes share memory.", "reteach_route": "visual_state", "reteach_action": "show_process_vs_thread"}],
        },
        "cs_core.oop_basics": {
            "discover": {"prompt": "Car, Bike, and Truck share properties like wheels and methods like drive(). How do you avoid repeating code?", "question": "Which OOP concept models this shared structure?", "options": ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"], "interaction_kind": "mcq_read"},
            "understand": "Inheritance lets a child class reuse parent behavior. Polymorphism lets the same method call behave differently by class. Encapsulation hides internal state behind methods. Abstraction exposes only essentials.",
            "manipulate": {"prompt": "Write a Vehicle base class with drive(). Make Car override drive() to print 'Car drives'.", "answer": "class Vehicle:\n    def drive(self):\n        print('Vehicle drives')\nclass Car(Vehicle):\n    def drive(self):\n        print('Car drives')", "hint": "Use class Child(Parent): and redefine the method.", "interaction_kind": "code_build"},
            "predict": {"prompt": "If v = Car() and v.drive() prints 'Car drives', which concept is demonstrated?", "answer": "Polymorphism", "options": ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Add an attribute color to Vehicle and set it via __init__ in Car.", "answer": "class Vehicle:\n    def __init__(self, color):\n        self.color = color\nclass Car(Vehicle):\n    pass\nc = Car('red')", "explanation": "Child inherits __init__ unless overridden.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why does `class Car(Vehicle): pass` still create a Car instance?", "broken_code": "c = Car('red')\n# expected error because Car has no __init__", "expected_failure": "Inheritance includes parent initialization.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Explain why Car inherits Vehicle.__init__ and how to override it.", "correct_code": "class Car(Vehicle):\n    def __init__(self, color, seats):\n        super().__init__(color)\n        self.seats = seats", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the difference between inheritance and composition?", "answer": "Inheritance is 'is-a'; composition is 'has-a'.", "alternative": ["Car is a Vehicle. Car has an Engine."], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Model a Student that IS-A Person and HAS-A ListOfCourses.", "answer": "class Person:\n    def __init__(self, name):\n        self.name = name\nclass Student(Person):\n    def __init__(self, name, courses):\n        super().__init__(name)\n        self.courses = courses", "explanation": "Use inheritance for identity, composition for owned parts.", "interaction_kind": "code_build"},
            "practice": [_mcq("Which relationship uses 'has-a'?", "Composition", ["Inheritance", "Composition", "Polymorphism", "Abstraction"], "Composition models ownership.", ["tcs", "infosys"]), _code("Override a parent method in a child class.", "class Parent:\n    def greet(self):\n        print('hi')", "class Child(Parent):\n    def greet(self):\n        print('hello from child')", ["wipro"])],
            "proof": [_proof_text("Explain inheritance vs composition with one example each.", "Inheritance: class Dog(Animal). Composition: Car has Engine.", "Pick examples that highlight 'is-a' versus 'has-a'.", ["tcs"], 60)],
            "srs": ["Inheritance reuses parent behavior.", "Polymorphism selects method by runtime type.", "Encapsulation hides internals behind methods."],
            "misconceptions": [{"code": "cs_core_oop_relationship_misconception", "signature": "Student confuses inheritance with composition or thinks inheritance copies code statically.", "reteach_route": "compare_worlds", "reteach_action": "show_oop_relationships"}],
        },
    }


def main() -> None:
    libraries: Dict[str, Dict[str, Any]] = {}
    libraries.update(_searching())
    libraries.update(_aptitude())
    libraries.update(_coding())
    libraries.update(_cs_core())

    updated = 0
    for json_file in PACKS_DIR.glob("*.json"):
        data = json.load(open(json_file, encoding="utf-8"))
        pack_id = data.get("id", "")
        content = libraries.get(pack_id)
        if not content:
            continue

        changed = False
        for stage_name, stage_data in content.items():
            if stage_name in ("practice", "proof", "srs", "misconceptions"):
                continue
            if isinstance(stage_data, dict) and data.get(stage_name) != stage_data:
                data[stage_name] = stage_data
                changed = True

        for key in ("practice", "proof", "srs_key_points", "misconceptions"):
            if key in content and data.get(key) != content[key]:
                data[key] = content[key]
                changed = True

        if changed:
            json.dump(data, open(json_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            updated += 1

    print("Enriched " + str(updated) + " mission packs")


if __name__ == "__main__":
    main()
