# ADR-003: Gamification Reward Ownership — Single Canonical Writer

## Status
Proposed

## Context

The gamification system has duplicated constants and potential ownership ambiguity:

| Component | File | Lines | Responsibility |
|-----------|------|-------|----------------|
| Gamification | `app/services/gamification.py` | 2284 | TOUER_TITLES, BOSS_BATTLES, FOREST_ZONES, BADGES, record_practice() |
| Gamification Core | `app/services/gamification_core.py` | 786 | TOUER_TITLES (duplicated), COMPANY_TITLE_BANDS, pure math helpers |

`gamification_core.py` docstring states: "copied verbatim from the original gamification module."

The Gamification Law (AGENTS.md) states:
1. The only writer of XP, coins, stars, streak, combo, badges is `record_practice()` (plus `spend_xp()` for shop debits)
2. Every award appends one immutable `gamification_events` row
3. `profile.xp == sum(ledger)` must reconcile

## Decision

**Canonical reward writer**: `record_practice()` in `app/services/gamification.py` is the single writer of all gamification state.

**Constant deduplication**: `gamification.py` imports `TOWER_TITLES`, `COMPANY_TITLE_BANDS`, and all pure math from `gamification_core.py`. No constants are defined in `gamification.py`.

**Event ledger**: Every award writes one immutable `gamification_events` row (inputs, outputs, `reward_policy_version`). This is already implemented via `gamification_events_collection`.

**Enforcement**: Architecture test verifies:
- No direct `$inc`/`$set` on XP fields outside `record_practice()` and `spend_xp()`
- Every reward creates a `gamification_events` row
- `profile.xp` reconciles with `sum(ledger)`

## Rationale

- `gamification_core.py` is already designed as a LEAF module (imports nothing from `gamification.py`)
- The Gamification Law already establishes `record_practice()` as the single writer
- The event ledger already exists but needs enforcement testing

## Migration Plan

1. Remove duplicated `TOWER_TITLES` from `gamification.py`, import from `gamification_core.py`
2. Remove all other duplicated constants from `gamification.py`
3. Add architecture test for Gamification Law compliance
4. Verify `gamification_events_collection` writes are atomic with state changes

## Consequences

- Positive: Single source of truth for gamification math, enforceable invariants
- Negative: Refactoring `gamification.py` (2284 lines) is extensive

## References

- `docs/AGENTS.md` — Gamification Law
- `app/services/gamification.py` — `record_practice()`
- `app/services/gamification_core.py` — Pure math helpers
- `app/database.py` — `gamification_events_collection`
