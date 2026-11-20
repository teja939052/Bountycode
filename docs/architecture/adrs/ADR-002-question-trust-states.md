# ADR-002: Question Trust State Consolidation

## Status
Proposed

## Context

The codebase uses multiple inconsistent question trust states:

| Trust State | Meaning | Servable? | Source |
|-------------|---------|-----------|--------|
| `verified` | Human-reviewed through trust lifecycle | Yes | `question_store.py` |
| `reviewed` | Human-reviewed | Yes | `question_store.py` |
| `automated_checked` | Passed deterministic execution | Yes (learning only) | `question_store.py` |
| `needs_review` | Fails validation | No | `question_store.py` |
| `quarantined` | Execution-broken | No | `question_store.py` |
| `unverified` | Raw import | No | `question_store.py` |
| `TRUSTED` | Fully verified (Vision Lock terminology) | Yes | Vision Lock only |

The Vision Lock uses `TRUSTED` as the final tier in the pipeline:
```
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED
```

But `question_store.py` uses different tier names (`verified`, `reviewed`, `automated_checked`, `needs_review`, `quarantined`, `unverified`).

## Decision

**Canonical trust states** (aligned with Vision Lock pipeline):

| State | Code Value | Servable | Readiness Weight |
|-------|-----------|----------|-----------------|
| UNVERIFIED | `unverified` | No | 0.0 |
| AUTOMATED_CHECKED | `automated_checked` | Yes (learning only) | 0.5 |
| HUMAN_REVIEWED | `reviewed` | Yes | 0.85 |
| TRUSTED | `verified` | Yes | 1.0 (high-stakes) |

Non-servable states: `needs_review`, `quarantined`

**Rule**: Only `verified` (TRUSTED) and `reviewed` (HUMAN_REVIEWED) questions are servable to students. `automated_checked` is servable for learning only, never for assessment. `needs_review`, `quarantined`, `unverified` are never served.

**API terminology**: External APIs use `TRUSTED` / `HUMAN_REVIEWED` / `AUTOMATED_CHECKED` / `UNVERIFIED`. Internal code uses `verified` / `reviewed` / `automated_checked` / `unverified`. Mapping layer converts between the two.

## Rationale

- The Vision Lock pipeline is the product standard
- `question_store.py` already implements the trust gating logic correctly
- The tier names differ but the semantics align
- Consistency between internal implementation and external documentation

## Migration Plan

1. Add a mapping function in `question_store.py` between internal state names and Vision Lock pipeline names
2. Update all API responses to use Vision Lock terminology (`TRUSTED`, etc.)
3. Add architecture test that verifies only `verified`/`reviewed` questions pass `_is_servable()`
4. Update documentation to reference consistent terminology

## Consequences

- Positive: Clear alignment between product vision and implementation
- Negative: Requires updating all code that references trust states

## References

- `docs/BOUNTYCODE_VISION_LOCK.md` — Content Trust Pipeline
- `app/services/question_store.py` — `_is_servable()`, trust tiers
- `docs/architecture/01_CURRENT_STATE.md` — Issue #7
