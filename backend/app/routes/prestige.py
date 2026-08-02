from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.gamification import get_gamification_profile

router = APIRouter(prefix="/api/v1/prestige", tags=["prestige"])

MAX_PRESTIGE_LEVEL = 10

PRESTIGE_THRESHOLDS = {
    1: 5000,
    2: 15000,
    3: 35000,
    4: 70000,
    5: 120000,
    6: 200000,
    7: 320000,
    8: 500000,
    9: 800000,
    10: 1200000,
}

PRESTIGE_PERKS = {
    1: {"level": 1, "title": "Bronze Sage", "emote": "🥉", "border": "#c084fc", "bonus_multiplier": 1.1},
    2: {"level": 2, "title": "Silver Code Adept", "emote": "🥈", "border": "#94a3b8", "bonus_multiplier": 1.25},
    3: {"level": 3, "title": "Gold Oracle", "emote": "🥇", "border": "#fbbf24", "bonus_multiplier": 1.4},
    4: {"level": 4, "title": "Emerald Sentinel", "emote": "🟢", "border": "#34d399", "bonus_multiplier": 1.6},
    5: {"level": 5, "title": "Sky Master", "emote": "🔵", "border": "#38bdf8", "bonus_multiplier": 1.8},
    6: {"level": 6, "title": "Purple Archon", "emote": "🟣", "border": "#a855f7", "bonus_multiplier": 2.0},
    7: {"level": 7, "title": "Pink Phantom", "emote": "🌸", "border": "#f472b6", "bonus_multiplier": 2.5},
    8: {"level": 8, "title": "Rose Tyrant", "emote": "🌹", "border": "#fb7185", "bonus_multiplier": 3.0},
    9: {"level": 9, "title": "Inferno Lord", "emote": "🔥", "border": "#fb923c", "bonus_multiplier": 4.0},
    10: {"level": 10, "title": "Prestige God", "emote": "👑", "border": "#facc15", "bonus_multiplier": 5.0},
}


def _build_state(level: int, prestige_xp, prestiged_at) -> dict:
    next_level = level + 1 if level < MAX_PRESTIGE_LEVEL else None
    return {
        "level": level,
        "bonus_multiplier": float(PRESTIGE_PERKS[level]["bonus_multiplier"]) if level > 0 else 1.0,
        "max_level": MAX_PRESTIGE_LEVEL,
        "next_requirements": (
            {"level": next_level, "xp_threshold": PRESTIGE_THRESHOLDS[next_level]}
            if next_level is not None else None
        ),
        "perks": {
            "current": PRESTIGE_PERKS.get(level),
            "next": PRESTIGE_PERKS.get(next_level) if next_level is not None else None,
        },
        "prestige_xp": prestige_xp,
        "prestiged_at": prestiged_at,
    }


@router.get("")
async def get_prestige(user=Depends(get_current_user)):
    db = get_db()
    doc = await db["prestige"].find_one({"user_id": user["id"]})
    level = doc.get("level", 0) if doc else 0
    profile = await get_gamification_profile(user["id"])
    state = _build_state(level, doc.get("prestige_xp") if doc else None, doc.get("prestiged_at") if doc else None)
    state["total_xp"] = profile.get("xp", 0)
    req = state["next_requirements"]
    state["xp_needed"] = max(0, req["xp_threshold"] - state["total_xp"]) if req else 0
    return state


@router.post("/reset")
async def prestige_reset(user=Depends(get_current_user)):
    db = get_db()
    doc = await db["prestige"].find_one({"user_id": user["id"]})
    level = doc.get("level", 0) if doc else 0
    if level >= MAX_PRESTIGE_LEVEL:
        raise HTTPException(status_code=400, detail="Already at max prestige level")

    next_level = level + 1
    threshold = PRESTIGE_THRESHOLDS[next_level]
    profile = await get_gamification_profile(user["id"])
    xp = profile.get("xp", 0)
    if xp < threshold:
        raise HTTPException(
            status_code=400,
            detail=f"Need {threshold} XP for Prestige {next_level}, you have {xp} XP",
        )

    now = datetime.now(timezone.utc)
    await db["prestige"].update_one(
        {"user_id": user["id"]},
        {
            "$inc": {"level": 1},
            "$set": {
                "prestiged_at": now,
                "last_threshold_met": threshold,
                "prestige_xp": xp,
            },
        },
        upsert=True,
    )
    doc = await db["prestige"].find_one({"user_id": user["id"]})
    new_level = doc.get("level", 1)
    state = _build_state(new_level, doc.get("prestige_xp"), doc.get("prestiged_at"))
    state["total_xp"] = xp
    state["prestiged"] = True
    state["threshold_met"] = threshold
    return state
