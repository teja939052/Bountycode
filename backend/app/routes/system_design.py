"""System design routes — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import json
import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.services.ai_system_design import generate_system_design_question, evaluate_system_design_answer
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.config import get_settings

router = APIRouter(prefix="/api/v1/system-design", tags=["system-design"])
settings = get_settings()

# Canonical System Design bank (single source of truth, file-backed).
_SD_BANK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "system_design_bank.json"
)
_SD_BANK: List[dict] = []

# topic keyword -> bank sub_topic (served bank-first, AI fallback on miss)
_TOPIC_MAP: Dict[str, str] = {
    "url": "url_shortener",
    "shortener": "url_shortener",
    "rate": "rate_limiter",
    "limiter": "rate_limiter",
    "notification": "notification_service",
    "chat": "chat_system",
    "whatsapp": "chat_system",
    "messaging": "chat_system",
    "payment": "payment_system",
    "stripe": "payment_system",
    "queue": "job_queue",
    "job": "job_queue",
    "analytics": "analytics",
    "dashboard": "analytics",
    "feed": "social_feed",
    "social": "social_feed",
    "twitter": "social_feed",
    "cache": "distributed_cache",
    "inventory": "inventory",
    "ecommerce": "inventory",
    "e-commerce": "inventory",
    "shop": "inventory",
}


def _load_sd_bank() -> List[dict]:
    global _SD_BANK
    if not _SD_BANK:
        try:
            with open(_SD_BANK_PATH, "r", encoding="utf-8") as f:
                _SD_BANK = json.load(f)
        except Exception:
            _SD_BANK = []
    return _SD_BANK


def _pick_bank_question(difficulty: str, topic: str) -> Optional[dict]:
    """Return a bank entry (as AI-shaped data) if one matches, else None."""
    bank = _load_sd_bank()
    if not bank:
        return None
    topic_l = topic.lower()
    diff_l = difficulty.lower()
    candidates = [
        q for q in bank
        if q.get("topic", "").lower() == topic_l
        and q.get("difficulty", "").lower() == diff_l
    ]
    if not candidates:
        return None
    import random
    return random.choice(candidates)


@router.post("/question")
async def get_system_design_question(
    difficulty: str = "medium",
    topic: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Get a system design question."""
    await check_and_reset_monthly_usage(user["id"])

    # Try bank first
    q = _pick_bank_question(difficulty, topic or "url_shortener")
    if not q:
        # Fall back to AI generation
        q = await generate_system_design_question(difficulty, topic)

    return {"question": q}


@router.post("/answer")
async def evaluate_system_design_answer_endpoint(
    question_id: str,
    answer: str,
    user=Depends(get_current_user),
):
    """Evaluate a system design answer."""
    await check_and_reset_monthly_usage(user["id"])

    result = await evaluate_system_design_answer(question_id, answer)
    return result


@router.get("/topics")
async def list_topics():
    """List available system design topics."""
    return {"topics": list(_TOPIC_MAP.keys())}