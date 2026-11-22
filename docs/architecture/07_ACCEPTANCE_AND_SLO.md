# 07_ACCEPTANCE_AND_SLO.md — Acceptance Criteria and SLOs

> Functional, performance, reliability, security, and product acceptance criteria. "Verified" means a pasted response body, a screenshot, or a test that asserts on real output. Compile-passes and route-imports are not evidence.

---

## Functional Acceptance Criteria

| # | Criterion | Evidence Required |
|---|-----------|-------------------|
| F1 | One canonical question-serving boundary | Test: `quiz_service.py` does not call `glob()` or scan question directories |
| F2 | Question trust gate | Test: `_is_servable(q)` returns False for `needs_review`, `quarantined`, `unverified` |
| F3 | Quiz determinism | Test: Same learner state + seed → identical quiz (100% match) |
| F4 | Single XP writer | Test: No direct `$inc`/`$set` on XP fields outside `record_practice()` |
| F5 | Reward ledger reconciliation | Test: `profile.xp == sum(gamification_events)` for all users |
| F6 | No answer key leakage | Test: Client response never contains `correct_index`, `correct_answer`, `solution` |
| F7 | Server-authoritative timing | Test: Late OA submission returns 410 |
| F8 | Idempotent writes | Test: Concurrent double-tap awards XP once |
| F9 | AI privacy | Test: PII (email, phone, card) stripped from AI messages |
| F10 | AI doesn't own mastery | Test: AI response never modifies skill_graph or readiness |
| F11 | No duplicate routes | Test: `validate_no_duplicate_paths()` returns empty |
| F12 | All routes registered | Test: Startup fails if any required router missing |
| F13 | Full learner E2E | Test: signup → onboarding → diagnostic → plan → lesson → assessment → evidence → repair → retest → readiness |
| F14 | Frontend route integrity | Test: Every `<Route>` path has a corresponding backend API |
| F15 | Mobile responsive | Test: Core journey renders on 375px width |

---

## Performance SLOs

| Metric | Target | Measurement |
|--------|--------|-------------|
| API p50 latency | < 100ms | Request metrics |
| API p95 latency | < 500ms | Request metrics |
| API p99 latency | < 2s | Request metrics |
| Quiz generation | < 2s | Test assertion |
| Lesson load | < 500ms | Test assertion |
| Readiness calculation | < 1s | Test assertion |
| Frontend bundle size | < 2MB | `npm run build` output |
| Time to interactive | < 3s | Lighthouse |
| Database query p95 | < 100ms | MongoDB profiler |
| AI response p95 | < 10s | AI gateway metrics |
| AI fallback activation | < 5% of requests | Circuit breaker metrics |

---

## Reliability SLOs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Uptime | 99.9% | Health check endpoint |
| Error rate | < 1% | Request metrics |
| Duplicate event suppression | 100% | Test assertion |
| Idempotency collisions | 0 | Test assertion |
| Circuit breaker recovery | < 60s | Circuit breaker metrics |
| Cache hit rate | > 80% | Cache stats |

---

## Security SLOs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Answer key leakage | 0 instances | Test assertion + manual audit |
| PII in AI requests | 0 instances | Test assertion + audit |
| Unauthenticated access to protected routes | 0 instances | Test assertion |
| Rate limit triggers | < 0.1% of requests | Rate limiter metrics |
| Login lockout events | < 0.1% of logins | Auth middleware metrics |

---

## Product Acceptance (Beta)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Onboarding completion | > 70% | Funnel metrics |
| Time to first lesson | < 5 minutes | Funnel metrics |
| Diagnostic completion | > 80% | Funnel metrics |
| First assessment completion | > 60% | Funnel metrics |
| Repair mission acceptance | > 50% | Funnel metrics |
| Retest completion | > 40% | Funnel metrics |
| Retest improvement | > 15% avg score gain | Assessment comparison |
| Readiness report views | > 30% of users | Funnel metrics |
| 7-day retention | > 30% | Analytics |
| Empty recommendation rate | < 5% | Algorithm health metrics |
| Duplicate recommendation rate | < 5% | Algorithm health metrics |

---

## Test Suite Requirements

| Stage | Command | Must Pass |
|-------|---------|-----------|
| Unit | `make test-backend-unit` | 100% |
| Integration | `make test-backend-integration` | 100% |
| E2E | `make test-e2e` | 100% |
| Content | `make test-content` | 100% |
| Frontend | `make test-frontend` | 100% |

---

## CI Gate

A merge is blocked when:
- Any test stage fails
- `validate_no_duplicate_paths()` returns errors
- `compileall` fails
- `npm run typecheck` fails
- `npm run build` fails

---

## Non-Negotiable Rules (from AGENTS.md)

1. Only `record_practice()` writes XP/coins/stars/streak/combo/badges
2. Callers pass 0-10 pedagogical score; engine normalizes 0-100%
3. Ship position, stars, level derive from server state — never client
4. Every award appends one immutable `gamification_events` row
5. `profile.xp == sum(ledger)` must reconcile
6. Badges stored as string IDs, hydrated on read
7. Question content never in MongoDB — files only
8. No LLM in question bank (authoring, tagging, grading, attribution)
9. "Verified" means pasted response body or test with real numbers
