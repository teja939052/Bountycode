from datetime import datetime, timezone
import logging
import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.interview import StartInterview, SubmitAnswer
from app.database import users_collection, interviews_collection, career_profiles_collection, oa_sessions_collection, skill_graph_collection
from app.middleware.auth import get_current_user
from app.services.ai_interview import (
    generate_interview_question,
    evaluate_answer,
    COMPANY_PROFILES,
)
from app.services.interview_evaluator import InterviewEvaluator
from app.services.interview_enhanced import (
    generate_follow_up_question,
    analyze_communication_style,
    generate_dynamic_difficulty,
)
from app.services.behavioral_enhanced import evaluate_star_answer
from app.services.gamification import record_practice
from app.config import get_settings
from bson import ObjectId

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/interview", tags=["interview"])
settings = get_settings()

TOTAL_QUESTIONS = 20
FOLLOW_UP_CHANCE = 0.4
MAX_FOLLOW_UPS_PER_QUESTION = 1


@router.post("/start")
async def start_interview(req: StartInterview, user=Depends(get_current_user)):
    if user.get("plan") == "free" and user.get("interviews_used", 0) >= settings.FREE_TIER_INTERVIEW_LIMIT:
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limit reached ({settings.FREE_TIER_INTERVIEW_LIMIT} interviews). Upgrade to Pro for unlimited.",
        )

    company = req.company.lower().strip() if req.company else "general"
    company_profile = COMPANY_PROFILES.get(company, {})
    company_style = company_profile.get("interview_style", "")

    mode = (req.interview_type or "mixed").lower().strip()
    # Resume/profile-aware questions: ground in the candidate's real background
    # (best-effort; empty when no profile exists — never blocks the interview).
    candidate_context = ""
    try:
        prof = await career_profiles_collection.find_one({"user_id": user["id"]}) or {}
        bits = []
        if prof.get("summary"):
            bits.append(f"Summary: {prof['summary'][:500]}")
        if prof.get("skills"):
            bits.append("Skills: " + ", ".join(prof["skills"][:20]))
        exp = prof.get("experience") or []
        if exp and isinstance(exp[0], dict):
            bits.append(
                "Latest experience: "
                + exp[0].get("title", "") + " at " + exp[0].get("company", "")
            )
        candidate_context = "\n".join(bits)
    except Exception:
        candidate_context = ""

    # Pull latest OA diagnosis for adaptive questioning (moat: interview probes real weaknesses)
    oa_context = {}
    try:
        latest_oa = await oa_sessions_collection.find_one(
            {"user_id": user["id"], "status": "completed"}, sort=[("completed_at", -1)]
        )
        if latest_oa:
            res = latest_oa.get("result", {}) or {}
            diag = res.get("diagnosis", {}) or {}
            if diag.get("skill_weaknesses") or diag.get("weaknesses"):
                oa_context = diag
    except Exception:
        pass

    interview_doc = {
        "user_id": user["id"],
        "job_role": req.job_role,
        "company": company,
        "interview_type": req.interview_type,
        "difficulty": req.difficulty,
        "questions": [],
        "status": "in_progress",
        "score_history": [],
        "difficulty_progression": [req.difficulty],
        "oa_context": oa_context,
        "created_at": datetime.now(timezone.utc),
    }
    result = await interviews_collection.insert_one(interview_doc)
    interview_id = str(result.inserted_id)

    # If OA revealed a primary weakness, probe it first (evidence-driven interview).
    # Generation failure rolls back: orphan session deleted, free-tier credit
    # untouched. Same no-loss rule as /answer's eval-pending path.
    try:
        if oa_context.get("primary_weakness") or oa_context.get("skill_weaknesses"):
            primary = oa_context.get("primary_weakness") or (oa_context.get("skill_weaknesses", [{}])[0].get("skill", ""))
            if primary:
                w = next((x for x in oa_context.get("skill_weaknesses", []) if x.get("skill")==primary), {})
                pct = w.get("pct", "")
                pct_str = f" (OA: {pct}%)" if pct else ""
                question_data = {
                    "question": f"You scored{pct_str} on {primary} in your recent Mock OA. Walk me through how you'd solve a {primary} problem and why a naive approach wouldn't scale.",
                    "question_type": "technical",
                    "tips": f"Focus on {primary} fundamentals; explain trade-offs.",
                    "difficulty": req.difficulty,
                }
            else:
                question_data = await generate_interview_question(
                    req.job_role, [], company=company, difficulty=req.difficulty, user_id=user["id"],
                    mode=mode, candidate_context=candidate_context or None,
                )
        else:
            question_data = await generate_interview_question(
                req.job_role, [], company=company, difficulty=req.difficulty,
            )
    except Exception as exc:
        logger.warning("interview start failed for %s, rolling back: %s", user["id"], exc)
        try:
            await interviews_collection.delete_one({"_id": ObjectId(interview_id)})
        except Exception:
            pass
        raise HTTPException(status_code=503, detail="Could not start interview right now. Please retry — no attempt was used.")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$inc": {"interviews_used": 1}},
    )

    return {
        "interview_id": interview_id,
        "question": question_data.get("question", "Tell me about yourself."),
        "question_type": question_data.get("question_type", "behavioral"),
        "tips": question_data.get("tips", ""),
        "difficulty": question_data.get("difficulty", req.difficulty),
        "company": company,
        "company_style": company_style,
        "total_questions": TOTAL_QUESTIONS,
    }


async def _update_interview_readiness(
    user_id: str, company: str, mode: str, overall: float, breakdown: dict
):
    """Best-effort: store interview outcomes as a readiness signal in the
    existing skill graph — same collection/shape convention as the OA signal
    (oa._update_readiness). No new store."""
    col = skill_graph_collection()
    doc = await col.find_one({"user_id": user_id})
    if not doc:
        doc = {"user_id": user_id, "categories": {}, "oa_outcomes": []}
    outcomes = doc.get("interview_outcomes", [])
    outcomes.append({
        "company": company,
        "mode": mode,
        "overall": overall,
        "breakdown": breakdown,
        "at": datetime.now(timezone.utc).isoformat(),
    })
    outcomes = outcomes[-20:]
    cats = doc.get("categories", {})
    prev = cats.get("interview", {})
    prev_score = prev.get("score", 0)
    cats["interview"] = {
        "score": round(prev_score * 0.6 + overall * 0.4, 1),
        "source": "interview",
    }
    await col.update_one(
        {"user_id": user_id},
        {"$set": {"categories": cats, "interview_outcomes": outcomes}},
        upsert=True,
    )


@router.post("/answer")
async def submit_answer(req: SubmitAnswer, user=Depends(get_current_user)):
    try:
        interview = await interviews_collection.find_one({"_id": ObjectId(req.interview_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid interview ID")

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if interview.get("status") == "completed":
        raise HTTPException(status_code=400, detail="Interview already completed")

    company = interview.get("company", "general")
    job_role = interview.get("job_role", "")
    current_difficulty = interview.get("difficulty", "medium")
    mode = (interview.get("interview_type") or "mixed").lower().strip()
    # Use the real question type sent by the client; follow-ups are behavioral
    # (probing deeper). Previously this was always "mixed", which gave the
    # evaluator no type-specific guidance.
    qtype = "behavioral" if req.is_follow_up else (req.question_type or "technical")

    # Prefer rubric-based evaluator for modes with explicit criteria
    rubric_feedback = None
    mode_key = (mode or qtype or "technical").lower().strip()
    if mode_key in {"behavioral", "hr", "technical", "system_design", "gd", "group_discussion"}:
        try:
            rubric_feedback = await InterviewEvaluator.evaluate_response(
                question_text=req.question,
                expected_points=[],
                student_transcript=req.answer,
                company_target=company,
                interview_mode=mode_key,
            )
        except Exception:
            rubric_feedback = None

    if rubric_feedback and not rubric_feedback.get("error"):
        overall_score = rubric_feedback.get("overall_score", 5)
        breakdown = {}
        for c in rubric_feedback.get("criteria", []):
            breakdown[c.get("id", c.get("label", ""))] = c.get("score", 0)
        if not breakdown:
            breakdown = {"overall": overall_score}
        feedback = {
            "score": overall_score,
            "breakdown": breakdown,
            "rubric_version": rubric_feedback.get("rubric_version", "1.0"),
            "criteria": rubric_feedback.get("criteria", []),
            "filler_words": rubric_feedback.get("filler_words", []),
            "structural_critique": rubric_feedback.get("critique", ""),
            "actionable_remediation": rubric_feedback.get("remediation", ""),
            "reaction": "thinking" if overall_score < 5 else ("muscle" if overall_score < 7 else "clap"),
        }
    else:
        # No rubric verdict (evaluator errored or returned error state).
        # One bounded AI fallback; if that also fails, the answer is STORED
        # as eval-pending and the client gets a retryable 200 — student text
        # is never lost to a 504, and pending answers never count as answered.
        try:
            feedback = await evaluate_answer(
                req.question, req.answer, job_role,
                company=company, question_type=qtype,
                difficulty=current_difficulty, time_taken=req.time_taken or 0,
                mode=mode,
            )
        except Exception as exc:
            logger.warning("interview eval failed for %s, storing pending: %s",
                           req.interview_id, exc)
            qa_pending = {
                "question": req.question,
                "answer": req.answer,
                "question_type": qtype,
                "difficulty": current_difficulty,
                "score": None,
                "breakdown": {},
                "feedback": None,
                "eval_pending": True,
                "is_follow_up": req.is_follow_up,
                "company": company,
                "time_taken": req.time_taken or 0,
            }
            await interviews_collection.update_one(
                {"_id": ObjectId(req.interview_id)},
                {"$push": {"questions": qa_pending}},
            )
            return {
                "interview_id": req.interview_id,
                "eval_pending": True,
                "feedback": {"message": "Grading hiccup — your answer is saved. Tap submit to retry grading."},
                "current_score": None,
                "questions_answered": len([
                    q for q in (interview.get("questions") or [])
                    if not q.get("is_follow_up") and not q.get("eval_pending")]),
                "total_questions": TOTAL_QUESTIONS,
                "finished": False,
                "is_follow_up": req.is_follow_up,
                "reaction": "",
                "breakdown": {},
                "next_question": req.question,
                "next_question_type": qtype,
                "next_tips": "",
                "next_difficulty": current_difficulty,
            }
        feedback = dict(feedback)
        feedback["degraded"] = True
        feedback["degraded_reason"] = "rubric_evaluator_unavailable"
        feedback.setdefault("score", 5)
        feedback.setdefault("breakdown", {})

    score = feedback.get("score", 5)
    breakdown = feedback.get("breakdown", {})
    reaction = feedback.get("reaction", "")

    if not breakdown:
        breakdown = {"technical": score, "communication": score, "problem_solving": score, "depth": score}

    qa_pair = {
        "question": req.question,
        "answer": req.answer,
        "question_type": qtype,
        "difficulty": current_difficulty,
        "score": score,
        "breakdown": breakdown,
        "feedback": feedback,
        "is_follow_up": req.is_follow_up,
        "company": company,
        "time_taken": req.time_taken or 0,
    }
    await interviews_collection.update_one(
        {"_id": ObjectId(req.interview_id)},
        {"$push": {"questions": qa_pair}},
    )

    # â”€â”€ Emit canonical LearningEvents for each scored dimension â”€â”€
    # The interview evaluator produces per-dimension scores (0-10).
    # Each dimension gets its own event with structured diagnosis codes
    # when the score indicates a gap.
    try:
        from app.services.study_engine import emit_learning_event
        from app.services.skill_taxonomy import parse_interview_dimension
        from app.services.diagnosis import diagnose_interview_failure

        question_id_for_event = None
        # Try to trace back the question_id from the interview doc
        if interview.get("questions"):
            question_id_for_event = interview.get("questions", [{}])[-1].get("question_id")

        for dim, dim_score in breakdown.items():
            if dim_score < 7:  # Below proficiency threshold
                codes = diagnose_interview_failure(
                    dimension=dim,
                    score=dim_score,
                    feedback=feedback,
                    answer_text=req.answer,
                    question_topic=getattr(req, "question_topic", None),
                )
                await emit_learning_event(user["id"], {
                    "activity_type": "interview_answer",
                    "source": "interview",
                    "skill_id": parse_interview_dimension(dim),
                    "question_id": question_id_for_event,
                    "assessment_id": req.interview_id,
                    "role": job_role,
                    "company": company,
                    "passed": dim_score >= 7,
                    "score": dim_score,
                    "time_spent_seconds": req.time_taken or 0,
                    "diagnosis_codes": codes,
                    "metadata": {
                        "question_type": qtype,
                        "difficulty": current_difficulty,
                        "overall_feedback": {
                            "strengths": feedback.get("strengths", []),
                            "improvements": feedback.get("improvements", []),
                        },
                    },
                })
    except Exception as exc:
        logger.warning("interview LearningEvent emission failed: %s", exc)

    updated_interview = await interviews_collection.find_one({"_id": ObjectId(req.interview_id)})
    history = updated_interview.get("questions", [])
    all_primary = [q for q in history if not q.get("is_follow_up") and not q.get("eval_pending")]
    questions_answered = len(all_primary)
    score_history = updated_interview.get("score_history", [])
    score_history.append(score)

    should_follow_up = (
        not req.is_follow_up
        and score >= 5
        and len([q for q in history if q.get("is_follow_up")]) < MAX_FOLLOW_UPS_PER_QUESTION
        and questions_answered < TOTAL_QUESTIONS
    )

    if should_follow_up:
        if random.random() < FOLLOW_UP_CHANCE:
            follow_up = await generate_follow_up_question(
                req.question, req.answer, job_role,
                [{"question": h["question"], "answer": h["answer"]} for h in history[-5:]],
                mode=mode,
            )

            await interviews_collection.update_one(
                {"_id": ObjectId(req.interview_id)},
                {"$set": {"score_history": score_history}},
            )

            return {
                "feedback": feedback,
                "next_question": follow_up.get("follow_up_question", ""),
                "next_question_type": "follow_up",
                "next_tips": follow_up.get("purpose", ""),
                "next_difficulty": follow_up.get("difficulty", "medium"),
                "current_score": round(sum(score_history) / len(score_history), 1),
                "questions_answered": questions_answered,
                "total_questions": TOTAL_QUESTIONS,
                "finished": False,
                "is_follow_up": True,
                "reaction": reaction,
                "breakdown": breakdown,
            }

    if questions_answered >= TOTAL_QUESTIONS:
        final_score = round(sum(score_history) / len(score_history), 1)
        await interviews_collection.update_one(
            {"_id": ObjectId(req.interview_id)},
            {"$set": {"status": "completed", "score_history": score_history}},
        )

        avg_breakdown = _average_breakdown([q.get("breakdown", {}) for q in history])
        strength_areas = feedback.get("strengths", [])
        improvement_areas = feedback.get("improvements", [])

        # --- Completion contract: competency-level diagnosis + next action ---
        # Bottom-2 dimensions become labeled weaknesses; they drive a repair
        # mission (score < 7) or a company-OA conversion step, and feed the
        # skill graph exactly like OA outcomes do. All best-effort.
        dim_labels = {
            "technical": "Technical Accuracy",
            "communication": "Communication & Delivery",
            "problem_solving": "Problem Solving",
            "depth": "Answer Depth",
        }
        ranked = sorted(avg_breakdown.items(), key=lambda kv: kv[1])
        weaknesses = [dim_labels.get(d, d) for d, _ in ranked[:2]]
        next_action = None
        if final_score < 7:
            try:
                from app.services.repair_service import create_repair_mission
                mission = await create_repair_mission(
                    user["id"], weaknesses, source="interview"
                )
                next_action = {
                    "type": "repair_mission",
                    "target": mission.title,
                    "reason": f"Repair weakest areas: {', '.join(weaknesses)}",
                }
            except Exception:
                next_action = {
                    "type": "practice",
                    "target": weaknesses[0] if weaknesses else "fundamentals",
                    "reason": "Targeted practice on weakest area",
                }
        else:
            next_action = {
                "type": "company_oa",
                "target": company,
                "reason": "Convert interview readiness into OA evidence",
            }
        try:
            await interviews_collection.update_one(
                {"_id": ObjectId(req.interview_id)},
                {"$set": {
                    "weaknesses": weaknesses,
                    "next_action": next_action,
                    "overall_score": final_score,
                }},
            )
        except Exception:
            pass
        try:
            await _update_interview_readiness(
                user["id"], company, mode, final_score, avg_breakdown
            )
        except Exception:
            pass

        gamification_result = await record_practice(
            user["id"], "interview",
            final_score,
            role=user.get("role") or user.get("target_role") or "sde",
        )

        # â”€â”€ Emit canonical LearningEvent for the completed interview â”€â”€
        try:
            from app.services.study_engine import emit_learning_event
            await emit_learning_event(user["id"], {
                "activity_type": "interview_complete",
                "source": "interview",
                "skill_id": "interview.overall",
                "assessment_id": req.interview_id,
                "role": job_role,
                "company": company,
                "passed": final_score >= 7,
                "score": final_score,
                "time_spent_seconds": sum(q.get("time_taken", 0) for q in history),
                "mastery_before": None,
                "mastery_after": "proficient" if final_score >= 8 else (
                    "competent" if final_score >= 5 else "developing"
                ),
                "diagnosis_codes": weaknesses,
                "repair_id": None,
                "metadata": {
                    "breakdown": avg_breakdown,
                    "next_action": next_action.get("type") if next_action else None,
                    "weaknesses": weaknesses,
                },
            })
        except Exception as exc:
            logger.warning("interview_complete event emission failed: %s", exc)

        return {
            "feedback": feedback,
            "next_question": None,
            "current_score": final_score,
            "questions_answered": questions_answered,
            "total_questions": TOTAL_QUESTIONS,
            "finished": True,
            "reaction": reaction,
            "breakdown": breakdown,
            "score_breakdown": avg_breakdown,
            "weaknesses": weaknesses,
            "next_action": next_action,
            "xp_gained": gamification_result.get("xp_gained", 0),
            "level": gamification_result.get("level", 1),
            "new_badges": gamification_result.get("new_badges", []),
            "streak": gamification_result.get("new_streak", 0),
        }

    new_difficulty = await generate_dynamic_difficulty(
        interview.get("difficulty", "medium"), score_history[-5:], questions_answered,
    )

    if new_difficulty != interview.get("difficulty"):
        await interviews_collection.update_one(
            {"_id": ObjectId(req.interview_id)},
            {"$set": {"difficulty": new_difficulty}},
        )
        progression = updated_interview.get("difficulty_progression", [])
        progression.append(new_difficulty)
        await interviews_collection.update_one(
            {"_id": ObjectId(req.interview_id)},
            {"$set": {"difficulty_progression": progression}},
        )

    next_q = await generate_interview_question(
        job_role, history, company=company, difficulty=new_difficulty, user_id=user["id"],
        mode=mode,
    )

    await interviews_collection.update_one(
        {"_id": ObjectId(req.interview_id)},
        {"$set": {"score_history": score_history}},
    )

    return {
        "feedback": feedback,
        "next_question": next_q.get("question", ""),
        "next_question_type": next_q.get("question_type", ""),
        "next_tips": next_q.get("tips", ""),
        "next_difficulty": next_q.get("difficulty", new_difficulty),
        "current_score": round(sum(score_history) / len(score_history), 1),
        "questions_answered": questions_answered,
        "total_questions": TOTAL_QUESTIONS,
        "finished": False,
        "is_follow_up": False,
        "reaction": reaction,
        "breakdown": breakdown,
    }


@router.get("/{interview_id}/result")
async def get_result(interview_id: str, user=Depends(get_current_user)):
    try:
        interview = await interviews_collection.find_one({"_id": ObjectId(interview_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid interview ID")

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    questions = interview.get("questions", [])
    scores = [q["score"] for q in questions if q.get("score")]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    avg_breakdown = _average_breakdown([q.get("breakdown", {}) for q in questions])

    all_strengths = []
    all_improvements = []
    comm_scores = []
    for q in questions:
        fb = q.get("feedback", {}) or {}
        all_strengths.extend(fb.get("strengths", [])[:1])
        all_improvements.extend(fb.get("improvements", [])[:1])
        ca = fb.get("communication_analysis", {})
        if isinstance(ca, dict) and "score" in ca:
            comm_scores.append(ca["score"])

    readiness = min(100, max(0, int(avg_score * 10)))

    return {
        "interview_id": interview_id,
        "job_role": interview.get("job_role", ""),
        "company": interview.get("company", "general"),
        "overall_score": avg_score,
        "score_breakdown": avg_breakdown,
        "questions": questions,
        "total_questions": len([q for q in questions if not q.get("is_follow_up")]),
        "difficulty_progression": interview.get("difficulty_progression", []),
        "strength_areas": all_strengths[:5],
        "improvement_areas": all_improvements[:5],
        "communication_score": round(sum(comm_scores) / len(comm_scores), 1) if comm_scores else None,
        "readiness_score": readiness,
    }


@router.get("/history")
async def get_history(user=Depends(get_current_user)):
    cursor = interviews_collection.find(
        {"user_id": user["id"]},
        {"questions.answer": 0, "questions.feedback": 0},
    ).sort("created_at", -1).limit(20)

    interviews = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        questions = doc.get("questions", [])
        scores = [q["score"] for q in questions if q.get("score")]
        doc["overall_score"] = round(sum(scores) / len(scores), 1) if scores else 0
        doc["total_questions"] = len([q for q in questions if not q.get("is_follow_up")])
        interviews.append(doc)

    return {"interviews": interviews}


def _average_breakdown(breakdowns: list) -> dict:
    if not breakdowns:
        return {}
    keys = set()
    for b in breakdowns:
        if isinstance(b, dict):
            keys.update(b.keys())
    result = {}
    for k in keys:
        values = [b.get(k, 0) for b in breakdowns if isinstance(b, dict) and k in b]
        result[k] = round(sum(values) / len(values), 1) if values else 0
    return result


@router.get("/personalized-config")
async def get_personalized_config(user=Depends(get_current_user)):
    """Generate a personalized interview configuration based on student data.

    Consumes: role, company, resume, mastery, weaknesses, OA history, previous interviews.
    Returns: recommended focus areas, difficulty, question types, and company-specific tips.
    """
    user_id = user["id"]

    # Read student profile
    user_doc = await users_collection.find_one({"user_id": user_id}) or {}
    target_role = user_doc.get("target_role", "sde")
    target_company = user_doc.get("target_company", "")

    # Read mastery state
    from app.services.adaptive_learning import assess_user_skills
    assessment = await assess_user_skills(user_id)
    skills = assessment.get("skills", {})

    # Identify weak areas for focused interview questions
    weak_areas = [s for s, data in skills.items() if data.get("mastery") in ("novice", "introduced")]
    strong_areas = [s for s, data in skills.items() if data.get("mastery") in ("competent", "proficient", "master")]

    # Read previous interview history
    prev_interviews = []
    async for doc in interviews_collection.find({"user_id": user_id}).sort("created_at", -1).limit(5):
        prev_interviews.append({
            "company": doc.get("company", ""),
            "score": doc.get("overall_score", 0),
            "weaknesses": doc.get("weaknesses", []),
        })

    # Company-specific rubric
    from app.services.ai_interview import COMPANY_PROFILES
    company_profile = COMPANY_PROFILES.get(target_company, {})
    interview_style = company_profile.get("interview_style", "")
    focus_areas = company_profile.get("focus_areas", [])

    return {
        "target_role": target_role,
        "target_company": target_company,
        "weak_areas": weak_areas[:5],
        "strong_areas": strong_areas[:5],
        "recommended_focus": weak_areas[:3] if weak_areas else focus_areas[:3],
        "difficulty": "medium" if len(strong_areas) < 3 else "hard",
        "question_types": ["technical", "behavioral"] if target_company in ("google", "amazon") else ["technical"],
        "company_style": interview_style,
        "previous_interviews": prev_interviews,
        "total_previous": len(prev_interviews),
        "tips": _get_interview_tips(target_company, weak_areas),
    }


def _get_interview_tips(company: str, weak_areas: List[str]) -> List[str]:
    """Generate company-specific interview tips."""
    tips = []
    if company == "google":
        tips.append("Focus on algorithmic thinking and clean code.")
        tips.append("Practice explaining your thought process out loud.")
    elif company == "amazon":
        tips.append("Use the STAR method for behavioral questions.")
        tips.append("Reference Leadership Principles in your answers.")
    elif company == "tcs":
        tips.append("Focus on fundamentals and clear communication.")
        tips.append("Practice basic DSA and aptitude questions.")
    else:
        tips.append("Research the company's interview format.")
        tips.append("Practice coding out loud.")

    for area in weak_areas[:2]:
        tips.append(f"Review {area} before the interview.")

    return tips
