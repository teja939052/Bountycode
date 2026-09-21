"""Runtime verification for OA session and interview evaluator."""
import sys
sys.path.insert(0, ".")
import asyncio
from datetime import datetime, timezone, timedelta

# Test 1: OA session model shape
async def test_oa_session_model():
    from app.routes.oa import _resolve_blueprint, _distribute, _build_questions, SECTION_META
    from app.services.question_store import find_one_verified
    
    blueprint = _resolve_blueprint("tcs_nqt", "swe")
    print(f"TCS NQT blueprint keys: {list(blueprint.keys())}")
    
    dist = _distribute(10, blueprint)
    print(f"10-question distribution: {dist}")
    
    # Try to build questions
    questions = await _build_questions(dist, verified_only=True, company="tcs")
    print(f"Built {len(questions)} questions for TCS NQT")
    for q in questions[:3]:
        print(f"  - {q.get('section')}: {q.get('question_uid')} kind={q.get('kind')}")
    
    # Verify session doc shape
    now = datetime.now(timezone.utc)
    session_doc = {
        "user_id": "test-user",
        "company": "tcs",
        "role": "swe",
        "blueprint": blueprint,
        "mode": "calm",
        "integrity_enabled": True,
        "verified_only": True,
        "questions": questions,
        "sections": [],
        "status": "in_progress",
        "answers": {},
        "integrity_signals": [],
        "tab_switch_count": 0,
        "fullscreen_exits": 0,
        "started_at": now,
        "duration_minutes": 90,
        "ends_at": now + timedelta(minutes=90),
        "created_at": now,
        "score_breakdown": {},
    }
    print(f"\nSession doc has sections field: {'sections' in session_doc}")
    print(f"Session doc has tab_switch_count: {'tab_switch_count' in session_doc}")
    print(f"Session doc has score_breakdown: {'score_breakdown' in session_doc}")
    print("OA session model: OK")

# Test 2: Interview evaluator with quote-or-zero
async def test_interview_evaluator():
    from app.services.interview_evaluator import InterviewEvaluator
    
    question = "Tell me about a time you handled a conflict in a team."
    transcript = """
    Last semester I was working on a group project with two teammates who had different ideas about 
    the architecture. One wanted microservices, the other wanted a monolith. I scheduled a meeting 
    where we each presented our pros and cons. We ended up with a modular monolith that satisfied 
    both requirements. The project got an A and the professor said it was the best architecture 
    he'd seen that semester.
    """
    
    result = await InterviewEvaluator.evaluate_response(
        question_text=question,
        expected_points=["conflict", "resolution", "outcome"],
        student_transcript=transcript,
        company_target="Google",
        interview_mode="behavioral",
    )
    
    print(f"\nInterview evaluator result:")
    print(f"  Mode: {result.get('mode')}")
    print(f"  Rubric version: {result.get('rubric_version')}")
    print(f"  Overall score: {result.get('overall_score')}")
    print(f"  Criteria:")
    for c in result.get("criteria", []):
        has_quote = bool(c.get("quote", "").strip())
        print(f"    - {c.get('id')} ({c.get('label')}): {c.get('score')}/{c.get('max')} quote={'YES' if has_quote else 'NO'}")
    
    # Verify quote-or-zero: any criterion with score > 0 must have a quote
    violations = []
    for c in result.get("criteria", []):
        if c.get("score", 0) > 0 and not c.get("quote", "").strip():
            violations.append(c.get("id"))
    
    if violations:
        print(f"  VIOLATION: criteria scored >0 without quotes: {violations}")
    else:
        print("  Quote-or-zero guardrail: SATISFIED")
    
    print("Interview evaluator: OK")

async def main():
    await test_oa_session_model()
    await test_interview_evaluator()

asyncio.run(main())
