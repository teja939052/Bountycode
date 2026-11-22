# Question Inventory Report

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Inventory Counts

| Metric | Value |
|--------|-------|
| Total loaded records | 15,882 |
| Unique canonical question IDs | 15,845 |
| Duplicate ID records | 37 |
| Duplicate clusters (by normalized title) | 117 |
| Servable questions | 1,403 |
| Servable rate | 8.8% |

## Trust Breakdown

| Trust Status | Count | Servable |
|-------------|-------|----------|
| verified | 948 | 829 |
| automated_checked | 10,581 | 0 |
| reviewed | 574 | 574 |
| needs_review | 2,965 | 0 |
| unverified | 693 | 0 |
| quarantined | 121 | 0 |

## Question Type Breakdown

| Type | Total | Servable |
|------|-------|----------|
| coding | 8,363 | 942 |
| aptitude | 4,022 | 50 |
| logical | 1,065 | 15 |
| verbal | 535 | 15 |
| cs_fundamentals | 453 | 43 |
| sql | 950 | 109 |
| interview | 148 | 148 |
| system_design | 62 | 12 |
| debugging | 209 | 4 |
| pseudocode | 10 | 10 |
| puzzle | 10 | 10 |
| written_communication | 20 | 20 |
| reasoning | 25 | 25 |
| cs | 10 | 0 |

## Per-Type Quality (Sampled 500 Questions)

| Metric | Value |
|--------|-------|
| All required fields present | 328 (65.6%) |
| Missing required fields | 172 (34.4%) |

Top missing required fields:
1. Competency being tested (100)
2. Expected thinking / response framework (100)
3. Seed data (72)
4. Expected query (72)

## Executability

| Status | Count |
|--------|-------|
| Executable | 14,406 |
| Not executable | 1,476 |

## Answer Correctness (Non-code types only)

| Result | Count |
|--------|-------|
| Automatable | 6,085 |
| Correct (100%) | 5,593 |
| Incorrect (<100%) | 492 |
| Not automatable | 275 |

## Skill Mapping

| Status | Count |
|--------|-------|
| Mapped to canonical skill | 11,753 |
| Unmapped | 4,129 |

## Quality Systems (Three Separate Systems)

| System | Function |
|--------|----------|
| Structural completeness | `validate_structure()` — per-type required/optional/inapplicable field presence |
| Answer correctness | `validate_answer_correctness()` — automated where possible; None = human review |
| Executability | `validate_executability()` — can the question actually be graded |
| Trust status | `question_store.py` — lifecycle state machine |
| Serving eligibility | `question_store._is_servable()` — trust in {verified, reviewed} AND executable |
| Quality score | `score_question()` — weighted field presence; never auto-grants verified |

## Key Finding

The previously reported 1,415 "servable" questions conflated quality score with trust status. The actual servable count is 1,403 (8.8% of 15,882). Quality tier (bronze/solid/premium) is independent of trust status.
