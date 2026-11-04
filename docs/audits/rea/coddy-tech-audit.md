# REA Audit: Coddy.tech (Reverse-Engineered)

Source: `https://coddy.tech` (homepage + `/brand/colors` + `/brand/logo`)
Method: Static web analysis (REA `analyze-web-bundle` + manual inspection)
Date: 2026-11-04

## 1. Brand Identity

| Element | Value |
|---|---|
| Brand name | Coddy |
| Tagline | "Elevating code learning to a daily hobby" |
| Learners | 5,996,625 in 202 countries |
| Submissions | 90,893,790 (live counter) |
| Characters | Bit (ant-robot mascot, logo head), Bugsy (AI tutor, magenta) |
| Learners called | "codders" |
| Rating | 4.9 App Store (2K+), 4.8 Google Play (8K+) |

## 2. Color Palette (coddy.tech/brand/colors)

### Brand colors (semantic, never decorative)

| Name | Hex | Usage |
|---|---|---|
| Coddy Blue | `#29ABE2` | Logo, Bit, links, accents (light & dark) |
| Coddy Blue (dark) | `#34B4E4` | Same blue lifted for dark backgrounds |
| Button blue | `#0077FF` | Primary buttons on web, light theme |
| Button shadow | `#005DC8` | Pressed edge under button blue |
| Deep blue | `#007ACCC` | Secondary buttons and links |
| Button blue (dark) | `#1B78A0` | Primary buttons on dark backgrounds |

### Semantic product colors (each means something — never decorative)

| Name | Hex | Meaning |
|---|---|---|
| Streak | `#E85A18` | Streak flame, daily streak moments |
| Score | `#FCAD00` | XP, score, coins, gems |
| Energy | `#3E39B8` | Energy bolt, daily limit |
| Pro | `#CF7F26` | Coddy Pro / premium features |
| Success | `#05B20C` | Passed tests, done lessons, correct answers |
| Hearts | `#FF4B4B` | Hearts and lives |
| Streak freeze | `#69AEFF` | Frozen streak saving a missed day |

### Bugsy (AI tutor only)

| Name | Hex | Usage |
|---|---|---|
| Bugsy Magenta | `#D31D65` | Bugsy and AI tutor features only |

### Backgrounds

| Name | Hex | Usage |
|---|---|---|
| White | `#FFFFFF` | Light theme background |
| Mist | `#F1F5F9` | Cards and secondary surfaces (light) |
| Sky wash | `#DDF4FF` | Light blue landing sections |
| Charcoal | `#252627` | Dark theme background |
| Graphite | `#2D2E2F` | Cards on dark |
| Editor | `#1E1E1E` | Code editor background |

### Gradients

| Name | Stops | Usage |
|---|---|---|
| Light Sky | `#26A8E4 · #037BFD` | Hero sections, big moments (light) |
| Dark Sky | `#072031 · #07314E` | Same after sunset |

### Button design principle

Buttons sit on a darker shadow that presses down when tapped (tactile affordance).

## 3. Gamification Model

Coddy's core loop (from homepage: "Every lesson counts"):

```
Streaks → Levels → Weekly leagues → Quests → Friends → Missions → Badges → Chests → Personalization
```

### Streak
- Fire icon, day counter ("24 day streak")
- "Return tomorrow to keep your streak!"
- Streak freeze available (saves a missed day)

### Level
- Number badge next to language icon (e.g., "7" by Python)
- Tier labels: Novice → Learner → Coder → Engineer → Architect → Master → Grandmaster

### Score / XP
- Gold coin icon, numeric counter ("250")
- XP, score, coins, gems all share gold color

### Energy
- Blue-purple bolt icon ("5")
- Daily limit mechanic

### Journey (hex-based learning map)
States per hex tile:
- **Done**: `hex-done-base/shadow/top` + `lesson-done` icon, green checkmark
- **Active**: `hex-active-base/shadow/top` + `lesson-theory-challenge` icon
- **Locked**: `hex-locked-base/shadow/top` + `lesson-theory-challenge` icon, 🔒 overlay

Path arrows between tiles: `path-right`, `path-left` (done variants exist)

Lesson types: `lesson-done`, `lesson-theory-challenge`, `lesson-all`

### Sidebar navigation
Journey · Goals (daily challenges) · Leaderboard · Profile

### Certificates
- Verifiable, shareable, unique ID (e.g., `SE1-PATH`)
- Signed by CTO, dated
- PDF download, LinkedIn-ready
- Seal badge, double top border (score gold → coddy blue gradient)

## 4. Product Architecture

### Navigation (5 primary tabs)
Catalog · Playground · Tools · Resources · Company

### Content domains (20+ languages + school subjects)
Programming (Python, JS, TS, Java, C++, C, C#, Go, Ruby, Kotlin, Lua, Luau, GDScript, Dart, Rust, Arduino, Verilog, Solidity, Assembly), Web (HTML, CSS, React, TypeScript, Next.js, PHP, Django), Mobile (Flutter, Swift, SwiftUI), Games (Unity, Godot, Pygame, Roblox/Luau), Data & AI (SQL, R, Excel, ML, AI Prompts), Systems (Terminal, Git, Docker, Kubernetes), Math, Physics, Chemistry, Chess, Cybersecurity

### Learning format
- Interactive in-browser code editor with test cases
- Bugsy AI tutor (hints, never answers)
- Visualizations (algorithms, data structures)
- Arcade (games made with code)
- Playgrounds (run code in browser)

### Monetization
- Free to start (dozens of courses)
- Optional Coddy Pro premium plan
- Certificates for completed courses
- Mobile app (iOS/Android) with synced progress/streak/tokens

## 5. What BountyCode Adopted

From this audit, BountyCode's gamification was rebuilt to match coddy.tech semantics:

| BountyCode element | coddy.tech source | Hex |
|---|---|---|
| Brand primary | Coddy Blue | `#29ABE2` |
| Streak flame / counter | Streak | `#E85A18` |
| XP / score counter | Score | `#FCAD00` |
| Energy bolt | Energy | `#3E39B8` |
| Premium tier | Pro | `#CF7F26` |
| Passed tests / done lessons | Success | `#05B20C` |
| Hearts / lives | Hearts | `#FF4B4B` |
| Frozen streak | Streak freeze | `#69AEFF` |
| Bugsy / AI tutor | Bugsy Magenta | `#D31D65` |
| Journey hex states | Done / Active / Locked | Success / Coddy / Slate |
| Certificate seal | Score gold | `#FCAD00` |
| Navbar primary button | Button blue | `#0077FF` |

Files changed: `tailwind.config.js` (coddy color safelist), `components/gamification/palette.ts`, `Streak.tsx`, `GamificationWidget.tsx`, `Badge.tsx`, `Chest.tsx`, `Certificate.tsx`, `JourneyTile.tsx`, `GamificationDashboard.tsx`.
