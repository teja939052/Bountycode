"""
Daily Orders — deadline-driven daily checklist ("First Mate Orders").

The user sets a placement drive deadline; the backend derives a small,
deterministic daily checklist that rotates by date (no AI cost), and tracks
completion per day with streak-friendly XP.
"""
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import user_deadlines_collection
from app.middleware.auth import get_current_user
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/orders", tags=["daily-orders"])

APTITUDE_ROTATION = ["quantitative", "logical", "verbal"]
APTITUDE_LABELS = {
    "quantitative": "Quantitative drill",
    "logical": "Logical reasoning drill",
    "verbal": "Verbal ability drill",
}


class DeadlineInput(BaseModel):
    company: str
    drive_date: str  # ISO date, e.g. 2026-09-15


def _date_key(now: datetime) -> str:
    return now.date().isoformat()


def _parse_drive_date(raw: str) -> datetime:
    try:
        return datetime.strptime(raw.strip(), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        raise HTTPException(status_code=400, detail="drive_date must be YYYY-MM-DD")


def _build_orders(user_id: str, now: datetime, days_left: Optional[int]) -> List[dict]:
    """Deterministic per-date checklist. Same day = same orders."""
    doy = now.timetuple().tm_yday
    apt_cat = APTITUDE_ROTATION[doy % len(APTITUDE_ROTATION)]
    deck = "service" if now.weekday() in (0, 2, 4) else "product"

    urgent = days_left is not None and 0 <= days_left <= 14
    imminent = days_left is not None and 0 <= days_left <= 3

    orders = [
        {
            "id": f"dsa-{_date_key(now)}",
            "type": "dsa",
            "title": "Chart one problem from the bounty board",
            "detail": (
                "One solved problem keeps the hull tight. Pick anything you "
                "haven't tried yet."
            ),
            "link": "/question-bank",
            "points": 20,
        },
        {
            "id": f"apt-{apt_cat}-{_date_key(now)}",
            "type": "aptitude",
            "title": APTITUDE_LABELS[apt_cat],
            "detail": "Run a quick set — speed on the basics wins the screening rounds.",
            "link": "/aptitude",
            "points": 15,
        },
        {
            "id": f"interview-{deck}-{_date_key(now)}",
            "type": "interview",
            "title": (
                "Report to the Service Deck" if deck == "service"
                else "Report to the Product Deck"
            ),
            "detail": (
                "Rapid-fire screen practice." if deck == "service"
                else "Deep-dive round practice."
            ),
            "link": "/interview-terminal",
            "points": 25,
        },
    ]

    if urgent:
        orders.append({
            "id": f"exam-{_date_key(now)}",
            "type": "exam",
            "title": "Full dress rehearsal",
            "detail": (
                f"{days_left} day(s) to the drive. Run one full Mass Recruiter paper "
                "under exam conditions."
            ),
            "link": "/mass-recruiter",
            "points": 30,
        })
    elif days_left is None or days_left > 14:
        orders.append({
            "id": f"assess-{_date_key(now)}",
            "type": "assessment",
            "title": "Check the horizon",
            "detail": "Re-run the Grand Line Assessment and adjust course.",
            "link": "/grand-line",
            "points": 10,
        })

    if imminent:
        orders.append({
            "id": f"logistics-{_date_key(now)}",
            "type": "logistics",
            "title": "Ready the gear",
            "detail": (
                "Interviews within 72 hours: refresh your resume bullet points, "
                "prepare your intro, charge everything. Boring wins drives."
            ),
            "link": "/resume-builder",
            "points": 10,
        })

    return orders


@router.put("/deadline")
async def set_deadline(req: DeadlineInput, user=Depends(get_current_user)):
    """Set or update the placement-drive countdown."""
    drive = _parse_drive_date(req.drive_date)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    await user_deadlines_collection().update_one(
        {"user_id": user["id"]},
        {"$set": {
            "company": req.company.strip()[:80] or "Target Company",
            "drive_date": drive,
            "updated_at": datetime.now(timezone.utc),
        }},
        upsert=True,
    )

    days_left = (drive - today).days
    return {
        "company": req.company,
        "drive_date": drive.date().isoformat(),
        "days_left": days_left,
        "message": (
            f"{days_left} days on the clock." if days_left >= 0
            else "That date has passed — set a new target when ready."
        ),
    }


@router.delete("/deadline")
async def clear_deadline(user=Depends(get_current_user)):
    await user_deadlines_collection().update_one(
        {"user_id": user["id"]},
        {"$unset": {"company": "", "drive_date": ""},
         "$set": {"updated_at": datetime.now(timezone.utc)}},
    )
    return {"cleared": True}


@router.get("/today")
async def get_today_orders(user=Depends(get_current_user)):
    """Today's checklist + deadline status. Deterministic per date."""
    uid = user["id"]
    now = datetime.now(timezone.utc)

    deadline_doc = await user_deadlines_collection().find_one({"user_id": uid})
    days_left: Optional[int] = None
    company: Optional[str] = None
    drive_iso: Optional[str] = None

    if deadline_doc and deadline_doc.get("drive_date"):
        drive = deadline_doc["drive_date"]
        if isinstance(drive, str):
            drive = _parse_drive_date(drive)
        today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        days_left = (drive - today_midnight).days
        company = deadline_doc.get("company")
        drive_iso = drive.date().isoformat()

    orders = _build_orders(uid, now, days_left)

    completed_today: List[str] = []
    if deadline_doc:
        completed_today = (deadline_doc.get("completed_orders") or {}).get(
            _date_key(now), []
        )

    for o in orders:
        o["completed"] = o["id"] in completed_today

    done_count = sum(1 for o in orders if o["completed"])
    total_points = sum(o["points"] for o in orders)
    earned_points = sum(o["points"] for o in orders if o["completed"])

    return {
        "date": _date_key(now),
        "deadline": {
            "company": company,
            "drive_date": drive_iso,
            "days_left": days_left,
        },
        "orders": orders,
        "progress": {
            "done": done_count,
            "total": len(orders),
            "earned_points": earned_points,
            "total_points": total_points,
            "all_done": done_count == len(orders) and len(orders) > 0,
        },
    }


@router.post("/{order_id}/complete")
async def complete_order(order_id: str, user=Depends(get_current_user)):
    """Mark an order complete; awards XP once per order per day."""
    uid = user["id"]
    now = datetime.now(timezone.utc)
    key = _date_key(now)

    valid_ids = {o["id"] for o in _build_orders(uid, now, None)}
    # exam/logistics ids depend on days_left; recompute against stored deadline
    deadline_doc = await user_deadlines_collection().find_one({"user_id": uid})
    days_left: Optional[int] = None
    if deadline_doc and deadline_doc.get("drive_date"):
        drive = deadline_doc["drive_date"]
        if isinstance(drive, str):
            drive = _parse_drive_date(drive)
        days_left = (
            drive - now.replace(hour=0, minute=0, second=0, microsecond=0)
        ).days
    valid_ids |= {o["id"] for o in _build_orders(uid, now, days_left)}

    if order_id not in valid_ids:
        raise HTTPException(status_code=404, detail="Unknown order for today")

    doc = await user_deadlines_collection().find_one({"user_id": uid})
    already = doc and order_id in (doc.get("completed_orders") or {}).get(key, [])

    await user_deadlines_collection().update_one(
        {"user_id": uid},
        {
            "$addToSet": {f"completed_orders.{key}": order_id},
            "$set": {"last_order_at": now},
        },
        upsert=True,
    )

    xp_gained = 0
    if not already:
        try:
            result = await record_practice(uid, "daily_order", 70)
            xp_gained = result.get("xp_gained", 0) if isinstance(result, dict) else 0
        except Exception:
            pass

    return {"order_id": order_id, "already_done": bool(already), "xp_gained": xp_gained}
