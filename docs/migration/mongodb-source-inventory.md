# BountyCode — MongoDB Source Inventory (Phase 6, PART A)

Complete inventory of every MongoDB collection declaration and active consumer.
Generated from `backend/app/database.py` (lazy collection proxies) and
grep-based consumer search across `backend/app/routes/` and `backend/app/services/`.

## Legend

| Column | Meaning |
|--------|---------|
| **Status** | Active = read/written by at least one active route or service; Legacy = declared but no active consumers; Uncertain = declared, consumer unclear |
| **Priority** | Import priority for Phase 6 importer (1=highest, 5=lowest) |
| **PG Destination** | Target PostgreSQL table (from the 41-table schema) |

---

## ═════════════════════════════════════════════════════════════════════════════
# 1. IDENTITY AND USERS
# ═════════════════════════════════════════════════════════════════════════════

### users
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `users` (via `User` model)
- **Declared:** `database.py:265` — `users_collection = _LazyCollection("users")`
- **Consumers (read/write):**
  - `routes/auth.py` — register, login, profile update, password change, email verification, Google OAuth
  - `routes/billing.py` — plan updates, coupon application, payment linking
  - `routes/admin_monitoring.py` — user counts, active user listing
  - `routes/admin_content.py` — user lookup for submissions
  - `routes/company_directory.py` — user directory
  - `routes/daily_challenge.py` — user challenge data
  - `services/adaptive_learning.py` — user lookup by ObjectId
  - `services/ai_interview.py` — skill graph + user context
  - `services/analytics_service.py` — user counts, aggregation
  - `services/career_profile.py` — user ownership
  - `services/company_conversion.py` — user updates, lookup
  - `services/coupon.py` — coupon application to user
  - `services/analytics.py` — user analytics
- **Relationships:** Referenced by nearly every collection via `user_id` (string) or `_id` (ObjectId)
- **TTL:** None
- **Notes:** Contains password hashes — must be handled with care during migration. Preserve algorithm compatibility.

---

## ═════════════════════════════════════════════════════════════════════════════
# 2. AUTHENTICATION RECORDS
# ══════════════════════════════════════════════════════════════════════════════

### No dedicated auth collection
- Auth state lives in `users` collection (password hash, email verification token, reset token)
- JWT refresh tokens are NOT stored in MongoDB (cookie-based, stateless JWT)
- **Status:** N/A (auth writes go through `users` collection)
- **Important:** Do NOT import old refresh-token sessions as active sessions (Phase 6, PART F)

---

## ═════════════════════════════════════════════════════════════════════════════
# 3. GAMIFICATION
# ══════════════════════════════════════════════════════════════════════════════

### gamification
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `gamification_profiles` + `xp_event_ledger`
- **Declared:** `database.py:276` — `gamification_collection = _LazyCollection("gamification")`
- **Consumers (read/write):**
  - `routes/daily_challenge.py` — XP/stream updates on challenge completion
  - `routes/daily_problem.py` — gamification updates
  - `routes/worlds.py` — gamification data for world view
  - `services/adaptive_learning.py` — gamification profile lookup
  - `services/ai_interview.py` — gamification context
  - `services/analytics.py` — gamification counts
  - `services/company_conversion.py` — gamification updates on mock test completion
  - `services/daily_drill.py` — gamification profile lookup
  - `services/gamification.py` — `record_practice()` — THE single authoritative XP writer (writes profile + events)
- **Important fields:** `user_id`, `xp`, `level`, `streak`, `coins`, `stars`, `combo`, `badges`, `bosses_defeated`
- **Relationships:** `user_id` → `users`
- **TTL:** None

### gamification_events
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `xp_event_ledger`
- **Declared:** `database.py:277` and `database.py:356` — `gamification_events_collection`
- **Consumers (write):**
  - `services/gamification.py:848` — `record_practice()` inserts event after profile update (best-effort, never blocks award)
- **Important fields:** `user_id`, `activity_type`, `score`, `xp_awarded`, `coins_awarded`, `metadata`, `reward_policy_version`, `created_at`
- **Relationships:** `user_id` → `users`
- **TTL:** None
- **Notes:** Event emission is best-effort — can be missing even when profile was updated. Migration must handle gaps.

---

## ═════════════════════════════════════════════════════════════════════════════
# 4. SKILL GRAPH AND LEARNING
# ══════════════════════════════════════════════════════════════════════════════

### skill_graphs
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `skills` (+ skill-state tracking)
- **Declared:** `database.py:275` — `skill_graph_collection = _LazyCollection("skill_graphs")`
- **Consumers (read/write):**
  - `routes/daily_challenge.py` — skill graph lookup/update
  - `routes/enterprise.py` — skill graph reads
  - `routes/worlds.py` — skill graph for world view
  - `services/adaptive_learning.py` — skill graph reads/writes
  - `services/ai_interview.py` — skill graph context for interview generation
  - `services/analytics.py` — skill graph counts
  - `services/company_conversion.py` — skill graph reads/writes
- **Important fields:** `user_id`, skill tree data, mastery levels, prerequisites
- **Relationships:** `user_id` → `users`

### learning_progress (aka user_learning_progress)
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `skill_states` / `learning_progress` tables
- **Declared:** `database.py:293` — `learning_progress_collection`; `database.py:316` — `user_learning_progress_collection`
- **Consumers (read/write):**
  - `services/adaptive_learning.py` — progress reads/writes
  - `services/learning.py` — lesson progress CRUD (heavy user)
  - `services/learning_paths.py` — progress lookup
  - `services/lesson_service.py` — progress reads/writes
  - `routes/company_lessons.py` — lesson progress CRUD
  - `routes/learning_modules.py` — progress CRUD
- **Important fields:** `user_id`, lesson/module ID, progress percentage, completion status, timestamps

### learning_events
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `learning_attempts` + `learning_evidence`
- **Declared:** `database.py:355` — `learning_events_collection = _LazyCollection("learning_events")`
- **Consumers:**
  - `routes/journey.py` — learning event recording
- **Relationships:** `user_id` → `users`, skill references

---

## ════════════════════════════════════════════════════════════════════════════
# 5. LEARNING ATTEMPTS AND EVIDENCE
# ══════════════════════════════════════════════════════════════════════════════

### learning_progress / user_learning_progress
- Covered in section 4 above. Stores lesson-level progress, not assessment attempts.

### srs_states / srs_cards
- **Status:** Active
- **Priority:** 2
- **PG Destination:** `srs_cards` table
- **Declared:** `database.py:344` — `srs_collection = _LazyCollection("srs_states")`; `database.py:345` — `srs_cards_collection = _LazyCollection("srs_cards")`
- **Consumers:** Declared but no active route/service consumers found in search results. May be used by SRS service not yet surfaced.
- **Notes:** Verify before import.

### repair_missions
- **Status:** Active
- **Priority:** 2
- **PG Destination:** `repair_missions` table
- **Declared:** `database.py:358` — `repair_missions_collection = _LazyCollection("repair_missions")`
- **Consumers (read):**
  - `services/ai_interview.py:196` — `repair_missions_collection.find()` for repair context
- **Relationships:** `user_id` → `users`

---

## ════════════════════════════════════════════════════════════════════════════
# 6. CODING SUBMISSIONS
# ══════════════════════════════════════════════════════════════════════════════

### coding_challenges
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `coding_submissions` + `execution_results`
- **Declared:** `database.py:274` — `coding_challenges_collection = _LazyCollection("coding_challenges")`
- **Consumers (read/write):**
  - `routes/coding.py` — ALL coding challenge operations (create, read, update, list)
  - `services/analytics.py` — coding challenge counts
- **Important fields:** `user_id`, `challenge_id` (question identity), `code`, `language`, `status`, `execution_result`, `score`, timestamps
- **Relationships:** `user_id` → `users`, `challenge_id` → question bank
- **Security:** Must NOT migrate protected/hidden test cases to publicly accessible fields

### submissions
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `coding_submissions` (consolidated)
- **Declared:** `database.py:292` — `submissions_collection = _LazyCollection("submissions")`
- **Consumers (read):**
  - `routes/distributions.py` — submission distribution analytics
  - `routes/dsa_fingerprint.py` — DSA skill assessment
  - `services/adaptive_learning.py` — submission history
- **Notes:** May overlap with `coding_challenges`. Deduplicate during import.

---

## ════════════════════════════════════════════════════════════════════════════
# 7. APTITUDE AND SQL ASSESSMENTS
# ══════════════════════════════════════════════════════════════════════════════

### aptitude_tests
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `assessment_attempts` (aptitude variant)
- **Declared:** `database.py:268` — `aptitude_collection`; `database.py:308` — `aptitude_tests_collection`
- **Consumers (read/write):**
  - `routes/aptitude_tests.py` — ALL aptitude test operations (start, answer, complete)
- **Important fields:** `user_id`, `category`, `questions`, `question_ids`, `answers`, `status`, `score`, `time_limit_minutes`, timestamps
- **Relationships:** `user_id` → `users`

### aptitude_leaderboard
- **Status:** Active
- **Priority:** 3
- **PG Destination:** `aptitude_leaderboard` table (if exists in 41-table schema)
- **Declared:** `database.py:307` — `aptitude_leaderboard_collection`
- **Consumers:** Declared, no active consumers found in search
- **Notes:** Verify before import

### system_design_tests / system_design_leaderboard
- **Status:** Active (declared)
- **Priority:** 3
- **PG Destination:** `system_design_tests` table
- **Declared:** `database.py:309` and `database.py:310`
- **Consumers:** Declared, no active consumers found in search
- **Notes:** Verify before import

---

## ═════════════════════════════════════════════════════════════════════════════
# 8. ONLINE ASSESSMENT (OA) SESSIONS
# ══════════════════════════════════════════════════════════════════════════════

### oa_sessions
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `oa_sessions`
- **Declared:** `database.py:349` — `oa_sessions_collection = _LazyCollection("oa_sessions")`
- **Consumers (read/write):**
  - `routes/oa.py` — OA session CRUD
  - `routes/interview.py` — OA session reads
  - `services/ai_interview.py:208` — `oa_sessions_collection.find()` for interview context
- **Important fields:** `user_id`, `company`, `role`, `blueprint`, `questions`, `status`, `started_at`, `completed_at`, integrity signals
- **Security:** Private candidate information (integrity signals) must be protected
- **Relationships:** `user_id` → `users`

### integrity_events
- **Status:** Active (declared)
- **Priority:** 3
- **PG Destination:** Part of `oa_sessions` (JSONB) or separate table
- **Declared:** `database.py:350` — `integrity_events_collection`
- **Consumers:** Declared, no active consumers found in search
- **Notes:** Verify before import

---

## ════════════════════════════════════════════════════════════════════════════
# 9. INTERVIEW SESSIONS
# ══════════════════════════════════════════════════════════════════════════════

### interviews
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `interview_sessions`
- **Declared:** `database.py:266` — `interviews_collection = _LazyCollection("interviews")`
- **Consumers (read/write):**
  - `routes/interview.py` — interview session CRUD
  - `routes/interview_booking.py` — interview booking reads/writes
  - `routes/interview_chat.py` — interview chat session reads/writes
  - `services/ai_interview.py:225` — `interviews_collection.find()` for interview history
- **Important fields:** `user_id`, `interview_type`, `role`, `company`, `difficulty`, `questions`, `responses`, `evaluation`, `feedback`, `status`, timestamps
- **Security:** PII in transcripts and feedback must be handled carefully. Never store API keys/provider secrets.
- **Relationships:** `user_id` → `users`
- **Access control:** User must never access another user's interview session

### interview_bookings
- **Status:** Active
- **Priority:** 2
- **PG Destination:** `interview_bookings` table
- **Declared:** `database.py:317` — `interview_bookings_collection`
- **Consumers (read/write):**
  - `routes/interview_booking.py` — ALL booking operations (create, read, update, cancel, list)
- **Important fields:** `user_id`, `scheduled_at`, `company`, `role`, `interview_type`, `status`

### interview_chat_sessions
- **Status:** Active
- **Priority:** 2
- **PG Destination:** Part of `interview_sessions` or separate table
- **Declared:** `database.py:325` — `interview_chat_sessions_collection`
- **Consumers (read/write):**
  - `routes/interview_chat.py` — ALL chat session operations
- **Important fields:** `user_id`, `session_id`, `messages`, `status`, timestamps

---

## ════════════════════════════════════════════════════════════════════════════
# 10. COMPANY PREPARATION
# ══════════════════════════════════════════════════════════════════════════════

### company_mock_tests
- **Status:** Active
- **Priority:** 1
- **PG Destination:** `assessment_attempts` (company mock variant) + `oa_sessions`
- **Declared:** `database.py:283` — `company_mock_tests_collection`
- **Consumers (read/write):**
  - `routes/company_mocks.py` — company mock test CRUD
  - `services/company_conversion.py` — company mock test creation, reads, updates
  - `services/analytics.py` — mock test counts
- **Important fields:** `user_id`, `company`, `role`, `assessment_type`, `questions`, `status`, `score`, source provenance, verification date, confidence
- **Security:** Never claim leaked/private company questions are official. Retain `source`, `verification_date`, `confidence` where they exist.

### company_prep
- **Status:** Declared, unclear usage
- **Priority:** 4
- **PG Destination:** `company_assessment_metadata`
- **Declared:** `database.py:273` — `company_prep_collection`
- **Consumers:** No active consumers found in search
- **Notes:** Verify before import

---

## ═════════════════════════════════════════════════════════════════════════════
# 11. CAREER PROFILES
# ══════════════════════════════════════════════════════════════════════════════

### career_profiles
- **Status:** Active
- **Priority:** 2
- **PG Destination:** `career_profiles`
- **Declared:** `database.py:286` — `career_profiles_collection`
- **Consumers (read/write):**
  - `services/career_profile.py` — ALL career profile operations (create, read, update)
- **Important fields:** `user_id`, skills, experience, portfolio, preferences
- **Relationships:** `user_id` → `users`

### resumes
- **Status:** Active
- **Priority:** 2
- **PG Destination:** `resumes` + `resume_uploads` (file metadata)
- **Declared:** `database.py:267` — `resumes_collection`
- **Consumers (read):**
  - `routes/cover_letter.py` — resume lookup
  - `services/analytics.py` — resume counts
  - `services/career_profile.py` — resume reads
- **Notes:** File metadata only — actual file objects stored separately (see PART I)

### cover_letters
- **Status:** Declared, unclear usage
- **Priority:** 4
- **PG Destination:** `cover_letters` table
- **Declared:** `database.py:269` — `cover_letters_collection`
- **Consumers:** No active consumers found in search
- **Notes:** Verify before import

---

## ═════════════════════════════════════════════════════════════════════════════
# 12. ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

### analytics_events
- **Status:** Active
- **Priority:** 3
- **PG Destination:** `analytics_events`
- **Declared:** `database.py:294` — `analytics_events_collection`
- **Consumers (read/write):**
  - `services/analytics_service.py` — ALL analytics event operations (insert, aggregate, query)
- **Important fields:** `user_id`, `event_type`, `event_data`, `created_at`
- **Relationships:** `user_id` → `users`

### analytics_rollups
- **Status:** Active
- **Priority:** 3
- **PG Destination:** `analytics_rollups`
- **Declared:** `database.py:295` — `analytics_rollups_collection`
- **Consumers (read/write):**
  - `services/analytics_service.py` — rollup reads/writes
- **Important fields:** rollup key, aggregated metrics, timestamps

### service_metrics
- **Status:** Active
- **Priority:** 4
- **PG Destination:** `service_metrics`
- **Declared:** `database.py:296` — `service_metrics_collection`
- **Consumers (write):**
  - `services/request_metrics.py` — service metrics recording
- **Notes:** Operational telemetry, lower import priority

---

## ═════════════════════════════════════════════════════════════════════════════
# 13. APPLICATIONS AND JOBS
# ══════════════════════════════════════════════════════════════════════════════

### applications
- **Status:** Active
- **Priority:** 3
- **PG Destination:** `job_applications` (application tracker)
- **Declared:** `database.py:297` — `applications_collection`
- **Consumers (read/write):**
  - `services/application_tracker.py` — application CRUD
  - `services/analytics.py` — application counts
  - `services/analytics_service.py` — application aggregation
- **Important fields:** `user_id`, `company`, `role`, `status`, `applied_at`

---

## ═════════════════════════════════════════════════════════════════════════════
# 14. BILLING RECORDS
# ══════════════════════════════════════════════════════════════════════════════

### payments
- **Status:** Active
- **Priority:** 2
- **PG Destination:** `payments`
- **Declared:** `database.py:327` — `payments_collection`
- **Consumers (read/write):**
  - `routes/billing.py` — payment records, status updates
  - `services/coupon.py` — payment lookups
- **Important fields:** `user_id`, `amount`, `status`, `transaction_id`, timestamps
- **Security:** Financial data — handle with care

### coupons
- **Status:** Active
- **Priority:** 3
- **PG Destination:** `coupons`
- **Declared:** `database.py:330` — `coupons_collection`
- **Consumers (read/write):**
  - `routes/billing.py` — coupon validation/application
  - `services/coupon.py` — coupon CRUD
- **Important fields:** `code`, `discount_type`, `value`, `valid_until`, `usage_limit`

### invoices
- **Status:** Declared, unclear usage
- **Priority:** 3
- **PG Destination:** `invoices`
- **Declared:** `database.py:354` — `invoices_collection`
- **Consumers:** No active consumers found in search
- **Notes:** Verify before import

### revenue_events
- **Status:** Declared, unclear usage
- **Priority:** 4
- **PG Destination:** `revenue_events`
- **Declared:** `database.py:328` — `revenue_events_collection`
- **Consumers:** No active consumers found in search
- **Notes:** Verify before import

### billing_metrics
- **Status:** Declared, unclear usage
- **Priority:** 4
- **PG Destination:** `billing_metrics`
- **Declared:** `database.py:329` — `billing_metrics_collection`
- **Consumers:** No active consumers found in search
- **Notes:** Verify before import

---

## ═════════════════════════════════════════════════════════════════════════════
# 15. AUDIT RECORDS
# ══════════════════════════════════════════════════════════════════════════════

### audit_logs
- **Status:** Active
- **Priority:** 3
- **PG Destination:** `audit_logs`
- **Declared:** `database.py:346` — `audit_logs_collection`
- **Consumers (write):**
  - `services/audit_log.py` — audit log insertion and querying
- **Important fields:** `user_id`, `action`, `resource`, `timestamp`, metadata

---

## ═════════════════════════════════════════════════════════════════════════════
# 16. DECLARED BUT NOT ACTIVELY CONSUMED (Legacy / Verify)
# ══════════════════════════════════════════════════════════════════════════════

The following collections are declared in `database.py` but had NO active consumers
found in the routes/services search. They are likely legacy from removed features
(August 2026 cleanup) or used by code outside the searched paths:

| Collection | Declared Line | Status | Recommendation |
|------------|--------------|--------|----------------|
| resumes | 267 | Active (partial) | Import |
| cover_letters | 269 | Uncertain | Verify |
| system_design | 271 | Uncertain | Verify |
| offers | 272 | Uncertain | Verify |
| skill_graphs | 275 | Active | Import |
| usage_tracking | 278 | Uncertain | Verify |
| predictions | 279 | Uncertain | Verify |
| prediction_outcomes | 280 | Uncertain | Verify |
| curated_questions | 281 | Uncertain | Verify |
| question_answers | 282 | Uncertain | Verify |
| alumni_experiences | 284 | Uncertain | Verify |
| placement_drives | 285 | Uncertain | Verify |
| practice_sessions | 287 | Uncertain | Verify |
| mock_tests | 288 | Uncertain | Verify |
| trials | 289 | Uncertain | Verify |
| discounts | 290 | Uncertain | Verify |
| learning_modules | 315 | Uncertain | Verify |
| interview_bookings | 317 | Active | Import |
| language_modules | 318 | Uncertain | Verify |
| language_levels | 319 | Uncertain | Verify |
| language_progress | 320 | Uncertain | Verify |
| content_modules | 321 | Uncertain | Verify |
| assignments | 322 | Uncertain | Verify |
| assignment_submissions | 323 | Active (admin_content) | Import |
| question_explanations | 324 | Uncertain | Verify |
| user_deadlines | 326 | Uncertain | Verify |
| revenue_events | 328 | Uncertain | Verify |
| billing_metrics | 329 | Uncertain | Verify |
| referrals | 331 | Uncertain | Verify |
| chat_messages | 332 | Uncertain | Verify |
| gd_rooms | 333 | Uncertain | Verify |
| gd_ratings | 334 | Uncertain | Verify |
| cgpa_calculations | 335 | Uncertain | Verify |
| drive_trackers | 336 | Uncertain | Verify |
| peer_reviews | 337 | Uncertain | Verify |
| study_squads | 338 | Uncertain | Verify |
| achievements | 339 | Uncertain | Verify |
| shares | 340 | Uncertain | Verify |
| pulse_battles | 341 | Uncertain | Verify |
| pulse_daily | 342 | Uncertain | Verify |
| debug_logs | 343 | Uncertain | Verify |
| srs_states | 344 | Uncertain | Verify |
| srs_cards | 345 | Active (academy_plan) | Import |
| audit_logs | 346 | Active | Import |
| friend_requests | 347 | Uncertain | Verify |
| friends | 348 | Uncertain | Verify |
| integrity_events | 350 | Uncertain | Verify |
| daily_quests | 351 | Uncertain | Verify |
| content_tranches | 352 | Uncertain | Verify |
| exam_memories | 353 | Uncertain | Verify |
| learning_events | 355 | Active (journey) | Import |
| gamification_events | 356 | Active | Import |
| question_reports | 357 | Uncertain | Verify |
| season_xp | 359 | Uncertain | Verify |
| served_quarantine | 360 | Uncertain | Verify |
| user_company_tracks | 361 | Uncertain | Verify |
| user_learning_paths | 362 | Uncertain | Verify |
| user_weaknesses | 363 | Uncertain | Verify |

**Intentional exclusions:** All "Uncertain" collections above are intentionally excluded from the initial import scope. They should be verified individually before any import attempt.

---

## ═════════════════════════════════════════════════════════════════════════════
# COLLECTION-TO-TABLE MAPPING SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

| MongoDB Collection | PostgreSQL Table | Priority | Status |
|-------------------|-----------------|----------|--------|
| users | users | 1 | Active |
| gamification | gamification_profiles + xp_event_ledger | 1 | Active |
| gamification_events | xp_event_ledger | 1 | Active |
| skill_graphs | skills | 1 | Active |
| learning_progress / user_learning_progress | skill_states / learning_progress | 1 | Active |
| learning_events | learning_attempts + learning_evidence | 1 | Active |
| coding_challenges | coding_submissions + execution_results | 1 | Active |
| submissions | coding_submissions (consolidated) | 1 | Active |
| aptitude_tests | assessment_attempts (aptitude) | 1 | Active |
| company_mock_tests | assessment_attempts (company mock) + oa_sessions | 1 | Active |
| oa_sessions | oa_sessions | 1 | Active |
| interviews | interview_sessions | 1 | Active |
| interview_bookings | interview_bookings | 2 | Active |
| interview_chat_sessions | interview_sessions (chat messages) | 2 | Active |
| career_profiles | career_profiles | 2 | Active |
| resumes | resumes | 2 | Active |
| payments | payments | 2 | Active |
| repair_missions | repair_missions | 2 | Active |
| srs_states / srs_cards | srs_cards | 2 | Active |
| applications | job_applications | 3 | Active |
| analytics_events | analytics_events | 3 | Active |
| analytics_rollups | analytics_rollups | 3 | Active |
| audit_logs | audit_logs | 3 | Active |
| coupons | coupons | 3 | Active |
| invoices | invoices | 3 | Declared |
| cover_letters | cover_letters | 4 | Declared |
| service_metrics | service_metrics | 4 | Active |
| revenue_events | revenue_events | 4 | Declared |
| billing_metrics | billing_metrics | 4 | Declared |

---

## Import Order (Dependency-Safe)

1. Users and identity mappings (no dependencies)
2. Gamification profiles (depends on users)
3. Skills and skill prerequisites (no dependencies)
4. Content and assessment metadata (no dependencies)
5. Gamification historical XP events (depends on users + gamification_profiles)
6. Learning skill states (depends on users + skills)
7. Learning attempts (depends on users + skills)
8. Learning evidence (depends on learning attempts)
9. Mastery snapshots (depends on learning evidence)
10. SRS cards (depends on users + skills)
11. Repair missions (depends on users + skills)
12. Assessment definitions and variants (no dependencies)
13. Assessment attempts and sections (depends on users + assessment definitions)
14. Responses (depends on assessment attempts)
15. Coding submissions (depends on users)
16. Execution results (depends on coding submissions)
17. OA sessions (depends on users)
18. Interviews (depends on users)
19. Company assessment metadata (no dependencies)
20. Career profiles (depends on users)
21. Resume and uploaded-file metadata (depends on users)
22. Analytics and audit records (depends on users)

**Never import child records before their required parent records.**
