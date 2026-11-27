"""System Design tests — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.middleware.auth import get_current_user
from app.services.ai_core import chat_completion, parse_json
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/system-design-tests", tags=["system-design-tests"])

_SD_CATEGORIES: Dict[str, dict] = {
    "hld": {
        "name": "High-Level Design (HLD)",
        "icon": "🏗️",
        "description": "System architecture, scalability, distributed systems",
        "subcategories": {
            "Social Media": "Twitter, Instagram, WhatsApp, News Feed",
            "E-commerce": "Amazon, Food Delivery, Ride-sharing",
            "Streaming": "YouTube, Netflix, Live Streaming",
            "Infrastructure": "URL Shortener, Rate Limiter, Cache, CDN",
            "Data": "Search Engine, Analytics, Data Pipelines",
            "Finance": "Payment Systems, Banking",
        },
    },
    "mld": {
        "name": "Machine Learning Design",
        "icon": "🤖",
        "description": "ML systems, recommendation engines, feature stores",
        "subcategories": {
            "Recommendation": "Netflix, YouTube, TikTok",
            "Search": "Google, Bing, Elasticsearch",
            "LLM": "ChatGPT, Claude, Llama",
        },
    },
}


class TestResult(BaseModel):
    question_id: str
    answer: str
    time_taken: int


@router.get("/categories")
async def list_categories():
    """List available system design categories."""
    return {"categories": _SD_CATEGORIES}


@router.get("/bank")
async def list_bank_questions():
    """List all system design bank questions."""
    return {"questions": []}


@router.post("/evaluate")
async def evaluate_design(
    result: TestResult,
    user=Depends(get_current_user),
):
    """Evaluate a system design answer."""
    eval_result = await chat_completion(
        messages=[
            {"role": "system", "content": "You are a system design interviewer. Evaluate the answer."},
            {"role": "user", "content": f"Question ID: {result.question_id}\nAnswer: {result.answer}"},
        ],
        use_cache=False,
    )
    parsed = parse_json(eval_result)
    await record_practice(user["id"], "system_design", score=parsed.get("score", 5))
    return parsed


@router.get("/leaderboard")
async def leaderboard():
    """Get system design leaderboard."""
    return {"leaderboard": []}