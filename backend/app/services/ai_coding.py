"""Coding challenge AI functions."""

import logging
from typing import Dict, Any
from app.services.ai_core import chat_completion, parse_json, assign_companies

logger = logging.getLogger(__name__)

TIME_LIMITS = {"easy": 1800, "medium": 2400, "hard": 3600}


async def generate_coding_challenge(
    difficulty: str,
    topic: str,
    language: str,
) -> Dict[str, Any]:
    system_prompt = f"""You are an expert coding challenge designer creating problems for {difficulty} difficulty.
Target topic: {topic}
Solution language: {language}

Generate a unique, well-structured coding challenge. The problem should be:
- Original (not a direct copy of famous problems)
- Clearly defined with unambiguous input/output
- Appropriate difficulty for {difficulty} level
- Related to the topic: {topic}
- Include at least one meaningful follow-up variant or edge-case twist that probes deeper understanding.

The output MUST be valid JSON with this exact structure:
{{
    "title": "Problem Title",
    "description": "Full problem description with clear explanation",
    "examples": [
        {{
            "input": "Example input",
            "output": "Example output",
            "explanation": "Step-by-step explanation"
        }}
    ],
    "constraints": [
        "constraint 1 (e.g., 1 <= n <= 10^5)",
        "constraint 2"
    ],
    "test_cases": [
        {{
            "input": "Test input",
            "expected_output": "Expected output",
            "is_hidden": false
        }},
        {{
            "input": "Hidden test input",
            "expected_output": "Hidden expected output",
            "is_hidden": true
        }}
    ],
    "hints": [
        "Hint 1: Think about the approach...",
        "Hint 2: Consider using...",
        "Hint 3: The time complexity should be..."
    ],
    "follow_up": "Can you solve it with O(n) time and O(1) space?",
    "time_limit_seconds": 1800
}}

Generate 2 visible test cases and 3 hidden test cases.
Hints should progressively reveal the approach.
Time limit: 1800 (easy), 2400 (medium), 3600 (hard).

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Create a {difficulty} coding challenge about {topic} for {language}."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("title", f"{topic.title()} Challenge")
    parsed.setdefault("description", "Solve the given coding problem.")
    parsed.setdefault("examples", [{"input": "[]", "output": "0", "explanation": ""}])
    parsed.setdefault("constraints", ["1 <= n <= 1000"])
    parsed.setdefault("test_cases", [{"input": "[]", "expected_output": "0", "is_hidden": False}])
    parsed.setdefault("hints", ["Think about the approach carefully."])
    parsed.setdefault("follow_up", "Can you optimize your solution?")
    parsed.setdefault("companies", assign_companies())
    parsed.setdefault("time_limit_seconds", TIME_LIMITS.get(difficulty, 1800))

    return parsed