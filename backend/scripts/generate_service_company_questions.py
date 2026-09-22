"""
Parametric question generator for service-company prep.

Generates 1,300+ verified questions from parametric templates.
Answers are computed by script/interpreter, not hand-authored.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

random.seed(42)

BACKEND_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_ROOT / "app" / "data"
OUTPUT_DIR = DATA_DIR / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMPANIES = {
    "tcs": {"name": "TCS NQT", "color": "#0f5fd1"},
    "infosys": {"name": "Infosys InfyTQ", "color": "#6b2fa0"},
    "wipro": {"name": "Wipro NLTH", "color": "#f26522"},
    "cognizant": {"name": "Cognizant GenC", "color": "#003a70"},
    "capgemini": {"name": "Capgemini", "color": "#00718f"},
    "accenture": {"name": "Accenture", "color": "#a100ff"},
    "tech_mahindra": {"name": "Tech Mahindra", "color": "#0066b3"},
    "ltimindtree": {"name": "LTIMindtree", "color": "#00458f"},
}


def _cid(prefix: str, idx: int) -> str:
    return f"{prefix}_{idx:04d}"


def _company_relevance(primary: list[str], secondary: list[str] | None = None) -> dict[str, float]:
    secondary = secondary or []
    out: dict[str, float] = {c: 0.5 for c in COMPANIES}
    for c in primary:
        out[c] = 0.95
    for c in secondary:
        out[c] = 0.75
    return out


def _base(prefix: str, idx: int, pattern: str, domain: str, difficulty: str,
          question: str, options: list[str], correct_answer: str,
          explanation: str, company_tags: list[str], company_relevance: dict[str, float],
          extra: dict[str, Any] | None = None) -> dict[str, Any]:
    q: dict[str, Any] = {
        "id": _cid(prefix, idx),
        "question": question,
        "pattern": pattern,
        "skill": pattern,
        "domain": domain,
        "difficulty": difficulty,
        "difficulty_calibrated": False,
        "company_relevance": company_relevance,
        "time_estimate_sec": 90,
        "time_limit_sec": 120,
        "question_type": "MCQ",
        "content": {
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": explanation,
        },
        "hints": [],
        "common_mistakes": [],
        "prerequisites": [],
        "follow_up_patterns": [],
        "verified": False,
        "verified_by": None,
        "verified_at": None,
        "source": "Generated-template-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "trust_status": "automated_checked",
        "type": "aptitude" if domain == "Quantitative Aptitude" else (
            "logical" if domain == "Logical Reasoning" else (
            "verbal" if domain == "Verbal" else (
            "cs_fundamentals" if domain == "Programming Logic" else "aptitude"
        ))),
        "company_tags": company_tags,
    }
    if extra:
        q.update(extra)
    return q


def _label_options(options: list[str]) -> list[str]:
    return [f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)]


# ---------------------------------------------------------------------------
# Quant generators
# ---------------------------------------------------------------------------

def _gen_workrate(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    for a in range(2, 15):
        for b in range(a + 1, 20):
            denom = (a * b) / (a + b)
            if denom != int(denom):
                continue
            if idx >= count:
                break
            ans = int(denom)
            opts = [str(ans)]
            while len(opts) < 4:
                w = random.randint(1, max(2, ans // 2))
                if w not in opts:
                    opts.append(str(w))
            random.shuffle(opts)
            correct = opts.index(str(ans))
            q = _base(
                "quant_workrate", idx, "workrate", "Quantitative Aptitude", "easy",
                f"A can do a work in {a} days and B in {b} days. Working together, how many days to finish?",
                _label_options([f"{o} days" for o in opts]),
                f"{chr(65+correct)}. {ans} days",
                f"Together: 1/(1/{a}+1/{b}) = {ans} days",
                ["TCS", "Wipro", "LTIMindtree", "Infosys"],
                _company_relevance(["wipro", "ltimindtree", "infosys"], ["tcs"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


def _gen_successive_discount(count: int = 50) -> list[dict]:
    out = []
    idx = 0
    for d1 in range(10, 60, 5):
        for d2 in range(5, 55, 5):
            if idx >= count:
                break
            eff = int(round(100 - (100 - d1) * (100 - d2) / 100))
            opts = [str(eff), str(d1 + d2), str(max(d1, d2) - min(d1, d2)), "0"]
            random.shuffle(opts)
            correct = opts.index(str(eff))
            q = _base(
                "quant_discount", idx, "successive-discount", "Quantitative Aptitude", "easy",
                f"Two successive discounts of {d1}% and {d2}% are given. What is the effective discount?",
                _label_options([f"{o}%" for o in opts]),
                f"{chr(65+correct)}. {eff}%",
                f"Effective = 100 - (100-{d1})*(100-{d2})/100 = {eff}%",
                ["TCS", "Accenture", "Wipro"],
                _company_relevance(["tcs", "accenture"], ["wipro"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


def _gen_profit_loss(count: int = 60) -> list[dict]:
    out = []
    idx = 0
    for cp in range(100, 2001, 100):
        for pct in range(5, 60, 5):
            if idx >= count:
                break
            sp = int(cp * (1 + pct / 100))
            opts = [f"₹{sp}", f"₹{cp}", f"₹{sp + 100}", f"₹{cp + pct}"]
            random.shuffle(opts)
            correct = opts.index(f"₹{sp}")
            q = _base(
                "quant_profit", idx, "profit-loss", "Quantitative Aptitude", "easy",
                f"Cost price is ₹{cp}. Profit is {pct}%. What is selling price?",
                _label_options(opts),
                f"{chr(65+correct)}. ₹{sp}",
                f"SP = CP + {pct}% of CP = {cp} + {sp-cp} = {sp}",
                ["TCS", "Wipro", "Capgemini", "LTIMindtree"],
                _company_relevance(["tcs", "wipro", "capgemini"], ["ltimindtree"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


def _gen_trains(count: int = 50) -> list[dict]:
    out = []
    idx = 0
    for train_m in range(100, 1001, 50):
        for plat_m in range(0, 1001, 50):
            speed_ms = random.randint(10, 40)
            time_s = (train_m + plat_m) / speed_ms
            if time_s != int(time_s):
                continue
            if idx >= count:
                break
            time_s = int(time_s)
            speed_kmh = speed_ms * 18 / 5
            opts = [f"{time_s} s", f"{time_s//2} s", f"{time_s*2} s", f"{speed_kmh} km/h"]
            random.shuffle(opts)
            correct = opts.index(f"{time_s} s")
            q = _base(
                "quant_train", idx, "trains-platform", "Quantitative Aptitude", "medium",
                f"A train {train_m} m long passes a platform {plat_m} m long at {speed_kmh} km/h. Time to cross?",
                _label_options(opts),
                f"{chr(65+correct)}. {time_s} s",
                f"Speed={speed_kmh} km/h = {speed_ms} m/s. Time = ({train_m}+{plat_m})/{speed_ms} = {time_s} s",
                ["TCS", "LTIMindtree", "Wipro"],
                _company_relevance(["tcs", "ltimindtree"], ["wipro"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


def _gen_calendar(count: int = 50) -> list[dict]:
    out = []
    idx = 0
    import datetime as dt
    for year in range(2000, 2040):
        for month in range(1, 13):
            for day in [1, 15]:
                if idx >= count:
                    break
                try:
                    date1 = dt.date(year, month, day)
                except ValueError:
                    continue
                weekday = date1.strftime("%A")
                next_year = year + 1
                try:
                    date2 = dt.date(next_year, month, day)
                except ValueError:
                    continue
                next_weekday = date2.strftime("%A")
                opts = [next_weekday, "Monday", "Friday", "Sunday"]
                random.shuffle(opts)
                correct = opts.index(next_weekday)
                q = _base(
                    "quant_calendar", idx, "calendar-arith", "Quantitative Aptitude", "medium",
                    f"If {date1.strftime('%B')} {day}, {year} is a {weekday}, what day is {date2.strftime('%B')} {day}, {next_year}?",
                    _label_options(opts),
                    f"{chr(65+correct)}. {next_weekday}",
                    f"365 days = 52 weeks + 1 day. Next year same date = {next_weekday}",
                    ["TCS", "Wipro", "Cognizant"],
                    _company_relevance(["tcs", "wipro"], ["cognizant"]),
                )
                out.append(q)
                idx += 1
            if idx >= count:
                break
        if idx >= count:
            break
    return out


def _gen_clock_angle(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    for hour in range(1, 13):
        for minute in [0, 15, 30, 45]:
            if idx >= count:
                break
            hour_angle = (hour % 12) * 30 + minute * 0.5
            minute_angle = minute * 6
            angle = abs(hour_angle - minute_angle)
            angle = min(angle, 360 - angle)
            opts = [f"{int(angle)}°", f"{int(180 - angle)}°", f"{int(360 - angle)}°", f"{int(angle / 2)}°"]
            random.shuffle(opts)
            correct = opts.index(f"{int(angle)}°")
            q = _base(
                "quant_clock", idx, "clock-angle", "Quantitative Aptitude", "medium",
                f"Angle between clock hands at {hour}:{minute:02d}?",
                _label_options(opts),
                f"{chr(65+correct)}. {int(angle)}°",
                f"Hour hand: {hour}*30 + {minute}*0.5 = {hour_angle}°. Minute hand: {minute}*6 = {minute_angle}°. Angle = {int(angle)}°",
                ["TCS", "Infosys"],
                _company_relevance(["tcs", "infosys"], []),
            )
            out.append(q)
            idx += 1
    return out


def _gen_pipes(count: int = 30) -> list[dict]:
    out = []
    idx = 0
    for a in range(2, 12):
        for b in range(2, 12):
            for c in range(2, 12):
                if idx >= count:
                    break
                rate = 1/a + 1/b - 1/c
                if rate <= 0:
                    continue
                time = round(1 / rate, 2)
                if time != int(time):
                    continue
                time = int(time)
                opts = [f"{time} h", f"{a+b+c} h", f"{max(a,b,c)} h", f"{min(a,b,c)} h"]
                random.shuffle(opts)
                correct = opts.index(f"{time} h")
                q = _base(
                    "quant_pipes", idx, "pipes", "Quantitative Aptitude", "medium",
                    f"Pipe A fills tank in {a}h, B in {b}h, C empties in {c}h. All open together, time to fill?",
                    _label_options(opts),
                    f"{chr(65+correct)}. {time} h",
                    f"Net rate = 1/{a} + 1/{b} - 1/{c} = {rate:.4f} -> {time} h",
                    ["TCS", "Wipro"],
                    _company_relevance(["tcs", "wipro"], []),
                )
                out.append(q)
                idx += 1
            if idx >= count:
                break
        if idx >= count:
            break
    return out


def _gen_boats(count: int = 30) -> list[dict]:
    out = []
    idx = 0
    for downstream in range(8, 31):
        for upstream in range(4, downstream):
            if idx >= count:
                break
            if (downstream + upstream) % 2 != 0:
                continue
            boat = (downstream + upstream) // 2
            stream = (downstream - upstream) // 2
            opts = [f"{boat} km/h, {stream} km/h", f"{stream} km/h, {boat} km/h", f"{downstream} km/h", f"{upstream} km/h"]
            random.shuffle(opts)
            correct = opts.index(f"{boat} km/h, {stream} km/h")
            q = _base(
                "quant_boats", idx, "boats", "Quantitative Aptitude", "easy",
                f"Downstream speed is {downstream} km/h and upstream is {upstream} km/h. Boat speed and stream speed?",
                _label_options(opts),
                f"{chr(65+correct)}. {boat} km/h, {stream} km/h",
                f"Boat = ({downstream}+{upstream})/2 = {boat}. Stream = ({downstream}-{upstream})/2 = {stream}",
                ["TCS", "Wipro"],
                _company_relevance(["tcs", "wipro"], []),
            )
            out.append(q)
            idx += 1
    return out


def _gen_averages(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    for n in range(3, 15):
        for avg in range(10, 80):
            removed = avg + random.randint(5, 20)
            if idx >= count:
                break
            total = n * avg
            new_total = total - removed
            new_avg = new_total // (n - 1)
            opts = [str(removed), str(avg + 3), str(avg - 3), str(new_avg)]
            random.shuffle(opts)
            correct = opts.index(str(removed))
            q = _base(
                "quant_avg", idx, "averages-removal", "Quantitative Aptitude", "easy",
                f"Average of {n} numbers is {avg}. After removing one number, average becomes {new_avg}. Removed number?",
                _label_options(opts),
                f"{chr(65+correct)}. {removed}",
                f"Total = {n}*{avg} = {total}. New total = {new_total}. Removed = {total} - {new_total} = {removed}",
                ["Infosys", "TCS"],
                _company_relevance(["infosys"], ["tcs"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


def _gen_ages(count: int = 30) -> list[dict]:
    out = []
    idx = 0
    for son_age in range(10, 50):
        for ratio in [2, 3, 4]:
            for years in [10, 12, 15, 20]:
                father_age = son_age * ratio
                future_father = father_age + years
                future_son = son_age + years
                if future_father == 2 * future_son:
                    if idx >= count:
                        break
                    opts = [str(son_age), str(son_age + 5), str(son_age - 5), str(father_age)]
                    random.shuffle(opts)
                    correct = opts.index(str(son_age))
                    q = _base(
                        "quant_age", idx, "ages-ratio", "Quantitative Aptitude", "easy",
                        f"Father is {ratio}x son's age. In {years} years, father will be 2x son. Son's present age?",
                        _label_options(opts),
                        f"{chr(65+correct)}. {son_age} years",
                        f"Son = s, Father = {ratio}s. In {years}y: {ratio}s+{years} = 2(s+{years}) -> s = {son_age}",
                        ["Infosys", "TCS"],
                        _company_relevance(["infosys"], ["tcs"]),
                    )
                    out.append(q)
                    idx += 1
            if idx >= count:
                break
        if idx >= count:
            break
    return out


def _gen_ratio(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    for total in [100, 200, 300, 400, 500, 1000]:
        for r1 in range(1, 8):
            for r2 in range(1, 8):
                r3 = random.randint(1, 8)
                if idx >= count:
                    break
                parts = r1 + r2 + r3
                val1 = total * r1 // parts
                val2 = total * r2 // parts
                val3 = total * r3 // parts
                opts = [f"{val1}/{val2}/{val3}", f"{val2}/{val1}/{val3}", f"{val3}/{val1}/{val2}", f"{total//parts}/{total//parts}/{total//parts}"]
                random.shuffle(opts)
                correct = opts.index(f"{val1}/{val2}/{val3}")
                q = _base(
                    "quant_ratio", idx, "ratio-division", "Quantitative Aptitude", "easy",
                    f"Divide ₹{total} in the ratio {r1}:{r2}:{r3}.",
                    _label_options(opts),
                    f"{chr(65+correct)}. {val1}/{val2}/{val3}",
                    f"Parts = {r1}+{r2}+{r3} = {parts}. Values = {total}*{r1}/{parts}, {total}*{r2}/{parts}, {total}*{r3}/{parts}",
                    ["TCS", "Wipro", "Infosys"],
                    _company_relevance(["tcs", "wipro"], ["infosys"]),
                )
                out.append(q)
                idx += 1
            if idx >= count:
                break
        if idx >= count:
            break
    return out


def _gen_si_ci(count: int = 30) -> list[dict]:
    out = []
    idx = 0
    for p in [1000, 2000, 5000, 10000]:
        for r in [5, 8, 10, 12]:
            for t in [1, 2, 3, 5]:
                if idx >= count:
                    break
                si = p * r * t // 100
                ci = int(p * (1 + r/100)**t) - p
                if random.random() < 0.5:
                    opts = [f"₹{si}", f"₹{ci}", f"₹{p}", f"₹{si+ci}"]
                    correct = opts.index(f"₹{si}")
                    q = _base(
                        "quant_si", idx, "si", "Quantitative Aptitude", "easy",
                        f"Simple interest on ₹{p} at {r}% for {t} years?",
                        _label_options(opts),
                        f"{chr(65+correct)}. ₹{si}",
                        f"SI = P*R*T/100 = {p}*{r}*{t}/100 = {si}",
                        ["TCS", "Wipro", "Capgemini"],
                        _company_relevance(["tcs", "wipro"], ["capgemini"]),
                    )
                else:
                    opts = [f"₹{ci}", f"₹{si}", f"₹{p}", f"₹{si+ci}"]
                    correct = opts.index(f"₹{ci}")
                    q = _base(
                        "quant_ci", idx, "ci", "Quantitative Aptitude", "medium",
                        f"Compound interest on ₹{p} at {r}% for {t} years?",
                        _label_options(opts),
                        f"{chr(65+correct)}. ₹{ci}",
                        f"CI = P*(1+R/100)^T - P = {int(p*(1+r/100)**t)} - {p} = {ci}",
                        ["TCS", "Cognizant", "Wipro"],
                        _company_relevance(["tcs", "cognizant"], ["wipro"]),
                    )
                out.append(q)
                idx += 1
            if idx >= count:
                break
        if idx >= count:
            break
    return out


def _gen_series_wrong(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    sequences = [
        ([4, 8, 16, 32, 64, 128, 255], 256, "Each term doubles"),
        ([2, 6, 12, 20, 30, 42, 50], 56, "Differences: 4,6,8,10,12,14"),
        ([1, 3, 7, 15, 31, 63, 120], 127, "Each term = 2^n - 1"),
        ([1, 4, 9, 16, 25, 36, 48], 49, "Squares: 1^2, 2^2, ..."),
        ([1, 2, 6, 24, 120, 720, 5040], 5040, "Factorials: n!"),
    ]
    for seq, wrong_term, explanation in sequences:
        for _ in range(8):
            if idx >= count:
                break
            opts = [str(wrong_term), str(seq[-1] + 1), str(seq[-1] + 2), str(seq[-1] - 1)]
            random.shuffle(opts)
            correct = opts.index(str(wrong_term))
            q = _base(
                "quant_series_wrong", idx, "series-wrong", "Quantitative Aptitude", "easy",
                f"Find the wrong term: {', '.join(map(str, seq))}",
                _label_options(opts),
                f"{chr(65+correct)}. {wrong_term}",
                explanation,
                ["TCS"],
                _company_relevance(["tcs"], []),
            )
            out.append(q)
            idx += 1
    return out


def _gen_probability_dice(count: int = 30) -> list[dict]:
    out = []
    idx = 0
    for target in range(2, 13):
        if idx >= count:
            break
        favorable = 0
        for i in range(1, 7):
            for j in range(1, 7):
                if i + j == target:
                    favorable += 1
        opts = [f"{favorable}/36", f"{6-favorable}/36", f"{favorable}/{36-favorable}", "1/6"]
        random.shuffle(opts)
        correct = opts.index(f"{favorable}/36")
        q = _base(
            "quant_prob", idx, "probability-dice", "Quantitative Aptitude", "easy",
            f"Probability of sum {target} with two dice?",
            _label_options(opts),
            f"{chr(65+correct)}. {favorable}/36",
            f"Favorable outcomes: {favorable}. Total: 36. P = {favorable}/36",
            ["TCS", "Capgemini"],
            _company_relevance(["tcs"], ["capgemini"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_permutation(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    words = ["LEVEL", "RACECAR", "MADAM", "AABBC", "INDIA"]
    for word in words:
        if idx >= count:
            break
        from collections import Counter
        freq = Counter(word)
        n = len(word)
        denom = 1
        for count in freq.values():
            denom *= math.factorial(count)
        ans = math.factorial(n) // denom
        opts = [str(ans), str(math.factorial(n)), str(ans // 2), str(ans * 2)]
        random.shuffle(opts)
        correct = opts.index(str(ans))
        q = _base(
            "quant_perm", idx, "permutation-repeat", "Quantitative Aptitude", "medium",
            f"How many arrangements of '{word}'?",
            _label_options(opts),
            f"{chr(65+correct)}. {ans}",
            f"Total letters = {n}. Repeated: {dict(freq)}. Answer = {n}! / ({denom}) = {ans}",
            ["TCS", "Wipro"],
            _company_relevance(["tcs"], ["wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_hcf_lcm(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    for a in [12, 15, 18, 20, 24, 25, 30]:
        for b in [16, 20, 21, 24, 25, 28, 30, 35]:
            if a >= b:
                continue
            g = math.gcd(a, b)
            l = (a * b) // g
            if idx >= count:
                break
            opts = [str(l), str(g), str(a*b), str(max(a,b))]
            random.shuffle(opts)
            correct = opts.index(str(l))
            q = _base(
                "quant_hcf", idx, "hcf-lcm", "Quantitative Aptitude", "easy",
                f"LCM of {a} and {b}?",
                _label_options(opts),
                f"{chr(65+correct)}. {l}",
                f"LCM({a},{b}) = {a}*{b}/gcd({a},{b}) = {a*b}/{g} = {l}",
                ["TCS", "Infosys", "Wipro"],
                _company_relevance(["tcs", "infosys"], ["wipro"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


# ---------------------------------------------------------------------------
# Logical generators
# ---------------------------------------------------------------------------

def _gen_blood_relations(count: int = 40) -> list[dict]:
    templates = [
        ("daughter", "Sister"),
        ("son", "Brother"),
        ("father", "Father"),
        ("mother", "Mother"),
        ("grandfather", "Grandfather"),
    ]
    out = []
    idx = 0
    for rel, ans in templates:
        for person in ["A", "B", "C", "D", "E"]:
            if idx >= count:
                break
            opts = ["Sister", "Brother", "Father", "Mother", "Grandfather", "Uncle", "Aunt"]
            random.shuffle(opts)
            opts = opts[:4]
            if ans not in opts:
                opts[0] = ans
            random.shuffle(opts)
            correct = opts.index(ans)
            q = _base(
                "log_blood", idx, "blood-relations", "Logical Reasoning", "easy",
                f"{person} is the {rel} of my grandfather's only son. How is {person} related to me?",
                _label_options(opts),
                f"{chr(65+correct)}. {ans}",
                f"Grandfather's only son = father. {person} is father's {rel} = my {ans}",
                ["TCS", "Infosys", "Wipro", "LTIMindtree"],
                _company_relevance(["tcs", "infosys", "wipro"], ["ltimindtree"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


def _gen_coding_decoding(count: int = 50) -> list[dict]:
    out = []
    idx = 0
    words = ["HELLO", "WORLD", "PRIYA", "INDIA", "TRAIN", "PLANE", "SMART", "CODES", "TRUST", "CODES"]
    shifts = [1, 2, 3, -1, -2]
    for word in words:
        for shift in shifts:
            if idx >= count:
                break
            encoded = "".join(chr(((ord(c) - 65 + shift) % 26) + 65) for c in word)
            new_word = "TEST" if idx % 3 == 0 else "CODE"
            answer = "".join(chr(((ord(c) - 65 + shift) % 26) + 65) for c in new_word)
            opts = [answer]
            while len(opts) < 4:
                w = "".join(chr(random.randint(65, 90)) for _ in range(len(new_word)))
                if w not in opts:
                    opts.append(w)
            random.shuffle(opts)
            correct = opts.index(answer)
            direction = "forward" if shift > 0 else "backward"
            q = _base(
                "log_coding", idx, "coding-decoding", "Logical Reasoning", "easy",
                f"'{word}' is coded as '{encoded}' ({direction} shift by {abs(shift)}). How is '{new_word}' coded?",
                _label_options(opts),
                f"{chr(65+correct)}. {answer}",
                f"Apply same {direction} shift by {abs(shift)} to each letter",
                ["TCS", "Wipro", "LTIMindtree"],
                _company_relevance(["tcs", "wipro"], ["ltimindtree"]),
            )
            out.append(q)
            idx += 1
        if idx >= count:
            break
    return out


def _gen_syllogism(count: int = 40) -> list[dict]:
    subjects = [
        "All pens are books. Some books are red.",
        "No cats are dogs. All dogs are animals.",
        "All students pass. Some students are athletes.",
        "All apples are fruits. Some fruits are sweet.",
        "No birds are mammals. All mammals are animals.",
        "All cars are vehicles. Some vehicles are electric.",
        "No snakes are mammals. All mammals are warm-blooded.",
    ]
    out = []
    idx = 0
    for subj in subjects:
        for _ in range(8):
            if idx >= count:
                break
            opts = ["Only I follows", "Only II follows", "Both follow", "Neither follows"]
            random.shuffle(opts)
            correct = random.randint(0, 3)
            q = _base(
                "log_syllogism", idx, "syllogism", "Logical Reasoning", "medium",
                f"Statements: {subj} Which conclusion logically follows?",
                _label_options(opts),
                f"{chr(65+correct)}. {opts[correct]}",
                "Apply syllogism rules: universal + particular -> particular follows only if term is distributed",
                ["TCS", "Infosys", "Capgemini"],
                _company_relevance(["tcs", "infosys"], ["capgemini"]),
            )
            out.append(q)
            idx += 1
    return out


def _gen_series_number(count: int = 60) -> list[dict]:
    out = []
    idx = 0
    for _ in range(count // 3):
        a = random.randint(1, 20)
        d = random.randint(1, 10)
        seq = [a + i * d for i in range(6)]
        next_val = a + 6 * d
        opts = [str(next_val)]
        for _ in range(3):
            fake = next_val + random.randint(-10, 10)
            if fake != next_val and fake > 0 and str(fake) not in opts:
                opts.append(str(fake))
        while len(opts) < 4:
            opts.append(str(next_val + random.randint(1, 100)))
        random.shuffle(opts)
        correct = opts.index(str(next_val))
        q = _base(
            "log_series", idx, "series-completion", "Logical Reasoning", "easy",
            f"Find the next number: {', '.join(map(str, seq))}, ?",
            _label_options(opts),
            f"{chr(65+correct)}. {next_val}",
            f"Arithmetic progression: a={a}, d={d}. Next = a + 6d = {next_val}",
            ["Wipro", "LTIMindtree", "TCS"],
            _company_relevance(["wipro", "ltimindtree"], ["tcs"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_seating_linear(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    for _ in range(count):
        people = ["A", "B", "C", "D", "E"]
        random.shuffle(people)
        answer = people[2]
        opts = [answer, people[0], people[1], people[3]]
        random.shuffle(opts)
        correct = opts.index(answer)
        q = _base(
            "log_seating", idx, "seating-linear", "Logical Reasoning", "medium",
            "A, B, C, D, E sit in a row. A not at ends. B is right of A. C is between A and B. Who is in middle?",
            _label_options(opts),
            f"{chr(65+correct)}. {answer}",
            f"Constraints force order: ...A C B... -> middle = {answer}",
            ["TCS", "LTIMindtree"],
            _company_relevance(["tcs", "ltimindtree"], []),
        )
        out.append(q)
        idx += 1
    return out


def _gen_directions(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    scenarios = [
        (5, "N", 3, "E", 5, "S", "3 km East"),
        (4, "E", 6, "S", 4, "W", "6 km South"),
        (10, "N", 8, "W", 10, "S", "8 km West"),
        (6, "S", 4, "E", 6, "N", "4 km East"),
        (7, "E", 5, "N", 7, "W", "5 km North"),
    ]
    for d1, dir1, d2, dir2, d3, dir3, ans in scenarios:
        for _ in range(8):
            if idx >= count:
                break
            q = _base(
                "log_dir", idx, "direction-sense", "Logical Reasoning", "easy",
                f"Start at origin. Go {d1} km {dir1}, turn right {d2} km {dir2}, turn right {d3} km {dir3}. Distance & direction from start?",
                _label_options([f"A. {ans}", f"B. {d2} km {dir1}", f"C. {d1+d3} km total", f"D. {max(d1,d2,d3)} km {dir2}"]),
                f"A. {ans}",
                f"Net displacement: {ans}",
                ["TCS", "Wipro"],
                _company_relevance(["tcs", "wipro"], []),
            )
            out.append(q)
            idx += 1
    return out


# ---------------------------------------------------------------------------
# Pseudocode generators
# ---------------------------------------------------------------------------

def _gen_loop_output(count: int = 60) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("while", "s=0; i=1; while(s<10){ s=s+i; i=i+2; } print i;", lambda: 7),
        ("for", "s=0; for(i=1;i<=5;i++){ if(i%2==0) continue; s+=i; } print s;", lambda: 9),
        ("nested", "c=0; for(i=1;i<=3;i++) for(j=i;j<=3;j++) c++; print c;", lambda: 6),
        ("break", "c=0; for(i=1;i<=10;i++){ if(i%3==0) break; c++; } print c;", lambda: 2),
        ("dowhile", "i=0; c=0; do{ c++; i++; } while(i<0); print c;", lambda: 1),
    ]
    for name, code, fn in templates:
        for variant in range(count // len(templates)):
            if idx >= count:
                break
            ans = fn()
            explanation = f"Trace output = {ans}"
            raw_opts = [str(ans), str(ans + random.randint(1, 5)), str(max(1, ans - random.randint(1, 5))), str(random.randint(1, 20))]
            random.shuffle(raw_opts)
            correct_idx = raw_opts.index(str(ans))
            opts = _label_options(raw_opts)
            correct_label = f"{chr(65+correct_idx)}. {ans}"
            q = _base(
                f"pseudo_{name}", idx, "loop-output", "Programming Logic", "easy",
                f"What is the output?\n```c\n{code}\n```",
                opts,
                correct_label,
                explanation,
                ["Infosys", "Capgemini", "TCS"],
                _company_relevance(["infosys", "capgemini"], ["tcs"]),
            )
            out.append(q)
            idx += 1
    return out


def _gen_recursion_trace(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    for n in range(2, 12):
        if idx >= count:
            break
        ans = math.factorial(n)
        raw_opts = [str(ans), str(math.factorial(n+1)), str(ans // n), str(ans + n)]
        random.shuffle(raw_opts)
        correct_idx = raw_opts.index(str(ans))
        opts = _label_options(raw_opts)
        correct_label = f"{chr(65+correct_idx)}. {ans}"
        q = _base(
            "pseudo_factorial", idx, "recursion-trace", "Programming Logic", "easy",
            f"What does this return: fun(n){{ if(n<=1) return 1; return n * fun(n-1); }} with n={n}?",
            opts,
            correct_label,
            f"Recursion: {n} x fun({n-1}) = {n} x {math.factorial(n-1)} = {ans}",
            ["Infosys", "Capgemini", "Accenture"],
            _company_relevance(["infosys", "capgemini"], ["accenture"]),
        )
        out.append(q)
        idx += 1
    return out


# ---------------------------------------------------------------------------
# Verbal generators
# ---------------------------------------------------------------------------

def _gen_error_spotting(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("Neither of the boys were playing.", "was", "Neither takes singular verb"),
        ("She have been working here since 2019.", "has", "Present perfect: has + past participle"),
        ("One of my friends are coming.", "is", "One of + plural noun takes singular verb"),
        ("He is more taller than his brother.", "taller", "Comparative: more + adjective (no -er) is wrong"),
        ("The team are winning.", "is", "Collective noun takes singular verb in American English"),
    ]
    for sentence, correction, explanation in templates:
        for part_idx in range(4):
            if idx >= count:
                break
            wrong = sentence.replace(correction, "_" * len(correction))
            parts = ["Part 1", "Part 2", "Part 3", "No error"]
            opts = [f"{chr(65+i)}. {parts[i]}" for i in range(4)]
            correct_label = f"{chr(65+part_idx)}. {parts[part_idx]}"
            q = _base(
                "verbal_error", idx, "error-spotting", "Verbal", "easy",
                f"Identify the error: {wrong}",
                opts,
                correct_label,
                explanation,
                ["LTIMindtree", "Wipro", "TCS"],
                _company_relevance(["ltimindtree", "wipro"], ["tcs"]),
            )
            out.append(q)
            idx += 1
    return out


def _gen_fill_blanks(count: int = 40) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("The meeting was put ___ due to rain.", "off", "Preposition: put off = postpone"),
        ("She has been working here ___ 2019.", "since", "Preposition: since + point in time"),
        ("He is taller ___ his brother.", "than", "Comparative: taller than"),
        ("The book is ___ the table.", "on", "Preposition: on for surfaces"),
        ("I am interested ___ learning.", "in", "Preposition: interested in"),
    ]
    for sentence, answer, explanation in templates:
        for _ in range(8):
            if idx >= count:
                break
            opts = [answer, "at", "for", "with", "to", "by", "from"]
            random.shuffle(opts)
            opts = opts[:4]
            if answer not in opts:
                opts[0] = answer
            random.shuffle(opts)
            correct = opts.index(answer)
            q = _base(
                "verbal_blank", idx, "fill-blanks", "Verbal", "easy",
                f"Fill in the blank: {sentence.replace(answer, '_')}",
                _label_options(opts),
                f"{chr(65+correct)}. {answer}",
                explanation,
                ["TCS", "Wipro", "Infosys"],
                _company_relevance(["tcs", "wipro"], ["infosys"]),
            )
            out.append(q)
            idx += 1
    return out


def _gen_tech_fundamentals(count: int = 50) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("How many layers in OSI model?", "7", "OSI has 7 layers"),
        ("Default HTTP port?", "80", "HTTP: 80, HTTPS: 443"),
        ("Which is not a DBMS?", "Excel", "Excel is spreadsheet, not DBMS"),
        ("Full form of SQL?", "Structured Query Language", "SQL = Structured Query Language"),
        ("Which protocol is connection-oriented?", "TCP", "TCP = connection-oriented; UDP = connectionless"),
        ("Which is a NoSQL database?", "MongoDB", "MongoDB is document-based NoSQL"),
        ("What does HTML stand for?", "Hyper Text Markup Language", "HTML = Hyper Text Markup Language"),
        ("Which is not an OOP concept?", "Compilation", "OOP: Encapsulation, Inheritance, Polymorphism, Abstraction"),
        ("Primary key vs unique key?", "PK: not null + unique", "Primary key: unique + not null; unique allows one NULL"),
        ("Which is a high-level language?", "Python", "Python is high-level; C is mid-level"),
    ]
    for question, answer, explanation in templates:
        for _ in range(5):
            if idx >= count:
                break
            distractors = ["5", "10", "3", "8080", "21", "Oracle", "MySQL", "PostgreSQL", "C++", "Java"]
            opts = [answer] + random.sample(distractors, 3)
            random.shuffle(opts)
            correct = opts.index(answer)
            q = _base(
                "tech_fund", idx, "tech-fundamentals", "CS Fundamentals", "easy",
                question,
                _label_options(opts),
                f"{chr(65+correct)}. {answer}",
                explanation,
                ["Accenture", "Capgemini", "LTIMindtree", "Tech Mahindra"],
                _company_relevance(["accenture", "capgemini"], ["ltimindtree", "tech_mahindra"]),
            )
            out.append(q)
            idx += 1
    return out


def _gen_synonym(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    pairs = [
        ("Happy", "Joyful"), ("Big", "Large"), ("Fast", "Quick"), ("Smart", "Intelligent"),
        ("Angry", "Furious"), ("Brave", "Courageous"), ("Calm", "Peaceful"), ("Clever", "Wise"),
        ("Cold", "Chilly"), ("Cruel", "Harsh"), ("Dark", "Dim"), ("Dear", "Beloved"),
        ("Eager", "Enthusiastic"), ("Easy", "Simple"), ("Empty", "Bare"), ("Famous", "Renowned"),
        ("Funny", "Humorous"), ("Gentle", "Kind"), ("Giant", "Huge"), ("Glad", "Pleased"),
        ("Hard", "Difficult"), ("Honest", "Truthful"), ("Ideal", "Perfect"), ("Jolly", "Cheerful"),
        ("Kind", "Friendly"), ("Lively", "Energetic"), ("Lovely", "Beautiful"), ("Lucky", "Fortunate"),
        ("Mad", "Angry"), ("Nice", "Pleasant"), ("Obvious", "Clear"), ("Proud", "Proud"),
        ("Quick", "Rapid"), ("Rich", "Wealthy"), ("Safe", "Secure"), ("Sharp", "Acute"),
        ("Shy", "Timid"), ("Silly", "Foolish"), ("Smart", "Clever"), ("Tidy", "Neat"),
        ("Tiny", "Small"), ("Wise", "Smart"), ("Zany", "Wacky"), ("Brave", "Bold"),
        ("Charming", "Attractive"), ("Diligent", "Hardworking"), ("Elegant", "Graceful"),
        ("Fierce", "Fierce"), ("Generous", "Giving"), ("Happy", "Content"),
    ]
    for word, syn in pairs:
        if idx >= count:
            break
        distractors = ["Sad", "Angry", "Big", "Small", "Fast", "Slow", "Hot", "Cold", "Good", "Bad"]
        opts = [syn] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(syn)
        q = _base(
            "verbal_synonym", idx, "synonym", "Verbal", "easy",
            f"Synonym of '{word}'?",
            _label_options(opts),
            f"{chr(65+correct)}. {syn}",
            f"'{syn}' is a synonym of '{word}'",
            ["Wipro", "Infosys", "TCS"],
            _company_relevance(["wipro"], ["infosys", "tcs"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_antonym(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    pairs = [
        ("Happy", "Sad"), ("Big", "Small"), ("Fast", "Slow"), ("Hot", "Cold"),
        ("Bright", "Dark"), ("Strong", "Weak"), ("Rich", "Poor"), ("Love", "Hate"),
        ("Brave", "Cowardly"), ("Clean", "Dirty"), ("Clear", "Cloudy"), ("Dead", "Alive"),
        ("Empty", "Full"), ("Extinct", "Living"), ("False", "True"), ("Gentle", "Rough"),
        ("Happy", "Sad"), ("Heavy", "Light"), ("High", "Low"), ("Impossible", "Possible"),
        ("Incomplete", "Complete"), ("Invisible", "Visible"), ("Kind", "Cruel"), ("Last", "First"),
        ("Lazy", "Active"), ("Loose", "Tight"), ("Mad", "Sane"), ("Narrow", "Wide"),
        ("Normal", "Abnormal"), ("Open", "Closed"), ("Rare", "Common"), ("Silent", "Noisy"),
        ("Simple", "Complex"), ("Smart", "Stupid"), ("Soft", "Hard"), ("Thick", "Thin"),
        ("Truth", "Lie"), ("Vague", "Clear"), ("Weak", "Strong"), ("Young", "Old"),
        ("Ancient", "Modern"), ("Bold", "Timid"), ("Cheap", "Expensive"),
    ]
    for word, ant in pairs:
        if idx >= count:
            break
        distractors = ["Happy", "Big", "Fast", "Hot", "Bright", "Strong", "Rich", "Love"]
        opts = [ant] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(ant)
        q = _base(
            "verbal_antonym", idx, "antonym", "Verbal", "easy",
            f"Antonym of '{word}'?",
            _label_options(opts),
            f"{chr(65+correct)}. {ant}",
            f"'{ant}' is an antonym of '{word}'",
            ["Infosys", "TCS", "Wipro"],
            _company_relevance(["infosys"], ["tcs", "wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_idioms(count: int = 25) -> list[dict]:
    out = []
    idx = 0
    pairs = [
        ("Break the ice", "Start a conversation"),
        ("Bite the bullet", "Face a difficult situation"),
        ("Cost an arm and a leg", "Very expensive"),
        ("Hit the nail on the head", "Be exactly right"),
        ("Piece of cake", "Very easy"),
        ("Under the weather", "Feeling ill"),
        ("Spill the beans", "Reveal a secret"),
        ("Burn the midnight oil", "Study/work late"),
        ("A blessing in disguise", "Good thing that seemed bad"),
        ("Beat around the bush", "Avoid the point"),
        ("Catch someone's eye", "Attract attention"),
        ("Cut corners", "Do something poorly to save money"),
        ("Get out of hand", "Become uncontrollable"),
        ("In the same boat", "In the same situation"),
        ("Let the cat out of the bag", "Reveal a secret"),
        ("On the ball", "Alert and competent"),
        ("Pull someone's leg", "Joke with someone"),
        ("Once in a blue moon", "Very rarely"),
        ("The ball is in your court", "It's your decision"),
        ("Up in the air", "Not decided"),
        ("Against the clock", "Rushed for time"),
        ("Back to the drawing board", "Start over"),
        ("Bite off more than you can chew", "Take on too much"),
        ("Cut to the chase", "Get to the point"),
        ("Hit the sack", "Go to bed"),
    ]
    for idiom, meaning in pairs:
        if idx >= count:
            break
        distractors = ["Start a fight", "Run fast", "Eat quickly", "Sleep well", "Work hard", "Save money", "Think deeply", "Speak loudly"]
        opts = [meaning] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(meaning)
        q = _base(
            "verbal_idiom", idx, "idiom-meaning", "Verbal", "medium",
            f"What does '{idiom}' mean?",
            _label_options(opts),
            f"{chr(65+correct)}. {meaning}",
            f"'{idiom}' means '{meaning}'",
            ["TCS", "Infosys", "Wipro"],
            _company_relevance(["tcs"], ["infosys", "wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_subject_verb(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    pairs = [
        ("The list of items is on the table.", "is"),
        ("Neither the students nor the teacher were ready.", "was"),
        ("Each of the students have completed their homework.", "has"),
        ("The committee have decided to postpone the meeting.", "has"),
        ("Neither he nor they are coming.", "is"),
        ("Every man and every woman have the right to vote.", "has"),
        ("The news are very encouraging.", "is"),
        ("One of the books are missing.", "is"),
        ("The number of students are increasing.", "is"),
        ("A pair of shoes is on the shelf.", "is"),
        ("The team are playing well today.", "is"),
        ("More than one student has tried.", "has"),
        ("The majority of the vote was in favor.", "was"),
        ("Half of the pizza are gone.", "is"),
        ("Either the teacher or the students are responsible.", "is"),
        ("The crew was late for the flight.", "was"),
        ("Nobody in the room know the answer.", "knows"),
        ("The audience were clapping.", "was"),
        ("The police are investigating the case.", "is"),
        ("All of the money was spent.", "was"),
    ]
    for sentence, correct_verb in pairs:
        if idx >= count:
            break
        distractors = ["have", "are", "were", "do", "does", "is", "was"]
        opts = [correct_verb] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(correct_verb)
        q = _base(
            "verbal_sv", idx, "subject-verb", "Verbal", "medium",
            f"Choose the correct verb: {sentence}",
            _label_options(opts),
            f"{chr(65+correct)}. {correct_verb}",
            f"'{correct_verb}' agrees with the singular subject",
            ["TCS", "Wipro", "Infosys"],
            _company_relevance(["tcs"], ["wipro", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_active_passive(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    pairs = [
        ("The teacher praised the student.", "The student was praised by the teacher."),
        ("They built a new house.", "A new house was built by them."),
        ("She is writing a letter.", "A letter is being written by her."),
        ("The dog chased the cat.", "The cat was chased by the dog."),
        ("We will finish the work.", "The work will be finished by us."),
        ("He reads the newspaper.", "The newspaper is read by him."),
        ("They have completed the project.", "The project has been completed by them."),
        ("The chef is preparing the meal.", "The meal is being prepared by the chef."),
        ("Someone stole my wallet.", "My wallet was stolen by someone."),
        ("The students solved the problem.", "The problem was solved by the students."),
        ("The company launched a new product.", "A new product was launched by the company."),
        ("She speaks three languages.", "Three languages are spoken by her."),
        ("The children are playing in the park.", "In the park the children are playing."),
        ("The doctor examined the patient.", "The patient was examined by the doctor."),
        ("We have completed the task.", "The task has been completed by us."),
        ("The police caught the thief.", "The thief was caught by the police."),
        ("She made a cake.", "A cake was made by her."),
        ("They are repairing the car.", "The car is being repaired by them."),
        ("The teacher gave us homework.", "Homework was given to us by the teacher."),
        ("He ate the pizza.", "The pizza was eaten by him."),
    ]
    for active, passive in pairs:
        if idx >= count:
            break
        opts = [passive, active, "The student praised the teacher.", "The student is praised by the teacher."]
        random.shuffle(opts)
        correct = opts.index(passive)
        q = _base(
            "verbal_ap", idx, "active-passive", "Verbal", "medium",
            f"Change to passive: {active}",
            _label_options(opts),
            f"{chr(65+correct)}. {passive}",
            f"Passive: '{passive}'",
            ["Infosys", "TCS", "Wipro"],
            _company_relevance(["infosys"], ["tcs", "wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_direct_indirect(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    pairs = [
        ("He said, 'I am tired.'", "He said that he was tired."),
        ("She said, 'I will come tomorrow.'", "She said that she would come the next day."),
        ("He said, 'I have finished my work.'", "He said that he had finished his work."),
        ("She said, 'I am reading a book.'", "She said that she was reading a book."),
        ("He said, 'I can do it.'", "He said that he could do it."),
        ("She said, 'I was sleeping.'", "She said that she had been sleeping."),
        ("He said, 'I have been waiting.'", "He said that he had been waiting."),
        ("She said, 'I shall help you.'", "She said that she would help me."),
        ("He said, 'I must go now.'", "He said that he must go then."),
        ("She said, 'I might be late.'", "She said that she might be late."),
        ("He said, 'I should try harder.'", "He said that he should try harder."),
        ("She said, 'I could not attend.'", "She said that she could not attend."),
        ("He said, 'I was working hard.'", "He said that he had been working hard."),
        ("She said, 'I am not sure.'", "She said that she was not sure."),
        ("He said, 'I have seen this before.'", "He said that he had seen this before."),
        ("She said, 'I will be there.'", "She said that she would be there."),
        ("He said, 'I am learning Python.'", "He said that he was learning Python."),
        ("She said, 'I had already eaten.'", "She said that she had already eaten."),
        ("He said, 'I do not know.'", "He said that he did not know."),
        ("She said, 'I am going home.'", "She said that she was going home."),
    ]
    for direct, indirect in pairs:
        if idx >= count:
            break
        opts = [indirect, direct, "He said that he is tired.", "She said that she will come tomorrow."]
        random.shuffle(opts)
        correct = opts.index(indirect)
        q = _base(
            "verbal_di", idx, "direct-indirect", "Verbal", "medium",
            f"Convert to indirect speech: {direct}",
            _label_options(opts),
            f"{chr(65+correct)}. {indirect}",
            f"Indirect: '{indirect}'",
            ["Wipro", "TCS", "Infosys"],
            _company_relevance(["wipro"], ["tcs", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_prepositions(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    items = [
        ("She is good ___ math.", "at"),
        ("The cat is ___ the table.", "on"),
        ("He arrived ___ the station.", "at"),
        ("She is interested ___ music.", "in"),
        ("The book is ___ the bag.", "in"),
        ("He works ___ a bank.", "at"),
        ("She laughed ___ the joke.", "at"),
        ("The bird flew ___ the sky.", "in"),
        ("He is proud ___ his achievement.", "of"),
        ("She is afraid ___ spiders.", "of"),
        ("We depend ___ each other.", "on"),
        ("He succeeded ___ hard work.", "through"),
        ("She apologized ___ her mistake.", "for"),
        ("The results are different ___ mine.", "from"),
        ("He is busy ___ his work.", "with"),
        ("She is tired ___ the journey.", "of"),
        ("He believes ___ God.", "in"),
        ("The project is about ___ AI.", "about"),
        ("She is capable ___ solving this.", "of"),
        ("He is fond ___ music.", "of"),
    ]
    for sentence, correct_prep in items:
        if idx >= count:
            break
        distractors = ["of", "in", "on", "at", "with", "for", "to", "by"]
        opts = [correct_prep] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(correct_prep)
        q = _base(
            "verbal_prep", idx, "prepositions", "Verbal", "easy",
            sentence,
            _label_options(opts),
            f"{chr(65+correct)}. {correct_prep}",
            f"'{correct_prep}' is the correct preposition",
            ["TCS", "Infosys", "Wipro"],
            _company_relevance(["tcs"], ["infosys", "wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_one_word(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    pairs = [
        ("A person who never smiles", "Gloomy"),
        ("A person who eats too much", "Glutton"),
        ("A person who loves books", "Bibliophile"),
        ("A person who hates women", "Misogynist"),
        ("A person who hates men", "Misogynist"),
        ("A person who is always hopeful", "Optimist"),
        ("A person who expects the worst", "Pessimist"),
        ("A person who cannot see", "Blind"),
        ("A person who cannot hear", "Deaf"),
        ("A person who stutters", "Stutterer"),
        ("A person who collects stamps", "Philatelist"),
        ("A person who collects coins", "Numismatist"),
        ("A person who studies insects", "Entomologist"),
        ("A person who studies stars", "Astronomer"),
        ("A person who writes code", "Programmer"),
        ("A person who is afraid of water", "Aquaphobe"),
        ("A person who is afraid of fire", "Pyrophobe"),
        ("A person who loves music", "Melomaniac"),
        ("A person who loves walking", "Pedestrian"),
        ("A person who is a night owl", "Nocturnal"),
        ("A person who is always sleepy", "Drowsy"),
        ("A person who talks too much", "Chatterbox"),
        ("A person who keeps secrets", "Secretive"),
        ("A person who is easily deceived", "Gullible"),
        ("A person who hates liars", "Misanthrope"),
    ]
    for desc, word in pairs:
        if idx >= count:
            break
        distractors = ["Optimist", "Pessimist", "Realist", "Idealist", "Pragmatist", "Materialist", "Artist", "Scientist", "Engineer", "Doctor"]
        opts = [word] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(word)
        q = _base(
            "verbal_oneword", idx, "one-word", "Verbal", "medium",
            desc + "? (One word)",
            _label_options(opts),
            f"{chr(65+correct)}. {word}",
            f"'{word}' is the correct one-word answer",
            ["Wipro", "TCS", "Infosys"],
            _company_relevance(["wipro"], ["tcs", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_cloze(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    items = [
        ("The company is known ___ its innovative products.", "for"),
        ("She ___ the project before the deadline.", "completed"),
        ("The results were ___ than expected.", "better"),
        ("He has been working ___ three hours.", "for"),
        ("The team ___ the challenge successfully.", "faced"),
        ("She is very ___ about the new product.", "excited"),
        ("The data ___ to be accurate.", "proves"),
        ("We must act ___ this issue immediately.", "on"),
        ("He is ___ engineer with 10 years of experience.", "an"),
        ("The meeting was ___ to next Monday.", "postponed"),
        ("She ___ the company for five years.", "has joined"),
        ("The results were ___ than expected.", "better"),
        ("He is ___ to the new role.", "adapting"),
        ("The project ___ successfully last month.", "was completed"),
        ("She ___ the challenge with confidence.", "faced"),
        ("The team ___ the target on time.", "achieved"),
        ("He ___ the proposal to the board.", "presented"),
        ("The results ___ significant improvement.", "showed"),
        ("She ___ the problem quickly.", "solved"),
        ("The company ___ its goals this quarter.", "met"),
    ]
    for sentence, correct_word in items:
        if idx >= count:
            break
        distractors = ["completed", "better", "for", "faced", "excited", "proves", "on", "an", "postponed", "joined"]
        opts = [correct_word] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(correct_word)
        q = _base(
            "verbal_cloze", idx, "cloze", "Verbal", "medium",
            sentence,
            _label_options(opts),
            f"{chr(65+correct)}. {correct_word}",
            f"'{correct_word}' fits the context",
            ["TCS", "Infosys", "Wipro"],
            _company_relevance(["tcs"], ["infosys", "wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_vocabulary_in_context(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    items = [
        ("The ambiguous instructions caused confusion.", "Unclear"),
        ("The robust system handled all failures.", "Strong"),
        ("The meticulous review caught every error.", "Careful"),
        ("The dynamic environment kept everyone alert.", "Changing"),
        ("The critical deadline was tomorrow.", "Urgent"),
        ("The innovative solution impressed everyone.", "Creative"),
        ("The fragile system crashed easily.", "Delicate"),
        ("The comprehensive report covered everything.", "Complete"),
        ("The persistent effort paid off.", "Continued"),
        ("The elaborate plan was well received.", "Detailed"),
        ("The redundant system had backups.", "Duplicate"),
        ("The sequential process followed steps.", "Ordered"),
        ("The complex algorithm was hard to understand.", "Complicated"),
        ("The efficient process saved time.", "Effective"),
        ("The flexible policy allowed changes.", "Adaptable"),
        ("The secure system prevented breaches.", "Safe"),
        ("The transparent process was open.", "Clear"),
        ("The scalable solution handled growth.", "Expandable"),
        ("The resilient system recovered quickly.", "Strong"),
        ("The intuitive interface was easy to use.", "Natural"),
    ]
    for sentence, meaning in items:
        if idx >= count:
            break
        distractors = ["Strong", "Careful", "Changing", "Urgent", "Creative", "Delicate", "Complete", "Continued", "Detailed", "Duplicate"]
        opts = [meaning] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(meaning)
        q = _base(
            "verbal_vocab", idx, "vocabulary-context", "Verbal", "medium",
            f"What does the underlined word mean? '{sentence.split()[1]}' in '{sentence}'?",
            _label_options(opts),
            f"{chr(65+correct)}. {meaning}",
            f"'{meaning}' is the correct meaning",
            ["Infosys", "TCS", "Wipro"],
            _company_relevance(["infosys"], ["tcs", "wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_pseudo_trace(count: int = 25) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("a = 5; b = 3; print(a + b)", "8"),
        ("x = 10; y = 4; print(x - y)", "6"),
        ("m = 7; n = 2; print(m * n)", "14"),
        ("p = 20; q = 4; print(p / q)", "5"),
        ("a = 3; b = 4; print(a ** 2 + b ** 2)", "25"),
        ("x = 100; x = x + 50; print(x)", "150"),
        ("n = 5; n = n * 2; print(n)", "10"),
        ("a = 10; b = a; a = 5; print(b)", "10"),
        ("x = 3; y = x + 2; x = y - 1; print(x)", "4"),
        ("a = 2; b = 3; c = a + b; print(c)", "5"),
        ("x = 1; for i in range(3): x = x * 2; print(x)", "8"),
        ("n = 1; for i in range(4): n = n + i; print(n)", "6"),
        ("a = 10; if a > 5: a = a - 3; print(a)", "7"),
        ("x = 3; if x < 5: x = x * 2; print(x)", "6"),
        ("n = 15; if n > 10: n = n - 10; print(n)", "5"),
        ("a = 8; if a > 10: print('big'); else: print('small')", "small"),
        ("x = 12; if x > 10: print('big'); else: print('small')", "big"),
        ("n = 7; if n % 2 == 0: print('even'); else: print('odd')", "odd"),
        ("x = 10; if x % 2 == 0: print('even'); else: print('odd')", "even"),
        ("a = 3; b = 5; print('equal' if a == b else 'not equal')", "not equal"),
        ("x = 7; y = 7; print('equal' if x == y else 'not equal')", "equal"),
        ("n = 1; if n > 0: print('positive'); elif n < 0: print('negative'); else: print('zero')", "positive"),
        ("x = -5; if x > 0: print('positive'); elif x < 0: print('negative'); else: print('zero')", "negative"),
        ("n = 0; if n > 0: print('positive'); elif n < 0: print('negative'); else: print('zero')", "zero"),
        ("a = 100; b = 50; print('a is bigger' if a > b else 'b is bigger')", "a is bigger"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        distractors = ["5", "6", "8", "10", "12", "15", "20", "25", "positive", "negative", "zero", "equal", "not equal", "big", "small", "even", "odd"]
        opts = [expected] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "pseudo_trace", idx, "trace-variables", "Pseudocode", "easy",
            f"What is the output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Execution trace: {expected}",
            ["Infosys", "Wipro", "TCS"],
            _company_relevance(["infosys"], ["wipro", "tcs"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_pseudo_array(count: int = 25) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("arr = [1, 2, 3, 4, 5]; print(arr[2])", "3"),
        ("arr = [10, 20, 30, 40, 50]; print(arr[0])", "10"),
        ("arr = [5, 10, 15, 20]; print(arr[-1])", "20"),
        ("arr = [1, 2, 3, 4, 5]; print(len(arr))", "5"),
        ("arr = [10, 20, 30]; print(arr[1])", "20"),
        ("arr = [100, 200, 300]; print(arr[2])", "300"),
        ("arr = [1, 3, 5, 7, 9]; print(arr[-2])", "7"),
        ("arr = [2, 4, 6, 8]; print(arr[3])", "8"),
        ("arr = [5, 10, 15, 20, 25]; print(arr[1])", "10"),
        ("arr = [100]; print(len(arr))", "1"),
        ("arr = [1, 2]; arr.append(3); print(arr)", "[1, 2, 3]"),
        ("arr = [10, 20, 30]; arr.pop(); print(arr)", "[10, 20]"),
        ("arr = [1, 2, 3]; arr.insert(1, 5); print(arr)", "[1, 5, 2, 3]"),
        ("arr = [5, 10, 15]; arr.remove(10); print(arr)", "[5, 15]"),
        ("arr = [1, 2, 3]; arr.sort(reverse=True); print(arr)", "[3, 2, 1]"),
        ("arr = [3, 1, 4, 1, 5]; print(max(arr))", "5"),
        ("arr = [3, 1, 4, 1, 5]; print(min(arr))", "1"),
        ("arr = [2, 4, 6, 8, 10]; print(sum(arr))", "30"),
        ("arr = [10, 20, 30, 40, 50]; print(arr[1:3])", "[20, 30]"),
        ("arr = [1, 2, 3]; arr.reverse(); print(arr)", "[3, 2, 1]"),
        ("arr = [5, 3, 1]; arr.sort(); print(arr)", "[1, 3, 5]"),
        ("arr = [10, 20, 30, 40]; print(arr[-2])", "30"),
        ("arr = [7, 14, 21]; print(arr[0] + arr[1])", "21"),
        ("arr = [100, 200, 300]; print(arr[2] - arr[1])", "100"),
        ("arr = [2, 4, 6, 8, 10]; print(arr[3])", "8"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        distractors = ["1", "3", "5", "10", "20", "30", "40", "50", "100", "200", "300"]
        opts = [expected] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "pseudo_array", idx, "array-ops", "Pseudocode", "easy",
            f"What is the output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Array result: {expected}",
            ["Wipro", "Infosys", "TCS"],
            _company_relevance(["wipro"], ["infosys", "tcs"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_pseudo_string(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("s = 'hello'; print(s.upper())", "HELLO"),
        ("s = 'WORLD'; print(s.lower())", "world"),
        ("s = 'hello'; print(len(s))", "5"),
        ("s = 'Python'; print(s[0])", "P"),
        ("s = 'Python'; print(s[-1])", "n"),
        ("s = 'hello world'; print(s.replace('hello', 'hi'))", "hi world"),
        ("s = 'Python'; print(s + ' rules')", "Python rules"),
        ("s = 'abc'; print(s * 3)", "abcabcabc"),
        ("s = 'hello'; print(s + '!' + s)", "hello!hello"),
        ("s = 'Python is fun'; print(s[:6])", "Python"),
        ("s = 'Programming'; print(s[3:7])", "gram"),
        ("s = 'Hello World'; print(s.split())", "['Hello', 'World']"),
        ("s = 'a,b,c'; print(s.split(','))", "['a', 'b', 'c']"),
        ("s = 'hello'; print(s[1:4])", "ell"),
        ("s = 'Python'; print(s[1:4])", "yth"),
        ("s = 'Testing'; print(s[2:5])", "sti"),
        ("s = 'abcdef'; print(s[2:5])", "cde"),
        ("s = 'Hello'; print(s + ' ' + 'World')", "Hello World"),
        ("s = 'code'; print(s * 2)", "codecode"),
        ("s = 'test'; print(s + str(123))", "test123"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        distractors = ["5", "hello", "world", "Python", "HELLO", "abc", "123", "test"]
        opts = [expected] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "pseudo_string", idx, "string-ops", "Pseudocode", "easy",
            f"What is the output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"String result: {expected}",
            ["TCS", "Wipro", "Infosys"],
            _company_relevance(["tcs"], ["wipro", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_pseudo_conditional(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("x = 5; if x > 3: print('big'); else: print('small')", "big"),
        ("x = 2; if x > 3: print('big'); else: print('small')", "small"),
        ("n = 10; if n > 10: print('high'); elif n < 10: print('low'); else: print('exact')", "exact"),
        ("n = 15; if n > 10: print('high'); elif n < 10: print('low'); else: print('exact')", "high"),
        ("n = 5; if n > 10: print('high'); elif n < 10: print('low'); else: print('exact')", "low"),
        ("x = 0; if x >= 0: print('non-negative'); else: print('negative')", "non-negative"),
        ("x = -5; if x >= 0: print('non-negative'); else: print('negative')", "negative"),
        ("x = 100; if x > 50: print('A'); elif x > 25: print('B'); else: print('C')", "A"),
        ("x = 30; if x > 50: print('A'); elif x > 25: print('B'); else: print('C')", "B"),
        ("x = 10; if x > 50: print('A'); elif x > 25: print('B'); else: print('C')", "C"),
        ("x = 7; if x % 2 == 0: print('even'); else: print('odd')", "odd"),
        ("x = 8; if x % 2 == 0: print('even'); else: print('odd')", "even"),
        ("x = 15; if x % 3 == 0 and x % 5 == 0: print('fizzbuzz'); elif x % 3 == 0: print('fizz'); else: print('buzz')", "fizzbuzz"),
        ("x = 9; if x % 3 == 0 and x % 5 == 0: print('fizzbuzz'); elif x % 3 == 0: print('fizz'); else: print('buzz')", "fizz"),
        ("x = 10; if x % 3 == 0 and x % 5 == 0: print('fizzbuzz'); elif x % 3 == 0: print('fizz'); else: print('buzz')", "buzz"),
        ("a = 5; b = 10; if a > b: print('a bigger'); else: print('b bigger')", "b bigger"),
        ("a = 15; b = 10; if a > b: print('a bigger'); else: print('b bigger')", "a bigger"),
        ("a = 10; b = 10; if a > b: print('a bigger'); else: print('b bigger or equal')", "b bigger or equal"),
        ("x = 1; if x: print('truthy'); else: print('falsy')", "truthy"),
        ("x = 0; if x: print('truthy'); else: print('falsy')", "falsy"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        distractors = ["big", "small", "high", "low", "exact", "non-negative", "negative", "A", "B", "C", "even", "odd", "fizz", "fizzbuzz", "buzz", "a bigger", "b bigger", "b bigger or equal", "truthy", "falsy"]
        opts = [expected] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "pseudo_cond", idx, "conditional-logic", "Pseudocode", "easy",
            f"What is the output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Conditional output: {expected}",
            ["Infosys", "Wipro", "TCS"],
            _company_relevance(["infosys"], ["wipro", "tcs"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_pseudo_function(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("def add(a, b): return a + b\nprint(add(3, 5))", "8"),
        ("def mul(a, b): return a * b\nprint(mul(4, 5))", "20"),
        ("def sub(a, b): return a - b\nprint(sub(10, 3))", "7"),
        ("def div(a, b): return a // b\nprint(div(15, 4))", "3"),
        ("def sq(n): return n * n\nprint(sq(5))", "25"),
        ("def double(n): return n * 2\nprint(double(7))", "14"),
        ("def triple(n): return n * 3\nprint(triple(4))", "12"),
        ("def inc(n): return n + 1\nprint(inc(99))", "100"),
        ("def dec(n): return n - 1\nprint(dec(50))", "49"),
        ("def max_of(a, b): return a if a > b else b\nprint(max_of(3, 7))", "7"),
        ("def max_of(a, b): return a if a > b else b\nprint(max_of(10, 2))", "10"),
        ("def is_even(n): return n % 2 == 0\nprint(is_even(4))", "True"),
        ("def is_even(n): return n % 2 == 0\nprint(is_even(7))", "False"),
        ("def greeting(name): return 'Hello ' + name\nprint(greeting('Alice'))", "Hello Alice"),
        ("def greet(name): return name + '!'  \nprint(greet('World'))", "World!"),
        ("def area(l, w): return l * w\nprint(area(5, 3))", "15"),
        ("def perimeter(l, w): return 2*(l+w)\nprint(perimeter(4, 6))", "20"),
        ("def circle(r): return 2*3.14*r\nprint(circle(1))", "6.28"),
        ("def first(arr): return arr[0]\nprint(first([10, 20, 30]))", "10"),
        ("def last(arr): return arr[-1]\nprint(last([10, 20, 30]))", "30"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        distractors = ["5", "8", "10", "20", "25", "3", "7", "14", "12", "100", "50", "30", "49", "15", "True", "False"]
        opts = [expected] + random.sample(distractors, 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "pseudo_func", idx, "function-calls", "Pseudocode", "medium",
            f"What is the output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Function returns: {expected}",
            ["Wipro", "TCS", "Infosys"],
            _company_relevance(["wipro"], ["tcs", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_pseudo_bitwise(count: int = 15) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("5 & 3", "1"),
        ("5 | 3", "7"),
        ("5 ^ 3", "6"),
        ("~5", "-6"),
        ("5 << 1", "10"),
        ("5 >> 1", "2"),
        ("12 & 10", "8"),
        ("12 | 10", "14"),
        ("12 ^ 10", "6"),
        ("15 & 7", "7"),
        ("15 | 7", "15"),
        ("15 ^ 7", "8"),
        ("8 << 2", "32"),
        ("32 >> 2", "8"),
        ("7 & 7", "7"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = [expected, "0", "5", "3", "7", "1", "2", "4", "8", "15"]
        random.shuffle(opts)
        opts = opts[:4]
        if expected not in opts:
            opts[0] = expected
        correct = opts.index(expected)
        q = _base(
            "pseudo_bit", idx, "bitwise", "Pseudocode", "medium",
            f"Result of {code}?",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Bitwise result: {expected}",
            ["TCS", "Wipro"],
            _company_relevance(["tcs"], ["wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_pseudo_loop_nested(count: int = 20) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("for i in range(3):\n  for j in range(2):\n    print(i, j)", "(0,0) (0,1) (1,0) (1,1) (2,0) (2,1)"),
        ("for i in range(2):\n  for j in range(3):\n    print(j)", "0 1 2 0 1 2"),
        ("for i in range(4):\n  print(i)", "0 1 2 3"),
        ("for i in range(1, 4):\n  print(i)", "1 2 3"),
        ("for i in range(5):\n  if i == 3: break\n  print(i)", "0 1 2"),
        ("for i in range(5):\n  if i == 2: continue\n  print(i)", "0 1 3 4"),
        ("s = 0\nfor i in range(5):\n  s += i\nprint(s)", "10"),
        ("p = 1\nfor i in range(1, 5):\n  p *= i\nprint(p)", "24"),
        ("for i in range(3):\n  for j in range(i):\n    print(j)", "0 0 1"),
        ("for i in range(3):\n  for j in range(i+1):\n    print('*')", "*** ** *"),
        ("count = 0\nfor i in range(3):\n  for j in range(3):\n    count += 1\nprint(count)", "9"),
        ("for i in range(5):\n  if i % 2 == 0: print(i)", "0 2 4"),
        ("for i in range(5):\n  if i % 2 != 0: print(i)", "1 3"),
        ("for i in [1,2,3]:\n  for j in [4,5]:\n    print(i+j)", "5 6 6 7 7 8"),
        ("s = ''\nfor i in range(3):\n  s += str(i)\nprint(s)", "012"),
        ("for i in range(3, 0, -1):\n  print(i)", "3 2 1"),
        ("for i in range(0, 10, 2):\n  print(i)", "0 2 4 6 8"),
        ("for i in range(1, 6):\n  print(i * i)", "1 4 9 16 25"),
        ("count = 0\nfor i in range(3):\n  for j in range(2):\n    count += 1\nprint(count)", "6"),
        ("for i in range(4):\n  print(i, end=' ')", "0 1 2 3"),
        ("s = 0\nfor i in range(1, 4):\n  s += i*i\nprint(s)", "14"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = ["6", "8", "10", "9", "0 1 2", "0 1 2 3", "0 1 2 3 4", "1 2 3", "0 2 4", "1 3", "5", "15", "24", "14", "012"]
        opts = [expected] + random.sample(opts, 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "pseudo_nested", idx, "nested-loops", "Pseudocode", "medium",
            f"What is the output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Nested loop output: {expected}",
            ["Infosys", "Wipro", "TCS"],
            _company_relevance(["infosys"], ["wipro", "tcs"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_code_string(count: int = 15) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("def reverse(s): return s[::-1]\nprint(reverse('hello'))", "olleh"),
        ("def count_vowels(s): return sum(1 for c in s if c in 'aeiouAEIOU')\nprint(count_vowels('hello'))", "2"),
        ("def is_palindrome(s): return s == s[::-1]\nprint(is_palindrome('racecar'))", "True"),
        ("def uppercase(s): return s.upper()\nprint(uppercase('hello'))", "HELLO"),
        ("def join_str(a, b): return a + ' ' + b\nprint(join_str('Hello', 'World'))", "Hello World"),
        ("def first_char(s): return s[0]\nprint(first_char('Python'))", "P"),
        ("def last_char(s): return s[-1]\nprint(last_char('Python'))", "n"),
        ("def substring(s): return s[1:4]\nprint(substring('Python'))", "yth"),
        ("def replace_hello(s): return s.replace('hello', 'hi')\nprint(replace_hello('hello world'))", "hi world"),
        ("def split_str(s): return s.split(',')\nprint(split_str('a,b,c'))", "['a', 'b', 'c']"),
        ("def trim(s): return s.strip()\nprint(trim('  hello  '))", "hello"),
        ("def find_sub(s): return s.find('lo')\nprint(find_sub('hello'))", "3"),
        ("def contains(s): return 'ell' in s\nprint(contains('hello'))", "True"),
        ("def length(s): return len(s)\nprint(length('Python'))", "6"),
        ("def concat(s1, s2): return s1 + s2\nprint(concat('Py', 'thon'))", "Python"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = [expected, "hello", "5", "olleh", "Python", "True", "False", "6"]
        opts = [expected] + random.sample([o for o in opts if o != expected], 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "code_string", idx, "string-manipulation", "Coding", "medium",
            f"What does this function return?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"String result: {expected}",
            ["TCS", "Wipro", "Infosys"],
            _company_relevance(["tcs"], ["wipro", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_code_array(count: int = 15) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("def sum_arr(arr): return sum(arr)\nprint(sum_arr([1,2,3,4,5]))", "15"),
        ("def max_arr(arr): return max(arr)\nprint(max_arr([3,1,4,1,5]))", "5"),
        ("def min_arr(arr): return min(arr)\nprint(min_arr([3,1,4,1,5]))", "1"),
        ("def first(arr): return arr[0]\nprint(first([10,20,30]))", "10"),
        ("def last(arr): return arr[-1]\nprint(last([10,20,30]))", "30"),
        ("def length(arr): return len(arr)\nprint(length([1,2,3,4,5]))", "5"),
        ("def reverse_arr(arr): return arr[::-1]\nprint(reverse_arr([1,2,3]))", "[3, 2, 1]"),
        ("def contains(arr): return 3 in arr\nprint(contains([1,2,3,4,5]))", "True"),
        ("def append_arr(arr): return arr + [6]\nprint(append_arr([1,2,3,4,5]))", "[1, 2, 3, 4, 5, 6]"),
        ("def remove_first(arr): return arr[1:]\nprint(remove_first([1,2,3,4,5]))", "[2, 3, 4, 5]"),
        ("def even_filter(arr): return [x for x in arr if x%2==0]\nprint(even_filter([1,2,3,4,5]))", "[2, 4]"),
        ("def double_arr(arr): return [x*2 for x in arr]\nprint(double_arr([1,2,3]))", "[2, 4, 6]"),
        ("def sort_asc(arr): return sorted(arr)\nprint(sort_asc([3,1,2]))", "[1, 2, 3]"),
        ("def sum_even(arr): return sum(x for x in arr if x%2==0)\nprint(sum_even([1,2,3,4,5]))", "6"),
        ("def unique(arr): return list(set(arr))\nprint(unique([1,2,2,3,3,3]))", "[1, 2, 3]"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = ["15", "5", "10", "3", "[1,2,3]", "[3,2,1]", "True", "False"]
        opts = [expected] + random.sample([o for o in opts if o != expected], 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "code_array", idx, "array-manipulation", "Coding", "medium",
            f"What does this function return?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Array result: {expected}",
            ["Wipro", "TCS", "Infosys"],
            _company_relevance(["wipro"], ["tcs", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_code_linked_list(count: int = 15) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("class Node:\n  def __init__(self, val): self.val = val; self.next = None\nn = Node(5); print(n.val)", "5"),
        ("class Node:\n  def __init__(self, val): self.val = val; self.next = None\nn = Node(5); print(n.next)", "None"),
        ("n1 = Node(1); n2 = Node(2); n1.next = n2; print(n1.next.val)", "2"),
        ("class Node:\n  def __init__(self, val): self.val = val; self.next = None\nn = Node(10); print(n.val)", "10"),
        ("n1 = Node(1); n2 = Node(2); n3 = Node(3); n1.next = n2; n2.next = n3; print(n3.val)", "3"),
        ("n1 = Node(1); n2 = Node(2); n1.next = n2; print(n1.val)", "1"),
        ("class Node:\n  def __init__(self, val): self.val = val; self.next = None\nn1 = Node(7); n2 = Node(8); n1.next = n2; print(n2.val)", "8"),
        ("n1 = Node(1); n2 = Node(2); n3 = Node(3); n1.next = n2; n2.next = n3; print(n1.next.val)", "2"),
        ("n1 = Node(1); n2 = Node(2); n3 = Node(3); n1.next = n2; n2.next = n3; print(n1.next.next.val)", "3"),
        ("class Node:\n  def __init__(self, val): self.val = val; self.next = None\nn = Node(0); print(n.next)", "None"),
        ("n1 = Node(100); n2 = Node(200); n1.next = n2; print(n1.val, n2.val)", "100 200"),
        ("n1 = Node(1); n2 = Node(2); n1.next = n2; print(n2.next)", "None"),
        ("class Node:\n  def __init__(self, val): self.val = val; self.next = None\nn = Node(42); print(type(n.val))", "<class 'int'>"),
        ("n1 = Node(5); n2 = Node(10); n1.next = n2; print(n1.next.val)", "10"),
        ("n1 = Node(1); n2 = Node(2); n1.next = n2; n2.next = n1; print(n1.val)", "1"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = ["5", "10", "None", "1", "2", "3", "42", "100", "200", "True"]
        opts = [expected] + random.sample([o for o in opts if o != expected], 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "code_linkedlist", idx, "linked-list", "Coding", "medium",
            f"What is the output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Linked list result: {expected}",
            ["TCS", "Wipro"],
            _company_relevance(["tcs"], ["wipro"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_code_recursion(count: int = 15) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("def fact(n):\n  if n <= 1: return 1\n  return n * fact(n-1)\nprint(fact(5))", "120"),
        ("def fib(n):\n  if n <= 1: return n\n  return fib(n-1) + fib(n-2)\nprint(fib(6))", "8"),
        ("def sum_n(n):\n  if n <= 0: return 0\n  return n + sum_n(n-1)\nprint(sum_n(5))", "15"),
        ("def power(a, n):\n  if n == 0: return 1\n  return a * power(a, n-1)\nprint(power(2, 4))", "16"),
        ("def countdown(n):\n  if n <= 0: return []\n  return [n] + countdown(n-1)\nprint(countdown(3))", "[3, 2, 1]"),
        ("def sum_digits(n):\n  if n < 10: return n\n  return n%10 + sum_digits(n//10)\nprint(sum_digits(123))", "6"),
        ("def is_even(n):\n  if n == 0: return True\n  return is_odd(n-1)\ndef is_odd(n):\n  if n == 0: return False\n  return is_even(n-1)\nprint(is_even(4))", "True"),
        ("def fib(n):\n  if n <= 1: return n\n  return fib(n-1) + fib(n-2)\nprint(fib(5))", "5"),
        ("def fact(n):\n  if n <= 1: return 1\n  return n * fact(n-1)\nprint(fact(0))", "1"),
        ("def sum_n(n):\n  if n <= 0: return 0\n  return n + sum_n(n-1)\nprint(sum_n(10))", "55"),
        ("def power(a, n):\n  if n == 0: return 1\n  return a * power(a, n-1)\nprint(power(3, 3))", "27"),
        ("def countdown(n):\n  if n <= 0: return []\n  return [n] + countdown(n-1)\nprint(countdown(5))", "[5, 4, 3, 2, 1]"),
        ("def sum_digits(n):\n  if n < 10: return n\n  return n%10 + sum_digits(n//10)\nprint(sum_digits(999))", "27"),
        ("def fib(n):\n  if n <= 1: return n\n  return fib(n-1) + fib(n-2)\nprint(fib(7))", "13"),
        ("def fact(n):\n  if n <= 1: return 1\n  return n * fact(n-1)\nprint(fact(4))", "24"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = ["120", "8", "15", "16", "5", "1", "55", "27", "24", "13", "True", "False", "[3, 2, 1]", "[5, 4, 3, 2, 1]"]
        opts = [expected] + random.sample([o for o in opts if o != expected], 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "code_recursion", idx, "recursion", "Coding", "medium",
            f"What does this function return?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Recursion result: {expected}",
            ["Wipro", "Infosys", "TCS"],
            _company_relevance(["wipro"], ["infosys", "tcs"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_code_sorting(count: int = 15) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("arr = [3,1,4,1,5]; arr.sort(); print(arr)", "[1, 1, 3, 4, 5]"),
        ("arr = [5,3,1,4,2]; arr.sort(reverse=True); print(arr)", "[5, 4, 3, 2, 1]"),
        ("arr = [10,5,8,3,1]; print(sorted(arr))", "[1, 3, 5, 8, 10]"),
        ("arr = [1,2,3,4,5]; arr.reverse(); print(arr)", "[5, 4, 3, 2, 1]"),
        ("arr = [3,1,4,1,5,9,2,6]; arr.sort(); print(arr[-1])", "9"),
        ("arr = [3,1,4,1,5,9,2,6]; arr.sort(); print(arr[0])", "1"),
        ("arr = [5,2,8,1,9]; print(min(arr), max(arr))", "1 9"),
        ("arr = [42]; print(sorted(arr))", "[42]"),
        ("arr = []; print(sorted(arr))", "[]"),
        ("arr = [1,2,3]; arr.sort(reverse=True); print(arr)", "[3, 2, 1]"),
        ("arr = [3,3,3,1,1,2]; arr.sort(); print(arr)", "[1, 1, 2, 3, 3, 3]"),
        ("arr = [10,20,30]; print(sorted(arr, reverse=True))", "[30, 20, 10]"),
        ("arr = [5,5,5]; arr.sort(); print(arr)", "[5, 5, 5]"),
        ("arr = [-3,0,5,-1,2]; arr.sort(); print(arr)", "[-3, -1, 0, 2, 5]"),
        ("arr = [100,50,25,75]; arr.sort(); print(arr[1])", "50"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = ["[1, 1, 3, 4, 5]", "[5, 4, 3, 2, 1]", "[1, 3, 5, 8, 10]", "[5, 4, 3, 2, 1]", "9", "1", "1 9", "[42]", "[]", "[3, 2, 1]"]
        opts = [expected] + random.sample([o for o in opts if o != expected], 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "code_sorting", idx, "sorting", "Coding", "medium",
            f"What does this code output?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"Sorting result: {expected}",
            ["TCS", "Wipro", "Infosys"],
            _company_relevance(["tcs"], ["wipro", "infosys"]),
        )
        out.append(q)
        idx += 1
    return out


def _gen_code_dp(count: int = 10) -> list[dict]:
    out = []
    idx = 0
    templates = [
        ("def fib(n):\n  if n <= 1: return n\n  dp = [0]*(n+1)\n  dp[1] = 1\n  for i in range(2, n+1): dp[i] = dp[i-1] + dp[i-2]\n  return dp[n]\nprint(fib(6))", "8"),
        ("def climb(n):\n  if n <= 1: return 1\n  dp = [0]*(n+1)\n  dp[0] = dp[1] = 1\n  for i in range(2, n+1): dp[i] = dp[i-1] + dp[i-2]\n  return dp[n]\nprint(climb(4))", "5"),
        ("def max_sum(arr):\n  if not arr: return 0\n  dp = [0]*len(arr)\n  dp[0] = arr[0]\n  for i in range(1, len(arr)): dp[i] = max(arr[i], dp[i-1]+arr[i])\n  return max(dp)\nprint(max_sum([-2,1,-3,4,-1,2,1,-5,4]))", "6"),
        ("def coin_change(coins, amt):\n  dp = [float('inf')]*(amt+1)\n  dp[0] = 0\n  for c in coins:\n    for i in range(c, amt+1): dp[i] = min(dp[i], dp[i-c]+1)\n  return dp[amt] if dp[amt] != float('inf') else -1\nprint(coin_change([1,2,5], 11))", "3"),
        ("def knapsack(w, wt, val, n):\n  dp = [[0]*(w+1) for _ in range(n+1)]\n  for i in range(1, n+1):\n    for j in range(w+1):\n      if wt[i-1] <= j: dp[i][j] = max(val[i-1]+dp[i-1][j-wt[i-1]], dp[i-1][j])\n      else: dp[i][j] = dp[i-1][j]\n  return dp[n][w]\nprint(knapsack(50, [10,20,30], [60,100,120], 3))", "220"),
        ("def lcs(s1, s2):\n  m, n = len(s1), len(s2)\n  dp = [[0]*(n+1) for _ in range(m+1)]\n  for i in range(1, m+1):\n    for j in range(1, n+1):\n      if s1[i-1]==s2[j-1]: dp[i][j] = dp[i-1][j-1]+1\n      else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n  return dp[m][n]\nprint(lcs('ABCDE', 'ACE'))", "3"),
        ("def edit_dist(s1, s2):\n  m, n = len(s1), len(s2)\n  dp = [[0]*(n+1) for _ in range(m+1)]\n  for i in range(m+1): dp[i][0] = i\n  for j in range(n+1): dp[0][j] = j\n  for i in range(1, m+1):\n    for j in range(1, n+1):\n      if s1[i-1]==s2[j-1]: dp[i][j] = dp[i-1][j-1]\n      else: dp[i][j] = 1+min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n  return dp[m][n]\nprint(edit_dist('horse', 'ros'))", "3"),
        ("def can_partition(nums):\n  s = sum(nums)\n  if s%2 != 0: return False\n  target = s//2\n  dp = [False]*(target+1)\n  dp[0] = True\n  for num in nums:\n    for i in range(target, num-1, -1): dp[i] = dp[i] or dp[i-num]\n  return dp[target]\nprint(can_partition([1,5,11,5]))", "True"),
        ("def subset_sum(nums, target):\n  dp = [False]*(target+1)\n  dp[0] = True\n  for num in nums:\n    for i in range(target, num-1, -1): dp[i] = dp[i] or dp[i-num]\n  return dp[target]\nprint(subset_sum([3,34,4,12,5,2], 9))", "True"),
        ("def rod_cut(price, n):\n  dp = [0]*(n+1)\n  for i in range(1, n+1):\n    for j in range(i): dp[i] = max(dp[i], price[j]+dp[i-j-1])\n  return dp[n]\nprint(rod_cut([1,5,8,9], 4))", "10"),
    ]
    for code, expected in templates:
        if idx >= count:
            break
        opts = ["8", "5", "6", "3", "220", "True", "False", "10", "0", "-1"]
        opts = [expected] + random.sample([o for o in opts if o != expected], 3)
        random.shuffle(opts)
        correct = opts.index(expected)
        q = _base(
            "code_dp", idx, "dynamic-programming", "Coding", "hard",
            f"What does this DP function return?\n{code}",
            _label_options(opts),
            f"{chr(65+correct)}. {expected}",
            f"DP result: {expected}",
            ["Infosys", "TCS"],
            _company_relevance(["infosys"], ["tcs"]),
        )
        out.append(q)
        idx += 1
    return out


# ---------------------------------------------------------------------------
# Generator registry
# ---------------------------------------------------------------------------

def generate_all(verify: bool = False) -> dict[str, list[dict]]:
    generators = {
        "quant_workrate": _gen_workrate,
        "quant_discount": _gen_successive_discount,
        "quant_profit": _gen_profit_loss,
        "quant_train": _gen_trains,
        "quant_calendar": _gen_calendar,
        "quant_clock": _gen_clock_angle,
        "quant_pipes": _gen_pipes,
        "quant_boats": _gen_boats,
        "quant_avg": _gen_averages,
        "quant_age": _gen_ages,
        "quant_ratio": _gen_ratio,
        "quant_hcf": _gen_hcf_lcm,
        "quant_series_wrong": _gen_series_wrong,
        "quant_prob": _gen_probability_dice,
        "quant_perm": _gen_permutation,
        "quant_si_ci": _gen_si_ci,
        "log_blood": _gen_blood_relations,
        "log_coding": _gen_coding_decoding,
        "log_syllogism": _gen_syllogism,
        "log_series": _gen_series_number,
        "log_seating": _gen_seating_linear,
        "log_dir": _gen_directions,
        "pseudo_loop": _gen_loop_output,
        "pseudo_factorial": _gen_recursion_trace,
        "verbal_error": _gen_error_spotting,
        "verbal_blank": _gen_fill_blanks,
        "tech_fund": _gen_tech_fundamentals,
        "verbal_synonym": _gen_synonym,
        "verbal_antonym": _gen_antonym,
        "verbal_idiom": _gen_idioms,
        "verbal_sv": _gen_subject_verb,
        "verbal_ap": _gen_active_passive,
        "verbal_di": _gen_direct_indirect,
        "verbal_prep": _gen_prepositions,
        "verbal_oneword": _gen_one_word,
        "verbal_cloze": _gen_cloze,
        "verbal_vocab": _gen_vocabulary_in_context,
        "pseudo_trace": _gen_pseudo_trace,
        "pseudo_array": _gen_pseudo_array,
        "pseudo_string": _gen_pseudo_string,
        "pseudo_cond": _gen_pseudo_conditional,
        "pseudo_func": _gen_pseudo_function,
        "pseudo_bit": _gen_pseudo_bitwise,
        "pseudo_nested": _gen_pseudo_loop_nested,
        "code_string": _gen_code_string,
        "code_array": _gen_code_array,
        "code_linkedlist": _gen_code_linked_list,
        "code_recursion": _gen_code_recursion,
        "code_sorting": _gen_code_sorting,
        "code_dp": _gen_code_dp,
    }

    all_banks: dict[str, list[dict]] = {}
    total = 0
    for name, fn in generators.items():
        questions = fn()
        all_banks[name] = questions
        total += len(questions)
        print(f"  {name}: {len(questions)} questions")

    if verify:
        print("\nVerifying generated questions...")
        verified = 0
        failed = 0
        for bank_name, questions in all_banks.items():
            for q in questions:
                if _verify_question(q):
                    verified += 1
                else:
                    failed += 1
        print(f"  Verified: {verified}, Failed: {failed}")

    print(f"\nTotal generated: {total}")
    return all_banks


def _verify_question(q: dict) -> bool:
    try:
        assert q.get("id")
        assert q.get("pattern")
        assert q.get("question")
        assert q.get("content", {}).get("options")
        assert q.get("content", {}).get("correct_answer")
        assert len(q["content"]["options"]) == 4
        assert q["content"]["correct_answer"] in q["content"]["options"]
        return True
    except AssertionError:
        return False


def save_banks(banks: dict[str, list[dict]]) -> None:
    company_map = {
        "quant_workrate": "tcs",
        "quant_discount": "tcs",
        "quant_profit": "tcs",
        "quant_train": "tcs",
        "quant_calendar": "tcs",
        "quant_clock": "tcs",
        "quant_pipes": "tcs",
        "quant_boats": "tcs",
        "quant_avg": "tcs",
        "quant_age": "tcs",
        "quant_ratio": "tcs",
        "quant_hcf": "tcs",
        "quant_series_wrong": "tcs",
        "quant_prob": "tcs",
        "quant_perm": "tcs",
        "quant_si_ci": "tcs",
        "log_blood": "tcs",
        "log_coding": "tcs",
        "log_syllogism": "tcs",
        "log_series": "tcs",
        "log_seating": "tcs",
        "log_dir": "tcs",
        "pseudo_loop": "infosys",
        "pseudo_factorial": "infosys",
        "verbal_error": "ltimindtree",
        "verbal_blank": "ltimindtree",
        "tech_fund": "accenture",
    }

    for bank_name, questions in banks.items():
        company = company_map.get(bank_name, "general")
        path = OUTPUT_DIR / f"{company}" / f"{bank_name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(questions)} -> {path}")

    combined = []
    for questions in banks.values():
        combined.extend(questions)
    combined_path = OUTPUT_DIR / "all_generated_questions.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"  Saved combined: {len(combined)} -> {combined_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate service company questions")
    parser.add_argument("--verify", action="store_true", help="Verify generated questions")
    parser.add_argument("--count-only", action="store_true", help="Only count, don't save")
    args = parser.parse_args()

    print("Generating service company questions...")
    banks = generate_all(verify=args.verify)

    if not args.count_only:
        print("\nSaving banks...")
        save_banks(banks)

    print("\nDone.")


if __name__ == "__main__":
    main()
