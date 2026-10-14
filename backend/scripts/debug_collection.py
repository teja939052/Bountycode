import asyncio
import sys
sys.path.insert(0, "D:/Project-Fremen/backend")

from app.database import skill_graph_collection, get_client

async def test():
    # Init client
    get_client()
    print("Collection proxy:", skill_graph_collection)
    print("Has delete_many:", hasattr(skill_graph_collection, 'delete_many'))
    
    # Try delete
    r = await skill_graph_collection.delete_many({"user_id": "truth_student_a"})
    print("Deleted count:", r.deleted_count)
    
    # Try insert
    from motor.motor_asyncio import AsyncIOMotorClient
    from app.config import get_settings
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    col = db["skill_graphs"]
    r2 = await col.insert_one({"user_id": "truth_student_a", "category": "coding", "score": 90.0})
    print("Inserted id:", r2.inserted_id)
    
    # Cleanup
    await col.delete_one({"_id": r2.inserted_id})

asyncio.run(test())
