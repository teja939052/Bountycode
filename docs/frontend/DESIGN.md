# BountyCode — Frontend Design Direction

## Design Thesis

BountyCode is not a dashboard. It is a place the learner enters.

The interface must continuously communicate:
- Where am I?
- What am I doing?
- What changed because of my action?
- What am I becoming?

Every screen must answer these questions before presenting options.

---

## Emotional Goals

### Primary
- **Focused clarity** — the learner knows exactly what to do next
- **Genuine progression** — skill growth is visible, not just XP accumulation
- **Intelligent play** — playful without being childish; proud to use on campus
- **Teacher presence** — the platform teaches, not just presents content

### Secondary
- **Anticipation** — what comes next feels meaningful
- **Recovery** — failure leads to growth, not shame
- **Agency** — choices matter
- **Belonging** — "this is my journey"

---

## Visual Identity

### Art Direction
**Nostalgic spring adventure** — growth, calm focus, fresh start.

The sakura imagery communicates the learner's journey: from bud to bloom, from first line of code to first offer.

### Color System

**One dominant accent per view.** Semantic colors are reserved for semantic states.

| Role | Color | Usage |
|------|-------|-------|
| Primary accent | `#D4A843` gold | CTAs, achievements, mastery moments |
| Success | `#22c55e` green | Correct answers, completion, mastered |
| Failure | `#ef4444` red | Wrong answers, broken code |
| Warning | `#f59e0b` amber | Weakness, repair needed |
| Neutral | `#64748b` slate | Secondary text, borders |
| Background | `#faf8f5` warm white | Base surface (not pure white) |
| Surface | `#ffffff` white | Cards, elevated content |
| Dark | `#1e293b` slate-800 | Text, high contrast |

**Anti-pattern:** Do not assign a different color to every feature. One view, one dominant accent.

### Typography

- **Headings**: Bold, confident, large scale
- **Body**: Readable, calm, generous line height
- **Code**: Monospace, clear, distinct from prose
- **Hierarchy**: 3 levels max per screen — title, section, detail

### Surfaces

- Cards exist because they represent meaningful objects, not because Tailwind makes `rounded-xl bg-white p-4` easy
- Elevation communicates importance
- Whitespace creates focus
- Dividers separate stages, not decorate

### Illustration Language

- One coherent visual grammar
- Sakura / spring motif for progression
- Minimal, purposeful icons
- No decorative particles unless they teach

---

## Layout Principles

### No Card Grid as Default
Cards are not a design system. Use:
- Composition
- Hierarchy
- Whitespace
- Dividers
- Stages
- Spatial progression
- Focused panels

### Mobile First
- Design for one thumb
- Touch targets ≥ 44px
- Dragging has alternatives
- Code editing remains usable
- Bottom navigation for primary actions

### Progressive Disclosure
Show minimum required NOW. Reveal complexity as competence increases.

---

## Motion Language

### Motion Communicates
- **Cause** — what changed?
- **Direction** — where did the learner move?
- **State** — what is active?
- **Reward** — what was achieved?
- **Recovery** — how did failure become progress?

### Motion States

The interface has nine motion states:

| State | Purpose | Duration | Easing |
|-------|---------|----------|--------|
| `idle` | Calm. No motion unless necessary. | 220ms | standard |
| `focus` | Attention moves toward the current task. | 220ms | emphasized |
| `interaction` | Immediate tactile response. | 120ms | spring |
| `success` | Clear positive feedback. | 320ms | spring |
| `failure` | Clear mistake communication. | 220ms | standard |
| `repair` | Visual transition into recovery. | 320ms | emphasized |
| `mastery` | Concept transforms/unlocks. | 480ms | spring |
| `boss` | Energy increases. | 480ms | emphasized |
| `navigation` | Quiet and fast. | 220ms | standard |

### Motion Tokens

```text
duration:
  instant: 0ms
  fast: 120ms
  normal: 220ms
  slow: 320ms
  ceremony: 480ms
  unlock: 700ms

easing:
  standard: cubic-bezier(0, 0, 0.2, 1)
  emphasized: cubic-bezier(0.2, 0, 0, 1)
  spring: cubic-bezier(0.34, 1.56, 0.64, 1)
  decelerate: cubic-bezier(0, 0, 0.2, 1)

scale:
  press: 0.97
  hover: 1.02
  success: 1.05
  mastery: 1.1
  boss: 1.15
```

### Rules
- Every motion must justify itself
- Use motion tokens from `design-system/motion.ts`
- Respect `prefers-reduced-motion`
- No 20MB animations, no 100 simultaneous animated elements
- Stillness is a state — use motion selectively
- Motion must teach, orient, reward, or progress the learner

### Key Moments
- Mastery: purposeful reveal
- Failure: gentle recovery
- Unlock: meaningful transition
- Progression: visible state change

### Golden 10 Interactions

These define BountyCode's "game feel":

| # | Interaction | Purpose | Motion Token |
|---|-------------|---------|--------------|
| 1 | Mission start | Transition from Today to active learning | `focus` + `normal` |
| 2 | Prediction commit | Learner commits to a hypothesis | `interaction` + `fast` |
| 3 | Correct prediction | Snap confirmation | `success` + `spring` |
| 4 | Wrong prediction | Gentle correction | `failure` + `standard` |
| 5 | Teacher intervention | MentorGuide appears/reacts | `idle` → `focus` |
| 6 | Code execution | State change causality | `interaction` + `normal` |
| 7 | Bug discovery | First wrong state animates | `failure` + `emphasized` |
| 8 | Repair | Visual transition into recovery | `repair` + `slow` |
| 9 | Mastery | Concept transforms/unlocks | `mastery` + `ceremony` |
| 10 | World unlock | Largest progression event | `unlock` + `spring` |

### Animation Tiers

| Tier | Purpose | Examples |
|------|---------|----------|
| 1 — Learning | Cause, state, execution, debugging | Prediction snap, code execution, bug discovery |
| 2 — Interaction | Press, drag, prediction, manipulation | Tactile press, prediction commit, manipulation |
| 3 — Progress | Mastery, unlock, journey | Mastery unlock, journey progression |
| 4 — Game | Boss, rewards, missions | Boss escalation, mission start |
| 5 — Decoration | Almost none | Avoid |

### Reduced Motion

When `prefers-reduced-motion: reduce`:
- Remove large transforms
- Remove unnecessary parallax
- Shorten transitions to `instant` or `fast`
- Preserve state clarity
- Preserve feedback
- Preserve functionality
- Never make animation essential to understanding

---

## Interaction Language

### All interactions share:
- Tactile behavior
- State transitions
- Visual language
- Feedback language
- Teacher response
- Sound behavior (optional)
- Motion behavior

The user should recognize: "This is a BountyCode interaction."

### Every interaction documents:
```
Interaction
Learner Goal
Mental Model
Action
Immediate Consequence
Teacher Response
Mistake Signal
Recovery
Mastery Evidence
```

Reject interactions where the learner merely clicks to continue.

---

## Feedback Language

### Success
- Show what was achieved
- Connect to capability gained
- "You changed the state correctly" not "Great job!"

### Failure
- Show where the mental model diverged
- Provide exact recovery path
- "The loop executed one extra time because..." not "Wrong"

### Mastery
- Show the new capability
- Connect to what is now unlocked
- Not just a badge — evidence of competence

---

## Copy Principles

Remove generic instructional language:
- ~~"Great job!"~~
- ~~"Keep going!"~~
- ~~"Correct!"~~

Replace with context-aware language:
- "You changed the state correctly."
- "The loop executed one extra time because the endpoint is excluded."
- "You found the first wrong state."
- "You're solving this independently now, so I'm removing the scaffold."

The copy should teach.

---

## Anti-Patterns

### Reject Anything That Looks Like
- Generic SaaS dashboard
- Generic AI tutor
- Generic card grid
- Generic LMS
- Generic game HUD
- Generic chatbot
- Generic Tailwind demo
- Generic "premium" gradient interface

### Reject These Behaviors
- Adding decoration to compensate for weak product thinking
- Adding features to compensate for weak design
- Polishing CSS without changing the experience
- Copying Duolingo / Brilliant / LeetCode / Linear / Notion
- Card grids as default layout
- Rainbow color assignment per feature
- XP/badges as the only game elements

---

## Accessibility

### Hard Gates
- Keyboard navigation for all interactions
- Touch targets ≥ 44px
- Screen reader support for dynamic updates
- `prefers-reduced-motion` respected
- Semantic labels on all interactive elements
- Focus management in modals/overlays
- Non-color feedback for all state changes
- Contrast ratios meeting WCAG AA

---

## Performance

### Rules
- No 20MB animations
- No 100 simultaneous animated elements
- No huge SVGs
- No unnecessary dependencies
- Core learning experience functional on slow phone / poor network
- Heavy visual effects optional, not required

---

## The 10 Golden Surfaces

These are the benchmark surfaces. When they feel like the same extraordinary product, everything else conforms to that language.

1. **Onboarding** — first impression and goal commitment
2. **Today/Dashboard** — daily entry point and mission clarity
3. **Journey** — core progression and world navigation
4. **World** — spatial progression and unlock meaning
5. **Lesson** — teaching presence and interaction flow
6. **Interaction** — unified interaction language
7. **Mistake Repair** — failure-to-mastery loop
8. **Boss** — meaningful competence test
9. **Company Destination** — targeted preparation
10. **Readiness** — evidence-based progress

Each surface redesign follows this process:
1. Understand existing behavior
2. Identify the emotional/product problem
3. Create redesign direction
4. Implement
5. Render verification
6. Play again as learner
7. Refine
8. Only then move to next surface
