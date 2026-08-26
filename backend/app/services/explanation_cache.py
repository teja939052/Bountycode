import logging
from datetime import datetime, timezone

from app.database import question_explanations_collection
from app.services.ai_core import chat_completion, parse_json
from app.services.cache import cache

logger = logging.getLogger(__name__)

EXPLANATION_TTL_SECONDS = 60 * 60 * 24 * 30


async def get_cached_explanation(question_id: str, language: str = "python"):
    try:
        cached = await cache.get("question_explanations", f"{question_id}:{language}")
        if cached:
            return cached
    except Exception:
        pass

    doc = await question_explanations_collection().find_one({
        "question_id": question_id,
        "language": language,
    })
    if doc:
        payload = doc.get("payload")
        try:
            await cache.set("question_explanations", f"{question_id}:{language}", payload, EXPLANATION_TTL_SECONDS)
        except Exception:
            pass
        return payload
    return None


async def generate_explanation(question, language: str = "python") -> dict:
    prompt = f"""You are a placement coach explaining a coding problem to a beginner. Do NOT evaluate any student answer — just teach the concept clearly.

Question: {question.get("question", "") or question.get("question_title", "")}
Topic: {question.get("topic", "")}
Companies: {', '.join(question.get("companies", []))}
Difficulty: {question.get("difficulty", "")}
Language: {language}

Respond in this exact JSON format:
{{
  "approach": "<2-3 sentence plain-language explanation of the right way to think about it>",
  "steps": ["<step1>", "<step2>", "<step3>"],
  "algorithm": "<name of the best algorithm, e.g. 'Two Pointers', 'Binary Search', 'DP'>",
  "time_complexity": "O(n)",
  "space_complexity": "O(1)",
  "common_mistakes": ["<mistake1>", "<mistake2>"],
  "analogy": "<one short real-world analogy a non-expert can relate to>"
}}

Be direct and concrete. Keep steps to 3-5. Assume the student has minimal coding background."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=False,
            max_tokens=1200,
        )
        parsed = parse_json(result)
    except Exception as e:
        logger.warning("Failed to generate explanation for %s: %s", question.get("id"), e)
        parsed = {
            "approach": "Break the problem into smaller pieces, solve each one, then combine.",
            "steps": ["Understand the input and expected output", "Identify the simplest correct approach", "Optimize if needed"],
            "algorithm": "Brute force first, optimize later",
            "time_complexity": "O(n^2)",
            "space_complexity": "O(1)",
            "common_mistakes": ["Jumping straight to the optimized solution", "Missing edge cases"],
            "analogy": "Like building a house — lay the foundation before adding the roof.",
        }

    return parsed


async def get_or_create_explanation(question, language: str = "python") -> dict:
    question_id = question.get("id", "")
    existing = await get_cached_explanation(question_id, language)
    if existing:
        return existing

    payload = await generate_explanation(question, language)
    try:
        await question_explanations_collection().update_one(
            {"question_id": question_id, "language": language},
            {"$set": {
                "payload": payload,
                "question_title": question.get("question", "") or question.get("question_title", ""),
                "topic": question.get("topic", ""),
                "difficulty": question.get("difficulty", ""),
                "created_at": datetime.now(timezone.utc),
            }},
            upsert=True,
        )
        await cache.set("question_explanations", f"{question_id}:{language}", payload, EXPLANATION_TTL_SECONDS)
    except Exception as e:
        logger.warning("Failed to persist explanation for %s: %s", question_id, e)

    return payload
