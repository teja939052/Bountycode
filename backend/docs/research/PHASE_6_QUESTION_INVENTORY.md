# Phase 6 Question Inventory Report

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Executive Summary

The question inventory was validated against the runtime question store. Trust status, quality score, and serving eligibility are reported as three separate systems — never combined into one number.

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

| Trust Status | Count |
|--------------|-------|
| verified | 948 |
| automated_checked | 10,581 |
| reviewed | 574 |
| needs_review | 2,965 |
| unverified | 693 |
| quarantined | 121 |

## Servable Breakdown

| Trust Status | Count |
|--------------|-------|
| verified | 829 |
| reviewed | 574 |

Servable questions require trust_status in {verified, reviewed} AND executability.

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
| cs | 10 | — |

## Type-Specific Quality (Sampled 500 Questions)

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

## Duplicate Clusters

117 duplicate clusters found by normalized title. Top clusters (2 questions each):
- `givenatableemployeeswithcolumnsidnamedepartmentsalaryagewrit`
- `givenatableproductsidnamepricecategorywriteaquerytoselectall`
- `givenatableordersidcustomeridamountorderdatewriteaquerytocou`
- `givenatableemployeesidnamedepartmentsalarywriteaquerytofindh`
- `givenatableordersidcustomeridamountwriteaquerytofindhowmanyd`

## Quality Systems (Three Separate Systems)

| System | Function | Purpose |
|--------|----------|---------|
| Structural completeness | `validate_structure()` | Per-type required/optional/inapplicable field presence |
| Answer correctness | `validate_answer_correctness()` | Automated where possible; None = human review |
| Executability | `validate_executability()` | Can the question actually be graded |
| Trust status | `question_store.py` | Lifecycle state machine (unverified → verified) |
| Serving eligibility | `question_store._is_servable()` | Trust in {verified, reviewed} AND executable |
| Quality score | `score_question()` | Weighted field presence; never auto-grants verified |

## Key Finding

The previously reported 1,415 "servable" questions and 286 "Solid" / 1,129 "Bronze" breakdown conflated quality score with trust status. The actual servable count is 1,403 (8.8% of 15,882), and quality tier (bronze/solid/premium) is independent of trust status.
