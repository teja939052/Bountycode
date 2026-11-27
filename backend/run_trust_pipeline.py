import json, os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend to path
sys.path.insert(0, r"D:\Project-Fremen\backend")

from app.services.question_store import (
    load_all,
    _dedupe_and_filter,
    _score_all_questions,
    _map_question_skills,
    _apply_served_quarantine,
    _audit_trust_integrity,
    _migrate_batch_added_questions,
    _migrate_bronze_verified_questions,
)
from app.config import get_settings

settings = get_settings()

bank_path = r"D:\Project-Fremen\backend\app\data\questions_bank_deduplicated.json"

# Step 1: Load the bank
print("=" * 60)
print("STEP 1: Loading question bank...")
print("=" * 60)

with open(bank_path, encoding='utf-8') as f:
    bank = json.load(f)

print(f"Loaded {len(bank)} questions")

# Step 2: Deduplicate and filter
print("\n" + "=" * 60)
print("STEP 2: Deduplicating and filtering...")
print("=" * 60)

unique_bank = _dedupe_and_filter(bank)
print(f"After dedup: {len(unique_bank)} questions (removed {len(bank) - len(unique_bank)} duplicates)")

# Step 3: Score all questions
print("\n" + "=" * 60)
print("STEP 3: Scoring all questions...")
print("=" * 60)

scored = _score_all_questions(unique_bank)
print(f"Scored {scored} questions")
print(f"Quality scores range: easy questions tend to score higher")

# Step 4: Map question skills
print("\n" + "=" * 60)
print("STEP 4: Mapping question skills...")
print("=" * 60)

mapped = _map_question_skills(unique_bank)
print(f"Mapped {mapped} questions to canonical skills")

# Step 5: Apply served quarantine
print("\n" + "=" * 60)
print("STEP 5: Applying served quarantine...")
print("=" * 60)

quarantined = _apply_served_quarantine(unique_bank)
print(f"Quarantined {quarantined} questions (execution-broken)")

# Step 6: Audit trust integrity
print("\n" + "=" * 60)
print("STEP 6: Auditing trust integrity...")
print("=" * 60)

audited = _audit_trust_integrity(unique_bank)
print(f"Audited trust integrity for all questions")

# Step 7: Migrate batch added questions
print("\n" + "=" * 60)
print("STEP 7: Migrating batch-added questions...")
print("=" * 60)

batch_downgraded = _migrate_batch_added_questions(unique_bank)
print(f"Downgraded {batch_downgraded} batch-added questions")

# Step 8: Migrate bronze verified questions
print("\n" + "=" * 60)
print("STEP 8: Migrating bronze-quality verified questions...")
print("=" * 60)

bronze_downgraded = _migrate_bronze_verified_questions(unique_bank)
print(f"Downgraded {bronze_downgraded} bronze-quality verified questions")

# Step 9: Count final trust status distribution
print("\n" + "=" * 60)
print("STEP 9: Final trust status distribution...")
print("=" * 60)

trust_counts = {}
for q in unique_bank:
    t = q.get('trust_status', 'unverified')
    trust_counts[t] = trust_counts.get(t, 0) + 1

for status, count in sorted(trust_counts.items()):
    print(f"  {status}: {count} ({count/len(unique_bank)*100:.1f}%)")

# Step 10: Save the pipeline-processed bank
print("\n" + "=" * 60)
print("STEP 10: Saving pipeline-processed bank...")
print("=" * 60)

output_path = r"D:\Project-Fremen\backend\app\data\questions_bank_pipeline.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(unique_bank, f, ensure_ascii=False, indent=2)

print(f"Saved to: {output_path}")
print(f"Total questions: {len(unique_bank)}")

print("\n" + "=" * 60)
print("TRUST PIPELINE COMPLETE!")
print("=" * 60)
print("\nThe question bank is now properly:")
print("  - Deduplicated")
print("  - Scored with quality metrics")
print("  - Mapped to canonical skills")
print("  - Quarantined (execution-broken)")
print("  - Audited for trust integrity")
print("  - Migrated from batch imports")
print("  - Ready for serving to users")