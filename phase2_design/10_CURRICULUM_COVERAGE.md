# 10 CURRICULUM COVERAGE — COMPLETE PRODUCT SCOPE

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the complete curriculum coverage for BountyCode across all domains named by the founder and the Vision Lock. This document maps every subject area to:

- Concept hierarchy
- Skill IDs (canonical `domain.subskill`)
- Prerequisites
- Difficulty levels
- Lesson types
- Meaningful interactions
- Assessment methods
- Retrieval / revision requirements
- Transfer evidence
- V1 vs roadmap release boundary

This is a design document. No implementation is authorized.

---

## 2. Scope Boundaries

### 2.1 V1 Launch Scope (October 18, 2026 — Vision Lock)

Per `BOUNTYCODE_VISION_LOCK.md` §10 "Launch Scope", V1 must be **great** in:

| World | Patterns |
|-------|----------|
| World 1 — Quantitative Aptitude | Percentages, Ratios, Profit/Loss, Averages, Time & Work, Time Speed Distance, SI/CI, Number Series |
| World 2 — Logical Reasoning | Blood Relations, Syllogism, Coding-Decoding, Directions, Seating, Series, Data Sufficiency |
| World 3 — Verbal | Grammar, Reading Comprehension, Para Jumble, Sentence Correction, Vocabulary, Email Format |
| World 4 — Pseudocode / Programming Logic (differentiator) | Trace Variables, Predict Output, Loops, Nested Loops, Arrays, Conditions, Functions, Recursion basics, Debugging |
| World 5 — Easy/Med DSA (service-level only) | Arrays, Strings, Hashing, Two Pointers, Sliding Window, Sorting, Binary Search, Stack/Queue basics, Linked List basics, Tree basics |
| World 6 — Company Simulation | TCS NQT, Accenture, Infosys, Wipro, Cognizant (blueprint-driven mocks, not question dump) |

**Launch rule:** 5-10 excellent lessons each, not 132 thin ones. World 6: TCS + Accenture blueprints excellent, others weights only.

### 2.2 Roadmap Scope (Post-Launch)

Everything in the founder's full list that does not fit V1 launch scope goes to post-launch, including:
- Full language tracks (C, C++, Python, Java) beyond the pseudocode world
- Advanced DSA beyond service-level
- Full SQL and database path
- Full CS fundamentals path
- Company tracks beyond TCS + Accenture weights
- AI Interview breadth, GD topics, behavioral depth
- Resume/ATS tools beyond secondary status

---

## 3. Curriculum Coverage Matrix

### 3.1 World 1 — Quantitative Aptitude

| Concept | Skill ID | Prerequisite | Difficulty | Lesson Type | Interaction Template | Assessment | Retrieval/Revision | Transfer Evidence | V1/Roadmap |
|---------|----------|--------------|------------|-------------|---------------------|------------|-------------------|-------------------|------------|
| Percentages | `aptitude.quantitative.percentages` | None | Easy | Interactive lesson | Manipulate | Deterministic numeric | SRS | Increased/decreased by X% variants | V1 |
| Ratios | `aptitude.quantitative.ratios` | Percentages | Easy | Interactive lesson | Manipulate | Deterministic | SRS | Recipe scaling variants | V1 |
| Profit/Loss | `aptitude.quantitative.profit_loss` | Percentages | Easy | Interactive lesson | Fill | Exact answer | SRS | Markup/markdown variants | V1 |
| Averages | `aptitude.quantitative.averages` | Percentages | Easy | Interactive lesson | Manipulate | Deterministic | SRS | Weighted average variants | V1 |
| Time & Work | `aptitude.quantitative.time_work` | Ratios | Medium | Interactive lesson | Manipulate | Deterministic | SRS | Pipe/cistern variants | V1 |
| Time Speed Distance | `aptitude.quantitative.tsd` | Averages | Medium | Interactive lesson | Manipulate | Deterministic | SRS | Upstream/downstream variants | V1 |
| Simple/Compound Interest | `aptitude.quantitative.si_ci` | Percentages | Medium | Interactive lesson | Manipulate | Deterministic | SRS | Varying periods variants | V1 |
| Number Series | `aptitude.logical.number_series` | None | Easy | Interactive lesson | Arrange | Pattern match | SRS | Different series family | V1 |

### 3.2 World 2 — Logical Reasoning

| Concept | Skill ID | Prerequisite | Difficulty | Lesson Type | Interaction Template | Assessment | Retrieval/Revision | Transfer Evidence | V1/Roadmap |
|---------|----------|--------------|------------|-------------|---------------------|------------|-------------------|-------------------|------------|
| Blood Relations | `aptitude.logical.blood_relations` | None | Easy | Interactive lesson | Arrange | Family tree build | SRS | Extended family variants | V1 |
| Syllogism | `aptitude.logical.syllogism` | None | Medium | Interactive lesson | Arrange | Venn diagram match | SRS | New premise sets | V1 |
| Coding-Decoding | `aptitude.logical.coding_decoding` | None | Medium | Interactive lesson | Fill | Decode exact output | SRS | Different cipher | V1 |
| Directions | `aptitude.logical.directions` | None | Easy | Interactive lesson | Manipulate | Coordinate match | SRS | Multi-step path variants | V1 |
| Seating Arrangement | `aptitude.logical.seating` | None | Hard | Interactive lesson | Arrange | Constraint check | SRS | Circular vs linear | V1 |
| Series | `aptitude.logical.series` | None | Medium | Interactive lesson | Predict | Next element | SRS | Alternate pattern | V1 |
| Data Sufficiency | `aptitude.logical.data_sufficiency` | None | Hard | Interactive lesson | Select | Sufficient/Not sufficient | SFS | New statement pairs | V1 |

### 3.3 World 3 — Verbal

| Concept | Skill ID | Prerequisite | Difficulty | Lesson Type | Interaction Template | Assessment | Retrieval/Revision | Transfer Evidence | V1/Roadmap |
|---------|----------|--------------|------------|-------------|---------------------|------------|-------------------|-------------------|------------|
| Grammar | `aptitude.verbal.grammar` | None | Easy | Interactive lesson | Fill | Exact match | SRS | New sentence | V1 |
| Reading Comprehension | `aptitude.verbal.reading` | None | Medium | Interactive lesson | Select | Answer key | SRS | New passage | V1 |
| Para Jumble | `aptitude.verbal.para_jumble` | None | Medium | Interactive lesson | Arrange | Order match | SRS | New paragraph set | V1 |
| Sentence Correction | `aptitude.verbal.sentence_correction` | Grammar | Medium | Interactive lesson | Select | Corrected sentence | SRS | New error types | V1 |
| Vocabulary | `aptitude.verbal.vocabulary` | None | Easy | Interactive lesson | Select | Synonym match | SRS | New word sets | V1 |
| Email Format | `aptitude.verbal.email_format` | None | Easy | Interactive lesson | Fill | Structure match | SRS | Different email types | V1 |

### 3.4 World 4 — Pseudocode / Programming Logic (Differentiator)

| Concept | Skill ID | Prerequisite | Difficulty | Lesson Type | Interaction Template | Assessment | Retrieval/Revision | Transfer Evidence | V1/Roadmap |
|---------|----------|--------------|------------|-------------|---------------------|------------|-------------------|-------------------|------------|
| Trace Variables | `pseudo.trace_variables` | None | Easy | Interactive lesson | Trace | Exact variable state | SRS | Different initial values | V1 |
| Predict Output | `pseudo.predict_output` | Trace Variables | Medium | Interactive lesson | Predict | Exact output | SRS | Different code snippet | V1 |
| Loops | `pseudo.loops` | Trace Variables | Easy | Interactive lesson | Manipulate | Loop count/output | SRS | Different bounds | V1 |
| Nested Loops | `pseudo.nested_loops` | Loops | Medium | Interactive lesson | Trace | Pattern output | SRS | Different pattern | V1 |
| Arrays | `pseudo.arrays` | Nested Loops | Easy | Interactive lesson | Manipulate | Index/output | SRS | Different array ops | V1 |
| Conditions | `pseudo.conditions` | Arrays | Easy | Interactive lesson | Select | Branch output | SRS | Different conditions | V1 |
| Functions | `pseudo.functions` | Conditions | Medium | Interactive lesson | Fill | Return value | SRS | Different params | V1 |
| Recursion basics | `pseudo.recursion` | Functions | Hard | Interactive lesson | Trace | Call stack | SRS | Different recursion | V1 |
| Debugging | `pseudo.debugging` | Recursion | Medium | Interactive lesson | Debug | Test cases pass | SRS | Different bug | V1 |

### 3.5 World 5 — Easy/Med DSA (Service-Level Only)

| Concept | Skill ID | Prerequisite | Difficulty | Lesson Type | Interaction Template | Assessment | Retrieval/Revision | Transfer Evidence | V1/Roadmap |
|---------|----------|--------------|------------|-------------|---------------------|------------|-------------------|-------------------|------------|
| Arrays | `dsa.arrays` | Pseudo Arrays | Easy | Interactive lesson | Manipulate | Index/output | SRS | Different array | V1 |
| Strings | `dsa.strings` | Arrays | Easy | Interactive lesson | Manipulate | String output | SRS | Different string | V1 |
| Hashing | `dsa.hashing` | Arrays | Medium | Interactive lesson | Manipulate | Collision/output | SRS | Different hash | V1 |
| Two Pointers | `dsa.two_pointers` | Arrays | Medium | Interactive lesson | Manipulate | Pair output | SRS | Different target | V1 |
| Sliding Window | `dsa.sliding_window` | Two Pointers | Medium | Interactive lesson | Manipulate | Max sum | SRS | Different window | V1 |
| Sorting | `dsa.sorting` | Arrays | Easy | Interactive lesson | Arrange | Sorted array | SRS | Different sort | V1 |
| Binary Search | `dsa.binary_search` | Sorting | Medium | Interactive lesson | Predict | Index/output | SRS | Different target | V1 |
| Stack/Queue basics | `dsa.stack_queue` | Arrays | Easy | Interactive lesson | Manipulate | Output order | SRS | Different ops | V1 |
| Linked List basics | `dsa.linked_list` | Arrays | Medium | Interactive lesson | Trace | Traversal | SRS | Different list | V1 |
| Tree basics | `dsa.trees` | Linked List | Medium | Interactive lesson | Trace | Traversal | SRS | Different tree | V1 |

### 3.6 World 6 — Company Simulation

| Concept | Skill ID | Prerequisite | Difficulty | Lesson Type | Interaction Template | Assessment | Retrieval/Revision | Transfer Evidence | V1/Roadmap |
|---------|----------|--------------|------------|-------------|---------------------|------------|-------------------|-------------------|------------|
| TCS NQT Blueprint | `company.tcs` | World 1-5 skills | Company | Mock OA | Timed assessment | Score | SRS | Different company | V1 |
| Accenture Blueprint | `company.accenture` | World 1-5 skills | Company | Mock OA | Timed assessment | Score | SRS | Different company | V1 |
| Infosys Blueprint | `company.infosys` | World 1-5 skills | Company | Mock OA | Timed assessment | Score | SRS | Different company | Roadmap |
| Wipro Blueprint | `company.wipro` | World 1-5 skills | Company | Mock OA | Timed assessment | Score | SRS | Different company | Roadmap |
| Cognizant Blueprint | `company.cognizant` | World 1-5 skills | Company | Mock OA | Timed assessment | Score | SRS | Different company | Roadmap |

### 3.7 Roadmap-Only Domains (Post-V1)

| Domain | Skill IDs | Status | Rationale |
|--------|-----------|--------|-----------|
| C programming | `coding.c.fundamentals`, `coding.c.pointers`, `coding.c.memory` | Roadmap | Not in V1 launch scope |
| C++ programming | `coding.cpp.fundamentals`, `coding.cpp.oop`, `coding.cpp.stl` | Roadmap | Not in V1 launch scope |
| Python programming | `coding.python.fundamentals`, `coding.python.collections` | Roadmap | Not in V1 launch scope |
| Java programming | `coding.java.fundamentals`, `coding.java.oop`, `coding.java.collections` | Roadmap | Not in V1 launch scope |
| SQL and databases | `cs_fundamentals.databases.sql` | Roadmap | Not in V1 launch scope |
| CS fundamentals | `cs_fundamentals.oop`, `cs_fundamentals.os`, `cs_fundamentals.networks` | Roadmap | Not in V1 launch scope |
| Advanced DSA | `dsa.graph`, `dsa.dp`, `dsa.backtracking`, `dsa.heap` | Roadmap | Beyond service-level |
| AI Interview | `interview.behavioral`, `interview.technical`, `interview.system_design` | Roadmap | Secondary per PRD §17 |
| Resume/ATS | `resume.build`, `resume.ats` | Roadmap | Secondary per PRD §17 |

---

## 4. Four Programming Language Tracks — Concept Mapping

### 4.1 Canonical Concept (Language-Agnostic)

| Concept | Canonical Skill ID | V1 Status |
|---------|-------------------|-----------|
| Variables and types | `coding.fundamentals.variables` | Roadmap (World 4 pseudocode covers logic only) |
| Conditions | `coding.fundamentals.conditions` | Roadmap |
| Loops | `coding.fundamentals.loops` | Roadmap |
| Functions | `coding.fundamentals.functions` | Roadmap |
| Arrays/Strings | `coding.fundamentals.arrays_strings` | Roadmap |
| Memory/Pointers | `coding.fundamentals.memory` | Roadmap (C-specific) |
| OOP | `coding.fundamentals.oop` | Roadmap |
| Error handling | `coding.fundamentals.error_handling` | Roadmap |
| Collections | `coding.fundamentals.collections` | Roadmap |
| Data structure implementations | `coding.dsa_implementations` | Roadmap |
| Algorithm implementations | `coding.algo_implementations` | Roadmap |
| Timed coding practice | `coding.timed_practice` | Roadmap |

### 4.2 Language Tracks (Roadmap)

| Language | Track Skill ID Prefix | V1 Status | Differentiator per language |
|----------|----------------------|-----------|----------------------------|
| C | `coding.c.*` | Roadmap | Memory, pointers, manual management |
| C++ | `coding.cpp.*` | Roadmap | OOP, STL, RAII, references |
| Python | `coding.python.*` | Roadmap | Collections, dynamic typing, readability |
| Java | `coding.java.*` | Roadmap | OOP-first, exceptions, JVM |

**Rule:** A learner's capability in Java must not automatically imply capability in C or Python. Each language has independent evidence tracking.

---

## 5. Complete DSA Coverage (Roadmap Beyond V1)

| Concept | Skill ID | Prerequisite | Difficulty | V1/Roadmap |
|---------|----------|--------------|------------|------------|
| Arrays | `dsa.arrays` | Pseudo Arrays | Easy | V1 |
| Strings | `dsa.strings` | Arrays | Easy | V1 |
| Hashing | `dsa.hashing` | Arrays | Medium | V1 |
| Two Pointers | `dsa.two_pointers` | Arrays | Medium | V1 |
| Sliding Window | `dsa.sliding_window` | Two Pointers | Medium | V1 |
| Sorting | `dsa.sorting` | Arrays | Easy | V1 |
| Binary Search | `dsa.binary_search` | Sorting | Medium | V1 |
| Stack/Queue basics | `dsa.stack_queue` | Arrays | Easy | V1 |
| Linked List basics | `dsa.linked_list` | Arrays | Medium | V1 |
| Tree basics | `dsa.trees` | Linked List | Medium | V1 |
| Heap | `dsa.heap` | Trees | Hard | Roadmap |
| Graph | `dsa.graph` | Trees | Hard | Roadmap |
| Recursion | `dsa.recursion` | Pseudo Recursion | Hard | Roadmap |
| Greedy | `dsa.greedy` | Graph | Hard | Roadmap |
| Backtracking | `dsa.backtracking` | Recursion | Hard | Roadmap |
| Dynamic Programming | `dsa.dp` | Recursion | Hard | Roadmap |

### 5.1 SQL Coverage (Roadmap)

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | V1/Roadmap |
|---------|----------|--------------|------------|-------------|------------|
| Query writing | `cs_fundamentals.databases.sql.query` | None | Easy | Fill | Roadmap |
| Joins | `cs_fundamentals.databases.sql.joins` | Query writing | Medium | Manipulate | Roadmap |
| Aggregations | `cs_fundamentals.databases.sql.aggregations` | Query writing | Easy | Select | Roadmap |
| Subqueries | `cs_fundamentals.databases.sql.subqueries` | Aggregations | Medium | Fill | Roadmap |
| CTEs | `cs_fundamentals.databases.sql.ctes` | Subqueries | Hard | Fill | Roadmap |
| Window functions | `cs_fundamentals.databases.sql.window` | CTEs | Hard | Fill | Roadmap |
| Data modification | `cs_fundamentals.databases.sql.dml` | Query writing | Easy | Fill | Roadmap |
| Constraints/Keys | `cs_fundamentals.databases.sql.constraints` | Data modification | Easy | Select | Roadmap |
| Normalization | `cs_fundamentals.databases.sql.normalization` | Constraints | Medium | Select | Roadmap |
| Indexes | `cs_fundamentals.databases.sql.indexes` | Normalization | Medium | Select | Roadmap |
| Transactions | `cs_fundamentals.databases.sql.transactions` | Indexes | Hard | Select | Roadmap |

**Rule:** SQL query-writing ability is separate from database-theory understanding.

---

## 6. Computer Science Fundamentals (Roadmap)

| Concept | Skill ID | Prerequisite | Difficulty | Assessment Type | V1/Roadmap |
|---------|----------|--------------|------------|---------------|------------|
| OOP | `cs_fundamentals.oop` | Programming fundamentals | Medium | MCQ + code | Roadmap |
| DBMS | `cs_fundamentals.databases.theory` | None | Easy | MCQ | Roadmap |
| Operating Systems | `cs_fundamentals.os` | None | Medium | MCQ | Roadmap |
| Computer Networks | `cs_fundamentals.networks` | OS | Medium | MCQ | Roadmap |
| Software Engineering | `cs_fundamentals.se` | None | Easy | MCQ + case | Roadmap |
| Testing | `cs_fundamentals.testing` | SE | Medium | MCQ + code | Roadmap |

**Note:** CS theory is tested through MCQs and short-answer, not only code execution.

---

## 7. Company-Specific Placement Preparation (World 6)

| Company | Blueprint ID | Sections | V1 Status |
|---------|-------------|----------|-----------|
| TCS NQT | `company.tcs` | Numerical, Verbal, Reasoning, Pseudocode, Coding | V1 (excellent) |
| Accenture | `company.accenture` | Cognitive, Technical, Coding | V1 (excellent) |
| Infosys | `company.infosys` | Cognitive, Technical, Coding | Roadmap (weights only) |
| Wipro | `company.wipro` | Quantitative, Verbal, Reasoning, Coding | Roadmap (weights only) |
| Cognizant | `company.cognizant` | Cognitive, Technical, Coding | Roadmap (weights only) |

---

## 8. Interview and Career Preparation (Roadmap)

| Capability | Skill ID | V1 Status | Notes |
|------------|----------|-----------|-------|
| Behavioral interview | `interview.behavioral` | Roadmap | STAR method |
| HR interview | `interview.hr` | Roadmap | |
| Technical interview | `interview.technical` | Roadmap | Code + theory |
| System Design | `interview.system_design` | Roadmap | |
| GD topics | `interview.gd` | Roadmap | ~150-200 topics needed |
| Resume/ATS | `resume.build` | Roadmap | Secondary per PRD §17 |
| Career tools | `career.tools` | Roadmap | Secondary per PRD §17 |

---

## 7. Gaps Identified Against Founder's Full List

| Founder Domain | V1 Status | Gap Severity | Notes |
|---------------|-----------|--------------|-------|
| Quantitative aptitude | Complete (World 1) | None | Fully covered in V1 |
| Logical reasoning | Complete (World 2) | None | Fully covered in V1 |
| Verbal ability | Complete (World 3) | None | Fully covered in V1 |
| Programming logic | Complete (World 4) | None | Pseudocode is the differentiator |
| C programming | Roadmap | High | Not in V1 launch scope |
| C++ programming | Roadmap | High | Not in V1 launch scope |
| Python programming | Roadmap | High | Not in V1 launch scope |
| Java programming | Roadmap | High | Not in V1 launch scope |
| DSA (Easy/Med) | Complete (World 5) | None | Service-level only |
| SQL | Roadmap | High | Not in V1 launch scope |
| CS fundamentals | Roadmap | High | Not in V1 launch scope |
| Company simulation | Partial (TCS + Accenture only) | Medium | Other companies weights only |
| AI Interview | Roadmap | Medium | Secondary per PRD |
| Resume/ATS | Roadmap | Medium | Secondary per PRD |
| Captain Byte tutor | Partial | Medium | Spec exists, not implemented |

---

**End of 10 Curriculum Coverage**
