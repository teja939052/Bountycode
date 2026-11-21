# Bountycode cleanup & content integrity — progress

## Incident
`question_store.py` was corrupted during a large push. See
`CRITICAL_QUESTION_STORE_RESTORE.md` and restore from commit `cb871f5` before deploy.

## Completed (safe)
1. Source-of-truth map: `docs/research/RUNTIME_SOURCE_OF_TRUTH.md`
2. Governance registry: dual ownership + service OA + offline artifacts
3. Inventory script: `backend/scripts/audit_question_inventory.py`
4. Original coding supplement: `original_coding_verified.json` (5 problems with tests)
5. Service OA curated path + quality policy (earlier commits)
6. Sprint / Study Engine wiring (earlier commits)

## Trust model (intended)
- `automated_checked` ≠ student-servable
- Student path requires `verified`/`reviewed` + executable
- Do not label auto-checked as human-verified

## Not done
- Dead-code deletions with evidence
- Full inventory execution in CI
- Deficit-based bulk question expansion
- Full test suite run (not claimed)

## Branch
`bountycode/academy-unification-and-resume`
