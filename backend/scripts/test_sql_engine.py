import sys
sys.path.insert(0, ".")
import json
from app.services.sql_engine import SQLEngine

with open("app/data/sql_practice_bank.json", "r", encoding="utf-8") as f:
    sql_bank = json.load(f)

print(f"Total SQL questions in bank: {len(sql_bank)}")

has_tests = [q for q in sql_bank if q.get("testcases") or q.get("test_cases")]
print(f"Have testcases: {len(has_tests)}")

passed = 0
failed = 0
skipped = 0
examples = []
for i, q in enumerate(has_tests[:20]):
    qid = q.get("id", f"idx-{i}")
    expected_query = q.get("correct_answer") or ""
    schema_ddl = q.get("schema_ddl") or ""
    seed_inserts = q.get("seed_inserts") or ""

    if not schema_ddl or not expected_query:
        skipped += 1
        continue

    try:
        result = SQLEngine.verify_query(
            schema_ddl=schema_ddl,
            seed_inserts=seed_inserts,
            expected_query=expected_query,
            student_query=expected_query,
            enforce_order=False,
        )
        if result.is_correct:
            passed += 1
        else:
            failed += 1
            if len(examples) < 3:
                examples.append((qid, result.error_message))
    except Exception as e:
        failed += 1
        if len(examples) < 3:
            examples.append((qid, f"ERROR: {e}"))

print(f"\nFirst 20 SQL results: passed={passed}, failed={failed}, skipped={skipped}")
for ex in examples:
    print(f"  {ex[0]}: {ex[1]}")

# Count how many have schema_ddl
has_schema = sum(1 for q in has_tests if q.get("schema_ddl"))
print(f"\nOf {len(has_tests)} with testcases, {has_schema} have schema_ddl")
