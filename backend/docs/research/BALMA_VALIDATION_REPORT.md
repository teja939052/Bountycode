# BALMA Validation Report

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

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

## Learner Scenarios (28/28 checks pass)

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
| Untrusted questions don't add unique evidence | PASS |
| Level unchanged by untrusted questions | PASS |
| Total attempts includes untrusted | PASS |

### Scenario D: Unmet Prerequisites Cap Mastery
| Check | Result |
|-------|--------|
| Level capped at 2 (Practicing) | PASS |
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
| First failure doesn't trigger remediation | PASS |
| Second failure on same question triggers remediation | PASS |

### Scenario H: Retention After Interval
| Check | Result |
|-------|--------|
| Delayed transfer questions add unique evidence | PASS — got 8 |
| Level maintained or improved after delay | PASS |

### Scenario I: Evidence Trail Integrity
| Check | Result |
|-------|--------|
| Question ID preserved | PASS |
| Question type preserved | PASS |
| Difficulty preserved | PASS |
| Trust status preserved | PASS |
| Difficulty weight recorded | PASS — got 2.0 for hard |

## Bug Fixes

1. **`record_solve()` was adding untrusted questions to `questions_seen`** — Fixed: only trusted questions (verified/reviewed) enter the unique evidence set.
2. **`calculate_mastery_from_stats()` was double-counting weighted_evidence** — Fixed: deduplicate by `question_id` when summing weighted evidence.

## Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 5 | Mastery evidence is reproducible | PASS |
| 6 | Transfer evidence cannot be inflated | PASS |
