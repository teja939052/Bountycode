# 05_DATA_FLOW_AND_AI_CONTRACTS.md — Data Flow and AI Contracts

> Defines what data moves between the frontend, backend, learning engines, AI providers, database, and compiler.

---

## Data Flow Diagram

```
Learner Action (Frontend)
      │
      ├─► HTTP Request (JWT httpOnly cookie)
      │     │
      │     ▼
      │  FastAPI Route (validated, idempotent)
      │     │
      │     ▼
      │  Application Use Case
      │     │
      │     ▼
      │  Domain Engine (deterministic)
      │     ├──► Question Store (read-only, files)
      │     ├──► Skill Taxonomy (read-only, pure)
      │     ├──► Company Blueprint (read-only, JSON)
      │     ├──► Code Executor (Piston → Docker → Local)
      │     └──► AI Gateway (assist only, privacy-filtered)
      │     │
      │     ▼
      │  Learning Event (append-only, versioned)
      │     │
      │     ▼
      │  MongoDB (learner state only — no question content)
      │     │
      │     ▼
      │  Projection Consumers (idempotent)
      │     ├──► Mastery Projection
      │     ├──► SRS Update
      │     ├──► Readiness Projection
      │     ├──► Reward Ledger (record_practice only)
      │     └──► Analytics
      │     │
      │     ▼
      │  API Response (no answer keys, no internal state)
      │
      └─► HTTP Response (JSON, typed)
```

---

## Data Classification

| Classification | Description | Can Go to AI? | Can Go to Client? | Stored in MongoDB? |
|---------------|-------------|---------------|-------------------|-------------------|
| Public | Lesson content, question statements | Yes | Yes | No (files only) |
| Internal | Question explanations, hints (post-submission) | No | Yes (after submission) | No |
| Confidential | Answer keys, correct indices, hidden test cases | No | Never | No (files only) |
| PII | Email, phone, name, address | No (filtered) | Only own user's data | Yes (users collection) |
| Learner State | Attempts, scores, mastery, SRS, XP | No (aggregates only) | Only own user's data | Yes |
| Rewards | XP, coins, streaks, badges | No | Only own user's data | Yes (gamification) |
| Events | Append-only learning events | No | Aggregated only | Yes (telemetry_events) |

---

## AI Gateway Contract

### Request Schema

```json
{
  "task": "explain_mistake",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "model": null,
  "temperature": 0.7,
  "max_tokens": 1000,
  "user_id": "opaque-id",
  "correlation_id": "req-123",
  "response_schema": {...},
  "strip_pii": true
}
```

### Response Schema

```json
{
  "content": "string",
  "parsed": null | object,
  "model": "string",
  "tokens": integer,
  "cost_estimate": number,
  "template_version": "string",
  "task": "string",
  "timestamp": "ISO-8601"
}
```

### PII Filtering (Applied Before AI Submission)

| Pattern | Replacement |
|---------|------------|
| Email addresses | `[EMAIL]` |
| Phone numbers | `[PHONE]` |
| Credit card numbers | `[CARD]` |
| Long alphanumeric tokens (20+ chars) | `[TOKEN]` |

### AI Allowed vs. Forbidden Responsibilities

| Allowed (Assist) | Forbidden (Engine) |
|-----------------|-------------------|
| Concept explanation | Question trust promotion |
| Progressive hints | Objective answer correctness |
| Mistake diagnosis | Hidden test evaluation |
| Interview rubric feedback | BALMA mastery calculation |
| Resume analysis | SRS scheduling |
| Cover letter generation | Readiness calculation |
| Content drafting (untrusted) | Company blueprint truth |
| | Rewards and XP |
| | Unlock authorization |

---

## Data Flow by Feature

### Lesson Completion

```
Frontend: POST /api/v1/lessons/{id}/complete
         {lesson_id, step_id, answer, code, time_spent}
      ↓
Backend: Validate JWT, lesson ownership, step eligibility
      ↓
Engine: Deterministic grader (worlds_data checks)
         ├──► question_store (read-only: expected patterns)
         └──► gamification.record_practice(score=0-10) [XP only]
      ↓
Event: LessonCompleted {user_id, lesson_id, score, xp_awarded, timestamp}
      ↓
MongoDB: lesson_progress (write), gamification_collection (write)
      ↓
Response: {lesson_completed: bool, xp_earned: int, mastery_updated: float}
```

### Quiz Submission

```
Frontend: POST /api/v1/questions/{id}/submit
         {question_id, answer, time_taken_seconds, client_attempt_id}
      ↓
Backend: Validate JWT, session ownership, question belongs to session
      ↓
Engine: Deterministic grader (single_choice, multiple_select, code, etc.)
         ├──► question_store.find_one_verified() [get correct answer]
         └──► gamification.record_practice(score=0-10) [XP only]
      ↓
Event: QuestionGraded {user_id, question_id, correct, score, attempt_id, timestamp}
      ↓
MongoDB: question_answers_collection (write), gamification_collection (write)
      ↓
Response: {correct: bool, score: int, explanation: string, next_question?: id}
```

### Mock OA

```
Frontend: POST /api/v1/oa/start
         {company, role, difficulty}
      ↓
Backend: Validate JWT, company blueprint exists, sufficient trusted questions
      ↓
Engine: Company blueprint (section weights, timing) + quiz_service.build_quiz()
         ├──► question_store._servable_questions() [trust gate]
         └──► Server timer (started_at, ends_at)
      ↓
Event: MockOAStarted {user_id, company, blueprint_version, session_id, timestamp}
      ↓
MongoDB: oa_sessions (write)
      ↓
Response: {session_id, sections, questions_without_keys, time_limits}
```

### AI Mistake Explanation

```
Frontend: POST /api/v1/ai/tutor/explain
         {lesson_id, question_id, attempt_id, preferred_language}
      ↓
Backend: Validate JWT, attempt ownership, lesson eligibility
      ↓
Engine: AI Gateway (ai_gateway.ai_explain_mistake)
         ├──► Privacy filter (PII removal)
         ├──► ai_core.chat_completion() [circuit breaker, cache, retry]
         └──► Schema validation (diagnosis, explanation, hint, next_step)
      ↓
Event: AIExplanationRequested {user_id, task, tokens, cost_estimate, timestamp}
      ↓
Response: {diagnosis, explanation, hint, next_step, confidence, template_version}
```

---

## Answer Key Protection

No API response to the client may contain:

- `correct_index`, `correct_answer`, `solution`, `_correct_index`, `_correct_answer`, `_solution`
- Hidden test cases
- Internal trust notes
- Private source metadata
- Server-only scoring configuration

Violations are caught by the route safety test suite.
