# Question Trust Audit

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Trust Lifecycle States

| State | Definition | Servable? | Contributes to Mastery? |
|-------|-----------|-----------|------------------------|
| DRAFT | Initial state, not reviewed | No | No |
| NORMALIZED | Schema-normalized, field completeness checked | No | No |
| AUTOMATED_CHECKED | Passed automated validation (answer key, format) | No | No |
| HUMAN_REVIEWED | Human reviewer verified correctness | Yes (if executable) | Yes |
| VERIFIED | Independently verified (second human or automated+human) | Yes (if executable) | Yes |
| QUARANTINED | Terminal — broken, placeholder, or invalid | No | No |

## Forward-Only Transition Policy

DRAFT → NORMALIZED → AUTOMATED_CHECKED → HUMAN_REVIEWED → VERIFIED → SERVABLE

- Backward transitions are rejected
- QUARANTINED is terminal (cannot return to any other state)
- Structural completeness cannot grant VERIFIED
- Correct answers cannot independently grant VERIFIED
- Automated checks cannot grant HUMAN_REVIEWED

## Validation Results (22/22 checks pass)

| Check | Result |
|-------|--------|
| DRAFT → NORMALIZED allowed | PASS |
| NORMALIZED → AUTOMATED_CHECKED allowed | PASS |
| AUTOMATED_CHECKED → HUMAN_REVIEWED allowed | PASS |
| HUMAN_REVIEWED → VERIFIED allowed | PASS |
| VERIFIED → AUTOMATED_CHECKED rejected | PASS |
| VERIFIED → DRAFT rejected | PASS |
| VERIFIED → QUARANTINED allowed | PASS |
| QUARANTINED → VERIFIED rejected | PASS |
| QUARANTINED → DRAFT rejected | PASS |
| Quarantined question NOT servable | PASS |
| Structurally complete DRAFT NOT servable | PASS |
| Correct-answer MCQ DRAFT NOT servable | PASS |
| High quality but DRAFT NOT servable | PASS |
| Audit log records forward transitions | PASS |
| All forward transitions marked allowed | PASS |
| Unverified questions exist and not servable | PASS |
| No unverified question is servable | PASS |
| Trust and quality dimensions independent | PASS |
| Missing provenance tracked | PASS |

## Trust Breakdown (Runtime Inventory)

| Trust Status | Count | Servable? |
|-------------|-------|-----------|
| verified | 948 | Yes (829 servable) |
| automated_checked | 10,581 | No |
| reviewed | 574 | Yes (574 servable) |
| needs_review | 2,965 | No |
| unverified | 693 | No |
| quarantined | 121 | No |

Total servable: 1,403 (8.8% of 15,882)
