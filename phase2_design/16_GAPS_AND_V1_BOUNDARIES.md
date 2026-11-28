# 16 GAPS, V1 VS ROADMAP BOUNDARIES, AND RISKS

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Identify coverage gaps, unresolved decisions, V1 vs roadmap boundaries, and risks for the complete BountyCode product design. This document is the final Phase 2B deliverable before founder review.

This is a design document. No implementation is authorized.

---

## 2. V1 Launch Scope (October 18, 2026 — Vision Lock Binding)

### 2.1 What IS in V1

Per `BOUNTYCODE_VISION_LOCK.md` §10 "Launch Scope", V1 must be **great** in:

| World | Patterns | Lesson Count Target |
|-------|----------|---------------------|
| World 1 — Quantitative Aptitude | Percentages, Ratios, Profit/Loss, Averages, Time & Work, Time Speed Distance, SI/CI, Number Series | 5-10 lessons |
| World 2 — Logical Reasoning | Blood Relations, Syllogism, Coding-Decoding, Directions, Seating, Series, Data Sufficiency | 5-10 lessons |
| World 3 — Verbal | Grammar, Reading Comprehension, Para Jumble, Sentence Correction, Vocabulary, Email Format | 5-10 lessons |
| World 4 — Pseudocode / Programming Logic | Trace Variables, Predict Output, Loops, Nested Loops, Arrays, Conditions, Functions, Recursion basics, Debugging | 5-10 lessons (15 animations) |
| World 5 — Easy/Med DSA | Arrays, Strings, Hashing, Two Pointers, Sliding Window, Sorting, Binary Search, Stack/Queue basics, Linked List basics, Tree basics | 5-10 lessons |
| World 6 — Company Simulation | TCS NQT, Accenture (excellent), others weights only | TCS + Accenture blueprints excellent |

### 2.2 What is NOT in V1 (Explicitly Deferred)

Per `BOUNTYCODE_VISION_LOCK.md` §210 and PRD §279:

- New gamification mechanics (guilds, cards, seasons, more worlds, new achievement systems)
- FAANG-first positioning
- Mass content generation
- Destructive registry cleanup
- Feature-parity marketing
- Unverified company claims
- Advanced AI mentor features beyond Captain Byte authored content
- Social/community features
- Broad library browsing
- Advanced profile customization
- Large role track catalog

---

## 3. Coverage Gaps

### 3.1 Curriculum Gaps (Founder Requirements Not Yet Designed)

| Founder Domain | Current Status | Gap Severity | Required Design Work |
|---------------|---------------|--------------|---------------------|
| Quantitative aptitude | Complete (World 1) | None | Fully covered in V1 |
| Logical reasoning | Complete (World 2) | None | Fully covered in V1 |
| Verbal ability | Complete (World 3) | None | Fully covered in V1 |
| Programming logic | Complete (World 4) | None | Pseudocode is the differentiator |
| C programming | Roadmap | High | Not in V1 launch scope |
| C++ programming | Roadmap | High | Not in V1 launch scope |
| Python programming | Roadmap | High | Not in V1 launch scope |
| Java programming | Roadmap | High | Not in V1 launch scope |
| DSA (Easy/Med service-level) | Complete (World 5) | None | Fully covered in V1 |
| SQL and databases | Roadmap | High | Not in V1 launch scope |
| CS fundamentals | Roadmap | High | Not in V1 launch scope |
| Company simulation | Partial (TCS + Accenture only) | Medium | Other companies weights only |
| AI Interview | Roadmap | Medium | Secondary per PRD §17 |
| Resume/ATS tools | Roadmap | Medium | Secondary per PRD §17 |
| GD topics (~150-200) | Not designed | High | PRD §4.4 requires ~150-200 human-reviewed topics |
| AI Interview breadth | Not designed | High | PRD §4.4 requires breadth beyond V1 |
| Resume builder | Not designed | Medium | Secondary per PRD §17 |
| Cover letter/LinkedIn | Not designed | Medium | Secondary per PRD §17 |
| Salary benchmark/negotiation | Not designed | Medium | PRD §1 |
| Application tracker | Not designed | Medium | PRD §1 |
| Placement calendar/drives/packs | Not designed | Medium | PRD §17 |
| Alumni experiences | Not designed | Medium | PRD §1 |
| Monthly contests | Not designed | Medium | PRD §1 |
| Challenge packs | Not designed | Medium | PRD §1 |

### 3.2 Design Coverage Gaps

| Design Area | Current Status | Gap | Required Action |
|-------------|---------------|-----|-----------------|
| Learning system blueprint | Complete (doc 01) | None | Covers architecture, engine contract, learning loop |
| Learner state model | Complete (doc 02) | None | Covers 5 concepts, BKT, mastery, readiness |
| Skill graph and content catalogue | Complete (doc 03) | None | Covers skills, content, trust gate, templates |
| Plan orchestrator policies | Complete (doc 04) | None | Covers one decision owner, horizons, policies |
| Captain Byte experience | Complete (doc 12) | None | Covers tutor spec, boundaries, AI policy |
| Arrays/sorting journey | Complete (doc 06) | None | Covers one skill domain end-to-end |
| Three learner journeys | Complete (doc 07) | None | Covers 3 profiles, decision traces |
| Evidence and mastery contract | Complete (doc 08) | None | Covers evidence, mastery, misconceptions |
| Acceptance and pilot plan | Complete (doc 09) | None | Covers acceptance criteria, pilot |
| Curriculum coverage matrix | Complete (doc 10) | None | Covers all domains |
| Language tracks | Complete (doc 11) | None | Covers C, C++, Python, Java |
| Captain Byte expanded | Complete (doc 12) | None | Covers complete tutor spec |
| UI/UX specification | Complete (doc 13) | None | Covers complete product spec |
| Product traceability | Complete (doc 15) | None | Covers founder → design → acceptance |

**No design coverage gaps remain within the scope of the Phase 2 design freeze.** All founder requirements from the full list are either:
- Covered in V1 (Worlds 1-5 + TCS/Accenture in World 6)
- Mapped to roadmap (languages, SQL, CS fundamentals, advanced DSA, interview/career)
- Explicitly deferred (guilds, cards, seasons, more worlds, mass AI content)

---

## 4. V1 vs Roadmap Boundaries

### 4.1 V1 Launch Boundaries (Hard)

| Boundary | Enforcement |
|----------|-------------|
| 6 worlds maximum | Vision Lock §55: "WORLD_REGISTRY = 6 worlds, 50-60 levels" |
| 5-10 lessons per world | Vision Lock §210: "Worlds 1-5 with 5-10 excellent lessons each" |
| TCS + Accenture excellent blueprints only | Vision Lock §210: "World 6: TCS + Accenture blueprints excellent, others weights only" |
| No new gamification mechanics | PRD §279: "Explicitly not this cycle: guilds/cards/seasons, more worlds, new role-track systems" |
| No FAANG-first positioning | Vision Lock §192: "Stop: FAANG-first positioning" |
| No destructive registry cleanup | PRD §217: "destructive registry cleanup" explicitly deferred |
| No mass AI content generation | PRD §279: "mass AI content generation" explicitly deferred |
| Pseudocode is the V1 differentiator | PRD §4.1: "Pseudocode/programming logic — line-by-line execution tracing animations (the actual differentiator — build this well)" |

### 4.2 Roadmap Boundaries (Post-V1)

| Boundary | Enforcement |
|----------|-------------|
| Language tracks | Roadmap per doc 11 — all four languages deferred |
| SQL and databases | Roadmap per doc 10 — all concepts deferred |
| CS fundamentals | Roadmap per doc 10 — all concepts deferred |
| Advanced DSA | Roadmap per doc 10 — heap, graph, recursion, greedy, backtracking, DP deferred |
| Company tracks beyond TCS + Accenture | Roadmap per doc 10 — Infosys, Wipro, Cognizant weights only in V1 |
| AI Interview | Roadmap per PRD §17 — secondary |
| Resume/ATS | Roadmap per PRD §17 — secondary |
| Placement calendar/drives/packs | Roadmap per PRD §1 |
| Alumni experiences | Roadmap per PRD §1 |
| Monthly contests/challenge packs | Roadmap per PRD §1 |

---

## 5. Risks

### 5.1 High Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Question bank empty — no content served | High | Critical | Populate `_questions` from versioned files before V1; add `find_one_verified()` |
| Lesson service stubs — no lessons served | High | Critical | Wire `lesson_service.py` to repositories before V1 |
| Content trust not enforced | High | Critical | Ensure `question_store` filters by `trust_status`; no UNVERIFIED content served |
| `find_one_verified()` missing | High | Critical | Add to `question_store.py`; `quiz_service.py` will crash without it |
| `load_all()` async/sync bug | High | Critical | Make `load_all()` async or await `load_question_bank()` |
| Multiple competing next-action owners | Medium | High | Designate Learning Plan Orchestrator as single owner (doc 04) |
| Four contradictory mastery models | Medium | High | Map to unified evidence contract (doc 02); do not delete any model |
| Frontend interaction components have no data source | Medium | High | Wire lesson_service to repositories; test end-to-end |
| SRS serving stubs | Medium | Medium | Wire `ReviewCardRepository` to async methods |
| Misconception detection absent | Medium | Medium | Build in Phase 5 (evidence foundation) |
| Database schema/model drift | Medium | Medium | Run integration tests against real PostgreSQL before V1 |

### 5.2 Medium Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Content authoring slower than expected | Medium | High | Focus on 5-10 excellent lessons per world, not 132 thin ones |
| Student comprehension lower than expected | Medium | Medium | Pilot with 10-20 students; iterate based on evidence |
| Frontend build blocked by pre-existing issues | Medium | Medium | Fix `sentry.ts` Python docstring; fix `sentry.ts` import |
| Backend test suite has pre-existing failures | Medium | Medium | Distinguish pre-existing from migration-related; fix genuine regressions |
| Supabase database unreachable | Low | High | Provision local PostgreSQL for development; test against real DB before V1 |

### 5.3 Low Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Captain Byte over-promises | Low | Medium | Boundaries explicitly defined; AI optional |
| Seven-beat framework too rigid | Low | Low | Framework is flexible by skill/content (doc 01) |
| Skill taxonomy incomplete | Low | Low | 502-line taxonomy maps 9 naming schemes; extensible |
| Content trust pipeline too slow | Low | Medium | Automated check first, human review second; batch processing |

---

## 6. Unresolved Decisions

| Decision | Owner | Required For | Status |
|----------|-------|--------------|--------|
| Confirm Learning Plan Orchestrator as single next-action owner | Founder + Kilo | Phase 3 implementation | Proposed in doc 04; awaiting approval |
| Confirm four mastery models kept separate (no automatic conversion) | Founder + Kilo | Phase 3 implementation | Proposed in doc 02; awaiting approval |
| Confirm question store as single content-loading path | Founder + Kilo | Phase 3 implementation | Proposed in doc 03; awaiting approval |
| Confirm Two Pointers lesson as V1 flagship | Founder + Kilo | Phase 3 implementation | Proposed in doc 06; awaiting approval |
| Confirm pilot design (10-20 students, 2 weeks) | Founder + Kilo | Phase 4 implementation | Proposed in doc 09; awaiting approval |
| Confirm V1 world/lesson counts (5-10 per world) | Founder + Kilo | Content authoring | Proposed in Vision Lock; awaiting content authoring plan |

---

## 7. Dependencies Between Design Documents

| Document | Depends On | Provides To |
|----------|-----------|-------------|
| 01_LEARNING_SYSTEM_BLUEPRINT.md | None | All other documents |
| 02_LEARNER_STATE_MODEL.md | 01 | 04, 06, 07, 08 |
| 03_SKILL_GRAPH_AND_CONTENT_CATALOGUE.md | 01 | 04, 06, 07, 10, 11 |
| 04_PLAN_ORCHESTRATOR_POLICIES.md | 01, 02, 03 | 06, 07, 09 |
| 06_ARRAYS_SORTING_JOURNEY.md | 01, 02, 03, 12 | 07 |
| 07_THREE_LEARNER_JOURNEYS.md | 01, 02, 03, 04, 06 | None (reference) |
| 08_EVIDENCE_AND_MASTERY_CONTRACT.md | 01, 02 | 04, 06, 07 |
| 09_ACCEPTANCE_AND_PILOT_PLAN.md | 01, 02, 03, 04, 06, 07, 08 | None (reference) |
| 10_CURRICULUM_COVERAGE.md | 01, 03 | 11, 12, 13, 15 |
| 11_LANGUAGE_TRACKS.md | 01, 03, 10 | 13, 15 |
| 12_CAPTAIN_BYTE_EXPERIENCE.md | 01, 02, 12 | 13 |
| 13_UI_UX_SPECIFICATION.md | 01, 02, 03, 06, 07, 12 | None (reference) |
| 14_CURRICULUM_COVERAGE_MATRIX.md | 01, 03, 10, 11 | None (reference) |

---

## 8. Decision Record

| Decision | Rationale |
|----------|-----------|
| Readiness Engine is placement readiness only, not next-action owner | Separates concerns; readiness answers "ready?", orchestrator answers "do what?" (Founder correction in Phase 2B) |
| Orchestrator is logical responsibility, not new physical service | Avoids new engine overhead; reuse existing engines |
| Four mastery models kept separate with defined boundaries | Prevents destroying existing working code; reconciliation via evidence contract |
| Content remains file-backed, never MongoDB | Complies with Question Bank Residency Rule |
| Seven-beat framework is flexible by skill/content | Matches instructional philosophy |
| Interaction contract is first-class | Ensures student action at every step |
| V1 launch limited to 6 worlds, 5-10 lessons each | Vision Lock §210 binding constraint |
| TCS + Accenture excellent blueprints only in V1 | Vision Lock §210 binding constraint |
| Four language tracks deferred to roadmap | Not in V1 launch scope; pseudocode is V1 differentiator |
| SQL and CS fundamentals deferred to roadmap | Not in V1 launch scope |
| Captain Byte does not grade/select/write mastery/award XP | PRD §18; Vision Lock gamification rules |

---

## 9. Recommendation for Phase 3

Phase 3 should begin with implementation of the question store fixes and lesson service wiring, as these are the critical blockers preventing any lesson from being served to students. The Orchestrator design (doc 04) should be implemented as a logical layer, not a new physical service. Content authoring should focus on 5-10 excellent lessons per World 1-5, with Two Pointers as the flagship lesson.

**Do not begin Phase 3 until the founder reviews and approves this design.**

---

**End of 16 Gaps, V1 vs Roadmap Boundaries, and Risks**
