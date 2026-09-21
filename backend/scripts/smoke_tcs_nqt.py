"""Quick smoke test for TCS NQT verified bank serving."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.question_store import (
    count_documents,
    find_one,
    find_one_verified,
    get_question_for_serving,
    load_all,
)


def main() -> int:
    load_all()
    total = count_documents()
    tcs_total = count_documents({"company": {"$in": ["TCS"]}})
    tcs_servable = count_documents({
        "company": {"$in": ["TCS"]},
        "trust_status": {"$in": ["verified", "automated_checked", "reviewed"]},
    })

    print(f"Total questions in store: {total}")
    print(f"TCS questions: {tcs_total}")
    print(f"TCS serveable (verified+): {tcs_servable}")

    sample = find_one_verified({"company": {"$in": ["TCS"]}})
    if sample:
        print(f"\nSample serveable TCS question:")
        print(f"  id: {sample.get('id')}")
        print(f"  type: {sample.get('type')}")
        print(f"  trust_status: {sample.get('trust_status')}")
        print(f"  question: {str(sample.get('question') or sample.get('question_title') or '')[:80]}")
        print(f"  source_bank: {sample.get('source_bank')}")
    else:
        print("\nNo serveable TCS question found!")
        return 1

    mcq = find_one_verified({"company": {"$in": ["TCS"]}, "source_bank": "tcs_nqt_all"})
    if mcq:
        print(f"\nMCQ bank sample:")
        print(f"  id: {mcq.get('id')}")
        print(f"  options: {mcq.get('options')}")
        print(f"  correct_answer: {mcq.get('correct_answer')}")
        print(f"  trust_status: {mcq.get('trust_status')}")
    else:
        print("\nNo MCQ bank sample found!")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
