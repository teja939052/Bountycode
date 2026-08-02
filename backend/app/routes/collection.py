from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/collection", tags=["collection"])

COMPANY_CARDS = [
    {"id": "google", "company": "Google", "rarity": "epic", "emoji": "🔍", "description": "Search giant — crack their reverse engineering interviews"},
    {"id": "amazon", "company": "Amazon", "rarity": "legendary", "emoji": "📦", "description": "LP-driven loops and ruthless leadership principles"},
    {"id": "meta", "company": "Meta", "rarity": "legendary", "emoji": "🔵", "description": "Product sense + algorithms under time pressure"},
    {"id": "netflix", "company": "Netflix", "rarity": "rare", "emoji": "🎬", "description": "Culture of freedom and responsibility — no rules, just judgment"},
    {"id": "apple", "company": "Apple", "rarity": "epic", "emoji": "🍎", "description": "Cross-functional collaboration and design obsession"},
    {"id": "microsoft", "company": "Microsoft", "rarity": "rare", "emoji": "🪟", "description": "Growth mindset with product and systems depth"},
]

TOTAL_CARDS = len(COMPANY_CARDS)
CARD_XP = 25
COMPLETE_XP = 500


class EarnCardRequest(BaseModel):
    company_id: str


async def _get_progress(db, user_id: str) -> dict:
    progress = await db["collection_progress"].find_one({"user_id": user_id})
    if not progress:
        progress = {
            "user_id": user_id,
            "owned_company_ids": [],
            "xp_earned": 0,
            "completion_reward_claimed": False,
            "date_first_completed": None,
            "updated_at": datetime.now(timezone.utc),
        }
        await db["collection_progress"].insert_one(progress)
    return progress


def _serialize_progress(progress: dict) -> dict:
    owned = progress.get("owned_company_ids", [])
    return {
        "owned_company_ids": owned,
        "xp_earned": progress.get("xp_earned", 0),
        "completion_percent": round(len(owned) / TOTAL_CARDS * 100, 2),
        "complete": len(owned) == TOTAL_CARDS,
        "completion_reward_claimed": progress.get("completion_reward_claimed", False),
        "date_first_completed": progress.get("date_first_completed"),
    }


@router.get("")
async def get_collection(user=Depends(get_current_user)):
    db = get_db()
    progress = await _get_progress(db, user["id"])
    serialized = _serialize_progress(progress)
    return {"cards": COMPANY_CARDS, **serialized}


@router.post("/earn")
async def earn_card(req: EarnCardRequest, user=Depends(get_current_user)):
    db = get_db()
    card = next((c for c in COMPANY_CARDS if c["id"] == req.company_id), None)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    progress = await _get_progress(db, user["id"])
    owned = progress.get("owned_company_ids", [])
    if req.company_id in owned:
        raise HTTPException(status_code=400, detail="Card already owned")

    await db["collection_progress"].update_one(
        {"user_id": user["id"]},
        {
            "$push": {"owned_company_ids": req.company_id},
            "$inc": {"xp_earned": CARD_XP},
            "$set": {"updated_at": datetime.now(timezone.utc)},
        },
    )

    try:
        gamification_result = await record_practice(user["id"], "collection", CARD_XP)
    except Exception:
        gamification_result = {}

    updated = await _get_progress(db, user["id"])
    return {
        "card": card,
        "xp_earned": CARD_XP,
        "xp_gained": gamification_result.get("xp_gained", CARD_XP),
        **_serialize_progress(updated),
    }


@router.get("/complete")
async def claim_completion_reward(user=Depends(get_current_user)):
    db = get_db()
    progress = await _get_progress(db, user["id"])
    owned = progress.get("owned_company_ids", [])

    if len(owned) != TOTAL_CARDS:
        return {"complete": False, "reward": 0}

    now = datetime.now(timezone.utc)
    already_claimed = progress.get("completion_reward_claimed", False)
    date_first_completed = progress.get("date_first_completed") or now.isoformat()

    if not already_claimed:
        await db["collection_progress"].update_one(
            {"user_id": user["id"]},
            {
                "$set": {
                    "completion_reward_claimed": True,
                    "date_first_completed": date_first_completed,
                    "updated_at": now,
                }
            },
        )
        try:
            await record_practice(user["id"], "collection_complete", COMPLETE_XP)
        except Exception:
            pass

    return {
        "complete": True,
        "reward": COMPLETE_XP if not already_claimed else 0,
        "already_claimed": already_claimed,
        "date_first_completed": date_first_completed,
    }
