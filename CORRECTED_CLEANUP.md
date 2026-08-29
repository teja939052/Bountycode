# BOUNTYCODE — CORRECTED CLEANUP CLASSIFICATION

**Date:** 2026-08-29
**Branch:** architecture-cleanup
**Tag:** pre-cleanup-baseline (safety net)

---

## PHASE 1: SAFE TO DELETE (0 external references)

These files have ZERO imports from other files. Safe to delete immediately.

| File | References | Evidence |
|------|-----------|----------|
| `routes/curriculum_engine.py` | 0 | No imports found |
| `routes/learning_journeys.py` | 0 | No imports found |
| `routes/predictor.py` | 0 | No imports found |
| `services/progression_systems.py` | 0 | No imports found |
| `services/quest_engine.py` | 0 | No imports found |

**Action:** Delete all 5.

---

## PHASE 2: CONDITIONAL DELETE (refs only from Phase 1 candidates)

These files are ONLY referenced by files being deleted in Phase 1.

| File | References | Referenced By | Action |
|------|-----------|---------------|--------|
| `routes/readiness.py` | 1 | `curriculum_engine.py` (Phase 1) | Delete AFTER Phase 1 |
| `services/job_readiness.py` | 2 | `curriculum_engine.py` (Phase 1), `readiness_engine.py` | Merge into `readiness_engine.py` AFTER Phase 1 |

---

## PHASE 3: MERGE REQUIRED (active references, overlapping responsibility)

These files have active references AND overlap with canonical systems. Must merge, not delete.

| File | References | Overlaps With | Action |
|------|-----------|---------------|--------|
| `routes/srs.py` | 4 | `study_engine.py` | Merge routes into study_engine, delete file |
| `services/spaced_repetition.py` | 2 | `srs_engine.py` | Merge unique functions into srs_engine, delete file |
| `services/curriculum_connector.py` | MANY | `world_registry.py` | Analyze: keep if unique, merge if duplicate |
| `services/lesson.py` | MANY | `lesson_definitions.py` | Analyze: likely has unique lesson content, keep or merge |
| `services/learning.py` | 100+ | Core infrastructure | KEEP — not a duplicate, heavily used |

---

## CORRECTED CLASSIFICATION SUMMARY

| Classification | Count | Files |
|---------------|-------|-------|
| **SAFE DELETE** | 5 | curriculum_engine, learning_journeys, predictor, progression_systems, quest_engine |
| **CONDITIONAL DELETE** | 2 | readiness (after Phase 1), job_readiness (merge into readiness_engine) |
| **MERGE REQUIRED** | 3 | srs routes, spaced_repetition, curriculum_connector |
| **KEEP** | 2 | lesson.py (unique content), learning.py (core infrastructure) |

---

## EXECUTION ORDER

1. Delete Phase 1 files (5 files)
2. Verify: compileall, boot, route enumeration
3. Delete Phase 2 files (2 files)
4. Verify: compileall, boot, route enumeration
5. Merge Phase 3 files (3 files)
6. Verify: compileall, boot, route enumeration, typecheck, build
7. Remove dead MongoDB collections
8. Clean up frontend pages
9. Final verification

---

## LESSON LEARNED

Initial audit incorrectly classified `services/learning.py` as duplicate.
Actual reference count: 100+ imports across routes, services, data files.
It is core infrastructure, NOT a duplicate.

Always verify references before classifying.
