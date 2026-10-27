# ROUTE_AUDIT.md — Learning curriculum + Company prep: full route audit

**Date:** 2026-09-27 · **Method:** static scan (routes, lazy.ts, pages, api modules, backend routers).
**Scope asked:** all learning/curriculum routes + all company-prep routes + cross-cutting breakers.
**Not yet verified (needs running backend):** response bodies per AGENTS.md evidence rule.

---

## 0. TL;DR for the decision

| # | Finding | Severity | Area |
|---|---------|----------|------|
| B1 | `/placement-calendar` calls `api.companyDirectory.*` — **not defined anywhere** → page crashes on load | **P0 breaker** | company prep |
| B2 | `IndianPlacement` fetches `/api/v1/company/roadmap` (no backend) + swallows **all** errors with `.catch(() => null)` → renders empty sections | **P0 empty-page** | company prep |
| B3 | Dead API surface with **zero routed-page callers** (contained, no user impact today): `predictorApi`+`readinessApi` (`/api/v1/predictor/*`, `/api/v1/readiness/*`), `placementApi` dashboard/drives/gap/probability fns, `missions` api, `VariableDiscovery` endpoints | P1 cleanup | both |
| B4 | 25 orphan pages (built, never wired) — 9 have **working backends ready** (§4) | P0 wiring decision | both |
| B5 | Already fixed this session: 5 undeclared shell exports (build-breaker), dup `/arena`, dead links `/admin/content-corpus`, `/mock?company=TCS`, `/rank`, UTF-16 file, `/company-prep` wired | done | — |
| B6 | `ENV_REDIRECTS` in AppRoutes is **defined but never consumed** (dead config); real redirects are ~45 hardcoded `<Navigate>` routes | P2 cleanup | routing |
| B7 | `StudentDashboard` (your F1-fixed page) is **unreachable**: `/student-dashboard` → redirects to `/world`; only importer is `lazy.ts` | note | routing |

API surface overall: **741 frontend endpoint literals scanned, 0 unbacked** except the contained items in B3
(template-literal matches like `${qs}`/`${suffix}` are false positives — they resolve to backed prefixes).

---

## 1. P0 breakers (detail)

### B1 — PlacementCalendar crashes (`/placement-calendar`, 401 lines, ROUTED)
- Calls `api.companyDirectory.getCalendar/getFilters/getCompanies/getCompany/search/getProgress/saveProgress` (lines ~100–149, in load effects).
- `companyDirectory` is **not defined in any file** under `frontend/src` and not a key of the `api` index object → `TypeError: Cannot read properties of undefined` on page load.
- Probable cause: page was built against deleted `backend/app/routes/company_directory.py` (confirmed MISSING).
- Nearest living backend: `placement_calendar.py` (`/api/v1/placement-calendar/*`: companies, calendar, countdown, company/{slug}, boss-battles, timeline/{slug}) — but it has **no** search/filters/progress endpoints, so the page needs re-pointing, not just a rename.
- **Decision needed:** (a) rebuild a `companyDirectory` api module against living backends, or (b) rewrite the page against `placement_calendar.py` (+alumni/drives data), or (c) unroute the page until fixed.

### B2 — IndianPlacement renders empty (`/indian-placement`, 876 lines, ROUTED)
- Uses raw `fetch()` (bypasses authed `api` client) to **backed** endpoints (`/api/v1/indian-placement/*`, `/api/v1/adaptive/readiness` ✓) — those work.
- BUT line 361 fetches `/api/v1/company/roadmap` — **no backend serves `/api/v1/company/*`** (living file is `companies.py` at `/api/v1/companies/*` with different shapes) → 404.
- Every fetch ends `.then(r => r.ok ? r.json() : null).catch(() => null)` → failures become silent `null`s → sections render empty instead of erroring. This is the "empty and worst" pattern.
- **Decision needed:** point roadmap section at a living endpoint (or drop it) + add visible error states instead of null-swallowing.

### B3 — Dead but contained (no routed caller today)
| Dead surface | Backend status | Who references it |
|---|---|---|
| `predictorApi` (`/api/v1/predictor/*` 12 endpoints) + `readinessApi` (`/api/v1/readiness/*`) in `adaptive.ts` | `predictor.py`, `readiness.py` MISSING | nobody (orphan `Predictor.tsx` doesn't even import it) |
| `placementApi.getDashboardInsights/getPlacementDrives/getGapAnalysis/getCompanyProbability` | `placement.py` has **only** `GET /alumni` | nobody imports `placement.ts` except index |
| `missions` api (`/api/v1/missions/`) | `missions.py`/`mission_engine.py` MISSING | nobody (`missions.filter/slice` hits are array methods) |
| `VariableDiscovery` raw calls `/api/v1/learning/lesson/variable-discovery[/complete]` | `learning.py` has only `/interaction-action`, `/diagnose` | orphan page only |
| `flatOverrides.ts` (friends/rank/projects/profile/predictor legacy) | mostly removed features | only `api/index.ts` re-export; **zero page callers** |
| `Skills.tsx` (7 lines) | n/a (alias of ReadinessHeatmap) | orphan, harmless |

---

## 2. Learning curriculum — backend inventory (all files tagged LEARN)

| Route file | Prefix | Eps | Status |
|---|---|---|---|
| adaptive_learning.py | `/api/v1/adaptive` | 8 | ✅ live (skills, weak-areas, daily-plan, recommendations, learning-path, readiness, activity, domains) |
| aptitude.py | `/api/v1/aptitude` | 10 | ✅ live |
| aptitude_tests.py | `/api/v1/aptitude-tests` | 9 | ✅ live — DUPLICATE system of aptitude.py (two aptitude engines) |
| arena.py | `/api/v1/arena` | 2 | ✅ live (quiz, submit) |
| atoms.py | `/api/v1/atoms` | 18 | ✅ live (worlds, atoms, attempt, misconception, intuition, metaphors, company paths) |
| compiler.py | `/api/v1/compiler` | 7 | ✅ live (Piston: execute, test-cases, trace, boilerplate) |
| concepts.py | `/api/v1/concepts` | 5 | ✅ live (graph, progress, frame, frame/result) |
| curriculum.py | `/api/v1/curriculum` | 2 | ✅ live (missions, missions/{id}) |
| daily_challenge.py | `/api/v1/daily`, `/api/v1/daily-challenge` | 4 | ✅ live |
| daily_problem.py | `/api/v1/daily-problem` | 3 | ✅ live |
| deck.py | `/api/v1/deck` | 2 | ✅ live (today, review) |
| dsa_fingerprint.py | `/api/v1/fingerprint` | 3 | ✅ live |
| free_practice.py | `/api/v1/free` | 2 | ✅ live |
| language_paths.py | `/api/v1/languages` | 7 | ✅ live (levels, modules, progress, complete, recommendations) |
| learner.py | `/api/v1/learner` | 1 | ✅ live (state) |
| learning.py | `/api/v1/learning` | 2 | ⚠️ thin (interaction-action, diagnose) — VariableDiscovery's endpoints missing |
| learning_modules.py | `/api/v1/learning-modules` | 5 | ✅ live, page ORPHAN (§4) |
| learning_paths.py | `/api/v1/learning-paths` | 6 | ✅ live, page ORPHAN (§4) |
| lesson.py | `/api/v1/lesson` | 12 | ✅ live (full lesson loop: run/build/transfer/predict/explain/break/assess/complete + plan + next-action), page ORPHAN (§4) |
| practice.py | `/api/v1/practice` | 3 | ✅ live |
| problems.py | `/api/v1/problems` | 9 | ✅ live (detail, lock-state, run, static-analysis, srs) |
| questions.py + questions_solve.py | `/api/v1/questions` | 23 | ✅ live (bank + solve/answer/submit/patterns/topics) |
| scrimba.py | `/api/v1/scrimba` | 3 | ✅ live, page ORPHAN (§4) |
| srs.py | `/api/v1/srs` | 5 | ✅ live |
| study.py | `/api/v1/study` | 2 | ✅ live (today, activity) |
| teachwall.py | `/api/v1/teachwall` | 2 | ✅ live |
| unified_learning.py | `/api/v1/unified` | 7 | ✅ live (canonical catalog + single write path; only `UnifiedHub` consumes it) |
| visualizations.py | `/api/v1/visualizations` | 8 | ✅ live |
| worlds.py | `/api/v1/worlds` | 7 | ✅ live |
| company_lessons.py | `/api/v1/company-lessons` | 2 | ✅ live (LessonPlayer uses `complete`) |
| placement_packs.py | `/api/v1/placement-packs` | 16 | ✅ live (sde/companies/learning-objects/learning-paths/mock-tests/roles) |
| placement_questions.py | `/api/v1/placement-questions` | 3 | ✅ live |
| company_mocks.py | `/api/v1/company-mocks` | 7 | ✅ live — is any page using it? `CompanyExam` orphan uses `companyPrepExam` module instead; verify overlap |

Missing (deleted by prior cleanup, referenced by dead code only): `study_library.py`, `study_timer.py`, `missions.py`, `predictor.py`, `readiness.py`.

## 3. Learning curriculum — frontend route table (routed pages only)

| Path(s) | Page | Backend it uses | Verdict |
|---|---|---|---|
| `/lab` | UnifiedHub (209) | `unifiedApi` (lessons, progress) | ✅ live, thin (links to `/learn/<id>` — redirect ✅) |
| `/lab/lesson/:id`, (`/lesson/:slug`, `/learn/*` → redirect here) | LessonPlayer (421) | `companyLessons.complete` only | ⚠️ **under-wired**: full `lesson.py` loop (12 eps) unused; records via legacy path, not unified activity |
| `/lab/concept/:id`, `/world/:w/concept/:c`, `/golden*` | GoldenFlow | (concept player) | ✅ routed — backend TBD verify |
| `/world`, `/world/:id` | JourneyPage, LevelMap | worlds/atoms | ✅ routed |
| `/arena`, `/arena/challenge/:id`, `/arena/boss/:id`, `/arena/mock-oa`, `/arena/contest/:id` | Arena, PracticeMode, Tower, MockOA, MonthlyContests | arena, questions, oa (`oa.py` ✅), gamification | ✅ routed — `oa.py` EXISTS (earlier `oa_engine` scare was a false alarm) |
| `/question-bank`, `/question-bank/:id`, `/problems`, `/problems/:topic`, `/pattern/:id`, `/solve/:id`, `/sheets` | QuestionBank, PracticeMode, Topics, TopicProblems, PatternPage, SolveProblem, Sheets | questions, problems | ✅ routed |
| `/aptitude`, `/coding`, `/daily-drill`, `/daily-challenge*`, `/problem-of-the-day`, `/speed`, `/simulator`, `/compiler`, `/playground`, `/challenge-packs`, `/dsa-visualizer`, `/visualize/compare`, `/cs-fundamentals` | (respective) | respective backends ✅ | ✅ routed |
| `/deck`, `/mistakes`, `/teach-wall`, `/command/*`, `/mock-oa`, `/tcs-nqt`, `/exam-memory/submit` | Deck, MistakeBook, TeachWall, Today/Readiness/Repair/MyProgress, MockOA, TcsNqtSimulation, ExamMemorySubmission | deck, evidence, teachwall, adaptive/o…a, exam-memories | ✅ routed |
| `/tower` (legacy, = arena boss) | Tower | gamification | ✅ routed |

## 4. Company prep — backend + frontend inventory

| Backend file | Prefix | Eps | Consumed by |
|---|---|---|---|
| companies.py | `/api/v1/companies` | 5 (list, role, role/company, evaluate, roadmap) | ? verify page usage |
| company_prep.py | `/api/v1/company-prep` | 5 (blueprints, questions, readiness, start-assessment) | `companyPrep` module (2 eps) — verify page usage |
| company_tracks.py | `/api/v1/company-tracks` | 5 (companies, track, enroll, complete, my-tracks) | orphan `CompanyTracks` page only |
| company_mocks.py | `/api/v1/company-mocks` | 7 (full session flow) | no routed page confirmed — verify |
| company_lessons.py | `/api/v1/company-lessons` | 2 | LessonPlayer ✅ |
| indian_placement.py | `/api/v1/indian-placement` | 6 | IndianPlacement ✅ (raw fetch) |
| interview.py | `/api/v1/interview` | 7 (+replay) | Interview/Session/Replay ✅ |
| interview_booking.py | `/api/v1/interview-booking` | 10 | InterviewBooking ✅ |
| interview_chat.py | `/api/v1/interview-chat` | 4 | ? verify page usage |
| exam_memories.py | `/api/v1/exam-memories` | 6 | ExamMemorySubmission + AdminExamReview ✅ |
| placement_calendar.py | `/api/v1/placement-calendar` | 6 | nobody (PlacementCalendar uses dead `companyDirectory`) |
| placement_packs.py | `/api/v1/placement-packs` | 16 | ? verify page usage |
| placement_questions.py | `/api/v1/placement-questions` | 3 | ? verify page usage |
| placement.py | `/api/v1/placement` | 1 (`/alumni`) | AlumniExperiences presumably ✅ |
| resume.py | `/api/v1/resume` | 13 | ResumeBuilder/Studio/ATS ✅ |
| cover_letter.py | `/api/v1/tools` | 1 (**only** `linkedin-about`) | full cover-letter generation is GONE; orphan `CoverLetter.tsx` uses no API at all |
| tcs_nqt.py | `/api/v1/tcs-nqt` | 6 | orphan `TcsNqtPrep` only; routed `TcsNqtSimulation` uses `oa.*` instead |

| Frontend path(s) | Page | Verdict |
|---|---|---|
| `/career`, `/career/resume`, `/career/interview`, `/career/company/:id`, `/company-prep`, `/tracks/:company` | Navigate, ResumeBuilder, Interview, CompanyTrack, **CompanyPrepHub (wired this session)** | ✅ live |
| `/interview`, `/interview/:id`, `/interview-booking`, `/interview-replay/:id` | Interview, Session, Booking, Replay | ✅ live |
| `/resume`, `/resume-studio`, `/ats`, `/resume-ats` | ResumeBuilder, ResumeStudio, ATSOptimizer, ResumeATS | ✅ live |
| `/placement-calendar` | PlacementCalendar | 🔴 **B1 crash** |
| `/indian-placement` | IndianPlacement | 🟡 **B2 partial-empty** |
| `/tcs-nqt`, `/mock-oa`, `/arena/mock-oa`, `/aptitude`, `/exam-memory/submit`, `/admin/exam-review`, `/alumni-experiences`, `/command/*` | (respective) | ✅ live |
| `/admin/corpus` | AdminContentCorpus | ✅ live (link fixed this session) |

## 5. Orphan pages — the 25 unwired systems (your agents' output)

**Group A — backend READY, just needs routes (highest value):**

| Page | Lines | Backend ready | Suggested home |
|---|---|---|---|
| LessonPage | 2179 | `lesson.py` 12 eps ✅ | `/lab/lesson-full/:slug` or replace LessonPlayer |
| LearningModules | 583 | `learning_modules.py` 5 eps ✅ | `/lab/modules` |
| LearningPaths | 339 | `learning_paths.py` 6 eps ✅ | `/lab/paths` |
| CompanyTracks | 368 | `company_tracks.py` 5 eps ✅ | `/career/tracks` |
| ProblemDetail | 477 | `problems.py` 9 eps ✅ | merge into PracticeMode or `/solve/:id` alt |
| CompanyExam | 531 | `companyPrepExam` module ✅ (verify its 4 eps hit `company_prep.py`/`company_mocks.py`) | `/arena/company-exam` |
| TcsNqtPrep | 518 | `tcs_nqt.py` 6 eps ✅ | `/tcs-nqt/prep` |
| Scrimba | 474 | `scrimba.py` 3 eps ✅ | `/lab/scrimba` |
| Problems | 441 | `problems.py`/`questions` ✅ | check overlap with Topics/QuestionBank first |

**Group B — needs product decision (overlap / unclear backend):**

| Page | Lines | Note |
|---|---|---|
| LearnTrack (163) + LearnLesson (548) | boot.dev-style track; links to `/curriculum/*` which **doesn't exist** | wire as `/lab/track`, `/lab/learn/:id` OR drop if LessonPlayer covers it |
| LanguageJourney (495) | `language_paths.py` 7 eps ✅ — actually Group A candidate | `/lab/languages` |
| StudyLibrary (458) | study_library.py DELETED; `study_materials` feeds unified catalog instead | point at unified catalog or drop |
| WorldMap (342) | worlds/atoms ✅ | `/world/map` |
| ConceptLearn/ConceptGraph/ConceptFrame (368/206/369) | concepts.py ✅; link to `/cific`, `/learn` (redirects) | merge into GoldenFlow or `/lab/concepts` |
| AtomLesson (682, in lazy, no route) + AtomWorlds (69) | atoms.py 18 eps ✅ | `/lab/atom/:id`, `/lab/atoms` |
| CurriculumHub (157), ModuleDetail (124), Practice (84), Concepts (80) | small hubs | verify overlap, likely merge |
| BeginnerLaunch (375) + DevLaunch (406) | launch flows; DevLaunch uses local mission data | `/start/*` variants or drop |
| Prepare (217), Compete (32), Home (292), Career (32) | thin hubs/redirects (`/prepare`→/world, `/compete`→/arena/mock-oa already redirect) | drop or keep as redirects |
| AdaptivePath (678, ex-UTF-16) | links to `/adaptive` (doesn't exist) | drop or re-point |
| CoverLetter (258, no API) | backend generation gone | drop or rebuild |
| Predictor (642) | predictor backend gone | drop or rebuild |
| PersonalDashboard (863) | unreachable (route redirects) | drop or make `/command` home |
| StudyGroups (199), MyAssignments (240, redirects to /world), Analytics (262), LessonView (983), VariableDiscovery (1012, backend gone), PatternAnimations (255), PlacementDrives (191), CompanyPrepHub ✅ done | mixed | per-item call |

## 6. Fixed this session (no action needed)
1. `lazy.ts`: 5 shell components exported-but-never-declared (build-breaker) — declared.
2. `CompanyPrepHub` wired (`lazy.ts` ×3 + import + `/company-prep` route in Career group).
3. Duplicate `/arena` route removed (kept env-group copy).
4. Dead links fixed: `/admin/content-corpus`→`/admin/corpus`, `/mock?company=TCS`→`/arena/mock-oa`, `/rank`→`/leaderboard`.
5. `AdaptivePath.tsx` converted UTF-16→UTF-8.
6. Post-fix: 0 dup routes, 0 missing lazy targets, 0/741 unbacked API literals (outside B3-contained), `lazy.ts` typecheck 0.

---

## 7. Open questions for you (tell me what to do)
- **Q1 B1:** PlacementCalendar — rebuild api module against living backends, rewrite page, or unroute?
- **Q2 B2:** IndianPlacement roadmap section — which living endpoint (or drop + error states)?
- **Q3 Group A:** wire all 9 now (I proposed homes in the table)?
- **Q4 Group B:** which to wire, which to delete? (biggest: LearnTrack/LearnLesson vs LessonPlayer — pick ONE lesson player; LessonPage 2179 lines vs LessonPlayer 421 lines)
- **Q5:** delete B3 dead surface (`predictorApi`/`readinessApi`, dead `placementApi` fns, `missions` api, `flatOverrides`, dead `ENV_REDIRECTS` config), or keep for a planned rebuild?
- **Q6:** aptitude.py vs aptitude_tests.py — two engines; keep both?
- **Q7:** `company_mocks.py` / `placement_packs.py` / `placement_questions.py` / `companies.py` / `company_prep.py` / `interview_chat.py` — 6 company backends with no confirmed routed consumer; map each to a page or park them?
