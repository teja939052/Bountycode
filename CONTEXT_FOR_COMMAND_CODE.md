# PlacementPro — Complete Context Handoff for Command Code

> This document is the single source of truth. Read AGENTS.md, FUTURE.md, and README.md too.
> Last updated: August 2026

---

## 1. What This Is

**PlacementPro** — AI-powered placement/job-search prep platform (students + professionals). Built by a solo founder with MimoCode (AI). Freemium SaaS targeting:
- **Indian students** (campus placements: TCS, Infosys, Wipro, aptitude tests)
- **US/Global job seekers** (behavioral interviews, resume optimization, salary negotiation, system design)
- **Professionals** (career changers, job switchers, FAANG aspirants)

The app has **50+ core features** and **130+ pages** (120+ TSX pages, 122 counted in `frontend/src/pages`).

---

## 2. Tech Stack

### Backend — FastAPI + MongoDB + Motor (async)
- Python 3.11, FastAPI, Motor async MongoDB driver
- 65+ route files in `backend/app/routes/`, 51+ service files in `backend/app/services/`
- 50+ MongoDB collections
- AI: OpenRouter → **Gemini 2.0 Flash** primary + 3-4 fallbacks (Llama 3.1, Phi-3, DeepSeek) with circuit breaker + retry (3x exponential backoff) + 1hr caching (Redis → in-memory fallback)
- Payments: PayPal primary, Stripe secondary (both implemented)
- Code execution: Piston API primary, local sandbox + Docker sandbox + remote fallbacks (Wandbox/Glot.io) for resilience
- Auth: JWT in httpOnly cookies, rate limiting (60/min/IP), login lockout (5 attempts → 15 min)
- RabbitMQ job queue + Redis cache (optional, graceful fallback)
- WebSockets: chat, battles, real-time (max 50k connections, 15s ping)

### Frontend — React 18 + Vite 5 + Tailwind 3
- **TypeScript migration in progress** — most pages are now `.tsx` (was all `.jsx`)
- Zustand for global auth state, Framer Motion, Monaco Editor
- `services/api/index.ts` aggregated API object
- Lazy-loaded pages via `React.lazy()` for code splitting
- ~5,892 pre-existing TypeScript errors accepted (not blocking builds — Vite uses esbuild, ignores tsc)

### Deployment
- Vercel (frontend, Hobby tier 100GB/mo) + backend currently local/sandbox
- Bandwidth protection: Cloudinary for images, YouTube embeds for videos

---

## 3. Plans & Pricing (Current — August 2026)

Pricing ladder enforced in `backend/app/routes/billing.py` (monthly < yearly ≈ 5-6x monthly < lifetime ≈ 8-12x monthly).

| Plan | Key | USD | INR | Notes |
|------|-----|-----|-----|-------|
| **Free** | "Cadet" | $0 | ₹0 | Monthly reset, no card |
| **Pro** | pro_monthly | $19/mo | ₹99/mo | Unlimited everything |
| **Pro Yearly** | pro_yearly | $99/yr | ₹499/yr | "Strategist" |
| **Lifetime** | lifetime | $149 one-time | ₹1,499 | "Admiral" |
| **Team** | team | $145/mo/seat (min 5 seats) | ₹12,250 | 5-50 seats |
| **Team Yearly** | team_yearly | $1,499/yr | ₹1,19,900 | |
| **Enterprise** | enterprise_monthly | $99/mo/seat (min 10 seats) | ₹66,392 | |
| **Enterprise Yearly** | enterprise_yearly | $999/yr | ₹6,63,920 | |

Plan keys stored on user: `free`, `pro`, `pro_yearly`, `lifetime`, `team`, `enterprise`.

### Free Tier Limits (monthly unless noted)
| Feature | Free Limit |
|---------|-----------|
| Interviews | 3/mo |
| Resume reviews | 3/mo |
| Aptitude tests | 5/mo |
| Cover letters | 3/mo |
| Company mocks | 1/mo |
| Predictor uses | 3/mo |
| Question bank | 5/mo |
| Compiler runs | 20/day |
| AI questions | 5/day |
| Mystery boxes | 1/day |
| Problems solved | 10/day |
| Mock interviews | 1/mo |
| Interview bookings | 3/mo |

Free tier companies limited to: tcs, infosys, wipro.

### Owner Admin Account (IMPORTANT)
- **Email**: `sridevi72901@gmail.com`
- **Password**: `lubuma@1234`
- **Plan in DB**: `enterprise`
- **Access**: Full admin via `ADMIN_EMAILS` config bypass (does NOT require pro/lifetime plan)
- Admin analytics live at `/admin` route (AdminDashboard.tsx) — NOT `/dashboard`

---

## 4. Admin Access Logic (How It Works Now)

**Admin = `plan in ("pro","lifetime")` OR email in `ADMIN_EMAILS`** — enforced in TWO places:
1. `backend/app/routes/auth.py` — `get_me` returns `is_admin` + `role`
2. `backend/app/middleware/auth.py` — `get_current_user` injects `is_admin` + `role` into user object for protected routes

Config: `backend/app/config.py:63` → `ADMIN_EMAILS = "sridevi72901@gmail.com"`

Admin endpoints check `user.get("role") == "admin" or user.get("is_admin") is True` → 403 otherwise. Files: `analytics_admin.py`, `admin_content.py`, `coupon.py`, `tiers.py`, `admin_monitoring.py`.

**Verified working endpoints** (all 200 with owner token):
- `GET /api/v1/analytics/admin/realtime`
- `GET /api/v1/analytics/admin/visitors?days=30`
- `GET /api/v1/analytics/admin/pages?days=7`
- `GET /api/v1/analytics/admin/geo`
- `GET /api/v1/analytics/admin/retention`

---

## 5. Routes / Key API Prefixes

All modern routes use `/api/v1/<feature>`. Some legacy routes use `/api/<feature>` (no versioning at app level — individual files choose).

Key areas:
- Auth: `/api/v1/auth/*` (register, login, me, onboarding, forgot/reset password)
- Interview: `/api/v1/interview/*`
- Questions/LeetCode: `/api/v1/questions/*` + `questions_solve.py`
- Gamification: `/api/v1/gamification/*`
- Coding: `/api/v1/coding/*`
- Compiler: `/api/v1/compiler/*`
- Company prep: `/api/v1/company/*`
- Learning: `/api/v1/learning/*`, `/api/v1/language-paths`
- Analytics: `/api/v1/analytics/track`, `/api/v1/analytics/admin/*`
- Billing: `/api/v1/billing/*` (PayPal + Stripe checkout, webhooks, status)
- Salary: `/api/v1/salary/*`
- Social: `/api/v1/chat/ws`, `/api/v1/invite/*`, `/api/v1/friends/*`, `/api/v1/study-squads/*`, `/api/v1/gd-rooms/*`
- Health: `/api/health/*` (ping, status, ready, live, metrics, dependencies) — NOT under v1

Full route list: run `python -c "from app.main import app; [print(r.methods, r.path) for r in app.routes]"` in `backend/`.

---

## 6. Recent Work (August 2026 — This Session)

### Completed
1. **Admin access for owner** — `sridevi72901@gmail.com` now has full admin (ADMIN_EMAILS config + is_admin/role in both auth paths). Admin analytics verified working.
2. **Frontend TSX fixes** — `Rocket` + `ListChecks` icon imports added to `StudentDashboard.tsx` (fixed ReferenceErrors).
3. **Onboarding contrast fixes** — text-gray-100 on dark backdrop in Onboarding.tsx.
4. **E2E Encrypted Chat** — WS `/api/v1/chat/ws` with encryption, message history, unread counts.
5. **Unified Invite System** — invites for friends/study-squads/discussions, single email pipeline.
6. **Admin analytics** — geo + retention endpoints added (`/admin/geo`, `/admin/retention`), RetentionAdmin.tsx page.
7. **WebSocket scaling** — `WS_MAX_CONNECTIONS: 50000`, `WS_PING_INTERVAL: 15s`.
8. **AI service split** — `services/ai.py` split into domain modules (`ai_core.py`, `ai_interview.py`, `ai_resume.py`, `ai_behavioral.py`, `ai_coding.py`, `ai_aptitude.py`, `ai_cover_letter.py`, `ai_project.py`, `ai_salary.py`, `ai_system_design.py`).
9. **Question bank seeding** — 500+ questions via multiple seed scripts; `questions.py` split into `questions.py` + `questions_solve.py`.
10. **Campus ecosystem** — StudySquads, GD rooms, friends, peer review, report card, CGPA simulator, drive tracker, placement calendar, study library, company directory (2026-27 companies).
11. **Frontend theme system** — candy + space themes, ThemeProvider/ThemeSwitcher, theme-vars.css.

### In Progress / Blocked
- **`/api/v1/revenue/summary` has a bug** — unhandled error (undefined variable `paid_total` in `backend/app/routes/revenue.py`). NOT yet fixed.
- **No `/admin/users` endpoint** — 404. Admin dashboard may need one for user management.
- **`getHealthStatus` 404 on frontend** — `flatOverrides.ts` uses `/health` or `/health/status`; backend health lives at `/api/health/*`. May already be wired correctly via generated client but needs verification.
- **Frontend `request.ts:102` "Request failed"** seen on `/admin` page — one or more dashboard API calls failing (verify which).
- **`backend/app/middleware/auth.py`** must NOT use `from app.config import settings` (import fails); it uses module-level `settings = get_settings()`.

---

## 7. Known Issues (Priority Order)

### P0 — CRITICAL (Recently Fixed)
- [x] Circuit breaker `await` bug in `chat_completion()`
- [x] `FALLBACK_MODELS` included primary redundantly
- [x] `circuit_breaker` undefined variable
- [x] `call_with_resilience()` dict `.get()` on CircuitBreaker object
- [x] CircuitBreaker missing `is_open`/`failures`/`last_failure_time` properties + `allow_request()`/`record_failure()`/`record_success()` methods
- [x] `asyncio.get_event_loop()` deprecation → `get_running_loop()`

### P1 — HIGH (Remaining)
- [ ] `/api/v1/revenue/summary` unhandled error (`paid_total` undefined) — owner-facing, FIX NEXT
- [ ] ~5,892 pre-existing TS errors on frontend (accepted, but cleaning helps)
- [ ] `ai.py` still large — domain split done, verify imports all updated

### P2 — MEDIUM
- [ ] No app-level API versioning consistency
- [ ] No Redis connection pooling config
- [ ] `_LazyCollection` `__getattr__` magic can mask typos
- [ ] Admin dashboard "Request failed" — find which call fails on `/admin`

### P3 — LOW
- [ ] No email verification on signup
- [ ] No admin audit log UI (audit_log.py service exists — not wired to UI)
- [ ] `index.css` 796+ lines with dead theme animations
- [ ] Health dashboard UI exists (HealthDashboard.tsx) but route wiring unverified
- [ ] Monaco Editor not integrated in all flows

---

## 8. Business Goals / Roadmap

**Target: $2M ARR** (see FUTURE.md). Revenue targets in config:
- `REVENUE_TARGET_ANNUAL = 2000000`
- `MRR_TARGET = 166667`
- `ARPU_TARGET = $12`
- `CHURN_TARGET = 5%`

### Phases
1. **Launch & Validate (M1-3)**: 200 users, $180 MRR. Distribution: Reddit, LinkedIn, Product Hunt.
2. **Growth (M3-6)**: 1,000 users, $720 MRR. SEO, YouTube/TikTok, partnerships, annual plan.
3. **Scale (M6-12)**: 3,000 users, $1,800 MRR. Paid ads, community, enterprise exploration. Price raises (Pro $12, Team $29/5 seats, Lifetime $59).
4. **$1M ARR (M12-18)**: Hybrid play — 800 Pro + 200 Team + 100 Enterprise. White-label, API product, mobile app, browser extension, AI career coach.

### Monetization modules already built
- Referral program (30 days reward, 12 max, min 30 days used)
- Coupons (20% default discount, 1000 max uses)
- Trials (feature trials service)
- API product pricing ($0.50/1K requests, $49/mo base)
- White-label licensing ($299/mo, $2,499/yr)
- Merch store (disabled by default)
- Revenue tracking (targets above)

---

## 9. Developer Workflow

### Verify after ANY change (MANDATORY)
```bash
# Backend import check
cd backend && python -c "from app.main import app"
# output must be: OK

# Frontend build
cd frontend && npm run build
# output must be: ✓ built in XXs (zero errors)
```

### Windows PowerShell notes
- `&&` / `||` are INVALID separators in PowerShell 5.1
- Use `cmd1; if ($?) { cmd2 }` for chaining
- `tail`, `grep`, `timeout` unavailable → use `findstr /i "built"` etc.
- Use `workdir` param, don't `cd ... && ...`

### Test endpoints (backend on :8000)
Use `TestClient` in `backend/`:
```python
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
res = client.post('/api/v1/auth/login', json={'email':'sridevi72901@gmail.com','password':'lubuma@1234'})
token = res.json()['token']
```

### Frontend smoke test
`npm run smoke` (11 checks) — requires backend on :8000, auto-starts Vite.

---

## 10. File Map (Key Files)

### Backend
- `backend/app/main.py` — FastAPI app, lifespan, 65+ routers, security middleware
- `backend/app/config.py` — ALL settings (admin emails at line 63, pricing-affecting limits)
- `backend/app/database.py` — Motor client, 50+ collections, init_db()
- `backend/app/middleware/auth.py` — JWT verify, cookie helpers, `get_current_user` (is_admin/role)
- `backend/app/routes/auth.py` — register/login/me/onboarding (get_me at ~line 174)
- `backend/app/routes/billing.py` — PayPal + Stripe, PRICING dict, coupon/team/enterprise
- `backend/app/routes/analytics_admin.py` — admin realtime/visitors/pages/geo/retention
- `backend/app/routes/revenue.py` — **BROKEN: `/summary` uses undefined `paid_total`**
- `backend/app/services/ai_core.py` + domain AI files — prompts + chat_completion + parse_json + retry
- `backend/app/services/code_executor.py` — Piston + local sandbox + remote fallbacks
- `backend/app/services/usage.py` — monthly/daily limits
- `backend/app/services/websocket_manager.py` — WS connection handling

### Frontend
- `frontend/src/App.tsx` — router, lazy pages, routes (/admin → AdminDashboard, /dashboard → StudentDashboard)
- `frontend/src/pages/StudentDashboard.tsx` — student view (Rocket/ListChecks imports at top)
- `frontend/src/pages/AdminDashboard.tsx` — admin analytics UI
- `frontend/src/pages/RetentionAdmin.tsx` — retention UI
- `frontend/src/services/api/index.ts` — aggregated API
- `frontend/src/services/api/flatOverrides.ts` — health/legacy overrides (getHealthStatus → `/health`)
- `frontend/src/services/api/request.ts` — fetch wrapper (error at line 102 = "Request failed")
- `frontend/src/store/authStore.ts` — Zustand auth state

---

## 11. Non-Goals / Guardrails
- Do NOT commit unless explicitly asked
- Do NOT add code comments unless asked
- Do NOT break the two verify commands
- Keep flat `useState<any>(null)` pattern (don't refactor unrelated types)
- Don't restart Redis/Mongo unnecessarily during testing
- Never log passwords or JWT secrets
- Backend runs from `D:\Project-Fremen\backend`; frontend from `D:\Project-Fremen\frontend`
