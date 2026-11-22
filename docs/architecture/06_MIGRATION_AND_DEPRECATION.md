# 06_MIGRATION_AND_DEPRECATION.md — Migration and Deprecation

> Obsolete code, replacement modules, backward compatibility, and safe removal. No mass deletion — every removed feature has a reason and replacement.

---

## Deprecation Lifecycle

```
Active
  ↓
Replacement Identified
  ↓
Compatibility Adapter
  ↓
Deprecated (warning logged)
  ↓
No Active Consumers
  ↓
Tests + Migration Verified
  ↓
Safe Removal
```

---

## Candidates for Deprecation

| Module | Issue | Replacement | Status |
|--------|-------|-------------|--------|
| `quiz_service.py` `_load_questions()` | Independent question loader | `question_store._servable_questions()` | Fixed (ADR-004) |
| `quiz_service.py` `clear_cache()` | Per-module cache | `question_store.load_all()` (cached) | Fixed (ADR-004) |
| `gamification.py` duplicated constants | `TOWER_TITLES`, `BOSS_BATTLES`, etc. duplicated | `gamification_core.py` | Planned (ADR-003) |
| `observability.py` prefix `/observability` | Inconsistent (no `/api/v1/`) | `/api/v1/observability` | Planned |
| `cover_letter.py` prefix `/api/v1/tools` | Inconsistent naming | `/api/v1/cover-letter` | Planned |
| `ai_feedback.py` prefix `/api/v1/feedback` | Inconsistent naming | `/api/v1/ai-feedback` | Planned |
| `free_practice.py` prefix `/api/v1/free` | Inconsistent naming | `/api/v1/free-practice` | Planned |
| `daily_challenge.py` prefix `/api/v1/daily` | Conflicts with `/api/v1/daily-challenge` | Use `/api/v1/daily-challenge` only | Planned |
| `curriculum_*.py` (8 files) | Multiple curriculum registries | `registry.py` + `worlds_data.py` | Planned (ADR-001) |
| `interview.py` vs `mock_interview.py` | Duplicate `/api/v1/interview` routes | Consolidate into one module | Planned |
| `mock_interview.py` internal duplicate routes | Same route defined twice | Remove duplicates | Bug fix |

---

## Migration Steps

### Phase 1: Documentation Only (No Breaking Changes)

1. Add deprecation warnings to modules slated for removal
2. Document replacement modules in ADRs
3. Add architecture tests that flag usage of deprecated modules
4. Update `main.py` to use explicit router registry (done)

### Phase 2: Compatibility Adapters

1. Add import aliases: `from app.services.quiz_service import _load_questions` → raises DeprecationWarning, delegates to `question_store`
2. Add prefix normalization middleware: redirect `/api/v1/tools` → `/api/v1/cover-letter`, etc.
3. Add route compatibility aliases in frontend App.tsx (done for removed pages)

### Phase 3: Safe Removal

1. Verify zero consumers of deprecated module
2. Run full test suite
3. Remove module
4. Update ADR with removal date

---

## Backward Compatibility Rules

1. **No breaking API contracts without compatibility layer** — old paths return 301 redirect to new paths for 1 release cycle
2. **No silent data migration** — all migrations logged, reversible
3. **Preserve user data** — historical attempts, reward balances, progress, question IDs, URLs never changed
4. **Frontend redirects** — all removed routes have `<Navigate to="/new-path" replace />` in App.tsx

---

## Rollback Plan

Each migration includes:
- Pre-migration backup of affected MongoDB collections
- Feature flag to toggle new behavior on/off
- Rollback script to restore previous state
- Test suite must pass before and after migration
