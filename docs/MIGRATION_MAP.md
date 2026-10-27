# Migration Map: Legacy → Constitution

> **Purpose:** Concrete guidance for reorganizing the codebase to match `ARCHITECTURE_CONSTITUTION.md`.
> **Status:** 2026-09-28

---

## Legend

- **KEEP** — Canonical; preserve and possibly refactor
- **MERGE** — Absorb into a canonical system; delete duplicates
- **ARCHIVE** — Move to `archive/`; not deleted, but not active
- **DELETE** — Remove from active codebase after confirming no dependencies

---

## 1. Frontend Pages

### Keep
| Page | Reason |
|------|--------|
| `Landing` | Public entry point |
| `Login`, `Register`, `ForgotPassword`, `ResetPassword` | Auth |
| `OnboardingQuest` | Tiny onboarding |
| `JourneyPage` / `LevelMap` | Learn Coding journey |
| `UnifiedHub` / `LessonPlayer` / `LearningModules` | Lesson experience |
| `PracticeMode` / `SolveProblem` / `Compiler` | Code practice |
| `Tower` | Simplified gamification (diamonds only) |
| `DailyChallenge` | Daily practice |
| `MockOA` | Mock assessments |
| `Interview` / `InterviewSession` | Interviews |
| `ResumeBuilder` / `ResumeStudio` / `ATSOptimizer` | Resume |
| `CompanyPrepHub` / `CompanyTrack` | Company prep |
| `IndianPlacement` / `TcsNqtSimulation` | Service-based prep |
| `DSAVisualizer` | DSA Visual Lab |
| `AdminDashboard` | Admin |
| `Pricing` / `FreeTrial` | Billing |
| `NotFound` | Error page |

### Merge into Canonical Shells
| Legacy Page | Merge Into | Reason |
|-------------|-----------|--------|
| `WorldMap`, `VariableDiscovery`, `StartPath`, `FindMyLevel` | `JourneyPage` / `LevelMap` | Duplicate journey views |
| `LessonView`, `Concepts`, `ConceptLearn`, `ConceptGraph`, `ConceptFrame` | `LessonPlayer` | Concepts are internal, not products |
| `AtomWorlds`, `AtomLesson` | `LessonPlayer` | Atoms are internal |
| `CurriculumHub`, `LearningPaths`, `LearningHub`, `LanguageJourney` | `UnifiedHub` | Duplicate learning hubs |
| `PrepHub`, `Prepare`, `StudentDashboard`, `PersonalDashboard`, `Target`, `Skills`, `Analytics` | `TodayPage` | Duplicate dashboards |
| `AptitudeTest`, `DailyDrill`, `ProblemOfTheDay`, `PatternPage`, `Topics`, `TopicProblems`, `Sheets`, `CSFundamentals`, `Deck`, `TeachWall`, `Arena`, `Simulator` | `PracticeMode` / `MockOA` | Merge into unified practice |
| `CodePlayground`, `CompareVisualizer` | `Compiler` / `DSAVisualizer` | Merge into existing tools |
| `ResumeATS`, `CoverLetter`, `SalaryBenchmark`, `SalaryNegotiation` | `ResumeBuilder` | Merge into career flow |
| `AlumniExperiences`, `PlacementDrives`, `PlacementCalendar` | `CompanyPrepHub` | Merge into placement |
| `StudyLibrary`, `StudyGroups` | Archive | Not in 4-door model |
| `Mission`, `MissionResult`, `SlidingWindowMission` | Archive | Legacy RPG |
| `AnimeCards` | Archive | Legacy gamification |
| `RoleSelect` | Merge into `OnboardingQuest` | Onboarding step |
| `SpeedSelect` | Archive | Not in 4-door model |
| `MistakeBook`, `RepairHub`, `EvidenceDashboard`, `ReadinessHeatmap` | `TodayPage` | Merge into command center |
| `ChallengePacks`, `MonthlyContests` | Archive | Not in 4-door model |
| `PwaSetup`, `Settings`, `Profile`, `History`, `Leaderboard` | Keep | Utility |
| `Blogs`, `BlogPost` | Archive or merge into `CompanyPrepHub` | Content marketing, not core |
| `Enterprise`, `StudentFeatures` | Archive | Not in 4-door model |
| `Terms`, `Privacy`, `UiverseShowcase` | Keep | Legal / dev |

### Archive (not routed or legacy)
- `WorldMap.tsx`
- `VariableDiscovery.tsx`
- `StudyLibrary.tsx`
- `StudyGroups.tsx`
- `Prepare.tsx`
- `Predictor.tsx`
- `Practice.tsx`
- `ProblemDetail.tsx`
- `PatternAnimations.tsx`
- `Home.tsx`
- `Journey.tsx`
- `LearnTrack.tsx`
- `LessonView.tsx`
- `Assess.tsx`
- `Compete.tsx`
- `AdminContent.tsx`
- `AdminExamReview.tsx`
- `ReadinessHeatmap.tsx`
- `EvidenceDashboard.tsx`
- `Profile.tsx`
- `Target.tsx`
- `Skills.tsx`
- `Analytics.tsx`
- `PersonalDashboard.tsx`
- `Scrimba.tsx`
- `GoldenFlow.tsx`
- `DevLaunch.tsx`
- `BeginnerLaunch.tsx`
- `Assess.tsx`
- `LearnTrack.tsx`

---

## 2. Backend Routes

### Keep
| Route | Reason |
|-------|--------|
| `auth.py` | Auth lifecycle |
| `onboarding.py` | Tiny onboarding |
| `interview.py` | AI interviews |
| `resume.py` | Resume lifecycle |
| `coding.py` | Coding challenges |
| `compiler.py` | Code execution |
| `questions.py` / `questions_solve.py` | Question bank |
| `gamification.py` | Diamonds only |
| `company_prep.py` | Company blueprints |
| `company_mocks.py` | Company mocks |
| `indian_placement.py` | Service-based prep |
| `system_design.py` | System design |
| `lesson.py` | Lesson engine |
| `learning_paths.py` | Role-based paths |
| `learning_modules.py` | Duolingo modules |
| `language_paths.py` | 6-language paths |
| `srs.py` | Spaced repetition |
| `daily_challenge.py` | Daily challenges |
| `billing.py` | Payments |
| `analytics_admin.py` | Admin analytics |
| `health.py` | Health checks |

### Merge
| Legacy Route | Merge Into | Reason |
|-------------|-----------|--------|
| `atoms.py`, `concepts.py`, `unified_learning.py`, `curriculum.py`, `scrimba.py`, `roles.py`, `worlds.py`, `teachwall.py`, `deck.py`, `study.py`, `adaptive_learning.py`, `learner.py`, `journey.py` | `lesson.py` + `learning_modules.py` | Single lesson/mission engine |
| `aptitude.py`, `aptitude_tests.py`, `cs_fundamentals.py`, `tcs_nqt.py`, `tracks.py`, `arena.py`, `quiz.py`, `daily_problem.py` | `questions.py` + `coding.py` | Unified practice/assessment |
| `practice.py`, `features.py`, `playlists.py` | `questions.py` | Practice is question-solving |
| `behavioral.py`, `hr.py`, `assessments.py` | `interview.py` | Interview types |
| `student_features.py`, `student_discount.py`, `free_practice.py` | Merge into relevant routes or delete | Student utilities are product-specific |
| `placement.py`, `placement_calendar.py`, `placement_packs.py`, `placement_questions.py`, `company_tracks.py`, `company_lessons.py`, `companies.py`, `opportunity.py` | `company_prep.py` + `indian_placement.py` | Unified company/role prep |
| `exam_memories.py` | Archive | Crowd-sourced memories not in 4-door model |
| `ai_feedback.py`, `ai_debugger.py` | Keep as AI sub-features | Advanced assistance |
| `evidence.py`, `dsa_fingerprint.py`, `distributions.py`, `personal_dashboard.py` | Merge into `analytics_admin.py` or `gamification.py` | Evidence/readiness |
| `enhanced.py` | Merge into relevant routes | Feature bundle |
| `enterprise.py` | Keep or archive | Not in 4-door MVP |
| `revenue.py`, `tiers.py`, `coupon.py`, `invoices.py` | Keep | Billing |
| `community.py`, `discussions.py` | Archive | Not in 4-door MVP |
| `visualizations.py`, `trace.py` | Keep | DSA Visual Lab |
| `runtime.py`, `metrics.py` | Keep or archive | Infrastructure |

### Archive
- `atoms.py`
- `concepts.py`
- `unified_learning.py`
- `curriculum.py`
- `scrimba.py`
- `roles.py`
- `worlds.py`
- `teachwall.py`
- `deck.py`
- `study.py`
- `adaptive_learning.py`
- `learner.py`
- `journey.py`
- `aptitude.py`
- `aptitude_tests.py`
- `cs_fundamentals.py`
- `tcs_nqt.py`
- `tracks.py`
- `arena.py`
- `quiz.py`
- `daily_problem.py`
- `practice.py`
- `features.py`
- `playlists.py`
- `behavioral.py`
- `hr.py`
- `assessments.py`
- `student_features.py`
- `student_discount.py`
- `free_practice.py`
- `placement.py`
- `placement_calendar.py`
- `placement_packs.py`
- `placement_questions.py`
- `company_tracks.py`
- `company_lessons.py`
- `companies.py`
- `opportunity.py`
- `exam_memories.py`
- `evidence.py`
- `dsa_fingerprint.py`
- `distributions.py`
- `personal_dashboard.py`
- `enhanced.py`
- `community.py`
- `discussions.py`
- `enterprise.py` (unless retained for B2B)

---

## 3. Backend Services

### Keep
| Service | Reason |
|---------|--------|
| `ai_core.py` | AI infrastructure |
| `ai_interview.py` | Interview AI |
| `ai_resume.py` | Resume AI |
| `ai_coding.py` | Coding challenge generation |
| `ai_system_design.py` | System design AI |
| `ai_behavioral.py` | Behavioral AI |
| `ai_tutor.py` | Deterministic tutor |
| `gamification.py` | Diamonds + streak |
| `gamification_core.py` | Pure math/constants |
| `code_executor.py` | Code execution |
| `local_sandbox.py` | Local sandbox |
| `circuit_breaker.py` | Circuit breaker |
| `resilience.py` | Retry wrapper |
| `cache.py` | Cache |
| `question_store.py` | Question bank |
| `auto_verify.py` | Trust pipeline |
| `analytics_service.py` | Analytics |
| `request_metrics.py` | Metrics |
| `usage.py` | Free tier limits |
| `email.py` | Transactional email |
| `invoice.py` | Invoices |
| `coupon.py` | Coupons |
| `websocket_manager.py` | WebSocket |
| `structured_logging.py` | Logging |
| `migrations.py` | Schema migrations |
| `health_checker.py` | Health checks |
| `feature_flags.py` | Feature flags |
| `idempotency.py` | Webhook idempotency |

### Merge
| Legacy Service | Merge Into | Reason |
|----------------|-----------|--------|
| `ai_aptitude.py`, `ai_cover_letter.py`, `ai_project.py`, `ai_feedback.py` | `ai_core.py` or domain routes | Domain AI |
| `behavioral_engine.py`, `behavioral_enhanced.py`, `behavioral_judge.py` | `ai_behavioral.py` | Behavioral evaluation |
| `coding_engine.py`, `code_tracer.py` | `code_executor.py` | Code execution |
| `curriculum.py`, `curriculum_engine.py`, `curriculum_connector.py` | `lesson.py` | Curriculum graph |
| `concept_engine.py`, `concepts.py`, `concept_mastery.py` | Archive | Concepts internal |
| `atom_engine.py`, `atoms.py` | Archive | Atoms internal |
| `lesson.py`, `learning.py`, `learning_paths.py`, `learning_modules.py`, `unified_learning.py`, `adaptive_learning.py`, `adaptive_lesson_planner.py` | Merge into `lesson.py` + `learning_modules.py` | Single lesson engine |
| `journey_engine.py` | `lesson.py` | Journey is lesson progression |
| `study_engine.py`, `study_timer.py` | Archive | Study sessions not in 4-door |
| `spaced_repetition.py` | Keep | SRS |
| `gamification.py` | Simplify | Diamonds only |
| `placement_engine.py`, `skill_assessment.py` | Keep or merge | Placement readiness |
| `application_tracker.py`, `career_profile.py` | Merge into `resume.py` | Career tools |
| `social.py` | Archive | Community not in 4-door |
| `student_discount.py`, `trial.py` | Merge or archive | Student/trial features |
| `docker_sandbox.py`, `code_execution_worker.py` | Keep | Code execution |
| `company_roadmap.py`, `company_content.py`, `company_conversion.py`, `company_exam.py`, `company_atom_map.py` | Merge into `company_prep.py` | Company data |
| `content_corpus.py`, `content_verification.py`, `content_promotion.py`, `content_factory.py` | Keep or archive | Content pipeline |
| `verification_pipeline.py` | Merge into `auto_verify.py` | Trust pipeline |
| `analytics.py`, `analytics_service.py` | Keep | Analytics |
| `websocket_manager.py` | Keep | Real-time |

### Archive
- `ai_aptitude.py`
- `ai_cover_letter.py`
- `ai_project.py`
- `ai_feedback.py`
- `behavioral_engine.py`
- `behavioral_enhanced.py`
- `behavioral_judge.py`
- `coding_engine.py`
- `code_tracer.py`
- `curriculum.py`
- `curriculum_engine.py`
- `curriculum_connector.py`
- `concept_engine.py`
- `concepts.py`
- `concept_mastery.py`
- `atom_engine.py`
- `atoms.py`
- `unified_learning.py`
- `adaptive_learning.py`
- `adaptive_lesson_planner.py`
- `journey_engine.py`
- `study_engine.py`
- `study_timer.py`
- `placement_engine.py`
- `skill_assessment.py`
- `application_tracker.py`
- `career_profile.py`
- `social.py`
- `student_discount.py`
- `trial.py`
- `company_roadmap.py`
- `company_content.py`
- `company_conversion.py`
- `company_exam.py`
- `company_atom_map.py`
- `verification_pipeline.py`
- `content_verification.py`
- `content_promotion.py`
- `content_factory.py`

---

## 4. Database Collections

### Keep
| Collection | Reason |
|------------|--------|
| `users` | User accounts |
| `interviews` | Interview sessions |
| `resumes` | Resume data |
| `gamification` | Diamonds, streak, level |
| `gamification_events` | Immutable ledger |
| `learning_events` | Canonical evidence layer |
| `srs_cards` | Spaced repetition |
| `srs_states` | SRS state |
| `submissions` | Code/problem submissions |
| `solved_problems` | Solved tracking |
| `question_answers` | Question attempts |
| `question_reports` | Bug reports |
| `served_quarantine` | Quarantine IDs |
| `payments` | Payment records |
| `invoices` | Invoices |
| `coupons` | Coupons |
| `processed_webhook_events` | Webhook idempotency |
| `analytics_events` | Analytics |
| `analytics_rollups` | Rollups |
| `service_metrics` | Metrics |
| `audit_logs` | Audit trail |
| `interview_bookings` | Interview bookings |
| `company_mock_tests` | Company mocks |
| `oa_sessions` | OA sessions |
| `aptitude_tests` | Aptitude tests |
| `learning_progress` | Learning progress |
| `user_learning_progress` | Per-module progress |
| `learning_modules` | Module definitions |
| `content_modules` | Content modules |
| `assignments` | Assignments |
| `assignment_submissions` | Assignment submissions |
| `skill_graphs` | Skill graph |
| `usage_tracking` | Usage counters |
| `predictions` | Predictions |
| `referrals` | Referrals |

### Merge
| Legacy Collections | Merge Into | Reason |
|-------------------|-----------|--------|
| `progress`, `user_learning_paths`, `user_company_tracks`, `concept_mastery`, `concept_sessions`, `atom_progress`, `thinkincode_progress` | `learner_state` + `mastery_state` | Consolidate learning state |
| `practice_sessions`, `daily_challenges_users`, `contests`, `contest_entries` | `learning_events` | Activity evidence |
| `community_posts`, `discussions`, `study_groups`, `bookmarks`, `notes` | Archive or merge | Community not in 4-door |
| `alumni_experiences`, `placement_drives`, `drive_trackers` | Archive or merge | Placement content |
| `anime_card_progress`, `anime_cards`, `generated_projects`, `tutor_sessions` | Archive | Legacy gamification/content |
| `cards` | Archive | Legacy |
| `content_tranches` | Keep or archive | Trust pipeline |
| `question_explanations` | Keep | Community explanations |
| `integrity_events` | Keep | OA integrity |
| `repair_missions`, `repair_events`, `user_weaknesses` | Keep | Repair loop |
| `trials`, `discounts` | Archive | Student/trial features |
| `billing_metrics`, `revenue_events` | Keep | Billing analytics |

### Archive
- `progress` (merge into `learner_state`)
- `user_learning_paths` (merge)
- `user_company_tracks` (merge)
- `concept_mastery` (merge)
- `concept_sessions` (merge)
- `atom_progress` (merge)
- `thinkincode_progress` (merge)
- `practice_sessions` (merge)
- `daily_challenges_users` (merge)
- `contests` (archive)
- `contest_entries` (archive)
- `community_posts` (archive)
- `discussions` (archive)
- `study_groups` (archive)
- `bookmarks` (archive)
- `notes` (archive)
- `alumni_experiences` (archive)
- `placement_drives` (archive)
- `drive_trackers` (archive)
- `anime_card_progress` (archive)
- `anime_cards` (archive)
- `generated_projects` (archive)
- `tutor_sessions` (archive)
- `cards` (archive)
- `trials` (archive)
- `discounts` (archive)

---

## 5. API Modules

### Keep
| Module | Maps To |
|--------|---------|
| `authApi` | `/api/v1/auth` |
| `interviewApi` | `/api/v1/interview` |
| `bookingApi` | `/api/v1/interview-booking` |
| `resumeApi` | `/api/v1/resume` |
| `billingApi` | `/api/v1/billing` |
| `codingApi` | `/api/v1/coding` |
| `compilerApi` | `/api/v1/compiler` |
| `questionsApi` | `/api/v1/questions` |
| `gamificationApi` | `/api/v1/gamification` |
| `systemDesignApi` | `/api/v1/system-design` |
| `companyMocksApi` | `/api/v1/company-mocks` |
| `companyPrepExamApi` | `/api/v1/company-prep` |
| `indianPlacementApi` | `/api/v1/indian-placement` |
| `visualizationsApi` | `/api/v1/visualizations` |
| `analyticsApi` | `/api/v1/analytics` |
| `adminContentApi` | `/api/v1/admin/content` |
| `onboardingApi` | `/api/v1/onboarding` |
| `dailyApi` | `/api/v1/daily` |
| `learningEventsApi` | `/api/v1/learning-events` |
| `progressApi` | `/api/v1/progress` |
| `submissionsApi` | `/api/v1/submissions` |

### Archive
| Module | Reason |
|--------|--------|
| `behavioralApi`, `hrApi` | Merge into `interviewApi` |
| `enhancedApi`, `freePracticeApi` | Feature bundle; merge or delete |
| `studentApi` | Student utilities not in 4-door |
| `placementApi` | Merge into `indianPlacementApi` |
| `systemDesignTestsApi` | Merge into `systemDesignApi` |
| `adaptiveApi`, `predictorApi`, `readinessApi` | Merge into `gamificationApi` or `analyticsApi` |
| `personalDashboardApi`, `dsaFingerprintApi` | Merge into `analyticsApi` |
| `playlistsApi` | Merge into `questionsApi` |
| `featuresApi` | Merge into `questionsApi` |
| `learningApi`, `learningModulesApi`, `studyApi` | Merge into `learningEventsApi` |
| `learningPathsApi`, `companyTracksApi` | Merge into `companyPrepExamApi` |
| `freeTrialApi` | Merge into `billingApi` or delete |
| `lessonApi`, `journeyApi`, `missionApi`, `mapApi` | Merge into `learningEventsApi` |
| `assignmentsApi` | Archive or merge |
| `metricsApi` | Infrastructure; keep or archive |
| `tracksApi` | Merge into `companyPrepExamApi` |
| `tcsNqtApi` | Merge into `indianPlacementApi` |
| `companyLessonsApi`, `companyDirectoryApi` | Merge into `companyPrepExamApi` |
| `flatApi`, `flatOverrides` | Delete |
| `examMemoriesApi` | Archive |
| `blogsApi` | Archive or merge |
| `csFundamentalsApi` | Merge into `questionsApi` |
| `animeCardsApi` | Archive |
| `atomsApi`, `curriculumApi` | Archive |
| `tutorApi`, `learnerApi` | Archive or merge |
| `opportunityApi` | Merge into `companyPrepExamApi` |
| `deckApi` | Archive |
| `arenaApi` | Archive |
| `teachwallApi` | Archive |
| `unifiedApi` | Archive |
| `toolsApi` | Merge into `resumeApi` |
| `rolesApi` | Archive |
| `oaApi` | Merge into `interviewApi` |
| `distributionsApi` | Archive or merge |
| `aiDebuggerApi` | Keep as advanced feature |
| `conceptsApi`, `evidenceApi` | Archive |

---

## 6. Services to Simplify

### Gamification
**Current:** diamonds + coins + stars + streak + combo + badges + bosses + power-ups + weekly league + monthly challenges  
**Target:** **diamonds + streak + level + badges only**

- Remove: coins, stars, combo, power-ups, bosses, weekly/monthly league XP
- Keep: diamonds, streak, level, badges, daily login
- `record_practice()` remains the single writer

### Lesson Engine
**Current:** 15+ competing systems  
**Target:** `lesson.py` + `learning_modules.py` only

- `lesson.py`: Vertical-slice lesson engine with 9-step loop
- `learning_modules.py`: Duolingo-style module progression
- All other learning routes/services archive

### Question Bank
**Current:** Multiple overlapping banks  
**Target:** `question_store.py` + file-backed `app/data/`

- Keep: `question_store.py`, `auto_verify.py`
- Remove duplicate bank loaders
- Enforce trust pipeline

### Company Prep
**Current:** 10+ overlapping routes  
**Target:** `company_prep.py` + `indian_placement.py` + `company_mocks.py`

- Merge: `companies.py`, `company_tracks.py`, `company_lessons.py`, `placement.py`, `placement_calendar.py`, `placement_packs.py`, `placement_questions.py`, `opportunity.py`
- Keep: `company_prep.py`, `company_mocks.py`, `indian_placement.py`

---

## 7. FRONTEND ARCHITECTURE

### 5-Environment Model (Simplified)

```
WORLD — Learn Coding journey
LAB — Lesson player, practice, compiler
ARENA — Challenges, mock OA, contests
COMMAND — Today, readiness, progress
CAREER — Resume, interview, company prep
```

### DSA Visual Lab
Standalone section, not part of gamified progression.

### Providers
Keep: ErrorBoundary, Toast, Theme, Background, Juice, Router  
Remove: Any provider tied to archived features

### State
- Zustand: auth only
- React Query: server state
- No client-side reward math

---

## 8. WHAT TO DELETE FIRST

### High Confidence Deletes
1. `anime_cards` collection + all routes/services/pages
2. `atoms.py`, `concepts.py`, `unified_learning.py`, `curriculum.py`, `scrimba.py`, `roles.py`, `worlds.py`, `teachwall.py`, `deck.py`, `study.py`, `adaptive_learning.py`, `learner.py`, `journey.py`
3. `aptitude.py`, `aptitude_tests.py`, `cs_fundamentals.py`, `tcs_nqt.py`, `tracks.py`, `arena.py`, `quiz.py`, `daily_problem.py`
4. `practice.py`, `features.py`, `playlists.py`
5. `behavioral.py`, `hr.py`, `assessments.py`
6. `student_features.py`, `student_discount.py`, `free_practice.py`
7. `placement.py`, `placement_calendar.py`, `placement_packs.py`, `placement_questions.py`, `company_tracks.py`, `company_lessons.py`, `companies.py`, `opportunity.py`
8. `exam_memories.py`
9. `evidence.py`, `dsa_fingerprint.py`, `distributions.py`, `personal_dashboard.py`
10. `community.py`, `discussions.py`
11. `enhanced.py`
12. `enterprise.py` (unless retained)
13. Frontend: all archived pages listed in Section 1

### Archive First (Don’t Delete)
1. `archive/legacy_learning_systems/` — all merged learning routes/services
2. `archive/legacy_pages/` — all archived pages
3. `archive/legacy_collections/` — schema backups before dropping collections

---

## 9. MIGRATION SEQUENCE

### Phase 1 — Freeze Constitution
1. Create `ARCHITECTURE_CONSTITUTION.md` ✅
2. Create this migration map ✅
3. Get architectural approval

### Phase 2 — Archive Legacy
1. Move legacy routes to `archive/legacy_routes/`
2. Move legacy services to `archive/legacy_services/`
3. Move legacy pages to `archive/legacy_pages/`
4. Export legacy collection schemas to `archive/legacy_collections/`
5. Update `main.py` route auto-discovery to exclude `archive/`

### Phase 3 — Simplify Gamification
1. Remove coins, stars, combo, power-ups from `gamification.py`
2. Remove power-up routes
3. Simplify frontend juice/overlays
4. Migrate existing user data: coins → diamonds (if needed)

### Phase 4 — Consolidate Learning
1. Merge lesson routes into `lesson.py` + `learning_modules.py`
2. Consolidate learning collections
3. Simplify frontend to `LessonPlayer` + `LearningModules`

### Phase 5 — Consolidate Company Prep
1. Merge company routes into `company_prep.py` + `indian_placement.py`
2. Simplify frontend to `CompanyPrepHub` + `CompanyTrack`

### Phase 6 — Simplify Economy
1. Remove power-up shop
2. Remove boss battles (or keep as simple level markers)
3. Remove weekly/monthly leagues
4. Keep diamonds + streak + level + badges

### Phase 7 — Clean Up API Modules
1. Reduce `services/api/index.ts` to ~20 modules
2. Remove dead API modules
3. Update frontend to use canonical modules

### Phase 8 — Verify
1. Run student flow: signup → onboarding → Learn Coding → first lesson → quiz → practice → diamonds → next level
2. Run student flow: signup → onboarding → Service-Based Prep → assessment → mission → practice
3. Run student flow: signup → onboarding → Company Prep → company mock
4. Run student flow: signup → onboarding → DSA Visual Lab → visualize → predict
5. Verify data persists at every arrow
6. Verify no legacy routes are reachable
7. Verify no legacy collections are written to

---

## 10. NON-NEGOTIABLES

1. **Four doors only.** No fifth door.
2. **Six technologies.** No 20-language catalogue.
3. **6 modules × 32 levels.** Not 100 levels × 80 modules.
4. **One currency: Diamonds.** No coins, stars, combo, power-up shop.
5. **One lesson engine.** Not 15 competing systems.
6. **One learner state.** Not 20 collections.
7. **One question bank.** File-backed, in-memory serving.
8. **Deterministic beginner curriculum.** No AI for core lessons.
9. **Captain Byte is deterministic.** No hallucinations, no token costs.
10. **Verified means verified.** Compile-passes are not evidence.

---

*This document is the reset. All prior architecture docs, strategy docs, and feature inventories are superseded.*
