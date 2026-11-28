# 02 LEARNER STATE MODEL

**BountyCode — Phase 2 Design Freeze**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the learner-state model for BountyCode. This document reconciles four
existing mastery models, defines five distinct concepts (context, evidence,
state estimate, mastery claim, placement readiness), and establishes how they
interact without becoming competing sources of truth.

This is a design document. No implementation is authorized.

---

## 2. Five Concepts (Mandatory Separation)

The system must explicitly distinguish five concepts. They are not equivalent
and must not be collapsed into one numeric score.

| Concept | Question Answered | Owner | Nature |
|---------|------------------|-------|--------|
| A. Learner Context | Goals, company, role, constraints | Profile / onboarding | Static-ish input |
| B. Raw Evidence | What actually happened (correctness, hints, scaffolding, task novelty) | Evidence events | Append-only record |
| C. Learner-State Estimate | System's evidence-based estimate of capability in a skill | Learner State Engine (BKT) | Probabilistic estimate |
| D. Mastery Claim | Whether learner satisfied approved proof policy for a capability | Mastery Engine (0–5) | Deterministic claim |
| E. Placement Readiness | How well verified skills match company blueprint | Readiness Engine | Go/no-go score |

**Rule**: These five concepts must not become competing sources of truth.
Each has a single owner and a defined contract with the others.

---

## 3. Concept A — Learner Context

### 3.1 Fields

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | UUID | Student identifier |
| `role` | string | e.g., `"sde"`, `"data-analyst"` |
| `target_company` | string | e.g., `"tcs"`, `"infosys"` |
| `target_blueprint_id` | string | Assessment blueprint identifier |
| `language` | string | Programming language preference |
| `time_budget_minutes` | number | Daily available time |
| `accessibility_preferences` | object | Reduced motion, screen reader, etc. |
| `experience_level` | string | `"absolute_beginner"` to `"experienced"` |

### 3.2 Entry Conditions

Set during onboarding. Updated only by explicit student action.

### 3.3 Usage

Used by Orchestrator to filter candidate actions, by Readiness Engine to
select blueprint, and by content system to select language-specific examples.

---

## 4. Concept B — Raw Evidence

### 4.1 Evidence Event Schema

| Field | Type | Constraints |
|-------|------|-------------|
| `event_id` | UUID | Unique, generated server-side |
| `user_id` | UUID | References user |
| `skill_id` | string | Canonical skill ID (`dsa.two_pointers`) |
| `lesson_id` | string | Lesson identifier |
| `interaction_type` | string | `select` / `manipulate` / `predict` / `trace` / `arrange` / `fill` / `debug` / `explain` / `transfer` |
| `first_committed_answer` | string | Student's first committed answer (before hints) |
| `hints_used` | integer | 0 or more |
| `scaffolding_level` | string | `"none"` / `"partial"` / `"full"` |
| `task_novelty` | string | `"guided"` / `"independent"` / `"transfer"` |
| `correct` | boolean | Server-graded only |
| `server_graded` | boolean | Must be `true` for evidence to count |
| `content_version` | string | Version of lesson/question content |
| `grading_version` | string | Version of grading logic |
| `time_spent_seconds` | number | Time on task |
| `created_at` | timestamp | Server time |

### 4.2 Evidence Rules

1. **Server-graded only**: Events where `server_graded !== true` are ignored
   for state estimation.
2. **First committed answer**: The answer before any hint is shown is the
   authoritative response for diagnosis.
3. **Duplicate prevention**: The same `question_id` + `user_id` combination
   counts once for distinct-question evidence. Repeated attempts increment
   `total_attempts` but not `distinct_questions`.
4. **Immutable**: Evidence events are append-only. Corrections create new
   events with `corrected_from` referencing the original.
5. **No client write**: Evidence events are written only by the server after
   grading.

---

## 5. Concept C — Learner-State Estimate

### 5.1 Owner

Learner State Engine (`app/services/learner_state_engine.py`) using Bayesian
Knowledge Tracing.

### 5.2 State Vocabulary

| State | Meaning | Evidence Requirement |
|-------|---------|---------------------|
| `unknown` | No evidence | < min_distinct_questions |
| `emerging` | Some evidence, below threshold | >= min_distinct_questions, BKT < 0.40 |
| `inconsistent` | Mixed correctness | BKT 0.40–0.65 |
| `independent` | Reliable correctness without hints | BKT >= 0.65, hints_used == 0 on recent items |
| `transfer_capable` | Can apply to changed context | BKT >= 0.80 + transfer task success |
| `needs_revision` | Previously independent, now decaying | SRS retrieval failure |

### 5.3 BKT Parameters (Versioned)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `p_l0` | 0.10 | Prior probability of knowing |
| `p_t` | 0.12 | Learning transition per observation |
| `p_g` | 0.20 | Guess probability |
| `p_s` | 0.10 | Slip probability |
| `version` | `"bkt-v1-initial"` | Policy version |

**Calibration note**: These are explicit starting assumptions, not empirically
calibrated BountyCode parameters. Must be evaluated against held-out delayed
outcomes before being shown to users as guaranteed facts.

### 5.4 Distinct-Question Rule

Only the first observation per distinct `question_id` updates BKT. This
prevents retries on the same item from masquerading as independent evidence.
Minimum 3 distinct questions required for a non-`unknown` state.

### 5.5 Uncertainty Representation

| Field | Type | Description |
|-------|------|-------------|
| `mastery_probability` | float 0–1 | BKT posterior |
| `confidence` | string | `"high"` / `"medium"` / `"low"` / `"insufficient_evidence"` |
| `distinct_questions` | integer | Count of distinct questions observed |
| `minimum_distinct_questions` | integer | Threshold for reliable estimate |
| `evidence_coverage` | float 0–1 | `distinct_questions / minimum_distinct_questions` |

### 5.6 Valid Transitions

```
unknown → emerging → inconsistent → independent → transfer_capable
         ↳ needs_revision (on SRS retrieval failure)
```

- `unknown` → `emerging`: After `minimum_distinct_questions` distinct questions.
- `emerging` → `inconsistent`: When BKT enters 0.40–0.65 band.
- `inconsistent` → `independent`: When BKT >= 0.65 AND no hints on recent items.
- `independent` → `transfer_capable`: When BKT >= 0.80 AND transfer task success.
- Any state → `needs_revision`: On SRS retrieval failure.

### 5.7 What the Student Sees

- State label (e.g., "Learning", "Independent")
- Progress bar based on `evidence_coverage`
- No raw BKT probability shown directly

---

## 6. Concept D — Mastery Claim

### 6.1 Owner

Mastery Engine (`app/services/mastery_engine.py`).

### 6.2 Scale

| Level | Name | Min Unique Questions | Min Accuracy |
|-------|------|---------------------|--------------|
| 0 | Unknown | 0 | 0.00 |
| 1 | Introduced | 1 | 0.00 |
| 2 | Practicing | 3 | 0.00 |
| 3 | Competent | 6 | 0.50 |
| 4 | Strong | 11 | 0.75 |
| 5 | Mastered | 20 | 0.90 |

### 6.3 Integrity Rules (Phase 6 in original doc)

1. Repeated attempts at ONE question do NOT create unlimited mastery evidence.
   Only unique validated question IDs count.
2. Unseen transfer questions contribute meaningful evidence (harder questions
   weight more; transfer questions count double).
3. Invalid or untrusted questions (trust_status not in `{verified, reviewed}`)
   do NOT contribute to mastery evidence.
4. Difficulty influences evidence: hard > medium > easy weighting.
5. Prerequisite skills must be respected: a skill cannot be Mastered (level 5)
   if its prerequisites are not at least Competent (level 3).
6. Repeated failures trigger targeted remediation flags.
7. Mastery is reproducible and explainable: every level change has an evidence
   trail (question_ids, difficulty weights, timestamps).

### 6.4 Difficulty Weights

| Difficulty | Weight |
|------------|--------|
| easy | 1.0 |
| medium | 1.5 |
| hard | 2.0 |

### 6.5 Trust Statuses That Contribute

`MASTERED_TRUST_STATUSES = {"verified", "reviewed"}`

### 6.6 Prerequisite Gating

If prerequisites not met and calculated level > 2 (Practicing), level is
capped at 2 and `prerequisite_gated` flag is set.

### 6.7 What Differs from Concept C

| Dimension | BKT (Concept C) | Mastery Engine (Concept D) |
|-----------|----------------|---------------------------|
| Scale | 0–1 probability | 0–5 integer level |
| Unit | Skill-level probability | Topic/sub_topic mastery |
| Evidence | Bayesian update per observation | Unique question count + accuracy |
| Prerequisite gating | No | Yes, caps at level 2 |
| Transfer weighting | Via `transfer_tasks` field | Transfer questions count double |
| Calibration | Explicitly uncalibrated | Deterministic rules |

### 6.8 Reconciliation Rule

Mastery Engine level 3 (Competent) is the minimum bar for a skill to be
considered "known" for placement purposes. BKT `independent` state is the
minimum bar for a skill to be considered ready for transfer tasks. These are
different thresholds serving different purposes and must not be conflated.

---

## 7. Concept E — Placement Readiness

### 7.1 Owner

Readiness Engine (`app/services/readiness_engine.py`).

### 7.2 Component Weights (must sum to 1.0)

| Component | Weight |
|-----------|--------|
| mastery | 0.30 |
| assessment | 0.25 |
| transfer | 0.20 |
| retention | 0.15 |
| consistency | 0.10 |

### 7.3 Thresholds

| Field | Value | Meaning |
|-------|-------|---------|
| `STRONG_SKILL` | 75.0 | Score >= this → "advance" action |
| `GAP_SKILL` | 50.0 | Score < this → "repair" action |
| `CRITICAL_SKILL_THRESHOLD` | 40.0 | Critical skill below this → "repair" |
| `MIN_COVERAGE_FOR_JUDGMENT` | 0.6 | Coverage below this → insufficient evidence |
| `READY_COVERAGE` | 0.8 | Coverage needed for readiness judgment |
| `READY_SCORE` | 70.0 | Overall score needed for "ready" |

### 7.4 Readiness Output

| Field | Type | Description |
|-------|------|-------------|
| `overall_readiness` | float 0–100 | Weighted skill score |
| `coverage` | float 0–1 | Evidence coverage across skills |
| `coverage_message` | string | Human-readable coverage status |
| `next_action` | object | Orchestrator recommendation |
| `target_weights` | object | Skill weight mapping |
| `skills` | array | Per-skill scored breakdown |

### 7.5 What Readiness Is NOT

- Not the next-action decision owner
- Not a learner-state estimate
- Not a mastery claim
- Not a teaching plan

---

## 8. State Transition Diagram

```
Concept C (Learner State Estimate)

     unknown
        │
        │ (>= min_distinct_questions)
        ▼
     emerging
        │
        │ (BKT 0.40-0.65)
        ▼
     inconsistent
        │
        │ (BKT >= 0.65, no hints recent)
        ▼
     independent
        │
        │ (BKT >= 0.80, transfer success)
        ▼
     transfer_capable
        ▲
        │
     needs_revision ◄── (SRS retrieval failure)
        ▲
        │
     (any state)
```

---

## 9. Reconciliation: Four Models

| Model | Measures | Best Used For | Never Used For |
|-------|----------|---------------|----------------|
| BKT (Concept C) | Probability of knowing skill | Real-time state during practice | Guaranteed mastery certification |
| Mastery Engine (Concept D) | Demonstrated problem-solving | Long-term skill certification | Real-time probability |
| Readiness (Concept E) | Company placement preparedness | Go/no-go for assessments | Daily lesson selection |
| Adaptive (7 levels) | Named proficiency display | UI display of proficiency | Deterministic decisions |

### 9.1 Conflict Resolution

If two models disagree (e.g., BKT says `independent` but Mastery Engine says
level 2), the Orchestrator uses the more conservative estimate for teaching
decisions and the more specific model for certification decisions:

- **Teaching next step**: Use the lower of BKT state and Mastery Engine level.
- **Placement decision**: Use Readiness Engine overall score.
- **Certification**: Use Mastery Engine level 3+ with prerequisites met.

### 9.2 No Arbitrary Conversion

There is no automatic formula converting BKT probability to Mastery Engine
level or vice versa. Each model is evaluated independently and the Orchestrator
makes decisions based on both outputs with explicit reasoning.

---

## 10. Persistence

All learner state is persisted to PostgreSQL via repositories in
`app/repositories/learning.py`. No in-memory-only state. No silent fallback.

Tables used:
- `learning_attempts` — raw evidence events
- `learning_evidence` — processed evidence
- `user_learning_progress` — per-user per-skill progress
- `skill_graphs` — skill state per user
- `gamification` — XP, level, streak (written only by `record_practice()`)

---

## 11. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Are five concepts explicitly separated? | Yes |
| 2 | Is uncertainty represented? | Yes (confidence, evidence_coverage) |
| 3 | Can system distinguish guided vs independent? | Yes (scaffolding_level, task_novelty) |
| 4 | Can it prove transfer? | Yes (task_novelty = "transfer") |
| 5 | Is duplicate-question inflation prevented? | Yes (distinct-question rule) |
| 6 | Are untrusted questions excluded? | Yes (trust_status filter) |
| 7 | Is prerequisite gating enforced? | Yes (Mastery Engine caps at level 2) |
| 8 | Is uncertainty shown to users as fact? | No (explicit calibration note) |
| 9 | Can new states be added? | Yes (state vocabulary is extensible) |
| 10 | Aligned with Vision Lock? | Yes |

---

**End of 02 Learner State Model**
