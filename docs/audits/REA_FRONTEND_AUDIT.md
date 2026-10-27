# REA Frontend Bundle Audit — BountyCode

**Date:** 2026-10-27
**Purpose:** Mirror the production frontend bundle with REA (static analysis, no native engines, own product only) and enforce the one-journey navigation model: `Today | Learn | Practice | Assess | Profile`.

## Evidence

| Field | Value |
|---|---|
| Command | `rea analyze-javascript-application D:/Project-Fremen/frontend/dist --format json --max-semantic-nodes 6000 --max-semantic-nodes-per-file 400 --max-semantic-unknowns 1500 --max-semantic-unknowns-per-file 100 --filter-output "..."` |
| Evidence bundle | `docs/audits/rea/frontend-bundle-audit.json` (8.6 MB, UTF-8) |
| evidence_id | `ev_6ba70f7e0de9fbfe2419edb2b79e23003c4e64f84a851a3904a769a46494640a` |
| Subject | `frontend/dist` directory, sha256 `6d5efae2…c9fd1f5d` (built 2026-10-27 08:15, contains the 5-tab nav + Today one-mission changes) |
| Graph | 796 nodes × 3,656 edges; 121 JS chunks, 464 modules, 78 endpoint observations, 20 storage nodes, 1 service worker + worker |
| Note | An unbounded reference run produced a ~194 MB envelope; the committed artifact is the bounded run above (flags recorded in `parameters`). `raw_result` filtered out to keep the file committable — inventory digests and integrity fields are intact. |
| Source cross-checks | `AppRoutes.tsx` route regex (38 routes), Navbar/BottomNav/SearchModal/page link grep, services/API grep |

---

## 1. Primary student journey

`Today (/placement) → Learn (/curriculum) → Practice (/question-bank) → Assess (/mock-oa) → Profile (/profile)`

Shipped and reachable from both desktop navbar and mobile bottom nav. Signed-in users land on `/placement` (`HomeRedirect`). 11/11 smoke checks passed on this build.

## 2. Routes reachable from primary navigation

| Route | Tab | Notes |
|---|---|---|
| `/placement` | Today | `PlacementCampaign.tsx` — one mission + reason + CTA via `campaign/today` |
| `/curriculum` | Learn | `PlacementCurriculum.tsx` |
| `/question-bank` | Practice | `QuestionBank.tsx` |
| `/mock-oa` | Assess | `MockOA.tsx` |
| `/profile` | Profile | `Profile.tsx` |

Contextual from primary surfaces: `/diagnostic` (Today fallback), `/mission/:slug`, `/pattern/:id`, `/battlefield` (Today → Details), `More` menu: `/aptitude`, `/coding`, `/daily-challenge`, `/battlefield`, `/interview`, `/compiler`, `/resume`, `/ats`, `/admin` (admin only).

## 3. Routes reachable only contextually

`/mission/:slug`, `/pattern/:id`, `/mission-pack/:packId`, `/round/:roundId`, `/learn/:domain`, `/lab/lesson/:lessonId`, `/question-bank/:questionId`, `/solve/:id` (in-page CTAs), `/settings` (gear), `/interview/:interviewId` (flow), `/onboarding` (post-signup), `/free-trial` + `/pricing` (public CTAs).

## 4. Dead routes (linked from shipped UI, target does not exist)

REA recovered 47 route-like strings from `App`; source cross-check proves these targets have **no route** in `AppRoutes.tsx`. Every click 404s:

| Dead target | Linked from (file:line) | Count |
|---|---|---|
| `/dashboard` | `RouteErrorBoundary.tsx:35`, `FeatureErrorBoundary.tsx:76`, `AdminDashboard.tsx:79` redirect, `AptitudeTest.tsx:476`, `ATSOptimizer.tsx:416`, `CodingChallenge.tsx:522`, `InterviewSession.tsx:355`, `MockOA.tsx:1545` | 8 |
| `/leaderboard` | `BottomNav.tsx:42` (league strip), `Profile.tsx:426`, `SearchModal.tsx:25` | 3 |
| `/journey` | `MissionPackPlayer.tsx:171,193,209`, `UnifiedLessonPlayer.tsx:796` | 4 |
| `/history` | `Profile.tsx:424` | 1 |
| `/company-mocks` | `AptitudeTest.tsx:217` | 1 |
| `/system-design` | `SearchModal.tsx:17` | 1 |
| `/company-prep` | `SearchModal.tsx:18`, `Landing.tsx:557,659` | 3 |
| `/dsa-visualizer` | `SearchModal.tsx:19`, `Landing.tsx:558` | 2 |
| `/learning-paths` | `SearchModal.tsx:20` | 1 |
| `/skill-graph` | `SearchModal.tsx:22` | 1 |
| `/applications` | `SearchModal.tsx:24` | 1 |
| `/tower` | `SearchModal.tsx:26` | 1 |

**~25 dead links across 14 files.** Worst offender: error boundaries link to `/dashboard` — a crashed feature offers a 404 as recovery. (Already-fixed earlier in this session: `/learning`, `/learn`, `/arena`, `/start` from Navbar/BottomNav/Landing/LessonPlayer.)

## 5. Duplicate pages

- `services/api.ts` shim + `services/api/index.ts` aggregate: intentional dual surface (documented), not a duplication bug.
- SearchModal advertises surfaces whose destinations don't exist → perceived duplicates with no behind-routes. Same for two Landing feature tiles.
- `DailyChallenge.tsx` (167 kB chunk) is a 30-day-sprint page whose leaderboard calls `api.getDailyChallengeLeaderboard()` — **method not defined** in the API layer; tab always renders empty (verified earlier).

## 6. Orphan components/pages (routed but unreachable from any nav/graph)

| Route | Verdict |
|---|---|
| `/landing` | Orphan — `HomeRedirect` renders `Landing` under `/`; the `/landing` route itself is never linked |
| `/leaderboard`-class pages (Tower, DSA visualizer, company-prep, system design, skill-graph, applications) | Not in bundle as routes at all — only SearchModal/landing strings point at ghosts |

## 7. API calls outside canonical paths (`services/api/request.ts`)

| Call | From | Evidence |
|---|---|---|
| `fetch("/api/v1/onboarding/diagnostic/status")` | `AptitudeTest.tsx:94` | REA `[call:fetch]` |
| `fetch("/api/v1/onboarding/diagnostic/start?role=sde")` | `PlacementDiagnostic.tsx:42` | REA `[call:fetch]` |
| `fetch("/api/v1/onboarding/diagnostic/complete")` | `PlacementDiagnostic.tsx:75` | REA `[call:fetch]` |
| `fetch("/api/v1/compiler/execute")` | `FreeTrial.tsx:128` | REA `[call:fetch]` |
| `fetch("/api/v1/analytics/track")` | `AppRoutes.tsx:60` (telemetry, pre-bootstrap) | REA `[call:fetch]` |
| `fetch(`${API_BASE}/api/v1/resume/upload`)` | `services/api/resume.ts:14` | canonical module, raw fetch (multipart) |
| `fetch` auth refresh | `authStore` chunk (`/api/v1/auth/refresh`) | canonical-adjacent bootstrap |
| WebSocket | `useBattleLive.ts:72`, `useWebSocket.ts:72` | live battle transport |

REA false positive resolved: `InterviewSession` `[call:$.post]` on `/api/v1/interview/answer` is the shared `api.post` wrapper (canonical), not jQuery.

## 8. Unexpected external endpoints

| Endpoint | Purpose |
|---|---|
| `https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js` | `judgeService.ts` local Python execution fallback |
| `https://res.cloudinary.com/bountycode/...` | image/video CDN (recurring, by design) |
| `https://raw.githubusercontent.com/uiverse-io/galaxy/main` | background CSS asset (third-party UI universe) |
| `https://example.com/photo.jpg` | dead placeholder string in shipped source |

Products impacted: compiler-fallback PVAs, Cloudinary media, one background pack. No unexpected analytics/trackers found.

## 9. Recommended hide/archive/merge actions

1. **Fix 25 dead links** — replace `/dashboard` → `/placement` (9 sites, incl. both error boundaries); `/journey` → `/curriculum`; `/history` → `/profile` (drop card); `/company-mocks` → `/interview`; delete or create the rest (SearchModal entries and Landing tiles most urgent: 8 ghost destinations behind Cmd+K).
2. **SearchModal**: prune to real, shipped routes only.
3. **Error boundaries**: recovery link must be Today, never 404.
4. **Route `/landing`**: redirect to `/` instead of rendering second copy.
5. **Diagnostic fetches**: move to `services/api` (`onboarding.ts`); keep `AppRoutes` telemetry fetch (documented pre-API bootstrap).
6. **FreeTrial compiler fetch**: route through `compilerApi` in canonical layer.
7. **`DailyChallenge`**: either wire `getDailyChallengeLeaderboard` into the API layer + backend or hide the page (BETA).
8. **League strip `/leaderboard`** in BottomNav: remove or implement league route.
9. **Canonical-layer note**: `resume.ts` upload and `authStore` refresh stay raw-fetch but should use the shared `requestWithRetry` error/retry semantics where possible.

## 10. Final route classification

| Route | Class | Reason |
|---|---|---|
| `/placement` | KEEP | Today |
| `/curriculum` | KEEP | Learn |
| `/question-bank` | KEEP | Practice |
| `/mock-oa` | KEEP | Assess |
| `/profile` | KEEP | Profile |
| `/diagnostic` | CONTEXTUAL | Today fallback + onboarding |
| `/mission/:slug` | CONTEXTUAL | Mission player |
| `/pattern/:id` | CONTEXTUAL | Pattern mission |
| `/mission-pack/:packId` | CONTEXTUAL | Mission pack |
| `/round/:roundId` | CONTEXTUAL | Round view |
| `/learn/:domain` | CONTEXTUAL | Lesson deep link |
| `/lab/lesson/:lessonId` | CONTEXTUAL | Lesson player |
| `/question-bank/:questionId` | CONTEXTUAL | Problem solve view |
| `/solve/:id` | CONTEXTUAL | Problem solve |
| `/aptitude` | CONTEXTUAL | Practice tool (More) |
| `/coding` | CONTEXTUAL | Practice tool (More) |
| `/daily-challenge` | BETA | 30-day sprint; dead leaderboard call — hide until wired |
| `/battlefield` | BETA | Pattern mastery radar; Today uses "Details"; keep behind More per brief |
| `/compiler` | CONTEXTUAL | Coding workspace (More) |
| `/interview`, `/interview/:interviewId` | CONTEXTUAL | Assess → interview practice (More) |
| `/resume`, `/ats` | CONTEXTUAL | Career tools (More) |
| `/settings` | CONTEXTUAL | Gear |
| `/onboarding` | CONTEXTUAL | Post-signup flow |
| `/free-trial`, `/pricing` | CONTEXTUAL | Public CTAs |
| `/admin` | ADMIN | Admin dashboard |
| `/login`, `/register`, `/forgot-password`, `/reset-password`, `/verify-email` | PUBLIC AUTH | Not journey |
| `/terms`, `/privacy` | PUBLIC | Footer |
| `/landing` | ARCHIVE | Orphan duplicate of `/`; redirect |
| `/` | SPECIAL | HomeRedirect (Landing or Today) |
| `*` | SPECIAL | 404 |
| *(non-routes)* `/leaderboard`, `/tower`, `/system-design`, `/company-prep`, `/dsa-visualizer`, `/skill-graph`, `/learning-paths`, `/applications`, `/dashboard`, `/journey`, `/history`, `/company-mocks`, `/arena`, `/learning`, `/learn`, `/start` | ARCHIVE (ghost) | No route; ~25 shipped links point here — fix or delete links |

## Product decisions locked by this audit

REA maps; it can't decide. The product calls this audit records:

- The five tabs are the product; `More` holds tools; ghosts get deleted, not resurrected.
- Recovery UIs obey the journey: crashed → Today, always.
- All domain calls funnel through `services/api` (telemetry bootstrap exempt).
- `DailyChallenge` and `Battlefield` are BETA: reachable, but not journeys until their data flows are truthful.
