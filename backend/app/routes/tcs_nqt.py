"""
TCS NQT Prep routes.

Provides:
  GET  /api/v1/tcs-nqt/patterns
  GET  /api/v1/tcs-nqt/patterns/{pattern}/questions
  POST /api/v1/tcs-nqt/patterns/{pattern}/assess
  GET  /api/v1/tcs-nqt/progress
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.middleware.auth import get_current_user
from app.services.question_store import load_all, load_unverified, find, find_one, count_documents, distinct, _questions, _unverified_questions

router = APIRouter(prefix="/api/v1/tcs-nqt", tags=["tcs-nqt"])


def _get_tcs_questions():
    load_all()
    load_unverified()
    all_qs = list(_questions) + list(_unverified_questions)
    return [q for q in all_qs if q.get("domain") in (
        "Quantitative Aptitude", "Logical Reasoning", "Verbal", "Programming Logic"
    ) or q.get("type") in ("aptitude", "logical", "verbal", "cs_fundamentals")]


@router.get("/patterns")
def get_patterns(user=Depends(get_current_user)):
    questions = _get_tcs_questions()
    patterns = {}
    for q in questions:
        p = q.get("pattern") or "General Practice"
        if p not in patterns:
            patterns[p] = {"pattern": p, "count": 0, "domains": set(), "skills": set()}
        patterns[p]["count"] += 1
        if q.get("domain"):
            patterns[p]["domains"].add(q["domain"])
        if q.get("skill"):
            patterns[p]["skills"].add(q["skill"])
    
    result = []
    for p, info in patterns.items():
        result.append({
            "pattern": p,
            "count": info["count"],
            "domains": sorted(info["domains"]),
            "skills": sorted(info["skills"])[:5],
        })
    result.sort(key=lambda x: x["count"], reverse=True)
    return {"patterns": result[:100], "total_patterns": len(result)}


@router.get("/patterns/{pattern}/questions")
def get_pattern_questions(pattern: str, user=Depends(get_current_user), limit: int = 20, difficulty: Optional[str] = None):
    questions = _get_tcs_questions()
    filtered = [q for q in questions if q.get("pattern") == pattern]
    
    if difficulty:
        filtered = [q for q in filtered if q.get("difficulty") == difficulty]
    
    # Prefer verified, then automated_checked
    filtered.sort(key=lambda q: q.get("trust_status", "unverified") != "verified")
    
    result = []
    for q in filtered[:limit]:
        result.append({
            "id": q.get("id"),
            "pattern": q.get("pattern"),
            "skill": q.get("skill"),
            "domain": q.get("domain"),
            "difficulty": q.get("difficulty"),
            "trust_status": q.get("trust_status", "unverified"),
            "question": q.get("question") or q.get("content", {}).get("question", ""),
            "options": q.get("content", {}).get("options", q.get("options", [])),
            "correct_answer": q.get("content", {}).get("correct_answer", q.get("correct_answer", "")),
            "explanation": q.get("content", {}).get("explanation", q.get("explanation", "")),
            "hints": q.get("hints", []),
            "common_mistakes": q.get("common_mistakes", []),
            "time_estimate_sec": q.get("time_estimate_sec", 90),
            "company_relevance": q.get("company_relevance", {}),
        })
    return {
        "pattern": pattern,
        "questions": result,
        "total": len(filtered),
        "returned": len(result),
    }


class AssessRequest(BaseModel):
    answers: Dict[str, str] = Field(default_factory=dict)
    time_spent_seconds: int = Field(default=0, ge=0)


@router.post("/patterns/{pattern}/assess")
def assess_pattern(pattern: str, req: AssessRequest, user=Depends(get_current_user)):
    questions = _get_tcs_questions()
    pattern_questions = [q for q in questions if q.get("pattern") == pattern]
    
    if not pattern_questions:
        raise HTTPException(status_code=404, detail=f"Pattern not found: {pattern}")
    
    results = []
    correct = 0
    total = 0
    
    for q in pattern_questions[:10]:
        qid = str(q.get("id", ""))
        if qid not in req.answers:
            continue
        
        total += 1
        user_answer = str(req.answers[qid]).strip()
        correct_answer = str(
            q.get("content", {}).get("correct_answer", q.get("correct_answer", ""))
        ).strip().lower()
        
        # For MCQ, compare with options
        options = q.get("content", {}).get("options", q.get("options", []))
        correct_index = q.get("correct_index")
        
        is_correct = False
        if correct_index is not None and isinstance(correct_index, int):
            try:
                is_correct = int(user_answer) == correct_index
            except (ValueError, TypeError):
                is_correct = False
        elif correct_answer:
            is_correct = user_answer.lower() == correct_answer
        
        if is_correct:
            correct += 1
        
        results.append({
            "id": qid,
            "correct": is_correct,
            "your_answer": user_answer,
            "correct_answer": correct_answer if correct_answer else str(correct_index),
            "explanation": q.get("content", {}).get("explanation", q.get("explanation", "")),
            "common_mistakes": q.get("common_mistakes", []),
        })
    
    score = round(correct / total * 100, 1) if total > 0 else 0
    mastery_threshold = 80
    
    return {
        "pattern": pattern,
        "score": score,
        "correct": correct,
        "total": total,
        "passed": score >= mastery_threshold,
        "mastery_threshold": mastery_threshold,
        "results": results,
        "message": f"You scored {score}% ({correct}/{total}). {'Mastered!' if score >= mastery_threshold else 'Keep practicing!'}",
    }


@router.get("/progress")
def get_progress(user=Depends(get_current_user)):
    questions = _get_tcs_questions()
    patterns = {}
    for q in questions:
        p = q.get("pattern") or "General Practice"
        if p not in patterns:
            patterns[p] = {"total": 0, "verified": 0, "domains": set()}
        patterns[p]["total"] += 1
        if q.get("trust_status") == "verified":
            patterns[p]["verified"] += 1
        if q.get("domain"):
            patterns[p]["domains"].add(q["domain"])
    
    progress = []
    for p, info in patterns.items():
        progress.append({
            "pattern": p,
            "total_questions": info["total"],
            "verified_questions": info["verified"],
            "domains": sorted(info["domains"]),
        })
    progress.sort(key=lambda x: x["pattern"])
    
    return {
        "progress": progress,
        "total_patterns": len(progress),
        "total_questions": sum(p["total_questions"] for p in progress),
        "total_verified": sum(p["verified_questions"] for p in progress),
    }


class VerifyRequest(BaseModel):
    trust_status: str = Field(..., description="verified | reviewed | needs_review | quarantined")
    reviewer: Optional[str] = Field(None, description="Reviewer name/email")
    notes: Optional[str] = Field(None, description="Review notes")


@router.post("/questions/{question_id}/verify")
def verify_question(question_id: str, req: VerifyRequest, user=Depends(get_current_user)):
    allowed = {"verified", "reviewed", "needs_review", "quarantined"}
    if req.trust_status not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid trust_status. Allowed: {sorted(allowed)}")

    q = find_one({"id": question_id}, allow_unverified=True)
    if not q:
        q = next((x for x in _unverified_questions if str(x.get("id")) == str(question_id)), None)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    q["trust_status"] = req.trust_status
    if req.trust_status == "verified":
        q["verified_by"] = req.reviewer or user.get("email")
        q["verified_at"] = datetime.now(timezone.utc).isoformat()
    if req.notes:
        q["review_notes"] = req.notes

    return {
        "id": question_id,
        "trust_status": req.trust_status,
        "verified_by": q.get("verified_by"),
        "verified_at": q.get("verified_at"),
        "review_notes": q.get("review_notes"),
        "message": f"Question marked as {req.trust_status}",
    }


@router.get("/questions/unverified")
def get_unverified_questions(user=Depends(get_current_user), limit: int = 50, offset: int = 0):
    questions = _get_tcs_questions()
    unverified = [q for q in questions if q.get("trust_status") in ("unverified", "needs_review")]
    unverified.sort(key=lambda q: q.get("id", ""))

    result = []
    for q in unverified[offset:offset + limit]:
        result.append({
            "id": q.get("id"),
            "pattern": q.get("pattern"),
            "skill": q.get("skill"),
            "domain": q.get("domain"),
            "difficulty": q.get("difficulty"),
            "trust_status": q.get("trust_status"),
            "question": q.get("question") or q.get("content", {}).get("question", ""),
            "options": q.get("content", {}).get("options", q.get("options", [])),
            "correct_answer": q.get("content", {}).get("correct_answer", q.get("correct_answer", "")),
            "explanation": q.get("content", {}).get("explanation", q.get("explanation", "")),
            "common_mistakes": q.get("common_mistakes", []),
        })

    return {
        "questions": result,
        "total": len(unverified),
        "returned": len(result),
        "offset": offset,
        "limit": limit,
    }
