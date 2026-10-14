import asyncio
import sys
sys.path.insert(0, "D:/Project-Fremen/backend")

from app.database import skill_graph_collection, get_client, _collections

async def test():
    get_client()
    uid = "truth_student_a"
    
    # Check if _collections has the proxy
    print("_collections keys:", list(_collections.keys()))
    
    # Direct motor access
    from app.config import get_settings
    settings = get_settings()
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    col = db["skill_graphs"]
    
    # Count existing
    cnt = await col.count_documents({"user_id": uid})
    print(f"Direct count for {uid}: {cnt}")
    
    if cnt > 0:
        docs = await col.find({"user_id": uid}).to_list(10)
        print("Existing docs:", docs)
    
    # Try lazy collection delete
    r = await skill_graph_collection.delete_many({"user_id": uid})
    print(f"Lazy delete result: {r.deleted_count}")
    
    # Count again
    cnt2 = await col.count_documents({"user_id": uid})
    print(f"Count after lazy delete: {cnt2}")

asyncio.run(test())
