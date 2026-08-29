# AGENTS.md — PlacementPro

## Project Overview

**PlacementPro** is an AI-powered placement preparation platform targeting job seekers (students + experienced professionals). It offers **40+ core features** across placement prep, gamified learning, and career development.

### Core Features
1. **AI Interviewer** — Mock interviews with AI that asks questions, evaluates answers, and gives feedback
2. **System Design Practice** — System design interviews with AI evaluation of architecture, scalability, and trade-offs
3. **Coding Challenges** — Timed coding problems with solutions and follow-up challenges
4. **LeetCode-Style Compiler** — Full code execution environment with Monaco Editor, test cases, and hidden judge
5. **Company-Specific Prep** — 53+ company prep with FAANG leadership principles, behavioral questions
6. **Resume Builder/Analyzer** — Upload existing resume or generate new one with AI
7. **ATS Score Optimizer** — Match resume to job descriptions, identify missing keywords, rewrite for ATS
8. **Aptitude Test Practice** — Quantitative, logical, verbal, technical MCQs for campus placements
9. **Cover Letter & LinkedIn** — AI-generated cover letters and LinkedIn About sections
10. **Salary Benchmark** — Market rate data, percentile breakdowns, company comparisons
11. **Salary Negotiation Coach** — AI-powered tips and scripts for negotiating offers
12. **Question Bank** — 100+ curated problems with visible/hidden test cases, company/topic filters
13. **Learning Hub** — Duolingo-style step-by-step coding lessons across 7 languages
14. **Gamification System** — XP, levels (1-100), streaks, badges, tower progression, power-ups, boss battles
15. **Daily Challenges** — Adaptive daily missions with leaderboards and rewards
16. **Mock Interviews** — Scheduled mock interviews with booking system
17. **Career Profile** — User career profile with skills, experience, portfolio
18. **Application Tracker** — Track job applications with status management
19. **Placement Drives** — Upcoming campus placement drives with deadlines and tiers
20. **Alumni Experiences** — Peer interview experiences and company insights
21. **AI Debugger** — AI-powered code debugging and error explanation
22. **DSA Fingerprint** — Personalized DSA skill assessment and gap analysis
23. **Visualizations** — Algorithm visualizations (sorting, graph, DP, etc.)
24. **Community** — Study groups, discussions, peer accountability
25. **Project Generator** — AI-generated complete projects from descriptions
26. **Code Review** — AI-powered project code review with actionable feedback
27. **Adaptive Learning** — AI-driven personalized learning paths
28. **Monthly Contests** — Competitive contests with prizes
29. **Challenge Packs** — Curated problem packs by topic/difficulty
30. **Onboarding Quest** — Guided onboarding with skill self-assessment
31. **Free Practice** — 3-question quick interview, instant evaluations
32. **Trial System** — Feature trials for Pro features
33. **Student Discounts** — Discount codes for students
34. **Enterprise** — Enterprise plan with admin dashboard
35. **Analytics** — Admin analytics dashboard with metrics
36. **AI Feedback** — Real-time AI-powered answer feedback
37. **Concept Explanations** — Learn coding concepts at beginner/intermediate/expert levels
38. **Language Learning Paths** — 7 languages x 100 levels x 80 modules
39. **Learning Journeys** — Structured learning paths with progress tracking
40. **Learning Modules** — Step-by-step coding lessons
41. **Interview Booking** — Schedule mock interviews with specific companies
42. **Company Mock Tests** — Company-specific mock test series
43. **Distributions** — Salary distribution comparisons
44. **Features** — Feature comparison and upsell
45. **PWA** — Progressive Web App with install prompt

### Removed Features (August 2026 Cleanup)
The following experimental/RPG-themed features were removed to reduce codebase bloat:
- Guild system, dungeons, grand line, steam profile, newspaper, merchant, economy
- Game events, guilds, world, skill trees, seasons, tournaments, teams, themes
- Trending challenges, shareable achievements, career RPG, bounty, live events
- Mission engine, hook model, cards, scrims, showcase, referrals, big four
- Campus wars, campus connect, campus pulse, campus, college network
- CGPA simulator, drive tracker, peer review, study squads, report card
- Battles, quests, goals, friends, referral, collection, journey
- Achievements, skill mastery, timeline, daily orders, invite, debug
- Real features, mass recruiter, pseudocode, rank, job readiness
- Energy system, mystery boxes, prestige, battle pass, wizard, lucky wheel
- Chat, GD rooms, discussions, behavioral practice, company directory

## Target Users
- **Indian students:** Campus placement preparation (TCS, Infosys, Wipro, etc.) with aptitude tests
- **US/Global job seekers:** Behavioral interviews, resume optimization, salary negotiation, system design
- **Professionals:** Career changers, job switchers, FAANG aspirants

## Business Model
Freemium (Free + Pro $9/mo + Lifetime $39 one-time). Free tier resets monthly with extensive limits.

**Built with:** MimoCode (AI coding assistant). Includes a LeetCode-style coding compiler with Monaco Editor and Piston API execution engine.

---

## Architecture

### Backend (FastAPI + MongoDB + Motor)
- **82 route files** — 100+ API endpoints organized by feature
- **82 service files** — Business logic, AI, execution, analytics
- **50+ MongoDB collections** — Each feature has its own collection
- **Async throughout** — All routes use `async def` with `motor` async driver

### Frontend (React 18 + Vite 5 + Tailwind 3)
- **91 pages** (lazy-loaded with `React.lazy()` for code splitting)
- **94 components** (UI, layout, gamification, animations)
- **39 API modules** aggregated in `services/api/index.ts`
- **Zustand** for global auth state only
- **Framer Motion** for page transitions and celebrations
- **Monaco Editor** for code editing

### AI Layer
- **OpenRouter → Gemini 2.0 Flash** as primary model
- **4 fallback models** (Llama 3.1, Phi-3 Mini, DeepSeek) with circuit breaker protection
- **In-memory + Redis caching** (1-hour TTL for AI responses)
- **Retry logic** — 3 retries with exponential backoff
- **AI prompts** in `services/ai.py` (split across domain-specific modules)

---

## Project Structure
```
placementpro/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, lifespan, middleware, auto-discovers routes
│   │   ├── config.py            # Pydantic Settings (all env vars, 50+ settings)
│   │   ├── database.py          # Motor client, 50+ collection refs, init_db()
│   │   ├── models/
│   │   │   ├── user.py          # UserCreate, UserLogin, UserInDB
│   │   │   ├── interview.py     # StartInterview, SubmitAnswer, QARecord
│   │   │   └── resume.py        # GenerateResume, OptimizeRequest
│   │   ├── routes/              # 82 route files (auto-discovered by main.py)
│   │   │   ├── auth.py          # Register, login, logout, onboarding
│   │   │   ├── interview.py     # Interview flow with follow-ups
│   │   │   ├── resume.py        # Upload, generate, optimize, export
│   │   │   ├── billing.py       # PayPal checkout, webhooks, status
│   │   │   ├── aptitude.py      # Aptitude test flow
│   │   │   ├── questions.py     # Question bank browse, submit, solve
│   │   │   ├── gamification.py  # XP, tower, boss battles, power-ups
│   │   │   ├── company_prep.py  # Company-specific interview prep
│   │   │   ├── coding.py        # Coding challenges
│   │   │   ├── compiler.py      # Piston API code execution
│   │   │   ├── system_design.py # System design interview practice
│   │   │   ├── salary.py        # Salary benchmark and comparison
│   │   │   ├── cover_letter.py  # Cover letter generation
│   │   │   ├── daily_challenge.py # Daily challenges with leaderboards
│   │   │   ├── community.py     # Study groups & discussions
│   │   │   ├── adaptive_learning.py # Adaptive learning paths
│   │   │   ├── predictor.py     # Interview prediction engine
│   │   │   ├── readiness.py     # Interview readiness scoring
│   │   │   ├── ai_debugger.py   # AI-powered code debugging
│   │   │   ├── analytics.py     # User analytics
│   │   │   ├── analytics_admin.py # Admin analytics dashboard
│   │   │   ├── invoices.py      # Invoice management
│   │   │   └── ... (60+ more route files)
│   │   ├── services/            # 82 service files
│   │   │   ├── ai.py            # ALL AI prompts + parse_json() + retry
│   │   │   ├── ai_core.py       # Core AI utilities
│   │   │   ├── ai_interview.py  # Interview-specific AI
│   │   │   ├── ai_resume.py     # Resume-specific AI
│   │   │   ├── ai_behavioral.py # Behavioral interview AI
│   │   │   ├── ai_coding.py     # Coding challenge AI
│   │   │   ├── ai_feedback.py   # AI-powered answer feedback
│   │   │   ├── ai_cover_letter.py # Cover letter AI
│   │   │   ├── ai_project.py    # Project generation AI
│   │   │   ├── ai_salary.py     # Salary analysis AI
│   │   │   ├── ai_system_design.py # System design AI
│   │   │   ├── ai_aptitude.py   # Aptitude test AI
│   │   │   ├── code_executor.py # Piston API code execution engine
│   │   │   ├── cache.py         # Unified cache (Redis → InMemory fallback)
│   │   │   ├── circuit_breaker.py # Async CircuitBreaker for AI/compiler
│   │   │   ├── resilience.py    # Unified retry + circuit breaker wrapper
│   │   │   ├── gamification.py  # XP, levels, streaks, badges, tower, bosses
│   │   │   ├── usage.py         # Monthly/daily usage tracking & limits
│   │   │   ├── question_store.py # File-based question bank loader
│   │   │   ├── feature_flags.py # Feature flag system
│   │   │   ├── invoice.py       # Invoice management
│   │   │   ├── migrations.py    # Schema migration system
│   │   │   ├── resume_parser.py # PyMuPDF PDF text extraction
│   │   │   ├── export.py        # DOCX + PDF export (ATS-safe)
│   │   │   ├── ats_semantic.py  # Semantic ATS scoring
│   │   │   ├── ats_enhanced.py  # Enhanced ATS keyword scoring
│   │   │   ├── resume_engine.py # Resume content generation
│   │   │   ├── behavioral_engine.py # Behavioral interview evaluation
│   │   │   ├── behavioral_enhanced.py # Enhanced STAR method evaluation
│   │   │   ├── placement_engine.py # Placement test engine
│   │   │   ├── coding_engine.py # Coding challenge engine
│   │   │   ├── code_tracer.py   # Code execution tracing
│   │   │   ├── skill_assessment.py # DSA skill graph assessment
│   │   │   ├── smart_prompts.py # Optimized AI prompts
│   │   │   ├── anti_plagiarism.py # Plagiarism detection
│   │   │   ├── free_ats_tool.py # Free ATS analysis tool
│   │   │   ├── real_ats.py      # Real ATS compatibility scoring
│   │   │   ├── application_tracker.py # Job application tracking
│   │   │   ├── career_profile.py # Career profile management
│   │   │   ├── social.py        # Social features
│   │   │   ├── student_features.py # Student-specific features
│   │   │   ├── trial.py         # Feature trials
│   │   │   ├── student_discount.py # Student discounts
│   │   │   ├── enterprise.py    # Enterprise plan features
│   │   │   ├── monetization.py  # Monetization logic
│   │   │   ├── revenue.py       # Revenue tracking
│   │   │   ├── coupon.py        # Coupon management
│   │   │   ├── email.py         # Email service
│   │   │   ├── health_checker.py # Health check service
│   │   │   ├── docker_sandbox.py # Docker sandbox for code execution
│   │   │   ├── local_sandbox.py # Local sandbox fallback
│   │   │   ├── spaced_repetition.py # Spaced repetition learning
│   │   │   ├── quest_engine.py  # Quest system engine
│   │   │   ├── job_readiness.py # Job readiness scoring
│   │   │   ├── audit_log.py     # Audit logging
│   │   │   ├── websocket_manager.py # WebSocket connections
│   │   │   └── ... (40+ more service files)
│   │   └── middleware/
│   │       ├── auth.py          # JWT creation/verification, httpOnly cookie
│   │       ├── rate_limiter.py  # IP rate limiting + account lockout
│   │       ├── tier_middleware.py # Tier-based feature gating
│   │       ├── duplicate_guard.py # Duplicate request prevention
│   │       ├── logging.py       # Request logging
│   │       └── __init__.py
│   ├── app/
│   │   ├── data/                # Data files (curriculum, questions, etc.)
│   │   ├── utils/               # Utility modules
│   │   └── ...
│   ├── scripts/                 # Seed/fix/test/utility scripts (consolidated from root)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Router + ErrorBoundary + 90+ lazy pages
│   │   ├── main.tsx             # ReactDOM entry
│   │   ├── index.css            # Tailwind base + custom animations
│   │   ├── pages/               # 91 page files (lazy-loaded)
│   │   │   ├── Landing.tsx      # Hero, features, pricing, CTA
│   │   │   ├── Dashboard.tsx    # Stats, usage, quick actions
│   │   │   ├── Interview.tsx    # Role/company selection
│   │   │   ├── InterviewSession.tsx # Live interview with feedback
│   │   │   ├── InterviewBooking.tsx # Mock interview scheduling
│   │   │   ├── ResumeBuilder.tsx # Upload or generate resume
│   │   │   ├── ATSOptimizer.tsx # 3-step ATS optimization
│   │   │   ├── AptitudeTest.tsx # Category select → timed test
│   │   │   ├── CoverLetter.tsx  # Cover letter + LinkedIn generator
│   │   │   ├── SalaryNegotiation.tsx # AI negotiation coaching
│   │   │   ├── SalaryBenchmark.tsx # Market rate data
│   │   │   ├── SystemDesign.tsx # System design practice
│   │   │   ├── CompanyPrep.tsx  # Company-specific prep
│   │   │   ├── CodingChallenge.tsx # Timed coding challenges
│   │   │   ├── Compiler.tsx     # Monaco editor with Piston
│   │   │   ├── SolveProblem.tsx # LeetCode-style two-column flow
│   │   │   ├── QuestionBank.tsx # Browse/search problems
│   │   │   ├── PracticeMode.tsx # Individual problem solving
│   │   │   ├── DailyChallenge.tsx # Daily adaptive challenge
│   │   │   ├── TowerDashboard.tsx # Gamification tower view
│   │   │   ├── MockOA.tsx       # Mock online assessment
│   │   │   ├── AIMentor.tsx     # AI mentor chat
│   │   │   ├── LearningHub.tsx  # Learning paths hub
│   │   │   ├── LanguageJourney.tsx # Language learning paths
│   │   │   ├── LessonView.tsx   # Individual lesson viewer
│   │   │   ├── LearningModules.tsx # Duolingo-style lessons
│   │   │   ├── ProjectGenerator.tsx # AI project generation
│   │   │   ├── DSAFingerprint.tsx # DSA skill assessment
│   │   │   ├── DSAVisualizer.tsx # Algorithm visualizations
│   │   │   ├── AdminDashboard.tsx # Admin analytics
│   │   │   ├── Community.tsx    # Community hub
│   │   │   ├── MonthlyContests.tsx # Contest page
│   │   │   ├── OnboardingQuest.tsx # Guided onboarding
│   │   │   ├── PersonalDashboard.tsx # User personal dashboard
│   │   │   ├── AdaptivePath.tsx # AI learning path
│   │   │   ├── IndianPlacement.tsx # Indian market prep
│   │   │   └── ... (60+ more pages)
│   │   ├── components/          # 94 component files
│   │   │   ├── Navbar.tsx       # Auth-aware navigation
│   │   │   ├── Footer.tsx
│   │   │   ├── ErrorBoundary.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   ├── CelebrationOverlay.tsx
│   │   │   ├── ActivityHeatmap.tsx
│   │   │   ├── XPBar.tsx
│   │   │   ├── XPPopup.tsx
│   │   │   ├── Toast.tsx
│   │   │   ├── Skeleton.tsx
│   │   │   ├── SpaceBackground.tsx
│   │   │   ├── ChallengePackCard.tsx
│   │   │   ├── ScoreRing.tsx
│   │   │   ├── StreakConstellation.tsx
│   │   │   ├── BadgeCeremony.tsx
│   │   │   ├── LevelUpCelebration.tsx
│   │   │   ├── JuiceProvider.tsx # Gamification juice system
│   │   │   ├── CookieBanner.tsx
│   │   │   ├── PwaInstallPrompt.tsx
│   │   │   ├── NeuralNetworkBackground.tsx
│   │   │   ├── ui/              # Button, Input, Card, Modal, Spinner, Skeleton
│   │   │   ├── tower/           # Tower/gamification stubs (minimal)
│   │   │   ├── motion/          # Framer Motion animations
│   │   │   ├── emblems/         # Badge/emblem system
│   │   │   ├── interactive/     # Interactive components
│   │   │   └── learning/        # Learning module components
│   │   ├── pages/lazy.ts        # All lazy imports
│   │   ├── services/api/        # 39 API module files
│   │   │   ├── index.ts         # Aggregated API object
│   │   │   ├── auth.ts, interview.ts, resume.ts, billing.ts, etc.
│   │   ├── store/
│   │   │   └── authStore.ts     # Zustand auth state
│   │   ├── hooks/               # Custom hooks
│   │   └── utils/               # Helpers
│   ├── package.json             # placementpro-frontend
│   ├── vite.config.ts           # Dev server + /api proxy
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vercel.json
├── .github/workflows/ci.yml    # CI: typecheck + build
├── Dockerfile                   # Python 3.12
├── FUTURE.md                    # $1M ARR scaling roadmap
└── README.md
```

---

## Key API Contracts

### Auth
- `POST /api/auth/register` → `{ email, password, name }` → `{ token, user }` + httpOnly cookie
- `POST /api/auth/login` → `{ email, password }` → `{ token, user }` + httpOnly cookie
- `POST /api/auth/logout` → clears httpOnly cookie
- `GET /api/auth/me` → cookie-based auth → `{ id, email, name, plan, usage, is_admin }`
- `POST /api/auth/forgot-password` → sends reset token
- `POST /api/auth/reset-password` → resets password with token
- `POST /api/auth/update-profile` → updates name/email
- `POST /api/auth/change-password` → changes password
- `GET /api/auth/onboarding-status` → checks onboarding completion
- `POST /api/auth/onboarding-complete` → completes onboarding

### Interview
- `POST /api/interview/start` → `{ job_role, company, interview_type, difficulty }`
- `POST /api/interview/answer` → `{ interview_id, question, answer, time_taken, is_follow_up }`
- `GET /api/interview/{id}/result` → detailed results with score breakdown
- `GET /api/interview/history` → 20 most recent interviews

### Resume
- `POST /api/resume/upload` → multipart PDF → analysis
- `POST /api/resume/generate` → AI-generated resume from details
- `POST /api/resume/optimize` → ATS optimization against JD
- `POST /api/resume/semantic-score` → semantic ATS scoring
- `GET /api/resume/{id}/export/docx` → binary DOCX
- `GET /api/resume/{id}/export/pdf` → binary PDF
- `GET /api/resume/history` → 20 most recent resumes

### Aptitude Test
- `GET /api/aptitude/categories` → available categories
- `POST /api/aptitude/start` → start a test
- `POST /api/aptitude/answer` → submit answer
- `POST /api/aptitude/{test_id}/complete` → finalize test
- `GET /api/aptitude/history` → past tests

### Question Bank (LeetCode Flow)
- `GET /api/questions/browse` → paginated, filterable question list
- `GET /api/questions/random` → random question with filters
- `GET /api/questions/{id}` → full problem detail
- `GET /api/questions/{id}/solution` → progressive hints with hint_level
- `GET /api/questions/{id}/solved` → check if solved
- `POST /api/questions/{id}/submit` → submit code, run hidden test cases
- `POST /api/questions/{id}/answer` → text answer with AI feedback
- `GET /api/questions/stats` → user attempt statistics
- `GET /api/questions/recent` → recent answers
- `GET /api/questions/filters` → available companies, roles, topics, difficulties
- `POST /api/questions/submit` → submit new question for curation
- `POST /api/questions/upvote` → upvote/downvote

### Gamification
- `GET /api/gamification/profile` → full gamification profile
- `POST /api/gamification/record` → record practice activity
- `GET /api/gamification/leaderboard` → global leaderboard
- `GET /api/gamification/badges` → available badges
- `GET /api/gamification/skills` → skill graph across categories
- `GET /api/gamification/skills/weak` → weak areas
- `GET /api/gamification/skills/readiness` → interview readiness score
- `GET /api/gamification/tower` → tower progression
- `GET /api/gamification/tower/boss/{level}` → boss battle details

### Coding
- `GET /api/coding/topics` → available topics
- `POST /api/coding/start` → start a challenge
- `POST /api/coding/submit` → submit solution
- `GET /api/coding/{id}/solution` → solution with hints
- `GET /api/coding/history` → past challenges

### Compiler
- `POST /api/compiler/execute` → execute code via Piston API
- `POST /api/compiler/execute-test-cases` → run test cases
- `GET /api/compiler/languages` → supported languages

### Company Prep
- `GET /api/company/companies` → 53+ company profiles
- `POST /api/company/behavioral` → company-specific behavioral Q
- `POST /api/company/tips` → company-specific interview tips
- `GET /api/company/{company}/guide` → full company guide

### Learning
- `GET /api/learning/modules` → learning modules
- `GET /api/learning/progress` → user learning progress
- `GET /api/language-paths` → 7 language learning paths

### Analytics
- `POST /api/analytics/track` → track page views and events
- `GET /api/analytics/admin` → admin dashboard metrics

### Profile & Stats
- `GET /api/profile/stats` → user profile with stats
- `PUT /api/profile/integrations` → update GitHub/LeetCode usernames

### Salary
- `POST /api/salary/benchmark` → market rate data
- `POST /api/salary/compare` → compare job offers
- `POST /api/salary/save` → save an offer
- `GET /api/salary/history` → saved offers

### Billing (PayPal)
- `POST /api/billing/checkout` → PayPal approval link
- `POST /api/billing/checkout/lifetime` → lifetime plan checkout
- `POST /api/billing/capture` → capture payment after approval
- `POST /api/billing/webhook` → PayPal webhook handler
- `GET /api/billing/status` → current plan and usage

### Practice & Community
- `GET /api/practice/sessions` → practice session history
- `GET /api/community/posts` → community discussions

---

## Security Features
- **httpOnly cookies** — JWT never touches JavaScript (XSS-proof)
- **Rate limiting** — 60 req/min per IP (configurable), Redis-backed when available
- **Login lockout** — 5 failed attempts → 15 min lockout per email
- **Duplicate request guard** — Blocks double-clicks within 2-second window
- **CORS locked** — Specific origins, credentials enabled
- **CSP headers** — Blocks inline scripts, restricts frame loading
- **Security headers** — X-Content-Type-Options, X-Frame-Options, HSTS, Referrer-Policy
- **Request ID tracing** — Every request gets a correlation ID
- **Structured logging** — JSON logs with sensitive data redaction
- **PDF validation** — Magic bytes check (`%PDF-`) before processing
- **Password strength** — Min 8 chars, requires number + special character
- **Tier gating** — Free/pro/lifetime feature limits enforced
- **Secrets hygiene** — `.env` tracked in `.gitignore` via `*.env` + `.env.*` patterns; only `.env.example` committed

## AI Reliability
- **In-memory + Redis caching** — AI responses cached for 1 hour
- **Fallback models** — Primary: Gemini Flash → 3 fallbacks (Llama, Phi-3, DeepSeek)
- **Circuit breaker** — Auto-switches to fallback if primary fails 5+ times
- **Retry logic** — 3 retries with exponential backoff
- **Async I/O** — All AI calls via `httpx.AsyncClient` with connection pooling

## Gamification
- **XP system** — Earn XP for every activity with daily bonuses
- **Level progression** — Levels 1-100 with 50+ titles (Hatchling → God of Code)
- **Streaks** — Daily practice streaks with multiplier bonuses
- **Badges** — 30+ achievement badges
- **Tower system** — Boss battles at levels 10, 20, 30... 100
- **Power-ups** — Extra time, hint reveal, retry, double XP, skip boss, show answer
- **Daily challenges** — Adaptive missions with leaderboards

## Free Tier Limits (Monthly/Daily)
| Feature | Free Limit | Pro/Lifetime |
|---------|-----------|-------------|
| Interviews/month | 3 | Unlimited |
| Resume reviews/month | 3 | Unlimited |
| Aptitude tests/month | 5 | Unlimited |
| Cover letters/month | 3 | Unlimited |
| Company mocks/month | 1 | Unlimited |
| Predictor uses/month | 3 | Unlimited |
| Question bank/month | 5 | Unlimited |
| Compiler runs/day | 20 | Unlimited |
| AI questions/day | 5 | Unlimited |
| Problems solved/day | 10 | Unlimited |
| Mock interviews/month | 1 | Unlimited |
| Interview bookings/month | 3 | Unlimited |

---

## Verified Landing Page Background Assets

The hero background on `frontend/src/pages/Landing.tsx` must use a **confirmed-valid Unsplash photo ID** (a broken ID renders as white/cream). All verified IDs below return HTTP 200. A neutral gradient + base-color fallback is layered behind the image so it never shows plain white.

Verified-working photo IDs (use with `https://images.unsplash.com/photo-<ID>?w=4096&q=80&auto=format&fit=crop&fm=jpg`):
- `1534067783941-51c9c23ecefd` — **current hero: user-approved "el perfecto" sakura image** (valid, 200). Set at `w=7680` with Imgix `bri=12&sat=8`, pink gradient fallback `#fbe4ec`.
- `1551632811-561732d1e306` — mountain/landscape candidate (valid, 200).
- `1534067783941-51c9c23ecefd` — sakura candidate, archived (valid, 200).
- `1743309979269-af5d46d0c390` — original sakura-trees wallpaper (user-confirmed "sakura trees").
- `1520763185298-1b434c919102` — sakura candidate (valid, 200).
- `1542273917363-3b1817f69a2d` — sakura candidate (valid, 200).
- `1518998053901-5348d3961a04` — sakura candidate (valid, 200).
- `1505691938895-1758d7feb511` — sakura candidate (valid, 200).
- `1534067783941-51c9c23ecefd` — sakura candidate (valid, 200).
- `1522383225653-ed111181a951` — cherry-blossom tree candidate (valid, 200).
- `1490750967868-88aa4486c946` — pink flower field (valid, 200; not trees).
- `1441974231531-c6227db76b6e` — forest path, green trees (valid, 200; not sakura).
- `1472396961693-142e6e269027` — autumn trees (valid, 200).

Known-broken ID to avoid: `15087040-efdd9b34cpho` (404 — previously caused the white screen).

Landing hero composition rules (locked): ONE navbar only — the global `Navbar` is hidden on `/` in `App.tsx` (line ~809: `{location.pathname !== "/" && <Navbar />}`), and `Landing.tsx` renders its own minimal `BountyCode / Login / Get started` nav over the photo. No "You are here" marker, no character, no glassmorphism card. Headline: "From your first line of code / to your first offer." with **"first offer." in gold (`#D4A843`)**, not rainbow. Keep the Diagnose → Learn → Practice → Get Hired strip (expedition path with arrows). Soft radial halo behind the headline only. Brand identity: **nostalgic spring adventure** — sakura communicates growth, calm focus, and a fresh start.

---

## Known Issues (Fix Priority)

### P0 — CRITICAL (Fixed)
- [x] ~~`_check_circuit_breaker()` called without `await` in `chat_completion()`~~ → Fixed
- [x] ~~`FALLBACK_MODELS` includes primary model redundantly~~ → Fixed
- [x] ~~`circuit_breaker` undefined in `chat_completion()` (should be `ai_breaker`)~~ → Fixed
- [x] ~~`call_with_resilience()` uses dict `.get()` on CircuitBreaker object~~ → Fixed

### P1 — HIGH (Remaining)
- [ ] `ai.py` is large — violates SRP, should be split by domain (partially done with ai_*.py modules)
- [ ] Frontend is JavaScript/TSX — no strict TypeScript typing on all components

### P2 — MEDIUM (Remaining)
- [ ] No API versioning at the app level — individual route files use `/api/v1/` prefix
- [ ] No connection pooling config for Redis if used in production
- [ ] `_LazyCollection` proxy uses `__getattr__` magic which can mask typos

### P3 — LOW (Remaining)
- [ ] No email verification on signup
- [ ] No audit log for admin actions
- [ ] No health check dashboard UI
- [ ] Monaco Editor not fully integrated in all flows

---

## Development Commands

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env           # Fill in values
uvicorn app.main:app --reload  # Hot reload on port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                    # Vite dev server on port 5173
npm run build                  # Production build
npm run typecheck              # TypeScript type checking
npm run smoke                  # Smoke test (11 checks): pages render w/o crash + auth + telemetry
```

---

## Recent Improvements (August 2026)

### Major Codebase Cleanup
- **Removed 60+ experimental/RPG features** — Deleted ~25,000 lines of dead code across backend routes, frontend pages, and API modules
- **Deleted backend routes**: guild_castle, dungeons, grand_line, steam_profile, newspaper, merchant, economy, game_events, guilds, world, skill_trees, seasons, tournaments, teams, themes, trending_challenges, shareable_achievements, career_rpg, bounty, live_events, mission_engine, hook_model, cards, scrims, showcase, referrals, big_four, chat, gd_rooms, campus_wars, campus_connect, campus_pulse, campus, college_network, cgpa_simulator, drive_tracker, peer_review, study_squads, report_card, battles, quests, goals, friends, referral, collection, journey, achievements, skill_mastery, timeline, daily_orders, invite, debug, real_features, mass_recruiter, pseudocode, rank, job_readiness, energy, mystery_box, prestige, battle_pass, wizard, lucky_wheel
- **Deleted frontend pages**: 65+ pages (Chat, GDRoom, CampusWars, CampusConnect, CampusPulse, CollegeNetwork, CGPASimulator, DriveTracker, PeerReview, StudySquads, PrepReportCard, BattleArena, Quests, GoalsPage, FriendsPage, Journey, CollectionEvents, AchievementChains, SkillMasteryPage, HealthDashboard, Referral, RetentionAdmin, ConsulsRoute, RoleSelector, InterviewTerminal, MassRecruiterExam, PseudocodeDrill, ReadinessScore, RankProfile, DiscussionsPage, BehavioralPractice, CompanyDirectory, JobReadiness, BattlePass, EnergyPage, LuckyWheel, MysteryBoxPage)
- **Deleted API modules**: 45+ modules (chat, gdRooms, campus, campusPulse, collegeNetwork, cgpa, driveTracker, peerReview, studySquads, reportCard, goals, friends, collectionEvents, achievements, referralSystem, studyTimer, massRecruiter, pseudocode, bigFour, companyDirectory, interviewChat, journey, career, battlePass, luckyWheel)
- **Cleaned cross-references**: lazy.ts, App.tsx, API index, Navbar, BottomNav, feature_flags.py, database.py, misc.ts, flatOverrides.ts, gamification.ts, authStore.ts
- **Created minimal tower stubs**: `components/tower/` with minimal implementations for TowerDashboard compatibility

### Infrastructure Fixes
- **Dockerfile**: Updated from Python 3.11 → 3.12 (matches CI)
- **CI**: Added `npm run typecheck` step before build
- **Package rename**: `bountycode-frontend` → `placementpro-frontend`
- **Scripts consolidated**: 30+ root-level scripts moved to `backend/scripts/` via `git mv`
- **.gitignore cleaned**: Added patterns for `d*.py`, `test_bank.py`, `backend/app/data/invoices/`

### Verified Builds
- **Backend**: `python -m compileall app/ -q` → passes clean
- **Frontend**: `npm run build` → ✓ built in ~42s (2108 modules transformed)

### Admin Analytics & Access Control
- **Admin analytics endpoints enabled**: Added `/api/v1/analytics/admin/geo` and `/api/v1/analytics/admin/retention` for visitor IP breakdown and new/returning user retention stats
- **Admin email access control**: Added `sridevi72901@gmail.com` to `ADMIN_EMAILS` config in `backend/app/config.py:63` — grants full admin access regardless of plan
- **`is_admin` / `role` in user payload**: Modified `backend/app/middleware/auth.py:191-198` and `backend/app/routes/auth.py:174` to compute `is_admin = plan in ("pro", "lifetime") or email in ADMIN_EMAILS` — now flows to all protected routes
- **`/api/v1/auth/me` returns admin status**: Now includes `is_admin: true` and `role: "admin"` for Pro/Lifetime/admin-email users
- **Admin dashboard verified**: `/admin` page (AdminDashboard) loads real-time stats, visitor trends, geo breakdown, retention stats for admin users

### Security & Access Control
- **Admin routes properly restricted**: All admin endpoints (`analytics_admin.py`, `admin_content.py`, `coupon.py`, `tiers.py`) check `user.get("role") == "admin" or user.get("is_admin") is True` — returns 403 for non-admin users
- **ADMIN_EMAILS bypass**: Owner email `sridevi72901@gmail.com` granted admin access via config without requiring Pro/Lifetime plan

---

## Recent Improvements (July 2026)

### Critical Bug Fixes
- **Circuit breaker `await` bug** — Fixed `_check_circuit_breaker()` called without `await` in `chat_completion()`
- **FALLBACK_MODELS redundancy** — Removed primary model from fallback list to avoid redundant retry
- **Undefined `circuit_breaker` variable** — Fixed to use `ai_breaker` (the actual import)
- **`call_with_resilience` type mismatch** — Updated to handle both `CircuitBreaker` objects and plain dicts via `_breaker_get`/`_breaker_set` helpers
- **CircuitBreaker property accessors** — Added `is_open`, `failures`, `last_failure_time` properties with setters to `CircuitBreaker` class
- **CircuitBreaker missing methods** — Added `allow_request()`, `record_failure()`, `record_success()` async methods with lock-protected state transitions
- **`asyncio.get_event_loop()` deprecation** — Replaced with `asyncio.get_running_loop()` in `resilience.py`
- **`tier_gate()` mixed concerns** — Extracted `check_tier_limit()` as a separate dependency function
- **`duplicate_guard.py` in-memory only** — Added file-based persistence to `data/duplicate_hashes.json`
- **Dead `request.js`** — Removed unused frontend API service file
- **Unused `axios` dependency** — Removed from `package.json` (frontend uses `fetch` exclusively)
- **`questions.py` too large** — Split into `questions.py` (curation routes) and `questions_solve.py` (solve/answer/code routes)
- **Missing password reset UI** — Created `ForgotPassword.jsx` and `ResetPassword.jsx` pages

### Backend Infrastructure
- **CSP Headers** — Content-Security-Policy middleware
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, etc.
- **Request ID Middleware** — X-Request-ID header for tracing
- **Duplicate Request Guard** — Prevents double-click duplicate submissions
- **Tier Middleware** — Free/pro/lifetime feature gating with monthly + daily limits
- **Structured Logging** — JSON logs with correlation IDs and sensitive data redaction
- **Request Metrics** — In-memory + MongoDB-persisted metrics with periodic flush
- **Migration System** — Decorator-based schema migration tracking
- **Redis Cache** — Unified cache with Redis → InMemory fallback

### AI Layer Improvements
- **In-memory caching** — AI responses cached for 1 hour
- **Fallback models** — 4 models with circuit breaker protection
- **Retry with exponential backoff** — 3 retries on AI API failures
- **Company-specific evaluation rubrics** — 9 company profiles in `ai.py`

### Frontend Enhancements
- **90+ lazy-loaded pages** — Code splitting reduces initial bundle
- **Gamification juice system** — XP popups, confetti, level-up animations, streak ceremonies
- **Keyboard shortcuts** — `Cmd/Ctrl+K` for search, `Escape` for modals
- **Dynamic daily missions** — Adapts based on user progress and weak areas

### Bandwidth Protection (Vercel Hobby 100 GB/mo limit)
- **Cloudinary integration** — `src/services/cloudinary.js` provides `cloudinaryImage()`, `cloudinaryVideo()`, `optimizeImage()` helpers with auto-format/auto-quality
- **Media hosting strategy:**
  - Video lessons → YouTube embeds (0 Vercel bandwidth)
  - Images/badges/logos → Cloudinary with `.webp` + `w_auto,q_auto` transforms
  - Company logos in Resume Builder → Cloudinary thumbnails (100px width)
- **No local assets in `public/`** — all visual content served via CDN

---

## Code Conventions

### Backend (Python)
- All routes use `async def` with `Depends(get_current_user)` for auth
- Pydantic models for request/response validation
- MongoDB operations via `motor` async driver
- AI calls via `httpx.AsyncClient` to OpenRouter (with retry)
- PayPal calls via `httpx.AsyncClient` (fully async)
- JSON parsing with fallback in `parse_json()`
- Errors raised as `HTTPException(status_code=..., detail=...)`
- Cookies set via `set_auth_cookie()` / `clear_auth_cookie()` in middleware
- Circuit breaker and resilience patterns for all external API calls
- Structured JSON logging with correlation IDs
- Route auto-discovery in `main.py` (scans `backend/app/routes/` — delete file to remove route)

### Frontend (React + TypeScript)
- Functional components with hooks
- TypeScript (`.tsx` / `.ts`) throughout
- Zustand for global state (auth only)
- `services/api/index.ts` aggregated API object for all backend calls
- Tailwind CSS for styling (no component library)
- `ProtectedRoute` wrapper for authenticated pages
- `ErrorBoundary` wraps entire app
- `React.lazy()` for all page components via `pages/lazy.ts` (code splitting)
- Consistent card-based layouts
- Gamification juice system for celebrations (confetti, XP popups, sound)

### File Organization
- Route files: `backend/app/routes/<feature>.py` (one per feature, auto-discovered)
- Service files: `backend/app/services/<domain>.py` (business logic)
- Route prefixes: `/api/<feature>` (no version prefix yet)
- AI prompts: Split across `ai.py`, `ai_interview.py`, `ai_resume.py`, `ai_behavioral.py`, etc.
- Scripts: `backend/scripts/` (consolidated from root-level `seed_*.py`, `fix_*.py`, etc.)

---

## Revenue Projections

| Month | Free Users | Paid Users | MRR |
|-------|-----------|------------|-----|
| 1 | 200 | 20 | $180 |
| 3 | 1,000 | 80 | $720 |
| 6 | 3,000 | 200 | $1,800 |
| 12 | 10,000 | 500 | $4,500 |

+ Lifetime purchases: ~$2K/mo additional

**Path to $1M ARR:** See `FUTURE.md` for detailed scaling roadmap.
