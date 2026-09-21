"""Debug interview evaluator parsing - detailed."""
import sys
sys.path.insert(0, ".")
import asyncio
import json
from app.services.ai_core import chat_completion

async def test():
    system_instruction = """
Return ONLY a JSON object:
{
  "criteria": [
    {"id": "situation_present", "score": 1, "quote": "exact text"}
  ],
  "filler_words": [],
  "critique": "text",
  "remediation": "text"
}
"""

    prompt = """
Question: "Tell me about a time you handled a conflict in a team."
Transcript: "Last semester I was working on a group project with two teammates who had different ideas about the architecture. One wanted microservices, the other wanted a monolith. I scheduled a meeting where we each presented our pros and cons. We ended up with a modular monolith that satisfied both requirements. The project got an A and the professor said it was the best architecture he'd seen that semester."
"""

    raw = await chat_completion(
        [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=800,
    )
    
    # Show last 500 chars to find JSON
    print("RAW OUTPUT (last 500 chars):")
    print(raw[-500:])
    print("\n" + "="*50)
    
    # Try to find JSON manually
    start = raw.rfind("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        candidate = raw[start:end]
        print("FOUND JSON CANDIDATE:")
        print(candidate[:1000])
        try:
            parsed = json.loads(candidate)
            print("\nPARSED SUCCESSFULLY:")
            print(parsed)
        except json.JSONDecodeError as e:
            print(f"\nPARSE FAILED: {e}")

asyncio.run(test())
