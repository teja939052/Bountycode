"""Convert legacy `main` trust_status records in questions_bank.json to canonical statuses."""
import sys
sys.path.insert(0, ".")
import json
import asyncio
from app.services.auto_verify import verify_question

async def convert_main_in_file():
    bank_path = "app/data/questions_bank.json"
    with open(bank_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    main_qs = [q for q in questions if str(q.get("trust_status", "")).lower() == "main"]
    print(f"Found {len(main_qs)} 'main' status records in {bank_path}")
    
    if not main_qs:
        return
    
    converted = {
        "automated_checked": 0,
        "needs_review": 0,
        "verified": 0,
        "reviewed": 0,
        "unverified": 0,
    }
    
    for q in main_qs:
        qid = q.get("id", "unknown")
        try:
            assessment = verify_question(q)
            canonical_status = assessment.get("trust_status", "unverified")
        except Exception as e:
            print(f"  Error assessing {qid}: {e}")
            canonical_status = "unverified"
        
        # Map to canonical statuses
        if canonical_status not in ("verified", "reviewed", "automated_checked", "needs_review", "unverified"):
            canonical_status = "unverified"
        
        q["trust_status"] = canonical_status
        converted[canonical_status] = converted.get(canonical_status, 0) + 1
    
    # Write back
    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"Conversion complete and written to {bank_path}:")
    for status, count in sorted(converted.items()):
        print(f"  {status}: {count}")
    
    # Verify
    with open(bank_path, "r", encoding="utf-8") as f:
        verify = json.load(f)
    remaining_main = sum(1 for q in verify if str(q.get("trust_status", "")).lower() == "main")
    print(f"Remaining 'main' status: {remaining_main}")

if __name__ == "__main__":
    asyncio.run(convert_main_in_file())
