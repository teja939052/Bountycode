"""Behavioral interview AI functions."""

import logging
from typing import Dict, Any, List
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
    mentor_name: str,
    current_day: int = 1,
    yesterday_completed: int = 0,
    topic: str = "",
    level: str = "intermediate",
) -> Dict[str, Any] | str:
    """Generate a personalized mentor message for daily challenge.

    When called with (mentor_name, current_day, yesterday_completed) — the
    daily-challenge pattern — returns a motivational string.  When called with
    (topic, level) — the original conceptual-explanation pattern — returns a
    JSON dict with explanation and examples.

    Args:
        mentor_name: Mentor character name (or topic in legacy mode).
        current_day: Current day number in the challenge.
        yesterday_completed: Number of quests completed yesterday.
        topic: Concept to explain (only used in legacy mode).
        level: Difficulty level (only used in legacy mode).

    Returns:
        str or Dict: Motivational message string (daily challenge mode) or
            explanation dict (legacy mode).
    """
    if topic:
        return await _generate_topic_explanation(topic, level)
    return await _generate_daily_mentor_message(mentor_name, current_day, yesterday_completed)


async def _generate_daily_mentor_message(
    mentor_name: str,
    current_day: int,
    yesterday_completed: int,
) -> str:
    """Generate a motivational mentor message for the daily challenge."""
    system_prompt = f"""You are a motivational coding mentor named "{mentor_name}".

Current day: {current_day} of a 30-day placement prep challenge.
Yesterday's completed quests: {yesterday_completed}.

Write a short (1-2 sentence) motivational message.
- If yesterday_completed > 0, acknowledge the streak.
- If yesterday_completed == 0, gently encourage them to get back on track.
- Reference the day number and keep it personal.

Return ONLY the message text, no JSON, no quotes, no markdown."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a day {current_day} mentor message."},
    ]

    try:
        result = await chat_completion(messages, max_tokens=200)
        return result.strip().strip('"').strip("'")
    except Exception:
        fallback = f"Day {current_day} — Let's make it count, {mentor_name} believes in you!"
        return fallback


async def _generate_topic_explanation(
    topic: str,
    level: str = "intermediate",
) -> Dict[str, Any]:
    """Generate a topic explanation for the mentor."""
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
