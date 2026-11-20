# ADR-004: Quiz Service Question Loading — Canonical Owner

## Status
Proposed

## Context

`quiz_service.py` maintains its own question-loading infrastructure completely independent of `question_store.py`:

| Component | File | Lines | Loading Mechanism |
|-----------|------|-------|-------------------|
| Question Store | `app/services/question_store.py` | 2178 | `_load_all()`, `_servable_questions()`, `find_one_verified()`, trust gating |
| Quiz Service | `app/services/quiz_service.py` | ~800 | `QUESTION_FILES` list, `_load_questions()`, per-module caches, `clear_cache()` |

`quiz_service.py` has:
- `QUESTION_FILES = [...]` — hardcoded JSON file paths
- `_questions_cache`, `_questions_by_id`, `_questions_by_topic`, `_questions_by_difficulty`, `_questions_by_company` — in-memory caches
- `_load_questions()` — loads and deduplicates questions
- `clear_cache()` — cache management

This violates the single-ownership rule: question content must flow through `question_store.py` only.

## Decision

**Canonical question owner**: `question_store.py` is the single owner of question loading, validation, trust state, and provenance.

**Quiz service dependency**: `quiz_service.py` delegates all question loading to `question_store.py` via:
- `_servable_questions()` — returns trust-gated question pool
- `find_one_verified()` — fetches one verified question by ID
- `load_all()` — ensures questions are loaded

**Removed from `quiz_service.py`**:
- `QUESTION_FILES` list
- `_load_questions()` function
- `_questions_cache`, `_questions_by_id`, etc. caches
- `clear_cache()` function

**Trust gate**: `quiz_service.py` must use `_is_servable(q)` from `question_store` to filter questions. Only `verified` + executable questions are servable.

## Rationale

- `question_store.py` already implements the complete trust pipeline (load → normalize → trust stamp → dedupe → serve)
- `question_store.py` caches `load_all()` via `_loaded` flag (no reload per request)
- `question_store.py` already has `_is_servable()` which correctly enforces verified+executable only
- Duplication creates risk of inconsistent question pools between quiz modes

## Migration Plan

1. Refactor `quiz_service.py` to remove independent loading (already partially done in RC1)
2. Replace all `_load_questions()` calls with `_servable_questions()` from `question_store`
3. Replace `get_question_by_id()` to use `question_store.find_one_verified()`
4. Add architecture test that fails if `quiz_service.py` or any production service calls `glob()` for question files or recursively scans question directories
5. Add architecture test that verifies same learner state + seed → same quiz (reproducibility)

## Quiz Session Reproducibility

For every quiz, persist:
- `question_bank_version`
- `blueprint_version`
- `composer_version`
- `selection_seed`
- `selection_policy`

This makes quiz results reproducible and auditable.

## Consequences

- Positive: Single question-serving boundary, consistent trust gating, reproducible quizzes
- Negative: `quiz_service.py` refactoring required, tests that monkeypatch `_load_questions()` must be updated

## References

- `docs/AGENTS.md` — Question Bank Residency Rule, No-LLM Bank Rule
- `app/services/question_store.py` — `_servable_questions()`, `find_one_verified()`, `_is_servable()`
- `app/services/quiz_service.py` — Quiz construction
- `docs/architecture/01_CURRENT_STATE.md` — Issue #1
