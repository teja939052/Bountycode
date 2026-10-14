# Blueprint P0 Inventory — `architecture-cleanup` @ 34a7ceb

Snapshot taken 2026-10-14 from the working tree. Supersedes
`docs/ROUTE_AUDIT_2026.md` and `docs/ROUTE_CONSOLIDATION.md` (both stale:
they describe 96 route files and a frontend route map that no longer exists).

Purpose: map what EXISTS before any keep/merge/defer/remove decision.
**No deletions were made in this pass.** Numbers are from static scans of
`backend/app/**` (routes, services, data, content) and
`frontend/src/**`; write-counts are lower bounds (proxy-call style
`x = foo_collection()` writes can be missed by the scanner — flagged inline).

---

## 1. Routes — 56 files, 54 `APIRouter`s (all `/api/v1/`)

| Area | Files (prefix) |
|---|---|
| Entry/rewards | `worlds.py` (/worlds), `map.py` (/map), `study.py` (/study), `campaign.py` (/campaign), `journey.py` (/journey), `learner.py` (/learner), `missions.py` (/missions), `mission_packs.py` (/mission-packs), `placement_packs.py` (/placement-packs) |
| Content/solve | `questions.py` + `questions_solve.py` (both /questions), `problems.py`, `coding.py`, `compiler.py`, `srs.py`, `repair.py`, `oa.py`, `company_mocks.py`, `company_prep.py` |
| Learning | `learning.py`, `learning_modules.py`, `lesson.py`, `lesson_player.py`, `unified_learning.py` (/unified), `cs_fundamentals.py`, `free_trial.py`, `trial.py` |
| Assessment/career | `interview.py`, `system_design.py`, `aptitude.py`, `resume.py`, `cover_letter.py` (/tools), `roles.py`, `profile_stats.py`, `progress.py`, `submissions.py`, `visualizations.py`, `trace.py`, `search.py` |
| Platform | `auth.py`, `onboarding.py`, `onboarding_doors.py` (/onboarding/doors), `onboarding_diagnostic.py` (/onboarding/diagnostic), `account.py`, `billing.py`, `invoices.py`, `coupon.py`, `student_discount.py`, `tiers.py`, `free_trial.py` |
| Ops | `analytics.py`, `analytics_admin.py`, `gamification.py`, `health.py`, `ai_debugger.py`, `ai_feedback.py` |

Frontend references **zero** prefixes for: `onboarding/doors`, `placement-packs`
(but `placement_packs` serves /curriculum page? verify before delete — scan is
string-containment based). Intentional same-prefix splits: `/questions`
(browse vs solve) — keep as one contract during consolidation.

## 2. Content registries — 7 competing curriculum sources

| # | Registry | File | Consumers | Notes |
|---|---|---|---|---|
| 1 | `WORLD_REGISTRY` | `app/data/worlds_data.py` | `routes/worlds.py:34`, `routes/map.py:26`, `routes/lesson_player.py:24`, `routes/gamification.py:447` (tower) | **Live.** `Town.levels` is the real field; `lessons` is a property alias (models/world.py:197-202) |
| 2 | `ALL_WORLDS` (WorldDefinition) | `app/content/world_registry.py:23` | `content/worlds_*.py`, `lesson_definitions` | Parallel lesson-graph schema |
| 3 | `ALL_WORLDS` (dict schema) | `app/data/capability_curriculum.py:1137` | itself | **Third** independent ALL_WORLDS with its own shape — collision-prone name |
| 4 | `LESSON_REGISTRY` + `canonical_worlds` | `app/content/curriculum/registry.py` | `routes/lesson.py:79-80`, `free_trial.py:3` (`app.data.curriculum`) | Placement curriculum contract |
| 5 | `LANGUAGES` / levels | `app/data/curriculum.py`, `curriculum_depth.py`, `curriculum_50_levels.py` | `study_engine`, `free_trial` | Older language-path system |
| 6 | Generated role curriculum | `content/curriculum/{learning_paths,final_curriculum,mock_tests,all_role_curricula}.json` | `routes/placement_packs.py:22-25` | Requires `generate_curriculum.py` run; 500s otherwise |
| 7 | CFIC graph | `app/content/cfic_curriculum.py` | additive graph lessons | Self-described additive layer |
| 8 | Question banks | `services/question_store.py` (66 JSON banks, ~150 MB; UNVERIFIED_EXTRA_BANKS:419, AUTO_CHECKED list) | all solve/serve paths | **Not Mongo** — residency rule holds |

## 3. State stores — 72 lazy collections declared (`app/database.py`), 42 mutated

Hot spots (writes from static scan; `x = col(); x.update_one` style may be undercounted):

| Collection | Writes (scan) | Importers | Role |
|---|---|---|---|
| `users` | 51 (49 update) | 40 | Profile + plan + usage counters + onboarding — biggest hot spot |
| `gamification` | 22 | 20 | Canonical XP/coins/streak (via `record_practice`) |
| `interviews` | 10 | 8 | Interview sessions |
| `oa_sessions` | 9 | 6 | Mock OA |
| `learning_progress` | 7 | 3 | Lesson progress (old learning service) |
| `skill_graphs` | 7 | 15 | Skills/mastery |
| `user_learning_paths` / `user_company_tracks` / `user_learning_progress` | 5/3/2 | 1-2 | Learning-paths layer |
| `srs_cards` | ≥1 (`routes/srs.py:128` via `cards_col` proxy) | 9 | **Live SRS store** |
| `srs_states` | 1 (`services/lesson.py:685`) | 5 | **Second SRS store** — duplicate responsibility |
| `user_question_state` | 2 | 1 | Per-question state (progress.py) |
| `solved_problems` | 1 | 9 | Solved list |
| `progress` | **0** | 1 (adaptive_learning) | Declared + read but never written |

**Duplicate responsibilities:**
- SRS: `srs_cards` (routes/srs.py — canonical per tag `spaced-repetition-problems`) vs `srs_states` (lesson.py write).
- Progress: `learning_progress` vs `user_learning_progress` vs `progress` vs `solved_problems` vs `user_question_state` — five stores, one responsibility.
- Rewards ledger: `gamification_events` is written only via
  `gamification_collection.database["gamification_events"]` (`services/gamification.py:107`);
  the declared `gamification_events_collection` (`database.py:307`) has **zero importers** — dead export.

**25 declared collections with zero writes found** (candidates for drop-after-verify):
`aptitude_leaderboard`, `assignments`, `assignment_submissions`, `bookmarks`,
`community_posts`, `content_modules`, `content_tranches`, `daily_challenges_users`,
`discussions`, `drive_trackers`, `exam_memories`, `interview_chat_sessions`,
`notes`, `playlists`, `practice_sessions`, `service_metrics`,
`system_design_leaderboard`, `system_design_tests`, `applications` (read-only),
`billing_metrics` (read-only), `generated_projects` (read-only),
`predictions` (read-only), `question_explanations` (read-only),
`repair_missions` (read-only), `submissions` (read-only).

## 4. Reward writers — single-writer law HOLDS

- `record_practice()` callers: 33 sites (aptitude, coding, company_prep,
  company_conversion, learning_modules, worlds, interview, unified_learning,
  gamification route, resume ×3, questions_solve ×2, campaign_service,
  lesson_orchestrator, learning_paths ×5, lesson, role_content_service,
  unified_learning service ×2, study_engine).
- `spend_xp()` — only `services/gamification.py:119` (+ its `$inc diamonds: -n` at :131).
- Direct `$inc` on diamonds/xp/level/streak/coins outside gamification.py: **none**.
- Remaining `$inc` sites are non-reward counters (usage limits, `hints_used`,
  `tab_switch_count`, coupon `used_count`, `repair trigger_count`) or
  path-local ledger (`learning_paths.total_xp_earned`).
- **One smell:** `adaptive_learning.py:446` does
  `$inc skills.<domain>.score` on what is likely `skill_graphs` — a second
  skill-score writer beside the canonical skill graph. Verify ownership.

## 5. Mastery / readiness — 3 parallel formulas

| Formula | Entry points |
|---|---|
| `readiness_engine.compute_readiness` (canonical) | `routes/gamification.py:512`, `journey.py:156`, `oa.py:1728` |
| `skill_assessment.get_readiness_score` (parallel) | `routes/auth.py:311-312` — **onboarding payload uses the non-canonical formula** |
| `adaptive_learning.calculate_readiness_score` (parallel) | adaptive_learning.py:663 |

Level/XP curve lives in `services/gamification.py` (+ `gamification_core.py`
counter map at :453). Frontend must render server-computed level only
(Gamification Law §3). `readiness_engine.calculate_target_readiness` and
`calculate_target_readiness_score` (:1409, :2154) are internal variants —
collapse during consolidation.

## 6. Question serving — trust-filter coverage

- **`only_verified()`** (strict): `questions.py:93,446,540`;
  `questions_solve.py:893` (random — fixed this branch);
  `oa.py:624,996,1814`; `company_conversion.py:335,349`;
  `question_store.py:1681` (company search).
- **`prefer_verified()`** (can fall back to UNVERIFIED on thin pools):
  `questions.py:258,311,826`; `progress.py:159`; `repair.py:66`;
  `company_prep_service.py:72,95,186,190`; `campaign_service.py:219,226`;
  `study_engine.py:290,702`.
- Remaining leak to close: make `prefer_verified` mean
  "prefer AUTOMATED_CHECKED/HUMAN_REVIEWED/TRUSTED, never UNVERIFIED"
  rather than "prefer verified but accept anything".

## 7. Code runners — 4 execution paths

| Path | File | Languages |
|---|---|---|
| Piston (primary network) | `code_executor.py:131,455` (`PISTON_API_URL`) | All Piston languages |
| Local sandbox (offline) | `local_sandbox.py:32` — `LOCAL_LANGUAGES = {"python", "javascript"}` | 2 only |
| Judge0 fallback | `remote_fallbacks.py:212` | Judge0 IDs |
| Docker sandbox + job queue | `docker_sandbox.py`, `code_execution_worker.py` (WS progress) | `LANGUAGE_CONFIGS` |
| Tracer | `code_tracer.py` → `local_sandbox.execute_local_sync` | python/js |

`anime_card_engine.py:161,238` also calls local + docker directly (side path).

## 8. Competing "Today" contracts — the merge target

Backend next-action producers (at least 9):
`study/today` (study_engine — daily plan, study.py:40),
`campaign/today` (campaign_service — company-aware override + legacy
redirect, campaign.py:93,152), `journey/state` (journey_engine — single
payload, journey.py:13), `learner/next-mission` (personalization,
learner.py:44), `unified_learning` next_mission (unified_learning.py:114),
onboarding state `next_mission` (auth.py:305,334), `roles.py:92` next
recommended activity, `oa.py:1579` next_missions, repair recommendations
(repair.py:161).

Frontend: `/` → `HomeRedirect.tsx:42` → **`/placement`** (PlacementCampaign)
for signed-in users. `frontend/src/services/api/journey.ts` calls BOTH
`journey/state` and `study/today`; `missions.ts` documents the same duality.
**No `/command`, `/journey`, `/lab` (except `/lab/lesson/:id`), `/arena`,
`/progress` routes exist** — the blueprint's 5 destinations are unimplemented;
`/placement` is the de-facto command screen.

## 9. Frontend — 39 pages, 37 api modules

- 1 dead page (zero importers): `pages/PercentagesMission.tsx`.
- 8 pages wired only via nested routes (not top-level elements): CompanyBattlefield,
  MissionPackPlayer, MissionPlayer, OnboardingQuest, PatternDrill,
  PlacementDiagnostic, RoundView, UnifiedLessonPlayer — all reachable.
- Router: `frontend/src/app/AppRoutes.tsx` (~45 paths). Navbar/BottomNav still
  surface the post-cleanup IA.

---

## Top 10 duplication/deletion targets (risk × payoff)

| # | Target | Why | Risk |
|---|---|---|---|
| 1 | Competing Today screens (§8) — pick `journey/state` as THE next-action contract | 9 producers confuse every screen; blueprint rule 1 | Medium — frontend callers to rewire |
| 2 | `prefer_verified` → never serve UNVERIFIED (§6) | Trust-pipeline leak on thin pools | Low — filter change + tests |
| 3 | Parallel readiness formulas (§5) — auth.py must use `compute_readiness` | Wrong readiness shown at onboarding | Low |
| 4 | 2nd SRS store `srs_states` writes (§3) | Split student memory | Medium — verify lesson.py path |
| 5 | 5 progress stores (§3) → 1 canonical | Progress truth fragmentation | High — migrate carefully |
| 6 | 7 curriculum registries (§2) → WORLD_REGISTRY + LESSON_REGISTRY | Content truth fragmentation | High — inventory consumers first |
| 7 | `PercentagesMission.tsx` + `gamification_events_collection` dead export (§3,§9) | Zero-risk deletes | Very low |
| 8 | 25 zero-write collections (§3) — verify then drop from database.py | Schema bloat | Low-Med — confirm no runtime `get_collection()` use |
| 9 | `adaptive_learning` skill `$inc` (§4) vs skill_graphs owner | Second skill writer | Medium |
| 10 | Nested-route orphan pages / old Navbar entries | IA drift vs 5-destination blueprint | Low |

**Not done in this pass:** any deletion, any merge decision, execution-heavy
bank tests, production smoke. Next step per blueprint: approve keep/merge/defer
per target above, then execute with the safe-deletion procedure (dependency
check → feature-flag or route removal → data migration → verify).
