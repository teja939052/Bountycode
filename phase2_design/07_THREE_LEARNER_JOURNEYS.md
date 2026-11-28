# 07 THREE LEARNER JOURNEYS

**BountyCode — Phase 2 Design Freeze**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Show how the same architecture serves three different learner profiles through
the Arrays and Sorting journey. Each profile starts at a different state,
receives a different diagnostic, and follows a different path through the same
content.

This is a design document. No implementation is authorized.

---

## 2. Learner Profile 1 — Absolute Beginner

### 2.1 Initial State

| Field | Value |
|-------|-------|
| Name | "Arjun" |
| Role | `sde` |
| Target company | `tcs` |
| Experience level | `absolute_beginner` |
| Preferred language | `python` |
| Daily time budget | 45 minutes |
| Arrays state | `unknown` (0 distinct questions) |
| Loops state | `unknown` |
| Variables state | `unknown` |

### 2.2 Diagnostic

The Orchestrator assesses Arjun's context and determines he has no prior
programming evidence. The diagnostic starts with `coding.variables` (a leaf
skill with no prerequisites).

**First action:** `learn` → `coding.variables` lesson (explain stage).

### 2.3 Journey Map (First 3 Days)

#### Day 1 (45 minutes)

| Time | Activity | Interaction | Evidence |
|------|----------|-------------|----------|
| 0–10 min | Variables: explain | `select` | Correctly identifies variable assignment |
| 10–25 min | Variables: predict | `predict` | Predicts output of `x = 5; x = x + 1` |
| 25–45 min | Variables: build | `fill` | Completes variable swap code |

**Orchestrator decision:** Next action = `learn` → `coding.loops` (prerequisite for arrays).

#### Day 2 (45 minutes)

| Time | Activity | Interaction | Evidence |
|------|----------|-------------|----------|
| 0–15 min | Loops: discover | `manipulate` | Moves pointer through array |
| 15–30 min | Loops: predict | `predict` | Predicts loop termination |
| 30–45 min | Loops: build | `fill` | Completes loop to sum array |

**Orchestrator decision:** Next action = `learn` → `dsa.arrays` (loops now at level 2, approaching Competent).

#### Day 3 (45 minutes)

| Time | Activity | Interaction | Evidence |
|------|----------|-------------|----------|
| 0–15 min | Loops: predict | `predict` | Predicts loop termination (question 4) |
| 15–25 min | Loops: build | `fill` | Completes loop to sum array (questions 5-6) |
| 25–45 min | Loops: practice | `predict` | Predicts loop execution on new problems (questions 7-8) |

**Orchestrator decision:** Loops now at level 3 (Competent) with 6 distinct questions. Prerequisite met for arrays. Next action = `learn` → `dsa.arrays` lesson (feel stage).

### 2.4 Progress After Week 1

| Skill | BKT State | Mastery Level | Evidence |
|-------|-----------|---------------|----------|
| `coding.variables` | `independent` | 2 (Practicing) | 3 distinct questions, 75% accuracy |
| `coding.loops` | `independent` | 3 (Competent) | 6 distinct questions, 75% accuracy |
| `dsa.arrays` | `unknown` | 0 (Unknown) | 0 distinct questions |

### 2.5 Captain Byte Interactions

- Day 1: "Great start! You understood variables on your first try."
- Day 2: "Loops take practice. Let's trace through this together."
- Day 3: "Loops mastered. Now let's start arrays - watch how the left pointer moves when the sum is too small?"

---

## 3. Learner Profile 2 — Intermediate

### 3.1 Initial State

| Field | Value |
|-------|-------|
| Name | "Priya" |
| Role | `sde` |
| Target company | `infosys` |
| Experience level | `experienced` |
| Preferred language | `java` |
| Daily time budget | 60 minutes |
| Arrays state | `independent` (BKT 0.72) |
| Loops state | `independent` |
| Variables state | `transfer_capable` |

### 2.2 Diagnostic

Priya has prior programming evidence. The Orchestrator skips `coding.variables` and
`coding.loops` (already at level 3+). The diagnostic starts directly with
`dsa.arrays` at the predict stage.

**First action:** `learn` → `dsa.arrays` → predict stage (skip feel and discover).

### 2.3 Journey Map (First 2 Days)

#### Day 1 (60 minutes)

| Time | Activity | Interaction | Evidence |
|------|----------|-------------|----------|
| 0–15 min | Arrays: predict | `predict` | Correctly predicts pointer movement |
| 15–30 min | Arrays: build | `fill` | Two-sum implementation, all tests pass |
| 30–45 min | Arrays: break | `debug` | Finds unsorted input that breaks code |
| 45–60 min | Arrays: debug | `debug` | Fixes boundary condition |

**Orchestrator decision:** Priya is at `independent` for arrays. Next action = `transfer` → container-with-most-water problem.

#### Day 2 (60 minutes)

| Time | Activity | Interaction | Evidence |
|------|----------|-------------|----------|
| 0–30 min | Arrays: transfer | `transfer` | Solves container problem independently |
| 30–45 min | Arrays: retrieve | `select` | Answers prediction question (SRS) |
| 45–60 min | Binary search: learn | `learn` | Starts `dsa.binary_search` (prerequisite: dsa.arrays met) |

**Orchestrator decision:** Arrays now at `transfer_capable`. Binary search unlocked (prerequisite met).

### 2.4 Progress After Week 1

| Skill | BKT State | Mastery Level | Evidence |
|-------|-----------|---------------|----------|
| `dsa.arrays` | `independent` | 3 (Competent) | 8 distinct questions, 85% accuracy |
| `coding.variables` | `transfer_capable` | 4 (Strong) | 12 distinct questions, 88% accuracy |
| `coding.loops` | `independent` | 3 (Competent) | 7 distinct questions, 72% accuracy |
| `dsa.binary_search` | `emerging` | 2 (Practicing) | 3 distinct questions, 67% accuracy |
| `dsa.binary_search` | `emerging` | 2 (Practicing) | 3 distinct questions, 67% accuracy |

### 2.5 Captain Byte Interactions

- Day 1: "You moved through the build quickly. Let's see if you can break it."
- Day 2: "Container problem uses the same two-pointer idea. Nice transfer."

---

## 4. Learner Profile 3 — Advanced with Gap

### 4.1 Initial State

| Field | Value |
|-------|-------|
| Name | "Rahul" |
| Role | `sde` |
| Target company | `wipro` |
| Experience level | `experienced` |
| Preferred language | `cpp` |
| Daily time budget | 30 minutes |
| Arrays state | `independent` (BKT 0.72) |
| Two Pointers state | `unknown` (never assessed) |
| Sliding Window state | `unknown` |

### 2.2 Diagnostic

Rahul knows arrays well but has never been assessed on Two Pointers. The
Orchestrator sees `dsa.two_pointers` as unassessed with prerequisite
`dsa.arrays` already met.

**First action:** `diagnostic` → `dsa.two_pointers` (skip learn, go straight to assessment).

### 2.3 Journey Map (First 2 Days)

#### Day 1 (30 minutes)

| Time | Activity | Interaction | Evidence |
|------|----------|-------------|----------|
| 0–10 min | Two Pointers: diagnostic | `predict` | Predicts pointer movement (3 scenarios) |
| 10–20 min | Two Pointers: build | `fill` | Two-sum implementation |
| 20–30 min | Two Pointers: assess | `transfer` | Container problem |

**Orchestrator decision:** Rahul scores 85% on diagnostic. Arrays prerequisite met. Two Pointers at `transfer_capable` (BKT 0.85).

#### Day 2 (30 minutes)

| Time | Activity | Interaction | Evidence |
|------|----------|-------------|----------|
| 0–15 min | Two Pointers: transfer | `transfer` | Container with most water |
| 15–25 min | Sliding Window: learn | `learn` | Starts `dsa.sliding_window` (prerequisite: dsa.two_pointers at independent) |
| 25–30 min | SRS review | `select` | Reviews arrays pointer rule |

**Orchestrator decision:** Sliding Window unlocked. Arrays review scheduled for tomorrow.

### 2.4 Progress After Week 1

| Skill | BKT State | Mastery Level | Evidence |
|-------|-----------|---------------|----------|
| `dsa.arrays` | `independent` | 3 (Competent) | 8 distinct questions, 85% accuracy |
| `dsa.two_pointers` | `independent` | 2 (Practicing) | 5 distinct questions |
| `dsa.sliding_window` | `emerging` | 1 (Introduced) | 3 distinct questions, 67% accuracy |

### 2.5 Captain Byte Interactions

- Day 1: "You know arrays well. Let's see how two pointers build on that."
- Day 2: "Sliding window is two pointers specialized. You'll see the connection."

---

## 5. How the Three Profiles Differ

| Dimension | Profile 1 (Beginner) | Profile 2 (Intermediate) | Profile 3 (Advanced) |
|-----------|---------------------|-------------------------|---------------------|
| Starting skill | `coding.variables` | `dsa.arrays` | `dsa.two_pointers` |
| Skipped stages | None | Feel, Discover | Feel, Discover, Build |
| First action | `learn` variables | `learn` arrays | `diagnostic` two pointers |
| Time to arrays | 3 days | Day 1 | Day 1 |
| Hints used | High (scaffolding) | Low | Minimal |
| Orchestrator decisions | Build foundations | Skip to application | Diagnostic then application |
| SRS involvement | Day 4+ | Day 2 | Day 1 |

---

## 6. Orchestrator Decision Traces

### Profile 1 — Day 3 Decision

```
1. Student context: beginner, 45 min budget, target TCS
2. Learner state: arrays=unknown, loops=inconsistent, variables=independent
3. Prerequisite check: coding.loops not yet at level 3
4. Active misconceptions: none
5. Due SRS reviews: none
6. Candidate actions:
   - learn coding.loops (prerequisite not yet met for arrays)
   - learn dsa.arrays (prerequisite not met)
7. Selected: learn coding.loops
   Reason: "Loops prerequisite not yet at level 3. Continue building foundations."
   Confidence: high
```

### Profile 2 — Day 1 Decision

```
1. Student context: experienced, 60 min budget, target Infosys
2. Learner state: arrays=independent, loops=independent, variables=transfer_capable
3. Prerequisite check: coding.loops met (level 3+)
4. Active misconceptions: none
5. Due SRS reviews: none
6. Candidate actions:
   - learn dsa.arrays (prerequisites met, unassessed)
   - practice coding.loops (already independent)
   - learn dsa.two_pointers (prerequisite arrays not yet met)
7. Selected: learn dsa.arrays
   Reason: "Prerequisites met. Next unassessed skill in prerequisite order."
   Confidence: high
```

### Profile 3 — Day 1 Decision

```
1. Student context: experienced, 30 min budget, target Wipro
2. Learner state: arrays=independent (BKT 0.72), two_pointers=unknown
3. Prerequisite check: dsa.arrays met (level 3)
4. Active misconceptions: none
5. Due SRS reviews: none
6. Candidate actions:
   - diagnostic dsa.two_pointers (prerequisite met, unassessed)
   - learn dsa.sliding_window (prerequisite two_pointers not met)
   - practice dsa.arrays (already independent)
7. Selected: diagnostic dsa.two_pointers
   Reason: "Prerequisite met. Skill unassessed. Determine current level."
   Confidence: high
```

---

## 7. Evidence Flow (Profile 2 Example)

```
Day 1, 10:03 — Arrays: build (fill)
  Event: {skill_id: dsa.arrays, interaction_type: fill, correct: true,
          hints_used: 0, scaffolding_level: partial, server_graded: true}
  → BKT update: 0.72 → 0.76
  → Mastery: unique_questions=12, accuracy=88%, level=4 (Strong)

Day 1, 10:20 — Arrays: break (debug)
  Event: {skill_id: dsa.arrays, interaction_type: debug, correct: true,
          hints_used: 0, scaffolding_level: none, server_graded: true}
  → BKT update: 0.76 → 0.79
  → Mastery: unique_questions=13, accuracy=88%, level=4 (Strong)

Orchestrator: BKT 0.79 ≥ 0.65, no hints → state=independent
              Mastery level 4 → Strong
              Next action: transfer → container problem
```

---

## 8. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Three distinct starting states? | Yes |
| 3 | Different diagnostic paths? | Yes |
| 4 | Same content, different entry points? | Yes |
| 6 | Prerequisites respected? | Yes |
| 7 | Orchestrator decisions differ appropriately? | Yes |
| 8 | Evidence emitted at every step? | Yes |
| 9 | Captain Byte adapts to profile? | Yes |
| 10 | Time budgets respected? | Yes (45/60/30 min) |

---

**End of 07 Three Learner Journeys**
