from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.gamification import get_gamification_profile, record_practice

router = APIRouter(prefix="/api/v1/journey", tags=["journey"])

REGIONS = [
    {"id": "village", "name": "Village", "emoji": "🏡", "order": 1, "xp_required": 0, "buildings": ["interview_hub", "merchant"]},
    {"id": "forest", "name": "Forest", "emoji": "🌲", "order": 2, "xp_required": 200, "buildings": ["arena", "dungeon"]},
    {"id": "mountain", "name": "Mountain", "emoji": "⛰️", "order": 3, "xp_required": 500, "buildings": ["guild_hall", "collection"]},
    {"id": "cyber-city", "name": "Cyber City", "emoji": "🌆", "order": 4, "xp_required": 1200, "buildings": ["interview_hub", "pvp"]},
    {"id": "silicon-valley", "name": "Silicon Valley", "emoji": "🏢", "order": 5, "xp_required": 3000, "buildings": ["showcase", "merchant"]},
    {"id": "faang-castle", "name": "FAANG Castle", "emoji": "🏰", "order": 6, "xp_required": 8000, "buildings": ["interview_hub", "guild_hall"]},
    {"id": "founder-island", "name": "Founder Island", "emoji": "🏝️", "order": 7, "xp_required": 20000, "buildings": ["showcase", "arena", "merchant"]},
    {"id": "legend-hall", "name": "Legend Hall", "emoji": "🏛️", "order": 8, "xp_required": 50000, "buildings": ["collection", "pvp", "dungeon"]},
]

BUILDINGS = {
    "interview_hub": {"label": "Interview Hub", "icon": "🎤"},
    "arena": {"label": "Arena", "icon": "⚔️"},
    "guild_hall": {"label": "Guild Hall", "icon": "🛡️"},
    "dungeon": {"label": "Dungeon", "icon": "🕳️"},
    "showcase": {"label": "Showcase", "icon": "🏆"},
    "merchant": {"label": "Merchant", "icon": "🛒"},
    "collection": {"label": "Collection", "icon": "📚"},
    "pvp": {"label": "PvP Arena", "icon": "🥊"},
}

REGION_BY_ID = {r["id"]: r for r in REGIONS}
REGION_BY_ORDER = {r["order"]: r for r in REGIONS}


def _default_progress(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "current_region": REGIONS[0]["id"],
        "fog_cleared_regions": [],
        "completed_quests": [],
        "last_seen": datetime.now(timezone.utc),
    }


async def _get_progress(db, user_id: str) -> dict:
    doc = await db["journey_progress"].find_one({"user_id": user_id})
    if not doc:
        doc = _default_progress(user_id)
        await db["journey_progress"].insert_one(doc)
    return doc


def _derive_current_region(total_xp: int) -> dict:
    current = REGIONS[0]
    for region in REGIONS:
        if total_xp >= region["xp_required"]:
            current = region
    return current


def _next_region_for(total_xp: int):
    for region in REGIONS:
        if total_xp < region["xp_required"]:
            return region
    return None


class MoveRequest(BaseModel):
    region_id: str


class QuestCompleteRequest(BaseModel):
    region_id: str
    quest_index: int


@router.get("")
async def get_journey(user=Depends(get_current_user)):
    db = get_db()
    profile = await get_gamification_profile(user["id"])
    total_xp = profile.get("xp", 0) or 0

    progress = await _get_progress(db, user["id"])
    derived = _derive_current_region(total_xp)
    if progress.get("current_region") != derived["id"]:
        await db["journey_progress"].update_one(
            {"user_id": user["id"]},
            {"$set": {"current_region": derived["id"], "last_seen": datetime.now(timezone.utc)}},
        )
        progress["current_region"] = derived["id"]

    next_region = _next_region_for(total_xp)
    progress_percent = 100
    if next_region:
        progress_percent = min(100, int((total_xp / next_region["xp_required"]) * 100))

    completed_quests = progress.get("completed_quests", [])
    return {
        "regions": REGIONS,
        "buildings": BUILDINGS,
        "current_region": derived,
        "total_xp": total_xp,
        "fog_cleared_regions": progress.get("fog_cleared_regions", []),
        "completed_quests": completed_quests,
        "quests_completed": len(completed_quests),
        "next_region": next_region,
        "progress_percent": progress_percent,
    }


@router.post("/move")
async def move_to_region(req: MoveRequest, user=Depends(get_current_user)):
    db = get_db()
    region = REGION_BY_ID.get(req.region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    profile = await get_gamification_profile(user["id"])
    total_xp = profile.get("xp", 0) or 0
    if total_xp < region["xp_required"]:
        raise HTTPException(status_code=403, detail=f"{region['name']} requires {region['xp_required']} XP")

    await db["journey_progress"].update_one(
        {"user_id": user["id"]},
        {"$set": {"current_region": region["id"], "last_seen": datetime.now(timezone.utc)}},
        upsert=True,
    )

    return {"current_region": region, "message": f"Entered {region['name']}"}


@router.post("/quest/complete")
async def complete_quest(req: QuestCompleteRequest, user=Depends(get_current_user)):
    db = get_db()
    if req.quest_index not in (0, 1, 2):
        raise HTTPException(status_code=400, detail="quest_index must be 0-2")

    region = REGION_BY_ID.get(req.region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    profile = await get_gamification_profile(user["id"])
    total_xp = profile.get("xp", 0) or 0
    if total_xp < region["xp_required"]:
        raise HTTPException(status_code=403, detail=f"{region['name']} is not unlocked")

    progress = await _get_progress(db, user["id"])
    completed = set(progress.get("completed_quests", []))
    quest_key = f"{region['id']}:{req.quest_index}"
    if quest_key in completed:
        raise HTTPException(status_code=400, detail="Quest already completed")

    completed.add(quest_key)
    update = {
        "$push": {"completed_quests": quest_key},
        "$set": {"last_seen": datetime.now(timezone.utc)},
    }

    region_quests = [k for k in completed if k.startswith(f"{region['id']}:")]
    result = {
        "completed": True,
        "quest_key": quest_key,
        "quests_in_region": len(region_quests),
        "fog_cleared": False,
        "fog_cleared_region": None,
        "xp_gained": 0,
    }

    if len(region_quests) >= 3:
        next_region = REGION_BY_ORDER.get(region["order"] + 1)
        if next_region:
            fog_cleared = progress.get("fog_cleared_regions", [])
            if next_region["id"] not in fog_cleared:
                update["$push"]["fog_cleared_regions"] = next_region["id"]
            result["fog_cleared"] = True
            result["fog_cleared_region"] = next_region["id"]
        practice = await record_practice(user["id"], "quest", 0, {"source": "journey"})
        result["xp_gained"] = practice.get("xp_gained", 0)

    await db["journey_progress"].update_one({"user_id": user["id"]}, update, upsert=True)
    updated = await _get_progress(db, user["id"])
    result["completed_quests"] = updated.get("completed_quests", [])
    result["fog_cleared_regions"] = updated.get("fog_cleared_regions", [])
    result["quests_completed"] = len(updated.get("completed_quests", []))

    return result
