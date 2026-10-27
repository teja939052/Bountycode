# HYBRID_BLUEPRINT.md — Brilliant × Mimo × Codecademy × boot.dev × Coddy hybrid

**Status:** research complete (web search, Sept 2026) · repo audit complete · build order below
**User directive:** hybrid of brilliant.org + mimo.org + codecademy + boot.dev + coddy.tech — do not author a
new curriculum; reuse curricula that already work, orchestrate them under our feature set into a
service-based product. Some portions already added, not complete.

---

## 1. The hybrid formula (what we take from each)

| Layer | Source platform | What we copy (mechanic, not content) |
|---|---|---|
| **Content unit structure** | Brilliant | `Course → Level → Lesson` (5–10 min, ~5 interactive problems + Skills Check per lesson, level review of 10–15 problems, course = 10–15 levels). Learning Path = ordered courses with checkpoints. No videos — interactive problems only. |
| **Lesson format + habit** | Mimo | Write real code from lesson 1; micro-lesson + instant check; streaks/goals; "career path = N sections + portfolio projects"; AI explains errors in context. |
| **Path orchestration + employability** | Codecademy | Skill Path vs Career Path (units → lessons → projects → quizzes, with milestones); certification exams; **job-readiness checker** (AI match of skills vs JD); AI assistant that knows the current course context. |
| **Depth + pass/fail practice** | boot.dev | Every lesson is a **pass/fail autograded assignment** (2–10 min); track → courses → chapters → lessons; difficulty score derived from attempts/solution-views/AI-chats; Socratic AI tutor (never reveals answer); lesson **reset without re-XP**; personal projects + capstone; auto-generated "spellbook" cheat-sheet pages; free preview, content-only mode behind the gate. |
| **Free acquisition + credentials** | Coddy | All courses free with a **daily energy limit**; in-browser execution (we already have Piston); **verifiable certificate per course** (unique ID + public URL, one-click LinkedIn); streak freeze days; split-screen lesson/editor/terminal; hidden unit tests; **roadmap pages built from existing courses** (SEO); quiz → auto-built guided path. |
| **Tutor (all three)** | Brilliant Koji / boot.dev Boots / Coddy Bugsy | One tutor, reads lesson context + the student's code, guides reasoning, never dumps the answer. We already have AI mentor + golden `MentorGuide`/`MentorCallout` components — needs to become THE tutor of the lesson runtime. |

Free-tier mechanics already exist in BountyCode (tier middleware, daily/monthly limits, hints,
XP/streak/badges). Coddy's *energy* ≈ our usage limits; boot.dev's *gem costs for hints/solutions* is
the one economy mechanic we don't have yet.

## 2. What the repo already has (your added portions)

**Backend canonical layer — DONE and additive:**
- `services/unified_catalog.py` (474 ln) — adapter translating **5 content sources** into one
  `LessonDefinition/Step` schema: vertical slices (`slice::`), CFIC concepts (`cfic::`), world levels
  (`worlds::`), Scrimba lessons (`scrimba::`), study articles (`article::`).
- `services/unified_learning.py` (329 ln) — **single write path**: `POST /activity` fans out to
  `record_practice()` (Gamification Law-compliant) + mastery engine + SRS + `learning_events`.
- `routes/unified_learning.py` — `/api/v1/unified/{lessons, activity, progress, catalog/stats,
  lessons/{id}/metaphor, lessons/{id}/intuition}`.

**Frontend IA — DONE:**
- 5 environments: `/lab` (UnifiedHub), `/arena`, `/world`, `/command`, `/career` + shells +
  `AppShell`/`EnvironmentEntry`; `ENV_REDIRECTS` maps ~50 legacy paths (all targets registered ✅).
- `GoldenFlow` concept player, `LessonPlayer`, `MentorGuide`/`RepairOverlay` golden components.
- `pages/Scrimba`, `uiverse/` component library, design tokens (F1 pass complete).

## 3. What's incomplete (audit findings)

### P0 — broken/empty product surface (user: "still empty and worst")
1. **26 orphan pages** — exist, not reachable from any route. Includes the hybrid portions you added:
   `Scrimba`, `LearnLesson`, `LearnTrack` (boot.dev-style track), `BeginnerLaunch`, `DevLaunch`,
   `Prepare`, `Home`, `WorldMap`, `StudyLibrary`, `LanguageJourney`, `LearningModules`, `ProblemDetail`,
   `StudyGroups`, `CompanyExam`, `CompanyPrepHub`, `TcsNqtPrep`, `CoverLetter`, `Predictor`, `Analytics`,
   `MyAssignments`, `PersonalDashboard`, `AdaptivePath`, `VariableDiscovery`, `PatternAnimations`,
   `LessonView`, `Compete`. → wire each into the 5-env IA or delete if superseded.
2. **Duplicate route `/arena`** registered twice (React Router picks one).
3. `AdaptivePath.tsx` is **UTF-16 encoded** — risk for esbuild; re-save as UTF-8.
4. Only `UnifiedHub` calls `/api/v1/unified/*` — `LessonPlayer`/`GoldenFlow` still write progress via
   legacy paths, so the "single write path" is not actually the only one yet.

### P1 — catalog too small for a "hybrid curriculum"
5. Catalog covers 5 sources only. **Not wired:** `language_paths` (7 langs × 100 levels × 80 modules),
   `learning_modules`, question bank (Arena problems), company tracks, mock-OA sets, Sheets.
6. Catalog is a **flat lesson list** — no Brilliant-style `Path → Course → Level → Lesson` hierarchy and
   no boot.dev-style `Track → Course → Chapter → Lesson`. Needs a `structure` payload on
   `/catalog/stats` + grouping in `UnifiedHub`.

### P2 — mechanics from the reference sites that don't exist yet
7. **Verifiable certificates** (Coddy/Codecademy): per-course completion → unique ID + public verify URL.
   No certificate system exists.
8. **Roadmap pages** (Coddy `/landing/software-engineer`): SEO pages composed of existing courses.
   None exist.
9. **Lesson reset without re-XP** (boot.dev; 11.7% of submissions are resets) — absent.
10. **Hint/solution costs** (boot.dev gems) — hints are free today.
11. **Spellbook** (boot.dev): condensed auto-notes per lesson — absent (SRS/MistakeBook are adjacent).
12. **Quiz → guided path builder** (Coddy) — `FindMyLevel`/onboarding diagnostic partially covers this.

### Constraint reminders (AGENTS.md)
- Content Trust + No-LLM Bank: reused curriculum content must enter through
  `UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED`; **no LLM writes question content**.
- We may copy *structure and mechanics*, not proprietary text. Curriculum source options:
  (a) our own existing banks/lessons (already resident in `backend/app/data|content`), (b) openly
  licensed sources (Exercism, freeCodeCamp, The Odin Project, CS50/OSSU, Khan Academy CC-BY-NC-SA),
  (c) outbound links/affiliates to the commercial platforms — never scraped copy.

## 4. Build order (recommended)

| # | Wave | Scope | Done when |
|---|---|---|---|
| 1 | **P0 route health** | Fix dup `/arena`, wire-or-delete 26 orphans into 5 envs, UTF-8 fix, verify every `Link to` + `ENV_REDIRECTS` target resolves, dead API calls to deleted backend routes removed | `npm run build` + route-graph audit script = 0 dead links; clicking through all 5 envs renders content |
| 2 | **P0 unified write path** | `LessonPlayer`/`GoldenFlow` record via `POST /api/v1/unified/activity` | one write path verified by response body |
| 3 | **P1 catalog scale** | adapters for `language_paths`, `learning_modules`, question bank, company tracks | `/catalog/stats` sources list grows; UnifiedHub shows them |
| 4 | **P1 hierarchy** | `structure` = paths/courses/levels/lessons on catalog + UnifiedHub/LearnTrack UI | Brilliant-style progression visible end-to-end |
| 5 | **P2 credentials** | certificate issue + verify endpoint on course completion | pasted response body of a issued cert + 200 verify |
| 6 | **P2 roadmap pages** | 2–3 SEO roadmap pages composed from catalog | pages render real catalog data |
| 7 | **P2 boot.dev economy** | hint/solution XP costs, lesson reset without re-XP | ledger shows cost entries |
| 8 | **P2 tutor** | one Socratic tutor (context + student code, no answers) across lesson runtime | test asserting tutor reply never contains solution |

Wave 1 first — the product being "empty and worst" is route wiring, not missing curriculum.
