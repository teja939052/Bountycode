"""Cover letter and LinkedIn AI functions."""

import logging
from typing import Dict, Any
from app.services.ai_core import chat_completion, parse_json

logger = logging.getLogger(__name__)


async def generate_cover_letter(
    resume_text: str,
    job_description: str,
    company_name: str,
) -> Dict[str, Any]:
    system_prompt = """You are an expert cover letter writer. Generate a compelling, tailored cover letter.

GUIDELINES:
- Open with a strong hook that connects to the company
- Reference specific skills from the resume that match the JD
- Show knowledge of the company (mission, products, values)
- Keep it to 3-4 paragraphs
- Professional but personable tone
- Close with a clear call to action

The output MUST be valid JSON:
{
    "cover_letter": "The full cover letter text..."
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Write a cover letter for {company_name}.\n\nRESUME:\n{resume_text[:2000]}\n\nJOB DESCRIPTION:\n{job_description[:1500]}"},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)
    parsed.setdefault("cover_letter", f"Dear Hiring Manager,\n\nI am writing to express my interest in the position at {company_name}...")

    return parsed


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