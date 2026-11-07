# Curriculum gap audit and first content expansion

**Date:** 2026-11-07  
**Branch:** `curriculum/fill-core-learning-gaps`

## Audit basis

The repository contains several curriculum systems. The interactive placement lesson API is backed by `backend/app/services/lessons/__init__.py` and `lesson_service.py`; lesson modules must be registered there to appear in `GET /api/v1/lessons`. Other content banks and routes exist, but their existence alone does not make them part of this learner-facing lesson catalog.

The existing `CONTENT_RECONCILIATION.md` is dated 2026-09-08. It reported 0 system-design and 0 debugging questions in the question-store student-serving pool, 29 behavioral questions, and uneven explanation coverage in verified question content. These are historical audit findings, not a claim that the current runtime has been re-counted.

## Confirmed repository gaps addressed in this change

| Area | Existing foundation | Gap addressed |
|---|---|---|
| Debugging | AI debugger endpoints and a debugging question bank | No dedicated debugging track in the interactive lesson catalog |
| System design | System-design question bank and interview routes | No dedicated system-design track in the interactive lesson catalog |
| Behavioral interviews | Existing company preparation and behavioral question data | No dedicated, sequenced behavioral communication lesson track |

## New learner-facing lessons

### Debugging
- A Reliable Debugging Workflow
- Trace Logic and Test Edge Cases

Covers reproducible failures, error classification, variable tracing, boundary tests, and regression verification.

### System design
- System Design: Requirements and Constraints
- System Design: Traffic, Caching, and Trade-offs

Covers functional/non-functional requirements, measurable constraints, rough capacity estimates, cache-aside, and freshness trade-offs.

### Behavioral interviews
- Answer Behavioral Questions with STAR
- Teamwork and Handling Disagreement

Covers truthful STAR answers, personal contribution, respectful disagreement, and reflective learning.

## Integration

- Registered all three tracks in the lesson catalog.
- Added skill-graph mappings for debugging, system design, and behavioral communication.
- Added a regression test that checks track registration and valid skill mappings.
- Lessons use the existing server-side quiz grading and answer-key sanitization path.

## Still outstanding

This is the first focused expansion, not a claim that the full A–Z blueprint is complete. Remaining work includes a full topic-by-topic inventory against the ten curriculum pillars, deeper programming-language and DSA lesson coverage, SQL labs and CS fundamentals, aptitude/reasoning/verbal depth, project-based milestones, company syllabus verification, and quality review of the existing large question bank.

## Validation status

Source files and imports were inspected after the changes. Automated backend tests and a full application run have **not** been executed in this GitHub-only editing pass. Run the backend lesson test suite and API smoke tests before merging.


## Second audit pass — programming and DSA

A source-level inventory of the registered lesson modules found **130 lesson objects across 17 registered tracks/modules** on this branch. This is a count of lesson objects, not proof that every planned concept is covered or that all code examples execute.

### Concrete issues found and fixed

- The repository had Python, C++, and Java lesson modules, but no registered C-language lesson module. Added a C track with four sequenced lessons covering program structure, variables/input, conditions/loops, arrays, functions, and pointers.
- Several Java lesson examples contained C++ output syntax (`cout` and `endl`), and the first Java lesson incorrectly described `#include <iostream>`. Corrected the Java examples to use `System.out.println` and the accurate Java program entry-point explanation.
- The DSA module covered a small foundation set but did not have dedicated lessons for hashing, recursion, graph traversal, or dynamic programming. Added a first lesson for each of those topics.
- Added tests to check C track registration and skill mapping, reject C++ output syntax in Java lessons, and verify the new DSA topics map to their intended canonical skills.
- Expanded the Learning Experience CI path filters so edits to the registered lesson modules, lesson service, skill taxonomy, and lesson tests trigger the targeted workflow.

### Registered lesson inventory snapshot

| Track/module | Lesson objects |
|---|---:|
| Python (two modules) | 18 |
| Java | 12 |
| C++ | 13 |
| C | 4 |
| DSA | 12 |
| DBMS | 11 |
| Operating systems | 8 |
| Computer networks | 8 |
| Aptitude | 10 |
| Logical reasoning | 7 |
| Verbal ability | 6 |
| OOP | 4 |
| Company preparation | 11 |
| Debugging | 2 |
| System design | 2 |
| Behavioral | 2 |
| **Total** | **130** |

### Important limitations

- This inventory covers the interactive lesson catalog modules that were inspected. It does not claim to inventory every separate question bank, generated curriculum file, or content endpoint in the repository.
- The DSA track remains incomplete relative to the blueprint: two pointers, sliding window, greedy patterns, backtracking, heaps, advanced trees, shortest paths, MST, and advanced DP still need dedicated lessons and assessments.
- SQL depth, DBMS concurrency/recovery/indexing, OS synchronization and memory management, networking subnetting/routing/TLS, computer architecture, and the full aptitude/verbal syllabus still require topic-by-topic coverage work.
- The C track is a foundation, not a complete C-to-advanced curriculum.
- Java and C lesson code samples have not yet been executed in a compiler as part of this editing pass.

## Next implementation sequence

1. Expand DSA patterns and advanced data structures, then add unseen assessments.
2. Expand SQL and DBMS with query exercises, output prediction, normalization, transactions, indexing, and concurrency.
3. Expand OS, networking, and computer architecture with worked examples and topic tests.
4. Expand quantitative aptitude, reasoning, and verbal modules.
5. Add complete project pathways and verified company-specific syllabi.
6. Continue enforcing the 13-part lesson standard from the blueprint: objectives, prerequisites, intuition, explanation, visual, code, pattern recognition, misconceptions, guided practice, assessment, mastery, spaced repetition, and real-world/interview connection.

## Validation update

The changed files have been re-fetched from the feature branch. GitHub Actions CI was observed queued/in progress during this pass; no successful test result is claimed yet. The compiler and full learner flow still need verification before merge.


## Third audit pass — SQL and DBMS

The existing interactive DBMS module had lessons for introductory SQL, joins, normalization, and ACID, but it did not provide a clear progression into grouped reporting, subqueries/CTEs, indexing/query plans, and transaction isolation. Added four lessons to cover those topics:

- SQL joins and grouped reports (JOIN, GROUP BY, HAVING)
- SQL subqueries and CTEs
- Database indexes and query plans
- Transactions and isolation levels

Each lesson includes explanations, code/query examples, an exercise, and a quiz. Added a regression test to confirm these lessons are registered and mapped to the existing DBMS skill.

The SQL examples are general relational SQL. Exact syntax and isolation semantics can vary between database engines; the lessons call this out rather than claiming all engines behave identically.

## CI findings

The targeted Learning Experience workflow ran, but its backend test collection failed before running the lesson tests. The reported import errors are in existing learning-engine dependencies: `adaptive_learning.py`, `learning_paths.py`, and `quiz.py` import collection names that are not exported by `app.database` (`user_company_tracks_collection`, `user_learning_paths_collection`, and `learning_events_collection`). Those files were not changed in this curriculum pass, so this is recorded as a pre-existing integration blocker rather than silently changed as part of content authoring.

The full CI workflow was still running when this audit note was updated. No passing full-suite result is claimed.


## Fourth audit pass — Operating systems and networking

Added three operating-systems lessons:
- Threads, race conditions, mutexes and semaphores
- Deadlock prevention, avoidance, detection and recovery
- Page faults, FIFO and LRU page replacement

Added three networking lessons:
- IPv4 prefixes, subnet masks and a worked /24 example
- DNS resolution, HTTPS and TLS concepts
- TCP versus UDP, the three-way handshake, flow control and congestion control

Added regression tests confirming all six lessons are registered and mapped to the existing operating-systems and computer-networks skill IDs.

Remaining core-subject gaps include deeper CPU scheduling calculations, synchronization exercises, file systems and disk scheduling; IPv6, routing, switching, DHCP, NAT, proxies, firewalls, and more subnetting practice; and a dedicated computer-architecture lesson track.
