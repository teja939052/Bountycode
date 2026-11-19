# CRITICAL: Restore `question_store.py`

## What happened
While pushing trust-status patches, a large-file transport failure overwrote
`backend/app/services/question_store.py` with a broken assembler/placeholder.

**This must be fixed before deploying this branch.**

## Restore (local clone)

```bash
git fetch origin
git checkout bountycode/academy-unification-and-resume

# Last known good full file (pre-corruption)
git checkout cb871f5c0c2701112c6384c88d7537f8f12ff185 -- backend/app/services/question_store.py

# Remove broken chunk transport if present
rm -rf backend/app/services/_qs_b64_chunks

git add backend/app/services/question_store.py
git commit -m "restore(question_store): recover full module from cb871f5"
```

## Optional trust honesty patch (after restore)

In `_load_auto_checked_banks`, after `_assign_id`, set:

```python
st = str(item.get("trust_status") or "").lower()
if st not in ("verified", "reviewed", "human_reviewed"):
    item["trust_status"] = "automated_checked"
```

In `_load_extra_bank`, when `fname` is in `EXTRA_BANKS` / `VERIFIED_EXTRA_BANKS`
and status is missing/unverified, set `trust_status = "verified"`.

Add `"original_coding_verified.json"` to `EXTRA_BANKS` and `VERIFIED_EXTRA_BANKS`.

## Still valid on this branch
- `question_governance.py` ownership map
- `docs/research/RUNTIME_SOURCE_OF_TRUTH.md`
- `scripts/audit_question_inventory.py`
- `original_coding_verified.json` (5 original coding problems)
- service OA curated banks + quality gate
- sprint / study bridge work from earlier commits
