# 09 ACCEPTANCE AND PILOT PLAN

**BountyCode — Phase 2 Design Freeze**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define acceptance criteria for the learning system design and a pilot plan
for validating it with real students. This document specifies what must be
true before Phase 3 implementation begins, and how the first real-student
pilot should be conducted.

This is a design document. No implementation is authorized.

---

## 2. Acceptance Criteria

### 2.1 Design Acceptance (Before Phase 3)

| # | Criterion | How Verified |
|---|-----------|--------------|
| A1 | One next-action decision owner identified | Document 04 names Learning Plan Orchestrator |
| A2 | Readiness Engine separated from Orchestrator | Document 04 shows separate responsibilities |
| A3 | Five learner concepts defined | Document 02 defines context, evidence, state, mastery, readiness |
| 4 | Four mastery models reconciled | Document 02 shows no automatic conversion |
| 5 | Content trust pipeline defined | Document 03 shows 4-level pipeline |
| 6 | Only TRUSTED content servable | Document 03 shows UNVERIFIED never served |
| 7 | Interaction contract defined | Document 01 defines 9 interaction templates |
| 8 | Seven-beat framework mapped | Document 01 maps Feel→Discover→Predict→Build→Break→Debug→Retrieve→Transfer |
| 9 | Misconception taxonomy defined | Document 08 defines 5 misconception IDs |
| 10 | Independent retest required | Document 08 requires retest after repair |
| 11 | No LLM for grading/mastery/readiness | Document 01 states AI may paraphrase only |
| 12 | Captain Byte boundaries defined | Document 05 lists what Captain Byte may/may not do |
| 13 | Extensibility without plugin platform | Document 01 states no microservices |
| 14 | Two full learner journeys designed | Documents 06 and 07 |
| 15 | Pilot plan defined | Document 09 |

### 2.2 Implementation Acceptance (Before Phase 4 Pilot)

| # | Criterion | How Verified |
|---|-----------|--------------|
| B1 | Question store serves verified content | `question_store.find()` returns non-empty list from versioned files |
| B2 | `find_one_verified()` exists and works | Returns only `trust_status == "TRUSTED"` questions |
| 3 | Lesson service wired to repositories | `get_public_lesson()` returns actual lesson content |
| 4 | Orchestrator makes next-action decisions | Returns a `next_action` object with `kind` and `skill_id` |
| 5 | Evidence events persisted to PostgreSQL | `learning_attempts` table populated after student action |
| 6 | Mastery Engine computes 0-5 levels | `calculate_mastery_level()` returns correct level for test inputs |
| 7 | Readiness Engine computes 0-100 score | `calculate_target_readiness()` returns score and coverage |
| 8 | SRS serving works | `get_due_cards()` returns cards from PostgreSQL |
| 9 | Prerequisite Graph validates DAG | `validate_prerequisite_graph()` returns empty errors |
| 10 | Frontend lesson renders with backend data | LessonPlayer loads content from API |
| 11 | No untrusted content served | `question_store` filters by `trust_status` |
| 12 | No client-side XP writes | All XP goes through `record_practice()` |

---

## 3. Pilot Plan

### 3.1 Pilot Objectives

The pilot is exploratory. It does NOT aim to prove scientific superiority.
It aims to validate that:

1. Students can complete an interactive learning journey end-to-end.
2. The seven-beat framework produces meaningful student actions.
3. Evidence events are correctly captured and persisted.
4. The Orchestrator produces sensible next actions.
5. Students understand Captain Byte guidance.

### 3.2 Pilot Design

| Element | Specification |
|---------|---------------|
| **Participants** | 10–20 real students (Indian engineering students, tier-2/3 colleges) |
| **Duration** | 2 weeks |
| **Time commitment** | 20–30 minutes per day |
| **Content** | Arrays and Sorting journey (World 1, Code Foundations) |
| **Devices** | Mobile-first (360px viewport), desktop optional |
| **Connectivity** | Uneven internet (simulate with throttling) |
| **Incentive** | Certificate of completion + small stipend |

### 3.3 Comparison (Optional, Exploratory Only)

If feasible, split participants into two groups:

| Group | Experience |
|-------|------------|
| A (Interactive) | Seven-beat interactive journey with Captain Byte |
| B (Conventional) | Explanation → Read → Quiz (traditional format) |

**Keep comparable:** Same content quality, same difficulty, same assessment conditions, same time budget.

**Do NOT claim scientific superiority** based on a small cohort. This is exploratory.

### 3.4 Measures

| Measure | When | How |
|---------|------|-----|
| Immediate independent solving | End of journey | First-attempt accuracy without hints |
| Next-day recall | Day 2 | SRS review accuracy |
| One-week transfer | Day 7 | New problem using same concept |
| Error recovery | During journey | Hints used before correct answer |
| First-attempt accuracy | Throughout | % correct on first try |
| Learner understanding | Post-session survey | Self-rated understanding (1–5) |
| Completion friction | Throughout | Drop-off points, time per step |
| Accessibility/usability | Post-pilot | System Usability Scale (SUS) |

### 3.5 Success Indicators (Directional Only)

| Indicator | Target | Notes |
|-----------|--------|-------|
| Journey completion rate | > 70% | Directional, not statistical |
| First-attempt accuracy (no hints) | > 60% | Directional |
| Next-day recall accuracy | > 70% | Directional |
| SUS score | > 68 | Average usability |
| Drop-off before lesson 3 | < 20% | Directional |

**These are NOT success/failure gates.** They inform iteration.

### 3.6 Hypothesis

**Primary hypothesis (exploratory):**
Students who complete the seven-beat interactive journey show better
next-day recall and transfer performance than students who complete a
conventional explanation-read-quiz format with equivalent content.

**Null hypothesis:** No difference between groups.

**Alternative:** Either direction is possible. The pilot is too small to
detect small effects.

---

## 4. Research Foundation

The following techniques used in BountyCode's design are supported by
research. These are research findings, not BountyCode claims.

| Technique | Research Basis | Application in BountyCode |
|-----------|---------------|---------------------------|
| Retrieval practice | Roediger & Karpicke (2006) | SRS reviews, delayed recall |
| Spaced repetition | Ebbinghaus (1885), Cepeda et al. (2006) | SM-2 algorithm, review scheduling |
| Worked examples | Sweller (1988), Renkl (2014) | Fully worked examples before practice |
| Faded guidance | Renkl & Atkinson (2003) | Progressive hint ladder, scaffolding fade |
| Predict-then-instruct | Schwartz & Bransford (1998) | Predict beat before explanation |
| Deliberate practice | Ericsson et al. (1993) | Targeted practice on weak areas |
| Transfer | Barnett & Ceci (2002) | Changed-context tasks |
| Formative assessment | Black & Wiliam (1998) | Immediate feedback, misconception detection |

**Distinction:** These research findings support individual techniques.
BountyCode's specific combination and implementation are hypotheses to be
tested, not established findings.

---

## 5. Data Privacy

| Data | Collected? | Stored Where? | Retention |
|------|-----------|---------------|-----------|
| Evidence events | Yes | PostgreSQL | Pilot duration + 30 days |
| Student identifiers | Yes (email/ID) | PostgreSQL | Pilot duration + 30 days |
| Interaction traces | Yes | PostgreSQL | Pilot duration + 30 days |
| Captain Byte conversations | No (authored text only) | N/A | N/A |
| AI-generated content | No (AI optional) | N/A | N/A |

### 5.1 Consent

Students must provide informed consent before data collection. Consent form
must explain:

- What data is collected
- How it is used (learning improvement only)
- Who has access (BountyCode team only)
- How long it is retained
- Right to withdraw

---

## 6. Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Small sample (10–20 students) | Cannot detect small effects | Treat as exploratory only |
| Short duration (2 weeks) | Cannot measure long-term retention | Measure next-day and 1-week only |
| Single content domain (Arrays) | Results may not generalize | Pilot one domain first |
| Self-selected participants | May not represent all students | Acknowledge selection bias |
| No control group (optional) | Cannot attribute causation | Compare groups if feasible |
| Mobile-first only | May miss desktop issues | Test on both |

---

## 7. Go/No-Go Criteria for Pilot → Phase 3 Scaling

| Criterion | Go Signal | No-Go Signal |
|-----------|-----------|--------------|
| Journey completion | > 70% of pilot students complete Arrays journey | < 40% complete |
| First-attempt accuracy | > 60% correct without hints | < 40% |
| Technical errors | < 5% of sessions have crashes | > 15% crash rate |
| Student understanding | Average self-rating ≥ 3.5/5 | Average < 2.5/5 |
| Orchestrator decisions | > 80% of next actions make sense to reviewers | < 50% make sense |

**Go/No-Go decision is made by the founder after reviewing pilot data,
not automatically.**

---

## 8. Phase 3 Recommendation

The correct implementation sequence is:

**Design approval → Phase 3 implementation → Internal end-to-end validation → Real-student pilot → Evaluate results → Decide what to scale or revise**

The pilot requires the Phase 3 implementation to exist first (question store fixed, lesson service wired to repositories, SRS serving connected, Orchestrator implemented, one complete lesson built). Pilot results cannot gate Phase 3 because the pilot depends on Phase 3 output.

If the Phase 3 implementation passes internal end-to-end validation, Phase 3 should:

1. Fix the question store (`_questions` population, `find_one_verified()`)
2. Wire lesson service to repositories
3. Wire SRS serving to `ReviewCardRepository`
4. Implement the Learning Plan Orchestrator (logical, not new service)
5. Build one complete interactive lesson (Arrays: Two Pointers)
6. Test end-to-end with real students (pilot)

If the pilot shows negative signals, revisit the design before scaling to additional lessons.

---

## 9. Documents in This Phase

| Document | Responsibility |
|----------|---------------|
| 01_LEARNING_SYSTEM_BLUEPRINT.md | Overall architecture |
| 02_LEARNER_STATE_MODEL.md | Five concepts, BKT, mastery, readiness |
| 03_SKILL_GRAPH_AND_CONTENT_CATALOGUE.md | Skills, content, interaction templates |
| 04_PLAN_ORCHESTRATOR_POLICIES.md | One decision owner, three horizons |
| 12_CAPTAIN_BYTE_EXPERIENCE.md | Tutor, state machine, boundaries |
| 06_ARRAYS_SORTING_JOURNEY.md | Seven-beat example, test matrix |
| 07_THREE_LEARNER_JOURNEYS.md | Three profiles, decision traces |
| 08_EVIDENCE_AND_MASTERY_CONTRACT.md | Evidence, mastery, misconceptions |
| 09_ACCEPTANCE_AND_PILOT_PLAN.md | Acceptance criteria, pilot |

All nine documents are internally consistent and cross-referenced.

---

## 10. Design Review Checklist (Final)

| # | Question | Status |
|---|----------|--------|
| 1 | Acceptance criteria are measurable? | Yes |
| 2 | Pilot is exploratory, not scientific? | Yes |
| 3 | Go/No-Go criteria defined? | Yes |
| 4 | Data privacy addressed? | Yes |
| 5 | Limitations acknowledged? | Yes |
| 6 | Research distinguished from claims? | Yes |
| 7 | Phase 3 recommendation clear? | Yes |
| 8 | No implementation in this phase? | Yes |

---

**End of 09 Acceptance and Pilot Plan**
