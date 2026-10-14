# Backend Route Inventory
Exhaustive metadata for every `backend/app/routes/*.py` file, grouped by feature area.

Legend
- Prefix: router prefix
- Methods: representative HTTP verbs/paths
- Purpose: 1–3 word summary
- Key deps: notable services/collections
- Notes: auth, content trust, special behavior

---

## Authentication & Onboarding
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `auth.py` | `/api/v1/auth` | POST register/login/refresh, POST forgot/reset password, POST update-profile/change-password, GET onboarding-status, POST onboarding-complete | Auth lifecycle | `users_collection`, `auth` middleware, `email`, `usage`, `audit_log`, `rate_limiter` | httpOnly cookies, refresh token rotation, rate limiting, audit logging |
| `onboarding.py` | `/api/v1/onboarding` | GET doors, POST doors/complete, GET/POST launch flows | Guided onboarding | `onboarding_launch`, `role_engine.profiles`, `job_diagnostic` | Door-based entry: job/dev/beginner |
| `trial.py` | `/api/v1/trial` | POST start, GET status, POST cancel | Trial lifecycle | `trial` service | Free trial start/status/cancel |
| `free_trial.py` | `/api/v1/free-trial` | GET lessons, POST complete, GET conversion-prompt, POST track-trial | Free trial lessons | Curriculum data loaders | Conversion funnel tracking, IP-based trial attempts |

## Interview & Assessment
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `interview.py` | `/api/v1/interview` | POST start, POST answer, GET result, GET history | AI interview flow | `ai_interview`, `interview_evaluator`, `interviews_collection`, `career_profiles`, `oa_sessions`, `skill_graph` | Free tier limit, OA-aware adaptive questioning, follow-ups |
| `interview_chat.py` | `/api/v1/interview-chat` | POST start, GET session, POST turn | Conversational interview | `interview_chat_sessions_collection`, `interviews_collection`, `ai.chat_completion` | Captain Byte persona, service/product round types |
| `interview_booking.py` | `/api/v1/interview-booking` | POST book, GET upcoming/history, POST cancel, POST submit-answers | Mock interview scheduling | `interview_bookings_collection`, `interviews_collection`, `ai_interview`, `usage` | Slot overlap checks, reminder scheduling |
| `assessments.py` | `/api/v1/assessments` | POST start/{id}, POST submit/{stage}, GET report, GET definitions, GET definitions/{id} | Assessment engine | `AssessmentEngine`, `AssessmentSession`, `AssessmentDefinition` | Stub session IDs in some endpoints |
| `oa.py` | `/api/v1/oa` | POST start, POST submit-answer, GET result, GET history, GET leaderboard, POST integrity-event | Mock OA simulator | `oa_sessions_collection`, `integrity_events_collection`, `aptitude_question_bank`, `behavioral_question_bank`, `readiness_engine` | Blueprint-driven company distributions, hidden test-case coding grading |
| `sde_diagnostic.py` | `/api/v1/sde` | POST diagnostic/start, GET diagnostic/status, GET roadmap, GET skills, POST skill/update, GET mastery | SDE baseline diagnostic | `skill_assessment`, `mastery_engine`, `role_engine.profiles` | Role-specific skill graph + roadmap |
| `behavioral.py` | `/api/v1/behavioral` | GET question, GET categories, POST questions, POST feedback | Behavioral question bank | `behavioral_question_bank` data | STAR framework questions |
| `hr.py` | `/api/v1/hr` | GET question, POST questions, GET categories, POST feedback | HR question bank | `hr_question_bank` data | People-management scenarios |
| `quiz.py` | `/api/v1/quiz` | POST build, POST answer, POST hint, POST results, POST learning-path, POST boss-battle, GET stats/weak-topics/questions | Quiz + mock interview builder | `quiz_service` | Modes: practice/quiz/mock_interview/speed_run/boss_battle |

## Resume & Career
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `resume.py` | `/api/v1/resume` | POST upload, POST generate, POST optimize, POST semantic-score, POST analyze-rulebased, POST improve-bullet(s), POST tailor, POST missing-bullet, GET export/docx|pdf|history | Resume lifecycle | `resumes_collection`, `ai_resume`, `resume_parser`, `export`, `ats_semantic`, `ats_enhanced`, `real_ats` | PDF magic-bytes validation, free tier limit, gamification award |
| `cover_letter.py` | `/api/v1/tools` | POST linkedin-about | LinkedIn About generation | `resumes_collection`, `ai_cover_letter` | Reads existing resume |
| `student_features.py` | `/api/v1/student` | POST cheatsheet, GET cheatsheet/templates, POST humanize/bullet|resume, POST applications pipeline/stage/stats/delete, GET applications/stages, POST drill/daily, POST drill/submit, POST sync/github|generate-bullets, GET sync/linkedin | Student utility suite | `cheatsheet`, `anti_plagiarism`, `application_tracker`, `daily_drill`, `profile_sync` | Application tracker Kanban, daily drill |
| `student_discount.py` | `/api/v1/discount` | POST student/verify, GET student/status | Student discount verification | `student_discount` service | Email-based verification |
| `opportunity.py` | `/api/v1/opportunity` | GET companies, GET company/{company}, GET company/{company}/capabilities|fit|gaps, GET adaptive-plan | Opportunity graph | `opportunity_graph`, `learner_graph` | Capability gap analysis |
| `companies.py` | `/api/v1/companies` | GET /, GET /{role_id}, GET /{role_id}/{company_id}, POST /{role_id}/{company_id}/stage/{stage_order}/evaluate, GET roadmap | Company journeys | `company_journeys`, `company_roadmap`, `readiness_engine` | Stage evaluation + repair missions |
| `company_prep.py` | `/api/v1/company-prep` | GET blueprints, GET blueprints/{company}, GET /{company}/questions, GET /{company}/readiness, POST /{company}/start-assessment, GET companies | Company blueprints | `company_blueprints` data, `question_store` | Verified-only questions |
| `company_mocks.py` | `/api/v1/company-mocks` | POST start, POST answer, GET result, GET history | Company mock portals | `company_mock_tests_collection`, `ai_core`, `repair_service` | Company-specific round configs |
| `company_tracks.py` | `/api/v1/company-tracks` | GET companies, GET companies/{track_id}, POST companies/enroll, POST companies/{track_id}/modules/{module_id}/complete, GET my-tracks | Company learning tracks | `learning_paths` service | Module progress + enrollment |
| `company_lessons.py` | `/api/v1/company-lessons` | GET list, GET /{slug}, POST /{slug}/complete | Company lesson content | File-based lessons, `gamification.record_practice` | JSON lesson files on disk |
| `placement.py` | `/api/v1/placement` | GET alumni | Alumni experiences | `company_conversion.list_alumni_experiences` | Thin read-only route |
| `placement_calendar.py` | `/api/v1/placement-calendar` | GET companies, GET calendar, GET countdown, GET company/{slug}, GET boss-battles, GET timeline/{slug} | Placement season calendar | `placement_calendar` service | Predicted drive dates, boss battle triggers |
| `placement_packs.py` | `/api/v1/placement-packs` | GET sde, GET companies, GET companies/{id}, GET learning-objects, GET learning-objects/{id}, GET curation-health, GET learning-paths, GET learning-paths/{id}, POST learning-paths/{id}/enroll, POST learning-paths/{id}/modules/{mid}/complete, GET my-paths | Placement curriculum packs | File-backed curriculum data | Pro gating for full blueprints |
| `placement_questions.py` | `/api/v1/placement-questions` | GET random, GET by-company/{company}, GET stats | Placement aptitude questions | `placement_aptitude_questions` data | Pattern-relevant company alignment |
| `indian_placement.py` | `/api/v1/indian-placement` | GET companies, GET /{id}, GET /{id}/mock-config, GET /{id}/hr-questions, GET /{id}/coding-patterns, POST start-mock | Indian company mocks | `indian_companies` data, `question_store` | Verified-only bank, thin sections |
| `blogs.py` | `/api/v1/blogs` | GET list, GET /company/{company}, GET /{slug} | Company prep guides | `data/blogs.json` | File-backed, provenance-labeled |

## Coding, Compiler & System Design
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `coding.py` | `/api/v1/coding` | GET topics, POST start, POST submit, POST hint, POST interviewer-feedback | Coding challenges | `coding_challenges_collection`, `ai_coding`, `coding_engine`, `code_executor`, `gamification`, `usage` | Company-specific challenge generation, repair trigger |
| `compiler.py` | `/api/v1/compiler` | POST execute, POST execute-test-cases, GET job/{id}, GET languages, POST starter-code, POST boilerplate, POST trace | Code execution | `CodeExecutionEngine`, `job_queue`, `websocket_manager`, `feature_flags` | Sync + async modes, kill switch, WebSocket updates |
| `system_design.py` | `/api/v1/system-design` | POST start, POST answer, GET /{session_id}/result | System design practice | `system_design_collection`, `ai_system_design`, `usage` | Bank-first question selection |
| `system_design_tests.py` | `/api/v1/system-design-tests` | GET categories, GET problems, GET problem/{id}, POST evaluate/{id} | System design test bank | `system_design_bank.json`, `ai_core` | File-backed bank, AI rubric evaluation |
| `visualizations.py` | `/api/v1/visualizations` | POST trace | Algorithm visualization | `code_tracer`, `ai_core` | 50+ pre-built templates + AI traces |
| `trace.py` | `/api/v1/trace` | POST generate | Algorithm trace generation | `algorithm_tracer` | Step-by-step visual trace data |
| `ai_debugger.py` | `/api/v1/ai-debugger` | POST analyze, POST hint, POST explain-error | AI debugging assistant | `question_store`, `code_executor`, `ai_core` | In-memory question store only |

## Question Bank & Practice
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `questions.py` | `/api/v1/questions` | GET browse, GET random, GET /{id}, GET /{id}/solution, GET /{id}/solved, POST /{id}/submit, POST /{id}/answer, GET stats, GET recent, GET filters, POST submit, POST upvote | Question bank browsing + curation | `question_answers_collection`, `solved_problems_collection`, `question_reports_collection`, `served_quarantine_collection`, `question_store`, `ai_core`, `code_executor`, `explanation_cache` | Daily free quota, verified-only serving, content trust quarantine |
| `questions_solve.py` | `/api/v1/questions` | POST /{id}/submit, POST /{id}/answer, GET /{id}/hints, GET /{id}/solution | Question solving flow | Same as `questions.py` | Code execution + AI feedback |
| `submissions.py` | `/api/v1/submissions` | POST /{id}/submit, GET history | Submission history + solved tracking | `submissions_collection`, `solved_problems_collection`, `question_answers_collection`, `code_executor`, `question_store` | Failure class enum for evidence layer |
| `problems.py` | `/api/v1/problems` | POST, GET, GET /{id}, GET /{id}/visible, GET /{id}/lock-state, POST /{id}/reset-locks, POST /{id}/check-lock, POST /{id}/run | Lock-engine problem CRUD | `lock_engine`, `unified_judge`, seed script | In-memory `PROBLEMS_DB` |
| `practice.py` | `/api/v1/practice` | POST session, POST session/{id}/complete, GET sessions | Role-based practice sessions | `practice_sessions_collection`, `placement_engine`, `company_conversion`, `skill_graph`, `gamification`, `repair_service` | Weak/strong area detection, repair triggers |
| `arena.py` | `/api/v1/arena` | GET quiz, POST submit | MCQ practice arena | `question_store`, `study_engine`, `gamification`, `repair._grade_mcq`, `diagnosis` | MCQ-only, answers stripped client-side |
| `daily_problem.py` | `/api/v1/daily-problem` | GET today, POST submit | Problem of the Day | `question_store`, `solved_problems_collection`, `gamification_collection`, `code_executor`, `gamification` | Deterministic UTC-date selection |
| `daily_challenge.py` | `/api/v1/daily` | GET challenge, POST submit, GET leaderboard, POST join | Daily challenge + leagues | `solved_problems_collection`, `question_answers_collection`, `gamification_collection`, `users_collection`, `cache` | Weakness-based mission builder, Diamond leagues |
| `playlists.py` | `/api/v1/playlists` | GET list, GET /{id} | Curated playlists | `playlists_collection`, `question_store`, `solved_problems_collection` | In-memory verified pool |
| `features.py` | `/api/v1/features` | GET random, POST bookmarks/{id}, GET bookmarks, POST notes/{id}, GET notes/{id} | Random problem, bookmarks, notes | `bookmarks_collection`, `notes_collection`, `solved_problems_collection`, `question_store` | |
| `aptitude.py` | `/api/v1/aptitude` | GET categories, GET theory, GET theory/{id}, GET theory-for/{category}, POST start, POST /{id}/answer, POST /{id}/complete | Aptitude drills + theory | `aptitude_question_bank`, `aptitude_theory`, `repair_service` | In-memory sessions |
| `aptitude_tests.py` | `/api/v1/aptitude-tests` | GET categories, GET configurations, POST start, POST /{id}/answer, POST /{id}/complete, GET leaderboard, GET history | Timed aptitude tests | `aptitude_tests_collection`, `aptitude_leaderboard_collection`, `gamification` | Test configs: quick/standard/advanced/mock |
| `cs_fundamentals.py` | `/api/v1/cs-fundamentals` | GET theory, GET theory/{id}, GET domain/{domain} | CS theory cards | `cs_fundamentals_theory` data | File-backed, no DB/LLM |
| `tcs_nqt.py` | `/api/v1/tcs-nqt` | GET patterns, GET patterns/{p}/questions, POST patterns/{p}/assess, GET progress, POST questions/{id}/verify | TCS NQT prep | `question_store` | Domain filtering: Quantitative/Logical/Verbal/Programming Logic |
| `tracks.py` | `/api/v1/tracks` | GET /{company}/overview | Company track overview | `question_store`, `solved_problems_collection`, `question_answers_collection`, `oa` route helpers | Verified bank + student status |
| `quiz.py` | `/api/v1/quiz` | POST build, POST answer, POST hint, POST results, POST learning-path, POST boss-battle, GET stats/weak-topics/questions | Quiz + boss battles | `quiz_service` | Modes: practice/quiz/mock_interview/speed_run/boss_battle |

## Learning & Curriculum
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `lesson.py` | `/api/v1/lesson` | GET /{slug}, GET /{slug}/step/{key}, POST /{slug}/run|build|transfer|predict|explain|break|assess|complete, GET plan/{id}, GET next-action | Vertical-slice lesson engine | `LessonService`, `adaptive_lesson_planner`, `learner_graph`, `curriculum.registry` | 9-step teaching loop |
| `learning.py` | `/api/v1/learning` | POST interaction-action, POST diagnose | Learning interaction logging | `action_trace_logger`, `misconception_diagnosis` | Misconception detection |
| `learning_paths.py` | `/api/v1/learning-paths` | GET roles, GET roles/{id}, POST roles/enroll, POST roles/{id}/modules/{id}/complete, GET my-paths, GET recommendations | Role-based learning paths | `learning_paths` service, `models.learning_path` | SDE/Data Analyst/QA/DevOps |
| `learning_modules.py` | `/api/v1/learning-modules` | GET list, GET /{id}, POST /{id}/start, POST /{id}/steps/{n}/complete | Duolingo-style modules | `learning_modules_collection`, `user_learning_progress_collection` | Step-based progression |
| `language_paths.py` | `/api/v1/languages` | GET /, GET /{id}, GET /{id}/levels, GET /{id}/modules/{idx}, GET /{id}/progress, POST /{id}/modules/{idx}/complete | 7-language paths | `language_modules`, `language_levels`, `language_progress` | 100 levels x 80 modules per language |
| `atoms.py` | `/api/v1/atoms` | GET worlds, GET world/{id}, GET /{id}, GET /{id}/animation|zero-code|analogies|mastery, GET path/{company}, GET company/{id}, GET languages, GET language/{id}/concept/{id}, POST attempt, POST check-misconception, GET progress/world/{id}|atom/{id}, GET /{id}/intuition | Atom curriculum | `atom_engine`, `company_atom_map` | 50-atom Concept Clarity Curriculum |
| `concepts.py` | `/api/v1/concepts` | GET graph, GET progress, GET sessions/{id}, GET concept/{id}/frame, POST concept/{id}/frame/result | CFIC concept graph | `content.cfic_curriculum`, `concept_engine`, `concept_mastery` | Additive collections: concept_graph_nodes, concept_mastery, concept_sessions |
| `unified_learning.py` | `/api/v1/unified` | GET lessons, GET lessons/{id}, POST activity, GET progress, GET catalog/stats, GET lessons/{id}/metaphor, GET lessons/{id}/intuition | Unified learning catalog | `unified_learning` service, `unified_catalog` | Aggregates all content sources |
| `curriculum.py` | `/api/v1/curriculum` | GET missions, GET missions/{id} | Flagship curriculum missions | `curriculum` service | |
| `scrimba.py` | `/api/v1/scrimba` | GET lessons, GET lessons/{id}, POST complete | Scrimba-style lessons | `scrimba_lessons` content, `gamification`, `spaced_repetition` | SRS + repair trigger |
| `roles.py` | `/api/v1/roles` | GET /, GET /{id}, GET /{id}/content|exercises|quizzes|challenges|practice-sets, POST /{id}/activity, GET /{id}/next|dashboard, GET exercise/{id}|challenge/{id}|quiz/{id} | Role content packages | `role_packages`, `role_content`, `role_content_service` | |
| `map.py` | `/api/v1/map` | GET map data | Adventure map | `worlds_data`, `routes.worlds`, `gamification` | Serpentine positions, fog-of-war, repair nodes |
| `worlds.py` | `/api/v1/worlds` | GET /{id}, GET /{id}/progress, POST /{id}/levels/{id}/attempt|complete|hint | World/town/level progression | `worlds_data`, `gamification_collection`, `skill_graph_collection`, `srs_cards_collection`, `code_executor` | Deterministic judge + SRS |
| `teachwall.py` | `/api/v1/teachwall` | GET challenge, POST answer | Teach-the-wall tutor play | `tutor_engine`, `study_engine` | Deterministic shuffle per node |
| `tutor.py` | `/api/v1/tutor` | POST act | AI tutor action | `ai_tutor.tutor_act` | |
| `deck.py` | `/api/v1/deck` | GET today, POST review | Daily flashcard deck | `srs_cards_collection`, `spaced_repetition`, `atom_engine` | SRS namespaced as `deck:{atom_id}` |
| `srs.py` | `/api/v1/srs` | GET due, GET stats, POST record, GET problem/{id}, DELETE problem/{id} | Spaced repetition for problems | `srs_cards_collection`, `spaced_repetition` | SM-2 scheduling |
| `study.py` | `/api/v1/study` | GET today, POST activity | Canonical daily study plan | `study_engine` | Legacy alias `/adaptive/daily-plan` |
| `adaptive_learning.py` | `/api/v1/adaptive` | GET skills, GET weak-areas, GET daily-plan, GET recommendations, GET learning-path, GET readiness, POST activity, GET domains | Adaptive learning paths | `adaptive_learning` service, `readiness_engine` | |
| `learner.py` | `/api/v1/learner` | GET state | Canonical learner state | `learner_graph` | Single source for 5-environment frontend |
| `journey.py` | `/api/v1/journey` | GET state, GET outcomes | Journey state + longitudinal outcomes | `journey_engine`, `readiness_engine`, `learning_events_collection`, `interviews_collection`, `oa_sessions_collection` | Composes Study/Gamification/Mastery/Readiness/Worlds |

## Gamification & Progress
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `gamification.py` | `/api/v1/gamification` | GET profile, POST profile/target-company, GET profile/title-progression, GET readiness, GET readiness/simulate, POST record, GET leaderboard, GET badges, GET skills, GET skills/weak, GET skills/readiness, GET tower, GET tower/boss/{level}, POST power-ups/{id}/use|buy, POST streak-freeze|repair, GET streak-status|forest-state|daily-goal|daily-login, POST daily-bonus|daily-login/claim, GET achievement-chains | Gamification profile + rewards | `gamification_collection`, `users_collection`, `skill_assessment`, `readiness_engine`, `idempotency` | Only `record_practice` writes XP/coins/stars/streak/badges |
| `progress.py` | `/api/v1/progress` | GET heatmap, GET streak, GET topic-progress, GET weekly-goal | Progress tracking + heatmap | `solved_problems_collection`, `submissions_collection`, `gamification_collection`, `question_store` | |
| `metrics.py` | `/api/v1/metrics` | POST event, GET features, GET retention | Feature metrics + retention | `feature_events` collection | Legacy feature list includes removed RPG features |
| `personal_dashboard.py` | `/api/v1/dashboard` | GET personal, GET weak-areas | Personal dashboard | `solved_problems_collection`, `question_answers_collection`, `users_collection`, `question_store`, `readiness_engine` | Weak area analysis + recommendations |

## Analytics & Admin
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `analytics.py` | `/api/v1/analytics` | GET overview, GET funnel, GET skills, GET companies, GET insights | User analytics | `analytics` service | |
| `analytics_admin.py` | `/api/v1/analytics` | POST track, GET admin/realtime|visitors|pages|features|hourly|geo|retention|users|summary | Admin analytics | `analytics_service`, `require_admin` | Public tracking with rate limit; admin endpoints restricted |
| `admin_monitoring.py` | `/api/v1/admin` | GET dashboard/overview, GET system/health, GET feature-flags, POST feature-flags/{n}/update-status|set-rollout, GET users/search|export|update|impersonate, GET content/queue, GET billing/overview, GET logs, POST cache/clear, POST system/maintenance, GET system/config, GET system/errors, POST system/restart-service | Admin operations dashboard | `health_checker`, `feature_flags`, `get_db`, `require_admin` | Feature flag management, user search/export/impersonation |
| `admin_content.py` | `/api/v1/admin/content` | POST, GET /{id}, PUT /{id}, DELETE /{id}, GET list, POST tranche/{tid}/stage, GET tranche/{tid}/stage, POST tranche/{tid}/promote, GET tranche/{tid}/status, GET tranche/list, POST assignments, GET assignments, GET assignments/{id}, POST assignments/{id}/submit, GET assignments/{id}/submissions, POST assignments/{id}/grade | Admin content + tranche workflow | `content_modules_collection`, `assignments_collection`, `assignment_submissions_collection`, `content_tranches_collection`, `gamification` | Tranche staging + independent oracle verification |
| `health.py` | `/api/v1/health` | GET ping, GET status, GET ready, GET live, GET metrics, GET dependencies | Health checks | `health_checker` | Kubernetes-style probes |
| `revenue.py` | `/api/v1/revenue` | GET funnel, GET summary | Revenue + conversion funnel | `users_collection`, `trials_collection`, `require_admin` | Approx MRR/ARR |

## Billing & Invoices
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `billing.py` | `/api/v1/billing` | POST checkout, POST checkout/lifetime, POST capture, POST webhook, GET status, POST stripe-checkout, POST apply-stripe-coupon | PayPal billing | `users_collection`, `payments_collection`, `coupons_collection`, `processed_webhook_events_collection`, `revenue`, `coupon`, `invoice` | Webhook idempotency, coupon application |
| `invoices.py` | `/api/v1/invoices` | POST generate, GET my-invoices, GET /{id} | Invoice generation | `InvoiceService`, `users_collection` | |
| `coupon.py` | `/api/v1/coupon` | POST apply, POST admin/create, GET validate/{code} | Coupon management | `coupon` service | Admin create restricted |

## Community & Social
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `community.py` | `/api/v1/community` | GET feed, POST feed, POST feed/{id}/like, POST feed/{id}/comment, DELETE feed/{id} | Community feed | `community_posts` collection, `sanitizer` | Likes, comments, ownership delete |
| `discussions.py` | `/api/v1/discussions` | POST /{qid}, GET /{qid}, POST /{did}/upvote, POST /{did}/reply, GET /{qid}/summary | Question discussions | `discussions_collection`, `users_collection`, `ai`, `question_store` | AI summary of top discussions |

## Student Features & Utilities
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `features.py` | `/api/v1/features` | GET random, POST bookmarks/{id}, GET bookmarks, POST notes/{id}, GET notes/{id}, DELETE notes/{id}, GET companies, POST companies/follow|unfollow, GET companies/following, GET companies/recommended, GET notes, GET recent|bookmarked, GET search, GET tags | Random problem + bookmarks/notes | `bookmarks_collection`, `notes_collection`, `solved_problems_collection`, `question_store` | Company follow/unfollow |
| `student_features.py` | `/api/v1/student` | POST cheatsheet, GET cheatsheet/templates, POST humanize/bullet|resume, POST applications, GET applications/pipeline|stats|stages, PUT applications/stage, DELETE applications/{id}, POST drill/daily|submit, POST sync/github|generate-bullets, GET sync/linkedin | Student utility suite | `cheatsheet`, `anti_plagiarism`, `application_tracker`, `daily_drill`, `profile_sync` | |
| `student_discount.py` | `/api/v1/discount` | POST student/verify, GET student/status | Student discount | `student_discount` | |
| `free_practice.py` | `/api/v1/free` | POST quick-interview, POST quick-evaluate | Free interview hook | `ai_interview` | No quota consumed |

## Placement & Indian Market
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `placement.py` | `/api/v1/placement` | GET alumni | Alumni experiences | `company_conversion` | |
| `placement_calendar.py` | `/api/v1/placement-calendar` | GET companies, GET calendar, GET countdown, GET company/{slug}, GET boss-battles, GET timeline/{slug} | Placement calendar | `placement_calendar` service | Predicted drives + boss battles |
| `placement_packs.py` | `/api/v1/placement-packs` | GET sde, GET companies, GET companies/{id}, GET learning-objects, GET learning-objects/{id}, GET curation-health, GET learning-paths, GET learning-paths/{id}, POST learning-paths/{id}/enroll, POST learning-paths/{id}/modules/{mid}/complete, GET my-paths | Placement packs | File-backed curriculum | Pro gating |
| `placement_questions.py` | `/api/v1/placement-questions` | GET random, GET by-company/{c}, GET stats | Placement aptitude questions | `placement_aptitude_questions` data | Pattern-relevant |
| `indian_placement.py` | `/api/v1/indian-placement` | GET companies, GET /{id}, GET /{id}/mock-config|hr-questions|coding-patterns, POST start-mock | Indian company mocks | `indian_companies`, `question_store` | Verified-only bank |
| `company_tracks.py` | `/api/v1/company-tracks` | GET companies, GET companies/{id}, POST companies/enroll, POST companies/{id}/modules/{id}/complete, GET my-tracks | Company tracks | `learning_paths` service | |
| `company_prep.py` | `/api/v1/company-prep` | GET blueprints, GET blueprints/{c}, GET /{c}/questions|readiness, POST /{c}/start-assessment, GET companies | Company prep | `company_blueprints`, `question_store` | |
| `company_mocks.py` | `/api/v1/company-mocks` | POST start, POST answer, GET result, GET history | Company mock portals | `company_mock_tests_collection`, `ai_core`, `repair_service` | Round configs per company |
| `company_lessons.py` | `/api/v1/company-lessons` | GET list, GET /{slug}, POST /{slug}/complete | Company lessons | File-backed lessons, `gamification` | |
| `companies.py` | `/api/v1/companies` | GET /, GET /{role_id}, GET /{role_id}/{company_id}, POST /{role_id}/{company_id}/stage/{order}/evaluate, GET roadmap | Company journeys | `company_journeys`, `company_roadmap`, `readiness_engine` | Repair missions on failure |
| `blogs.py` | `/api/v1/blogs` | GET list, GET /company/{c}, GET /{slug} | Prep guides | `data/blogs.json` | |

## Repair, Evidence & Diagnostics
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `repair.py` | `/api/v1/repair` | GET missions, POST diagnose, POST retest/submit, GET retest/{id}/result | Repair loop | `repair_service`, `question_store`, `code_executor` | Verified-only retest content |
| `evidence.py` | `/api/v1/evidence` | GET heatmap, failures, time-trend, company-gap, records, retention, reattempts, mistakes, recurring-mistakes, pacing, complexity, report, my-performance | Student evidence views | `evidence_aggregator` | Thin aggregation layer |
| `dsa_fingerprint.py` | `/api/v1/fingerprint` | GET skill-profile, GET company-probability | DSA fingerprint + company predictor | `solved_problems_collection`, `submissions_collection`, `aptitude_collection`, `gamification_collection`, `question_store`, `indian_companies` | Probability per company |
| `distributions.py` | `/api/v1/distributions` | GET runtime/{id}, GET memory/{id}, GET comparison/{id} | Submission distributions | `submissions_collection`, `solved_problems_collection`, `question_store` | Histograms + percentiles |

## AI Feedback & Debugging
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `ai_feedback.py` | `/api/v1/feedback` | POST sentence-level | Sentence-level AI feedback | `ai_feedback.sentence_level_feedback` | |
| `ai_debugger.py` | `/api/v1/ai-debugger` | POST analyze, POST hint, POST explain-error | AI debugger | `question_store`, `code_executor`, `ai_core` | Step-by-step trace |

## Admin & Content Management
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `admin_monitoring.py` | `/api/v1/admin` | GET dashboard/overview, GET system/health, GET feature-flags, POST feature-flags/{n}/update-status|set-rollout, GET users/search|export|update|impersonate, GET content/queue, GET billing/overview, GET logs, POST cache/clear, POST system/maintenance, GET system/config, GET system/errors, POST system/restart-service | Admin operations | `health_checker`, `feature_flags`, `get_db`, `require_admin` | |
| `admin_content.py` | `/api/v1/admin/content` | CRUD content, tranche workflow, assignment CRUD + submissions + grading | Admin content + tranche curation | `content_modules_collection`, `assignments_collection`, `content_tranches_collection`, `gamification` | Independent oracle verification |

## Miscellaneous
| File | Prefix | Methods | Purpose | Key Deps | Notes |
|---|---|---|---|---|---|
| `__init__.py` | — | — | Empty package init | — | |
| `runtime.py` | `/api/v1/runtime` | GET workers/python.worker.js|js.worker.js, GET pyodide/{path}, GET config, POST execute/python|javascript | Browser runtime assets | `local_runtime` | Pyodide CDN redirect |
| `enhanced.py` | `/api/v1/enhanced` | POST free/ats-check, POST coding/company-challenge|interviewer-feedback|hint|explain|creative-mind, POST behavioral/evaluate-star|start-template|practice-questions | Enhanced feature bundle | `coding_engine`, `behavioral_engine`, `free_ats_tool`, `monetization`, `ai_core` | Free ATS is unauthenticated |
| `enterprise.py` | `/api/v1/enterprise` | POST cohorts, GET cohorts, GET cohorts/{id}/progress | Enterprise cohorts | `cohorts` collection, `skill_graphs`, `gamification` | |
| `exam_memories.py` | `/api/v1/exam-memories` | POST submit, GET list, GET /{id}, POST /{id}/verify, GET admin/pending|approved|stats | Exam memory crowd-sourcing | `exam_memories_collection`, `users_collection`, `gamification` | Trust pipeline: new → verified_crowd → approved → file bank |
| `metrics.py` | `/api/v1/metrics` | POST event, GET features, GET retention | Legacy metrics | `feature_events` | Includes removed RPG feature names |
| `revenue.py` | `/api/v1/revenue` | GET funnel, GET summary | Revenue analytics | `users_collection`, `trials_collection`, `require_admin` | |
| `tiers.py` | `/api/v1/tiers` | GET status, GET features, GET lock-reason, POST check, GET admin/overrides, POST admin/override | Tier/plan enforcement | `users_collection`, `usage`, `require_admin` | Free/pro/lifetime limits |
| `visualizations.py` | `/api/v1/visualizations` | POST trace | Algorithm visualization | `code_tracer`, `ai_core` | 50+ templates |
| `unified_learning.py` | `/api/v1/unified` | GET lessons, GET lessons/{id}, POST activity, GET progress, GET catalog/stats, GET lessons/{id}/metaphor|intuition | Unified learning API | `unified_learning`, `unified_catalog` | Single write path |
| `journey.py` | `/api/v1/journey` | GET state, GET outcomes | Journey state + outcomes | `journey_engine`, `readiness_engine`, `learning_events_collection`, `interviews_collection`, `oa_sessions_collection` | Longitudinal outcome report |
