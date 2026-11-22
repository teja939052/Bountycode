# 02_TARGET_ARCHITECTURE.md — BountyCode Target Architecture

> **Source of Truth**: `docs/BOUNTYCODE_VISION_LOCK.md`, `docs/PRD_SERVICE_BASED_V1.md`, `docs/AGENTS.md`
> **ADRs**: `docs/architecture/adrs/ADR-001` through `ADR-004`
> **Current State**: `docs/architecture/01_CURRENT_STATE.md`

---

## System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEARNER (Browser / PWA)                      │
│  React 18 + TypeScript + Vite + React Router + TanStack Query   │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTPS / JWT httpOnly cookie
                      v
┌─────────────────────────────────────────────────────────────────┐
│                 BOUNTYCODE API (FastAPI)                        │
│  Auth → Rate Limit → Duplicate Guard → Route → Use Case → Engine│
└─────────────────────┬───────────────────────────────────────────┘
                      │
          ┌───────────┼───────────┬───────────┐
                      v           v           v
              ┌─────────────┐ ┌──────────┐ ┌─────────────┐
              │  MongoDB    │ │  Redis   │ │  OpenRouter │
              │ (Motor)     │ │ (Cache)  │ │  (AI)       │
              │             │ │          │ │             │
              │ Learner     │ │ AI cache │ │ Gemini 2.0  │
              │ state only  │ │ (1hr TTL)│ │ Fallbacks   │
              │ No question │ │          │ │ Circuit     │
              │ content     │ │          │ │ Breaker     │
              └─────────────┘ └──────────┘ └─────────────┘
                      │
                      v
              ┌─────────────┐
              │  Piston API │
              │  (Code exec)│
              │  Fallbacks: │
              │  Docker/Local│
              └─────────────┘
```

---

## Container Diagram

| Container | Technology | Responsibility |
|-----------|-----------|---------------|
| Frontend | React 18, Vite, TypeScript | UI, routing, client state (Zustand) |
| API | FastAPI, Pydantic | Route handling, validation, auth |
| AI Gateway | Python, httpx | Centralized AI access, privacy, cost tracking |
| Question Store | Python, JSON files | Canonical question loading, trust gating |
| Database | MongoDB (Motor) | Learner state only (attempts, results, SRS, etc.) |
| Cache | Redis → in-memory | AI response cache (1hr TTL), session cache |
| Code Execution | Piston API → Docker → Local | Deterministic code judging |

---

## Component Diagram

### Layer A — Presentation (Frontend)

```
Six Primary Hubs:
├── /dashboard       → Daily starting point (today's hunt)
├── /journey         → World/map navigation, lessons
├── /practice        → Question bank, coding, DSA
├── /mock-oa         → Company mock assessments
├── /ai-interview    → AI interview sessions
├── /company-tracks  → Company-specific preparation
└── /profile         → Evidence, achievements, settings
```

### Layer B — API (FastAPI)

Explicit router registry (`app/services/router_registry.py`) — 113 route modules registered with prefixes, tags, and startup validation for duplicate paths.

### Layer C — Application/Use-Case Layer

| Use Case | File | Coordinates |
|----------|------|-------------|
| CompleteOnboarding | `routes/onboarding.py` | Profile + blueprint + question store |
| RunDiagnostic | `routes/academy_diagnostic.py` | Quiz composer + question store |
| BuildDailyHunt | `services/path_generator.py` | Skill graph + SRS + mastery + blueprint |
| StartLesson | `routes/lesson.py` | Curriculum registry + lesson content |
| CompleteLesson | `routes/lesson.py` | Mastery engine + event + rewards |
| CreateQuizSession | `services/quiz_service.py` | Question store + adaptive composer |
| SubmitQuizAttempt | `routes/questions_solve.py` | Deterministic grader + evidence |
| StartMockAssessment | `routes/oa.py` | Company blueprint + quiz + server timer |
| FinalizeMock | `routes/oa.py` | Grader + evidence + readiness |
| CreateRepairMission | `routes/repair.py` | Mistake diagnosis + repair planning |
| CompleteRepairMission | `routes/repair.py` | Mastery + retest + SRS |
| RecordSRSReview | `services/spaced_repetition.py` | SM-2 algorithm |
| CalculateReadiness | `services/readiness_engine.py` | Evidence + blueprint + trust weights |
| GetLearnerDashboard | `routes/personal_dashboard.py` | Dashboard projections |
| RecordAuthoritativeReward | `services/gamification.py` | `record_practice()` — single XP writer |

### Layer D — Domain Engines (Canonical Owners)

| Capability | Canonical Owner | File |
|-----------|----------------|------|
| Question governance & serving | Question Store | `services/question_store.py` |
| Question trust & quality | Trust Gate | `services/question_store.py` |
| Quiz construction | Quiz Composer | `services/quiz_service.py` |
| Skill identity | Skill Taxonomy | `services/skill_taxonomy.py` |
| Skill dependencies | Skill Graph | `services/skill_assessment.py` |
| Company blueprint & role adaptation | Blueprint Overlay | `data/company_blueprints.json` |
| Curriculum & lesson progression | Lesson Registry | `content/curriculum/registry.py` |
| Deterministic grading | Grader Adapters | `routes/worlds.py`, `routes/oa.py` |
| Coding execution | Code Executor | `services/code_executor.py` |
| Mastery | Mastery Engine | `services/skill_assessment.py` |
| SRS | Spaced Repetition | `services/spaced_repetition.py` |
| Mistake diagnosis | Repair Service | `services/repair_service.py` |
| Repair planning | Repair Service | `services/repair_service.py` |
| Readiness calculation | Readiness Engine | `services/readiness_engine.py` |
| Gamification | Reward Ledger | `services/gamification.py` (`record_practice()`) |
| Daily mission planning | Daily Hunt | `services/path_generator.py` |
| Evidence aggregation | Evidence Aggregator | `services/observability.py` |
| Dashboard projections | Dashboard Read Model | `routes/personal_dashboard.py` |
| AI access | AI Gateway | `services/ai_gateway.py` |
| Compiler access | Execution Provider | `services/code_executor.py` |

### Layer E — Infrastructure

| Component | Technology | Interface |
|-----------|-----------|-----------|
| Learner state | MongoDB (Motor) | Repository pattern |
| Cache | Redis → in-memory | `services/cache.py` |
| Background jobs | Job Queue | `services/job_queue.py` |
| External AI | OpenRouter | `services/ai_gateway.py` → `ai_core.py` |
| Code execution | Piston → Docker → Local | `services/code_executor.py` |

---

## Database Architecture

**Critical Rule**: Question content never lives in MongoDB. MongoDB stores learner state only.

| Collection | Purpose | Writes From |
|-----------|---------|-------------|
| `users` | User profiles, auth | Auth routes |
| `gamification_collection` | XP, level, streak, badges | `record_practice()` only |
| `gamification_events_collection` | Immutable reward ledger | `record_practice()` only |
| `skill_graph_collection` | Skill mastery state | Mastery engine |
| `srs_cards_collection` | Spaced repetition cards | SRS engine |
| `academy_learner_profiles` | Learner profiles, onboarding | Onboarding routes |
| `academy_diagnostic_sessions` | Diagnostic attempts | Diagnostic routes |
| `academy_learning_plans` | Generated learning plans | Plan generator |
| `telemetry_events` | Observability events | Observability service |
| `lesson_progress` | Lesson completion state | Lesson routes |
| `question_answers_collection` | Question attempt history | Quiz routes |

**Indexes**: `(user_id, next_review)`, `(user_id, problem_id)`, `(user_id, event_type)`

---

## Event Flow

```
Learner Action
      ↓
API Route (validated, idempotent)
      ↓
Application Use Case
      ↓
Domain Engine (deterministic)
      ↓
Learning Event (append-only, versioned)
      ↓
Repository (MongoDB write)
      ↓
Projection Consumers (idempotent):
  ├── Mastery Projection
  ├── SRS Update
  ├── Readiness Projection
  ├── Reward Eligibility (record_practice only)
  └── Analytics
      ↓
API Response (no answer keys, no internal state)
```

---

## Security Boundaries

| Boundary | Control |
|----------|---------|
| JWT | httpOnly cookie, never in JavaScript |
| Rate limiting | 60 req/min per IP, Redis-backed |
| Login lockout | 5 failed attempts → 15 min lockout |
| Duplicate guard | 2-second window, prevents double-clicks |
| CSP headers | Blocks inline scripts, restricts frames |
| PII filtering | AI gateway strips emails, phones, cards, tokens |
| Answer key protection | Never in client payload |
| Server-authoritative timing | OA sections use `started_at`/`ends_at` |
| Idempotency | All write endpoints idempotent |

---

## Scalability Strategy

- Modular monolith — no independently deployed microservices
- Read projections rebuilt from event store
- Cache invalidation on deploy
- Cap due reviews (8-20) and practice pack size
- Pure functions for mastery/SRS (unit-testable without DB)
- Target: 1,000-10,000 early users on modest infrastructure
