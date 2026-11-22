# 01_CURRENT_STATE.md — BountyCode Architecture Audit

> **Source of Truth**: `docs/BOUNTYCODE_VISION_LOCK.md` and `docs/PRD_SERVICE_BASED_V1.md`
> **Audit Date**: 2026-11-20
> **Auditor**: Principal Architect (Kilo)

---

## Executive Summary

Bountycode is a modular monolith (FastAPI + MongoDB + React) with 115 backend route files, 128 frontend page files, and ~100 frontend routes. The platform implements the full placement-preparation lifecycle (onboarding → diagnostic → plan → lesson → practice → assessment → evidence → repair → retest → readiness), but critical architectural issues exist:

1. **Duplicate question-serving ownership** between `question_store.py` and `quiz_service.py`
2. **Multiple curriculum/world registries** with no single canonical source
3. **Duplicated gamification constants** between `gamification.py` and `gamification_core.py`
4. **Inconsistent skill ID namespaces** across 6+ subsystems (mitigated by `skill_taxonomy.py`)
5. **Inconsistent question trust states** (`TRUSTED`, `verified`, `reviewed`, `automated_checked`)

---

## 1. Module Inventory

### Backend (Python/FastAPI)

| Layer | Count | Location |
|-------|-------|----------|
| Route files | 115 | `backend/app/routes/` |
| Service files | ~140 | `backend/app/services/` |
| Data files | ~20+ | `backend/app/data/` |
| Content files | ~15+ | `backend/app/content/` |
| Middleware files | 6 | `backend/app/middleware/` |
| Models | 3 | `backend/app/models/` |

### Frontend (React 18 + Vite + TypeScript)

| Layer | Count | Location |
|-------|-------|----------|
| Page files | 128 | `frontend/src/pages/` |
| API modules | 39 | `frontend/src/services/api/` |
| Component files | ~94 | `frontend/src/components/` |
| Routes (App.tsx) | ~100+ | `frontend/src/App.tsx` |

---

## 2. Actual Dependencies & Duplicate Ownership

### 2.1 Question Serving — DUPLICATE OWNERSHIP (CRITICAL)

| Component | File | Lines | Owns Question Loading? |
|-----------|------|-------|------------------------|
| Question Store | `app/services/question_store.py` | 2178 | YES — canonical loader, trust gating, `_is_servable()` |
| Quiz Service | `app/services/quiz_service.py` | ~800 | YES — independent `QUESTION_FILES` list, `_load_questions()`, per-module caches |
| Adaptive Quiz Composer | `app/services/adaptive_quiz_composer.py` | ? | Selects from supplied pools (consumer, not owner) |

**Issue**: `quiz_service.py` maintains its own `QUESTION_FILES` list, `_load_questions()` function, and in-memory caches (`_questions_cache`, `_questions_by_id`, etc.), completely independent of `question_store.py`. This violates the single-ownership rule.

**Evidence**: `quiz_service.py` lines 1-~100 contain `QUESTION_FILES = [...]`, `_load_questions()`, `_questions_cache`, `_questions_by_id`, `_questions_by_topic`, `_questions_by_difficulty`, `_questions_by_company`, and `clear_cache()`.

**Resolution**: `quiz_service.py` must delegate all question loading to `question_store.py` via `_servable_questions()` / `find_one_verified()`.

### 2.2 Curriculum/World Registries — MULTIPLE REGISTRIES

| Registry | File | Purpose | Canonical? |
|----------|------|---------|------------|
| World Registry | `app/data/worlds_data.py` | 12 worlds, level-based learning | YES (worlds) |
| Curriculum Base | `app/data/curriculum.py` | Language curricula (7 languages × 50 levels) | Partial |
| Curriculum 50 Levels | `app/data/curriculum_50_levels.py` | 50-level progression | Duplicate |
| Curriculum Web | `app/data/curriculum_web.py` | Web development curriculum | Duplicate |
| Curriculum Depth | `app/data/curriculum_depth.py` | Deep-dive curriculum | Duplicate |
| Curriculum Enrichment | `app/data/curriculum_enrichment.py` | Enrichment patches | Patches base |
| Curriculum World Class | `app/data/curriculum_world_class.py` | World-class curriculum | Duplicate |
| Capability Curriculum | `app/data/capability_curriculum.py` | Capability-based curriculum | Duplicate |
| Lesson Registry | `app/content/curriculum/registry.py` | Lesson slug → content dict | Partial |

**Issue**: 8+ curriculum files with overlapping lesson data. No single canonical curriculum registry.

**Resolution**: Consolidate into one canonical curriculum registry with versioned lesson content.

### 2.3 Gamification — DUPLICATED CONSTANTS

| Component | File | Lines | Content |
|-----------|------|-------|---------|
| Gamification | `app/services/gamification.py` | 2284 | TOUER_TITLES, BOSS_BATTLES, FOREST_ZONES, BADGES, record_practice() |
| Gamification Core | `app/services/gamification_core.py` | 786 | TOUER_TITLES (duplicated), COMPANY_TITLE_BANDS, pure math helpers |

**Issue**: `TOWER_TITLES` is defined identically in both files. `gamification_core.py` docstring says "copied verbatim from the original gamification module."

**Resolution**: `gamification.py` should import constants from `gamification_core.py`, not duplicate them.

### 2.4 Skill ID Namespaces — 6+ INCOMPATIBLE SCHEMES (MITIGATED)

| Subsystem | File | Naming Scheme |
|-----------|------|---------------|
| Adaptive Learning | `app/services/adaptive_learning.py` | `SKILL_DOMAINS` (arrays_hashing, trees, dp, ...) |
| Skill Assessment | `app/services/skill_assessment.py` | `SKILL_CATEGORIES` (dsa→arrays, aptitude→quantitative, ...) |
| Readiness Engine | `app/services/readiness_engine.py` | `CATEGORY_WEIGHTS` (dsa, aptitude, cs_fundamentals, ...) |
| OA | `app/routes/oa.py` | Section names (aptitude, logical, verbal, coding, ...) |
| Interview | `app/routes/interview.py` | Dimension names (technical, communication, ...) |
| SRS | `app/services/spaced_repetition.py` | `DSA_CONCEPTS` (arrays, linked-lists, ...) |

**Mitigation**: `skill_taxonomy.py` (502 lines) establishes canonical `domain.subskill` namespace with reverse index and explicit synonym maps for all 6 source systems.

**Status**: Partially resolved — `skill_taxonomy.py` exists but needs to be adopted by all subsystems.

---

## 3. Dead Code Candidates

From the August 2026 cleanup, 60+ experimental features were removed. Remaining candidates for review:

- `backend/app/data/curriculum_rust.py`, `curriculum_go.py`, `curriculum_csharp.py`, `curriculum_typescript.py` — language-specific curricula, may be unused
- `backend/app/data/capability_curriculum.py` — may duplicate `curriculum.py`
- `backend/app/data/curriculum_world_class.py` — may duplicate `curriculum_world_class.py` in content/
- Frontend pages with `Navigate to` redirects — may be dead after cleanup

---

## 4. Missing Implementations

| Feature | Status | Notes |
|---------|--------|-------|
| Central AI gateway | MISSING | AI calls scattered across `ai.py`, `ai_*.py` modules |
| Single reward ledger | PARTIAL | `record_practice()` is the single XP writer (gamification.py), but no immutable event ledger enforcement |
| Explicit router registry | MISSING | Dynamic `pkgutil` discovery in `main.py` |
| Route-to-API-to-engine mapping | MISSING | No documentation |
| Architecture tests | MISSING | No tests detecting forbidden imports or duplicate ownership |
| Dashboard read-model | PARTIAL | `analytics.py` provides overview, no unified dashboard endpoint |
| Company blueprint registry | PARTIAL | `company_blueprints.json` exists, not fully integrated |

---

## 5. Existing APIs (Backend Route Inventory)

Key route files and their prefixes:

| Route File | Prefix | Key Responsibility |
|-----------|--------|-------------------|
| `auth.py` | `/api/v1/auth` | Register, login, onboarding, password reset |
| `interview.py` | `/api/v1/interview` | AI interview flow |
| `resume.py` | `/api/v1/resume` | Upload, generate, optimize, export |
| `coding.py` | `/api/v1/coding` | Coding challenges |
| `compiler.py` | `/api/v1/compiler` | Code execution via Piston |
| `questions.py` | `/api/v1/questions` | Question bank browse, solve, submit |
| `questions_solve.py` | `/api/v1/questions` | Submit code, run hidden test cases |
| `gamification.py` | `/api/v1/gamification` | XP, tower, badges, leaderboard, readiness |
| `worlds.py` | `/api/v1/worlds` | World progression, level completion |
| `lesson.py` | `/api/v1/lesson` | Lesson content, step completion |
| `oa.py` | `/api/v1/oa` | Mock online assessment |
| `readiness.py` | `/api/v1/readiness` | Readiness score |
| `repair.py` | `/api/v1/repair` | Repair missions, retest |
| `company_prep.py` | `/api/v1/company` | Company-specific prep |
| `company_tracks.py` | `/api/v1/company-tracks` | Company tracks |
| `aptitude.py` | `/api/v1/aptitude` | Aptitude test |
| `srs.py` | `/api/v1/srs` | Spaced repetition |
| `daily_challenge.py` | `/api/v1/daily-challenge` | Daily missions |
| `onboarding.py` | `/api/v1/onboarding` | Onboarding flow |
| `target.py` | `/api/v1/target` | Target company selection |
| `path_generator.py` | service | Deterministic next-action |

---

## 6. Frontend Route Inventory (App.tsx)

Primary navigation hubs present:
- `/dashboard` — Student dashboard
- `/practice` — Practice hub
- `/mock-oa` — Mock online assessment
- `/interview` — AI interview
- `/company-tracks` → `/skills` (redirected)
- `/profile` → `/dashboard` (redirected)

Learning routes:
- `/learn/:languageId` — Learning hub
- `/lessons/:lessonId` — Lesson player
- `/skills` — Skill map

Question bank:
- `/question-bank` — Browse
- `/question-bank/:questionId` — Practice mode
- `/solve/:id` — Solve problem

Assessment:
- `/aptitude` — Aptitude test
- `/daily-challenge` — Daily challenge
- `/coding` — Coding challenge
- `/daily-drill` → `/tower` (redirected)

Gamification:
- `/tower` — Tower dashboard
- `/gamification` — Gamification dashboard

Career:
- `/resume`, `/ats`, `/cover-letter`, `/career-profile`, `/applications`

Admin:
- `/admin` — Admin dashboard

Removed-page redirects: `/academy`, `/journey`, `/profile`, `/rank`, `/company-prep`, `/company-tracks`, `/quiz`, `/levels`, etc.

---

## 7. Database Collections (MongoDB)

Key collections (from `database.py`):

| Collection | Purpose |
|------------|---------|
| `users` | User profiles, auth state |
| `gamification_collection` | XP, level, streak, badges |
| `gamification_events_collection` | Immutable reward events |
| `skill_graph_collection` | Skill mastery state |
| `srs_cards_collection` | Spaced repetition cards |
| `academy_learner_profiles` | Learner profiles, onboarding status |
| `academy_diagnostic_sessions` | Diagnostic attempts |
| `academy_learning_plans` | Generated learning plans |
| `telemetry_events` | Observability events |
| `lesson_progress` | Lesson completion state |
| `question_answers_collection` | Question attempt history |

Note: Question content is NOT stored in MongoDB (residency rule enforced).

---

## 8. External Providers

| Provider | Purpose | Integration |
|----------|---------|-------------|
| OpenRouter → Gemini 2.0 Flash | Primary AI model | `services/ai.py` with circuit breaker |
| Llama 3.1, Phi-3 Mini, DeepSeek | Fallback AI models | Circuit breaker with 4 fallbacks |
| Piston API | Code execution | `services/code_executor.py` |
| Docker sandbox | Alternative code execution | `services/docker_sandbox.py` |
| Local sandbox | Fallback code execution | `services/local_sandbox.py` |
| Redis | Cache layer | `services/cache.py` (Redis → in-memory fallback) |
| PayPal, Razorpay, Stripe | Payments | `services/billing.py` |

---

## 9. CI Pipeline

`.github/workflows/ci.yml`:

| Job | Steps |
|-----|-------|
| `backend` | Checkout, Python 3.12, install deps, compileall, pytest, alembic check |
| `frontend` | Checkout, Node 22, lockfile reconcile, npm ci, typecheck, build |
| `curate-questions` | Weekly (schedule), re-curate question bank via scripts |

**Issues**: No MongoDB/Redis services in CI, all tests run together (no stage separation), no MongoDB test database isolation.

---

## 10. Known Architectural Issues

| # | Issue | Severity | Location |
|---|-------|----------|----------|
| 1 | Duplicate question loading in `quiz_service.py` vs `question_store.py` | CRITICAL | `quiz_service.py`, `question_store.py` |
| 2 | Multiple curriculum registries with overlapping data | HIGH | `app/data/curriculum*.py` |
| 3 | Duplicated `TOWER_TITLES` in `gamification.py` and `gamification_core.py` | MEDIUM | `gamification.py`, `gamification_core.py` |
| 4 | Dynamic router discovery (no explicit registry) | MEDIUM | `main.py` |
| 5 | No architecture tests for forbidden imports/duplicate ownership | MEDIUM | None |
| 6 | 6+ skill ID namespaces (mitigated by `skill_taxonomy.py`) | MEDIUM (mitigated) | 6 subsystem files |
| 7 | Inconsistent question trust states | MEDIUM | `question_store.py` |
| 8 | No central AI gateway | MEDIUM | `ai.py`, `ai_*.py` scattered |
| 9 | CI lacks MongoDB/Redis services, no stage separation | MEDIUM | `.github/workflows/ci.yml` |

---

## 11. Compliance with AGENTS.md Laws

| Law | Status | Evidence |
|-----|--------|----------|
| Single XP writer (`record_practice()`) | COMPLIANT | `gamification.py:624` docstring |
| Content trust pipeline (UNVERIFIED→AUTOMATED_CHECKED→HUMAN_REVIEWED→TRUSTED) | PARTIAL | `question_store.py` has trust tiers |
| Question residency (files, not MongoDB) | COMPLIANT | `question_store.py` loads from files |
| No-LLM bank rule | COMPLIANT | No LLM in question bank |
| Server-authoritative timing | PARTIAL | OA uses `started_at`/`ends_at` |
| Idempotency on writes | PARTIAL | `complete_level` uses atomic `find_one_and_update` |
| Badges as string IDs | COMPLIANT | `gamification_core.py` |

---

## Next Steps

1. Create ADRs for each conflict (world count, trust states, reward ownership, registries)
2. Phase 1: Explicit router registration + OpenAPI contract
3. Phase 2: Unified question & quiz pipeline (question_store as canonical owner)
4. Phase 3: Learning orchestration
5. Phase 4: AI gateway
6. Phase 5: Gamification single reward ledger
7. Phase 6: Frontend route catalog
8. Phase 7: Performance hardening & CI acceptance gates
