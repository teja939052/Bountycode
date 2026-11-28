# 01 LEARNING SYSTEM BLUEPRINT

**BountyCode — Phase 2 Design Freeze**
**Status: Design-only document**
**No application code written**
**No database changes**
**No migrations created**

---

## 1. Purpose

This document is the single architecture blueprint for BountyCode's learning system.
It describes how existing engines, repositories, and frontend components are wired
into one coherent student experience. Every engine keeps its declared responsibility.
One Learning Plan Orchestrator makes the final next-action decision.

This is a design document. No implementation is authorized.

---

## 2. Guiding Principles

| Principle | Meaning |
|-----------|---------|
| Student action first | Every learning step requires a meaningful student action that can be checked. |
| Evidence-backed states | No arbitrary promotion to mastery. States require verified evidence. |
| One decision owner | Exactly one next-action decision owner (Learning Plan Orchestrator). |
| Algorithmic correctness | The visual execution trace, grading, and reference algorithm must agree. |
| No duplicate engines | Reuse existing BKT, Mastery Engine, Readiness, Prerequisite Graph, SRS, Repair, Adaptive Action Planner. |
| Content trust | Only verified, servable content is exposed in graded flows. |
| No client-side rewards | XP/coins/stars/streak are written only by `record_practice()` on the server. |
| Extensible, not generic | New engines and states can be added without a plugin platform or microservices. |

---

## 3. High-Level Architecture

### 3.1 Logical Layering

```
┌─────────────────────────────────────────────┐
│   Student Experience (Frontend)             │
│   LessonPlayer, PracticeConsole, CodeTracer │
│   Captain Byte tutor, PatternPage           │
└─────────────────────────────────────────────┘
                            │ API / contracts
┌─────────────────────────────────────────────┐
│   Learning Plan Orchestrator                │
│   (final next-action decision owner)        │
└─────────────────────────────────────────────┘
                            │
    ┌───────────────────────┼───────────────────────┐
    ▼                       ▼                       ▼
┌──────────┐        ┌──────────┐          ┌──────────┐
│ Readiness│        │ SRS      │          │ Repair   │
│ placement│        │ retrieval│          │ misconcep│
│ readiness│        │          │          │ recovery │
└──────────┘        └──────────┘          └──────────┘
    ▼                       ▼                       ▼
┌──────────┐        ┌──────────┐          ┌──────────┐
│ Prereq   │        │ BKT      │          │ Adaptive │
│ Graph    │        │ state    │          │ ranker   │
│ planning │        │ learner  │          │          │
└──────────┘        └──────────┘          └──────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
┌─────────────────────────────────────────────┐
│   Content & Evidence Layer                  │
│   Question Store, Content Loader,           │
│   Lesson Repositories, Evidence Events      │
│   (file-backed content, server-authoritative)│
└─────────────────────────────────────────────┘
```

### 3.2 Engine Contract

Every specialized learning engine declares:

| Field | Meaning |
|-------|---------|
| `engine_id` | Stable identifier (e.g., `readiness_evaluator_v1`) |
| `engine_version` | Implementation version |
| `policy_version` | Policy/ruleset version |
| `input_contract` | Validated input schema |
| `output_contract` | Structured output schema |
| `decision_trace` | Human-readable explanation of decisions |
| `confidence` | high / medium / low / insufficient_evidence |
| `side_effect_boundary` | Which domains this engine may write |
| `failure_behavior` | What happens on invalid or insufficient input |
| `test_strategy` | Unit, property, replay tests |

### 3.3 Existing Engines Reused (Conceptual Mapping)

| Existing Engine | File | Responsibility in Design |
|-----------------|------|--------------------------|
| Prerequisite Graph | `app/services/prerequisite_graph.py` | DAG validation, prerequisite planning |
| BKT / Learner State | `app/services/learner_state_engine.py` | Skill mastery probability estimation |
| Mastery Engine | `app/services/mastery_engine.py` | 0–5 mastery tracking, evidence trail |
| Readiness Engine | `app/services/readiness_engine.py` | Placement readiness scoring |
| Adaptive Action Planner | `app/services/adaptive_action_planner.py` | Candidate ranking (EV/minute) |
| Spaced Repetition | `app/services/spaced_repetition.py` | SM-2 retrieval scheduling |
| Repair Service | `app/services/repair_service.py` | Misconception recovery missions |
| Curriculum Quality | `app/services/curriculum_quality.py` | Content authoring gate (0–100 score) |
| Skill Taxonomy | `app/services/skill_taxonomy.py` | Canonical skill ID mapping |

### 3.4 Content Flow (Residency Rule)

Content never lives in MongoDB. Question content lives in versioned files under
`backend/app/data/` and `backend/app/content/`, loaded into memory at startup by
`question_store` / `content_loader`.

### 3.5 Repository Layer

PostgreSQL repositories exist under `backend/app/repositories/learning.py`.
No new collections. All student state is persisted to PostgreSQL. No silent
fallback to in-memory or MongoDB.

---

## 4. Learning Loop Design

### 4.1 The Seven-Beat Framework

| Beat | Student Action | Existing Stage Mapping |
|------|---------------|------------------------|
| Feel | Attempt a meaningful problem before full explanation | `explain` / challenge prompt |
| Discover | Interact with concept and work out central idea | `see` / `interact` |
| Predict | Commit to an answer before seeing result | `predict` |
| Build | Gradually faded support from examples to independent work | `solve` |
| Break | Test counterexamples and boundary cases | `break` / `debug` |
| Transfer | Apply to a meaningfully changed problem | `transfer` |
| Return | Retrieve knowledge later (SRS) | `recall` / SRS review |

### 4.2 Interaction Contract

Every interactive step type declares:

| Field | Meaning |
|-------|---------|
| `interaction_type` | select / manipulate / predict / trace / arrange / fill / debug / explain / transfer |
| `input_schema` | What the student provides |
| `expected_response` | Canonical correct answer / rule |
| `validation_strategy` | How correctness is determined |
| `feedback_contract` | What feedback is returned |
| `hint_levels` | Progressive hint sequence |
| `accessibility_behavior` | Keyboard / screen-reader / reduced-motion behavior |
| `evidence_emitted` | What learning event is recorded |

No decorative interaction counts as learning evidence.
No Next button grants mastery or bypasses required checks.

---

## 5. User-Facing Flows

### 5.1 Landing and Diagnosis

Student lands → company/role selection → diagnostic assessment → learner context
established → first learning journey step.

### 5.2 Today's Plan

One coherent plan with three views:

| View | Meaning |
|------|---------|
| Learning Journey | Long-term target (company → blueprint → skill → lesson) |
| Today's Plan | Time-bounded sequence (today's available activities) |
| Next Learning Step | One immediate action |

All three are views of one coherent plan generated by the Orchestrator.

### 5.3 Lesson Flow

1. Student opens lesson
2. Server serves verified, servable lesson content
3. Student interacts (every step validated server-side)
4. Evidence events recorded to PostgreSQL
5. Orchestrator computes next action
6. Lesson completes → mastery claim evaluated → next lesson recommended

### 5.4 Repair Flow

Misconception detected → repair mission → guided practice → independent retest
→ updated learner state → orchestrator recomputes next action.

### 5.5 Retrieval Flow

SRS identifies due reviews → student reviews → evidence recorded → mastery
probability updated → orchestrator recomputes next action.

---

## 6. Data Contracts (Conceptual)

### 6.1 Evidence Event

```json
{
  "event_id": "uuid",
  "user_id": "uuid",
  "skill_id": "dsa.two_pointers",
  "lesson_id": "world_1.lesson_3",
  "interaction_type": "predict",
  "first_committed_answer": "move right pointer",
  "hints_used": 1,
  "scaffolding_level": "partial",
  "task_novelty": "independent",
  "correct": true,
  "server_graded": true,
  "content_version": "lesson_v2",
  "grading_version": "grader_v1",
  "created_at": "2026-11-28T03:15:00Z"
}
```

### 6.2 Learner State Estimate

```json
{
  "skill_id": "dsa.two_pointers",
  "state": "inconsistent",
  "confidence": 0.65,
  "evidence_sufficient": false,
  "bkt_mastery_probability": 0.42,
  "mastery_level_0_5": 2,
  "distinct_questions": 2,
  "min_distinct_questions": 3,
  "parameter_version": "bkt-v1-initial"
}
```

### 6.3 Next-Action Decision

```json
{
  "orchestrator_version": "orchestrator-v1",
  "decision_trace": [
    "active misconception repair found for dsa.two_pointers",
    "no due SRS reviews",
    "prerequisite dsa.arrays met",
    "selected repair action: teach_and_reassess"
  ],
  "next_action": {
    "kind": "repair",
    "skill_id": "dsa.two_pointers",
    "lesson_id": "world_1.lesson_3",
    "estimated_minutes": 15,
    "content_version": "lesson_v2"
  },
  "alternatives": []
}
```

---

## 7. Constraints

- **No LLM decides grading, mastery, content trust, readiness, or next action.**
- **AI may paraphrase approved educational content but must be optional.**
- **Captain Byte does not grade, select activity, write mastery, write readiness, award XP, or unlock progression without verified outcomes.**
- **Readiness measures placement preparedness only. Orchestrator chooses next activity.**
- **New engines and states can be added without a plugin platform or microservice architecture.**
- **One complete lesson must work end-to-end before scaling.**

---

## 8. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Are we creating duplicate engines? | No |
| 2 | Is there one next-action decision owner? | Yes (Orchestrator) |
| 3 | Are learner states evidence-backed? | Yes |
| 4 | Is uncertainty represented? | Yes (confidence fields) |
| 5 | Can the system distinguish practice from independence? | Yes (scaffolding_level field) |
| 6 | Can it prove transfer? | Yes (transfer interaction type) |
| 7 | Is SRS truly connected? | Yes (via Orchestrator) |
| 8 | Are all algorithms independently verifiable? | Yes (pure functions) |
| 9 | Does every interaction require meaningful learner action? | Yes |
| 10 | Can the same lesson model support aptitude and coding? | Yes |
| 11 | Can Captain Byte function without AI? | Yes (authored fallback) |
| 12 | Can future skills/states be added without restructuring? | Yes |
| 13 | Is the architecture maintainable? | Yes |
| 14 | Aligned with current Vision Lock? | Yes |
| 15 | Can real students understand the experience? | To be validated in pilot |

---

## 9. Phase 2 Decision Record

| Decision | Rationale |
|----------|-----------|
| Readiness Engine is placement readiness only, not next-action owner | Separates concerns; readiness answers "ready?", orchestrator answers "do what?" |
| Orchestrator is logical responsibility, not new physical service | Avoids new engine overhead |
| Four mastery models kept separate with defined boundaries | Prevents destroying existing working code; reconciliation via evidence contract |
| Content remains file-backed, never MongoDB | Complies with Question Bank Residency Rule |
| Seven-beat framework is flexible by skill/content | Matches instructional philosophy |
| Interaction contract is first-class | Ensures student action at every step |

---

**End of 01 Learning System Blueprint**
