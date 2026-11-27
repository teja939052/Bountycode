"""Deterministic MCQ oracle — no LLM, no network, no human judgement.

The canonical gate (`auto_promote.gate_oracle`) verifies coding items by
execution and parametric items via `verify_parametric_bank.recompute`. It has
no path for an MCQ: with no `testcases` it returns `no_testcases`, so an
aptitude/logical item can never be verified and never becomes servable.

This module fills that gap. It recomputes the answer from the numbers and
relations stated in the question text, then requires that exactly one option
matches the recomputed value.

Contract
--------
    solve(item) -> OracleResult

`OracleResult.answer` is the option text the oracle derived, or None when the
item is outside the oracle's competence. None is NOT a failure of the item; it
means "this oracle cannot judge it". Callers must never treat None as a pass.

Evidence rules
--------------
* The oracle never reads `explanation` or `correct_answer` to decide. Both are
  generator output. Reading either would make the check circular.
* Agreement proves the key matches independent arithmetic. It does NOT prove
  pedagogical quality, originality, or that a human reviewed the item. Passing
  items stay `automated_checked`; promotion to `reviewed`/`trusted` is human.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Callable, Optional

# --------------------------------------------------------------------------
# option parsing
# --------------------------------------------------------------------------

_UNIT = re.compile(
    r"(rs\.?|₹|inr|km/h|km/hr|km|m/s|m|cm|sq cm|cubic cm|litres?|liters?|"
    r"hours?|hrs?|days?|seconds?|sec|years?|yrs?|%|degrees?|kg|g\b)",
    re.I,
)


def _opt_value(text: str) -> Optional[float]:
    """Numeric value of an option string, or None if it is not numeric.

    Handles 'Rs. 1,200', '12%', '4.8 hours', '6 2/3 days', '5/14', '1:3'.
    """
    s = str(text).strip()
    if not s:
        return None
    s = _UNIT.sub(" ", s).replace(",", "").strip()

    # mixed number: "6 2/3"
    m = re.fullmatch(r"(-?\d+)\s+(\d+)\s*/\s*(\d+)", s)
    if m:
        whole, num, den = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if den == 0:
            return None
        return whole + num / den

    # ratio "1:3" -> value is not a scalar; caller handles ratios separately
    if re.fullmatch(r"-?\d+(?:\.\d+)?\s*:\s*-?\d+(?:\.\d+)?", s):
        return None

    # plain fraction "5/14"
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*/\s*(-?\d+(?:\.\d+)?)", s)
    if m:
        den = float(m.group(2))
        if den == 0:
            return None
        return float(m.group(1)) / den

    m = re.fullmatch(r"-?\d+(?:\.\d+)?", s)
    if m:
        return float(s)
    return None


def _pick(options, value, tol=5e-3) -> Optional[str]:
    """Return the single option whose numeric value equals `value`."""
    if value is None:
        return None
    hits = []
    for opt in options:
        v = _opt_value(opt)
        if v is None:
            continue
        if abs(v - value) <= max(tol, abs(value) * 1e-6):
            hits.append(str(opt))
    return hits[0] if len(hits) == 1 else None


def _pick_text(options, value: str) -> Optional[str]:
    """Return the option matching a textual answer (case/space insensitive)."""
    if not value:
        return None
    target = _norm(value)
    hits = [str(o) for o in options if _norm(o) == target]
    return hits[0] if len(hits) == 1 else None


def _norm(s) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()


def _nums(text: str) -> list[float]:
    """All numbers in order, including decimals and commas."""
    out = []
    for m in re.finditer(r"-?\d+(?:,\d{3})*(?:\.\d+)?", str(text)):
        out.append(float(m.group(0).replace(",", "")))
    return out


def _ints(text: str) -> list[int]:
    return [int(v) for v in _nums(text) if float(v).is_integer()]


# --------------------------------------------------------------------------
# result type
# --------------------------------------------------------------------------


@dataclass
class OracleResult:
    answer: Optional[str]
    family: str
    detail: str = ""

    @property
    def resolved(self) -> bool:
        return self.answer is not None


def _unresolved(family: str, detail: str = "") -> OracleResult:
    return OracleResult(None, family, detail)


def _resolved(answer: str, family: str, detail: str = "") -> OracleResult:
    return OracleResult(answer, family, detail)


# --------------------------------------------------------------------------
# quantitative solvers
# --------------------------------------------------------------------------


def _profit_sell_price(q, opts):
    """buys for Rs. X ... sells it at Y% profit -> selling price"""
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("profit_sell_price", "needs price+percent")
    cost, pct = n[0], n[1]
    return _resolved_or_none(_pick(opts, cost * (1 + pct / 100)), "profit_sell_price")


def _resolved_or_none(opt, family, detail=""):
    return _resolved(opt, family, detail) if opt else _unresolved(family, "no unique option")


def _successive_pct(q, opts):
    """increased by a% then decreased by b% -> net change"""
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("successive_pct")
    a, b = n[0], -abs(n[1])
    net = a + b + a * b / 100
    word = "increase" if net > 0 else "decrease"
    target = f"{abs(net):g}% {word}"
    hit = _pick_text(opts, target)
    if hit:
        return _resolved(hit, "successive_pct", target)
    return _resolved_or_none(_pick(opts, abs(net)), "successive_pct", target)


def _population_pct(q, opts):
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("population_pct")
    up, down, pop = n[0], n[1], n[2]
    val = pop * (1 + up / 100) * (1 - down / 100)
    return _resolved_or_none(_pick(opts, round(val, 2)), "population_pct")


def _reverse_discount(q, opts):
    """After a d% discount the price is Rs. p. Original?"""
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("reverse_discount")
    d, final = n[0], n[1]
    return _resolved_or_none(_pick(opts, final * 100 / (100 - d)), "reverse_discount")


def _mixture_water(q, opts):
    """In V litres, w% is water. How much water to make it 50%?"""
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("mixture_water")
    total, pct = n[0], n[1]
    water = total * pct / 100
    milk = total - water
    # target: water == milk  ->  add (milk - water)
    return _resolved_or_none(_pick(opts, milk - water), "mixture_water")


def _election_margin(q, opts):
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("election_margin")
    pct, margin = n[0], n[1]
    # winner pct, loser 100-pct, margin = (2p-100)% of total
    total = margin * 100 / (2 * pct - 100)
    return _resolved_or_none(_pick(opts, total), "election_margin")


def _profit_after_increment(q, opts):
    """20% profit; both CP and SP up by Rs. X -> profit becomes 10%."""
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("profit_after_increment")
    p1, add, p2 = n[0], n[1], n[2]
    # (CP*(1+p1/100)+add) / (CP+add) - 1 = p2/100
    num = add * (1 + p2 / 100) - add
    den = (1 + p1 / 100) - (1 + p2 / 100)
    if den == 0:
        return _unresolved("profit_after_increment", "degenerate")
    return _resolved_or_none(_pick(opts, num / den), "profit_after_increment")


def _markup_discount(q, opts):
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("markup_discount")
    up, disc = n[0], n[1]
    pct = (1 + up / 100) * (1 - disc / 100) * 100 - 100
    return _resolved_or_none(_pick(opts, pct), "markup_discount")


def _cp_eq_sp(q, opts):
    """CP of n articles = SP of m articles -> profit%"""
    n = _ints(q)
    if len(n) < 2:
        return _unresolved("cp_eq_sp")
    a, b = n[0], n[1]
    if b == 0:
        return _unresolved("cp_eq_sp")
    return _resolved_or_none(_pick(opts, (a - b) * 100 / b, tol=0.02), "cp_eq_sp")


def _false_weight(q, opts):
    """uses an Xg weight instead of Ykg -> profit%"""
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("false_weight")
    used, claimed = n[0], n[1] * 1000
    if used == 0:
        return _unresolved("false_weight")
    return _resolved_or_none(_pick(opts, (claimed - used) * 100 / used, tol=0.02),
                             "false_weight")


def _two_articles(q, opts):
    """two articles at Rs. X each, gain a% / lose a% -> overall %"""
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("two_articles")
    pct = n[1]
    loss = pct * pct / 100
    target = f"{loss:g}% loss"
    hit = _pick_text(opts, target)
    if hit:
        return _resolved(hit, "two_articles", target)
    return _resolved_or_none(_pick(opts, loss), "two_articles", target)


def _alligation(q, opts):
    """mix tea at Rs. a/kg with Rs. b/kg to get Rs. c/kg -> ratio"""
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("alligation")
    a, b, c = n[0], n[1], n[2]
    # (b-c) : (c-a)
    x, y = b - c, c - a
    g = math.gcd(int(round(x)), int(round(y))) or 1
    target = f"{int(round(x))/g:.0f}:{int(round(y))/g:.0f}"
    hit = _pick_text(opts, target)
    return _resolved(hit, "alligation", target) if hit else _unresolved("alligation", target)


def _income_ratio(q, opts):
    """incomes ratio a:b, expenditures c:d, savings s1,s2 -> B's income"""
    n = _nums(q)
    if len(n) < 6:
        return _unresolved("income_ratio")
    a, b, c, d, s1, s2 = n[:6]
    # a*k - c*m = s1 ; b*k - d*m = s2
    det = a * (-d) - b * (-c)
    if det == 0:
        return _unresolved("income_ratio", "degenerate")
    k = (s1 * (-d) - s2 * (-c)) / det
    return _resolved_or_none(_pick(opts, b * k), "income_ratio")


def _age_ratio(q, opts):
    n = _nums(q)
    if len(n) < 5:
        return _unresolved("age_ratio")
    a, b, yrs, c, d = n[:5]
    # (a*k+y)/(b*k+y) = c/d
    k = yrs * (c - d) / (a * d - b * c) if (a * d - b * c) else None
    if k is None:
        return _unresolved("age_ratio", "degenerate")
    return _resolved_or_none(_pick(opts, a * k), "age_ratio")


def _work_together(q, opts):
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("work_together")
    a, b = n[0], n[1]
    return _resolved_or_none(_pick(opts, a * b / (a + b), tol=0.02), "work_together")


def _efficiency(q, opts):
    """A is k times as efficient as B; together d days -> A alone"""
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("efficiency")
    k, together = n[0], n[1]
    rate = 1 / together
    a_rate = rate * k / (k + 1)
    return _resolved_or_none(_pick(opts, 1 / a_rate, tol=0.02), "efficiency")


def _pipes(q, opts):
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("pipes")
    a, b, c = n[0], n[1], n[2]
    rate = 1 / a + 1 / b - 1 / c
    if rate <= 0:
        return _unresolved("pipes", "never fills")
    return _resolved_or_none(_pick(opts, 1 / rate, tol=0.02), "pipes")


def _average_speed(q, opts):
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("average_speed")
    a, b = n[0], n[1]
    return _resolved_or_none(_pick(opts, 2 * a * b / (a + b)), "average_speed")


def _train_platform(q, opts):
    """train L m long crosses platform in t s at v km/h -> platform length"""
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("train_platform")
    length, secs, kmh = n[0], n[1], n[2]
    dist = kmh * 5 / 18 * secs
    return _resolved_or_none(_pick(opts, dist - length), "train_platform")


def _two_trains(q, opts):
    n = _nums(q)
    if len(n) < 4:
        return _unresolved("two_trains")
    l1, l2, v1, v2 = n[:4]
    rel = (v1 + v2) * 5 / 18
    return _resolved_or_none(_pick(opts, (l1 + l2) / rel, tol=0.02), "two_trains")


def _dice_sum(q, opts):
    n = _nums(q)
    target = n[-1] if n else 7
    count = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == target)
    return _resolved_or_none(_pick(opts, count / 36, tol=1e-4), "dice_sum")


def _card_prob(q, opts):
    """red king or black queen"""
    if "red king" in q.lower() and "black queen" in q.lower():
        return _resolved_or_none(_pick(opts, 4 / 52, tol=1e-4), "card_prob")
    return _unresolved("card_prob")


def _largest_divisible(q, opts):
    """largest 4-digit number divisible by a, b, c"""
    n = _ints(q)
    if len(n) < 3:
        return _unresolved("largest_divisible")
    lcm = 1
    for v in n[:3]:
        lcm = lcm * v // math.gcd(lcm, v)
    largest = (9999 // lcm) * lcm
    return _resolved_or_none(_pick(opts, largest), "largest_divisible")


def _unit_digit(q, opts):
    m = re.search(r"(\d+)\s*\^\s*(\d+)", q)
    if not m:
        return _unresolved("unit_digit")
    base, exp = int(m.group(1)), int(m.group(2))
    return _resolved_or_none(_pick(opts, pow(base, exp, 10)), "unit_digit")


def _lcm_hcf(q, opts):
    n = _ints(q)
    if len(n) < 3:
        return _unresolved("lcm_hcf")
    lcm, hcf, one = n[0], n[1], n[2]
    other = lcm * hcf / one
    return _resolved_or_none(_pick(opts, other), "lcm_hcf")


def _pie_chart(q, opts):
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("pie_chart")
    deg, total = n[0], n[1]
    return _resolved_or_none(_pick(opts, total * deg / 360), "pie_chart")


def _average_sales(q, opts):
    m = re.search(r"([A-E]\s*=\s*\d+(?:\s*,\s*[A-E]\s*=\s*\d+)+)", q)
    if not m:
        return _unresolved("average_sales")
    vals = [float(x) for x in re.findall(r"=\s*(\d+)", m.group(1))]
    if not vals:
        return _unresolved("average_sales")
    return _resolved_or_none(_pick(opts, sum(vals) / len(vals)), "average_sales")


def _arrangements(q, opts):
    n = _ints(q)
    if not n:
        return _unresolved("arrangements")
    if "arranged in a row" in q.lower():
        return _resolved_or_none(_pick(opts, math.factorial(n[0])), "arrangements")
    if "selected from" in q.lower() and len(n) >= 2:
        k, total = n[0], n[1]
        return _resolved_or_none(_pick(opts, math.comb(total, k)), "arrangements")
    return _unresolved("arrangements")


def _milk_replacement(q, opts):
    """V litres milk, r removed & replaced, n times -> milk left"""
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("milk_replacement")
    total, removed, times = n[0], n[1], n[2]
    left = total * ((total - removed) / total) ** times
    return _resolved_or_none(_pick(opts, round(left, 2), tol=0.02), "milk_replacement")


def _average_replaced(q, opts):
    n = _nums(q)
    if len(n) < 4:
        return _unresolved("average_replaced")
    count, old_avg, new_val, new_avg = n[:4]
    replaced = old_avg * count - (new_avg * count - new_val)
    return _resolved_or_none(_pick(opts, replaced), "average_replaced")


def _weighted_average(q, opts):
    n = _nums(q)
    if len(n) < 4:
        return _unresolved("weighted_average")
    c1, a1, c2, a2 = n[:4]
    return _resolved_or_none(_pick(opts, (c1 * a1 + c2 * a2) / (c1 + c2), tol=0.02),
                             "weighted_average")


def _simple_interest(q, opts):
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("simple_interest")
    p, r, t = n[:3]
    return _resolved_or_none(_pick(opts, p * r * t / 100), "simple_interest")


def _rate_from_si(q, opts):
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("rate_from_si")
    p, si, t = n[:3]
    return _resolved_or_none(_pick(opts, si * 100 / (p * t)), "rate_from_si")


def _compound_interest(q, opts):
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("compound_interest")
    p, r, t = n[:3]
    return _resolved_or_none(_pick(opts, p * (1 + r / 100) ** t - p, tol=0.02),
                             "compound_interest")


def _boat_stream(q, opts):
    n = _nums(q)
    if len(n) < 4:
        return _unresolved("boat_stream")
    up_d, up_t, down_d, down_t = n[:4]
    return _resolved_or_none(
        _pick(opts, (down_d / down_t - up_d / up_t) / 2, tol=0.02), "boat_stream")


def _consumption(q, opts):
    """price rises a->b, expenditure up e% -> consumption reduction %"""
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("consumption")
    p1, p2, e = n[0], n[1], n[2]
    ratio = (p2 * 100) / (p1 * (100 + e))
    return _resolved_or_none(_pick(opts, (1 - ratio) * 100, tol=0.05), "consumption")


def _circle_area_circumference(q, opts):
    n = _nums(q)
    if not n:
        return _unresolved("circle")
    area = n[0]
    pi = 22 / 7
    r = math.sqrt(area / pi)
    return _resolved_or_none(_pick(opts, 2 * pi * r, tol=0.05), "circle")


def _cube_surface(q, opts):
    n = _nums(q)
    if not n:
        return _unresolved("cube")
    vol = n[0]
    side = round(vol ** (1 / 3))
    return _resolved_or_none(_pick(opts, 6 * side * side), "cube")


def _profit_share(q, opts):
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("profit_share")
    a, b, total = n[0], n[1], n[2]
    return _resolved_or_none(_pick(opts, total * a / (a + b)), "profit_share")


def _balls_both_red(q, opts):
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("balls_both_red")
    red, blue = n[0], n[1]
    total = red + blue
    return _resolved_or_none(_pick(opts, (red / total) * ((red - 1) / (total - 1)), tol=1e-4),
                             "balls_both_red")


def _work_fraction_left(q, opts):
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("work_fraction_left")
    a, b, d = n[:3]
    done = d * (1 / a + 1 / b)
    return _resolved_or_none(_pick(opts, 1 - done, tol=0.02), "work_fraction_left")


def _percent_of_number(q, opts):
    """If p% of a number is x, what is q% of it?"""
    n = _nums(q)
    if len(n) < 3:
        return _unresolved("percent_of_number")
    p, x, q2 = n[0], n[1], n[2]
    number = x * 100 / p
    return _resolved_or_none(_pick(opts, number * q2 / 100), "percent_of_number")


def _train_speed(q, opts):
    n = _nums(q)
    if len(n) < 2:
        return _unresolved("train_speed")
    d, t = n[0], n[1]
    return _resolved_or_none(_pick(opts, d / t), "train_speed")


# --------------------------------------------------------------------------
# logical solvers
# --------------------------------------------------------------------------


def _number_series(q, opts):
    """Find the next term of a numeric series. Supports the common rules."""
    m = re.search(r"([-\d,\s]+)\?", q)
    if not m:
        return _unresolved("number_series")
    terms = [int(x) for x in re.findall(r"-?\d+", m.group(1))]
    if len(terms) < 3:
        return _unresolved("number_series")

    diffs = [terms[i + 1] - terms[i] for i in range(len(terms) - 1)]
    # constant difference
    if len(set(diffs)) == 1:
        return _resolved_or_none(_pick(opts, terms[-1] + diffs[0]), "series_ap")
    # constant second difference
    d2 = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
    if d2 and len(set(d2)) == 1:
        return _resolved_or_none(_pick(opts, terms[-1] + diffs[-1] + d2[0]), "series_d2")
    # geometric
    if terms[0] != 0 and all(
            terms[i] != 0 and terms[i + 1] == terms[i] * (terms[1] // terms[0] or 1)
            for i in range(len(terms) - 1)) and terms[1] % terms[0] == 0:
        r = terms[1] // terms[0]
        if all(terms[i + 1] == terms[i] * r for i in range(len(terms) - 1)):
            return _resolved_or_none(_pick(opts, terms[-1] * r), "series_gp")
    # perfect squares
    roots = [math.isqrt(t) for t in terms]
    if all(r * r == t for r, t in zip(roots, terms)):
        return _resolved_or_none(_pick(opts, (roots[-1] + 1) ** 2), "series_square")
    # fibonacci-style: each = sum of previous two
    if all(terms[i] == terms[i - 1] + terms[i - 2] for i in range(2, len(terms))):
        return _resolved_or_none(_pick(opts, terms[-1] + terms[-2]), "series_fib")
    # each = sum of previous three
    if len(terms) >= 4 and all(
            terms[i] == terms[i - 1] + terms[i - 2] + terms[i - 3] for i in range(3, len(terms))):
        return _resolved_or_none(_pick(opts, terms[-1] + terms[-2] + terms[-3]),
                                 "series_sum3")
    # n*(n+1)*(n+2) style: 0,6,24,60,120
    prod = [(i, i * (i + 1) * (i + 2)) for i in range(0, 20)]
    if all(t in [p[1] for p in prod] for t in terms):
        idxs = [[i for i, v in prod if v == t][0] for t in terms]
        if len(set(b - a for a, b in zip(idxs, idxs[1:]))) == 1:
            nxt = idxs[-1] + (idxs[1] - idxs[0])
            return _resolved_or_none(_pick(opts, prod[nxt][1]), "series_product")
    return _unresolved("number_series", f"unrecognised diffs={diffs}")


def _letter_series(q, opts):
    m = re.search(r"((?:[A-Z]\s*,\s*)+[A-Z])\s*,\s*\?", q)
    if not m:
        return _unresolved("letter_series")
    letters = re.findall(r"[A-Z]", m.group(1))
    vals = [ord(c) - 65 for c in letters]
    if len(vals) < 2:
        return _unresolved("letter_series")
    steps = [(vals[i + 1] - vals[i]) % 26 for i in range(len(vals) - 1)]
    if len(set(steps)) == 1:
        nxt = (vals[-1] + steps[0]) % 26
        return _resolved_or_none(_pick_text(opts, chr(65 + nxt)), "letter_series")
    return _unresolved("letter_series", f"steps={steps}")


def _position_code(q, opts):
    """FACE is coded as 6135 by alphabet position -> code BEAD"""
    m = re.search(r"([A-Z]{3,})\s+is coded as\s+([\d\-]+)", q)
    if not m:
        return _unresolved("position_code")
    plain, coded = m.group(1), m.group(2)
    if len(plain) != len(re.findall(r"\d+", coded)):
        return _unresolved("position_code", "length mismatch")
    pos = lambda w: "-".join(str(ord(c) - 64) for c in w) if "-" in coded else \
        "".join(str(ord(c) - 64) for c in w)
    if pos(plain) != coded:
        return _unresolved("position_code", f"rule does not reproduce {plain}")
    m2 = re.search(r"code for\s+([A-Z]{3,})", q)
    if not m2:
        return _unresolved("position_code")
    return _resolved_or_none(_pick_text(opts, pos(m2.group(1))), "position_code")


def _shift_code(q, opts):
    """MANGO written as NBOHP (+1) -> GRAPE"""
    m = re.search(r"([A-Z]{3,})\s+is written as\s+([A-Z]{3,})", q)
    if not m:
        return _unresolved("shift_code")
    src, dst = m.group(1), m.group(2)
    if len(src) != len(dst):
        return _unresolved("shift_code")
    shifts = {(ord(b) - ord(a)) % 26 for a, b in zip(src, dst)}
    if len(shifts) != 1:
        return _unresolved("shift_code", f"non-uniform shift {shifts}")
    k = shifts.pop()
    m2 = re.search(r"how is\s+([A-Z]{3,})\s+written", q)
    if not m2:
        return _unresolved("shift_code")
    out = "".join(chr((ord(c) - 65 + k) % 26 + 65) for c in m2.group(1))
    return _resolved_or_none(_pick_text(opts, out), "shift_code")


def _syllogism_all_all(q, opts):
    """All A are B, all B are C -> All A are C"""
    if re.search(r"all\s+\w+\s+are\s+\w+.*all\s+\w+\s+are\s+\w+", q, re.I | re.S):
        return _resolved_or_none(_pick_text(opts, "All A are C"), "syllogism_aa")
    return _unresolved("syllogism_aa")


def _syllogism_some(q, opts):
    """All X are Y, some Y are Z -> no conclusion"""
    if re.search(r"all\s+\w+\s+are\s+\w+.*some\s+\w+\s+are\s+\w+", q, re.I | re.S):
        hit = _pick_text(opts, "No conclusion follows")
        if hit:
            return _resolved(hit, "syllogism_some")
    return _unresolved("syllogism_some")


def _direction_net(q, opts):
    """walks a km North, turns right b km, ... -> displacement"""
    m = re.search(r"walks?\s+(\d+)\s*km\s+(north|south|east|west)", q, re.I)
    if not m:
        return _unresolved("direction_net")
    steps = re.findall(r"(\d+)\s*km\s*(north|south|east|west)?", q, re.I)
    facing = {"north": 0, "east": 90, "south": 180, "west": 270}
    cur = facing[m.group(2).lower()]
    x = y = 0
    for dist, d in steps:
        dist = int(dist)
        if d:
            cur = facing[d.lower()]
        else:
            cur = (cur + 90) % 360  # "turns right"
        dx = {0: 0, 90: dist, 180: 0, 270: -dist}[cur]
        dy = {0: dist, 90: 0, 180: -dist, 270: 0}[cur]
        x += dx
        y += dy
    return _resolved_or_none(_pick(opts, round(math.hypot(x, y), 2), tol=0.02),
                             "direction_net")


def _calendar_days(q, opts):
    m = re.search(r"today is\s+(\w+).*?(\d+)\s*days from now", q, re.I)
    if not m:
        return _unresolved("calendar_days")
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    start = days.index(m.group(1).lower())
    target = days[(start + int(m.group(2))) % 7]
    return _resolved_or_none(_pick_text(opts, target.capitalize()), "calendar_days")


def _clock_angle(q, opts):
    m = re.search(r"at\s+(\d+):(\d+)", q)
    if not m:
        return _unresolved("clock_angle")
    h, mi = int(m.group(1)) % 12, int(m.group(2))
    angle = abs(30 * h - 5.5 * mi)
    angle = min(angle, 360 - angle)
    return _resolved_or_none(_pick(opts, angle), "clock_angle")


def _venn_neither(q, opts):
    n = _nums(q)
    if len(n) < 4:
        return _unresolved("venn_neither")
    total, a, b, both = n[:4]
    return _resolved_or_none(_pick(opts, total - (a + b - both)), "venn_neither")


def _analogy_square(q, opts):
    m = re.search(r"(\d+)\s*:\s*(\d+)\s*::\s*(\d+)\s*:\s*\?", q)
    if not m:
        return _unresolved("analogy_square")
    a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if b == a * a:
        return _resolved_or_none(_pick(opts, c * c), "analogy_square")
    return _unresolved("analogy_square")


def _taller_chain(q, opts):
    """A taller than B, B taller than C -> who is tallest"""
    m = re.search(r"(\w)\s+is taller than\s+(\w)", q)
    if not m:
        return _unresolved("taller_chain")
    return _resolved_or_none(_pick_text(opts, m.group(1)), "taller_chain")


def _dice_opposite(q, opts):
    n = _ints(q)
    if len(n) < 4:
        return _unresolved("dice_opposite")
    pairs = set()
    for i in range(0, len(n) - 1, 2):
        pairs.add(frozenset((n[i], n[i + 1])))
    for f in range(1, 7):
        if all(frozenset((f, g)) not in pairs for g in range(1, 7) if g != f):
            return _resolved_or_none(_pick(opts, f), "dice_opposite")
    return _unresolved("dice_opposite")


# --------------------------------------------------------------------------
# dispatch table (order matters: most specific first)
# --------------------------------------------------------------------------

_FAMILIES: list[tuple[str, re.Pattern, Callable]] = [
    ("successive_pct", re.compile(r"increased by .* and then decreased by", re.I), _successive_pct),
    ("population_pct", re.compile(r"population of a town increases", re.I), _population_pct),
    ("reverse_discount", re.compile(r"after a .*discount.*original price", re.I), _reverse_discount),
    ("mixture_water", re.compile(r"milk-water mixture", re.I), _mixture_water),
    ("election_margin", re.compile(r"election between two candidates", re.I), _election_margin),
    ("profit_after_increment", re.compile(r"both cost price and selling price are increased", re.I),
     _profit_after_increment),
    ("markup_discount", re.compile(r"marks an article .*above cost price", re.I), _markup_discount),
    ("two_articles", re.compile(r"two articles at rs", re.I), _two_articles),
    ("alligation", re.compile(r"in what ratio must .* be mixed", re.I), _alligation),
    ("income_ratio", re.compile(r"ratio of incomes", re.I), _income_ratio),
    ("age_ratio", re.compile(r"present ages of .* in ratio", re.I), _age_ratio),
    ("false_weight", re.compile(r"weight instead of", re.I), _false_weight),
    ("cp_eq_sp", re.compile(r"cost price of .* equals the selling price of", re.I), _cp_eq_sp),
    ("efficiency", re.compile(r"times as efficient as", re.I), _efficiency),
    ("pipes", re.compile(r"pipe .* fills .* empties", re.I), _pipes),
    ("work_fraction_left", re.compile(r"work together for .*fraction of work is left", re.I),
     _work_fraction_left),
    ("work_together", re.compile(r"how long will they take together|they take together", re.I),
     _work_together),
    ("average_speed", re.compile(r"returns at .*average speed", re.I), _average_speed),
    ("train_platform", re.compile(r"train .* crosses a platform", re.I), _train_platform),
    ("two_trains", re.compile(r"two trains of lengths", re.I), _two_trains),
    ("dice_sum", re.compile(r"two dice are thrown", re.I), _dice_sum),
    ("card_prob", re.compile(r"card is drawn from a deck", re.I), _card_prob),
    ("largest_divisible", re.compile(r"largest \d+-digit number divisible", re.I), _largest_divisible),
    ("unit_digit", re.compile(r"unit digit of", re.I), _unit_digit),
    ("lcm_hcf", re.compile(r"lcm of two numbers", re.I), _lcm_hcf),
    ("pie_chart", re.compile(r"pie chart", re.I), _pie_chart),
    ("average_sales", re.compile(r"average sales", re.I), _average_sales),
    ("arrangements", re.compile(r"in how many ways", re.I), _arrangements),
    ("milk_replacement", re.compile(r"removed and replaced with water", re.I), _milk_replacement),
    ("average_replaced", re.compile(r"average of \d+ numbers is .*replaced by", re.I),
     _average_replaced),
    ("weighted_average", re.compile(r"average of \d+ boys is .*average of \d+ girls", re.I),
     _weighted_average),
    ("compound_interest", re.compile(r"compound interest", re.I), _compound_interest),
    ("simple_interest", re.compile(r"simple interest on", re.I), _simple_interest),
    ("rate_from_si", re.compile(r"gives .* as simple interest", re.I), _rate_from_si),
    ("boat_stream", re.compile(r"upstream .* downstream", re.I), _boat_stream),
    ("consumption", re.compile(r"price of sugar increases", re.I), _consumption),
    ("circle", re.compile(r"area of a circle", re.I), _circle_area_circumference),
    ("cube", re.compile(r"volume of a cube", re.I), _cube_surface),
    ("profit_share", re.compile(r"invest in a business in ratio", re.I), _profit_share),
    ("balls_both_red", re.compile(r"bag contains .* balls", re.I), _balls_both_red),
    ("percent_of_number", re.compile(r"% of a number is .*what is", re.I), _percent_of_number),
    ("train_speed", re.compile(r"train travels .* what is its speed", re.I), _train_speed),
    ("profit_sell_price", re.compile(r"buys an item for rs", re.I), _profit_sell_price),
    ("letter_series", re.compile(r"(?:[A-Z]\s*,\s*){2,}[A-Z]\s*,\s*\?", re.S), _letter_series),
    ("number_series", re.compile(r"(?:find the (?:next|missing) (?:number|term)|complete the series)"
                                 r".*\d\s*,\s*\d", re.I | re.S), _number_series),
    ("position_code", re.compile(r"position in the alphabet|coded as [\d\-]+", re.I), _position_code),
    ("shift_code", re.compile(r"is written as\s+[A-Z]{3,}", re.I), _shift_code),
    ("clock_angle", re.compile(r"angle between the hour and minute hands", re.I), _clock_angle),
    ("calendar_days", re.compile(r"days from now", re.I), _calendar_days),
    ("venn_neither", re.compile(r"like neither", re.I), _venn_neither),
    ("analogy_square", re.compile(r"\d+\s*:\s*\d+\s*::\s*\d+\s*:\s*\?", re.I), _analogy_square),
    ("dice_opposite", re.compile(r"opposite face", re.I), _dice_opposite),
    ("direction_net", re.compile(r"walks?\s+\d+\s*km\s+(?:north|south|east|west)", re.I),
     _direction_net),
    ("taller_chain", re.compile(r"is taller than", re.I), _taller_chain),
    ("syllogism_some", re.compile(r"some\s+\w+\s+are\s+\w+", re.I), _syllogism_some),
    ("syllogism_aa", re.compile(r"all\s+\w+\s+are\s+\w+", re.I), _syllogism_all_all),
]


def solve(item: dict) -> OracleResult:
    """Recompute the answer to an MCQ from its question text alone."""
    q = str(item.get("question") or "")
    opts = item.get("options")
    if not isinstance(opts, list) or len(opts) != 4:
        return _unresolved("not_mcq", "options must be a 4-item list")
    if not q:
        return _unresolved("empty_question")

    for family, pattern, fn in _FAMILIES:
        if not pattern.search(q):
            continue
        try:
            res = fn(q, [str(o) for o in opts])
        except Exception as e:  # a solver bug must never look like a pass
            return _unresolved(family, f"solver_error:{type(e).__name__}:{e}")
        if res.resolved:
            return res
        return res  # matched a family but could not resolve: stop, do not guess
    return _unresolved("no_family")


def verdict(item: dict) -> tuple[str, str]:
    """('AGREE'|'DISAGREE'|'NO_ORACLE', detail) for a single item."""
    res = solve(item)
    if not res.resolved:
        return "NO_ORACLE", f"{res.family}:{res.detail}"[:120]
    key = str(item.get("correct_answer") or "").strip()
    if _norm(res.answer) == _norm(key):
        return "AGREE", res.family
    return "DISAGREE", f"{res.family}: oracle={res.answer!r} key={key!r}"
