"""
Trial service — 7-day free trial with no card required.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from bson import ObjectId
from app.database import users_collection, trials_collection
from app.config import get_settings
from app.services.email import send_email, trial_started_email

settings = get_settings()
TRIAL_DAYS = 7


async def start_trial(user_id: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=TRIAL_DAYS)

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "plan": "trial",
            "trial_start": now,
            "trial_end": end,
        }},
    )

    trial_doc = {
        "user_id": user_id,
        "start_date": now,
        "end_date": end,
        "status": "active",
        "created_at": now,
    }
    await trials_collection.insert_one(trial_doc)

    user = await users_collection.find_one({"_id": ObjectId(user_id)}, {"email": 1, "name": 1})
    if user:
        try:
            import asyncio
            asyncio.create_task(
                send_email(user.get("email"), *trial_started_email(user.get("name", ""), TRIAL_DAYS))
            )
        except Exception:
            pass

    return {
        "status": "trial_started",
        "plan": "trial",
        "trial_end": end.isoformat(),
        "days": TRIAL_DAYS,
    }


async def check_trial_status(user_id: str) -> Dict[str, Any]:
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"active": False}

    plan = user.get("plan", "free")
    if plan != "trial":
        return {"active": False, "plan": plan}

    end = user.get("trial_end")
    if not end:
        return {"active": False, "plan": plan}

    now = datetime.now(timezone.utc)
    if end < now:
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"plan": "free"}},
        )
        # Win-back: trial just expired — the hottest moment to convert.
        try:
            if user.get("email"):
                asyncio.create_task(
                    send_email(user.get("email"), *trial_expired_email(user.get("name", "")))
                )
        except Exception:
            pass
        return {"active": False, "plan": "free", "expired": True}

    remaining = (end - now).total_seconds() / 86400
    return {
        "active": True,
        "plan": "trial",
        "trial_end": end.isoformat(),
        "days_remaining": round(remaining, 1),
    }


async def cancel_trial(user_id: str) -> Dict[str, Any]:
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"plan": "free"}, "$unset": {"trial_end": "", "trial_start": ""}},
    )
    return {"status": "trial_cancelled", "plan": "free"}


async def mark_trial_converted(user_id: str) -> None:
    """Mark any trial records for this user as converted (used at purchase)."""
    try:
        await trials_collection.update_many(
            {"user_id": user_id, "converted": {"$ne": True}},
            {"$set": {"converted": True, "converted_at": datetime.now(timezone.utc)}},
        )
    except Exception:
        pass
