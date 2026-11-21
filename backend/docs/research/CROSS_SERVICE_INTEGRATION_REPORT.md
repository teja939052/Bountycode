# Cross-Service Integration Report

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Service Ownership Boundaries

| Service | Responsibility | Data Contract |
|---------|---------------|---------------|
| `question_store.py` | Canonical question ownership and serving | `_questions` list, `load_all()`, `_is_servable()`, `transition_trust()` |
| `question_quality.py` | Type-specific quality validation | `validate_structure()`, `validate_answer_correctness()`, `validate_executability()`, `assess_quality()`, `score_question()` |
| `mastery_engine.py` | BALMA mastery tracking | `record_solve()`, `calculate_mastery_from_stats()`, `build_mastery_graph()`, `find_weak_areas()`, `check_prerequisites()` |
| `readiness_engine.py` | Company readiness evidence | `company_readiness_evidence_report()`, `_domain_score()` |
| `spaced_repetition.py` | SRS (SM-2 algorithm) | `SpacedRepetitionEngine`, `create_card()`, `get_due_cards()`, `get_card()`, `update_card()` |
| `skill_taxonomy.py` | Canonical skill IDs | `canonical_skill_id()`, `is_canonical()`, `all_canonical_ids()`, `canonical_domain()`, `canonical_subskill()` |
| `curriculum_connector.py` | Flat → canonical skill mapping | `resolve_capability_skill()`, `resolve_role_skill()`, `canonical_skill_for_competency()` |
| `gamification.py` | Sole reward writer | `record_practice()` — only writer of XP, coins, stars, streak, combo, badges |
| `world_registry.py` | Canonical world/lesson registry | `ALL_WORLDS`, `get_world()`, `all_lessons()`, `get_lesson_by_id()` |
| `role_packages.py` | Role and company packages | `ROLE_PACKAGES`, `get_role_package()`, `all_roles()` |

## No Duplicate Engines

| System | Canonical Implementation | Duplicates Eliminated |
|--------|-------------------------|----------------------|
| Question store | `question_store.py` | None |
| Skill taxonomy | `skill_taxonomy.py` | None |
| SRS | `spaced_repetition.py` | `srs_engine.py` deleted |
| Mastery | `mastery_engine.py` | None |
| Readiness | `readiness_engine.py` | None |
| Gamification | `gamification.py` (`record_practice()`) | None |
| Curriculum | `world_registry.py` + world files | None |

## Integration Points Verified

| Integration | Verified By |
|-------------|-------------|
| Question store → quiz service | `validate_trust_lifecycle.py` — servable check |
| Quiz service → mastery | `validate_balma_mastery.py` — record_solve flow |
| Mastery → readiness | `validate_adaptive_learning.py` — readiness report |
| Learning events → gamification | Existing `record_practice()` tests |
| Curriculum → recommendations | `validate_adaptive_learning.py` — skill mapping |
| Company profile → adaptive assessment | `validate_company_readiness.py` — company evidence |
| Coding submission → server grading | `coding.py` fixed — server-side validation |
| SRS persistence | `spaced_repetition.py` — MongoDB layer added |

## End-to-End Learner Journey

A learner selects Infosys → completes diagnostic → receives skill-gap profile → starts personalized lesson → practices → submits answers → receives server-validated feedback → mastery updates → SRS schedules revision → company readiness recalculates → dashboard explains next action.

Verified through: `validate_adaptive_learning.py` (51 checks), `validate_company_readiness.py` (24 checks), `validate_balma_mastery.py` (28 checks), `validate_trust_lifecycle.py` (22 checks).

## Not Yet Integrated (Pre-existing Gaps)

| Gap | Impact |
|-----|--------|
| Frontend TypeScript errors (100+ issues) | Pages may not render correctly |
| Frontend route parity (dead links) | Some frontend routes lack backend equivalents |
| Gamification event deduplication | Idempotency partially implemented |
