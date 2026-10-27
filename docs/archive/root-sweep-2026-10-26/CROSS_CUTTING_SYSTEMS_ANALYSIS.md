# BountyCode — Cross-Cutting Systems Analysis

> **Scope:** Backend + Frontend core infrastructure  
> **Date:** 2026-09-28  
> **Status:** Verified from source

---

## 1) Authentication & Authorization

### Files
- `backend/app/middleware/auth.py`
- `backend/app/routes/auth.py`

### Architecture
BountyCode uses **JWT access tokens** + **httpOnly refresh tokens** stored in cookies.  
The cookie name is `pp_token` (access) and `pp_refresh_token` (refresh).

#### Token Model
| Token | Lifetime | Storage | Rotation |
|-------|----------|---------|----------|
| Access (`pp_token`) | `JWT_EXPIRY_DAYS` (default 7) | httpOnly cookie | Re-issued on refresh |
| Refresh (`pp_refresh_token`) | `JWT_REFRESH_EXPIRY_DAYS` (default 30) | httpOnly cookie | **Rotated** on every refresh; old jti invalidated |

Refresh tokens carry a server-tracked `jti` stored in `users.refresh_jti`.  
Logout / password change sets `refresh_revoked_at` in MongoDB so stolen tokens cannot be rotated after revocation.

#### Auth Endpoints (`/api/v1/auth`)
| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/register` | Create user, hash password, set both cookies, fire welcome email async |
| `POST` | `/login` | Verify bcrypt password, set cookies, audit log, rate-limit check |
| `POST` | `/refresh` | Validate refresh cookie + jti match, rotate pair, update `last_active` |
| `POST` | `/logout` | Set `refresh_revoked_at`, clear both cookies |
| `GET` | `/me` | Return sanitized user + usage stats + `is_admin` + `role` |
| `GET` | `/me/state` | Aggregate state for Home: readiness, categories, weak areas, next mission |
| `POST` | `/update-profile` | Update `name` / `email` (unique check) |
| `POST` | `/change-password` | Verify current password, hash new password, revoke all refresh tokens |
| `POST` | `/forgot-password` | Generate 15-min reset token, email reset link |
| `POST` | `/reset-password` | Validate token + expiry, hash new password, clear token |
| `GET` | `/verify-email` | Validate 24-hr email verification token |
| `GET` | `/onboarding-status` | Check `onboarding.completed` |
| `POST` | `/onboarding-complete` | Persist onboarding + normalize target company to gamification profile |
| `GET` | `/google` | Redirect to Google OAuth2 consent |
| `GET` | `/google/callback` | Exchange code, find/create user, set cookies, redirect to frontend |

#### Authorization Rules
- **Admin** is derived **only** from `ADMIN_EMAILS` config (e.g. `sridevi72901@gmail.com`).  
  Subscription plan (`pro` / `lifetime`) does **not** grant admin rights.
- `require_plan(required_plan)` dependency enforces tier-based gating (`free < premium < pro < enterprise`).
- `require_admin` dependency enforces admin-only access.

#### Password Policy
- Minimum length: `PASSWORD_MIN_LENGTH` (default 8)
- Requires number: `PASSWORD_REQUIRE_NUMBER`
- Requires special character: `PASSWORD_REQUIRE_SPECIAL`
- Hashed with bcrypt (72-byte truncation)

#### Caching
- User document is cached in Redis/in-memory under `auth:user:{user_id}` with TTL 300s.
- **Privileges (`is_admin`, `role`) are never cached** — `_finalize_user()` recomputes them on every request.

---

## 2) Database & Data Layer

### File
- `backend/app/database.py`

### Connection
- **Motor** async driver with connection pooling.
- Singleton `AsyncIOMotorClient` / `AsyncIOMotorDatabase`.
- Pool defaults: `maxPoolSize=50`, `minPoolSize=10`, `maxIdleTimeMS=10000`.
- Lazy collection proxies via `_LazyCollection` to avoid import-time DB access.

### Collections (87 total)

#### Core User & Identity
| Collection | Purpose |
|------------|---------|
| `users` | User accounts, emails, password hashes, plan, usage counters, refresh jti |
| `career_profiles` | Extended career profile data |
| `referrals` | Referral program state |

#### Interview & Assessment
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

#### Resume & Career
| Collection | Purpose |
|------------|---------|
| `resumes` | Generated/uploaded resumes |
| `applications` | Job application tracker |
| `cover_letters` | Generated cover letters |
| `salary_offers` | Saved salary offers |

#### Learning & Content
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

#### Questions & Practice
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

#### Gamification
| Collection | Purpose |
|------------|---------|
| `gamification` | User gamification profile (level, diamonds, streak, badges, power-ups) |
| `gamification_events` | Immutable reward ledger (every XP/coin award) |
| `daily_challenges_users` | Daily challenge enrollment and progress |

#### Social & Community
| Collection | Purpose |
|------------|---------|
| `community_posts` | Community posts |
| `discussions` | Discussion threads |
| `study_groups` | Study groups |
| `bookmarks` | User bookmarks |
| `notes` | User notes |
| `alumni_experiences` | Alumni interview experiences |
| `placement_drives` | Campus placement drives |

#### Contest & Events
| Collection | Purpose |
|------------|---------|
| `contests` | Monthly contests |
| `contest_entries` | Contest entries |
| `playlists` | Learning playlists |

#### Analytics & Monitoring
| Collection | Purpose |
|------------|---------|
| `analytics_events` | Raw analytics events (TTL 180 days) |
| `analytics_rollups` | Pre-aggregated rollup counters |
| `service_metrics` | Periodic service metrics snapshots |
| `audit_logs` | Audit log (TTL 1 year) |
| `integrity_events` | Browser integrity signals (TTL 30 days) |

#### Billing & Payments
| Collection | Purpose |
|------------|---------|
| `payments` | Payment records |
| `revenue_events` | Revenue event tracking |
| `billing_metrics` | Billing metrics |
| `invoices` | Generated invoices |
| `coupons` | Coupon codes and usage |
| `processed_webhook_events` | Idempotent webhook processing |

#### Repair & Weakness (Closed-Loop Learning)
| Collection | Purpose |
|------------|---------|
| `repair_missions` | Repair missions from OA failures |
| `repair_events` | Repair event audit trail |
| `user_weaknesses` | Misconception-tagged weaknesses |

#### Game Extensions
| Collection | Purpose |
|------------|---------|
| `anime_card_progress` | Anime card game progress |
| `anime_cards` | Anime card inventory |
| `generated_projects` | AI-generated projects |
| `tutor_sessions` | Tutor session logs |

#### Misc / Legacy
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

### Index Strategy
- `init_db()` creates indexes for all collections on startup with conflict-safe `_safe_create_index()`.
- TTL indexes auto-expire: `analytics_events` (180 days), `submissions` (90 days), `practice_sessions` (90 days), `service_metrics` (30 days), `audit_logs` (1 year), `integrity_events` (30 days).

---

## 3) Question Bank & Content Trust

### Files
- `backend/app/services/question_store.py`
- `backend/app/services/auto_verify.py`

### Residency Rule (Binding)
**Question content lives in versioned files under `backend/app/data/` and is loaded into process memory at startup by `question_store`.**  
No code may read question content from MongoDB. The database holds student state only (attempts, submissions, results). No code may write question content to MongoDB.

### Trust Pipeline
```
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED
```

| Status | Meaning | Student-Facing? |
|--------|---------|-----------------|
| `unverified` | Raw imported/legacy content | **No** |
| `automated_checked` | Passed deterministic execution validation (no LLM) | **No** |
| `needs_review` | Awaiting human review | **No** |
| `reviewed` | Human verified | **Yes** |
| `verified` | Fully trusted (independent output verification) | **Yes** |
| `quarantined` | Execution failure or quorum report; sticky across restarts | **No** |

**Quarantine is sticky:** A reboot re-verify never clears a `quarantined` status. It is cleared only by explicit human review.

### Serving Gate
- `_is_servable(q)` returns `True` **only** if `trust_status in ("verified", "reviewed")` **and** `_is_executable(q)` is true.
- `get_question_for_serving()` enforces this gate and returns `None` for non-servable content.
- Admin/candidate modes can call `find_one(allow_unverified=True)` to see the unverified pool.

### Bank Loading Order
1. **Verified extra banks** (`EXTRA_BANKS`) — company-specific verified banks (TCS, Infosys, Wipro, etc.)
2. **Auto-checked banks** (`AUTO_CHECKED_BANKS`) — deterministic execution-passed artifacts
3. **Unverified banks** (`UNVERIFIED_EXTRA_BANKS`) — loaded so auto-verifier can promote passable entries

### Auto-Verifier (`auto_verify.py`)
- `verify_question(q)` runs deterministic checks:
  - **Structural check:** title, solution code, test cases / options / rubric present
  - **Coding:** Execute Python solution against test cases via `exec()` sandbox
  - **MCQ:** Validate options A/B/C/D and correct answer consistency
  - **Interview/System Design:** Structural completeness only
- Mutates `q.trust_status` to `automated_checked` or `quarantined` in-memory.
- `verify_all_questions()` runs after `load_all()` and respects sticky quarantine.

### Lesson Verification
- `verify_lesson()` checks structural completeness of world lesson data (concept, code prompt, predict/answer, hints, reward).
- Optional runtime checks execute starter/placeholder/broken/debug code via local sandbox.

### Striver Pattern Mapping
- Every coding question is tagged with a canonical Striver A2Z pattern (Arrays, Binary Search, DP, Graphs, etc.).
- Pattern detection: explicit `topic` mapping → keyword blob matching → fallback `Arrays`.

---

## 4) Gamification

### Files
- `backend/app/services/gamification.py`
- `backend/app/services/gamification_core.py`

### Currency & Progression Model

#### Diamonds (XP)
- Earned via `record_practice()` — the **only** writer of diamonds/coins/stars/streak/combo/badges.
- Base XP per activity type:
  - Interview: 50, Resume: 25, Aptitude: 25, Coding: 40, System Design: 50, Question Bank: 35, etc.
- Difficulty bonus for coding: Hard (≥9) = 80, Medium (≥7) = 40, Easy = 20.
- Perfect score (10/10): +40 bonus.
- High score (≥8): +20 bonus.
- Role multiplier applied (SDE, Data Science, DevOps, Frontend, Backend, QA, Mobile).

#### Level Curve
- `level = max(1, min(100, int(math.sqrt(diamonds / 50)) + 1))`
- Diamonds per level span: `xp_for_next_level(level) = level² * 50`
- Total diamonds to reach level N: `(N-1)² * 50`

#### Stars
- 1–3 stars per activity based on score and time:
  - Score ≥ 7 → 2 stars
  - Score ≥ 9 and time < 5 min → 3 stars

#### Coins
- Earned: `10 + (stars * 5)` per activity (15–25 coins).
- Spent on power-ups and streak repairs.
- **Coins never affect Diamonds/level** — cosmetic economy only.

#### Proof & Bounty
- **Proof** = non-spendable mastery signal (earned from learning activities).
- **Bounty** = spendable cosmetic currency.
- Conversion: 1 XP → 1 Proof, 1 Coin → 1 Bounty.

#### Streak
- Consecutive daily practice days.
- **Streak Freeze:** Consumable token to preserve streak after 1 missed day.
- **Streak Repair:** Duolingo-style paid restore (100 coins) for broken streaks; free users limited to 1/month.
- **Mastery Streak:** Consecutive days scoring ≥ 8/10. Grants milestone rewards:
  - 3 days: 1 freeze + 50 coins
  - 7 days: 1 freeze + 150 coins
  - 14 days: 2 freezes + 400 coins + 1 double_xp
  - 30 days: 3 freezes + 1000 coins + 2 double_xp + 1 skip_boss

#### Streak Multipliers
| Streak | Multiplier | Bonus XP |
|--------|-----------|----------|
| 0 | 1.0x | 0 |
| 3 | 1.2x | 10 |
| 7 | 1.5x | 50 |
| 14 | 2.0x | 100 |
| 30 | 3.0x | 300 |
| 60 | 4.0x | 500 |
| 100 | 5.0x | 1000 |

#### Combo
- Rapid-fire activities within `COMBO_WINDOW_SECONDS` increment combo counter.
- Combo multiplier scales Diamonds and coins.
- Decays after window expires.

#### Performance Bonuses
- **Precision:** Score ≥ 9 AND time ≤ 5 min → 1.25x
- **Independent:** No hint used AND score ≥ 8 → 1.5x
- **Double Diamonds Power-Up:** Time-limited 2x Diamonds (1 hour)

#### Tower / Boss System
- Levels 10, 20, 30, ..., 100 are **boss levels**.
- Boss auto-defeated when activity score ≥ boss `required_score` (default 70).
- Boss defeat bonus: `level * 10` Diamonds + `level * 5` coins.
- Bosses defeated tracked in `bosses_defeated[]`.

#### Boss Definitions
| Level | Name | Topic |
|-------|------|-------|
| 10 | Sliding Window Dragon | sliding_window |
| 20 | DP Wizard | dynamic_programming |
| 30 | Graph Knight | graph |
| 40 | System Design King | system_design |
| 50 | Interview Emperor | behavioral |
| 60 | Algorithm Overlord | algorithm |
| 70 | Data Structure God | data_structure |
| 80 | Code Lightning | optimization |
| 90 | Placement Master | all |
| 100 | The Final Boss | ultimate |

#### Forest Journey (Theming)
- 10 zones (bands of 10 levels) with nature-themed names and emojis.
- Computed from existing tower state; additive only, no stored mutations.

#### Voyage Ranks
| Tier | Min Level | Rank |
|------|-----------|------|
| 0 | 1 | Deckhand |
| 1 | 10 | Lookout |
| 2 | 25 | Navigator |
| 3 | 45 | First Mate |
| 4 | 65 | Captain |
| 5 | 85 | Fleet Admiral |

#### Badges
- 40+ badges across categories: interview, resume, aptitude, coding, streak, tower, daily, learning, powerups, company, exam_memory.
- Evaluated declaratively via `BADGE_CONDITIONS` in `gamification_core.py`.
- Stored as string IDs; hydrated on read.

#### Power-Ups
| ID | Name | Cost (coins) | Effect |
|----|------|-------------|--------|
| `extra_time` | Extra Time | 10 | +5 min on timed test |
| `hint_reveal` | Hint Reveal | 15 | Show 1 hint free |
| `retry` | Retry | 25 | One extra attempt |
| `double_xp` | Double Diamonds | 50 | 2x Diamonds 1 hour |
| `skip_boss` | Skip Boss | 75 | Skip one boss battle |
| `show_answer` | Show Answer | 100 | Reveal answer |
| `speed_boost` | Speed Boost | 8 | +30s on timed tests |
| `shield` | Shield | 30 | Block 1 wrong-answer penalty |
| `x2_coins` | Double Coins | 60 | 2x coins 1 hour |
| `auto_save` | Auto-Save | 12 | Auto-save code every 30s |
| `night_mode` | Night Mode | 5 | Dark theme |
| `focus_mode` | Focus Mode | 35 | Hide distractions 25 min |

#### Daily Login Bonus
- 7-tier escalating calendar (Duolingo-style).
- Pays out Diamonds + coins (coins unlock at tier 3+).

#### Weekly / Monthly Challenges
- Tracked in profile; progress updated inside the `record_practice` transaction.
- Weekly: problems solved, streak, aptitude 90+, interviews, hard solved.
- Monthly: problems solved, level reached, interviews, streak.

#### Immutable Reward Ledger
- Every award appends one row to `gamification_events` with inputs, outputs, and `reward_policy_version`.
- Reconciliation invariant: `profile.diamonds == sum(ledger.xp_awarded)` (modulo pre-ledger history).

---

## 5) Code Execution

### Files
- `backend/app/services/code_executor.py`
- `backend/app/services/local_sandbox.py`

### Fallback Chain
```
Piston API (primary)
  → Own compiler service / GCP Cloud Run (if COMPILER_SERVICE_URL set)
    → Remote fallbacks: Judge0 / Wandbox / Glot.io (if USE_REMOTE_FALLBACKS=true)
      → Local sandbox subprocess (if USE_LOCAL_SANDBOX=true)
```

### Circuit Breaker
- `compiler_breaker` (`threshold=5`, `recovery_time=45s`) wraps Piston calls.
- On open, falls back through the chain above.

### Piston Engine (`CodeExecutionEngine`)
- Supported languages: Python 3.10, JS 18, TS 5.0, Java 15, C++ 10.2, C 10.2, Go 1.16, Rust 1.68, Ruby 3.0, PHP 8.2, Swift 5.3, Kotlin 1.8.
- Limits: max code length 120,000 chars, max timeout 30s, max test cases 50.
- Boilerplate generation for common problem types (linked list, binary tree, graph, DP).
- `execute_against_test_cases()` runs cases in parallel (semaphore 6) or uses **local batch oracle** for Python.

### Local Sandbox (`local_sandbox.py`)
- **Oracle path for Python:** `execute_local_python_batch()` runs the submission **once** against all test cases in a single restricted subprocess.
- Function-call mode: auto-detects single top-level return-style function via AST.
- Canonical serialization contract: strings bare, bools Python-style, containers compact JSON.
- Safety:
  - Restricted builtins whitelist (no `open`, `exec`, `eval`, dangerous modules).
  - `SAFE_MODULES` set controls imports.
  - POSIX `resource` limits: 30s CPU, 256MB address space (no-ops on Windows).
  - Hard timeout via `proc.kill()`.

### JavaScript Local Sandbox
- Runs `node` with `--input-type=module --no-warnings`.
- No AST instrumentation; basic execution only.

### Execution Trace
- `generate_execution_trace()`:
  - Python: uses `execute_with_trace()` (AST instrumentation) for step-by-step trace.
  - Other languages: falls back to AI-generated trace via OpenRouter, then static fallback.

---

## 6) Payments & Billing

### Files
- `backend/app/routes/billing.py`
- `backend/app/config.py`

### Payment Processors
| Processor | Config Keys | Mode |
|-----------|-------------|------|
| PayPal | `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_MODE` | sandbox / live |
| Stripe | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` | sandbox / live |
| Razorpay | `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET` | test / live |

### Pricing Ladder
| Plan Key | Name | INR | USD |
|----------|------|-----|-----|
| `pro_monthly` | Commander | ₹99/mo | $19/mo |
| `pro_yearly` | Strategist | ₹899/yr | $99/yr |
| `lifetime` | Admiral | ₹1,499 | $149 |
| `team` | Command Squad | ₹12,250/seat/mo | $145/seat/mo |
| `team_yearly` | Command Squad (yr) | ₹1,19,900/seat/yr | $1,499/seat/yr |
| `enterprise_monthly` | Executive Suite | ₹66,392/seat/mo | $99/seat/mo |
| `enterprise_yearly` | Executive Suite (yr) | ₹6,63,920/seat/yr | $999/seat/yr |

Team: 5–50 seats minimum. Enterprise: 10+ seats minimum.

### Billing Flow
1. **Create Checkout** (`POST /api/v1/billing/checkout`):  
   - Validates coupon via `apply_coupon_service`.  
   - Creates PayPal order via `/v2/checkout/orders`.  
   - Stores `paypal_order_id` + `plan_pending` on user.  
   - Records payment as `pending`.

2. **Capture** (`POST /api/v1/billing/capture`):  
   - Captures PayPal order after user approval.  
   - On `COMPLETED`: upgrades user plan, generates invoice, marks payment `completed`.

3. **Webhooks** (`POST /api/v1/billing/webhook`):  
   - PayPal: Verifies signature via HMAC-SHA256.  
   - Handles `PAYMENT.CAPTURE.COMPLETED` and `PAYMENT.CAPTURE.DENIED`.  
   - Idempotent via `processed_webhook_events` collection (unique `provider + event_id`).  
   - Stripe: Verifies `stripe-signature` header. Handles `checkout.session.completed`.  
   - Razorpay: Verifies `x-razorpay-signature`. Handles `payment.captured` and `payment.failed`.

4. **Invoices** (`/api/v1/billing/invoices`):  
   - JSON or HTML format (`?format=html`).

### Coupon System
- `POST /api/v1/billing/coupon/validate` — validate coupon code.
- `POST /api/v1/billing/coupon/apply` — apply coupon to checkout amount.

---

## 7) Analytics & Monitoring

### Files
- `backend/app/services/analytics_service.py`
- `backend/app/services/request_metrics.py`

### Analytics Architecture

#### Event Ingestion
- `track_event(event, path, user_id, meta, ip_address)` inserts into `analytics_events`.
- IP addresses are HMAC-SHA256 hashed with JWT secret as salt for privacy.
- Each event also increments `analytics_rollups` counters for fast dashboard queries.

#### Rollups
- Buckets: `event`, `event:path:{path}`, `event:user:{user_id}`.
- Rebuilt by `refresh_rollups()` to heal missed writes.

#### Key Metrics
| Metric | Source |
|--------|--------|
| Page views | `event=page_view` |
| Feature usage | `event=feature_use` |
| Daily active users | Unique `user_id` with `page_view` today |
| Hourly distribution | `$group` by `hour` |
| New / returning users | First event in period vs. prior period |
| Geo breakdown | Top 50 IP hashes |
| Real-time stats | Today's views, active last hour, total users |

#### TTL
- `analytics_events`: 180 days.
- `analytics_rollups`: No TTL (historical).

#### Request Metrics (`request_metrics.py`)
- In-memory counters per service/outcome.
- Periodic flush to `service_metrics` every 5 minutes.
- Snapshot API for admin dashboard.

---

## 8) AI Layer

### Files
- `backend/app/services/ai_core.py`
- `backend/app/services/circuit_breaker.py`

### Primary Model
- `OPENROUTER_MODEL` (default: `google/gemma-4-31b-it:free`)
- OpenRouter API with bearer key authentication.

### Fallback Models
```python
FALLBACK_MODELS = [
    "nvidia/nemotron-3.5-lightning:free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
]
```

### Circuit Breaker
- `ai_breaker`: `threshold=5`, `recovery_time=60s`.
- `compiler_breaker`: `threshold=5`, `recovery_time=45s`.
- Async-safe with `asyncio.Lock`.
- Half-open recovery after `recovery_time` seconds.

### Request Flow
1. Check cache (SHA-256 key from messages + model, TTL 1 hour).
2. If circuit breaker closed → try primary model with retries (`MAX_RETRIES=3`, exponential backoff).
3. On failure → iterate fallback models (excluding primary).
4. Cache successful responses.

### Resilience Wrapper
- `call_with_resilience()` in `resilience.py` wraps all AI/compiler external calls with retry + circuit breaker.

### JSON Parsing
- `parse_json()` strips chain-of-thought prefixes, markdown fences, and extracts JSON by substring.
- Used by all AI-powered features to coerce model output into structured data.

---

## 9) Frontend App Shell

### Files
- `frontend/src/App.tsx`
- `frontend/src/app/AppContent.tsx`
- `frontend/src/app/AppRoutes.tsx`

### Provider Stack (inside `ErrorBoundary`)
```
ErrorBoundary
 └── ToastProvider
      └── ThemeProvider
           └── BackgroundProvider
                └── JuiceProvider
                     └── BrowserRouter
                          └── AppContent
```

### Routing Architecture
- **React Router v6** with `Routes` / `Route`.
- All page components are **lazy-loaded** via `React.lazy()` in `pages/lazy.ts`.
- Code splitting reduces initial bundle.

### Route Groups (Unified 5-Environment Model)
```
WORLD      — Learning journey, concepts, curriculum, progression
LAB        — Interactive lessons, code, experiments, debugging
ARENA      — Timed challenges, bosses, mock assessments, competitions
COMMAND    — Today, readiness, weaknesses, applications
CAREER     — Resume, interview, company preparation, application
```

### Guards
- `ProtectedRoute`: Auth required; redirects to `/login` if not authenticated.
- `OnboardingGuard`: Ensures onboarding is complete before entering main app.

### AppContent Responsibilities
- **Navbar** + **Footer** + **BottomNav** (lazy).
- **CustomCursor** overlay.
- **CookieBanner**.
- **JuiceProvider** integration: listens for `diamonds-gained`, `juice:levelup`, `juice:diamonds` events to trigger XP popups and `RewardShowcase`.
- **ComboCounter** + **ComboWarningOverlay** (visible when combo ≥ 2/3).
- **SearchModal** (`Cmd/Ctrl+K` toggle).
- **Page tracking**: `usePageTracking` fires `gtag` page_view + `POST /api/v1/analytics/track` on route change.
- **RouteErrorBoundary** wraps `AnimatedRoutes`.

### Legacy Redirects
Extensive `Navigate` rules preserve old URLs (e.g. `/dashboard`, `/profile`, `/journey`, `/learn/:slug`) by redirecting to new environment routes.

### State
- Global auth state via **Zustand** (`store/authStore.ts`).
- `useGamificationData` hook reads gamification state.
- No client-side XP/level computation — frontend renders exactly what the server returns.

---

## Cross-Cutting Concerns Summary

| Concern | Pattern | Key File(s) |
|---------|---------|-------------|
| **Auth** | JWT + httpOnly cookies, refresh rotation, admin email bypass | `middleware/auth.py`, `routes/auth.py` |
| **DB** | Motor async, lazy proxies, index-on-startup, TTL indexes | `database.py` |
| **Trust** | File-resident bank, in-memory serving, quarantine sticky, no Mongo question content | `services/question_store.py`, `services/auto_verify.py` |
| **Gamification** | Single writer `record_practice()`, immutable ledger, level from Diamonds only | `services/gamification.py`, `services/gamification_core.py` |
| **Execution** | Piston → GCP → Remote → Local sandbox, circuit breaker, batch oracle | `services/code_executor.py`, `services/local_sandbox.py` |
| **Billing** | PayPal / Stripe / Razorpay checkout + capture + webhook idempotency | `routes/billing.py` |
| **Analytics** | Raw events + rollup counters, IP hash, TTL cleanup | `services/analytics_service.py`, `services/request_metrics.py` |
| **AI** | OpenRouter primary + 6 fallbacks, circuit breaker, 1h cache, resilient retry | `services/ai_core.py`, `services/circuit_breaker.py` |
| **Frontend** | Lazy routes, 5-environment routing, juice/gamification overlays, analytics tracking | `App.tsx`, `app/AppContent.tsx`, `app/AppRoutes.tsx` |
