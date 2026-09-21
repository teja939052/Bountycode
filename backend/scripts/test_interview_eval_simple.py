import sys
sys.path.insert(0, ".")
import asyncio
from app.services.ai_core import chat_completion, parse_json

async def test():
    system_instruction = """
You are an evaluation engine. Output ONLY JSON. No thinking, no reasoning, no explanation.

Evaluate the interview transcript against these criteria. For EACH criterion:
1. Assign a score within the specified range.
2. Quote the EXACT transcript sentence.
3. If no quote possible, score MUST be 0.

Criteria:
- situation_present (Situation): score 0-1. QUOTE REQUIRED.
- task_clarity (Task): score 0-2. QUOTE REQUIRED.
- action_specificity (Action): score 0-3. QUOTE REQUIRED.
- result_quantified (Result): score 0-2. QUOTE REQUIRED.

Output ONLY this JSON:
{
  "criteria": [{"id": "criterion_id", "score": 0, "quote": "exact text"}],
  "filler_words": [],
  "critique": "text",
  "remediation": "text"
}
"""

    prompt = """
Question: "Tell me about a time you handled a conflict in a team."
Transcript: "Last semester I was working on a group project with two teammates who had different ideas about the architecture. One wanted microservices, the other wanted a monolith. I scheduled a meeting where we each presented our pros and cons. We ended up with a modular monolith that satisfied both requirements. The project got an A."
"""

    raw = await chat_completion(
        [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2000,
    )
    
    print("RAW LENGTH:", len(raw))
    print("RAW:")
    print(raw)
    print("\n" + "="*50)
    
    try:
        parsed = parse_json(raw)
        print("PARSED:")
        print(parsed)
    except Exception as e:
        print(f"PARSE FAILED: {e}")

asyncio.run(test())
