import hashlib
import random
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/events", tags=["events"])

RANDOM_EVENTS = [
    {"id": "lightning_round", "name": "Lightning Round", "emoji": "⚡", "effect": "Double XP for 5 minutes"},
    {"id": "brain_boost", "name": "Brain Boost", "emoji": "🧠", "effect": "+50% XP for 30 minutes"},
    {"id": "blazing_streak", "name": "Blazing Streak", "emoji": "🔥", "effect": "Streak freeze +1 for today"},
]

RESEARCH_EVENT_ID = "research-1"
RESEARCH_EVENT_DEFAULTS = {
    "id": RESEARCH_EVENT_ID,
    "title": "Solve 1,000,000 Graph Problems",
    "contribution": 0,
    "goal": 1000000,
    "target": 1000000,
    "reward_name": "Legend Card",
    "emoji": "🌐",
}

FESTIVALS = [
    {"id": "diwali_fiesta", "name": "Diwali Fiesta", "emoji": "🪔", "date_range": "October 28 – November 3", "bonus_multiplier": 2.0, "month": 10},
    {"id": "code_carnival", "name": "Code Carnival", "emoji": "🎪", "date_range": "December 20 – January 2", "bonus_multiplier": 1.5, "month": 12},
    {"id": "placement_summer_fest", "name": "Placement Summer Fest", "emoji": "☀️", "date_range": "June 1 – June 15", "bonus_multiplier": 1.75, "month": 6},
]

RESEARCH_DURATION_DAYS = 30
LUCKY_CHANCE = 0.02
LUCKY_XP = 500
MAX_LUCKY_ATTEMPTS = 10


class ContributeRequest(BaseModel):
    amount: int


class LuckyRequest(BaseModel):
    attempts: int = 1


def _hour_key(now: datetime) -> str:
    return now.strftime("%Y-%m-%d-%H")


def _pick_random_event(user_id: str, now: datetime) -> dict:
    seed = int.from_bytes(
        hashlib.sha256(f"{user_id}:{_hour_key(now)}".encode("utf-8")).digest()[:4], "big"
    )
    return RANDOM_EVENTS[seed % len(RANDOM_EVENTS)]


async def _get_or_create_research(db, now: datetime) -> dict:
    event = await db["research_events"].find_one({"id": RESEARCH_EVENT_ID})
    if not event:
        await db["research_events"].update_one(
            {"id": RESEARCH_EVENT_ID},
            {
                "$setOnInsert": {
                    **RESEARCH_EVENT_DEFAULTS,
                    "started_at": now,
                    "ends_at": now + timedelta(days=RESEARCH_DURATION_DAYS),
                }
            },
            upsert=True,
        )
        event = await db["research_events"].find_one({"id": RESEARCH_EVENT_ID})
    return event


def _serialize_research(event: dict, now: datetime) -> dict:
    contribution = event.get("contribution", 0)
    goal = event.get("goal", event.get("target", 1))
    progress = round(contribution / goal * 100, 2) if goal > 0 else 0.0
    ends_at = event.get("ends_at")
    if isinstance(ends_at, str):
        ends_at = datetime.fromisoformat(ends_at)
    return {
        "id": event.get("id"),
        "title": event.get("title"),
        "contribution": contribution,
        "goal": goal,
        "progress_percent": progress,
        "reward_name": event.get("reward_name"),
        "emoji": event.get("emoji"),
        "started_at": event.get("started_at").isoformat() if isinstance(event.get("started_at"), datetime) else event.get("started_at"),
        "ends_at": ends_at.isoformat() if isinstance(ends_at, datetime) else event.get("ends_at"),
        "active": not ends_at or ends_at > now,
    }


@router.get("/random")
async def get_random_event(user=Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    event = _pick_random_event(user["id"], now)
    return {
        "id": event["id"],
        "name": event["name"],
        "emoji": event["emoji"],
        "effect": event["effect"],
        "expires_at": (now + timedelta(hours=1)).isoformat(),
        "active": True,
    }


@router.get("/research")
async def get_research():
    db = get_db()
    now = datetime.now(timezone.utc)
    event = await _get_or_create_research(db, now)
    return _serialize_research(event, now)


@router.post("/research/contribute")
async def contribute_research(req: ContributeRequest, user=Depends(get_current_user)):
    db = get_db()
    now = datetime.now(timezone.utc)
    if req.amount < 1 or req.amount > 1000000:
        raise HTTPException(status_code=400, detail="Amount must be between 1 and 1,000,000")

    event = await _get_or_create_research(db, now)
    await db["research_events"].update_one(
        {"id": RESEARCH_EVENT_ID},
        {"$inc": {"contribution": req.amount}, "$set": {"updated_at": now}},
    )
    updated = await db["research_events"].find_one({"id": RESEARCH_EVENT_ID})
    return {
        "id": RESEARCH_EVENT_ID,
        "contributed": req.amount,
        **_serialize_research(updated, now),
    }


@router.get("/festival")
async def get_festival():
    now = datetime.now(timezone.utc)
    ordered = sorted(FESTIVALS, key=lambda f: f["month"])
    festival = next((f for f in ordered if f["month"] >= now.month), ordered[0])
    return {
        "id": festival["id"],
        "name": festival["name"],
        "emoji": festival["emoji"],
        "date_range": festival["date_range"],
        "bonus_multiplier": festival["bonus_multiplier"],
    }


@router.post("/lucky")
async def lucky_compile(req: LuckyRequest, user=Depends(get_current_user)):
    attempts = max(1, min(req.attempts, MAX_LUCKY_ATTEMPTS))
    lucky = any(random.random() < LUCKY_CHANCE for _ in range(attempts))
    if not lucky:
        return {"lucky": False, "xp": 0, "message": "No Golden Compiler this time. Keep compiling!"}

    try:
        await record_practice(user["id"], "lucky_compile", LUCKY_XP)
    except Exception:
        pass
    return {
        "lucky": True,
        "xp": LUCKY_XP,
        "message": "🎉 Lucky Compile! You found the Golden Compiler +500 XP",
    }
