# AGENTS.md — PlacementPro

## Project Overview

**PlacementPro** is an AI-powered placement preparation platform targeting job seekers (students + experienced professionals). It offers **15+ core features**:

### Core Features
1. **AI Interviewer** — Mock interviews with AI that asks questions, evaluates answers, and gives feedback
2. **System Design Practice** — System design interviews with AI evaluation of architecture, scalability, and trade-offs
3. **Coding Challenges** — Timed coding problems with solutions and follow-up challenges
4. **LeetCode-Style Compiler** — Full code execution environment with Monaco Editor, test cases, and hidden judge
5. **Company-Specific Prep** — FAANG interview guides, leadership principles, and behavioral questions
6. **Resume Builder/Analyzer** — Upload existing resume or generate new one with AI
7. **ATS Score Optimizer** — Match resume to job descriptions, identify missing keywords, rewrite for ATS compatibility
8. **Aptitude Test Practice** — Quantitative, logical, verbal, technical MCQs for campus placements
9. **Cover Letter & LinkedIn** — AI-generated cover letters and LinkedIn About sections
10. **Salary Benchmark** — Market rate data, percentile breakdowns, and company comparisons
11. **Salary Negotiation Coach** — AI-powered tips and scripts for negotiating offers

### Enhanced Features (Student-Requested)
12. **Resume Bullet Improver** — Transform weak bullets into powerful, ATS-friendly statements
13. **ATS Formatting Checklist** — Analyze resume for common ATS pitfalls
14. **Resume Tailoring** — Auto-tailor resume for specific job descriptions
15. **Company-Specific Coding** — Coding challenges in the style of Google, Amazon, TCS, etc.
16. **Mock Interviewer Feedback** — Real-time code evaluation like a live interviewer
17. **STAR Method Evaluation** — Behavioral answers scored on Situation, Task, Action, Result
18. **Progressive Hints** — Get unstuck without seeing the full solution
19. **Code Concept Explanations** — Learn concepts at beginner, intermediate, or expert level
20. **Profile Sidebar** — Avatar, solved count, streak, skill graph, badges, activity heatmap, integrations
21. **Problem Solving Flow** — `/solve/:id` with left-panel problem description + right-panel Monaco compiler

**Target users:** 
- **Indian students:** Campus placement preparation (TCS, Infosys, Wipro, etc.) with aptitude tests
- **US/Global job seekers:** Behavioral interviews, resume optimization, salary negotiation, system design
- **Professionals:** Career changers, job switchers, FAANG aspirants

**Business model:** Freemium (Free + Pro $9/mo + Lifetime $39 one-time). Free tier resets monthly:
- 3 interviews/month + 3 resume reviews/month + 5 aptitude tests/month + 3 cover letters/month

**Built with:** MimoCode (AI coding assistant). Includes a LeetCode-style coding compiler with Monaco Editor and Piston API execution engine.

---

## Advanced Features (World-Class)

### AI Reliability
- **In-memory caching** — AI responses cached for 1 hour (reduces cost, improves speed)
- **Fallback models** — Primary: Gemini Flash → Fallback: Llama 3.1, Phi-3 Mini
- **Circuit breaker** — Auto-switches to fallback if primary fails 5+ times
- **Retry logic** — 3 retries with exponential backoff

### Gamification
- **XP system** — Earn XP for every activity (interviews, coding, aptitude)
- **Levels** — Level up based on XP (exponential curve)
- **Streaks** — Daily practice streaks with rewards
- **Badges** — 20+ achievement badges (First Steps, Interview Master, ATS Master, etc.)
- **Leaderboard** — Compete with other users

### Skill Assessment
- **Skill graph** — Track proficiency across 5 categories (DSA, System Design, Behavioral, Aptitude, Resume)
- **Weak area detection** — Identify and prioritize weak skills
- **Readiness score** — Company-specific interview readiness percentage
- **Personalized recommendations** — AI-driven improvement suggestions

### Hook Model (Addictive Mechanics)
- **Mystery boxes** — Random rewards after completing activities (XP, streak freeze, badges)
- **Double XP triggers** — Variable rewards for perfect scores, streaks, early birds
- **Streak freeze** — Protect streaks when life happens
- **Savage feedback** — Engaging, memorable feedback that's fun to read
- **Daily bonuses** — Comeback rewards for returning users
- **Social proof** — Leaderboards, study groups, contests

### Social Features
- **Study groups** — Form prep squads with friends
- **Monthly contests** — Compete for prizes and bragging rights
- **Peer accountability** — See group members' progress

### Free Practice Hook
- **Quick interview** — 3-question practice session (no quota consumed)
- **Quick evaluate** — Instant feedback on answers
- **Upgrade prompt** — Clear path to Pro for full features

---

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | React 18 + Vite 5 + Tailwind 3 | SPA, deployed to Vercel |
| Backend | FastAPI (Python 3.11+) | Async, deployed to Render |
| Database | MongoDB Atlas (free tier, 512MB) | Motor async driver |
| AI | OpenRouter → Gemini 2.0 Flash | Cheapest model (~$0.07/1M tokens) |
| Auth | JWT (python-jose + passlib/bcrypt) | 7-day expiry, httpOnly cookie |
| Payments | PayPal REST API | Checkout orders + webhooks |
| PDF parsing | PyMuPDF (fitz) | Extract text from uploaded PDFs |
| DOCX export | python-docx | ATS-safe single-column format |
| PDF export | PyMuPDF | ATS-safe formatting |
| Code Execution | Piston API | Dockerized sandbox, 11+ languages, <500ms cold start |
| Editor | Monaco Editor | VS Code-like editing experience in browser |
| Animations | Framer Motion | Page transitions, confetti, micro-interactions |
| Icons | Lucide React | Consistent icon set across UI |

**Total hosting cost: $0 upfront** (all free tiers). AI costs start at ~$5/mo once users arrive.

---

## Project Structure

```
placementpro/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, lifespan, rate limiter, routes
│   │   ├── config.py            # Pydantic Settings (all env vars)
│   │   ├── database.py          # Motor client, collection refs, init_db()
│   │   ├── models/
│   │   │   ├── user.py          # UserCreate, UserLogin, UserResponse, UserInDB
│   │   │   ├── interview.py     # StartInterview, SubmitAnswer, QARecord
│   │   │   ├── resume.py        # GenerateResume, OptimizeRequest
│   │   │   └── aptitude.py      # AptitudeQuestion, AptitudeTest, StartAptitudeTest
│   │   ├── routes/
│   │   │   ├── auth.py          # POST register/login/logout, GET me (rate-limited)
│   │   │   ├── interview.py     # POST start/answer, GET result/history
│   │   │   ├── resume.py        # POST upload/generate/optimize, GET export/history
│   │   │   ├── billing.py       # POST checkout/lifetime/capture, webhook, GET status (PayPal)
│   │   │   ├── aptitude.py      # POST start/answer/complete, GET categories/history
│   │   │   ├── cover_letter.py  # POST cover-letter/linkedin-about/salary-negotiation
│   │   │   ├── compiler.py      # POST /api/compiler/execute, /execute-test-cases, /languages
│   │   │   ├── questions.py     # GET /api/questions/{id}, /browse, /submit, /solved, stats, recent
│   │   │   └── profile_stats.py # GET /api/profile/stats, PUT /api/profile/integrations
│   │   ├── services/
│   │   │   ├── ai.py            # All OpenRouter AI prompts + parse_json() + retry
│   │   │   ├── resume_parser.py # PyMuPDF PDF text extraction
│   │   │   ├── export.py        # DOCX + PDF export (ATS-safe)
│   │   │   ├── code_executor.py # Piston API code execution engine
│   │   │   ├── profile_stats.py # Profile sidebar aggregation + integrations
│   │   │   └── usage.py         # Monthly reset logic, feature limits, usage stats
│   │   └── middleware/
│   │       ├── auth.py          # JWT creation/verification, httpOnly cookie, get_current_user
│   │       └── rate_limiter.py  # IP rate limiting + account lockout
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Router + ErrorBoundary + route definitions
│   │   ├── main.jsx             # ReactDOM entry
│   │   ├── index.css            # Tailwind base + custom classes
│   │   ├── pages/
│   │   │   ├── Landing.jsx      # Hero, features, how-it-works, pricing, CTA
│   │   │   ├── Login.jsx        # Login form
│   │   │   ├── Register.jsx     # Registration form
│   │   │   ├── Dashboard.jsx    # Stats, usage tracking, quick actions, upgrade CTA
│   │   │   ├── Interview.jsx    # Role selection grid
│   │   │   ├── InterviewSession.jsx # Live interview with feedback
│   │   │   ├── ResumeBuilder.jsx    # Upload or generate resume
│   │   │   ├── ATSOptimizer.jsx     # 3-step: upload → paste JD → optimize
│   │   │   ├── AptitudeTest.jsx     # Category select → timed test → results
│   │   │   ├── CoverLetter.jsx      # Cover letter + LinkedIn About generator
│   │   │   ├── SalaryNegotiation.jsx # AI negotiation coaching
│   │   │   ├── Pricing.jsx      # Pricing cards with PayPal checkout
│   │   │   ├── Compiler.jsx     # Monaco-ready compiler with Piston execution
│   │   │   ├── SolveProblem.jsx # Two-column: ProblemDetail + Compiler
│   │   │   └── NotFound.jsx     # 404 page
│   │   ├── components/
│   │   │   ├── Navbar.jsx       # Auth-aware navigation + mobile menu
│   │   │   ├── Footer.jsx
│   │   │   ├── ErrorBoundary.jsx # Catches React crashes, shows recovery UI
│   │   │   ├── ProtectedRoute.jsx # Auth guard (redirects to /login)
│   │   │   ├── ProblemDetail.jsx # Left-panel problem description for LeetCode flow
│   │   │   ├── ProfileSidebar.jsx # User stats, streak, badges, heatmap, integrations
│   │   │   ├── CelebrationOverlay.jsx # Confetti on problem solve / achievements
│   │   │   ├── ActivityHeatmap.jsx # GitHub-style contribution calendar
│   │   │   └── ui/              # Button, Input, Card, Modal, Spinner, Skeleton
│   │   ├── services/
│   │   │   └── api.js           # All API calls (cookie-based auth, credentials: include)
│   │   ├── store/
│   │   │   └── authStore.js     # Zustand auth state (no localStorage, cookie-only)
│   │   ├── hooks/               # (empty — add custom hooks here)
│   │   └── utils/               # (empty — add helpers here)
│   ├── package.json
│   ├── vite.config.js           # Dev server + /api proxy to backend
│   ├── tailwind.config.js
│   └── postcss.config.js
├── FUTURE.md                    # $1M ARR scaling roadmap
└── README.md
```

---

## Key API Contracts

### Auth
- `POST /api/auth/register` → `{ email, password, name }` → `{ token, user }` + httpOnly cookie
- `POST /api/auth/login` → `{ email, password }` → `{ token, user }` + httpOnly cookie
- `POST /api/auth/logout` → clears httpOnly cookie
- `GET /api/auth/me` → cookie-based auth → `{ id, email, name, plan, usage }`

### Interview
- `POST /api/interview/start` → `{ job_role }` → `{ interview_id, question, question_type, tips }`
- `POST /api/interview/answer` → `{ interview_id, question, answer }` → `{ feedback, next_question, current_score, questions_answered, finished }`
- `GET /api/interview/{id}/result` → `{ interview_id, job_role, overall_score, questions, total_questions }`
- `GET /api/interview/history` → `{ interviews: [...] }`

### Resume
- `POST /api/resume/upload` → multipart `file` → `{ resume_id, text, analysis }`
- `POST /api/resume/generate` → `{ name, email, target_role, experience, education, skills }` → `{ resume_id, content }`
- `POST /api/resume/optimize` → `{ resume_id, job_description }` → `{ ats_score, missing_keywords, present_keywords, optimized_resume, changes_made }`
- `GET /api/resume/{id}/export/docx` → binary DOCX
- `GET /api/resume/{id}/export/pdf` → binary PDF
- `GET /api/resume/history` → `{ resumes: [...] }`

### Aptitude Test
- `GET /api/aptitude/categories` → `{ categories: [{ id, name, description }] }`
- `POST /api/aptitude/start` → `{ category, difficulty, question_count }` → `{ test_id, questions, total_questions }`
- `POST /api/aptitude/answer` → `{ test_id, question_index, answer }` → `{ is_correct, correct_answer, explanation }`
- `POST /api/aptitude/{test_id}/complete` → `{ test_id, score, percentage, weak_areas, strong_areas, questions }`
- `GET /api/aptitude/history` → `{ tests: [...] }`

### Cover Letter & LinkedIn
- `POST /api/tools/cover-letter` → `{ resume_id, job_description, company_name }` → `{ cover_letter_id, cover_letter }`
- `POST /api/tools/linkedin-about` → `{ resume_id, target_role }` → `{ linkedin_about }`
- `POST /api/tools/salary-negotiation` → `{ job_title, offered_salary, location, years_experience, company_size, benefits }` → `{ market_research, negotiation_points, scripts, dos, donts }`
- `GET /api/tools/cover-letter/history` → `{ cover_letters: [...] }`

### System Design
- `POST /api/system-design/start` → `{ difficulty, topic }` → `{ session_id, question, hints, expected_components }`
- `POST /api/system-design/answer` → `{ session_id, question, answer, diagram_description }` → `{ feedback, score }`
- `GET /api/system-design/{id}/result` → `{ session_id, topic, overall_score, questions }`
- `GET /api/system-design/history` → `{ sessions: [...] }`

### Company-Specific Prep
- `GET /api/company/companies` → `{ companies: [{ id, name, leadership_principles, interview_rounds, focus_areas }] }`
- `POST /api/company/behavioral` → `{ company, role }` → `{ company, role, question: { question, category, star_framework, red_flags } }`
- `POST /api/company/tips` → `{ company, role, round_type }` → `{ tips: { company_overview, key_focus_areas, common_questions } }`
- `GET /api/company/{company}/guide` → `{ company, interview_process, focus_areas, leadership_principles, tips }`

### Coding Challenges
- `GET /api/coding/topics` → `{ topics: [{ id, name }] }`
- `POST /api/coding/start` → `{ difficulty, topic, language }` → `{ challenge_id, title, description, examples, constraints, hints, time_limit }`
- `POST /api/coding/submit` → `{ challenge_id, code, time_taken }` → `{ status }`
- `GET /api/coding/{id}/solution` → `{ title, test_cases, hints, follow_up, user_code }`
- `GET /api/coding/history` → `{ challenges: [...] }`

### Compiler
- `POST /api/compiler/execute` → `{ code, language, stdin, timeout }` → `{ stdout, stderr, execution_time, success }`
- `POST /api/compiler/execute-test-cases` → `{ code, language, test_cases, timeout }` → `{ passed, total, results, all_passed }`
- `GET /api/compiler/languages` → `{ languages: [{ id, name, version }] }`

### Question Bank (LeetCode Flow)
- `GET /api/questions/browse` → `{ questions, total, page, pages }` with filters
- `GET /api/questions/{id}` → full problem detail with `statement`, `examples`, `constraints`, `visible_test_cases`, `topics`, `companies`
- `GET /api/questions/{id}/solved` → `{ solved: boolean }`
- `POST /api/questions/{id}/submit` → runs hidden test cases, returns `{ all_passed, passed_count, total_count, score, xp_gained, solved }`
- `GET /api/questions/stats` → user attempt stats, weak/strong areas
- `GET /api/questions/recent` → recent answers with feedback
- `GET /api/questions/filters` → available companies, roles, topics, difficulties
- `POST /api/questions/submit` → submit new question for curation
- `POST /api/questions/upvote` → upvote/downvote question
- `POST /api/questions/answer` → submit text answer with AI feedback

### Profile & Stats
- `GET /api/profile/stats` → `{ name, plan, streak, longest_streak, xp, level, badges, skills, total_solved, heatmap, github_username, leetcode_username }`
- `PUT /api/profile/integrations` → `{ platform, username }` updates GitHub/LeetCode username

### Salary Benchmark
- `POST /api/salary/benchmark` → `{ job_title, location, company, years_experience, level }` → `{ market_rate, percentiles, factors_affecting_pay, companies_paying_above_market }`
- `POST /api/salary/compare` → `{ offers: [...] }` → `{ winner, winner_reason, comparison_matrix, recommendation }`
- `POST /api/salary/save` → `{ offer }` → `{ offer_id }`
- `GET /api/salary/history` → `{ offers: [...] }`

### Billing (PayPal)
- `POST /api/billing/checkout` → `{ checkout_url }` (PayPal approval link)
- `POST /api/billing/checkout/lifetime` → `{ checkout_url }` (PayPal approval link)
- `POST /api/billing/capture` → `{ order_id }` → `{ status, plan }` (captures payment after approval)
- `POST /api/billing/webhook` → PayPal webhook handler
- `GET /api/billing/status` → `{ plan, interviews_used, resumes_used }`

### Gamification & Skills
- `GET /api/gamification/profile` → `{ xp, level, streak, badges, total_* }`
- `POST /api/gamification/record` → `{ activity_type, score }` → `{ xp_gained, new_streak, new_badges, level }`
- `GET /api/gamification/leaderboard` → `{ users: [...] }`
- `GET /api/gamification/badges` → `{ badges: [...] }`
- `GET /api/gamification/skills` → `{ categories: { dsa: { score, skills }, ... }, overall_score }`
- `GET /api/gamification/skills/weak` → `{ weak_areas: [...] }`
- `GET /api/gamification/skills/readiness` → `{ overall, categories, recommendations }`

---

## Security Features

- **httpOnly cookies** — JWT never touches JavaScript (XSS-proof)
- **Rate limiting** — 30 req/min per IP on all endpoints
- **Account lockout** — 5 failed login attempts → 15 min lockout
- **CORS locked** — POST only methods, specific origins
- **PDF validation** — Magic bytes check (`%PDF-`) before processing
- **AI retry** — 3 retries with exponential backoff on AI API failures

---

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=placementpro
JWT_SECRET=<random-64-char-string>
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=google/gemini-2.0-flash-001
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox
FREE_TIER_INTERVIEW_LIMIT=3
FREE_TIER_RESUME_LIMIT=3
FREE_TIER_APTITUDE_LIMIT=5
FREE_TIER_COVER_LETTER_LIMIT=3
CORS_ORIGINS=http://localhost:5173,https://your-domain.vercel.app
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000  # or production URL
```

---

## Free Tier Logic

- Counter fields: `interviews_used`, `resumes_used`, `aptitude_used`, `cover_letters_used` on user document
- Monthly reset logic in `services/usage.py`: checks `monthly_reset_date` and resets counters when month changes
- Checked in each route handler before AI operations
- Limits defined in `config.py`: `FREE_TIER_INTERVIEW_LIMIT=3`, `FREE_TIER_RESUME_LIMIT=3`, `FREE_TIER_APTITUDE_LIMIT=5`, `FREE_TIER_COVER_LETTER_LIMIT=3`
- **Free tier now resets monthly** — counters reset on the 1st of each month
- **Question bank free limit**: 5 practice questions/month for free users; unlimited for Pro

---

## AI Prompts (The Moat)

All AI logic is in `backend/app/services/ai.py`. Key functions:

| Function | Purpose | Model |
|----------|---------|-------|
| `generate_interview_question()` | Creates next interview Q based on role + history | Gemini Flash |
| `evaluate_answer()` | Scores answer 1-10 with strengths/improvements | Gemini Flash |
| `analyze_resume()` | Scores resume across 4 dimensions | Gemini Flash |
| `optimize_ats()` | Extracts JD keywords, rewrites resume | Gemini Flash |
| `generate_resume_content()` | Writes resume from user details | Gemini Flash |
| `generate_aptitude_questions()` | Creates MCQs for placement prep | Gemini Flash |
| `generate_cover_letter()` | Writes tailored cover letters | Gemini Flash |
| `generate_linkedin_about()` | Creates LinkedIn About section | Gemini Flash |
| `generate_salary_negotiation_tips()` | Provides negotiation coaching | Gemini Flash |
| `generate_system_design_question()` | Creates system design interview Q | Gemini Flash |
| `evaluate_system_design_answer()` | Evaluates system design response | Gemini Flash |
| `generate_salary_benchmark()` | Provides market rate data | Gemini Flash |
| `generate_offer_comparison()` | Compares multiple job offers | Gemini Flash |
| `generate_behavioral_question()` | Creates company-specific behavioral Qs | Gemini Flash |
| `generate_coding_challenge()` | Creates timed coding problems | Gemini Flash |
| `generate_interview_tips()` | Provides company-specific interview tips | Gemini Flash |
| `generate_salary_negotiation_tips()` | Provides negotiation coaching | Gemini Flash |

All prompts return JSON. `parse_json()` handles AI output parsing with fallbacks.
All AI calls have retry logic (3 retries, exponential backoff).

**To improve quality:** Adjust prompts in `ai.py`. This is 80% of the product value.

---

## Known Issues (Fix Priority)

### P0 — CRITICAL (All fixed)
- [x] ~~Stripe checkout URLs hardcoded to `localhost:5173`~~ → Replaced with PayPal
- [x] ~~`created_at` never set on documents~~ → Fixed
- [x] ~~Pricing page buttons dead~~ → Fixed with PayPal checkout
- [x] ~~No rate limiting~~ → IP rate limiter added
- [x] ~~Synchronous Stripe calls~~ → All async httpx

### P1 — HIGH (All fixed)
- [x] ~~Interview role slug~~ → Sends label now
- [x] ~~InterviewSession crash on direct nav~~ → Handles missing state
- [x] ~~Dashboard ignores usage~~ → Shows real counters
- [x] ~~Education section missing~~ → Added to ResumeBuilder
- [x] ~~File upload/export bypass 401~~ → Fixed with credentials:include
- [x] ~~PDF validates filename~~ → Validates %PDF- magic bytes
- [x] ~~No 404 page~~ → Added

### P2 — MEDIUM (All fixed)
- [x] ~~JWT in localStorage~~ → httpOnly cookie
- [x] ~~No account lockout~~ → 5 attempts / 15 min lockout
- [x] ~~No retry logic for AI~~ → 3 retries, exponential backoff
- [x] ~~No error boundary~~ → ErrorBoundary wraps App
- [x] ~~No loading skeletons~~ → Skeleton components added
- [x] ~~MongoDB client never closed~~ → Closed on shutdown
- [x] ~~Free tier was lifetime~~ → Monthly reset logic added

### P3 — LOW (Remaining)
- [ ] No password reset flow
- [ ] No email verification on signup
- [ ] No audit log for admin actions
- [ ] No CSP headers
- [ ] No health check dashboard
- [ ] Monaco Editor not fully integrated (placeholder remains in some flows)
- [ ] Need 100+ seeded problems with proper visible/hidden test cases

---

## Deployment Checklist

### Backend (Render)
- [ ] Create Render account
- [ ] Connect GitHub repo
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add all env vars in Render dashboard
- [ ] Enable auto-deploy on push

### Frontend (Vercel)
- [ ] Create Vercel account
- [ ] Import GitHub repo
- [ ] Set framework preset: Vite
- [ ] Add `VITE_API_URL` env var pointing to Render backend URL
- [ ] Deploy

### MongoDB Atlas
- [ ] Create free cluster
- [ ] Add IP whitelist (0.0.0.0/0 for Render)
- [ ] Create database user
- [ ] Get connection string → add to backend .env

### PayPal
- [ ] Create PayPal Developer account
- [ ] Create REST API app in dashboard
- [ ] Get Client ID + Secret → add to .env
- [ ] Set webhook endpoint: `https://your-backend.onrender.com/api/billing/webhook`
- [ ] Webhook events: `PAYMENT.CAPTURE.COMPLETED`, `PAYMENT.CAPTURE.DENIED`
- [ ] Switch PAYPAL_MODE from sandbox to live before production

### OpenRouter
- [ ] Create account at openrouter.ai
- [ ] Add $5 credit
- [ ] Get API key → add to .env

---

## Development Commands

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate    # Mac/Linux
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
```

---

## Recent Improvements (July 2026)

### Backend Security & Infrastructure
- **CSP Headers** — Added `Content-Security-Policy` middleware blocking inline scripts, restricting frame loading, and securing Connect/SCRIPT/STYLE sources
- **Security Headers Middleware** — Added `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy`, and `Strict-Transport-Security`
- **Request ID Middleware** — Added `X-Request-ID` header for request tracing across logs and monitoring

### Question Bank Enhancements
- **Random Question Endpoint** — `GET /api/questions/random` with filters (type, difficulty, topic, company) and `exclude_solved` support for quick practice
- **Progressive Hints** — `POST /api/questions/{id}/solution` with `hint_level` parameter for unlocking hints progressively; free users get 1 hint, Pro users get all hints
- **Solution Access Control** — Solutions and hidden test cases are locked for free users who haven't solved the problem; Pro users and solved problems get full access

### Frontend Improvements
- **Dynamic Daily Missions** — Dashboard missions now adapt based on user progress and weak areas; weak-area practice missions appear when students have identified gaps
- **Quick Practice Button** — Added "Quick Practice" link in Navbar for fast access to random questions
- **Keyboard Shortcuts** — `Cmd/Ctrl+K` toggles search, `Escape` closes modals/search
- **Landing Page CTAs** — Improved call-to-action buttons with "Launch Mission" and "Access Command Deck" labels
- **Weak Area Highlight** — Dashboard mission for weak-area drilling appears dynamically when assessment data is available

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

### Frontend (React)
- Functional components with hooks
- Zustand for global state (auth only)
- `api.js` service class for all backend calls (credentials: include)
- Tailwind CSS for styling (no component library)
- `ProtectedRoute` wrapper for authenticated pages
- `ErrorBoundary` wraps entire app
- Consistent card-based layouts

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

---

## Scaling Architecture (100K+ Users)

### Infrastructure Components

| Component | Current | Scaled Solution |
|-----------|---------|-----------------|
| **Backend** | Single Render instance | Dockerized + Kubernetes/ECS with auto-scaling |
| **Database** | MongoDB Atlas free tier (512MB) | MongoDB Atlas M10+ with indexes + sharding |
| **Cache** | In-memory only | Redis (Upstash free → ElastiCache) |
| **Frontend** | Vercel | Vercel + Cloudflare CDN |
| **AI** | Synchronous calls | Async queue + fallback models |

### Docker Deployment

```bash
# Build and run locally
docker-compose up --build

# Production deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Redis Configuration

```env
# .env
REDIS_URL=redis://localhost:6379/0  # Local
REDIS_URL=redis://:password@redis-endpoint:6379  # Production
```

### Database Indexes (Critical for Performance)

All indexes are created automatically on startup:
- `users`: email (unique), plan, created_at
- `interviews`: user_id + created_at (compound), status
- `resumes`: user_id + created_at (compound), ats_score
- `aptitude_tests`: user_id + created_at (compound), category, status
- `coding_challenges`: user_id + created_at (compound), topic, difficulty
- `gamification`: user_id (unique), xp (for leaderboard)
- `skill_graphs`: user_id (unique)
- `curated_questions`: company, topic, difficulty, type, compound indexes
- `question_answers`: user_id, compound (user_id + question_id), created_at
- `solved_problems`: user_id, compound unique (user_id + question_id), created_at

### Frontend Optimizations

- **Code splitting** — Lazy load all pages (reduces initial bundle by 60%)
- **Gzip compression** — Enabled in nginx config
- **Asset caching** — 1-year cache for static assets
- **Security headers** — X-Frame-Options, CSP, etc.

### Cost Projections

| Scale | Infrastructure | AI | Total |
|-------|---------------|-----|-------|
| 1K users | $0 (free tiers) | $10/mo | $10/mo |
| 10K users | $50/mo (Redis + DB) | $100/mo | $150/mo |
| 100K users | $500/mo (K8s + DB + Redis) | $2,000/mo | $2,500/mo |

---

## File Editing Rules

When modifying this project:

1. **Backend files:** Always use `async/await`. Never use synchronous blocking calls in route handlers.
2. **Frontend files:** Use Tailwind classes. No inline styles. Follow existing component patterns.
3. **AI prompts:** These are the core product value. Test thoroughly before changing.
4. **Database schema:** Changes require migration consideration for existing users.
5. **API contracts:** Frontend and backend must stay in sync. Update both when changing endpoints.
6. **Auth:** Always use cookie-based auth. Never store JWT in localStorage.
7. **Payments:** All payment processing goes through PayPal REST API.
