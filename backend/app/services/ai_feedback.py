"""
Sentence-level AI feedback for interview/question answers.
Provides per-sentence scoring and specific improvement suggestions.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
from app.services.ai_core import chat_completion, parse_json


_SENTENCE_PROMPT = """
You are an expert placement coach. Analyze the user's answer sentence-by-sentence.

User question/topic: {topic}
Ideal answer characteristics: {ideal}

User answer:
{answer}

Return ONLY valid JSON with this exact schema:
{{
  "overall_score": <1-10>,
  "sentences": [
    {{
      "sentence": "<exact sentence from user's answer>",
      "score": <1-10>,
      "suggestion": "<specific rewrite or improvement>",
      "reason": "<why this matters for placements>"
    }}
  ],
  "top_strengths": ["<strength1>", "<strength2>"],
  "top_improvements": ["<improvement1>", "<improvement2>"]
}}

Rules:
- Split the user's answer into sentences.
- Score each sentence individually.
- Be specific: mention exact words/phrases to change.
- If the answer is too short, return fewer sentence objects.
- Do NOT hallucinate improvements that contradict the user's intent.
"""


def _split_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 5]


async def sentence_level_feedback(
    answer: str,
    topic: str = "",
    ideal: str = "Clear, structured, uses STAR method, includes metrics, shows technical depth",
) -> Dict[str, Any]:
    if not answer or not answer.strip():
        return {
            "overall_score": 0,
            "sentences": [],
            "top_strengths": [],
            "top_improvements": ["Answer is empty. Provide a detailed response."],
        }

    sentences = _split_sentences(answer)
    if not sentences:
        return {
            "overall_score": 3,
            "sentences": [],
            "top_strengths": [],
            "top_improvements": ["Answer too short. Expand with specific examples and results."],
        }

    prompt = _SENTENCE_PROMPT.format(
        topic=topic or "General interview question",
        ideal=ideal,
        answer=answer,
    )

    try:
        raw = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=False,
            max_tokens=2000,
        )
        data = parse_json(raw) or {}
    except Exception:
        data = {}

    # Fallback if AI didn't return sentence-level detail
    if not data.get("sentences"):
        data = {
            "overall_score": data.get("overall_score", 5),
            "sentences": [
                {
                    "sentence": s,
                    "score": 5,
                    "suggestion": "Add specific metrics and outcomes to strengthen this point.",
                    "reason": "Quantified achievements stand out to interviewers.",
                }
                for s in sentences[:5]
            ],
            "top_strengths": data.get("top_strengths", ["Attempted the question"]),
            "top_improvements": data.get("top_improvements", ["Add more specific examples"]),
        }

    return data
