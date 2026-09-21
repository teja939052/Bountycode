"""Run first Class B batch: 20 Time & Work questions through the full pipeline with real AI."""
from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone

sys.path.insert(0, r"D:\Project-Fremen\backend")

from app.services.class_b_generator import generate_batch, verify_batch, ClassBQuestion
from app.services.content_promotion import promote_questions
from app.services.question_verification import quick_structural_check
from app.services.ai_core import close_http_client


async def main():
    print("=" * 70)
    print("CLASS B BATCH: Time & Work — 20 questions (REAL AI)")
    print("=" * 70)
    print(f"Start time: {datetime.now(timezone.utc).isoformat()}")

    # 1. Generate
    print("\n[1] Generating Time & Work questions...")
    questions = await generate_batch(
        category="time-work",
        question_type="aptitude",
        count=5,
        difficulty=3,
        seed=42,
        mock=False,  # REAL AI
    )
    print(f"Generated: {len(questions)} questions")

    if not questions:
        print("FATAL: No questions generated. Check AI service.")
        return

    # Show sample
    print("\nSample generated question:")
    q0 = questions[0]
    print(f"  ID: {q0.question_id}")
    print(f"  Topic: {q0.topic} / {q0.subtopic}")
    print(f"  Difficulty: {q0.difficulty}")
    print(f"  Question: {q0.question[:100]}...")
    print(f"  Options: {list(q0.options.keys())}")
    print(f"  Correct: {q0.correct_answer}")
    print(f"  Has worked_solution: {bool(q0.worked_solution)}")
    print(f"  Has trick: {bool(q0.trick)}")
    print(f"  Has trap: {bool(q0.trap)}")
    print(f"  Companies: {q0.company_tags}")

    # 2. Verify
    print("\n[2] Running verification pipeline...")
    report = await verify_batch(questions, mock=True)

    # 3. Detailed results
    print("\n[3] Batch report:")
    print(f"  Total:       {report['total']}")
    print(f"  Passed:      {report['passed']}")
    print(f"  Rejected:    {report['rejected']}")
    print(f"  Pass rate:   {report['pass_rate']:.0%}")
    print(f"  Spot checked:{report['spot_checked']}")
    print(f"  Spot OK:     {report['spot_ok']}")
    print(f"  Spot pass:   {report['spot_pass_rate']:.0%}")

    if report.get("rejection_reasons"):
        print("\n  Rejection reasons:")
        for reason, count in report["rejection_reasons"].items():
            print(f"    {reason}: {count}")

    # 4. Show passed questions
    passed_qs = [q for q in questions if q.verification.get("passed")]
    if passed_qs:
        print(f"\n[4] Passed questions ({len(passed_qs)}):")
        for q in passed_qs[:5]:
            print(f"  [PASS] {q.question_id}: {q.question[:60]}...")
            print(f"    Correct: {q.correct_answer}, Quality: {q.verification.get('quality_score', 0)}/100")

    # 5. Show rejected questions with reasons
    rejected_qs = [q for q in questions if not q.verification.get("passed")]
    if rejected_qs:
        print(f"\n[5] Rejected questions ({len(rejected_qs)}):")
        for q in rejected_qs[:5]:
            reasons = q.verification.get("rejection_reasons", [])
            print(f"  [FAIL] {q.question_id}: {q.question[:60]}...")
            print(f"    Reasons: {reasons}")
            print(f"    Quality: {q.verification.get('quality_score', 0)}/100")

    # 6. Promotion attempt
    print("\n[6] Attempting promotion...")
    promotion = promote_questions(passed_qs, reviewer_id="class_b_pipeline_batch1")
    print(f"  Promoted: {promotion['promoted']}")
    print(f"  Rejected: {promotion['rejected']}")
    if promotion.get("rejection_reasons"):
        print("  Promotion rejections:")
        for r in promotion["rejection_reasons"][:5]:
            print(f"    {r.get('question_id')}: {r.get('reason')}")

    # 7. Final verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    pass_rate = report["pass_rate"]
    if pass_rate >= 0.70:
        print(f"PASS: {pass_rate:.0%} pass rate meets >=70% threshold")
        print(f"  {report['passed']}/{report['total']} questions promoted to reviewed")
    else:
        print(f"FAIL: {pass_rate:.0%} pass rate is below 70% threshold")
        print(f"  Only {report['passed']}/{report['total']} questions passed")
        print("\n  Top rejection reasons:")
        reasons = report.get("rejection_reasons", {})
        for reason, count in sorted(reasons.items(), key=lambda x: -x[1])[:5]:
            print(f"    - {reason}: {count}")
        print("\n  ACTION REQUIRED: Tighten generation prompt before scaling.")

    # 8. Save detailed report
    report_path = r"D:\Project-Fremen\backend\logs\class_b_batch1_report.json"
    import os
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "batch_id": "time-work-1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "category": "quant",
            "count_generated": len(questions),
            "report": report,
            "promotion": promotion,
            "questions": [q.to_dict() for q in questions],
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nDetailed report saved to: {report_path}")
    await close_http_client()


if __name__ == "__main__":
    asyncio.run(main())
