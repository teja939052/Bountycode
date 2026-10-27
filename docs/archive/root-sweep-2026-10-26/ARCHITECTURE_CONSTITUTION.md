# ARCHITECTURE_CONSTITUTION

> **THIS IS THE ONLY ARCHITECTURAL AUTHORITY FOR THE STUDENT PRODUCT.**
> No agent, feature branch, or sprint may deviate from this document without explicit architectural approval.

---

## 1. PRODUCT IDENTITY

PlacementPro = **Personalized interactive service-based placement preparation.**

Primary commercial mode: **service-based placement prep**.

Supporting capabilities: Mock OA, AI Interview, Resume Analyzer, DSA Visual Lab.

Everything else is secondary or removed.

---

## 2. FOUR ENTRY MODES ONLY

After onboarding:

```
┌──────────────────────────────┐
│ 💻 LEARN CODING              │
│ Build programming ability    │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 🎯 SERVICE-BASED PREP        │
│ Aptitude + Reasoning +       │
│ Verbal + Coding + SQL/CS     │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 🏢 COMPANY / ROLE PREP       │
│ Target-specific preparation  │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 🧠 DSA VISUAL LAB            │
│ Explore algorithms visually  │
└──────────────────────────────┘
```

No fifth door. No separate Concept/Atom/CFIC/ThinkInCode/Scrimba/LearningHub/PrepHub/AdaptiveHub products.

Those are internal implementation concepts, not student destinations.

---

## 3. ONBOARDING — TINY

Question 1: What defines you?
- Student
- Professional
- Job Seeker

Question 2: What do you want to achieve?
- Learn Coding
- Service-Based Placement
- Specific Company
- Specific Role
- Not Sure

Question 3 (only when relevant): Target company / role

Then optional: “Find my level” → short adaptive diagnostic.

Onboarding places the learner. It does not collect life history.

---

## 4. PERSONALIZATION IS THE CORE ENGINE

Personalization determines what this student sees, learns, practices, reviews, and gets assessed on next.

### Learner model understands:
- **WHO** → Student / Professional / Job Seeker
- **GOAL** → Learn coding / Placement / Company / Role
- **TARGET** → company + role
- **CURRENT LEVEL** → inferred, not only self-declared
- **SKILLS** → mastery per concept
- **MISCONCEPTIONS** → what they repeatedly misunderstand
- **PERFORMANCE** → accuracy + attempts + time + hints
- **TRANSFER** → can they use the concept in a new context?
- **RECALL** → is knowledge retained?
- **RECENCY** → what have they practiced recently?
- **PREFERENCES** → language, session length, learning style signals
- **READINESS** → current placement capability

### Principles:
1. **Curriculum is shared; the learner's path through it is personal.**
2. **Never teach a learner something they have already demonstrated mastery of merely because it exists earlier in the curriculum.**
3. **Never skip a prerequisite merely because the learner selected an advanced target.**
4. **When a learner fails, personalize the repair to the failure type, not merely the topic.**
5. **When a learner succeeds repeatedly, reduce scaffolding and increase novelty rather than repeating easier content.**
6. **Evidence-driven, not profile-driven.** If student says “I'm intermediate” but fails variables/loops/arrays, behave as beginner at those concepts.

### Final personalization principle:
The product should know:
- WHO I AM
- WHERE I WANT TO GO
- WHAT I CAN DO
- WHAT I CANNOT DO
- WHY I AM STRUGGLING
- WHAT I SHOULD LEARN NEXT
- WHICH COMPANY/ROLE REQUIRES IT
- WHETHER I CAN PROVE IT
- WHAT I NEED TO REPAIR
- HOW READY I AM

And it should continuously update those answers from evidence.

---

## 5. ADAPTIVE LOOP

```
CURRENT LEARNER STATE
        ↓
TARGET REQUIREMENTS
        ↓
AVAILABLE CURRICULUM
        ↓
PREREQUISITES
        ↓
SELECT NEXT BEST EXPERIENCE
        ↓
LEARN / PRACTICE
        ↓
EVIDENCE
        ↓
UPDATE LEARNER STATE
        ↓
RESELECT NEXT EXPERIENCE
```

This is the heart of PlacementPro.

### Next-action priority:
1. REQUIRED PREREQUISITE
2. FAILED CONCEPT / REPAIR
3. OVERDUE RECALL / SRS
4. TARGET-COMPANY REQUIRED SKILL
5. LOWEST IMPORTANT MASTERY
6. TRANSFER / INTERLEAVING
7. SESSION-TIME FIT

### Final principle:
Personalization must determine what this student sees, learns, practices, reviews, and gets assessed on next — not just the homepage.

---

## 6. SERVICE-BASED CURRICULUM — SIX WORLDS

### WORLD 1 — THINK & SOLVE
Foundation. Teaches students to think before they calculate.
- Numerical thinking: number sense, place value, fractions, decimals, approximation
- Problem translation: identify given/asked, choose formula, estimate, eliminate
- Logical thinking: sequence, pattern, classification, analogy, deduction, constraint thinking

### WORLD 2 — QUANTITATIVE APTITUDE
- Percentages, profit/loss, discounts, simple/compound interest
- Ratio/proportion, partnership, mixtures/alligation, averages, ages
- Time/work, pipes/cisterns, time/speed/distance, trains, boats/streams
- Permutations, combinations, probability, number systems, divisibility, HCF/LCM
- Data interpretation: tables, bar/pie/line charts, caselets, mixed DI
- Advanced screening: multi-step arithmetic, data-heavy questions, optimization, timed mixed

### WORLD 3 — REASONING
- Directions, blood relations, coding-decoding, number/letter series, odd one out, analogy, ranking
- Syllogisms, statements/conclusions, assumptions, cause/effect, data sufficiency, logical deductions
- Linear/circular seating, floor arrangement, scheduling, distribution, constraint puzzles
- Complex deduction, visual reasoning, critical reasoning, mixed timed reasoning

Teaching pattern: scenario → visual model → manipulate constraints → predict → solve → explain why → timed problem

### WORLD 4 — VERBAL & COMMUNICATION
- Sentence structure, parts of speech, subject-verb agreement, articles, prepositions, tenses, modifiers
- Context vocabulary, synonyms, antonyms, word usage, confusing words, phrasal verbs, root-word intuition
- Main idea, supporting detail, inference, tone, author intent, fact vs inference, long-form comprehension
- Sentence correction, fill in blanks, para jumbles, error spotting, cloze tests, timed verbal sets
- Professional email, workplace message, asking for clarification, reporting problems, explaining delay, interview communication

### WORLD 5 — CODING & TECHNICAL FOUNDATION
- Programming thinking: program, I/O, variables, types, expressions, conditions, loops, functions, arrays/lists, strings, debugging, tracing
- Problem solving: read problem, examples, constraints, brute force, complexity, edge cases, frequency counting, prefix sum, two pointers, sliding window, binary search, sorting+scan, hashing, stack patterns
- DSA foundations: arrays, strings, linked lists, stack, queue, hash map, set, trees, heaps, graphs, recursion, BFS/DFS

Progression: Programming Thinking → Basic Problem Solving → Basic DSA → Patterns → Intermediate DSA → Advanced

### WORLD 6 — TECHNICAL SCREENING & INTERVIEW
- SQL: SELECT, WHERE, ORDER BY, DISTINCT, aggregation, GROUP BY, HAVING, JOIN, LEFT JOIN, subqueries, CTE, CASE, window functions
- CS fundamentals: OOP, DBMS, OS, Networks, HTTP, APIs, Git, software engineering basics
- Technical interview: explain code, complexity, edge cases, debugging, follow-up modification, project explanation, technical communication
- Interview readiness: introduce yourself, project deep dive, behavioral, STAR, conflict, failure, leadership, why this company/role

---

## 7. COMPANY / ROLE PERSONALIZATION

Company is a lens over the shared curriculum, not a separate curriculum.

### Company blueprint determines:
- Required capabilities
- Priority/weighting
- Assessment mix
- Role relevance
- Version/effective date
- Provenance

### Example:
Target: Company X — Software role
Required: Quant High, Reasoning High, Verbal Medium, Coding High, SQL Low, Interview High

Student gaps:
- Reasoning: Blood Relations, Syllogism, Seating Arrangement
- Coding: Loops, Arrays, Two Pointers

System routes to: **Blood Relations → guided repair → placement application**

It does NOT create `company_x_blood_relations_lesson`.

It reuses: **canonical Blood Relations lesson** with company relevance metadata.

### Rules:
- Do not duplicate content per company
- Company information must be versioned and evidence-backed
- Do not claim “most asked” or “frequently asked” unless supported by current verified data/provenance
- Exact assessments vary by role/company/version → company routing must remain versioned

---

## 8. LEARNING EXPERIENCE

### Canonical grammar (not rigid screen count):

```
HOOK
→ SEE
→ UNDERSTAND
→ INTERACT
→ PREDICT
→ CHANGE
→ BUILD
→ MANDATORY QUIZ
→ EXPLAIN IF WRONG
→ RETRY
→ PRACTICE
→ BREAK
→ FIX
→ RECALL
→ TRANSFER
→ PROVE
```

A simple concept can use fewer stages. A complex concept can use more.

### Adaptive teaching style:
- **Beginner**: maximum intuition, visual guidance, scaffolding
- **Developing**: less explanation, more prediction/modification/build
- **Strong**: minimal explanation, novel problems, transfer, timed proof
- **Repeated success**: reduce scaffolding
- **Repeated failure**: switch to misconception-specific repair

### Captain Byte:
- Deterministic authored mentor
- Introduces, explains, asks Socratic questions, gives hints, explains incorrect answers, summarizes
- **No LLM dependency for core curriculum**
- No expensive AI call per beginner interaction

### Mandatory quiz:
- Every meaningful concept has a knowledge check
- PASS → continue
- FAIL → explain misconception → show example/visual → give similar question → retry → only then continue
- No shame screen. No “you failed.” Instead: “Let’s look at this another way.”

---

## 9. CODING LANGUAGES

Student-facing languages:
- C
- C++
- Java
- Python
- HTML
- CSS

Each language can have structured modules and levels.

**Do not force identical linear paths for every learner.** Use diagnostics and mastery to skip already-proven material.

Language mastery updates the shared learner/skill state.

Example: Student masters loops in C++ → later company preparation requires loops → route directly to application/placement-level practice. Do not teach loops from zero again.

---

## 10. DSA VISUAL LAB

Fourth door. Visual exploration environment, not gamified curriculum.

Supported topics:
- arrays, pointers, linked lists, stacks, queues, sorting, binary search, recursion, trees, graphs, BFS, DFS, two pointers, sliding window

Controls: play, pause, step, restart, manipulate, observe

No separate progression engine. No separate mastery engine. No separate XP system.

Evidence from meaningful use enters the shared learner state.

---

## 11. MOCK OA

Composed from selected company/role blueprint.

Possible areas:
- numerical, reasoning, verbal, coding, SQL, CS, communication

Exact composition comes from current company blueprint, not hardcoded universal test.

### Flow:
```
TARGET
 ↓
COMPANY BLUEPRINT
 ↓
PERSONALIZED MOCK
 ↓
RESULT
 ↓
GAP DIAGNOSIS
 ↓
REPAIR MISSIONS
 ↓
RETEST
```

Diagnosis identifies weak capabilities and misconception/failure classes.

---

## 12. AI INTERVIEW

Downstream evidence. Assesses:
- Communication
- Project explanation
- Technical reasoning
- Coding explanation
- Follow-up adaptation
- Behavioral answers

### Flow:
```
AI INTERVIEW
 ↓
TECHNICAL
 ↓
PROJECT
 ↓
BEHAVIORAL
 ↓
FOLLOW-UP
 ↓
FEEDBACK
 ↓
WEAKNESS
 ↓
LEARNING / PRACTICE
```

Weaknesses feed back into the same curriculum.

AI remains for: AI Interview, AI Debugging, Resume Analyzer, advanced assistance.

---

## 13. RESUME ANALYZER

Separate from learning graph but connected to career layer:
```
Resume
 ↓
ATS
 ↓
Role fit
 ↓
Company fit
 ↓
Improvement
```
Career utility, not a separate curriculum system.

---

## 14. GAMIFICATION — SIMPLIFIED

### ONE currency: 💎 Diamonds

```
Meaningful learning
        ↓
Evidence
        ↓
Mastery / completion
        ↓
💎 Diamonds
```

### Levels: progression/identity
### Streak: habit indicator

### Remove student-facing:
- XP
- Coins
- Stars
- Combo economy
- Power-up shop
- Double-XP items
- Boss currency
- Stamina
- Energy

### Immutable ledger:
Every diamond award appends one immutable `gamification_events` row.

### Only writer:
`record_practice()` is the only writer of diamonds/streak/level/badges.

---

## 15. QUESTIONS ARE NOT THE CURRICULUM

Questions are the **practice/evidence layer**.

Curriculum teaches: why, how, recognition, intuition, application
Questions prove: can you actually do it?

```
LESSON
 ↓
INTERACTION
 ↓
QUIZ
 ↓
QUESTION
 ↓
TRANSFER
 ↓
PROOF
```

Existing questions provide: practice, application, assessment, transfer, proof.

### Content trust rules (binding):
- Question content lives in versioned files under `backend/app/data/`
- Loaded into memory at startup by `question_store`
- MongoDB holds **student state only**
- Trust pipeline: `UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED`
- Serving gate: only `verified`/`reviewed` content served to students
- No LLM in question bank

---

## 16. CANONICAL PIPELINE

```
Onboarding
   ↓
Goal
   ↓
Diagnostic
   ↓
Learner State
   ↓
Company/Role Target
   ↓
Curriculum Graph
   ↓
Next Mission
   ↓
Interactive Learning
   ↓
Mandatory Quiz
   ↓
Practice
   ↓
Proof
   ↓
Evidence
   ↓
Mastery
   ↓
SRS / Repair
   ↓
Journey
   ↓
Mock OA
   ↓
Diagnosis
   ↓
Repair
   ↓
Retest
   ↓
AI Interview
   ↓
Readiness
```

**ONE of each:**
- Learner state
- Curriculum graph
- Lesson experience
- Activity sink
- Mastery source
- SRS
- Repair
- Gamification currency
- Company opportunity graph

---

## 17. DATABASE DISCIPLINE

One authoritative source for each type of student state.

**Required collections:**
- `learner_state`
- `learning_events`
- `mastery_state`
- `srs_state`
- `gamification`
- `company_target`
- `assessment_session`
- `interview_session`

Every other collection must prove why it needs to exist.

Question content lives in versioned files. MongoDB holds **student state only**.

---

## 18. AI RELIABILITY

All AI calls flow through `ai_core.chat_completion()`:
- Circuit breaker gating
- 3 retries with exponential backoff
- 6 fallback models
- 1-hour cache
- Request metrics recording

Domain modules never call OpenRouter directly.

AI remains for: interviews, debugging, advanced assistance, career tools.

---

## 19. CODE EXECUTION

Fallback chain:
1. Local Python oracle batch
2. GCP compiler service
3. Remote fallbacks: Judge0 / Wandbox / Glot.io
4. Local sandbox subprocess
5. Piston API

Circuit breaker protects external calls.

---

## 20. AUTHURITY

- JWT + httpOnly cookies
- Refresh token rotation
- Admin derived only from `ADMIN_EMAILS`
- Rate limiting + account lockout
- Password strength enforcement
- User caching with 5-min TTL; privileges never cached

---

## 21. PROCESS RULES

### Rule 1 — One architect
One agent owns architecture decisions. Other agents cannot invent a new canonical system.

### Rule 2 — One writer
Never run multiple coding agents modifying the same architecture simultaneously.

Use: Architect → Plan → Implementer → Verifier

### Rule 3 — Every new system needs a replacement statement
Before creating a new module, answer: **Which existing system does this replace?**

If the answer is “None,” it does not get created.

### Rule 4 — Classify before deleting
Do not delete working content blindly. Classify each system:
- **KEEP** — canonical
- **KEEP** — supporting
- **MERGE** — duplicate
- **MIGRATE** — useful content
- **REDIRECT** — legacy UI
- **ARCHIVE** — experimental
- **DELETE** — genuinely dead

---

## 22. MANDATORY VERIFICATION

Before declaring any work complete:
- Verify the actual student flow, not compilation
- Verify data persists at every arrow
- Verify content is correct, not merely present
- Verify the feature serves capability gained per student

**“Verified” means a pasted response body, a screenshot, or a test asserting real output. Compile-passes and route-imports are not evidence.**

---

## 23. QUALITY GATE

For every lesson ask:
- Can a beginner SEE the idea?
- Can they INTERACT with it?
- Can they PREDICT it?
- Can they CHANGE it?
- Can they BUILD something?
- Do they GET A QUIZ?
- Can they UNDERSTAND a mistake?
- Can they RETRY?
- Can they SOLVE a real placement problem?
- Can they TRANSFER the concept?
- Can they PROVE it independently?

If a screen is just text + Next, it fails the standard.
If a screen is video + paragraph + Next, it fails the standard.
If a lesson has visual + interaction + prediction + feedback + proof, it is moving toward the target.

---

## 24. IMPLEMENTATION ORDER

1. Architecture inventory + dependency map
2. Choose ONE canonical learning renderer: MissionShell + MissionExperience
3. Consolidate interaction vocabulary and parameterize existing widgets
4. Build six reference-quality concepts: Trace Variables, Percentages, Blood Relations, Two Pointers, Email Format Validation, Sliding Window
5. Build the service-based curriculum worlds
6. Map the existing verified question bank into the curriculum
7. Connect company blueprints to skill priorities
8. Connect Mock OA → Diagnosis → Repair → Retest
9. Connect AI Interview → Evidence → Curriculum repair
10. Run end-to-end tests

**Do not increase feature count until the canonical learning loop works.**

---

*This document supersedes all prior architecture docs, strategy docs, and feature inventories. When in doubt, this document is the source of truth.*
