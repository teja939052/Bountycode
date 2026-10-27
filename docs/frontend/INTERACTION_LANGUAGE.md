# BountyCode — Interaction Language

## Principle

All 15+ interaction types are one interaction language. They share tactile behavior, state transitions, visual language, feedback language, teacher response, sound behavior, and motion behavior.

The user should recognize: "This is a BountyCode interaction."

---

## Universal Interaction States

Every BountyCode interaction has these states:

```
IDLE
  ↓
READY
  ↓
ACTIVE
  ↓
FEEDBACK
  ↓
NEXT
```

### State Definitions

| State | Visual | Behavior |
|-------|--------|----------|
| **IDLE** | Dimmed, waiting | Learner observes, prepares |
| **READY** | Highlighted, pulsing subtly | "You can act now" |
| **ACTIVE** | Focused, responsive | Learner is doing the thing |
| **FEEDBACK** | Animated response | System reacts to action |
| **NEXT** | Clear forward path | "Now do this" |

---

## Interaction Catalog

### 1. Predict (Multiple Choice)
**Learner Goal:** Anticipate behavior before execution
**Mental Model:** "I think I know what happens"
**Action:** Select option
**Consequence:** Immediate correct/incorrect + explanation
**Teacher Response:** Explain why, reveal mental model gap
**Mistake Signal:** Wrong selection + misconception hint
**Recovery:** Retry with hint
**Mastery Evidence:** Correct prediction without hint

### 2. Manipulate (Code Editor)
**Learner Goal:** Change state and observe
**Mental Model:** "If I change X, Y happens"
**Action:** Edit code, run
**Consequence:** Execution result + variable state visualization
**Teacher Response:** "You changed X, but Y stayed the same because..."
**Mistake Signal:** Unexpected output + state divergence
**Recovery:** Debug mode, hint ladder
**Mastery Evidence:** Correct manipulation on first try

### 3. Trace (Execution Path)
**Learner Goal:** Follow code execution step by step
**Mental Model:** "Code runs line by line"
**Action:** Step through execution
**Consequence:** Variable state at each line, highlighted current line
**Teacher Response:** "At this line, the variable becomes..."
**Mistake Signal:** State doesn't match expectation
**Recovery:** Replay, hint
**Mastery Evidence:** Correct trace prediction

### 4. Build (Construct Code)
**Learner Goal:** Write working code from specification
**Mental Model:** "I can translate requirements into code"
**Action:** Write code in editor, submit
**Consequence:** Test case results, pass/fail
**Teacher Response:** Show passing/failing tests, explain gap
**Mistake Signal:** Test failure + error message
**Recovery:** Repair steps, retry
**Mastery Evidence:** All tests pass without hints

### 5. Debug (Fix Broken Code)
**Learner Goal:** Find and fix a bug
**Mental Model:** "Something is wrong, I need to find it"
**Action:** Identify bug location, apply fix
**Consequence:** Code executes correctly
**Teacher Response:** "The bug was here because..."
**Mistake Signal:** Wrong diagnosis
**Recovery:** Hint ladder, show solution
**Mastery Evidence:** Correct diagnosis + fix on first attempt

### 6. Break (Diagnose Buggy Code)
**Learner Goal:** Identify what's wrong with given code
**Mental Model:** "I can read code and find issues"
**Action:** Select diagnosis from options
**Consequence:** Correct/incorrect + explanation
**Teacher Response:** Explain the misconception
**Mistake Signal:** Wrong diagnosis
**Recovery:** Retry, show correct diagnosis
**Mastery Evidence:** Correct diagnosis without hint

### 7. Retrieve (Recall)
**Learner Goal:** Recall concept without notes
**Mental Model:** "I know this"
**Action:** Write explanation/code from memory
**Consequence:** AI-checked accuracy
**Teacher Response:** Fill gaps, reinforce correct parts
**Mistake Signal:** Incomplete/incorrect recall
**Recovery:** Review, retry
**Mastery Evidence:** Complete, accurate recall

### 8. Transfer (New Context)
**Learner Goal:** Apply concept to new problem
**Mental Model:** "I can use this anywhere"
**Action:** Solve novel problem
**Consequence:** Pass/fail + generalization feedback
**Teacher Response:** "You transferred X to Y, but missed Z because..."
**Mistake Signal:** Partial transfer, missing edge case
**Recovery:** Guided practice, retry
**Mastery Evidence:** Correct transfer without scaffold

### 9. Decompose (Break Down Problem)
**Learner Goal:** Break complex problem into steps
**Mental Model:** "I can plan before coding"
**Action:** Arrange steps in correct order
**Consequence:** Correct/incorrect sequence
**Teacher Response:** Explain step dependencies
**Mistake Signal:** Wrong ordering
**Recovery:** Retry, show correct order
**Mastery Evidence:** Correct decomposition

### 10. Compare (Analyze Differences)
**Learner Goal:** Understand code variants
**Mental Model:** "These look similar but behave differently"
**Action:** Select correct explanation
**Consequence:** Immediate feedback
**Teacher Response:** Highlight key difference
**Mistake Signal:** Wrong selection
**Recovery:** Hint, retry
**Mastery Evidence:** Correct comparison

### 11. Fill (Complete Code)
**Learner Goal:** Complete missing code
**Mental Model:** "I know what goes here"
**Action:** Fill blank(s)
**Consequence:** Code executes correctly
**Teacher Response:** Validate completion
**Mistake Signal:** Syntax/semantic error
**Recovery:** Hint, retry
**Mastery Evidence:** Correct fill without hint

### 12. Order (Sequence Steps)
**Learner Goal:** Arrange execution order
**Mental Model:** "I understand execution flow"
**Action:** Drag/select step order
**Consequence:** Correct/incorrect sequence
**Teacher Response:** Explain flow
**Mistake Signal:** Wrong order
**Recovery:** Retry, show correct order
**Mastery Evidence:** Correct ordering

### 13. Match (Pair Concepts)
**Learner Goal:** Connect related concepts
**Mental Model:** "These go together"
**Action:** Match pairs
**Consequence:** Correct/incorrect matches
**Teacher Response:** Explain relationships
**Mistake Signal:** Wrong pairs
**Recovery:** Retry, show correct pairs
**Mastery Evidence:** All matches correct

### 14. Teach Back (Explain Concept)
**Learner Goal:** Articulate understanding
**Mental Model:** "I can explain this to someone"
**Action:** Write/speak explanation
**Consequence:** AI-evaluated completeness
**Teacher Response:** Fill gaps, reinforce
**Mistake Signal:** Incomplete explanation
**Recovery:** Guided completion, retry
**Mastery Evidence:** Complete, accurate explanation

### 15. Predict State (Variable Watch)
**Learner Goal:** Predict variable values
**Mental Model:** "I can trace state changes"
**Action:** Enter expected value
**Consequence:** Correct/incorrect
**Teacher Response:** Show actual state, explain divergence
**Mistake Signal:** Wrong prediction
**Recovery:** Retry, show execution
**Mastery Evidence:** Correct prediction

---

## Shared Interaction Behaviors

### Tactile
- Buttons respond to press (scale, shadow)
- Inputs respond to focus (border, glow)
- Drag targets highlight on hover
- Sliders show value on drag

### State Transitions
- IDLE → READY: Subtle pulse
- READY → ACTIVE: Focus ring, slight scale
- ACTIVE → FEEDBACK: Animated response
- FEEDBACK → NEXT: Clear forward motion

### Visual Language
- Correct: Green accent, checkmark
- Incorrect: Red accent, X mark
- Hint: Amber accent, lightbulb
- Mastery: Gold accent, star
- Locked: Gray, lock icon

### Feedback Language
- Success: "You changed the state correctly."
- Failure: "The loop executed one extra time because..."
- Hint: "Watch what happens when..."
- Mastery: "You can now do X without help."

### Teacher Response
- Contextual, not generic
- References specific learner action
- Explains the "why"
- Offers next step
- Never: "Great job!", "Correct!", "Wrong!"

### Motion Behavior
- Correct: Satisfying confirmation (short, purposeful)
- Incorrect: Gentle shake, then recovery
- Hint: Subtle attention shift
- Mastery: Meaningful celebration
- All respect `prefers-reduced-motion`

---

## Interaction Composition Rules

### Do Not Stack Interactions
One primary interaction per screen. Supporting interactions are secondary.

### Do Not Overwhelm
One feedback channel at a time. Visual + textual, not visual + textual + sound + animation + vibration.

### Do Not Decorate
Interaction feedback teaches. If it doesn't communicate state, consequence, or guidance, remove it.

### Do Preserve Consistency
Same interaction type → same behavior across all surfaces.
