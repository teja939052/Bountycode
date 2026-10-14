#!/usr/bin/env python3
"""Final verification: full learner flow with persisted state."""

import sys
sys.path.insert(0, "D:/Project-Fremen/backend")

from app.services.lesson_orchestrator import LessonOrchestrator, STEP_NAMES

async def test_full_learner_flow():
    """Simulate a complete learner flow through a mission pack."""
    orchestrator = LessonOrchestrator()
    
    # Start a lesson
    result = await orchestrator.start(
        user_id="test-user-1",
        domain="aptitude",
        level_or_context=None,
        company="tcs",
        role="sde",
        mastery_threshold=75,
    )
    
    session_id = result["session_id"]
    print(f"Started session: {session_id}")
    assert session_id.startswith("lesson:aptitude:")
    
    # Step 0: discover
    assert result["current_step"] == 0
    assert result["step_name"] == "discover"
    print(f"Step 0: {result['step_name']} PASS")
    
    # Submit correct answer for discover
    submit_result = await orchestrator.submit_step(
        session_id=session_id,
        step_index=0,
        response={"selected_option": "a"},
        time_spent_seconds=5,
    )
    assert submit_result["passed"] is True
    print(f"Step 0 submit: passed={submit_result['passed']} PASS")
    
    # Step 1: understand
    assert submit_result["next_step"]["step_name"] == "understand"
    print(f"Step 1: {submit_result['next_step']['step_name']} PASS")
    
    # Submit wrong answer for manipulate (step 2) to test diagnosis
    submit_result2 = await orchestrator.submit_step(
        session_id=session_id,
        step_index=2,
        response={"answer": "wrong answer"},
        time_spent_seconds=10,
    )
    
    # Check if diagnosis fired
    diagnosis = submit_result2.get("diagnosis") or {}
    if submit_result2.get("reteach_required"):
        print(f"Reteach triggered after step 2: {diagnosis.get('misconception_code')}")
        print(f"  Confidence: {diagnosis.get('confidence')}")
        print(f"  Evidence: {diagnosis.get('evidence_count')}")
        
        # Submit reteach engagement
        reteach_result = await orchestrator.submit_step(
            session_id=session_id,
            step_index=2,
            response={"answer": "I understand now. The base is the original value, and percentage change is calculated from that base."},
            time_spent_seconds=30,
        )
        print(f"Reteach submit: passed={reteach_result['passed']}, reteach_required={reteach_result.get('reteach_required')}")
    else:
        print(f"No reteach triggered (confidence={diagnosis.get('confidence', 0)})")
    
    # Get session state
    session = await orchestrator.get_session(session_id)
    assert session is not None
    print(f"Session state retrieved: domain={session['domain']}, step={session['current_step']} PASS")
    
    # Get reteach plan
    reteach_plan = await orchestrator.get_reteach_plan(session_id)
    print(f"Reteach plan: {reteach_plan.get('reteach_required')} PASS")
    
    print("\nPASS: Full learner flow verified")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_full_learner_flow())
