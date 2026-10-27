# BountyCode Backend Services & Frontend API Modules — Structured Analysis

## 1. Frontend API Modules (`frontend/src/services/api/index.ts`)

| API Module Names | Feature Area | Likely Backend Route Prefix(es) |
|---|---|---|
| `authApi` | Authentication, registration, onboarding, profile | `/api/auth/*` |
| `interviewApi` | Mock interview sessions, answer submission, results | `/api/interview/*` |
| `bookingApi` | Interview scheduling / booking | `/api/interview/booking` or `/api/booking/*` |
| `resumeApi` | Resume upload, generation, optimization, export | `/api/resume/*` |
| `billingApi` | PayPal checkout, webhooks, plan status | `/api/billing/*` |
| `aptitudeApi` | Aptitude test flow (start, answer, complete, history) | `/api/aptitude/*` |
| `behavioralApi` | Behavioral interview practice | `/api/behavioral/*` |
| `hrApi` | HR-style interview questions | `/api/hr/*` |
| `codingApi` | Coding challenges, history, hints | `/api/coding/*` |
| `compilerApi` | Code execution, test cases, language list | `/api/compiler/*` |
| `questionsApi` | Question bank browse, solve, submit, stats | `/api/questions/*` |
| `toolsApi` | Utility tools (e.g., ATS, cover letter helpers) | `/api/tools/*` |
| `companyMocksApi` | Company-specific mock interviews and tips | `/api/company/*` |
| `companyPrepExamApi` | Company prep exam flow | `/api/company/*` |
| `gamificationApi` | Profile, leaderboard, badges, skills, tower | `/api/gamification/*` |
| `rolesApi` | Role-based progression or selection | `/api/roles/*` |
| `oaApi` | Mock online assessments (OAs) | `/api/oa/*` |
| `enhancedApi` | Enhanced/adaptive practice features | `/api/enhanced/*` |
| `freePracticeApi` | Free-tier quick interview / practice | `/api/free-practice/*` |
| `studentApi` | Student-specific dashboard and stats | `/api/student/*` |
| `placementApi` | Placement prep, drives, predictions | `/api/placement/*` |
| `indianPlacementApi` | Indian market placement prep (TCS/Infosys/etc.) | `/api/indian-placement/*` |
| `systemDesignApi` | System design interview practice | `/api/system_design/*` |
| `systemDesignTestsApi` | System design test cases / evaluation | `/api/system_design/*` |
| `dailyApi` | Daily challenges, missions | `/api/daily/*` |
| `learningApi` | Learning hub, paths, progress | `/api/learning/*` |
| `communityApi` | Community discussions, posts | `/api/community/*` |
| `learningEventsApi` | Learning lifecycle events | `/api/learning-events/*` |
| `adaptiveApi` | Adaptive learning path | `/api/adaptive/*` |
| `predictorApi` | Placement prediction engine | `/api/predictor/*` |
| `readinessApi` | Interview readiness scoring | `/api/readiness/*` |
| `personalDashboardApi` | Personal dashboard stats | `/api/personal-dashboard/*` |
| `dsaFingerprintApi` | DSA skill fingerprint / assessment | `/api/dsa-fingerprint/*` |
| `playlistsApi` | Learning playlists | `/api/playlists/*` |
| `submissionsApi` | Code / problem submission history | `/api/submissions/*` |
| `featuresApi` | Feature flags / enabled features list | `/api/features/*` |
| `visualizationsApi` | Algorithm visualizations | `/api/visualizations/*` |
| `distributionsApi` | Salary distribution comparisons | `/api/distributions/*` |
| `analyticsApi` | User analytics, insights, progression | `/api/analytics/*` |
| `aiDebuggerApi` | AI-powered debugging assistance | `/api/ai-debugger/*` |
| `conceptsApi` | Concept explanations | `/api/concepts/*` |
| `evidenceApi` | Evidence aggregation for mastery | `/api/evidence/*` |
| `progressApi` | Learning progress tracking | `/api/progress/*` |
| `learningModulesApi` | Duolingo-style learning modules | `/api/learning-modules/*` |
| `studyApi` | Study engine, sessions, timers | `/api/study/*` |
| `learningPathsApi` | Language learning paths | `/api/learning-paths/*` |
| `companyTracksApi` | Company-specific learning tracks | `/api/company-tracks/*` |
| `freeTrialApi` | Free trial activation / status | `/api/free-trial/*` |
| `onboardingApi` | Onboarding quest and status | `/api/onboarding/*` |
| `lessonApi` | Individual lesson viewer | `/api/lesson/*` |
| `journeyApi` | Learning journey / roadmap | `/api/journey/*` |
| `missionApi` | Missions and quests | `/api/missions/*` |
| `mapApi` | World / tower map state | `/api/map/*` |
| `adminContentApi` | Admin content management | `/api/admin-content/*` |
| `assignmentsApi` | Assignments / tasks | `/api/assignments/*` |
| `metricsApi` | System / service metrics | `/api/metrics/*` |
| `tracksApi` | Learning tracks | `/api/tracks/*` |
| `tcsNqtApi` | TCS NQT specific prep | `/api/tcs-nqt/*` |
| `companyLessonsApi` | Company-specific lessons | `/api/company-lessons/*` |
| `companyDirectoryApi` | Company directory / profiles | `/api/company-directory/*` |
| `flatApi` / `flatOverrides` | Legacy flat compatibility routes | `/api/flat/*` |
| `examMemoriesApi` | Exam memory submissions | `/api/exam-memories/*` |
| `blogsApi` | Blog / article content | `/api/blogs/*` |
| `csFundamentalsApi` | CS fundamentals questions | `/api/cs-fundamentals/*` |
| `animeCardsApi` | Anime-card gamification (legacy/stub) | `/api/anime-cards/*` |
| `atomsApi` | Atomic concept units | `/api/atoms/*` |
| `curriculumApi` | Curriculum maps and sequences | `/api/curriculum/*` |
| `tutorApi` | AI tutor interactions | `/api/tutor/*` |
| `learnerApi` | Learner state / graph | `/api/learner/*` |
| `opportunityApi` | Job opportunities | `/api/opportunity/*` |
| `deckApi` | Flashcard / deck system | `/api/deck/*` |
| `arenaApi` | Arena / contest battles | `/api/arena/*` |
| `teachwallApi` | Teach wall (content authoring) | `/api/teachwall/*` |
| `unifiedApi` | Unified catch-all API surface | `/api/unified/*` |

> **Note:** Route-prefix mapping is inferred from module naming conventions and the canonical route list in `AGENTS.md`. Exact prefixes may vary slightly (hyphen vs underscore), but the feature-to-domain mapping is stable.

---

## 2. Backend Service Groups

### 2.1 AI Services

| Service File | Responsibility |
|---|---|
| `ai.py` | Backward-compatible re-export hub for all domain-specific AI functions. Imports and republishes `chat_completion`, `parse_json`, interview/coding/aptitude/resume/behavioral/system_design/project/feedback/tutor AI functions so existing consumers remain unchanged. |
| `ai_core.py` | Core AI infrastructure: manages a singleton `httpx.AsyncClient` for OpenRouter, implements `chat_completion()` with circuit-breaker gating, retry logic (3 retries with exponential backoff), 6 fallback models, SHA-256 caching (1-hour TTL), and request-metrics recording. Also provides `parse_json()` with aggressive fallback strategies (code fences, substring extraction, single-quote repair) and company-tag utilities. |
| `ai_interview.py` | Interview-domain AI: maintains `COMPANY_PROFILES` for Google/Amazon/Meta/Microsoft/TCS/Infosys/Wipro/Uber with style descriptions, rubrics, and leadership principles. Generates next interview questions (curated-bank first 3, then LLM) with difficulty adaptation and student-context personalization from skill graph / OA history / repair missions / past interviews. Evaluates answers using difficulty-aware, rubric-weighted scoring blended with heuristic communication-style analysis. |
| `ai_resume.py` | Resume-domain AI: `analyze_resume()` scores content/formatting/keywords/impact; `optimize_ats()` rewrites resumes against a JD with missing/present keyword lists and change logs; `generate_resume_content()` produces structured resume sections from user details. All functions use strict JSON parsing with safe defaults. |
| `ai_behavioral.py` | Behavioral interview AI: generates STAR-method behavioral questions by category (leadership, teamwork, conflict, etc.), produces company-specific interview tips (do's/don'ts/common questions), and creates daily-challenge mentor messages in two modes — motivational strings or structured topic explanations. |
| `ai_coding.py` | Coding challenge generation: produces original problems with description, examples, constraints, visible/hidden test cases, progressive hints, and follow-up variants. Time limits scale by difficulty (easy/medium/hard). Assigns company tags via weighted random selection. |
| `ai_system_design.py` | System design AI: generates difficulty-appropriate design questions (URL shortener → YouTube-at-scale) with expected components and hints. Evaluates answers across 10 criteria (requirements, scalability, trade-offs, DB design, etc.) returning strengths, improvements, and missing concepts. |
| `ai_aptitude.py` | Aptitude test AI: contains `APTITUDE_SUB_CATEGORY_GUIDELINES` for 16 sub-categories (quant-shortcuts, syllogisms, blood-relations, direction-sense, coding-decoding, series-completion, analogies, puzzles, reading-comprehension, para-jumbles, sentence-correction, vocabulary, fill-in-blanks, critical-reasoning, data-interpretation, time-work). Generates MCQs with 4 options, correct answer, explanation, and 2–5 company tags; evaluates selected answers. |
| `ai_cover_letter.py` | LinkedIn About generation: produces a first-person LinkedIn About section from resume text and target role, optimized for recruiter search keywords and under 2600 characters. |
| `ai_project.py` | Project generator AI: `generate_project()` creates complete runnable project files, dependencies, and setup instructions; `review_project()` scores code quality/security/performance and returns actionable issues; `improve_code()` suggests refactors for a specific aspect; `generate_setup_instructions()` produces run/test commands. |
| `ai_feedback.py` | Sentence-level answer feedback: splits answers into sentences, scores each 1–10 with specific rewrite suggestions, and returns top strengths/improvements. Falls back to generic per-sentence suggestions if AI parsing fails. |
| `ai_tutor.py` | Pedagogical AI tutor inside the learning loop. Six modes: TEACH (concept + example), GUIDE (hint only), DIAGNOSE (misconception + repair), DEBUG (bug-localization questions), REFACTOR (cleaner approach), REFLECT (summary + next action). Returns `mode`, `target`, `prompt`, `evidence_tag`, and `follow_up`. Falls back to deterministic strings on AI failure. |

---

### 2.2 Gamification Services

| Service File | Responsibility |
|---|---|
| `gamification.py` | Canonical gamification orchestrator and the **only** writer of XP/coins/stars/streak/combo/badges/weekly-league-XP (per Gamification Law). `record_practice()` normalizes 0–100 scores to 0–10, computes streak/mastery/combo/performance multipliers, awards Diamonds/coins/proof/bounty, updates tower fields, checks badges/achievements/streak-milestones/mastery-milestones/boss-eligibility, and appends an immutable `gamification_events` ledger row. Also provides `award_bonus_xp()`, `spend_xp()`, `use_power_up()`, `buy_power_up()`, streak freeze/repair, daily goals, weekly/monthly challenges, leaderboard, and league status. |
| `gamification_core.py` | Pure data + pure math leaf module imported by `gamification.py`. Defines level titles (generic + company-aware bands for TCS/Infosys/Wipro/Cognizant/Accenture/Google/Amazon/Meta/Microsoft/Apple), boss battles, forest journey zones, seasonal storms, power-ups, streak multipliers, weekly/monthly challenge templates, 40+ badge definitions, declarative `BADGE_CONDITIONS`, Proof/Bounty economy tables, Voyage ranks, level color tiers, and helper functions (`_calculate_level`, `_calculate_xp`, `get_title_for_level`, `voyage_rank_for_level`, `compute_forest_state`, `calculate_stars`, etc.). |
| `spaced_repetition.py` | SM-2 spaced repetition engine for DSA concept mastery. Manages per-concept `SRSState` (interval, repetitions, ease factor, learning steps). Provides `review()` with grade-aware interval calculation (AGAIN/HARD/GOOD/EASY), `get_due_cards()` sorted by overdue-ness, `get_stats()` (retention rate, new/learning/review counts), and `simulate_forecast()`. Includes a static DSA concept taxonomy (arrays, linked-lists, trees, graphs, DP, heaps, tries, backtracking, bit-manipulation, math-geometry) for initialization. |

---

### 2.3 Code Execution Services

| Service File | Responsibility |
|---|---|
| `code_executor.py` | Production `CodeExecutionEngine` wrapping the Piston API. Executes single code runs and batch test-case grading with concurrency limits. Supports 12 languages with boilerplate templates (general, class, linked_list, binary_tree, graph, dp). Includes a local-Python oracle path (`_grade_python_batched`) that runs ALL test cases in ONE subprocess for zero API cost. Falls back through: own GCP compiler service → remote fallbacks (Judge0/Wandbox/Glot.io) → local sandbox. Also generates AI or AST-based execution traces for algorithm visualizations. |
| `local_sandbox.py` | UX-level safety-net sandbox for Python and JavaScript. Runs restricted subprocesses with stripped builtins (`open`, `exec`, dangerous `__import__`), whitelisted safe modules, POSIX `resource` limits (30s CPU, 256MB AS), and hard `kill` timeouts. Provides `execute_local()` for single runs and `execute_local_python_batch()` for batched oracle grading (auto-detects single top-level function, canonical JSON serialization). Also exposes a synchronous `execute_local_sync()` wrapper for non-async callers. |
| `docker_sandbox.py` | Secure Docker-based sandbox (`DockerSandbox`) pulling per-language images (python:3.11-slim, node:20-slim, openjdk:17-slim, gcc:13, etc.). Compiles when needed, runs with strict resource limits (`cpu_quota`, `mem_limit`, `pids_limit`, `network_disabled`, `read_only` rootfs, `no-new-privileges`, `cap_drop ALL`, non-root user). Writes code to temp files, bind-mounts into containers, captures stdout/stderr/exit_code, and returns `SandboxResult` dataclasses. |
| `code_execution_worker.py` | Background `CodeExecutionWorker` consuming jobs from `JobQueue`. Handles three job types: `CODE_EXECUTION` (routes to Docker first, then Piston), `TEST_CASES` (oracle batch path for Python when Docker is off, else per-case execution), and `EXECUTION_TRACE` (AST or AI trace). Sends WebSocket progress events (`job_started`, `job_progress`, `job_completed`, `job_failed`) to the user. |

---

### 2.4 Payments / Billing Services

| Service File | Responsibility |
|---|---|
| `invoice.py` | `InvoiceService` generates legally compliant invoices stored in MongoDB (`invoices_collection`). Creates invoice IDs, customer/company details, line items, tax/total, and period end dates. Also renders HTML invoices. Legacy JSON-file seed directory exists but request-time writes go to Mongo. |
| `coupon.py` | Coupon lifecycle: `create_coupon()`, `validate_coupon()` (active, expiry, usage limit, plan applicability), `apply_coupon()` (percent/fixed discount, increments `used_count`, records on user doc), and `get_coupon_stats()`. |
| `monetization.py` | Tier definitions and feature-access enforcement. Defines `FREE_TIER`, `PRO_TIER`, `LIFETIME_TIER`, `TEAM_TIER`, `ENTERPRISE_TIER` with daily/monthly limits per feature. `check_feature_access()` reads from `usage_collection`, resets daily/monthly counters, and returns remaining quota. `record_feature_usage()` increments counters and triggers limit-reached upsell emails (2-day cooldown). |
| `usage.py` | Free-tier usage tracking and monthly reset. `check_and_reset_monthly_usage()` zeros `interviews_used`, `resumes_used`, `aptitude_used`, etc. on month change for non-Pro users. `can_use_feature()` checks per-feature limits against configurable `FREE_TIER_*` settings. `mark_feature_used()` increments counters and fires limit-reached emails. `get_usage_stats()` returns plan-aware usage dashboards. |

---

### 2.5 Content / Question Bank Services

| Service File | Responsibility |
|---|---|
| `question_store.py` | Canonical in-memory question bank loader and query engine. Loads from a consolidated `questions_bank.json`, 20+ verified extra banks, auto-checked banks, and unverified banks. Normalizes schemas, dedupes on normalized title (keeping highest-trust variant), enforces Striver A2Z pattern tagging, applies LeetCode metadata overlays, and maintains quarantine state via `served_quarantine.json` + Mongo overrides. `_is_servable()` gates on `trust_status in ("verified", "reviewed")` plus executability. Exposes `QuestionCursor` with `prefer_verified()`, `only_verified()`, skip/limit/sort, and async iteration. |
| `content_corpus.py` | Read-only knowledge corpus loader from `backend/app/data/knowledge/corpus.json`. Provides concept registry, prerequisite graph (with transitive closure), curriculum map, cross-language mappings, and source registry. Offers keyword search, domain/language/category filters, curriculum sequence retrieval, and corpus validation (orphaned prerequisites, circular dependencies, unmapped concepts). |
| `auto_verify.py` | Deterministic, no-LLM automated verification pipeline. `verify_question()` runs structural checks (missing solution, missing test cases, MCQ option validation), normalizes test cases from examples/MCQs, executes Python solutions against test cases, and updates in-memory `trust_status` to `automated_checked` or `quarantined`. `verify_all_questions()` processes the entire canonical store. Also verifies lesson content structure and runtime (starter/placeholder/broken-code/debug-fix execution). |

---

### 2.6 Analytics Services

| Service File | Responsibility |
|---|---|
| `analytics.py` | User-facing analytics aggregation: `get_overview()` (apps, gamification stats, skill graph, 30-day activity counts), `get_funnel()` (application stage funnel with percentages), `get_skill_progression()` (30-day category score history), `get_company_stats()` (per-company application rates, interview rates, offer rates, prediction history), and `get_insights()` (avg prediction probability, best company, weak areas). |
| `analytics_service.py` | Event tracking and rollup analytics: `track_event()` writes to `analytics_events_collection` with HMAC-SHA256 IP hashing. Maintains `analytics_rollups_collection` for fast dashboard queries. Provides `get_geo_breakdown()`, `get_retention_stats()` (new vs returning), `get_visitor_stats()`, `get_page_stats()`, `get_feature_usage()`, `get_realtime_stats()`, `get_user_list()`, and `get_user_stats_summary()`. |
| `request_metrics.py` | Lightweight in-memory `RequestMetrics` singleton recording service-level success/failure counts, latency totals, last-error strings, and last-seen timestamps. Periodically flushes snapshots to `service_metrics` Mongo collection (default 5-minute interval). Used by AI, compiler, and other critical paths for observability. |

---

### 2.7 Auth / Session / Infrastructure Services

| Service File | Responsibility |
|---|---|
| `middleware/auth.py` | Authentication middleware: JWT creation/decoding (access + refresh tokens with `jti`), bcrypt password hashing/verification, httpOnly cookie management (`pp_token`), WebSocket auth, user caching (5-min TTL, raw doc only), `require_plan()` dependency, and `require_admin()` dependency. `is_admin`/`role` are recomputed on every request from `ADMIN_EMAILS` config — never cached. |
| `usage.py` | Monthly usage reset and free-tier enforcement. `check_and_reset_monthly_usage()` resets per-feature counters when the month rolls over. `can_use_feature()` checks configurable limits (interviews, resumes, aptitude, company mocks, predictor, question bank, streak repair). `mark_feature_used()` increments counters and sends limit-reached upsell emails with a 2-day cooldown. |
| `feature_flags.py` | Feature flag registry for 50+ features with status (`disabled`/`internal`/`beta`/`gradual`/`enabled`) and optional `allowed_plans` restrictions. `is_feature_enabled()` evaluates flags against a plan tier. `FeatureManager` supports runtime updates for gradual rollouts. |
| `cache.py` | Unified caching layer: `InMemoryCache` (OrderedDict LRU with TTL), `RedisCache` (async Redis with `json` serialization), and `UnifiedCache` (Redis-first with in-memory fallback). Global `cache` singleton used by auth, AI, and other services. |
| `circuit_breaker.py` | Async-safe `CircuitBreaker` class used by AI (`ai_breaker`) and compiler (`compiler_breaker`) services. Tracks failure count, opens after threshold, half-opens after recovery timeout, and exposes `allow_request()`, `record_failure()`, `record_success()`. |
| `resilience.py` | `call_with_resilience()` wrapper combining retry (configurable attempts + delay) with circuit-breaker state checks for external API calls. Used by `ai_core.py` and other resilience-needing services. |

---

### 2.8 Other Notable Services

| Service File | Responsibility |
|---|---|
| `curriculum.py` / `curriculum_engine.py` / `curriculum_connector.py` | Curriculum map loading, sequencing, and cross-referencing with the content corpus and learning paths. |
| `concept_engine.py` / `concepts.py` / `concept_mastery.py` | Concept-level mastery tracking, mastery state transitions, and concept graph navigation. |
| `atom_engine.py` / `atoms.py` | Atomic learning unit (atom) generation, sequencing, and state management for the learning loop. |
| `behavioral_engine.py` / `behavioral_enhanced.py` / `behavioral_judge.py` | Behavioral interview evaluation engine with STAR-method parsing, enhanced heuristic analysis, and LLM-judge blending. |
| `study_engine.py` / `study_timer.py` | Study session management, focus-timer logic, and session-state persistence. |
| `journey_engine.py` | Learning journey orchestration, stage progression, and branching based on student performance. |
| `placement_engine.py` | Placement prediction and readiness scoring using skill graph, OA outcomes, and interview history. |
| `adaptive_learning.py` / `adaptive_lesson_planner.py` | AI-driven adaptive path adjustment and lesson planning based on student evidence. |
| `code_tracer.py` | Python AST-based execution tracer for algorithm visualizations (variable state, line-by-line steps, data-structure snapshots). |
| `email.py` | Email service wrapper (SMTP) for transactional emails: password reset, limit-reached upsells, notifications. |
| `websocket_manager.py` | WebSocket connection manager with personal message routing, used by code execution worker and real-time features. |
| `audit_log.py` | Audit logging for admin actions and sensitive operations. |
| `migrations.py` | Decorator-based schema migration tracking for database collection evolution. |

---

## 3. Cross-Cutting Observations

1. **Single Source of Truth Enforcement**
   - `record_practice()` in `gamification.py` is the only sanctioned writer of Diamonds/coins/stars/streak/combo/badges/weekly-league-XP. All other modules read, never write these fields.
   - `question_store.py` is the only question-content reader. No route or service may read question statements/answers/test cases from MongoDB.

2. **Trust Pipeline**
   - Question content follows `UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED`. `auto_verify.py` handles the deterministic first hop (no LLM). Student-facing serving returns only `verified`/`reviewed` items.

3. **AI Reliability Stack**
   - All AI calls flow through `ai_core.chat_completion()` with circuit-breaker gating, 3 retries, 6 fallback models, 1-hour caching, and request-metrics recording. Domain modules (`ai_interview`, `ai_resume`, etc.) never call OpenRouter directly.

4. **Code Execution Fallback Chain**
   - `CodeExecutionEngine.execute_code()` tries: local Python oracle batch → GCP compiler service → remote fallbacks (Judge0/Wandbox/Glot.io) → local subprocess sandbox → Piston API. Each hop records metrics and respects circuit-breaker state.

5. **Frontend Rendering Rule**
   - The UI never computes reward math. Every XP/level/streak display renders exactly what `record_practice()` returns. The frontend derives no independent curves or multipliers.

---

*Generated by read-only inspection of `frontend/src/services/api/index.ts` and `backend/app/services/*.py`.*
