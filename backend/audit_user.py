import asyncio
import sys
sys.path.insert(0, r"D:\Project-Fremen\backend")
from app.data.worlds_data import WORLD_REGISTRY as R
from app.database import gamification_collection, users_collection

async def find_test_user():
    async for doc in gamification_collection().find({}):
        uid = doc.get("user_id", "?")
        completed = doc.get("completed_competencies", {}) or {}
        done_by_world = {}
        for wid in R:
            w = R[wid]
            total = sum(len(t.levels) for t in w.towns)
            prog = [k for k in completed.get(f"{wid}:", []) if isinstance(completed.get(k), dict)]
            if len(prog) >= total and total > 0:
                done_by_world[wid] = len(prog)
        if done_by_world:
            if "dynamic" in done_by_world and "alpine" in done_by_world:
                return uid
    return None

uid = asyncio.run(find_test_user())
print("Test user uid:", uid)