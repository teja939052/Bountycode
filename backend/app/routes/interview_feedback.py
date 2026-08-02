from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from app.middleware.auth import get_current_user
from app.database import get_db, interviews_collection, gamification_collection
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/interview", tags=["interview-feedback"])


@router.post("/feedback")
async def submit_interview_feedback(
    interview_id: str = Body(..., embed=True),
    scores: dict = Body(..., embed=True),
    comment: str = Body("", embed=True),
    user=Depends(get_current_user),
):
    """Submit peer feedback for a completed mock interview.

    Expected scores format:
    scores = {
      "clarity": 1-5,
      "depth": 1-5,
      "confidence": 1-5,
      "relevance": 1-5,
      "problem_solving": 1-5
    }
    """
    db = get_db()
    interview = await interviews_collection().find_one({"_id": interview_id})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Ensure user is a participant
    if user["id"] not in [str(interview.get("user_id")), str(interview.get("interviewer_id"))]:
        raise HTTPException(status_code=403, detail="You are not part of this interview")

    categories = ["clarity", "depth", "confidence", "relevance", "problem_solving"]
    scored = {k: int(v) for k, v in scores.items() if k in categories and 1 <= int(v) <= 5}

    feedback_entry = {
        "reviewer_id": user["id"],
        "reviewer_name": user.get("name", "Anonymous"),
        "scores": scored,
        "comment": comment,
        "submitted_at": datetime.now(timezone.utc),
    }

    await interviews_collection().update_one(
        {"_id": interview_id},
        {"$push": {"peer_feedback": feedback_entry}},
    )

    # Award XP for giving feedback
    await record_practice(user["id"], "mock_interview_feedback", 25, {"interview_id": interview_id})

    return {"success": True, "feedback_id": str(datetime.now(timezone.utc).timestamp())}


@router.get("/feedback/{interview_id}")
async def get_interview_feedback(interview_id: str, user=Depends(get_current_user)):
    """Get aggregated peer feedback for both interview participants."""
    db = get_db()
    interview = await interviews_collection().find_one({"_id": interview_id})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    feedbacks = interview.get("peer_feedback", [])
    if not feedbacks:
        return {"interview_id": interview_id, "average_scores": {}, "count": 0}

    categories = ["clarity", "depth", "confidence", "relevance", "problem_solving"]
    sums = {cat: 0 for cat in categories}
    count = 0
    for fb in feedbacks:
        for cat in categories:
            sums[cat] += fb.get("scores", {}).get(cat, 0)
        count += 1

    averages = {cat: round(sums[cat] / max(1, count), 1) for cat in categories}
    overall = round(sum(averages.values()) / len(categories), 1)

    return {
        "interview_id": interview_id,
        "average_scores": averages,
        "overall_score": overall,
        "feedback_count": count,
        "comments": [fb.get("comment") for fb in feedbacks if fb.get("comment")],
    }


@router.get("/stats/{user_id}")
async def get_interview_stats(user_id: str, current=Depends(get_current_user)):
    """Get a user's mock interview stats.

    Users can view their own stats. Admins can view anyone's.
    """
    if str(user_id) != current["id"] and current.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    db = get_db()
    cursor = interviews_collection().find({"user_id": user_id})
    interviews = [doc async for doc in cursor]

    total = len(interviews)
    wins = sum(1 for i in interviews if i.get("winner_id") == user_id)
    all_scores = []
    for interview in interviews:
        for fb in interview.get("peer_feedback", []):
            scores = fb.get("scores", {})
            if scores:
                all_scores.append(sum(scores.values()) / len(scores))

    avg_score = round(sum(all_scores) / max(1, len(all_scores)), 1) if all_scores else 0
    badge_progress = min(100, (total // 5) * 20)  # 5 interviews per 20% badge progress

    return {
        "total_interviews": total,
        "wins": wins,
        "win_rate": round(wins / max(1, total) * 100, 1),
        "average_score": avg_score,
        "badge_progress": badge_progress,
        "mock_interview_champion": total >= 10 and avg_score >= 4.0,
    }
