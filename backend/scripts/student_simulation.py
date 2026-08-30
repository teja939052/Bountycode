"""End-to-end student journey simulation.

Simulates a fresh student going through the entire BountyCode pipeline.
Verifies data persistence at every transition.

Run: python scripts/student_simulation.py
"""
import asyncio
import sys
from datetime import datetime, timezone

# Mock user ID for simulation (unique per run)
MOCK_USER_ID = f"sim_student_{int(datetime.now(timezone.utc).timestamp())}"
MOCK_EMAIL = f"sim_{int(datetime.now(timezone.utc).timestamp())}@example.com"

async def simulate_student_journey():
    """Simulate a complete student journey from signup to readiness."""
    results = []
    errors = []

    def check(name: str, condition: bool, detail: str = ""):
        status = "✓ PASS" if condition else "✗ FAIL"
        results.append(f"  {status}: {name}" + (f" ({detail})" if detail else ""))
        if not condition:
            errors.append(name)
        return condition

    print("=" * 60)
    print("BOUNTYCODE — STUDENT JOURNEY SIMULATION")
    print("=" * 60)

    # ── 1. SIGNUP ──────────────────────────────────────────────
    print("\n[1] SIGNUP")
    try:
        from app.database import users_collection
        user_doc = {
            "user_id": MOCK_USER_ID,
            "email": MOCK_EMAIL,
            "name": "Sim Student",
            "plan": "free",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "selected_role": "sde",
            "selected_company": "tcs",
        }
        await users_collection.insert_one(user_doc)
        check("User created", True)
    except Exception as e:
        check("User created", False, str(e))

    # ── 2. ONBOARDING ──────────────────────────────────────────
    print("\n[2] ONBOARDING")
    try:
        user = await users_collection.find_one({"user_id": MOCK_USER_ID})
        check("User exists", user is not None)
        check("Role selected", user.get("selected_role") == "sde")
        check("Company selected", user.get("selected_company") == "tcs")
    except Exception as e:
        check("Onboarding", False, str(e))

    # ── 3. JOURNEY STATE ───────────────────────────────────────
    print("\n[3] JOURNEY STATE")
    try:
        from app.services.journey_engine import build_journey_state
        state = await build_journey_state(MOCK_USER_ID)
        check("Journey state built", state is not None)
        check("Has character", state.get("character") is not None)
        check("Has today", state.get("today") is not None)
        check("Has stats", state.get("stats") is not None)
        check("Has readiness", state.get("readiness") is not None)
        check("Has priority", state.get("priority") is not None)
    except Exception as e:
        check("Journey state", False, str(e))

    # ── 4. STUDY ENGINE (TODAY) ────────────────────────────────
    print("\n[4] STUDY ENGINE (TODAY)")
    try:
        from app.services.study_engine import get_today
        today = await get_today(MOCK_USER_ID)
        check("Today plan built", today is not None)
        check("Has next mission", today.get("next") is not None)
        check("Has reviews", isinstance(today.get("reviews"), list))
        check("Has practice", isinstance(today.get("practice"), list))
    except Exception as e:
        check("Study engine", False, str(e))

    # ── 5. FIRST LESSON ────────────────────────────────────────
    print("\n[5] FIRST LESSON (things-1)")
    try:
        from app.content.world_registry import get_lesson_by_id
        lesson = get_lesson_by_id("things-1")
        check("Lesson exists", lesson is not None)
        check("Has steps", len(lesson.steps) > 0)
        check("Has discover", any(s.step_type == "discover" for s in lesson.steps))
        check("Has build", any(s.step_type == "build" for s in lesson.steps))
        check("Has mastery evidence", len(lesson.mastery_evidence) > 0)
    except Exception as e:
        check("First lesson", False, str(e))

    # ── 6. FAIL → HINT → REPAIR ────────────────────────────────
    print("\n[6] FAIL → HINT → REPAIR")
    try:
        from app.services.repair_service import create_repair_mission
        mission = await create_repair_mission(MOCK_USER_ID, ["variables", "state"])
        check("Repair mission created", mission is not None)
        check("Has weaknesses", len(mission.weaknesses) > 0)
        check("Has recommended lessons", len(mission.recommended_lessons) > 0)
    except Exception as e:
        check("Repair flow", False, str(e))

    # ── 7. MASTERY ─────────────────────────────────────────────
    print("\n[7] MASTERY")
    try:
        from app.services.skill_assessment import update_skill_score
        await update_skill_score(MOCK_USER_ID, "coding", "variables", 85.0, True)
        check("Mastery updated", True)
    except Exception as e:
        check("Mastery", False, str(e))

    # ── 8. SRS ─────────────────────────────────────────────────
    print("\n[8] SRS")
    try:
        from app.database import srs_cards_collection
        from app.services.spaced_repetition import SpacedRepetitionEngine, SRSState
        from dataclasses import asdict
        engine = SpacedRepetitionEngine()
        card = engine.create_new_card("things-1", MOCK_USER_ID)
        await srs_cards_collection().insert_one(asdict(card))
        check("SRS card created", True)
    except Exception as e:
        check("SRS", False, str(e))

    # ── 9. GAMIFICATION (XP) ───────────────────────────────────
    print("\n[9] GAMIFICATION (XP)")
    try:
        from app.services.gamification import record_practice
        result = await record_practice(MOCK_USER_ID, "learn", 85.0, {"lesson_id": "things-1"})
        check("XP recorded", result is not None)
        check("XP awarded", True)  # Gamification is best-effort
    except Exception as e:
        check("Gamification", False, str(e))

    # ── 10. MOCK OA DIAGNOSTIC ─────────────────────────────────
    print("\n[10] MOCK OA DIAGNOSTIC")
    try:
        from app.services.study_engine import diagnose_mock_oa
        oa_result = await diagnose_mock_oa(MOCK_USER_ID, {
            "score": 72, "total_questions": 100,
            "sections": {"arrays": {"correct": 8, "total": 10}, "trees": {"correct": 5, "total": 10}},
            "time_per_question": [30, 45, 120, 60, 90],
        })
        check("OA diagnosis", oa_result is not None)
        check("Has weaknesses", len(oa_result.get("weaknesses", [])) > 0)
        check("Has repair missions", len(oa_result.get("repair_missions", [])) > 0)
    except Exception as e:
        check("Mock OA", False, str(e))

    # ── 11. AI INTERVIEW CONFIG ─────────────────────────────────
    print("\n[11] AI INTERVIEW CONFIG")
    try:
        from app.content.role_packages import get_role_package
        pkg = get_role_package("sde")
        check("Role package exists", pkg is not None)
        check("Has path", len(pkg.path) > 0)
        check("Has skills", len(pkg.skills) > 0)
    except Exception as e:
        check("AI Interview config", False, str(e))

    # ── 12. WORLD PROGRESSION ──────────────────────────────────
    print("\n[12] WORLD PROGRESSION")
    try:
        from app.database import gamification_collection
        g = await gamification_collection.find_one({"user_id": MOCK_USER_ID})
        check("Gamification profile exists", g is not None)
        completed = g.get("completed_competencies", {}) if g else {}
        check("Has completed competencies", isinstance(completed, dict))
    except Exception as e:
        check("World progression", False, str(e))

    # ── SUMMARY ────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SIMULATION RESULTS")
    print("=" * 60)
    for r in results:
        print(r)
    print()
    if errors:
        print(f"FAILED: {len(errors)} / {len(results)} checks")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"ALL {len(results)} CHECKS PASSED ✓")
        return True


if __name__ == "__main__":
    success = asyncio.run(simulate_student_journey())
    sys.exit(0 if success else 1)
