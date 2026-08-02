"""Unified retry + circuit breaker wrapper for external calls."""
import asyncio
import logging
import time
from typing import Callable, Any, Awaitable

logger = logging.getLogger(__name__)


def _breaker_get(breaker, key, default=None):
    if isinstance(breaker, dict):
        return breaker.get(key, default)
    return getattr(breaker, key, default)


def _breaker_set(breaker, key, value):
    if isinstance(breaker, dict):
        breaker[key] = value
    else:
        setattr(breaker, key, value)


async def call_with_resilience(
    func: Callable[..., Awaitable[Any]],
    breaker,
    service_name: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
    metrics=None,
    *args,
    **kwargs,
) -> Any:
    """Execute func with retry, backoff, and circuit breaker protection.

    Args:
        func: Async callable to execute.
        breaker: CircuitBreaker object or mutable dict with keys
                 failures, last_failure_time, is_open, threshold, recovery_time.
        service_name: Human-readable label for logging / metrics.
        max_retries: Maximum number of retries (total attempts = max_retries + 1).
        base_delay: Base delay in seconds; doubles each attempt (exponential backoff).
        metrics: Optional RequestMetrics instance.
        *args, **kwargs: Positional and keyword arguments forwarded to func.
    """
    last_error = None
    for attempt in range(max_retries + 1):
        is_open = _breaker_get(breaker, "is_open", False)
        if is_open:
            elapsed = time.time() - _breaker_get(breaker, "last_failure_time", 0)
            recovery_time = _breaker_get(breaker, "recovery_time", 60)
            if elapsed > recovery_time:
                _breaker_set(breaker, "is_open", False)
                _breaker_set(breaker, "failures", 0)
                logger.info(f"Circuit breaker half-open for {service_name}")
            else:
                raise Exception(f"Circuit breaker open for {service_name}")

        started = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            _breaker_set(breaker, "failures", 0)
            _breaker_set(breaker, "is_open", False)
            duration = (time.perf_counter() - started) * 1000
            if metrics:
                await metrics.record(service_name, "success", duration)
            return result
        except Exception as e:
            last_error = e
            failures = _breaker_get(breaker, "failures", 0) + 1
            _breaker_set(breaker, "failures", failures)
            _breaker_set(breaker, "last_failure_time", time.time())
            threshold = _breaker_get(breaker, "threshold", 5)
            if failures >= threshold:
                _breaker_set(breaker, "is_open", True)
                logger.warning(f"Circuit breaker opened for {service_name}")

            duration = (time.perf_counter() - started) * 1000
            if metrics:
                await metrics.record(
                    service_name, "failure", duration, str(e)[:200]
                )

            if attempt < max_retries:
                jitter = asyncio.get_running_loop().time() % 1
                delay = base_delay * (2 ** attempt) + jitter
                logger.warning(
                    f"{service_name} attempt {attempt + 1} failed: {e}, "
                    f"retrying in {delay:.1f}s"
                )
                await asyncio.sleep(delay)

    raise last_error  # type: ignore[misc]