"""Convert legacy `main` trust_status records to canonical statuses."""
import sys
sys.path.insert(0, ".")
import asyncio

async def convert_main_status():
    import app.services.question_store as qs
    qs.load_all()
    
    main_qs = [q for q in qs._questions if str(q.get("trust_status", "")).lower() == "main"]
    print(f"Converting {len(main_qs)} legacy 'main' status records...")
    
    if not main_qs:
        print("No 'main' status records found after load_all().")
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
        qtype = str(q.get("type", "")).lower()
        
        # Run quality assessment
        try:
            from app.services.auto_verify import verify_question
            assessment = verify_question(q)
            canonical_status = assessment.get("trust_status", "unverified")
        except Exception as e:
            print(f"  Error assessing {qid}: {e}")
            canonical_status = "unverified"
        
        # Map to canonical statuses
        if canonical_status not in ("verified", "reviewed", "automated_checked", "needs_review", "unverified"):
            canonical_status = "unverified"
        
        # Update in-memory
        q["trust_status"] = canonical_status
        converted[canonical_status] = converted.get(canonical_status, 0) + 1
    
    print(f"Conversion complete:")
    for status, count in sorted(converted.items()):
        print(f"  {status}: {count}")
    
    # Verify all converted
    remaining_main = sum(1 for q in qs._questions if str(q.get("trust_status", "")).lower() == "main")
    print(f"Remaining 'main' status: {remaining_main}")

if __name__ == "__main__":
    asyncio.run(convert_main_status())
