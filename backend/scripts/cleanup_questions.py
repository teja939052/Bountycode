"""Cleanup script: remove seed questions from MongoDB to save storage.

Run: python backend/scripts/cleanup_questions.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings
from app.services import question_store

settings = get_settings()


async def cleanup():
    db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = db_client[settings.DATABASE_NAME]
    collection = db["curated_questions"]

    # Load all seed questions into memory
    question_store.load_all()
    seed_ids = [q["id"] for q in question_store._questions if q.get("id")]

    print(f"Loaded {len(seed_ids)} seed questions from files")

    # Delete seed questions from MongoDB
    from bson import ObjectId
    mongo_seed_ids = []
    for qid in seed_ids:
        if ObjectId.is_valid(qid):
            mongo_seed_ids.append(ObjectId(qid))

    if mongo_seed_ids:
        result = await collection.delete_many({"_id": {"$in": mongo_seed_ids}})
        print(f"Deleted {result.deleted_count} seed questions from MongoDB")
    else:
        print("No valid ObjectIds found in seed questions")

    # Show remaining count
    remaining = await collection.count_documents({})
    print(f"Remaining questions in MongoDB: {remaining}")

    # Show storage stats
    stats = await db.command("dbStats")
    storage_mb = stats.get("storageSize", 0) / (1024 * 1024)
    data_mb = stats.get("dataSize", 0) / (1024 * 1024)
    print(f"\nStorage: {storage_mb:.2f} MB (storage), {data_mb:.2f} MB (data)")


if __name__ == "__main__":
    asyncio.run(cleanup())
