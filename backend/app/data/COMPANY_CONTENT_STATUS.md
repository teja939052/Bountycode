# Company Content Generation Status

## Generated Banks

| Company | File | Generated Count | Serveable Count | Status |
|---------|------|----------------|-----------------|--------|
| TCS NQT | `backend/app/data/tcs_nqt_mcq_verified.json` | 2472 | 2472 | ✅ Verified (MCQ) |
| TCS NQT | `backend/app/data/tcs_nqt_coding_verified.json` | 97 | 40 | ✅ Registered |
| Infosys InfyTQ | `backend/app/data/infosys_infytq_verified.json` | 105 | 73 | ✅ Registered |
| Wipro NLTH | `backend/app/data/wipro_nlth_verified.json` | 97 | 29 | ✅ Registered |
| Cognizant GenC | `backend/app/data/cognizant_genc_verified.json` | 107 | 26 | ✅ Registered |
| Capgemini + Accenture | `backend/app/data/capgemini_accenture_verified.json` | 99 | 49 | ✅ Registered |

**Total generated:** 2977 problems
**Total serveable:** 2689 problems

## Registration

All banks are registered in `backend/app/services/question_store.py` `VERIFIED_EXTRA_BANKS` list.

## Notes

- `tcs_nqt_mcq_verified.json` contains 2472 auto-checked TCS NQT MCQs with normalized `options` + `correct_answer`.
- `tcs_nqt_questions.json` is retained in the unverified pool for audit; 450 entries are quarantined as broken placeholders.
- `tcs_nqt_coding_verified.json` remains the canonical verified coding bank for TCS NQT.
- Deduplication against existing banks reduces serveable counts.
- Company blueprints already exist in `backend/app/data/company_blueprints.json` for all 5 companies.

## Next Steps

1. Verify API serving works end-to-end for the new MCQ bank
2. Update frontend TCS NQT flows to consume verified questions
3. Consider sourcing original TCS NQT content to replace quarantined placeholders
