# BOUNTYCODE — ARCHITECTURE AUDIT REPORT

**Date:** 2026-08-29
**Scope:** Full repository scan — backend routes, services, MongoDB collections, frontend pages.

---

## A. CANONICAL SYSTEMS (Source of Truth)

| System | Canonical File | Responsibility |
|--------|---------------|----------------|
| **Journey** | `routes/journey.py` + `pages/JourneyPage.tsx` | Visual world/map/progression/home. Single endpoint `GET /api/v1/journey/state`. |
| **Study Engine** | `services/study_engine.py` | Decides "what should this student do next". Composes WORLD_REGISTRY + SRS + adaptive + gamification. |
| **Lesson Engine** | `content/lesson_definitions.py` + `content/world1_foundations.py` + `content/world_registry.py` | Generic teaching algorithm. `LessonDefinition` with `discover → manipulate → predict → build → break → debug → retrieve → transfer → prove`. |
| **Curriculum** | `content/world_registry.py` + `content/world*.py` | Defines what must be learned. 12 worlds, each with towns + lessons. |
| **Mastery** | `services/mastery_engine.py` | Determines whether something was learned. `SkillMastery`, `MasteryGraph`, `find_weak_areas`. |
| **SRS** | `services/srs_engine.py` | ONE spaced repetition implementation. `SRSCard`, `get_due_cards`, `update_card`. |
| **Gamification** | `services/gamification.py` | XP, levels, streaks, coins, bosses, badges, power-ups, leagues, challenges, daily goals. |
| **Readiness** | `services/readiness_engine.py` | Converts evidence into job readiness. `calculate_readiness`, `score_dsa`, `score_aptitude`, etc. |
| **Question Bank** | `data/questions_bank.json` + `data/questions_bank_curated.json` | Curated questions with quality tiers. |
| **Compiler/Judge** | `services/code_executor.py` + `routes/worlds.py` (`judge_level`) | Local deterministic judge + Piston API execution. |
| **Hint System** | `content/hint_system.py` | Gamified hint unlocks. `MysteryBox`, `HintLadder`. |
| **Role Packages** | `content/role_packages.py` | Role-based learning paths. SDE, Data Scientist, ML Engineer, DevOps, Frontend, CP. |
| **Analytics** | `services/analytics.py` + `frontend/src/services/api/analytics.ts` | Learning loop telemetry. |

---

## B. DUPLICATES — MERGE OR DELETE

### 🔴 CRITICAL: Journey/World Systems (7 duplicates)

| File | Status | Action |
|------|--------|--------|
| `routes/worlds.py` | **DUPLICATE** — OLD Foundations world with hardcoded `FOUNDATIONS_WORLD`, `WORLD_REGISTRY`, `get_world()`. Has `judge_level()` which is canonical. | **MERGE**: Extract `judge_level()` → keep in `worlds.py` as canonical judge. Delete the rest (world definitions moved to `content/`). |
| `routes/curriculum_engine.py` | **DUPLICATE** — OLD curriculum with `DAILY_MISSION_TYPES`, `get_daily_plan`, `get_world_view`. | **DELETE**: Superseded by `routes/journey.py` + `content/world_registry.py`. |
| `routes/learning_journeys.py` | **DUPLICATE** — OLD learning journeys system. | **DELETE**: Superseded by `routes/journey.py`. |
| `pages/WorldJourney.tsx` | **DUPLICATE** — OLD world journey page. | **DELETE**: Superseded by `pages/JourneyPage.tsx`. |
| `pages/WorldMap.tsx` | **DUPLICATE** — OLD world map page. | **DELETE**: Superseded by `pages/JourneyPage.tsx`. |
| `pages/AdaptivePath.tsx` | **DUPLICATE** — OLD adaptive path page. | **DELETE**: Superseded by `pages/JourneyPage.tsx`. |
| `pages/CommandCenter.tsx` | **DUPLICATE** — OLD command center page. | **DELETE**: Superseded by `pages/JourneyPage.tsx`. |

### 🔴 CRITICAL: SRS Systems (3 duplicates)

| File | Status | Action |
|------|--------|--------|
| `services/spaced_repetition.py` | **DUPLICATE** — OLD `SpacedRepetitionEngine` class. | **DELETE**: Superseded by `services/srs_engine.py`. |
| `routes/srs.py` | **DUPLICATE** — OLD SRS routes. | **DELETE**: Superseded by `services/srs_engine.py` consumed via `study_engine.py`. |
| `pages/SRSMastery.tsx` | **DUPLICATE** — OLD SRS mastery page. | **DELETE**: SRS reviews should appear in Journey, not a separate page. |

### 🔴 CRITICAL: Readiness Systems (4 duplicates)

| File | Status | Action |
|------|--------|--------|
| `services/job_readiness.py` | **DUPLICATE** — OLD job readiness system. | **DELETE**: Superseded by `services/readiness_engine.py`. |
| `routes/readiness.py` | **DUPLICATE** — OLD readiness routes. | **DELETE**: Superseded by `services/readiness_engine.py`. |
| `routes/predictor.py` | **DUPLICATE** — OLD predictor routes. | **DELETE**: Superseded by `services/readiness_engine.py`. |
| `pages/Predictor.tsx` | **DUPLICATE** — OLD predictor page. | **DELETE**: Superseded by Journey + readiness engine. |

### 🟡 HIGH: Mastery Systems (3 duplicates)

| File | Status | Action |
|------|--------|--------|
| `services/skill_assessment.py` | **DUPLICATE** — OLD skill assessment with `get_readiness_score`, `get_skill_graph`. | **MERGE**: Keep `update_skill_score` (used by study_engine). Delete the rest. |
| `services/progression_systems.py` | **DUPLICATE** — OLD progression systems. | **DELETE**: Zero imports found. |
| `pages/DSAFingerprint.tsx` | **DUPLICATE** — OLD DSA fingerprint page. | **DELETE**: Superseded by mastery engine + Journey. |

### 🟡 HIGH: Learning Engine Systems (5 duplicates)

| File | Status | Action |
|------|--------|--------|
| `services/adaptive_learning.py` | **OVERLAP** — Has `assess_user_skills`, `detect_weak_areas`, `generate_daily_plan`. | **MERGE**: `detect_weak_areas` is used by `study_engine.py`. Keep the rest as data providers, delete duplicate orchestration. |
| `services/curriculum_connector.py` | **DUPLICATE** — OLD curriculum connector. | **DELETE**: Superseded by `content/world_registry.py`. |
| `services/quest_engine.py` | **DUPLICATE** — OLD quest engine with 670 lines. | **DELETE**: Zero imports found. |
| `services/lesson.py` | **DUPLICATE** — OLD lesson service. | **DELETE**: Superseded by `content/lesson_definitions.py`. |
| `services/learning.py` | **DUPLICATE** — OLD learning service. | **DELETE**: Superseded by `study_engine.py`. |

### 🟡 HIGH: Frontend Journey Pages (10 duplicates)

| File | Status | Action |
|------|--------|--------|
| `pages/TowerDashboard.tsx` | **DUPLICATE** — OLD tower dashboard. | **DELETE**: Superseded by JourneyPage. |
| `pages/LearningJourneys.tsx` | **DUPLICATE** — OLD learning journeys page. | **DELETE**: Superseded by JourneyPage. |
| `pages/LearnTrack.tsx` | **DUPLICATE** — OLD learn track page. | **DELETE**: Superseded by JourneyPage. |
| `pages/LessonView.tsx` | **DUPLICATE** — OLD lesson view page. | **DELETE**: Superseded by LevelPlayer overlay. |
| `pages/LearningModule.tsx` | **DUPLICATE** — OLD learning module page. | **DELETE**: Superseded by JourneyPage. |
| `pages/LearningModules.tsx` | **DUPLICATE** — OLD learning modules page. | **DELETE**: Superseded by JourneyPage. |
| `pages/CurriculumHub.tsx` | **DUPLICATE** — OLD curriculum hub page. | **DELETE**: Superseded by JourneyPage. |
| `pages/CurriculumHubV2.tsx` | **DUPLICATE** — OLD curriculum hub v2 page. | **DELETE**: Superseded by JourneyPage. |
| `pages/RoleCurriculum.tsx` | **DUPLICATE** — OLD role curriculum page. | **DELETE**: Superseded by RoleSelect. |
| `pages/VariableDiscovery.tsx` | **DUPLICATE** — OLD variable discovery page. | **DELETE**: Superseded by LevelPlayer. |

### 🟢 MEDIUM: Question Bank Pages (3 duplicates)

| File | Status | Action |
|------|--------|--------|
| `pages/QuestionBank.tsx` | **ACTIVE** — Question bank browse page. | **KEEP**: Can remain as a practice/browse tool. |
| `pages/SolveProblem.tsx` | **ACTIVE** — Solve individual problem. | **KEEP**: Can remain as a practice tool. |
| `pages/PracticeMode.tsx` | **ACTIVE** — Practice mode page. | **KEEP**: Can remain as a practice tool. |

---

## C. DEAD CODE — UNUSED COLLECTIONS

These MongoDB collection proxies have **zero imports** outside `database.py`:

| Collection | Reason |
|------------|--------|
| `achievements_collection` | Removed feature (RPG achievements) |
| `alumni_experiences_collection` | Removed feature |
| `battles_collection` | Removed feature (RPG battles) |
| `campus_events_collection` | Removed feature (campus system) |
| `campus_leaderboard_collection` | Removed feature |
| `campus_profiles_collection` | Removed feature |
| `campus_winners_collection` | Removed feature |
| `cgpa_calculations_collection` | Removed feature (CGPA simulator) |
| `chat_messages_collection` | Removed feature (chat system) |
| `daily_quests_collection` | Removed feature (quest system) |
| `debug_logs_collection` | Removed feature (debug system) |
| `drive_trackers_collection` | Removed feature (drive tracker) |
| `friend_requests_collection` | Removed feature (friends system) |
| `friends_collection` | Removed feature |
| `gd_ratings_collection` | Removed feature (GD rooms) |
| `gd_rooms_collection` | Removed feature |
| `integrity_events_collection` | Removed feature |
| `matchmaking_queue_collection` | Removed feature |
| `oa_sessions_collection` | Removed feature |
| `peer_reviews_collection` | Removed feature |
| `pulse_battles_collection` | Removed feature (pulse system) |
| `pulse_daily_collection` | Removed feature |
| `ranks_collection` | Removed feature (rank system) |
| `referrals_collection` | Removed feature (referral system) |
| `shares_collection` | Removed feature |
| `study_squads_collection` | Removed feature (study squads) |

**Total: 26 dead collections** — safe to remove after confirming zero runtime usage.

---

## D. CONFLICTING ROUTES

| Route | Conflict | Resolution |
|-------|----------|------------|
| `GET /api/v1/journey/state` (new) vs `GET /api/v1/curriculum/daily` (old) | Both return "what to do next" | **Keep**: `journey/state`. **Delete**: `curriculum/daily`. |
| `GET /api/v1/worlds/foundations` (old) vs `GET /api/v1/journey/state` (new) | Both return world/lesson data | **Keep**: `journey/state`. **Delete**: `worlds/foundations` route. |
| `GET /api/v1/adaptive/daily-plan` vs `GET /api/v1/study/today` | Both return daily plan | **Keep**: `study/today`. **Delete**: `adaptive/daily-plan`. |
| `GET /api/v1/learning/journeys` vs `GET /api/v1/journey/state` | Both return journey data | **Keep**: `journey/state`. **Delete**: `learning/journeys`. |

---

## E. CONFLICTING DATABASE COLLECTIONS

| Collection | Conflict | Resolution |
|------------|----------|------------|
| `srs_cards_collection` vs `srs_collection` | Two SRS collections | **Keep**: `srs_cards` (used by `srs_engine.py`). **Delete**: `srs_states`. |
| `learning_progress_collection` vs `user_learning_progress_collection` vs `progress_collection` | Three progress collections | **Merge**: Keep `learning_progress` (used by study_engine). Delete others. |
| `questions_collection` vs `curated_questions_collection` | Two question collections | **Keep**: `curated_questions` (the curated bank). **Delete**: `questions`. |

---

## F. FEATURES ALREADY BUILT (Do Not Rebuild)

1. ✅ **Journey home** — `JourneyPage.tsx` with character, world map, level nodes
2. ✅ **Study Engine** — `study_engine.py` composing all subsystems
3. ✅ **Lesson Engine** — `LessonDefinition` with full teaching loop
4. ✅ **12 World Architecture** — `world_registry.py` with 92 lessons
5. ✅ **Multi-language support** — Python, Java, C++, C in lessons
6. ✅ **Mystery Box hints** — `MysteryBox.tsx` + `hint_system.py`
7. ✅ **Role packages** — `role_packages.py` with 6 roles
8. ✅ **Mastery system** — `mastery_engine.py` with evidence-based mastery
9. ✅ **SRS** — `srs_engine.py` with spaced repetition
10. ✅ **Gamification** — `gamification.py` with XP, levels, streaks, bosses, badges
11. ✅ **Readiness engine** — `readiness_engine.py` with company matching
12. ✅ **Question bank curation** — `curate_questions.py` with quality tiers
13. ✅ **Analytics** — `analytics.ts` with learning loop events
14. ✅ **Celebration system** — `Celebration.tsx` with confetti + mastery display
15. ✅ **Role selection** — `RoleSelect.tsx` with career path cards

---

## G. FEATURES ACTUALLY MISSING

1. ❌ **Onboarding flow** — 3 doors (Get a Job / Learn Coding / Starting From Zero)
2. ❌ **Daily Study Queue** — Unified "Today" view in Journey
3. ❌ **Job-seeker career layer** — Resume, interview, OA, company prep integration
4. ❌ **World 2 content** — Problem Solver (DSA patterns)
5. ❌ **Worlds 3-12 content** — Build Systems through Creative
6. ❌ **Question bank review pipeline** — AI-assisted review of 3,727 quarantined questions
7. ❌ **Admin question moderation** — Review/approve workflow
8. ❌ **Mobile polish** — Touch targets, reduced motion, keyboard handling

---

## H. EXACT DELETE/MERGE PLAN

### Phase 1: Delete Dead Routes (safe, no dependencies)

```
routes/curriculum_engine.py      → DELETE (superseded by journey.py)
routes/learning_journeys.py      → DELETE (superseded by journey.py)
routes/srs.py                    → DELETE (superseded by srs_engine.py)
routes/readiness.py              → DELETE (superseded by readiness_engine.py)
routes/predictor.py              → DELETE (superseded by readiness_engine.py)
```

### Phase 2: Delete Dead Services (safe, no dependencies)

```
services/spaced_repetition.py    → DELETE (superseded by srs_engine.py)
services/progression_systems.py  → DELETE (zero imports)
services/quest_engine.py         → DELETE (zero imports)
services/curriculum_connector.py → DELETE (superseded by world_registry.py)
services/lesson.py               → DELETE (superseded by lesson_definitions.py)
services/learning.py             → DELETE (superseded by study_engine.py)
services/job_readiness.py        → DELETE (superseded by readiness_engine.py)
```

### Phase 3: Merge Overlapping Services

```
services/skill_assessment.py     → MERGE: keep update_skill_score, delete get_readiness_score
services/adaptive_learning.py    → MERGE: keep detect_weak_areas, delete generate_daily_plan
routes/worlds.py                 → MERGE: keep judge_level, delete world definitions + routes
```

### Phase 4: Delete Dead Frontend Pages

```
pages/WorldJourney.tsx           → DELETE
pages/WorldMap.tsx               → DELETE
pages/AdaptivePath.tsx           → DELETE
pages/CommandCenter.tsx          → DELETE
pages/TowerDashboard.tsx         → DELETE
pages/LearningJourneys.tsx       → DELETE
pages/LearnTrack.tsx             → DELETE
pages/LessonView.tsx             → DELETE
pages/LearningModule.tsx         → DELETE
pages/LearningModules.tsx        → DELETE
pages/CurriculumHub.tsx          → DELETE
pages/CurriculumHubV2.tsx        → DELETE
pages/RoleCurriculum.tsx         → DELETE
pages/VariableDiscovery.tsx      → DELETE
pages/SRSMastery.tsx             → DELETE
pages/Predictor.tsx              → DELETE
pages/DSAFingerprint.tsx         → DELETE
```

### Phase 5: Remove Dead MongoDB Collections

Remove 26 dead collection proxies from `database.py` (listed in Section C).

### Phase 6: Clean Up Cross-References

- Remove deleted page imports from `App.tsx`
- Remove deleted page imports from `pages/lazy.ts`
- Remove deleted route imports from `main.py` (auto-discovers, but clean up)
- Update `AGENTS.md` to reflect canonical architecture

---

## SUMMARY

| Category | Count |
|----------|-------|
| **Canonical systems** | 12 |
| **Duplicate systems to delete** | 18 |
| **Overlapping services to merge** | 3 |
| **Dead frontend pages to delete** | 17 |
| **Dead MongoDB collections** | 26 |
| **Conflicting routes** | 4 (resolve by deletion) |
| **Features already built** | 15 |
| **Features actually missing** | 8 |

**Net result:** ~60 fewer files, ~26 fewer collections, zero duplicate engines, one canonical architecture.
