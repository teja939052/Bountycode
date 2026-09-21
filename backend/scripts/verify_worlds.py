import sys
sys.path.insert(0, ".")
import asyncio
from app.content.worlds_7_to_9 import get_world_9
from app.content.worlds_10_to_12 import get_world_10, get_world_12

async def test():
    w9 = get_world_9()
    w10 = get_world_10()
    w12 = get_world_12()
    
    for world, name in [(w9, "World 9"), (w10, "World 10"), (w12, "World 12")]:
        if isinstance(world, dict):
            print(f"{name}: {world.get('name', 'unnamed')}")
            print(f"  Levels: {len(world.get('levels', []))}")
            print(f"  Has boss: {bool(world.get('boss_battle'))}")
            print(f"  Keys: {list(world.keys())[:8]}")
        else:
            print(f"{name}: {type(world).__name__}")

asyncio.run(test())
