# BALMA × SM-2 wiring (implemented)

Branch: `bountycode/academy-unification-and-resume`

## What BALMA means here

Not a separate package. Product loop:

1. **Curriculum** — service company sprint (`study_sprint_bridge`)
2. **Mastery** — `mastery_engine` (0–5)
3. **Retention** — SM-2 (`spaced_repetition` + `srs_cards`)
4. **Company readiness** — `/service-oa` when overall ≥ 55

## Changes shipped

### Study Today includes due SRS cards
`GET /api/v1/study/today` → `get_today_sprint_first`:
- Calls `load_srs_due_reviews` (Mongo `srs_cards`)
- Merges into `reviews` (SRS first, then legacy)
- Adds `srs_due_count` and `balma` metadata block

### Richer SM-2 grades
`POST /api/v1/srs/record` accepts optional:
```json
{ "problem_id": "...", "is_correct": true, "grade": "hard", "concept_id": "quant:percentages", "difficulty": "medium" }
```
`grade`: `again` | `hard` | `good` | `easy`  
If omitted: correct → GOOD, incorrect → AGAIN (backward compatible).

### Service OA concept taxonomy
`backend/app/services/service_oa_srs_concepts.py`  
IDs like `quant:percentages`, `logical:seating`, `verbal:para-jumbles`.

## Client integration notes

- Dashboard / Study Today UI should render `plan.reviews` where `source === "sm2_srs"`.
- After practice, call `/api/v1/srs/record` with a real grade when the UI has confidence (e.g. timed vs instant).
- Pass `concept_id` from service OA topic tags when recording OA practice.

## Still open

- Frontend grade picker (HARD/GOOD/EASY buttons)
- Wire `get_all_concept_ids()` to also union `all_service_oa_concept_ids()` on user init
- Restore `question_store.py` if still broken on this branch (see CRITICAL_QUESTION_STORE_RESTORE.md)
