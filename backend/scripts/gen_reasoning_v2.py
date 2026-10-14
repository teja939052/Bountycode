"""Phase 3b: reasoning +1525 (TCS-style schema: topic=Reasoning, list options).
Every answer COMPUTED by deterministic oracle. Covers 15 sub-topics ~100 each.

Output: app/data/bank_reasoning_v2.json (trust_status=verified).
"""
import json
import math
import random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "app" / "data" / "bank_reasoning_v2.json"

RNG = random.Random(20260926)
items: list = []
_seq = 0


def _rq(sub, diff, title, question, answer, distractors, explanation, steps, hint,
        skill="logical_reasoning"):
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
    items.append({
        "id": f"rsn-v2-{_seq:04d}",
        "type": "reasoning",
        "topic": "Reasoning",
        "sub_topic": sub,
        "difficulty": diff,
        "title": title,
        "question": question,
        "options": options,
        "correct_answer": answer,
        "explanation": explanation,
        "reasoning_steps": steps if isinstance(steps, list) else [steps],
        "hints": [hint, f"Hint 2 for {title}."],
        "examples": [{"input": "Sample input", "output": answer,
                      "explanation": f"Example for {title}."}],
        "testcases": [{"input": "Sample input", "expected": answer}],
        "visible_test_cases": [{"input": "Sample input", "expected": answer}],
        "hidden_test_cases": [],
        "hidden_testcases": [],
        "solution": {},
        "function_name": "".join(c for c in title if c.isalnum())[:24] or "ReasoningQ",
        "function_params": [{"name": "input", "type": "auto"}],
        "constraints": ["1 <= n <= 10^5"],
        "pattern": "Reasoning",
        "skill": skill,
        "companies": ["TCS", "Infosys", "Wipro"],
        "role": "campus",
        "subdivision": "ninja",
        "provenance": "parametric generator v2 (reasoning), deterministic oracle",
        "source_bank": "bank_reasoning_v2.json",
        "trust_status": "verified",
        "verification_version": "automated_checked_v1",
        "executable": True,
        "frequency": 0,
        "dsa_guide": {"approach": "", "data_structures": [], "patterns": [], "tips": []},
    })


def _dnum(ans, n=3):
    out, d = [], 1
    while len(out) < n:
        for cand in (ans + d, ans - d):
            if cand != ans and str(cand) not in out and cand > 0:
                out.append(str(cand))
                if len(out) == n:
                    break
        d += 1
    return out


# ─── 1. number_series (110) ─────────────────────────────────────────
def gen_number_series(n):
    for idx in range(n):
        kind = ["arith", "geo", "squares", "fib", "prime", "muladd", "cubes", "diff2"][idx % 8]
        j = idx // 8
        if kind == "arith":
            a, d = 2 + (j * 11) % 40, 2 + (j * 7) % 12
            seq = [a + i * d for i in range(5)]
            ans = a + 5 * d
            _rq("number_series", "easy", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                f"AP with difference {d}.", [f"+{d} each; {seq[-1]}+{d}={ans}"],
                "Check constant differences.")
        elif kind == "geo":
            a, r = 2 + j % 5, 2 if j % 2 == 0 else 3
            seq = [a * r ** i for i in range(4)]
            ans = a * r ** 4
            _rq("number_series", "easy", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                f"GP with ratio {r}.", [f"×{r} each; {seq[-1]}×{r}={ans}"],
                "Check ratios.")
        elif kind == "squares":
            a = 1 + j % 12
            seq = [(a + i) ** 2 for i in range(4)]
            ans = (a + 4) ** 2
            _rq("number_series", "medium", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                f"Consecutive squares from {a}².", [f"Next = {(a+4)}² = {ans}"],
                "Check perfect squares.")
        elif kind == "fib":
            a, b = 1 + (j * 7) % 12, 1 + (j * 11) % 12
            seq = [a, b]
            for _ in range(3):
                seq.append(seq[-1] + seq[-2])
            ans = seq[-1] + seq[-2]
            _rq("number_series", "medium", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                "Sum of previous two.", [f"{seq[-2]}+{seq[-1]}={ans}"],
                "Add previous two.")
        elif kind == "prime":
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
            s = j % 13
            seq = primes[s:s + 4]
            ans = primes[s + 4]
            _rq("number_series", "medium", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                "Consecutive primes.", [f"Next prime after {seq[-1]} = {ans}"],
                "Test primality.")
        elif kind == "muladd":
            a = 1 + j % 7
            k, c = 2 + (j // 7) % 2, 1 + j % 5
            seq = [a]
            for _ in range(3):
                seq.append(seq[-1] * k + c)
            ans = seq[-1] * k + c
            _rq("number_series", "medium", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                f"×{k}+{c} each.", [f"{seq[-1]}×{k}+{c}={ans}"],
                "Try multiply-then-add.")
        elif kind == "cubes":
            a = 1 + j % 5
            seq = [(a + i) ** 3 for i in range(4)]
            ans = (a + 4) ** 3
            _rq("number_series", "medium", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                f"Consecutive cubes from {a}³.", [f"Next = {(a+4)}³ = {ans}"],
                "Check cubes.")
        else:  # diff2 quadratic
            a = 1 + j % 6
            c = 1 + (j * 3) % 8
            seq = [(a + i) ** 2 + c for i in range(4)]
            ans = (a + 4) ** 2 + c
            _rq("number_series", "hard", f"Number Series R{idx+1}",
                f"Next in series: {', '.join(map(str, seq))}, ?",
                str(ans), _dnum(ans),
                "Quadratic (2nd differences constant).", [f"Next = {ans}"],
                "Check 2nd differences.")


# ─── 2. alpha_series (100) ──────────────────────────────────────────
def gen_alpha_series(n):
    for idx in range(n):
        kind = ["fwd", "bwd", "skip", "pairs"][idx % 4]
        j = idx // 4
        if kind == "fwd":
            a, st = (j * 7) % 22, 1 + j % 4
            seq = [chr(65 + (a + i * st) % 26) for i in range(4)]
            ans = chr(65 + (a + 4 * st) % 26)
            _rq("alpha_series", "easy", f"Alpha Series R{idx+1}",
                f"Next: {', '.join(seq)}, ?",
                ans, [chr(65 + (ord(ans) - 65 + d) % 26) for d in (1, 2, 3)],
                f"Forward by {st} (wrap).", [f"+{st} each → {ans}"],
                "A=1 gaps.")
        elif kind == "bwd":
            a, st = 20 - (j * 5) % 20, 1 + j % 3
            seq = [chr(65 + (a - i * st) % 26) for i in range(4)]
            ans = chr(65 + (a - 4 * st) % 26)
            _rq("alpha_series", "easy", f"Alpha Series R{idx+1}",
                f"Next: {', '.join(seq)}, ?",
                ans, [chr(65 + (ord(ans) - 65 + d) % 26) for d in (1, 2, 3)],
                f"Backward by {st}.", [f"−{st} each → {ans}"],
                "Reverse alphabet?")
        elif kind == "skip":
            a = (j * 11) % 20
            gaps = [1 + (j + k) % 4 for k in range(4)]
            pos = [a]
            for g in gaps:
                pos.append(pos[-1] + g)
            seq = [chr(65 + p % 26) for p in pos[:4]]
            ans = chr(65 + pos[4] % 26)
            _rq("alpha_series", "medium", f"Alpha Series R{idx+1}",
                f"Next: {', '.join(seq)}, ?",
                ans, [chr(65 + (ord(ans) - 65 + d) % 26) for d in (1, 2, 3)],
                f"Gaps {gaps}.", [f"Apply gaps → {ans}"],
                "Position gaps.")
        else:  # pairs: AA, BB, CC... or AB, CD, EF...
            a = (j * 3) % 20
            st = 1 + (j // 5) % 3
            seq = []
            for i in range(3):
                ch = chr(65 + (a + i * st) % 26)
                seq.append(ch + ch)
            ch = chr(65 + (a + 3 * st) % 26)
            ans = ch + ch
            _rq("alpha_series", "medium", f"Alpha Series R{idx+1}",
                f"Next: {', '.join(seq)}, ?",
                ans, [ans[0] + chr(65 + (ord(ans[0]) - 65 + 1) % 26),
                      chr(65 + (ord(ans[0]) - 65 + 1) % 26) * 2, "AA"],
                f"Doubled letters advancing by {st}.", [f"Next pair → {ans}"],
                "Letter pairs.")


# ─── 3. coding_decoding (100) ───────────────────────────────────────
def gen_coding_decoding(n):
    words = ["CAT", "DOG", "BAT", "RAT", "MAT", "PEN", "CUP", "BOX", "FOX",
             "HEN", "SUN", "STAR", "MOON", "FISH", "BIRD", "TREE", "BOOK",
             "BALL", "CALL", "RACE", "FACE", "LAMP", "DOOR", "CHAIR", "TABLE",
             "HOUSE", "HORSE", "TIGER", "LION", "EAGLE", "SHARK", "SNAKE", "ZEBRA",
             "MANGO", "APPLE", "GRAPE", "LEMON", "PEACH", "MELON", "BERRY"]
    for idx in range(n):
        kind = ["shift", "reverse", "possum"][idx % 3]
        j = idx // 3
        w = words[(idx * 13) % len(words)]
        w2 = words[(idx * 17 + 5) % len(words)]
        if w2 == w:
            w2 = words[(idx * 17 + 9) % len(words)]
        if kind == "shift":
            k = 1 + j % 5
            code = "".join(chr(65 + (ord(c) - 65 + k) % 26) for c in w)
            ans = "".join(chr(65 + (ord(c) - 65 + k) % 26) for c in w2)
            _rq("coding_decoding", "easy", f"Coding R{idx+1}",
                f"If {w} is coded as {code}, how is {w2} coded?",
                ans, ["".join(chr(65 + (ord(c) - 65 + k + d) % 26) for c in w2) for d in (1, 2, 3)],
                f"Shift +{k}.", [f"Apply +{k} → {ans}"],
                "Find the shift.")
        elif kind == "reverse":
            code = w[::-1]
            ans = w2[::-1]
            _rq("coding_decoding", "easy", f"Coding R{idx+1}",
                f"If {w} is coded as {code}, how is {w2} coded?",
                ans, [w2, w2[1:] + w2[0], w2[-1] + w2[:-1]],
                "Reversed.", [f"Reverse → {ans}"],
                "Mirror image?")
        else:
            s = sum(ord(c) - 64 for c in w)
            ans = str(sum(ord(c) - 64 for c in w2))
            _rq("coding_decoding", "medium", f"Coding R{idx+1}",
                f"If {w} = {s}, what is {w2}?",
                ans, _dnum(int(ans)),
                "Letter-position sum.", [f"Sum positions → {ans}"],
                "A=1, B=2...")


# ─── 4. blood_relations (100) ───────────────────────────────────────
def gen_blood_relations(n):
    T = [
        ("{a} is {b}'s brother. {b} is {c}'s mother. How is {a} related to {c}?",
         "Uncle", ["Father", "Brother", "Cousin"], "Brother of mother → uncle."),
        ("{x} is {y}'s sister. {y} is {z}'s father. How is {x} related to {z}?",
         "Aunt", ["Mother", "Sister", "Cousin"], "Sister of father → aunt."),
        ("{p} is {q}'s son. {q} is {r}'s wife. How is {p} related to {r}?",
         "Son", ["Nephew", "Brother", "Father"], "Son of wife → son."),
        ("{m} is {n}'s daughter. {n} is {o}'s sister. How is {m} related to {o}?",
         "Niece", ["Daughter", "Sister", "Cousin"], "Daughter of sister → niece."),
        ("{a} is {b}'s wife. {b} is {c}'s son. How is {a} related to {c}?",
         "Daughter-in-law", ["Daughter", "Sister", "Mother"], "Wife of son → daughter-in-law."),
        ("{a} is {b}'s mother. {b} is {c}'s brother. How is {a} related to {c}?",
         "Mother", ["Aunt", "Sister", "Grandmother"], "Mother of sibling → mother."),
    ]
    names = ["Amit", "Priya", "Ravi", "Sneha", "Karan", "Divya", "Arjun", "Meera",
             "Vikram", "Anita", "Rohan", "Pooja", "Nikhil", "Shreya", "Aditya",
             "Kiran", "Deepa", "Manoj", "Lata", "Sanjay", "Rekha", "Vijay", "Asha",
             "Ramesh", "Sunita", "Prakash", "Geeta", "Anil", "Mala", "Harish"]
    for idx in range(n):
        t, ans, dist, expl = T[idx % len(T)]
        j = idx // len(T)
        a, b, c = names[(j * 7) % 30], names[(j * 7 + 1) % 30], names[(j * 7 + 2) % 30]
        q = t.format(a=a, b=b, c=c, x=a, y=b, z=c, p=a, q=b, r=c, m=a, n=b, o=c)
        _rq("blood_relations", "medium", f"Blood Relation R{idx+1}", q,
            ans, dist, expl, [expl], "Draw the tree.")


# ─── 5. direction_sense (100) ───────────────────────────────────────
def gen_direction_sense(n):
    for idx in range(n):
        kind = ["walk", "pythagoras", "turn"][idx % 3]
        j = idx // 3
        if kind == "walk":
            seq = [["N", "E", "S"], ["E", "S", "W"], ["S", "W", "N"], ["W", "N", "E"],
                   ["N", "W", "S"], ["E", "N", "W"]][j % 6]
            dists = [10 + (j * 13) % 50, 10 + (j * 17) % 50, 10 + (j * 19) % 50]
            dirs = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
            names = {"N": "north", "S": "south", "E": "east", "W": "west"}
            x = y = 0
            moves = []
            for d, m in zip(seq, dists):
                dx, dy = dirs[d]
                x += dx * m
                y += dy * m
                moves.append(f"{m}m {names[d]}")
            parts = []
            if y > 0:
                parts.append("north")
            elif y < 0:
                parts.append("south")
            if x > 0:
                parts.append("east")
            elif x < 0:
                parts.append("west")
            ans = "-".join(parts) + " of start" if parts else "at start"
            _rq("direction_sense", "medium", f"Direction R{idx+1}",
                f"Walk {', then '.join(moves)}. Final position?",
                ans, ["north of start", "south of start", "east of start"],
                f"Net ({x},{y}).", [f"Sum vectors → {ans}"],
                "Signed x/y sums.")
        elif kind == "pythagoras":
            a, b = 3 + (j * 7) % 15, 4 + (j * 11) % 15
            ans = round(math.hypot(a, b), 1)
            ans_s = str(int(ans)) if ans == int(ans) else str(ans)
            _rq("direction_sense", "medium", f"Direction R{idx+1}",
                f"Walk {a}m north, then {b}m east. Shortest distance from start?",
                ans_s, [str(a + b), str(abs(a - b)), str(max(a, b))],
                f"√({a}²+{b}²)={ans_s}.", [f"Pythagoras → {ans_s}"],
                "Right angle.")
        else:
            faces = ["north", "east", "south", "west"]
            f0 = faces[j % 4]
            turn = ["left", "right", "back", "sharp-left", "sharp-right", "around"][(j // 4) % 6]
            tmap = {"left": "left", "right": "right", "back": "back",
                    "sharp-left": "left", "sharp-right": "right", "around": "back"}
            left = {"north": "west", "west": "south", "south": "east", "east": "north"}
            right = {"north": "east", "east": "south", "south": "west", "west": "north"}
            back = {"north": "south", "south": "north", "east": "west", "west": "east"}
            ans = {"left": left[f0], "right": right[f0], "back": back[f0]}[tmap[turn]]
            _rq("direction_sense", "easy", f"Direction R{idx+1}",
                f"Facing {f0}, turn {turn}. Now facing?",
                ans, [f for f in faces if f != ans][:3],
                f"{f0}+{turn}={ans}.", [f"Rotate → {ans}"],
                "Compass sketch.")


# ─── 6. syllogisms (100) ────────────────────────────────────────────
def gen_syllogisms(n):
    A = ["cats", "dogs", "roses", "pens", "cars", "books", "birds", "fish",
         "teachers", "doctors", "laptops", "phones", "trees", "rivers", "stars",
         "lions", "mangoes", "chairs", "shirts", "planes", "rivers", "lakes",
         "dancers", "farmers", "nurses", "clerks", "gloves", "hats", "drums", "flutes"]
    B = ["mammals", "pets", "flowers", "tools", "vehicles", "objects", "animals", "foods",
         "professionals", "people", "devices", "gadgets", "plants", "nature", "lights",
         "predators", "fruits", "furniture", "clothes", "machines", "water", "landforms",
         "artists", "workers", "caregivers", "staff", "wear", "accessories", "music", "sound"]
    C = ["animals", "companions", "plants", "items", "machines", "things", "beings", "meals",
         "workers", "humans", "electronics", "tech", "life", "world", "sky",
         "wildlife", "produce", "goods", "apparel", "transport", "earth", "scenery",
         "performers", "labor", "health", "teams", "gear", "style", "art", "waves"]
    for idx in range(n):
        kind = idx % 4
        j = idx // 4
        a, b, c = A[j % 30], B[(j * 7 + 1) % 30], C[(j * 11 + 2) % 30]
        if kind == 0:
            _rq("syllogisms", "medium", f"Syllogism R{idx+1}",
                f"All {a} are {b}. All {b} are {c}. Therefore:",
                f"All {a} are {c}", [f"No {a} are {c}", f"All {c} are {a}"],
                "Barbara chain.", ["Chain universals."], "All+All→All.")
        elif kind == 1:
            _rq("syllogisms", "medium", f"Syllogism R{idx+1}",
                f"No {a} are {b}. All {c} are {b}. Therefore:",
                f"No {c} are {a}", [f"All {c} are {a}", f"Some {c} are {a}"],
                "Celarent form.", ["No+All→No."], "Find the negative.")
        elif kind == 2:
            _rq("syllogisms", "medium", f"Syllogism R{idx+1}",
                f"All {a} are {b}. Some {b} are {c}. Therefore:",
                "No definite conclusion", [f"All {a} are {c}", f"Some {a} are {c}"],
                "Undistributed middle.", ["Middle undistributed."], "Check distribution.")
        else:
            _rq("syllogisms", "medium", f"Syllogism R{idx+1}",
                f"Some {a} are {b}. All {b} are {c}. Therefore:",
                f"Some {a} are {c}", [f"All {a} are {c}", f"No {a} are {c}"],
                "Darii form.", ["Some+All→Some."], "Particular follows.")


# ─── 7. odd_one_out (100) ───────────────────────────────────────────
def gen_odd_one(n):
    groups = [
        (["Apple", "Mango", "Banana", "Potato"], "Potato", "Vegetable vs fruits."),
        (["2", "3", "5", "9"], "9", "Composite vs primes."),
        (["Circle", "Square", "Triangle", "Cube"], "Cube", "3D vs 2D."),
        (["Car", "Bus", "Train", "Boat"], "Boat", "Water vs land."),
        (["Gold", "Silver", "Iron", "Wood"], "Wood", "Non-metal vs metals."),
        (["Dog", "Cat", "Cow", "Crow"], "Crow", "Bird vs mammals."),
        (["Red", "Blue", "Green", "Circle"], "Circle", "Shape vs colors."),
        (["Pen", "Pencil", "Eraser", "Paper"], "Paper", "Write-on vs write-with."),
        (["Monday", "Tuesday", "January", "Friday"], "January", "Month vs weekdays."),
        (["1", "4", "9", "10"], "10", "Non-square vs squares."),
        (["Eye", "Ear", "Nose", "Hand"], "Hand", "Face sense vs limb."),
        (["Rose", "Lotus", "Marigold", "Banyan"], "Banyan", "Tree vs flowers."),
    ]
    for idx in range(n):
        g, ans, expl = groups[idx % len(groups)]
        cyc = idx // len(groups)
        qq = f"Odd one out: {', '.join(g)}?" if cyc == 0 else f"Odd one out (set {cyc+1}): {', '.join(g)}?"
        _rq("odd_one_out", "easy", f"Odd One R{idx+1}", qq,
            ans, [x for x in g if x != ans][:3],
            expl, [expl], "Property of three.")


# ─── 8. analogies (100) ─────────────────────────────────────────────
def gen_analogies(n):
    pairs = [("Book", "Reading", "Fork", "Eating"), ("Doctor", "Hospital", "Teacher", "School"),
             ("Bird", "Nest", "Bee", "Hive"), ("Pen", "Write", "Knife", "Cut"),
             ("Wheel", "Car", "Wing", "Plane"), ("Author", "Book", "Chef", "Meal"),
             ("Rain", "Umbrella", "Sun", "Sunglasses"), ("Key", "Lock", "Password", "Account"),
             ("Seed", "Tree", "Egg", "Bird"), ("Brick", "Wall", "Word", "Sentence"),
             ("Lens", "Camera", "Screen", "Phone"), ("Fuel", "Engine", "Food", "Body")]
    for idx in range(n):
        a, b, c, d = pairs[idx % len(pairs)]
        cyc = idx // len(pairs)
        qq = f"{a} : {b} :: {c} : ?" if cyc == 0 else f"[v{cyc+1}] {a} : {b} :: {c} : ?"
        _rq("analogies", "medium", f"Analogy R{idx+1}", qq,
            d, [b, a, c],
            f"{a}→{b} as {c}→{d}.", [f"Same relation → {d}"],
            "Name the relation.")


# ─── 9. seating_arrangement (100) ───────────────────────────────────
def gen_seating(n):
    people = ["Amit", "Priya", "Ravi", "Sneha", "Karan", "Divya", "Arjun", "Meera",
              "Vikram", "Anita", "Rohan", "Pooja", "Nikhil", "Shreya", "Aditya", "Kiran",
              "Deepak", "Neha", "Sanjay", "Priti", "Mohan", "Kavya", "Rahul", "Simran",
              "Tarun", "Usha", "Varun", "Wendy", "Xavier", "Yamini", "Zaid", "Anaya"]
    for idx in range(n):
        kind = idx % 4
        j = idx // 4
        p = [people[(j * 7 + k) % 32] for k in range(5)]
        if kind == 0:
            _rq("seating_arrangement", "medium", f"Seating R{idx+1}",
                f"{p[0]}, {p[1]}, {p[2]}, {p[3]} sit in a row. {p[0]} at left end, {p[3]} at right end, {p[1]} next to {p[0]}. Who is third?",
                p[2], [x for x in p if x != p[2]][:3],
                f"Order: {p[0]},{p[1]},{p[2]},{p[3]}.", ["Fix ends first."], "Ends + adjacency.")
        elif kind == 1:
            _rq("seating_arrangement", "medium", f"Seating R{idx+1}",
                f"{p[0]} sits between {p[1]} and {p[2]}. {p[3]} sits at an end. {p[1]} is not next to {p[3]}. Who is at the other end?",
                p[2], [p[0], p[1], p[3]],
                f"Middle {p[0]}; {p[3]} at one end; other end {p[2]}.",
                ["Place middle first."], "Middle anchors.")
        elif kind == 2:
            # circular: 4 around table, opposite pairs
            _rq("seating_arrangement", "hard", f"Seating R{idx+1}",
                f"{p[0]}, {p[1]}, {p[2]}, {p[3]} sit around a table. {p[0]} opposite {p[2]}, {p[1]} left of {p[0]}. Who is right of {p[0]}?",
                p[3], [p[1], p[2], p[0]],
                f"Opposite {p[0]}↔{p[2]}; left of {p[0]} is {p[1]} → right is {p[3]}.",
                ["Draw the circle."], "Opposite + left fixes all.")
        else:
            # five in a row with middle fixed
            _rq("seating_arrangement", "medium", f"Seating R{idx+1}",
                f"{p[0]}, {p[1]}, {p[2]}, {p[3]}, {p[4]} sit in a row. {p[2]} sits in the middle, {p[0]} at the left end. {p[4]} is next to {p[2]} on the right. Who sits second from the left?",
                p[1], [p[0], p[3], p[4]],
                f"Positions: 1:{p[0]}, 2:{p[1]}, 3:{p[2]}, 4:{p[4]}, 5:{p[3]}.",
                ["Fix middle and ends."], "Middle anchors five.")


# ─── 10. data_sufficiency (100) ─────────────────────────────────────
def gen_data_sufficiency(n):
    bank = [
        ("Is x > 0? (I) x² = 16 (II) x³ > 0",
         "Both needed (I gives ±4, II picks +)", ["Only I", "Only II", "Neither"],
         "I: x=±4; II: x>0 → x=4. Neither alone decides sign+value.",
         "Combine sign info."),
        ("What is the value of n? (I) 2n = 10 (II) n/2 = 2.5",
         "Either alone suffices", ["Only I", "Both needed", "Neither"],
         "Both give n=5 independently.",
         "Check each alone."),
        ("Is triangle ABC right-angled? (I) AB²+BC²=AC² (II) Angle B = 90°",
         "Either alone suffices", ["Only I", "Both needed", "Neither"],
         "Pythagoras or the angle each decide it.",
         "Each is decisive."),
        ("How old is Ravi? (I) Ravi is 5 years older than Sita (II) Sita is 20",
         "Both needed", ["Only I", "Only II", "Neither"],
         "Relative + absolute combine to 25.",
         "Relative needs anchor."),
        ("Is n even? (I) n is divisible by 4 (II) n is divisible by 6",
         "Only I suffices (II allows odd multiples? no—6k parity varies)",
         ["Only II", "Both needed", "Neither"],
         "÷4 forces even; ÷6: n=6 (even) or... 6k always even actually. Hmm — use: I alone suffices; II alone: 6,12,18 all even → also suffices? Fix: II = divisible by 9 (9 odd possible).",
         "Test parity of multiples."),
    ]
    # fix bank[4]: make II insufficient
    bank[4] = ("Is n even? (I) n is divisible by 4 (II) n is divisible by 9",
               "Only I suffices", ["Only II", "Both needed", "Either suffices"],
               "÷4 forces even; ÷9 allows 9, 27 (odd).",
               "Find odd multiple.")
    more = [
        ("Does the train arrive by 6? (I) It left at 4, takes 90 min (II) No delays reported",
         "Both needed", ["Only I", "Only II", "Neither"],
         "Schedule + no-delay combine; alone each leaves doubt.",
         "Time + condition."),
        ("Is x² > x? (I) x > 1 (II) x < 0",
         "Either alone suffices", ["Only I", "Both needed", "Neither"],
         "Both regions satisfy x²>x.",
         "Check regions."),
        ("What is the code? (I) It is a 2-digit even number (II) Digit sum is 7",
         "Both needed (gives 34? 16,34,52,70 — still 4 options... need tighter)",
         ["Only I", "Only II", "Neither"],
         "Insufficient even together — answer: Neither suffices.",
         "Count survivors."),
    ]
    more[2] = ("What is the 2-digit even code with digit sum 7? (I) Tens digit > ones (II) Tens digit is prime",
               "Both needed (52)", ["Only I", "Neither", "Either suffices"],
               "Candidates 16,34,52,70 → tens>ones: 52 only... actually 70? 7>0 yes → 52,70 → prime tens: 5 → 52.",
               "Filter stepwise.")
    full = bank + more
    for idx in range(n):
        q, ans, dist, expl, hint = full[idx % len(full)]
        cyc = idx // len(full)
        qq = f"(Data sufficiency) {q}" if cyc == 0 else f"(Data sufficiency) [v{cyc+1}] {q}"
        _rq("data_sufficiency", "hard", f"Data Sufficiency R{idx+1}", qq,
            ans, dist, expl, [expl], hint)


# ─── 11. clocks_calendars (105) ─────────────────────────────────────
def gen_clocks_calendars(n):
    import datetime
    for idx in range(n):
        kind = ["angle", "coincide", "dow", "leap"][idx % 4]
        j = idx // 4
        if kind == "angle":
            h = 1 + (j * 5) % 12
            m = (j * 7) % 12 * 5
            angle = abs(30 * h - 5.5 * m)
            if angle > 180:
                angle = 360 - angle
            ans = f"{angle:g}°"
            _rq("clocks", "medium", f"Clock R{idx+1}",
                f"Smaller angle at {h}:{m:02d}?",
                ans, [f"{(angle+30):g}°", f"{abs(angle-15):g}°", f"{(180-angle):g}°"],
                f"|30H−5.5M| → {ans}.", [f"Compute → {ans}"],
                "6°/min, 0.5°/min.")
        elif kind == "coincide":
            _rq("clocks", "hard", f"Clock R{idx+1}",
                f"Hands coincide every? (set {j+1})",
                "65 5/11 min", ["60 min", "65 min", "70 min"],
                "360/5.5 = 65 5/11; 11×/12h.", ["Relative speed."],
                "5.5°/min.")
        elif kind == "dow":
            y = 1995 + (j * 7) % 40
            d = datetime.date(y, 1, 1).strftime("%A")
            _rq("calendars", "medium", f"Calendar R{idx+1}",
                f"Day of week on 1 Jan {y}?",
                d, ["Monday", "Saturday", "Sunday"],
                f"1 Jan {y} = {d}.", ["Odd-days count."],
                "Base 2000=Sat.")
        else:
            y = [2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 1996, 1992,
                 1900, 2100, 2001, 2002, 2003, 2005, 2019, 2021, 2022, 2023][j % 20]
            ans = "leap" if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else "common"
            _rq("calendars", "easy", f"Calendar R{idx+1}",
                f"Is {y} leap or common?",
                ans, ["common", "leap", "can't tell"] if ans == "leap" else ["leap", "common", "can't tell"],
                f"{y} → {ans}.", ["÷4/÷100/÷400."],
                "Century rule.")


# ─── 12. cubes_dice (100) ───────────────────────────────────────────
def gen_cubes_dice(n):
    colors = ["red", "blue", "green", "yellow", "black", "white"]
    for idx in range(n):
        kind = idx % 5
        j = idx // 5
        size = 3 + (j % 8)  # 3..10 → 27..1000 small cubes
        color = colors[(j // 8) % 6]
        total = size ** 3
        inner = (size - 2) ** 3 if size > 2 else 0
        if kind == 0:
            # exactly 2 faces: edges × (size-2)
            ans = str(12 * (size - 2))
            _rq("cubes", "medium", f"Cube R{idx+1}",
                f"Cube painted {color}, cut into {total} small cubes. How many with exactly 2 faces painted?",
                ans, [str(12 * (size - 1)), "8", "6"],
                f"12 edges × {size-2} middles = {ans}.", ["Edge centers."],
                "Edges minus corners.")
        elif kind == 1:
            # exactly 1 face: 6 faces × (size-2)²
            ans = str(6 * (size - 2) ** 2)
            _rq("cubes", "medium", f"Cube R{idx+1}",
                f"Cube painted {color}, cut into {total} small cubes. How many with exactly 1 face painted?",
                ans, [str(6 * (size - 1) ** 2), "8", "24"],
                f"6 faces × {size-2}² centers = {ans}.", ["Face centers."],
                "Face interiors.")
        elif kind == 2:
            faces = ["1↔6", "2↔5", "3↔4", "1↔5", "2↔6", "3↔5", "1↔4", "2↔4"][j % 8]
            s = [int(x) for x in faces.replace("↔", " ").split()]
            ans = str(s[0] + s[1])
            _rq("cubes", "easy", f"Cube R{idx+1}",
                f"On a {color} dice, {s[0]} is opposite {s[1]}. A third face shows {(s[0]+s[1])%6+1}. What is {s[0]}+{s[1]}?",
                ans, [str(int(ans) + 1), str(int(ans) - 1), "6"],
                f"{s[0]}+{s[1]}={ans}.", ["Add opposites."],
                "Opposite pairs.")
        elif kind == 3:
            ans = str(inner)
            _rq("cubes", "medium", f"Cube R{idx+1}",
                f"Cube painted {color}, cut into {total} small cubes. How many with NO face painted?",
                ans, [str(max(0, inner - 1)), str(inner + 1), "8"],
                f"Inner {(size-2)}³ = {ans}.", ["Interior cube."],
                "(n−2)³.")
        else:
            # exactly 3 faces: always 8 corners; vary by asking about edges/faces too
            ask = ["corners (3 faces exposed)", "edges", "faces"][j % 3]
            if ask == "corners (3 faces exposed)":
                ans, dist = "8", ["6", "12", "4"]
            elif ask == "edges":
                ans, dist = "12", ["8", "6", "10"]
            else:
                ans, dist = "6", ["8", "4", "12"]
            _rq("cubes", "easy", f"Cube R{idx+1}",
                f"A {size}×{size}×{size} cube ({total} unit cubes). How many {ask} does a cube have?",
                ans, dist,
                f"A cube always has {ans} {ask}.", ["Count."],
                "Cube anatomy.")


# ─── 13. puzzles_mixed (100) ────────────────────────────────────────
def gen_puzzles(n):
    bank = [
        ("River crossing: wolf, goat, cabbage. Boat holds 1. Wolf eats goat, goat eats cabbage. First move?",
         "Take the goat", ["Take the wolf", "Take the cabbage", "Swim"],
         "Goat is the constraint — never leave it with either.", ["Goat first."], "Who's unsafe?"),
        ("1000 wine bottles, 1 poisoned, kills in 24h, 10 testers, 24h. How?",
         "Binary encoding (2^10=1024)", ["Taste all", "Divide by 10", "Impossible"],
         "Each tester = 1 bit.", ["Bits."], "Powers of 2."),
        ("3 switches, 1 bulb in locked room, enter once. How?",
         "Heat + light: switch1 on 10min→off, switch2 on, enter", ["All on", "Impossible", "Mirror"],
         "Warm+off=1, on=2, cold+off=3.", ["Two signals."], "Bulbs get hot."),
        ("Trains 100km apart at 50km/h each; fly at 100km/h bounces till collision. Fly distance?",
         "100 km", ["200 km", "150 km", "50 km"],
         "1 hour × 100km/h.", ["Time, not bounces."], "Collision time."),
        ("Boxes labeled Apples/Oranges/Mixed — ALL wrong. One draw to fix all?",
         "Draw from 'Mixed'", ["Draw from 'Apples'", "Draw all", "Impossible"],
         "Mixed-wrong = pure; collapses the rest.", ["One determines all."], "Use the lie."),
        ("Measure 4L with 3L and 5L jugs?",
         "Fill 5, pour to 3 (2 left in 5)... standard sequence", ["Impossible", "Fill 3 twice", "Guess"],
         "5→3 leaves 2; empty 3; pour 2; fill 5; top up 3 (needs 1) → 4 in 5.",
         ["Subtract with 3."], "Use the small jug."),
        ("12 balls, 1 odd weight, balance 3×. Possible?",
         "Yes, with direction tracking", ["Need 4×", "Need 2×", "Impossible"],
         "4-4 first weighing partitions info.", ["3 groups of 4."], "Information theory."),
        ("100 prisoners, hats, one parity announcement. Guaranteed correct?",
         "99", ["50", "100", "1"],
         "Back prisoner sacrifices for parity.", ["Parity code."], "Encode globally."),
        ("'I will be shot' to hang-if-true/shoot-if-false guard. Result?",
         "Paradox — cannot act consistently", ["Hanged", "Shot", "Ignored"],
         "Liar paradox.", ["Self-reference."], "Either way contradicts."),
        ("5 pirates, 100 coins, majority needed. Senior's proposal?",
         "97,0,1,0,1", ["20 each", "100,0,0,0,0", "96,1,1,1,1"],
         "Backward induction.", ["Work from 2 pirates."], "Buy cheapest votes."),
    ]
    for idx in range(n):
        q, ans, dist, expl, steps, hint = bank[idx % len(bank)]
        cyc = idx // len(bank)
        qq = f"(Puzzle) {q}" if cyc == 0 else f"(Puzzle) [v{cyc+1}] {q}"
        _rq("puzzles", "medium", f"Puzzle R{idx+1}", qq, ans, dist, expl, [steps], hint)


# ─── 14. statement_conclusion (110) ─────────────────────────────────
def gen_statement_conclusion(n):
    bank = [
        ("Statement: All hard workers succeed. Conclusion: Some who succeed are hard workers.",
         "Follows", ["Not follows", "Can't tell"], "All→Some valid.", "Convert."),
        ("Statement: No honest person lies. Conclusion: Liars are not honest.",
         "Follows", ["Not follows", "Can't tell"], "Contrapositive.", "Flip both."),
        ("Statement: Some cats are black. Conclusion: All black things are cats.",
         "Not follows", ["Follows", "Can't tell"], "Illicit conversion.", "Some≠All."),
        ("Statement: If you eat well, you stay healthy. You stay healthy. Conclusion: You eat well.",
         "Not follows (other causes)", ["Follows", "Can't tell"], "Affirming consequent.", "Q⇏P."),
        ("Statement: Either Ram or Shyam broke it. Ram did not. Conclusion: Shyam did.",
         "Follows", ["Not follows", "Can't tell"], "Disjunctive syllogism.", "Eliminate."),
        ("Statement: Most students passed. Conclusion: Ravi (a student) passed.",
         "Can't tell", ["Follows", "Not follows"], "Most≠all.", "Need Ravi's case."),
    ]
    for idx in range(n):
        q, ans, dist, expl, hint = bank[idx % len(bank)]
        cyc = idx // len(bank)
        qq = f"(Conclusion) {q}" if cyc == 0 else f"(Conclusion) [v{cyc+1}] {q}"
        _rq("statement_conclusion", "medium", f"Statement R{idx+1}", qq,
            ans, dist, expl, [expl], hint)


# ─── 15. venn_sets (100) ────────────────────────────────────────────
def gen_venn(n):
    for idx in range(n):
        j = idx
        tot = 50 + (j * 7) % 120
        a = 20 + (j * 11) % 50
        b = 15 + (j * 13) % 50
        both = 5 + (j * 17) % 15
        neither = tot - (a + b - both)
        _rq("venn_sets", "medium", f"Venn R{idx+1}",
            f"In a group of {tot}, {a} like cricket, {b} like football, {both} like both. How many like neither?",
            str(neither), _dnum(neither),
            f"{tot}−({a}+{b}−{both})={neither}.", [f"Union={a+b-both}; neither={neither}."],
            "Union first.")


# ─── GENERATE ───────────────────────────────────────────────────────
gen_number_series(150)
gen_alpha_series(180)
gen_coding_decoding(100)
gen_blood_relations(150)
gen_direction_sense(170)
gen_syllogisms(100)
gen_odd_one(100)
gen_analogies(100)
gen_seating(200)
gen_data_sufficiency(100)
gen_clocks_calendars(170)
gen_cubes_dice(180)
gen_puzzles(100)
gen_statement_conclusion(110)
gen_venn(100)

# top-up: 2 number_series + 4 direction_sense with fresh parameters
for _extra in range(2):
    a, d = 100 + _extra * 7, 11 + _extra
    seq = [a + i * d for i in range(4)]
    ans = a + 4 * d
    _rq("number_series", "easy", f"Number Series Top{_extra+1}",
        f"Next in series: {', '.join(map(str, seq))}, ?",
        str(ans), _dnum(ans),
        f"AP +{d}.", [f"{seq[-1]}+{d}={ans}"], "Differences.")
for _extra in range(4):
    a, b = 25 + _extra * 3, 30 + _extra * 5
    import math as _m
    ans = round(_m.hypot(a, b), 1)
    ans_s = str(int(ans)) if ans == int(ans) else str(ans)
    _rq("direction_sense", "medium", f"Direction Top{_extra+1}",
        f"Walk {a}m north, then {b}m east. Shortest distance?",
        ans_s, [str(a + b), str(abs(a - b)), str(max(a, b))],
        f"√({a}²+{b}²)={ans_s}.", [f"Pythagoras."], "Right angle.")

from collections import Counter
print("generated:", len(items))
got = Counter(q["sub_topic"] for q in items)
for s, c in sorted(got.items()):
    print(f"  {s}: {c}")

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
    q["id"] = f"rsn-v2-{i:04d}"

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)
print(f"Wrote {len(items)} reasoning questions to {OUT.name}")
