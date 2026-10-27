# BountyCode — Unified Architecture

## Product Thesis

BountyCode is a **Personal Placement Operating System**.

It is not a question bank. It is not a course platform. It is not a coding game.

It is the system that moves a learner through:

```text
UNDERSTAND
→ PRACTICE
→ APPLY
→ REPAIR
→ PROVE
→ BECOME PLACEMENT-READY
→ PREPARE FOR A SPECIFIC OPPORTUNITY
→ INTERVIEW
→ CAREER
```

The product should reduce uncertainty about what to learn, whether the learner actually understands it, what to repair, and whether the learner is ready for a specific hiring opportunity.

---

## 1. Canonical Architecture

Use exactly one canonical learner state.

```text
                    BOUNTYCODE CORE
                           │
          ┌────────────────┴────────────────┐
          │                                 │
    LEARNER GRAPH                    OPPORTUNITY GRAPH
          │                                 │
          └────────────────┬────────────────┘
                           ↓
                   ADAPTIVE PLANNER
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
      SKILLS            PROJECTS          PLACEMENT
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ↓
                     EVIDENCE ENGINE
                           ↓
                 MASTERY / SRS / REPAIR
                           ↓
                      READINESS
                           ↓
                       CAREER
```

Existing Journey, Study Engine, Lesson Engine, Mastery, SRS, Repair, Gamification Law, and learner state remain canonical.

Any new learning feature must plug into those systems. Do not create parallel curriculum, progression, mastery, session, reward, or learner-state systems.

---

## 2. Learning Grammar

Use the following as the BountyCode teaching grammar:

```text
See
→ Understand
→ Touch
→ Predict
→ Change
→ Solve
→ Break
→ Fix
→ Remember
→ Transfer
→ Prove
```

This is **not** a requirement that every lesson contain exactly eleven screens.

The lesson planner should choose the **minimum experiences required** for the learner and concept.

- Simple concepts may use: `See → Predict → Solve → Recall → Prove`
- Difficult concepts may use the full sequence
- The learner's misconception and prior evidence should influence which experiences appear

---

## 3. Four Curriculum Layers

These are curriculum/product layers, **not** separate backend engines.

### Layer 1 — Skills

Teach:
- Programming fundamentals
- C++ / Python / Java / JavaScript
- SQL
- DSA
- Aptitude
- Reasoning
- Verbal
- CS fundamentals
- Software engineering
- AI-era development fundamentals

The teaching experience combines:
- visual explanation
- prediction
- manipulation
- real code
- immediate feedback
- guided hints
- independent proof
- spaced recall
- transfer

### Layer 2 — Projects

Projects must integrate previously learned capabilities.

Each project should contain:
- Project goal
- required concepts
- guided milestones
- code workspace
- debugging moments
- AI guidance
- independent checkpoints
- final build
- README
- shareable artifact

Projects should generate evidence toward capability, not merely completion badges.

### Layer 3 — Placement

Placement preparation is opportunity-specific.

Model:
```text
Company
→ Assessment Variant
→ Version
→ Effective Date
→ Sections
→ Skills
→ Timing
→ Question Types
→ Interview Stages
```

Never hardcode company assessment patterns globally.

The Opportunity Graph should determine which capabilities matter for each opportunity.

### Layer 4 — Proof

Proof should include:
- technical interview simulation
- behavioral interview
- HR simulation
- coding performance
- timed assessment performance
- project evidence
- concept mastery
- transfer performance
- repair history
- readiness passport

Certificates must represent verified evidence and must not imply employer endorsement unless a real employer relationship exists.

---

## 4. Flagship Curriculum

Create the first flagship experiences:

1. Trace Variables
2. Percentages
3. Blood Relations
4. Two Pointers
5. Email Format Validation
6. Sliding Window
7. SQL JOINs
8. Loop Tracing
9. Syllogisms
10. Profit/Loss

Each flagship mission must have:
- one explicit learner outcome
- short core mission
- meaningful interaction
- prediction before explanation
- change-one-variable experiment
- debugging/breaking experience where appropriate
- independent proof
- canonical evidence recording
- recall scheduling
- repair path

These are flagship exemplars, not the entire curriculum.

---

## 5. AI Tutor

AI must operate inside the learning architecture.

Modes:
```text
TEACH
GUIDE
DIAGNOSE
DEBUG
REFACTOR
REFLECT
```

Default behavior:
- identify the learner's current state
- locate the likely misconception
- ask a leading question
- provide the smallest useful hint
- progressively increase assistance
- avoid giving the final solution prematurely

Do not implement the AI as a generic chatbot floating beside the lesson.

The AI should see:
- current concept
- current interaction
- learner action history
- current code/state
- previous mistakes
- mastery evidence
- current objective

Hints may interact with the existing BountyCode economy, but do not create a second reward system.

---

## 6. Readiness Engine

Do not reduce readiness to question percentages.

Maintain evidence dimensions such as:

```text
Conceptual Understanding
Independent Solve
Transfer
Timed Performance
Consistency
Recall Stability
Error Recovery
Code Quality
Interview Performance
Recent Performance
```

Then derive readiness for a particular Opportunity Graph target.

Example:
```text
Target Opportunity
        ↓
Required Capabilities
        ↓
Learner Evidence
        ↓
Capability Gaps
        ↓
Repair Plan
        ↓
Retest
        ↓
Updated Evidence
        ↓
Readiness
```

Readiness must always be explainable.

A learner must be able to answer:
> “Why is my readiness score what it is?”

---

## 7. Placement Personalization

Company preparation is not a collection of company pages.

The system should personalize:
```text
company
role
assessment version
college context
deadline
learner strengths
learner weaknesses
recent performance
```

Then produce:
```text
TODAY
→ next best learning action
→ next best practice
→ next repair
→ upcoming assessment
→ readiness change
```

---

## 8. Product Environments

The five environments remain canonical:

```text
WORLD
What am I becoming capable of?

LAB
Can I understand and use the concept?

ARENA
Can I perform under pressure?

COMMAND
Am I ready for my target opportunity?

CAREER
Can I convert readiness into an actual opportunity?
```

No sixth student-facing learning environment should be introduced without architectural review.

---

## 9. Non-Negotiable Invariants

Exactly one:
- learner state
- curriculum graph
- progression system
- mastery system
- evidence system
- SRS system
- repair system
- gamification law
- readiness model
- canonical lesson/activity pipeline

New features must compose existing systems.

Do not create feature-specific databases merely because implementation is easier.

---

## 10. Quality Test

A flagship BountyCode experience fails if it feels like:
- a generic LMS
- a question bank
- a collection of dashboards
- a chatbot with quizzes
- a prettier LeetCode clone

It succeeds when the learner feels:
> “This system understands what I know, shows me what I don't understand, teaches me through interaction, gives me something real to build, tells me exactly what I need for my target company, and proves whether I am actually ready.”

Build toward that experience.

The central insight is that **your product should not imitate four platforms separately**. It should absorb their strongest mechanics into one learner system and then add the thing those products generally don't optimize for: **evidence-driven placement readiness tied to actual opportunities**.

That is a substantially more defensible architecture than “Brilliant + Mimo + Codecademy + Boot.dev.”
