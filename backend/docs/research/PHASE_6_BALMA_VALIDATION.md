# Phase 6 BALMA Mastery Validation

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Executive Summary

BALMA mastery integrity was validated against 9 learner scenarios (A–I). All 28 checks pass. Mastery evidence is based on unique validated question IDs, not total attempts. Repeated attempts at one question do not inflate mastery.

## Mastery Level Thresholds

| Level | Name | Min Unique Questions | Min Accuracy |
|-------|------|---------------------|--------------|
| 0 | Unknown | 0 | 0% |
| 1 | Introduced | 1 | 0% |
| 2 | Practicing | 3 | 0% |
| 3 | Competent | 6 | 50% |
| 4 | Strong | 11 | 75% |
| 5 | Mastered | 20 | 90% |

Difficulty weights: easy=1.0, medium=1.5, hard=2.0. Transfer questions count double.

## Learner Scenarios (All Passing)

### Scenario A: Repeated Same Question (20 attempts at 1 question)
| Check | Result |
|-------|--------|
| One unique question (not 20) | PASS — got 1 |
| 20 total attempts recorded | PASS — got 20 |
| Level 1 (Introduced) | PASS — got level 1 |
| Accuracy 100% (based on unique) | PASS — got 1.0 |

### Scenario B: Twenty Different Questions
| Check | Result |
|-------|--------|
| 20 unique questions attempted | PASS — got 20 |
| 20 unique questions solved | PASS — got 20 |
| Level 5 (Mastered) | PASS — got level 5 |
| Accuracy 100% | PASS — got 1.0 |

### Scenario C: Untrusted Questions Cannot Inflate Mastery
| Check | Result |
|-------|--------|
| Untrusted questions don't add unique evidence | PASS — unique count unchanged |
| Level unchanged by untrusted questions | PASS |
| Total attempts includes untrusted | PASS — 15 total (5 trusted + 10 untrusted) |

### Scenario D: Unmet Prerequisites Cap Mastery
| Check | Result |
|-------|--------|
| Level capped at 2 (Practicing) | PASS — got level 2 despite 25 questions |
| Prerequisite gating flagged | PASS |

### Scenario E: No False Unseen-Transfer Credit
| Check | Result |
|-------|--------|
| Repeated question doesn't add new unique evidence | PASS — got 1 |
| Weighted evidence doesn't double for repeat transfer | PASS — got 1.5 (not 4.5) |

### Scenario F: Genuine Transfer Credit
| Check | Result |
|-------|--------|
| Transfer question adds unique evidence | PASS — got 10 |
| Transfer evidence counts double | PASS — got 17.5 (>15.0 expected) |
| Transfer evidence trail records is_transfer=True | PASS |

### Scenario G: Repeated Failures → Remediation
| Check | Result |
|-------|--------|
| First failure doesn't trigger remediation | PASS — False |
| Second failure on same question triggers remediation | PASS — True |

### Scenario H: Retention After Interval
| Check | Result |
|-------|--------|
| Delayed transfer questions add unique evidence | PASS — got 8 |
| Level maintained or improved after delay | PASS — got 4, was 3 |

### Scenario I: Evidence Trail Integrity
| Check | Result |
|-------|--------|
| Question ID preserved | PASS |
| Question type preserved | PASS |
| Difficulty preserved | PASS |
| Trust status preserved | PASS |
| Difficulty weight recorded | PASS — got 2.0 for hard |

## Bug Fixes

1. **`record_solve()` was adding untrusted questions to `questions_seen`** — Fixed: only trusted questions (verified/reviewed) enter the unique evidence set. Untrusted questions increment `total_attempts` only.

2. **`calculate_mastery_from_stats()` was double-counting weighted_evidence for repeated attempts** — Fixed: deduplicate by `question_id` when summing weighted evidence. Each unique question contributes at most once.

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 5 | Mastery evidence is reproducible | PASS | Same inputs → same outputs (tested) |
| 6 | Transfer evidence cannot be inflated | PASS | Repeated question as transfer = 1.5 (not 4.5) |

## Files

- `backend/app/services/mastery_engine.py` — Rewritten with unique question ID tracking, difficulty weighting, transfer evidence, prerequisite gating, remediation
- `backend/tests/test_mastery_engine_regression.py` — 24 regression tests (all passing)
- `backend/scripts/validate_balma_mastery.py` — 28 scenario checks (all passing)
