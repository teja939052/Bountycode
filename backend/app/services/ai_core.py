"""Core AI infrastructure: HTTP client, circuit breaker, caching, retry.

Provides the primary chat_completion() interface to OpenRouter with fallback
models, circuit breaker protection, request metrics, and response caching.
"""
import json
import time
import hashlib
import asyncio
import logging
import random
from typing import List, Dict, Any, Optional
import httpx
from app.config import get_settings
from app.services.cache import cache
from app.services.request_metrics import metrics as request_metrics
from app.services.resilience import call_with_resilience
from app.services.circuit_breaker import ai_breaker

logger = logging.getLogger(__name__)
settings = get_settings()

MAX_RETRIES = settings.OPENROUTER_MAX_RETRIES
RETRY_DELAY = 1.0

FALLBACK_MODELS = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
]

COMPANY_TAGS = ["TCS", "Infosys", "Wipro", "Cognizant", "HCL Tech", "Accenture", "Capgemini",
                 "Tech Mahindra", "L&T Infotech", "Mphasis", "Hexaware", "IBM", "Flipkart",
                 "Zomato", "Razorpay", "Google", "Microsoft", "Amazon"]
MASS_RECRUITERS = ["TCS", "Infosys", "Wipro", "Cognizant"]


def assign_companies(count: int = None) -> List[str]:
    """Assign random company tags weighted toward mass recruiters.

    Args:
        count: Number of companies to select (clamped between 2 and 5).
            Defaults to a random integer in [2, 5].

    Returns:
        List[str]: Sorted list of unique company name strings.
    """
    if count is None:
        count = random.randint(2, 5)
    count = max(2, min(5, count))
    weighted = list(COMPANY_TAGS)
    for c in MASS_RECRUITERS:
        weighted.extend([c, c])
    selected = set()
    while len(selected) < count and weighted:
        pick = random.choice(weighted)
        selected.add(pick)
        weighted = [c for c in weighted if c != pick]
    return sorted(selected)


_http_client: Optional[httpx.AsyncClient] = None


def _http2_supported() -> bool:
    """Check if the HTTP/2 package is installed.

    Returns:
        bool: True if the h2 package is importable, False otherwise.
    """
    try:
        import h2  # noqa: F401

        return True
    except ImportError:
        return False


async def _get_http_client() -> httpx.AsyncClient:
    """Get or create the singleton Async HTTP client for OpenRouter.

    Configures connection limits, timeouts, and optional HTTP/2 support.

    Returns:
        httpx.AsyncClient: Shared async HTTP client instance.
    """
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.OPENROUTER_TIMEOUT, connect=10.0),
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
                keepalive_expiry=30.0,
            ),
            http2=_http2_supported(),
        )
        logger.info("HTTP client initialized for AI service")
    return _http_client


async def close_http_client():
    """Close the shared HTTP client and release resources."""
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
        _http_client = None
        logger.info("HTTP client closed")


async def _check_circuit_breaker() -> bool:
    """Check if the AI circuit breaker allows a new request.

    Returns:
        bool: True if requests are allowed (closed or recovered half-open).
    """
    return await ai_breaker.allow_request()


async def _record_failure():
    """Record an AI service failure on the circuit breaker."""
    await ai_breaker.record_failure()


async def _record_success():
    """Record an AI service success and reset the circuit breaker."""
    await ai_breaker.record_success()


def _make_cache_key(messages: List[Dict], model: str) -> str:
    """Generate a short SHA-256 cache key from messages and model name.

    Args:
        messages: List of chat message dicts.
        model: Model identifier string.

    Returns:
        str: 16-character hex cache key.
    """
    content = json.dumps(messages, sort_keys=True) + model
    return hashlib.sha256(content.encode()).hexdigest()[:16]


async def _call_openrouter(messages: List[Dict], model: str) -> str:
    """Execute a single chat completion call to OpenRouter.

    Args:
        messages: List of chat message dicts for the completion request.
        model: Model identifier string (e.g., 'google/gemini-2.0-flash-001').

    Returns:
        str: The model's response content string.

    Raises:
        ValueError: If OPENROUTER_API_KEY is not configured.
        httpx.TimeoutException: If the request times out.
        httpx.HTTPStatusError: If OpenRouter returns a non-2xx status.
        Exception: For any other network or parsing errors.
    """
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not configured")

    client = await _get_http_client()
    started = time.perf_counter()

    try:
        response = await client.post(
            settings.OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://placementpro.app",
                "X-Title": "PlacementPro",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000,
                "top_p": 0.9,
            },
            timeout=settings.OPENROUTER_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        await request_metrics.record("ai", "success", duration_ms=(time.perf_counter() - started) * 1000)
        return content
    except httpx.TimeoutException as e:
        logger.warning(f"OpenRouter timeout for model {model}: {e}")
        await request_metrics.record("ai", "failure", duration_ms=(time.perf_counter() - started) * 1000, error="timeout")
        raise
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.warning(f"Rate limit hit for model {model}, waiting before retry")
        elif e.response.status_code >= 500:
            logger.warning(f"OpenRouter server error for model {model}: {e}")
        else:
            logger.error(f"OpenRouter error for model {model}: {e}")
        await request_metrics.record("ai", "failure", duration_ms=(time.perf_counter() - started) * 1000, error=str(e))
        raise
    except Exception as e:
        logger.error(f"Unexpected error calling OpenRouter: {e}")
        await request_metrics.record("ai", "failure", duration_ms=(time.perf_counter() - started) * 1000, error=str(e))
        raise


async def chat_completion(
    messages: List[Dict],
    model: Optional[str] = None,
    use_cache: bool = True,
    temperature: float = 0.7,
    max_tokens: int = 2000,
) -> str:
    """Execute a chat completion with caching, retry, and fallback models.

    Attempts the primary model first. If the circuit breaker is open, iterates
    through fallback models. If the primary is allowed, tries it with retries,
    then falls back to alternative models on failure. Caches successful responses
    for 1 hour.

    Args:
        messages: List of chat message dicts (role + content).
        model: Model identifier override. Defaults to settings.OPENROUTER_MODEL.
        use_cache: Whether to read/write responses from the AI cache.
        temperature: Sampling temperature (passed to OpenRouter).
        max_tokens: Maximum tokens to generate (passed to OpenRouter).

    Returns:
        str: The model's response content string.

    Raises:
        Exception: If all primary and fallback models fail or the circuit breaker
            remains open after recovery attempts.
    """
    primary_model = model or settings.OPENROUTER_MODEL

    if use_cache:
        cache_key = _make_cache_key(messages, primary_model)
        cached = await cache.get("ai", cache_key)
        if cached:
            logger.debug(f"Cache hit for {primary_model}")
            await request_metrics.record("ai", "cache_hit")
            return cached

    if not await _check_circuit_breaker():
        for fallback in FALLBACK_MODELS:
            if fallback != primary_model:
                try:
                    result = await call_with_resilience(
                        _call_openrouter,
                        ai_breaker,
                        "ai",
                        1,
                        0.5,
                        request_metrics,
                        messages,
                        fallback,
                    )
                    await _record_success()
                    if use_cache:
                        cache_key = _make_cache_key(messages, primary_model)
                        await cache.set("ai", cache_key, result, ttl=3600)
                    return result
                except Exception as e:
                    logger.warning(f"Fallback model {fallback} failed: {e}")
                    continue
        raise Exception("AI service temporarily unavailable (circuit breaker open)")

    models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]

    for model_to_use in models_to_try:
        try:
            result = await call_with_resilience(
                _call_openrouter,
                ai_breaker,
                "ai",
                MAX_RETRIES,
                RETRY_DELAY,
                request_metrics,
                messages,
                model_to_use,
            )
            await _record_success()
            if use_cache:
                cache_key = _make_cache_key(messages, primary_model)
                await cache.set("ai", cache_key, result, ttl=3600)
            return result
        except Exception as e:
            logger.error(f"AI call failed for {model_to_use}: {e}")
            continue

    raise Exception("AI service temporarily unavailable")


def parse_json(text: str) -> Dict[str, Any]:
    """Parse a JSON string from AI model output with multiple fallback strategies.

    Handles markdown code fences, trailing fences, substring extraction
    (first object or array), and single-quote replacement.

    Args:
        text: Raw text output from an AI model.

    Returns:
        Dict[str, Any]: Parsed JSON object.

    Raises:
        ValueError: If the text cannot be parsed as JSON after all fallback attempts.
    """
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    start = text.find("[")
    end = text.rfind("]") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    try:
        fixed = text.replace("'", '"')
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass

    logger.error(f"Failed to parse JSON from: {text[:200]}...")
    raise ValueError(f"Could not parse JSON from AI response: {text[:200]}...")