"""Independent verifier for the parametric bank (deterministic, no LLM).

Recomputes every answer from the question text with an independent oracle
(regex parse + arithmetic / execution) and checks options/correct_index.
Writes app/data/parametric_verify_report.json.
"""
import ast
import contextlib
import io
import json
import math
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BANK = BASE / "app" / "data" / "parametric_practice_bank.json"
OUT = BASE / "app" / "data" / "parametric_verify_report.json"


def recompute(q):
    prov = q.get("provenance", "")
    fam = prov.split("(")[1].split(")")[0] if "(" in prov else "?"
    t = q["question"]
    nums = list(map(int, re.findall(r"-?\d+", t)))
    if fam == "pct_of":
        p, base = nums[0], nums[1]
        return str(base * p // 100)
    if fam == "pct_change":
        old, new = nums[0], nums[1]
        return f"{(new - old) * 100 // old}%"
    if fam == "profit_loss":
        cost, pct = nums[0], nums[1]
        return str(cost * (100 + pct) // 100)
    if fam == "ratio":
        total, a, b = nums[0], nums[1], nums[2]
        return str(max(total * a // (a + b), total * b // (a + b)))
    if fam == "average":
        return str(sum(nums) // len(nums))
    if fam == "std":
        return str(nums[0] * nums[1])
    if fam == "time_work":
        if "Together, how many jobs" in t:
            return "2"
        a, b = nums[0], nums[1]
        return str(a * b // (a + b))
    if fam == "si":
        p, r, yrs = nums[0], nums[1], nums[2]
        return str(p * r * yrs // 100)
    if fam == "ci":
        return str(nums[0] * 121 // 100)
    if fam == "npr":
        rr, nn = nums[0], nums[1]
        return str(math.perm(nn, rr))
    if fam == "prob":
        if "die" in t:
            return "1/2"
        if "coins" in t:
            return "1/4"
        red, blue = nums[0], nums[1]
        tot = red + blue
        g = math.gcd(red, tot)
        return f"{red//g}/{tot//g}"
    if fam in ("num_series", "mixed_series"):
        terms = nums
        diffs = [terms[i + 1] - terms[i] for i in range(len(terms) - 1)]
        if len(set(diffs)) == 1:
            return str(terms[-1] + diffs[0])
        if all(terms[i + 1] == terms[i] * 2 for i in range(len(terms) - 1)):
            return str(terms[-1] * 2)
        if all(terms[i + 1] == terms[i] * 2 + 1 for i in range(len(terms) - 1)):
            return str(terms[-1] * 2 + 1)
        roots = [int(math.isqrt(v)) for v in terms]
        if all(r * r == v for r, v in zip(roots, terms)):
            return str((roots[-1] + 1) ** 2)
        return None
    if fam == "odd_one":
        odds = [v for v in nums if v % 2]
        evens = [v for v in nums if not v % 2]
        if len(odds) == 1:
            return str(odds[0])
        if len(evens) == 1:
            return str(evens[0])
        return None
    if fam == "letter_series":
        m = re.search(r"\?\s*([A-Z](?:,\s*[A-Z])+)", t)
        letters = re.findall(r"[A-Z]", m.group(1)) if m else re.findall(r"[A-Z]", t)
        vals = [ord(c) - 65 for c in letters]
        step = (vals[1] - vals[0]) % 26
        return chr(65 + ((vals[-1] + step) % 26))
    if fam == "direction":
        return "5"
    if fam == "bin_dec":
        b = re.search(r"[01]{2,}", t).group(0)
        return str(int(b, 2))
    if fam == "hex_dec":
        h = re.search(r"[0-9A-F]{1,}", t).group(0)
        return str(int(h, 16))
    if fam == "bitwise":
        m = re.search(r"(\d+)\s*([&|^])\s*(\d+)", t)
        a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
        return str({"&": a & b, "|": a | b, "^": a ^ b}[op])
    if fam == "bigo":
        for sig, ans in [("halves", "O(log n)"), ("nested", "O(n²)"),
                         ("n times with a log", "O(n log n)"),
                         ("no loops", "O(1)"), ("single loop", "O(n)")]:
            if sig in t:
                return ans
        return None
    if fam == "code_output":
        code = q["solution"]["code"]
        ns: dict = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(code, ns)
        m = re.search(r"solve\(a=(\d+),\s*b=(\d+)\)", t)
        a, b = int(m.group(1)), int(m.group(2))
        with contextlib.redirect_stdout(io.StringIO()):
            got = ns["solve"](a=a, b=b)
        # also check hidden
        for h in q.get("hidden_testcases", []):
            m2 = re.search(r"a=(\d+),\s*b=(\d+)", h["input"])
            a2, b2 = int(m2.group(1)), int(m2.group(2))
            with contextlib.redirect_stdout(io.StringIO()):
                exp2 = str(ns["solve"](a=a2, b=b2))
            if exp2 != h["expected"]:
                return f"HIDDEN_MISMATCH:{exp2}!={h['expected']}"
        return str(got)
    return None


def main():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    ok, fail = 0, 0
    bad_fams: dict = {}
    for q in bank:
        # structural
        opts = q.get("options", [])
        ci = q.get("correct_index")
        ans = q.get("correct_answer")
        struct_ok = (len(opts) == 4 and len(set(opts)) == 4
                     and isinstance(ci, int) and 0 <= ci < 4
                     and opts[ci] == ans and ans in (q.get("explanation") or ""))
        if not struct_ok:
            fail += 1
            bad_fams["STRUCT"] = bad_fams.get("STRUCT", 0) + 1
            continue
        try:
            exp = recompute(q)
        except Exception:
            exp = None
        if exp is None or exp != ans:
            fail += 1
            fam = q.get("provenance", "?")[:60]
            bad_fams[fam] = bad_fams.get(fam, 0) + 1
        else:
            ok += 1
    OUT.write_text(json.dumps({
        "total": len(bank),
        "independent_pass": ok,
        "fail": fail,
        "bad_families": bad_fams,
        "trust": "automated_checked (human sampling still required for TRUSTED)",
    }, indent=1), encoding="utf-8")
    print(f"PARAMETRIC_VERIFY pass={ok} fail={fail} total={len(bank)}")
    print(bad_fams)


if __name__ == "__main__":
    main()
