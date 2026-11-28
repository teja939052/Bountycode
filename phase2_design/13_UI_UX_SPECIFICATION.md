# 13 UI/UX PRODUCT SPEIFICATION

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the complete UI/UX product specification for BountyCode — from the learner's first visit to long-term readiness. This document covers all screens, information architecture, navigation, layouts, editors, editors, assessment experience, feedback states, accessibility, responsive layouts, and loading/error/empty/offline states.

The pirate theme makes the experience memorable without compromising clarity or usability. The product must be clear, fast, accessible, and polished.

This is a design document. No implementation is authorized.

---

## 2. Design System Principles

### 2.1 Core Principles

| Principle | Application |
|-----------|-------------|
| Mobile-first | Most users are on phones with inconsistent connections |
| Lean over decorative | Animation never blocks navigation; content loads fast |
| Accessibility first | Keyboard navigable, reduced motion, sufficient contrast, screen-reader labels |
| Clear over cute | Pirate theme enhances, never obscures, the learning task |
| State clarity | Every screen has an obvious state: loading, empty, error, success, offline |
| Feedback immediacy | Every student action receives visible, server-confirmed feedback |

### 2.2 Color Vocabulary (State Colors)

| Color | Meaning | Usage |
|-------|---------|-------|
| Gold (#D4A843) | Done / completed | Completed lessons, mastery achieved |
| Green (#22C55E) | Current / active | Current lesson, active step |
| Muted (#9CA3AF) | Locked | Locked levels, unavailable actions |
| Sky-dash (#3B82F6) | Recovered / repaired | Post-repair success, weakness addressed |
| Red (#EF4444) | Error | Form validation, server errors |
| Amber (#F59E0B) | Warning | Hints available, partial progress |
| Slate (#6B7280) | Neutral | Secondary text, placeholders |

### 2.3 Typography

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| Headline | 1.5rem | 700 | Page titles |
| Subhead | 1.125rem | 600 | Section titles |
| Body | 1rem | 400 | Main text |
| Caption | 0.875rem | 400 | Helper text |
| Small | 0.75rem | 400 | Captions, metadata |
| Monospace | 0.875rem | 500 | Code, terminal output |

### 2.4 Motion

| Motion | Rule |
|--------|------|
| Page transitions | Fast, under 300ms, no layout shift |
| Animations | Optional; respect `prefers-reduced-motion` |
| Sound | Optional, mutable, never the only information channel |
| Flashing effects | None |
| Loader | Visible for actions > 300ms; skeleton for content > 500ms |

---

## 3. Information Architecture

### 3.1 Top-Level Hubs (6 hubs, nothing else)

| Hub | Purpose | Screens |
|-------|---------|---------|
| Journey | Guided learning path, worlds, lessons, repair branches, SRS | World map, level view, lesson player |
| Practice | Question bank, patterns/topics, compiler/playground | Browse, solve, editor, hints |
| Mock OA | Timed company-templated assessments | Company selection, timed test, results |
| AI Interview | Behavioral/HR/Technical/System Design/GD sessions | Interview setup, session, feedback |
| Company Tracks | Per-company blueprints, verified prep paths | Company page, syllabus, mock |
| Profile | Rank, badge, readiness score, streak, settings | Profile, settings, career tools |

Resume/ATS/Applications live under Profile, not top-level. Admin/auth/legal are unrouted utility pages.

### 3.2 Screen Inventory

| Screen | Path | State Variants | V1 Status |
|--------|------|-------------|-----------|
| Landing | `/` | Loading, empty, error | V1 |
| Onboarding | `/onboarding` | Step 1-4, complete | V1 |
| Dashboard | `/dashboard` | Loading, empty, error | V1 |
| Journey | `/journey` | Loading, empty, error | V1 |
| World map | `/learn/world/:id` | Loading, locked, unlocked | V1 |
| Level view | `/learn/world/:id/level/:id` | Loading, locked, in-progress, complete | V1 |
| Lesson player | `/learn/world/:id/level/:id/lesson/:slug` | Loading, idle, correct, incorrect, hint, complete | V1 |
| Practice | `/practice` | Loading, empty, error | V1 |
| Problem solve | `/problems?topic=:topic` | Loading, idle, correct, incorrect, compile-error | V1 |
| Compiler/playground | `/compiler` | Idle, running, error, output | V1 |
| Mock OA | `/companies/:slug/mock` | Loading, in-progress, complete, results | V1 |
| Company page | `/companies/:slug` | Loading, empty, error | V1 |
| Company practice | `/companies/:slug/practice` | Loading, idle, correct, incorrect | V1 |
| Evidence dashboard | `/evidence` | Loading, empty, error | V1 |
| Readiness dashboard | `/companies/:slug/readiness` | Loading, insufficient, ready | V1 |
| Profile | `/profile` | Loading, empty, error | V1 |
| Settings | `/profile/settings` | Idle, saving, error | V1 |
| Repair mission | `/repair/:skill` | Loading, idle, correct, incorrect | V1 |
| AI Interview | `/interview` | Loading, in-progress, complete, feedback | Roadmap (top-level hub visible, feature gated) |
| SQL editor | `/compiler/sql` | Loading, idle, correct, incorrect, query-error | Roadmap |
| Resume builder | `/resume` | Idle, generating, error | Roadmap |
| ATS optimizer | `/ats` | Idle, analyzing, result | Roadmap |

### 3.3 Navigation

| Level | Component | Behavior |
|-------|-----------|----------|
| Top-level | Hub switcher (6 hubs) | Persistent on all hub pages |
| Secondary | World/level selector | Collapsible on mobile |
| Tertiary | Lesson step navigator | Previous/Next disabled when not applicable |
| Contextual | Captain Byte | Floating, dismissible, optional |
| User | Profile/settings | Dropdown or bottom sheet on mobile |

---

## 4. Critical Screens

### 4.1 Onboarding

**Purpose:** Collect only information that meaningfully changes the journey.

**Screens:**
1. Welcome + value proposition
2. Year/experience band
3. Target company (or "not sure yet")
4. Preferred language (if supported)
5. Current preparation level / baseline
6. Daily time budget (minutes available per day)
7. First mission recommendation

**Mobile rules:**
- One question per screen
- Large tap targets (44px minimum)
- Clear progress indicator
- Skip where appropriate

**Exit state:** Student reaches a useful activity quickly (target → blueprint → first mission).

### 4.2 Landing Page

**Purpose:** Communicate value and drive signup.

**Sections:**
- Hero: "From your first line of code to your first offer."
- Diagnose → Learn → Practice → Get Hired strip
- World preview (6 worlds)
- Pricing (free + pro + lifetime)
- CTA: Get started

**Mobile rules:**
- Hero text readable at 320px
- CTA button full-width, thumb-reachable
- No horizontal scroll

### 4.3 World Map (Journey)

**Purpose:** Show progress through worlds and levels.

**Layout:**
- World selector (6 worlds)
- Level nodes with lock state (gold=done, green=current, muted=locked, sky-dash=recovered)
- Progress bar per world
- Boss islands at milestone levels (10, 20, 30...)
- Captain Byte floating widget

**Mobile rules:**
- Horizontal scroll for world list (visual indicator)
- Level nodes as circular buttons
- Progress bar as thin line beneath world name

### 4.4 Level View

**Purpose:** Show lessons within a level and prerequisites.

**Layout:**
- Level title and description
- Prerequisite chain (which levels must be complete)
- Lesson cards with lock state
- Estimated time per lesson
- XP reward per lesson

**Mobile rules:**
- Lesson cards as full-width rows
- Prerequisite chain as horizontal scroll
- Lock state obvious (grayed + lock icon)

### 4.5 Lesson Player

**Purpose:** Deliver the seven-beat interactive experience.

**Layout:**
- Header: Lesson title, progress, time estimate, hints remaining
- Main: Lesson content (varies by beat stage)
- Sidebar: Captain Byte, hints, progress
- Footer: Previous/Next (disabled when not applicable), submit answer

**Beat Stage Layouts:**
| Stage | Main Content | Interaction |
|-------|-------------|-------------|
| Explain | Text + narration | Read |
| See | Animation / visualization | Watch |
| Interact | Manipulable component | Drag/tap/select |
| Predict | Question + input field | Commit answer |
| Solve | Code editor / answer field | Build solution |
| Break | Broken example | Identify defect |
| Debug | Fix interface | Fix code |
| Recall | SRS prompt | Answer retrieval |
| Transfer | Changed context problem | Independent solution |
| Prove | Timed check | Formal assessment |

**Mobile rules:**
- Code editor has responsive height (min 200px)
- Input fields full-width
- Primary action reachable without scrolling
- Timer visible without blocking content
- Result state obvious (green/red/amber)

### 4.6 Code Editor (Practice Console)

**Purpose:** Write and execute code in C, C++, Python, Java.

**Layout:**
- Language selector (top-left)
- Editor area (Monaco, responsive height)
- Run/Submit buttons (primary, right)
- Output panel (bottom, collapsible)
- Test case results (pass/fail per case)
- Error panel (compile/runtime errors)

**Mobile rules:**
- Keyboard avoids editor (resize, not overlay)
- Run button thumb-reachable
- Output panel scrollable
- Font size adjustable

### 4.7 SQL Practice Environment

**Purpose:** Write and execute SQL queries.

**Layout:**
- Schema browser (left, collapsible)
- Query editor (center)
- Run button (primary)
- Result table (bottom)
- Explain plan (optional, advanced)

**Mobile rules:**
- Schema browser collapses on mobile
- Result table scrollable horizontally
- Query editor responsive height

### 4.8 Mock OA

**Purpose:** Timed company-templated assessment.

**Layout:**
- Header: Company name, section, timer (server-truth), question counter
- Main: Question content + answer input
- Sidebar: Question navigation, flag question, time remaining
- Footer: Submit section, next section, finish mock

**Mobile rules:**
- Timer prominent at top
- Question counter visible
- Submit section confirmation dialog
- Section timer server-truth (client is suggestion only)

### 4.9 Results / Diagnosis

**Purpose:** Show assessment results and weakness diagnosis.

**Layout:**
- Overall score and readiness
- Section breakdown
- Weakness heatmap
- Failure reasons (timeout vs wrong answer vs runtime error)
- Repair recommendations
- Retest CTA

**Mobile rules:**
- Score prominent at top
- Weakness cards full-width
- Repair CTA thumb-reachable

### 4.10 Repair Mission

**Purpose:** Targeted practice on identified weakness.

**Layout:**
- Misconception explanation
- Broken example (for debugging)
- Fix interface
- Test case results
- Independent retest CTA

**Mobile rules:**
- Broken code full-width
- Fix input full-width
- Test results clear pass/fail

### 4.11 Evidence Dashboard

**Purpose:** Show learning evidence and progress.

**Layout:**
- Heatmap (daily activity)
- Skill breakdown (accuracy per skill)
- Failure reasons (timeout vs wrong answer vs runtime error)
- Forgetting curve (SRS schedule)
- Time-to-solve trend
- Personal records (fastest solve, streak)

**Mobile rules:**
- Heatmap as weekly row
- Skill cards full-width
- Charts simplified for mobile

### 4.12 Readiness Dashboard

**Purpose:** Show company placement readiness.

**Layout:**
- Target company selector
- Overall readiness score
- Coverage percentage
- Section/skill breakdown
- Blockers
- Strongest/weakest skills
- Trend
- Last mock
- Next action
- Repair CTA
- Retest status

**Mobile rules:**
- Score prominent at top
- Section cards full-width
- Next action thumb-reachable

### 4.13 Profile

**Purpose:** Show learner profile and settings.

**Layout:**
- Rank badge (Deckhand → Lookout → Navigator → First Mate → Captain → Fleet Admiral)
- Streak display
- Badges
- Skill/evidence summary
- Recent activity
- Settings

**Mobile rules:**
- Rank badge prominent
- Streak visible
- Settings as list

---

## 5. Component Library

### 5.1 Buttons

| Variant | Usage | States |
|---------|-------|--------|
| Primary | Main action (submit, next, start) | Default, hover, active, disabled, loading |
| Secondary | Secondary action (back, cancel) | Default, hover, active, disabled |
| Tertiary | Minimal action (hint, skip) | Default, hover, active, disabled |
| Danger | Destructive (delete, reset) | Default, hover, active, disabled |

**Mobile rules:** Primary buttons full-width; secondary as text links where possible.

### 5.2 Input Fields

| Type | Usage | Validation |
|------|-------|------------|
| Text | Short answers | Real-time validation |
| Number | Numeric answers | Range check |
| Select | Multiple choice | Keyboard accessible |
| Textarea | Long answers | Auto-resize |
| Code | Code editor | Syntax highlighting, lint |

**Code editor language support:** The editor supports C, C++, Python, and Java syntax highlighting. However, language-specific learning tracks (beyond pseudocode) are Roadmap per the Vision Lock. The editor is available for practice but language-specific lesson content is Roadmap.


### 5.3 Cards

| Variant | Usage |
|---------|-------|
| Lesson card | Lesson title, time, XP, lock state |
| Skill card | Skill name, level, accuracy, trend |
| Company card | Company name, blueprint, readiness |
| Badge card | Badge icon, name, earned date |
| Mission card | Mission title, reward, status |

### 5.4 Feedback States

| State | Visual | Interaction |
|-------|--------|-------------|
| Loading | Skeleton + spinner | No interaction |
| Empty | Illustration + CTA | Primary action visible |
| Error | Red banner + retry | Retry action visible |
| Success | Green check + message | Auto-dismiss or dismissible |
| Offline | Banner + cached content | Limited functionality |

---

## 6. Mobile QA Viewports

| Viewport | Use |
|----------|-----|
| 320px | Sanity check / no catastrophic overflow |
| 390px | Primary launch QA |
| 430px | Primary launch QA |
| Desktop | Regression |

### 6.1 Mobile Rules

- No essential content hidden behind horizontal scroll
- Code editors have responsive height
- Primary action remains reachable
- Timers visible without blocking content
- Result state obvious (green/red/amber)
- Animation never blocks navigation

### 6.2 Critical Screens for Mobile QA

- Onboarding
- Company blueprint
- Journey
- Interactive lesson
- Code editor
- Mock
- Result/diagnosis
- Repair
- Readiness dashboard

---

## 7. Captain Byte Integration

### 7.1 UI Placement

| Location | Behavior |
|----------|----------|
| Bottom-right floating widget | Dismissible, optional |
| Lesson header | Small avatar + text |
| Mission intro | Full-width banner |
| Error state | Contextual message |

### 7.2 Captain Byte States

| State | Visual | Animation |
|-------|--------|-----------|
| Idle | Character neutral | None |
| Speaking | Character + text bubble | Text appears character-by-character |
| Thinking | Character + thinking dots | Dots pulse |
| Celebrating | Character + confetti | Confetti bursts |
| Error | Character + concerned expression | Shake |

### 7.3 Accessibility

- All spoken text available as ARIA labels
- Character is decorative (aria-hidden)
- Text bubble has sufficient contrast
- No animation as only information channel

### 7.4 Conversational Chat UI

| Element | Behavior |
|---------|----------|
| Chat panel | Dockable bottom-right panel, dismissible |
| Message bubble | Student messages left-aligned, tutor messages right-aligned with avatar |
| Typing indicator | Shows when Captain Byte is generating a response |
| Message history | Scrollable within current lesson session only |
| Input field | Bottom of chat panel, Enter to send |
| Submit button | Disabled when input is empty |
| Error state | Red border + inline error message |
| Empty state | "Start a conversation" placeholder text |

### 7.5 Optimistic vs Server-Confirmed Feedback

| Interaction | UI Behavior | Server Confirmation |
|-------------|-------------|---------------------|
| Answer submission | Immediate visual feedback (green/red/amber) | Server verdict overrides client prediction |
| Code execution | Loading state → result display | Server result replaces optimistic prediction |
| Hint request | Immediate hint display | Server-validated hint content |
| Lesson completion | Celebration animation | Server-confirmed completion unlocks next lesson |
| Mastery achievement | Confetti + badge | Server-verified mastery claim |

**Rule:** Optimistic UI feedback is allowed for responsiveness, but all final decisions (correctness, mastery, readiness, next action) must be server-confirmed. The client never unilaterally declares correctness or mastery.

---

## 8. Gamification UI

### 8.1 Rank Badge

| Rank | Visual | Unlock Condition |
|------|--------|------------------|
| Deckhand | Gray badge | Onboarding complete |
| Lookout | Bronze badge | First lesson complete |
| Navigator | Silver badge | First mock complete |
| First Mate | Gold badge | First repair complete |
| Captain | Platinum badge | Readiness ≥ 70% |
| Fleet Admiral | Diamond badge | Readiness ≥ 90% |

### 8.2 Streak Display

- Flame icon + day count
- "X day streak" text
- Freeze option (one per month)

### 8.3 Reward Display

- What was demonstrated
- Reward earned (diamonds)
- Progress change
- Next unlock
- Next action

**Mobile rules:**
- Reward celebration under 900ms
- `prefers-reduced-motion` fallback
- No excessive particles

---

## 9. Accessibility Specification

| Requirement | Implementation |
|-------------|---------------|
| Keyboard navigation | All interactive elements reachable via Tab |
| Focus visible | Clear focus outline on all interactive elements |
| Screen reader | ARIA labels on all interactive elements; live regions for dynamic content |
| Color contrast | WCAG AA minimum (4.5:1 for normal text, 3:1 for large text) |
| Non-color-only | State communicated by text + icon, not color alone |
| Reduced motion | `prefers-reduced-motion` respected; animations optional |
| Text resize | Up to 200% without loss of functionality |
| Touch targets | Minimum 44px × 44px |
| Language | Clear, simple English (CEFR B1 target) |

---

## 10. Loading / Empty / Error / Offline States

### 10.1 Loading State

**Visual:** Skeleton + spinner
**Interaction:** No interaction with loading content
**Message:** "Loading..." or context-specific

### 10.2 Empty State

**Visual:** Illustration + primary CTA
**Interaction:** Primary action visible and prominent
**Message:** Context-specific (e.g., "No lessons available yet", "Start your first mission")

### 10.3 Error State

**Visual:** Red banner + retry button
**Interaction:** Retry action visible and prominent
**Message:** Human-readable error (not technical)

### 10.4 Offline State

**Visual:** Offline banner + cached content
**Interaction:** Limited functionality; cached content readable
**Message:** "You're offline. Some features may not work."

---

## 11. Interaction Feedback

| Action | Feedback | Timing |
|--------|----------|--------|
| Submit answer | Immediate visual (green/red/amber) | < 100ms |
| Submit code | Loading → result | < 2000ms typical |
| Complete lesson | Celebration + progress update | < 500ms |
| Earn reward | Juice animation | < 900ms |
| Unlock level | Confetti + badge | < 1000ms |
| Network error | Banner + retry | Immediate |
| Server error | Banner + retry | Immediate |

---

## 12. Pirate Theme Application

| Element | Pirate Treatment | Usability Rule |
|---------|---------------|----------------|
| Rank badges | Deckhand → Fleet Admiral | Clear progression; no confusion |
| Captain Byte | Tutor character | Optional; doesn't block content |
| Missions | Voyage/map framing | Clear objective; not decorative |
| Unlocks | Island/town unlocking | Clear prerequisite chain |
| XP/Diamonds | Treasure theme | Server-authoritative; no client calculation |
| Streak | Voyage continuity | No streak-guilt; no fake scarcity |
| Leaderboards | Fleet ranking | Optional; not paywall |

**Rule:** Pirate theme enhances memorability without compromising clarity, speed, accessibility, or polish.

---

## 13. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Mobile-first design? | Yes |
| 2 | All critical screens covered? | Yes |
| 3 | Loading/empty/error/offline states defined? | Yes |
| 4 | Accessibility requirements met? | Yes |
| 5 | Responsive viewports defined? | Yes |
| 6 | Pirate theme doesn't compromise usability? | Yes |
| 7 | Captain Byte integration defined? | Yes |
| 8 | Gamification UI defined? | Yes |
| 9 | Interaction feedback timing defined? | Yes |
| 10 | Design system consistent? | Yes |

---

**End of 13 UI/UX Product Specification**
