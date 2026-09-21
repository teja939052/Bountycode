"""Debug interview evaluator parsing."""
import sys
sys.path.insert(0, ".")
import asyncio
from app.services.ai_core import chat_completion, parse_json

async def test():
    system_instruction = """
You are an elite Tech Lead evaluating a candidate.
Evaluate the response against these criteria. For EACH criterion:
1. Assign a score within the specified range.
2. Quote the EXACT transcript sentence that justifies the score.
3. If you cannot find a supporting quote, score MUST be 0 for that criterion.

Criteria:
- situation_present (Situation): score 0-1. QUOTE REQUIRED.
- task_clarity (Task): score 0-2. QUOTE REQUIRED.
- action_specificity (Action): score 0-3. QUOTE REQUIRED.
- result_quantified (Result): score 0-2. QUOTE REQUIRED.

Return ONLY a JSON object:
{
  "criteria": [
    {"id": "criterion_id", "score": 0, "quote": "exact transcript text"}
  ],
  "filler_words": ["um", "like"],
  "critique": "Detailed assessment",
  "remediation": "One specific drill"
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
        max_tokens=1000,
    )
    print("RAW OUTPUT:")
    print(raw[:2000])
    print("\nPARSED:")
    parsed = parse_json(raw)
    print(parsed)

asyncio.run(test())
