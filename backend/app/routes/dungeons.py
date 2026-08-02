from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.middleware.auth import get_current_user, optional_get_current_user
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/dungeons", tags=["dungeons"])

DUNGEONS = [
    {
        "id": "google",
        "company": "Google",
        "emoji": "🔍",
        "reward_chest": "Google Chest",
        "stages": [
            {"type": "OA", "title": "OA: Array & Sliding Window"},
            {"type": "OA", "title": "OA: Graph Traversal"},
            {"type": "OA", "title": "OA: Dynamic Programming"},
            {"type": "Interview", "title": "Interview: System Design"},
            {"type": "Behavioral", "title": "Behavioral: Leadership & Googleyness"},
        ],
    },
    {
        "id": "amazon",
        "company": "Amazon",
        "emoji": "📦",
        "reward_chest": "Amazon Chest",
        "stages": [
            {"type": "OA", "title": "OA: Greedy & Sorting"},
            {"type": "OA", "title": "OA: Trees & Heaps"},
            {"type": "OA", "title": "OA: Two Pointers"},
            {"type": "Interview", "title": "Interview: Scale & Distributed Systems"},
            {"type": "Behavioral", "title": "Behavioral: 14 Leadership Principles"},
        ],
    },
    {
        "id": "meta",
        "company": "Meta",
        "emoji": "👓",
        "reward_chest": "Meta Chest",
        "stages": [
            {"type": "OA", "title": "OA: Strings & Prefix Sum"},
            {"type": "OA", "title": "OA: Stacks & Queues"},
            {"type": "OA", "title": "OA: Recursion & Backtracking"},
            {"type": "Interview", "title": "Interview: Product Systems"},
            {"type": "Behavioral", "title": "Behavioral: Move Fast & Execution"},
        ],
    },
    {
        "id": "microsoft",
        "company": "Microsoft",
        "emoji": "🪟",
        "reward_chest": "Microsoft Chest",
        "stages": [
            {"type": "OA", "title": "OA: Arrays & Math"},
            {"type": "OA", "title": "OA: Linked Lists"},
            {"type": "OA", "title": "OA: Dynamic Programming"},
            {"type": "Interview", "title": "Interview: System Design"},
            {"type": "Behavioral", "title": "Behavioral: Growth Mindset"},
        ],
    },
    {
        "id": "apple",
        "company": "Apple",
        "emoji": "🍎",
        "reward_chest": "Apple Chest",
        "stages": [
            {"type": "OA", "title": "OA: Strings & Hashing"},
            {"type": "OA", "title": "OA: Binary Search"},
            {"type": "OA", "title": "OA: Trees"},
            {"type": "Interview", "title": "Interview: Systems & Frameworks"},
            {"type": "Behavioral", "title": "Behavioral: Craftsmanship & Collaboration"},
        ],
    },
]

DUNGEON_REWARD_XP = 150


def serialize_run(r):
    return {
        "id": str(r["_id"]),
        "user_id": r["user_id"],
        "dungeon_id": r["dungeon_id"],
        "current_stage": r.get("current_stage", 0),
        "completed_stages": r.get("completed_stages", []),
        "status": r.get("status", "active"),
        "started_at": r["started_at"].isoformat() if isinstance(r["started_at"], datetime) else str(r["started_at"]),
        "completed_at": r.get("completed_at").isoformat() if isinstance(r.get("completed_at"), datetime) else r.get("completed_at"),
    }


def _find_dungeon(dungeon_id: str):
    return next((d for d in DUNGEONS if d["id"] == dungeon_id), None)


@router.get("")
async def list_dungeons(user=Depends(optional_get_current_user)):
    db = get_db()
    result = {"dungeons": DUNGEONS}
    if user:
        active_run = await db["dungeon_runs"].find_one({"user_id": user["id"], "status": "active"})
        result["active_run"] = serialize_run(active_run) if active_run else None
        completions = []
        cursor = db["dungeon_completions"].find({"user_id": user["id"]})
        async for c in cursor:
            completions.append(c["dungeon_id"])
        result["completed"] = completions
    return result


@router.post("/{dungeon_id}/start")
async def start_dungeon(dungeon_id: str, user=Depends(get_current_user)):
    db = get_db()
    if not _find_dungeon(dungeon_id):
        raise HTTPException(status_code=404, detail="Dungeon not found")
    existing = await db["dungeon_runs"].find_one({"user_id": user["id"], "dungeon_id": dungeon_id, "status": "active"})
    if existing:
        raise HTTPException(status_code=409, detail="An active run already exists for this dungeon")

    run = {
        "user_id": user["id"],
        "dungeon_id": dungeon_id,
        "current_stage": 0,
        "completed_stages": [],
        "status": "active",
        "started_at": datetime.now(timezone.utc),
        "completed_at": None,
    }
    result = await db["dungeon_runs"].insert_one(run)
    run["_id"] = result.inserted_id
    return serialize_run(run)


@router.post("/{dungeon_id}/advance")
async def advance_dungeon(dungeon_id: str, body: dict, user=Depends(get_current_user)):
    db = get_db()
    dungeon = _find_dungeon(dungeon_id)
    if not dungeon:
        raise HTTPException(status_code=404, detail="Dungeon not found")

    stage_index = body.get("stage_index")
    if not isinstance(stage_index, int) or stage_index < 0 or stage_index >= len(dungeon["stages"]):
        raise HTTPException(status_code=400, detail="Invalid stage index")

    run = await db["dungeon_runs"].find_one({"user_id": user["id"], "dungeon_id": dungeon_id, "status": "active"})
    if not run:
        raise HTTPException(status_code=404, detail="No active run for this dungeon")
    if stage_index != run.get("current_stage", 0):
        raise HTTPException(status_code=400, detail="Stage out of order")

    completed = list(run.get("completed_stages", []))
    if stage_index not in completed:
        completed.append(stage_index)

    is_last = stage_index == len(dungeon["stages"]) - 1
    if is_last:
        now = datetime.now(timezone.utc)
        await db["dungeon_runs"].update_one(
            {"_id": run["_id"]},
            {"$set": {"status": "completed", "completed_stages": completed, "completed_at": now}},
        )
        await db["dungeon_completions"].update_one(
            {"user_id": user["id"], "dungeon_id": dungeon_id},
            {"$set": {"user_id": user["id"], "dungeon_id": dungeon_id, "completed_at": now}},
            upsert=True,
        )
        try:
            await record_practice(user["id"], "dungeon", DUNGEON_REWARD_XP)
        except Exception:
            pass
    else:
        await db["dungeon_runs"].update_one(
            {"_id": run["_id"]},
            {"$set": {"current_stage": stage_index + 1, "completed_stages": completed}},
        )

    updated = await db["dungeon_runs"].find_one({"_id": run["_id"]})
    return serialize_run(updated)


@router.get("/completed")
async def completed_dungeons(user=Depends(get_current_user)):
    db = get_db()
    completions = []
    cursor = db["dungeon_completions"].find({"user_id": user["id"]}).sort("completed_at", -1)
    async for c in cursor:
        dungeon = _find_dungeon(c["dungeon_id"])
        completions.append({
            "dungeon_id": c["dungeon_id"],
            "company": dungeon["company"] if dungeon else c["dungeon_id"],
            "emoji": dungeon["emoji"] if dungeon else "🎁",
            "reward_chest": dungeon["reward_chest"] if dungeon else "Mystery Chest",
            "completed_at": c["completed_at"].isoformat() if isinstance(c["completed_at"], datetime) else str(c["completed_at"]),
        })
    return {"completed": completions}
