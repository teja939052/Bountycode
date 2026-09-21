import sys
sys.path.insert(0, ".")
import asyncio
from app.services.ai_core import chat_completion

async def test():
    raw = await chat_completion(
        [
            {"role": "system", "content": "Output ONLY this JSON: {\"test\": 1}"},
            {"role": "user", "content": "Say hello"},
        ],
        temperature=0.1,
        max_tokens=200,
    )
    print("RAW:")
    print(raw)
    print("\n" + "="*50)
    
    # Try to find JSON
    import json
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        candidate = raw[start:end]
        print("JSON CANDIDATE:")
        print(candidate)
        try:
            parsed = json.loads(candidate)
            print("\nPARSED:")
            print(parsed)
        except json.JSONDecodeError as e:
            print(f"\nPARSE FAILED: {e}")

asyncio.run(test())
