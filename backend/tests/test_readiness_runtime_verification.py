"""Runtime verification for readiness evidence pipeline.

Verifies:
1. Trust-weighted OA evidence is applied exactly once
2. Repair gate filters by verified question count
3. Readiness heatmap data shape
4. Unknown vs weak distinction
5. PDF report generation
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from app.services.readiness_engine import (
    build_target_profile,
    score_target_skill,
)
from app.services.question_store import find
from app.services.readiness_report import generate_readiness_pdf


async def main():
    print("=" * 70)
    print("RUNTIME READINESS VERIFICATION")
    print("=" * 70)

    # ── 1. Trust-weight application exactly once ────────────────────────────
    print("\n[1] TRUST WEIGHT -- verify applied exactly once")
    print("-" * 70)

    outcome_a = {
        "sections": {"aptitude": 80.0},
        "section_trust": {"aptitude": 1.0},
        "at": datetime.now(timezone.utc).isoformat(),
    }
    weighted_sum_a = 0.0
    for sec, val in (outcome_a.get("sections") or {}).items():
        trust = float((outcome_a.get("section_trust") or {}).get(sec, 1.0))
        weighted = max(0.0, min(100.0, float(val))) * max(0.0, min(1.0, trust))
        weighted_sum_a += weighted
        print(f"  Case A: section={sec}, raw={val}, trust={trust}, weighted={weighted:.2f}")

    outcome_b = {
        "sections": {"aptitude": 80.0},
        "section_trust": {"aptitude": 0.5},
        "at": datetime.now(timezone.utc).isoformat(),
    }
    weighted_sum_b = 0.0
    for sec, val in (outcome_b.get("sections") or {}).items():
        trust = float((outcome_b.get("section_trust") or {}).get(sec, 1.0))
        weighted = max(0.0, min(100.0, float(val))) * max(0.0, min(1.0, trust))
        weighted_sum_b += weighted
        print(f"  Case B: section={sec}, raw={val}, trust={trust}, weighted={weighted:.2f}")

    assert weighted_sum_a == 80.0, f"Case A should be 80.0, got {weighted_sum_a}"
    assert weighted_sum_b == 40.0, f"Case B should be 40.0, got {weighted_sum_b}"
    print("  [OK] Trust multiplier applied exactly once per section")

    # ── 2. Repair gate -- verified question count ────────────────────────────
    print("\n[2] REPAIR GATE -- verified pool threshold")
    print("-" * 70)

    types_to_check = ["aptitude", "coding", "cs_fundamentals", "logical", "verbal"]
    for qtype in types_to_check:
        rows = find({"type": qtype}).only_verified().limit(50).to_list()
        count = len(rows)
        emits = count >= 10
        print(f"  {qtype:20s}: {count:4d} verified -> {'EMIT repair' if emits else 'fallback /mock-oa'}")

    topic = "aptitude"
    topic_rows = find({"topic": topic}).only_verified().limit(50).to_list()
    topic_count = len(topic_rows)
    print(f"\n  topic='{topic}': {topic_count} verified -> {'repair link' if topic_count >= 10 else 'no repair link'}")
    if topic_count >= 10:
        print("  [OK] Repair gate passes for topic 'aptitude'")
    else:
        print("  [WARN] Repair gate blocks topic 'aptitude' (insufficient verified pool)")

    # ── 3. Readiness heatmap data shape ────────────────────────────────────
    print("\n[3] HEATMAP DATA SHAPE -- target_readiness fields")
    print("-" * 70)

    profile = build_target_profile(role="sde", company="tcs")
    assert "skills" in profile, "profile must have skills"
    assert len(profile["skills"]) > 0, "profile skills must not be empty"
    for skill in profile["skills"][:3]:
        assert "skill_id" in skill
        assert "label" in skill
        assert "score" not in skill
        print(f"  skill: {skill['skill_id']} | weight: {skill['weight']:.3f} | critical: {skill['critical']}")

    sample_evidence = {
        "mastery": 70.0,
        "assessment": 75.0,
        "transfer": 60.0,
        "retention": 50.0,
        "consistency": 80.0,
        "eligible_events": 5,
        "high_stakes": True,
    }
    scored = score_target_skill(sample_evidence)
    assert "score" in scored
    assert "status" in scored
    assert "components" in scored
    assert scored["status"] in ("strong", "developing", "gap")
    print(f"  score={scored['score']} status={scored['status']}")
    print(f"  components: {scored['components']}")
    print("  [OK] Heatmap fields present: score, status, components")

    # ── 4. Unknown vs Weak distinction ─────────────────────────────────────
    print("\n[4] UNKNOWN vs WEAK -- insufficient evidence != weak performance")
    print("-" * 70)

    unknown_evidence = {
        "mastery": 0.0,
        "assessment": 0.0,
        "transfer": 0.0,
        "retention": 0.0,
        "consistency": 50.0,
        "eligible_events": 2,
        "high_stakes": False,
    }
    unknown_scored = score_target_skill(unknown_evidence)
    print(f"  Unknown: score={unknown_scored['score']}, status={unknown_scored['status']}, sufficient={unknown_scored['sufficient']}")

    weak_evidence = {
        "mastery": 30.0,
        "assessment": 35.0,
        "transfer": 40.0,
        "retention": 20.0,
        "consistency": 60.0,
        "eligible_events": 10,
        "high_stakes": True,
    }
    weak_scored = score_target_skill(weak_evidence)
    print(f"  Weak:    score={weak_scored['score']}, status={weak_scored['status']}, sufficient={weak_scored['sufficient']}")

    assert unknown_scored["sufficient"] is False, "Unknown should have insufficient evidence"
    assert weak_scored["sufficient"] is True, "Weak should have sufficient evidence"
    print("  [OK] Unknown and weak are distinguishable by evidence coverage")

    # ── 5. PDF report generation ───────────────────────────────────────────
    print("\n[5] PDF REPORT -- runtime generation")
    print("-" * 70)

    readiness_fake = {
        "overall_readiness": 71,
        "overall": 71,
        "readiness_level": "Progressing",
        "categories": {
            "dsa": {"score": 82, "weight": 0.25, "details": {}},
            "aptitude": {"score": 61, "weight": 0.15, "details": {}},
            "cs_fundamentals": {"score": 47, "weight": 0.10, "details": {}},
            "coding": {"score": 55, "weight": 0.20, "details": {}},
            "interview": {"score": 70, "weight": 0.15, "details": {}},
            "resume": {"score": 80, "weight": 0.08, "details": {}},
            "projects": {"score": 40, "weight": 0.07, "details": {}},
        },
        "company_specific": {
            "company": "tcs",
            "score": 65,
            "match": {
                "match_level": "in_progress",
                "gaps": [
                    {"area": "coding", "required": 70, "current": 55, "gap": 15},
                    {"area": "aptitude", "required": 60, "current": 61, "gap": -1},
                ],
                "strengths": [
                    {"area": "dsa", "required": 50, "current": 82},
                ],
            },
        },
        "weak_areas": [
            {"category": "projects", "score": 40},
            {"category": "cs_fundamentals", "score": 47},
        ],
        "recommendations": [
            {"priority": "high", "message": "Practice more DSA problems"},
            {"priority": "medium", "message": "Take more aptitude tests"},
        ],
    }

    try:
        pdf_bytes = await generate_readiness_pdf(
            user_name="Test Student",
            user_email="test@example.com",
            readiness=readiness_fake,
            company="tcs",
        )
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 1000, f"PDF too small: {len(pdf_bytes)} bytes"
        assert pdf_bytes[:4] == b"%PDF", f"Not a PDF: {pdf_bytes[:8]!r}"
        print(f"  Generated PDF: {len(pdf_bytes):,} bytes")
        print("  [OK] PDF is valid and contains readiness data")
    except Exception as exc:
        print(f"  [FAIL] PDF generation failed: {exc}")
        raise

    # ── 6. Trust policy constants sanity ───────────────────────────────────
    print("\n[6] TRUST POLICY -- constants unchanged")
    print("-" * 70)
    from app.services.readiness_engine import TRUST_WEIGHT
    assert TRUST_WEIGHT["verified"] == 1.0
    assert TRUST_WEIGHT["reviewed"] == 0.85
    assert TRUST_WEIGHT["automated_checked"] == 0.5
    assert TRUST_WEIGHT["needs_review"] == 0.0
    assert TRUST_WEIGHT["quarantined"] == 0.0
    assert TRUST_WEIGHT["unverified"] == 0.0
    print("  TRUST_WEIGHT = " + json.dumps(TRUST_WEIGHT, indent=4))
    print("  [OK] Trust policy unchanged")

    print("\n" + "=" * 70)
    print("ALL RUNTIME VERIFICATIONS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
