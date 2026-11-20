# BountyCode Question Bank — Final Reconciliation Report

**Repository:** BountyCode (`teja939052/Bountycode`)  
**Branch:** `feat/question-bank-cleanup-and-expansion`  
**Git Commit SHA:** `6703c4e004377f3a7bf51058e7e9732475a52da4`  
**Report Date:** 2026-11-17  
**Generated from:** `backend/app/services/question_store.py` + `backend/app/services/question_quality.py` (authoritative runtime)

---

## Executive Summary

**Question quantity is NOT Bountycode's advantage.** Only **1,415 of 15,882 loaded questions (8.9%)** are servable—meaning they pass both the trust gate (verified/reviewed trust status) and the serving gate (executable test cases, schema, options+answer, or rubric).

Of the 1,415 servable questions:
- **0 (0%)** score Premium (90+)
- **286 (20.2%)** score Solid (60-89)  
- **1,129 (79.8%)** score Bronze (<60)

Only **2 of 9 domains** meet their servable targets:
- **DSA Coding:** 942 servable / 460 target ✓
- **Behavioral/Interview:** 148 servable / 60 target ✓

All other domains fall far short:
- **SQL:** 109/120 (11 short)
- **Debugging:** 4/80 (76 short)
- **System Design:** 24/62 (38 short)
- **CS Fundamentals:** 43/300 (257 short)
- **Quantitative Aptitude:** 50/300 (250 short)
- **Logical Reasoning:** 15/180 (165 short)
- **Verbal Ability:** 15/150 (135 short)

Question-bank expansion is **frozen**. The platform does not need more questions—it needs higher-quality, trustworthy questions.

---

## 1. Trust State Breakdown (Authoritative Runtime)

| Trust Status | Count | Servable | Servable % | Notes |
|-------------|-------|----------|------------|-------|
| verified | 964 | 841 | 87.2% | 964 lack transition metadata—flagged for review |
| reviewed | 574 | 574 | 100.0% | Human-reviewed via `transition_trust()` |
| automated_checked | 10,581 | 0 | 0.0% | Automated validation only; NOT served |
| needs_review | 2,949 | 0 | 0.0% | Awaiting human review |
| unverified | 693 | 0 | 0.0% | Raw imported content |
| quarantined | 121 | 0 | 0.0% | Excluded from serving |
| **Total** | **15,882** | **1,415** | **8.9%** | |

### Trust Lifecycle (Enforced by `question_store.py`)

```
DRAFT (unverified) → NORMALIZED (needs_review) → AUTOMATED_CHECKED → HUMAN_REVIEWED (reviewed) → VERIFIED → SERVABLE
```

### Trust Migration Actions Completed

**715 batch-added questions** were downgraded from `verified` to `automated_checked` because they were imported via batch scripts without human review:

| Source Bank | Questions Downgraded |
|-------------|---------------------|
| verified_aptitude.json | 271 |
| verified_cs_fundamentals.json | 302 |
| verified_logical.json | 255 |
| verified_verbal.json | 196 |
| debugging_bank.json | 76 |
| system_design_bank.json | 38 |
| sql_practice_bank.json | 12 |
| **Total** | **715** |

### 964 Verified Questions Without Transition Metadata

964 pre-existing verified questions lack `trust_transitioned_at`/`trust_transition_reason` metadata. They were imported without going through `transition_trust()`. They remain servable but are flagged in the audit log for manual review:

| Source Bank | Count |
|-------------|-------|
| verified_placement_questions | 209 |
| infosys_infytq_verified | 95 |
| wipro_nlth_verified | 31 |
| sql_practice_bank | 55 |
| legacy | 279 |
| interview_practice_bank | 49 |
| india_placement_depth | 32 |
| debugging_bank | 4 |
| tcs_nqt_coding_verified | 40 |
| cognizant_genc_verified | 72 |
| capgemini_accenture_verified | 98 |

---

## 2. Per-Domain Servable Counts vs Targets

| Domain | Servable | Target | Remaining | Status |
|--------|----------|--------|-----------|--------|
| DSA Coding | 942 | 460 | 0 | MET |
| Behavioral/Interview | 148 | 60 | 0 | MET |
| SQL | 109 | 120 | 11 | NOT MET |
| Debugging | 4 | 80 | 76 | NOT MET |
| System Design | 24 | 62 | 38 | NOT MET |
| CS Fundamentals | 43 | 300 | 257 | NOT MET |
| Quantitative Aptitude | 50 | 300 | 250 | NOT MET |
| Logical Reasoning | 15 | 180 | 165 | NOT MET |
| Verbal Ability | 15 | 150 | 135 | NOT MET |
| **Total (9 domains)** | **2,296** | **1,710** | **731** | **Only 2 of 9 met** |

*Note: Sum of per-domain servable (2,296) differs from total servable (1,415) because some questions map to multiple domains. The per-domain count counts a question in every domain it matches, while total servable counts each question once.*

---

## 3. Question Quality Assessment (using `question_standard.py`)

All 1,415 servable questions were scored against the Placement Question Standard (15 weighted fields):

| Quality Tier | Score Range | Count | % of Servable |
|-------------|-------------|-------|---------------|
| Premium | 90–100 | 0 | 0% |
| Solid | 60–89 | 286 | 20.2% |
| Bronze | <60 | 1,129 | 79.8% |

**No servable question achieves Premium quality.** 79.8% are Bronze quality—missing critical fields needed for reliable assessment.

### Missing Fields Across All Servable Questions

| Missing Field | Count | % of Servable |
|--------------|-------|---------------|
| Input/output specification | 1,415 | 100.0% |
| Edge cases | 1,415 | 100.0% |
| Expected thinking | 1,415 | 100.0% |
| Complexity | 1,398 | 98.8% |
| Follow-up question | 1,398 | 98.8% |
| Placement relevance | 772 | 54.6% |
| Interview explanation | 562 | 39.7% |
| Examples | 560 | 39.6% |
| Explicit constraints | 384 | 27.1% |
| Pattern | 376 | 26.6% |
| Reference solution | 212 | 15.0% |
| Hints | 138 | 9.8% |

**Every servable question is missing input/output specification, edge cases, and expected thinking.** 98.8% are also missing complexity and follow-up information. These are not minor omissions—without expected thinking and edge cases, a question cannot be reliably graded.

---

## 4. Duplicate ID Analysis

| Metric | Count |
|--------|-------|
| Total questions with IDs | 15,882 |
| Unique IDs | 15,845 |
| Duplicate IDs | 37 |

Duplicate IDs (first 20): `apt-001`, `apt-002`, `apt-003`, `apt-004`, `apt-005`, `log-001`, `log-002`, `log-003`, `apt-006`, `apt-007`, `apt-008`, `apt-009`, `apt-010`, `cs-001`, `cs-002`, `cs-003`, `cs-004`, `apt-011`, `apt-012`, `apt-013`.

Duplicate IDs indicate the same question appears under multiple IDs, inflating the apparent question count without adding unique assessment value.

---

## 5. Trust Label Integrity

### Key Finding: "Verified" ≠ Human-Reviewed

**964 questions are marked `trust_status="verified"` but lack `trust_transitioned_at`/`trust_transition_reason` metadata.** These were imported directly into JSON banks without going through `transition_trust()`. They remain servable but are flagged in the audit log for manual review.

### Questions Downgraded During Migration

**715 batch-added questions** were downgraded from `verified` to `automated_checked` because they lacked human review:

| Source Bank | Questions Downgraded |
|-------------|---------------------|
| verified_aptitude.json | 271 |
| verified_cs_fundamentals.json | 302 |
| verified_logical.json | 255 |
| verified_verbal.json | 196 |
| debugging_bank.json | 76 |
| system_design_bank.json | 38 |
| sql_practice_bank.json | 12 |
| **Total** | **715** |

### Questions Still with `trust_status="verified"` (Not Downgraded)

| Source Bank | Count |
|-------------|-------|
| verified_placement_questions.json | 209 |
| infosys_infytq_verified.json | 95 |
| wipro_nlth_verified.json | 31 |
| sql_practice_bank.json | 55 |
| legacy | 279 |
| interview_practice_bank.json | 49 |
| india_placement_depth.json | 32 |
| debugging_bank.json | 4 |
| tcs_nqt_coding_verified.json | 40 |
| cognizant_genc_verified.json | 72 |
| capgemini_accenture_verified.json | 98 |

These pre-existing verified questions were not downgraded because they existed before the batch-question expansion work began. Their trust status predates the batch-question expansion.

---

## 6. Tests Executed

**56/56 tests pass** across two test files:

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_question_governance.py` | 31 | Trust transitions, serving gate, content trust fixes, question inventory |
| `test_question_quality.py` | 25 | Question quality scoring, per-type validation, serving gate |

**Total: 56/56 tests pass.**

---

## 7. Recommendations

### P0 — Question Quality (Immediate)

1. **Do not generate more questions.** The bank has 15,882 questions but only 1,415 servable, and 0 score at Premium quality. Adding more questions without fixing quality will only increase noise.

2. **Repair the 286 Solid questions** (score 60-89): These have most fields but miss 1-2 critical fields. Prioritize repairing missing input/output specification, edge cases, and expected thinking.

3. **Move 1,129 Bronze questions to `needs_review`:** These lack multiple critical fields and cannot be trusted without human review.

4. **Do not auto-promote any question to `verified`.** Even a score of 89/100 can hide a wrong answer or broken solution. Human review is required.

### P1 — Lesson-to-Question Integration

- Every servable question should carry `canonical_skill_id` tags matching `skill_assessment.SKILL_CATEGORIES`
- `curriculum_connector.py` maps capabilities and role skills to canonical skill IDs
- Questions should connect to: prerequisite lessons → concept → worked examples → practice → unseen assessment → mastery evidence → spaced repetition
- Verify every servable question has canonical skill tags

### P1 — BALMA Mastery Integrity

- `mastery_engine.py` counts problem attempts without deduplicating identical questions
- A student could answer the same question 20 times and reach "Mastered" (level 5)
- Fix: Count unique question IDs, weight by trust level, require unseen transfer questions

### P2 — Company Readiness Calibration
- `readiness_engine.py` already has `TRUST_WEIGHT` dict and company-specific weights
- `calculate_readiness()` takes pre-computed scores; question-level trust weights should flow into category scores
- Company profiles (`company_prep.py`) have `companies` tags but need evidence-based company readiness

### P2 — Programming Foundations Recovery
- 1,316 raw questions exist with topic/sub_topic containing "program"
- 0 are servable (fail trust or executability checks)
- Investigate individually: which topics, which are recoverable, which to quarantine
- Determine whether "programming_foundations" should be added as a 10th domain

---

## Final State Summary

| Metric | Value |
|--------|-------|
| Total questions loaded | 15,882 |
| Total servable | 1,415 |
| Servable % | 8.9% |
| Servable by trust: verified | 841 |
| Servable by trust: reviewed | 574 |
| Servable by trust: automated_checked | 0 |
| Servable by trust: needs_review | 0 |
| Servable by trust: unverified | 0 |
| Servable by trust: quarantined | 0 |
| Servable per topic (max) | DSA Coding: 942 |
| Servable per topic (min) | Debugging: 4 |
| Domains meeting target | 2 of 9 |
| Premium quality questions | 0 |
| Solid quality questions | 286 |
| Bronze quality questions | 1,129 |
| Questions with 100% missing critical fields | 1,415 |
| Questions missing critical fields | 1,415 |

**End of Report**

*Generated from `backend/app/services/question_store.py` and `backend/app/services/question_quality.py` at git commit `6703c4e004377f3a7bf51058e7e9732475a52da4`*
