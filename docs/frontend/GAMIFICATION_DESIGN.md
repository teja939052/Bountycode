# BountyCode — Gamification Design

## Principle

Gamification serves learning, not the reverse.

The current system has many mechanics. The task is to make them meaningful, not add more.

---

## Reward Hierarchy

### From Weakest to Strongest

```
ATTEMPTED
  ↓
UNDERSTOOD
  ↓
PRACTICED
  ↓
MASTERED
  ↓
TRANSFERRED
  ↓
INDEPENDENT
```

**Rule:** A learner who opens 20 lessons should NOT visually out-rank a learner who genuinely mastered 5 concepts.

### Reward Tiers

| Tier | Trigger | Reward | Visual |
|------|---------|--------|--------|
| **Attempted** | Started activity | Small XP | Subtle glow |
| **Understood** | Completed with hints | Moderate XP | Checkmark |
| **Practiced** | Completed without hints | Good XP | Star |
| **Mastered** | Passed assessment | Diamonds + badge | Gold highlight |
| **Transferred** | Solved new problem independently | Bonus diamonds | Special animation |
| **Independent** | Taught back / debugged others | Legendary reward | Unique visual |

---

## Currency System

### Diamonds (Primary)
- Earned through mastery
- Used for unlocks, power-ups
- Visible in `/tower`

### XP (Progression)
- Tracks overall level
- Not the primary focus
- Level titles communicate growth

### Stars (Quality)
- Earned for perfect performances
- Used for prestige

### Coins (Secondary)
- Earned through activities
- Used for minor unlocks

---

## Progression Systems

### Streak
**Meaning:** "I am becoming a better programmer."

**Criteria (not just "clicked app"):**
- Concept progress
- Retrieval practice
- Deliberate practice
- Mastery advancement
- Repair completion

**Behavior:**
- Streak anxiety avoided
- Failure leads to recovery path
- Freezes available but limited
- Visual: growing flame, not just number

### Combo
**Meaning:** Sustained thinking quality.

**Triggers:**
- Consecutive correct predictions
- Successful debugging
- Uninterrupted reasoning
- Solving without hints
- Successful transfer

**Visual:** "Your thinking is on fire." — flame animation, multiplier display.

### Level
**Meaning:** Capability milestone.

**Behavior:**
- Levels 1-100 with meaningful titles
- XP curve flattens at higher levels
- Each level unlocks something specific

### Boss Battles
**Meaning:** Synthesis test — show what you can do without help.

**Structure:**
```
UNDERSTAND
+
PREDICT
+
BUILD
+
DEBUG
+
TRANSFER
```

**Not just:** harder quiz.

**Visual:** Epic confrontation, clear stakes, meaningful reward.

### Mystery Boxes
**Meaning:** Surprise reward for sustained effort.

**Behavior:**
- Earned through level completion
- Contains diamonds, power-ups, or bonus content
- Not purchasable — only earned

### Leaderboard
**Meaning:** Community progress, not competition.

**Behavior:**
- Shows mastery, not just activity
- Weekly/monthly resets
- Friendly comparison

---

## Power-ups

### Available
- Extra time
- Hint reveal
- Retry
- Double XP
- Skip boss (limited)
- Show answer (limited, costs diamonds)

### Principles
- Power-ups enhance learning, not replace it
- Limited supply creates strategic choice
- "Show answer" is last resort, costs significantly

---

## Daily Login

**Meaning:** Consistent practice habit.

**Behavior:**
- Escalating rewards for consecutive days
- Reset on miss (no anxiety spiral)
- Bonus on 7-day streak

---

## Badges

**Meaning:** Evidence of capability.

**Storage:** String IDs, hydrated on read.

**Types:**
- Mastery badges (concept completed)
- Streak badges (consistency)
- Boss badges (synthesis)
- Transfer badges (independence)
- Community badges (helping others)

**Not:** Participation trophies.

---

## Failure & Recovery

### Streak Repair
- Streak can be repaired, not just frozen
- Repair requires genuine practice, not just click
- Limited repairs per month

### Mistake Book
- Every failure creates a mistake record
- Mistakes are learning material, not shame
- Repair path from each mistake
- "Clean slate" when mastered

### Retry Loop
```
FAIL
  ↓
WHY? (misconception identified)
  ↓
REPAIR (targeted practice)
  ↓
RETRY
  ↓
GROWTH
```

**Never:** "Wrong. Next question."

---

## Teaching Presence in Gamification

### Teacher Reacts To
- Actions
- Timing
- Mistakes
- Hesitation
- Hints requested
- Retries
- Execution results
- Confidence signals
- Mastery evidence

### Teacher Says
- "You changed the state correctly."
- "The loop executed one extra time because the endpoint is excluded."
- "You found the first wrong state."
- "You're solving this independently now, so I'm removing the scaffold."

### Teacher Does NOT Say
- "Great job!"
- "Keep going!"
- "Correct!"
- "Wrong!"

---

## Visual Feedback Teaches

### Success Animation
- Shows what was achieved
- Connects to capability gained
- Not just flash green

### Failure
- Shows where mental model diverged
- Provides exact recovery path
- Not just turn red

### Mastery
- Shows new capability
- Connects to what is now unlocked
- Not just add a badge

---

## Game World Reflects Skill

### Progression Visualization

```
Beginner
  → Broken workshop

Learning
  → Repair tools appear

Mastery
  → Workshop becomes functional

Transfer
  → New machine unlocked

Placement-ready
  → Challenge arena opens
```

Progression through capability, not just numbers.

---

## Information Hiding

### Never Hide
- Current skill
- Current mission
- Current goal
- Current progress
- Current weakness
- Next action

### Game Mechanics Enhance Clarity
- XP shows progress toward goal
- Streak shows consistency
- Diamonds show mastery depth
- Levels show capability milestones

**Never obscure important information behind gamification.**

---

## Consistency Rules

### XP, Diamonds, Stars, Streak, Combo, Badges
- **Only writer:** `record_practice()` (plus `spend_xp()` for shop debits)
- No direct `$inc`/`$set` elsewhere
- Every award appends one immutable `gamification_events` row
- `profile.xp == sum(ledger)` must reconcile

### Level, Ship Position, Stars
- Derive from server state
- Never incremented on client
- Never stored in localStorage
- Frontend renders backend `level`/`xp_into_level`/`xp_level_span`

---

## Anti-Patterns

### Do NOT
- Add more currencies
- Add more badges
- Add more gradients
- Add decorative particles
- Make XP the only game element
- Create fake gamification (click → XP → confetti → next)

### DO
- Make each mechanic meaningful
- Connect mechanics to learning
- Reward competence, not activity
- Create genuine anticipation
- Enable meaningful agency
- Provide clear recovery from failure
