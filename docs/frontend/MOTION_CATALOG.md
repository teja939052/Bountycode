# BountyCode Motion Catalog

## Principles

1. **Stillness is a state.** If everything moves, nothing feels important.
2. **Motion teaches.** Every animation must communicate state, causality, or progression.
3. **Tactile over decorative.** Press, drag, predict, manipulate — these get motion. Decorative particles do not.
4. **One motion language.** All surfaces inherit the same tokens, easings, and state behaviors.
5. **Reduced motion first.** Every animated interaction has a non-motion fallback.

## Motion Tokens

| Token | Value | Use |
|-------|-------|-----|
| `instant` | 0ms | Instant state changes, reduced motion |
| `fast` | 120ms | Tactile press, hover feedback |
| `normal` | 220ms | Standard transitions, navigation |
| `slow` | 320ms | Success, repair, focus shifts |
| `ceremony` | 480ms | Mastery, boss, world unlock |
| `unlock` | 700ms | Major progression events |
| `standard` | cubic-bezier(0, 0, 0.2, 1) | Default easing |
| `emphasized` | cubic-bezier(0.2, 0, 0, 1) | Important transitions |
| `spring` | cubic-bezier(0.34, 1.56, 0.64, 1) | Tactile feedback, success |
| `press` | scale 0.97 | Button press |
| `hover` | scale 1.02 | Button hover |
| `success` | scale 1.05 | Correct answer |
| `mastery` | scale 1.1 | Concept mastered |
| `boss` | scale 1.15 | Boss battle escalation |

## Interaction States

Every important interactive element supports:

```
REST → HOVER → FOCUS → PRESS → ACTIVE → SUCCESS → ERROR → DISABLED → LOADING → LOCKED
```

State changes use the `motion.states` tokens above.

## Golden 10 Interactions

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

## Interaction Catalog

### Tactile Press
- **Source:** Uiverse press-button patterns
- **Purpose:** Make mission actions feel physical
- **Used:** Mission CTA, Submit, Start Learning
- **States:** rest → hover → press → release
- **Motion:** `press` scale on active, `hover` scale on hover
- **Accessibility:** `:active` fallback, reduced motion = instant state
- **Performance:** transform/opacity only

### Prediction Snap
- **Source:** Uiverse toggle/select patterns
- **Purpose:** Confirm prediction commitment
- **Used:** Predict phase in ConceptPlayer
- **States:** unselected → selected → result
- **Motion:** `spring` scale on select, `success` pulse on correct
- **Accessibility:** Keyboard selectable, reduced motion = color change only
- **Performance:** transform only

### Teacher Reveal
- **Source:** MentorGuide component
- **Purpose:** Teacher presence communicates guidance
- **Used:** All learning screens
- **States:** hidden → explaining → correcting → celebrating → hidden
- **Motion:** `focus` entrance, `idle` exit, mood-based color shift
- **Accessibility:** Reduced motion = instant show/hide
- **Performance:** opacity + translate only

### Repair Transition
- **Source:** Uiverse modal/overlay patterns
- **Purpose:** Shift from failure to recovery
- **Used:** RepairOverlay, mistake repair
- **States:** problem → repair → retry
- **Motion:** `repair` entrance, `normal` exit, background blur
- **Accessibility:** Focus trap, reduced motion = instant overlay
- **Performance:** opacity + backdrop-filter

### Mastery Unlock
- **Source:** Uiverse reward/reveal patterns
- **Purpose:** Celebrate genuine achievement
- **Used:** Concept mastery, world unlock
- **States:** incomplete → mastering → mastered → unlock
- **Motion:** `mastery` scale, `ceremony` duration, confetti only here
- **Accessibility:** Reduced motion = static badge reveal
- **Performance:** transform + opacity

### Code Execution
- **Source:** Uiverse loader/progress patterns
- **Purpose:** Show causality of code → result
- **Used:** Manipulate phase, transfer phase
- **States:** idle → running → result
- **Motion:** `interaction` state change, execution trace animation
- **Accessibility:** Text status, reduced motion = instant result
- **Performance:** transform + opacity

### Bug Discovery
- **Source:** Uiverse error/alert patterns
- **Purpose:** Animate first wrong state
- **Used:** Break phase
- **States:** code → bug → diagnosis
- **Motion:** `failure` shake, `emphasized` error state
- **Accessibility:** Color + icon, reduced motion = instant highlight
- **Performance:** transform + opacity

### Journey Progression
- **Source:** Uiverse navigation/stepper patterns
- **Purpose:** Spatial continuity through world
- **Used:** JourneyPage, LevelMap
- **States:** current → complete → next reveal
- **Motion:** `navigation` path activation, `focus` next node
- **Accessibility:** Text status, reduced motion = instant transition
- **Performance:** transform + opacity

### Dashboard State Change
- **Source:** Uiverse progress/counter patterns
- **Purpose:** Show meaningful progress changes only
- **Used:** TodayPage, Skills
- **States:** stale → updated
- **Motion:** `focus` on changed metric, `normal` duration
- **Accessibility:** Text update, reduced motion = instant update
- **Performance:** transform + opacity

### Boss Escalation
- **Source:** Uiverse loader/escalation patterns
- **Purpose:** Increase energy without casino feel
- **Used:** MockOA, Tower boss battles
- **States:** enter → focus → challenge → result
- **Motion:** `boss` scale, `ceremony` duration, restrained palette
- **Accessibility:** Text status, reduced motion = instant state
- **Performance:** transform + opacity

## Animation Quality Test

For every animation:
1. Why does it move?
2. What does the learner understand from the movement?
3. What state changed?
4. Does it improve orientation?
5. Does it improve satisfaction?
6. Could I remove it without losing anything?

If #6 is yes, remove it.

## Animation Tiers

| Tier | Purpose | Examples |
|------|---------|----------|
| 1 — Learning | Cause, state, execution, debugging | Prediction snap, code execution, bug discovery |
| 2 — Interaction | Press, drag, prediction, manipulation | Tactile press, prediction commit, manipulation |
| 3 — Progress | Mastery, unlock, journey | Mastery unlock, journey progression |
| 4 — Game | Boss, rewards, missions | Boss escalation, mission start |
| 5 — Decoration | Almost none | Avoid |

## Reduced Motion Behavior

When `prefers-reduced-motion: reduce`:
- Remove large transforms
- Remove unnecessary parallax
- Shorten transitions to `instant` or `fast`
- Preserve state clarity
- Preserve feedback
- Preserve functionality
- Never make animation essential to understanding
