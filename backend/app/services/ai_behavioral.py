"""Behavioral interview AI functions."""

import logging
from typing import Dict, Any
from app.services.ai_core import chat_completion, parse_json

logger = logging.getLogger(__name__)


async def generate_behavioral_question(
    company: str,
    role: str,
    count: int = 5,
) -> Dict[str, Any]:
    system_prompt = f"""You are an expert behavioral interview question generator for {company} interviews.

Generate {count} behavioral interview questions for a {role} position.
Use the STAR method (Situation, Task, Action, Result) as the framework.
Questions should cover leadership, teamwork, conflict resolution, problem-solving, and adaptability.

The output MUST be valid JSON:
{{
    "questions": [
        {{
            "question": "Tell me about a time when...",
            "category": "leadership|teamwork|conflict|problem-solving|adaptability",
            "follow_up": "What was the outcome? How did you measure success?"
        }}
    ]
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate {count} behavioral questions for {role} at {company}."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("questions", [])
    for q in parsed["questions"]:
        q.setdefault("question", "Tell me about a challenging situation you faced.")
        q.setdefault("category", "problem-solving")
        q.setdefault("follow_up", "What was the outcome?")

    return parsed


async def generate_interview_tips(
    company: str,
    role: str,
    interview_type: str = "behavioral",
) -> Dict[str, Any]:
    system_prompt = f"""You are an expert interview coach specializing in {company} interviews.

Provide actionable tips for a {role} position {interview_type} interview.

The output MUST be valid JSON:
{{
    "tips": [
        "Tip 1: Specific actionable advice",
        "Tip 2: What to prepare",
        "Tip 3: Common mistakes to avoid"
    ],
    "common_questions": [
        "Question 1",
        "Question 2"
    ],
    "do's": ["Do 1", "Do 2"],
    "don'ts": ["Don't 1", "Don't 2"]
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Provide interview tips for {role} at {company} ({interview_type} interview)."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("tips", ["Prepare specific examples using the STAR method", "Research the company thoroughly", "Practice your answers out loud"])
    parsed.setdefault("common_questions", ["Tell me about yourself", "Why do you want to work here?", "What is your greatest weakness?"])
    parsed.setdefault("do's", ["Use the STAR method to structure answers", "Quantify your achievements", "Ask thoughtful questions at the end"])
    parsed.setdefault("don'ts", ["Don't speak negatively about previous employers", "Don't give generic answers", "Don't interrupt the interviewer"])

    return parsed


async def generate_mentor_message(
    topic: str,
    level: str = "intermediate",
) -> Dict[str, Any]:
    system_prompt = f"""You are an experienced coding mentor. Explain the concept of "{topic}" clearly.

Target audience: {level} level developer.

The output MUST be valid JSON:
{{
    "explanation": "Clear, beginner-friendly explanation of the concept",
    "example": "A simple code example or analogy",
    "common_mistakes": ["Mistake 1", "Mistake 2"],
    "best_practices": ["Practice 1", "Practice 2"],
    "further_reading": ["Resource 1", "Resource 2"]
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Explain {topic} to a {level} developer."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("explanation", f"{topic} is an important concept in software development.")
    parsed.setdefault("example", "Think of it like organizing a library — books (data) need a system to find them quickly.")
    parsed.setdefault("common_mistakes", ["Overcomplicating the solution", "Not considering edge cases"])
    parsed.setdefault("best_practices", ["Start with the simplest approach", "Test with real data"])
    parsed.setdefault("further_reading", [])

    return parsed