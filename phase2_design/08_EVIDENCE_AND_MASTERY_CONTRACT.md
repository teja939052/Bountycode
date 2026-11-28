# 08 EVIDENCE AND MASTERY CONTRACT

**BountyCode — Phase 2 Design Freeze**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the evidence contract for BountyCode's learning system. This document
specifies what counts as evidence, how evidence becomes state, how mastery is
claimed, and how misconceptions are detected. Every claim about a learner's
capability must be traceable to specific evidence events.

This is a design document. No implementation is authorized.

---

## 2. Evidence Event Contract

### 2.1 Schema

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `event_id` | UUID | Required, server-generated | Unique event identifier |
| `user_id` | UUID | Required | Student identifier |
| `skill_id` | string | Required | Canonical skill ID (`dsa.two_pointers`) |
| `lesson_id` | string | Required | Lesson identifier |
| `interaction_type` | string | Required | `select` / `manipulate` / `predict` / `trace` / `arrange` / `fill` / `debug` / `explain` / `transfer` |
| `first_committed_answer` | string | Required | Student's answer before any hint |
| `hints_used` | integer | Required, ≥ 0 | Number of hints requested |
| `scaffolding_level` | string | Required | `"none"` / `"partial"` / `"full"` |
| `task_novelty` | string | Required | `"guided"` / `"independent"` / `"transfer"` |
| `correct` | boolean | Required | Server-graded only |
| `server_graded` | boolean | Required, must be `true` | Set only by trusted backend code |
| `content_version` | string | Required | Version of lesson/question content |
| `grading_version` | string | Required | Version of grading logic |
| `time_spent_seconds` | number | Required, ≥ 0 | Time on task |
| `created_at` | timestamp | Required | Server timestamp |

### 2.2 Evidence Rules (Binding)

| Rule | Description |
|------|-------------|
| R1 | **Server-graded only**: Events where `server_graded !== true` are ignored for state estimation. |
| R2 | **First committed answer**: The answer before any hint is shown is the authoritative response for diagnosis. |
| R3 | **Duplicate prevention**: The same `question_id` + `user_id` counts once for `distinct_questions`. Repeated attempts increment `total_attempts` but not `distinct_questions`. |
| R4 | **Immutable**: Evidence events are append-only. Corrections create new events with `corrected_from` referencing the original. |
| R5 | **No client write**: Evidence events are written only by the server after grading. |
| R6 | **Trust required**: Questions with `trust_status` not in `{verified, reviewed}` do not contribute to mastery evidence (they increment `total_attempts` only). |
| R7 | **Version recorded**: Both `content_version` and `grading_version` must be recorded for reproducibility. |

### 2.3 What Counts as Evidence vs. What Doesn't

| Counts as Evidence | Does NOT Count |
|-------------------|----------------|
| Server-graded correct answer | Client self-reported "I solved it" |
| First committed answer (no hints) | Answer changed after seeing hint |
| Independent task completion | Guided task with full scaffolding |
| Transfer task success | Same-context repetition |
| SRS retrieval after delay | Immediate repetition |
| Unique question ID | Same question retried |
| Verified/reviewed trust status | Unverified/quarantined content |

---

## 3. Learner-State Estimate (Concept C)

### 3.1 State Vocabulary

| State | Meaning | BKT Probability | Evidence Required |
|-------|---------|-----------------|-------------------|
| `unknown` | No evidence | < 0.40 | < min_distinct_questions |
| `emerging` | Some evidence, weak | 0.10–0.40 | ≥ 3 distinct questions |
| `inconsistent` | Mixed correctness | 0.40–0.65 | ≥ 3 distinct questions |
| `independent` | Reliable without hints | 0.65–0.80 | ≥ 3 distinct questions, hints_used=0 on recent |
| `transfer_capable` | Applies to changed context | 0.80–1.00 | ≥ 3 distinct questions + transfer success |
| `needs_revision` | Previously known, decaying | Any | SRS retrieval failure |

### 3.2 BKT Parameters (Versioned)

| Parameter | Value | Range | Description |
|-----------|-------|-------|-------------|
| `p_l0` | 0.10 | [0, 1] | Prior probability of knowing |
| `p_t` | 0.12 | [0, 1] | Learning transition per observation |
| `p_g` | 0.20 | [0, 1] | Guess probability |
| `p_s` | 0.10 | [0, 1] | Slip probability |
| `version` | `"bkt-v1-initial"` | Non-empty string | Policy version |

**Calibration rule**: These are explicit starting assumptions. They must be
evaluated against held-out student outcomes before `mastery_probability` is
shown to users as a guaranteed fact.

### 3.3 Distinct-Question Rule

| Aspect | Rule |
|--------|------|
| What counts | First observation per distinct `question_id` |
| What doesn't count | Retries on same question, same answer repeated |
| Minimum | 3 distinct questions for non-`unknown` state |
| Tracking | `seen_questions` set per skill |

### 3.4 Uncertainty Representation

| Field | Type | Meaning |
|-------|------|---------|
| `mastery_probability` | float 0–1 | BKT posterior after last observation |
| `confidence` | string | `"high"` / `"medium"` / `"low"` / `"insufficient_evidence"` |
| `distinct_questions` | integer | Count of distinct questions observed |
| `minimum_distinct_questions` | integer | Threshold (3) |
| `evidence_coverage` | float 0–1 | `min(1.0, distinct_questions / 3)` |

### 3.5 State Transitions

| From → To | Condition |
|-----------|-----------|
| `unknown` → `emerging` | ≥ 3 distinct questions |
| `emerging` → `inconsistent` | BKT enters 0.40–0.65 band |
| `inconsistent` → `independent` | BKT ≥ 0.65 AND hints_used = 0 on last 3 items |
| `independent` → `transfer_capable` | BKT ≥ 0.80 AND transfer task success |
| Any → `needs_revision` | SRS retrieval failure |

---

## 4. Mastery Claim (Concept D)

### 4.1 Scale

| Level | Name | Min Unique Questions | Min Accuracy | Prerequisite |
|-------|------|---------------------|--------------|--------------|
| 0 | Unknown | 0 | 0.00 | None |
| 1 | Introduced | 1 | 0.00 | None |
| 2 | Practicing | 3 | 0.00 | None |
| 3 | Competent | 6 | 0.50 | Prerequisites met |
| 4 | Strong | 11 | 0.75 | Prerequisites met |
| 5 | Mastered | 20 | 0.90 | Prerequisites met |

### 4.2 Difficulty Weights

| Difficulty | Weight | Transfer Multiplier |
|------------|--------|---------------------|
| easy | 1.0 | 1.0 |
| medium | 1.5 | 2.0 |
| hard | 2.0 | 2.0 |

### 4.3 Trust Statuses That Count as Evidence

`MASTERED_TRUST_STATUSES = {"verified", "reviewed"}`

Questions with any other trust status increment `total_attempts` but do NOT
count as unique evidence.

### 4.4 Integrity Rules

| Rule | Description |
|------|-------------|
| M1 | Unique question IDs only — repeated attempts at same question don't inflate mastery |
| M2 | Transfer questions count double for weighted evidence |
| M3 | Untrusted questions don't contribute to unique evidence |
| M4 | Prerequisite gating: level capped at 2 if prerequisites not met |
| M5 | Repeated failures (≥2 failures on same question) trigger remediation flag |
| M6 | <50% accuracy on 3+ unique questions triggers remediation flag |
| M7 | Every level change has an evidence trail (question_ids, weights, timestamps) |

### 4.5 What Differs from BKT

| Dimension | BKT (State Estimate) | Mastery Engine (Mastery Claim) |
|-----------|---------------------|-------------------------------|
| Scale | 0–1 probability | 0–5 integer level |
| Purpose | Real-time state during practice | Long-term skill certification |
| Update rule | Bayesian per observation | Unique question count + accuracy |
| Prerequisite gating | No | Yes (cap at level 2) |
| Transfer weighting | Via `transfer_tasks` field | Transfer questions count double |
| Trust filter | Server-graded only | `{verified, reviewed}` only |

---

## 6. Placement Readiness (Concept E)

### 6.1 Component Weights (Sum = 1.0)

| Component | Weight |
|-----------|--------|
| mastery | 0.30 |
| assessment | 0.25 |
| transfer | 0.20 |
| retention | 0.15 |
| consistency | 0.10 |

### 6.2 Thresholds

| Field | Value | Meaning |
|-------|-------|---------|
| `STRONG_SKILL` | 75.0 | ≥ this → "advance" |
| `GAP_SKILL` | 50.0 | < this → "repair" |
| `CRITICAL_SKILL_THRESHOLD` | 40.0 | Critical skill < this → "repair" |
| `MIN_COVERAGE_FOR_JUDGMENT` | 0.6 | Coverage < this → insufficient evidence |
| `READY_COVERAGE` | 0.8 | Coverage needed for readiness judgment |
| `READY_SCORE` | 70.0 | Overall score needed for "ready" |

### 6.3 Readiness Output Schema

```json
{
  "overall_readiness": 78.5,
  "coverage": 0.85,
  "coverage_message": "Sufficient evidence: 85.0% coverage",
  "next_action": { ... },
  "target_weights": {"dsa.arrays": 0.35, "coding.loops": 0.25, ...},
  "skills": [
    {"skill_id": "dsa.arrays", "score": 82.0, "weight": 0.35, "critical": true}
  ]
}
```

---

## 7. Misconception Contract

### 7.1 Definition

A misconception is a **confirmed or sufficiently supported systematic error**
in a student's understanding. A wrong answer is NOT automatically a
misconception.

### 7.2 Misconception Taxonomy

| ID | Description | Triggering Evidence | Disconfirming Evidence |
|----|-------------|---------------------|------------------------|
| `ZERO_BASED_INDEX_CONFUSION` | Thinks arrays start at index 1 | Accesses `arr[1]` as first element | Correctly accesses `arr[0]` |
| `LOOP_BOUNDARY_OFF_BY_ONE` | Loop boundary error | `i <= len(arr)` instead of `i < len(arr)` | Correctly uses `i < len(arr)` |
| `POINTER_MOVEMENT_REVERSED` | Moves wrong pointer | Moves right when should move left | Correctly moves left when sum < target |
| `PERCENTAGE_POINTS_VS_PERCENT_CHANGE` | Confuses percentage points with percent change | Treats 5% → 7% as 2% change | Correctly identifies 40% relative change |
| `BASELINE_PERCENTAGE_CONFUSION` | Uses wrong baseline for percentage | Calculates percentage of new value instead of original | Uses original value as baseline |

### 7.3 Diagnosis Pipeline

```
Wrong Answer → Error Category → Diagnosis Candidate → Confidence Check → Confirmed Misconception → Repair → Independent Retest → Updated State
```

### 7.4 Confidence Requirements

| Confidence Level | Required Evidence |
|------------------|-------------------|
| `low` | Single wrong answer on one question type |
| `medium` | Same error on 2+ distinct questions |
| `high` | Same error on 3+ distinct questions + pattern match |
| `confirmed` | Independent retest after repair shows correct without hints |

### 7.5 Repair Contract

| Field | Type | Description |
|-------|------|-------------|
| `misconception_id` | string | Which misconception |
| `defective_code` | string | Code with the misconception (for coding) |
| `fix_prompt` | string | What student must fix |
| `test_cases` | array | Cases that expose the defect |
| `explanation` | string | Why the defect is wrong |

### 7.6 Independent Retest

After repair, student must solve a **different** question testing the same
concept without hints to confirm the misconception is resolved.

---

## 8. Reconciliation: Four Models

| Model | Measures | Scale | Best Used For | Never Used For |
|-------|----------|-------|---------------|----------------|
| BKT (Concept C) | Probability of knowing skill | 0–1 | Real-time state during practice | Guaranteed mastery certification |
| Mastery Engine (Concept D) | Demonstrated problem-solving | 0–5 level | Long-term skill certification | Real-time probability |
| Readiness (Concept E) | Placement preparedness | 0–100 score | Go/no-go for company assessments | Daily lesson selection |
| Adaptive (7 levels) | Named proficiency | named | UI display of proficiency | Deterministic decisions |

### 8.1 Conflict Resolution

| Situation | Resolution |
|-----------|------------|
| BKT says `independent`, Mastery says level 2 | Use BKT for teaching next step, Mastery for certification |
| Readiness says 70%, Mastery says level 5 | Readiness for placement, Mastery for skill claim |
| SRS says due review, Mastery says level 5 | SRS review still required (retention decay) |

### 8.2 No Automatic Conversion

There is **no formula** converting BKT probability to Mastery Engine level or
vice versa. Each model is evaluated independently. The Orchestrator makes
decisions based on both outputs with explicit reasoning in the decision trace.

---

## 9. Idempotency and Deduplication

### 9.1 Duplicate Event Prevention

| Aspect | Implementation |
|--------|---------------|
| Same question + same user | Counts once for `distinct_questions` |
| Same answer repeated | Increments `total_attempts` only |
| Same evidence event submitted twice | Rejected by `event_id` uniqueness |
| Network retry | Client sends same `event_id`; server deduplicates |

### 9.2 Idempotency Key

```
event_id = uuid4()  # Generated server-side
```

Clients must not generate `event_id`. Server rejects events with duplicate
`event_id` for the same `user_id`.

---

## 10. Persistence

| Table | Purpose | Written By |
|-------|---------|------------|
| `learning_attempts` | Raw evidence events | Server after grading |
| `learning_evidence` | Processed evidence | Learner State Engine |
| `user_learning_progress` | Per-user per-skill progress | Mastery Engine |
| `skill_graphs` | Skill state per user | Prerequisite Graph |
| `gamification` | XP, level, streak | `record_practice()` only |

### 10.1 No Silent Fallback

If PostgreSQL is unavailable, the system returns an error. No in-memory or
MongoDB fallback.

---

## 11. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Five concepts explicitly separated? | Yes |
| 2 | Evidence schema defined? | Yes |
| 3 | Server-graded only enforced? | Yes |
| 4 | Duplicate prevention defined? | Yes |
| 5 | Trust filter for mastery defined? | Yes |
| 6 | Prerequisite gating defined? | Yes |
| 7 | Four models reconciled? | Yes |
| 8 | Misconception taxonomy defined? | Yes |
| 9 | Diagnosis pipeline defined? | Yes |
| 10 | Independent retest required? | Yes |
| 11 | Persistence layer defined? | Yes |
| 12 | No silent fallback? | Yes |

---

**End of 08 Evidence and Mastery Contract**
