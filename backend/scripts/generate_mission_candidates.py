"""Deterministic mission-candidate generator: successive percentage change.

Not an LLM author. Every answer is computed twice by independent methods
(sequential application vs fraction multiplication, exact Fraction
arithmetic) and the item is emitted only if both agree, distractors differ,
and intake_lint accepts the shape.

Output enters the ISOLATED UNVERIFIED pool only
(backend/app/data/mission_candidates_percentages.json, trust_status
"unverified", no companies claims). Promotion requires the trust pipeline
(automated execution evidence below -> human review -> tranche-approve).
Never served until then.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from typing import Any, Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.services.intake_lint import lint_question  # noqa: E402

OUT = os.path.join(
    os.path.dirname(__file__), "..", "app", "data",
    "mission_candidates_percentages.json",
)
GENERATOR = "deterministic_generator:percentage_change v1"


def apply_seq(base: Fraction, rise: int, fall: int) -> Fraction:
    return base * (100 + rise) / 100 * (100 - fall) / 100


def apply_frac(base: Fraction, rise: int, fall: int) -> Fraction:
    return base * Fraction(100 + rise, 100) * Fraction(100 - fall, 100)


def net_pct(rise: int, fall: int) -> Fraction:
    return Fraction((100 + rise) * (100 - fall) - 10000, 100)


def fmt_money(v: Fraction) -> str:
    return f"Rs. {float(v):.2f}".rstrip("0").rstrip(".")


def build_item(idx: int, base: int, rise: int, fall: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Return (candidate, evidence). Raises on any disagreement."""
    b, r, f = Fraction(base), rise, fall
    final_a = apply_seq(b, r, f)
    final_b = apply_frac(b, r, f)
    assert final_a == final_b, f"method disagreement {final_a} != {final_b}"
    net = net_pct(r, f)
    assert final_a == b + b * net / 100, "net-check disagreement"

    direction = "increase" if net > 0 else "decrease" if net < 0 else "no change"
    if net == 0:
        correct = "No net change"
    else:
        pct = abs(net)
        pct_s = str(pct) if pct.denominator == 1 else f"{float(pct):.2f}"
        correct = f"{pct_s}% {direction}"

    traps = [
        "No net change" if net != 0 else f"{abs(r - f)}% {'increase' if r > f else 'decrease'}",
        f"{abs(r - f)}% {'increase' if r >= f else 'decrease'}",
        f"{r + f}% increase",
        fmt_money(b),
    ]
    options: List[str] = []
    for t in [correct] + traps:
        if t not in options:
            options.append(t)
    assert len(options) >= 4, "not enough distinct options"
    options = options[:4]
    assert correct in options

    q = (
        f"A shopkeeper raises the price of an article (Rs. {base}) by {r}%, "
        f"then offers a {f}% discount on the raised price. "
        f"What is the net change?"
    )
    expl = (
        f"Method 1 (sequential): {base} x {100 + r}/100 = {fmt_money(b * (100 + r) / 100)}; "
        f"x {100 - f}/100 = {fmt_money(final_a)}. "
        f"Method 2 (fractions): {base} x {100 + r}/100 x {100 - f}/100 = {fmt_money(final_b)}. "
        f"Both agree: {correct}."
    )
    item = {
        "id": f"gen_pct_{idx:04d}",
        "type": "aptitude",
        "topic": "Quantitative Aptitude",
        "sub_topic": "Successive Percentage Change",
        "question": q,
        "options": options,
        "correct_answer": correct,
        "explanation": expl,
        "worked_solution": expl,
        "difficulty": "easy",
        "trust_status": "unverified",
        "provenance": GENERATOR,
        "companies": [],
        "source_bank": "mission_candidates",
        "verification": {
            "method_agreement": True,
            "exact_arithmetic": True,
            "distinct_options": True,
        },
    }
    lint = lint_question(item)
    item["lint_verdict"] = lint.get("verdict", lint.get("status", "unknown"))
    item["lint_flags"] = lint.get("flags", lint.get("reasons", []))
    return item, {"id": item["id"], "lint": item["lint_verdict"]}


def main() -> int:
    params = [
        (1000, 20, 10), (800, 25, 20), (1500, 10, 10), (2000, 30, 15),
        (500, 40, 25), (1200, 15, 5), (2500, 20, 20), (900, 50, 30),
        (1600, 12, 8), (700, 35, 10), (1100, 25, 25), (3000, 18, 12),
    ]
    items, evidence = [], []
    for i, (base, rise, fall) in enumerate(params):
        item, ev = build_item(i, base, rise, fall)
        if item["lint_verdict"] == "rejected":
            print(f"REJECTED by lint: {item['id']} {item['lint_flags']}")
            continue
        items.append(item)
        evidence.append(ev)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(items, fh, ensure_ascii=False, indent=1)
    print(f"wrote {len(items)} UNVERIFIED candidates -> {OUT}")
    print(f"lint verdicts: {sorted(e['lint'] for e in evidence)}")
    print("serving: none (unverified pool only; promotion needs human review)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
