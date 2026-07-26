from datetime import datetime, timezone, timedelta
from app.database import study_groups_collection, contests_collection, contest_entries_collection
from bson import ObjectId


async def create_study_group(
    name: str,
    creator_id: str,
    description: str = "",
    max_members: int = 10,
) -> dict:
    group = {
        "name": name,
        "description": description,
        "creator_id": creator_id,
        "members": [creator_id],
        "max_members": max_members,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await study_groups_collection.insert_one(group)
    return {"group_id": str(result.inserted_id), "name": name}


async def join_study_group(group_id: str, user_id: str) -> dict:
    try:
        group = await study_groups_collection.find_one({"_id": ObjectId(group_id)})
    except Exception:
        return {"success": False, "message": "Invalid group ID"}
    if not group:
        return {"success": False, "message": "Group not found"}
    if user_id in group.get("members", []):
        return {"success": False, "message": "Already a member"}
    if len(group.get("members", [])) >= group.get("max_members", 10):
        return {"success": False, "message": "Group is full"}
    await study_groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$push": {"members": user_id}},
    )
    return {"success": True, "message": f"Joined {group['name']}!"}


async def get_study_groups(user_id: str = None, limit: int = 10) -> list:
    query = {}
    if user_id:
        query = {"members": user_id}
    cursor = study_groups_collection.find(query).limit(limit)
    groups = []
    async for doc in cursor:
        groups.append({
            "id": str(doc["_id"]),
            "name": doc.get("name", ""),
            "description": doc.get("description", ""),
            "members_count": len(doc.get("members", [])),
            "max_members": doc.get("max_members", 10),
            "is_member": user_id in doc.get("members", []) if user_id else False,
        })
    return groups


async def create_contest(
    title: str,
    description: str,
    contest_type: str,
    start_date: datetime,
    end_date: datetime,
    prizes: list = None,
) -> dict:
    contest = {
        "title": title,
        "description": description,
        "contest_type": contest_type,
        "start_date": start_date,
        "end_date": end_date,
        "prizes": prizes or ["1st Place Badge", "500 XP", "Bragging Rights"],
        "status": "upcoming",
        "entries_count": 0,
        "created_at": datetime.now(timezone.utc),
    }
    result = await contests_collection.insert_one(contest)
    return {"contest_id": str(result.inserted_id), "title": title}


async def enter_contest(contest_id: str, user_id: str, score: float, metadata: dict = None) -> dict:
    try:
        contest = await contests_collection.find_one({"_id": ObjectId(contest_id)})
    except Exception:
        return {"success": False, "message": "Invalid contest ID"}
    if not contest:
        return {"success": False, "message": "Contest not found"}
    now = datetime.now(timezone.utc)
    if now < contest["start_date"]:
        return {"success": False, "message": "Contest hasn't started yet"}
    if now > contest["end_date"]:
        return {"success": False, "message": "Contest has ended"}
    existing = await contest_entries_collection.find_one({"contest_id": contest_id, "user_id": user_id})
    if existing:
        if score > existing.get("score", 0):
            await contest_entries_collection.update_one(
                {"_id": existing["_id"]},
                {"$set": {"score": score, "metadata": metadata, "updated_at": now}},
            )
            return {"success": True, "message": "Score updated!", "improved": True}
        return {"success": False, "message": "Already entered with a better score"}
    entry = {
        "contest_id": contest_id,
        "user_id": user_id,
        "score": score,
        "metadata": metadata or {},
        "entered_at": now,
    }
    await contest_entries_collection.insert_one(entry)
    await contests_collection.update_one({"_id": ObjectId(contest_id)}, {"$inc": {"entries_count": 1}})
    return {"success": True, "message": "Entered contest!"}


async def get_contest_leaderboard(contest_id: str, limit: int = 10) -> list:
    cursor = contest_entries_collection.find({"contest_id": contest_id}).sort("score", -1).limit(limit)
    leaderboard = []
    rank = 1
    async for doc in cursor:
        leaderboard.append({
            "rank": rank,
            "user_id": doc.get("user_id", ""),
            "score": doc.get("score", 0),
            "entered_at": doc.get("entered_at"),
        })
        rank += 1
    return leaderboard


async def get_active_contests() -> list:
    now = datetime.now(timezone.utc)
    cursor = contests_collection.find({
        "start_date": {"$lte": now},
        "end_date": {"$gte": now},
    })
    contests = []
    async for doc in cursor:
        contests.append({
            "id": str(doc["_id"]),
            "title": doc.get("title", ""),
            "description": doc.get("description", ""),
            "contest_type": doc.get("contest_type", ""),
            "end_date": doc.get("end_date"),
            "entries_count": doc.get("entries_count", 0),
            "prizes": doc.get("prizes", []),
        })
    return contests
