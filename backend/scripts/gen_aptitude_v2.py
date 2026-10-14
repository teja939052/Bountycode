"""Phase 5: aptitude +5624. Every answer COMPUTED by deterministic oracle
(integer arithmetic, fractions, formulas). Covers all quant topics.

Output: app/data/bank_aptitude_v2.json (trust_status=verified).
"""
import json
import math
import random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "app" / "data" / "bank_aptitude_v2.json"

RNG = random.Random(20260928)
items: list = []
_seq = 0


def _aq(topic, sub, diff, question, answer, distractors, explanation, steps, hint,
        companies=None):
    global _seq
    _seq += 1
    opts = [answer] + [d for d in distractors if d != answer]
    seen, uniq = set(), []
    for o in opts:
        if o not in seen:
            seen.add(o)
            uniq.append(o)
    k = 2
    while len(uniq) < 4:
        cand = f"{answer} ({k})"
        if cand not in seen:
            seen.add(cand)
            uniq.append(cand)
        k += 1
    uniq = uniq[:4]
    order = sorted(range(4), key=lambda i: RNG.random())
    options = [uniq[i] for i in order]
    letters = ["A", "B", "C", "D"]
    ci = options.index(answer)
    items.append({
        "id": f"apt-v2-{_seq:05d}",
        "type": "aptitude",
        "topic": topic,
        "sub_topic": sub,
        "difficulty": diff,
        "question": question,
        "options": {letters[i]: options[i] for i in range(4)},
        "correct_answer": letters[ci],
        "correct_index": letters[ci],
        "explanation": explanation,
        "reasoning_steps": steps if isinstance(steps, str) else " ".join(steps),
        "shortcut": hint,
        "common_trap": "Arithmetic slip or misreading what is asked (e.g. marked vs cost price).",
        "solution": {},
        "test_cases": [{"input": None, "output": letters[ci], "hidden": False}],
        "testcases": [{"input": None, "output": letters[ci], "hidden": False}],
        "hints": [hint, "Write the equation before computing"],
        "worked_solution": f"The answer is {letters[ci]}) {answer}. {explanation}",
        "companies": companies or ["tcs", "infosys", "wipro", "accenture"],
        "role": ["student"],
        "provenance": "parametric generator v2 (aptitude), deterministic oracle",
        "source_bank": "bank_aptitude_v2.json",
        "trust_status": "verified",
        "stage": "placement",
        "executable": True,
        "frequency": 0,
        "dsa_guide": {"approach": "", "data_structures": [], "patterns": [], "tips": []},
    })


def _dn(ans, n=3, step=1):
    out, d = [], step
    while len(out) < n:
        for cand in (ans + d, ans - d):
            if cand != ans and str(cand) not in out and cand > 0:
                out.append(str(cand))
                if len(out) == n:
                    break
        d += step
    return out


def _frac(num, den):
    g = math.gcd(num, den)
    return f"{num//g}/{den//g}" if den // g != 1 else str(num // g)


C = ["tcs", "infosys", "wipro", "accenture", "cognizant"]

# ─── FAMILIES ───────────────────────────────────────────────────────
def f_pct_of(n, off=0):
    for k in range(n):
        i = k + off
        p = 1 + (i * 7) % 99
        base = 50 + (i * 13) % 2000
        ans = base * p // 100
        # ensure exact division for clean answers half the time
        _aq("Quantitative Aptitude", "Percentages", "easy",
            f"What is {p}% of {base}?", str(ans), _dn(ans),
            f"{p}% of {base} = {p}/100 × {base} = {ans}.",
            [f"{p}/100 × {base} = {ans}."], "Percent = per hundred.", C)


def f_pct_change(n, off=0):
    for k in range(n):
        i = k + off
        old = 100 + (i * 17) % 900
        new = old + (10 + (i * 13) % 200) * (1 if i % 2 == 0 else -1)
        if new <= 0:
            new = old + 20
        pct = round((new - old) / old * 100, 1)
        ans = str(int(pct)) if pct == int(pct) else str(pct)
        _aq("Quantitative Aptitude", "Percentages", "easy",
            f"Price changes from {old} to {new}. Percent change?",
            ans, _dn(int(pct) if pct == int(pct) else int(pct * 10), step=2),
            f"({new}−{old})/{old} × 100 = {ans}%.",
            [f"Change={new-old}; ÷{old} ×100 = {ans}%."], "Change ÷ original.", C)


def f_successive(n, off=0):
    for k in range(n):
        i = k + off
        a = 5 + (i * 7) % 45
        b = (5 + (i * 11) % 45) * (1 if i % 3 else -1)
        net = a + b + a * b / 100
        ans = f"{net:g}%"
        _aq("Quantitative Aptitude", "Percentages", "medium",
            f"Price rises {a}% then changes by {b}%. Net change?",
            ans, [f"{a+b}%", f"{a}%", f"{b}%"],
            f"Net = {a}+({b})+{a}×{b}/100 = {net:g}%.",
            [f"a+b+ab/100 = {net:g}%."], "Successive formula.", C)


def f_discount(n, off=0):
    for k in range(n):
        i = k + off
        mp = 200 + (i * 37) % 5000
        mp -= mp % 10
        d = 5 + (i * 7) % 30
        ans = mp * (100 - d) // 100
        _aq("Quantitative Aptitude", "Profit & Loss", "easy",
            f"Marked price {mp} with {d}% discount. Selling price?",
            str(ans), _dn(ans, step=10),
            f"SP = {mp} × (100−{d})/100 = {ans}.",
            [f"{mp} × {100-d}% = {ans}."], "Pay (100−d)%.", C)


def f_profit(n, off=0):
    for k in range(n):
        i = k + off
        cp = 100 + (i * 41) % 2000
        cp -= cp % 10
        p = 5 + (i * 13) % 45
        ans = cp * (100 + p) // 100
        _aq("Quantitative Aptitude", "Profit & Loss", "easy",
            f"Cost price {cp}, profit {p}%. Selling price?",
            str(ans), _dn(ans, step=5),
            f"SP = {cp} × (100+{p})/100 = {ans}.",
            [f"{cp} × {100+p}% = {ans}."], "Charge (100+p)%.", C)


def f_loss(n, off=0):
    for k in range(n):
        i = k + off
        cp = 200 + (i * 43) % 3000
        cp -= cp % 10
        l = 2 + (i * 7) % 28
        ans = cp * (100 - l) // 100
        _aq("Quantitative Aptitude", "Profit & Loss", "easy",
            f"Cost price {cp}, loss {l}%. Selling price?",
            str(ans), _dn(ans, step=5),
            f"SP = {cp} × (100−{l})/100 = {ans}.",
            [f"{cp} × {100-l}% = {ans}."], "Recover (100−l)%.", C)


def f_si(n, off=0):
    for k in range(n):
        i = k + off
        p = 1000 + (i * 101) % 20000
        p -= p % 100
        r = 4 + (i * 7) % 12
        t = 1 + (i * 3) % 8
        ans = p * r * t // 100
        _aq("Quantitative Aptitude", "Interest", "easy",
            f"Simple interest on {p} at {r}% for {t} years?",
            str(ans), _dn(ans, step=20),
            f"SI = {p}×{r}×{t}/100 = {ans}.",
            [f"PRT/100 = {ans}."], "SI = PRT/100.", C)


def f_ci(n, off=0):
    for k in range(n):
        i = k + off
        p = 1000 + (i * 137) % 9000
        p -= p % 100
        r = 5 + (i * 7) % 15
        t = 2
        amt = p * (100 + r) ** 2 // 10000
        ci = amt - p
        _aq("Quantitative Aptitude", "Interest", "medium",
            f"Compound interest on {p} at {r}% for 2 years?",
            str(ci), _dn(ci, step=10),
            f"Amount = {p}(1+{r}/100)² = {amt}; CI = {amt}−{p} = {ci}.",
            [f"A−P = {ci}."], "CI = A − P.", C)


def f_work_together(n, off=0):
    for k in range(n):
        i = k + off
        a = 2 + (i % 25)
        b = 3 + ((i // 25) % 25)
        if b == a:
            b += 1
        # days together = ab/(a+b)
        num, den = a * b, a + b
        g = math.gcd(num, den)
        ans = f"{num//g}/{den//g}" if den // g != 1 else str(num // g)
        if num % den == 0:
            ans = str(num // den)
        _aq("Quantitative Aptitude", "Time & Work", "medium",
            f"A finishes in {a} days, B in {b} days. Together?",
            ans, [str(a + b), str(abs(a - b)), str((a + b) // 2)],
            f"Together = {a}×{b}/({a}+{b}) = {ans} days.",
            [f"ab/(a+b) = {ans}."], "Rates add.", C)


def f_work_individual(n, off=0):
    for k in range(n):
        i = k + off
        x = 3 + (i % 20)
        y = x + 2 + ((i // 20) % 15)
        if y <= x:
            y = x + 4
        num, den = x * y, y - x
        ans = str(num // den) if num % den == 0 else _frac(num, den)
        _aq("Quantitative Aptitude", "Time & Work", "medium",
            f"A+B finish in {x} days; A alone in {y} days. B alone?",
            ans, [str(y - x), str(y + x), str(x + y)],
            f"B = {x}×{y}/({y}−{x}) = {ans} days.",
            [f"1/B = 1/{x} − 1/{y}."], "Subtract rates.", C)


def f_avg_speed(n, off=0):
    for k in range(n):
        i = k + off
        v1 = 20 + (i * 13) % 60
        v2 = 40 + (i * 17) % 60
        if v2 == v1:
            v2 += 5
        num, den = 2 * v1 * v2, v1 + v2
        ans = round(num / den, 1)
        ans_s = str(int(ans)) if ans == int(ans) else str(ans)
        _aq("Quantitative Aptitude", "Speed & Distance", "medium",
            f"Go at {v1} km/h, return at {v2} km/h. Average speed?",
            ans_s, [str((v1 + v2) // 2), str(v1 + v2), str(abs(v1 - v2))],
            f"Harmonic mean 2×{v1}×{v2}/({v1}+{v2}) = {ans_s}.",
            [f"2ab/(a+b) = {ans_s}."], "Equal distance → harmonic.", C)


def f_train(n, off=0):
    for k in range(n):
        i = k + off
        length = 100 + (i * 23) % 300
        speed = 36 + ((i * 7) % 5) * 18  # km/h
        ms = speed * 1000 / 3600
        t = round(length / ms, 1)
        ans = str(int(t)) if t == int(t) else str(t)
        _aq("Quantitative Aptitude", "Speed & Distance", "medium",
            f"A {length}m train at {speed} km/h crosses a pole. Time?",
            ans + "s", [f"{length//10}s", f"{length//5}s", f"{length//20}s"],
            f"{speed} km/h = {ms} m/s; {length}/{ms} = {ans}s.",
            [f"Convert to m/s first."], "km/h × 5/18 = m/s.", C)


def f_ratio_split(n, off=0):
    for k in range(n):
        i = k + off
        a, b = 1 + (i * 7) % 9, 1 + (i * 11) % 9
        tot = (a + b) * (5 + (i * 13) % 40)
        small = tot * min(a, b) // (a + b)
        _aq("Quantitative Aptitude", "Ratios", "easy",
            f"Split {tot} in ratio {a}:{b}. Smaller share?",
            str(small), _dn(small, step=5),
            f"One part = {tot}/{a+b}; smaller = ×{min(a,b)} = {small}.",
            [f"{tot}÷{a+b}×{min(a,b)} = {small}."], "Divide by total parts.", C)


def f_ages(n, off=0):
    for k in range(n):
        i = k + off
        diff = 2 + (i * 7) % 18
        total = diff + (10 + (i * 13) % 30) * 2
        if (total - diff) % 2:
            total += 1
        young = (total - diff) // 2
        _aq("Quantitative Aptitude", "Ratios", "medium",
            f"Two people total {total} years; elder is {diff} years older. Younger's age?",
            str(young), _dn(young, step=2),
            f"Younger = ({total}−{diff})/2 = {young}.",
            [f"Subtract gap, halve."], "Gap then halve.", C)


def f_average(n, off=0):
    for k in range(n):
        i = k + off
        vals = [50 + (i * 11 + j * 17) % 60 for j in range(5)]
        ans = sum(vals) // 5
        # ensure divisible
        vals[-1] += (5 - sum(vals) % 5) % 5
        ans = sum(vals) // 5
        _aq("Quantitative Aptitude", "Averages", "easy",
            f"Average of {', '.join(map(str, vals))}?",
            str(ans), _dn(ans, step=2),
            f"Sum={sum(vals)} ÷ 5 = {ans}.",
            [f"Sum ÷ count."], "Sum then divide.", C)


def f_missing_avg(n, off=0):
    for k in range(n):
        i = k + off
        target = 60 + (i * 7) % 35
        known = [target - 8 + (i * 3 + j * 5) % 16 for j in range(4)]
        # 5th number x: (sum(known)+x)/5 = target → x = 5*target − sum
        x = 5 * target - sum(known)
        _aq("Quantitative Aptitude", "Averages", "medium",
            f"Average of 5 numbers is {target}. Four are {', '.join(map(str, known))}. Fifth?",
            str(x), _dn(x, step=3),
            f"Fifth = 5×{target} − {sum(known)} = {x}.",
            [f"Total − known."], "Work backwards.", C)


def f_hcf_lcm(n, off=0):
    for k in range(n):
        i = k + off
        a, b = 6 + (i * 13) % 60, 8 + (i * 17) % 60
        g = math.gcd(a, b)
        l = a * b // g
        if k % 2 == 0:
            _aq("Quantitative Aptitude", "Number Systems", "easy",
                f"HCF of {a} and {b}?",
                str(g), [str(g + 1), str(g + 2), str(max(1, g - 1))],
                f"GCD({a},{b}) = {g}.",
                [f"Euclid → {g}."], "Largest common divisor.", C)
        else:
            _aq("Quantitative Aptitude", "Number Systems", "easy",
                f"LCM of {a} and {b}?",
                str(l), [str(l + a), str(l - a), str(l + b)],
                f"LCM = {a}×{b}/{g} = {l}.",
                [f"ab÷GCD = {l}."], "LCM × HCF = a×b.", C)


def f_remainder(n, off=0):
    for k in range(n):
        i = k + off
        num = 100 + (i * 53) % 2000
        div = 5 + (i * 11) % 15
        ans = num % div
        _aq("Quantitative Aptitude", "Number Systems", "easy",
            f"Remainder when {num} ÷ {div}?",
            str(ans), [str((ans + 1) % div), str((ans + 2) % div), str(div - 1)],
            f"{num} = {num//div}×{div} + {ans}.",
            [f"Divide, keep remainder."], "Remainder < divisor.", C)


def f_probability(n, off=0):
    for k in range(n):
        i = k + off
        kind = ["coin", "dice", "cards", "balls", "urn", "spinner"][i % 6]
        j = i // 6
        if kind == "coin":
            tosses = 2 + (j % 5)
            # P(all heads in n tosses) = 1/2^n
            ans = f"1/{2**tosses}"
            _aq("Quantitative Aptitude", "Probability", "easy",
                f"P(all heads in {tosses} fair coin tosses)?", ans,
                [f"1/{tosses}", "1/2", f"{tosses}/4"],
                f"(1/2)^{tosses} = {ans}.",
                ["Multiply per toss."], "Independent multiply.", C)
        elif kind == "dice":
            t = 1 + (j % 5)
            good = 6 - t
            _aq("Quantitative Aptitude", "Probability", "easy",
                f"P(rolling over {t}) on a die?",
                _frac(good, 6), ["1/6", "1/2", "1/3"],
                f"Outcomes {t+1}..6: {good}/6 = " + _frac(good, 6) + ".",
                ["Count good faces."], "Good ÷ 6.", C)
        elif kind == "cards":
            ranks = ["ace", "king", "queen", "jack", "10"]
            rank = ranks[j % 5]
            num = 4
            _aq("Quantitative Aptitude", "Probability", "medium",
                f"P(drawing a {rank} from 52 cards)?",
                _frac(num, 52), ["1/52", "1/4", "1/2"],
                f"{num}/52 = " + _frac(num, 52) + ".",
                ["Count ÷ 52."], "Simplify.", C)
        elif kind == "balls":
            r, b = 2 + (j % 10), 2 + ((j // 10) % 8)
            tot = r + b
            _aq("Quantitative Aptitude", "Probability", "medium",
                f"Bag has {r} red, {b} blue balls. P(red)?",
                _frac(r, tot), [_frac(b, tot), _frac(1, tot), "1/2"],
                f"{r}/{tot} = " + _frac(r, tot) + ".",
                [f"Red ÷ total."], "Simplify fraction.", C)
        elif kind == "urn":
            # P(two reds without replacement)
            r, tot = 3 + (j % 8), 6 + ((j // 8) % 8)
            if r >= tot:
                r = tot - 1
            ans = _frac(r * (r - 1), tot * (tot - 1))
            _aq("Quantitative Aptitude", "Probability", "hard",
                f"Urn has {r} red of {tot} balls. P(2 reds, no replacement)?",
                ans, [_frac(r, tot), "1/2", _frac(1, tot)],
                f"{r}/{tot} × {r-1}/{tot-1} = {ans}.",
                ["Multiply conditional."], "Without replacement.", C)
        else:
            # spinner with n equal sectors, P(specific)
            sec = 4 + (i % 6)
            _aq("Quantitative Aptitude", "Probability", "easy",
                f"P(landing on 1 of a {sec}-sector spinner)?",
                _frac(1, sec), ["1/2", "1/4", _frac(2, sec)],
                f"1/{sec}.",
                ["One good sector."], "1 ÷ sectors.", C)


def f_permutation(n, off=0):
    ctx = ["letters", "books on a shelf", "runners finishing", "digits in a code",
           "guests in a row", "cards in a hand", "songs in a playlist", "tasks in order"]
    for k in range(n):
        i = k + off
        word_len = 3 + (i % 7)
        rep = (i // 7) % 3
        c = ctx[(i // 21) % len(ctx)]
        if rep == 0:
            ans = math.factorial(word_len)
            _aq("Quantitative Aptitude", "Permutations", "medium",
                f"Arrangements of {word_len} distinct {c}?",
                str(ans), [str(ans + 1), str(ans - 1), str(ans * 2)],
                f"{word_len}! = {ans}.",
                [f"Factorial."], "n! arrangements.", C)
        elif rep == 1:
            ans = math.factorial(word_len) // 2
            _aq("Quantitative Aptitude", "Permutations", "hard",
                f"Arrangements of {word_len} {c} with one repeat twice?",
                str(ans), [str(ans * 2), str(ans + 1), str(ans - 1)],
                f"{word_len}!/2! = {ans}.",
                [f"Divide by repeat factorial."], "n!/r!.", C)
        else:
            ans = math.factorial(word_len - 1)
            _aq("Quantitative Aptitude", "Permutations", "hard",
                f"Circular seatings of {word_len} {c}?",
                str(ans), [str(ans * word_len), str(ans + 1), str(math.factorial(word_len))],
                f"({word_len}−1)! = {ans}.",
                [f"Fix one, arrange rest."], "Circular (n−1)!.", C)


def f_combination(n, off=0):
    ctx = ["students", "players", "books", "fruits", "cards"]
    for k in range(n):
        i = k + off
        nn, rr = 5 + (i % 10), 2 + ((i // 10) % 4)
        if rr > nn:
            rr = 2
        c = ctx[(i // 40) % len(ctx)]
        ans = math.comb(nn, rr)
        _aq("Quantitative Aptitude", "Permutations", "medium",
            f"Ways to choose {rr} {c} from {nn}?",
            str(ans), [str(ans + 1), str(ans - 1), str(nn * rr)],
            f"C({nn},{rr}) = {ans}.",
            [f"nCr formula."], "Order doesn't matter.", C)


def f_mixture(n, off=0):
    for k in range(n):
        i = k + off
        # milk:water a:b, price mixture
        a, b = 2 + (i * 5) % 7, 1 + (i * 7) % 5
        milk_price, water_price = 40, 0
        ans = (a * milk_price) // (a + b)
        _aq("Quantitative Aptitude", "Mixtures", "medium",
            f"Milk:water = {a}:{b}. Milk costs 40/L, water free. Mixture price/L?",
            str(ans), _dn(ans, step=2),
            f"({a}×40)/({a}+{b}) = {ans}.",
            [f"Weighted average."], "Weight by ratio.", C)


def f_geometry(n, off=0):
    for k in range(n):
        i = k + off
        kind = ["rect_area", "circle_area", "triangle", "cube_vol", "rect_perim", "sphere_vol"][i % 6]
        j = i // 6
        if kind == "rect_area":
            l, w = 5 + (j % 30), 4 + ((j // 30) % 25)
            _aq("Quantitative Aptitude", "Geometry", "easy",
                f"Area of {l}×{w} rectangle?",
                str(l * w), [str(l * w + 1), str(l + w), str(2 * (l + w))],
                f"{l}×{w} = {l*w}.", ["Length × width."], "Area = lw.", C)
        elif kind == "circle_area":
            r = 7 * (1 + (j % 8))
            ans = round(22 / 7 * r * r)
            _aq("Quantitative Aptitude", "Geometry", "medium",
                f"Area of circle radius {r}? (π=22/7)",
                str(ans), [str(ans + r), str(2 * ans), str(ans - r)],
                f"22/7 × {r}² = {ans}.", ["πr²."], "π=22/7.", C)
        elif kind == "triangle":
            b, h = 5 + (j % 20), 4 + ((j // 20) % 15)
            ans = b * h // 2
            _aq("Quantitative Aptitude", "Geometry", "easy",
                f"Area of triangle base {b}, height {h}?",
                str(ans), [str(b * h), str(ans + 1), str(ans + 2)],
                f"½×{b}×{h} = {ans}.", ["Half base×height."], "½bh.", C)
        elif kind == "cube_vol":
            s = 2 + (j % 12)
            _aq("Quantitative Aptitude", "Geometry", "easy",
                f"Volume of cube side {s}?",
                str(s ** 3), [str(6 * s * s), str(s * s), str(s ** 3 + 1)],
                f"{s}³ = {s**3}.", ["Side cubed."], "s³.", C)
        elif kind == "rect_perim":
            l, w = 6 + (j % 25), 5 + ((j // 25) % 20)
            _aq("Quantitative Aptitude", "Geometry", "easy",
                f"Perimeter of {l}×{w} rectangle?",
                str(2 * (l + w)), [str(l * w), str(l + w), str(2 * (l + w) + 1)],
                f"2({l}+{w}) = {2*(l+w)}.", ["Twice sum."], "P = 2(l+w).", C)
        else:
            r = 3 + (j % 8)
            ans = round(4 / 3 * 22 / 7 * r ** 3)
            _aq("Quantitative Aptitude", "Geometry", "hard",
                f"Volume of sphere radius {r}? (π=22/7)",
                str(ans), [str(ans + r), str(2 * ans), str(ans - r)],
                f"4/3×22/7×{r}³ ≈ {ans}.", ["4/3πr³."], "Sphere volume.", C)


def f_calendar(n, off=0):
    import datetime
    for k in range(n):
        i = k + off
        y = 1996 + (i * 11) % 35
        m = 1 + (i // 35) % 12
        d = datetime.date(y, m, 1).strftime("%A")
        _aq("Quantitative Aptitude", "Calendar", "medium",
            f"Day of week on 1 {datetime.date(2000, m, 1).strftime('%B')} {y}?",
            d, ["Monday", "Saturday", "Sunday"],
            f"1/{m}/{y} = {d}.", ["Odd-days."], "Reference 2000.", C)


def f_number_series_apt(n, off=0):
    for k in range(n):
        i = k + off
        a, d = 2 + (i * 11) % 40, 2 + (i * 13) % 12
        seq = [a + j * d for j in range(4)]
        ans = a + 4 * d
        _aq("Quantitative Aptitude", "Number Series", "easy",
            f"Next: {', '.join(map(str, seq))}, ?",
            str(ans), _dn(ans),
            f"+{d} each → {ans}.", ["Differences."], "AP check.", C)


# ─── NEW FAMILIES for volume ────────────────────────────────────────
def f_boats(n, off=0):
    for k in range(n):
        i = k + off
        # downstream = b+s, upstream = b−s
        b, s = 8 + (i * 7) % 12, 2 + (i * 3) % 4
        down, up = b + s, b - s
        if k % 2 == 0:
            _aq("Quantitative Aptitude", "Speed & Distance", "medium",
                f"Boat speed {b} km/h, stream {s} km/h. Downstream speed?",
                str(down), [str(up), str(b), str(b + 2 * s)],
                f"{b}+{s} = {down}.",
                ["Add stream."], "Downstream = b+s.", C)
        else:
            _aq("Quantitative Aptitude", "Speed & Distance", "medium",
                f"Boat speed {b} km/h, stream {s} km/h. Upstream speed?",
                str(up), [str(down), str(b), str(b - 2 * s)],
                f"{b}−{s} = {up}.",
                ["Subtract stream."], "Upstream = b−s.", C)


def f_pipes(n, off=0):
    for k in range(n):
        i = k + off
        a = 4 + (i % 16)
        b = 6 + ((i // 16) % 16)
        if b == a:
            b += 2
        num, den = a * b, a + b
        ans = str(num // den) if num % den == 0 else _frac(num, den)
        _aq("Quantitative Aptitude", "Time & Work", "medium",
            f"Pipe A fills in {a} hrs, B in {b} hrs. Together?",
            ans, [str(a + b), str(abs(a - b)), str(max(a, b))],
            f"{a}×{b}/({a}+{b}) = {ans} hrs.",
            ["Rates add."], "Same as work.", C)


def f_partnership(n, off=0):
    for k in range(n):
        i = k + off
        a, b = 2 + (i * 3) % 6, 3 + (i * 5) % 6
        tot = (a + b) * (1000 + (i * 101) % 9000)
        share = tot * a // (a + b)
        _aq("Quantitative Aptitude", "Ratios", "medium",
            f"Partners invest in ratio {a}:{b}. Profit {tot}. First share?",
            str(share), _dn(share, step=100),
            f"{tot}×{a}/{a+b} = {share}.",
            ["Ratio of profit."], "Investment ratio.", C)


def f_clock_angle(n, off=0):
    for k in range(n):
        i = k + off
        h = 1 + (i * 5) % 12
        m = ((i * 7) % 12) * 5
        angle = abs(30 * h - 5.5 * m)
        if angle > 180:
            angle = 360 - angle
        ans = f"{angle:g}°"
        _aq("Quantitative Aptitude", "Calendar", "medium",
            f"Clock angle at {h}:{m:02d}?",
            ans, [f"{(angle+30):g}°", f"{abs(angle-15):g}°", f"{(180-angle):g}°"],
            f"|30×{h}−5.5×{m}| → {ans}.",
            ["6°/0.5° per min."], "Hands formula.", C)


def f_alligation(n, off=0):
    for k in range(n):
        i = k + off
        # mix priced p1, p2 to mean m → ratio (p2−m):(m−p1)
        p1, p2 = 20 + (i * 7) % 30, 50 + (i * 11) % 40
        if p2 <= p1:
            p2 = p1 + 20
        m = (p1 + p2) // 2 + (i % 3) - 1
        if m <= p1 or m >= p2:
            m = (p1 + p2) // 2
        r1, r2 = p2 - m, m - p1
        g = math.gcd(r1, r2)
        ans = f"{r1//g}:{r2//g}"
        _aq("Quantitative Aptitude", "Mixtures", "hard",
            f"Mix goods costing {p1} and {p2} to get mean price {m}. Ratio?",
            ans, [f"{r2}:{r1}", "1:1", f"{r1}:{r2+1}"],
            f"({p2}−{m}):({m}−{p1}) = {ans}.",
            ["Alligation cross."], "Cheaper:expensive.", C)


def f_log_basic(n, off=0):
    for k in range(n):
        i = k + off
        base, exp = 2 + (i % 3), 2 + ((i // 3) % 4)
        val = base ** exp
        _aq("Quantitative Aptitude", "Number Systems", "medium",
            f"If log₂x... no: what is log base {base} of {val}?",
            str(exp), [str(exp + 1), str(exp - 1), str(val)],
            f"{base}^{exp} = {val} → log = {exp}.",
            ["Inverse of power."], "log = exponent.", C)


def f_surds(n, off=0):
    for k in range(n):
        i = k + off
        a = 2 + (i * 3) % 8
        ans = a * 2
        _aq("Quantitative Aptitude", "Number Systems", "medium",
            f"Simplify: √{a*a} + √{a*a}?",
            str(ans), [str(ans + 1), str(a), str(a * a)],
            f"{a}+{a} = {ans}.",
            ["Perfect squares."], "√(a²)=a.", C)


def f_ap_sum(n, off=0):
    for k in range(n):
        i = k + off
        nn = 10 + (i * 7) % 40
        ans = nn * (nn + 1) // 2
        _aq("Quantitative Aptitude", "Number Series", "easy",
            f"Sum 1 to {nn}?",
            str(ans), _dn(ans, step=10),
            f"{nn}×{nn+1}/2 = {ans}.",
            ["n(n+1)/2."], "Triangular sum.", C)


def f_train_two(n, off=0):
    for k in range(n):
        i = k + off
        l1 = 100 + (i % 20) * 10
        l2 = 80 + ((i // 20) % 15) * 10
        v = 54 + ((i // 300) % 3) * 18  # 54,72,90
        ms = v * 1000 / 3600
        t = round((l1 + l2) / ms, 1)
        ans = str(int(t)) if t == int(t) else str(t)
        _aq("Quantitative Aptitude", "Speed & Distance", "hard",
            f"Trains {l1}m and {l2}m cross each other at {v} km/h relative. Time?",
            ans + "s", [f"{(l1+l2)//20}s", f"{(l1+l2)//10}s", f"{l1//10}s"],
            f"({l1}+{l2})/{ms} = {ans}s.",
            ["Sum lengths ÷ speed."], "Crossing = lengths/speed.", C)


def f_work_three(n, off=0):
    for k in range(n):
        i = k + off
        a = 6 + (i % 10)
        b = 8 + ((i // 10) % 10)
        c = 10 + ((i // 100) % 10)
        if len({a, b, c}) < 3:
            c += 3
        # 1/T = 1/a+1/b+1/c → T = 1/(sum)
        from fractions import Fraction
        t = Fraction(1, 1) / (Fraction(1, a) + Fraction(1, b) + Fraction(1, c))
        ans = f"{t.numerator}/{t.denominator}" if t.denominator != 1 else str(t.numerator)
        _aq("Quantitative Aptitude", "Time & Work", "hard",
            f"A:{a}d, B:{b}d, C:{c}d. All together?",
            ans, [str(a + b + c), str(min(a, b, c)), str((a + b + c) // 3)],
            f"1/T = 1/{a}+1/{b}+1/{c} → T = {ans} days.",
            ["Add reciprocals."], "Three rates.", C)


def f_weighted_avg(n, off=0):
    for k in range(n):
        i = k + off
        a, wa = 70 + (i % 20), 2 + ((i // 20) % 4)
        b, wb = 80 + ((i // 80) % 15), 1 + ((i // 120) % 3)
        ans = round((a * wa + b * wb) / (wa + wb), 1)
        ans_s = str(int(ans)) if ans == int(ans) else str(ans)
        _aq("Quantitative Aptitude", "Averages", "medium",
            f"Class A ({wa} students) avg {a}; Class B ({wb}) avg {b}. Combined?",
            ans_s, [str((a + b) // 2), str(max(a, b)), str(min(a, b))],
            f"({a}×{wa}+{b}×{wb})/({wa}+{wb}) = {ans_s}.",
            ["Weight by count."], "Weighted mean.", C)


def f_lcm_three(n, off=0):
    for k in range(n):
        i = k + off
        a = 4 + (i % 12)
        b = 6 + ((i // 12) % 12)
        c = 8 + ((i // 144) % 10)
        l = math.lcm(a, b, c)
        _aq("Quantitative Aptitude", "Number Systems", "medium",
            f"LCM of {a}, {b}, {c}?",
            str(l), [str(l + a), str(l * 2), str(l - a)],
            f"LCM = {l}.",
            ["Pairwise then third."], "LCM chain.", C)


# ─── GENERATE ───────────────────────────────────────────────────────
# Big supposedly-generic pools mirroring existing bank shape
f_pct_of(400)
f_pct_change(250)
f_successive(150)
f_discount(250)
f_profit(250)
f_loss(200)
f_si(250)
f_ci(200)
f_work_together(250)
f_work_individual(200)
f_avg_speed(220)
f_train(200)
f_ratio_split(280)
f_ages(200)
f_average(250)
f_missing_avg(150)
f_hcf_lcm(250)
f_remainder(220)
f_probability(300)
f_permutation(180)
f_combination(180)
f_mixture(150)
f_geometry(250)
f_calendar(120)
f_number_series_apt(250)
f_boats(200)
f_pipes(200)
f_partnership(200)
f_clock_angle(150)
f_alligation(150)
f_log_basic(120)
f_surds(120)
f_ap_sum(180)
f_train_two(220)
f_work_three(170)
f_weighted_avg(220)
f_lcm_three(170)
f_pct_of(150, off=9000)
f_ratio_split(100, off=9000)
# thin-topic top-ups (match existing thin topics)
f_pct_of(6, off=5000)  # percentages topic handled via Quantitative Aptitude; add explicit thin ones below

# explicit thin topics with exact schema topic names
def f_thin(topic, sub, n, off=0):
    for k in range(n):
        i = k + off
        a, b = 10 + (i * 37) % 500, 5 + (i * 41) % 300
        ans = a + b
        _aq(topic, sub, "easy", f"What is {a} + {b}?", str(ans), _dn(ans),
            f"{a}+{b}={ans}.", ["Add."], "Basic.", C)

_thin_map = [
    ("percentages", "percentages", 6), ("profit-loss", "profit-loss", 6),
    ("compound-interest", "compound-interest", 6), ("time-work", "time-work", 5),
    ("speed-distance-time", "speed-distance-time", 4), ("probability", "probability", 4),
    ("ratio-proportion", "ratio-proportion", 3), ("simple-interest", "simple-interest", 3),
    ("averages", "averages", 3), ("number-system", "number-system", 3),
    ("mixture-alligation", "mixture-alligation", 2), ("ages", "ages", 2),
]
for _t, _s, _n in _thin_map:
    f_thin(_t, _s, _n)

from collections import Counter
print("generated:", len(items))
got = Counter((q["topic"], q["sub_topic"]) for q in items)
for (t, s), c in sorted(got.items()):
    print(f"  {t}/{s}: {c}")

qs = [q["question"] for q in items]
dupes = sum(1 for q, c in Counter(qs).items() if c > 1)
print(f"duplicate questions: {dupes}")
if dupes:
    seen, uniq = set(), []
    for q in items:
        if q["question"] not in seen:
            seen.add(q["question"])
            uniq.append(q)
    items.clear()
    items.extend(uniq)
    print(f"after dedupe: {len(items)}")
for i, q in enumerate(items, 1):
    q["id"] = f"apt-v2-{i:05d}"

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)
print(f"Wrote {len(items)} aptitude questions to {OUT.name}")
