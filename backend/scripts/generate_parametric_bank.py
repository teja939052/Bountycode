"""Deterministic parametric practice bank (zero LLM, zero network, seeded RNG).

Every item's answer is COMPUTED by an exact oracle (integer arithmetic,
fractions via gcd, executed Python for code drills) — never guessed. Output:
- app/data/parametric_practice_bank.json (AUTOMATED_CHECKED candidates)
- app/data/parametric_bank_report.json (family counts)

Not loaded by student serving. Promotion to TRUSTED needs human sampling
per Content Trust Pipeline. No company tags (provenance pattern-relevant).
"""
import json
import math
import random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "app" / "data" / "parametric_practice_bank.json"
REPORT = BASE / "app" / "data" / "parametric_bank_report.json"
RNG = random.Random(20260912)

_items: list = []
_seq = 0


def _mcq(family, topic, sub, difficulty, question, answer, distractors,
         explanation, steps, hint, qtype="aptitude"):
    global _seq
    _seq += 1
    opts = [answer] + [d for d in distractors if d != answer]
    # unique, exactly 4
    seen, uniq = set(), []
    for o in opts:
        if o not in seen:
            seen.add(o)
            uniq.append(o)
    need = 2
    while len(uniq) < 4:
        cand = f"{answer} ({need})" if isinstance(answer, str) else str(answer) + f".{need}"
        if cand not in seen:
            seen.add(cand)
            uniq.append(cand)
        need += 1
    uniq = uniq[:4]
    # deterministic shuffle
    order = sorted(range(4), key=lambda i: RNG.random())
    options = [uniq[i] for i in order]
    correct_index = options.index(answer)
    return {
        "id": f"parametric-{_seq:06d}",
        "type": qtype,
        "topic": topic,
        "sub_topic": sub,
        "difficulty": difficulty,
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "correct_answer": answer,
        "solution": {},
        "testcases": [],
        "hidden_testcases": [],
        "hints": [hint],
        "explanation": explanation,
        "reasoning_steps": steps,
        "companies": [],
        "role": "",
        "provenance": f"parametric generator v1 ({family}), deterministic oracle",
        "source_bank": "parametric_practice_bank.json",
        "trust_status": "automated_checked",
        "stage": "practice",
    }


def _int_opts(ans: int, spread=(1, 2, 3, 5, 10)):
    c = [ans + d for d in spread] + [ans - d for d in spread]
    c = [x for x in c if x != ans]
    RNG.shuffle(c)
    out = []
    for x in c:
        if x not in out:
            out.append(str(x))
        if len(out) == 3:
            break
    return out


def gen_pct_of(n):
    for _ in range(n):
        p = RNG.choice([5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75])
        base = RNG.choice([100, 200, 240, 300, 400, 500, 600, 800, 1000])
        ans = base * p // 100
        q = f"What is {p}% of {base}?"
        _items.append(_mcq("pct_of", "Aptitude", "Percentages", "easy", q, str(ans),
                           _int_opts(ans), f"{p}% of {base} = ({p}/100) × {base} = {ans}.",
                           [f"Convert {p}% to {p}/100.", f"Multiply by {base}."],
                           "Percent means per hundred."))


def gen_pct_change(n):
    for _ in range(n):
        old = RNG.choice([100, 120, 200, 240, 400, 500])
        pct = RNG.choice([10, 20, 25, 50])
        new = old * (100 + pct) // 100
        q = f"A price rises from {old} to {new}. What is the percentage increase?"
        _items.append(_mcq("pct_change", "Aptitude", "Percentages", "easy", q, f"{pct}%",
                           [f"{pct+5}%", f"{pct-5}%", f"{pct+10}%"],
                           f"Change = {new-old}; ({new-old}/{old}) × 100 = {pct}%.",
                           ["Find the change.", "Divide by original, × 100."],
                           "Percentage change uses the original value."))


def gen_profit_loss(n):
    for _ in range(n):
        cost = RNG.choice([200, 300, 400, 500, 600, 800, 1000])
        pct = RNG.choice([10, 20, 25])
        sp = cost * (100 + pct) // 100
        q = f"A shopkeeper buys an item for {cost} and wants a {pct}% profit. What should the selling price be?"
        _items.append(_mcq("profit_loss", "Aptitude", "Profit & Loss", "easy", q, str(sp),
                           _int_opts(sp), f"SP = {cost} × (1 + {pct}/100) = {sp}.",
                           ["Profit = cost × rate.", "Add to cost."],
                           "Selling price = cost + profit."))


def gen_ratio(n):
    for _ in range(n):
        a, b = RNG.choice([(1, 2), (2, 3), (3, 4), (1, 3), (3, 5)])
        total = (a + b) * RNG.choice([10, 20, 25, 50])
        sa, sb = total * a // (a + b), total * b // (a + b)
        q = f"Divide {total} in the ratio {a}:{b}. What is the larger share?"
        ans = max(sa, sb)
        _items.append(_mcq("ratio", "Aptitude", "Ratios", "easy", q, str(ans),
                           _int_opts(ans), f"Parts = {a+b}; shares = {sa} and {sb}; larger = {ans}.",
                           [f"Total parts = {a+b}.", "Multiply total by each part."],
                           "Split by total parts."))


def gen_average(n):
    for _ in range(n):
        k = RNG.choice([3, 4, 5])
        start = RNG.choice([10, 12, 15, 20])
        step = RNG.choice([2, 3, 4, 5])
        nums = [start + i * step for i in range(k)]
        ans = sum(nums) // k
        q = f"What is the average of {', '.join(map(str, nums))}?"
        _items.append(_mcq("average", "Aptitude", "Averages", "easy", q, str(ans),
                           _int_opts(ans), f"Sum = {sum(nums)}; count = {k}; avg = {ans}.",
                           ["Add all numbers.", "Divide by count."],
                           "Average = sum ÷ count."))


def gen_std(n):
    for _ in range(n):
        d = RNG.choice([60, 80, 100, 120])
        t = RNG.choice([2, 3, 4, 5])
        dist = d * t
        q = f"A train travels at {d} km/h for {t} hours. How far does it travel?"
        _items.append(_mcq("std", "Aptitude", "Speed & Distance", "easy", q, str(dist),
                           _int_opts(dist), f"Distance = {d} × {t} = {dist} km.",
                           ["Use distance = speed × time."],
                           "Distance = speed × time."))


def gen_time_work(n):
    for _ in range(n):
        a = RNG.choice([4, 5, 6, 8, 10])
        b = RNG.choice([4, 5, 6, 8, 10])
        # together: 1/(1/a+1/b) — pick pairs giving integer days
        days = (a * b) / (a + b)
        if abs(days - round(days)) > 1e-9:
            # fall back to doubling framing with integer answer
            q = f"A does a job in {a} days, B in {a} days. Together, how many jobs in {a} days?"
            ans = 2
            _items.append(_mcq("time_work", "Aptitude", "Time & Work", "easy", q, str(ans),
                               _int_opts(ans), "Each does 1 job; together 2.",
                               ["Add individual outputs."], "Rates add up."))
            continue
        ans = int(round(days))
        q = f"A finishes a job in {a} days, B in {b} days. Working together, in how many days do they finish one job?"
        _items.append(_mcq("time_work", "Aptitude", "Time & Work", "medium", q, str(ans),
                           _int_opts(ans), f"Combined rate = 1/{a}+1/{b} = {a+b}/{a*b}; days = {ans}.",
                           ["Add rates, invert."], "Add rates, then invert."))


def gen_si(n):
    for _ in range(n):
        p = RNG.choice([1000, 2000, 5000])
        r = RNG.choice([5, 8, 10])
        t = RNG.choice([2, 3, 4])
        si = p * r * t // 100
        q = f"Simple interest on {p} at {r}% per annum for {t} years is?"
        _items.append(_mcq("si", "Aptitude", "Interest", "easy", q, str(si),
                           _int_opts(si), f"SI = {p}×{r}×{t}/100 = {si}.",
                           ["Apply P×R×T/100."], "SI = PRT/100."))


def gen_ci(n):
    for _ in range(n):
        p = RNG.choice([1000, 2000, 5000])
        amt = p * 121 // 100
        q = f"{p} invested at 10% per annum compounded annually for 2 years becomes?"
        _items.append(_mcq("ci", "Aptitude", "Interest", "medium", q, str(amt),
                           _int_opts(amt), f"Amount = {p} × 1.1² = {amt}.",
                           ["Square 1.1.", "Multiply by principal."],
                           "Compound: multiply each year."))


def gen_npr(n):
    for _ in range(n):
        nn, rr = RNG.choice([(5, 2), (6, 2), (5, 3), (7, 2)])
        ans = math.perm(nn, rr)
        q = f"In how many ways can {rr} prizes be given to {nn} people (no sharing)?"
        _items.append(_mcq("npr", "Aptitude", "Permutations", "medium", q, str(ans),
                           _int_opts(ans), f"P({nn},{rr}) = {nn}!/{nn-rr}! = {ans}.",
                           ["Order matters.", "Use nPr."],
                           "Ordered selection: nPr."))


def gen_prob(n):
    for _ in range(n):
        kind = RNG.choice(["die_even", "coin", "bag"])
        if kind == "die_even":
            q = "A fair die is rolled. What is P(even number)?"
            ans = "1/2"
            d = ["1/3", "2/3", "1/6"]
            exp = "Evens {2,4,6} = 3 of 6 = 1/2."
        elif kind == "coin":
            q = "Two fair coins are tossed. What is P(both heads)?"
            ans = "1/4"
            d = ["1/2", "3/4", "1/3"]
            exp = "HH out of {HH,HT,TH,TT} = 1/4."
        else:
            red = RNG.choice([2, 3, 4])
            tot = red + RNG.choice([2, 3, 4])
            g = math.gcd(red, tot)
            ans = f"{red//g}/{tot//g}"
            q = f"A bag has {red} red and {tot-red} blue balls. P(red) in one draw?"
            d = [f"{red//g+1}/{tot//g}", f"{red//g}/{tot//g+1}", "1/2"]
            exp = f"Favourable {red}, total {tot} = {ans}."
        _items.append(_mcq("prob", "Aptitude", "Probability", "medium", q, ans, d, exp,
                           ["Count favourable.", "Divide by total, simplify."],
                           "Probability = favourable ÷ total."))


def gen_num_series(n):
    for _ in range(n):
        kind = RNG.choice(["ap", "gp", "sq"])
        if kind == "ap":
            a = RNG.randint(2, 20)
            d = RNG.choice([2, 3, 4, 5, 6])
            terms = [a + i * d for i in range(5)]
            ans = terms[-1] + d
            q = f"What comes next? {', '.join(map(str, terms))}, ?"
            exp = f"AP with difference {d}; next = {ans}."
        elif kind == "gp":
            a = RNG.choice([2, 3])
            r = 2
            terms = [a * (r ** i) for i in range(5)]
            ans = terms[-1] * r
            q = f"What comes next? {', '.join(map(str, terms))}, ?"
            exp = f"GP with ratio {r}; next = {ans}."
        else:
            s = RNG.randint(3, 8)
            terms = [(s + i) ** 2 for i in range(4)]
            ans = (s + 4) ** 2
            q = f"What comes next? {', '.join(map(str, terms))}, ?"
            exp = f"Squares of {s}..{s+3}; next = {s+4}² = {ans}."
        _items.append(_mcq("num_series", "Aptitude", "Number Series", "easy", q, str(ans),
                           _int_opts(ans), exp, ["Find the rule.", "Apply once more."],
                           "Look at differences/ratios."))


def gen_odd_one(n):
    for _ in range(n):
        base = RNG.choice([10, 12, 14, 20])
        evens = [base + 2 * i for i in range(3)]
        odd = base + 1 + 2 * RNG.randint(0, 4)
        while odd in evens:
            odd += 2
        opts = evens + [odd]
        RNG.shuffle(opts)
        ans = str(odd)
        q = f"Find the odd one out: {', '.join(map(str, opts))}."
        _items.append(_mcq("odd_one", "Logical", "Classification", "easy", q, ans,
                           [str(e) for e in evens[:3]], f"{odd} is odd; the rest are even.",
                           ["Check even/odd.", "Three share it."],
                           "Three share a property; one doesn't."))


def gen_letter_series(n):
    for _ in range(n):
        start = RNG.randint(0, 20)
        step = RNG.choice([1, 2, 3])
        terms = [chr(65 + ((start + i * step) % 26)) for i in range(4)]
        ans = chr(65 + ((start + 4 * step) % 26))
        q = f"What comes next? {', '.join(terms)}, ?"
        _items.append(_mcq("letter_series", "Logical", "Letter Series", "easy", q, ans,
                           [chr(65 + ((start + 4 * step + d) % 26)) for d in (1, 2, 3)],
                           f"Step +{step} through the alphabet; next = {ans}.",
                           ["Measure gaps.", "Step once more."],
                           "Convert letters to positions."))


def gen_direction(n):
    for _ in range(n):
        x = RNG.choice([3, 4, 5, 6])
        y = RNG.choice([2, 4, 5])
        q = f"Starting at origin, walk {x} km East then {y} km North. How far (straight line) from start?"
        ans = round(math.hypot(x, y), 2)
        ans_s = str(int(ans)) if ans == int(ans) else f"{ans:.2f}"
        # pick integer triples mostly
        if (x, y) not in [(3, 4), (6, 8), (5, 12)]:
            x, y = 3, 4
            ans_s = "5"
            q = "Starting at origin, walk 3 km East then 4 km North. How far (straight line) from start?"
        _items.append(_mcq("direction", "Logical", "Direction Sense", "easy", q, ans_s,
                           _int_opts(int(float(ans_s))), f"Right triangle: √({x}²+{y}²) = {ans_s}.",
                           ["Draw East then North.", "Use Pythagoras."],
                           "East+Noth makes a right angle."))


def gen_mixed_series(n):
    for _ in range(n):
        a = RNG.randint(1, 9)
        terms = [a]
        for i in range(4):
            terms.append(terms[-1] * 2 + 1)
        ans = terms[-1] * 2 + 1
        q = f"What comes next? {', '.join(map(str, terms))}, ?"
        _items.append(_mcq("mixed_series", "Logical", "Number Series", "medium", q, str(ans),
                           _int_opts(ans), f"Rule ×2+1; next = {ans}.",
                           ["Relate consecutive terms.", "Apply again."],
                           "Each term builds from the last."))


def gen_bin_dec(n):
    for _ in range(n):
        v = RNG.randint(5, 255)
        b = bin(v)[2:]
        q = f"What is binary {b} in decimal?"
        _items.append(_mcq("bin_dec", "CS Fundamentals", "Number Systems", "easy", q, str(v),
                           _int_opts(v), f"Positional powers of 2 sum to {v}.",
                           ["Weight each bit.", "Add."],
                           "Each bit is a power of 2."))


def gen_hex_dec(n):
    for _ in range(n):
        v = RNG.choice([10, 15, 16, 31, 64, 100, 255])
        h = hex(v)[2:].upper()
        q = f"What is hex {h} in decimal?"
        _items.append(_mcq("hex_dec", "CS Fundamentals", "Number Systems", "easy", q, str(v),
                           _int_opts(v), f"Hex {h} = {v} in decimal.",
                           ["16s place then 1s."], "Hex is base 16."))


def gen_bitwise(n):
    for _ in range(n):
        a = RNG.randint(1, 31)
        b = RNG.randint(1, 31)
        op = RNG.choice(["&", "|", "^"])
        ans = eval(f"{a}{op}{b}")
        q = f"What is {a} {op} {b} in Python (integers, bitwise)?"
        _items.append(_mcq("bitwise", "CS Fundamentals", "Bit Manipulation", "easy", q, str(ans),
                           _int_opts(ans), f"Bitwise {a} {op} {b} = {ans}.",
                           ["Write both in binary.", "Combine bit by bit."],
                           "Compare binary columns."))


def gen_bigo(n):
    shapes = [
        ("A single loop runs n times doing O(1) work.", "O(n)"),
        ("Two nested loops each run n times.", "O(n²)"),
        ("Input halves each step (binary search).", "O(log n)"),
        ("One statement, no loops.", "O(1)"),
        ("Loop n times with a log-n inner step.", "O(n log n)"),
    ]
    for _ in range(n):
        desc, ans = RNG.choice(shapes)
        q = f"What is the time complexity of this? {desc}"
        d = [c for _, c in shapes if c != ans][:3]
        _items.append(_mcq("bigo", "CS Fundamentals", "Complexities", "easy", q, ans, d,
                           f"{desc} → {ans}.", ["Count loop nesting.", "Drop constants."],
                           "Count nested loops."))


def gen_code_output(n):
    global _seq
    for _ in range(n):
        a = RNG.randint(1, 20)
        b = RNG.randint(1, 20)
        op = RNG.choice(["add", "mul", "mod"])
        if op == "add":
            code = f"def solve(a, b):\n    return a * 2 + b"
            exp_val = a * 2 + b
            inp = {"a": a, "b": b}
        elif op == "mul":
            code = f"def solve(a, b):\n    return a * b - a"
            exp_val = a * b - a
            inp = {"a": a, "b": b}
        else:
            b = RNG.randint(2, 9)
            code = f"def solve(a, b):\n    return (a * 3 + b) % 7"
            exp_val = (a * 3 + b) % 7
            inp = {"a": a, "b": b}
        # independent oracle: execute
        ns: dict = {}
        exec(code, ns)
        got = ns["solve"](**inp)
        assert got == exp_val
        _seq += 1
        ans = str(exp_val)
        distract = []
        for d in (1, 2, -1, 10):
            c = str(exp_val + d)
            if c != ans and c not in distract:
                distract.append(c)
        order = sorted(range(4), key=lambda i: RNG.random())
        base = [ans] + distract[:3]
        options = [base[i] for i in order]
        correct_index = options.index(ans)
        call = f"solve(a={a}, b={b})"
        _items.append({
            "id": f"parametric-{_seq:06d}",
            "type": "coding",
            "topic": "Python Basics",
            "sub_topic": "Output Prediction",
            "difficulty": "easy",
            "question": f"What does this print? {code} Print {call}.",
            "statement": f"Predict the output.\n{code}\nCall: {call}",
            "options": options,
            "correct_index": correct_index,
            "correct_answer": ans,
            "solution": {"code": code, "language": "python"},
            "testcases": [{"input": f"a={a}, b={b}", "expected": ans}],
            "hidden_testcases": [{"input": f"a={a+1}, b={b+2}",
                                  "expected": str(ns["solve"](a + 1, b + 2))}],
            "hints": ["Substitute the values line by line."],
            "explanation": f"Substituting a={a}, b={b} gives {ans}.",
            "reasoning_steps": ["Read the expression.", "Substitute.", "Compute."],
            "companies": [],
            "role": "",
            "constraints": "",
            "examples": [],
            "provenance": "parametric generator v1 (code_output), executed oracle",
            "source_bank": "parametric_practice_bank.json",
            "trust_status": "automated_checked",
            "stage": "practice",
        })


def main():
    gen_pct_of(500)
    gen_pct_change(300)
    gen_profit_loss(500)
    gen_ratio(400)
    gen_average(300)
    gen_std(400)
    gen_time_work(400)
    gen_si(300)
    gen_ci(200)
    gen_npr(200)
    gen_prob(200)
    gen_num_series(500)
    gen_odd_one(300)
    gen_letter_series(200)
    gen_direction(200)
    gen_mixed_series(300)
    gen_bin_dec(300)
    gen_hex_dec(200)
    gen_bitwise(300)
    gen_bigo(200)
    gen_code_output(400)
    OUT.write_text(json.dumps(_items, indent=1), encoding="utf-8")
    fam: dict = {}
    for q in _items:
        prov = q.get("provenance", "")
        key = prov.split("(")[1].split(")")[0] if "(" in prov else "?"
        fam[key] = fam.get(key, 0) + 1
    REPORT.write_text(json.dumps({
        "total": len(_items),
        "families": fam,
        "trust": "automated_checked (needs human sampling before TRUSTED)",
        "note": "Deterministic oracles, seeded RNG. Not served by default.",
    }, indent=1), encoding="utf-8")
    print(f"PARAMETRIC_TOTAL {len(_items)}")


if __name__ == "__main__":
    main()
