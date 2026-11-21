"""Generate "what is the output?" code-tracing MCQs (pseudocode round).

Infosys (5 pseudocode questions) and Capgemini (pseudocode as the first
section) test this, and the bank had 0 such questions.

How the answer is trusted: the code shown to the student IS the code that is
executed, so the answer cannot disagree with the question. Wrong options are
the outputs of the same code with one realistic bug injected (off-by-one,
wrong operator, wrong bound), so each distractor is a mistake a student makes.
The code is written in Python syntax with only basic constructs (loops, ifs,
lists, strings, recursion) so it reads as language-neutral pseudocode.

Items are written as trust_status "unverified" into app/data/intake/ and are
NOT loaded by question_store. They go through the normal trust pipeline.

Usage: python scripts/gen_pseudocode_items.py [--per-template 5] [--seed 2026]
"""
import argparse
import contextlib
import io
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app", "data", "intake", "pseudocode_generated_v2.json")
COMPANIES = ["infosys", "capgemini", "tcs", "accenture"]
WORDS = ["education", "beautiful", "algorithm", "database", "sequence", "computer", "internet", "variable"]


def run_code(code):
    """Execute the displayed code and return what it prints (None on error)."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<item>", "exec"), {"__builtins__": {
                "range": range, "len": len, "print": print, "int": int, "str": str, "min": min, "max": max}})
    except Exception:
        return None
    out = buf.getvalue().strip()
    return out or None


# Each template: (name, difficulty, code_template(params), params_fn(rng), mutations[(old, new)])
def T(name, diff, code, params, muts):
    return {"name": name, "diff": diff, "code": code, "params": params, "muts": muts}


TEMPLATES = [
    T("conditional sum", "easy",
      "total = 0\nfor i in range(1, {n} + 1):\n    if i % {k} == 0:\n        total = total + i\nprint(total)",
      lambda r: {"n": r.randint(10, 30), "k": r.choice((2, 3, 4, 5, 7))},
      [("range(1, {n} + 1)", "range(1, {n})"), ("% {k} == 0", "% {k} == 1"), ("total + i", "total + 1")]),
    T("digit sum", "easy",
      "n = {n}\ns = 0\nwhile n > 0:\n    s = s + n % 10\n    n = n // 10\nprint(s)",
      lambda r: {"n": r.randint(1000, 99999)},
      [("n > 0", "n > 9"), ("s + n % 10", "s + n // 10"), ("s = 0", "s = 1")]),
    T("nested loop count", "medium",
      "count = 0\nfor i in range({a}):\n    for j in range(i, {b}):\n        count = count + 1\nprint(count)",
      lambda r: {"a": r.randint(3, 6), "b": r.randint(6, 9)},
      [("range(i, {b})", "range(i + 1, {b})"), ("range({a})", "range({a} + 1)"), ("count + 1", "count + 2")]),
    T("count vowels", "easy",
      "s = \"{word}\"\nc = 0\nfor ch in s:\n    if ch in \"aeiou\":\n        c = c + 1\nprint(c)",
      lambda r: {"word": r.choice(WORDS)},
      [("\"aeiou\"", "\"aeio\""), ("c + 1", "c + 2"), ("c = 0", "c = 1")]),
    T("reverse and slice", "medium",
      "s = \"{word}\"\nr = \"\"\nfor ch in s:\n    r = ch + r\nprint(r[:{k}])",
      lambda r: {"word": r.choice(WORDS), "k": r.randint(2, 4)},
      [("ch + r", "r + ch"), ("r[:{k}]", "r[{k}:]"), ("r[:{k}]", "r[:{k} + 1]")]),
    T("one bubble pass", "medium",
      "a = {lst}\nfor i in range(len(a) - 1):\n    if a[i] > a[i + 1]:\n        t = a[i]\n        a[i] = a[i + 1]\n        a[i + 1] = t\nprint(a)",
      lambda r: {"lst": r.sample(range(1, 20), 5)},
      [("a[i] > a[i + 1]", "a[i] < a[i + 1]"), ("range(len(a) - 1)", "range(len(a) - 2)"), ("a[i + 1] = t", "a[i + 1] = a[i]")]),
    T("recursion fibonacci", "medium",
      "def f(n):\n    if n <= 1:\n        return n\n    return f(n - 1) + f(n - 2)\nprint(f({n}))",
      lambda r: {"n": r.randint(5, 10)},
      [("n <= 1", "n <= 2"), ("f(n - 2)", "f(n - 3)"), ("return n", "return 1")]),
    T("continue and break", "hard",
      "x = 0\nfor i in range(1, {n}):\n    if i % {a} == 0:\n        continue\n    if i > {b}:\n        break\n    x = x + i\nprint(x)",
      lambda r: {"n": r.randint(15, 25), "a": r.choice((2, 3, 4)), "b": r.randint(8, 13)},
      [("continue", "break"), ("i > {b}", "i >= {b}"), ("range(1, {n})", "range(0, {n})")]),
    T("euclid gcd", "medium",
      "a = {a}\nb = {b}\nwhile b != 0:\n    t = a % b\n    a = b\n    b = t\nprint(a)",
      lambda r: (lambda g, p, q: {"a": g * p, "b": g * q})(r.choice((3, 4, 6, 7)), r.choice((5, 8, 9)), r.choice((2, 7, 11))),
      [("a % b", "b % a"), ("b != 0", "b > 1"), ("print(a)", "print(b)")]),
    T("loop with multiplier", "medium",
      "i = {s}\nc = 0\nwhile i < {limit}:\n    i = i * {m}\n    c = c + 1\nprint(c, i)",
      lambda r: {"s": r.randint(1, 4), "limit": r.randint(50, 200), "m": r.choice((2, 3))},
      [("i < {limit}", "i <= {limit}"), ("c + 1", "c + 2"), ("i * {m}", "i + {m}")]),
    T("matrix diagonals", "hard",
      "m = [[{a}, {b}, {c}], [{d}, {e}, {f}], [{g}, {h}, {i}]]\ns = 0\nfor k in range(3):\n    s = s + m[k][k] - m[k][2 - k]\nprint(s)",
      lambda r: dict(zip("abcdefghi", r.sample(range(1, 20), 9))),
      [("m[k][2 - k]", "m[k][k]"), ("- m[k]", "+ m[k]"), ("range(3)", "range(2)")]),
    T("operator precedence", "easy",
      "a = {a}\nb = {b}\nc = a + b * 2 - a // {d}\nprint(c)",
      lambda r: {"a": r.randint(10, 30), "b": r.randint(3, 9), "d": r.choice((3, 4, 5))},
      [("a + b * 2", "(a + b) * 2"), ("a // {d}", "a % {d}"), ("- a //", "+ a //")]),
]


def make(rng, tpl, n):
    for _ in range(100):
        params = tpl["params"](rng)
        code = tpl["code"].format(**params)
        answer = run_code(code)
        if answer is None:
            continue
        wrong = []
        for old, new in tpl["muts"]:
            old_s, new_s = old.format(**params), new.format(**params)
            if old_s not in code:
                continue
            out = run_code(code.replace(old_s, new_s, 1))
            if out and out != answer and out not in wrong:
                wrong.append(out)
        if len(wrong) < 3 and answer.lstrip("-").isdigit():     # pad with near-misses
            for delta in (1, -1, 2, -2, 3):
                v = str(int(answer) + delta)
                if v not in wrong and v != answer:
                    wrong.append(v)
                if len(wrong) >= 3:
                    break
        if len(wrong) < 3:
            continue
        opts = [answer] + wrong[:3]
        order = list(range(4))
        rng.shuffle(order)
        shuffled = [opts[i] for i in order]
        return {
            "question": "What is the output of the following code?\n\n" + code,
            "options": shuffled, "correct_index": shuffled.index(answer), "correct_answer": answer,
            "code": code,
        }
    return None


def run(per_template, seed):
    rng = random.Random(seed)
    items, seen = [], set()
    for tpl in TEMPLATES:
        made = 0
        for _ in range(per_template * 40):
            if made >= per_template:
                break
            it = make(rng, tpl, made)
            if not it or it["question"] in seen:
                continue
            seen.add(it["question"])
            made += 1
            # Re-run the displayed code one more time, independently of make().
            assert run_code(it["code"]) == it["correct_answer"]
            items.append({
                "id": f"gen2-pseudo-{tpl['name'].replace(' ', '-')}-{made:03d}", "type": "cs_fundamentals",
                "topic": "pseudocode", "sub_topic": tpl["name"], "difficulty": tpl["diff"],
                "question": it["question"], "options": it["options"], "correct_index": it["correct_index"],
                "correct_answer": it["correct_answer"],
                "explanation": "Trace the variables line by line. The answer is the printed value: " + it["correct_answer"] + ".",
                "common_trap": "Wrong options are what the same code prints with one common slip (off-by-one, wrong operator or bound).",
                "companies": COMPANIES, "role": ["student"], "stage": "placement",
                "trust_status": "unverified", "source_bank": "generated_pseudocode_v2", "verification_version": 0,
                "provenance": "generated; answer = output of executing the displayed code; distractors = outputs "
                              "of the same code with one injected bug; not yet through tranche review",
            })
    return items


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-template", type=int, default=5)
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    items = run(a.per_template, a.seed)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(items)} items -> {OUT}")
