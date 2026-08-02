from datetime import datetime, timezone
import random
from fastapi import APIRouter, Depends, HTTPException
from app.models.interview import StartInterview, SubmitAnswer
from app.database import users_collection, interviews_collection
from app.middleware.auth import get_current_user
from app.services.ai import (
    generate_interview_question,
    evaluate_answer,
    COMPANY_PROFILES,
)
from app.services.interview_enhanced import (
    generate_follow_up_question,
    analyze_communication_style,
    generate_dynamic_difficulty,
)
from app.services.behavioral_enhanced import evaluate_star_answer
from app.services.gamification import record_practice
from app.config import get_settings
from bson import ObjectId

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
        "created_at": datetime.now(timezone.utc),
    }
    result = await interviews_collection.insert_one(interview_doc)
    interview_id = str(result.inserted_id)

    question_data = await generate_interview_question(
        req.job_role, [], company=company, difficulty=req.difficulty,
    )

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

    feedback = await evaluate_answer(
        req.question, req.answer, job_role,
        company=company, question_type="behavioral" if req.is_follow_up else "mixed",
    )

    score = feedback.get("score", 5)
    breakdown = feedback.get("breakdown", {})
    reaction = feedback.get("reaction", "")

    if not breakdown:
        breakdown = {"technical": score, "communication": score, "problem_solving": score, "depth": score}

    qa_pair = {
        "question": req.question,
        "answer": req.answer,
        "question_type": "follow_up" if req.is_follow_up else "primary",
        "difficulty": interview.get("difficulty", "medium"),
        "score": score,
        "breakdown": breakdown,
        "feedback": feedback,
        "is_follow_up": req.is_follow_up,
        "company": company,
        "time_taken": req.time_taken,
    }
    await interviews_collection.update_one(
        {"_id": ObjectId(req.interview_id)},
        {"$push": {"questions": qa_pair}},
    )

    updated_interview = await interviews_collection.find_one({"_id": ObjectId(req.interview_id)})
    history = updated_interview.get("questions", [])
    all_primary = [q for q in history if not q.get("is_follow_up")]
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
        await interviews_collection.update_one(
            {"_id": ObjectId(req.interview_id)},
            {"$set": {"status": "completed", "score_history": score_history}},
        )

        avg_breakdown = _average_breakdown([q.get("breakdown", {}) for q in history])
        strength_areas = feedback.get("strengths", [])
        improvement_areas = feedback.get("improvements", [])

        gamification_result = await record_practice(
            user["id"], "interview",
            round(sum(score_history) / len(score_history), 1),
        )

        return {
            "feedback": feedback,
            "next_question": None,
            "current_score": round(sum(score_history) / len(score_history), 1),
            "questions_answered": questions_answered,
            "total_questions": TOTAL_QUESTIONS,
            "finished": True,
            "reaction": reaction,
            "breakdown": breakdown,
            "score_breakdown": avg_breakdown,
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
        job_role, history, company=company, difficulty=new_difficulty,
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
    for q in questions:
        fb = q.get("feedback", {})
        all_strengths.extend(fb.get("strengths", [])[:1])
        all_improvements.extend(fb.get("improvements", [])[:1])

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
