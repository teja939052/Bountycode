import sys
sys.path.insert(0, ".")
import asyncio
from app.services.ai_core import chat_completion

async def test():
    raw = await chat_completion(
        [
            {"role": "user", "content": 'Output ONLY this JSON: {"test": 1}'},
        ],
        temperature=0.1,
        max_tokens=2000,
    )
    print("RAW LENGTH:", len(raw))
    print("LAST 200:")
    print(raw[-200:])

asyncio.run(test())
