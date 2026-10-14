"""Run auto_verify on the expanded question banks."""
import asyncio
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.services import question_store
from app.services.auto_verify import verify_all_questions

async def main():
    print("Loading question store...")
    question_store.load_all()
    print(f"Loaded {len(question_store._questions)} questions")
    
    print("\nRunning auto_verify...")
    result = await verify_all_questions()
    
    print(f"\nVerification complete:")
    print(f"  Total:     {result.total}")
    print(f"  Passed:    {result.passed}")
    print(f"  Failed:    {result.failed}")
    print(f"  Quarantined: {result.quarantined}")
    print(f"  Skipped:   {result.skipped}")
    
    if result.details:
        print(f"\nFirst 10 failures:")
        for detail in result.details[:10]:
            print(f"  - {detail.get('id', 'unknown')}: {detail.get('reason', 'unknown')}")
    
    # Save results
    import json
    from datetime import datetime, timezone
    results_path = os.path.join(backend_dir, "app", "data", "auto_verify_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {results_path}")

if __name__ == "__main__":
    asyncio.run(main())
