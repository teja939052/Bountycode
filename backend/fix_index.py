import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

async def fix_index():
    client = AsyncIOMotorClient('mongodb://127.0.0.1:27017')
    db = client['placementpro']
    
    # Drop the existing uid index
    await db.users.drop_index('uid_1')
    print('Dropped uid_1 index')
    
    # Create sparse unique index
    await db.users.create_index([('uid', ASCENDING)], unique=True, sparse=True)
    print('Created sparse uid_1 index')
    
    # Verify
    indexes = await db.users.list_indexes().to_list(length=None)
    for idx in indexes:
        print(f'  {idx.get("name")}: unique={idx.get("unique")}, sparse={idx.get("sparse", False)}')
    
    client.close()

asyncio.run(fix_index())