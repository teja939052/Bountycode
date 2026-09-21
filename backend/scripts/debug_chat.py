import asyncio
from app.services.ai_core import chat_completion

async def test():
    raw = await chat_completion(
        [
            {"role": "system", "content": 'Return ONLY this JSON: {"test": 1}'},
            {"role": "user", "content": "Say hello"},
        ],
        temperature=0.1,
        max_tokens=100,
    )
    print("RAW:")
    print(repr(raw))
    print("\nLAST 200:")
    print(raw[-200:])

asyncio.run(test())
