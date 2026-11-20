"""
AI Gateway — centralized, controlled access to all LLM providers.

Every AI call in Bountycode flows through this gateway. No frontend component
or domain engine may call an LLM provider directly.

Responsibilities:
  - Provider selection and model routing
  - Prompt-template versioning
  - Structured JSON output with schema validation
  - Token budgets and cost tracking
  - Privacy filtering (PII removal before sending to AI)
  - Request tracing (correlation IDs)
  - Fallback behavior (circuit breaker from ai_core)
  - Rate limits and quotas

AI failure must never stop core quizzes, deterministic scoring, readiness, or
learning progression. The gateway degrades gracefully.

Dependency direction:
    Routes / Domain Engines → AI Gateway → ai_core.chat_completion → OpenRouter
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.ai_core import chat_completion as _chat_completion, parse_json
from app.services.request_metrics import metrics as request_metrics

logger = logging.getLogger(__name__)

# ─── Prompt template versions ──────────────────────────────────────────────
# Increment when a prompt template changes. All AI calls include the template
# version so responses can be audited against the exact prompt used.
PROMPT_TEMPLATE_VERSIONS: Dict[str, str] = {
    "explain_mistake": "v1.0",
    "tutor_explanation": "v1.0",
    "interview_evaluate": "v1.0",
    "resume_analyze": "v1.0",
    "ats_optimize": "v1.0",
    "cover_letter_generate": "v1.0",
    "system_design_evaluate": "v1.0",
    "behavioral_evaluate": "v1.0",
    "coding_hint": "v1.0",
    "aptitude_explain": "v1.0",
    "coding_review": "v1.0",
    "project_generate": "v1.0",
}

# ─── PII patterns — removed before sending to AI ───────────────────────────
_PII_PATTERNS: List[tuple[str, str]] = [
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
    (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),
    (r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[CARD]"),
    (r"\b[A-Za-z0-9]{20,}\b", "[TOKEN]"),  # Long alphanumeric strings (API keys, etc.)
]

# ─── Cost tracking (approximate, per 1K tokens) ────────────────────────────
# These are planning estimates; actual costs come from OpenRouter response headers.
COST_PER_1K_TOKENS: Dict[str, float] = {
    "google/gemini-2.0-flash-001": 0.0004,
    "meta-llama/llama-3.1-8b-instruct:free": 0.0,
    "microsoft/phi-3-mini-128k-instruct:free": 0.0,
    "deepseek/deepseek-chat-v3-0324:free": 0.0,
    "nvidia/nemotron-3.5-lightning:free": 0.0,
}


def _strip_pii(text: str) -> str:
    """Remove personally identifiable information from text before AI submission."""
    result = text
    for pattern, replacement in _PII_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 characters per token for English text."""
    return max(1, len(text) // 4)


class AIGatewayError(Exception):
    """Raised when the AI gateway cannot produce a valid response."""


async def ai_complete(
    *,
    task: str,
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    user_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    response_schema: Optional[Dict[str, Any]] = None,
    strip_pii: bool = True,
) -> Dict[str, Any]:
    """Central AI completion entry point.

    All AI calls in Bountycode must go through this function. It applies
    privacy filtering, prompt-template versioning, cost tracking, and
    structured output validation.

    Args:
        task: Task identifier (used for prompt template versioning and metrics).
        messages: Chat messages (system, user, assistant).
        model: Override model selection (None = use ai_core default).
        temperature: Sampling temperature.
        max_tokens: Maximum output tokens.
        user_id: Opaque user identifier for metrics (no PII).
        correlation_id: Request tracing ID.
        response_schema: JSON schema for structured output validation.
        strip_pii: Remove PII from messages before sending to AI.

    Returns:
        Dict with keys: content, parsed (if schema provided), model, tokens,
        cost_estimate, template_version.

    Raises:
        AIGatewayError: If the AI response is invalid after retries.
    """
    template_version = PROMPT_TEMPLATE_VERSIONS.get(task, "unknown")

    # Strip PII from all message content
    safe_messages = []
    for msg in messages:
        content = msg.get("content", "")
        if strip_pii:
            content = _strip_pii(content)
        safe_messages.append({**msg, "content": content})

    # Estimate input tokens for cost tracking
    input_text = " ".join(m.get("content", "") for m in safe_messages)
    input_tokens = _estimate_tokens(input_text)

    try:
        result = await _chat_completion(
            messages=safe_messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as exc:
        logger.warning(
            "AI gateway failure",
            extra={
                "task": task,
                "user_id": user_id,
                "correlation_id": correlation_id,
                "error": str(exc)[:200],
            },
        )
        raise AIGatewayError(f"AI completion failed for task '{task}': {exc}") from exc

    content = result.get("content", "")
    model_used = result.get("model", "unknown")
    output_tokens = _estimate_tokens(content)
    total_tokens = input_tokens + output_tokens
    cost_estimate = (total_tokens / 1000) * COST_PER_1K_TOKENS.get(model_used, 0.0)

    # Track metrics
    request_metrics.record_ai_call(task, model_used, total_tokens, cost_estimate)

    # Parse structured output if schema provided
    parsed = None
    if response_schema:
        try:
            parsed = parse_json(content, response_schema)
        except Exception as exc:
            logger.warning(
                "AI response schema validation failed",
                extra={
                    "task": task,
                    "schema": str(response_schema)[:100],
                    "error": str(exc)[:200],
                    "raw_content": content[:200],
                },
            )
            # Don't fail — return raw content for fallback handling
            parsed = None

    return {
        "content": content,
        "parsed": parsed,
        "model": model_used,
        "tokens": total_tokens,
        "cost_estimate": round(cost_estimate, 6),
        "template_version": template_version,
        "task": task,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def ai_explain_mistake(
    *,
    skill_id: str,
    lesson_excerpt: str,
    question_statement: str,
    student_response: str,
    failure_class: str,
    hint_level: int = 1,
    preferred_language: str = "en",
    user_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Explain a student's mistake with a structured, schema-validated response.

    This is the canonical AI tutor path. All mistake explanations go through
    this function, ensuring consistent privacy filtering, prompt versioning,
    and output validation.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a patient coding tutor. Explain the student's mistake "
                "without giving away the answer. Use the approved lesson excerpt "
                "as reference. Respond in the requested language."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Skill: {skill_id}\n"
                f"Lesson excerpt: {lesson_excerpt}\n"
                f"Question: {question_statement}\n"
                f"Student answer: {student_response}\n"
                f"Failure class: {failure_class}\n"
                f"Hint level: {hint_level}\n"
                f"Language: {preferred_language}\n"
                "Provide: diagnosis (what went wrong), explanation (why), "
                "hint (one small nudge), next_step (what to try next)."
            ),
        },
    ]

    return await ai_complete(
        task="explain_mistake",
        messages=messages,
        user_id=user_id,
        correlation_id=correlation_id,
        response_schema={
            "type": "object",
            "properties": {
                "diagnosis": {"type": "string"},
                "explanation": {"type": "string"},
                "hint": {"type": "string"},
                "next_step": {"type": "string"},
                "confidence": {"type": "string"},
            },
            "required": ["diagnosis", "explanation", "hint", "next_step"],
        },
    )


# ─── Backward-compatible re-exports ────────────────────────────────────────
# Existing code imports chat_completion and parse_json from ai_core.
# The gateway wraps these; domain modules should migrate to ai_complete().

from app.services.ai_core import (  # noqa: E402
    chat_completion,
    parse_json,
    close_http_client,
    FALLBACK_MODELS,
    MAX_RETRIES,
    RETRY_DELAY,
)

__all__ = [
    "ai_complete",
    "ai_explain_mistake",
    "chat_completion",
    "parse_json",
    "close_http_client",
    "AIGatewayError",
    "PROMPT_TEMPLATE_VERSIONS",
]
