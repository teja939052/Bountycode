# 04_ENGINE_DEPENDENCY_GRAPH.md — Engine Dependencies

> Every engine, its dependencies, data inputs, outputs, and ownership. No circular imports. No domain engine imports FastAPI routes or frontend data.

---

## Dependency Direction

```
Routes (FastAPI)
      ↓
Application Use Cases
      ↓
Domain Engines (deterministic, pure)
      ↓
Repository Interfaces
      ↑
Infrastructure Adapters (MongoDB, Redis, OpenRouter, Piston)
```

**Forbidden**:
- Mastery engine importing FastAPI routes
- Readiness importing frontend data
- Quiz service writing XP directly
- AI responses writing mastery
- Frontend deciding question trust
- Multiple services updating the same reward balance
- Duplicate question loaders
- Circular imports between domain engines
- Each route implementing its own learning lifecycle

---

## Engine Inventory

| Engine | File | Inputs | Outputs | Owns | Dependencies |
|--------|------|--------|---------|------|--------------|
| Question Store | `services/question_store.py` | Versioned JSON files | Servable question pool | Question loading, trust gating | Config (settings) |
| Quiz Composer | `services/quiz_service.py` | Question pool, learner state, blueprint | Quiz session | Quiz construction | question_store |
| Skill Taxonomy | `services/skill_taxonomy.py` | Raw skill names | Canonical `domain.subskill` IDs | Skill identity | None (pure) |
| Skill Assessment | `services/skill_assessment.py` | Attempts, correctness, difficulty | Mastery scores | Mastery calculation | skill_taxonomy |
| Curriculum Registry | `content/curriculum/registry.py` | Lesson slug | Lesson content dict | Lesson lookup | worlds_data, registry |
| Company Blueprint | `data/company_blueprints.json` | Company, role | Section weights, skill weights | Blueprint overlay | None (static JSON) |
| Deterministic Grader | `routes/worlds.py`, `routes/oa.py` | Student code, test cases | Pass/fail, score | Code/answer grading | code_executor (optional) |
| Code Executor | `services/code_executor.py` | Code, language, test cases | Execution result | Code execution | Piston → Docker → Local |
| Mastery Engine | `services/skill_assessment.py` | Attempts, first-attempt, recency | Mastery level (0-1) | Mastery authority | skill_assessment |
| SRS Engine | `services/spaced_repetition.py` | Attempt history, ease, interval | Next review date | SRS scheduling | None (pure) |
| Repair Service | `services/repair_service.py` | Weak skills, failure class | Repair mission, retest | Mistake diagnosis + repair | skill_assessment, question_store |
| Readiness Engine | `services/readiness_engine.py` | Evidence, blueprint, trust weights | Readiness score (0-100), blockers | Readiness calculation | skill_assessment, question_store |
| Gamification | `services/gamification.py` | Activity, score (0-10) | XP, coins, streaks, badges | Reward authority (single writer) | gamification_core |
| Daily Hunt | `services/path_generator.py` | Learner context, blueprint, mastery | Personalized plan | Next-action recommendation | skill_assessment, question_store |
| Evidence Aggregator | `services/observability.py` | Learning events | Funnel stats, algorithm health | Observability | telemetry_events |
| AI Gateway | `services/ai_gateway.py` | Task, messages, schema | Structured AI response | AI access (assist only) | ai_core.chat_completion |
| Core AI | `services/ai_core.py` | Messages, model | Completion text | AI infrastructure | OpenRouter (HTTP) |
| Dashboard Read Model | `routes/personal_dashboard.py` | User ID | Aggregated dashboard data | Dashboard projections | gamification, skill_graph, readiness |

---

## Engine Call Graph

```
STARTUP
  └── question_store.load_all()          [loads questions into memory]
  └── router_registry.collect_all_routers() [validates all routes]

LEARNER JOURNEY
  │
  ├── Onboarding → CompleteOnboarding
  │     └── academy_learner_profiles (write)
  │
  ├── Diagnostic → RunDiagnostic
  │     ├── question_store._servable_questions()  [trust gate]
  │     ├── quiz_service.build_quiz()             [compose session]
  │     └── academy_diagnostic_sessions (write)
  │
  ├── Plan → BuildDailyHunt (path_generator)
  │     ├── skill_assessment.get_skill_graph()    [mastery state]
  │     ├── readiness_engine.compute_readiness()  [readiness score]
  │     └── company_blueprints.json               [skill weights]
  │
  ├── Lesson → GetLesson / CompleteLesson
  │     ├── curriculum.registry.get_lesson_dict() [lesson content]
  │     ├── worlds_data.py                        [world levels]
  │     ├── skill_assessment.update_skill_score() [mastery update]
  │     └── gamification.record_practice()        [XP reward - SINGLE WRITER]
  │
  ├── Practice → CreateQuizSession / SubmitQuizAttempt
  │     ├── question_store._servable_questions()  [trust gate]
  │     ├── quiz_service.build_quiz()             [compose session]
  │     ├── deterministic grader                  [pass/fail]
  │     └── question_answers_collection (write)   [attempt history]
  │
  ├── Mock OA → StartMockAssessment / FinalizeMock
  │     ├── company_blueprints.json               [section weights]
  │     ├── quiz_service.build_quiz()             [compose session]
  │     ├── server timer (started_at/ends_at)     [authoritative timing]
  │     └── readiness_engine.compute_readiness()  [post-mock update]
  │
  ├── Repair → CreateRepairMission / CompleteRepairMission
  │     ├── repair_service.create_repair_mission() [diagnosis]
  │     ├── question_store._servable_questions()  [retest questions]
  │     └── skill_assessment.update_skill_score() [mastery re-eval]
  │
  └── SRS → RecordSRSReview
        └── spaced_repetition.SM2()               [next review date]
          └── srs_cards_collection (write)

READINESS
  │
  └── CalculateReadiness
        ├── skill_assessment.get_skill_graph()    [evidence]
        ├── readiness_engine.calculate_target_readiness()
        ├── company_blueprints.json               [required skills]
        └── question_store trust states           [evidence filtering]

GAMIFICATION
  │
  └── record_practice()                           [single XP writer]
        ├── gamification_core.py                  [pure math: level, titles]
        ├── gamification_events_collection (write) [immutable ledger]
        └── gamification_collection (write)       [XP, level, streak]
```

---

## Trust Boundaries

| Engine | Can Write XP/Rewards? | Can Write Question Content? | Can Modify Mastery? |
|--------|----------------------|----------------------------|---------------------|
| Question Store | No | No (read-only from files) | No |
| Quiz Composer | No | No | No |
| Skill Assessment | No | No | Yes (via gamification) |
| Curriculum Registry | No | No | No |
| Company Blueprint | No | No | No |
| Deterministic Grader | No | No | No |
| Code Executor | No | No | No |
| Mastery Engine | No | No | Yes (via gamification) |
| SRS Engine | No | No | No |
| Repair Service | No | No | Yes (via gamification) |
| Readiness Engine | No | No | No |
| Gamification | YES (only via record_practice) | No | No |
| Daily Hunt | No | No | No |
| Evidence Aggregator | No | No | No |
| AI Gateway | No | No | No |
| Core AI | No | No | No |
| Dashboard Read Model | No | No | No |

---

## Architecture Tests (To Be Implemented)

```
TEST: question_store_is_canonical_owner
  → FAILS if quiz_service.py calls glob() for question files
  → FAILS if quiz_service.py recursively scans question directories
  → FAILS if quiz_service.py duplicates trust filtering
  → FAILS if quiz_service.py silently falls back to unrelated questions

TEST: quiz_determinism
  → FAILS if same learner state + seed produces different quiz

TEST: gamification_single_writer
  → FAILS if direct $inc/$set on XP fields outside record_practice()
  → FAILS if reward created without gamification_events row
  → FAILS if profile.xp != sum(ledger)

TEST: ai_no_frontend_access
  → FAILS if frontend imports OpenRouter SDK directly

TEST: no_circular_imports
  → FAILS if domain engine imports route module

TEST: question_trust_gate
  → FAILS if unverified/quarantined question passes _is_servable()
```
