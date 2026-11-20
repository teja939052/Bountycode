# Company Readiness Audit

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Readiness Level Thresholds

| Score Range | Level |
|-------------|-------|
| 90–100 | Interview Ready |
| 75–89 | Almost There |
| 60–74 | Progressing |
| 40–59 | Building Foundation |
| 0–39 | Getting Started |

## Readiness Methodology

Readiness is based on canonical skill mastery, valid assessment performance, unseen transfer assessments, retention, consistency, and company-specific requirements — NOT on percentage of questions completed.

Four distinct measures are kept separate:
1. **Actual learner performance** — domain scores from assessments
2. **Internal mastery estimate** — mastery_engine levels (0–5)
3. **Company-specific predicted readiness** — weighted by company requirements
4. **Verified employer assessment results** — external validation (not fabricated)

## Simulated Learner Results (24/24 checks pass)

### Learner 1: High Question Completion, Low Mastery
- 200+ questions per domain, scores 5–30%
- Overall readiness: 19.1 (Getting Started)
- **Key finding:** Readiness is NOT based on question count

### Learner 2: Low Question Completion, High Demonstrated Mastery
- 2–15 questions per domain, scores 65–92%
- Overall readiness: 80.3 (Almost There)
- **Key finding:** Demonstrated mastery matters more than question count

### Learner 3: High Mastery, Poor Retention
- Mastery levels 4–5, retention scores 20–40%
- Overall readiness: 83.2 (capped by poor retention)

### Learner 4: High Mastery, No Unseen Transfer
- Mastery levels 3–5, transfer_score = 0
- Overall readiness: 83.2 (capped without transfer evidence)

### Learner 5: Strong Skills with Unmet Prerequisites
- DSA/system_design at level 5, aptitude/coding at level 1
- Overall readiness: 40.5 (Building Foundation)

### Learner 6: Company-Aligned Evidence (TCS)
- Aptitude 95%, DSA 85%, coding 80%, cs_fundamentals 88%
- TCS readiness: 83.9, Internal prediction: 76.0
- **Key finding:** Company evidence differs from internal prediction; never presented as cutoff

### Learner 7: Insufficient Evidence
- All domains at 0%, level 0
- Overall readiness: 0.0, Evidence confidence: 0.0

## Readiness Evidence Distinction

| Check | Result |
|-------|--------|
| Demonstrated evidence in domain_scores | PASS |
| Internal prediction separate from company evidence | PASS |
| Company evidence includes domain breakdown | PASS |
| Readiness level is not "Hired" or "Guaranteed" | PASS |
| Methodology: not based on question count | PASS |
| Methodology: based on demonstrated skills | PASS |
| Company evidence separate from internal prediction | PASS |
