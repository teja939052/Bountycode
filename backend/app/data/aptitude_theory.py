"""Aptitude theory cards — versioned file content, loaded at import.

Crisp theory for NQT-style screening: definition, key formulas, one worked
example, recognition triggers, common pitfalls. Served read-only via
``GET /api/v1/aptitude/theory`` — no database, no LLM, no new systems.
"""

THEORY = [
    {
        "id": "percentages",
        "title": "Percentages",
        "category": "quantitative",
        "definition": "A percentage expresses a part out of 100. x% of N means (x/100) × N.",
        "formulas": [
            "x% of N = (x × N) / 100",
            "Percentage change = ((New − Old) / Old) × 100",
            "Successive changes a% then b%: net = a + b + (a×b)/100",
            "1/2=50%, 1/3≈33.33%, 1/4=25%, 1/5=20%, 1/8=12.5%, 1/10=10%, 1/20=5%",
        ],
        "worked_example": {
            "problem": "A salary rises from ₹40,000 to ₹46,000. Percentage increase?",
            "solution": "Change = 6,000. (6,000 / 40,000) × 100 = 15%.",
        },
        "triggers": ["'percent of', 'increase/decrease by %'", "successive discounts or hikes"],
        "pitfalls": ["Applying % to the new value instead of the original base"],
        "practice_category": "quantitative",
    },
    {
        "id": "ratios-proportion",
        "title": "Ratios & Proportion",
        "category": "quantitative",
        "definition": "A ratio a:b compares two quantities. A proportion states two ratios are equal: a/b = c/d.",
        "formulas": [
            "If a:b = 2:3 and total = 50, shares are (2/5)×50=20 and (3/5)×50=30",
            "Componendo-dividendo: if a/b = c/d then (a+b)/(a−b) = (c+d)/(c−d)",
            "Mean proportional of a,b = √(a×b)",
        ],
        "worked_example": {
            "problem": "Divide 90 in ratio 2:3:4.",
            "solution": "Sum = 9. Shares: (2/9)×90=20, (3/9)×90=30, (4/9)×90=40.",
        },
        "triggers": ["'divide in the ratio', 'proportional to'", "mixtures and partnerships"],
        "pitfalls": ["Forgetting to add all ratio parts before dividing the total"],
        "practice_category": "quantitative",
    },
    {
        "id": "profit-loss",
        "title": "Profit & Loss",
        "category": "quantitative",
        "definition": "Profit = Selling Price − Cost Price. All percentages are computed on Cost Price unless stated otherwise.",
        "formulas": [
            "Profit% = ((SP − CP) / CP) × 100",
            "Loss% = ((CP − SP) / CP) × 100",
            "SP = CP × (1 + profit%/100); CP = SP / (1 + profit%/100)",
            "Discount% is always on Marked Price, then profit% on CP",
        ],
        "worked_example": {
            "problem": "Bought for ₹800, sold for ₹920. Profit%?",
            "solution": "Profit = 120. (120/800) × 100 = 15%.",
        },
        "triggers": ["'marked price', 'discount', 'sold at a gain/loss of'"],
        "pitfalls": ["Computing profit% on SP instead of CP"],
        "practice_category": "quantitative",
    },
    {
        "id": "averages",
        "title": "Averages",
        "category": "quantitative",
        "definition": "Average = Sum of observations / Number of observations. Adding or removing values shifts the average predictably.",
        "formulas": [
            "Average = Sum / n, so Sum = Average × n",
            "If average of n values rises by d after adding one value, new value = old average + (n+1)×d",
            "Average of first n naturals = (n+1)/2; first n even = n+1; first n odd = n",
        ],
        "worked_example": {
            "problem": "Average of 5 numbers is 27. A 6th number makes it 29. The 6th number?",
            "solution": "New sum − old sum = 29×6 − 27×5 = 174 − 135 = 39.",
        },
        "triggers": ["'average age/score', 'a new member joins'"],
        "pitfalls": ["Averaging the averages of unequal-sized groups directly"],
        "practice_category": "quantitative",
    },
    {
        "id": "time-work",
        "title": "Time & Work",
        "category": "quantitative",
        "definition": "If A finishes work in n days, A's 1-day work = 1/n. Add rates when people work together.",
        "formulas": [
            "Combined 1-day work = 1/a + 1/b; days together = (a×b)/(a+b)",
            "Work = Rate × Time; Men × Days = constant for fixed work",
            "A is twice as efficient as B → A takes half the time B takes",
        ],
        "worked_example": {
            "problem": "A does a job in 10 days, B in 15. Together?",
            "solution": "Rate = 1/10 + 1/15 = 5/30 = 1/6 → 6 days.",
        },
        "triggers": ["'together', 'pipes and cisterns' (same math with signs)"],
        "pitfalls": ["Subtracting days instead of adding rates"],
        "practice_category": "quantitative",
    },
    {
        "id": "time-speed-distance",
        "title": "Time, Speed & Distance",
        "category": "quantitative",
        "definition": "Distance = Speed × Time. For fixed distance, speed and time are inversely proportional.",
        "formulas": [
            "D = S × T; average speed for equal distances = 2ab/(a+b)",
            "km/h → m/s: multiply by 5/18; m/s → km/h: multiply by 18/5",
            "Relative speed: towards each other add; same direction subtract",
            "Trains: crossing a pole uses train length; crossing a platform uses train + platform length",
        ],
        "worked_example": {
            "problem": "60 km at 40 km/h, back at 60 km/h. Average speed?",
            "solution": "2×40×60/(40+60) = 4800/100 = 48 km/h (not 50).",
        },
        "triggers": ["'upstream/downstream' (boat speed ± stream)", "'trains cross'"],
        "pitfalls": ["Taking the simple mean of two speeds for a round trip"],
        "practice_category": "quantitative",
    },
    {
        "id": "si-ci",
        "title": "Simple & Compound Interest",
        "category": "quantitative",
        "definition": "SI pays interest on principal only; CI pays interest on accumulated amount each period.",
        "formulas": [
            "SI = (P × R × T) / 100",
            "CI amount = P × (1 + R/100)^T",
            "CI − SI for 2 years = P × (R/100)²",
            "Doubling: Rule of 72 → years ≈ 72 / rate",
        ],
        "worked_example": {
            "problem": "₹10,000 at 10% for 2 years, compounded annually. Amount?",
            "solution": "10,000 × 1.1² = 10,000 × 1.21 = ₹12,100.",
        },
        "triggers": ["'compounded half-yearly' → halve rate, double periods"],
        "pitfalls": ["Using annual rate with half-yearly periods unchanged"],
        "practice_category": "quantitative",
    },
    {
        "id": "number-series",
        "title": "Number Series",
        "category": "quantitative",
        "definition": "Find the rule linking consecutive terms: difference, ratio, squares, cubes, primes, or interleaved sequences.",
        "formulas": [
            "Check differences first, then ratios, then squares/cubes near terms",
            "n² series: 1, 4, 9, 16, 25…; n³: 1, 8, 27, 64…; primes: 2, 3, 5, 7, 11…",
            "Alternating two series interleaved is a classic NQT trap",
        ],
        "worked_example": {
            "problem": "2, 6, 12, 20, 30, ?",
            "solution": "Gaps 4, 6, 8, 10 → next gap 12 → 30 + 12 = 42.",
        },
        "triggers": ["steady growing gaps → second differences", "×2±1 patterns"],
        "pitfalls": ["Assuming one rule — always test alternates"],
        "practice_category": "quantitative",
    },
    {
        "id": "blood-relations",
        "title": "Blood Relations",
        "category": "logical",
        "definition": "Map every person to a family tree. Solve from the target person backwards through the clues.",
        "formulas": [
            "Draw symbols: □ male, ○ female, = marriage, | parent→child",
            "'Only son/daughter of X' collapses branches — use it first",
            "Coded relations: decode each symbol to a tree edge before combining",
        ],
        "worked_example": {
            "problem": "A is B's brother. B is C's mother. How is A related to C?",
            "solution": "A and B are siblings; B is C's mother → A is C's uncle.",
        },
        "triggers": ["'only', 'pointing to a photograph'"],
        "pitfalls": ["Assuming gender the statement never gives"],
        "practice_category": "logical",
    },
    {
        "id": "syllogism",
        "title": "Syllogisms",
        "category": "logical",
        "definition": "Decide which conclusions must follow from given statements. Draw Venn overlaps; a conclusion is valid only if true in every possible diagram.",
        "formulas": [
            "'All A are B' → A circle inside B; 'Some A are B' → circles overlap",
            "'No A is B' → disjoint; 'Some A are not B' → A extends outside B",
            "Two particular ('some') premises yield no universal conclusion",
        ],
        "worked_example": {
            "problem": "All pens are books. Some books are erasers. Conclusion: Some pens are erasers?",
            "solution": "Invalid — the eraser overlap may sit entirely outside pens.",
        },
        "triggers": ["'definitely follows' vs 'possibly follows'"],
        "pitfalls": ["Treating 'some' as 'some but not all'"],
        "practice_category": "logical",
    },
    {
        "id": "coding-decoding",
        "title": "Coding-Decoding",
        "category": "logical",
        "definition": "Letters map to other letters/numbers by a fixed rule — usually a positional shift. Write A=1…Z=26 and compare positions.",
        "formulas": [
            "Forward shift: CAT → DBU is +1 each (C→D, A→B, T→U)",
            "Reverse/mirror: A↔Z, B↔Y (position pairs summing to 27)",
            "Number codes often = position sums: CAT → 3+1+20 = 24",
        ],
        "worked_example": {
            "problem": "If DOG is coded as FQI, how is CAT coded?",
            "solution": "D→F +2, O→Q +2, G→I +2. CAT → ECV.",
        },
        "triggers": ["letter↔number mixes", "matrix coding (check rows and columns)"],
        "pitfalls": ["Assuming +1 shift before verifying all letters"],
        "practice_category": "coding-decoding",
    },
    {
        "id": "direction-sense",
        "title": "Direction Sense",
        "category": "logical",
        "definition": "Track position on a compass grid turn by turn. Draw the path; compute displacement with Pythagoras only at the end.",
        "formulas": [
            "Left/right turns rotate facing: N →(right)→ E → S → W → N",
            "Displacement = √(dx² + dy²) for perpendicular legs",
            "Shadow at sunrise falls west; at sunset falls east",
        ],
        "worked_example": {
            "problem": "Walk 3 km north, then 4 km east. Distance from start?",
            "solution": "√(9+16) = 5 km north-east.",
        },
        "triggers": ["'facing', 'to his left/right' (orientation, not map direction)"],
        "pitfalls": ["Adding leg lengths instead of computing displacement"],
        "practice_category": "logical",
    },
    {
        "id": "seating-arrangement",
        "title": "Seating Arrangement",
        "category": "logical",
        "definition": "Fix positions around a circle/line using definite clues first; keep 2 candidate diagrams when a clue is ambiguous, kill one as facts arrive.",
        "formulas": [
            "Circle facing center: right-hand side is anticlockwise",
            "Anchor on the most constrained person first",
            "'Between A and B' + 'second to the left' pins exact slots",
        ],
        "worked_example": {
            "problem": "A sits opposite B; C sits immediately right of A (facing center). Order?",
            "solution": "Going clockwise: A, C, …, B opposite A.",
        },
        "triggers": ["'immediate neighbour', 'second to the left of'"],
        "pitfalls": ["Mirroring left/right when people face outward vs inward"],
        "practice_category": "puzzles",
    },
    {
        "id": "series-completion",
        "title": "Series Completion (Reasoning)",
        "category": "logical",
        "definition": "Same engine as quant series plus letter series: convert letters to positions (A=1…Z=26) and run number-series logic.",
        "formulas": [
            "Letter gaps: B, D, G, K, P… gaps 2,3,4,5 → next gap 6 → V",
            "Figure series: track one element's rotation/position per step",
            "Alphabet + number combos decode each stream separately",
        ],
        "worked_example": {
            "problem": "A, C, F, J, O, ?",
            "solution": "Gaps +2,+3,+4,+5 → next +6 → O+6 = U.",
        },
        "triggers": ["mixed alphanumeric strings"],
        "pitfalls": ["Reading figures as a whole instead of tracking one element"],
        "practice_category": "series-completion",
    },
    {
        "id": "reading-comprehension",
        "title": "Reading Comprehension",
        "category": "verbal",
        "definition": "Answer only what the passage supports. Read questions first, then scan for the answering lines.",
        "formulas": [
            "Main idea = repeated concept across paragraphs, usually paragraph 1 + last",
            "'According to the passage' → answer must be textually present",
            "Tone words: cautious (may, suggests) vs absolute (always, never)",
        ],
        "worked_example": {
            "problem": "Passage lists three causes of attrition. 'Which is NOT mentioned?'",
            "solution": "Eliminate the three named causes; the leftover option is the answer.",
        },
        "triggers": ["'infer', 'implies' → closest paraphrase, not outside knowledge"],
        "pitfalls": ["Picking true-in-real-life options the passage never states"],
        "practice_category": "reading-comprehension",
    },
    {
        "id": "para-jumbles",
        "title": "Para Jumbles",
        "category": "verbal",
        "definition": "Order shuffled sentences: find the opener (independent, introduces topic), then chain pronoun/linker connections.",
        "formulas": [
            "Opener: no pronouns (it/they/this) pointing backwards, no 'however/therefore'",
            "Mandatory pairs: full name → pronoun; question → answer; cause → effect",
            "Chronology and general→specific are tiebreakers",
        ],
        "worked_example": {
            "problem": "(A) He later patented it. (B) Edison tested 6,000 filaments. (C) The bulb glowed 13 hours.",
            "solution": "B opens (names Edison), C continues (it=bulb), A closes → B-C-A.",
        },
        "triggers": ["concluding lines: 'thus', 'in summary'"],
        "pitfalls": ["Starting with a sentence that contains 'it' or 'they'"],
        "practice_category": "para-jumbles",
    },
    {
        "id": "sentence-correction",
        "title": "Sentence Correction",
        "category": "verbal",
        "definition": "Pick the grammatically sound version: subject-verb agreement, tense consistency, parallelism, modifier placement.",
        "formulas": [
            "Neither/either + singular verb; 'each/every' + singular",
            "Parallel lists keep one form: 'to read, to write, to speak'",
            "Compare like with like: ' Ram's score is higher than Shyam's' (not 'than Shyam')",
        ],
        "worked_example": {
            "problem": "Neither of the answers (is/are) correct.",
            "solution": "'Neither' is singular → 'is'.",
        },
        "triggers": ["underlined-phrase variants differing in one word"],
        "pitfalls": ["Choosing the wordiest option — brevity usually wins ties"],
        "practice_category": "sentence-correction",
    },
    {
        "id": "email-format",
        "title": "Email Writing (TCS-style)",
        "category": "verbal",
        "definition": "NQT email writing is graded on structure: subject, greeting, purpose, 3 key points covered, closing. Formal tone, 70–100 words.",
        "formulas": [
            "Subject: crisp noun phrase naming the request",
            "Body: greeting → one-line purpose → cover every keyword from the prompt → polite closing",
            "Never: slang, texting abbreviations, missing sign-off",
        ],
        "worked_example": {
            "problem": "Write to HR requesting a shift change citing health, transport, notice period.",
            "solution": "Subject: Request for shift change. Dear Sir/Madam, I request… (health)… (transport)… I will serve the full notice… Regards, Name.",
        },
        "triggers": ["prompts listing 3 bullet facts — all three must appear"],
        "pitfalls": ["Dropping one prompt keyword — each is worth marks"],
        "practice_category": "verbal",
    },
]


def get_theory_topics():
    """Lightweight topic list for the theory index."""
    return [
        {"id": t["id"], "title": t["title"], "category": t["category"]}
        for t in THEORY
    ]


def get_theory(topic_id: str):
    """Full theory card for one topic, or None."""
    tid = (topic_id or "").strip().lower()
    for t in THEORY:
        if t["id"] == tid:
            return t
    return None


def get_theory_by_category(category: str):
    """Theory cards matching a practice category (for 'learn first' wiring)."""
    cat = (category or "").strip().lower()
    return [t for t in THEORY if t["category"] == cat or t["practice_category"] == cat]
