# 18 GOVERNANCE AMENDMENT PROPOSAL

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

This document proposes exact updates to the governing documents (`BOUNTYCODE_VISION_LOCK.md`, `PRD_SERVICE_BASED_V1.md`, `AGENTS.md`) to align them with the Phase 2 design architecture. These are proposed amendments only — no governing document is modified by this proposal.

This is a design document. No implementation is authorized.

---

## 2. Governance Discrepancy: MongoDB References

### 2.1 Current State

The PRD (`docs/PRD_SERVICE_BASED_V1.md`) still describes student state as living in MongoDB. The actual architecture has been migrated to PostgreSQL/SQLAlchemy async + asyncpg. The design documents all specify PostgreSQL as the authoritative database.

### 2.2 Proposed Amendment

**PRD_SERVICE_BASED_V1.md:** Update all references to MongoDB as the student state database to PostgreSQL/SQLAlchemy. Specifically:

- Replace "MongoDB collections" with "PostgreSQL tables via SQLAlchemy"
- Replace "MongoDB" with "PostgreSQL" in database architecture sections
- Update any reference to `get_collection`, `MongoCompatCollection`, or motor/pymongo to `get_session`, SQLAlchemy `AsyncSession`, asyncpg
- Update collection names to table names (e.g., `learning_attempts`, `question_answers`, `coding_submissions`, `analytics_events`)

**No code changes are required by this proposal — the migration is already complete in the application code.**

---

## 3. Governance Discrepancy: Readiness vs Orchestrator Ownership

### 3.1 Current State

The Vision Lock and PRD describe the Readiness Engine as responsible for determining the next learning action. The Phase 2 design separates these concerns:

- **Readiness Engine**: Calculates placement readiness score (0-100) and coverage. Does NOT choose next action.
- **Learning Plan Orchestrator**: Makes the final next-action decision, consuming readiness output as one input among many.

### 3.2 Proposed Amendment

**BOUNTYCODE_VISION_LOCK.md:** Add explicit language:

> "The Readiness Engine calculates placement preparedness (0-100 score, coverage percentage) but does not select the next learning action. The Learning Plan Orchestrator is the sole owner of next-action decisions, consuming readiness output, mastery state, SRS due reviews, repair missions, and prerequisite graphs as inputs."

**PRD_SERVICE_BASED_V1.md:** Update all references to `next_action` being computed by Readiness Engine to instead reference the Learning Plan Orchestrator.

**AGENTS.md:** Update the Architecture Guidelines section to reflect the Orchestrator as the canonical next-action decision owner.

---

## 4. Governance Discrepancy: Content Trust Pipeline

### 4.1 Current State

The Vision Lock defines the trust pipeline as:

```
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED
```

Doc 03 originally used `verified/reviewed` terminology, which created ambiguity about whether human review equals TRUSTED.

### 4.2 Proposed Amendment

**BOUNTYCODE_VISION_LOCK.md:** Add explicit language:

> "Content trust pipeline: UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED. Only TRUSTED content may be served in graded flows or placement-quality assessments. HUMAN_REVIEWED content may be served only with restrictions and explicit disclosure. Human review is not automatically equivalent to TRUSTED."

**AGENTS.md:** Add the same language to the Content Trust Pipeline section.

---

## 5. Governance Discrepancy: Evidence Contract

### 5.1 Current State

The Vision Lock and PRD do not explicitly define what constitutes an evidence event. The Phase 2 design defines a comprehensive evidence event schema.

### 5.2 Proposed Amendment

**AGENTS.md:** Add to Architecture Guidelines:

> "Evidence events are server-authoritative, append-only records. Each event must include: event_id, user_id, question_id, skill_id, lesson_id, language (optional), interaction_type, first_committed_answer, final_response, hints_used, scaffolding_level, task_novelty, correct, server_graded, content_version, grading_version, time_spent_seconds, test_case_results (coding only), execution_time_ms (optional), compiler_exit_code (optional), stderr (optional), trust_status_at_time, created_at. Client-side self-reported correctness is not evidence. Duplicate events are rejected by event_id uniqueness."

---

## 6. Governance Discrepancy: Captain Byte Boundaries

### 6.1 Current State

The Vision Lock describes Captain Byte as a mentor but does not explicitly define what Captain Byte may NOT do.

### 6.2 Proposed Amendment

**BOUNTYCODE_VISION_LOCK.md:** Add to Gamification Law or AI section:

> "Captain Byte is a contextual instructional guide. Captain Byte may explain concepts, provide authored hints, narrate algorithms, and celebrate server-confirmed achievements. Captain Byte must NOT grade answers, select next activities, write mastery state, write readiness scores, award XP, or unlock progression without verified server-side outcomes. AI may paraphrase approved educational content but must be optional. AI-generated content is never authoritative for grading, mastery, readiness, or next-action decisions."

---

## 7. Governance Discrepancy: V1 Scope vs Roadmap

### 7.1 Current State

The Vision Lock defines V1 as Worlds 1-5 + TCS/Accenture in World 6. The Phase 2 design documents confirm this boundary but also document extensive roadmap content (four language tracks, SQL, CS fundamentals, advanced DSA, interview/career prep).

### 7.2 Proposed Amendment

**BOUNTYCODE_VISION_LOCK.md:** Add explicit language:

> "V1 Launch (October 18, 2026): Worlds 1-5 with 5-10 excellent lessons each, plus World 6 with TCS NQT and Accenture blueprints excellent. All other content domains (full language tracks, SQL, CS fundamentals, advanced DSA, company tracks beyond TCS/Accenture, interview/career prep) are roadmap items and must not be implemented in V1."

---

## 8. Summary of Proposed Document Changes

| Document | Section | Change |
|----------|---------|--------|
| `BOUNTYCODE_VISION_LOCK.md` | Launch Scope | Add explicit V1 boundary language |
| `BOUNTYCODE_VISION_LOCK.md` | Content Trust | Add TRUSTED-only servable rule |
| `BOUNTYCODE_VISION_LOCK.md` | Captain Byte | Add explicit boundaries (no grading/mastery/readiness/XP) |
| `BOUNTYCODE_VISION_LOCK.md` | Architecture | Add Learning Plan Orchestrator as next-action owner |
| `PRD_SERVICE_BASED_V1.md` | Database | Replace MongoDB with PostgreSQL/SQLAlchemy references |
| `PRD_SERVICE_BASED_V1.md` | Readiness | Replace Readiness next-action with Orchestrator next-action |
| `AGENTS.md` | Architecture Guidelines | Add Orchestrator as canonical next-action owner |
| `AGENTS.md` | Architecture Guidelines | Add evidence event schema requirements |
| `AGENTS.md` | Architecture Guidelines | Add PostgreSQL as authoritative database |

---

## 9. Approval Process

These governance amendments require founder approval before they become authoritative. Until approved, the design documents describe the intended architecture but the governing documents remain the source of truth.

**No code or database changes are required by this proposal.**

---

**End of 18 Governance Amendment Proposal**
