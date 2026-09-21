"""LinkedIn About AI function."""

import logging
from typing import Dict, Any
from app.services.ai_core import chat_completion, parse_json

logger = logging.getLogger(__name__)


async def generate_linkedin_about(
    resume_text: str,
    target_role: str,
) -> Dict[str, Any]:
    system_prompt = """You are a LinkedIn profile expert. Generate a compelling About section.

GUIDELINES:
- Write in first person
- Start with a hook (who you are, what drives you)
- Highlight key achievements and skills
- Use relevant keywords for recruiter searches
- End with a call to action (open to opportunities, let's connect)
- Keep it to 3-5 short paragraphs (under 2600 characters)
- Professional but personable

The output MUST be valid JSON:
{
    "linkedin_about": "The LinkedIn About section text..."
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Write a LinkedIn About section for someone targeting {target_role} roles.\n\nResume:\n{resume_text[:2000]}"},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)
    parsed.setdefault("linkedin_about", f"Passionate {target_role} professional with a track record of delivering impactful solutions...")

    return parsed
