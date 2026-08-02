from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import interviews_collection
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/interview", tags=["interview-replay"])


@router.get("/{interview_id}/replay")
async def get_interview_replay(interview_id: str, user=Depends(get_current_user)):
    """Get full replay trace for an interview solution.

    Returns time-stamped code snapshots showing the evolution from
    blank editor to final submission.
    """
    db = interviews_collection()
    interview = await db.find_one({"_id": interview_id})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Ensure user participated
    if str(user["id"]) not in [str(interview.get("user_id"))]:
        raise HTTPException(status_code=403, detail="Not authorized to view this replay")

    # Reconstruct code evolution from submission history
    submissions = interview.get("submissions", [])
    trace = [
        {
            "time": (sub.get("submitted_at") or datetime.now(timezone.utc)).isoformat(),
            "code": sub.get("code", ""),
            "cursor_line": 0,
            "cursor_col": 0,
            "event": "submit",
            "run_result": sub.get("result", {}),
        }
        for sub in sorted(submissions, key=lambda s: s.get("submitted_at", datetime.now(timezone.utc)))
    ]

    return {
        "interview_id": interview_id,
        "problem": interview.get("problem", {}),
        "final_code": interview.get("final_code", ""),
        "trace": trace,
    }


@router.get("/{interview_id}/replay/stats")
async def get_interview_replay_stats(interview_id: str, user=Depends(get_current_user)):
    """Get coding metrics for the interview solution."""
    db = interviews_collection()
    interview = await db.find_one({"_id": interview_id})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if str(user["id"]) != str(interview.get("user_id")):
        raise HTTPException(status_code=403, detail="Not authorized")

    submissions = interview.get("submissions", [])
    total_compiles = len(submissions)
    errors = sum(1 for s in submissions if s.get("result", {}).get("status") == "error")
    acceptance = interview.get("result", {}).get("accepted", False)

    # Estimate WPM from code length and total typing time (if available)
    code = interview.get("final_code", "")
    duration_seconds = interview.get("duration_seconds", 0) or 1
    words = len(code.split())
    wpm = round((words * 60) / duration_seconds, 1) if duration_seconds > 0 else 0

    return {
        "total_submissions": total_compiles,
        "compile_errors": errors,
        "accepted": acceptance,
        "estimated_wpm": wpm,
        "code_length": len(code),
        "duration_seconds": duration_seconds,
    }
