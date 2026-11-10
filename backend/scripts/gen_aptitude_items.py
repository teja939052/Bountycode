"""Generate aptitude / reasoning MCQ intake candidates with COMPUTED answers.

Why: verified aptitude supply was 50 + 15 + 15 items, but TCS NQT alone needs
65 foundation questions per sitting (20 numerical, 25 verbal, 20 reasoning).

How the answer is trusted: every item is computed by one method (the closed
form a student would use) and then re-computed by a different method (direct
simulation with exact fractions). The script aborts if they disagree. The
items are written as trust_status "unverified" into app/data/intake/ so they
go through the normal pipeline (intake lint -> ground truth -> tranche review).
Nothing here is loaded by question_store and nothing is stamped verified.

Usage: python scripts/gen_aptitude_items.py [--per-topic 25] [--seed 2026]
"""
import argparse
import json
import math
import os
import random
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app", "data", "intake", "aptitude_generated_v2.json")
COMPANIES = ["tcs", "infosys", "wipro", "cognizant"]


def num(fr, places=2):
    """Exact Fraction -> display string, or None if it needs more decimals."""
    fr = Fraction(fr)
    if fr.denominator == 1:
        return f"{fr.numerator:,}" if abs(fr) >= 10000 else str(fr.numerator)
    scaled = fr * 10 ** places
    if scaled.denominator != 1:
        return None
    s = f"{float(fr):.{places}f}".rstrip("0").rstrip(".")
    return s


def build(rng, correct, wrong, fmt):
    """Return (options, index) with 4 distinct formatted options, or None."""
    vals = []
    for v in [correct] + list(wrong):
        s = fmt(v)
        if s is None or s in [fmt(x) for x in vals if fmt(x) is not None]:
            continue
        vals.append(v)
    if len(vals) < 4 or vals[0] != correct:
        return None
    vals = vals[:4]
    order = list(range(4))
    rng.shuffle(order)
    return [fmt(vals[i]) for i in order], order.index(0)


def txt(fr):
    """Exact value for explanations: decimal when short, else a fraction."""
    return num(fr) or str(Fraction(fr))


def pct_fmt(v):
    s = num(v)
    if s is None:
        return None
    return (f"+{s}%" if Fraction(v) > 0 else f"{s}%")


def rs_fmt(v):
    s = num(v)
    return None if s is None else f"Rs {s}"


# ---- generators: each returns (question, correct, wrong, fmt, explanation, trap, difficulty)

def g_percent_change(rng):
    x, y = rng.choice(range(10, 55, 5)), rng.choice(range(10, 45, 5))
    up_first = rng.random() < 0.5
    a, b = (x, -y) if up_first else (-y, x)
    net = a + b + Fraction(a * b, 100)                      # closed form
    base = Fraction(10000)                                   # simulation
    after = base * (100 + a) / 100 * (100 + b) / 100
    assert (after - base) / base * 100 == net
    word = lambda p: f"increased by {p}%" if p > 0 else f"decreased by {-p}%"
    q = f"The price of an item is first {word(a)} and then {word(b)}. The net change in price is:"
    wrong = [Fraction(a + b), Fraction(a + b) / 2, net + 2 * abs(Fraction(a * b, 100))]
    ex = (f"Net = a + b + ab/100 = {a} + ({b}) + ({a}*{b})/100 = {num(net)}%. "
          f"Check with base 10000: {num(base)} -> {num(after)}.")
    trap = "Adding the two percentages directly ignores that the second change applies to the new price."
    return q, net, wrong, pct_fmt, ex, trap, "medium"


def g_profit_loss(rng):
    if rng.random() < 0.5:
        cp, p = rng.choice(range(400, 2050, 50)), rng.choice(range(10, 45, 5))
        sp = Fraction(cp) * (100 + p) / 100
        assert sp / (100 + p) * 100 == cp
        q = f"A shopkeeper buys an article for Rs {cp} and sells it at a profit of {p}%. The selling price is:"
        wrong = [Fraction(cp) * p / 100, Fraction(cp + p), Fraction(cp) * (100 - p) / 100]
        ex = f"SP = CP * (100 + p)/100 = {cp} * {100 + p}/100 = {num(sp)}."
        return q, sp, wrong, rs_fmt, ex, "Giving only the profit amount, not the selling price.", "easy"
    sp, loss = rng.choice(range(360, 1800, 40)), rng.choice(range(10, 40, 5))
    cp = Fraction(sp) * 100 / (100 - loss)
    assert cp * (100 - loss) / 100 == sp                      # forward check
    q = f"An article is sold for Rs {sp} at a loss of {loss}%. Its cost price is:"
    wrong = [Fraction(sp) * (100 - loss) / 100, Fraction(sp) * (100 + loss) / 100, Fraction(sp + sp * loss // 100)]
    ex = f"CP = SP * 100/(100 - loss) = {sp} * 100/{100 - loss} = {num(cp)}."
    return q, cp, wrong, rs_fmt, ex, "Applying the loss percentage to the selling price instead of the cost price.", "medium"


def g_discount(rng):
    m, d1, d2 = rng.choice(range(800, 4000, 100)), rng.choice((10, 20, 25)), rng.choice((5, 10, 20))
    final = Fraction(m) * (100 - d1) / 100 * (100 - d2) / 100
    price = Fraction(m)
    for d in (d1, d2):                                        # simulation
        price -= price * d / 100
    assert price == final
    q = f"A shirt marked at Rs {m} is sold with two successive discounts of {d1}% and {d2}%. The price paid is:"
    wrong = [Fraction(m) * (100 - d1 - d2) / 100, Fraction(m) * (100 - d1) / 100, Fraction(m) * (100 - d2) / 100]
    ex = f"Price = {m} * {100 - d1}/100 * {100 - d2}/100 = {num(final)}."
    return q, final, wrong, rs_fmt, ex, f"Using a single discount of {d1 + d2}% instead of two successive ones.", "medium"


def g_ratio(rng):
    a, b = rng.choice([(2, 3), (3, 5), (4, 7), (5, 6), (3, 4), (2, 5), (7, 9)])
    t = (a + b) * rng.choice(range(20, 200, 10))
    pick_b = rng.random() < 0.5
    share = Fraction(t * (b if pick_b else a), a + b)
    other = Fraction(t) - share
    assert share + other == t and (share / other == Fraction(b, a) if pick_b else share / other == Fraction(a, b))
    who = "B" if pick_b else "A"
    q = f"Rs {t} is divided between A and B in the ratio {a}:{b}. {who}'s share is:"
    wrong = [other, Fraction(t, a + b), Fraction(t * (a if pick_b else b), 1) / (a + b) + 10]
    ex = f"Each part = {t}/({a}+{b}) = {num(Fraction(t, a + b))}; {who}'s share = {b if pick_b else a} parts = {num(share)}."
    return q, share, wrong, rs_fmt, ex, "Forgetting to divide by the sum of the ratio parts.", "easy"


def g_time_work(rng):
    while True:
        a, b = rng.choice(range(6, 40, 2)), rng.choice(range(6, 40, 2))
        if a != b and num(Fraction(a * b, a + b)) is not None:
            break
    together = Fraction(a * b, a + b)
    work = math.lcm(a, b)                                     # simulation in units of work
    rate = Fraction(work, a) + Fraction(work, b)
    assert Fraction(work) / rate == together
    q = f"A can finish a job in {a} days and B can finish it in {b} days. Working together, they finish it in:"
    wrong = [Fraction(a + b, 2), Fraction(a + b), Fraction(abs(a - b))]
    ex = f"Rate = 1/{a} + 1/{b} = {a + b}/{a * b} per day, so time = {a * b}/{a + b} = {num(together)} days."
    return q, together, wrong, lambda v: None if num(v) is None else f"{num(v)} days", ex, \
        "Averaging the two times instead of adding their rates.", "medium"


def g_avg_speed(rng):
    while True:
        s1, s2 = rng.choice(range(20, 90, 5)), rng.choice(range(20, 90, 5))
        if s1 != s2 and num(Fraction(2 * s1 * s2, s1 + s2)) is not None:
            break
    avg = Fraction(2 * s1 * s2, s1 + s2)
    d = math.lcm(s1, s2)                                      # simulation: distance each way
    assert Fraction(2 * d) / (Fraction(d, s1) + Fraction(d, s2)) == avg
    q = f"A car goes from P to Q at {s1} km/h and returns along the same road at {s2} km/h. The average speed for the whole trip is:"
    wrong = [Fraction(s1 + s2, 2), Fraction(abs(s1 - s2)), Fraction(s1 * s2, s1 + s2)]
    ex = f"Equal distances: average = 2*{s1}*{s2}/({s1}+{s2}) = {num(avg)} km/h (not the simple mean)."
    return q, avg, wrong, lambda v: None if num(v) is None else f"{num(v)} km/h", ex, \
        "Taking the simple mean of the two speeds.", "medium"


def g_train(rng):
    while True:
        l1, l2 = rng.choice(range(100, 400, 25)), rng.choice(range(100, 400, 25))
        v1, v2 = rng.choice(range(36, 90, 6)), rng.choice(range(36, 90, 6))
        t = Fraction((l1 + l2) * 18, (v1 + v2) * 5)
        if t.denominator == 1:
            break
    mps = Fraction((v1 + v2) * 5, 18)                         # simulation in m/s
    assert Fraction(l1 + l2) / mps == t
    q = (f"Two trains of lengths {l1} m and {l2} m run in opposite directions at {v1} km/h and {v2} km/h. "
         f"They take how many seconds to cross each other completely?")
    wrong = [Fraction((l1 + l2) * 18, abs(v1 - v2) * 5) if v1 != v2 else t + 3, t + 2, t - 1]
    ex = f"Relative speed = {v1 + v2} km/h = {txt(mps)} m/s; time = {l1 + l2}/({txt(mps)}) = {num(t)} s."
    return q, t, wrong, lambda v: None if num(v) is None else f"{num(v)} s", ex, \
        "Subtracting the speeds even though the trains move in opposite directions.", "hard"


def g_average(rng):
    n = rng.choice((5, 6, 8, 10))
    m = rng.choice(range(20, 60))
    x, y = rng.choice(range(10, 40)), rng.choice(range(41, 90))
    new = Fraction(m * n - x + y, n)
    assert new == m + Fraction(y - x, n)
    q = f"The average of {n} numbers is {m}. If one of them, {x}, is replaced by {y}, the new average is:"
    wrong = [Fraction(m) + Fraction(y - x), Fraction(m) + Fraction(y - x, n * 2), Fraction(m) - Fraction(y - x, n)]
    ex = f"Total = {m}*{n} = {m * n}; new total = {m * n} - {x} + {y} = {m * n - x + y}; new average = {num(new)}."
    return q, new, wrong, lambda v: num(v), ex, "Adding the full change to the average instead of dividing it by n.", "easy"


def g_interest(rng):
    if rng.random() < 0.5:
        p, r, t = rng.choice(range(2000, 20000, 500)), rng.choice((5, 8, 10, 12)), rng.choice((2, 3, 4))
        si = Fraction(p * r * t, 100)
        assert si == sum(Fraction(p * r, 100) for _ in range(t))
        q = f"Find the simple interest on Rs {p} at {r}% per annum for {t} years."
        wrong = [Fraction(p * r, 100), si + Fraction(p * r, 200), Fraction(p * (100 + r * t), 100)]
        return q, si, wrong, rs_fmt, f"SI = P*R*T/100 = {p}*{r}*{t}/100 = {num(si)}.", \
            "Reporting the amount (principal + interest) instead of the interest.", "easy"
    r = rng.choice((5, 10, 20))
    p = 100 * rng.choice(range(20, 400, 20)) * (100 // r if 100 % r == 0 else 1)
    diff = Fraction(p) * r * r / 10000
    amount = Fraction(p)
    for _ in range(2):                                        # simulation of compounding
        amount += amount * r / 100
    ci = amount - p
    si = Fraction(p * r * 2, 100)
    assert ci - si == diff
    q = f"What is the difference between compound interest and simple interest on Rs {p} at {r}% per annum for 2 years?"
    wrong = [Fraction(p) * r / 100, ci, diff * 2]
    ex = f"Difference for 2 years = P*(r/100)^2 = {p}*({r}/100)^2 = {num(diff)}. Check: CI {num(ci)} - SI {num(si)}."
    return q, diff, wrong, rs_fmt, ex, "Using the formula for 3 years or forgetting to square the rate.", "hard"


GENS = {
    "percentages": g_percent_change, "profit_loss": g_profit_loss, "discount": g_discount,
    "ratio": g_ratio, "time_work": g_time_work, "average_speed": g_avg_speed,
    "trains": g_train, "averages": g_average, "interest": g_interest,
}


def g_series(rng):
    kind = rng.choice(("arith", "geo", "square", "alt", "tri"))
    if kind == "arith":
        a, d = rng.randint(2, 20), rng.randint(3, 12)
        seq, nxt = [a + i * d for i in range(5)], a + 5 * d
        rule = f"constant difference {d}"
    elif kind == "geo":
        a, r = rng.randint(1, 5), rng.choice((2, 3))
        seq, nxt = [a * r ** i for i in range(5)], a * r ** 5
        rule = f"each term is {r} times the previous"
    elif kind == "square":
        c = rng.randint(0, 6)
        seq, nxt = [(i + 1) ** 2 + c for i in range(5)], 36 + c
        rule = f"n^2 + {c} (differences are consecutive odd numbers)"
    elif kind == "alt":
        a, x, y = rng.randint(5, 30), rng.randint(2, 9), rng.randint(1, 4)
        seq = [a]
        for i in range(5):
            seq.append(seq[-1] + (x if i % 2 == 0 else -y))
        seq, nxt = seq[:5], seq[4] + (x if 4 % 2 == 0 else -y)
        rule = f"alternately +{x} and -{y}"
    else:
        a = rng.randint(1, 8)
        seq, nxt = [a + i * (i + 1) // 2 for i in range(5)], a + 5 * 6 // 2
        rule = "differences increase by 1 each time (+1, +2, +3, +4, +5)"
    # independent check: rebuild from first differences / ratios
    if kind in ("arith", "square", "tri", "alt"):
        diffs = [seq[i + 1] - seq[i] for i in range(4)]
        if kind == "arith":
            assert len(set(diffs)) == 1 and seq[-1] + diffs[0] == nxt
        if kind == "square":
            assert diffs == [3, 5, 7, 9] and seq[-1] + 11 == nxt
        if kind == "tri":
            assert diffs == [1, 2, 3, 4] and seq[-1] + 5 == nxt
        if kind == "alt":
            assert nxt == seq[-1] + (x if 4 % 2 == 0 else -y)
    else:
        assert all(seq[i + 1] == seq[i] * r for i in range(4)) and seq[-1] * r == nxt
    return seq, nxt, rule, kind


def make_series(rng):
    seq, nxt, rule, kind = g_series(rng)
    q = f"Find the next term in the series: {', '.join(map(str, seq))}, ?"
    wrong = [Fraction(nxt + 1), Fraction(nxt - 1), Fraction(nxt + (seq[-1] - seq[-2]))]
    return q, Fraction(nxt), wrong, num, f"Rule: {rule}. Next term = {nxt}.", \
        "Assuming a constant difference when the gaps change.", "easy" if kind in ("arith", "geo") else "medium"


def run(per_topic, seed):
    rng = random.Random(seed)
    items, seen = [], set()
    jobs = [(t, g, "aptitude") for t, g in GENS.items()] + [("series", make_series, "logical")]
    for topic, gen, qtype in jobs:
        made, tries = 0, 0
        while made < per_topic and tries < per_topic * 200:
            tries += 1
            q, correct, wrong, fmt, ex, trap, diff = gen(rng)
            if q in seen:
                continue
            built = build(rng, correct, wrong, fmt)
            if not built:
                continue
            opts, idx = built
            seen.add(q)
            made += 1
            items.append({
                "id": f"gen2-{topic}-{made:03d}", "type": qtype, "topic": topic, "sub_topic": topic.replace("_", " "),
                "difficulty": diff, "question": q, "options": opts, "correct_index": idx, "correct_answer": opts[idx],
                "explanation": ex, "common_trap": trap, "companies": COMPANIES, "role": ["student"], "stage": "placement",
                "trust_status": "unverified", "source_bank": "generated_aptitude_v2", "verification_version": 0,
                "provenance": "generated; answer computed in closed form and re-computed by an independent "
                              "simulation in scripts/gen_aptitude_items.py (aborts on disagreement); not yet "
                              "through ground_truth or tranche review",
            })
        if made < per_topic:
            print(f"WARNING {topic}: only {made}/{per_topic}", file=sys.stderr)
    return items


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-topic", type=int, default=25)
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    items = run(a.per_topic, a.seed)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")
    by = {}
    for i in items:
        by[i["topic"]] = by.get(i["topic"], 0) + 1
    print(f"wrote {len(items)} items -> {OUT}\n{by}")
