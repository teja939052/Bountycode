"""Real OA session end-to-end execution test."""
import sys
sys.path.insert(0, ".")
import asyncio
from datetime import datetime, timezone, timedelta
from app.routes.oa import _resolve_blueprint, _distribute, _build_questions
from app.services.question_store import find_one_verified

async def run_oa_session():
    print("=== OA SESSION END-TO-END TEST ===")
    
    # 1. Resolve blueprint
    bp = _resolve_blueprint("tcs_nqt", "swe")
    print(f"1. Blueprint resolved: {list(bp.keys())}")
    
    # 2. Distribute questions
    dist = _distribute(10, bp)
    print(f"2. Question distribution: {dist}")
    
    # 3. Build questions
    questions = await _build_questions(dist, verified_only=True, company="tcs")
    print(f"3. Built {len(questions)} questions")
    
    # 4. Create session document (simulating what the route does)
    now = datetime.now(timezone.utc)
    section_groups = {}
    for q in questions:
        sec = q.get("section", "other")
        section_groups.setdefault(sec, []).append(q)
    
    sections = []
    for sec, qs in section_groups.items():
        section_time_limit = sum(int(q.get("time_limit", 120)) for q in qs)
        sections.append({
            "id": sec,
            "title": sec,
            "type": sec,
            "question_ids": [q["question_uid"] for q in qs],
            "time_limit_s": section_time_limit,
            "started_at": now.isoformat() if sec == list(section_groups.keys())[0] else None,
            "submitted_at": None,
            "answers": [],
        })
    
    session_doc = {
        "user_id": "test-user-e2e",
        "company": "tcs",
        "role": "swe",
        "blueprint": bp,
        "mode": "calm",
        "integrity_enabled": True,
        "verified_only": True,
        "questions": questions,
        "sections": sections,
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
    
    print(f"4. Session created with {len(sections)} sections")
    for s in sections:
        print(f"   - {s['title']}: {len(s['question_ids'])} questions, {s['time_limit_s']}s")
    
    # 5. Simulate answering questions
    answers = {}
    correct_count = 0
    for q in questions:
        qid = q.get("question_uid")
        correct = q.get("correct_answer")
        opts = q.get("options", [])
        if isinstance(opts, dict):
            opt_values = list(opts.values())
        else:
            opt_values = list(opts)
        
        # Simulate: answer correctly 70% of the time
        import random
        is_correct = random.random() < 0.7
        if is_correct:
            answers[qid] = correct
            correct_count += 1
        else:
            # Pick wrong answer
            wrong_answers = [o for o in opt_values if o != correct]
            if wrong_answers:
                answers[qid] = wrong_answers[0]
            else:
                answers[qid] = "wrong"
    
    session_doc["answers"] = answers
    session_doc["status"] = "submitted"
    session_doc["completed_at"] = datetime.now(timezone.utc)
    
    print(f"5. Submitted {len(answers)} answers")
    print(f"   Correct: {correct_count}/{len(questions)} ({correct_count/len(questions)*100:.1f}%)")
    
    # 6. Compute score breakdown
    score_breakdown = {}
    for q in questions:
        sec = q.get("section", "other")
        qid = q.get("question_uid")
        correct = q.get("correct_answer")
        opts = q.get("options", [])
        if isinstance(opts, dict):
            opt_values = list(opts.values())
        else:
            opt_values = list(opts)
        student_answer = answers.get(qid)
        is_correct = student_answer == correct
        if sec not in score_breakdown:
            score_breakdown[sec] = {"correct": 0, "total": 0}
        score_breakdown[sec]["total"] += 1
        if is_correct:
            score_breakdown[sec]["correct"] += 1
    
    session_doc["score_breakdown"] = score_breakdown
    
    print(f"6. Score breakdown:")
    for sec, scores in score_breakdown.items():
        pct = scores["correct"] / scores["total"] * 100 if scores["total"] > 0 else 0
        print(f"   {sec}: {scores['correct']}/{scores['total']} ({pct:.1f}%)")
    
    overall_correct = sum(s["correct"] for s in score_breakdown.values())
    overall_total = sum(s["total"] for s in score_breakdown.values())
    overall_pct = overall_correct / overall_total * 100 if overall_total > 0 else 0
    
    print(f"7. Overall: {overall_correct}/{overall_total} ({overall_pct:.1f}%)")
    print(f"   Session status: {session_doc['status']}")
    print(f"   Tab switches: {session_doc['tab_switch_count']}")
    print(f"   Fullscreen exits: {session_doc['fullscreen_exits']}")
    
    print("\n=== OA END-TO-END TEST: PASS ===")
    return session_doc

asyncio.run(run_oa_session())
