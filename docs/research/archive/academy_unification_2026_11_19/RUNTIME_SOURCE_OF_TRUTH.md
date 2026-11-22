# Runtime source-of-truth map (Bountycode questions)

**Branch:** `bountycode/academy-unification-and-resume`  
**Scope:** How questions reach learners. Not a marketing inventory.

## Ownership (do not add a fourth system)

| Runtime | Role | Student-facing? |
|---------|------|-----------------|
| `question_store` | DSA / SQL / interview / CS placement bank | Only `trust_status` ∈ {verified, reviewed} **and** executable |
| `quiz_service` | Curated interactive quizzes / learning objects | Yes (curated content) |
| `service_oa_mocks` | Service-company OA MCQs (TCS/Infy/Wipro/…) | Yes (curated parts 1–3) |

Canonical contract: `backend/app/services/question_governance.py`.

## Path

```
source file
  → loader (question_store.load_all / quiz load / service_oa load_problem_bank)
  → normalize (_assign_id)
  → trust stamp (verified | automated_checked | unverified)
  → dedupe / quarantine
  → _is_servable / section filters
  → API (questions / coding / quiz / service-oa)
  → frontend
  → grade / progress
```

## Critical serving rule

`automated_checked` means **machine tests passed**, not human review.

`_is_servable()` requires `trust_status in (verified, reviewed)` **and** `_is_executable()`.

Loader bug (fixed on this branch): auto-checked banks were documented as if they were the verified pool; they are now stamped `automated_checked` and stay non-servable until promotion.

## Service OA path (separate)

Files: `service_oa_problem_bank_part*.json`  
Loader: `service_oa_mocks.load_problem_bank` (quality gate: options + correct_index + explanation)  
API: `/api/v1/service-oa/*`

## Curriculum path (not a question bank)

Lessons: `app/data/lessons/*.json`  
Sprint: `service_company_sprint.json`  
Study today: `study_sprint_bridge` → Academy lessons + weak skills + `/service-oa`

## Inventory command

```bash
cd backend && python -m scripts.audit_question_inventory
```

Writes machine-readable counts under `docs/research/generated/` (when run locally).
