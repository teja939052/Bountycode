"""Prep Report Card — deterministic summary of a user's placement prep,
aggregated from real data across the app's collections. Exportable as DOCX
or PDF by reusing the resume export pipeline (no AI involved).
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.middleware.auth import get_current_user
from app.database import (
    users_collection,
    interviews_collection,
    aptitude_tests_collection,
    coding_challenges_collection,
    solved_problems_collection,
    resumes_collection,
    gamification_collection,
    battles_collection,
    peer_reviews_collection,
    gd_ratings_collection,
    drive_trackers_collection,
)
from app.services.export import export_to_docx, export_to_pdf

router = APIRouter(prefix="/api/v1/report-card", tags=["Report Card"])


def _pct(value) -> float:
    try:
        return round(max(0.0, min(100.0, float(value))), 1)
    except (TypeError, ValueError):
        return 0.0


def _avg(values):
    nums = [v for v in values if isinstance(v, (int, float)) and v is not None]
    return round(sum(nums) / len(nums), 1) if nums else 0.0


async def _collect_sections(user_id: str) -> dict:
    uid = user_id

    # Interviews (score_history is a list of 1-10 per-answer scores)
    interview_docs = []
    cursor = interviews_collection().find({"user_id": uid, "status": "completed"}).sort("created_at", -1).limit(100)
    async for d in cursor:
        interview_docs.append(d)
    interview_scores = []
    for d in interview_docs:
        history = d.get("score_history") or []
        nums = [s for s in history if isinstance(s, (int, float)) and s is not None]
        if nums:
            interview_scores.append(sum(nums) / len(nums))
    interviews = {
        "count": len(interview_docs),
        "score": _pct(_avg(interview_scores) * 10),  # 10-point → percent
    }

    # Aptitude tests (score is already 0-100)
    aptitude_docs = []
    cursor = aptitude_tests_collection().find({"user_id": uid, "status": "completed"}).sort("created_at", -1).limit(100)
    async for d in cursor:
        aptitude_docs.append(d)
    aptitude = {
        "count": len(aptitude_docs),
        "score": _pct(_avg([d.get("score") for d in aptitude_docs])),
    }

    # Coding challenges (score 0-100)
    coding_docs = []
    cursor = coding_challenges_collection().find({"user_id": uid}).sort("created_at", -1).limit(100)
    async for d in cursor:
        if d.get("status") in ("completed", "submitted", "passed", "solved"):
            coding_docs.append(d)
    coding = {
        "count": len(coding_docs),
        "score": _pct(_avg([d.get("score") for d in coding_docs])),
    }

    # Question bank solves
    solved = await solved_problems_collection().count_documents({"user_id": uid})

    # Resume reviews
    resumes = await resumes_collection().count_documents({"user_id": uid})

    # Gamification profile
    gprofile = await gamification_collection().find_one({"user_id": uid})
    gamification = {
        "level": (gprofile or {}).get("level", 1),
        "xp": (gprofile or {}).get("xp", 0),
        "streak": (gprofile or {}).get("streak", 0),
    }

    # Battles
    wins = losses = 0
    cursor = battles_collection().find({
        "status": "completed",
        "$or": [{"player1_id": uid}, {"player2_id": uid}],
    }).limit(200)
    async for b in cursor:
        if b.get("winner_id") == uid:
            wins += 1
        else:
            losses += 1
    battles = {"wins": wins, "losses": losses, "total": wins + losses}

    # Peer reviews (reviews I gave + received)
    reviews_given = await peer_reviews_collection().count_documents({"kind": "review", "reviewer_id": uid})
    reviews_received = await peer_reviews_collection().count_documents(
        {"kind": "review", "item_id": {"$in": [
            str(d["_id"]) async for d in peer_reviews_collection().find({"user_id": uid, "kind": {"$ne": "review"}})
        ]}}
    )

    # GD ratings received
    gd_ratings = 0
    try:
        gd_ratings = await gd_ratings_collection().count_documents({"target_user_id": uid})
    except Exception:
        gd_ratings = 0

    # Drive tracker
    drives = await drive_trackers_collection().count_documents({"user_id": uid})
    offers = await drive_trackers_collection().count_documents(
        {"user_id": uid, "stage": {"$in": ["offer", "joined"]}},
    )

    return {
        "interviews": interviews,
        "aptitude": aptitude,
        "coding": coding,
        "solved_problems": solved,
        "resumes": resumes,
        "gamification": gamification,
        "battles": battles,
        "reviews_given": reviews_given,
        "reviews_received": reviews_received,
        "gd_ratings": gd_ratings,
        "drives": drives,
        "offers": offers,
    }


def _grade_label(score: float) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Strong"
    if score >= 60:
        return "Good"
    if score >= 45:
        return "Developing"
    if score >= 30:
        return "Needs Work"
    return "Just Started"


def _build_report(sections: dict, user) -> dict:
    available = []
    parts = {}

    for key, label, weight in [
        ("interviews", "AI Interviews", 25),
        ("aptitude", "Aptitude Tests", 15),
        ("coding", "Coding Challenges", 25),
        ("solved_problems", "Question Bank", 10),
        ("resumes", "Resume Reviews", 10),
        ("drives", "Drive Progress", 15),
    ]:
        if key in ("solved_problems", "resumes", "drives"):
            count = sections[key] if isinstance(sections[key], int) else sections[key].get("count", 0)
            if key == "drives":
                offers = sections["offers"]
                score = _pct(offers * 100 / count) if count else 0.0
            else:
                score = _pct(min(count * 10, 100))
            parts[label] = {"count": count, "score": score}
        else:
            count = sections[key].get("count", 0)
            score = sections[key].get("score", 0.0)
            parts[label] = {"count": count, "score": score}
        if count > 0:
            available.append((score, weight))

    overall = round(sum(s * w for s, w in available) / sum(w for _, w in available), 1) if available else 0.0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user": {
            "name": user.get("name", "User"),
            "email": user.get("email", ""),
            "plan": user.get("plan", "free"),
        },
        "sections": parts,
        "activity": {
            "solved_problems": sections["solved_problems"],
            "resumes": sections["resumes"],
            "reviews_given": sections["reviews_given"],
            "reviews_received": sections["reviews_received"],
            "gd_ratings": sections["gd_ratings"],
            "level": sections["gamification"]["level"],
            "xp": sections["gamification"]["xp"],
            "streak": sections["gamification"]["streak"],
            "battles": sections["battles"],
            "drives": sections["drives"],
            "offers": sections["offers"],
        },
        "overall_score": overall,
        "grade": _grade_label(overall),
    }


def _render_text(report: dict) -> str:
    lines = []
    lines.append("PLACEMENTPRO — PREP REPORT CARD")
    lines.append("=" * 42)
    lines.append("")
    lines.append(f"Name:       {report['user']['name']}")
    lines.append(f"Email:      {report['user']['email']}")
    lines.append(f"Plan:       {report['user']['plan']}")
    lines.append(f"Generated:  {report['generated_at']}")
    lines.append("")
    lines.append("SECTIONS")
    lines.append("-" * 42)
    for label, part in report["sections"].items():
        lines.append(f"{label:<22} {part['score']:>6.1f}/100   ({part['count']} attempts)")
    lines.append("")
    lines.append("ACTIVITY")
    lines.append("-" * 42)
    a = report["activity"]
    lines.append(f"Problems solved:     {a['solved_problems']}")
    lines.append(f"Resumes reviewed:    {a['resumes']}")
    lines.append(f"Peer reviews given:  {a['reviews_given']}")
    lines.append(f"Peer reviews got:    {a['reviews_received']}")
    lines.append(f"GD ratings received: {a['gd_ratings']}")
    lines.append(f"Level:               {a['level']}  (XP {a['xp']})")
    lines.append(f"Streak:              {a['streak']} days")
    lines.append(f"Battles:             {a['battles']['wins']}W / {a['battles']['losses']}L")
    lines.append(f"Drives tracked:      {a['drives']}  (offers: {a['offers']})")
    lines.append("")
    lines.append("OVERALL READINESS")
    lines.append("-" * 42)
    lines.append(f"Score: {report['overall_score']}/100")
    lines.append(f"Grade: {report['grade']}")
    return "\n".join(lines)


@router.get("")
async def get_report_card(user=Depends(get_current_user)):
    sections = await _collect_sections(user["id"])
    return _build_report(sections, user)


@router.get("/export/{fmt}")
async def export_report_card(fmt: str, user=Depends(get_current_user)):
    sections = await _collect_sections(user["id"])
    report = _build_report(sections, user)
    text = _render_text(report)

    if fmt == "docx":
        data = export_to_docx(text)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = "placementpro-report-card.docx"
    elif fmt == "pdf":
        data = export_to_pdf(text)
        media_type = "application/pdf"
        filename = "placementpro-report-card.pdf"
    else:
        data = text.encode("utf-8")
        media_type = "text/plain; charset=utf-8"
        filename = "placementpro-report-card.txt"

    return StreamingResponse(
        iter([data]),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
