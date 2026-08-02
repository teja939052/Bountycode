"""Skill Trees — visual progression paths for different skill areas."""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.gamification import record_practice
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/skill-trees", tags=["skill-trees"])

SKILL_TREES = {
    "algorithms": {
        "name": "Algorithm Mastery",
        "emoji": "🧮",
        "description": "Master algorithms from basics to advanced",
        "branches": [
            {
                "name": "Arrays & Strings",
                "icon": "📝",
                "levels": [
                    {"id": "arr_1", "name": "Two Pointers", "xp": 20, "type": "problems_solved", "target": 3},
                    {"id": "arr_2", "name": "Sliding Window", "xp": 30, "type": "problems_solved", "target": 5},
                    {"id": "arr_3", "name": "Prefix Sums", "xp": 40, "type": "problems_solved", "target": 8},
                ],
            },
            {
                "name": "Graphs",
                "icon": "🕸️",
                "levels": [
                    {"id": "graph_1", "name": "BFS/DFS", "xp": 30, "type": "problems_solved", "target": 3},
                    {"id": "graph_2", "name": "Shortest Path", "xp": 50, "type": "problems_solved", "target": 5},
                    {"id": "graph_3", "name": "Union-Find", "xp": 60, "type": "problems_solved", "target": 7},
                ],
            },
            {
                "name": "Dynamic Programming",
                "icon": "📊",
                "levels": [
                    {"id": "dp_1", "name": "1D DP", "xp": 40, "type": "problems_solved", "target": 3},
                    {"id": "dp_2", "name": "2D DP", "xp": 60, "type": "problems_solved", "target": 5},
                    {"id": "dp_3", "name": "Interval DP", "xp": 80, "type": "problems_solved", "target": 7},
                ],
            },
        ],
    },
    "system_design": {
        "name": "System Design",
        "emoji": "🏗️",
        "description": "Design scalable systems like a pro",
        "branches": [
            {
                "name": "Basics",
                "icon": "🏠",
                "levels": [
                    {"id": "sd_1", "name": "Load Balancing", "xp": 20, "type": "system_designs_completed", "target": 1},
                    {"id": "sd_2", "name": "Caching", "xp": 30, "type": "system_designs_completed", "target": 2},
                    {"id": "sd_3", "name": "Database Sharding", "xp": 40, "type": "system_designs_completed", "target": 3},
                ],
            },
            {
                "name": "Advanced",
                "icon": "🏙️",
                "levels": [
                    {"id": "sd_4", "name": "Microservices", "xp": 50, "type": "system_designs_completed", "target": 2},
                    {"id": "sd_5", "name": "Event-Driven Architecture", "xp": 60, "type": "system_designs_completed", "target": 3},
                    {"id": "sd_6", "name": "Global Scale", "xp": 80, "type": "system_designs_completed", "target": 4},
                ],
            },
        ],
    },
    "coding": {
        "name": "Coding Excellence",
        "emoji": "💻",
        "description": "Sharpen your coding skills",
        "branches": [
            {
                "name": "Languages",
                "icon": "🌐",
                "levels": [
                    {"id": "code_1", "name": "Python Master", "xp": 20, "type": "problems_solved", "target": 5},
                    {"id": "code_2", "name": "Java Pro", "xp": 25, "type": "problems_solved", "target": 5},
                    {"id": "code_3", "name": "C++ Expert", "xp": 30, "type": "problems_solved", "target": 5},
                ],
            },
            {
                "name": "Patterns",
                "icon": "🔧",
                "levels": [
                    {"id": "code_4", "name": "OOP Patterns", "xp": 30, "type": "problems_solved", "target": 3},
                    {"id": "code_5", "name": "Design Patterns", "xp": 40, "type": "problems_solved", "target": 5},
                    {"id": "code_6", "name": "Concurrency", "xp": 50, "type": "problems_solved", "target": 4},
                ],
            },
        ],
    },
    "interview": {
        "name": "Interview Prep",
        "emoji": "🎤",
        "description": "Ace your interviews",
        "branches": [
            {
                "name": "Behavioral",
                "icon": "💬",
                "levels": [
                    {"id": "int_1", "name": "STAR Method", "xp": 15, "type": "interviews_completed", "target": 1},
                    {"id": "int_2", "name": "Leadership Stories", "xp": 20, "type": "interviews_completed", "target": 2},
                    {"id": "int_3", "name": "Conflict Resolution", "xp": 25, "type": "interviews_completed", "target": 3},
                ],
            },
            {
                "name": "Technical",
                "icon": "🔬",
                "levels": [
                    {"id": "int_4", "name": "System Design", "xp": 30, "type": "interviews_completed", "target": 2},
                    {"id": "int_5", "name": "Coding Rounds", "xp": 40, "type": "interviews_completed", "target": 3},
                    {"id": "int_6", "name": "Behavioral Rounds", "xp": 35, "type": "interviews_completed", "target": 3},
                ],
            },
        ],
    },
}


@router.get("/all")
async def get_all_skill_trees(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    progress = user_gam.get("skill_tree_progress", {}) if user_gam else {}

    trees = []
    for key, tree in SKILL_TREES.items():
        tree_progress = progress.get(key, {})
        total_levels = sum(len(b["levels"]) for b in tree["branches"])
        completed_levels = sum(
            1 for b in tree["branches"]
            for l in b["levels"]
            if tree_progress.get(b["name"], {}).get(l["id"], {}).get("completed")
        )

        trees.append({
            "key": key,
            "name": tree["name"],
            "emoji": tree["emoji"],
            "description": tree["description"],
            "branches": tree["branches"],
            "progress": {
                "completed": completed_levels,
                "total": total_levels,
                "percentage": round(completed_levels / total_levels * 100, 1) if total_levels > 0 else 0,
            },
        })

    return {"trees": trees}


@router.post("/progress")
async def update_skill_tree_progress(req: dict, user=Depends(get_current_user)):
    tree_key = req.get("tree_key")
    branch_name = req.get("branch_name")
    level_id = req.get("level_id")
    xp_earned = req.get("xp", 0)

    if not tree_key or not branch_name or not level_id:
        raise HTTPException(status_code=400, detail="tree_key, branch_name, and level_id are required")

    tree = SKILL_TREES.get(tree_key)
    if not tree:
        raise HTTPException(status_code=404, detail="Skill tree not found")

    branch = next((b for b in tree["branches"] if b["name"] == branch_name), None)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    level = next((l for l in branch["levels"] if l["id"] == level_id), None)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$set": {
            f"skill_tree_progress.{tree_key}.{branch_name}.{level_id}": {
                "completed": True,
                "xp_earned": xp_earned,
                "completed_at": datetime.now(timezone.utc),
            }
        }},
        upsert=True,
    )

    # Check if branch is complete
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    branch_progress = user_gam.get("skill_tree_progress", {}).get(tree_key, {}).get(branch_name, {}) if user_gam else {}
    all_completed = all(
        branch_progress.get(l["id"], {}).get("completed") for l in branch["levels"]
    )

    bonus_xp = 0
    if all_completed:
        bonus_xp = sum(l["xp"] for l in branch["levels"])
        await gamification_collection.update_one(
            {"user_id": user["id"]},
            {"$inc": {"xp": bonus_xp}},
        )

    return {
        "tree_key": tree_key,
        "branch_name": branch_name,
        "level_id": level_id,
        "xp_earned": xp_earned,
        "bonus_xp": bonus_xp,
        "total_xp": xp_earned + bonus_xp,
        "branch_complete": all_completed,
    }


@router.get("/progress")
async def get_skill_tree_progress(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    progress = user_gam.get("skill_tree_progress", {}) if user_gam else {}

    total_xp = 0
    for tree_key, tree in SKILL_TREES.items():
        for branch in tree["branches"]:
            for level in branch["levels"]:
                branch_data = progress.get(tree_key, {}).get(branch["name"], {})
                level_data = branch_data.get(level["id"], {})
                if level_data.get("completed"):
                    total_xp += level.get("xp", 0)

    return {
        "total_xp": total_xp,
        "progress": progress,
    }