"""System design AI functions."""

import logging
from typing import Dict, Any
from app.services.ai_core import chat_completion, parse_json

logger = logging.getLogger(__name__)


async def generate_system_design_question(
    difficulty: str,
    topic: str,
) -> Dict[str, Any]:
    system_prompt = f"""You are a system design interview expert. Generate realistic system design questions.

Difficulty: {difficulty}
Topic: {topic}

DIFFICULTY GUIDELINES:
- easy: Design a URL shortener, Pastebin, Rate Limiter (small scale, few components)
- medium: Design a chat system, News Feed, Notification system (moderate scale, multiple services)
- hard: Design Google Search, WhatsApp at scale, Uber, YouTube (massive scale, complex distributed systems)

The output MUST be valid JSON:
{{
    "question": "Design a [system] that [requirements]. Users should be able to [features]. Scale: [expected load].",
    "hints": [
        "Start by clarifying requirements and constraints",
        "Think about the core entities and their relationships",
        "Consider read-heavy vs write-heavy patterns",
        "Think about data storage and caching strategies"
    ],
    "expected_components": [
        "Load Balancer",
        "API Gateway",
        "Application Servers",
        "Database (specify type)",
        "Cache Layer",
        "Message Queue",
        "CDN"
    ],
    "difficulty": "{difficulty}",
    "topic": "{topic}"
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a {difficulty} system design question about {topic}."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("question", f"Design a scalable {topic} system.")
    parsed.setdefault("hints", ["Start with requirements gathering", "Think about scale and bottlenecks"])
    parsed.setdefault("expected_components", ["Load Balancer", "Application Server", "Database", "Cache"])
    parsed.setdefault("difficulty", difficulty)
    parsed.setdefault("topic", topic)

    return parsed


async def evaluate_system_design_answer(
    question: str,
    answer: str,
    diagram_description: str,
) -> Dict[str, Any]:
    system_prompt = """You are a system design interview evaluator. Score the candidate's response.

EVALUATION CRITERIA (score 1-10):
1. Requirements clarity (functional + non-functional)
2. High-level design correctness
3. Component selection and justification
4. Scalability discussion
5. Trade-off analysis
6. Database design
7. Caching strategy
8. API design
9. Communication clarity
10. Handling bottlenecks

The output MUST be valid JSON:
{
    "score": 7,
    "strengths": ["Strong point 1", "Strong point 2"],
    "improvements": ["Area to improve 1", "Area to improve 2"],
    "missing_concepts": ["Important concept they missed 1", "Concept 2"],
    "ideal_design": "Brief description of what an ideal answer would include..."
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {question}\n\nAnswer: {answer}\n\nDiagram: {diagram_description}\n\nEvaluate this system design response."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("score", 5)
    parsed.setdefault("strengths", ["Attempted to address the problem"])
    parsed.setdefault("improvements", ["Could provide more detail on scalability"])
    parsed.setdefault("missing_concepts", [])
    parsed.setdefault("ideal_design", "A comprehensive answer covering all 10 evaluation criteria with specific examples and trade-off analysis.")

    return parsed