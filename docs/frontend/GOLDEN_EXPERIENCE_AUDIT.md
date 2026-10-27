# BountyCode Product Audit & Golden Experience Design

## 1. Current State: What Exists

### 1.1 Backend Canonical Systems (strong foundation)

| System | Status | Role |
|--------|--------|------|
| Journey Engine | Canonical | Composes Study + Gamification + Mastery + Readiness + Worlds + Company |
| Study Engine | Canonical | Daily plan: NEXT + REVIEW + PRACTICE + CHALLENGE |
| Concept Engine (CFIC) | Additive | Concept graph with predict/visualize/manipulate/break/transfer frames |
| Gamification | Canonical | Diamonds, level, streak, badges, tower, power-ups |
| Mastery | Canonical | Per-skill scores, skill graph |
| Readiness | Canonical | 0-100 score with 7 categories + company match |
| Repair Missions | Canonical | Targeted misconception repair with retest |
| SRS | Canonical | Spaced repetition due cards |
| World Registry | Data | World/town/level progression structure |

### 1.2 Frontend Surfaces (current inventory)

**Learning surfaces:** Learn, Practice, Target, Skills, Profile, Journey, WorldMap, LevelMap, LessonPage, SolveProblem, Concepts, UnifiedHub, QuestionBank, PracticeMode, ProblemOfTheDay, DailyChallenge, DailyDrill, CodingChallenge, AptitudeTest, SystemDesign

**Assessment surfaces:** MockOA, TcsNqtSimulation, ExamMemorySubmission, AdminExamReview, Interview, InterviewBooking, InterviewReplay

**Career surfaces:** ResumeBuilder, ResumeStudio, ATSOptimizer, ResumeATS, CareerProfile, CompanyTracks, PrepHub

**Gamification surfaces:** Tower, Leaderboard, SkillGraph, DailyChallenge, MockOA, RepairHub

**Utility surfaces:** Settings, History, NotFound, Landing, Register, Login, ForgotPassword, ResetPassword, Pricing, FreeTrial, Terms, Privacy, PwaSetup, AdminDashboard, AdminContentCorpus

### 1.3 Design System (existing)

- **Colors:** Green primary (#22C55E), adventure palette (ocean/sky/sand/wood), gold reward (#EAB74D)
- **Typography:** Manrope/Inter
- **Shadows:** Soft, minimal
- **Radii:** 16px cards, 10px buttons
- **PageShell:** 5 themes (nature, adventure, focus, celebration, spring)
- **AmbientNature:** Background component
- **Mentor:** Teacher presence component
- **Progress:** ReadinessRing, MasteryBar, TreasureBadge
- **JourneyMap:** IslandNode, PathConnector, BountyCard

---

## 2. Audit: What Feels Generic, Confusing, or Broken

### 2.1 Generic Feel
- Many screens are standard card grids with generic copy ("Learn fundamental coding concepts", "Practice by category")
- No distinctive BountyCode voice — reads like any edtech SaaS
- Teacher presence is optional/inconsistent (Mentor component exists but is not used on LessonPage, SolveProblem)
- Generic button styles, generic inputs, generic cards

### 2.2 Confusion & Noise
- **90+ routes**, many duplicate mental models:
  - `/learn`, `/learning-paths`, `/learn/:lessonId`, `/atom/:atomId`, `/atoms`, `/concepts`, `/cific`, `/cific/:conceptId`, `/problems`, `/question-bank`, `/question-bank/:questionId`, `/practice`, `/practice-mode`, `/problem-of-the-day`, `/daily-drill`, `/daily-challenge` — all lead to learning/practice
  - `/journey`, `/levels`, `/worlds`, `/level-map` — all lead to progression
  - `/mock-oa`, `/tcs-nqt`, `/exam-memory/submit`, `/coding`, `/aptitude` — all lead to assessment
  - `/resume`, `/resume-studio`, `/ats`, `/resume-ats`, `/career-profile` — all lead to career
- **Multiple navigation systems:** Navbar primary links + "More" dropdown (4 groups) + BottomNav (5 items) + page-local navigation
- **Multiple progression languages:** Journey/World/Level + Tower + Daily Challenge + SRS + Concept Graph + UnifiedHub progress
- **Multiple content sources:** World levels, CFIC concepts, Scrimba lessons, articles, question bank — accessible from multiple entry points

### 2.3 Overlapping Systems
| Overlap | Current State |
|---------|---------------|
| Learning entry | 12+ different routes lead to learning |
| Practice entry | 8+ different routes lead to practice |
| Progression display | JourneyPage, WorldMap, LevelMap, Tower, SkillGraph, ReadinessHeatmap all show progress differently |
| Content catalog | UnifiedHub aggregates 5 sources, but each source also has its own page |
| Assessment | MockOA, TcsNqtSimulation, ExamMemorySubmission, AptitudeTest, CodingChallenge, DailyChallenge, DailyDrill |
| Career | ResumeBuilder, ResumeStudio, ATSOptimizer, ResumeATS, CareerProfile, CompanyTracks, PrepHub |

### 2.4 Emotional Journey (current)
1. Landing: Excitement (sakura, adventure theme)
2. Onboarding: Clarity (3-step goal selection)
3. Today: Overwhelm (6+ optional tasks, no clear priority)
4. Journey: Confusion (pirate theme, multiple tabs, complex map)
5. World/Level: Anxiety (locked nodes, boss icons, complex navigation)
6. Lesson: Engagement (teaching loop exists but teacher is absent)
7. SolveProblem: Focus (good LeetCode-style flow)
8. Repair: Relief (teacher tips present)
9. MockOA: Stress (timer, complex UI)
10. CompanyTracks: Curiosity (but disconnected from journey)
11. Readiness: Confidence (evidence-based, but cold/dashboard-like)

**Problem:** The emotional journey is not coherent. Landing promises adventure, but inner pages feel like generic dashboards. The teacher (Mentor) appears inconsistently.

---

## 3. Genuinely Strong Existing Pieces

1. **Journey Engine** — backend already composes all systems into one canonical state
2. **Today page** — shows one clear next action (when not overloaded with optional tasks)
3. **Concept Engine (CFIC)** — real teaching loop: predict → visualize → manipulate → break → transfer
4. **Readiness Engine** — evidence-based scoring with company match
5. **Repair Missions** — targeted misconception repair with retest
6. **PageShell + AmbientNature** — established visual system
7. **Mentor component** — teacher presence (just needs to be used consistently)
8. **Sakura/adventure color palette** — distinctive identity
9. **BottomNav** — 5-item unified navigation (Journey/Practice/Target/Skills/Profile)
10. **Backend data** — concept graphs, mastery, SRS, gamification all persist correctly

---

## 4. Overlapping Pages & Duplicate Mental Models

### 4.1 Learning Surfaces (merge into ONE)
- `/learn` (UnifiedHub) → **KEEP as the single learning entry**
- `/learning-paths` → MERGE into UnifiedHub
- `/learn/:lessonId` → MERGE into UnifiedHub
- `/atom/:atomId` → MERGE into UnifiedHub  
- `/atoms` → MERGE into UnifiedHub
- `/concepts` → MERGE into UnifiedHub
- `/cific` → MERGE into UnifiedHub
- `/problems` → MERGE into Practice
- `/question-bank` → MERGE into Practice
- `/question-bank/:questionId` → MERGE into PracticeMode
- `/practice` → **KEEP as the single practice entry**
- `/practice-mode` → KEEP as the solving surface
- `/problem-of-the-day` → MERGE into Today
- `/daily-drill` → MERGE into Today
- `/daily-challenge` → MERGE into Today

### 4.2 Progression Surfaces (merge into ONE)
- `/journey` → **KEEP as the single progression view**
- `/levels` → MERGE into Journey
- `/worlds` → MERGE into Journey
- `/level-map` → MERGE into Journey
- `/tower` → MERGE into gamification sidebar in Journey
- `/skill-graph` → MERGE into Skills
- `/leaderboard` → KEEP as social feature

### 4.3 Assessment Surfaces (merge into ONE)
- `/mock-oa` → **KEEP as the single assessment entry**
- `/tcs-nqt` → MERGE into MockOA (company filter)
- `/exam-memory/submit` → MERGE into MockOA
- `/coding` → MERGE into Practice
- `/aptitude` → MERGE into Practice
- `/system-design` → MERGE into Practice

### 4.4 Career Surfaces (merge into ONE)
- `/resume` → **KEEP as Resume entry**
- `/resume-studio` → MERGE into Resume
- `/ats` → MERGE into Resume
- `/resume-ats` → MERGE into Resume
- `/career-profile` → MERGE into Profile
- `/company-tracks` → MERGE into Target
- `/prep-hub` → MERGE into Target

### 4.5 Dead/Unused Routes to Remove
- `/student-dashboard` → redirect to `/journey`
- `/my-dashboard` → redirect to `/journey`
- `/home` → redirect to `/journey`
- `/hub` → redirect to `/journey`
- `/compete` → redirect to `/mock-oa`
- `/career` → redirect to `/career-profile`
- `/prepare` → redirect to `/journey`
- `/company-mocks` → redirect to `/mock-oa`
- `/company-mocks/:testId` → redirect to `/mock-oa`
- `/analytics` → redirect to `/skills`
- `/learning` → redirect to `/learn`
- `/prep-hub` → redirect to `/target`
- `/atoms/worlds` → redirect to `/atoms`
- `/role-select` → merge into onboarding
- `/student-dashboard` → redirect to `/journey`
- `/find-my-level` → merge into onboarding
- `/diagnostic` → merge into onboarding
- `/onboarding` → merge into register flow

---

## 5. ONE Unified Product Experience

### 5.1 Product Metaphor
**"A focused learning room, not a theme park."**

The learner enters a calm, intentional space. The teacher is present. The path is clear. Progress is visible. Mistakes are expected and repaired. Gamification amplifies the learning transformation, never replaces it.

### 5.2 Visual Language
- **Palette:** Sakura/adventure restrained — soft greens, warm golds, gentle blues, muted earth tones
- **Background:** AmbientNature only (no particles, no neon, no glassmorphism everywhere)
- **Cards:** Minimal borders, soft shadows, no gradients on every card
- **Typography:** Manrope for headings, Inter for body, mono for data
- **Teacher presence:** Mentor component on every learning screen, not decorative
- **Progress:** ReadinessRing/MasteryBar always visible, not hidden in dropdowns

### 5.3 Interaction Language
- **One primary action per screen** — no competing CTAs
- **Teacher-guided loop:** Show → Try → Fail → Explain → Repair → Succeed
- **Mistakes are normal** — failure states are gentle, not punishing
- **Repair is automatic** — when a concept fails, the system offers targeted repair
- **Feedback is specific** — "You forgot to initialize the accumulator" not "Wrong answer"

### 5.4 Gamification Philosophy
- **Gamification amplifies learning, never replaces it**
- Diamonds = proof of capability
- Level = growth
- Streak = commitment
- Repair = recovery, not punishment
- No confetti on every action — only on mastery/unlock

### 5.5 Motion Philosophy
- **Restrained:** Entrance only, not every element
- **Teacher transitions:** Gentle, not bouncy
- **Progress always animates forward**
- **Celebration only on mastery/unlock**

---

## 6. THE GOLDEN EXPERIENCE: 30-Minute Beginner Journey

### Flow
```
NEW STUDENT (near-zero Python experience)
↓
LANDING — "From your first line of code to your first offer."
↓ One CTA: "Start Learning"
↓
REGISTER — email + password only
↓
ONBOARDING — 3 steps:
  1. "What's your goal?" → Learn to code / Get placed / Switch careers
  2. "Pick your language" → Python / JavaScript / Java / C++ / Not sure
  3. "Any target company?" → Optional
↓
TODAY — ONE clear mission:
  "Today: Learn variables in Python"
  - Estimated time: 15 min
  - Reward: 50 diamonds
  - One button: "Start"
↓
JOURNEY — see progress, enter active world
  - Current world highlighted
  - One button: "Continue"
↓
WORLD — concept map
  - Current concept glowing
  - One button: "Start Concept"
↓
CONCEPT FRAME (teaching loop):
  Phase 1: PREDICT — "What will this code output?"
  Phase 2: VISUALIZE — step-by-step execution with teacher narration
  Phase 3: MANIPULATE — change a value, rerun, observe
  Phase 4: BREAK — introduce a bug, diagnose it, fix it
  Phase 5: TRANSFER — apply in new context
↓
INTERACT — Monaco editor, teacher feedback panel
↓
MAKE MISTAKE — bug introduced, teacher explains why
↓
REPAIR — guided fix, retest
↓
SOLVE INDEPENDENTLY — transfer challenge
↓
MASTERY — score, diamonds, level up animation
↓
UNLOCK — next concept revealed, tomorrow's mission set
```

### Emotional Arc
1. **Curiosity** (Landing: "I want to try this")
2. **Commitment** (Onboarding: "I'm doing this")
3. **Clarity** (Today: "I know exactly what to do")
4. **Focus** (Journey → World → Concept: "I'm in the right place")
5. **Discovery** (Predict: "I think I know...")
6. **Understanding** (Visualize: "Oh, that's how it works")
7. **Agency** (Manipulate: "I can change it")
8. **Resilience** (Break → Repair: "I can fix mistakes")
9. **Mastery** (Transfer: "I can do this alone")
10. **Motivation** (Unlock: "What's next?")

### Anti-Generic Test Results
- **Could this belong to another edtech company?** NO — sakura/adventure + teacher presence + concept graph is unique
- **Could this belong to a generic SaaS dashboard?** NO — every screen is teacher-guided, not data-dump
- **Could this interaction exist in any coding website?** NO — predict/visualize/manipulate/break/transfer is specific to BountyCode
- **Would the learner remember this screen tomorrow?** YES — the teaching loop is memorable

---

## 7. Implementation Plan: ONE Golden Flow

### Phase 1: Define the canonical surfaces
1. **Landing** — already strong, keep as-is
2. **Onboarding** — already strong, keep as-is
3. **Today** — simplify to ONE mission, remove optional clutter
4. **Journey** — keep as progression hub
5. **Concept Frame** — the teaching loop (predict/visualize/manipulate/break/transfer)
6. **Repair** — integrate into Concept Frame, not separate hub

### Phase 2: Build the golden flow
1. Create a **single learning shell** that wraps all concept interactions
2. Build the **5-phase teaching loop** UI (predict → visualize → manipulate → break → transfer)
3. Integrate **Mentor** into every phase
4. Build **Repair** as an automatic overlay, not a separate page
5. Build **Mastery** celebration that feels earned, not decorative

### Phase 3: Connect to backend
1. Use **Journey Engine** as the single source of truth for "what next"
2. Use **Concept Engine** for the teaching loop content
3. Use **Readiness Engine** for progress display
4. Use **Gamification** for diamonds/level/streak

### Phase 4: Remove duplicates
1. Remove duplicate routes
2. Remove duplicate navigation
3. Remove duplicate progression displays

---

## 8. What NOT To Do

- Do NOT add more components, more animation, more gamification
- Do NOT rebuild the engine — reuse Journey Engine, Concept Engine, Readiness Engine
- Do NOT create new abstractions — use existing canonical systems
- Do NOT add confetti, particles, neon, glassmorphism everywhere
- Do NOT make every screen a dashboard
- Do NOT protect features because engineering time was spent

---

## 9. Success Criteria

The golden flow is done when:
1. A beginner can complete the 30-minute journey without confusion
2. Every screen feels like BountyCode, not another edtech site
3. The teacher is present on every learning screen
4. Mistakes are expected and repaired automatically
5. Progress is visible and meaningful
6. The learner wants to come back tomorrow

**The question is NOT: "Is the UI beautiful?"**
**The question is: "Does BountyCode feel like a completely different category of learning product?"**
