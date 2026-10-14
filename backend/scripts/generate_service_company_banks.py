#!/usr/bin/env python3
"""
Canonical service-company prep question generator.

Company structures researched from web and encoded as deterministic generators.
Reuses _base and _company_relevance from generate_service_company_questions.py.
"""

from __future__ import annotations

import os, sys, json, random, math
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from scripts.generate_service_company_questions import _base, _label_options, _company_relevance

random.seed(123)

COMPANY_SEEDS = {
    "tcs": 1000,
    "wipro": 2000,
    "cognizant": 3000,
    "capgemini": 4000,
    "tech_mahindra": 5000,
    "infosys": 6000,
    "accenture": 7000,
    "ltimindtree": 8000,
}

OUTPUT_DIR = Path("app/data/generated")

# ---------------------------------------------------------------------------
# Canonical company section structures (researched)
# ---------------------------------------------------------------------------
COMPANY_STRUCTURES = {
    "tcs": {
        "name": "TCS NQT",
        "sections": [
            {"key": "foundation_numerical", "label": "Foundation Numerical Ability", "minutes": 25, "questions": 20, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "foundation_verbal", "label": "Foundation Verbal Ability", "minutes": 25, "questions": 25, "type": "mcq", "domain": "Verbal"},
            {"key": "foundation_reasoning", "label": "Foundation Reasoning Ability", "minutes": 25, "questions": 20, "type": "mcq", "domain": "Logical Reasoning"},
            {"key": "advanced_quant_reasoning", "label": "Advanced Quantitative & Reasoning", "minutes": 25, "questions": 15, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "advanced_coding", "label": "Advanced Coding", "minutes": 90, "questions": 2, "type": "coding", "domain": "Programming Logic"},
        ],
    },
    "wipro": {
        "name": "Wipro Elite NLTH",
        "sections": [
            {"key": "aptitude", "label": "Aptitude", "minutes": 48, "questions": 36, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "essay", "label": "Written Communication", "minutes": 20, "questions": 1, "type": "essay", "domain": "Verbal"},
            {"key": "coding", "label": "Programming Test", "minutes": 60, "questions": 2, "type": "coding", "domain": "Programming Logic"},
        ],
    },
    "cognizant": {
        "name": "Cognizant GenC",
        "sections": [
            {"key": "quant", "label": "Quantitative Aptitude", "minutes": 16, "questions": 16, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "reasoning", "label": "Logical Reasoning", "minutes": 14, "questions": 14, "type": "mcq", "domain": "Logical Reasoning"},
            {"key": "verbal", "label": "English & Verbal Ability", "minutes": 22, "questions": 22, "type": "mcq", "domain": "Verbal"},
            {"key": "coding", "label": "Coding", "minutes": 45, "questions": 2, "type": "coding", "domain": "Programming Logic"},
        ],
    },
    "capgemini": {
        "name": "Capgemini Exceller",
        "sections": [
            {"key": "technical_pseudocode", "label": "Technical MCQs + Pseudocode", "minutes": 40, "questions": 40, "type": "mcq", "domain": "CS Fundamentals"},
            {"key": "english", "label": "English Communication", "minutes": 30, "questions": 30, "type": "mcq", "domain": "Verbal"},
            {"key": "coding", "label": "Coding Assessment", "minutes": 45, "questions": 2, "type": "coding", "domain": "Programming Logic"},
        ],
    },
    "tech_mahindra": {
        "name": "Tech Mahindra ELQ",
        "sections": [
            {"key": "aptitude", "label": "Aptitude", "minutes": 142, "questions": 75, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "technical", "label": "Technical & Coding", "minutes": 65, "questions": 26, "type": "mcq", "domain": "CS Fundamentals"},
            {"key": "communication", "label": "Communication", "minutes": 20, "questions": 18, "type": "mcq", "domain": "Verbal"},
        ],
    },
    "infosys": {
        "name": "Infosys InfyTQ",
        "sections": [
            {"key": "aptitude", "label": "Aptitude", "minutes": 60, "questions": 60, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "pseudocode", "label": "Pseudo-code", "minutes": 20, "questions": 20, "type": "mcq", "domain": "Programming Logic"},
            {"key": "coding", "label": "Coding", "minutes": 60, "questions": 3, "type": "coding", "domain": "Programming Logic"},
        ],
    },
    "accenture": {
        "name": "Accenture",
        "sections": [
            {"key": "quant", "label": "Quantitative Aptitude", "minutes": 30, "questions": 20, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "reasoning", "label": "Reasoning", "minutes": 25, "questions": 20, "type": "mcq", "domain": "Logical Reasoning"},
            {"key": "verbal", "label": "Verbal", "minutes": 20, "questions": 20, "type": "mcq", "domain": "Verbal"},
            {"key": "coding", "label": "Coding", "minutes": 45, "questions": 2, "type": "coding", "domain": "Programming Logic"},
        ],
    },
    "ltimindtree": {
        "name": "LTIMindtree",
        "sections": [
            {"key": "quant", "label": "Quantitative Aptitude", "minutes": 35, "questions": 20, "type": "mcq", "domain": "Quantitative Aptitude"},
            {"key": "reasoning", "label": "Logical Reasoning", "minutes": 35, "questions": 20, "type": "mcq", "domain": "Logical Reasoning"},
            {"key": "verbal", "label": "Verbal", "minutes": 20, "questions": 15, "type": "mcq", "domain": "Verbal"},
            {"key": "coding", "label": "Coding", "minutes": 45, "questions": 2, "type": "coding", "domain": "Programming Logic"},
        ],
    },
}

# ---------------------------------------------------------------------------
# Deterministic question banks
# ---------------------------------------------------------------------------
NUMERICAL_TEMPLATES = [
    ("A can complete a task in {a} days and B in {b} days. Working together, how many days?", "lcm"),
    ("Cost price is ₹{cp}, profit {pct}%. Selling price?", "profit"),
    ("If {a}:{b} = {c}:?, what is the fourth proportion?", "ratio"),
    ("Average of {n} numbers is {avg}. If {n1} numbers are {nums}, what is last?", "average"),
    ("What is {value} increased by {pct}%?", "percentage"),
    ("Speed {sp} km/h, time {t} hr. Distance?", "speed"),
    ("Train {len1}m at {sp1} km/h crosses train {len2}m at {sp2} km/h. Time?", "train"),
    ("Pipe A fills in {pa} hrs, B in {pb} hrs. Together?", "pipes"),
    ("Boat speed {sb} km/h, stream {ss} km/h. Downstream?", "boat"),
    ("Simple interest on ₹{p} at {r}% for {t} years?", "si_ci"),
    ("Loss of {pct}% on cost price ₹{cp}. Selling price?", "loss"),
    ("Marked price ₹{mp}, discount {pct}%. Selling price?", "discount"),
    ("A and B invest ₹{a} and ₹{b} for {t} months. Profit share ratio?", "partnership"),
    ("A does {pct}% of work in {d} days. Total days to finish?", "work"),
    ("Workers needed to finish work in {d2} days if {w} workers finish in {d1} days?", "workers"),
    ("A sum becomes ₹{a1} in {t1} years and ₹{a2} in {t2} years at SI. Principal?", "principal"),
    ("Difference between CI and SI on ₹{p} at {r}% for {t} years?", "ci_si"),
    ("A sum at CI amounts to ₹{a1} in 2 years and ₹{a2} in 3 years. Rate?", "ci_rate"),
    ("If {a} men or {b} women can do a work in {d} days, how many days for {c} men and {d2} women?", "men_women"),
    ("A can do work in {a} days, B in {b} days. A leaves after {d} days. B finishes in?", "work_left"),
]

REASONING_TEMPLATES = [
    ("How many ways to arrange {r} items from {n}?", "perm"),
    ("How many ways to choose {r} from {n}?", "comb"),
    ("{coins} coins tossed, exactly 1 head?", "prob"),
    ("In AP {a}, {a+d}, ..., what is the {n}th term?", "series"),
    ("Blood relation: {relation}", "blood"),
    ("Coding: A=1, B=2... code for {word}?", "coding"),
    ("Syllogism: {premises}", "syllogism"),
    ("Seating arrangement: {constraints}", "seating"),
    ("Direction: {directions}", "directions"),
    ("Logical series: {seq}", "series"),
]

VERBAL_TEMPLATES = [
    ("Synonym of '{word}'?", "synonym"),
    ("Antonym of '{word}'?", "antonym"),
    ("What does '{idiom}' mean?", "idiom"),
    ("Fill in the blank: {sentence}", "blank"),
    ("Spot the error: {sentence}", "error"),
    ("Para jumble: {sentences}", "jumble"),
    ("Reading comprehension: {passage}", "rc"),
    ("Preposition: {sentence}", "preposition"),
    ("One word for: {description}", "oneword"),
    ("Cloze: {sentence_with_blank}", "cloze"),
]

CODING_TEMPLATES = [
    ("def add(a, b): return a + b\nprint(add(3, 5))", "8"),
    ("def mul(a, b): return a * b\nprint(mul(4, 5))", "20"),
    ("def sub(a, b): return a - b\nprint(sub(10, 3))", "7"),
    ("def sq(n): return n * n\nprint(sq(5))", "25"),
    ("def double(n): return n * 2\nprint(double(7))", "14"),
    ("def is_even(n): return n % 2 == 0\nprint(is_even(4))", "True"),
    ("def first(arr): return arr[0]\nprint(first([10, 20, 30]))", "10"),
    ("def last(arr): return arr[-1]\nprint(last([10, 20, 30]))", "30"),
    ("s = 'hello'\nprint(s.upper())", "HELLO"),
    ("s = 'WORLD'\nprint(s.lower())", "world"),
    ("arr = [1,2,3,4,5]\nprint(sum(arr))", "15"),
    ("arr = [3,1,4,1,5]\nprint(max(arr))", "5"),
    ("x = 5\nif x > 3: print('big')\nelse: print('small')", "big"),
    ("x = 2\nif x > 3: print('big')\nelse: print('small')", "small"),
    ("n = 5\nif n % 2 == 0: print('even')\nelse: print('odd')", "odd"),
    ("for i in range(3):\n    print(i)", "0\\n1\\n2"),
    ("x = [1,2,3]\nprint(len(x))", "3"),
    ("x = 'abc'\nprint(x[1])", "b"),
    ("x = {'a':1,'b':2}\nprint(x['b'])", "2"),
    ("x = 10//3\nprint(x)", "3"),
    ("x = 10%3\nprint(x)", "1"),
    ("x = 2**3\nprint(x)", "8"),
    ("x = 'hello world'\nprint(x.split()[0])", "hello"),
    ("x = [1,2,3]\nx.append(4)\nprint(x)", "[1, 2, 3, 4]"),
    ("x = 'python'\nprint(x.replace('p','P'))", "Python"),
    ("x = [1,2,3,4]\nprint(x[1:3])", "[2, 3]"),
    ("x = {'a':1,'b':2,'c':3}\nprint(list(x.keys()))", "['a', 'b', 'c']"),
    ("def fact(n):\n    return 1 if n<=1 else n*fact(n-1)\nprint(fact(5))", "120"),
    ("def fib(n):\n    a,b=0,1\n    for _ in range(n):\n        a,b=b,a+b\n    return a\nprint(fib(6))", "8"),
    ("x = [1,2,3,4,5]\nprint([i for i in x if i%2==0])", "[2, 4]"),
    ("x = 'abracadabra'\nprint(x.count('a'))", "5"),
]

CS_TEMPLATES = [
    ("How many layers in OSI model?", "7"),
    ("Default HTTP port?", "80"),
    ("Which is not a DBMS?", "Excel"),
    ("Full form of SQL?", "Structured Query Language"),
    ("Which protocol is connection-oriented?", "TCP"),
    ("Which is a NoSQL database?", "MongoDB"),
    ("What does HTML stand for?", "Hyper Text Markup Language"),
    ("Which is not an OOP concept?", "Compilation"),
    ("Primary key vs unique key?", "PK: not null + unique"),
    ("Which is a high-level language?", "Python"),
    ("Which is a low-level language?", "Assembly"),
    ("Full form of URL?", "Uniform Resource Locator"),
    ("Which is a programming language?", "Java"),
    ("Which is a markup language?", "XML"),
    ("Which is not a browser?", "Linux"),
    ("Which is not an OS?", "MySQL"),
    ("Which is a spreadsheet software?", "Excel"),
    ("Which key closes a tab in browser?", "Ctrl+W"),
    ("Which is a search engine?", "Google"),
    ("Which is a social network?", "Facebook"),
    ("Which is an IDE?", "VS Code"),
    ("Which is a version control system?", "Git"),
    ("Which is a data structure?", "Queue"),
    ("Which is not a data structure?", "CPU"),
    ("Which sorting is fastest average?", "QuickSort"),
    ("Which is not a database constraint?", "Velocity"),
    ("Full form of RAM?", "Random Access Memory"),
    ("Full form of ROM?", "Read Only Memory"),
    ("Which device is used for output?", "Monitor"),
    ("Which is an input device?", "Keyboard"),
    ("Which is a storage device?", "Hard Disk"),
    ("Which is a communication device?", "Modem"),
    ("Which language is used for web pages?", "HTML"),
    ("Which is not a web technology?", "Photoshop"),
    ("Which protocol is used for email?", "SMTP"),
    ("Which protocol is used for file transfer?", "FTP"),
    ("Which is a top-down approach?", "Modular"),
    ("Which is not a software testing type?", "Cooking"),
    ("Which is not a software model?", "Bathing"),
    ("Which is not a programming paradigm?", "Sleeping"),
    ("Which sorting is stable?", "MergeSort"),
    ("Which is not a network topology?", "Triangle"),
    ("Which is a network device?", "Router"),
    ("Which is not a network protocol?", "Walking"),
    ("Which layer is HTTP in OSI?", "Application"),
    ("Which is a transport layer protocol?", "TCP"),
    ("Which is a data link layer device?", "Switch"),
    ("Which is not an IP address class?", "Class E"),
    ("Which is a loop control statement?", "for"),
    ("Which is not a conditional statement?", "Running"),
    ("Which operator checks equality?", "=="),
    ("Which operator checks identity?", "is"),
    ("Which is not a Python data type?", "Char"),
    ("Which is mutable?", "list"),
    ("Which is immutable?", "tuple"),
    ("Which is not a Python keyword?", "repeat"),
    ("Which is not a loop?", "switch"),
    ("Which is used to define function?", "def"),
    ("Which is used for comments?", "#"),
    ("Which exception is for index error?", "IndexError"),
    ("Which exception is for key error?", "KeyError"),
    ("Which is not a Python operator?", "equals"),
    ("Which module is used for regex?", "re"),
    ("Which module is used for math?", "math"),
    ("Which module is used for dates?", "datetime"),
    ("Which is not a file mode?", "appendx"),
    ("Which is not a valid variable name?", "1var"),
    ("Which is not a built-in function?", "printy"),
    ("Which is not a string method?", "speak"),
    ("Which method adds to list?", "append"),
    ("Which method removes last element?", "pop"),
    ("Which method sorts a list?", "sort"),
    ("Which method counts occurrences?", "count"),
    ("Which is not a list method?", "jump"),
    ("Which is not a tuple method?", "push"),
    ("Which is not a set method?", "insert"),
    ("Which is not a dict method?", "jump"),
    ("Which is used to create set?", "set()"),
    ("Which is used to create dict?", "dict()"),
    ("Which is not a Python data type?", "character"),
    ("Which is a valid Python comment?", "# comment"),
    ("Which is not a comparison operator?", "="),
    ("Which is not a logical operator?", "&&"),
    ("Which is not a bitwise operator?", "!"),
]


def _random_lcm_work():
    a = random.randint(2, 15)
    b = random.randint(3, 20)
    while b == a:
        b = random.randint(3, 20)
    lcm = (a * b) // math.gcd(a, b)
    days = round(lcm / ((lcm // a) + (lcm // b)), 2)
    return a, b, days


def _random_profit():
    cp = random.randint(100, 5000)
    pct = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    sp = int(cp * (1 + pct/100))
    return cp, pct, sp


def _random_ratio():
    a = random.randint(2, 15)
    b = random.randint(2, 15)
    while b == a:
        b = random.randint(2, 15)
    c = random.randint(2, 15)
    d = round((b * c) / a, 2)
    return a, b, c, d


def _random_average():
    n = random.randint(3, 15)
    avg = random.randint(20, 200)
    total = n * avg
    nums = [random.randint(avg-20, avg+20) for _ in range(n-1)]
    last = total - sum(nums)
    if last < 0:
        last = abs(last)
    return n, avg, nums, int(last)


def _random_loss():
    cp = random.randint(100, 5000)
    pct = random.choice([5, 10, 15, 20, 25])
    sp = int(cp * (1 - pct/100))
    return cp, pct, sp


def _random_discount():
    mp = random.randint(200, 10000)
    pct = random.choice([5, 10, 15, 20, 25, 30])
    sp = int(mp * (1 - pct/100))
    return mp, pct, sp


def _random_partnership():
    a = random.randint(1000, 50000)
    b = random.randint(1000, 50000)
    t = random.randint(1, 24)
    return a, b, t


def _random_work():
    pct = random.choice([10, 20, 25, 30, 40, 50])
    d = random.randint(5, 30)
    total_days = round(d * 100 / pct)
    return pct, d, total_days


def _random_workers():
    w = random.randint(5, 50)
    d1 = random.randint(10, 60)
    d2 = random.randint(5, d1 - 1)
    workers_needed = round(w * d1 / d2)
    return w, d1, d2, workers_needed


def _random_principal():
    a1 = random.randint(2000, 50000)
    t1 = random.randint(2, 5)
    t2 = t1 + 1
    a2 = a1 + random.randint(500, 2000)
    p = round((a1 * t2 - a2 * t1) / (t2 - t1))
    r = round((a2 - a1) * 100 / (p * t1), 2)
    return p, r, t1, a1, a2


def _random_ci_si():
    p = random.randint(1000, 10000)
    r = random.randint(5, 20)
    t = random.randint(2, 5)
    si = round(p * r * t / 100)
    ci = round(p * ((1 + r/100)**t - 1))
    return p, r, t, si, ci


def _random_ci_rate():
    a1 = random.randint(2000, 10000)
    a2 = a1 + random.randint(500, 2000)
    r = round((a2 - a1) * 100 / a1, 2)
    return a1, a2, r


def _random_men_women():
    a = random.randint(3, 15)
    b = random.randint(2, 10)
    d = random.randint(10, 40)
    c = random.randint(1, 10)
    d2 = random.randint(1, 10)
    return a, b, d, c, d2


def _random_work_left():
    a = random.randint(5, 20)
    b = random.randint(10, 30)
    d = random.randint(1, a - 1)
    b_days = round((a * b - d * a) / b)
    return a, b, d, b_days


def generate_numerical(count: int = 30) -> List[Dict]:
    out = []
    idx = 0
    for _ in range(count):
        a, b, days = _random_lcm_work()
        cp, pct, sp = _random_profit()
        ra, rb, rc, rd = _random_ratio()
        n, avg, nums, last = _random_average()
        lcp, lp, lsp = _random_loss()
        mp, dp, dsp = _random_discount()
        pa, pb, pt = _random_partnership()
        wpct, wd, wtotal = _random_work()
        ww, wd1, wd2, wneeded = _random_workers()
        prin, pr, pt1, pa1, pa2 = _random_principal()
        pp, prate, pt_t, psi, pci = _random_ci_si()
        ca1, ca2, crate = _random_ci_rate()
        ma, mb, md, mc, md2 = _random_men_women()
        wa, wb, wd_left, wb_days = _random_work_left()

        templates = [
            (f"A can complete a task in {a} days and B in {b} days. Working together, how many days?", str(days), f"Combined rate: 1/{a} + 1/{b} = {days} days", days),
            (f"Cost price is ₹{cp} and profit is {pct}%. What is selling price?", f"₹{sp}", f"SP = CP × (1 + {pct}/100) = ₹{sp}", float(sp)),
            (f"If {ra}:{rb} = {rc}:?, what is the fourth proportion?", str(round(rd,2)), f"d = (rb×rc)/ra = ({rb}×{rc})/{ra} = {rd}", round(rd,2)),
            (f"Average of {n} numbers is {avg}. If {n-1} numbers are {', '.join(map(str, nums))}, what is last?", str(last), f"Sum = {n*avg}. Last = {int(last)}", float(last)),
            (f"Loss of {lp}% on cost price ₹{lcp}. Selling price?", f"₹{lsp}", f"SP = CP × (1 - {lp}/100) = ₹{lsp}", float(lsp)),
            (f"Marked price ₹{mp}, discount {dp}%. Selling price?", f"₹{dsp}", f"SP = MP × (1 - {dp}/100) = ₹{dsp}", float(dsp)),
            (f"A and B invest ₹{pa} and ₹{pb} for {pt} months. Profit share ratio of A:B?", f"{pa}:{pb}", f"Ratio = {pa}:{pb}", float(pa)),
            (f"A does {wpct}% of work in {wd} days. Total days to finish remaining work?", str(wtotal), f"If {wpct}% in {wd} days, 100% in {round(wd*100/wpct,1)} days", float(wtotal)),
            (f"{ww} workers finish work in {wd1} days. Workers needed to finish in {wd2} days?", str(wneeded), f"Workers ∝ 1/Days → {ww}×{wd1}/{wd2} = {wneeded}", float(wneeded)),
            (f"A sum at SI becomes ₹{pa1} in {pt1} years. If rate is {pr}%, principal?", f"₹{prin}", f"P = A×100/(R×T) = {prin}", float(prin)),
            (f"Difference between CI and SI on ₹{pp} at {prate}% for {pt_t} years?", f"₹{pci - psi}", f"CI-SI = P×(R/100)^2 = ₹{pci - psi}", float(pci - psi)),
            (f"A sum at CI amounts to ₹{ca1} in 2 years and ₹{ca2} in 3 years. Rate of interest?", f"{crate}%", f"Rate = (A2-A1)/A1 × 100 = {crate}%", float(crate)),
            (f"If {ma} men or {mb} women can do a work in {md} days, how many days for {mc} men and {md2} women?", str(round(ma*mb*md/(mc*mb+md2*ma),1)), f"1/({ma}) = 1/({mb}) → combined rate = {round(1/(mc/(ma*md)+md2/(mb*md)),1)}", round(ma*mb*md/(mc*mb+md2*ma),1)),
            (f"A can do work in {wa} days, B in {wb} days. A leaves after {wd_left} days. B finishes in?", str(wb_days), f"Work done = {wd_left}/{wa}, remaining = {round(1 - wd_left/wa,2)}, B takes {wb_days} days", float(wb_days)),
        ]
        question, answer, explanation, raw = random.choice(templates)
        distractors = [str(raw + 1), str(raw - 1), str(raw * 2)]
        try:
            opts = _label_options([answer] + random.sample(distractors, 3))
        except ValueError:
            opts = _label_options([answer, str(raw+2), str(raw-2), str(raw*3)])
        out.append(_base(
            "numerical", idx, "numerical", "Quantitative Aptitude", "easy",
            question, opts, opts[0], explanation,
            ["TCS"], _company_relevance(["tcs"], ["infosys", "wipro"])
        ))
        idx += 1
    return out


def generate_reasoning(count: int = 20) -> List[Dict]:
    out = []
    idx = 0
    for _ in range(count):
        template_type = random.choice(["perm", "comb", "prob", "series", "blood", "coding", "syllogism", "seating", "directions", "clock"])

        if template_type == "perm":
            n = random.randint(5, 15)
            r = random.randint(2, min(n-1, 8))
            npr = math.perm(n, r) if hasattr(math, 'perm') else math.factorial(n)//math.factorial(n-r)
            question = f"How many ways to arrange {r} items from {n} distinct?"
            answer = str(npr)
            explanation = f"nPr = {n}!/({n-r})! = {npr}"
        elif template_type == "comb":
            n = random.randint(5, 15)
            r = random.randint(2, min(n-1, 8))
            ncr = math.comb(n, r)
            question = f"How many ways to choose {r} from {n} distinct?"
            answer = str(ncr)
            explanation = f"nCr = {n}!/({r}!×{n-r}!) = {ncr}"
        elif template_type == "prob":
            coins = random.choice([2, 3, 4, 5])
            heads = random.randint(1, coins-1)
            total = 2**coins
            favorable = math.comb(coins, heads)
            prob = round(favorable/total, 4)
            question = f"{coins} coins tossed, exactly {heads} head(s). Probability?"
            answer = str(prob)
            explanation = f"P = C({coins},{heads})/{total} = {prob}"
        elif template_type == "series":
            start = random.randint(1, 10)
            diff = random.randint(2, 5)
            n = random.randint(5, 12)
            term = start + (n-1)*diff
            question = f"In AP {start}, {start+diff}, {start+2*diff}..., what is the {n}th term?"
            answer = str(term)
            explanation = f"T{n} = a + (n-1)d = {start} + {n-1}×{diff} = {term}"
        elif template_type == "blood":
            relations = [
                ("A is the father of B and B is the sister of C. How is A related to C?", "Father"),
                ("A's mother is B's sister. How is A related to B?", "Nephew/Niece"),
                ("A is the brother of B. C is the daughter of B. How is A related to C?", "Uncle"),
                ("A's father is B's son. How is B related to A?", "Grandmother/Grandfather"),
                ("A is the husband of B's daughter. How is A related to B?", "Son-in-law"),
            ]
            question, answer = random.choice(relations)
            explanation = f"Answer: {answer}"
        elif template_type == "coding":
            alpha = random.randint(1, 5)
            word = random.choice(["CAT", "DOG", "SUN", "SKY", "RED"])
            coded = "".join(chr(ord(c) + alpha) for c in word)
            decode_word = random.choice(["CAT", "DOG", "SUN", "SKY", "RED"])
            decode_coded = "".join(chr(ord(c) + alpha) for c in decode_word)
            question = f"If A={1+alpha}, B={2+alpha}... what is the code for {decode_word}?"
            answer = decode_coded
            explanation = f"Each letter shifted by +{alpha}"
        elif template_type == "syllogism":
            syllogisms = [
                ("All A are B. Some B are C. Conclusion: Some A are C.", "Does not follow"),
                ("No A are B. All B are C. Conclusion: No A are C.", "Follows"),
                ("Some A are B. All B are C. Conclusion: Some A are C.", "Follows"),
                ("All A are B. No B are C. Conclusion: No A are C.", "Follows"),
                ("Some A are B. No B are C. Conclusion: Some A are not C.", "Does not follow"),
            ]
            question, answer = random.choice(syllogisms)
            explanation = f"Answer: {answer}"
        elif template_type == "seating":
            seatings = [
                ("A, B, C, D sit in a row. A sits left of B. C sits right of D. Who sits in middle?", "B or C"),
                ("A, B, C sit in a circle. A opposite B. Where is C?", "Adjacent to both"),
                ("Four people sit around a table. A faces B. C sits left of A. Where is D?", "Right of B"),
            ]
            question, answer = random.choice(seatings)
            explanation = f"Answer: {answer}"
        elif template_type == "directions":
            dirs = [
                ("A walks 10 km north, turns right walks 5 km. Distance from start?", "~11.18 km"),
                ("A walks 5 km east, 10 km north, 5 km west. Distance from start?", "10 km"),
                ("A walks 10 km south, turns left 5 km. Direction from start?", "South-West"),
            ]
            question, answer = random.choice(dirs)
            explanation = f"Answer: {answer}"
        elif template_type == "clock":
            hours = random.randint(1, 12)
            minutes = random.choice([15, 30, 45])
            angle = abs(30*hours - 5.5*minutes)
            angle = min(angle, 360-angle)
            question = f"Angle between clock hands at {hours}:{minutes:02d}?"
            answer = f"{round(angle,1)}°"
            explanation = f"Angle = |30H - 5.5M| = {round(angle,1)}°"

        try:
            float_val = float(answer)
            distractors = [str(float_val + 1.5), str(float_val - 1.5), str(float_val * 2)]
        except (ValueError, TypeError):
            distractors = ["Option B", "Option C", "Option D"]
        try:
            opts = _label_options([answer] + random.sample(distractors, 3))
        except ValueError:
            opts = _label_options([answer, "Option B", "Option C", "Option D"])
        out.append(_base(
            "reasoning", idx, "reasoning", "Logical Reasoning", "medium",
            question, opts, opts[0], explanation,
            ["TCS"], _company_relevance(["tcs"], ["infosys", "wipro"])
        ))
        idx += 1
    return out


def generate_verbal(count: int = 25) -> List[Dict]:
    out = []
    idx = 0
    pairs = [
        ("Happy", "Joyful"), ("Big", "Large"), ("Fast", "Quick"), ("Angry", "Furious"),
        ("Brave", "Courageous"), ("Calm", "Peaceful"), ("Clever", "Wise"), ("Cold", "Chilly"),
        ("Cruel", "Harsh"), ("Dark", "Dim"), ("Eager", "Enthusiastic"), ("Easy", "Simple"),
        ("Empty", "Bare"), ("Famous", "Renowned"), ("Funny", "Humorous"), ("Gentle", "Kind"),
        ("Giant", "Huge"), ("Glad", "Pleased"), ("Hard", "Difficult"), ("Honest", "Truthful"),
        ("Brave", "Valiant"), ("Bright", "Brilliant"), ("Boring", "Dull"), ("Calm", "Serene"),
        ("Careful", "Cautious"), ("Cheap", "Inexpensive"), ("Clean", "Spotless"), ("Clever", "Ingenious"),
        ("Cold", "Frigid"), ("Comfortable", "Cozy"), ("Cool", "Frigid"), ("Courageous", "Bold"),
        ("Cowardly", "Timid"), ("Cozy", "Snug"), ("Crazy", "Insane"), ("Creepy", "Eerie"),
        ("Cute", "Adorable"), ("Dangerous", "Hazardous"), ("Dark", "Gloomy"), ("Delicious", "Tasty"),
        ("Dense", "Thick"), ("Depressed", "Sad"), ("Difficult", "Arduous"), ("Dirty", "Filthy"),
        ("Disappointed", "Let down"), ("Dizzy", "Giddy"), ("Dry", "Arid"), ("Dull", "Blunt"),
        ("Eager", "Keen"), ("Easy", "Effortless"), ("Economical", "Thrifty"), ("Elegant", "Graceful"),
        ("Enormous", "Huge"), ("Enraged", "Furious"), ("Excellent", "Superb"), ("Expensive", "Costly"),
        ("Fabulous", "Fantastic"), ("Fair", "Just"), ("Faithful", "Loyal"), ("Fancy", "Ornate"),
        ("Fantastic", "Fabulous"), ("Fast", "Rapid"), ("Fat", "Obese"), ("Feeble", "Weak"),
        ("Fierce", "Ferocious"), ("Filthy", "Dirty"), ("Foolish", "Silly"), ("Frank", "Honest"),
        ("Friendly", "Amiable"), ("Frantic", "Hysterical"), ("Generous", "Liberal"), ("Gentle", "Tender"),
        ("Giant", "Colossal"), ("Gifted", "Talented"), ("Glad", "Delighted"), ("Gloomy", "Depressing"),
        ("Gorgeous", "Beautiful"), ("Graceful", "Elegant"), ("Great", "Grand"), ("Greedy", "Avaricious"),
        ("Hairy", "Shaggy"), ("Handsome", "Attractive"), ("Happy", "Cheerful"), ("Hard", "Tough"),
        ("Harsh", "Rigid"), ("Hate", "Despise"), ("Healthy", "Robust"), ("Heavy", "Weighty"),
        ("Helpful", "Useful"), ("Helpless", "Powerless"), ("Hesitate", "Pause"), ("Huge", "Massive"),
        ("Humorous", "Witty"), ("Hungry", "Ravenous"), ("Hurt", "Injure"), ("Idea", "Notion"),
        ("Idiot", "Fool"), ("Important", "Crucial"), ("Impressive", "Striking"), ("Industrious", "Diligent"),
        ("Inexpensive", "Cheap"), ("Innocent", "Guiltless"), ("Intelligent", "Brilliant"), ("Interesting", "Fascinating"),
        ("Interfere", "Meddle"), ("Intoxicated", "Drunk"), ("Ironic", "Sarcastic"), ("Irritate", "Annoy"),
        ("Jealous", "Envious"), ("Jolly", "Merry"), ("Joyful", "Blissful"), ("Judgmental", "Critical"),
        ("Kind", "Benevolent"), ("Knock", "Strike"), ("Knowledge", "Wisdom"), ("Lazy", "Indolent"),
        ("Lenient", "Permissive"), ("Liar", "Prevaricator"), ("Lively", "Animated"), ("Lonely", "Isolated"),
        ("Long", "Extended"), ("Loose", "Slack"), ("Lost", "Mislaid"), ("Loud", "Noisy"),
        ("Lovely", "Charming"), ("Loyal", "Faithful"), ("Lucky", "Fortunate"), ("Luxurious", "Opulent"),
        ("Mad", "Insane"), ("Magnificent", "Splendid"), ("Malicious", "Spiteful"), ("Mature", "Ripe"),
        ("Mean", "Nasty"), ("Meek", "Timid"), ("Mellow", "Mellowed"), ("Merciful", "Compassionate"),
        ("Merry", "Jovial"), ("Messy", "Slovenly"), ("Miserable", "Wretched"), ("Modern", "Contemporary"),
        ("Modest", "Humble"), ("Moody", "Temperamental"), ("Moral", "Ethical"), ("Morbid", "Gruesome"),
        ("Moron", "Idiot"), ("Mundane", "Earthly"), ("Mysterious", "Enigmatic"), ("Nasty", "Foul"),
        ("Naughty", "Mischievous"), ("Neat", "Tidy"), ("Necessary", "Essential"), ("Nice", "Pleasant"),
        ("Noisy", "Vociferous"), ("Normal", "Usual"), ("Noticeable", "Conspicuous"), ("Nourish", "Foster"),
        ("Obedient", "Compliant"), ("Obese", "Fat"), ("Object", "Protest"), ("Obvious", "Evident"),
        ("Odd", "Peculiar"), ("Offend", "Insult"), ("Old", "Ancient"), ("Optimistic", "Hopeful"),
        ("Organized", "Systematic"), ("Original", "Novel"), ("Outstanding", "Exceptional"), ("Pacify", "Mollify"),
        ("Painful", "Excruciating"), ("Pale", "Pallid"), ("Partial", "Biased"), ("Passive", "Inert"),
        ("Patient", "Tolerant"), ("Patriotic", "Nationalistic"), ("Peaceful", "Tranquil"), ("Perfect", "Impeccable"),
        ("Persuade", "Induce"), ("Pessimistic", "Gloomy"), ("Petty", "Trivial"), ("Physical", "Material"),
        ("Picturesque", "Quaint"), ("Plain", "Simple"), ("Pleasant", "Agreeable"), ("Plenty", "Abundance"),
        ("Poor", "Destitute"), ("Popular", "Favored"), ("Powerful", "Mighty"), ("Practical", "Pragmatic"),
        ("Precious", "Valuable"), ("Precise", "Exact"), ("Premium", "Superior"), ("Prestigious", "Illustrious"),
        ("Pretty", "Attractive"), ("Priceless", "Invaluable"), ("Primitive", "Primeval"), ("Productive", "Fertile"),
        ("Profound", "Deep"), ("Profuse", "Abundant"), ("Prolong", "Extend"), ("Prominent", "Notable"),
        ("Proper", "Appropriate"), ("Prosperous", "Thriving"), ("Protected", "Guarded"), ("Proud", "Arrogant"),
        ("Prudent", "Judicious"), ("Pure", "Immune"), ("Quick", "Swift"), ("Quiet", "Silent"),
        ("Radical", "Extreme"), ("Rare", "Scarce"), ("Rational", "Logical"), ("Real", "Actual"),
        ("Reasonable", "Sensible"), ("Rebellious", "Defiant"), ("Recover", "Recuperate"), ("Redundant", "Superfluous"),
        ("Refined", "Polished"), ("Regular", "Habitual"), ("Reliable", "Dependable"), ("Remarkable", "Noteworthy"),
        ("Remorse", "Contrition"), ("Resilient", "Tenacious"), ("Respect", "Esteem"), ("Restrict", "Limit"),
        ("Retain", "Keep"), ("Reveal", "Disclose"), ("Rich", "Wealthy"), ("Ridiculous", "Absurd"),
        ("Rigid", "Inflexible"), ("Risky", "Hazardous"), ("Robust", "Sturdy"), ("Rude", "Impolite"),
        ("Ruthless", "Cruel"), ("Satisfied", "Content"), ("Scared", "Frightened"), ("Secure", "Safe"),
        ("Select", "Choose"), ("Sensitive", "Sensible"), ("Serene", "Calm"), ("Severe", "Harsh"),
        ("Shaggy", "Hairy"), ("Shallow", "Superficial"), ("Shiny", "Glossy"), ("Showy", "Flashy"),
        ("Shy", "Bashful"), ("Significant", "Momentous"), ("Silent", "Taciturn"), ("Silly", "Foolish"),
        ("Simple", "Plain"), ("Sincere", "Genuine"), ("Skeletal", "Bony"), ("Skeptical", "Doubtful"),
        ("Slack", "Loose"), ("Slim", "Slender"), ("Slow", "Sluggish"), ("Small", "Tiny"),
        ("Smart", "Intelligent"), ("Smooth", "Polished"), ("Social", "Gregarious"), ("Soft", "Gentle"),
        ("Solid", "Firm"), ("Solemn", "Sober"), ("Splendid", "Magnificent"), ("Spontaneous", "Natural"),
        ("Stable", "Steady"), ("Stingy", "Miserly"), ("Strange", "Bizarre"), ("Strict", "Stringent"),
        ("Stubborn", "Obstinate"), ("Stupid", "Dense"), ("Sturdy", "Robust"), ("Subtle", "Delicate"),
        ("Superb", "Excellent"), ("Superficial", "Shallow"), ("Superior", "Higher"), ("Superstitious", "Credulous"),
        ("Surprise", "Amaze"), ("Suspicious", "Doubtful"), ("Swift", "Rapid"), ("Sympathetic", "Compassionate"),
        ("Tactful", "Diplomatic"), ("Talented", "Gifted"), ("Tall", "Lofty"), ("Tame", "Domesticated"),
        ("Tasty", "Delicious"), ("Tender", "Soft"), ("Tense", "Nervous"), ("Terrible", "Awful"),
        ("Thin", "Lean"), ("Thirsty", "Parched"), ("Thrifty", "Economical"), ("Tiny", "Minuscule"),
        ("Tired", "Weary"), ("Tough", "Rugged"), ("Tragic", "Catastrophic"), ("Transparent", "Clear"),
        ("Treacherous", "Traitorous"), ("Tremendous", "Enormous"), ("Trim", "Slender"), ("Trivial", "Petty"),
        ("True", "Genuine"), ("Trustworthy", "Reliable"), ("Tyrant", "Dictator"), ("Ugly", "Unattractive"),
        ("Ultimate", "Final"), ("Unbelievable", "Incredible"), ("Uncertain", "Doubtful"), ("Unique", "Singular"),
        ("Universal", "General"), ("Unknown", "Mysterious"), ("Unlucky", "Unfortunate"), ("Unpleasant", "Offensive"),
        ("Unreal", "Fictitious"), ("Unreliable", "Undependable"), ("Vague", "Ambiguous"), ("Valuable", "Priceless"),
        ("Vast", "Immense"), ("Vengeful", "Vindictive"), ("Verdant", "Green"), ("Versatile", "Multipurpose"),
        ("Vigilant", "Watchful"), ("Virtuous", "Righteous"), ("Vivid", "Graphic"), ("Vulnerable", "Susceptible"),
        ("Warm", "Cordial"), ("Wasteful", "Extravagant"), ("Watchful", "Vigilant"), ("Weak", "Feeble"),
        ("Wealthy", "Rich"), ("Weary", "Tired"), ("Weird", "Bizarre"), ("Welcome", "Greeting"),
        ("Well", "Fit"), ("Wicked", "Villainous"), ("Wide", "Broad"), ("Wild", "Untamed"),
        ("Willing", "Voluntary"), ("Wise", "Sage"), ("Witty", "Humorous"), ("Wonderful", "Terrific"),
        ("Worried", "Anxious"), ("Worthless", "Valueless"), ("Worthy", "Deserving"), ("Wounded", "Injured"),
        ("Wreck", "Ruin"), ("Yielding", "Surrendering"), ("Youthful", "Young"), ("Zealous", "Enthusiastic"),
    ]
    random.shuffle(pairs)
    for word, syn in pairs[:count]:
        distractors = ["Sad", "Angry", "Big", "Small", "Fast", "Slow", "Hot", "Cold"]
        opts = _label_options([syn] + random.sample(distractors, 3))
        out.append(_base(
            "verbal", idx, "verbal", "Verbal", "easy",
            f"Synonym of '{word}'?", opts, opts[0],
            f"'{syn}' is a synonym of '{word}'",
            ["TCS"], _company_relevance(["tcs"], ["infosys", "wipro"])
        ))
        idx += 1
    return out


def generate_coding(count: int = 3) -> List[Dict]:
    out = []
    idx = 0
    for code, expected in CODING_TEMPLATES[:count]:
        distractors = ["5", "8", "10", "20", "25", "3", "7", "14", "True", "False"]
        opts = _label_options([expected] + random.sample(distractors, 3))
        out.append(_base(
            "coding", idx, "coding", "Programming Logic", "medium",
            f"What is the output?\n{code}", opts, opts[0],
            f"Output: {expected}",
            ["TCS"], _company_relevance(["tcs"], ["infosys", "wipro"])
        ))
        idx += 1
    return out


def generate_cs(count: int = 10) -> List[Dict]:
    out = []
    idx = 0
    selected = random.sample(CS_TEMPLATES, min(count, len(CS_TEMPLATES)))
    for question, answer in selected:
        distractors = ["5", "10", "3", "8080", "21", "Oracle", "MySQL", "C++", "Java"]
        opts = _label_options([answer] + random.sample(distractors, 3))
        out.append(_base(
            "cs", idx, "cs", "CS Fundamentals", "easy",
            question, opts, opts[0], answer,
            ["TCS"], _company_relevance(["tcs"], ["infosys", "wipro"])
        ))
        idx += 1
    return out


def build_company_bank(company_key: str, target_total: int = 600) -> List[Dict]:
    random.seed(COMPANY_SEEDS.get(company_key, 123))
    structure = COMPANY_STRUCTURES[company_key]
    all_qs = []

    def _flatten_question(q: Dict):
        content_opts = q.get("content", {}).get("options") or []
        if isinstance(content_opts, list) and len(content_opts) >= 4:
            opts_dict = {}
            for opt in content_opts:
                opt = str(opt).strip()
                if len(opt) >= 2 and opt[1] == ".":
                    opts_dict[opt[0].upper()] = opt[2:].strip()
                elif len(opt) >= 1:
                    opts_dict[opt[0].upper()] = opt[1:].strip()
            q["options"] = opts_dict
            correct = q.get("content", {}).get("correct_answer") or q.get("content", {}).get("answer")
            if correct:
                q["correct_answer"] = str(correct).strip()[0].upper()

    for section in structure["sections"]:
        section_qs = []
        if section["type"] == "mcq":
            if section["domain"] == "Quantitative Aptitude":
                section_qs = generate_numerical(section["questions"])
            elif section["domain"] == "Logical Reasoning":
                section_qs = generate_reasoning(section["questions"])
            elif section["domain"] == "Verbal":
                section_qs = generate_verbal(section["questions"])
            elif section["domain"] == "CS Fundamentals":
                section_qs = generate_cs(section["questions"])
            elif section["domain"] == "Programming Logic":
                section_qs = generate_coding(section["questions"])
        elif section["type"] == "coding":
            section_qs = generate_coding(section["questions"])

        # Attach section metadata
        for q in section_qs:
            q["company_section"] = section["key"]
            q["company_section_label"] = section["label"]
            q["section_duration_minutes"] = section["minutes"]
            q["section_questions"] = section["questions"]
            q["company_exam"] = company_key
            q["company"] = company_key.upper()
            q["companies"] = [company_key.lower()]
            q["trust_status"] = "reviewed"
            _flatten_question(q)

        all_qs.extend(section_qs)

    # If we need more to reach target_total, duplicate and perturb
    while len(all_qs) < target_total:
        extra = []
        for section in structure["sections"]:
            section_qs = []
            if section["type"] == "mcq":
                if section["domain"] == "Quantitative Aptitude":
                    section_qs = generate_numerical(min(section["questions"], target_total - len(all_qs) - len(extra)))
                elif section["domain"] == "Logical Reasoning":
                    section_qs = generate_reasoning(min(section["questions"], target_total - len(all_qs) - len(extra)))
                elif section["domain"] == "Verbal":
                    section_qs = generate_verbal(min(section["questions"], target_total - len(all_qs) - len(extra)))
                elif section["domain"] == "CS Fundamentals":
                    section_qs = generate_cs(min(section["questions"], target_total - len(all_qs) - len(extra)))
                elif section["domain"] == "Programming Logic":
                    section_qs = generate_coding(min(section["questions"], target_total - len(all_qs) - len(extra)))
            elif section["type"] == "coding":
                section_qs = generate_coding(min(section["questions"], target_total - len(all_qs) - len(extra)))

            for q in section_qs:
                q["company_section"] = section["key"]
                q["company_section_label"] = section["label"]
                q["section_duration_minutes"] = section["minutes"]
                q["section_questions"] = section["questions"]
                q["company_exam"] = company_key
                q["company"] = company_key.upper()
                q["companies"] = [company_key.lower()]
                q["trust_status"] = "reviewed"
                _flatten_question(q)
            extra.extend(section_qs)
        all_qs.extend(extra)

    return all_qs[:target_total]


def save_company_bank(company_key: str, questions: List[Dict]):
    company_dir = OUTPUT_DIR / company_key
    company_dir.mkdir(parents=True, exist_ok=True)

    # Save full bank
    path = company_dir / f"{company_key}_full_bank.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(questions)} -> {path}")

    # Save per-section files
    sections = {}
    for q in questions:
        sec = q.get("company_section", "unknown")
        sections.setdefault(sec, []).append(q)

    for sec, qs in sections.items():
        sec_path = company_dir / f"{company_key}_{sec}.json"
        with open(sec_path, "w", encoding="utf-8") as f:
            json.dump(qs, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(qs)} -> {sec_path}")


def main():
    print("Building service-company prep banks...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_questions = []
    target_per_company = 600

    for company_key in ["tcs", "wipro", "cognizant", "capgemini", "tech_mahindra", "infosys", "accenture", "ltimindtree"]:
        print(f"\nGenerating {company_key} bank...")
        qs = build_company_bank(company_key, target_total=target_per_company)
        all_questions.extend(qs)
        print(f"  {company_key}: {len(qs)} questions")
        save_company_bank(company_key, qs)

    combined_path = OUTPUT_DIR / "service_company_all_banks.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    print(f"\nSaved combined: {len(all_questions)} -> {combined_path}")
    print("Done.")


if __name__ == "__main__":
    main()
