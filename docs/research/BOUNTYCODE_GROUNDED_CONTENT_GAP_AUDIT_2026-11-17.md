# Bountycode grounded content gap audit and measurable targets

**Audit date:** 2026-11-17  
**Repository/ref inspected:** `teja939052/Bountycode` / `main`  
**Purpose:** turn repository evidence into a prioritized content plan. This is an audit document only; no production code or question data was modified.

## Executive finding

Bountycode does not primarily have a raw-volume problem. It has a **trust, curriculum integrity, serving-path consistency and topic-depth problem**.

The repository already contains large banks and many curriculum files. However, repository presence, automated execution, human review and student-facing serving are different states. Counts from different audit snapshots must not be summed or presented as one current live count.

The strongest immediate evidence:

- `docs/learning/LESSON_INVENTORY_summary.json` reports 1,112 lesson rows, 1,112 unique IDs, 60 silently overwritten IDs, 1,023 template-filler lessons and 1,013 broken prerequisite links. These counts indicate a serious lesson-catalog integrity issue. They are the report's recorded inventory, not a fresh runtime execution.
- `backend/app/data/question_content_trust_report.json` records 6,379 records: 2,879 coding, 50 aptitude, 30 logical, 20 verbal and 3,400 unknown type. Its repair reasons are 3,128 template shells, 2,821 unverified expected outputs and 430 missing test cases. It lists 104 verified IDs. This is a report snapshot and must be reconciled with the live loader.
- `backend/app/data/expanded_bank_report.json` records 7,561 inputs, 1,550 automated_checked and 6,011 quarantined. It includes 5,483 coding, 1,558 aptitude, 60 logical, 49 verbal, 43 CS fundamentals, 106 interview, 12 system design, 133 debugging, 108 SQL and 9 CS records. The report explicitly labels the 1,550 as automated_checked, not independently human verified.
- `backend/app/data/bank_autocheck_report.json` records 6,161 checked, 645 automated_checked and 5,516 quarantined. It says automated_checked only and not loaded by student serving. Its scope differs from the expanded-bank report.
- `backend/app/data/parametric_bank_report.json` records 6,600 parameterized practice variants, with trust state automated_checked and an explicit note that they are not served by default.
- `backend/app/data/COMPANY_CONTENT_STATUS.md` records 2,977 generated company items and 2,689 serveable at the time of that status note. It also says the TCS MCQ bank has 2,472 auto-checked items. This is not proof that those records pass the current runtime trust gate.

## 1. Actual serving architecture and trust-gate findings

### Runtime ownership

The current `backend/app/services/question_governance.py` defines two owners:

1. `question_store`: coding and placement bank.
2. `quiz_service`: curated interactive quizzes and learning objects.

It explicitly says not to introduce a third question system.

The governance registry lists the intended trusted banks and separate unverified/curated artifacts. The runtime implementation in `backend/app/services/question_store.py` must be treated as the final authority for what is loaded and served.

### Important implementation contradiction

In `question_store.py`:

- `AUTO_CHECKED_BANKS` includes `llm_draft_checked.json`, `expanded_question_bank.json`, and `verified_question_bank.json`.
- `load_all()` loads the verified extra banks, auto-checked banks and unverified banks for verification, then deduplicates and applies quarantine.
- `_is_servable()` accepts only trust statuses `verified` and `reviewed`, and also requires `_is_executable()`.
- Therefore a record with `trust_status="automated_checked"` is loaded into the in-memory candidate pool but is **not student-servable** under the current gate.
- Some comments near the auto-checked loader describe those records as belonging to the verified serving pool, which conflicts with the actual `_is_servable()` implementation.
- The method `only_verified()` also calls `_is_servable()`; its docstring says automated_checked may be included, but the implementation excludes it.

**P0 action:** add tests and a single explicit policy for the status transition. Do not loosen the gate just to increase visible question count. Automated execution is not independent correctness review.

### Non-coding schema risk

The current `_is_executable()` rules require:

- coding / SQL / debugging: test cases; SQL additionally needs `sql_schema`.
- aptitude / logical / verbal / HR / CS MCQ: valid options and correct answer/index.
- interview / system design / GD: rubric, evaluation criteria or worked solution.

Spot checks found examples requiring review:

- The first `infosys_infytq_verified.json` coding record includes an empty-array case with expected `null`, while its solution calls `max(arr)`, which raises on an empty array.
- The first Wipro, Cognizant and Capgemini/Accenture coding examples use scalar test inputs despite a solution signature expecting an array and target.
- The first `india_placement_depth.json` record has a one-element options list, not a usable four-option MCQ.
- The first `interview_practice_bank.json` record has a prose scoring description but no explicit rubric field, evaluation criteria or worked_solution, so it may fail the current executable/servable gate.
- The SQL practice bank's first record has no `sql_schema`; the runtime explicitly requires schema metadata for SQL execution.

These are **record-level spot checks**, not claims that every record in each file is defective. They show why file names and `trust_status` labels cannot substitute for running the actual production validator.

## 2. Actual content and curriculum coverage

### DSA canonical skill inventory

The current `skill_taxonomy.py` defines 23 DSA skills:

Arrays, Hashing, Two Pointers, Sliding Window, Stack/Monotonic Stack, Binary Search, Linked List, Strings, Trees, BST, Tries, Heap/Priority Queue, Graphs, BFS, DFS, Dynamic Programming, Greedy, Backtracking, Math & Geometry, Bit Manipulation, Sorting, Searching and Recursion.

The curated placement question file `backend/app/content/questions/curated/placement_questions.json` contains 61 questions, with the recorded topic distribution:

| Topic | Count |
|---|---:|
| Arrays & Hashing | 37 |
| Binary Search | 10 |
| Sorting | 6 |
| Strings | 5 |
| Two Pointers | 3 |
| **Total** | **61** |

This file is owned by `quiz_service`, not the main coding question store. It is not the entire DSA bank.

The November curriculum audit explicitly identifies remaining DSA lesson gaps: two pointers, sliding window, greedy, backtracking, heaps, advanced trees, shortest paths, MST and advanced DP. It also notes missing depth in SQL/DBMS concurrency and recovery, OS synchronization and memory, networking subnetting/routing/TLS, and aptitude/verbal coverage.

### Core subject gaps already documented in repo

- **DSA:** dedicated depth for two pointers, sliding window, greedy, backtracking, heaps, advanced trees, shortest paths, MST and advanced DP.
- **DBMS/SQL:** deeper query practice, CTEs/subqueries, query plans/indexes, concurrency, recovery and transaction isolation; SQL items must carry executable schema fixtures.
- **Operating systems:** CPU scheduling calculations, synchronization, memory management, file systems and disk scheduling.
- **Computer networks:** subnetting, IPv6, routing, switching, DHCP, NAT, proxies, firewalls and TLS.
- **Computer architecture:** cache mapping, instruction formats, virtualization and pipeline performance calculations.
- **Aptitude/reasoning/verbal:** complete subtopic coverage, worked methods, timed practice and difficulty progression.
- **Debugging/system design/behavioral:** content exists in separate banks and lesson tracks, but their rubric/schema and learner-facing integration must be verified.

### Lesson catalog integrity

The recorded lesson inventory is a more urgent warning than raw lesson count:

| Metric | Recorded count |
|---|---:|
| Lesson rows | 1,112 |
| Unique IDs | 1,112 |
| Template-filler lessons | 1,023 |
| Broken prerequisite links | 1,013 |
| Silently overwritten IDs | 60 |

Do not claim 1,112 complete lessons. First determine which catalog the summary represents, reproduce the report from current files, inspect the 1,023 template records and resolve the 60 overwritten-ID cases. A separate November curriculum audit reports 134 lesson objects across 18 registered modules on its inspected branch; this is a different scope/snapshot and must not be conflated with the 1,112-row inventory.

## 3. Company profiles: what is actually supported

The current `company_blueprints.json` contains six profiles: TCS NQT, Accenture, Infosys, Wipro NLTH, Capgemini and IBM.

The blueprint records generally label their provenance `pattern_relevant`; multiple profiles use secondary sources and contain a verification TODO. They should not be advertised as official current company exam patterns until checked against current employer material.

Current public evidence checked on 2026-11-17:

- **TCS:** the official 2026 All India NQT page describes a 190-minute integrated test: 75-minute Foundation (Numerical, Verbal, Reasoning) and 115-minute Advanced (Advanced Quantitative/Reasoning and Advanced Coding). This supports the broad structure in the repository; individual blueprint details still need reconciliation. Source: https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring
- **Amazon SDE:** Amazon's official SDE preparation page lists programming language, data structures, algorithms, coding, object-oriented design, databases, distributed computing, OS, internet topics and general ML/AI. It also provides a sample coding challenge. Source: https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics
- **Amazon SDE II:** the official page describes a role-specific assessment with two technical questions, system-design scenarios and a work-style survey, plus coding, design and Leadership Principles interviews. Do not generalize SDE II timings to graduate hiring. Source: https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep
- **Microsoft:** its official technical interview guide calls out coding, testing, algorithms, data structures, system design/distributed systems, networking, and role-dependent AI/ML and data science. Source: https://careers.microsoft.com/v2/global/en/hiring-tips/technical-interviewing.html
- **Accenture:** its official India recruitment guidance says technical assessments evaluate applied problem solving, logical reasoning and technical knowledge in a coding environment; format and timing are role/process dependent. Source: https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture

No official source was found in this pass to confirm every exact section count in the Infosys, Wipro, Capgemini or IBM blueprints. Those profiles remain pattern-relevant / to-be-verified.

## 4. Proposed content targets

These are **Bountycode product targets**, not claims about the exact number of questions a company asks. They are intentionally modest enough to review thoroughly and large enough to support progression and adaptive assessment.

### Minimum trusted assessment corpus

| Domain | Target unique items | Coverage rule |
|---|---:|---|
| DSA coding | 460 | 23 canonical skills × 20 each: 5 easy, 10 medium, 5 hard |
| Programming foundations | 200 | 25 core concepts × 8 tasks/MCQs; language-neutral concepts plus language-specific code tracing |
| Quantitative aptitude | 300 | 15 subtopics × 20; 5 easy, 10 medium, 5 hard |
| Logical reasoning | 180 | 12 subtopics × 15; include timed and multi-step reasoning |
| Verbal ability | 150 | 10 subtopics × 15; include reading passages, grammar and contextual usage |
| CS fundamentals | 300 | OS, DBMS, Networks, OOP and Architecture × 60 each |
| SQL | 120 | 6 areas × 20, all with schema, seed data and executable expected results |
| Debugging | 80 | 8 bug classes × 10, each with buggy code, corrected behavior and regression tests |
| System design | 60 | 6 dimensions × 10, each with rubric and trade-off evaluation |
| Behavioral/interview | 60 | 6 competency groups × 10, with evidence-based scoring rubrics |
| **Total** | **1,910** | Unique authored/reviewed assessment items, before company mock compositions |

A question reused in multiple company blueprints remains one canonical question with multiple evidence-backed tags. Do not duplicate records to inflate company counts.

### Company assessment targets

First cohort: TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini, IBM, Amazon, Microsoft and Google.

For each company/role profile:

- 1 current evidence dossier with source URLs and last-verified date.
- 1 canonical topic map to the existing skill taxonomy.
- 3 full mock blueprints: foundation/entry, standard and advanced where the hiring track supports those levels.
- Each mock assembled from canonical items, not copied/duplicated bank records.
- Every company-specific claim labelled official, candidate-reported, historical, pattern-relevant or unknown.
- At least 30 role-relevant unique tagged questions before calling the profile content-complete; shared core questions are allowed but counted once globally.

These are minimum product coverage targets, not assertions that every company uses these exact assessments.

### Lesson quality target per canonical skill

For each of the 23 DSA skills and each core CS/aptitude skill:

- 1 complete concept lesson with prerequisites and measurable outcomes.
- 3 worked examples: intuitive, standard and edge-case/optimized.
- 1 visual or dry-run explanation where appropriate.
- 1 quick-revision sheet (patterns, complexity, formulas or shortcuts).
- 1 common-mistakes / misconceptions section.
- 1 practice set with at least 5 questions.
- 1 unseen transfer assessment.
- 1 spaced-repetition card set.
- 1 explicit mapping to company-role requirements where supported.

Lesson acceptance requires correct content and valid prerequisite edges, not merely non-empty text.

## 5. Sourcing plan: use these sources for concepts, not bulk copying

| Area | Primary sources to mine | What to extract/author |
|---|---|---|
| DSA / algorithms | MIT OCW 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ; OpenDSA: https://opendsa.cs.vt.edu/ ; Open Data Structures: https://opendatastructures.org/ | Topic sequence, proof/intuition, complexity, visualizations, original practice tasks |
| Competitive programming patterns | CP-Algorithms: https://cp-algorithms.com/ ; USACO Guide: https://usaco.guide/ | Algorithm explanations, prerequisites, edge cases, advanced variants; check each site's terms before reuse |
| OS | OSTEP: https://pages.cs.wisc.edu/~remzi/OSTEP/ | Processes, scheduling, memory, concurrency, file systems and simulator-based learning |
| DBMS / SQL | PostgreSQL tutorial: https://www.postgresql.org/docs/current/tutorial.html ; Runestone database textbook: https://runestone.academy/ns/books/published/practical_db/front-matter/preface.html | Executable SQL labs, schemas, transactions, indexes, query plans |
| Networks | Loyola computer networks text: https://intronetworks4.cs.luc.edu/ | Protocol diagrams, TCP/IP, routing and network exercises |
| Programming / web | Python docs: https://docs.python.org/3/tutorial/ ; MDN: https://developer.mozilla.org/en-US/docs/Learn_web_development ; React: https://react.dev/learn ; TypeScript: https://www.typescriptlang.org/docs/handbook/intro.html | Language concepts, code examples, practical projects and reference links |
| Aptitude | Khan Academy: https://www.khanacademy.org/math | Foundational explanation, worked examples and original placement-style timed questions |
| Company-specific | Official employer career/interview pages; official sample papers; HackerRank candidate resources | Hiring-stage evidence, assessment format, skill expectations; do not reproduce proprietary items |

Rights rule: link by default. Only ingest, mirror or adapt a resource if the exact license permits the intended use. Free access does not equal redistribution permission. Public candidate reports may inform pattern relevance but must be labelled as reports, not official questions.

## 6. Compiler and coding assessment targets

A separate compiler audit is still required; this report does not claim the current execution engine passed these checks.

Target the first reliable language set: C, C++, Java, Python, JavaScript and SQL sandbox (SQL isolated separately). Add Go, Rust and C# only after demand and execution reliability are demonstrated.

For every supported language, maintain a conformance suite covering:
- compile success and compile failure
- stdin/stdout contract
- multiple test cases
- empty and boundary inputs
- large input and timeouts
- memory/output limits
- runtime exceptions
- process cleanup
- concurrent submissions
- sandbox/network/filesystem restrictions

Acceptance: no user code runs inside the FastAPI application process; every language has reproducible runtime/compiler versions and isolated execution limits. SQL runs against ephemeral isolated databases with fixture schemas.

## 7. Prioritized execution plan

### P0 — Establish one trustworthy truth
1. Reproduce the lesson inventory from current tracked files; resolve 60 overwritten IDs and 1,013 broken prerequisites.
2. Resolve the `automated_checked` versus `verified/reviewed` serving-policy contradiction.
3. Generate a question-level export from the actual runtime loader with ID, source file, type, topic, pattern, difficulty, company tags, trust state, executability, quarantine reason and duplicate canonical ID.
4. Reconcile every existing report snapshot; stamp each report with branch, commit SHA, date, script version and input files.
5. Spot-check and repair malformed company bank examples and SQL/interview schema issues.

### P1 — Fill core content
1. DSA: build to 460 trusted unique questions with balanced skill/difficulty coverage.
2. Aptitude/reasoning/verbal: build to 630 trusted unique questions with subtopic coverage.
3. CS fundamentals: build to 300.
4. SQL: build to 120 schema-backed executable tasks.
5. Debugging/system design/behavioral: build to 200 rubric- or test-backed assessment items.
6. Build the 10-company evidence dossiers and mock compositions.

### P2 — Complete learning depth
1. Repair the 1,023 template-filler lesson candidates; do not count them until accepted.
2. Repair prerequisite edges and ID collisions.
3. Complete each skill's lesson, worked examples, visual, quick sheet, practice and transfer test.
4. Connect all content to canonical skill IDs and existing learning evidence flow.

### P3 — Scale and calibrate
1. Run compiler conformance and concurrency tests.
2. Calibrate difficulty and mastery using observed learner outcomes.
3. Measure unseen transfer and delayed retention, not only question completion.
4. Update company evidence on a scheduled review cycle.

## 8. What this audit did not do

- Did not scrape or copy proprietary question text.
- Did not execute the repository's Python scripts or tests; this was a GitHub source and report inspection.
- Did not freshly run the full question-store loader against production dependencies/database.
- Did not claim every current student-serving count is known.
- Did not modify any question, lesson, runtime route or deployment configuration.

## 9. Immediate next artifact

The next engineering artifact should be a reproducible, read-only inventory command that imports the canonical `question_store` in a controlled test environment and emits a row per record with the actual trust/serving verdict. It should separately inventory quiz_service, lesson catalog and company blueprint data. Then the counts and targets above can be measured against the exact current main commit rather than historical reports.

---
**Bottom line:** The first target is not “add 10,000 questions.” It is to make the current bank and lesson catalog truthful, auditable and measurable. Then fill to the explicit 1,910-item trusted assessment baseline and 10 evidence-backed company profiles.
