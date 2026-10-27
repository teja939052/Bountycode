# BountyCode — A-to-Z Route & Feature Inventory

> **Scope:** Complete backend routes, frontend pages, feature areas, API module mappings, cross-cutting systems, database collections, and codebase architecture.
> **Date:** 2026-09-28
> **Status:** Verified from source inspection

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Backend Routes A-Z](#2-backend-routes-a-z)
3. [Frontend Pages A-Z](#3-frontend-pages-a-z)
4. [Feature Area Mapping](#4-feature-area-mapping)
5. [API Module Mapping](#5-api-module-mapping)
6. [Cross-Cutting Systems](#6-cross-cutting-systems)
7. [Database Collections](#7-database-collections)
8. [Architecture Patterns](#8-architecture-patterns)

---

## 1. Executive Summary

**BountyCode** is an AI-powered placement preparation platform built as a full-stack web application:

- **Backend:** FastAPI + MongoDB (Motor) + Redis + 99 route files + 90+ service files
- **Frontend:** React 18 + Vite 5 + TypeScript + 120+ pages + 39 API modules
- **AI:** OpenRouter (Gemini primary, 6 fallbacks) with circuit breaker + cache + retry
- **Code Execution:** Piston → GCP compiler service → Judge0/Wandbox/Glot → Local sandbox
- **Payments:** PayPal + Stripe + Razorpay with webhook idempotency
- **Real-time:** WebSocket manager for live updates
- **Gamification:** Diamonds/levels/streaks/badges/boss battles/power-ups with immutable ledger

### Key Numbers
- **99 backend route files** (auto-discovered by `main.py`)
- **~120 frontend pages** (lazy-loaded via `pages/lazy.ts`)
- **39 API modules** aggregated in `services/api/index.ts`
- **87 MongoDB collections** (student state only)
- **50+ feature flags**
- **6 AI fallback models**
- **12 supported code execution languages**

---

## 2. Backend Routes A-Z

### 2.1 Authentication & Onboarding

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `auth.py` | `/api/v1/auth` | `POST /register`, `POST /login`, `POST /refresh`, `POST /logout`, `GET /me`, `POST /update-profile`, `POST /change-password`, `POST /forgot-password`, `POST /reset-password`, `GET /verify-email`, `GET /onboarding-status`, `POST /onboarding-complete`, `GET /google`, `GET /google/callback` | Auth lifecycle, JWT + httpOnly cookies, refresh rotation, rate limiting, Google OAuth |
| `onboarding.py` | `/api/v1/onboarding` | `GET /doors`, `POST /doors/complete`, `GET/POST /launch` | Guided onboarding with door-based entry (job/dev/beginner) |
| `trial.py` | `/api/v1/trial` | `POST /start`, `GET /status`, `POST /cancel` | Trial lifecycle management |
| `free_trial.py` | `/api/v1/free-trial` | `GET /lessons`, `POST /complete`, `GET /conversion-prompt`, `POST /track-trial` | Free trial lessons with conversion funnel tracking |

### 2.2 Interview & Assessment

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `interview.py` | `/api/v1/interview` | `POST /start`, `POST /answer`, `GET /result`, `GET /history` | AI mock interviews with follow-ups, OA-aware adaptive questioning |
| `interview_chat.py` | `/api/v1/interview-chat` | `POST /start`, `GET /session`, `POST /turn` | Conversational interview with Captain Byte persona |
| `interview_booking.py` | `/api/v1/interview-booking` | `POST /book`, `GET /upcoming`, `GET /history`, `POST /cancel`, `POST /submit-answers` | Mock interview scheduling with slot overlap checks |
| `assessments.py` | `/api/v1/assessments` | `POST /start/{id}`, `POST /submit/{stage}`, `GET /report`, `GET /definitions` | Assessment engine with staged submissions |
| `oa.py` | `/api/v1/oa` | `POST /start`, `POST /submit-answer`, `GET /result`, `GET /history`, `GET /leaderboard`, `POST /integrity-event` | Mock OA simulator with blueprint-driven company distributions |
| `sde_diagnostic.py` | `/api/v1/sde` | `POST /diagnostic/start`, `GET /diagnostic/status`, `GET /roadmap`, `GET /skills`, `POST /skill/update`, `GET /mastery` | SDE baseline diagnostic with role-specific skill graph |
| `behavioral.py` | `/api/v1/behavioral` | `GET /question`, `GET /categories`, `POST /questions`, `POST /feedback` | STAR framework behavioral questions |
| `hr.py` | `/api/v1/hr` | `GET /question`, `POST /questions`, `GET /categories`, `POST /feedback` | HR-style people-management scenarios |
| `quiz.py` | `/api/v1/quiz` | `POST /build`, `POST /answer`, `POST /hint`, `POST /results`, `POST /learning-path`, `POST /boss-battle`, `GET /stats`, `GET /weak-topics`, `GET /questions` | Quiz builder with modes: practice/quiz/mock_interview/speed_run/boss_battle |

### 2.3 Resume & Career

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `resume.py` | `/api/v1/resume` | `POST /upload`, `POST /generate`, `POST /optimize`, `POST /semantic-score`, `POST /analyze-rulebased`, `POST /improve-bullet(s)`, `POST /tailor`, `POST /missing-bullet`, `GET /export/docx|pdf`, `GET /history` | Resume lifecycle: upload, generate, optimize, ATS scoring, export |
| `cover_letter.py` | `/api/v1/tools` | `POST /linkedin-about` | LinkedIn About generation from resume text |
| `student_features.py` | `/api/v1/student` | `POST /cheatsheet`, `GET /cheatsheet/templates`, `POST /humanize/bullet|resume`, `POST /applications/pipeline|stage|stats|delete`, `GET /applications/stages`, `POST /drill/daily|submit`, `POST /sync/github|generate-bullets`, `GET /sync/linkedin` | Student utility suite: cheatsheet, anti-plagiarism, application tracker, daily drill |
| `student_discount.py` | `/api/v1/discount` | `POST /student/verify`, `GET /student/status` | Student discount email verification |
| `opportunity.py` | `/api/v1/opportunity` | `GET /companies`, `GET /company/{company}`, `GET /company/{company}/capabilities|fit|gaps`, `GET /adaptive-plan` | Opportunity graph with capability gap analysis |
| `companies.py` | `/api/v1/companies` | `GET /`, `GET /{role_id}`, `GET /{role_id}/{company_id}`, `POST /{role_id}/{company_id}/stage/{stage_order}/evaluate`, `GET /roadmap` | Company journeys with stage evaluation + repair missions |
| `company_prep.py` | `/api/v1/company-prep` | `GET /blueprints`, `GET /blueprints/{company}`, `GET /{company}/questions`, `GET /{company}/readiness`, `POST /{company}/start-assessment`, `GET /companies` | Company blueprints with verified-only questions |
| `company_mocks.py` | `/api/v1/company-mocks` | `POST /start`, `POST /answer`, `GET /result`, `GET /history` | Company-specific mock portals with round configs |
| `company_tracks.py` | `/api/v1/company-tracks` | `GET /companies`, `GET /companies/{track_id}`, `POST /companies/enroll`, `POST /companies/{track_id}/modules/{module_id}/complete`, `GET /my-tracks` | Company learning tracks with module progress |
| `company_lessons.py` | `/api/v1/company-lessons` | `GET /list`, `GET /{slug}`, `POST /{slug}/complete` | Company-specific lesson content |
| `placement.py` | `/api/v1/placement` | `GET /alumni` | Alumni experiences read-only |
| `placement_calendar.py` | `/api/v1/placement-calendar` | `GET /companies`, `GET /calendar`, `GET /countdown`, `GET /company/{slug}`, `GET /boss-battles`, `GET /timeline/{slug}` | Placement season calendar with predicted drive dates |
| `placement_packs.py` | `/api/v1/placement-packs` | `GET /sde`, `GET /companies`, `GET /companies/{id}`, `GET /learning-objects`, `GET /learning-objects/{id}`, `GET /curation-health`, `GET /learning-paths`, `GET /learning-paths/{id}`, `POST /learning-paths/{id}/enroll`, `POST /learning-paths/{id}/modules/{mid}/complete`, `GET /my-paths` | Placement curriculum packs with pro gating |
| `placement_questions.py` | `/api/v1/placement-questions` | `GET /random`, `GET /by-company/{company}`, `GET /stats` | Placement aptitude questions with pattern-relevant company alignment |
| `indian_placement.py` | `/api/v1/indian-placement` | `GET /companies`, `GET /{id}`, `GET /{id}/mock-config`, `GET /{id}/hr-questions`, `GET /{id}/coding-patterns`, `POST /start-mock` | Indian company mocks (TCS/Infosys/Wipro/etc.) with verified-only bank |
| `blogs.py` | `/api/v1/blogs` | `GET /list`, `GET /company/{company}`, `GET /{slug}` | Company prep guides from file-backed blogs.json |

### 2.4 Coding, Compiler & System Design

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `coding.py` | `/api/v1/coding` | `GET /topics`, `POST /start`, `POST /submit`, `POST /hint`, `POST /interviewer-feedback` | Coding challenges with company-specific generation |
| `compiler.py` | `/api/v1/compiler` | `POST /execute`, `POST /execute-test-cases`, `GET /job/{id}`, `GET /languages`, `POST /starter-code`, `POST /boilerplate`, `POST /trace` | Code execution with sync/async modes, WebSocket updates |
| `system_design.py` | `/api/v1/system-design` | `POST /start`, `POST /answer`, `GET /{session_id}/result` | System design practice with bank-first question selection |
| `system_design_tests.py` | `/api/v1/system-design-tests` | `GET /categories`, `GET /problems`, `GET /problem/{id}`, `POST /evaluate/{id}` | System design test bank with AI rubric evaluation |
| `visualizations.py` | `/api/v1/visualizations` | `POST /trace` | Algorithm visualization with 50+ pre-built templates |
| `trace.py` | `/api/v1/trace` | `POST /generate` | Algorithm trace generation (step-by-step) |
| `ai_debugger.py` | `/api/v1/ai-debugger` | `POST /analyze`, `POST /hint`, `POST /explain-error` | AI debugging assistant with step-by-step trace |

### 2.5 Question Bank & Practice

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `questions.py` | `/api/v1/questions` | `GET /browse`, `GET /random`, `GET /{id}`, `GET /{id}/solution`, `GET /{id}/solved`, `POST /{id}/submit`, `POST /{id}/answer`, `GET /stats`, `GET /recent`, `GET /filters`, `POST /submit`, `POST /upvote` | Question bank browsing + curation with verified-only serving |
| `questions_solve.py` | `/api/v1/questions` | `POST /{id}/submit`, `POST /{id}/answer`, `GET /{id}/hints`, `GET /{id}/solution` | Question solving flow with code execution + AI feedback |
| `submissions.py` | `/api/v1/submissions` | `POST /{id}/submit`, `GET /history` | Submission history + solved tracking with failure class enum |
| `problems.py` | `/api/v1/problems` | `POST`, `GET`, `GET /{id}`, `GET /{id}/visible`, `GET /{id}/lock-state`, `POST /{id}/reset-locks`, `POST /{id}/check-lock`, `POST /{id}/run` | Lock-engine problem CRUD with in-memory PROBLEMS_DB |
| `practice.py` | `/api/v1/practice` | `POST /session`, `POST /session/{id}/complete`, `GET /sessions` | Role-based practice sessions with weak/strong area detection |
| `arena.py` | `/api/v1/arena` | `GET /quiz`, `POST /submit` | MCQ practice arena with answers stripped client-side |
| `daily_problem.py` | `/api/v1/daily-problem` | `GET /today`, `POST /submit` | Problem of the Day with deterministic UTC-date selection |
| `daily_challenge.py` | `/api/v1/daily` | `GET /challenge`, `POST /submit`, `GET /leaderboard`, `POST /join` | Daily challenge + Diamond leagues with weakness-based mission builder |
| `playlists.py` | `/api/v1/playlists` | `GET /list`, `GET /{id}` | Curated playlists from in-memory verified pool |
| `features.py` | `/api/v1/features` | `GET /random`, `POST /bookmarks/{id}`, `GET /bookmarks`, `POST /notes/{id}`, `GET /notes/{id}`, `GET /companies`, `POST /companies/follow|unfollow`, `GET /companies/following`, `GET /companies/recommended`, `GET /notes`, `GET /recent|bookmarked`, `GET /search`, `GET /tags` | Random problem + bookmarks/notes + company follow |
| `aptitude.py` | `/api/v1/aptitude` | `GET /categories`, `GET /theory`, `GET /theory/{id}`, `GET /theory-for/{category}`, `POST /start`, `POST /{id}/answer`, `POST /{id}/complete` | Aptitude drills + theory with in-memory sessions |
| `aptitude_tests.py` | `/api/v1/aptitude-tests` | `GET /categories`, `GET /configurations`, `POST /start`, `POST /{id}/answer`, `POST /{id}/complete`, `GET /leaderboard`, `GET /history` | Timed aptitude tests with configs: quick/standard/advanced/mock |
| `cs_fundamentals.py` | `/api/v1/cs-fundamentals` | `GET /theory`, `GET /theory/{id}`, `GET /domain/{domain}` | CS theory cards from file-backed data |
| `tcs_nqt.py` | `/api/v1/tcs-nqt` | `GET /patterns`, `GET /patterns/{p}/questions`, `POST /patterns/{p}/assess`, `GET /progress`, `POST /questions/{id}/verify` | TCS NQT prep with domain filtering |
| `tracks.py` | `/api/v1/tracks` | `GET /{company}/overview` | Company track overview from verified bank + student status |

### 2.6 Learning & Curriculum

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `lesson.py` | `/api/v1/lesson` | `GET /{slug}`, `GET /{slug}/step/{key}`, `POST /{slug}/run|build|transfer|predict|explain|break|assess|complete`, `GET /plan/{id}`, `GET /next-action` | Vertical-slice lesson engine with 9-step teaching loop |
| `learning.py` | `/api/v1/learning` | `POST /interaction-action`, `POST /diagnose` | Learning interaction logging with misconception detection |
| `learning_paths.py` | `/api/v1/learning-paths` | `GET /roles`, `GET /roles/{id}`, `POST /roles/enroll`, `POST /roles/{id}/modules/{id}/complete`, `GET /my-paths`, `GET /recommendations` | Role-based learning paths (SDE/Data Analyst/QA/DevOps) |
| `learning_modules.py` | `/api/v1/learning-modules` | `GET /list`, `GET /{id}`, `POST /{id}/start`, `POST /{id}/steps/{n}/complete` | Duolingo-style modules with step-based progression |
| `language_paths.py` | `/api/v1/languages` | `GET /`, `GET /{id}`, `GET /{id}/levels`, `GET /{id}/modules/{idx}`, `GET /{id}/progress`, `POST /{id}/modules/{idx}/complete` | 7-language paths (100 levels × 80 modules per language) |
| `atoms.py` | `/api/v1/atoms` | `GET /worlds`, `GET /world/{id}`, `GET /{id}`, `GET /{id}/animation\|zero-code\|analogies\|mastery`, `GET /path/{company}`, `GET /company/{id}`, `GET /languages`, `GET /language/{id}/concept/{id}`, `POST /attempt`, `POST /check-misconception`, `GET /progress/world/{id}\|atom/{id}`, `GET /{id}/intuition` | 50-atom Concept Clarity Curriculum |
| `concepts.py` | `/api/v1/concepts` | `GET /graph`, `GET /progress`, `GET /sessions/{id}`, `GET /concept/{id}/frame`, `POST /concept/{id}/frame/result` | CFIC concept graph with additive collections |
| `unified_learning.py` | `/api/v1/unified` | `GET /lessons`, `GET /lessons/{id}`, `POST /activity`, `GET /progress`, `GET /catalog/stats`, `GET /lessons/{id}/metaphor`, `GET /lessons/{id}/intuition` | Unified learning catalog aggregating all content sources |
| `curriculum.py` | `/api/v1/curriculum` | `GET /missions`, `GET /missions/{id}` | Flagship curriculum missions |
| `scrimba.py` | `/api/v1/scrimba` | `GET /lessons`, `GET /lessons/{id}`, `POST /complete` | Scrimba-style lessons with SRS + repair trigger |
| `roles.py` | `/api/v1/roles` | `GET /`, `GET /{id}`, `GET /{id}/content\|exercises\|quizzes\|challenges\|practice-sets`, `POST /{id}/activity`, `GET /{id}/next\|dashboard`, `GET /exercise/{id}\|challenge/{id}\|quiz/{id}` | Role content packages |
| `map.py` | `/api/v1/map` | `GET /map` | Adventure map with serpentine positions, fog-of-war, repair nodes |
| `worlds.py` | `/api/v1/worlds` | `GET /{id}`, `GET /{id}/progress`, `POST /{id}/levels/{id}/attempt\|complete\|hint` | World/town/level progression with deterministic judge + SRS |
| `teachwall.py` | `/api/v1/teachwall` | `GET /challenge`, `POST /answer` | Teach-the-wall tutor play with deterministic shuffle |
| `tutor.py` | `/api/v1/tutor` | `POST /act` | AI tutor action with 6 modes: TEACH/GUIDE/DIAGNOSE/DEBUG/REFACTOR/REFLECT |
| `deck.py` | `/api/v1/deck` | `GET /today`, `POST /review` | Daily flashcard deck with SRS namespaced as `deck:{atom_id}` |
| `srs.py` | `/api/v1/srs` | `GET /due`, `GET /stats`, `POST /record`, `GET /problem/{id}`, `DELETE /problem/{id}` | Spaced repetition for problems with SM-2 scheduling |
| `study.py` | `/api/v1/study` | `GET /today`, `POST /activity` | Canonical daily study plan (legacy alias `/adaptive/daily-plan`) |
| `adaptive_learning.py` | `/api/v1/adaptive` | `GET /skills`, `GET /weak-areas`, `GET /daily-plan`, `GET /recommendations`, `GET /learning-path`, `GET /readiness`, `POST /activity`, `GET /domains` | Adaptive learning paths based on student evidence |
| `learner.py` | `/api/v1/learner` | `GET /state` | Canonical learner state for 5-environment frontend |
| `journey.py` | `/api/v1/journey` | `GET /state`, `GET /outcomes` | Journey state + longitudinal outcomes composing Study/Gamification/Mastery/Readiness/Worlds |

### 2.7 Gamification & Progress

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `gamification.py` | `/api/v1/gamification` | `GET /profile`, `POST /profile/target-company`, `GET /profile/title-progression`, `GET /readiness`, `GET /readiness/simulate`, `POST /record`, `GET /leaderboard`, `GET /badges`, `GET /skills`, `GET /skills/weak`, `GET /skills/readiness`, `GET /tower`, `GET /tower/boss/{level}`, `POST /power-ups/{id}/use\|buy`, `POST /streak-freeze\|repair`, `GET /streak-status\|forest-state\|daily-goal\|daily-login`, `POST /daily-bonus\|daily-login/claim`, `GET /achievement-chains` | Gamification profile + rewards — **only `record_practice` writes XP/coins/stars/streak/badges** |
| `progress.py` | `/api/v1/progress` | `GET /heatmap`, `GET /streak`, `GET /topic-progress`, `GET /weekly-goal` | Progress tracking + heatmap from solved problems + submissions |
| `metrics.py` | `/api/v1/metrics` | `POST /event`, `GET /features`, `GET /retention` | Legacy feature metrics (includes removed RPG feature names) |
| `personal_dashboard.py` | `/api/v1/dashboard` | `GET /personal`, `GET /weak-areas` | Personal dashboard with weak area analysis + recommendations |

### 2.8 Analytics & Admin

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `analytics.py` | `/api/v1/analytics` | `GET /overview`, `GET /funnel`, `GET /skills`, `GET /companies`, `GET /insights` | User analytics: apps, gamification stats, skill graph, company stats |
| `analytics_admin.py` | `/api/v1/analytics` | `POST /track`, `GET /admin/realtime\|visitors\|pages\|features\|hourly\|geo\|retention\|users\|summary` | Admin analytics: geo breakdown, retention stats, visitor trends |
| `admin_monitoring.py` | `/api/v1/admin` | `GET /dashboard/overview`, `GET /system/health`, `GET /feature-flags`, `POST /feature-flags/{n}/update-status\|set-rollout`, `GET /users/search\|export\|update\|impersonate`, `GET /content/queue`, `GET /billing/overview`, `GET /logs`, `POST /cache/clear`, `POST /system/maintenance`, `GET /system/config`, `GET /system/errors`, `POST /system/restart-service` | Admin operations: feature flags, user management, system health |
| `admin_content.py` | `/api/v1/admin/content` | CRUD content, tranche workflow, assignment CRUD + submissions + grading | Admin content + tranche curation with independent oracle verification |
| `health.py` | `/api/v1/health` | `GET /ping`, `GET /status`, `GET /ready`, `GET /live`, `GET /metrics`, `GET /dependencies` | Kubernetes-style health probes |
| `revenue.py` | `/api/v1/revenue` | `GET /funnel`, `GET /summary` | Revenue + conversion funnel analytics |

### 2.9 Billing & Invoices

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `billing.py` | `/api/v1/billing` | `POST /checkout`, `POST /checkout/lifetime`, `POST /capture`, `POST /webhook`, `GET /status`, `POST /stripe-checkout`, `POST /apply-stripe-coupon` | PayPal/Stripe/Razorpay billing with webhook idempotency |
| `invoices.py` | `/api/v1/invoices` | `POST /generate`, `GET /my-invoices`, `GET /{id}` | Invoice generation (JSON or HTML) |
| `coupon.py` | `/api/v1/coupon` | `POST /apply`, `POST /admin/create`, `GET /validate/{code}` | Coupon management with admin create restricted |

### 2.10 Community & Social

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `community.py` | `/api/v1/community` | `GET /feed`, `POST /feed`, `POST /feed/{id}/like`, `POST /feed/{id}/comment`, `DELETE /feed/{id}` | Community feed with likes, comments, ownership delete |
| `discussions.py` | `/api/v1/discussions` | `POST /{qid}`, `GET /{qid}`, `POST /{did}/upvote`, `POST /{did}/reply`, `GET /{qid}/summary` | Question discussions with AI summary of top discussions |

### 2.11 Student Features & Utilities

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `features.py` | `/api/v1/features` | `GET /random`, `POST /bookmarks/{id}`, `GET /bookmarks`, `POST /notes/{id}`, `GET /notes/{id}`, `DELETE /notes/{id}`, `GET /companies`, `POST /companies/follow\|unfollow`, `GET /companies/following`, `GET /companies/recommended`, `GET /notes`, `GET /recent\|bookmarked`, `GET /search`, `GET /tags` | Random problem + bookmarks/notes + company follow |
| `student_features.py` | `/api/v1/student` | `POST /cheatsheet`, `GET /cheatsheet/templates`, `POST /humanize/bullet\|resume`, `POST /applications`, `GET /applications/pipeline\|stats\|stages`, `PUT /applications/stage`, `DELETE /applications/{id}`, `POST /drill/daily\|submit`, `POST /sync/github\|generate-bullets`, `GET /sync/linkedin` | Student utility suite |
| `student_discount.py` | `/api/v1/discount` | `POST /student/verify`, `GET /student/status` | Student discount verification |
| `free_practice.py` | `/api/v1/free` | `POST /quick-interview`, `POST /quick-evaluate` | Free-tier quick interview hook (no quota consumed) |

### 2.12 Placement & Indian Market

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `placement.py` | `/api/v1/placement` | `GET /alumni` | Alumni experiences |
| `placement_calendar.py` | `/api/v1/placement-calendar` | `GET /companies`, `GET /calendar`, `GET /countdown`, `GET /company/{slug}`, `GET /boss-battles`, `GET /timeline/{slug}` | Placement calendar with predicted drives + boss battles |
| `placement_packs.py` | `/api/v1/placement-packs` | `GET /sde`, `GET /companies`, `GET /companies/{id}`, `GET /learning-objects`, `GET /learning-objects/{id}`, `GET /curation-health`, `GET /learning-paths`, `GET /learning-paths/{id}`, `POST /learning-paths/{id}/enroll`, `POST /learning-paths/{id}/modules/{mid}/complete`, `GET /my-paths` | Placement curriculum packs with pro gating |
| `placement_questions.py` | `/api/v1/placement-questions` | `GET /random`, `GET /by-company/{c}`, `GET /stats` | Placement aptitude questions |
| `indian_placement.py` | `/api/v1/indian-placement` | `GET /companies`, `GET /{id}`, `GET /{id}/mock-config\|hr-questions\|coding-patterns`, `POST /start-mock` | Indian company mocks (TCS/Infosys/Wipro/etc.) |
| `company_tracks.py` | `/api/v1/company-tracks` | `GET /companies`, `GET /companies/{id}`, `POST /companies/enroll`, `POST /companies/{id}/modules/{id}/complete`, `GET /my-tracks` | Company learning tracks |
| `company_prep.py` | `/api/v1/company-prep` | `GET /blueprints`, `GET /blueprints/{c}`, `GET /{c}/questions\|readiness`, `POST /{c}/start-assessment`, `GET /companies` | Company prep with verified-only questions |
| `company_mocks.py` | `/api/v1/company-mocks` | `POST /start`, `POST /answer`, `GET /result`, `GET /history` | Company mock portals with round configs |
| `company_lessons.py` | `/api/v1/company-lessons` | `GET /list`, `GET /{slug}`, `POST /{slug}/complete` | Company lesson content |
| `companies.py` | `/api/v1/companies` | `GET /`, `GET /{role_id}`, `GET /{role_id}/{company_id}`, `POST /{role_id}/{company_id}/stage/{order}/evaluate`, `GET /roadmap` | Company journeys with repair missions |
| `blogs.py` | `/api/v1/blogs` | `GET /list`, `GET /company/{c}`, `GET /{slug}` | Prep guides from file-backed blogs.json |

### 2.13 Repair, Evidence & Diagnostics

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `repair.py` | `/api/v1/repair` | `GET /missions`, `POST /diagnose`, `POST /retest/submit`, `GET /retest/{id}/result` | Repair loop: OA weakness → repair → retest |
| `evidence.py` | `/api/v1/evidence` | `GET /heatmap`, `GET /failures`, `GET /time-trend`, `GET /company-gap`, `GET /records`, `GET /retention`, `GET /reattempts`, `GET /mistakes`, `GET /recurring-mistakes`, `GET /pacing`, `GET /complexity`, `GET /report`, `GET /my-performance` | Student evidence views as thin aggregation layer |
| `dsa_fingerprint.py` | `/api/v1/fingerprint` | `GET /skill-profile`, `GET /company-probability` | DSA fingerprint + company predictor with probability per company |
| `distributions.py` | `/api/v1/distributions` | `GET /runtime/{id}`, `GET /memory/{id}`, `GET /comparison/{id}` | Submission distributions with histograms + percentiles |

### 2.14 AI Feedback & Debugging

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `ai_feedback.py` | `/api/v1/feedback` | `POST /sentence-level` | Sentence-level AI feedback with rewrite suggestions |
| `ai_debugger.py` | `/api/v1/ai-debugger` | `POST /analyze`, `POST /hint`, `POST /explain-error` | AI debugging assistant with step-by-step trace |

### 2.15 Admin & Content Management

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `admin_monitoring.py` | `/api/v1/admin` | `GET /dashboard/overview`, `GET /system/health`, `GET /feature-flags`, `POST /feature-flags/{n}/update-status\|set-rollout`, `GET /users/search\|export\|update\|impersonate`, `GET /content/queue`, `GET /billing/overview`, `GET /logs`, `POST /cache/clear`, `POST /system/maintenance`, `GET /system/config`, `GET /system/errors`, `POST /system/restart-service` | Admin operations dashboard |
| `admin_content.py` | `/api/v1/admin/content` | CRUD content, tranche workflow, assignment CRUD + submissions + grading | Admin content + tranche curation with independent oracle verification |

### 2.16 Miscellaneous

| File | Prefix | Key Endpoints | Purpose |
|------|--------|---------------|---------|
| `__init__.py` | — | — | Empty package init |
| `runtime.py` | `/api/v1/runtime` | `GET /workers/python.worker.js\|js.worker.js`, `GET /pyodide/{path}`, `GET /config`, `POST /execute/python\|javascript` | Browser runtime assets (Pyodide CDN redirect) |
| `enhanced.py` | `/api/v1/enhanced` | `POST /free/ats-check`, `POST /coding/company-challenge\|interviewer-feedback\|hint\|explain\|creative-mind`, `POST /behavioral/evaluate-star\|start-template\|practice-questions` | Enhanced feature bundle (free ATS is unauthenticated) |
| `enterprise.py` | `/api/v1/enterprise` | `POST /cohorts`, `GET /cohorts`, `GET /cohorts/{id}/progress` | Enterprise cohorts |
| `exam_memories.py` | `/api/v1/exam-memories` | `POST /submit`, `GET /list`, `GET /{id}`, `POST /{id}/verify`, `GET /admin/pending\|approved\|stats` | Exam memory crowd-sourcing with trust pipeline |
| `metrics.py` | `/api/v1/metrics` | `POST /event`, `GET /features`, `GET /retention` | Legacy metrics (includes removed RPG feature names) |
| `revenue.py` | `/api/v1/revenue` | `GET /funnel`, `GET /summary` | Revenue analytics |
| `tiers.py` | `/api/v1/tiers` | `GET /status`, `GET /features`, `GET /lock-reason`, `POST /check`, `GET /admin/overrides`, `POST /admin/override` | Tier/plan enforcement (free/pro/lifetime limits) |
| `visualizations.py` | `/api/v1/visualizations` | `POST /trace` | Algorithm visualization (50+ templates) |
| `unified_learning.py` | `/api/v1/unified` | `GET /lessons`, `GET /lessons/{id}`, `POST /activity`, `GET /progress`, `GET /catalog/stats`, `GET /lessons/{id}/metaphor\|intuition` | Unified learning API (single write path) |
| `journey.py` | `/api/v1/journey` | `GET /state`, `GET /outcomes` | Journey state + longitudinal outcomes |

---

## 3. Frontend Pages A-Z

### 3.1 Public Pages

| Page Component | Route Path | Purpose | Auth Required |
|----------------|-----------|---------|---------------|
| `Landing` | `/` | Hero with sakura background, gold headline, expedition path strip | No |
| `Login` | `/login` | User login | No |
| `Register` | `/register` | User registration | No |
| `ForgotPassword` | `/forgot-password` | Password reset request | No |
| `ResetPassword` | `/reset-password` | Password reset with token | No |
| `Pricing` | `/pricing` | Pricing plans | No |
| `FreeTrial` | `/free-trial` | Free trial landing | No |
| `Terms` | `/terms` | Terms of service | No |
| `Privacy` | `/privacy` | Privacy policy | No |
| `UiverseShowcase` | `/uiverse` | UI component showcase | No |
| `GoldenFlow` | `/golden`, `/golden/:conceptId` | Golden concept flow | No |
| `NotFound` | `*` | 404 page | No |

### 3.2 Authenticated Pages (ProtectedRoute + OnboardingGuard)

#### WORLD Environment — Learning Journey

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `JourneyPage` | `/world` | Learning journey hub |
| `LevelMap` | `/world/:worldId` | World/town/level progression map |
| `GoldenFlow` | `/world/:worldId/concept/:conceptId` | Golden concept flow |
| `WorldShell` | `/environments/WorldShell` | World environment shell |
| `WorldMap` | (legacy) | World map visualization |

#### LAB Environment — Interactive Learning

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `UnifiedHub` | `/lab` | Unified learning hub |
| `LessonPlayer` | `/lab/lesson/:lessonId` | Individual lesson viewer |
| `LearningModules` | `/lab/modules` | Duolingo-style learning modules |
| `LearningPaths` | `/lab/paths` | Learning paths hub |
| `Scrimba` | `/lab/scrimba` | Scrimba-style lessons |
| `AtomWorlds` | `/lab/atoms` | Atom curriculum worlds |
| `AtomLesson` | `/lab/atom/:atomId` | Individual atom lesson |
| `CurriculumHub` | `/curriculum` | Curriculum hub |
| `ConceptLearn` | `/concept-learn` | Concept learning |
| `ConceptGraph` | `/concept-graph` | Concept graph visualization |
| `ConceptFrame` | `/concept-frame` | Concept frame viewer |
| `Concepts` | `/concepts` | Concepts hub |
| `GoldenFlow` | `/lab/concept/:conceptId` | Golden concept flow |
| `VariableDiscovery` | (legacy) | Variable discovery |
| `LessonView` | (legacy) | Lesson viewer |

#### ARENA Environment — Challenges & Assessments

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `Arena` | `/arena` | Arena hub for challenges |
| `PracticeMode` | `/arena/challenge/:challengeId` | Individual challenge practice |
| `Tower` | `/arena/boss/:bossId` | Tower boss battles |
| `MockOA` | `/arena/mock-oa` | Mock online assessment |
| `MonthlyContests` | `/arena/contest/:contestId` | Monthly contests |
| `ArenaShell` | `/environments/ArenaShell` | Arena environment shell |
| `AptitudeTest` | `/aptitude` | Aptitude test |
| `CodingChallenge` | `/coding` | Coding challenge |
| `Compiler` | `/compiler` | Monaco editor with Piston |
| `SolveProblem` | `/solve/:id` | LeetCode-style problem solving |
| `PracticeMode` | `/question-bank/:questionId` | Question bank practice |
| `QuestionBank` | `/question-bank` | Question bank browse/search |
| `DailyDrill` | `/daily-drill` | Daily drill |
| `DailyChallenge` | `/daily-challenge`, `/daily-challenge/leaderboard` | Daily challenge + leaderboard |
| `ProblemOfTheDay` | `/problem-of-the-day` | Problem of the Day |
| `TcsNqtSimulation` | `/tcs-nqt` | TCS NQT simulation |
| `TcsNqtPrep` | `/tcs-nqt/prep` | TCS NQT prep |
| `MockOA` | `/mock-oa` | Mock OA |
| `SpeedSelect` | `/speed` | Speed select |
| `SlidingWindowMission` | `/mission/sliding-window` | Sliding window mission |
| `PatternPage` | `/pattern/:patternId` | Pattern-based problems |
| `PatternAnimations` | (legacy) | Pattern animations |
| `Simulator` | `/simulator` | Simulator |
| `CodePlayground` | `/playground` | Code playground |
| `Sheets` | `/sheets` | Sheets/cheatsheets |
| `CSFundamentals` | `/cs-fundamentals` | CS fundamentals |
| `MistakeBook` | `/mistakes` | Mistake book |
| `Deck` | `/deck` | Flashcard deck |
| `TeachWall` | `/teach-wall` | Teach-the-wall tutor |
| `DSAVisualizer` | `/dsa-visualizer` | DSA visualizations |
| `CompareVisualizer` | `/visualize/compare` | Algorithm comparison visualizer |

#### COMMAND Environment — Today & Readiness

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `TodayPage` | `/command/today`, `/today` | Today's tasks and missions |
| `ReadinessHeatmap` | `/command/readiness`, `/readiness` | Interview readiness heatmap |
| `RepairHub` | `/command/weaknesses`, `/repair-hub` | OA weakness repair hub |
| `MyProgress` | `/command/applications`, `/question-bank/progress` | Application tracker + progress |
| `EvidenceDashboard` | `/evidence` | Evidence dashboard |
| `Target` | `/target` | Target goals |
| `Skills` | `/skills` | Skills overview |
| `Analytics` | `/analytics` | Analytics dashboard |
| `PersonalDashboard` | `/personal-dashboard` | Personal dashboard |
| `Predictor` | `/predictor` | Placement predictor |

#### CAREER Environment — Resume & Interview

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `ResumeBuilder` | `/career/resume`, `/resume` | Resume builder |
| `ResumeStudio` | `/resume-studio` | Resume studio |
| `ATSOptimizer` | `/ats` | ATS optimizer |
| `ResumeATS` | `/resume-ats` | Resume ATS scoring |
| `Interview` | `/career/interview`, `/interview` | Interview role/company selection |
| `InterviewSession` | `/interview/:interviewId` | Live interview session |
| `InterviewBooking` | `/interview-booking` | Mock interview scheduling |
| `InterviewReplay` | `/interview-replay/:interviewId` | Interview replay |
| `CompanyTrack` | `/career/company/:companyId`, `/tracks/:company` | Company-specific track |
| `CompanyTracks` | `/career/tracks` | Company tracks list |
| `CompanyPrepHub` | `/company-prep` | Company prep hub |
| `CoverLetter` | `/cover-letter` | Cover letter generator |
| `SalaryBenchmark` | `/salary` | Salary benchmark |
| `SalaryNegotiation` | `/salary/negotiation` | Salary negotiation coach |
| `Profile` | `/profile` | User profile |
| `Settings` | `/settings` | User settings |
| `History` | `/history` | Activity history |
| `Leaderboard` | `/leaderboard` | Global leaderboard |
| `AlumniExperiences` | `/alumni-experiences` | Alumni experiences |
| `PlacementDrives` | `/placement-drives` | Placement drives |
| `PlacementCalendar` | `/placement-calendar` | Placement calendar |
| `IndianPlacement` | `/indian-placement` | Indian placement prep |

#### Gamification Pages

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `Tower` | `/tower` | Tower progression |
| `DailyChallenge` | `/daily-challenge` | Daily challenge |
| `SkillGraph` | `/skill-graph` | Skill graph visualization |
| `AnimeCards` | `/anime-cards` | Anime card gamification |
| `Arena` | `/arena` | Arena challenges |
| `ChallengePacks` | `/challenge-packs` | Challenge packs |

#### Learning Pages

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `LearningHub` | `/learning-hub` | Learning hub |
| `LanguageJourney` | `/language-journey` | Language learning paths |
| `LessonView` | `/lesson/:slug` | Lesson viewer |
| `LearningPaths` | `/learning-paths` | Learning paths |
| `CompanyTracks` | `/company-tracks` | Company tracks |
| `CurriculumHub` | `/curriculum` | Curriculum hub |
| `OnboardingQuest` | `/onboarding` | Guided onboarding |
| `StartPath` | `/start` | Start path |
| `RoleSelect` | `/role-select` | Role selection |
| `FindMyLevel` | `/diagnostic` | SDE level diagnostic |
| `LevelMap` | `/levels` | Level map |
| `Journey` | `/journey` | Learning journey |
| `StudyLibrary` | `/study-library` | Study library |
| `StudyGroups` | `/study-groups` | Study groups |
| `PrepHub` | `/prep-hub` | Prep hub |
| `Prepare` | `/prepare` | Prepare page |
| `DevLaunch` | (legacy) | Dev launch |
| `BeginnerLaunch` | (legacy) | Beginner launch |

#### Admin Pages

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `AdminDashboard` | `/admin` | Admin analytics dashboard |
| `AdminContentCorpus` | `/admin/corpus` | Admin content corpus |
| `AdminContent` | `/admin-content` | Admin content management |
| `AdminExamReview` | `/admin/exam-review` | Admin exam memory review |

#### Utility Pages

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `Settings` | `/settings` | User settings |
| `History` | `/history` | Activity history |
| `Leaderboard` | `/leaderboard` | Global leaderboard |
| `Contests` | `/contests` | Monthly contests |
| `PwaSetup` | `/pwa` | PWA setup |
| `Blogs` | `/blogs` | Blog list |
| `BlogPost` | `/blogs/:slug` | Blog post |
| `Assess` | `/assess` | Assessment |
| `Profile` | `/profile` | User profile |
| `MyAssignments` | `/my-assignments` | My assignments |
| `ModuleDetail` | `/module/:id` | Module detail |
| `TopicProblems` | `/problems/:topic` | Topic problems |
| `Topics` | `/problems` | Topics list |
| `ProblemDetail` | `/problem/:id` | Problem detail |
| `Mission` | `/mission/:missionId` | Mission page |
| `MissionResult` | `/mission/:missionId/result` | Mission result |
| `ExamMemorySubmission` | `/exam-memory/submit` | Exam memory submission |
| `ReadinessHeatmap` | `/readiness` | Readiness heatmap |
| `EvidenceDashboard` | `/evidence` | Evidence dashboard |
| `StudentDashboard` | `/student-dashboard` | Student dashboard |
| `PersonalDashboard` | `/personal-dashboard` | Personal dashboard |
| `CompanyPrepHub` | `/company-prep` | Company prep hub |
| `AIMentor` | `/ai-mentor` | AI mentor chat |

### 3.3 Environment Shells

| Page Component | Route Path | Purpose |
|----------------|-----------|---------|
| `WorldShell` | `/environments/WorldShell` | World environment shell |
| `LabShell` | `/environments/LabShell` | Lab environment shell |
| `ArenaShell` | `/environments/ArenaShell` | Arena environment shell |
| `CommandShell` | `/environments/CommandShell` | Command environment shell |
| `CareerShell` | `/environments/CareerShell` | Career environment shell |

---

## 4. Feature Area Mapping

### 4.1 Authentication & Onboarding
**Backend Routes:** `auth.py`, `onboarding.py`, `trial.py`, `free_trial.py`
**Frontend Pages:** `Login`, `Register`, `ForgotPassword`, `ResetPassword`, `OnboardingQuest`, `StartPath`, `FreeTrial`, `RoleSelect`
**API Modules:** `authApi`, `onboardingApi`, `freeTrialApi`
**Key Services:** `auth` middleware, `usage`, `email`, `rate_limiter`

### 4.2 Interview & Assessment
**Backend Routes:** `interview.py`, `interview_chat.py`, `interview_booking.py`, `assessments.py`, `oa.py`, `sde_diagnostic.py`, `behavioral.py`, `hr.py`, `quiz.py`
**Frontend Pages:** `Interview`, `InterviewSession`, `InterviewBooking`, `InterviewReplay`, `MockOA`, `Behavioral`, `Assess`, `AptitudeTest`, `TcsNqtSimulation`
**API Modules:** `interviewApi`, `bookingApi`, `oaApi`, `behavioralApi`, `hrApi`, `enhancedApi`
**Key Services:** `ai_interview`, `interview_evaluator`, `behavioral_engine`, `placement_engine`

### 4.3 Resume & Career
**Backend Routes:** `resume.py`, `cover_letter.py`, `student_features.py`, `opportunity.py`, `companies.py`, `company_prep.py`, `company_mocks.py`, `company_tracks.py`, `company_lessons.py`, `placement.py`, `placement_calendar.py`, `placement_packs.py`, `placement_questions.py`, `indian_placement.py`, `blogs.py`
**Frontend Pages:** `ResumeBuilder`, `ResumeStudio`, `ATSOptimizer`, `ResumeATS`, `CoverLetter`, `CompanyPrepHub`, `CompanyTrack`, `CompanyTracks`, `IndianPlacement`, `PlacementCalendar`, `PlacementDrives`, `AlumniExperiences`, `TcsNqtPrep`
**API Modules:** `resumeApi`, `placementApi`, `indianPlacementApi`, `companyMocksApi`, `companyPrepExamApi`, `companyLessonsApi`, `companyDirectoryApi`, `tcsNqtApi`
**Key Services:** `ai_resume`, `resume_parser`, `export`, `ats_semantic`, `ats_enhanced`, `company_roadmap`, `company_content`

### 4.4 Coding, Compiler & System Design
**Backend Routes:** `coding.py`, `compiler.py`, `system_design.py`, `system_design_tests.py`, `visualizations.py`, `trace.py`, `ai_debugger.py`
**Frontend Pages:** `CodingChallenge`, `Compiler`, `SolveProblem`, `SystemDesign`, `DSAVisualizer`, `CompareVisualizer`, `CodePlayground`, `Simulator`
**API Modules:** `codingApi`, `compilerApi`, `systemDesignApi`, `systemDesignTestsApi`, `visualizationsApi`, `aiDebuggerApi`
**Key Services:** `ai_coding`, `code_executor`, `local_sandbox`, `docker_sandbox`, `code_execution_worker`, `code_tracer`, `ai_system_design`

### 4.5 Question Bank & Practice
**Backend Routes:** `questions.py`, `questions_solve.py`, `submissions.py`, `problems.py`, `practice.py`, `arena.py`, `daily_problem.py`, `daily_challenge.py`, `playlists.py`, `features.py`, `aptitude.py`, `aptitude_tests.py`, `cs_fundamentals.py`, `tcs_nqt.py`, `tracks.py`
**Frontend Pages:** `QuestionBank`, `PracticeMode`, `ProblemOfTheDay`, `DailyDrill`, `DailyChallenge`, `AptitudeTest`, `Topics`, `TopicProblems`, `PatternPage`, `ChallengePacks`, `TcsNqtSimulation`, `Deck`, `TeachWall`, `Arena`, `CSFundamentals`, `Sheets`
**API Modules:** `questionsApi`, `codingApi`, `compilerApi`, `featuresApi`, `playlistsApi`, `submissionsApi`, `aptitudeApi`, `csFundamentalsApi`, `tcsNqtApi`, `tracksApi`, `arenaApi`, `deckApi`
**Key Services:** `question_store`, `auto_verify`, `coding_engine`, `study_engine`, `spaced_repetition`, `aptitude_question_bank`

### 4.6 Learning & Curriculum
**Backend Routes:** `lesson.py`, `learning.py`, `learning_paths.py`, `learning_modules.py`, `language_paths.py`, `atoms.py`, `concepts.py`, `unified_learning.py`, `curriculum.py`, `scrimba.py`, `roles.py`, `map.py`, `worlds.py`, `teachwall.py`, `tutor.py`, `deck.py`, `srs.py`, `study.py`, `adaptive_learning.py`, `learner.py`, `journey.py`
**Frontend Pages:** `LearningHub`, `LanguageJourney`, `LessonPlayer`, `LessonView`, `LearningPaths`, `LearningModules`, `AtomWorlds`, `AtomLesson`, `CurriculumHub`, `ConceptLearn`, `ConceptGraph`, `ConceptFrame`, `Concepts`, `UnifiedHub`, `JourneyPage`, `Journey`, `WorldMap`, `Scrimba`, `LevelMap`
**API Modules:** `lessonApi`, `learningApi`, `learningPathsApi`, `learningModulesApi`, `studyApi`, `adaptiveApi`, `learnerApi`, `journeyApi`, `mapApi`, `tutorApi`, `curriculumApi`, `unifiedApi`, `srsApi`, `deckApi`
**Key Services:** `lesson`, `learning`, `curriculum_engine`, `concept_engine`, `atom_engine`, `adaptive_learning`, `journey_engine`, `spaced_repetition`, `study_engine`

### 4.7 Gamification & Progress
**Backend Routes:** `gamification.py`, `progress.py`, `metrics.py`, `personal_dashboard.py`
**Frontend Pages:** `Tower`, `DailyChallenge`, `SkillGraph`, `AnimeCards`, `Arena`, `ChallengePacks`, `MyProgress`, `TodayPage`, `Skills`, `ReadinessHeatmap`
**API Modules:** `gamificationApi`, `progressApi`, `metricsApi`, `personalDashboardApi`
**Key Services:** `gamification`, `gamification_core`, `spaced_repetition`, `skill_assessment`

### 4.8 Analytics & Admin
**Backend Routes:** `analytics.py`, `analytics_admin.py`, `admin_monitoring.py`, `admin_content.py`, `health.py`, `revenue.py`
**Frontend Pages:** `AdminDashboard`, `AdminContentCorpus`, `AdminExamReview`, `Analytics`, `EvidenceDashboard`, `ReadinessHeatmap`
**API Modules:** `analyticsApi`, `metricsApi`, `adminContentApi`, `assignmentsApi`
**Key Services:** `analytics`, `analytics_service`, `request_metrics`, `health_checker`, `feature_flags`, `idempotency`

### 4.9 Billing & Invoices
**Backend Routes:** `billing.py`, `invoices.py`, `coupon.py`
**Frontend Pages:** `Pricing`, `FreeTrial`, `Enterprise`
**API Modules:** `billingApi`, `freeTrialApi`
**Key Services:** `invoice`, `coupon`, `monetization`, `usage`

### 4.10 Community & Social
**Backend Routes:** `community.py`, `discussions.py`
**Frontend Pages:** `Community`, `StudyGroups`, `Blogs`, `BlogPost`
**API Modules:** `communityApi`, `dailyApi` (community sub-features)
**Key Services:** `social`, `sanitizer`

### 4.11 Student Features & Utilities
**Backend Routes:** `features.py`, `student_features.py`, `student_discount.py`, `free_practice.py`
**Frontend Pages:** `StudentDashboard`, `MistakeBook`, `PrepHub`, `StudentFeatures`
**API Modules:** `studentApi`, `featuresApi`, `freePracticeApi`, `toolsApi`
**Key Services:** `cheatsheet`, `anti_plagiarism`, `application_tracker`, `daily_drill`, `profile_sync`, `student_discount`

### 4.12 Repair, Evidence & Diagnostics
**Backend Routes:** `repair.py`, `evidence.py`, `dsa_fingerprint.py`, `distributions.py`
**Frontend Pages:** `RepairHub`, `EvidenceDashboard`, `ReadinessHeatmap`, `DSAFingerprint`, `PersonalDashboard`
**API Modules:** `evidenceApi`, `dsaFingerprintApi`, `distributionsApi`, `readinessApi`
**Key Services:** `repair_service`, `evidence_aggregator`, `skill_assessment`, `placement_engine`

### 4.13 AI Feedback & Debugging
**Backend Routes:** `ai_feedback.py`, `ai_debugger.py`
**Frontend Pages:** `AIMentor`, `CodePlayground`
**API Modules:** `aiDebuggerApi`
**Key Services:** `ai_feedback`, `ai_core`

### 4.14 Content & Question Bank
**Backend Services:** `question_store.py`, `content_corpus.py`, `auto_verify.py`, `curriculum_engine.py`, `concept_engine.py`, `atom_engine.py`
**Frontend Pages:** `QuestionBank`, `PracticeMode`, `CurriculumHub`, `ConceptLearn`, `AtomWorlds`, `UnifiedHub`
**Key Concepts:**
- **Residency Rule:** Question content lives in `app/data/*.json` files, loaded into memory at startup
- **Trust Pipeline:** `UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED`
- **Serving Gate:** Only `verified`/`reviewed` content is served to students
- **No-LLM Bank Rule:** No LLM involved in question bank; deterministic auto-verify only

---

## 5. API Module Mapping

### 5.1 Frontend API Modules ↔ Backend Routes

| Frontend API Module | Backend Route Prefix | Feature Area |
|---------------------|---------------------|--------------|
| `authApi` | `/api/v1/auth` | Authentication |
| `interviewApi` | `/api/v1/interview` | Interviews |
| `bookingApi` | `/api/v1/interview-booking` | Interview Booking |
| `resumeApi` | `/api/v1/resume` | Resume |
| `billingApi` | `/api/v1/billing` | Billing |
| `aptitudeApi` | `/api/v1/aptitude` | Aptitude |
| `behavioralApi` | `/api/v1/behavioral` | Behavioral |
| `hrApi` | `/api/v1/hr` | HR Questions |
| `codingApi` | `/api/v1/coding` | Coding |
| `compilerApi` | `/api/v1/compiler` | Compiler |
| `questionsApi` | `/api/v1/questions` | Questions |
| `toolsApi` | `/api/v1/tools` | Tools (Cover Letter, etc.) |
| `companyMocksApi` | `/api/v1/company-mocks` | Company Mocks |
| `companyPrepExamApi` | `/api/v1/company-prep` | Company Prep |
| `gamificationApi` | `/api/v1/gamification` | Gamification |
| `rolesApi` | `/api/v1/roles` | Roles |
| `oaApi` | `/api/v1/oa` | OA |
| `enhancedApi` | `/api/v1/enhanced` | Enhanced Features |
| `freePracticeApi` | `/api/v1/free` | Free Practice |
| `studentApi` | `/api/v1/student` | Student Features |
| `placementApi` | `/api/v1/placement` | Placement |
| `indianPlacementApi` | `/api/v1/indian-placement` | Indian Placement |
| `systemDesignApi` | `/api/v1/system-design` | System Design |
| `systemDesignTestsApi` | `/api/v1/system-design-tests` | System Design Tests |
| `dailyApi` | `/api/v1/daily` | Daily Challenges |
| `learningApi` | `/api/v1/learning` | Learning |
| `communityApi` | `/api/v1/community` | Community |
| `learningEventsApi` | `/api/v1/learning-events` | Learning Events |
| `adaptiveApi` | `/api/v1/adaptive` | Adaptive Learning |
| `predictorApi` | `/api/v1/predictor` | Predictor |
| `readinessApi` | `/api/v1/readiness` | Readiness |
| `personalDashboardApi` | `/api/v1/dashboard` | Personal Dashboard |
| `dsaFingerprintApi` | `/api/v1/fingerprint` | DSA Fingerprint |
| `playlistsApi` | `/api/v1/playlists` | Playlists |
| `submissionsApi` | `/api/v1/submissions` | Submissions |
| `featuresApi` | `/api/v1/features` | Features |
| `visualizationsApi` | `/api/v1/visualizations` | Visualizations |
| `distributionsApi` | `/api/v1/distributions` | Distributions |
| `analyticsApi` | `/api/v1/analytics` | Analytics |
| `aiDebuggerApi` | `/api/v1/ai-debugger` | AI Debugger |
| `conceptsApi` | `/api/v1/concepts` | Concepts |
| `evidenceApi` | `/api/v1/evidence` | Evidence |
| `progressApi` | `/api/v1/progress` | Progress |
| `learningModulesApi` | `/api/v1/learning-modules` | Learning Modules |
| `studyApi` | `/api/v1/study` | Study |
| `learningPathsApi` | `/api/v1/learning-paths` | Learning Paths |
| `companyTracksApi` | `/api/v1/company-tracks` | Company Tracks |
| `freeTrialApi` | `/api/v1/free-trial` | Free Trial |
| `onboardingApi` | `/api/v1/onboarding` | Onboarding |
| `lessonApi` | `/api/v1/lesson` | Lesson |
| `journeyApi` | `/api/v1/journey` | Journey |
| `missionApi` | `/api/v1/missions` | Missions |
| `mapApi` | `/api/v1/map` | Map |
| `adminContentApi` | `/api/v1/admin/content` | Admin Content |
| `assignmentsApi` | `/api/v1/assignments` | Assignments |
| `metricsApi` | `/api/v1/metrics` | Metrics |
| `tracksApi` | `/api/v1/tracks` | Tracks |
| `tcsNqtApi` | `/api/v1/tcs-nqt` | TCS NQT |
| `companyLessonsApi` | `/api/v1/company-lessons` | Company Lessons |
| `companyDirectoryApi` | `/api/v1/company-directory` | Company Directory |
| `flatApi` / `flatOverrides` | `/api/v1/flat` | Legacy Flat |
| `examMemoriesApi` | `/api/v1/exam-memories` | Exam Memories |
| `blogsApi` | `/api/v1/blogs` | Blogs |
| `csFundamentalsApi` | `/api/v1/cs-fundamentals` | CS Fundamentals |
| `animeCardsApi` | `/api/v1/anime-cards` | Anime Cards |
| `atomsApi` | `/api/v1/atoms` | Atoms |
| `curriculumApi` | `/api/v1/curriculum` | Curriculum |
| `tutorApi` | `/api/v1/tutor` | Tutor |
| `learnerApi` | `/api/v1/learner` | Learner |
| `opportunityApi` | `/api/v1/opportunity` | Opportunity |
| `deckApi` | `/api/v1/deck` | Deck |
| `arenaApi` | `/api/v1/arena` | Arena |
| `teachwallApi` | `/api/v1/teachwall` | Teach Wall |
| `unifiedApi` | `/api/v1/unified` | Unified |

---

## 6. Cross-Cutting Systems

### 6.1 Authentication & Authorization
- **JWT + httpOnly cookies:** Access token (`pp_token`, 7d) + refresh token (`pp_refresh_token`, 30d, rotated)
- **Admin bypass:** `ADMIN_EMAILS` config grants admin regardless of plan
- **Password:** bcrypt hashing, strength validation (min 8 chars, number, special char)
- **Rate limiting:** 5 login attempts → 15 min lockout per email
- **User caching:** 5-min TTL, raw doc only; `is_admin`/`role` never cached

### 6.2 Database & Data Layer
- **Motor async client** with connection pooling (max 50, min 10)
- **87 MongoDB collections** for student state only
- **Lazy collection proxies** with typo suggestions
- **TTL indexes:** analytics_events (180d), submissions (90d), service_metrics (30d), audit_logs (1y)
- **Index-on-startup** with conflict-safe creation

### 6.3 Question Bank & Content Trust
- **Residency Rule:** Content lives in `app/data/*.json`, loaded into memory at startup
- **Trust Pipeline:** `UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED`
- **Serving Gate:** Only `verified`/`reviewed` content served
- **Quarantine:** Sticky across restarts; cleared only by human review
- **No-LLM Bank Rule:** No LLM in question bank; deterministic auto-verify only

### 6.4 Gamification
- **Single Writer:** `record_practice()` is the only writer of diamonds/coins/stars/streak/combo/badges
- **Immutable Ledger:** Every award appends `gamification_events` row
- **Level Curve:** `level = max(1, min(100, int(math.sqrt(diamonds / 50)) + 1))`
- **Streak Multipliers:** Up to 5x at 100-day streak
- **Boss Battles:** Levels 10, 20, 30... 100 with topic-specific bosses
- **Power-Ups:** 12 types (extra_time, hint_reveal, retry, double_xp, skip_boss, etc.)
- **Daily Login:** 7-tier escalating calendar
- **Weekly/Monthly Challenges:** Tracked in profile

### 6.5 Code Execution
- **Fallback Chain:** Piston → GCP compiler service → Judge0/Wandbox/Glot → Local sandbox
- **Circuit Breaker:** `compiler_breaker` (threshold=5, recovery=45s)
- **Local Sandbox:** Restricted subprocess with POSIX limits (30s CPU, 256MB AS)
- **Batch Oracle:** Python test cases run in single subprocess for zero API cost
- **12 Languages:** Python, JS, TS, Java, C++, C, Go, Rust, Ruby, PHP, Swift, Kotlin

### 6.6 Payments & Billing
- **Processors:** PayPal + Stripe + Razorpay
- **Plans:** Free, Pro ($19/mo), Lifetime ($149), Team ($145/seat/mo), Enterprise ($99/seat/mo)
- **Webhook Idempotency:** `processed_webhook_events` collection with unique `provider + event_id`
- **Coupons:** Percent/fixed discounts with usage limits
- **Invoices:** JSON or HTML format

### 6.7 Analytics & Monitoring
- **Event Ingestion:** `analytics_events` with HMAC-SHA256 IP hashing
- **Rollups:** `analytics_rollups` for fast dashboard queries
- **Request Metrics:** In-memory counters with periodic DB flush
- **TTL:** analytics_events (180d), service_metrics (30d)

### 6.8 AI Layer
- **Primary:** `google/gemma-4-31b-it:free`
- **Fallbacks:** 6 models (Nemotron, Gemma variants, Llama, Phi-3, DeepSeek)
- **Circuit Breaker:** `ai_breaker` (threshold=5, recovery=60s)
- **Caching:** 1-hour TTL (Redis or in-memory)
- **Retry:** 3 retries with exponential backoff
- **JSON Parsing:** Aggressive fallback (code fences, substring extraction, single-quote repair)

### 6.9 Frontend App Shell
- **Provider Stack:** ErrorBoundary → Toast → Theme → Background → Juice → Router
- **Routing:** React Router v6 with lazy-loaded pages
- **5-Environment Model:** WORLD | LAB | ARENA | COMMAND | CAREER
- **Guards:** ProtectedRoute (auth) + OnboardingGuard (onboarding complete)
- **Gamification Juice:** XP popups, confetti, level-up animations, combo counter
- **Page Tracking:** gtag + `/api/v1/analytics/track`
- **Search:** Cmd/Ctrl+K toggle

---

## 7. Database Collections

### 7.1 Core User & Identity
| Collection | Purpose |
|------------|---------|
| `users` | User accounts, emails, password hashes, plan, usage counters, refresh jti |
| `career_profiles` | Extended career profile data |
| `referrals` | Referral program state |

### 7.2 Interview & Assessment
| Collection | Purpose |
|------------|---------|
| `interviews` | Mock interview sessions |
| `interview_bookings` | Scheduled interview bookings |
| `interview_chat_sessions` | Real-time interview chat logs |
| `oa_sessions` | Mock online assessment sessions |
| `aptitude_tests` | Aptitude test records |
| `aptitude_leaderboard` | Aptitude leaderboard |
| `system_design` | System design practice sessions |
| `system_design_leaderboard` | System design leaderboard |
| `company_mock_tests` | Company-specific mock tests |

### 7.3 Resume & Career
| Collection | Purpose |
|------------|---------|
| `resumes` | Generated/uploaded resumes |
| `applications` | Job application tracker |
| `cover_letters` | Generated cover letters |
| `salary_offers` | Saved salary offers |

### 7.4 Learning & Content
| Collection | Purpose |
|------------|---------|
| `progress` | Learning progress per topic |
| `learning_progress` | Daily learning progress |
| `user_learning_progress` | Per-module learning progress |
| `learning_modules` | Learning module definitions |
| `learning_events` | Canonical longitudinal learning evidence layer |
| `user_learning_paths` | User-enrolled learning paths |
| `user_company_tracks` | Company-specific tracks |
| `content_modules` | Curriculum content modules |
| `assignments` | Assigned content |
| `assignment_submissions` | Assignment submissions |
| `concept_graph_nodes` | CFIC concept curriculum graph |
| `concept_mastery` | Per-user concept mastery |
| `concept_sessions` | Concept learning sessions |
| `atom_progress` | Atom-level progress |
| `thinkincode_progress` | ThinkInCode integration progress |

### 7.5 Questions & Practice
| Collection | Purpose |
|------------|---------|
| `question_answers` | User question attempts/answers |
| `solved_problems` | Solved problem records |
| `submissions` | Code submissions |
| `user_question_state` | Per-user question state |
| `question_reports` | Question bug reports |
| `served_quarantine` | Quarantined question IDs (survives restarts) |
| `practice_sessions` | Practice session logs |
| `srs_states` | Spaced repetition user state |
| `srs_cards` | SRS cards |
| `exam_memories` | Crowd-sourced exam memory submissions |

### 7.6 Gamification
| Collection | Purpose |
|------------|---------|
| `gamification` | User gamification profile (level, diamonds, streak, badges, power-ups) |
| `gamification_events` | Immutable reward ledger (every XP/coin award) |
| `daily_challenges_users` | Daily challenge enrollment and progress |

### 7.7 Social & Community
| Collection | Purpose |
|------------|---------|
| `community_posts` | Community posts |
| `discussions` | Discussion threads |
| `study_groups` | Study groups |
| `bookmarks` | User bookmarks |
| `notes` | User notes |
| `alumni_experiences` | Alumni interview experiences |
| `placement_drives` | Campus placement drives |

### 7.8 Contest & Events
| Collection | Purpose |
|------------|---------|
| `contests` | Monthly contests |
| `contest_entries` | Contest entries |
| `playlists` | Learning playlists |

### 7.9 Analytics & Monitoring
| Collection | Purpose |
|------------|---------|
| `analytics_events` | Raw analytics events (TTL 180 days) |
| `analytics_rollups` | Pre-aggregated rollup counters |
| `service_metrics` | Periodic service metrics snapshots |
| `audit_logs` | Audit log (TTL 1 year) |
| `integrity_events` | Browser integrity signals (TTL 30 days) |

### 7.10 Billing & Payments
| Collection | Purpose |
|------------|---------|
| `payments` | Payment records |
| `revenue_events` | Revenue event tracking |
| `billing_metrics` | Billing metrics |
| `invoices` | Generated invoices |
| `coupons` | Coupon codes and usage |
| `processed_webhook_events` | Idempotent webhook processing |

### 7.11 Repair & Weakness
| Collection | Purpose |
|------------|---------|
| `repair_missions` | Repair missions from OA failures |
| `repair_events` | Repair event audit trail |
| `user_weaknesses` | Misconception-tagged weaknesses |

### 7.12 Game Extensions
| Collection | Purpose |
|------------|---------|
| `anime_card_progress` | Anime card game progress |
| `anime_cards` | Anime card inventory |
| `generated_projects` | AI-generated projects |
| `tutor_sessions` | Tutor session logs |

### 7.13 Misc / Legacy
| Collection | Purpose |
|------------|---------|
| `usage_tracking` | Feature usage counters |
| `predictions` | Interview prediction history |
| `trials` | Feature trial state |
| `discounts` | Student discounts |
| `cards` | Legacy card inventory |
| `skill_graphs` | DSA skill graph |
| `served_quarantine` | Quarantine question IDs (legacy) |
| `content_tranches` | Content trust tranches |
| `question_explanations` | Community question explanations |
| `drive_trackers` | Drive tracking state |
| `tutor_sessions` | Tutor session logs |
| `processed_webhook_events` | Webhook idempotency |

---

## 8. Architecture Patterns

### 8.1 Single Sources of Truth
1. **Gamification:** `record_practice()` is the only writer of diamonds/coins/stars/streak/combo/badges
2. **Question Content:** `question_store.py` is the only question-content reader; MongoDB holds student state only
3. **Learner State:** `learner.py` provides canonical learner state for 5-environment frontend

### 8.2 Trust Pipeline
```
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED
```
- **Automated:** Deterministic checks, no LLM (structural + execution validation)
- **Human Review:** Explicit promotion to `reviewed`/`verified`
- **Quarantine:** Sticky across restarts; cleared only by human review

### 8.3 AI Reliability Stack
1. Check cache (SHA-256 key, 1-hour TTL)
2. If circuit breaker closed → try primary model with 3 retries
3. On failure → iterate 6 fallback models
4. Cache successful responses
5. Record metrics

### 8.4 Code Execution Fallback Chain
1. Local Python oracle batch (zero API cost)
2. GCP compiler service (`COMPILER_SERVICE_URL`)
3. Remote fallbacks: Judge0 / Wandbox / Glot.io
4. Local sandbox subprocess
5. Piston API

### 8.5 Frontend Rendering Rule
- **Never compute reward math client-side**
- Render exactly what `record_practice()` returns
- No independent curves or multipliers

### 8.6 Security Patterns
- httpOnly cookies for JWT (XSS-proof)
- Rate limiting (60 req/min per IP, Redis-backed)
- Login lockout (5 attempts → 15 min)
- Duplicate request guard (2-second window)
- CSP headers + security headers
- Request ID tracing
- Structured JSON logging with sensitive data redaction
- PDF magic-bytes validation
- Password strength enforcement
- Tier gating (free/pro/lifetime/enterprise)

---

## Appendix A: Unused/Legacy Pages

The following `.tsx` files exist in `frontend/src/pages/` but are **not routed** in `AppRoutes.tsx` and may be legacy:

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
- `AdminExamReview.tsx` (routed at `/admin/exam-review`)
- `ReadinessHeatmap.tsx` (routed)
- `EvidenceDashboard.tsx` (routed)
- `Profile.tsx` (routed indirectly)
- `Target.tsx` (legacy redirect)
- `Skills.tsx` (legacy redirect)
- `Analytics.tsx` (legacy redirect)
- `PersonalDashboard.tsx` (legacy redirect)

---

## Appendix B: Service File Count

| Category | Count |
|----------|-------|
| Backend Route Files | 99 |
| Backend Service Files | 90+ |
| Backend Middleware Files | 6 |
| Frontend Pages | 120+ |
| Frontend Components | 94 |
| Frontend API Modules | 39 |
| MongoDB Collections | 87 |
| Feature Flags | 50+ |
| AI Fallback Models | 6 |
| Code Execution Languages | 12 |
| Level Titles | 100 |
| Badges | 40+ |
| Power-Ups | 12 |
| Boss Battles | 10 |

---

*Generated from direct source inspection of `backend/app/routes/`, `backend/app/services/`, `frontend/src/pages/`, `frontend/src/app/AppRoutes.tsx`, `frontend/src/services/api/index.ts`, and `backend/app/database.py`.*
