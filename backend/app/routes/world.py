from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.gamification import get_gamification_profile

router = APIRouter(prefix="/api/v1/world", tags=["world"])
skill_router = APIRouter(prefix="/api/v1/world/skill", tags=["world-skill"])

REGIONS = [
    {
        "id": "village",
        "name": "Village",
        "order": 1,
        "xp_required_to_unlock": 0,
        "emoji": "🏘️",
        "description": "Your starting home. Learn the basics of coding and build your first streaks.",
        "reward_badge": "First Steps",
    },
    {
        "id": "forest",
        "name": "Forest",
        "order": 2,
        "xp_required_to_unlock": 200,
        "emoji": "🌲",
        "description": "Arrays and loops grow here. Master the fundamentals to light the path.",
        "reward_badge": "Forest Runner",
    },
    {
        "id": "mountain",
        "name": "Mountain",
        "order": 3,
        "xp_required_to_unlock": 500,
        "emoji": "🏔️",
        "description": "A steep climb through hashing and sliding windows. The air is thin, the XP is thick.",
        "reward_badge": "Mountain Climber",
    },
    {
        "id": "cyber-city",
        "name": "Cyber City",
        "order": 4,
        "xp_required_to_unlock": 1200,
        "emoji": "🌆",
        "description": "Neon-lit alleyways of binary search and system design. Quick reflexes required.",
        "reward_badge": "Cyber Programmer",
    },
    {
        "id": "silicon-valley",
        "name": "Silicon Valley",
        "order": 5,
        "xp_required_to_unlock": 3000,
        "emoji": "🏙️",
        "description": "Where startups become unicorns. Graphs, scalability, and product sense collide.",
        "reward_badge": "Innovator",
    },
    {
        "id": "faang-castle",
        "name": "FAANG Castle",
        "order": 6,
        "xp_required_to_unlock": 8000,
        "emoji": "🏰",
        "description": "The final fortress. Prove mastery across every domain to claim the crown.",
        "reward_badge": "FAANG Legend",
    },
]

SKILL_TREE_NODES = [
    {"id": "arrays", "name": "Arrays", "parent_id": None, "xp_cost": 100, "perk": "2x XP on array problems", "icon": "🔢", "depth": 0},
    {"id": "sliding-window", "name": "Sliding Window", "parent_id": "arrays", "xp_cost": 200, "perk": "hints +1 on array problems", "icon": "🪟", "depth": 1},
    {"id": "aptitude", "name": "Aptitude", "parent_id": "arrays", "xp_cost": 150, "perk": "+5 XP per aptitude test", "icon": "🧠", "depth": 1},
    {"id": "hashing", "name": "Hashing", "parent_id": "sliding-window", "xp_cost": 250, "perk": "Free hint reveals on hashing problems", "icon": "🔑", "depth": 2},
    {"id": "logic", "name": "Logic", "parent_id": "aptitude", "xp_cost": 200, "perk": "2x XP on logic questions", "icon": "🧩", "depth": 2},
    {"id": "binary-search", "name": "Binary Search", "parent_id": "hashing", "xp_cost": 350, "perk": "Skip boss at level 30", "icon": "🎯", "depth": 3},
    {"id": "verbal", "name": "Verbal", "parent_id": "logic", "xp_cost": 250, "perk": "hints +1 on verbal questions", "icon": "🗣️", "depth": 3},
    {"id": "graphs", "name": "Graphs", "parent_id": "binary-search", "xp_cost": 500, "perk": "Skip boss at level 40", "icon": "🕸️", "depth": 4},
]

WORLD_DEFAULTS = {
    "current_region": "village",
    "unlocked_regions": ["village"],
    "total_xp": 0,
}

SKILL_TREE_DEFAULTS = {
    "unlocked_node_ids": [],
}


async def _get_world_progress(db, user_id: str) -> dict:
    doc = await db["world_progress"].find_one({"user_id": user_id})
    if not doc:
        doc = {
            "user_id": user_id,
            "current_region": WORLD_DEFAULTS["current_region"],
            "unlocked_regions": list(WORLD_DEFAULTS["unlocked_regions"]),
            "total_xp": 0,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        await db["world_progress"].insert_one(doc)
    return doc


async def _get_skill_tree_progress(db, user_id: str) -> dict:
    doc = await db["skill_tree"].find_one({"user_id": user_id})
    if not doc:
        doc = {
            "user_id": user_id,
            "unlocked_node_ids": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        await db["skill_tree"].insert_one(doc)
    return doc


async def _get_user_xp(user_id: str) -> int:
    profile = await get_gamification_profile(user_id)
    return int(profile.get("xp", 0) or 0)


def _serialize_world(doc, xp: int) -> dict:
    regions = sorted(REGIONS, key=lambda r: r["order"])
    unlocked = doc.get("unlocked_regions", ["village"])
    current_id = doc.get("current_region", "village")

    current = next((r for r in regions if r["id"] == current_id), regions[0])
    current_index = regions.index(current)
    next_region = regions[current_index + 1] if current_index + 1 < len(regions) else None

    progress_percent = 100
    if next_region:
        required = next_region["xp_required_to_unlock"]
        progress_percent = max(0, min(100, round(xp / required * 100))) if required else 100

    return {
        "regions": regions,
        "unlocked_regions": unlocked,
        "current_region": current,
        "next_region": next_region,
        "total_xp": xp,
        "progress_percent": progress_percent,
    }


@router.get("/map")
async def get_world_map(user=Depends(get_current_user)):
    db = get_db()
    doc = await _get_world_progress(db, user["id"])
    xp = await _get_user_xp(user["id"])
    result = _serialize_world(doc, xp)
    await db["world_progress"].update_one(
        {"user_id": user["id"]},
        {"$set": {"total_xp": xp, "updated_at": datetime.now(timezone.utc)}},
    )
    return result


@router.post("/advance")
async def advance_world(user=Depends(get_current_user)):
    db = get_db()
    doc = await _get_world_progress(db, user["id"])
    xp = await _get_user_xp(user["id"])

    regions = sorted(REGIONS, key=lambda r: r["order"])
    current = next((r for r in regions if r["id"] == doc.get("current_region", "village")), regions[0])
    current_index = regions.index(current)

    if current_index + 1 >= len(regions):
        return {**_serialize_world(doc, xp), "unlocked": False, "message": "All regions unlocked"}

    next_region = regions[current_index + 1]
    if xp < next_region["xp_required_to_unlock"]:
        raise HTTPException(
            status_code=400,
            detail=f"Need {next_region['xp_required_to_unlock']} XP to unlock {next_region['name']}",
        )

    unlocked = doc.get("unlocked_regions", ["village"])
    if next_region["id"] not in unlocked:
        unlocked.append(next_region["id"])

    await db["world_progress"].update_one(
        {"user_id": user["id"]},
        {
            "$set": {
                "current_region": next_region["id"],
                "unlocked_regions": unlocked,
                "total_xp": xp,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )

    doc["current_region"] = next_region["id"]
    doc["unlocked_regions"] = unlocked
    doc["total_xp"] = xp
    return {**_serialize_world(doc, xp), "unlocked": True, "unlocked_region": next_region}


@skill_router.get("/tree")
async def get_skill_tree(user=Depends(get_current_user)):
    db = get_db()
    doc = await _get_skill_tree_progress(db, user["id"])
    return {
        "nodes": SKILL_TREE_NODES,
        "unlocked_node_ids": doc.get("unlocked_node_ids", []),
    }


class UnlockNodeRequest(BaseModel):
    node_id: str


@skill_router.post("/unlock")
async def unlock_skill_node(req: UnlockNodeRequest, user=Depends(get_current_user)):
    db = get_db()
    doc = await _get_skill_tree_progress(db, user["id"])
    unlocked = doc.get("unlocked_node_ids", [])

    node = next((n for n in SKILL_TREE_NODES if n["id"] == req.node_id), None)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    if req.node_id in unlocked:
        return {
            "nodes": SKILL_TREE_NODES,
            "unlocked_node_ids": unlocked,
            "node": node,
            "already_unlocked": True,
        }

    if node["parent_id"] and node["parent_id"] not in unlocked:
        raise HTTPException(status_code=400, detail="Unlock the parent node first")

    xp = await _get_user_xp(user["id"])
    if xp < node["xp_cost"]:
        raise HTTPException(
            status_code=400,
            detail=f"Need {node['xp_cost']} XP to unlock {node['name']}",
        )

    unlocked.append(req.node_id)
    await db["skill_tree"].update_one(
        {"user_id": user["id"]},
        {
            "$set": {
                "unlocked_node_ids": unlocked,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )

    return {
        "nodes": SKILL_TREE_NODES,
        "unlocked_node_ids": unlocked,
        "node": node,
        "already_unlocked": False,
    }
