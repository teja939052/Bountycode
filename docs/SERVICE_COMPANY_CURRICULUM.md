# BountyCode — Service-Company Placement Curriculum (Canonical)

**Status:** LOCKED for content direction  
**Audience:** Content authors, curriculum engineers, product  
**Primary goal:** Take a complete beginner to job-ready for Indian service-based companies (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini, HCL, Tech Mahindra, LTIMindtree, Mphasis).

This document is the single source of truth for **what** we teach and in **what order**.  
It sits under the product vision in `docs/BOUNTYCODE_VISION_LOCK.md` and the learning standard in `docs/learning/LEARNING_EXPERIENCE_STANDARD.md`.

---

## 1. Product promise (one sentence)

A student who starts with zero coding knowledge can follow one coherent path, master every concept that service companies actually test, prove readiness with timed mocks, and walk into the interview prepared.

---

## 2. Competitive reality we are beating

Existing platforms mostly sell:
- Question dumps
- Pattern notes
- Timed mocks

Almost none deliver:
- Deep interactive teaching from zero
- Mental models + visualization
- Guided practice → transfer → mastery
- Misconception diagnosis + repair
- Evidence-based company readiness

BountyCode wins by being the **learning system**, not another question bank.

---

## 3. The only acceptable lesson quality

Every released lesson must follow the World-1 standard already proven in the repo:

1. Outcome / learning objective  
2. Prerequisite check  
3. Intuition + mental model  
4. Worked example with narration  
5. Interactive step (predict / manipulate / select)  
6. Build / code exercise with hidden tests  
7. Break (common failure mode)  
8. Debug  
9. Retrieve (recall without looking)  
10. Transfer (new problem, same concept)  
11. Mastery check (unseen questions)  
12. Spaced-repetition tag

No title-only lessons. No "All of the above" quizzes. No unverified answer keys.  
XP and progression are awarded only for verified evidence.

---

## 4. Curriculum spine (ordered)

### Phase A — Absolute foundations (must be world-class)

| Module | What the student can do at the end |
|--------|-------------------------------------|
| Computer & program basics | Explain hardware vs software, source vs executable, syntax vs logic errors |
| Variables & state | Store, reassign, and reason about values |
| Control flow | Conditionals, loops, nested logic |
| Functions | Parameters, return values, scope |
| Basic data in language | Strings, lists/arrays, simple maps |
| Debugging fundamentals | Read errors, dry-run, fix off-by-one and type mistakes |

**Languages (same concepts, language-specific differences):**  
Primary teaching language: **Python**  
Interview languages: **Java**, **C++**, **C**  
(Do not duplicate identical lessons under five language names.)

### Phase B — Programming logic (heavily tested by service companies)

- Output prediction / dry-run  
- Simple algorithms (factorial, reverse, palindrome, max/min, frequency)  
- Nested loops and pattern printing (classic written-test style)  
- Basic recursion  
- Time complexity intuition (O(1), O(n), O(n²))

### Phase C — Core DSA patterns (enough to clear coding rounds)

Priority order:
1. Arrays & hashing  
2. Strings  
3. Two pointers  
4. Sliding window  
5. Sorting & searching (binary search)  
6. Stack & queue  
7. Linked list basics  
8. Basic recursion / backtracking  
9. Trees (basics only for most service roles)  
10. Simple DP patterns (climbing stairs, knapsack intro)

Depth stops at the level required by TCS Digital / Infosys Power Programmer / Wipro coding rounds. Advanced graph / hard DP is post-placement stretch content.

### Phase D — Quantitative aptitude (full NQT depth)

Number system, percentages, ratio & proportion, averages, profit & loss, simple & compound interest, time & work, time-speed-distance, mixtures, permutations & combinations, probability, data interpretation, elementary statistics, basic geometry/mensuration.

Every topic: concept → formula derivation → shortcuts → progressive difficulty → timed sets.

### Phase E — Logical reasoning (full NQT depth)

Number/letter series, coding-decoding, blood relations, direction sense, seating (linear + circular), puzzles, syllogisms, statements & conclusions, data sufficiency, analogy, odd-one-out, clocks & calendars.

### Phase F — Verbal ability (current TCS-style)

Sentence completion, passage recall, professional email writing, error spotting, sentence correction, para-jumbles, reading comprehension, vocabulary in context, grammar (subject-verb, tenses, articles, prepositions).

### Phase G — CS fundamentals (interview + written)

- OOP (classes, inheritance, polymorphism, encapsulation)  
- SQL (SELECT, JOIN, GROUP BY, subqueries, basic optimization)  
- DBMS (keys, normalization, transactions, ACID)  
- OS (processes, threads, scheduling, memory, deadlock)  
- Networks (OSI/TCP-IP, IP, HTTP, DNS basics)

### Phase H — Company pathways + mocks

For each major recruiter:
- Verified assessment pattern (source + last-verified date)  
- Section-wise skill mapping  
- Timed full mock  
- Diagnosis → repair path  
- Technical + HR interview practice

Companies in priority order:  
TCS (Ninja / Digital / Prime) → Infosys → Wipro → Accenture → Cognizant → Capgemini → HCL → Tech Mahindra → LTIMindtree → Mphasis.

---

## 5. Personalization & mastery rules (non-negotiable)

- Diagnostic assessment before the main path.  
- Prerequisites block progress.  
- Mastery requires independent, repeated evidence (not one lucky quiz).  
- Wrong answers produce a specific misconception diagnosis and a repair set.  
- Readiness score is company-weighted and evidence-based.  
- Gamification rewards verified learning only.

---

## 6. Content ownership & single source of truth

| Layer | Location |
|-------|----------|
| Interactive teaching lessons | `backend/app/content/world*.py` + `world_registry.py` |
| Traditional track lessons (if still used) | `backend/app/services/lessons/` (must meet same quality bar or be retired) |
| Question bank | File-based under `backend/app/content/questions/` and `backend/app/data/` — only TRUSTED items served |
| Company blueprints | `backend/app/content/company_journeys.py` + role packages |
| Learning standard | `docs/learning/LEARNING_EXPERIENCE_STANDARD.md` |

No parallel curriculum. No second mastery system.

---

## 7. Release order (what we build next)

1. **Hygiene complete** — live catalog contains only real content; prerequisites clean; only verified questions served.  
2. **Phase A complete** at World-1 quality (Programming Foundations).  
3. **Phase D + E + F** (Aptitude + Reasoning + Verbal) to full NQT depth.  
4. **Phase B + C** (Programming logic + Core DSA patterns).  
5. **Phase G** (CS fundamentals).  
6. **Phase H** (Company pathways + full mocks with repair).  
7. Continuous quality, analytics, and outcome measurement.

---

## 8. Definition of "done" for any module

- Every concept has at least one full-standard interactive lesson.  
- Progressive exercises and unseen mastery checks exist.  
- Common misconceptions are documented and tested.  
- Prerequisites are enforced.  
- Timed practice sets exist for the module.  
- Company mapping (which companies test this) is recorded with source.  
- A student can go from zero on that module to consistent first-attempt success on new questions.

---

*This document supersedes any earlier vague "A–Z" claims. Content work that does not serve this spine is out of scope until the spine is complete.*
