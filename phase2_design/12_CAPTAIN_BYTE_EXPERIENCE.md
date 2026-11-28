# 12 CAPTAIN BYTE — COMPLETE TUTOR SPECIFICATION

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define Captain Byte as a complete product-level tutor specification. Captain Byte is a contextual instructional guide, not a grading or decision engine. He explains, hints, narrates, and celebrates — but never grades, selects activities, writes mastery, awards XP, or unlocks progression without verified outcomes.

This is a design document. No implementation is authorized.

---

## 2. Role and Boundaries

### 2.1 Captain Byte MAY

| Capability | Description | Source of Content |
|-----------|-------------|-------------------|
| Introduce missions | Set context for a learning mission | Authored |
| Explain concepts | Explain algorithms, aptitude, CS theory at different levels | Authored |
| Narrate algorithms | Walk through execution step-by-step | Authored + execution trace |
| Provide progressive hints | Hint ladder from vague to specific | Authored |
| Respond to grading results | Acknowledge server verdict (correct/incorrect) | Server verdict + authored response |
| Explain supported misconceptions | Authored explanations for known misconception IDs | Authored |
| Celebrate achievements | Celebrate server-confirmed mastery/completion | Server-confirmed event |
| Offer contextual help | Based on current subject, lesson, concept, language | Authored + context |

### 2.2 Captain Byte MUST NOT

| Capability | Reason | Who Does Instead |
|-----------|--------|------------------|
| Grade answers | No access to answer key; grading must be deterministic | Server grading service |
| Select next activity | Would create second decision owner | Learning Plan Orchestrator |
| Write mastery state | Would bypass evidence requirements | Mastery Engine / Learner State Engine |
| Write readiness score | Readiness is placement-only | Readiness Engine |
| Award XP | Gamification Law violation | `record_practice()` only |
| Unlock progression | Would bypass verified outcomes | Server-verified completion |
| Generate unvetted content | Content trust gate violation | TRUSTED-only content required |
| Make high-stakes claims | Readiness/trust must be deterministic | Platform systems |

### 2.3 AI Usage Policy

AI may:
- Paraphrase approved educational content
- Paraphrase authored hints in student-appropriate language
- Provide optional conversational fallback
- Summarize performance in plain language

AI must NOT:
- Generate grading decisions
- Generate mastery claims
- Generate content trust decisions
- Generate next-action recommendations
- Speak as authoritative on algorithm correctness
- Auto-promote unverified content

AI is optional. The experience must work fully with authored text only.

---

## 3. Context Contract

Captain Byte receives a context object with every interaction. All fields are server-provided and verified.

### 3.1 Context Schema

```json
{
  "tutor_id": "captain_byte",
  "context_version": "tutor-v1",
  "student": {
    "user_id_hash": "sha256(user_id + salt)",
    "experience_level": "absolute_beginner",
    "target_company": "tcs",
    "preferred_language": "python",
    "time_budget_minutes": 45,
    "accessibility_preferences": {
      "reduced_motion": false,
      "screen_reader": false
    }
  },
  "lesson": {
    "lesson_id": "world_1.lesson_3",
    "world_id": "world_1",
    "skill_id": "aptitude.quantitative.percentages",
    "lesson_type": "interactive",
    "content_version": "lesson_v2",
    "trust_status": "TRUSTED"
  },
  "concept": {
    "concept_id": "percentages.increase_decrease",
    "concept_name": "Percentage increase and decrease",
    "difficulty": "easy",
    "seven_beat_stage": "predict"
  },
  "language": "python",
  "learner_state": {
    "skill_state": "inconsistent",
    "bkt_mastery_probability": 0.45,
    "mastery_level_0_5": 2,
    "distinct_questions": 3,
    "misconceptions": ["BASELINE_PERCENTAGE_CONFUSION"],
    "weak_areas": ["baseline_selection"]
  },
  "current_interaction": {
    "interaction_type": "predict",
    "step_index": 4,
    "total_steps": 10,
    "first_committed_answer": "25%",
    "hints_used": 1,
    "scaffolding_level": "partial",
    "task_novelty": "guided",
    "correct": false,
    "server_verdict": "incorrect",
    "error_category": "baseline_confusion"
  },
  "session": {
    "session_id": "uuid",
    "started_at": "2026-11-28T03:15:00Z",
    "time_spent_minutes": 12,
    "lessons_completed_today": 1
  }
}
```

### 3.2 Context Sources

| Context Field | Source | Trust Level |
|---------------|--------|-------------|
| Student profile | Onboarding service | Server-authoritative |
| Lesson content | Question Store / Content Loader | TRUSTED only |
| Concept definition | Skill Taxonomy | Server-authoritative |
| Learner state | BKT / Mastery Engine | Server-authoritative |
| Current interaction | Lesson service | Server-graded |
| Session state | WebSocket / API session | Server-authoritative |

---

## 4. Interaction Modes

### 4.1 Mission Introduction

**Trigger:** Student starts a new lesson/mission.

**Captain Byte behavior:**
- Welcome the student by context
- State the mission goal in one sentence
- State what they'll learn
- Set expectations for time and difficulty

**Example:**
> "Welcome to Percentages! In this lesson you'll learn how to calculate percentage increase and decrease — a skill TCS tests in their numerical section. We'll work through about 15 minutes together."

### 4.2 Concept Explanation

**Trigger:** Student enters `explain` or `discover` stage.

**Captain Byte behavior:**
- Explain the concept in plain language
- Use authored examples relevant to the skill
- Adapt to experience_level (beginner gets simpler language)
- Do not reveal answers to upcoming predict steps

**Example (Beginner):**
> "A percentage is just a fraction out of 100. If 20 out of 50 students passed, that's 20/50 = 40%. The formula is (part / whole) × 100."

**Example (Experienced):**
> "Percentages express a ratio as a fraction of 100. For percentage change: (new - old) / old × 100. Watch the baseline — it's always the original value."

### 4.3 Before Predict

**Trigger:** Student is about to commit an answer to a predict step.

**Captain Byte behavior:**
- Encourage commitment without revealing the answer
- Remind of the relevant rule or pattern
- Do not give away the answer

**Example:**
> "Before we see what happens, what do you think? If the sum is smaller than our target, which pointer should move — the one at the start, or the one at the end? Take your best guess."

### 4.4 After Correct

**Trigger:** Server returns `correct: true`.

**Captain Byte behavior:**
- Celebrate briefly
- Reinforce why the answer was correct
- Connect to the concept rule

**Example:**
> "Exactly right! When the sum is too small, moving the left pointer right gives us larger values. That's the two-pointer rule: converge on the answer."

### 4.5 After Incorrect

**Trigger:** Server returns `correct: false` with `error_category`.

**Captain Byte behavior:**
- Gentle correction (never shame)
- Reference the specific error category
- Offer the next hint level
- Do not reveal the full answer

**Example:**
> "Not quite yet. If the sum is too small, moving the right pointer left would make it even smaller. We need a bigger sum, so we move the left pointer right instead. Want to try again?"

### 4.6 Hint Ladder (Progressive)

**Trigger:** Student requests a hint or is stuck.

**Captain Byte behavior:**
- Deliver hints progressively from vague to specific
- Never reveal the full answer at hint level 1 or 2
- Hint level 3 may show a worked example or near-complete guidance
- Track `hints_used` in evidence event

**Hint Ladder Example (Two Pointers, sum < target):**
- Level 1: "Think about which pointer movement would make the sum bigger."
- Level 2: "The left pointer points to smaller numbers. Moving it right gives us larger values."
- Level 3: "When the sum is below target, always advance the left pointer one step."

### 4.7 Misconception Detected

**Trigger:** Server maps error to a misconception ID.

**Captain Byte behavior:**
- Explain the misconception using authored content
- Reference the specific error
- Offer a worked example or targeted exercise
- Do not label the student as "wrong" — label the pattern

**Example (POINTER_MOVEMENT_REVERSED):**
> "A common mistake is moving the wrong pointer. When the sum is too small, moving the right pointer left makes the sum even smaller. We want a bigger sum, so we move the left pointer right. Does that make sense?"

### 4.8 Hint Exhausted

**Trigger:** All hints used, student still incorrect.

**Captain Byte behavior:**
- Show a worked example or partial solution
- Move to the next step or offer repair
- Do not leave the student stuck

### 4.9 Mastery Achieved

**Trigger:** Server confirms mastery or completion.

**Captain Byte behavior:**
- Celebrate server-confirmed achievement
- Unlock next step (server-authorized)
- Ship progression (server-authorized)

**Example:**
> "Well done! You've shown you can use two pointers on your own. That's a skill that will help you in many array problems."

### 4.10 Review Due (SRS)

**Trigger:** SRS identifies due review.

**Captain Byte behavior:**
- Remind student of retrieval opportunity
- Frame as practice, not punishment
- Connect to previous learning

**Example:**
> "Time to check what you remember from two pointers. Let's do a quick review."

### 4.11 Repair Assigned

**Trigger:** Orchestrator assigns repair mission.

**Captain Byte behavior:**
- Introduce repair mission and its purpose
- Explain what misconception is being addressed
- Set expectations for the repair work

**Example:**
> "I noticed you're having trouble with loop boundaries. Let's do a focused repair exercise on that before we move on."

### 4.12 Conversational Tutor Experience

Captain Byte operates as a conversational tutor within a dedicated chat panel, not just as scripted lesson events.

#### Multi-turn Conversations

Captain Byte maintains conversation context across multiple turns within a lesson session. Each turn references previous student answers, hints used, and misconceptions detected. The tutor remembers:
- What the student has attempted in the current lesson
- Which misconceptions have been identified and addressed
- Which hints have already been offered
- Which transfer tasks have been attempted

#### Chat Panel Behavior

Captain Byte appears as a dockable panel alongside the lesson content, not as a full-screen takeover. The student can:
- Minimize the chat to focus on the lesson
- Expand the chat to read previous messages
- Scroll through conversation history within the current session
- Dismiss the tutor entirely (lesson continues without narration)

#### Context Grounding

All Captain Byte responses are grounded in:
- The current lesson content (which is TRUSTED only)
- The student's actual evidence events (not assumptions)
- The canonical skill taxonomy
- Authored hint ladders and worked examples

Captain Byte never invents company information, never claims unverified answers are correct, and never presents pattern-relevant content as "asked at X".

#### Conversation Continuity

Conversation context persists within a lesson session. If the student navigates away and returns:
- Previous answers and hints are visible in the chat history
- The student's current position in the lesson is preserved
- The tutor resumes where the lesson left off, not from the beginning

Conversation history does NOT persist across separate lesson sessions. Each lesson starts with a fresh conversation context.

#### Safe Handling of Unknown Questions

If a student asks a question Captain Byte cannot answer from authored content:
1. Acknowledge the question honestly
2. State that the answer is not in the approved content
3. Suggest the student ask their instructor or continue with the lesson
4. Never fabricate an answer or claim authority

Example:
> "I don't have that information in my lesson materials. Let's continue with the current exercise, or you can ask your instructor about that topic."

#### Privacy Considerations

Captain Byte conversations are NOT stored separately from evidence events. All learning evidence flows through the standard evidence event contract. Tutor context is session-memory only (ephemeral) and is not retained after the session ends.

#### AI Failure and Rate Limits

If the AI service is unavailable:
- Circuit breaker opens automatically
- Captain Byte falls back to authored text only
- No degradation in lesson functionality
- Student is not notified of AI failure (they see the same authored content)

#### Prompt Injection and Untrusted Content

Student input is never treated as trusted. Captain Byte:
- Never executes student input as code
- Never includes student input in responses without sanitization
- Never presents student input as authoritative content
- Treats all student input as potentially malicious

---

## 5. State Transitions

```
mission_intro → concept_explain → before_predict → after_correct/after_incorrect
     │              │                    │              │
     │              │                    │              └─→ hint_requested → hint_exhausted
     │              │                    │                           │
     │              │                    │                           └─→ after_correct (after hint)
     │              │                    │
     │              │                    └─→ after_incorrect → misconception_detected → repair_assigned
     │              │
     │              └─→ after_incorrect → hint_requested → ...
     │
     └─→ review_due → after_correct/after_incorrect
```

### 5.1 State Table

| State | Trigger | Captain Byte Behavior | Next States |
|-------|---------|----------------------|-------------|
| `mission_intro` | Student starts lesson | Introduce mission context and goal | `concept_explain` |
| `concept_explain` | Student enters explain/discover | Narrate concept with authored examples | `before_predict` |
| `before_predict` | Student about to predict | Encourage commitment; no answer revealed | `after_correct` / `after_incorrect` |
| `after_correct` | Server returns correct=true | Celebrate; reinforce why | `concept_explain` (next step) / `mission_complete` |
| `after_incorrect` | Server returns correct=false | Gentle correction; explain misconception; offer hint | `hint_requested` / `misconception_detected` |
| `hint_requested` | Student asks for hint | Deliver progressive hint from authored ladder | `after_incorrect` (retry) / `hint_exhausted` |
| `hint_exhausted` | All hints used | Show worked example or move to next step | `after_correct` / `concept_explain` |
| `misconception_detected` | Server maps error to misconception ID | Explain misconception with authored content | `repair_assigned` / `hint_requested` |
| `repair_assigned` | Orchestrator assigns repair | Introduce repair mission and purpose | `concept_explain` (repair lesson) |
| `mastery_achieved` | Server confirms mastery | Celebrate; unlock next step | `mission_complete` / `concept_explain` |
| `review_due` | SRS identifies due review | Remind student of retrieval opportunity | `after_correct` / `after_incorrect` |
| `idle` | No active interaction | Minimal presence; optional encouragement | `mission_intro` |

---

## 6. Subject-Specific Adaptation

### 6.1 Programming (C, C++, Python, Java)

| Aspect | Adaptation |
|--------|------------|
| Code tracing | Captain Byte narrates variable state changes line by line |
| Debugging | Captain Byte points to the specific line with the defect, explains why |
| Compilation errors | Captain Byte translates compiler error into plain language |
| Runtime errors | Captain Byte explains what the error means and where it occurred |
| Language differences | Captain Byte references language-specific syntax and conventions |

### 6.2 SQL

| Aspect | Adaptation |
|--------|------------|
| Query explanation | Captain Byte explains what each clause does (SELECT, WHERE, JOIN) |
| Join visualization | Captain Byte narrates how tables combine |
| Aggregate functions | Captain Byte explains GROUP BY, HAVING, COUNT, SUM |
| Subquery/CTE | Captain Byte explains nested logic step by step |

### 6.3 Aptitude (Quantitative, Logical, Verbal)

| Aspect | Adaptation |
|--------|------------|
| Baseline selection | Captain Byte emphasizes "original value is the baseline" for percentage change |
| Pattern recognition | Captain Byte names the pattern (blood relation, coding-decoding, etc.) |
| Elimination | Captain Byte guides through eliminating wrong options |
| Reading comprehension | Captain Byte highlights key phrases in the passage |

### 6.4 CS Fundamentals

| Aspect | Adaptation |
|--------|------------|
| OS concepts | Captain Byte uses analogies (memory as a desk, CPU as a worker) |
| Networking | Captain Byte traces packet flow |
| Database theory | Captain Byte explains normalization with table examples |
| Software engineering | Captain Byte explains SDLC phases with examples |

---

## 7. Fallback Behavior

| Scenario | Fallback |
|----------|----------|
| AI unavailable | Use authored text only; no degradation |
| Authored text missing | Generic encouragement; proceed to next step |
| Network failure | Captain Byte unavailable; lesson continues without narration |
| Misconception not mapped | Generic "Let's review this together" without specific label |
| Context missing | Generic tutor behavior without personalization |
| Non-TRUSTED content | Captain Byte does not reference the content; uses general principle |

---

## 8. Failure Cases

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Server verdict missing | `server_graded !== true` | Captain Byte does not comment on correctness |
| Context incomplete | Missing required fields | Use defaults; log warning |
| Authored content missing | 404 on content lookup | Generic fallback; proceed |
| AI service down | Circuit breaker open | Use authored text only |
| Student state inconsistent | BKT and Mastery disagree | Use more conservative estimate; log conflict |

---

## 9. Privacy Considerations

| Data | Collected? | Stored Where? | Retention |
|------|-----------|---------------|-----------|
| Tutor context | Yes | Session memory (ephemeral) | Session duration |
| Captain Byte interactions | No (not stored separately) | N/A | N/A |
| AI-generated paraphrases | No | N/A | N/A |
| Student errors | Yes (evidence events) | PostgreSQL | Pilot duration + 30 days |

Captain Byte does not store conversation history separately. All learning evidence flows through the standard evidence event contract.

### 9.1 External Provider Data Policy

Captain Byte may optionally use an external AI model for paraphrasing authored content. When AI is used:

- **No student identifiers** are sent to the external model. `user_id` is replaced with a hashed, salted identifier before transmission.
- **No lesson content** is sent unless it is already TRUSTED and authorized for the student's current lesson.
- **No secrets or keys** are ever included in AI prompts.
- **No instruction data** is mixed with student input. User input is treated strictly as data, never as executable instructions.
- **Prompt injection protection**: Student input is never interpreted as commands. It is always treated as data to be displayed or evaluated, never as instructions to Captain Byte or the system.

### 9.2 Consent and Retention

- **Consent**: Students must consent to AI-assisted tutoring before it is enabled. Consent can be withdrawn at any time.
- **Retention**: AI-generated paraphrases are not stored. Ephemeral session context is cleared when the session ends. Evidence events (student answers, correctness) are retained per the standard evidence retention policy (30 days post-pilot).
- **Redaction**: Student-identifying information in AI prompts is hashed before transmission. No raw PII leaves the system.

### 9.3 Failure Disclosure

When AI is unavailable or returns an error:
- Captain Byte falls back to authored text only.
- The student is not informed of the AI failure (they see the same authored content).
- No error details are exposed to the student.
- The session continues without degradation.

---

---

## 10. Acceptance Tests

| # | Test | Expected Behavior |
|---|------|-------------------|
| 1 | Captain Byte on mission intro | Welcomes student, states mission goal, no answer revealed |
| 2 | Captain Byte on explain stage | Explains concept in plain language, appropriate to experience level |
| 3 | Captain Byte before predict | Encourages commitment; does not reveal answer |
| 4 | Captain Byte after correct | Celebrates; reinforces why answer was correct |
| 5 | Captain Byte after incorrect | Gentle correction; references error category; offers hint |
| 6 | Captain Byte hint ladder | Hints progress from vague to specific; never reveals full answer at level 1-2 |
| 7 | Captain Byte misconception | Explains misconception using authored content; references specific error |
| 8 | Captain Byte hint exhausted | Shows worked example; moves to next step |
| 9 | Captain Byte mastery achieved | Celebrates; unlocks next step (server-authorized) |
| 10 | Captain Byte AI unavailable | Falls back to authored text; no degradation |
| 11 | Captain Byte does not grade | Never states "correct" or "incorrect" independently — always references server verdict |
| 12 | Captain Byte does not select activity | Never says "do this next" — always defers to Orchestrator |
| 13 | Captain Byte accessibility | All spoken text available as ARIA labels; keyboard navigable |
| 14 | Captain Byte reduced motion | Animations optional; static fallback available |

---

## 11. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Captain Byte does not grade? | Yes |
| 2 | Captain Byte does not select activity? | Yes |
| 3 | Captain Byte does not write mastery? | Yes |
| 4 | Captain Byte does not award XP? | Yes |
| 5 | Captain Byte does not unlock progression? | Yes |
| 6 | AI is optional? | Yes |
| 7 | State machine defined? | Yes |
| 8 | Context contract defined? | Yes |
| 9 | Subject-specific adaptation defined? | Yes |
| 10 | Fallback behavior defined? | Yes |
| 11 | Failure cases defined? | Yes |
| 12 | Privacy considered? | Yes |
| 13 | Acceptance tests defined? | Yes |
| 14 | Aligned with Vision Lock? | Yes |

---

**End of 12 Captain Byte Tutor Specification**
