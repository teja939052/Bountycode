# BountyCode — Dual Database Retirement Readiness (Phase 7, PART H)

## Route Persistence Ownership Matrix

### ✅ PostgreSQL Authoritative (Migrated)

| Route File | Routes | Persistence Layer | Status |
|------------|--------|-------------------|--------|
| `routes/auth.py` | 15 routes (register, login, refresh, logout, me, update-profile, change-password, forgot-password, reset-password, onboarding-status, onboarding-complete, verify-email, google, google/callback) | PostgreSQL (`users` table via `PostgresAuthService`) | **Complete** |
| `routes/coding.py` | 7 routes (topics, start, submit, hint, interviewer-review, solution, history) | PostgreSQL (`coding_submissions` + `execution_results` via `PostgresAssessmentService`) | **Complete** |

### ⚠️ Partially Migrated (XP Writer on PostgreSQL, Data Still on MongoDB)

| Route File | Routes | Persistence Layer | Remaining Motor Usage |
|------------|--------|-------------------|----------------------|
| `routes/aptitude_tests.py` | start, answer, complete, leaderboard | Motor (`aptitude_tests_collection`, `aptitude_leaderboard_collection`) | Test CRUD on MongoDB; XP via `pg_record_practice` |
| `routes/interview.py` | start, answer, result, history | Motor (`interviews_collection`, `interview_chat_sessions_collection`) | Interview CRUD on MongoDB; XP via `pg_record_practice` |
| `routes/interview_chat.py` | start, submit_turn, end_session | Motor (`interview_chat_sessions_collection`, `interviews_collection`) | Chat session CRUD on MongoDB; XP via `pg_record_practice` |
| `routes/interview_booking.py` | book, submit_answers, etc. | Motor (`interview_bookings_collection`, `interviews_collection`) | Booking CRUD on MongoDB; XP via `pg_record_practice` |
| `routes/resume.py` | upload, generate, optimize, export | Motor (`resumes_collection`, `users_collection`) | Resume CRUD on MongoDB; XP via `pg_record_practice` |
| `routes/daily_challenge.py` | submit, complete-day, leagues | Motor (`solved_problems_collection`, `gamification_collection`, `daily_challenges_users_collection`) | Challenge data on MongoDB; XP via `pg_record_practice` |
| `routes/daily_problem.py` | submit | Motor (`solved_problems_collection`, `gamification_collection`) | Problem data on MongoDB; XP via `pg_record_practice` |
| `routes/gamification.py` | record, profile | Motor (`gamification_collection`) | Profile CRUD on MongoDB; XP via `pg_record_practice` |
| `routes/company_lessons.py` | lesson CRUD | Motor (various collections) | Lesson data on MongoDB |
| `routes/learning_modules.py` | module CRUD | Motor (`learning_modules_collection`, `user_learning_progress_collection`) | Module/progress data on MongoDB |
| `routes/lessons.py` | lesson CRUD | Motor (via `lesson_service`) | Lesson data on MongoDB |
| `routes/company_mocks.py` | mock test CRUD | Motor (`company_mock_tests_collection` via `db["company_mock_tests"]`) | Mock test data on MongoDB |
| `routes/oa.py` | OA session CRUD | Motor (`oa_sessions_collection`, `integrity_events_collection`) | OA session data on MongoDB |

### ❌ Unmigrated (Motor Only)

| Route File | Routes | Persistence Layer |
|------------|--------|-------------------|
| `routes/academy_plan.py` | plan CRUD | Motor (`_profiles()`, `_diagnostics()`, `srs_cards_collection()`, `_plans()`) |
| `routes/academy_profile.py` | profile CRUD | Motor (`_profiles()`) |
| `routes/academy_diagnostic.py` | diagnostic CRUD | Motor (`_sessions()`) |
| `routes/admin_content.py` | content/assignment CRUD | Motor (`content_tranches_collection`, `content_modules_collection()`, `assignments_collection()`, `assignment_submissions_collection()`, `users_collection()`) |
| `routes/admin_monitoring.py` | admin analytics | Motor (`db["users"]`, `db["billing_transactions"]`) |
| `routes/billing.py` | billing/payment CRUD | Motor (`users_collection`, `payments_collection`) |
| `routes/company_directory.py` | directory CRUD | Motor (`users_collection`) |
| `routes/community.py` | community posts | Motor (`db["community_posts"]`) |
| `routes/worlds.py` | world/gamification | Motor (various collections) |
| `routes/system_design_tests.py` | system design | Motor (various collections) |
| `routes/quiz.py` | quiz CRUD | Motor (various collections) |
| `routes/admin_content.py` | assignments | Motor (various collections) |
| `routes/exam_memories.py` | exam memories | Motor (various collections) |
| `routes/language_paths.py` | language learning | Motor (various collections) |
| `routes/study_engine.py` | study engine | Motor (various collections) |
| `routes/role_content_service.py` | role content | Motor (various collections) |
| `routes/company_conversion.py` | company conversion | Motor (various collections) |

## Service-Level Motor References

### ✅ PostgreSQL Services (No Motor)
- `services/postgres_auth.py` — `PostgresAuthService` (users table)
- `services/postgres_gamification.py` — `PostgresGamificationService` (gamification_profiles, xp_event_ledger)
- `services/postgres_learning.py` — `PostgresLearningService` (learning_attempts, learning_evidence)
- `services/postgres_assessments.py` — `PostgresAssessmentService` (assessment_attempts, responses, coding_submissions, execution_results, oa_sessions, interview_sessions)

### ⚠️ Mixed Services (PostgreSQL + Motor)

| Service File | Motor Usage | PostgreSQL Usage |
|-------------|-------------|-----------------|
| `services/gamification.py` | `record_practice()` — full MongoDB implementation | None (replaced by `postgres_gamification.py`) |
| `services/learning.py` | MongoDB for lesson progress | None |
| `services/lesson.py` | MongoDB for lesson operations | None |
| `services/learning_paths.py` | MongoDB for learning paths | None |

### ❌ Motor-Only Services
- `services/ai_interview.py` — MongoDB for interview context
- `services/analytics_service.py` — MongoDB for analytics events
- `services/career_profile.py` — MongoDB for career profiles
- `services/company_conversion.py` — MongoDB for company mock tests
- `services/adaptive_learning.py` — MongoDB for skill graphs
- `services/daily_drill.py` — MongoDB for gamification profiles
- `services/request_metrics.py` — MongoDB for service metrics

## Remaining Motor Collection References (by collection)

| Collection | Routes/Services Using It | Migration Status |
|------------|-------------------------|-----------------|
| `users` | auth.py (migrated), billing.py, admin_monitoring.py, company_directory.py, resume.py, company_mocks.py, daily_challenge.py, etc. | Partially migrated (auth done, others pending) |
| `gamification` | gamification.py, daily_challenge.py, daily_problem.py, resume.py | Partially (XP writer moved to PostgreSQL, profile still Motor) |
| `coding_challenges` | coding.py (migrated) | Migrated |
| `oa_sessions` | oa.py | Not migrated |
| `interviews` | interview.py, interview_chat.py, interview_booking.py, oa.py | Not migrated |
| `interview_bookings` | interview_booking.py | Not migrated |
| `interview_chat_sessions` | interview_chat.py | Not migrated |
| `company_mock_tests` | company_mocks.py | Not migrated |
| `aptitude_tests` | aptitude_tests.py | Not migrated |
| `solved_problems` | daily_challenge.py, daily_problem.py, distributions.py, dsa_fingerprint.py | Not migrated |
| `submissions` | distributions.py, dsa_fingerprint.py | Not migrated |
| `learning_modules` | learning_modules.py | Not migrated |
| `user_learning_progress` | learning_modules.py | Not migrated |
| `resumes` | resume.py | Not migrated |
| `payments` | billing.py | Not migrated |
| `repair_missions` | ai_interview.py | Not migrated |
| `srs_cards` | academy_plan.py | Not migrated |
| `analytics_events` | analytics_service.py | Not migrated |
| `audit_logs` | audit_log.py | Not migrated |

## Migration Readiness Assessment

### Blocks to Full Migration

1. **Auth routes fully migrated** — registration, login, refresh, logout, profile all use PostgreSQL
2. **Coding routes fully migrated** — start, submit, hint, solution, history all use PostgreSQL
3. **XP writer on PostgreSQL** — `PostgresGamificationService.record_practice()` is the single authoritative XP writer; all 30+ callers updated
4. **Assessment repositories ready** — `PostgresAssessmentService` provides all assessment persistence methods

### Remaining Work for Full Migration

1. Migrate `aptitude_tests.py` persistence from Motor to `PostgresAssessmentService`
2. Migrate `interview.py` persistence from Motor to `PostgresAssessmentService`
3. Migrate `interview_chat.py` persistence from Motor to `PostgresAssessmentService`
4. Migrate `interview_booking.py` persistence from Motor to `PostgresAssessmentService`
5. Migrate `company_mocks.py` persistence from Motor to `PostgresAssessmentService`
6. Migrate `oa.py` persistence from Motor to `PostgresAssessmentService`
7. Migrate `resume.py` persistence from Motor to PostgreSQL (`resumes` table)
8. Migrate `daily_challenge.py` and `daily_problem.py` persistence from Motor
9. Migrate `learning_modules.py` and `lessons.py` persistence from Motor to `PostgresLearningService`
10. Migrate remaining admin/billing/career routes from Motor

### Dual-Database Safety

- No route pretends a PostgreSQL transaction spans MongoDB
- `PostgresAssessmentService.award_xp()` uses `pg_record_practice()` which writes to PostgreSQL only
- No silent Motor fallback in PostgreSQL services
- All PostgreSQL writers flush but never commit (caller owns transaction boundary)
