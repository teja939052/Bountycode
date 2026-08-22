"""Salary and negotiation AI functions."""

import json
import logging
from typing import Dict, Any, List
from app.services.ai_core import chat_completion, parse_json

logger = logging.getLogger(__name__)


async def generate_salary_negotiation_tips(
    job_title: str,
    offered_salary: float,
    location: str,
    years_experience: int,
    company_size: str,
    benefits: str,
) -> Dict[str, Any]:
    system_prompt = """You are an expert salary negotiation coach. Provide actionable negotiation advice.

The output MUST be valid JSON:
{
    "market_research": "Summary of market rate for this role/location",
    "negotiation_points": [
        "Point 1: reason to negotiate higher",
        "Point 2: leverage point"
    ],
    "scripts": {
        "opening": "What to say to start the negotiation",
        "counter": "How to present a counter-offer",
        "benefits_fallback": "If they can't increase salary, ask for these benefits",
        "closing": "How to close the negotiation professionally"
    },
    "dos": [
        "Do 1: Specific negotiation best practice"
    ],
    "donts": [
        "Don't 1: Common negotiation mistake to avoid"
    ]
}

Provide at least 5 dos and 5 donts. Scripts should be word-for-word scripts they can use.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Negotiate for: {job_title} at offered ${offered_salary:,.0f}/yr\nLocation: {location}\nExperience: {years_experience} years\nCompany size: {company_size}\nBenefits: {benefits}"},
    ]

    result = await chat_completion(messages, max_tokens=3000)
    parsed = parse_json(result)

    parsed.setdefault("market_research", "Market research data not available.")
    parsed.setdefault("negotiation_points", ["Consider your total compensation package"])
    parsed.setdefault("scripts", {
        "opening": "Thank you for the offer. I'm excited about this opportunity.",
        "counter": "Based on my research and experience, I'd like to discuss a salary of...",
        "benefits_fallback": "If salary flexibility is limited, I'd like to discuss...",
        "closing": "I appreciate the discussion and look forward to finalizing the details.",
    })
    parsed.setdefault("dos", ["Research market rates thoroughly", "Practice your pitch beforehand"])
    parsed.setdefault("donts", ["Don't give a number first", "Don't accept immediately"])

    return parsed


async def generate_salary_benchmark(
    job_title: str,
    location: str,
    company: str,
    years_experience: int,
    level: str,
) -> Dict[str, Any]:
    system_prompt = """You are a compensation data analyst. Provide salary benchmark information.

Use your knowledge of tech industry salaries (2024-2025 data). Be realistic and specific.

The output MUST be valid JSON:
{
    "market_rate": {"min": 80000, "median": 110000, "max": 150000, "currency": "USD"},
    "percentiles": {"p10": 75000, "p25": 90000, "p50": 110000, "p75": 135000, "p90": 160000},
    "factors_affecting_pay": [
        "Factor 1 that influences salary positively",
        "Factor 2"
    ],
    "companies_paying_above_market": [
        {"company": "Company Name", "range": "$120K-$160K", "notes": "Why they pay more"}
    ]
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Benchmark salary for: {job_title} at {level} level\nLocation: {location}\nExperience: {years_experience} years\nCompany: {company}"},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("market_rate", {"min": 0, "median": 0, "max": 0, "currency": "USD"})
    parsed.setdefault("percentiles", {"p10": 0, "p25": 0, "p50": 0, "p75": 0, "p90": 0})
    parsed.setdefault("factors_affecting_pay", ["Location", "Experience", "Company size"])
    parsed.setdefault("companies_paying_above_market", [])

    return parsed


async def generate_offer_comparison(offers: List[Dict[str, Any]]) -> Dict[str, Any]:
    system_prompt = """You are a career advisor helping compare job offers.
Analyze each offer holistically — not just salary, but benefits, growth, culture, and work-life balance.

The output MUST be valid JSON:
{
    "winner": "Company Name",
    "winner_reason": "Detailed explanation of why this offer wins overall",
    "comparison_matrix": {
        "Company1": {
            "salary_score": 8,
            "benefits_score": 7,
            "growth_score": 9,
            "work_life_score": 6,
            "total_score": 30,
            "pros": ["Pro 1", "Pro 2"],
            "cons": ["Con 1"]
        },
        "Company2": {
            "salary_score": 9,
            "benefits_score": 8,
            "growth_score": 6,
            "work_life_score": 7,
            "total_score": 30,
            "pros": ["Pro 1"],
            "cons": ["Con 1", "Con 2"]
        }
    },
    "recommendation": "Personalized recommendation paragraph explaining the trade-offs"
}

Score each dimension 1-10. Total is sum of all dimensions. Consider the full picture.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Compare these job offers:\n\n{json.dumps(offers, indent=2)}"},
    ]

    result = await chat_completion(messages, max_tokens=3000)
    parsed = parse_json(result)

    parsed.setdefault("winner", offers[0].get("company", "Option A") if offers else "N/A")
    parsed.setdefault("winner_reason", "Based on overall compensation and opportunities.")
    parsed.setdefault("comparison_matrix", {})
    parsed.setdefault("recommendation", "Consider both short-term and long-term career goals.")

    return parsed