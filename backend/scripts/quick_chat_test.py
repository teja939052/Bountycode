import sys
sys.path.insert(0, ".")
import asyncio
from app.services.ai_core import chat_completion

async def test():
    try:
        raw = await chat_completion(
            [{"role": "user", "content": 'Say hello in JSON: {"message": "..."}'}],
            temperature=0.1,
            max_tokens=50,
        )
        print("OK:", raw[:200])
    except Exception as e:
        print("ERROR:", e)

asyncio.run(test())
