# BountyCode — Vision Lock

**Status:** LOCKED  
**Launch Date:** October 18, 2026  
**Authority:** This document supersedes all prior positioning, strategy, and vision docs. No pivots before launch.

---

## North Star (verbatim)

> BountyCode is an interactive placement-preparation platform for Indian engineering students targeting service-based and mass-recruiting companies — structured, visually-taught patterns like AlgoMaster, personalized to your role/company/language, with a game layer that makes daily practice a habit. Built for the TCS/Infosys/Wipro/Cognizant/Capgemini/Accenture pipeline that FAANG platforms ignore.

Check every feature against this sentence before building it. No exceptions.

---

## Core Loop — this is the product, not the worlds

```
Company → Blueprint → Skill → Pattern → Interactive Lesson →
Practice → Assessment → Evidence → Diagnosis → Repair → Retest → Readiness
```

Game wraps it: Mission → Progression → XP → Streak → Rank → Unlock.  
Game = retention layer, not product.

---

## Information Architecture — single hierarchy

```
COMPANY (tcs, accenture, infosys, wipro, cognizant, capgemini, hcl, techm, lti, mphasis)
  ↓
ASSESSMENT BLUEPRINT (sections, timing, skill weights, thresholds)
  ↓
SKILL (aptitude_numerical, reasoning, verbal, pseudo_code, dsa, cs_fundamentals)
  ↓
PATTERN (Two Pointers, Blood Relation, Email Format, Trace Variables)
  ↓
INTERACTIVE LESSON (template below)
  ↓
PRACTICE (TRUSTED questions only)
  ↓
MOCK (company-style timed)
  ↓
EVIDENCE (attempts, failure_mix, heatmap)
  ↓
READINESS (deterministic, no LLM probability)
```

**Single World Registry Rule:** `WORLD_REGISTRY` = 6 worlds, 50-60 levels. All adapters read this. Delete Registry B as separate source after migration, merge its 132 lessons INTO Registry A levels. No parallel registries.

---

## Worlds — 6 worlds for launch, not 12

### World 1 — Quantitative Aptitude
Patterns: Percentages, Ratios, Profit/Loss, Averages, Time & Work, Time Speed Distance, SI/CI, Number Series  
- Animation: visual bar for %, work rate diagram

### World 2 — Logical Reasoning
Patterns: Blood Relations, Syllogism, Coding-Decoding, Directions, Seating, Series, Data Sufficiency  
- Animation: family tree, Venn

### World 3 — Verbal
Patterns: Grammar, Reading Comprehension, Para Jumble, Sentence Correction, Vocabulary, Email Format  
- Animation: email structure blocks

### World 4 — Pseudocode / Programming Logic [DIFFERENTIATOR]
Patterns: Trace Variables, Predict Output, Loops, Nested Loops, Arrays, Conditions, Functions, Recursion basics, Debugging  
- Animation: variable table updating step-by-step — this is your 600 animations equivalent. Build 15 excellent.

### World 5 — Easy/Med DSA [Service-level only]
Patterns: Arrays, Strings, Hashing, Two Pointers, Sliding Window, Sorting, Binary Search, Stack/Queue basics, Linked List basics, Tree basics  
- Animation: pointer movement, window sliding

### World 6 — Company Simulation
TCS NQT, Accenture, Infosys, Wipro, Cognizant. Not question dump — blueprint-driven mock.

---

## Lesson Template — every lesson uses this

1. What is it? — 1 sentence definition
2. Why does it work? — intuition
3. How to recognize? — triggers
4. See — animation (mandatory for W4, optional for others at launch)
5. Interact — manipulate variables
6. Predict — what happens next?
7. Solve — build it (code/answer)
8. Break — deliberately break it
9. Debug — fix it
10. Recall — 1-min SRS prompt
11. Transfer — new problem same pattern
12. Prove — timed check, counts for readiness

**Fields in `world.py`:** Only `discover/manipulate/predict/build/break/debug/retrieve/transfer/mastery` — but at launch only implement 1,4,5,6,7,12 fully. Rest = future. Don't ship dead fields.

---

## Content Governance — trust gate is load-bearing

```
UNVERIFIED → AUTOMATED_CHECKED (Piston runs, expected_output matches) → HUMAN_REVIEWED → TRUSTED
```

- Only TRUSTED serves to students.
- Every question MUST have `source_url`, `company`, `section`, `topic`, `difficulty`, `expected_output` for coding.
- Company-pattern practice = original question matching pattern. Label: "Company-pattern practice" NOT "Asked at TCS" unless evidence.
- No scraping copyrighted text. No LLM-authored bank.

**Question Schema:**
`slug, company, section, topic, difficulty, question_text, options, correct_answer, explanation, expected_output, source_url, year, trust_status`

---

## Company Blueprint — measurement config, not employer claim

Each company in `role_packages.py`:

```
accenture: weights {verbal 20%, pseudo 15%, reasoning 15%, numerical 15%, dsa 20%, cs_fund 15%}, critical [verbal, pseudo, dsa], pattern: Cognitive + Technical + Coding
tcs: weights {numerical 20%, verbal 15%, reasoning 15%, dsa 15%, pseudo 10%, email 10%, cs 15%}
```

**Label in-code:** "Platform measurement config". This feeds deterministic readiness you already proved: same evidence → Frontend+Google 9.6/12.2% vs Backend+Amazon 14.0/23.9%.

---

## Gamification — retention, not differentiation

- Diamonds: `record_practice("lesson", 10.0) → base 75 × streak/combo/crit` — display = real. The canonical reward unit is diamonds.
- Stars: 3 iff best≥85 and ≤1 hint, else 2/1.
- Unlock: strict linear chain. `unlocks_town/unlocks_world` currently dead — delete or implement.
- Streak, daily challenge (5-15 min), league — keep existing, no new economies.
- Single writer of XP: gamification_core only. No frontend-calculated XP.

---

## Personalization Adapters

- **RoleAdapter:** remaps world content (frontend skips advanced SQL)
- **CompanyAdapter:** overlays company weights + practice set + mock structure
- **LanguageAdapter:** Python vs Java syntax
- **ReadinessEngine:** score, coverage, status DEVELOPING/INSUFFICIENT_EVIDENCE, blockers, next_action {type: repair, skill_id}
- **Evidence:** heatmap [{pattern_id, accuracy, attempts, color yellow/insufficient}], failure_mix {SUCCESS, WRONG_ANSWER, TIMEOUT}, improvement {sufficient}

You already have runtime verification:
- runtime_user_a: 3 events, 4 submissions, score 22.0, coverage 45.2%
- runtime_user_zero: score 5.0, coverage 0.0%, status INSUFFICIENT_EVIDENCE, no fake weakness.

---

## Repair Loop — first-class

Fail → diagnose (failure_mix) → repair (3 targeted exercises) → retest → mastery → readiness moves. Two repair systems currently unlinked — unify to persisted repair_missions. Quiz finder must respect skill arg.

---

## Mocks & Readiness

Mock = blueprint timing + section weights. Generates from TRUSTED bank filtered by company relevance. After mock → evidence → readiness + blockers + next_action.

Readiness Dashboard needs:
- `api.evidence.getMyPerformance()` for skill patterns
- `api.progress.getHeatmap()` for daily activity (you fixed wiring)

---

## API & Frontend Routes

**Backend:**
- `GET /companies`
- `GET /companies/:slug`
- `GET /companies/:slug/questions?section=&trust=TRUSTED`
- `GET /evidence/my-performance`
- `GET /progress/heatmap`
- `POST /admin/companies/import` (trust gate)

**Frontend:**
- `/companies`
- `/companies/:slug` (readiness for company + syllabus + next action)
- `/companies/:slug/practice`
- `/companies/:slug/mock`
- `/evidence` (you built 19.14 kB)
- `/learn/world/:id/level/:id`

---

## What to STOP / START

### STOP
- Two parallel registries
- Generic one-world-fits-all
- Dead API stubs
- 6389 unverified questions served
- New gamification mechanics
- FAANG-first positioning

### START
- Single registry + adapters
- Skill XP visible
- Company-tagged sets with mocks
- Repair as first-class
- Outcome certificates (post-launch)
- Interest graph recommending weakest pattern

---

## Launch Scope Oct 18 — MUST BE GREAT

1. Worlds 1-5 with 5-10 excellent lessons each (not 132 thin)
2. World 6: TCS + Accenture blueprints excellent, others weights only
3. Interactive engine + in-browser judge (Piston) + failure_mix
4. Mock → diagnosis → repair → retest → readiness
5. Evidence dashboard
6. Accounts + live smoke with real numbers

Everything else post-launch.

---

## Migration Plan — no destructive rewrite

1. Fix P0: repair_service phantom import, B-NEXT dead link, /lesson/complete orphan keys, /study/activity not advancing
2. Create adapter layer reading single WORLD_REGISTRY
3. Migrate 132 B lessons INTO A levels — mapping file `registry_migration_map.json`
4. Tag levels with `company_relevance` and `role_relevance`
5. Delete shadow WORLD_* objects, foundations_world.py, curriculum_50_levels side effect after tests green
6. 69/69 + 2 company profile tests green = deploy

---

## Metrics — what proves thesis

- D7 retention: daily challenge completion
- Repair effectiveness: fail → repair → retest delta
- Readiness trust: student says score matches real mock performance
- Free tier placement: can student place using only free?

---

## Verification Standard

Compile/build success is not sufficient, ever. Every critical loop needs runtime evidence:
student action → database state → returned API state → UI result → next state.

A claim that "should work" or "same code path as X" is not evidence.

---

## Final Launch Gate

A real student, on a real mobile device, must be able to:
1. Choose a company
2. Follow the recommended path
3. Complete a real interactive lesson
4. Practice
5. Take a mock
6. Receive a real weakness diagnosis
7. Complete repair
8. Retest
9. See readiness/evidence actually change

— without breaking state, rewards, progress, or navigation.

That's the whole bar. Once it's true, the patient content-building phase begins. October 18 is proof-of-product, not the finished company.
