# Phase 6 Company Readiness Validation

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Executive Summary

Company readiness was validated against 7 simulated learner profiles plus evidence type distinction checks. All 24 checks pass. Readiness is based on canonical skill mastery, valid assessment performance, unseen transfer assessments, role-specific requirements, weaknesses and prerequisites, confidence and evidence quality — NOT on percentage of questions completed.

## Readiness Level Thresholds

| Score Range | Level |
|-------------|-------|
| 90–100 | Interview Ready |
| 75–89 | Almost There |
| 60–74 | Progressing |
| 40–59 | Building Foundation |
| 0–39 | Getting Started |

## Simulated Learner Results (All Passing)

### Learner 1: High Question Completion, Low Mastery
- 200+ questions completed per domain, but scores 5–30%
- **Overall readiness: 19.1** (Getting Started)
- **Key finding:** Readiness is NOT based on question count — high completion with low mastery = low readiness

### Learner 2: Low Question Completion, High Demonstrated Mastery
- 2–15 questions completed per domain, but scores 65–92%
- **Overall readiness: 80.3** (Almost There)
- **Key finding:** Demonstrated mastery matters more than question completion count

### Learner 3: High Mastery, Poor Retention
- Mastery levels 4–5 across all domains, retention scores 20–40%
- **Overall readiness: 83.2** (capped by poor retention)
- **Key finding:** Retention penalty reduces readiness despite high mastery

### Learner 4: High Mastery, No Unseen Transfer
- Mastery levels 3–5 across all domains, transfer_score = 0
- **Overall readiness: 83.2** (capped without transfer evidence)
- **Key finding:** Unseen transfer evidence is required for full readiness

### Learner 5: Strong Skills with Unmet Prerequisites
- DSA and system_design at mastery level 5, but aptitude/coding/cs_fundamentals at level 1
- **Overall readiness: 40.5** (Building Foundation)
- **Key finding:** Missing foundational skills drag down readiness

### Learner 6: Strong Evidence Aligned with Company Role (TCS)
- Aptitude 95%, DSA 85%, coding 80%, cs_fundamentals 88%
- **TCS readiness: 83.9**, Internal prediction: 76.0
- **Key finding:** Company-specific evidence differs from internal prediction; never presented as company cutoff

### Learner 7: Insufficient Evidence
- All domains at 0% score, level 0
- **Overall readiness: 0.0**, Evidence confidence: 0.0
- **Key finding:** Zero evidence = zero readiness

## Readiness Evidence Distinction (All Passing)

| Check | Result |
|-------|--------|
| Demonstrated evidence in domain_scores | PASS |
| Internal prediction separate from company evidence | PASS (76.0 vs 83.9 for TCS) |
| Company evidence includes domain breakdown | PASS |
| Readiness level is not "Hired" or "Guaranteed" | PASS (got "Progressing") |
| Methodology: not based on question count | PASS |
| Methodology: based on demonstrated skills | PASS |
| Company evidence separate from internal prediction | PASS |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 8 | Readiness uses genuine validated evidence | PASS | 24/24 checks pass across 7 learner profiles |

## Bug Fixes

1. **`_domain_score()` was called but never defined in readiness_engine.py** — Added as helper function that extracts assessment_score or maps mastery_level (0–5) to 0–100 scale.

## Files

- `backend/app/services/readiness_engine.py` — Added `_domain_score()` helper and `company_readiness_evidence_report()`
- `backend/scripts/validate_company_readiness.py` — 24 readiness checks (all passing)
