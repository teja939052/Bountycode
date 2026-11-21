# Programming Foundations Recovery Report

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Classification Summary

| Classification | Count |
|---------------|-------|
| Recoverable | 4 |
| Requires repair | 183 |
| Requires review | 308 |
| Duplicate | 196 |
| Quarantine | 0 |
| **Total** | **691** |

## Classification Criteria

| Classification | Criteria | Action |
|---------------|----------|--------|
| Recoverable | Structurally complete + correct + human-reviewed (verified/reviewed) | Promote to servable |
| Requires repair | Fixable issues (missing fields, incorrect answer, not executable) | Repair and re-review |
| Requires review | Correctness not automatable or unverified | Human review required |
| Duplicate | Same normalized title as another question | Mark as duplicate, keep canonical |
| Quarantine | Placeholder, empty, already quarantined, or broken beyond repair | Quarantine — do not serve |

## Methodology

Classification based on:
1. Type-specific structural validation (validate_structure)
2. Answer correctness (validate_answer_correctness — automated where possible)
3. Executability (validate_executability)
4. Trust status (question_store)
5. Duplicate detection (normalized title matching)

No questions were automatically promoted. All classifications require human review before promotion.

## Reports Generated

- `backend/app/data/quality_reports/programming_foundations_recovery.json` — Machine-readable classification
- `backend/scripts/pf_recovery_direct.py` — Classification script

## Important Note

These counts are from the current repository state. Historical reports may show different numbers due to inventory changes. No questions were modified or promoted during this classification.
