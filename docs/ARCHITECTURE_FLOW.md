# BountyCode — Complete Architecture Flow

## 1. Vision (Locked)

**North Star:**
> BountyCode is an interactive placement-preparation platform for Indian engineering students targeting service-based and mass-recruiting companies — structured, visually-taught patterns like AlgoMaster, personalized to your role/company/language, with a game layer that makes daily practice a habit. Built for the TCS/Infosys/Wipro/Cognizant/Capgemini/Accenture pipeline that FAANG platforms ignore.

**Launch Date:** October 18, 2026

**Core Loop:**
```
Company → Blueprint → Skill → Pattern → Interactive Lesson →
Practice → Assessment → Evidence → Diagnosis → Repair → Retest → Readiness
```

Game wraps it: Mission → Progression → XP → Streak → Rank → Unlock.
Game = retention layer, not product.

---

## 2. Information Architecture — Current (Post-Cleanup)

### Primary Navigation (5-Lens Company-First Flow)

| Lens | Route | Purpose |
|------|-------|---------|
| **Today** | `/dashboard` | PrepHub — unified company-first hub with readiness, daily mission, blockers, quick actions |
| **Learn** | `/learn` | Learning hub — company-prep lessons, pattern mastery, SRS review |
| **Practice** | `/practice` | Question bank, coding challenges, compiler, topics/patterns |
| **Assess** | `/company-mocks` | Mock OAs, company-specific assessments, readiness scoring |
| **Profile** | `/career-profile` | User profile, stats, badges, settings, career tools |

### Secondary Routes (still exist, not in primary nav)

| Route | Purpose |
|-------|---------|
| `/interview` | AI Interview sessions (behavioral/HR/technical) |
| `/company-tracks` | Company-specific prep tracks |
| `/journey` | Legacy redirect → `/dashboard` |
| `/mock-oa` | Legacy redirect → `/company-mocks` |
| `/home` | Legacy redirect → `/dashboard` |
| `/hub` | Legacy redirect → `/dashboard` |
| `/prepare` | Legacy redirect → `/dashboard` |
| `/compete` | Legacy redirect → `/company-mocks` |
| `/career` | Legacy redirect → `/career-profile` |

### Complete Route Map

#### Public Routes
- `/` — Landing page
- `/login` — Login
- `/register` — Register
- `/forgot-password` — Forgot password
- `/reset-password` — Reset password
- `/pricing` — Pricing plans
- `/privacy` — Privacy policy
- `/terms` — Terms of service

#### Authenticated Routes
- `/dashboard` — **PrepHub (canonical home)**
- `/learn` — Learning hub
- `/learn/lesson/:slug` — **Company-prep lesson player** (new)
- `/practice` — Practice console
- `/practice/:topic` — Topic-specific practice
- `/company-mocks` — Company mock assessments
- `/company/:companyId` — Company-specific prep
- `/career-profile` — User profile & stats
- `/interview` — AI Interview
- `/interview/session/:id` — Live interview session
- `/interview/booking` — Book mock interview
- `/coding-challenge` — Coding challenges
- `/compiler` — Code compiler/playground
- `/question-bank` — Browse question bank
- `/solve/:questionId` — Solve specific question
- `/aptitude-test` — Aptitude test
- `/system-design` — System design practice
- `/resume-builder` — Resume builder
- `/resume-ats` — ATS optimizer
- `/cover-letter` — Cover letter generator
- `/salary-benchmark` — Salary benchmarking
- `/salary-negotiation` — Salary negotiation coach
- `/placement-calendar` — Placement drives calendar
- `/alumni-experiences` — Alumni interview experiences
- `/community` — Community discussions
- `/leaderboard` — Gamification leaderboard
- `/tower` — Tower/boss battles
- `/daily-challenge` — Daily adaptive challenge
- `/problem-of-the-day` — Daily problem
- `/monthly-contests` — Monthly coding contests
- `/dsa-visualizer` — Algorithm visualizations
- `/learning-hub` — Learning paths hub
- `/language-journey` — Language learning paths
- `/adaptive-path` — AI-driven adaptive learning
- `/project-generator` — AI project generator
- `/ai-mentor` — AI mentor chat
- `/onboarding` — Onboarding quest
- `/settings` — User settings
- `/history` — Activity history
- `/admin` — Admin dashboard
- `/admin/content` — Admin content management
- `/admin/exam-review` — Admin exam review

---

## 3. User Flow — Student Journey

### Entry Flow
```
Landing → Register/Login → Onboarding Quest → 
Select Target Companies (TCS/Infosys/Wipro/etc.) →
PrepHub (/dashboard)
```

### Core Learning Flow
```
PrepHub
  ↓
Select Company (e.g., TCS)
  ↓
View Readiness Score + Blueprint
  ↓
Choose Path:
  ├─→ Learn → Lesson Player → Complete Lesson → XP/Proof earned
  ├─→ Practice → Question Bank → Solve → Feedback → SRS cards
  ├─→ Assess → Mock OA → Score → Readiness update → Repair path
  └─→ Daily Mission → Complete → Rewards
```

### Lesson Flow (New)
```
/learn/lesson/:slug
  ↓
Step 1-N (Explain / Interactive / Practice)
  ↓
Assessment
  ↓
Completion → record_practice() → XP/Proof/Bounty
  ↓
SRS cards generated
```

### Practice Flow
```
/question-bank
  ↓
Filter by company/pattern/difficulty
  ↓
Solve problem
  ↓
Judge runs test cases
  ↓
Result → Explanation → SRS card created
```

### Mock OA Flow
```
/company-mocks
  ↓
Select company (TCS NQT, etc.)
  ↓
Timed assessment (blueprint-matched sections)
  ↓
Submit → Score → Evidence recorded
  ↓
Readiness updated
  ↓
Weak areas → Repair lessons → Retest
```

---

## 4. Backend Architecture

### Route Registry (`backend/app/main.py`)
Auto-discovers all route files in `backend/app/routes/`. Each file is mounted at `/api/v1/<feature>`.

### Key Route Files

| Route File | Prefix | Purpose |
|------------|--------|---------|
| `auth.py` | `/auth` | Register, login, logout, onboarding |
| `lesson.py` | `/lessons` | Lesson serving (legacy) |
| `company_lessons.py` | `/company-lessons` | **New company-prep lesson serving** |
| `questions.py` | `/questions` | Question bank curation |
| `questions_solve.py` | `/questions` | Question solving/submission |
| `daily_challenge.py` | `/daily-challenge` | Company-aware daily missions |
| `companies.py` | `/companies` | Company blueprints, readiness, roadmap |
| `adaptive_learning.py` | `/adaptive` | Skill assessment, weak areas, daily plans |
| `gamification.py` | `/gamification` | XP, levels, streaks, badges, tower |
| `coding.py` | `/coding` | Coding challenges |
| `compiler.py` | `/compiler` | Piston API code execution |
| `interview.py` | `/interview` | Interview sessions |
| `resume.py` | `/resume` | Resume upload/generate/optimize |
| `billing.py` | `/billing` | PayPal checkout/webhooks |
| `aptitude.py` | `/aptitude` | Aptitude test flow |
| `system_design.py` | `/system-design` | System design practice |
| `readiness_engine.py` | *(service)* | Deterministic per-company readiness scoring |
| `question_store.py` | *(service)* | File-based question bank loader |
| `gamification.py` | *(service)* | **Single writer for XP/coins/stars/streak/combo/badges** |

### Service Layer
- All business logic lives in `backend/app/services/`
- AI calls via `httpx.AsyncClient` to OpenRouter with retry/fallback
- Code execution via Piston API or local sandbox
- Question content loaded from JSON files at startup — **never stored in MongoDB**

---

## 5. Question Bank Architecture

### Residency Rule (Binding)
Question content lives in versioned JSON files under `backend/app/data/` and `backend/app/content/`, loaded into memory at startup by `question_store`. **Never write question content to MongoDB.**

### Trust Pipeline
```
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED
```

- Only TRUSTED/AUTOMATED_CHECKED content serves to students
- No LLM in question authoring, tagging, grading keys, or promotion
- Company banks are deterministic filters over human-verified stock

### Verified Banks (Current)

| Bank | Location | Count | Status |
|------|----------|-------|--------|
| TCS NQT MCQs | `backend/app/data/tcs_nqt_mcq_verified.json` | 2,472 | Automated checked |
| TCS NQT Coding | `backend/app/data/tcs_nqt_coding_verified.json` | 97 | Verified |
| Verified Placement | `backend/app/data/verified_placement_questions.json` | — | Trusted |
| SQL Practice | `backend/app/data/sql_practice_bank.json` | — | Trusted |
| System Design | `backend/app/data/system_design_bank.json` | — | Trusted |
| Interview Practice | `backend/app/data/interview_practice_bank.json` | — | Trusted |

### TCS NQT Quarantined
- `backend/app/data/tcs_nqt_questions.json` — 450 placeholder entries quarantined
- `backend/app/data/tcs_nqt_coding_auto_verified.json` — empty (placeholder solutions)
- These await original content sourcing; cannot be promoted without violating trust rules

---

## 6. Company Blueprint System

### Supported Companies
TCS, Infosys, Wipro, Cognizant, Capgemini, Accenture, HCL, TechM, LTI, Mphasis

### Blueprint Structure
Each company defines:
- Sections (e.g., Quantitative, Verbal, Reasoning, Programming Logic)
- Timing per section
- Skill weights
- Pass thresholds
- Pattern mappings

### Readiness Engine
- Deterministic scoring per company
- No LLM probability
- Based on pattern mastery + blueprint weights
- Outputs: overall score, domain breakdown, blockers, next steps

---

## 7. Lesson System (New)

### Format
Company-prep lessons are JSON files in `backend/app/data/lessons/*.json`

### Schema
```json
{
  "id": "lesson_successive_percentage_001",
  "slug": "successive_percentage_change",
  "title": "Successive Percentage Change",
  "domain": "Quantitative Aptitude",
  "pattern": "Successive Percentage Change",
  "difficulty": "easy",
  "duration_min": 15,
  "xp_reward": 80,
  "mastery_threshold": 0.7,
  "steps": [
    {
      "step_number": 1,
      "step_type": "explain",
      "title": "The Trap of Simple Addition",
      "content": "...",
      "example": "...",
      "formula": "...",
      "tip": "..."
    },
    {
      "step_number": 2,
      "step_type": "interactive",
      "title": "Apply the Formula",
      "prompt": "...",
      "options": ["A", "B", "C", "D"],
      "correct_index": 1,
      "explanation": "..."
    }
  ],
  "practice_questions": ["tcs_nqt_quant_0001"],
  "assessment": {
    "questions": [...],
    "mastery_threshold": 0.7,
    "duration_sec": 120
  },
  "srs_cards": [
    {
      "type": "formula",
      "question": "...",
      "answer": "..."
    }
  ]
}
```

### API Endpoints
- `GET /api/v1/company-lessons` — list all lessons
- `GET /api/v1/company-lessons/:slug` — get lesson content
- `POST /api/v1/company-lessons/:slug/complete` — record completion + rewards

### Frontend
- `LessonPlayer.tsx` — step-based player with progress, quizzes, explanations
- Route: `/learn/lesson/:slug`
- Wired in `lazy.ts` and `AppRoutes.tsx`

### Current Lessons (5)
1. `successive_percentage_change.json` — Quantitative
2. `blood_relations.json` — Reasoning
3. `reading_comprehension.json` — Verbal
4. `flowchart_basics.json` — Programming Logic
5. `arrays_basics.json` — DSA

---

## 8. Gamification System

### Single Writer Rule (Binding)
The only writer of XP, coins, stars, streak, combo, badges, and weekly/monthly league XP is `record_practice()` in `backend/app/services/gamification.py`. Direct `$inc`/`$set` on those fields elsewhere is a bug.

### Reward Types
- **XP** → Levels 1-100, titles from Hatchling → God of Code
- **Proof** → Company-specific title bands (TCS/Infosys/Wipro/Cognizant)
- **Bounty** → Currency for shop/power-ups
- **Streak** → Daily practice streak multiplier
- **Badges** → Achievement badges (30+)
- **League** → Weekly/monthly league rankings

### Activity Scoring
Callers pass a 0–10 pedagogical score; engine normalizes to 0–100 percents centrally. World/language/company travel in `metadata`, never as `activity_type`.

---

## 9. Pricing

### Plans

| Plan | Price | Features |
|------|-------|----------|
| **Free** | ₹0/month | 3 interviews/month, 3 resume reviews, 5 aptitude tests, 3 cover letters, 1 company mock/month, 5 question bank/month, 20 compiler runs/day, 5 AI questions/day, 10 problems solved/day |
| **Pro** | ₹799/month (~$9) | Unlimited everything, priority AI, advanced analytics, custom learning paths |
| **Lifetime** | ₹3,999 one-time (~$39) | All Pro features forever, early access to new features |

### Free Tier Limits
| Feature | Monthly Limit | Daily Limit |
|---------|--------------|-------------|
| Interviews | 3 | — |
| Resume reviews | 3 | — |
| Aptitude tests | 5 | — |
| Cover letters | 3 | — |
| Company mocks | 1 | — |
| Question bank | 5 | — |
| Compiler runs | — | 20 |
| AI questions | — | 5 |
| Problems solved | — | 10 |

---

## 10. Deployment Architecture

### Frontend
- **Host:** Cloudflare Pages
- **Build:** Vite 5.4.21
- **Root directory:** `frontend/`
- **Build command:** `npm run build`
- **Output:** `frontend/dist/`
- **Config:** `frontend/wrangler.toml` (bypasses Vite auto-detection)

### Backend
- **Host:** To be deployed (Docker-ready)
- **Framework:** FastAPI + Motor (MongoDB async)
- **Python:** 3.12
- **Entry:** `backend/app/main.py`

### CI/CD
- GitHub repo → Cloudflare Pages auto-deploy on push to `main`
- Backend: `python -m compileall app/ -q` passes clean

---

## 11. Current State Summary

### Completed
- ✅ 5-lens company-first navigation (Today/Learn/Practice/Assess/Profile)
- ✅ PrepHub as canonical dashboard at `/dashboard`
- ✅ Legacy route redirects
- ✅ TypeScript/JSX fixes
- ✅ Cloudflare deployment config (`wrangler.toml`)
- ✅ TypeScript downgraded to 6.0.3 for ESLint compatibility
- ✅ 5 interactive company-prep lessons with JSON schema
- ✅ Lesson player frontend (`LessonPlayer.tsx`)
- ✅ Lesson API backend (`company_lessons.py`)
- ✅ TCS NQT verification: 2,472 MCQs + 97 coding questions
- ✅ Question store updated with verified banks

### In Progress
- 500 TCS NQT questions need human review to promote from automated_checked → verified
- Readiness scores integration in PrepHub
- Company roadmap endpoint testing

### Blocked/Not Started
- World 1 complete lesson loop (10-step) for all 35 lessons
- 5,000 question verification target
- Email verification on signup
- API versioning at app level

---

## 12. Key Files Reference

### Frontend
- `frontend/src/app/AppRoutes.tsx` — Route registry
- `frontend/src/pages/lazy.ts` — Lazy-loaded pages
- `frontend/src/pages/PrepHub.tsx` — Canonical dashboard
- `frontend/src/pages/LessonPlayer.tsx` — Lesson player
- `frontend/src/components/BottomNav.tsx` — Mobile bottom nav
- `frontend/src/components/Navbar.tsx` — Top navigation
- `frontend/src/services/api/companyLessons.ts` — Lesson API client
- `frontend/wrangler.toml` — Cloudflare config

### Backend
- `backend/app/main.py` — FastAPI app, route auto-discovery
- `backend/app/routes/company_lessons.py` — Lesson serving API
- `backend/app/services/question_store.py` — Question bank loader
- `backend/app/services/gamification.py` — Reward writer
- `backend/app/services/readiness_engine.py` — Readiness scoring
- `backend/app/data/lessons/*.json` — Lesson content files
- `backend/app/data/tcs_nqt_mcq_verified.json` — Verified TCS MCQs
- `backend/app/data/tcs_nqt_coding_verified.json` — Verified TCS coding
- `backend/scripts/verify_tcs_nqt.py` — Verification script

### Docs
- `docs/BOUNTYCODE_VISION_LOCK.md` — Binding product vision
- `docs/PRD_SERVICE_BASED_V1.md` — Product requirements
