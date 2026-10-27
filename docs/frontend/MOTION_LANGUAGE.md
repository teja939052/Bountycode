# BountyCode — Motion Language

## Principle

Motion communicates. It is not decoration.

Every motion must justify itself by communicating:
- **Cause** — what changed?
- **Direction** — where did the learner move?
- **State** — what is active?
- **Reward** — what was achieved?
- **Recovery** — how did failure become progress?

---

## Motion Hierarchy

### Tier 1: Essential (Always)
- State transitions (active, complete, error)
- Feedback confirmation (correct, incorrect)
- Directional guidance (next step, back)
- Attention shift (new content revealed)

### Tier 2: Contextual (When it teaches)
- Execution visualization (code running)
- State changes (variable updates)
- Comparison reveal (before/after)
- Progression indication (level advanced)

### Tier 3: Delight (Rare, meaningful)
- Mastery celebration
- Major unlock
- Boss victory
- Streak milestone

### Tier 0: Never
- Decorative particles
- Generic entrance animations
- Everything moving at once
- Motion without meaning

---

## Core Motion Patterns

### Attention Shift
**When:** New content appears, learner moves to next step
**How:** Gentle fade + slight upward movement
**Duration:** 200-300ms
**Easing:** Ease-out
**Meaning:** "This is now active"

### State Activation
**When:** Learner selects, focuses, or activates
**How:** Scale up slightly (1.0 → 1.02), shadow deepen
**Duration:** 150ms
**Easing:** Ease-out
**Meaning:** "This is ready for your action"

### Confirmation
**When:** Action completes successfully
**How:** Brief pulse (scale 1.0 → 1.05 → 1.0), green accent flash
**Duration:** 300ms
**Easing:** Ease-in-out
**Meaning:** "Your action had the intended effect"

### Error/Recovery
**When:** Action fails, then recovery path appears
**How:** Gentle shake (3px horizontal), then settle
**Duration:** 400ms total
**Easing:** Ease-in-out for shake
**Meaning:** "Something diverged, here is how to fix it"

### Progression
**When:** Learner advances, unlocks, or levels up
**How:** Smooth slide forward, previous content fades
**Duration:** 400ms
**Easing:** Ease-in-out
**Meaning:** "You moved forward"

### Reward
**When:** Mastery, significant achievement
**How:** Purposeful reveal (scale from 0.8 → 1.0, opacity 0 → 1)
**Duration:** 500ms
**Easing:** Spring-like overshoot
**Meaning:** "This matters"

---

## Page Transitions

### Forward (Advancing)
- Current content slides out left, fades
- New content slides in from right, fades in
- Duration: 400ms
- Meaning: "Moving forward in journey"

### Back (Returning)
- Reverse of forward
- Duration: 300ms
- Meaning: "Going back to reconsider"

### Overlay (Modal, Level Player)
- Background dims (opacity 0 → 0.5)
- Content scales up (0.95 → 1.0) + fades in
- Duration: 300ms
- Meaning: "Focused context"

### Dismiss Overlay
- Reverse of overlay
- Duration: 250ms
- Meaning: "Returning to main context"

---

## Interaction-Specific Motion

### Code Execution
**When:** Learner runs code
**How:**
1. Button press feedback (100ms)
2. Execution indicator appears (spinner or progress)
3. Result reveals with staggered timing per test case
**Duration:** 200ms per test case reveal
**Meaning:** "Code ran, here is what happened"

### Hint Reveal
**When:** Learner requests hint
**How:**
1. Previous hint fades slightly
2. New hint slides down, fades in
3. Attention shifts to new content
**Duration:** 300ms
**Meaning:** "Here is more guidance"

### Mistake Reveal
**When:** Showing what went wrong
**How:**
1. Error indicator appears (red accent)
2. Explanation fades in below
3. Recovery option highlights
**Duration:** 400ms
**Meaning:** "Here is the gap, here is the fix"

### Mastery Unlock
**When:** Concept mastered
**How:**
1. Achievement icon scales in with spring
2. Confetti or particle burst (minimal, purposeful)
3. Unlock notification slides in
**Duration:** 600ms
**Meaning:** "You have grown"

### Streak Fire
**When:** Streak active, combo building
**How:**
1. Flame grows slightly with each action
2. Color intensifies with combo
3. On break: gentle fade, recovery option
**Duration:** 200ms per action
**Meaning:** "Your consistency is burning"

---

## Timing Rules

### Micro-interactions
- **Target:** 100-200ms
- **Examples:** Button press, input focus, checkbox toggle
- **Rule:** Faster than perception threshold

### Feedback
- **Target:** 200-400ms
- **Examples:** Correct/incorrect, state change, reveal
- **Rule:** Immediate enough to connect action to consequence

### Transition
- **Target:** 300-500ms
- **Examples:** Page change, phase advance, overlay
- **Rule:** Smooth enough to follow, fast enough to not wait

### Celebration
- **Target:** 500-800ms
- **Examples:** Mastery, unlock, boss victory
- **Rule:** Meaningful enough to remember, not so long to obstruct

### Minimum
- **Never:** < 100ms (invisible)
- **Never:** > 1000ms (feels slow)

---

## Easing

### Preferred
- `ease-out` — entering, appearing
- `ease-in` — exiting, disappearing
- `ease-in-out` — state changes
- `spring` — rewards, celebrations

### Avoid
- `linear` — feels robotic
- `ease` — too generic
- Bouncy overshoot except for rewards

---

## Reduced Motion

### Respects `prefers-reduced-motion`

**When reduced motion is preferred:**
- Replace motion with opacity changes
- Instant state transitions
- No particle effects
- No parallax
- No continuous animations
- Preserve functional feedback (color, shape change)

**Never remove:**
- Functional feedback (correct/incorrect indication)
- State changes (active, disabled)
- Accessibility announcements

---

## Performance

### Rules
- No 20MB animation assets
- No 100 simultaneous animated elements
- Use `transform` and `opacity` only (GPU accelerated)
- Avoid animating `width`, `height`, `top`, `left`
- Use `will-change` sparingly
- Clean up animations on unmount

### Mobile
- Simpler motion on low-end devices
- Detect performance capability
- Graceful degradation

---

## Sound (Optional)

### When to Use
- Major mastery moments
- Unlock events
- Boss victories
- Important feedback

### When NOT to Use
- Every interaction
- Decorative purposes
- Without mute option

### Requirements
- Mute button always visible
- Volume control
- Reduced-motion-compatible (visual alternative)
- Non-audio equivalent for all information

---

## Motion Audit Checklist

For every motion in the product:

- [ ] Does it communicate cause, direction, state, reward, or recovery?
- [ ] Is it the minimum duration needed?
- [ ] Does it use GPU-accelerated properties?
- [ ] Does it respect `prefers-reduced-motion`?
- [ ] Does it have a non-motion equivalent?
- [ ] Is it consistent with the same action elsewhere?
- [ ] Would removing it make the experience worse?

If any answer is "no" or "I don't know," remove or redesign the motion.
