# BOUNTYCODE_GAME_ENGINE_V2.md
**Version:** 2.0 (Launch Spec)
**Effective Date:** October 18, 2026
**Governed By:** `/docs/BOUNTYCODE_VISION_LOCK.md`
**Theme Spec:** `/docs/BOUNTYCODE_THEME_LOCK.md`

---

## 0. Scope Guard (Read This First)

**This document changes:**
- ✅ What things are **called** (XP → Proof, diamonds → Bounty)
- ✅ How things **look** (Career Voyage theme, not fantasy RPG)
- ✅ How rewards are **earned** (mastery-linked, not RNG)
- ✅ Which badges are **awardable** (all visible badges must be earnable)

**This document does NOT change:**
- ❌ XP math / level curve (existing gamification.py logic)
- ❌ Badge IDs (stored data, for backward compatibility)
- ❌ Reward ledger schema (gamification_events collection)
- ❌ Streak logic (existing single-writer law)
- ❌ Power-up effects (existing functionality)
- ❌ League promotion logic (only labeling, not computation)

**If a task in this doc would require:**
- New MongoDB collection
- New reward source type
- New game logic beyond renaming/relabeling

**→ It's out of scope.** Flag it back to PRD, don't do it under cover of "theme pass."

---

## 1. The Fundamental Rule

**The game must answer:**
> "What did I actually accomplish?"

**Not:**
> "How many clicks did I make?"

**Hierarchy:**
```
REAL LEARNING ACTION
       ↓
EVIDENCE
       ↓
PROOF (non-spendable, demonstrated capability)
       ↓
PROGRESSION
       ↓
BOUNTY / COSMETIC REWARD (spendable currency)
       ↓
RETURN MOTIVATION
```

**Not:**
```
CLICK
 ↓
XP
 ↓
LEVEL
```

**This distinction is absolutely central.**

---

## 2. Product Vocabulary (XP → Proof/Bounty)

### 2.1 PROOF (Non-Spendable)

**Represents:** Demonstrated capability
**Earned through:** Mastery-linked learning actions
**Display:** "You earned +24 Proof" (not "+75 XP")

**Proof Table:**
| Action | Proof Earned | Reason |
|---|---|---|
| Correct prediction | +5 Proof | Pattern recognition demonstrated |
| Successful manipulation | +8 Proof | Interactive understanding |
| Solve without hint | +15 Proof | Independent problem-solving |
| Debug successfully | +18 Proof | Error diagnosis + fix |
| Successful transfer | +22 Proof | Apply pattern to new context |
| Timed drill passed | +25 Proof | Speed + accuracy under pressure |
| Repair + retest passed | +30 Proof | Overcame identified weakness |
| Pattern mastered (80%+ on assessment) | +40 Proof | Demonstrated mastery |

**Important:**
- Proof is **not** a readiness score
- Student cannot say: "I have 8,000 Proof, therefore I'm 80% ready"
- Readiness remains **evidence-based** and separately calculated

### 2.2 BOUNTY (Spendable Currency)

**Represents:** Game currency for cosmetics
**Earned through:** Meaningful progress + selected game activities
**Spent on:**
- Character skins (ship captain avatars)
- Ship/route skins (voyage visual themes)
- Camp decorations (profile customization)
- Profile frames (achievement borders)
- Effects (celebration animations)
- Emotes (social expressions)
- Sound packs (custom SFX)
- Map cosmetics (voyage map themes)
- Theme variants (Pirate Voyage, Cyberpunk, Terminal, Campus, Minimal)

**Display:**
```
MISSION COMPLETE

+24 PROOF
+50 BOUNTY

Two Pointers demonstrated
Transfer passed
Retention scheduled
```

**Not:**
```
+75 XP
```

**Why this wins:**
- **Ownable vocabulary** (Proof/Bounty, not generic XP/Gold)
- **Fits brand** (Career Voyage theme)
- **Clear separation** (Proof = mastery, Bounty = cosmetics)

---

## 3. The Seven Loops (Time Horizons)

### 3.1 Moment Loop (5–60 seconds)

**Flow:**
```
attempt → feedback → micro celebration → next action
```

**Implementation:**
- Visual state change (button pulse, progress bar fill)
- Tiny sound (subtle chime, not explosion)
- Progress animation (combo counter, streak flame)
- Immediate feedback ("Correct!" / "Not quite, try again")

**Rule:** No giant fireworks for every click.

### 3.2 Mission Loop (5–15 minutes)

**Flow:**
```
MISSION → learn → interact → solve → prove → reward
```

**Implementation:**
- This is your **main game loop** (10-step lesson: Explain → See → Interact → Predict → Solve → Break → Debug → Recall → Transfer → Prove)
- Reward at end: Proof + Bounty + celebration

**Example:**
```
MISSION: Two Pointers Pattern
├── Explain (2 min) → +5 Proof
├── See (2 min) → +5 Proof
├── Interact (3 min) → +8 Proof
├── Predict (2 min) → +8 Proof
├── Solve (5 min) → +15 Proof
├── Break (3 min) → +18 Proof
├── Debug (3 min) → +18 Proof
├── Recall (2 min) → +15 Proof
├── Transfer (5 min) → +22 Proof
└── Prove (10 min, timed assessment) → +40 Proof + 100 Bounty

TOTAL: +136 Proof + 100 Bounty
```

### 3.3 Repair Loop (Your Strongest Product-Specific Loop)

**Flow:**
```
FAIL → DIAGNOSE → REPAIR MISSION → RETEST → PROOF
```

**Why this wins:**
- **Bigger sense of achievement** than first-try success
- **Student overcame identified weakness** (productive struggle rewarded)
- **Aligns with vision** (closed-loop repair → mastery)

### 3.4 Daily Loop (Every Day)

**Flow:**
```
TODAY'S CONTRACT → complete → daily streak → reward
```

**Example Contract:**
```
TODAY — TCS PREP

1. Repair percentages      8 min
2. Practice syllogisms     10 min
3. Pseudocode drill        7 min
4. Retrieval                5 min

Estimated time: 30 min
```

**Why this wins:**
- **Student doesn't wonder:** "What do I study today?"
- **System answers:** "Here's your 30-min contract"
- **Aligns with AlgoMaster/Duolingo:** Structured path + repeated practice

### 3.5 Weekly Loop (Later, Post-Launch)

**Flow:**
```
Weekly Mission → company challenge → cohort comparison → reward
```

**Implementation:**
- **Leagues live here** (but only after promotion/relegation is real)
- **Until then:** Simple personal weekly challenge (not fake competition)

**Rule:** Never show fake competition mechanics.

### 3.6 Long-Term Loop

**Flow:**
```
PATTERN → MASTER → RANK → DOMAIN MASTERY → COMPANY READINESS → NEW TARGET
```

**Why this wins:**
- **Game + readiness systems meet** (Proof leads to Readiness)
- **Clear next step** (student knows what to do)
- **Outcome-focused** (readiness for company, not just "level up")

---

## 4. Curriculum Drives Game (Not Other Way Around)

### 4.1 Canonical Hierarchy

```
COMPANY (TCS, Infosys, Wipro, Cognizant, Capgemini)
   ↓
BLUEPRINT (NQT, Elevate, Elite, NLTH, GenC)
   ↓
DOMAIN (Quantitative, Reasoning, Verbal, Programming Logic, DSA)
   ↓
SKILL (Percentages, Ratios, Syllogisms, Loop Tracing, Arrays)
   ↓
PATTERN (Successive Change, Ratio Scaling, Set Relationships, Nested-Loop State Tracking, Two Pointers)
   ↓
MISSION (10-step lesson: Explain → See → Interact → Predict → Solve → Break → Debug → Recall → Transfer → Prove)
```

**Why this wins:**
- **Matches actual assessments**
- **Not generic fantasy worlds** (no "Variables Valley", "Loop Lake")
- **Blueprint metadata** (source, source_type, effective_from, last_verified, verification_status)

### 4.2 Blueprint Metadata Schema

```python
# backend/app/models/company_blueprint.py
class CompanyBlueprint:
    id: str
    company: str  # "TCS"
    assessment_name: str  # "NQT"
    source: str  # "https://www.tcsion.com/hub/national-qualifier-test/it-career-readiness-pack/"
    source_type: str  # "official_company_website"
    effective_from: str  # "2026-01-01"
    last_verified: str  # "2026-09-15"
    verification_status: str  # "verified" | "unverified" | "outdated"
    sections: list[Section]
```

**Rule:** Never hardcode "this is the TCS format" without date/source metadata.

---

## 5. Pattern Engine (Broader Than DSA)

### 5.1 Pattern Categories

**Quant Patterns:** Percentage change, Successive percentage, Ratio scaling, Work-rate composition, Relative speed, Average replacement, Profit/loss transformation

**Reasoning Patterns:** Syllogism set logic, Blood-relation graph, Direction graph, Coding-decoding transformation, Sequence detection, Arrangement constraints

**Programming Logic:** Variable tracing, Loop-state tracking, Nested-loop counting, Condition evaluation, Array mutation, Function flow, Recursion tracing

**DSA:** Two pointers, Sliding window, Hash lookup, Binary search, Prefix sum, Sorting, Stack, Queue

**Why this wins:**
- **AlgoMaster philosophy** (structured patterns, recommended order, concept quizzes, focused practice, speedruns) applied to **service-company prep** (not just DSA)
- **Broader than DSA** (Quant, Reasoning, Programming Logic patterns)

---

## 6. Lesson = Level (10-Step Mission)

### 6.1 Mission Structure

```
Pattern Mission
├── HOOK (story intro, 30 sec)
├── SEE (visual explanation, 2 min)
├── INTERACT (drag-drop, 3 min)
├── PREDICT (MCQ, 2 min)
├── SOLVE (code/written, 5 min)
├── BREAK (find bug, 3 min)
├── DEBUG (fix bug, 3 min)
├── RECALL (fill-in-blank, 2 min)
├── TRANSFER (new context, 5 min)
└── PROVE (timed assessment, 10 min)
```

**Not every subject needs every step**, but runtime should support all of them.

---

## 7. Declarative Reward Engine

### 7.1 One Reward Result Schema

```python
# backend/app/models/reward.py
class RewardResult:
    event: str  # "pattern_transfer_passed"
    proof: int  # 20
    bounty: int  # 15
    badges: list[str]  # []
    unlock: str  # "pattern-advanced-02"
    reason: str  # "Transfer demonstrated"
```

**Rule:**
- Frontend **does not calculate** any rewards
- Server **decides** (content event → reward policy → one reward result → ledger → player state)
- Every reward must have **reason** (tells story: "Transfer demonstrated", not "+75 XP")

### 7.2 Reward Policy Schema

```python
# backend/app/models/reward_policy.py
class RewardPolicy:
    event: str  # "pattern_transfer_passed"
    proof_base: int  # 20
    bounty_base: int  # 15
    multipliers: dict  # {"first_attempt": 1.5, "speed_bonus": 1.25}
    badges: list[str]  # []
    unlock: str  # "pattern-advanced-02"
```

---

## 8. Performance Rewards (Not RNG)

### 8.1 Replace Random with Performance

**Bad:**
```
Student solves badly → RANDOM CRIT → huge reward
```

**Better:**
```
Solved independently → Independent bonus (+1.5× Proof)
Solved quickly + correctly → Precision bonus (+1.25× Proof)
Passed transfer → Transfer bonus (+22 Proof)
Repaired previous weakness → Recovery bonus (+30 Proof)
Returned after SRS → Retention bonus (+15 Proof)
```

**Every bonus tells a story** (not "you got lucky").

---

## 9. Power-Ups (Functional, Not Cosmetic)

### 9.1 Active Gameplay Power-Ups

**Keep:**
- **SCOUT** (reveal first clue, 10 Bounty)
- **SECOND CHANCE** (one retry on failed practice, 30 Bounty)
- **TIME BANK** (add 2 min to non-high-stakes drill, 20 Bounty)
- **FOCUS** (suppress distractions/animations for 10 min, 15 Bounty)

**Remove:**
- extra_time (cosmetic, no consumer)
- hint_reveal (cosmetic, no consumer)
- retry (cosmetic, no consumer)
- show_answer (cosmetic, no consumer)
- speed_boost (cosmetic, no consumer)
- shield (cosmetic, no consumer)

**Rule:** Never let power-up bypass evidence requirements for readiness or high-stakes assessment.

```
Mock OA
❌ Show Answer
❌ Infinite Retry
❌ Score Shield
```

**Keep competitive/high-stakes results clean.**

---

## 10. Declarative Badge System

### 10.1 Badge Catalog Schema

```python
# backend/app/models/badge.py
class Badge:
    id: str  # "debug-hunter"
    name: str  # "Debug Hunter"
    condition: dict  # {"event": "debug_passed", "count": 10}
    reward: dict  # {"proof": 50, "bounty": 100, "cosmetic": "debug-aura"}
```

**Rule:**
- Catalogued but unawardable badges → **CI fails**
- Same for achievement chains (if UI says "Reward: 500 Bounty", backend must actually pay it)

### 10.2 Runtime Award Logic

```python
# backend/app/services/badges.py
class BadgeEngine:
    async def check_badges(self, user_id: str, event: str, context: dict) -> list[str]:
        badges_earned = []
        for badge in self.BADGE_CATALOG:
            if await self.check_condition(user_id, badge.condition, event, context):
                await award_badge(user_id, badge.id)
                await award_proof(user_id, badge.reward["proof"])
                await award_bounty(user_id, badge.reward["bounty"])
                await unlock_cosmetic(user_id, badge.reward["cosmetic"])
                badges_earned.append(badge.id)
        return badges_earned
```

---

## 11. Role Personalization (Adapter, Not Duplicate)

### 11.1 Role Lens

```
ONE CURRICULUM
      ↓
ROLE LENS
```

**Role Dimensions:** Software Developer, QA / Automation, Data / BI, Support / Operations, Analyst

**Role Changes:**
- ✅ Skill weight
- ✅ Recommended patterns
- ✅ Practice order
- ✅ Mock composition
- ✅ Readiness lens

**Role Does NOT Change:**
- ❌ Duplicate lessons (Two Pointers lesson is one lesson, not "Developer Two Pointers" + "QA Two Pointers")

---

## 12. Language Personalization (Two Independent Concepts)

### 12.1 Interface/Teaching Language
English, Hindi, Telugu, Marathi, Tamil, Kannada

### 12.2 Coding Language
C, C++, Java, Python, JavaScript

**Rule:** Never mix them.
- ✅ Telugu explanation of Python lesson (interface language = Telugu, coding language = Python)
- ❌ "Python translated to Telugu"

**Canonical knowledge remains the same.**

---

## 13. Theme System (Career Voyage)

### 13.1 Core Theme

**Career Voyage**
- Student is progressing toward target career
- Not fantasy RPG (no dragons, wizards, dungeons)
- Not generic esports ladder (no "Iron III", no bare tier-list naming)

**Visual Metaphor:**
```
HOME PORT (onboarding)
   ↓
QUANT DISTRICT (Quantitative Aptitude)
   ↓
REASONING DISTRICT (Logical Reasoning)
   ↓
LOGIC DISTRICT (Programming Logic)
   ↓
DSA DISTRICT (Data Structures & Algorithms)
   ↓
COMPANY DOCK (TCS, Infosys, Wipro, Cognizant, Capgemini)
   ↓
ASSESSMENT (mock OA)
   ↓
READY (job offer)
```

### 13.2 Theme Skins (Cosmetic Only)

**Default:** Career Voyage
**Theme Skins:** Pirate Voyage, Cyberpunk, Terminal, Campus, Minimal

**Rule:** Content should never know theme.

---

## 14. Social Game Layer (Post-Launch)

### 14.1 Build Order

```
Personal progress (launch)
      ↓
Weekly challenge (post-launch Week 1)
      ↓
Friends (post-launch Week 2)
      ↓
Small cohorts (post-launch Week 3)
      ↓
Company cohorts (post-launch Week 4)
      ↓
Campus competitions (post-launch Week 5)
```

**Evidence-backed:** Duolingo uses friends quests + friend streaks.

---

## 15. GameState Model (Technical Architecture)

### 15.1 GameState Schema

```python
# backend/app/models/game_state.py
class GameState:
    player_id, target_company, target_role, language
    domain_progress, pattern_progress, mastery, unlocks
    proof (non-spendable), bounty (spendable), reward_history
    streak: current, longest, freezes
    missions: daily, active, completed, quests
    inventory: cosmetics, powerups, themes
    achievements: badges, titles, chains
    social: friends, cohort, leaderboard
    presentation: theme, sound, accessibility
```

### 15.2 Key Law

```
CLIENT = presentation
SERVER = truth
LEDGER = history
```

**Client:** Renders theme, plays sound, shows accessibility options. **Does NOT compute level/Proof/Bounty.**
**Server:** Computes level/Proof/Bounty, validates badge conditions, awards rewards. **Single source of truth.**
**Ledger:** gamification_events collection, REWARD_POLICY_VERSION = "2026.1", reconciliation pinned by tests/test_economy_honesty.py.

---

## 16. Existing gamification.py (Don't Rewrite Before Launch)

### 16.1 Preserve Facade

```python
# backend/app/services/gamification.py
async def record_practice(user_id, activity_type, score, metadata):
    # Existing orchestration engine (keep as-is for launch)
    return result
```

### 16.2 Post-Launch Split

```
gamification/
├── rewards.py, progression.py, streaks.py, quests.py
├── achievements.py, economy.py, social.py, cosmetics.py
├── events.py, policies.py, facade.py
```

**Why:** Clean future architecture, no destructive rewrite, backward compatible.

---

## 17. Bug Fix Acceptance Criteria

| Current Issue | New Rule | CI Check |
|---|---|---|
| Duplicate reward fields | One canonical result schema | Schema validation |
| 38 display-only badges | Every visible badge awardable | Badge awardability test |
| Unpaid achievements | Reward transaction mandatory | Ledger reconciliation |
| Wrong badge condition | Declarative test per badge | Condition schema validation |
| RNG critical hits | Performance-linked bonuses | No RNG in reward calculation |
| Cosmetic-only power-ups | Every active power-up has real consumer | Power-up consumer test |
| Fake leagues | Real cohort/season state or don't show it | League state validation |
| Client level calculation | Server-only progression | No client-side level math |
| milestone_xp_bonus mismatch | Schema names match actual meaning | Field naming audit |
| Three streak counters | One canonical streak state | Streak source consolidation |
| XP/diamonds terminology | Product UI → Proof/Bounty | Vocabulary audit |

---

## 18. October 18 Launch Requirements

### 18.1 Must Ship

- ✅ Server-authoritative rewards (no client computation)
- ✅ Proof/Bounty product vocabulary (rename XP → Proof, diamonds → Bounty in UI)
- ✅ Mission progression (10-step lesson loop)
- ✅ Real unlocks (pattern-advanced-02, etc.)
- ✅ Streak (single canonical source)
- ✅ Daily mission (Today's Contract)
- ✅ Mastery-linked rewards (performance bonuses, not RNG)
- ✅ Working badges (all visible badges awardable)
- ✅ Working completion celebrations (moment loop)
- ✅ Company-targeted route (TCS/Infosys/Wipro/Cognizant/Capgemini)
- ✅ Theme system (Career Voyage + Pirate/Cyberpunk/Terminal/Campus/Minimal skins)
- ✅ Sound/motion settings (accessibility, prefers-reduced-motion)
- ✅ Mobile-responsive game UI
- ✅ Analytics (Proof/Bounty earned, mission completion, streak)
- ✅ Idempotency (no double-rewards)
- ✅ Reward reconciliation (gamification_events ledger)

### 18.2 Post-Launch

- Real leagues (cohort/season state)
- Friends (social layer)
- Campus competition (college leaderboards)
- Guild/cohort challenges (5-person squads)
- Seasonal events (festive themes)
- Cosmetic marketplace (Bounty spending)
- Advanced collections (badge albums)
- Richer world map (Quant/Reasoning/Logic/DSA districts)
- Dynamic events (limited-time challenges)

---

## 19. Architecture

```
                    BOUNTYCODE GAME ENGINE
                             │
              ┌──────────────┴──────────────┐
              │                             │
        LEARNING ENGINE                GAME ENGINE
              │                             │
       Company Blueprint               Mission
              │                        Progression
          Skill/Pattern                 Rewards
              │                         Streak
           Lesson                      Quests
              │                         Rank
           Practice                   Inventory
              │                        Social
          Assessment                 Cosmetics
              │                          Theme
           Evidence
              │
          Readiness
              │
              └──────────────┬──────────────┘
                             │
                    PLAYER STATE + LEDGER
```

**Every game event comes from meaningful educational event:**
- ✅ Predicted correctly, Solved independently, Debugged, Recalled, Transferred, Mastered, Repaired, Retested

**BountyCode is rewarding them for becoming good at the thing they came here to learn.**

---

## 20. Agent Instruction

```
Build BountyCode's game engine around demonstrated learning, not activity volume.

1. Product vocabulary: Proof = non-spendable demonstrated-skill progression; Bounty = spendable game currency.

2. Preserve existing single-writer ledger architecture during launch.
   - Do NOT rewrite the 2,032-line gamification orchestration engine yet.
   - Keep record_practice(...) as compatibility facade.

3. Fix all known integrity gaps:
   - Impossible badges → wire or remove
   - Unpaid achievement rewards → pay them
   - Wrong badge conditions → fix declarative tests
   - Unused power-ups → remove or add consumers
   - Fake league state → hide or make real
   - Client-side level truth → server-only
   - Duplicate result fields → one canonical schema
   - Misleading field names → schema names match actual meaning
   - Multiple streak sources → one canonical streak state
   - XP/diamonds terminology → product UI → Proof/Bounty

4. Every visible mechanic must have:
   - Functioning backend consumer
   - Reward reconciliation with ledger

5. Learning events are primary source of Proof:
   - Prediction, interaction, independent solve, debug, recall, transfer, mastery, repair, retest

6. Random reward multipliers must NOT materially determine learning progression.
   - Replace RNG critical hits with performance-linked bonuses

7. Game mechanics must NEVER bypass high-stakes evidence/readiness gates.
   - Mock OA: no Show Answer, no Infinite Retry, no Score Shield power-ups

8. Curriculum hierarchy:
   Company → Blueprint → Skill Domain → Pattern → Lesson → Practice → Assessment → Evidence → Diagnosis → Repair → Retest → Readiness

9. Game hierarchy:
   Mission → Progression → Proof/Bounty → Streak → Quest → Rank → Unlock → Cosmetics

10. Role/company/language are adapters over ONE canonical curriculum.
    - Do NOT duplicate content

11. Themes are presentation skins over canonical curriculum.
    - Do NOT embed theme logic in lessons

12. Launch target: October 18, 2026.

13. Before implementing any large change:
    - Inspect existing code
    - Produce migration plan
    - NO DESTRUCTIVE REWRITE

14. Governed by: /docs/BOUNTYCODE_VISION_LOCK.md
```