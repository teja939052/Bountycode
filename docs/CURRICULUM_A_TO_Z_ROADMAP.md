# BountyCode — Complete A–Z Curriculum & Learning-System Roadmap

**Status:** Long-term product vision (post-v1)  
**Relationship to locked vision:** This document extends, does not replace, `docs/BOUNTYCODE_VISION_LOCK.md`.  
The current launch product remains the focused service-company placement platform (6 worlds, interactive lesson template, trust-gated bank, company blueprints for TCS/Infosys/etc.).  
Everything below is the target end-state once the locked v1 loops are proven and stable.

**Goal**  
Turn BountyCode into a complete placement-preparation and career-learning system.  
A learner should be able to start with zero knowledge, learn every required concept in the right order, practise it, identify weaknesses, repair them, prepare for specific companies, and prove readiness through assessments.

A topic appearing in the curriculum is **not** the same as a topic being fully taught. Every topic needs structured lessons, examples, exercises, assessments, feedback, and mastery criteria.

---

## 1. What already has a foundation (inventory from current repo)

| Area | Existing foundation |
|------|---------------------|
| Coding practice | 474+ coding problems, compiler integration, 11 languages |
| Aptitude | 67+ questions |
| System design | 20 problems |
| Behavioral | 50+ questions |
| AI interviews | Company personas, follow-up questions, voice analysis |
| Gamification | XP, tower, wallet, marketplace, scrims, showcase, assignments |
| Learning | Python, C, C++, Java lesson profiles + interactive coding academy |
| Core subjects | SQL, DBMS, OS, networking, aptitude curriculum groundwork |
| Personalization | Adaptive quizzes, evidence tracking, skill graph, prerequisite DAG |
| Company preparation | Company-aware study paths and question filtering |
| Worlds | 12 worlds registered (see `backend/app/content/world_registry.py`); 13 DSA worlds mentioned in prior context need rigorous lesson-stage gates and mastery rules |

**Important:** This is an inventory from project context and file structure, **not** a fresh audit of every current file. A lesson profile or question count does not prove the content is complete or production-ready.

---

## 2. The complete curriculum: 10 pillars

### Pillar 1 — Programming foundations (Highest priority)

Beginner → intermediate. A student must start without knowing how to code.

- **Module 1:** Computer & programming fundamentals  
  (hardware/software, CPU/RAM, OS, languages, compilers vs interpreters, syntax vs logic errors, debugging)
- **Module 2:** Programming logic  
  (algorithms, pseudocode, flowcharts, variables, data types, operators, conditionals, loops, functions, recursion, clean code)
- **Module 3:** Data structures inside languages  
  (strings, arrays, lists, tuples, sets, maps, stacks, queues, iterators, generators, mutability, memory, exceptions, files, modules)
- **Module 4:** Object-oriented programming  
  (classes, constructors, encapsulation, inheritance, polymorphism, interfaces, SOLID, design patterns intro)

**Language tracks** (same core concepts, language-specific differences — do **not** simply duplicate lessons):
- Python, C, C++, Java  
- JavaScript/TypeScript as practical web track

### Pillar 2 — Data structures and algorithms (Highest priority)

One of BountyCode’s strongest learning experiences.

Modules: Complexity analysis → Arrays & hashing → Core patterns (two pointers, sliding window, prefix, binary search, monotonic stack/queue, greedy, bit) → Linked lists → Stacks & queues → Recursion & backtracking → Trees → Graphs → Dynamic programming → Advanced algorithms (segment/Fenwick, string algorithms, number theory).

**Required outcome:** Learner can recognize a pattern, explain why it applies, derive an approach, analyse complexity, implement, debug, and solve unseen variations.

### Pillar 3 — SQL and database mastery

Beginner → intermediate → advanced SQL + database theory (ER, keys, normalization, ACID, indexing, concurrency, sharding).

Add coding exercises, output prediction, debugging, schema design, timed assessments.

### Pillar 4 — DBMS, OS, Computer Networks, Architecture

Essential for campus placements. Full coverage of the standard GATE/placement syllabus in each subject.

### Pillar 5 — Quantitative aptitude

Full range of service + product company tests. Arithmetic → advanced quant → data interpretation.  
Teach underlying mathematical reasoning first, then shortcuts.

### Pillar 6 — Logical reasoning and verbal ability

Series, coding-decoding, blood relations, seating, puzzles, syllogisms, critical reasoning, grammar, RC, para-jumbles, business communication, interview communication.

### Pillar 7 — Web development and practical engineering

HTML/CSS → JavaScript/TypeScript → React → Backend (REST, auth, JWT, middleware) → Databases & deployment (Mongo, Postgres, Redis, Docker, CI/CD, cloud) → Testing & engineering quality.

### Pillar 8 — System design and software engineering

LLD (OOP, UML, SOLID, design patterns, classic problems) + HLD (capacity, API, caching, scaling, queues, microservices, consistency) + practical exercises (URL shortener, chat, feed, e-commerce, etc.).

### Pillar 9 — Company-specific placement curriculum

Four stages per company: Foundation → Company-style OA → Technical interviews → HR/behavioral.

**Indian service:** TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini, HCL, Tech Mahindra, LTIMindtree, Mphasis.  
**Product:** Google, Amazon, Microsoft, Meta, Apple, Adobe, Oracle, Salesforce, Uber, Atlassian.

Every pathway needs: company overview, timed assessment, technical syllabus, question bank, coding sets, interview questions, projects, HR, full mock, readiness breakdown.  
**Never present guessed hiring patterns as official syllabi.** Show source, last-verified date, confidence level.

### Pillar 10 — Resume, interview and career readiness

Resume/ATS, job applications, LinkedIn/portfolio/GitHub, STAR behavioral, mock interviews, role expectations, workplace skills.

---

## 3. Lesson standard (non-negotiable)

Every concept needs a complete learning experience — not a short paragraph + 3 MCQs.

**BountyCode lesson blueprint:**
1. Learning objective  
2. Prerequisite check  
3. Intuition first (real-world analogy)  
4. Concept explanation (theory, diagrams, edge cases)  
5. Visual demonstration  
6. Code demonstration (beginner → intermediate → optimized)  
7. Pattern recognition  
8. Common mistakes  
9. Guided practice  
10. Assessment  
11. Mastery check (unseen questions)  
12. Spaced repetition  
13. Real-world / interview connection

Minimum content targets per topic: multiple explanation sections, ≥3 progressive examples, visualization where useful, ≥5 exercises, conceptual + applied + debugging questions, misconceptions, interview questions, one real-world use case, clear mastery criteria.

---

## 4. Personalized learning engine

**Cycle:** Learner profile → Diagnostic → Personalized curriculum → Teach → Practice/Assess → Diagnose mistakes → Repair & reassess → Readiness & progression.

Required features: skill graph + prerequisites, adaptive sequencing & difficulty, AI tutor (Teach / Socratic / Hint / Debug / Interview / Revision / Challenge / Explain-my-mistake modes), misconception engine, repair engine, quiz generator (within curriculum boundaries), spaced repetition, mastery engine (independent evidence, not XP or completion %), readiness engine, learning analytics, interview simulation.

AI must never invent mastery, claim correctness without verification, or fabricate company requirements.

---

## 5. Assessment system

Beyond MCQs: conceptual quizzes, coding tests (correctness + edge cases + complexity), debugging, application tests, timed assessments, oral interviews.

Mastery rules must use distinct question evidence, server-graded correctness, difficulty/skill relevance, independent retests, recency, consistent performance, and confidence based on sample size.  
Three questions at 70% is a useful gate, not certification for advanced DSA or interview readiness.

---

## 6. Gamification that improves learning

Existing mechanics (XP, tower, worlds, etc.) must reinforce the curriculum.  
Rewards must never bypass prerequisites, create fake mastery, or incentivize spam.

---

## 7. Projects & portfolio curriculum

Beginner → Intermediate → Full-stack → Advanced → Engineering → Deployment.  
Every project needs requirements, architecture, prerequisites, milestones, starter tasks, review checklist, tests, deployment instructions, README, evaluation rubric, portfolio-ready output, and project-based interview questions.

---

## 8. Dashboard & learner experience

The dashboard answers six questions only:  
What am I trying to achieve? Where am I? What should I learn today? What am I weak at? What have I mastered? Am I ready for my target company?

Navigation: Home / Learn / Practice / Assess / Companies / Interviews / Projects / Progress / Profile.  
Game world is a navigation layer, not a replacement for a clear curriculum.

---

## 9. Content infrastructure

Canonical skill taxonomy, prerequisite dependency graph, lesson/question schemas with versioning, skill mapping, difficulty classification, misconception taxonomy, quality validators, authoring dashboard, coverage dashboard, duplicate detection, company syllabus mapping, source & review dates, learning-event audit trail, assessment version tracking.

Example lesson metadata shape is already sketched in the original blueprint; implement it as the single source of truth.

---

## 10. Recommended execution order (do not build all pillars at once)

| Phase | Focus |
|-------|--------|
| 0 | Repository & curriculum audit — map every item to canonical skill IDs, flag incomplete/duplicated/placeholder content, produce honest coverage report |
| 1 | Learning engine completion (diagnostic, prerequisites, grading, retesting, mastery, SRS, readiness) |
| 2 | Programming foundations + full DSA |
| 3 | Placement core subjects (SQL/DBMS/OS/CN/Architecture) |
| 4 | Aptitude + verbal |
| 5 | Company preparation (individual syllabi + mocks) |
| 6 | Engineering + system design + projects |
| 7 | Career preparation (resume, interviews, communication) |
| 8 | Quality, analytics, launch readiness of the expanded product |

**Priorities**  
- **P0:** Finish the learner journey from diagnostic → verified mastery; complete foundational programming + DSA; complete aptitude + SQL + DBMS + OS + networking.  
- **P1:** Company-specific paths + assessments; projects + system design + interview prep.  
- **P2:** Advanced AI, social learning, extra game mechanics.

---

## 11. Definition of done (acceptance criteria)

- Curriculum: all planned concepts mapped; coverage gaps visible.  
- Lessons: no placeholder / title-only lessons in released tracks.  
- Questions: verified answer keys, explanations, skill mappings.  
- Prerequisites: learner cannot skip required foundations.  
- Diagnostics, adaptation, repair, mastery, revision, company paths, coding, interviews, gamification, analytics, reliability — all meet the standards listed in the original blueprint.

---

## 12. Product vision statement

**BountyCode**  
*Learn. Practise. Prove. Get hired.*

One connected platform where a beginner develops into a job-ready engineer through structured learning, personalized assessments, and measurable skills.

A learner can: start from absolute zero → choose target role & companies → receive a complete personalized curriculum → learn every concept through deep lessons → practise with interactive examples and coding → identify and repair misconceptions → revise at the right time → build real projects → pass company-specific mock assessments → demonstrate interview and job readiness.

**Do not claim A–Z coverage** just because a large question bank or many lesson titles exist. Measure actual content coverage, quality, and learner outcomes.

The previous work on DSA worlds, programming tracks, prerequisite graph, and adaptive assessment must become **one connected system** — not separate products competing for attention.

---

## Next concrete action

Produce a repository-grounded implementation specification:

1. Inspect the current branch.  
2. Map every curriculum item in this document to existing files and endpoints.  
3. Mark each item `complete` / `partial` / `missing` / `needs verification`.  
4. Generate the exact ordered implementation backlog.

That backlog is the real A–Z execution plan. It avoids rebuilding features that already exist.
